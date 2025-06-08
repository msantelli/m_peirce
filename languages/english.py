"""
languages/english.py

English language implementation for the argument generator.
"""

from typing import Dict, List, Tuple, Optional, Set, Any
import re
from language_base import (
    LanguageSpecificPattern, LanguageTemplates, 
    LanguageGrammar, LanguageStyleGuide, LanguageAdapter
)
from linguistic_patterns import ComplexityLevel
from template_system import TemplateBuilder, EnhancedTemplate


class EnglishPattern(LanguageSpecificPattern):
    """English-specific linguistic patterns."""
    
    def __init__(self):
        super().__init__("en")
    
    def _init_negation_patterns(self) -> Dict[str, List[str]]:
        """Initialize English negation patterns."""
        return {
            "simple": [
                "{sentence} is not the case",
                "{sentence} is false",
                "not {sentence}",
                "{sentence} doesn't hold",
                "{sentence} is not true"
            ],
            "formal": [
                "it is false that {sentence}",
                "it is not the case that {sentence}",
                "the proposition that {sentence} is false",
                "it is not true that {sentence}",
                "the claim that {sentence} is false"
            ],
            "emphatic": [
                "{sentence} is definitely false",
                "{sentence} is certainly not the case",
                "{sentence} is absolutely false",
                "{sentence} is unquestionably false",
                "there is no way that {sentence}"
            ],
            "double": [
                "it is not the case that {sentence} is false",
                "it is false that {sentence} is not true",
                "{sentence} is not not the case",
                "it isn't false that {sentence}"
            ],
            "colloquial": [
                "{sentence} isn't true",
                "{sentence} ain't happening",
                "no way {sentence}",
                "{sentence} is not a thing",
                "forget about {sentence}"
            ],
            "semantic": [
                "the opposite of {sentence} is true",
                "{sentence} fails to be the case",
                "the negation of {sentence} holds",
                "{sentence} is absent",
                "there is an absence of {sentence}"
            ],
            "contrastive": [
                "contrary to {sentence}",
                "rather than {sentence}",
                "instead of {sentence}",
                "not {sentence}, but its opposite",
                "the reverse of {sentence}"
            ]
        }
    
    def _init_conjunction_patterns(self) -> Dict[str, List[str]]:
        """Initialize English conjunction patterns."""
        return {
            "simple": [
                "{p} and {q}",
                "{p}, and {q}",
                "both {p} and {q}",
                "{p} as well as {q}",
                "{p} along with {q}"
            ],
            "sequential": [
                "{p}, and also {q}",
                "{p}, moreover {q}",
                "{p}, furthermore {q}",
                "{p}, in addition {q}",
                "{p}, plus {q}"
            ],
            "emphatic": [
                "both {p} and {q}",
                "not only {p} but also {q}",
                "{p} and, equally, {q}",
                "{p} together with {q}",
                "{p} combined with {q}"
            ],
            "formal": [
                "{p} in conjunction with {q}",
                "{p} conjoined with {q}",
                "the conjunction of {p} and {q}",
                "{p} and simultaneously {q}",
                "{p} concurrently with {q}"
            ],
            "causal": [
                "{p}, and consequently {q}",
                "{p}, and as a result {q}",
                "{p}, which leads to {q}",
                "{p}, thereby {q}",
                "{p}, hence also {q}"
            ],
            "temporal": [
                "{p}, and then {q}",
                "{p}, followed by {q}",
                "{p}, and subsequently {q}",
                "{p}, after which {q}",
                "first {p}, then {q}"
            ],
            "additive": [
                "not only {p} but also {q}",
                "{p}, and what's more, {q}",
                "{p}, and additionally {q}",
                "{p}, and on top of that {q}",
                "{p}, and besides {q}"
            ]
        }
    
    def _init_disjunction_patterns(self) -> Dict[str, List[str]]:
        """Initialize English disjunction patterns."""
        return {
            "inclusive": [
                "{p} or {q}",
                "{p}, or {q}",
                "either {p} or {q} or both",
                "{p} and/or {q}",
                "{p} or alternatively {q}"
            ],
            "exclusive": [
                "either {p} or {q} but not both",
                "exactly one of {p} or {q}",
                "{p} or {q}, but not both",
                "either {p} or {q} (exclusive)",
                "{p} xor {q}"
            ],
            "alternative": [
                "{p}, alternatively {q}",
                "{p}, or else {q}",
                "{p}, otherwise {q}",
                "{p}, or instead {q}",
                "{p}, failing that {q}"
            ],
            "formal": [
                "{p} or else {q}",
                "the disjunction of {p} and {q}",
                "{p} vel {q}",
                "at least one of {p} or {q}",
                "{p} or possibly {q}"
            ],
            "conditional": [
                "{p}, unless {q}",
                "{p} except if {q}",
                "{p} if not {q}",
                "{p} barring {q}",
                "{p} save for {q}"
            ],
            "preferential": [
                "{p}, or failing that, {q}",
                "preferably {p}, otherwise {q}",
                "{p} if possible, else {q}",
                "ideally {p}, but {q} will do",
                "first choice {p}, second choice {q}"
            ],
            "exhaustive": [
                "it's either {p} or it's {q}",
                "one of two things: {p} or {q}",
                "the options are {p} or {q}",
                "we have {p} or we have {q}",
                "the choice is between {p} and {q}"
            ]
        }
    
    def _init_conditional_patterns(self) -> Dict[str, List[str]]:
        """Initialize English conditional patterns."""
        return {
            "standard": [
                "if {antecedent}, then {consequent}",
                "if {antecedent} then {consequent}",
                "{consequent} if {antecedent}",
                "given {antecedent}, {consequent}",
                "when {antecedent}, {consequent}"
            ],
            "temporal": [
                "when {antecedent}, then {consequent}",
                "whenever {antecedent}, {consequent}",
                "once {antecedent}, {consequent}",
                "as soon as {antecedent}, {consequent}",
                "after {antecedent}, {consequent}"
            ],
            "causal": [
                "because {antecedent}, {consequent}",
                "{antecedent} causes {consequent}",
                "{antecedent} leads to {consequent}",
                "{antecedent} results in {consequent}",
                "{antecedent} brings about {consequent}"
            ],
            "hypothetical": [
                "supposing {antecedent}, {consequent}",
                "assuming {antecedent}, {consequent}",
                "provided that {antecedent}, {consequent}",
                "on the condition that {antecedent}, {consequent}",
                "in the event that {antecedent}, {consequent}"
            ],
            "necessity": [
                "{consequent} is necessary for {antecedent}",
                "{antecedent} requires {consequent}",
                "without {consequent}, no {antecedent}",
                "{antecedent} only if {consequent}",
                "for {antecedent}, {consequent} is required"
            ],
            "sufficiency": [
                "{antecedent} is sufficient for {consequent}",
                "{antecedent} guarantees {consequent}",
                "{antecedent} ensures {consequent}",
                "{antecedent} implies {consequent}",
                "{antecedent} entails {consequent}"
            ],
            "biconditional_hint": [
                "{antecedent} exactly when {consequent}",
                "{antecedent} if and only if {consequent}",
                "{antecedent} just in case {consequent}",
                "{antecedent} precisely when {consequent}",
                "{antecedent} iff {consequent}"
            ],
            "probabilistic": [
                "if {antecedent}, then probably {consequent}",
                "if {antecedent}, then likely {consequent}",
                "{antecedent} suggests {consequent}",
                "{antecedent} indicates {consequent}",
                "given {antecedent}, {consequent} is likely"
            ]
        }
    
    def _init_connectives(self) -> Dict[str, List[str]]:
        """Initialize English logical connectives."""
        return {
            "conclusion": [
                "therefore", "thus", "hence", "consequently",
                "so", "accordingly", "as a result", "it follows that",
                "we can conclude that", "this means that", "ergo"
            ],
            "premise": [
                "since", "because", "as", "given that",
                "considering that", "in light of", "due to",
                "on account of", "for", "seeing that"
            ],
            "assumption": [
                "suppose", "assume", "let's say", "imagine",
                "consider", "posit", "grant that", "presuming"
            ],
            "contrast": [
                "but", "however", "yet", "nevertheless",
                "nonetheless", "still", "although", "though",
                "despite", "in spite of"
            ],
            "addition": [
                "and", "also", "moreover", "furthermore",
                "additionally", "besides", "plus", "as well as",
                "in addition", "what's more"
            ]
        }
    
    def format_sentence(self, sentence: str, formatting_type: str) -> str:
        """Apply English-specific formatting."""
        if formatting_type == "capitalize":
            return self.capitalize_sentence(sentence)
        elif formatting_type == "negate":
            return self._simple_negate(sentence)
        elif formatting_type == "question":
            return self._make_question(sentence)
        elif formatting_type == "emphasize":
            return self._emphasize(sentence)
        return sentence
    
    def normalize_sentence(self, sentence: str) -> str:
        """Normalize an English sentence."""
        # Remove trailing punctuation
        sentence = sentence.rstrip('.!?;:,')
        
        # Convert to lowercase
        sentence = sentence.lower()
        
        # Remove extra whitespace
        sentence = ' '.join(sentence.split())
        
        return sentence
    
    def capitalize_sentence(self, sentence: str) -> str:
        """Capitalize an English sentence properly."""
        if not sentence:
            return sentence
        
        # Simple capitalization - first letter
        # Could be enhanced to handle proper nouns, 'I', etc.
        return sentence[0].upper() + sentence[1:]
    
    def _simple_negate(self, sentence: str) -> str:
        """Apply simple negation to a sentence."""
        # Very basic - could be enhanced with NLP
        if " is " in sentence:
            return sentence.replace(" is ", " is not ", 1)
        elif " are " in sentence:
            return sentence.replace(" are ", " are not ", 1)
        elif " was " in sentence:
            return sentence.replace(" was ", " was not ", 1)
        elif " were " in sentence:
            return sentence.replace(" were ", " were not ", 1)
        else:
            return f"it is not the case that {sentence}"
    
    def _make_question(self, sentence: str) -> str:
        """Convert a statement to a question."""
        # Very basic - could be enhanced
        if sentence.startswith(("is ", "are ", "was ", "were ")):
            return sentence + "?"
        else:
            return f"is it true that {sentence}?"
    
    def _emphasize(self, sentence: str) -> str:
        """Add emphasis to a sentence."""
        return f"certainly {sentence}"


