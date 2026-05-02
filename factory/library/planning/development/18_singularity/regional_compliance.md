# Regional Compliance — {{PHASE_NAME}}

**Law:** Egypt Law 151/2020 on Personal Data Protection  
**Phase:** {{PHASE_NUMBER}} — {{PHASE_NAME}}  
**Planning Type:** {{PLANNING_TYPE}}  
**Compliance Status:** PENDING REVIEW  
**Reasoning Hash:** {{REASONING_HASH}}  
**Timestamp:** {{ISO_TIMESTAMP}}  

---

## 1. Data Residency Assessment

| Data Type | Storage Location | Processing Location | Law 151 Compliant | Notes |
|-----------|-----------------|---------------------|-------------------|-------|
| {{DATA_TYPE_1}} | Egypt / MENA | Egypt | ✅ Yes | — |
| {{DATA_TYPE_2}} | {{LOCATION}} | {{LOCATION}} | ⚠️ Review | {{NOTE}} |

**Rule:** Personal data of Egyptian subjects must be processed and stored within Egypt or a country with equivalent protections. Cross-border transfer requires explicit consent + DPA approval.

---

## 2. MENA Adaptations

- **Arabic Language:** {{ARABIC_SUPPORT_REQUIRED: yes/no}}
- **RTL Layout:** {{RTL_REQUIRED: yes/no}}  
- **Local Payment Methods:** {{MENA_PAYMENT_REQUIRED: yes/no}}
- **Cultural Sensitivity Review:** {{REVIEW_DATE}}

---

## 3. Geofencing Rules

```yaml
geofence:
  primary_region: egypt
  allowed_regions: [egypt, uae, ksa, jordan, kuwait]
  blocked_regions: [{{BLOCKED_REGIONS}}]
  enforcement: OMEGA_GATE_V3
```

---

## 4. Compliance Checklist

- [ ] All personal data identified and classified
- [ ] Storage locations confirmed as Egypt/approved MENA
- [ ] Cross-border transfer consent documented (if any)
- [ ] OMEGA Gate v3 sovereignty certificate generated
- [ ] DPA (Data Processing Agreement) in place for any third parties

---

## 5. Certification

Once all checklist items are complete, generate:

```bash
python factory/scripts/core/omega_release.py --generate-cert --phase {{PHASE_ID}}
```

Output: `SOVEREIGN_COMPLIANCE_CERTIFICATE_{{PHASE_ID}}.md`
