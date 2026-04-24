# Firebase Integration

## What Firebase Provides in Sovereign

| Service | Sovereign Usage |
|---------|-----------|
| Authentication | Social login (Google, Apple, GitHub) + email/password + phone |
| Firestore | NoSQL document database with real-time subscriptions |
| Realtime Database | Low-latency JSON sync (simpler than Firestore, for presence/chat) |
| Storage | File uploads (images, docs) — GCS-backed |
| Cloud Functions | Serverless backend triggers (Firestore triggers, HTTP, scheduled) |
| FCM | Push notifications (web, iOS, Android) |
| App Check | Attestation — prevents abuse from non-app clients |
| Remote Config | Feature flags + A/B testing without redeploy |

**When to choose Firebase over Supabase:** Mobile-first apps, push notifications required, Google social login is primary, need offline-first Firestore sync.

---

## Setup in Sovereign Monorepo

### pnpm Catalog Entries
```yaml
# pnpm-workspace.yaml → catalog section
catalog:
  "firebase": "^11.5.0"                  # Client SDK (web)
  "firebase-admin": "^13.2.0"            # Server SDK (Cloud Functions / API)
  "firebase-functions": "^6.3.2"         # Cloud Functions SDK
  "firebase-tools": "^13.30.0"           # CLI (devDependencies)
```

### Environment Variables
```bash
# .env.example
NEXT_PUBLIC_FIREBASE_API_KEY=AIzaSy...
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=[project].firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=[project-id]
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=[project].appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=...
NEXT_PUBLIC_FIREBASE_APP_ID=1:...:web:...

# Server-side only (Cloud Functions / Admin SDK)
FIREBASE_SERVICE_ACCOUNT_KEY={"type":"service_account",...}   # JSON string, use Secret Manager
```

---

## Client SDK Setup

```typescript
// packages/shared/src/lib/firebase/client.ts
import { initializeApp, getApps, getApp } from 'firebase/app'

const firebaseConfig = {
  apiKey:            process.env.NEXT_PUBLIC_FIREBASE_API_KEY!,
  authDomain:        process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN!,
  projectId:         process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID!,
  storageBucket:     process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET!,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID!,
  appId:             process.env.NEXT_PUBLIC_FIREBASE_APP_ID!,
}

// Singleton — prevents duplicate initialization during Next.js hot reload
export const firebaseApp = getApps().length ? getApp() : initializeApp(firebaseConfig)
```

```typescript
// packages/shared/src/lib/firebase/admin.ts — Server-only
import { initializeApp, getApps, cert } from 'firebase-admin/app'
import { getAuth } from 'firebase-admin/auth'
import { getFirestore } from 'firebase-admin/firestore'

const adminApp = getApps().find(a => a.name === 'admin')
  ?? initializeApp({
       credential: cert(JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT_KEY!)),
     }, 'admin')

export const adminAuth = getAuth(adminApp)
export const adminDb   = getFirestore(adminApp)
```

---

## Authentication

### Client-Side Auth
```typescript
// packages/shared/src/lib/firebase/auth.ts
import { getAuth, signInWithPopup, GoogleAuthProvider, signOut } from 'firebase/auth'
import { firebaseApp } from './client'

export const auth = getAuth(firebaseApp)

export async function signInWithGoogle() {
  const provider = new GoogleAuthProvider()
  provider.addScope('profile')
  provider.addScope('email')
  const result = await signInWithPopup(auth, provider)
  return result.user
}

export async function signOutUser() {
  await signOut(auth)
}
```

### Auth in Next.js App Router (Server Components)
```typescript
// apps/web/src/lib/firebase-session.ts
// Firebase Auth is client-side — verify on server via ID token
import { adminAuth } from '@workspace/shared/lib/firebase/admin'
import { cookies } from 'next/headers'

export async function getServerUser() {
  const sessionCookie = cookies().get('firebase-session')?.value
  if (!sessionCookie) return null

  try {
    const decoded = await adminAuth.verifySessionCookie(sessionCookie, true)
    return decoded
  } catch {
    return null
  }
}

// In middleware or API route — exchange ID token for session cookie
export async function createSession(idToken: string) {
  const expiresIn = 60 * 60 * 24 * 5 * 1000  // 5 days
  return adminAuth.createSessionCookie(idToken, { expiresIn })
}
```

