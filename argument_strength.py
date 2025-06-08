"""
argument_strength.py

System for analyzing and scoring argument strength, persuasiveness,
and psychological convincingness.
"""

from typing import Dict, List, Tuple, Optional, Any, Set
from dataclasses import dataclass
from enum import Enum
import re
import math


class PersuasionTechnique(Enum):
    """Common persuasion techniques used in arguments."""
    AUTHORITY = "appeal_to_authority"
    EMOTION = "emotional_appeal"
    COMMON_SENSE = "appeal_to_common_sense"
    FEAR = "fear_appeal"
    TRADITION = "appeal_to_tradition"
    NOVELTY = "appeal_to_novelty"
    POPULARITY = "appeal_to_popularity"
    CERTAINTY = "false_certainty"
    SIMPLICITY = "oversimplification"
    ANALOGY = "misleading_analogy"


@dataclass
class ArgumentStrength:
    """Comprehensive strength analysis of an argument."""
    logical_validity: float  # 0-1, based on inference rule
    semantic_plausibility: float  # 0-1, real-world likelihood
    linguistic_clarity: float  # 0-1, how clear the expression is
    persuasiveness: float  # 0-1, psychological convincingness
    sophistication: float  # 0-1, subtlety of fallacy/validity
    emotional_impact: float  # 0-1, emotional resonance
    techniques_used: List[PersuasionTechnique]
    weaknesses: List[str]
    strengths: List[str]
    overall_score: float  # Weighted combination
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'logical_validity': self.logical_validity,
            'semantic_plausibility': self.semantic_plausibility,
            'linguistic_clarity': self.linguistic_clarity,
            'persuasiveness': self.persuasiveness,
            'sophistication': self.sophistication,
            'emotional_impact': self.emotional_impact,
            'techniques_used': [t.value for t in self.techniques_used],
            'weaknesses': self.weaknesses,
            'strengths': self.strengths,
            'overall_score': self.overall_score
        }


class LinguisticAnalyzer:
    """Analyzes linguistic features that affect argument strength."""
    
    def __init__(self):
        self.clarity_indicators = self._init_clarity_indicators()
        self.hedge_words = self._init_hedge_words()
        self.certainty_markers = self._init_certainty_markers()
        self.emotional_words = self._init_emotional_words()
    
    def _init_clarity_indicators(self) -> Dict[str, float]:
        """Initialize indicators of linguistic clarity."""
        return {
            # Clear connectives
            'therefore': 0.9,
            'thus': 0.9,
            'hence': 0.85,
            'consequently': 0.9,
            'because': 0.85,
            'since': 0.8,
            
            # Less clear connectives
            'somehow': 0.3,
            'maybe': 0.4,
            'sort of': 0.3,
            'kind of': 0.3
        }
    
    def _init_hedge_words(self) -> Set[str]:
        """Words that indicate uncertainty."""
        return {
            'maybe', 'perhaps', 'possibly', 'might', 'could',
            'seems', 'appears', 'apparently', 'arguably',
            'presumably', 'supposedly', 'allegedly'
        }
    
    def _init_certainty_markers(self) -> Dict[str, float]:
        """Words that indicate (over)confidence."""
        return {
            'definitely': 0.9,
            'certainly': 0.9,
            'absolutely': 0.95,
            'undoubtedly': 0.95,
            'clearly': 0.85,
            'obviously': 0.85,
            'must': 0.8,
            'always': 0.9,
            'never': 0.9,
            'every': 0.85,
            'all': 0.85,
            'none': 0.85
        }
    
    def _init_emotional_words(self) -> Dict[str, float]:
        """Words with emotional impact."""
        return {
            # Fear
            'danger': 0.8,
            'threat': 0.8,
            'risk': 0.7,
            'harm': 0.7,
            'disaster': 0.9,
            
            # Positive emotion
            'wonderful': 0.7,
            'amazing': 0.7,
            'excellent': 0.6,
            'perfect': 0.8,
            
            # Negative emotion
            'terrible': 0.7,
            'horrible': 0.8,
            'awful': 0.7,
            'disgusting': 0.8
        }
    
    def analyze_clarity(self, text: str) -> float:
        """Analyze linguistic clarity of the argument."""
        score = 0.5  # Base score
        
        text_lower = text.lower()
        words = text_lower.split()
        
        # Check for clarity indicators
        for word, clarity_score in self.clarity_indicators.items():
            if word in text_lower:
                score = max(score, clarity_score)
        
        # Penalize hedging
        hedge_count = sum(1 for word in words if word in self.hedge_words)
        score -= hedge_count * 0.1
        
        # Bonus for structured argument markers
        if 'if' in text_lower and 'then' in text_lower:
            score += 0.1
        if 'because' in text_lower or 'since' in text_lower:
            score += 0.1
        
        # Penalize overly complex sentences
        if len(words) > 30:
            score -= 0.1
        elif len(words) < 10:
            score += 0.1
        
        return max(0, min(1, score))
    
    def detect_certainty_level(self, text: str) -> Tuple[float, bool]:
        """
        Detect certainty level and whether it's overconfident.
        Returns (certainty_score, is_overconfident)
        """
        text_lower = text.lower()
        certainty_score = 0.5
        marker_count = 0
        
        for marker, strength in self.certainty_markers.items():
            if marker in text_lower:
                certainty_score = max(certainty_score, strength)
                marker_count += 1
        
        # Multiple certainty markers suggest overconfidence
        is_overconfident = marker_count >= 2 or certainty_score > 0.9
        
        return certainty_score, is_overconfident
    
    def measure_emotional_impact(self, text: str) -> float:
        """Measure emotional impact of the text."""
        text_lower = text.lower()
        impact = 0.0
        
        for word, strength in self.emotional_words.items():
            if word in text_lower:
                impact = max(impact, strength)
        
        # Check for exclamation marks
        if '!' in text:
            impact = min(1.0, impact + 0.2)
        
        # Check for all caps words (excluding single letters)
        words = text.split()
        caps_words = [w for w in words if len(w) > 1 and w.isupper()]
        if caps_words:
            impact = min(1.0, impact + 0.1 * len(caps_words))
        
        return impact


