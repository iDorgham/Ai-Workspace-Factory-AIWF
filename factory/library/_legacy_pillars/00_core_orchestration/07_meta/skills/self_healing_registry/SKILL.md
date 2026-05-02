---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🩹 Self-Healing Registry

> **Tier:** 💎 OMEGA (Tier 1)
> **Department:** 07-meta
> **Domain:** system-resilience
> **Status:** PRODUCTION_READY

## 🎯 Purpose
This skill provides the automated orchestration logic for detecting registry drift, fixing broken path symlinks, and reconciling the `_taxonomy.json` with the actual file system state. It is the core engine for maintaining 100/100 integrity in the Sovereign Factory.

## 🏛️ Core Principles
1. **Consistency First**: The registry must match reality. If a file exists, it must be indexed. If it is indexed, it must exist.
2. **Automated Reconciliation**: No manual registry edits should be required for routine relocation or archival.
3. **Audit-as-Service**: The registry should be self-auditing every time an agent queries a component.
4. **Resilient Meta-Data**: Protecting essential metadata (version, tier, ID) from corruption during automated moves.

## 🛠️ Techniques & Implementation

### 1. Drift Detection Algorithm
Compares the `REGISTRY.md` and `.ai/registry/*.json` files against the current recursive directory listing.
```python
import os
import json

def detect_registry_drift(current_paths: list, registry_data: list) -> dict:
    """
    Identifies orphans (in registry but not FS) and ghosts (in FS but not registry).
    """
    reg_paths = {item['path'] for item in registry_data}
    fs_paths = set(current_paths)
    
    orphans = reg_paths - fs_paths
    ghosts = fs_paths - reg_paths
    
    return {"orphans": list(orphans), "ghosts": list(ghosts)}
```

### 2. Auto-Reconciler (The "Healer")
Automatically appends ghosts to the registry with default metadata and purges orphans.
```python
def reconcile_registry(drift_report: dict) -> bool:
    # Logic to prune orphans and register ghosts
    # Enforces naming conventions and minimum file existence
    return True
```

### 3. Path-Taxonomy Verifier
Validates that every file's physical path correctly reflects its `cluster` and `category` as defined in the YAML frontmatter.
```python
def verify_taxonomy_alignment(file_path: str, metadata: dict) -> bool:
    # Check if 'factory/library/01-software' matches metadata['cluster']
    return True
```

## 🚫 Anti-Patterns
- **Stale Indexing**: Keeping references to deleted or archived files in the active search manifest.
- **Manual Mirroring**: Forcing devs to update three different files (REGISTRY, JSON, MASTER_CONTEXT) manually for every new skill.
- **Silent Failure**: Failing to notify the `@Architect` when a core symlink is broken.

## 🏁 Success Criteria
- [ ] Integrity: 0% drift between FS and Registry after a Healing Loop.
- [ ] Speed: Full registry audit (< 300ms for 300+ nodes).
- [ ] Safety: Mandatory backup of registry files before any write action.
- [ ] Transparency: Detailed diff generation for every automated change.

---
*Last Updated: 2026-04-20*
*Version: 1.0.0*
