#!/usr/bin/env python3
"""
Import ``skills/*`` from https://github.com/nexu-io/open-design (Apache-2.0)
into ``factory/library/skills/nexu_open_design/<pack>/``.

Ensures each pack has ``skill.md`` (copy from ``SKILL.md`` when needed) so
``rebuild_canonical_registries.py`` discovers entries on case-sensitive filesystems.

Run from repo root:
  python3 factory/library/scripts/maintenance/import_nexu_open_design_skills.py
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in here.parents:
        if (p / "AGENTS.md").is_file():
            return p
    return here.parents[4]


ROOT = repo_root()
TMP = Path("/tmp/aiwf_nexu_open_design_skills")
REPO = "https://github.com/nexu-io/open-design.git"
DST_ROOT = ROOT / "factory" / "library" / "skills" / "nexu_open_design"


def clone_or_update() -> None:
    if TMP.exists():
        subprocess.run(
            ["git", "-C", str(TMP), "fetch", "--depth", "1", "origin", "main"],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(TMP), "checkout", "main"],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(TMP), "reset", "--hard", "origin/main"],
            check=True,
        )
    else:
        TMP.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "clone", "--depth", "1", "--branch", "main", REPO, str(TMP)],
            check=True,
        )


def main() -> None:
    clone_or_update()
    src_skills = TMP / "skills"
    if not src_skills.is_dir():
        raise SystemExit(f"missing {src_skills}")
    DST_ROOT.mkdir(parents=True, exist_ok=True)
    imported = 0
    for child in sorted(src_skills.iterdir()):
        if not child.is_dir():
            continue
        if not (child / "SKILL.md").is_file() and not (child / "skill.md").is_file():
            continue
        dest = DST_ROOT / child.name
        shutil.copytree(child, dest, dirs_exist_ok=True)
        if not (dest / "skill.md").is_file() and (dest / "SKILL.md").is_file():
            shutil.copy2(dest / "SKILL.md", dest / "skill.md")
        imported += 1
    print(f"imported {imported} skill packs -> {DST_ROOT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