class PersuasionAnalyzer:
    """Analyzes persuasion techniques and psychological impact."""
    
    def __init__(self):
        self.technique_patterns = self._init_technique_patterns()
        self.fallacy_persuasiveness = self._init_fallacy_persuasiveness()
    
    def _init_technique_patterns(self) -> Dict[PersuasionTechnique, List[str]]:
        """Initialize patterns for detecting persuasion techniques."""
        return {
            PersuasionTechnique.AUTHORITY: [
                'experts say', 'scientists agree', 'doctors recommend',
                'studies show', 'research proves', 'authorities confirm'
            ],
            PersuasionTechnique.EMOTION: [
                'feel', 'fear', 'love', 'hate', 'angry', 'happy',
                'sad', 'worried', 'excited', 'disgusted'
            ],
            PersuasionTechnique.COMMON_SENSE: [
                'everyone knows', 'common sense', 'obvious', 'clearly',
                'self-evident', 'goes without saying'
            ],
            PersuasionTechnique.FEAR: [
                'danger', 'risk', 'threat', 'harm', 'disaster',
                'catastrophe', 'crisis', 'emergency'
            ],
            PersuasionTechnique.TRADITION: [
                'always been', 'traditionally', 'historically',
                'ancestors', 'time-tested', 'proven over time'
            ],
            PersuasionTechnique.NOVELTY: [
                'new', 'innovative', 'cutting-edge', 'modern',
                'latest', 'revolutionary', 'breakthrough'
            ],
            PersuasionTechnique.POPULARITY: [
                'everyone', 'most people', 'majority', 'popular',
                'trending', 'viral', 'widely accepted'
            ]
        }
    
    def _init_fallacy_persuasiveness(self) -> Dict[str, float]:
        """Initialize base persuasiveness scores for fallacies."""
        return {
            'Affirming the Consequent': 0.7,  # Quite convincing
            'Denying the Antecedent': 0.6,
            'Affirming a Disjunct': 0.5,
            'False Conjunction': 0.4,
            'Composition Fallacy': 0.6,
            'False Dilemma': 0.8,  # Very convincing
            'Non Sequitur': 0.3,  # Usually obvious
            'Invalid Disjunction Elimination': 0.5
        }
    
    def detect_techniques(self, text: str) -> List[PersuasionTechnique]:
        """Detect persuasion techniques used in the text."""
        text_lower = text.lower()
        techniques = []
        
        for technique, patterns in self.technique_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    techniques.append(technique)
                    break
        
        return techniques
    
    def calculate_persuasiveness(self, text: str, rule_type: str,
                               is_valid: bool) -> float:
        """Calculate how persuasive an argument is psychologically."""
        base_score = 0.5
        
        # Valid arguments have baseline persuasiveness
        if is_valid:
            base_score = 0.6
        else:
            # Invalid arguments vary by type
            base_score = self.fallacy_persuasiveness.get(rule_type, 0.4)
        
        # Adjust based on techniques used
        techniques = self.detect_techniques(text)
        
        if PersuasionTechnique.AUTHORITY in techniques:
            base_score += 0.15
        if PersuasionTechnique.COMMON_SENSE in techniques:
            base_score += 0.1
        if PersuasionTechnique.FEAR in techniques:
            base_score += 0.2
        if PersuasionTechnique.POPULARITY in techniques:
            base_score += 0.1
        
        # Multiple techniques can be too obvious
        if len(techniques) > 3:
            base_score -= 0.1
        
        return min(1.0, base_score)
    
    def assess_sophistication(self, text: str, rule_type: str,
                            is_valid: bool) -> float:
        """Assess how sophisticated/subtle the argument is."""
        sophistication = 0.5
        
        # Some fallacies are more subtle
        subtle_fallacies = {
            'Affirming the Consequent': 0.7,
            'False Dilemma': 0.6,
            'Composition Fallacy': 0.8
        }
        
        obvious_fallacies = {
            'Non Sequitur': 0.2,
            'False Conjunction': 0.3
        }
        
        if not is_valid:
            if rule_type in subtle_fallacies:
                sophistication = subtle_fallacies[rule_type]
            elif rule_type in obvious_fallacies:
                sophistication = obvious_fallacies[rule_type]
        
        # Adjust based on linguistic features
        if 'obvious' in text.lower() or 'clearly' in text.lower():
            sophistication -= 0.1
        
        # Technical language increases sophistication
        technical_terms = ['therefore', 'hence', 'consequently', 'implies']
        tech_count = sum(1 for term in technical_terms if term in text.lower())
        sophistication += tech_count * 0.05
        
        return max(0, min(1, sophistication))


