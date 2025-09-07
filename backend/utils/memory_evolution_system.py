"""
Memory Evolution System
Advanced system for memory evolution, adaptation, and growth
"""
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import asyncio
import json
import numpy as np

from backend.utils.neo4j_production import neo4j_production
from backend.utils.advanced_memory_architecture import advanced_memory_architecture, MemoryType, MemoryConsolidationLevel
from backend.utils.embedding_enhanced import embedding_manager

logger = logging.getLogger(__name__)

class EvolutionTrigger(Enum):
    """Memory evolution triggers"""
    CONSCIOUSNESS_GROWTH = "consciousness_growth"
    EMOTIONAL_BREAKTHROUGH = "emotional_breakthrough"
    LEARNING_MILESTONE = "learning_milestone"
    MEMORY_CONFLICT = "memory_conflict"
    ASSOCIATION_STRENGTHENING = "association_strengthening"
    TEMPORAL_PATTERN = "temporal_pattern"
    CONCEPTUAL_INTEGRATION = "conceptual_integration"
    EXPERIENTIAL_ACCUMULATION = "experiential_accumulation"

class EvolutionType(Enum):
    """Types of memory evolution"""
    IMPORTANCE_EVOLUTION = "importance_evolution"
    EMOTIONAL_EVOLUTION = "emotional_evolution"
    CONSCIOUSNESS_EVOLUTION = "consciousness_evolution"
    ASSOCIATION_EVOLUTION = "association_evolution"
    CONCEPTUAL_EVOLUTION = "conceptual_evolution"
    TEMPORAL_EVOLUTION = "temporal_evolution"
    STRUCTURAL_EVOLUTION = "structural_evolution"

@dataclass
class EvolutionEvent:
    """Memory evolution event"""
    event_id: str
    memory_id: str
    evolution_type: EvolutionType
    trigger: EvolutionTrigger
    before_state: Dict[str, Any]
    after_state: Dict[str, Any]
    evolution_data: Dict[str, Any]
    timestamp: datetime
    significance: float

@dataclass
class EvolutionPattern:
    """Memory evolution pattern"""
    pattern_id: str
    pattern_type: str
    memory_ids: List[str]
    evolution_sequence: List[EvolutionEvent]
    pattern_strength: float
    evolution_velocity: float
    insights: Dict[str, Any]
    timestamp: datetime

