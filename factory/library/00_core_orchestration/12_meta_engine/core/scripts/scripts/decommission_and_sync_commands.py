#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

AG_ROOT = Path("/Users/Dorgham/Documents/Work/Devleopment/AIWF/.antigravity")
AI_CMDS = Path("/Users/Dorgham/Documents/Work/Devleopment/AIWF/.ai/commands")
LIB_CMDS = Path("/Users/Dorgham/Documents/Work/Devleopment/AIWF/factory/library/00-core-orchestration/commands")

def decommission_antigravity():
    if AG_ROOT.exists():
        print(f"[-] Decommissioning {AG_ROOT}...")
        shutil.rmtree(AG_ROOT)
    else:
        print("[!] .antigravity already decommissioned.")

def sync_high_density_manifests():
    print(f"[*] Syncing high-density manifests to {LIB_CMDS}...")
    # Clear old library commands
    for f in LIB_CMDS.iterdir():
        if f.is_file() and f.name != "README.md":
            f.unlink()
            
    # Sync from .ai/commands
    for f in AI_CMDS.iterdir():
        if f.is_file() and f.suffix == ".md":
            print(f"[+] Syncing {f.name}...")
            shutil.copy(str(f), str(LIB_CMDS / f.name))

if __name__ == "__main__":
    decommission_antigravity()
    sync_high_density_manifests()
