---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Brand Grammar & Emotional Intent Mapping

## Purpose
Every visual and textual element must convey intentional emotion. Sovereign supports two primary emotional registers for the Hurghada market: **Luxury Hospitality** (aspiration, immersion, exclusivity) and **Gov-Tech** (authority, trust, clarity). Each has distinct grammar rules.

## Emotional Registers

### Register 1: Luxury Hospitality / Nightlife
*Used for: beach clubs, dive schools, luxury hotels, VIP venues, nightlife*

```
Emotional Target: Aspiration + Exclusivity + Sensory Immersion
Tone: Sophisticated, evocative, present-tense, first-person invitation
Visual Language: Deep blues, gold accents, generous whitespace, soft shadows
Typography: Elegant display font (Playfair Display / Cormorant) + clean body (Inter)
Motion: Slow fades, subtle parallax, gentle float animations
Copy Rhythm: Short declarative + sensory detail — "Dive into the Red Sea. At dawn."
```

#### Brand Grammar Rules — Luxury
```
✅ Use:
- Present tense: "You arrive..." not "You will arrive..."
- Sensory words: crystalline, salt-kissed, golden hour, velvety, immersive
- Intimate scale: "Your table" not "A table"
- Specific detail: "17 meters below" not "deep dive"
- Active invitation: "Reserve your evening" not "Click here to book"
- Bilingual parity: Same emotion, not literal translation

❌ Avoid:
- Corporate buzzwords: "leveraging", "synergize", "optimize"
- Passive voice: "A room has been reserved" → "Your room awaits"
- Urgency tactics: "Limited time!" "Book now before it's too late!"
- Excessive punctuation: "Amazing!!!" 
- Informal contractions: "gonna", "wanna"
- Price-first messaging: Don't open with cost
```

#### Luxury Component Patterns
```tsx
// Hero section — sensory + aspirational
<section className="relative min-h-[100svh] overflow-hidden">
  <div className="absolute inset-0 bg-gradient-to-b from-[var(--color-primary)]/80 to-[var(--color-primary)]/20" />
  <video autoPlay muted loop playsInline aria-hidden="true" className="absolute inset-0 size-full object-cover" />
  <div className="relative z-10 flex flex-col items-center justify-center min-h-[100svh] text-center px-[var(--space-6)]">
    <p className="text-[var(--color-accent)] text-[length:var(--text-body-sm)] tracking-[0.25em] uppercase mb-[var(--space-4)]">
      {t('hero.eyebrow')} {/* "Red Sea, Hurghada" */}
    </p>
    <h1 className="font-display text-[length:var(--text-display-2xl)] text-white leading-[var(--leading-tight)] mb-[var(--space-6)]">
      {t('hero.headline')} {/* "Where the ocean becomes your world." */}
    </h1>
    <p className="text-white/80 text-[length:var(--text-body-lg)] max-w-[600px] mb-[var(--space-8)]">
      {t('hero.subline')} {/* "Private dive expeditions, dawn to dusk." */}
    </p>
    <a href="#reserve" className="btn-luxury">{t('hero.cta')}</a>
  </div>
</section>
```

### Register 2: Gov-Tech / Enterprise
*Used for: government platforms, public services, enterprise dashboards, compliance tools*

```
Emotional Target: Trust + Authority + Clarity
Tone: Formal, precise, bilingual-first, zero-ambiguity
Visual Language: Professional blues/greys, structured layout, clear hierarchy
Typography: System fonts or Inter — no display fonts
Motion: None or minimal — no decorative animations
Copy Rhythm: Action + Object + Context — "Submit your application online."
```

#### Brand Grammar Rules — Gov-Tech
```
✅ Use:
- Active voice: "Submit your application" not "Applications can be submitted"
- Imperative clarity: "Enter your national ID number"
- Official register: "Ministry of Tourism" not "the tourism people"
- Bilingual simultaneity: Both languages have equal visual hierarchy
- Error clarity: Specific, actionable errors without blame
- Progress indicators: "Step 2 of 5" / "الخطوة ٢ من ٥"

❌ Avoid:
- Jargon: "leverage the platform's affordances"
- Emotional language: "Amazing!" "You're all set!"
- Informal tone: "Hey!" "Quick question..."
- Vague errors: "Something went wrong" → "Your session expired. Please sign in again."
- Decoration over function: No hero videos, no parallax
```

## Visual Emotional Mapping

```
EMOTION          VISUAL SIGNAL               TOKEN
─────────────────────────────────────────────────────────────
Exclusivity   →  Deep navy + gold accent  →  --color-primary + --color-accent
Calm          →  Generous whitespace      →  --space-16 to --space-24 sections
Premium       →  Larger border radius     →  --radius-2xl (luxury) vs --radius-md (default)
Depth         →  Layered shadows          →  --shadow-luxury (0 32px 64px)
Authority     →  High contrast + weight   →  --color-content-primary, font-weight 600+
Trust         →  Consistent system        →  Uniform token usage, no surprises
Energy        →  Gold accent + motion     →  --color-accent + --duration-slow ease-spring
```

## Copy Review Checklist (@BrandGuardian)

```markdown
## Brand Grammar Review

### Emotional Register
- [ ] Correct register identified (luxury vs gov-tech vs hybrid)
- [ ] Tone consistent with register throughout

### Language Quality
- [ ] Active voice ≥85% of sentences
- [ ] No corporate filler words
- [ ] Sensory language present (luxury) OR precision language present (gov-tech)
- [ ] No urgency/scarcity tactics (luxury)

### Bilingual Parity
- [ ] Arabic is not a literal translation — it captures the same emotion
- [ ] Arabic text tested for display issues (letter spacing, line height)
- [ ] Gendered forms correct in Arabic (where applicable)
- [ ] Numbers use Arabic-Indic numerals in Arabic locale (١٢٣ not 123)

### Visual-Copy Harmony
- [ ] Typography scale matches emotional weight of content
- [ ] CTA phrasing matches button hierarchy (primary vs secondary)
- [ ] Error messages follow gov-tech clarity rules
```

## Common Mistakes
- Translating luxury copy literally into Arabic — emotion is lost, cultural register misses
- Using "Buy Now" for luxury — use "Reserve", "Secure", "Discover"
- Gov-tech with decorative elements — undermines authority
- Mixing registers in one project without clear section boundaries
- Ignoring Arabic cultural sensitivities (gender, formal address)

## Success Criteria
- [ ] Brand register documented in project plan
- [ ] All copy reviewed against register checklist
- [ ] Arabic copy reviewed by @I18n for cultural accuracy (not just translation)
- [ ] Visual tokens match emotional register (luxury vs gov-tech profile)
- [ ] `@BrandGuardian` sign-off on every UI PR