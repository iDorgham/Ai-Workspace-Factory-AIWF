#!/usr/bin/env python3
"""Materialize a sovereign workspace from workspace_bundle.manifest.yaml (library-first).

Reads YAML bundles under factory/library/profiles/**/workspace_bundle.manifest.yaml and
symlinks (or copies) the skill allowlist plus explicit ``library:`` paths into
``workspaces/<layer>/<slug>/001_<slug>/.ai/...``.

This complements:
- ``compose.py`` — JSON profiles under ``factory/profiles/*.json`` (legacy layout).
- ``factory_materialize.sh`` — copies from ``factory/shards/<TEMPLATE>`` (not the bundle).

Usage (from AIWF repo root)::

    python3 factory/scripts/core/materialize_workspace_from_bundle.py my-app --personal \\
      --manifest factory/library/profiles/personal/WEB_OS_TITAN/workspace_bundle.manifest.yaml

    python3 factory/scripts/core/materialize_workspace_from_bundle.py my-app --client acme \\
      --manifest factory/library/profiles/personal/WEB_OS_TITAN/workspace_bundle.manifest.yaml

    python3 factory/scripts/core/materialize_workspace_from_bundle.py my-app --clients \\
      --dry-run   # workspaces/clients/my-app/001_my-app (client folder = slug)

    python3 factory/scripts/core/materialize_workspace_from_bundle.py acme corp-site --dry-run \\
      # workspaces/clients/acme/001_corp-site (two positionals: client then project slug)

    python3 factory/scripts/core/materialize_workspace_from_bundle.py my-app --dry-run
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve()
FACTORY_ROOT = SCRIPT.parents[2]  # factory/ (…/factory/scripts/core/<this>.py)
REPO_ROOT = FACTORY_ROOT.parent


def load_manifest(path: Path) -> dict:
    """Parse workspace_bundle YAML (PyYAML preferred; Node ``yaml`` package as fallback)."""
    text = path.read_text()
    try:
        import yaml  # type: ignore[import-untyped]

        return yaml.safe_load(text) or {}
    except ImportError:
        pass
    import json
    import subprocess

    node = shutil.which("node")
    if not node:
        print(
            "Install PyYAML (venv: pip install pyyaml) or install Node and `npm i -g yaml` "
            "so this script can parse the manifest.",
            file=sys.stderr,
        )
        raise SystemExit(1)
    js = r"""
const fs = require('fs');
const yaml = require('yaml');
const p = process.argv[1];
console.log(JSON.stringify(yaml.parse(fs.readFileSync(p, 'utf8'))));
"""
    try:
        proc = subprocess.run(
            [node, "-e", js, str(path.resolve())],
            capture_output=True,
            text=True,
            check=True,
            cwd=str(REPO_ROOT),
        )
    except subprocess.CalledProcessError as exc:
        print(exc.stderr or exc.stdout or str(exc), file=sys.stderr)
        print(
            "Node could not parse YAML (install: npm i -g yaml). "
            "Alternatively use a venv with: pip install pyyaml",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc
    return json.loads(proc.stdout)


def load_workspace_root() -> str:
    for rel in (
        FACTORY_ROOT / "registry" / "factory-config.json",
        FACTORY_ROOT / "scripts" / "registry" / "factory-config.json",
        FACTORY_ROOT / "cfg" / "registry" / "factory-config.json",
    ):
        if rel.is_file():
            data = json.loads(rel.read_text())
            return str(data.get("workspace_root_folder", "workspaces"))
    return "workspaces"


def strip_path_token(s: str) -> str:
    """Take first path token from YAML strings that may include inline ``#`` comments."""
    if not isinstance(s, str):
        return ""
    t = s.split(" #", 1)[0].strip()
    if (t.startswith('"') and t.endswith('"')) or (t.startswith("'") and t.endswith("'")):
        t = t[1:-1]
    return t.strip()


