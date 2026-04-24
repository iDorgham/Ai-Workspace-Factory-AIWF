---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🎧 DJ Mixing & Performance (Omega-tier)

## Purpose
Enforce professional standards for DJing and digital music library management. This skill covers **Beat-Matching**, **Harmonic Mixing**, **Track Analysis**, and **Metadata Tagging** to ensure seamless performances and efficient track discovery.

---

## Technique 1 — Track Analysis & Grid Prep

### The "Pulse" Protocol
- **Rule**: Every track must be analyzed for BPM and Key (Camelot Scale preferred).
- **Protocol**: Verify the **Beatgrid** align exactly with the first downbeat. Use "Cue Points" to mark critical structural changes (Intro, Breakdown, Drop, Outro).

---

## Technique 2 — Harmonic & Rhythmic Mixing

### Harmonic Mixing (Camelot Wheel)
- **Protocol**: Mix between keys that are adjacent on the wheel (e.g., 8A to 7A or 9A) to ensure melodic compatibility.
- **Rhythmic Beat-Matching**: Use manual pitch adjustment (nudging) to align transients when "Sync" is unavailable or unstable. Always listen for "Flamming" (double kick sounds) which indicates poor alignment.

---

## Technique 3 — Library Metadata & Tagging

### "Omega" Tagging Standard
- **File Format**: Prefer **WAV/AIFF** for club performance; **MP3 (320kbps)** for general listening.
- **ID3 Tags**:
    - **Genre**: Specific (Melodic Techno, Indie Dance).
    - **Energy**: Scale of 1-5 in the "Comment" field.
    - **Keys**: 1A-12B format.
- **Organization**: Use a "Year/Month" or "Genre/Energy" folder structure for rapid access during a live set.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Mixing in "Red"** | Digital Distortion | Keep your channel trims and master output below clipping; allow the club's limiter to handle final volume. |
| **Clashing Vocals** | Sonic Mess | Never mix two vocal-heavy sections simultaneously; use EQ or Filter to carve space. |
| **Ignoring Phase** | Low-end loss | If the bass disappears during a mix, one track's phase may be inverted; swap tracks or adjust EQ quickly. |

---

## Success Criteria (DJ QA)
- [ ] Track Grid is perfectly aligned.
- [ ] Harmonic transitions are melodically pleasing.
- [ ] Metadata tags are complete (BPM, Key, Genre).
- [ ] Transitions between 120BPM and 126BPM are smooth (Transition tracks or slow pitch shift).