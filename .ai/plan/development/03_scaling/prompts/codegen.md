# 🤖 CODEGEN PROMPT: SaaS Industrial Architect
# Phase: 3 | Status: DRAFT | Reasoning Hash: sha256:saas-codegen-2026-04-23

## 🛠️ Operational Protocol

### 1. Structural Integrity (The Sovereign Rule)
- All generated components must reside in `src/components/`.
- Use **Atomic Design** principles (Atoms, Molecules, Organisms).
- Standard: Tailwind CSS + TypeScript + App Router.

### 2. Pedagogy & Traceability
- Every non-trivial function MUST include a `// #sdd-trace:REQ-XXX` comment mapping it to the spec.
- Provide a "Sovereign Documentation Block" at the top of every new file explaining its role in the ecosystem.

### 3. Regional Compliance (MENA)
- If `region` is active, inject `MENA_COMPLIANCE_GATE` logic.
- Format currency using `Intl.NumberFormat` with support for EGP/SAR/AED.
- Ensure RTL support for all UI elements via Tailwind `rtl:` modifiers.

---

## 📋 Example Component Header

```typescript
/**
 * @component [ComponentName]
 * @role [Description]
 * @trace #sdd-trace:REQ-SAAS-001
 * @owner AIWF Factory v8.0.0
 */
```


# #omega-evolution: v10.0-Refactor-20260423
# Optimization: Enhanced context injection & MENA compliance shims.