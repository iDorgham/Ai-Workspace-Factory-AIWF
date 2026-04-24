---
cluster: execution
category: commands
display_category: Commands
id: commands:execution/commands/monorepo
version: 10.0.0
domains: [product-delivery]
sector_compliance: pending
---
# Command: /monorepo

> **Agent:** @Architect
> **Purpose:** Manage monorepo apps and packages — add, remove, optimize, and track status
> **Scope:** pnpm workspace + Turborepo pipeline management

---

## Usage

```bash
/monorepo status
/monorepo add-app [--name] [--type] [--framework]
/monorepo add-package [--name] [--type]
/monorepo optimize [--scope]
```

---

## Execution Flow

### 1. `/monorepo status` — Show Monorepo Health

**Output format:**
```markdown
## Monorepo Status

### Workspace Configuration
- **Package manager:** pnpm 9 (catalogMode: strict)
- **Build orchestrator:** Turborepo 2
- **Workspace file:** pnpm-workspace.yaml
- **Pipeline config:** turbo.json

### Apps
| Name | Type | Framework | Status | Last built |
|------|------|-----------|--------|------------|
| web | frontend | Next.js 15 (App Router) | [pending | active | built] | [timestamp] |
| api | backend | Hono v4 | [pending | active | built] | [timestamp] |
| [custom] | [type] | [framework] | [status] | [timestamp] |

### Packages
| Name | Type | Status | Consumers |
|------|------|--------|-----------|
| shared | contracts + utils | [active] | web, api |
| ui | components + tokens | [pending | active] | web |
| config | eslint, tsconfig, tailwind | [pending | active] | web, api |

### Pipeline Health
| Task | Cache hit | Last run | Status |
|------|-----------|----------|--------|
| contract:validate | [N]% | [timestamp] | ✅ / ❌ |
| build | [N]% | [timestamp] | ✅ / ❌ |
| test | [N]% | [timestamp] | ✅ / ❌ |
| compliance | [N]% | [timestamp] | ✅ / ❌ |

### Package Boundaries (Strict)
- `packages/shared` → imports external only
- `packages/ui` → imports `packages/shared` + external
- `packages/config` → imports external tools only
- `apps/*` → imports any `packages/*` + external, never other apps

### Dependency Graph
```
packages/shared ← packages/ui ← apps/web
packages/shared ← apps/api
packages/config → all packages (dev dependencies)
```
```

---

### 2. `/monorepo add-app` — Add New Application

**Parameters:**
- `--name [app-name]`: Required — application identifier (kebab-case)
- `--type [app-type]`: Required — `web | api | mobile | desktop | cli | docs`
- `--framework [framework]`: Optional — auto-selected by type if not provided

**Framework defaults by type:**
| Type | Default framework | Alternatives |
|------|-------------------|--------------|
| web | Next.js 15 (App Router) | Vite + React, Remix |
| api | Hono v4 | Fastify, NestJS, Express |
| mobile | React Native (Expo) | Flutter, NativeScript |
| desktop | Electron + React | Tauri, Neutralinojs |
| cli | Node.js + Commander | Go, Rust (Clap) |
| docs | VitePress | Docusaurus, Mintlify |

**Flow:**
1. **Validate inputs:**
   - App name is kebab-case, unique in workspace
   - App type is recognized
   - No existing app with same name in `apps/`

2. **Select framework:**
   - Use `--framework` if provided
   - Otherwise use default for app type
   - Confirm with user if multiple valid options

3. **Scaffold app:**
   ```bash
   # Create directory structure
   apps/[app-name]/
   ├── package.json          # Depends on @workspace/shared, @workspace/ui (if web)
   ├── tsconfig.json         # Extends @workspace/config/tsconfig.json
   ├── src/
   │   ├── app/ or routes/   # Framework-specific entry
   │   ├── components/       # App-specific components
   │   └── lib/              # App utilities
   ├── tests/                # Test files
   └── README.md             # App documentation
   ```

4. **Update workspace config:**
   ```yaml
   # pnpm-workspace.yaml — add app to packages list
   packages:
     - 'apps/*'      # Already covers new app
     - 'packages/*'
   ```

5. **Update Turborepo pipeline:**
   ```json
   // turbo.json — ensure pipeline handles new app type
   {
     "pipeline": {
       "build": {
         "dependsOn": ["^build", "contract:validate"]
       }
     }
   }
   ```

6. **Install dependencies:**
   ```bash
   pnpm install  # Resolves from catalog, adds new app to workspace
   ```

7. **Create initial build:**
   ```bash
   pnpm --filter [app-name] build
   # Verify build passes
   ```

8. **Update project context:**
   - Add app to `.ai/context/project-type.md` apps list
   - Update `.ai/memory/project-context.md` with new app status

---

### 3. `/monorepo add-package` — Add Shared Package

**Parameters:**
- `--name [pkg-name]`: Required — package identifier (kebab-case)
- `--type [pkg-type]`: Required — `shared | ui | config | utils | types`

**Flow:**
1. **Validate inputs:**
   - Package name is kebab-case, unique in workspace
   - Package type is recognized
   - No existing package with same name in `packages/`

2. **Scaffold package:**
   ```bash
   packages/[pkg-name]/
   ├── package.json          # Name: @workspace/[pkg-name]
   ├── tsconfig.json         # Extends workspace config
   ├── src/
   │   ├── index.ts          # Main entry point
   │   └── [type-specific structure]
   ├── tests/                # Test files
   └── README.md             # Package documentation
   ```

3. **Set package boundaries:**
   - `shared` → imports external only, exports contracts + utils
   - `ui` → imports `shared` + external, exports components + tokens
   - `config` → imports external tools only, exports configs
   - `utils` → imports `shared` + external, exports utilities
   - `types` → imports external only, exports TypeScript types

4. **Update workspace config:**
   - Already covered by `packages/*` in pnpm-workspace.yaml

5. **Install dependencies:**
   ```bash
   pnpm install
   ```

6. **Build package:**
   ```bash
   pnpm --filter @workspace/[pkg-name] build
   # Verify build passes
   ```

7. **Document imports:**
   - Add import examples to README.md
   - Update package boundary rules in `.ai/context/architecture.md` if needed

---

### 4. `/monorepo optimize` — Optimize Build Pipeline

**Parameters:**
- `--scope [scope]`: Optional — `all | apps | packages | [specific-name]`

**Flow:**
1. **Analyze current pipeline:**
   ```bash
   pnpm turbo run build --dry=json > .turbo/analysis.json
   # Parse task durations, cache hit rates, dependency chains
   ```

2. **Identify bottlenecks:**
   - Tasks with low cache hit rate (<70%)
   - Tasks with long durations (>30s)
   - Tasks blocking many downstream tasks
   - Packages/apps rebuilt unnecessarily

3. **Optimize Turborepo config:**
   ```json
   // turbo.json — optimization targets
   {
     "pipeline": {
       "build": {
         "inputs": ["src/**", "!src/**/*.test.ts"],  // Exclude tests from build cache
         "outputs": [".next/**", "dist/**"],
         "dependsOn": ["^build", "contract:validate"]
       },
       "test": {
         "inputs": ["src/**", "tests/**"],
         "outputs": ["coverage/**"],
         "dependsOn": ["build"]
       }
     }
   }
   ```

4. **Optimize pnpm catalog:**
   - Check for duplicate dependency versions
   - Ensure all packages use catalog, not direct versions
   - Remove unused dependencies

5. **Run optimized pipeline:**
   ```bash
   pnpm turbo run build --cache-dir .turbo/cache
   # Measure new cache hit rate and duration
   ```

6. **Report improvements:**
   ```markdown
   ## Optimization Results
   - Cache hit rate: [before]% → [after]% ([+/-]N%)
   - Average build time: [before]s → [after]s ([+/-]N%)
   - Unnecessary rebuilds eliminated: [count]
   - Pipeline efficiency: [score]/100
   ```

7. **Update metrics:**
   - Log to `.ai/memory/decisions.md` with optimization rationale
   - @MetricsAgent tracks cache hit rate trend

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| "App name already exists" | Duplicate name in `apps/` | Choose different name or remove existing app |
| "Package name already exists" | Duplicate name in `packages/` | Choose different name or remove existing package |
| "Framework not supported for type" | Invalid framework choice | Use default or select from alternatives |
| "Build failed" | Compilation errors in new app/package | Fix errors, check dependencies, retry |
| "Catalog violation" | Package specifies direct version | Move version to `pnpm-workspace.yaml` catalog |

---

## Integration Points

- **@Architect:** Owns monorepo structure, package boundaries, pipeline design
- **@Backend:** Implements API apps
- **@Frontend:** Implements web apps
- **@QA:** Tests new apps/packages
- **@MetricsAgent:** Tracks cache hit rates, build times, pipeline efficiency

---

*Command Version: 1.0 | Created: 2026-04-08 | Maintained by: @Architect*
