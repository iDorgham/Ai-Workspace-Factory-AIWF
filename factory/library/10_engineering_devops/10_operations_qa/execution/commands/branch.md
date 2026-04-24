---
type: Command
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---


# /branch — Git Branch Management

## Syntax
```
/branch feature [name]          → Create feature branch
/branch fix [name]              → Create bug fix branch
/branch release [version]       → Create release branch
/branch hotfix [name]           → Create hotfix from main
/branch list                    → List all active branches + status
/branch cleanup                 → Archive stale branches (>14 days inactive)
/branch [name] --strategy       → Override default branching strategy
```

## Primary Agent
`@Automation`

## Branch Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/[plan-id]-[slug]` | `feature/42-booking-flow` |
| Fix | `fix/[issue-id]-[slug]` | `fix/87-login-redirect` |
| Release | `release/v[X.X.X]` | `release/v1.2.0` |
| Hotfix | `hotfix/[id]-[slug]` | `hotfix/112-payment-crash` |
| AI Swarm | `ai-swarm/[task-slug]` | `ai-swarm/auth-login` |

## Execution Flow

### /branch feature booking-flow
```
1. @Automation reads .ai/plans/active/features/booking_flow.md
   → Extracts plan ID, description, sprint reference
2. Determines base branch from strategy:
   - Founder: checkout main, pull
   - Hybrid: checkout develop, pull
   - Enterprise: checkout develop, pull
3. Creates branch: feature/[plan-id]-booking-flow
4. Pushes to remote with tracking
5. Optionally opens draft PR if --pr flag provided
6. Updates .ai/plans/active/audit/git_audit.md
```

### Branch Protection Auto-Configuration
```yaml
# Applied on branch creation (Hybrid Agile example)
develop protection:
  required_status_checks:
    - contract:validate
    - compliance
    - test
  required_pull_request_reviews:
    required_approving_review_count: 1
  enforce_admins: false
  allow_deletions: false

main protection:
  required_status_checks:
    - contract:validate
    - compliance
    - security:scan
    - test
    - build
  required_pull_request_reviews:
    required_approving_review_count: 2
    dismiss_stale_reviews: true
  require_signed_commits: true  # Enterprise only
```

## Output
```
### @Automation — Branch Created
Branch: feature/42-booking-flow
Base: develop (synced — 0 commits behind)
Remote: origin/feature/42-booking-flow (pushed)
Plan linked: .ai/plans/active/features/booking_flow.md
Draft PR: #48 (title auto-generated from plan)

CI triggered: lint + type-check → running
Next: Implement features → /commit when ready
```

## /branch list Output
```
Active branches (strategy: Hybrid Agile):
  develop          ← base (3 commits ahead of main)
  feature/42-booking-flow    [2 days] @Frontend active
  feature/39-auth-refresh    [5 days] @Backend active — PR #45 open
  fix/87-login-redirect      [1 day]  @Frontend complete — awaiting review

Stale (>14 days, no activity):
  feature/31-admin-panel     [18 days] → /branch cleanup to archive

Next: /commit [changes] → /push → PR gates run automatically
```

---
*Invokes: @Automation | Logs to: .ai/plans/active/audit/git_audit.md*
