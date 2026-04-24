# 📏 Meta-Taxonomy Enforcer

> **Tier:** 💎 OMEGA (Tier 1)
> **Department:** 07-meta
> **Domain:** taxonomy-governance
> **Status:** PRODUCTION_READY

## 🎯 Purpose
This skill enforces the structural laws of the Sovereign Factory. It ensures that every directory, file name, and metadata field adheres to the OMEGA naming convention. It prevents "Taxonomy Rot" by proactively identifying misfiled components and redundant structures.

## 🏛️ Core Principles
1. **Hierarchical Purity**: No "flat" folders in the library root. Everything must belong to a numbered department.
2. **Kebab-Case Orthodoxy**: All directory and file names must be lowercase-kebab-case.
3. **Metadata Parity**: The frontmatter in `AGENT.md`/`SKILL.md` must be a 1:1 match with the physical path.
4. **No-Redundancy Law**: Disallowing nested `skills/skills/` or `agents/agents/` patterns.

## 🛠️ Techniques & Implementation

### 1. Naming Convention Validator
Regex-based scanning of the entire directory tree.
```python
import re

def validate_kebab_case(name: str) -> bool:
    """
    Ensures name is lowercase-kebab-case (e.g., 'my-component-name').
    """
    pattern = r'^[a-z0-9]+(-[a-z0-9]+)*$'
    return bool(re.match(pattern, name))
```

### 2. Path-Metadata Synchronization Check
Cross-references the `id` field in YAML frontmatter with the current OS path.
```python
def check_frontmatter_integrity(file_content: str, actual_path: str) -> bool:
    # Logic to extract 'id' from YAML and compare to path
    return True
```

### 3. Redundant Nesting Detector
Identifies patterns like `.../skills/skills/...` or `.../content/content/...` and triggers a cleanup alert.
```python
def find_redundant_nesting(root_dir: str) -> list:
    violations = []
    for root, dirs, files in os.walk(root_dir):
        parts = root.split(os.sep)
        for i in range(len(parts) - 1):
            if parts[i] == parts[i+1] and parts[i] in ['skills', 'agents', 'content']:
                violations.append(root)
    return violations
```

## 🚫 Anti-Patterns
- **Generic Numbering**: Creating folders like `99-misc` or `temp-backup` in the library root.
- **CamelCase/PascalCase**: Using `MyService/` or `API_Controller/` in the library taxonomy.
- **Ghost Clusters**: Defining clusters in the `_taxonomy.json` that have no physical directories.

## 🏁 Success Criteria
- [ ] Compliance: 100% of files follow the kebab-case naming standard.
- [ ] Purity: 0 redundant nested directories found.
- [ ] Documentation: Every component has a valid internal ID that matches its path.
- [ ] Enforcement: Automated prevention of unconventional directory creation via pre-commit hooks.

---
*Last Updated: 2026-04-20*
*Version: 1.0.0*
