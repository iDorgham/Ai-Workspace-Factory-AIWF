---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 📐 Vector Database Architecture (Omega-tier)


## Purpose
Enforce professional standards for the design and deployment of Vector Databases (Pinecone, Milvus, Weaviate, PGVector). This skill provides the "Memory Layer" for RAG (Retrieval-Augmented Generation) systems, ensuring sub-second semantic retrieval across multi-million vector sets.

---

## Technique 1 — High-Performance Indexing

### HNSW vs. IVF-Flat
- **HNSW (Hierarchical Navigable Small World)**: Use for low-latency, high-accuracy queries. Ideal for production and real-time bots.
- **IVF-Flat**: Use for high-recall scenarios with restricted memory budgets.

### Index Compression
- **Scalar Quantization / Product Quantization (PQ)**: Use to reduce the memory footprint of vectors by up to 90% without significant loss in recall accuracy.

---

## Technique 2 — RAG Optimization (Hybrid Search)

### The "Obsidian" Retrieval Loop
- **Step 1: Semantic Search**: Retrieve top-k results using Vector Embeddings.
- **Step 2: BM25 / Keyword Search**: Retrieve matches using traditional token-matching (essential for technical terms/names).
- **Step 3: Reciprocal Rank Fusion (RRF)**: Re-rank the combined results to provide the most semantically and contextually relevant data to the LLM.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Missing Chunk Overlap** | Logic cut-off at boundaries | Ensure 10-20% sentence-level overlap between vector chunks. |
| **Embedding Drift** | Recall degradation | Ensure the `Embedding Model` used for ingestion matches the query model exactly. |
| **Ignoring Meta-Filters** | Irrelevant results | Use "Metadata Filtering" (e.g., `Category: Finance`) to narrow the search space before vector math. |

---

## Success Criteria (Vector QA)
- [ ] Query latency < 300ms for 1M+ vectors.
- [ ] Recall accuracy verified against "Ground Truth" question sets.
- [ ] Hybrid search active (Vector + Technical Keyword).
- [ ] Namespaces used to isolate distinct datasets (e.g., separating "Public Docs" from "Private Contracts").
