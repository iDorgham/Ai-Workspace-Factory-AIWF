---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# shadcn/ui + Atomic Design + Component Abstraction

## Purpose
Build components using shadcn/ui as a foundation, following Atomic Design principles. Business logic never enters atoms or molecules. All visual customization flows through tokens, never through raw class overrides.

## Atomic Design Hierarchy

```
TOKENS (CSS variables — packages/ui/src/lib/styles/tokens.css)
  ↓
ATOMS (packages/ui/src/components/atoms/)
  Button, Input, Badge, Icon, Avatar, Spinner, Checkbox, Radio
  ↓
MOLECULES (packages/ui/src/components/molecules/)
  FormField, CardHeader, SearchBar, StatusBadge, PriceBadge, DateDisplay
  ↓
ORGANISMS (packages/ui/src/components/ or apps/[app]/src/components/)
  BookingCard, MembershipCard, VenueHeader, DataTable, BookingForm
  ↓
TEMPLATES (apps/[app]/src/components/layouts/)
  DashboardLayout, AuthLayout, MarketingLayout
  ↓
PAGES (apps/[app]/src/app/[route]/page.tsx)
  BookingListPage, MembershipPage, Dashboard
```

## shadcn/ui Installation & Customization

```bash
# Install shadcn components — customize with tokens, not overrides
npx shadcn@latest add button
npx shadcn@latest add dialog
npx shadcn@latest add form
npx shadcn@latest add input
npx shadcn@latest add select
npx shadcn@latest add table
```

```css
/* globals.css — override shadcn via token mapping */
@layer base {
  :root {
    --background:    var(--color-surface-primary);
    --foreground:    var(--color-content-primary);
    --primary:       var(--color-primary);
    --primary-foreground: var(--color-content-inverse);
    --secondary:     var(--color-surface-secondary);
    --muted:         var(--color-surface-secondary);
    --muted-foreground: var(--color-content-secondary);
    --border:        var(--color-border-default);
    --ring:          var(--color-border-focus);
    --radius:        var(--radius-md);
    --destructive:   var(--color-error);
  }
}
```

## Atom Pattern

```tsx
// packages/ui/src/components/atoms/Button/Button.tsx
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@workspace/ui/lib/utils'

const buttonVariants = cva(
  // Base styles — tokens only
  'inline-flex items-center justify-center gap-[var(--space-2)] rounded-[var(--radius-button)] font-medium text-[length:var(--text-label)] transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-border-focus)] disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        primary:   'bg-[var(--color-primary)] text-[var(--color-content-inverse)] hover:bg-[var(--color-primary-hover)]',
        secondary: 'bg-[var(--color-surface-secondary)] text-[var(--color-content-primary)] hover:bg-[var(--color-border-default)]',
        ghost:     'hover:bg-[var(--color-surface-secondary)] text-[var(--color-content-primary)]',
        danger:    'bg-[var(--color-error)] text-white hover:opacity-90',
        luxury:    'bg-[var(--color-accent)] text-[var(--color-content-primary)] hover:bg-[var(--color-accent-hover)] shadow-[var(--shadow-button)]',
      },
      size: {
        sm: 'h-8 px-[var(--space-3)] text-[length:var(--text-body-sm)]',
        md: 'h-10 px-[var(--space-6)]',
        lg: 'h-12 px-[var(--space-8)] text-[length:var(--text-body-lg)]',
      },
    },
    defaultVariants: { variant: 'primary', size: 'md' },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  isLoading?: boolean
  loadingText?: string
}

export function Button({ className, variant, size, isLoading, loadingText, children, ...props }: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size }), className)}
      aria-busy={isLoading}
      disabled={isLoading || props.disabled}
      {...props}
    >
      {isLoading && <Spinner className="size-4" aria-hidden="true" />}
      {isLoading ? loadingText ?? children : children}
    </button>
  )
}
```

## Molecule Pattern

