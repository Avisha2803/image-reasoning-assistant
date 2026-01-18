# Image-Aware Reasoning Assistant

A mini multimodal system that analyzes an image for e-commerce suitability using object detection, OCR, and LLM reasoning.

## Project Structure

image_reasoning_assistant/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── config.py                           # Configuration settings
├── feature_extractor.py                # Pre-LLM feature extraction
├── llm_reasoner.py                     # LLM + rule-based reasoning
├── main.py                             # Main pipeline orchestrator
├── create_test_images.py               # Generate test images
├── test_multiple_images.py             # Batch testing script
├── .env.example                        # Environment template
├── samples/                            # Test images directory
│   ├── professional_product.jpg       # Clean product image
│   ├── sample1.jpg                    # Casual photo (person + bed)
│   └── blurry_test.jpg                # Blurry test image
└── analysis_output_*.json             # Generated analysis files

## 🚀 Quick Start

# 1. Installation

# Clone repository
git clone <your-repo-url>
cd image_reasoning_assistant

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR (Windows)
Download from: https://github.com/UB-Mannheim/tesseract/wiki
Default path: C:\Program Files\Tesseract-OCR\tesseract.exe

# 2. Configuration
# Edit .env with your API keys
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here

# 3. Generate Test Images
python create_test_images.py
# Creates 3 sample images in 'samples/' folder

# 4. Run Analysis
# Analyze single image
python main.py samples/professional_product.jpg

# Run batch tests
python test_multiple_images.py

## 🔧 System Architecture
Image Input
    ↓
[1] Feature Extraction (Pre-LLM Intelligence)
    ├── Object Detection (YOLO11n)
    ├── Text Extraction (Tesseract OCR)
    └── Blur Analysis (Laplacian Variance)
    ↓
[2] Hybrid Reasoning Layer
    ├── LLM Analysis (Gemini/OpenAI)
    ├── Rule-Based Validation
    └── Intelligent Result Blending
    ↓
[3] Structured Output (JSON) 

# Key Components
FeatureExtractor - Extracts 3+ visual features before LLM

LLMReasoner - Hybrid analysis with fallback mechanisms

MultimodalAnalyzer - Orchestrates the complete pipeline

## 🎯 Core Features
# ✅ Pre-LLM Feature Extraction
Object Detection: YOLO11n detects 80+ object classes

Text Extraction: Tesseract OCR with preprocessing

Quality Assessment: Blur detection via Laplacian variance

# ✅ Intelligent Reasoning
LLM Integration: Gemini/OpenAI with structured prompting

Rule-Based Fallback: Comprehensive scoring system

Validation Logic: Cross-checks LLM outputs

# ✅ Structured Output
{
  "image_quality_score": 0.85,
  "issues_detected": ["background clutter", "poor lighting"],
  "detected_objects": ["shoe", "hand"],
  "text_detected": [],
  "llm_reasoning_summary": "The image shows...",
  "final_verdict": "Suitable for professional e-commerce use",
  "confidence": 0.82
}

