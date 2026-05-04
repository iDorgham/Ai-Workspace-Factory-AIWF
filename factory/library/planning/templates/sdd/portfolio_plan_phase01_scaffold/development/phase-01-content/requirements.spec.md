# Requirements specification — phase 01 (content)

**Phase:** 01 — Content — portfolio foundation  
**Planning type:** content  
**Topic:** Ezzat Gamaly — portfolio website (public site + CMS)  
**Status:** DRAFT  
**Reasoning hash:** sha256:portfolio-website-content-phase01-2026-05-04  
**Timestamp:** 2026-05-04  

**Human inputs (fill first):** [docs/product/PRD.md](../../../../docs/product/PRD.md) · [docs/product/ROADMAP.md](../../../../docs/product/ROADMAP.md) · [docs/overview/CONTEXT.md](../../../../docs/overview/CONTEXT.md)

---

## 1. Functional requirements

| ID | Requirement | Priority | Source | Acceptance criterion |
|----|-------------|----------|--------|------------------------|
| FR-01 | Public portfolio pages load core IA (home, work, about, contact) | P1 | PRD | All routes listed in PRD return 200 with agreed content blocks |
| FR-02 | CMS authors can create, edit, and schedule content per content contract | P1 | PRD | Role-based draft → review → publish flow documented and testable |
| FR-03 | Media assets respect image SEO and brand voice gates | P2 | content_contract.md | checklist in validation/audit_checklist.md passes |

---

## 2. Non-functional requirements

| ID | Requirement | Category | Measurable target |
|----|-------------|----------|---------------------|
| NFR-01 | First contentful experience | Performance | LCP target set in PRD (mobile) |
| NFR-02 | Data handling | Security / Law 151 | No personal data offshore; see regional_compliance.md |
| NFR-03 | Bilingual readiness | Compliance | Arabic + English handling per regional_compliance.md |

---

## 3. Gherkin acceptance criteria

```gherkin
Feature: Portfolio content governance
  Background:
    Given the site is governed by SDD phase-01-content
    And Law 151/2020 applies to Egyptian data subjects

  Scenario: Publish only after review
    Given a draft page exists in the CMS
    When the author submits for review
    Then an editor can approve or reject with audit trail

  Scenario: Public site reflects approved content
    Given a page is approved for publish
    When the publish job completes
    Then the public site shows the approved version within SLA in PRD
```

---

## 4. Constraints and boundaries

- **In scope:** Editorial model, contracts, C4 for site + CMS, phase-01 tasks.  
- **Out of scope:** Implementation code (later `/dev` phases unless explicitly promoted).  
- **External dependencies:** GitHub repo, hosting, CMS vendor — list in docs/context.  
- **Law 151/2020:** Personal data processed/stored per regional_compliance.md.

---

## 5. Stakeholders

| Role | Responsibility |
|------|----------------|
| Owner | spec_architect_v2 — plan integrity |
| Client | Ezzat Gamaly — approvals and brand |
| Executor | TBD — implementation in later phase |

---

## 6. Open questions

- [ ] Final CMS choice and headless vs embedded admin  
- [ ] Exact Arabic/English URL and SEO strategy  
- [ ] Analytics and consent tooling (document in api_contract / state)
