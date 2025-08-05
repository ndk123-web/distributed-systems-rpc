# client_app.py (Client)

from flask import Flask, render_template_string

app = Flask(__name__)

# --- Client UI (HTML with JavaScript) ---
CLIENT_UI_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Smart Traffic Client</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; background-color: #34495e; color: white; margin: 0; }
        .container { text-align: center; background: #2c3e50; padding: 40px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); max-width: 600px; }
        h1 { margin-bottom: 20px; }
        .button-group { display: flex; flex-direction: column; gap: 15px; margin-top: 30px; }
        button { padding: 12px 25px; font-size: 1rem; font-weight: bold; border-radius: 8px; border: none; cursor: pointer; transition: background-color 0.3s; }
        .vehicle-btn { background-color: #2ecc71; color: white; }
        .vehicle-btn:hover { background-color: #27ae60; }
        .pedestrian-btn { background-color: #e74c3c; color: white; }
        .pedestrian-btn:hover { background-color: #c0392b; }
        #response-box { background: rgba(0,0,0,0.3); padding: 15px; margin-top: 20px; border-radius: 8px; text-align: left; white-space: pre-wrap; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Traffic Signal Client</h1>
        <p>Send RPC commands to the server to control the traffic and pedestrian signals.</p>

        <div class="button-group">
            <button class="vehicle-btn" onclick="sendRequest('/control_vehicle', {road_id: 1})">Switch to Road 1 (Lanes 1 & 2)</button>
            <button class="vehicle-btn" onclick="sendRequest('/control_vehicle', {road_id: 2})">Switch to Road 2 (Lanes 3 & 4)</button>
            <button class="pedestrian-btn" onclick="sendRequest('/control_pedestrian', {crossing_id: 1})">Request Pedestrian Crossing 1</button>
            <button class="pedestrian-btn" onclick="sendRequest('/control_pedestrian', {crossing_id: 2})">Request Pedestrian Crossing 2</button>
        </div>

        <div id="response-box">
            <p><strong>Response from Server:</strong></p>
            <pre id="response-text">Waiting for your command...</pre>
        </div>
    </div>

    <script>
        const responseTextEl = document.getElementById('response-text');

        async function sendRequest(endpoint, data) {
            responseTextEl.textContent = 'Sending request...';
            try {
                const response = await fetch(`http://localhost:5000${endpoint}`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                
                let message = `Status: ${result.status}\nMessage: ${result.message}`;
                responseTextEl.textContent = message;
            } catch (error) {
                responseTextEl.textContent = `Error: Could not connect to the server. Is it running?\nDetails: ${error.message}`;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(CLIENT_UI_HTML)

if __name__ == '__main__':
    print("Traffic Signal Client starting on port 5001...")
    app.run(debug=True, host="0.0.0.0", port=5001)