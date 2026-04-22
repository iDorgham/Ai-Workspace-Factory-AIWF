# ♻️ React Incremental Static Regeneration (ISR)

## Purpose
Enforce standards for refreshing static content without a full rebuild. This skill focuses on the ISR model, where static pages are updated in the background after they have been deployed, enabling high-performance sites with massive amounts of dynamic content.

---

## Technique 1 — Time-Based Revalidation
- **Rule**: Set a revalidation interval (`revalidate`) based on the data's volatility.
- **Protocol**: 
    1. Deliver the stale cached version of the page immediately.
    2. Trigger a background re-generation of the page if the revalidate interval has passed.
    3. Swap the old cache with the new HTML for subsequent requests once ready.

---

## Technique 2 — On-Demand Revalidation (Tag/Path)
- **On-Demand**: Use Webhooks or API calls (e.g., `revalidatePath` or `revalidateTag`) to manually purge the cache when a CMS update occurs. This ensures "Static" content stays fresh within seconds of an update.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)
| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Too frequent time-reval** | Cache trashing / DB load | Balance the interval; use On-Demand revalidation for data that changes infrequently but needs instant updates. |
| **Missing Fallback States** | 404 for new paths | Use `fallback: 'blocking'` to generate new routes on-the-fly when they are first visited. |
| **Prop-Drilling Large Objects** | Response bloat | Ensure only the necessary data for the page is passed to the component props; use data-selection at the fetch level. |

---

## Success Criteria (ISR QA)
- [ ] Pages update automatically without a full GitHub Actions / CI build.
- [ ] User receives a fast "Edge" response every time.
- [ ] Background re-generation does not block current user requests.
- [ ] Stale data duration is within acceptable business limits (defined by the revalidate interval).