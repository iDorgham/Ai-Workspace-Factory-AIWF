# Blameless Escalation (SBAR Format)

## Purpose
When any agent is blocked, a conflict exists, or a decision exceeds an agent's authority, escalate using the SBAR format. Blameless means we fix processes, not people. Escalation is a sign of good judgment, not failure.

## When to Escalate

```
MUST escalate:
- Blocked >15 minutes with no clear resolution path
- Two agents disagree on architectural approach
- Contract change required mid-sprint
- Security vulnerability discovered
- Feature scope would exceed sprint capacity
- External dependency unavailable (payment provider, API)

DO NOT escalate:
- Questions you can answer by reading context files
- Minor implementation decisions within your domain
- Standard test failures (fix them)
```

## SBAR Format

```markdown
---
ESCALATION: [Short Title]
Severity: CRITICAL | HIGH | MEDIUM | LOW
From: @[AgentName]
To: @EscalationHandler
Timestamp: [ISO 8601]
Feature: [feature-name]
Plan Step: [X.Y]
---

## Situation
[What is happening RIGHT NOW — 1-2 sentences, present tense]

## Background
[Relevant context: what were you doing, what changed, what was expected]

## Assessment
[Impact: what happens if this is NOT resolved? Include timeline impact]

## Recommendation
[Specific options with trade-offs. Recommend one. Include estimated effort]
```

## Severity Levels & SLA

```
CRITICAL (≤15 min response)
  - Production down or data loss risk
  - Security vulnerability in deployed code
  - Blocked all sprint work (all agents blocked)
  - Data migration failure

HIGH (≤1 hour response)
  - Blocked critical path (2+ agents blocked)
  - Contract breaking change needed
  - External service outage affecting feature
  - Test environment unavailable

MEDIUM (≤4 hours response)
  - Single agent blocked
  - Architectural disagreement
  - Scope creep request
  - Non-critical dependency unavailable

LOW (≤24 hours response)
  - Process improvement suggestion
  - Technical debt discussion
  - Tool/library decision
  - Documentation gap
```

## Real Escalation Examples

### Example 1: Contract Breaking Change (HIGH)
```markdown
---
ESCALATION: Payment contract breaking change required
Severity: HIGH
From: @Backend
To: @EscalationHandler
Timestamp: 2026-04-08T14:30:00Z
Feature: booking-payment-flow
Plan Step: 3.4
---

## Situation
Stripe requires a `payment_intent_id` field on all payment records that was not included in the locked payment.ts contract (v1.0).

## Background
Implementing POST /api/payments/create-intent (Step 3.4). Stripe API response includes `payment_intent_id` which must be stored for webhook reconciliation and refunds. This field is absent from the current PaymentSchema.

## Assessment
Cannot proceed with Stripe integration without this field. All downstream steps (Step 3.5 webhook handler, 3.6 refund flow) also depend on it. Impact: 2-session delay if contract cannot be updated today.

## Recommendation
Option A (Recommended): Add `stripePaymentIntentId` to PaymentSchema as optional string.
  - @Architect updates + re-locks payment.ts
  - No breaking change to existing data (nullable)
  - Effort: 30 min

Option B: Store in separate payment_metadata table (no contract change)
  - More complex, no real benefit
  - Effort: 2 hours
```

### Example 2: Architectural Disagreement (MEDIUM)
```markdown
---
ESCALATION: REST vs tRPC API decision blocking booking module
Severity: MEDIUM
From: @Backend
To: @EscalationHandler
Timestamp: 2026-04-08T11:00:00Z
Feature: booking-api
Plan Step: 2.1
---

## Situation
@Frontend and @Backend disagree on API pattern: REST (current plan) vs tRPC (type-safe, no contract duplication).

## Background
@Backend proposes tRPC to eliminate the need for separate Zod contracts + OpenAPI docs. @Frontend prefers REST for mobile app compatibility (React Native tRPC client adds complexity). Architecture doc (.ai/context/architecture.md) specifies Hono REST but was written before tRPC v11.

## Assessment
Decision affects all 12 planned API endpoints. Proceeding with REST preserves mobile parity. Switching to tRPC reduces backend work by ~30% but complicates mobile integration.

## Recommendation
Maintain REST pattern for cross-platform compatibility. @Architect to add note to architecture.md confirming REST is the standard for this project. Effort to resolve: 15 min.
```

## @EscalationHandler Response Format

```markdown
---
ESCALATION RESPONSE
Escalation: [Title from SBAR]
Resolved By: @EscalationHandler
Resolution Time: [X minutes]
Decision: [APPROVED | REJECTED | DEFERRED | NEEDS_INFO]

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Decision
[Clear statement of what has been decided]

## Rationale
[Why this decision was made]

## Action Items
- @[Agent]: [specific action] by [time]
- @[Agent]: [specific action] by [time]

## Follow-Up
[What to monitor / when to re-escalate if unresolved]
```

## Escalation Log Location

```
.ai/plans/active/audit/escalations/
├── 2026-04-08-payment-contract.md      ← Filed escalations
├── 2026-04-08-api-pattern.md
└── resolutions/
    ├── 2026-04-08-payment-contract.md  ← @EscalationHandler responses
```

## Common Mistakes
- Not escalating to protect "looking capable" — silent blocks kill sprint velocity
- Escalating without attempting resolution first — try for 15 min, then escalate
- Vague Situation statement — "it's not working" is useless
- No recommendation — @EscalationHandler needs options, not just problems
- Escalating LOW severity to CRITICAL — wastes escalation bandwidth

## Success Criteria
- [ ] SBAR format used for all escalations
- [ ] Severity correctly assessed
- [ ] At least two options in Recommendation section
- [ ] Escalation filed to `.ai/plans/active/audit/escalations/`
- [ ] SLA response times met by @EscalationHandler
- [ ] Resolution logged and @Guide notified to resume dependent work