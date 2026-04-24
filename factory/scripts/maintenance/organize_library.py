#!/usr/bin/env python3
"""
Normalize factory/library layouts (field/category buckets, not workspace names):
- skills: flat *.md under skills/ -> skills/<field>/<slug>/SKILL.md
- skills: creative-marketing/**/*.md (leaf docs) -> nested SKILL.md packages
- agents: flat *.md under agents/ -> agents/<field>/<slug>/AGENT.md
- agents: creative-marketing flat *.md -> agents/creative-marketing/<slug>/AGENT.md
- subagents: flat *.json -> subagents/<field>/<slug>/<slug>.json
- templates: flat *.md -> templates/<field>/<slug>/TEMPLATE.md (default field: product-delivery)
- commands: remove root duplicates when commands/product-delivery/<same> exists
- prune empty directories; refresh ids via migrate_library_to_fields helpers
Idempotent: skips when destination already exists.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "library"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from migrate_library_to_fields import (
    field_for_agent_slug,
    field_for_sovereign_skill_slug,
    field_for_subagent_slug,
    refresh_all_meta_ids,
    write_taxonomy,
)


def update_meta(meta_path: Path, *, new_id: str, new_name: str | None = None) -> None:
    data = json.loads(meta_path.read_text())
    data["id"] = new_id
    if new_name is not None:
        data["name"] = new_name
    meta_path.write_text(json.dumps(data, indent=2) + "\n")


def prune_empty_dirs(base: Path) -> int:
    removed = 0
    if not base.is_dir():
        return 0
    for p in sorted(base.rglob("*"), key=lambda x: len(x.parts), reverse=True):
        if p.is_dir():
            try:
                next(p.iterdir())
            except StopIteration:
                p.rmdir()
                removed += 1
    return removed


def dedupe_command_roots() -> int:
    cmd = LIB / "commands"
    if not cmd.is_dir():
        return 0
    n = 0
    for md in list(cmd.glob("*.md")):
        twin = cmd / "product-delivery" / md.name
        if twin.is_file():
            meta = md.with_name(md.name + ".meta.json")
            md.unlink(missing_ok=True)
            meta.unlink(missing_ok=True)
            n += 1
    return n


def migrate_skills_root_flat() -> int:
    skills = LIB / "skills"
    if not skills.is_dir():
        return 0
    n = 0
    for md in list(skills.glob("*.md")):
        stem = md.stem
        field = field_for_sovereign_skill_slug(stem)
        dest_dir = skills / field / stem
        dest = dest_dir / "SKILL.md"
        if dest.exists():
            continue
        meta_old = md.with_name(md.name + ".meta.json")
        if not meta_old.is_file():
            continue
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(md), str(dest))
        meta_new = dest.with_name(dest.name + ".meta.json")
        shutil.move(str(meta_old), str(meta_new))
        data = json.loads(meta_new.read_text())
        src = data.get("source", )
        rel_id = dest.relative_to(LIB / "skills").as_posix()
        new_id = f"{src}:skills:{rel_id}"
        update_meta(meta_new, new_id=new_id, new_name=stem)
        n += 1
    return n


def migrate_dios_skills() -> int:
    base = LIB / "skills" / "creative-marketing"
    if not base.is_dir():
        return 0
    n = 0
    for md in list(base.rglob("*.md")):
        if md.name == "SKILL.md":
            continue
        rel = md.relative_to(base)
        if len(rel.parts) < 2:
            continue
        stem = md.stem
        dest_dir = md.parent / stem
        dest = dest_dir / "SKILL.md"
        if dest.exists():
            continue
        meta_old = md.with_name(md.name + ".meta.json")
        if not meta_old.is_file():
            continue
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(md), str(dest))
        meta_new = dest.with_name("SKILL.md.meta.json")
        shutil.move(str(meta_old), str(meta_new))
        data = json.loads(meta_new.read_text())
        src = data.get("source", "local")
        rel_id = dest.relative_to(LIB / "skills").as_posix()
        new_id = f"{src}:skills:{rel_id}"
        update_meta(meta_new, new_id=new_id, new_name=stem)
        n += 1
    return n


def migrate_agents_root_flat() -> int:
    agents = LIB / "agents"
    if not agents.is_dir():
        return 0
    n = 0
    for md in list(agents.glob("*.md")):
        stem = md.stem
        field = field_for_agent_slug(stem)
        dest_dir = agents / field / stem
        dest = dest_dir / "AGENT.md"
        if dest.exists():
            continue
        meta_old = md.with_name(md.name + ".meta.json")
        if not meta_old.is_file():
            continue
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(md), str(dest))
        meta_new = dest.with_name("AGENT.md.meta.json")
        shutil.move(str(meta_old), str(meta_new))
        data = json.loads(meta_new.read_text())
        src = data.get("source", "sovereign")
        rel_id = dest.relative_to(LIB / "agents").as_posix()
        new_id = f"{src}:agents:{rel_id}"
        update_meta(meta_new, new_id=new_id, new_name=stem)
        n += 1
    return n


def migrate_agents_dios_root() -> int:
    cm = LIB / "agents" / "creative-marketing"
    if not cm.is_dir():
        return 0
    n = 0
    for md in list(cm.glob("*.md")):
        stem = md.stem
        dest_dir = cm / stem
        dest = dest_dir / "AGENT.md"
        if dest.exists():
            continue
        meta_old = md.with_name(md.name + ".meta.json")
        if not meta_old.is_file():
            continue
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(md), str(dest))
        meta_new = dest.with_name("AGENT.md.meta.json")
        shutil.move(str(meta_old), str(meta_new))
        data = json.loads(meta_new.read_text())
        src = data.get("source", "local")
        rel_id = dest.relative_to(LIB / "agents").as_posix()
        new_id = f"{src}:agents:{rel_id}"
        update_meta(meta_new, new_id=new_id, new_name=stem)
        n += 1
    return n


def migrate_subagents_root_flat() -> int:
    sub = LIB / "subagents"
    if not sub.is_dir():
        return 0
    n = 0
    for js in list(sub.glob("*.json")):
        if js.name.endswith(".meta.json"):
            continue
        stem = js.stem
        field = field_for_subagent_slug(stem)
        dest_dir = sub / field / stem
        dest = dest_dir / js.name
        if dest.exists():
            continue
        meta_old = js.with_name(js.name + ".meta.json")
        if not meta_old.is_file():
            continue
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(js), str(dest))
        meta_new = dest.with_name(dest.name + ".meta.json")
        shutil.move(str(meta_old), str(meta_new))
        data = json.loads(meta_new.read_text())
        src = data.get("source", "sovereign")
        rel_id = dest.relative_to(LIB / "subagents").as_posix()
        new_id = f"{src}:subagents:{rel_id}"
        update_meta(meta_new, new_id=new_id, new_name=stem)
        n += 1
    return n


def migrate_templates_root_flat() -> int:
    tmpl = LIB / "templates"
    if not tmpl.is_dir():
        return 0
    skip = {"README.md"}
    n = 0
    for md in list(tmpl.glob("*.md")):
        if md.name in skip:
            continue
        stem = md.stem
        field = field_for_sovereign_skill_slug(stem)
        dest_dir = tmpl / field / stem
        dest = dest_dir / "TEMPLATE.md"
        if dest.exists():
            continue
        meta_old = md.with_name(md.name + ".meta.json")
        if not meta_old.is_file():
            continue
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(md), str(dest))
        meta_new = dest.with_name("TEMPLATE.md.meta.json")
        shutil.move(str(meta_old), str(meta_new))
        data = json.loads(meta_new.read_text())
        src = data.get("source", )
        rel_id = dest.relative_to(LIB / "templates").as_posix()
        new_id = f"{src}:templates:{rel_id}"
        update_meta(meta_new, new_id=new_id, new_name=stem)
        n += 1
    return n


def main() -> None:
    print("dedupe_command_roots:", dedupe_command_roots())
    print("migrate_skills_root_flat:", migrate_skills_root_flat())
    print("migrate_dios_skills:", migrate_dios_skills())
    print("migrate_agents_root_flat:", migrate_agents_root_flat())
    print("migrate_agents_dios_root:", migrate_agents_dios_root())
    print("migrate_subagents_root_flat:", migrate_subagents_root_flat())
    print("migrate_templates_root_flat:", migrate_templates_root_flat())
    rounds = 0
    total_pruned = 0
    while True:
        pr = prune_empty_dirs(LIB)
        total_pruned += pr
        rounds += 1
        if pr == 0 or rounds > 20:
            break
    print("prune_empty_dirs (total):", total_pruned)
    print("refresh_all_meta_ids:", refresh_all_meta_ids())
    write_taxonomy()
    print("Wrote", LIB / "_taxonomy.json")


if __name__ == "__main__":
    main()
