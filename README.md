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
