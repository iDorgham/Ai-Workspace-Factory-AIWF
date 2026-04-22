# 🏗️ React HOC (Higher-Order Components) Pattern

## Purpose
Enforce standards for cross-cutting concerns using Higher-Order Components. While modern React favors Hooks, HOCs remain vital for certain library integrations and legacy codebase maintenance.

---

## Technique 1 — The "Pure" Wrapper
- **Rule**: Never mutate the original component; always return a new wrapper.
- **Protocol**: 
    1. Pass through all props that aren't specifically used by the HOC.
    2. Coordinate `displayName` for better debugging (e.g., `WithAuth(BaseComponent)`).
    3. Ensure refs are forwarded using `React.forwardRef`.

---

## Technique 2 — Composable Enhancements
- **Composition**: Structure HOCs such that they can be chained (e.g., `compose(withAuth, withLogger)(Component)`).
- **Static Hoisting**: Use `hoist-non-react-statics` to ensure static methods of the wrapped component aren't lost.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **HOC in Render** | Component remounts/State loss | Always define HOC wrappers outside the component's render method. |
| **Prop Collision** | Overwritten data | Prefix HOC-injected props to avoid name clashes with user-passed props. |
| **Ref Loss** | Fragmented DOM access | Always use `forwardRef` in the HOC wrapper. |

---

## Success Criteria (HOC QA)
- [ ] Wrapper preserves all static methods of the child.
- [ ] `displayName` is properly set for DevTools.
- [ ] Prop-passing uses the spread operator for pass-through.
- [ ] No HOCs are defined inside of a component's body.