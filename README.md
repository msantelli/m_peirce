# Logical Argument Generation System (m-peirce-a)

A sophisticated multi-language logical argument generation system with context-aware capabilities, comprehensive strength analysis, and educational features. This system generates valid and invalid logical arguments across multiple languages with rich metadata for educational and research applications.

## 🌟 Features

### 🎯 Core Capabilities
- **Multi-language Support**: English, Spanish, French, German with extensible architecture
- **11 Logical Inference Rules**: Both valid forms and common fallacies
- **Context-Aware Generation**: Semantic coherence and thematic consistency
- **Advanced Strength Analysis**: Multi-dimensional argument assessment
- **Educational Tools**: Interactive configuration, difficulty calibration, quiz generation
- **HuggingFace Integration**: Ready-to-use dataset export functionality

### 🌍 Language Features
- **50+ Linguistic Variations** per language
- **Multiple Expression Styles**: Formal, casual, academic, colloquial
- **Rich Pattern Library**: Negations, conjunctions, disjunctions, conditionals
- **Cultural Adaptation**: Language-specific reasoning patterns

### 🧠 Argument Types & Structural Variations

#### Valid Inference Rules (11 Total)
- **Modus Ponens**: If P then Q, P, therefore Q
- **Modus Tollens**: If P then Q, not Q, therefore not P
- **Disjunctive Syllogism**: P or Q, not P, therefore Q
- **Conjunction Introduction/Elimination**: Combining and separating premises
- **Disjunction Introduction/Elimination**: Adding/removing disjunctive options
- **Hypothetical Syllogism**: Chaining conditional statements
- **Material Conditional Introduction**: Deriving conditionals from premises
- **Constructive/Destructive Dilemma**: Complex conditional reasoning

#### Common Fallacies (8 Total)
- **Affirming the Consequent**: If P then Q, Q, therefore P
- **Denying the Antecedent**: If P then Q, not P, therefore not Q
- **Affirming a Disjunct**: P or Q, P, therefore not Q
- **False Dilemma**: Presenting only two options when more exist
- **False Conjunction**: Concluding conjunction from single premise
- **Composition Fallacy**: Attributing group properties to individuals
- **Invalid Disjunction Elimination**: Improper elimination from disjunctions
- **Non Sequitur**: Conclusions that don't follow from premises

#### 🔄 Argument Structure Variations

**Premise-First Structure (Traditional):**
```
"If temperature rises, then pressure increases.
Temperature rises.
Therefore, pressure increases."
```

**Conclusion-First Structure (Premise Markers):**
```
"Pressure increases, because temperature rises
and we know that if temperature rises, then pressure increases."
```

**Available Conclusion Markers:**
- Standard: "therefore", "thus", "hence", "consequently"
- Formal: "it follows that", "we can conclude that", "this establishes"
- Academic: "proving that", "demonstrating that", "confirming that"

**Available Premise Markers:**
- Causal: "because", "since", "as", "due to"
- Given: "given that", "considering that", "in light of"
- Formal: "on the grounds that", "by virtue of", "owing to"

## 🚀 Quick Start

### Basic Usage

```python
from advanced_generator import AdvancedArgumentGenerator

# Initialize generator
generator = AdvancedArgumentGenerator('data/sentences.txt')

# Generate a single argument
argument = generator.generate_single('Modus Ponens')
print(argument.text)
print(f"Valid: {argument.is_valid}")
print(f"Strength: {argument.strength_analysis.overall_score:.2f}")

# Generate a valid/invalid pair
valid_arg, invalid_arg = generator.generate_pair('Modus Ponens')
```

### Interactive Configuration

```python
# Run interactive configuration session
generator.interactive_generation_session()

# Or configure programmatically
generator.configure(
    language='es',
    complexity='advanced',
    domain='scientific',
    target_persuasiveness=0.8,
    output_format='educational'
)
```

### HuggingFace Dataset Export

```python
from hf_dataset_converter import HuggingFaceDatasetConverter

# Generate arguments
arguments = []
for i in range(100):
    arg = generator.generate_single()
    arguments.append(arg)

# Convert to HuggingFace format
converter = HuggingFaceDatasetConverter("logical_arguments", "1.0.0")
converter.export_to_jsonl(arguments, "my_dataset")
```

