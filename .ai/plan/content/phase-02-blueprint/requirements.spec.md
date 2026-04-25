# Requirements Specification — Phase 02: Blueprint

**Planning Type:** content | **Topic:** AIWF v21 Launch Content Strategy  
**Reasoning Hash:** sha256:aiwf-v21-launch-content-02-blueprint-2026-04-25  

---

## 1. Functional Requirements

| ID | Requirement | Priority | Acceptance Criterion |
|----|-------------|----------|----------------------|
| FR-01 | Define 4-pillar content architecture with 3 content types per pillar | P1 | Pillar map in domain_model.md |
| FR-02 | Build 30-day content calendar skeleton (week-by-week, channel-assigned) | P1 | Calendar table covering launch window |
| FR-03 | Write AIWF v21 brand narrative: positioning statement + 3 proof points | P1 | brand_narrative.md in contracts/ |
| FR-04 | Define content sequencing logic: what publishes first, why | P2 | Sequence rationale in design.md |
| FR-05 | Identify content formats per channel (long-form, thread, README, diagram) | P2 | Format spec in channel_contract.md |

---

## 2. Gherkin Acceptance Criteria

```gherkin
Feature: AIWF v21 Content Blueprint

  Scenario: Pillar architecture definition
    Given 4 personas from Phase 01 (Sovereign Builder, Pragmatic Dev, MENA Pioneer, AI Director)
    When the content blueprint is complete
    Then each of the 4 pillars maps to at least 1 persona
    And each pillar has 3 distinct content type examples

  Scenario: Launch calendar
    Given a 30-day launch window starting at v21 public announcement
    When the calendar is drafted
    Then GitHub README updates are scheduled for Day 1
    And LinkedIn launch post is Day 1 or Day 2
    And X thread series begins Day 1
    And first Arabic MENA piece is within the first 2 weeks
```

---

## 3. Open Questions

- [ ] Confirm v21 public announcement date (drives Day 1 of calendar)
- [ ] Founder (Dorgham) voice: LinkedIn posts written in 1st person? Or brand account?
