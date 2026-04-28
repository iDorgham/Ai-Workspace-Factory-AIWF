# Requirements Specification — Phase 04: Tasks & Contracts

**Planning Type:** content | **Topic:** AIWF v21 Launch Content Strategy
**Reasoning Hash:** sha256:aiwf-v21-launch-content-04-tasks-contracts-2026-04-25

---

## 1. Functional Requirements

| ID | Requirement | Priority | Acceptance Criterion |
|----|-------------|----------|----------------------|
| FR-01 | Generate all 12 launch pieces via multi-CLI using Phase 03 briefs | P1 | 12 content files in docs/content/launch/ |
| FR-02 | Each piece passes quality gate: SEO ≥85, brand voice ≥92, readability ≥65 | P1 | Gate report per piece in validation/ |
| FR-03 | 3 Arabic pieces reviewed by native Arabic speaker before commit | P1 | Review sign-off in validation/arabic_review.md |
| FR-04 | All 12 pieces committed via sovereign commit protocol with reasoning hash | P2 | Git log shows correct commit format |
| FR-05 | production_log.md records CLI used, latency, tokens, and gate result per piece | P2 | Structured log in validation/ |

---

## 2. Gherkin Acceptance Criteria

```gherkin
Feature: AIWF v21 Content Production

  Scenario: Multi-CLI content generation
    Given 12 content briefs from Phase 03
    When each brief is executed via prompt_library/ prompts
    Then all 12 pieces are produced with no TODO_P_L_A_C_E_H_O_L_D_E_R strings remaining
    And the CLI used for each piece is logged in tool_performance.jsonl

  Scenario: Quality gate enforcement
    Given a produced content piece
    When the quality gate runs
    Then pieces scoring SEO <85 are flagged for revision
    And no piece with brand voice <92 is committed to the repository
```

---

## 3. Open Questions
- [ ] Which CLI produces best Arabic output: Qwen or Claude? (Run comparison in T-C04-01)
- [ ] Does production_log.md feed back into tool_performance.jsonl automatically?
