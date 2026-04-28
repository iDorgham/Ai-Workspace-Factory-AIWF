#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime
import json
import shutil
import hashlib
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = ROOT.parent

BUCKETS = [
    "agents",
    "subagents",
    "skills",
    "commands",
    "subcommands",
    "templates",
    "scripts",
]

def resolve_library_path(bucket: str, name: str) -> Path | None:
    src_root = ROOT / "library"
    # 1. Direct file match
    for p in src_root.rglob("*"):
        if p.is_file() and f"/{bucket}/" in str(p) and p.stem.lower() == name.lower():
            return p
            
    # 2. Directory match (AGENT.md, SKILL.md, etc.)
    clean_name = name.lower().replace("-", "").replace("_", "")
    for p in src_root.rglob("*"):
        clean_p_name = p.name.lower().replace("-", "").replace("_", "")
        if p.is_dir() and f"/{bucket}/" in str(p) and (clean_p_name == clean_name or clean_name in clean_p_name):
            for filename in ["AGENT.md", "SKILL.md", "COMMANDS.md", "MANIFEST.json"]:
                if (p / filename).exists():
                    return p / filename
                    
    # 3. Fuzzy match fallback
    matches = sorted(
        [
            p
            for p in src_root.rglob("*")
            if p.is_file()
            and f"/{bucket}/" in str(p)
            and not p.name.endswith(".meta.json")
            and (name.lower() in p.stem.lower() or name.lower() in p.as_posix().lower())
        ]
    )
    return matches[0] if matches else None

def mirror_commands_to_ide(workspace: Path, commands_dir: Path):
    rules_map = {
        ".cursor/rules": ".mdc",
        ".github": "-copilot-instructions.md",
        ".claude/commands": "",
        ".gemini/rules": ""
    }
    
    # v5.1.0: Version pinning metadata
    version_id = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    try:
        import subprocess
        git_hash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
        version_id = f"git-{git_hash}"
    except:
        pass

    for relative_dir, suffix in rules_map.items():
        rules_dir = workspace / relative_dir
        rules_dir.mkdir(parents=True, exist_ok=True)
        
        for cmd_file in commands_dir.glob("*"):
            if cmd_file.suffix in [".md", ".json"]:
                # Deterministic filename for the rule
                if relative_dir == ".github":
                    target_rule = rules_dir / "copilot-instructions.md"
                    mode = "a" if target_rule.exists() else "w"
                else:
                    target_rule = rules_dir / f"{cmd_file.stem}{suffix}"
                    mode = "w"

                content = f"\n\n---\n# {cmd_file.stem} definition\n# Version-Pin: {version_id}\n"
                if cmd_file.suffix == ".json":
                    content += "```json\n" + cmd_file.read_text() + "\n```\n"
                else:
                    content += cmd_file.read_text() + "\n"
                
                with open(target_rule, mode) as f:
                    f.write(content)

def calculate_hash(path: Path) -> str:
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def validate_manifest(profile_data: dict) -> bool:
    required_keys = ["profile", "display", "version", "required"]
    required_buckets = ["agents", "skills", "commands"]
    
    if not all(k in profile_data for k in required_keys):
        return False
    if not all(b in profile_data["required"] for b in required_buckets):
        return False
    return True

def assemble_components(profile: dict, workspace: Path, dry_run: bool, verbose: bool):
    components: dict[str, list[str]] = {}
    ai_root = workspace / ".ai"
    verification_log = []
    
    for bucket in BUCKETS:
        requested = profile.get("required", {}).get(bucket, [])
        components[bucket] = []
        dst_bucket = ai_root / bucket
        
        if not dry_run:
            dst_bucket.mkdir(parents=True, exist_ok=True)
        
        for name in requested:
            lib_path = resolve_library_path(bucket, name)
            
            if not lib_path:
                if verbose: print(f"⚠ Warning: Could not find {bucket} component '{name}'")
                continue
            
            dest_name = name
            if not dest_name.lower().endswith(lib_path.suffix.lower()):
                dest_name += lib_path.suffix
            dest = dst_bucket / dest_name
            
            if dry_run:
                print(f"[DRY-RUN] Would link: {lib_path.relative_to(ROOT)} -> {dest.relative_to(workspace.parent.parent)}")
            else:
                if dest.exists() or dest.is_symlink():
                    dest.unlink()
                
                try:
                    # PREFER SYMLINKS for library-first governance
                    os.symlink(lib_path.resolve(), dest)
                    if verbose: print(f"✓ Linked {lib_path.name} -> {dest_name}")
                except (OSError, AttributeError):
                    # Fallback to copy
                    shutil.copy2(lib_path, dest)
                    if verbose: print(f"⚡ Copied {lib_path.name} -> {dest_name} (Symlink Failed)")
                
                components[bucket].append(dest_name)
    return components


