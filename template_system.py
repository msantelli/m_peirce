"""
template_system.py

Enhanced template system that supports multiple variation types and complex template structures.
"""

from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass
from enum import Enum
import re
import random
from linguistic_patterns import VariationTemplate, VariationType, ComplexityLevel


class TemplateComponentType(Enum):
    """Types of components in a template."""
    STATIC = "static"  # Fixed text
    VARIABLE = "variable"  # Simple variable substitution
    VARIATION = "variation"  # Variation point with multiple options
    CONDITIONAL = "conditional"  # Conditional inclusion
    REPEATED = "repeated"  # Repeated pattern


@dataclass
class TemplateComponent:
    """Represents a component of a template."""
    component_type: TemplateComponentType
    content: str
    options: Optional[Dict[str, Any]] = None
    
    def render(self, context: Dict[str, Any]) -> str:
        """Render this component given a context."""
        if self.component_type == TemplateComponentType.STATIC:
            return self.content
        
        elif self.component_type == TemplateComponentType.VARIABLE:
            var_name = self.content
            if var_name in context:
                return str(context[var_name])
            return f"{{{var_name}}}"  # Return placeholder if not found
        
        elif self.component_type == TemplateComponentType.VARIATION:
            # Options should contain 'choices' key with list of options
            if self.options and 'choices' in self.options:
                choice = random.choice(self.options['choices'])
                # Recursively render the choice
                return self._render_template_string(choice, context)
            return self.content
        
        elif self.component_type == TemplateComponentType.CONDITIONAL:
            # Options should contain 'condition' and 'true_template', 'false_template'
            if self.options:
                condition = self.options.get('condition', '')
                if self._evaluate_condition(condition, context):
                    template = self.options.get('true_template', '')
                else:
                    template = self.options.get('false_template', '')
                return self._render_template_string(template, context)
            return ""
        
        elif self.component_type == TemplateComponentType.REPEATED:
            # Options should contain 'items' key and 'separator'
            if self.options:
                items_key = self.options.get('items', '')
                separator = self.options.get('separator', ', ')
                if items_key in context and isinstance(context[items_key], list):
                    rendered = []
                    for item in context[items_key]:
                        item_context = context.copy()
                        item_context['item'] = item
                        rendered.append(self._render_template_string(
                            self.content, item_context
                        ))
                    return separator.join(rendered)
            return ""
        
        return ""
    
    def _render_template_string(self, template: str, context: Dict[str, Any]) -> str:
        """Helper to render a template string."""
        # Simple variable substitution
        for key, value in context.items():
            template = template.replace(f"{{{key}}}", str(value))
        return template
    
    def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """Evaluate a simple condition."""
        # Very simple evaluation - just checks if a variable exists and is truthy
        # Could be enhanced with more complex logic
        if condition in context:
            return bool(context[condition])
        return False