class MemoryEvolutionSystem:
    """
    Advanced memory evolution system
    """
    
    def __init__(self):
        self.neo4j = neo4j_production
        self.memory_architecture = advanced_memory_architecture
        self.embedding_manager = embedding_manager
        
        # Evolution parameters
        self.evolution_threshold = 0.6
        self.significance_threshold = 0.5
        self.pattern_threshold = 0.7
        
        # Evolution triggers
        self.evolution_triggers = self._initialize_evolution_triggers()
    
    def _initialize_evolution_triggers(self) -> List[EvolutionTrigger]:
        """Initialize memory evolution triggers"""
        return [
            EvolutionTrigger.CONSCIOUSNESS_GROWTH,
            EvolutionTrigger.EMOTIONAL_BREAKTHROUGH,
            EvolutionTrigger.LEARNING_MILESTONE,
            EvolutionTrigger.MEMORY_CONFLICT,
            EvolutionTrigger.ASSOCIATION_STRENGTHENING,
            EvolutionTrigger.TEMPORAL_PATTERN,
            EvolutionTrigger.CONCEPTUAL_INTEGRATION,
            EvolutionTrigger.EXPERIENTIAL_ACCUMULATION
        ]
    
    async def evolve_memory(
        self,
        memory_id: str,
        evolution_type: EvolutionType,
        trigger: EvolutionTrigger,
        evolution_data: Dict[str, Any],
        user_id: str = "mainza-user"
    ) -> Optional[EvolutionEvent]:
        """Evolve a specific memory"""
        try:
            logger.info(f"🔄 Evolving memory: {memory_id} with {evolution_type.value}")
            
            # Get current memory state
            current_memory = await self._get_memory_by_id(memory_id, user_id)
            if not current_memory:
                logger.warning(f"Memory not found: {memory_id}")
                return None
            
            # Calculate evolution changes
            evolution_changes = await self._calculate_evolution_changes(
                current_memory, evolution_type, trigger, evolution_data
            )
            
            if not evolution_changes:
                logger.info(f"No evolution changes needed for memory: {memory_id}")
                return None
            
            # Apply evolution changes
            evolved_memory = await self._apply_evolution_changes(
                memory_id, evolution_changes, user_id
            )
            
            if not evolved_memory:
                logger.warning(f"Failed to apply evolution changes to memory: {memory_id}")
                return None
            
            # Create evolution event
            evolution_event = EvolutionEvent(
                event_id=f"evolution_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
                memory_id=memory_id,
                evolution_type=evolution_type,
                trigger=trigger,
                before_state=current_memory,
                after_state=evolved_memory,
                evolution_data=evolution_data,
                timestamp=datetime.now(),
                significance=self._calculate_evolution_significance(evolution_changes)
            )
            
            # Store evolution event
            await self._store_evolution_event(evolution_event, user_id)
            
            logger.info(f"✅ Memory evolved: {memory_id} (significance: {evolution_event.significance:.3f})")
            return evolution_event
            
        except Exception as e:
            logger.error(f"❌ Failed to evolve memory: {e}")
            return None
    
    async def detect_evolution_triggers(self, user_id: str = "mainza-user") -> List[EvolutionTrigger]:
        """Detect memory evolution triggers"""
        try:
            logger.info("🔍 Detecting memory evolution triggers")
            
            triggers = []
            
            # Check consciousness growth
            if await self._check_consciousness_growth_trigger(user_id):
                triggers.append(EvolutionTrigger.CONSCIOUSNESS_GROWTH)
            
            # Check emotional breakthrough
            if await self._check_emotional_breakthrough_trigger(user_id):
                triggers.append(EvolutionTrigger.EMOTIONAL_BREAKTHROUGH)
            
            # Check learning milestone
            if await self._check_learning_milestone_trigger(user_id):
                triggers.append(EvolutionTrigger.LEARNING_MILESTONE)
            
            # Check memory conflicts
            if await self._check_memory_conflict_trigger(user_id):
                triggers.append(EvolutionTrigger.MEMORY_CONFLICT)
            
            # Check association strengthening
            if await self._check_association_strengthening_trigger(user_id):
                triggers.append(EvolutionTrigger.ASSOCIATION_STRENGTHENING)
            
            # Check temporal patterns
            if await self._check_temporal_pattern_trigger(user_id):
                triggers.append(EvolutionTrigger.TEMPORAL_PATTERN)
            
            # Check conceptual integration
            if await self._check_conceptual_integration_trigger(user_id):
                triggers.append(EvolutionTrigger.CONCEPTUAL_INTEGRATION)
            
            # Check experiential accumulation
            if await self._check_experiential_accumulation_trigger(user_id):
                triggers.append(EvolutionTrigger.EXPERIENTIAL_ACCUMULATION)
            
            logger.info(f"✅ Detected {len(triggers)} evolution triggers")
            return triggers
            
        except Exception as e:
            logger.error(f"❌ Failed to detect evolution triggers: {e}")
            return []
    
    async def analyze_evolution_patterns(self, user_id: str = "mainza-user") -> List[EvolutionPattern]:
        """Analyze memory evolution patterns"""
        try:
            logger.info("📊 Analyzing memory evolution patterns")
            
            # Get evolution events
            evolution_events = await self._get_evolution_events(user_id)
            
            if not evolution_events:
                return []
            
            # Group events by memory
            memory_events = {}
            for event in evolution_events:
                memory_id = event["memory_id"]
                if memory_id not in memory_events:
                    memory_events[memory_id] = []
                memory_events[memory_id].append(event)
            
            # Identify evolution patterns
            patterns = []
            for memory_id, events in memory_events.items():
                if len(events) >= 2:  # Minimum pattern size
                    pattern = await self._create_evolution_pattern(memory_id, events)
                    if pattern:
                        patterns.append(pattern)
            
            # Store patterns
            await self._store_evolution_patterns(patterns, user_id)
            
            logger.info(f"✅ Analyzed {len(patterns)} evolution patterns")
            return patterns
            
        except Exception as e:
            logger.error(f"❌ Failed to analyze evolution patterns: {e}")
            return []
    
    async def evolve_memory_network(self, user_id: str = "mainza-user") -> Dict[str, Any]:
        """Evolve the entire memory network"""
        try:
            logger.info("🌐 Evolving memory network")
            
            # Detect evolution triggers
            triggers = await self.detect_evolution_triggers(user_id)
            
            if not triggers:
                logger.info("No evolution triggers detected")
                return {"evolved_memories": 0, "evolution_events": 0, "triggers": []}
            
            # Evolve memories based on triggers
            evolution_results = []
            for trigger in triggers:
                result = await self._evolve_memories_for_trigger(trigger, user_id)
                evolution_results.append(result)
            
            # Calculate network evolution metrics
            total_evolved = sum(r["evolved_memories"] for r in evolution_results)
            total_events = sum(r["evolution_events"] for r in evolution_results)
            
            # Analyze evolution patterns
            patterns = await self.analyze_evolution_patterns(user_id)
            
            network_evolution = {
                "evolved_memories": total_evolved,
                "evolution_events": total_events,
                "triggers": [t.value for t in triggers],
                "patterns_identified": len(patterns),
                "evolution_velocity": total_events / 7.0,  # Events per day
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"✅ Memory network evolution complete: {total_evolved} memories evolved")
            return network_evolution
            
        except Exception as e:
            logger.error(f"❌ Failed to evolve memory network: {e}")
            return {"evolved_memories": 0, "evolution_events": 0, "triggers": []}
    
    async def _calculate_evolution_changes(
        self,
        memory: Dict[str, Any],
        evolution_type: EvolutionType,
        trigger: EvolutionTrigger,
        evolution_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate evolution changes for a memory"""
        changes = {}
        
        if evolution_type == EvolutionType.IMPORTANCE_EVOLUTION:
            # Evolve importance based on new information
            current_importance = memory.get("importance_score", 0.5)
            new_importance = evolution_data.get("new_importance", current_importance)
            if abs(new_importance - current_importance) > 0.1:
                changes["importance_score"] = new_importance
        
        elif evolution_type == EvolutionType.EMOTIONAL_EVOLUTION:
            # Evolve emotional context
            current_emotional = memory.get("emotional_context", {})
            new_emotional = evolution_data.get("emotional_context", {})
            if new_emotional:
                changes["emotional_context"] = {**current_emotional, **new_emotional}
        
        elif evolution_type == EvolutionType.CONSCIOUSNESS_EVOLUTION:
            # Evolve consciousness context
            current_consciousness = memory.get("consciousness_context", {})
            new_consciousness = evolution_data.get("consciousness_context", {})
            if new_consciousness:
                changes["consciousness_context"] = {**current_consciousness, **new_consciousness}
        
        elif evolution_type == EvolutionType.ASSOCIATION_EVOLUTION:
            # Evolve associations
            current_associations = memory.get("associations", [])
            new_associations = evolution_data.get("new_associations", [])
            if new_associations:
                changes["associations"] = list(set(current_associations + new_associations))
        
        elif evolution_type == EvolutionType.CONCEPTUAL_EVOLUTION:
            # Evolve conceptual understanding
            current_metadata = memory.get("metadata", {})
            new_metadata = evolution_data.get("conceptual_metadata", {})
            if new_metadata:
                changes["metadata"] = {**current_metadata, **new_metadata}
        
        elif evolution_type == EvolutionType.TEMPORAL_EVOLUTION:
            # Evolve temporal context
            current_metadata = memory.get("metadata", {})
            temporal_context = evolution_data.get("temporal_context", {})
            if temporal_context:
                changes["metadata"] = {**current_metadata, "temporal_context": temporal_context}
        
        elif evolution_type == EvolutionType.STRUCTURAL_EVOLUTION:
            # Evolve memory structure
            current_metadata = memory.get("metadata", {})
            structural_changes = evolution_data.get("structural_changes", {})
            if structural_changes:
                changes["metadata"] = {**current_metadata, "structural_evolution": structural_changes}
        
        return changes
    
    async def _apply_evolution_changes(
        self,
        memory_id: str,
        changes: Dict[str, Any],
        user_id: str
    ) -> Optional[Dict[str, Any]]:
        """Apply evolution changes to a memory"""
        try:
            if not changes:
                return None
            
            # Build update query
            set_clauses = []
            params = {"memory_id": memory_id}
            
            for key, value in changes.items():
                if key == "emotional_context" or key == "consciousness_context" or key == "metadata":
                    set_clauses.append(f"m.{key} = ${key}")
                    params[key] = json.dumps(value)
                else:
                    set_clauses.append(f"m.{key} = ${key}")
                    params[key] = value
            
            cypher = f"""
            MATCH (m:AdvancedMemory {{memory_id: $memory_id}})
            SET {', '.join(set_clauses)},
                m.last_accessed = $timestamp
            RETURN m
            """
            
            params["timestamp"] = datetime.now().isoformat()
            
            result = self.neo4j.execute_write_query(cypher, params)
            
            if result:
                # Get updated memory
                updated_memory = await self._get_memory_by_id(memory_id, user_id)
                return updated_memory
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Failed to apply evolution changes: {e}")
            return None
    
    def _calculate_evolution_significance(self, changes: Dict[str, Any]) -> float:
        """Calculate evolution significance based on changes"""
        if not changes:
            return 0.0
        
        significance = 0.0
        
        # Importance changes are highly significant
        if "importance_score" in changes:
            significance += 0.4
        
        # Emotional changes are significant
        if "emotional_context" in changes:
            significance += 0.3
        
        # Consciousness changes are significant
        if "consciousness_context" in changes:
            significance += 0.3
        
        # Association changes are moderately significant
        if "associations" in changes:
            significance += 0.2
        
        # Metadata changes are less significant
        if "metadata" in changes:
            significance += 0.1
        
        return min(1.0, significance)
    
    async def _check_consciousness_growth_trigger(self, user_id: str) -> bool:
        """Check for consciousness growth trigger"""
        try:
            # Query for recent consciousness level increases
            cypher = """
            MATCH (cm:ConsciousnessMetrics)
            WHERE cm.timestamp > datetime() - duration('P1D')
            RETURN cm.overall_level as level
            ORDER BY cm.timestamp DESC
            LIMIT 2
            """
            
            result = self.neo4j.execute_query(cypher)
            
            if len(result) >= 2:
                current_level = result[0]["level"] or 0.0
                previous_level = result[1]["level"] or 0.0
                growth = current_level - previous_level
                return growth > 0.05  # 5% growth threshold
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Failed to check consciousness growth trigger: {e}")
            return False
    
    async def _check_emotional_breakthrough_trigger(self, user_id: str) -> bool:
        """Check for emotional breakthrough trigger"""
        try:
            # Query for recent emotional activities
            cypher = """
            MATCH (aa:AgentActivity)
            WHERE aa.timestamp > datetime() - duration('P1D')
            AND aa.emotional_impact > 0.8
            RETURN count(*) as emotional_activities
            """
            
            result = self.neo4j.execute_query(cypher)
            
            if result:
                emotional_activities = result[0]["emotional_activities"] or 0
                return emotional_activities > 5  # Threshold for emotional breakthrough
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Failed to check emotional breakthrough trigger: {e}")
            return False
    
    async def _check_learning_milestone_trigger(self, user_id: str) -> bool:
        """Check for learning milestone trigger"""
        try:
            # Query for recent learning activities
            cypher = """
            MATCH (aa:AgentActivity)
            WHERE aa.timestamp > datetime() - duration('P1D')
            AND aa.learning_impact > 0.7
            RETURN count(*) as learning_activities
            """
            
            result = self.neo4j.execute_query(cypher)
            
            if result:
                learning_activities = result[0]["learning_activities"] or 0
                return learning_activities > 10  # Threshold for learning milestone
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Failed to check learning milestone trigger: {e}")
            return False
    
    async def _check_memory_conflict_trigger(self, user_id: str) -> bool:
        """Check for memory conflict trigger"""
        try:
            # Query for conflicting memories
            cypher = """
            MATCH (m1:AdvancedMemory)-[:ASSOCIATED_WITH]->(m2:AdvancedMemory)
            WHERE m1.importance_score > 0.7 AND m2.importance_score > 0.7
            AND m1.memory_type = m2.memory_type
            AND m1.created_at > datetime() - duration('P7D')
            RETURN count(*) as conflicting_memories
            """
            
            result = self.neo4j.execute_query(cypher)
            
            if result:
                conflicting_memories = result[0]["conflicting_memories"] or 0
                return conflicting_memories > 3  # Threshold for memory conflicts
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Failed to check memory conflict trigger: {e}")
            return False
    
    async def _check_association_strengthening_trigger(self, user_id: str) -> bool:
        """Check for association strengthening trigger"""
        try:
            # Query for recent association activities
            cypher = """
            MATCH (m1:AdvancedMemory)-[a:ASSOCIATED_WITH]->(m2:AdvancedMemory)
            WHERE a.created_at > datetime() - duration('P1D')
            AND a.association_strength > 0.8
            RETURN count(*) as strong_associations
            """
            
            result = self.neo4j.execute_query(cypher)
            
            if result:
                strong_associations = result[0]["strong_associations"] or 0
                return strong_associations > 5  # Threshold for association strengthening
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Failed to check association strengthening trigger: {e}")
            return False
    
    async def _check_temporal_pattern_trigger(self, user_id: str) -> bool:
        """Check for temporal pattern trigger"""
        try:
            # Query for temporal memory patterns
            cypher = """
            MATCH (m:AdvancedMemory)
            WHERE m.created_at > datetime() - duration('P7D')
            RETURN m.created_at as created_at
            ORDER BY m.created_at
            """
            
            result = self.neo4j.execute_query(cypher)
            
            if len(result) >= 5:
                # Check for temporal clustering
                timestamps = [datetime.fromisoformat(r["created_at"]) for r in result]
                time_diffs = [(timestamps[i+1] - timestamps[i]).total_seconds() for i in range(len(timestamps)-1)]
                avg_diff = sum(time_diffs) / len(time_diffs)
                return avg_diff < 3600  # Less than 1 hour between memories
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Failed to check temporal pattern trigger: {e}")
            return False
    
    async def _check_conceptual_integration_trigger(self, user_id: str) -> bool:
        """Check for conceptual integration trigger"""
        try:
            # Query for conceptual memory clusters
            cypher = """
            MATCH (m:AdvancedMemory)
            WHERE m.memory_type = 'semantic'
            AND m.importance_score > 0.6
            AND m.created_at > datetime() - duration('P3D')
            RETURN count(*) as conceptual_memories
            """
            
            result = self.neo4j.execute_query(cypher)
            
            if result:
                conceptual_memories = result[0]["conceptual_memories"] or 0
                return conceptual_memories > 8  # Threshold for conceptual integration
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Failed to check conceptual integration trigger: {e}")
            return False
    
    async def _check_experiential_accumulation_trigger(self, user_id: str) -> bool:
        """Check for experiential accumulation trigger"""
        try:
            # Query for experiential memories
            cypher = """
            MATCH (m:AdvancedMemory)
            WHERE m.memory_type = 'episodic'
            AND m.created_at > datetime() - duration('P1D')
            RETURN count(*) as episodic_memories
            """
            
            result = self.neo4j.execute_query(cypher)
            
            if result:
                episodic_memories = result[0]["episodic_memories"] or 0
                return episodic_memories > 15  # Threshold for experiential accumulation
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Failed to check experiential accumulation trigger: {e}")
            return False
    
    async def _evolve_memories_for_trigger(
        self,
        trigger: EvolutionTrigger,
        user_id: str
    ) -> Dict[str, Any]:
        """Evolve memories for a specific trigger"""
        try:
            # Get memories relevant to trigger
            memories = await self._get_memories_for_trigger(trigger, user_id)
            
            evolved_memories = 0
            evolution_events = 0
            
            for memory in memories:
                # Determine evolution type based on trigger
                evolution_type = self._determine_evolution_type_for_trigger(trigger)
                
                # Create evolution data
                evolution_data = self._create_evolution_data_for_trigger(trigger, memory)
                
                # Evolve memory
                evolution_event = await self.evolve_memory(
                    memory["memory_id"], evolution_type, trigger, evolution_data, user_id
                )
                
                if evolution_event:
                    evolved_memories += 1
                    evolution_events += 1
            
            return {
                "trigger": trigger.value,
                "evolved_memories": evolved_memories,
                "evolution_events": evolution_events
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to evolve memories for trigger: {e}")
            return {"trigger": trigger.value, "evolved_memories": 0, "evolution_events": 0}
    
    async def _get_memories_for_trigger(
        self,
        trigger: EvolutionTrigger,
        user_id: str
    ) -> List[Dict[str, Any]]:
        """Get memories relevant to a specific trigger"""
        try:
            if trigger == EvolutionTrigger.CONSCIOUSNESS_GROWTH:
                cypher = """
                MATCH (u:User {user_id: $user_id})-[:HAS_MEMORY]->(m:AdvancedMemory)
                WHERE m.consciousness_context.consciousness_level > 0.6
                ORDER BY m.importance_score DESC
                LIMIT 20
                RETURN m
                """
            elif trigger == EvolutionTrigger.EMOTIONAL_BREAKTHROUGH:
                cypher = """
                MATCH (u:User {user_id: $user_id})-[:HAS_MEMORY]->(m:AdvancedMemory)
                WHERE m.memory_type = 'emotional'
                ORDER BY m.importance_score DESC
                LIMIT 20
                RETURN m
                """
            elif trigger == EvolutionTrigger.LEARNING_MILESTONE:
                cypher = """
                MATCH (u:User {user_id: $user_id})-[:HAS_MEMORY]->(m:AdvancedMemory)
                WHERE m.memory_type = 'learning'
                ORDER BY m.importance_score DESC
                LIMIT 20
                RETURN m
                """
            else:
                cypher = """
                MATCH (u:User {user_id: $user_id})-[:HAS_MEMORY]->(m:AdvancedMemory)
                ORDER BY m.importance_score DESC
                LIMIT 20
                RETURN m
                """
            
            result = self.neo4j.execute_query(cypher, {"user_id": user_id})
            
            memories = []
            for record in result:
                memories.append(record["m"])
            
            return memories
            
        except Exception as e:
            logger.error(f"❌ Failed to get memories for trigger: {e}")
            return []
    
    def _determine_evolution_type_for_trigger(self, trigger: EvolutionTrigger) -> EvolutionType:
        """Determine evolution type based on trigger"""
        trigger_mapping = {
            EvolutionTrigger.CONSCIOUSNESS_GROWTH: EvolutionType.CONSCIOUSNESS_EVOLUTION,
            EvolutionTrigger.EMOTIONAL_BREAKTHROUGH: EvolutionType.EMOTIONAL_EVOLUTION,
            EvolutionTrigger.LEARNING_MILESTONE: EvolutionType.CONCEPTUAL_EVOLUTION,
            EvolutionTrigger.MEMORY_CONFLICT: EvolutionType.IMPORTANCE_EVOLUTION,
            EvolutionTrigger.ASSOCIATION_STRENGTHENING: EvolutionType.ASSOCIATION_EVOLUTION,
            EvolutionTrigger.TEMPORAL_PATTERN: EvolutionType.TEMPORAL_EVOLUTION,
            EvolutionTrigger.CONCEPTUAL_INTEGRATION: EvolutionType.CONCEPTUAL_EVOLUTION,
            EvolutionTrigger.EXPERIENTIAL_ACCUMULATION: EvolutionType.STRUCTURAL_EVOLUTION
        }
        
        return trigger_mapping.get(trigger, EvolutionType.IMPORTANCE_EVOLUTION)
    
    def _create_evolution_data_for_trigger(
        self,
        trigger: EvolutionTrigger,
        memory: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create evolution data for a specific trigger"""
        evolution_data = {
            "trigger": trigger.value,
            "memory_id": memory["memory_id"],
            "timestamp": datetime.now().isoformat()
        }
        
        if trigger == EvolutionTrigger.CONSCIOUSNESS_GROWTH:
            evolution_data["consciousness_context"] = {
                "consciousness_level": memory.get("consciousness_context", {}).get("consciousness_level", 0.7) + 0.1
            }
        elif trigger == EvolutionTrigger.EMOTIONAL_BREAKTHROUGH:
            evolution_data["emotional_context"] = {
                "intensity": min(1.0, memory.get("emotional_context", {}).get("intensity", 0.5) + 0.2)
            }
        elif trigger == EvolutionTrigger.LEARNING_MILESTONE:
            evolution_data["conceptual_metadata"] = {
                "learning_milestone": True,
                "milestone_type": "achievement"
            }
        elif trigger == EvolutionTrigger.MEMORY_CONFLICT:
            evolution_data["new_importance"] = memory.get("importance_score", 0.5) * 0.9  # Reduce importance
        elif trigger == EvolutionTrigger.ASSOCIATION_STRENGTHENING:
            evolution_data["new_associations"] = [f"strengthened_{datetime.now().strftime('%Y%m%d_%H%M%S')}"]
        elif trigger == EvolutionTrigger.TEMPORAL_PATTERN:
            evolution_data["temporal_context"] = {
                "pattern_detected": True,
                "pattern_type": "temporal_cluster"
            }
        elif trigger == EvolutionTrigger.CONCEPTUAL_INTEGRATION:
            evolution_data["conceptual_metadata"] = {
                "integration_level": "high",
                "integration_type": "conceptual"
            }
        elif trigger == EvolutionTrigger.EXPERIENTIAL_ACCUMULATION:
            evolution_data["structural_changes"] = {
                "accumulation_detected": True,
                "accumulation_type": "experiential"
            }
        
        return evolution_data
    
    async def _get_memory_by_id(self, memory_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific memory by ID"""
        try:
            cypher = """
            MATCH (u:User {user_id: $user_id})-[:HAS_MEMORY]->(m:AdvancedMemory {memory_id: $memory_id})
            RETURN m
            """
            
            result = self.neo4j.execute_query(cypher, {
                "user_id": user_id,
                "memory_id": memory_id
            })
            
            if result:
                return result[0]["m"]
            return None
            
        except Exception as e:
            logger.error(f"❌ Failed to get memory by ID: {e}")
            return None
    
    async def _get_evolution_events(self, user_id: str) -> List[Dict[str, Any]]:
        """Get evolution events for a user"""
        try:
            cypher = """
            MATCH (u:User {user_id: $user_id})-[:EXPERIENCED_EVOLUTION]->(ee:EvolutionEvent)
            WHERE ee.timestamp > datetime() - duration('P30D')
            RETURN ee
            ORDER BY ee.timestamp DESC
            """
            
            result = self.neo4j.execute_query(cypher, {"user_id": user_id})
            
            events = []
            for record in result:
                events.append(record["ee"])
            
            return events
            
        except Exception as e:
            logger.error(f"❌ Failed to get evolution events: {e}")
            return []
    
    async def _create_evolution_pattern(
        self,
        memory_id: str,
        events: List[Dict[str, Any]]
    ) -> Optional[EvolutionPattern]:
        """Create evolution pattern from events"""
        try:
            if len(events) < 2:
                return None
            
            # Sort events by timestamp
            events.sort(key=lambda x: x["timestamp"])
            
            # Calculate pattern strength
            pattern_strength = sum(float(e.get("significance", 0.0)) for e in events) / len(events)
            
            # Calculate evolution velocity
            time_span = (datetime.fromisoformat(events[-1]["timestamp"]) - 
                        datetime.fromisoformat(events[0]["timestamp"])).days
            evolution_velocity = len(events) / max(1, time_span) if time_span > 0 else len(events)
            
            # Generate insights
            insights = {
                "total_events": len(events),
                "pattern_strength": pattern_strength,
                "evolution_velocity": evolution_velocity,
                "evolution_types": list(set(e.get("evolution_type", "unknown") for e in events)),
                "triggers": list(set(e.get("trigger", "unknown") for e in events))
            }
            
            pattern = EvolutionPattern(
                pattern_id=f"pattern_{memory_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                pattern_type="memory_evolution",
                memory_ids=[memory_id],
                evolution_sequence=events,
                pattern_strength=pattern_strength,
                evolution_velocity=evolution_velocity,
                insights=insights,
                timestamp=datetime.now()
            )
            
            return pattern
            
        except Exception as e:
            logger.error(f"❌ Failed to create evolution pattern: {e}")
            return None
    
    async def _store_evolution_event(self, evolution_event: EvolutionEvent, user_id: str):
        """Store evolution event in Neo4j"""
        try:
            cypher = """
            MERGE (u:User {user_id: $user_id})
            CREATE (ee:EvolutionEvent {
                event_id: $event_id,
                memory_id: $memory_id,
                evolution_type: $evolution_type,
                trigger: $trigger,
                before_state: $before_state,
                after_state: $after_state,
                evolution_data: $evolution_data,
                timestamp: $timestamp,
                significance: $significance
            })
            CREATE (u)-[:EXPERIENCED_EVOLUTION]->(ee)
            
            RETURN ee.event_id AS event_id
            """
            
            result = self.neo4j.execute_write_query(cypher, {
                "user_id": user_id,
                "event_id": evolution_event.event_id,
                "memory_id": evolution_event.memory_id,
                "evolution_type": evolution_event.evolution_type.value,
                "trigger": evolution_event.trigger.value,
                "before_state": json.dumps(evolution_event.before_state),
                "after_state": json.dumps(evolution_event.after_state),
                "evolution_data": json.dumps(evolution_event.evolution_data),
                "timestamp": evolution_event.timestamp.isoformat(),
                "significance": evolution_event.significance
            })
            
            logger.debug(f"✅ Stored evolution event: {result}")
            
        except Exception as e:
            logger.error(f"❌ Failed to store evolution event: {e}")
    
    async def _store_evolution_patterns(self, patterns: List[EvolutionPattern], user_id: str):
        """Store evolution patterns in Neo4j"""
        try:
            for pattern in patterns:
                cypher = """
                MERGE (u:User {user_id: $user_id})
                CREATE (ep:EvolutionPattern {
                    pattern_id: $pattern_id,
                    pattern_type: $pattern_type,
                    memory_ids: $memory_ids,
                    pattern_strength: $pattern_strength,
                    evolution_velocity: $evolution_velocity,
                    insights: $insights,
                    timestamp: $timestamp
                })
                CREATE (u)-[:HAS_EVOLUTION_PATTERN]->(ep)
                
                RETURN ep.pattern_id AS pattern_id
                """
                
                result = self.neo4j.execute_write_query(cypher, {
                    "user_id": user_id,
                    "pattern_id": pattern.pattern_id,
                    "pattern_type": pattern.pattern_type,
                    "memory_ids": pattern.memory_ids,
                    "pattern_strength": pattern.pattern_strength,
                    "evolution_velocity": pattern.evolution_velocity,
                    "insights": json.dumps(pattern.insights),
                    "timestamp": pattern.timestamp.isoformat()
                })
                
                logger.debug(f"✅ Stored evolution pattern: {result}")
            
        except Exception as e:
            logger.error(f"❌ Failed to store evolution patterns: {e}")

# Global instance
memory_evolution_system = MemoryEvolutionSystem()
