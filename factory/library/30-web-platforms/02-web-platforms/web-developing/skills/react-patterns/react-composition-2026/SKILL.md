# 🧩 React Composition 2026

## Purpose
Enforce modular, reusable component design by favoring **Composition** over complex prop configurations. This skill focuses on building flexible UI systems that are easy to extend without bloating component APIs.

---

## Technique 1 — The "Children" Injection Pattern
- **Rule**: Avoid `Boolean` flags for UI variants; use slot-based composition.
- **Protocol**: 
    1. Define Container components that manage layout.
    2. Use the `children` prop for content injection.
    3. Pass "Slots" (custom props that accept JSX) for complex multi-area layouts.

---

## Technique 2 — Component Compounding
- **Namespace Pattern**: Group related components into a single namespace (e.g., `Modal.Header`, `Modal.Content`).
- **Context Sharing**: Use `React.Context` internally to share state between compounded parts without prop drilling.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **"God" Components** | Unmaintainable code | Break down components with > 10 props into smaller, composable units. |
| **Render-Action-Flags** | Rigid APIs | Replace `showIcon={true}` with `<Header icon={<Icon />} />`. |
| **Prop Drilling Context** | Logic leakage | Wrap compounded children in a local Provider hidden inside the parent. |

---

## Success Criteria (Composition QA)
- [ ] Components have a "Flat" prop API (< 5 props for UI logic).
- [ ] No cross-component prop drilling observed.
- [ ] Sub-components are accessible via namespaced exports.
- [ ] Layout is decoupled from content logic.