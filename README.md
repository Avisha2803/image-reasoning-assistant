🛍️ Image Reasoning Assistant for E-Commerce
A multimodal AI system that analyzes images for e-commerce suitability using computer vision, OCR, and LLM reasoning with hybrid validation.

https://img.shields.io/badge/python-3.9+-blue.svg
https://img.shields.io/badge/license-MIT-green.svg
https://img.shields.io/badge/LLM-OpenAI%252FGemini-purple.svg

📋 Table of Contents
Overview

✨ Features

🚀 Quick Start

🏗️ System Architecture

📁 Project Structure

🔧 Installation

⚙️ Configuration

📊 Usage

📈 Output Format

🛠️ Technical Details

🤝 Contributing

📄 License

Overview
The Image Reasoning Assistant is an intelligent system that evaluates product images for e-commerce platforms. It combines computer vision (object detection, OCR, quality analysis) with large language model reasoning to provide comprehensive assessments of image suitability.

Perfect for e-commerce platforms, marketplaces, or anyone needing automated image quality control and content analysis.

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

Basic Installation
bash
# 1. Clone the repository
git clone https://github.com/yourusername/image_reasoning_assistant.git
cd image_reasoning_assistant

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Tesseract OCR
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
# Default path: C:\Program Files\Tesseract-OCR\tesseract.exe

# Linux (Ubuntu/Debian):
sudo apt-get install tesseract-ocr

# macOS:
brew install tesseract
Configuration
Copy the environment template:

bash
cp .env.example .env
Edit .env with your API keys:

env
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here
# Optional: Configure paths and thresholds
Generate Test Images
bash
python create_test_images.py
# Creates 3 sample images in 'samples/' folder
Run Analysis
bash
# Analyze single image
python main.py samples/professional_product.jpg

# Run batch tests
python test_multiple_images.py
🏗️ System Architecture












Detailed Pipeline
Feature Extraction Layer (Pre-LLM Intelligence)

Object Detection: YOLO11n with 80+ classes and confidence thresholds

Text Extraction: Tesseract OCR with text cleanup and filtering

Quality Analysis: Laplacian variance for blur detection and sharpness assessment

Hybrid Reasoning Layer

LLM-Based Analysis: Structured prompts with features JSON and e-commerce criteria

Rule-Based Validation:

Score calculation (Sharpness: 30%, Object Focus: 40%, Background: 20%, Professionalism: 10%)

Issue detection (personal items, clutter, text appropriateness)

Intelligent Blending: LLM result validation with weighted confidence blending

Structured Output Layer

Comprehensive JSON with scores, issues, detected objects, and final verdict

Confidence levels and processing metadata

📁 Project Structure
text
image_reasoning_assistant/
├── README.md                    # This documentation
├── requirements.txt             # Python dependencies
├── config.py                    # Configuration settings
├── feature_extractor.py         # Pre-LLM feature extraction
├── llm_reasoner.py             # LLM + rule-based reasoning
├── main.py                      # Main pipeline orchestrator
├── create_test_images.py        # Generate test images
├── test_multiple_images.py      # Batch testing script
├── .env.example                 # Environment template
├── samples/                     # Test images directory
│   ├── professional_product.jpg # Clean product image
│   ├── sample1.jpg              # Casual photo (person + bed)
│   └── blurry_test.jpg          # Blurry test image
└── analysis_output_*.json       # Generated analysis files
🔧 Installation
Detailed Installation Steps
Python Environment Setup

bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
Tesseract OCR Installation

Windows:

Download installer from UB-Mannheim Tesseract

Install to C:\Program Files\Tesseract-OCR

Add to PATH or configure in .env

Linux:

bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install tesseract-ocr

# Install additional language packs if needed
sudo apt-get install tesseract-ocr-eng tesseract-ocr-chi-sim
macOS:

bash
brew install tesseract
brew install tesseract-lang  # For additional languages
YOLO Model Setup

bash
# The system automatically downloads YOLO11n model on first run
# Model will be saved to ~/.ultralytics/ for caching
⚙️ Configuration
Environment Variables
Create a .env file with the following variables:

env
# Required API Keys
OPENAI_API_KEY=sk-your-openai-key-here
GEMINI_API_KEY=your-gemini-api-key-here

# Optional Configuration
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe  # Windows
# TESSERACT_PATH=/usr/bin/tesseract  # Linux/Mac

# Analysis Parameters
OBJECT_CONFIDENCE_THRESHOLD=0.5
BLUR_THRESHOLD=100
MAX_OBJECTS_TO_DISPLAY=5