### 📊 Dataset Generation Formats

The system supports multiple output formats for different use cases:

#### Individual Format
Each argument as a separate record with complete metadata:
```python
python hf_dataset_converter.py data/sentences_english.txt 100 my_dataset en individual
```

#### Paired Comparison Format
Valid/invalid argument pairs with randomization for assessment:
```python
python hf_dataset_converter.py data/sentences_english.txt 100 my_dataset en paired
```

**Paired Format Features:**
- Logical rule-to-fallacy mappings (Modus Ponens ↔ Affirming the Consequent)
- Randomized option order with mapping preservation
- Reproducible seeds for consistent randomization
- Both JSONL and human-readable TXT formats

#### **Complexity Control for Argument Structure**

**Mixed Complexity (Default - Recommended)**
```bash
python hf_dataset_converter.py data/sentences_english.txt 300 dataset en paired mixed
```
Produces diverse argument structures:
- 40% premise-first: "If P, then Q. P. Therefore, Q."
- 40% conclusion-first: "Q because P. Also, if P, then Q."
- 20% advanced: Complex formal patterns

**Structure-Specific Generation**
```bash
# Only traditional premise-first structures
python hf_dataset_converter.py data/sentences_english.txt 100 dataset en paired basic

# Only conclusion-first with premise markers  
python hf_dataset_converter.py data/sentences_english.txt 100 dataset en paired intermediate

# Expert-level with logical notation
python hf_dataset_converter.py data/sentences_english.txt 100 dataset en paired expert
```

## 📋 Installation

### Requirements
- Python 3.7+
- No external dependencies required (pure Python implementation)

