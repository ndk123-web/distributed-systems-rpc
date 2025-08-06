# 🚦 Auto Pedestrian Traffic Server

from flask import Flask, jsonify, request, render_template_string
import threading
import time
import datetime
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

traffic_state = {
    'road1': 'RED',
    'road2': 'GREEN',
    'pedestrian1': 'RED',
    'pedestrian2': 'RED'
}

log_entries = []
system_stats = {
    'total_requests': 0,
    'vehicle_requests': 0,
    'server_start_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

lock = threading.Lock()

def add_log(log_type, action, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        'timestamp': timestamp,
        'type': log_type,
        'action': action,
        'message': message
    }
    log_entries.append(log_entry)
    if len(log_entries) > 100:
        log_entries.pop(0)
    socketio.emit('log_update', {
        'logs': log_entries[-10:],
        'stats': system_stats
    })

# Automatically update pedestrian signals based on road state

def update_pedestrian_signals():
    # If road is RED, pedestrian can cross (GREEN)
    traffic_state['pedestrian1'] = 'GREEN' if traffic_state['road1'] == 'RED' else 'RED'
    traffic_state['pedestrian2'] = 'GREEN' if traffic_state['road2'] == 'RED' else 'RED'
    socketio.emit('update', traffic_state)

@app.route('/api/control_vehicle', methods=['POST'])
def control_vehicle():
    data = request.get_json()
    road_id = data.get('road_id')
    with lock:
        if traffic_state[f'road{road_id}'] == 'GREEN':
            add_log('VEHICLE', f'Switch to Road {road_id}', f"Road {road_id} is already GREEN")
            return jsonify({"success": False, "message": f"Road {road_id} is already GREEN"})
    def vehicle_sequence():
        other_road_id = 2 if road_id == 1 else 1
        with lock:
            traffic_state[f'road{other_road_id}'] = 'YELLOW'
            traffic_state[f'road{road_id}'] = 'RED'
            socketio.emit('update', traffic_state)
            add_log('VEHICLE', f'Switch to Road {road_id}', f"Road {other_road_id} changed to YELLOW")
        time.sleep(3)
        with lock:
            traffic_state[f'road{other_road_id}'] = 'RED'
            socketio.emit('update', traffic_state)
            add_log('VEHICLE', f'Switch to Road {road_id}', f"Road {other_road_id} changed to RED")
        time.sleep(2)
        with lock:
            traffic_state[f'road{road_id}'] = 'GREEN'
            socketio.emit('update', traffic_state)
            add_log('VEHICLE', f'Switch to Road {road_id}', f"Road {road_id} changed to GREEN")
            update_pedestrian_signals()
    threading.Thread(target=vehicle_sequence, daemon=True).start()
    system_stats['total_requests'] += 1
    system_stats['vehicle_requests'] += 1
    add_log('VEHICLE', f'Switch to Road {road_id}', 'Traffic switch sequence started')
    return jsonify({"success": True, "message": f"Traffic switch to Road {road_id} initiated successfully"})

@app.route('/api/status')
def get_status():
    with lock:
        return jsonify({
            'traffic_state': traffic_state,
            'logs': log_entries[-10:],
            'stats': system_stats
        })

@app.route('/api/logs')
def get_logs():
    return jsonify({
        'logs': log_entries,
        'stats': system_stats
    })

@app.route('/api/clear_logs', methods=['POST'])
def clear_logs():
    global log_entries
    log_entries = []
    add_log('SYSTEM', 'Clear Logs', 'All logs cleared by user')
    return jsonify({"success": True, "message": "Logs cleared successfully"})

# Enhanced Dashboard with Logs (Complete UI)
ENHANCED_DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🚦 Auto Pedestrian Traffic Control Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.0/socket.io.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .header {
            background: rgba(0,0,0,0.3);
            padding: 20px;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        .container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            padding: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }
        .panel {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        .traffic-section {
            margin: 15px 0;
            padding: 15px;
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
        }
        .lights {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin: 10px 0;
        }
        .light {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #333;
            border: 2px solid #666;
            transition: all 0.3s ease;
        }
        .light.red { background: #ff4444; box-shadow: 0 0 20px #ff4444; }
        .light.yellow { 
            background: #ffaa00; 
            box-shadow: 0 0 20px #ffaa00; 
            animation: pulse 1s infinite;
        }
        .light.green { background: #44ff44; box-shadow: 0 0 20px #44ff44; }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }
        .logs-panel {
            max-height: 400px;
            overflow-y: auto;
        }
        .log-entry {
            background: rgba(0,0,0,0.3);
            margin: 5px 0;
            padding: 10px;
            border-radius: 5px;
            border-left: 4px solid #4CAF50;
            font-size: 0.9rem;
        }
        .log-timestamp {
            color: #bbb;
            font-size: 0.8rem;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 10px;
            margin: 15px 0;
        }
        .stat-card {
            background: rgba(0,0,0,0.3);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-number {
            font-size: 1.5rem;
            font-weight: bold;
            color: #00d4aa;
        }
        .clear-btn {
            background: #f44336;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px 0;
        }
        .clear-btn:hover { background: #d32f2f; }
        .auto-note {
            background: rgba(76, 175, 80, 0.2);
            padding: 10px;
            border-radius: 8px;
            margin: 10px 0;
            border-left: 4px solid #4CAF50;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚦 Auto Pedestrian Traffic Control Dashboard</h1>
        <p>Pedestrian signals automatically change based on road availability</p>
        <div class="auto-note">
            <strong>🤖 Auto Mode:</strong> Pedestrians can cross when road is RED (safe), blocked when road is GREEN
        </div>
    </div>

    <div class="container">
        <div class="panel">
            <h2>🚦 Traffic Junction Status</h2>
            
            <div class="traffic-section">
                <h3>Road 1 (North-South)</h3>
                <div class="lights">
                    <div id="road1-red" class="light"></div>
                    <div id="road1-yellow" class="light"></div>
                    <div id="road1-green" class="light"></div>
                </div>
                <div id="road1-status" style="text-align: center; font-weight: bold;"></div>
            </div>

            <div class="traffic-section">
                <h3>Road 2 (East-West)</h3>
                <div class="lights">
                    <div id="road2-red" class="light"></div>
                    <div id="road2-yellow" class="light"></div>
                    <div id="road2-green" class="light"></div>
                </div>
                <div id="road2-status" style="text-align: center; font-weight: bold;"></div>
            </div>

            <div class="traffic-section">
                <h3>🚶 Auto Pedestrian Crossings</h3>
                <div style="display: flex; gap: 30px; justify-content: center;">
                    <div style="text-align: center;">
                        <p>Crossing 1 (Auto)</p>
                        <div id="ped1-light" class="light" style="width: 30px; height: 30px;"></div>
                        <div id="ped1-status"></div>
                    </div>
                    <div style="text-align: center;">
                        <p>Crossing 2 (Auto)</p>
                        <div id="ped2-light" class="light" style="width: 30px; height: 30px;"></div>
                        <div id="ped2-status"></div>
                    </div>
                </div>
            </div>
        </div>

        <div class="panel">
            <h2>📊 System Statistics</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number" id="total-requests">0</div>
                    <div>Total Requests</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="vehicle-requests">0</div>
                    <div>Vehicle Requests</div>
                </div>
            </div>

            <h3>📝 Activity Logs</h3>
            <button class="clear-btn" onclick="clearLogs()">Clear Logs</button>
            <div class="logs-panel" id="logs-container">
                <div class="log-entry">Waiting for activity...</div>
            </div>
        </div>
    </div>

    <script>
        const socket = io();
        
        function updateTrafficLights(state) {
            // Reset all lights
            document.querySelectorAll('.light').forEach(light => {
                light.classList.remove('red', 'yellow', 'green');
            });
            
            // Update Road 1
            const road1State = state.road1.toLowerCase();
            document.getElementById(`road1-${road1State}`).classList.add(road1State);
            document.getElementById('road1-status').textContent = `Status: ${state.road1}`;
            
            // Update Road 2
            const road2State = state.road2.toLowerCase();
            document.getElementById(`road2-${road2State}`).classList.add(road2State);
            document.getElementById('road2-status').textContent = `Status: ${state.road2}`;
            
            // Update Pedestrian 1 (Auto)
            const ped1Light = document.getElementById('ped1-light');
            if (state.pedestrian1 === 'GREEN') {
                ped1Light.classList.add('green');
                document.getElementById('ped1-status').textContent = 'WALK (Auto)';
            } else {
                ped1Light.classList.add('red');
                document.getElementById('ped1-status').textContent = 'STOP (Auto)';
            }
            
            // Update Pedestrian 2 (Auto)
            const ped2Light = document.getElementById('ped2-light');
            if (state.pedestrian2 === 'GREEN') {
                ped2Light.classList.add('green');
                document.getElementById('ped2-status').textContent = 'WALK (Auto)';
            } else {
                ped2Light.classList.add('red');
                document.getElementById('ped2-status').textContent = 'STOP (Auto)';
            }
        }
        
        function updateStats(stats) {
            document.getElementById('total-requests').textContent = stats.total_requests;
            document.getElementById('vehicle-requests').textContent = stats.vehicle_requests;
        }
        
        function updateLogs(logs) {
            const container = document.getElementById('logs-container');
            if (logs.length === 0) {
                container.innerHTML = '<div class="log-entry">No activity yet...</div>';
                return;
            }
            
            container.innerHTML = logs.slice(-10).reverse().map(log => `
                <div class="log-entry">
                    <div class="log-timestamp">${log.timestamp}</div>
                    <div><strong>[${log.type}]</strong> ${log.action}</div>
                    <div>${log.message}</div>
                </div>
            `).join('');
            
            container.scrollTop = 0;
        }
        
        async function clearLogs() {
            try {
                const response = await fetch('/api/clear_logs', { method: 'POST' });
                const result = await response.json();
                if (result.success) {
                    fetchStatus();
                }
            } catch (error) {
                console.error('Error clearing logs:', error);
            }
        }
        
        async function fetchStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                updateTrafficLights(data.traffic_state);
                updateStats(data.stats);
                updateLogs(data.logs);
            } catch (error) {
                console.error('Error fetching status:', error);
            }
        }
        
        // Socket.IO real-time updates
        socket.on('update', function(state) {
            updateTrafficLights(state);
        });
        
        socket.on('log_update', function(data) {
            updateStats(data.stats);
            updateLogs(data.logs);
        });
        
        // Initial load and periodic refresh
        fetchStatus();
        setInterval(fetchStatus, 5000);
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(ENHANCED_DASHBOARD_HTML)

if __name__ == '__main__':
    add_log('SYSTEM', 'Server Start', 'Auto pedestrian traffic server started successfully')
    print("🚦 Auto Pedestrian Traffic Server running at http://localhost:5000")
    socketio.run(app, debug=True, port=5000)
