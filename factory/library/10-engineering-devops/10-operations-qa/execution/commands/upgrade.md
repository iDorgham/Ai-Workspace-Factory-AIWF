---
cluster: execution
category: commands
display_category: Commands
id: commands:execution/commands/upgrade
version: 10.0.0
domains: [product-delivery]
sector_compliance: pending
---
# Command: /upgrade

> **Agent:** @Architect + @Security
> **Purpose:** Scan for dependency, stack, and contract upgrades — assess risk, propose migration path
> **Scope:** Workspace-wide version management

---

## Usage

```bash
/upgrade [dependencies|stack|contracts|all] [--risk-check] [--dry-run]
```

---

## Execution Flow

### 1. `/upgrade dependencies` — Dependency Version Scan

**Parameters:**
- `--risk-check`: Optional — run risk assessment for each upgrade
- `--dry-run`: Optional — show proposed changes without applying

**Flow:**

1. **Scan current versions:**
   ```bash
   # Read pnpm-workspace.yaml catalog
   catalog:
     react: ^19.0.0
     next: ^15.0.0
     zod: ^3.24.0
     # ...
   ```

2. **Check for updates:**
   ```bash
   pnpm outdated --recursive --long --json > .tmp/outdated.json
   # Parse for major, minor, patch updates
   ```

3. **Classify updates by risk:**
   | Risk Level | Criteria | Examples |
   |------------|----------|----------|
   | **Low** | Patch versions, bug fixes | `1.2.3 → 1.2.4` |
   | **Medium** | Minor versions, new features | `1.2.x → 1.3.0` |
   | **High** | Major versions, breaking changes | `1.x → 2.0.0` |
   | **Critical** | Core framework, tooling changes | `Next.js 14 → 15`, `React 18 → 19` |

4. **Check changelogs for breaking changes:**
   - For each major/minor update → fetch release notes
   - Identify breaking changes, deprecations, migration steps
   - Flag incompatible combinations (e.g., React 19 requires Next.js 15)

5. **Run risk assessment (if `--risk-check`):**
   - **Impact analysis:** Which packages/apps affected?
   - **Migration effort:** S/M/L based on breaking changes
   - **Test coverage:** Can existing tests catch regressions?
   - **Rollback plan:** Can we revert if upgrade fails?

6. **Generate upgrade report:**

```markdown
## Dependency Upgrade Report

**Date:** [YYYY-MM-DD]
**Total dependencies:** [N]
**Updates available:** [N]
  - Major: [N] (high risk)
  - Minor: [N] (medium risk)
  - Patch: [N] (low risk)

---

### Recommended Upgrades (Low/Medium Risk)
| Package | Current | Latest | Risk | Migration Effort | Action |
|---------|---------|--------|------|------------------|--------|
| [package] | [version] | [version] | [low/med] | [S/M/L] | [Upgrade in next sprint] |

### High-Risk Upgrades (Requires Planning)
| Package | Current | Latest | Breaking Changes | Migration Plan |
|---------|---------|--------|------------------|----------------|
| [Next.js] | [14.x] | [15.x] | [List breaking changes] | [Migration steps, testing strategy] |

### Dependency Conflict Resolution
| Conflict | Packages | Resolution |
|----------|----------|------------|
| [React 19 required by Next.js 15] | [react, next] | [Upgrade both together] |

### Estimated Effort
- **Low-risk upgrades:** [N] packages — [N] hours (batch update)
- **Medium-risk upgrades:** [N] packages — [N] hours (test after each)
- **High-risk upgrades:** [N] packages — [N] hours (dedicated sprint)

### Upgrade Strategy
1. **Batch 1 (Low-risk):** Update all patch versions — run tests, merge
2. **Batch 2 (Medium-risk):** Update minor versions — test per package, merge
3. **Batch 3 (High-risk):** Plan dedicated sprint — full regression testing

### Rollback Plan
- All upgrades via pnpm catalog change — revert catalog, `pnpm install`, rebuild
- Git branch per batch — easy revert via branch deletion
- Staging deploy verification before production rollout
```

7. **Apply upgrades (if not `--dry-run`):**
   ```bash
   # Update catalog in pnpm-workspace.yaml
   # Run pnpm install
   # Run tests
   # Commit changes: chore(deps): upgrade [packages] [risk:low]
   ```

---

### 2. `/upgrade stack` — Technology Stack Review

**Purpose:** Evaluate if current technology choices are still optimal

**Flow:**

1. **Review current stack:**
   ```yaml
   Frontend: Next.js 15, React 19, Tailwind CSS v4, shadcn/ui
   Backend: Hono v4, Prisma 6, PostgreSQL
   Testing: Vitest, Playwright
   Monorepo: pnpm 9, Turborepo 2
   ```

2. **Compare against alternatives:**
   | Current | Alternative | Pros | Cons | Recommendation |
   |---------|-------------|------|------|----------------|
   | Hono v4 | Fastify, NestJS | [Hono: lighter, simpler] | [NestJS: more structure] | Keep Hono for now |
   | Vitest | Jest | [Vitest: faster, native TS] | [Jest: more plugins] | Keep Vitest |

3. **Evaluate emerging tech:**
   - Check for new stable releases of core tools
   - Assess maturity, adoption rates, community support
   - Identify deprecation warnings from current stack maintainers

4. **Generate stack review:**