def resolve_workspace_dir(
    *,
    name: str,
    personal: bool,
    client: str | None,
    workspace_root: str,
) -> Path:
    root = REPO_ROOT / workspace_root
    if personal:
        client_path = root / "personal" / name
    elif client:
        client_path = root / "clients" / client
    else:
        client_path = root / name
    default_workspace = client_path / f"001_{name}"
    if not client_path.exists():
        return default_workspace
    # Prefer an existing NNN_<name> with the highest numeric prefix (rematerialize + same-slug copies).
    # Only consider directories whose name ends with _<name> so 001_<other> does not steal numbering.
    best: Path | None = None
    best_n = -1
    for d in client_path.iterdir():
        if not d.is_dir() or "_" not in d.name:
            continue
        if not d.name.endswith(f"_{name}"):
            continue
        try:
            n = int(d.name.split("_", 1)[0])
        except ValueError:
            continue
        if n > best_n:
            best_n = n
            best = d
    return best if best is not None else default_workspace


def _unlink(dest: Path) -> None:
    if dest.is_symlink() or dest.is_file():
        dest.unlink()
    elif dest.is_dir():
        shutil.rmtree(dest)


def link_path(
    src: Path,
    dest: Path,
    *,
    copy: bool,
    dry_run: bool,
    verbose: bool,
) -> bool:
    if not src.exists():
        if verbose:
            print(f"  skip (missing): {src}")
        return False
    if dry_run:
        print(f"  [dry-run] {src.relative_to(REPO_ROOT)} -> {dest.relative_to(REPO_ROOT)}")
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() or dest.is_symlink():
        _unlink(dest)
    try:
        if copy:
            if src.is_dir():
                shutil.copytree(src, dest, symlinks=True)
            else:
                shutil.copy2(src, dest)
        else:
            os.symlink(src.resolve(), dest)
        if verbose:
            print(f"  ok: {dest.relative_to(REPO_ROOT)}")
        return True
    except OSError as exc:
        print(f"  fail: {src} -> {dest}: {exc}", file=sys.stderr)
        return False


def collect_skill_ids(skills_block: object) -> list[str]:
    out: list[str] = []
    if not isinstance(skills_block, list):
        return out
    for item in skills_block:
        if isinstance(item, str) and item.strip():
            out.append(item.strip())
    return out


def ensure_docs_scaffold(workspace: Path, *, dry_run: bool, verbose: bool) -> None:
    """Human docs layout (PRD, roadmap, context). Matches AIWF convention: docs/overview, docs/product, docs/context."""
    docs = workspace / "docs"
    stubs: list[tuple[str, str]] = [
        (
            "README.md",
            """# Documentation

Human-facing specs for this workspace. Prefer editing here; keep machine registries under `.ai/`.

| Area | Path |
|------|------|
| Context (why / who / constraints) | [overview/CONTEXT.md](overview/CONTEXT.md) |
| PRD (what to build) | [product/PRD.md](product/PRD.md) |
| Roadmap (phases / milestones) | [product/ROADMAP.md](product/ROADMAP.md) |
| Technical & ops context | [context/](context/) |
| Onboarding (GitHub → design → docs → plan) | [guides/ONBOARDING.md](guides/ONBOARDING.md) |
""",
        ),
        (
            "guides/ONBOARDING.md",
            """# Onboarding (ordered)

| Step | What | Notes |
|------|------|--------|
| **1. GitHub** | Create / connect the app repository | README, `.gitignore`, branch policy |
| **2. design.md** | Pick a design pack from `.ai/templates/design/` and capture baseline UI rules | See `docs/profile/DESIGN_ONBOARDING.md` if present |
| **3. Docs** | Fill `docs/product/PRD.md`, `docs/product/ROADMAP.md`, `docs/overview/CONTEXT.md`, `docs/context/` | Before dense SDD edits |
| **4. Planning** | Author `.ai/plan/.../phase-*` folders (≥12 files, C4, contracts) | From AIWF root: `python3 factory/scripts/core/spec_density_gate_v2.py --phase <path>` |

Keep human narrative in `docs/`; keep machine registries and phase JSON under `.ai/`.
""",
        ),
        (
            "overview/CONTEXT.md",
            """# Context

**Purpose:** Why this product exists, who it is for, and non-negotiable constraints (region, compliance, brand).

Use this before large `/plan` or SDD passes so phases stay aligned.

## Suggested sections

- Problem and audience
- Success criteria (qualitative + measurable)
- Constraints (residency, languages, integrations)
""",
        ),
        (
            "product/PRD.md",
            """# Product requirements (PRD)

**Purpose:** What shipped scope includes (and excludes).

Link dense phase specs from `.ai/plan/` when they exist.

## Outline

1. Goals and non-goals
2. User stories or journeys
3. Functional requirements
4. Explicitly out of scope (later phases)
""",
        ),
        (
            "product/ROADMAP.md",
            """# Roadmap

**Purpose:** Delivery order and milestones (not a duplicate of the PRD).

## Suggested sections

- Now / next / later (or quarters)
- Dependencies between milestones
- Risks and decision points
""",
        ),
        (
            "context/README.md",
            """# Project context

**Purpose:** Technical and operational notes: architecture, ADR links, environments.

Product narrative belongs in [../overview/CONTEXT.md](../overview/CONTEXT.md).

## Suggested contents

- Stack and repository layout
- Links to ADRs or decision records
- Integration notes (never store secrets in this folder)
""",
        ),
    ]
    for rel, body in stubs:
        dest = docs / rel
        if dry_run:
            print(f"  [dry-run] ensure docs stub if missing: {dest.relative_to(REPO_ROOT)}")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            if verbose:
                print(f"  docs skip (exists): {dest.relative_to(REPO_ROOT)}")
            continue
        dest.write_text(body.strip() + "\n", encoding="utf-8")
        print(f"  docs created: {dest.relative_to(REPO_ROOT)}")


