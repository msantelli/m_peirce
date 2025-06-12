"""
Spanish language handler for streamlined argument generation.
Contains all Spanish patterns and templates in a single class.
"""

import random
from typing import Dict, List, Tuple


class SpanishHandler:
    """Simplified Spanish language handler with all patterns and logic."""
    
    def __init__(self):
        self.language_code = "es"
        self.language_name = "Spanish"
        
        # Conclusion markers
        self.conclusion_markers = {
            'basic': ['Por lo tanto', 'Así', 'Por ende', 'Entonces', 'En consecuencia'],
            'formal': ['Por lo tanto', 'En consecuencia', 'Por ende', 'Así pues', 'Se sigue que'],
            'casual': ['Entonces', 'Así', 'Por eso', 'Por lo tanto']
        }
        
        # Conditional patterns
        self.conditional_patterns = {
            'basic': [
                'Si {p}, entonces {q}',
                'Si {p} entonces {q}',
                '{q} si {p}',
                'Dado {p}, {q}'
            ],
            'formal': [
                'Si {p}, entonces {q}',
                'Dado que {p}, {q}',
                'Siempre que {p}, {q}',
                'En el caso de que {p}, {q}'
            ],
            'causal': [
                '{p} implica {q}',
                '{p} lleva a {q}',
                '{p} resulta en {q}',
                '{p} causa {q}'
            ]
        }
        
        # Conjunction patterns
        self.conjunction_patterns = {
            'basic': [
                '{p} y {q}',
                '{p}, y {q}',
                'Tanto {p} como {q}',
                '{p} así como {q}'
            ],
            'formal': [
                '{p} y {q}',
                '{p} en conjunción con {q}',
                'Tanto {p} como {q}',
                '{p} junto con {q}'
            ]
        }
        
        # Disjunction patterns
        self.disjunction_patterns = {
            'inclusive': [
                '{p} o {q}',
                'O {p} o {q}',
                '{p} o {q} o ambos',
                '{p} y/o {q}'
            ],
            'exclusive': [
                'O {p} o {q} pero no ambos',
                'Exactamente uno de {p} o {q}',
                '{p} o {q}, pero no ambos'
            ]
        }
        
        # Negation patterns
        self.negation_patterns = {
            'basic': [
                'no {sentence}',
                '{sentence} es falso',
                '{sentence} no es el caso',
                '{sentence} no se cumple'
            ],
            'formal': [
                'no es el caso que {sentence}',
                'es falso que {sentence}',
                '{sentence} no es verdad',
                'la negación de {sentence}'
            ]
        }
    
    def format_sentence(self, sentence: str, style: str = "normal") -> str:
        """Format a sentence according to style preferences."""
        sentence = sentence.strip()
        
        # Ensure proper capitalization
        if sentence and not sentence[0].isupper():
            sentence = sentence[0].upper() + sentence[1:]
        
        # Ensure proper punctuation
        if sentence and sentence[-1] not in '.!?':
            sentence += '.'
        
        return sentence
    
    def negate_sentence(self, sentence: str, style: str = "basic") -> str:
        """Create a negated version of a sentence."""
        sentence = sentence.strip().rstrip('.!?')
        pattern = random.choice(self.negation_patterns.get(style, self.negation_patterns['basic']))
        return pattern.format(sentence=sentence)
    
    def generate_templates(self, rule_name: str, is_valid: bool = True) -> Dict[str, List[str]]:
        """Generate templates for a specific logical rule."""
        templates = {}
        
        if rule_name == "Modus Ponens":
            if is_valid:
                templates['premise_first'] = [
                    '{conditional}. {premise}. {conclusion} {result}.',
                    '{conditional}. {premise}. {conclusion}, {result}.',
                    '{conditional}. Dado que {premise}, {conclusion} {result}.'
                ]
                templates['conclusion_first'] = [
                    '{result} porque {premise}. Después de todo, {conditional}.',
                    '{result}, ya que {premise}. Dado que {conditional}.',
                    '{result}. Esto se sigue de {premise} y el hecho de que {conditional}.'
                ]
            else:  # Affirming the Consequent
                templates['premise_first'] = [
                    '{conditional}. {result}. {conclusion} {premise}.',
                    '{conditional}. {result}. {conclusion}, {premise}.',
                    '{conditional}. Dado que {result}, {conclusion} {premise}.'
                ]
                templates['conclusion_first'] = [
                    '{premise} porque {result}. Después de todo, {conditional}.',
                    '{premise}, ya que {result}. Dado que {conditional}.',
                    '{premise}. Esto se sigue de {result} y el hecho de que {conditional}.'
                ]
        
        elif rule_name == "Modus Tollens":
            if is_valid:
                templates['premise_first'] = [
                    '{conditional}. {negated_result}. {conclusion} {negated_premise}.',
                    '{conditional}. {negated_result}. {conclusion}, {negated_premise}.',
                    '{conditional}. Dado que {negated_result}, {conclusion} {negated_premise}.'
                ]
                templates['conclusion_first'] = [
                    '{negated_premise} porque {negated_result}. Después de todo, {conditional}.',
                    '{negated_premise}, ya que {negated_result}. Dado que {conditional}.',
                    '{negated_premise}. Esto se sigue de {negated_result} y el hecho de que {conditional}.'
                ]
            else:  # Denying the Antecedent
                templates['premise_first'] = [
                    '{conditional}. {negated_premise}. {conclusion} {negated_result}.',
                    '{conditional}. {negated_premise}. {conclusion}, {negated_result}.',
                    '{conditional}. Dado que {negated_premise}, {conclusion} {negated_result}.'
                ]
                templates['conclusion_first'] = [
                    '{negated_result} porque {negated_premise}. Después de todo, {conditional}.',
                    '{negated_result}, ya que {negated_premise}. Dado que {conditional}.',
                    '{negated_result}. Esto se sigue de {negated_premise} y el hecho de que {conditional}.'
                ]
        
        elif rule_name == "Conjunction Introduction":
            if is_valid:
                templates['premise_first'] = [
                    '{p}. {q}. {conclusion} {conjunction}.',
                    '{p}. {q}. {conclusion}, {conjunction}.',
                    '{p}. También, {q}. {conclusion} {conjunction}.'
                ]
                templates['conclusion_first'] = [
                    '{conjunction} porque {p} y {q}.',
                    '{conjunction}, ya que tanto {p} como {q}.',
                    '{conjunction}. Esto se sigue de {p} y {q}.'
                ]
            else:  # False Conjunction
                templates['premise_first'] = [
                    '{p}. {conclusion} {conjunction}.',
                    '{p}. {conclusion}, {conjunction}.',
                    'Dado que {p}, {conclusion} {conjunction}.'
                ]
                templates['conclusion_first'] = [
                    '{conjunction} porque {p}.',
                    '{conjunction}, ya que {p}.',
                    '{conjunction}. Esto se sigue de {p}.'
                ]
        
        # Add more rules as needed...
        
        return templates
    
    def create_conditional(self, p: str, q: str, style: str = "basic") -> str:
        """Create a conditional statement."""
        pattern = random.choice(self.conditional_patterns.get(style, self.conditional_patterns['basic']))
        return pattern.format(p=p.rstrip('.'), q=q.rstrip('.'))
    
    def create_conjunction(self, p: str, q: str, style: str = "basic") -> str:
        """Create a conjunction statement."""
        pattern = random.choice(self.conjunction_patterns.get(style, self.conjunction_patterns['basic']))
        return pattern.format(p=p.rstrip('.'), q=q.rstrip('.'))
    
    def create_disjunction(self, p: str, q: str, style: str = "inclusive") -> str:
        """Create a disjunction statement."""
        pattern = random.choice(self.disjunction_patterns.get(style, self.disjunction_patterns['inclusive']))
        return pattern.format(p=p.rstrip('.'), q=q.rstrip('.'))
    
    def get_conclusion_marker(self, style: str = "basic") -> str:
        """Get a random conclusion marker."""
        return random.choice(self.conclusion_markers.get(style, self.conclusion_markers['basic']))