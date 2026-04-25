# Requirements Specification — Phase 01: Discovery

**Planning Type:** content  
**Topic:** AIWF v21 Launch Content Strategy  
**Status:** APPROVED  
**Reasoning Hash:** sha256:aiwf-v21-launch-content-01-discovery-2026-04-25  

---

## 1. Functional Requirements

| ID | Requirement | Priority | Source | Acceptance Criterion |
|----|-------------|----------|--------|----------------------|
| FR-01 | Define 3–5 audience personas for AIWF v21 launch | P1 | PRD 2026_04_24 | Personas documented in domain_model.md with pain points + format prefs |
| FR-02 | Audit all existing AIWF content assets (docs/, .ai/dashboard/, README) | P1 | Workspace scan | Content audit table with quality score per asset |
| FR-03 | Map 3+ competitor content strategies (sovereign AI tools, developer platforms) | P1 | Competitive research | Competitor matrix in domain_model.md |
| FR-04 | Define content objectives tied to AIWF v21 goals (tripartite planning adoption) | P1 | v21 SDD doc | SMART objectives in requirements with KPI baseline |
| FR-05 | Identify channel priorities for launch (GitHub, LinkedIn, X, dev communities) | P2 | Audience research | Channel priority matrix with rationale |
| FR-06 | Arabic-language content requirements assessment for MENA audience | P2 | Law 151/2020 | RTL/Arabic scope decision documented |

---

## 2. Non-Functional Requirements

| ID | Requirement | Category | Measurable Target |
|----|-------------|----------|-------------------|
| NFR-01 | Discovery must complete before any content production begins | Process | Phase gate enforced |
| NFR-02 | All personas must be grounded in real signals (workspace data, community) | Quality | No fictional personas without signal source |
| NFR-03 | Competitor research must not reproduce copyrighted content | Compliance | Originality ≤15% |

---

## 3. Gherkin Acceptance Criteria

```gherkin
Feature: AIWF v21 Launch Content Discovery

  Background:
    Given the AIWF system is at v21.0.0
    And Law 151/2020 data residency is enforced for all Egyptian audience data

  Scenario: Audience persona definition
    Given the AIWF target audience spans MENA developers and AI-native founders
    When the discovery phase completes
    Then at least 3 personas are documented with name, role, pain points, and AIWF use case
    And at least 1 persona is MENA-specific with Arabic language preference noted

  Scenario: Content gap identification
    Given the existing AIWF documentation lives in docs/ and .ai/
    When the content audit runs
    Then every existing asset has a quality score (SEO, readability, brand voice)
    And gaps between current coverage and launch needs are listed in priority order

  Scenario: Channel prioritisation
    Given the launch targets developer communities and AI-adjacent audiences
    When channel research completes
    Then channels are ranked by audience fit × reach × production cost
    And GitHub README is always ranked P1 for developer-first positioning
```

---

## 4. Constraints & Boundaries

- **In Scope:** Audience research, content audit, competitor mapping, objective setting, channel prioritisation
- **Out of Scope:** Content production, scheduling, copy drafting (Phase 04)
- **External Dependencies:** Existing AIWF docs, PRD 2026-04-24, v21 SDD plan doc
- **Law 151/2020:** Egyptian user persona data must not leave Egypt; anonymise before archiving

---

## 5. Stakeholders

| Role | Name/Agent | Responsibility |
|------|------------|----------------|
| Owner | spec_architect_v2 | Phase integrity |
| Research | brainstorm_agent | Audience + competitor signals |
| Compliance | factory_orchestrator | Law 151 data handling |

---

## 6. Open Questions

- [ ] Is there a target launch date for v21.0.0 public announcement? (drives channel timing)
- [ ] Should AIWF content target Arabic-speaking developers specifically, or English-first MENA?
