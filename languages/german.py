"""
languages/german.py

German language implementation for the argument generator.
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


class GermanPattern(LanguageSpecificPattern):
    """German-specific linguistic patterns."""
    
    def __init__(self):
        super().__init__("de")
    
    def _init_negation_patterns(self) -> Dict[str, List[str]]:
        """Initialize German negation patterns."""
        return {
            "simple": [
                "es ist nicht der Fall, dass {sentence}",
                "{sentence} ist nicht wahr",
                "{sentence} trifft nicht zu",
                "{sentence} ist falsch",
                "nicht {sentence}"
            ],
            "formal": [
                "es ist falsch, dass {sentence}",
                "es trifft nicht zu, dass {sentence}",
                "die Aussage, dass {sentence}, ist falsch",
                "es ist unzutreffend, dass {sentence}",
                "die Behauptung, dass {sentence}, ist unrichtig"
            ],
            "emphatic": [
                "{sentence} ist definitiv falsch",
                "{sentence} ist keinesfalls der Fall",
                "{sentence} ist absolut falsch",
                "{sentence} ist zweifellos falsch",
                "auf keinen Fall {sentence}",
                "unter keinen Umständen {sentence}"
            ],
            "double": [
                "es ist nicht falsch, dass {sentence}",
                "es ist nicht unwahr, dass {sentence}",
                "man kann nicht leugnen, dass {sentence}",
                "es lässt sich nicht bestreiten, dass {sentence}"
            ],
            "colloquial": [
                "{sentence} stimmt nicht",
                "{sentence} ist Quatsch",
                "vergiss es, dass {sentence}",
                "{sentence} kannst du vergessen",
                "von wegen {sentence}"
            ],
            "semantic": [
                "das Gegenteil von {sentence} ist wahr",
                "{sentence} trifft nicht zu",
                "die Negation von {sentence} gilt",
                "es besteht eine Abwesenheit von {sentence}",
                "{sentence} liegt nicht vor"
            ],
            "philosophical": [
                "der Wahrheitswert von {sentence} ist falsch",
                "{sentence} entbehrt der Wahrheit",
                "die Proposition {sentence} korrespondiert nicht mit der Realität",
                "{sentence} hat keinen Wahrheitswert",
                "es gibt keinen Sachverhalt, in dem {sentence}"
            ],
            "academic": [
                "die These, dass {sentence}, ist zu verwerfen",
                "{sentence} kann nicht aufrechterhalten werden",
                "die Annahme, dass {sentence}, ist unhaltbar",
                "{sentence} lässt sich nicht verifizieren"
            ]
        }
    
    def _init_conjunction_patterns(self) -> Dict[str, List[str]]:
        """Initialize German conjunction patterns."""
        return {
            "simple": [
                "{p} und {q}",
                "{p}, und {q}",
                "sowohl {p} als auch {q}",
                "{p} sowie {q}",
                "{p} und gleichermaßen {q}"
            ],
            "sequential": [
                "{p}, und auch {q}",
                "{p}, außerdem {q}",
                "{p}, des Weiteren {q}",
                "{p}, überdies {q}",
                "{p}, ferner {q}"
            ],
            "emphatic": [
                "sowohl {p} als auch {q}",
                "nicht nur {p}, sondern auch {q}",
                "{p} und gleichermaßen {q}",
                "{p} zusammen mit {q}",
                "{p} in Verbindung mit {q}"
            ],
            "formal": [
                "{p} in Konjunktion mit {q}",
                "{p} konjugiert mit {q}",
                "die Konjunktion von {p} und {q}",
                "{p} bei gleichzeitigem {q}",
                "{p} nebst {q}"
            ],
            "causal": [
                "{p}, und folglich {q}",
                "{p}, und infolgedessen {q}",
                "{p}, was zu {q} führt",
                "{p}, dadurch {q}",
                "{p}, somit auch {q}"
            ],
            "temporal": [
                "{p}, und dann {q}",
                "{p}, anschließend {q}",
                "{p}, und nachfolgend {q}",
                "{p}, danach {q}",
                "erst {p}, dann {q}"
            ],
            "additive": [
                "nicht nur {p}, sondern auch {q}",
                "{p}, und darüber hinaus {q}",
                "{p}, und zusätzlich {q}",
                "{p}, und obendrein {q}",
                "{p}, zudem {q}"
            ],
            "logical": [
                "{p} ∧ {q}",
                "({p}) UND ({q})",
                "{p} & {q}",
                "die logische Konjunktion von {p} und {q}",
                "sowohl {p} als auch {q} sind wahr"
            ]
        }
    
    def _init_disjunction_patterns(self) -> Dict[str, List[str]]:
        """Initialize German disjunction patterns."""
        return {
            "inclusive": [
                "{p} oder {q}",
                "{p}, oder {q}",
                "entweder {p} oder {q} oder beides",
                "{p} und/oder {q}",
                "{p} beziehungsweise {q}"
            ],
            "exclusive": [
                "entweder {p} oder {q}, aber nicht beides",
                "genau eines von {p} oder {q}",
                "{p} oder {q}, aber nicht beide",
                "entweder {p} oder {q} (exklusiv)",
                "nur eines: {p} oder {q}"
            ],
            "alternative": [
                "{p}, alternativ {q}",
                "{p}, andernfalls {q}",
                "{p}, sonst {q}",
                "{p}, oder stattdessen {q}",
                "{p}, ansonsten {q}"
            ],
            "formal": [
                "{p} oder aber {q}",
                "die Disjunktion von {p} und {q}",
                "{p} vel {q}",
                "mindestens eines von {p} oder {q}",
                "entweder {p} oder möglicherweise {q}"
            ],
            "conditional": [
                "{p}, es sei denn {q}",
                "{p} außer wenn {q}",
                "{p} wenn nicht {q}",
                "{p} ausgenommen {q}",
                "{p} sofern nicht {q}"
            ],
            "preferential": [
                "{p}, oder andernfalls {q}",
                "vorzugsweise {p}, ansonsten {q}",
                "{p} wenn möglich, sonst {q}",
                "idealerweise {p}, aber {q} genügt",
                "erste Wahl {p}, zweite Wahl {q}"
            ],
            "exhaustive": [
                "es ist entweder {p} oder es ist {q}",
                "eine von zwei Möglichkeiten: {p} oder {q}",
                "die Optionen sind {p} oder {q}",
                "wir haben {p} oder wir haben {q}",
                "die Wahl besteht zwischen {p} und {q}"
            ],
            "logical": [
                "{p} ∨ {q}",
                "({p}) ODER ({q})",
                "{p} | {q}",
                "die logische Disjunktion von {p} und {q}",
                "{p} ODER {q} ist wahr"
            ]
        }
    
    def _init_conditional_patterns(self) -> Dict[str, List[str]]:
        """Initialize German conditional patterns."""
        return {
            "standard": [
                "wenn {antecedent}, dann {consequent}",
                "falls {antecedent}, dann {consequent}",
                "{consequent}, wenn {antecedent}",
                "gegeben {antecedent}, folgt {consequent}",
                "sofern {antecedent}, {consequent}"
            ],
            "temporal": [
                "wenn {antecedent}, dann {consequent}",
                "sobald {antecedent}, {consequent}",
                "sowie {antecedent}, {consequent}",
                "nachdem {antecedent}, {consequent}",
                "immer wenn {antecedent}, {consequent}"
            ],
            "causal": [
                "weil {antecedent}, {consequent}",
                "{antecedent} verursacht {consequent}",
                "{antecedent} führt zu {consequent}",
                "{antecedent} bewirkt {consequent}",
                "{antecedent} hat {consequent} zur Folge"
            ],
            "hypothetical": [
                "angenommen {antecedent}, dann {consequent}",
                "vorausgesetzt {antecedent}, {consequent}",
                "unter der Bedingung, dass {antecedent}, {consequent}",
                "für den Fall, dass {antecedent}, {consequent}",
                "gesetzt den Fall {antecedent}, {consequent}"
            ],
            "necessity": [
                "{consequent} ist notwendig für {antecedent}",
                "{antecedent} erfordert {consequent}",
                "ohne {consequent} kein {antecedent}",
                "{antecedent} nur wenn {consequent}",
                "für {antecedent} ist {consequent} erforderlich"
            ],
            "sufficiency": [
                "{antecedent} ist hinreichend für {consequent}",
                "{antecedent} garantiert {consequent}",
                "{antecedent} gewährleistet {consequent}",
                "{antecedent} impliziert {consequent}",
                "{antecedent} zieht {consequent} nach sich"
            ],
            "biconditional_hint": [
                "{antecedent} genau dann, wenn {consequent}",
                "{antecedent} dann und nur dann, wenn {consequent}",
                "{antecedent} äquivalent zu {consequent}",
                "{antecedent} gdw. {consequent}",
                "{antecedent} ⟺ {consequent}"
            ],
            "probabilistic": [
                "wenn {antecedent}, dann wahrscheinlich {consequent}",
                "wenn {antecedent}, dann vermutlich {consequent}",
                "{antecedent} legt {consequent} nahe",
                "{antecedent} deutet auf {consequent} hin",
                "bei {antecedent} ist {consequent} wahrscheinlich"
            ],
            "colloquial": [
                "{antecedent} heißt {consequent}",
                "aus {antecedent} folgt {consequent}",
                "{antecedent} bringt {consequent}",
                "mit {antecedent} kommt {consequent}",
                "wo {antecedent} ist, da ist {consequent}"
            ],
        }
    
    def _init_connectives(self) -> Dict[str, List[str]]:
        """Initialize German logical connectives."""
        return {
            "conclusion": [
                "daher", "also", "folglich", "somit",
                "demnach", "infolgedessen", "daraus folgt", "es ergibt sich",
                "wir können schließen", "das bedeutet", "ergo",
                "hieraus ersehen wir", "was zeigt, dass", "mithin"
            ],
            "premise": [
                "da", "weil", "denn", "zumal",
                "angesichts dessen, dass", "in Anbetracht", "aufgrund",
                "wegen", "nämlich", "schließlich"
            ],
            "assumption": [
                "angenommen", "nehmen wir an", "gesetzt", "unterstellen wir",
                "betrachten wir", "postulieren wir", "sei", "vorausgesetzt",
                "hypothetisch", "zum Zwecke der Argumentation"
            ],
            "contrast": [
                "aber", "jedoch", "allerdings", "dennoch",
                "trotzdem", "gleichwohl", "obwohl", "wenngleich",
                "ungeachtet", "im Gegenteil", "hingegen", "indes"
            ],
            "addition": [
                "und", "auch", "außerdem", "zudem",
                "zusätzlich", "ferner", "überdies", "sowie",
                "gleichermaßen", "des Weiteren", "obendrein"
            ],
            "emphasis": [
                "tatsächlich", "in der Tat", "zweifellos",
                "sicherlich", "gewiss", "fraglos", "unbestreitbar",
                "offensichtlich", "eindeutig", "nachweislich"
            ]
        }
    
    def format_sentence(self, sentence: str, formatting_type: str) -> str:
        """Apply German-specific formatting."""
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
        """Normalize a German sentence."""
        # Remove trailing punctuation
        sentence = sentence.rstrip('.!?;:,')
        
        # DON'T convert to lowercase - German nouns are capitalized
        # Just normalize spacing
        sentence = ' '.join(sentence.split())
        
        return sentence
    
    def capitalize_sentence(self, sentence: str) -> str:
        """Capitalize a German sentence properly."""
        if not sentence:
            return sentence
        
        # German capitalizes all nouns, not just sentence start
        # For simplicity, capitalize first letter
        return sentence[0].upper() + sentence[1:]
    
    def _simple_negate(self, sentence: str) -> str:
        """Apply simple negation to a German sentence."""
        # German negation patterns
        if " ist " in sentence:
            return sentence.replace(" ist ", " ist nicht ", 1)
        elif " sind " in sentence:
            return sentence.replace(" sind ", " sind nicht ", 1)
        elif " hat " in sentence:
            return sentence.replace(" hat ", " hat nicht ", 1)
        elif " haben " in sentence:
            return sentence.replace(" haben ", " haben nicht ", 1)
        else:
            return f"es ist nicht der Fall, dass {sentence}"
    
    def _make_question(self, sentence: str) -> str:
        """Convert a statement to a question in German."""
        # German uses verb-first for questions
        words = sentence.split()
        if len(words) >= 2:
            # Simple verb inversion
            return f"{words[1]} {words[0]} " + " ".join(words[2:]) + "?"
        else:
            return f"Ist es wahr, dass {sentence}?"
    
    def _emphasize(self, sentence: str) -> str:
        """Add emphasis to a German sentence."""
        emphatics = ["zweifellos", "sicherlich", "gewiss"]
        import random
        return f"{random.choice(emphatics)} {sentence}"


class GermanTemplates(LanguageTemplates):
    """German-specific argument templates."""
    
    def __init__(self, language_pattern: GermanPattern):
        super().__init__(language_pattern)
    
    def _init_templates(self) -> Dict[str, Dict[str, List[EnhancedTemplate]]]:
        """Initialize German templates - all 11 logical rules."""
        templates = {}
        
        # Basic Inference Rules
        templates["Modus Ponens"] = {
            "valid": self._create_modus_ponens_valid(),
            "invalid": self._create_simple_invalid("Wenn {p}, dann {q}. {Q}. Also {p}.")
        }
        
        templates["Modus Tollens"] = {
            "valid": self._create_modus_tollens_valid(),
            "invalid": self._create_simple_invalid("Wenn {p}, dann {q}. Nicht {P}. Also nicht {q}.")
        }
        
        templates["Disjunctive Syllogism"] = {
            "valid": self._create_disjunctive_syllogism_valid(),
            "invalid": self._create_simple_invalid("{P} oder {q}. {P}. Also nicht {q}.")
        }
        
        # Conjunction Rules
        templates["Conjunction Introduction"] = {
            "valid": self._create_simple_valid("{P}. {Q}. Also {p} und {q}."),
            "invalid": self._create_simple_invalid("{P}. Also {p} und {q}.")
        }
        
        templates["Conjunction Elimination"] = {
            "valid": self._create_simple_valid("{P} und {q}. Also {p}."),
            "invalid": self._create_simple_invalid("{P} hat die Eigenschaft {q}. Also die Gesamtheit von {p} hat die Eigenschaft {q}.")
        }
        
        # Disjunction Rules
        templates["Disjunction Introduction"] = {
            "valid": self._create_simple_valid("{P}. Also {p} oder {q}."),
            "invalid": self._create_simple_invalid("{P}. Also entweder {p} oder {q} (nur).")
        }
        
        templates["Disjunction Elimination"] = {
            "valid": self._create_simple_valid("{P} oder {q}. Wenn {p}, dann {r}. Wenn {q}, dann {r}. Also {r}."),
            "invalid": self._create_simple_invalid("{P} oder {q}. {P} impliziert {r}. Also {r}.")
        }
        
        # Complex Rules
        templates["Hypothetical Syllogism"] = {
            "valid": self._create_hypothetical_syllogism_valid(),
            "invalid": self._create_simple_invalid("{P}. Also {q}.")
        }
        
        templates["Material Conditional Introduction"] = {
            "valid": self._create_simple_valid("{P} impliziert {q}. {Q} impliziert {r}. Also wenn {p}, dann {r}."),
            "invalid": self._create_simple_invalid("{P}. Also {q}.")
        }
        
        templates["Constructive Dilemma"] = {
            "valid": self._create_simple_valid("{p} impliziert {q}. {r} impliziert {s}. {P} oder {r}. Also {q} oder {s}."),
            "invalid": self._create_simple_invalid("{P}. Also entweder {p} oder {q} (keine anderen Optionen).")
        }
        
        templates["Destructive Dilemma"] = {
            "valid": self._create_simple_valid("Wenn {p}, dann {q}. Wenn {r}, dann {s}. Nicht {q} oder nicht {s}. Also nicht {p} oder nicht {r}."),
            "invalid": self._create_simple_invalid("{P}. Also {q}.")
        }
        
        # Invalid forms (fallacies) 
        templates["Affirming the Consequent"] = {
            "invalid": self._create_simple_invalid("Wenn {p}, dann {q}. {Q}. Also {p}.")
        }
        
        templates["Denying the Antecedent"] = {
            "invalid": self._create_simple_invalid("Wenn {p}, dann {q}. Nicht {P}. Also nicht {q}.")
        }
        
        templates["Affirming a Disjunct"] = {
            "invalid": self._create_simple_invalid("{P} oder {q}. {P}. Also nicht {q}.")
        }
        
        templates["False Conjunction"] = {
            "invalid": self._create_simple_invalid("{P}. Also {p} und {q}.")
        }
        
        templates["Composition Fallacy"] = {
            "invalid": self._create_simple_invalid("{P} hat die Eigenschaft {q}. Also die Gesamtheit von {p} hat die Eigenschaft {q}.")
        }
        
        templates["Invalid Conjunction Introduction"] = {
            "invalid": self._create_invalid_conjunction_introduction()
        }
        
        templates["False Dilemma"] = {
            "invalid": self._create_simple_invalid("{P}. Also entweder {p} oder {q} (nur).")
        }
        
        templates["Invalid Disjunction Elimination"] = {
            "invalid": self._create_simple_invalid("{P} oder {q}. {P} impliziert {r}. Also {r}.")
        }
        
        templates["Non Sequitur"] = {
            "invalid": self._create_simple_invalid("{P}. Also {q}.")
        }
        
        return templates
    
    def _create_simple_valid(self, template_text: str) -> List[EnhancedTemplate]:
        """Create a simple valid template from text."""
        builder = TemplateBuilder()
        builder.add_static(template_text)
        return [builder.build()]
    
    def _create_simple_invalid(self, template_text: str) -> List[EnhancedTemplate]:
        """Create a simple invalid template from text."""
        builder = TemplateBuilder()
        builder.add_static(template_text)
        return [builder.build()]
    
    def _create_modus_ponens_valid(self) -> List[EnhancedTemplate]:
        """Create valid Modus Ponens templates in German."""
        templates = []
        
        # Basic with verb-final in subordinate clause
        builder = TemplateBuilder()
        builder.add_static('Wenn ')
        builder.add_variable('p')
        builder.add_static(', dann ')
        builder.add_variable('q')
        builder.add_static('. ')
        builder.add_variable('P')
        builder.add_static('. Also ')
        builder.add_variable('q')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        # Intermediate with variations
        builder2 = TemplateBuilder()
        builder2.add_variation('conditional', [
            'Wenn {p}, dann {q}',
            'Falls {p}, dann {q}',
            'Sofern {p}, {q}',
            '{p} impliziert {q}',
            'Gegeben {p}, folgt {q}'
        ])
        builder2.add_static('. ')
        builder2.add_variation('now', [
            'Nun',
            'Es ist der Fall, dass',
            'Wir wissen, dass',
            'Es gilt'
        ])
        builder2.add_static(' ')
        builder2.add_variable('p')
        builder2.add_static('. ')
        builder2.add_variation('conclusion', [
            'Daher',
            'Also',
            'Folglich',
            'Somit',
            'Daraus ergibt sich'
        ])
        builder2.add_static(' ')
        builder2.add_variable('q')
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        templates.append(builder2.build())
        
        # Advanced - philosophical style
        builder3 = TemplateBuilder()
        builder3.add_variable('Q')
        builder3.add_static(', ')
        builder3.add_variation('because', [
            'denn',
            'weil',
            'da',
            'zumal'
        ])
        builder3.add_static(' ')
        builder3.add_variable('p')
        builder3.add_static('. ')
        builder3.add_variation('note', [
            'Beachte, dass',
            'Es ist etabliert, dass',
            'Wir wissen, dass',
            'Es gilt nämlich'
        ])
        builder3.add_static(' ')
        builder3.add_variation('conditional', [
            'wenn {p}, dann {q}',
            '{p} zieht {q} nach sich',
            'aus {p} folgt notwendig {q}',
            '{p} bedingt {q}'
        ])
        builder3.add_static('.')
        builder3.set_metadata('complexity', ComplexityLevel.ADVANCED)
        templates.append(builder3.build())
        
        # Expert - formal logic style
        builder4 = TemplateBuilder()
        builder4.add_static('Aus der ')
        builder4.add_variation('premise_type', [
            'Prämisse',
            'Bedingung',
            'Annahme'
        ])
        builder4.add_static(' „')
        builder4.add_variable('p')
        builder4.add_static(' → ')
        builder4.add_variable('q')
        builder4.add_static('" und der ')
        builder4.add_variation('fact', [
            'Tatsache',
            'Feststellung',
            'Gegebenheit'
        ])
        builder4.add_static(' „')
        builder4.add_variable('p')
        builder4.add_static('" ')
        builder4.add_variation('follows', [
            'folgt logisch',
            'ergibt sich zwingend',
            'leitet sich ab'
        ])
        builder4.add_static(' „')
        builder4.add_variable('q')
        builder4.add_static('".')
        builder4.set_metadata('complexity', ComplexityLevel.EXPERT)
        builder4.set_metadata('style', 'formal-logic')
        templates.append(builder4.build())
        
        return templates
    
    def _create_modus_tollens_valid(self) -> List[EnhancedTemplate]:
        """Create valid Modus Tollens templates in German."""
        templates = []
        
        # Basic
        builder = TemplateBuilder()
        builder.add_static('Wenn ')
        builder.add_variable('p')
        builder.add_static(', dann ')
        builder.add_variable('q')
        builder.add_static('. ')
        builder.add_variable('not_Q')
        builder.add_static('. Also ')
        builder.add_variable('not_p')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        # Intermediate with necessity
        builder2 = TemplateBuilder()
        builder2.add_variation('conditional', [
            'Wenn {p}, dann {q}',
            '{q} ist notwendig für {p}',
            '{p} erfordert {q}',
            'Ohne {q} kein {p}',
            '{p} setzt {q} voraus'
        ])
        builder2.add_static('. ')
        builder2.add_variation('but', [
            'Aber',
            'Jedoch',
            'Allerdings',
            'Nun ist es so, dass'
        ])
        builder2.add_static(' ')
        builder2.add_variable('not_q')
        builder2.add_static('. ')
        builder2.add_variation('therefore', [
            'Daher',
            'Folglich',
            'Somit',
            'Daraus folgt, dass'
        ])
        builder2.add_static(' ')
        builder2.add_variable('not_p')
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        templates.append(builder2.build())
        
        return templates
    
    def _create_disjunctive_syllogism_valid(self) -> List[EnhancedTemplate]:
        """Create valid Disjunctive Syllogism templates in German."""
        templates = []
        
        # Basic
        builder = TemplateBuilder()
        builder.add_static('Entweder ')
        builder.add_variable('p')
        builder.add_static(' oder ')
        builder.add_variable('q')
        builder.add_static('. ')
        builder.add_variable('not_P')
        builder.add_static('. Also ')
        builder.add_variable('q')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        # Intermediate
        builder2 = TemplateBuilder()
        builder2.add_variation('disjunction', [
            'Entweder {p} oder {q}',
            'Es gilt entweder {p} oder {q}',
            'Wir haben entweder {p} oder {q}',
            'Die Optionen sind {p} oder {q}'
        ])
        builder2.add_static('. ')
        builder2.add_variation('negation', [
            '{not_P}',
            'Nun {not_p}',
            'Aber {not_p}',
            'Es zeigt sich, dass {not_p}'
        ])
        builder2.add_static('. ')
        builder2.add_variation('conclusion', [
            'Daher',
            'Also',
            'Folglich',
            'Somit muss gelten'
        ])
        builder2.add_static(' ')
        builder2.add_variable('q')
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        templates.append(builder2.build())
        
        return templates
    
    def _create_hypothetical_syllogism_valid(self) -> List[EnhancedTemplate]:
        """Create valid Hypothetical Syllogism templates in German."""
        templates = []
        
        # Basic
        builder = TemplateBuilder()
        builder.add_static('Wenn ')
        builder.add_variable('p')
        builder.add_static(', dann ')
        builder.add_variable('q')
        builder.add_static('. Wenn ')
        builder.add_variable('q')
        builder.add_static(', dann ')
        builder.add_variable('r')
        builder.add_static('. Also: wenn ')
        builder.add_variable('p')
        builder.add_static(', dann ')
        builder.add_variable('r')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        # Advanced - causal chain
        builder2 = TemplateBuilder()
        builder2.add_variation('given', [
            'Da',
            'Weil',
            'Angesichts der Tatsache, dass'
        ])
        builder2.add_static(' ')
        builder2.add_variable('p')
        builder2.add_static(' ')
        builder2.add_variation('leads1', [
            'zu',
            'führt zu',
            'bewirkt',
            'verursacht'
        ])
        builder2.add_static(' ')
        builder2.add_variable('q')
        builder2.add_static(' ')
        builder2.add_variation('and', [
            'führt',
            'und dies',
            ', welches'
        ])
        builder2.add_static(' ')
        builder2.add_variation('leads2', [
            'wiederum zu',
            'seinerseits',
            'folglich zu'
        ])
        builder2.add_static(' ')
        builder2.add_variable('r')
        builder2.add_static(' ')
        builder2.add_variation('leads_final', [
            'führt',
            ', führt'
        ])
        builder2.add_static(', ')
        builder2.add_variation('conclude', [
            'können wir schließen, dass',
            'folgt daraus, dass',
            'ergibt sich, dass'
        ])
        builder2.add_static(' ')
        builder2.add_variable('p')
        builder2.add_static(' ')
        builder2.add_variation('ultimately', [
            'letztendlich',
            'schlussendlich',
            'am Ende'
        ])
        builder2.add_static(' ')
        builder2.add_variable('r')
        builder2.add_static(' ')
        builder2.add_variation('causes', [
            'bewirkt',
            'zur Folge hat',
            'herbeiführt'
        ])
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.ADVANCED)
        templates.append(builder2.build())
        
        return templates
    
    def _create_affirming_consequent(self) -> List[EnhancedTemplate]:
        """Create Affirming the Consequent templates in German."""
        templates = []
        
        # Basic invalid form
        builder = TemplateBuilder()
        builder.add_static('Wenn ')
        builder.add_variable('p')
        builder.add_static(', dann ')
        builder.add_variable('q')
        builder.add_static('. ')
        builder.add_variable('Q')
        builder.add_static('. Also ')
        builder.add_variable('p')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        return templates
    
    def _create_denying_antecedent(self) -> List[EnhancedTemplate]:
        """Create Denying the Antecedent templates in German."""
        templates = []
        
        # Basic invalid form
        builder = TemplateBuilder()
        builder.add_static('Wenn ')
        builder.add_variable('p')
        builder.add_static(', dann ')
        builder.add_variable('q')
        builder.add_static('. ')
        builder.add_variable('not_P')
        builder.add_static('. Also ')
        builder.add_variable('not_q')
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        return templates
    
    def _create_invalid_conjunction_introduction(self) -> List[EnhancedTemplate]:
        """Create Invalid Conjunction Introduction templates (A / Therefore, A and B) in German."""
        templates = []
        
        # Basic invalid conjunction introduction
        builder = TemplateBuilder()
        builder.add_variable('P')
        builder.add_static('. ')
        builder.add_variation('conclusion', [
            'Also',
            'Daher',
            'Folglich',
            'Somit'
        ])
        builder.add_static(', ')
        builder.add_variation('conjunction', [
            '{p} und {q}',
            'sowohl {p} als auch {q}',
            '{p} sowie {q}'
        ])
        builder.add_static('.')
        builder.set_metadata('complexity', ComplexityLevel.BASIC)
        templates.append(builder.build())
        
        # Intermediate version with more sophisticated language
        builder2 = TemplateBuilder()
        builder2.add_variable('P')
        builder2.add_static('. ')
        builder2.add_variation('conclusion', [
            'Daraus folgt, dass',
            'Wir können schließen, dass',
            'Das bedeutet, dass'
        ])
        builder2.add_static(' ')
        builder2.add_variation('conjunction', [
            'nicht nur {p}, sondern auch {q}',
            '{p} und außerdem {q}',
            '{p} zusammen mit {q}'
        ])
        builder2.add_static('.')
        builder2.set_metadata('complexity', ComplexityLevel.INTERMEDIATE)
        templates.append(builder2.build())
        
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
            "Destructive Dilemma": 4,
            # Invalid forms (fallacies)
            "Affirming the Consequent": 2,
            "Denying the Antecedent": 2,
            "Affirming a Disjunct": 2,
            "False Conjunction": 2,
            "Composition Fallacy": 2,
            "Invalid Conjunction Introduction": 2,
            "False Dilemma": 2,
            "Invalid Disjunction Elimination": 3,
            "Non Sequitur": 2
        }
        return requirements.get(rule_name, 2)
    
    def get_template_variables(self, rule_name: str) -> Set[str]:
        """Get variables used in templates for a rule."""
        basic_vars = {'p', 'q', 'P', 'Q'}
        
        if rule_name in ["Modus Tollens", "Destructive Dilemma", "Denying the Antecedent"]:
            basic_vars.update({'not_p', 'not_q', 'not_P', 'not_Q'})
        
        if rule_name in ["Hypothetical Syllogism", "Material Conditional Introduction", "Constructive Dilemma"]:
            basic_vars.update({'r', 'R'})
        
        if rule_name in ["Disjunction Elimination", "Destructive Dilemma", "Invalid Disjunction Elimination"]:
            basic_vars.update({'s', 'S'})
        
        return basic_vars


class GermanGrammar(LanguageGrammar):
    """German grammar rules."""
    
    def __init__(self):
        super().__init__("de")
    
    def apply_agreement(self, subject: str, verb: str, 
                       object: Optional[str] = None) -> Tuple[str, str, Optional[str]]:
        """Apply German subject-verb agreement."""
        # German has complex agreement with case system
        # Simplified implementation
        
        # Check plurality
        plural_indicators = ['die', 'viele', 'einige', 'mehrere']
        is_plural = any(ind in subject.lower() for ind in plural_indicators)
        
        # Adjust verb for plural
        if is_plural:
            verb_mappings = {
                'ist': 'sind',
                'hat': 'haben',
                'macht': 'machen',
                'geht': 'gehen'
            }
            if verb in verb_mappings:
                verb = verb_mappings[verb]
        
        return subject, verb, object
    
    def apply_article_rules(self, noun: str, definite: bool = False) -> str:
        """Apply German article rules (gender and case)."""
        # Simplified - German has 3 genders and 4 cases
        # Using nominative case only
        
        # Guess gender based on endings
        if noun.endswith(('ung', 'heit', 'keit', 'schaft', 'ion', 'tät', 'ik')):
            # Likely feminine
            article = 'die' if definite else 'eine'
        elif noun.endswith(('er', 'ling', 'ismus', 'or')):
            # Likely masculine
            article = 'der' if definite else 'ein'
        elif noun.endswith(('chen', 'lein', 'ment', 'um')):
            # Likely neuter
            article = 'das' if definite else 'ein'
        else:
            # Default to masculine
            article = 'der' if definite else 'ein'
        
        return f"{article} {noun}"
    
    def apply_word_order(self, components: Dict[str, str]) -> str:
        """Apply German word order (V2 in main clauses)."""
        parts = []
        
        # German has V2 order in main clauses
        # Verb should be second element
        if 'time' in components:
            # Time-Verb-Subject-Object
            parts.append(components['time'])
            if 'verb' in components:
                parts.append(components['verb'])
            if 'subject' in components:
                parts.append(components['subject'])
        else:
            # Subject-Verb-Object (standard)
            if 'subject' in components:
                parts.append(components['subject'])
            if 'verb' in components:
                parts.append(components['verb'])
        
        if 'object' in components:
            parts.append(components['object'])
        
        # Add other components
        for key, value in components.items():
            if key not in ['subject', 'verb', 'object', 'time']:
                parts.append(value)
        
        return ' '.join(parts)
    
    def pluralize(self, word: str, count: int = 2) -> str:
        """Pluralize a German word."""
        if count == 1:
            return word
        
        # German pluralization is complex with umlauts
        # Simplified rules
        if word.endswith('e'):
            return word + 'n'
        elif word.endswith('er'):
            return word  # No change
        elif word.endswith(('el', 'en')):
            return word  # No change
        elif any(v in word for v in ['a', 'o', 'u']):
            # Might need umlaut - simplified
            return word + 'e'
        else:
            return word + 'en'
    
    def apply_case(self, word: str, case: str) -> str:
        """Apply German grammatical case."""
        # German has 4 cases: nominative, accusative, dative, genitive
        # This is highly simplified
        
        article_cases = {
            'der': {
                'nominative': 'der',
                'accusative': 'den',
                'dative': 'dem',
                'genitive': 'des'
            },
            'die': {
                'nominative': 'die',
                'accusative': 'die',
                'dative': 'der',
                'genitive': 'der'
            },
            'das': {
                'nominative': 'das',
                'accusative': 'das',
                'dative': 'dem',
                'genitive': 'des'
            }
        }
        
        # Handle articles
        for article, cases in article_cases.items():
            if word.startswith(article + ' '):
                new_article = cases.get(case, article)
                return word.replace(article, new_article, 1)
        
        return word


class GermanStyleGuide(LanguageStyleGuide):
    """German style guide."""
    
    def __init__(self):
        super().__init__("de")
    
    def _init_formality_levels(self) -> Dict[str, Dict[str, Any]]:
        """Initialize German formality levels."""
        return {
            "casual": {
                "pronouns": "du",
                "contractions": True,
                "particles": ["mal", "doch", "ja", "halt"],
                "sentence_starters": ["Na", "Also", "Tja", "Naja"],
                "connectives": ["und", "aber", "also", "weil"]
            },
            "neutral": {
                "pronouns": "Sie",
                "contractions": False,
                "particles": [],
                "sentence_starters": [],
                "connectives": ["und", "aber", "daher", "weil"]
            },
            "formal": {
                "pronouns": "Sie",
                "contractions": False,
                "particles": [],
                "sentence_starters": ["Des Weiteren", "Außerdem", "Zudem"],
                "connectives": ["sowie", "jedoch", "folglich", "aufgrund"]
            },
            "academic": {
                "pronouns": "man",  # Impersonal
                "contractions": False,
                "nominalization": True,
                "passive_voice": True,
                "sentence_starters": ["Es ist zu bemerken, dass", "Hieraus folgt"],
                "connectives": ["sowie", "indes", "mithin", "infolgedessen"]
            }
        }
    
    def apply_formality(self, text: str, formality_level: str) -> str:
        """Apply German formality transformations."""
        if formality_level not in self.formality_levels:
            return text
        
        rules = self.formality_levels[formality_level]
        
        # Apply pronoun changes
        if rules.get("pronouns") == "Sie":
            text = self._use_sie(text)
        elif rules.get("pronouns") == "man":
            text = self._use_man(text)
        
        # Add particles for casual
        if "particles" in rules and rules["particles"]:
            text = self._add_particles(text, rules["particles"])
        
        return text
    
    def get_domain_specific_style(self, domain: str) -> Dict[str, Any]:
        """Get domain-specific style preferences for German."""
        domain_styles = {
            "legal": {
                "precision": "high",
                "compound_words": True,
                "subjunctive": True,
                "formal_vocabulary": True,
                "avoid": ["vielleicht", "wahrscheinlich", "ungefähr"]
            },
            "scientific": {
                "precision": "high",
                "passive_voice": True,
                "nominalization": True,
                "technical_compounds": True,
                "anglicisms": True
            },
            "philosophical": {
                "abstract": True,
                "compound_concepts": True,
                "subjunctive_mood": True,
                "complex_sentences": True
            },
            "everyday": {
                "precision": "medium",
                "dialects": True,
                "particles": True,
                "ellipsis": True
            }
        }
        
        return domain_styles.get(domain, {})
    
    def apply_rhetorical_emphasis(self, text: str, emphasis_type: str) -> str:
        """Apply rhetorical emphasis in German."""
        emphasis_patterns = {
            "strong": lambda t: f"Es ist absolut gewiss, dass {t}",
            "subtle": lambda t: f"Es scheint, dass {t}",
            "questioning": lambda t: f"Ist es nicht so, dass {t}?",
            "dramatic": lambda t: f"Fürwahr, {t}!",
            "understated": lambda t: f"Man könnte sagen, dass {t}"
        }
        
        if emphasis_type in emphasis_patterns:
            return emphasis_patterns[emphasis_type](text)
        
        return text
    
    def _use_sie(self, text: str) -> str:
        """Convert to formal 'Sie' form."""
        replacements = {
            'du hast': 'Sie haben',
            'du bist': 'Sie sind',
            'du kannst': 'Sie können',
            'du musst': 'Sie müssen',
            'dein': 'Ihr',
            'deine': 'Ihre'
        }
        
        for informal, formal in replacements.items():
            text = text.replace(informal, formal)
        
        return text
    
    def _use_man(self, text: str) -> str:
        """Convert to impersonal 'man' form."""
        replacements = {
            'wir können': 'man kann',
            'wir sehen': 'man sieht',
            'wir wissen': 'man weiß',
            'wir schließen': 'man schließt'
        }
        
        for personal, impersonal in replacements.items():
            text = text.replace(personal, impersonal)
        
        return text
    
    def _add_particles(self, text: str, particles: List[str]) -> str:
        """Add modal particles for casual German."""
        import random
        # Add particle after verb or at strategic positions
        # Simplified implementation
        if random.random() < 0.3:
            particle = random.choice(particles)
            words = text.split()
            if len(words) > 2:
                words.insert(2, particle)
                text = ' '.join(words)
        
        return text


class GermanLanguageAdapter(LanguageAdapter):
    """Complete German language adapter."""
    
    def __init__(self):
        pattern = GermanPattern()
        templates = GermanTemplates(pattern)
        grammar = GermanGrammar()
        style_guide = GermanStyleGuide()
        
        super().__init__(pattern, templates, grammar, style_guide)


# Register the German adapter
from language_base import LanguageFactory
LanguageFactory.register_language("de", GermanLanguageAdapter)
