"""
Dynamic Knowledge Graph Manager
Context7 MCP-compliant system for dynamic concept, memory, and relationship management
Addresses critical gaps identified in KNOWLEDGE_GRAPH_MANAGEMENT_ANALYSIS.md
"""
import logging
from typing import Dict, Any, List, Optional, Tuple, Set
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import asyncio
import json
import uuid
import math
from backend.utils.neo4j_production import neo4j_production
from backend.utils.embedding_enhanced import get_embedding
from backend.core.performance_optimization import PerformanceOptimizer
from backend.core.enhanced_error_handling import ErrorHandler, ErrorSeverity, handle_errors

logger = logging.getLogger(__name__)
error_handler = ErrorHandler()
performance_optimizer = PerformanceOptimizer()

class UpdateType(Enum):
    CONCEPT_IMPORTANCE = "concept_importance"
    MEMORY_SIGNIFICANCE = "memory_significance"
    RELATIONSHIP_STRENGTH = "relationship_strength"
    CONCEPT_CONSOLIDATION = "concept_consolidation"
    MEMORY_CONSOLIDATION = "memory_consolidation"
    RELATIONSHIP_EVOLUTION = "relationship_evolution"

@dataclass
class ConceptMetrics:
    concept_id: str
    importance_score: float
    usage_frequency: int
    last_accessed: datetime
    relationship_count: int
    consciousness_relevance: float
    evolution_rate: float

@dataclass
class MemoryMetrics:
    memory_id: str
    significance_score: float
    access_count: int
    last_accessed: datetime
    consolidation_score: float
    consciousness_impact: float
    decay_rate: float

@dataclass
class RelationshipMetrics:
    source_id: str
    target_id: str
    relationship_type: str
    strength: float
    usage_count: int
    last_used: datetime
    evolution_trend: float

