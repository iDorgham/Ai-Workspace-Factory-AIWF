# State contract — editorial + release (phase 01)

**Contract type:** State / workflow  
**Reasoning hash:** sha256:portfolio-website-content-phase01-2026-05-04  

---

## State definitions

```yaml
states:
  - id: "DRAFT"
    description: "Author working copy"
    allowed_transitions: ["REVIEW", "DELETED"]
    owner: "author"

  - id: "REVIEW"
    description: "Editorial QA"
    allowed_transitions: ["APPROVED", "DRAFT"]

  - id: "APPROVED"
    description: "Ready for publish pipeline"
    allowed_transitions: ["PUBLISHED", "DRAFT"]
    prerequisite: "content_contract gates met"

  - id: "PUBLISHED"
    description: "Live on public site"
    allowed_transitions: ["ARCHIVED"]

  - id: "ARCHIVED"
    description: "Removed from nav; may redirect"
    allowed_transitions: []

  - id: "DELETED"
    description: "Soft-delete tombstone"
    allowed_transitions: []
```

---

## Transition guards

| Transition | Guard |
|------------|--------|
| REVIEW → APPROVED | Checklist in validation/audit_checklist.md |
| APPROVED → PUBLISHED | Build succeeds; no density gate regressions on linked plan |
| Any → involving personal data | Law 151 checklist in regional_compliance.md |

---

## Mapping to technical flags

Document CMS-specific status fields here when the stack is chosen (e.g. Sanity `draft` vs `published`).
