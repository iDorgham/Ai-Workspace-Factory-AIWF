import os
from pathlib import Path

TARGET_DIR = Path("/Users/Dorgham/Documents/Work/Devleopment/Sovereign/Sovereign Workspace Factory/factory/library/11-industry-verticals")

def get_skill_density(path):
    skills_path = path / "skills"
    if not skills_path.exists(): return 0
    files = list(skills_path.glob("*.md"))
    if not files: return 0
    return sum(f.stat().st_size for f in files) / len(files)

def main():
    report = ["# 🏭 Industry Maturity & Intelligence Boost Report\n"]
    report.append("| Industry | Skill Density | Status | Action Required |")
    report.append("|---|---|---|---|")
    
    verticals = [d for d in TARGET_DIR.iterdir() if d.is_dir() and d.name != "meta-ops"]
    
    for v in verticals:
        density = get_skill_density(v)
        if density == 0:
            status = "🚨 LEGACY (Tier 1)"
            action = "Full skill hydration required."
        elif density < 1500:
            status = "🟡 OPERATIONAL (Tier 2)"
            action = "Enhance with Omega-tier playbooks."
        else:
            status = "💎 OMEGA (Tier 3)"
            action = "Routine QA only."
        
        report.append(f"| `{v.name}` | {density:.0f} bytes | {status} | {action} |")

    out_path = TARGET_DIR.parent / "INDUSTRY_MATURITY_REPORT.md"
    out_path.write_text("\n".join(report))
    print(f"Maturity scan complete. Report written to {out_path}")

if __name__ == "__main__":
    main()
