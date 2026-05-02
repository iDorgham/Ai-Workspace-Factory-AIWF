# Audit Checklist — {{PHASE_NAME}}

**Phase:** {{PHASE_NUMBER}} — {{PHASE_NAME}}  
**Planning Type:** {{PLANNING_TYPE}}  
**Auditor Agent:** factory_orchestrator  
**Reasoning Hash:** {{REASONING_HASH}}  

---

## 1. Structural Density Gate

- [ ] Phase folder contains ≥ 12 spec files (run `spec_density_gate_v2.py`)
- [ ] `phase.spec.json` present and valid JSON
- [ ] `requirements.spec.md` present
- [ ] `design.md` present
- [ ] `c4-context.mmd` present and renders without error
- [ ] `c4-containers.mmd` present and renders without error
- [ ] `domain_model.md` present
- [ ] `task_graph.mmd` present
- [ ] `tasks.json` present with ≥ 5 tasks
- [ ] `contracts/` has ≥ 3 files
- [ ] `templates/` has ≥ 1 file
- [ ] `validation/` has ≥ 2 files
- [ ] `regional_compliance.md` present
- [ ] `prompt_library/` has ≥ 2 files

**Density Gate Result:** [ ] PASS / [ ] FAIL

---

## 2. C4 Diagram Quality

- [ ] Context diagram ≤ 25 elements total
- [ ] Container diagram ≤ 30 elements total
- [ ] All elements have: Name + Technology + 1-line description
- [ ] All arrows: unidirectional, action-verb labels
- [ ] No orphan nodes

**C4 Quality Result:** [ ] PASS / [ ] FAIL

---

## 3. Acceptance Criteria (from requirements.spec.md)

| AC ID | Criterion | Status |
|-------|-----------|--------|
| AC-01 | {{CRITERION_1}} | [ ] PASS / [ ] FAIL |
| AC-02 | {{CRITERION_2}} | [ ] PASS / [ ] FAIL |

---

## 4. Law 151/2020 Compliance

- [ ] `regional_compliance.md` fully completed
- [ ] All personal data flows identified
- [ ] Storage locations confirmed as Egypt/approved MENA
- [ ] SOVEREIGN_COMPLIANCE_CERTIFICATE generated

**Law 151 Result:** [ ] CERTIFIED / [ ] BLOCKED

---

## 5. Traceability Matrix

| Requirement | Design Ref | Task Ref | Test Ref |
|-------------|------------|----------|----------|
| FR-01 | design.md#§{{N}} | T-{{PHASE_NUM}}-01 | AC-01 |
| FR-02 | design.md#§{{N}} | T-{{PHASE_NUM}}-02 | AC-02 |

---

## Final Verdict

**[ ] APPROVED FOR ACTIVATION** — All gates passed.  
**[ ] BLOCKED** — See failures above. Fix and re-run before phase activates.

_Signed by: factory_orchestrator | {{ISO_TIMESTAMP}}_
