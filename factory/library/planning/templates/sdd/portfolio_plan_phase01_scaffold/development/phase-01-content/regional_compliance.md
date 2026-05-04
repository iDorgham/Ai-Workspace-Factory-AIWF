# Regional compliance — Law 151/2020 + Arabic content (phase 01)

**Law:** Egypt Law 151/2020 on Personal Data Protection  
**Phase:** 01 — Content — portfolio foundation  
**Planning type:** content  
**Compliance status:** PENDING REVIEW  
**Reasoning hash:** sha256:portfolio-website-content-phase01-2026-05-04  
**Timestamp:** 2026-05-04  

---

## 1. Data residency assessment

| Data type | Storage location | Processing location | Law 151 compliant | Notes |
|-----------|------------------|----------------------|-------------------|--------|
| Public marketing copy | TBD | TBD | Review | No personal data |
| Contact / lead forms | TBD | TBD | Review | Consent + purpose limitation |
| Analytics | TBD | TBD | Review | Prefer EU/Egypt-approved processors or self-host |

**Rule:** Personal data of Egyptian subjects must be processed and stored within Egypt or an approved jurisdiction; transfers need lawful basis + documentation.

---

## 2. MENA adaptations

- **Arabic language:** required for public-facing parity where PRD states  
- **RTL layout:** required for Arabic routes  
- **Cultural sensitivity:** review imagery and idioms for dual-language site  

---

## 3. Geofencing (if applicable)

```yaml
geofence:
  primary_region: egypt
  allowed_regions: [egypt, uae, ksa, jordan, kuwait]
  enforcement: "document in hosting choice"
```

---

## 4. Compliance checklist

- [ ] Personal data categories listed (forms, newsletters, analytics)  
- [ ] Storage + subprocessors documented with regions  
- [ ] Cookie / consent UX aligned with policy pages  
- [ ] Arabic content parity and RTL verified in acceptance tests  

---

## 5. Open compliance actions

- [ ] DPA with CMS / hosting vendors  
- [ ] Retention schedule for leads and logs  
