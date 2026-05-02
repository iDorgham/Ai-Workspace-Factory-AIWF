#!/usr/bin/env python3
"""
AIWF Industrial Mirror Sync v1.0.0
===================================
Deep outbound mirror: .ai/ → factory/library/

Mappings:
  .ai/agents/     -> factory/library/core_orchestration/registry/agents/
                   + factory/library/agents/workspace_imports/ai/agents/
                   + factory/library/archive/legacy_pillars/00_core_orchestration/registry/agents/
  .ai/commands/   -> factory/library/commands/
  .ai/governance/ -> factory/library/core_orchestration/omega_singularity/governance/
  .ai/plan/       -> factory/library/planning/
  .ai/skills/     -> factory/library/skills/ (per-skill folders; `egyptian_arabic_content_master` may merge)
  .ai/subagents/  -> factory/library/subagents/workspace_imports/ai/subagents/
  .ai/templates/  -> factory/library/templates/
  .ai/registry/   -> factory/library/registry/
  .ai/rules/      -> factory/library/rules/workspace_imports/ai/rules/

Exclusions:
  logs/, locks/, memory/, dashboard/, .DS_Store
"""

import os
import shutil
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# --- CONFIGURATION ---
ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = ROOT / ".ai"
LIBRARY_ROOT = ROOT / "factory/library"

MAPPINGS = {
    "agents": "core_orchestration/registry/agents",
    "commands": "commands",
    "governance": "core_orchestration/omega_singularity/governance",
    "plan": "planning",
    "skills": "skills",
    "subagents": "subagents/workspace_imports/ai/subagents",
    "templates": "templates",
    "registry": "registry",
    "rules": "rules/workspace_imports/ai/rules",
}

# Additional destinations for the same .ai/agents/ tree (keep imports + legacy pillars aligned).
AGENT_MIRROR_EXTRA = (
    "agents/workspace_imports/ai/agents",
    "archive/legacy_pillars/00_core_orchestration/registry/agents",
)

EXCLUSIONS = {"logs", "locks", "memory", "dashboard", ".DS_Store", "__pycache__", "tmp", "scratch"}

def _git_head_sha():
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT, capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() if result.returncode == 0 else "no-git"
    except:
        return "no-git"

def generate_reasoning_hash(synced_files):
    git_sha = _git_head_sha()
    timestamp = datetime.now(timezone.utc).isoformat()
    payload = f"{git_sha}:{timestamp}:{':'.join(sorted(synced_files))}"
    return f"sha256:{hashlib.sha256(payload.encode()).hexdigest()[:16]}"

def sync_dir(src, dest):
    copied = []
    if not src.exists():
        return copied
    
    os.makedirs(dest, exist_ok=True)
    
    for item in src.iterdir():
        if item.name in EXCLUSIONS:
            continue
            
        rel_path = item.relative_to(src)
        target_path = dest / rel_path
        
        if item.is_dir():
            copied.extend(sync_dir(item, target_path))
        else:
            shutil.copy2(item, target_path)
            copied.append(str(item.relative_to(ROOT)))
            
    return copied

def main():
    print(f"🚀 Starting Industrial Deep Sync (v20.0 OMEGA)")
    print(f"Source: {SOURCE_ROOT.relative_to(ROOT)}")
    print(f"Library: {LIBRARY_ROOT.relative_to(ROOT)}")
    print("-" * 50)

    total_synced = []

    for src_slug, dest_rel in MAPPINGS.items():
        src_path = SOURCE_ROOT / src_slug
        dest_path = LIBRARY_ROOT / dest_rel
        
        if not src_path.exists():
            print(f"⚠️  Skipping {src_slug} (Source not found)")
            continue
            
        print(f"🔄 Syncing {src_slug} -> {dest_rel}...")
        synced = sync_dir(src_path, dest_path)
        total_synced.extend(synced)
        print(f"   ✅ {len(synced)} files synced.")

        if src_slug == "agents":
            for extra_rel in AGENT_MIRROR_EXTRA:
                extra_dest = LIBRARY_ROOT / extra_rel
                print(f"🔄 Syncing {src_slug} -> {extra_rel} (parallel mirror)...")
                extra_synced = sync_dir(src_path, extra_dest)
                total_synced.extend(extra_synced)
                print(f"   ✅ {len(extra_synced)} files synced.")

    reasoning_hash = generate_reasoning_hash(total_synced)
    
    # Log to evolution ledger
    ledger_path = ROOT / ".ai/logs/ledgers/evolution_ledger.jsonl"
    os.makedirs(ledger_path.parent, exist_ok=True)
    
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": "industrial_deep_sync",
        "details": {
            "files_synced": len(total_synced),
            "mappings": MAPPINGS
        },
        "reasoning_hash": reasoning_hash,
        "status": "success"
    }
    
    with open(ledger_path, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    print("-" * 50)
    print(f"✅ Industrial Deep Sync Complete.")
    print(f"📊 Total Files: {len(total_synced)}")
    print(f"🔒 Reasoning Hash: {reasoning_hash}")
    print(f"📝 Logged to: {ledger_path.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
