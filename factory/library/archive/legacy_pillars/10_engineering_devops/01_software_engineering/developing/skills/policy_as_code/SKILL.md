---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Policy-as-Code (compliance as Policy Engine)

## Purpose
Encode Sovereign governance rules as automated checks that run in CI. No human review can catch everything — the compliance gate enforces design tokens, RTL, i18n, accessibility, contract adherence, and security baselines automatically on every PR.

## When to Activate
- Every PR (automatically via CI)
- Before any `/build` or `/deploy`
- After any design token, contract, or dependency change
- During `/quality all` command

## Compliance Gate Architecture

```
PR opened / /quality all
        ↓
spec:validate         → Feature spec + testable AC + Data Shape + Edge Cases complete?
contract:auto-validate → Zod schemas locked? Fingerprints match? (CI task may be named contract:validate)
        ↓
compliance       → Design tokens, RTL, i18n, a11y, security, catalog
        ↓
security:scan         → Secrets, vulnerabilities, SBOM
        ↓
test                  → Coverage thresholds met?
        ↓
build                 → Type errors, compile errors
        ↓
GATE PASS → Allow merge
GATE FAIL → Block merge + file detailed report
```

## compliance Check Definitions

```typescript
// packages/config/src/sovereign-compliance.ts
// Run as: turbo run compliance

export interface ComplianceCheck {
  name:        string
  weight:      number   // contribution to Sovereign Compliance Score
  run:         () => Promise<ComplianceResult>
  failMessage: string
}

export const complianceChecks: ComplianceCheck[] = [
  // ── CONTRACT ADHERENCE (25%) ───────────────────────────────
  {
    name:    'contract:lock-state',
    weight:  10,
    run:     checkAllContractsLocked,
    failMessage: 'Unlocked contracts found. Run /contract lock [domain].'
  },
  {
    name:    'contract:no-drift',
    weight:  10,
    run:     checkContractFingerprints,
    failMessage: 'Contract fingerprint mismatch — schema changed after lock.'
  },
  {
    name:    'contract:api-validation',
    weight:  5,
    run:     checkApiRoutesUseContracts,
    failMessage: 'API routes found without Zod validation.'
  },

  // ── DESIGN TOKENS (15%) ───────────────────────────────────
  {
    name:    'tokens:no-raw-hex',
    weight:  8,
    run:     checkNoRawHexInSource,
    failMessage: 'Raw hex colors found in source. Use CSS variables from tokens.css.'
  },
  {
    name:    'tokens:no-raw-px',
    weight:  4,
    run:     checkNoRawPixelValues,
    failMessage: 'Raw pixel values found. Use spacing tokens (--space-*).'
  },
  {
    name:    'tokens:no-inline-styles',
    weight:  3,
    run:     checkNoInlineStyleWithValues,
    failMessage: 'Inline styles with raw values found. Use className with tokens.'
  },

  // ── RTL / BILINGUAL (20%) ─────────────────────────────────
  {
    name:    'rtl:no-directional-css',
    weight:  10,
    run:     checkNoDirectionalCSSProperties,
    failMessage: 'Directional CSS (margin-left/right, padding-left/right) found. Use logical properties.'
  },
  {
    name:    'i18n:no-hardcoded-text',
    weight:  10,
    run:     checkNoHardcodedUIText,
    failMessage: 'Hardcoded user-facing strings found. Use t() translation keys.'
  },

  // ── ACCESSIBILITY (20%) ───────────────────────────────────
  {
    name:    'a11y:interactive-elements',
    weight:  10,
    run:     checkInteractiveElementsHaveLabels,
    failMessage: 'Interactive elements missing aria-label or visible label.'
  },
  {
    name:    'a11y:no-div-buttons',
    weight:  5,
    run:     checkNoClickHandlersOnDivs,
    failMessage: 'onClick handlers on div/span found. Use <button> or <a>.'
  },
  {
    name:    'a11y:image-alt',
    weight:  5,
    run:     checkImagesHaveAlt,
    failMessage: 'Images missing alt attribute.'
  },

  // ── PNPM CATALOG (20%) ────────────────────────────────────
  {
    name:    'catalog:strict-mode',
    weight:  20,
    run:     checkAllDepsUseCatalog,
    failMessage: 'package.json files with non-catalog versions found.'
  },
]
```

