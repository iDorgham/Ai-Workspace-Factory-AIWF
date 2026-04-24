import os
import json
from pathlib import Path

class DistributionRouter:
    """
    Industrial Distribution Router v1.0.0
    Manages multi-region shard propagation for AIWF.
    """
    
    def __init__(self, factory_root: str):
        self.factory_root = Path(factory_root)
        self.spec_path = self.factory_root / "plan/12-distribution/distribution-router.spec.json"
        self.workspaces_path = self.factory_root / "workspaces"
        self.regions = ["aws-me-1", "gcp-eg-1", "azure-uae-1"]

    def load_spec(self):
        with open(self.spec_path, 'r') as f:
            self.spec = json.load(f)

    def discover_shards(self):
        """Scans for active sovereign shards in the workspaces."""
        shards = []
        for d in self.workspaces_path.iterdir():
            if d.is_dir():
                # Recursive search for .ai marker
                for sub in d.iterdir():
                    if sub.is_dir() and (sub / ".ai").exists():
                        shards.append(sub)
        return shards

    def route_shard(self, shard_path: Path):
        """Determines the target regions for a given shard."""
        shard_name = shard_path.name
        print(f"🚢 Routing Shard: {shard_name}")
        
        # Simplified routing logic
        targets = [self.regions[0]] # Default to primary MENA region
        if "global" in shard_name.lower():
            targets = self.regions
            
        print(f"  - Target Regions: {', '.join(targets)}")
        return targets

    def propagate_all(self):
        print("🚀 [DIST-ROUTER] Initializing Global Shard Propagation...")
        self.load_spec()
        shards = self.discover_shards()
        
        results = {}
        for shard in shards:
            targets = self.route_shard(shard)
            results[shard.name] = targets
            
        print("\n✅ Propagation Strategy Mapped.")
        return results

if __name__ == "__main__":
    router = DistributionRouter(".")
    router.propagate_all()
