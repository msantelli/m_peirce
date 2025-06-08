"""
language_base.py

Abstract base classes for implementing language-specific logic patterns and templates.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional, Set, Any
from linguistic_patterns import (
    LinguisticPattern, VariationType, ComplexityLevel,
    NegationPattern, ConditionalPattern, VariationTemplate
)


class LanguageSpecificPattern(LinguisticPattern):
    """Base class for language-specific pattern implementations."""
    
    def __init__(self, language_code: str):
        super().__init__(language_code)
        self.negation_patterns = self._init_negation_patterns()
        self.conjunction_patterns = self._init_conjunction_patterns()
        self.disjunction_patterns = self._init_disjunction_patterns()
        self.conditional_patterns = self._init_conditional_patterns()
        self.connectives = self._init_connectives()
    
    @abstractmethod
    def _init_negation_patterns(self) -> Dict[str, List[str]]:
        """Initialize negation patterns for this language."""
        pass
    
    @abstractmethod
    def _init_conjunction_patterns(self) -> Dict[str, List[str]]:
        """Initialize conjunction patterns for this language."""
        pass
    
    @abstractmethod
    def _init_disjunction_patterns(self) -> Dict[str, List[str]]:
        """Initialize disjunction patterns for this language."""
        pass
    
    @abstractmethod
    def _init_conditional_patterns(self) -> Dict[str, List[str]]:
        """Initialize conditional patterns for this language."""
        pass
    
    @abstractmethod
    def _init_connectives(self) -> Dict[str, List[str]]:
        """Initialize logical connectives for this language."""
        pass
    
    def get_variations(self, variation_type: VariationType) -> Dict[str, List[str]]:
        """Get all variations for a specific variation type."""
        if variation_type == VariationType.NEGATION:
            return self.negation_patterns
        elif variation_type == VariationType.CONJUNCTION:
            return self.conjunction_patterns
        elif variation_type == VariationType.DISJUNCTION:
            return self.disjunction_patterns
        elif variation_type == VariationType.CONDITIONAL:
            return self.conditional_patterns
        else:
            return {}
    
    def get_connectives(self) -> Dict[str, List[str]]:
        """Get language-specific logical connectives."""
        return self.connectives
    
    @abstractmethod
    def format_sentence(self, sentence: str, formatting_type: str) -> str:
        """Apply language-specific formatting to a sentence."""
        pass
    
    @abstractmethod
    def normalize_sentence(self, sentence: str) -> str:
        """Normalize a sentence according to language rules."""
        pass
    
    @abstractmethod
    def capitalize_sentence(self, sentence: str) -> str:
        """Capitalize a sentence according to language rules."""
        pass


class LanguageTemplates(ABC):
    """Abstract base class for language-specific argument templates."""
    
    def __init__(self, language_pattern: LanguageSpecificPattern):
        self.language_pattern = language_pattern
        self.templates = self._init_templates()
    
    @abstractmethod
    def _init_templates(self) -> Dict[str, Dict[str, List[VariationTemplate]]]:
        """
        Initialize all templates for this language.
        
        Returns:
            Dictionary mapping rule names to valid/invalid template lists
        """
        pass
    
    def get_templates(self, rule_name: str, is_valid: bool = True) -> List[VariationTemplate]:
        """
        Get templates for a specific rule.
        
        Args:
            rule_name: Name of the inference rule
            is_valid: Whether to get valid or invalid templates
            
        Returns:
            List of variation templates
        """
        if rule_name not in self.templates:
            return []
        
        template_type = "valid" if is_valid else "invalid"
        return self.templates[rule_name].get(template_type, [])
    
    @abstractmethod
    def get_required_sentences(self, rule_name: str) -> int:
        """Get the number of sentences required for a rule."""
        pass
    
    @abstractmethod
    def get_template_variables(self, rule_name: str) -> Set[str]:
        """Get the set of variables used in templates for a rule."""
        pass


class LanguageGrammar(ABC):
    """Abstract base class for language-specific grammar rules."""
    
    def __init__(self, language_code: str):
        self.language_code = language_code
    
    @abstractmethod
    def apply_agreement(self, subject: str, verb: str, object: Optional[str] = None) -> Tuple[str, str, Optional[str]]:
        """
        Apply grammatical agreement rules.
        
        Args:
            subject: The subject of the sentence
            verb: The verb
            object: Optional object
            
        Returns:
            Tuple of (modified_subject, modified_verb, modified_object)
        """
        pass
    
    @abstractmethod
    def apply_article_rules(self, noun: str, definite: bool = False) -> str:
        """
        Apply article rules to a noun.
        
        Args:
            noun: The noun
            definite: Whether to use definite article
            
        Returns:
            Noun with appropriate article
        """
        pass
    
    @abstractmethod
    def apply_word_order(self, components: Dict[str, str]) -> str:
        """
        Apply word order rules to sentence components.
        
        Args:
            components: Dictionary with keys like 'subject', 'verb', 'object'
            
        Returns:
            Properly ordered sentence
        """
        pass
    
    @abstractmethod
    def pluralize(self, word: str, count: int = 2) -> str:
        """
        Pluralize a word according to language rules.
        
        Args:
            word: The word to pluralize
            count: The count (for languages with multiple plural forms)
            
        Returns:
            Pluralized word
        """
        pass
    
    @abstractmethod
    def apply_case(self, word: str, case: str) -> str:
        """
        Apply grammatical case to a word (for languages with cases).
        
        Args:
            word: The word
            case: The grammatical case (nominative, accusative, etc.)
            
        Returns:
            Word in the specified case
        """
        pass


class LanguageStyleGuide(ABC):
    """Abstract base class for language-specific style preferences."""
    
    def __init__(self, language_code: str):
        self.language_code = language_code
        self.formality_levels = self._init_formality_levels()
    
    @abstractmethod
    def _init_formality_levels(self) -> Dict[str, Dict[str, Any]]:
        """Initialize formality level configurations."""
        pass
    
    @abstractmethod
    def apply_formality(self, text: str, formality_level: str) -> str:
        """
        Apply formality transformations to text.
        
        Args:
            text: The text to transform
            formality_level: Level of formality (casual, formal, academic, etc.)
            
        Returns:
            Transformed text
        """
        pass
    
    @abstractmethod
    def get_domain_specific_style(self, domain: str) -> Dict[str, Any]:
        """
        Get style preferences for a specific domain.
        
        Args:
            domain: The domain (legal, scientific, everyday, etc.)
            
        Returns:
            Dictionary of style preferences
        """
        pass
    
    @abstractmethod
    def apply_rhetorical_emphasis(self, text: str, emphasis_type: str) -> str:
        """
        Apply rhetorical emphasis to text.
        
        Args:
            text: The text to emphasize
            emphasis_type: Type of emphasis (strong, subtle, questioning, etc.)
            
        Returns:
            Emphasized text
        """
        pass


class LanguageAdapter:
    """Adapter class that combines all language-specific components."""
    
    def __init__(self, 
                 pattern: LanguageSpecificPattern,
                 templates: LanguageTemplates,
                 grammar: LanguageGrammar,
                 style_guide: LanguageStyleGuide):
        self.pattern = pattern
        self.templates = templates
        self.grammar = grammar
        self.style_guide = style_guide
        self.language_code = pattern.language_code
    
    def prepare_sentence(self, sentence: str, 
                        formatting_options: Optional[Dict[str, Any]] = None) -> str:
        """
        Prepare a sentence with all language-specific rules applied.
        
        Args:
            sentence: The raw sentence
            formatting_options: Optional formatting preferences
            
        Returns:
            Fully prepared sentence
        """
        # Normalize the sentence
        sentence = self.pattern.normalize_sentence(sentence)
        
        # Apply grammar rules if needed
        if formatting_options and "apply_grammar" in formatting_options:
            # This would need more context, but shows the idea
            sentence = self.grammar.apply_article_rules(sentence)
        
        # Apply style preferences
        if formatting_options and "formality" in formatting_options:
            sentence = self.style_guide.apply_formality(
                sentence, formatting_options["formality"]
            )
        
        # Apply capitalization if needed
        if formatting_options and formatting_options.get("capitalize", False):
            sentence = self.pattern.capitalize_sentence(sentence)
        
        return sentence
    
    def generate_argument(self, rule_name: str, variables: Dict[str, str],
                         is_valid: bool = True, 
                         options: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate a complete argument in this language.
        
        Args:
            rule_name: Name of the inference rule
            variables: Variable substitutions
            is_valid: Whether to generate valid or invalid form
            options: Optional generation options
            
        Returns:
            Generated argument
        """
        # Get templates for this rule
        templates = self.templates.get_templates(rule_name, is_valid)
        
        if not templates:
            return f"No templates available for {rule_name} in {self.language_code}"
        
        # Select a template (could be based on options)
        template = templates[0]  # Simplified for now
        
        # Prepare variables with language-specific formatting
        prepared_vars = {}
        for var, value in variables.items():
            prepared_vars[var] = self.prepare_sentence(value, options)
        
        # Generate the argument
        # This is simplified - would integrate with VariationGenerator
        return template.generate(prepared_vars, options)
    
    def get_language_info(self) -> Dict[str, Any]:
        """Get information about this language adapter."""
        return {
            "language_code": self.language_code,
            "supported_rules": list(self.templates.templates.keys()),
            "negation_styles": list(self.pattern.negation_patterns.keys()),
            "conjunction_styles": list(self.pattern.conjunction_patterns.keys()),
            "disjunction_styles": list(self.pattern.disjunction_patterns.keys()),
            "conditional_styles": list(self.pattern.conditional_patterns.keys()),
            "formality_levels": list(self.style_guide.formality_levels.keys())
        }


class LanguageFactory:
    """Factory for creating language adapters."""
    
    _registered_languages: Dict[str, type] = {}
    
    @classmethod
    def register_language(cls, language_code: str, adapter_class: type):
        """Register a language adapter class."""
        cls._registered_languages[language_code] = adapter_class
    
    @classmethod
    def create_adapter(cls, language_code: str) -> Optional[LanguageAdapter]:
        """Create a language adapter for the specified language."""
        if language_code not in cls._registered_languages:
            return None
        
        adapter_class = cls._registered_languages[language_code]
        return adapter_class()
    
    @classmethod
    def get_available_languages(cls) -> List[str]:
        """Get list of available language codes."""
        return list(cls._registered_languages.keys())
