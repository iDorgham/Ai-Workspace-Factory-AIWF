---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 3D Illusion & Immersive Visual Prompts

## Purpose
Generate and validate 3D illusion visuals, depth effects, and immersive photography prompts for luxury hospitality projects in Hurghada. These assets create the sensory richness that separates premium from generic.

## When to Activate
- Hero sections for luxury venues (dive schools, beach clubs, VIP clubs)
- Feature section backgrounds requiring depth and texture
- Card hover effects suggesting physical dimensionality
- Photography direction for brand assets

## 3D CSS Depth Techniques

### Layered Parallax Hero
```tsx
// packages/ui/src/components/organisms/ImmersiveHero/ImmersiveHero.tsx
export function ImmersiveHero({ heading, subline, cta, videoSrc, imageSrc }: ImmersiveHeroProps) {
  return (
    <section className="relative min-h-[100svh] overflow-hidden isolate">
      {/* Layer 1 — Deepest: background video/image */}
      <div
        className="absolute inset-0 will-change-transform"
        style={{ transform: 'translateZ(-2px) scale(1.5)' }} // CSS 3D parallax
      >
        {videoSrc
          ? <video src={videoSrc} autoPlay muted loop playsInline className="size-full object-cover" />
          : <Image src={imageSrc} alt="" fill className="object-cover" priority />
        }
      </div>

      {/* Layer 2 — Mid: gradient overlay creates depth */}
      <div
        className="absolute inset-0"
        style={{
          background: 'linear-gradient(to bottom, transparent 20%, rgba(11,79,108,0.4) 60%, rgba(11,79,108,0.85) 100%)',
          transform: 'translateZ(-1px) scale(1.25)',
        }}
      />

      {/* Layer 3 — Foreground: content */}
      <div className="relative z-10 flex flex-col items-center justify-end min-h-[100svh] pb-[var(--space-24)] px-[var(--space-8)] text-center">
        <p className="text-[var(--color-accent)] tracking-[0.3em] uppercase text-[length:var(--text-body-sm)] mb-[var(--space-4)]">
          {t('hero.location')}
        </p>
        <h1 className="font-display text-[length:var(--text-display-2xl)] text-white leading-[var(--leading-tight)] mb-[var(--space-6)] drop-shadow-[0_4px_24px_rgba(0,0,0,0.4)]">
          {heading}
        </h1>
        <p className="text-white/80 text-[length:var(--text-body-lg)] max-w-[560px] mb-[var(--space-10)]">
          {subline}
        </p>
        <a href={cta.href} className="btn-luxury">{cta.label}</a>
      </div>
    </section>
  )
}
```

### Card 3D Lift Effect (CSS only)
```css
/* packages/ui/src/lib/styles/components/cards.css */
.card-luxury {
  background: var(--color-surface-elevated);
  border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-card);
  transition:
    transform var(--duration-slow) var(--ease-spring),
    box-shadow var(--duration-slow) var(--ease-out);
  transform-style: preserve-3d;
}

.card-luxury:hover {
  transform: translateY(-8px) rotateX(2deg);
  box-shadow:
    var(--shadow-luxury),
    0 0 0 1px rgba(212, 168, 67, 0.15); /* subtle gold glow */
}

/* Sheen effect on hover */
.card-luxury::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(
    135deg,
    rgba(255,255,255,0.08) 0%,
    transparent 50%,
    transparent 100%
  );
  opacity: 0;
  transition: opacity var(--duration-normal);
}

.card-luxury:hover::after {
  opacity: 1;
}
```

### Glass Morphism (VIP/Overlay elements)
```css
.glass-panel {
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: var(--radius-2xl);
  box-shadow: 0 8px 32px rgba(11, 79, 108, 0.3);
}
```

## AI Image Generation Prompts (Midjourney/DALL-E/Stable Diffusion)

