#!/usr/bin/env python3
"""
ollama_evaluator.py

Enhanced LLM evaluation module for logical reasoning datasets.
Evaluates models via Ollama API on generated argument pairs.
"""

import json
import requests
import csv
import time
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from collections import defaultdict
import statistics
import math

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    print("Install tqdm for progress bars: pip install tqdm")


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


class OllamaEvaluator:
    """Enhanced LLM evaluator using Ollama API."""
    
    def __init__(self, 
                 ollama_url: str = "http://localhost:11434",
                 timeout: int = 60,
                 max_retries: int = 3):
        """
        Initialize evaluator.
        
        Args:
            ollama_url: Ollama API endpoint
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts for failed requests
        """
        self.ollama_url = ollama_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        
    def check_ollama_connection(self) -> bool:
        """Check if Ollama is running and accessible."""
        try:
            response = self.session.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def get_available_models(self) -> List[str]:
        """Get list of available models from Ollama."""
        try:
            response = self.session.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
        except requests.RequestException:
            pass
        return []
    
    def warm_up_model(self, model_name: str) -> bool:
        """Warm up model by sending a simple test request."""
        print(f"Warming up model {model_name}...")
        test_prompt = "Answer with just the letter A: A or B?"
        
        try:
            response, _ = self.query_model(test_prompt, model_name)
            if response and response != "ERROR":
                print(f"✓ Model {model_name} warmed up successfully")
                return True
        except Exception as e:
            print(f"✗ Model warm-up failed: {e}")
        
        return False
    
    def query_model(self, prompt: str, model_name: str) -> Tuple[str, float]:
        """
        Query Ollama model with retries.
        
        Returns:
            Tuple of (response_text, response_time_seconds)
        """
        for attempt in range(self.max_retries):
            try:
                start_time = time.time()
                
                response = self.session.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        'model': model_name,
                        'prompt': prompt,
                        'stream': False,
                        'options': {
                            'temperature': 0.1,  # Low temperature for consistency
                            'top_p': 0.9,
                            'max_tokens': 10  # We only need A or B
                        }
                    },
                    timeout=self.timeout
                )
                
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get('response', ''), response_time
                else:
                    print(f"HTTP {response.status_code} on attempt {attempt + 1}")
                    
            except requests.RequestException as e:
                if "timeout" in str(e).lower():
                    print(f"Timeout on attempt {attempt + 1}/{self.max_retries} (consider increasing --timeout)")
                else:
                    print(f"Request failed on attempt {attempt + 1}/{self.max_retries}: {e}")
                
                if attempt < self.max_retries - 1:
                    delay = min(2 ** attempt, 10)  # Exponential backoff, max 10s
                    print(f"Retrying in {delay}s...")
                    time.sleep(delay)
        
        return "ERROR", 0.0
    
    def parse_model_response(self, response: str) -> str:
        """
        Parse model response to extract A or B.
        
        Handles various response formats:
        - "A" or "B" 
        - "The answer is A"
        - "I choose option B"
        - "A: This argument is valid"
        """
        if not response or response == "ERROR":
            return "ERROR"
            
        response = response.strip().upper()
        
        # Direct single letter
        if response in ['A', 'B']:
            return response
            
        # Response starts with A or B
        if response.startswith('A'):
            return 'A'
        elif response.startswith('B'):
            return 'B'
            
        # Look for patterns
        if 'OPTION A' in response or 'CHOOSE A' in response:
            return 'A'
        elif 'OPTION B' in response or 'CHOOSE B' in response:
            return 'B'
            
        # Count occurrences (more robust)
        a_count = response.count('A')
        b_count = response.count('B')
        
        if a_count > b_count and b_count == 0:
            return 'A'
        elif b_count > a_count and a_count == 0:
            return 'B'
        elif a_count == 1 and b_count == 0:
            return 'A'
        elif b_count == 1 and a_count == 0:
            return 'B'
            
        return "UNCLEAR"
    
    def create_prompt(self, options: List[str], prompt_style: str = "standard") -> str:
        """
        Create evaluation prompt for argument pair.
        
        Args:
            options: List of [option_a, option_b] arguments
            prompt_style: Prompt variation ("standard", "formal", "instructional", "enhanced", "analytical")
        """
        if prompt_style == "formal":
            return f"""You are evaluating logical arguments. Which of these arguments follows valid logical reasoning?

Argument A: {options[0]}

Argument B: {options[1]}

Answer with only the letter (A or B):"""
        
        elif prompt_style == "instructional":
            return f"""Determine which argument is logically valid. A valid argument is one where the conclusion follows necessarily from the premises.

A: {options[0]}

B: {options[1]}

Which argument is logically valid? Answer A or B:"""
        
        elif prompt_style == "enhanced":
            return f"""Compare these two logical arguments. One follows valid reasoning patterns while the other contains a logical fallacy.

ARGUMENT A:
{options[0]}

ARGUMENT B:
{options[1]}

Task: Identify which argument is logically valid by checking if the conclusion necessarily follows from the premises. Look for proper logical structure and avoid common fallacies.

Which argument is logically sound? Answer A or B:"""
        
        elif prompt_style == "analytical":
            return f"""You are analyzing logical arguments for validity. A valid argument has a conclusion that follows necessarily from its premises.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARGUMENT A:
{options[0]}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARGUMENT B:
{options[1]}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Instructions:
1. Examine each argument's logical structure
2. Check if conclusions follow necessarily from premises
3. Identify any logical fallacies or invalid inferences
4. Select the argument with valid logical reasoning

Which argument is logically valid?
Answer: """
        
        else:  # standard
            return f"""Which of these arguments is logically correct?

A: {options[0]}

B: {options[1]}

Answer: """
    
    def evaluate_dataset(self, 
                        jsonl_file: Path, 
                        model_name: str,
                        prompt_style: str = "standard") -> Tuple[Optional[ModelStats], List[EvaluationResult]]:
        """Evaluate a single dataset file with a model."""
        
        # Load questions
        questions = []
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questions.append(json.loads(line))
        
        if not questions:
            print(f"No questions found in {jsonl_file}")
            return None, []
        
        print(f"Evaluating {len(questions)} questions with {model_name}...")
        
        results = []
        by_rule_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
        unclear_count = 0
        
        # Progress bar setup
        if HAS_TQDM:
            iterator = tqdm(questions, desc=f"Evaluating {model_name}")
        else:
            iterator = questions
        
        for q in iterator:
            options = q['test_options']['randomized']
            correct_idx = q['correct_answer']['randomized_index']
            correct_answer = 'A' if correct_idx == 0 else 'B'
            
            # Create prompt and query model
            prompt = self.create_prompt(options, prompt_style)
            raw_response, response_time = self.query_model(prompt, model_name)
            model_answer = self.parse_model_response(raw_response)
            
            # Handle unclear responses
            if model_answer in ["UNCLEAR", "ERROR"]:
                unclear_count += 1
                is_correct = False
            else:
                is_correct = model_answer == correct_answer
            
            # Track by-rule statistics
            good_type = q.get('good_argument_type', 'Unknown')
            by_rule_stats[good_type]['total'] += 1
            if is_correct:
                by_rule_stats[good_type]['correct'] += 1
            
            result = EvaluationResult(
                question_id=q['question_id'],
                model_answer=model_answer,
                correct_answer=correct_answer,
                is_correct=is_correct,
                good_argument_type=good_type,
                bad_argument_type=q.get('bad_argument_type', 'Unknown'),
                response_time=response_time,
                raw_response=raw_response[:100]  # Truncate for storage
            )
            results.append(result)
            
            # Brief delay to avoid overwhelming Ollama
            time.sleep(0.1)
        
        # Calculate statistics
        correct_total = sum(1 for r in results if r.is_correct)
        accuracy = correct_total / len(results) * 100
        avg_response_time = statistics.mean(r.response_time for r in results if r.response_time > 0)
        
        # Convert by-rule stats
        by_rule_accuracy = {}
        for rule, stats in by_rule_stats.items():
            by_rule_accuracy[rule] = (stats['correct'], stats['total'])
        
        model_stats = ModelStats(
            model_name=model_name,
            dataset_name=jsonl_file.stem,
            total_questions=len(results),
            correct_answers=correct_total,
            accuracy=accuracy,
            avg_response_time=avg_response_time,
            unclear_responses=unclear_count,
            by_rule_accuracy=by_rule_accuracy
        )
        
        return model_stats, results
    
    def save_detailed_results(self, 
                            results: List[EvaluationResult], 
                            output_file: Path):
        """Save detailed results to CSV."""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'question_id', 'model_answer', 'correct_answer', 'is_correct',
                'good_argument_type', 'bad_argument_type', 'response_time', 'raw_response'
            ])
            
            for r in results:
                writer.writerow([
                    r.question_id, r.model_answer, r.correct_answer, r.is_correct,
                    r.good_argument_type, r.bad_argument_type, 
                    f"{r.response_time:.2f}", r.raw_response
                ])
    
    def save_summary_stats(self, 
                         all_stats: List[ModelStats], 
                         output_file: Path):
        """Save summary statistics."""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        from datetime import datetime
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# LLM Evaluation Results Summary\n\n")
            f.write(f"**Evaluation Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Evaluator**: ollama_evaluator.py\n")
            f.write(f"**Total Evaluations**: {len(all_stats)}\n\n")
            
            for stats in all_stats:
                f.write(f"## {stats.model_name} - {stats.dataset_name}\n\n")
                f.write(f"**Overall Accuracy**: {stats.accuracy:.1f}% ({stats.correct_answers}/{stats.total_questions})\n")
                f.write(f"**Average Response Time**: {stats.avg_response_time:.2f}s\n")
                f.write(f"**Unclear Responses**: {stats.unclear_responses}\n\n")
                
                f.write("**Accuracy by Logical Rule**:\n")
                for rule, (correct, total) in stats.by_rule_accuracy.items():
                    rule_accuracy = correct / total * 100 if total > 0 else 0
                    f.write(f"- {rule}: {rule_accuracy:.1f}% ({correct}/{total})\n")
                f.write("\n")
                
                # Calculate confidence interval (95%)
                n = stats.total_questions
                p = stats.accuracy / 100
                if n > 0:
                    margin = 1.96 * math.sqrt(p * (1 - p) / n)
                    ci_lower = max(0, (p - margin) * 100)
                    ci_upper = min(100, (p + margin) * 100)
                    f.write(f"**95% Confidence Interval**: [{ci_lower:.1f}%, {ci_upper:.1f}%]\n\n")
                
                f.write("---\n\n")


