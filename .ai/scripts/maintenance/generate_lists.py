import json
from pathlib import Path


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "AGENTS.md").is_file():
            return parent
    return here.parents[3]


LIBRARY_DIR = "factory/library"

# Phase 1 & 2 Generate
rm_commands = []
mv_commands = []
root = _repo_root()
audit_path = root / "docs" / "reports" / "audit_report.json"
with open(audit_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Sort dead weights, pick the shallowest 33 to kill
deletes = sorted([x for x in data["dead_weights"]], key=lambda k: k["lines"])[:33]
for d in deletes:
    # include meta.json
    path = d["path"]
    rm_commands.append(f"rm '{path}'")
    rm_commands.append(f"rm '{path.replace('.md', '.meta.json')}'")

out_path = root / "docs" / "reports" / "cleanup_lists.txt"
out_path.parent.mkdir(parents=True, exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    f.write("# Phase 1: RM Commands\n")
    f.write("\n".join(rm_commands))
    f.write("\n\n# Phase 2: MV Commands\n")
    # For taxonomies... we can just assume moving seo into 07-visibility-optimization/seo if not already there
    f.write(
        "mv 'factory/library/archive/legacy_pillars/02-web-platforms/seo' "
        "'factory/library/07-visibility-optimization/seo-technical' 2>/dev/null || true\n"
    )
