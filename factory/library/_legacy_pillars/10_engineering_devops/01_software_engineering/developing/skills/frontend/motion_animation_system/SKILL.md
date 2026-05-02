---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Motion & Animation System

## Purpose

Implement production-grade motion and animation for React/Next.js applications using Framer Motion as the primary library, with CSS animations for simple cases and SVG animation patterns for complex graphics. This skill consolidates 8 fragmented animation files into one comprehensive motion system — covering philosophy, spring physics, layout transitions, scroll-linked effects, page transitions, RTL-aware animation, and performance budgets.

**Measurable Impact:**
- Before: 8 separate 45-65 line animation files → agents load wrong one, miss context
- After: Single motion system → correct pattern found in one lookup
- Before: Overanimated UIs → 15-20% slower FCP, janky on mobile
- After: Performance-budgeted animation → <100ms added to FCP, 60fps on mid-tier devices
- Before: CSS transitions for complex layout shifts → layout thrashing, jitter
- After: Framer Motion layout + spring physics → buttery smooth morphs

**Consolidates:** `framer-motion`, `motion-philosophy`, `motion-primitives`, `svg-animation`, `animejs`, `creative-animation`, `analytics-animation`, `uiux-animator`

---

## Core Principles — Motion Philosophy

```markdown
## When to Animate (Decision Framework)

ANIMATE when:
  ✅ Element changes context (nav → detail view, card → modal)
  ✅ Element enters/exits the DOM (list item add/remove)
  ✅ State change needs visual feedback (toggle, tab switch)
  ✅ Scroll position affects element meaning (sticky header, parallax)
  ✅ User needs orientation (where did I come from? where am I going?)

DO NOT animate:
  ❌ Static content that doesn't change state
  ❌ Every single element on page load (Christmas tree effect)
  ❌ Animations that block user interaction (forced delays)
  ❌ Decorative motion with no purpose (spinning logos)
  ❌ Animations on print or reduced-motion preference

## RTL Animation Rules (MENA)
  - Slide-in from inline-start (right in RTL, left in LTR)
  - Progress bars fill from inline-end to inline-start
  - Carousels swipe direction reverses
  - Use logical x values: `x: isRTL ? 20 : -20` for enter animations
```

---

## Technique 1 — Spring Physics & Timing Tokens

### Standard Motion Presets

```typescript
// lib/motion.ts — Animation system constants
import type { Transition, Variants } from 'framer-motion';

// --- SPRING PRESETS ---
// Use springs for ALL structural UI motion (not duration/ease)
export const springs = {
  // Smooth: Default for most transitions (modal open, page change)
  smooth: { type: 'spring', stiffness: 100, damping: 20 } as Transition,
  
  // Snappy: Small UI elements (button press, toggle, tooltip)
  snappy: { type: 'spring', stiffness: 300, damping: 30 } as Transition,
  
  // Bouncy: Playful elements (badge pop, notification, success state)
  bouncy: { type: 'spring', stiffness: 400, damping: 15 } as Transition,
  
  // Gentle: Large structural changes (page transition, layout shift)
  gentle: { type: 'spring', stiffness: 60, damping: 15 } as Transition,
  
  // Stiff: Immediate response (drag release, snap to position)
  stiff: { type: 'spring', stiffness: 500, damping: 35 } as Transition,
} as const;

// --- DURATION PRESETS (CSS fallback, non-physics) ---
export const durations = {
  instant: 0.1,    // Tooltip show, hover state
  fast: 0.2,       // Button state, icon swap
  normal: 0.3,     // Modal open, dropdown, accordion
  slow: 0.5,       // Page transition, hero reveal
  glacial: 0.8,    // Full-screen animations only
} as const;

// --- STAGGER ---
export const stagger = {
  fast: 0.03,      // Tight list items (search results)
  normal: 0.05,    // Standard lists, grid items
  dramatic: 0.1,   // Hero sections, feature showcases
} as const;

// --- FADE + SLIDE VARIANTS ---
export const fadeUp: Variants = {
  hidden: { opacity: 0, y: 12 },
  visible: { opacity: 1, y: 0, transition: springs.smooth },
  exit: { opacity: 0, y: -8, transition: { duration: durations.fast } },
};

export const fadeInScale: Variants = {
  hidden: { opacity: 0, scale: 0.95 },
  visible: { opacity: 1, scale: 1, transition: springs.snappy },
  exit: { opacity: 0, scale: 0.95, transition: { duration: durations.fast } },
};

// RTL-aware slide variant factory
export const slideIn = (direction: 'start' | 'end', isRTL = false): Variants => {
  const x = direction === 'start' 
    ? (isRTL ? 20 : -20) 
    : (isRTL ? -20 : 20);
  return {
    hidden: { opacity: 0, x },
    visible: { opacity: 1, x: 0, transition: springs.smooth },
    exit: { opacity: 0, x: x * -0.5, transition: { duration: durations.fast } },
  };
};
```

