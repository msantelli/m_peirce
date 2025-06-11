#!/usr/bin/env python3
"""
unified_evaluator.py

Unified evaluation script supporting multiple model types:
- Ollama (local models via Ollama API)
- HuggingFace (local/remote models via transformers)
- OpenAI (OpenAI API, vLLM, and other OpenAI-compatible endpoints)
"""

import argparse
import csv
import json
import math
import statistics
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Import evaluators
from base_evaluator import EvaluationConfig, ModelStats, EvaluationResult


def find_jsonl_files(outputs_dir: Path, datasets: Optional[List[str]] = None, 
                     splits: List[str] = ["test"]) -> List[Path]:
    """Find all .jsonl files in outputs directory."""
    jsonl_files = []
    
    if datasets:
        # Look for specific datasets
        for dataset in datasets:
            for split in splits:
                jsonl_file = outputs_dir / dataset / f"{split}.jsonl"
                if jsonl_file.exists():
                    jsonl_files.append(jsonl_file)
    else:
        # Find all datasets
        for subdir in outputs_dir.iterdir():
            if subdir.is_dir():
                for split in splits:
                    jsonl_file = subdir / f"{split}.jsonl"
                    if jsonl_file.exists():
                        jsonl_files.append(jsonl_file)
    
    return sorted(jsonl_files)


def save_detailed_results(results: List[EvaluationResult], output_file: Path):
    """Save detailed results to CSV."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'question_id', 'model_answer', 'correct_answer', 'is_correct',
            'good_argument_type', 'bad_argument_type', 'response_time', 'raw_response',
            'parsing_method'
        ])
        
        for r in results:
            writer.writerow([
                r.question_id, r.model_answer, r.correct_answer, r.is_correct,
                r.good_argument_type, r.bad_argument_type, 
                f"{r.response_time:.2f}", r.raw_response,
                r.parsing_method or ""
            ])


def save_summary_stats(all_stats: List[ModelStats], output_file: Path):
    """Save summary statistics."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# LLM Evaluation Results Summary\n\n")
        f.write(f"**Evaluation Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Evaluator**: unified_evaluator.py\n")
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


