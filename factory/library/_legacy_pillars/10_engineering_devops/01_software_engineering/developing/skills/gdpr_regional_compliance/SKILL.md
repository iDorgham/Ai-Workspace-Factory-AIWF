---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# GDPR & Regional Compliance (Egypt/GCC)

## Purpose
Handle personal data according to GDPR principles and Egypt's Personal Data Protection Law (PDPL). Critical for Hurghada hospitality businesses that serve EU tourists and must demonstrate data governance to international partners.

## Applicable Regulations

```
GDPR (EU)           — Applies to EU guests at Hurghada properties
Egypt PDPL 2020     — Applies to all data collected in Egypt
Saudi PDPL          — Applies to KSA guests/transactions
UAE PDPA            — Applies when serving UAE nationals
PCI-DSS             — Applies whenever payment card data is processed
```

## Data Classification Schema

```typescript
// packages/shared/src/contracts/data-classification.ts
export const DataClassificationSchema = z.object({
  level: z.enum([
    'public',          // No restrictions
    'internal',        // Company use only
    'confidential',    // Named individuals only
    'restricted',      // Executive + legal only
  ]),
  personalData: z.boolean(),
  sensitiveCategory: z.enum([
    'none',
    'health',          // Medical conditions, fitness data
    'financial',       // Payment cards, bank accounts
    'biometric',       // Fingerprints, face ID
    'identity',        // National ID, passport
    'location',        // GPS, address history
  ]).optional(),
  retentionDays: z.number().int().positive(),
  encryptAtRest: z.boolean(),
  auditLogged: z.boolean(),
})
```

## Personal Data Handling

```typescript
// packages/database/src/schema/guest.prisma
// Annotate sensitive fields for compliance tooling
model Guest {
  id          String   @id @default(cuid())
  email       String   @unique // PII — encrypted at rest
  phone       String?           // PII — encrypted at rest
  fullName    String            // PII
  nationalId  String?           // Sensitive — encrypted + restricted
  passportNo  String?           // Sensitive — encrypted + restricted
  dateOfBirth DateTime?         // PII
  createdAt   DateTime @default(now())
  deletedAt   DateTime?         // Soft delete for right-to-erasure

  // Audit trail
  dataConsent     Boolean  @default(false)
  consentDate     DateTime?
  consentVersion  String?
  marketingOptIn  Boolean  @default(false)
}
```

## Right to Erasure (Right to be Forgotten)

```typescript
// apps/api/src/services/gdpr.service.ts
export async function anonymizeGuest(guestId: string, requestedBy: string) {
  // Log the erasure request (keep for 7 years per audit requirements)
  await auditLog.create({
    action:      'gdpr.erasure_request',
    subjectId:   guestId,
    requestedBy,
    timestamp:   new Date().toISOString(),
  })

  // Anonymize — don't fully delete (breaks referential integrity)
  await prisma.guest.update({
    where: { id: guestId },
    data: {
      email:       `deleted-${guestId}@anonymized.local`,
      phone:       null,
      fullName:    'Deleted User',
      nationalId:  null,
      passportNo:  null,
      dateOfBirth: null,
      deletedAt:   new Date(),
      dataConsent: false,
    }
  })

  // Keep booking records (financial obligation) but unlink personal data
  await prisma.booking.updateMany({
    where: { guestId },
    data: { guestSnapshot: null } // remove any cached guest PII
  })
}
```

## Data Portability (GDPR Article 20)

```typescript
// apps/api/src/routes/gdpr.ts
auth.get('/my-data', requireAuth, async (c) => {
  const userId = c.get('user').sub

  const [guest, bookings, memberships] = await Promise.all([
    prisma.guest.findUnique({ where: { id: userId } }),
    prisma.booking.findMany({ where: { guestId: userId } }),
    prisma.membership.findMany({ where: { memberId: userId } }),
  ])

  // Return machine-readable export (GDPR Article 20)
  return c.json({
    exportedAt: new Date().toISOString(),
    subject:    userId,
    data: {
      profile:     sanitizeGuestExport(guest),
      bookings:    bookings.map(sanitizeBookingExport),
      memberships: memberships.map(sanitizeMembershipExport),
    }
  })
})
```

## Consent Management

```typescript
// packages/shared/src/contracts/consent.ts
export const ConsentSchema = z.object({
  guestId:            z.string().uuid(),
  consentVersion:     z.string(),  // "v1.2" — tied to privacy policy version
  purposes: z.object({
    essentialServices:    z.literal(true),  // cannot opt out
    marketingEmails:      z.boolean(),
    analyticsTracking:    z.boolean(),
    thirdPartySharing:    z.boolean(),
  }),
  ipAddress:  z.string().ip(),
  userAgent:  z.string().max(500),
  timestamp:  z.string().datetime(),
  locale:     z.enum(['en', 'ar']),
})
```

## Data Retention Policies

```markdown
## Retention Schedule

| Data Type               | Retention    | Legal Basis                    |
|-------------------------|--------------|-----------------------------
## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---
|
| Booking records         | 7 years      | Tax/financial obligation       |
| Payment records         | 7 years      | PCI-DSS + tax                  |
| Guest profiles          | 3 years      | Service delivery               |
| Marketing consent       | Until revoked| GDPR consent                   |
| Security audit logs     | 2 years      | Security investigation         |
| Support tickets         | 3 years      | Service records                |
| National ID/Passport    | 1 year       | KYC requirement                |
| Health/biometric data   | 90 days      | Minimum necessary              |
```

## Automated Retention Cleanup

```typescript
// apps/api/src/jobs/retention.ts — runs daily
export async function enforceRetentionPolicies() {
  const threeYearsAgo = subYears(new Date(), 3)

  // Anonymize old guest profiles (not delete — preserve bookings)
  const expiredGuests = await prisma.guest.findMany({
    where: {
      deletedAt: null,
      createdAt: { lt: threeYearsAgo },
      bookings: { none: { createdAt: { gt: threeYearsAgo } } },
    }
  })

  for (const guest of expiredGuests) {
    await anonymizeGuest(guest.id, 'retention-automation')
  }

  // Log audit trail
  auditLog.info({ event: 'retention.cleanup', count: expiredGuests.length })
}
```

## Common Mistakes
- Storing national IDs in plaintext — always encrypt sensitive identity data
- No soft delete — hard deleting guests breaks booking FK and audit trails
- Consent captured once and never versioned — policy updates require re-consent
- No data portability endpoint — GDPR Article 20 requires this
- Marketing emails to users who didn't opt in — GDPR violation

## Success Criteria
- [ ] All personal data fields identified and classified
- [ ] Sensitive fields (national ID, passport) encrypted at rest
- [ ] Right-to-erasure endpoint implemented and tested
- [ ] Data portability export endpoint available
- [ ] Consent captured with version, timestamp, IP, locale
- [ ] Retention policies defined and automated cleanup scheduled
- [ ] Audit log for all GDPR-relevant operations