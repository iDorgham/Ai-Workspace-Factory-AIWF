import os
import re
from pathlib import Path

TARGET_DIR = Path("/Users/Dorgham/Documents/Work/Devleopment/Sovereign/Sovereign Workspace Factory/factory/library")

def main():
    referenced_agents = set()
    existing_agent_files = {} # name: path
    
    # 1. Find all existing agent files
    for r, d, f in os.walk(TARGET_DIR):
        if "agents" in Path(r).parts:
            for file in f:
                if file.endswith('.md'):
                    if file.upper() == "AGENT.MD":
                        name = Path(r).name.lower()
                    else:
                        name = file.replace('.md', '').lower()
                    existing_agent_files[name] = Path(r) / file

    # 2. Extract all references (@AgentName) from AGENT.md and SKILL.md
    # Also look at frontmatter 'subagents' or 'agents'
    ref_pattern = re.compile(r"@(\w+)")
    
    for r, d, f in os.walk(TARGET_DIR):
        for file in f:
            if file.endswith('.md'):
                path = Path(r) / file
                try:
                    content = path.read_text('utf-8')
                    # Find @mentions
                    matches = ref_pattern.findall(content)
                    for m in matches:
                        referenced_agents.add(m.lower())
                except:
                    pass

    # 3. Analyze the gap
    unique_refs = sorted(list(referenced_agents))
    defined_agents = set(existing_agent_files.keys())
    
    missing_agents = [r for r in unique_refs if r not in defined_agents]
    orphan_agents = [d for d in defined_agents if d not in referenced_agents]
    
    # Output the analysis
    print(f"Total Unique Sub-Agents Referenced: {len(unique_refs)}")
    print(f"Total Actual Agent Files Defined: {len(defined_agents)}")
    print(f"Gap (Referenced but NOT Defined): {len(missing_agents)}")
    print(f"Orphaned (Defined but NOT Referenced): {len(orphan_agents)}")
    
    print("\n--- SAMPLE OF MISSING AGENTS (TOP 20) ---")
    for m in missing_agents[:20]:
        # Heuristic for "Importance": If it appears many times
        count = 0
        for r, d, f in os.walk(TARGET_DIR):
            for file in f:
                if file.endswith('.md'):
                    try:
                        if f"@{m}" in (Path(r) / file).read_text('utf-8').lower():
                            count += 1
                    except: pass
        print(f"{m} (Referenced in {count} files)")

if __name__ == "__main__":
    main()
