#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

ROOT = Path("/Users/Dorgham/Documents/Work/Devleopment/AIWF")
WS_CLIENTS = ROOT / "workspaces/clients"
WS_PERSONAL = ROOT / "workspaces/personal"
OLD_PLAN = ROOT / "plan"
NEW_PLAN = ROOT / ".ai/plan"
MEMORY_DIR = ROOT / ".ai/memory"

def cleanup_workspaces():
    print("[*] Emptying workspaces...")
    for d in [WS_CLIENTS, WS_PERSONAL]:
        if d.exists():
            for item in d.iterdir():
                if item.name != ".gitkeep":
                    print(f"[-] Deleting workspace project: {item.name}")
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()

def move_and_reorganize_plan():
    print("[*] Moving and reorganizing plan into .ai/plan/...")
    NEW_PLAN.mkdir(parents=True, exist_ok=True)
    dev_plan = NEW_PLAN / "development"
    cont_plan = NEW_PLAN / "content"
    soc_plan = NEW_PLAN / "social"
    dev_plan.mkdir(exist_ok=True)
    cont_plan.mkdir(exist_ok=True)
    soc_plan.mkdir(exist_ok=True)
    
    if OLD_PLAN.exists():
        # Move manifest
        if (OLD_PLAN / "_manifest.yaml").exists():
            shutil.move(str(OLD_PLAN / "_manifest.yaml"), str(NEW_PLAN / "_manifest.yaml"))
            
        for item in OLD_PLAN.iterdir():
            if item.is_dir():
                # Content-related
                if "content" in item.name.lower():
                    print(f"[*] Moving {item.name} -> plan/content/")
                    shutil.move(str(item), str(cont_plan / item.name))
                # Development-related (everything else)
                else:
                    print(f"[*] Moving {item.name} -> plan/development/")
                    shutil.move(str(item), str(dev_plan / item.name))
        
        # Cleanup old plan dir
        if not any(OLD_PLAN.iterdir()):
            OLD_PLAN.rmdir()

def clean_memory():
    print("[*] Resetting industrial memory...")
    if MEMORY_DIR.exists():
        # Keep the directory but clear contents that are mutable state
        for item in MEMORY_DIR.iterdir():
            if item.name in ["state.json", "workspace-index.json", "workspace-memory.md", "library-health-report.json"]:
                print(f"[-] Resetting memory file: {item.name}")
                item.unlink()
            elif item.is_dir() and item.name in ["context-cache", "multi-tool-state"]:
                print(f"[-] Clearing memory cache: {item.name}")
                shutil.rmtree(item)
                item.mkdir()

if __name__ == "__main__":
    cleanup_workspaces()
    move_and_reorganize_plan()
    clean_memory()
