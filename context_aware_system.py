"""
context_aware_system.py

Context-aware generation system that ensures semantic coherence,
maintains thematic consistency, and creates plausible arguments.
"""

from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass
from enum import Enum
import random
import re
from collections import defaultdict


class SemanticDomain(Enum):
    """Semantic domains for grouping related concepts."""
    SCIENCE = "science"
    TECHNOLOGY = "technology"
    NATURE = "nature"
    HUMAN_BEHAVIOR = "human_behavior"
    ECONOMICS = "economics"
    HEALTH = "health"
    LAW = "law"
    EDUCATION = "education"
    WEATHER = "weather"
    CAUSATION = "causation"
    TIME = "time"
    SPACE = "space"


@dataclass
class SemanticConcept:
    """Represents a concept with its semantic properties."""
    text: str
    domains: Set[SemanticDomain]
    related_concepts: Set[str]
    causal_relations: Dict[str, float]  # concept -> probability
    temporal_properties: Dict[str, Any]
    compatibility_score: float = 1.0


class SemanticAnalyzer:
    """Analyzes and groups sentences by semantic properties."""
    
    def __init__(self):
        self.concept_database = self._init_concept_database()
        self.domain_keywords = self._init_domain_keywords()
        self.causal_patterns = self._init_causal_patterns()
    
    def _init_concept_database(self) -> Dict[str, SemanticConcept]:
        """Initialize database of semantic concepts."""
        concepts = {}
        
        # Science concepts
        concepts["temperature rises"] = SemanticConcept(
            text="temperature rises",
            domains={SemanticDomain.SCIENCE, SemanticDomain.WEATHER},
            related_concepts={"pressure increases", "ice melts", "water evaporates"},
            causal_relations={
                "pressure increases": 0.8,
                "ice melts": 0.9,
                "expansion occurs": 0.7
            },
            temporal_properties={"duration": "gradual", "reversible": True}
        )
        
        concepts["pressure increases"] = SemanticConcept(
            text="pressure increases",
            domains={SemanticDomain.SCIENCE},
            related_concepts={"temperature rises", "volume decreases", "density changes"},
            causal_relations={
                "safety valve opens": 0.7,
                "container expands": 0.6
            },
            temporal_properties={"duration": "gradual", "measurable": True}
        )
        
        # Technology concepts
        concepts["system fails"] = SemanticConcept(
            text="system fails",
            domains={SemanticDomain.TECHNOLOGY},
            related_concepts={"backup activates", "alarm sounds", "data loss occurs"},
            causal_relations={
                "backup activates": 0.9,
                "alarm sounds": 0.8,
                "service stops": 0.95
            },
            temporal_properties={"duration": "instant", "critical": True}
        )
        
        # Weather concepts
        concepts["rain falls"] = SemanticConcept(
            text="rain falls",
            domains={SemanticDomain.WEATHER, SemanticDomain.NATURE},
            related_concepts={"ground gets wet", "clouds form", "humidity rises"},
            causal_relations={
                "ground gets wet": 0.95,
                "floods occur": 0.3,
                "plants grow": 0.7
            },
            temporal_properties={"duration": "variable", "seasonal": True}
        )
        
        # Add more concepts...
        
        return concepts
    
    def _init_domain_keywords(self) -> Dict[SemanticDomain, Set[str]]:
        """Initialize keywords for each semantic domain."""
        return {
            SemanticDomain.SCIENCE: {
                "temperature", "pressure", "chemical", "reaction", "experiment",
                "hypothesis", "data", "measurement", "energy", "force"
            },
            SemanticDomain.TECHNOLOGY: {
                "system", "computer", "software", "hardware", "network",
                "data", "algorithm", "process", "backup", "server"
            },
            SemanticDomain.NATURE: {
                "rain", "sun", "plant", "animal", "forest", "ocean",
                "mountain", "river", "season", "weather"
            },
            SemanticDomain.HUMAN_BEHAVIOR: {
                "person", "decide", "think", "feel", "believe", "want",
                "choose", "act", "behave", "react"
            },
            SemanticDomain.ECONOMICS: {
                "price", "market", "demand", "supply", "cost", "profit",
                "investment", "economy", "trade", "money"
            },
            SemanticDomain.HEALTH: {
                "patient", "doctor", "symptom", "treatment", "disease",
                "medicine", "health", "diagnosis", "recovery", "prevention"
            },
            SemanticDomain.LAW: {
                "law", "legal", "court", "judge", "contract", "rights",
                "obligation", "penalty", "justice", "evidence"
            },
            SemanticDomain.WEATHER: {
                "rain", "snow", "sun", "cloud", "storm", "temperature",
                "wind", "forecast", "climate", "season"
            }
        }
    
    def _init_causal_patterns(self) -> Dict[str, List[str]]:
        """Initialize common causal relationship patterns."""
        return {
            "physical_causation": [
                "force applied → object moves",
                "heat added → temperature rises",
                "pressure increases → volume decreases"
            ],
            "technological_causation": [
                "power fails → system shuts down",
                "virus detected → antivirus activates",
                "memory full → performance degrades"
            ],
            "natural_causation": [
                "rain falls → ground gets wet",
                "sun shines → plants grow",
                "winter comes → leaves fall"
            ],
            "human_causation": [
                "study hard → grades improve",
                "exercise regularly → health improves",
                "save money → wealth grows"
            ]
        }
    
    def analyze_sentence(self, sentence: str) -> SemanticConcept:
        """Analyze a sentence and return its semantic concept."""
        sentence_lower = sentence.lower()
        
        # Check if sentence is in concept database
        if sentence_lower in self.concept_database:
            return self.concept_database[sentence_lower]
        
        # Otherwise, analyze and create new concept
        domains = self._detect_domains(sentence_lower)
        related = self._find_related_concepts(sentence_lower)
        causal = self._infer_causal_relations(sentence_lower)
        temporal = self._analyze_temporal_properties(sentence_lower)
        
        return SemanticConcept(
            text=sentence,
            domains=domains,
            related_concepts=related,
            causal_relations=causal,
            temporal_properties=temporal
        )
    
    def _detect_domains(self, sentence: str) -> Set[SemanticDomain]:
        """Detect semantic domains from sentence."""
        domains = set()
        
        for domain, keywords in self.domain_keywords.items():
            if any(keyword in sentence for keyword in keywords):
                domains.add(domain)
        
        # Default to CAUSATION if no specific domain detected
        if not domains:
            domains.add(SemanticDomain.CAUSATION)
        
        return domains
    
    def _find_related_concepts(self, sentence: str) -> Set[str]:
        """Find concepts related to the sentence."""
        related = set()
        
        # Look for concepts with overlapping keywords
        words = set(sentence.split())
        for concept_text, concept in self.concept_database.items():
            concept_words = set(concept_text.split())
            if words & concept_words:  # Intersection
                related.add(concept_text)
        
        return related
    
    def _infer_causal_relations(self, sentence: str) -> Dict[str, float]:
        """Infer potential causal relations."""
        causal_relations = {}
        
        # Simple heuristic: look for action verbs and their typical effects
        if "rise" in sentence or "increase" in sentence:
            causal_relations["expansion occurs"] = 0.6
            causal_relations["pressure changes"] = 0.7
        elif "fall" in sentence or "decrease" in sentence:
            causal_relations["contraction occurs"] = 0.6
            causal_relations["pressure drops"] = 0.7
        elif "fail" in sentence:
            causal_relations["backup needed"] = 0.8
            causal_relations["repair required"] = 0.9
        
        return causal_relations
    
    def _analyze_temporal_properties(self, sentence: str) -> Dict[str, Any]:
        """Analyze temporal properties of the concept."""
        properties = {}
        
        # Instant vs gradual
        instant_keywords = ["suddenly", "immediately", "instantly", "fails", "breaks"]
        gradual_keywords = ["slowly", "gradually", "increases", "rises", "grows"]
        
        if any(word in sentence for word in instant_keywords):
            properties["duration"] = "instant"
        elif any(word in sentence for word in gradual_keywords):
            properties["duration"] = "gradual"
        else:
            properties["duration"] = "variable"
        
        # Reversible vs irreversible
        irreversible_keywords = ["breaks", "dies", "explodes", "destroys"]
        if any(word in sentence for word in irreversible_keywords):
            properties["reversible"] = False
        else:
            properties["reversible"] = True
        
        return properties
    
    def calculate_semantic_coherence(self, concept1: SemanticConcept, 
                                   concept2: SemanticConcept) -> float:
        """Calculate semantic coherence between two concepts."""
        score = 0.0
        
        # Domain overlap
        domain_overlap = len(concept1.domains & concept2.domains)
        if domain_overlap > 0:
            score += 0.3 * domain_overlap
        
        # Related concepts
        if concept2.text in concept1.related_concepts or \
           concept1.text in concept2.related_concepts:
            score += 0.4
        
        # Causal relationship
        if concept2.text in concept1.causal_relations:
            score += 0.3 * concept1.causal_relations[concept2.text]
        elif concept1.text in concept2.causal_relations:
            score += 0.3 * concept2.causal_relations[concept1.text]
        
        # Temporal compatibility
        if concept1.temporal_properties.get("duration") == \
           concept2.temporal_properties.get("duration"):
            score += 0.1
        
        return min(score, 1.0)