def main():
    """Main evaluation script."""
    parser = argparse.ArgumentParser(description="Unified LLM evaluator for logical reasoning datasets")
    
    # Model type selection
    parser.add_argument("--type", choices=["ollama", "huggingface", "openai", "vllm"],
                       required=True, help="Type of model evaluator to use")
    
    # Common arguments
    parser.add_argument("--models", nargs="+", 
                       help="Models to evaluate (if not specified, uses available models)")
    parser.add_argument("--outputs-dir", type=Path, default="../outputs", 
                       help="Directory containing output datasets")
    parser.add_argument("--datasets", nargs="+",
                       help="Specific datasets to evaluate")
    parser.add_argument("--splits", nargs="+", default=["test"],
                       choices=["train", "validation", "test"],
                       help="Dataset splits to evaluate")
    parser.add_argument("--results-dir", type=Path, default="evaluation_results",
                       help="Output directory for results")
    parser.add_argument("--prompt-style", choices=["standard", "enhanced"],
                       default="standard", help="Prompt style to use")
    
    # Model configuration
    parser.add_argument("--max-tokens", type=int, default=10,
                       help="Maximum tokens to generate")
    parser.add_argument("--temperature", type=float, default=0.1,
                       help="Temperature for generation")
    parser.add_argument("--timeout", type=int, default=60,
                       help="Request timeout in seconds")
    
    # Type-specific arguments
    parser.add_argument("--ollama-url", default="http://localhost:11434",
                       help="Ollama API URL")
    parser.add_argument("--device", help="Device for HuggingFace models (cuda/cpu)")
    parser.add_argument("--trust-remote-code", action="store_true",
                       help="Trust remote code for HuggingFace models")
    parser.add_argument("--api-base", default="http://localhost:8000/v1",
                       help="API base URL for OpenAI-compatible endpoints")
    parser.add_argument("--api-key", default="dummy-key",
                       help="API key for OpenAI-compatible endpoints")
    parser.add_argument("--vllm-host", default="localhost",
                       help="vLLM host")
    parser.add_argument("--vllm-port", type=int, default=8000,
                       help="vLLM port")
    
    args = parser.parse_args()
    
    # Create timestamped results directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamped_results_dir = args.results_dir / f"evaluation_{timestamp}"
    
    # Import and initialize evaluators based on type
    if args.type == "ollama":
        from ollama_evaluator import OllamaEvaluator
        # Adapt to new interface
        models_to_test = args.models or []
        if not models_to_test:
            # Get available models from Ollama
            import requests
            try:
                response = requests.get(f"{args.ollama_url}/api/tags", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    models_to_test = [model['name'] for model in data.get('models', [])]
            except:
                print(f"Could not connect to Ollama at {args.ollama_url}")
                return
        
        print(f"Testing Ollama models: {models_to_test}")
        evaluators = []
        for model in models_to_test:
            evaluator = OllamaEvaluator(args.ollama_url, args.timeout)
            evaluators.append((model, evaluator))
            
    else:
        # Use unified evaluator system
        if args.type == "huggingface":
            from huggingface_evaluator import HuggingFaceEvaluator
        elif args.type in ["openai", "vllm"]:
            from openai_evaluator import OpenAIEvaluator, vLLMEvaluator
        
        models_to_test = args.models
        if not models_to_test:
            print("Please specify --models for this evaluator type")
            return
        
        evaluators = []
        for model in models_to_test:
            config = EvaluationConfig(
                model_name=model,
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                timeout=args.timeout,
                device=args.device,
                trust_remote_code=args.trust_remote_code
            )
            
            if args.type == "vllm":
                evaluator = vLLMEvaluator(config, args.vllm_host, args.vllm_port)
            elif args.type == "openai":
                evaluator = OpenAIEvaluator(config, args.api_base, args.api_key)
            else:  # huggingface
                evaluator = HuggingFaceEvaluator(config)
            
            evaluators.append((model, evaluator))
    
    # Find datasets
    jsonl_files = find_jsonl_files(args.outputs_dir, args.datasets, args.splits)
    
    if not jsonl_files:
        print(f"No .jsonl files found in {args.outputs_dir}")
        return
    
    print(f"Found {len(jsonl_files)} dataset files")
    
    # Run evaluations
    all_stats = []
    
    for model_name, evaluator in evaluators:
        print(f"\n{'='*50}")
        print(f"Evaluating model: {model_name}")
        print(f"{'='*50}")
        
        # Check availability and warm up
        if hasattr(evaluator, 'check_model_availability') and not evaluator.check_model_availability():
            print(f"⚠ Model {model_name} not available, skipping...")
            continue
        
        if hasattr(evaluator, 'warm_up_model'):
            if not evaluator.warm_up_model():
                print(f"⚠ Warning: Model warm-up failed for {model_name}, continuing anyway...")
        
        for jsonl_file in jsonl_files:
            print(f"\nProcessing: {jsonl_file}")
            
            try:
                if args.type == "ollama":
                    # Use original Ollama evaluator interface
                    stats, results = evaluator.evaluate_dataset(
                        jsonl_file, model_name, args.prompt_style
                    )
                else:
                    # Use new unified interface
                    stats, results = evaluator.evaluate_dataset(
                        jsonl_file, args.prompt_style
                    )
                
                if stats:
                    all_stats.append(stats)
                    
                    # Save detailed results
                    result_file = timestamped_results_dir / f"{model_name}_{jsonl_file.parent.name}_{jsonl_file.stem}.csv"
                    save_detailed_results(results, result_file)
                    
                    print(f"✓ Accuracy: {stats.accuracy:.1f}% ({stats.correct_answers}/{stats.total_questions})")
                    print(f"  Results saved to: {result_file}")
                    
            except Exception as e:
                print(f"✗ Error evaluating {jsonl_file} with {model_name}: {e}")
    
    # Save summary
    if all_stats:
        summary_file = timestamped_results_dir / "evaluation_summary.md"
        save_summary_stats(all_stats, summary_file)
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