---

## Technique 2 — Layout Transitions & Shared Elements

### Layout Animation Pattern

```tsx
// LayoutId morphing: card → modal seamlessly
import { motion, AnimatePresence } from 'framer-motion';
import { springs } from '@/lib/motion';

interface MorphCardProps {
  id: string;
  title: string;
  isExpanded: boolean;
  onToggle: () => void;
  children: React.ReactNode;
}

export function MorphCard({ id, title, isExpanded, onToggle, children }: MorphCardProps) {
  return (
    <motion.div
      layoutId={`card-${id}`}
      onClick={onToggle}
      transition={springs.smooth}
      className={isExpanded ? 'fixed inset-4 z-50' : 'relative'}
      style={{ borderRadius: isExpanded ? 16 : 12 }}
    >
      {/* Title morphs between compact and expanded */}
      <motion.h3 layout="position" className="text-lg font-semibold">
        {title}
      </motion.h3>
      
      {/* Content fades in only when expanded */}
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ delay: 0.1, duration: 0.2 }}
          >
            {children}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

// Overlay backdrop for expanded card
export function CardOverlay({ isVisible, onClose }: { isVisible: boolean; onClose: () => void }) {
  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="fixed inset-0 bg-black/50 z-40"
        />
      )}
    </AnimatePresence>
  );
}
```

### AnimatePresence List Pattern

```tsx
// Animated list with stagger and exit animations
import { motion, AnimatePresence } from 'framer-motion';
import { springs, stagger, fadeUp } from '@/lib/motion';

interface AnimatedListProps<T> {
  items: T[];
  keyExtractor: (item: T) => string;
  renderItem: (item: T) => React.ReactNode;
}

export function AnimatedList<T>({ items, keyExtractor, renderItem }: AnimatedListProps<T>) {
  return (
    <AnimatePresence mode="popLayout">
      {items.map((item, index) => (
        <motion.div
          key={keyExtractor(item)}
          layout
          variants={fadeUp}
          initial="hidden"
          animate="visible"
          exit="exit"
          transition={{
            ...springs.snappy,
            delay: index * stagger.fast,
          }}
        >
          {renderItem(item)}
        </motion.div>
      ))}
    </AnimatePresence>
  );
}
```

---

## Technique 3 — Scroll-Linked & Parallax Effects

### Scroll Progress Animations

```tsx
import { motion, useScroll, useTransform, useSpring } from 'framer-motion';
import { useRef } from 'react';

// Scroll-linked sticky header with blur
export function DynamicHeader() {
  const { scrollYProgress } = useScroll();
  const headerOpacity = useTransform(scrollYProgress, [0, 0.05], [1, 0.95]);
  const blur = useTransform(scrollYProgress, [0, 0.05], [0, 12]);
  const springBlur = useSpring(blur, { stiffness: 100, damping: 20 });
  
  return (
    <motion.header
      style={{
        opacity: headerOpacity,
        backdropFilter: useTransform(springBlur, v => `blur(${v}px)`),
      }}
      className="sticky top-0 z-50 border-b border-border/50"
    >
      {/* Header content */}
    </motion.header>
  );
}

// Section reveal on scroll (for landing pages / marketing)
export function ScrollReveal({ children, delay = 0 }: { children: React.ReactNode; delay?: number }) {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ['start 0.8', 'start 0.3'], // Trigger between 80% and 30% viewport
  });
  
  const opacity = useTransform(scrollYProgress, [0, 1], [0, 1]);
  const y = useTransform(scrollYProgress, [0, 1], [40, 0]);
  const springY = useSpring(y, { stiffness: 80, damping: 20 });
  
  return (
    <motion.div ref={ref} style={{ opacity, y: springY }}>
      {children}
    </motion.div>
  );
}

// Parallax speed layer
export function ParallaxLayer({ children, speed = 0.5 }: { children: React.ReactNode; speed?: number }) {
  const { scrollYProgress } = useScroll();
  const y = useTransform(scrollYProgress, [0, 1], ['0%', `${speed * 100}%`]);
  
  return <motion.div style={{ y }}>{children}</motion.div>;
}
```

---

## Technique 4 — Page & Route Transitions

### Next.js Page Transition Pattern

```tsx
// app/template.tsx — Wraps all pages with enter/exit animation
'use client';
import { motion, AnimatePresence } from 'framer-motion';
import { usePathname } from 'next/navigation';
import { springs } from '@/lib/motion';

export default function Template({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={pathname}
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -8 }}
        transition={springs.smooth}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}
```

