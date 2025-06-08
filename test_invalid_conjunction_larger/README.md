---
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
    num_bytes: 40000
    num_examples: 80
  - name: validation
    num_bytes: 5000
    num_examples: 10
  - name: test
    num_bytes: 5000
    num_examples: 10
  download_size: 50000
  dataset_size: 50000
task_categories:
- text-classification
- logical-reasoning
task_ids:
- logical-fallacy-detection
- argument-validity-classification
language:
['en']
pretty_name: Logical Arguments Dataset
size_categories:
- n<1K
---

# Logical Arguments Dataset

## Dataset Description

This dataset contains logical arguments with validity labels and comprehensive strength analysis, generated using the m-peirce-a logical argument system.

### Dataset Summary

The dataset includes 100 logical arguments across 20 different inference rules and fallacy types. Each argument is annotated with:

- **Logical validity**: Whether the argument follows valid inference rules
- **Strength analysis**: Multi-dimensional scoring including semantic plausibility, persuasiveness, and sophistication
- **Linguistic features**: Clarity, emotional impact, and persuasion techniques used
- **Semantic information**: Premises, conclusions, and domain classifications

### Supported Tasks

- **Logical fallacy detection**: Identify invalid arguments and classify fallacy types
- **Argument validity classification**: Binary classification of logical validity
- **Argument strength prediction**: Regression on multiple strength dimensions
- **Cross-lingual logical reasoning**: Available in 1 languages

### Languages

en

## Dataset Structure

### Data Instances

Each instance contains:

```json
{
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
}
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

- **Train**: 80 examples (80.0%)
- **Validation**: 10 examples (10.0%)
- **Test**: 10 examples (10.0%)

## Dataset Creation

### Source Data

Arguments are generated using semantic templates and context-aware systems that ensure:
- Realistic variable substitutions
- Semantic coherence within domains
- Varied complexity levels
- Multilingual consistency

### Rule Types Included

Affirming a Disjunct, Affirming the Consequent, Composition Fallacy, Conjunction Elimination, Conjunction Introduction, Constructive Dilemma, Denying the Antecedent, Destructive Dilemma, Disjunction Elimination, Disjunction Introduction, Disjunctive Syllogism, False Conjunction, False Dilemma, Hypothetical Syllogism, Invalid Conjunction Introduction, Invalid Disjunction Elimination, Material Conditional Introduction, Modus Ponens, Modus Tollens, Non Sequitur

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
@dataset{logical_arguments_2025,
  title={Logical Arguments Dataset},
  author={m-peirce-a system},
  year={2025},
  note={Generated logical arguments with validity and strength analysis}
}
```
