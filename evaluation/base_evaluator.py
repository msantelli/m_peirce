#!/usr/bin/env python3
"""
base_evaluator.py

Abstract base classes for different model evaluation interfaces.
Provides a unified API for testing logical reasoning across different model types.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass
from pathlib import Path
import json
import time

# Simplified parsing - no complex reasoning parser needed
HAS_REASONING_PARSER = False

@dataclass
class EvaluationConfig:
    """Configuration for model evaluation."""
    model_name: str
    max_tokens: int = 10
    temperature: float = 0.1
    timeout: int = 60
    device: Optional[str] = None  # For HF models
    trust_remote_code: bool = False


@dataclass
class EvaluationResult:
    """Single evaluation result."""
    question_id: int
    model_answer: str
    correct_answer: str
    is_correct: bool
    good_argument_type: str
    bad_argument_type: str
    response_time: float
    raw_response: str
    parsing_method: Optional[str] = None


@dataclass
class ModelStats:
    """Statistics for a model evaluation."""
    model_name: str
    dataset_name: str
    total_questions: int
    correct_answers: int
    accuracy: float
    avg_response_time: float
    unclear_responses: int
    by_rule_accuracy: Dict[str, Tuple[int, int]]  # rule -> (correct, total)


class BaseEvaluator(ABC):
    """Abstract base class for model evaluators."""
    
    def __init__(self, config: EvaluationConfig):
        """Initialize evaluator with configuration."""
        self.config = config
        self.session_start_time = time.time()
    
    @abstractmethod
    def check_model_availability(self) -> bool:
        """Check if the model is available and accessible."""
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[str]:
        """Get list of available models."""
        pass
    
    @abstractmethod
    def warm_up_model(self) -> bool:
        """Warm up model by sending a test request."""
        pass
    
    @abstractmethod
    def query_model(self, prompt: str) -> Tuple[str, float]:
        """
        Query model with a prompt.
        
        Returns:
            Tuple of (response_text, response_time_seconds)
        """
        pass
    
    def parse_model_response(self, response: str) -> Tuple[str, Dict[str, Any]]:
        """
        Parse model response to extract A or B.
        
        Returns:
            Tuple of (answer, metadata_dict)
        """
        metadata = {"parsing_method": None}
        
        if not response or response == "ERROR":
            return "ERROR", metadata
        
        response_clean = response.strip().upper()
        
        # Direct single letter
        if response_clean in ['A', 'B']:
            metadata["parsing_method"] = "direct"
            return response_clean, metadata
            
        # Response starts with A or B
        if response_clean.startswith('A'):
            metadata["parsing_method"] = "starts_with"
            return 'A', metadata
        elif response_clean.startswith('B'):
            metadata["parsing_method"] = "starts_with"
            return 'B', metadata
            
        # Look for answer patterns
        if any(pattern in response_clean for pattern in ['OPTION A', 'CHOOSE A', 'ANSWER A', 'A:']):
            metadata["parsing_method"] = "pattern"
            return 'A', metadata
        elif any(pattern in response_clean for pattern in ['OPTION B', 'CHOOSE B', 'ANSWER B', 'B:']):
            metadata["parsing_method"] = "pattern"
            return 'B', metadata
            
        # Count occurrences as fallback
        a_count = response_clean.count('A')
        b_count = response_clean.count('B')
        
        if a_count > b_count:
            metadata["parsing_method"] = "count"
            return 'A', metadata
        elif b_count > a_count:
            metadata["parsing_method"] = "count"
            return 'B', metadata
        
        metadata["parsing_method"] = "unclear"
        return "UNCLEAR", metadata
    
    def create_prompt(self, options: List[str], prompt_style: str = "standard") -> str:
        """
        Create evaluation prompt for argument pair.
        
        Args:
            options: List of [option_a, option_b] arguments
            prompt_style: Prompt variation ("standard", "enhanced")
        """        
        if prompt_style == "enhanced":
            return f"""Compare these two logical arguments. One follows valid reasoning patterns while the other contains a logical fallacy.

ARGUMENT A:
{options[0]}

ARGUMENT B:
{options[1]}

Which argument is logically valid? Answer A or B:"""
        
        else:  # standard
            return f"""Which of these arguments is logically correct?

A: {options[0]}

B: {options[1]}

Answer: """
    
    def evaluate_dataset(self, 
                        jsonl_file: Path, 
                        prompt_style: str = "standard") -> Tuple[Optional[ModelStats], List[EvaluationResult]]:
        """Evaluate a single dataset file."""
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
        
        results = []
        by_rule_stats = {}
        unclear_count = 0
        
        # Process questions (subclasses can override for batch processing)
        for q in questions:
            result = self._evaluate_single_question(q, prompt_style)
            results.append(result)
            
            # Track by-rule statistics
            good_type = q.get('good_argument_type', 'Unknown')
            if good_type not in by_rule_stats:
                by_rule_stats[good_type] = {'correct': 0, 'total': 0}
            
            by_rule_stats[good_type]['total'] += 1
            if result.is_correct:
                by_rule_stats[good_type]['correct'] += 1
            
            if result.model_answer in ["UNCLEAR", "ERROR"]:
                unclear_count += 1
        
        # Calculate statistics
        correct_total = sum(1 for r in results if r.is_correct)
        accuracy = correct_total / len(results) * 100
        avg_response_time = sum(r.response_time for r in results if r.response_time > 0) / len(results)
        
        # Convert by-rule stats
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
    
    def _evaluate_single_question(self, question: Dict[str, Any], prompt_style: str) -> EvaluationResult:
        """Evaluate a single question."""
        options = question['test_options']['randomized']
        correct_idx = question['correct_answer']['randomized_index']
        correct_answer = 'A' if correct_idx == 0 else 'B'
        
        # Create prompt and query model
        prompt = self.create_prompt(options, prompt_style)
        raw_response, response_time = self.query_model(prompt)
        model_answer, parsing_metadata = self.parse_model_response(raw_response)
        
        # Handle unclear responses
        if model_answer in ["UNCLEAR", "ERROR"]:
            is_correct = False
        else:
            is_correct = model_answer == correct_answer
        
        return EvaluationResult(
            question_id=question['question_id'],
            model_answer=model_answer,
            correct_answer=correct_answer,
            is_correct=is_correct,
            good_argument_type=question.get('good_argument_type', 'Unknown'),
            bad_argument_type=question.get('bad_argument_type', 'Unknown'),
            response_time=response_time,
            raw_response=raw_response[:100],  # Truncate for storage
            parsing_method=parsing_metadata.get("parsing_method")
        )


# Factory pattern removed - use direct imports instead