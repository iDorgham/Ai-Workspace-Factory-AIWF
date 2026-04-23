#!/usr/bin/env python3
"""
AIWF Discovery Engine v9.0.0
Implementation of node discovery protocols for the Global Swarm.
"""

import os
import json
import time

class DiscoveryEngine:
    def __init__(self, factory_root):
        self.registry_path = os.path.join(factory_root, "factory/core/p2p/registry.json")
        os.makedirs(os.path.dirname(self.registry_path), exist_ok=True)

    def register_node(self, node_id, host, port):
        """Register local node in the shared registry."""
        registry = self.load_registry()
        registry[node_id] = {
            "address": f"{host}:{port}",
            "last_seen": time.time(),
            "status": "ONLINE"
        }
        self.save_registry(registry)
        print(f"📡 [DISCOVERY] Node {node_id} registered at {host}:{port}")

    def find_peers(self, exclude_id):
        """Return list of active peers."""
        registry = self.load_registry()
        peers = []
        for nid, data in registry.items():
            if nid != exclude_id:
                # Check if last seen is within 10 minutes
                if time.time() - data["last_seen"] < 600:
                    peers.append((nid, data["address"]))
        return peers

    def load_registry(self):
        if not os.path.exists(self.registry_path):
            return {}
        try:
            with open(self.registry_path, "r") as f:
                return json.load(f)
        except:
            return {}

    def save_registry(self, registry):
        with open(self.registry_path, "w") as f:
            json.dump(registry, f, indent=2)

if __name__ == "__main__":
    root = "/Users/Dorgham/Documents/Work/Devleopment/AIWF"
    engine = DiscoveryEngine(root)
    engine.register_node("factory-primary", "127.0.0.1", 9000)
    print(f"Found peers: {engine.find_peers('factory-primary')}")
