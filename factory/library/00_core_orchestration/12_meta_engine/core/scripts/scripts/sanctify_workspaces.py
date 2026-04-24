#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

WS_ROOT = Path("/Users/Dorgham/Documents/Work/Devleopment/AIWF/workspaces")

def cleanup():
    print("[*] Starting Workspace Sanctification...")
    
    # Ensure targets exist
    personal_dir = WS_ROOT / "personal"
    clients_dir = WS_ROOT / "clients"
    personal_dir.mkdir(exist_ok=True)
    clients_dir.mkdir(exist_ok=True)
    
    # 1. Move from 01-Personal
    p_old = WS_ROOT / "01-Personal"
    if p_old.exists():
        for item in p_old.iterdir():
            print(f"[*] Moving {item.name} to personal/")
            shutil.move(str(item), str(personal_dir / item.name))
        p_old.rmdir()
        
    # 2. Move from 02-Clients
    c_old = WS_ROOT / "02-Clients"
    if c_old.exists():
        for item in c_old.iterdir():
            print(f"[*] Moving {item.name} to clients/")
            shutil.move(str(item), str(clients_dir / item.name))
        c_old.rmdir()
        
    # 3. Delete unwanted
    unwanted = ["galaxy", "sovereign-web"]
    for d in unwanted:
        path = WS_ROOT / d
        if path.exists():
            print(f"[-] Deleting unwanted workspace: {d}")
            shutil.rmtree(path)
            
    print("[+] Workspace Sanctification Complete.")

if __name__ == "__main__":
    cleanup()
