"""
languages/french.py

French language implementation for the argument generator.
Includes all variation types and complexity levels.
"""

from typing import Dict, List, Tuple, Optional, Set, Any
import re
from language_base import (
    LanguageSpecificPattern, LanguageTemplates, 
    LanguageGrammar, LanguageStyleGuide, LanguageAdapter
)
from linguistic_patterns import ComplexityLevel, VariationType
from template_system import TemplateBuilder, EnhancedTemplate


class FrenchPattern(LanguageSpecificPattern):
    """French-specific linguistic patterns."""
    
    def __init__(self):
        super().__init__("fr")
    
    def _init_negation_patterns(self) -> Dict[str, List[str]]:
        """Initialize French negation patterns."""
        return {
            "simple": [
                "il n'est pas vrai que {sentence}",
                "{sentence} n'est pas le cas",
                "ce n'est pas que {sentence}",
                "{sentence} est faux",
                "{sentence} n'est pas vrai"
            ],
            "formal": [
                "il est faux que {sentence}",
                "il n'est pas exact que {sentence}",
                "la proposition selon laquelle {sentence} est fausse",
                "il est incorrect d'affirmer que {sentence}",
                "l'affirmation que {sentence} est erronée"
            ],
            "emphatic": [
                "{sentence} est absolument faux",
                "{sentence} n'est certainement pas le cas",
                "{sentence} est catégoriquement faux",
                "{sentence} est indubitablement faux",
                "il n'y a aucune façon que {sentence}",
                "en aucun cas {sentence}"
            ],
            "double": [
                "il n'est pas faux que {sentence}",
                "ce n'est pas incorrect que {sentence}",
                "on ne peut nier que {sentence}",
                "il n'est pas inexact que {sentence}"
            ],
            "colloquial": [
                "{sentence} c'est pas vrai",
                "pas du tout {sentence}",
                "jamais de la vie {sentence}",
                "{sentence} c'est faux",
                "oublie que {sentence}"
            ],
            "semantic": [
                "le contraire de {sentence} est vrai",
                "{sentence} ne s'applique pas",
                "la négation de {sentence} est vraie",
                "il y a absence de {sentence}",
                "{sentence} ne se réalise pas"
            ],
            "literary": [
                "point n'est vrai que {sentence}",
                "nullement {sentence}",
                "aucunement {sentence}",
                "nenni, {sentence}",
                "que nenni pour {sentence}"
            ],
            "philosophical": [
                "la valeur de vérité de {sentence} est fausse",
                "{sentence} manque de vérité",
                "la proposition {sentence} ne correspond pas à la réalité",
                "{sentence} est dénué de vérité",
                "il n'existe aucun état de fait où {sentence}"
            ]
        }
    
    def _init_conjunction_patterns(self) -> Dict[str, List[str]]:
        """Initialize French conjunction patterns."""
        return {
            "simple": [
                "{p} et {q}",
                "{p}, et {q}",
                "{p} ainsi que {q}",
                "{p} avec {q}",
                "à la fois {p} et {q}"
            ],
            "sequential": [
                "{p}, et aussi {q}",
                "{p}, de plus {q}",
                "{p}, en outre {q}",
                "{p}, également {q}",
                "{p}, qui plus est {q}"
            ],
            "emphatic": [
                "non seulement {p} mais aussi {q}",
                "tant {p} que {q}",
                "{p} et, de manière égale, {q}",
                "{p} conjointement avec {q}",
                "{p} de concert avec {q}"
            ],
            "formal": [
                "{p} en conjonction avec {q}",
                "{p} conjointement à {q}",
                "la conjonction de {p} et {q}",
                "{p} et simultanément {q}",
                "{p} de façon concomitante avec {q}"
            ],
            "causal": [
                "{p}, et par conséquent {q}",
                "{p}, et en conséquence {q}",
                "{p}, ce qui entraîne {q}",
                "{p}, d'où {q}",
                "{p}, par suite {q}"
            ],
            "temporal": [
                "{p}, puis {q}",
                "{p}, ensuite {q}",
                "{p}, et par la suite {q}",
                "{p}, après quoi {q}",
                "d'abord {p}, puis {q}"
            ],
            "additive": [
                "non seulement {p} mais encore {q}",
                "{p}, et qui plus est, {q}",
                "{p}, et de surcroît {q}",
                "{p}, et par-dessus le marché {q}",
                "{p}, sans compter {q}"
            ],
            "logical": [
                "{p} ∧ {q}",
                "({p}) ET ({q})",
                "{p} & {q}",
                "la conjonction logique de {p} et {q}",
                "{p} ET {q} sont tous deux vrais"
            ]
        }
    
    def _init_disjunction_patterns(self) -> Dict[str, List[str]]:
        """Initialize French disjunction patterns."""
        return {
            "inclusive": [
                "{p} ou {q}",
                "{p}, ou {q}",
                "soit {p} soit {q} ou les deux",
                "{p} et/ou {q}",
                "{p} ou bien {q}"
            ],
            "exclusive": [
                "soit {p} soit {q} mais pas les deux",
                "exactement un parmi {p} ou {q}",
                "{p} ou {q}, mais pas les deux",
                "ou {p} ou {q} (exclusif)",
                "l'un ou l'autre: {p} ou {q}"
            ],
            "alternative": [
                "{p}, alternativement {q}",
                "{p}, ou sinon {q}",
                "{p}, à défaut {q}",
                "{p}, ou au contraire {q}",
                "{p}, sinon {q}"
            ],
            "formal": [
                "{p} ou bien {q}",
                "la disjonction de {p} et {q}",
                "{p} vel {q}",
                "au moins un parmi {p} ou {q}",
                "soit {p} soit éventuellement {q}"
            ],
            "conditional": [
                "{p}, à moins que {q}",
                "{p} sauf si {q}",
                "{p} si ce n'est {q}",
                "{p} hormis si {q}",
                "{p} excepté si {q}"
            ],
            "preferential": [
                "{p}, ou à défaut, {q}",
                "préférablement {p}, sinon {q}",
                "{p} si possible, sinon {q}",
                "idéalement {p}, mais {q} fera l'affaire",
                "premier choix {p}, second choix {q}"
            ],
            "exhaustive": [
                "c'est soit {p} soit {q}",
                "il y a deux options: {p} ou {q}",
                "les options sont {p} ou {q}",
                "nous avons {p} ou nous avons {q}",
                "le choix est entre {p} et {q}"
            ],
            "logical": [
                "{p} ∨ {q}",
                "({p}) OU ({q})",
                "{p} | {q}",
                "la disjonction logique de {p} et {q}",
                "{p} OU {q} est vrai"
            ]
        }
    
    def _init_conditional_patterns(self) -> Dict[str, List[str]]:
        """Initialize French conditional patterns."""
        return {
            "standard": [
                "si {antecedent}, alors {consequent}",
                "si {antecedent} alors {consequent}",
                "{consequent} si {antecedent}",
                "étant donné {antecedent}, {consequent}",
                "quand {antecedent}, {consequent}"
            ],
            "temporal": [
                "quand {antecedent}, alors {consequent}",
                "lorsque {antecedent}, {consequent}",
                "une fois que {antecedent}, {consequent}",
                "dès que {antecedent}, {consequent}",
                "après que {antecedent}, {consequent}"
            ],
            "causal": [
                "parce que {antecedent}, {consequent}",
                "{antecedent} cause {consequent}",
                "{antecedent} entraîne {consequent}",
                "{antecedent} produit {consequent}",
                "{antecedent} provoque {consequent}"
            ],
            "hypothetical": [
                "en supposant que {antecedent}, {consequent}",
                "en admettant que {antecedent}, {consequent}",
                "pourvu que {antecedent}, {consequent}",
                "à condition que {antecedent}, {consequent}",
                "dans l'hypothèse où {antecedent}, {consequent}"
            ],
            "necessity": [
                "{consequent} est nécessaire pour {antecedent}",
                "{antecedent} requiert {consequent}",
                "sans {consequent}, pas de {antecedent}",
                "{antecedent} seulement si {consequent}",
                "pour {antecedent}, il faut {consequent}"
            ],
            "sufficiency": [
                "{antecedent} est suffisant pour {consequent}",
                "{antecedent} garantit {consequent}",
                "{antecedent} assure {consequent}",
                "{antecedent} implique {consequent}",
                "{antecedent} entraîne {consequent}"
            ],
            "biconditional_hint": [
                "{antecedent} exactement quand {consequent}",
                "{antecedent} si et seulement si {consequent}",
                "{antecedent} équivaut à {consequent}",
                "{antecedent} précisément quand {consequent}",
                "{antecedent} ssi {consequent}"
            ],
            "probabilistic": [
                "si {antecedent}, alors probablement {consequent}",
                "si {antecedent}, alors vraisemblablement {consequent}",
                "{antecedent} suggère {consequent}",
                "{antecedent} indique {consequent}",
                "étant donné {antecedent}, {consequent} est probable"
            ],
            "colloquial": [
                "{antecedent} veut dire {consequent}",
                "de {antecedent} vient {consequent}",
                "{antecedent} donne {consequent}",
                "avec {antecedent} vient {consequent}",
                "qui dit {antecedent} dit {consequent}"
            ],
            "subjunctive": [
                "si {antecedent} était vrai, {consequent} serait vrai",
                "pour peu que {antecedent}, {consequent}",
                "à supposer que {antecedent}, {consequent}",
                "en cas où {antecedent}, {consequent}",
                "si jamais {antecedent}, {consequent}"
            ]
        }
    
    def _init_connectives(self) -> Dict[str, List[str]]:
        """Initialize French logical connectives."""
        return {
            "conclusion": [
                "donc", "ainsi", "alors", "par conséquent",
                "en conséquence", "d'où", "il s'ensuit que",
                "on peut conclure que", "cela signifie que", "ergo",
                "de cela nous voyons que", "ce qui démontre que"
            ],
            "premise": [
                "puisque", "parce que", "comme", "étant donné que",
                "considérant que", "vu que", "du fait que",
                "en raison de", "car", "attendu que"
            ],
            "assumption": [
                "supposons", "admettons", "disons que", "imaginons",
                "considérons", "posons que", "soit", "en supposant",
                "hypothétiquement", "pour les besoins de l'argument"
            ],
            "contrast": [
                "mais", "cependant", "néanmoins", "toutefois",
                "pourtant", "or", "bien que", "malgré",
                "en dépit de", "au contraire", "en revanche"
            ],
            "addition": [
                "et", "aussi", "de plus", "en outre",
                "également", "par ailleurs", "qui plus est",
                "de surcroît", "sans compter", "outre"
            ],
            "emphasis": [
                "en effet", "effectivement", "certainement",
                "assurément", "à coup sûr", "indubitablement",
                "sans aucun doute", "manifestement", "évidemment"
            ]
        }
    
    def format_sentence(self, sentence: str, formatting_type: str) -> str:
        """Apply French-specific formatting."""
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
        """Normalize a French sentence."""
        # Remove trailing punctuation
        sentence = sentence.rstrip('.!?;:,')
        
        # Convert to lowercase
        sentence = sentence.lower()
        
        # Handle French contractions
        sentence = sentence.replace("l'", "le ")
        sentence = sentence.replace("d'", "de ")
        sentence = sentence.replace("qu'", "que ")
        
        # Remove extra whitespace
        sentence = ' '.join(sentence.split())
        
        return sentence
    
    def capitalize_sentence(self, sentence: str) -> str:
        """Capitalize a French sentence properly."""
        if not sentence:
            return sentence
        
        # Handle contractions at start
        if sentence.startswith("l'"):
            return "L'" + sentence[2:]
        elif sentence.startswith("d'"):
            return "D'" + sentence[2:]
        else:
            return sentence[0].upper() + sentence[1:]
    
    def _simple_negate(self, sentence: str) -> str:
        """Apply simple negation to a French sentence."""
        # French negation typically uses ne...pas
        if " est " in sentence:
            return sentence.replace(" est ", " n'est pas ", 1)
        elif " sont " in sentence:
            return sentence.replace(" sont ", " ne sont pas ", 1)
        elif " a " in sentence:
            return sentence.replace(" a ", " n'a pas ", 1)
        elif " ont " in sentence:
            return sentence.replace(" ont ", " n'ont pas ", 1)
        else:
            return f"il n'est pas vrai que {sentence}"
    
    def _make_question(self, sentence: str) -> str:
        """Convert a statement to a question in French."""
        # Simple inversion or est-ce que
        if sentence.startswith(("il ", "elle ", "on ")):
            parts = sentence.split(" ", 1)
            if len(parts) > 1:
                return f"{parts[1]}-{parts[0]}?"
        
        return f"est-ce que {sentence}?"
    
    def _emphasize(self, sentence: str) -> str:
        """Add emphasis to a French sentence."""
        emphatics = ["certainement", "assurément", "indubitablement"]
        import random
        return f"{random.choice(emphatics)} {sentence}"


