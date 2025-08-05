# signal_controller.py (Server)

from flask import Flask, jsonify, request, render_template_string
import time
import threading

app = Flask(__name__)

# Global state for traffic and pedestrian signals
road_states = {1: 'RED', 2: 'GREEN'}
pedestrian_states = {1: 'RED', 2: 'RED'}
signal_lock = threading.Lock()

# --- Visual Dashboard (HTML with SVG) ---
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Traffic Junction Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="2">
    <style>
        body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; background-color: #2c3e50; color: white; margin: 0; }
        .junction-container { display: flex; align-items: center; justify-content: center; position: relative; width: 600px; height: 600px; }
        .road-label { position: absolute; font-weight: bold; font-size: 1.2rem; }
        #road1-label { top: 20px; left: 50%; transform: translateX(-50%); }
        #road2-label { bottom: 20px; left: 50%; transform: translateX(-50%); }
        #ped1-label { top: 50%; left: 20px; transform: translateY(-50%) rotate(-90deg); }
        #ped2-label { top: 50%; right: 20px; transform: translateY(-50%) rotate(90deg); }
        .status-message { font-size: 1.2rem; margin-top: 20px; padding: 10px 20px; background: rgba(0,0,0,0.3); border-radius: 8px; }
    </style>
</head>
<body>
    <h1 style="margin-bottom: 40px;">Smart Traffic Junction Controller</h1>
    <div class="junction-container">
        <svg width="600" height="600" viewBox="0 0 600 600">
            <rect x="250" y="250" width="100" height="100" fill="#666" />
            <rect x="0" y="250" width="250" height="100" fill="#444" />
            <rect x="350" y="250" width="250" height="100" fill="#444" />
            <rect x="250" y="0" width="100" height="250" fill="#444" />
            <rect x="250" y="350" width="100" height="250" fill="#444" />
            <rect x="150" y="250" width="20" height="100" fill="white" />
            <rect x="430" y="250" width="20" height="100" fill="white" />
            <rect x="250" y="150" width="100" height="20" fill="white" />
            <rect x="250" y="430" width="100" height="20" fill="white" />
            <g id="road1-lights" transform="translate(250, 400)">
                <circle cx="25" cy="0" r="10" fill="red" class="light" id="road1-red"></circle>
                <circle cx="50" cy="0" r="10" fill="gray" class="light" id="road1-yellow"></circle>
                <circle cx="75" cy="0" r="10" fill="gray" class="light" id="road1-green"></circle>
            </g>
            <g id="road2-lights" transform="translate(250, 150)">
                <circle cx="25" cy="0" r="10" fill="gray" class="light" id="road2-red"></circle>
                <circle cx="50" cy="0" r="10" fill="gray" class="light" id="road2-yellow"></circle>
                <circle cx="75" cy="0" r="10" fill="green" class="light" id="road2-green"></circle>
            </g>
            <g id="ped1-lights" transform="translate(100, 250)">
                <rect x="0" y="0" width="20" height="40" fill="white" rx="5" />
                <path d="M5 10 L15 10 L15 30 L5 30 Z M10 5 L10 10 M10 30 L10 35 M5 25 L15 25" stroke="red" stroke-width="2" fill="none" class="ped-dont-walk" id="ped1-red"></path>
                <path d="M5 25 L10 20 L15 25 M10 20 L10 5 M5 5 L15 5 L15 15 L5 15 Z" stroke="gray" stroke-width="2" fill="none" class="ped-walk" id="ped1-green"></path>
            </g>
            <g id="ped2-lights" transform="translate(480, 250)">
                <rect x="0" y="0" width="20" height="40" fill="white" rx="5" />
                <path d="M5 10 L15 10 L15 30 L5 30 Z M10 5 L10 10 M10 30 L10 35 M5 25 L15 25" stroke="gray" stroke-width="2" fill="none" class="ped-dont-walk" id="ped2-red"></path>
                <path d="M5 25 L10 20 L15 25 M10 20 L10 5 M5 5 L15 5 L15 15 L5 15 Z" stroke="gray" stroke-width="2" fill="none" class="ped-walk" id="ped2-green"></path>
            </g>
        </svg>
        <div id="status-message" class="status-message"></div>
    </div>
    <script>
        const statusEl = document.getElementById('status-message');
        function updateLights(states) {
            document.querySelectorAll('.light').forEach(el => el.setAttribute('fill', 'gray'));
            document.querySelectorAll('.ped-walk, .ped-dont-walk').forEach(el => el.setAttribute('stroke', 'gray'));
            document.querySelectorAll('.ped-walk, .ped-dont-walk').forEach(el => el.setAttribute('fill', 'none'));
            
            // Update Road 1
            document.getElementById(`road1-${states.road_states[1].toLowerCase()}`).setAttribute('fill', states.road_states[1].toLowerCase());
            // Update Road 2
            document.getElementById(`road2-${states.road_states[2].toLowerCase()}`).setAttribute('fill', states.road_states[2].toLowerCase());
            
            // Update Pedestrian 1
            if (states.pedestrian_states[1] === 'GREEN') {
                document.getElementById('ped1-green').setAttribute('stroke', 'green');
                document.getElementById('ped1-green').setAttribute('fill', 'green');
            } else {
                document.getElementById('ped1-red').setAttribute('stroke', 'red');
            }
            // Update Pedestrian 2
            if (states.pedestrian_states[2] === 'GREEN') {
                document.getElementById('ped2-green').setAttribute('stroke', 'green');
                document.getElementById('ped2-green').setAttribute('fill', 'green');
            } else {
                document.getElementById('ped2-red').setAttribute('stroke', 'red');
            }
        }
        
        async function fetchStatus() {
            try {
                const response = await fetch('/status');
                const data = await response.json();
                updateLights(data);
                statusEl.textContent = data.message;
            } catch (error) {
                statusEl.textContent = 'Server not reachable.';
                console.error(error);
            }
        }
        setInterval(fetchStatus, 500); // Poll for status every half second
        fetchStatus();
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML)

