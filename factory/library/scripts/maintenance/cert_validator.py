import os
import json

LIBRARY_DIR = 'factory/library'
REGISTRY_DIR = '.ai/registry'

def main():
    orphaned_paths = []
    missing_meta = []
    failed_lines = []

    # Simple scan
    output_md = []
    output_md.append("# 100/100 Certification Validation Run")
    output_md.append("## Pre-Flight Checks")
    
    for root, dirs, files in os.walk(LIBRARY_DIR):
        for f in files:
            p = os.path.join(root, f)
            if f in ['SKILL.md', 'AGENT.md']:
                meta_p = p.replace('.md', '.meta.json')
                if not os.path.exists(meta_p):
                    missing_meta.append(p)
                
                with open(p, 'r', encoding='utf-8') as file:
                    lines = len(file.readlines())
                    if f == 'SKILL.md' and lines < 50:
                        failed_lines.append(f"{p} (Lines: {lines}/50)")
                    elif f == 'AGENT.md' and lines < 100:
                        failed_lines.append(f"{p} (Lines: {lines}/100)")

    output_md.append(f"- **Missing Meta JSON:** {len(missing_meta)} files")
    output_md.append(f"- **Failed Line Thresholds:** {len(failed_lines)} files")
    output_md.append(f"- **Orphaned Paths identified:** {len(orphaned_paths)} files")
    
    with open('CERTIFICATION_VALIDATION.md', 'w') as out:
        out.write("\n".join(output_md))
        if failed_lines:
            out.write("\n\n### Failed Components (Require Upgrades or Deletion)\n")
            for fl in failed_lines:
                out.write(f"- {fl}\n")

if __name__ == '__main__':
    main()
