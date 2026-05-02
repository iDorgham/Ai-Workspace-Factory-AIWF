---
name: azure-ai
description: "Use for Azure AI: Search, Speech, OpenAI, Document Intelligence. Helps with search, vector/hybrid search, speech-to-text, text-to-speech, transcription, OCR. WHEN: AI Search, query search, vector search, hybrid search, semantic search, speech-to-text, text-to-speech, transcribe, OCR, convert text to speech."
license: MIT
metadata:
  author: Microsoft
  version: "1.0.1"
---

# Azure AI Services

## Services

| Service | Use When | MCP Tools | CLI |
|---------|----------|-----------|-----|
| AI Search | Full-text, vector, hybrid search | `azure__search` | `az search` |
| Speech | Speech-to-text, text-to-speech | `azure__speech` | - |
| OpenAI | GPT models, embeddings, DALL-E | - | `az cognitiveservices` |
| Document Intelligence | Form extraction, OCR | - | - |

## MCP Server (Preferred)

When Azure MCP is enabled:

### AI Search
- `azure__search` with command `search_index_list` - List search indexes
- `azure__search` with command `search_index_get` - Get index details
- `azure__search` with command `search_query` - Query search index

### Speech
- `azure__speech` with command `speech_transcribe` - Speech to text
- `azure__speech` with command `speech_synthesize` - Text to speech

**If Azure MCP is not enabled:** Run `/azure:setup` or enable via `/mcp`.

## AI Search Capabilities

| Feature | Description |
|---------|-------------|
| Full-text search | Linguistic analysis, stemming |
| Vector search | Semantic similarity with embeddings |
| Hybrid search | Combined keyword + vector |
| AI enrichment | Entity extraction, OCR, sentiment |

## Speech Capabilities

| Feature | Description |
|---------|-------------|
| Speech-to-text | Real-time and batch transcription |
| Text-to-speech | Neural voices, SSML support |
| Speaker diarization | Identify who spoke when |
| Custom models | Domain-specific vocabulary |

## SDK Quick References

For programmatic access to these services, see the condensed SDK guides:

- **AI Search**: Python (`references/sdk/azure_search_documents_py.md`) | TypeScript (`references/sdk/azure_search_documents_ts.md`) | .NET (`references/sdk/azure_search_documents_dotnet.md`)
- **OpenAI**: .NET (`references/sdk/azure_ai_openai_dotnet.md`)
- **Vision**: Python (`references/sdk/azure_ai_vision_imageanalysis_py.md`) | Java (`references/sdk/azure_ai_vision_imageanalysis_java.md`)
- **Transcription**: Python (`references/sdk/azure_ai_transcription_py.md`)
- **Translation**: Python (`references/sdk/azure_ai_translation_text_py.md`) | TypeScript (`references/sdk/azure_ai_translation_ts.md`)
- **Document Intelligence**: .NET (`references/sdk/azure_ai_document_intelligence_dotnet.md`) | TypeScript (`references/sdk/azure_ai_document_intelligence_ts.md`)
- **Content Safety**: Python (`references/sdk/azure_ai_contentsafety_py.md`) | TypeScript (`references/sdk/azure_ai_contentsafety_ts.md`) | Java (`references/sdk/azure_ai_contentsafety_java.md`)

## Service Details

For deep documentation on specific services:

- AI Search indexing and queries -> [Azure AI Search documentation](https://learn.microsoft.com/azure/search/search-what-is-azure-search)
- Speech transcription patterns -> [Azure AI Speech documentation](https://learn.microsoft.com/azure/ai-services/speech-service/overview)
