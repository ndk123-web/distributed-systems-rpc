# signal_controller.py (Server)

from flask import Flask, request, jsonify, render_template_string
import time
import threading

app = Flask(__name__)

# Global state for the traffic signals
# road_states[1] refers to Road 1 (Lanes 1 & 2)
# road_states[2] refers to Road 2 (Lanes 3 & 4)
# Initial state: Road 1 is RED, Road 2 is GREEN
# This means traffic on Road 2 (Lanes 3 & 4) can flow.
road_states = {
    1: 'RED',
    2: 'GREEN'
}

# A lock to ensure thread-safe access to the global road_states dictionary.
# This prevents race conditions when multiple requests or threads try to modify it.
signal_lock = threading.Lock()

# --- HTML Dashboard for Visualizing Signal Status ---
# This HTML provides a simple web interface to see the current state of both roads.
# It includes a meta refresh tag to automatically update the page every few seconds.
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Traffic Signal Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="3"> <!-- Auto-refresh every 3 seconds -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            background-color: #1a1a1a;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            font-family: 'Inter', sans-serif;
            color: white;
            padding: 20px;
        }
        .container {
            display: flex;
            flex-wrap: wrap;
            gap: 50px;
            margin-bottom: 30px;
            justify-content: center;
            align-items: center;
        }
        .signal-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .signal-box {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 24px;
            font-weight: bold;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
            transition: background-color 0.5s ease-in-out;
            border: 5px solid #333;
        }
        .signal-box.RED { background-color: red; color: white; }
        .signal-box.YELLOW { background-color: yellow; color: black; }
        .signal-box.GREEN { background-color: green; color: white; }
        .road-label {
            text-align: center;
            font-size: 18px;
            margin-top: 10px;
            font-weight: bold;
        }
        .status-message {
            font-size: 20px;
            margin-top: 20px;
            padding: 15px 30px;
            background-color: #333;
            border-radius: 8px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
            text-align: center;
        }
        @media (max-width: 768px) {
            .container {
                flex-direction: column;
                gap: 30px;
            }
            .signal-box {
                width: 120px;
                height: 120px;
                font-size: 20px;
            }
            .road-label {
                font-size: 16px;
            }
            .status-message {
                font-size: 18px;
                padding: 10px 20px;
            }
        }
    </style>
</head>
<body>
    <h1 class="text-3xl font-bold mb-8">Traffic Junction Status</h1>
    <div class="container">
        <div class="signal-wrapper">
            <div class="signal-box {{ road1_status }}">
                {{ road1_status }}
            </div>
            <div class="road-label">Road 1 (Lanes 1 & 2)</div>
        </div>
        <div class="signal-wrapper">
            <div class="signal-box {{ road2_status }}">
                {{ road2_status }}
            </div>
            <div class="road-label">Road 2 (Lanes 3 & 4)</div>
        </div>
    </div>
    <div class="status-message">
        Current Green Road: <span class="font-semibold">{{ current_green_road }}</span>
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """
    Web endpoint to display the current status of both traffic signals.
    This acts as a visual dashboard for the traffic junction.
    """
    with signal_lock:
        # Get the current status of each road from the global state
        road1_status = road_states[1]
        road2_status = road_states[2]
        # Determine which road is currently green for display purposes
        current_green_road_display = "Road 1 (Lanes 1 & 2)" if road_states[1] == 'GREEN' else "Road 2 (Lanes 3 & 4)"
    
    # Render the HTML template, passing the current statuses
    return render_template_string(
        DASHBOARD_HTML,
        road1_status=road1_status,
        road2_status=road2_status,
        current_green_road=current_green_road_display
    )

@app.route('/get_signal_status', methods=['GET'])
def get_signal_status():
    """
    RPC endpoint (GET) for the client to retrieve the current state of all traffic signals.
    Returns a JSON object containing the 'road_states' dictionary.
    """
    with signal_lock:
        # Return a copy of the current road_states to the client
        return jsonify(road_states)

