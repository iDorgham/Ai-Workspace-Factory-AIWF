#!/usr/bin/env python3
import os
from pathlib import Path

AI_DIR = Path("/Users/Dorgham/Documents/Work/Devleopment/AIWF/.ai/commands")
AG_DIR = Path("/Users/Dorgham/Documents/Work/Devleopment/AIWF/.antigravity/commands")

DEV_COMMAND_SETS = {
    "plan": {
        "desc": "Discovery, blueprinting, and SDD phase management",
        "agent": "factory_orchestrator",
        "subs": {
            "discovery": "Structured requirements interrogation",
            "blueprint": "Generate high-density SDD specs",
            "status": "Phase progress & compliance check",
            "adr": "Generate Architecture Decision Records",
            "review": "Stakeholder consensus & approval"
        }
    },
    "create": {
        "desc": "High-fidelity asset and content materialization",
        "agent": "library_curator",
        "subs": {
            "content": "Scaffold/assemble discovered content",
            "image": "Generate industrial-grade visual assets",
            "page": "Materialize UI components & pages",
            "spec": "Generate spec.yaml & contracts",
            "docs": "Auto-generate API & system documentation"
        }
    },
    "dev": {
        "desc": "Implementation, testing, and automated remediation",
        "agent": "factory_orchestrator",
        "subs": {
            "init": "Env setup & CI/CD scaffolding",
            "implement": "Code generation governed by specs",
            "test": "Execute industrial test suites",
            "fix": "Recursive remediation of drift & failures",
            "build": "Production bundle & verification"
        }
    },
    "git": {
        "desc": "Silent versioning, releases, and distribution",
        "agent": "registry_guardian",
        "subs": {
            "auto": "Silent versioning & traceability",
            "release": "Sovereign handover & version increment",
            "review": "Autonomous PR & code audit",
            "rollback": "Recovery with compliance preservation",
            "deploy": "Shard distribution to cloud endpoints"
        }
    },
    "do": {
        "desc": "Execute industrial tasks with multi-agent orchestration",
        "agent": "swarm_router_v3",
        "subs": {
            "task": "Execute atomic industrial task",
            "chain": "Execute deterministic multi-command chain",
            "assign": "Delegate task to specialized agent",
            "monitor": "Real-time task execution tracking",
            "report": "Post-execution completion audit"
        }
    }
}

TEMPLATE = """---
type: command-registry
tier: OMEGA
version: 19.0.0
compliance: Law 151/2020
traceability: ISO-8601 Certified
---

# `/{cmd}`

{desc}

## 📋 Subcommands

| Subcommand | Purpose | Usage |
|------------|---------|-------|
{sub_rows}

## 🛡️ Sovereign Protocol
- **Agent**: {agent}
- **Gate**: Omega Gate v2
- **Traceability**: Appends Reasoning Hash to .ai/logs/factory.jsonl
- **Compliance**: Egyptian Law 151/2020 Certified
"""

def create_expanded_dev_commands(directory):
    print(f"Expanding dev commands in {directory}...")
    for cmd, info in DEV_COMMAND_SETS.items():
        fname = f"{cmd}.md"
        sub_rows = ""
        for sub, sub_desc in info["subs"].items():
            sub_rows += f"| `{sub}` | {sub_desc} | `/{cmd} {sub}` |\n"
            
        content = TEMPLATE.format(
            cmd=cmd, 
            desc=info["desc"], 
            agent=info["agent"],
            sub_rows=sub_rows.strip()
        )
        (directory / fname).write_text(content)

def main():
    create_expanded_dev_commands(AI_DIR)
    create_expanded_dev_commands(AG_DIR)
    print("Developer command suite expansion complete.")

if __name__ == "__main__":
    main()
