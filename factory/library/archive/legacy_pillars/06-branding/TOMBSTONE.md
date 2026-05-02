# TOMBSTONE — factory/library/archive/legacy_pillars/06-branding/

**Status:** DEPRECATED  
**Tombstoned:** 2026-04-25  
**Reasoning Hash:** sha256:tombstone-06-branding-2026-04-25  

---

## Why This Domain Was Deprecated

`06-branding/` was an early domain naming convention using kebab-case with numeric prefix.
It was superseded by `00_core_orchestration/` and `50_intelligence_marketing/` during
the library restructuring that standardised all domain names to `{NN}_{snake_case}` format
(AIWF v13.0+).

Branding assets and design token specs now live in:
- `factory/library/archive/legacy_pillars/00_core_orchestration/` — brand governance contracts
- `factory/library/archive/legacy_pillars/50_intelligence_marketing/` — brand intelligence and marketing assets

**File Count at Tombstone:** 0 (all assets were migrated during restructuring)  
**Empty Subdirs:** `design-tokens/` (migration artifact — content is in 00_core_orchestration/)

---

## Import/Reference Audit

Before any code references `06-branding`, it should be updated to the appropriate successor.

Run:
```bash
grep -r "06-branding" . --include="*.py" --include="*.yaml" --include="*.md"
```

---

## Governance

Per F3 tombstone_governance spec: this directory must NOT be deleted until the import audit
above returns 0 results. It must remain as a navigation marker for exactly 2 release cycles
after tombstone date, then may be hard-deleted.

**Scheduled Hard-Delete:** After AIWF v21.0 (Phase 21 completion)  
**Owner:** registry_guardian (T0 agent)
