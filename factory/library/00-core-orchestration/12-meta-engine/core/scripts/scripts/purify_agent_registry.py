#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

AGENT_DIR = Path("/Users/Dorgham/Documents/Work/Devleopment/AIWF/.ai/agents")
SUBAGENT_DIR = Path("/Users/Dorgham/Documents/Work/Devleopment/AIWF/.ai/subagents")

# 1. Cleanup Legacy/Deprecated
DELETED_FILES = [
    "agents.md",
    "master-guide-v13.json",
    "registry.json"
]

# 2. Rename & Core Assignment
RENAMES = {
    "factory-manager.md": "factory_orchestrator.md",
    "healing-bot.md": "healing_bot_v2.md",
    "guide-agent.md": "teaching_agent.md",
    "swarm-router-v3.md": "swarm_router_v3.md" # Just normalization
}

# 3. Categorization
CORE_AGENTS = [
    "factory_orchestrator.md",
    "healing_bot_v2.md",
    "teaching_agent.md",
    "swarm_router_v3.md",
    "master-guide.md",
    "antigravity-agent.md",
    "library-curator.md",
    "recursive-engine.json",
    "chaos-validator.json"
]

REGISTRY_FILES = [
    "registry.yaml",
    "routing_map.yaml",
    "sub-agent-contracts.json"
]

def organize():
    print("[*] Starting Agent Registry Purification...")
    
    # Create structure
    (AGENT_DIR / "core").mkdir(exist_ok=True)
    (AGENT_DIR / "specialized").mkdir(exist_ok=True)
    (AGENT_DIR / "registry").mkdir(exist_ok=True)
    (AGENT_DIR / "legacy").mkdir(exist_ok=True)
    
    # Delete legacy
    for f in DELETED_FILES:
        path = AGENT_DIR / f
        if path.exists():
            print(f"[-] Deleting legacy: {f}")
            path.unlink()
            
    # Rename
    for old, new in RENAMES.items():
        old_path = AGENT_DIR / old
        new_path = AGENT_DIR / new
        if old_path.exists():
            print(f"[*] Renaming: {old} -> {new}")
            shutil.move(str(old_path), str(new_path))
            
    # Move to Core
    for f in CORE_AGENTS:
        src = AGENT_DIR / f
        if src.exists():
            print(f"[*] Moving to CORE: {f}")
            shutil.move(str(src), str(AGENT_DIR / "core" / f))
            
    # Move to Registry
    for f in REGISTRY_FILES:
        src = AGENT_DIR / f
        if src.exists():
            print(f"[*] Moving to REGISTRY: {f}")
            shutil.move(str(src), str(AGENT_DIR / "registry" / f))
            
    # Move everything else to Specialized (including subagents)
    for f in AGENT_DIR.iterdir():
        if f.is_file() and f.suffix in [".md", ".json", ".yaml"] and f.name != ".DS_Store":
            print(f"[*] Moving to SPECIALIZED: {f.name}")
            shutil.move(str(f), str(AGENT_DIR / "specialized" / f.name))
            
    # Move subagents to specialized/subagents
    (AGENT_DIR / "specialized" / "subagents").mkdir(exist_ok=True)
    for f in SUBAGENT_DIR.iterdir():
        if f.is_file() and f.suffix == ".json":
            print(f"[*] Moving subagent: {f.name}")
            shutil.move(str(f), str(AGENT_DIR / "specialized" / "subagents" / f.name))
            
    # Final cleanup of empty subagents dir
    if not any(SUBAGENT_DIR.iterdir()):
        SUBAGENT_DIR.rmdir()

if __name__ == "__main__":
    organize()
