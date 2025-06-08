"""
interactive_config.py

Interactive configuration system for fine-tuning argument generation
with real-time preview and adjustment capabilities.
"""

from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
import os
from datetime import datetime


class ConfigurationType(Enum):
    """Types of configuration parameters."""
    LANGUAGE = "language"
    COMPLEXITY = "complexity"
    DOMAIN = "domain"
    FORMALITY = "formality"
    VARIATION_STYLE = "variation_style"
    STRENGTH = "strength"
    COHERENCE = "coherence"
    OUTPUT_FORMAT = "output_format"


@dataclass
class ConfigOption:
    """Represents a configuration option."""
    name: str
    type: ConfigurationType
    value: Any
    possible_values: List[Any]
    description: str
    affects: List[str]  # What this option affects
    constraints: Dict[str, Any] = field(default_factory=dict)
    
    def validate(self, value: Any) -> bool:
        """Validate if a value is acceptable for this option."""
        if self.possible_values and value not in self.possible_values:
            return False
        
        # Check constraints
        if 'min' in self.constraints and value < self.constraints['min']:
            return False
        if 'max' in self.constraints and value > self.constraints['max']:
            return False
        if 'depends_on' in self.constraints:
            # Would need access to other config values
            pass
        
        return True


@dataclass
class ConfigurationProfile:
    """A complete configuration profile."""
    name: str
    description: str
    options: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'name': self.name,
            'description': self.description,
            'options': self.options,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConfigurationProfile':
        """Create from dictionary."""
        return cls(
            name=data['name'],
            description=data['description'],
            options=data['options'],
            metadata=data.get('metadata', {})
        )


