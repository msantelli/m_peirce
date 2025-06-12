#!/usr/bin/env python3
"""
create_hf_dataset_card.py

Utility to generate HuggingFace dataset cards (YAML metadata) for logical reasoning datasets.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


def analyze_dataset(dataset_path: Path) -> Dict[str, Any]:
    """Analyze a dataset directory and extract metadata."""
    
    metadata = {
        'splits': {},
        'total_examples': 0,
        'total_bytes': 0,
        'languages': set(),
        'rule_types': set(),
        'features': {}
    }
    
    # Analyze each split
    for split_file in ['train.jsonl', 'validation.jsonl', 'test.jsonl']:
        jsonl_path = dataset_path / split_file
        if not jsonl_path.exists():
            continue
            
        split_name = split_file.replace('.jsonl', '')
        examples = []
        
        # Read examples
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    examples.append(json.loads(line))
        
        # Calculate size
        file_size = jsonl_path.stat().st_size
        
        metadata['splits'][split_name] = {
            'num_examples': len(examples),
            'num_bytes': file_size
        }
        
        metadata['total_examples'] += len(examples)
        metadata['total_bytes'] += file_size
        
        # Analyze features from first example
        if examples and not metadata['features']:
            metadata['features'] = analyze_features(examples[0])
        
        # Collect languages and rule types
        for example in examples:
            if 'language' in example:
                metadata['languages'].add(example['language'])
            if 'good_argument_type' in example:
                metadata['rule_types'].add(example['good_argument_type'])
    
    return metadata


def analyze_features(example: Dict[str, Any]) -> Dict[str, str]:
    """Analyze the features/schema of a dataset example."""
    
    features = {}
    
    for key, value in example.items():
        if isinstance(value, int):
            features[key] = 'int64'
        elif isinstance(value, float):
            features[key] = 'float64'
        elif isinstance(value, str):
            features[key] = 'string'
        elif isinstance(value, bool):
            features[key] = 'bool'
        elif isinstance(value, list):
            if value and isinstance(value[0], str):
                features[key] = 'sequence of string'
            else:
                features[key] = 'sequence'
        elif isinstance(value, dict):
            features[key] = 'nested object'
        else:
            features[key] = 'unknown'
    
    return features


def generate_yaml_frontmatter(metadata: Dict[str, Any], dataset_name: str) -> str:
    """Generate the YAML frontmatter for the dataset card."""
    
    languages = sorted(list(metadata['languages'])) if metadata['languages'] else ['en']
    
    # Determine size category
    total_examples = metadata['total_examples']
    if total_examples < 1000:
        size_category = 'n<1K'
    elif total_examples < 10000:
        size_category = '1K<n<10K'
    elif total_examples < 100000:
        size_category = '10K<n<100K'
    else:
        size_category = 'n>100K'
    
    yaml_content = f"""---
dataset_info:
  features:"""
    
    # Add features
    for feature, dtype in metadata['features'].items():
        if feature == 'test_options':
            yaml_content += f"""
    - name: {feature}
      dtype:
        randomized:
          sequence: string
        original:
          sequence: string
        mapping:
          dtype: string"""
        elif feature == 'correct_answer':
            yaml_content += f"""
    - name: {feature}
      dtype:
        original_index: int64
        randomized_index: int64"""
        elif feature == 'sentences_used':
            yaml_content += f"""
    - name: {feature}
      sequence: string"""
        else:
            yaml_content += f"""
    - name: {feature}
      dtype: {dtype}"""
    
    # Add splits
    yaml_content += """
  splits:"""
    
    for split_name, split_info in metadata['splits'].items():
        yaml_content += f"""
    - name: {split_name}
      num_bytes: {split_info['num_bytes']}
      num_examples: {split_info['num_examples']}"""
    
    yaml_content += f"""
  download_size: {metadata['total_bytes']}
  dataset_size: {metadata['total_bytes']}
configs:
  - config_name: default
    data_files:"""
    
    # Add data files
    for split_name in metadata['splits'].keys():
        yaml_content += f"""
      - split: {split_name}
        path: {split_name}.jsonl"""
    
    yaml_content += f"""
    default: true