CLIENT_ONBOARDING_YAML = """version: "1"
onboarding_complete: false
steps:
  github_repo:
    label: "GitHub repository created and linked (remote + first commit)"
    done: false
  design_baseline:
    label: "design.md baseline chosen from .ai/templates/design/ (see docs/profile/DESIGN_ONBOARDING.md)"
    done: false
  docs_prd_roadmap_context:
    label: "docs/product/PRD.md, ROADMAP.md, overview/CONTEXT.md, context/README.md drafted"
    done: false
  planning_ready:
    label: ".ai/plan/development/ scaffold copied and phase spec started (see factory/library/planning/templates/sdd/portfolio_plan_phase01_scaffold/)"
    done: false
updated_at: "2026-05-04T00:00:00Z"
"""


def ensure_client_onboarding_scaffold(
    workspace: Path, *, dry_run: bool, verbose: bool
) -> None:
    """Under workspaces/clients/, add .ai/onboarding/state.yaml for /onboard gate."""
    dest = workspace / ".ai" / "onboarding" / "state.yaml"
    if dry_run:
        print(f"  [dry-run] ensure client onboarding state if missing: {dest.relative_to(REPO_ROOT)}")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        if verbose:
            print(f"  onboarding skip (exists): {dest.relative_to(REPO_ROOT)}")
        return
    dest.write_text(CLIENT_ONBOARDING_YAML, encoding="utf-8")
    print(f"  onboarding created: {dest.relative_to(REPO_ROOT)}")


def link_onboard_command(ai: Path, *, copy: bool, dry_run: bool, verbose: bool) -> None:
    """Symlink factory onboard command into workspace .ai/commands/."""
    src = REPO_ROOT / "factory" / "library" / "commands" / "onboard.md"
    dest = ai / "commands" / "onboard.md"
    link_path(src, dest, copy=copy, dry_run=dry_run, verbose=verbose)


def materialize_design_pack(
    repo: Path,
    rel: str,
    dest_root: Path,
    *,
    copy: bool,
    dry_run: bool,
    verbose: bool,
) -> bool:
    """.../templates/design/<pack>/design.md -> dest_root/<pack>/design.md"""
    p = repo / strip_path_token(rel)
    if not p.is_file():
        if verbose:
            print(f"  skip (missing design pack): {p}")
        return False
    parts = p.parts
    try:
        i = parts.index("design")
        pack = parts[i + 1] if i + 1 < len(parts) else p.parent.name
    except ValueError:
        pack = p.parent.name
    dest = dest_root / pack / p.name
    return link_path(p, dest, copy=copy, dry_run=dry_run, verbose=verbose)


