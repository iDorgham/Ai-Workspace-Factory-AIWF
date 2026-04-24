---
cluster: execution
category: commands
display_category: Commands
id: commands:execution/commands/brand
version: 10.0.0
domains: [product-delivery]
sector_compliance: pending
---
# Command: /brand

> **Agent:** @DesignSystem + @BrandGuardian
> **Purpose:** Initialize brand identity, generate design tokens, create component library
> **Scope:** Brand-first design system setup

---

## Usage

```bash
/brand [--name] [--colors hex,hex] [--fonts] [--tone]
/brand sync-figma
/brand audit
```

---

## Execution Flow

### 1. `/brand` — Brand Initialization

**Parameters:**
- `--name [brand-name]`: Optional — brand/project name
- `--colors [hex,hex,...]`: Optional — primary brand colors (comma-separated)
- `--fonts [font-family]`: Optional — primary display font
- `--tone [tone]`: Optional — brand tone/archetype

**Interactive Flow (if parameters not provided):**

**Step 1 — Brand Identity Discovery (@Founder leads for non-technical users):**
```
@DesignSystem asks:

1. "What's your brand or project name?"
2. "Describe your brand in 3 words (e.g., 'Luxurious, Modern, Warm')"
3. "Who is your target audience?"
4. "What emotion should users feel when using your app? (Exclusivity, Confidence, Safety, Energy, Serenity)"
```

**Step 2 — Color Palette Generation:**
```
If --colors provided:
  → Use provided colors as primary palette
  → Generate full semantic palette (50-900 scale) via color algorithm

If no colors provided:
  → Ask: "Do you have brand colors? (hex codes or description)"
  → If yes: Generate palette from provided colors
  → If no: Generate palette based on brand archetype:

| Archetype | Primary | Accent | Neutrals |
|-----------|---------|--------|----------|
| Luxury | Deep navy/gold | Champagne | Warm grays |
| Bold/Energetic | Electric blue/neon | Vibrant accent | Dark backgrounds |
| Gov-Tech/Trust | Navy blue | Sky blue | Cool grays |
| Empowering/Startup | Bright blue/green | Orange/yellow | Light grays |
| Calm/Wellness | Sage green | Soft lavender | Warm whites |
```

**Step 3 — Typography Selection:**
```
@DesignSystem asks:
1. "What's your brand personality? (Modern, Classic, Playful, Serious)"
2. Based on response, recommend font pairings:

| Personality | Display Font | Body Font | Arabic Font |
|-------------|--------------|-----------|-------------|
| Modern | Inter Variable | Inter Variable | Cairo Variable |
| Classic/Luxury | Playfair Display Variable | Source Sans 3 | Noto Sans Arabic |
| Playful | Poppins Variable | Poppins Variable | Tajawal Variable |
| Serious/Gov | IBM Plex Sans Variable | IBM Plex Sans Variable | Noto Sans Arabic |
```

**Step 4 — Tone & Voice:**
```
@Content asks:
1. "How should your app speak to users? (Formal, Conversational, Authoritative, Friendly)"
2. Based on response, set brand grammar rules:

| Tone | Copy Style | CTA Style | Error Messages |
|------|------------|-----------|----------------|
| Formal/Luxury | Elevated, aspirational, short sentences | "Reserve Your Suite" | "Something went wrong. Let's try that again." |
| Conversational/Startup | Friendly, encouraging, plain language | "Get Started Free" | "Oops! Let's try that again." |
| Authoritative/Gov | Clear, direct, jargon-free, bilingual | "Submit Application" | "Error: Please correct the highlighted fields." |
| Friendly/Wellness | Warm, empathetic, supportive | "Begin Your Journey" | "Something didn't work. We're here to help." |
```

**Step 5 — Brand Archetype Assignment:**
```
Based on all inputs, assign brand archetype:

| Archetype | Visual Doctrine | Emotional Intent |
|-----------|-----------------|------------------|
| Luxury/Hospitality | Generous whitespace, dark/deep palettes, serif display, large radius, deep shadows, slow animations | Exclusivity, sophistication |
| Bold/Entertaiment | High contrast, 3D depth, dynamic typography, glow effects, fast animations | Energy, excitement, FOMO |
| Gov-Tech/Enterprise | Restrained palette, clean grid, readable body, subtle shadows, predictable interactions | Trust, authority, clarity |
| Empowering/Startup | Bright, optimistic, bold typography, medium radius, purposeful micro-animations | Confidence, possibility |
| Calm/Wellness | Soft palette, organic shapes, gentle animations, nature-inspired | Serenity, mindfulness |
```

**Step 6 — Generate Brand Configuration:**
```markdown
# Brand Configuration: [brand-name]

**Archetype:** [archetype]
**Primary emotion:** [emotion]
**Visual doctrine:** [doctrine]
**Target audience:** [audience]

## Color Palette
```css
:root {
  --color-primary: [hex];
  --color-primary-hover: [hex];
  --color-primary-active: [hex];
  --color-accent: [hex];
  --color-surface-primary: [hex];
  --color-content-primary: [hex];
  /* ... full semantic palette */
}
```

## Typography
```css
:root {
  --font-family-display: '[font] Variable', system-ui, sans-serif;
  --font-family-sans: '[font] Variable', system-ui, sans-serif;
  --font-family-arabic: '[arabic-font] Variable', 'Noto Sans Arabic', sans-serif;
}
```

## Copy Voice
- **Style:** [tone]
- **CTAs:** [style]
- **Errors:** [style]
- **Forbidden:** [list of words/phrases to avoid]
```

