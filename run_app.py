"""
VeriMorph - Direct Entry Point Launcher
Run this script to start the web dashboard and automatically open the browser.
Usage:
    python run_app.py
"""

import sys
import os
import socket
import webbrowser
import threading
import time
from pathlib import Path

# Ensure root directory is on sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import uvicorn
from verimorph.web.app import app

def is_port_in_use(port: int) -> bool:
    """Check if a TCP port is currently in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(('127.0.0.1', port)) == 0

def find_available_port(start_port: int = 8000) -> int:
    """Find the first available port starting from start_port."""
    for port in range(start_port, start_port + 20):
        if not is_port_in_use(port):
            return port
    return start_port

def open_browser(port: int):
    time.sleep(1.2)
    url = f"http://127.0.0.1:{port}"
    print(f"[*] Opening default browser at {url}...")
    webbrowser.open(url)

if __name__ == "__main__":
    target_port = find_available_port(8000)
    
    print("\n" + "=" * 65)
    print("  🛡️ VeriMorph Enterprise AI Platform")
    print("  Automated Multi-Channel Transformation & Cryptographic Ledger")
    print(f"  🌐 Web Server URL: http://127.0.0.1:{target_port}")
    print(f"  🌐 Alternate URL:  http://localhost:{target_port}")
    if target_port != 8000:
        print(f"  ℹ️ Port 8000 was busy; automatically allocated port {target_port}.")
    print("=" * 65 + "\n")
    
    # Auto-open browser in background thread
    threading.Thread(target=open_browser, args=(target_port,), daemon=True).start()
    
    # Start Uvicorn ASGI server
    uvicorn.run(app, host="127.0.0.1", port=target_port)
