#!/usr/bin/env python3
"""
AIWF Registry-Guardian v1.0.0
Industrial immune system for the command registry.
Detects YAML duplicate keys and ID collisions.
"""

import sys
import os
from datetime import datetime

class RegistryGuardian:
    def __init__(self, registry_path):
        self.registry_path = registry_path
        self.log_path = "factory/reports/registry_repairs.log"

    def log_repair(self, issue_type, details):
        """Log the repair event with ISO-8601 timestamp."""
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        with open(self.log_path, "a") as f:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "issue": issue_type,
                "details": details,
                "reasoning_hash": f"sha256:repair-{datetime.now().timestamp()}"
            }
            import json
            f.write(json.dumps(entry) + "\n")
        print(f"🔧 [REPAIR-LOGGED] {issue_type}: {details}")

    def audit(self):
        """Audit the registry for structural and semantic integrity (Dependency-Free)."""
        print(f"🛡️  [REGISTRY-GUARDIAN] Auditing: {self.registry_path}")
        
        if not os.path.exists(self.registry_path):
            print("❌ Registry file not found.")
            return False

        keys = []
        ids = []
        duplicates = []
        id_collisions = []
        
        with open(self.registry_path, "r") as f:
            for line in f:
                stripped = line.strip()
                
                # 1. Detect Duplicate Keys (Root Level)
                if stripped.endswith(":") and not line.startswith(" ") and not line.startswith("\t") and not stripped.startswith("-") and not stripped.startswith("#"):
                    key = stripped[:-1].strip()
                    if key in keys:
                        duplicates.append(key)
                    else:
                        keys.append(key)
                
                # 2. Detect ID Collisions (Precise match for 'id:' key)
                if stripped.startswith("id:") or " id:" in stripped:
                    if not stripped.startswith("#"):
                        cmd_id = stripped.split("id:")[1].strip().strip('"').strip("'")
                        if cmd_id in ids:
                            id_collisions.append(cmd_id)
                        else:
                            ids.append(cmd_id)

        if duplicates:
            self.log_repair("DUPLICATE_KEY_DETECTED", duplicates)
            print(f"⚠️  [BLOCK] Duplicate keys found: {duplicates}")
            return False

        if id_collisions:
            self.log_repair("ID_COLLISION_DETECTED", id_collisions)
            print(f"⚠️  [BLOCK] ID Collisions found: {id_collisions}")
            return False

        print("✨ [REGISTRY-GUARDIAN] Integrity verified. Proceeding to sync.")
        return True

if __name__ == "__main__":
    registry = "/Users/Dorgham/Documents/Work/Devleopment/AIWF/factory/library/12-meta-engine/meta-orchestration/v7-orchestration/command-system.yaml"
    guardian = RegistryGuardian(registry)
    if not guardian.audit():
        sys.exit(1)
