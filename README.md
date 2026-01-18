# 🛍️ Image Reasoning Assistant  
*A Mini Multimodal System for E-commerce Image Suitability Analysis*

This project is a **hybrid multimodal AI system** that analyzes product images for **professional e-commerce suitability** using:

- 🧠 **Object Detection**
- 🔤 **OCR (Text Extraction)**
- 🤖 **LLM-based Reasoning**
- 📏 **Rule-based Quality Scoring**

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

✨ Features
✅ Pre-LLM Feature Extraction
Object Detection: YOLO11n detects 80+ object classes with confidence scores

Text Extraction: Tesseract OCR with preprocessing and filtering

Quality Assessment: Blur detection via Laplacian variance algorithm

Multi-feature Analysis: Combines visual, textual, and quality metrics

🧠 Intelligent Reasoning Layer
LLM Integration: Gemini (primary) and OpenAI (fallback) with structured prompting

Rule-Based Validation: Comprehensive scoring system with configurable weights

Hybrid Analysis: Combines AI reasoning with deterministic rules

Fallback Mechanisms: Robust error handling and graceful degradation

📊 Structured Output
Comprehensive JSON: Detailed analysis with scores, issues, and recommendations

Confidence Scoring: Weighted confidence levels for all assessments

Actionable Insights: Clear verdicts with specific improvement suggestions

Performance Metrics: Processing time and analysis method tracking

🚀 Quick Start
Prerequisites
Python 3.9 or higher
Tesseract OCR installed
API keys for Gemini and/or OpenAI

1. Clone the repository
git clone https://github.com/yourusername/image_reasoning_assistant.git
cd image_reasoning_assistant

2. Install Python dependencies
pip install -r requirements.txt

3. Install Tesseract OCR
Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
Default path: C:\Program Files\Tesseract-OCR\tesseract.exe

GEMINI_API_KEY=your_gemini_key_here

python create_test_images.py
python main.py samples/professional_product.jpg
python test_multiple_images.py

🏗️ System Architecture

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