### Auth State in Client Components
```typescript
// hooks/useUser.ts ('use client')
import { useEffect, useState } from 'react'
import { onAuthStateChanged, type User } from 'firebase/auth'
import { auth } from '@workspace/shared/lib/firebase/auth'

export function useUser() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (u) => {
      setUser(u)
      setLoading(false)
    })
    return unsubscribe   // cleanup — always unsubscribe
  }, [])

  return { user, loading }
}
```

---

## Firestore — Document Database

### Type-Safe Collection Helpers
```typescript
// packages/shared/src/lib/firebase/firestore.ts
import { getFirestore, collection, CollectionReference } from 'firebase/firestore'
import { firebaseApp } from './client'
import type { Booking, UserProfile } from '@workspace/shared/contracts'

export const db = getFirestore(firebaseApp)

// Typed collection references
export const bookingsCollection = collection(db, 'bookings') as CollectionReference<Booking>
export const usersCollection    = collection(db, 'users')    as CollectionReference<UserProfile>
```

### CRUD Operations
```typescript
import { doc, getDoc, setDoc, updateDoc, deleteDoc, serverTimestamp } from 'firebase/firestore'
import { bookingsCollection } from './firestore'

// Create (merge-safe upsert)
await setDoc(doc(bookingsCollection, bookingId), {
  ...bookingData,
  createdAt: serverTimestamp(),
  updatedAt: serverTimestamp(),
})

// Read
const snap = await getDoc(doc(bookingsCollection, bookingId))
if (!snap.exists()) throw new Error('Booking not found')
const booking = snap.data()   // fully typed via CollectionReference<Booking>

// Update (partial)
await updateDoc(doc(bookingsCollection, bookingId), {
  status: 'confirmed',
  updatedAt: serverTimestamp(),
})

// Soft delete (preferred over deleteDoc)
await updateDoc(doc(bookingsCollection, bookingId), {
  deletedAt: serverTimestamp(),
})
```

### Pagination Query
```typescript
import { query, orderBy, limit, startAfter, where, getDocs } from 'firebase/firestore'

async function getBookingPage(lastDoc?: DocumentSnapshot, pageSize = 20) {
  const q = query(
    bookingsCollection,
    where('deletedAt', '==', null),       // soft delete filter
    orderBy('createdAt', 'desc'),
    ...(lastDoc ? [startAfter(lastDoc)] : []),
    limit(pageSize),
  )
  const snap = await getDocs(q)
  return { docs: snap.docs.map(d => d.data()), lastDoc: snap.docs.at(-1) }
}
```

### Real-Time Subscription
```typescript
// 'use client' component
import { onSnapshot, query, where, orderBy, limit } from 'firebase/firestore'

useEffect(() => {
  const q = query(bookingsCollection, where('userId', '==', userId), limit(20))
  const unsubscribe = onSnapshot(q, (snap) => {
    setBookings(snap.docs.map(d => d.data()))
  })
  return unsubscribe   // cleanup on unmount
}, [userId])
```

---

## Storage — File Uploads

```typescript
import { getStorage, ref, uploadBytesResumable, getDownloadURL } from 'firebase/storage'
import { firebaseApp } from './client'

const storage = getStorage(firebaseApp)

export async function uploadFile(path: string, file: File, onProgress?: (pct: number) => void) {
  const storageRef = ref(storage, path)
  const task = uploadBytesResumable(storageRef, file)

  return new Promise<string>((resolve, reject) => {
    task.on(
      'state_changed',
      (snap) => onProgress?.(Math.round(snap.bytesTransferred / snap.totalBytes * 100)),
      reject,
      async () => resolve(await getDownloadURL(task.snapshot.ref))
    )
  })
}
```

