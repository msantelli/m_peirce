"""
English language handler for streamlined argument generation.
Contains all English patterns and templates in a single class.
"""

import random
from typing import Dict, List, Tuple


class EnglishHandler:
    """Simplified English language handler with all patterns and logic."""
    
    def __init__(self):
        self.language_code = "en"
        self.language_name = "English"
        
        # Conclusion markers (how we introduce the conclusion)
        self.conclusion_markers = {
            'basic': ['Therefore', 'Thus', 'Hence', 'So', 'Consequently'],
            'formal': ['Therefore', 'Thus', 'Hence', 'Consequently', 'It follows that'],
            'casual': ['So', 'Thus', 'Therefore', 'Hence']
        }
        
        # Conditional patterns (if-then structures) 
        self.conditional_patterns = {
            'basic': [
                'If {p}, then {q}',
                'If {p} then {q}',
                '{q} if {p}',
                'Given {p}, {q}'
            ],
            'formal': [
                'If {p}, then {q}',
                'Given that {p}, {q}',
                'Provided that {p}, {q}',
                'On the condition that {p}, {q}'
            ],
            'causal': [
                '{p} implies {q}',
                '{p} leads to {q}',
                '{p} results in {q}',
                '{p} causes {q}'
            ]
        }
        
        # Conjunction patterns (and structures)
        self.conjunction_patterns = {
            'basic': [
                '{p} and {q}',
                '{p}, and {q}',
                'Both {p} and {q}',
                '{p} as well as {q}'
            ],
            'formal': [
                '{p} and {q}',
                '{p} in conjunction with {q}',
                'Both {p} and {q}',
                '{p} together with {q}'
            ]
        }
        
        # Disjunction patterns (or structures)
        self.disjunction_patterns = {
            'inclusive': [
                '{p} or {q}',
                #'Either {p} or {q}',
                            ],
            'exclusive': [
                'Either {p} or {q} but not both',
                'Exactly one of {p} or {q}',
                '{p} or {q}, but not both'
            ]
        }
        
        # Negation patterns
        self.negation_patterns = {
            'basic': [
                'not {sentence}',
                '{sentence} is false',
                '{sentence} is not the case',
                '{sentence} doesn\'t hold'
            ],
            'formal': [
                'it is not the case that {sentence}',
                'it is false that {sentence}',
                '{sentence} is not true',
                'the negation of {sentence}'
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
                    '{Conditional}. Since {p}, {conclusion} {q}.'
                ]
                templates['conclusion_first'] = [
                    '{Q} because {p}. After all, {conditional}.',
                    '{Q}, since {p}. Given that {conditional}.',
                    '{Q}. This follows from {p} and the fact that {conditional}.'
                ]
            else:  # Affirming the Consequent
                templates['premise_first'] = [
                    '{Conditional}. {Q}. {conclusion} {p}.',
                    '{Conditional}. {Q}. {conclusion}, {p}.',
                    '{Conditional}. Since {q}, {conclusion} {p}.'
                ]
                templates['conclusion_first'] = [
                    '{P} because {q}. After all, {conditional}.',
                    '{P}, since {q}. Given that {conditional}.',
                    '{P}. This follows from {q} and the fact that {conditional}.'
                ]
        
        elif rule_name == "Modus Tollens":
            if is_valid:
                templates['premise_first'] = [
                    '{Conditional}. {Negated_result}. {conclusion} {negated_premise}.',
                    '{Conditional}. {Negated_result}. {conclusion}, {negated_premise}.',
                    '{Conditional}. Since {negated_result}, {conclusion} {negated_premise}.'
                ]
                templates['conclusion_first'] = [
                    '{Negated_premise} because {negated_result}. After all, {conditional}.',
                    '{Negated_premise}, since {negated_result}. Given that {conditional}.',
                    '{Negated_premise}. This follows from {negated_result} and the fact that {conditional}.'
                ]
            else:  # Denying the Antecedent
                templates['premise_first'] = [
                    '{Conditional}. {Negated_premise}. {conclusion} {negated_result}.',
                    '{Conditional}. {Negated_premise}. {conclusion}, {negated_result}.',
                    '{Conditional}. Since {negated_premise}, {conclusion} {negated_result}.'
                ]
                templates['conclusion_first'] = [
                    '{Negated_result} because {negated_premise}. After all, {conditional}.',
                    '{Negated_result}, since {negated_premise}. Given that {conditional}.',
                    '{Negated_result}. This follows from {negated_premise} and the fact that {conditional}.'
                ]
        
        elif rule_name == "Disjunctive Syllogism":
            if is_valid:
                templates['premise_first'] = [
                    '{Disjunction}. {Negated_p}. {conclusion} {q}.',
                    '{Disjunction}. {Negated_p}. {conclusion}, {q}.',
                    '{Disjunction}. Since {negated_p}, {conclusion} {q}.'
                ]
                templates['conclusion_first'] = [
                    '{Q} because {negated_p}. After all, {disjunction}.',
                    '{Q}, since {negated_p}. Given that {disjunction}.',
                    '{Q}. This follows from {negated_p} and the fact that {disjunction}.'
                ]
            else:  # Affirming a Disjunct
                templates['premise_first'] = [
                    '{Disjunction}. {P}. {conclusion} {negated_q}.',
                    '{Disjunction}. {P}. {conclusion}, {negated_q}.',
                    '{Disjunction}. Since {p}, {conclusion} {negated_q}.'
                ]
                templates['conclusion_first'] = [
                    '{Negated_q} because {p}. After all, {disjunction}.',
                    '{Negated_q}, since {p}. Given that {disjunction}.',
                    '{Negated_q}. This follows from {p} and the fact that {disjunction}.'
                ]
        
        elif rule_name == "Conjunction Introduction":
            if is_valid:
                templates['premise_first'] = [
                    '{P}. {Q}. {conclusion} {conjunction}.',
                    '{P}. {Q}. {conclusion}, {conjunction}.',
                    '{P}. Also, {Q}. {conclusion} {conjunction}.'
                ]
                templates['conclusion_first'] = [
                    '{Conjunction} because {p} and {q}.',
                    '{Conjunction}, since both {p} and {q}.',
                    '{Conjunction}. This follows from {p} and {q}.'
                ]
            else:  # False Conjunction  
                templates['premise_first'] = [
                    '{P}. {conclusion} {conjunction}.',
                    '{P}. {conclusion}, {conjunction}.',
                    'Since {p}, {conclusion} {conjunction}.'
                ]
                templates['conclusion_first'] = [
                    '{Conjunction} because {p}.',
                    '{Conjunction}, since {p}.',
                    '{Conjunction}. This follows from {p}.'
                ]
        
        elif rule_name == "Conjunction Elimination":
            if is_valid:
                templates['premise_first'] = [
                    '{Conjunction}. {conclusion} {p}.',
                    '{Conjunction}. {conclusion}, {p}.',
                    'Since {conjunction}, {conclusion} {p}.'
                ]
                templates['conclusion_first'] = [
                    '{P} because {conjunction}.',
                    '{P}, since {conjunction}.',
                    '{P}. This follows from {conjunction}.'
                ]
            else:  # Composition Fallacy
                templates['premise_first'] = [
                    'The group has the property that {p}. {conclusion} every member {p}.',
                    'The team as a whole {p}. {conclusion}, each player {p}.',
                    'The organization {p}. {conclusion} every employee {p}.'
                ]
                templates['conclusion_first'] = [
                    'Every member {p} because the group has this property.',
                    'Each individual {p}, since the collective {p}.',
                    'All parts {p} because the whole {p}.'
                ]
        
        elif rule_name == "Disjunction Introduction":
            if is_valid:
                templates['premise_first'] = [
                    '{P}. {conclusion} {disjunction}.',
                    '{P}. {conclusion}, {disjunction}.',
                    'Since {p}, {conclusion} {disjunction}.'
                ]
                templates['conclusion_first'] = [
                    '{Disjunction} because {p}.',
                    '{Disjunction}, since {p}.',
                    '{Disjunction}. This follows from {p}.'
                ]
            else:  # Invalid Conjunction Introduction
                templates['premise_first'] = [
                    '{P}. {conclusion} {conjunction}.',
                    '{P}. {conclusion}, {conjunction}.',
                    'Since {p}, {conclusion} {conjunction}.'
                ]
                templates['conclusion_first'] = [
                    '{Conjunction} because {p}.',
                    '{Conjunction}, since {p}.',
                    '{Conjunction}. This follows from {p}.'
                ]
        
        elif rule_name == "Disjunction Elimination":
            if is_valid:
                templates['premise_first'] = [
                    '{Disjunction}. If {p}, then {r}. If {q}, then {r}. {conclusion} {r}.',
                    '{Disjunction}. {P} implies {r}. {Q} implies {r}. {conclusion}, {r}.'
                    'Either {p} or {q}. In both cases, {R}. {conclusion} {r}.'
                ]
                templates['conclusion_first'] = [
                    '{R} because either way it follows. We know {disjunction}, and both {p} and {q} lead to {r}.',
                    '{R}, since {disjunction} and both options imply {r}.',
                    '{R}. This follows from {disjunction} and the fact that both {p} and {q} result in {r}.'
                ]
            else:  # Invalid Disjunction Elimination
                templates['premise_first'] = [
                    '{Disjunction}. If {p}, then {r}. {conclusion} {r}.',
                    '{Disjunction}. {P} implies {r}. {conclusion}, {r}.',
                    'Either {p} or {q}. {P} leads to {r}. {conclusion} {r}.'
                ]
                templates['conclusion_first'] = [
                    '{R} because {p} implies it. We know {disjunction}.',
                    '{R}, since {p} leads to it and we have {disjunction}.',
                    '{R}. This follows from the possibility of {p} in {disjunction}.'
                ]
        
        elif rule_name == "Hypothetical Syllogism":
            if is_valid:
                templates['premise_first'] = [
                    '{Conditional1}. {Conditional2}. {conclusion} {conditional3}.',
                    '{Conditional1}. Also, {Conditional2}. {conclusion}, {conditional3}.',
                    'Given that {conditional1} and {conditional2}, {conclusion} {conditional3}.'
                ]
                templates['conclusion_first'] = [
                    '{Conditional3} because {conditional1} and {conditional2}.',
                    '{Conditional3}, since {conditional1} and {conditional2}.',
                    '{Conditional3}. This follows from the chain: {conditional1} and {conditional2}.'
                ]
            else:  # Non Sequitur
                templates['premise_first'] = [
                    '{P}. {conclusion} {q}.',
                    'Since {p}, {conclusion} {q}.',
                    '{P}. {conclusion}, {q}.'
                ]
                templates['conclusion_first'] = [
                    '{Q} because {p}.',
                    '{Q}, since {p}.',
                    '{Q}. This somehow follows from {p}.'
                ]
        
        elif rule_name == "Material Conditional Introduction":
            if is_valid:
                templates['premise_first'] = [
                    'Either {negated_p} or {q}. {conclusion} {conditional}.',
                    '{Negated_p} or {q}. {conclusion}, {conditional}.',
                    'Since either {negated_p} or {q}, {conclusion} {conditional}.'
                ]
                templates['conclusion_first'] = [
                    '{Conditional} because either {negated_p} or {q}.',
                    '{Conditional}, since {negated_p} or {q}.',
                    '{Conditional}. This follows from either {negated_p} or {q}.'
                ]
            else:  # Invalid Material Conditional Introduction
                templates['premise_first'] = [
                    'Either {negated_p} or {q}. {conclusion} if {p}, then both {q} and {r}.',
                    '{Negated_p} or {q}. {conclusion}, if {p} then {q} and {r}.',
                    'Since either {negated_p} or {q}, {conclusion} {p} implies both {q} and {r}.'
                ]
                templates['conclusion_first'] = [
                    'If {p}, then both {q} and {r} because either {negated_p} or {q}.',
                    'If {p} then {q} and {r}, since {negated_p} or {q}.',
                    '{P} implies both {q} and {r}. This follows from either {negated_p} or {q}.'
                ]
        
        elif rule_name == "Constructive Dilemma":
            if is_valid:
                templates['premise_first'] = [
                    '{Conditional1}. {Conditional2}. {Disjunction}. {conclusion} either {p} or {q} leads to {r}.',
                    'If {p}, then {r}. If {q}, then {r}. Either {p} or {q}. {conclusion}, {r}.',
                    '{Conditional1} and {conditional2}. Since {disjunction}, {conclusion} {r}.'
                ]
                templates['conclusion_first'] = [
                    '{R} because {disjunction}. Given {conditional1} and {conditional2}.',
                    '{R}, since {disjunction}. We know {conditional1} and {conditional2}.',
                    '{R}. This follows from {disjunction} and the conditionals {conditional1} and {conditional2}.'
                ]
            else:  # False Dilemma
                templates['premise_first'] = [
                    'Either {p} or {q}. {conclusion} one of these must be true.',
                    '{p} or {q}. {conclusion}, these are the only options.',
                    'Since either {p} or {q}, {conclusion} no other possibility exists.'
                ]
                templates['conclusion_first'] = [
                    'One of these must be true because either {p} or {q}.',
                    'These are the only options, since {p} or {q}.',
                    'No other possibility exists. Either {p} or {q} covers all cases.'
                ]
        
        elif rule_name == "Destructive Dilemma":
            if is_valid:
                templates['premise_first'] = [
                    '{Conditional1}. {Conditional2}. Either {negated_result1} or {negated_result2}. {conclusion} either {negated_p} or {negated_q}.',
                    'If {p}, then {r}. If {q}, then {r}. Either {negated_result1} or {negated_result2}. {conclusion}, either {negated_p} or {negated_q}.',
                    '{Conditional1} and {conditional2}. Since either {negated_result1} or {negated_result2}, {conclusion} either {negated_p} or {negated_q}.'
                ]
                templates['conclusion_first'] = [
                    'Either {negated_p} or {negated_q} because either {negated_result1} or {negated_result2}. Given {conditional1} and {conditional2}.',
                    'Either {negated_p} or {negated_q}, since either {negated_result1} or {negated_result2}. We know {conditional1} and {conditional2}.',
                    'Either {negated_p} or {negated_q}. This follows from either {negated_result1} or {negated_result2} and the conditionals {conditional1} and {conditional2}.'
                ]
            else:  # Non Sequitur
                templates['premise_first'] = [
                    '{P}. {conclusion} {q}.',
                    'Since {p}, {conclusion} {q}.',
                    '{P}. {conclusion}, {q}.'
                ]
                templates['conclusion_first'] = [
                    '{Q} because {p}.',
                    '{Q}, since {p}.',
                    '{Q}. This somehow follows from {p}.'
                ]
        
        return templates
    
    def create_conditional(self, p: str, q: str, style: str = "basic") -> str:
        """Create a conditional statement."""
        pattern = random.choice(self.conditional_patterns.get(style, self.conditional_patterns['basic']))
        # Clean up the inputs - remove punctuation and extra spaces
        p_clean = p.strip().rstrip('.!?')
        q_clean = q.strip().rstrip('.!?')
        
        # Handle capitalization based on conditional pattern
        if pattern.startswith('If {p}'):
            # For "If P, then Q" patterns, P should be lowercase (not sentence start)
            if p_clean and p_clean[0].isupper() and not self._is_proper_noun(p_clean):
                p_clean = p_clean[0].lower() + p_clean[1:]
            # Q should also be lowercase in "then Q" context
            if q_clean and q_clean[0].isupper() and not self._is_proper_noun(q_clean):
                q_clean = q_clean[0].lower() + q_clean[1:]
        elif pattern.startswith('{q} if {p}'):
            # For "Q if P" patterns, P should be lowercase  
            if p_clean and p_clean[0].isupper() and not self._is_proper_noun(p_clean):
                p_clean = p_clean[0].lower() + p_clean[1:]
        elif pattern.startswith('Given {p}') or 'Given {p}' in pattern:
            # For "Given P, Q" patterns, P should be lowercase
            if p_clean and p_clean[0].isupper() and not self._is_proper_noun(p_clean):
                p_clean = p_clean[0].lower() + p_clean[1:]
        elif pattern.startswith('Given {q}') or 'Given {q}' in pattern:
            # For "Given Q, ..." patterns, Q should be lowercase  
            if q_clean and q_clean[0].isupper() and not self._is_proper_noun(q_clean):
                q_clean = q_clean[0].lower() + q_clean[1:]
        
        return pattern.format(p=p_clean, q=q_clean)
    
    def _is_proper_noun(self, text: str) -> bool:
        """Check if text starts with a proper noun that should remain capitalized."""
        # Simple heuristic: common proper nouns or words that should stay capitalized
        proper_indicators = ['I ', 'I\'', 'Mr.', 'Mrs.', 'Dr.', 'Monday', 'Tuesday', 'Wednesday', 
                           'Thursday', 'Friday', 'Saturday', 'Sunday', 'January', 'February', 
                           'March', 'April', 'May', 'June', 'July', 'August', 'September', 
                           'October', 'November', 'December']
        return any(text.startswith(indicator) for indicator in proper_indicators)
    
    def create_conjunction(self, p: str, q: str, style: str = "basic") -> str:
        """Create a conjunction statement."""
        pattern = random.choice(self.conjunction_patterns.get(style, self.conjunction_patterns['basic']))
        # Clean up the inputs - remove punctuation and extra spaces  
        p_clean = p.strip().rstrip('.!?')
        q_clean = q.strip().rstrip('.!?')
        
        # Handle capitalization context for conjunctions  
        if pattern.startswith('{p} and {q}') or pattern.startswith('{p}, and {q}'):
            # For "p and q" patterns, q should be lowercase (not sentence start)
            if q_clean and q_clean[0].isupper() and not self._is_proper_noun(q_clean):
                q_clean = q_clean[0].lower() + q_clean[1:]
        elif pattern.startswith('Both {p} and {q}'):
            # For "Both p and q" patterns, both should be lowercase
            if p_clean and p_clean[0].isupper() and not self._is_proper_noun(p_clean):
                p_clean = p_clean[0].lower() + p_clean[1:]
            if q_clean and q_clean[0].isupper() and not self._is_proper_noun(q_clean):
                q_clean = q_clean[0].lower() + q_clean[1:]
        elif pattern.startswith('{p} as well as {q}') or pattern.startswith('{p} together with {q}') or pattern.startswith('{p} in conjunction with {q}'):
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
        if pattern.startswith('{p} or {q}'):
            # For "p or q" patterns, q should be lowercase (not sentence start)
            if q_clean and q_clean[0].isupper() and not self._is_proper_noun(q_clean):
                q_clean = q_clean[0].lower() + q_clean[1:]
        elif pattern.startswith('Either {p} or {q}'):
            # For "Either p or q" patterns, both should be lowercase
            if p_clean and p_clean[0].isupper() and not self._is_proper_noun(p_clean):
                p_clean = p_clean[0].lower() + p_clean[1:]
            if q_clean and q_clean[0].isupper() and not self._is_proper_noun(q_clean):
                q_clean = q_clean[0].lower() + q_clean[1:]
        
        return pattern.format(p=p_clean, q=q_clean)
    
    def get_conclusion_marker(self, style: str = "basic") -> str:
        """Get a random conclusion marker."""
        return random.choice(self.conclusion_markers.get(style, self.conclusion_markers['basic']))