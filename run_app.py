"""
VeriMorph - Direct Entry Point Launcher
Run this script to start the web dashboard and automatically open the browser.
Usage:
    python run_app.py
"""

import sys
import os
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

def open_browser():
    time.sleep(1.2)
    url = "http://localhost:8000"
    print(f"[*] Opening browser at {url}...")
    webbrowser.open(url)

if __name__ == "__main__":
    print("\n" + "=" * 65)
    print("  VeriMorph Enterprise AI Platform")
    print("  Zero-Trust Automated Multi-Channel Content Transformation")
    print("  Web Server: http://127.0.0.1:8000 (or http://localhost:8000)")
    print("=" * 65 + "\n")
    
    # Auto-open browser in background thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start Uvicorn ASGI server
    uvicorn.run(app, host="127.0.0.1", port=8000)
