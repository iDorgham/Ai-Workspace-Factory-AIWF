# Metrics-Driven Decision Making

## Purpose
Every significant decision — sprint goals, architectural changes, deployment timing, agent calibration — must be grounded in data. Velocity, compliance scores, cache hit rates, and risk registers replace gut feel with evidence.

## Core Metric Set

### Sovereign Compliance Score (ECS)
```
Formula: weighted average of all compliance checks
Target:  ≥95%
Warning: 85–94% → fix before next sprint
Block:   <85%   → merge blocked

Components:
  Contract adherence   (25%) → lock state + no drift
  Design tokens        (15%) → no raw hex/px
  RTL + i18n           (20%) → logical CSS + t() keys
  Accessibility        (20%) → ARIA + keyboard nav
  pnpm catalog         (20%) → strict mode compliance
```

### Cache Hit Rate (CHR)
```
Target:  ≥85%
Warning: 70–84% → review Turborepo inputs
Critical: <70%  → @RiskAgent auto-triggers, @Architect reviews pipeline

Measured per task: build | test | contract:validate | compliance
Trend: improving | stable | degrading
```

### Sprint Velocity (SV)
```
Unit: Story Points per session
Baseline: Establish in sprint 1 (typically 8–12 SP)
Target: Stable or growing
Red flag: >20% drop from baseline → investigate blockers

Breakdown by category:
  Feature work: [N] SP
  Bug fixes:    [N] SP
  Tech debt:    [N] SP
  Quality:      [N] SP
```

### Parallel Success Rate (PSR)
```
Target:  ≥88% (parallel executions without merge conflicts)
Warning: 75–87% → tighten scope boundaries
Critical: <75%  → switch to sequential pattern

Causes tracked: contract not locked | scope overlap | missing manifest
```

### Context Retention Index (CRI)
```
Target:  ≥95% (outputs consistent with loaded context)
Warning: 85–94% → review DMP loading order
Critical: <85%  → increase agent budgets or reduce parallel load

Measured by: reviewer rejections + hallucination count
```

## Decision Framework

### Sprint Goal Setting
```markdown
Before committing sprint goals, verify:
1. Current velocity: [N] SP/session (rolling 3-sprint average)
2. Compliance score: [N]% (must be ≥85% before new feature sprint)
3. Active risks ≥HIGH: [N] (must have mitigation plans)
4. Blocked items: [N] (must resolve before sprint start)

Capacity calculation:
  Total capacity = velocity × sprint_sessions
  Buffer = 20% (for bugs + tech debt)
  Available = Total × 0.8
```

### Go/No-Go Deployment Decision
```markdown
## Deployment Gate Check
Timestamp: [ISO]
Branch: [feature/X]

REQUIRED — all must be ✅:
  [ ] ECS ≥85%: [current score]%
  [ ] All tests pass: [pass/fail]
  [ ] Security scan: [0 critical/high]
  [ ] Build successful: [pass/fail]
  [ ] Health check endpoint: [200 OK]

RECOMMENDED:
  [ ] Lighthouse ≥95: [current score]
  [ ] Cache hit rate ≥70%: [current rate]%
  [ ] No active CRITICAL risks

Decision: DEPLOY | HOLD | ROLLBACK
```

### Architecture Change Decision
```markdown
Before any significant architecture change:
1. What metric is this improving? (cache rate / compliance / velocity)
2. What is the baseline (before)?
3. What is the target (after)?
4. What is the rollback plan if metrics worsen?
5. @RiskAgent score for this change: [X/25]
```

## Dashboard Format (@MetricsAgent Output)

```markdown
## Sovereign Metrics Dashboard
Sprint: [N] | Date: [ISO] | Project: [Name]

### Health Indicators
| Metric                    | Current | Target | Status  |
|---------------------------|---------|--------|------
## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---
|
| ECS (Compliance Score)    | 94%     | ≥95%   | ⚠️ Warn |
| Cache Hit Rate            | 88%     | ≥85%   | ✅ Good |
| Sprint Velocity           | 11 SP   | 10 SP  | ✅ Good |
| Parallel Success Rate     | 91%     | ≥88%   | ✅ Good |
| Context Retention Index   | 97%     | ≥95%   | ✅ Good |
| Test Coverage             | 93%     | ≥90%   | ✅ Good |
| Active HIGH+ Risks        | 2       | ≤2     | ✅ Good |

### Trend (last 3 sprints)
ECS:   91% → 93% → 94% (improving ↑)
CHR:   82% → 86% → 88% (improving ↑)
SV:    9 → 10 → 11 SP   (improving ↑)

### Actions Required
1. ⚠️ ECS at 94% — 1% below target. Cause: 2 token violations in BookingCard.tsx
   Fix: Replace #1B4F72 with var(--color-primary) — @Frontend, est. 15 min

### Forecast (@ForecastingAgent)
  Remaining work:    18 SP
  Current velocity:  11 SP/session
  ETA:               1.6 sessions
  Confidence:        85%
```

## Common Mistakes
- Making sprint commitments without checking current velocity
- Deploying when ECS is <85% "just this once" — creates compliance debt
- Ignoring cache hit rate degradation until it's critical
- Not measuring baseline before architectural changes — can't prove improvement
- Treating all metrics equally — ECS and security scan are blocking; velocity is informational

## Success Criteria
- [ ] Dashboard generated at sprint start + end
- [ ] Go/No-Go checklist completed before every deployment
- [ ] Sprint capacity calculated from actual velocity (not optimism)
- [ ] All metric trends tracked over ≥3 sprints
- [ ] Architectural decisions reference metrics in rationale