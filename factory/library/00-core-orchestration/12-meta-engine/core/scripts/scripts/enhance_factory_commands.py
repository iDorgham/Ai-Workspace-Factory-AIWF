#!/usr/bin/env python3
import os
from pathlib import Path

COMMANDS_DIR = Path("/Users/Dorgham/Documents/Work/Devleopment/AIWF/.ai/commands")
FILES = [
    "factory-compose.md", "factory-diff.md", "factory-doctor.md",
    "factory-generate.md", "factory-help.md", "factory-intake.md",
    "factory-library-refresh.md", "factory-library-search.md",
    "factory-library-status.md", "factory-profile-list.md",
    "factory-profile-show.md", "factory-validate.md"
]

BOILERPLATE = """---
type: factory-command
tier: OMEGA
version: 19.0.0
compliance: Law 151/2020
traceability: ISO-8601 Certified
---

# {title}

## 📋 Technical Specification
{description}

## 🚀 Industrial Usage
`{syntax}`

## 🛡️ OMEGA-Tier Gating
- **Compliance**: Law 151/2020 (Egypt/MENA)
- **Isolation**: Level 4 Absolute Shard
- **Traceability**: Appends Reasoning Hash to `.ai/logs/factory.jsonl`

## 📝 Example
`{example}`
"""

def enhance():
    for filename in FILES:
        filepath = COMMANDS_DIR / filename
        if not filepath.exists():
            continue
            
        content = filepath.read_text()
        lines = content.split('\n')
        
        # Simple extraction
        title = lines[0].replace('# ', '').strip()
        syntax = ""
        example = ""
        purpose = ""
        
        for i, line in enumerate(lines):
            if "## Syntax" in line:
                syntax = lines[i+1].replace('`', '').strip()
            if "## Beginner Example" in line:
                example = lines[i+1].replace('`', '').strip()
            if "## Purpose" in line:
                purpose = lines[i+1].strip()
        
        new_content = BOILERPLATE.format(
            title=title,
            description=purpose,
            syntax=syntax,
            example=example
        )
        
        filepath.write_text(new_content)
        print(f"Enhanced {filename}")

if __name__ == "__main__":
    enhance()
