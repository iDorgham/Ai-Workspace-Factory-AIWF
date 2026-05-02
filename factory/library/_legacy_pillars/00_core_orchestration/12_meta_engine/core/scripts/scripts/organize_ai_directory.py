#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

AI_ROOT = Path("/Users/Dorgham/Documents/Work/Devleopment/AIWF/.ai")

MOVES = {
    "agents": [
        "agents.md",
        "brainstorm-agent.md",
        "master-guide.md",
        "sub-agent-contracts.json"
    ],
    "commands": [
        "commands.md",
    ],
    "governance": [
        "access-rules.md",
        "data-ownership.md",
        "data-ownership-multi-tool.md",
        "versioning.md",
        "error-recovery.md"
    ],
    "logs/ledgers": [
        "distribution_manifest.jsonl",
        "evolution_ledger.jsonl",
        "financial_ledger.jsonl",
        "governance_ledger.jsonl",
        "intelligence_ledger.jsonl",
        "resilience_ledger.jsonl",
        "security_risk_registry.jsonl"
    ],
    "skills": [
        "skill-integration.md",
        "skill-integration-map.json"
    ],
    "registry": [
        "tool-registry.json"
    ]
}

def organize():
    print(f"Organizing {AI_ROOT}...")
    for target_dir, files in MOVES.items():
        dest_path = AI_ROOT / target_dir
        dest_path.mkdir(parents=True, exist_ok=True)
        
        for filename in files:
            src_file = AI_ROOT / filename
            if src_file.exists():
                print(f"[*] Moving {filename} -> {target_dir}/")
                shutil.move(str(src_file), str(dest_path / filename))
            else:
                print(f"[!] File not found: {filename}")

if __name__ == "__main__":
    organize()
