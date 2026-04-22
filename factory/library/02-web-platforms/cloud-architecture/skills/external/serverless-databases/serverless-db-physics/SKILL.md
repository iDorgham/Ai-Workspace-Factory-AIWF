# 💾 Serverless Database Physics (Neon/Convex)

## Purpose
Enforce standards for managing serverless, horizontally-scalable databases. This skill focuses on the logic of "Compute-Storage Separation" (Neon) and "Realtime Reactivity" (Convex) to ensure database performance matches the scaling patterns of serverless applications.

---

## Technique 1 — Branching Workflows (Neon Data Physics)
- **Rule**: Use database branching for every development feature; never run migrations directly on the "main" branch without prior isolated testing.
- **Protocol**: 
    1. Create a data branch from production for the feature.
    2. Run Prisma/Drizzle migrations on the branch.
    3. Verify data integrity in the preview environment.
    4. Merge schemas into the master branch once the feature PR is approved.

---

## Technique 2 — Re-active Data Orchestration (Convex)
- **Rule**: Prioritize "Realtime Subscriptions" over REST polling for interactive applications.
- **Protocol**: 
    1. Define `query` and `mutation` functions in the `convex` folder.
    2. Use the `useQuery` hook in the React frontend to establish a live subscription.
    3. Leverage Convex's "Internal Functions" for background scheduling and third-party API sync.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Connection Exhaustion** | 500 "Too many connections" | Use a "Connection Pooler" (e.g., Neon's pooled URL) for serverless environments where functions scale rapidly. |
| **Massive Scanning Queries** | High latency / Cost spikes | Ensure every query uses a defined Index; avoid `SELECT *` without filters on large datasets. |
| **Complex Logic in Realtime** | Sub-optimal UI lag | Offload heavy computation to asynchronous workers; keep the critical path for Realtime updates minimal. |

---

## Success Criteria (Serverless DB QA)
- [ ] 0 Migrations failed on production due to lack of branching tests.
- [ ] Realtime UI updates are reflected in < 100ms globally.
- [ ] 100% of sensitive storage is encrypted at rest.
- [ ] Backup schedules (PITR) are verified and active.