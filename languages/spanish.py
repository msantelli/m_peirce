"""
languages/spanish.py

Spanish language implementation for the argument generator.
"""

from typing import Dict, List, Tuple, Optional, Set, Any
import re
from language_base import (
    LanguageSpecificPattern, LanguageTemplates, 
    LanguageGrammar, LanguageStyleGuide, LanguageAdapter
)
from linguistic_patterns import ComplexityLevel
from template_system import TemplateBuilder, EnhancedTemplate


class SpanishPattern(LanguageSpecificPattern):
    """Spanish-specific linguistic patterns."""
    
    def __init__(self):
        super().__init__("es")
    
    def _init_negation_patterns(self) -> Dict[str, List[str]]:
        """Initialize Spanish negation patterns."""
        return {
            "simple": [
                "no es cierto que {sentence}",
                "{sentence} no es el caso",
                "no {sentence}",
                "{sentence} es falso",
                "{sentence} no es verdadero"
            ],
            "formal": [
                "es falso que {sentence}",
                "no es el caso que {sentence}",
                "la proposición de que {sentence} es falsa",
                "no es verdad que {sentence}",
                "la afirmación de que {sentence} es falsa"
            ],
            "emphatic": [
                "{sentence} es definitivamente falso",
                "{sentence} ciertamente no es el caso",
                "{sentence} es absolutamente falso",
                "de ninguna manera {sentence}",
                "en absoluto {sentence}"
            ]
        }
    
    def _init_conjunction_patterns(self) -> Dict[str, List[str]]:
        """Initialize Spanish conjunction patterns."""
        return {
            "simple": [
                "{p} y {q}",
                "{p}, y {q}",
                "tanto {p} como {q}",
                "{p} así como {q}",
                "{p} junto con {q}"
            ],
            "formal": [
                "{p} y también {q}",
                "{p}, además {q}",
                "{p}, asimismo {q}",
                "{p} conjuntamente con {q}",
                "la conjunción de {p} y {q}"
            ]
        }
    
    def _init_disjunction_patterns(self) -> Dict[str, List[str]]:
        """Initialize Spanish disjunction patterns."""
        return {
            "inclusive": [
                "{p} o {q}",
                "{p}, o {q}",
                "o {p} o {q} o ambos",
                "{p} y/o {q}",
                "{p} o alternativamente {q}"
            ],
            "exclusive": [
                "o {p} o {q} pero no ambos",
                "exactamente uno de {p} o {q}",
                "{p} o {q}, pero no ambos",
                "o {p} o {q} (exclusivo)"
            ]
        }
    
    def _init_conditional_patterns(self) -> Dict[str, List[str]]:
        """Initialize Spanish conditional patterns."""
        return {
            "standard": [
                "si {antecedent}, entonces {consequent}",
                "si {antecedent} entonces {consequent}",
                "{consequent} si {antecedent}",
                "dado {antecedent}, {consequent}",
                "cuando {antecedent}, {consequent}"
            ],
            "causal": [
                "porque {antecedent}, {consequent}",
                "{antecedent} causa {consequent}",
                "{antecedent} lleva a {consequent}",
                "{antecedent} resulta en {consequent}",
                "{antecedent} produce {consequent}"
            ]
        }
    
    def _init_connectives(self) -> Dict[str, List[str]]:
        """Initialize Spanish logical connectives."""
        return {
            "conclusion": [
                "por lo tanto", "así", "por ende", "en consecuencia",
                "entonces", "por consiguiente", "como resultado",
                "se sigue que", "podemos concluir que", "esto significa que"
            ],
            "premise": [
                "ya que", "porque", "como", "dado que",
                "considerando que", "debido a", "puesto que"
            ],
            "assumption": [
                "supongamos", "asumamos", "digamos", "imaginemos",
                "consideremos", "supone que"
            ]
        }
    
    def format_sentence(self, sentence: str, formatting_type: str) -> str:
        """Apply Spanish-specific formatting."""
        if formatting_type == "capitalize":
            return self.capitalize_sentence(sentence)
        elif formatting_type == "negate":
            return self._simple_negate(sentence)
        return sentence
    
    def normalize_sentence(self, sentence: str) -> str:
        """Normalize a Spanish sentence."""
        # Remove trailing punctuation
        sentence = sentence.rstrip('.!?;:,')
        
        # Convert to lowercase
        sentence = sentence.lower()
        
        # Remove extra whitespace
        sentence = ' '.join(sentence.split())
        
        return sentence
    
    def capitalize_sentence(self, sentence: str) -> str:
        """Capitalize a Spanish sentence properly."""
        if not sentence:
            return sentence
        
        return sentence[0].upper() + sentence[1:]
    
    def _simple_negate(self, sentence: str) -> str:
        """Apply simple negation to a Spanish sentence."""
        if " es " in sentence:
            return sentence.replace(" es ", " no es ", 1)
        elif " son " in sentence:
            return sentence.replace(" son ", " no son ", 1)
        else:
            return f"no es cierto que {sentence}"


