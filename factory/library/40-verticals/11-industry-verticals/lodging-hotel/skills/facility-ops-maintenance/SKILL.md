# 🧹 Facility Ops Maintenance
> **Skill Category:** Property Operations / Maintenance Physics
> **Domains:** Luxury Lodging, Housekeeping, HSE

## Purpose
Govern the physical operational health of the hospitality facility. This skill ensures that the luxury standard is maintained through sequenced housekeeping and continuous facility auditing.

---

## 🛠️ Operational Techniques

### 1. Housekeeping Sequencing Logic
- **Physics**: Automate the assignment of "Room-Status" nodes (Clean, Dirty, Inspected, Out-of-Order).
- **Trigger**: Automated alerts for rooms that transition to "Dirty" status based on guest check-out timestamps.
- **Verification**: Enforce the "Omega-White-Glove" inspection protocol for all luxury suites.

### 2. Facility Health & Safety (HSE) Compliance
- **Physics**: Periodically audit facility maintenance logs (AC, Plumbing, Fire Safety).
- **Compliance**: Generate automated alerts for upcoming preventative maintenance (PPM) cycles.
- **Workflow**: `/hotel FacilityAudit` generates a comprehensive property safety score.

---

## 🛡️ Governance & Anti-Patterns
- **Anti-Pattern**: Releasing rooms for check-in without an explicit "Inspected" tag.
- **Correction**: Use the "Double-Lock" verification—a room cannot be assigned to a new guest stub until both the Housekeeping and Supervisor stubs are validated.

## Success Criteria
- [ ] 100% of rooms assigned have a valid "Inspected" verification hash.
- [ ] Overdue maintenance cycles reduced to zero via automated PPM alerts.
