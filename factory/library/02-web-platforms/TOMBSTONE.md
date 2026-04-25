# TOMBSTONE — factory/library/02-web-platforms/

**Status:** DEPRECATED  
**Tombstoned:** 2026-04-25  
**Reasoning Hash:** sha256:tombstone-02-web-platforms-2026-04-25  

---

## Why This Domain Was Deprecated

`02-web-platforms/` was an early domain naming convention using kebab-case with numeric prefix.
It was superseded by `30_web_platforms/` during the library restructuring that standardised
all domain names to `{NN}_{snake_case}` format (AIWF v13.0+).

**Successor Domain:** `factory/library/30_web_platforms/`  
**File Count at Tombstone:** 0 (all assets were migrated to 30_web_platforms during restructuring)  
**Empty Subdirs:** `sovereign-ui/` (migration artifact — content is in 30_web_platforms/03_ui_components/)

---

## Import/Reference Audit

Before any code references `02-web-platforms`, it should be updated to `30_web_platforms`.

Run:
```bash
grep -r "02-web-platforms" . --include="*.py" --include="*.yaml" --include="*.md"
```

---

## Governance

Per F3 tombstone_governance spec: this directory must NOT be deleted until the import audit
above returns 0 results. It must remain as a navigation marker for exactly 2 release cycles
after tombstone date, then may be hard-deleted.

**Scheduled Hard-Delete:** After AIWF v21.0 (Phase 21 completion)  
**Owner:** registry_guardian (T0 agent)