class ArgumentStrengthAnalyzer:
    """Main analyzer for comprehensive argument strength assessment."""
    
    def __init__(self, semantic_analyzer=None):
        self.linguistic_analyzer = LinguisticAnalyzer()
        self.persuasion_analyzer = PersuasionAnalyzer()
        self.semantic_analyzer = semantic_analyzer
        
        # Weights for overall score calculation
        self.weights = {
            'logical_validity': 0.25,
            'semantic_plausibility': 0.20,
            'linguistic_clarity': 0.15,
            'persuasiveness': 0.20,
            'sophistication': 0.10,
            'emotional_impact': 0.10
        }
    
    def analyze_argument(self, argument_text: str, rule_type: str,
                        is_valid: bool, 
                        semantic_score: Optional[float] = None) -> ArgumentStrength:
        """Perform comprehensive strength analysis of an argument."""
        
        # Logical validity
        logical_validity = 1.0 if is_valid else 0.0
        
        # Semantic plausibility
        if semantic_score is not None:
            semantic_plausibility = semantic_score
        else:
            # Default based on validity
            semantic_plausibility = 0.7 if is_valid else 0.4
        
        # Linguistic clarity
        linguistic_clarity = self.linguistic_analyzer.analyze_clarity(argument_text)
        
        # Certainty analysis
        certainty, overconfident = self.linguistic_analyzer.detect_certainty_level(argument_text)
        
        # Emotional impact
        emotional_impact = self.linguistic_analyzer.measure_emotional_impact(argument_text)
        
        # Persuasion analysis
        techniques = self.persuasion_analyzer.detect_techniques(argument_text)
        persuasiveness = self.persuasion_analyzer.calculate_persuasiveness(
            argument_text, rule_type, is_valid
        )
        
        # Sophistication
        sophistication = self.persuasion_analyzer.assess_sophistication(
            argument_text, rule_type, is_valid
        )
        
        # Identify strengths and weaknesses
        strengths = []
        weaknesses = []
        
        # Logical analysis
        if is_valid:
            strengths.append("Logically valid inference")
        else:
            weaknesses.append(f"Commits {rule_type} fallacy")
        
        # Clarity analysis
        if linguistic_clarity > 0.7:
            strengths.append("Clear and well-structured")
        elif linguistic_clarity < 0.4:
            weaknesses.append("Unclear or confusing structure")
        
        # Plausibility analysis
        if semantic_plausibility > 0.7:
            strengths.append("Highly plausible in real world")
        elif semantic_plausibility < 0.3:
            weaknesses.append("Implausible or unrealistic")
        
        # Persuasion analysis
        if persuasiveness > 0.7 and not is_valid:
            weaknesses.append("Persuasive but logically flawed")
        elif persuasiveness > 0.7 and is_valid:
            strengths.append("Both valid and persuasive")
        
        # Certainty analysis
        if overconfident:
            weaknesses.append("Uses overconfident language")
        
        # Sophistication analysis
        if sophistication > 0.7 and not is_valid:
            weaknesses.append("Subtle fallacy - hard to detect")
        elif sophistication > 0.7 and is_valid:
            strengths.append("Sophisticated reasoning")
        
        # Calculate overall score
        overall_score = (
            self.weights['logical_validity'] * logical_validity +
            self.weights['semantic_plausibility'] * semantic_plausibility +
            self.weights['linguistic_clarity'] * linguistic_clarity +
            self.weights['persuasiveness'] * persuasiveness +
            self.weights['sophistication'] * sophistication +
            self.weights['emotional_impact'] * emotional_impact
        )
        
        return ArgumentStrength(
            logical_validity=logical_validity,
            semantic_plausibility=semantic_plausibility,
            linguistic_clarity=linguistic_clarity,
            persuasiveness=persuasiveness,
            sophistication=sophistication,
            emotional_impact=emotional_impact,
            techniques_used=techniques,
            weaknesses=weaknesses,
            strengths=strengths,
            overall_score=overall_score
        )
    
    def compare_arguments(self, arg1: ArgumentStrength, 
                         arg2: ArgumentStrength) -> Dict[str, Any]:
        """Compare two arguments and identify key differences."""
        comparison = {
            'stronger_overall': 1 if arg1.overall_score > arg2.overall_score else 2,
            'score_difference': abs(arg1.overall_score - arg2.overall_score),
            'key_differences': []
        }
        
        # Find largest differences
        metrics = [
            ('logical_validity', arg1.logical_validity, arg2.logical_validity),
            ('semantic_plausibility', arg1.semantic_plausibility, arg2.semantic_plausibility),
            ('linguistic_clarity', arg1.linguistic_clarity, arg2.linguistic_clarity),
            ('persuasiveness', arg1.persuasiveness, arg2.persuasiveness),
            ('sophistication', arg1.sophistication, arg2.sophistication)
        ]
        
        for metric, val1, val2 in metrics:
            diff = abs(val1 - val2)
            if diff > 0.3:
                if val1 > val2:
                    comparison['key_differences'].append(
                        f"Argument 1 has higher {metric} ({val1:.2f} vs {val2:.2f})"
                    )
                else:
                    comparison['key_differences'].append(
                        f"Argument 2 has higher {metric} ({val2:.2f} vs {val1:.2f})"
                    )
        
        return comparison
    
    def generate_feedback(self, strength: ArgumentStrength) -> str:
        """Generate human-readable feedback about argument strength."""
        feedback = []
        
        # Overall assessment
        if strength.overall_score > 0.8:
            feedback.append("This is a very strong argument.")
        elif strength.overall_score > 0.6:
            feedback.append("This is a moderately strong argument.")
        elif strength.overall_score > 0.4:
            feedback.append("This argument has some weaknesses.")
        else:
            feedback.append("This is a weak argument.")
        
        # Specific strengths
        if strength.strengths:
            feedback.append(f"Strengths: {', '.join(strength.strengths)}.")
        
        # Specific weaknesses
        if strength.weaknesses:
            feedback.append(f"Weaknesses: {', '.join(strength.weaknesses)}.")
        
        # Persuasion techniques
        if strength.techniques_used:
            techniques_str = ', '.join(t.value.replace('_', ' ') 
                                     for t in strength.techniques_used)
            feedback.append(f"Uses: {techniques_str}.")
        
        # Recommendations
        if strength.logical_validity < 1.0:
            feedback.append("Consider the logical structure more carefully.")
        if strength.linguistic_clarity < 0.5:
            feedback.append("Try to express the argument more clearly.")
        if strength.semantic_plausibility < 0.5:
            feedback.append("The conclusion doesn't follow naturally from the premises.")
        
        return " ".join(feedback)


