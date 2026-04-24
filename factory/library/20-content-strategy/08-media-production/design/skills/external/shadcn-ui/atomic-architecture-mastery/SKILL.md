# 🧱 Shadcn UI Atomic Architecture

## Purpose
Enforce standards for high-fidelity component engineering using the "Copy-and-Paste" atomic model. This skill focuses on Radix UI primitives, Tailwind CSS orchestration, and ensuring accessible, themeable components that follow the Sovereign "Cine-Serious" design language.

---

## Technique 1 — Primitive-First Component Logic (Radix)
- **Rule**: Never build complex interactive components (Modals, Selects, Accordions) from scratch; always use **Radix UI Primitives**.
- **Protocol**: 
    1. Import the headless Radix primitive.
    2. Wrap it in a localized Tailwind-styled component.
    3. Expose consistent `className` props to support "Tailwind Merge" (`twMerge`).
    4. Ensure 100% ARIA compliance through Radix's built-in accessibility.

---

## Technique 2 — Tokenized Theming (CSS Variables)
- **Rule**: Use HSL CSS variables for all design tokens (colors, radii, spacing) to enable dynamic dark/light/luxury mode switching.
- **Protocol**: 
    1. Define tokens in `index.css` using the `--primary`, `--background`, `--accent` naming convention.
    2. Map these tokens to Tailwind utilities in `tailwind.config.js`.
    3. Access tokens in components strictly via utility classes (e.g., `bg-primary`, `text-accent`).

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Hard-coded Colors** | Broken Dark Mode | Always use CSS variables; never use `bg-[#ff0000]` in shared components. |
| **Monolithic Prop-Drilling** | Component rigidity | Use the Compound Pattern (e.g., `Dialog.Title`, `Dialog.Content`) to keep components flexible. |
| **Ignoring Focused States** | Accessibility failure | Always style the `focus-visible` ring using standardized theme tokens. |

---

## Success Criteria (Shadcn QA)
- [ ] 100% WCAG 2.1 AA Accessibility on all interactive elements.
- [ ] Dynamic theme switching (Dark/Light) is instantaneous and artifact-free.
- [ ] Mobile-responsive layout maintained through Tailwind's breakpoint system.
- [ ] Components are "Atomic" (Self-contained, minimal external dependencies).
- [ ] RTL (Arabic) layout support verified for all text-heavy components.