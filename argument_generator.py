"""
argument_generator.py

Streamlined argument generator for logical reasoning datasets.
Replaces the complex multi-layer architecture with a simple, direct approach.
"""

import random
import json
from typing import List, Dict, Tuple, Optional, Any
from pathlib import Path
from dataclasses import dataclass

from rules import LOGICAL_RULES, get_rule_definition, get_all_rules
from languages.english import EnglishHandler
from languages.spanish import SpanishHandler


@dataclass 
class GeneratedArgument:
    """Simple container for a generated argument."""
    text: str
    rule_type: str
    is_valid: bool
    language: str
    sentences_used: List[str]
    metadata: Dict[str, Any] = None


class ArgumentGenerator:
    """Streamlined argument generator with minimal complexity."""
    
    def __init__(self, 
                 sentences_file: str,
                 language: str = "en",
                 shared_sentences: bool = True):
        """
        Initialize the streamlined generator.
        
        Args:
            sentences_file: Path to sentences file
            language: Language code ('en', 'es', 'fr', 'de')
            shared_sentences: Whether valid/invalid pairs share sentences
        """
        self.sentences = self._load_sentences(sentences_file)
        self.language_code = language
        self.shared_sentences = shared_sentences
        
        # Initialize language handler
        self.language_handler = self._get_language_handler(language)
        
        # Simple configuration
        self.config = {
            'style': 'basic',  # basic, formal, casual
            'complexity': 'mixed'  # basic, intermediate, advanced, mixed
        }
    
    def _load_sentences(self, sentences_file: str) -> List[str]:
        """Load sentences from file."""
        try:
            with open(sentences_file, 'r', encoding='utf-8') as f:
                sentences = [line.strip() for line in f if line.strip()]
            
            if not sentences:
                raise ValueError(f"No sentences found in {sentences_file}")
            
            # Ensure sentences are properly formatted
            formatted_sentences = []
            for sentence in sentences:
                sentence = sentence.strip().rstrip('.!?')
                if sentence:
                    formatted_sentences.append(sentence)
            
            return formatted_sentences
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Sentences file not found: {sentences_file}")
    
    def _get_language_handler(self, language: str):
        """Get the appropriate language handler."""
        handlers = {
            'en': EnglishHandler,
            'es': SpanishHandler,
            # 'fr': FrenchHandler,  # Can be added later
            # 'de': GermanHandler   # Can be added later
        }
        
        if language not in handlers:
            raise ValueError(f"Unsupported language: {language}. Supported: {list(handlers.keys())}")
        
        return handlers[language]()
    
    def select_sentences(self, count: int, exclude: List[str] = None) -> List[str]:
        """Select random sentences, optionally excluding some."""
        available = [s for s in self.sentences if s not in (exclude or [])]
        
        if len(available) < count:
            # If not enough unique sentences, allow repeats
            available = self.sentences
        
        return random.sample(available, min(count, len(available)))
    
    def _lowercase_sentence(self, sentence: str) -> str:
        """Convert sentence to lowercase unless it starts with a proper noun."""
        if not sentence:
            return sentence
        
        # Simple proper noun detection
        proper_indicators = ['I ', 'I\'', 'Mr.', 'Mrs.', 'Dr.']
        if any(sentence.startswith(indicator) for indicator in proper_indicators):
            return sentence
            
        return sentence[0].lower() + sentence[1:] if len(sentence) > 1 else sentence.lower()
    
    def _to_lowercase(self, sentence: str) -> str:
        """Convert sentence to lowercase unless it starts with a proper noun."""
        if not sentence:
            return sentence
        
        # Keep "I" capitalized, lowercase everything else
        if sentence.startswith('I ') or sentence == 'I':
            return sentence
            
        return sentence[0].lower() + sentence[1:] if len(sentence) > 1 else sentence.lower()
    
    def prepare_sentence_variables(self, sentences: List[str], rule_name: str) -> Dict[str, str]:
        """Prepare sentence variables for template substitution."""
        rule_def = get_rule_definition(rule_name)
        variables = {}
        
        # Create both capitalized and lowercase versions of sentence variables
        if len(sentences) >= 1:
            formatted = self.language_handler.format_sentence(sentences[0])
            variables['P'] = formatted  # Capitalized for sentence starts
            variables['p'] = self._to_lowercase(formatted)  # Lowercase for mid-sentence
            variables['premise'] = variables['P']  # Default to capitalized
            variables['Premise'] = variables['P']
        
        if len(sentences) >= 2:
            formatted = self.language_handler.format_sentence(sentences[1])
            variables['Q'] = formatted  # Capitalized for sentence starts
            variables['q'] = self._to_lowercase(formatted)  # Lowercase for mid-sentence  
            variables['result'] = variables['Q']  # Default to capitalized
            variables['Result'] = variables['Q']
        
        if len(sentences) >= 3:
            formatted = self.language_handler.format_sentence(sentences[2])
            variables['R'] = formatted  # Capitalized for sentence starts
            variables['r'] = self._to_lowercase(formatted)  # Lowercase for mid-sentence
        
        # Create compound statements based on rule type (both capitalized and lowercase versions)
        if rule_def.template_type == "conditional":
            cap_conditional = self.language_handler.create_conditional(
                variables['P'], variables['Q'], self.config['style']
            )
            variables['Conditional'] = cap_conditional
            variables['conditional'] = self._to_lowercase(cap_conditional)
            
        elif rule_def.template_type == "conditional_negation":
            cap_conditional = self.language_handler.create_conditional(
                variables['P'], variables['Q'], self.config['style']
            )
            variables['Conditional'] = cap_conditional
            variables['conditional'] = self._to_lowercase(cap_conditional)
            
        elif rule_def.template_type == "conjunction":
            if len(sentences) >= 2:
                cap_conjunction = self.language_handler.create_conjunction(
                    variables['P'], variables['Q'], self.config['style']
                )
                variables['Conjunction'] = cap_conjunction
                variables['conjunction'] = self._to_lowercase(cap_conjunction)
        
        elif rule_def.template_type == "conjunction_elimination":
            if len(sentences) >= 2:
                cap_conjunction = self.language_handler.create_conjunction(
                    variables['P'], variables['Q'], self.config['style']
                )
                variables['Conjunction'] = cap_conjunction
                variables['conjunction'] = self._to_lowercase(cap_conjunction)
        
        elif rule_def.template_type == "disjunctive":
            if len(sentences) >= 2:
                cap_disjunction = self.language_handler.create_disjunction(
                    variables['P'], variables['Q'], 'inclusive'
                )
                variables['Disjunction'] = cap_disjunction
                variables['disjunction'] = self._to_lowercase(cap_disjunction)
        
        elif rule_def.template_type == "disjunction_intro":
            if len(sentences) >= 2:
                cap_disjunction = self.language_handler.create_disjunction(
                    variables['P'], variables['Q'], 'inclusive'
                )
                variables['Disjunction'] = cap_disjunction
                variables['disjunction'] = self._to_lowercase(cap_disjunction)
                
                cap_conjunction = self.language_handler.create_conjunction(
                    variables['P'], variables['Q'], self.config['style']
                )
                variables['Conjunction'] = cap_conjunction
                variables['conjunction'] = self._to_lowercase(cap_conjunction)
        
        elif rule_def.template_type == "disjunction_elimination":
            if len(sentences) >= 2:
                cap_disjunction = self.language_handler.create_disjunction(
                    variables['P'], variables['Q'], 'inclusive'
                )
                variables['Disjunction'] = cap_disjunction
                variables['disjunction'] = self._to_lowercase(cap_disjunction)
        
        elif rule_def.template_type == "hypothetical":
            if len(sentences) >= 3:
                cap_cond1 = self.language_handler.create_conditional(
                    variables['P'], variables['Q'], self.config['style']
                )
                cap_cond2 = self.language_handler.create_conditional(
                    variables['Q'], variables['R'], self.config['style']
                )
                cap_cond3 = self.language_handler.create_conditional(
                    variables['P'], variables['R'], self.config['style']
                )
                variables['Conditional1'] = cap_cond1
                variables['conditional1'] = self._to_lowercase(cap_cond1)
                variables['Conditional2'] = cap_cond2
                variables['conditional2'] = self._to_lowercase(cap_cond2)
                variables['Conditional3'] = cap_cond3
                variables['conditional3'] = self._to_lowercase(cap_cond3)
        
        elif rule_def.template_type == "material_conditional":
            if len(sentences) >= 3:
                cap_conditional = self.language_handler.create_conditional(
                    variables['P'], variables['Q'], self.config['style']
                )
                variables['Conditional'] = cap_conditional
                variables['conditional'] = self._to_lowercase(cap_conditional)
        
        elif rule_def.template_type == "constructive_dilemma":
            if len(sentences) >= 3:
                cap_cond1 = self.language_handler.create_conditional(
                    variables['P'], variables['R'], self.config['style']
                )
                cap_cond2 = self.language_handler.create_conditional(
                    variables['Q'], variables['R'], self.config['style']
                )
                cap_disjunction = self.language_handler.create_disjunction(
                    variables['P'], variables['Q'], 'inclusive'
                )
                variables['Conditional1'] = cap_cond1
                variables['conditional1'] = self._to_lowercase(cap_cond1)
                variables['Conditional2'] = cap_cond2
                variables['conditional2'] = self._to_lowercase(cap_cond2)
                variables['Disjunction'] = cap_disjunction
                variables['disjunction'] = self._to_lowercase(cap_disjunction)
        
        elif rule_def.template_type == "destructive_dilemma":
            if len(sentences) >= 3:
                cap_cond1 = self.language_handler.create_conditional(
                    variables['P'], variables['R'], self.config['style']
                )
                cap_cond2 = self.language_handler.create_conditional(
                    variables['Q'], variables['R'], self.config['style']
                )
                cap_neg_result = self.language_handler.negate_sentence(
                    variables['R'], self.config['style']
                )
                variables['Conditional1'] = cap_cond1
                variables['conditional1'] = self._to_lowercase(cap_cond1)
                variables['Conditional2'] = cap_cond2
                variables['conditional2'] = self._to_lowercase(cap_cond2)
                variables['Negated_result1'] = cap_neg_result
                variables['negated_result1'] = self._to_lowercase(cap_neg_result)
                variables['Negated_result2'] = cap_neg_result
                variables['negated_result2'] = self._to_lowercase(cap_neg_result)
        
        # Create negated versions (both capitalized and lowercase)
        if 'P' in variables:
            cap_neg_p = self.language_handler.negate_sentence(
                variables['P'], self.config['style']
            )
            variables['Negated_p'] = cap_neg_p
            variables['negated_p'] = self._to_lowercase(cap_neg_p)
            variables['Negated_premise'] = cap_neg_p
            variables['negated_premise'] = self._to_lowercase(cap_neg_p)
        
        if 'Q' in variables:
            cap_neg_q = self.language_handler.negate_sentence(
                variables['Q'], self.config['style']
            )
            variables['Negated_q'] = cap_neg_q
            variables['negated_q'] = self._to_lowercase(cap_neg_q)
            variables['Negated_result'] = cap_neg_q
            variables['negated_result'] = self._to_lowercase(cap_neg_q)
        
        # Add conclusion marker
        variables['conclusion'] = self.language_handler.get_conclusion_marker(self.config['style'])
        
        return variables
    
    def generate_argument(self, rule_name: str, is_valid: bool = True, 
                         sentences: List[str] = None) -> GeneratedArgument:
        """Generate a single argument for the given rule."""
        rule_def = get_rule_definition(rule_name)
        if not rule_def:
            raise ValueError(f"Unknown rule: {rule_name}")
        
        # Select sentences if not provided
        if sentences is None:
            sentences = self.select_sentences(rule_def.sentences_needed)
        
        # Prepare variables for template substitution
        variables = self.prepare_sentence_variables(sentences, rule_name)
        
        # Get templates for this rule
        templates = self.language_handler.generate_templates(rule_name, is_valid)
        
        if not templates:
            raise ValueError(f"No templates found for {rule_name} (valid={is_valid})")
        
        # Choose template style based on complexity setting
        if self.config['complexity'] == 'mixed':
            template_style = random.choice(['premise_first', 'conclusion_first'])
        elif self.config['complexity'] == 'basic':
            template_style = 'premise_first'
        else:
            template_style = random.choice(list(templates.keys()))
        
        # Select and render template
        if template_style in templates:
            template = random.choice(templates[template_style])
            try:
                argument_text = template.format(**variables)
            except KeyError as e:
                # Fallback if template variable is missing
                print(f"Warning: Missing variable {e} in template for {rule_name}")
                argument_text = template  # Return template as-is for debugging
        else:
            argument_text = f"Template not found for {rule_name} ({template_style})"
        
        # Determine rule type name
        actual_rule_name = rule_def.valid_name if is_valid else rule_def.invalid_name
        
        return GeneratedArgument(
            text=argument_text,
            rule_type=actual_rule_name,
            is_valid=is_valid,
            language=self.language_code,
            sentences_used=sentences,
            metadata={
                'template_style': template_style,
                'variables_used': list(variables.keys()),
                'base_rule': rule_name
            }
        )
    
    def generate_argument_pair(self, rule_name: str) -> Tuple[GeneratedArgument, GeneratedArgument]:
        """Generate a valid/invalid argument pair."""
        rule_def = get_rule_definition(rule_name)
        if not rule_def:
            raise ValueError(f"Unknown rule: {rule_name}")
        
        # Select sentences
        if self.shared_sentences:
            # Use same sentences for both arguments
            sentences = self.select_sentences(rule_def.sentences_needed)
            valid_sentences = sentences
            invalid_sentences = sentences
        else:
            # Use different sentences for each argument
            valid_sentences = self.select_sentences(rule_def.sentences_needed)
            invalid_sentences = self.select_sentences(rule_def.sentences_needed, exclude=valid_sentences)
        
        # Generate both arguments
        valid_arg = self.generate_argument(rule_name, is_valid=True, sentences=valid_sentences)
        invalid_arg = self.generate_argument(rule_name, is_valid=False, sentences=invalid_sentences)
        
        return valid_arg, invalid_arg
    
    def generate_dataset(self, num_pairs: int, rules: List[str] = None, rule_proportions: Dict[str, float] = None) -> List[Tuple[GeneratedArgument, GeneratedArgument]]:
        """
        Generate a dataset of argument pairs.
        
        Args:
            num_pairs: Number of pairs to generate
            rules: List of rules to use (default: all rules)
            rule_proportions: Dict mapping rule names to proportions (0.0-1.0)
                             If provided, must sum to 1.0. Example:
                             {"Modus Ponens": 0.3, "Modus Tollens": 0.2, ...}
        """
        if rules is None:
            rules = get_all_rules()
        
        # Handle rule proportions
        if rule_proportions:
            # Validate proportions
            if not abs(sum(rule_proportions.values()) - 1.0) < 0.001:
                raise ValueError("Rule proportions must sum to 1.0")
            
            # Check all specified rules exist
            invalid_rules = set(rule_proportions.keys()) - set(rules)
            if invalid_rules:
                raise ValueError(f"Unknown rules in proportions: {invalid_rules}")
            
            # Create weighted selection list
            weighted_rules = []
            for rule, proportion in rule_proportions.items():
                count = max(1, int(num_pairs * proportion))
                weighted_rules.extend([rule] * count)
            
            # Fill remaining slots with random rules if needed
            while len(weighted_rules) < num_pairs:
                weighted_rules.append(random.choice(rules))
            
            # Trim to exact count and shuffle
            weighted_rules = weighted_rules[:num_pairs]
            random.shuffle(weighted_rules)
            rule_sequence = weighted_rules
        else:
            # Random selection as before
            rule_sequence = [random.choice(rules) for _ in range(num_pairs)]
        
        dataset = []
        rule_counts = {}
        
        for i, rule_name in enumerate(rule_sequence):
            try:
                valid_arg, invalid_arg = self.generate_argument_pair(rule_name)
                dataset.append((valid_arg, invalid_arg))
                rule_counts[rule_name] = rule_counts.get(rule_name, 0) + 1
            except Exception as e:
                print(f"Warning: Failed to generate pair {i+1} for rule {rule_name}: {e}")
                continue
        
        # Print distribution summary
        if rule_proportions:
            print(f"Generated {len(dataset)} pairs with specified proportions:")
            for rule in sorted(rule_counts.keys()):
                actual_prop = rule_counts[rule] / len(dataset)
                target_prop = rule_proportions.get(rule, 0.0)
                print(f"  {rule}: {rule_counts[rule]} pairs ({actual_prop:.2%}, target: {target_prop:.1%})")
        
        return dataset
    
    @staticmethod
    def get_preset_proportions(preset_name: str) -> Dict[str, float]:
        """
        Get predefined rule proportion presets.
        
        Available presets:
        - 'basic_logic': Focus on fundamental rules (Modus Ponens, Modus Tollens, etc.)
        - 'conjunctive_disjunctive': Emphasis on conjunction/disjunction rules
        - 'conditional_heavy': Focus on conditional reasoning patterns
        - 'balanced': Equal distribution across all rules
        """
        presets = {
            'basic_logic': {
                'Modus Ponens': 0.25,
                'Modus Tollens': 0.25, 
                'Disjunctive Syllogism': 0.20,
                'Conjunction Introduction': 0.15,
                'Conjunction Elimination': 0.15
            },
            'conjunctive_disjunctive': {
                'Conjunction Introduction': 0.2,
                'Conjunction Elimination': 0.2,
                'Disjunction Introduction': 0.2,
                'Disjunction Elimination': 0.2,
                'Disjunctive Syllogism': 0.2
            },
            'conditional_heavy': {
                'Modus Ponens': 0.3,
                'Modus Tollens': 0.3,
                'Hypothetical Syllogism': 0.2,
                'Material Conditional Introduction': 0.2
            },
            'balanced': {rule: 1.0/11 for rule in get_all_rules()}
        }
        
        if preset_name not in presets:
            available = ', '.join(presets.keys())
            raise ValueError(f"Unknown preset: {preset_name}. Available: {available}")
        
        return presets[preset_name]
    
    def set_style(self, style: str):
        """Set generation style."""
        if style in ['basic', 'formal', 'casual']:
            self.config['style'] = style
        else:
            raise ValueError(f"Invalid style: {style}. Use 'basic', 'formal', or 'casual'")
    
    def set_complexity(self, complexity: str):
        """Set complexity level."""
        if complexity in ['basic', 'intermediate', 'advanced', 'mixed']:
            self.config['complexity'] = complexity
        else:
            raise ValueError(f"Invalid complexity: {complexity}. Use 'basic', 'intermediate', 'advanced', or 'mixed'")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get basic statistics about the generator."""
        return {
            'language': self.language_code,
            'sentence_count': len(self.sentences),
            'shared_sentences': self.shared_sentences,
            'supported_rules': len(LOGICAL_RULES),
            'config': self.config.copy()
        }