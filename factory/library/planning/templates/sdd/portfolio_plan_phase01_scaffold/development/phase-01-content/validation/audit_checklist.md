# Audit checklist — phase 01 content

**Phase:** 01 — Content — portfolio foundation  
**Planning type:** content  
**Auditor:** factory_orchestrator (or human reviewer)  
**Reasoning hash:** sha256:portfolio-website-content-phase01-2026-05-04  

---

## 1. Structural density gate

- [ ] Phase folder contains ≥ 12 spec files (`spec_density_gate_v2.py`)  
- [ ] `phase.spec.json` valid JSON  
- [ ] `requirements.spec.md` present  
- [ ] `design.md` present  
- [ ] `c4-context.mmd` + `c4-containers.mmd` render  
- [ ] `domain_model.md` present  
- [ ] `task_graph.mmd` present  
- [ ] `tasks.json` with ≥ 5 tasks  
- [ ] `contracts/` ≥ 3 files  
- [ ] `templates/` ≥ 1 file  
- [ ] `validation/` ≥ 2 files  
- [ ] `regional_compliance.md` present  
- [ ] `prompt_library/` ≥ 2 files  

**Density gate result:** [ ] PASS / [ ] FAIL  

---

## 2. C4 quality

- [ ] Context diagram ≤ 25 elements  
- [ ] Container diagram ≤ 30 elements  
- [ ] Labels use action verbs on relationships  

**C4 quality result:** [ ] PASS / [ ] FAIL  

---

## 3. Acceptance criteria (from phase.spec + requirements)

| AC ID | Criterion | Status |
|-------|-----------|--------|
| AC-01 | PRD/roadmap/context linked and coherent | ⏳ |
| AC-02 | C4 matches design baseline | ⏳ |
| AC-03 | Contracts + regional complete | ⏳ |

---

## 4. Content / brand spot checks

- [ ] content_contract.yaml block matches live editorial policy  
- [ ] Image alt and SEO rules smoke-tested on one template page  

---

## AC anchors for tooling

`#AC-01` `#AC-02` `#AC-03` — keep IDs stable for `test_ref` in phase.spec.json.