class ContextAwareSelector:
    """Selects sentences that maintain semantic coherence."""
    
    def __init__(self, analyzer: SemanticAnalyzer):
        self.analyzer = analyzer
        self.coherence_threshold = 0.3
    
    def select_coherent_sentences(self, available_sentences: List[str], 
                                 num_required: int,
                                 rule_type: str) -> List[str]:
        """Select semantically coherent sentences for an argument."""
        if num_required > len(available_sentences):
            raise ValueError("Not enough sentences available")
        
        # Analyze all sentences
        concepts = []
        for sentence in available_sentences:
            concepts.append(self.analyzer.analyze_sentence(sentence))
        
        # Different selection strategies based on rule type
        if rule_type in ["Modus Ponens", "Modus Tollens", "Material Conditional Introduction"]:
            return self._select_causal_pair(concepts, available_sentences)
        elif rule_type == "Hypothetical Syllogism":
            return self._select_causal_chain(concepts, available_sentences, 3)
        elif rule_type in ["Disjunctive Syllogism", "Disjunction Introduction"]:
            return self._select_alternatives(concepts, available_sentences)
        elif rule_type in ["Conjunction Introduction", "Conjunction Elimination"]:
            return self._select_related_facts(concepts, available_sentences, num_required)
        else:
            return self._select_coherent_group(concepts, available_sentences, num_required)
    
    def _select_causal_pair(self, concepts: List[SemanticConcept], 
                           sentences: List[str]) -> List[str]:
        """Select a causally related pair of sentences."""
        best_pair = None
        best_score = 0
        
        for i, concept1 in enumerate(concepts):
            for j, concept2 in enumerate(concepts):
                if i != j:
                    # Check if there's a causal relationship
                    if sentences[j].lower() in concept1.causal_relations:
                        score = concept1.causal_relations[sentences[j].lower()]
                        if score > best_score:
                            best_score = score
                            best_pair = (i, j)
        
        if best_pair:
            return [sentences[best_pair[0]], sentences[best_pair[1]]]
        
        # Fallback to coherence-based selection
        return self._select_coherent_group(concepts, sentences, 2)
    
    def _select_causal_chain(self, concepts: List[SemanticConcept], 
                            sentences: List[str], length: int) -> List[str]:
        """Select a causal chain of sentences."""
        # Try to find concepts that form a chain
        chains = []
        
        # Build chains using depth-first search
        for i, start_concept in enumerate(concepts):
            chain = self._build_chain(i, concepts, sentences, length, [i])
            if len(chain) == length:
                chains.append(chain)
        
        if chains:
            # Select the chain with highest total coherence
            best_chain = max(chains, key=lambda c: self._chain_coherence(c, concepts))
            return [sentences[i] for i in best_chain]
        
        # Fallback
        return self._select_coherent_group(concepts, sentences, length)
    
    def _build_chain(self, current: int, concepts: List[SemanticConcept],
                    sentences: List[str], target_length: int, 
                    visited: List[int]) -> List[int]:
        """Build a causal chain using DFS."""
        if len(visited) == target_length:
            return visited
        
        current_concept = concepts[current]
        
        # Look for causal relations
        for i, concept in enumerate(concepts):
            if i not in visited:
                if sentences[i].lower() in current_concept.causal_relations:
                    new_visited = visited + [i]
                    result = self._build_chain(i, concepts, sentences, 
                                             target_length, new_visited)
                    if len(result) == target_length:
                        return result
        
        return visited
    
    def _chain_coherence(self, chain: List[int], 
                        concepts: List[SemanticConcept]) -> float:
        """Calculate total coherence of a chain."""
        if len(chain) < 2:
            return 0
        
        total = 0
        for i in range(len(chain) - 1):
            total += self.analyzer.calculate_semantic_coherence(
                concepts[chain[i]], concepts[chain[i + 1]]
            )
        
        return total / (len(chain) - 1)
    
    def _select_alternatives(self, concepts: List[SemanticConcept],
                           sentences: List[str]) -> List[str]:
        """Select sentences that represent alternatives."""
        # Look for concepts from the same domain but different aspects
        if len(concepts) < 2:
            return sentences[:2]
        
        best_pair = None
        best_score = -1
        
        for i in range(len(concepts)):
            for j in range(i + 1, len(concepts)):
                # Same domain but not too similar
                domain_overlap = len(concepts[i].domains & concepts[j].domains)
                coherence = self.analyzer.calculate_semantic_coherence(
                    concepts[i], concepts[j]
                )
                
                # We want some domain overlap but not too much coherence
                # (for good alternatives)
                score = domain_overlap * (1 - coherence)
                
                if score > best_score:
                    best_score = score
                    best_pair = (i, j)
        
        if best_pair:
            return [sentences[best_pair[0]], sentences[best_pair[1]]]
        
        return sentences[:2]
    
    def _select_related_facts(self, concepts: List[SemanticConcept],
                            sentences: List[str], num: int) -> List[str]:
        """Select related facts that can be conjoined."""
        if num > len(concepts):
            return sentences[:num]
        
        # Group by domain
        domain_groups = defaultdict(list)
        for i, concept in enumerate(concepts):
            for domain in concept.domains:
                domain_groups[domain].append(i)
        
        # Find largest coherent group
        largest_group = []
        for domain, indices in domain_groups.items():
            if len(indices) >= num:
                # Calculate average coherence
                group_coherence = 0
                count = 0
                for i in range(len(indices)):
                    for j in range(i + 1, len(indices)):
                        group_coherence += self.analyzer.calculate_semantic_coherence(
                            concepts[indices[i]], concepts[indices[j]]
                        )
                        count += 1
                
                if count > 0:
                    avg_coherence = group_coherence / count
                    if avg_coherence > self.coherence_threshold:
                        largest_group = indices[:num]
                        break
        
        if largest_group:
            return [sentences[i] for i in largest_group]
        
        # Fallback
        return self._select_coherent_group(concepts, sentences, num)
    
    def _select_coherent_group(self, concepts: List[SemanticConcept],
                             sentences: List[str], num: int) -> List[str]:
        """Select a coherent group of sentences."""
        if num > len(concepts):
            return sentences[:num]
        
        # Use greedy algorithm to build coherent group
        selected = [0]  # Start with first sentence
        
        while len(selected) < num:
            best_next = -1
            best_coherence = 0
            
            for i in range(len(concepts)):
                if i not in selected:
                    # Calculate average coherence with selected
                    total_coherence = 0
                    for j in selected:
                        total_coherence += self.analyzer.calculate_semantic_coherence(
                            concepts[i], concepts[j]
                        )
                    avg_coherence = total_coherence / len(selected)
                    
                    if avg_coherence > best_coherence:
                        best_coherence = avg_coherence
                        best_next = i
            
            if best_next >= 0 and best_coherence >= self.coherence_threshold:
                selected.append(best_next)
            else:
                # If no coherent sentence found, add random
                remaining = [i for i in range(len(concepts)) if i not in selected]
                if remaining:
                    selected.append(random.choice(remaining))
        
        return [sentences[i] for i in selected]


