#!/usr/bin/env python3
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_json(path: Path):
    return json.loads(path.read_text())


def main():
    legacy = load_json(ROOT / ".ai/sub-agent-contracts.json")
    registry = load_json(ROOT / ".ai/registry/subagents.registry.json")["subagents"]
    compat = load_json(ROOT / ".ai/compat/subagents.legacy-map.json")["legacy_key_to_subagent_file"]

    report = {
        "summary": {
            "legacy_subagents": 0,
            "registry_subagents": len(registry),
            "checked": 0,
            "missing_in_registry": [],
            "missing_file": [],
            "field_mismatch": []
        },
        "details": []
    }

    registry_ids = {item["id"] for item in registry}
    legacy_ids = [k for k in legacy.keys() if k != "_meta"]
    report["summary"]["legacy_subagents"] = len(legacy_ids)

    for sid in legacy_ids:
        if sid not in registry_ids:
            report["summary"]["missing_in_registry"].append(sid)
            continue

        rel_path = compat.get(sid)
        if not rel_path:
            report["summary"]["missing_file"].append(sid)
            continue

        path = ROOT / rel_path
        if not path.exists():
            report["summary"]["missing_file"].append(str(path))
            continue

        split = load_json(path)
        expected = legacy[sid]

        missing_keys = [k for k in expected.keys() if k not in split]
        if split.get("id") != sid:
            missing_keys.append("id")

        if missing_keys:
            report["summary"]["field_mismatch"].append({"id": sid, "missing_keys": missing_keys})

        report["details"].append({
            "id": sid,
            "path": rel_path,
            "missing_keys": missing_keys
        })
        report["summary"]["checked"] += 1

    out_path = ROOT / ".ai/migrations/semantic-drift-report.json"
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n")

    print("semantic_drift_check_complete")
    print(f"checked={report['summary']['checked']}")
    print(f"missing_in_registry={len(report['summary']['missing_in_registry'])}")
    print(f"missing_file={len(report['summary']['missing_file'])}")
    print(f"field_mismatch={len(report['summary']['field_mismatch'])}")
    print(f"report={out_path}")


if __name__ == "__main__":
    main()
