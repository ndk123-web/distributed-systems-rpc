from flask import Flask, render_template_string

app = Flask(__name__)

CLIENT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Traffic Dashboard</title>
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
    <style>
        body { font-family: sans-serif; background: #2c3e50; color: white; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
        .container { background: #34495e; padding: 30px; border-radius: 10px; text-align: center; box-shadow: 0 0 10px rgba(0,0,0,0.5); }
        button { padding: 10px 20px; margin: 10px; border: none; border-radius: 5px; background: #e67e22; color: white; font-weight: bold; cursor: pointer; }
        .status { margin-top: 20px; background: #16a085; padding: 15px; border-radius: 8px; min-width: 300px; }
        .status div { margin: 5px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🚦 Live Traffic Dashboard</h2>
        <button onclick="requestVehicle(1)">Switch to Road 1</button>
        <button onclick="requestVehicle(2)">Switch to Road 2</button>
        <button onclick="requestPedestrian(1)">Pedestrian 1 Cross</button>
        <button onclick="requestPedestrian(2)">Pedestrian 2 Cross</button>
        <div class="status" id="status-box">
            <div id="road1">Road 1: RED</div>
            <div id="road2">Road 2: GREEN</div>
            <div id="ped1">Pedestrian 1: RED</div>
            <div id="ped2">Pedestrian 2: RED</div>
        </div>
    </div>

    <script>
        const socket = io("http://localhost:5000");
        socket.on("connect", () => console.log("Connected to WebSocket"));

        socket.on("update", data => {
            document.getElementById("road1").textContent = `Road 1: ${data.road1}`;
            document.getElementById("road2").textContent = `Road 2: ${data.road2}`;
            document.getElementById("ped1").textContent = `Pedestrian 1: ${data.pedestrian1}`;
            document.getElementById("ped2").textContent = `Pedestrian 2: ${data.pedestrian2}`;
        });

        async function requestPedestrian(id) {
            await fetch("http://localhost:5000/api/control_pedestrian", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ crossing_id: id })
            });
        }

        async function requestVehicle(id) {
            await fetch("http://localhost:5000/api/control_vehicle", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ road_id: id })
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(CLIENT_HTML)

if __name__ == '__main__':
    print("🎮 Client running at http://localhost:5001")
    app.run(debug=True, port=5001)
