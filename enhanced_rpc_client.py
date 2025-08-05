# Enhanced RPC Client with Beautiful Interactive UI
from flask import Flask, render_template_string
import requests
import json

app = Flask(__name__)

# Enhanced Client UI with modern design and real-time features
ENHANCED_CLIENT_UI_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🎮 Traffic Control Client Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white; 
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        .header {
            background: rgba(0,0,0,0.3);
            padding: 20px;
            text-align: center;
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255,255,255,0.2);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        
        .connection-status {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9rem;
            margin-top: 10px;
        }
        
        .connected {
            background: rgba(76, 175, 80, 0.3);
            border: 1px solid #4caf50;
        }
        
        .disconnected {
            background: rgba(244, 67, 54, 0.3);
            border: 1px solid #f44336;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 30px 20px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }
        
        .control-section {
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 30px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        
        .section-title {
            font-size: 1.5rem;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .button-grid {
            display: grid;
            gap: 15px;
        }
        
        .control-btn {
            padding: 20px;
            font-size: 1.1rem;
            font-weight: bold;
            border-radius: 15px;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .vehicle-btn {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
        }
        
        .vehicle-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(76, 175, 80, 0.6);
        }
        
        .pedestrian-btn {
            background: linear-gradient(45deg, #FF9800, #F57C00);
            color: white;
            box-shadow: 0 4px 15px rgba(255, 152, 0, 0.4);
        }
        
        .pedestrian-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(255, 152, 0, 0.6);
        }
        
        .emergency-btn {
            background: linear-gradient(45deg, #F44336, #D32F2F);
            color: white;
            box-shadow: 0 4px 15px rgba(244, 67, 54, 0.4);
        }
        
        .emergency-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(244, 67, 54, 0.6);
        }
        
        .control-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none !important;
        }
        
        .loading {
            position: relative;
        }
        
        .loading::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 20px;
            height: 20px;
            margin: -10px 0 0 -10px;
            border: 2px solid transparent;
            border-top: 2px solid white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .response-panel {
            background: rgba(0,0,0,0.3);
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
            border-left: 4px solid #00d4aa;
        }
        
        .response-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
            font-weight: bold;
        }
        
        .response-content {
            background: rgba(0,0,0,0.2);
            padding: 15px;
            border-radius: 8px;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            min-height: 100px;
            max-height: 200px;
            overflow-y: auto;
        }
        
        .server-status {
            margin-top: 20px;
        }
        
        .status-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 15px;
        }
        
        .status-item {
            background: rgba(0,0,0,0.2);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
        
        .status-value {
            font-size: 1.5rem;
            font-weight: bold;
            color: #00d4aa;
        }
        
        .quick-actions {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }
        
        .quick-btn {
            flex: 1;
            padding: 10px;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.3);
            color: white;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .quick-btn:hover {
            background: rgba(255,255,255,0.2);
        }
        
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: bold;
            z-index: 1000;
            transform: translateX(400px);
            transition: transform 0.3s ease;
        }
        
        .notification.show {
            transform: translateX(0);
        }
        
        .notification.success {
            background: linear-gradient(45deg, #4CAF50, #45a049);
        }
        
        .notification.error {
            background: linear-gradient(45deg, #F44336, #D32F2F);
        }
        
        .notification.warning {
            background: linear-gradient(45deg, #FF9800, #F57C00);
        }
        
        @media (max-width: 768px) {
            .container {
                grid-template-columns: 1fr;
                padding: 20px 10px;
            }
            .header h1 {
                font-size: 1.8rem;
            }
            .status-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1><i class="fas fa-gamepad"></i> Traffic Control Client Dashboard</h1>
        <p>Remote control interface for traffic junction management</p>
        <div id="connection-status" class="connection-status disconnected">
            <i class="fas fa-circle"></i>
            <span>Checking connection...</span>
        </div>
    </div>
    
    <div class="container">
        <div class="control-section">
            <h2 class="section-title">
                <i class="fas fa-car"></i>
                Vehicle Traffic Control
            </h2>
            <div class="button-grid">
                <button class="control-btn vehicle-btn" onclick="sendRequest('/control_vehicle', {road_id: 1})">
                    <i class="fas fa-arrow-up"></i>
                    Switch to Road 1 (North-South)
                </button>
                <button class="control-btn vehicle-btn" onclick="sendRequest('/control_vehicle', {road_id: 2})">
                    <i class="fas fa-arrow-right"></i>
                    Switch to Road 2 (East-West)
                </button>
            </div>
            
            <h2 class="section-title" style="margin-top: 30px;">
                <i class="fas fa-walking"></i>
                Pedestrian Crossing Control
            </h2>
            <div class="button-grid">
                <button class="control-btn pedestrian-btn" onclick="sendRequest('/control_pedestrian', {crossing_id: 1})">
                    <i class="fas fa-street-view"></i>
                    Request Crossing 1
                </button>
                <button class="control-btn pedestrian-btn" onclick="sendRequest('/control_pedestrian', {crossing_id: 2})">
                    <i class="fas fa-street-view"></i>
                    Request Crossing 2
                </button>
            </div>
            
            <h2 class="section-title" style="margin-top: 30px;">
                <i class="fas fa-exclamation-triangle"></i>
                Emergency Controls
            </h2>
            <div class="button-grid">
                <button class="control-btn emergency-btn" onclick="sendRequest('/emergency', {})">
                    <i class="fas fa-ban"></i>
                    Emergency Stop (All Red)
                </button>
            </div>
            
            <div class="quick-actions">
                <button class="quick-btn" onclick="checkServerStatus()">
                    <i class="fas fa-sync"></i> Refresh Status
                </button>
                <button class="quick-btn" onclick="clearLogs()">
                    <i class="fas fa-trash"></i> Clear Logs
                </button>
            </div>
        </div>
        
        <div class="control-section">
            <h2 class="section-title">
                <i class="fas fa-terminal"></i>
                Response & Monitoring
            </h2>
            
            <div class="response-panel">
                <div class="response-header">
                    <i class="fas fa-comment-dots"></i>
                    <span>Server Response</span>
                </div>
                <div class="response-content" id="response-text">
                    Waiting for your command...
                    
Click any control button to send an RPC request to the server.
                </div>
            </div>
            
            <div class="server-status">
                <h3><i class="fas fa-server"></i> Server Status</h3>
                <div class="status-grid">
                    <div class="status-item">
                        <div class="status-value" id="response-time">--</div>
                        <div>Response Time</div>
                    </div>
                    <div class="status-item">
                        <div class="status-value" id="request-count">0</div>
                        <div>Requests Sent</div>
                    </div>
                    <div class="status-item">
                        <div class="status-value" id="success-rate">100%</div>
                        <div>Success Rate</div>
                    </div>
                    <div class="status-item">
                        <div class="status-value" id="last-request">Never</div>
                        <div>Last Request</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div id="notification" class="notification"></div>

    <script>
        let requestCount = 0;
        let successCount = 0;
        let isConnected = false;
        
        const SERVER_URL = 'http://localhost:5000';
        
        function showNotification(message, type = 'success') {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.className = `notification ${type}`;
            notification.classList.add('show');
            
            setTimeout(() => {
                notification.classList.remove('show');
            }, 3000);
        }
        
        function updateConnectionStatus(connected) {
            const statusEl = document.getElementById('connection-status');
            const icon = statusEl.querySelector('i');
            const text = statusEl.querySelector('span');
            
            isConnected = connected;
            
            if (connected) {
                statusEl.className = 'connection-status connected';
                icon.className = 'fas fa-circle';
                text.textContent = 'Connected to Server';
            } else {
                statusEl.className = 'connection-status disconnected';
                icon.className = 'fas fa-circle';
                text.textContent = 'Server Disconnected';
            }
        }
        
        function updateStats(responseTime) {
            document.getElementById('response-time').textContent = responseTime + 'ms';
            document.getElementById('request-count').textContent = requestCount;
            document.getElementById('success-rate').textContent = 
                requestCount > 0 ? Math.round((successCount / requestCount) * 100) + '%' : '100%';
            document.getElementById('last-request').textContent = new Date().toLocaleTimeString();
        }
        
        async function sendRequest(endpoint, data) {
            const startTime = Date.now();
            const responseTextEl = document.getElementById('response-text');
            const buttons = document.querySelectorAll('.control-btn');
            
            // Disable buttons and show loading
            buttons.forEach(btn => {
                btn.disabled = true;
                if (btn.onclick.toString().includes(endpoint)) {
                    btn.classList.add('loading');
                }
            });
            
            responseTextEl.textContent = 'Sending request to server...\\nPlease wait...';
            requestCount++;
            
            try {
                const response = await fetch(`${SERVER_URL}${endpoint}`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                const responseTime = Date.now() - startTime;
                
                successCount++;
                updateConnectionStatus(true);
                updateStats(responseTime);
                
                let message = `✅ SUCCESS\\n`;
                message += `Status: ${result.status}\\n`;
                message += `Message: ${result.message}\\n`;
                message += `Response Time: ${responseTime}ms\\n`;
                message += `Timestamp: ${new Date().toLocaleString()}`;
                
                responseTextEl.textContent = message;
                
                showNotification(`Request successful: ${result.message}`, 'success');
                
            } catch (error) {
                const responseTime = Date.now() - startTime;
                updateConnectionStatus(false);
                updateStats(responseTime);
                
                let errorMessage = `❌ ERROR\\n`;
                errorMessage += `Could not connect to the server.\\n`;
                errorMessage += `Error: ${error.message}\\n`;
                errorMessage += `Response Time: ${responseTime}ms\\n`;
                errorMessage += `Timestamp: ${new Date().toLocaleString()}\\n\\n`;
                errorMessage += `Make sure the server is running on port 5000!`;
                
                responseTextEl.textContent = errorMessage;
                
                showNotification('Server connection failed!', 'error');
            }
            
            // Re-enable buttons and remove loading
            buttons.forEach(btn => {
                btn.disabled = false;
                btn.classList.remove('loading');
            });
        }
        
        async function checkServerStatus() {
            try {
                const response = await fetch(`${SERVER_URL}/status`);
                const data = await response.json();
                updateConnectionStatus(true);
                showNotification('Server is online and responsive', 'success');
                
                const statusInfo = `🟢 SERVER STATUS\\n`;
                const info = statusInfo + `Road 1: ${data.road_states[1]}\\n`;
                const info2 = info + `Road 2: ${data.road_states[2]}\\n`;
                const info3 = info2 + `Pedestrian 1: ${data.pedestrian_states[1]}\\n`;
                const finalInfo = info3 + `Pedestrian 2: ${data.pedestrian_states[2]}\\n`;
                
                document.getElementById('response-text').textContent = finalInfo;
            } catch (error) {
                updateConnectionStatus(false);
                showNotification('Server status check failed', 'error');
            }
        }
        
        function clearLogs() {
            document.getElementById('response-text').textContent = 'Logs cleared.\\n\\nWaiting for your next command...';
            showNotification('Response logs cleared', 'warning');
        }
        
        // Check server status on page load and every 5 seconds
        checkServerStatus();
        setInterval(checkServerStatus, 5000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(ENHANCED_CLIENT_UI_HTML)

if __name__ == '__main__':
    print("🎮 Enhanced Traffic Signal Client starting on port 5001...")
    print("🌐 Client Dashboard available at: http://localhost:5001")
    print("📡 Make sure the server is running on port 5000 for RPC communication!")
    app.run(debug=True, host="0.0.0.0", port=5001)
