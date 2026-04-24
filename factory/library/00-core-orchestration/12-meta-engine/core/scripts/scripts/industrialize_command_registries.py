#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

AI_DIR = Path("/Users/Dorgham/Documents/Work/Devleopment/AIWF/.ai/commands")
AG_DIR = Path("/Users/Dorgham/Documents/Work/Devleopment/AIWF/.antigravity/commands")

FACTORY_SUB = {
    "start": "Begin new project + gather requirements & discovery",
    "profile": "List/show workspace composition templates",
    "build": "Assemble project structure from template",
    "make": "Materialize full workspace in workspaces/<client>/",
    "test": "Verify structure, contracts, compliance, health",
    "check": "Compare workspace vs manifest, detect drift",
    "sync": "Aggregate global workspace state & P2P sync",
    "assign": "Route task to specialized swarm agent",
    "suggest": "AI-driven optimization recommendations",
    "repair": "Self-heal indexes, schemas, core scripts",
    "help": "Context-aware teaching assistant for /factory",
    "status": "Real-time workspace health & phase tracking"
}

LIBRARY_SUB = {
    "create": "Guided generation of agents, skills, rules, commands",
    "scan": "Deep inspection for drift, conflicts, outdated schemas",
    "test": "Validate components against contracts & sovereignty",
    "fix": "Auto-remediate scan failures, patch manifests",
    "improve": "Optimize components for perf, clarity, compliance",
    "agent": "Manage agent lifecycle (register, bind, retire, list)",
    "skill": "Manage skill lifecycle (catalog, version, link, archive)",
    "rule": "Manage factory rules & policy enforcement",
    "profile": "Manage library/workspace profiles",
    "maintain": "Background upkeep (index, cache, registry, storage)",
    "report": "Generate audit, compliance, health, usage reports",
    "help": "Context-aware teaching assistant for /library"
}

TEMPLATE = """---
type: command-registry
tier: OMEGA
version: 19.0.0
compliance: Law 151/2020
traceability: ISO-8601 Certified
---

# `/{cmd} {sub}`

## 📋 Purpose
{desc}

## 🚀 Usage
`/{cmd} {sub} [args] [flags]`

## 🛡️ Sovereign Protocol
- **Agent**: {agent}
- **Gate**: Omega Gate v2
- **Traceability**: Appends Reasoning Hash to .ai/logs/factory.jsonl
"""

def cleanup(directory):
    print(f"Cleaning up {directory}...")
    for item in directory.iterdir():
        if item.is_file() and item.name != ".DS_Store" and item.name != "README.md":
            item.unlink()

def create_commands(directory):
    print(f"Creating commands in {directory}...")
    for sub, desc in FACTORY_SUB.items():
        fname = f"factory-{sub}.md"
        content = TEMPLATE.format(cmd="factory", sub=sub, desc=desc, agent="factory_orchestrator")
        (directory / fname).write_text(content)
        
    for sub, desc in LIBRARY_SUB.items():
        fname = f"library-{sub}.md"
        agent = "library_curator" if sub != "agent" and sub != "rule" and sub != "maintain" else "registry_guardian"
        content = TEMPLATE.format(cmd="library", sub=sub, desc=desc, agent=agent)
        (directory / fname).write_text(content)

def main():
    # Cleanup
    cleanup(AI_DIR)
    cleanup(AG_DIR)
    
    # Create
    create_commands(AI_DIR)
    create_commands(AG_DIR)
    
    print("Command registry industrialization complete.")

if __name__ == "__main__":
    main()
