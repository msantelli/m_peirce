"""
hf_dataset_converter.py

HuggingFace dataset converter for the logical argument generation system.
Converts GeneratedArgument objects to HuggingFace dataset format with JSONL export.
"""

import json
import uuid
import random
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

from advanced_generator import GeneratedArgument, AdvancedArgumentGenerator


@dataclass
class DatasetSplit:
    """Configuration for dataset splits."""
    train: float = 0.8
    validation: float = 0.1
    test: float = 0.1


class HuggingFaceDatasetConverter:
    """Converts logical arguments to HuggingFace dataset format."""
    
    def __init__(self, dataset_name: str = "logical_arguments", version: str = "1.0.0", format_type: str = "individual"):
        self.dataset_name = dataset_name
        self.version = version
        self.format_type = format_type  # "individual" or "paired"
        self.dataset_info = self._create_dataset_info()
        
    def _create_dataset_info(self) -> Dict[str, Any]:
        """Create dataset metadata."""
        return {
            "dataset_name": self.dataset_name,
            "version": self.version,
            "description": "Logical argument dataset with validity labels and strength analysis",
            "citation": "Generated using m-peirce-a logical argument system",
            "homepage": "",
            "license": "MIT",
            "features": {
                "id": {"dtype": "string", "_type": "Value"},
                "text": {"dtype": "string", "_type": "Value"},
                "rule_type": {"dtype": "string", "_type": "Value"},
                "is_valid": {"dtype": "bool", "_type": "Value"},
                "language": {"dtype": "string", "_type": "Value"},
                "complexity": {"dtype": "string", "_type": "Value"},
                "premises": {"feature": {"dtype": "string", "_type": "Value"}, "_type": "Sequence"},
                "conclusion": {"dtype": "string", "_type": "Value"},
                "variables": {"dtype": "string", "_type": "Value"},
                "semantic_coherence": {"dtype": "float64", "_type": "Value"},
                "domains": {"feature": {"dtype": "string", "_type": "Value"}, "_type": "Sequence"},
                "logical_validity": {"dtype": "float64", "_type": "Value"},
                "semantic_plausibility": {"dtype": "float64", "_type": "Value"},
                "linguistic_clarity": {"dtype": "float64", "_type": "Value"},
                "persuasiveness": {"dtype": "float64", "_type": "Value"},
                "sophistication": {"dtype": "float64", "_type": "Value"},
                "emotional_impact": {"dtype": "float64", "_type": "Value"},
                "overall_strength_score": {"dtype": "float64", "_type": "Value"},
                "techniques_used": {"feature": {"dtype": "string", "_type": "Value"}, "_type": "Sequence"},
                "strengths": {"feature": {"dtype": "string", "_type": "Value"}, "_type": "Sequence"},
                "weaknesses": {"feature": {"dtype": "string", "_type": "Value"}, "_type": "Sequence"},
                "timestamp": {"dtype": "string", "_type": "Value"},
                "split": {"dtype": "string", "_type": "Value"}
            },
            "task_categories": ["text-classification", "logical-reasoning"],
            "task_ids": ["logical-fallacy-detection", "argument-validity-classification"],
            "created": datetime.now().isoformat()
        }
    
    def convert_argument(self, argument: GeneratedArgument, split: str = "train") -> Dict[str, Any]:
        """Convert a single GeneratedArgument to HuggingFace format."""
        # Generate unique ID
        arg_id = str(uuid.uuid4())
        
        # Extract data from GeneratedArgument
        arg_dict = argument.to_dict()
        
        # Flatten strength analysis
        strength = arg_dict['strength_analysis']
        
        # Create HuggingFace compatible record
        hf_record = {
            "id": arg_id,
            "text": arg_dict['text'],
            "rule_type": arg_dict['rule_type'],
            "is_valid": arg_dict['is_valid'],
            "language": arg_dict['language'],
            "complexity": arg_dict['complexity'],
            
            # Semantic information
            "premises": arg_dict['semantic_info'].get('premises', []),
            "conclusion": arg_dict['semantic_info'].get('conclusion', ''),
            "variables": json.dumps(arg_dict['variables']),
            "semantic_coherence": arg_dict['semantic_info'].get('semantic_coherence', 0.0),
            "domains": arg_dict['semantic_info'].get('domains', []),
            
            # Strength analysis (flattened)
            "logical_validity": strength['logical_validity'],
            "semantic_plausibility": strength['semantic_plausibility'],
            "linguistic_clarity": strength['linguistic_clarity'],
            "persuasiveness": strength['persuasiveness'],
            "sophistication": strength['sophistication'],
            "emotional_impact": strength['emotional_impact'],
            "overall_strength_score": strength['overall_score'],
            "techniques_used": strength['techniques_used'],
            "strengths": strength['strengths'],
            "weaknesses": strength['weaknesses'],
            
            # Metadata
            "timestamp": arg_dict['generation_metadata'].get('timestamp', datetime.now().isoformat()),
            "split": split
        }
        
        return hf_record
    
    def convert_arguments(self, arguments: List[GeneratedArgument], 
                         split_config: Optional[DatasetSplit] = None) -> List[Dict[str, Any]]:
        """Convert multiple arguments with automatic splitting."""
        if split_config is None:
            split_config = DatasetSplit()
        
        total_args = len(arguments)
        train_size = int(total_args * split_config.train)
        val_size = int(total_args * split_config.validation)
        
        converted_args = []
        
        for i, arg in enumerate(arguments):
            if i < train_size:
                split = "train"
            elif i < train_size + val_size:
                split = "validation"
            else:
                split = "test"
            
            converted_args.append(self.convert_argument(arg, split))
        
        return converted_args
    
    def export_to_jsonl(self, arguments: List[GeneratedArgument], 
                       output_dir: Union[str, Path],
                       split_config: Optional[DatasetSplit] = None,
                       create_separate_files: bool = True) -> Dict[str, Path]:
        """Export arguments to JSONL format for HuggingFace datasets."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if self.format_type == "paired":
            return self._export_paired_format(arguments, output_dir, split_config, create_separate_files)
        else:
            return self._export_individual_format(arguments, output_dir, split_config, create_separate_files)
    
    def _export_individual_format(self, arguments: List[GeneratedArgument], 
                                 output_dir: Path, split_config: Optional[DatasetSplit],
                                 create_separate_files: bool) -> Dict[str, Path]:
        """Export in individual argument format."""
        # Convert arguments
        converted_args = self.convert_arguments(arguments, split_config)
        
        # Group by split
        splits = {}
        for arg in converted_args:
            split_name = arg['split']
            if split_name not in splits:
                splits[split_name] = []
            splits[split_name].append(arg)
        
        output_files = {}
        
        if create_separate_files:
            # Create separate JSONL files for each split
            for split_name, split_args in splits.items():
                output_file = output_dir / f"{split_name}.jsonl"
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    for arg in split_args:
                        f.write(json.dumps(arg, ensure_ascii=False) + '\n')
                
                output_files[split_name] = output_file
                print(f"Exported {len(split_args)} {split_name} examples to {output_file}")
        else:
            # Create single JSONL file with all data
            output_file = output_dir / f"{self.dataset_name}.jsonl"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                for arg in converted_args:
                    f.write(json.dumps(arg, ensure_ascii=False) + '\n')
            
            output_files['all'] = output_file
            print(f"Exported {len(converted_args)} examples to {output_file}")
        
        # Create dataset info file
        info_file = output_dir / "dataset_info.json"
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(self.dataset_info, f, indent=2, ensure_ascii=False)
        
        output_files['dataset_info'] = info_file
        
        return output_files
    
    def _export_paired_format(self, arguments: List[GeneratedArgument], 
                             output_dir: Path, split_config: Optional[DatasetSplit],
                             create_separate_files: bool) -> Dict[str, Path]:
        """Export in paired comparison format."""
        # Define logical pairings between valid rules and their corresponding fallacies
        # Based on actual generated fallacy names from the English system
        logical_pairings = {
            "Modus Ponens": "Affirming the Consequent",
            "Modus Tollens": "Denying the Antecedent", 
            "Disjunctive Syllogism": "Affirming a Disjunct",
            "Conjunction Introduction": "False Conjunction",
            "Conjunction Elimination": "Composition Fallacy",
            "Disjunction Introduction": "Invalid Conjunction Introduction",
            "Disjunction Elimination": "Invalid Disjunction Elimination",
            "Hypothetical Syllogism": "Non Sequitur",
            "Material Conditional Introduction": "Invalid Material Conditional Introduction",
            "Constructive Dilemma": "False Dilemma", 
            "Destructive Dilemma": "Non Sequitur"
        }
        
        # Group arguments by rule type
        valid_by_rule = {}
        invalid_by_rule = {}
        
        for arg in arguments:
            if arg.is_valid:
                if arg.rule_type not in valid_by_rule:
                    valid_by_rule[arg.rule_type] = []
                valid_by_rule[arg.rule_type].append(arg)
            else:
                if arg.rule_type not in invalid_by_rule:
                    invalid_by_rule[arg.rule_type] = []
                invalid_by_rule[arg.rule_type].append(arg)
        
        # Create logically paired questions
        paired_questions = []
        question_id = 1
        
        for valid_rule, fallacy_rule in logical_pairings.items():
            if valid_rule in valid_by_rule and fallacy_rule in invalid_by_rule:
                valid_args = valid_by_rule[valid_rule]
                invalid_args = invalid_by_rule[fallacy_rule]
                
                # Pair up to the minimum available in each group
                min_pairs = min(len(valid_args), len(invalid_args))
                
                for i in range(min_pairs):
                    good_arg = valid_args[i]
                    bad_arg = invalid_args[i]
                    
                    paired_question = create_paired_comparison(
                        good_arg, bad_arg, question_id, seed=question_id * 42
                    )
                    paired_questions.append(paired_question)
                    question_id += 1
        
        if not paired_questions:
            print("Warning: No valid logical pairings found in the generated arguments")
            return {}
        
        # Apply splits to paired questions
        if split_config is None:
            split_config = DatasetSplit()
        
        total_pairs = len(paired_questions)
        train_size = int(total_pairs * split_config.train)
        val_size = int(total_pairs * split_config.validation)
        
        # Add split information
        for i, question in enumerate(paired_questions):
            if i < train_size:
                question['split'] = 'train'
            elif i < train_size + val_size:
                question['split'] = 'validation'
            else:
                question['split'] = 'test'
        
        # Group by split
        splits = {}
        for question in paired_questions:
            split_name = question['split']
            if split_name not in splits:
                splits[split_name] = []
            splits[split_name].append(question)
        
        output_files = {}
        
        if create_separate_files:
            # Create separate files for each split
            for split_name, split_questions in splits.items():
                # JSONL format
                jsonl_file = output_dir / f"{split_name}.jsonl"
                with open(jsonl_file, 'w', encoding='utf-8') as f:
                    for question in split_questions:
                        f.write(json.dumps(question, ensure_ascii=False) + '\n')
                
                # Simple text format
                txt_file = output_dir / f"{split_name}.txt"
                with open(txt_file, 'w', encoding='utf-8') as f:
                    for question in split_questions:
                        f.write(f"Question {question['question_id']}:\n")
                        f.write(f"Option A: {question['test_options']['randomized'][0]}\n")
                        f.write(f"Option B: {question['test_options']['randomized'][1]}\n")
                        correct_letter = 'A' if question['correct_answer']['randomized_index'] == 0 else 'B'
                        f.write(f"Correct Answer: {correct_letter}\n")
                        f.write(f"Good Type: {question['good_argument_type']}\n")
                        f.write(f"Bad Type: {question['bad_argument_type']}\n")
                        f.write("\n" + "-"*50 + "\n\n")
                
                output_files[f"{split_name}_jsonl"] = jsonl_file
                output_files[f"{split_name}_txt"] = txt_file
                print(f"Exported {len(split_questions)} {split_name} paired questions to {jsonl_file} and {txt_file}")
        
        # Create dataset info file
        info_file = output_dir / "dataset_info.json"
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(self.dataset_info, f, indent=2, ensure_ascii=False)
        
        output_files['dataset_info'] = info_file
        
        return output_files
    
    def create_dataset_card(self, output_dir: Union[str, Path], 
                           arguments: List[GeneratedArgument]) -> Path:
        """Create a README.md dataset card for HuggingFace Hub."""
        output_dir = Path(output_dir)
        
        # Analyze dataset statistics
        stats = self._analyze_dataset_stats(arguments)
        
        card_content = f"""---
