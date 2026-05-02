#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Target directory
LIB_PATH = Path("/Users/Dorgham/Documents/Work/Devleopment/Sovereign/Sovereign Workspace Factory/factory/library/skills")

# Template sections to inject
INJECTION_CONTENT = """
## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.
"""

def inject_logic(fpath):
    with open(fpath, 'r') as f:
        content = f.read()
    
    # Only inject if not already present
    if "## 🛡️ Critical Failure Modes" not in content:
        # Find the end of the content or the last signature line
        if "---" in content:
            # Insert before the last horizontal rule if possible
            parts = content.rsplit("---", 1)
            new_content = parts[0] + INJECTION_CONTENT + "\n---\n" + parts[1]
        else:
            new_content = content + INJECTION_CONTENT
            
        with open(fpath, 'w') as f:
            f.write(new_content)
        return True
    return False

def main():
    count = 0
    for root, dirs, files in os.walk(LIB_PATH):
        for file in files:
            if file == "SKILL.md":
                fpath = Path(root) / file
                if inject_logic(fpath):
                    count += 1
                    print(f"Injected intelligence into {fpath.relative_to(LIB_PATH)}")
    
    print(f"--- Injection Complete: {count} skills updated ---")

if __name__ == "__main__":
    main()