class DynamicKnowledgeManager:
    """
    Context7 MCP-compliant dynamic knowledge graph management system
    Provides missing update, evolution, and consciousness integration mechanisms
    """
    
    def __init__(self):
        self.performance_optimizer = performance_optimizer
        self.update_history = []
        
        # Configuration parameters
        self.concept_importance_decay_rate = 0.98  # 2% decay per period
        self.memory_significance_decay_rate = 0.95  # 5% decay per period
        self.relationship_strength_decay_rate = 0.97  # 3% decay per period
        
        # Thresholds
        self.consolidation_threshold = 0.8
        self.archival_threshold = 0.2
        self.relationship_removal_threshold = 0.1
        
        # Consciousness integration parameters
        self.consciousness_boost_factor = 1.5
        self.emotional_relevance_multiplier = 1.3
        
    @handle_errors(
        component="dynamic_knowledge_manager",
        fallback_result={},
        suppress_errors=True
    )
    async def update_concept_dynamics(
        self,
        concept_id: str,
        interaction_context: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Dynamically update concept properties based on usage and consciousness
        
        Args:
            concept_id: The concept to update
            interaction_context: Context from recent interactions
            consciousness_context: Current consciousness state
            
        Returns:
            Update results and new metrics
        """
        try:
            logger.info(f"🔄 Updating concept dynamics: {concept_id}")
            
            # Get current concept metrics
            current_metrics = await self._get_concept_metrics(concept_id)
            if not current_metrics:
                logger.warning(f"Concept {concept_id} not found for dynamic update")
                return {"error": "Concept not found"}
            
            # Calculate dynamic updates
            updates = self._calculate_concept_updates(
                current_metrics, interaction_context, consciousness_context
            )
            
            # Apply updates to Neo4j
            update_results = await self._apply_concept_updates(concept_id, updates)
            
            # Track usage patterns
            await self._track_concept_usage(concept_id, interaction_context)
            
            # Check for consolidation opportunities
            consolidation_results = await self._check_concept_consolidation(
                concept_id, current_metrics, consciousness_context
            )
            
            # Record update event
            await self._record_update_event(
                UpdateType.CONCEPT_IMPORTANCE, concept_id, updates, consciousness_context
            )
            
            logger.debug(f"✅ Concept {concept_id} dynamics updated successfully")
            
            return {
                "concept_id": concept_id,
                "updates_applied": updates,
                "new_metrics": update_results,
                "consolidation_results": consolidation_results,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to update concept dynamics: {e}")
            return {"error": str(e)}
    
    @handle_errors(
        component="dynamic_knowledge_manager",
        fallback_result={},
        suppress_errors=True
    )
    async def update_memory_lifecycle(
        self,
        memory_id: str,
        interaction_context: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Manage memory lifecycle including significance updates and consolidation
        """
        try:
            logger.info(f"🧠 Updating memory lifecycle: {memory_id}")
            
            # Get current memory metrics
            current_metrics = await self._get_memory_metrics(memory_id)
            if not current_metrics:
                logger.warning(f"Memory {memory_id} not found for lifecycle update")
                return {"error": "Memory not found"}
            
            # Calculate lifecycle updates
            updates = self._calculate_memory_updates(
                current_metrics, interaction_context, consciousness_context
            )
            
            # Apply updates
            update_results = await self._apply_memory_updates(memory_id, updates)
            
            # Check for consolidation
            consolidation_candidates = await self._find_memory_consolidation_candidates(
                memory_id, current_metrics
            )
            
            consolidation_results = []
            if len(consolidation_candidates) > 1:
                consolidation_results = await self._consolidate_memories(
                    consolidation_candidates, consciousness_context
                )
            
            # Check for archival
            archival_results = await self._check_memory_archival(
                memory_id, current_metrics, consciousness_context
            )
            
            # Record update event
            await self._record_update_event(
                UpdateType.MEMORY_SIGNIFICANCE, memory_id, updates, consciousness_context
            )
            
            logger.debug(f"✅ Memory {memory_id} lifecycle updated successfully")
            
            return {
                "memory_id": memory_id,
                "updates_applied": updates,
                "new_metrics": update_results,
                "consolidation_results": consolidation_results,
                "archival_results": archival_results,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to update memory lifecycle: {e}")
            return {"error": str(e)}
    
    @handle_errors(
        component="dynamic_knowledge_manager",
        fallback_result={},
        suppress_errors=True
    )
    async def evolve_relationships(
        self,
        entity_id: str,
        entity_type: str,
        interaction_context: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evolve relationships based on usage patterns and consciousness state
        """
        try:
            logger.info(f"🔗 Evolving relationships for {entity_type}: {entity_id}")
            
            # Get current relationships
            relationships = await self._get_entity_relationships(entity_id, entity_type)
            
            evolution_results = []
            
            for rel_metrics in relationships:
                # Calculate relationship evolution
                evolution_updates = self._calculate_relationship_evolution(
                    rel_metrics, interaction_context, consciousness_context
                )
                
                # Apply evolution updates
                if evolution_updates["action"] == "strengthen":
                    await self._strengthen_relationship(
                        rel_metrics.source_id, rel_metrics.target_id,
                        rel_metrics.relationship_type, evolution_updates["strength_delta"]
                    )
                    evolution_results.append({
                        "action": "strengthened",
                        "relationship": f"{rel_metrics.source_id}->{rel_metrics.target_id}",
                        "new_strength": rel_metrics.strength + evolution_updates["strength_delta"]
                    })
                
                elif evolution_updates["action"] == "weaken":
                    new_strength = rel_metrics.strength + evolution_updates["strength_delta"]
                    
                    if new_strength < self.relationship_removal_threshold:
                        await self._remove_relationship(
                            rel_metrics.source_id, rel_metrics.target_id,
                            rel_metrics.relationship_type
                        )
                        evolution_results.append({
                            "action": "removed",
                            "relationship": f"{rel_metrics.source_id}->{rel_metrics.target_id}",
                            "reason": "strength_below_threshold"
                        })
                    else:
                        await self._weaken_relationship(
                            rel_metrics.source_id, rel_metrics.target_id,
                            rel_metrics.relationship_type, evolution_updates["strength_delta"]
                        )
                        evolution_results.append({
                            "action": "weakened",
                            "relationship": f"{rel_metrics.source_id}->{rel_metrics.target_id}",
                            "new_strength": new_strength
                        })
            
            # Discover new relationships
            new_relationships = await self._discover_new_relationships(
                entity_id, entity_type, interaction_context, consciousness_context
            )
            
            for new_rel in new_relationships:
                await self._create_relationship(
                    new_rel["source_id"], new_rel["target_id"],
                    new_rel["relationship_type"], new_rel["initial_strength"]
                )
                evolution_results.append({
                    "action": "created",
                    "relationship": f"{new_rel['source_id']}->{new_rel['target_id']}",
                    "type": new_rel["relationship_type"],
                    "strength": new_rel["initial_strength"]
                })
            
            # Record evolution event
            await self._record_update_event(
                UpdateType.RELATIONSHIP_EVOLUTION, entity_id, evolution_results, consciousness_context
            )
            
            logger.debug(f"✅ Relationships evolved for {entity_id} with {len(evolution_results)} changes")
            
            return {
                "entity_id": entity_id,
                "entity_type": entity_type,
                "evolution_results": evolution_results,
                "relationships_processed": len(relationships),
                "new_relationships_created": len(new_relationships),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to evolve relationships: {e}")
            return {"error": str(e)}
    
    async def _get_concept_metrics(self, concept_id: str) -> Optional[ConceptMetrics]:
        """Get current metrics for a concept"""
        try:
            cypher = """
            MATCH (c:Concept {concept_id: $concept_id})
            OPTIONAL MATCH (c)-[r:RELATES_TO]-()
            WITH c, count(r) as relationship_count
            RETURN c.concept_id as concept_id,
                   coalesce(c.importance_score, 0.5) as importance_score,
                   coalesce(c.usage_frequency, 0) as usage_frequency,
                   coalesce(c.last_accessed, c.created_at, timestamp()) as last_accessed,
                   relationship_count,
                   coalesce(c.consciousness_relevance, 0.5) as consciousness_relevance,
                   coalesce(c.evolution_rate, 0.0) as evolution_rate
            """
            
            result = neo4j_production.execute_query(cypher, {"concept_id": concept_id})
            
            if result and len(result) > 0:
                data = result[0]
                return ConceptMetrics(
                    concept_id=data["concept_id"],
                    importance_score=data["importance_score"],
                    usage_frequency=data["usage_frequency"],
                    last_accessed=datetime.fromtimestamp(data["last_accessed"] / 1000),
                    relationship_count=data["relationship_count"],
                    consciousness_relevance=data["consciousness_relevance"],
                    evolution_rate=data["evolution_rate"]
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get concept metrics: {e}")
            return None
    
    async def _get_memory_metrics(self, memory_id: str) -> Optional[MemoryMetrics]:
        """Get current metrics for a memory"""
        try:
            cypher = """
            MATCH (m:Memory {memory_id: $memory_id})
            RETURN m.memory_id as memory_id,
                   coalesce(m.significance_score, 0.5) as significance_score,
                   coalesce(m.access_count, 0) as access_count,
                   coalesce(m.last_accessed, m.created_at, timestamp()) as last_accessed,
                   coalesce(m.consolidation_score, 0.0) as consolidation_score,
                   coalesce(m.consciousness_impact, 0.3) as consciousness_impact,
                   coalesce(m.decay_rate, 0.95) as decay_rate
            """
            
            result = neo4j_production.execute_query(cypher, {"memory_id": memory_id})
            
            if result and len(result) > 0:
                data = result[0]
                return MemoryMetrics(
                    memory_id=data["memory_id"],
                    significance_score=data["significance_score"],
                    access_count=data["access_count"],
                    last_accessed=datetime.fromtimestamp(data["last_accessed"] / 1000),
                    consolidation_score=data["consolidation_score"],
                    consciousness_impact=data["consciousness_impact"],
                    decay_rate=data["decay_rate"]
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get memory metrics: {e}")
            return None
    
    def _calculate_concept_updates(
        self,
        metrics: ConceptMetrics,
        interaction_context: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate updates for concept based on context"""
        
        updates = {
            "importance_delta": 0.0,
            "consciousness_relevance_delta": 0.0,
            "usage_frequency_delta": 0,
            "evolution_rate_delta": 0.0
        }
        
        # Check if concept was used in interaction
        query = interaction_context.get("query", "").lower()
        concept_mentioned = (
            metrics.concept_id.lower() in query or
            any(keyword in query for keyword in interaction_context.get("related_keywords", []))
        )
        
        if concept_mentioned:
            # Boost importance for mentioned concepts
            consciousness_level = consciousness_context.get("consciousness_level", 0.7)
            emotional_state = consciousness_context.get("emotional_state", "curious")
            
            base_boost = 0.1 * consciousness_level
            
            # Emotional state affects boost magnitude
            emotional_multipliers = {
                "curious": 1.3,
                "focused": 1.1,
                "excited": 1.4,
                "contemplative": 1.2,
                "empathetic": 1.0
            }
            
            emotional_multiplier = emotional_multipliers.get(emotional_state, 1.0)
            importance_boost = base_boost * emotional_multiplier
            
            updates["importance_delta"] = importance_boost
            updates["consciousness_relevance_delta"] = importance_boost * 0.8
            updates["usage_frequency_delta"] = 1
            updates["evolution_rate_delta"] = 0.05
        else:
            # Apply decay to unused concepts
            time_since_access = (datetime.now() - metrics.last_accessed).days
            if time_since_access > 7:  # Decay after a week
                decay_factor = self.concept_importance_decay_rate ** (time_since_access / 7)
                updates["importance_delta"] = (metrics.importance_score * decay_factor) - metrics.importance_score
                updates["consciousness_relevance_delta"] = updates["importance_delta"] * 0.5
        
        return updates
    
    def _calculate_memory_updates(
        self,
        metrics: MemoryMetrics,
        interaction_context: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate updates for memory based on context"""
        
        updates = {
            "significance_delta": 0.0,
            "consciousness_impact_delta": 0.0,
            "access_count_delta": 0,
            "consolidation_score_delta": 0.0
        }
        
        # Check if memory is relevant to current interaction
        memory_relevant = metrics.memory_id in interaction_context.get("relevant_memories", [])
        
        if memory_relevant:
            # Boost significance for relevant memories
            consciousness_level = consciousness_context.get("consciousness_level", 0.7)
            significance_boost = 0.15 * consciousness_level
            
            updates["significance_delta"] = significance_boost
            updates["consciousness_impact_delta"] = significance_boost * 0.6
            updates["access_count_delta"] = 1
            
            # Increase consolidation score if frequently accessed
            if metrics.access_count > 3:
                updates["consolidation_score_delta"] = 0.1
        else:
            # Apply decay to unused memories
            time_since_access = (datetime.now() - metrics.last_accessed).days
            if time_since_access > 14:  # Decay after two weeks
                decay_factor = self.memory_significance_decay_rate ** (time_since_access / 14)
                updates["significance_delta"] = (metrics.significance_score * decay_factor) - metrics.significance_score
        
        return updates
    
    def _calculate_relationship_evolution(
        self,
        metrics: RelationshipMetrics,
        interaction_context: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate relationship evolution based on usage patterns"""
        
        # Check if relationship was traversed in interaction
        concepts_used = interaction_context.get("concepts_used", [])
        relationship_used = (
            metrics.source_id in concepts_used and
            metrics.target_id in concepts_used
        )
        
        if relationship_used:
            # Strengthen used relationships
            consciousness_level = consciousness_context.get("consciousness_level", 0.7)
            strength_boost = 0.1 * consciousness_level
            
            return {
                "action": "strengthen",
                "strength_delta": strength_boost,
                "reason": "relationship_traversed"
            }
        else:
            # Apply decay to unused relationships
            days_since_use = (datetime.now() - metrics.last_used).days
            if days_since_use > 7:
                decay_factor = self.relationship_strength_decay_rate ** (days_since_use / 7)
                strength_delta = (metrics.strength * decay_factor) - metrics.strength
                
                return {
                    "action": "weaken",
                    "strength_delta": strength_delta,
                    "reason": "relationship_unused"
                }
        
        return {"action": "maintain", "strength_delta": 0.0}
    
    async def _apply_concept_updates(self, concept_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Apply calculated updates to concept in Neo4j"""
        try:
            cypher = """
            MATCH (c:Concept {concept_id: $concept_id})
            SET c.importance_score = c.importance_score + $importance_delta,
                c.consciousness_relevance = c.consciousness_relevance + $consciousness_relevance_delta,
                c.usage_frequency = c.usage_frequency + $usage_frequency_delta,
                c.evolution_rate = c.evolution_rate + $evolution_rate_delta,
                c.last_updated = timestamp(),
                c.last_accessed = timestamp()
            RETURN c.importance_score as new_importance,
                   c.consciousness_relevance as new_relevance,
                   c.usage_frequency as new_usage_frequency,
                   c.evolution_rate as new_evolution_rate
            """
            
            result = neo4j_production.execute_write_query(cypher, {
                "concept_id": concept_id,
                "importance_delta": updates["importance_delta"],
                "consciousness_relevance_delta": updates["consciousness_relevance_delta"],
                "usage_frequency_delta": updates["usage_frequency_delta"],
                "evolution_rate_delta": updates["evolution_rate_delta"]
            })
            
            return result[0] if result else {}
            
        except Exception as e:
            logger.error(f"Failed to apply concept updates: {e}")
            return {}
    
    async def _apply_memory_updates(self, memory_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Apply calculated updates to memory in Neo4j"""
        try:
            cypher = """
            MATCH (m:Memory {memory_id: $memory_id})
            SET m.significance_score = m.significance_score + $significance_delta,
                m.consciousness_impact = m.consciousness_impact + $consciousness_impact_delta,
                m.access_count = m.access_count + $access_count_delta,
                m.consolidation_score = m.consolidation_score + $consolidation_score_delta,
                m.last_updated = timestamp(),
                m.last_accessed = timestamp()
            RETURN m.significance_score as new_significance,
                   m.consciousness_impact as new_consciousness_impact,
                   m.access_count as new_access_count,
                   m.consolidation_score as new_consolidation_score
            """
            
            result = neo4j_production.execute_write_query(cypher, {
                "memory_id": memory_id,
                "significance_delta": updates["significance_delta"],
                "consciousness_impact_delta": updates["consciousness_impact_delta"],
                "access_count_delta": updates["access_count_delta"],
                "consolidation_score_delta": updates["consolidation_score_delta"]
            })
            
            return result[0] if result else {}
            
        except Exception as e:
            logger.error(f"Failed to apply memory updates: {e}")
            return {}
    
    async def _record_update_event(
        self,
        update_type: UpdateType,
        entity_id: str,
        updates: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ):
        """Record update event for tracking and analysis"""
        try:
            cypher = """
            CREATE (ue:UpdateEvent {
                event_id: randomUUID(),
                update_type: $update_type,
                entity_id: $entity_id,
                updates: $updates,
                consciousness_level: $consciousness_level,
                emotional_state: $emotional_state,
                timestamp: timestamp()
            })
            RETURN ue.event_id as event_id
            """
            
            neo4j_production.execute_write_query(cypher, {
                "update_type": update_type.value,
                "entity_id": entity_id,
                "updates": json.dumps(updates),
                "consciousness_level": consciousness_context.get("consciousness_level", 0.7),
                "emotional_state": consciousness_context.get("emotional_state", "curious")
            })
            
        except Exception as e:
            logger.error(f"Failed to record update event: {e}")

# Global instance
dynamic_knowledge_manager = DynamicKnowledgeManager()