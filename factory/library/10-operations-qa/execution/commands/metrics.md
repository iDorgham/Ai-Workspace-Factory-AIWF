---
cluster: execution
category: commands
display_category: Commands
id: commands:execution/commands/metrics
version: 10.0.0
domains: [product-delivery]
sector_compliance: pending
---
# Command: /metrics

> **Agent:** @MetricsAgent + @ForecastingAgent
> **Purpose:** Generate workspace metrics dashboards — velocity, risk, compliance, forecasts
> **Scope:** Project health tracking, sprint performance, predictive analytics

---

## Usage

```bash
/metrics dashboard [--scope sprint|project|team]
/metrics velocity [--sprint N|--range N]
/metrics risk [--scope feature|sprint|project]
/metrics forecast [--confidence 0.9|0.95] [--range N-sprints]
```

---

## Execution Flow

### 1. `/metrics dashboard` — Full Health Overview

**Parameters:**
- `--scope [scope]`: Optional — `sprint | project | team` (default: `project`)

**Output format:**

```markdown
## Sovereign Metrics Dashboard — [Date]

**Scope:** [sprint | project | team]
**Sprint:** [Current sprint N]
**Project:** [Project name]
**Mode:** [founder | pro | hybrid]

---

### 📊 Sprint Velocity
| Metric | Value | Target | Trend |
|--------|-------|--------|-------|
| Story points delivered | [N] | [N] | ↑ / → / ↓ |
| Features completed | [N] | [N] | ↑ / → / ↓ |
| Tasks completed | [N] | [N] | ↑ / → / ↓ |
| Velocity (pts/sprint) | [N] | [N] | ↑ / → / ↓ |
| Sprint completion rate | [N]% | 90%+ | ↑ / → / ↓ |

---

### 🛡️ Quality & Compliance
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Sovereign Compliance Score | [N]% | 95%+ | ✅ / ❌ |
| Contract Lock Rate | [N]% | 100% | ✅ / ❌ |
| Test Coverage (Unit) | [N]% | 45% | ✅ / ❌ |
| Test Coverage (Integration) | [N]% | 30% | ✅ / ❌ |
| Test Coverage (E2E) | [N]% | 5% | ✅ / ❌ |
| Security Findings (Critical) | [N] | 0 | ✅ / ❌ |
| Security Findings (High) | [N] | 0 | ✅ / ❌ |
| Visual Regressions | [N] | 0 | ✅ / ❌ |
| pnpm Catalog Usage | [N]% | 100% | ✅ / ❌ |

---

### ⚡ Performance
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Turborepo Cache Hit Rate | [N]% | 85%+ | ✅ / ❌ |
| Average Build Time | [N]s | <60s | ✅ / ❌ |
| Average Test Time | [N]s | <120s | ✅ / ❌ |
| Lighthouse Score (Performance) | [N] | ≥95 | ✅ / ❌ |
| Bundle Size (gzipped) | [N]KB | <120KB | ✅ / ❌ |
| First Contentful Paint | [N]ms | <1.5s | ✅ / ❌ |

---

### 🐝 Agent Swarm Efficiency
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Active Agents (this sprint) | [N] | — | — |
| Tasks per Agent (avg) | [N] | 3-7 | ✅ / ❌ |
| Escalations (this sprint) | [N] | <2 | ✅ / ❌ |
| Avg Time to Resolution | [N]min | <15min | ✅ / ❌ |
| Parallel Execution Rate | [N]% | >50% | ✅ / ❌ |

---

### 📈 Trend Summary (Last 5 Sprints)
```
Sprint N-4: [N] pts | [N]% compliance | [N] features
Sprint N-3: [N] pts | [N]% compliance | [N] features
Sprint N-2: [N] pts | [N]% compliance | [N] features
Sprint N-1: [N] pts | [N]% compliance | [N] features
Sprint N:   [N] pts | [N]% compliance | [N] features (in progress)
```

**Velocity trend:** ↑ Increasing / → Stable / ↓ Decreasing
**Quality trend:** ↑ Improving / → Stable / ↓ Degrading
**Risk level:** 🟢 Low | 🟡 Medium | 🔴 High

---

### ⚠️ Active Risks
| Risk | Score | Status | Owner |
|------|-------|--------|-------|
| [Risk description] | [N/25] | [open | mitigated] | @Agent |

---

### 🎯 Next Sprint Forecast
- **Expected velocity:** [N] ± [N] story points ([confidence]% confidence)
- **Features likely to complete:** [N] of [N] planned
- **Risk factors:** [List top 3 risks]
- **Recommendations:** [2-3 actionable improvements]

---

*Generated: [YYYY-MM-DD HH:MM] | By: @MetricsAgent + @ForecastingAgent*
```

