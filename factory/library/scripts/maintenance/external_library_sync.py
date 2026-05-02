#!/usr/bin/env python3
"""
External Library Sync
=====================

Manifest-driven ingestion and smart merge for external agents/subagents/design sources.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
MANIFEST_PATH = ROOT / "factory/library/registry/external_sources.registry.json"
REPORT_JSON_PATH = ROOT / "factory/library/reports/external_library_merge_report.json"
REPORT_MD_PATH = ROOT / "factory/library/reports/external_library_merge_report.md"
TMP_ROOT = Path("/tmp/aiwf_external_sources")

TIER_RANK = {"community": 1, "curated": 2, "official": 3, "local": 4}


@dataclass
class Candidate:
    key: str
    category: str
    relative_name: str
    content: str
    source_id: str
    source_url: str
    tier: str
    license_detected: str

    @property
    def digest(self) -> str:
        return hashlib.sha256(self.content.encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def run(command: list[str], cwd: Path | None = None) -> str:
    out = subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True)
    return out.stdout.strip()


def github_clone_or_update(url: str, branch: str, source_id: str) -> Path:
    repo_dir = TMP_ROOT / source_id
    if repo_dir.exists():
        run(["git", "fetch", "--depth", "1", "origin", branch or "main"], cwd=repo_dir)
        run(["git", "checkout", branch or "main"], cwd=repo_dir)
        run(["git", "reset", "--hard", f"origin/{branch or 'main'}"], cwd=repo_dir)
        return repo_dir

    TMP_ROOT.mkdir(parents=True, exist_ok=True)
    run(["git", "clone", "--depth", "1", "--branch", branch or "main", url, str(repo_dir)])
    return repo_dir


def detect_license(repo_dir: Path) -> str:
    for file_name in ("LICENSE", "LICENSE.md", "LICENSE.txt"):
        p = repo_dir / file_name
        if p.exists():
            first = p.read_text(encoding="utf-8", errors="ignore").splitlines()[0].strip()
            if "MIT" in first.upper():
                return "MIT"
            if "APACHE" in first.upper():
                return "Apache-2.0"
            if "BSD" in first.upper():
                return "BSD"
            return first or "unknown"
    return "unknown"


def extract_frontmatter_value(content: str, key: str) -> str | None:
    m = re.search(rf"^{re.escape(key)}:\s*\"?([^\n\"]+)\"?\s*$", content, flags=re.MULTILINE)
    return m.group(1).strip() if m else None


def collect_local_subagents(target_root: Path) -> list[Candidate]:
    local: list[Candidate] = []
    cats = target_root / "categories"
    if not cats.exists():
        return local
    for cat in sorted([p for p in cats.iterdir() if p.is_dir()]):
        for md in sorted(cat.glob("*.md")):
            if md.name.lower() == "readme.md":
                continue
            content = md.read_text(encoding="utf-8", errors="ignore")
            key = f"{cat.name}/{md.stem}"
            local.append(
                Candidate(
                    key=key,
                    category=cat.name,
                    relative_name=md.name,
                    content=content,
                    source_id="local-existing",
                    source_url="local",
                    tier="local",
                    license_detected="n/a",
                )
            )
    return local


def collect_local_design(target_root: Path) -> list[Candidate]:
    local: list[Candidate] = []
    if not target_root.exists():
        return local
    for provider in sorted([p for p in target_root.iterdir() if p.is_dir()]):
        p = provider / "design.md"
        if not p.exists():
            continue
        local.append(
            Candidate(
                key=provider.name,
                category="design",
                relative_name="design.md",
                content=p.read_text(encoding="utf-8", errors="ignore"),
                source_id="local-existing",
                source_url="local",
                tier="local",
                license_detected="n/a",
            )
        )
    return local


def collect_subagent_candidates(repo_dir: Path, source: dict[str, Any], license_detected: str) -> list[Candidate]:
    out: list[Candidate] = []
    categories_dir = repo_dir / "categories"
    if not categories_dir.exists():
        return out
    for cat in sorted([p for p in categories_dir.iterdir() if p.is_dir()]):
        for md in sorted(cat.glob("*.md")):
            if md.name.lower() == "readme.md":
                continue
            content = md.read_text(encoding="utf-8", errors="ignore")
            key = f"{cat.name}/{md.stem}"
            out.append(
                Candidate(
                    key=key,
                    category=cat.name,
                    relative_name=md.name,
                    content=content,
                    source_id=source["id"],
                    source_url=source["url"],
                    tier=source["tier"],
                    license_detected=license_detected,
                )
            )
    return out


def collect_design_candidates(repo_dir: Path, source: dict[str, Any], license_detected: str) -> list[Candidate]:
    out: list[Candidate] = []
    design_root = repo_dir / "design-md"
    if not design_root.exists():
        return out
    for provider in sorted([p for p in design_root.iterdir() if p.is_dir()]):
        candidate_file = provider / "design.md"
        if not candidate_file.exists():
            candidate_file = provider / "README.md"
        if not candidate_file.exists():
            continue
        content = candidate_file.read_text(encoding="utf-8", errors="ignore")
        out.append(
            Candidate(
                key=provider.name,
                category="design",
                relative_name="design.md",
                content=content,
                source_id=source["id"],
                source_url=source["url"],
                tier=source["tier"],
                license_detected=license_detected,
            )
        )
    return out


def select_best(candidates: list[Candidate]) -> tuple[dict[str, Candidate], dict[str, list[dict[str, Any]]]]:
    grouped: dict[str, list[Candidate]] = {}
    for c in candidates:
        grouped.setdefault(c.key, []).append(c)

    selected: dict[str, Candidate] = {}
    variants: dict[str, list[dict[str, Any]]] = {}

    for key, group in grouped.items():
        ordered = sorted(group, key=lambda x: (TIER_RANK.get(x.tier, 0), len(x.content)), reverse=True)
        best = ordered[0]
        selected[key] = best
        variants[key] = [
            {
                "source_id": c.source_id,
                "tier": c.tier,
                "digest": c.digest,
                "license": c.license_detected,
                "selected": c is best,
            }
            for c in ordered
        ]
    return selected, variants


def write_subagents_target(
    target_root: Path, selected: dict[str, Candidate], variants: dict[str, list[dict[str, Any]]]
) -> dict[str, Any]:
    categories_dir = target_root / "categories"
    if categories_dir.exists():
        shutil.rmtree(categories_dir)
    categories_dir.mkdir(parents=True, exist_ok=True)

    catalog_entries: list[dict[str, Any]] = []
    by_cat: dict[str, list[tuple[str, Candidate]]] = {}
    for key, cand in selected.items():
        by_cat.setdefault(cand.category, []).append((key, cand))

    for cat, items in sorted(by_cat.items()):
        cat_dir = categories_dir / cat
        cat_dir.mkdir(parents=True, exist_ok=True)
        subagents: list[dict[str, Any]] = []
        for key, cand in sorted(items, key=lambda x: x[1].relative_name.lower()):
            out_file = cat_dir / cand.relative_name
            out_file.write_text(cand.content, encoding="utf-8")
            name = extract_frontmatter_value(cand.content, "name") or out_file.stem
            desc = extract_frontmatter_value(cand.content, "description") or ""
            subagents.append(
                {
                    "id": out_file.stem,
                    "name": name,
                    "description": desc,
                    "file": f"{cat}/{out_file.name}",
                    "provenance": variants[key],
                }
            )

        catalog_entries.append(
            {
                "category": cat,
                "count": len(subagents),
                "subagents": subagents,
            }
        )

    catalog = {
        "generated_at": now_iso(),
        "type": "subagents_catalog",
        "categories": catalog_entries,
    }
    write_json(target_root / "catalog.json", catalog)
    (target_root / "README.md").write_text(
        "# External Subagents Catalog\n\nGenerated by `external_library_sync.py`.\n", encoding="utf-8"
    )
    return {"count": sum(c["count"] for c in catalog_entries), "categories": len(catalog_entries)}


def write_design_target(
    target_root: Path, selected: dict[str, Candidate], variants: dict[str, list[dict[str, Any]]]
) -> dict[str, Any]:
    for child in list(target_root.iterdir()) if target_root.exists() else []:
        if child.is_dir():
            shutil.rmtree(child)
    target_root.mkdir(parents=True, exist_ok=True)

    providers: list[dict[str, Any]] = []
    for provider, cand in sorted(selected.items()):
        out_dir = target_root / provider
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "design.md").write_text(cand.content, encoding="utf-8")
        providers.append({"provider": provider, "provenance": variants[provider]})

    catalog = {"generated_at": now_iso(), "type": "design_catalog", "providers": providers}
    write_json(target_root / "catalog.json", catalog)
    lines = [
        "# Design Catalog",
        "",
        "Generated by `external_library_sync.py`.",
        "",
        "Available providers:",
    ] + [f"- {p['provider']}" for p in providers]
    (target_root / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"count": len(providers)}


def sync_templates_for_target(target: Path) -> list[str]:
    rel = target.relative_to(ROOT / "factory/library")
    synced: list[str] = []
    # Canonical targets live under factory/library/…; mirror only into library/templates and .ai/templates.
    mirrors = [
        ROOT / "factory/library/templates" / rel,
        ROOT / ".ai/templates" / rel,
    ]
    for dst in mirrors:
        if dst.exists():
            shutil.rmtree(dst)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(target, dst)
        synced.append(str(dst.relative_to(ROOT)))
    return synced


def ensure_no_duplicate_keys(selected: dict[str, Candidate]) -> None:
    keys = list(selected.keys())
    if len(keys) != len(set(keys)):
        raise RuntimeError("Duplicate keys detected after merge selection.")


def main() -> None:
    manifest = load_json(MANIFEST_PATH)
    allowlist = set(manifest.get("license_allowlist", []))
    enabled_sources = [s for s in manifest.get("sources", []) if s.get("enabled")]

    report: dict[str, Any] = {
        "timestamp": now_iso(),
        "manifest": str(MANIFEST_PATH.relative_to(ROOT)),
        "imported_sources": [],
        "targets": {},
        "skipped_sources": [],
        "template_sync": [],
        "validation": {"duplicate_keys": "pass", "license_policy": "pass"},
    }

    by_target_kind: dict[tuple[str, str], list[Candidate]] = {}

    for source in enabled_sources:
        kind = source["kind"]
        target = ROOT / source["target"]
        source_record = {
            "id": source["id"],
            "kind": kind,
            "url": source["url"],
            "target": source["target"],
            "tier": source["tier"],
            "status": "processed",
            "detected_license": "unknown",
            "items": 0,
        }

        if source["url"].startswith("https://github.com/"):
            repo_dir = github_clone_or_update(source["url"], source.get("branch", "main"), source["id"])
            detected_license = detect_license(repo_dir)
            source_record["detected_license"] = detected_license
            if detected_license not in allowlist:
                source_record["status"] = "skipped_license_policy"
                report["validation"]["license_policy"] = "warn"
                report["skipped_sources"].append(source_record)
                continue

            if kind == "subagents_categories":
                candidates = collect_subagent_candidates(repo_dir, source, detected_license)
            elif kind == "design_catalog":
                candidates = collect_design_candidates(repo_dir, source, detected_license)
            else:
                candidates = []
        else:
            # Non-git indexes are tracked in manifest only for now.
            source_record["status"] = "tracked_index_only"
            report["imported_sources"].append(source_record)
            continue

        source_record["items"] = len(candidates)
        report["imported_sources"].append(source_record)
        by_target_kind.setdefault((str(target), kind), []).extend(candidates)

    for (target_str, kind), candidates in by_target_kind.items():
        target = Path(target_str)
        # Merge with existing local library artifacts as highest precedence.
        if kind == "subagents_categories":
            candidates.extend(collect_local_subagents(target))
        elif kind == "design_catalog":
            candidates.extend(collect_local_design(target))

        selected, variants = select_best(candidates)
        ensure_no_duplicate_keys(selected)

        if kind == "subagents_categories":
            summary = write_subagents_target(target, selected, variants)
        elif kind == "design_catalog":
            summary = write_design_target(target, selected, variants)
        else:
            continue

        sync_paths = sync_templates_for_target(target)
        report["template_sync"].extend(sync_paths)
        report["targets"][str(target.relative_to(ROOT))] = {
            "kind": kind,
            "selected_count": len(selected),
            "summary": summary,
        }

    write_json(REPORT_JSON_PATH, report)
    md_lines = [
        "# External Library Merge Report",
        "",
        f"- Timestamp: {report['timestamp']}",
        f"- Manifest: `{report['manifest']}`",
        "",
        "## Source Results",
    ]
    for src in report["imported_sources"]:
        md_lines.append(
            f"- `{src['id']}` ({src['kind']}): status={src['status']}, license={src['detected_license']}, items={src['items']}"
        )
    if report["skipped_sources"]:
        md_lines.append("")
        md_lines.append("## Skipped Sources")
        for src in report["skipped_sources"]:
            md_lines.append(f"- `{src['id']}` skipped by license policy ({src['detected_license']})")
    md_lines.append("")
    md_lines.append("## Target Results")
    for target_name, details in sorted(report["targets"].items()):
        md_lines.append(f"- `{target_name}`: selected={details['selected_count']}, kind={details['kind']}")
    md_lines.append("")
    md_lines.append("## Template Sync")
    for p in sorted(set(report["template_sync"])):
        md_lines.append(f"- `{p}`")
    REPORT_MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_MD_PATH.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(f"Report written: {REPORT_JSON_PATH}")
    print(f"Report written: {REPORT_MD_PATH}")


if __name__ == "__main__":
    main()
