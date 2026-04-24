#!/usr/bin/env python3
import os
import re
import shutil
from pathlib import Path

ROOT = Path("/Users/Dorgham/Documents/Work/Devleopment/AIWF")
AI_DIR = ROOT / ".ai"
LIB_DIR = ROOT / "factory/library"

def to_snake_case(name):
    # Replace hyphens with underscores, remove "agent" suffix, lowercase
    name = name.replace("-", "_").lower()
    name = re.sub(r"_agent$", "", name)
    return name

def unify_naming(directory):
    print(f"[*] Unifying naming in {directory.relative_to(ROOT)}...")
    for root, dirs, files in os.walk(directory):
        # Unify directories
        for d in dirs:
            if d in [".git", "__pycache__", "node_modules", ".cursor", ".claude"]:
                continue
            new_d = to_snake_case(d)
            if d != new_d:
                old_path = Path(root) / d
                new_path = Path(root) / new_d
                print(f"[*] Renaming dir: {d} -> {new_d}")
                shutil.move(str(old_path), str(new_path))
        
        # Unify files
        for f in files:
            if f.startswith(".") or f == "LICENSE" or f == "README.md":
                continue
            f_stem = Path(f).stem
            f_ext = Path(f).suffix
            new_stem = to_snake_case(f_stem)
            new_f = new_stem + f_ext
            if f != new_f:
                old_path = Path(root) / f
                new_path = Path(root) / new_f
                print(f"[*] Renaming file: {f} -> {new_f}")
                # Use os.rename or shutil.move; shutil.move is safer across filesystems but here it's fine
                os.rename(str(old_path), str(new_path))

def repair_links():
    print("[*] Repairing broken links in Markdown files...")
    # This is a basic implementation; a full one would check every path
    # For now, we'll focus on replacing hyphens with underscores in existing .md links
    md_files = list(ROOT.rglob("*.md"))
    for md in md_files:
        content = md.read_text()
        # Find links like [text](path)
        # We'll just do a global replace of hyphenated agent names to snake_case ones
        # This is safe because we just renamed them
        new_content = re.sub(r"([a-zA-Z0-9]+)-([a-zA-Z0-9-]+)\.md", lambda m: m.group(0).replace("-", "_"), content)
        if content != new_content:
            print(f"[+] Fixed links in {md.relative_to(ROOT)}")
            md.write_text(new_content)

def mirror_ai_to_library():
    print("[*] Mirroring .ai/ (Active Set) to Library (Archive Set)...")
    lib_reg = LIB_DIR / "00_core_orchestration/registry"
    lib_reg.mkdir(parents=True, exist_ok=True)
    
    # 1. Sync Agents
    if (AI_DIR / "agents").exists():
        for root, dirs, files in os.walk(AI_DIR / "agents"):
            for f in files:
                if f.endswith(".md"):
                    src = Path(root) / f
                    rel_path = src.relative_to(AI_DIR / "agents")
                    dest = lib_reg / "agents" / rel_path
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    print(f"[+] Archiving agent: {f}")
                    shutil.copy(str(src), str(dest))

    # 2. Sync Commands
    if (AI_DIR / "commands").exists():
        for f in (AI_DIR / "commands").iterdir():
            if f.is_file() and f.suffix == ".md":
                dest = lib_reg / "commands" / f.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                print(f"[+] Archiving command: {f.name}")
                shutil.copy(str(f), str(dest))

    # 3. Sync Templates
    if (AI_DIR / "templates").exists():
        for root, dirs, files in os.walk(AI_DIR / "templates"):
            for f in files:
                src = Path(root) / f
                rel_path = src.relative_to(AI_DIR / "templates")
                # Mirror to library/templates/
                dest = LIB_DIR / "templates" / rel_path
                dest.parent.mkdir(parents=True, exist_ok=True)
                print(f"[+] Archiving template: {f}")
                shutil.copy(str(src), str(dest))

    # 4. Sync Scripts
    if (AI_DIR / "scripts").exists():
        for root, dirs, files in os.walk(AI_DIR / "scripts"):
            for f in files:
                src = Path(root) / f
                rel_path = src.relative_to(AI_DIR / "scripts")
                dest = LIB_DIR / "scripts" / rel_path
                dest.parent.mkdir(parents=True, exist_ok=True)
                print(f"[+] Archiving script: {f}")
                shutil.copy(str(src), str(dest))

if __name__ == "__main__":
    unify_naming(AI_DIR)
    unify_naming(LIB_DIR)
    repair_links()
    mirror_ai_to_library()
    print("[+] Outbound-Only Sync Complete. .ai/ is mirrored to Library.")
