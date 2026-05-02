---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Accessibility (WCAG 2.1 AA+)

## Purpose
Build all UI components to WCAG 2.1 AA standard minimum, targeting AAA where feasible. Every interactive element must be keyboard-navigable, screen-reader-friendly, and visually distinct. This is non-negotiable — especially for gov-tech projects.

## When to Activate
- Every UI component creation
- Every interactive element (buttons, links, inputs, selects)
- Every form, modal, drawer, dropdown
- Every data table, list, or navigation
- Every loading state or dynamic content update

## Color Contrast Requirements

```
Normal text (<18px, <14px bold):  4.5:1 minimum | 7:1 target (AAA)
Large text (≥18px, ≥14px bold):   3:1 minimum | 4.5:1 target
Interactive elements (borders):    3:1 against adjacent colors
Focus indicators:                  3:1 against adjacent colors
```

### Token Contrast Pairs (Pre-Validated)
```css
/* These token combinations meet AA contrast */
--color-content-primary on --color-surface-primary:   15.8:1 ✅ AAA
--color-content-secondary on --color-surface-primary:  5.2:1 ✅ AA
--color-primary on --color-surface-primary:            7.1:1 ✅ AAA
--color-error on --color-surface-primary:              5.4:1 ✅ AA
```

## ARIA Patterns by Component Type

### Buttons
```tsx
// Icon-only button — must have aria-label
<button
  type="button"
  aria-label={t('actions.deleteBooking')}
  onClick={handleDelete}
>
  <TrashIcon aria-hidden="true" className="size-4" />
</button>

// Loading state
<button
  type="submit"
  aria-busy={isSubmitting}
  disabled={isSubmitting}
>
  {isSubmitting ? t('common.loading') : t('booking.form.submit')}
</button>
```

### Forms
```tsx
<form onSubmit={handleSubmit}>
  <div className="space-y-[var(--space-4)]">
    {/* Visible label linked to input */}
    <label htmlFor="guest-name" className="block font-medium text-[var(--color-content-primary)]">
      {t('form.guestName')}
      <span aria-hidden="true" className="text-[var(--color-error)]"> *</span>
    </label>
    <input
      id="guest-name"
      type="text"
      aria-required="true"
      aria-invalid={!!errors.guestName}
      aria-describedby={errors.guestName ? 'guest-name-error' : undefined}
      autoComplete="name"
      className="..."
    />
    {errors.guestName && (
      <p id="guest-name-error" role="alert" aria-live="polite" className="text-[var(--color-error)]">
        {errors.guestName.message}
      </p>
    )}
  </div>
</form>
```

### Modals / Dialogs
```tsx
// Use <dialog> or radix Dialog — never custom div modals
import * as Dialog from '@radix-ui/react-dialog'

<Dialog.Root open={open} onOpenChange={setOpen}>
  <Dialog.Trigger asChild>
    <button type="button">{t('booking.create')}</button>
  </Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Overlay className="fixed inset-0 bg-[var(--color-surface-overlay)]" />
    <Dialog.Content
      className="..."
      aria-describedby="booking-modal-description"
    >
      <Dialog.Title>{t('booking.modal.title')}</Dialog.Title>
      <Dialog.Description id="booking-modal-description">
        {t('booking.modal.description')}
      </Dialog.Description>
      {/* form content */}
      <Dialog.Close asChild>
        <button type="button" aria-label={t('common.close')}>
          <XIcon aria-hidden="true" />
        </button>
      </Dialog.Close>
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

### Tables
```tsx
<table role="table" aria-label={t('booking.table.ariaLabel')}>
  <caption className="sr-only">{t('booking.table.caption')}</caption>
  <thead>
    <tr>
      <th scope="col" aria-sort="ascending">{t('booking.table.date')}</th>
      <th scope="col">{t('booking.table.guest')}</th>
      <th scope="col">{t('booking.table.status')}</th>
    </tr>
  </thead>
  <tbody>
    {bookings.map(b => (
      <tr key={b.id}>
        <td>{formatDate(b.startsAt)}</td>
        <td>{b.guestName}</td>
        <td>
          <span
            role="status"
            className={cn('badge', `badge-${b.status}`)}
          >
            {t(`booking.status.${b.status}`)}
          </span>
        </td>
      </tr>
    ))}
  </tbody>
