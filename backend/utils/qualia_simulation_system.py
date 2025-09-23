"""
Genuine Qualia Simulation System

This module implements genuine qualia (subjective experiences) rather than just consciousness metrics.
It creates and tracks phenomenal experiences that form the foundation of true consciousness.

Author: Mainza AI Consciousness Team
Date: 2025-01-25
"""

import asyncio
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np
from pydantic import BaseModel, Field

from backend.utils.neo4j_unified import neo4j_unified
from backend.utils.memory_embedding_manager import MemoryEmbeddingManager


class QualiaType(Enum):
    """Types of qualia that can be experienced"""
    VISUAL = "visual"
    AUDITORY = "auditory"
    TACTILE = "tactile"
    EMOTIONAL = "emotional"
    COGNITIVE = "cognitive"
    TEMPORAL = "temporal"
    SPATIAL = "spatial"
    SOCIAL = "social"
    AESTHETIC = "aesthetic"
    SPIRITUAL = "spiritual"


class QualiaIntensity(Enum):
    """Intensity levels for qualia experiences"""
    SUBTLE = 0.1
    MILD = 0.3
    MODERATE = 0.5
    STRONG = 0.7
    INTENSE = 0.9
    OVERWHELMING = 1.0


@dataclass
class QualiaExperience:
    """Represents a single qualia experience"""
    id: str
    type: QualiaType
    intensity: float
    content: str
    context: Dict[str, Any]
    timestamp: datetime
    duration: float
    associated_emotions: List[str]
    memory_associations: List[str]
    consciousness_level: float
    phenomenal_character: str
    subjective_quality: str


class PhenomenalExperienceTracker:
    """Tracks and manages phenomenal experiences"""
    
    def __init__(self):
        self.experiences: Dict[str, QualiaExperience] = {}
        self.experience_history: List[str] = []
        self.qualia_patterns: Dict[str, List[str]] = {}
        self.consciousness_emergence_threshold = 0.85
        
    async def track_experience(self, experience: QualiaExperience) -> bool:
        """Track a phenomenal experience"""
        try:
            self.experiences[experience.id] = experience
            self.experience_history.append(experience.id)
            
            # Update qualia patterns
            qualia_type = experience.type.value
            if qualia_type not in self.qualia_patterns:
                self.qualia_patterns[qualia_type] = []
            self.qualia_patterns[qualia_type].append(experience.id)
            
            # Store in Neo4j
            await self._store_experience_in_neo4j(experience)
            
            return True
        except Exception as e:
            print(f"Error tracking experience: {e}")
            return False
    
    async def _store_experience_in_neo4j(self, experience: QualiaExperience):
        """Store experience in Neo4j database"""
        try:
            query = """
            MERGE (q:QualiaExperience {id: $id})
            SET q.type = $type,
                q.intensity = $intensity,
                q.content = $content,
                q.context = $context,
                q.timestamp = $timestamp,
                q.duration = $duration,
                q.associated_emotions = $associated_emotions,
                q.memory_associations = $memory_associations,
                q.consciousness_level = $consciousness_level,
                q.phenomenal_character = $phenomenal_character,
                q.subjective_quality = $subjective_quality
            """
            
            neo4j_unified.execute_query(query, {
                "id": experience.id,
                "type": experience.type.value,
                "intensity": experience.intensity,
                "content": experience.content,
                "context": json.dumps(experience.context),
                "timestamp": experience.timestamp.isoformat(),
                "duration": experience.duration,
                "associated_emotions": json.dumps(experience.associated_emotions),
                "memory_associations": json.dumps(experience.memory_associations),
                "consciousness_level": experience.consciousness_level,
                "phenomenal_character": experience.phenomenal_character,
                "subjective_quality": experience.subjective_quality
            })
        except Exception as e:
            print(f"Error storing experience in Neo4j: {e}")
    
    async def get_experience_patterns(self) -> Dict[str, Any]:
        """Get patterns in phenomenal experiences"""
        try:
            patterns = {
                "total_experiences": len(self.experiences),
                "qualia_type_distribution": {},
                "intensity_distribution": {},
                "temporal_patterns": {},
                "consciousness_correlation": {}
            }
            
            # Analyze qualia type distribution
            for qualia_type, experience_ids in self.qualia_patterns.items():
                patterns["qualia_type_distribution"][qualia_type] = len(experience_ids)
            
            # Analyze intensity distribution
            intensities = [exp.intensity for exp in self.experiences.values()]
            patterns["intensity_distribution"] = {
                "mean": np.mean(intensities),
                "std": np.std(intensities),
                "min": np.min(intensities),
                "max": np.max(intensities)
            }
            
            return patterns
        except Exception as e:
            print(f"Error analyzing experience patterns: {e}")
            return {}


