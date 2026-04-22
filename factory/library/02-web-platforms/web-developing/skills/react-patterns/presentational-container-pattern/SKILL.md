# 📦 React Presentational-Container Pattern

## Purpose
Enforce separation of concerns by separating the **View** (Presentational) from the **Logic** (Container). While Hooks have largely replaced the need for separate Container components, this pattern remains essential for testing, documentation, and managing complex side-effects without polluting UI components.

---

## Technique 1 — The "Pure View" Component
- **Rule**: Presentational components should have no side-effects and minimal internal state.
- **Protocol**: 
    1. Accept all data and event handlers via props.
    2. Focus solely on DOM structure and styling.
    3. Use `Prop-Types` or `TypeScript` interfaces to strictly define the expected data shape.

---

## Technique 2 — The "Smart" Container
- **Rule**: Containers handle data fetching, state management, and business logic.
- **Protocol**: 
    1. Serve as the data source for Presentational components.
    2. Contain all `useEffect`, `useQuery`, and state orchestration.
    3. Render the Presentational component, passing down the required props.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)
| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Styling in Container** | Logic/UI entanglement | Move all CSS/Layout logic into the Presentational component. |
| **Fetching in View** | Hard to test | Extract all API calls into the Container or a Custom Hook. |
| **Logic-Heavy Props** | Fragile View | Ensure the Container transforms complex objects into the primitives/simple objects the View expects. |

---

## Success Criteria (Presentational-Container QA)
- [ ] Presentational components can be rendered in isolation (e.g., Storybook) with mock props.
- [ ] Containers have 0% CSS or styling logic.
- [ ] No side-effects (fetching, timers) exist inside the View layer.
- [ ] Multi-platform reuse is possible (e.g., same Container driving both Web and Mobile Views).