dataset_info:
  config_name: default
  features:
  - name: id
    dtype: string
  - name: text
    dtype: string
  - name: rule_type
    dtype: string
  - name: is_valid
    dtype: bool
  - name: language
    dtype: string
  - name: complexity
    dtype: string
  - name: premises
    sequence: string
  - name: conclusion
    dtype: string
  - name: logical_validity
    dtype: float64
  - name: semantic_plausibility
    dtype: float64
  - name: overall_strength_score
    dtype: float64
  splits:
  - name: train
    num_bytes: {stats['train_bytes']}
    num_examples: {stats['train_examples']}
  - name: validation
    num_bytes: {stats['val_bytes']}
    num_examples: {stats['val_examples']}
  - name: test
    num_bytes: {stats['test_bytes']}
    num_examples: {stats['test_examples']}
  download_size: {stats['total_bytes']}
  dataset_size: {stats['total_bytes']}
task_categories:
- text-classification
- logical-reasoning
task_ids:
- logical-fallacy-detection
- argument-validity-classification
language:
{stats['languages']}
pretty_name: Logical Arguments Dataset
size_categories:
- {stats['size_category']}
---

# Logical Arguments Dataset

## Dataset Description

This dataset contains logical arguments with validity labels and comprehensive strength analysis, generated using the m-peirce-a logical argument system.

