#!/usr/bin/env python3
"""
evaluator.py

Unified evaluator containing all model provider implementations.
Supports HuggingFace, OpenAI, and Ollama models through consistent interface.
"""

import requests
import json
import time
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path

from base_evaluator import BaseEvaluator, EvaluationConfig


class HuggingFaceEvaluator(BaseEvaluator):
    """HuggingFace model evaluator using transformers library."""
    
    def __init__(self, config: EvaluationConfig):
        super().__init__(config)
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self):
        """Load HuggingFace model and tokenizer."""
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            import torch
        except ImportError:
            raise RuntimeError(
                "HuggingFace support requires: pip install transformers torch"
            )
        
        print(f"Loading HuggingFace model: {self.config.model_name}")
        
        # Determine device
        if self.config.device:
            device = self.config.device
        elif torch.cuda.is_available():
            device = "cuda"
        else:
            device = "cpu"
        
        self.device = device
        
        try:
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.config.model_name,
                trust_remote_code=self.config.trust_remote_code
            )
            
            # Add pad token if missing
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.model_name,
                trust_remote_code=self.config.trust_remote_code,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                device_map="auto" if device == "cuda" else None
            )
            
            if device == "cpu":
                self.model = self.model.to(device)
            
            self.model.eval()
            print(f"✅ Model loaded successfully on {device}")
            
        except Exception as e:
            raise RuntimeError(f"Failed to load HuggingFace model: {e}")
    
    def query_model(self, prompt: str) -> Tuple[str, float]:
        """Query HuggingFace model."""
        import torch
        
        start_time = time.time()
        
        try:
            # Tokenize input
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=2048
            ).to(self.device)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=self.config.max_tokens,
                    temperature=self.config.temperature,
                    do_sample=True if self.config.temperature > 0 else False,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            input_length = inputs['input_ids'].shape[1]
            generated_tokens = outputs[0][input_length:]
            response = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)
            
            response_time = time.time() - start_time
            return response.strip(), response_time
            
        except Exception as e:
            response_time = time.time() - start_time
            raise RuntimeError(f"HuggingFace query failed: {e}")


class OpenAIEvaluator(BaseEvaluator):
    """OpenAI API evaluator supporting OpenAI and compatible endpoints."""
    
    def __init__(self, config: EvaluationConfig, api_base: str = None, api_key: str = None):
        super().__init__(config)
        self.api_base = api_base or "https://api.openai.com/v1"
        self.api_key = api_key
        self.session = requests.Session()
        
        if not self.api_key:
            raise ValueError("API key is required for OpenAI evaluator")
        
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
    
    def check_model_availability(self) -> bool:
        """Check if OpenAI API is accessible."""
        try:
            response = self.session.get(
                f"{self.api_base}/models",
                timeout=10
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def query_model(self, prompt: str) -> Tuple[str, float]:
        """Query OpenAI API."""
        start_time = time.time()
        
        try:
            payload = {
                "model": self.config.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": self.config.max_tokens,
                "temperature": self.config.temperature
            }
            
            response = self.session.post(
                f"{self.api_base}/chat/completions",
                json=payload,
                timeout=self.config.timeout
            )
            
            response_time = time.time() - start_time
            
            if response.status_code != 200:
                raise RuntimeError(f"API request failed: {response.status_code} - {response.text}")
            
            data = response.json()
            content = data['choices'][0]['message']['content']
            
            return content.strip(), response_time
            
        except Exception as e:
            response_time = time.time() - start_time
            raise RuntimeError(f"OpenAI query failed: {e}")


class OllamaEvaluator(BaseEvaluator):
    """Ollama evaluator for local models via Ollama API."""
    
    def __init__(self, config: EvaluationConfig, ollama_url: str = "http://localhost:11434"):
        super().__init__(config)
        self.ollama_url = ollama_url
        self.session = requests.Session()
    
    def check_model_availability(self) -> bool:
        """Check if Ollama is running and model is available."""
        try:
            # Check if Ollama is running
            response = self.session.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code != 200:
                return False
            
            # Check if specific model is available
            data = response.json()
            available_models = [model['name'] for model in data.get('models', [])]
            return self.config.model_name in available_models
            
        except Exception:
            return False
    
    def get_available_models(self) -> List[str]:
        """Get list of available models from Ollama."""
        try:
            response = self.session.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
        except Exception:
            pass
        return []
    
    def warm_up_model(self) -> bool:
        """Warm up Ollama model."""
        print(f"Warming up Ollama model: {self.config.model_name}")
        try:
            test_prompt = "Answer with just the letter A: A or B?"
            _, _ = self.query_model(test_prompt)
            return True
        except Exception:
            return False
    
    def query_model(self, prompt: str) -> Tuple[str, float]:
        """Query Ollama model."""
        start_time = time.time()
        
        payload = {
            "model": self.config.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.config.temperature,
                "num_predict": self.config.max_tokens
            }
        }
        
        try:
            response = self.session.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=self.config.timeout
            )
            
            response_time = time.time() - start_time
            
            if response.status_code != 200:
                raise RuntimeError(f"Ollama request failed: {response.status_code} - {response.text}")
            
            data = response.json()
            content = data.get('response', '')
            
            return content.strip(), response_time
            
        except Exception as e:
            response_time = time.time() - start_time
            raise RuntimeError(f"Ollama query failed: {e}")


def create_evaluator(evaluator_type: str, config: EvaluationConfig, **kwargs) -> BaseEvaluator:
    """
    Factory function to create appropriate evaluator.
    
    Args:
        evaluator_type: "huggingface", "openai", or "ollama"
        config: EvaluationConfig object
        **kwargs: Additional provider-specific arguments
    
    Returns:
        Appropriate evaluator instance
    """
    if evaluator_type.lower() == "huggingface":
        return HuggingFaceEvaluator(config)
    
    elif evaluator_type.lower() == "openai":
        api_base = kwargs.get('api_base')
        api_key = kwargs.get('api_key')
        return OpenAIEvaluator(config, api_base, api_key)
    
    elif evaluator_type.lower() == "ollama":
        ollama_url = kwargs.get('ollama_url', "http://localhost:11434")
        return OllamaEvaluator(config, ollama_url)
    
    else:
        raise ValueError(f"Unknown evaluator type: {evaluator_type}. Use 'huggingface', 'openai', or 'ollama'")


# Legacy support functions for backward compatibility
def evaluate_with_ollama(jsonl_file: Path, model_name: str, prompt_style: str = "standard",
                        ollama_url: str = "http://localhost:11434", timeout: int = 60):
    """Legacy function for Ollama evaluation."""
    config = EvaluationConfig(model_name=model_name, timeout=timeout)
    evaluator = OllamaEvaluator(config, ollama_url)
    return evaluator.evaluate_dataset(jsonl_file, prompt_style)


def evaluate_with_huggingface(jsonl_file: Path, model_name: str, prompt_style: str = "standard",
                              device: str = None, timeout: int = 60):
    """Legacy function for HuggingFace evaluation."""
    config = EvaluationConfig(model_name=model_name, device=device, timeout=timeout)
    evaluator = HuggingFaceEvaluator(config)
    return evaluator.evaluate_dataset(jsonl_file, prompt_style)


def evaluate_with_openai(jsonl_file: Path, model_name: str, prompt_style: str = "standard",
                        api_key: str = None, api_base: str = None, timeout: int = 60):
    """Legacy function for OpenAI evaluation."""
    config = EvaluationConfig(model_name=model_name, timeout=timeout)
    evaluator = OpenAIEvaluator(config, api_base, api_key)
    return evaluator.evaluate_dataset(jsonl_file, prompt_style)