class InteractiveConfigurator:
    """Interactive configuration system for argument generation."""
    
    def __init__(self):
        self.options = self._init_configuration_options()
        self.profiles = self._load_profiles()
        self.current_config = self._get_default_config()
        self.preview_callback = None
        self.validation_rules = self._init_validation_rules()
    
    def _init_configuration_options(self) -> Dict[str, ConfigOption]:
        """Initialize all configuration options."""
        options = {}
        
        # Language selection
        options['language'] = ConfigOption(
            name='language',
            type=ConfigurationType.LANGUAGE,
            value='en',
            possible_values=[
                'standard', 'educational', 'quiz', 'comparative', 
                'detailed', 'minimal', 'json'
            ],
            description='Output format for generated arguments',
            affects=['formatting', 'metadata_inclusion']
        )
        
        options['include_analysis'] = ConfigOption(
            name='include_analysis',
            type=ConfigurationType.OUTPUT_FORMAT,
            value=False,
            possible_values=[True, False],
            description='Include strength analysis with arguments',
            affects=['output_verbosity']
        )
        
        return options
    
    def _load_profiles(self) -> Dict[str, ConfigurationProfile]:
        """Load saved configuration profiles."""
        profiles = {}
        
        # Default profiles
        profiles['beginner'] = ConfigurationProfile(
            name='beginner',
            description='Simple arguments for logic beginners',
            options={
                'language': 'en',
                'complexity': 'basic',
                'domain': 'everyday',
                'formality': 'casual',
                'semantic_coherence': 'high',
                'target_plausibility': 0.9
            }
        )
        
        profiles['advanced_logic'] = ConfigurationProfile(
            name='advanced_logic',
            description='Complex arguments for advanced study',
            options={
                'language': 'en',
                'complexity': 'expert',
                'domain': 'philosophical',
                'formality': 'formal',
                'semantic_coherence': 'medium',
                'target_persuasiveness': 0.8
            }
        )
        
        profiles['multilingual_demo'] = ConfigurationProfile(
            name='multilingual_demo',
            description='Showcase arguments across languages',
            options={
                'complexity': 'intermediate',
                'domain': 'general',
                'formality': 'neutral',
                'output_format': 'comparative'
            }
        )
        
        # Load custom profiles from file if exists
        profile_file = 'config_profiles.json'
        if os.path.exists(profile_file):
            try:
                with open(profile_file, 'r') as f:
                    custom_profiles = json.load(f)
                    for name, data in custom_profiles.items():
                        profiles[name] = ConfigurationProfile.from_dict(data)
            except:
                pass
        
        return profiles
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {opt.name: opt.value for opt in self.options.values()}
    
    def _init_validation_rules(self) -> List[Callable]:
        """Initialize cross-option validation rules."""
        rules = []
        
        def academic_requires_formal(config):
            if config.get('domain') == 'academic' and config.get('formality') == 'casual':
                return False, "Academic domain requires at least neutral formality"
            return True, ""
        
        def expert_coherence_flexibility(config):
            if config.get('complexity') == 'expert' and config.get('semantic_coherence') == 'strict':
                return False, "Expert complexity works better with flexible coherence"
            return True, ""
        
        rules.extend([academic_requires_formal, expert_coherence_flexibility])
        return rules
    
    def set_option(self, option_name: str, value: Any) -> bool:
        """Set a configuration option."""
        if option_name not in self.options:
            return False
        
        option = self.options[option_name]
        if not option.validate(value):
            return False
        
        # Update current config
        self.current_config[option_name] = value
        
        # Validate overall configuration
        is_valid, message = self.validate_configuration(self.current_config)
        if not is_valid:
            # Revert
            self.current_config[option_name] = option.value
            print(f"Configuration invalid: {message}")
            return False
        
        # Update option default
        option.value = value
        
        # Trigger preview if callback set
        if self.preview_callback:
            self.preview_callback(self.current_config)
        
        return True
    
    def validate_configuration(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate entire configuration."""
        for rule in self.validation_rules:
            is_valid, message = rule(config)
            if not is_valid:
                return False, message
        return True, "Configuration valid"
    
    def save_profile(self, name: str, description: str = ""):
        """Save current configuration as a profile."""
        profile = ConfigurationProfile(
            name=name,
            description=description,
            options=self.current_config.copy(),
            metadata={
                'created': datetime.now().isoformat(),
                'version': '1.0'
            }
        )
        
        self.profiles[name] = profile
        self._save_profiles_to_file()
    
    def load_profile(self, name: str) -> bool:
        """Load a configuration profile."""
        if name not in self.profiles:
            return False
        
        profile = self.profiles[name]
        
        # Validate before loading
        is_valid, message = self.validate_configuration(profile.options)
        if not is_valid:
            print(f"Profile '{name}' is invalid: {message}")
            return False
        
        self.current_config = profile.options.copy()
        
        # Update option values
        for opt_name, value in self.current_config.items():
            if opt_name in self.options:
                self.options[opt_name].value = value
        
        return True
    
    def _save_profiles_to_file(self):
        """Save custom profiles to file."""
        custom_profiles = {
            name: profile.to_dict()
            for name, profile in self.profiles.items()
            if name not in ['beginner', 'advanced_logic', 'multilingual_demo']
        }
        
        with open('config_profiles.json', 'w') as f:
            json.dump(custom_profiles, f, indent=2)
    
    def get_config_summary(self) -> str:
        """Get human-readable summary of current configuration."""
        summary = ["Current Configuration:"]
        
        for opt_name, value in self.current_config.items():
            if opt_name in self.options:
                opt = self.options[opt_name]
                summary.append(f"  {opt.description}: {value}")
        
        return "\n".join(summary)
    
    def get_affected_components(self, option_name: str) -> List[str]:
        """Get list of components affected by changing an option."""
        if option_name in self.options:
            return self.options[option_name].affects
        return []
    
    def suggest_configuration(self, goal: str) -> Dict[str, Any]:
        """Suggest configuration based on stated goal."""
        suggestions = {}
        
        goal_lower = goal.lower()
        
        if 'beginner' in goal_lower or 'easy' in goal_lower:
            suggestions = self.profiles['beginner'].options.copy()
        elif 'advanced' in goal_lower or 'difficult' in goal_lower:
            suggestions = self.profiles['advanced_logic'].options.copy()
        elif 'subtle' in goal_lower or 'tricky' in goal_lower:
            suggestions = {
                'complexity': 'advanced',
                'target_persuasiveness': 0.8,
                'semantic_coherence': 'high',
                'include_analysis': True
            }
        elif 'clear' in goal_lower or 'obvious' in goal_lower:
            suggestions = {
                'complexity': 'basic',
                'target_persuasiveness': 0.3,
                'semantic_coherence': 'low',
                'formality': 'casual'
            }
        elif 'academic' in goal_lower or 'research' in goal_lower:
            suggestions = {
                'domain': 'academic',
                'formality': 'formal',
                'complexity': 'advanced',
                'include_analysis': True,
                'output_format': 'detailed'
            }
        
        return suggestions


class ConfigurationWizard:
    """Interactive wizard for configuration."""
    
    def __init__(self, configurator: InteractiveConfigurator):
        self.configurator = configurator
        self.steps = self._init_wizard_steps()
        self.current_step = 0
        self.responses = {}
    
    def _init_wizard_steps(self) -> List[Dict[str, Any]]:
        """Initialize wizard steps."""
        return [
            {
                'name': 'purpose',
                'question': 'What is your primary purpose?',
                'options': [
                    ('teaching', 'Teaching logic to students'),
                    ('research', 'Academic research'),
                    ('practice', 'Practice identifying fallacies'),
                    ('demonstration', 'Demonstrating logical concepts'),
                    ('other', 'Other')
                ],
                'affects': ['domain', 'complexity', 'output_format']
            },
            {
                'name': 'audience',
                'question': 'Who is your target audience?',
                'options': [
                    ('beginners', 'Complete beginners'),
                    ('students', 'Logic students'),
                    ('advanced', 'Advanced learners'),
                    ('mixed', 'Mixed audience')
                ],
                'affects': ['complexity', 'formality']
            },
            {
                'name': 'difficulty',
                'question': 'How challenging should the arguments be?',
                'options': [
                    ('easy', 'Easy to distinguish'),
                    ('moderate', 'Moderately challenging'),
                    ('difficult', 'Difficult - subtle fallacies'),
                    ('variable', 'Mix of difficulties')
                ],
                'affects': ['target_persuasiveness', 'semantic_coherence']
            },
            {
                'name': 'language_choice',
                'question': 'Which language(s) do you need?',
                'options': [
                    ('english', 'English only'),
                    ('multilingual', 'Multiple languages'),
                    ('specific', 'Specific non-English language')
                ],
                'affects': ['language']
            },
            {
                'name': 'output_preference',
                'question': 'How should arguments be presented?',
                'options': [
                    ('simple', 'Simple text'),
                    ('analyzed', 'With strength analysis'),
                    ('comparative', 'Side-by-side comparison'),
                    ('quiz', 'Quiz format')
                ],
                'affects': ['output_format', 'include_analysis']
            }
        ]
    
    def start(self):
        """Start the configuration wizard."""
        print("=== Argument Generator Configuration Wizard ===\n")
        self.current_step = 0
        self.responses = {}
    
    def next_step(self) -> Optional[Dict[str, Any]]:
        """Get the next wizard step."""
        if self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            return step
        return None
    
    def process_response(self, response: str):
        """Process user response for current step."""
        if self.current_step >= len(self.steps):
            return
        
        step = self.steps[self.current_step]
        self.responses[step['name']] = response
        self.current_step += 1
    
    def finish(self) -> Dict[str, Any]:
        """Finish wizard and generate configuration."""
        config = {}
        
        # Process responses
        if self.responses.get('purpose') == 'teaching':
            config['domain'] = 'educational'
            config['output_format'] = 'educational'
        elif self.responses.get('purpose') == 'research':
            config['domain'] = 'academic'
            config['formality'] = 'formal'
        
        if self.responses.get('audience') == 'beginners':
            config['complexity'] = 'basic'
            config['semantic_coherence'] = 'high'
        elif self.responses.get('audience') == 'advanced':
            config['complexity'] = 'advanced'
        
        if self.responses.get('difficulty') == 'easy':
            config['target_persuasiveness'] = 0.3
        elif self.responses.get('difficulty') == 'difficult':
            config['target_persuasiveness'] = 0.8
            config['semantic_coherence'] = 'medium'
        
        if self.responses.get('language_choice') == 'multilingual':
            config['output_format'] = 'comparative'
        
        if self.responses.get('output_preference') == 'analyzed':
            config['include_analysis'] = True
            config['output_format'] = 'detailed'
        elif self.responses.get('output_preference') == 'quiz':
            config['output_format'] = 'quiz'
        
        return config


class ConfigurationExporter:
    """Export configurations in various formats."""
    
    def __init__(self):
        self.export_formats = ['json', 'yaml', 'ini', 'python']
    
    def export_config(self, config: Dict[str, Any], 
                     format: str = 'json') -> str:
        """Export configuration in specified format."""
        if format == 'json':
            return json.dumps(config, indent=2)
        
        elif format == 'yaml':
            # Simple YAML format
            lines = []
            for key, value in config.items():
                if isinstance(value, bool):
                    lines.append(f"{key}: {str(value).lower()}")
                elif isinstance(value, (int, float)):
                    lines.append(f"{key}: {value}")
                else:
                    lines.append(f"{key}: {value}")
            return '\n'.join(lines)
        
        elif format == 'ini':
            # INI format
            lines = ["[ArgumentGenerator]"]
            for key, value in config.items():
                lines.append(f"{key} = {value}")
            return '\n'.join(lines)
        
        elif format == 'python':
            # Python dict format
            lines = ["config = {"]
            for key, value in config.items():
                if isinstance(value, str):
                    lines.append(f"    '{key}': '{value}',")
                else:
                    lines.append(f"    '{key}': {value},")
            lines.append("}")
            return '\n'.join(lines)
        
        return ""
    
    def import_config(self, config_str: str, format: str = 'json') -> Dict[str, Any]:
        """Import configuration from string."""
        if format == 'json':
            return json.loads(config_str)
        
        # Other formats would need proper parsing
        return {}