**Step 7 — Generate Token Files:**
```bash
# Create token override file
.ai/context/brands/[brand-name]/
├── brand-grammar.md     ← Brand grammar rules for this brand
├── tokens.css           ← Token overrides for this brand
└── palette.json         ← Full color palette (machine-readable)

# Update project configuration
.ai/context/project-type.md:
  design_system:
    initialized: true
    brand_name: [brand-name]
    primary_color: [hex]
    font_family: [font]
```

**Step 8 — Generate Component Library (Optional — can be done via `/build design-system`):**
```bash
/build design-system
# Generates:
# - packages/ui/src/components/ (atoms, molecules, organisms)
# - packages/ui/src/lib/styles/tokens.css (master token file)
# - Storybook stories for all components
```

**Step 9 — Confirm Brand Setup:**
```markdown
✅ Brand initialized: [brand-name]

**Archetype:** [archetype]
**Primary color:** [hex]
**Display font:** [font]
**Tone:** [tone]

**Generated files:**
- `.ai/context/brands/[brand-name]/brand-grammar.md`
- `.ai/context/brands/[brand-name]/tokens.css`
- `.ai/context/brands/[brand-name]/palette.json`
- `packages/ui/src/lib/styles/tokens.css` (updated with brand colors)

**Next steps:**
1. Run `/build design-system` to generate component library
2. Run `/init --type [type]` to scaffold apps with brand tokens
3. Review brand grammar: `.ai/context/brands/[brand-name]/brand-grammar.md`

**Brand compliance:** @BrandGuardian will validate all future UI against this brand
```

---

### 2. `/brand sync-figma` — Figma ↔ Token Sync

**Purpose:** Bidirectional sync between Figma design tokens and code tokens

**Flow:**
1. Export tokens from Figma (via Figma API or Tokens Studio plugin)
2. Compare Figma tokens with code tokens in `packages/ui/src/lib/styles/tokens.css`
3. Identify differences:
   - Figma has token not in code → add to code
   - Code has token not in Figma → add to Figma
   - Same token, different value → flag for review
4. Generate sync report
5. Apply sync (with user confirmation)

**Output:**
```markdown
## Figma ↔ Token Sync

**Date:** [YYYY-MM-DD]
**Figma file:** [Figma file URL]
**Code tokens:** `packages/ui/src/lib/styles/tokens.css`

### Sync Results
| Action | Count | Details |
|--------|-------|---------|
| Added to code | [N] | [Token names] |
| Added to Figma | [N] | [Token names] |
| Value conflicts | [N] | [Token names — review required] |

### Conflicts Requiring Review
| Token | Figma Value | Code Value | Recommendation |
|-------|-------------|------------|----------------|
| [--color-primary] | [#1A2B3C] | [#2B3C4D] | [Use Figma — designer updated] |

**Sync applied:** ✅ / ❌
**Updated files:** [List]
```

---

### 3. `/brand audit` — Brand Compliance Review

**Purpose:** Check all UI components against brand grammar and tokens

**Flow:**
1. Scan all components in `packages/ui/src/components/` and `apps/web/src/components/`
2. Check for:
   - Raw color values (should use tokens)
   - Wrong fonts (should use brand-approved fonts)
   - Incorrect spacing (should use token spacing)
   - Copy not matching brand voice (should use i18n keys with brand-appropriate copy)
   - Border radius not matching brand doctrine (luxury = large, gov = medium)
   - Animation timing not matching brand energy (luxury = slow, bold = fast)
3. Generate compliance report

**Output:**
```markdown
## Brand Audit: [brand-name]

**Date:** [YYYY-MM-DD]
**Components scanned:** [N]
**Compliance score:** [N]%

### Token Usage
| Check | Pass | Fail | Details |
|-------|------|------|---------|
| Color tokens | [N] | [N] | [Components using raw hex] |
| Spacing tokens | [N] | [N] | [Components using raw px/rem] |
| Typography tokens | [N] | [N] | [Components using wrong fonts] |
| Radius tokens | [N] | [N] | [Components with brand-wrong radius] |

### Brand Grammar
| Check | Pass | Fail | Details |
|-------|------|------|---------|
| Copy tone | [N] | [N] | [Components with off-brand copy] |
| CTA style | [N] | [N] | [Components with wrong CTA style] |
| Error message style | [N] | [N] | [Components with wrong error style] |

### Violations Requiring Fix
| # | Component | Violation | Severity | Fix |
|---|-----------|-----------|----------|-----|
| 1 | [Button.tsx] | [Raw hex: #1A2B3C] | [high] | [Use --color-primary] |

### Recommendations
1. **[Fix N raw color values]** — Replace with design tokens
2. **[Update N copy strings]** — Align with brand voice
3. **[Adjust N animations]** — Match brand energy level

**Next audit:** After next component update or sprint end
```

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| "Brand name already exists" | Brand initialized before | Use existing brand, or delete and reinitialize |
| "Invalid color format" | Color not valid hex | Use format: #RRGGBB or #RRGGBBAA |
| "Font not available" | Font not in approved list | Select from approved font pairings |
| "Token generation failed" | Invalid brand configuration | Review archetype, ensure all fields set |

---

## Integration Points

- **@DesignSystem:** Leads brand initialization, token generation
- **@BrandGuardian:** Validates brand grammar, enforces brand compliance
- **@Content:** Sets copy voice, generates brand-appropriate i18n keys
- **@VisualQA:** Runs visual regression tests with brand baselines
- **@Frontend:** Uses brand tokens in all component generation
- **@Founder:** Guides non-technical users through brand discovery

---

*Command Version: 1.0 | Created: 2026-04-08 | Maintained by: @DesignSystem + @BrandGuardian*
