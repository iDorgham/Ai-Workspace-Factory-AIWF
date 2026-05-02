#!/usr/bin/env python3
"""
Import skills and agents from local shallow Git clones into factory/library.

Deduplication: skills are keyed by the parent folder name of SKILL.md when that
name is not in GENERIC_NAMES; otherwise by ``<source>__<relpath>`` under the
source root. When the same key appears from multiple sources, the higher
PRIORITY wins; on equal priority, the larger SKILL.md body wins.

Sources (see docs/files.md):
  - anthropics/skills
  - anthropics/claude-code (plugins/*/skills/*/SKILL.md)
  - obra/superpowers
  - K-Dense-AI/claude-scientific-skills/scientific-skills/*
  - alirezarezvani/claude-skills (excludes .gemini, .git)
  - wshobson/agents (plugins/*/skills and plugins/*/agents)

Usage:
  python3 factory/scripts/core/import_github_skills_library.py \\
    --clone-root /tmp/aiwf_github_imports
"""

from __future__ import annotations

import argparse
import json
import shutil
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

GENERIC_NAMES = frozenset(
    {
        "core",
        "status",
        "init",
        "review",
        "run",
        "tests",
        "test",
        "scripts",
        "helpers",
        "utils",
        "lib",
        "docs",
        "templates",
        "src",
        "examples",
    }
)

# Higher number wins on duplicate keys across sources.
PRIORITY = {
    "anthropics_official": 100,
    "anthropics_claude_code": 90,
    "obra_superpowers": 80,
    "k_dense_scientific": 70,
    "alirezarezvani": 60,
    "wshobson_agents": 50,
}


@dataclass
class SkillCandidate:
    source: str
    priority: int
    skill_root: Path  # directory containing SKILL.md
    skill_md: Path
    merge_key: str


def _skill_md_size(p: Path) -> int:
    try:
        return p.stat().st_size
    except OSError:
        return 0


def _merge_key(source: str, skill_parent: Path, anchor: Path) -> str:
    base = skill_parent.name.lower()
    if base in GENERIC_NAMES:
        try:
            rel = skill_parent.relative_to(anchor)
        except ValueError:
            rel = Path(source) / skill_parent.name
        return f"{source}__{str(rel).replace(chr(92), '/').replace('/', '__').lower()}"
    return base


def _ignore_git(dirpath: str, names: list[str]) -> set[str]:
    return {n for n in names if n == ".git"}


def discover_anthropics_official(clone_root: Path) -> list[SkillCandidate]:
    root = clone_root / "anthropics_skills" / "skills"
    if not root.is_dir():
        return []
    out: list[SkillCandidate] = []
    for md in root.rglob("SKILL.md"):
        parent = md.parent
        key = _merge_key("anthropics_official", parent, root)
        out.append(
            SkillCandidate(
                "anthropics_official",
                PRIORITY["anthropics_official"],
                parent,
                md,
                key,
            )
        )
    return out


def discover_claude_code_plugins(clone_root: Path) -> list[SkillCandidate]:
    root = clone_root / "anthropics_claude-code" / "plugins"
    if not root.is_dir():
        return []
    out: list[SkillCandidate] = []
    for md in root.rglob("SKILL.md"):
        if "/skills/" not in str(md).replace("\\", "/"):
            continue
        parent = md.parent
        key = _merge_key("anthropics_claude_code", parent, root)
        out.append(
            SkillCandidate(
                "anthropics_claude_code",
                PRIORITY["anthropics_claude_code"],
                parent,
                md,
                key,
            )
        )
    return out


def discover_obra_superpowers(clone_root: Path) -> list[SkillCandidate]:
    root = clone_root / "obra_superpowers" / "skills"
    if not root.is_dir():
        return []
    out: list[SkillCandidate] = []
    for md in root.rglob("SKILL.md"):
        parent = md.parent
        key = _merge_key("obra_superpowers", parent, root)
        out.append(
            SkillCandidate(
                "obra_superpowers",
                PRIORITY["obra_superpowers"],
                parent,
                md,
                key,
            )
        )
    return out


def discover_k_dense(clone_root: Path) -> list[SkillCandidate]:
    root = clone_root / "K-Dense-AI_claude-scientific-skills" / "scientific-skills"
    if not root.is_dir():
        return []
    out: list[SkillCandidate] = []
    for md in root.rglob("SKILL.md"):
        parent = md.parent
        key = _merge_key("k_dense_scientific", parent, root)
        out.append(
            SkillCandidate(
                "k_dense_scientific",
                PRIORITY["k_dense_scientific"],
                parent,
                md,
                key,
            )
        )
    return out


def discover_alirezarezvani(clone_root: Path) -> list[SkillCandidate]:
    root = clone_root / "alirezarezvani_claude-skills"
    if not root.is_dir():
        return []
    out: list[SkillCandidate] = []
    for md in root.rglob("SKILL.md"):
        p = str(md).replace("\\", "/")
        if "/.gemini/" in p or "/.git/" in p:
            continue
        parent = md.parent
        key = _merge_key("alirezarezvani", parent, root)
        out.append(
            SkillCandidate(
                "alirezarezvani",
                PRIORITY["alirezarezvani"],
                parent,
                md,
                key,
            )
        )
    return out


