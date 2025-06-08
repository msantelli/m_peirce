"""
languages/english_enhanced.py

Complete English language implementation with all inference rules,
complexity levels, and domain-specific variations.
"""

from typing import Dict, List, Tuple, Optional, Set, Any
import re
import random
from language_base import (
    LanguageSpecificPattern, LanguageTemplates, 
    LanguageGrammar, LanguageStyleGuide, LanguageAdapter
)
from linguistic_patterns import ComplexityLevel, VariationType
from template_system import TemplateBuilder, EnhancedTemplate, VariationLibrary


class EnhancedEnglishPattern(LanguageSpecificPattern):
    """Enhanced English-specific linguistic patterns with full variation support."""
    
    def __init__(self):
        super().__init__("en")
        self.variation_library = VariationLibrary()
        self._init_extended_variations()
    
    def _init_extended_variations(self):
        """Initialize extended variations for richer expression."""
        # Extended negation patterns by complexity
        self.negation_by_complexity = {
            ComplexityLevel.BASIC: ["simple", "colloquial"],
            ComplexityLevel.INTERMEDIATE: ["simple", "formal", "contrastive"],
            ComplexityLevel.ADVANCED: ["formal", "emphatic", "semantic"],
            ComplexityLevel.EXPERT: ["formal", "double", "semantic", "philosophical"]
        }
        
        # Extended conditional patterns by domain
        self.conditional_by_domain = {
            "scientific": ["causal", "sufficiency", "necessity", "probabilistic"],
            "legal": ["standard", "hypothetical", "necessity", "conditional_precedent"],
            "everyday": ["standard", "temporal", "causal", "colloquial"],
            "philosophical": ["standard", "necessity", "sufficiency", "biconditional_hint"],
            "mathematical": ["standard", "biconditional_hint", "sufficiency", "equivalence"]
        }
    
    def _init_negation_patterns(self) -> Dict[str, List[str]]:
        """Initialize comprehensive English negation patterns."""
        return {
            "simple": [
                "{sentence} is not the case",
                "{sentence} is false",
                "not {sentence}",
                "{sentence} doesn't hold",
                "{sentence} is not true",
                "{sentence} fails"
            ],
            "formal": [
                "it is false that {sentence}",
                "it is not the case that {sentence}",
                "the proposition that {sentence} is false",
                "it is not true that {sentence}",
                "the claim that {sentence} is false",
                "the statement that {sentence} does not hold"
            ],
            "emphatic": [
                "{sentence} is definitely false",
                "{sentence} is certainly not the case",
                "{sentence} is absolutely false",
                "{sentence} is unquestionably false",
                "there is no way that {sentence}",
                "{sentence} is categorically false",
                "under no circumstances is {sentence} true"
            ],
            "double": [
                "it is not the case that {sentence} is false",
                "it is false that {sentence} is not true",
                "{sentence} is not not the case",
                "it isn't false that {sentence}",
                "it cannot be denied that {sentence}",
                "one cannot say that {sentence} is false"
            ],
            "colloquial": [
                "{sentence} isn't true",
                "{sentence} ain't happening",
                "no way {sentence}",
                "{sentence} is not a thing",
                "forget about {sentence}",
                "{sentence} is bogus",
                "yeah right, {sentence}"
            ],
            "semantic": [
                "the opposite of {sentence} is true",
                "{sentence} fails to be the case",
                "the negation of {sentence} holds",
                "{sentence} is absent",
                "there is an absence of {sentence}",
                "{sentence} does not obtain",
                "the contradiction of {sentence} is true"
            ],
            "contrastive": [
                "contrary to {sentence}",
                "rather than {sentence}",
                "instead of {sentence}",
                "not {sentence}, but its opposite",
                "the reverse of {sentence}",
                "as opposed to {sentence}",
                "in contrast to {sentence}"
            ],
            "philosophical": [
                "the truth value of {sentence} is false",
                "{sentence} lacks truth",
                "the proposition {sentence} fails to correspond to reality",
                "{sentence} is without truth value",
                "there is no state of affairs in which {sentence}",
                "{sentence} has no truth-maker"
            ]
        }
    
    def _init_conjunction_patterns(self) -> Dict[str, List[str]]:
        """Initialize comprehensive English conjunction patterns."""
        return {
            "simple": [
                "{p} and {q}",
                "{p}, and {q}",
                "both {p} and {q}",
                "{p} as well as {q}",
                "{p} along with {q}",
                "{p} plus {q}"
            ],
            "sequential": [
                "{p}, and also {q}",
                "{p}, moreover {q}",
                "{p}, furthermore {q}",
                "{p}, in addition {q}",
                "{p}, plus {q}",
                "{p}, and what's more, {q}",
                "{p}, additionally {q}"
            ],
            "emphatic": [
                "both {p} and {q}",
                "not only {p} but also {q}",
                "{p} and, equally, {q}",
                "{p} together with {q}",
                "{p} combined with {q}",
                "{p} as well as {q}, both being true",
                "the combination of {p} and {q}"
            ],
            "formal": [
                "{p} in conjunction with {q}",
                "{p} conjoined with {q}",
                "the conjunction of {p} and {q}",
                "{p} and simultaneously {q}",
                "{p} concurrently with {q}",
                "both propositions {p} and {q}",
                "{p} & {q}"
            ],
            "causal": [
                "{p}, and consequently {q}",
                "{p}, and as a result {q}",
                "{p}, which leads to {q}",
                "{p}, thereby {q}",
                "{p}, hence also {q}",
                "{p}, and this causes {q}",
                "{p}, resulting in {q}"
            ],
            "temporal": [
                "{p}, and then {q}",
                "{p}, followed by {q}",
                "{p}, and subsequently {q}",
                "{p}, after which {q}",
                "first {p}, then {q}",
                "{p}, and afterwards {q}",
                "{p} preceding {q}"
            ],
            "additive": [
                "not only {p} but also {q}",
                "{p}, and what's more, {q}",
                "{p}, and additionally {q}",
                "{p}, and on top of that {q}",
                "{p}, and besides {q}",
                "{p}, and to boot {q}",
                "{p}, and furthermore {q} as well"
            ],
            "logical": [
                "{p} ∧ {q}",
                "({p}) AND ({q})",
                "{p} & {q}",
                "the logical conjunction of {p} and {q}",
                "{p} AND {q} are both true",
                "the truth of both {p} and {q}"
            ],
            "balanced": [
                "on one hand {p}, and on the other {q}",
                "{p} on the one side, {q} on the other",
                "equally {p} and {q}",
                "{p} just as much as {q}",
                "{p} no less than {q}",
                "as much {p} as {q}"
            ]
        }
    
    def _init_disjunction_patterns(self) -> Dict[str, List[str]]:
        """Initialize comprehensive English disjunction patterns."""
        return {
            "inclusive": [
                "{p} or {q}",
                "{p}, or {q}",
                "either {p} or {q} or both",
                "{p} and/or {q}",
                "{p} or alternatively {q}",
                "{p} or possibly {q}",
                "at least one of {p} or {q}"
            ],
            "exclusive": [
                "either {p} or {q} but not both",
                "exactly one of {p} or {q}",
                "{p} or {q}, but not both",
                "either {p} or {q} (exclusive)",
                "{p} xor {q}",
                "{p} or else {q}, exclusively",
                "one and only one of {p} or {q}"
            ],
            "alternative": [
                "{p}, alternatively {q}",
                "{p}, or else {q}",
                "{p}, otherwise {q}",
                "{p}, or instead {q}",
                "{p}, failing that {q}",
                "{p}, if not then {q}",
                "{p}, or as an alternative {q}"
            ],
            "formal": [
                "{p} or else {q}",
                "the disjunction of {p} and {q}",
                "{p} vel {q}",
                "at least one of {p} or {q}",
                "{p} or possibly {q}",
                "either proposition {p} or proposition {q}",
                "{p} ∨ {q}"
            ],
            "conditional": [
                "{p}, unless {q}",
                "{p} except if {q}",
                "{p} if not {q}",
                "{p} barring {q}",
                "{p} save for {q}",
                "{p} except when {q}",
                "{p} provided not {q}"
            ],
            "preferential": [
                "{p}, or failing that, {q}",
                "preferably {p}, otherwise {q}",
                "{p} if possible, else {q}",
                "ideally {p}, but {q} will do",
                "first choice {p}, second choice {q}",
                "best case {p}, worst case {q}",
                "{p} by preference, {q} by necessity"
            ],
            "exhaustive": [
                "it's either {p} or it's {q}",
                "one of two things: {p} or {q}",
                "the options are {p} or {q}",
                "we have {p} or we have {q}",
                "the choice is between {p} and {q}",
                "there are two possibilities: {p} or {q}",
                "it must be either {p} or {q}"
            ],
            "logical": [
                "{p} ∨ {q}",
                "({p}) OR ({q})",
                "{p} | {q}",
                "the logical disjunction of {p} and {q}",
                "{p} OR {q} is true",
                "the truth of {p} or {q} or both"
            ],
            "uncertain": [
                "maybe {p} or maybe {q}",
                "possibly {p} or possibly {q}",
                "perhaps {p} or perhaps {q}",
                "it could be {p} or it could be {q}",
                "either {p} is possible or {q} is possible",
                "we might have {p} or we might have {q}"
            ]
        }
    
    def _init_conditional_patterns(self) -> Dict[str, List[str]]:
        """Initialize comprehensive English conditional patterns."""
        return {
            "standard": [
                "if {antecedent}, then {consequent}",
                "if {antecedent} then {consequent}",
                "{consequent} if {antecedent}",
                "given {antecedent}, {consequent}",
                "when {antecedent}, {consequent}",
                "{antecedent} → {consequent}",
                "should {antecedent}, then {consequent}"
            ],
            "temporal": [
                "when {antecedent}, then {consequent}",
                "whenever {antecedent}, {consequent}",
                "once {antecedent}, {consequent}",
                "as soon as {antecedent}, {consequent}",
                "after {antecedent}, {consequent}",
                "upon {antecedent}, {consequent}",
                "the moment {antecedent}, {consequent}"
            ],
            "causal": [
                "because {antecedent}, {consequent}",
                "{antecedent} causes {consequent}",
                "{antecedent} leads to {consequent}",
                "{antecedent} results in {consequent}",
                "{antecedent} brings about {consequent}",
                "{antecedent} produces {consequent}",
                "{antecedent} yields {consequent}",
                "due to {antecedent}, {consequent}"
            ],
            "hypothetical": [
                "supposing {antecedent}, {consequent}",
                "assuming {antecedent}, {consequent}",
                "provided that {antecedent}, {consequent}",
                "on the condition that {antecedent}, {consequent}",
                "in the event that {antecedent}, {consequent}",
                "in case {antecedent}, {consequent}",
                "should it be that {antecedent}, {consequent}"
            ],
            "necessity": [
                "{consequent} is necessary for {antecedent}",
                "{antecedent} requires {consequent}",
                "without {consequent}, no {antecedent}",
                "{antecedent} only if {consequent}",
                "for {antecedent}, {consequent} is required",
                "{antecedent} necessitates {consequent}",
                "there is no {antecedent} without {consequent}",
                "{antecedent} depends on {consequent}"
            ],
            "sufficiency": [
                "{antecedent} is sufficient for {consequent}",
                "{antecedent} guarantees {consequent}",
                "{antecedent} ensures {consequent}",
                "{antecedent} implies {consequent}",
                "{antecedent} entails {consequent}",
                "{antecedent} is enough for {consequent}",
                "{antecedent} suffices for {consequent}",
                "all it takes is {antecedent} for {consequent}"
            ],
            "biconditional_hint": [
                "{antecedent} exactly when {consequent}",
                "{antecedent} if and only if {consequent}",
                "{antecedent} just in case {consequent}",
                "{antecedent} precisely when {consequent}",
                "{antecedent} iff {consequent}",
                "{antecedent} ⟺ {consequent}",
                "{antecedent} is equivalent to {consequent}",
                "{antecedent} means the same as {consequent}"
            ],
            "probabilistic": [
                "if {antecedent}, then probably {consequent}",
                "if {antecedent}, then likely {consequent}",
                "{antecedent} suggests {consequent}",
                "{antecedent} indicates {consequent}",
                "given {antecedent}, {consequent} is likely",
                "{antecedent} makes {consequent} probable",
                "chances are if {antecedent}, then {consequent}",
                "{antecedent} tends to lead to {consequent}"
            ],
            "colloquial": [
                "{antecedent} means {consequent}",
                "you get {consequent} from {antecedent}",
                "{antecedent} gives you {consequent}",
                "with {antecedent} comes {consequent}",
                "{antecedent} equals {consequent}",
                "where there's {antecedent}, there's {consequent}",
                "{antecedent} goes hand in hand with {consequent}"
            ],
            "logical": [
                "{antecedent} → {consequent}",
                "{antecedent} ⊃ {consequent}",
                "({antecedent}) IMPLIES ({consequent})",
                "from {antecedent} follows {consequent}",
                "{antecedent} logically implies {consequent}",
                "the truth of {antecedent} guarantees {consequent}"
            ],
            "conditional_precedent": [
                "only after {antecedent} can {consequent}",
                "{consequent} but only if {antecedent}",
                "first {antecedent}, then {consequent}",
                "{antecedent} must precede {consequent}",
                "{consequent} requires {antecedent} first",
                "not until {antecedent} will {consequent}"
            ],
            "equivalence": [
                "{antecedent} is equivalent to {consequent}",
                "{antecedent} amounts to {consequent}",
                "{antecedent} equals {consequent}",
                "{antecedent} is the same as {consequent}",
                "{antecedent} corresponds to {consequent}",
                "{antecedent} matches {consequent}"
            ]
        }
    
    def _init_connectives(self) -> Dict[str, List[str]]:
        """Initialize comprehensive English logical connectives."""
        return {
            "conclusion": [
                "therefore", "thus", "hence", "consequently",
                "so", "accordingly", "as a result", "it follows that",
                "we can conclude that", "this means that", "ergo",
                "from this we see that", "which shows that", "proving that",
                "demonstrating that", "establishing that", "confirming that"
            ],
            "premise": [
                "since", "because", "as", "given that",
                "considering that", "in light of", "due to",
                "on account of", "for", "seeing that",
                "in view of", "owing to", "by virtue of",
                "on the grounds that", "for the reason that"
            ],
            "assumption": [
                "suppose", "assume", "let's say", "imagine",
                "consider", "posit", "grant that", "presuming",
                "hypothetically", "for the sake of argument",
                "let us suppose", "taking it that", "if we assume"
            ],
            "contrast": [
                "but", "however", "yet", "nevertheless",
                "nonetheless", "still", "although", "though",
                "despite", "in spite of", "even so", "be that as it may",
                "on the contrary", "conversely", "on the other hand"
            ],
            "addition": [
                "and", "also", "moreover", "furthermore",
                "additionally", "besides", "plus", "as well as",
                "in addition", "what's more", "not to mention",
                "coupled with", "together with", "along with"
            ],
            "emphasis": [
                "indeed", "in fact", "actually", "certainly",
                "surely", "clearly", "obviously", "evidently",
                "undoubtedly", "without doubt", "unquestionably",
                "indisputably", "undeniably", "manifestly"
            ],
            "example": [
                "for instance", "for example", "e.g.", "such as",
                "like", "namely", "specifically", "in particular",
                "to illustrate", "case in point", "as in",
                "exemplified by", "as shown by", "as demonstrated by"
            ],
            "sequence": [
                "first", "second", "third", "next", "then",
                "subsequently", "afterwards", "finally", "lastly",
                "to begin with", "following that", "in turn",
                "to conclude", "in the end", "ultimately"
            ]
        }
    
    def get_complexity_appropriate_style(self, variation_type: VariationType, 
                                       complexity: ComplexityLevel) -> str:
        """Get appropriate style for given complexity level."""
        if variation_type == VariationType.NEGATION:
            styles = self.negation_by_complexity.get(complexity, ["simple"])
        elif variation_type == VariationType.CONDITIONAL:
            # Default complexity mapping for conditionals
            complexity_map = {
                ComplexityLevel.BASIC: ["standard", "temporal"],
                ComplexityLevel.INTERMEDIATE: ["standard", "causal", "hypothetical"],
                ComplexityLevel.ADVANCED: ["necessity", "sufficiency", "probabilistic"],
                ComplexityLevel.EXPERT: ["biconditional_hint", "logical", "equivalence"]
            }
            styles = complexity_map.get(complexity, ["standard"])
        else:
            # For other types, return None to use default selection
            return None
        
        return random.choice(styles)
    
    def get_domain_appropriate_style(self, variation_type: VariationType,
                                   domain: str) -> str:
        """Get appropriate style for given domain."""
        if variation_type == VariationType.CONDITIONAL:
            styles = self.conditional_by_domain.get(domain, ["standard"])
            return random.choice(styles)
        
        # Domain mappings for other variation types
        if domain == "scientific":
            domain_map = {
                VariationType.NEGATION: ["formal", "semantic"],
                VariationType.CONJUNCTION: ["formal", "logical"],
                VariationType.DISJUNCTION: ["formal", "logical"]
            }
        elif domain == "legal":
            domain_map = {
                VariationType.NEGATION: ["formal", "emphatic"],
                VariationType.CONJUNCTION: ["formal", "sequential"],
                VariationType.DISJUNCTION: ["formal", "exhaustive"]
            }
        elif domain == "everyday":
            domain_map = {
                VariationType.NEGATION: ["simple", "colloquial"],
                VariationType.CONJUNCTION: ["simple", "sequential"],
                VariationType.DISJUNCTION: ["inclusive", "alternative"]
            }
        else:
            return None
        
        styles = domain_map.get(variation_type, [None])
        return random.choice(styles) if styles[0] else None


