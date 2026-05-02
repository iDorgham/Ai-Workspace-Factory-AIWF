# Regional compliance — Law 151/2020 & MENA-soil

**Phase:** 06 — Egyptian Arabic Content Master v1.2  
**Applies to:** Example copy, golden pairs, vertical stubs, any user-like data in artifacts.

---

## Rules

1. **No real personal data** in `validation/` golden examples or `templates/` — use fictional names and generic locations unless client provides approved public copy.
2. **Data residency framing:** Skill text may reference Egypt/MENA audiences; do not assert specific hosting certifications unless sourced from approved infra docs.
3. **Legal-adjacent copy:** Marketing summaries only; defer binding language to counsel (`legal_and_contracts_guidance.md` in live pack).
4. **Logging:** If KPI or tooling logs briefs, strip PII before writing to shared logs.

## Checklist (before promoting phase)

- [ ] All sample Arabic strings are synthetic or anonymised.  
- [ ] No live API keys, phone numbers, or national IDs in YAML/Markdown.  
- [ ] `golden_pairs.jsonl` (when added to factory) reviewed for Law 151.

---

**Certification note:** Phase satisfies `regional_compliance.md` presence for v21 density gate; legal certification for production systems remains a separate governance action.
