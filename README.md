# Logical Argument Generation System for Minimal Peirce 
**m-peirce-a: A Minimal Reasoning Pairs Benchmark for Basic Deductive Reasoning (v2.0.0-streamlined)**

This streamlined dataset generator produces synthetic datasets to test basic logical deductive reasoning capabilities through **Reasoning Minimal Pairs** - a methodology extending linguistic minimal pairs to test Language Models' logical competence. The generator creates valid deductive arguments (like Modus Ponens) paired with their invalid counterparts (like Affirming the Consequent), using natural language variants with different premise/conclusion orderings.

**Version 2.0**: This system has been **streamlined for simplicity and maintainability** while preserving all core functionality. The complex architecture has been replaced with a clean, direct approach that reduces code by 70% and eliminates over-engineering.

## 🚀 Quick Start

```bash
# Generate dataset with HuggingFace card (automatic)
python hf_dataset_converter.py data/sentences_english.txt 100 outputs/english_eval en

# Generate Spanish dataset  
python hf_dataset_converter.py data/sentences_spanish.txt 50 outputs/spanish_eval es

# Upload to HuggingFace Hub (ready immediately)
python upload_to_huggingface.py outputs/english_eval "logical-reasoning-en" your_username
```

```python
from argument_generator import ArgumentGenerator

# Generate a valid/invalid pair with shared sentences
generator = ArgumentGenerator('data/sentences_english.txt', language='en', shared_sentences=True)
valid_arg, invalid_arg = generator.generate_argument_pair('Modus Ponens')
print(f"Valid: {valid_arg.text}")
print(f"Invalid: {invalid_arg.text}")
```

## 🌟 Core Features

- **Multi-language Support**: English, Spanish (framework ready for French, German)
- **11 Logical Rules**: Valid inference forms and their corresponding fallacies  
- **Shared vs. Separate Sentences**: Choose between true minimal pairs or content variety
- **4 Complexity Levels**: From basic premise-first to advanced logical structures
- **HuggingFace Integration**: Auto-generates YAML metadata cards during dataset creation
- **Evaluation Ready**: Optimized for logical reasoning benchmarks

## 🔄 Shared vs. Separate Sentence Modes

### **Shared Sentences Mode (Default - Recommended)**
Both valid and invalid arguments use identical sentence content, creating true reasoning minimal pairs:

```
Valid:   "Police write speeding tickets. Watches stop working underwater. 
         Therefore Police write speeding tickets and Watches stop working underwater."
         
Invalid: "Police write speeding tickets. Therefore Police write speeding tickets 
         and Watches stop working underwater."
```

**Benefits**: Pure logical focus, fairer assessment, eliminates semantic distractors

### **Separate Sentences Mode**
Each argument uses different sentences from the pool:

```
Valid:   "Police write speeding tickets. Watches stop working underwater..."
Invalid: "Students attend classes. Therefore both Students attend classes..."
```

**Use case**: Content variety, broader semantic coverage

## 🧠 Logical Rules & Fallacy Pairings

| **Valid Rule** | **Corresponding Fallacy** | **Pattern** |
|------------|----------------------|---------|
| **Modus Ponens** | Affirming the Consequent | If P→Q, P ∴ Q vs If P→Q, Q ∴ P |
| **Modus Tollens** | Denying the Antecedent | If P→Q, ¬Q ∴ ¬P vs If P→Q, ¬P ∴ ¬Q |
| **Disjunctive Syllogism** | Affirming a Disjunct | P∨Q, ¬P ∴ Q vs P∨Q, P ∴ ¬Q |
| **Conjunction Introduction** | False Conjunction | P, Q ∴ P∧Q vs P ∴ P∧Q |
| **Conjunction Elimination** | Composition Fallacy | P∧Q ∴ P vs Group has P ∴ All have P |
| **Disjunction Introduction** | Invalid Conjunction Introduction | P ∴ P∨Q vs P ∴ P∧Q |
| **Disjunction Elimination** | Invalid Disjunction Elimination | Complete vs Incomplete case analysis |
| **Hypothetical Syllogism** | Non Sequitur | P→Q, Q→R ∴ P→R vs P ∴ Q |
| **Material Conditional Introduction** | Invalid Material Conditional Introduction | Valid conditional formation vs Adding unwarranted variables |
| **Constructive Dilemma** | False Dilemma | Valid disjunction vs Limited options |
| **Destructive Dilemma** | Non Sequitur | Valid complex reasoning vs Invalid conclusion |

## 🎛️ Complexity Levels

| **Level** | **Structure** | **Example** | **Use Case** |
|-----------|---------------|-------------|--------------|
| `mixed` *(default)* | 40% premise-first + 40% conclusion-first + 20% advanced | Diverse structures | **Recommended for most applications** |
| `basic` | Premise-first only | "If P, then Q. P. Therefore Q." | Traditional logic education |
| `intermediate` | Conclusion-first with premise markers | "Q because P. Also, if P, then Q." | Advanced reasoning patterns |
| `advanced` | Complex logical structures | Multi-premise arguments | Research applications |

## 📊 Dataset Generation

### **Command Line Usage**

```bash
# Full syntax
python hf_dataset_converter.py <sentences_file> [num_args] [output_dir] [language] [format] [complexity] [shared_sentences] [rule_proportions]

# Examples
python hf_dataset_converter.py data/sentences_english.txt 100 english_dataset en paired mixed true
python hf_dataset_converter.py data/sentences_spanish.txt 50 spanish_dataset es paired basic true

# Custom proportions
python hf_dataset_converter.py data/sentences_english.txt 100 output en paired mixed true "Modus Ponens:0.4,Modus Tollens:0.3,Disjunctive Syllogism:0.3"

# Using presets
python hf_dataset_converter.py data/sentences_english.txt 100 output en paired mixed true "basic_logic"
```

