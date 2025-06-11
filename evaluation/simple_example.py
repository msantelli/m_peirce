#!/usr/bin/env python3
"""
simple_example.py

Basic example showing how to evaluate models on logical reasoning datasets.
"""

import subprocess
import sys
from pathlib import Path

def run_example():
    """Run a simple evaluation example."""
    
    print("🔍 LLM Evaluation Example")
    print("=" * 50)
    
    # Check if outputs directory exists
    outputs_dir = Path("../outputs")
    if not outputs_dir.exists():
        print("⚠ No datasets found in ../outputs")
        print("Please generate datasets first using the main m-peirce-a generator.")
        return
    
    # Find available datasets
    datasets = [d.name for d in outputs_dir.iterdir() if d.is_dir() and (d / "test.jsonl").exists()]
    
    if not datasets:
        print("⚠ No test.jsonl files found in datasets")
        return
    
    print(f"📊 Found {len(datasets)} datasets: {', '.join(datasets[:3])}")
    if len(datasets) > 3:
        print(f"    ... and {len(datasets) - 3} more")
    
    # Example configurations to try
    examples = [
        {
            "name": "HuggingFace GPT-2 (CPU)",
            "cmd": ["python", "unified_evaluator.py", "--type", "huggingface", "--models", "gpt2", "--datasets", datasets[0]]
        },
        {
            "name": "Ollama (if available)",
            "cmd": ["python", "unified_evaluator.py", "--type", "ollama", "--models", "llama3.1", "--datasets", datasets[0]]
        }
    ]
    
    print("\n🚀 Example Commands:")
    print("-" * 30)
    
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['name']}:")
        print(f"   {' '.join(example['cmd'])}")
        print()
    
    # Try to run a simple example
    print("🧪 Running simple test with GPT-2...")
    try:
        result = subprocess.run([
            "python", "unified_evaluator.py", 
            "--type", "huggingface", 
            "--models", "gpt2",
            "--datasets", datasets[0],
            "--prompt-style", "standard"
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ Evaluation completed successfully!")
            print("📁 Check evaluation_results/ directory for detailed results")
        else:
            print("❌ Evaluation failed:")
            print(result.stderr[:200])
            
    except subprocess.TimeoutExpired:
        print("⏱ Evaluation timed out (this is normal for first-time model loading)")
    except FileNotFoundError:
        print("⚠ unified_evaluator.py not found. Run from evaluation/ directory.")
    except Exception as e:
        print(f"⚠ Could not run example: {e}")
    
    print("\n📖 Next steps:")
    print("1. Install model-specific requirements (see README.md)")
    print("2. Start required services (ollama serve for Ollama)")
    print("3. Run unified_evaluator.py with your preferred model type")
    print("4. Check evaluation_results/ for detailed analysis")

if __name__ == "__main__":
    run_example()