### Dataset Summary

The dataset includes {stats['total_examples']} logical arguments across {len(stats['rule_types'])} different inference rules and fallacy types. Each argument is annotated with:

- **Logical validity**: Whether the argument follows valid inference rules
- **Strength analysis**: Multi-dimensional scoring including semantic plausibility, persuasiveness, and sophistication
- **Linguistic features**: Clarity, emotional impact, and persuasion techniques used
- **Semantic information**: Premises, conclusions, and domain classifications

### Supported Tasks

- **Logical fallacy detection**: Identify invalid arguments and classify fallacy types
- **Argument validity classification**: Binary classification of logical validity
- **Argument strength prediction**: Regression on multiple strength dimensions
- **Cross-lingual logical reasoning**: Available in {len(stats['languages'])} languages

### Languages

{', '.join(stats['languages'])}

## Dataset Structure

### Data Instances

Each instance contains:

```json
{{
  "id": "unique-uuid",
  "text": "If temperature rises, then pressure increases. Temperature rises. Therefore, pressure increases.",
  "rule_type": "Modus Ponens",
  "is_valid": true,
  "language": "en",
  "complexity": "intermediate",
  "premises": ["If temperature rises, then pressure increases", "Temperature rises"],
  "conclusion": "Therefore, pressure increases",
  "logical_validity": 1.0,
  "semantic_plausibility": 0.85,
  "persuasiveness": 0.75,
  "overall_strength_score": 0.82,
  "split": "train"
}}
```

