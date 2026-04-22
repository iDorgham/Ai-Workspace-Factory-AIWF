# Test Plan: [Feature / Release Name]

> **Plan ID:** `[TEST-SPRINT-N-slug]`
> **Feature plan:** `.ai/plans/active/features/[feature].md`
> **Author:** @QA
> **Status:** [draft | approved | executed]
> **Target release / sprint:** [name or date]

---

## 1. Scope

**In scope:**
- [Area or user story]
- [Area]

**Out of scope:**
- [Explicit exclusions]

---

## 2. Quality objectives

| Objective | Target |
|-----------|--------|
| Unit test coverage (changed code) | [e.g. ≥80% lines] |
| Critical path E2E | [pass / list] |
| Accessibility | [WCAG 2.1 AA — key flows] |
| RTL / i18n parity | [flows to verify] |

---

## 3. Test levels

### Unit
| Module / package | Focus | Owner |
|------------------|-------|-------|
| | | |

### Integration / contract
| Boundary | Scenarios |
|----------|-----------|
| API ↔ DB | |
| Client ↔ API | |

### E2E / manual exploratory
| Journey | Data setup | Automation (Y/N) |
|---------|------------|------------------|
| | | |

### Non-functional (if applicable)
- Performance: [budgets]
- Security: [checks — @Security]

---

## 4. Environment & data

| Environment | URL / config | Test data |
|-------------|--------------|-----------|
| Local | | |
| Staging | | |

---

## 5. Entry / exit criteria

**Entry:**
- [ ] Contract locked for touched domains
- [ ] Build green on target branch
- [ ] Feature behind flag (if applicable): [flag name]

**Exit:**
- [ ] All P0/P1 cases pass
- [ ] No open critical defects
- [ ] Sign-off: @QA + [PM/Tech lead]

---

## 6. Risks & dependencies

| Risk | Mitigation |
|------|------------|
| Flaky E2E | |

---

## 7. Execution log

| Date | Build / commit | Result | Notes |
|------|----------------|--------|-------|
| | | pass / fail | |

---

*Template: test-plan | Gate order: spec:validate → contract:auto-validate → compliance → security:scan → test → build → deploy*