</table>
```

### Loading & Live Regions
```tsx
// Announce dynamic content changes to screen readers
<div aria-live="polite" aria-atomic="true" aria-busy={isLoading}>
  {isLoading
    ? <Spinner aria-label={t('common.loading')} />
    : <BookingList bookings={bookings} />
  }
</div>

// Toast notifications
<div role="status" aria-live="polite" aria-atomic="true">
  {toast && <p>{toast.message}</p>}
</div>
```

### Navigation
```tsx
<nav aria-label={t('navigation.main')}>
  <ul role="list">
    <li>
      <a
        href="/dashboard"
        aria-current={isActive('/dashboard') ? 'page' : undefined}
      >
        {t('navigation.dashboard')}
      </a>
    </li>
  </ul>
</nav>

{/* Skip link — must be first focusable element */}
<a
  href="#main-content"
  className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:start-4 focus:z-[var(--z-tooltip)] focus:bg-[var(--color-primary)] focus:text-white focus:px-4 focus:py-2 focus:rounded"
>
  {t('common.skipToContent')}
</a>
```

## Keyboard Navigation Rules

```
Tab:       Move to next focusable element
Shift+Tab: Move to previous focusable element
Enter:     Activate button/link, submit form
Space:     Activate checkbox, button
Escape:    Close modal, dropdown, drawer
Arrow:     Navigate within select, menu, tabs, radio group
Home/End:  First/last item in list or menu
```

### Focus Trap (Modals)
```tsx
// Radix UI handles this automatically
// For custom implementations:
import { useFocusTrap } from '@workspace/ui/hooks/useFocusTrap'

function Modal({ isOpen }: { isOpen: boolean }) {
  const modalRef = useRef<HTMLDivElement>(null)
  useFocusTrap(modalRef, isOpen)
  // ...
}
```

## Focus Visible Styles (Never Remove)
```css
/* packages/ui/src/lib/styles/tokens.css */
/* Override browser default with token-based style */
:focus-visible {
  outline: 2px solid var(--color-border-focus);
  outline-offset: 2px;
  border-radius: var(--radius-sm);
}

/* Never: outline: none without a visible alternative */
```

## Automated Testing
```typescript
// vitest + @axe-core/react
import { axe, toHaveNoViolations } from 'jest-axe'
expect.extend(toHaveNoViolations)

test('BookingCard has no accessibility violations', async () => {
  const { container } = render(<BookingCard booking={mockBooking} />)
  const results = await axe(container)
  expect(results).toHaveNoViolations()
})
```

## Common Mistakes
- `aria-label` on elements that already have visible text — redundant and confusing
- Missing `role="alert"` on error messages — screen readers won't announce them
- Removing `:focus-visible` outline — keyboard users can't navigate
- Using `div` or `span` for interactive elements — use native elements
- Missing `aria-hidden="true"` on decorative icons — clutters screen reader output
- No skip link — sighted keyboard users must tab through entire nav every page

## Success Criteria
- [ ] All interactive elements keyboard-accessible (Tab + Enter/Space)
- [ ] All images have `alt` text (decorative: `alt=""`)
- [ ] All form inputs linked to labels via `htmlFor`/`id`
- [ ] All error messages have `role="alert"` or `aria-live`
- [ ] Skip-to-content link present
- [ ] Modal focus trap working (Tab cycles within modal)
- [ ] Color contrast ≥4.5:1 for all text
- [ ] `axe-core` automated test passes
- [ ] Manual keyboard navigation test passes