class FrenchTemplates(LanguageTemplates):
    """French-specific argument templates."""
    
    def __init__(self, language_pattern: FrenchPattern):
        super().__init__(language_pattern)
    
    def _init_templates(self) -> Dict[str, Dict[str, List[EnhancedTemplate]]]:
        """Initialize French templates - all 11 logical rules."""
        templates = {}
        
        # Basic Inference Rules
        templates["Modus Ponens"] = {
            "valid": self._create_modus_ponens_valid(),
            "invalid": self._create_modus_ponens_invalid()
        }
        
        templates["Modus Tollens"] = {
            "valid": self._create_modus_tollens_valid(),
            "invalid": self._create_modus_tollens_invalid()
        }
        
        templates["Disjunctive Syllogism"] = {
            "valid": self._create_disjunctive_syllogism_valid(),
            "invalid": self._create_disjunctive_syllogism_invalid()
        }
        
        # Conjunction Rules
        templates["Conjunction Introduction"] = {
            "valid": self._create_conjunction_introduction_valid(),
            "invalid": self._create_conjunction_introduction_invalid()
        }
        
        templates["Conjunction Elimination"] = {
            "valid": self._create_conjunction_elimination_valid(),
            "invalid": self._create_conjunction_elimination_invalid()
        }
        
        # Disjunction Rules
        templates["Disjunction Introduction"] = {
            "valid": self._create_disjunction_introduction_valid(),
            "invalid": self._create_invalid_conjunction_introduction()
        }
        
        templates["Disjunction Elimination"] = {
            "valid": self._create_disjunction_elimination_valid(),
            "invalid": self._create_disjunction_elimination_invalid()
        }
        
        # Complex Rules
        templates["Hypothetical Syllogism"] = {
            "valid": self._create_hypothetical_syllogism_valid(),
            "invalid": self._create_hypothetical_syllogism_invalid()
        }
        
        templates["Material Conditional Introduction"] = {
            "valid": self._create_material_conditional_introduction_valid(),
            "invalid": self._create_material_conditional_introduction_invalid()
        }
        
        templates["Constructive Dilemma"] = {
            "valid": self._create_constructive_dilemma_valid(),
            "invalid": self._create_constructive_dilemma_invalid()
        }
        
        templates["Destructive Dilemma"] = {
            "valid": self._create_destructive_dilemma_valid(),
            "invalid": self._create_destructive_dilemma_invalid()
        }
        
        # Invalid forms (fallacies)
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
        
        templates["False Dilemma"] = {
            "invalid": self._create_constructive_dilemma_invalid()
        }
        
        templates["Invalid Disjunction Elimination"] = {
            "invalid": self._create_disjunction_elimination_invalid()
        }
        
        templates["Non Sequitur"] = {
            "invalid": self._create_hypothetical_syllogism_invalid() + self._create_material_conditional_introduction_invalid() + self._create_destructive_dilemma_invalid()
        }
        
        return templates
    
    def _create_modus_ponens_valid(self) -> List[EnhancedTemplate]:
        """Create valid Modus Ponens templates in French."""
        templates = []
        
        # Basic Modus Ponens: Si p, alors q. p. Donc q.
        builder = TemplateBuilder()
        builder.add_variation('conditional', [
            'Si {p}, alors {q}',
            '{Q} si {p}',
            '{P} implique {q}',
            '{P} entraîne {q}'
        ])
        builder.add_static('. ')
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Donc',
            'Ainsi',
            'Par conséquent',
            'En conséquence'
        ])
        builder.add_static(', ')
        builder.add_variable('q')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        return templates
    
    def _create_modus_tollens_valid(self) -> List[EnhancedTemplate]:
        """Create valid Modus Tollens templates in French."""
        templates = []
        
        # Basic Modus Tollens: Si p, alors q. Non q. Donc non p.
        builder = TemplateBuilder()
        builder.add_variation('conditional', [
            'Si {p}, alors {q}',
            '{Q} si {p}',
            '{P} implique {q}'
        ])
        builder.add_static('. ')
        builder.add_variable('not_Q')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Donc',
            'Ainsi',
            'Par conséquent'
        ])
        builder.add_static(', ')
        builder.add_variable('not_p')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        return templates
    
    def _create_disjunctive_syllogism_valid(self) -> List[EnhancedTemplate]:
        """Create valid Disjunctive Syllogism templates in French."""
        templates = []
        
        # Basic: p ou q. Non p. Donc q.
        builder = TemplateBuilder()
        builder.add_variation('disjunction', [
            '{P} ou {q}',
            'Soit {p} soit {q}',
            '{P} ou bien {q}'
        ])
        builder.add_static('. ')
        builder.add_variable('not_P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Donc',
            'Ainsi',
            'Par conséquent'
        ])
        builder.add_static(', ')
        builder.add_variable('q')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        return templates
    
    def _create_hypothetical_syllogism_valid(self) -> List[EnhancedTemplate]:
        """Create valid Hypothetical Syllogism templates in French."""
        templates = []
        
        # Basic: Si p, alors q. Si q, alors r. Donc, si p, alors r.
        builder = TemplateBuilder()
        builder.add_variation('conditional1', [
            'Si {p}, alors {q}',
            '{P} implique {q}'
        ])
        builder.add_static('. ')
        builder.add_variation('conditional2', [
            'Si {q}, alors {r}',
            '{Q} implique {r}'
        ])
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Donc',
            'Ainsi',
            'Par conséquent'
        ])
        builder.add_static(', ')
        builder.add_variation('conditional3', [
            'si {p}, alors {r}',
            '{p} implique {r}'
        ])
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        return templates
    
    def _create_modus_ponens_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Modus Ponens templates (Affirming the Consequent) in French."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('conditional', [
            'Si {p}, alors {q}',
            '{p} implique {q}',
            '{p} entraîne {q}'
        ])
        builder.add_static('. ')
        builder.add_variable('Q')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Donc',
            'Ainsi',
            'Par conséquent'
        ])
        builder.add_static(', ')
        builder.add_variable('p')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_modus_tollens_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Modus Tollens templates (Denying the Antecedent) in French."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('conditional', [
            'Si {p}, alors {q}',
            '{p} implique {q}',
            '{p} entraîne {q}'
        ])
        builder.add_static('. ')
        builder.add_variable('not_P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Donc',
            'Ainsi',
            'Par conséquent'
        ])
        builder.add_static(', ')
        builder.add_variable('not_q')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_disjunctive_syllogism_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Disjunctive Syllogism templates (Affirming a Disjunct) in French."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('disjunction', [
            '{p} ou {q}',
            'Soit {p} soit {q}',
            '{p} ou bien {q}'
        ])
        builder.add_static('. ')
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Donc',
            'Ainsi',
            'Par conséquent'
        ])
        builder.add_static(', ')
        builder.add_variable('not_q')
        builder.add_static(' n\'est pas le cas.')
        
        templates.append(builder.build())
        return templates
    
    def _create_conjunction_introduction_valid(self) -> List[EnhancedTemplate]:
        """Create valid Conjunction Introduction templates in French."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variable('Q')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Donc',
            'Ainsi',
            'Par conséquent'
        ])
        builder.add_static(', ')
        builder.add_variation('conjunction', [
            '{p} et {q}',
            'à la fois {p} et {q}',
            '{p} ainsi que {q}'
        ])
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_conjunction_introduction_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Conjunction Introduction templates (False Conjunction) in French."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Donc',
            'Ainsi',
            'Par conséquent'
        ])
        builder.add_static(', ')
        builder.add_variation('conjunction', [
            '{p} et {q}',
            'à la fois {p} et {q}'
        ])
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_conjunction_elimination_valid(self) -> List[EnhancedTemplate]:
        """Create valid Conjunction Elimination templates in French."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('conjunction', [
            '{p} et {q}',
            'à la fois {p} et {q}',
            '{p} ainsi que {q}'
        ])
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Donc',
            'Ainsi',
            'Par conséquent'
        ])
        builder.add_static(', ')
        builder.add_variable('p')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_conjunction_elimination_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Conjunction Elimination templates (Composition Fallacy) in French."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static(' a la propriété {q}. ')
        builder.add_variation('conclusion', [
            'Donc',
            'Ainsi',
            'Par conséquent'
        ])
        builder.add_static(', l\'ensemble de ')
        builder.add_variable('p')
        builder.add_static(' a la propriété ')
        builder.add_variable('q')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_disjunction_introduction_valid(self) -> List[EnhancedTemplate]:
        """Create valid Disjunction Introduction templates in French."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Donc',
            'Ainsi',
            'Par conséquent'
        ])
        builder.add_static(', ')
        builder.add_variation('disjunction', [
            '{p} ou {q}',
            'soit {p} soit {q}',
            '{p} ou bien {q}'
        ])
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_invalid_conjunction_introduction(self) -> List[EnhancedTemplate]:
        """Create Invalid Conjunction Introduction templates (A / Therefore, A and B) in French."""
        templates = []
        
        # Basic invalid conjunction introduction
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Donc',
            'Ainsi',
            'Par conséquent',
            'Alors'
        ])
        builder.add_static(', ')
        builder.add_variation('conjunction', [
            '{p} et {q}',
            'à la fois {p} et {q}',
            '{p} ainsi que {q}'
        ])
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        # Intermediate version with more sophisticated language
        builder2 = TemplateBuilder()
        builder2.add_variable('P')
        builder2.add_static('. ')
        builder2.add_variation('conclusion', [
            'Il s\'ensuit que',
            'Nous pouvons conclure que',
            'Cela signifie que'
        ])
        builder2.add_static(' ')
        builder2.add_variation('conjunction', [
            'non seulement {p} mais aussi {q}',
            '{p} et en plus {q}',
            '{p} avec {q}'
        ])
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        templates.append(builder2.build())
        
        return templates
    
    def _create_disjunction_elimination_valid(self) -> List[EnhancedTemplate]:
        """Create valid Disjunction Elimination templates in French."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('disjunction', [
            '{p} ou {q}',
            'soit {p} soit {q}',
            '{p} ou bien {q}'
        ])
        builder.add_static('. Si ')
        builder.add_variable('p')
        builder.add_static(', alors ')
        builder.add_variable('r')
        builder.add_static('. Si ')
        builder.add_variable('q')
        builder.add_static(', alors ')
        builder.add_variable('r')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Donc',
            'Ainsi',
            'Par conséquent'
        ])
        builder.add_static(', ')
        builder.add_variable('r')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_disjunction_elimination_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Disjunction Elimination templates in French."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('disjunction', [
            '{p} ou {q}',
            'soit {p} soit {q}'
        ])
        builder.add_static('. ')
        builder.add_variable('P')
        builder.add_static(' implique ')
        builder.add_variable('r')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Donc',
            'Ainsi'
        ])
        builder.add_static(', ')
        builder.add_variable('r')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_hypothetical_syllogism_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Hypothetical Syllogism templates (Non Sequitur) in French."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Donc',
            'Ainsi',
            'Par conséquent'
        ])
        builder.add_static(', ')
        builder.add_variable('q')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_material_conditional_introduction_valid(self) -> List[EnhancedTemplate]:
        """Create valid Material Conditional Introduction templates in French."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static(' implique ')
        builder.add_variable('q')
        builder.add_static('. ')
        builder.add_variable('Q')
        builder.add_static(' implique ')
        builder.add_variable('r')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Donc',
            'Ainsi',
            'Par conséquent'
        ])
        builder.add_static(', si ')
        builder.add_variable('p')
        builder.add_static(', alors ')
        builder.add_variable('r')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_material_conditional_introduction_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Material Conditional Introduction templates (Non Sequitur) in French."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Donc',
            'Ainsi'
        ])
        builder.add_static(', ')
        builder.add_variable('q')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_constructive_dilemma_valid(self) -> List[EnhancedTemplate]:
        """Create valid Constructive Dilemma templates in French."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variable('p')
        builder.add_static(' implique ')
        builder.add_variable('q')
        builder.add_static('. ')
        builder.add_variable('r')
        builder.add_static(' implique ')
        builder.add_variable('s')
        builder.add_static('. ')
        builder.add_variation('disjunction', [
            'soit {p} soit {r}',
            '{p} ou {r}',
            '{p} ou bien {r}'
        ])
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Donc',
            'Ainsi',
            'Par conséquent'
        ])
        builder.add_static(', ')
        builder.add_variation('result_disjunction', [
            'soit {q} soit {s}',
            '{q} ou {s}',
            '{q} ou bien {s}'
        ])
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_constructive_dilemma_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Constructive Dilemma templates (False Dilemma) in French."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Donc',
            'Ainsi'
        ])
        builder.add_static(', soit ')
        builder.add_variable('p')
        builder.add_static(' soit ')
        builder.add_variable('q')
        builder.add_static(' (il n\'y a pas d\'autres options).')
        
        templates.append(builder.build())
        return templates
    
    def _create_destructive_dilemma_valid(self) -> List[EnhancedTemplate]:
        """Create valid Destructive Dilemma templates in French."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_static('Si ')
        builder.add_variable('p')
        builder.add_static(', alors ')
        builder.add_variable('q')
        builder.add_static('. Si ')
        builder.add_variable('r')
        builder.add_static(', alors ')
        builder.add_variable('s')
        builder.add_static('. ')
        builder.add_variation('negated_disjunction', [
            'Non {q} ou non {s}',
            'soit non {q} soit non {s}',
            '{q} n\'est pas vrai ou {s} n\'est pas vrai'
        ])
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Donc',
            'Ainsi',
            'Par conséquent'
        ])
        builder.add_static(', ')
        builder.add_variation('negated_result', [
            'non {p} ou non {r}',
            'soit non {p} soit non {r}',
            '{p} n\'est pas vrai ou {r} n\'est pas vrai'
        ])
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_destructive_dilemma_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Destructive Dilemma templates (Non Sequitur) in French."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Donc',
            'Ainsi'
        ])
        builder.add_static(', ')
        builder.add_variable('q')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_affirming_consequent(self) -> List[EnhancedTemplate]:
        """Create Affirming the Consequent templates in French."""
        templates = []
        
        # Basic invalid form
        builder = TemplateBuilder()
        builder.add_static('Si ')
        builder.add_variable('p')
        builder.add_static(', alors ')
        builder.add_variable('q')
        builder.add_static('. ')
        builder.add_variable('Q')
        builder.add_static('. Donc, ')
        builder.add_variable('p')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        return templates
    
    def _create_denying_antecedent(self) -> List[EnhancedTemplate]:
        """Create Denying the Antecedent templates in French."""
        templates = []
        
        # Basic invalid form
        builder = TemplateBuilder()
        builder.add_static('Si ')
        builder.add_variable('p')
        builder.add_static(', alors ')
        builder.add_variable('q')
        builder.add_static('. ')
        builder.add_variable('not_P')
        builder.add_static('. Donc, ')
        builder.add_variable('not_q')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
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
        basic_vars = {'p', 'q', 'P', 'Q'}
        
        if rule_name in ["Modus Tollens", "Disjunctive Syllogism"]:
            basic_vars.update({'not_p', 'not_q', 'not_P', 'not_Q'})
        
        if rule_name in ["Disjunction Elimination", "Hypothetical Syllogism", "Material Conditional Introduction"]:
            basic_vars.update({'r', 'R'})
        
        if rule_name in ["Constructive Dilemma", "Destructive Dilemma"]:
            basic_vars.update({'r', 's', 'R', 'S'})
        
        return basic_vars


class FrenchGrammar(LanguageGrammar):
    """French grammar rules."""
    
    def __init__(self):
        super().__init__("fr")
    
    def apply_agreement(self, subject: str, verb: str, 
                       object: Optional[str] = None) -> Tuple[str, str, Optional[str]]:
        """Apply French subject-verb agreement."""
        # Simplified - French has complex agreement rules
        
        # Check plurality
        plural_indicators = ['s', 'x', 'les', 'des', 'plusieurs']
        is_plural = any(subject.endswith(ind) for ind in plural_indicators[:2]) or \
                   any(ind in subject for ind in plural_indicators[2:])
        
        # Adjust verb
        if is_plural:
            verb_mappings = {
                'est': 'sont',
                'a': 'ont',
                'fait': 'font',
                'va': 'vont'
            }
            if verb in verb_mappings:
                verb = verb_mappings[verb]
        
        return subject, verb, object
    
    def apply_article_rules(self, noun: str, definite: bool = False) -> str:
        """Apply French article rules (gender-based)."""
        # Simplified gender detection
        feminine_endings = ['e', 'ion', 'té', 'ée', 'ie', 'ue', 'ance', 'ence']
        is_feminine = any(noun.endswith(end) for end in feminine_endings)
        
        # Check if starts with vowel
        starts_with_vowel = noun[0].lower() in 'aeiouhàâéèêëîïôùû'
        
        if definite:
            if starts_with_vowel:
                article = "l'"
            elif is_feminine:
                article = "la"
            else:
                article = "le"
        else:
            if is_feminine:
                article = "une"
            else:
                article = "un"
        
        return f"{article} {noun}" if not article.endswith("'") else f"{article}{noun}"
    
    def apply_word_order(self, components: Dict[str, str]) -> str:
        """Apply French word order (generally SVO but with variations)."""
        parts = []
        
        # Handle pronoun placement (before verb in French)
        if 'pronoun_object' in components:
            if 'subject' in components:
                parts.append(components['subject'])
            parts.append(components['pronoun_object'])
            if 'verb' in components:
                parts.append(components['verb'])
        else:
            # Standard SVO
            if 'subject' in components:
                parts.append(components['subject'])
            if 'verb' in components:
                parts.append(components['verb'])
            if 'object' in components:
                parts.append(components['object'])
        
        # Add other components
        for key, value in components.items():
            if key not in ['subject', 'verb', 'object', 'pronoun_object']:
                parts.append(value)
        
        return ' '.join(parts)
    
    def pluralize(self, word: str, count: int = 2) -> str:
        """Pluralize a French word."""
        if count == 1:
            return word
        
        # French pluralization rules
        if word.endswith(('s', 'x', 'z')):
            return word  # No change
        elif word.endswith('au'):
            return word + 'x'
        elif word.endswith('eu'):
            return word + 'x'
        elif word.endswith('al'):
            return word[:-2] + 'aux'
        elif word.endswith('ail'):
            return word[:-3] + 'aux'
        else:
            return word + 's'
    
    def apply_case(self, word: str, case: str) -> str:
        """French doesn't have cases, but has pronoun forms."""
        pronoun_cases = {
            'je': {'nominative': 'je', 'accusative': 'me', 'stressed': 'moi'},
            'tu': {'nominative': 'tu', 'accusative': 'te', 'stressed': 'toi'},
            'il': {'nominative': 'il', 'accusative': 'le', 'stressed': 'lui'},
            'elle': {'nominative': 'elle', 'accusative': 'la', 'stressed': 'elle'},
            'nous': {'nominative': 'nous', 'accusative': 'nous', 'stressed': 'nous'},
            'vous': {'nominative': 'vous', 'accusative': 'vous', 'stressed': 'vous'},
            'ils': {'nominative': 'ils', 'accusative': 'les', 'stressed': 'eux'},
            'elles': {'nominative': 'elles', 'accusative': 'les', 'stressed': 'elles'}
        }
        
        if word in pronoun_cases:
            return pronoun_cases[word].get(case, word)
        
        return word