@app.route('/status')
def get_status():
    with signal_lock:
        return jsonify({
            'road_states': road_states,
            'pedestrian_states': pedestrian_states,
            'message': f"Road 1: {road_states[1]}, Road 2: {road_states[2]} | Ped 1: {pedestrian_states[1]}, Ped 2: {pedestrian_states[2]}"
        })

@app.route('/control_vehicle', methods=['POST'])
def control_vehicle():
    data = request.get_json()
    target_road_id = int(data.get('road_id'))
    
    with signal_lock:
        if road_states[target_road_id] == 'GREEN':
            return jsonify({"status": "already_green", "message": f"Road {target_road_id} is already GREEN."})

        other_road_id = 1 if target_road_id == 2 else 2
        
        # Change other road to YELLOW then RED
        road_states[other_road_id] = 'YELLOW'
        time.sleep(3)
        road_states[other_road_id] = 'RED'
        time.sleep(1)
        
        # Change target road to GREEN
        road_states[target_road_id] = 'GREEN'
        
        return jsonify({"status": "success", "message": f"Signal changed. Road {target_road_id} is now GREEN."})

@app.route('/control_pedestrian', methods=['POST'])
def control_pedestrian():
    data = request.get_json()
    crossing_id = int(data.get('crossing_id'))
    
    with signal_lock:
        if road_states[crossing_id] == 'GREEN':
            return jsonify({"status": "wait", "message": f"Road {crossing_id} is GREEN for vehicles. Pedestrians must wait."})

        # Change pedestrian signal to GREEN
        pedestrian_states[crossing_id] = 'GREEN'
        time.sleep(10)
        
        # Flash for a bit
        pedestrian_states[crossing_id] = 'RED_FLASHING'
        time.sleep(3)
        
        # Turn RED
        pedestrian_states[crossing_id] = 'RED'
        
        return jsonify({"status": "success", "message": f"Pedestrian crossing {crossing_id} sequence completed."})

if __name__ == '__main__':
    print("Traffic Signal Controller Server starting on port 5000...")
    app.run(debug=True, host="0.0.0.0", port=5000)