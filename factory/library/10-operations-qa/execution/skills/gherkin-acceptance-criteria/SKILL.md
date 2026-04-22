# Gherkin Acceptance Criteria

## Purpose
Express feature requirements as testable Given/When/Then scenarios. Makes acceptance criteria unambiguous, directly maps to test cases, and works for both Founder (business language) and Pro (technical) modes.

## When to Activate
- Every `/plan [feature]` command
- Every feature plan in `.ai/plans/active/features/`
- Sprint planning sessions
- Whenever a feature requirement is ambiguous

## Gherkin Format

```gherkin
Feature: [Feature name — matches contract domain]

  Background:
    Given [common setup for all scenarios]

  Scenario: [Happy path — primary success case]
    Given  [initial context / precondition]
    When   [user action or event]
    Then   [expected observable outcome]
    And    [additional outcome]

  Scenario: [Alternative path]
    Given  [different starting condition]
    When   [same or different action]
    Then   [different expected outcome]

  Scenario: [Error / edge case]
    Given  [condition that causes an error]
    When   [action attempted]
    Then   [appropriate error handling]

  @arabic
  Scenario: [Same flow in Arabic locale]
    Given  [locale is Arabic]
    When   [same action]
    Then   [outcome includes RTL layout and Arabic text]
```

## Real Example: Booking Feature

```gherkin
Feature: Table Booking — Red Sea Venue

  Background:
    Given the venue "Coral Terrace" is operational
    And the guest is authenticated as "Ahmed Hassan"
    And tables are available for the requested date

  Scenario: Guest successfully books a table
    Given the guest is on the bookings page
    And the date "2026-04-15" has available tables
    When the guest selects party size "4"
    And the guest selects time slot "19:00"
    And the guest taps "Confirm Booking"
    Then a booking is created with status "pending"
    And the guest receives a confirmation email
    And the booking appears in the guest's booking history

  Scenario: Manager confirms a pending booking
    Given a booking exists with status "pending"
    And the user is authenticated as a manager
    When the manager taps "Confirm" on the booking
    Then the booking status changes to "confirmed"
    And the guest receives a confirmation SMS

  Scenario: Guest cancels booking within policy window
    Given a confirmed booking exists for tomorrow
    And the cancellation policy allows free cancellation 24 hours before
    When the guest cancels the booking
    Then the booking status changes to "cancelled"
    And no cancellation fee is charged

  Scenario: Guest attempts to book a fully-booked slot
    Given all tables for "19:00 on 2026-04-15" are reserved
    When the guest attempts to book the "19:00" slot
    Then the booking form shows "No tables available for this time"
    And the system suggests the next available slot

  Scenario: Booking form validation — party size
    Given the guest is on the booking form
    When the guest enters party size "0"
    And taps "Confirm Booking"
    Then the form shows "Party size must be at least 1"
    And no booking is created

  Scenario: Booking flow in Arabic locale
    Given the page language is set to Arabic
    And the page direction is RTL
    When the guest completes the booking form in Arabic
    Then the booking is created successfully
    And the confirmation message appears in Arabic
    And all dates and numbers use Arabic-Indic format

  @admin
  Scenario: Admin exports booking report
    Given bookings exist for the date range "2026-04-01 to 2026-04-30"
    When the admin requests an export
    Then a CSV file is downloaded
    And the file contains all bookings within the range
    And amounts are formatted in EGP
```

## Feature Plan Template

```markdown
# Feature: [Name]
## Plan Reference
- Contract: packages/shared/src/contracts/[domain].ts
- Sprint: [N]
- Assigned: @Frontend, @Backend, @QA
- Plan Step: [X.Y]

## Acceptance Criteria (Gherkin)
[Gherkin scenarios here — minimum 3, maximum 7]

## Definition of Done
- [ ] Contracts locked
- [ ] All Gherkin scenarios have passing tests
- [ ] compliance passes
- [ ] @Reviewer approved
- [ ] @BrandGuardian approved (if UI changes)
- [ ] RTL scenario passing
- [ ] Deployed to staging
```

## Mapping Scenarios to Tests

```typescript
// Each Gherkin scenario maps to a test
// "Guest successfully books a table" → integration test
test('creates booking with valid data', async () => {
  // Given
  const venue = await createTestVenue()
  const guest = await createTestGuest()
  const token = await getTestToken('guest')

  // When
  const response = await app.request('/api/bookings', {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify({ venueId: venue.id, partySize: 4, startsAt: tomorrow19h }),
  })

  // Then
  expect(response.status).toBe(201)
  const booking = await response.json()
  expect(booking.status).toBe('pending')
  expect(booking.guestId).toBe(guest.id)
})
```

## Founder Mode Translation

Gherkin is shown to `@Founder` in plain language, not raw syntax:

```
✅ Founder mode output:
"When a guest books a table, they get a confirmation email 
and the booking shows as 'pending' until a manager confirms it."

✅ Pro mode output:
"POST /api/bookings → 201 { status: 'pending' }
 Email notification triggered via event queue."
```

## Common Mistakes
- Scenarios too implementation-specific ("When the user clicks button#submit") — use behavior
- Missing error scenarios — happy path alone is insufficient
- No Arabic/RTL scenario — bilingual parity must be tested
- More than 7 scenarios per feature — split into sub-features
- Scenarios that can't be automated — every Gherkin must map to a test

## Success Criteria
- [ ] Minimum 3 scenarios per feature plan
- [ ] Happy path, alternative path, and at least one error case covered
- [ ] Arabic locale scenario included for all UI features
- [ ] Every scenario maps to at least one automated test
- [ ] Scenarios written before `/build` starts