### Setup
```bash
git clone <repository-url>
cd m-peirce-a
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## 🏗️ System Architecture

### Core Components

| Component | Purpose | Key Features |
|-----------|---------|--------------|
| `advanced_generator.py` | Main orchestrator | Phase 4 integration, session management |
| `argument_generator_v2.py` | Multi-language engine | Enhanced rule processing, flexible generation |
| `context_aware_system.py` | Semantic analysis | Domain classification, coherence scoring |
| `argument_strength.py` | Quality assessment | Multi-dimensional analysis, persuasion detection |
| `interactive_config.py` | User interface | Real-time configuration, profile management |
| `hf_dataset_converter.py` | Data export | HuggingFace dataset creation, JSONL export |

### Language Architecture

```
language_base.py           # Abstract base classes
├── languages/
│   ├── english.py         # Complete English implementation  
│   ├── spanish.py         # Spanish patterns and rules
│   ├── french.py          # French linguistic features
│   └── german.py          # German grammar patterns
├── linguistic_patterns.py # Shared pattern definitions
└── template_system.py     # Template engine
```

## 🎨 Configuration Options

### Language Settings
- **Languages**: `en`, `es`, `fr`, `de`
- **Complexity**: `mixed` (default), `basic`, `intermediate`, `advanced`, `expert`
- **Formality**: `casual`, `neutral`, `formal`, `academic`

### 🎛️ Complexity-Based Linguistic Variations

#### Mixed Level (Default)
- **40% Basic**: Premise-first structures ("If P, then Q. P. Therefore, Q.")
- **40% Intermediate**: Conclusion-first structures ("Q because P. Also, if P, then Q.")
- **20% Advanced**: Complex formal patterns with sophisticated language
- **Automatic variety**: Ensures diverse argument structures in every dataset

#### Basic Level
- Simple sentence structures with premise-first ordering
- Common connectives ("if...then", "and", "or")
- Straightforward conclusion markers ("therefore", "thus", "so")
- Example: "If rain falls, then streets get wet. Rain falls. Therefore, streets get wet."

#### Intermediate Level  
- **Conclusion-first structures** with premise markers
- Causal reasoning patterns ("because", "since", "given that")
- Sophisticated connectives ("moreover", "additionally", "furthermore")
- Example: "Streets get wet because rain falls. Also, if rain falls, then streets get wet."

#### Advanced Level
- Complex reasoning patterns with formal academic language
- Modal expressions ("necessarily", "sufficient for", "required that")
- Sophisticated premise markers ("in light of", "on the grounds that")
- Multiple embedded conditionals and complex logical structures

#### Expert Level
- **Formal logical notation** (→, ∧, ∨, ¬)
- Meta-logical language ("from the premise", "logical entailment", "valid inference")
- Philosophical terminology ("proposition", "material conditional", "logical consequence")
- Example: "From P → Q and P, we derive Q by modus ponens."

### 🌐 Multilingual Consistency

All languages implement the same logical rules with language-specific patterns:

**English**: "If P, then Q" → "P" → "Therefore, Q"
**Spanish**: "Si P, entonces Q" → "P" → "Por lo tanto, Q"  
**French**: "Si P, alors Q" → "P" → "Par conséquent, Q"
**German**: "Wenn P, dann Q" → "P" → "Also, Q"

### Domain Specialization
- **Scientific**: Research methodology, statistical language
- **Legal**: Precedent application, statutory interpretation
- **Everyday**: Casual expressions, story-like formats
- **Academic**: Scholarly language, theoretical frameworks
- **Philosophical**: Metaphysical concepts, modal logic
- **Business**: Strategic planning, market analysis
- **Medical**: Clinical evidence, diagnostic reasoning

### Output Formats
- **Standard**: Clean presentation with optional analysis
- **Educational**: Detailed explanations and learning feedback
- **Quiz**: Interactive format for assessment
- **Comparative**: Side-by-side multi-language view
- **Detailed**: Complete metadata and statistics
- **JSON**: Structured data for programmatic use

## 📊 Strength Analysis Features

### Multi-Dimensional Assessment
- **Logical Validity** (0-1): Adherence to inference rules
- **Semantic Plausibility** (0-1): Real-world likelihood  
- **Linguistic Clarity** (0-1): Expression clarity and structure
- **Persuasiveness** (0-1): Psychological convincingness
- **Sophistication** (0-1): Subtlety and complexity
- **Emotional Impact** (0-1): Emotional resonance

### Persuasion Technique Detection
- Appeal to Authority, Emotion, Common Sense
- Fear Appeals, Tradition, Novelty, Popularity
- False Certainty, Oversimplification
- Misleading Analogies

### Educational Feedback
```python
# Get detailed feedback
feedback = analyzer.generate_feedback(argument.strength_analysis)
print(feedback)
# Output: "This is a moderately strong argument. 
#          Strengths: Logically valid inference, Clear structure.
#          Weaknesses: Commits Affirming the Consequent fallacy."
```

## 🎓 Educational Applications

### Difficulty-Calibrated Generation
```python
# Generate arguments at specific difficulty levels
easy_pairs = generator.generate_difficulty_calibrated_set('easy', count=10)
expert_pairs = generator.generate_difficulty_calibrated_set('expert', count=5)
```

### Themed Argument Sets
```python
from context_aware_system import SemanticDomain

# Generate science-themed arguments
science_args = generator.generate_themed_set(
    SemanticDomain.SCIENCE, 
    ['Modus Ponens', 'Modus Tollens']
)
```

### Multi-language Comparisons
```python
# Same argument across languages
comparisons = generator.generate_multilingual_comparison('Modus Ponens')
for lang, argument in comparisons.items():
    print(f"{lang}: {argument.text}")
```

## 📁 Project Structure

```
m-peirce-a/
├── README.md                    # This file
├── advanced_generator.py        # Main system orchestrator
├── argument_generator_v2.py     # Enhanced multi-language generator
├── context_aware_system.py      # Semantic analysis and coherence
├── argument_strength.py         # Comprehensive strength analysis
├── interactive_config.py        # Configuration management
├── hf_dataset_converter.py      # HuggingFace dataset export
├── template_system.py           # Template engine
├── domain_templates.py          # Domain-specific templates
├── linguistic_patterns.py       # Shared linguistic patterns
├── language_base.py             # Language architecture foundation
├── english_integration.py       # Enhanced English features
├── languages/                   # Language-specific implementations
│   ├── english.py
│   ├── spanish.py
│   ├── french.py
│   └── german.py
├── demos/                       # Demonstration scripts
│   ├── phase2_demo.py
│   ├── phase4_demo.py
│   └── multilingual_demo.py
├── data/                        # Input data
│   └── sentences.txt
└── generated_files/             # Pre-generated example outputs
    ├── arguments_v2.txt
    ├── arguments_spanish.txt
    ├── arguments_french.txt
    └── arguments_german.txt
