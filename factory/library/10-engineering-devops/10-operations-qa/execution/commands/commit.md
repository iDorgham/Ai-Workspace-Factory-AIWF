---
cluster: execution
category: commands
display_category: Commands
id: commands:execution/commands/commit
version: 10.0.0
domains: [product-delivery]
sector_compliance: pending
---
# /commit — Intelligent Git Commits

## Syntax
```
/commit                         → Auto-generate message from staged changes + plan
/commit --message "custom msg"  → Use custom message (still adds plan reference)
/commit --scope feat|fix|chore|docs|refactor|test|security|style
/commit --auto                  → Fully automated (no confirmation prompt)
/commit --amend                 → Amend last commit (use carefully)
```

## Primary Agent
`@Automation`

## Pre-Flight Checks (Always Run Before Commit)

```
1. pnpm lint --filter='...[HEAD^1]'        → Must pass
2. pnpm type-check                         → Must pass
3. pnpm contract:validate                  → Must pass (no contract drift)
4. pnpm compliance --scope=staged     → Must pass

If ANY check fails:
→ Report exact violations
→ Provide specific fix for each violation
→ Block commit
→ After fix: re-run pre-flight automatically
```

## Commit Message Format

```
[type]([scope]): [description] [plan:X.Y | contract:domain.ts]

Types: feat | fix | chore | docs | refactor | test | security | style | perf | build | ci

Examples:
  feat(booking): add cart page with seat selection [plan:4.2 | contract:booking.ts]
  fix(auth): resolve token refresh race condition [plan:2.1 | contract:auth.ts]
  test(booking): add contract validation + E2E tests [plan:4.3 | contract:booking.ts]
  chore(deps): update prisma to 6.5.0 via pnpm catalog
  security(api): enforce HttpOnly cookie flag on refresh token [plan:2.3]
  style(ui): apply brand token corrections to BookingCard [plan:3.1]
  docs(api): update booking endpoint OpenAPI spec
```

## Auto-Message Generation

`@Automation` analyzes staged changes and generates commit message:
```
Staged files detected:
  M  apps/web/src/components/BookingCard/BookingCard.tsx
  M  apps/web/src/components/BookingCard/BookingCard.test.tsx
  A  messages/en.json (5 new keys)
  A  messages/ar.json (5 new keys)

Active plan: .ai/plans/active/features/booking-flow.md → Step 4.2
Contract reference: packages/shared/src/contracts/booking.ts

Generated message:
  feat(booking): implement BookingCard component with RTL support [plan:4.2 | contract:booking.ts]

  - Add BookingCard with token-compliant styling and WCAG AA a11y
  - Add 5 i18n keys (EN + AR) for booking card copy
  - Add unit tests with 94% coverage

Confirm commit? [y/n] (or /commit --auto to skip confirmation)
```

## Git Audit Log Entry
```
# .ai/plans/active/audit/git-audit.md entry
| 2026-04-08 14:32 | feat(booking) | a7f3b2c1 | @Frontend | plan:4.2 | contract:booking.ts |
```

## Signing (Enterprise Strategy)
```
# When enterprise branching strategy is active:
# All commits are GPG/SSH signed automatically
# @Automation configures signing key from CI secrets
git commit -S -m "feat(booking): ..."
```

---
*Invokes: @Automation | Logs to: .ai/plans/active/audit/git-audit.md*
