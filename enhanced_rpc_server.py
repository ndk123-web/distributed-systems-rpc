# Enhanced RPC Server with Beautiful UI
from flask import Flask, jsonify, request, render_template_string
import time
import threading
import datetime
import json

app = Flask(__name__)

# Global state for traffic and pedestrian signals
road_states = {1: 'RED', 2: 'GREEN'}
pedestrian_states = {1: 'RED', 2: 'RED'}
signal_lock = threading.Lock()
request_logs = []
system_stats = {
    'total_requests': 0,
    'vehicle_requests': 0,
    'pedestrian_requests': 0,
    'server_start_time': datetime.datetime.now()
}

def log_request(request_type, details):
    """Log all requests for monitoring"""
    global system_stats
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        'timestamp': timestamp,
        'type': request_type,
        'details': details
    }
    request_logs.append(log_entry)
    if len(request_logs) > 50:  # Keep only last 50 logs
        request_logs.pop(0)
    
    system_stats['total_requests'] += 1
    if request_type == 'vehicle':
        system_stats['vehicle_requests'] += 1
    elif request_type == 'pedestrian':
        system_stats['pedestrian_requests'] += 1

# Enhanced Dashboard HTML with better styling and animations
ENHANCED_DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🚦 Smart Traffic Junction Control Center</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            min-height: 100vh;
            overflow-x: auto;
        }
        
        .header {
            background: rgba(0,0,0,0.3);
            padding: 20px;
            text-align: center;
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        
        .container {
            display: grid;
            grid-template-columns: 1fr 350px;
            gap: 20px;
            padding: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .junction-panel {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 30px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            text-align: center;
        }
        
        .control-panel {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            height: fit-content;
        }
        
        .junction-container {
            position: relative;
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
        }
        
        .status-card {
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #00d4aa;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin: 20px 0;
        }
        
        .stat-item {
            background: rgba(0,0,0,0.2);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #00d4aa;
        }
        
        .logs-section {
            max-height: 300px;
            overflow-y: auto;
            background: rgba(0,0,0,0.2);
            border-radius: 8px;
            padding: 15px;
            margin-top: 20px;
        }
        
        .log-entry {
            padding: 8px;
            margin: 5px 0;
            background: rgba(255,255,255,0.1);
            border-radius: 5px;
            font-size: 0.9rem;
        }
        
        .log-timestamp {
            color: #bbb;
            font-size: 0.8rem;
        }
        
        .light {
            transition: all 0.3s ease;
            filter: drop-shadow(0 0 10px currentColor);
        }
        
        .light.active {
            filter: drop-shadow(0 0 20px currentColor) drop-shadow(0 0 40px currentColor);
        }
        
        .pulse {
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .emergency-btn {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            margin: 10px 0;
            width: 100%;
            transition: transform 0.2s;
        }
        
        .emergency-btn:hover {
            transform: scale(1.05);
        }
        
        @media (max-width: 768px) {
            .container {
                grid-template-columns: 1fr;
            }
            .header h1 {
                font-size: 1.8rem;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1><i class="fas fa-traffic-light"></i> Smart Traffic Junction Control Center</h1>
        <p>Real-time monitoring and control system</p>
    </div>
    
    <div class="container">
        <div class="junction-panel">
            <h2 style="margin-bottom: 20px;">Junction Visualization</h2>
            <div class="junction-container">
                <svg width="600" height="600" viewBox="0 0 600 600" style="max-width: 100%; height: auto;">
                    <!-- Roads -->
                    <rect x="250" y="250" width="100" height="100" fill="#2c3e50" stroke="#34495e" stroke-width="2"/>
                    <rect x="0" y="250" width="250" height="100" fill="#34495e" stroke="#2c3e50" stroke-width="1"/>
                    <rect x="350" y="250" width="250" height="100" fill="#34495e" stroke="#2c3e50" stroke-width="1"/>
                    <rect x="250" y="0" width="100" height="250" fill="#34495e" stroke="#2c3e50" stroke-width="1"/>
                    <rect x="250" y="350" width="100" height="250" fill="#34495e" stroke="#2c3e50" stroke-width="1"/>
                    
                    <!-- Lane markings -->
                    <rect x="150" y="250" width="20" height="100" fill="white" opacity="0.8"/>
                    <rect x="430" y="250" width="20" height="100" fill="white" opacity="0.8"/>
                    <rect x="250" y="150" width="100" height="20" fill="white" opacity="0.8"/>
                    <rect x="250" y="430" width="100" height="20" fill="white" opacity="0.8"/>
                    
                    <!-- Traffic Lights -->
                    <g id="road1-lights" transform="translate(250, 380)">
                        <rect x="0" y="0" width="100" height="30" fill="#1a1a1a" rx="15"/>
                        <circle cx="20" cy="15" r="8" fill="#660000" class="light" id="road1-red"></circle>
                        <circle cx="50" cy="15" r="8" fill="#666600" class="light" id="road1-yellow"></circle>
                        <circle cx="80" cy="15" r="8" fill="#006600" class="light" id="road1-green"></circle>
                    </g>
                    
                    <g id="road2-lights" transform="translate(250, 190)">
                        <rect x="0" y="0" width="100" height="30" fill="#1a1a1a" rx="15"/>
                        <circle cx="20" cy="15" r="8" fill="#660000" class="light" id="road2-red"></circle>
                        <circle cx="50" cy="15" r="8" fill="#666600" class="light" id="road2-yellow"></circle>
                        <circle cx="80" cy="15" r="8" fill="#006600" class="light" id="road2-green"></circle>
                    </g>
                    
                    <!-- Pedestrian Crossings -->
                    <g id="ped1-lights" transform="translate(80, 280)">
                        <rect x="0" y="0" width="30" height="50" fill="#1a1a1a" rx="10"/>
                        <rect x="5" y="5" width="20" height="20" fill="#660000" class="ped-light" id="ped1-red"></rect>
                        <rect x="5" y="25" width="20" height="20" fill="#006600" class="ped-light" id="ped1-green"></rect>
                    </g>
                    
                    <g id="ped2-lights" transform="translate(490, 280)">
                        <rect x="0" y="0" width="30" height="50" fill="#1a1a1a" rx="10"/>
                        <rect x="5" y="5" width="20" height="20" fill="#660000" class="ped-light" id="ped2-red"></rect>
                        <rect x="5" y="25" width="20" height="20" fill="#006600" class="ped-light" id="ped2-green"></rect>
                    </g>
                    
                    <!-- Labels -->
                    <text x="300" y="40" text-anchor="middle" fill="white" font-size="16" font-weight="bold">Road 1 (North-South)</text>
                    <text x="300" y="580" text-anchor="middle" fill="white" font-size="16" font-weight="bold">Road 1 (South-North)</text>
                    <text x="50" y="305" text-anchor="middle" fill="white" font-size="16" font-weight="bold" transform="rotate(-90, 50, 305)">Road 2 (West-East)</text>
                    <text x="550" y="305" text-anchor="middle" fill="white" font-size="16" font-weight="bold" transform="rotate(90, 550, 305)">Road 2 (East-West)</text>
                </svg>
            </div>
            
            <div class="status-card" id="current-status">
                <h3><i class="fas fa-info-circle"></i> Current Status</h3>
                <p id="status-text">Loading...</p>
            </div>
        </div>
        
        <div class="control-panel">
            <h3><i class="fas fa-chart-bar"></i> System Statistics</h3>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number" id="total-requests">0</div>
                    <div>Total Requests</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="vehicle-requests">0</div>
                    <div>Vehicle Requests</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="pedestrian-requests">0</div>
                    <div>Pedestrian Requests</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="uptime">0s</div>
                    <div>Uptime</div>
                </div>
            </div>
            
            <button class="emergency-btn" onclick="emergencyMode()">
                <i class="fas fa-exclamation-triangle"></i> Emergency Mode
            </button>
            
            <h4><i class="fas fa-history"></i> Request Logs</h4>
            <div class="logs-section" id="logs-container">
                <div class="log-entry">No requests yet...</div>
            </div>
        </div>
    </div>

    <script>
        let isEmergencyMode = false;
        
        function updateLights(states) {
            // Reset all lights
            document.querySelectorAll('.light').forEach(el => {
                el.setAttribute('fill', el.id.includes('red') ? '#660000' : el.id.includes('yellow') ? '#666600' : '#006600');
                el.classList.remove('active', 'pulse');
            });
            
            document.querySelectorAll('.ped-light').forEach(el => {
                el.setAttribute('fill', el.id.includes('red') ? '#660000' : '#006600');
                el.classList.remove('active', 'pulse');
            });
            
            // Update Road 1
            const road1Color = states.road_states[1].toLowerCase();
            const road1Light = document.getElementById(`road1-${road1Color}`);
            if (road1Light) {
                road1Light.setAttribute('fill', road1Color === 'red' ? '#ff0000' : road1Color === 'yellow' ? '#ffff00' : '#00ff00');
                road1Light.classList.add('active');
            }
            
            // Update Road 2
            const road2Color = states.road_states[2].toLowerCase();
            const road2Light = document.getElementById(`road2-${road2Color}`);
            if (road2Light) {
                road2Light.setAttribute('fill', road2Color === 'red' ? '#ff0000' : road2Color === 'yellow' ? '#ffff00' : '#00ff00');
                road2Light.classList.add('active');
            }
            
            // Update Pedestrian 1
            if (states.pedestrian_states[1] === 'GREEN') {
                document.getElementById('ped1-green').setAttribute('fill', '#00ff00');
                document.getElementById('ped1-green').classList.add('active');
            } else {
                document.getElementById('ped1-red').setAttribute('fill', '#ff0000');
                document.getElementById('ped1-red').classList.add('active');
            }
            
            // Update Pedestrian 2
            if (states.pedestrian_states[2] === 'GREEN') {
                document.getElementById('ped2-green').setAttribute('fill', '#00ff00');
                document.getElementById('ped2-green').classList.add('active');
            } else {
                document.getElementById('ped2-red').setAttribute('fill', '#ff0000');
                document.getElementById('ped2-red').classList.add('active');
            }
        }
        
        function updateStats(stats) {
            document.getElementById('total-requests').textContent = stats.total_requests;
            document.getElementById('vehicle-requests').textContent = stats.vehicle_requests;
            document.getElementById('pedestrian-requests').textContent = stats.pedestrian_requests;
            
            const startTime = new Date(stats.server_start_time);
            const now = new Date();
            const uptimeSeconds = Math.floor((now - startTime) / 1000);
            document.getElementById('uptime').textContent = formatUptime(uptimeSeconds);
        }
        
        function updateLogs(logs) {
            const container = document.getElementById('logs-container');
            if (logs.length === 0) {
                container.innerHTML = '<div class="log-entry">No requests yet...</div>';
                return;
            }
            
            container.innerHTML = logs.slice(-10).reverse().map(log => `
                <div class="log-entry">
                    <div class="log-timestamp">${log.timestamp}</div>
                    <div><strong>${log.type.toUpperCase()}</strong>: ${log.details}</div>
                </div>
            `).join('');
        }
        
        function formatUptime(seconds) {
            const hours = Math.floor(seconds / 3600);
            const minutes = Math.floor((seconds % 3600) / 60);
            const secs = seconds % 60;
            return `${hours}h ${minutes}m ${secs}s`;
        }
        
        async function fetchStatus() {
            try {
                const response = await fetch('/status');
                const data = await response.json();
                updateLights(data);
                updateStats(data.stats);
                updateLogs(data.logs);
                document.getElementById('status-text').textContent = data.message;
            } catch (error) {
                document.getElementById('status-text').textContent = 'Server connection lost!';
                console.error(error);
            }
        }
        
        async function emergencyMode() {
            if (isEmergencyMode) return;
            
            isEmergencyMode = true;
            try {
                const response = await fetch('/emergency', { method: 'POST' });
                const result = await response.json();
                alert(result.message);
            } catch (error) {
                alert('Emergency mode failed: ' + error.message);
            }
            
            setTimeout(() => { isEmergencyMode = false; }, 5000);
        }
        
        // Update every 500ms
        setInterval(fetchStatus, 500);
        fetchStatus();
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(ENHANCED_DASHBOARD_HTML)

@app.route('/status')
def get_status():
    with signal_lock:
        return jsonify({
            'road_states': road_states,
            'pedestrian_states': pedestrian_states,
            'message': f"Road 1: {road_states[1]}, Road 2: {road_states[2]} | Ped 1: {pedestrian_states[1]}, Ped 2: {pedestrian_states[2]}",
            'stats': system_stats,
            'logs': request_logs
        })

@app.route('/control_vehicle', methods=['POST'])
def control_vehicle():
    data = request.get_json()
    target_road_id = int(data.get('road_id'))
    
    log_request('vehicle', f"Request to switch to Road {target_road_id}")
    
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
        
        log_request('vehicle', f"Successfully switched to Road {target_road_id}")
        return jsonify({"status": "success", "message": f"Signal changed. Road {target_road_id} is now GREEN."})

@app.route('/control_pedestrian', methods=['POST'])
def control_pedestrian():
    data = request.get_json()
    crossing_id = int(data.get('crossing_id'))
    
    log_request('pedestrian', f"Request for pedestrian crossing {crossing_id}")
    
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
        
        log_request('pedestrian', f"Completed pedestrian crossing {crossing_id}")
        return jsonify({"status": "success", "message": f"Pedestrian crossing {crossing_id} sequence completed."})

@app.route('/emergency', methods=['POST'])
def emergency_mode():
    """Emergency mode - all signals turn red"""
    log_request('emergency', "Emergency mode activated")
    
    with signal_lock:
        road_states[1] = 'RED'
        road_states[2] = 'RED'
        pedestrian_states[1] = 'RED'
        pedestrian_states[2] = 'RED'
        
        return jsonify({"status": "success", "message": "Emergency mode activated! All signals are RED."})

if __name__ == '__main__':
    print("🚦 Enhanced Traffic Signal Controller Server starting on port 5000...")
    print("📊 Dashboard available at: http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)
