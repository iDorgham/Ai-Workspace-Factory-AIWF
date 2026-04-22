#!/usr/bin/env python3
import os
import sys
import json
from pathlib import Path

def audit_path_integrity(workspaces_root: str, check_content: bool = False):
    root = Path(workspaces_root)
    if not root.exists():
        print(f"Error: Workspaces root '{workspaces_root}' not found.")
        return False

    violations = []
    
    # Check clients folder
    clients_dir = root / "clients"
    if clients_dir.exists():
        for client_folder in clients_dir.iterdir():
            if not client_folder.is_dir(): continue
            
            # FR-2.1: Client folder contains ONLY metadata/README
            allowed = ["metadata.json", "README.md", "dashboard", ".DS_Store"]
            for item in client_folder.iterdir():
                if item.is_dir():
                    # Check if it's a project folder (001_...)
                    if not (item.name.startswith("00") and "_" in item.name):
                        violations.append(f"ILLEGAL_SUBDIR: Client '{client_folder.name}' has non-project subdir '{item.name}'")
                else:
                    if item.name not in allowed:
                        violations.append(f"METADATA_POLLUTION: Client '{client_folder.name}' contains unexpected file '{item.name}'")

            # FR-2.2: Project folder must be sovereign
            for project_folder in client_folder.iterdir():
                if project_folder.is_dir() and project_folder.name.startswith("00"):
                    if not (project_folder / ".ai").exists():
                        violations.append(f"SOVEREIGNTY_VIOLATION: Project '{project_folder.name}' missing .ai/ folder.")
                    if not (project_folder / "dashboard").exists():
                        violations.append(f"STRUCTURE_VIOLATION: Project '{project_folder.name}' missing dashboard/ folder.")
                    
                    if check_content:
                        # FR-2.2: Verify actual file presence
                        required = {
                            "agents": ["research-agent.md", "creator-agent.md", "workflow-agent.md"],
                            "skills": ["context-compression.md", "mistake-prevention.md"],
                            "commands": ["command-routing.json"]
                        }
                        for bucket, files in required.items():
                            bucket_dir = project_folder / ".ai" / bucket
                            if not bucket_dir.exists():
                                violations.append(f"CONTENT_MISSING: Project '{project_folder.name}' missing bucket '{bucket}'")
                                continue
                            for f in files:
                                if not (bucket_dir / f).exists():
                                    violations.append(f"COMPONENT_MISSING: Project '{project_folder.name}' missing {bucket}/{f}")

    if violations:
        print("\n❌ Path Integrity Audit FAILED:")
        for v in violations:
            print(f"  - {v}")
        return False
    
    print("\n✅ Path Integrity Audit PASSED. All workspaces compliant with FR-2.1 and FR-2.2.")
    return True

if __name__ == "__main__":
    # Default to current workspaces folder
    ws_root = str(Path(__file__).resolve().parents[2] / "workspaces")
    check_content = "--check-content" in sys.argv
    
    # Simple positional arg for root if not flag
    for arg in sys.argv[1:]:
        if not arg.startswith("-"):
            ws_root = arg
            break
            
    success = audit_path_integrity(ws_root, check_content)
    sys.exit(0 if success else 1)
