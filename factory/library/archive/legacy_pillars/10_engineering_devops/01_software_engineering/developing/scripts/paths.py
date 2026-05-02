"""Canonical repo root and per-project content paths for `.ai/scripts/` tooling."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def find_repo_root() -> Path:
    """Resolve AIWF repo root for scripts that live under factory/library/... (CI may omit .ai/memory)."""
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        marker = parent / ".ai" / "memory" / "state.json"
        if marker.is_file():
            return parent
        if (parent / ".git").is_dir() or (parent / ".git").is_file():
            return parent
    raise FileNotFoundError("Could not locate repo root (no .ai/memory/state.json and no .git ancestor)")


REPO_ROOT: Path = find_repo_root()


def load_state() -> dict[str, Any]:
    p = REPO_ROOT / ".ai" / "memory" / "state.json"
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def active_project(default: str = "sovereign") -> str:
    st = load_state()
    v = st.get("active_project")
    if isinstance(v, str) and v.strip():
        return v.strip()
    return default


def project_content_root(project: str | None = None) -> Path:
    return REPO_ROOT / "content" / (project or active_project())


def project_reference_dir(project: str | None = None) -> Path:
    return project_content_root(project) / "reference"


def project_scraped_dir(project: str | None = None) -> Path:
    return project_content_root(project) / "scraped"


def project_outputs_dir(project: str | None = None) -> Path:
    return project_content_root(project) / "outputs"


def project_comparisons_dir(project: str | None = None) -> Path:
    return project_content_root(project) / "comparisons"


def workspace_docs_dir() -> Path:
    return REPO_ROOT / ".ai" / "workspace"


def scripts_dir() -> Path:
    return REPO_ROOT / ".ai" / "scripts"


def templates_dir() -> Path:
    return REPO_ROOT / ".ai" / "templates"


def logs_dir() -> Path:
    return REPO_ROOT / ".ai" / "logs"


def tests_data_dir() -> Path:
    return workspace_docs_dir() / "08-testing" / "tests"