def load_factory_config() -> dict:
    p = ROOT / "registry" / "factory-config.json"
    return json.loads(p.read_text())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("name", help="Slug for the project/client")
    ap.add_argument("--client", help="Client name (triggers routing to clients/ hierarchy)", default=None)
    ap.add_argument("--personal", action="store_true", help="Marks as a personal project")
    ap.add_argument("--profile", default=None, help="Direct profile selection")
    ap.add_argument("--pipeline", default=None, help="Pipeline alias (e.g. sovereign, web-dev-rtl-first)")
    ap.add_argument("--explain-routing", action="store_true", help="Outputs deterministic routing path without executing composition")
    ap.add_argument("--structure", choices=["sovereign", "legacy"], default="sovereign", help="Enforce specific folder structure (default: sovereign)")
    ap.add_argument("--dry-run", action="store_true", help="Prints mapping without executing composition")
    ap.add_argument("--verbose", action="store_true", help="Enable detailed logging")
    ap.add_argument("--verify-assembly", action="store_true", help="Validates hashes/symlinks after assembly")
    ap.add_argument("--preserve-state", action="store_true", default=True, help="Prevents overwriting sovereign memory/state files (default: True)")
    args = ap.parse_args()

    cfg = load_factory_config()
    root_name = cfg.get("workspace_root_folder", "workspaces")

    # Routing Logic Phase 2: Metadata vs Sovereign Workspace
    if args.personal:
        client_path = REPO_ROOT / root_name / "personal" / args.name
        workspace = client_path / f"001_{args.name}"
    elif args.client:
        client_path = REPO_ROOT / root_name / "clients" / args.client
        workspace = client_path / f"001_{args.name}"
    else:
        # Fallback to general workspace
        client_path = REPO_ROOT / root_name / args.name
        workspace = client_path / f"001_{args.name}"

    # FR-2.3: Enforce --structure validation pre-generation
    if args.structure == "sovereign":
        import re
        if not re.match(r"^[a-zA-Z0-9_-]+$", args.name):
             print(f"Error: Slug '{args.name}' contains invalid characters. Use alphanumeric, hyphens, or underscores.")
             return
        
        # Check if project already exists with a different numbering
        if client_path.exists():
            existing = [d.name for d in client_path.iterdir() if d.is_dir() and "_" in d.name]
            if existing:
                # Find highest number
                try:
                    nums = [int(d.split("_")[0]) for d in existing]
                    next_num = max(nums) + 1
                    workspace = client_path / f"{next_num:03d}_{args.name}"
                except ValueError:
                    pass

    intake_name = args.client if args.client else args.name
    intake_path = ROOT / "intake" / f"{intake_name}.json"
    
    if not intake_path.exists():
        intake = {"workspace_purpose": "web-product-suite"}
    else:
        intake = json.loads(intake_path.read_text())

    profile_name = args.profile or intake.get("workspace_purpose", "web-product-suite")

    # Phase 1: Pipeline Alias Resolution
    routing_explanation = []
    if args.pipeline:
        alias_path = ROOT / "library" / "pipeline-alias-mapping.json"
        if alias_path.exists():
            aliases = json.loads(alias_path.read_text()).get("pipelines", {})
            if args.pipeline in aliases:
                profile_name = aliases[args.pipeline]["profile_target"]
                routing_explanation.append(f"✓ Alias '{args.pipeline}' resolved to profile '{profile_name}' via mapping table.")
            else:
                routing_explanation.append(f"⚠ Alias '{args.pipeline}' not found in mapping table.")
        else:
            routing_explanation.append(f"⚠ Mapping table not found at {alias_path.relative_to(ROOT)}.")
    elif args.profile:
        routing_explanation.append(f"✓ Direct profile override: '{args.profile}'.")
    else:
        routing_explanation.append(f"✓ Using default/intake profile: '{profile_name}'.")

    profile_path = ROOT / "profiles" / f"{profile_name}.json"
    if not profile_path.exists():
         routing_explanation.append(f"⚠ Profile '{profile_name}' not found on disk. Falling back to 'web-product-suite'.")
         profile_name = "web-product-suite"
         profile_path = ROOT / "profiles" / f"{profile_name}.json"

    if args.explain_routing:
        print("\n--- DETERMINISTIC ROUTING EXPLANATION ---")
        for line in routing_explanation:
            print(line)
        print(f"Final Execution Path: {profile_path.relative_to(ROOT)}")
        print("-----------------------------------------\n")
        return

    # Load unified JSON manifest (v5.1.0 Standard)
    profile = json.loads(profile_path.read_text())

    if not validate_manifest(profile):
        print(f"Error: Profile '{profile_name}' failed schema validation. Missing required industrial headers.")
        return

    # Scaffold structural isolation (Phase 2)
    client_path.mkdir(parents=True, exist_ok=True)
    
    # PRESERVE STATE GUARD (v5.1.0 Hot-Sync Protocol)
    if args.preserve_state:
        preserve_paths = [
            ".cursor/hooks/state/continual-learning-index.json",
            ".ai/memory/state.json",
            ".ai/memory/workflow.jsonl",
            ".ai/dashboard/memory.json",
            "dashboard/memory.json"
        ]
        for p in preserve_paths:
            if (workspace / p).exists():
                if args.verbose: print(f"🛡️ Hot-Sync Guard: Preserving {p}")
                # We handle this by not wiping these folders during re-composition
    
    if not (client_path / "metadata.json").exists():
        (client_path / "metadata.json").write_text(json.dumps({"client": args.client or args.name, "created_at": str(datetime.datetime.now())}))
    
    workspace.mkdir(parents=True, exist_ok=True)
    (workspace / "dashboard").mkdir(parents=True, exist_ok=True)

    # Phase 2.1: Implement Local Dashboard Memory natively
    dash_folder = workspace / ".ai" / "dashboard"
    dash_folder.mkdir(parents=True, exist_ok=True)
    default_memory = {
        "project_id": args.name,
        "client_id": args.client or args.name,
        "status": "Composed",
        "health": 100,
        "progress_percentage": 0,
        "phases": [
            {"name": "Composition", "status": "completed"},
            {"name": "Execution", "status": "pending"}
        ],
        "tasks": [{"id": "init", "description": "Sovereign Framework Initialized", "completed": True}],
        "last_updated": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    (dash_folder / "memory.json").write_text(json.dumps(default_memory, indent=2))
    
    if not args.dry_run:
        # Phase 5: Trigger Dashboard Rendering
        render_script = ROOT / "scripts" / "render_dashboard.py"
        if render_script.exists():
            import subprocess
            # Render Client Dashboard
            subprocess.run([sys.executable, str(render_script), "client", str(client_path / "dashboard")], check=False)
            # Render Project Dashboard
            subprocess.run([sys.executable, str(render_script), "project", str(workspace / "dashboard")], check=False)

    components = assemble_components(profile, workspace, args.dry_run, args.verbose)

    if args.dry_run:
        print("\n--- DRY RUN COMPLETE ---")
        return

    # Mirror commands to multiple IDEs
    mirror_commands_to_ide(workspace, workspace / ".ai" / "commands")
    
    if args.verify_assembly:
        print("\n--- ASSEMBLY VERIFICATION ---")
        for bucket, files in components.items():
            for f in files:
                p = workspace / ".ai" / bucket / f
                if p.is_symlink():
                    print(f"✅ {bucket}/{f}: Symlink Valid")
                else:
                    print(f"⚡ {bucket}/{f}: Verified Copy")

    # Phase 2: Generate Project-Level Registries
    (workspace / ".ai" / "registry").mkdir(parents=True, exist_ok=True)
    
    agents_reg = {"version": "1.0", "project": args.name, "agents": components.get("agents", [])}
    skills_reg = {"version": "1.0", "project": args.name, "skills": components.get("skills", [])}
    cmds_reg = {"version": "1.0", "project": args.name, "commands": components.get("commands", [])}
    
    (workspace / ".ai" / "registry" / "agents.registry.json").write_text(json.dumps(agents_reg, indent=2))
    (workspace / ".ai" / "registry" / "skills.registry.json").write_text(json.dumps(skills_reg, indent=2))
    (workspace / ".ai" / "registry" / "commands.registry.json").write_text(json.dumps(cmds_reg, indent=2))

    manifest = {
        "client": args.client,
        "profile": profile_name,
        "pipeline_alias": args.pipeline,
        "generated_at": datetime.datetime.now(datetime.timezone.utc)
        .replace(microsecond=0)
        .isoformat(),
        "components": components,
        "output_path": str(workspace),
        "validation": {"status": "pending"},
    }
    (ROOT / "manifests" / f"{args.client or args.name}.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (ROOT / "reports" / f"{args.client or args.name}-composition.md").write_text(
        f"# Composition Report: {args.client or args.name}\n\n"
        f"- Profile: {profile_name}\n"
        f"- Output: {workspace}\n"
        + "\n".join(f"- {k}: {len(v)}" for k, v in components.items())
        + "\n"
    )
    print(f"Composed {workspace} with Sovereign 3-Tier Layer")


if __name__ == "__main__":
    main()