```markdown
## Technology Stack Review

**Date:** [YYYY-MM-DD]
**Reviewed by:** @Architect

---

### Current Stack Assessment

#### Frontend
| Technology | Version | Status | Recommendation |
|------------|---------|--------|----------------|
| Next.js | 15.x | ✅ Current | Maintain — stable, well-supported |
| React | 19.x | ✅ Current | Maintain — latest stable |
| Tailwind CSS | v4 | ⚠️ Monitor | Recent major release — watch for bugs |
| shadcn/ui | Latest | ✅ Current | Maintain — follows best practices |

#### Backend
| Technology | Version | Status | Recommendation |
|------------|---------|--------|----------------|
| Hono | v4 | ✅ Current | Maintain — excellent DX |
| Prisma | 6.x | ✅ Current | Maintain — type-safe queries |
| PostgreSQL | Latest | ✅ Current | Maintain — proven, reliable |

#### Infrastructure
| Technology | Version | Status | Recommendation |
|------------|---------|--------|----------------|
| pnpm | 9.x | ✅ Current | Maintain — catalog mode essential |
| Turborepo | 2.x | ✅ Current | Maintain — caching critical |
| TypeScript | 5.8+ | ✅ Current | Maintain — strict mode non-negotiable |

### Emerging Tech to Watch
| Technology | Maturity | Potential Impact | Evaluation Timeline |
|------------|----------|------------------|---------------------|
| [Bun runtime] | Beta | Could replace Node.js for faster builds | Q3 2026 |
| [Biome linter] | Stable | Could replace ESLint + Prettier | Q4 2026 |

### Stack Change Recommendations
| Change | Impact | Effort | Recommendation |
|--------|--------|--------|----------------|
| [None at this time] | — | — | **Maintain current stack** |

### Next Review: [Date — typically quarterly]
```

---

### 3. `/upgrade contracts` — Contract Schema Review

**Purpose:** Identify outdated, deprecated, or unlock contracts

**Flow:**

1. **Scan all contracts:**
   ```bash
   ls packages/shared/src/contracts/*.ts
   # For each contract:
   #   - Check lock state
   #   - Check version
   #   - Check consumer count (how many apps/packages import this)
   ```

2. **Identify issues:**
   - Unlocked contracts → flag for review
   - Old versions (v1.x when v2.x exists) → flag for archival
   - Unused contracts (no consumers) → flag for removal
   - Contracts with frequent changes → flag for stability review

3. **Generate contract report:**

```markdown
## Contract Upgrade Review

**Date:** [YYYY-MM-DD]
**Total contracts:** [N]
**Locked:** [N] ([N]%)
**Unlocked:** [N] ([N]%)

---

### Contract Status
| Contract | Version | Lock State | Consumers | Status | Action |
|----------|---------|------------|-----------|--------|--------|
| [booking.ts] | v1.2 | ✅ Locked | [3] | Healthy | None |
| [auth.ts] | v1.0 | ❌ Unlocked | [5] | ⚠️ Review | Lock or update |
| [legacy.ts] | v1.0 | ✅ Locked | [0] | ❌ Unused | Archive |

### Breaking Changes Pending
| Contract | Proposed Change | Impact | Migration Effort |
|----------|-----------------|--------|------------------|
| [auth.ts] | [Add 2FA field] | [Medium — all auth consumers] | [S — additive only] |

### Recommendations
1. **[Lock auth.ts]** — Current schema stable, no pending changes
2. **[Archive legacy.ts]** — No consumers, functionality moved to [new-contract.ts]
3. **[Plan auth.ts v2]** — 2FA field needed, schedule for next sprint

### Contract Health Score: [N]/100
- Locked contracts: [N]% of total (×0.4 weight)
- Active consumers: [N] total (×0.3 weight)
- No pending breaking changes: ✅/❌ (×0.3 weight)
```

---

### 4. `/upgrade all` — Comprehensive Upgrade Scan

**Flow:**
1. Run all three scans: dependencies, stack, contracts
2. Combine results into unified report
3. Prioritize by risk and impact
4. Propose upgrade roadmap

**Output:** Combined report with sections for dependencies, stack, and contracts

---

## Risk Assessment Matrix

For each proposed upgrade:

| Factor | Low Risk | Medium Risk | High Risk |
|--------|----------|-------------|-----------|
| **Scope** | Single package | Multiple packages | Core framework |
| **Breaking changes** | None | Minor (deprecated APIs) | Major (API redesign) |
| **Test coverage** | >90% | 70-90% | <70% |
| **Rollback complexity** | Simple (revert catalog) | Moderate (restore backup) | Complex (data migration) |
| **Downstream impact** | No dependents | 1-3 dependents | 4+ dependents |

**Risk score = Sum of factor scores (1-3 each) → 5-15 total**
- **5-7:** Low risk — upgrade in current sprint
- **8-11:** Medium risk — plan for next sprint
- **12-15:** High risk — dedicated upgrade sprint

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| "No updates available" | All dependencies current | Report: "All dependencies up to date" |
| "Upgrade failed" | Breaking change not handled | Review changelog, update code, retry |
| "Tests failed after upgrade" | Incompatible change | Rollback, investigate, plan migration |
| "Contract upgrade blocked" | Contract locked with active consumers | Unlock only after all consumers updated |

---

## Integration Points

- **@Architect:** Leads stack review, contract review, migration planning
- **@Security:** Reviews dependency vulnerabilities, security implications
- **@RiskAgent:** Assesses upgrade risks, mitigation strategies
- **@QA:** Validates test suite catches upgrade regressions
- **@Automation:** Applies upgrades, creates branches, commits changes
- **@Guide:** Schedules upgrades into sprints based on risk

---

*Command Version: 1.0 | Created: 2026-04-08 | Maintained by: @Architect*
