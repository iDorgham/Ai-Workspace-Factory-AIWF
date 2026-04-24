#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Target directory
LIB_PATH = Path("/Users/Dorgham/Documents/Work/Devleopment/Sovereign/Sovereign Workspace Factory/factory/library")

def repair_json_content(content):
    # Fix 1: Remove leading commas after { or [ (with any whitespace/newlines)
    content = re.sub(r'(\{|\[)\s*,', r'\1', content)
    
    # Fix 2: Remove trailing commas before } or ]
    content = re.sub(r',\s*(\}|\])', r'\1', content)
    
    # Fix 3: Remove double commas
    content = re.sub(r',\s*,', ',', content)
    
    return content

def main():
    count = 0
    for root, dirs, files in os.walk(LIB_PATH):
        for file in files:
            if file.endswith(".meta.json"):
                fpath = Path(root) / file
                try:
                    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    repaired = repair_json_content(content)
                    
                    if repaired != content:
                        with open(fpath, 'w', encoding='utf-8') as f:
                            f.write(repaired)
                        count += 1
                        print(f"Repaired JSON: {fpath.relative_to(LIB_PATH)}")
                except Exception as e:
                    print(f"Error repairing {fpath}: {e}")
                    
    print(f"--- JSON Repair Complete: {count} files fixed ---")

if __name__ == "__main__":
    main()
