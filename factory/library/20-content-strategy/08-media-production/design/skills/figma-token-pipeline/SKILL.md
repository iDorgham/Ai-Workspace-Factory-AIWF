---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Figma Token Pipeline

## Purpose
Maintain bidirectional synchronization between Figma design tokens (via Tokens Studio) and code tokens (`tokens.css`). Ensures designers and developers work from the same source of truth.

## When to Activate
- Design system updates in Figma
- Token changes in code
- Brand initialization or rebranding
- Visual discrepancy detected between design and implementation

## Step-by-Step Execution

### 1. Token Architecture

**Figma Tokens Studio Structure:**
```json
// Figma Tokens — exported as tokens.json
{
  "global": {
    "color": {
      "primitive": {
        "blue": {
          "50": { "value": "#eff6ff", "type": "color" },
          "500": { "value": "#3b82f6", "type": "color" },
          "900": { "value": "#1e3a5f", "type": "color" }
        }
      },
      "semantic": {
        "primary": { "value": "{color.primitive.blue.500}", "type": "color" },
        "primaryHover": { "value": "{color.primitive.blue.600}", "type": "color" },
        "surface": { "value": "#ffffff", "type": "color" },
        "content": { "value": "#0f172a", "type": "color" }
      }
    },
    "spacing": {
      "xs": { "value": 6, "type": "spacing" },
      "sm": { "value": 8, "type": "spacing" },
      "md": { "value": 12, "type": "spacing" },
      "lg": { "value": 16, "type": "spacing" },
      "xl": { "value": 24, "type": "spacing" }
    },
    "typography": {
      "heading": {
        "md": { 
          "value": { 
            "fontSize": 24, 
            "lineHeight": 1.3, 
            "fontFamily": "Inter Variable",
            "fontWeight": 600
          },
          "type": "typography"
        }
      }
    },
    "radius": {
      "md": { "value": 6, "type": "borderRadius" },
      "lg": { "value": 8, "type": "borderRadius" },
      "card": { "value": 12, "type": "borderRadius" }
    }
  }
}
```

### 2. Export Pipeline (Figma → Code)

**Step 1 — Export from Figma:**
```bash
# Using Tokens Studio CLI
npx @tokens-studio/cli export \
  --file [figma-file-id] \
  --output .tmp/tokens-figma.json \
  --format tokens
```

**Step 2 — Transform to CSS:**
```typescript
// scripts/tokens/transform-figema-to-css.ts
import { type FigmaTokens } from './types'
import { writeFileSync } from 'fs'

function transformToCSS(figmaTokens: FigmaTokens): string {
  const cssTokens: string[] = [':root {']

  // Colors
  for (const [name, token] of Object.entries(figmaTokens.global.color.semantic)) {
    const value = resolveTokenReference(token.value, figmaTokens)
    cssTokens.push(`  --color-${kebabCase(name)}: ${value};`)
  }

  // Spacing
  for (const [name, token] of Object.entries(figmaTokens.global.spacing)) {
    cssTokens.push(`  --spacing-${name}: ${token.value / 16}rem; /* ${token.value}px */`)
  }

  // Typography
  for (const [name, token] of Object.entries(figmaTokens.global.typography)) {
    const { fontSize, lineHeight, fontFamily, fontWeight } = token.value
    cssTokens.push(
      `  --text-${kebabCase(name)}: ${fontSize / 16}rem / ${lineHeight};`
    )
  }

  // Border Radius
  for (const [name, token] of Object.entries(figmaTokens.global.radius)) {
    cssTokens.push(`  --radius-${name}: ${token.value / 16}rem;`)
  }

  cssTokens.push('}')
  return cssTokens.join('\n')
}

// Generate CSS
const css = transformToCSS(figmaTokens)
writeFileSync('packages/ui/src/lib/styles/tokens.css', css, 'utf-8')
```

**Step 3 — Validate Transformation:**
```bash
# Run validation script
node scripts/tokens/validate.js

# Output:
# ✅ 45 tokens transformed
# ✅ 0 tokens lost
# ✅ All references resolved
# ✅ CSS valid and parseable
```

### 3. Import Pipeline (Code → Figma)

**Step 1 — Parse CSS Tokens:**
```typescript
// scripts/tokens/parse-css.ts
import { parse } from 'css-tree'

function parseCSSToTokens(css: string): Record<string, unknown> {
  const ast = parse(css)
  const tokens: Record<string, unknown> = {}

  ast.rules.forEach(rule => {
    if (rule.type === 'Rule') {
      rule.block.declarations.forEach(declaration => {
        if (declaration.property.startsWith('--')) {
          const name = declaration.property.slice(2) // Remove --
          const value = declaration.value.generate().trim()
          
          setNestedValue(tokens, name, parseCSSValue(value))
        }
      })
    }
  })

  return tokens
}
```

