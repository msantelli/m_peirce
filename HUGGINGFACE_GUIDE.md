# 🤗 HuggingFace Dataset Upload Guide

This guide walks you through the **streamlined process** for uploading logical reasoning datasets to HuggingFace Hub. Dataset cards are now **automatically generated** during dataset creation.

## 🚀 Quick Start (2 Steps)

### 1. Generate Dataset (includes HuggingFace card automatically)
```bash
# Creates JSONL files + README.md with YAML metadata automatically
python hf_dataset_converter.py data/sentences_english.txt 1000 outputs/my_dataset en
```

### 2. Upload to HuggingFace Hub
```bash
# Install HuggingFace Hub
pip install huggingface_hub

# Login (get token from https://huggingface.co/settings/tokens)
huggingface-cli login

# Upload dataset
python upload_to_huggingface.py outputs/my_dataset "logical-reasoning-en" your_username
```

## 📋 What You Need

1. **HuggingFace Account**: [huggingface.co](https://huggingface.co)
2. **API Token**: [Settings > Access Tokens](https://huggingface.co/settings/tokens)
3. **Dataset**: Generated with integrated card creation (automatic)

## 🔧 YAML Metadata (Auto-Generated)

The system automatically creates YAML frontmatter in `README.md` that describes your dataset:

```yaml
dataset_info:
  features:           # Auto-detected from your JSONL
    - name: question_id
      dtype: int64
    - name: test_options
      dtype:
        randomized: sequence: string
  splits:            # Auto-calculated from files
    - name: train
      num_examples: 800
      num_bytes: 792361
language:            # Auto-detected from data
  - en
task_categories:     # Auto-assigned
  - question-answering
tags:               # Auto-generated
  - logical-reasoning
  - argument-evaluation
```

### Why YAML Matters

- **Discoverability**: Helps users find your dataset
- **Integration**: Allows automatic loading with `load_dataset()`
- **Documentation**: Describes structure and usage
- **Validation**: Ensures data format consistency

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

## 🔄 Streamlined Workflow

### Complete Pipeline (2 Steps)
```bash
# 1. Generate dataset (creates JSONL + HuggingFace card automatically)
python hf_dataset_converter.py data/sentences_english.txt 1000 outputs/my_dataset en

# 2. Upload to HuggingFace (ready immediately)
python upload_to_huggingface.py outputs/my_dataset "logical-reasoning-en" your_username
```

### What Gets Created Automatically:
- `train.jsonl`, `validation.jsonl`, `test.jsonl` - Data files
- `train.txt`, `validation.txt`, `test.txt` - Human-readable versions
- `README.md` - **With YAML frontmatter + documentation**
- `dataset_info.json` - Metadata summary

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

1. **One-Step Generation**: Dataset + HuggingFace card created together
2. **Automatic Metadata**: YAML frontmatter describes dataset structure automatically
3. **Instant Upload Ready**: No manual card creation needed
4. **Easy Discovery**: Users find datasets through HuggingFace search
5. **Seamless Integration**: `load_dataset()` works instantly with your data
6. **Rich Documentation**: Examples and usage generated automatically
7. **Research Ready**: Share with the research community in 2 simple steps

The integrated workflow makes your logical reasoning datasets instantly HuggingFace-ready! 🌍