#!/usr/bin/env python3
"""
Rebuild agents.registry.json and skills.registry.json from on-disk canonical trees.

Legacy pillar paths (factory/library/NN-*, archive-only SKILL.md) are dropped.
Paths are validated relative to repo root.

Run from repo root:
  python3 factory/scripts/analytics/rebuild_canonical_registries.py
"""
from __future__ import annotations

import json
from pathlib import Path


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in here.parents:
        if (p / "AGENTS.md").is_file():
            return p
    return here.parents[3]


def kebab(s: str) -> str:
    return s.replace("_", "-")


def skill_entry_id(skill_file: Path, skills_root: Path) -> str:
    rel = skill_file.relative_to(skills_root)
    parts = rel.parts
    if parts[0] == "github_imports":
        return "github-imports-" + kebab(parts[-2])
    return kebab(skill_file.parent.name)


def discover_skills(root: Path) -> list[dict]:
    skills_root = root / "factory" / "library" / "skills"
    out: list[dict] = []
    seen: dict[str, str] = {}
    for p in sorted(skills_root.rglob("skill.md")):
        if not p.is_file():
            continue
        sid = skill_entry_id(p, skills_root)
        base = sid
        n = 0
        while sid in seen and seen[sid] != str(p):
            n += 1
            sid = f"{base}-{n}"
        seen[sid] = str(p)
        rel = p.relative_to(root).as_posix()
        out.append(
            {
                "id": sid,
                "path": rel,
                "source": "workspace",
                "version": "1.0.0",
                "status": "active",
                "meta": {},
            }
        )
    out.sort(key=lambda x: x["id"])
    return out


def agent_entries(root: Path) -> list[dict]:
    """Map .ai/agents/* to stable IDs used by command_bindings.registry.json."""
    agents_dir = root / ".ai" / "agents"
    mapping: list[tuple[str, Path]] = []
    specialized = agents_dir / "specialized"
    core = agents_dir / "core"
    for stem, aid in (
        ("research", "research-agent"),
        ("scraper", "scraper-agent"),
        ("creator", "creator-agent"),
        ("seo", "seo-agent"),
        ("workflow", "workflow-agent"),
        ("brand", "brand-agent"),
    ):
        p = specialized / f"{stem}.md"
        if p.is_file():
            mapping.append((aid, p))
    for core_file, aid in (
        ("master_guide.md", "guide-agent"),
        ("antigravity.md", "antigravity-agent"),
    ):
        p = core / core_file
        if p.is_file():
            mapping.append((aid, p))
    # Remaining core/specialized agents (library completeness)
    extra_ids = {
        "healing_bot_v2.md": "healing-bot-v2",
        "swarm_router_v3.md": "swarm-router-v3",
        "factory_orchestrator.md": "factory-orchestrator",
        "registry_guardian.md": "registry-guardian",
        "library_curator.md": "library-curator",
        "teaching.md": "teaching-agent",
        "chaos_validator.json": "chaos-validator",
        "recursive_engine.json": "recursive-engine",
    }
    for fname, aid in extra_ids.items():
        p = core / fname
        if p.is_file():
            mapping.append((aid, p))
    primary_stems = {"research", "scraper", "creator", "seo", "workflow", "brand"}
    for p in sorted(specialized.glob("*.md")):
        if p.stem in primary_stems:
            continue
        aid = kebab(p.stem) + "-agent"
        mapping.append((aid, p))

    seen: set[str] = set()
    rows = []
    for aid, path in mapping:
        if aid in seen:
            continue
        seen.add(aid)
        rows.append(
            {
                "id": aid,
                "path": path.relative_to(root).as_posix(),
                "tier": 1,
                "role": aid,
                "single_responsibility": f"See {path.name}",
                "owns": [],
                "triggers": [],
                "subagents": [],
                "input_contract": [],
                "output_contract": [],
                "validation_gates": [],
                "error_handling": [],
                "meta": {},
                "status": "active",
            }
        )
    rows.sort(key=lambda x: x["id"])
    return rows


def main() -> None:
    root = repo_root()
    skills = discover_skills(root)
    agents = agent_entries(root)
    reg_dir = root / ".ai" / "registry"
    reg_dir.mkdir(parents=True, exist_ok=True)
    (reg_dir / "skills.registry.json").write_text(
        json.dumps({"_meta": {"version": "2.0.0", "source": "rebuild_canonical_registries.py"}, "skills": skills}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    (reg_dir / "agents.registry.json").write_text(
        json.dumps({"_meta": {"version": "2.0.0", "source": "rebuild_canonical_registries.py"}, "agents": agents}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote skills.registry.json count={len(skills)} agents.registry.json count={len(agents)}")


if __name__ == "__main__":
    main()
