---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Booking & Scheduling Domain Patterns

## Purpose
Reusable patterns for booking flows across all Hurghada business types: restaurants (table booking), dive schools (activity scheduling), health clubs (class booking), hotels (room reservations), and VIP clubs (event + table reservations).

## Universal Booking Contract

```typescript
// packages/shared/src/contracts/booking.ts
// Designed to cover: table, room, activity, class, equipment
import { z } from 'zod'

export const BookingTypeEnum = z.enum([
  'table',      // Restaurant, beach club
  'room',       // Hotel, villa
  'activity',   // Diving, desert tour, water sport
  'class',      // Fitness, yoga, diving lesson
  'equipment',  // Dive gear, sports equipment
  'event',      // VIP event, private party
  'slot',       // Generic time slot
])

export const BookingSchema = z.object({
  id:             z.string().uuid(),
  tenantId:       z.string().uuid(),
  venueId:        z.string().uuid(),
  resourceId:     z.string().uuid().optional(), // table, room, lane, equipment ID
  guestId:        z.string().uuid(),
  type:           BookingTypeEnum,
  startsAt:       z.string().datetime(),
  endsAt:         z.string().datetime(),
  partySize:      z.number().int().min(1).max(500),
  status:         z.enum(['pending', 'confirmed', 'checked-in', 'completed', 'cancelled', 'no-show']),
  source:         z.enum(['walk-in', 'online', 'phone', 'agent', 'concierge']),
  totalAmount:    z.number().nonnegative(),
  depositAmount:  z.number().nonnegative().default(0),
  currency:       z.enum(['EGP', 'USD', 'EUR', 'SAR']),
  specialRequests: z.string().max(500).optional(),
  internalNotes:   z.string().max(1000).optional(),
  metadata:        z.record(z.unknown()).optional(), // type-specific extras
  createdBy:       z.string().uuid(),
  confirmedBy:     z.string().uuid().optional(),
  cancelledBy:     z.string().uuid().optional(),
  cancellationReason: z.string().optional(),
  createdAt:       z.string().datetime(),
  updatedAt:       z.string().datetime(),
}).refine(
  data => new Date(data.endsAt) > new Date(data.startsAt),
  { message: 'End time must be after start time', path: ['endsAt'] }
)
```

## Availability Check Pattern

```typescript
// packages/shared/src/utils/availability.ts
// Core business logic — shared between web, mobile, and API

export interface AvailabilityQuery {
  venueId:    string
  resourceId?: string  // specific table/room/lane
  type:       BookingTypeEnum
  startsAt:   Date
  endsAt:     Date
  partySize:  number
}

export interface AvailableSlot {
  startsAt:  Date
  endsAt:    Date
  capacity:  number
  remaining: number
  resources: { id: string; name: string }[]
}

// apps/api/src/services/availability.service.ts
export async function checkAvailability(query: AvailabilityQuery): Promise<AvailableSlot[]> {
  // Get all resources of the requested type for this venue
  const resources = await prisma.resource.findMany({
    where: {
      venueId:   query.venueId,
      type:      query.type,
      isActive:  true,
      capacity:  { gte: query.partySize },
    }
  })

  // Get conflicting bookings in the time window
  const conflicting = await prisma.booking.findMany({
    where: {
      venueId:   query.venueId,
      type:      query.type,
      status:    { in: ['pending', 'confirmed', 'checked-in'] },
      OR: [
        { startsAt: { gte: query.startsAt, lt: query.endsAt } },
        { endsAt:   { gt: query.startsAt, lte: query.endsAt } },
        { startsAt: { lte: query.startsAt }, endsAt: { gte: query.endsAt } },
      ]
    }
  })

  // Compute available resources
  const bookedResourceIds = new Set(conflicting.map(b => b.resourceId).filter(Boolean))
  const available = resources.filter(r => !bookedResourceIds.has(r.id))

  if (available.length === 0) return []

  return [{
    startsAt:  query.startsAt,
    endsAt:    query.endsAt,
    capacity:  resources.reduce((sum, r) => sum + r.capacity, 0),
    remaining: available.reduce((sum, r) => sum + r.capacity, 0),
    resources: available.map(r => ({ id: r.id, name: r.name })),
  }]
}
```

## Booking State Machine