```tsx
// packages/ui/src/components/molecules/FormField/FormField.tsx
// Combines: Label + Input + Error — reusable form building block
import { useTranslations } from 'next-intl'

interface FormFieldProps {
  id:           string
  label:        string
  error?:       string
  required?:    boolean
  children:     React.ReactElement
}

export function FormField({ id, label, error, required, children }: FormFieldProps) {
  const errorId = `${id}-error`

  return (
    <div className="flex flex-col gap-[var(--space-2)]">
      <label htmlFor={id} className="text-[length:var(--text-label)] font-medium text-[var(--color-content-primary)]">
        {label}
        {required && <span aria-hidden="true" className="text-[var(--color-error)] ms-1">*</span>}
      </label>

      {React.cloneElement(children, {
        id,
        'aria-required':   required,
        'aria-invalid':    !!error,
        'aria-describedby': error ? errorId : undefined,
      })}

      {error && (
        <p id={errorId} role="alert" className="text-[length:var(--text-caption)] text-[var(--color-error)]">
          {error}
        </p>
      )}
    </div>
  )
}
```

## Organism Pattern (Domain-Aware)

```tsx
// packages/ui/src/components/organisms/BookingCard/BookingCard.tsx
// Organisms CAN reference domain types — they're assembled from molecules
import type { BookingType } from '@workspace/shared/contracts/booking'
import { useTranslations } from 'next-intl'

interface BookingCardProps {
  booking: BookingType
  onConfirm?: (id: string) => void
  onCancel?: (id: string) => void
}

export function BookingCard({ booking, onConfirm, onCancel }: BookingCardProps) {
  const t = useTranslations('booking')

  return (
    <article
      className="bg-[var(--color-surface-elevated)] rounded-[var(--radius-card)] shadow-[var(--shadow-card)] p-[var(--space-6)]"
      aria-label={t('card.ariaLabel', { guest: booking.guestName })}
    >
      <CardHeader title={booking.guestName} subtitle={booking.venueName} />
      <dl className="grid grid-cols-2 gap-[var(--space-3)] mt-[var(--space-4)]">
        <div>
          <dt className="text-[length:var(--text-caption)] text-[var(--color-content-secondary)]">{t('table.date')}</dt>
          <dd className="text-[length:var(--text-body-sm)] font-medium">{formatDate(booking.startsAt)}</dd>
        </div>
        <div>
          <dt className="text-[length:var(--text-caption)] text-[var(--color-content-secondary)]">{t('table.status')}</dt>
          <dd><StatusBadge status={booking.status} /></dd>
        </div>
      </dl>
      {(onConfirm || onCancel) && (
        <div className="flex gap-[var(--space-3)] mt-[var(--space-6)]">
          {onConfirm && <Button variant="primary" onClick={() => onConfirm(booking.id)}>{t('actions.confirm')}</Button>}
          {onCancel && <Button variant="ghost" onClick={() => onCancel(booking.id)}>{t('actions.cancel')}</Button>}
        </div>
      )}
    </article>
  )
}
```

## File Structure Convention

```
packages/ui/src/components/
├── atoms/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx
│   │   └── index.ts
│   └── Input/...
├── molecules/
│   ├── FormField/...
│   └── StatusBadge/...
└── organisms/
    ├── BookingCard/...
    └── DataTable/...
```

## Common Mistakes
- Business logic (API calls, state management) in atoms or molecules
- Raw Tailwind colors (`text-blue-600`) instead of token vars
- Duplicating shadcn component code — customize via CSS variables in globals.css
- Organisms in `apps/` when they're reusable across apps — they belong in `packages/ui`
- `className` string concatenation without `cn()` — merge conflicts

## Success Criteria
- [ ] Atoms: no domain types, no API calls, tokens only
- [ ] Molecules: composed from atoms, no business logic
- [ ] Organisms: may reference domain types, no direct API calls
- [ ] All shadcn overrides via CSS variables in globals.css
- [ ] Every component file includes test file
- [ ] `compliance` component check passes