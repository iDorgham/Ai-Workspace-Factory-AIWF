---
type: Command
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---


# /diagnose — Root Cause Analysis & Pattern Investigation

> **Primary Agents:** `@Debugger` (leads) + `@Security` + `@Optimizer` + `@ErrorDetective` + `@Guide`
> **Purpose:** Systematic root-cause analysis of bugs, performance issues, security gaps, and recurring failure patterns — without guessing or spraying fixes

---

## Usage

```bash
/diagnose [feature|performance|security|logs|patterns] [--depth quick|deep] [--scope path|app|package]
```

---

## Phase 0 — Before Diagnosing (mandatory)

```
Load: .ai/memory/error_patterns.md
Load: .ai/memory/anti_patterns.md
Check: is this issue already a known pattern?

  MATCH FOUND (AP-[id] or EP-[id]):
    → The root cause is likely the same
    → @Debugger reads the previous fix and applies it
    → @ErrorDetective logs: recurrence of EP-[id]
    → No full diagnosis needed — saves 2,000–6,000 tokens

  NO MATCH:
    → Run full diagnosis protocol below
    → Capture as EP-[next] to error_patterns.md after resolving
```

---

## 1. `/diagnose feature` — Bug & Feature Diagnosis

**Primary agent: @Debugger** — follows the 6-step diagnosis protocol from `debugger.md`