task_categories:
  - question-answering
  - text-classification
language:"""
    
    for lang in languages:
        yaml_content += f"""
  - {lang}"""
    
    yaml_content += f"""
tags:
  - logical-reasoning
  - argument-evaluation
  - critical-thinking
  - philosophy
  - logic
size_categories:
  - {size_category}
license: mit
---"""
    
    return yaml_content


def generate_dataset_description(metadata: Dict[str, Any], dataset_name: str) -> str:
    """Generate the markdown description for the dataset card."""
    
    rule_types = sorted(list(metadata['rule_types'])) if metadata['rule_types'] else []
    languages = sorted(list(metadata['languages'])) if metadata['languages'] else ['en']
    
    description = f"""
# {dataset_name.replace('_', ' ').title()} Dataset

## Dataset Summary

This dataset contains pairs of logical arguments for evaluating reasoning capabilities of language models. Each example presents two arguments (one valid, one invalid) and asks models to identify the stronger logical argument.

Generated using the m-peirce-a logical argument generation system.

## Dataset Structure

### Data Instances

```json
{{
  "question_id": 1,
  "test_options": {{
    "randomized": [
      "If it rains, then the ground gets wet. It is raining. Therefore, the ground gets wet.",
      "If it rains, then the ground gets wet. The ground is wet. Therefore, it is raining."
    ],
    "original": [...],
    "mapping": {{"0": 0, "1": 1}}
  }},
  "correct_answer": {{
    "original_index": 0,
    "randomized_index": 0
  }},
  "good_argument_type": "Modus Ponens",
  "bad_argument_type": "Affirming the Consequent",
  "language": "en",
  "sentences_used": ["It rains", "The ground gets wet"],
  "split": "train"
}}
```

### Data Fields

- `question_id`: Unique identifier for each question
- `test_options`: Object containing argument options
  - `randomized`: List of 2 arguments in randomized order (to avoid position bias)
  - `original`: List of 2 arguments in original order (valid argument first)
  - `mapping`: Maps randomized indices back to original indices
- `correct_answer`: Object with correct answer indices
  - `original_index`: Index of correct answer in original order (always 0 = valid argument)
  - `randomized_index`: Index of correct answer in randomized order
- `good_argument_type`: Name of the valid logical rule being demonstrated
- `bad_argument_type`: Name of the corresponding logical fallacy
- `language`: Language code ({', '.join(languages)})
- `sentences_used`: Base sentences used to construct the arguments
- `split`: Dataset split (train/validation/test)

### Data Splits

|       |"""
    
    # Add split table
    for split_name, split_info in metadata['splits'].items():
        description += f" {split_name.title()} |"
    description += "\n|-------|"
    for _ in metadata['splits']:
        description += "--------|"
    description += "\n| Examples |"
    for split_info in metadata['splits'].values():
        description += f" {split_info['num_examples']} |"
    
    description += f"""

**Total Examples:** {metadata['total_examples']}

## Logical Rules Covered

This dataset includes examples for the following logical reasoning patterns:"""
    
    if rule_types:
        for rule in rule_types:
            description += f"\n- {rule}"
    
    description += f"""

## Language Coverage

"""
    
    if 'en' in languages:
        description += "- **English (en)**: Complete coverage of all logical rules\n"
    if 'es' in languages:
        description += "- **Spanish (es)**: Complete coverage of all logical rules\n"
    
    description += f"""
## Usage

### Loading the Dataset

```python
from datasets import load_dataset

# Load the dataset
dataset = load_dataset("your-username/{dataset_name}")

# Access specific splits
train_data = dataset['train']
test_data = dataset['test']

# Example usage
for example in train_data:
    question_id = example['question_id']
    options = example['test_options']['randomized'] 
    correct_idx = example['correct_answer']['randomized_index']
    correct_answer = 'A' if correct_idx == 0 else 'B'
    
    print(f"Question {{question_id}}:")
    print(f"A: {{options[0]}}")
    print(f"B: {{options[1]}}")
    print(f"Correct: {{correct_answer}}")
```

### Evaluation Example

