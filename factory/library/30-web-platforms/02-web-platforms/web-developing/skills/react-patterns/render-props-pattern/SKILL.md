# 🧩 React Render Props Pattern

## Purpose
Enforce standards for a component's logic sharing using a prop whose value is a function. While largely superseded by Hooks, Render Props remain critical for building certain utility components (e.g., `<MouseTracker />`, `<Query />`) where the component manages state and "renders" whatever the user provides via the function prop.

---

## Technique 1 — The "Function as Child" Pattern
- **Rule**: Use the `children` prop as a function to provide the clearest API.
- **Protocol**: 
    1. Parent manages state/events.
    2. Parent calls `props.children(state)` in its render method.
    3. User implements the View logic inside the callback.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)
| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Render-Props Nesting** | "Callback Hell" | If more than 2-3 render props are nested, transition the logic to **Custom Hooks**. |
| **Non-Stable Functions** | Unnecessary re-renders | If the render-prop function is defined inline in a memoized component, wrap it in `useCallback`. |
| **Ambiguous Prop Naming** | Developer confusion | Use standard naming conventions like `render` or `children` rather than custom names like `componentToRender`. |

---

## Success Criteria (Render Props QA)
- [ ] Pattern correctly shares dynamic state with the consumer.
- [ ] Props passed back to the function are clearly typed and stable.
- [ ] Implementation is focused purely on logic, leaving 100% of UI control to the consumer.