class SpanishTemplates(LanguageTemplates):
    """Spanish-specific argument templates."""
    
    def __init__(self, language_pattern: SpanishPattern):
        super().__init__(language_pattern)
    
    def _init_templates(self) -> Dict[str, Dict[str, List[EnhancedTemplate]]]:
        """Initialize Spanish templates - all 11 logical rules."""
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
            "invalid": self._create_hypothetical_syllogism_invalid() + self._create_destructive_dilemma_invalid()
        }
        
        templates["Invalid Material Conditional Introduction"] = {
            "invalid": self._create_material_conditional_introduction_invalid()
        }
        
        return templates
    
    def _create_modus_ponens_valid(self) -> List[EnhancedTemplate]:
        """Create valid Modus Ponens templates in Spanish."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('conditional', [
            'Si {p}, entonces {q}',
            '{Q} si {p}',
            '{P} implica {q}',
            '{P} lleva a {q}'
        ])
        builder.add_static('. ')
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Por lo tanto',
            'Así',
            'Por ende',
            'En consecuencia'
        ])
        builder.add_static(', ')
        builder.add_variable('q')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        
        templates.append(builder.build())
        return templates
    
    def _create_modus_ponens_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Modus Ponens templates (Affirming the Consequent) in Spanish."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('conditional', [
            'Si {p}, entonces {q}',
            '{Q} si {p}',
            '{P} implica {q}'
        ])
        builder.add_static('. ')
        builder.add_variable('Q')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Por lo tanto',
            'Así',
            'Por ende'
        ])
        builder.add_static(', ')
        builder.add_variable('p')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_modus_tollens_valid(self) -> List[EnhancedTemplate]:
        """Create valid Modus Tollens templates in Spanish."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('conditional', [
            'Si {p}, entonces {q}',
            '{Q} si {p}',
            '{P} implica {q}'
        ])
        builder.add_static('. ')
        builder.add_variable('not_Q')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Por lo tanto',
            'Así',
            'Por ende'
        ])
        builder.add_static(', ')
        builder.add_variable('not_p')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_modus_tollens_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Modus Tollens templates (Denying the Antecedent) in Spanish."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('conditional', [
            'Si {p}, entonces {q}',
            '{Q} si {p}',
            '{P} implica {q}'
        ])
        builder.add_static('. ')
        builder.add_variable('not_P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Por lo tanto',
            'Así',
            'Por ende'
        ])
        builder.add_static(', ')
        builder.add_variable('not_q')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_disjunctive_syllogism_valid(self) -> List[EnhancedTemplate]:
        """Create valid Disjunctive Syllogism templates in Spanish."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('disjunction', [
            '{P} o {q}',
            'O {p} o {q}',
            '{P}, o alternativamente {q}',
            'Bien {p} o bien {q}'
        ])
        builder.add_static('. ')
        builder.add_variable('not_P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Por lo tanto',
            'Así',
            'Por ende',
            'En consecuencia'
        ])
        builder.add_static(', ')
        builder.add_variable('q')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_disjunctive_syllogism_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Disjunctive Syllogism templates (Affirming a Disjunct) in Spanish."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('disjunction', [
            '{P} o {q}',
            'O {p} o {q}',
            '{P}, o alternativamente {q}'
        ])
        builder.add_static('. ')
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Por lo tanto',
            'Así',
            'Por ende'
        ])
        builder.add_static(', ')
        builder.add_variable('not_q')
        builder.add_static(' no es el caso.')
        
        templates.append(builder.build())
        return templates
    
    def _create_conjunction_introduction_valid(self) -> List[EnhancedTemplate]:
        """Create valid Conjunction Introduction templates in Spanish."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variable('Q')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Por lo tanto',
            'Así',
            'En consecuencia'
        ])
        builder.add_static(', ')
        builder.add_variation('conjunction', [
            '{p} y {q}',
            'tanto {p} como {q}',
            '{p} junto con {q}'
        ])
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_conjunction_introduction_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Conjunction Introduction templates (False Conjunction) in Spanish."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Por lo tanto',
            'Así',
            'En consecuencia'
        ])
        builder.add_static(', ')
        builder.add_variation('conjunction', [
            '{p} y {q}',
            'tanto {p} como {q}'
        ])
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_conjunction_elimination_valid(self) -> List[EnhancedTemplate]:
        """Create valid Conjunction Elimination templates in Spanish."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('conjunction', [
            '{P} y {q}',
            'Tanto {p} como {q}',
            '{P} junto con {q}'
        ])
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Por lo tanto',
            'Así',
            'En consecuencia'
        ])
        builder.add_static(', ')
        builder.add_variable('p')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_conjunction_elimination_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Conjunction Elimination templates (Composition Fallacy) in Spanish."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static(' tiene la propiedad {q}. ')
        builder.add_variation('conclusion', [
            'Por lo tanto',
            'Así',
            'En consecuencia'
        ])
        builder.add_static(', el conjunto de ')
        builder.add_variable('p')
        builder.add_static(' tiene la propiedad ')
        builder.add_variable('q')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_disjunction_introduction_valid(self) -> List[EnhancedTemplate]:
        """Create valid Disjunction Introduction templates in Spanish."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Por lo tanto',
            'Así',
            'En consecuencia'
        ])
        builder.add_static(', ')
        builder.add_variation('disjunction', [
            '{p} o {q}',
            'o {p} o {q}',
            '{p}, o alternativamente {q}'
        ])
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_invalid_conjunction_introduction(self) -> List[EnhancedTemplate]:
        """Create Invalid Conjunction Introduction templates (A / Therefore, A and B) in Spanish."""
        templates = []
        
        # Basic invalid conjunction introduction
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Por lo tanto',
            'Así',
            'En consecuencia',
            'Entonces'
        ])
        builder.add_static(', ')
        builder.add_variation('conjunction', [
            '{p} y {q}',
            'tanto {p} como {q}',
            '{p} así como {q}'
        ])
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        # Intermediate version with more sophisticated language
        builder2 = TemplateBuilder()
        builder2.add_variable('P')
        builder2.add_static('. ')
        builder2.add_variation('conclusion', [
            'Se sigue que',
            'Podemos concluir que',
            'Esto significa que'
        ])
        builder2.add_static(' ')
        builder2.add_variation('conjunction', [
            'no solo {p} sino también {q}',
            '{p} y además {q}',
            '{p} junto con {q}'
        ])
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        templates.append(builder2.build())
        
        return templates
    
    def _create_disjunction_elimination_valid(self) -> List[EnhancedTemplate]:
        """Create valid Disjunction Elimination templates in Spanish."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('disjunction', [
            '{p} o {q}',
            'o {p} o {q}',
            '{p}, o alternativamente {q}'
        ])
        builder.add_static('. Si ')
        builder.add_variable('p')
        builder.add_static(', entonces ')
        builder.add_variable('r')
        builder.add_static('. Si ')
        builder.add_variable('q')
        builder.add_static(', entonces ')
        builder.add_variable('r')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Por lo tanto',
            'Así',
            'En consecuencia'
        ])
        builder.add_static(', ')
        builder.add_variable('r')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_disjunction_elimination_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Disjunction Elimination templates in Spanish."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('disjunction', [
            '{p} o {q}',
            'o {p} o {q}'
        ])
        builder.add_static('. ')
        builder.add_variable('P')
        builder.add_static(' implica ')
        builder.add_variable('r')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Por lo tanto',
            'Así'
        ])
        builder.add_static(', ')
        builder.add_variable('r')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_hypothetical_syllogism_valid(self) -> List[EnhancedTemplate]:
        """Create valid Hypothetical Syllogism templates in Spanish."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variation('conditional1', [
            'Si {p}, entonces {q}',
            '{q} si {p}',
            '{p} implica {q}'
        ])
        builder.add_static('. ')
        builder.add_variation('conditional2', [
            'Si {q}, entonces {r}',
            '{r} si {q}',
            '{q} implica {r}'
        ])
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Por lo tanto',
            'Así',
            'En consecuencia'
        ])
        builder.add_static(', si ')
        builder.add_variable('p')
        builder.add_static(', entonces ')
        builder.add_variable('r')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_hypothetical_syllogism_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Hypothetical Syllogism templates (Non Sequitur) in Spanish."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Por lo tanto',
            'Así',
            'En consecuencia'
        ])
        builder.add_static(', ')
        builder.add_variable('q')
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_material_conditional_introduction_valid(self) -> List[EnhancedTemplate]:
        """Create valid Material Conditional Introduction templates in Spanish."""
        templates = []
        
        # Plantilla 1: Estilo formal original
        builder1 = TemplateBuilder()
        builder1.add_static('Supongamos que ')
        builder1.add_variable('p')
        builder1.add_static(', podemos derivar que ')
        builder1.add_variable('q')
        builder1.add_static('. ')
        builder1.add_variation('conclusion', [
            'Por lo tanto',
            'Así',
            'En consecuencia'
        ])
        builder1.add_static(', ')
        builder1.add_variation('conditional', [
            'si {p}, entonces {q}',
            '{p} implica {q}'
        ])
        builder1.add_static('.')
        templates.append(builder1.build())
        
        # Plantilla 2: Estilo de suposición natural
        builder2 = TemplateBuilder()
        builder2.add_variation('suppose', [
            'Cuando suponemos que {p}',
            'Si aceptamos que {p}',
            'Dado {p} como premisa'
        ])
        builder2.add_static(', ')
        builder2.add_variation('follows', [
            'se sigue que {q}',
            'obtenemos {q}',
            'resulta que {q}'
        ])
        builder2.add_static('. ')
        builder2.add_variation('establishes', [
            'Esto establece que',
            'Podemos concluir que',
            'Esto demuestra que'
        ])
        builder2.add_static(' ')
        builder2.add_variation('conditional', [
            '{p} implica {q}',
            'si {p}, entonces {q}',
            '{p} conduce a {q}'
        ])
        builder2.add_static('.')
        templates.append(builder2.build())
        
        # Plantilla 3: Formato de prueba
        builder3 = TemplateBuilder()
        builder3.add_variation('proof_start', [
            'Supongamos {p}',
            'Sea {p} dado',
            'Asumamos {p} por argumento'
        ])
        builder3.add_static('. ')
        builder3.add_variation('derivation', [
            'De esto, se sigue {q}',
            'Entonces {q} debe ser cierto',
            'Esto produce {q}'
        ])
        builder3.add_static('. ')
        builder3.add_variation('conclusion', [
            'Por lo tanto',
            'En consecuencia',
            'Así'
        ])
        builder3.add_static(', ')
        builder3.add_variation('conditional', [
            '{p} → {q}',
            'si {p}, entonces {q}',
            '{p} implica {q}'
        ])
        builder3.add_static('.')
        templates.append(builder3.build())
        
        # Plantilla 4: Orden inverso (conclusión primero)
        builder4 = TemplateBuilder()
        builder4.add_static('Establecemos que ')
        builder4.add_variation('conditional', [
            '{p} implica {q}',
            'si {p}, entonces {q}',
            '{p} garantiza {q}'
        ])
        builder4.add_static(' ')
        builder4.add_variation('justification', [
            'porque suponer {p} conduce a {q}',
            'ya que asumir {p} resulta en {q}',
            'dado que {p} produce {q}'
        ])
        builder4.add_static('.')
        templates.append(builder4.build())
        
        return templates
    
    def _create_material_conditional_introduction_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Material Conditional Introduction templates in Spanish."""
        templates = []
        
        # Patrón inválido: Suponer P, derivar Q, pero concluir condicional inválido con variable extra
        builder = TemplateBuilder()
        builder.add_static('Supongamos que ')
        builder.add_variable('p')
        builder.add_static(', ')
        builder.add_variable('q')
        builder.add_static(' es derivable. ')
        builder.add_variation('conclusion', [
            'Así',
            'Por lo tanto',
            'En consecuencia'
        ])
        builder.add_static(', ')
        builder.add_variation('conditional', [
            'si {p} entonces {q} y {r}',
            'si {p}, entonces {q} y {r}'
        ])
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_constructive_dilemma_valid(self) -> List[EnhancedTemplate]:
        """Create valid Constructive Dilemma templates in Spanish."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variable('p')
        builder.add_static(' implica ')
        builder.add_variable('q')
        builder.add_static('. ')
        builder.add_variable('r')
        builder.add_static(' implica ')
        builder.add_variable('s')
        builder.add_static('. ')
        builder.add_variation('disjunction', [
            'o {p} o {r}',
            '{p} o {r}',
            'bien {p} o bien {r}'
        ])
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Por lo tanto',
            'Así',
            'En consecuencia'
        ])
        builder.add_static(', ')
        builder.add_variation('result_disjunction', [
            'o {q} o {s}',
            '{q} o {s}',
            'bien {q} o bien {s}'
        ])
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_constructive_dilemma_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Constructive Dilemma templates (False Dilemma) in Spanish."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Por lo tanto',
            'Así'
        ])
        builder.add_static(', o ')
        builder.add_variable('p')
        builder.add_static(' o ')
        builder.add_variable('q')
        builder.add_static(' (no hay otras opciones).')
        
        templates.append(builder.build())
        return templates
    
    def _create_destructive_dilemma_valid(self) -> List[EnhancedTemplate]:
        """Create valid Destructive Dilemma templates in Spanish."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_static('Si ')
        builder.add_variable('p')
        builder.add_static(', entonces ')
        builder.add_variable('q')
        builder.add_static('. Si ')
        builder.add_variable('r')
        builder.add_static(', entonces ')
        builder.add_variable('s')
        builder.add_static('. ')
        builder.add_variation('negated_disjunction', [
            'No {q} o no {s}',
            'o no {q} o no {s}',
            'bien no {q} o bien no {s}'
        ])
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Por lo tanto',
            'Así',
            'En consecuencia'
        ])
        builder.add_static(', ')
        builder.add_variation('negated_result', [
            'no {p} o no {r}',
            'o no {p} o no {r}',
            'bien no {p} o bien no {r}'
        ])
        builder.add_static('.')
        
        templates.append(builder.build())
        return templates
    
    def _create_destructive_dilemma_invalid(self) -> List[EnhancedTemplate]:
        """Create invalid Destructive Dilemma templates (Non Sequitur) in Spanish."""
        templates = []
        
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Por lo tanto',
            'Así'
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
            "Conjunction Elimination": 2,
            "Disjunction Introduction": 2,
            "Disjunction Elimination": 4,
            "Hypothetical Syllogism": 3,
            "Material Conditional Introduction": 3,
            "Constructive Dilemma": 4,
            "Destructive Dilemma": 4,
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


class SpanishGrammar(LanguageGrammar):
    """Spanish grammar rules."""
    
    def __init__(self):
        super().__init__("es")
    
    def apply_agreement(self, subject: str, verb: str, 
                       object: Optional[str] = None) -> Tuple[str, str, Optional[str]]:
        """Apply subject-verb agreement for Spanish."""
        # Simplified Spanish agreement
        return subject, verb, object
    
    def apply_article_rules(self, noun: str, definite: bool = False) -> str:
        """Apply Spanish article rules."""
        if definite:
            # Simplified - should check gender and number
            return f"el {noun}"  # masculine singular default
        else:
            return f"un {noun}"  # masculine singular default
    
    def apply_word_order(self, components: Dict[str, str]) -> str:
        """Apply Spanish SVO word order."""
        parts = []
        
        if 'subject' in components:
            parts.append(components['subject'])
        if 'verb' in components:
            parts.append(components['verb'])
        if 'object' in components:
            parts.append(components['object'])
        
        for key, value in components.items():
            if key not in ['subject', 'verb', 'object']:
                parts.append(value)
        
        return ' '.join(parts)
    
    def pluralize(self, word: str, count: int = 2) -> str:
        """Pluralize a Spanish word."""
        if count == 1:
            return word
        
        # Basic Spanish pluralization
        if word.endswith(('a', 'e', 'o')):
            return word + 's'
        elif word.endswith(('r', 'l', 'n', 'd', 'z')):
            return word + 'es'
        else:
            return word + 's'
    
    def apply_case(self, word: str, case: str) -> str:
        """Spanish doesn't have grammatical cases like German."""
        return word


