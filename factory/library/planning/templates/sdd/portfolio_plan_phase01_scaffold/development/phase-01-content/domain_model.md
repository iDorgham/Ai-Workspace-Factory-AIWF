# Domain model — phase 01 (content)

**Planning type:** content  
**Reasoning hash:** sha256:portfolio-website-content-phase01-2026-05-04  

---

## 1. Core entities

| Entity | Description | Attributes | Relationships |
|--------|-------------|------------|----------------|
| Page | Routable portfolio surface | slug, locale, status, seo_title | belongs to Section; has many Blocks |
| Block | Reusable content slice | type, payload JSON, order | belongs to Page |
| MediaAsset | Image / file | url, alt, focal, law_151_region | referenced by Block |
| Author | Human actor | id, role | creates Page versions |
| Publication | Immutable snapshot | version, published_at | of Page |

---

## 2. Domain schema (illustrative)

```json
{
  "Page": {
    "id": "uuid",
    "slug": "string",
    "locale": "en | ar",
    "status": "draft | review | approved | published",
    "law_151_region": "egypt | mena | global"
  }
}
```

---

## 3. State machine (editorial)

```
[DRAFT] → (submit) → [REVIEW] → (approve) → [APPROVED] → (publish) → [PUBLISHED]
              ↓ reject              ↓
           [DRAFT]              [DRAFT]
```

---

## 4. Invariants

- Published pages must reference approved Publication version only.  
- Personal data fields (forms) carry `law_151_region` and retention per regional_compliance.md.  
- Arabic and English pages share stable slug strategy documented in PRD.

---

## 5. Glossary

| Term | Definition |
|------|------------|
| Publication | Immutable content snapshot visible to public visitors |
| Block | CMS-level reusable unit (hero, gallery, rich text, etc.) |