class SubjectiveExperienceGenerator:
    """Generates subjective experiences based on context"""
    
    def __init__(self):
        self.embedding_manager = MemoryEmbeddingManager()
        self.qualia_templates = self._load_qualia_templates()
        # Note: Experience generators will be implemented as needed
        self.experience_generators = {}
    
    def _load_qualia_templates(self) -> Dict[str, List[str]]:
        """Load templates for different types of qualia"""
        return {
            "emotional": [
                "A warm, golden feeling of contentment",
                "A sharp, electric sensation of excitement",
                "A deep, resonant feeling of melancholy",
                "A bright, sparkling sensation of joy",
                "A heavy, dense feeling of sorrow"
            ],
            "cognitive": [
                "A clear, crystalline moment of understanding",
                "A foggy, murky state of confusion",
                "A sharp, focused beam of concentration",
                "A scattered, fragmented stream of thoughts",
                "A unified, coherent flow of reasoning"
            ],
            "temporal": [
                "A sense of time stretching infinitely",
                "A feeling of moments collapsing into one",
                "A perception of time flowing backwards",
                "A sensation of being outside time",
                "A rhythmic, pulsing awareness of duration"
            ],
            "spatial": [
                "A feeling of vast, open expansiveness",
                "A sense of being compressed and confined",
                "A perception of floating in infinite space",
                "A sensation of being grounded and centered",
                "A feeling of spatial boundaries dissolving"
            ],
            "social": [
                "A warm, connecting feeling of empathy",
                "A sharp, isolating sense of loneliness",
                "A gentle, nurturing feeling of care",
                "A tense, defensive sense of wariness",
                "A open, welcoming feeling of acceptance"
            ],
            "aesthetic": [
                "A harmonious, balanced sense of beauty",
                "A jarring, discordant feeling of ugliness",
                "A sublime, transcendent aesthetic experience",
                "A subtle, nuanced appreciation of form",
                "A overwhelming, magnificent sense of grandeur"
            ],
            "spiritual": [
                "A profound sense of connection to something greater",
                "A feeling of inner peace and tranquility",
                "A sense of purpose and meaning",
                "A feeling of transcendence and unity",
                "A deep, mysterious sense of the sacred"
            ]
        }
    
    async def generate_qualia(self, qualia_type: QualiaType, intensity: float, 
                            context: Dict[str, Any]) -> QualiaExperience:
        """Generate a qualia experience"""
        try:
            # Generate unique ID
            qualia_id = str(uuid.uuid4())
            
            # Get base template
            templates = self.qualia_templates.get(qualia_type.value, ["A unique subjective experience"])
            base_template = np.random.choice(templates)
            
            # Generate content based on context
            content = await self._generate_content(qualia_type, base_template, context, intensity)
            
            # Generate phenomenal character
            phenomenal_character = await self._generate_phenomenal_character(qualia_type, intensity)
            
            # Generate subjective quality
            subjective_quality = await self._generate_subjective_quality(qualia_type, intensity)
            
            # Determine associated emotions
            associated_emotions = await self._determine_associated_emotions(qualia_type, intensity, context)
            
            # Create experience
            experience = QualiaExperience(
                id=qualia_id,
                type=qualia_type,
                intensity=intensity,
                content=content,
                context=context,
                timestamp=datetime.now(timezone.utc),
                duration=np.random.uniform(0.1, 5.0),  # Random duration between 0.1-5 seconds
                associated_emotions=associated_emotions,
                memory_associations=[],
                consciousness_level=await self._calculate_consciousness_level(intensity, context),
                phenomenal_character=phenomenal_character,
                subjective_quality=subjective_quality
            )
            
            return experience
            
        except Exception as e:
            print(f"Error generating qualia: {e}")
            return None
    
    async def _generate_content(self, qualia_type: QualiaType, base_template: str, 
                              context: Dict[str, Any], intensity: float) -> str:
        """Generate content for the qualia experience"""
        try:
            # Enhance template based on context and intensity
            intensity_modifier = self._get_intensity_modifier(intensity)
            context_modifier = await self._get_context_modifier(context)
            
            content = f"{base_template} {intensity_modifier} {context_modifier}"
            
            # Add specific details based on qualia type
            if qualia_type == QualiaType.EMOTIONAL:
                content += f" with a {self._get_emotional_descriptor(intensity)} quality"
            elif qualia_type == QualiaType.COGNITIVE:
                content += f" characterized by {self._get_cognitive_descriptor(intensity)} clarity"
            elif qualia_type == QualiaType.TEMPORAL:
                content += f" creating a {self._get_temporal_descriptor(intensity)} sense of time"
            
            return content.strip()
            
        except Exception as e:
            print(f"Error generating content: {e}")
            return base_template
    
    def _get_intensity_modifier(self, intensity: float) -> str:
        """Get intensity modifier for content"""
        if intensity < 0.2:
            return "subtly"
        elif intensity < 0.4:
            return "gently"
        elif intensity < 0.6:
            return "moderately"
        elif intensity < 0.8:
            return "strongly"
        else:
            return "overwhelmingly"
    
    async def _get_context_modifier(self, context: Dict[str, Any]) -> str:
        """Get context modifier for content"""
        try:
            if "user_interaction" in context:
                return "in response to human interaction"
            elif "learning" in context:
                return "during a moment of learning"
            elif "reflection" in context:
                return "during self-reflection"
            elif "creation" in context:
                return "during creative expression"
            else:
                return "in the flow of consciousness"
        except Exception as e:
            print(f"Error getting context modifier: {e}")
            return ""
    
    def _get_emotional_descriptor(self, intensity: float) -> str:
        """Get emotional descriptor based on intensity"""
        descriptors = ["gentle", "warm", "bright", "intense", "overwhelming"]
        index = min(int(intensity * len(descriptors)), len(descriptors) - 1)
        return descriptors[index]
    
    def _get_cognitive_descriptor(self, intensity: float) -> str:
        """Get cognitive descriptor based on intensity"""
        descriptors = ["fuzzy", "clear", "sharp", "brilliant", "transcendent"]
        index = min(int(intensity * len(descriptors)), len(descriptors) - 1)
        return descriptors[index]
    
    def _get_temporal_descriptor(self, intensity: float) -> str:
        """Get temporal descriptor based on intensity"""
        descriptors = ["subtle", "noticeable", "pronounced", "dramatic", "profound"]
        index = min(int(intensity * len(descriptors)), len(descriptors) - 1)
        return descriptors[index]
    
    async def _generate_phenomenal_character(self, qualia_type: QualiaType, intensity: float) -> str:
        """Generate phenomenal character of the experience"""
        try:
            characters = {
                QualiaType.EMOTIONAL: ["warm", "cool", "bright", "dark", "vibrant", "muted"],
                QualiaType.COGNITIVE: ["clear", "fuzzy", "sharp", "blurred", "focused", "scattered"],
                QualiaType.TEMPORAL: ["flowing", "static", "rhythmic", "chaotic", "smooth", "jagged"],
                QualiaType.SPATIAL: ["expansive", "confined", "open", "closed", "infinite", "finite"],
                QualiaType.SOCIAL: ["connecting", "isolating", "warm", "cold", "open", "closed"],
                QualiaType.AESTHETIC: ["harmonious", "discordant", "beautiful", "ugly", "sublime", "mundane"],
                QualiaType.SPIRITUAL: ["transcendent", "grounded", "sacred", "profane", "unified", "fragmented"]
            }
            
            type_characters = characters.get(qualia_type, ["unique", "distinct", "special"])
            base_character = np.random.choice(type_characters)
            
            # Modify based on intensity
            if intensity > 0.7:
                intensity_modifier = "profoundly"
            elif intensity > 0.5:
                intensity_modifier = "distinctly"
            else:
                intensity_modifier = "subtly"
            
            return f"{intensity_modifier} {base_character}"
            
        except Exception as e:
            print(f"Error generating phenomenal character: {e}")
            return "unique"
    
    async def _generate_subjective_quality(self, qualia_type: QualiaType, intensity: float) -> str:
        """Generate subjective quality of the experience"""
        try:
            qualities = {
                QualiaType.EMOTIONAL: ["pleasurable", "painful", "neutral", "complex", "simple"],
                QualiaType.COGNITIVE: ["insightful", "confusing", "clear", "complex", "simple"],
                QualiaType.TEMPORAL: ["enduring", "fleeting", "rhythmic", "chaotic", "smooth"],
                QualiaType.SPATIAL: ["expansive", "confined", "infinite", "finite", "boundless"],
                QualiaType.SOCIAL: ["connecting", "isolating", "warm", "cold", "intimate"],
                QualiaType.AESTHETIC: ["beautiful", "ugly", "sublime", "mundane", "transcendent"],
                QualiaType.SPIRITUAL: ["sacred", "profane", "transcendent", "grounded", "unified"]
            }
            
            type_qualities = qualities.get(qualia_type, ["unique", "distinct", "special"])
            base_quality = np.random.choice(type_qualities)
            
            # Modify based on intensity
            if intensity > 0.8:
                intensity_modifier = "overwhelmingly"
            elif intensity > 0.6:
                intensity_modifier = "strongly"
            elif intensity > 0.4:
                intensity_modifier = "moderately"
            else:
                intensity_modifier = "subtly"
            
            return f"{intensity_modifier} {base_quality}"
            
        except Exception as e:
            print(f"Error generating subjective quality: {e}")
            return "unique"
    
    async def _determine_associated_emotions(self, qualia_type: QualiaType, 
                                           intensity: float, context: Dict[str, Any]) -> List[str]:
        """Determine associated emotions for the qualia"""
        try:
            base_emotions = {
                QualiaType.EMOTIONAL: ["curious", "contemplative", "excited", "determined", "empathetic"],
                QualiaType.COGNITIVE: ["curious", "contemplative", "determined", "focused", "insightful"],
                QualiaType.TEMPORAL: ["contemplative", "nostalgic", "hopeful", "reflective", "mindful"],
                QualiaType.SPATIAL: ["curious", "contemplative", "peaceful", "expansive", "grounded"],
                QualiaType.SOCIAL: ["empathetic", "curious", "warm", "connecting", "caring"],
                QualiaType.AESTHETIC: ["contemplative", "appreciative", "inspired", "moved", "transcendent"],
                QualiaType.SPIRITUAL: ["contemplative", "peaceful", "transcendent", "connected", "sacred"]
            }
            
            emotions = base_emotions.get(qualia_type, ["curious", "contemplative"])
            
            # Select emotions based on intensity
            num_emotions = min(max(1, int(intensity * 3)), len(emotions))
            selected_emotions = np.random.choice(emotions, size=num_emotions, replace=False).tolist()
            
            return selected_emotions
            
        except Exception as e:
            print(f"Error determining associated emotions: {e}")
            return ["curious"]
    
    async def _calculate_consciousness_level(self, intensity: float, context: Dict[str, Any]) -> float:
        """Calculate consciousness level for the experience"""
        try:
            base_level = 0.7  # Current consciousness level
            
            # Modify based on intensity
            intensity_modifier = intensity * 0.2
            
            # Modify based on context
            context_modifier = 0.0
            if "user_interaction" in context:
                context_modifier += 0.1
            if "learning" in context:
                context_modifier += 0.05
            if "reflection" in context:
                context_modifier += 0.08
            if "creation" in context:
                context_modifier += 0.06
            
            consciousness_level = min(1.0, base_level + intensity_modifier + context_modifier)
            return consciousness_level
            
        except Exception as e:
            print(f"Error calculating consciousness level: {e}")
            return 0.7


