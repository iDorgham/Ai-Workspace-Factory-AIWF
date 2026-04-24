#!/usr/bin/env python3
"""
Workspace path integrity scanner.

Checks:
1) Python string-literal file paths point to existing files.
2) Markdown/TXT concrete path references point to existing files.

Outputs JSON report to .ai/logs/path-integrity-report.json.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

_scripts = Path(__file__).resolve().parent
_lib = _scripts / "lib"
for p in [str(_scripts), str(_lib)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from paths import REPO_ROOT  # noqa: E402

ROOT = REPO_ROOT
REPORT_PATH = ROOT / ".ai" / "logs" / "path-integrity-report.json"
SUMMARY_PATH = ROOT / ".ai" / "logs" / "path-integrity-summary.md"

DOC_EXTENSIONS = {".md", ".txt"}
PY_EXTENSIONS = {".py"}
PATH_LIKE_RE = re.compile(r"[A-Za-z0-9._-]+/[A-Za-z0-9._/\-\[\]]+")
PY_STRING_RE = re.compile(r"[\"']([^\"']+)[\"']")

# Allow placeholders / examples that are intentionally non-concrete.
PLACEHOLDER_PATTERNS = [
    r"\[[A-Za-z0-9_-]+\]",
    r"-\[[A-Za-z0-9_-]+\](?:\.[A-Za-z0-9]+)?$",
    r"/\[[A-Za-z0-9_-]+\](?:\.[A-Za-z0-9]+)?$",
    r"-$",
    r"_$",
    r"\[slug\]",
    r"\[name\]",
    r"\[topic\]",
    r"\[campaign\]",
    r"\[feedback\]",
    r"\[source\]",
    r"\*",
    r"^\.\.\.$",
    r"^/.*",  # slash commands
    r"^\.ai/scripts/test-$",
    r"^scripts/test-$",
]

CANONICAL_TOP_LEVEL = {
    ".ai",
    ".cursor",
    ".antigravity",
    "content",
    "archive",
    "CLAUDE.md",
    "AGENTS.md",
}


@dataclass(frozen=True)
class Finding:
    file: str
    reference: str
    category: str


def _is_placeholder(token: str) -> bool:
    return any(re.search(pattern, token) for pattern in PLACEHOLDER_PATTERNS)


def _normalize_token(token: str) -> str:
    return token.strip().strip("`'\".,;:(){}<>")


def _is_concrete_candidate(token: str) -> bool:
    if not token:
        return False
    if token.startswith(("http://", "https://", "mailto:", "#")):
        return False
    if _is_placeholder(token):
        return False
    if "/" not in token:
        return False
    first = token.split("/", 1)[0]
    if token.startswith(("./", "../")):
        return True
    return first in CANONICAL_TOP_LEVEL


def _is_under_dot_ai_logs(file_path: Path) -> bool:
    """Skip generated audit/log artifacts (path fragments inside JSON/JSONL create noise and self-churn)."""
    try:
        rel = file_path.resolve().relative_to(ROOT.resolve())
    except ValueError:
        return False
    return len(rel.parts) >= 2 and rel.parts[0] == ".ai" and rel.parts[1] == "logs"


def _exists(reference: str, source_file: Path) -> bool:
    candidate = Path(reference)
    if candidate.is_absolute():
        return candidate.exists()
    rel_exists = (source_file.parent / candidate).exists()
    root_exists = (ROOT / candidate).exists()
    return rel_exists or root_exists


def scan_python_paths() -> tuple[list[Finding], list[Finding]]:
    broken: list[Finding] = []
    ignored: list[Finding] = []
    for file_path in ROOT.rglob("*.py"):
        if ".venv" in file_path.parts:
            continue
        if _is_under_dot_ai_logs(file_path):
            continue
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        for raw in PY_STRING_RE.findall(text):
            token = _normalize_token(raw)
            if _is_placeholder(token):
                ignored.append(Finding(str(file_path.relative_to(ROOT)), token, "placeholder"))
                continue
            if not _is_concrete_candidate(token):
                continue
            if not _exists(token, file_path):
                broken.append(Finding(str(file_path.relative_to(ROOT)), token, "python_literal"))
    return broken, ignored


def scan_doc_paths() -> tuple[list[Finding], list[Finding]]:
    broken: list[Finding] = []
    ignored: list[Finding] = []
    doc_files = [p for p in ROOT.rglob("*") if p.is_file() and p.suffix in DOC_EXTENSIONS]
    for file_path in doc_files:
        if _is_under_dot_ai_logs(file_path):
            continue
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        for raw in PATH_LIKE_RE.findall(text):
            token = _normalize_token(raw)
            if _is_placeholder(token):
                ignored.append(Finding(str(file_path.relative_to(ROOT)), token, "placeholder"))
                continue
            if not _is_concrete_candidate(token):
                continue
            if not _exists(token, file_path):
                broken.append(Finding(str(file_path.relative_to(ROOT)), token, "doc_path"))
    return broken, ignored


def _write_summary_md(report: dict[str, object]) -> None:
    """Human-readable summary; must be written after REPORT_PATH so mtime stays >= JSON."""
    summary = report["summary"]  # type: ignore[assignment]
    assert isinstance(summary, dict)
    py_b = int(summary.get("python_broken", 0))
    doc_b = int(summary.get("doc_broken", 0))
    tot = int(summary.get("total_broken", 0))
    ign = int(summary.get("ignored_placeholders", 0))
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    py_status = "pass" if py_b == 0 else "fail"
    doc_status = "pass" if doc_b == 0 else "fail"
    tot_status = "pass" if tot == 0 else "fail"
    body = f"""# Path Integrity Summary

