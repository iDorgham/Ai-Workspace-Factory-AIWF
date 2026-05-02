#!/usr/bin/env python3
"""
Reconcile workspace artifacts into factory/library.

Scans .antigravity, .claude, .cursor, .ai for skills/agents/subagents/commands/templates/scripts
and backfills missing artifacts into factory/library while deduplicating by logical key.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
LIB_ROOT = ROOT / "factory/library"
REPORT_PATH = ROOT / ".ai/logs/library_reconcile_report.json"

SOURCE_DIRS = [".antigravity", ".claude", ".cursor", ".ai"]
ARTIFACT_DIRS = {
    "skills": LIB_ROOT / "skills",
    "agents": LIB_ROOT / "agents",
    "subagents": LIB_ROOT / "subagents",
    "commands": LIB_ROOT / "commands",
    "templates": LIB_ROOT / "templates",
    "scripts": LIB_ROOT / "scripts",
}

SCRIPT_EXT = {".py", ".sh", ".js", ".ts", ".tsx", ".bash", ".zsh"}
TEXT_EXT = {".md", ".markdown", ".json", ".yaml", ".yml", ".toml", ".txt"} | SCRIPT_EXT


@dataclass
class Candidate:
    src: Path
    artifact: str
    key: str
    content: str
    source_root: str

    @property
    def digest(self) -> str:
        return hashlib.sha256(self.content.encode("utf-8")).hexdigest()


def classify(path: Path, source_root: Path) -> str | None:
    rel_parts = [p.lower() for p in path.relative_to(source_root).parts]
    name = path.name.lower()
    suffix = path.suffix.lower()

    if name in {"skill.md", "skill.md.meta.json", "skill.md.meta.yaml", "skill.md.meta.yml"}:
        return "skills"
    if name == "skill.md" or "skills" in rel_parts:
        return "skills"
    if name == "agent.md" or "agents" in rel_parts:
        if "subagents" in rel_parts:
            return "subagents"
        return "agents"
    if "subagents" in rel_parts:
        return "subagents"
    if "commands" in rel_parts or name.startswith("commands"):
        return "commands"
    if "templates" in rel_parts:
        return "templates"
    if "scripts" in rel_parts or suffix in SCRIPT_EXT:
        return "scripts"
    return None


def build_key(path: Path, artifact: str) -> str:
    name = path.stem.lower()
    if artifact in {"skills", "agents", "subagents"} and path.name.lower() in {"skill.md", "agent.md"}:
        name = path.parent.name.lower()
    return re.sub(r"[^a-z0-9]+", "-", name).strip("-")


def score(path: Path, artifact: str, content: str) -> int:
    s = 0
    rel = path.relative_to(ROOT) if path.is_absolute() else path
    rel_s = str(rel)
    if rel_s.startswith("factory/library/"):
        s += 100
    if "workspace_imports" in rel_s:
        s -= 20
    if content.lstrip().startswith("---"):
        s += 10
    if artifact == "skills" and path.name.lower() == "skill.md":
        s += 10
    if artifact in {"agents", "subagents"} and path.name.lower() == "agent.md":
        s += 10
    s += min(len(content) // 1000, 20)
    return s


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def collect_existing() -> dict[str, dict[str, list[tuple[Path, str]]]]:
    out: dict[str, dict[str, list[tuple[Path, str]]]] = {k: {} for k in ARTIFACT_DIRS}
    for artifact, base in ARTIFACT_DIRS.items():
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if not p.is_file() or p.suffix.lower() not in TEXT_EXT:
                continue
            txt = read_text(p)
            key = build_key(p, artifact)
            out[artifact].setdefault(key, []).append((p, txt))
    return out


def collect_incoming() -> list[Candidate]:
    candidates: list[Candidate] = []
    for src_name in SOURCE_DIRS:
        src_root = ROOT / src_name
        if not src_root.exists():
            continue
        for p in src_root.rglob("*"):
            if not p.is_file() or p.suffix.lower() not in TEXT_EXT:
                continue
            artifact = classify(p, src_root)
            if not artifact:
                continue
            txt = read_text(p)
            key = build_key(p, artifact)
            candidates.append(Candidate(src=p, artifact=artifact, key=key, content=txt, source_root=src_name))
    return candidates


def target_import_path(c: Candidate) -> Path:
    src_root = ROOT / c.source_root
    rel = c.src.relative_to(src_root)
    return ARTIFACT_DIRS[c.artifact] / "workspace_imports" / c.source_root.strip(".") / rel


def main() -> None:
    for p in ARTIFACT_DIRS.values():
        p.mkdir(parents=True, exist_ok=True)

    existing = collect_existing()
    incoming = collect_incoming()
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "scanned_sources": SOURCE_DIRS,
        "incoming_candidates": len(incoming),
        "added": 0,
        "skipped_duplicate": 0,
        "replaced_weaker_import": 0,
        "details": [],
    }

    for c in incoming:
        bucket = existing[c.artifact].get(c.key, [])
        incoming_score = score(c.src, c.artifact, c.content)
        incoming_digest = hashlib.sha256(c.content.encode("utf-8")).hexdigest()

        if not bucket:
            dst = target_import_path(c)
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(c.content, encoding="utf-8")
            existing[c.artifact].setdefault(c.key, []).append((dst, c.content))
            report["added"] += 1
            report["details"].append(
                {"action": "added", "artifact": c.artifact, "key": c.key, "src": str(c.src.relative_to(ROOT)), "dst": str(dst.relative_to(ROOT))}
            )
            continue

        best_path, best_content = max(bucket, key=lambda t: score(t[0], c.artifact, t[1]))
        best_digest = hashlib.sha256(best_content.encode("utf-8")).hexdigest()
        best_score = score(best_path, c.artifact, best_content)

        if incoming_digest == best_digest:
            report["skipped_duplicate"] += 1
            continue

        # Replace only weaker imported copies, never canonical curated files.
        if "workspace_imports" in str(best_path.relative_to(ROOT)) and incoming_score > best_score:
            best_path.write_text(c.content, encoding="utf-8")
            report["replaced_weaker_import"] += 1
            report["details"].append(
                {
                    "action": "replaced_weaker_import",
                    "artifact": c.artifact,
                    "key": c.key,
                    "src": str(c.src.relative_to(ROOT)),
                    "dst": str(best_path.relative_to(ROOT)),
                }
            )
        else:
            report["skipped_duplicate"] += 1

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"incoming={report['incoming_candidates']}")
    print(f"added={report['added']}")
    print(f"skipped_duplicate={report['skipped_duplicate']}")
    print(f"replaced_weaker_import={report['replaced_weaker_import']}")
    print(f"report={REPORT_PATH}")


if __name__ == "__main__":
    main()