class EnhancedTemplate:
    """Enhanced template with rich variation support."""
    
    def __init__(self, template_string: str, metadata: Optional[Dict[str, Any]] = None):
        self.template_string = template_string
        self.metadata = metadata or {}
        self.components = self._parse_template()
        self.required_variables = self._extract_required_variables()
    
    def _parse_template(self) -> List[TemplateComponent]:
        """Parse the template string into components."""
        components = []
        
        # Pattern for variation points: [[choice1|choice2|choice3]]
        variation_pattern = r'\[\[([^\]]+)\]\]'
        
        # Pattern for variables: {variable_name}
        variable_pattern = r'\{([^}]+)\}'
        
        remaining = self.template_string
        
        while remaining:
            # Find the next occurrence of either pattern
            variation_match = re.search(variation_pattern, remaining)
            variable_match = re.search(variable_pattern, remaining)
            
            # Determine which pattern comes first
            next_variation_pos = variation_match.start() if variation_match else float('inf')
            next_variable_pos = variable_match.start() if variable_match else float('inf')
            
            if next_variation_pos < next_variable_pos:
                # Variation comes first
                # Add static text before variation (parse it for variables)
                if variation_match and variation_match.start() > 0:
                    static_text = remaining[:variation_match.start()]
                    components.extend(self._parse_static_text(static_text))
                
                # Add variation component
                if variation_match:
                    choices = variation_match.group(1).split('|')
                    components.append(TemplateComponent(
                        TemplateComponentType.VARIATION,
                        variation_match.group(0),
                        {'choices': choices}
                    ))
                    
                    remaining = remaining[variation_match.end():]
                
            elif next_variable_pos < float('inf'):
                # Variable comes first
                # Add static text before variable
                if variable_match and variable_match.start() > 0:
                    static_text = remaining[:variable_match.start()]
                    if static_text:
                        components.append(TemplateComponent(
                            TemplateComponentType.STATIC,
                            static_text
                        ))
                
                # Add variable component
                if variable_match:
                    components.append(TemplateComponent(
                        TemplateComponentType.VARIABLE,
                        variable_match.group(1)
                    ))
                    
                    remaining = remaining[variable_match.end():]
                
            else:
                # No more patterns, rest is static text
                if remaining:
                    components.append(TemplateComponent(
                        TemplateComponentType.STATIC,
                        remaining
                    ))
                break
        
        return components
    
    def _parse_static_text(self, text: str) -> List[TemplateComponent]:
        """Parse static text that might contain variables."""
        if not text:
            return []
        
        components = []
        variable_pattern = r'\{([^}]+)\}'
        
        remaining = text
        while remaining:
            var_match = re.search(variable_pattern, remaining)
            if var_match:
                # Add static text before variable
                if var_match.start() > 0:
                    components.append(TemplateComponent(
                        TemplateComponentType.STATIC,
                        remaining[:var_match.start()]
                    ))
                
                # Add variable component
                components.append(TemplateComponent(
                    TemplateComponentType.VARIABLE,
                    var_match.group(1)
                ))
                
                remaining = remaining[var_match.end():]
            else:
                # Rest is static text
                if remaining:
                    components.append(TemplateComponent(
                        TemplateComponentType.STATIC,
                        remaining
                    ))
                break
        
        return components
    
    def _extract_required_variables(self) -> Set[str]:
        """Extract all required variables from the template."""
        variables = set()
        
        for component in self.components:
            if component.component_type == TemplateComponentType.VARIABLE:
                variables.add(component.content)
            elif component.component_type == TemplateComponentType.VARIATION:
                # Extract variables from choices
                if component.options and 'choices' in component.options:
                    for choice in component.options['choices']:
                        # Find variables in choice
                        var_matches = re.findall(r'\{([^}]+)\}', choice)
                        variables.update(var_matches)
        
        return variables
    
    def render(self, context: Dict[str, Any], 
               variation_preferences: Optional[Dict[str, Any]] = None) -> str:
        """
        Render the template with the given context.
        
        Args:
            context: Variable values and other context
            variation_preferences: Optional preferences for variations
            
        Returns:
            Rendered template string
        """
        # Merge variation preferences into context
        full_context = context.copy()
        if variation_preferences:
            full_context.update(variation_preferences)
        
        # Render each component
        rendered_parts = []
        for component in self.components:
            rendered_parts.append(component.render(full_context))
        
        return ''.join(rendered_parts)
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about this template."""
        return {
            'template_string': self.template_string,
            'required_variables': list(self.required_variables),
            'component_count': len(self.components),
            'has_variations': any(c.component_type == TemplateComponentType.VARIATION 
                                 for c in self.components),
            'metadata': self.metadata
        }


class TemplateBank:
    """Manages collections of templates organized by rule and type."""
    
    def __init__(self):
        self.templates: Dict[str, Dict[str, List[EnhancedTemplate]]] = {}
        self.variation_mappings: Dict[str, Dict[str, Any]] = {}
    
    def add_template(self, rule_name: str, template_type: str, 
                    template: EnhancedTemplate):
        """Add a template to the bank."""
        if rule_name not in self.templates:
            self.templates[rule_name] = {}
        if template_type not in self.templates[rule_name]:
            self.templates[rule_name][template_type] = []
        
        self.templates[rule_name][template_type].append(template)
    
    def add_variation_mapping(self, variation_name: str, mapping: Dict[str, Any]):
        """Add a variation mapping."""
        self.variation_mappings[variation_name] = mapping
    
    def get_templates(self, rule_name: str, template_type: str = "valid") -> List[EnhancedTemplate]:
        """Get templates for a rule and type."""
        if rule_name in self.templates and template_type in self.templates[rule_name]:
            return self.templates[rule_name][template_type]
        return []
    
    def get_random_template(self, rule_name: str, template_type: str = "valid",
                           complexity: Optional[ComplexityLevel] = None) -> Optional[EnhancedTemplate]:
        """Get a random template, optionally filtered by complexity."""
        templates = self.get_templates(rule_name, template_type)
        
        if complexity:
            # Filter by complexity if specified
            filtered = [t for t in templates 
                       if t.metadata.get('complexity', ComplexityLevel.BASIC) == complexity]
            if filtered:
                templates = filtered
        
        if templates:
            return random.choice(templates)
        return None
    
    def create_template_from_pattern(self, pattern: str, 
                                   variation_points: Optional[Dict[str, List[str]]] = None,
                                   metadata: Optional[Dict[str, Any]] = None) -> EnhancedTemplate:
        """
        Create a template from a pattern string with variation points.
        
        Args:
            pattern: Pattern string with placeholders
            variation_points: Dict mapping variation names to choices
            metadata: Optional metadata for the template
            
        Returns:
            Enhanced template
        """
        # Replace variation points in pattern
        if variation_points:
            for var_name, choices in variation_points.items():
                # Replace {{var_name}} with [[choice1|choice2|...]]
                placeholder = f"{{{{{var_name}}}}}"
                variation = f"[[{'|'.join(choices)}]]"
                pattern = pattern.replace(placeholder, variation)
        
        return EnhancedTemplate(pattern, metadata)
    
    def generate_argument(self, rule_name: str, variables: Dict[str, str],
                         template_type: str = "valid",
                         options: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate an argument using templates.
        
        Args:
            rule_name: Name of the inference rule
            variables: Variable substitutions
            template_type: Type of template (valid/invalid)
            options: Optional generation options
            
        Returns:
            Generated argument string
        """
        # Get template based on options
        complexity = options.get('complexity', None) if options else None
        template = self.get_random_template(rule_name, template_type, complexity)
        
        if not template:
            return f"No template found for {rule_name} ({template_type})"
        
        # Prepare context
        context = variables.copy()
        
        # Add any additional context from options
        if options:
            if 'variation_preferences' in options:
                context.update(options['variation_preferences'])
        
        # Render template
        return template.render(context)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the template bank."""
        stats = {
            'total_rules': len(self.templates),
            'total_templates': 0,
            'rules': {}
        }
        
        for rule_name, rule_templates in self.templates.items():
            rule_stats = {}
            for template_type, templates in rule_templates.items():
                rule_stats[template_type] = len(templates)
                stats['total_templates'] += len(templates)
            stats['rules'][rule_name] = rule_stats
        
        return stats


class TemplateBuilder:
    """Builder class for creating templates with complex variations."""
    
    def __init__(self):
        self.components = []
        self.metadata = {}
        self.variation_points = {}
    
    def add_static(self, text: str) -> 'TemplateBuilder':
        """Add static text to the template."""
        self.components.append(('static', text))
        return self
    
    def add_variable(self, var_name: str) -> 'TemplateBuilder':
        """Add a variable to the template."""
        self.components.append(('variable', var_name))
        return self
    
    def add_variation(self, name: str, choices: List[str]) -> 'TemplateBuilder':
        """Add a variation point to the template."""
        self.variation_points[name] = choices
        self.components.append(('variation', name))
        return self
    
    def add_conditional(self, condition: str, true_part: str, 
                       false_part: str = "") -> 'TemplateBuilder':
        """Add a conditional component."""
        self.components.append(('conditional', {
            'condition': condition,
            'true': true_part,
            'false': false_part
        }))
        return self
    
    def set_metadata(self, key: str, value: Any) -> 'TemplateBuilder':
        """Set metadata for the template."""
        self.metadata[key] = value
        return self
    
    def build(self) -> EnhancedTemplate:
        """Build the final template."""
        # Construct template string
        template_parts = []
        
        for comp_type, content in self.components:
            if comp_type == 'static':
                template_parts.append(content)
            elif comp_type == 'variable':
                template_parts.append(f"{{{content}}}")
            elif comp_type == 'variation':
                if content in self.variation_points:
                    choices = self.variation_points[content]
                    template_parts.append(f"[[{'|'.join(choices)}]]")
                else:
                    template_parts.append(f"{{{{{content}}}}}")
            elif comp_type == 'conditional':
                # Simplified conditional representation
                template_parts.append(f"{{if {content['condition']}}}{content['true']}{{else}}{content['false']}{{endif}}")
        
        template_string = ''.join(template_parts)
        return EnhancedTemplate(template_string, self.metadata)


class VariationLibrary:
    """Library of reusable variation patterns."""
    
    def __init__(self):
        self.variations = {}
        self._init_standard_variations()
    
    def _init_standard_variations(self):
        """Initialize standard variations used across languages."""
        # Negation variations
        self.variations['negation_simple'] = [
            "{sentence} is not the case",
            "{sentence} is false",
            "not {sentence}",
            "{sentence} doesn't hold"
        ]
        
        self.variations['negation_formal'] = [
            "it is false that {sentence}",
            "it is not the case that {sentence}",
            "{sentence} is not true",
            "the proposition that {sentence} is false"
        ]
        
        self.variations['negation_emphatic'] = [
            "{sentence} is definitely false",
            "{sentence} is certainly not the case",
            "{sentence} is absolutely false",
            "{sentence} is unquestionably false"
        ]
        
        # Conjunction variations
        self.variations['conjunction_simple'] = [
            "{p} and {q}",
            "{p}, and {q}",
            "both {p} and {q}",
            "{p} as well as {q}"
        ]
        
        self.variations['conjunction_formal'] = [
            "{p} in conjunction with {q}",
            "{p} combined with {q}",
            "{p} together with {q}",
            "the conjunction of {p} and {q}"
        ]
        
        # Disjunction variations
        self.variations['disjunction_inclusive'] = [
            "{p} or {q}",
            "{p}, or {q}",
            "either {p} or {q} or both",
            "{p} and/or {q}"
        ]
        
        self.variations['disjunction_exclusive'] = [
            "either {p} or {q} but not both",
            "exactly one of {p} or {q}",
            "{p} or {q}, but not both",
            "either {p} or {q} (exclusive)"
        ]
        
        # Conditional variations
        self.variations['conditional_standard'] = [
            "if {antecedent}, then {consequent}",
            "if {antecedent} then {consequent}",
            "{consequent} if {antecedent}",
            "given {antecedent}, {consequent}"
        ]
        
        self.variations['conditional_causal'] = [
            "{antecedent} causes {consequent}",
            "{antecedent} leads to {consequent}",
            "{antecedent} results in {consequent}",
            "{antecedent} brings about {consequent}"
        ]
        
        self.variations['conditional_necessity'] = [
            "{consequent} is necessary for {antecedent}",
            "{antecedent} requires {consequent}",
            "without {consequent}, no {antecedent}",
            "{antecedent} only if {consequent}"
        ]
        
        self.variations['conditional_sufficiency'] = [
            "{antecedent} is sufficient for {consequent}",
            "{antecedent} guarantees {consequent}",
            "{antecedent} ensures {consequent}",
            "{antecedent} implies {consequent}"
        ]
    
    def get_variation(self, variation_type: str) -> List[str]:
        """Get a variation pattern by type."""
        return self.variations.get(variation_type, [])
    
    def add_variation(self, name: str, patterns: List[str]):
        """Add a new variation pattern."""
        self.variations[name] = patterns
    
    def get_all_variations(self) -> Dict[str, List[str]]:
        """Get all variations."""
        return self.variations.copy()
    
    def get_variation_types(self) -> List[str]:
        """Get list of available variation types."""
        return list(self.variations.keys())