**Quick depth:**
1. Check `.ai/memory/error_patterns.md` — known pattern?
2. Read the exact error (not just the first line — full stack trace)
3. Check feature plan step and contract lock status
4. Identify last change before the error appeared (`git diff HEAD~3`)
5. Diagnose root cause (don't guess — verify the hypothesis)
6. Apply minimal fix

**Deep depth:**
1. All quick steps
2. Read and verify every import/dependency the failing code uses
3. Check pnpm-workspace.yaml — package versions correct?
4. Cross-reference contract fields vs what implementation uses
5. Check for architectural drift from the feature plan
6. Run relevant tests in isolation to confirm hypothesis

**Output format:**
```markdown
## @Debugger — Feature Diagnosis: [feature-name]
Depth: [quick | deep] | Date: YYYY-MM-DD

### Pattern Check (Phase 0)
Known pattern match: [AP-XXX / EP-XXX / NONE]
If match: [applying known fix — see EP-XXX for details]
If no match: [proceeding with full diagnosis]

### Error Analysis
Error: [exact message — NOT paraphrased]
Stack origin: [actual file:line where it started — usually bottom of stack]
Error type: [syntax | logic | contract_mismatch | wrong_api | hallucination | missing_file | env]

### Hypothesis (written before touching code)
Root cause: [specific, falsifiable hypothesis]
Evidence: [what in the error/code supports this]
Verification: [how to confirm without a full fix]

### Verification Result
Hypothesis: [CONFIRMED | WRONG — revised: ...]
Actual root cause: [1-2 sentences]

### Minimal Fix Applied
Changed: [file:line] — [exact change, nothing else]
Did NOT change: [list anything deliberately untouched]

### Quality Gates
| Gate | Status | Notes |
|------|--------|-------|
| spec:validate | ✅ / ❌ | |
| contract:auto-validate | ✅ / ❌ | |
| TypeScript | ✅ / ❌ | No `any` or `@ts-ignore` used |
| Tests pass | ✅ / ❌ | |
| Fix is minimal | ✅ / ❌ | No refactor, no new features |

### Error Capture (to .ai/memory/error_patterns.md)
EP-[id]: [pattern type] | Severity: [level] | Tokens wasted: ~[N] | Prevention rule: [rule]
Recurrence: [first occurrence | 2nd → promoting to AP-[next]]
```

---

## 2. `/diagnose performance` — Performance Bottleneck Analysis

**Primary agent: @Optimizer** with @MetricsAgent data

**Quick depth:**
1. Check Turborepo cache hit rate (target: ≥85%)
2. Check bundle size reports
3. Check Lighthouse scores
4. Check slow-running tests

**Deep depth:**
1. All quick steps
2. `pnpm turbo run build -- --analyze` (bundle analysis)
3. Check code splitting effectiveness and lazy loading
4. Analyze DB query performance (N+1 queries, missing indexes)
5. Review caching strategies (HTTP, CDN, in-memory)
6. Check for unbounded queries (AP-020 — common performance killer)

**Output format:**
```markdown
## @Optimizer — Performance Diagnosis
Scope: [web | api | all] | Depth: [quick | deep] | Date: YYYY-MM-DD

### Anti-Pattern Check
AP-020 (unbounded queries): [checked — [N] violations / none found]
AP-019 (missing DB indexes): [checked — [N] missing / all present]

### Frontend Performance (apps/web)
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Lighthouse Performance | [N] | ≥95 | ✅ / ❌ |
| LCP | [N]ms | <2.5s | ✅ / ❌ |
| CLS | [N] | <0.1 | ✅ / ❌ |
| TBT | [N]ms | <200ms | ✅ / ❌ |
| Bundle (gzipped) | [N]KB | <120KB | ✅ / ❌ |

### Backend Performance (apps/api)
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Avg Response | [N]ms | <200ms | ✅ / ❌ |
| P95 Response | [N]ms | <500ms | ✅ / ❌ |
| Error Rate | [N]% | <1% | ✅ / ❌ |

### Slow Endpoints
| Endpoint | Avg | P95 | Issue | Fix |
|----------|-----|-----|-------|-----|
| GET /api/[route] | [N]ms | [N]ms | N+1 queries | Add select + include |

### Build Pipeline
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Turborepo Cache Hit | [N]% | ≥85% | ✅ / ❌ |
| Avg Build Time | [N]s | <60s | ✅ / ❌ |
| CI Duration | [N]min | <10min | ✅ / ❌ |

### Prioritized Recommendations
| # | Action | Impact | Effort | Est. Improvement |
|---|--------|--------|--------|-----------------|
| 1 | [specific action] | High | S | [N]% faster / [N]KB smaller |
| 2 | [specific action] | Medium | M | [estimate] |
```

---

## 3. `/diagnose security` — Security Vulnerability Scan

**Primary agent: @Security** — always runs at deep depth

**Flow:**
1. Secret scan (TruffleHog equivalent)
2. AP-040 check: hardcoded credentials in code
3. Auth review: JWT config, cookie flags, token storage
4. AP-041 check: Zod validation at all API boundaries
5. AP-042 check: auth middleware on all non-public routes
6. CORS configuration review
7. Rate limiting implementation check
8. CSP headers review
9. `pnpm audit` — dependency vulnerabilities
10. OWASP Top 10 spot-check

**Output format:**
```markdown
## @Security — Security Diagnosis
Depth: deep (always) | Date: YYYY-MM-DD

### Anti-Pattern Status
| AP-ID | Check | Result |
|-------|-------|--------|
| AP-040 | Secrets in code/logs | ✅ Clean / ❌ Found: [location] |
| AP-041 | Zod at all API boundaries | ✅ All routes / ❌ Gap: [routes] |
| AP-042 | Auth on protected routes | ✅ All routes / ❌ Gap: [routes] |

### Secret Scan
| Check | Status | Details |
|-------|--------|---------|
| Hardcoded secrets | ✅ / ❌ | |
| .env in git history | ✅ / ❌ | |
| Tokens in localStorage | ✅ / ❌ | |

### Authentication Review
| Check | Status |
|-------|--------|
| JWT access expiry ≤15min | ✅ / ❌ |
| Refresh token rotation | ✅ / ❌ |
| HttpOnly + Secure + SameSite cookies | ✅ / ❌ |

### OWASP Top 10
| Risk | Status | Notes |
|------|--------|-------|
| A01: Broken Access Control | ✅ / ❌ | |
| A02: Cryptographic Failures | ✅ / ❌ | |
| A03: Injection | ✅ / ❌ | |
| A04: Insecure Design | ✅ / ❌ | |
| A05: Security Misconfiguration | ✅ / ❌ | |
| A06: Vulnerable Components | ✅ / ❌ | |
| A07: Auth Failures | ✅ / ❌ | |
| A08: Data Integrity | ✅ / ❌ | |
| A09: Logging Failures | ✅ / ❌ | |
| A10: SSRF | ✅ / ❌ | |

### Dependency Audit
Critical: [N] | High: [N] | Moderate: [N] | Low: [N]

### Critical Findings (block deploy)
| # | Finding | Severity | Location | Fix |
|---|---------|----------|----------|-----|
| 1 | [finding] | CRITICAL | [file/endpoint] | [specific action] |

### Security Score: [N]/100
Recommendation: [action required before deploy if <80]
```

**Every security finding → EP-[id] in error_patterns.md.**
**CRITICAL finding → immediate @EscalationHandler notification.**

---

## 4. `/diagnose logs` — Log & Command History Analysis

**Primary agent: @ErrorDetective** (log pattern specialist)

**Quick depth:**
1. Read recent command logs: `.ai/plans/active/audit/command-logs/`
2. Cross-reference failures with error_patterns.md
3. Identify recurring command failures
4. Present summary + pattern matches

**Deep depth:**
1. All quick steps
2. Correlation analysis: which agents + domains + commands fail together?
3. Check anti-pattern injection effectiveness (injected vs prevented)
4. Identify APs that aren't working (recurring despite injection)
5. Recommendations for injection improvements

**Output format:**
```markdown
## @ErrorDetective — Log Analysis
Scope: [command | build | test | ci] | Period: Last [N] days | Date: YYYY-MM-DD

### Command Summary
| Metric | Value |
|--------|-------|
| Total commands | [N] |
| Success rate | [N]% |
| Avg tokens per command | [N] |

### Failure Analysis
| Command | Failures | Rate | Pattern match | AP-ID |
|---------|----------|------|---------------|-------|
| /build | [N] | [N]% | Contract not locked | AP-030 |
| /test | [N] | [N]% | E2E timing issue | EP-019 |

### Anti-Pattern Injection Effectiveness
| AP-ID | Injected | Violations | Prevented | Effectiveness |
|-------|---------|------------|-----------|--------------|
| AP-001 | [N] | [N] | [N] | [N]% |

### Recommendations
1. AP-[id] effectiveness low → @KnowledgeSynthesizer: update agent Hard Rules
2. [Command] failing most → review pre-flight gate for that command
3. New pattern EP-[id] appearing 2+ times → promote to AP immediately
```

---

## 5. `/diagnose patterns` — Dedicated Mistake Pattern Analysis

**Primary agent: @ErrorDetective** + **@KnowledgeSynthesizer**

Provides full analysis of the mistake prevention system health:

```markdown
## @ErrorDetective + @KnowledgeSynthesizer — Pattern Analysis
Date: YYYY-MM-DD

### Error Pattern Health
Total EP entries (active): [N]
Promoted to AP: [N] | Pending (1 occurrence): [N] | Retired: [N]

### Anti-Pattern Registry Health
Total APs: [N] | CRITICAL: [N] | HIGH: [N] | MEDIUM: [N]
Average effectiveness: [N]% (target: ≥80%)

### Underperforming APs (effectiveness <80%)
| AP-ID | Effectiveness | Reason | Fix |
|-------|--------------|--------|-----|
| AP-010 | 72% | Injected after task starts | Move to pre-flight gate |

### Patterns Ready for Promotion (2+ occurrences)
| EP-ID | Pattern | Count | Proposed AP-ID |
|-------|---------|-------|----------------|
| EP-022 | Missing RTL visual test | 3 | AP-054 (new) |

### Estimated Token Savings This Sprint
AP injection prevented [N] violations × avg [N] tokens/fix = ~[N] tokens saved
```

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| "Feature not found" | Invalid feature name | `/status` to list active features |
| "No performance data" | App not built yet | Run `/build` first |
| "No logs found" | No command history | Check `.ai/plans/active/audit/` exists |
| "Pattern not found" | No match in error_patterns.md | New issue — proceed with full diagnosis |
| @Debugger returns "cannot determine cause" | Insufficient information | Re-run with `--depth deep`, provide error logs |

---

## Integration Points

| Agent | Role in /diagnose |
|-------|------------------|
| `@Debugger` | Leads feature diagnosis — 6-step protocol, no guessing |
| `@ErrorDetective` | Checks known patterns first, captures new patterns after |
| `@Security` | Leads security diagnosis — always deep |
| `@Optimizer` | Leads performance diagnosis, bundle analysis |
| `@KnowledgeSynthesizer` | Updates skill/agent files when recurring patterns found |
| `@Guide` | Coordinates diagnosis output, updates plan blockers |
| `@QA` | Provides test failure data, coverage context |
| `@Reviewer` | Reviews any architectural drift found |
| `@MetricsAgent` | Supplies historical performance trends |
| `@EscalationHandler` | Receives CRITICAL security findings |

---

*Command Version: 2.0 | Updated: 2026-04-11*
*Skills: mistake-prevention-system, hallucination-containment, structured-logging-tracing, self-healing-workflows, owasp-zero-trust-architecture*
