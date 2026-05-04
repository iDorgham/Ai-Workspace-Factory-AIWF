# Design document — phase 01 (content)

**Phase:** 01 — Content — portfolio foundation  
**Planning type:** content  
**Reasoning hash:** sha256:portfolio-website-content-phase01-2026-05-04  
**Timestamp:** 2026-05-04  

> C4: context + containers are mandatory. Tie narrative to the **design pack** you selected during onboarding (see `docs/guides/ONBOARDING.md`).

---

## 1. System context (C4 level 1)

See `c4-context.mmd`.

**Narrative:** Visitors and editors interact with a portfolio system bounded by a public site and a CMS. External systems include GitHub, hosting, and optional analytics — each relationship labeled in the diagram.

---

## 2. Container architecture (C4 level 2)

See `c4-containers.mmd`.

**Narrative:** Replace placeholder technologies with your stack (e.g. Next.js app, headless CMS, CDN). Each container owns one clear responsibility.

### Container inventory

| Container | Technology (placeholder) | Responsibility |
|-----------|-------------------------|----------------|
| Public site | TBD (e.g. Next.js) | Render portfolio pages, SEO, i18n surface |
| CMS / content API | TBD (e.g. Sanity / WP REST) | Authoring, drafts, publish pipeline |
| Asset pipeline | TBD (e.g. CDN + image optimizer) | Images and media per content contract |

---

## 3. Component design (C4 level 3)

_Defer to a later phase unless you intentionally scope UI components here._

---

## 4. Data flow

```
Author → [CMS write] → Draft store
Editor → [approve] → Published store
Published store → [build / ISR] → Public site
Visitor → [read] → CDN / edge
```

---

## 5. Key design decisions

| Decision | Options | Chosen | Rationale |
|----------|---------|--------|-----------|
| CMS | Headless vs monolith | TBD | Record in PRD + api_contract |
| i18n | Subpath vs domain | TBD | SEO + Law 151 copy handling |

---

## 6. Design risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Scope creep into build before specs pass | Medium | High | Keep phase-01 plan-only until density gate passes |
| RTL / Arabic layout regressions | Medium | High | Lock design tokens + component notes in chosen design.md pack |
