"""
streamlined_dataset_converter.py

Simplified HuggingFace dataset converter for the streamlined argument generation system.
Replaces the complex converter with a straightforward approach focused on the core task.
"""

import json
import random
import sys
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

from argument_generator import ArgumentGenerator, GeneratedArgument


@dataclass
class DatasetConfig:
    """Simple dataset configuration."""
    train_split: float = 0.8
    validation_split: float = 0.1
    test_split: float = 0.1


class StreamlinedDatasetConverter:
    """Simplified dataset converter focused on logical reasoning evaluation."""
    
    def __init__(self, 
                 dataset_name: str = "logical_arguments",
                 format_type: str = "paired"):
        """
        Initialize converter.
        
        Args:
            dataset_name: Name of the dataset
            format_type: "individual" or "paired" (paired recommended for evaluation)
        """
        self.dataset_name = dataset_name
        self.format_type = format_type
    
    def convert_to_paired_format(self, 
                                valid_arg: GeneratedArgument, 
                                invalid_arg: GeneratedArgument,
                                question_id: int,
                                split: str = "train") -> Dict[str, Any]:
        """Convert argument pair to evaluation format."""
        
        # Create the two options
        original_options = [valid_arg.text, invalid_arg.text]
        
        # Randomize order to avoid position bias
        randomized_options = original_options.copy()
        random.shuffle(randomized_options)
        
        # Create mapping from randomized back to original
        mapping = {}
        for i, randomized_option in enumerate(randomized_options):
            original_index = original_options.index(randomized_option)
            mapping[str(i)] = original_index
        
        # Determine correct answer indices
        correct_original_index = 0  # Valid argument is always at index 0 in original
        correct_randomized_index = randomized_options.index(original_options[0])
        
        return {
            "question_id": question_id,
            "test_options": {
                "original": original_options,
                "randomized": randomized_options,
                "mapping": mapping
            },
            "correct_answer": {
                "original_index": correct_original_index,
                "randomized_index": correct_randomized_index
            },
            "good_argument_type": valid_arg.rule_type,
            "bad_argument_type": invalid_arg.rule_type,
            "language": valid_arg.language,
            "sentences_used": valid_arg.sentences_used,
            "split": split
        }
    
    def convert_to_individual_format(self, 
                                   argument: GeneratedArgument,
                                   arg_id: int,
                                   split: str = "train") -> Dict[str, Any]:
        """Convert single argument to individual classification format."""
        return {
            "id": arg_id,
            "text": argument.text,
            "rule_type": argument.rule_type,
            "is_valid": argument.is_valid,
            "language": argument.language,
            "sentences_used": argument.sentences_used,
            "metadata": argument.metadata or {},
            "split": split
        }
    
    def generate_and_convert_dataset(self,
                                   sentences_file: str,
                                   num_arguments: int,
                                   output_dir: Path,
                                   language: str = "en",
                                   shared_sentences: bool = True,
                                   complexity: str = "mixed",
                                   style: str = "basic",
                                   rule_proportions: Dict[str, float] = None) -> None:
        """Generate and convert a complete dataset."""
        
        # Initialize generator
        generator = ArgumentGenerator(
            sentences_file=sentences_file,
            language=language,
            shared_sentences=shared_sentences
        )
        generator.set_complexity(complexity)
        generator.set_style(style)
        
        print(f"Generating {num_arguments} argument pairs...")
        print(f"Language: {language}")
        print(f"Shared sentences: {shared_sentences}")
        print(f"Complexity: {complexity}")
        print(f"Style: {style}")
        
        # Generate dataset
        try:
            dataset_pairs = generator.generate_dataset(num_arguments, rule_proportions=rule_proportions)
        except Exception as e:
            print(f"Error generating dataset: {e}")
            return
        
        if not dataset_pairs:
            print("No argument pairs generated successfully.")
            return
        
        print(f"Successfully generated {len(dataset_pairs)} argument pairs")
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Split dataset
        config = DatasetConfig()
        total_pairs = len(dataset_pairs)
        
        train_count = int(total_pairs * config.train_split)
        val_count = int(total_pairs * config.validation_split)
        test_count = total_pairs - train_count - val_count
        
        train_pairs = dataset_pairs[:train_count]
        val_pairs = dataset_pairs[train_count:train_count + val_count]
        test_pairs = dataset_pairs[train_count + val_count:]
        
        print(f"Dataset splits: train={len(train_pairs)}, val={len(val_pairs)}, test={len(test_pairs)}")
        
        # Convert and save each split
        splits = [
            ("train", train_pairs),
            ("validation", val_pairs), 
            ("test", test_pairs)
        ]
        
        for split_name, pairs in splits:
            if not pairs:
                continue
                
            self._save_split(pairs, output_dir, split_name, language, generator.get_statistics())
        
        # Save dataset info
        self._save_dataset_info(output_dir, language, generator.get_statistics(), 
                              total_pairs, len(train_pairs), len(val_pairs), len(test_pairs))
        
        # Save README
        self._save_readme(output_dir, language, generator.get_statistics(), 
                         total_pairs, shared_sentences, complexity, style)
        
        # Generate HuggingFace dataset card
        try:
            from create_hf_dataset_card import create_dataset_card
            print("Generating HuggingFace dataset card...")
            create_dataset_card(output_dir, dataset_name=self.dataset_name)
            print("✅ HuggingFace dataset card created")
        except ImportError:
            print("⚠ Could not import dataset card generator - skipping HF card creation")
        except Exception as e:
            print(f"⚠ Warning: Failed to create HuggingFace dataset card: {e}")
        
        print(f"✅ Dataset saved to {output_dir}")
    
    def _save_split(self, 
                   pairs: List[Tuple[GeneratedArgument, GeneratedArgument]],
                   output_dir: Path,
                   split_name: str,
                   language: str,
                   stats: Dict[str, Any]) -> None:
        """Save a dataset split to JSONL and TXT files."""
        
        jsonl_file = output_dir / f"{split_name}.jsonl"
        txt_file = output_dir / f"{split_name}.txt"
        
        with open(jsonl_file, 'w', encoding='utf-8') as jsonl_f, \
             open(txt_file, 'w', encoding='utf-8') as txt_f:
            
            for i, (valid_arg, invalid_arg) in enumerate(pairs, 1):
                
                if self.format_type == "paired":
                    # Paired comparison format (recommended for evaluation)
                    record = self.convert_to_paired_format(
                        valid_arg, invalid_arg, i, split_name
                    )
                    
                    # Write JSONL
                    jsonl_f.write(json.dumps(record, ensure_ascii=False) + '\n')
                    
                    # Write human-readable TXT
                    txt_f.write(f"Question {i}:\n")
                    txt_f.write(f"Option A: {record['test_options']['randomized'][0]}\n")
                    txt_f.write(f"Option B: {record['test_options']['randomized'][1]}\n")
                    correct_letter = 'A' if record['correct_answer']['randomized_index'] == 0 else 'B'
                    txt_f.write(f"Correct Answer: {correct_letter}\n")
                    txt_f.write(f"Good Type: {record['good_argument_type']}, Bad Type: {record['bad_argument_type']}\n")
                    txt_f.write("\n")
                
                else:
                    # Individual classification format
                    for j, arg in enumerate([valid_arg, invalid_arg]):
                        record = self.convert_to_individual_format(
                            arg, i * 2 + j - 1, split_name
                        )
                        
                        # Write JSONL
                        jsonl_f.write(json.dumps(record, ensure_ascii=False) + '\n')
                        
                        # Write human-readable TXT
                        txt_f.write(f"ID: {record['id']}\n")
                        txt_f.write(f"Text: {record['text']}\n")
                        txt_f.write(f"Valid: {record['is_valid']}\n")
                        txt_f.write(f"Rule: {record['rule_type']}\n")
                        txt_f.write("\n")
    
    def _save_dataset_info(self, 
                          output_dir: Path,
                          language: str,
                          stats: Dict[str, Any],
                          total_pairs: int,
                          train_count: int,
                          val_count: int,
                          test_count: int) -> None:
        """Save dataset metadata."""
        
        dataset_info = {
            "dataset_name": self.dataset_name,
            "description": "Logical argument dataset for reasoning evaluation using minimal pairs methodology",
            "version": "2.0.0-streamlined",
            "format": self.format_type,
            "language": language,
            "total_argument_pairs": total_pairs,
            "splits": {
                "train": train_count,
                "validation": val_count, 
                "test": test_count
            },
            "generator_stats": stats,
            "features": {
                "question_id": "Unique identifier for each question",
                "test_options": "Original and randomized argument pairs",
                "correct_answer": "Indices of the correct (valid) argument",
                "good_argument_type": "Name of the valid logical rule",
                "bad_argument_type": "Name of the corresponding fallacy",
                "language": "Language code",
                "sentences_used": "Source sentences used in generation",
                "split": "Dataset split (train/validation/test)"
            },
            "citation": "Generated using streamlined m-peirce-a logical argument system",
            "license": "MIT",
            "created": datetime.now().isoformat()
        }
        
        with open(output_dir / "dataset_info.json", 'w', encoding='utf-8') as f:
            json.dump(dataset_info, f, indent=2, ensure_ascii=False)
    
    def _save_readme(self, 
                    output_dir: Path,
                    language: str,
                    stats: Dict[str, Any],
                    total_pairs: int,
                    shared_sentences: bool,
                    complexity: str,
                    style: str) -> None:
        """Save README file with dataset description."""
        
        readme_content = f"""# {self.dataset_name.title()} Dataset

## Overview
This dataset contains logical argument pairs for evaluating reasoning capabilities using the "reasoning minimal pairs" methodology.

## Dataset Details
- **Language**: {language}
- **Total Argument Pairs**: {total_pairs}
- **Format**: {self.format_type}
- **Shared Sentences**: {shared_sentences}
- **Complexity Level**: {complexity}
- **Style**: {style}

## Generation Statistics
- **Source Sentences**: {stats.get('sentence_count', 'Unknown')}
- **Supported Rules**: {stats.get('supported_rules', 'Unknown')}
- **Generator Version**: Streamlined v2.0

## Format Description

### Paired Format (Recommended for Evaluation)
Each record contains:
- `question_id`: Unique question identifier
- `test_options`: Both original and randomized argument options (A, B)
- `correct_answer`: Index of the valid argument in both orders
- `good_argument_type`: Valid logical rule (e.g., "Modus Ponens")
- `bad_argument_type`: Corresponding fallacy (e.g., "Affirming the Consequent")

### Usage Example
```python
import json

# Load test data
with open('test.jsonl', 'r') as f:
    for line in f:
        question = json.loads(line)
        options = question['test_options']['randomized']
        correct_idx = question['correct_answer']['randomized_index']
        
        print(f"Question: Choose the logically valid argument")
        print(f"A: {{options[0]}}")
        print(f"B: {{options[1]}}")
        print(f"Correct: {{'A' if correct_idx == 0 else 'B'}}")
```

## Logical Rules Covered
The dataset covers 11 fundamental logical inference rules and their corresponding fallacies:

1. **Modus Ponens** → Affirming the Consequent
2. **Modus Tollens** → Denying the Antecedent  
3. **Disjunctive Syllogism** → Affirming a Disjunct
4. **Conjunction Introduction** → False Conjunction
5. **Conjunction Elimination** → Composition Fallacy
6. **Disjunction Introduction** → Invalid Conjunction Introduction
7. **Disjunction Elimination** → Invalid Disjunction Elimination
8. **Hypothetical Syllogism** → Non Sequitur
9. **Material Conditional Introduction** → Invalid Material Conditional Introduction
10. **Constructive Dilemma** → False Dilemma
11. **Destructive Dilemma** → Non Sequitur

## Citation
Generated using the streamlined m-peirce-a logical argument system.

## License
MIT License
"""
        
        with open(output_dir / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)


