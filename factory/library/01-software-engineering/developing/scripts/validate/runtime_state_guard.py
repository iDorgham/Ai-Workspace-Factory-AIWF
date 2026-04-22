#!/usr/bin/env python3
"""
Validate runtime-state.md (YAML inside first ```yaml ... ``` fence).

Discovers optional repo-root sos/runtime-state.md and every
.ai/plans/active/features/*/sos/runtime-state.md. Bootstrap copy: .ai/templates/sos-root/

CI / pre-commit / /runtime sync --ci — stdlib + optional PyYAML.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any


def find_repo_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / ".ai").is_dir():
            return p
    return start


def extract_yaml_block(text: str) -> str | None:
    m = re.search(r"```yaml\s*\n(.*?)```", text, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else None


def parse_yaml(blob: str) -> dict[str, Any]:
    try:
        import yaml  # type: ignore

        out = yaml.safe_load(blob)
        return out if isinstance(out, dict) else {}
    except Exception:
        return parse_yaml_fallback(blob)


def parse_yaml_fallback(blob: str) -> dict[str, Any]:
    """Enough for drift / flags / flat gate_status."""
    data: dict[str, Any] = {}
    gate: dict[str, str] = {}
    in_gates = False
    for line in blob.splitlines():
        ls = line.strip()
        if not ls or ls.startswith("#"):
            continue
        if ls.startswith("gate_status:"):
            in_gates = True
            data["gate_status"] = gate
            continue
        if in_gates:
            m = re.match(r"^([\w:-]+):\s*(\S+)", ls)
            if m and line.startswith("  ") and not line.startswith("    "):
                gate[m.group(1)] = m.group(2).strip().strip('"').strip("'")
                continue
            if not line.startswith(" ") or re.match(r"^[a-z_]+:", ls):
                in_gates = False
        m = re.match(r"^([a-zA-Z0-9_]+):\s*(.+)$", ls)
        if m and not in_gates:
            k, v = m.group(1), m.group(2).strip().strip('"').strip("'")
            if k != "gate_status":
                data[k] = v
    if gate:
        data["gate_status"] = gate
    return data


def drift_score(data: dict[str, Any]) -> int:
    raw = data.get("drift_score_last", 0)
    try:
        return int(float(raw))
    except (TypeError, ValueError):
        return 0


def truthy(v: Any) -> bool:
    return str(v).lower() in ("true", "1", "yes")


def gates_all_passed(gs: Any) -> bool:
    if not isinstance(gs, dict) or not gs:
        return True
    for _k, v in gs.items():
        if str(v).lower() != "passed":
            return False
    return True


def discover_paths(root: Path, explicit: list[str]) -> list[Path]:
    if explicit:
        return [Path(p) for p in explicit]
    found = {*root.glob("sos/runtime-state.md"), *root.glob(".ai/plans/active/features/*/sos/runtime-state.md")}
    return sorted(p for p in found if p.is_file())


def emit_summary(paths: list[Path]) -> str:
    lines = [
        "## Runtime state snapshot (CI)",
        "",
        "| Path | status | drift_last | trace |",
        "|------|--------|------------|-------|",
    ]
    for p in paths:
        text = p.read_text(encoding="utf-8")
        blob = extract_yaml_block(text)
        data = parse_yaml(blob) if blob else {}
        rel = p.as_posix()
        d = drift_score(data)
        st = data.get("status", "?")
        tid = data.get("trace_id_last", "")
        lines.append(f"| `{rel}` | {st} | {d} | {tid} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Runtime state guard (filesystem only)")
    ap.add_argument("--ci", action="store_true", help="Strict PR checks when ci_validate or pr_gate_strict")
    ap.add_argument("--emit-summary", action="store_true", help="Markdown table for GITHUB_STEP_SUMMARY")
    ap.add_argument("--critical-only", action="store_true", help="Block only drift>=2 or failed-critical")
    ap.add_argument("paths", nargs="*", help="Optional explicit paths")
    args = ap.parse_args()

    root = find_repo_root(Path.cwd())
    paths = discover_paths(root, args.paths)

    if args.emit_summary:
        sys.stdout.write(emit_summary(paths))
        return 0

    if not paths:
        return 0

    failed = False
    for p in paths:
        text = p.read_text(encoding="utf-8")
        blob = extract_yaml_block(text)
        if not blob:
            continue
        data = parse_yaml(blob)

        if args.critical_only:
            d = drift_score(data)
            st = str(data.get("status", "")).lower()
            if d >= 2 or st == "failed-critical":
                sys.stderr.write(f"[runtime-guard] BLOCK {p}: drift={d} status={data.get('status')}\n")
                failed = True
            continue

        if args.ci:
            if not (truthy(data.get("ci_validate")) or truthy(data.get("pr_gate_strict"))):
                continue
            d = drift_score(data)
            if d > 0:
                sys.stderr.write(f"[runtime-guard] FAIL {p}: drift_score_last={d} (must be 0)\n")
                failed = True
            if not gates_all_passed(data.get("gate_status")):
                sys.stderr.write(f"[runtime-guard] FAIL {p}: gate_status not all passed\n")
                failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
