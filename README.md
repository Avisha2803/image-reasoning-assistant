# Image-Aware Reasoning Assistant

A mini multimodal system that analyzes an image for e-commerce suitability using object detection, OCR, and LLM reasoning.

## Key Design Choices & Trade-offs

| Component | Choice | Rationale & Trade-off |
|-----------|--------|-----------------------|
| **Object Detection** | YOLO11n (Ultralytics) | **Speed vs. Accuracy:** The nano model offers fast inference with reasonable accuracy for this demo. For production, consider YOLO11s/m for higher precision[reference:7]. |
| **OCR** | Tesseract (pytesseract) | **Cost vs. Capability:** Free and open-source. Trade-off is lower accuracy on complex fonts/layouts vs. cloud APIs (Google Vision, AWS Textract). |
| **LLM** | GPT-4o (OpenAI API) | **Reasoning vs. Cost:** GPT-4o provides excellent reasoning and native JSON output. Trade-off is API cost vs. using a smaller local model (e.g., Llama 3.1) which would require more plumbing for structured output[reference:8]. |
| **Pipeline** | Sequential feature extraction → LLM call | **Simplicity vs. Parallelism:** Easy to debug and explain. For production, parallelize feature extractors and implement caching. |

## Running the System

1. Install dependencies: `pip install -r requirements.txt`
2. Set your OpenAI API key in a `.env` file: `OPENAI_API_KEY=sk-...`
3. Run analysis: `python main.py samples/your_image.jpg`

## Sample Output
```json
{
  "image_quality_score": 0.78,
  "issues_detected": ["low lighting", "background clutter"],
  "detected_objects": ["shoe", "hand"],
  "text_detected": [],
  "llm_reasoning_summary": "The image appears informal and lacks a clean background...",
  "final_verdict": "Not suitable for professional e-commerce use",
  "confidence": 0.82
}