class SpanishStyleGuide(LanguageStyleGuide):
    """Spanish style guide."""
    
    def __init__(self):
        super().__init__("es")
    
    def _init_formality_levels(self) -> Dict[str, Dict[str, Any]]:
        """Initialize Spanish formality levels."""
        return {
            "casual": {
                "contractions": True,
                "informal_pronouns": True,
                "connectives": ["y", "pero", "entonces", "porque"]
            },
            "formal": {
                "contractions": False,
                "formal_pronouns": True,
                "connectives": ["y", "sin embargo", "por lo tanto", "porque", "en consecuencia"]
            }
        }
    
    def apply_formality(self, text: str, formality_level: str) -> str:
        """Apply Spanish formality transformations."""
        return text
    
    def get_domain_specific_style(self, domain: str) -> Dict[str, Any]:
        """Get domain-specific style preferences for Spanish."""
        return {}
    
    def apply_rhetorical_emphasis(self, text: str, emphasis_type: str) -> str:
        """Apply rhetorical emphasis in Spanish."""
        return text


class SpanishLanguageAdapter(LanguageAdapter):
    """Complete Spanish language adapter."""
    
    def __init__(self):
        pattern = SpanishPattern()
        templates = SpanishTemplates(pattern)
        grammar = SpanishGrammar()
        style_guide = SpanishStyleGuide()
        
        super().__init__(pattern, templates, grammar, style_guide)


# Register the Spanish adapter
from language_base import LanguageFactory
LanguageFactory.register_language("es", SpanishLanguageAdapter)