```typescript
// Valid state transitions
const BOOKING_TRANSITIONS: Record<BookingStatus, BookingStatus[]> = {
  'pending':    ['confirmed', 'cancelled'],
  'confirmed':  ['checked-in', 'cancelled', 'no-show'],
  'checked-in': ['completed'],
  'completed':  [], // terminal state
  'cancelled':  [], // terminal state
  'no-show':    [], // terminal state
}

export function canTransition(from: BookingStatus, to: BookingStatus): boolean {
  return BOOKING_TRANSITIONS[from].includes(to)
}

export async function transitionBooking(
  bookingId: string,
  newStatus: BookingStatus,
  userId: string,
  reason?: string
) {
  const booking = await prisma.booking.findUniqueOrThrow({ where: { id: bookingId } })

  if (!canTransition(booking.status, newStatus)) {
    throw new Error(`Cannot transition from ${booking.status} to ${newStatus}`)
  }

  return prisma.booking.update({
    where: { id: bookingId },
    data: {
      status: newStatus,
      ...(newStatus === 'confirmed' && { confirmedBy: userId }),
      ...(newStatus === 'cancelled' && { cancelledBy: userId, cancellationReason: reason }),
      updatedAt: new Date(),
    }
  })
}
```

## Venue-Type Specific Patterns

### Restaurant (Table Booking)
```typescript
// metadata for table booking
const RestaurantBookingMetadata = z.object({
  tablePreference: z.enum(['indoor', 'outdoor', 'terrace', 'vip']).optional(),
  occasion:        z.enum(['birthday', 'anniversary', 'business', 'regular']).optional(),
  dietaryRequirements: z.array(z.string()).optional(),
  seatingTime:     z.number().min(60).max(240).default(120), // expected duration in minutes
})
```

### Dive School (Activity Booking)
```typescript
const DiveActivityMetadata = z.object({
  diveType:       z.enum(['fun-dive', 'discover-scuba', 'night-dive', 'wreck', 'course']),
  certLevel:      z.enum(['none', 'open-water', 'advanced', 'divemaster']).optional(),
  equipmentRental: z.boolean().default(true),
  buddyBookingId: z.string().uuid().optional(), // linked booking for buddy pairs
  depth:          z.number().min(0).max(40).optional(),
  siteId:         z.string().uuid().optional(), // dive site reference
})
```

### VIP Club (Event + Table)
```typescript
const VIPBookingMetadata = z.object({
  packageType:     z.enum(['table-only', 'bottle-service', 'vip-package', 'exclusive-buyout']),
  bottleCount:     z.number().int().min(0).optional(),
  guestListNames:  z.array(z.string()).max(20).optional(),
  dresscode:       z.string().optional(),
  entertainerRequest: z.string().optional(),
})
```

## Notification Events

```typescript
// packages/shared/src/events/booking.events.ts
export const BookingEvents = {
  CREATED:    'booking.created',
  CONFIRMED:  'booking.confirmed',
  CANCELLED:  'booking.cancelled',
  REMINDER:   'booking.reminder',    // 24h + 2h before
  CHECKED_IN: 'booking.checked_in',
  NO_SHOW:    'booking.no_show',
} as const

// Notification content (bilingual)
export const getNotificationContent = (
  event: keyof typeof BookingEvents,
  booking: BookingType,
  locale: 'en' | 'ar'
) => {
  const messages = {
    'booking.confirmed': {
      en: `Your booking at ${booking.venueName} is confirmed for ${formatDate(booking.startsAt, 'en')}`,
      ar: `تم تأكيد حجزك في ${booking.venueName} بتاريخ ${formatDate(booking.startsAt, 'ar')}`,
    },
    // ... other events
  }
  return messages[BookingEvents[event]][locale]
}
```

## Common Mistakes
- No conflict detection — double bookings happen silently
- Hardcoded business types — use the `type` enum + metadata pattern for extensibility
- Not using state machine — invalid transitions (pending → completed) allowed
- Missing `tenantId` in booking — critical for multi-tenant isolation
- No `source` field — can't analyze booking channel performance
- Timezone not stored — dates are ambiguous without timezone (Hurghada = Africa/Cairo)

## Success Criteria
- [ ] Booking contract locked before any implementation
- [ ] Availability check prevents double-booking
- [ ] State machine enforces valid transitions only
- [ ] Metadata schema extends base booking for each venue type
- [ ] Notification events emit on key status changes
- [ ] All booking times stored in UTC, displayed in Africa/Cairo timezone