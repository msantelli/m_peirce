"""
linguistic_patterns.py

Core linguistic pattern engine for multi-language support and natural language variations.
This module provides the base classes and interfaces for language-specific implementations.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum
import random


class ComplexityLevel(Enum):
    """Defines the complexity levels for generated arguments."""
    BASIC = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4


class VariationType(Enum):
    """Types of linguistic variations supported."""
    NEGATION = "negation"
    CONJUNCTION = "conjunction"
    DISJUNCTION = "disjunction"
    CONDITIONAL = "conditional"
    BICONDITIONAL = "biconditional"


class LinguisticPattern(ABC):
    """Abstract base class for linguistic patterns."""
    
    def __init__(self, language_code: str):
        self.language_code = language_code
        self.complexity_level = ComplexityLevel.BASIC
    
    @abstractmethod
    def get_variations(self, variation_type: VariationType) -> Dict[str, List[str]]:
        """
        Get all variations for a specific variation type.
        
        Args:
            variation_type: The type of variation to retrieve
            
        Returns:
            Dictionary mapping variation names to template patterns
        """
        pass
    
    @abstractmethod
    def format_sentence(self, sentence: str, formatting_type: str) -> str:
        """
        Apply language-specific formatting to a sentence.
        
        Args:
            sentence: The sentence to format
            formatting_type: Type of formatting (e.g., 'capitalize', 'negate')
            
        Returns:
            Formatted sentence
        """
        pass
    
    @abstractmethod
    def get_connectives(self) -> Dict[str, List[str]]:
        """Get language-specific logical connectives."""
        pass


class VariationTemplate:
    """Represents a template with multiple variation points."""
    
    def __init__(self, base_template: str, variation_points: Dict[str, List[str]]):
        """
        Initialize a variation template.
        
        Args:
            base_template: The base template string with placeholders
            variation_points: Dictionary mapping placeholder names to possible variations
        """
        self.base_template = base_template
        self.variation_points = variation_points
    
    def generate(self, variables: Dict[str, str], 
                 variation_preferences: Optional[Dict[str, str]] = None) -> str:
        """
        Generate a concrete instance of this template.
        
        Args:
            variables: Dictionary of variable substitutions (p, q, r, etc.)
            variation_preferences: Optional specific variations to use
            
        Returns:
            Generated string with variations applied
        """
        # First, select variations for each variation point
        selected_variations = {}
        for point, options in self.variation_points.items():
            if variation_preferences and point in variation_preferences:
                selected_variations[point] = variation_preferences[point]
            else:
                selected_variations[point] = random.choice(options)
        
        # Apply variations to the template
        result = self.base_template
        for point, variation in selected_variations.items():
            result = result.replace(f"{{{point}}}", variation)
        
        # Apply variable substitutions
        for var, value in variables.items():
            result = result.replace(f"{{{var}}}", value)
        
        return result


class NegationPattern:
    """Handles various forms of negation across languages."""
    
    def __init__(self, patterns: Dict[str, str]):
        """
        Initialize negation patterns.
        
        Args:
            patterns: Dictionary mapping negation types to patterns
                     Pattern should contain {sentence} placeholder
        """
        self.patterns = patterns
    
    def apply(self, sentence: str, negation_type: str = "simple") -> str:
        """
        Apply negation to a sentence.
        
        Args:
            sentence: The sentence to negate
            negation_type: Type of negation to apply
            
        Returns:
            Negated sentence
        """
        if negation_type not in self.patterns:
            negation_type = "simple"
        
        pattern = self.patterns[negation_type]
        return pattern.format(sentence=sentence)


class ConditionalPattern:
    """Handles various forms of conditional statements."""
    
    def __init__(self, patterns: Dict[str, str]):
        """
        Initialize conditional patterns.
        
        Args:
            patterns: Dictionary mapping conditional types to patterns
                     Patterns should contain {antecedent} and {consequent} placeholders
        """
        self.patterns = patterns
    
    def apply(self, antecedent: str, consequent: str, 
              conditional_type: str = "standard") -> str:
        """
        Create a conditional statement.
        
        Args:
            antecedent: The 'if' part
            consequent: The 'then' part
            conditional_type: Type of conditional to use
            
        Returns:
            Conditional statement
        """
        if conditional_type not in self.patterns:
            conditional_type = "standard"
        
        pattern = self.patterns[conditional_type]
        return pattern.format(antecedent=antecedent, consequent=consequent)


class VariationGenerator:
    """Main class for generating varied linguistic expressions."""
    
    def __init__(self, linguistic_pattern: LinguisticPattern):
        self.pattern = linguistic_pattern
        self.variation_cache = {}
    
    def set_complexity(self, level: ComplexityLevel):
        """Set the complexity level for generation."""
        self.pattern.complexity_level = level
    
    def generate_negation(self, sentence: str, style: Optional[str] = None) -> str:
        """
        Generate a negated form of a sentence.
        
        Args:
            sentence: The sentence to negate
            style: Optional specific negation style
            
        Returns:
            Negated sentence
        """
        negation_variations = self.pattern.get_variations(VariationType.NEGATION)
        
        if style and style in negation_variations:
            patterns = negation_variations[style]
        else:
            # Select based on complexity level
            available_styles = list(negation_variations.keys())
            if self.pattern.complexity_level == ComplexityLevel.BASIC:
                style = "simple" if "simple" in available_styles else available_styles[0]
            elif self.pattern.complexity_level == ComplexityLevel.EXPERT:
                style = "formal" if "formal" in available_styles else available_styles[-1]
            else:
                style = random.choice(available_styles)
            patterns = negation_variations[style]
        
        pattern = random.choice(patterns)
        return pattern.format(sentence=sentence)
    
    def generate_conjunction(self, sentences: List[str], style: Optional[str] = None) -> str:
        """
        Generate a conjunction of sentences.
        
        Args:
            sentences: List of sentences to conjoin
            style: Optional specific conjunction style
            
        Returns:
            Conjoined sentence
        """
        conjunction_variations = self.pattern.get_variations(VariationType.CONJUNCTION)
        
        if style and style in conjunction_variations:
            patterns = conjunction_variations[style]
        else:
            available_styles = list(conjunction_variations.keys())
            style = random.choice(available_styles)
            patterns = conjunction_variations[style]
        
        pattern = random.choice(patterns)
        
        # Handle different numbers of sentences
        if len(sentences) == 2:
            return pattern.format(p=sentences[0], q=sentences[1])
        elif len(sentences) > 2:
            # For multiple sentences, use list format
            if "{list}" in pattern:
                sentence_list = ", ".join(sentences[:-1]) + f", and {sentences[-1]}"
                return pattern.format(list=sentence_list)
            else:
                # Fall back to simple conjunction
                return ", and ".join(sentences)
        else:
            return sentences[0] if sentences else ""
    
    def generate_disjunction(self, sentences: List[str], style: Optional[str] = None,
                           exclusive: bool = False) -> str:
        """
        Generate a disjunction of sentences.
        
        Args:
            sentences: List of sentences to disjoin
            style: Optional specific disjunction style
            exclusive: Whether to use exclusive or inclusive disjunction
            
        Returns:
            Disjoined sentence
        """
        disjunction_variations = self.pattern.get_variations(VariationType.DISJUNCTION)
        
        if exclusive and "exclusive" in disjunction_variations:
            patterns = disjunction_variations["exclusive"]
        elif style and style in disjunction_variations:
            patterns = disjunction_variations[style]
        else:
            available_styles = [s for s in disjunction_variations.keys() 
                              if s != "exclusive" or exclusive]
            style = random.choice(available_styles)
            patterns = disjunction_variations[style]
        
        pattern = random.choice(patterns)
        
        if len(sentences) == 2:
            return pattern.format(p=sentences[0], q=sentences[1])
        elif len(sentences) > 2:
            if "{list}" in pattern:
                sentence_list = ", ".join(sentences[:-1]) + f", or {sentences[-1]}"
                return pattern.format(list=sentence_list)
            else:
                return ", or ".join(sentences)
        else:
            return sentences[0] if sentences else ""
    
    def generate_conditional(self, antecedent: str, consequent: str, 
                           style: Optional[str] = None) -> str:
        """
        Generate a conditional statement.
        
        Args:
            antecedent: The condition (if part)
            consequent: The result (then part)
            style: Optional specific conditional style
            
        Returns:
            Conditional statement
        """
        conditional_variations = self.pattern.get_variations(VariationType.CONDITIONAL)
        
        if style and style in conditional_variations:
            patterns = conditional_variations[style]
        else:
            available_styles = list(conditional_variations.keys())
            # Select based on complexity
            if self.pattern.complexity_level == ComplexityLevel.BASIC:
                style = "standard" if "standard" in available_styles else available_styles[0]
            else:
                style = random.choice(available_styles)
            patterns = conditional_variations[style]
        
        pattern = random.choice(patterns)
        return pattern.format(antecedent=antecedent, consequent=consequent)


class ArgumentStructure:
    """Represents the structure of a logical argument with variation points."""
    
    def __init__(self, rule_name: str, premises: List[VariationTemplate], 
                 conclusion: VariationTemplate):
        self.rule_name = rule_name
        self.premises = premises
        self.conclusion = conclusion
    
    def generate(self, variables: Dict[str, str], 
                 variation_generator: VariationGenerator,
                 variation_preferences: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate a complete argument with variations.
        
        Args:
            variables: Variable substitutions
            variation_generator: Generator for linguistic variations
            variation_preferences: Optional preferences for variations
            
        Returns:
            Generated argument string
        """
        # Generate premises
        generated_premises = []
        for premise in self.premises:
            generated_premises.append(premise.generate(variables, variation_preferences))
        
        # Generate conclusion
        generated_conclusion = self.conclusion.generate(variables, variation_preferences)
        
        # Combine into argument
        # This is a simple combination - could be enhanced with more variation
        argument_parts = generated_premises + [generated_conclusion]
        return " ".join(argument_parts)


class LanguageConfig:
    """Configuration for a specific language."""
    
    def __init__(self, language_code: str, name: str):
        self.language_code = language_code
        self.name = name
        self.capitalization_rules = {}
        self.punctuation_rules = {}
        self.word_order = "SVO"  # Subject-Verb-Object default
    
    def set_capitalization_rule(self, rule_name: str, rule_function):
        """Add a capitalization rule."""
        self.capitalization_rules[rule_name] = rule_function
    
    def set_punctuation_rule(self, rule_name: str, rule_function):
        """Add a punctuation rule."""
        self.punctuation_rules[rule_name] = rule_function
    
    def apply_capitalization(self, text: str, rule_name: str = "sentence") -> str:
        """Apply capitalization rules to text."""
        if rule_name in self.capitalization_rules:
            return self.capitalization_rules[rule_name](text)
        return text
    
    def apply_punctuation(self, text: str, rule_name: str = "statement") -> str:
        """Apply punctuation rules to text."""
        if rule_name in self.punctuation_rules:
            return self.punctuation_rules[rule_name](text)
        return text