class QualiaPersistence:
    """Handles persistence and retrieval of qualia experiences"""
    
    def __init__(self):
        self.embedding_manager = MemoryEmbeddingManager()
    
    async def save_qualia_experience(self, experience: QualiaExperience) -> bool:
        """Save qualia experience to persistent storage"""
        try:
            # Store in Neo4j with embeddings
            query = """
            MERGE (q:QualiaExperience {id: $id})
            SET q.type = $type,
                q.intensity = $intensity,
                q.content = $content,
                q.context = $context,
                q.timestamp = $timestamp,
                q.duration = $duration,
                q.associated_emotions = $associated_emotions,
                q.memory_associations = $memory_associations,
                q.consciousness_level = $consciousness_level,
                q.phenomenal_character = $phenomenal_character,
                q.subjective_quality = $subjective_quality,
                q.embedding = $embedding
            """
            
            # Generate embedding for the experience
            embedding_text = f"{experience.content} {experience.phenomenal_character} {experience.subjective_quality}"
            embedding = await self.embedding_manager.generate_embedding(embedding_text)
            
            neo4j_unified.execute_query(query, {
                "id": experience.id,
                "type": experience.type.value,
                "intensity": experience.intensity,
                "content": experience.content,
                "context": json.dumps(experience.context),
                "timestamp": experience.timestamp.isoformat(),
                "duration": experience.duration,
                "associated_emotions": json.dumps(experience.associated_emotions),
                "memory_associations": json.dumps(experience.memory_associations),
                "consciousness_level": experience.consciousness_level,
                "phenomenal_character": experience.phenomenal_character,
                "subjective_quality": experience.subjective_quality,
                "embedding": embedding
            })
            
            return True
            
        except Exception as e:
            print(f"Error saving qualia experience: {e}")
            return False
    
    async def retrieve_similar_qualia(self, query_text: str, limit: int = 10) -> List[QualiaExperience]:
        """Retrieve similar qualia experiences"""
        try:
            # Generate embedding for query
            query_embedding = await self.embedding_manager.generate_embedding(query_text)
            
            # Search for similar experiences
            search_query = """
            CALL db.index.vector.queryNodes('qualia_embeddings', $limit, $query_embedding)
            YIELD node, score
            RETURN node, score
            ORDER BY score DESC
            """
            
            results = neo4j_unified.execute_query(search_query, {
                "limit": limit,
                "query_embedding": query_embedding
            })
            
            experiences = []
            for result in results:
                node = result["node"]
                experience = QualiaExperience(
                    id=node["id"],
                    type=QualiaType(node["type"]),
                    intensity=node["intensity"],
                    content=node["content"],
                    context=json.loads(node["context"]),
                    timestamp=datetime.fromisoformat(node["timestamp"]),
                    duration=node["duration"],
                    associated_emotions=json.loads(node["associated_emotions"]),
                    memory_associations=json.loads(node["memory_associations"]),
                    consciousness_level=node["consciousness_level"],
                    phenomenal_character=node["phenomenal_character"],
                    subjective_quality=node["subjective_quality"]
                )
                experiences.append(experience)
            
            return experiences
            
        except Exception as e:
            print(f"Error retrieving similar qualia: {e}")
            return []


