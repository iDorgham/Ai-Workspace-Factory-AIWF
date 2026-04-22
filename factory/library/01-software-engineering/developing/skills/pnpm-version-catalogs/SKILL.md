# pnpm Version Catalogs (Strict Mode)

## Purpose
Centralize all dependency versions in `pnpm-workspace.yaml`. No package may specify its own version. This prevents version drift, phantom dependencies, and supply chain inconsistencies across the monorepo.

## When to Activate
- When adding any new dependency
- When upgrading any existing package
- When creating a new app or package in the monorepo
- During `/init` workspace setup
- During `/upgrade` dependency review

## Workspace Configuration

### pnpm-workspace.yaml
```yaml
packages:
  - 'apps/*'
  - 'packages/*'

catalog:
  # ── Core Framework ──────────────────────────────────────────
  next: ^15.3.0
  react: ^19.1.0
  react-dom: ^19.1.0

  # ── Backend ─────────────────────────────────────────────────
  hono: ^4.7.0
  '@hono/node-server': ^1.13.0
  fastify: ^5.2.0

  # ── Database ─────────────────────────────────────────────────
  prisma: ^6.6.0
  '@prisma/client': ^6.6.0

  # ── Validation ───────────────────────────────────────────────
  zod: ^3.24.0
  '@hookform/resolvers': ^3.10.0
  react-hook-form: ^7.55.0

  # ── Styling ──────────────────────────────────────────────────
  tailwindcss: ^4.1.0
  '@tailwindcss/typography': ^0.5.16

  # ── UI Components ────────────────────────────────────────────
  '@radix-ui/react-dialog': ^1.1.6
  '@radix-ui/react-dropdown-menu': ^2.1.6
  '@radix-ui/react-select': ^2.1.6
  '@radix-ui/react-toast': ^1.2.6
  'class-variance-authority': ^0.7.1
  clsx: ^2.1.1
  'tailwind-merge': ^3.2.0
  'lucide-react': ^0.487.0

  # ── i18n ─────────────────────────────────────────────────────
  'next-intl': ^4.1.0

  # ── Auth ─────────────────────────────────────────────────────
  'jose': ^5.10.0
  'bcryptjs': ^3.0.2

  # ── State Management ─────────────────────────────────────────
  zustand: ^5.0.3
  '@tanstack/react-query': ^5.71.0

  # ── Testing ──────────────────────────────────────────────────
  vitest: ^3.1.0
  '@vitest/coverage-v8': ^3.1.0
  playwright: ^1.51.0
  '@playwright/test': ^1.51.0
  '@testing-library/react': ^16.3.0
  '@testing-library/user-event': ^14.6.0

  # ── Build & Tooling ──────────────────────────────────────────
  typescript: ^5.8.0
  eslint: ^9.23.0
  prettier: ^3.5.0
  turbo: ^2.4.4

  # ── Observability ────────────────────────────────────────────
  '@opentelemetry/api': ^1.9.0
  '@opentelemetry/sdk-node': ^0.57.0
```

### Package-Level package.json (Correct Pattern)
```json
{
  "name": "@workspace/web",
  "dependencies": {
    "next":          "catalog:",
    "react":         "catalog:",
    "react-dom":     "catalog:",
    "zod":           "catalog:",
    "next-intl":     "catalog:",
    "@workspace/ui": "workspace:*",
    "@workspace/shared": "workspace:*"
  },
  "devDependencies": {
    "typescript": "catalog:",
    "vitest":     "catalog:"
  }
}
```

### What's FORBIDDEN
```json
// ❌ NEVER — direct version specification
{
  "dependencies": {
    "zod": "^3.22.0",
    "react": "18.2.0"
  }
}

// ❌ NEVER — mismatched workspace protocol
{
  "dependencies": {
    "@workspace/ui": "^1.0.0"
  }
}
```

## Adding a New Dependency

```bash
# Step 1: Add to pnpm-workspace.yaml catalog section
# Step 2: Reference in package.json with "catalog:"
# Step 3: Install
pnpm install

# Never run:
pnpm add some-package --save  # ❌ bypasses catalog
```

## Upgrading Dependencies

```bash
# Scan for upgrades
/upgrade dependencies --risk-check

# @Architect reviews + @RiskAgent scores each upgrade
# Update version in pnpm-workspace.yaml ONLY
# All packages consuming "catalog:" get the upgrade automatically
pnpm install
```

## Enforcement

```bash
# compliance checks for:
# - Any package.json with non-"catalog:" or non-"workspace:*" versions
# - Any package installing at a different version than catalog

# CI check (turbo.json)
{
  "pipeline": {
    "compliance": {
      "dependsOn": ["build"],
      "env": ["GALERIA_STRICT_CATALOG=true"]
    }
  }
}
```

## Common Mistakes
- Running `pnpm add` directly in a package — always edit workspace.yaml first
- Using `^` or exact versions in package.json — use `"catalog:"` only
- Forgetting `workspace:*` for internal packages — never use relative paths or versions
- Mixing catalog entries with inline versions during package creation

## Success Criteria
- [ ] All external deps in `pnpm-workspace.yaml` catalog
- [ ] All `package.json` files use `"catalog:"` for external packages
- [ ] All `package.json` files use `"workspace:*"` for internal packages
- [ ] `pnpm install` succeeds with no version warnings
- [ ] `compliance` catalog check passes