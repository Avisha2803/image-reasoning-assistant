import json
import re
from config import Config

class LLMReasoner:
    def __init__(self):
        self.provider = Config.LLM_PROVIDER.lower()
        self.client = None
        self.model = None
        
        print(f"Initializing LLM Reasoner with provider: {self.provider}")
        
        if self.provider == "openai":
            self._init_openai()
        elif self.provider == "gemini":
            self._init_gemini()
        else:
            print("⚠  Using rule-based analysis only")
    
    def _init_openai(self):
        """Initialize OpenAI client."""
        try:
            from openai import OpenAI
            if not Config.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not found")
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
            self.model = Config.OPENAI_MODEL
            print(f"✓ LLM: OpenAI ({self.model})")
        except Exception as e:
            print(f"⚠  OpenAI init failed: {e}")
    
    def _init_gemini(self):
        """Initialize Google Gemini client."""
        try:
            import google.generativeai as genai
            if not Config.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY not found. Please add GEMINI_API_KEY to your .env file")
            
            genai.configure(api_key=Config.GEMINI_API_KEY)
            
            # Try different model names
            model_names_to_try = [
                "gemini-2.0-flash-latest",      # Latest stable
                "gemini-2.0-flash",             # Alternative
                "gemini-2.0-flash-001",         # Another alternative
                "gemini-pro-latest",            # Pro version
                "gemini-1.5-flash"              # Original (might not exist)
            ]
            
            for model_name in model_names_to_try:
                try:
                    print(f"  Trying model: {model_name}")
                    self.client = genai.GenerativeModel(model_name)
                    # Test with a simple prompt to verify
                    test_response = self.client.generate_content("Hello")
                    self.model = model_name
                    print(f"✓ LLM: Google Gemini ({self.model})")
                    return
                except Exception as model_error:
                    print(f"    Model {model_name} failed: {str(model_error)[:80]}...")
                    continue

            # If none worked, try listing and using first available
            print("  Listing all available models...")
            models = genai.list_models()
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    print(f"  Available for generateContent: {model.name}")
                    try:
                        self.client = genai.GenerativeModel(model.name)
                        self.model = model.name
                        print(f"✓ LLM: Using available model {self.model}")
                        return
                    except:
                        continue
        
            raise ValueError("No working Gemini model found")
        
        except Exception as e:
            print(f"⚠  Gemini init failed: {e}")
            print("   Please check your API key at: https://aistudio.google.com/app/apikey")
    
    def analyze_features(self, image_path, features):
        """Hybrid analysis: LLM + rule-based validation."""
        
        print(f"\n[2/2] Reasoning over features...")
        
        # Get LLM analysis
        llm_result = self._get_llm_analysis(features) if self.client else None
        
        # Get rule-based analysis
        rule_result = self._enhanced_fallback_analysis(features)
        
        # Combine results intelligently
        combined_result = self._combine_analyses(llm_result, rule_result, features)
        
        # Add processing metadata
        combined_result["analysis_method"] = "hybrid" if llm_result else "rule-based"
        if llm_result:
            combined_result["llm_score"] = llm_result.get('image_quality_score', 'N/A')
        combined_result["rule_score"] = rule_result.get('image_quality_score', 'N/A')
        
        return combined_result
    
    def _get_llm_analysis(self, features):
        """Get analysis from LLM."""
        try:
            prompt = self._build_prompt(features)
            
            if self.provider == "openai":
                result = self._call_openai(prompt)
                print(f"  ✓ OpenAI analysis complete")
            else:  # gemini
                result = self._call_gemini(prompt)
                print(f"  ✓ Gemini analysis complete")
            
            return result
            
        except Exception as e:
            print(f"  ⚠  {self.provider.capitalize()} API failed: {e}")
            return None
    
    def _combine_analyses(self, llm_result, rule_result, features):
        """Intelligently combine LLM and rule-based results."""
        
        if not llm_result:
            # No LLM result, use rule-based
            print("  Using rule-based analysis (LLM failed)")
            return rule_result
        
        # Check for obvious LLM errors
        llm_issues = self._validate_llm_result(llm_result, features)
        
        if llm_issues:
            print(f"  LLM validation issues detected: {', '.join(llm_issues)}")
            # LLM made questionable call, blend with rule-based
            return self._blend_results(llm_result, rule_result, weight=0.3)  # 30% LLM, 70% rules
        else:
            # LLM result seems reasonable
            print("  Using LLM analysis (validated)")
            return llm_result
    
    def _validate_llm_result(self, llm_result, features):
        """Validate LLM result against basic rules."""
        issues = []
        
        # Check 1: If image is blurry but LLM gave high score
        if features['blur_score'] < 0.3 and llm_result.get('image_quality_score', 0) > 0.7:
            issues.append("LLM gave high score to blurry image")
        
        # Check 2: If contains person/bed but LLM says suitable
        objects = [obj['object'].lower() for obj in features['detected_objects']]
        personal_items = ['person', 'bed', 'couch', 'sofa', 'food', 'toilet', 'bathroom', 'kitchen']
        has_personal = any(any(item in obj for item in personal_items) for obj in objects)
        
        if has_personal and llm_result.get('final_verdict', '').lower().startswith('suitable'):
            issues.append("LLM approved image with personal items")
        
        # Check 3: Score seems unrealistic
        score = llm_result.get('image_quality_score', 0)
        if score > 0.9 and (features['blur_score'] < 0.5 or len(features['detected_objects']) > 5):
            issues.append("LLM score seems unrealistically high")
        
        # Check 4: If LLM missed obvious text issues
        if features['has_text'] and len(features['detected_text']) > 20:
            text_lower = features['detected_text'].lower()
            casual_indicators = ['personal', 'name', 'www.', 'http://', '@', 'casual', 'funny', 'meme']
            if any(indicator in text_lower for indicator in casual_indicators):
                if 'contains text' not in ' '.join(llm_result.get('issues_detected', [])).lower():
                    issues.append("LLM missed casual text issue")
        
        return issues
    
    def _blend_results(self, llm_result, rule_result, weight=0.5):
        """Blend LLM and rule-based results."""
        llm_weight = weight
        rule_weight = 1 - weight
        
        # Blend scores
        llm_score = llm_result.get('image_quality_score', 0.5)
        rule_score = rule_result.get('image_quality_score', 0.5)
        blended_score = (llm_score * llm_weight) + (rule_score * rule_weight)
        
        # Combine issues (unique)
        llm_issues = set(llm_result.get('issues_detected', []))
        rule_issues = set(rule_result.get('issues_detected', []))
        blended_issues = list(llm_issues.union(rule_issues))
        
        # Determine verdict based on blended score and issues
        if blended_score >= 0.7 and len(blended_issues) == 0:
            verdict = "Suitable for professional e-commerce use"
        elif blended_score >= 0.5 and len(blended_issues) <= 1:
            verdict = "Marginally suitable for professional e-commerce use"
        else:
            verdict = "Not suitable for professional e-commerce use"
        
        # Use LLM reasoning if available, otherwise rule-based
        llm_reasoning = llm_result.get('llm_reasoning_summary', '')
        rule_reasoning = rule_result.get('llm_reasoning_summary', '')
        
        if llm_reasoning and rule_reasoning:
            reasoning = f"Hybrid analysis: LLM noted '{llm_reasoning[:100]}...' Rules added: {', '.join(rule_issues) if rule_issues else 'no additional issues'}."
        elif llm_reasoning:
            reasoning = f"LLM analysis: {llm_reasoning}"
        else:
            reasoning = rule_reasoning
        
        # Combine other fields
        detected_objects = llm_result.get('detected_objects', []) or rule_result.get('detected_objects', [])
        text_detected = llm_result.get('text_detected', []) or rule_result.get('text_detected', [])
        
        # Calculate confidence
        llm_confidence = llm_result.get('confidence', 0.7)
        rule_confidence = rule_result.get('confidence', 0.7)
        blended_confidence = (llm_confidence * llm_weight) + (rule_confidence * rule_weight)
        
        return {
            "image_quality_score": round(blended_score, 2),
            "issues_detected": blended_issues,
            "detected_objects": detected_objects[:5],  # Limit to top 5
            "text_detected": text_detected,
            "llm_reasoning_summary": reasoning[:300],  # Limit length
            "final_verdict": verdict,
            "confidence": round(blended_confidence, 2)
        }
    
    def _build_prompt(self, features):
        """Build analysis prompt."""
        return f"""Analyze this image for e-commerce product suitability.

EXTRACTED FEATURES:
- Objects detected: {features['detected_objects']}
- Main objects: {features['top_objects']}
- Text found: "{features['detected_text']}"
- Image sharpness: {features['blur_assessment']} (score: {features['blur_score']}/1.0)
- Total objects: {features['object_count']}

CRITERIA FOR E-COMMERCE PRODUCT IMAGES:
1. Professional: Clean background, good lighting, no personal items
2. Product-focused: Product should be main subject
3. High quality: Sharp, well-lit, no clutter
4. Brand-appropriate: Minimal/no casual text

IMPORTANT: Be strict about personal items (person, bed, furniture, food) - these make images unsuitable for professional e-commerce.

ANALYSIS TASK:
1. Score image quality 0-1 (be realistic, not overly generous)
2. List any issues found (be specific)
3. Provide final verdict
4. Explain reasoning briefly

OUTPUT FORMAT (JSON only):
{{
    "image_quality_score": 0.85,
    "issues_detected": ["issue1", "issue2"],
    "detected_objects": ["object1", "object2"],
    "text_detected": [],
    "llm_reasoning_summary": "Brief explanation...",
    "final_verdict": "Suitable for professional e-commerce use",
    "confidence": 0.8
}}

Return ONLY valid JSON, no other text."""
    
    def _call_openai(self, prompt):
        """Call OpenAI API."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    
    def _call_gemini(self, prompt):
        """Call Google Gemini API."""
        response = self.client.generate_content(prompt)
        text = response.text.strip()
        
        # Clean the response
        text = text.replace('```json', '').replace('```', '').strip()
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to extract JSON
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except:
                    pass
            
            # If still fails, parse text
            return self._parse_text_response(text)
    
    def _parse_text_response(self, text):
        """Parse text response into structured format."""
        # Simple parsing for demonstration
        issues = []
        text_lower = text.lower()
        
        if "clutter" in text_lower or "messy" in text_lower:
            issues.append("background clutter")
        if "blur" in text_lower or "fuzzy" in text_lower:
            issues.append("blurry")
        if "dark" in text_lower or "dim" in text_lower or "lighting" in text_lower:
            issues.append("poor lighting")
        if "person" in text_lower or "people" in text_lower:
            issues.append("contains people")
        
        # Try to extract score
        score_match = re.search(r'(\d+\.\d+|\d+)', text)
        score = 0.7
        if score_match:
            try:
                score = float(score_match.group())
                score = max(0.1, min(1.0, score / 10 if score > 1 else score))
            except:
                pass
        
        # Determine verdict from text
        if "not suitable" in text_lower or "unsuitable" in text_lower or "poor" in text_lower:
            verdict = "Not suitable for professional e-commerce use"
        elif "suitable" in text_lower or "good" in text_lower or "excellent" in text_lower:
            verdict = "Suitable for professional e-commerce use"
        else:
            verdict = "Analysis completed"
        
        return {
            "image_quality_score": round(score, 2),
            "issues_detected": issues,
            "detected_objects": [],
            "text_detected": [],
            "llm_reasoning_summary": f"Parsed from LLM response: {text[:200]}...",
            "final_verdict": verdict,
            "confidence": 0.6
        }
    
    def _enhanced_fallback_analysis(self, features):
        """Enhanced rule-based analysis with better scoring."""
        print("  Using enhanced rule-based analysis...")
        
        # Initialize scoring
        scores = {
            "sharpness": features['blur_score'],
            "object_focus": 0.0,
            "background": 0.5,
            "professionalism": 0.5
        }
        
        issues = []
        warnings = []
        
        # Analyze objects
        objects = [obj['object'].lower() for obj in features['detected_objects']]
        
        # Product vs non-product objects
        product_keywords = ['shoe', 'bag', 'watch', 'phone', 'laptop', 'product', 
                           'electronics', 'clothing', 'accessory', 'jewelry', 'perfume',
                           'cosmetic', 'makeup', 'tool', 'equipment', 'instrument']
        non_product_keywords = ['person', 'face', 'hand', 'bed', 'couch', 'sofa',
                               'food', 'animal', 'pet', 'toilet', 'bathroom', 'kitchen',
                               'child', 'baby', 'dog', 'cat']
        
        product_count = sum(1 for obj in objects if any(kw in obj for kw in product_keywords))
        non_product_count = sum(1 for obj in objects if any(kw in obj for kw in non_product_keywords))
        
        # Object focus score
        if product_count > 0:
            scores['object_focus'] = 0.8
            if product_count == 1:
                scores['object_focus'] = 0.9
        elif non_product_count == 0:
            scores['object_focus'] = 0.6  # Neutral objects
        else:
            scores['object_focus'] = 0.3
            issues.append(f"contains {non_product_count} non-product object(s)")
        
        # Background/clutter analysis
        total_objects = len(objects)
        if total_objects <= 2:
            scores['background'] = 0.8  # Clean background
        elif total_objects <= 4:
            scores['background'] = 0.6  # Some clutter
            warnings.append("multiple objects (potential clutter)")
        else:
            scores['background'] = 0.3  # Cluttered
            issues.append("too many objects (cluttered background)")
        
        # Text analysis
        if features['has_text']:
            text = features['detected_text'].lower()
            if len(text) > 10:  # Meaningful text
                # Check if it looks like product text
                product_text_indicators = ['$', 'price', 'sale', 'brand', 'model', 'size', 'product', 'item']
                casual_text_indicators = ['personal', 'name', 'www.', 'http', '@', 'funny', 'meme', 'lol']
                
                has_product_text = any(indicator in text for indicator in product_text_indicators)
                has_casual_text = any(indicator in text for indicator in casual_text_indicators)
                
                if has_product_text and not has_casual_text:
                    scores['professionalism'] = 0.7  # Product text is OK
                    warnings.append("contains product/brand text")
                elif has_casual_text:
                    scores['professionalism'] = 0.3  # Casual text is bad
                    issues.append("contains casual/personal text")
                else:
                    scores['professionalism'] = 0.5  # Neutral text
                    warnings.append("contains text")
            else:
                scores['professionalism'] = 0.6  # Minimal text
        else:
            scores['professionalism'] = 0.8  # No text is good
        
        # Calculate weighted final score
        weights = {
            "sharpness": 0.3,      # 30% - image quality
            "object_focus": 0.4,   # 40% - subject matter
            "background": 0.2,     # 20% - composition
            "professionalism": 0.1 # 10% - text/branding
        }
        
        final_score = sum(scores[category] * weights[category] for category in scores)
        final_score = max(0.1, min(0.95, final_score))
        
        # Determine verdict
        if final_score >= 0.7 and len(issues) == 0:
            verdict = "Suitable for professional e-commerce use"
            confidence = final_score
        elif final_score >= 0.5 and len(issues) <= 1:
            verdict = "Marginally suitable for professional e-commerce use"
            confidence = final_score * 0.9
        else:
            verdict = "Not suitable for professional e-commerce use"
            confidence = max(0.5, final_score)
        
        # Build reasoning summary
        reasoning_parts = []
        
        if scores['sharpness'] >= 0.7:
            reasoning_parts.append("Image is sharp and clear")
        elif scores['sharpness'] >= 0.4:
            reasoning_parts.append("Image has acceptable sharpness")
        else:
            reasoning_parts.append("Image is blurry")
        
        if product_count > 0:
            reasoning_parts.append(f"Contains {product_count} product-like object(s)")
        elif non_product_count > 0:
            reasoning_parts.append(f"Contains {non_product_count} non-product object(s)")
        
        if features['has_text']:
            reasoning_parts.append("Contains text")
        
        if len(issues) > 0:
            reasoning_parts.append(f"Has {len(issues)} quality issue(s)")
        elif len(warnings) > 0:
            reasoning_parts.append(f"Has {len(warnings)} warning(s)")
        
        reasoning_summary = "Rule-based analysis: " + ". ".join(reasoning_parts) + "."
        
        return {
            "image_quality_score": round(final_score, 2),
            "issues_detected": issues,
            "warnings": warnings,
            "detected_objects": features['top_objects'][:5],
            "text_detected": [features['detected_text']] if features['detected_text'] else [],
            "llm_reasoning_summary": reasoning_summary,
            "final_verdict": verdict,
            "confidence": round(confidence, 2),
            "score_breakdown": {k: round(v, 2) for k, v in scores.items()}
        }