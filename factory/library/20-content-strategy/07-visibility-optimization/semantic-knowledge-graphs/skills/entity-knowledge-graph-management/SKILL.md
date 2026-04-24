---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🕸️ Entity & Knowledge Graph Management

## Purpose
Enforce professional standards for mapping and governing the brand's "Semantic Identity." This skill ensures that your brand, products, and experts are recognized as **Entities** (not just strings) within the Global Knowledge Graphs (Google, Bing, Wikidata).

---

## Technique 1 — The "Sentinel" Schema Archetype

### Advanced Schema.org Implementation
- **Rule**: Use "Nested Entities" rather than flat properties.
- **Protocol**: 
    1. **Organization**: Define the `Organization` entity with `sameAs` links to social profiles and wikidata.
    2. **People**: Link authors/experts to the organization using `worksFor` and `knowsAbout` (expertise markers).
    3. **Product**: Define the `Product` entity with `brand` (pointing to the Organization node) and `isRelatedTo` links.

---

## Technique 2 — Knowledge Graph Seeding (The Entity Loop)

- **Wikidata & Wikipedia Synchronization**: Ensure "Entity Nodes" exist in open-data repositories. This is the primary signal for Google's Knowledge Panel.
- **SameAs Citation**: Use the `sameAs` property to "Cluster" all fragmented digital identities (LinkedIn, Crunchbase, GitHub) into one single Entity Node.

---

## Technique 3 — Entity Internal Linking (Topic Clusters)

- **Semantic Slinks**: Every internal link must have a `rel="entity"` or equivalent semantic marker to help the crawler understand the relationship between the two pages (e.g., "This page *describes* Entity X").
- **Knowledge Silos**: Organize content into silos that reflect the hierarchy of the company's "Intelligence Domains."

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Conflicting Schema** | Identity fragmentation | Maintain a "Single Source of Truth" JSON-LD template. |
| **Broken sameAs Links** | Trust signal loss | Periodically audit `sameAs` targets for 404s or hijacking. |
| **Ignoring Local Entities** | Poor regional visibility | Map the organization to physical `LocalBusiness` nodes for MENA/regional search. |

---

## Success Criteria (Entity QA)
- [ ] Brand appears as a "Knowledge Panel" for relevant queries.
- [ ] Schema Markup passes validation with 0 errors/warnings.
- [ ] LLMs (Claude/GPT) recognize the entity as a distinct node with specific attributes.
- [ ] Internal linking follows the "Entity Silo" standard.