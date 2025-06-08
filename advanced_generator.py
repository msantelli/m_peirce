"""
advanced_argument_generator.py

Advanced argument generator that integrates context awareness,
strength analysis, and interactive configuration.
"""

from typing import Dict, List, Tuple, Optional, Any, Set
import json
import random
from dataclasses import dataclass
from datetime import datetime

from argument_generator_v2 import ArgumentGeneratorV2
from context_aware_system import (
    ContextAwareArgumentGenerator, SemanticAnalyzer, 
    SemanticDomain, PlausibilityScorer
)
from argument_strength import (
    ArgumentStrengthAnalyzer, ArgumentStrength,
    ArgumentDifficultyCalibrator
)
from interactive_config import (
    InteractiveConfigurator, ConfigurationWizard,
    ConfigurationExporter
)
from linguistic_patterns import ComplexityLevel


@dataclass
class GeneratedArgument:
    """Complete generated argument with all metadata."""
    text: str
    rule_type: str
    is_valid: bool
    variables: Dict[str, str]
    language: str
    complexity: ComplexityLevel
    strength_analysis: ArgumentStrength
    semantic_info: Dict[str, Any]
    generation_metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'text': self.text,
            'rule_type': self.rule_type,
            'is_valid': self.is_valid,
            'variables': self.variables,
            'language': self.language,
            'complexity': self.complexity.value,
            'strength_analysis': self.strength_analysis.to_dict(),
            'semantic_info': self.semantic_info,
            'generation_metadata': self.generation_metadata
        }


