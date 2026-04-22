# ci-quality-gates

Converted from `ci-quality-gates.yml` for template-folder type consistency.

```yml
# Sovereign template — GitHub Actions: full quality gate ORDER (CFG / contract-first).
# Copied to .github/workflows/ by: bash scripts/setup/create-github-workflows.sh (during /init).
#
# Gate order (do not reorder without updating Sovereign docs):
#   contract:validate → compliance → security:scan → test → build
#
# Wire each step to package.json scripts when your monorepo is ready (see CLAUDE.md).
# scripts/check/*.sh are used where they exist for fast local parity with CI.

name: Sovereign Quality Gates

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

permissions:
  contents: read

jobs:
  sovereign-quality-gates:
    name: Sovereign Quality Gates
    runs-on: ubuntu-latest
    timeout-minutes: 45

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: pnpm
          cache-dependency-path: pnpm-lock.yaml

      - name: Enable corepack (pnpm)
        run: corepack enable && corepack prepare pnpm@9 --activate

      - name: Install dependencies
        id: install
        run: |
          set -euo pipefail
          if [[ ! -f package.json ]]; then
            echo "No package.json — scaffold /init first. Skipping remaining gates."
            echo "skip=1" >> "$GITHUB_OUTPUT"
            exit 0
          fi
          if [[ -f pnpm-lock.yaml ]]; then
            pnpm install --frozen-lockfile
          else
            echo "::warning::No pnpm-lock.yaml — using non-frozen install. Commit a lockfile for reproducible CI."
            pnpm install --no-frozen-lockfile
          fi
          echo "skip=0" >> "$GITHUB_OUTPUT"

      # --- Gate 1: contract:validate (@ContractLock / Zod) ---
      - name: contract:validate
        if: steps.install.outputs.skip != '1'
        run: |
          set -euo pipefail
          if node -e "const p=require('./package.json');process.exit(p.scripts&&p.scripts['contract:validate']?0:1)" 2>/dev/null; then
            pnpm run contract:validate
          else
            echo "::warning::Add scripts.contract:validate in package.json to enforce Zod contracts in CI (Sovereign gate 1)."
          fi

      # --- Gate 2: compliance (tokens, a11y, i18n, RTL, …) ---
      - name: compliance
        if: steps.install.outputs.skip != '1'
        run: |
          set -euo pipefail
          if node -e "const p=require('./package.json');const s=p.scripts||{};process.exit(s['compliance']?0:1)" 2>/dev/null; then
            pnpm run compliance
          elif node -e "const p=require('./package.json');const s=p.scripts||{};process.exit(s['quality']?0:1)" 2>/dev/null; then
            pnpm run quality
          else
            echo "::notice::No compliance or quality script — running scripts/check/quick-check.sh (lint / typecheck when configured)."
            bash scripts/check/quick-check.sh
          fi

      # --- Gate 3: security:scan ---
      - name: security:scan
        if: steps.install.outputs.skip != '1'
        run: |
          set -euo pipefail
          if node -e "const p=require('./package.json');process.exit(p.scripts&&p.scripts['security:scan']?0:1)" 2>/dev/null; then
            pnpm run security:scan
          else
            echo "::warning::Add scripts.security:scan for SAST/audit (Sovereign gate 3). Running pnpm audit (high+)."
            pnpm audit --audit-level=high
          fi

      # --- Gate 4: test ---
      - name: test
        if: steps.install.outputs.skip != '1'
        run: |
          set -euo pipefail
          if node -e "const p=require('./package.json');process.exit(p.scripts&&p.scripts['test']?0:1)" 2>/dev/null; then
            pnpm run test
          else
            echo "::warning::Add scripts.test (Sovereign gate 4). Skipping tests until defined."
          fi

      # --- Gate 5: build ---
      - name: build
        if: steps.install.outputs.skip != '1'
        run: |
          set -euo pipefail
          if node -e "const p=require('./package.json');process.exit(p.scripts&&p.scripts['build']?0:1)" 2>/dev/null; then
            pnpm run build
          else
            echo "::warning::Add scripts.build (Sovereign gate 5). Skipping build until defined."
          fi

      # Optional: full local parity (install + quality chain) when you want a single bash entrypoint
      - name: scripts/check/full-check.sh (optional deep pass)
        if: steps.install.outputs.skip != '1'
        continue-on-error: true
        run: bash scripts/check/full-check.sh

```
