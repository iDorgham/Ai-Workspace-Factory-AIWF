# Task 5.2: Gemini Adapter Implementation Specification

**Day:** 5  
**Task:** 5.2  
**Duration:** 4 hours  
**Status:** READY TO IMPLEMENT

---

## Overview

Implement a production-ready Gemini tool adapter with multimodal support (text + vision) for image processing. This adapter integrates with Google's Generative AI API and inherits from the `ToolAdapter` base class.

---

## Key Differences from Claude Adapter

| Aspect | Claude | Gemini |
|--------|--------|--------|
| **API** | Anthropic SDK | Google Generative AI SDK |
| **Models** | claude-opus-4-6 | gemini-pro, gemini-pro-vision |
| **Multimodal** | Text only | Text + Vision (images) |
| **Pricing** | $0.003 / $0.009 | $0.0005 / $0.0015 |
| **Strength** | Long context | Vision tasks |
| **Latency** | ~2.1s avg | ~0.85s avg |

---

## Implementation Details

### File Location
```
.ai/scripts/adapters/[tool]-adapter.py
```

### Dependencies
```bash
pip install google-generativeai --break-system-packages
```

### Environment Variables
```bash
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-pro (default)
GEMINI_VISION_MODEL=gemini-pro-vision (for images)
```

### Class Structure

```python
class GeminiAdapter(ToolAdapter):
    """Gemini tool adapter for Google Generative AI integration"""
    
    # Pricing (April 2026)
    INPUT_PRICE_PER_1K = 0.0005      # $0.0005 per 1K input tokens
    OUTPUT_PRICE_PER_1K = 0.0015     # $0.0015 per 1K output tokens
    
    def __init__(self, api_key: str, config: Dict = None):
        """Initialize Gemini adapter with multimodal support"""
        # Same initialization pattern as Claude
        # But with Gemini-specific configuration
    
    def execute(self, command: str, images: List[str] = None) -> Dict:
        """
        Execute command via Gemini API with optional image support
        
        Args:
            command (str): Text prompt
            images (List[str]): List of image paths (optional)
            
        Returns:
            Dict with execution result (same format as Claude)
        """
        # Implementation for multimodal support
        # Detect if images provided
        # Use gemini-pro for text, gemini-pro-vision for images
    
    def process_images(self, image_paths: List[str]) -> List:
        """Process and prepare images for API"""
        # Convert images to proper format
        # Validate image types and sizes
        # Return prepared image objects
    
    def count_tokens(self, text: str, images: List = None) -> int:
        """Count tokens including image tokens"""
        # Text tokens + image tokens
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost with Gemini pricing"""
        # Much cheaper than Claude (0.0005 vs 0.003)
    
    def handle_error(self, error: Exception) -> Dict:
        """Handle Gemini-specific errors"""
        # Similar error handling as Claude
        # But with Gemini-specific error types
```

### Multimodal Capabilities

```python
# Text-only request
response = adapter.execute("Describe this image")

# With image
response = adapter.execute(
    "What objects are in this image?",
    images=["/path/to/image.jpg"]
)

# Multiple images
response = adapter.execute(
    "Compare these two images",
    images=["/path/to/image1.jpg", "/path/to/image2.jpg"]
)
```

### Key Features

1. **Vision Support:** Process images with gemini-pro-vision
2. **Cost Efficiency:** 5-10x cheaper than Claude
3. **Fast Latency:** ~0.85s average
4. **Multimodal:** Mix text and images in single request
5. **Error Recovery:** Handle API-specific errors gracefully

---

## Testing Strategy

**Test Cases (5 total):**

1. **Text-Only Execution** - Standard text prompt
2. **Image Analysis** - Single image processing  
3. **Multimodal** - Text + image combined
4. **Cost Calculation** - Verify cheaper pricing
5. **Performance** - Measure latency (should be fastest)

---

## Pricing Model

```
Input:  $0.0005 per 1K tokens  (10x cheaper than Claude)
Output: $0.0015 per 1K tokens  (6x cheaper than Claude)

Example for 1000 input + 500 output tokens:
├─ Input: 1000 / 1000 × $0.0005 = $0.0005
├─ Output: 500 / 1000 × $0.0015 = $0.00075
└─ Total: $0.00125 (vs Claude's $0.0345)
```

---

## File Structure

```
.ai/scripts/adapters/[tool]-adapter.py (250 lines)
├─ GeminiAdapter class
├─ Multimodal support methods
├─ Image processing
└─ Error handling
```

---

**Status:** READY FOR IMPLEMENTATION
