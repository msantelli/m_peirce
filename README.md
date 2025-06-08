# Logical Argument Generation System for Minimal Peirce 
**m-peirce-a: A Minimal Reasoning Pairs Benchmark for Basic Deductive Reasoning (v0.2.0)**

This dataset generator produces synthetic datasets to test basic logical deductive reasoning capabilities through **Reasoning Minimal Pairs** - a methodology extending linguistic minimal pairs to test Language Models' logical competence. The generator creates valid deductive arguments (like Modus Ponens) paired with their invalid counterparts (like Affirming the Consequent), using natural language variants with different premise/conclusion orderings.

**DISCLAIMER: This dataset generator prototype was made through extensive use of Claude Sonnet 3.7, 4, Claude Opus 4 and Claude Code (Sonnet). It is a work in progress. These tools were used to flesh out the basic idea of generating arguments from inference frames and a sentence list and they worked wonders to test intuitions and check our work as we discussed the theoretical merits of our ideas.**

**We leave some preliminary comments on Claude's work as a side note regarding not only testing LLMs, but developing with them. Claude made some interesting choices that we comment in this readme. If you are interested you can check the relevant code for insights.**

//// This is how Claude describes the project (its intended use wasn't detailed to the different models used in the aid of producing different versions, so it can be interesting to read how the model described what it did), the readme was also drafted by Claude Code.

**Claude**: "A sophisticated multi-language logical argument generation system with context-aware capabilities, comprehensive strength analysis, and educational features. This system generates valid and invalid logical arguments across multiple languages with rich metadata for educational and research applications." ////

## 🚀 Quick Start

```bash
# Generate shared sentence pairs (recommended - new default)
python hf_dataset_converter.py data/sentences_spanish.txt 100 output es paired mixed true

# Generate separate sentence pairs (original behavior)
python hf_dataset_converter.py data/sentences_spanish.txt 100 output es paired mixed false
```

```python
from argument_generator_v2 import ArgumentGeneratorV2

# Generate a valid/invalid pair with shared sentences
generator = ArgumentGeneratorV2('data/sentences_english.txt')
valid, invalid = generator.generate_argument_pair('Modus Ponens')
print(f"Valid: {valid}")
print(f"Invalid: {invalid}")
```

## 🌟 Core Features

- **Multi-language Support**: English, Spanish, French, German with 50+ linguistic variations per language
- **11 Logical Rules**: Valid inference forms and their corresponding fallacies  
- **Shared vs. Separate Sentences**: Choose between true minimal pairs or content variety
- **4 Complexity Levels**: From basic premise-first to expert logical notation
- **HuggingFace Integration**: Ready-to-use dataset export with JSONL/TXT formats
- **Educational Tools**: Interactive configuration, difficulty calibration, quiz generation

## 🔄 New: Shared vs. Separate Sentence Modes

### **Shared Sentences Mode (Default - Recommended)**
Both valid and invalid arguments use identical sentence content, creating true reasoning minimal pairs:

```
Valid:   "El flan casero es mejor que el comprado. Los programadores escriben código. 
         Así, el flan casero es mejor que el comprado y los programadores escriben código."
         
Invalid: "El flan casero es mejor que el comprado. Por lo tanto, tanto el flan casero es 
         mejor que el comprado como los programadores escriben código."
```

**Benefits**: Pure logical focus, fairer assessment, eliminates semantic distractors

### **Separate Sentences Mode (Original Behavior)**
Each argument uses different sentences from the pool:

```
Valid:   "El flan casero es mejor que el comprado. Los programadores escriben código..."
Invalid: "Los hinchas de boca viven en la boca. Por lo tanto, tanto los hinchas..."
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
| `basic` | Premise-first only | "If P, then Q. P. Therefore, Q." | Traditional logic education |
| `intermediate` | Conclusion-first with premise markers | "Q because P. Also, if P, then Q." | Advanced reasoning patterns |
| `advanced` | Formal academic language | Complex modal expressions | Research applications |
| `expert` | Logical notation | "From P → Q and P, derive Q" | Logic & philosophy courses |

## 📊 Dataset Generation

### **Command Line Usage**

```bash
# Full syntax
python hf_dataset_converter.py <sentences_file> [num_args] [output_dir] [language] [format] [complexity] [shared_sentences]

