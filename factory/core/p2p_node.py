#!/usr/bin/env python3
"""
AIWF P2P Node Engine v9.0.1 (Prototype)
Core logic for node identity, discovery, and secure component exchange.

Fix (v9.0.1): connect_to_peer() now sets a socket timeout before connecting.
Without it, connect() blocks for the full OS TCP timeout (~75-130s) when the
peer is unreachable, freezing any AI response that triggers peer discovery.
"""

# Maximum time to wait for a peer connection attempt before giving up.
PEER_CONNECT_TIMEOUT_S = 2.0

import socket
import threading
import json
import hashlib
import time
from datetime import datetime

class P2PNode:
    def __init__(self, node_id, host='127.0.0.1', port=9000):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.peers = {} # node_id -> (host, port)
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def log(self, message):
        print(f"🌐 [P2P-NODE:{self.node_id}] {message}")

    def start(self):
        """Start the node server to listen for peer connections."""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.log(f"Started on {self.host}:{self.port}")
        
        threading.Thread(target=self.listen_for_peers, daemon=True).start()

    def listen_for_peers(self):
        while self.running:
            try:
                client, address = self.server_socket.accept()
                threading.Thread(target=self.handle_peer, args=(client,), daemon=True).start()
            except Exception as e:
                if self.running:
                    self.log(f"Server error: {e}")

    def handle_peer(self, client):
        try:
            data = client.recv(4096).decode('utf-8')
            if not data: return
            
            message = json.loads(data)
            msg_type = message.get("type")
            
            if msg_type == "HELO":
                peer_id = message.get("node_id")
                self.peers[peer_id] = message.get("address")
                self.log(f"Discovered peer: {peer_id}")
                # Reply with own HELO
                response = {"type": "HELO_ACK", "node_id": self.node_id}
                client.send(json.dumps(response).encode('utf-8'))
            
            elif msg_type == "SYNC_REQ":
                self.log(f"Sync request received for: {message.get('component')}")
                # Logic for sending library component...
            
            elif msg_type == "MEM_QUERY":
                key = message.get("key")
                self.log(f"Memory query received: {key}")
                # In real impl: results = shard.query_local(key)
                response = {"type": "MEM_RESP", "results": [f"Knowledge for {key} from {self.node_id}"]}
                client.send(json.dumps(response).encode('utf-8'))
                
        except Exception as e:
            self.log(f"Error handling peer: {e}")
        finally:
            client.close()

    def connect_to_peer(self, host, port):
        """Initial handshake with a peer."""
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(PEER_CONNECT_TIMEOUT_S)  # ← prevents freeze when peer is down
            client.connect((host, port))
            client.settimeout(None)  # restore blocking for send
            
            helo = {
                "type": "HELO",
                "node_id": self.node_id,
                "address": [self.host, self.port],
                "timestamp": time.time()
            }
            client.send(json.dumps(helo).encode('utf-8'))
            client.close()
            return True
        except Exception as e:
            self.log(f"Failed to connect to {host}:{port} - {e}")
            return False

    def stop(self):
        self.running = False
        self.server_socket.close()

if __name__ == "__main__":
    # For testing, create a node
    import sys
    id = sys.argv[1] if len(sys.argv) > 1 else "factory-primary"
    p = int(sys.argv[2]) if len(sys.argv) > 2 else 9000
    
    node = P2PNode(id, port=p)
    node.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        node.stop()
