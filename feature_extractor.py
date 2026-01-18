from ultralytics import YOLO
import pytesseract
from PIL import Image
import cv2
import numpy as np
from config import Config

class FeatureExtractor:
    def __init__(self):
        # Load YOLO model once at initialization
        print("Loading YOLO model for object detection...")
        self.object_detector = YOLO(Config.YOLO_MODEL_PATH)
        
        # Set Tesseract path explicitly
        pytesseract.pytesseract.tesseract_cmd = Config.TESSERACT_PATH
        print(f"✓ Tesseract configured at: {Config.TESSERACT_PATH}")
        
        # Verify Tesseract works
        try:
            version = pytesseract.get_tesseract_version()
            print(f"✓ Tesseract version: {version}")
            self.tesseract_available = True
        except:
            print("✗ Tesseract verification failed")
            self.tesseract_available = False
    
    def extract_objects(self, image_path):
        """Run object detection and return list of detected objects with confidences."""
        try:
            print(f"  Running object detection on {image_path}...")
            results = self.object_detector(image_path)[0]
            detections = []
            if results.boxes is not None:
                for box, cls in zip(results.boxes, results.boxes.cls):
                    conf = float(box.conf[0])
                    if conf >= Config.OBJECT_CONFIDENCE_THRESHOLD:
                        class_name = results.names[int(cls)]
                        detections.append({
                            "object": class_name,
                            "confidence": round(conf, 3)
                        })
            print(f"  Found {len(detections)} objects")
            return detections
        except Exception as e:
            print(f"⚠  Object detection failed: {e}")
            return []
    
    def extract_text(self, image_path):
        """Extract text from image using Tesseract OCR."""
        if not self.tesseract_available:
            return ""
        
        try:
            image = Image.open(image_path)
            
            # Preprocess for better OCR
            # Convert to grayscale
            gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
            
            # Apply thresholding for better text recognition
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
            
            # Use Tesseract with optimized settings for product images
            custom_config = r'--oem 3 --psm 6'  # OEM 3 = default, PSM 6 = assume uniform block of text
            text = pytesseract.image_to_string(thresh, config=custom_config)
            
            cleaned_text = text.strip()
            # Filter out meaningless single characters/punctuation
            meaningful_chars = sum(1 for c in cleaned_text if c.isalnum())
            if meaningful_chars < 2:  # Less than 2 alphanumeric characters
                print("  Text filtered out (not meaningful)")
                return ""
        
            print(f"  Text found: '{cleaned_text[:50]}'" + ("..." if len(cleaned_text) > 50 else ""))
                
            return cleaned_text
        except Exception as e:
            print(f"⚠  OCR extraction failed: {e}")
            return ""
    
    def extract_blur_score(self, image_path):
        """Calculate image blur score using Laplacian variance."""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return 0.0
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Calculate Laplacian variance
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Normalize to 0-1 scale
            # Typical values: >100 = sharp, <50 = blurry
            blur_score = max(0, min(1, laplacian_var / 200))
            
            assessment = "sharp" if blur_score > 0.5 else "slightly blurry" if blur_score > 0.25 else "blurry"
            print(f"  Image sharpness: {assessment} ({blur_score:.3f})")
            
            return round(blur_score, 3)
        except Exception as e:
            print(f"⚠  Blur detection failed: {e}")
            return 0.0
    
    def run_all(self, image_path):
        """Run all available feature extractors and return consolidated results."""
        print("\n=== FEATURE EXTRACTION ===")
        
        # Run extractors
        objects = self.extract_objects(image_path)
        text = self.extract_text(image_path)
        blur_score = self.extract_blur_score(image_path)
        
        # Get top objects by confidence
        sorted_objects = sorted(objects, key=lambda x: x["confidence"], reverse=True)
        top_objects = [obj["object"] for obj in sorted_objects[:5]]  # Top 5 objects
        
        # Prepare results
        result = {
            "detected_objects": objects,
            "detected_text": text,
            "object_count": len(objects),
            "has_text": bool(text),
            "blur_score": blur_score,
            "blur_assessment": "sharp" if blur_score > 0.5 else "slightly blurry" if blur_score > 0.25 else "blurry",
            "top_objects": top_objects,
            "object_summary": f"{len(objects)} objects: {', '.join(top_objects[:3])}" + ("..." if len(top_objects) > 3 else "")
        }
        
        print(f"\n=== EXTRACTION SUMMARY ===")
        print(f"Total objects detected: {len(objects)}")
        print(f"Text detected: {'Yes' if text else 'No'}")
        print(f"Image sharpness: {result['blur_assessment']} ({blur_score:.2f}/1.0)")
        print("=" * 30)
        
        return result