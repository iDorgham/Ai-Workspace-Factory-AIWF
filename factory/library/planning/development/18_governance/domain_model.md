# Domain Model — {{PHASE_NAME}}

**Planning Type:** {{PLANNING_TYPE}}  
**Reasoning Hash:** {{REASONING_HASH}}  

> Adapt this template per planning type:
> - **development**: schemas, entity relationships, state machines
> - **content/branding**: content pillars, voice clusters, persona matrices
> - **marketing/seo**: channel matrices, keyword clusters, funnel models
> - **business**: financial models, OKR trees, strategy maps
> - **media**: asset taxonomy, production lifecycle, distribution model
> - **social_media**: platform strategies, engagement loops, content cadence

---

## 1. Core Entities / Concepts

| Entity | Description | Attributes | Relationships |
|--------|-------------|------------|---------------|
| {{ENTITY_1}} | {{DESCRIPTION}} | {{ATTRS}} | {{RELS}} |
| {{ENTITY_2}} | {{DESCRIPTION}} | {{ATTRS}} | {{RELS}} |
| {{ENTITY_3}} | {{DESCRIPTION}} | {{ATTRS}} | {{RELS}} |

---

## 2. Domain Schema (for development type)

```json
{
  "{{ENTITY_1}}": {
    "id": "string (uuid)",
    "{{FIELD_1}}": "{{TYPE}}",
    "{{FIELD_2}}": "{{TYPE}}",
    "created_at": "ISO8601",
    "law_151_region": "egypt|mena|global"
  }
}
```

_For non-development types, replace with content pillars, keyword clusters, or financial models as appropriate._

---

## 3. State Machine / Lifecycle

```
[DRAFT] → (review) → [REVIEW] → (approve) → [APPROVED] → (activate) → [ACTIVE]
                                                            ↓
                                                       (reject) → [REJECTED]
[ACTIVE] → (complete) → [COMPLETED]
[ACTIVE] → (deprecate) → [DEPRECATED → TOMBSTONED]
```

---

## 4. Constraints & Invariants

- `{{INVARIANT_1}}`
- `{{INVARIANT_2}}`
- Law 151/2020: Personal data entities must carry `law_151_region` field; offshore region forbidden

---

## 5. Glossary

| Term | Definition | Canonical Slug |
|------|------------|----------------|
| {{TERM_1}} | {{DEFINITION}} | `{{slug}}` |
| {{TERM_2}} | {{DEFINITION}} | `{{slug}}` |
