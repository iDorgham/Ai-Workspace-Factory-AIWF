# Design — Phase 06: Egyptian Arabic Content Master v1.2

**Reasoning hash:** sha256:phase-06-egyptian-arabic-content-master-v12-design-2026-05-02

---

## 1. Pack layout (target factory state)

After implementation, the factory pack gains (conceptually):

```
factory/library/skills/egyptian_arabic_content_master/
├── contracts/                    # NEW — brief_schema.yaml, pack_router_map.yaml (copied from this phase or symlinked by policy)
├── evaluation/                   # OPTIONAL v1.2 — rubric_masri.md, golden_pairs.jsonl
├── verticals/                    # OPTIONAL v1.2 — <sector>.md stubs from templates/vertical_stub.md
├── ... (existing v1.1.0 files unchanged unless bumped)
```

**This phase** owns the **authoritative copy** under `.ai/plan/content/phase-06-egyptian-arabic-content-master-v12/contracts/` until tasks promote content into `factory/`.

---

## 2. Load order (agent guidance)

1. `egyptian_arabic_content_master.md` (persona)  
2. `tone_matrix.md` → `channel_formats.md`  
3. If brief lists `sector` + `channel`, merge hints from `pack_router_map.yaml`  
4. Pick `prompt_library/user_*.md` / `examples/` per brief  
5. Run mental QA against `validation/rubric_masri.md` (and live `quality_checklist.md`)

---

## 3. Sync contract

- **Source of truth for skill markdown:** `factory/library/skills/egyptian_arabic_content_master/`  
- **Runtime mirror:** `.ai/skills/egyptian_arabic_content_master/`  
- **Final task in `tasks.json`:** one-line `rsync` (see tasks).

This would auto-sync to `factory/library/` per Outbound Mirror Protocol when implementation tasks complete.
