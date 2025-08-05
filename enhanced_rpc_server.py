# 🚦 traffic_server.py

from flask import Flask, jsonify, request
import threading
import time
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
lock = threading.Lock()

@app.route('/api/control_pedestrian', methods=['POST'])
def control_pedestrian():
    data = request.get_json()
    crossing_id = data.get('crossing_id')
    road_id = crossing_id

    with lock:
        if traffic_state[f'road{road_id}'] == 'GREEN':
            return jsonify({"success": False, "message": f"Cannot cross. Road {road_id} is GREEN."})

    def crossing_sequence():
        with lock:
            traffic_state[f'pedestrian{crossing_id}'] = 'GREEN'
            socketio.emit('update', traffic_state)
        time.sleep(8)
        with lock:
            traffic_state[f'pedestrian{crossing_id}'] = 'RED'
            socketio.emit('update', traffic_state)

    threading.Thread(target=crossing_sequence, daemon=True).start()
    return jsonify({"success": True, "message": f"Pedestrian Crossing {crossing_id} active for 8 seconds."})

@app.route('/api/control_vehicle', methods=['POST'])
def control_vehicle():
    data = request.get_json()
    road_id = data.get('road_id')

    with lock:
        if traffic_state[f'road{road_id}'] == 'GREEN':
            return jsonify({"success": False, "message": f"Road {road_id} is already GREEN."})

    def vehicle_sequence():
        other_road_id = 2 if road_id == 1 else 1
        with lock:
            traffic_state[f'road{other_road_id}'] = 'YELLOW'
            traffic_state[f'road{road_id}'] = 'RED'
            socketio.emit('update', traffic_state)
        time.sleep(3)
        with lock:
            traffic_state[f'road{other_road_id}'] = 'RED'
            socketio.emit('update', traffic_state)
        time.sleep(2)
        with lock:
            traffic_state[f'road{road_id}'] = 'GREEN'
            socketio.emit('update', traffic_state)

    threading.Thread(target=vehicle_sequence, daemon=True).start()
    return jsonify({"success": True, "message": f"Switching to Road {road_id} initiated."})

@app.route('/api/status')
def get_status():
    with lock:
        return jsonify(traffic_state)

if __name__ == '__main__':
    print("🚦 Server running at http://localhost:5000")
    socketio.run(app, debug=True, port=5000)
