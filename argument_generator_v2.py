"""
argument_generator_v2.py

Refactored argument generator that uses the new variation-aware template system
and supports multiple languages.
"""

import random
import json
import os
from typing import List, Dict, Tuple, Optional, Any
from pathlib import Path

from linguistic_patterns import (
    VariationGenerator, ComplexityLevel, VariationType
)
from language_base import LanguageFactory, LanguageAdapter
from template_system import (
    TemplateBank, TemplateBuilder, VariationLibrary,
    EnhancedTemplate
)

# Import language modules to register them
from languages import english, spanish, french, german


class ArgumentGeneratorV2:
    """Enhanced argument generator with multi-language and variation support."""
    
    def __init__(self, 
                 sentences_file: str,
                 language: str = "en",
                 rule_mappings_file: Optional[str] = None,
                 flexible_mode: bool = False):
        """
        Initialize the enhanced argument generator.
        
        Args:
            sentences_file: Path to file containing sentences
            language: Language code (e.g., 'en', 'es', 'fr')
            rule_mappings_file: Optional custom rule mappings
            flexible_mode: Enable flexible invalid argument generation
        """
        self.sentences = self._load_sentences(sentences_file)
        self.language_code = language
        self.flexible_mode = flexible_mode
        
        # Initialize language adapter
        self.language_adapter = LanguageFactory.create_adapter(language)
        if not self.language_adapter:
            raise ValueError(f"Language '{language}' not supported")
        
        # Initialize variation generator
        self.variation_generator = VariationGenerator(self.language_adapter.pattern)
        
        # Initialize template bank
        self.template_bank = TemplateBank()
        self._load_templates()
        
        # Initialize variation library
        self.variation_library = VariationLibrary()
        
        # Load rule mappings
        self.rule_mappings = self._load_rule_mappings(rule_mappings_file)
        
        # Configuration
        self.config = {
            'complexity_level': ComplexityLevel.BASIC,
            'variation_preferences': {},
            'domain': 'general',
            'formality': 'neutral'
        }
    
    def _load_sentences(self, file_path: str) -> List[str]:
        """Load sentences from file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")
            return []
    
    def _load_rule_mappings(self, file_path: Optional[str]) -> Dict[str, str]:
        """Load rule mappings from file or use defaults."""
        # Default mappings
        default_mappings = {
            "Modus Ponens": "Affirming the Consequent",
            "Modus Tollens": "Denying the Antecedent",
            "Disjunctive Syllogism": "Affirming a Disjunct",
            "Conjunction Introduction": "False Conjunction",
            "Conjunction Elimination": "Composition Fallacy",
            "Disjunction Introduction": "Invalid Conjunction Introduction",
            "Hypothetical Syllogism": "Non Sequitur",
            "Disjunction Elimination": "Invalid Disjunction Elimination",
            "Material Conditional Introduction": "Invalid Material Conditional Introduction",
            "Constructive Dilemma": "False Dilemma",
            "Destructive Dilemma": "Non Sequitur"
        }
        
        if not file_path:
            return default_mappings
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading rule mappings: {e}")
            return default_mappings
    
    def _load_templates(self):
        """Load templates for the current language."""
        # Load templates from the language adapter
        if self.language_adapter and self.language_adapter.templates:
            for rule_name, rule_templates in self.language_adapter.templates.templates.items():
                for template_type, templates in rule_templates.items():
                    for template in templates:
                        self.template_bank.add_template(rule_name, template_type, template)
    
    def _create_example_templates(self):
        """Create example templates to demonstrate the system."""
        # Modus Ponens templates with variations
        mp_builder = TemplateBuilder()
        mp_builder.add_variation('conditional_type', [
            'If {p}, then {q}',
            '{q} if {p}',
            '{p} implies {q}',
            '{p} leads to {q}'
        ])
        mp_builder.add_static('. ')
        mp_builder.add_variable('P')
        mp_builder.add_static('. ')
        mp_builder.add_variation('conclusion_intro', [
            'Therefore',
            'Thus',
            'Hence',
            'Consequently'
        ])
        mp_builder.add_static(', ')
        mp_builder.add_variable('q')
        mp_builder.add_static('.')
        mp_builder.set_metadata('complexity', ComplexityLevel.BASIC)
        
        self.template_bank.add_template(
            'Modus Ponens', 
            'valid',
            mp_builder.build()
        )
        
        # Invalid version (Affirming the Consequent)
        ac_builder = TemplateBuilder()
        ac_builder.add_variation('conditional_type', [
            'If {p}, then {q}',
            '{q} if {p}',
            '{p} implies {q}'
        ])
        ac_builder.add_static('. ')
        ac_builder.add_variable('Q')
        ac_builder.add_static('. ')
        ac_builder.add_variation('conclusion_intro', [
            'Therefore',
            'Thus',
            'Hence'
        ])
        ac_builder.add_static(', ')
        ac_builder.add_variable('p')
        ac_builder.add_static('.')
        ac_builder.set_metadata('complexity', ComplexityLevel.BASIC)
        
        self.template_bank.add_template(
            'Affirming the Consequent',
            'invalid',
            ac_builder.build()
        )
    
    def set_config(self, **kwargs):
        """Update configuration settings."""
        self.config.update(kwargs)
        
        # Update variation generator complexity if changed
        if 'complexity_level' in kwargs:
            self.variation_generator.set_complexity(kwargs['complexity_level'])
    
    def get_random_sentences(self, n: int) -> List[str]:
        """Get n random sentences."""
        if n > len(self.sentences):
            raise ValueError(f"Requested {n} sentences but only {len(self.sentences)} available")
        return random.sample(self.sentences, n)
    
    def prepare_variables(self, sentences: List[str]) -> Dict[str, str]:
        """
        Prepare variables for template substitution.
        
        Args:
            sentences: List of sentences
            
        Returns:
            Dictionary of variables with variations
        """
        variables = {}
        
        # Ensure we have enough sentences for complex rules
        available_sentences = list(sentences)
        if len(available_sentences) < 4:
            # Repeat sentences if we don't have enough
            while len(available_sentences) < 4:
                available_sentences.extend(sentences)
        
        for i, sentence in enumerate(available_sentences[:4]):  # Support up to 4 variables (p, q, r, s)
            # Get letter for this sentence
            letter = chr(ord('p') + i)
            
            # Normalize sentence
            normalized = self.language_adapter.pattern.normalize_sentence(sentence)
            
            # Basic forms
            variables[letter] = normalized
            variables[letter.upper()] = self.language_adapter.pattern.capitalize_sentence(normalized)
            
            # Negation variations
            variables[f'not_{letter}'] = self.variation_generator.generate_negation(
                normalized, style='simple'
            )
            variables[f'not_{letter.upper()}'] = self.language_adapter.pattern.capitalize_sentence(
                variables[f'not_{letter}']
            )
            
            # Formal negation
            variables[f'not_formal_{letter}'] = self.variation_generator.generate_negation(
                normalized, style='formal'
            )
            
            # Emphatic negation
            variables[f'not_emphatic_{letter}'] = self.variation_generator.generate_negation(
                normalized, style='emphatic'
            )
        
        return variables
    
    def generate_argument_pair(self, rule_name: str) -> Tuple[str, str]:
        """
        Generate a valid/invalid argument pair.
        
        Args:
            rule_name: Name of the inference rule
            
        Returns:
            Tuple of (valid_argument, invalid_argument)
        """
        # Get invalid rule name
        invalid_rule = self.rule_mappings.get(rule_name, "Non Sequitur")
        
        # Determine required sentences
        required_sentences = self._get_required_sentences(rule_name)
        
        # Get sentences and prepare variables
        sentences = self.get_random_sentences(required_sentences)
        variables = self.prepare_variables(sentences)
        
        # Generate valid argument
        valid_options = {
            'complexity': self.config['complexity_level'],
            'variation_preferences': self.config.get('variation_preferences', {})
        }
        
        # Debug: print variables to see what's available
        # print(f"Variables for {rule_name}: {list(variables.keys())}")
        
        valid_argument = self.template_bank.generate_argument(
            rule_name, variables, 'valid', valid_options
        )
        
        # Generate invalid argument
        if self.flexible_mode and invalid_rule not in self.template_bank.templates:
            # Use flexible transformation
            invalid_argument = self._generate_flexible_invalid(
                rule_name, invalid_rule, variables
            )
        else:
            invalid_argument = self.template_bank.generate_argument(
                invalid_rule, variables, 'invalid', valid_options
            )
        
        return valid_argument, invalid_argument
    
    def _get_required_sentences(self, rule_name: str) -> int:
        """Get number of required sentences for a rule."""
        requirements = {
            "Modus Ponens": 2,
            "Modus Tollens": 2,
            "Disjunctive Syllogism": 2,
            "Conjunction Introduction": 3,
            "Conjunction Elimination": 3,
            "Disjunction Introduction": 2,
            "Disjunction Elimination": 4,
            "Hypothetical Syllogism": 3,
            "Material Conditional Introduction": 3,
            "Constructive Dilemma": 4,
            "Destructive Dilemma": 4
        }
        return requirements.get(rule_name, 3)
    
    def _generate_flexible_invalid(self, valid_rule: str, invalid_rule: str,
                                  variables: Dict[str, str]) -> str:
        """Generate invalid argument using flexible transformation."""
        # Get a valid template
        valid_template = self.template_bank.get_random_template(valid_rule, 'valid')
        if not valid_template:
            return f"No template available for {valid_rule}"
        
        # Transform based on rule type
        if valid_rule == "Modus Ponens":
            # Swap P and Q in conclusion
            transformed_vars = variables.copy()
            transformed_vars['p'], transformed_vars['q'] = transformed_vars['q'], transformed_vars['p']
            transformed_vars['P'], transformed_vars['Q'] = transformed_vars['Q'], transformed_vars['P']
            return valid_template.render(transformed_vars)
        
        # Default transformation
        return valid_template.render(variables)
    
    def generate_arguments(self, num_per_rule: int = 2) -> str:
        """
        Generate arguments for all rules.
        
        Args:
            num_per_rule: Number of argument pairs per rule
            
        Returns:
            Formatted string with all arguments
        """
        result = []
        argument_count = 1
        
        # Get available rules
        available_rules = list(self.rule_mappings.keys())
        
        for rule_name in available_rules:
            for _ in range(num_per_rule):
                try:
                    # Generate pair
                    valid_arg, invalid_arg = self.generate_argument_pair(rule_name)
                    
                    # Format valid argument
                    result.append(f"{argument_count}. {rule_name}")
                    result.append(f"{valid_arg}\n")
                    argument_count += 1
                    
                    # Format invalid argument
                    invalid_rule = self.rule_mappings[rule_name]
                    result.append(f"{argument_count}. {invalid_rule} (Invalid)")
                    result.append(f"{invalid_arg}\n")
                    argument_count += 1
                    
                except Exception as e:
                    print(f"Error generating {rule_name}: {e}")
                    continue
        
        return "\n".join(result)
    
    def generate_with_options(self, rule_name: str, options: Dict[str, Any]) -> str:
        """
        Generate a single argument with specific options.
        
        Args:
            rule_name: Name of the rule
            options: Generation options (complexity, style, etc.)
            
        Returns:
            Generated argument
        """
        # Update config temporarily
        old_config = self.config.copy()
        self.config.update(options)
        
        try:
            # Generate argument
            if options.get('is_valid', True):
                valid_arg, _ = self.generate_argument_pair(rule_name)
                return valid_arg
            else:
                _, invalid_arg = self.generate_argument_pair(rule_name)
                return invalid_arg
        finally:
            # Restore config
            self.config = old_config
    
    def get_variation_info(self) -> Dict[str, Any]:
        """Get information about available variations."""
        return {
            'language': self.language_code,
            'language_info': self.language_adapter.get_language_info(),
            'template_statistics': self.template_bank.get_statistics(),
            'variation_types': self.variation_library.get_variation_types(),
            'complexity_levels': [level.name for level in ComplexityLevel],
            'current_config': self.config
        }


def main():
    """Main function to run the enhanced argument generator."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate propositional logic arguments with variations"
    )
    parser.add_argument("sentences_file", help="Path to sentences file")
    parser.add_argument("--language", "-l", default="en",
                       help="Language code (default: en)")
    parser.add_argument("--output", "-o", default="arguments_v2.txt",
                       help="Output file (default: arguments_v2.txt)")
    parser.add_argument("--rules", "-r", help="Custom rule mappings file")
    parser.add_argument("--num", "-n", type=int, default=2,
                       help="Number of pairs per rule (default: 2)")
    parser.add_argument("--flexible", "-f", action="store_true",
                       help="Enable flexible mode")
    parser.add_argument("--complexity", "-c", 
                       choices=['basic', 'intermediate', 'advanced', 'expert'],
                       default='basic',
                       help="Complexity level (default: basic)")
    parser.add_argument("--info", "-i", action="store_true",
                       help="Show variation information")
    
    args = parser.parse_args()
    
    try:
        # Create generator
        generator = ArgumentGeneratorV2(
            args.sentences_file,
            language=args.language,
            rule_mappings_file=args.rules,
            flexible_mode=args.flexible
        )
        
        # Set complexity
        complexity_map = {
            'basic': ComplexityLevel.BASIC,
            'intermediate': ComplexityLevel.INTERMEDIATE,
            'advanced': ComplexityLevel.ADVANCED,
            'expert': ComplexityLevel.EXPERT
        }
        generator.set_config(complexity_level=complexity_map[args.complexity])
        
        if args.info:
            # Show variation info
            info = generator.get_variation_info()
            print(json.dumps(info, indent=2))
        else:
            # Generate arguments
            arguments = generator.generate_arguments(args.num)
            
            # Write output
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(arguments)
            
            print(f"Arguments written to {args.output}")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    main()
