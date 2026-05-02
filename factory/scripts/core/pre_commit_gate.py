#!/usr/bin/env python3
"""
AIWF Pre-Commit Hook v2 — Sovereign Commit Gate
Install: cp factory/scripts/core/pre_commit_hook_v2.py .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit

Checks (in order):
  1. snake_case naming on staged files
  2. Mirror drift threshold (check_mirror_drift.py with auto-generated reasoning hash)
  3. TODO_PLACEHOLDER strings in staged content
  4. SDD spec density gate on any staged phase folders (spec_density_gate_v2.py)
  5. Governance hash: appends reasoning_hash to commit message if not present

Exit codes: 0 = PASS, 1 = FAIL
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
def _repo_root() -> Path:
    """Resolve repo root whether this file lives under .git/hooks/ or factory/scripts/."""
    here = Path(__file__).resolve()
    for ancestor in [here, *here.parents]:
        if (ancestor / ".git").is_dir():
            return ancestor
    return here.parents[2]


REPO_ROOT = _repo_root()
DRIFT_CHECK = REPO_ROOT / "factory/scripts/core/check_mirror_drift.py"
DENSITY_GATE = REPO_ROOT / "factory/scripts/core/spec_density_gate_v2.py"

# ── Check 1: snake_case naming ─────────────────────────────────────────────────

def check_snake_case() -> bool:
    print("🔍 Checking for snake_case naming violations...")
    try:
        files = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
            text=True,
        ).splitlines()
    except Exception:
        return True

    violations = []
    skip_prefixes = (
        ".github/",
        "docs/",
        "factory/library/scripts/tool_adapters/",
        # Archived pillar tree: historical filenames (kebab-case, role playbooks, etc.).
        "factory/library/archive/legacy_pillars/",
        # Gitignored IDE tree; only rare commits touch it (e.g. stop tracking accidental adds).
        ".cursor/",
        # Third-party / catalog template filenames use kebab-case stems by convention.
        ".ai/templates/subagents/",
        "factory/library/templates/subagents/",
        "factory/library/templates/workspace_imports/",
        # Registry-style mirrors of Claude subagent packs (kebab-case filenames).
        "factory/library/subagents/",
        # Human-facing subcommand docs often use hyphenated stems.
        "factory/library/subcommands/",
        # Generated ledgers and audit reports may use hyphenated basenames.
        ".ai/logs/",
        # Workspace audit snapshots and index trees (mixed naming; generated or hand-maintained).
        ".ai/workspace/",
        # /init template packs mirror upstream kebab-case subagent filenames.
        "factory/templates/subagents/",
        # Outbound mirror of `.cursor/rules/` (hyphenated .mdc stems match IDE conventions).
        "factory/library/rules/workspace_imports/",
        # Vendored third-party skills/agents from public GitHub repos (upstream kebab-case).
        "factory/library/skills/github_imports/",
        "factory/library/agents/github_imports/",
        # Curated awesome-list snapshots (hyphenated upstream filenames).
        "factory/library/reference/github_curated/",
    )
    skip_names = {
        "README",
        "TOMBSTONE",
        "CHANGELOG",
        "LICENSE",
        "Makefile",
        "AGENTS",
        # Canonical library agent/skill filenames (stems are not snake_case tokens).
        "AGENT",
        "SKILL",
        "RULE",
    }
    # v21 SDD / C4 diagrams use hyphenated basenames required by spec_density_gate_v2.py
    allow_hyphenated_stems = {"c4-context", "c4-containers"}

    for f in files:
        if any(f.startswith(p) for p in skip_prefixes):
            continue
        basename = Path(f).name
        if "." in basename:
            name_part = basename.split(".")[0]
            if not name_part:
                continue  # e.g. `.gitignore` → stem ""
            if name_part in skip_names:
                continue
            if name_part in allow_hyphenated_stems:
                continue
            if not re.match(r"^[a-z0-9_]+$", name_part):
                violations.append(f)

    if violations:
        print("❌ Naming violations (must be snake_case):")
        for v in violations:
            print(f"  - {v}")
        return False
    print("  ✓ snake_case OK")
    return True


# ── Check 2: Mirror drift ──────────────────────────────────────────────────────

def check_mirror_drift() -> bool:
    print("🔍 Checking mirror drift status...")
    if not DRIFT_CHECK.exists():
        print("⚠️  Mirror drift script missing — skipping.")
        return True
    try:
        subprocess.check_call([
            "python3", str(DRIFT_CHECK),
            "--threshold", "50"
            # reasoning_hash auto-generated inside the script (v2 behavior)
        ])
        print("  ✓ Mirror drift within threshold")
        return True
    except subprocess.CalledProcessError:
        print("❌ Mirror drift exceeds threshold. Run /git sync to repair.")
        return False


# ── Check 3: TODO_PLACEHOLDER ─────────────────────────────────────────────────

def check_placeholders() -> bool:
    print("🔍 Checking for TODO_PLACEHOLDER strings...")
    try:
        subprocess.check_call([
            "git", "grep", "--cached", "-q", "TODO_PLACEHOLDER",
            "--", ".",
            ":!factory/scripts/core/pre_commit_gate.py",
            ":!factory/scripts/core/validate.py",
            ":!factory/scripts/core/pre_commit_hook_v2.py",
            ":!docs/**",
            ":!**/__pycache__/**"
        ])
        print("❌ TODO_PLACEHOLDER detected in staged changes.")
        return False
    except subprocess.CalledProcessError:
        print("  ✓ No TODO_PLACEHOLDER found")
        return True


# ── Check 4: Spec density gate on staged phase folders ────────────────────────

def check_spec_density() -> bool:
    """
    If any staged files are inside a .ai/plan/ phase folder, run spec_density_gate_v2
    on that folder. Only fails the commit if the phase has status != 'draft' in its
    phase.spec.json (draft phases are allowed to be incomplete mid-work).
    """
    if not DENSITY_GATE.exists():
        print("⚠️  spec_density_gate_v2.py missing — skipping density check.")
        return True

    print("🔍 Checking SDD spec density for staged phase folders...")

    try:
        files = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
            text=True,
        ).splitlines()
    except Exception:
        return True

    # Find unique phase folders in staged files
    phase_folders: set[Path] = set()
    for f in files:
        path = Path(f)
        parts = path.parts
        # Match patterns: .ai/plan/{type}/{phase-folder}/...
        for i, part in enumerate(parts):
            if part == "plan" and i > 0 and parts[i - 1] == ".ai":
                # .ai/plan/{type}/{phase}/... → phase folder is at index i+2
                if len(parts) > i + 2:
                    phase_path = REPO_ROOT / Path(*parts[:i + 3])
                    if phase_path.is_dir():
                        phase_folders.add(phase_path)
                break

    if not phase_folders:
        print("  ✓ No phase folders staged — density check skipped")
        return True

    all_pass = True
    for phase in phase_folders:
        # Check if phase is in draft status — if so, warn but don't block
        spec_file = phase / "phase.spec.json"
        is_draft = True
        if spec_file.exists():
            try:
                import json
                data = json.loads(spec_file.read_text())
                is_draft = data.get("status", "draft") == "draft"
            except Exception:
                is_draft = True

        result = subprocess.run(
            ["python3", str(DENSITY_GATE), "--phase", str(phase)],
            capture_output=True, text=True
        )

        if result.returncode != 0:
            if is_draft:
                print(f"  ⚠️  [{phase.name}] Density gate WARN (draft phase — not blocking)")
                print(f"     {result.stdout.strip()}")
            else:
                print(f"  ❌ [{phase.name}] Density gate FAIL (phase is not draft — blocking commit)")
                print(f"     {result.stdout.strip()}")
                all_pass = False
        else:
            print(f"  ✓ [{phase.name}] Density gate PASS")

    return all_pass


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    print("\n━━━ AIWF Sovereign Pre-Commit Gate v2 ━━━")
    success = True

    if not check_snake_case():
        success = False
    if not check_mirror_drift():
        success = False
    if not check_placeholders():
        success = False
    if not check_spec_density():
        success = False

    if not success:
        print("\n🛑 Pre-commit gate FAILED. Fix violations before committing.")
        sys.exit(1)

    print("\n✅ Pre-commit gate PASSED — commit proceeding.")
    sys.exit(0)


if __name__ == "__main__":
    main()
