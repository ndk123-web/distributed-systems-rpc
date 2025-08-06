from flask import Flask, render_template_string

app = Flask(__name__)

# Auto Pedestrian Client HTML with Complete UI
CLIENT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🎮 Auto Pedestrian Traffic Control Client</title>
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
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
            max-width: 1200px;
            margin: 0 auto;
        }
        .panel {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        .control-section {
            margin: 20px 0;
        }
        .control-btn {
            width: 100%;
            padding: 15px;
            margin: 8px 0;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .vehicle-btn {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
        }
        .vehicle-btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4); }
        .status-display {
            background: rgba(0,0,0,0.3);
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
        }
        .status-item {
            display: flex;
            justify-content: space-between;
            margin: 8px 0;
            padding: 8px;
            background: rgba(255,255,255,0.1);
            border-radius: 5px;
        }
        .connection-status {
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            margin: 10px 0;
            font-weight: bold;
        }
        .connected { background: rgba(76, 175, 80, 0.3); }
        .disconnected { background: rgba(244, 67, 54, 0.3); }
        .logs-panel {
            max-height: 300px;
            overflow-y: auto;
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            padding: 15px;
        }
        .log-entry {
            background: rgba(255,255,255,0.1);
            margin: 5px 0;
            padding: 10px;
            border-radius: 5px;
            border-left: 4px solid;
            font-size: 0.9rem;
        }
        .log-entry.success { border-left-color: #4CAF50; }
        .log-entry.error { border-left-color: #F44336; }
        .log-entry.info { border-left-color: #2196F3; }
        .log-timestamp {
            color: #bbb;
            font-size: 0.8rem;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
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
            font-size: 1.2rem;
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
        .random-section {
            background: rgba(255, 193, 7, 0.2);
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            border-left: 4px solid #FFC107;
        }
        .random-btn {
            background: linear-gradient(45deg, #FF9800, #F57C00);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            cursor: pointer;
            margin: 5px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .random-btn:hover { 
            transform: translateY(-2px); 
            box-shadow: 0 5px 15px rgba(255, 152, 0, 0.4); 
        }
        .random-display {
            background: rgba(0,0,0,0.3);
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            font-family: monospace;
            font-size: 1.1rem;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎮 Auto Pedestrian Traffic Control Client</h1>
        <p>Control vehicle traffic - pedestrian signals update automatically</p>
        <div class="auto-note">
            <strong>🤖 Auto Mode:</strong> No pedestrian buttons needed - signals change automatically!
        </div>
        <div id="connection-status" class="connection-status disconnected">
            🔴 Connecting to server...
        </div>
    </div>

    <div class="container">
        <div class="panel">
            <h2>🎮 Vehicle Control Panel</h2>
            
            <div class="control-section">
                <h3>🚗 Vehicle Traffic Control</h3>
                <button class="control-btn vehicle-btn" onclick="requestVehicle(1)">
                    🚗 Switch to Road 1 (North-South)
                </button>
                <button class="control-btn vehicle-btn" onclick="requestVehicle(2)">
                    🚗 Switch to Road 2 (East-West)
                </button>
            </div>

            <div class="random-section">
                <h3>🎲 Random Traffic Generator</h3>
                <p><strong>Number Mapping:</strong></p>
                <ul style="margin: 10px 0; padding-left: 20px;">
                    <li>1, 2 → Road 1 (North-South)</li>
                    <li>3, 4 → Road 2 (East-West)</li>
                </ul>
                <div class="random-display" id="random-display">
                    Random Number: <span id="current-random">--</span> → Road: <span id="mapped-road">--</span>
                </div>
                <button class="random-btn" onclick="generateRandomRequest()">
                    🎲 Generate Random Request
                </button>
                <button class="random-btn" onclick="startAutoRandom()" id="auto-btn">
                    🔄 Start Auto Random (5s)
                </button>
                <button class="random-btn" onclick="stopAutoRandom()" id="stop-btn" style="display:none; background: #f44336;">
                    ⏹️ Stop Auto Random
                </button>
            </div>

            <div class="status-display">
                <h3>📊 Current Status</h3>
                <div class="status-item">
                    <span>Road 1 (N-S):</span>
                    <span id="road1-status">RED</span>
                </div>
                <div class="status-item">
                    <span>Road 2 (E-W):</span>
                    <span id="road2-status">GREEN</span>
                </div>
                <div class="status-item">
                    <span>Pedestrian 1 (Auto):</span>
                    <span id="ped1-status">GREEN</span>
                </div>
                <div class="status-item">
                    <span>Pedestrian 2 (Auto):</span>
                    <span id="ped2-status">RED</span>
                </div>
            </div>
        </div>

        <div class="panel">
            <h2>📊 Client Statistics</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number" id="requests-sent">0</div>
                    <div>Requests Sent</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="success-rate">100%</div>
                    <div>Success Rate</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="last-response">--</div>
                    <div>Last Response (ms)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="connection-time">--</div>
                    <div>Connected Since</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="random-requests">0</div>
                    <div>Random Requests</div>
                </div>
            </div>

            <h3>📝 Client Activity Logs</h3>
            <button class="clear-btn" onclick="clearClientLogs()">Clear Client Logs</button>
            <div class="logs-panel" id="client-logs">
                <div class="log-entry info">
                    <div class="log-timestamp">Waiting for activity...</div>
                    <div>Client ready to send commands</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const socket = io("http://localhost:5000");
        let clientLogs = [];
        let clientStats = {
            requestsSent: 0,
            successfulRequests: 0,
            connectionTime: null,
            randomRequests: 0
        };

        let autoRandomInterval = null;

        // Random number generation and mapping
        function generateRandomNumber() {
            return Math.floor(Math.random() * 4) + 1; // Generates 1, 2, 3, or 4
        }

        function mapNumberToRoad(randomNum) {
            if (randomNum === 1 || randomNum === 2) {
                return 1; // North-South
            } else if (randomNum === 3 || randomNum === 4) {
                return 2; // East-West
            }
        }

        function generateRandomRequest() {
            const randomNum = generateRandomNumber();
            const roadId = mapNumberToRoad(randomNum);
            
            document.getElementById('current-random').textContent = randomNum;
            document.getElementById('mapped-road').textContent = `Road ${roadId} (${roadId === 1 ? 'North-South' : 'East-West'})`;
            
            clientStats.randomRequests++;
            updateClientStats();
            
            addClientLog('info', `Random number generated: ${randomNum}`, `Mapped to Road ${roadId}, sending request...`);
            
            // Send the request
            requestVehicle(roadId, true, randomNum);
        }

        function startAutoRandom() {
            if (autoRandomInterval) return; // Already running
            
            document.getElementById('auto-btn').style.display = 'none';
            document.getElementById('stop-btn').style.display = 'inline-block';
            
            addClientLog('info', 'Auto random mode started', 'Generating random requests every 5 seconds');
            
            autoRandomInterval = setInterval(() => {
                generateRandomRequest();
            }, 5000);
        }

        function stopAutoRandom() {
            if (autoRandomInterval) {
                clearInterval(autoRandomInterval);
                autoRandomInterval = null;
            }
            
            document.getElementById('auto-btn').style.display = 'inline-block';
            document.getElementById('stop-btn').style.display = 'none';
            
            addClientLog('info', 'Auto random mode stopped', 'Manual control resumed');
        }

        function addClientLog(type, message, details = '') {
            const timestamp = new Date().toLocaleString();
            const logEntry = {
                timestamp,
                type,
                message,
                details,
                success: type !== 'error'
            };
            
            clientLogs.push(logEntry);
            if (clientLogs.length > 50) {
                clientLogs.shift();
            }
            
            updateClientLogs();
        }

        function updateClientLogs() {
            const container = document.getElementById('client-logs');
            if (clientLogs.length === 0) {
                container.innerHTML = '<div class="log-entry info"><div class="log-timestamp">No activity yet...</div><div>Client ready to send commands</div></div>';
                return;
            }
            
            container.innerHTML = clientLogs.slice(-10).reverse().map(log => `
                <div class="log-entry ${log.success ? 'success' : 'error'}">
                    <div class="log-timestamp">${log.timestamp}</div>
                    <div><strong>${log.type.toUpperCase()}</strong>: ${log.message}</div>
                    ${log.details ? `<div style="font-size: 0.8rem; opacity: 0.8;">${log.details}</div>` : ''}
                </div>
            `).join('');
        }

        function updateClientStats() {
            document.getElementById('requests-sent').textContent = clientStats.requestsSent;
            document.getElementById('success-rate').textContent = 
                clientStats.requestsSent > 0 ? 
                Math.round((clientStats.successfulRequests / clientStats.requestsSent) * 100) + '%' : '100%';
            
            if (clientStats.connectionTime) {
                document.getElementById('connection-time').textContent = clientStats.connectionTime;
            }
            
            document.getElementById('random-requests').textContent = clientStats.randomRequests;
        }

        function clearClientLogs() {
            clientLogs = [];
            addClientLog('info', 'Client logs cleared by user');
        }

        // Socket.IO event handlers
        socket.on("connect", () => {
            console.log("Connected to WebSocket");
            clientStats.connectionTime = new Date().toLocaleTimeString();
            document.getElementById('connection-status').className = 'connection-status connected';
            document.getElementById('connection-status').innerHTML = '🟢 Connected to server';
            addClientLog('info', 'Connected to server successfully', 'WebSocket connection established');
            updateClientStats();
        });

        socket.on("disconnect", () => {
            document.getElementById('connection-status').className = 'connection-status disconnected';
            document.getElementById('connection-status').innerHTML = '🔴 Disconnected from server';
            addClientLog('error', 'Disconnected from server', 'WebSocket connection lost');
        });

        socket.on("update", data => {
            document.getElementById("road1-status").textContent = data.road1;
            document.getElementById("road2-status").textContent = data.road2;
            document.getElementById("ped1-status").textContent = data.pedestrian1 + ' (Auto)';
            document.getElementById("ped2-status").textContent = data.pedestrian2 + ' (Auto)';
            
            addClientLog('info', 'Traffic state updated', 
                `Road1: ${data.road1}, Road2: ${data.road2}, Ped1: ${data.pedestrian1}, Ped2: ${data.pedestrian2} (Auto)`);
        });

        async function requestVehicle(roadId, isRandom = false, randomNum = null) {
            const startTime = Date.now();
            clientStats.requestsSent++;
            
            const logPrefix = isRandom ? `Random request (${randomNum} → Road ${roadId})` : `Manual vehicle request`;
            addClientLog('info', `${logPrefix} sent`, `Requesting switch to Road ${roadId}`);
            
            try {
                const response = await fetch("http://localhost:5000/api/control_vehicle", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ road_id: roadId })
                });
                
                const result = await response.json();
                const responseTime = Date.now() - startTime;
                document.getElementById('last-response').textContent = responseTime + 'ms';
                
                if (result.success) {
                    clientStats.successfulRequests++;
                    const successMsg = isRandom ? 
                        `Random request successful (${randomNum} → Road ${roadId})` : 
                        `Manual vehicle request successful`;
                    addClientLog('success', successMsg, 
                        `${result.message} (${responseTime}ms) - Pedestrians will auto-update`);
                } else {
                    const errorMsg = isRandom ? 
                        `Random request failed (${randomNum} → Road ${roadId})` : 
                        `Manual vehicle request failed`;
                    addClientLog('error', errorMsg, 
                        `${result.message} (${responseTime}ms)`);
                }
            } catch (error) {
                const responseTime = Date.now() - startTime;
                const errorMsg = isRandom ? 
                    `Random request error (${randomNum} → Road ${roadId})` : 
                    `Manual vehicle request error`;
                addClientLog('error', errorMsg, 
                    `${error.message} (${responseTime}ms)`);
            }
            
            updateClientStats();
        }

        // Initialize
        addClientLog('info', 'Auto pedestrian client started', 'Pedestrian signals will update automatically based on road state');
        addClientLog('info', 'Random generator ready', 'Numbers 1,2 → Road 1 (N-S), Numbers 3,4 → Road 2 (E-W)');
        updateClientStats();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(CLIENT_HTML)

if __name__ == '__main__':
    print("🎮 Auto Pedestrian Client running at http://localhost:5001")
    app.run(debug=True, port=5001, host='0.0.0.0')
