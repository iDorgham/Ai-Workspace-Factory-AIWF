# Risk Scoring (5×5 Sovereign Matrix)

## Purpose
Quantify and track project risks with a 5×5 matrix adapted for Sovereign's specific risk categories. Prevents surprises by surfacing risks before they become incidents. @RiskAgent maintains the live register.

## The 5×5 Sovereign Risk Matrix

```
LIKELIHOOD →        1-Rare  2-Unlikely  3-Possible  4-Likely  5-Almost Certain
                   ┌───────┬──────────┬───────────┬──────────┬─────────────────┐
5 - Critical       │   5   │    10    │     15    │    20    │        25       │
4 - Major          │   4   │     8    │     12    │    16    │        20       │
3 - Moderate       │   3   │     6    │      9    │    12    │        15       │
2 - Minor          │   2   │     4    │      6    │     8    │        10       │
1 - Negligible     │   1   │     2    │      3    │     4    │         5       │
                   └───────┴──────────┴───────────┴──────────┴─────────────────┘

SCORE THRESHOLDS:
  ≥20: CRITICAL — Halt sprint, immediate escalation to @EscalationHandler
  15-19: HIGH    — Mitigation plan required before sprint start
  10-14: MEDIUM  — Monitor weekly, assign owner
  5-9:   LOW     — Log and review monthly
  1-4:   MINIMAL — Accept and note
```

## Sovereign Risk Modifiers

Standard 5×5 score gets +1 to +3 modifier for Sovereign-specific factors:

```
+3: Contract drift detected (no lock = uncontrolled change)
+2: pnpm catalog violation (version inconsistency)
+2: RTL/i18n compliance failure (Arabic market exposure)
+2: Security scan finding (high/critical vulnerability)
+1: Cache hit rate <70% (CI performance risk)
+1: Coverage below threshold (quality gate risk)
+1: Single point of failure (only one person/agent knows this)
```

## Risk Register Format

```markdown
# Sovereign Risk Register — [Project Name]
Last Updated: [Date] by @RiskAgent

## Active Risks

### RISK-001 | HIGH (Score: 16)
**Title:** Stripe payment integration API changes
**Category:** External Dependency
**Likelihood:** 4 (Likely — Stripe v3 → v4 migration announced)
**Impact:** 4 (Major — breaks all payment processing)
**Sovereign Modifier:** +0
**Final Score:** 16

**Description:**
Stripe API v4 announced for Q3 2026. Current implementation uses v3. Migration required or payments will fail.

**Owner:** @Backend
**Target Resolution:** 2026-06-01

**Mitigation:**
- [ ] Abstract Stripe calls behind PaymentAdapter interface
- [ ] Pin stripe SDK version in pnpm catalog until migration
- [ ] Monitor Stripe changelog weekly (@Automation webhook)
- [ ] Migration plan in .ai/plans/backlog/stripe-v4-migration.md

**Contingency (if materializes):**
Switch to PayMob (Egyptian payment gateway) as fallback — contract already drafted.

---

### RISK-002 | MEDIUM (Score: 12)
**Title:** Contract drift during parallel execution
**Category:** Governance / Process
**Likelihood:** 3 (Possible)
**Impact:** 4 (Major — divergent implementations)
**Sovereign Modifier:** +0
**Final Score:** 12

**Description:**
When multiple agents work in parallel, a missed contract update can cause frontend and backend to implement different schemas.

**Owner:** @ContractLock
**Target Resolution:** Ongoing

**Mitigation:**
- [ ] contract:validate runs before every parallel agent start
- [ ] @ContractLock notifies all agents on contract changes
- [ ] PSR (Parallel Success Rate) tracked — alert if <88%

---

### RISK-003 | HIGH (Score: 17)
**Title:** Arabic locale display issues in production
**Category:** RTL/i18n Compliance
**Likelihood:** 4 (Likely — has occurred in similar projects)
**Impact:** 3 (Moderate — affects Arabic-speaking users)
**Sovereign Modifier:** +2 (RTL compliance)
**Final Score:** 17 → HIGH

**Owner:** @I18n
**Target Resolution:** Before staging deployment

**Mitigation:**
- [ ] RTL visual regression baselines created for all key pages
- [ ] Arabic locale E2E tests in CI
- [ ] Native Arabic speaker review before go-live
```

## Risk Review Cadence

```markdown
## Review Schedule

| Frequency  | Activity                              | Owner         |
|------------|---------------------------------------|------------
## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---
|
| Per sprint | Identify new risks for features       | @RiskAgent    |
| Weekly     | Update likelihood/impact scores       | @RiskAgent    |
| Per deploy | Re-assess CRITICAL/HIGH risks         | @RiskAgent + @Guide |
| Per retro  | Archive resolved risks, extract lessons | @RetroFacilitator |
```

## Risk Identification Triggers

```
New contract created     → Risk: contract drift if complex domain
New external dependency  → Risk: API changes, license, availability
Security finding         → Risk: immediate HIGH, +2 modifier
New payment feature      → Risk: fraud, failed payments, chargebacks
Arabic content added     → Risk: RTL regression, cultural accuracy
New agent added to swarm → Risk: coordination overhead, token bloat
Performance regression   → Risk: user abandonment (hospitality = high impact)
```

## Risk Report Format (@MetricsAgent)

```
## Risk Report — Sprint [N]
Generated: [Date]

SUMMARY:
  Critical:  [N] risks
  High:      [N] risks
  Medium:    [N] risks
  Resolved:  [N] risks this sprint

CRITICAL/HIGH DETAILS: [RISK-IDs with scores]

TREND: [Improving | Stable | Worsening]
VELOCITY IMPACT: [N sessions at risk from HIGH+ items]

RECOMMENDED ACTIONS:
1. [Action for highest risk]
2. [Action for second highest]
```

## Common Mistakes
- Scoring all risks LOW to avoid mitigation work — risks materialize without warning
- No owner assigned — unowned risks never get mitigated
- Not applying Sovereign modifiers — contract drift risk is always higher than base 5×5 suggests
- Treating risk register as one-time exercise — update every sprint
- Not linking risks to features — when feature ships, risk should close

## Success Criteria
- [ ] Risk register exists and is updated each sprint
- [ ] All risks ≥15 have owner + mitigation plan
- [ ] CRITICAL risks trigger escalation to @EscalationHandler
- [ ] New external dependencies trigger risk assessment
- [ ] Risk trend tracked by @MetricsAgent