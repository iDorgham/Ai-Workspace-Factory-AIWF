# 🔥 Firebase Platform Mastery

## Purpose
Enforce standards for the Google Firebase ecosystem. This skill focuses on Firestore data modeling, Security Rules, and Cloud Function optimization to ensure low-latency, secure serverless applications.

---

## Technique 1 — Firestore Security Rules (Production-Grade)
- **Rule**: Deny all by default; allow specific access based on `request.auth.uid`.
- **Protocol**: 
    1. Define granular rules for every collection.
    2. Use `get()` or `exists()` in Rules to verify relationships (e.g., "User is part of this project").
    3. Use the `firebaserules` emulator to unit-test all rule permutations before deployment.

---

## Technique 2 — Atomicity & Batched Writes
- **Rule**: Use `transactions` for any logic involving increments or multi-document updates.
- **Protocol**: 
    1. Orchestrate transactions for sensitive data (e.g., inventory, balance).
    2. Use `writeBatch` for bulk-uploading non-sensitive data to minimize network roundtrips.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Indexing everything** | High cost / Write delay | Only index fields that are actually used in complex queries. |
| **Logic in Firestore Rules** | Slow execution | Keep Rules simple; move complex business logic to Cloud Functions to keep reads fast. |
| **Client-Side Admin Access** | Full data breach | Never use the `admin` SDK in any client-side code; reserve it for Cloud Functions and secure backends. |

---

## Success Criteria (Firebase QA)
- [ ] 0 items with `allow read, write: if true` in Security Rules.
- [ ] Cloud Functions are optimized for cold-starts (< 1s).
- [ ] No "Race Conditions" detected in multi-user write scenarios.
- [ ] Analytics and Crashlytics are integrated into the deployment pipeline.