# Incident Runbook: [Service / area name]

> **Runbook ID:** `[RB-incident-type]`
> **Severity model:** [P1 user-down | P2 major degradation | P3 minor | P4 cosmetic]
> **Last reviewed:** [YYYY-MM-DD]
> **Owner:** [team / on-call]

---

## 1. Detection

**Symptoms:** [What users or monitors see]

**Alerts / dashboards:** [links or names]

---

## 2. Impact assessment

- **Scope:** [% users, regions, tenants]
- **Data:** [risk to integrity / PII exposure — @Security if yes]
- **SLA:** [internal targets]

---

## 3. Immediate actions (first 15 minutes)

1. [Acknowledge incident — channel / tool]
2. [Stabilize — e.g. scale, circuit break, disable feature flag]
3. [Assign incident commander]

---

## 4. Diagnosis

| Check | Command / location | Healthy signal |
|-------|-------------------|----------------|
| Health endpoint | | |
| DB connectivity | | |
| Queue depth | | |
| Recent deploy | | |

---

## 5. Mitigation options

| Option | When to use | Tradeoff |
|--------|-------------|----------|
| [e.g. Failover] | | |
| [e.g. Rollback to version X] | | |

**Rollback steps:** [ordered, with links to deploy docs]

---

## 6. Communication

| Audience | Channel | Template owner |
|----------|---------|----------------|
| Internal | | |
| Customers | | |

---

## 7. Post-incident

- [ ] **Root cause** documented (blameless)
- [ ] **Timeline** in audit or postmortem doc
- [ ] **Action items** with owners — link to tasks
- [ ] **Update this runbook** if process changed

---

## Related

- Escalation: `.ai/templates/escalation.md`
- SBAR: `.ai/plans/active/audit/escalations/`

---

*Template: incident-runbook | @Security for data breach class incidents*
