# API contract — CMS + public frontend (phase 01)

**Contract type:** API / service interface  
**Version:** 1.0.0  
**Reasoning hash:** sha256:portfolio-website-content-phase01-2026-05-04  

---

## Endpoint / interface definition

```yaml
contract_id: "portfolio-cms-public-v1"
type: "rest"
version: "1.0.0"

endpoints:
  - path: "/api/v1/pages/{slug}"
    method: "GET"
    description: "Public read model for published page by slug and locale"
    auth: "none | edge-cache-key"
    law_151_applies: true
    rate_limit: "TBD req/min"

  - path: "/api/v1/drafts"
    method: "POST"
    description: "Create draft content (authenticated editor)"
    auth: "bearer"
    law_151_applies: true
```

---

## Request / response notes

- Replace paths with the real CMS (Sanity GROQ, WP REST, etc.).  
- All payloads that may include personal data must declare residency handling in regional_compliance.md.

---

## Error handling

| Code | Meaning | Recovery |
|------|---------|----------|
| 400 | Invalid slug or locale | Fix client request |
| 401 / 403 | Auth failure on mutating routes | Renew session / RBAC |
| 404 | Unpublished or missing slug | Check workflow state_contract |
