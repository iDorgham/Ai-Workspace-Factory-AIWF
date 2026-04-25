#!/usr/bin/env python3
"""
AIWF Log Broadcaster v1.1.0
Utility for workspaces to stream logs to the Omega Relay.

Fix (v1.1.0): Added CONNECT_TIMEOUT_S to prevent blocking the calling process
when the Omega Relay is not running. Without a timeout, socket.connect() uses
the OS default TCP connect timeout (~75-130s on Linux/macOS), which freezes
AI responses in Antigravity and any other caller.
"""

import socket
import json
from datetime import datetime

# Hard cap on connect attempt — relay is optional infrastructure.
# If it is not reachable within this window, we silently skip and continue.
CONNECT_TIMEOUT_S = 1.0

class LogBroadcaster:
    def __init__(self, workspace_slug, relay_host='127.0.0.1', relay_port=9001):
        self.workspace_slug = workspace_slug
        self.relay_host = relay_host
        self.relay_port = relay_port

    def send_log(self, level, message):
        """Send a log event to the relay."""
        event = {
            "type": "LOG_STREAM",
            "workspace": self.workspace_slug,
            "level": level,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        self._transmit(event)

    def send_ping(self):
        """Send a health ping to the relay."""
        event = {
            "type": "HEALTH_PING",
            "workspace": self.workspace_slug,
            "timestamp": datetime.now().isoformat()
        }
        self._transmit(event)

    def _transmit(self, event):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(CONNECT_TIMEOUT_S)   # ← prevents OS-level TCP freeze
                s.connect((self.relay_host, self.relay_port))
                s.settimeout(None)                 # restore blocking for sendall
                s.sendall((json.dumps(event) + "\n").encode())
        except Exception:
            # Relay is optional — silently skip if not reachable
            pass

if __name__ == "__main__":
    import sys
    slug = sys.argv[1] if len(sys.argv) > 1 else "test-workspace"
    msg = sys.argv[2] if len(sys.argv) > 2 else "Relay connection test."
    
    broadcaster = LogBroadcaster(slug)
    broadcaster.send_log("INFO", msg)
    print(f"📡 Broadcast sent from {slug}")
