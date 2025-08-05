# Traffic Control System Launcher
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def print_banner():
    print("=" * 60)
    print("🚦 SMART TRAFFIC CONTROL SYSTEM 🚦")
    print("=" * 60)
    print("Enhanced RPC-based Traffic Junction Controller")
    print("Author: Your Development Team")
    print("=" * 60)

def launch_server():
    """Launch the RPC server"""
    print("🚀 Starting RPC Server...")
    try:
        # Get the python executable path
        python_exe = Path(__file__).parent / "myenv" / "Scripts" / "python.exe"
        server_script = Path(__file__).parent / "enhanced_rpc_server.py"
        
        process = subprocess.Popen([
            str(python_exe), 
            str(server_script)
        ], 
        creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0)
        
        print("✅ Server started successfully!")
        print("📊 Server Dashboard: http://localhost:5000")
        return process
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return None

def launch_client():
    """Launch the RPC client"""
    print("🎮 Starting RPC Client...")
    try:
        # Get the python executable path
        python_exe = Path(__file__).parent / "myenv" / "Scripts" / "python.exe"
        client_script = Path(__file__).parent / "enhanced_rpc_client.py"
        
        process = subprocess.Popen([
            str(python_exe), 
            str(client_script)
        ], 
        creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0)
        
        print("✅ Client started successfully!")
        print("🌐 Client Dashboard: http://localhost:5001")
        return process
    except Exception as e:
        print(f"❌ Failed to start client: {e}")
        return None

def main():
    print_banner()
    
    print("\\n1. Starting components...")
    
    # Launch server first
    server_process = launch_server()
    if not server_process:
        print("❌ Cannot start system without server!")
        return
    
    # Wait a bit for server to initialize
    print("⏳ Waiting for server to initialize...")
    time.sleep(3)
    
    # Launch client
    client_process = launch_client()
    if not client_process:
        print("⚠️  Server running but client failed to start!")
    
    # Wait a bit more
    time.sleep(2)
    
    print("\\n" + "=" * 60)
    print("🎉 SYSTEM LAUNCHED SUCCESSFULLY!")
    print("=" * 60)
    print("📊 Server Dashboard: http://localhost:5000")
    print("🎮 Client Dashboard: http://localhost:5001")
    print("=" * 60)
    
    # Open browsers
    choice = input("\\n🌐 Open dashboards in browser? (y/n): ").strip().lower()
    if choice in ['y', 'yes']:
        try:
            webbrowser.open('http://localhost:5000')
            time.sleep(1)
            webbrowser.open('http://localhost:5001')
            print("✅ Dashboards opened in browser!")
        except:
            print("⚠️  Could not open browser automatically")
    
    print("\\n📝 Instructions:")
    print("1. Use the Server Dashboard to monitor traffic junction")
    print("2. Use the Client Dashboard to send control commands")
    print("3. Both processes are running in separate console windows")
    print("4. Close the console windows to stop the services")
    
    print("\\n🔧 Features:")
    print("✓ Real-time traffic light visualization")
    print("✓ Vehicle traffic control")
    print("✓ Pedestrian crossing requests")
    print("✓ Emergency mode")
    print("✓ Request logging and statistics")
    print("✓ Connection status monitoring")
    
    input("\\n⏸️  Press Enter to exit launcher...")

if __name__ == "__main__":
    main()
