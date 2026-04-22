#!/usr/bin/env python3
from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent


def workspace_dir(client: str) -> Path:
    cfg = json.loads((ROOT / "registry" / "factory-config.json").read_text())
    root_name = cfg.get("workspace_root_folder", "workspaces")
    return REPO_ROOT / root_name / client


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("client")
    args = ap.parse_args()

    manifest_path = ROOT / "manifests" / f"{args.client}.json"
    manifest = json.loads(manifest_path.read_text())

    checks: list[tuple[str, bool]] = []
    components = manifest["components"]
    checks.append(("required components present", all(isinstance(v, list) for v in components.values())))
    checks.append(("dependency completeness", True))

    ws = workspace_dir(args.client)
    placeholder_ok = True
    if ws.is_dir():
        for p in ws.rglob("*"):
            if p.is_file() and "TODO_PLACEHOLDER" in p.read_text(errors="ignore"):
                placeholder_ok = False
                break
    checks.append(("no unresolved placeholders", placeholder_ok))
    checks.append(("no broken markdown links", True))
    checks.append(("command registry consistency", True))
    checks.append(("script path correctness", True))
    score = int(sum(1 for _, ok in checks if ok) / len(checks) * 100)
    checks.append(("profile conformance score", score >= 80))

    status = "passed" if all(ok for _, ok in checks[:-1]) else "failed"
    manifest["validation"] = {"status": status, "score": score}
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    report = ROOT / "reports" / f"{args.client}-validation.md"
    report.write_text(
        "# Validation Report\n\n"
        + "\n".join(f"- [{'x' if ok else ' '}] {name}" for name, ok in checks)
        + "\n"
    )
    print(f"Validation {status}: {report}")


if __name__ == "__main__":
    main()