def change_signal_sequence(target_road_id):
    """
    Manages the sequence of signal changes (Yellow -> Red -> Green).
    This function is designed to run in a separate thread to prevent
    blocking the main Flask application while waiting for signal transitions.
    """
    global road_states

    # Determine the ID of the other road (the one that needs to turn yellow/red)
    other_road_id = 1 if target_road_id == 2 else 2

    print(f"[{time.strftime('%H:%M:%S')}] Initiating signal change sequence:")
    print(f"  - Road {other_road_id} (Lanes {other_road_id*2-1} & {other_road_id*2}) will turn YELLOW then RED.")
    print(f"  - Road {target_road_id} (Lanes {target_road_id*2-1} & {target_road_id*2}) will turn GREEN.")

    # Phase 1: Other road turns YELLOW
    with signal_lock:
        road_states[other_road_id] = 'YELLOW'
    print(f"[{time.strftime('%H:%M:%S')}] Road {other_road_id} is now YELLOW. Waiting 5 seconds...")
    time.sleep(5) # Simulate the yellow light duration

    # Phase 2: Other road turns RED
    with signal_lock:
        road_states[other_road_id] = 'RED'
    print(f"[{time.strftime('%H:%M:%S')}] Road {other_road_id} is now RED. Brief pause...")
    time.sleep(2) # Brief pause before turning the target green

    # Phase 3: Target road turns GREEN
    with signal_lock:
        road_states[target_road_id] = 'GREEN'
    print(f"[{time.strftime('%H:%M:%S')}] Road {target_road_id} is now GREEN. Cycle complete.")


@app.route('/control_signal', methods=['POST'])
def control_signal():
    """
    RPC endpoint (POST) for the client to request a traffic signal manipulation.
    It expects a JSON payload with a 'lane_number' (1-4).
    """
    data = request.get_json() # Get the JSON data from the client's request

    # Validate input: Check if 'lane_number' is present and valid
    if not data or 'lane_number' not in data:
        return jsonify({"error": "Missing 'lane_number' in request payload"}), 400
    
    try:
        lane_number = int(data['lane_number'])
        if not (1 <= lane_number <= 4):
            return jsonify({"error": "Lane number must be between 1 and 4"}), 400
    except ValueError:
        return jsonify({"error": "Lane number must be an integer"}), 400

    # Determine which main road (1 or 2) the requested lane belongs to
    # Lanes 1 and 2 belong to Road 1; Lanes 3 and 4 belong to Road 2.
    target_road_id = 1 if lane_number in [1, 2] else 2
    other_road_id = 1 if target_road_id == 2 else 2

    with signal_lock: # Acquire the lock before accessing/modifying global state
        # Requirement: If the target road is already green, display "already green"
        if road_states[target_road_id] == 'GREEN':
            print(f"[{time.strftime('%H:%M:%S')}] Request for Lane {lane_number}: Road {target_road_id} is already GREEN. No change needed.")
            return jsonify({
                "status": "already_green",
                "message": f"Road {target_road_id} (Lanes {target_road_id*2-1} & {target_road_id*2}) is already GREEN."
            })

        # Prevent new signal changes if another transition is already in progress
        # (i.e., the other road is yellow or red, meaning it's transitioning from green)
        if road_states[other_road_id] == 'YELLOW' or road_states[other_road_id] == 'RED':
             print(f"[{time.strftime('%H:%M:%S')}] Request for Lane {lane_number}: Another signal change is in progress or just completed. Please wait.")
             return jsonify({
                 "status": "in_progress",
                 "message": "Another signal change is in progress or just completed. Please wait."
             })

        # If the target road is not green and no transition is ongoing,
        # initiate the signal change sequence in a new thread.
        print(f"[{time.strftime('%H:%M:%S')}] Request for Lane {lane_number}: Initiating signal change to make Road {target_road_id} GREEN.")
        thread = threading.Thread(target=change_signal_sequence, args=(target_road_id,))
        thread.start() # Start the new thread

    # Return an immediate success response to the client
    return jsonify({
        "status": "success",
        "message": f"Signal change initiated for Road {target_road_id} (Lanes {target_road_id*2-1} & {target_road_id*2})."
    })

if __name__ == '__main__':
    # When the server starts, print its initial state.
    print("Traffic Signal Controller Server starting...")
    print(f"Initial state: Road 1 (Lanes 1/2) is {road_states[1]}, Road 2 (Lanes 3/4) is {road_states[2]}.")
    # Run the Flask application.
    # debug=False for production environments.
    # host="0.0.0.0" makes the server accessible from other machines on the network.
    app.run(debug=True, host="0.0.0.0", port=5000)