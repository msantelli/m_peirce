"""
Spanish language handler for streamlined argument generation.
Contains all Spanish patterns and templates with context-aware capitalization.
"""

import random
from typing import Dict, List, Tuple


class SpanishHandler:
    """Spanish language handler with complete logical rules and context-aware capitalization."""
    
    def __init__(self):
        self.language_code = "es"
        self.language_name = "Spanish"
        
        # Conclusion markers (how we introduce the conclusion)
        self.conclusion_markers = {
            'basic': ['Por lo tanto', 'Así', 'Por ende', 'Entonces', 'En consecuencia'],
            'formal': ['Por lo tanto', 'En consecuencia', 'Por ende', 'Así pues', 'Se sigue que'],
            'casual': ['Entonces', 'Así', 'Por eso', 'Por lo tanto']
        }
        
        # Conditional patterns (if-then structures) 
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
        
        # Conjunction patterns (and structures)
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
        
        # Disjunction patterns (or structures)
        self.disjunction_patterns = {
            'inclusive': [
                '{p} o {q}',
                # 'O {p} o {q}',  # Commented to avoid capitalization issues
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
        
        # Remove any trailing punctuation first to avoid double punctuation
        sentence = sentence.rstrip('.!?')
        
        # Ensure proper capitalization
        if sentence and not sentence[0].isupper():
            sentence = sentence[0].upper() + sentence[1:]
        
        # Don't add period here - let templates control punctuation
        return sentence
    
    def negate_sentence(self, sentence: str, style: str = "basic") -> str:
        """Create a negated version of a sentence."""
        sentence = sentence.strip().rstrip('.!?')
        
        # Ensure proper capitalization for the base sentence
        if sentence and not sentence[0].isupper():
            sentence = sentence[0].upper() + sentence[1:]
        
        pattern = random.choice(self.negation_patterns.get(style, self.negation_patterns['basic']))
        result = pattern.format(sentence=sentence)
        
        # Ensure the result starts with proper capitalization
        if result and not result[0].isupper():
            result = result[0].upper() + result[1:]
        
        return result
    
    def generate_templates(self, rule_name: str, is_valid: bool = True) -> Dict[str, List[str]]:
        """Generate templates for a specific logical rule."""
        templates = {}
        
        if rule_name == "Modus Ponens":
            if is_valid:
                templates['premise_first'] = [
                    '{Conditional}. {P}. {conclusion} {q}.',
                    '{Conditional}. {P}. {conclusion}, {q}.',
                    '{Conditional}. Dado que {p}, {conclusion} {q}.'
                ]
                templates['conclusion_first'] = [
                    '{Q} porque {p}. Después de todo, {conditional}.',
                    '{Q}, ya que {p}. Dado que {conditional}.',
                    '{Q}. Esto se sigue de {p} y el hecho de que {conditional}.'
                ]
            else:  # Affirming the Consequent
                templates['premise_first'] = [
                    '{Conditional}. {Q}. {conclusion} {p}.',
                    '{Conditional}. {Q}. {conclusion}, {p}.',
                    '{Conditional}. Dado que {q}, {conclusion} {p}.'
                ]
                templates['conclusion_first'] = [
                    '{P} porque {q}. Después de todo, {conditional}.',
                    '{P}, ya que {q}. Dado que {conditional}.',
                    '{P}. Esto se sigue de {q} y el hecho de que {conditional}.'
                ]
        
        elif rule_name == "Modus Tollens":
            if is_valid:
                templates['premise_first'] = [
                    '{Conditional}. {Negated_result}. {conclusion} {negated_premise}.',
                    '{Conditional}. {Negated_result}. {conclusion}, {negated_premise}.',
                    '{Conditional}. Dado que {negated_result}, {conclusion} {negated_premise}.'
                ]
                templates['conclusion_first'] = [
                    '{Negated_premise} porque {negated_result}. Después de todo, {conditional}.',
                    '{Negated_premise}, ya que {negated_result}. Dado que {conditional}.',
                    '{Negated_premise}. Esto se sigue de {negated_result} y el hecho de que {conditional}.'
                ]
            else:  # Denying the Antecedent
                templates['premise_first'] = [
                    '{Conditional}. {Negated_premise}. {conclusion} {negated_result}.',
                    '{Conditional}. {Negated_premise}. {conclusion}, {negated_result}.',
                    '{Conditional}. Dado que {negated_premise}, {conclusion} {negated_result}.'
                ]
                templates['conclusion_first'] = [
                    '{Negated_result} porque {negated_premise}. Después de todo, {conditional}.',
                    '{Negated_result}, ya que {negated_premise}. Dado que {conditional}.',
                    '{Negated_result}. Esto se sigue de {negated_premise} y el hecho de que {conditional}.'
                ]
        
        elif rule_name == "Disjunctive Syllogism":
            if is_valid:
                templates['premise_first'] = [
                    '{Disjunction}. {Negated_p}. {conclusion} {q}.',
                    '{Disjunction}. {Negated_p}. {conclusion}, {q}.',
                    '{Disjunction}. Dado que {negated_p}, {conclusion} {q}.'
                ]
                templates['conclusion_first'] = [
                    '{Q} porque {negated_p}. Después de todo, {disjunction}.',
                    '{Q}, ya que {negated_p}. Dado que {disjunction}.',
                    '{Q}. Esto se sigue de {negated_p} y el hecho de que {disjunction}.'
                ]
            else:  # Affirming a Disjunct
                templates['premise_first'] = [
                    '{Disjunction}. {P}. {conclusion} {negated_q}.',
                    '{Disjunction}. {P}. {conclusion}, {negated_q}.',
                    '{Disjunction}. Dado que {p}, {conclusion} {negated_q}.'
                ]
                templates['conclusion_first'] = [
                    '{Negated_q} porque {p}. Después de todo, {disjunction}.',
                    '{Negated_q}, ya que {p}. Dado que {disjunction}.',
                    '{Negated_q}. Esto se sigue de {p} y el hecho de que {disjunction}.'
                ]
        
        elif rule_name == "Conjunction Introduction":
            if is_valid:
                templates['premise_first'] = [
                    '{P}. {Q}. {conclusion} {conjunction}.',
                    '{P}. {Q}. {conclusion}, {conjunction}.',
                    '{P}. También, {Q}. {conclusion} {conjunction}.'
                ]
                templates['conclusion_first'] = [
                    '{Conjunction} porque {p} y {q}.',
                    '{Conjunction}, ya que tanto {p} como {q}.',
                    '{Conjunction}. Esto se sigue de {p} y {q}.'
                ]
            else:  # False Conjunction  
                templates['premise_first'] = [
                    '{P}. {conclusion} {conjunction}.',
                    '{P}. {conclusion}, {conjunction}.',
                    'Dado que {p}, {conclusion} {conjunction}.'
                ]
                templates['conclusion_first'] = [
                    '{Conjunction} porque {p}.',
                    '{Conjunction}, ya que {p}.',
                    '{Conjunction}. Esto se sigue de {p}.'
                ]
        
        elif rule_name == "Conjunction Elimination":
            if is_valid:
                templates['premise_first'] = [
                    '{Conjunction}. {conclusion} {p}.',
                    '{Conjunction}. {conclusion}, {p}.',
                    'Dado que {conjunction}, {conclusion} {p}.'
                ]
                templates['conclusion_first'] = [
                    '{P} porque {conjunction}.',
                    '{P}, ya que {conjunction}.',
                    '{P}. Esto se sigue de {conjunction}.'
                ]
            else:  # Composition Fallacy
                templates['premise_first'] = [
                    'El grupo tiene la propiedad de que {p}. {conclusion} cada miembro {p}.',
                    'El equipo como conjunto {p}. {conclusion}, cada jugador {p}.',
                    'La organización {p}. {conclusion} cada empleado {p}.'
                ]
                templates['conclusion_first'] = [
                    'Cada miembro {p} porque el grupo tiene esta propiedad.',
                    'Cada individuo {p}, ya que el colectivo {p}.',
                    'Todas las partes {p} porque el conjunto {p}.'
                ]
        
        elif rule_name == "Disjunction Introduction":
            if is_valid:
                templates['premise_first'] = [
                    '{P}. {conclusion} {disjunction}.',
                    '{P}. {conclusion}, {disjunction}.',
                    'Dado que {p}, {conclusion} {disjunction}.'
                ]
                templates['conclusion_first'] = [
                    '{Disjunction} porque {p}.',
                    '{Disjunction}, ya que {p}.',
                    '{Disjunction}. Esto se sigue de {p}.'
                ]
            else:  # Invalid Conjunction Introduction
                templates['premise_first'] = [
                    '{P}. {conclusion} {conjunction}.',
                    '{P}. {conclusion}, {conjunction}.',
                    'Dado que {p}, {conclusion} {conjunction}.'
                ]
                templates['conclusion_first'] = [
                    '{Conjunction} porque {p}.',
                    '{Conjunction}, ya que {p}.',
                    '{Conjunction}. Esto se sigue de {p}.'
                ]
        
        elif rule_name == "Disjunction Elimination":
            if is_valid:
                templates['premise_first'] = [
                    '{Disjunction}. Si {p}, entonces {r}. Si {q}, entonces {r}. {conclusion} {r}.',
                    '{Disjunction}. {P} implica {r}. {Q} implica {r}. {conclusion}, {r}.',
                    'O {p} o {q}. En ambos casos, {R}. {conclusion} {r}.'
                ]
                templates['conclusion_first'] = [
                    '{R} porque de cualquier manera se sigue. Sabemos {disjunction}, y tanto {p} como {q} llevan a {r}.',
                    '{R}, ya que {disjunction} y ambas opciones implican {r}.',
                    '{R}. Esto se sigue de {disjunction} y el hecho de que tanto {p} como {q} resultan en {r}.'
                ]
            else:  # Invalid Disjunction Elimination
                templates['premise_first'] = [
                    '{Disjunction}. Si {p}, entonces {r}. {conclusion} {r}.',
                    '{Disjunction}. {P} implica {r}. {conclusion}, {r}.',
                    'O {p} o {q}. {P} lleva a {r}. {conclusion} {r}.'
                ]
                templates['conclusion_first'] = [
                    '{R} porque {p} lo implica. Sabemos {disjunction}.',
                    '{R}, ya que {p} lleva a ello y tenemos {disjunction}.',
                    '{R}. Esto se sigue de la posibilidad de {p} en {disjunction}.'
                ]
        
        elif rule_name == "Hypothetical Syllogism":
            if is_valid:
                templates['premise_first'] = [
                    '{Conditional1}. {Conditional2}. {conclusion} {conditional3}.',
                    '{Conditional1}. También, {Conditional2}. {conclusion}, {conditional3}.',
                    'Dado que {conditional1} y {conditional2}, {conclusion} {conditional3}.'
                ]
                templates['conclusion_first'] = [
                    '{Conditional3} porque {conditional1} y {conditional2}.',
                    '{Conditional3}, ya que {conditional1} y {conditional2}.',
                    '{Conditional3}. Esto se sigue de la cadena: {conditional1} y {conditional2}.'
                ]
            else:  # Non Sequitur
                templates['premise_first'] = [
                    '{P}. {conclusion} {q}.',
                    'Dado que {p}, {conclusion} {q}.',
                    '{P}. {conclusion}, {q}.'
                ]
                templates['conclusion_first'] = [
                    '{Q} porque {p}.',
                    '{Q}, ya que {p}.',
                    '{Q}. Esto de alguna manera se sigue de {p}.'
                ]
        
        elif rule_name == "Material Conditional Introduction":
            if is_valid:
                templates['premise_first'] = [
                    'O {negated_p} o {q}. {conclusion} {conditional}.',
                    '{Negated_p} o {q}. {conclusion}, {conditional}.',
                    'Dado que o {negated_p} o {q}, {conclusion} {conditional}.'
                ]
                templates['conclusion_first'] = [
                    '{Conditional} porque o {negated_p} o {q}.',
                    '{Conditional}, ya que {negated_p} o {q}.',
                    '{Conditional}. Esto se sigue de o {negated_p} o {q}.'
                ]
            else:  # Invalid Material Conditional Introduction
                templates['premise_first'] = [
                    'O {negated_p} o {q}. {conclusion} si {p}, entonces tanto {q} como {r}.',
                    '{Negated_p} o {q}. {conclusion}, si {p} entonces {q} y {r}.',
                    'Dado que o {negated_p} o {q}, {conclusion} {p} implica tanto {q} como {r}.'
                ]
                templates['conclusion_first'] = [
                    'Si {p}, entonces tanto {q} como {r} porque o {negated_p} o {q}.',
                    'Si {p} entonces {q} y {r}, ya que {negated_p} o {q}.',
                    '{P} implica tanto {q} como {r}. Esto se sigue de o {negated_p} o {q}.'
                ]
        
        elif rule_name == "Constructive Dilemma":
            if is_valid:
                templates['premise_first'] = [
                    '{Conditional1}. {Conditional2}. {Disjunction}. {conclusion} o {p} o {q} lleva a {r}.',
                    'Si {p}, entonces {r}. Si {q}, entonces {r}. O {p} o {q}. {conclusion}, {r}.',
                    '{Conditional1} y {conditional2}. Dado que {disjunction}, {conclusion} {r}.'
                ]
                templates['conclusion_first'] = [
                    '{R} porque {disjunction}. Dado {conditional1} y {conditional2}.',
                    '{R}, ya que {disjunction}. Sabemos {conditional1} y {conditional2}.',
                    '{R}. Esto se sigue de {disjunction} y los condicionales {conditional1} y {conditional2}.'
                ]
            else:  # False Dilemma
                templates['premise_first'] = [
                    'O {p} o {q}. {conclusion} una de estas debe ser verdad.',
                    '{p} o {q}. {conclusion}, estas son las únicas opciones.',
                    'Dado que o {p} o {q}, {conclusion} no existe otra posibilidad.'
                ]
                templates['conclusion_first'] = [
                    'Una de estas debe ser verdad porque o {p} o {q}.',
                    'Estas son las únicas opciones, ya que {p} o {q}.',
                    'No existe otra posibilidad. O {p} o {q} cubre todos los casos.'
                ]
        
        elif rule_name == "Destructive Dilemma":
            if is_valid:
                templates['premise_first'] = [
                    '{Conditional1}. {Conditional2}. O {negated_result1} o {negated_result2}. {conclusion} o {negated_p} o {negated_q}.',
                    'Si {p}, entonces {r}. Si {q}, entonces {r}. O {negated_result1} o {negated_result2}. {conclusion}, o {negated_p} o {negated_q}.',
                    '{Conditional1} y {conditional2}. Dado que o {negated_result1} o {negated_result2}, {conclusion} o {negated_p} o {negated_q}.'
                ]
                templates['conclusion_first'] = [
                    'O {negated_p} o {negated_q} porque o {negated_result1} o {negated_result2}. Dado {conditional1} y {conditional2}.',
                    'O {negated_p} o {negated_q}, ya que o {negated_result1} o {negated_result2}. Sabemos {conditional1} y {conditional2}.',
                    'O {negated_p} o {negated_q}. Esto se sigue de o {negated_result1} o {negated_result2} y los condicionales {conditional1} y {conditional2}.'
                ]
            else:  # Non Sequitur
                templates['premise_first'] = [
                    '{P}. {conclusion} {q}.',
                    'Dado que {p}, {conclusion} {q}.',
                    '{P}. {conclusion}, {q}.'
                ]
                templates['conclusion_first'] = [
                    '{Q} porque {p}.',
                    '{Q}, ya que {p}.',
                    '{Q}. Esto de alguna manera se sigue de {p}.'
                ]
        
        return templates
    
    def _is_proper_noun(self, text: str) -> bool:
        """Check if text starts with a proper noun that should remain capitalized."""
        # Spanish proper noun indicators
        proper_indicators = ['I ', 'Sr.', 'Sra.', 'Dr.', 'Dra.', 'Lunes', 'Martes', 'Miércoles', 
                           'Jueves', 'Viernes', 'Sábado', 'Domingo', 'Enero', 'Febrero', 
                           'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 
                           'Octubre', 'Noviembre', 'Diciembre']
        return any(text.startswith(indicator) for indicator in proper_indicators)
    
    def create_conditional(self, p: str, q: str, style: str = "basic") -> str:
        """Create a conditional statement."""
        pattern = random.choice(self.conditional_patterns.get(style, self.conditional_patterns['basic']))
        # Clean up the inputs - remove punctuation and extra spaces
        p_clean = p.strip().rstrip('.!?')
        q_clean = q.strip().rstrip('.!?')
        
        # Handle capitalization based on conditional pattern
        if pattern.startswith('Si {p}'):
            # For "Si P, entonces Q" patterns, P should be lowercase (not sentence start)
            if p_clean and p_clean[0].isupper() and not self._is_proper_noun(p_clean):
                p_clean = p_clean[0].lower() + p_clean[1:]
            # Q should also be lowercase in "entonces Q" context
            if q_clean and q_clean[0].isupper() and not self._is_proper_noun(q_clean):
                q_clean = q_clean[0].lower() + q_clean[1:]
        elif pattern.startswith('{q} si {p}'):
            # For "Q si P" patterns, P should be lowercase  
            if p_clean and p_clean[0].isupper() and not self._is_proper_noun(p_clean):
                p_clean = p_clean[0].lower() + p_clean[1:]
        elif pattern.startswith('Dado {p}') or 'Dado {p}' in pattern:
            # For "Dado P, Q" patterns, P should be lowercase
            if p_clean and p_clean[0].isupper() and not self._is_proper_noun(p_clean):
                p_clean = p_clean[0].lower() + p_clean[1:]
        
        return pattern.format(p=p_clean, q=q_clean)
    
    def create_conjunction(self, p: str, q: str, style: str = "basic") -> str:
        """Create a conjunction statement."""
        pattern = random.choice(self.conjunction_patterns.get(style, self.conjunction_patterns['basic']))
        # Clean up the inputs - remove punctuation and extra spaces  
        p_clean = p.strip().rstrip('.!?')
        q_clean = q.strip().rstrip('.!?')
        
        # Handle capitalization context for conjunctions  
        if pattern.startswith('{p} y {q}') or pattern.startswith('{p}, y {q}'):
            # For "p y q" patterns, q should be lowercase (not sentence start)
            if q_clean and q_clean[0].isupper() and not self._is_proper_noun(q_clean):
                q_clean = q_clean[0].lower() + q_clean[1:]
        elif pattern.startswith('Tanto {p} como {q}'):
            # For "Tanto p como q" patterns, both should be lowercase
            if p_clean and p_clean[0].isupper() and not self._is_proper_noun(p_clean):
                p_clean = p_clean[0].lower() + p_clean[1:]
            if q_clean and q_clean[0].isupper() and not self._is_proper_noun(q_clean):
                q_clean = q_clean[0].lower() + q_clean[1:]
        elif pattern.startswith('{p} así como {q}') or pattern.startswith('{p} junto con {q}') or pattern.startswith('{p} en conjunción con {q}'):
            # For patterns with connecting phrases, q should be lowercase
            if q_clean and q_clean[0].isupper() and not self._is_proper_noun(q_clean):
                q_clean = q_clean[0].lower() + q_clean[1:]
        
        return pattern.format(p=p_clean, q=q_clean)
    
    def create_disjunction(self, p: str, q: str, style: str = "inclusive") -> str:
        """Create a disjunction statement.""" 
        pattern = random.choice(self.disjunction_patterns.get(style, self.disjunction_patterns['inclusive']))
        # Clean up the inputs - remove punctuation and extra spaces
        p_clean = p.strip().rstrip('.!?')
        q_clean = q.strip().rstrip('.!?')
        
        # Handle capitalization context for disjunctions
        if pattern.startswith('{p} o {q}'):
            # For "p o q" patterns, q should be lowercase (not sentence start)
            if q_clean and q_clean[0].isupper() and not self._is_proper_noun(q_clean):
                q_clean = q_clean[0].lower() + q_clean[1:]
        elif pattern.startswith('O {p} o {q}'):
            # For "O p o q" patterns, both should be lowercase
            if p_clean and p_clean[0].isupper() and not self._is_proper_noun(p_clean):
                p_clean = p_clean[0].lower() + p_clean[1:]
            if q_clean and q_clean[0].isupper() and not self._is_proper_noun(q_clean):
                q_clean = q_clean[0].lower() + q_clean[1:]
        
        return pattern.format(p=p_clean, q=q_clean)
    
    def get_conclusion_marker(self, style: str = "basic") -> str:
        """Get a random conclusion marker."""
        return random.choice(self.conclusion_markers.get(style, self.conclusion_markers['basic']))