**Step 2 — Transform to Figma Format:**
```typescript
// scripts/tokens/transform-css-to-figma.ts
function transformToFigma(cssTokens: Record<string, unknown>): FigmaTokens {
  return {
    global: {
      color: {
        primitive: extractPrimitiveColors(cssTokens),
        semantic: extractSemanticColors(cssTokens),
      },
      spacing: extractSpacing(cssTokens),
      typography: extractTypography(cssTokens),
      radius: extractRadius(cssTokens),
    }
  }
}
```

**Step 3 — Push to Figma:**
```bash
# Using Tokens Studio API
npx @tokens-studio/cli import \
  --file [figma-file-id] \
  --input .tmp/tokens-figma.json \
  --format tokens \
  --mode update # Update existing tokens, don't create duplicates
```

### 4. Sync Validation

**Check for Drift:**
```typescript
// scripts/tokens/validate-sync.ts
import { readFileSync } from 'fs'

function validateSync(): SyncReport {
  const figmaTokens = JSON.parse(readFileSync('.tmp/tokens-figma.json', 'utf-8'))
  const cssTokens = parseCSS(readFileSync('packages/ui/src/lib/styles/tokens.css', 'utf-8'))
  
  const report: SyncReport = {
    inSync: true,
    figmaOnly: [], // Tokens in Figma but not in CSS
    cssOnly: [],   // Tokens in CSS but not in Figma
    conflicts: [], // Same token, different value
  }

  // Compare token by token
  const allTokens = new Set([
    ...extractAllTokens(figmaTokens),
    ...extractAllTokens(cssTokens),
  ])

  for (const token of allTokens) {
    const figmaValue = getNestedValue(figmaTokens, token)
    const cssValue = getNestedValue(cssTokens, token)

    if (figmaValue && !cssValue) {
      report.figmaOnly.push(token)
      report.inSync = false
    } else if (cssValue && !figmaValue) {
      report.cssOnly.push(token)
      report.inSync = false
    } else if (figmaValue !== cssValue) {
      report.conflicts.push({
        token,
        figmaValue,
        cssValue,
      })
      report.inSync = false
    }
  }

  return report
}
```

**Sync Report Output:**
```markdown
## Token Sync Report

**Date:** [YYYY-MM-DD]
**Status:** ✅ In Sync / ❌ Drift Detected

### Summary
| Category | Count | Tokens |
|----------|-------|--------|
| In sync | [N] | [List] |
| Figma only | [N] | [List] |
| Code only | [N] | [List] |
| Conflicts | [N] | [List] |

### Conflicts Requiring Resolution
| Token | Figma Value | Code Value | Recommended Action |
|-------|-------------|------------|----------------
## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---
|
| [--color-primary] | [#3b82f6] | [#2563eb] | [Update code — Figma is source of truth] |
| [--spacing-lg] | [1.25rem] | [1rem] | [Update Figma — code change intentional] |

### Actions Required
1. [Action to resolve conflict 1]
2. [Action to resolve conflict 2]
```

### 5. Automation (CI/CD Integration)

**GitHub Workflow — Token Sync Check:**
```yaml
# .github/workflows/token-sync.yml
name: Token Sync Check
on:
  pull_request:
    paths:
      - 'packages/ui/src/lib/styles/tokens.css'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pnpm install
      - run: node scripts/tokens/validate-sync.js
        id: sync-check
      - if: steps.sync-check.outputs.inSync == 'false'
        run: |
          echo "❌ Token drift detected"
          cat .tmp/sync-report.md >> $GITHUB_STEP_SUMMARY
          exit 1
```

**Automated Sync Commands:**
```bash
# Figma → Code (designer pushes update)
/brand sync-figma --direction figma-to-code

# Code → Figma (developer adds new token)
/brand sync-figma --direction code-to-figma

# Validate only (CI/CD)
/brand sync-figma --direction validate
```

## Common Mistakes
- Manual token updates — leads to drift between Figma and code
- Not resolving token references — `{color.blue.500}` not expanded
- One-way sync only — both directions needed
- No validation — drift goes undetected
- Updating Figma and code separately — causes conflicts

## Success Criteria
- [ ] Figma tokens exported as JSON
- [ ] All tokens transformed to CSS custom properties
- [ ] Token references resolved (no unresolved `{references}`)
- [ ] CSS valid and parseable
- [ ] No drift between Figma and code (validate script passes)
- [ ] CI/CD checks token sync on PRs
- [ ] Sync direction documented (Figma→Code or Code→Figma)
- [ ] Conflicts resolved before merge