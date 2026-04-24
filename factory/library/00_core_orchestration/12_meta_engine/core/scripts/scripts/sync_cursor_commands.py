#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

CURSOR_CMDS = Path("/Users/Dorgham/Documents/Work/Devleopment/AIWF/.cursor/commands")
AI_CMDS = Path("/Users/Dorgham/Documents/Work/Devleopment/AIWF/.ai/commands")

def update_cursor_commands():
    print(f"[*] Updating Cursor command registries in {CURSOR_CMDS}...")
    
    # 1. Clear old commands
    for f in CURSOR_CMDS.iterdir():
        if f.is_file() and f.name != "README.md":
            print(f"[-] Removing legacy: {f.name}")
            f.unlink()
            
    # 2. Sync new high-density manifests
    for f in AI_CMDS.iterdir():
        if f.is_file() and f.suffix == ".md":
            print(f"[+] Syncing OMEGA-Tier manifest: {f.name}")
            shutil.copy(str(f), str(CURSOR_CMDS / f.name))

if __name__ == "__main__":
    update_cursor_commands()
