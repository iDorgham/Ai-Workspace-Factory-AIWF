#!/usr/bin/env python3
import os
from pathlib import Path

AI_DIR = Path("/Users/Dorgham/Documents/Work/Devleopment/AIWF/.ai/commands")
AG_DIR = Path("/Users/Dorgham/Documents/Work/Devleopment/AIWF/.antigravity/commands")

DEV_COMMANDS = {
    "do": {
        "desc": "Execute industrial tasks with multi-agent orchestration",
        "agent": "swarm_router_v3"
    },
    "plan": {
        "desc": "Discovery, blueprinting, and SDD phase management",
        "agent": "factory_orchestrator"
    },
    "dev": {
        "desc": "Implementation, testing, and automated remediation",
        "agent": "factory_orchestrator"
    },
    "create": {
        "desc": "High-fidelity asset and content materialization",
        "agent": "library_curator"
    },
    "git": {
        "desc": "Silent versioning, releases, and distribution",
        "agent": "registry_guardian"
    }
}

TEMPLATE = """---
type: dev-command
tier: OMEGA
version: 19.0.0
compliance: Law 151/2020
traceability: ISO-8601 Certified
---

# `/{cmd}`

## 📋 Purpose
{desc}

## 🚀 Usage
`/{cmd} [subcommand] [args] [flags]`

## 🛡️ Sovereign Protocol
- **Agent**: {agent}
- **Gate**: Omega Gate v2
- **Traceability**: Appends Reasoning Hash to .ai/logs/factory.jsonl
"""

def create_dev_commands(directory):
    print(f"Creating dev commands in {directory}...")
    for cmd, info in DEV_COMMANDS.items():
        fname = f"{cmd}.md"
        content = TEMPLATE.format(cmd=cmd, desc=info["desc"], agent=info["agent"])
        (directory / fname).write_text(content)

def main():
    create_dev_commands(AI_DIR)
    create_dev_commands(AG_DIR)
    print("Developer command suite industrialization complete.")

if __name__ == "__main__":
    main()
