#!/usr/bin/env python3
"""
Normalize the factory library to field/category folders (not workspace names).

Phase 1: agents, skills, subagents, commands, subcommands (dios/gate-access/sovereign
trees), scripts gate-access mirror, templates catalog/gate-access/dios.

Phase 2: nest Cursor/Antigravity under subcommands/engineering/; move loose
scripts/ and templates/ theme folders under scripts/<field>/ and templates/<field>/.

Re-runnable: skips missing sources. After moves, refreshes canonical `id` on
library *.meta.json.

Run from repo: python3 factory/scripts/migrate_library_to_fields.py
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "library"

TYPE_TO_BUCKET = {
    "agent": "agents",
    "skill": "skills",
    "subagent": "subagents",
    "template": "templates",
    "command": "commands",
    "subcommand": "subcommands",
    "script": "scripts",
}

# Id path convention: agents/skills/subagents/templates use paths relative to that bucket.
# commands/subcommands/scripts use paths relative to factory/library (include bucket prefix).
FULL_PATH_BUCKETS = frozenset({"commands", "subcommands", "scripts"})


def field_for_agent_slug(slug: str) -> str:
    s = slug.lower()
    if any(
        x in s
        for x in (
            "security",
            "compliance",
            "legal",
            "contract-lock",
            "risk",
            "multi-tenant",
            "escalation",
        )
    ):
        return "security-compliance"
    if any(
        x in s
        for x in (
            "brand",
            "creative",
            "marketing",
            "seo",
            "content",
            "design",
            "style",
            "creator",
            "scraper",
            "research-agent",
            "guide-agent",
            "3d-visualization",
            "branding",
            "motion-video",
            "visual",
            "style-transfer",
        )
    ):
        return "creative-marketing"
    if any(x in s for x in ("business", "founder", "hospitality", "forecasting")):
        return "business-strategy"
    if any(
        x in s
        for x in (
            "research",
            "metrics",
            "analytics",
            "knowledge",
            "tutor",
        )
    ):
        return "research-analytics"
    if any(
        x in s
        for x in (
            "workflow",
            "router",
            "orchestrator",
            "automation",
            "dependency",
            "guide",
            "memory",
            "retro",
            "capability",
            "client-preview",
            "prompt",
            "optimizer",
            "debugger",
            "error",
            "contract",
            "runtime",
        )
    ):
        return "product-delivery"
    return "engineering"


def field_for_sovereign_skill_slug(slug: str) -> str:
    s = slug.lower()
    if any(
        x in s
        for x in (
            "security",
            "zero-trust",
            "owasp",
            "rbac",
            "compliance",
            "gdpr",
            "encryption",
            "auth",
            "legal",
            "audit",
            "hallucination",
        )
    ):
        return "security-compliance"
    if any(
        x in s
        for x in (
            "contract",
            "sdd",
            "spec",
            "plan",
            "acceptance",
            "gherkin",
            "pitch",
            "escalation",
            "blameless",
            "spike",
            "backlog",
            "retro",
            "incremental-build",
            "mistake-prevention",
            "compound-engineering",
        )
    ):
        return "product-delivery"
    if any(
        x in s
        for x in (
            "brand",
            "content",
            "marketing",
            "seo",
            "social",
            "design",
            "figma",
            "token",
            "visual",
            "3d",
            "grammar",
            "emotion",
            "govtech",
            "bilingual",
            "cms-studio",
            "client-preview",
            "inclusive",
        )
    ):
        return "creative-marketing"
    return "engineering"


def field_for_subagent_slug(slug: str) -> str:
    return field_for_agent_slug(slug)


def safe_move(src: Path, dest: Path) -> None:
    if not src.exists():
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        raise SystemExit(f"Refusing to overwrite existing destination: {dest}")
    shutil.move(str(src), str(dest))


def merge_dir_contents(src: Path, dest: Path) -> int:
    """Move every child of src into dest, then remove empty src. Returns number of items moved."""
    if not src.is_dir():
        return 0
    dest.mkdir(parents=True, exist_ok=True)
    n = 0
    for item in list(src.iterdir()):
        target = dest / item.name
        if target.exists():
            raise SystemExit(f"Refusing merge collision: {item} -> {target}")
        shutil.move(str(item), str(target))
        n += 1
    src.rmdir()
    return n


def recompute_id(meta_path: Path) -> str | None:
    if not meta_path.name.endswith(".meta.json"):
        return None
    data = json.loads(meta_path.read_text())
    typ = data.get("type")
    if typ not in TYPE_TO_BUCKET:
        return None
    bucket = TYPE_TO_BUCKET[typ]
    primary = meta_path.name[: -len(".meta.json")]
    asset = meta_path.parent / primary
    if not asset.exists():
        return None
    try:
        if bucket in FULL_PATH_BUCKETS:
            rel = asset.relative_to(LIB).as_posix()
        else:
            rel = asset.relative_to(LIB / bucket).as_posix()
    except ValueError:
        return None
    return f"{data['source']}:{bucket}:{rel}"


def refresh_all_meta_ids() -> int:
    n = 0
    for meta in LIB.rglob("*.meta.json"):
        if "_raw" in meta.parts:
            continue
        new_id = recompute_id(meta)
        if not new_id:
            continue
        data = json.loads(meta.read_text())
        if data.get("id") != new_id:
            data["id"] = new_id
            meta.write_text(json.dumps(data, indent=2) + "\n")
            n += 1
    return n


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


def migrate_agents() -> None:
    gal_root = LIB / "agents" / "catalog" / "sovereign"
    if gal_root.is_dir():
        for child in list(gal_root.iterdir()):
            if not child.is_dir():
                continue
            field = field_for_agent_slug(child.name)
            safe_move(child, LIB / "agents" / field / child.name)
        gal_root.rmdir()
        cat = gal_root.parent
        if cat.is_dir() and not any(cat.iterdir()):
            cat.rmdir()

    dios = LIB / "agents" / "dios"
    if dios.is_dir():
        dest_root = LIB / "agents" / "creative-marketing"
        dest_root.mkdir(parents=True, exist_ok=True)
        for child in list(dios.iterdir()):
            safe_move(child, dest_root / child.name)
        dios.rmdir()

    ga = LIB / "agents" / "gate-access"
    if ga.is_dir():
        dest = LIB / "agents" / "security-compliance"
        dest.mkdir(parents=True, exist_ok=True)
        for child in list(ga.iterdir()):
            safe_move(child, dest / child.name)
        ga.rmdir()


def migrate_skills() -> None:
    dios = LIB / "skills" / "dios"
    if dios.is_dir():
        dest = LIB / "skills" / "creative-marketing"
        dest.mkdir(parents=True, exist_ok=True)
        for child in list(dios.iterdir()):
            safe_move(child, dest / child.name)
        dios.rmdir()

    sovereign = LIB / "skills" / "catalog" / 
    if sovereign.is_dir():
        for child in list(sovereign.iterdir()):
            if not child.is_dir():
                continue
            field = field_for_sovereign_skill_slug(child.name)
            safe_move(child, LIB / "skills" / field / child.name)
        sovereign.rmdir()
        cat = LIB / "skills" / "catalog"
        if cat.is_dir() and not any(cat.iterdir()):
            cat.rmdir()

    ga = LIB / "skills" / "gate-access"
    if ga.is_dir():
        dest_root = LIB / "skills" / "engineering"
        dest_root.mkdir(parents=True, exist_ok=True)
        for child in list(ga.iterdir()):
            safe_move(child, dest_root / child.name)
        ga.rmdir()

    # Top-level skill packages (slug folders directly under skills/)
    skills = LIB / "skills"
    skip = {"catalog", "creative-marketing", "engineering", "security-compliance", "product-delivery", "research-analytics", "business-strategy", "design-media"}
    if not skills.is_dir():
        return
    for child in list(skills.iterdir()):
        if not child.is_dir() or child.name in skip:
            continue
        if not (child / "SKILL.md").is_file():
            continue
        field = field_for_sovereign_skill_slug(child.name)
        safe_move(child, skills / field / child.name)


def migrate_subagents() -> None:
    gal = LIB / "subagents" / "catalog" / "sovereign"
    if gal.is_dir():
        for child in list(gal.iterdir()):
            if not child.is_dir():
                continue
            field = field_for_subagent_slug(child.name)
            safe_move(child, LIB / "subagents" / field / child.name)
        gal.rmdir()
        cat = gal.parent
        if cat.is_dir() and not any(cat.iterdir()):
            cat.rmdir()

    ga = LIB / "subagents" / "gate-access"
    if ga.is_dir():
        dest = LIB / "subagents" / "engineering"
        dest.mkdir(parents=True, exist_ok=True)
        for child in list(ga.iterdir()):
            safe_move(child, dest / child.name)
        ga.rmdir()


def migrate_commands() -> None:
    mapping = [
        (LIB / "commands" / , LIB / "commands" / "product-delivery"),
        (LIB / "commands" / "gate-access", LIB / "commands" / "engineering"),
        (LIB / "commands" / "dios", LIB / "commands" / "creative-marketing"),
    ]
    for src, dest in mapping:
        if src.is_dir():
            safe_move(src, dest)


def migrate_subcommands() -> None:
    mapping = [
        (LIB / "subcommands" / "dios", LIB / "subcommands" / "creative-marketing"),
        (LIB / "subcommands" / "gate-access", LIB / "subcommands" / "engineering"),
    ]
    for src, dest in mapping:
        if src.is_dir():
            safe_move(src, dest)


def migrate_scripts() -> None:
    ga = LIB / "scripts" / "gate-access"
    if ga.is_dir():
        dest = LIB / "scripts" / "engineering"
        dest.mkdir(parents=True, exist_ok=True)
        for child in list(ga.iterdir()):
            safe_move(child, dest / child.name)
        ga.rmdir()


def migrate_templates() -> None:
    sovereign = LIB / "templates" / "catalog" / 
    if sovereign.is_dir():
        dest = LIB / "templates" / "product-delivery"
        safe_move(sovereign, dest)
        cat = LIB / "templates" / "catalog"
        if cat.is_dir() and not any(cat.iterdir()):
            cat.rmdir()

    ga = LIB / "templates" / "gate-access"
    if ga.is_dir():
        dest = LIB / "templates" / "engineering"
        safe_move(ga, dest)

    dios = LIB / "templates" / "dios"
    if dios.is_dir():
        dest = LIB / "templates" / "creative-marketing"
        dest.mkdir(parents=True, exist_ok=True)
        for child in list(dios.iterdir()):
            safe_move(child, dest / child.name)
        dios.rmdir()


def migrate_subcommands_ide_under_engineering() -> None:
    """Nest Cursor / Antigravity specs under the engineering field."""
    base = LIB / "subcommands" / "engineering"
    base.mkdir(parents=True, exist_ok=True)
    for name in ("cursor", "antigravity"):
        src = LIB / "subcommands" / name
        if not src.is_dir():
            continue
        dest = base / name
        if dest.exists():
            merge_dir_contents(src, dest)
        else:
            safe_move(src, dest)


def migrate_scripts_loose_into_fields() -> None:
    """Move legacy top-level script packages under scripts/<field>/."""
    scripts = LIB / "scripts"
    if not scripts.is_dir():
        return
    eng = scripts / "engineering"
    eng.mkdir(parents=True, exist_ok=True)
    cm = scripts / "creative-marketing"
    ra = scripts / "research-analytics"
    pd = scripts / "product-delivery"

    # Whole directories -> field bucket (merge when target already exists)
    dir_moves: list[tuple[str, Path]] = [
        ("adapters", eng),
        ("core", eng),
        ("cursor", eng),
        ("git", eng),
        ("hooks", eng),
        ("lib", eng),
        ("setup", eng),
        ("start", eng),
        ("tools", eng),
        ("validate", eng),
        ("brand", cm),
        ("creator", cm),
        ("scraper", cm),
        ("seo", cm),
        ("research", ra),
        ("workflow", pd),
    ]
    for name, dest_parent in dir_moves:
        src = scripts / name
        if not src.is_dir():
            continue
        dest = dest_parent / name
        if dest.exists():
            merge_dir_contents(src, dest)
        else:
            dest_parent.mkdir(parents=True, exist_ok=True)
            safe_move(src, dest)

    # Merge shell check helpers into engineering/check/
    root_check = scripts / "check"
    if root_check.is_dir():
        merge_dir_contents(root_check, eng / "check")

    # Loose executable / library files at scripts/
    for path in list(scripts.iterdir()):
        if not path.is_file():
            continue
        if path.name == ".DS_Store":
            continue
        dest = eng / path.name
        if dest.exists():
            raise SystemExit(f"Collision moving script file to engineering: {path}")
        shutil.move(str(path), str(dest))


def migrate_templates_loose_into_fields() -> None:
    """Move domain template folders that lived at templates/<theme>/ into templates/<field>/<theme>/."""
    tmpl = LIB / "templates"
    if not tmpl.is_dir():
        return
    eng = tmpl / "engineering"
    cm = tmpl / "creative-marketing"
    pd = tmpl / "product-delivery"

    moves: list[tuple[str, Path]] = [
        ("advertising", cm),
        ("brand-discovery", cm),
        ("branding", cm),
        ("content-blueprints", cm),
        ("motion-3d", cm),
        ("seo-meta-templates", cm),
        ("social-marketing", cm),
        ("csv-schemas", eng),
        ("github-workflows", eng),
        ("feature-package", pd),
        ("sdd-spec", pd),
        ("sos-root", pd),
    ]
    for name, dest_parent in moves:
        src = tmpl / name
        if not src.exists():
            continue
        dest = dest_parent / name
        if dest.exists():
            if src.is_dir():
                merge_dir_contents(src, dest)
            else:
                raise SystemExit(f"Collision: {dest} exists for file move {src}")
        else:
            dest_parent.mkdir(parents=True, exist_ok=True)
            safe_move(src, dest)


def flatten_commands_creative_marketing_workflows() -> None:
    """Lift commands/creative-marketing/workflows/*.md to commands/creative-marketing/."""
    wf = LIB / "commands" / "creative-marketing" / "workflows"
    if not wf.is_dir():
        return
    dest = LIB / "commands" / "creative-marketing"
    dest.mkdir(parents=True, exist_ok=True)
    for item in list(wf.iterdir()):
        target = dest / item.name
        if target.exists():
            raise SystemExit(f"Cannot flatten workflows: destination exists: {target}")
        shutil.move(str(item), str(target))
    wf.rmdir()


def flatten_subcommands_creative_marketing_workflows() -> None:
    """Lift subcommands/creative-marketing/workflows/*.md to subcommands/creative-marketing/."""
    wf = LIB / "subcommands" / "creative-marketing" / "workflows"
    if not wf.is_dir():
        return
    dest = LIB / "subcommands" / "creative-marketing"
    dest.mkdir(parents=True, exist_ok=True)
    for item in list(wf.iterdir()):
        target = dest / item.name
        if target.exists():
            raise SystemExit(f"Cannot flatten workflows: destination exists: {target}")
        shutil.move(str(item), str(target))
    wf.rmdir()


LEGACY_BUCKET_TAGS = {
    "dios": "creative-marketing",
    : "product-delivery",
    "gate-access": "engineering",
}


def scrub_legacy_folder_tags_in_bucket(bucket: Path) -> int:
    """Replace old folder-name tags (dios/sovereign/gate-access) with field labels."""
    if not bucket.is_dir():
        return 0
    updated = 0
    for meta in bucket.rglob("*.meta.json"):
        try:
            data = json.loads(meta.read_text())
        except json.JSONDecodeError:
            continue
        tags = data.get("tags")
        if not isinstance(tags, list) or not tags:
            continue
        seen: set[str] = set()
        new_tags: list[str] = []
        changed = False
        for t in tags:
            if not isinstance(t, str):
                continue
            u = LEGACY_BUCKET_TAGS.get(t, t)
            if u != t:
                changed = True
            if u not in seen:
                seen.add(u)
                new_tags.append(u)
        if changed and new_tags != tags:
            data["tags"] = new_tags
            meta.write_text(json.dumps(data, indent=2) + "\n")
            updated += 1
    return updated


def write_commands_readme() -> None:
    """Explain field layout (no per-repo folder names under commands/)."""
    text = """# Commands (library)

Commands are grouped **only** by **field** (`engineering/`, `product-delivery/`, `creative-marketing/`, …).

There is **no** `commands/sovereign/` directory: creative- and growth-oriented command files from studio-style workspaces live under **`creative-marketing/`**. Methodology and delivery commands live under **`product-delivery/`**. Engineering and operator CLIs live under **`engineering/`**.

Legacy folder names (`dios`, `sovereign`, `gate-access`) are not used as path segments here.
"""
    (LIB / "commands" / "README.md").write_text(text)


def write_subcommands_readme() -> None:
    text = """# Sub-commands (library)

Sub-commands are grouped by **field** under `subcommands/<field>/`.

- **Engineering** — day-to-day operator snippets plus IDE specs in `engineering/cursor/` and `engineering/antigravity/` (same filenames can exist in both trees).
- **Creative marketing** — growth and campaign workflow snippets live directly under `creative-marketing/` (no `workflows/` segment).

There is **no** `subcommands/sovereign/` directory; studio-style snippets map to **`creative-marketing/`** the same way as commands.

Legacy folder names (`dios`, `sovereign`, `gate-access`) are not used as path segments here.
"""
    (LIB / "subcommands" / "README.md").write_text(text)


def write_taxonomy() -> None:
    doc = {
        "version": "1.1.0",
        "description": "Library layout grouped by field (domain), not by source workspace name.",
        "fields": [
            "engineering",
            "security-compliance",
            "product-delivery",
            "creative-marketing",
            "business-strategy",
            "research-analytics",
            "design-media",
        ],
        "buckets": {
            "agents": {
                "layout": "agents/<field>/<agent-slug>/AGENT.md",
                "notes": [
                    "Role-playbook mirrors (roles/ and scenarios/) live under agents/security-compliance/.",
                    "Orchestration stack agents (prompts, rules, orchestrator, …) live under agents/creative-marketing/.",
                ],
            },
            "subagents": {
                "layout": "subagents/<field>/<subagent-slug>/<subagent-slug>.json",
                "notes": ["Leaf JSON + sibling *.meta.json"],
            },
            "skills": {
                "layout": "skills/<field>/<skill-slug>/SKILL.md",
                "notes": [
                    "Growth and campaign pillars stay nested under skills/creative-marketing/<pillar>/...",
                ],
            },
            "commands": {
                "layout": "commands/<field>/<command>.md (no dios/sovereign/gate-access path segments)",
                "notes": [
                    "Product methodology → product-delivery/; engineering CLIs → engineering/; studio-style growth workflows → creative-marketing/.",
                    "See commands/README.md for why there is no per-repo folder (e.g. sovereign) under commands/.",
                ],
            },
            "subcommands": {
                "layout": "subcommands/<field>/... (IDE trees: <field>/cursor/ and <field>/antigravity/)",
                "notes": [
                    "Cursor and Antigravity specs live under subcommands/engineering/cursor/ and subcommands/engineering/antigravity/.",
                    "Creative workflow snippets live as loose *.md under subcommands/creative-marketing/.",
                    "See subcommands/README.md for the same field mapping as commands.",
                ],
            },
            "scripts": {
                "layout": "scripts/<field>/...",
                "notes": [
                    "Automation, adapters, git hooks, checks, and workspace utilities live under scripts/engineering/.",
                    "Brand/creator/scraper helpers live under scripts/creative-marketing/.",
                    "Workflow runners live under scripts/product-delivery/.",
                ],
            },
            "templates": {
                "layout": "templates/<field>/... (packaged trees keep internal structure)",
                "notes": [
                    "SDD / SOS / feature-package scaffolds live under templates/product-delivery/.",
                    "Brand, motion, social, and SEO templates live under templates/creative-marketing/.",
                    "CI and data-schema templates live under templates/engineering/.",
                ],
            },
        },
    }
    (LIB / "_taxonomy.json").write_text(json.dumps(doc, indent=2) + "\n")


def main() -> None:
    if not LIB.is_dir():
        print("Library not found:", LIB, file=sys.stderr)
        sys.exit(1)
    migrate_agents()
    migrate_skills()
    migrate_subagents()
    migrate_commands()
    migrate_subcommands()
    migrate_scripts()
    migrate_templates()
    migrate_subcommands_ide_under_engineering()
    migrate_scripts_loose_into_fields()
    migrate_templates_loose_into_fields()
    flatten_commands_creative_marketing_workflows()
    flatten_subcommands_creative_marketing_workflows()
    total_pruned = 0
    for _ in range(25):
        pr = prune_empty_dirs(LIB)
        total_pruned += pr
        if pr == 0:
            break
    print("prune_empty_dirs total:", total_pruned)
    n = refresh_all_meta_ids()
    print("refresh_all_meta_ids:", n)
    nt = scrub_legacy_folder_tags_in_bucket(LIB / "commands")
    nt += scrub_legacy_folder_tags_in_bucket(LIB / "subcommands")
    print("scrub_legacy_folder_tags:", nt)
    write_commands_readme()
    write_subcommands_readme()
    write_taxonomy()
    print("Wrote", LIB / "_taxonomy.json")


if __name__ == "__main__":
    main()
