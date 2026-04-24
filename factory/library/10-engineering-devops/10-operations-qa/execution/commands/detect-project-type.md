---
type: Command
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---


# Command: /detect-project-type

> **Agent:** @Guide + @Architect
> **Purpose:** Analyze workspace and auto-detect project type, set configuration
> **Scope:** Workspace analysis, project-type.md auto-population

---

## Usage

```bash
/detect-project-type
```

---

## Execution Flow

### Analysis Steps

**Step 1 — Scan Workspace Structure:**
```
Check for:
- apps/ directory → What apps exist? (web, api, mobile, desktop)
- packages/ directory → What packages exist? (shared, ui, config)
- Framework indicators in package.json files:
  - "next" → Next.js (web)
  - "react-native" or "expo" → React Native (mobile)
  - "hono" or "fastify" or "express" → Backend API
  - "electron" → Desktop
  - "storybook" → Design system/brand
```

**Step 2 — Analyze Dependencies:**
```
Read package.json files for:
- Frontend indicators: react, next, tailwindcss, shadcn/ui
- Backend indicators: hono, fastify, prisma, postgres
- Mobile indicators: react-native, expo, @react-navigation
- Desktop indicators: electron, @electron-forge
- AI indicators: ai, openai, @ai-sdk, langchain
- Gov-tech indicators: @node-saml, passport-saml, 2fa libs
- Multi-brand indicators: multiple brand directories in .ai/context/brands/
```

**Step 3 — Check Configuration Files:**
```
Read:
- .ai/context/project-type.md → Current configuration (if any)
- pnpm-workspace.yaml → Workspace structure
- turbo.json → Pipeline configuration
- tsconfig.json files → TypeScript setup
```

**Step 4 — Detect Project Type:**
```
Decision tree:

1. Has apps/web AND apps/api? → fullstack
2. Has apps/web only? → web
3. Has apps/api only? → backend
4. Has apps/mobile or react-native? → mobile
5. Has apps/desktop or electron? → desktop
6. Has packages/ui with Storybook but no apps? → brand
7. Has ai/openai/langchain dependencies? → ai-native
8. Has SAML/2fa/gov-compliance libs? → gov-tech
9. Has multiple brands in .ai/context/brands/? → hospitality (multi-brand)
10. Has multiple apps sharing design system? → multi-app
11. Nothing detected? → unknown (manual configuration needed)
```

**Step 5 — Detect Mode:**
```
Analyze user interaction history:
- Mostly business-language questions → founder mode
- Mostly technical questions with code requests → pro mode
- Mix of both → hybrid mode
- Mostly code generation with minimal discussion → build mode

Default: hybrid (adapts based on detected interaction style)
```

**Step 6 — Detect Branching Strategy:**
```
Check git history:
- If main branch only, few commits → founder (trunk-based)
- If main + develop branches → hybrid (GitFlow light)
- If main + develop + release/* + feature/* branches → enterprise (full GitFlow)

Default: hybrid (recommended for most teams)
```

**Step 7 — Generate Configuration:**
```yaml
# .ai/context/project-type.md — update with detected values
project_name: "[Detected or from package.json name field]"
project_type: "[detected type]"
mode: "[detected mode]"
focus: "[build | brand | gov | design — based on recent activity]"

# Preserve existing values from /init when present; only set if missing:
development_methodology:
  primary: "[keep existing | or sovereign-default if absent]"
  notes: "[keep existing]"

initialized: true
initialized_at: "[YYYY-MM-DDTHH:MM:SSZ]"

apps:
  - name: [detected]
    framework: [detected]
    status: [active | pending]

databases:
  - type: [detected or postgres if Prisma present]
    orm: [detected or prisma if schema.prisma exists]
    status: [active | pending]

design_system:
  initialized: [true if packages/ui with tokens.css exists]
  brand_name: [detected from .ai/context/brands/ if exists]
  primary_color: [from tokens.css if exists]
  font_family: [from tokens.css if exists]

branching_strategy: "[detected strategy]"
```

