#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Target directory
FACTORY_PATH = Path("/Users/Dorgham/Documents/Work/Devleopment/Sovereign/Sovereign Workspace Factory/factory")

def scrub_content(fpath):
    try:
        with open(fpath, 'r') as f:
            content = f.read()
        
        # 1. Remove Swarm references
        new_content = re.sub(r'Part of Sovereign Agent Swarm', '', content, flags=re.IGNORECASE)
        new_content = re.sub(r'Part of the Sovereign legacy suite', '', new_content, flags=re.IGNORECASE)
        
        # 2. General replacement (Sovereign -> Sovereign)
        # We target specific common phrases to avoid breaking code if 'sovereign' was a variable (unlikely here)
        new_content = re.sub(r'Sovereign Workspace', 'Sovereign Workspace Factory', new_content)
        new_content = re.sub(r'agent for Sovereign', 'agent for Sovereign', new_content)
        new_content = re.sub(r'within Sovereign', 'within Sovereign', new_content)
        
        # 3. Clean up double lines if any were created by the removals
        new_content = re.sub(r'\n\n\n+', '\n\n', new_content)

        if new_content != content:
            with open(fpath, 'w') as f:
                f.write(new_content)
            return True
            
    except Exception as e:
        print(f"Error processing {fpath}: {e}")
        
    return False

def main():
    count = 0
    # Include both .md and .json files for broad coverage
    for root, dirs, files in os.walk(FACTORY_PATH):
        for file in files:
            if file.endswith((".md", ".json")):
                fpath = Path(root) / file
                if scrub_content(fpath):
                    count += 1
                    print(f"Sanitized content: {fpath.relative_to(FACTORY_PATH)}")
    
    print(f"--- Content Purge Complete: {count} files sanitized ---")

if __name__ == "__main__":
    main()
