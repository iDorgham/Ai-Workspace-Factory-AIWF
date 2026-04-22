#!/usr/bin/env python3
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def extract_legacy_agent_ids(text: str):
    return re.findall(r"### `([a-z0-9-]+)`", text)


def read_yaml_frontmatter_id(path: Path):
    content = path.read_text()
    m = re.search(r"^---\n(.*?)\n---", content, flags=re.S)
    if not m:
        return None
    fm = m.group(1)
    id_match = re.search(r"^id:\s*([a-z0-9-]+)\s*$", fm, flags=re.M)
    return id_match.group(1) if id_match else None


def main():
    legacy_text = (ROOT / ".ai/agents.md").read_text()
    registry = json.loads((ROOT / ".ai/registry/agents.registry.json").read_text())["agents"]
    compat = json.loads((ROOT / ".ai/compat/agents.legacy-map.json").read_text())["legacy_section_to_agent_file"]

    legacy_ids = extract_legacy_agent_ids(legacy_text)
    registry_ids = {a["id"] for a in registry}

    report = {
        "summary": {
            "legacy_agents": len(legacy_ids),
            "registry_agents": len(registry),
            "checked": 0,
            "missing_in_registry": [],
            "missing_in_compat_map": [],
            "missing_file": [],
            "frontmatter_id_mismatch": []
        },
        "details": []
    }

    for aid in legacy_ids:
        if aid not in registry_ids:
            report["summary"]["missing_in_registry"].append(aid)
            continue

        rel_path = compat.get(aid)
        if not rel_path:
            report["summary"]["missing_in_compat_map"].append(aid)
            continue

        path = ROOT / rel_path
        if not path.exists():
            report["summary"]["missing_file"].append(str(path))
            continue

        fm_id = read_yaml_frontmatter_id(path)
        mismatch = fm_id != aid
        if mismatch:
            report["summary"]["frontmatter_id_mismatch"].append(
                {"agent": aid, "frontmatter_id": fm_id, "path": rel_path}
            )

        report["details"].append(
            {"agent": aid, "path": rel_path, "frontmatter_id": fm_id, "match": not mismatch}
        )
        report["summary"]["checked"] += 1

    out_path = ROOT / ".ai/migrations/agent-parity-report.json"
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n")

    print("agent_parity_check_complete")
    print(f"checked={report['summary']['checked']}")
    print(f"missing_in_registry={len(report['summary']['missing_in_registry'])}")
    print(f"missing_in_compat_map={len(report['summary']['missing_in_compat_map'])}")
    print(f"missing_file={len(report['summary']['missing_file'])}")
    print(f"frontmatter_id_mismatch={len(report['summary']['frontmatter_id_mismatch'])}")
    print(f"report={out_path}")


if __name__ == "__main__":
    main()