class ArgumentDifficultyCalibrator:
    """Calibrates argument difficulty for educational purposes."""
    
    def __init__(self):
        self.difficulty_factors = {
            'subtlety': 0.3,      # How subtle the fallacy is
            'complexity': 0.2,    # Linguistic complexity
            'similarity': 0.2,    # How similar valid/invalid look
            'plausibility': 0.2,  # Real-world plausibility
            'length': 0.1         # Argument length
        }
    
    def calculate_difficulty(self, valid_arg: str, invalid_arg: str,
                           valid_strength: ArgumentStrength,
                           invalid_strength: ArgumentStrength) -> float:
        """Calculate how difficult it is to distinguish valid from invalid."""
        
        # Subtlety factor
        subtlety = invalid_strength.sophistication
        
        # Complexity factor
        complexity = (len(valid_arg.split()) + len(invalid_arg.split())) / 60
        complexity = min(1.0, complexity)
        
        # Similarity factor (how close the persuasiveness scores are)
        similarity = 1.0 - abs(valid_strength.persuasiveness - 
                              invalid_strength.persuasiveness)
        
        # Plausibility factor
        plausibility = (valid_strength.semantic_plausibility + 
                       invalid_strength.semantic_plausibility) / 2
        
        # Length factor
        avg_length = (len(valid_arg) + len(invalid_arg)) / 2
        length_factor = min(1.0, avg_length / 200)
        
        # Calculate weighted difficulty
        difficulty = (
            self.difficulty_factors['subtlety'] * subtlety +
            self.difficulty_factors['complexity'] * complexity +
            self.difficulty_factors['similarity'] * similarity +
            self.difficulty_factors['plausibility'] * plausibility +
            self.difficulty_factors['length'] * length_factor
        )
        
        return difficulty
    
    def categorize_difficulty(self, difficulty_score: float) -> str:
        """Categorize difficulty level."""
        if difficulty_score < 0.3:
            return "Easy"
        elif difficulty_score < 0.5:
            return "Medium"
        elif difficulty_score < 0.7:
            return "Hard"
        else:
            return "Expert"
    
    def generate_difficulty_explanation(self, valid_arg: str, invalid_arg: str,
                                      difficulty_score: float,
                                      valid_strength: ArgumentStrength,
                                      invalid_strength: ArgumentStrength) -> str:
        """Explain why an argument pair has a certain difficulty."""
        
        level = self.categorize_difficulty(difficulty_score)
        explanation = [f"This is a {level} argument pair to evaluate."]
        
        # Explain contributing factors
        if invalid_strength.sophistication > 0.7:
            explanation.append("The fallacy is quite subtle and hard to spot.")
        
        if abs(valid_strength.persuasiveness - invalid_strength.persuasiveness) < 0.2:
            explanation.append("Both arguments are similarly persuasive.")
        
        if invalid_strength.semantic_plausibility > 0.7:
            explanation.append("The invalid argument seems plausible in real life.")
        
        if len(valid_arg.split()) > 30 or len(invalid_arg.split()) > 30:
            explanation.append("The arguments are complex and lengthy.")
        
        if invalid_strength.persuasiveness > valid_strength.persuasiveness:
            explanation.append("The invalid argument is actually more persuasive!")
        
        return " ".join(explanation)