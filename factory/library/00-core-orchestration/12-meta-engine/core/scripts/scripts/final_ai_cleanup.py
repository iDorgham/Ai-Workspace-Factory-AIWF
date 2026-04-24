#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

AI_ROOT = Path("/Users/Dorgham/Documents/Work/Devleopment/AIWF/.ai")

def move_safe(src, dest):
    if src.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        print(f"[*] Moving {src.relative_to(AI_ROOT)} -> {dest.relative_to(AI_ROOT)}")
        if dest.is_dir():
            shutil.move(str(src), str(dest / src.name))
        else:
            shutil.move(str(src), str(dest))

def cleanup():
    print("[*] Starting Final .ai Directory Sanctification...")
    
    # 1. Delete Legacy
    legacy_dirs = ["commands-cross-tool"]
    for d in legacy_dirs:
        path = AI_ROOT / d
        if path.exists():
            print(f"[-] Deleting legacy: {d}")
            shutil.rmtree(path)
            
    # 2. Reorganize CLI Layer
    cli_layer = AI_ROOT / "cli-layer"
    if cli_layer.exists():
        move_safe(cli_layer / "command-routing.json", AI_ROOT / "registry/routing/command-routing.json")
        move_safe(cli_layer / "flag-parser.md", AI_ROOT / "registry/routing/flag-parser.md")
        move_safe(cli_layer / "tool-router.md", AI_ROOT / "registry/routing/tool-router.md")
        move_safe(cli_layer / "error-handling.md", AI_ROOT / "governance/error-handling.md")
        shutil.rmtree(cli_layer)
        
    # 3. Consolidate Tool Adapters
    move_safe(AI_ROOT / "tool-adapters", AI_ROOT / "registry/adapters")
    
    # 4. Archive Migrations
    move_safe(AI_ROOT / "migrations", AI_ROOT / "compat/migrations")
    
    # 5. Organize Scripts
    script_dir = AI_ROOT / "scripts"
    if script_dir.exists():
        (script_dir / "core").mkdir(exist_ok=True)
        (script_dir / "maintenance").mkdir(exist_ok=True)
        (script_dir / "intelligence").mkdir(exist_ok=True)
        
        script_moves = {
            "core": [
                "chaos_validator.py", "fetch-official-skills.py", "gate_verifier.py", 
                "master_sync.py", "recursive_engine.py", "render_dashboard.py",
                "silent_phase_release.py", "swarm_router.py", "sync_master_memory.py",
                "sync_registry.py", "volatility_scaler.py"
            ],
            "maintenance": [
                "audit_path_integrity.py", "healing_agent.py", "library-health-scorer.py",
                "run-smoke-tests.py", "smoke_test.sh"
            ],
            "intelligence": [
                "proactive_brainstorm_trigger.py"
            ]
        }
        
        for subdir, files in script_moves.items():
            for f in files:
                move_safe(script_dir / f, script_dir / subdir / f)

if __name__ == "__main__":
    cleanup()