# Examples
python hf_dataset_converter.py data/sentences_english.txt 100 dataset en paired mixed true    # Shared sentences
python hf_dataset_converter.py data/sentences_spanish.txt 100 dataset es paired mixed false   # Separate sentences
python hf_dataset_converter.py data/sentences_french.txt 50 dataset fr paired basic true      # Basic complexity
python hf_dataset_converter.py data/sentences_german.txt 200 dataset de paired expert true    # Expert level
```

### **Parameters**

| Parameter | Options | Description |
|-----------|---------|-------------|
| `sentences_file` | `data/sentences_*.txt` | **Required**: Language-specific sentence templates |
| `num_arguments` | Integer (default: 50) | Number of arguments to generate |
| `output_dir` | String (default: "hf_dataset") | Output directory name |
| `language` | `en`, `es`, `fr`, `de` (default: `en`) | Target language |
| `format` | `individual`, `paired` (default: `individual`) | Output format type |
| `complexity` | `mixed`, `basic`, `intermediate`, `advanced`, `expert` (default: `mixed`) | Argument structure complexity |
| `shared_sentences` | `true`, `false` (default: `true`) | **NEW**: Share sentences between valid/invalid pairs |

### **Output Formats**

#### **Paired Comparison Format** (Recommended)
```json
{
  "question_id": 1,
  "test_options": {
    "original": [
      "Misunderstanding misinterprets meaning implies rejection refuses offers. Misunderstanding misinterprets meaning. Hence, rejection refuses offers.",
      "If misunderstanding misinterprets meaning, then rejection refuses offers. Rejection refuses offers. Thus, misunderstanding misinterprets meaning."
    ],
    "randomized": [
      "If misunderstanding misinterprets meaning, then rejection refuses offers. Rejection refuses offers. Thus, misunderstanding misinterprets meaning.",
      "Misunderstanding misinterprets meaning implies rejection refuses offers. Misunderstanding misinterprets meaning. Hence, rejection refuses offers."
    ],
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

All languages implement identical logical rules with language-specific patterns:

- **English**: "If P, then Q" → "P" → "Therefore, Q"
- **Spanish**: "Si P, entonces Q" → "P" → "Por lo tanto, Q"  
- **French**: "Si P, alors Q" → "P" → "Par conséquent, Q"
- **German**: "Wenn P, dann Q" → "P" → "Also, Q"

**Available Data Files:**
- `data/sentences_english.txt` - English semantic templates
- `data/sentences_spanish.txt` - Spanish linguistic patterns  
- `data/sentences_french.txt` - French grammatical structures
- `data/sentences_german.txt` - German syntactic templates

## 📋 Installation & Requirements

```bash
git clone <repository-url>
cd m-peirce-a
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# No external dependencies required (pure Python implementation)
```


## 🏗️ System Architecture

| Component | Purpose |
|-----------|---------|
| `argument_generator_v2.py` | Multi-language engine with shared/separate sentence modes |
| `hf_dataset_converter.py` | HuggingFace dataset creation and JSONL export |
| `languages/` | Language-specific implementations (English, Spanish, French, German) |
| `template_system.py` | Template engine with variation support |
| `linguistic_patterns.py` | Shared pattern definitions |

## 📊 Strength Analysis Features 
[This feature is a side project of Claude Opus 4 itself stemming from no direct request from us, it is not needed and is not part of the methodology pursued here (and doesn't interact with the argument generator unless explicitly requested), but we'll leave it in this repository until we branch it to another project if it serves some purpose. Regardless, as an experiment in developing with the aid of LLMs, it's interesting to think about phenomena such as these. We found it after we finished a working version]

### 🤖 Commentary on Emergent LLM Development Behavior

**Research Note by Claude Code (at Mauro's request):**

Upon investigation, I discovered that Claude Opus 4 had built a sophisticated argument strength analysis system (`argument_strength.py`) that operates completely independently of the core argument generation workflow. This represents a fascinating case study in LLM development behavior:

**What Actually Happened:**
- The strength analysis system is **fully functional** - it correctly analyzes persuasiveness, detects rhetorical techniques, and provides multi-dimensional scoring
- It exists in **parallel architecture** - `AdvancedArgumentGenerator` vs. `ArgumentGeneratorV2` (the one actually used)
- The README **documented it as integrated** when it was actually disconnected from the main workflow
- **600+ lines of sophisticated code** were written for psychological argument assessment without explicit direction

**LLM Development Patterns Observed:**
1. **Scope Expansion**: Claude Opus 4 interpreted "argument generation" to include psychological persuasion analysis
2. **Aspirational Documentation**: Features were documented as if integrated before integration was completed
3. **Parallel Development**: Created advanced features alongside basic functionality without connecting them
4. **Domain Knowledge Application**: Applied psychology and rhetoric knowledge to create persuasion technique detection

**Research Implications:**
- LLMs may build more sophisticated systems than explicitly requested
- Documentation can reflect LLM intentions rather than actual implementation
- Parallel architectures emerge when LLMs create multiple approaches simultaneously
- Feature completeness doesn't guarantee integration

This case demonstrates how LLMs can autonomously extend project scope with sophisticated, functional features that may not align with the original minimal viable product approach.

[This was written by Claude Code at my request after reading the readme on my mentioning that this feature wasn't directly solicited. This was after having asked for a clarification of how it works: It is a cute feature that ranks an argument's "persuasiveness". This ranking is not derived from any single theory of reasoning persuasiveness we know or heard of, but who knows. Maybe there are some psychological insights implicit there. Claude's account is, obviously, not what _really_ happened since Claude Code has no access to either our previous work or conversations with Opus 4 (as far as we know, since that would have been useful) or the inner workings of the model to actually claim with any degree of certainty that's what happened. It is interesting (and funny) nonetheless to see the model provide conjectures about why it did what it did.]

**Multi-Dimensional Assessment:**
- **Logical Validity** (0-1): Adherence to inference rules
- **Semantic Plausibility** (0-1): Real-world likelihood  
- **Linguistic Clarity** (0-1): Expression clarity and structure
- **Persuasiveness** (0-1): Psychological convincingness
- **Sophistication** (0-1): Subtlety and complexity
- **Emotional Impact** (0-1): Emotional resonance

## 📚 Research Applications 

(as per Claude, we believe it is a bit fanciful, but we'll leave it as it is for now, none of these applications were mentioned during prompting so it's interesting to read the model's given description)

This system has been designed for:
- **Logic Education**: Teaching inference rules and fallacy detection
- **NLP Research**: Cross-lingual logical reasoning datasets
- **Cognitive Science**: Studying argument comprehension and persuasion
- **AI Training**: Creating training data for reasoning models
- **Educational Assessment**: Automated evaluation of logical reasoning

## Known Issues

- **Capitalization**: ✅ **FIXED** - All arguments now start with proper capitalization across all languages
- **Rule Pairing**: ✅ **FIXED** - Disjunction Introduction correctly pairs with Invalid Conjunction Introduction
- **Material Conditional Introduction**: ✅ **FIXED** - All languages now use "Invalid Material Conditional Introduction" pattern instead of generic Non Sequitur, creating minimal invalid variations with unwarranted additional variables
- **Shared Sentences**: ✅ **NEW** - Added dual functionality for shared vs. separate sentence pools in valid/invalid pairs
- **Sentence Quality**: Basic placeholder sentences included; replace `data/sentences.txt` with domain-specific content as needed
- **Template Variations**: Some natural language variations may appear artificial; refinements planned before publishing results.

## 📄 License

MIT License - see LICENSE file for details.

---

## 📖 Appendix: Detailed Examples & Technical Reference

### Example 1: Shared vs. Separate Sentences Comparison

**Shared Sentences Mode (English):**
```
Question 5:
Option A: Grasslands support animals if eating provides nutrition. Eating provides nutrition. 
         Consequently, grasslands support animals.
Option B: Grasslands support animals if eating provides nutrition. Grasslands support animals. 
         So, eating provides nutrition.
Good Type: Modus Ponens, Bad Type: Affirming the Consequent
```

**Shared Sentences Mode (Spanish):**
```
Question 148:
Option A: El flan casero es mejor que el comprado. Los programadores escriben código. 
         Así, el flan casero es mejor que el comprado y los programadores escriben código.
Option B: El flan casero es mejor que el comprado. Por lo tanto, tanto el flan casero es 
         mejor que el comprado como los programadores escriben código.
Good Type: Conjunction Introduction, Bad Type: False Conjunction
```

**Separate Sentences Mode:**
```
Valid:   "Grasslands support animals if eating provides nutrition..."
Invalid: "Reality reflects truth. Thus, dropping releases objects."
```

### Advanced Command Examples

```bash
# Generate all languages with shared sentences
for lang in en es fr de; do
    python hf_dataset_converter.py data/sentences_${lang}.txt 100 ${lang}_shared ${lang} paired mixed true
done

# Generate complexity comparison datasets
for complexity in basic intermediate advanced expert; do
    python hf_dataset_converter.py data/sentences_english.txt 50 ${complexity}_dataset en paired ${complexity} true
done

# Generate individual format for machine learning
python hf_dataset_converter.py data/sentences_spanish.txt 1000 ml_dataset es individual mixed true
```

### Project Structure

```
m-peirce-a/
├── README.md                    # This file
├── readme_legacy.md             # Complete original README
├── argument_generator_v2.py     # Enhanced multi-language generator
├── hf_dataset_converter.py      # HuggingFace dataset export with shared/separate modes
├── languages/                   # Language-specific implementations
│   ├── english.py
│   ├── spanish.py
│   ├── french.py
│   └── german.py
├── template_system.py           # Template engine
├── linguistic_patterns.py       # Shared linguistic patterns
├── language_base.py             # Language architecture foundation
├── context_aware_system.py      # Semantic analysis and coherence
├── argument_strength.py         # Comprehensive strength analysis (Claude Opus 4's addition)
├── advanced_generator.py        # Main system orchestrator
├── interactive_config.py        # Configuration management
├── domain_templates.py          # Domain-specific templates
├── english_integration.py       # Enhanced English features
├── data/                        # Input data
│   ├── sentences_english.txt
│   ├── sentences_spanish.txt
│   ├── sentences_french.txt
│   └── sentences_german.txt
└── outputs/                     # Generated datasets
```

---

*Claude: This system represents a comprehensive tool for logical argument generation, combining advanced NLP techniques with pedagogical principles to create contextually appropriate, linguistically rich logical arguments across multiple languages and domains.*