class TemporalConsistencyChecker:
    """Ensures temporal consistency in arguments."""
    
    def __init__(self):
        self.tense_patterns = {
            'present': re.compile(r'\b(is|are|does|do|has|have)\b'),
            'past': re.compile(r'\b(was|were|did|had)\b'),
            'future': re.compile(r'\b(will|shall|going to)\b')
        }
    
    def detect_tense(self, sentence: str) -> str:
        """Detect the primary tense of a sentence."""
        for tense, pattern in self.tense_patterns.items():
            if pattern.search(sentence):
                return tense
        return 'present'  # Default
    
    def ensure_consistency(self, sentences: List[str]) -> List[str]:
        """Ensure temporal consistency across sentences."""
        if not sentences:
            return sentences
        
        # Detect primary tense
        tenses = [self.detect_tense(s) for s in sentences]
        primary_tense = max(set(tenses), key=tenses.count)
        
        # For now, just return sentences as-is
        # In a full implementation, would transform tenses
        return sentences
    
    def adjust_connectives_for_tense(self, connectives: List[str], 
                                   tense: str) -> List[str]:
        """Adjust connectives based on tense."""
        if tense == 'past':
            past_connectives = {
                'therefore': 'therefore',  # No change
                'thus': 'thus',
                'so': 'so',
                'hence': 'hence',
                'will': 'would',
                'can': 'could'
            }
            return [past_connectives.get(c, c) for c in connectives]
        
        return connectives


