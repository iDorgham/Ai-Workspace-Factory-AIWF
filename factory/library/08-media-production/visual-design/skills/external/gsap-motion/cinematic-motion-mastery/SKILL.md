# 🎬 GSAP Cinematic Motion Physics

## Purpose
Enforce standards for high-performance, cinematic web animations using the GreenSock Animation Platform (GSAP). This skill focuses on the "Physics-Based" movement model, ScrollTrigger orchestration, and ensuring smooth 60fps interaction on both desktop and mobile.

---

## Technique 1 — Timeline Orchestration (Complex Sequences)
- **Rule**: Never use standalone tweens for multi-step animations; always use `gsap.timeline()` for precise control.
- **Protocol**: 
    1. Define the master timeline.
    2. Add tweens with relative offsets (e.g., `"-=0.5"`).
    3. Use "Labels" to coordinate parallel events (e.g., `tl.addLabel("intro")`).
    4. Control the entire sequence (play, pause, reverse) as a single unit.

---

## Technique 2 — Scroll-Driven Narrative (ScrollTrigger)
- **Rule**: Use `ScrollTrigger` for scroll-bound animations to ensure the narrative unfolds according to the user's focus.
- **Protocol**: 
    1. Scrub animations based on scroll position for "Active Progress" effects.
    2. Use `pin: true` for focus sections to keep content in view during complex transitions.
    3. Implement `anticipatePin` to reduce layout jumps on high-dpi screens.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Animating Performance Killers** | Janky motion (Low FPS) | Only animate `transform` (GPU) and `opacity`. Never animate `top`, `left`, `margin`, or `width`. |
| **Over-Animation** | Motion sickness / Friction | Use "Subtle Micro-interactions" for utility; reserve "Cinematic sequences" for the landing page hero. |
| **Memory Leaks** | Browser crashes | Always clean up (kill) ScrollTriggers and Timelines when components unmount in SPA environments. |

---

## Success Criteria (GSAP QA)
- [ ] 60 FPS maintained throughout all animation cycles.
- [ ] Layout shift (CLS) is 0 during ScrollTrigger pinning.
- [ ] Animations feel "Elastic" and "Alive" (using `back.out` or `power2.out` eases).
- [ ] Reduced Motion query (`prefers-reduced-motion`) is respected (animations are bypassed or simplified).