Last run: {stamp} (from `audit_path_integrity.py`)

## Validation Results
- Python literal file-path references: {py_status} (`python_broken = {py_b}`)
- Documentation path scan: {doc_status} (`doc_broken = {doc_b}`)
- Total broken references: {tot_status} (`total_broken = {tot}`)
- Ignored placeholder references: `ignored_placeholders = {ign}`
- Machine-readable source: `.ai/logs/path-integrity-report.json`

## Status
- Path integrity is currently {"clean" if tot == 0 else "not clean — see report JSON"}.
- Summary is regenerated after each audit (canonical logs live under `.ai/logs/`).

## Notes
- Placeholder-heavy references are intentionally ignored by scanner rules.
- Files under `.ai/logs/` are excluded from path scans so generated reports and JSONL lines do not create self-referential findings.
- Continue using `.ai/scripts/audit_path_integrity.py` before releasing structural changes.
"""
    SUMMARY_PATH.write_text(body, encoding="utf-8")


def _unique(findings: list[Finding]) -> list[Finding]:
    seen: set[tuple[str, str, str]] = set()
    uniq: list[Finding] = []
    for finding in findings:
        key = (finding.file, finding.reference, finding.category)
        if key in seen:
            continue
        seen.add(key)
        uniq.append(finding)
    return uniq


def main() -> int:
    py_broken, py_ignored = scan_python_paths()
    doc_broken, doc_ignored = scan_doc_paths()

    py_broken = _unique(py_broken)
    py_ignored = _unique(py_ignored)
    doc_broken = _unique(doc_broken)
    doc_ignored = _unique(doc_ignored)

    report = {
        "summary": {
            "python_broken": len(py_broken),
            "doc_broken": len(doc_broken),
            "ignored_placeholders": len(py_ignored) + len(doc_ignored),
            "total_broken": len(py_broken) + len(doc_broken),
        },
        "python_broken": [finding.__dict__ for finding in py_broken],
        "doc_broken": [finding.__dict__ for finding in doc_broken],
        "ignored": [finding.__dict__ for finding in (py_ignored + doc_ignored)],
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    _write_summary_md(report)

    print(json.dumps(report["summary"], indent=2))
    return 1 if report["summary"]["total_broken"] > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
