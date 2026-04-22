# Design Token Governance

## Purpose
Use CSS Custom Properties exclusively for all visual values. No raw hex codes, no pixel values, no magic numbers. Design tokens are the single source of truth that enables theming, brand overrides, dark mode, and RTL without code changes.

## When to Activate
- Any time a color, spacing, font size, shadow, border radius, or animation value is used
- When creating new components
- When building brand overrides
- When adding dark mode support

## Token File: Source of Truth

```css
/* packages/ui/src/lib/styles/tokens.css */
:root {
  /* ── PRIMITIVE TOKENS (reference only, never use in components) ── */
  --primitive-navy-50:  #EFF6FF;
  --primitive-navy-700: #1B4F72;
  --primitive-navy-800: #154360;
  --primitive-navy-900: #0E2D42;
  --primitive-gold-400: #D4A843;
  --primitive-gold-500: #B8941F;
  --primitive-sand-100: #FEF9EE;

  /* ── SEMANTIC TOKENS (use in all components) ── */
  --color-primary:           var(--primitive-navy-700);
  --color-primary-hover:     var(--primitive-navy-800);
  --color-primary-active:    var(--primitive-navy-900);
  --color-accent:            var(--primitive-gold-400);
  --color-accent-hover:      var(--primitive-gold-500);

  --color-surface-primary:   #FFFFFF;
  --color-surface-secondary: #F8FAFC;
  --color-surface-elevated:  #FFFFFF;
  --color-surface-overlay:   rgba(15, 23, 42, 0.6);

  --color-content-primary:   #0F172A;
  --color-content-secondary: #64748B;
  --color-content-disabled:  #94A3B8;
  --color-content-inverse:   #FFFFFF;

  --color-border-default:    #E2E8F0;
  --color-border-strong:     #94A3B8;
  --color-border-focus:      var(--color-primary);

  --color-error:             #EF4444;
  --color-warning:           #F59E0B;
  --color-success:           #22C55E;
  --color-info:              #3B82F6;

  /* ── TYPOGRAPHY ── */
  --font-sans:    'Inter Variable', system-ui, sans-serif;
  --font-arabic:  'Cairo Variable', 'Noto Sans Arabic', sans-serif;
  --font-mono:    'JetBrains Mono Variable', monospace;
  --font-display: var(--font-sans);

  --text-display-2xl: clamp(2.5rem, 6vw, 4.5rem);
  --text-display-xl:  clamp(2rem, 5vw, 3.75rem);
  --text-heading-xl:  clamp(1.75rem, 4vw, 2.25rem);
  --text-heading-lg:  clamp(1.5rem, 3vw, 1.875rem);
  --text-heading-md:  clamp(1.25rem, 2.5vw, 1.5rem);
  --text-heading-sm:  clamp(1.125rem, 2vw, 1.25rem);
  --text-body-lg:     1.125rem;
  --text-body-md:     1rem;
  --text-body-sm:     0.875rem;
  --text-caption:     0.75rem;
  --text-label:       0.875rem;

  --leading-tight:    1.2;
  --leading-snug:     1.35;
  --leading-normal:   1.6;
  --leading-relaxed:  1.75;

  /* ── SPACING ── */
  --space-1:   0.25rem;   /* 4px  */
  --space-2:   0.5rem;    /* 8px  */
  --space-3:   0.75rem;   /* 12px */
  --space-4:   1rem;      /* 16px */
  --space-6:   1.5rem;    /* 24px */
  --space-8:   2rem;      /* 32px */
  --space-10:  2.5rem;    /* 40px */
  --space-12:  3rem;      /* 48px */
  --space-16:  4rem;      /* 64px */
  --space-20:  5rem;      /* 80px */
  --space-24:  6rem;      /* 96px */

  /* ── BORDER RADIUS ── */
  --radius-sm:   0.25rem;
  --radius-md:   0.375rem;
  --radius-lg:   0.5rem;
  --radius-xl:   0.75rem;
  --radius-2xl:  1rem;
  --radius-3xl:  1.5rem;
  --radius-full: 9999px;

  /* ── SHADOWS ── */
  --shadow-sm:   0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md:   0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg:   0 10px 15px -3px rgb(0 0 0 / 0.1);
  --shadow-xl:   0 20px 25px -5px rgb(0 0 0 / 0.1);
  --shadow-luxury: 0 32px 64px -12px rgb(27 79 114 / 0.25);

  /* ── ANIMATION ── */
  --duration-fast:   100ms;
  --duration-normal: 200ms;
  --duration-slow:   300ms;
  --ease-default:    cubic-bezier(0.4, 0, 0.2, 1);
  --ease-spring:     cubic-bezier(0.175, 0.885, 0.32, 1.275);

  /* ── Z-INDEX ── */
  --z-dropdown:  100;
  --z-sticky:    200;
  --z-overlay:   300;
  --z-modal:     400;
  --z-toast:     500;
  --z-tooltip:   600;
}
```

