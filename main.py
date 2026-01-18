import sys
import json
import time
from feature_extractor import FeatureExtractor
from llm_reasoner import LLMReasoner

class MultimodalAnalyzer:
    def __init__(self):
        print("Initializing Multimodal Analyzer...")
        print("=" * 50)
        self.feature_extractor = FeatureExtractor()
        try:
            self.llm_reasoner = LLMReasoner()
            print("✓ LLM Reasoner initialized (OpenAI)")
        except Exception as e:
            print(f"⚠  LLM initialization warning: {e}")
            print("   Using fallback analysis only")
            self.llm_reasoner = None
    
    def analyze(self, image_path):
        """Main pipeline: extract features, reason with LLM, return structured output."""
        print(f"\nAnalyzing image: {image_path}")
        
        # 1. Extract meaningful visual features (Pre-LLM Intelligence)
        print("\n[1/2] Extracting image features...")
        start_time = time.time()
        features = self.feature_extractor.run_all(image_path)
        feature_time = time.time() - start_time
        
        print(f"   ✓ Object detection: {features['object_count']} objects found")
        print(f"   ✓ Text detection: {'Text found' if features['has_text'] else 'No text'}")
        print(f"   ✓ Image sharpness: {features['blur_assessment']} ({features['blur_score']:.2f}/1.0)")
        print(f"   ⏱️  Feature extraction time: {feature_time:.2f}s")
        
        # 2. Reason over features using LLM
        print("\n[2/2] Reasoning over features...")
        start_time = time.time()
        
        if self.llm_reasoner:
            analysis = self.llm_reasoner.analyze_features(image_path, features)
            print(f"   ✓ LLM analysis complete")
        else:
            # Use fallback from feature extractor
            analysis = {
                "image_quality_score": features['blur_score'],
                "issues_detected": [],
                "detected_objects": features['main_objects'],
                "text_detected": [features['detected_text']] if features['detected_text'] else [],
                "llm_reasoning_summary": "Fallback mode: Analysis based on blur score and object count only.",
                "final_verdict": "Suitable" if features['blur_score'] > 0.5 and features['object_count'] <= 3 else "Not suitable",
                "confidence": 0.6
            }
            print(f"   ✓ Fallback analysis complete")
        
        llm_time = time.time() - start_time
        print(f"   ⏱️  Reasoning time: {llm_time:.2f}s")
        
        # 3. Combine results
        total_time = feature_time + llm_time
        final_output = {
            **analysis,
            "processing_time": round(total_time, 2),
            "raw_features": {
                k: v for k, v in features.items() 
                if k not in ['detected_objects', 'main_objects']
            }
        }
        
        print(f"\n✅ Analysis complete in {total_time:.2f}s")
        return final_output

def print_summary(result):
    """Print a clean summary of the analysis."""
    print("\n" + "=" * 50)
    print("📊 ANALYSIS SUMMARY")
    print("=" * 50)
    
    print(f"Final Verdict: {result['final_verdict']}")
    print(f"Quality Score: {result['image_quality_score']:.2f}/1.0")
    print(f"Confidence: {result['confidence']:.2f}/1.0")
    
    if result['issues_detected']:
        print(f"Issues Found: {', '.join(result['issues_detected'])}")
    else:
        print("Issues Found: None ✓")
    
    if result['detected_objects']:
        print(f"Main Objects: {', '.join(result['detected_objects'])}")
    
    print(f"\n📝 Reasoning Summary:")
    print(f"  {result['llm_reasoning_summary']}")
    print("\n" + "=" * 50)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_image>")
        print("Example: python main.py samples/product_photo.jpg")
        sys.exit(1)
    
    analyzer = MultimodalAnalyzer()
    result = analyzer.analyze(sys.argv[1])
    
    print_summary(result)
    
    # Save detailed results to file
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_file = f"analysis_output_{timestamp}.json"
    
    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n📁 Detailed results saved to: {output_file}")