---

### 2. `/metrics velocity` — Detailed Velocity Analysis

**Parameters:**
- `--sprint [N]`: Optional — specific sprint number
- `--range [N]`: Optional — last N sprints (default: 5)

**Output:**
```markdown
## Velocity Report — Last [N] Sprints

### Sprint Breakdown
| Sprint | Planned (pts) | Delivered (pts) | Completion % | Features | Tasks | Escalations |
|--------|---------------|-----------------|--------------|----------|-------|-------------|
| [N-4] | [N] | [N] | [N]% | [N] | [N] | [N] |
| [N-3] | [N] | [N] | [N]% | [N] | [N] | [N] |
| [N-2] | [N] | [N] | [N]% | [N] | [N] | [N] |
| [N-1] | [N] | [N] | [N]% | [N] | [N] | [N] |
| [N] | [N] | [N] | [N]% | [N] | [N] | [N] |

### Velocity Statistics
- **Average velocity:** [N] pts/sprint
- **Median velocity:** [N] pts/sprint
- **Standard deviation:** [N] pts
- **Best sprint:** Sprint [N] — [N] pts
- **Worst sprint:** Sprint [N] — [N] pts

### Throughput by Agent
| Agent | Tasks Completed | Avg Duration | Success Rate |
|-------|-----------------|--------------|--------------|
| @Backend | [N] | [N]min | [N]% |
| @Frontend | [N] | [N]min | [N]% |
| @QA | [N] | [N]min | [N]% |
| ... | ... | ... | ... |

### Bottleneck Analysis
- **Slowest phase:** [Contract | Backend | Frontend | Testing | Review]
- **Average wait time:** [N]min (time tasks wait for dependencies)
- **Recommendation:** [Actionable improvement]

### Capacity Planning
- **Sustainable velocity:** [N] pts/sprint (80th percentile)
- **Stretch_velocity:** [N] pts/sprint (95th percentile, higher risk)
- **Recommended next sprint capacity:** [N] pts
```

---

### 3. `/metrics risk` — Risk Register & Analysis

**Parameters:**
- `--scope [scope]`: Optional — `feature | sprint | project` (default: `project`)

**Output:**
```markdown
## Risk Report — [Scope]

**Date:** [YYYY-MM-DD]
**Scope:** [feature | sprint | project]
**Total risks:** [N]
**Critical:** [N] | **High:** [N] | **Medium:** [N] | **Low:** [N]

---

### Risk Register (5×5 Matrix)

| ID | Risk | Likelihood (1-5) | Impact (1-5) | Score | Status | Mitigation | Owner |
|----|------|------------------|--------------|-------|--------|------------|-------|
| R1 | [Description] | [N] | [N] | [N] | [open | mitigated] | [Strategy] | @Agent |
| R2 | ... | ... | ... | ... | ... | ... | ... |

---

### Risk Heat Map
```
Impact
5 | R3 |
4 | R1 | R4
3 |    | R2 | R5
2 |    |
1 |____|____|____|____|____
   1    2    3    4    5  Likelihood
```

### Risk Trends
- **New risks (this sprint):** [N]
- **Mitigated risks (this sprint):** [N]
- **Escalated risks:** [List risks that increased in score]
- **De-escalated risks:** [List risks that decreased in score]

### Top 3 Risks Requiring Action
1. **[Risk name]** — Score: [N]/25
   - **Why critical:** [Impact explanation]
   - **Recommended action:** [Specific mitigation]
   - **Owner:** @Agent

2. **[Risk name]** — Score: [N]/25
   - **Why critical:** [Impact explanation]
   - **Recommended action:** [Specific mitigation]
   - **Owner:** @Agent

3. **[Risk name]** — Score: [N]/25
   - **Why critical:** [Impact explanation]
   - **Recommended action:** [Specific mitigation]
   - **Owner:** @Agent

### Sovereign-Specific Risk Modifiers
- **Contract drift multiplier:** ×1.5 (if contracts unlocked)
- **Token violation multiplier:** ×1.3 (if raw values detected)
- **Test coverage penalty:** ×1.2 (if coverage < target)
- **Security finding multiplier:** ×2.0 (if critical/high findings)

*Applied modifiers increase base risk scores accordingly*
```

