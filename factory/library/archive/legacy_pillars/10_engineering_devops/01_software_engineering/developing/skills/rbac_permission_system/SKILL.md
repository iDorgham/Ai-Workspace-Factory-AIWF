---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# RBAC Permission System

## Purpose
Define granular roles and permissions for Hurghada hospitality businesses. A receptionist has different access than a manager who has different access than the venue owner. Multi-venue staff need cross-venue coordination without cross-venue data access.

## Role Hierarchy

```
superadmin          → Platform operator (Sovereign team) — full access
    ↓
admin               → Tenant owner — all venues in their organization
    ↓
manager             → Single venue manager — full venue operations
    ↓
supervisor          → Shift supervisor — booking + staff management
    ↓
staff               → Front desk, waiter, instructor — operational tasks
    ↓
guest               → End user — own bookings only
```

## Permission Contract

```typescript
// packages/shared/src/contracts/auth.ts
export const RoleEnum = z.enum([
  'superadmin', 'admin', 'manager', 'supervisor', 'staff', 'guest'
])

export const PermissionEnum = z.enum([
  // Bookings
  'bookings:read',
  'bookings:create',
  'bookings:update',
  'bookings:cancel',
  'bookings:confirm',
  'bookings:export',

  // Members
  'members:read',
  'members:create',
  'members:update',
  'members:delete',

  // Venue
  'venue:read',
  'venue:update',
  'venue:manage-staff',
  'venue:manage-resources',

  // Financial
  'payments:read',
  'payments:process',
  'payments:refund',
  'reports:financial',

  // Admin
  'admin:manage-venues',
  'admin:manage-users',
  'admin:view-audit-logs',
  'admin:manage-tenants',  // superadmin only
])

export type Role       = z.infer<typeof RoleEnum>
export type Permission = z.infer<typeof PermissionEnum>

// Role → Permission mapping
export const ROLE_PERMISSIONS: Record<Role, Permission[]> = {
  superadmin: Object.values(PermissionEnum.enum) as Permission[],

  admin: [
    'bookings:read', 'bookings:create', 'bookings:update', 'bookings:cancel',
    'bookings:confirm', 'bookings:export',
    'members:read', 'members:create', 'members:update', 'members:delete',
    'venue:read', 'venue:update', 'venue:manage-staff', 'venue:manage-resources',
    'payments:read', 'payments:process', 'payments:refund', 'reports:financial',
    'admin:manage-venues', 'admin:manage-users', 'admin:view-audit-logs',
  ],

  manager: [
    'bookings:read', 'bookings:create', 'bookings:update', 'bookings:cancel',
    'bookings:confirm', 'bookings:export',
    'members:read', 'members:create', 'members:update',
    'venue:read', 'venue:manage-resources',
    'payments:read', 'payments:process', 'reports:financial',
  ],

  supervisor: [
    'bookings:read', 'bookings:create', 'bookings:update', 'bookings:confirm',
    'members:read', 'members:create',
    'venue:read',
    'payments:read', 'payments:process',
  ],

  staff: [
    'bookings:read', 'bookings:create', 'bookings:update',
    'members:read',
    'venue:read',
  ],

  guest: [
    'bookings:read', // own bookings only — enforced via resource check
    'bookings:create',
    'bookings:cancel', // own bookings only
  ],
}
```

## Permission Check Middleware

```typescript
// packages/auth/src/middleware.ts
export const requirePermission = (...permissions: Permission[]) =>
  createMiddleware(async (c, next) => {
    const user = c.get('user') as TokenPayload
    const userPermissions = ROLE_PERMISSIONS[user.role] ?? []

    const hasAll = permissions.every(p => userPermissions.includes(p))
    if (!hasAll) {
      return c.json({
        error: 'Forbidden',
        required: permissions,
        hint: 'Insufficient permissions for this operation',
      }, 403)
    }

    await next()
  })

// Usage
bookings.post('/', requireAuth, requirePermission('bookings:create'), handler)
bookings.delete('/:id', requireAuth, requirePermission('bookings:cancel'), handler)
reports.get('/financial', requireAuth, requirePermission('reports:financial'), handler)
```

## Resource-Level Authorization

```typescript
// Not all permission checks are role-based — some are resource-based
// Guests can only cancel their OWN bookings, not others'

export const requireBookingOwnership = createMiddleware(async (c, next) => {
  const user = c.get('user') as TokenPayload
  const { id } = c.req.param()

  // Managers and above can access any booking in their venue
  if (['superadmin', 'admin', 'manager', 'supervisor'].includes(user.role)) {
    await next()
    return
  }

  // Staff and guests can only access their own or their venue's bookings
  const booking = await prisma.booking.findUnique({ where: { id } })
  if (!booking) return c.json({ error: 'Not found' }, 404)

  const isOwner    = booking.guestId === user.sub
  const isVenueStaff = booking.venueId === user.venueId

  if (!isOwner && !isVenueStaff) {
    return c.json({ error: 'Forbidden' }, 403)
  }

  await next()
})
```

## Frontend Permission Guard

```tsx
// apps/web/src/components/PermissionGate.tsx
import { usePermissions } from '@/hooks/usePermissions'
import type { Permission } from '@workspace/shared/contracts/auth'

interface PermissionGateProps {
  requires: Permission | Permission[]
  fallback?: React.ReactNode
  children: React.ReactNode
}

export function PermissionGate({ requires, fallback = null, children }: PermissionGateProps) {
  const { hasPermission, hasAllPermissions } = usePermissions()
  const permissions = Array.isArray(requires) ? requires : [requires]

  if (!hasAllPermissions(permissions)) return <>{fallback}</>
  return <>{children}</>
}

// Usage
<PermissionGate requires="bookings:confirm">
  <ConfirmBookingButton bookingId={booking.id} />
</PermissionGate>

<PermissionGate requires={['reports:financial', 'bookings:export']} fallback={<AccessDenied />}>
  <FinancialReportPanel />
</PermissionGate>
```

## Audit Log for Permission-Sensitive Operations

```typescript
// All permission-sensitive operations must be audit-logged
export async function auditLog(event: {
  action:      string
  userId:      string
  userRole:    Role
  tenantId:    string
  resourceId?: string
  resourceType?: string
  metadata?:   Record<string, unknown>
}) {
  await prisma.auditLog.create({
    data: {
      ...event,
      ipAddress: getRequestIp(),
      timestamp: new Date(),
    }
  })
}

// Usage
await auditLog({
  action:       'booking.cancelled',
  userId:       user.sub,
  userRole:     user.role,
  tenantId:     user.tenantId,
  resourceId:   bookingId,
  resourceType: 'booking',
  metadata:     { reason: cancellationReason, amount: booking.totalAmount },
})
```

## Common Mistakes
- Checking only authentication (is the user logged in?) but not authorization (can they do this?)
- Role checks only at API level — frontend shows forbidden actions to users without permission
- `admin` role bypassing venue isolation — admin sees other tenants' data
- No audit log on financial operations — critical for hospitality compliance
- Permission list hardcoded in frontend — should come from JWT claims

## Success Criteria
- [ ] All roles defined with specific permission arrays
- [ ] `requirePermission` middleware on every non-public route
- [ ] Resource-level checks for ownership-sensitive operations
- [ ] `PermissionGate` component hides unauthorized UI
- [ ] Audit log captures all permission-sensitive operations
- [ ] `@Security` audit passes — zero routes missing permission checks