class EnhancedEnglishTemplates(LanguageTemplates):
    """Enhanced English templates with all inference rules."""
    
    def __init__(self, language_pattern: EnhancedEnglishPattern):
        super().__init__(language_pattern)
    
    def _init_templates(self) -> Dict[str, Dict[str, List[EnhancedTemplate]]]:
        """Initialize templates for all inference rules."""
        templates = {}
        
        # Basic rules
        templates["Modus Ponens"] = {
            "valid": self._create_modus_ponens_valid(),
            "invalid": []  # Will be handled by mappings
        }
        
        templates["Modus Tollens"] = {
            "valid": self._create_modus_tollens_valid(),
            "invalid": []
        }
        
        templates["Disjunctive Syllogism"] = {
            "valid": self._create_disjunctive_syllogism_valid(),
            "invalid": []
        }
        
        templates["Conjunction Introduction"] = {
            "valid": self._create_conjunction_introduction_valid(),
            "invalid": []
        }
        
        templates["Conjunction Elimination"] = {
            "valid": self._create_conjunction_elimination_valid(),
            "invalid": []
        }
        
        templates["Disjunction Introduction"] = {
            "valid": self._create_disjunction_introduction_valid(),
            "invalid": []
        }
        
        templates["Disjunction Elimination"] = {
            "valid": self._create_disjunction_elimination_valid(),
            "invalid": []
        }
        
        templates["Hypothetical Syllogism"] = {
            "valid": self._create_hypothetical_syllogism_valid(),
            "invalid": []
        }
        
        templates["Material Conditional Introduction"] = {
            "valid": self._create_material_conditional_introduction_valid(),
            "invalid": []
        }
        
        templates["Constructive Dilemma"] = {
            "valid": self._create_constructive_dilemma_valid(),
            "invalid": []
        }
        
        templates["Destructive Dilemma"] = {
            "valid": self._create_destructive_dilemma_valid(),
            "invalid": []
        }
        
        # Invalid forms (fallacies)
        templates["Affirming the Consequent"] = {
            "invalid": self._create_affirming_consequent()
        }
        
        templates["Denying the Antecedent"] = {
            "invalid": self._create_denying_antecedent()
        }
        
        templates["Affirming a Disjunct"] = {
            "invalid": self._create_affirming_disjunct()
        }
        
        templates["False Conjunction"] = {
            "invalid": self._create_false_conjunction()
        }
        
        templates["Composition Fallacy"] = {
            "invalid": self._create_composition_fallacy()
        }
        
        templates["False Dilemma"] = {
            "invalid": self._create_false_dilemma()
        }
        
        templates["Invalid Disjunction Elimination"] = {
            "invalid": self._create_invalid_disjunction_elimination()
        }
        
        templates["Non Sequitur"] = {
            "invalid": self._create_non_sequitur()
        }
        
        return templates
    
    def _create_modus_ponens_valid(self) -> List[EnhancedTemplate]:
        """Create Modus Ponens templates with complexity levels."""
        templates = []
        
        # Basic level
        builder = TemplateBuilder()
        builder.add_static('If ')
        builder.add_variable('p')
        builder.add_static(', then ')
        builder.add_variable('q')
        builder.add_static(', then ')
        builder.add_variable('s')  # Different consequence
        builder.add_static('. Therefore, either ')
        builder.add_variable('r')
        builder.add_static(' or ')
        builder.add_variable('s')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        return templates
    
    def _create_non_sequitur(self) -> List[EnhancedTemplate]:
        """Create Non Sequitur templates."""
        templates = []
        
        # Basic
        builder = TemplateBuilder()
        builder.add_static('If ')
        builder.add_variable('p')
        builder.add_static(', then ')
        builder.add_variable('q')
        builder.add_static('. ')
        builder.add_variable('R')  # Unrelated premise
        builder.add_static('. Therefore, ')
        builder.add_variable('q')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        # Intermediate - more disguised
        builder2 = TemplateBuilder()
        builder2.add_variable('Q')
        builder2.add_static(' ')
        builder2.add_variation('because', [
            'because',
            'since',
            'as'
        ])
        builder2.add_static(' ')
        builder2.add_variable('r')
        builder2.add_static(' is true. ')
        builder2.add_variation('also', [
            'Also',
            'Moreover',
            'Additionally'
        ])
        builder2.add_static(', ')
        builder2.add_variation('conditional', [
            'if {p}, then {q}',
            '{p} implies {q}'
        ])
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        templates.append(builder2.build())
        
        # Advanced - complex non sequitur
        builder3 = TemplateBuilder()
        builder3.add_variable('P')
        builder3.add_static('. ')
        builder3.add_variable('Q')
        builder3.add_static('. ')
        builder3.add_variation('therefore', [
            'Therefore',
            'It follows that',
            'We can conclude that'
        ])
        builder3.add_static(', ')
        builder3.add_variable('r')  # Completely unrelated
        builder3.add_static('.')
        builder3.set_metadata('complexity', ComplexityLevel.ADVANCED)
        templates.append(builder3.build())
        
        return templatesadd_static('. ')
        builder.add_variable('P')
        builder.add_static('. Therefore, ')
        builder.add_variable('q')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        builder.set_metadata('structure', 'premise-first')
        templates.append(builder.build())
        
        # Intermediate level with variations
        builder2 = TemplateBuilder()
        builder2.add_variation('conditional', [
            'If {p}, then {q}',
            '{q} if {p}',
            '{p} implies {q}',
            'Given {p}, {q}'
        ])
        builder2.add_static('. ')
        builder2.add_variable('P')
        builder2.add_static('. ')
        builder2.add_variation('conclusion', [
            'Therefore',
            'Thus',
            'Hence',
            'Consequently',
            'So'
        ])
        builder2.add_static(', ')
        builder2.add_variable('q')
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        templates.append(builder2.build())
        
        # Advanced level - conclusion first
        builder3 = TemplateBuilder()
        builder3.add_variable('Q')
        builder3.add_static(' ')
        builder3.add_variation('reasoning', [
            'because',
            'since',
            'as',
            'given that',
            'due to the fact that'
        ])
        builder3.add_static(' ')
        builder3.add_variable('p')
        builder3.add_static('. ')
        builder3.add_variation('connector', [
            'Also',
            'Moreover',
            'Furthermore',
            'Additionally',
            'Note that'
        ])
        builder3.add_static(', ')
        builder3.add_variation('conditional_advanced', [
            'if {p}, then {q}',
            '{p} guarantees {q}',
            '{p} ensures {q}',
            '{p} leads to {q}',
            '{p} is sufficient for {q}'
        ])
        builder3.add_static('.')
        builder3.set_metadata('complexity', ComplexityLevel.ADVANCED)
        builder3.set_metadata('structure', 'conclusion-first')
        templates.append(builder3.build())
        
        # Expert level - formal logical
        builder4 = TemplateBuilder()
        builder4.add_variation('premise1', [
            'From the conditional proposition that {p} → {q}',
            'Given the implication {p} ⊃ {q}',
            'Taking the material conditional if {p} then {q}'
        ])
        builder4.add_static(', ')
        builder4.add_variation('premise2', [
            'and the fact that {p} is true',
            'together with the truth of {p}',
            'combined with the assertion of {p}'
        ])
        builder4.add_static(', ')
        builder4.add_variation('inference', [
            'we can validly infer',
            'it logically follows',
            'modus ponens yields',
            'we derive by detachment'
        ])
        builder4.add_static(' that ')
        builder4.add_variable('q')
        builder4.add_static('.')
        builder4.set_metadata('complexity', ComplexityLevel.EXPERT)
        builder4.set_metadata('style', 'formal-logical')
        templates.append(builder4.build())
        
        return templates
    
    def _create_modus_tollens_valid(self) -> List[EnhancedTemplate]:
        """Create Modus Tollens templates."""
        templates = []
        
        # Basic
        builder = TemplateBuilder()
        builder.add_static('If ')
        builder.add_variable('p')
        builder.add_static(', then ')
        builder.add_variable('q')
        builder.add_static('. ')
        builder.add_variable('not_Q')
        builder.add_static('. Therefore, ')
        builder.add_variable('not_p')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        # Intermediate with variations
        builder2 = TemplateBuilder()
        builder2.add_variation('conditional', [
            'If {p}, then {q}',
            '{q} is necessary for {p}',
            '{p} requires {q}',
            'Without {q}, no {p}'
        ])
        builder2.add_static('. ')
        builder2.add_variation('negation_style', [
            '{not_Q}',
            'But {not_q}',
            'However, {not_q}',
            'Yet {not_q}'
        ])
        builder2.add_static('. ')
        builder2.add_variation('conclusion', [
            'Therefore',
            'Thus',
            'It follows that',
            'We must conclude that'
        ])
        builder2.add_static(', ')
        builder2.add_variable('not_p')
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        templates.append(builder2.build())
        
        # Advanced - with explicit reasoning
        builder3 = TemplateBuilder()
        builder3.add_variable('not_P')
        builder3.add_static(' ')
        builder3.add_variation('because', [
            'because',
            'since',
            'as',
            'due to the fact that'
        ])
        builder3.add_static(' ')
        builder3.add_variable('not_q')
        builder3.add_static('. ')
        builder3.add_variation('note', [
            'Note that',
            'Remember that',
            'We know that',
            'It\'s established that'
        ])
        builder3.add_static(' ')
        builder3.add_variation('conditional', [
            'if {p}, then {q}',
            '{p} necessitates {q}',
            '{q} is required for {p}',
            'there is no {p} without {q}'
        ])
        builder3.add_static('.')
        builder3.set_metadata('complexity', ComplexityLevel.ADVANCED)
        templates.append(builder3.build())
        
        return templates
    
    def _create_disjunctive_syllogism_valid(self) -> List[EnhancedTemplate]:
        """Create Disjunctive Syllogism templates."""
        templates = []
        
        # Basic
        builder = TemplateBuilder()
        builder.add_static('Either ')
        builder.add_variable('p')
        builder.add_static(' or ')
        builder.add_variable('q')
        builder.add_static('. ')
        builder.add_variable('not_P')
        builder.add_static('. Therefore, ')
        builder.add_variable('q')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        # Intermediate
        builder2 = TemplateBuilder()
        builder2.add_variation('disjunction', [
            'Either {p} or {q}',
            'We have either {p} or {q}',
            'It\'s either {p} or {q}',
            'The options are {p} or {q}'
        ])
        builder2.add_static('. ')
        builder2.add_variation('negation', [
            '{not_P}',
            'But {not_p}',
            'However, {not_p}',
            'We know that {not_p}'
        ])
        builder2.add_static('. ')
        builder2.add_variation('conclusion', [
            'Therefore',
            'So',
            'Thus',
            'It follows that',
            'We can conclude'
        ])
        builder2.add_static(', ')
        builder2.add_variable('q')
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        templates.append(builder2.build())
        
        # Advanced - reasoning style
        builder3 = TemplateBuilder()
        builder3.add_variable('Q')
        builder3.add_static(' must be true ')
        builder3.add_variation('reasoning', [
            'because',
            'since',
            'given that',
            'due to the fact that'
        ])
        builder3.add_static(' ')
        builder3.add_variable('not_p')
        builder3.add_static(', and ')
        builder3.add_variation('disjunction', [
            'either {p} or {q}',
            'we know either {p} or {q}',
            'it\'s established that either {p} or {q}'
        ])
        builder3.add_static('.')
        builder3.set_metadata('complexity', ComplexityLevel.ADVANCED)
        templates.append(builder3.build())
        
        return templates
    
    def _create_conjunction_introduction_valid(self) -> List[EnhancedTemplate]:
        """Create Conjunction Introduction templates."""
        templates = []
        
        # Basic
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variable('Q')
        builder.add_static('. Therefore, ')
        builder.add_variable('p')
        builder.add_static(' and ')
        builder.add_variable('q')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        # Intermediate
        builder2 = TemplateBuilder()
        builder2.add_variation('intro', [
            'We know two things',
            'Two facts are established',
            'We have the following',
            'Consider these facts'
        ])
        builder2.add_static(': ')
        builder2.add_variable('p')
        builder2.add_static(', and ')
        builder2.add_variable('q')
        builder2.add_static('. ')
        builder2.add_variation('conclusion', [
            'From these, we can conclude that',
            'Therefore',
            'It follows that',
            'We can combine these to say'
        ])
        builder2.add_static(' ')
        builder2.add_variation('conjunction', [
            '{p} and {q}',
            'both {p} and {q}',
            '{p} as well as {q}',
            '{p} in conjunction with {q}'
        ])
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        templates.append(builder2.build())
        
        return templates
    
    def _create_conjunction_elimination_valid(self) -> List[EnhancedTemplate]:
        """Create Conjunction Elimination templates."""
        templates = []
        
        # Basic
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static(' and ')
        builder.add_variable('q')
        builder.add_static('. Therefore, ')
        builder.add_variable('p')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        # Intermediate
        builder2 = TemplateBuilder()
        builder2.add_variation('conjunction', [
            '{P} and {q}',
            'Both {p} and {q} are true',
            'We have {p} as well as {q}',
            'It\'s the case that {p} and {q}'
        ])
        builder2.add_static('. ')
        builder2.add_variation('conclusion', [
            'Therefore',
            'From this we can conclude',
            'It follows that',
            'In particular'
        ])
        builder2.add_static(', ')
        builder2.add_variable('p')
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        templates.append(builder2.build())
        
        return templates
    
    def _create_disjunction_introduction_valid(self) -> List[EnhancedTemplate]:
        """Create Disjunction Introduction templates."""
        templates = []
        
        # Basic
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. Therefore, either ')
        builder.add_variable('p')
        builder.add_static(' or ')
        builder.add_variable('q')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        # Intermediate
        builder2 = TemplateBuilder()
        builder2.add_variation('premise', [
            '{P}',
            'Given that {p}',
            'Since {p}',
            'We know that {p}'
        ])
        builder2.add_static('. ')
        builder2.add_variation('conclusion', [
            'Therefore',
            'It follows that',
            'We can conclude that',
            'This means'
        ])
        builder2.add_static(' ')
        builder2.add_variation('disjunction', [
            'either {p} or {q}',
            '{p} or {q}',
            'at least one of {p} or {q}',
            '{p} or possibly {q}'
        ])
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        templates.append(builder2.build())
        
        return templates
    
    def _create_disjunction_elimination_valid(self) -> List[EnhancedTemplate]:
        """Create Disjunction Elimination templates."""
        templates = []
        
        # Basic
        builder = TemplateBuilder()
        builder.add_static('Either ')
        builder.add_variable('p')
        builder.add_static(' or ')
        builder.add_variable('q')
        builder.add_static('. If ')
        builder.add_variable('p')
        builder.add_static(', then ')
        builder.add_variable('r')
        builder.add_static('. If ')
        builder.add_variable('q')
        builder.add_static(', then ')
        builder.add_variable('r')
        builder.add_static('. Therefore, ')
        builder.add_variable('r')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        # Intermediate with variations
        builder2 = TemplateBuilder()
        builder2.add_variation('disjunction', [
            'Either {p} or {q}',
            'We have either {p} or {q}',
            'One of two things: {p} or {q}'
        ])
        builder2.add_static('. ')
        builder2.add_variation('conditional1', [
            'If {p}, then {r}',
            '{p} leads to {r}',
            '{p} implies {r}'
        ])
        builder2.add_static('. ')
        builder2.add_variation('conditional2', [
            'If {q}, then {r}',
            '{q} leads to {r}',
            '{q} implies {r}'
        ])
        builder2.add_static('. ')
        builder2.add_variation('conclusion', [
            'Therefore',
            'Either way',
            'In both cases',
            'No matter which'
        ])
        builder2.add_static(', ')
        builder2.add_variable('r')
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        templates.append(builder2.build())
        
        # Advanced - compact reasoning
        builder3 = TemplateBuilder()
        builder3.add_variable('R')
        builder3.add_static(' ')
        builder3.add_variation('because', [
            'because',
            'since',
            'as'
        ])
        builder3.add_static(' either ')
        builder3.add_variable('p')
        builder3.add_static(' or ')
        builder3.add_variable('q')
        builder3.add_static(', and both ')
        builder3.add_variation('lead', [
            'lead to',
            'imply',
            'result in',
            'guarantee'
        ])
        builder3.add_static(' ')
        builder3.add_variable('r')
        builder3.add_static('.')
        builder3.set_metadata('complexity', ComplexityLevel.ADVANCED)
        templates.append(builder3.build())
        
        return templates
    
    def _create_hypothetical_syllogism_valid(self) -> List[EnhancedTemplate]:
        """Create Hypothetical Syllogism templates."""
        templates = []
        
        # Basic
        builder = TemplateBuilder()
        builder.add_static('If ')
        builder.add_variable('p')
        builder.add_static(', then ')
        builder.add_variable('q')
        builder.add_static('. If ')
        builder.add_variable('q')
        builder.add_static(', then ')
        builder.add_variable('r')
        builder.add_static('. Therefore, if ')
        builder.add_variable('p')
        builder.add_static(', then ')
        builder.add_variable('r')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        # Intermediate
        builder2 = TemplateBuilder()
        builder2.add_variation('conditional1', [
            'If {p}, then {q}',
            '{p} implies {q}',
            '{p} leads to {q}',
            'Given {p}, we get {q}'
        ])
        builder2.add_static('. ')
        builder2.add_variation('conditional2', [
            'If {q}, then {r}',
            '{q} implies {r}',
            '{q} leads to {r}',
            'Given {q}, we get {r}'
        ])
        builder2.add_static('. ')
        builder2.add_variation('conclusion', [
            'Therefore',
            'It follows that',
            'By transitivity',
            'We can conclude that'
        ])
        builder2.add_static(', ')
        builder2.add_variation('result', [
            'if {p}, then {r}',
            '{p} implies {r}',
            '{p} leads to {r}',
            '{p} ultimately gives us {r}'
        ])
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        templates.append(builder2.build())
        
        # Advanced - chain reasoning
        builder3 = TemplateBuilder()
        builder3.add_variation('intro', [
            'Since',
            'Given that',
            'Because'
        ])
        builder3.add_static(' ')
        builder3.add_variable('p')
        builder3.add_static(' ')
        builder3.add_variation('link1', [
            'leads to',
            'implies',
            'results in'
        ])
        builder3.add_static(' ')
        builder3.add_variable('q')
        builder3.add_static(', and ')
        builder3.add_variable('q')
        builder3.add_static(' ')
        builder3.add_variation('link2', [
            'leads to',
            'implies',
            'results in'
        ])
        builder3.add_static(' ')
        builder3.add_variable('r')
        builder3.add_static(', ')
        builder3.add_variation('conclusion', [
            'we can conclude that',
            'it follows that',
            'we know that'
        ])
        builder3.add_static(' ')
        builder3.add_variable('p')
        builder3.add_static(' ')
        builder3.add_variation('final_link', [
            'leads to',
            'implies',
            'ultimately results in'
        ])
        builder3.add_static(' ')
        builder3.add_variable('r')
        builder3.add_static('.')
        builder3.set_metadata('complexity', ComplexityLevel.ADVANCED)
        templates.append(builder3.build())
        
        return templates
    
    def _create_material_conditional_introduction_valid(self) -> List[EnhancedTemplate]:
        """Create Material Conditional Introduction templates."""
        templates = []
        
        # Basic
        builder = TemplateBuilder()
        builder.add_static('Assuming ')
        builder.add_variable('p')
        builder.add_static(', we can derive that ')
        builder.add_variable('q')
        builder.add_static('. Therefore, if ')
        builder.add_variable('p')
        builder.add_static(', then ')
        builder.add_variable('q')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        # Intermediate
        builder2 = TemplateBuilder()
        builder2.add_variation('assumption', [
            'Assuming {p}',
            'Suppose {p}',
            'If we assume {p}',
            'Let\'s say {p}'
        ])
        builder2.add_static(', ')
        builder2.add_variation('derivation', [
            'we can derive that',
            'it follows that',
            'we get',
            'we can show that'
        ])
        builder2.add_static(' ')
        builder2.add_variable('q')
        builder2.add_static('. ')
        builder2.add_variation('conclusion', [
            'Therefore',
            'Hence',
            'This means',
            'We can conclude that'
        ])
        builder2.add_static(', ')
        builder2.add_variation('conditional', [
            'if {p}, then {q}',
            '{p} implies {q}',
            '{p} leads to {q}',
            'given {p}, we have {q}'
        ])
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        templates.append(builder2.build())
        
        return templates
    
    def _create_constructive_dilemma_valid(self) -> List[EnhancedTemplate]:
        """Create Constructive Dilemma templates."""
        templates = []
        
        # Basic
        builder = TemplateBuilder()
        builder.add_static('If ')
        builder.add_variable('p')
        builder.add_static(', then ')
        builder.add_variable('q')
        builder.add_static('. If ')
        builder.add_variable('r')
        builder.add_static(', then ')
        builder.add_variable('s')
        builder.add_static('. Either ')
        builder.add_variable('p')
        builder.add_static(' or ')
        builder.add_variable('r')
        builder.add_static('. Therefore, either ')
        builder.add_variable('q')
        builder.add_static(' or ')
        builder.add_variable('s')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        # Intermediate with variations
        builder2 = TemplateBuilder()
        builder2.add_variation('conditional1', [
            'If {p}, then {q}',
            '{p} implies {q}',
            '{p} leads to {q}'
        ])
        builder2.add_static('. ')
        builder2.add_variation('conditional2', [
            'If {r}, then {s}',
            '{r} implies {s}',
            '{r} leads to {s}'
        ])
        builder2.add_static('. ')
        builder2.add_variation('disjunction', [
            'Either {p} or {r}',
            'We have either {p} or {r}',
            'One of {p} or {r} is true'
        ])
        builder2.add_static('. ')
        builder2.add_variation('conclusion', [
            'Therefore',
            'It follows that',
            'Consequently',
            'We must have'
        ])
        builder2.add_static(', ')
        builder2.add_variation('result', [
            'either {q} or {s}',
            'one of {q} or {s}',
            'at least one of {q} or {s}'
        ])
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        templates.append(builder2.build())
        
        return templates
    
    def _create_destructive_dilemma_valid(self) -> List[EnhancedTemplate]:
        """Create Destructive Dilemma templates."""
        templates = []
        
        # Basic
        builder = TemplateBuilder()
        builder.add_static('If ')
        builder.add_variable('p')
        builder.add_static(', then ')
        builder.add_variable('q')
        builder.add_static('. If ')
        builder.add_variable('r')
        builder.add_static(', then ')
        builder.add_variable('s')
        builder.add_static('. Either ')
        builder.add_variable('not_q')
        builder.add_static(' or ')
        builder.add_variable('not_s')
        builder.add_static('. Therefore, either ')
        builder.add_variable('not_p')
        builder.add_static(' or ')
        builder.add_variable('not_r')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        # Intermediate
        builder2 = TemplateBuilder()
        builder2.add_variation('conditional1', [
            'If {p}, then {q}',
            '{p} implies {q}',
            '{q} follows from {p}'
        ])
        builder2.add_static('. ')
        builder2.add_variation('conditional2', [
            'If {r}, then {s}',
            '{r} implies {s}',
            '{s} follows from {r}'
        ])
        builder2.add_static('. ')
        builder2.add_variation('disjunction', [
            'Either {not_q} or {not_s}',
            'We have either {not_q} or {not_s}',
            'At least one of {not_q} or {not_s}'
        ])
        builder2.add_static('. ')
        builder2.add_variation('conclusion', [
            'Therefore',
            'It follows that',
            'By modus tollens on each case'
        ])
        builder2.add_static(', ')
        builder2.add_variation('result', [
            'either {not_p} or {not_r}',
            'one of {not_p} or {not_r}',
            'at least one of {not_p} or {not_r}'
        ])
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        templates.append(builder2.build())
        
        return templates
    
    # Invalid forms (fallacies)
    
    def _create_affirming_consequent(self) -> List[EnhancedTemplate]:
        """Create Affirming the Consequent templates."""
        templates = []
        
        # Basic
        builder = TemplateBuilder()
        builder.add_static('If ')
        builder.add_variable('p')
        builder.add_static(', then ')
        builder.add_variable('q')
        builder.add_static('. ')
        builder.add_variable('Q')
        builder.add_static('. Therefore, ')
        builder.add_variable('p')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        # Intermediate - disguised
        builder2 = TemplateBuilder()
        builder2.add_variable('P')
        builder2.add_static(' ')
        builder2.add_variation('because', [
            'because',
            'since',
            'as'
        ])
        builder2.add_static(' ')
        builder2.add_variable('q')
        builder2.add_static('. ')
        builder2.add_variation('also', [
            'Also',
            'We know that',
            'It\'s true that'
        ])
        builder2.add_static(', ')
        builder2.add_variation('conditional', [
            'if {p}, then {q}',
            '{p} implies {q}',
            '{p} leads to {q}'
        ])
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        builder2.set_metadata('persuasiveness', 'high')
        templates.append(builder2.build())
        
        return templates
    
    def _create_denying_antecedent(self) -> List[EnhancedTemplate]:
        """Create Denying the Antecedent templates."""
        templates = []
        
        # Basic
        builder = TemplateBuilder()
        builder.add_static('If ')
        builder.add_variable('p')
        builder.add_static(', then ')
        builder.add_variable('q')
        builder.add_static('. ')
        builder.add_variable('not_P')
        builder.add_static('. Therefore, ')
        builder.add_variable('not_q')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        # Intermediate - more natural
        builder2 = TemplateBuilder()
        builder2.add_variable('not_Q')
        builder2.add_static(' ')
        builder2.add_variation('because', [
            'because',
            'since',
            'as'
        ])
        builder2.add_static(' ')
        builder2.add_variable('not_p')
        builder2.add_static('. ')
        builder2.add_variation('note', [
            'We know that',
            'Remember that',
            'It\'s established that'
        ])
        builder2.add_static(' ')
        builder2.add_variation('conditional', [
            'if {p}, then {q}',
            '{p} leads to {q}',
            '{q} follows from {p}'
        ])
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        templates.append(builder2.build())
        
        return templates
    
    def _create_affirming_disjunct(self) -> List[EnhancedTemplate]:
        """Create Affirming a Disjunct templates."""
        templates = []
        
        # Basic
        builder = TemplateBuilder()
        builder.add_static('Either ')
        builder.add_variable('p')
        builder.add_static(' or ')
        builder.add_variable('q')
        builder.add_static('. ')
        builder.add_variable('P')
        builder.add_static('. Therefore, ')
        builder.add_variable('not_q')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        # Intermediate - disguised exclusive
        builder2 = TemplateBuilder()
        builder2.add_variable('not_Q')
        builder2.add_static(' ')
        builder2.add_variation('because', [
            'because',
            'since'
        ])
        builder2.add_static(' ')
        builder2.add_variable('p')
        builder2.add_static(' is true. ')
        builder2.add_variation('known', [
            'It\'s known that',
            'We established that',
            'We have'
        ])
        builder2.add_static(' either ')
        builder2.add_variable('p')
        builder2.add_static(' or ')
        builder2.add_variable('q')
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        templates.append(builder2.build())
        
        return templates
    
    def _create_false_conjunction(self) -> List[EnhancedTemplate]:
        """Create False Conjunction templates."""
        templates = []
        
        # Basic
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variable('Q')
        builder.add_static('. Therefore, ')
        builder.add_variable('p')
        builder.add_static(' and ')
        builder.add_variable('r')  # Note: using unrelated variable
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        # Intermediate
        builder2 = TemplateBuilder()
        builder2.add_static('From the facts that ')
        builder2.add_variable('p')
        builder2.add_static(' and ')
        builder2.add_variable('q')
        builder2.add_static(', ')
        builder2.add_variation('conclusion', [
            'we can conclude that',
            'it follows that',
            'we know that'
        ])
        builder2.add_static(' ')
        builder2.add_variable('p')
        builder2.add_static(' and ')
        builder2.add_variable('r')  # Unrelated
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        templates.append(builder2.build())
        
        return templates
    
    def _create_composition_fallacy(self) -> List[EnhancedTemplate]:
        """Create Composition Fallacy templates."""
        templates = []
        
        # Basic
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variable('Q')
        builder.add_static('. Therefore, ')
        builder.add_variable('p')
        builder.add_static(' and ')
        builder.add_variable('q')
        builder.add_static(' and ')
        builder.add_variable('r')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        return templates
    
    def _create_false_dilemma(self) -> List[EnhancedTemplate]:
        """Create False Dilemma templates."""
        templates = []
        
        # Basic
        builder = TemplateBuilder()
        builder.add_static('Either ')
        builder.add_variable('p')
        builder.add_static(' or ')
        builder.add_variable('q')
        builder.add_static('. Therefore, not both ')
        builder.add_variable('p')
        builder.add_static(' and ')
        builder.add_variable('q')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        # Intermediate
        builder2 = TemplateBuilder()
        builder2.add_variation('since', [
            'Since',
            'Given that',
            'Because'
        ])
        builder2.add_static(' either ')
        builder2.add_variable('p')
        builder2.add_static(' or ')
        builder2.add_variable('q')
        builder2.add_static(', ')
        builder2.add_variation('conclusion', [
            'we can conclude that',
            'it follows that',
            'we know that'
        ])
        builder2.add_static(' ')
        builder2.add_variable('p')
        builder2.add_static(' and ')
        builder2.add_variable('q')
        builder2.add_static(' cannot both be true.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        templates.append(builder2.build())
        
        return templates
    
    def _create_invalid_disjunction_elimination(self) -> List[EnhancedTemplate]:
        """Create Invalid Disjunction Elimination templates."""
        templates = []
        
        # Basic
        builder = TemplateBuilder()
        builder.add_static('Either ')
        builder.add_variable('p')
        builder.add_static(' or ')
        builder.add_variable('q')
        builder.add_static('. If ')
        builder.add_variable('p')
        builder.add_static(', then ')
        builder.add_variable('r')
        builder.add_static('. If ')
        builder.add_variable('q')
        builder.