```python
def evaluate_model(model, dataset_split):
    correct = 0
    total = len(dataset_split)
    
    for example in dataset_split:
        options = example['test_options']['randomized']
        correct_idx = example['correct_answer']['randomized_index']
        
        # Create prompt
        prompt = f\"\"\"Which argument is logically stronger?

A: {{options[0]}}

B: {{options[1]}}

Answer: \"\"\"
        
        # Get model prediction
        response = model.generate(prompt)
        predicted = parse_answer(response)  # Extract A or B
        
        if (predicted == 'A' and correct_idx == 0) or (predicted == 'B' and correct_idx == 1):
            correct += 1
    
    return correct / total
```

## Dataset Creation

### Generation Process

1. **Sentence Selection**: Base sentences are randomly selected from curated lists
2. **Rule Application**: Logical rules are applied to create valid arguments
3. **Fallacy Generation**: Corresponding fallacies are generated for invalid arguments  
4. **Randomization**: Argument order is randomized to prevent position bias
5. **Quality Control**: Generated arguments follow grammatical and logical patterns

### Curation Rationale

- Arguments are template-based to ensure logical validity/invalidity
- Randomization prevents models from learning position biases
- Multiple logical rules provide comprehensive reasoning evaluation
- Clean sentence construction avoids grammatical distractors

## Considerations for Use

### Recommended Use Cases

- Evaluating logical reasoning capabilities of language models
- Testing argument strength discrimination
- Benchmarking critical thinking skills
- Educational tools for logic and reasoning

### Limitations

- Arguments follow template patterns (may not reflect natural reasoning)
- Limited to formal logical reasoning (excludes informal reasoning)
- Relatively simple sentence structures
- Not suitable for factual knowledge evaluation
- Generated content may not capture real-world reasoning complexity

### Ethical Considerations

- Artificially generated content should not be taken as factual claims
- Intended for logical reasoning evaluation, not domain knowledge training
- Users should be aware of template-based generation approach

## Citation

```bibtex
@dataset{{{dataset_name},
  title={{{dataset_name.replace('_', ' ').title()} Dataset}},
  author={{Santelli, Mauro; Toranzo Calderón, Joaquín; Caso, Ramiro}},
  year={{{datetime.now().year}}},
  url={{https://huggingface.co/datasets/mesantelli/{dataset_name}}}
}}
```

## Dataset Card Creation

This dataset card was automatically generated using the m-peirce-a dataset card generator on {datetime.now().strftime('%Y-%m-%d')}.
"""
    
    return description


def create_dataset_card(dataset_path: Path, output_path: Path = None, dataset_name: str = None) -> None:
    """Create a complete HuggingFace dataset card for a given dataset."""
    
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset directory not found: {dataset_path}")
    
    if dataset_name is None:
        dataset_name = dataset_path.name
    
    if output_path is None:
        output_path = dataset_path / "README.md"
    
    print(f"Analyzing dataset: {dataset_path}")
    metadata = analyze_dataset(dataset_path)
    
    print(f"Generating dataset card for {dataset_name}...")
    
    # Generate YAML frontmatter and markdown content
    yaml_content = generate_yaml_frontmatter(metadata, dataset_name)
    description = generate_dataset_description(metadata, dataset_name)
    
    # Combine into full dataset card
    full_content = yaml_content + description
    
    # Save to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"✅ Dataset card created: {output_path}")
    print(f"📊 Total examples: {metadata['total_examples']}")
    print(f"📁 Total size: {metadata['total_bytes']:,} bytes")
    print(f"🌐 Languages: {', '.join(sorted(metadata['languages']))}")


def main():
    """CLI interface for creating dataset cards."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Create HuggingFace dataset cards for logical reasoning datasets")
    parser.add_argument("dataset_path", help="Path to dataset directory")
    parser.add_argument("--output", help="Output path for README.md (default: dataset_path/README.md)")
    parser.add_argument("--name", help="Dataset name (default: directory name)")
    
    args = parser.parse_args()
    
    dataset_path = Path(args.dataset_path)
    output_path = Path(args.output) if args.output else None
    
    create_dataset_card(dataset_path, output_path, args.name)


if __name__ == "__main__":
    main()