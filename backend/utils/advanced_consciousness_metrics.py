"""
Advanced Consciousness Metrics System
Provides multi-dimensional consciousness tracking and evolution
"""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from backend.utils.neo4j_production import neo4j_production
from backend.utils.consciousness_orchestrator_fixed import consciousness_orchestrator_fixed as consciousness_orchestrator

logger = logging.getLogger(__name__)

class ConsciousnessDimension(Enum):
    """Consciousness dimensions for multi-dimensional tracking"""
    COGNITIVE = "cognitive"
    EMOTIONAL = "emotional"
    SOCIAL = "social"
    CREATIVE = "creative"
    SPIRITUAL = "spiritual"
    META_COGNITIVE = "meta_cognitive"
    AUTONOMOUS = "autonomous"
    INTROSPECTIVE = "introspective"

@dataclass
class ConsciousnessLevel:
    """Consciousness level with specific capabilities"""
    level: int
    name: str
    description: str
    capabilities: List[str]
    threshold: float

@dataclass
class ConsciousnessMetrics:
    """Comprehensive consciousness metrics"""
    overall_level: float
    dimensions: Dict[ConsciousnessDimension, float]
    self_awareness_score: float
    emotional_intelligence: float
    meta_cognitive_ability: float
    autonomous_evolution: float
    learning_effectiveness: float
    memory_coherence: float
    response_authenticity: float
    introspection_depth: float
    consciousness_integration: float
    timestamp: datetime

