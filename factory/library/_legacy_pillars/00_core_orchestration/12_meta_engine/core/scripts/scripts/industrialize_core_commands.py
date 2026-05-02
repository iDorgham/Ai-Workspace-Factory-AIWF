#!/usr/bin/env python3
import os
from pathlib import Path

AI_DIR = Path("/Users/Dorgham/Documents/Work/Devleopment/AIWF/.ai/commands")
AG_DIR = Path("/Users/Dorgham/Documents/Work/Devleopment/AIWF/.antigravity/commands")

CORE_COMMAND_SETS = {
    "guide": {
        "desc": "Intelligence, strategy, and autonomous ecosystem evolution",
        "agent": "teaching_agent",
        "subs": {
            "brainstorm": "Multi-agent consensus for architecture & strategy",
            "learn": "Recursive skill extraction and friction-to-skill conversion",
            "heal": "Autonomous structural remediation & predictive monitoring",
            "chaos": "Stress testing, boundary validation, and resilience injection",
            "dashboard": "Real-time KPI/health UI and project roster"
        }
    },
    "audit": {
        "desc": "Quality, security, and industrial-grade observability",
        "agent": "healing_bot_v2",
        "subs": {
            "health": "Industrial health scoring (99.0+) & structural drift",
            "content": "High-fidelity content validation & strategic alignment",
            "security": "SAST, DAST, secrets scanning, and SBOM generation",
            "logs": "Log aggregation, distributed tracing, and perf profiling",
            "seo": "Technical SEO audit and meta-strategy verification"
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

def create_core_commands(directory):
    print(f"Creating core commands in {directory}...")
    for cmd, info in CORE_COMMAND_SETS.items():
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
    create_core_commands(AI_DIR)
    create_core_commands(AG_DIR)
    print("Core command suite industrialization complete.")

if __name__ == "__main__":
    main()
