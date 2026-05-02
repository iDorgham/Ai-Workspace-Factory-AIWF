import os
import json
from pathlib import Path
from datetime import datetime

TARGET_DIR = Path("/Users/Dorgham/Documents/Work/Devleopment/Sovereign/Sovereign Workspace Factory/factory/library")
DOCS_DIR = Path("/Users/Dorgham/Documents/Work/Devleopment/Sovereign/Sovereign Workspace Factory/docs/qwen")

def parse_markdown_metadata(content):
    """
    Unified parser for AGENT.MD and SKILL.MD metadata.
    Supported formats: YAML frontmatter (---) or Key-Value block.
    """
    meta = {}
    
    # Handle YAML frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            header = parts[1]
            for line in header.strip().split('\n'):
                if ':' in line:
                    k, v = line.split(':', 1)
                    meta[k.strip().lower()] = v.strip().replace('[', '').replace(']', '').replace('"', '').replace("'", "")
            return meta
            
    # Handle inline metadata (e.g., > **Governance:** ...)
    for line in content.split('\n'):
        if line.startswith('> **') or line.startswith('**'):
            # Extract key/value from bold markers
            parts = line.replace('>', '').replace('**', '').split(':', 1)
            if len(parts) == 2:
                meta[parts[0].strip().lower()] = parts[1].strip()
                
    return meta

def main():
    library_index = {
        "agents": [],
        "engines": []
    }
    
    for r, d, f in os.walk(TARGET_DIR):
        rel_path = Path(r).relative_to(TARGET_DIR)
        dept = rel_path.parts[0] if rel_path.parts else "Core"
        
        for file in f:
            filepath = Path(r) / file
            
            # --- AGENT INDEXING ---
            if file.upper() == "AGENT.MD":
                try:
                    content = filepath.read_text('utf-8')
                    meta = parse_markdown_metadata(content)
                    library_index["agents"].append({
                        "name": meta.get('agent', Path(r).name),
                        "role": meta.get('role', 'Specialized Worker'),
                        "dept": dept,
                        "domains": meta.get('domains', 'Regional'),
                        "id": meta.get('id', 'N/A'),
                        "path": str(filepath.parent).replace(str(TARGET_DIR.parent.parent), '')
                    })
                except: continue

            # --- ENGINE INDEXING (SKILLS WITH LOGIC) ---
            if file.upper() == "SKILL.MD":
                # Check if this skill has a core.py logic engine
                has_logic = (Path(r) / "core.py").exists()
                if has_logic:
                    try:
                        content = filepath.read_text('utf-8')
                        meta = parse_markdown_metadata(content)
                        library_index["engines"].append({
                            "name": Path(r).name,
                            "dept": dept,
                            "type": meta.get('type', 'Specialized Logic'),
                            "governance": meta.get('governance', '00-Standard'),
                            "status": "OMEGA-TIER" if "OMEGA" in content.upper() else "STRUCTURAL",
                            "path": str(filepath.parent).replace(str(TARGET_DIR.parent.parent), '')
                        })
                    except: continue

    # Generat the Master Discovery Dictionary (Markdown)
    report = [
        "# 🧠 Sovereign Factory: Master Discovery Dictionary",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n",
        "This document integrates all 322 structural nodes and identifies the active OMEGA-tier logic engines.\n",
        "## 🧩 Active Logic Engines (OMEGA Tier)",
        "| Engine | Dept | Type | Status | Path |",
        "|---|---|---|---|---|",
    ]
    
    # Sort and add engines
    for engine in sorted(library_index["engines"], key=lambda x: x['dept']):
        status_icon = "💎" if engine["status"] == "OMEGA-TIER" else "🏗️"
        report.append(f"| **{engine['name']}** | {engine['dept']} | {engine['type']} | {status_icon} {engine['status']} | `{engine['path']}` |")

    report.append("\n## 👥 Agentic Workforce Directory")
    report.append("| Agent | Role | Dept | Domains | ID |")
    report.append("|---|---|---|---|---|")
    
    # Sort and add agents
    for agent in sorted(library_index["agents"], key=lambda x: x['name']):
        report.append(f"| **{agent['name']}** | {agent['role']} | {agent['dept']} | `{agent['domains']}` | `{agent['id']}` |")

    # Output to multiple locations for redundancy
    out_path_docs = DOCS_DIR / "FACTORY_MASTER_DICTIONARY.md"
    out_path_lib = TARGET_DIR / "DICTIONARY.md"
    
    final_content = "\n".join(report)
    out_path_docs.write_text(final_content)
    out_path_lib.write_text(final_content)
    
    print(f"Master Dictionary generated at {out_path_docs}")
    print(f"Master Dictionary (Mirrored) generated at {out_path_lib}")

if __name__ == "__main__":
    main()
