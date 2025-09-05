"""
Knowledge Graph Evolution System
Context7 MCP-compliant dynamic management of concepts, memories, and relationships
Provides consciousness-aware evolution and learning-based updates
"""
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import asyncio
import json
import uuid
from backend.utils.neo4j_production import neo4j_production
from backend.utils.embedding_enhanced import get_embedding
from backend.core.performance_optimization import PerformanceOptimizer
from backend.core.enhanced_error_handling import ErrorHandler, ErrorSeverity, handle_errors

logger = logging.getLogger(__name__)
error_handler = ErrorHandler()
performance_optimizer = PerformanceOptimizer()

class EntityType(Enum):
    CONCEPT = "concept"
    MEMORY = "memory"
    RELATIONSHIP = "relationship"

class EvolutionAction(Enum):
    CREATE = "create"
    UPDATE = "update"
    STRENGTHEN = "strengthen"
    WEAKEN = "weaken"
    CONSOLIDATE = "consolidate"
    ARCHIVE = "archive"

@dataclass
class ConceptEvolution:
    concept_id: str
    importance_score: float
    usage_frequency: int
    last_accessed: datetime
    relationship_count: int
    consciousness_relevance: float

@dataclass
class MemoryEvolution:
    memory_id: str
    significance_score: float
    access_count: int
    last_accessed: datetime
    consolidation_candidate: bool
    consciousness_impact: float

@dataclass
class RelationshipEvolution:
    source_id: str
    target_id: str
    relationship_type: str
    strength: float
    usage_count: int
    last_used: datetime
    decay_rate: float

