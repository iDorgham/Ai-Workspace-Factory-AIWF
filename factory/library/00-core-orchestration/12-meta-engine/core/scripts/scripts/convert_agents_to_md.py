#!/usr/bin/env python3
import json
import os
from pathlib import Path

SPECIALIZED_DIR = Path("/Users/Dorgham/Documents/Work/Devleopment/AIWF/.ai/agents/specialized")

MD_TEMPLATE = """# 🛠️ AGENT: {name} (v19.0.0 OMEGA)
**Role:** {role}
**Tier:** T1 (Specialized Sub-Agent)
**Governance:** Law 151/2020 Compliant

---

## 🎯 MISSION
{mission}

## 📋 RESPONSIBILITIES
{responsibilities}

## 🛡️ SOVEREIGN PROTOCOLS
- **Traceability**: All actions logged with Reasoning Hashes.
- **Residency**: Operates strictly within assigned geospatial boundaries.
- **Contract**: Bound by sub-agent-contracts.json.

---
*Governor: Dorgham | Registry: .ai/agents/specialized/{fname}*
"""

def convert_dir(directory):
    print(f"[*] Processing directory: {directory}")
    for f in directory.iterdir():
        if f.is_file() and f.suffix == ".json" and f.name != "sub-agent-contracts.json":
            try:
                data = json.loads(f.read_text())
                name = data.get("name", f.stem.replace("-", " ").title())
                role = data.get("role", "Specialized Sub-Agent")
                mission = data.get("mission", "To assist in specialized industrial tasks.")
                resps = data.get("responsibilities", [])
                if isinstance(resps, list):
                    resps_str = "\n".join([f"- {r}" for r in resps])
                else:
                    resps_str = f"- {resps}"
                
                new_fname = f.stem.replace("-", "_") + ".md"
                # Adjust relative path in footer if in subagent subdir
                rel_path = "subagents/" + new_fname if directory.name == "subagents" else new_fname
                
                content = MD_TEMPLATE.format(
                    name=name.upper(),
                    role=role,
                    mission=mission,
                    responsibilities=resps_str,
                    fname=rel_path
                )
                
                (directory / new_fname).write_text(content)
                print(f"[+] Created: {new_fname}")
                f.unlink()
            except Exception as e:
                print(f"[!] Error processing {f.name}: {e}")

def main():
    convert_dir(SPECIALIZED_DIR)
    if (SPECIALIZED_DIR / "subagents").exists():
        convert_dir(SPECIALIZED_DIR / "subagents")

if __name__ == "__main__":
    main()
