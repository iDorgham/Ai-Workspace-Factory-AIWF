# Requirements — Phase 06: Egyptian Arabic Content Master v1.2

**Planning type:** content  
**Topic:** Skill pack v1.2 (brief-driven routing, vertical depth, Masri quality rubric)  
**Reasoning hash:** sha256:phase-06-egyptian-arabic-content-master-v12-req-2026-05-02

---

## 1. Functional requirements

| ID | Requirement | Priority | Acceptance |
|----|-------------|----------|--------------|
| FR-01 | Phase folder satisfies `spec_density_gate_v2` (≥12 files, required tops, C4, subdirs, ≥5 tasks) | P0 | `validation/density_gate_report.json` overall PASS |
| FR-02 | `contracts/brief_schema.yaml` defines minimum brief fields: `tone`, `channel`, `sector`; optional `banned_claims`, `legal_sensitivity`, `locale` | P0 | Schema committed; referenced from `design.md` |
| FR-03 | `contracts/pack_router_map.yaml` maps `(sector, channel)` → suggested `examples/` + `prompt_library/` entries (advisory, not runtime-enforced unless tooling added) | P1 | Valid YAML; ≥3 example rows |
| FR-04 | `validation/rubric_masri.md` lists scored criteria aligned with `quality_checklist.md` in the live pack | P0 | Rubric reviewed against v1.1.0 checklist |
| FR-05 | Live pack changes (when executed) bump `skill_manifest.json` to `1.2.0` and sync manifest skill.md protocols | P1 | Version fields consistent |
| FR-06 | Final handoff: `rsync` factory pack → `.ai/skills/egyptian_arabic_content_master/` | P0 | Documented exact command in `tasks.json` |

---

## 2. Non-functional

- **Law 151/2020:** Golden pairs and vertical samples contain no real PII; anonymised placeholders only.
- **Traceability:** Phase tasks reference concrete paths under `factory/library/skills/egyptian_arabic_content_master/`.

---

## 3. Out of scope (this phase)

- Automated CI enforcement of `brief_schema` at generation time (future development task).
- Replacing counsel-reviewed legal text in client deployments.