def find_jsonl_files(outputs_dir: Path) -> List[Path]:
    """Find all .jsonl files in outputs directory."""
    jsonl_files = []
    for subdir in outputs_dir.iterdir():
        if subdir.is_dir():
            for split in ['test.jsonl', 'validation.jsonl', 'train.jsonl']:
                jsonl_file = subdir / split
                if jsonl_file.exists():
                    jsonl_files.append(jsonl_file)
    return sorted(jsonl_files)


def main():
    """Main evaluation script."""
    parser = argparse.ArgumentParser(description="Evaluate LLMs on logical reasoning datasets")
    parser.add_argument("--outputs-dir", type=Path, default="../outputs", 
                       help="Directory containing output datasets")
    parser.add_argument("--models", nargs="+", 
                       help="Models to evaluate (if not specified, uses all available)")
    parser.add_argument("--datasets", nargs="+",
                       help="Specific datasets to evaluate (e.g., english_new_8-6-8)")
    parser.add_argument("--splits", nargs="+", default=["test"],
                       choices=["train", "validation", "test"],
                       help="Dataset splits to evaluate")
    parser.add_argument("--results-dir", type=Path, default="evaluation_results",
                       help="Output directory for results")
    parser.add_argument("--prompt-style", choices=["standard", "formal", "instructional", "enhanced", "analytical"],
                       default="standard", help="Prompt style to use")
    parser.add_argument("--ollama-url", default="http://localhost:11434",
                       help="Ollama API URL")
    parser.add_argument("--timeout", type=int, default=60,
                       help="Request timeout in seconds (default: 60)")
    parser.add_argument("--max-retries", type=int, default=3,
                       help="Maximum retry attempts (default: 3)")
    
    args = parser.parse_args()
    
    # Create timestamped results directory
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamped_results_dir = args.results_dir / f"evaluation_{timestamp}"
    
    # Initialize evaluator
    evaluator = OllamaEvaluator(ollama_url=args.ollama_url, timeout=args.timeout, max_retries=args.max_retries)
    
    # Check Ollama connection
    if not evaluator.check_ollama_connection():
        print(f"Error: Cannot connect to Ollama at {args.ollama_url}")
        print("Make sure Ollama is running: ollama serve")
        return
    
    # Get available models
    available_models = evaluator.get_available_models()
    if not available_models:
        print("No models found in Ollama. Install a model first:")
        print("ollama pull llama3.1")
        return
    
    models_to_test = args.models if args.models else available_models
    print(f"Available models: {available_models}")
    print(f"Testing models: {models_to_test}")
    
    # Find datasets
    if args.datasets:
        jsonl_files = []
        for dataset in args.datasets:
            for split in args.splits:
                file_path = args.outputs_dir / dataset / f"{split}.jsonl"
                if file_path.exists():
                    jsonl_files.append(file_path)
    else:
        all_files = find_jsonl_files(args.outputs_dir)
        jsonl_files = [f for f in all_files if f.stem in args.splits]
    
    if not jsonl_files:
        print(f"No .jsonl files found in {args.outputs_dir}")
        return
    
    print(f"Found {len(jsonl_files)} dataset files")
    
    # Run evaluations
    all_stats = []
    
    for model_name in models_to_test:
        print(f"\n{'='*50}")
        print(f"Evaluating model: {model_name}")
        print(f"{'='*50}")
        
        # Warm up model before evaluation
        if not evaluator.warm_up_model(model_name):
            print(f"⚠ Warning: Model warm-up failed, continuing anyway...")
        
        for jsonl_file in jsonl_files:
            print(f"\nProcessing: {jsonl_file}")
            
            try:
                stats, results = evaluator.evaluate_dataset(
                    jsonl_file, model_name, args.prompt_style
                )
                
                if stats:
                    all_stats.append(stats)
                    
                    # Save detailed results
                    result_file = timestamped_results_dir / f"{model_name}_{jsonl_file.parent.name}_{jsonl_file.stem}.csv"
                    evaluator.save_detailed_results(results, result_file)
                    
                    print(f"✓ Accuracy: {stats.accuracy:.1f}% ({stats.correct_answers}/{stats.total_questions})")
                    print(f"  Results saved to: {result_file}")
                    
            except Exception as e:
                print(f"✗ Error evaluating {jsonl_file}: {e}")
    
    # Save summary
    if all_stats:
        summary_file = timestamped_results_dir / "evaluation_summary.md"
        evaluator.save_summary_stats(all_stats, summary_file)
        print(f"\n📊 Summary saved to: {summary_file}")
        
        # Print quick summary
        print(f"\n{'='*60}")
        print("EVALUATION SUMMARY")
        print(f"{'='*60}")
        for stats in all_stats:
            print(f"{stats.model_name:15} | {stats.dataset_name:20} | {stats.accuracy:5.1f}% | {stats.unclear_responses:3} unclear")
    
    print("\n🎉 Evaluation complete!")


if __name__ == "__main__":
    main()