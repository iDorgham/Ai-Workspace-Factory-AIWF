## Learned User Preferences
- **Industrial Aesthetic**: Prefers dark mode, high-tech, and "premium" visual styling for all artifacts and UIs.
- **Library-First**: Prioritizes reuse and versioning of components from `factory/library/` over ad-hoc generation.
- **Traceability**: Requires ISO-8601 timestamps and Reasoning Hashes for all autonomous mutations.
- **MENA Focus**: High priority on regional adaptations (Arabic RTL, local payments, Law 151 compliance).

## Learned Workspace Facts
- **Project State**: AIWF v13.0.0 "Geospatial Sovereignty" achieved.
- **Compliance**: Law 151/2020 data residency enforced via `Regional-Controller`.
- **Core Architecture**:
  - `factory/core/regional_controller.py`: Geospatial boundary enforcement.
  - `factory/core/galaxy_sync.py`: P2P registry propagation.
  - `factory/core/cloud_gateway.py`: Residency-aware routing.
- **Sovereign Isolation**: Client work contained in `workspaces/<slug>/`.
- **Governance**: Changes require `Dorgham-Approval` via Omega Gate v2.
- **Deployment**: Vercel-only via `/deploy` command.
- **Library Health**: Current global average component score is 62.0/100 (per `DEEP_LIBRARY_DOC.md`).
