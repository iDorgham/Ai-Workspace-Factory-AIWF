---
type: Generic
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# SBOM + License Scanning + Secret Management

## Purpose
Track every dependency (Software Bill of Materials), ensure licenses are compatible, and prevent secrets from ever entering the codebase. These are non-negotiable for hospitality properties serving EU guests (GDPR supply chain requirements) and gov-tech clients.

## When to Activate
- Every release build
- When adding new dependencies
- When `pnpm audit` finds vulnerabilities
- During `/quality security` audit

## Secret Management Rules

### What Never Goes in Code
```bash
# ❌ NEVER commit these — not even in .env
DATABASE_URL=postgresql://...
JWT_ACCESS_SECRET=...
STRIPE_SECRET_KEY=sk_live_...
API_KEYS=...
ENCRYPTION_KEY=...

# ✅ Only commit .env.example with placeholder values
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DB_NAME
JWT_ACCESS_SECRET=minimum-32-character-secret-replace-in-ci
STRIPE_SECRET_KEY=sk_test_or_live_key_from_stripe_dashboard
```

### .env.example Pattern
```bash
# apps/api/.env.example
# ── Database ──────────────────────────────────────────────
DATABASE_URL=postgresql://user:password@localhost:5432/sovereign_dev

# ── Authentication ────────────────────────────────────────
JWT_ACCESS_SECRET=change-me-min-32-chars-for-production
JWT_REFRESH_SECRET=different-change-me-min-32-chars-for-production
BCRYPT_ROUNDS=12

# ── External Services ─────────────────────────────────────
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
MAILGUN_API_KEY=key-...
MAILGUN_DOMAIN=mail.yourdomain.com

# ── Encryption ────────────────────────────────────────────
ENCRYPTION_KEY=64-char-hex-key-generate-with-openssl-rand-hex-32

# ── App ───────────────────────────────────────────────────
NEXT_PUBLIC_APP_URL=http://localhost:3000
NODE_ENV=development
PORT=4000
```

### CI Secret Injection (GitHub Actions)
```yaml
# All secrets injected via CI — never in code
- name: Deploy
  env:
    DATABASE_URL:       ${{ secrets.DATABASE_URL }}
    JWT_ACCESS_SECRET:  ${{ secrets.JWT_ACCESS_SECRET }}
    JWT_REFRESH_SECRET: ${{ secrets.JWT_REFRESH_SECRET }}
    STRIPE_SECRET_KEY:  ${{ secrets.STRIPE_SECRET_KEY }}
  run: vercel deploy --prod
```

## Secret Scanning (TruffleHog)

```yaml
# .github/workflows/security.yml
- name: Secret scanning
  uses: trufflesecurity/trufflehog@main
  with:
    path: ./
    base: ${{ github.event.repository.default_branch }}
    extra_args: --only-verified --fail
```

### .gitignore (Mandatory Entries)
```gitignore
# Environment files — never commit
.env
.env.local
.env.production
.env.staging
*.env

# Secrets and keys
*.pem
*.key
*.p12
*.pfx
secrets/
```

## SBOM Generation

```bash
# Generate Software Bill of Materials for every release
npx @cyclonedx/cyclonedx-npm \
  --output sbom.json \
  --output-format json \
  --short-puris false \
  --production

# Store in release artifacts
# Required for: ISO 27001, SOC 2, EU cyber resilience act
```

### SBOM Integration in CI
```yaml
- name: Generate SBOM
  run: |
    npx @cyclonedx/cyclonedx-npm --output sbom-${{ github.sha }}.json
    
- name: Upload SBOM
  uses: actions/upload-artifact@v4
  with:
    name: sbom-${{ github.sha }}
    path: sbom-${{ github.sha }}.json
    retention-days: 365  # Keep for compliance audits
```

## License Scanning

```bash
# Check all licenses — fail on GPL (incompatible with commercial)
npx license-checker \
  --production \
  --failOn "GPL;LGPL;AGPL" \
  --excludePackages "your-private-package" \
  --json \
  --out licenses.json
```

### Allowed License List
```
MIT       ✅ Allowed
Apache-2.0 ✅ Allowed
BSD-2     ✅ Allowed
BSD-3     ✅ Allowed
ISC       ✅ Allowed
CC0-1.0   ✅ Allowed
Unlicense ✅ Allowed

GPL-2.0   ❌ Blocked (copyleft — affects commercial use)
GPL-3.0   ❌ Blocked
AGPL-3.0  ❌ Blocked (strongest copyleft)
LGPL-2.0  ⚠️  Review required
LGPL-3.0  ⚠️  Review required
```

## Dependency Vulnerability Management

```bash
# Audit all deps — fail on high/critical
pnpm audit --audit-level=high --prod

# Auto-fix compatible updates
pnpm audit --fix

# Dependabot config — .github/dependabot.yml
version: 3.3.1
updates:
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: weekly
    open-pull-requests-limit: 5
    labels: ["security", "dependencies"]
    ignore:
      - dependency-name: "*"
        update-types: ["version-update:semver-major"]
```

## Secrets Rotation Policy

```markdown
## Secret Rotation Schedule

| Secret              | Rotation Frequency | Method              |
|---------------------|--------------------|------------------
## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---
|
| JWT Access Secret   | 90 days            | CI/CD secret update |
| JWT Refresh Secret  | 90 days            | CI/CD secret update |
| Database password   | 180 days           | DB admin + CI update|
| Stripe keys         | On compromise only | Stripe dashboard    |
| Encryption keys     | 1 year             | Key rotation job    |

Rotation procedure:
1. Generate new secret
2. Update in CI/CD secrets (GitHub Secrets)
3. Deploy — new secret takes effect
4. Old tokens/sessions expire naturally (JWT expiry)
```

## Common Mistakes
- Using the same secret for JWT access and refresh — rotate/compromise is coupled
- Committing `.env.local` by forgetting `.gitignore` — scan with TruffleHog pre-commit
- Not generating SBOM before major releases — required for enterprise clients
- GPL dependency slipping in via transitive deps — license scanner catches this
- Storing secrets in GitHub Actions environment output — use `::add-mask::` to redact

## Success Criteria
- [ ] `.gitignore` includes all `.env*` patterns
- [ ] `.env.example` committed with all required keys (placeholder values only)
- [ ] TruffleHog secret scan passes in CI
- [ ] `pnpm audit` shows zero critical/high vulnerabilities
- [ ] License scan passes with no GPL dependencies
- [ ] SBOM artifact generated and stored on every release
- [ ] Secret rotation schedule documented and tracked