```

## 🔧 Advanced Usage

### Custom Rule Implementation
```python
# Add new logical rule
class CustomRule(LogicalRule):
    def __init__(self):
        super().__init__("Custom Rule", required_premises=2)
    
    def generate_valid(self, premises):
        # Implementation
        pass
    
    def generate_invalid(self, premises):
        # Implementation  
        pass
```

### Batch Processing
```python
# Generate large datasets
def batch_generate(count=1000):
    arguments = []
    for i in range(count):
        if i % 2 == 0:
            arg = generator.generate_single()
        else:
            valid, invalid = generator.generate_pair()
            arguments.extend([valid, invalid])
    return arguments
```

### Statistical Analysis
```python
# View generation statistics
generator._show_statistics()
# Output: 
# Total arguments generated: 150
# By rule type:
#   Modus Ponens: 45
#   Modus Tollens: 38
# Average strength score: 0.742
```

## 📈 Performance & Scalability

- **Generation Speed**: ~100 arguments/second
- **Memory Usage**: Efficient template caching
- **Scalability**: Batch generation up to 10,000+ arguments
- **Extensibility**: Plugin architecture for new languages/domains

## 🤝 Contributing

### Adding New Languages
1. Create new file in `languages/` directory
2. Inherit from `LanguageBase` 
3. Implement required patterns and rules
4. Add language code to configuration

### Adding New Domains
1. Define domain templates in `domain_templates.py`
2. Add domain-specific vocabulary
3. Configure semantic patterns
4. Update configuration options

### Adding New Rules
1. Define rule logic in appropriate language files
2. Add template patterns
3. Implement both valid and invalid forms
4. Update rule mappings

## 📊 Dataset Export & Usage

### Command-Line Dataset Generation

#### **Basic Usage**
```bash
# Generate English dataset with mixed complexity (default - includes both structures)
python hf_dataset_converter.py data/sentences_english.txt 100 english_dataset en paired

# Full syntax with all parameters
python hf_dataset_converter.py <sentences_file> [num_arguments] [output_dir] [language] [format] [complexity]
```

#### **Complexity Level Examples**
```bash
# Mixed complexity (DEFAULT) - 40% premise-first + 40% conclusion-first + 20% advanced
python hf_dataset_converter.py data/sentences_english.txt 300 mixed_dataset en paired mixed

# Only premise-first structures ("If P, then Q. P. Therefore, Q.")
python hf_dataset_converter.py data/sentences_english.txt 100 premise_first en paired basic

# Only conclusion-first structures ("Q because P. Also, if P, then Q.")
python hf_dataset_converter.py data/sentences_english.txt 100 conclusion_first en paired intermediate

# Advanced formal patterns
python hf_dataset_converter.py data/sentences_english.txt 100 advanced_dataset en paired advanced

# Expert-level with logical notation (→, ∧, ∨)
python hf_dataset_converter.py data/sentences_english.txt 100 expert_dataset en paired expert
```

#### **Language-Specific Examples**
```bash
# Spanish dataset with mixed complexity
python hf_dataset_converter.py data/sentences_spanish.txt 200 spanish_mixed es paired mixed

# French dataset with only conclusion-first structures
python hf_dataset_converter.py data/sentences_french.txt 150 french_conclusion fr paired intermediate

