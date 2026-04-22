#!/usr/bin/env python3
import os
import sys
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG_FILE = ROOT / ".ai" / "logs" / "learning-engine.md"
SKILL_MEMORY_DIR = ROOT / ".ai" / "memory" / "skill-memory"

def generate_reasoning_hash(agent_id="RE"):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    nonce = os.urandom(2).hex()
    return f"[{agent_id}-{timestamp}-{nonce}]"

def log_event(message, hash_id):
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(LOG_FILE, "a") as f:
        f.write(f"- **{timestamp}** {hash_id}: {message}\n")

def analyze_workflow(project_path: Path):
    workflow_log = project_path / ".ai" / "memory" / "workflow.jsonl"
    if not workflow_log.exists():
        return []

    corrections = []
    with open(workflow_log, "r") as f:
        for line in f:
            try:
                entry = json.loads(line)
                # Look for /refine or /polish commands
                if entry.get("command") in ["/refine", "/polish"]:
                    corrections.append(entry)
            except json.JSONDecodeError:
                continue
    return corrections

def generate_skill_manifest(skill_id, patterns):
    manifest_path = SKILL_MEMORY_DIR / f"{skill_id}-learning.json"
    data = {
        "skill_id": skill_id,
        "last_updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "correction_patterns": patterns,
        "status": "draft"
    }
    
    with open(manifest_path, "w") as f:
        json.dump(data, f, indent=2)
    return manifest_path

def learn(workspaces_root: str, dry_run: bool = True):
    root = Path(workspaces_root)
    all_corrections = {}

    # Scan for all workflow logs
    for workflow_file in root.glob("**/workflow.jsonl"):
        project_path = workflow_file.parents[2] # Adjust based on 00X_ hierarchy
        project_name = project_path.name
        
        corrections = analyze_workflow(project_path)
        if corrections:
            for c in corrections:
                skill_id = c.get("context", {}).get("skill_id", "unknown_skill")
                if skill_id not in all_corrections:
                    all_corrections[skill_id] = []
                all_corrections[skill_id].append({
                    "project": project_name,
                    "input": c.get("input"),
                    "output_id": c.get("target_id"),
                    "timestamp": c.get("timestamp")
                })

    # Process clusters
    for skill_id, patterns in all_corrections.items():
        if len(patterns) >= 1: # Threshold for learning
            msg = f"Identified learning pattern for skill '{skill_id}' from {len(patterns)} corrections."
            print(f"🧠 {msg}")
            hash_id = generate_reasoning_hash()
            if not dry_run:
                manifest_path = generate_skill_manifest(skill_id, patterns)
                log_event(f"{msg} Manifest created: {manifest_path.name}", hash_id)
            else:
                print(f"   [DRY-RUN] Would generate manifest for '{skill_id}'")

def main():
    ws_root = str(ROOT / "workspaces")
    dry_run = "--execute" not in sys.argv
    
    if not LOG_FILE.parent.exists():
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not SKILL_MEMORY_DIR.exists():
        SKILL_MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        
    if not LOG_FILE.exists():
        with open(LOG_FILE, "w") as f:
            f.write("# 🧠 RECURSIVE LEARNING ENGINE LOGS\n\n")

    print(f"🐝 Recursive Learning Engine analyzing '{ws_root}'...")
    learn(ws_root, dry_run)
    
    if dry_run:
        print("\n⚠️  Dry-run complete. Use '--execute' to generate skill manifests.")
    else:
        print("\n✅ Learning complete. Check '.ai/logs/learning-engine.md' for details.")

if __name__ == "__main__":
    main()
