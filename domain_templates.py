"""
domain_templates.py

Domain-specific template generator for creating arguments tailored to
different fields and contexts (scientific, legal, everyday, academic, etc.)
"""

from typing import Dict, List, Optional, Any
from template_system import TemplateBuilder, EnhancedTemplate, TemplateBank
from linguistic_patterns import ComplexityLevel, VariationType
import random


class DomainTemplateGenerator:
    """Generates domain-specific templates for logical arguments."""
    
    def __init__(self):
        self.domains = {
            "scientific": self._create_scientific_templates,
            "legal": self._create_legal_templates,
            "everyday": self._create_everyday_templates,
            "academic": self._create_academic_templates,
            "philosophical": self._create_philosophical_templates,
            "mathematical": self._create_mathematical_templates,
            "business": self._create_business_templates,
            "medical": self._create_medical_templates
        }
        
        self.domain_characteristics = self._init_domain_characteristics()
    
    def _init_domain_characteristics(self) -> Dict[str, Dict[str, Any]]:
        """Initialize characteristics for each domain."""
        return {
            "scientific": {
                "formality": "high",
                "precision": "very_high",
                "passive_voice": True,
                "hedging": True,
                "technical_terms": True,
                "citation_style": True,
                "preferred_connectives": ["therefore", "thus", "consequently", "it follows that"],
                "preferred_conditionals": ["causal", "sufficiency", "necessity", "probabilistic"],
                "example_phrases": [
                    "experimental evidence suggests",
                    "data indicate",
                    "results demonstrate",
                    "findings support",
                    "hypothesis predicts"
                ]
            },
            "legal": {
                "formality": "very_high",
                "precision": "absolute",
                "passive_voice": False,
                "qualifiers": True,
                "technical_terms": True,
                "latin_terms": True,
                "preferred_connectives": ["therefore", "thus", "hence", "accordingly"],
                "preferred_conditionals": ["standard", "necessity", "conditional_precedent"],
                "example_phrases": [
                    "pursuant to",
                    "notwithstanding",
                    "whereas",
                    "in accordance with",
                    "subject to"
                ]
            },
            "everyday": {
                "formality": "low",
                "precision": "medium",
                "contractions": True,
                "colloquialisms": True,
                "simple_vocabulary": True,
                "preferred_connectives": ["so", "because", "and", "but"],
                "preferred_conditionals": ["standard", "temporal", "colloquial"],
                "example_phrases": [
                    "you know",
                    "I mean",
                    "the thing is",
                    "basically",
                    "sort of"
                ]
            },
            "academic": {
                "formality": "high",
                "precision": "high",
                "hedging": True,
                "citations": True,
                "complex_sentences": True,
                "preferred_connectives": ["therefore", "moreover", "furthermore", "consequently"],
                "preferred_conditionals": ["standard", "hypothetical", "sufficiency"],
                "example_phrases": [
                    "scholars argue",
                    "research suggests",
                    "literature indicates",
                    "studies show",
                    "evidence points to"
                ]
            },
            "philosophical": {
                "formality": "high",
                "precision": "conceptual",
                "abstract_terms": True,
                "metaphysical_language": True,
                "preferred_connectives": ["therefore", "hence", "thus", "it follows"],
                "preferred_conditionals": ["necessity", "sufficiency", "biconditional_hint"],
                "example_phrases": [
                    "it is conceivable that",
                    "necessarily",
                    "contingently",
                    "a priori",
                    "metaphysically possible"
                ]
            },
            "mathematical": {
                "formality": "high",
                "precision": "absolute",
                "symbolic_notation": True,
                "proof_language": True,
                "preferred_connectives": ["therefore", "thus", "hence", "QED"],
                "preferred_conditionals": ["biconditional_hint", "equivalence", "standard"],
                "example_phrases": [
                    "by definition",
                    "it follows directly",
                    "by axiom",
                    "without loss of generality",
                    "by induction"
                ]
            },
            "business": {
                "formality": "medium",
                "precision": "practical",
                "action_oriented": True,
                "metrics_focused": True,
                "preferred_connectives": ["therefore", "so", "as a result", "consequently"],
                "preferred_conditionals": ["causal", "temporal", "probabilistic"],
                "example_phrases": [
                    "market analysis shows",
                    "ROI indicates",
                    "strategic planning suggests",
                    "competitive advantage requires",
                    "stakeholder value"
                ]
            },
            "medical": {
                "formality": "high",
                "precision": "clinical",
                "technical_terms": True,
                "evidence_based": True,
                "preferred_connectives": ["therefore", "thus", "indicating", "suggesting"],
                "preferred_conditionals": ["causal", "probabilistic", "temporal"],
                "example_phrases": [
                    "clinical evidence suggests",
                    "symptoms indicate",
                    "diagnosis confirms",
                    "treatment protocol requires",
                    "patient presents with"
                ]
            }
        }
    
    def generate_domain_templates(self, domain: str, rule_name: str) -> List[EnhancedTemplate]:
        """
        Generate templates for a specific domain and rule.
        
        Args:
            domain: The domain (scientific, legal, etc.)
            rule_name: The inference rule name
            
        Returns:
            List of domain-specific templates
        """
        if domain not in self.domains:
            raise ValueError(f"Unknown domain: {domain}")
        
        return self.domains[domain](rule_name)
    
    def _create_scientific_templates(self, rule_name: str) -> List[EnhancedTemplate]:
        """Create scientific domain templates."""
        templates = []
        
        if rule_name == "Modus Ponens":
            # Scientific Modus Ponens
            builder = TemplateBuilder()
            builder.add_variation('hypothesis', [
                'The hypothesis that',
                'Experimental data suggest that',
                'Research indicates that',
                'Evidence demonstrates that'
            ])
            builder.add_static(' if ')
            builder.add_variable('p')
            builder.add_static(', then ')
            builder.add_variable('q')
            builder.add_static('. ')
            builder.add_variation('observation', [
                'Empirical observation confirms',
                'Data show',
                'Measurements indicate',
                'Results demonstrate'
            ])
            builder.add_static(' that ')
            builder.add_variable('p')
            builder.add_static('. ')
            builder.add_variation('conclusion', [
                'Therefore, we can conclude',
                'Thus, the data support',
                'Consequently, evidence indicates',
                'It follows from the data'
            ])
            builder.add_static(' that ')
            builder.add_variable('q')
            builder.add_static('.')
            builder.set_metadata('domain', 'scientific')
            builder.set_metadata('complexity', ComplexityLevel.ADVANCED)
            templates.append(builder.build())
            
            # With statistical confidence
            builder2 = TemplateBuilder()
            builder2.add_static('Given the ')
            builder2.add_variation('relationship', [
                'statistically significant relationship',
                'strong correlation',
                'causal relationship',
                'empirical connection'
            ])
            builder2.add_static(' whereby ')
            builder2.add_variable('p')
            builder2.add_static(' ')
            builder2.add_variation('leads_to', [
                'leads to',
                'results in',
                'causes',
                'produces'
            ])
            builder2.add_static(' ')
            builder2.add_variable('q')
            builder2.add_static(' (p < 0.05), and ')
            builder2.add_variation('given', [
                'given that',
                'observing that',
                'noting that'
            ])
            builder2.add_static(' ')
            builder2.add_variable('p')
            builder2.add_static(' ')
            builder2.add_variation('is_true', [
                'has been confirmed',
                'is observed',
                'is measured',
                'is demonstrated'
            ])
            builder2.add_static(', ')
            builder2.add_variation('we_conclude', [
                'we can infer with confidence',
                'statistical analysis suggests',
                'the data support the conclusion'
            ])
            builder2.add_static(' that ')
            builder2.add_variable('q')
            builder2.add_static('.')
            builder2.set_metadata('domain', 'scientific')
            builder2.set_metadata('complexity', ComplexityLevel.EXPERT)
            templates.append(builder2.build())
            
        elif rule_name == "Hypothetical Syllogism":
            # Scientific chain of causation
            builder = TemplateBuilder()
            builder.add_variation('studies_show', [
                'Studies demonstrate',
                'Research indicates',
                'Evidence suggests',
                'Literature confirms'
            ])
            builder.add_static(' that ')
            builder.add_variable('p')
            builder.add_static(' ')
            builder.add_variation('mechanism1', [
                'triggers a cascade resulting in',
                'initiates a process leading to',
                'causes a chain reaction producing',
                'activates pathways that yield'
            ])
            builder.add_static(' ')
            builder.add_variable('q')
            builder.add_static('. ')
            builder.add_variation('furthermore', [
                'Furthermore, research shows',
                'Additionally, studies confirm',
                'Moreover, evidence indicates'
            ])
            builder.add_static(' that ')
            builder.add_variable('q')
            builder.add_static(' ')
            builder.add_variation('mechanism2', [
                'subsequently leads to',
                'in turn produces',
                'ultimately results in',
                'consequently causes'
            ])
            builder.add_static(' ')
            builder.add_variable('r')
            builder.add_static('. ')
            builder.add_variation('therefore', [
                'Therefore, the complete pathway shows',
                'Thus, we can conclude that',
                'Consequently, the evidence supports that'
            ])
            builder.add_static(' ')
            builder.add_variable('p')
            builder.add_static(' ')
            builder.add_variation('final_result', [
                'ultimately leads to',
                'results in',
                'produces',
                'causes'
            ])
            builder.add_static(' ')
            builder.add_variable('r')
            builder.add_static(' through this mechanism.')
            builder.set_metadata('domain', 'scientific')
            builder.set_metadata('complexity', ComplexityLevel.EXPERT)
            templates.append(builder.build())
        
        return templates
    
    def _create_legal_templates(self, rule_name: str) -> List[EnhancedTemplate]:
        """Create legal domain templates."""
        templates = []
        
        if rule_name == "Modus Ponens":
            # Legal precedent application
            builder = TemplateBuilder()
            builder.add_variation('precedent', [
                'Legal precedent establishes',
                'Case law clearly states',
                'Binding authority holds',
                'Established jurisprudence provides'
            ])
            builder.add_static(' that if ')
            builder.add_variable('p')
            builder.add_static(', then ')
            builder.add_variable('q')
            builder.add_static('. ')
            builder.add_variation('facts', [
                'The facts of the present case demonstrate',
                'Evidence before the court shows',
                'The record clearly establishes',
                'Testimony confirms'
            ])
            builder.add_static(' that ')
            builder.add_variable('p')
            builder.add_static('. ')
            builder.add_variation('therefore', [
                'Therefore, as a matter of law',
                'Accordingly, the court must find',
                'Thus, it follows necessarily',
                'Hence, the legal conclusion is'
            ])
            builder.add_static(' that ')
            builder.add_variable('q')
            builder.add_static('.')
            builder.set_metadata('domain', 'legal')
            builder.set_metadata('complexity', ComplexityLevel.ADVANCED)
            templates.append(builder.build())
            
            # Statutory interpretation
            builder2 = TemplateBuilder()
            builder2.add_variation('statute', [
                'The statute provides',
                'The regulation states',
                'The law requires',
                'The code mandates'
            ])
            builder2.add_static(' that ')
            builder2.add_variation('condition', [
                'whenever',
                'in any case where',
                'if and when',
                'upon a showing that'
            ])
            builder2.add_static(' ')
            builder2.add_variable('p')
            builder2.add_static(', ')
            builder2.add_variation('consequence', [
                'the legal consequence is',
                'it shall follow that',
                'the result must be',
                'the law requires'
            ])
            builder2.add_static(' ')
            builder2.add_variable('q')
            builder2.add_static('. ')
            builder2.add_variation('application', [
                'In the instant case',
                'Here',
                'In this matter',
                'Applying this to the facts'
            ])
            builder2.add_static(', ')
            builder2.add_variable('p')
            builder2.add_static(' ')
            builder2.add_variation('proven', [
                'has been proven by a preponderance of the evidence',
                'is established beyond reasonable doubt',
                'is admitted by all parties',
                'is not in dispute'
            ])
            builder2.add_static('. ')
            builder2.add_variation('ruling', [
                'Therefore, this court holds',
                'Accordingly, we find',
                'Thus, the judgment must be',
                'Hence, the ruling is'
            ])
            builder2.add_static(' that ')
            builder2.add_variable('q')
            builder2.add_static('.')
            builder2.set_metadata('domain', 'legal')
            builder2.set_metadata('complexity', ComplexityLevel.EXPERT)
            templates.append(builder2.build())
            
        elif rule_name == "Modus Tollens":
            # Legal burden of proof
            builder = TemplateBuilder()
            builder.add_variation('burden', [
                'The burden of proof requires showing',
                'To establish liability, one must prove',
                'The elements of the claim require',
                'For a valid cause of action'
            ])
            builder.add_static(' that if ')
            builder.add_variable('p')
            builder.add_static(', then ')
            builder.add_variable('q')
            builder.add_static(' must follow. ')
            builder.add_variation('failure', [
                'The plaintiff has failed to show',
                'The evidence does not establish',
                'The record is devoid of proof',
                'No credible evidence supports'
            ])
            builder.add_static(' that ')
            builder.add_variable('q')
            builder.add_static('. ')
            builder.add_variation('therefore', [
                'Therefore, as a matter of law',
                'Consequently, the court must conclude',
                'Thus, it necessarily follows',
                'Accordingly, we must find'
            ])
            builder.add_static(' that ')
            builder.add_variable('not_p')
            builder.add_static('.')
            builder.set_metadata('domain', 'legal')
            builder.set_metadata('complexity', ComplexityLevel.ADVANCED)
            templates.append(builder.build())
        
        return templates
    
    def _create_everyday_templates(self, rule_name: str) -> List[EnhancedTemplate]:
        """Create everyday language templates."""
        templates = []
        
        if rule_name == "Modus Ponens":
            # Casual Modus Ponens
            builder = TemplateBuilder()
            builder.add_variation('setup', [
                'You know how',
                'Everyone knows',
                'It\'s like',
                'The thing is'
            ])
            builder.add_static(' if ')
            builder.add_variable('p')
            builder.add_static(', ')
            builder.add_variation('then', [
                'then',
                'you get',
                'that means',
                'it follows that'
            ])
            builder.add_static(' ')
            builder.add_variable('q')
            builder.add_static('. ')
            builder.add_variation('well', [
                'Well',
                'So',
                'And guess what',
                'Turns out'
            ])
            builder.add_static(', ')
            builder.add_variable('p')
            builder.add_static('. ')
            builder.add_variation('so', [
                'So',
                'That means',
                'Obviously',
                'Clearly'
            ])
            builder.add_static(', ')
            builder.add_variable('q')
            builder.add_static('.')
            builder.set_metadata('domain', 'everyday')
            builder.set_metadata('complexity', ComplexityLevel.BASIC)
            templates.append(builder.build())
            
            # Story-like format
            builder2 = TemplateBuilder()
            builder2.add_variable('Q')
            builder2.add_static(', ')
            builder2.add_variation('because', [
                'because',
                '\'cause',
                'since',
                'seeing as'
            ])
            builder2.add_static(' ')
            builder2.add_variable('p')
            builder2.add_static('. ')
            builder2.add_variation('remember', [
                'I mean',
                'You see',
                'The thing is',
                'Remember'
            ])
            builder2.add_static(', ')
            builder2.add_variation('whenever', [
                'whenever',
                'every time',
                'when',
                'if'
            ])
            builder2.add_static(' ')
            builder2.add_variable('p')
            builder2.add_static(', ')
            builder2.add_variation('you_get', [
                'you get',
                'you\'ve got',
                'there\'s',
                'you have'
            ])
            builder2.add_static(' ')
            builder2.add_variable('q')
            builder2.add_static('.')
            builder2.set_metadata('domain', 'everyday')
            builder2.set_metadata('complexity', ComplexityLevel.BASIC)
            templates.append(builder2.build())
        
        elif rule_name == "Disjunctive Syllogism":
            # Everyday choice elimination
            builder = TemplateBuilder()
            builder.add_variation('choice', [
                'It\'s either',
                'You\'ve got two options:',
                'The choice is',
                'It\'s one or the other:'
            ])
            builder.add_static(' ')
            builder.add_variable('p')
            builder.add_static(' or ')
            builder.add_variable('q')
            builder.add_static('. ')
            builder.add_variation('but', [
                'But',
                'Thing is',
                'However',
                'Turns out'
            ])
            builder.add_static(', ')
            builder.add_variable('not_p')
            builder.add_static('. ')
            builder.add_variation('so', [
                'So',
                'That leaves us with',
                'Guess that means',
                'Obviously then'
            ])
            builder.add_static(', ')
            builder.add_variable('q')
            builder.add_static('.')
            builder.set_metadata('domain', 'everyday')
            builder.set_metadata('complexity', ComplexityLevel.BASIC)
            templates.append(builder.build())
        
        return templates
    
    def _create_academic_templates(self, rule_name: str) -> List[EnhancedTemplate]:
        """Create academic writing templates."""
        templates = []
        
        if rule_name == "Modus Ponens":
            # Academic argument with citations
            builder = TemplateBuilder()
            builder.add_variation('scholars', [
                'Scholars have established',
                'The literature demonstrates',
                'Research consistently shows',
                'Academic consensus holds'
            ])
            builder.add_static(' that if ')
            builder.add_variable('p')
            builder.add_static(', then ')
            builder.add_variable('q')
            builder.add_static(' ')
            builder.add_variation('citation', [
                '(Smith, 2023)',
                '(Johnson et al., 2022)',
                '(Brown & Davis, 2024)',
                '(Wilson, 2023; Lee, 2024)'
            ])
            builder.add_static('. ')
            builder.add_variation('evidence', [
                'Recent evidence confirms',
                'Current data demonstrate',
                'Contemporary research shows',
                'New findings indicate'
            ])
            builder.add_static(' that ')
            builder.add_variable('p')
            builder.add_static('. ')
            builder.add_variation('therefore', [
                'Therefore, one can conclude',
                'Thus, the evidence supports',
                'Consequently, we may infer',
                'Hence, scholarship suggests'
            ])
            builder.add_static(' that ')
            builder.add_variable('q')
            builder.add_static('.')
            builder.set_metadata('domain', 'academic')
            builder.set_metadata('complexity', ComplexityLevel.ADVANCED)
            templates.append(builder.build())
            
        elif rule_name == "Hypothetical Syllogism":
            # Academic theoretical framework
            builder = TemplateBuilder()
            builder.add_variation('theory', [
                'Theoretical frameworks suggest',
                'The theoretical model posits',
                'According to established theory',
                'The conceptual framework indicates'
            ])
            builder.add_static(' that ')
            builder.add_variable('p')
            builder.add_static(' ')
            builder.add_variation('leads1', [
                'leads to',
                'results in',
                'produces',
                'generates'
            ])
            builder.add_static(' ')
            builder.add_variable('q')
            builder.add_static('. ')
            builder.add_variation('furthermore', [
                'Furthermore, research demonstrates',
                'Additionally, studies show',
                'Moreover, evidence indicates'
            ])
            builder.add_static(' that ')
            builder.add_variable('q')
            builder.add_static(' ')
            builder.add_variation('leads2', [
                'subsequently leads to',
                'in turn produces',
                'consequently results in'
            ])
            builder.add_static(' ')
            builder.add_variable('r')
            builder.add_static('. ')
            builder.add_variation('synthesis', [
                'Synthesizing these findings',
                'Integrating this evidence',
                'Combining these insights',
                'Drawing from this research'
            ])
            builder.add_static(', ')
            builder.add_variation('conclude', [
                'one can conclude',
                'we may infer',
                'it becomes evident',
                'scholarship supports'
            ])
            builder.add_static(' that ')
            builder.add_variable('p')
            builder.add_static(' ')
            builder.add_variation('ultimately', [
                'ultimately leads to',
                'eventually produces',
                'finally results in'
            ])
            builder.add_static(' ')
            builder.add_variable('r')
            builder.add_static('.')
            builder.set_metadata('domain', 'academic')
            builder.set_metadata('complexity', ComplexityLevel.EXPERT)
            templates.append(builder.build())
        
        return templates
    
    def _create_philosophical_templates(self, rule_name: str) -> List[EnhancedTemplate]:
        """Create philosophical argument templates."""
        templates = []
        
        if rule_name == "Modus Ponens":
            # Philosophical necessity
            builder = TemplateBuilder()
            builder.add_variation('premise', [
                'It is a necessary truth that',
                'By metaphysical necessity',
                'As a matter of logical necessity',
                'It is analytically true that'
            ])
            builder.add_static(' if ')
            builder.add_variable('p')
            builder.add_static(' obtains, then ')
            builder.add_variable('q')
            builder.add_static(' must follow. ')
            builder.add_variation('given', [
                'Given that',
                'Granting that',
                'Supposing that',
                'Acknowledging that'
            ])
            builder.add_static(' ')
            builder.add_variable('p')
            builder.add_static(' ')
            builder.add_variation('is_case', [
                'is indeed the case',
                'obtains in actuality',
                'holds true',
                'is instantiated'
            ])
            builder.add_static(', ')
            builder.add_variation('follows', [
                'it follows necessarily',
                'we must conclude',
                'reason compels us to accept',
                'logic dictates'
            ])
            builder.add_static(' that ')
            builder.add_variable('q')
            builder.add_static('.')
            builder.set_metadata('domain', 'philosophical')
            builder.set_metadata('complexity', ComplexityLevel.EXPERT)
            templates.append(builder.build())
        
        return templates
    
    def _create_mathematical_templates(self, rule_name: str) -> List[EnhancedTemplate]:
        """Create mathematical proof templates."""
        templates = []
        
        if rule_name == "Modus Ponens":
            # Mathematical proof style
            builder = TemplateBuilder()
            builder.add_variation('given', [
                'Given',
                'Let us assume',
                'Suppose',
                'By hypothesis'
            ])
            builder.add_static(' that ')
            builder.add_variable('p')
            builder.add_static(' → ')
            builder.add_variable('q')
            builder.add_static('. ')
            builder.add_variation('observe', [
                'We observe that',
                'It is given that',
                'By assumption',
                'We have'
            ])
            builder.add_static(' ')
            builder.add_variable('p')
            builder.add_static('. ')
            builder.add_variation('therefore', [
                'Therefore',
                'Hence',
                'Thus',
                'By modus ponens'
            ])
            builder.add_static(', ')
            builder.add_variable('q')
            builder.add_static('. ∎')
            builder.set_metadata('domain', 'mathematical')
            builder.set_metadata('complexity', ComplexityLevel.ADVANCED)
            templates.append(builder.build())
            
        elif rule_name == "Hypothetical Syllogism":
            # Mathematical transitivity
            builder = TemplateBuilder()
            builder.add_variation('let', [
                'Let',
                'Suppose',
                'Given',
                'Consider'
            ])
            builder.add_static(' ')
            builder.add_variable('p')
            builder.add_static(' ⟹ ')
            builder.add_variable('q')
            builder.add_static(' and ')
            builder.add_variable('q')
            builder.add_static(' ⟹ ')
            builder.add_variable('r')
            builder.add_static('. ')
            builder.add_variation('by', [
                'By transitivity of implication',
                'By the transitive property',
                'Applying transitivity',
                'Using chain rule'
            ])
            builder.add_static(', we have ')
            builder.add_variable('p')
            builder.add_static(' ⟹ ')
            builder.add_variable('r')
            builder.add_static('. ∎')
            builder.set_metadata('domain', 'mathematical')
            builder.set_metadata('complexity', ComplexityLevel.ADVANCED)
            templates.append(builder.build())
        
        return templates