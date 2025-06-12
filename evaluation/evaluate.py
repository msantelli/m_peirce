#!/usr/bin/env python3
"""
evaluate.py

Streamlined evaluation CLI for testing language models on logical reasoning datasets.
Supports HuggingFace, OpenAI, and Ollama models through unified interface.
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

from base_evaluator import EvaluationConfig, ModelStats, EvaluationResult
from evaluator import create_evaluator


def find_datasets(outputs_dir: Path, datasets: Optional[List[str]] = None, 
                 splits: List[str] = ["test"]) -> List[Path]:
    """Find dataset files to evaluate."""
    jsonl_files = []
    
    if datasets:
        # Look for specific datasets
        for dataset in datasets:
            for split in splits:
                jsonl_file = outputs_dir / dataset / f"{split}.jsonl"
                if jsonl_file.exists():
                    jsonl_files.append(jsonl_file)
                else:
                    print(f"⚠ Dataset file not found: {jsonl_file}")
    else:
        # Find all datasets
        for subdir in outputs_dir.iterdir():
            if subdir.is_dir():
                for split in splits:
                    jsonl_file = subdir / f"{split}.jsonl"
                    if jsonl_file.exists():
                        jsonl_files.append(jsonl_file)
    
    return sorted(jsonl_files)


def save_results(results: List[EvaluationResult], output_file: Path):
    """Save detailed results to CSV."""
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'question_id', 'model_answer', 'correct_answer', 'is_correct',
            'good_argument_type', 'bad_argument_type', 'response_time',
            'raw_response', 'parsing_method'
        ])
        
        for result in results:
            writer.writerow([
                result.question_id,
                result.model_answer,
                result.correct_answer,
                result.is_correct,
                result.good_argument_type,
                result.bad_argument_type,
                f"{result.response_time:.3f}",
                result.raw_response.replace('\n', ' ')[:200],  # Truncate and clean
                result.parsing_method or ''
            ])


def save_summary(all_stats: List[ModelStats], output_dir: Path):
    """Save evaluation summary."""
    summary_file = output_dir / "evaluation_summary.md"
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("# Evaluation Summary\n\n")
        f.write(f"**Evaluation Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Overall results table
        f.write("## Overall Results\n\n")
        f.write("| Model | Dataset | Questions | Correct | Accuracy | Avg Time | Unclear |\n")
        f.write("|-------|---------|-----------|---------|----------|----------|---------|\n")
        
        for stats in all_stats:
            f.write(f"| {stats.model_name} | {stats.dataset_name} | "
                   f"{stats.total_questions} | {stats.correct_answers} | "
                   f"{stats.accuracy:.1%} | {stats.avg_response_time:.2f}s | "
                   f"{stats.unclear_responses} |\n")
        
        # Per-rule breakdown
        if all_stats:
            f.write("\n## Per-Rule Accuracy\n\n")
            for stats in all_stats:
                if stats.by_rule_accuracy:
                    f.write(f"### {stats.model_name} - {stats.dataset_name}\n\n")
                    f.write("| Rule Comparison | Correct | Total | Accuracy |\n")
                    f.write("|-----------------|---------|-------|----------|\n")
                    
                    for rule, (correct, total) in stats.by_rule_accuracy.items():
                        accuracy = correct / total if total > 0 else 0
                        f.write(f"| {rule} | {correct} | {total} | {accuracy:.1%} |\n")
                    f.write("\n")


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate language models on logical reasoning datasets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # HuggingFace model
  python evaluate.py --type huggingface --models gpt2
  
  # OpenAI API
  python evaluate.py --type openai --models gpt-3.5-turbo --api-key YOUR_KEY
  
  # Ollama local model
  python evaluate.py --type ollama --models llama3.1
  
  # Multiple models on specific datasets
  python evaluate.py --type ollama --models llama3.1 qwen2.5:7b --datasets balanced_eval_1 --splits test validation
        """
    )
    
    # Model configuration
    parser.add_argument('--type', choices=['huggingface', 'openai', 'ollama'], 
                       required=True, help='Model provider type')
    parser.add_argument('--models', nargs='+', required=True,
                       help='Model names to evaluate')
    
    # Evaluation options
    parser.add_argument('--datasets', nargs='+',
                       help='Specific datasets to evaluate (default: all)')
    parser.add_argument('--splits', nargs='+', default=['test'],
                       help='Dataset splits to evaluate (default: test)')
    parser.add_argument('--prompt-style', choices=['standard', 'enhanced'], 
                       default='standard', help='Prompting style')
    
    # Provider-specific options
    parser.add_argument('--api-key', help='OpenAI API key')
    parser.add_argument('--api-base', default='https://api.openai.com/v1',
                       help='OpenAI API base URL')
    parser.add_argument('--ollama-url', default='http://localhost:11434',
                       help='Ollama API URL')
    parser.add_argument('--device', help='Device for HuggingFace models (auto/cuda/cpu)')
    
    # Performance options
    parser.add_argument('--timeout', type=int, default=60,
                       help='Query timeout in seconds')
    parser.add_argument('--max-tokens', type=int, default=10,
                       help='Maximum tokens in response')
    parser.add_argument('--temperature', type=float, default=0.1,
                       help='Sampling temperature')
    
    # I/O options
    parser.add_argument('--outputs-dir', type=Path, default=Path('../outputs'),
                       help='Directory containing datasets')
    parser.add_argument('--results-dir', type=Path, default=Path('evaluation_results'),
                       help='Directory to save results')
    
    args = parser.parse_args()
    
    # Validate provider-specific requirements
    if args.type == 'openai' and not args.api_key:
        parser.error("--api-key is required for OpenAI provider")
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = args.results_dir / f"evaluation_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🔍 LLM Logical Reasoning Evaluation")
    print(f"{'='*50}")
    print(f"Provider: {args.type}")
    print(f"Models: {', '.join(args.models)}")
    print(f"Results: {output_dir}")
    print()
    
    # Find datasets
    jsonl_files = find_datasets(args.outputs_dir, args.datasets, args.splits)
    
    if not jsonl_files:
        print(f"❌ No dataset files found in {args.outputs_dir}")
        return 1
    
    print(f"📊 Found {len(jsonl_files)} dataset files:")
    for f in jsonl_files:
        print(f"  - {f.parent.name}/{f.name}")
    print()
    
    # Create evaluators
    evaluators = []
    for model_name in args.models:
        config = EvaluationConfig(
            model_name=model_name,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
            timeout=args.timeout,
            device=args.device
        )
        
        try:
            evaluator = create_evaluator(
                args.type,
                config,
                api_key=args.api_key,
                api_base=args.api_base,
                ollama_url=args.ollama_url
            )
            evaluators.append((model_name, evaluator))
            print(f"✅ Created evaluator for {model_name}")
            
        except Exception as e:
            print(f"❌ Failed to create evaluator for {model_name}: {e}")
            continue
    
    if not evaluators:
        print("❌ No working evaluators created")
        return 1
    
    print()
    
    # Run evaluations
    all_stats = []
    
    for model_name, evaluator in evaluators:
        print(f"🤖 Evaluating: {model_name}")
        print(f"{'-'*40}")
        
        # Check availability and warm up
        if not evaluator.check_model_availability():
            print(f"⚠ Model {model_name} not available, skipping...")
            continue
        
        if not evaluator.warm_up_model():
            print(f"⚠ Warning: Model warm-up failed, continuing anyway...")
        
        for jsonl_file in jsonl_files:
            dataset_name = f"{jsonl_file.parent.name}_{jsonl_file.stem}"
            print(f"\n📝 Dataset: {dataset_name}")
            
            try:
                # Run evaluation
                stats, results = evaluator.evaluate_dataset(jsonl_file, args.prompt_style)
                
                # Save detailed results
                safe_model_name = model_name.replace('/', '_').replace(':', '_')
                output_file = output_dir / f"{safe_model_name}_{dataset_name}.csv"
                save_results(results, output_file)
                
                # Print quick stats
                print(f"✅ Accuracy: {stats.accuracy:.1%} ({stats.correct_answers}/{stats.total_questions})")
                print(f"   Avg time: {stats.avg_response_time:.2f}s, Unclear: {stats.unclear_responses}")
                
                all_stats.append(stats)
                
            except Exception as e:
                print(f"❌ Failed to evaluate {dataset_name}: {e}")
                continue
        
        print()
    
    # Save summary
    if all_stats:
        save_summary(all_stats, output_dir)
        print(f"📄 Summary saved to: {output_dir / 'evaluation_summary.md'}")
        
        # Print overall results
        print("\n📊 Final Results:")
        for stats in all_stats:
            print(f"  {stats.model_name} on {stats.dataset_name}: "
                  f"{stats.accuracy:.1%} accuracy ({stats.correct_answers}/{stats.total_questions})")
    
    print(f"\n✅ Evaluation complete! Results in: {output_dir}")
    return 0


if __name__ == "__main__":
    exit(main())