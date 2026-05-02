# Requirements Specification — {{PHASE_NAME}}

**Phase:** {{PHASE_NUMBER}} — {{PHASE_NAME}}  
**Planning Type:** {{PLANNING_TYPE}}  
**Topic:** {{TOPIC}}  
**Status:** DRAFT  
**Reasoning Hash:** {{REASONING_HASH}}  
**Timestamp:** {{ISO_TIMESTAMP}}  

---

## 1. Functional Requirements

| ID | Requirement | Priority | Source | Acceptance Criterion |
|----|-------------|----------|--------|----------------------|
| FR-01 | {{REQUIREMENT_1}} | P1 | {{SOURCE}} | {{AC}} |
| FR-02 | {{REQUIREMENT_2}} | P1 | {{SOURCE}} | {{AC}} |
| FR-03 | {{REQUIREMENT_3}} | P2 | {{SOURCE}} | {{AC}} |

---

## 2. Non-Functional Requirements

| ID | Requirement | Category | Measurable Target |
|----|-------------|----------|-------------------|
| NFR-01 | {{NFR_1}} | Performance | {{TARGET}} |
| NFR-02 | {{NFR_2}} | Security | {{TARGET}} |
| NFR-03 | {{NFR_3}} | Compliance | Law 151/2020 |

---

## 3. Gherkin Acceptance Criteria

```gherkin
Feature: {{FEATURE_NAME}}
  Background:
    Given the AIWF system is operating under OMEGA Gate v3
    And Law 151/2020 data residency is enforced

  Scenario: {{SCENARIO_1}}
    Given {{CONTEXT}}
    When {{ACTION}}
    Then {{EXPECTED_OUTCOME}}
    And {{SECONDARY_OUTCOME}}

  Scenario: {{SCENARIO_2}}
    Given {{CONTEXT}}
    When {{ACTION}}
    Then {{EXPECTED_OUTCOME}}
```

---

## 4. Constraints & Boundaries

- **In Scope:** {{IN_SCOPE}}
- **Out of Scope:** {{OUT_OF_SCOPE}}
- **External Dependencies:** {{EXTERNAL_DEPS}}
- **Law 151/2020 Constraints:** Data processed in Egypt/MENA; no offshore residency for personal data

---

## 5. Stakeholders

| Role | Name/Agent | Responsibility |
|------|------------|----------------|
| Owner | spec_architect_v2 | Plan integrity |
| Executor | {{AGENT_NAME}} | Implementation |
| Reviewer | factory_orchestrator | Quality gate |

---

## 6. Open Questions

- [ ] {{OPEN_QUESTION_1}}
- [ ] {{OPEN_QUESTION_2}}

_Resolve before phase-03 begins._