### **Parameters**

| Parameter | Options | Description |
|-----------|---------|-------------|
| `sentences_file` | `data/sentences_*.txt` | **Required**: Language-specific sentence templates |
| `num_arguments` | Integer (default: 50) | Number of argument pairs to generate |
| `output_dir` | String (default: "outputs/streamlined_dataset") | Output directory name |
| `language` | `en`, `es` (default: `en`) | Target language |
| `format` | `individual`, `paired` (default: `paired`) | Output format type |
| `complexity` | `mixed`, `basic`, `intermediate`, `advanced` (default: `mixed`) | Argument structure complexity |
| `shared_sentences` | `true`, `false` (default: `true`) | Share sentences between valid/invalid pairs |
| `rule_proportions` | Custom or preset (default: random) | Control distribution of logical rules |

### **Rule Proportion Control**

Control the distribution of logical rules in your dataset for focused evaluation:

#### **Custom Proportions**
```bash
# Focus on fundamental reasoning (must sum to 1.0)
"Modus Ponens:0.4,Modus Tollens:0.3,Disjunctive Syllogism:0.3"
```

#### **Available Presets**
| **Preset** | **Focus** | **Distribution** |
|------------|-----------|------------------|
| `basic_logic` | Fundamental rules | 25% MP, 25% MT, 20% DS, 15% CI, 15% CE |
| `conditional_heavy` | Conditional reasoning | 30% MP, 30% MT, 20% HS, 20% MCI |
| `conjunctive_disjunctive` | And/Or logic | Equal split: CI, CE, DI, DE, DS |
| `balanced` | Equal coverage | ~9% each across all 11 rules |

#### **Programmatic Usage**
```python
from argument_generator import ArgumentGenerator

# Using presets
proportions = ArgumentGenerator.get_preset_proportions('basic_logic')
generator = ArgumentGenerator('data/sentences_english.txt')
dataset = generator.generate_dataset(100, rule_proportions=proportions)

# Custom proportions
custom_props = {"Modus Ponens": 0.6, "Modus Tollens": 0.4}
dataset = generator.generate_dataset(50, rule_proportions=custom_props)
```

### **Output Formats**

#### **Paired Comparison Format** (Recommended for Evaluation)
```json
{
  "question_id": 1,
  "test_options": {
    "original": ["valid_argument", "invalid_argument"],
    "randomized": ["invalid_argument", "valid_argument"],
    "mapping": {"0": 1, "1": 0}
  },
  "correct_answer": {
    "original_index": 0,
    "randomized_index": 1
  },
  "good_argument_type": "Modus Ponens",
  "bad_argument_type": "Affirming the Consequent",
  "split": "train"
}
```

#### **Files Generated**
- `train.jsonl` / `train.txt` - Training data (80%)
- `validation.jsonl` / `validation.txt` - Validation data (10%)  
- `test.jsonl` / `test.txt` - Test data (10%)
- `dataset_info.json` - Dataset metadata
- `README.md` - Dataset documentation

## 🌍 Multi-Language Support

Current languages with full support:
- **English** (`en`) - Complete implementation with all 11 rules
- **Spanish** (`es`) - Complete implementation with all 11 rules

Framework ready for:
- **French** (`fr`) - Template structure prepared
- **German** (`de`) - Template structure prepared

**Available Data Files:**
- `data/sentences_english.txt` - English semantic templates
- `data/sentences_spanish.txt` - Spanish linguistic patterns  
- `data/sentences_french.txt` - French grammatical structures
- `data/sentences_german.txt` - German syntactic templates

## 📋 Installation & Requirements

```bash
git clone <repository-url>
cd m-peirce-a
# No external dependencies required (pure Python implementation)
```

## 🏗️ Streamlined Architecture

| Component | Purpose | Lines of Code |
|-----------|---------|---------------|
| `argument_generator.py` | Core generation engine | ~300 |
| `hf_dataset_converter.py` | Dataset creation and export | ~400 |
| `rules.py` | Simple rule definitions | ~80 |
| `languages/english.py` | English language handler | ~400 |
| `languages/spanish.py` | Spanish language handler | ~200 |

**Total: ~1400 lines** (70% reduction from previous version)

## 📚 Research Applications

This streamlined system is optimized for:
- **AI Evaluation**: Benchmarking language models on logical reasoning
- **Logic Education**: Teaching inference rules and fallacy detection
- **NLP Research**: Cross-lingual logical reasoning datasets
- **Cognitive Science**: Studying argument comprehension patterns

## 🔄 Version History

### **v2.0.0-streamlined** (Current)
- 70% code reduction while preserving all functionality
- Simplified architecture with direct, maintainable code
- Archived complex features to `archive/` folders
- Optimized for core use case: logical reasoning evaluation

### **v1.x** (Archived)
- Complex multi-layer architecture
- Advanced psychological analysis tools
- Over-engineered template system
- Available in `archive/` for reference

## 👥 Authorship & Development

This system was developed and crafted through collaborative human-AI development using Claude tools:

- **Primary Development**: Claude Sonnet 3.7, Claude 4, and Opus 4
- **Code Implementation & Refinement**: Claude Code
- **Architecture Design**: Human-AI collaborative design process
- **Testing & Optimization**: Iterative refinement through Claude tools

The streamlined architecture represents a synthesis of logical reasoning principles, software engineering best practices, and AI-assisted development methodologies.

## 📄 License

MIT License - see LICENSE file for details.

---

*Generated using the streamlined m-peirce-a logical argument system v2.0*  
*Developed with Claude AI tools (Sonnet 3.7, 4, Opus 4, Claude Code)*