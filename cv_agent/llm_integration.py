#!/usr/bin/env python3
"""
LLM Integration Module for CV Content Rewriting
Integrates with Hugging Face models for intelligent content generation
"""

import os
import json
import re
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
import requests
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

@dataclass
class RewriteRequest:
    """Structure for content rewrite requests"""
    content: str
    target_role: Optional[str] = None
    target_skills: Optional[List[str]] = None
    tone: str = "professional"  # professional, casual, confident, humble
    length: str = "maintain"    # expand, condense, maintain
    focus: str = "general"      # achievements, skills, responsibilities, general

@dataclass
class RewriteResponse:
    """Structure for rewrite responses"""
    original_content: str
    rewritten_content: str
    improvements: List[str]
    confidence_score: float
    word_count_change: int

class LLMContentRewriter:
    """
    LLM-powered content rewriter for CV optimization
    Supports both local and API-based models
    """
    
    def __init__(self, huggingface_token: str = None, use_local: bool = False):
        self.huggingface_token = huggingface_token or os.getenv('HUGGINGFACE_TOKEN')
        self.use_local = use_local
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        
        # API endpoints
        self.api_base = "https://api-inference.huggingface.co/models"
        
        # Model configurations
        self.models = {
            'text_generation': 'microsoft/DialoGPT-medium',  # For general text generation
            'summarization': 'facebook/bart-large-cnn',      # For content condensing
            'text2text': 'google/flan-t5-base',            # For text transformation
            'grammar': 'grammarly/coedit-large'             # For grammar and style
        }
        
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize the LLM models based on configuration"""
        try:
            if self.use_local:
                print("🤖 Initializing local LLM models...")
                self._setup_local_models()
            else:
                print("🌐 Using Hugging Face API for LLM services...")
                self._test_api_connection()
                
        except Exception as e:
            print(f"⚠️ LLM initialization warning: {e}")
            print("💡 Falling back to template-based rewriting")
    
    def _setup_local_models(self):
        """Setup local models for offline use"""
        model_name = "microsoft/DialoGPT-small"  # Smaller model for local use
        
        print(f"📥 Loading model: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        
        # Set up text generation pipeline
        self.pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if torch.cuda.is_available() else -1
        )
        
        print("✅ Local models loaded successfully")
    
    def _test_api_connection(self):
        """Test Hugging Face API connection"""
        headers = {"Authorization": f"Bearer {self.huggingface_token}"}
        test_url = f"{self.api_base}/{self.models['text2text']}"
        
        response = requests.get(test_url, headers=headers)
        if response.status_code == 200:
            print("✅ Hugging Face API connection successful")
        else:
            raise Exception(f"API connection failed: {response.status_code}")
    
    def _call_huggingface_api(self, model_name: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Make API call to Hugging Face"""
        headers = {"Authorization": f"Bearer {self.huggingface_token}"}
        url = f"{self.api_base}/{model_name}"
        
        response = requests.post(url, headers=headers, json=inputs)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API call failed: {response.status_code} - {response.text}")
    
    def rewrite_cv_section(self, request: RewriteRequest) -> RewriteResponse:
        """
        Main method to rewrite CV content based on requirements
        """
        print(f"\n🔄 REWRITING CONTENT")
        print(f"   Original length: {len(request.content.split())} words")
        print(f"   Target role: {request.target_role or 'General'}")
        print(f"   Tone: {request.tone}")
        print(f"   Focus: {request.focus}")
        
        try:
            # Choose rewriting strategy based on request type
            if request.focus == "achievements":
                rewritten = self._rewrite_achievements(request)
            elif request.focus == "skills":
                rewritten = self._rewrite_skills_section(request)
            elif request.focus == "responsibilities":
                rewritten = self._rewrite_responsibilities(request)
            else:
                rewritten = self._general_rewrite(request)
            
            # Generate improvement suggestions
            improvements = self._generate_improvements(request.content, rewritten)
            
            # Calculate confidence and metrics
            confidence = self._calculate_confidence_score(request.content, rewritten)
            word_change = len(rewritten.split()) - len(request.content.split())
            
            response = RewriteResponse(
                original_content=request.content,
                rewritten_content=rewritten,
                improvements=improvements,
                confidence_score=confidence,
                word_count_change=word_change
            )
            
            self._print_rewrite_results(response)
            return response
            
        except Exception as e:
            print(f"❌ Rewriting failed: {e}")
            # Fallback to template-based rewriting
            return self._template_based_rewrite(request)
    
    def _rewrite_achievements(self, request: RewriteRequest) -> str:
        """Rewrite achievement-focused content"""
        prompt = self._build_achievement_prompt(request)
        
        if self.use_local and self.pipeline:
            return self._generate_with_local_model(prompt)
        else:
            return self._generate_with_api(prompt, "text2text")
    
    def _rewrite_skills_section(self, request: RewriteRequest) -> str:
        """Rewrite skills section with better organization"""
        prompt = self._build_skills_prompt(request)
        
        if self.use_local and self.pipeline:
            return self._generate_with_local_model(prompt)
        else:
            return self._generate_with_api(prompt, "text2text")
    
    def _rewrite_responsibilities(self, request: RewriteRequest) -> str:
        """Rewrite job responsibilities with action verbs"""
        prompt = self._build_responsibilities_prompt(request)
        
        if self.use_local and self.pipeline:
            return self._generate_with_local_model(prompt)
        else:
            return self._generate_with_api(prompt, "text2text")
    
    def _general_rewrite(self, request: RewriteRequest) -> str:
        """General content rewriting"""
        prompt = self._build_general_prompt(request)
        
        if self.use_local and self.pipeline:
            return self._generate_with_local_model(prompt)
        else:
            return self._generate_with_api(prompt, "text2text")
    
    def _build_achievement_prompt(self, request: RewriteRequest) -> str:
        """Build prompt for achievement rewriting"""
        base_prompt = f"""
Rewrite the following professional achievement to be more impactful and quantifiable:

Original: {request.content}

Requirements:
- Use strong action verbs
- Include specific metrics where possible
- Highlight business impact
- Tone: {request.tone}
- Target role: {request.target_role or 'professional role'}

Rewritten achievement:"""
        
        return base_prompt
    
    def _build_skills_prompt(self, request: RewriteRequest) -> str:
        """Build prompt for skills section rewriting"""
        skills_context = f"Skills to emphasize: {', '.join(request.target_skills)}" if request.target_skills else ""
        
        prompt = f"""
Rewrite and organize the following skills section for a CV:

Original: {request.content}

Requirements:
- Group related skills together
- Use industry-standard terminology
- Highlight most relevant skills first
- {skills_context}
- Format: Clean, scannable list

Rewritten skills section:"""
        
        return prompt
    
    def _build_responsibilities_prompt(self, request: RewriteRequest) -> str:
        """Build prompt for responsibilities rewriting"""
        prompt = f"""
Rewrite the following job responsibilities using strong action verbs and clear impact:

Original: {request.content}

Requirements:
- Start each point with action verbs
- Be specific about technologies and methods
- Show progression and growth
- Tone: {request.tone}
- Target role: {request.target_role or 'similar role'}

Rewritten responsibilities:"""
        
        return prompt
    
    def _build_general_prompt(self, request: RewriteRequest) -> str:
        """Build general rewriting prompt"""
        length_instruction = {
            'expand': 'Make it more detailed and comprehensive',
            'condense': 'Make it more concise while keeping key information',
            'maintain': 'Keep similar length but improve clarity and impact'
        }.get(request.length, 'Improve clarity and impact')
        
        prompt = f"""
Rewrite the following CV content to make it more professional and impactful:

Original: {request.content}

Requirements:
- {length_instruction}
- Tone: {request.tone}
- Target role: {request.target_role or 'professional position'}
- Focus on: {request.focus}

Rewritten content:"""
        
        return prompt
    
    def _generate_with_local_model(self, prompt: str) -> str:
        """Generate content using local model"""
        try:
            # Truncate prompt if too long
            max_length = 512
            if len(prompt) > max_length:
                prompt = prompt[:max_length]
            
            outputs = self.pipeline(
                prompt,
                max_length=len(prompt) + 150,
                num_return_sequences=1,
                temperature=0.7,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            generated = outputs[0]['generated_text']
            # Extract only the new content after the prompt
            if prompt in generated:
                result = generated.replace(prompt, '').strip()
            else:
                result = generated.strip()
            
            return result if result else self._template_fallback(prompt)
            
        except Exception as e:
            print(f"⚠️ Local generation failed: {e}")
            return self._template_fallback(prompt)
    
    def _generate_with_api(self, prompt: str, model_type: str = "text2text") -> str:
        """Generate content using Hugging Face API"""
        try:
            model_name = self.models.get(model_type, self.models['text2text'])
            
            inputs = {
                "inputs": prompt,
                "parameters": {
                    "max_length": len(prompt.split()) + 100,
                    "temperature": 0.7,
                    "num_return_sequences": 1
                }
            }
            
            response = self._call_huggingface_api(model_name, inputs)
            
            if isinstance(response, list) and len(response) > 0:
                generated = response[0].get('generated_text', '')
                # Clean up the response
                if prompt in generated:
                    result = generated.replace(prompt, '').strip()
                else:
                    result = generated.strip()
                
                return result if result else self._template_fallback(prompt)
            else:
                return self._template_fallback(prompt)
                
        except Exception as e:
            print(f"⚠️ API generation failed: {e}")
            return self._template_fallback(prompt)
    
    def _template_fallback(self, prompt: str) -> str:
        """Template-based fallback when LLM fails"""
        # Extract original content from prompt
        content_match = re.search(r'Original: (.*?)(?=\n\nRequirements:)', prompt, re.DOTALL)
        if content_match:
            original = content_match.group(1).strip()
            return self._apply_template_improvements(original)
        return "Content rewriting unavailable"
    
    def _apply_template_improvements(self, content: str) -> str:
        """Apply template-based improvements"""
        # Basic improvements using regex and templates
        improved = content
        
        # Improve action verbs
        verb_replacements = {
            r'\bworked on\b': 'developed',
            r'\bhelped with\b': 'assisted in',
            r'\bdid\b': 'executed',
            r'\bmade\b': 'created',
            r'\bwas responsible for\b': 'managed'
        }
        
        for pattern, replacement in verb_replacements.items():
            improved = re.sub(pattern, replacement, improved, flags=re.IGNORECASE)
        
        # Add quantifiable language
        if not re.search(r'\d+%|\d+\+|\$\d+', improved):
            improved += " (specific metrics to be added)"
        
        return improved
    
    def _template_based_rewrite(self, request: RewriteRequest) -> RewriteResponse:
        """Complete template-based rewrite fallback"""
        improved_content = self._apply_template_improvements(request.content)
        
        improvements = [
            "Applied stronger action verbs",
            "Suggested quantifiable metrics",
            "Enhanced professional language"
        ]
        
        return RewriteResponse(
            original_content=request.content,
            rewritten_content=improved_content,
            improvements=improvements,
            confidence_score=0.6,  # Lower confidence for template method
            word_count_change=len(improved_content.split()) - len(request.content.split())
        )
    
    def _generate_improvements(self, original: str, rewritten: str) -> List[str]:
        """Generate specific improvement suggestions"""
        improvements = []
        
        # Check for action verbs
        strong_verbs = ['developed', 'implemented', 'managed', 'led', 'created', 'optimized']
        if any(verb in rewritten.lower() for verb in strong_verbs):
            improvements.append("✅ Added strong action verbs")
        
        # Check for quantifiable elements
        if re.search(r'\d+%|\d+\+|\$\d+|x\d+', rewritten):
            improvements.append("✅ Included quantifiable metrics")
        
        # Check length optimization
        orig_words = len(original.split())
        new_words = len(rewritten.split())
        if new_words > orig_words:
            improvements.append("✅ Expanded with more detail")
        elif new_words < orig_words:
            improvements.append("✅ Made more concise")
        else:
            improvements.append("✅ Maintained length while improving quality")
        
        # Check for technical terms
        if len(re.findall(r'\b[A-Z]{2,}\b', rewritten)) > 0:
            improvements.append("✅ Included relevant technical terms")
        
        return improvements
    
    def _calculate_confidence_score(self, original: str, rewritten: str) -> float:
        """Calculate confidence score for the rewrite"""
        score = 0.5  # Base score
        
        # Length appropriateness
        orig_len = len(original.split())
        new_len = len(rewritten.split())
        length_ratio = min(new_len, orig_len) / max(new_len, orig_len)
        score += length_ratio * 0.2
        
        # Content similarity (basic check)
        common_words = set(original.lower().split()) & set(rewritten.lower().split())
        similarity = len(common_words) / max(len(original.split()), len(rewritten.split()))
        score += similarity * 0.3
        
        # Professional language indicators
        professional_indicators = ['achieved', 'developed', 'managed', 'led', 'implemented']
        if any(word in rewritten.lower() for word in professional_indicators):
            score += 0.2
        
        return min(score, 1.0)
    
    def _print_rewrite_results(self, response: RewriteResponse):
        """Print detailed rewrite results"""
        print(f"\n📝 REWRITE RESULTS")
        print(f"   Confidence: {response.confidence_score:.1%}")
        print(f"   Word change: {response.word_count_change:+d}")
        print(f"\n🔄 ORIGINAL:")
        print(f"   {response.original_content}")
        print(f"\n✨ REWRITTEN:")
        print(f"   {response.rewritten_content}")
        print(f"\n💡 IMPROVEMENTS MADE:")
        for improvement in response.improvements:
            print(f"   {improvement}")
    
    def batch_rewrite_cv_sections(self, cv_data: Dict[str, Any], target_role: str = None) -> Dict[str, Any]:
        """Batch rewrite multiple CV sections"""
        print(f"\n🔄 BATCH REWRITING CV SECTIONS")
        print(f"   Target role: {target_role or 'General optimization'}")
        
        rewritten_sections = {}
        
        # Sections to rewrite
        sections_to_rewrite = ['summary', 'experience', 'skills']
        
        for section_name in sections_to_rewrite:
            if section_name in cv_data.get('sections', {}) and cv_data['sections'][section_name].strip():
                print(f"\n📝 Rewriting {section_name.upper()} section...")
                
                request = RewriteRequest(
                    content=cv_data['sections'][section_name],
                    target_role=target_role,
                    focus=section_name if section_name != 'summary' else 'general',
                    tone='professional'
                )
                
                response = self.rewrite_cv_section(request)
                rewritten_sections[section_name] = response
        
        return rewritten_sections
    
    def suggest_cv_improvements(self, cv_data: Dict[str, Any]) -> List[str]:
        """Generate overall CV improvement suggestions"""
        suggestions = []
        
        # Check sections presence
        required_sections = ['summary', 'experience', 'skills', 'education']
        missing_sections = [s for s in required_sections if not cv_data.get('sections', {}).get(s, '').strip()]
        
        if missing_sections:
            suggestions.append(f"❗ Add missing sections: {', '.join(missing_sections)}")
        
        # Check content length
        for section, content in cv_data.get('sections', {}).items():
            if content.strip():
                word_count = len(content.split())
                if section == 'summary' and word_count < 50:
                    suggestions.append(f"📝 Expand {section} section (currently {word_count} words)")
                elif section == 'experience' and word_count < 100:
                    suggestions.append(f"📝 Add more detail to {section} section")
        
        # Check for quantifiable achievements
        experience_text = cv_data.get('sections', {}).get('experience', '')
        if not re.search(r'\d+%|\d+\+|\$\d+', experience_text):
            suggestions.append("📊 Add quantifiable achievements with specific metrics")
        
        # Check for action verbs
        weak_verbs = ['worked', 'helped', 'did', 'was responsible for']
        if any(verb in experience_text.lower() for verb in weak_verbs):
            suggestions.append("💪 Replace weak verbs with strong action verbs")
        
        return suggestions