**Step 8 — Present Detection Results:**
```markdown
## Project Type Detected: [type]

**Confidence:** [High | Medium | Low] — based on number of indicators found

### Detection Summary
**Project name:** [name]
**Project type:** [web | mobile | backend | fullstack | brand | ai-native | gov-tech | hospitality | multi-app]
**Mode:** [founder | pro | hybrid | build]
**Branching strategy:** [founder | hybrid | enterprise]

### Evidence
| Indicator | Found | Weight |
|-----------|-------|--------|
| apps/web with Next.js | ✅ | High |
| apps/api with Hono | ✅ | High |
| packages/shared with contracts | ✅ | Medium |
| packages/ui with tokens.css | ✅ | Medium |
| pnpm-workspace.yaml | ✅ | Low |

### Detected Apps
| App | Framework | Status |
|-----|-----------|--------|
| web | Next.js 15 | [active | pending] |
| api | Hono v4 | [active | pending] |

### Detected Database
| Type | ORM | Status |
|------|-----|--------|
| PostgreSQL | Prisma 6 | [active | pending] |

### Design System
| Status | Brand | Primary Color | Font |
|--------|-------|---------------|------|
| [Initialized | Not initialized] | [name] | [hex] | [font] |

### Configuration Updated
✅ `.ai/context/project-type.md` updated with detected values

**If confidence is Low:**
⚠️ Low confidence detection — please review and manually adjust configuration in `.ai/context/project-type.md`

**If confidence is High:**
✅ High confidence detection — configuration auto-applied

### Next Steps
- [If design system not initialized]: Run `/brand` to initialize design system
- [If apps not scaffolded]: Run `/init --type [type]` to scaffold missing apps
- [If ready to build]: Run `/plan [feature-name]` to start first feature
```

**Step 9 — Log Detection:**
```
Append to .ai/memory/decisions.md:
- Detection date, confidence, detected type
- Evidence summary
- Manual adjustments (if any)
```

---

## Manual Override

If detection is incorrect, user can manually set:
```bash
# Manual configuration via /init
/init --type fullstack --mode pro --db postgres

# Or edit directly
# .ai/context/project-type.md — edit project_type field
```

---

## Project Type Definitions

| Type | Required Indicators | Optional Indicators |
|------|---------------------|---------------------|
| **web** | apps/web with Next.js/React | Tailwind, shadcn/ui, next-intl |
| **mobile** | apps/mobile with React Native/Expo | @react-navigation, native modules |
| **backend** | apps/api with Hono/Fastify/NestJS | Prisma, PostgreSQL, JWT auth |
| **fullstack** | apps/web AND apps/api | packages/shared with contracts |
| **brand** | packages/ui with Storybook | No apps, design system only |
| **ai-native** | ai/openai/langchain dependencies | Prompt templates, streaming UI |
| **gov-tech** | SAML/2fa/gov-compliance libs | WCAG libs, i18n with Arabic |
| **hospitality** | Multiple brands in .ai/context/brands/ | Luxury tokens, 3D elements |
| **multi-app** | 3+ apps sharing design system | packages/ui, packages/shared |

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| "No indicators found" | Empty workspace | Run `/init --type [type]` to scaffold |
| "Conflicting indicators" | Mixed project types detected | Review manually, select primary type |
| "Detection failed" | Unrecognized framework | Use manual configuration via `/init` |

---

## Integration Points

- **@Guide:** Coordinates detection, presents results
- **@Architect:** Analyzes architecture, validates detection accuracy
- **@MetricsAgent:** Uses project type for appropriate metrics dashboard
- **@Founder:** Adapts language based on detected mode
- **All agents:** Read project-type.md to adapt behavior

---

*Command Version: 1.0 | Created: 2026-04-08 | Maintained by: @Guide + @Architect*
