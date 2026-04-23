#!/usr/bin/env python3
"""
AIWF Hot-Sync Engine v7.2.0
Logic for propagating library updates to sovereign workspaces.
"""

import os
import shutil
import json
import hashlib
from datetime import datetime

class SyncEngine:
    def __init__(self, factory_root):
        self.factory_root = factory_root
        self.library_path = os.path.join(factory_root, "factory/library/12-meta-engine/meta-orchestration/v7-orchestration")
        self.workspaces_path = os.path.join(factory_root, "workspaces")
        self.timestamp = datetime.now().isoformat()

    def get_workspaces(self):
        """List all valid workspaces."""
        workspaces = []
        for d in os.listdir(self.workspaces_path):
            wp = os.path.join(self.workspaces_path, d)
            if os.path.isdir(wp):
                # Search for 001_xxx subfolder
                for sub in os.listdir(wp):
                    sub_path = os.path.join(wp, sub)
                    if os.path.isdir(sub_path) and (sub.startswith("001_") or os.path.exists(os.path.join(sub_path, ".ai"))):
                        workspaces.append(sub_path)
        return workspaces

    def sync_workspace(self, ws_path, dry_run=False):
        """Propagate v7 orchestration layer to a specific workspace."""
        print(f"🔄 Syncing: {os.path.basename(ws_path)}")
        
        updates = [
            ("agents-registry.md", ".ai/agents/agents-registry.md"),
            ("command-system.yaml", ".ai/commands/v7-command-system.yaml"),
            ("tutorial.md", ".ai/commands/tutorial.md"),
            ("skills/generative-art-pipeline/SKILL.md", ".ai/skills/generative-art-pipeline/SKILL.md")
        ]

        changes = []
        for src_rel, dest_rel in updates:
            src = os.path.join(self.library_path, src_rel)
            dest = os.path.join(ws_path, dest_rel)
            
            if not os.path.exists(src):
                print(f"⚠️ Source missing: {src_rel}")
                continue

            # Ensure destination directory exists
            os.makedirs(os.path.dirname(dest), exist_ok=True)

            if dry_run:
                print(f"  [DRY-RUN] Would copy {src_rel} -> {dest_rel}")
            else:
                shutil.copy2(src, dest)
                changes.append(dest_rel)

        # Update sync log in workspace
        if not dry_run and changes:
            log_path = os.path.join(ws_path, ".ai/logs/sync.log")
            os.makedirs(os.path.dirname(log_path), exist_ok=True)
            with open(log_path, "a") as f:
                f.write(f"{self.timestamp} | SYNC v7.2.0 | Reasoning: sha256:sync-v7-{hashlib.md5(ws_path.encode()).hexdigest()[:8]}\n")
        
        return len(changes)

    def sync_all(self, dry_run=False):
        """Sync all workspaces."""
        workspaces = self.get_workspaces()
        print(f"🚀 Starting Hot-Sync for {len(workspaces)} workspaces...")
        
        results = {}
        for ws in workspaces:
            count = self.sync_workspace(ws, dry_run)
            results[ws] = count
            
        print("\n✅ Sync Complete.")
        return results

if __name__ == "__main__":
    import sys
    root = "/Users/Dorgham/Documents/Work/Devleopment/AIWF"
    engine = SyncEngine(root)
    
    is_dry = "--dry-run" in sys.argv
    engine.sync_all(dry_run=is_dry)
