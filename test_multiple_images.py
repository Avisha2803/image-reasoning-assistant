# test_multiple_images.py
import os
import json
from main import MultimodalAnalyzer

def test_images():
    analyzer = MultimodalAnalyzer()
    
    test_cases = [
        {
            "name": "Professional Product",
            "path": "samples/professional_product.jpg",  # You'll need to add this
            "expected": "Suitable"
        },
        {
            "name": "Casual Photo (your current)",
            "path": "samples/sample1.jpg",
            "expected": "Not suitable/Marginally suitable"
        },
        {
            "name": "Blurry Image",
            "path": "samples/blurry_test.jpg",  # Create or find one
            "expected": "Not suitable"
        }
    ]
    
    results = []
    
    for test in test_cases:
        if os.path.exists(test["path"]):
            print(f"\n{'='*60}")
            print(f"Testing: {test['name']}")
            print(f"Image: {test['path']}")
            print('='*60)
            
            try:
                result = analyzer.analyze(test["path"])
                results.append({
                    "test": test["name"],
                    "path": test["path"],
                    "verdict": result["final_verdict"],
                    "score": result["image_quality_score"],
                    "issues": result["issues_detected"]
                })
                
                # Save individual result
                filename = f"test_result_{test['name'].replace(' ', '_').lower()}.json"
                with open(filename, 'w') as f:
                    json.dump(result, f, indent=2)
                    
            except Exception as e:
                print(f"Error analyzing {test['path']}: {e}")
                results.append({
                    "test": test["name"],
                    "error": str(e)
                })
        else:
            print(f"\n⚠  Skipping {test['name']}: {test['path']} not found")
    
    # Print summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    for res in results:
        if 'error' not in res:
            print(f"{res['test']}:")
            print(f"  Verdict: {res['verdict']}")
            print(f"  Score: {res['score']}/1.0")
            print(f"  Issues: {', '.join(res['issues']) if res['issues'] else 'None'}")
        else:
            print(f"{res['test']}: ERROR - {res['error']}")
    
    # Save summary
    with open("test_summary.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to individual JSON files")
    print(f"Summary saved to: test_summary.json")

if __name__ == "__main__":
    test_images()