# German dataset with expert-level complexity
python hf_dataset_converter.py data/sentences_german.txt 100 german_expert de paired expert
```

### Available Data Files
- `data/sentences_english.txt` - English semantic templates
- `data/sentences_spanish.txt` - Spanish linguistic patterns  
- `data/sentences_french.txt` - French grammatical structures
- `data/sentences_german.txt` - German syntactic templates

### **Parameter Reference**

| Parameter | Options | Description |
|-----------|---------|-------------|
| `sentences_file` | `data/sentences_*.txt` | **Required**: Language-specific sentence templates |
| `num_arguments` | Integer (default: 50) | Number of arguments to generate |
| `output_dir` | String (default: "hf_dataset") | Output directory name |
| `language` | `en`, `es`, `fr`, `de` (default: `en`) | Target language |
| `format` | `individual`, `paired` (default: `individual`) | Output format type |
| `complexity` | `mixed`, `basic`, `intermediate`, `advanced`, `expert` (default: `mixed`) | **NEW**: Argument structure complexity |

### **Complexity Levels Explained**

| Level | Structure | Example Output | Use Case |
|-------|-----------|----------------|----------|
| `mixed` *(default)* | 40% premise-first + 40% conclusion-first + 20% advanced | Diverse structures in one dataset | **Recommended for most applications** |
| `basic` | Premise-first only | "If P, then Q. P. Therefore, Q." | Traditional logic education |
| `intermediate` | Conclusion-first only | "Q because P. Also, if P, then Q." | Advanced reasoning patterns |
| `advanced` | Formal academic | Complex modal expressions | Research applications |
| `expert` | Logical notation | "From P → Q and P, derive Q" | Logic & philosophy courses |

### HuggingFace Dataset Format

#### Individual Format Schema
```json
{
  "id": "unique-uuid",
  "text": "If P then Q. P. Therefore, Q.",
  "rule_type": "Modus Ponens", 
  "is_valid": true,
  "language": "en",
  "complexity": "intermediate",
  "premises": ["If P then Q", "P"],
  "conclusion": "Therefore, Q",
  "logical_validity": 1.0,
  "semantic_plausibility": 0.85,
  "persuasiveness": 0.75,
  "overall_strength_score": 0.82,
  "techniques_used": ["appeal_to_authority"],
  "strengths": ["Logically valid inference"],
  "weaknesses": [],
  "timestamp": "2025-06-07T14:54:47.303650"
}
```

#### Paired Comparison Format Schema
```json
{
  "question_id": 1,
  "test_options": {
    "original": ["Valid argument text", "Invalid argument text"],
    "randomized": ["Invalid argument text", "Valid argument text"], 
    "mapping": {"0": 1, "1": 0}
  },
  "correct_answer": {
    "original_index": 0,
    "randomized_index": 1
  },
  "randomization_seed": 42,
  "good_argument_type": "Modus Ponens",
  "bad_argument_type": "Affirming the Consequent",
  "split": "train"
}
```

### Output Files Generated
Each dataset generation creates:
- `train.jsonl` / `train.txt` - Training data (80%)
- `validation.jsonl` / `validation.txt` - Validation data (10%)  
- `test.jsonl` / `test.txt` - Test data (10%)
- `dataset_info.json` - Dataset metadata
- `README.md` - Dataset documentation

### Dataset Applications
- **Logical Fallacy Detection**: Train models to identify invalid reasoning
- **Argument Strength Prediction**: Multi-dimensional regression tasks
- **Cross-lingual Reasoning**: Study logical patterns across languages
- **Educational Assessment**: Automated evaluation of student responses
- **Multilingual Logic Models**: Train reasoning systems across languages

## 📝 Examples

### Example 1: Basic Generation
```python
from advanced_generator import AdvancedArgumentGenerator

generator = AdvancedArgumentGenerator('data/sentences_english.txt')
arg = generator.generate_single('Modus Ponens')

print(f"Argument: {arg.text}")
print(f"Rule: {arg.rule_type}")
print(f"Valid: {arg.is_valid}")
print(f"Language: {arg.language}")
print(f"Strength: {arg.strength_analysis.overall_score:.2f}")

# Example Output:
# Argument: If computers process data, then scientists study phenomena. 
#           Computers process data. Therefore, scientists study phenomena.
# Rule: Modus Ponens
# Valid: True
# Language: en
# Strength: 0.85
```

### Example 2: Structural Variations
```python
# Generate different argument structures
basic_arg = generator.generate_single('Modus Ponens', complexity='basic')
print(f"Basic: {basic_arg.text}")
# Output: "If P, then Q. P. Therefore, Q."

advanced_arg = generator.generate_single('Modus Ponens', complexity='advanced') 
print(f"Advanced: {advanced_arg.text}")
# Output: "Q, because P and we know that if P, then Q."

expert_arg = generator.generate_single('Modus Ponens', complexity='expert')
print(f"Expert: {expert_arg.text}")
# Output: "From the conditional P → Q and the premise P, we derive Q."
```

### Example 3: Educational Use
```python
# Configure for beginners
generator.configure(
    complexity='basic',
    domain='everyday',
    formality='casual',
    target_persuasiveness=0.3,
    output_format='educational'
)

