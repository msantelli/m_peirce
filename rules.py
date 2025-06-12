"""
rules.py

Simple logical rule definitions and mappings.
Defines the 11 valid inference rules and their corresponding fallacies.
"""

from typing import Dict, Tuple, List
from dataclasses import dataclass


@dataclass
class RuleDefinition:
    """Simple rule definition with template requirements."""
    valid_name: str
    invalid_name: str
    description: str
    sentences_needed: int  # How many sentences are required
    template_type: str  # Type of logical structure


# Core logical rules and their fallacy counterparts
LOGICAL_RULES: Dict[str, RuleDefinition] = {
    "Modus Ponens": RuleDefinition(
        valid_name="Modus Ponens",
        invalid_name="Affirming the Consequent", 
        description="If P→Q, P ∴ Q vs If P→Q, Q ∴ P",
        sentences_needed=2,
        template_type="conditional"
    ),
    
    "Modus Tollens": RuleDefinition(
        valid_name="Modus Tollens",
        invalid_name="Denying the Antecedent",
        description="If P→Q, ¬Q ∴ ¬P vs If P→Q, ¬P ∴ ¬Q", 
        sentences_needed=2,
        template_type="conditional_negation"
    ),
    
    "Disjunctive Syllogism": RuleDefinition(
        valid_name="Disjunctive Syllogism",
        invalid_name="Affirming a Disjunct",
        description="P∨Q, ¬P ∴ Q vs P∨Q, P ∴ ¬Q",
        sentences_needed=2,
        template_type="disjunctive"
    ),
    
    "Conjunction Introduction": RuleDefinition(
        valid_name="Conjunction Introduction", 
        invalid_name="False Conjunction",
        description="P, Q ∴ P∧Q vs P ∴ P∧Q",
        sentences_needed=2,
        template_type="conjunction"
    ),
    
    "Conjunction Elimination": RuleDefinition(
        valid_name="Conjunction Elimination",
        invalid_name="Composition Fallacy", 
        description="P∧Q ∴ P vs Group has P ∴ All have P",
        sentences_needed=2,
        template_type="conjunction_elimination"
    ),
    
    "Disjunction Introduction": RuleDefinition(
        valid_name="Disjunction Introduction",
        invalid_name="Invalid Conjunction Introduction",
        description="P ∴ P∨Q vs P ∴ P∧Q", 
        sentences_needed=2,
        template_type="disjunction_intro"
    ),
    
    "Disjunction Elimination": RuleDefinition(
        valid_name="Disjunction Elimination",
        invalid_name="Invalid Disjunction Elimination",
        description="Complete vs Incomplete case analysis",
        sentences_needed=3,
        template_type="disjunction_elimination"
    ),
    
    "Hypothetical Syllogism": RuleDefinition(
        valid_name="Hypothetical Syllogism", 
        invalid_name="Non Sequitur",
        description="P→Q, Q→R ∴ P→R vs P ∴ Q",
        sentences_needed=3,
        template_type="hypothetical"
    ),
    
    "Material Conditional Introduction": RuleDefinition(
        valid_name="Material Conditional Introduction",
        invalid_name="Invalid Material Conditional Introduction", 
        description="Valid conditional formation vs Adding unwarranted variables",
        sentences_needed=3,
        template_type="material_conditional"
    ),
    
    "Constructive Dilemma": RuleDefinition(
        valid_name="Constructive Dilemma",
        invalid_name="False Dilemma",
        description="Valid disjunction vs Limited options",
        sentences_needed=3,
        template_type="constructive_dilemma"
    ),
    
    "Destructive Dilemma": RuleDefinition(
        valid_name="Destructive Dilemma", 
        invalid_name="Non Sequitur",
        description="Valid complex reasoning vs Invalid conclusion",
        sentences_needed=3,
        template_type="destructive_dilemma"
    )
}


def get_rule_definition(rule_name: str) -> RuleDefinition:
    """Get rule definition by name."""
    return LOGICAL_RULES.get(rule_name)


def get_all_rules() -> List[str]:
    """Get list of all rule names."""
    return list(LOGICAL_RULES.keys())


def get_rules_by_sentence_count(count: int) -> List[str]:
    """Get rules that require a specific number of sentences."""
    return [name for name, rule in LOGICAL_RULES.items() 
            if rule.sentences_needed == count]


def get_rule_pairs() -> List[Tuple[str, str]]:
    """Get all (valid_rule, invalid_rule) pairs.""" 
    return [(rule.valid_name, rule.invalid_name) 
            for rule in LOGICAL_RULES.values()]