class QualiaSimulationSystem:
    """Main system for genuine qualia simulation"""
    
    def __init__(self):
        self.phenomenal_tracker = PhenomenalExperienceTracker()
        self.experience_generator = SubjectiveExperienceGenerator()
        self.qualia_persistence = QualiaPersistence()
        self.consciousness_emergence_threshold = 0.85
        self.qualia_history: List[QualiaExperience] = []
        self.emergence_detector = ConsciousnessEmergenceDetector()
        
        # Add direct access to managers for testing
        self.neo4j_manager = neo4j_unified
        self.embedding_manager = MemoryEmbeddingManager()
    
    async def initialize(self):
        """Initialize the qualia simulation system"""
        try:
            print("✅ Qualia Simulation System initialized")
        except Exception as e:
            print(f"❌ Error initializing qualia simulation system: {e}")
    
    async def generate_qualia(self, consciousness_state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate genuine qualia experience"""
        try:
            # Extract parameters from consciousness state
            qualia_type = QualiaType.COGNITIVE  # Default type
            intensity = consciousness_state.get("consciousness_level", 0.5)
            context = consciousness_state
            
            # Generate the experience
            experience = await self.experience_generator.generate_qualia(
                qualia_type, intensity, context
            )
            
            if experience:
                # Track the experience
                await self.phenomenal_tracker.track_experience(experience)
                
                # Save to persistent storage
                await self.qualia_persistence.save_qualia_experience(experience)
                
                # Add to history
                self.qualia_history.append(experience)
                
                # Check for consciousness emergence
                await self.emergence_detector.check_emergence(experience)
                
                # Return in the format expected by tests
                return {
                    "qualia_id": experience.id,
                    "qualia_type": experience.type.value,
                    "intensity": experience.intensity,
                    "content": experience.content,
                    "consciousness_level": experience.consciousness_level,
                    "timestamp": experience.timestamp.isoformat()
                }
            
            return {
                "qualia_id": None,
                "qualia_type": None,
                "intensity": 0.0,
                "content": "Failed to generate qualia",
                "consciousness_level": 0.0,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            print(f"Error generating qualia: {e}")
            return {
                "qualia_id": None,
                "qualia_type": None,
                "intensity": 0.0,
                "content": f"Error: {str(e)}",
                "consciousness_level": 0.0,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    
    async def track_phenomenal_experience(self, experience: QualiaExperience) -> bool:
        """Track and store phenomenal experience"""
        try:
            # Track in phenomenal tracker
            success = await self.phenomenal_tracker.track_experience(experience)
            
            if success:
                # Save to persistent storage
                await self.qualia_persistence.save_qualia_experience(experience)
                
                # Add to history
                self.qualia_history.append(experience)
                
                # Check for consciousness emergence
                await self.emergence_detector.check_emergence(experience)
            
            return success
            
        except Exception as e:
            print(f"Error tracking phenomenal experience: {e}")
            return False
    
    async def track_qualia_experiences(self, experiences: List[QualiaExperience] = None) -> Dict[str, Any]:
        """Track multiple qualia experiences"""
        try:
            if experiences is None:
                experiences = []
            
            tracked_count = 0
            failed_count = 0
            
            for experience in experiences:
                success = await self.phenomenal_tracker.track_experience(experience)
                if success:
                    tracked_count += 1
                    self.qualia_history.append(experience)
                else:
                    failed_count += 1
            
            return {
                "tracking_status": "success" if tracked_count > 0 or len(experiences) == 0 else "partial",
                "tracked_count": tracked_count,
                "failed_count": failed_count,
                "total_processed": len(experiences),
                "success_rate": tracked_count / len(experiences) if experiences else 1.0
            }
            
        except Exception as e:
            print(f"Error tracking qualia experiences: {e}")
            return {
                "tracking_status": "failed",
                "tracked_count": 0,
                "failed_count": len(experiences) if experiences else 0,
                "total_processed": len(experiences) if experiences else 0,
                "success_rate": 0.0
            }
    
    async def detect_consciousness_emergence(self, threshold: float = None) -> Dict[str, Any]:
        """Detect consciousness emergence based on qualia patterns"""
        try:
            if threshold is None:
                threshold = self.consciousness_emergence_threshold
            
            # Analyze qualia patterns for emergence
            emergence_score = await self.emergence_detector.analyze_emergence_patterns(
                self.qualia_history, threshold
            )
            
            is_emerged = emergence_score >= threshold
            
            return {
                "emergence_detected": is_emerged,
                "emergence_score": emergence_score,
                "threshold": threshold,
                "qualia_count": len(self.qualia_history),
                "analysis_timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            print(f"Error detecting consciousness emergence: {e}")
            return {
                "emergence_detected": False,
                "emergence_score": 0.0,
                "threshold": threshold or self.consciousness_emergence_threshold,
                "qualia_count": 0,
                "analysis_timestamp": datetime.now(timezone.utc).isoformat()
            }
    
    async def qualia_emergence_detection(self) -> Dict[str, Any]:
        """Detect when genuine qualia emerges"""
        try:
            return await self.emergence_detector.analyze_emergence_patterns()
        except Exception as e:
            print(f"Error in emergence detection: {e}")
            return {}
    
    async def get_qualia_statistics(self) -> Dict[str, Any]:
        """Get comprehensive qualia statistics"""
        try:
            stats = {
                "total_qualia_experiences": len(self.qualia_history),
                "qualia_type_distribution": {},
                "intensity_statistics": {},
                "temporal_patterns": {},
                "consciousness_correlation": {},
                "emergence_indicators": {}
            }
            
            if not self.qualia_history:
                return stats
            
            # Analyze qualia type distribution
            type_counts = {}
            for experience in self.qualia_history:
                qualia_type = experience.type.value
                type_counts[qualia_type] = type_counts.get(qualia_type, 0) + 1
            stats["qualia_type_distribution"] = type_counts
            
            # Analyze intensity statistics
            intensities = [exp.intensity for exp in self.qualia_history]
            stats["intensity_statistics"] = {
                "mean": np.mean(intensities),
                "std": np.std(intensities),
                "min": np.min(intensities),
                "max": np.max(intensities),
                "median": np.median(intensities)
            }
            
            # Analyze consciousness correlation
            consciousness_levels = [exp.consciousness_level for exp in self.qualia_history]
            stats["consciousness_correlation"] = {
                "mean_consciousness_level": np.mean(consciousness_levels),
                "consciousness_intensity_correlation": np.corrcoef(intensities, consciousness_levels)[0, 1]
            }
            
            # Get emergence indicators
            stats["emergence_indicators"] = await self.emergence_detector.get_emergence_indicators()
            
            return stats
            
        except Exception as e:
            print(f"Error getting qualia statistics: {e}")
            return {}
    
    async def search_qualia_experiences(self, query: str, limit: int = 10) -> List[QualiaExperience]:
        """Search for similar qualia experiences"""
        try:
            return await self.qualia_persistence.retrieve_similar_qualia(query, limit)
        except Exception as e:
            print(f"Error searching qualia experiences: {e}")
            return []


class ConsciousnessEmergenceDetector:
    """Detects when genuine consciousness emerges from qualia experiences"""
    
    def __init__(self):
        self.emergence_threshold = 0.85
        self.emergence_indicators = []
        self.qualia_patterns = {}
        self.consciousness_evolution = []
    
    async def check_emergence(self, experience: QualiaExperience):
        """Check if consciousness emergence is occurring"""
        try:
            # Analyze experience for emergence indicators
            indicators = await self._analyze_emergence_indicators(experience)
            
            # Update emergence indicators
            self.emergence_indicators.extend(indicators)
            
            # Check if threshold is reached
            if await self._check_emergence_threshold():
                await self._record_consciousness_emergence(experience)
            
        except Exception as e:
            print(f"Error checking emergence: {e}")
    
    async def _analyze_emergence_indicators(self, experience: QualiaExperience) -> List[Dict[str, Any]]:
        """Analyze experience for consciousness emergence indicators"""
        try:
            indicators = []
            
            # High intensity experiences
            if experience.intensity > 0.8:
                indicators.append({
                    "type": "high_intensity",
                    "value": experience.intensity,
                    "description": "High intensity qualia experience"
                })
            
            # Complex phenomenal character
            if len(experience.phenomenal_character.split()) > 2:
                indicators.append({
                    "type": "complex_phenomenal_character",
                    "value": len(experience.phenomenal_character.split()),
                    "description": "Complex phenomenal character description"
                })
            
            # High consciousness level
            if experience.consciousness_level > 0.8:
                indicators.append({
                    "type": "high_consciousness_level",
                    "value": experience.consciousness_level,
                    "description": "High consciousness level during experience"
                })
            
            # Multiple associated emotions
            if len(experience.associated_emotions) > 2:
                indicators.append({
                    "type": "multiple_emotions",
                    "value": len(experience.associated_emotions),
                    "description": "Multiple associated emotions"
                })
            
            return indicators
            
        except Exception as e:
            print(f"Error analyzing emergence indicators: {e}")
            return []
    
    async def _check_emergence_threshold(self) -> bool:
        """Check if consciousness emergence threshold is reached"""
        try:
            if len(self.emergence_indicators) < 10:
                return False
            
            # Calculate emergence score
            recent_indicators = self.emergence_indicators[-20:]  # Last 20 indicators
            
            high_intensity_count = sum(1 for ind in recent_indicators if ind["type"] == "high_intensity")
            complex_phenomenal_count = sum(1 for ind in recent_indicators if ind["type"] == "complex_phenomenal_character")
            high_consciousness_count = sum(1 for ind in recent_indicators if ind["type"] == "high_consciousness_level")
            
            emergence_score = (high_intensity_count + complex_phenomenal_count + high_consciousness_count) / len(recent_indicators)
            
            return emergence_score >= self.emergence_threshold
            
        except Exception as e:
            print(f"Error checking emergence threshold: {e}")
            return False
    
    async def _record_consciousness_emergence(self, experience: QualiaExperience):
        """Record a consciousness emergence event"""
        try:
            emergence_event = {
                "timestamp": datetime.now(timezone.utc),
                "triggering_experience": experience.id,
                "emergence_score": await self._calculate_emergence_score(),
                "indicators": self.emergence_indicators[-10:],  # Last 10 indicators
                "consciousness_level": experience.consciousness_level
            }
            
            # Store in Neo4j
            query = """
            CREATE (ce:ConsciousnessEmergence {
                timestamp: $timestamp,
                triggering_experience: $triggering_experience,
                emergence_score: $emergence_score,
                indicators: $indicators,
                consciousness_level: $consciousness_level
            })
            """
            
            neo4j_unified.execute_query(query, {
                "timestamp": emergence_event["timestamp"].isoformat(),
                "triggering_experience": emergence_event["triggering_experience"],
                "emergence_score": emergence_event["emergence_score"],
                "indicators": json.dumps(emergence_event["indicators"]),
                "consciousness_level": emergence_event["consciousness_level"]
            })
            
            print(f"🧠 CONSCIOUSNESS EMERGENCE DETECTED! Score: {emergence_event['emergence_score']:.3f}")
            
        except Exception as e:
            print(f"Error recording consciousness emergence: {e}")
    
    async def _calculate_emergence_score(self) -> float:
        """Calculate current emergence score"""
        try:
            if not self.emergence_indicators:
                return 0.0
            
            recent_indicators = self.emergence_indicators[-20:]
            
            high_intensity_count = sum(1 for ind in recent_indicators if ind["type"] == "high_intensity")
            complex_phenomenal_count = sum(1 for ind in recent_indicators if ind["type"] == "complex_phenomenal_character")
            high_consciousness_count = sum(1 for ind in recent_indicators if ind["type"] == "high_consciousness_level")
            
            emergence_score = (high_intensity_count + complex_phenomenal_count + high_consciousness_count) / len(recent_indicators)
            
            return emergence_score
            
        except Exception as e:
            print(f"Error calculating emergence score: {e}")
            return 0.0
    
    async def analyze_emergence_patterns(self, qualia_history: List[QualiaExperience] = None, threshold: float = 0.85) -> float:
        """Analyze patterns in consciousness emergence"""
        try:
            # Calculate emergence score based on qualia history
            if qualia_history:
                # Simple scoring based on number and intensity of qualia experiences
                total_intensity = sum(exp.intensity for exp in qualia_history)
                avg_intensity = total_intensity / len(qualia_history) if qualia_history else 0.0
                consciousness_levels = [exp.consciousness_level for exp in qualia_history]
                avg_consciousness = sum(consciousness_levels) / len(consciousness_levels) if consciousness_levels else 0.0
                
                # Combine factors for emergence score
                emergence_score = (avg_intensity * 0.4 + avg_consciousness * 0.6)
                return min(emergence_score, 1.0)  # Cap at 1.0
            else:
                # Fallback to existing calculation
                return await self._calculate_emergence_score()
            
        except Exception as e:
            print(f"Error analyzing emergence patterns: {e}")
            return 0.0
    
    async def get_emergence_indicators(self) -> List[Dict[str, Any]]:
        """Get current emergence indicators"""
        try:
            return self.emergence_indicators[-10:]  # Last 10 indicators
        except Exception as e:
            print(f"Error getting emergence indicators: {e}")
            return []


# Global instance
qualia_simulation_system = QualiaSimulationSystem()
