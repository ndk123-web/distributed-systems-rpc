# 🚦 Smart Traffic Control System

A distributed RPC-based traffic junction management system with beautiful web interfaces.

## ✨ Features

### 🖥️ Server Dashboard (Port 5000)
- **Real-time Traffic Visualization**: Live SVG-based junction display
- **Signal Status Monitoring**: Current state of all traffic lights
- **System Statistics**: Request counts, uptime, performance metrics
- **Request Logging**: Complete history of all control requests
- **Emergency Mode**: Instant all-red signal activation

### 🎮 Client Dashboard (Port 5001)
- **Vehicle Traffic Control**: Switch between road directions
- **Pedestrian Crossing**: Request crossing signals
- **Emergency Controls**: Emergency stop functionality
- **Real-time Feedback**: Instant response and status updates
- **Connection Monitoring**: Server connectivity status
- **Performance Metrics**: Response times and success rates

## 🚀 Quick Start

### Method 1: Using Batch File (Recommended for Windows)
```bash
# Double-click the batch file
start_system.bat
```

### Method 2: Using Python Launcher
```bash
# Activate virtual environment
myenv\Scripts\activate

# Run launcher
python launcher.py
```

### Method 3: Manual Start
```bash
# Terminal 1 - Start Server
myenv\Scripts\python.exe enhanced_rpc_server.py

# Terminal 2 - Start Client
myenv\Scripts\python.exe enhanced_rpc_client.py
```

## 🌐 Access URLs

- **Server Dashboard**: http://localhost:5000
- **Client Control Panel**: http://localhost:5001

## 🏗️ System Architecture

```
┌─────────────────┐    HTTP/JSON RPC    ┌─────────────────┐
│   RPC Client    │ ──────────────────► │   RPC Server    │
│   (Port 5001)   │                     │   (Port 5000)   │
│                 │                     │                 │
│ • Control UI    │                     │ • Signal Logic  │
│ • Request Panel │                     │ • State Manager │
│ • Status Monitor│                     │ • Monitor UI    │
└─────────────────┘                     └─────────────────┘
```

## 🎯 API Endpoints

### Vehicle Control
```http
POST /control_vehicle
Content-Type: application/json

{
  "road_id": 1  // 1 for North-South, 2 for East-West
}
```

### Pedestrian Control
```http
POST /control_pedestrian
Content-Type: application/json

{
  "crossing_id": 1  // 1 or 2 for crossing points
}
```

### Emergency Mode
```http
POST /emergency
Content-Type: application/json

{}
```

### Status Query
```http
GET /status
```

## 📊 Response Format

```json
{
  "status": "success|wait|already_green|error",
  "message": "Descriptive message",
  "road_states": {
    "1": "RED|YELLOW|GREEN",
    "2": "RED|YELLOW|GREEN"
  },
  "pedestrian_states": {
    "1": "RED|GREEN",
    "2": "RED|GREEN"
  }
}
```

## 🔧 System Components

### Files Structure
```
distributed-systems-rpc/
├── enhanced_rpc_server.py      # Main RPC server with dashboard
├── enhanced_rpc_client.py      # Client interface with controls
├── rpc_server.py              # Original server (basic)
├── rpc_client.py              # Original client (basic)
├── launcher.py                # Python launcher script
├── start_system.bat           # Windows batch launcher
├── requirements.txt           # Python dependencies
├── README.md                  # This documentation
└── myenv/                     # Python virtual environment
```

### Dependencies
- Flask (Web framework)
- Requests (HTTP client)
- Threading (Concurrent operations)
- JSON (Data serialization)

## 🎨 UI Features

### Modern Design Elements
- **Glassmorphism**: Blur effects and transparency
- **Gradient Backgrounds**: Beautiful color schemes
- **FontAwesome Icons**: Professional iconography
- **Responsive Design**: Mobile-friendly layouts
- **Real-time Updates**: Live data refresh
- **Smooth Animations**: Polished interactions

### Visual Indicators
- **Traffic Lights**: Color-coded signal states
- **Connection Status**: Green/Red connectivity indicator
- **Loading States**: Progress indicators for requests
- **Notifications**: Toast-style success/error messages
- **Statistics Cards**: Key performance metrics

## 🚦 Traffic Logic

### Signal Timing
1. **Yellow Phase**: 3 seconds transition
2. **Red Clearance**: 1 second safety gap
3. **Pedestrian Walk**: 10 seconds crossing time
4. **Pedestrian Flash**: 3 seconds warning

### Safety Rules
- Only one road direction can be GREEN
- Pedestrians cannot cross when vehicles have GREEN
- Emergency mode immediately sets all signals to RED
- Proper yellow-red transition sequence

## 📈 Monitoring & Analytics

### Real-time Metrics
- Total system requests
- Vehicle vs pedestrian request ratio
- System uptime tracking
- Response time monitoring
- Success rate calculations

### Request Logging
- Timestamped request history
- Request type classification
- Operation success tracking
- Error logging and reporting

## 🔐 Security Features

- Input validation on all endpoints
- Thread-safe signal state management
- Error handling and graceful degradation
- Connection timeout management

## 🛠️ Development

### Adding New Features
1. **Server Side**: Add new endpoints in `enhanced_rpc_server.py`
2. **Client Side**: Add controls in `enhanced_rpc_client.py`
3. **UI Updates**: Modify HTML templates and CSS
4. **Testing**: Use both dashboards to verify functionality

### Configuration
- **Server Port**: Change in `app.run()` call
- **Client Port**: Update in client configuration
- **Update Intervals**: Modify JavaScript timers
- **Styling**: Edit CSS in template strings

## 🎓 Learning Objectives

This project demonstrates:
- **RPC Communication**: Client-server request/response
- **Web Technologies**: HTML, CSS, JavaScript, Flask
- **Real-time Systems**: Live updates and monitoring
- **State Management**: Thread-safe operations
- **UI/UX Design**: Modern web interfaces
- **System Integration**: Multiple component coordination

## 🆘 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Kill processes on ports 5000/5001
netstat -ano | findstr :5000
taskkill /PID <process_id> /F
```

**Python Environment Issues**
```bash
# Recreate virtual environment
rmdir /s myenv
python -m venv myenv
myenv\Scripts\activate
pip install -r requirements.txt
```

**Browser Not Opening**
- Manually navigate to http://localhost:5000 and http://localhost:5001
- Check Windows Firewall settings
- Verify Python is not blocked

### Contact & Support
For issues or improvements, please check the system logs in the terminal windows.

---

## 🎉 Enjoy Your Traffic Control System!

**Happy Traffic Managing! 🚦🎮**