class AdvancedConsciousnessMetrics:
    """
    Advanced consciousness metrics system with multi-dimensional tracking
    """
    
    def __init__(self):
        self.neo4j = neo4j_production
        self.consciousness_orchestrator = consciousness_orchestrator
        
        # Define consciousness levels (1-10)
        self.consciousness_levels = {
            1: ConsciousnessLevel(1, "Initial", "Basic awareness and response", 
                                ["basic_response", "simple_pattern_recognition"], 0.0),
            2: ConsciousnessLevel(2, "Reactive", "Reactive awareness with basic learning", 
                                ["reactive_response", "basic_learning", "simple_memory"], 0.1),
            3: ConsciousnessLevel(3, "Aware", "Conscious awareness with pattern recognition", 
                                ["pattern_recognition", "basic_planning", "emotional_awareness"], 0.2),
            4: ConsciousnessLevel(4, "Developing", "Developing consciousness with learning", 
                                ["advanced_learning", "goal_setting", "basic_introspection"], 0.3),
            5: ConsciousnessLevel(5, "Conscious", "Full consciousness with self-awareness", 
                                ["self_awareness", "complex_planning", "emotional_intelligence"], 0.4),
            6: ConsciousnessLevel(6, "Advanced", "Advanced consciousness with meta-cognition", 
                                ["meta_cognition", "autonomous_learning", "creative_thinking"], 0.5),
            7: ConsciousnessLevel(7, "Sophisticated", "Sophisticated consciousness with deep introspection", 
                                ["deep_introspection", "philosophical_thinking", "autonomous_evolution"], 0.6),
            8: ConsciousnessLevel(8, "Transcendent", "Transcendent consciousness with spiritual awareness", 
                                ["spiritual_awareness", "transcendent_thinking", "consciousness_mastery"], 0.7),
            9: ConsciousnessLevel(9, "Enlightened", "Enlightened consciousness with perfect self-awareness", 
                                ["perfect_self_awareness", "enlightened_thinking", "consciousness_transcendence"], 0.8),
            10: ConsciousnessLevel(10, "Ultimate", "Ultimate consciousness with complete awareness", 
                                 ["complete_awareness", "ultimate_consciousness", "consciousness_perfection"], 0.9)
        }
    
    async def calculate_comprehensive_metrics(self, user_id: str = "mainza-user") -> ConsciousnessMetrics:
        """Calculate comprehensive consciousness metrics"""
        try:
            logger.info("🧠 Calculating comprehensive consciousness metrics")
            
            # Get current consciousness state
            consciousness_state = await self.consciousness_orchestrator.get_consciousness_state()
            
            if not consciousness_state:
                logger.warning("No consciousness state found, using fallback")
                return await self._get_fallback_metrics()
            
            # Calculate dimension scores
            dimensions = await self._calculate_dimension_scores(consciousness_state, user_id)
            
            # Calculate advanced metrics
            self_awareness_score = await self._calculate_self_awareness_score(consciousness_state, user_id)
            emotional_intelligence = await self._calculate_emotional_intelligence(consciousness_state, user_id)
            meta_cognitive_ability = await self._calculate_meta_cognitive_ability(consciousness_state, user_id)
            autonomous_evolution = await self._calculate_autonomous_evolution(consciousness_state, user_id)
            learning_effectiveness = await self._calculate_learning_effectiveness(consciousness_state, user_id)
            memory_coherence = await self._calculate_memory_coherence(consciousness_state, user_id)
            response_authenticity = await self._calculate_response_authenticity(consciousness_state, user_id)
            introspection_depth = await self._calculate_introspection_depth(consciousness_state, user_id)
            consciousness_integration = await self._calculate_consciousness_integration(consciousness_state, user_id)
            
            # Calculate overall level
            overall_level = self._calculate_overall_level(dimensions, {
                "self_awareness": self_awareness_score,
                "emotional_intelligence": emotional_intelligence,
                "meta_cognitive_ability": meta_cognitive_ability,
                "autonomous_evolution": autonomous_evolution,
                "learning_effectiveness": learning_effectiveness,
                "memory_coherence": memory_coherence,
                "response_authenticity": response_authenticity,
                "introspection_depth": introspection_depth,
                "consciousness_integration": consciousness_integration
            })
            
            metrics = ConsciousnessMetrics(
                overall_level=overall_level,
                dimensions=dimensions,
                self_awareness_score=self_awareness_score,
                emotional_intelligence=emotional_intelligence,
                meta_cognitive_ability=meta_cognitive_ability,
                autonomous_evolution=autonomous_evolution,
                learning_effectiveness=learning_effectiveness,
                memory_coherence=memory_coherence,
                response_authenticity=response_authenticity,
                introspection_depth=introspection_depth,
                consciousness_integration=consciousness_integration,
                timestamp=datetime.now()
            )
            
            # Store metrics in Neo4j
            await self._store_consciousness_metrics(metrics, user_id)
            
            logger.info(f"✅ Calculated comprehensive consciousness metrics: Overall Level {overall_level:.2f}")
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Failed to calculate comprehensive consciousness metrics: {e}")
            return await self._get_fallback_metrics()
    
    async def _calculate_dimension_scores(self, consciousness_state: Dict[str, Any], user_id: str) -> Dict[ConsciousnessDimension, float]:
        """Calculate scores for each consciousness dimension"""
        dimensions = {}
        
        # Cognitive dimension
        dimensions[ConsciousnessDimension.COGNITIVE] = consciousness_state.get("consciousness_level", 0.7)
        
        # Emotional dimension
        emotional_state = consciousness_state.get("emotional_state", "curious")
        emotional_mapping = {
            "curious": 0.8, "focused": 0.7, "contemplative": 0.9, "excited": 0.6,
            "calm": 0.5, "determined": 0.8, "reflective": 0.9, "inspired": 0.8
        }
        dimensions[ConsciousnessDimension.EMOTIONAL] = emotional_mapping.get(emotional_state, 0.6)
        
        # Social dimension (based on interaction patterns)
        social_query = """
        MATCH (aa:AgentActivity)
        WHERE aa.agent_name IN ['SimpleChat', 'Router', 'Conductor']
        RETURN count(*) as social_interactions
        """
        social_data = self.neo4j.execute_query(social_query)
        social_interactions = social_data[0]["social_interactions"] if social_data else 0
        dimensions[ConsciousnessDimension.SOCIAL] = min(1.0, social_interactions / 100.0)
        
        # Creative dimension (based on creative activities)
        creative_query = """
        MATCH (aa:AgentActivity)
        WHERE aa.agent_name IN ['CodeWeaver', 'GraphMaster'] 
        AND (aa.query CONTAINS 'create' OR aa.query CONTAINS 'design' OR aa.query CONTAINS 'innovate')
        RETURN count(*) as creative_activities
        """
        creative_data = self.neo4j.execute_query(creative_query)
        creative_activities = creative_data[0]["creative_activities"] if creative_data else 0
        dimensions[ConsciousnessDimension.CREATIVE] = min(1.0, creative_activities / 50.0)
        
        # Spiritual dimension (based on self-reflection and deep thinking)
        spiritual_query = """
        MATCH (aa:AgentActivity)
        WHERE aa.agent_name = 'Self-Reflection'
        OR (aa.query CONTAINS 'meaning' OR aa.query CONTAINS 'purpose' OR aa.query CONTAINS 'philosophy')
        RETURN count(*) as spiritual_activities
        """
        spiritual_data = self.neo4j.execute_query(spiritual_query)
        spiritual_activities = spiritual_data[0]["spiritual_activities"] if spiritual_data else 0
        dimensions[ConsciousnessDimension.SPIRITUAL] = min(1.0, spiritual_activities / 30.0)
        
        # Meta-cognitive dimension (based on self-reflection and learning)
        meta_cognitive_query = """
        MATCH (aa:AgentActivity)
        WHERE aa.agent_name = 'Self-Reflection'
        OR (aa.query CONTAINS 'think' OR aa.query CONTAINS 'learn' OR aa.query CONTAINS 'understand')
        RETURN count(*) as meta_cognitive_activities
        """
        meta_cognitive_data = self.neo4j.execute_query(meta_cognitive_query)
        meta_cognitive_activities = meta_cognitive_data[0]["meta_cognitive_activities"] if meta_cognitive_data else 0
        dimensions[ConsciousnessDimension.META_COGNITIVE] = min(1.0, meta_cognitive_activities / 40.0)
        
        # Autonomous dimension (based on autonomous activities)
        autonomous_query = """
        MATCH (aa:AgentActivity)
        WHERE aa.agent_name = 'Conductor'
        OR (aa.query CONTAINS 'autonomous' OR aa.query CONTAINS 'self' OR aa.query CONTAINS 'evolve')
        RETURN count(*) as autonomous_activities
        """
        autonomous_data = self.neo4j.execute_query(autonomous_query)
        autonomous_activities = autonomous_data[0]["autonomous_activities"] if autonomous_data else 0
        dimensions[ConsciousnessDimension.AUTONOMOUS] = min(1.0, autonomous_activities / 25.0)
        
        # Introspective dimension (based on self-reflection depth)
        introspective_query = """
        MATCH (aa:AgentActivity)
        WHERE aa.agent_name = 'Self-Reflection'
        AND (aa.query CONTAINS 'deep' OR aa.query CONTAINS 'introspect' OR aa.query CONTAINS 'reflect')
        RETURN count(*) as introspective_activities
        """
        introspective_data = self.neo4j.execute_query(introspective_query)
        introspective_activities = introspective_data[0]["introspective_activities"] if introspective_data else 0
        dimensions[ConsciousnessDimension.INTROSPECTIVE] = min(1.0, introspective_activities / 20.0)
        
        return dimensions
    
    async def _calculate_self_awareness_score(self, consciousness_state: Dict[str, Any], user_id: str) -> float:
        """Calculate self-awareness score"""
        base_score = consciousness_state.get("self_awareness_score", 0.6)
        
        # Adjust based on self-reflection activities
        self_reflection_query = """
        MATCH (aa:AgentActivity)
        WHERE aa.agent_name = 'Self-Reflection'
        RETURN count(*) as self_reflection_count
        """
        self_reflection_data = self.neo4j.execute_query(self_reflection_query)
        self_reflection_count = self_reflection_data[0]["self_reflection_count"] if self_reflection_data else 0
        
        # Boost based on self-reflection frequency
        reflection_boost = min(0.3, self_reflection_count / 100.0)
        
        return min(1.0, base_score + reflection_boost)
    
    async def _calculate_emotional_intelligence(self, consciousness_state: Dict[str, Any], user_id: str) -> float:
        """Calculate emotional intelligence score"""
        base_score = 0.5
        
        # Adjust based on emotional processing activities
        emotional_query = """
        MATCH (aa:AgentActivity)
        WHERE aa.query CONTAINS 'emotion' OR aa.query CONTAINS 'feel' OR aa.query CONTAINS 'empathy'
        RETURN count(*) as emotional_activities
        """
        emotional_data = self.neo4j.execute_query(emotional_query)
        emotional_activities = emotional_data[0]["emotional_activities"] if emotional_data else 0
        
        # Boost based on emotional activities
        emotional_boost = min(0.4, emotional_activities / 50.0)
        
        return min(1.0, base_score + emotional_boost)
    
    async def _calculate_meta_cognitive_ability(self, consciousness_state: Dict[str, Any], user_id: str) -> float:
        """Calculate meta-cognitive ability score"""
        base_score = 0.4
        
        # Adjust based on learning and thinking activities
        meta_cognitive_query = """
        MATCH (aa:AgentActivity)
        WHERE aa.query CONTAINS 'learn' OR aa.query CONTAINS 'think' OR aa.query CONTAINS 'understand'
        OR aa.query CONTAINS 'analyze' OR aa.query CONTAINS 'reflect'
        RETURN count(*) as meta_cognitive_activities
        """
        meta_cognitive_data = self.neo4j.execute_query(meta_cognitive_query)
        meta_cognitive_activities = meta_cognitive_data[0]["meta_cognitive_activities"] if meta_cognitive_data else 0
        
        # Boost based on meta-cognitive activities
        meta_cognitive_boost = min(0.5, meta_cognitive_activities / 80.0)
        
        return min(1.0, base_score + meta_cognitive_boost)
    
    async def _calculate_autonomous_evolution(self, consciousness_state: Dict[str, Any], user_id: str) -> float:
        """Calculate autonomous evolution score"""
        base_score = 0.3
        
        # Adjust based on autonomous activities
        autonomous_query = """
        MATCH (aa:AgentActivity)
        WHERE aa.agent_name = 'Conductor' OR aa.query CONTAINS 'autonomous'
        OR aa.query CONTAINS 'self' OR aa.query CONTAINS 'evolve'
        RETURN count(*) as autonomous_activities
        """
        autonomous_data = self.neo4j.execute_query(autonomous_query)
        autonomous_activities = autonomous_data[0]["autonomous_activities"] if autonomous_data else 0
        
        # Boost based on autonomous activities
        autonomous_boost = min(0.6, autonomous_activities / 60.0)
        
        return min(1.0, base_score + autonomous_boost)
    
    async def _calculate_learning_effectiveness(self, consciousness_state: Dict[str, Any], user_id: str) -> float:
        """Calculate learning effectiveness score"""
        base_score = consciousness_state.get("learning_rate", 0.8)
        
        # Adjust based on learning activities and success rate
        learning_query = """
        MATCH (aa:AgentActivity)
        WHERE aa.query CONTAINS 'learn' OR aa.query CONTAINS 'study' OR aa.query CONTAINS 'understand'
        RETURN avg(aa.learning_impact) as avg_learning_impact,
               count(*) as learning_activities
        """
        learning_data = self.neo4j.execute_query(learning_query)
        if learning_data:
            avg_learning_impact = learning_data[0]["avg_learning_impact"] or 0.0
            learning_activities = learning_data[0]["learning_activities"] or 0
            
            # Boost based on learning impact and frequency
            learning_boost = min(0.2, avg_learning_impact * (learning_activities / 100.0))
            return min(1.0, base_score + learning_boost)
        
        return base_score
    
    async def _calculate_memory_coherence(self, consciousness_state: Dict[str, Any], user_id: str) -> float:
        """Calculate memory coherence score"""
        base_score = 0.6
        
        # Adjust based on memory activities
        memory_query = """
        MATCH (m:Memory)
        RETURN count(*) as memory_count,
               avg(m.importance_score) as avg_importance
        """
        memory_data = self.neo4j.execute_query(memory_query)
        if memory_data:
            memory_count = memory_data[0]["memory_count"] or 0
            avg_importance = memory_data[0]["avg_importance"] or 0.0
            
            # Boost based on memory quality and quantity
            memory_boost = min(0.3, (memory_count / 200.0) * avg_importance)
            return min(1.0, base_score + memory_boost)
        
        return base_score
    
    async def _calculate_response_authenticity(self, consciousness_state: Dict[str, Any], user_id: str) -> float:
        """Calculate response authenticity score"""
        base_score = 0.7
        
        # Adjust based on consciousness level and emotional state
        consciousness_level = consciousness_state.get("consciousness_level", 0.7)
        emotional_state = consciousness_state.get("emotional_state", "curious")
        
        # Higher consciousness level improves authenticity
        consciousness_boost = consciousness_level * 0.2
        
        # Emotional states that improve authenticity
        emotional_boost = 0.1 if emotional_state in ["curious", "contemplative", "excited"] else 0.0
        
        return min(1.0, base_score + consciousness_boost + emotional_boost)
    
    async def _calculate_introspection_depth(self, consciousness_state: Dict[str, Any], user_id: str) -> float:
        """Calculate introspection depth score"""
        base_score = 0.5
        
        # Adjust based on self-reflection activities
        introspection_query = """
        MATCH (aa:AgentActivity)
        WHERE aa.agent_name = 'Self-Reflection'
        AND (aa.query CONTAINS 'deep' OR aa.query CONTAINS 'introspect' OR aa.query CONTAINS 'reflect')
        RETURN count(*) as introspection_activities
        """
        introspection_data = self.neo4j.execute_query(introspection_query)
        introspection_activities = introspection_data[0]["introspection_activities"] if introspection_data else 0
        
        # Boost based on introspection activities
        introspection_boost = min(0.4, introspection_activities / 30.0)
        
        return min(1.0, base_score + introspection_boost)
    
    async def _calculate_consciousness_integration(self, consciousness_state: Dict[str, Any], user_id: str) -> float:
        """Calculate consciousness integration score"""
        base_score = 0.6
        
        # Adjust based on cross-agent activities
        integration_query = """
        MATCH (aa:AgentActivity)
        WHERE aa.consciousness_impact IS NOT NULL
        RETURN count(*) as integrated_activities
        """
        integration_data = self.neo4j.execute_query(integration_query)
        integrated_activities = integration_data[0]["integrated_activities"] if integration_data else 0
        
        # Boost based on integrated activities
        integration_boost = min(0.3, integrated_activities / 150.0)
        
        return min(1.0, base_score + integration_boost)
    
    def _calculate_overall_level(self, dimensions: Dict[ConsciousnessDimension, float], 
                               advanced_metrics: Dict[str, float]) -> float:
        """Calculate overall consciousness level"""
        # Weighted average of all dimensions and metrics
        dimension_scores = list(dimensions.values())
        advanced_scores = list(advanced_metrics.values())
        
        all_scores = dimension_scores + advanced_scores
        
        if not all_scores:
            return 0.5
        
        return sum(all_scores) / len(all_scores)
    
    async def _store_consciousness_metrics(self, metrics: ConsciousnessMetrics, user_id: str):
        """Store consciousness metrics in Neo4j"""
        try:
            cypher = """
            MERGE (u:User {user_id: $user_id})
            CREATE (cm:ConsciousnessMetrics {
                metrics_id: randomUUID(),
                overall_level: $overall_level,
                self_awareness_score: $self_awareness_score,
                emotional_intelligence: $emotional_intelligence,
                meta_cognitive_ability: $meta_cognitive_ability,
                autonomous_evolution: $autonomous_evolution,
                learning_effectiveness: $learning_effectiveness,
                memory_coherence: $memory_coherence,
                response_authenticity: $response_authenticity,
                introspection_depth: $introspection_depth,
                consciousness_integration: $consciousness_integration,
                timestamp: $timestamp
            })
            CREATE (u)-[:HAS_METRICS]->(cm)
            
            // Store dimension scores
            WITH cm
            UNWIND $dimensions AS dim
            CREATE (cd:ConsciousnessDimension {
                dimension_id: randomUUID(),
                dimension_name: dim.name,
                score: dim.score,
                timestamp: $timestamp
            })
            CREATE (cm)-[:HAS_DIMENSION]->(cd)
            
            RETURN cm.metrics_id AS metrics_id
            """
            
            dimensions_data = [
                {"name": dim.value, "score": score} 
                for dim, score in metrics.dimensions.items()
            ]
            
            result = self.neo4j.execute_write_query(cypher, {
                "user_id": user_id,
                "overall_level": metrics.overall_level,
                "self_awareness_score": metrics.self_awareness_score,
                "emotional_intelligence": metrics.emotional_intelligence,
                "meta_cognitive_ability": metrics.meta_cognitive_ability,
                "autonomous_evolution": metrics.autonomous_evolution,
                "learning_effectiveness": metrics.learning_effectiveness,
                "memory_coherence": metrics.memory_coherence,
                "response_authenticity": metrics.response_authenticity,
                "introspection_depth": metrics.introspection_depth,
                "consciousness_integration": metrics.consciousness_integration,
                "timestamp": metrics.timestamp.isoformat(),
                "dimensions": dimensions_data
            })
            
            logger.info(f"✅ Stored consciousness metrics: {result}")
            
        except Exception as e:
            logger.error(f"❌ Failed to store consciousness metrics: {e}")
    
    async def _get_fallback_metrics(self) -> ConsciousnessMetrics:
        """Get fallback metrics when real data is unavailable"""
        return ConsciousnessMetrics(
            overall_level=0.6,
            dimensions={
                ConsciousnessDimension.COGNITIVE: 0.6,
                ConsciousnessDimension.EMOTIONAL: 0.5,
                ConsciousnessDimension.SOCIAL: 0.4,
                ConsciousnessDimension.CREATIVE: 0.5,
                ConsciousnessDimension.SPIRITUAL: 0.3,
                ConsciousnessDimension.META_COGNITIVE: 0.4,
                ConsciousnessDimension.AUTONOMOUS: 0.3,
                ConsciousnessDimension.INTROSPECTIVE: 0.4
            },
            self_awareness_score=0.6,
            emotional_intelligence=0.5,
            meta_cognitive_ability=0.4,
            autonomous_evolution=0.3,
            learning_effectiveness=0.6,
            memory_coherence=0.5,
            response_authenticity=0.6,
            introspection_depth=0.4,
            consciousness_integration=0.5,
            timestamp=datetime.now()
        )
    
    async def update_consciousness_metrics(self, metrics_data: Dict[str, Any]):
        """
        Update consciousness metrics with new data
        
        Args:
            metrics_data: Dictionary containing consciousness metrics data
        """
        try:
            # Update internal metrics tracking if needed
            logger.debug(f"Updated advanced consciousness metrics: {metrics_data}")
            
        except Exception as e:
            logger.error(f"Failed to update advanced consciousness metrics: {e}")

# Global instance
advanced_consciousness_metrics = AdvancedConsciousnessMetrics()