def discover_wshobson_skills(clone_root: Path) -> list[SkillCandidate]:
    root = clone_root / "wshobson_agents" / "plugins"
    if not root.is_dir():
        return []
    out: list[SkillCandidate] = []
    for md in root.rglob("SKILL.md"):
        parent = md.parent
        key = _merge_key("wshobson_agents", parent, root)
        out.append(
            SkillCandidate(
                "wshobson_agents",
                PRIORITY["wshobson_agents"],
                parent,
                md,
                key,
            )
        )
    return out


def pick_winners(
    candidates: list[SkillCandidate],
) -> tuple[dict[str, SkillCandidate], list[dict]]:
    """Per merge_key, keep highest (priority, SKILL.md size); log the rest as skipped."""
    groups: dict[str, list[SkillCandidate]] = defaultdict(list)
    for c in candidates:
        groups[c.merge_key].append(c)
    winners: dict[str, SkillCandidate] = {}
    skipped: list[dict] = []
    for key, group in groups.items():
        best = max(group, key=lambda x: (x.priority, _skill_md_size(x.skill_md)))
        winners[key] = best
        for c in group:
            if c is best:
                continue
            skipped.append(
                {
                    "merge_key": key,
                    "skipped_source": c.source,
                    "skipped_path": str(c.skill_md),
                    "kept_source": best.source,
                    "kept_path": str(best.skill_md),
                    "reason": "duplicate_merge_key",
                }
            )
    return winners, skipped


def sanitize_dest_name(key: str) -> str:
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in key)
    return safe[:200] or "unnamed_skill"


def copy_skill_bundle(src: Path, dest: Path, meta: dict) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest, ignore=_ignore_git)
    (dest / "_AIWF_IMPORT.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )


def import_agents_wshobson(clone_root: Path, dest_base: Path) -> int:
    plugins = clone_root / "wshobson_agents" / "plugins"
    if not plugins.is_dir():
        return 0
    n = 0
    for agent_md in plugins.rglob("*.md"):
        rel = agent_md.relative_to(plugins)
        parts = rel.parts
        if len(parts) < 3 or parts[1] != "agents":
            continue
        plugin = parts[0]
        out = dest_base / "wshobson_agents" / plugin / agent_md.name
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(agent_md, out)
        n += 1
    return n


def import_agents_obra(clone_root: Path, dest_base: Path) -> int:
    agents_dir = clone_root / "obra_superpowers" / "agents"
    if not agents_dir.is_dir():
        return 0
    n = 0
    for f in agents_dir.glob("*.md"):
        out = dest_base / "obra_superpowers" / f.name
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, out)
        n += 1
    return n


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--clone-root",
        type=Path,
        default=Path("/tmp/aiwf_github_imports"),
        help="Directory containing shallow clones (see docs/files.md)",
    )
    ap.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="AIWF repository root (default: parent of factory/)",
    )
    args = ap.parse_args()
    clone_root: Path = args.clone_root.expanduser().resolve()
    repo_root = (
        args.repo_root.expanduser().resolve()
        if args.repo_root
        else Path(__file__).resolve().parents[3]
    )
    skills_out = repo_root / "factory" / "library" / "skills" / "github_imports"
    agents_out = repo_root / "factory" / "library" / "agents" / "github_imports"

    all_cands: list[SkillCandidate] = []
    all_cands.extend(discover_anthropics_official(clone_root))
    all_cands.extend(discover_claude_code_plugins(clone_root))
    all_cands.extend(discover_obra_superpowers(clone_root))
    all_cands.extend(discover_k_dense(clone_root))
    all_cands.extend(discover_alirezarezvani(clone_root))
    all_cands.extend(discover_wshobson_skills(clone_root))

    winners, skipped = pick_winners(all_cands)
    skills_out.mkdir(parents=True, exist_ok=True)

    manifest_skills: list[dict] = []
    for merge_key, winner in sorted(winners.items(), key=lambda x: x[0]):
        dest_name = sanitize_dest_name(merge_key)
        dest = skills_out / dest_name
        meta = {
            "merge_key": merge_key,
            "winner_source": winner.source,
            "priority": winner.priority,
            "original_skill_md": str(winner.skill_md),
            "original_skill_root": str(winner.skill_root),
        }
        copy_skill_bundle(winner.skill_root, dest, meta)
        manifest_skills.append(
            {
                "merge_key": merge_key,
                "dest_rel": str(dest.relative_to(repo_root)),
                "source": winner.source,
                "skill_md": str(winner.skill_md),
            }
        )

    manifest_path = skills_out / "_IMPORT_MANIFEST.json"
    manifest_path.write_text(
        json.dumps(
            {
                "clone_root": str(clone_root),
                "skill_count_imported": len(winners),
                "skill_candidates_total": len(all_cands),
                "skipped_duplicates": skipped,
                "skills": manifest_skills,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    agents_out.mkdir(parents=True, exist_ok=True)
    na = import_agents_wshobson(clone_root, agents_out)
    nb = import_agents_obra(clone_root, agents_out)
    (agents_out / "_IMPORT_MANIFEST.json").write_text(
        json.dumps(
            {
                "clone_root": str(clone_root),
                "wshobson_agent_files": na,
                "obra_agent_files": nb,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "skills_imported": len(winners),
                "skills_candidates": len(all_cands),
                "duplicates_skipped": len(skipped),
                "agents_wshobson": na,
                "agents_obra": nb,
                "skills_dest": str(skills_out),
                "agents_dest": str(agents_out),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
