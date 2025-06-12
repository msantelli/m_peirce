#!/usr/bin/env python3
"""
base_evaluator.py

Consolidated base classes and shared functionality for model evaluation.
Contains all core data structures and common logic used across different model providers.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import json
import time
import re


@dataclass
class EvaluationConfig:
    """Configuration for model evaluation."""
    model_name: str
    max_tokens: int = 10
    temperature: float = 0.1
    timeout: int = 60
    device: Optional[str] = None  # For HuggingFace models
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
    """Abstract base class for all model evaluators."""
    
    def __init__(self, config: EvaluationConfig):
        self.config = config
        self.model_name = config.model_name
    
    @abstractmethod
    def query_model(self, prompt: str) -> Tuple[str, float]:
        """
        Query the model with a prompt and return response + timing.
        
        Returns:
            Tuple of (response_text, response_time_seconds)
        """
        pass
    
    def check_model_availability(self) -> bool:
        """Check if model is available. Override if needed."""
        return True
    
    def warm_up_model(self) -> bool:
        """Warm up model with test query. Override if needed."""
        try:
            test_prompt = "Answer with just the letter A: A or B?"
            _, _ = self.query_model(test_prompt)
            return True
        except Exception:
            return False
    
    def create_prompt(self, options: List[str], prompt_style: str = "standard") -> str:
        """Create evaluation prompt from argument options."""
        option_a, option_b = options
        
        if prompt_style == "enhanced":
            return f"""Evaluate these two logical arguments and choose the stronger one.

Argument A: {option_a}

Argument B: {option_b}

Which argument is logically stronger? Consider:
1. Logical validity of the reasoning
2. Strength of the connection between premises and conclusion
3. Whether the argument commits any logical fallacies

Answer with just the letter A or B."""

        else:  # standard
            return f"""Which argument is logically stronger?

A: {option_a}

B: {option_b}

Answer: """
    
    def parse_model_answer(self, response: str) -> Tuple[str, str]:
        """
        Parse model response to extract answer choice.
        
        Returns:
            Tuple of (parsed_answer, parsing_method)
        """
        if not response:
            return "UNCLEAR", "empty_response"
        
        response = response.strip().upper()
        
        # Method 1: Direct A or B
        if response in ['A', 'B']:
            return response, "direct"
        
        # Method 2: "Answer: A" or "Answer: B"
        answer_match = re.search(r'ANSWER:\s*([AB])', response)
        if answer_match:
            return answer_match.group(1), "answer_prefix"
        
        # Method 3: First occurrence of A or B
        first_match = re.search(r'\b([AB])\b', response)
        if first_match:
            return first_match.group(1), "first_occurrence"
        
        # Method 4: "Option A" or "Option B"
        option_match = re.search(r'OPTION\s+([AB])', response)
        if option_match:
            return option_match.group(1), "option_prefix"
        
        # Method 5: Choice indicators
        if any(phrase in response for phrase in ['CHOICE A', 'CHOOSE A', 'SELECT A']):
            return "A", "choice_indicator"
        if any(phrase in response for phrase in ['CHOICE B', 'CHOOSE B', 'SELECT B']):
            return "B", "choice_indicator"
        
        return "UNCLEAR", "no_match"
    
    def load_dataset(self, jsonl_file: Path) -> List[Dict[str, Any]]:
        """Load questions from JSONL file."""
        questions = []
        try:
            with open(jsonl_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        questions.append(json.loads(line))
        except Exception as e:
            raise RuntimeError(f"Failed to load dataset {jsonl_file}: {e}")
        
        return questions
    
    def evaluate_single_question(self, question: Dict[str, Any], prompt_style: str) -> EvaluationResult:
        """Evaluate a single question."""
        question_id = question.get('question_id', 0)
        options = question.get('options', [])
        correct_answer = question.get('correct_answer', '')
        good_type = question.get('good_argument_type', 'Unknown')
        bad_type = question.get('bad_argument_type', 'Unknown')
        
        if len(options) != 2:
            return EvaluationResult(
                question_id=question_id,
                model_answer="ERROR",
                correct_answer=correct_answer,
                is_correct=False,
                good_argument_type=good_type,
                bad_argument_type=bad_type,
                response_time=0.0,
                raw_response="Invalid question format",
                parsing_method="error"
            )
        
        # Query model
        prompt = self.create_prompt(options, prompt_style)
        try:
            raw_response, response_time = self.query_model(prompt)
            model_answer, parsing_method = self.parse_model_answer(raw_response)
        except Exception as e:
            return EvaluationResult(
                question_id=question_id,
                model_answer="ERROR",
                correct_answer=correct_answer,
                is_correct=False,
                good_argument_type=good_type,
                bad_argument_type=bad_type,
                response_time=0.0,
                raw_response=f"Query failed: {e}",
                parsing_method="error"
            )
        
        is_correct = model_answer == correct_answer
        
        return EvaluationResult(
            question_id=question_id,
            model_answer=model_answer,
            correct_answer=correct_answer,
            is_correct=is_correct,
            good_argument_type=good_type,
            bad_argument_type=bad_type,
            response_time=response_time,
            raw_response=raw_response[:500],  # Truncate for storage
            parsing_method=parsing_method
        )
    
    def evaluate_dataset(self, jsonl_file: Path, prompt_style: str = "standard") -> Tuple[ModelStats, List[EvaluationResult]]:
        """Evaluate entire dataset and return statistics."""
        questions = self.load_dataset(jsonl_file)
        
        if not questions:
            raise RuntimeError(f"No questions found in {jsonl_file}")
        
        results = []
        by_rule_stats = {}
        
        print(f"Evaluating {len(questions)} questions...")
        
        # Import tqdm if available for progress bar
        try:
            from tqdm import tqdm
            questions_iter = tqdm(questions, desc="Evaluating")
        except ImportError:
            questions_iter = questions
            print("Install tqdm for progress bars: pip install tqdm")
        
        for question in questions_iter:
            result = self.evaluate_single_question(question, prompt_style)
            results.append(result)
            
            # Track by-rule statistics
            rule_key = f"{result.good_argument_type} vs {result.bad_argument_type}"
            if rule_key not in by_rule_stats:
                by_rule_stats[rule_key] = [0, 0]  # [correct, total]
            
            by_rule_stats[rule_key][1] += 1  # total
            if result.is_correct:
                by_rule_stats[rule_key][0] += 1  # correct
        
        # Calculate statistics
        correct_count = sum(1 for r in results if r.is_correct)
        unclear_count = sum(1 for r in results if r.model_answer == "UNCLEAR")
        total_time = sum(r.response_time for r in results)
        avg_time = total_time / len(results) if results else 0.0
        
        # Convert by_rule_stats to proper format
        by_rule_accuracy = {
            rule: (correct, total) for rule, (correct, total) in by_rule_stats.items()
        }
        
        dataset_name = jsonl_file.parent.name if jsonl_file.parent.name != "." else jsonl_file.stem
        
        stats = ModelStats(
            model_name=self.model_name,
            dataset_name=dataset_name,
            total_questions=len(results),
            correct_answers=correct_count,
            accuracy=correct_count / len(results) if results else 0.0,
            avg_response_time=avg_time,
            unclear_responses=unclear_count,
            by_rule_accuracy=by_rule_accuracy
        )
        
        return stats, results