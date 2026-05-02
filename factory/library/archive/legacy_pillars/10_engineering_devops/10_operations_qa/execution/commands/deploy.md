---
type: Command
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---


# /deploy — Gated Deployment

## Syntax
```
/deploy staging                 → Deploy to staging environment
/deploy production              → Deploy to production (all gates required)
/deploy staging --feature name  → Deploy specific feature branch to staging
/deploy --rollback              → Roll back to previous stable version
/deploy --status                → Show current deployment status
/deploy --dry-run               → Simulate deployment (no actual deploy)
```

## Primary Agent
`@Automation`

## Deployment Gate Order

### Staging Deploy
```
1. contract:validate     → All contracts locked
2. compliance       → Tokens, a11y, i18n, RTL pass
3. security:scan         → No critical/high findings
4. test                  → All tests pass (unit + integration)
5. build                 → Compiles successfully
6. → DEPLOY to staging
7. health-check          → /api/health returns 200 within 60s
8. smoke-tests           → Critical paths smoke-tested
```

### Production Deploy
```
All staging gates PLUS:
5. @Reviewer approval    → Explicit approval required
6. e2e:passing           → Playwright E2E suite passes
7. visual:baseline       → No visual regressions
8. → DEPLOY to production
9. health-check          → /api/health returns 200 within 60s (3 retries)
10. auto-rollback trigger → If health check fails after 3 retries
11. @Guide notified       → Deployment status report
```

## Deployment Output

### Success
```
### @Automation — Deployment: Staging ✅
**Feature:** booking-flow | **Branch:** feature/42-booking-flow
**Time:** 2026-04-08 14:45 | **Duration:** 2m 14s

Pipeline:
  ✅ contract:validate    (0.8s)
  ✅ compliance      (1.2s) — Score: 97%
  ✅ security:scan        (3.1s) — 0 findings
  ✅ test                 (24s)  — 142 passed, 0 failed, 89% coverage
  ✅ build                (48s)  — Cache hit: 89% ↑
  ✅ deploy:staging       (14s)
  ✅ health-check         (3s)   — /api/health → 200 OK

Staging URL: https://booking-flow--preview.app.dev
Cache metrics: 89% hit rate | Build time: 48s (↓ 34% vs last)

Next: Test on staging → /deploy production when ready
```

### Failure + Auto-Rollback
```
### @Automation — Deployment: FAILED + ROLLED BACK ❌
**Health check failed** after 3 retries (timeout 60s)

Auto-rollback triggered:
  ✅ Previous version restored (v1.1.4)
  ✅ Production health confirmed (/api/health → 200)
  ✅ @Guide notified | @RiskAgent flagged | Incident logged

Root cause: [Error from health check logs]
Action needed: Investigate → fix → re-deploy

SBAR escalation created: .ai/plans/active/audit/escalations/deploy-fail-[timestamp].md
```

## Environment Configuration
```yaml
# Auto-generated .github/workflows/deploy.yml
# Environment secrets managed by @Automation (never in code)
environments:
  staging:
    url: ${{ secrets.STAGING_URL }}
    variables:
      NODE_ENV: staging
      DATABASE_URL: ${{ secrets.STAGING_DB_URL }}
  production:
    url: ${{ secrets.PRODUCTION_URL }}
    requires_approval: true  # GitHub environment protection
    variables:
      NODE_ENV: production
```

---
*Invokes: @Automation | Requires: @Reviewer approval (production) | Logs: git_audit.md*
