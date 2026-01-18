# config.py
import os
import sys
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LLM Configuration
    LLM_PROVIDER = "gemini"  # Options: "openai", "gemini", "fallback"
    
    # OpenAI API
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-4o"
    
    # Google Gemini API - CORRECTED MODEL NAME
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = "gemini-2.0-flash-latest"  # Try this
    
    # Feature Extraction Models
    YOLO_MODEL_PATH = "yolo11n.pt"
    
    # OCR Configuration
    TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    
    # Analysis Parameters
    OBJECT_CONFIDENCE_THRESHOLD = 0.25