class OutputFormatter:
    """Formats arguments according to configuration."""
    
    def __init__(self):
        self.formats = {
            'standard': self._format_standard,
            'educational': self._format_educational,
            'quiz': self._format_quiz,
            'comparative': self._format_comparative,
            'detailed': self._format_detailed,
            'minimal': self._format_minimal,
            'json': self._format_json
        }
    
    def format_argument(self, argument: GeneratedArgument, 
                       format_type: str = 'standard',
                       include_analysis: bool = False) -> str:
        """Format an argument according to specified format."""
        if format_type in self.formats:
            return self.formats[format_type](argument, include_analysis)
        return self._format_standard(argument, include_analysis)
    
    def _format_standard(self, arg: GeneratedArgument, 
                        include_analysis: bool) -> str:
        """Standard format with optional analysis."""
        lines = []
        
        # Header
        validity = "" if arg.is_valid else " (Invalid)"
        lines.append(f"{arg.rule_type}{validity}")
        lines.append(arg.text)
        
        if include_analysis:
            lines.append(f"\nStrength Score: {arg.strength_analysis.overall_score:.2f}")
            if arg.strength_analysis.strengths:
                lines.append(f"Strengths: {', '.join(arg.strength_analysis.strengths)}")
            if arg.strength_analysis.weaknesses:
                lines.append(f"Weaknesses: {', '.join(arg.strength_analysis.weaknesses)}")
        
        return '\n'.join(lines)
    
    def _format_educational(self, arg: GeneratedArgument, 
                           include_analysis: bool) -> str:
        """Educational format with explanations."""
        lines = []
        
        # Title and argument
        lines.append(f"=== {arg.rule_type} ===")
        lines.append(f"Validity: {'Valid' if arg.is_valid else 'Invalid'}")
        lines.append(f"\nArgument:")
        lines.append(arg.text)
        
        # Structure breakdown
        lines.append(f"\nStructure:")
        if 'premises' in arg.semantic_info:
            for i, premise in enumerate(arg.semantic_info['premises'], 1):
                lines.append(f"  Premise {i}: {premise}")
            lines.append(f"  Conclusion: {arg.semantic_info.get('conclusion', 'N/A')}")
        
        # Analysis
        if include_analysis:
            lines.append(f"\nAnalysis:")
            lines.append(f"  Logical Validity: {arg.strength_analysis.logical_validity}")
            lines.append(f"  Plausibility: {arg.strength_analysis.semantic_plausibility:.2f}")
            lines.append(f"  Persuasiveness: {arg.strength_analysis.persuasiveness:.2f}")
            
            feedback = ArgumentStrengthAnalyzer().generate_feedback(arg.strength_analysis)
            lines.append(f"\nFeedback: {feedback}")
        
        # Educational notes
        if not arg.is_valid:
            lines.append(f"\nWhy this is invalid:")
            lines.append(f"This commits the {arg.rule_type} fallacy.")
            if arg.rule_type == "Affirming the Consequent":
                lines.append("The conclusion affirms the consequent of the conditional.")
            elif arg.rule_type == "Denying the Antecedent":
                lines.append("The conclusion denies the antecedent of the conditional.")
        
        return '\n'.join(lines)
    
    def _format_quiz(self, arg: GeneratedArgument, 
                    include_analysis: bool) -> str:
        """Quiz format - hides validity."""
        lines = []
        
        lines.append(f"Question: Is the following argument valid or invalid?")
        lines.append(f"\n{arg.text}")
        lines.append(f"\nRule Type: {arg.rule_type.replace(' (Invalid)', '')}")
        
        if include_analysis:
            lines.append(f"\nHints:")
            if arg.strength_analysis.persuasiveness > 0.7:
                lines.append("- This argument is quite persuasive")
            if arg.strength_analysis.semantic_plausibility > 0.7:
                lines.append("- The conclusion seems plausible")
            if arg.strength_analysis.sophistication > 0.7:
                lines.append("- Look carefully at the logical structure")
        
        lines.append(f"\n[Answer hidden - {'Valid' if arg.is_valid else 'Invalid'}]")
        
        return '\n'.join(lines)
    
    def _format_comparative(self, arg: GeneratedArgument, 
                           include_analysis: bool) -> str:
        """Comparative format for multiple arguments."""
        lines = []
        
        lines.append(f"{arg.language.upper()} - {arg.rule_type}:")
        lines.append(f"  {arg.text}")
        
        if include_analysis:
            lines.append(f"  Score: {arg.strength_analysis.overall_score:.2f}")
        
        return '\n'.join(lines)
    
    def _format_detailed(self, arg: GeneratedArgument, 
                        include_analysis: bool) -> str:
        """Detailed format with all information."""
        lines = []
        
        lines.append("="*60)
        lines.append(f"Rule: {arg.rule_type}")
        lines.append(f"Valid: {arg.is_valid}")
        lines.append(f"Language: {arg.language}")
        lines.append(f"Complexity: {arg.complexity.value}")
        
        lines.append(f"\nArgument Text:")
        lines.append(arg.text)
        
        lines.append(f"\nVariables:")
        for var, value in arg.variables.items():
            lines.append(f"  {var}: {value}")
        
        if include_analysis:
            lines.append(f"\nStrength Analysis:")
            analysis = arg.strength_analysis
            lines.append(f"  Overall Score: {analysis.overall_score:.3f}")
            lines.append(f"  Logical Validity: {analysis.logical_validity}")
            lines.append(f"  Semantic Plausibility: {analysis.semantic_plausibility:.3f}")
            lines.append(f"  Linguistic Clarity: {analysis.linguistic_clarity:.3f}")
            lines.append(f"  Persuasiveness: {analysis.persuasiveness:.3f}")
            lines.append(f"  Sophistication: {analysis.sophistication:.3f}")
            lines.append(f"  Emotional Impact: {analysis.emotional_impact:.3f}")
            
            if analysis.techniques_used:
                techniques = [t.value for t in analysis.techniques_used]
                lines.append(f"  Techniques: {', '.join(techniques)}")
        
        lines.append(f"\nSemantic Information:")
        lines.append(f"  Coherence: {arg.semantic_info.get('semantic_coherence', 'N/A')}")
        lines.append(f"  Domains: {arg.semantic_info.get('domains', [])}")
        
        lines.append(f"\nGeneration Metadata:")
        for key, value in arg.generation_metadata.items():
            lines.append(f"  {key}: {value}")
        
        return '\n'.join(lines)
    
    def _format_minimal(self, arg: GeneratedArgument, 
                       include_analysis: bool) -> str:
        """Minimal format - just the text."""
        return arg.text
    
    def _format_json(self, arg: GeneratedArgument, 
                    include_analysis: bool) -> str:
        """JSON format for programmatic use."""
        data = arg.to_dict()
        if not include_analysis:
            data.pop('strength_analysis', None)
        return json.dumps(data, indent=2)


