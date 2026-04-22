# 🧩 React Compound Pattern

## Purpose
Enforce standards for building complex components that share state implicitly. This skill focuses on the "Select/Option" or "Tabs" model, where a parent coordinate sub-components without requiring the developer to pass state manually between them.

---

## Technique 1 — Internal Context Coordination
- **Rule**: Use a local `React.Context` to share state between the parent and its children.
- **Protocol**: 
    1. Define a Parent component (e.g., `<Tabs />`).
    2. Define sub-components as static properties (e.g., `<Tabs.List />`, `<Tabs.Trigger />`).
    3. Use a custom hook (`useTabsContext`) inside children to consume the shared state.

---

## Technique 2 — Implicit Prop Injection (Legacy)
- **React.Children.map**: Occasionally used for simpler compounds where state is injected via `cloneElement`, though Context is preferred for deep nesting.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)
| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Loose Children** | Logic break | Wrap children in a `Provider` and check for its existence in sub-components; throw helpful errors if children are used outside the parent. |
| **Over-Exporting State** | API bloat | Keep the "Active Index" or "Open" state inside the compound; only export `onChange` for external consumers. |
| **Fragile Ordering** | UI bugs | Design the pattern so the order of child components doesn't break the logic (using Context identifiers). |

---

## Success Criteria (Compound QA)
- [ ] Components are usable as `<Parent><Parent.Child /></Parent>`.
- [ ] No manual prop-drilling required for standard behavior.
- [ ] Sub-components throw clear errors when used outside of the parent.
- [ ] Accessible `aria-*` attributes are managed automatically by the parent.