---

## Cloud Functions (Gen 2)

```typescript
// functions/src/bookings.ts
import { onDocumentCreated } from 'firebase-functions/v2/firestore'
import { onCall, HttpsError } from 'firebase-functions/v2/https'
import { onSchedule } from 'firebase-functions/v2/scheduler'

// Trigger on new booking document
export const onBookingCreated = onDocumentCreated('bookings/{bookingId}', async (event) => {
  const booking = event.data?.data()
  if (!booking) return

  // Send confirmation email, create audit log, etc.
  await sendConfirmationEmail(booking)
})

// Callable function (from client SDK)
export const confirmBooking = onCall({ region: 'us-central1' }, async (request) => {
  if (!request.auth) throw new HttpsError('unauthenticated', 'Must be logged in')
  const { bookingId } = request.data

  // ... business logic
  return { success: true }
})

// Scheduled function
export const dailyCleanup = onSchedule('0 2 * * *', async () => {
  // cleanup expired sessions, etc.
})
```

---

## Security Rules (Firestore)

```javascript
// firestore.rules
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Bookings — users can read/write own, staff can read all
    match /bookings/{bookingId} {
      allow read:   if request.auth != null &&
                       (resource.data.userId == request.auth.uid ||
                        request.auth.token.role == 'staff')
      allow create: if request.auth != null &&
                       request.resource.data.userId == request.auth.uid
      allow update: if request.auth != null &&
                       (resource.data.userId == request.auth.uid ||
                        request.auth.token.role == 'staff')
      allow delete: if false   // always soft delete
    }

    // User profiles — own profile only
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId
    }
  }
}
```

---

## Push Notifications (FCM)

```typescript
// Client — request permission and get token
import { getMessaging, getToken, onMessage } from 'firebase/messaging'

export async function initFCM(): Promise<string | null> {
  try {
    const messaging = getMessaging(firebaseApp)
    const token = await getToken(messaging, {
      vapidKey: process.env.NEXT_PUBLIC_FIREBASE_VAPID_KEY,
    })
    return token
  } catch {
    return null  // user denied notifications
  }
}

// Server — send notification via Admin SDK
import { getMessaging } from 'firebase-admin/messaging'

await getMessaging(adminApp).send({
  token: userFCMToken,
  notification: { title: 'Booking Confirmed', body: 'Your booking #123 is confirmed.' },
  data: { bookingId: booking.id },
})
```

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Common Mistakes

- **[FB-001]** Initializing Firebase SDK multiple times — use `getApps().length` singleton check
- **[FB-002]** Storing service account key in environment as a file path — store as JSON string in Secret Manager
- **[FB-003]** Using `onAuthStateChanged` without cleanup — always return the unsubscribe function
- **[FB-004]** Firestore `.collection().get()` without `limit()` — unbounded query, same as AP-020
- **[FB-005]** Not setting Firestore security rules — all data is public by default in test mode
- **[FB-006]** Using Realtime Database for complex queries — use Firestore; Realtime DB has no filtering
- **[FB-007]** Cloud Functions Gen 1 — use Gen 2 (onDocumentCreated vs onWrite, better cold start)
- **[FB-008]** Not verifying ID tokens on server — client-side auth can be spoofed; always use Admin SDK verify

## Success Criteria
- [ ] Firebase app initialized once (singleton pattern with `getApps()` guard)
- [ ] Service account key stored in Secret Manager (not in repo or plain env)
- [ ] All Firestore queries include `limit()` (AP-020 equivalent)
- [ ] Firestore security rules deployed and tested
- [ ] `onAuthStateChanged` / `onSnapshot` subscriptions cleaned up on unmount
- [ ] Server-side auth uses `verifySessionCookie` or `verifyIdToken` via Admin SDK
- [ ] Cloud Functions Gen 2 used (not Gen 1)
- [ ] FCM tokens stored per user, refreshed on each session