### Data Fields

- `id`: Unique identifier for the argument
- `text`: The complete argument text
- `rule_type`: The logical rule or fallacy type
- `is_valid`: Boolean indicating logical validity
- `language`: Language code (en, es, fr, de)
- `complexity`: Argument complexity level
- `premises`: List of premise statements
- `conclusion`: The conclusion statement
- `logical_validity`: Numeric validity score (0 or 1)
- `semantic_plausibility`: Real-world plausibility score (0-1)
- `linguistic_clarity`: Clarity of expression score (0-1)
- `persuasiveness`: Psychological convincingness score (0-1)
- `sophistication`: Subtlety/sophistication score (0-1)
- `emotional_impact`: Emotional impact score (0-1)
- `overall_strength_score`: Weighted combination of all metrics (0-1)
- `techniques_used`: List of persuasion techniques employed
- `strengths`: List of identified argument strengths
- `weaknesses`: List of identified argument weaknesses

### Data Splits

- **Train**: {stats['train_examples']} examples ({stats['train_percent']:.1f}%)
- **Validation**: {stats['val_examples']} examples ({stats['val_percent']:.1f}%)
- **Test**: {stats['test_examples']} examples ({stats['test_percent']:.1f}%)

## Dataset Creation

### Source Data

Arguments are generated using semantic templates and context-aware systems that ensure:
- Realistic variable substitutions
- Semantic coherence within domains
- Varied complexity levels
- Multilingual consistency

