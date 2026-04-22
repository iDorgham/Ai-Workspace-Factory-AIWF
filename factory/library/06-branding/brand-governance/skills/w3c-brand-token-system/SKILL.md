# 🏗️ W3C Brand Token System (Design-to-Code)

## Purpose
Enforce professional standards for brand governance through "Design Tokens." This skill focuses on the **W3C Design Token Community Group (DTCG)** standard to ensure 1:1 synchronization between **Figma** designs and **Tailwind/CSS** implementation.

---

## Technique 1 — Token Hierarchy (The "CoreThree" levels)

### 1. Primitive Tokens (Global)
- **Definition**: The raw values of the brand (e.g., `color-blue-500`, `font-size-base`).
- **Rule**: Never use Primitives directly in UI. They are the "source of truth" but carry no semantic meaning.

### 2. Semantic Tokens (Contextual)
- **Definition**: Mapping primitives to meaning (e.g., `action-primary-color`, `text-header-large`).
- **Rule**: These are the "Workhorse" tokens. Use these for 90% of all design and development work.

### 3. Component Tokens (Specific)
- **Definition**: Tokens tied to a specific UI element (e.g., `button-primary-background-hover`).
- **Rule**: Use only for high-complexity components with specific state variations.

---

## Technique 2 — Figma to Tailwind Pipeline

- **Naming Convention**: Use kebab-case following the `category-type-item-state` pattern (e.g., `color-brand-primary-hover`).
- **Standard**: All tokens must be exportable via **Style Dictionary** format to ensure they can be consumed by both JSON-based Figma plugins and CSS variable files.

---

## Technique 3 — Typography & Spacing Tokens

### Proportional Relationships
- **Scale**: Use a **Modular Scale** (e.g., 1.250 Major Third) for font sizes to ensure mathematical harmony.
- **Rhythm**: Map spacing tokens to the **8pt Grid** (e.g., `space-1` = 4px, `space-2` = 8px).

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Ad-hoc Hex Codes** | Brand Drift / Visual Debt | Every color must be linked to a Semantic Token. No hardcoded hex values. |
| **Inconsistent Naming** | Friction between teams | Enforce the `category-type-item` naming convention across Figma and CSS. |
| **Missing Dark Mode logic** | Accessibility failure | Every Semantic Token must have a defined **Alias** for Dark Mode themes. |

---

## Success Criteria (Token QA)
- [ ] JSON export passes W3C Token validation.
- [ ] Tailwind config correctly imports all Semantic Tokens.
- [ ] Figma styles are 1:1 mapped to the Code implementation.
- [ ] Modular scale for typography is mathematically consistent.