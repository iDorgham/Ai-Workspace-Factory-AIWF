#!/usr/bin/env python3
"""
AIWF Log Broadcaster v1.0.0
Utility for workspaces to stream logs to the Omega Relay.
"""

import socket
import json
from datetime import datetime

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
                s.connect((self.relay_host, self.relay_port))
                s.sendall((json.dumps(event) + "\n").encode())
        except Exception:
            # Silently fail if relay is down
            pass

if __name__ == "__main__":
    import sys
    slug = sys.argv[1] if len(sys.argv) > 1 else "test-workspace"
    msg = sys.argv[2] if len(sys.argv) > 2 else "Relay connection test."
    
    broadcaster = LogBroadcaster(slug)
    broadcaster.send_log("INFO", msg)
    print(f"📡 Broadcast sent from {slug}")
