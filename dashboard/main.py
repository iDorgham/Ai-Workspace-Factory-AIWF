import json
import asyncio
import os
from pathlib import Path
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="AI Workspace Factory Master Dashboard")

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
AGGREGATED_STATE = BASE_DIR / "master" / ".ai" / "memory" / "aggregated-state.json"
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

# Connection Manager for WebSockets
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

WATCHDOG_PID_FILE = BASE_DIR / "master" / ".ai" / ".watchdog.pid"

def get_watchdog_status():
    if WATCHDOG_PID_FILE.exists():
        try:
            pid = int(WATCHDOG_PID_FILE.read_text().strip())
            # Basic check if PID is alive on MacOS/Linux
            os.kill(pid, 0)
            return {"active": True, "pid": pid}
        except (ProcessLookupError, ValueError, OSError):
            return {"active": False, "pid": None}
    return {"active": False, "pid": None}

@app.get("/health")
def health():
    return {
        "status": "healthy", 
        "aggregated_state_exists": AGGREGATED_STATE.exists(),
        "watchdog": get_watchdog_status()
    }

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    with open(TEMPLATES_DIR / "index.html", "r") as f:
        return f.read()

@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Send initial state
        if AGGREGATED_STATE.exists():
            with open(AGGREGATED_STATE, "r") as f:
                state = json.load(f)
                state["watchdog"] = get_watchdog_status()
                await websocket.send_json({"type": "initial_state", "data": state})
        
        while True:
            await asyncio.sleep(10)
            # Push periodic heartbeat status even if state hasn't changed
            await websocket.send_json({"type": "watchdog_heartbeat", "status": get_watchdog_status()})
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/api/state")
async def get_state():
    """Returns the consolidated state for HTTP polling fallback"""
    if AGGREGATED_STATE.exists():
        with open(AGGREGATED_STATE, "r") as f:
            state = json.load(f)
            state["watchdog"] = get_watchdog_status()
            return state
    return {"error": "state_not_found"}

@app.post("/api/update-state")
async def update_state():
    """Manual trigger to re-read and broadcast state (used by sync protocol)"""
    if AGGREGATED_STATE.exists():
        with open(AGGREGATED_STATE, "r") as f:
            state = json.load(f)
            state["watchdog"] = get_watchdog_status()
            await manager.broadcast(json.dumps({"type": "update", "data": state}))
    return {"status": "broadcast_sent"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