## Compliance Score Formula

```
Sovereign Compliance Score (ECS) =
  (Contract Adherence  × 0.25) +
  (Design Tokens       × 0.15) +
  (RTL + i18n          × 0.20) +
  (Accessibility       × 0.20) +
  (pnpm Catalog        × 0.20)

Target: ≥95%
Warning: 85–94%
Block:   <85% → merge blocked
```

## Check Implementation Examples

```typescript
// Check: no raw hex colors in .tsx/.ts/.css source files
async function checkNoRawHexInSource(): Promise<ComplianceResult> {
  const { glob } = await import('glob')
  const files = await glob('apps/**/src/**/*.{tsx,ts,css}', { ignore: ['**/tokens.css', '**/*.test.*'] })

  const violations: string[] = []
  for (const file of files) {
    const content = await fs.readFile(file, 'utf-8')
    const hexMatches = content.match(/#[0-9a-fA-F]{3,8}\b/g)
    if (hexMatches) {
      violations.push(`${file}: ${hexMatches.join(', ')}`)
    }
  }
  return { passed: violations.length === 0, violations }
}

// Check: no directional CSS properties
async function checkNoDirectionalCSSProperties(): Promise<ComplianceResult> {
  const { glob } = await import('glob')
  const files = await glob('apps/**/src/**/*.{tsx,ts,css}')
  const forbidden = /margin-left|margin-right|padding-left|padding-right|border-left|border-right|text-align:\s*left|text-align:\s*right/

  const violations: string[] = []
  for (const file of files) {
    const content = await fs.readFile(file, 'utf-8')
    if (forbidden.test(content)) {
      violations.push(file)
    }
  }
  return { passed: violations.length === 0, violations }
}
```

## Compliance Report Output

```json
// .sovereign/compliance-report.json
{
  "timestamp": "2026-04-08T10:00:00Z",
  "branch": "feature/42-booking-flow",
  "score": 96.5,
  "status": "PASS",
  "checks": {
    "contract:lock-state":      { "passed": true,  "score": 10 },
    "contract:no-drift":        { "passed": true,  "score": 10 },
    "tokens:no-raw-hex":        { "passed": false, "score": 0,
      "violations": ["apps/web/src/components/BookingCard.tsx: #1B4F72"] },
    "rtl:no-directional-css":   { "passed": true,  "score": 10 },
    "i18n:no-hardcoded-text":   { "passed": true,  "score": 10 },
    "catalog:strict-mode":      { "passed": true,  "score": 20 }
  },
  "blockers": ["tokens:no-raw-hex"],
  "recommendation": "Replace #1B4F72 with var(--color-primary) in BookingCard.tsx"
}
```

## CI Integration

```yaml
# .github/workflows/ci.yml
- name: Sovereign Compliance Gate
  run: turbo run compliance
  env:
    GALERIA_STRICT_CATALOG: 'true'
    GALERIA_COMPLIANCE_TARGET: '85'

- name: Upload compliance report
  uses: actions/upload-artifact@v4
  with:
    name: compliance-report
    path: .sovereign/compliance-report.json

- name: Comment compliance score on PR
  if: github.event_name == 'pull_request'
  uses: actions/github-script@v7
  with:
    script: |
      const report = require('./.sovereign/compliance-report.json')
      const icon = report.status === 'PASS' ? '✅' : '❌'
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: `${icon} Sovereign Compliance: **${report.score}%** | ${report.status}`
      })
```

## Common Mistakes
- Running compliance only before release — run on every PR, not just at the end
- Ignoring warning-level findings — they become blockers next sprint
- Whitelisting files from compliance — fix the issue, don't exempt the file
- Not including compliance report in PR comments — teams don't know what failed

## Success Criteria
- [ ] `compliance` Turborepo task defined and running in CI
- [ ] Compliance score ≥95% on main branch
- [ ] PR blocked when score <85%
- [ ] Compliance report artifact uploaded on every CI run
- [ ] Score trend tracked by @MetricsAgent