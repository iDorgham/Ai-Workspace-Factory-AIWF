#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

FACTORY_ROOT = Path("/Users/Dorgham/Documents/Work/Devleopment/AIWF/factory")
LIB_ROOT = FACTORY_ROOT / "library"

def move_safe(src, dest):
    if src.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        print(f"[*] Moving {src.name} -> {dest.parent.relative_to(FACTORY_ROOT.parent)}/")
        if dest.is_dir():
            shutil.move(str(src), str(dest / src.name))
        else:
            shutil.move(str(src), str(dest))

def organize_factory():
    print("[*] Organizing Factory root...")
    move_safe(FACTORY_ROOT / "dna.json", FACTORY_ROOT / "core/dna.json")
    move_safe(FACTORY_ROOT / "aiwf.sh", FACTORY_ROOT / "core/aiwf.sh")
    move_safe(
        FACTORY_ROOT.parent / "DEEP_LIBRARY_DOC.md",
        FACTORY_ROOT.parent / "docs/reference/DEEP_LIBRARY_DOC.md",
    )

def organize_library():
    print("[*] Organizing Factory library...")
    reg_dir = LIB_ROOT / "registry"
    rep_dir = LIB_ROOT / "reports"
    reg_dir.mkdir(exist_ok=True)
    rep_dir.mkdir(exist_ok=True)
    
    lib_registry_files = ["REGISTRY.md", "DICTIONARY.md", "_taxonomy.json", "pipeline-alias-mapping.json"]
    for f in lib_registry_files:
        move_safe(LIB_ROOT / f, reg_dir / f)
        
    move_safe(LIB_ROOT / "INDUSTRY_MATURITY_REPORT.md", rep_dir / "INDUSTRY_MATURITY_REPORT.md")

def organize_scripts():
    print("[*] Organizing Factory scripts...")
    script_dir = FACTORY_ROOT / "scripts"
    
    moves = {
        "core": [
            "chain_executor.py", "compose.py", "registry_guardian.py", 
            "registry_validator.py", "swarm.py", "sync_engine.py", 
            "validate.py", "omega_release.py"
        ],
        "maintenance": [
            "chaos_validator.py", "compliance_auditor.py", "health_scorer.py", 
            "log_broadcaster.py", "organize_library.py", "rebuild_library_index.py", 
            "sanitize_profiles.py", "validate_library.py"
        ],
        "automation": [
            "plan_content.py", "saas_auto_generate.py", "saas_scaffolder.py", "harvest_engine.py"
        ],
        "utils": [
            "secrets_manager.py", "websocket_relay.py", "create-workspace.sh"
        ],
        "migrations": [
            "migrate_library_to_fields.py", "migrate_profiles.py"
        ]
    }
    
    for subdir, files in moves.items():
        for f in files:
            move_safe(script_dir / f, script_dir / subdir / f)

if __name__ == "__main__":
    organize_factory()
    organize_library()
    organize_scripts()
