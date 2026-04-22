

---
# command-routing definition
# Version-Pin: 20260422-0230
```json
{
  "version": "2.0",
  "updated": "2026-04-13",
  "defaults": {
    "ranking": ["copilot", "codex", "gemini", "qwen"],
    "fallback_policy": "quality_first",
    "confidence_threshold": 0.75
  },
  "commands": [
    {
      "id": "research_competitors",
      "patterns": [
        "^/research competitors?$"
      ],
      "ranking": ["gemini", "copilot", "codex", "qwen"],
      "fallback_policy": "context_heavy",
      "confidence_threshold": 0.8,
      "quality_gates": {
        "min_confidence": 0.8,
        "require_citations": true
      }
    },
    {
      "id": "scrape_all_blog",
      "patterns": [
        "^/scrape all competitors? blog$"
      ],
      "ranking": ["qwen", "codex", "copilot", "gemini"],
      "fallback_policy": "speed_cost",
      "confidence_threshold": 0.82,
      "quality_gates": {
        "min_confidence": 0.82,
        "allow_partial_results": true
      }
    },
    {
      "id": "scrape_all_projects",
      "patterns": [
        "^/scrape all competitors? projects?$"
      ],
      "ranking": ["qwen", "codex", "copilot", "gemini"],
      "fallback_policy": "speed_cost",
      "confidence_threshold": 0.82,
      "quality_gates": {
        "min_confidence": 0.82,
        "allow_partial_results": true
      }
    },
    {
      "id": "scrape_all_website",
      "patterns": [
        "^/scrape all competitors? all website$"
      ],
      "ranking": ["qwen", "codex", "copilot", "gemini"],
      "fallback_policy": "speed_cost",
      "confidence_threshold": 0.84,
      "quality_gates": {
        "min_confidence": 0.84,
        "allow_partial_results": true
      }
    },
    {
      "id": "scrape_single_website",
      "patterns": [
        "^/scrape (.+?) website$"
      ],
      "ranking": ["qwen", "codex", "copilot", "gemini"],
      "fallback_policy": "speed_cost",
      "confidence_threshold": 0.83,
      "quality_gates": {
        "min_confidence": 0.83,
        "allow_partial_results": true
      }
    },
    {
      "id": "scrape_single_all_website",
      "patterns": [
        "^/scrape (.+?) all website$"
      ],
      "ranking": ["qwen", "codex", "copilot", "gemini"],
      "fallback_policy": "speed_cost",
      "confidence_threshold": 0.84,
      "quality_gates": {
        "min_confidence": 0.84,
        "allow_partial_results": true
      }
    },
    {
      "id": "sync",
      "patterns": [
        "^/sync$"
      ],
      "ranking": ["qwen", "codex", "copilot", "gemini"],
      "fallback_policy": "speed_cost",
      "confidence_threshold": 0.8,
      "quality_gates": {
        "min_confidence": 0.8
      }
    },
    {
      "id": "create_blog_posts",
      "patterns": [
        "^/create blog-posts$",
        "^/create blog posts? about (.+)$"
      ],
      "ranking": ["copilot", "codex", "gemini", "qwen"],
      "fallback_policy": "quality_first",
      "confidence_threshold": 0.75
    },
    {
      "id": "optimize_images",
      "patterns": [
        "^/optimize images(?: in content/)?$"
      ],
      "ranking": ["gemini", "codex", "copilot", "qwen"],
      "fallback_policy": "multimodal",
      "confidence_threshold": 0.78
    },
    {
      "id": "export",
      "patterns": [
        "^/export$"
      ],
      "ranking": ["qwen", "codex", "copilot", "gemini"],
      "fallback_policy": "speed_cost",
      "confidence_threshold": 0.75
    },
    {
      "id": "brand",
      "patterns": [
        "^/brand$",
        "^/brand workshop$"
      ],
      "ranking": ["gemini", "copilot"],
      "fallback_policy": "quality_first",
      "confidence_threshold": 0.8
    },
    {
      "id": "extract_brand_voice",
      "patterns": [
        "^/extract brand voice from (.+)$"
      ],
      "ranking": ["gemini", "qwen"],
      "fallback_policy": "context_heavy",
      "confidence_threshold": 0.8
    },
    {
      "id": "refine_brand_voice",
      "patterns": [
        "^/refine brand voice$"
      ],
      "ranking": ["gemini", "qwen"],
      "fallback_policy": "quality_first",
      "confidence_threshold": 0.8
    },
    {
      "id": "create_website_pages",
      "patterns": [
        "^/create website pages$"
      ],
      "ranking": ["copilot", "gemini"],
      "fallback_policy": "quality_first",
      "confidence_threshold": 0.75
    },
    {
      "id": "create_project_pages",
      "patterns": [
        "^/create project pages$"
      ],
      "ranking": ["copilot", "gemini"],
      "fallback_policy": "quality_first",
      "confidence_threshold": 0.75
    },
    {
      "id": "create_landing_pages",
      "patterns": [
        "^/create landing pages for (.+)$"
      ],
      "ranking": ["copilot", "gemini"],
      "fallback_policy": "quality_first",
      "confidence_threshold": 0.75
    },
    {
      "id": "compare",
      "patterns": [
        "^/compare sovereign vs competitor (.+)$"
      ],
      "ranking": ["gemini", "qwen"],
      "fallback_policy": "context_heavy",
      "confidence_threshold": 0.8
    },
    {
      "id": "intel_competitor",
      "patterns": [
        "^/intel competitor (.+)$"
      ],
      "ranking": ["gemini", "qwen"],
      "fallback_policy": "context_heavy",
      "confidence_threshold": 0.8
    },
    {
      "id": "intel_market_snapshot",
      "patterns": [
        "^/intel market snapshot$"
      ],
      "ranking": ["gemini", "qwen"],
      "fallback_policy": "context_heavy",
      "confidence_threshold": 0.8
    },
    {
      "id": "intel_opportunities",
      "patterns": [
        "^/intel opportunities$"
      ],
      "ranking": ["gemini", "qwen"],
      "fallback_policy": "context_heavy",
      "confidence_threshold": 0.8
    },
    {
      "id": "polish_content",
      "patterns": [
        "^/polish content in content/$"
      ],
      "ranking": ["gemini", "qwen"],
      "fallback_policy": "quality_first",
      "confidence_threshold": 0.8
    },
    {
      "id": "review",
      "patterns": [
        "^/review$"
      ],
      "ranking": ["gemini", "qwen"],
      "fallback_policy": "quality_first",
      "confidence_threshold": 0.8
    },
    {
      "id": "approve",
      "patterns": [
        "^/approve$"
      ],
      "ranking": ["gemini", "qwen"],
      "fallback_policy": "quality_first",
      "confidence_threshold": 0.8
    },
    {
      "id": "revise",
      "patterns": [
        "^/revise (.+)$"
      ],
      "ranking": ["copilot", "gemini"],
      "fallback_policy": "quality_first",
      "confidence_threshold": 0.75
    },
    {
      "id": "archive",
      "patterns": [
        "^/archive old content$"
      ],
      "ranking": ["qwen", "codex"],
      "fallback_policy": "speed_cost",
      "confidence_threshold": 0.75
    },
    {
      "id": "memory_save",
      "patterns": [
        "^/memory save$"
      ],
      "ranking": ["qwen", "codex"],
      "fallback_policy": "speed_cost",
      "confidence_threshold": 0.75
    },
    {
      "id": "memory_load",
      "patterns": [
        "^/memory load$"
      ],
      "ranking": ["qwen", "codex"],
      "fallback_policy": "speed_cost",
      "confidence_threshold": 0.75
    },
    {
      "id": "memory_clear",
      "patterns": [
        "^/memory clear$"
      ],
      "ranking": ["qwen", "codex"],
      "fallback_policy": "speed_cost",
      "confidence_threshold": 0.75
    },
    {
      "id": "budget_check",
      "patterns": [
        "^/budget check$"
      ],
      "ranking": ["gemini", "qwen"],
      "fallback_policy": "speed_cost",
      "confidence_threshold": 0.75
    },
    {
      "id": "antigravity",
      "patterns": [
        "^/antigravity (status|sync|learn)$"
      ],
      "ranking": ["gemini", "qwen"],
      "fallback_policy": "quality_first",
      "confidence_threshold": 0.8
    }
  ]
}

```