class EnglishTemplates(LanguageTemplates):
    """English-specific argument templates."""
    
    def __init__(self, language_pattern: EnglishPattern):
        super().__init__(language_pattern)
    
    def _init_templates(self) -> Dict[str, Dict[str, List[EnhancedTemplate]]]:
        """Initialize English templates."""
        templates = {}
        
        # Modus Ponens
        templates["Modus Ponens"] = {
            "valid": self._create_modus_ponens_valid(),
            "invalid": self._create_modus_ponens_invalid()
        }
        
        # Modus Tollens
        templates["Modus Tollens"] = {
            "valid": self._create_modus_tollens_valid(),
            "invalid": self._create_modus_tollens_invalid()
        }
        
        # Disjunctive Syllogism
        templates["Disjunctive Syllogism"] = {
            "valid": self._create_disjunctive_syllogism_valid(),
            "invalid": self._create_disjunctive_syllogism_invalid()
        }
        
        # Conjunction Introduction
        templates["Conjunction Introduction"] = {
            "valid": self._create_conjunction_introduction_valid(),
            "invalid": self._create_conjunction_introduction_invalid()
        }
        
        # Conjunction Elimination
        templates["Conjunction Elimination"] = {
            "valid": self._create_conjunction_elimination_valid(),
            "invalid": self._create_conjunction_elimination_invalid()
        }
        
        # Disjunction Introduction
        templates["Disjunction Introduction"] = {
            "valid": self._create_disjunction_introduction_valid(),
            "invalid": self._create_invalid_conjunction_introduction()
        }
        
        # Hypothetical Syllogism
        templates["Hypothetical Syllogism"] = {
            "valid": self._create_hypothetical_syllogism_valid(),
            "invalid": self._create_hypothetical_syllogism_invalid()
        }
        
        # Disjunction Elimination
        templates["Disjunction Elimination"] = {
            "valid": self._create_disjunction_elimination_valid(),
            "invalid": self._create_disjunction_elimination_invalid()
        }
        
        # Material Conditional Introduction
        templates["Material Conditional Introduction"] = {
            "valid": self._create_material_conditional_introduction_valid(),
            "invalid": self._create_material_conditional_introduction_invalid()
        }
        
        # Constructive Dilemma
        templates["Constructive Dilemma"] = {
            "valid": self._create_constructive_dilemma_valid(),
            "invalid": self._create_constructive_dilemma_invalid()
        }
        
        # Destructive Dilemma
        templates["Destructive Dilemma"] = {
            "valid": self._create_destructive_dilemma_valid(),
            "invalid": self._create_destructive_dilemma_invalid()
        }
        
        # Invalid forms
        templates["Affirming the Consequent"] = {
            "invalid": self._create_modus_ponens_invalid()
        }
        
        templates["Denying the Antecedent"] = {
            "invalid": self._create_modus_tollens_invalid()
        }
        
        templates["Affirming a Disjunct"] = {
            "invalid": self._create_disjunctive_syllogism_invalid()
        }
        
        templates["False Conjunction"] = {
            "invalid": self._create_conjunction_introduction_invalid()
        }
        
        templates["Composition Fallacy"] = {
            "invalid": self._create_conjunction_elimination_invalid()
        }
        
        templates["Invalid Conjunction Introduction"] = {
            "invalid": self._create_invalid_conjunction_introduction()
        }
        
        templates["Non Sequitur"] = {
            "invalid": self._create_non_sequitur_invalid()
        }
        
        templates["Invalid Disjunction Elimination"] = {
            "invalid": self._create_disjunction_elimination_invalid()
        }
        
        return templates
    
    def _create_modus_ponens_valid(self) -> List[EnhancedTemplate]:
        """Create valid Modus Ponens templates."""
        templates = []
        
        # Basic template with variations
        builder = TemplateBuilder()
        builder.add_variation('conditional', [
            'If {p}, then {q}',
            '{Q} if {p}',
            '{P} implies {q}',
            '{P} leads to {q}',
            '{P} guarantees {q}'
        ])
        builder.add_static('. ')
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Therefore',
            'Thus',
            'Hence',
            'So',
            'Consequently'
        ])
        builder.add_static(', ')
        builder.add_variable('q')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        
        templates.append(builder.build())
        
        # Conclusion-first variation
        builder2 = TemplateBuilder()
        builder2.add_variable('Q')
        builder2.add_static(' ')
        builder2.add_variation('because', [
            'because',
            'since',
            'as',
            'given that'
        ])
        builder2.add_static(' ')
        builder2.add_variable('p')
        builder2.add_static('. ')
        builder2.add_variation('also', [
            'Also',
            'Moreover',
            'Furthermore',
            'Additionally'
        ])
        builder2.add_static(', ')
        builder2.add_variation('conditional', [
            'if {p}, then {q}',
            '{P} implies {q}',
            '{P} leads to {q}'
        ])
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        
        templates.append(builder2.build())
        
        return templates
    
    def _create_modus_ponens_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Modus Ponens templates (Affirming the Consequent)."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('conditional', [
            'If {p}, then {q}',
            '{Q} if {p}',
            '{P} implies {q}'
        ])
        builder.add_static('. ')
        builder.add_variable('Q')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Therefore',
            'Thus',
            'So'
        ])
        builder.add_static(', ')
        builder.add_variable('p')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        
        templates.append(builder.build())
        
        return templates
    
    def _create_modus_tollens_valid(self) -> List[EnhancedTemplate]:
        """Create valid Modus Tollens templates."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('conditional', [
            'If {p}, then {q}',
            '{Q} if {p}',
            '{P} implies {q}'
        ])
        builder.add_static('. ')
        builder.add_variable('not_Q')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Therefore',
            'Thus',
            'Hence'
        ])
        builder.add_static(', ')
        builder.add_variable('not_p')
        builder.add_static('.')
        
        templates.append(builder.build())
        
        return templates
    
    def _create_modus_tollens_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Modus Tollens templates (Denying the Antecedent)."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('conditional', [
            'If {p}, then {q}',
            '{Q} if {p}',
            '{P} implies {q}'
        ])
        builder.add_static('. ')
        builder.add_variable('not_P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Therefore',
            'Thus',
            'So'
        ])
        builder.add_static(', ')
        builder.add_variable('not_q')
        builder.add_static('.')
        
        templates.append(builder.build())
        
        return templates
    
    def _create_disjunctive_syllogism_valid(self) -> List[EnhancedTemplate]:
        """Create valid Disjunctive Syllogism templates."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('disjunction', [
            '{P} or {q}',
            'Either {p} or {q}',
            '{P}, or alternatively {q}'
        ])
        builder.add_static('. ')
        builder.add_variable('not_P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Therefore',
            'Thus',
            'Hence'
        ])
        builder.add_static(', ')
        builder.add_variable('q')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_disjunctive_syllogism_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Disjunctive Syllogism templates (Affirming a Disjunct)."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('disjunction', [
            '{P} or {q}',
            'Either {p} or {q}'
        ])
        builder.add_static('. ')
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Therefore',
            'Thus'
        ])
        builder.add_static(', ')
        builder.add_variable('not_q')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_conjunction_introduction_valid(self) -> List[EnhancedTemplate]:
        """Create valid Conjunction Introduction templates."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variable('Q')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Therefore',
            'Thus',
            'Hence'
        ])
        builder.add_static(', ')
        builder.add_variation('conjunction', [
            '{p} and {q}',
            'both {p} and {q}',
            '{p} as well as {q}'
        ])
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_conjunction_introduction_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Conjunction Introduction templates (False Conjunction)."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Therefore',
            'Thus'
        ])
        builder.add_static(', ')
        builder.add_variation('conjunction', [
            '{p} and {q}',
            'both {p} and {q}'
        ])
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_conjunction_elimination_valid(self) -> List[EnhancedTemplate]:
        """Create valid Conjunction Elimination templates."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('conjunction', [
            '{P} and {q}',
            'Both {p} and {q}',
            '{P} as well as {q}'
        ])
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Therefore',
            'Thus',
            'Hence'
        ])
        builder.add_static(', ')
        builder.add_variable('p')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_conjunction_elimination_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Conjunction Elimination templates (Composition Fallacy)."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('conjunction', [
            '{P} and {q}',
            'Both {p} and {q}'
        ])
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Therefore',
            'Thus'
        ])
        builder.add_static(', ')
        builder.add_variable('r')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_disjunction_introduction_valid(self) -> List[EnhancedTemplate]:
        """Create valid Disjunction Introduction templates."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Therefore',
            'Thus',
            'Hence'
        ])
        builder.add_static(', ')
        builder.add_variation('disjunction', [
            '{p} or {q}',
            'either {p} or {q}',
            '{p} or alternatively {q}'
        ])
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_invalid_conjunction_introduction(self) -> List[EnhancedTemplate]:
        """Create Invalid Conjunction Introduction templates (A / Therefore, A and B)."""
        templates = []
        
        # Basic invalid conjunction introduction
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Therefore',
            'Thus',
            'Hence',
            'So'
        ])
        builder.add_static(', ')
        builder.add_variation('conjunction', [
            '{p} and {q}',
            'both {p} and {q}',
            '{p} as well as {q}'
        ])
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        # Intermediate version with more sophisticated language
        builder2 = TemplateBuilder()
        builder2.add_variable('P')
        builder2.add_static('. ')
        builder2.add_variation('conclusion', [
            'It follows that',
            'We can conclude that',
            'This means that'
        ])
        builder2.add_static(' ')
        builder2.add_variation('conjunction', [
            'not only {p} but also {q}',
            '{p} and additionally {q}',
            '{p} together with {q}'
        ])
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        templates.append(builder2.build())
        
        return templates
    
    def _create_hypothetical_syllogism_valid(self) -> List[EnhancedTemplate]:
        """Create valid Hypothetical Syllogism templates."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('conditional1', [
            'If {p}, then {q}',
            '{P} implies {q}'
        ])
        builder.add_static('. ')
        builder.add_variation('conditional2', [
            'If {q}, then {r}',
            '{Q} implies {r}'
        ])
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Therefore',
            'Thus',
            'Hence'
        ])
        builder.add_static(', ')
        builder.add_variation('conditional3', [
            'If {p}, then {r}',
            '{P} implies {r}'
        ])
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_hypothetical_syllogism_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Hypothetical Syllogism templates (Non Sequitur)."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('conditional1', [
            'If {p}, then {q}',
            '{P} implies {q}'
        ])
        builder.add_static('. ')
        builder.add_variation('conditional2', [
            'If {q}, then {r}',
            '{Q} implies {r}'
        ])
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Therefore',
            'Thus'
        ])
        builder.add_static(', ')
        builder.add_variable('not_p')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_disjunction_elimination_valid(self) -> List[EnhancedTemplate]:
        """Create valid Disjunction Elimination templates."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('disjunction', [
            '{P} or {q}',
            'Either {p} or {q}'
        ])
        builder.add_static('. ')
        builder.add_variation('conditional1', [
            'If {p}, then {r}',
            '{P} implies {r}'
        ])
        builder.add_static('. ')
        builder.add_variation('conditional2', [
            'If {q}, then {r}',
            '{Q} implies {r}'
        ])
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Therefore',
            'Thus',
            'Hence'
        ])
        builder.add_static(', ')
        builder.add_variable('r')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_disjunction_elimination_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Disjunction Elimination templates."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('disjunction', [
            '{P} or {q}',
            'Either {p} or {q}'
        ])
        builder.add_static('. ')
        builder.add_variation('conditional1', [
            'If {p}, then {r}',
            '{P} implies {r}'
        ])
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Therefore',
            'Thus'
        ])
        builder.add_static(', ')
        builder.add_variable('r')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_material_conditional_introduction_valid(self) -> List[EnhancedTemplate]:
        """Create valid Material Conditional Introduction templates."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static(' implies ')
        builder.add_variable('q')
        builder.add_static('. ')
        builder.add_variable('Q')
        builder.add_static(' implies ')
        builder.add_variable('r')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Therefore',
            'Thus',
            'Hence'
        ])
        builder.add_static(', ')
        builder.add_variation('conditional', [
            'If {p}, then {r}',
            '{P} implies {r}'
        ])
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_material_conditional_introduction_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Material Conditional Introduction templates (Non Sequitur)."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static(' implies ')
        builder.add_variable('q')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Therefore',
            'Thus'
        ])
        builder.add_static(', ')
        builder.add_variable('r')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_constructive_dilemma_valid(self) -> List[EnhancedTemplate]:
        """Create valid Constructive Dilemma templates."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('conditional1', [
            'If {p}, then {q}',
            '{P} implies {q}'
        ])
        builder.add_static('. ')
        builder.add_variation('conditional2', [
            'If {r}, then {s}',
            '{R} implies {s}'
        ])
        builder.add_static('. ')
        builder.add_variation('disjunction', [
            '{P} or {r}',
            'Either {p} or {r}'
        ])
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Therefore',
            'Thus',
            'Hence'
        ])
        builder.add_static(', ')
        builder.add_variation('conclusion_disjunction', [
            '{q} or {s}',
            'Either {q} or {s}'
        ])
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_constructive_dilemma_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Constructive Dilemma templates (False Dilemma)."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('conditional1', [
            'If {p}, then {q}',
            '{p} implies {q}'
        ])
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Therefore',
            'Thus'
        ])
        builder.add_static(', ')
        builder.add_variation('false_disjunction', [
            'either {p} or {r}',
            'it must be {p} or {r}'
        ])
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_destructive_dilemma_valid(self) -> List[EnhancedTemplate]:
        """Create valid Destructive Dilemma templates."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('conditional1', [
            'If {p}, then {q}',
            '{P} implies {q}'
        ])
        builder.add_static('. ')
        builder.add_variation('conditional2', [
            'If {r}, then {s}',
            '{R} implies {s}'
        ])
        builder.add_static('. ')
        builder.add_variation('disjunction', [
            '{not_q} or {not_s}',
            'Either {not_q} or {not_s}'
        ])
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Therefore',
            'Thus',
            'Hence'
        ])
        builder.add_static(', ')
        builder.add_variation('conclusion_disjunction', [
            '{not_p} or {not_r}',
            'Either {not_p} or {not_r}'
        ])
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_destructive_dilemma_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Destructive Dilemma templates (Non Sequitur)."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('conditional1', [
            'If {p}, then {q}',
            '{P} implies {q}'
        ])
        builder.add_static('. ')
        builder.add_variation('conditional2', [
            'If {r}, then {s}',
            '{R} implies {s}'
        ])
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Therefore',
            'Thus'
        ])
        builder.add_static(', ')
        builder.add_variable('not_p')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_non_sequitur_invalid(self) -> List[EnhancedTemplate]:
        """Create Non Sequitur templates (generic invalid reasoning)."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Therefore',
            'Thus',
            'So'
        ])
        builder.add_static(', ')
        builder.add_variable('q')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def get_required_sentences(self, rule_name: str) -> int:
        """Get required sentences for a rule."""
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
        return requirements.get(rule_name, 2)
    
    def get_template_variables(self, rule_name: str) -> Set[str]:
        """Get variables used in templates for a rule."""
        # This would analyze templates to extract variables
        # For now, returning common ones
        basic_vars = {'p', 'q', 'P', 'Q'}
        
        if rule_name in ["Modus Tollens", "Destructive Dilemma"]:
            basic_vars.update({'not_p', 'not_q', 'not_P', 'not_Q'})
        
        if rule_name in ["Hypothetical Syllogism", "Constructive Dilemma"]:
            basic_vars.update({'r', 'R'})
        
        if rule_name in ["Disjunction Elimination", "Destructive Dilemma"]:
            basic_vars.update({'s', 'S'})
        
        return basic_vars


class EnglishGrammar(LanguageGrammar):
    """English grammar rules."""
    
    def __init__(self):
        super().__init__("en")
    
    def apply_agreement(self, subject: str, verb: str, 
                       object: Optional[str] = None) -> Tuple[str, str, Optional[str]]:
        """Apply subject-verb agreement."""
        # Simplified - would need more sophisticated NLP
        # Check if subject is plural
        if subject.endswith('s') and not subject.endswith(('ss', 'us')):
            # Likely plural
            if verb == "is":
                verb = "are"
            elif verb == "was":
                verb = "were"
            elif verb == "has":
                verb = "have"
        
        return subject, verb, object
    
    def apply_article_rules(self, noun: str, definite: bool = False) -> str:
        """Apply article rules."""
        if definite:
            return f"the {noun}"
        else:
            # Check if noun starts with vowel sound
            if noun and noun[0].lower() in 'aeiou':
                return f"an {noun}"
            else:
                return f"a {noun}"
    
    def apply_word_order(self, components: Dict[str, str]) -> str:
        """Apply English SVO word order."""
        # Standard order: Subject Verb Object
        parts = []
        
        if 'subject' in components:
            parts.append(components['subject'])
        if 'verb' in components:
            parts.append(components['verb'])
        if 'object' in components:
            parts.append(components['object'])
        
        # Add other components
        for key, value in components.items():
            if key not in ['subject', 'verb', 'object']:
                parts.append(value)
        
        return ' '.join(parts)
    
    def pluralize(self, word: str, count: int = 2) -> str:
        """Pluralize a word."""
        if count == 1:
            return word
        
        # Basic pluralization rules
        if word.endswith(('s', 'ss', 'sh', 'ch', 'x', 'z')):
            return word + 'es'
        elif word.endswith('y') and len(word) > 1 and word[-2] not in 'aeiou':
            return word[:-1] + 'ies'
        elif word.endswith('f'):
            return word[:-1] + 'ves'
        elif word.endswith('fe'):
            return word[:-2] + 'ves'
        else:
            return word + 's'
    
    def apply_case(self, word: str, case: str) -> str:
        """English doesn't have cases like other languages."""
        # English only has case for pronouns
        pronoun_cases = {
            'I': {'nominative': 'I', 'accusative': 'me', 'possessive': 'my'},
            'you': {'nominative': 'you', 'accusative': 'you', 'possessive': 'your'},
            'he': {'nominative': 'he', 'accusative': 'him', 'possessive': 'his'},
            'she': {'nominative': 'she', 'accusative': 'her', 'possessive': 'her'},
            'it': {'nominative': 'it', 'accusative': 'it', 'possessive': 'its'},
            'we': {'nominative': 'we', 'accusative': 'us', 'possessive': 'our'},
            'they': {'nominative': 'they', 'accusative': 'them', 'possessive': 'their'}
        }
        
        if word.lower() in pronoun_cases:
            return pronoun_cases[word.lower()].get(case, word)
        
        return word


