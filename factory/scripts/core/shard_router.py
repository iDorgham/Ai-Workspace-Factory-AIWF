#!/usr/bin/env python3
import sys
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]

def route_deployment(workspace_path):
    print(f"🛤️  Routing deployment for: {workspace_path}")
    
    metadata_path = Path(workspace_path) / "metadata.json"
    if not metadata_path.exists():
        print(f"⚠️  Missing metadata in {workspace_path}. Routing to DEFAULT shard.")
        return "default-global"
        
    try:
        with open(metadata_path, "r") as f:
            meta = json.load(f)
            ws_type = meta.get("workspace_type", "personal")
            region = meta.get("region", "mena")
            
            if ws_type == "client" and region == "egypt":
                return "mena-egypt-01"
            elif ws_type == "client":
                return "mena-general-01"
            else:
                return "personal-global-01"
    except:
        return "error-shard"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 shard_router.py <workspace_path>")
        sys.exit(1)
    
    shard = route_deployment(sys.argv[1])
    print(f"🎯 Target Shard: {shard}")