### Red Sea Luxury Dive (Hero)
```
Prompt: "Underwater photography, Red Sea coral reef, crystalline blue-green water,
diver silhouette against sunlight rays piercing the surface, warm golden hour light
diffusing through water, rich saturated blues and teals, depth field bokeh,
professional underwater photography, hyperrealistic, 8K, --ar 16:9 --style raw --q 2"

Negative: "text, watermark, dark, murky, amateur, stock photo aesthetic"
```

### VIP Beach Club (Atmosphere)
```
Prompt: "Luxury beach club at golden hour, Hurghada Red Sea coast, infinity pool
reflecting sunset in deep amber and rose gold, white cabanas with flowing fabric,
elegant guests, palm trees silhouetted, warm cinematic color grading,
architectural photography, wide angle, depth of field, dreamy atmosphere,
editorial quality, --ar 16:9 --style raw"
```

### Interior Luxury Venue (Dining/VIP)
```
Prompt: "High-end restaurant interior, warm ambient lighting, deep navy and gold
color scheme, intimate booth seating, candlelight reflections on polished surfaces,
slight depth of field blur on background, no people, architectural photography,
Hurghada hotel luxury, moody elegant atmosphere, --ar 4:3 --style raw --q 2"
```

### Brand Photography Direction (Art Direction Notes)
```markdown
## Photography Art Direction — [Brand Name]

Color Temperature: Warm (3200–4000K) — golden hour or soft indoor
Composition:  Rule of thirds, horizon at lower third for sky emphasis
Depth:        Shallow depth of field — subject sharp, environment dreamy
Human subjects: Present but not focal — environment is the star
Water:        Must be present in at least 60% of exteriors
Lighting:     Never harsh midday sun — dawn, dusk, or overcast preferred
Post-processing: Slight desaturation + contrast boost + warm highlights
Avoid:        Stock photo staging, fluorescent lighting, busy backgrounds
```

## Validation Checklist (@BrandGuardian)

```markdown
## 3D Visual Quality Review

### Technical Quality
- [ ] No visible compression artifacts
- [ ] No text or watermarks from generation
- [ ] Correct aspect ratio (16:9 hero | 4:3 cards | 1:1 thumbnails)
- [ ] WebP format ≤200KB per image, AVIF fallback available

### Emotional Alignment
- [ ] Image evokes: [target emotion from brand-grammar.md]
- [ ] Color temperature matches brand tokens (warm/cool)
- [ ] Depth/layering creates sense of premium quality
- [ ] Human element creates emotional connection (if required)

### Brand Register
- [ ] Luxury register: environmental immersion, golden light, depth
- [ ] No stock-photo aesthetic (overly perfect, unnatural staging)
- [ ] Red Sea/Hurghada context visible or implied

### 3D CSS Effects
- [ ] Card lift effect ≤400ms transition
- [ ] No jank on hover (will-change: transform on parent)
- [ ] Mobile: 3D effects reduced/disabled (performance)
- [ ] Reduced motion: all transforms disabled (prefers-reduced-motion)
```

## Reduced Motion (Accessibility)
```css
@media (prefers-reduced-motion: reduce) {
  .card-luxury,
  .card-luxury::after {
    transition: none;
    transform: none;
  }
  .card-luxury:hover {
    transform: none;
    box-shadow: var(--shadow-luxury);
  }
}
```

## Common Mistakes
- Heavy 3D CSS causing jank on mid-range mobile devices — test on real devices
- Forgetting `prefers-reduced-motion` — accessibility violation for motion-sensitive users
- AI-generated images with visible artifacts or unnatural proportions
- Over-using 3D effects — one hero + card hover is enough; too much = overwhelm
- 3D on glass panels over busy backgrounds — combine only intentionally

## Success Criteria
- [ ] Hero section uses layered parallax or immersive video
- [ ] Card hover has subtle 3D lift (translateY + shadow change)
- [ ] AI-generated assets pass @BrandGuardian review
- [ ] `prefers-reduced-motion` disables all transforms
- [ ] Performance: no jank on iPhone 12+ and mid-range Android
- [ ] Lighthouse performance ≥95 with 3D effects active