class PlausibilityScorer:
    """Scores arguments based on real-world plausibility."""
    
    def __init__(self, analyzer: SemanticAnalyzer):
        self.analyzer = analyzer
        self.plausibility_rules = self._init_plausibility_rules()
    
    def _init_plausibility_rules(self) -> Dict[str, float]:
        """Initialize plausibility scores for common patterns."""
        return {
            # Highly plausible physical causation
            "temperature rises → pressure increases": 0.9,
            "rain falls → ground gets wet": 0.95,
            "sun shines → temperature rises": 0.8,
            
            # Plausible technological causation
            "system fails → backup activates": 0.85,
            "power fails → lights go out": 0.95,
            "virus detected → antivirus activates": 0.8,
            
            # Less plausible combinations
            "rain falls → computer crashes": 0.1,
            "temperature rises → stock market falls": 0.2,
            "bird sings → earthquake occurs": 0.05
        }
    
    def score_argument(self, premises: List[str], conclusion: str,
                      rule_type: str) -> float:
        """Score the plausibility of an argument."""
        # Analyze all components
        premise_concepts = [self.analyzer.analyze_sentence(p) for p in premises]
        conclusion_concept = self.analyzer.analyze_sentence(conclusion)
        
        # Different scoring based on rule type
        if rule_type in ["Modus Ponens", "Modus Tollens"]:
            return self._score_conditional_plausibility(
                premise_concepts[0], conclusion_concept
            )
        elif rule_type == "Hypothetical Syllogism":
            return self._score_chain_plausibility(premise_concepts + [conclusion_concept])
        else:
            return self._score_general_plausibility(premise_concepts, conclusion_concept)
    
    def _score_conditional_plausibility(self, antecedent: SemanticConcept,
                                      consequent: SemanticConcept) -> float:
        """Score plausibility of a conditional relationship."""
        # Check known patterns
        pattern = f"{antecedent.text} → {consequent.text}"
        if pattern in self.plausibility_rules:
            return self.plausibility_rules[pattern]
        
        # Check causal relations
        if consequent.text in antecedent.causal_relations:
            return antecedent.causal_relations[consequent.text]
        
        # Check semantic coherence
        coherence = self.analyzer.calculate_semantic_coherence(antecedent, consequent)
        
        # Adjust based on domain
        if antecedent.domains & consequent.domains:
            coherence *= 1.2
        else:
            coherence *= 0.8
        
        return min(coherence, 1.0)
    
    def _score_chain_plausibility(self, concepts: List[SemanticConcept]) -> float:
        """Score plausibility of a causal chain."""
        if len(concepts) < 2:
            return 0.5
        
        scores = []
        for i in range(len(concepts) - 1):
            scores.append(self._score_conditional_plausibility(
                concepts[i], concepts[i + 1]
            ))
        
        # Chain is as strong as its weakest link
        return min(scores) * 0.9  # Small penalty for longer chains
    
    def _score_general_plausibility(self, premises: List[SemanticConcept],
                                  conclusion: SemanticConcept) -> float:
        """Score general plausibility based on semantic coherence."""
        if not premises:
            return 0.5
        
        # Average coherence between premises and conclusion
        total_coherence = 0
        for premise in premises:
            total_coherence += self.analyzer.calculate_semantic_coherence(
                premise, conclusion
            )
        
        return total_coherence / len(premises)