class FrenchStyleGuide(LanguageStyleGuide):
    """French style guide."""
    
    def __init__(self):
        super().__init__("fr")
    
    def _init_formality_levels(self) -> Dict[str, Dict[str, Any]]:
        """Initialize French formality levels."""
        return {
            "casual": {
                "pronouns": "tu",
                "contractions": True,
                "slang": True,
                "omit_ne": True,  # French often drops 'ne' in casual speech
                "sentence_starters": ["Bon", "Ben", "Alors", "Bref"],
                "connectives": ["et", "mais", "donc", "parce que"]
            },
            "neutral": {
                "pronouns": "vous",
                "contractions": True,
                "slang": False,
                "omit_ne": False,
                "sentence_starters": [],
                "connectives": ["et", "mais", "donc", "car"]
            },
            "formal": {
                "pronouns": "vous",
                "contractions": False,
                "slang": False,
                "omit_ne": False,
                "sentence_starters": ["En outre", "Par ailleurs", "De plus"],
                "connectives": ["et", "néanmoins", "par conséquent", "car"]
            },
            "literary": {
                "pronouns": "vous",
                "contractions": False,
                "slang": False,
                "subjunctive": True,
                "passé_simple": True,
                "literary_negation": True,  # Use 'point' instead of 'pas'
                "sentence_starters": ["Or", "Ainsi", "Au demeurant"],
                "connectives": ["et", "toutefois", "partant", "attendu que"]
            }
        }
    
    def apply_formality(self, text: str, formality_level: str) -> str:
        """Apply French formality transformations."""
        if formality_level not in self.formality_levels:
            return text
        
        rules = self.formality_levels[formality_level]
        
        # Apply pronoun changes
        if rules.get("pronouns") == "vous":
            text = self._use_vous(text)
        
        # Apply ne dropping for casual
        if rules.get("omit_ne", False):
            text = self._drop_ne(text)
        
        # Apply literary negation
        if rules.get("literary_negation", False):
            text = text.replace(" pas ", " point ")
        
        return text
    
    def get_domain_specific_style(self, domain: str) -> Dict[str, Any]:
        """Get domain-specific style preferences for French."""
        domain_styles = {
            "legal": {
                "precision": "high",
                "subjunctive": True,
                "formal_vocabulary": True,
                "passive_constructions": True,
                "avoid": ["peut-être", "probablement", "sans doute"]
            },
            "scientific": {
                "precision": "high",
                "objectivity": True,
                "impersonal": True,
                "present_tense": True,
                "anglicisms": True  # French science often uses English terms
            },
            "philosophical": {
                "abstract": True,
                "subjunctive": True,
                "complex_sentences": True,
                "conceptual_vocabulary": True
            },
            "everyday": {
                "precision": "medium",
                "colloquialisms": True,
                "contractions": True,
                "verlan": True  # French slang that reverses syllables
            }
        }
        
        return domain_styles.get(domain, {})
    
    def apply_rhetorical_emphasis(self, text: str, emphasis_type: str) -> str:
        """Apply rhetorical emphasis in French."""
        emphasis_patterns = {
            "strong": lambda t: f"Il est absolument certain que {t}",
            "subtle": lambda t: f"Il semblerait que {t}",
            "questioning": lambda t: f"N'est-il pas vrai que {t}?",
            "dramatic": lambda t: f"En vérité, {t}!",
            "understated": lambda t: f"On pourrait dire que {t}"
        }
        
        if emphasis_type in emphasis_patterns:
            return emphasis_patterns[emphasis_type](text)
        
        return text
    
    def _use_vous(self, text: str) -> str:
        """Convert to formal 'vous' form."""
        replacements = {
            'tu as': 'vous avez',
            'tu es': 'vous êtes',
            'tu peux': 'vous pouvez',
            'tu dois': 'vous devez',
            'tu sais': 'vous savez',
            'ton': 'votre',
            'ta': 'votre',
            'tes': 'vos'
        }
        
        for informal, formal in replacements.items():
            text = text.replace(informal, formal)
        
        return text
    
    def _drop_ne(self, text: str) -> str:
        """Drop 'ne' for casual French."""
        # Common patterns where 'ne' is dropped
        patterns = [
            (r"\bne\s+(\w+)\s+pas\b", r"\1 pas"),
            (r"\bn'(\w+)\s+pas\b", r"\1 pas"),
            (r"\bne\s+(\w+)\s+plus\b", r"\1 plus"),
            (r"\bn'(\w+)\s+plus\b", r"\1 plus"),
            (r"\bne\s+(\w+)\s+jamais\b", r"\1 jamais"),
            (r"\bn'(\w+)\s+jamais\b", r"\1 jamais")
        ]
        
        for pattern, replacement in patterns:
            text = re.sub(pattern, replacement, text)
        
        return text


class FrenchLanguageAdapter(LanguageAdapter):
    """Complete French language adapter."""
    
    def __init__(self):
        pattern = FrenchPattern()
        templates = FrenchTemplates(pattern)
        grammar = FrenchGrammar()
        style_guide = FrenchStyleGuide()
        
        super().__init__(pattern, templates, grammar, style_guide)


# Register the French adapter
from language_base import LanguageFactory
LanguageFactory.register_language("fr", FrenchLanguageAdapter)
