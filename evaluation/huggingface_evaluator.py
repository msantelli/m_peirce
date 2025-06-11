#!/usr/bin/env python3
"""
huggingface_evaluator.py

HuggingFace Transformers evaluator for logical reasoning datasets.
Supports local and remote models via transformers pipeline.
"""

import time
import torch
from typing import List, Tuple, Optional, Dict, Any
from pathlib import Path

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    import torch
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False
    print("transformers not installed. Run: pip install transformers torch")

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False

from base_evaluator import BaseEvaluator, EvaluationConfig, EvaluationResult


class HuggingFaceEvaluator(BaseEvaluator):
    """HuggingFace Transformers evaluator."""
    
    def __init__(self, config: EvaluationConfig):
        """Initialize HuggingFace evaluator."""
        if not HAS_TRANSFORMERS:
            raise ImportError("transformers library required for HuggingFace evaluator")
        
        super().__init__(config)
        
        self.device = config.device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.pipeline = None
        self.tokenizer = None
        self.model = None
        
        # Initialize model
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the model and pipeline."""
        try:
            print(f"Loading {self.config.model_name} on {self.device}...")
            
            # For chat models, we might need to handle them differently
            if any(chat_indicator in self.config.model_name.lower() 
                   for chat_indicator in ['chat', 'instruct', 'it']):
                self._initialize_chat_model()
            else:
                self._initialize_causal_model()
                
        except Exception as e:
            print(f"Error initializing model: {e}")
            raise
    
    def _initialize_chat_model(self):
        """Initialize chat/instruct model with conversation pipeline."""
        try:
            self.pipeline = pipeline(
                "text-generation",
                model=self.config.model_name,
                device=0 if self.device == "cuda" else -1,
                trust_remote_code=self.config.trust_remote_code,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                model_kwargs={
                    "cache_dir": None,
                    "use_cache": self.config.use_cache
                }
            )
            print("✓ Chat model loaded successfully")
        except Exception as e:
            print(f"Failed to load as chat model, trying causal: {e}")
            self._initialize_causal_model()
    
    def _initialize_causal_model(self):
        """Initialize causal language model."""
        self.pipeline = pipeline(
            "text-generation",
            model=self.config.model_name,
            device=0 if self.device == "cuda" else -1,
            trust_remote_code=self.config.trust_remote_code,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            model_kwargs={
                "cache_dir": None,
                "use_cache": self.config.use_cache
            }
        )
        print("✓ Causal model loaded successfully")
    
    def check_model_availability(self) -> bool:
        """Check if the model is available."""
        return self.pipeline is not None
    
    def get_available_models(self) -> List[str]:
        """Get list of available models."""
        # This would require querying HF Hub, for now return the configured model
        return [self.config.model_name] if self.pipeline else []
    
    def warm_up_model(self) -> bool:
        """Warm up model with a test prompt."""
        if not self.pipeline:
            return False
        
        print(f"Warming up {self.config.model_name}...")
        test_prompt = "Answer with just the letter A: A or B?"
        
        try:
            response, _ = self.query_model(test_prompt)
            if response and response != "ERROR":
                print("✓ Model warmed up successfully")
                return True
        except Exception as e:
            print(f"✗ Model warm-up failed: {e}")
        
        return False
    
    def query_model(self, prompt: str) -> Tuple[str, float]:
        """Query the HuggingFace model."""
        if not self.pipeline:
            return "ERROR", 0.0
        
        for attempt in range(self.config.max_retries):
            try:
                start_time = time.time()
                
                # Configure generation parameters
                generation_kwargs = {
                    "max_new_tokens": self.config.max_tokens,
                    "temperature": self.config.temperature,
                    "top_p": self.config.top_p,
                    "do_sample": True if self.config.temperature > 0 else False,
                    "pad_token_id": self.pipeline.tokenizer.eos_token_id,
                    "return_full_text": False  # Only return generated text
                }
                
                # Handle different model types
                if hasattr(self.pipeline.tokenizer, 'apply_chat_template'):
                    # Chat model - format as conversation
                    messages = [{"role": "user", "content": prompt}]
                    try:
                        formatted_prompt = self.pipeline.tokenizer.apply_chat_template(
                            messages, tokenize=False, add_generation_prompt=True
                        )
                    except:
                        # Fallback if chat template fails
                        formatted_prompt = prompt
                else:
                    formatted_prompt = prompt
                
                # Generate response
                outputs = self.pipeline(formatted_prompt, **generation_kwargs)
                
                response_time = time.time() - start_time
                
                # Extract generated text
                if isinstance(outputs, list) and len(outputs) > 0:
                    generated_text = outputs[0].get('generated_text', '')
                else:
                    generated_text = str(outputs)
                
                return generated_text.strip(), response_time
                
            except Exception as e:
                print(f"Attempt {attempt + 1}/{self.config.max_retries} failed: {e}")
                if attempt < self.config.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    return "ERROR", 0.0
        
        return "ERROR", 0.0
    
    def evaluate_dataset(self, 
                        jsonl_file: Path, 
                        prompt_style: str = "standard") -> Tuple[Optional[Any], List[EvaluationResult]]:
        """Evaluate dataset with optional batch processing."""
        # Load questions
        import json
        questions = []
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questions.append(json.loads(line))
        
        if not questions:
            print(f"No questions found in {jsonl_file}")
            return None, []
        
        print(f"Evaluating {len(questions)} questions with {self.config.model_name}...")
        
        # Use batch processing if batch_size > 1
        if self.config.batch_size > 1:
            return self._evaluate_dataset_batch(questions, prompt_style, jsonl_file)
        else:
            return super().evaluate_dataset(jsonl_file, prompt_style)
    
    def _evaluate_dataset_batch(self, questions: List[Dict[str, Any]], 
                               prompt_style: str, jsonl_file: Path) -> Tuple[Optional[Any], List[EvaluationResult]]:
        """Evaluate dataset using batch processing."""
        results = []
        by_rule_stats = {}
        unclear_count = 0
        
        # Process in batches
        batch_size = self.config.batch_size
        batches = [questions[i:i + batch_size] for i in range(0, len(questions), batch_size)]
        
        if HAS_TQDM:
            batches = tqdm(batches, desc=f"Processing batches")
        
        for batch in batches:
            batch_results = self._process_batch(batch, prompt_style)
            results.extend(batch_results)
            
            # Update statistics
            for result in batch_results:
                good_type = result.good_argument_type
                if good_type not in by_rule_stats:
                    by_rule_stats[good_type] = {'correct': 0, 'total': 0}
                
                by_rule_stats[good_type]['total'] += 1
                if result.is_correct:
                    by_rule_stats[good_type]['correct'] += 1
                
                if result.model_answer in ["UNCLEAR", "ERROR"]:
                    unclear_count += 1
        
        # Calculate final statistics
        from base_evaluator import ModelStats
        correct_total = sum(1 for r in results if r.is_correct)
        accuracy = correct_total / len(results) * 100
        avg_response_time = sum(r.response_time for r in results if r.response_time > 0) / len(results)
        
        by_rule_accuracy = {}
        for rule, stats in by_rule_stats.items():
            by_rule_accuracy[rule] = (stats['correct'], stats['total'])
        
        model_stats = ModelStats(
            model_name=self.config.model_name,
            dataset_name=jsonl_file.stem,
            total_questions=len(results),
            correct_answers=correct_total,
            accuracy=accuracy,
            avg_response_time=avg_response_time,
            unclear_responses=unclear_count,
            by_rule_accuracy=by_rule_accuracy
        )
        
        return model_stats, results
    
    def _process_batch(self, batch: List[Dict[str, Any]], prompt_style: str) -> List[EvaluationResult]:
        """Process a batch of questions."""
        results = []
        
        for question in batch:
            result = self._evaluate_single_question(question, prompt_style)
            results.append(result)
            
            # Small delay to avoid overwhelming GPU
            time.sleep(0.05)
        
        return results


# Register the evaluator
from base_evaluator import EvaluatorFactory
EvaluatorFactory.register_evaluator("huggingface", HuggingFaceEvaluator)