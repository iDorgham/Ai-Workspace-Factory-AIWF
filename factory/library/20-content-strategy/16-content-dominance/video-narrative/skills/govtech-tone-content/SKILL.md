---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Gov-Tech Tone & Progressive Disclosure

## Purpose
Government and enterprise platforms require authoritative, precise, bilingual Arabic/English content that builds trust. Progressive disclosure reveals complexity gradually — users see only what they need, when they need it.

## Gov-Tech Writing Principles

### The Four Gov-Tech Pillars
```
1. CLARITY    — One idea per sentence. No ambiguity.
2. AUTHORITY  — Official register. No colloquialisms.
3. EFFICIENCY — Users complete tasks without reading documentation.
4. TRUST      — Consistent terminology. Predictable behavior.
```

### Sentence Construction Rules
```
✅ CORRECT patterns:
- Action + Object: "Submit your application."
- Condition + Action: "If your permit is expired, renew it online."
- Status + Next step: "Your application is under review. You will be notified within 3 business days."
- Error + Resolution: "Your session has expired. Sign in again to continue."

❌ FORBIDDEN patterns:
- Passive voice: "Your application has been received by our team."
  → FIX: "We received your application."
- Corporate jargon: "Leverage the platform's capabilities."
  → FIX: "Use the platform."
- Vague errors: "Something went wrong."
  → FIX: "Your payment was declined. Check your card details and try again."
- Excitement markers: "You're all set!" "Great news!"
  → These undermine authority in formal contexts
```

## Bilingual Gov-Tech Standards

### Equal Visual Hierarchy
```tsx
// ✅ Arabic and English have equal prominence — neither is secondary
<div className="grid grid-cols-1 md:grid-cols-2 gap-[var(--space-6)]">
  <div lang="ar" dir="rtl" className="font-[var(--font-arabic)]">
    <h1 className="text-[length:var(--text-heading-xl)]">تقديم الطلب</h1>
    <p>يرجى إدخال بياناتك للمتابعة.</p>
  </div>
  <div lang="en" dir="ltr">
    <h1 className="text-[length:var(--text-heading-xl)]">Submit Application</h1>
    <p>Enter your details to proceed.</p>
  </div>
</div>

// ❌ Arabic as footnote/smaller text — implies inferiority
<div>
  <h1>Submit Application</h1>
  <small className="text-[var(--color-content-secondary)]">تقديم الطلب</small>
</div>
```

### Egyptian Government Arabic Register
```
Formal address:   يُرجى (formal "please") not لو سمحت (informal)
Official titles:  وزارة السياحة (full official name) not "the ministry"
Numbers:          Arabic-Indic numerals in Arabic text (١٢٣ not 123)
Dates:            Hijri date alongside Gregorian when relevant
Documents:        الرقم القومي (National ID), جواز السفر (Passport)
Status messages:  قيد المراجعة (under review), مقبول (accepted), مرفوض (rejected)
```

## Progressive Disclosure Pattern

### Level 1: Essential Only (Default View)
```tsx
// Show only what's needed to complete the primary task
function ApplicationForm() {
  return (
    <form>
      {/* Only 3 required fields visible by default */}
      <FormField id="national-id" label={t('form.nationalId')} required />
      <FormField id="full-name" label={t('form.fullName')} required />
      <FormField id="email" label={t('form.email')} required />
      
      <ProgressiveSection
        trigger={t('form.optionalDetails')}
        description={t('form.optionalDetailsHint')}
      >
        {/* Advanced fields revealed on demand */}
        <FormField id="mobile" label={t('form.mobile')} />
        <FormField id="address" label={t('form.address')} />
        <FormField id="employer" label={t('form.employer')} />
      </ProgressiveSection>
    </form>
  )
}
```

### Level 2: Help on Demand
```tsx
// Detailed explanations available but not cluttering the UI
<FormField
  id="permit-type"
  label={t('form.permitType')}
  hint={t('form.permitTypeHint')}  // one-line hint visible
>
  <Select>...</Select>
  <HelpPanel
    trigger={t('common.whatIsThis')} // "What is this?"
    content={t('form.permitTypeExplained')} // full explanation hidden until needed
  />
</FormField>
```

### Level 3: Status Communication
```tsx
// Status messages — precise and actionable
const STATUS_MESSAGES = {
  pending: {
    label:  t('status.pending'),       // "Under Review"
    detail: t('status.pendingDetail'), // "Estimated: 3-5 business days"
    action: null,                      // no action needed
  },
  info_required: {
    label:  t('status.infoRequired'),
    detail: t('status.infoRequiredDetail'),
    action: t('status.infoRequiredAction'), // "Provide missing documents"
    actionHref: '/applications/[id]/documents',
  },
  rejected: {
    label:  t('status.rejected'),
    detail: t('status.rejectedReason'), // specific reason
    action: t('status.rejectedAction'), // "Appeal this decision" or "Reapply"
  },
}
```

## Error Message Standards

```typescript
// Gov-tech error messages: specific, actionable, bilingual
const GOV_ERRORS = {
  'national_id_invalid': {
    en: 'Your National ID must be 14 digits. Example: 29801011234567',
    ar: 'يجب أن يتكون الرقم القومي من 14 رقمًا. مثال: 29801011234567',
  },
  'session_expired': {
    en: 'Your session expired after 30 minutes of inactivity. Sign in to continue.',
    ar: 'انتهت جلستك بعد 30 دقيقة من عدم النشاط. سجّل دخولك للمتابعة.',
  },
  'document_too_large': {
    en: 'Document exceeds the 5 MB size limit. Compress the file and try again.',
    ar: 'حجم المستند يتجاوز 5 ميغابايت. قلّل حجم الملف وحاول مرة أخرى.',
  },
}
```

## Common Mistakes
- "Conversational" Arabic that sounds informal in a government context
- English-only error messages — Arabic users see untranslated errors
- Showing all form fields upfront — overwhelms users, reduces completion rates
- Vague status messages without timeline or next action
- Mixing formal and informal register within the same interface

## Success Criteria
- [ ] All copy reviewed against gov-tech tone rules
- [ ] Arabic and English have equal visual prominence
- [ ] Progressive disclosure: ≤5 fields visible by default, rest on demand
- [ ] All error messages are specific and actionable
- [ ] Status messages include timeline and next step
- [ ] @Content sign-off on all gov-tech copy before shipping