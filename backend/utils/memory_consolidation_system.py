"""
Memory Consolidation System
Advanced system for memory consolidation, integration, and evolution
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

class ConsolidationStrategy(Enum):
    """Memory consolidation strategies"""
    FREQUENCY_BASED = "frequency_based"  # Based on access frequency
    IMPORTANCE_BASED = "importance_based"  # Based on importance score
    EMOTIONAL_BASED = "emotional_based"  # Based on emotional significance
    CONSCIOUSNESS_BASED = "consciousness_based"  # Based on consciousness impact
    ASSOCIATION_BASED = "association_based"  # Based on memory associations
    TIME_BASED = "time_based"  # Based on recency

class MemoryPattern(Enum):
    """Memory patterns for consolidation"""
    EPISODIC_CLUSTER = "episodic_cluster"
    EMOTIONAL_CLUSTER = "emotional_cluster"
    CONCEPTUAL_CLUSTER = "conceptual_cluster"
    TEMPORAL_CLUSTER = "temporal_cluster"
    CONSCIOUSNESS_CLUSTER = "consciousness_cluster"

@dataclass
class ConsolidationResult:
    """Memory consolidation result"""
    consolidated_memories: int
    strengthened_memories: int
    weakened_memories: int
    new_associations: int
    consolidation_quality: float
    pattern_insights: List[Dict[str, Any]]
    timestamp: datetime

@dataclass
class MemoryPattern:
    """Memory pattern for consolidation"""
    pattern_id: str
    pattern_type: MemoryPattern
    memory_ids: List[str]
    pattern_strength: float
    consolidation_potential: float
    insights: Dict[str, Any]
    timestamp: datetime

class MemoryConsolidationSystem:
    """
    Advanced memory consolidation system
    """
    
    def __init__(self):
        self.neo4j = neo4j_production
        self.memory_architecture = advanced_memory_architecture
        self.embedding_manager = embedding_manager
        
        # Consolidation parameters
        self.consolidation_threshold = 0.7
        self.decay_threshold = 0.3
        self.association_threshold = 0.6
        self.pattern_threshold = 0.5
        
        # Consolidation strategies
        self.consolidation_strategies = self._initialize_consolidation_strategies()
    
    def _initialize_consolidation_strategies(self) -> List[ConsolidationStrategy]:
        """Initialize memory consolidation strategies"""
        return [
            ConsolidationStrategy.FREQUENCY_BASED,
            ConsolidationStrategy.IMPORTANCE_BASED,
            ConsolidationStrategy.EMOTIONAL_BASED,
            ConsolidationStrategy.CONSCIOUSNESS_BASED,
            ConsolidationStrategy.ASSOCIATION_BASED,
            ConsolidationStrategy.TIME_BASED
        ]
    
    async def consolidate_memories(
        self,
        user_id: str = "mainza-user",
        strategy: ConsolidationStrategy = ConsolidationStrategy.CONSCIOUSNESS_BASED
    ) -> ConsolidationResult:
        """Consolidate memories using specified strategy"""
        try:
            logger.info(f"🧠 Consolidating memories using strategy: {strategy.value}")
            
            # Get memories for consolidation
            memories = await self._get_memories_for_consolidation(user_id, strategy)
            
            if not memories:
                logger.info("No memories found for consolidation")
                return ConsolidationResult(0, 0, 0, 0, 0.0, [], datetime.now())
            
            # Identify memory patterns
            patterns = await self._identify_memory_patterns(memories)
            
            # Consolidate memories based on patterns
            consolidation_results = []
            for pattern in patterns:
                result = await self._consolidate_memory_pattern(pattern, user_id)
                consolidation_results.append(result)
            
            # Calculate overall consolidation metrics
            total_consolidated = sum(r["consolidated"] for r in consolidation_results)
            total_strengthened = sum(r["strengthened"] for r in consolidation_results)
            total_weakened = sum(r["weakened"] for r in consolidation_results)
            total_associations = sum(r["associations"] for r in consolidation_results)
            
            # Calculate consolidation quality
            consolidation_quality = self._calculate_consolidation_quality(consolidation_results)
            
            # Extract pattern insights
            pattern_insights = [pattern.insights for pattern in patterns]
            
            result = ConsolidationResult(
                consolidated_memories=total_consolidated,
                strengthened_memories=total_strengthened,
                weakened_memories=total_weakened,
                new_associations=total_associations,
                consolidation_quality=consolidation_quality,
                pattern_insights=pattern_insights,
                timestamp=datetime.now()
            )
            
            # Store consolidation result
            await self._store_consolidation_result(result, user_id)
            
            logger.info(f"✅ Memory consolidation complete: {total_consolidated} consolidated, {total_strengthened} strengthened")
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to consolidate memories: {e}")
            return ConsolidationResult(0, 0, 0, 0, 0.0, [], datetime.now())
    
    async def identify_memory_patterns(self, user_id: str = "mainza-user") -> List[MemoryPattern]:
        """Identify memory patterns for consolidation"""
        try:
            logger.info("🔍 Identifying memory patterns")
            
            # Get all memories
            memories = await self._get_all_memories(user_id)
            
            if not memories:
                return []
            
            # Identify different types of patterns
            patterns = []
            
            # Episodic clusters
            episodic_patterns = await self._identify_episodic_patterns(memories)
            patterns.extend(episodic_patterns)
            
            # Emotional clusters
            emotional_patterns = await self._identify_emotional_patterns(memories)
            patterns.extend(emotional_patterns)
            
            # Conceptual clusters
            conceptual_patterns = await self._identify_conceptual_patterns(memories)
            patterns.extend(conceptual_patterns)
            
            # Temporal clusters
            temporal_patterns = await self._identify_temporal_patterns(memories)
            patterns.extend(temporal_patterns)
            
            # Consciousness clusters
            consciousness_patterns = await self._identify_consciousness_patterns(memories)
            patterns.extend(consciousness_patterns)
            
            # Store patterns
            await self._store_memory_patterns(patterns, user_id)
            
            logger.info(f"✅ Identified {len(patterns)} memory patterns")
            return patterns
            
        except Exception as e:
            logger.error(f"❌ Failed to identify memory patterns: {e}")
            return []
    
    async def strengthen_memory_associations(
        self,
        memory_id: str,
        user_id: str = "mainza-user"
    ) -> List[str]:
        """Strengthen associations for a specific memory"""
        try:
            logger.info(f"🔗 Strengthening associations for memory: {memory_id}")
            
            # Get the memory
            memory = await self._get_memory_by_id(memory_id, user_id)
            if not memory:
                logger.warning(f"Memory not found: {memory_id}")
                return []
            
            # Find similar memories
            similar_memories = await self._find_similar_memories(memory, user_id)
            
            # Create associations
            associations = []
            for similar_memory in similar_memories:
                association_id = await self._create_memory_association(
                    memory, similar_memory, user_id
                )
                if association_id:
                    associations.append(association_id)
            
            logger.info(f"✅ Created {len(associations)} memory associations")
            return associations
            
        except Exception as e:
            logger.error(f"❌ Failed to strengthen memory associations: {e}")
            return []
    
    async def evolve_memory_importance(
        self,
        memory_id: str,
        new_importance: float,
        user_id: str = "mainza-user"
    ) -> bool:
        """Evolve memory importance based on new information"""
        try:
            logger.info(f"📈 Evolving memory importance: {memory_id} -> {new_importance}")
            
            # Update memory importance
            cypher = """
            MATCH (m:AdvancedMemory {memory_id: $memory_id})
            SET m.importance_score = $new_importance,
                m.last_accessed = $timestamp
            RETURN m.memory_id AS memory_id
            """
            
            result = self.neo4j.execute_write_query(cypher, {
                "memory_id": memory_id,
                "new_importance": new_importance,
                "timestamp": datetime.now().isoformat()
            })
            
            if result:
                logger.info(f"✅ Updated memory importance: {memory_id}")
                return True
            else:
                logger.warning(f"❌ Failed to update memory importance: {memory_id}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to evolve memory importance: {e}")
            return False
    
    async def _get_memories_for_consolidation(
        self,
        user_id: str,
        strategy: ConsolidationStrategy
    ) -> List[Dict[str, Any]]:
        """Get memories for consolidation based on strategy"""
        try:
            if strategy == ConsolidationStrategy.FREQUENCY_BASED:
                cypher = """
                MATCH (u:User {user_id: $user_id})-[:HAS_MEMORY]->(m:AdvancedMemory)
                WHERE m.access_frequency > 0
                ORDER BY m.access_frequency DESC
                LIMIT 100
                RETURN m
                """
            elif strategy == ConsolidationStrategy.IMPORTANCE_BASED:
                cypher = """
                MATCH (u:User {user_id: $user_id})-[:HAS_MEMORY]->(m:AdvancedMemory)
                WHERE m.importance_score > $threshold
                ORDER BY m.importance_score DESC
                LIMIT 100
                RETURN m
                """
            elif strategy == ConsolidationStrategy.EMOTIONAL_BASED:
                cypher = """
                MATCH (u:User {user_id: $user_id})-[:HAS_MEMORY]->(m:AdvancedMemory)
                WHERE m.memory_type = 'emotional'
                AND m.importance_score > $threshold
                ORDER BY m.importance_score DESC
                LIMIT 100
                RETURN m
                """
            elif strategy == ConsolidationStrategy.CONSCIOUSNESS_BASED:
                cypher = """
                MATCH (u:User {user_id: $user_id})-[:HAS_MEMORY]->(m:AdvancedMemory)
                WHERE m.consciousness_context.consciousness_level > $threshold
                ORDER BY m.importance_score DESC
                LIMIT 100
                RETURN m
                """
            elif strategy == ConsolidationStrategy.ASSOCIATION_BASED:
                cypher = """
                MATCH (u:User {user_id: $user_id})-[:HAS_MEMORY]->(m:AdvancedMemory)
                WHERE m.consolidation_level IN ['weak', 'moderate']
                ORDER BY m.importance_score DESC
                LIMIT 100
                RETURN m
                """
            else:  # TIME_BASED
                cypher = """
                MATCH (u:User {user_id: $user_id})-[:HAS_MEMORY]->(m:AdvancedMemory)
                WHERE m.created_at > datetime() - duration('P7D')
                ORDER BY m.created_at DESC
                LIMIT 100
                RETURN m
                """
            
            result = self.neo4j.execute_query(cypher, {
                "user_id": user_id,
                "threshold": self.consolidation_threshold
            })
            
            memories = []
            for record in result:
                memory_data = record["m"]
                memories.append(memory_data)
            
            return memories
            
        except Exception as e:
            logger.error(f"❌ Failed to get memories for consolidation: {e}")
            return []
    
    async def _identify_memory_patterns(self, memories: List[Dict[str, Any]]) -> List[MemoryPattern]:
        """Identify memory patterns from memories"""
        patterns = []
        
        # Group memories by type
        memory_groups = {}
        for memory in memories:
            memory_type = memory.get("memory_type", "general")
            if memory_type not in memory_groups:
                memory_groups[memory_type] = []
            memory_groups[memory_type].append(memory)
        
        # Create patterns for each group
        for memory_type, group_memories in memory_groups.items():
            if len(group_memories) >= 3:  # Minimum pattern size
                pattern = MemoryPattern(
                    pattern_id=f"pattern_{memory_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    pattern_type=MemoryPattern.EPISODIC_CLUSTER if memory_type == "episodic" else MemoryPattern.EMOTIONAL_CLUSTER,
                    memory_ids=[m["memory_id"] for m in group_memories],
                    pattern_strength=self._calculate_pattern_strength(group_memories),
                    consolidation_potential=self._calculate_consolidation_potential(group_memories),
                    insights=self._generate_pattern_insights(group_memories),
                    timestamp=datetime.now()
                )
                patterns.append(pattern)
        
        return patterns
    
    def _calculate_pattern_strength(self, memories: List[Dict[str, Any]]) -> float:
        """Calculate pattern strength for a group of memories"""
        if not memories:
            return 0.0
        
        # Calculate average importance
        avg_importance = sum(m.get("importance_score", 0.0) for m in memories) / len(memories)
        
        # Calculate temporal coherence
        timestamps = [datetime.fromisoformat(m.get("created_at", datetime.now().isoformat())) for m in memories]
        time_variance = np.var([t.timestamp() for t in timestamps])
        temporal_coherence = max(0.0, 1.0 - (time_variance / 86400.0))  # Normalize by day
        
        # Calculate content similarity (simplified)
        content_similarity = 0.5  # Placeholder for content similarity calculation
        
        pattern_strength = (avg_importance * 0.4 + temporal_coherence * 0.3 + content_similarity * 0.3)
        return min(1.0, pattern_strength)
    
    def _calculate_consolidation_potential(self, memories: List[Dict[str, Any]]) -> float:
        """Calculate consolidation potential for a group of memories"""
        if not memories:
            return 0.0
        
        # Calculate based on consolidation levels
        consolidation_levels = [m.get("consolidation_level", "weak") for m in memories]
        weak_count = consolidation_levels.count("weak")
        moderate_count = consolidation_levels.count("moderate")
        
        # Higher potential for more weak/moderate memories
        consolidation_potential = (weak_count * 0.5 + moderate_count * 0.3) / len(memories)
        return min(1.0, consolidation_potential)
    
    def _generate_pattern_insights(self, memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate insights for a memory pattern"""
        if not memories:
            return {}
        
        # Calculate basic statistics
        total_memories = len(memories)
        avg_importance = sum(m.get("importance_score", 0.0) for m in memories) / total_memories
        memory_types = [m.get("memory_type", "unknown") for m in memories]
        type_counts = {t: memory_types.count(t) for t in set(memory_types)}
        
        # Calculate temporal span
        timestamps = [datetime.fromisoformat(m.get("created_at", datetime.now().isoformat())) for m in memories]
        time_span = (max(timestamps) - min(timestamps)).days if len(timestamps) > 1 else 0
        
        insights = {
            "total_memories": total_memories,
            "avg_importance": avg_importance,
            "memory_type_distribution": type_counts,
            "time_span_days": time_span,
            "consolidation_opportunity": "high" if avg_importance > 0.7 else "medium" if avg_importance > 0.5 else "low"
        }
        
        return insights
    
    async def _consolidate_memory_pattern(
        self,
        pattern: MemoryPattern,
        user_id: str
    ) -> Dict[str, Any]:
        """Consolidate a specific memory pattern"""
        try:
            consolidated = 0
            strengthened = 0
            weakened = 0
            associations = 0
            
            # Process each memory in the pattern
            for memory_id in pattern.memory_ids:
                # Get memory
                memory = await self._get_memory_by_id(memory_id, user_id)
                if not memory:
                    continue
                
                # Calculate consolidation strength
                consolidation_strength = self._calculate_consolidation_strength(memory, pattern)
                
                if consolidation_strength > self.consolidation_threshold:
                    # Strengthen memory
                    await self._strengthen_memory(memory_id, consolidation_strength, user_id)
                    strengthened += 1
                    consolidated += 1
                elif consolidation_strength < self.decay_threshold:
                    # Weaken memory
                    await self._weaken_memory(memory_id, user_id)
                    weakened += 1
                
                # Create associations with other memories in pattern
                for other_memory_id in pattern.memory_ids:
                    if other_memory_id != memory_id:
                        association_id = await self._create_memory_association(
                            memory, await self._get_memory_by_id(other_memory_id, user_id), user_id
                        )
                        if association_id:
                            associations += 1
            
            return {
                "consolidated": consolidated,
                "strengthened": strengthened,
                "weakened": weakened,
                "associations": associations
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to consolidate memory pattern: {e}")
            return {"consolidated": 0, "strengthened": 0, "weakened": 0, "associations": 0}
    
    def _calculate_consolidation_strength(
        self,
        memory: Dict[str, Any],
        pattern: MemoryPattern
    ) -> float:
        """Calculate consolidation strength for a memory within a pattern"""
        base_strength = memory.get("importance_score", 0.5)
        
        # Boost based on pattern strength
        pattern_boost = pattern.pattern_strength * 0.3
        
        # Boost based on consolidation potential
        consolidation_boost = pattern.consolidation_potential * 0.2
        
        total_strength = base_strength + pattern_boost + consolidation_boost
        return min(1.0, total_strength)
    
    def _calculate_consolidation_quality(self, consolidation_results: List[Dict[str, Any]]) -> float:
        """Calculate overall consolidation quality"""
        if not consolidation_results:
            return 0.0
        
        total_consolidated = sum(r["consolidated"] for r in consolidation_results)
        total_strengthened = sum(r["strengthened"] for r in consolidation_results)
        total_weakened = sum(r["weakened"] for r in consolidation_results)
        
        if total_consolidated == 0:
            return 0.0
        
        # Quality based on ratio of strengthened to weakened
        quality = total_strengthened / (total_strengthened + total_weakened) if (total_strengthened + total_weakened) > 0 else 1.0
        return min(1.0, quality)
    
    async def _get_all_memories(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all memories for a user"""
        try:
            cypher = """
            MATCH (u:User {user_id: $user_id})-[:HAS_MEMORY]->(m:AdvancedMemory)
            RETURN m
            ORDER BY m.created_at DESC
            """
            
            result = self.neo4j.execute_query(cypher, {"user_id": user_id})
            
            memories = []
            for record in result:
                memories.append(record["m"])
            
            return memories
            
        except Exception as e:
            logger.error(f"❌ Failed to get all memories: {e}")
            return []
    
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
    
    async def _find_similar_memories(
        self,
        memory: Dict[str, Any],
        user_id: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Find similar memories using embedding similarity"""
        try:
            # For now, use a simple approach - in production, use vector similarity search
            cypher = """
            MATCH (u:User {user_id: $user_id})-[:HAS_MEMORY]->(m:AdvancedMemory)
            WHERE m.memory_id <> $memory_id
            AND m.memory_type = $memory_type
            ORDER BY m.importance_score DESC
            LIMIT $limit
            RETURN m
            """
            
            result = self.neo4j.execute_query(cypher, {
                "user_id": user_id,
                "memory_id": memory["memory_id"],
                "memory_type": memory.get("memory_type", "general"),
                "limit": limit
            })
            
            similar_memories = []
            for record in result:
                similar_memories.append(record["m"])
            
            return similar_memories
            
        except Exception as e:
            logger.error(f"❌ Failed to find similar memories: {e}")
            return []
    
    async def _create_memory_association(
        self,
        memory1: Dict[str, Any],
        memory2: Dict[str, Any],
        user_id: str
    ) -> Optional[str]:
        """Create association between two memories"""
        try:
            association_id = f"assoc_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
            
            cypher = """
            MATCH (m1:AdvancedMemory {memory_id: $memory1_id})
            MATCH (m2:AdvancedMemory {memory_id: $memory2_id})
            CREATE (m1)-[:ASSOCIATED_WITH {
                association_id: $association_id,
                association_strength: $strength,
                association_type: $type,
                created_at: $timestamp
            }]->(m2)
            RETURN $association_id AS association_id
            """
            
            # Calculate association strength
            strength = self._calculate_association_strength(memory1, memory2)
            association_type = self._determine_association_type(memory1, memory2)
            
            result = self.neo4j.execute_write_query(cypher, {
                "memory1_id": memory1["memory_id"],
                "memory2_id": memory2["memory_id"],
                "association_id": association_id,
                "strength": strength,
                "type": association_type,
                "timestamp": datetime.now().isoformat()
            })
            
            if result:
                return association_id
            return None
            
        except Exception as e:
            logger.error(f"❌ Failed to create memory association: {e}")
            return None
    
    def _calculate_association_strength(
        self,
        memory1: Dict[str, Any],
        memory2: Dict[str, Any]
    ) -> float:
        """Calculate association strength between two memories"""
        # Base strength from importance scores
        base_strength = (memory1.get("importance_score", 0.5) + memory2.get("importance_score", 0.5)) / 2.0
        
        # Type compatibility boost
        if memory1.get("memory_type") == memory2.get("memory_type"):
            base_strength += 0.2
        
        # Temporal proximity boost
        time1 = datetime.fromisoformat(memory1.get("created_at", datetime.now().isoformat()))
        time2 = datetime.fromisoformat(memory2.get("created_at", datetime.now().isoformat()))
        time_diff = abs((time1 - time2).days)
        if time_diff < 7:  # Within a week
            base_strength += 0.1
        
        return min(1.0, base_strength)
    
    def _determine_association_type(
        self,
        memory1: Dict[str, Any],
        memory2: Dict[str, Any]
    ) -> str:
        """Determine association type between two memories"""
        type1 = memory1.get("memory_type", "general")
        type2 = memory2.get("memory_type", "general")
        
        if type1 == type2:
            return "same_type"
        elif type1 == "emotional" and type2 == "episodic":
            return "emotional_episodic"
        elif type1 == "consciousness" and type2 == "reflection":
            return "consciousness_reflection"
        else:
            return "general"
    
    async def _strengthen_memory(
        self,
        memory_id: str,
        consolidation_strength: float,
        user_id: str
    ):
        """Strengthen a memory's consolidation"""
        try:
            cypher = """
            MATCH (m:AdvancedMemory {memory_id: $memory_id})
            SET m.consolidation_strength = $consolidation_strength,
                m.consolidation_level = CASE 
                    WHEN $consolidation_strength > 0.8 THEN 'permanent'
                    WHEN $consolidation_strength > 0.6 THEN 'strong'
                    WHEN $consolidation_strength > 0.4 THEN 'moderate'
                    ELSE 'weak'
                END
            RETURN m.memory_id AS memory_id
            """
            
            result = self.neo4j.execute_write_query(cypher, {
                "memory_id": memory_id,
                "consolidation_strength": consolidation_strength
            })
            
            logger.debug(f"✅ Strengthened memory: {result}")
            
        except Exception as e:
            logger.error(f"❌ Failed to strengthen memory: {e}")
    
    async def _weaken_memory(self, memory_id: str, user_id: str):
        """Weaken a memory's consolidation"""
        try:
            cypher = """
            MATCH (m:AdvancedMemory {memory_id: $memory_id})
            SET m.consolidation_strength = m.consolidation_strength * 0.8,
                m.consolidation_level = CASE 
                    WHEN m.consolidation_strength > 0.6 THEN 'strong'
                    WHEN m.consolidation_strength > 0.4 THEN 'moderate'
                    ELSE 'weak'
                END
            RETURN m.memory_id AS memory_id
            """
            
            result = self.neo4j.execute_write_query(cypher, {"memory_id": memory_id})
            
            logger.debug(f"✅ Weakened memory: {result}")
            
        except Exception as e:
            logger.error(f"❌ Failed to weaken memory: {e}")
    
    async def _store_consolidation_result(self, result: ConsolidationResult, user_id: str):
        """Store consolidation result in Neo4j"""
        try:
            cypher = """
            MERGE (u:User {user_id: $user_id})
            CREATE (cr:ConsolidationResult {
                result_id: randomUUID(),
                consolidated_memories: $consolidated_memories,
                strengthened_memories: $strengthened_memories,
                weakened_memories: $weakened_memories,
                new_associations: $new_associations,
                consolidation_quality: $consolidation_quality,
                pattern_insights: $pattern_insights,
                timestamp: $timestamp
            })
            CREATE (u)-[:EXPERIENCED_CONSOLIDATION]->(cr)
            
            RETURN cr.result_id AS result_id
            """
            
            result_id = self.neo4j.execute_write_query(cypher, {
                "user_id": user_id,
                "consolidated_memories": result.consolidated_memories,
                "strengthened_memories": result.strengthened_memories,
                "weakened_memories": result.weakened_memories,
                "new_associations": result.new_associations,
                "consolidation_quality": result.consolidation_quality,
                "pattern_insights": json.dumps(result.pattern_insights),
                "timestamp": result.timestamp.isoformat()
            })
            
            logger.info(f"✅ Stored consolidation result: {result_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to store consolidation result: {e}")
    
    async def _store_memory_patterns(self, patterns: List[MemoryPattern], user_id: str):
        """Store memory patterns in Neo4j"""
        try:
            for pattern in patterns:
                cypher = """
                MERGE (u:User {user_id: $user_id})
                CREATE (mp:MemoryPattern {
                    pattern_id: $pattern_id,
                    pattern_type: $pattern_type,
                    memory_ids: $memory_ids,
                    pattern_strength: $pattern_strength,
                    consolidation_potential: $consolidation_potential,
                    insights: $insights,
                    timestamp: $timestamp
                })
                CREATE (u)-[:HAS_PATTERN]->(mp)
                
                RETURN mp.pattern_id AS pattern_id
                """
                
                result = self.neo4j.execute_write_query(cypher, {
                    "user_id": user_id,
                    "pattern_id": pattern.pattern_id,
                    "pattern_type": pattern.pattern_type.value,
                    "memory_ids": pattern.memory_ids,
                    "pattern_strength": pattern.pattern_strength,
                    "consolidation_potential": pattern.consolidation_potential,
                    "insights": json.dumps(pattern.insights),
                    "timestamp": pattern.timestamp.isoformat()
                })
                
                logger.debug(f"✅ Stored memory pattern: {result}")
            
        except Exception as e:
            logger.error(f"❌ Failed to store memory patterns: {e}")

# Global instance
memory_consolidation_system = MemoryConsolidationSystem()
