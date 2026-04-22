# Pull Request: [Feature Name]

> **PR ID:** #[number]
> **Branch:** `feature/[plan-id]-[slug]` → `develop` / `main`
> **Author:** @AgentName
> **Reviewers:** @Reviewer, @DesignSystem, @Security (as applicable)
> **Created:** [YYYY-MM-DD]
> **Status:** [draft | ready-for-review | in-review | approved | merged | closed]

---

## 1. Summary

**What this PR does:**
[2-3 sentence summary of changes]

**Business value:**
[Why this matters — user impact, revenue, compliance]

**Related Feature Plan:** `.ai/plans/active/features/[feature-name].md`

---

## 2. Changes

### New Files
| File | Purpose |
|------|---------|
| `packages/shared/src/contracts/[domain].ts` | [Contract definition] |
| `apps/web/src/components/[Name].tsx` | [Component description] |
| `apps/api/src/routes/[name].ts` | [API route] |
| `tests/[name].test.ts` | [Test coverage] |

### Modified Files
| File | Change Summary |
|------|----------------|
| `path/to/file.ts` | [What changed and why] |

### Deleted Files
| File | Reason |
|------|--------|
| — | None |

---

## 3. Contract Validation

- [ ] Contract exists and is locked: `packages/shared/src/contracts/[domain].ts` ✅ / ❌
- [ ] All API inputs validated against contract ✅ / ❌
- [ ] All API responses validated against contract ✅ / ❌
- [ ] Frontend forms use `zodResolver` with contract schema ✅ / ❌

**Contract fingerprint:** `sha256:[hash]`
**Lock state:** TRUE ✅

---

## 4. Quality Gate Results

| Gate | Status | Details |
|------|--------|---------|
| `spec:validate` | ✅ / ❌ | [Details] |
| `contract:auto-validate` | ✅ / ❌ | [Details — CI may show `contract:validate`] |
| `compliance` | ✅ / ❌ | Tokens: ✅ | a11y: ✅ | i18n: ✅ | RTL: ✅ |
| `security:scan` | ✅ / ❌ | [N] findings (0 critical) |
| `test` | ✅ / ❌ | Coverage: [N]% |
| `build` | ✅ / ❌ | [passing | failing] |
| Visual regression | ✅ / ❌ | [N] regressions |

---

## 5. Testing

### Test Coverage
```
Unit tests:        [N] passing, [N] failing
Integration tests: [N] passing, [N] failing
E2E tests:         [N] passing, [N] failing
Visual tests:      [N] baselines captured
```

### Manual Testing Checklist
- [ ] Happy path works end-to-end
- [ ] Error states display correctly (with i18n keys)
- [ ] RTL layout renders correctly (Arabic)
- [ ] Keyboard navigation works on all interactive elements
- [ ] Screen reader announces all meaningful changes
- [ ] Mobile responsive (if applicable)
- [ ] Loading/error states implemented

---

## 6. Design System Compliance

- [ ] No raw hex/px values — all design tokens used ✅ / ❌
- [ ] CSS logical properties only (no left/right) ✅ / ❌
- [ ] All user-facing text uses i18n keys ✅ / ❌
- [ ] Components follow atomic design (atom → molecule → organism) ✅ / ❌
- [ ] Brand grammar compliance (if brand context active) ✅ / ❌

---

## 7. Security Review

- [ ] No secrets/tokens in code ✅ / ❌
- [ ] All inputs validated via Zod ✅ / ❌
- [ ] No SQL injection risks (parameterized queries only) ✅ / ❌
- [ ] No XSS risks (proper sanitization) ✅ / ❌
- [ ] Auth checks in place (JWT validation, role checks) ✅ / ❌

---

## 8. Definition of Done

- [ ] All acceptance criteria met (per feature plan)
- [ ] All quality gates passing
- [ ] Tests written and passing
- [ ] No architectural drift detected
- [ ] Documentation updated (if applicable)
- [ ] Ready for deployment to staging

---

## 9. Reviewer Sign-Off

| Reviewer | Status | Comments |
|----------|--------|----------|
| @Reviewer | [approved | changes-requested] | [Notes] |
| @DesignSystem | [approved | changes-requested] | [Notes] |
| @Security | [approved | changes-requested] | [Notes] |
| @BrandGuardian | [approved | changes-requested | N/A] | [Notes] |

**Approved for merge:** ✅ / ❌
**Merged by:** @Automation
**Merged at:** [YYYY-MM-DD HH:MM]

---

*Template Version: 1.0 | Maintained by: @Automation | Auto-generated from feature plans*
