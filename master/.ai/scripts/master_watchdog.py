#!/usr/bin/env python3
import time
import subprocess
import os
from pathlib import Path
import requests
import sys

# Paths
ROOT = Path(__file__).resolve().parents[3]
SYNC_SCRIPT = ROOT / "master" / ".ai" / "scripts" / "sync-aggregated-state.py"
MAINTENANCE_SCRIPT = ROOT / "master" / ".ai" / "scripts" / "autonomous_maintenance_bot.py"
DASHBOARD_API = "http://localhost:8000/api/update-state"

# Configuration
INTERVAL_SECONDS = 1800 # 30 mins

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] 🐕 WATCHDOG: {msg}")

def run_step(script_path):
    if not script_path.exists():
        log(f"Error: {script_path.name} not found.")
        return False
    
    log(f"Running {script_path.name}...")
    try:
        subprocess.run([sys.executable, str(script_path)], check=True, cwd=ROOT)
        return True
    except subprocess.CalledProcessError as e:
        log(f"Error executing {script_path.name}: {e}")
        return False

def broadcast_to_dashboard():
    log("Broadcasting state to Dashboard...")
    try:
        response = requests.post(DASHBOARD_API)
        if response.status_code == 200:
            log("Dashboard sync complete.")
        else:
            log(f"Dashboard API error: {response.status_code}")
    except Exception as e:
        log(f"Could not connect to Dashboard API: {e}")

def main_loop():
    log("Master Watchdog v14.0.0 INITIALIZED.")
    log(f"Cycle frequency: every {INTERVAL_SECONDS} seconds.")
    
    while True:
        log("--- Starting Sovereign Sync Cycle ---")
        
        # 1. Economic Sync
        run_step(SYNC_SCRIPT)
        
        # 2. Structural Maintenance
        run_step(MAINTENANCE_SCRIPT)
        
        # 3. Dashboard Broadcast
        broadcast_to_dashboard()
        
        log("--- Cycle Complete. Hibernating... ---")
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    main_loop()
