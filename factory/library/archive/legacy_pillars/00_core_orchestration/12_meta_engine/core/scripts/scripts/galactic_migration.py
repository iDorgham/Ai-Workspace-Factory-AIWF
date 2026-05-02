#!/usr/bin/env python3
import os
import shutil
import json
from pathlib import Path

# Target directory
LIB_PATH = Path("/Users/Dorgham/Documents/Work/Devleopment/Sovereign/Sovereign Workspace Factory/factory/library")

# Asset types to migrate
ASSET_TYPES = ["agents", "skills", "commands", "templates", "scripts", "subagents", "subcommands"]

def migrate_assets():
    moved_count = 0
    # Walk through the current Asset-First top-level folders
    for asset_type in ASSET_TYPES:
        asset_root = LIB_PATH / asset_type
        if not asset_root.exists(): continue
        
        # Walk Cluster / Field
        # Structure is factory/library/agents/01-cyber/developing/slug/...
        for cluster in os.listdir(asset_root):
            cluster_path = asset_root / cluster
            if not cluster_path.is_dir() or cluster.startswith('.'): continue
            
            for field in os.listdir(cluster_path):
                field_path = cluster_path / field
                if not field_path.is_dir() or field.startswith('.'): continue
                
                # We have found a target field. 
                # New destination: factory/library/01-cyber/developing/agents/
                dest_root = LIB_PATH / cluster / field / asset_type
                os.makedirs(dest_root, exist_ok=True)
                
                # Move everything from field_path to dest_root
                for item in os.listdir(field_path):
                    src = field_path / item
                    dst = dest_root / item
                    
                    if dst.exists():
                        # If it exists, it might be a merge-able directory (common for Skills/Agents headers)
                        if src.is_dir():
                            for subitem in os.listdir(src):
                                shutil.move(str(src / subitem), str(dst / subitem))
                            shutil.rmtree(src)
                        else:
                            # Conflict (should not happen in a clean sync, but we handle)
                            print(f"Conflict: {dst} already exists. Skipping.")
                    else:
                        shutil.move(str(src), str(dst))
                    moved_count += 1
    
    return moved_count

def heal_metadata(version="3.3.1"):
    healed_count = 0
    # Search for all meta.json and md files in the NEW structure
    for root, dirs, files in os.walk(LIB_PATH):
        for file in files:
            fpath = Path(root) / file
            
            # Skip non-relevant folders
            if "_gen" in str(fpath): continue

            # 1. Handle JSON Metadata
            if file.endswith(".meta.json"):
                try:
                    with open(fpath, 'r') as f:
                        data = json.load(f)
                    
                    # Update Category based on its new path
                    # Path: .../library/03-creative/branding/agents/brand-strategist/AGENT.md.meta.json
                    parts = fpath.parts
                    # library is at index i
                    try:
                        idx = parts.index("library")
                        cluster = parts[idx+1]
                        field = parts[idx+2]
                        asset_type = parts[idx+3]
                        
                        data["category"] = f"{cluster}/{field}"
                        data["asset_type"] = asset_type
                        data["version"] = version # reset to 3.3.1
                        
                        # Fix ID (Remove legacy prefixes if any remain, and align to path)
                        data["id"] = "/".join(parts[idx+1:-1]) # relative to library
                        
                        with open(fpath, 'w') as f:
                            json.dump(data, f, indent=2)
                        healed_count += 1
                    except Exception as e:
                        print(f"Error healing metadata for {fpath}: {e}")
                except Exception as e:
                    print(f"Error reading {fpath}: {e}")

            # 2. Handle Markdown Versioning Reset
            elif file.endswith(".md"):
                try:
                    with open(fpath, 'r') as f:
                        lines = f.readlines()
                    
                    new_lines = []
                    updated = False
                    for line in lines:
                        if line.startswith("version:"):
                            new_lines.append(f"version: {version}\n")
                            updated = True
                        else:
                            # Special case: profiles often have "version": "..."
                            line = re.sub(r'"version": "[^"]+"', f'"version": "{version}"', line)
                            new_lines.append(line)
                    
                    if updated:
                        with open(fpath, 'w') as f:
                            f.writelines(new_lines)
                except:
                    pass
                    
    return healed_count

def cleanup_empty_dirs():
    # Remove the top-level asset folders now that they are empty
    for asset_type in ASSET_TYPES:
        asset_root = LIB_PATH / asset_type
        if asset_root.exists():
            try:
                shutil.rmtree(asset_root)
                print(f"Purged legacy top-level folder: {asset_type}")
            except Exception as e:
                print(f"Warning: Could not purge {asset_type} (not empty?): {e}")

if __name__ == "__main__":
    import re
    print("--- Starting Galactic Migration (V15.0.0) ---")
    moves = migrate_assets()
    print(f"Physically relocated {moves} asset clusters.")
    heals = heal_metadata("3.3.1")
    print(f"Healed metadata and reset versions to v3.3.1 for {heals} files.")
    cleanup_empty_dirs()
    print("--- Migration Complete ---")
