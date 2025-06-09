#!/usr/bin/env python3
"""
evaluate_example.py

Quick example of how to use the ollama_evaluator module.
"""

from ollama_evaluator import OllamaEvaluator
from pathlib import Path

def quick_test():
    """Test evaluator with a single file."""
    
    # Initialize evaluator
    evaluator = OllamaEvaluator()
    
    # Check connection
    if not evaluator.check_ollama_connection():
        print("❌ Ollama not running. Start with: ollama serve")
        return
    
    # Get available models
    models = evaluator.get_available_models()
    if not models:
        print("❌ No models found. Install one with: ollama pull llama3.1")
        return
    
    print(f"✅ Found models: {models}")
    model = models[0]  # Use first available model
    
    # Find a test file
    test_files = list(Path("../outputs").glob("*/test.jsonl"))
    if not test_files:
        print("❌ No test files found in ../outputs/")
        return
    
    test_file = test_files[0]
    print(f"📄 Testing with: {test_file}")
    
    # Run evaluation
    try:
        stats, results = evaluator.evaluate_dataset(test_file, model)
        
        print(f"\n📊 Results:")
        print(f"   Accuracy: {stats.accuracy:.1f}%")
        print(f"   Questions: {stats.total_questions}")
        print(f"   Unclear responses: {stats.unclear_responses}")
        
        # Show by-rule breakdown
        print(f"\n📋 By logical rule:")
        for rule, (correct, total) in stats.by_rule_accuracy.items():
            rule_acc = correct/total*100 if total > 0 else 0
            print(f"   {rule}: {rule_acc:.1f}% ({correct}/{total})")
        
        # Save results
        output_file = Path("evaluation_results") / f"quick_test_{model}_{test_file.parent.name}.csv"
        evaluator.save_detailed_results(results, output_file)
        print(f"\n💾 Detailed results saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    quick_test()