def main() -> None:
    ap = argparse.ArgumentParser(description="Materialize workspace from workspace_bundle.manifest.yaml")
    ap.add_argument(
        "name",
        help="Project slug (single-arg), or client folder when a second positional is given",
    )
    ap.add_argument(
        "project",
        nargs="?",
        default=None,
        metavar="PROJECT",
        help="Optional: two-arg form <client_folder> <project_slug> under workspaces/clients/",
    )
    ap.add_argument(
        "--manifest",
        default="factory/library/profiles/personal/WEB_OS_TITAN/workspace_bundle.manifest.yaml",
        help="Path to workspace_bundle.manifest.yaml (repo-relative or absolute)",
    )
    ap.add_argument("--personal", action="store_true", help="Route to workspaces/personal/<name>/")
    ap.add_argument(
        "--client",
        default=None,
        metavar="CLIENT",
        help="Route to workspaces/clients/<client>/001_<name>",
    )
    ap.add_argument(
        "--clients",
        action="store_true",
        help="Shorthand: same as --client <name> (client folder equals project slug)",
    )
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--copy", action="store_true", help="Copy instead of symlink")
    ap.add_argument("--verbose", "-v", action="store_true")
    args = ap.parse_args()

    if args.project is not None:
        if args.personal:
            ap.error("two positionals (<client> <project>) cannot be used with --personal")
        if args.clients:
            ap.error("two positionals cannot be combined with --clients")
        if args.client:
            ap.error("two positionals cannot be combined with --client; use: <client> <project>")
        args.client = args.name
        args.name = args.project

    if args.personal and args.clients:
        ap.error("use only one of --personal and --clients")
    if args.clients and not args.client:
        args.client = args.name

    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = REPO_ROOT / manifest_path
    if not manifest_path.is_file():
        print(f"Manifest not found: {manifest_path}", file=sys.stderr)
        raise SystemExit(1)

    data = load_manifest(manifest_path)
    lib = data.get("library") or {}
    skill_base = REPO_ROOT / strip_path_token(str(lib.get("skill_mirror_base", "factory/library/skills")))

    workspace_root = load_workspace_root()
    workspace = resolve_workspace_dir(
        name=args.name,
        personal=args.personal,
        client=args.client,
        workspace_root=workspace_root,
    )

    print(f"Workspace: {workspace.relative_to(REPO_ROOT)}")
    print(f"Manifest:  {manifest_path.relative_to(REPO_ROOT)}")

    ai = workspace / ".ai"
    skills_dir = ai / "skills"
    counts = {"skills": 0, "library": 0, "skipped": 0}

    if not args.dry_run:
        workspace.mkdir(parents=True, exist_ok=True)
        skills_dir.mkdir(parents=True, exist_ok=True)
        (ai / "registry").mkdir(parents=True, exist_ok=True)
        (ai / "commands").mkdir(parents=True, exist_ok=True)
        (ai / "subcommands").mkdir(parents=True, exist_ok=True)
        (ai / "rules").mkdir(parents=True, exist_ok=True)
        (ai / "templates").mkdir(parents=True, exist_ok=True)
        (ai / "scripts").mkdir(parents=True, exist_ok=True)
        (ai / "hooks").mkdir(parents=True, exist_ok=True)
        (workspace / "docs" / "profile").mkdir(parents=True, exist_ok=True)
        ensure_docs_scaffold(workspace, dry_run=False, verbose=args.verbose)
    else:
        ensure_docs_scaffold(workspace, dry_run=True, verbose=args.verbose)

    if args.client:
        ensure_client_onboarding_scaffold(workspace, dry_run=args.dry_run, verbose=args.verbose)

    # Bundle copy for operators
    bundle_dest = ai / "workspace_bundle.manifest.yaml"
    link_path(manifest_path, bundle_dest, copy=args.copy, dry_run=args.dry_run, verbose=args.verbose)

    if args.client:
        link_onboard_command(ai, copy=args.copy, dry_run=args.dry_run, verbose=args.verbose)

    kw = {"copy": args.copy, "dry_run": args.dry_run, "verbose": args.verbose}

    for sid in collect_skill_ids(data.get("skills")):
        src = skill_base / sid
        dest = skills_dir / sid
        if not src.is_dir():
            print(f"  missing skill dir: {src.relative_to(REPO_ROOT)}", file=sys.stderr)
            counts["skipped"] += 1
            continue
        if link_path(src, dest, **kw):
            counts["skills"] += 1
        else:
            counts["skipped"] += 1

    # Single-path library entries
    single_map: list[tuple[str, Path]] = [
        ("agents_registry_yaml", ai / "registry" / "agents_registry.yaml"),
        ("subagents_registry_json", ai / "registry" / "subagents_registry.json"),
        ("commands_merged_md", ai / "commands" / "commands.md"),
        ("commands_registry_yaml", ai / "commands" / "registry.yaml"),
        ("templates_design_readme", ai / "templates" / "design" / "README.md"),
        ("templates_design_catalog_json", ai / "templates" / "design" / "catalog.json"),
    ]
    for key, dest in single_map:
        rel = lib.get(key)
        if not rel:
            continue
        src = REPO_ROOT / strip_path_token(str(rel))
        if link_path(src, dest, **kw):
            counts["library"] += 1
        else:
            counts["skipped"] += 1

    # Directory library entries
    dir_map: list[tuple[str, Path]] = [
        ("command_templates_dir", ai / "commands" / "templates"),
        ("templates_core_dir", ai / "templates" / "core"),
    ]
    for key, dest in dir_map:
        rel = lib.get(key)
        if not rel:
            continue
        src = REPO_ROOT / strip_path_token(str(rel))
        if link_path(src, dest, **kw):
            counts["library"] += 1
        else:
            counts["skipped"] += 1

    # List-of-files → basename under target dir
    list_map: list[tuple[str, Path]] = [
        ("commands_support_md", ai / "commands"),
        ("subcommands_md", ai / "subcommands"),
        ("rules_workspace_mirror_mdc", ai / "rules"),
        ("scripts_workspace_imports", ai / "scripts"),
        ("profile_scripts", ai / "scripts"),
        ("hooks_operator_readme", ai / "hooks"),
    ]
    for key, dest_dir in list_map:
        for rel in lib.get(key) or []:
            src = REPO_ROOT / strip_path_token(str(rel))
            dest = dest_dir / src.name
            if link_path(src, dest, **kw):
                counts["library"] += 1
            else:
                counts["skipped"] += 1

    for rel in lib.get("templates_design_packs_md") or []:
        if materialize_design_pack(
            REPO_ROOT,
            str(rel),
            ai / "templates" / "design",
            copy=args.copy,
            dry_run=args.dry_run,
            verbose=args.verbose,
        ):
            counts["library"] += 1
        else:
            counts["skipped"] += 1

    def profile_operator_dest_basename(src: Path) -> str:
        """Avoid docs/profile/README.md collision: profile hooks README → HOOKS.md."""
        if src.name == "README.md" and "hooks" in src.parts:
            return "HOOKS.md"
        return src.name

    for rel in lib.get("profile_operator_docs") or []:
        src = REPO_ROOT / strip_path_token(str(rel))
        dest = workspace / "docs" / "profile" / profile_operator_dest_basename(src)
        if dest.exists() and dest.is_file() and not dest.is_symlink():
            if args.verbose:
                print(f"  skip profile_operator (workspace file): {dest.relative_to(REPO_ROOT)}")
            continue
        if link_path(src, dest, **kw):
            counts["library"] += 1
        else:
            counts["skipped"] += 1

    for rel in lib.get("factory_repo_scripts_note") or []:
        token = strip_path_token(str(rel))
        if not token.endswith(".py") and not token.endswith(".sh"):
            continue
        src = REPO_ROOT / token
        dest = ai / "scripts" / src.name
        if link_path(src, dest, **kw):
            counts["library"] += 1
        else:
            counts["skipped"] += 1

    print(
        f"Done — skills: {counts['skills']}, library links: {counts['library']}, skipped: {counts['skipped']}"
        + (" (dry-run)" if args.dry_run else "")
    )


if __name__ == "__main__":
    main()
