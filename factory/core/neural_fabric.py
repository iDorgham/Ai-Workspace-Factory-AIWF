import json
import os
from datetime import datetime
import hashlib

class NeuralFabric:
    def __init__(self, workspace_root):
        self.root = workspace_root
        self.ledger_path = os.path.join(self.root, ".ai/intelligence_ledger.jsonl")
        self.active_nodes = ["node-mena-01", "node-mena-02", "node-global-01"]

    def propose_state_update(self, source_shard, update_data, signatures):
        """Joint-Consensus State Propagation."""
        print(f"🧠 [SYNC] Proposing intelligence update from {source_shard}...")
        
        # Verify 2/3 Consensus
        required_votes = len(self.active_nodes) * 2 // 3 + 1
        valid_votes = sum(1 for s in signatures if s in self.active_nodes)
        
        if valid_votes < required_votes:
            print(f"🚨 [BLOCK] Consensus Failure: {valid_votes}/{required_votes} votes obtained.")
            return False

        consensus_hash = hashlib.sha256(json.dumps(update_data).encode()).hexdigest()
        print(f"✅ [CONSENSUS] Update Authorized: {consensus_hash[:12]}")
        
        self.log_sync_event(source_shard, consensus_hash, "AUTHORIZED")
        return True

    def log_sync_event(self, source, consensus_hash, status):
        entry = {
            "ts": datetime.now().isoformat(),
            "source": source,
            "consensus_hash": consensus_hash,
            "status": status,
            "compliance_id": "LAW151-SYNC-015"
        }
        with open(self.ledger_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--data", default='{"intelligence": "alpha"}')
    parser.add_argument("--votes", nargs="+", default=[])
    args = parser.parse_args()

    fabric = NeuralFabric(".")
    data = json.loads(args.data)
    fabric.propose_state_update(args.source, data, args.votes)