# Generate quiz questions
valid, invalid = generator.generate_pair('Modus Ponens')
print("Which argument is valid?")
print(f"A) {valid.text}")
print(f"B) {invalid.text}")

# Example Output:
# A) If rain falls, then streets get wet. Rain falls. Thus, streets get wet.
# B) If rain falls, then streets get wet. Streets get wet. Thus, rain falls.
```

### Example 4: Complexity-Aware Generation
```python
# Generate different complexity levels
complexities = ['basic', 'intermediate', 'advanced', 'expert']

for complexity in complexities:
    # Generate with specific complexity
    os.system(f'python hf_dataset_converter.py data/sentences_english.txt 50 {complexity}_dataset en paired {complexity}')
    
    print(f"Generated {complexity} dataset with:")
    if complexity == 'basic':
        print("- Premise-first structures only")
        print("- Simple connectives (if-then, and, or)")
    elif complexity == 'intermediate':
        print("- Conclusion-first structures")
        print("- Premise markers (because, since, given that)")
    elif complexity == 'advanced':
        print("- Complex formal patterns")
        print("- Modal expressions (necessarily, sufficient for)")
    elif complexity == 'expert':
        print("- Logical notation (→, ∧, ∨)")
        print("- Meta-logical terminology")

# Generate mixed complexity (default)
os.system('python hf_dataset_converter.py data/sentences_english.txt 300 mixed_dataset en paired mixed')
print("Mixed dataset: 40% premise-first + 40% conclusion-first + 20% advanced")
```

### Example 5: Multilingual Dataset Generation
```python
# Generate datasets for all languages with mixed complexity
languages = ['en', 'es', 'fr', 'de']

for lang in languages:
    # Generate paired comparison dataset with mixed structures
    os.system(f'python hf_dataset_converter.py data/sentences_{lang}.txt 100 {lang}_mixed {lang} paired mixed')
    
    print(f"Generated {lang} dataset with:")
    print(f"- All 11 logical rules")  
    print(f"- Proper logical pairings")
    print(f"- Mixed complexity structures")
    print(f"- Both JSONL and TXT formats")
```

### Example 3: Research Application
```python
# Generate diverse dataset for research
languages = ['en', 'es', 'fr', 'de']
complexities = ['basic', 'intermediate', 'advanced']
domains = ['scientific', 'legal', 'philosophical']

dataset = []
for lang in languages:
    for complexity in complexities:
        for domain in domains:
            generator.configure(
                language=lang,
                complexity=complexity, 
                domain=domain
            )
            args = [generator.generate_single() for _ in range(10)]
            dataset.extend(args)

# Export to HuggingFace format
converter = HuggingFaceDatasetConverter()
converter.export_to_jsonl(dataset, "research_dataset")
```

## 🔍 Troubleshooting

### Common Issues

**Import Errors**: Ensure all files are in the same directory
```bash
# Check file structure
ls -la *.py
```

**Generation Failures**: Verify sentences.txt file exists and is readable
```python
# Test data loading
with open('data/sentences.txt', 'r') as f:
    print(f"Loaded {len(f.readlines())} sentences")
```

**Configuration Errors**: Use built-in validation
```python
# Validate configuration
is_valid, message = generator.configurator.validate_configuration(config)
if not is_valid:
    print(f"Configuration error: {message}")
```

## 📚 Research Applications

This system has been designed for:
- **Logic Education**: Teaching inference rules and fallacy detection
- **NLP Research**: Cross-lingual logical reasoning datasets
- **Cognitive Science**: Studying argument comprehension and persuasion
- **AI Training**: Creating training data for reasoning models
- **Educational Assessment**: Automated evaluation of logical reasoning

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Built on logical reasoning principles from formal logic
- Multi-language support inspired by cross-cultural reasoning research
- Educational features designed for logic pedagogy
- Strength analysis based on argumentation theory

## 📞 Support

For questions, issues, or contributions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review the demo scripts for usage examples

---

*This system represents a comprehensive tool for logical argument generation, combining advanced NLP techniques with pedagogical principles to create contextually appropriate, linguistically rich logical arguments across multiple languages and domains.*