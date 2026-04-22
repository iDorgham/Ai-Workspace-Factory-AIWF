#!/usr/bin/env python3
import os
import json
from pathlib import Path

# Target directory
LIB_PATH = Path("/Users/Dorgham/Documents/Work/Devleopment/Sovereign/Sovereign Workspace Factory/factory/library")

def scrub_meta(fpath):
    updated = False
    try:
        with open(fpath, 'r') as f:
            data = json.load(f)
        
        # 1. Scrub IDs
        if "id" in data and data["id"].startswith(""):
            data["id"] = data["id"].replace("", "")
            updated = True
        
        # 2. Scrub Sources
        if "source" in data and data["source"] == :
            del data["source"]
            updated = True
        
        if "source_path" in data and "Sovereign Workspace" in data["source_path"]:
            del data["source_path"]
            updated = True
            
        # 3. Scrub Tags
        if "tags" in data and  in data["tags"]:
            data["tags"] = [t for t in data["tags"] if t != ]
            updated = True
            
        # 4. Scrub Mentions
        if "mentions" in data:
            new_mentions = []
            for m in data["mentions"]:
                if isinstance(m, dict):
                    if m.get("source") == : continue
                    if "Sovereign" in m.get("source_path", ""): continue
                new_mentions.append(m)
            if len(new_mentions) != len(data["mentions"]):
                data["mentions"] = new_mentions
                updated = True

        if updated:
            with open(fpath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
            
    except Exception as e:
        print(f"Error processing {fpath}: {e}")
        
    return False

def main():
    count = 0
    for root, dirs, files in os.walk(LIB_PATH):
        for file in files:
            if file.endswith(".meta.json"):
                fpath = Path(root) / file
                if scrub_meta(fpath):
                    count += 1
                    print(f"Scrubbed metadata: {fpath.relative_to(LIB_PATH)}")
    
    print(f"--- Metadata Purge Complete: {count} files sanitized ---")

if __name__ == "__main__":
    main()