### SVG Path Animation

```tsx
// Animated SVG drawing effect (for icons, illustrations)
import { motion } from 'framer-motion';

export function AnimatedCheckmark({ isVisible }: { isVisible: boolean }) {
  return (
    <AnimatePresence>
      {isVisible && (
        <motion.svg viewBox="0 0 24 24" width={24} height={24}>
          <motion.path
            d="M5 13l4 4L19 7"
            fill="none"
            stroke="currentColor"
            strokeWidth={2}
            strokeLinecap="round"
            strokeLinejoin="round"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{ pathLength: 1, opacity: 1 }}
            exit={{ pathLength: 0, opacity: 0 }}
            transition={{ duration: 0.4, ease: 'easeInOut' }}
          />
        </motion.svg>
      )}
    </AnimatePresence>
  );
}
```

---

## Performance Budget & Accessibility

```markdown
## Animation Performance Rules (Non-Negotiable)

### Only animate composite properties:
  ✅ transform (translate, scale, rotate)
  ✅ opacity
  ❌ width, height, top, left (trigger layout recalculation)
  ❌ margin, padding (trigger layout)
  ❌ border-radius changes > 0→X (use scale instead)
  Exception: `layout` prop in Framer Motion handles layout safely

### Bundle budget:
  framer-motion: ~30KB gzipped (acceptable as primary motion library)
  Do NOT additionally import: anime.js, GSAP, Lottie (unless specific need)
  Prefer CSS animations for simple hover/focus states

### Mobile performance:
  - Max 3 simultaneously animating elements on mobile
  - Disable parallax on mobile (performance + motion sickness)
  - Test on mid-tier Android device (not just iPhone 15 Pro)
  - Use `will-change: transform` sparingly (GPU memory cost)

### Accessibility (prefers-reduced-motion):
  MANDATORY: Respect user's reduced-motion preference

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

```tsx
// In React — disable animations for reduced-motion users
import { useReducedMotion } from 'framer-motion';

export function AnimatedComponent() {
  const shouldReduce = useReducedMotion();
  
  return (
    <motion.div
      initial={shouldReduce ? false : { opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={shouldReduce ? { duration: 0 } : springs.smooth}
    >
      Content
    </motion.div>
  );
}
```
```

---

## Anti-Pattern Catalog

| ID | Anti-Pattern | Risk | Fix |
|----|-------------|------|-----|
| MOT-001 | Animating width/height directly | **HIGH** — Layout thrashing, 10-30fps drops | Use `scale` transform or Framer `layout` prop |
| MOT-002 | CSS transitions for layout shifts | **HIGH** — Jitter, no exit animation | Use Framer Motion `layout` + `AnimatePresence` |
| MOT-003 | Duration-based timing for structural UI | **MEDIUM** — Feels sluggish, unresponsive | Use spring physics (stiffness/damping) |
| MOT-004 | Animating everything (Christmas tree) | **HIGH** — Overwhelming, performance-killing | Animate state changes only; still elements stay still |
| MOT-005 | Missing `prefers-reduced-motion` check | **HIGH** — Accessibility violation (WCAG 2.3.3) | Always check `useReducedMotion`; CSS fallback |
| MOT-006 | LTR-only slide direction | **MEDIUM** — Feels wrong in RTL layout | Use `slideIn('start', isRTL)` factory |
| MOT-007 | Importing multiple animation libraries | **HIGH** — 60-100KB unnecessary bundle bloat | Pick one: Framer Motion for React; CSS for simple states |
| MOT-008 | No `AnimatePresence` on conditional render | **MEDIUM** — Element pops out abruptly | Always wrap conditionally rendered animated elements |
| MOT-009 | `key` changing unnecessarily on lists | **HIGH** — Destroys layout animation, causes flicker | Stable keys from data IDs, never from array index |

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Success Criteria

- [ ] All animation constants defined in `lib/motion.ts` — no inline magic numbers
- [ ] Spring presets used for structural transitions (not `duration` + `ease`)
- [ ] `AnimatePresence` wrapping all conditionally rendered animated elements
- [ ] `prefers-reduced-motion` respected (CSS + React hook)
- [ ] RTL-aware slide variants used for Arabic locale animations
- [ ] Only `transform` and `opacity` animated (no width/height/top/left)
- [ ] Maximum 1 animation library imported (Framer Motion preferred)
- [ ] Mobile tested: 60fps on mid-tier Android with max 3 simultaneous animations
- [ ] SVG path animation used for icon reveals (checkmarks, progress indicators)
- [ ] Page transitions via `template.tsx` with `AnimatePresence mode="wait"`