### Rule Types Included

{', '.join(sorted(stats['rule_types']))}

### Personal and Sensitive Information

The dataset contains only generated logical arguments about general topics. No personal or sensitive information is included.

## Considerations for Using the Data

### Social Impact of Dataset

This dataset is designed for educational and research purposes in logical reasoning. It can help:
- Train models to detect logical fallacies
- Develop automated argument analysis tools
- Support logic education applications
- Research cross-lingual reasoning patterns

### Discussion of Biases

- Arguments are generated using predefined templates and may reflect biases in the template design
- Semantic domains may not equally represent all cultural contexts
- Strength scoring is based on Western logical traditions

### Other Known Limitations

- Generated arguments may not reflect the full complexity of real-world reasoning
- Some cultural and contextual nuances may be missing
- Template-based generation may create subtle patterns detectable by models

## Additional Information

### Dataset Curators

Generated using the m-peirce-a logical argument system.

### Licensing Information

MIT License

### Citation Information

```
@dataset{{logical_arguments_{datetime.now().year},
  title={{Logical Arguments Dataset}},
  author={{m-peirce-a system}},
  year={{{datetime.now().year}}},
  note={{Generated logical arguments with validity and strength analysis}}
}}
```
"""
        
        readme_file = output_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(card_content)
        
        return readme_file
    
    def _analyze_dataset_stats(self, arguments: List[GeneratedArgument]) -> Dict[str, Any]:
        """Analyze dataset statistics for the card."""
        total_examples = len(arguments)
        
        # Calculate split sizes
        train_size = int(total_examples * 0.8)
        val_size = int(total_examples * 0.1)
        test_size = total_examples - train_size - val_size
        
        # Estimate sizes (rough approximation)
        avg_size = 500  # bytes per example
        train_bytes = train_size * avg_size
        val_bytes = val_size * avg_size
        test_bytes = test_size * avg_size
        total_bytes = total_examples * avg_size
        
        # Size category
        if total_examples < 1000:
            size_category = "n<1K"
        elif total_examples < 10000:
            size_category = "1K<n<10K"
        elif total_examples < 100000:
            size_category = "10K<n<100K"
        else:
            size_category = "100K<n<1M"
        
        # Extract unique values
        languages = set()
        rule_types = set()
        
        for arg in arguments:
            languages.add(arg.language)
            rule_types.add(arg.rule_type)
        
        # Format languages for YAML
        lang_yaml = '\n'.join(f"- {lang}" for lang in sorted(languages))
        
        return {
            'total_examples': total_examples,
            'train_examples': train_size,
            'val_examples': val_size,
            'test_examples': test_size,
            'train_percent': (train_size / total_examples) * 100,
            'val_percent': (val_size / total_examples) * 100,
            'test_percent': (test_size / total_examples) * 100,
            'train_bytes': train_bytes,
            'val_bytes': val_bytes,
            'test_bytes': test_bytes,
            'total_bytes': total_bytes,
            'size_category': size_category,
            'languages': sorted(languages),
            'languages_yaml': lang_yaml,
            'rule_types': rule_types
        }


def get_available_rules(generator) -> List[str]:
    """Get list of rules that have working templates."""
    available_rules = []
    
    # Complete list of all logical rules that should be available
    all_logical_rules = [
        'Modus Ponens', 'Modus Tollens', 'Disjunctive Syllogism',
        'Conjunction Introduction', 'Conjunction Elimination',
        'Disjunction Introduction', 'Disjunction Elimination', 
        'Hypothetical Syllogism', 'Material Conditional Introduction',
        'Constructive Dilemma', 'Destructive Dilemma'
    ]
    
    # Language-specific rule availability 
    language_rules = {
        'es': all_logical_rules,  # Spanish has full implementation
        'en': all_logical_rules,  # English has full implementation
        'fr': all_logical_rules,  # French now has full implementation
        'de': all_logical_rules   # German now has full implementation
    }
    
    test_rules = language_rules.get(generator.language_code, ['Modus Ponens', 'Modus Tollens'])
    
    for rule in test_rules:
        try:
            # Test if we can generate a valid argument
            test_arg = generator.generate_with_options(rule, {'is_valid': True})
            if test_arg and len(test_arg.strip()) > 10 and "No template" not in test_arg:
                available_rules.append(rule)
                print(f"✓ {rule} template available")
            else:
                print(f"✗ {rule} template failed (result: {test_arg[:50]}...)")
        except Exception as e:
            print(f"✗ {rule} template failed: {e}")
    
    return available_rules


def create_paired_comparison(good_arg: GeneratedArgument, bad_arg: GeneratedArgument, question_id: int, seed: int = None) -> Dict[str, Any]:
    """Create a paired comparison question from good and bad arguments."""
    if seed is None:
        seed = random.randint(0, 2**32 - 1)
    
    # Set random seed for reproducible randomization
    rng = random.Random(seed)
    
    good_text = good_arg.text
    bad_text = bad_arg.text
    
    # Create original and randomized options
    original_options = [good_text, bad_text]
    randomized_options = original_options.copy()
    rng.shuffle(randomized_options)
    
    # Find mapping between original and randomized indices
    mapping = {}
    for rand_idx, option in enumerate(randomized_options):
        orig_idx = original_options.index(option)
        mapping[str(rand_idx)] = orig_idx
    
    # Determine correct answer indices
    good_orig_idx = 0  # good argument is always at index 0 in original
    good_rand_idx = randomized_options.index(good_text)
    
    return {
        "question_id": question_id,
        "test_options": {
            "original": original_options,
            "randomized": randomized_options,
            "mapping": mapping
        },
        "correct_answer": {
            "original_index": good_orig_idx,
            "randomized_index": good_rand_idx
        },
        "randomization_seed": seed,
        "good_argument_type": good_arg.rule_type,
        "bad_argument_type": bad_arg.rule_type
    }


def generate_sample_dataset(sentences_file: str, num_arguments: int = 100, language: str = 'en', complexity_mix: str = 'mixed') -> List[GeneratedArgument]:
    """Generate a sample dataset for testing."""
    print(f"Generating {num_arguments} sample arguments in {language.upper()}...")
    if complexity_mix == 'mixed':
        print("Using mixed complexity levels (premise-first + conclusion-first structures)")
    else:
        print(f"Using {complexity_mix} complexity level")
    
    from argument_generator_v2 import ArgumentGeneratorV2
    from argument_strength import ArgumentStrengthAnalyzer
    from linguistic_patterns import ComplexityLevel
    from datetime import datetime
    import random
    
    # Create simple generators directly
    arguments = []
    
    analyzer = ArgumentStrengthAnalyzer()
    
    # Create generator once for the specified language
    try:
        generator = ArgumentGeneratorV2(sentences_file, language=language, flexible_mode=True)
        print(f"Successfully initialized {language} generator")
    except Exception as e:
        print(f"Error initializing generator for {language}: {e}")
        return []
    
    # Get available rules that actually have templates
    print("Testing available rule templates...")
    available_rules = get_available_rules(generator)
    
    if not available_rules:
        print("No working rule templates found!")
        return []
    
    print(f"Using {len(available_rules)} available rules: {', '.join(available_rules)}")
    
    # Define complexity levels and their distribution
    complexity_map = {
        'basic': ComplexityLevel.BASIC,
        'intermediate': ComplexityLevel.INTERMEDIATE, 
        'advanced': ComplexityLevel.ADVANCED,
        'expert': ComplexityLevel.EXPERT,
        'mixed': None  # Will be handled specially
    }
    
    # Set up complexity selection strategy
    if complexity_mix == 'mixed':
        # Default: Mix of basic (premise-first) and intermediate (conclusion-first) 
        # with occasional advanced structures
        complexity_choices = [
            ComplexityLevel.BASIC,      # 40% - premise-first structures
            ComplexityLevel.BASIC,
            ComplexityLevel.INTERMEDIATE,   # 40% - conclusion-first structures  
            ComplexityLevel.INTERMEDIATE,
            ComplexityLevel.ADVANCED    # 20% - complex patterns
        ]
    else:
        # Single complexity level
        complexity_choices = [complexity_map.get(complexity_mix, ComplexityLevel.BASIC)]
    
    successful_generations = 0
    max_attempts = num_arguments * 3  # Allow more attempts
    
    for i in range(max_attempts):
        if successful_generations >= num_arguments:
            break
            
        rule = available_rules[i % len(available_rules)]
        is_valid = successful_generations % 2 == 0  # Alternate valid/invalid
        
        # Select complexity level for this generation
        selected_complexity = random.choice(complexity_choices)
        
        # Temporarily set generator complexity
        old_complexity = generator.config['complexity_level']
        generator.config['complexity_level'] = selected_complexity
        
        try:
            # Generate argument text with better error handling
            if is_valid:
                text = generator.generate_with_options(rule, {'is_valid': True})
                actual_rule = rule
            else:
                # For invalid arguments, use the generator's flexible mode
                text = generator.generate_with_options(rule, {'is_valid': False})
                
                # Determine the actual invalid rule name
                if hasattr(generator, 'rule_mappings') and rule in generator.rule_mappings:
                    actual_rule = generator.rule_mappings[rule]
                else:
                    actual_rule = f"{rule} (Invalid)"
            
            # Validate the generated text
            if not text or len(text.strip()) < 10 or "No template" in text:
                print(f"Skipping invalid generation: {text[:50]}...")
                continue
            
            # Analyze strength
            strength = analyzer.analyze_argument(text, actual_rule, is_valid)
            
            # Parse premises and conclusion better
            sentences = [s.strip() for s in text.split('.') if s.strip()]
            premises = sentences[:-1] if len(sentences) > 1 else [sentences[0] if sentences else text]
            conclusion = sentences[-1] if len(sentences) > 1 else ""
            
            # Create GeneratedArgument with the selected complexity
            arg = GeneratedArgument(
                text=text,
                rule_type=actual_rule,
                is_valid=is_valid,
                variables={},
                language=language,
                complexity=selected_complexity,
                strength_analysis=strength,
                semantic_info={
                    'premises': premises,
                    'conclusion': conclusion,
                    'semantic_coherence': 0.7,
                    'domains': ['general']
                },
                generation_metadata={
                    'timestamp': datetime.now().isoformat(),
                    'plausibility_score': 0.7,
                    'generation_attempt': i + 1,
                    'available_rules': available_rules,
                    'complexity_level': selected_complexity.name
                }
            )
            
            arguments.append(arg)
            successful_generations += 1
            
            if successful_generations % 25 == 0:
                print(f"Generated {successful_generations}/{num_arguments} arguments...")
                
        except Exception as e:
            print(f"Error generating argument {i + 1} ({rule}, valid={is_valid}): {e}")
        finally:
            # Restore original complexity level
            generator.config['complexity_level'] = old_complexity
    
    print(f"Successfully generated {len(arguments)} arguments in {language.upper()}")
    print(f"Success rate: {len(arguments)}/{max_attempts} = {len(arguments)/max_attempts*100:.1f}%")
    return arguments


def main():
    """Demonstrate the HuggingFace dataset converter."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python hf_dataset_converter.py <sentences_file> [num_arguments] [output_dir] [language] [format] [complexity]")
        print("Languages: en (English), es (Spanish), fr (French), de (German)")
        print("Formats: individual (default), paired")
        print("Complexity: mixed (default - premise+conclusion-first), basic, intermediate, advanced, expert")
        return
    
    sentences_file = sys.argv[1]
    num_arguments = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "hf_dataset"
    language = sys.argv[4] if len(sys.argv) > 4 else "en"
    format_type = sys.argv[5] if len(sys.argv) > 5 else "individual"
    complexity_mix = sys.argv[6] if len(sys.argv) > 6 else "mixed"
    
    # Validate language
    valid_languages = ['en', 'es', 'fr', 'de']
    if language not in valid_languages:
        print(f"Error: Invalid language '{language}'. Valid options: {', '.join(valid_languages)}")
        return
    
    # Validate format
    valid_formats = ['individual', 'paired']
    if format_type not in valid_formats:
        print(f"Error: Invalid format '{format_type}'. Valid options: {', '.join(valid_formats)}")
        return
    
    # Validate complexity
    valid_complexities = ['mixed', 'basic', 'intermediate', 'advanced', 'expert']
    if complexity_mix not in valid_complexities:
        print(f"Error: Invalid complexity '{complexity_mix}'. Valid options: {', '.join(valid_complexities)}")
        return
    
    print(f"Generating dataset in {language.upper()} language")
    
    # Generate sample arguments
    arguments = generate_sample_dataset(sentences_file, num_arguments, language, complexity_mix)
    
    if not arguments:
        print("No arguments generated!")
        return
    
    # Create converter with language-specific name
    dataset_name = f"logical_arguments_{language}"
    converter = HuggingFaceDatasetConverter(dataset_name, "1.0.0", format_type=format_type)
    
    # Export to JSONL
    print(f"\nExporting to {output_dir}...")
    output_files = converter.export_to_jsonl(
        arguments, 
        output_dir,
        split_config=DatasetSplit(train=0.8, validation=0.1, test=0.1),
        create_separate_files=True
    )
    
    # Create dataset card
    readme_file = converter.create_dataset_card(output_dir, arguments)
    print(f"Created dataset card: {readme_file}")
    
    # Show summary
    print(f"\nDataset created successfully!")
    print(f"Language: {language.upper()}")
    print(f"Total arguments: {len(arguments)}")
    print(f"Output directory: {output_dir}")
    print(f"Files created:")
    for split, file_path in output_files.items():
        print(f"  {split}: {file_path}")
    
    # Show language distribution to verify consistency
    lang_count = {}
    for arg in arguments:
        lang = arg.language
        lang_count[lang] = lang_count.get(lang, 0) + 1
    
    print(f"\nLanguage distribution:")
    for lang, count in lang_count.items():
        print(f"  {lang}: {count} arguments ({count/len(arguments)*100:.1f}%)")


if __name__ == "__main__":
    main()