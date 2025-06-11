#!/usr/bin/env python3
"""
openai_evaluator.py

OpenAI API compatible evaluator for logical reasoning datasets.
Works with OpenAI API, vLLM, and other OpenAI-compatible endpoints.
"""

import time
import requests
import json
from typing import List, Tuple, Optional, Dict, Any
from pathlib import Path

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False

from base_evaluator import BaseEvaluator, EvaluationConfig, EvaluationResult


class OpenAIEvaluator(BaseEvaluator):
    """OpenAI API compatible evaluator for vLLM and similar endpoints."""
    
    def __init__(self, config: EvaluationConfig, 
                 api_base: str = "http://localhost:8000/v1",
                 api_key: str = "dummy-key"):
        """
        Initialize OpenAI evaluator.
        
        Args:
            config: Evaluation configuration
            api_base: API base URL (e.g., "http://localhost:8000/v1" for vLLM)
            api_key: API key (can be dummy for local vLLM)
        """
        super().__init__(config)
        
        self.api_base = api_base.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        # Set headers
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
    
    def check_model_availability(self) -> bool:
        """Check if the API endpoint is available."""
        try:
            response = self.session.get(f"{self.api_base}/models", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def get_available_models(self) -> List[str]:
        """Get list of available models from the API."""
        try:
            response = self.session.get(f"{self.api_base}/models", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model['id'] for model in data.get('data', [])]
        except requests.RequestException:
            pass
        return []
    
    def warm_up_model(self) -> bool:
        """Warm up model with a test request."""
        print(f"Warming up model {self.config.model_name}...")
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
        """Query the model via OpenAI-compatible API."""
        for attempt in range(self.config.max_retries):
            try:
                start_time = time.time()
                
                # Prepare request payload
                payload = {
                    "model": self.config.model_name,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": self.config.max_tokens,
                    "temperature": self.config.temperature,
                    "top_p": self.config.top_p,
                    "stream": False
                }
                
                response = self.session.post(
                    f"{self.api_base}/chat/completions",
                    json=payload,
                    timeout=self.config.timeout
                )
                
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extract response text
                    if 'choices' in data and len(data['choices']) > 0:
                        message = data['choices'][0].get('message', {})
                        content = message.get('content', '')
                        return content.strip(), response_time
                    else:
                        print(f"Unexpected response format: {data}")
                        return "ERROR", response_time
                else:
                    print(f"HTTP {response.status_code}: {response.text}")
                    
            except requests.Timeout:
                print(f"Timeout on attempt {attempt + 1}/{self.config.max_retries}")
            except requests.RequestException as e:
                print(f"Request failed on attempt {attempt + 1}/{self.config.max_retries}: {e}")
            except Exception as e:
                print(f"Unexpected error on attempt {attempt + 1}/{self.config.max_retries}: {e}")
            
            if attempt < self.config.max_retries - 1:
                delay = min(2 ** attempt, 10)  # Exponential backoff, max 10s
                print(f"Retrying in {delay}s...")
                time.sleep(delay)
        
        return "ERROR", 0.0
    
    def query_model_completion(self, prompt: str) -> Tuple[str, float]:
        """
        Alternative method using completions endpoint (for non-chat models).
        """
        for attempt in range(self.config.max_retries):
            try:
                start_time = time.time()
                
                payload = {
                    "model": self.config.model_name,
                    "prompt": prompt,
                    "max_tokens": self.config.max_tokens,
                    "temperature": self.config.temperature,
                    "top_p": self.config.top_p,
                    "stream": False
                }
                
                response = self.session.post(
                    f"{self.api_base}/completions",
                    json=payload,
                    timeout=self.config.timeout
                )
                
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'choices' in data and len(data['choices']) > 0:
                        text = data['choices'][0].get('text', '')
                        return text.strip(), response_time
                    else:
                        return "ERROR", response_time
                else:
                    print(f"HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < self.config.max_retries - 1:
                    time.sleep(2 ** attempt)
        
        return "ERROR", 0.0
    
    def evaluate_dataset(self, 
                        jsonl_file: Path, 
                        prompt_style: str = "standard") -> Tuple[Optional[Any], List[EvaluationResult]]:
        """Evaluate dataset with optional batch processing."""
        # Load questions
        questions = []
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questions.append(json.loads(line))
        
        if not questions:
            print(f"No questions found in {jsonl_file}")
            return None, []
        
        print(f"Evaluating {len(questions)} questions with {self.config.model_name}...")
        
        # Use batch processing if supported
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
            
            # Rate limiting for API calls
            time.sleep(0.1)
        
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
            
            # Small delay between requests
            time.sleep(0.1)
        
        return results


class vLLMEvaluator(OpenAIEvaluator):
    """Specialized evaluator for vLLM endpoints."""
    
    def __init__(self, config: EvaluationConfig, 
                 vllm_host: str = "localhost",
                 vllm_port: int = 8000):
        """Initialize vLLM evaluator."""
        api_base = f"http://{vllm_host}:{vllm_port}/v1"
        super().__init__(config, api_base=api_base, api_key="dummy-key")
    
    def warm_up_model(self) -> bool:
        """vLLM-specific warm up with health check."""
        # Check if vLLM is healthy
        try:
            health_response = self.session.get(f"{self.api_base.replace('/v1', '')}/health", timeout=5)
            if health_response.status_code != 200:
                print("⚠ vLLM health check failed")
        except:
            print("⚠ Could not connect to vLLM health endpoint")
        
        return super().warm_up_model()


# Register the evaluators
from base_evaluator import EvaluatorFactory
EvaluatorFactory.register_evaluator("openai", OpenAIEvaluator)
EvaluatorFactory.register_evaluator("vllm", vLLMEvaluator)