## Dark Mode Tokens

```css
/* packages/ui/src/lib/styles/themes/dark.css */
:root[data-theme="dark"] {
  --color-surface-primary:   #0F172A;
  --color-surface-secondary: #1E293B;
  --color-surface-elevated:  #1E293B;
  --color-content-primary:   #F8FAFC;
  --color-content-secondary: #94A3B8;
  --color-border-default:    #334155;
  --color-border-strong:     #475569;
}
```

## Brand Override System

```css
/* packages/ui/src/lib/styles/themes/brand/red-sea-resort.css */
:root[data-brand="red-sea-resort"] {
  --color-primary:        #0B4F6C;
  --color-primary-hover:  #093D54;
  --color-accent:         #D4A843;
  --font-display:         'Playfair Display Variable', serif;
  --radius-card:          var(--radius-2xl);
  --shadow-card:          var(--shadow-luxury);
}

/* Usage: <html data-brand="red-sea-resort"> */
```

## How to Use in Components

```tsx
// ✅ CORRECT — uses tokens
function BookingCard() {
  return (
    <div className="bg-[var(--color-surface-elevated)] rounded-[var(--radius-xl)] shadow-[var(--shadow-md)] p-[var(--space-6)]">
      <h2 className="text-[length:var(--text-heading-md)] text-[var(--color-content-primary)]">
        Dive Experience
      </h2>
      <button className="bg-[var(--color-primary)] hover:bg-[var(--color-primary-hover)] text-[var(--color-content-inverse)] rounded-[var(--radius-md)] px-[var(--space-6)] py-[var(--space-3)]">
        Book Now
      </button>
    </div>
  )
}

// ❌ FORBIDDEN — raw values
function BookingCard() {
  return (
    <div style={{ backgroundColor: '#FFFFFF', borderRadius: '12px', padding: '24px' }}>
      <h2 style={{ fontSize: '20px', color: '#0F172A' }}>Dive Experience</h2>
      <button className="bg-[#1B4F72] text-white rounded-md px-6 py-3">Book Now</button>
    </div>
  )
}
```

## Tailwind CSS v4 Configuration

```css
/* apps/web/src/app/globals.css */
@import "tailwindcss";
@import "@workspace/ui/styles/tokens.css";
@import "@workspace/ui/styles/themes/dark.css";

/* Map tokens to Tailwind theme */
@theme {
  --color-primary:    var(--color-primary);
  --color-accent:     var(--color-accent);
  --color-surface:    var(--color-surface-primary);
  --font-sans:        var(--font-sans);
  --font-arabic:      var(--font-arabic);
  --spacing-*:        var(--space-*);
  --radius-*:         var(--radius-*);
}
```

## compliance Token Check

```bash
# Patterns that fail compliance:
# - Any hex color in .tsx/.ts/.css: #[0-9a-fA-F]{3,8}
# - Any px value not in tokens.css: \d+px
# - Any rgb()/rgba() not in tokens.css
# - Any hardcoded font size not using token
```

## Common Mistakes
- Using `text-blue-600` from Tailwind defaults — use `text-[var(--color-primary)]`
- Setting `style={{ color: '#...' }}` inline — use tokens
- Defining one-off colors in component files — add to tokens.css first
- Forgetting dark mode overrides — every surface and content token needs a dark variant

## Success Criteria
- [ ] `tokens.css` is the only place raw color/spacing values appear
- [ ] All components use `var(--token-name)` for visual properties
- [ ] Dark mode works by toggling `data-theme="dark"` only
- [ ] Brand override works by toggling `data-brand="[name]"` only
- [ ] `compliance` token check passes with zero violations