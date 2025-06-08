"""
english_integration.py

Integration module that combines enhanced English language support
with domain-specific templates and complexity levels.
"""

from typing import Dict, List, Optional, Any, Set
from languages.english_enhanced import (
    EnhancedEnglishPattern, EnhancedEnglishTemplates, EnglishGrammar, EnglishStyleGuide
)
from domain_templates import DomainTemplateGenerator
from template_system import TemplateBank, EnhancedTemplate
from linguistic_patterns import ComplexityLevel, VariationType, VariationGenerator
from language_base import LanguageAdapter, LanguageFactory


class IntegratedEnglishAdapter(LanguageAdapter):
    """
    Integrated English adapter that combines base English support
    with domain-specific templates and advanced features.
    """
    
    def __init__(self):
        # Initialize enhanced components
        self.pattern = EnhancedEnglishPattern()
        self.base_templates = EnhancedEnglishTemplates(self.pattern)
        self.grammar = EnglishGrammar()
        self.style_guide = EnglishStyleGuide()
        
        # Initialize domain generator
        self.domain_generator = DomainTemplateGenerator()
        
        # Create integrated template bank
        self.integrated_templates = self._create_integrated_templates()
        
        # Initialize parent with base templates
        super().__init__(self.pattern, self.base_templates, 
                        self.grammar, self.style_guide)
        
        # Override templates with integrated version
        self.templates = self.integrated_templates
        
        # Create variation generator
        self.variation_generator = VariationGenerator(self.pattern)
    
    def _create_integrated_templates(self) -> 'IntegratedTemplates':
        """Create integrated template system."""
        return IntegratedTemplates(
            self.base_templates,
            self.domain_generator,
            self.pattern
        )
    
    def generate_argument(self, rule_name: str, variables: Dict[str, str],
                         is_valid: bool = True, 
                         options: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate an argument with full support for domains and complexity.
        
        Args:
            rule_name: Name of the inference rule
            variables: Variable substitutions
            is_valid: Whether to generate valid or invalid form
            options: Generation options including domain, complexity, etc.
            
        Returns:
            Generated argument
        """
        options = options or {}
        
        # Extract options
        domain = options.get('domain', 'general')
        complexity = options.get('complexity', ComplexityLevel.BASIC)
        formality = options.get('formality', 'neutral')
        emphasis = options.get('emphasis', None)
        
        # Set complexity in variation generator
        self.variation_generator.set_complexity(complexity)
        
        # Prepare variables with appropriate variations
        enhanced_vars = self._prepare_enhanced_variables(
            variables, complexity, domain
        )
        
        # Get appropriate templates
        if domain != 'general':
            templates = self.integrated_templates.get_domain_templates(
                rule_name, is_valid, domain
            )
        else:
            templates = self.integrated_templates.get_templates(
                rule_name, is_valid
            )
        
        # Filter by complexity if templates available
        if templates:
            complexity_filtered = [
                t for t in templates 
                if t.metadata.get('complexity', ComplexityLevel.BASIC) == complexity
            ]
            if complexity_filtered:
                templates = complexity_filtered
        
        if not templates:
            return f"No templates available for {rule_name} in {domain} domain"
        
        # Select template
        import random
        template = random.choice(templates)
        
        # Render template
        argument = template.render(enhanced_vars, options)
        
        # Apply style guide
        argument = self.style_guide.apply_formality(argument, formality)
        
        # Apply domain-specific styling
        if domain != 'general':
            argument = self.domain_generator.apply_domain_style(argument, domain)
        
        # Apply emphasis if requested
        if emphasis:
            argument = self.style_guide.apply_rhetorical_emphasis(argument, emphasis)
        
        return argument
    
    def _prepare_enhanced_variables(self, variables: Dict[str, str],
                                   complexity: ComplexityLevel,
                                   domain: str) -> Dict[str, str]:
        """
        Prepare variables with complexity and domain-appropriate variations.
        
        Args:
            variables: Base variables
            complexity: Complexity level
            domain: Domain
            
        Returns:
            Enhanced variables with variations
        """
        enhanced = variables.copy()
        
        # For each base variable, add variations
        for var, value in variables.items():
            if var.islower() and len(var) == 1:  # Base variables like p, q, r
                # Add negation variations
                neg_style = self.pattern.get_complexity_appropriate_style(
                    VariationType.NEGATION, complexity
                )
                if not neg_style:
                    neg_style = self.pattern.get_domain_appropriate_style(
                        VariationType.NEGATION, domain
                    )
                
                enhanced[f'not_{var}'] = self.variation_generator.generate_negation(
                    value, style=neg_style
                )
                enhanced[f'not_{var.upper()}'] = self.pattern.capitalize_sentence(
                    enhanced[f'not_{var}']
                )
                
                # Add additional negation styles for higher complexity
                if complexity in [ComplexityLevel.ADVANCED, ComplexityLevel.EXPERT]:
                    enhanced[f'not_formal_{var}'] = self.variation_generator.generate_negation(
                        value, style='formal'
                    )
                    enhanced[f'not_emphatic_{var}'] = self.variation_generator.generate_negation(
                        value, style='emphatic'
                    )
        
        return enhanced
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Get comprehensive capabilities of this adapter."""
        return {
            'language_code': 'en',
            'language_name': 'English',
            'supported_domains': self.get_supported_domains(),
            'complexity_levels': [level.name for level in ComplexityLevel],
            'variation_types': {
                'negation': list(self.pattern.negation_patterns.keys()),
                'conjunction': list(self.pattern.conjunction_patterns.keys()),
                'disjunction': list(self.pattern.disjunction_patterns.keys()),
                'conditional': list(self.pattern.conditional_patterns.keys())
            },
            'formality_levels': list(self.style_guide.formality_levels.keys()),
            'inference_rules': list(self.templates.templates.keys()),
            'features': [
                'complexity_aware_generation',
                'domain_specific_templates',
                'rich_linguistic_variations',
                'style_adaptation',
                'rhetorical_emphasis'
            ]
        }


class IntegratedTemplates:
    """
    Integrated template system that combines base templates
    with domain-specific templates.
    """
    
    def __init__(self, base_templates: EnhancedEnglishTemplates,
                 domain_generator: DomainTemplateGenerator,
                 pattern: EnhancedEnglishPattern):
        self.base_templates = base_templates
        self.domain_generator = domain_generator
        self.pattern = pattern
        
        # Cache for domain templates
        self.domain_cache = {}
        
        # Create unified template bank
        self.templates = self._merge_templates()
    
    def _merge_templates(self) -> Dict[str, Dict[str, List[EnhancedTemplate]]]:
        """Merge base and domain templates."""
        # Start with base templates
        merged = self.base_templates.templates.copy()
        
        # For each domain, generate and store templates
        for domain in self.domain_generator.domains.keys():
            domain_key = f"domain_{domain}"
            if domain_key not in self.domain_cache:
                self.domain_cache[domain_key] = {}
                
                # Generate templates for each rule
                for rule in merged.keys():
                    try:
                        domain_templates = self.domain_generator.generate_domain_templates(
                            domain, rule
                        )
                        if domain_templates:
                            self.domain_cache[domain_key][rule] = {
                                'valid': domain_templates
                            }
                    except:
                        # Not all domains have all rules
                        continue
        
        return merged
    
    def get_templates(self, rule_name: str, is_valid: bool = True) -> List[EnhancedTemplate]:
        """Get base templates for a rule."""
        template_type = 'valid' if is_valid else 'invalid'
        
        if rule_name in self.templates:
            return self.templates[rule_name].get(template_type, [])
        return []
    
    def get_domain_templates(self, rule_name: str, is_valid: bool,
                           domain: str) -> List[EnhancedTemplate]:
        """Get domain-specific templates."""
        domain_key = f"domain_{domain}"
        template_type = 'valid' if is_valid else 'invalid'
        
        # Check cache first
        if domain_key in self.domain_cache:
            if rule_name in self.domain_cache[domain_key]:
                templates = self.domain_cache[domain_key][rule_name].get(template_type, [])
                if templates:
                    return templates
        
        # Generate on demand if not cached
        try:
            templates = self.domain_generator.generate_domain_templates(domain, rule_name)
            if templates:
                if domain_key not in self.domain_cache:
                    self.domain_cache[domain_key] = {}
                if rule_name not in self.domain_cache[domain_key]:
                    self.domain_cache[domain_key][rule_name] = {}
                self.domain_cache[domain_key][rule_name][template_type] = templates
                return templates
        except:
            pass
        
        # Fall back to base templates
        return self.get_templates(rule_name, is_valid)
    
    def get_required_sentences(self, rule_name: str) -> int:
        """Get required sentences for a rule."""
        return self.base_templates.get_required_sentences(rule_name)
    
    def get_template_variables(self, rule_name: str) -> Set[str]:
        """Get variables used in templates for a rule."""
        return self.base_templates.get_template_variables(rule_name)


# Register the integrated adapter
LanguageFactory.register_language("en", IntegratedEnglishAdapter)


# Example usage function
def demonstrate_integrated_english():
    """Demonstrate the capabilities of the integrated English adapter."""
    
    # Create adapter
    adapter = IntegratedEnglishAdapter()
    
    # Example sentences
    sentences = {
        'p': 'the data shows anomalies',
        'q': 'the hypothesis is rejected',
        'P': 'The data shows anomalies',
        'Q': 'The hypothesis is rejected'
    }
    
    print("=== Integrated English Adapter Demonstration ===\n")
    
    # 1. Scientific domain, expert level
    print("1. Scientific Domain (Expert Level):")
    arg1 = adapter.generate_argument(
        "Modus Ponens",
        sentences,
        is_valid=True,
        options={
            'domain': 'scientific',
            'complexity': ComplexityLevel.EXPERT,
            'formality': 'formal'
        }
    )
    print(arg1)
    print()
    
    # 2. Legal domain, advanced level
    legal_sentences = {
        'p': 'the defendant breached the contract',
        'q': 'the plaintiff is entitled to damages',
        'P': 'The defendant breached the contract',
        'Q': 'The plaintiff is entitled to damages'
    }
    
    print("2. Legal Domain (Advanced Level):")
    arg2 = adapter.generate_argument(
        "Modus Ponens",
        legal_sentences,
        is_valid=True,
        options={
            'domain': 'legal',
            'complexity': ComplexityLevel.ADVANCED,
            'formality': 'formal'
        }
    )
    print(arg2)
    print()
    
    # 3. Everyday domain, basic level
    everyday_sentences = {
        'p': 'it rains',
        'q': 'the ground gets wet',
        'P': 'It rains',
        'Q': 'The ground gets wet'
    }
    
    print("3. Everyday Domain (Basic Level):")
    arg3 = adapter.generate_argument(
        "Modus Ponens",
        everyday_sentences,
        is_valid=True,
        options={
            'domain': 'everyday',
            'complexity': ComplexityLevel.BASIC,
            'formality': 'casual'
        }
    )
    print(arg3)
    print()
    
    # 4. Business domain with disjunctive syllogism
    business_sentences = {
        'p': 'we expand internationally',
        'q': 'we focus on domestic growth',
        'not_p': 'international expansion is not viable',
        'P': 'We expand internationally',
        'Q': 'We focus on domestic growth',
        'not_P': 'International expansion is not viable'
    }
    
    print("4. Business Domain (Disjunctive Syllogism):")
    arg4 = adapter.generate_argument(
        "Disjunctive Syllogism",
        business_sentences,
        is_valid=True,
        options={
            'domain': 'business',
            'complexity': ComplexityLevel.INTERMEDIATE,
            'formality': 'neutral'
        }
    )
    print(arg4)
    print()
    
    # 5. Show capabilities
    print("5. Adapter Capabilities:")
    capabilities = adapter.get_capabilities()
    print(f"Supported domains: {', '.join(capabilities['supported_domains'])}")
    print(f"Complexity levels: {', '.join(capabilities['complexity_levels'])}")
    print(f"Negation styles: {', '.join(capabilities['variation_types']['negation'])}")
    print(f"Features: {', '.join(capabilities['features'])}")


if __name__ == "__main__":
    demonstrate_integrated_english()_supported_domains(self) -> List[str]:
        """Get list of supported domains."""
        return list(self.domain_generator.domains.keys())
    
    def get