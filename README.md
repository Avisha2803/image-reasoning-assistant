# 🛍️ Image Reasoning Assistant  
*A Mini Multimodal System for E-commerce Image Suitability Analysis*

This project is a **hybrid multimodal AI system** that analyzes product images for **professional e-commerce suitability** using:

- 🔍 Object detection using YOLO (80+ classes)
- 🔤 Text extraction using OCR
- 📏 Image quality assessment (blur / sharpness)
- 🤖 LLM-based semantic reasoning (Gemini / OpenAI)
- ⚖️ Rule-based validation & score blending
- 📊 Structured, explainable JSON outputs
  
The system combines **pre-LLM visual intelligence** with **LLM reasoning and validation** to produce reliable, structured decisions suitable for real-world production pipelines.

---

## 📁 Project Structure
```text
image_reasoning_assistant/
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
├── config.py                  # Configuration settings
├── feature_extractor.py       # Pre-LLM feature extraction
├── llm_reasoner.py             # LLM + rule-based reasoning
├── main.py                    # Main pipeline orchestrator
├── create_test_images.py      # Generate test images
├── test_multiple_images.py    # Batch testing script
├── .env.example               # Environment variable template
├── samples/                   # Test images directory
│   ├── professional_product.jpg
│   ├── sample1.jpg
│   └── blurry_test.jpg
└── analysis_output_*.json     # Generated analysis outputs
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Clone the repository
```sh
git clone https://github.com/yourusername/image_reasoning_assistant.git
```

2. Install Python dependencies
```sh
pip install -r requirements.txt
 ```

3. Install Tesseract OCR
Windows: Download from:
👉 https://github.com/UB-Mannheim/tesseract/wiki


5. 🔑 Configuration
```js 
GEMINI_API_KEY=your_gemini_key_here
  ```

7. Generate Test Images
```sh
python create_test_images.py
 ```
6. Analyze a Single Image/Run Batch Analysis
```sh
python main.py samples/professional_product.jpg
python test_multiple_images.py
 ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## System Architecture
```text
IMAGE INPUT (JPEG / PNG)
        │
        ▼
[1] FEATURE EXTRACTION LAYER (Pre-LLM Intelligence)
------------------------------------------------
• Object Detection (YOLO11n – 80+ classes)
• Text Extraction (Tesseract OCR)
• Quality Assessment (Laplacian Variance)
        │
        ▼
Extracted Features JSON
------------------------------------------------
{
  "detected_objects": [{"object": "person", "confidence": 0.95}],
  "detected_text": "Product Name v2.0",
  "blur_score": 0.85,
  "object_count": 5,
  "top_objects": ["person", "bed", "phone"]
}
        │
        ▼
[2] HYBRID REASONING LAYER
------------------------------------------------
LLM-Based Analysis
• Structured prompt
• E-commerce criteria
• Schema-constrained output

Rule-Based Validation
• Sharpness (30%)
• Object Focus (40%)
• Background Cleanliness (20%)
• Professionalism (10%)

Result Blending
• Score validation
• Issue consistency
• Confidence estimation
        │
        ▼
[3] STRUCTURED OUTPUT
------------------------------------------------
{
  "image_quality_score": 0.78,
  "issues_detected": ["background clutter", "low lighting"],
  "detected_objects": ["shoe", "hand"],
  "text_detected": [],
  "llm_reasoning_summary": "The image appears informal...",
  "final_verdict": "Not suitable for professional use",
  "confidence": 0.82,
  "processing_time": 1.95,
  "analysis_method": "hybrid"
}
```

## Why This Approach?

Pre-LLM feature extraction ensures grounded reasoning
Hybrid logic reduces hallucinations
Rule-based fallback guarantees deterministic behavior
Structured outputs enable automation and auditing
This design mirrors real-world ML + LLM production systems.

## ⚠️ Limitations & Future Improvements

Current Limitations:
Object detection may miss fine-grained product attributes
OCR accuracy drops under severe blur or low lighting
LLM inference adds latency and API cost
Fixed rule weights may not generalize across all categories

## Future Improvements:
Fine-tune detection models on e-commerce datasets
Replace OCR with vision-language models
Learn scoring weights from labeled data
Add multi-image (gallery) analysis
Human-in-the-loop validation

## Production Deployment Strategy

To productionize this system:
Deploy as a FastAPI microservice
Use async processing (Celery / Kafka)
Cache features and LLM responses
Secure secrets via a secrets manager
Add monitoring for latency, confidence drift, and failures
Log all decisions for auditability

## Sample Outputs
# Example 1: Professional Product Image
Input: samples/professional_product.jpg
output:
{
  "image_quality_score": 0.91,
  "issues_detected": [],
  "detected_objects": ["shoe"],
  "final_verdict": "Suitable for professional e-commerce use",
  "confidence": 0.88
}
Explanation:
Single product, clean background, high sharpness.

# Example 2: Casual Indoor Image
Input: samples/sample1.jpg
output:
{
  "image_quality_score": 0.43,
  "issues_detected": ["background clutter", "personal items detected"],
  "detected_objects": ["person", "bed", "phone"],
  "final_verdict": "Not suitable for professional use",
  "confidence": 0.84
}
Explanation:
Presence of people and clutter violates listing standards.

# Example 3: Blurry Image
Input: samples/blurry_test.jpg
output:
{
  "image_quality_score": 0.29,
  "issues_detected": ["blur detected"],
  "detected_objects": ["bottle"],
  "final_verdict": "Not suitable for professional use",
  "confidence": 0.90
}
Explanation:
Blur significantly reduces visual clarity