class EnglishStyleGuide(LanguageStyleGuide):
    """English style guide."""
    
    def __init__(self):
        super().__init__("en")
    
    def _init_formality_levels(self) -> Dict[str, Dict[str, Any]]:
        """Initialize formality levels."""
        return {
            "casual": {
                "contractions": True,
                "slang": True,
                "idioms": True,
                "sentence_starters": ["So", "Well", "Anyway", "Look"],
                "connectives": ["and", "but", "so", "'cause"]
            },
            "neutral": {
                "contractions": False,
                "slang": False,
                "idioms": True,
                "sentence_starters": [],
                "connectives": ["and", "but", "therefore", "because"]
            },
            "formal": {
                "contractions": False,
                "slang": False,
                "idioms": False,
                "sentence_starters": ["Furthermore", "Moreover", "Additionally"],
                "connectives": ["and", "however", "therefore", "because", "consequently"]
            },
            "academic": {
                "contractions": False,
                "slang": False,
                "idioms": False,
                "passive_voice": True,
                "hedging": True,
                "sentence_starters": ["It can be argued that", "Research suggests that"],
                "connectives": ["furthermore", "however", "therefore", "thus", "consequently"]
            }
        }
    
    def apply_formality(self, text: str, formality_level: str) -> str:
        """Apply formality transformations."""
        if formality_level not in self.formality_levels:
            return text
        
        rules = self.formality_levels[formality_level]
        
        # Apply contractions
        if not rules.get("contractions", True):
            text = self._expand_contractions(text)
        
        # Apply hedging for academic style
        if rules.get("hedging", False):
            text = self._add_hedging(text)
        
        return text
    
    def get_domain_specific_style(self, domain: str) -> Dict[str, Any]:
        """Get domain-specific style preferences."""
        domain_styles = {
            "legal": {
                "precision": "high",
                "qualifiers": ["pursuant to", "notwithstanding", "whereas"],
                "avoid": ["probably", "maybe", "sort of"],
                "prefer_passive": True
            },
            "scientific": {
                "precision": "high",
                "objectivity": True,
                "avoid_personal": True,
                "prefer_passive": True,
                "units": "metric"
            },
            "everyday": {
                "precision": "medium",
                "contractions": True,
                "idioms": True,
                "prefer_active": True
            },
            "literary": {
                "metaphors": True,
                "varied_vocabulary": True,
                "emotional_language": True,
                "prefer_active": True
            }
        }
        
        return domain_styles.get(domain, {})
    
    def apply_rhetorical_emphasis(self, text: str, emphasis_type: str) -> str:
        """Apply rhetorical emphasis."""
        emphasis_patterns = {
            "strong": lambda t: f"It is absolutely certain that {t}",
            "subtle": lambda t: f"It would seem that {t}",
            "questioning": lambda t: f"Is it not the case that {t}?",
            "dramatic": lambda t: f"Indeed, {t}!",
            "understated": lambda t: f"One might say that {t}"
        }
        
        if emphasis_type in emphasis_patterns:
            return emphasis_patterns[emphasis_type](text)
        
        return text
    
    def _expand_contractions(self, text: str) -> str:
        """Expand contractions."""
        contractions = {
            "isn't": "is not",
            "aren't": "are not",
            "wasn't": "was not",
            "weren't": "were not",
            "haven't": "have not",
            "hasn't": "has not",
            "hadn't": "had not",
            "won't": "will not",
            "wouldn't": "would not",
            "don't": "do not",
            "doesn't": "does not",
            "didn't": "did not",
            "can't": "cannot",
            "couldn't": "could not",
            "shouldn't": "should not",
            "mightn't": "might not",
            "mustn't": "must not"
        }
        
        for contraction, expansion in contractions.items():
            text = text.replace(contraction, expansion)
            text = text.replace(contraction.capitalize(), expansion.capitalize())
        
        return text
    
    def _add_hedging(self, text: str) -> str:
        """Add academic hedging."""
        hedges = [
            "it appears that",
            "it seems that",
            "arguably",
            "possibly",
            "it could be argued that"
        ]
        
        # Simple implementation - prepend hedge
        import random
        hedge = random.choice(hedges)
        return f"{hedge} {text}"


class EnglishLanguageAdapter(LanguageAdapter):
    """Complete English language adapter."""
    
    def __init__(self):
        pattern = EnglishPattern()
        templates = EnglishTemplates(pattern)
        grammar = EnglishGrammar()
        style_guide = EnglishStyleGuide()
        
        super().__init__(pattern, templates, grammar, style_guide)


# Register the English adapter
from language_base import LanguageFactory
LanguageFactory.register_language("en", EnglishLanguageAdapter)