class AdvancedArgumentGenerator:
    """
    Advanced argument generator with all Phase 4 features integrated.
    """
    
    def __init__(self, sentences_file: str):
        # Load sentences
        self.sentences = self._load_sentences(sentences_file)
        
        # Initialize components
        self.configurator = InteractiveConfigurator()
        self.semantic_analyzer = SemanticAnalyzer()
        self.context_generator = ContextAwareArgumentGenerator(self.sentences)
        self.strength_analyzer = ArgumentStrengthAnalyzer(self.semantic_analyzer)
        self.difficulty_calibrator = ArgumentDifficultyCalibrator()
        self.formatter = OutputFormatter()
        
        # Initialize base generators for each language
        self.generators = {}
        self._init_generators()
        
        # Statistics tracking
        self.generation_stats = {
            'total_generated': 0,
            'by_rule': {},
            'by_language': {},
            'average_strength': 0.0,
            'strength_scores': []
        }
    
    def _load_sentences(self, file_path: str) -> List[str]:
        """Load sentences from file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")
            return []
    
    def _init_generators(self):
        """Initialize language-specific generators."""
        languages = ['en', 'es', 'fr', 'de']
        
        # Create temporary file with sentences
        with open('temp_sentences.txt', 'w', encoding='utf-8') as f:
            for sentence in self.sentences:
                f.write(sentence + '\n')
        
        for lang in languages:
            try:
                self.generators[lang] = ArgumentGeneratorV2(
                    'temp_sentences.txt',
                    language=lang,
                    flexible_mode=True
                )
            except Exception as e:
                print(f"Error initializing {lang}: {e}")
        
        # Cleanup
        import os
        try:
            os.remove('temp_sentences.txt')
        except:
            pass
    
    def configure(self, **kwargs):
        """Configure the generator."""
        for key, value in kwargs.items():
            self.configurator.set_option(key, value)
    
    def use_profile(self, profile_name: str):
        """Load a configuration profile."""
        return self.configurator.load_profile(profile_name)
    
    def generate_single(self, rule_type: Optional[str] = None) -> GeneratedArgument:
        """Generate a single argument with full analysis."""
        config = self.configurator.current_config
        
        # Select rule type if not specified
        if not rule_type:
            available_rules = list(self.generators[config['language']].rule_mappings.keys())
            rule_type = random.choice(available_rules)
        
        # Determine if valid or invalid
        is_valid = random.choice([True, False])
        
        # Generate context-aware argument
        required_sentences = self._get_required_sentences(rule_type)
        context_result = self.context_generator.generate_context_aware_argument(
            rule_type, required_sentences,
            ensure_plausible=(config['target_plausibility'] > 0.5)
        )
        
        # Get language generator
        lang = config['language']
        if lang not in self.generators:
            lang = 'en'
        
        generator = self.generators[lang]
        
        # Set configuration
        complexity_map = {
            'basic': ComplexityLevel.BASIC,
            'intermediate': ComplexityLevel.INTERMEDIATE,
            'advanced': ComplexityLevel.ADVANCED,
            'expert': ComplexityLevel.EXPERT
        }
        
        generator.set_config(
            complexity_level=complexity_map[config['complexity']],
            formality=config['formality'],
            domain=config['domain']
        )
        
        # Generate valid argument
        valid_text = generator.generate_with_options(
            rule_type,
            options={'is_valid': True}
        )
        
        # Generate invalid argument with same variables
        invalid_rule = generator.rule_mappings.get(rule_type, "Non Sequitur")
        invalid_text = generator.generate_with_options(
            invalid_rule,
            options={'is_valid': False}
        )
        
        # Analyze both
        valid_strength = self.strength_analyzer.analyze_argument(
            valid_text, rule_type, True,
            semantic_score=context_result['plausibility_score']
        )
        
        invalid_strength = self.strength_analyzer.analyze_argument(
            invalid_text, invalid_rule, False,
            semantic_score=context_result['plausibility_score'] * 0.8
        )
        
        # Calculate difficulty
        difficulty = self.difficulty_calibrator.calculate_difficulty(
            valid_text, invalid_text, valid_strength, invalid_strength
        )
        
        # Create results
        shared_metadata = {
            'timestamp': datetime.now().isoformat(),
            'config_profile': config.get('profile_name', 'custom'),
            'pair_difficulty': difficulty,
            'difficulty_level': self.difficulty_calibrator.categorize_difficulty(difficulty)
        }
        
        valid_arg = GeneratedArgument(
            text=valid_text,
            rule_type=rule_type,
            is_valid=True,
            variables=context_result['variables'],
            language=lang,
            complexity=complexity_map[config['complexity']],
            strength_analysis=valid_strength,
            semantic_info={
                'premises': context_result['premises'],
                'conclusion': context_result['conclusion'],
                'semantic_coherence': context_result['semantic_coherence'],
                'domains': list(context_result['domains'])
            },
            generation_metadata=shared_metadata.copy()
        )
        
        invalid_arg = GeneratedArgument(
            text=invalid_text,
            rule_type=invalid_rule,
            is_valid=False,
            variables=context_result['variables'],
            language=lang,
            complexity=complexity_map[config['complexity']],
            strength_analysis=invalid_strength,
            semantic_info={
                'premises': context_result['premises'],
                'conclusion': context_result['conclusion'],
                'semantic_coherence': context_result['semantic_coherence'],
                'domains': list(context_result['domains'])
            },
            generation_metadata=shared_metadata.copy()
        )
        
        # Update statistics
        self._update_statistics(valid_arg)
        self._update_statistics(invalid_arg)
        
        return valid_arg, invalid_arg
    
    def generate_themed_set(self, theme: SemanticDomain, 
                           rules: Optional[List[str]] = None) -> List[GeneratedArgument]:
        """Generate a themed set of arguments."""
        if not rules:
            rules = ['Modus Ponens', 'Modus Tollens', 'Disjunctive Syllogism']
        
        # Get themed arguments from context generator
        themed_contexts = self.context_generator.generate_themed_argument_set(theme, rules)
        
        results = []
        for context in themed_contexts:
            # Generate argument for each context
            config = self.configurator.current_config
            lang = config['language']
            
            if lang not in self.generators:
                continue
            
            generator = self.generators[lang]
            
            try:
                text = generator.generate_with_options(
                    context['rule_type'],
                    options={'is_valid': True}
                )
                
                strength = self.strength_analyzer.analyze_argument(
                    text, context['rule_type'], True,
                    semantic_score=context['plausibility_score']
                )
                
                arg = GeneratedArgument(
                    text=text,
                    rule_type=context['rule_type'],
                    is_valid=True,
                    variables=context['variables'],
                    language=lang,
                    complexity=ComplexityLevel.INTERMEDIATE,
                    strength_analysis=strength,
                    semantic_info={
                        'theme': theme.value,
                        'premises': context['premises'],
                        'conclusion': context['conclusion'],
                        'semantic_coherence': context['semantic_coherence'],
                        'domains': list(context['domains'])
                    },
                    generation_metadata={
                        'timestamp': datetime.now().isoformat(),
                        'theme': theme.value
                    }
                )
                
                results.append(arg)
                self._update_statistics(arg)
                
            except Exception as e:
                print(f"Error generating themed argument: {e}")
                continue
        
        return results
    
    def generate_difficulty_calibrated_set(self, 
                                         target_difficulty: str,
                                         count: int = 5) -> List[Tuple[GeneratedArgument, GeneratedArgument]]:
        """Generate argument pairs calibrated to specific difficulty."""
        difficulty_ranges = {
            'easy': (0.0, 0.3),
            'medium': (0.3, 0.5),
            'hard': (0.5, 0.7),
            'expert': (0.7, 1.0)
        }
        
        if target_difficulty not in difficulty_ranges:
            target_difficulty = 'medium'
        
        min_diff, max_diff = difficulty_ranges[target_difficulty]
        
        results = []
        attempts = 0
        max_attempts = count * 5  # Allow retries
        
        while len(results) < count and attempts < max_attempts:
            attempts += 1
            
            # Generate a pair
            valid_arg, invalid_arg = self.generate_pair()
            
            # Check difficulty
            difficulty = self.difficulty_calibrator.calculate_difficulty(
                valid_arg.text, invalid_arg.text,
                valid_arg.strength_analysis, invalid_arg.strength_analysis
            )
            
            if min_diff <= difficulty <= max_diff:
                results.append((valid_arg, invalid_arg))
        
        return results
    
    def generate_multilingual_comparison(self, rule_type: str) -> Dict[str, GeneratedArgument]:
        """Generate the same argument in multiple languages."""
        results = {}
        
        # Generate context once
        required_sentences = self._get_required_sentences(rule_type)
        context_result = self.context_generator.generate_context_aware_argument(
            rule_type, required_sentences, ensure_plausible=True
        )
        
        # Generate for each language
        for lang in ['en', 'es', 'fr', 'de']:
            if lang not in self.generators:
                continue
            
            generator = self.generators[lang]
            
            try:
                # Use same configuration
                text = generator.generate_with_options(
                    rule_type,
                    options={'is_valid': True}
                )
                
                strength = self.strength_analyzer.analyze_argument(
                    text, rule_type, True,
                    semantic_score=context_result['plausibility_score']
                )
                
                arg = GeneratedArgument(
                    text=text,
                    rule_type=rule_type,
                    is_valid=True,
                    variables=context_result['variables'],
                    language=lang,
                    complexity=ComplexityLevel.INTERMEDIATE,
                    strength_analysis=strength,
                    semantic_info={
                        'premises': context_result['premises'],
                        'conclusion': context_result['conclusion'],
                        'semantic_coherence': context_result['semantic_coherence'],
                        'domains': list(context_result['domains'])
                    },
                    generation_metadata={
                        'timestamp': datetime.now().isoformat(),
                        'comparison_set': True
                    }
                )
                
                results[lang] = arg
                self._update_statistics(arg)
                
            except Exception as e:
                print(f"Error generating {lang} argument: {e}")
                continue
        
        return results
    
    def interactive_generation_session(self):
        """Run an interactive generation session."""
        print("=== Interactive Argument Generation ===\n")
        
        # Run configuration wizard
        wizard = ConfigurationWizard(self.configurator)
        wizard.start()
        
        while True:
            step = wizard.next_step()
            if not step:
                break
            
            print(f"\n{step['question']}")
            for code, desc in step['options']:
                print(f"  {code}: {desc}")
            
            response = input("\nYour choice: ").strip()
            wizard.process_response(response)
        
        # Apply configuration
        new_config = wizard.finish()
        for key, value in new_config.items():
            self.configurator.set_option(key, value)
        
        print("\nConfiguration complete!")
        print(self.configurator.get_config_summary())
        
        # Generation loop
        while True:
            print("\n" + "="*40)
            print("What would you like to generate?")
            print("1. Single argument")
            print("2. Valid/Invalid pair")
            print("3. Themed set")
            print("4. Difficulty-calibrated set")
            print("5. Multilingual comparison")
            print("6. Change configuration")
            print("7. View statistics")
            print("8. Exit")
            
            choice = input("\nChoice: ").strip()
            
            if choice == '1':
                arg = self.generate_single()
                print("\n" + self.formatter.format_argument(
                    arg, 
                    self.configurator.current_config['output_format'],
                    self.configurator.current_config['include_analysis']
                ))
                
            elif choice == '2':
                valid, invalid = self.generate_pair()
                print("\nVALID:")
                print(self.formatter.format_argument(
                    valid,
                    self.configurator.current_config['output_format'],
                    self.configurator.current_config['include_analysis']
                ))
                print("\nINVALID:")
                print(self.formatter.format_argument(
                    invalid,
                    self.configurator.current_config['output_format'],
                    self.configurator.current_config['include_analysis']
                ))
                
                # Show difficulty
                difficulty = valid.generation_metadata.get('pair_difficulty', 0)
                level = valid.generation_metadata.get('difficulty_level', 'Unknown')
                print(f"\nDifficulty: {level} ({difficulty:.2f})")
                
            elif choice == '3':
                print("\nAvailable themes:")
                for domain in SemanticDomain:
                    print(f"  {domain.value}")
                theme_name = input("Select theme: ").strip()
                
                try:
                    theme = SemanticDomain(theme_name)
                    args = self.generate_themed_set(theme)
                    
                    print(f"\n=== {theme.value.upper()} THEMED ARGUMENTS ===")
                    for arg in args:
                        print(f"\n{arg.rule_type}:")
                        print(arg.text)
                except:
                    print("Invalid theme!")
                    
            elif choice == '4':
                level = input("Difficulty level (easy/medium/hard/expert): ").strip()
                count = int(input("How many pairs? ").strip())
                
                pairs = self.generate_difficulty_calibrated_set(level, count)
                print(f"\n=== {level.upper()} DIFFICULTY PAIRS ===")
                
                for i, (valid, invalid) in enumerate(pairs, 1):
                    print(f"\nPair {i}:")
                    print("Valid:", valid.text)
                    print("Invalid:", invalid.text)
                    
            elif choice == '5':
                rule = input("Rule type (e.g., Modus Ponens): ").strip()
                comparisons = self.generate_multilingual_comparison(rule)
                
                print(f"\n=== {rule} IN MULTIPLE LANGUAGES ===")
                for lang, arg in comparisons.items():
                    print(f"\n{lang.upper()}:")
                    print(arg.text)
                    
            elif choice == '6':
                self._interactive_config_change()
                
            elif choice == '7':
                self._show_statistics()
                
            elif choice == '8':
                break
    
    def _interactive_config_change(self):
        """Interactive configuration change."""
        print("\nCurrent configuration:")
        print(self.configurator.get_config_summary())
        
        print("\nOptions to change:")
        for i, (name, option) in enumerate(self.configurator.options.items(), 1):
            print(f"{i}. {option.description}: {option.value}")
        
        choice = input("\nSelect option number (or 'back'): ").strip()
        if choice == 'back':
            return
        
        try:
            idx = int(choice) - 1
            option_name = list(self.configurator.options.keys())[idx]
            option = self.configurator.options[option_name]
            
            print(f"\nChanging: {option.description}")
            print(f"Current value: {option.value}")
            
            if option.possible_values:
                print("Possible values:")
                for val in option.possible_values:
                    print(f"  {val}")
            
            new_value = input("New value: ").strip()
            
            # Convert type if needed
            if isinstance(option.value, bool):
                new_value = new_value.lower() in ['true', 'yes', '1']
            elif isinstance(option.value, (int, float)):
                new_value = float(new_value)
            
            if self.configurator.set_option(option_name, new_value):
                print("Configuration updated!")
            else:
                print("Invalid value!")
                
        except Exception as e:
            print(f"Error: {e}")
    
    def _show_statistics(self):
        """Show generation statistics."""
        print("\n=== GENERATION STATISTICS ===")
        print(f"Total arguments generated: {self.generation_stats['total_generated']}")
        
        if self.generation_stats['by_rule']:
            print("\nBy rule type:")
            for rule, count in sorted(self.generation_stats['by_rule'].items()):
                print(f"  {rule}: {count}")
        
        if self.generation_stats['by_language']:
            print("\nBy language:")
            for lang, count in sorted(self.generation_stats['by_language'].items()):
                print(f"  {lang}: {count}")
        
        if self.generation_stats['strength_scores']:
            avg_strength = sum(self.generation_stats['strength_scores']) / len(self.generation_stats['strength_scores'])
            print(f"\nAverage strength score: {avg_strength:.3f}")
            print(f"Highest: {max(self.generation_stats['strength_scores']):.3f}")
            print(f"Lowest: {min(self.generation_stats['strength_scores']):.3f}")
    
    def _update_statistics(self, arg: GeneratedArgument):
        """Update generation statistics."""
        self.generation_stats['total_generated'] += 1
        
        # By rule
        rule = arg.rule_type
        if rule not in self.generation_stats['by_rule']:
            self.generation_stats['by_rule'][rule] = 0
        self.generation_stats['by_rule'][rule] += 1
        
        # By language
        lang = arg.language
        if lang not in self.generation_stats['by_language']:
            self.generation_stats['by_language'][lang] = 0
        self.generation_stats['by_language'][lang] += 1
        
        # Strength scores
        self.generation_stats['strength_scores'].append(
            arg.strength_analysis.overall_score
        )
    
    def _get_required_sentences(self, rule_type: str) -> int:
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
        return requirements.get(rule_type, 2)
    
    def export_session(self, filename: str):
        """Export current session data."""
        session_data = {
            'configuration': self.configurator.current_config,
            'statistics': self.generation_stats,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"Session exported to {filename}")


def main():
    """Main function to demonstrate advanced features."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python advanced_argument_generator.py <sentences_file>")
        return
    
    sentences_file = sys.argv[1]
    generator = AdvancedArgumentGenerator(sentences_file)
    
    # Check for command line options
    if len(sys.argv) > 2 and sys.argv[2] == '--interactive':
        generator.interactive_generation_session()
    else:
        # Demo mode
        print("=== ADVANCED ARGUMENT GENERATOR DEMO ===\n")
        
        # Configure for interesting output
        generator.configure(
            complexity='advanced',
            target_persuasiveness=0.7,
            semantic_coherence='high',
            include_analysis=True,
            output_format='educational'
        )
        
        # Generate a difficult pair
        print("1. DIFFICULT ARGUMENT PAIR:")
        valid, invalid = generator.generate_pair("Modus Ponens")
        
        print("\nVALID VERSION:")
        print(generator.formatter.format_argument(valid, 'educational', True))
        
        print("\n" + "="*60 + "\n")
        
        print("INVALID VERSION:")
        print(generator.formatter.format_argument(invalid, 'educational', True))
        
        # Show comparison
        comparison = generator.strength_analyzer.compare_arguments(
            valid.strength_analysis, invalid.strength_analysis
        )
        
        print("\n" + "="*60)
        print("COMPARISON:")
        print(f"Stronger argument: {comparison['stronger_overall']}")
        print(f"Score difference: {comparison['score_difference']:.3f}")
        for diff in comparison['key_differences']:
            print(f"  - {diff}")
        
        # Show difficulty analysis
        difficulty = generator.difficulty_calibrator.calculate_difficulty(
            valid.text, invalid.text,
            valid.strength_analysis, invalid.strength_analysis
        )
        
        explanation = generator.difficulty_calibrator.generate_difficulty_explanation(
            valid.text, invalid.text, difficulty,
            valid.strength_analysis, invalid.strength_analysis
        )
        
        print(f"\nDIFFICULTY ANALYSIS:")
        print(explanation)


if __name__ == "__main__":
    main()