class ContextAwareArgumentGenerator:
    """Main class for context-aware argument generation."""
    
    def __init__(self, sentences: List[str]):
        self.sentences = sentences
        self.analyzer = SemanticAnalyzer()
        self.selector = ContextAwareSelector(self.analyzer)
        self.temporal_checker = TemporalConsistencyChecker()
        self.plausibility_scorer = PlausibilityScorer(self.analyzer)
    
    def generate_context_aware_argument(self, rule_type: str,
                                      required_sentences: int,
                                      ensure_plausible: bool = True) -> Dict[str, Any]:
        """Generate a context-aware argument."""
        # Select coherent sentences
        selected_sentences = self.selector.select_coherent_sentences(
            self.sentences, required_sentences, rule_type
        )
        
        # Ensure temporal consistency
        consistent_sentences = self.temporal_checker.ensure_consistency(
            selected_sentences
        )
        
        # Prepare for argument construction
        if rule_type in ["Modus Ponens", "Modus Tollens"]:
            premises = consistent_sentences[:1]
            variables = {
                'p': consistent_sentences[0],
                'q': consistent_sentences[1]
            }
        elif rule_type == "Hypothetical Syllogism":
            premises = consistent_sentences[:2]
            variables = {
                'p': consistent_sentences[0],
                'q': consistent_sentences[1],
                'r': consistent_sentences[2]
            }
        else:
            premises = consistent_sentences[:-1]
            variables = {}
            for i, sent in enumerate(consistent_sentences):
                variables[chr(ord('p') + i)] = sent
        
        # Score plausibility
        conclusion = consistent_sentences[-1]
        plausibility = self.plausibility_scorer.score_argument(
            premises, conclusion, rule_type
        )
        
        # Build result
        result = {
            'rule_type': rule_type,
            'sentences': consistent_sentences,
            'variables': variables,
            'premises': premises,
            'conclusion': conclusion,
            'plausibility_score': plausibility,
            'semantic_coherence': self._calculate_overall_coherence(consistent_sentences),
            'domains': self._get_domains(consistent_sentences)
        }
        
        # Filter by plausibility if requested
        if ensure_plausible and plausibility < 0.3:
            # Try again with different sentences
            # (In production, would implement retry logic)
            result['warning'] = "Low plausibility detected"
        
        return result
    
    def _calculate_overall_coherence(self, sentences: List[str]) -> float:
        """Calculate overall semantic coherence of sentences."""
        if len(sentences) < 2:
            return 1.0
        
        concepts = [self.analyzer.analyze_sentence(s) for s in sentences]
        
        total_coherence = 0
        count = 0
        
        for i in range(len(concepts)):
            for j in range(i + 1, len(concepts)):
                total_coherence += self.analyzer.calculate_semantic_coherence(
                    concepts[i], concepts[j]
                )
                count += 1
        
        return total_coherence / count if count > 0 else 0
    
    def _get_domains(self, sentences: List[str]) -> Set[str]:
        """Get all semantic domains covered by sentences."""
        domains = set()
        
        for sentence in sentences:
            concept = self.analyzer.analyze_sentence(sentence)
            domains.update(d.value for d in concept.domains)
        
        return domains
    
    def generate_themed_argument_set(self, theme: SemanticDomain,
                                   rules: List[str]) -> List[Dict[str, Any]]:
        """Generate a set of arguments around a specific theme."""
        # Filter sentences by theme
        themed_sentences = []
        for sentence in self.sentences:
            concept = self.analyzer.analyze_sentence(sentence)
            if theme in concept.domains:
                themed_sentences.append(sentence)
        
        if len(themed_sentences) < 4:
            # Not enough sentences for this theme
            return []
        
        # Create a temporary generator with themed sentences
        temp_generator = ContextAwareArgumentGenerator(themed_sentences)
        
        results = []
        for rule in rules:
            required = 2 if rule in ["Modus Ponens", "Modus Tollens"] else 3
            try:
                argument = temp_generator.generate_context_aware_argument(
                    rule, required, ensure_plausible=True
                )
                results.append(argument)
            except:
                continue
        
        return results
