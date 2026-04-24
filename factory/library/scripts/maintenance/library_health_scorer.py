#!/usr/bin/env python3
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIBRARY = ROOT / "factory/library"

def score_component(path: Path) -> int:
    score = 0
    if path.is_file():
        content = path.read_text()
        # Header checks
        if "# " in content: score += 20
        if "## " in content: score += 20
        if "> [!" in content: score += 10 # Alert blocks
        
        # Metadata checks
        meta = path.with_suffix(".meta.json")
        if meta.exists(): score += 30
        
        # Quality/Length check
        if len(content) > 1000: score += 20
    return min(100, score)

def main():
    report = {
        "version": "1.0.0",
        "timestamp": Path("/tmp").stat().st_atime, # Dummy for now or use datetime
        "departments": {}
    }
    
    import datetime
    report["timestamp"] = datetime.datetime.now().isoformat()
    
    for dept in sorted(LIBRARY.glob("[0-9][0-9]-*")):
        dept_name = dept.name
        report["departments"][dept_name] = {"score": 0, "components": []}
        dept_scores = []
        
        for comp in dept.rglob("*"):
            if comp.name in ["AGENT.md", "SKILL.md", "COMMANDS.md", "MANIFEST.json"]:
                score = score_component(comp)
                report["departments"][dept_name]["components"].append({
                    "name": comp.parent.name if comp.name != "MANIFEST.json" else comp.name,
                    "type": comp.name.replace(".md", ""),
                    "path": str(comp.relative_to(LIBRARY)),
                    "score": score
                })
                dept_scores.append(score)
        
        if dept_scores:
            report["departments"][dept_name]["score"] = sum(dept_scores) // len(dept_scores)

    output_path = ROOT / ".ai/memory/library-health-report.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"✅ Library Health Report generated: {output_path}")

if __name__ == "__main__":
    main()