def parse_rule_proportions(proportions_str: str) -> Dict[str, float]:
    """
    Parse rule proportions from string format.
    
    Format: "rule1:0.3,rule2:0.2,rule3:0.5" or preset name like "basic_logic"
    """
    if not proportions_str:
        return None
    
    # Check if it's a preset name
    from argument_generator import ArgumentGenerator
    try:
        return ArgumentGenerator.get_preset_proportions(proportions_str)
    except ValueError:
        pass  # Not a preset, try parsing as custom proportions
    
    # Parse custom proportions
    proportions = {}
    try:
        for pair in proportions_str.split(','):
            rule, prop = pair.split(':')
            proportions[rule.strip()] = float(prop.strip())
        return proportions
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid proportions format: {proportions_str}. Use 'rule1:0.3,rule2:0.2' or preset name")


def main():
    """Command-line interface for dataset generation."""
    if len(sys.argv) < 3:
        print("Usage: python streamlined_dataset_converter.py <sentences_file> <num_arguments> [output_dir] [language] [format] [complexity] [shared_sentences] [rule_proportions]")
        print("\nExamples:")
        print("  python streamlined_dataset_converter.py data/sentences_english.txt 100")
        print("  python streamlined_dataset_converter.py data/sentences_spanish.txt 100 output es paired mixed true")
        print("  python streamlined_dataset_converter.py data/sentences_english.txt 100 output en paired mixed true \"Modus Ponens:0.4,Modus Tollens:0.3,Disjunctive Syllogism:0.3\"")
        print("  python streamlined_dataset_converter.py data/sentences_english.txt 100 output en paired mixed true \"basic_logic\"")
        return
    
    # Parse arguments
    sentences_file = sys.argv[1]
    num_arguments = int(sys.argv[2])
    output_dir = Path(sys.argv[3]) if len(sys.argv) > 3 else Path("outputs") / "streamlined_dataset"
    language = sys.argv[4] if len(sys.argv) > 4 else "en"
    format_type = sys.argv[5] if len(sys.argv) > 5 else "paired"
    complexity = sys.argv[6] if len(sys.argv) > 6 else "mixed"
    shared_sentences = sys.argv[7].lower() == 'true' if len(sys.argv) > 7 else True
    rule_proportions_str = sys.argv[8] if len(sys.argv) > 8 else None
    
    # Validate inputs
    if not Path(sentences_file).exists():
        print(f"Error: Sentences file not found: {sentences_file}")
        return
    
    if language not in ['en', 'es']:  # Add more as language handlers are created
        print(f"Error: Unsupported language: {language}. Supported: en, es")
        return
    
    if format_type not in ['individual', 'paired']:
        print(f"Error: Invalid format: {format_type}. Use 'individual' or 'paired'")
        return
    
    # Parse rule proportions if provided
    rule_proportions = None
    if rule_proportions_str:
        try:
            rule_proportions = parse_rule_proportions(rule_proportions_str)
            print(f"Using custom rule proportions: {rule_proportions}")
        except ValueError as e:
            print(f"Error: {e}")
            return
    
    # Generate dataset with meaningful name
    dataset_name = output_dir.name if output_dir.name != "streamlined_dataset" else f"logical_arguments_{language}"
    converter = StreamlinedDatasetConverter(
        dataset_name=dataset_name,
        format_type=format_type
    )
    
    try:
        converter.generate_and_convert_dataset(
            sentences_file=sentences_file,
            num_arguments=num_arguments,
            output_dir=output_dir,
            language=language,
            shared_sentences=shared_sentences,
            complexity=complexity,
            style="basic",
            rule_proportions=rule_proportions
        )
    except Exception as e:
        print(f"Error: {e}")
        return


if __name__ == "__main__":
    main()