# 🤗 HuggingFace Dataset Upload Guide

This guide walks you through uploading your logical reasoning datasets to HuggingFace Hub.

## 📋 What You Need

1. **Generated Dataset**: A complete dataset in `outputs/` directory
2. **HuggingFace Account**: Sign up at [huggingface.co](https://huggingface.co)
3. **API Token**: Get from [Settings > Access Tokens](https://huggingface.co/settings/tokens)

## 🔧 YAML Files Explained

### What are YAML Files?

YAML (Yet Another Markup Language) files contain **metadata** that describes your dataset:

```yaml
dataset_info:
  features:           # What fields your data has
    - name: question_id
      dtype: int64
  splits:            # Train/validation/test splits
    - name: train
      num_examples: 800
language:            # Supported languages
  - en
  - es
task_categories:     # What the dataset is for
  - question-answering
tags:               # Search tags
  - logical-reasoning
  - philosophy
```

### Why YAML Matters

- **Discoverability**: Helps users find your dataset
- **Integration**: Allows automatic loading with `load_dataset()`
- **Documentation**: Describes structure and usage
- **Validation**: Ensures data format consistency

## 🚀 Step-by-Step Upload Process

### 1. Install Dependencies

```bash
pip install huggingface_hub
```

### 2. Generate Dataset Card

```bash
# Create YAML metadata + documentation
python create_hf_dataset_card.py outputs/your_dataset --name "logical-reasoning-en"

# This creates outputs/your_dataset/README.md with:
# - YAML frontmatter (metadata)
# - Dataset description
# - Usage examples
# - Citation information
```

### 3. Login to HuggingFace

```bash
# Option A: Use CLI
huggingface-cli login

# Option B: Set environment variable  
export HF_TOKEN=your_token_here
```

### 4. Upload Dataset

```bash
# Upload to HuggingFace Hub
python upload_to_huggingface.py outputs/your_dataset "logical-reasoning-en" your_username

# For private datasets:
python upload_to_huggingface.py outputs/your_dataset "logical-reasoning-en" your_username --private
```

## 📊 YAML Interaction with Your Datasets

### Your Dataset Structure
```
outputs/balanced_eval_1/
├── train.jsonl         # Training data
├── validation.jsonl    # Validation data  
├── test.jsonl         # Test data
├── train.txt          # Human-readable format
├── validation.txt     # Human-readable format
├── test.txt           # Human-readable format
└── README.md          # Auto-generated YAML + docs
```

### Generated YAML Features

The YAML automatically detects and describes your dataset structure:

```yaml
dataset_info:
  features:
    - name: question_id      # ← Detected from your JSONL
      dtype: int64
    - name: test_options     # ← Your argument pairs
      dtype:
        randomized:
          sequence: string
    - name: correct_answer   # ← Answer indices
      dtype:
        original_index: int64
        randomized_index: int64
    - name: good_argument_type  # ← Logical rule names
      dtype: string
  splits:
    - name: train           # ← Auto-detected splits
      num_examples: 800     # ← Counted from files
      num_bytes: 792361     # ← Calculated file sizes
```

### Language Detection

The system automatically detects languages from your data:

```yaml
language:
  - en    # ← From "language": "en" in JSONL
  - es    # ← From "language": "es" in JSONL
```

## 🎯 HuggingFace Integration Benefits

### 1. Easy Loading
```python
from datasets import load_dataset

# Users can instantly load your dataset
dataset = load_dataset("your_username/logical-reasoning-en")
train_data = dataset['train']
```

### 2. Automatic Parsing
```python
# HuggingFace automatically handles your complex structure
for example in dataset['train']:
    options = example['test_options']['randomized']  # ← Parsed automatically
    correct = example['correct_answer']['randomized_index']
```

### 3. Built-in Features
- **Streaming**: Handle large datasets efficiently
- **Caching**: Automatic caching for faster loading
- **Filtering**: Built-in filtering and selection
- **Metrics**: Integration with evaluation metrics

### 4. Search & Discovery
Your dataset becomes searchable by:
- **Task**: "question-answering", "text-classification"
- **Language**: "en", "es"
- **Tags**: "logical-reasoning", "philosophy", "critical-thinking"
- **Size**: Automatic categorization by dataset size

## 🔄 Workflow Integration

### Complete Pipeline
```bash
# 1. Generate dataset
python hf_dataset_converter.py data/sentences_english.txt 1000 outputs/my_dataset en paired mixed balanced

# 2. Create HuggingFace card
python create_hf_dataset_card.py outputs/my_dataset --name "logical-reasoning-en-balanced"

# 3. Upload to HuggingFace
python upload_to_huggingface.py outputs/my_dataset "logical-reasoning-en-balanced" your_username
```

### User Experience
```python
# Users can then do:
from datasets import load_dataset
from evaluation.evaluator import create_evaluator
from evaluation.base_evaluator import EvaluationConfig

# Load your dataset
dataset = load_dataset("your_username/logical-reasoning-en-balanced")

# Evaluate a model on it
config = EvaluationConfig(model_name="gpt-3.5-turbo")
evaluator = create_evaluator("openai", config, api_key="your_key")

# The dataset format is automatically compatible!
for example in dataset['test']:
    # Your YAML ensures this structure is documented and validated
    options = example['test_options']['randomized']
    correct_idx = example['correct_answer']['randomized_index']
    # ... evaluation logic
```

## 📖 Example YAML Output

Here's what the auto-generated YAML looks like for a Spanish dataset:

```yaml
---
dataset_info:
  features:
    - name: question_id
      dtype: int64
    - name: test_options
      dtype:
        randomized:
          sequence: string
        original:
          sequence: string
        mapping:
          dtype: string
    - name: correct_answer
      dtype:
        original_index: int64
        randomized_index: int64
    - name: good_argument_type
      dtype: string
    - name: bad_argument_type
      dtype: string
    - name: language
      dtype: string
    - name: sentences_used
      sequence: string
    - name: split
      dtype: string
  splits:
    - name: train
      num_bytes: 156789
      num_examples: 80
    - name: validation  
      num_bytes: 19823
      num_examples: 10
    - name: test
      num_bytes: 20145
      num_examples: 10
  download_size: 196757
  dataset_size: 196757
configs:
  - config_name: default
    data_files:
      - split: train
        path: train.jsonl
      - split: validation
        path: validation.jsonl
      - split: test
        path: test.jsonl
    default: true
task_categories:
  - question-answering
  - text-classification
language:
  - es
tags:
  - logical-reasoning
  - argument-evaluation
  - critical-thinking
  - philosophy
  - logic
size_categories:
  - n<1K
license: mit
---
```

## 🎉 Benefits Summary

1. **Automatic Metadata**: YAML files describe your dataset structure automatically
2. **Easy Discovery**: Users find datasets through HuggingFace search
3. **Seamless Integration**: `load_dataset()` works instantly with your data
4. **Documentation**: Rich documentation with examples generated automatically
5. **Validation**: YAML ensures data format consistency
6. **Version Control**: HuggingFace tracks dataset versions
7. **Community**: Share with the research community easily

The YAML files act as a "bridge" between your generated datasets and the HuggingFace ecosystem, making your logical reasoning datasets instantly usable by researchers worldwide! 🌍