# LLM Settings
PRIMARY_LLM_PROVIDER=gemini  # gemini or openai
FALLBACK_ENABLED=true
LOCAL_LLM_ENABLED=false
Configuration File (config.py)
Key settings you can customize:

python
# Analysis weights (sum to 1.0)
SCORE_WEIGHTS = {
    'sharpness': 0.3,
    'object_focus': 0.4,
    'background': 0.2,
    'professionalism': 0.1
}

# Object detection settings
YOLO_MODEL = 'yolo11n.pt'
OBJECT_CONFIDENCE_THRESHOLD = 0.5

# Text processing
MIN_TEXT_CONFIDENCE = 0.6
FILTER_COMMON_WORDS = True

# LLM prompts
PROMPT_TEMPLATES = {
    'analysis': """Analyze this e-commerce image..."""
}
📊 Usage
Single Image Analysis
bash
# Basic usage
python main.py path/to/your/image.jpg

# Specify output directory
python main.py input.jpg --output ./results/

# Use specific LLM provider
python main.py input.jpg --llm openai

# Enable verbose logging
python main.py input.jpg --verbose
Batch Processing
bash
# Process all images in a directory
python test_multiple_images.py --input_dir ./my_images/ --output_dir ./results/

# Process specific file patterns
python test_multiple_images.py --pattern "*.jpg" --recursive

# Generate summary report
python test_multiple_images.py --summary report.json
Programmatic Usage
python
from multimodal_analyzer import MultimodalAnalyzer

# Initialize analyzer
analyzer = MultimodalAnalyzer()

# Analyze single image
result = analyzer.analyze_image("product_photo.jpg")
print(f"Quality Score: {result['image_quality_score']}")
print(f"Verdict: {result['final_verdict']}")

# Analyze multiple images
results = analyzer.analyze_batch(["img1.jpg", "img2.jpg", "img3.jpg"])
for img_path, analysis in results.items():
    print(f"{img_path}: {analysis['final_verdict']}")
📈 Output Format
JSON Output Example
json
{
  "image_quality_score": 0.78,
  "issues_detected": [
    "low lighting",
    "background clutter",
    "personal items visible"
  ],
  "detected_objects": [
    {"object": "shoe", "confidence": 0.92},
    {"object": "hand", "confidence": 0.87},
    {"object": "bed", "confidence": 0.76}
  ],
  "text_detected": ["Nike Air Max", "Limited Edition"],
  "llm_reasoning_summary": "The image shows a shoe product but includes personal elements...",
  "final_verdict": "Not suitable for professional e-commerce use",
  "confidence": 0.82,
  "processing_time": 1.95,
  "analysis_method": "hybrid",
  "improvement_suggestions": [
    "Use plain background",
    "Improve lighting",
    "Remove personal items from frame",
    "Use higher resolution camera"
  ],
  "metadata": {
    "image_dimensions": "1920x1080",
    "file_size_kb": 245,
    "format": "JPEG"
  }
}
Score Interpretation
0.9-1.0: Excellent - Ready for professional e-commerce

0.7-0.89: Good - Minor improvements needed

0.5-0.69: Fair - Significant improvements recommended

0.0-0.49: Poor - Not suitable without major changes

🛠️ Technical Details
Feature Extraction
YOLO11n: Lightweight but accurate object detection (80+ classes)

Tesseract OCR: Open-source OCR with preprocessing (grayscale, thresholding)

Laplacian Variance: Mathematical blur detection algorithm

Multi-threading: Parallel processing for faster analysis

LLM Integration
Structured Prompts: Carefully designed prompts for consistent outputs

Fallback System: Automatic switching between providers

Output Validation: Ensures LLM responses follow expected schema

Caching: Optional response caching for cost reduction

Performance Optimization
Model Caching: YOLO model cached locally after first download

Async Processing: Optional async/await for batch processing

Memory Management: Automatic cleanup of large tensors and images

Progress Tracking: Real-time progress for batch operations

🤝 Contributing
We welcome contributions! Here's how you can help:

Fork the repository

Create a feature branch

bash
git checkout -b feature/amazing-feature
Commit your changes

bash
git commit -m 'Add some amazing feature'
Push to the branch

bash
git push origin feature/amazing-feature
Open a Pull Request

Development Setup
bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Check code style
flake8 .

# Type checking
mypy .
Roadmap
Support for additional image formats (WebP, HEIC)

Video analysis capabilities

Custom object detection training

Cloud deployment (Docker, AWS Lambda)

Web interface with Streamlit/FastAPI

Additional LLM providers (Claude, Llama)

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
Ultralytics YOLO for object detection

Google Tesseract OCR

OpenAI and Google Gemini for LLM APIs

All contributors and users of this project
