#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Target directory
FACTORY_PATH = Path("/Users/Dorgham/Documents/Work/Devleopment/Sovereign/Sovereign Workspace Factory/factory")

def ultimate_scrub(fpath):
    try:
        # Skip binary files/pycache
        if "__pycache__" in str(fpath) or fpath.suffix in [".pyc", ".png", ".jpg", ".ico"]:
            return False
            
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # 1. Broad case-insensitive replacement for standalone 'Sovereign'
        # We replace with 'Sovereign' for general mentions
        # We use 'sovereign' for technical slugs
        
        # Specific high-risk replacements first
        new_content = re.sub(r'sovereign-default', 'sovereign-default', content)
        new_content = re.sub(r'sovereign-production', 'sovereign-production', new_content)
        new_content = re.sub(r'sovereign-uploads', 'sovereign-uploads', new_content)
        new_content = re.sub(r'sovereign-api', 'sovereign-api', new_content)
        new_content = re.sub(r'sovereign-web', 'sovereign-web', new_content)
        new_content = re.sub(r'Sovereign Monorepo', 'Sovereign Monorepo', new_content)
        new_content = re.sub(r'Sovereign CI', 'Sovereign CI', new_content)
        
        # Case-specific replacements
        new_content = re.sub(r'\bGALERIA\b', 'Sovereign', new_content)
        new_content = re.sub(r'\bsovereign\b', 'sovereign', new_content)
        
        # Clean up any leftover sovereign: prefixes if any were missed
        new_content = re.sub(r'sovereign:', '', new_content)

        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
            
    except Exception as e:
        print(f"Error processing {fpath}: {e}")
        
    return False

def main():
    count = 0
    for root, dirs, files in os.walk(FACTORY_PATH):
        for file in files:
            fpath = Path(root) / file
            if ultimate_scrub(fpath):
                count += 1
                print(f"Scrubbed: {fpath.relative_to(FACTORY_PATH)}")
    
    print(f"--- TOTAL PURGE COMPLETE: {count} files sanitized ---")

if __name__ == "__main__":
    main()