class KnowledgeGraphEvolutionManager:
    """
    Context7 MCP-compliant knowledge graph evolution system
    Manages dynamic updates, learning-based evolution, and consciousness integration
    """
    
    def __init__(self):
        self.performance_optimizer = performance_optimizer
        self.evolution_history = []
        self.consolidation_threshold = 0.8
        self.archival_threshold = 0.2
        self.relationship_decay_rate = 0.95  # 5% decay per period
        
    @handle_errors(
        component="knowledge_graph_evolution",
        fallback_result={},
        suppress_errors=True
    )
    async def evolve_concept(
        self,
        concept_id: str,
        interaction_context: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evolve a concept based on interaction and consciousness context
        
        Args:
            concept_id: The concept to evolve
            interaction_context: Context from recent interactions
            consciousness_context: Current consciousness state
            
        Returns:
            Evolution results and actions taken
        """
        try:
            logger.info(f"🧠 Evolving concept: {concept_id}")
            
            # Get current concept state
            concept_state = await self._get_concept_evolution_state(concept_id)
            
            if not concept_state:
                logger.warning(f"Concept {concept_id} not found for evolution")
                return {"error": "Concept not found"}
            
            # Calculate evolution parameters
            evolution_params = self._calculate_concept_evolution_params(
                concept_state, interaction_context, consciousness_context
            )
            
            # Apply evolution actions
            evolution_actions = []
            
            # Update importance score
            if evolution_params["importance_delta"] != 0:
                new_importance = max(0.0, min(1.0, 
                    concept_state.importance_score + evolution_params["importance_delta"]
                ))
                await self._update_concept_importance(concept_id, new_importance)
                evolution_actions.append({
                    "action": EvolutionAction.UPDATE.value,
                    "field": "importance_score",
                    "old_value": concept_state.importance_score,
                    "new_value": new_importance
                })
            
            # Update consciousness relevance
            consciousness_level = consciousness_context.get("consciousness_level", 0.7)
            emotional_state = consciousness_context.get("emotional_state", "curious")
            
            relevance_boost = self._calculate_consciousness_relevance_boost(
                concept_id, consciousness_level, emotional_state, interaction_context
            )
            
            if relevance_boost > 0.1:
                new_relevance = min(1.0, concept_state.consciousness_relevance + relevance_boost)
                await self._update_concept_consciousness_relevance(concept_id, new_relevance)
                evolution_actions.append({
                    "action": EvolutionAction.STRENGTHEN.value,
                    "field": "consciousness_relevance",
                    "boost": relevance_boost,
                    "new_value": new_relevance
                })
            
            # Discover new relationships
            if evolution_params["relationship_discovery"]:
                new_relationships = await self._discover_concept_relationships(
                    concept_id, interaction_context, consciousness_context
                )
                
                for rel in new_relationships:
                    await self._create_concept_relationship(
                        concept_id, rel["target_concept"], rel["strength"], rel["context"]
                    )
                    evolution_actions.append({
                        "action": EvolutionAction.CREATE.value,
                        "type": "relationship",
                        "target": rel["target_concept"],
                        "strength": rel["strength"]
                    })
            
            # Record evolution
            await self._record_concept_evolution(concept_id, evolution_actions, consciousness_context)
            
            logger.debug(f"✅ Concept {concept_id} evolved with {len(evolution_actions)} actions")
            
            return {
                "concept_id": concept_id,
                "evolution_actions": evolution_actions,
                "new_importance": concept_state.importance_score + evolution_params.get("importance_delta", 0),
                "consciousness_relevance": concept_state.consciousness_relevance + relevance_boost,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to evolve concept {concept_id}: {e}")
            return {"error": str(e)}
    
    @handle_errors(
        component="knowledge_graph_evolution",
        fallback_result={},
        suppress_errors=True
    )
    async def evolve_memory(
        self,
        memory_id: str,
        interaction_context: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evolve a memory based on interaction and consciousness context
        """
        try:
            logger.info(f"🧠 Evolving memory: {memory_id}")
            
            # Get current memory state
            memory_state = await self._get_memory_evolution_state(memory_id)
            
            if not memory_state:
                logger.warning(f"Memory {memory_id} not found for evolution")
                return {"error": "Memory not found"}
            
            # Calculate evolution parameters
            evolution_params = self._calculate_memory_evolution_params(
                memory_state, interaction_context, consciousness_context
            )
            
            evolution_actions = []
            
            # Update significance score
            if evolution_params["significance_delta"] != 0:
                new_significance = max(0.0, min(1.0,
                    memory_state.significance_score + evolution_params["significance_delta"]
                ))
                await self._update_memory_significance(memory_id, new_significance)
                evolution_actions.append({
                    "action": EvolutionAction.UPDATE.value,
                    "field": "significance_score",
                    "old_value": memory_state.significance_score,
                    "new_value": new_significance
                })
            
            # Check for consolidation opportunity
            if evolution_params["consolidation_candidate"]:
                similar_memories = await self._find_similar_memories(memory_id, similarity_threshold=0.8)
                
                if len(similar_memories) > 1:
                    consolidated_memory = await self._consolidate_memories(
                        [memory_id] + similar_memories, consciousness_context
                    )
                    evolution_actions.append({
                        "action": EvolutionAction.CONSOLIDATE.value,
                        "consolidated_memories": len(similar_memories) + 1,
                        "new_memory_id": consolidated_memory["memory_id"]
                    })
            
            # Check for archival
            if (memory_state.significance_score < self.archival_threshold and 
                memory_state.access_count < 2 and
                (datetime.now() - memory_state.last_accessed).days > 30):
                
                await self._archive_memory(memory_id)
                evolution_actions.append({
                    "action": EvolutionAction.ARCHIVE.value,
                    "reason": "low_significance_and_usage"
                })
            
            # Record evolution
            await self._record_memory_evolution(memory_id, evolution_actions, consciousness_context)
            
            logger.debug(f"✅ Memory {memory_id} evolved with {len(evolution_actions)} actions")
            
            return {
                "memory_id": memory_id,
                "evolution_actions": evolution_actions,
                "new_significance": memory_state.significance_score + evolution_params.get("significance_delta", 0),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to evolve memory {memory_id}: {e}")
            return {"error": str(e)}
    
    @handle_errors(
        component="knowledge_graph_evolution",
        fallback_result={},
        suppress_errors=True
    )
    async def evolve_relationships(
        self,
        entity_id: str,
        entity_type: EntityType,
        interaction_context: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evolve relationships for a given entity based on usage patterns
        """
        try:
            logger.info(f"🧠 Evolving relationships for {entity_type.value}: {entity_id}")
            
            # Get current relationships
            relationships = await self._get_entity_relationships(entity_id, entity_type)
            
            evolution_actions = []
            
            for rel in relationships:
                # Calculate relationship evolution
                evolution_params = self._calculate_relationship_evolution_params(
                    rel, interaction_context, consciousness_context
                )
                
                # Strengthen frequently used relationships
                if evolution_params["usage_boost"] > 0:
                    new_strength = min(1.0, rel.strength + evolution_params["usage_boost"])
                    await self._update_relationship_strength(
                        rel.source_id, rel.target_id, rel.relationship_type, new_strength
                    )
                    evolution_actions.append({
                        "action": EvolutionAction.STRENGTHEN.value,
                        "relationship": f"{rel.source_id}->{rel.target_id}",
                        "old_strength": rel.strength,
                        "new_strength": new_strength
                    })
                
                # Apply decay to unused relationships
                if evolution_params["apply_decay"]:
                    decayed_strength = rel.strength * self.relationship_decay_rate
                    
                    if decayed_strength < 0.1:
                        # Remove very weak relationships
                        await self._remove_weak_relationship(
                            rel.source_id, rel.target_id, rel.relationship_type
                        )
                        evolution_actions.append({
                            "action": "remove",
                            "relationship": f"{rel.source_id}->{rel.target_id}",
                            "reason": "decay_below_threshold"
                        })
                    else:
                        await self._update_relationship_strength(
                            rel.source_id, rel.target_id, rel.relationship_type, decayed_strength
                        )
                        evolution_actions.append({
                            "action": EvolutionAction.WEAKEN.value,
                            "relationship": f"{rel.source_id}->{rel.target_id}",
                            "old_strength": rel.strength,
                            "new_strength": decayed_strength
                        })
            
            # Discover new relationships based on co-occurrence patterns
            new_relationships = await self._discover_entity_relationships(
                entity_id, entity_type, interaction_context, consciousness_context
            )
            
            for new_rel in new_relationships:
                await self._create_relationship(
                    new_rel["source_id"], new_rel["target_id"], 
                    new_rel["relationship_type"], new_rel["strength"]
                )
                evolution_actions.append({
                    "action": EvolutionAction.CREATE.value,
                    "relationship": f"{new_rel['source_id']}->{new_rel['target_id']}",
                    "type": new_rel["relationship_type"],
                    "strength": new_rel["strength"]
                })
            
            logger.debug(f"✅ Relationships evolved for {entity_id} with {len(evolution_actions)} actions")
            
            return {
                "entity_id": entity_id,
                "entity_type": entity_type.value,
                "evolution_actions": evolution_actions,
                "relationships_processed": len(relationships),
                "new_relationships": len(new_relationships),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to evolve relationships for {entity_id}: {e}")
            return {"error": str(e)}
    
    async def _get_concept_evolution_state(self, concept_id: str) -> Optional[ConceptEvolution]:
        """Get current evolution state of a concept"""
        try:
            cypher = """
            MATCH (c:Concept {concept_id: $concept_id})
            OPTIONAL MATCH (c)-[r:RELATES_TO]-()
            WITH c, count(r) as relationship_count
            RETURN c.concept_id as concept_id,
                   coalesce(c.importance_score, 0.5) as importance_score,
                   coalesce(c.usage_frequency, 0) as usage_frequency,
                   coalesce(c.last_accessed, timestamp()) as last_accessed,
                   relationship_count,
                   coalesce(c.consciousness_relevance, 0.5) as consciousness_relevance
            """
            
            result = neo4j_production.execute_query(cypher, {"concept_id": concept_id})
            
            if result and len(result) > 0:
                data = result[0]
                return ConceptEvolution(
                    concept_id=data["concept_id"],
                    importance_score=data["importance_score"],
                    usage_frequency=data["usage_frequency"],
                    last_accessed=datetime.fromtimestamp(data["last_accessed"] / 1000),
                    relationship_count=data["relationship_count"],
                    consciousness_relevance=data["consciousness_relevance"]
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get concept evolution state: {e}")
            return None
    
    async def _get_memory_evolution_state(self, memory_id: str) -> Optional[MemoryEvolution]:
        """Get current evolution state of a memory"""
        try:
            cypher = """
            MATCH (m:Memory {memory_id: $memory_id})
            RETURN m.memory_id as memory_id,
                   coalesce(m.significance_score, 0.5) as significance_score,
                   coalesce(m.access_count, 0) as access_count,
                   coalesce(m.last_accessed, m.created_at, timestamp()) as last_accessed,
                   coalesce(m.consolidation_candidate, false) as consolidation_candidate,
                   coalesce(m.consciousness_impact, 0.3) as consciousness_impact
            """
            
            result = neo4j_production.execute_query(cypher, {"memory_id": memory_id})
            
            if result and len(result) > 0:
                data = result[0]
                return MemoryEvolution(
                    memory_id=data["memory_id"],
                    significance_score=data["significance_score"],
                    access_count=data["access_count"],
                    last_accessed=datetime.fromtimestamp(data["last_accessed"] / 1000),
                    consolidation_candidate=data["consolidation_candidate"],
                    consciousness_impact=data["consciousness_impact"]
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get memory evolution state: {e}")
            return None
    
    def _calculate_concept_evolution_params(
        self,
        concept_state: ConceptEvolution,
        interaction_context: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate evolution parameters for a concept"""
        
        # Base importance delta
        importance_delta = 0.0
        
        # Boost importance if concept was mentioned in interaction
        query = interaction_context.get("query", "").lower()
        if concept_state.concept_id.lower() in query or any(
            keyword in query for keyword in interaction_context.get("related_keywords", [])
        ):
            importance_delta += 0.1
        
        # Consciousness level affects evolution sensitivity
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        importance_delta *= consciousness_level
        
        # Relationship discovery based on consciousness and interaction
        relationship_discovery = (
            consciousness_level > 0.7 and 
            concept_state.usage_frequency > 2 and
            len(interaction_context.get("related_concepts", [])) > 0
        )
        
        return {
            "importance_delta": importance_delta,
            "relationship_discovery": relationship_discovery,
            "consciousness_boost": consciousness_level > 0.8
        }
    
    def _calculate_memory_evolution_params(
        self,
        memory_state: MemoryEvolution,
        interaction_context: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate evolution parameters for a memory"""
        
        # Base significance delta
        significance_delta = 0.0
        
        # Boost significance if memory is relevant to current interaction
        if memory_state.memory_id in interaction_context.get("relevant_memories", []):
            significance_delta += 0.15
        
        # Consciousness impact affects significance
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        significance_delta *= consciousness_level
        
        # Check consolidation candidacy
        consolidation_candidate = (
            memory_state.access_count > 3 and
            memory_state.significance_score > 0.6 and
            not memory_state.consolidation_candidate
        )
        
        return {
            "significance_delta": significance_delta,
            "consolidation_candidate": consolidation_candidate,
            "consciousness_impact": consciousness_level * 0.2
        }
    
    def _calculate_relationship_evolution_params(
        self,
        relationship: RelationshipEvolution,
        interaction_context: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate evolution parameters for a relationship"""
        
        # Usage boost if relationship was traversed in interaction
        usage_boost = 0.0
        if (relationship.source_id in interaction_context.get("concepts_used", []) and
            relationship.target_id in interaction_context.get("concepts_used", [])):
            usage_boost = 0.1
        
        # Apply decay if relationship hasn't been used recently
        days_since_use = (datetime.now() - relationship.last_used).days
        apply_decay = days_since_use > 7  # Decay after a week of non-use
        
        return {
            "usage_boost": usage_boost,
            "apply_decay": apply_decay,
            "decay_factor": self.relationship_decay_rate
        }
    
    def _calculate_consciousness_relevance_boost(
        self,
        concept_id: str,
        consciousness_level: float,
        emotional_state: str,
        interaction_context: Dict[str, Any]
    ) -> float:
        """Calculate consciousness relevance boost for a concept"""
        
        boost = 0.0
        
        # Higher consciousness levels are more sensitive to relevance
        base_boost = consciousness_level * 0.1
        
        # Emotional state affects relevance
        emotional_boosts = {
            "curious": 0.15,
            "contemplative": 0.12,
            "focused": 0.08,
            "empathetic": 0.10,
            "excited": 0.13
        }
        
        emotional_boost = emotional_boosts.get(emotional_state, 0.05)
        
        # Interaction context affects relevance
        if concept_id in interaction_context.get("primary_concepts", []):
            boost += base_boost + emotional_boost
        elif concept_id in interaction_context.get("related_concepts", []):
            boost += (base_boost + emotional_boost) * 0.5
        
        return boost
    
    async def _update_concept_importance(self, concept_id: str, importance_score: float):
        """Update concept importance score"""
        cypher = """
        MATCH (c:Concept {concept_id: $concept_id})
        SET c.importance_score = $importance_score,
            c.last_updated = timestamp(),
            c.usage_frequency = coalesce(c.usage_frequency, 0) + 1
        """
        
        neo4j_production.execute_write_query(cypher, {
            "concept_id": concept_id,
            "importance_score": importance_score
        })
    
    async def _update_concept_consciousness_relevance(self, concept_id: str, relevance: float):
        """Update concept consciousness relevance"""
        cypher = """
        MATCH (c:Concept {concept_id: $concept_id})
        SET c.consciousness_relevance = $relevance,
            c.last_consciousness_update = timestamp()
        """
        
        neo4j_production.execute_write_query(cypher, {
            "concept_id": concept_id,
            "relevance": relevance
        })
    
    async def _update_memory_significance(self, memory_id: str, significance_score: float):
        """Update memory significance score"""
        cypher = """
        MATCH (m:Memory {memory_id: $memory_id})
        SET m.significance_score = $significance_score,
            m.last_updated = timestamp(),
            m.access_count = coalesce(m.access_count, 0) + 1
        """
        
        neo4j_production.execute_write_query(cypher, {
            "memory_id": memory_id,
            "significance_score": significance_score
        })
    
    async def _record_concept_evolution(
        self,
        concept_id: str,
        evolution_actions: List[Dict],
        consciousness_context: Dict[str, Any]
    ):
        """Record concept evolution for tracking"""
        try:
            cypher = """
            CREATE (ce:ConceptEvolution {
                evolution_id: randomUUID(),
                concept_id: $concept_id,
                actions: $actions,
                consciousness_level: $consciousness_level,
                emotional_state: $emotional_state,
                timestamp: timestamp()
            })
            
            WITH ce
            MATCH (c:Concept {concept_id: $concept_id})
            CREATE (ce)-[:EVOLVED]->(c)
            
            RETURN ce.evolution_id as evolution_id
            """
            
            neo4j_production.execute_write_query(cypher, {
                "concept_id": concept_id,
                "actions": json.dumps(evolution_actions),
                "consciousness_level": consciousness_context.get("consciousness_level", 0.7),
                "emotional_state": consciousness_context.get("emotional_state", "curious")
            })
            
        except Exception as e:
            logger.error(f"Failed to record concept evolution: {e}")
    
    async def _record_memory_evolution(
        self,
        memory_id: str,
        evolution_actions: List[Dict],
        consciousness_context: Dict[str, Any]
    ):
        """Record memory evolution for tracking"""
        try:
            cypher = """
            CREATE (me:MemoryEvolution {
                evolution_id: randomUUID(),
                memory_id: $memory_id,
                actions: $actions,
                consciousness_level: $consciousness_level,
                emotional_state: $emotional_state,
                timestamp: timestamp()
            })
            
            WITH me
            MATCH (m:Memory {memory_id: $memory_id})
            CREATE (me)-[:EVOLVED]->(m)
            
            RETURN me.evolution_id as evolution_id
            """
            
            neo4j_production.execute_write_query(cypher, {
                "memory_id": memory_id,
                "actions": json.dumps(evolution_actions),
                "consciousness_level": consciousness_context.get("consciousness_level", 0.7),
                "emotional_state": consciousness_context.get("emotional_state", "curious")
            })
            
        except Exception as e:
            logger.error(f"Failed to record memory evolution: {e}")

# Global instance
knowledge_graph_evolution_manager = KnowledgeGraphEvolutionManager()