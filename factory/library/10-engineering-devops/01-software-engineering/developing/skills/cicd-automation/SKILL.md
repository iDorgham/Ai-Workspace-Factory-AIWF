# CI/CD Automation + GitHub Branching Workflows

## Purpose
Automate quality gates, branch protection, PR creation, and deployments. @Automation handles all git operations — developers and agents never push directly to main. Every change goes through the full gate sequence.

## Branching Strategy Selection

```markdown
### founder (Trunk-Based) — Solo/Small Team
main ← ai-swarm/* branches (squash merge, auto-delete)
No develop branch. Fast iteration. Suitable for: solo founders, 1-3 person teams.

### hybrid (Agile) — Most Projects
main ← develop ← feature/* branches
release/* from develop when stable.
Suitable for: 2-10 person teams, sprint-based development.

### enterprise (GitFlow) — Large Teams / Gov-Tech
main ← develop ← feature/* (merge commit)
release/* from develop → rebase merge to main + tag
hotfix/* from main
2 approvals + signed commits. Suitable for: regulated industries.
```

## Branch Naming Convention

```bash
feature/[plan-id]-[slug]         # feature/42-booking-flow
fix/[plan-id]-[slug]             # fix/43-double-booking-bug
release/v[X.X.X]                 # release/v1.2.0
hotfix/[plan-id]-[slug]          # hotfix/44-payment-crash
ai-swarm/[task-slug]             # ai-swarm/booking-form-rtl
chore/[slug]                     # chore/update-dependencies
```

## Commit Convention

```bash
# Format: type(scope): message [plan:X.Y | contract:domain.ts]
feat(booking): add table availability check [plan:3.2 | contract:booking.ts]
fix(auth): resolve refresh token rotation bug [plan:3.5]
chore(deps): update zod to 3.24.0 in catalog
test(booking): add integration tests for cancellation flow
security(auth): add rate limiting to login endpoint
refactor(ui): extract BookingCard to packages/ui
```

## GitHub Actions — Full CI Pipeline

```yaml
# .github/workflows/ci.yml
name: Sovereign CI

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]

env:
  TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
  TURBO_TEAM: ${{ secrets.TURBO_TEAM }}

jobs:
  quality-gates:
    name: Quality Gates
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }

      - uses: pnpm/action-setup@v3
        with: { version: '9' }

      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'pnpm' }

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      # Gate 1: Contract Validation
      - name: Contract validation
        run: turbo run contract:validate

      # Gate 2: Type Check
      - name: Type check
        run: turbo run type-check

      # Gate 3: Lint
      - name: Lint
        run: turbo run lint

      # Gate 4: Sovereign Compliance
      - name: Sovereign Compliance Gate
        run: turbo run compliance
        env:
          GALERIA_STRICT_CATALOG: 'true'
          GALERIA_COMPLIANCE_TARGET: '85'

      # Gate 5: Unit + Integration Tests
      - name: Tests
        run: turbo run test
        env:
          DATABASE_URL: ${{ secrets.TEST_DATABASE_URL }}

      # Gate 6: Security Scan
      - name: Security scan
        run: pnpm audit --audit-level=high --prod

      - name: Secret scanning
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          extra_args: --only-verified

      # Gate 7: Build
      - name: Build
        run: turbo run build
        env:
          NODE_ENV: production

      # Post: Upload compliance report
      - name: Upload compliance report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: compliance-report-${{ github.sha }}
          path: .sovereign/compliance-report.json

  e2e-tests:
    name: E2E Tests
    runs-on: ubuntu-latest
    needs: quality-gates
    if: github.event_name == 'pull_request'

    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'pnpm' }
      - run: pnpm install --frozen-lockfile
      - run: pnpm exec playwright install --with-deps chromium
      - name: E2E Tests
        run: turbo run test:e2e
        env:
          DATABASE_URL: ${{ secrets.TEST_DATABASE_URL }}
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

## Deploy Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-production:
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'pnpm' }
      - run: pnpm install --frozen-lockfile

      - name: Deploy to Vercel (web)
        run: vercel deploy --prod --token ${{ secrets.VERCEL_TOKEN }}
        working-directory: apps/web

      - name: Health check
        run: |
          for i in 1 2 3 4 5; do
            STATUS=$(curl -s -o /dev/null -w "%{http_code}" ${{ vars.API_URL }}/health)
            if [ "$STATUS" = "200" ]; then echo "Healthy" && exit 0; fi
            sleep 15
          done
          exit 1

      - name: Rollback on failure
        if: failure()
        run: vercel rollback --token ${{ secrets.VERCEL_TOKEN }}
```

## Branch Protection Rules

```yaml
# .github/workflows/setup-branch-protection.yml
# Run once during /init

Branch: main
Required status checks:
  - quality-gates
  - e2e-tests
Required reviews: 1
Dismiss stale reviews: true
Require signed commits: true (enterprise mode)
Restrict pushes: only via PR
Auto-delete head branches: true
```

## PR Auto-Generation Template

```markdown
## PR: [feature name]
**Plan Step:** [X.Y] | **Contract:** [domain.ts] | **Sprint:** [N]

### Changes
[Auto-generated from git diff summary]

### Acceptance Criteria Verified
- [x] [Gherkin scenario 1]
- [x] [Gherkin scenario 2 — RTL]
- [x] [Gherkin scenario 3 — error case]

### Quality Gates
- [x] contract:validate ✅
- [x] compliance ✅ ([score]%)
- [x] security:scan ✅
- [x] tests ✅ ([coverage]% coverage)
- [x] build ✅

### Screenshots
[Attach LTR + RTL screenshots for UI changes]
```

## Common Mistakes
- Direct push to main — always via PR + gates
- Skipping `--frozen-lockfile` in CI — non-deterministic installs
- Not caching Turborepo in CI — rebuilds everything every run
- Bypassing gates with `--no-verify` — destroys the compliance system
- Not setting branch protection until "launch" — protection must exist from day one

## Success Criteria
- [ ] CI pipeline runs all 7 quality gates on every PR
- [ ] Branch protection configured on main (and develop for hybrid)
- [ ] Deploy pipeline has health check + auto-rollback
- [ ] Turborepo remote caching enabled in CI
- [ ] All commits follow conventional commit format
- [ ] Auto-delete head branches after merge