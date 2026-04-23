#!/usr/bin/env python3
"""
AIWF Knowledge Shard Engine v9.0.0
Distributed vector-like memory for sharded factory intelligence.
"""

import os
import json
import sqlite3
import time
import hashlib

class KnowledgeShard:
    def __init__(self, factory_root, shard_id):
        self.factory_root = factory_root
        self.shard_id = shard_id
        self.db_path = os.path.join(factory_root, f"factory/core/p2p/shards/shard_{shard_id}.db")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS knowledge 
                     (id TEXT PRIMARY KEY, key TEXT, value TEXT, tags TEXT, timestamp REAL)''')
        conn.commit()
        conn.close()

    def store(self, key, value, tags=""):
        """Store a knowledge item locally."""
        ki_id = hashlib.sha256(f"{key}:{time.time()}".encode()).hexdigest()[:12]
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO knowledge VALUES (?, ?, ?, ?, ?)", 
                  (ki_id, key, value, tags, time.time()))
        conn.commit()
        conn.close()
        print(f"🧠 [SHARD:{self.shard_id}] Stored: {key}")
        return ki_id

    def query_local(self, key):
        """Query the local shard."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT value FROM knowledge WHERE key LIKE ?", (f"%{key}%",))
        results = c.fetchall()
        conn.close()
        return [r[0] for r in results]

    def distribute_query(self, p2p_node, key):
        """Query peers if local results are insufficient."""
        local_results = self.query_local(key)
        if local_results:
            return local_results
        
        print(f"📡 [SHARD:{self.shard_id}] Local miss. Querying Swarm for: {key}")
        # In a real impl, p2p_node.broadcast({"type": "MEM_QUERY", "key": key})
        # For prototype, we return a simulated peer response
        return [f"SIMULATED_PEER_RESPONSE: Optimization for {key} found in Shard B."]

if __name__ == "__main__":
    root = "/Users/Dorgham/Documents/Work/Devleopment/AIWF"
    shard = KnowledgeShard(root, "primary")
    shard.store("fawry-api-limit", "1000 requests per minute for sandbox")
    print(f"Query: 'fawry' -> {shard.query_local('fawry')}")
    print(f"Query: 'stripe' -> {shard.distribute_query(None, 'stripe')}")