---

### 4. `/metrics forecast` — Predictive Analytics

**Parameters:**
- `--confidence [level]`: Optional — `0.9 | 0.95` (default: `0.9`)
- `--range [N]`: Optional — forecast next N sprints (default: 3)

**Output:**
```markdown
## Forecast Report — Next [N] Sprints

**Date:** [YYYY-MM-DD]
**Confidence level:** [N]%
**Historical data:** [N] sprints

---

### Delivery Forecast

| Sprint | Velocity (pts) | Confidence Interval | Features Expected | Completion Probability |
|--------|----------------|---------------------|-------------------|------------------------|
| N+1 | [N] ± [N] | [low]-[high] | [N] of [N] | [N]% |
| N+2 | [N] ± [N] | [low]-[high] | [N] of [N] | [N]% |
| N+3 | [N] ± [N] | [low]-[high] | [N] of [N] | [N]% |

### Scenario Analysis

#### Optimistic Scenario (95th percentile velocity)
- **Average velocity:** [N] pts/sprint
- **Features delivered in [N] sprints:** [N]
- **Project completion:** [Date]
- **Probability:** [N]%

#### Most Likely Scenario (median velocity)
- **Average velocity:** [N] pts/sprint
- **Features delivered in [N] sprints:** [N]
- **Project completion:** [Date]
- **Probability:** [N]%

#### Pessimistic Scenario (5th percentile velocity)
- **Average velocity:** [N] pts/sprint
- **Features delivered in [N] sprints:** [N]
- **Project completion:** [Date]
- **Probability:** [N]%

### Milestone Probabilities
| Milestone | Target Date | Probability | Confidence |
|-----------|-------------|-------------|------------|
| [Milestone 1] | [Date] | [N]% | ✅ / ⚠️ / ❌ |
| [Milestone 2] | [Date] | [N]% | ✅ / ⚠️ / ❌ |
| [Milestone 3] | [Date] | [N]% | ✅ / ⚠️ / ❌ |

### Recommendations
1. **[Action]** — [Rationale based on data]
2. **[Action]** — [Rationale based on data]
3. **[Action]** — [Rationale based on data]

### Risk-Adjusted Forecast
*Accounting for active risks and historical volatility:*
- **Adjusted velocity:** [N] pts/sprint (down [N]% from raw average)
- **Adjusted completion date:** [Date] ([N] sprints vs [N] raw)
- **Confidence in adjusted forecast:** [N]%

---

*Generated by: @ForecastingAgent | Model: Probabilistic velocity distribution*
```

---

## Data Sources

Metrics are calculated from:
1. **Sprint plans:** `.ai/plans/active/current-sprint.md` + `.ai/plans/archive/sprints/`
2. **Feature plans:** `.ai/plans/active/features/` + `.ai/plans/archive/features/`
3. **Task logs:** `.ai/plans/active/tasks/` + completion timestamps
4. **Quality gates:** Turborepo pipeline results, CI/CD reports
5. **Audit logs:** `.ai/plans/active/audit/command-logs/`
6. **Risk register:** Feature plan risk sections + active risk assessments
7. **Git history:** Commit frequency, merge frequency, branch lifespan

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| "No sprint data available" | No completed sprints yet | Run at least 1 full sprint before metrics |
| "No feature data available" | No completed features yet | Complete at least 1 feature before metrics |
| "Insufficient data for forecast" | <3 sprints of history | Forecasts unreliable with <3 sprints; show warning |
| "Metrics calculation failed" | Missing or corrupt data files | Check `.ai/plans/` structure, repair missing files |

---

## Integration Points

- **@MetricsAgent:** Calculates all metrics, generates reports
- **@ForecastingAgent:** Probabilistic forecasting, scenario modeling
- **@RiskAgent:** Risk register maintenance, scoring, mitigation tracking
- **@Guide:** Uses metrics for sprint planning and capacity decisions
- **@Founder:** Translates metrics to business-language status reports
- **@AnalyticsAgent:** Trend analysis, comparative analytics (future enhancement)

---

*Command Version: 1.0 | Created: 2026-04-08 | Maintained by: @MetricsAgent*
