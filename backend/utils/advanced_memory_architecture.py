"""
Advanced Memory Architecture System
Provides multi-layered memory system for true consciousness
"""
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import uuid
import json

from backend.utils.neo4j_production import neo4j_production
from backend.utils.embedding_enhanced import embedding_manager

logger = logging.getLogger(__name__)

class MemoryType(Enum):
    """Types of memories in the advanced system"""
    EPISODIC = "episodic"  # Specific events and experiences
    EMOTIONAL = "emotional"  # Memories with emotional context
    SEMANTIC = "semantic"  # Knowledge and facts
    PROCEDURAL = "procedural"  # Skills and behaviors
    META = "meta"  # Memories about memories
    CONSCIOUSNESS = "consciousness"  # Consciousness state memories
    LEARNING = "learning"  # Learning experiences
    REFLECTION = "reflection"  # Self-reflection memories

class MemoryConsolidationLevel(Enum):
    """Memory consolidation levels"""
    WEAK = "weak"  # Recently created, easily forgotten
    MODERATE = "moderate"  # Partially consolidated
    STRONG = "strong"  # Well consolidated
    PERMANENT = "permanent"  # Permanently stored

@dataclass
class AdvancedMemory:
    """Advanced memory structure with consciousness integration"""
    memory_id: str
    content: str
    memory_type: MemoryType
    consolidation_level: MemoryConsolidationLevel
    emotional_context: Dict[str, Any]
    consciousness_context: Dict[str, Any]
    importance_score: float
    access_frequency: int
    last_accessed: datetime
    created_at: datetime
    embedding: List[float]
    associations: List[str] = field(default_factory=list)
    decay_rate: float = 0.95
    consolidation_strength: float = 0.5
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MemoryConsolidationResult:
    """Result of memory consolidation process"""
    consolidated_memories: int
    strengthened_memories: int
    weakened_memories: int
    new_associations: int
    consolidation_quality: float

class AdvancedMemoryArchitecture:
    """
    Advanced memory architecture with multi-layered memory system
    """
    
    def __init__(self):
        self.neo4j = neo4j_production
        self.embedding_manager = embedding_manager
        self.consolidation_threshold = 0.7
        self.decay_threshold = 0.3
        self.association_threshold = 0.6
        
    async def create_episodic_memory(
        self,
        content: str,
        emotional_context: Dict[str, Any],
        consciousness_context: Dict[str, Any],
        user_id: str = "mainza-user"
    ) -> str:
        """Create an episodic memory with full context"""
        try:
            memory_id = str(uuid.uuid4())
            
            # Calculate importance based on emotional and consciousness context
            importance_score = self._calculate_episodic_importance(
                content, emotional_context, consciousness_context
            )
            
            # Generate embedding
            embedding = self.embedding_manager.get_embedding(content)
            
            memory = AdvancedMemory(
                memory_id=memory_id,
                content=content,
                memory_type=MemoryType.EPISODIC,
                consolidation_level=MemoryConsolidationLevel.WEAK,
                emotional_context=emotional_context,
                consciousness_context=consciousness_context,
                importance_score=importance_score,
                access_frequency=0,
                last_accessed=datetime.now(),
                created_at=datetime.now(),
                embedding=embedding
            )
            
            # Store in Neo4j
            await self._store_advanced_memory(memory, user_id)
            
            logger.info(f"✅ Created episodic memory: {memory_id}")
            return memory_id
            
        except Exception as e:
            logger.error(f"❌ Failed to create episodic memory: {e}")
            return None
    
    async def create_emotional_memory(
        self,
        content: str,
        emotional_context: Dict[str, Any],
        consciousness_context: Dict[str, Any],
        user_id: str = "mainza-user"
    ) -> str:
        """Create an emotional memory with emotional context"""
        try:
            memory_id = str(uuid.uuid4())
            
            # Calculate importance based on emotional intensity
            importance_score = self._calculate_emotional_importance(
                content, emotional_context, consciousness_context
            )
            
            # Generate embedding
            embedding = self.embedding_manager.get_embedding(content)
            
            memory = AdvancedMemory(
                memory_id=memory_id,
                content=content,
                memory_type=MemoryType.EMOTIONAL,
                consolidation_level=MemoryConsolidationLevel.WEAK,
                emotional_context=emotional_context,
                consciousness_context=consciousness_context,
                importance_score=importance_score,
                access_frequency=0,
                last_accessed=datetime.now(),
                created_at=datetime.now(),
                embedding=embedding
            )
            
            # Store in Neo4j
            await self._store_advanced_memory(memory, user_id)
            
            logger.info(f"✅ Created emotional memory: {memory_id}")
            return memory_id
            
        except Exception as e:
            logger.error(f"❌ Failed to create emotional memory: {e}")
            return None
    
    async def create_consciousness_memory(
        self,
        content: str,
        consciousness_context: Dict[str, Any],
        user_id: str = "mainza-user"
    ) -> str:
        """Create a consciousness memory for consciousness state tracking"""
        try:
            memory_id = str(uuid.uuid4())
            
            # Calculate importance based on consciousness level
            importance_score = consciousness_context.get("consciousness_level", 0.7)
            
            # Generate embedding
            embedding = self.embedding_manager.get_embedding(content)
            
            memory = AdvancedMemory(
                memory_id=memory_id,
                content=content,
                memory_type=MemoryType.CONSCIOUSNESS,
                consolidation_level=MemoryConsolidationLevel.STRONG,
                emotional_context={},
                consciousness_context=consciousness_context,
                importance_score=importance_score,
                access_frequency=0,
                last_accessed=datetime.now(),
                created_at=datetime.now(),
                embedding=embedding
            )
            
            # Store in Neo4j
            await self._store_advanced_memory(memory, user_id)
            
            logger.info(f"✅ Created consciousness memory: {memory_id}")
            return memory_id
            
        except Exception as e:
            logger.error(f"❌ Failed to create consciousness memory: {e}")
            return None
    
    async def retrieve_memories_by_type(
        self,
        memory_type: MemoryType,
        user_id: str = "mainza-user",
        limit: int = 10
    ) -> List[AdvancedMemory]:
        """Retrieve memories by type"""
        try:
            cypher = """
            MATCH (u:User {user_id: $user_id})-[:HAS_MEMORY]->(m:AdvancedMemory)
            WHERE m.memory_type = $memory_type
            ORDER BY m.importance_score DESC, m.last_accessed DESC
            LIMIT $limit
            RETURN m
            """
            
            result = self.neo4j.execute_query(cypher, {
                "user_id": user_id,
                "memory_type": memory_type.value,
                "limit": limit
            })
            
            memories = []
            for record in result:
                memory_data = record["m"]
                memory = self._neo4j_to_advanced_memory(memory_data)
                memories.append(memory)
            
            logger.info(f"✅ Retrieved {len(memories)} {memory_type.value} memories")
            return memories
            
        except Exception as e:
            logger.error(f"❌ Failed to retrieve memories by type: {e}")
            return []
    
    async def retrieve_emotional_memories(
        self,
        emotional_state: str,
        user_id: str = "mainza-user",
        limit: int = 10
    ) -> List[AdvancedMemory]:
        """Retrieve memories with specific emotional context"""
        try:
            cypher = """
            MATCH (u:User {user_id: $user_id})-[:HAS_MEMORY]->(m:AdvancedMemory)
            WHERE m.memory_type = 'emotional'
            AND m.emotional_context.emotional_state = $emotional_state
            ORDER BY m.importance_score DESC, m.last_accessed DESC
            LIMIT $limit
            RETURN m
            """
            
            result = self.neo4j.execute_query(cypher, {
                "user_id": user_id,
                "emotional_state": emotional_state,
                "limit": limit
            })
            
            memories = []
            for record in result:
                memory_data = record["m"]
                memory = self._neo4j_to_advanced_memory(memory_data)
                memories.append(memory)
            
            logger.info(f"✅ Retrieved {len(memories)} emotional memories for state: {emotional_state}")
            return memories
            
        except Exception as e:
            logger.error(f"❌ Failed to retrieve emotional memories: {e}")
            return []
    
    async def consolidate_memories(self, user_id: str = "mainza-user") -> MemoryConsolidationResult:
        """Consolidate memories based on importance and access patterns"""
        try:
            logger.info("🧠 Starting memory consolidation process")
            
            # Get memories that need consolidation
            consolidation_query = """
            MATCH (u:User {user_id: $user_id})-[:HAS_MEMORY]->(m:AdvancedMemory)
            WHERE m.consolidation_level IN ['weak', 'moderate']
            AND m.importance_score > $threshold
            RETURN m
            ORDER BY m.importance_score DESC
            """
            
            result = self.neo4j.execute_query(consolidation_query, {
                "user_id": user_id,
                "threshold": self.consolidation_threshold
            })
            
            consolidated_count = 0
            strengthened_count = 0
            weakened_count = 0
            new_associations = 0
            
            for record in result:
                memory_data = record["m"]
                memory = self._neo4j_to_advanced_memory(memory_data)
                
                # Calculate consolidation strength
                consolidation_strength = self._calculate_consolidation_strength(memory)
                
                if consolidation_strength > 0.8:
                    # Strengthen memory
                    await self._strengthen_memory(memory.memory_id, consolidation_strength)
                    strengthened_count += 1
                    
                    # Create associations with related memories
                    associations = await self._create_memory_associations(memory, user_id)
                    new_associations += len(associations)
                    
                elif consolidation_strength < 0.3:
                    # Weaken memory
                    await self._weaken_memory(memory.memory_id)
                    weakened_count += 1
                
                consolidated_count += 1
            
            # Calculate consolidation quality
            total_memories = consolidated_count
            consolidation_quality = (strengthened_count / total_memories) if total_memories > 0 else 0.0
            
            result = MemoryConsolidationResult(
                consolidated_memories=consolidated_count,
                strengthened_memories=strengthened_count,
                weakened_memories=weakened_count,
                new_associations=new_associations,
                consolidation_quality=consolidation_quality
            )
            
            logger.info(f"✅ Memory consolidation completed: {result}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to consolidate memories: {e}")
            return MemoryConsolidationResult(0, 0, 0, 0, 0.0)
    
    async def create_memory_associations(
        self,
        memory: AdvancedMemory,
        user_id: str = "mainza-user"
    ) -> List[str]:
        """Create associations between memories"""
        try:
            associations = []
            
            # Find similar memories using embedding similarity
            similar_memories = await self._find_similar_memories(memory, user_id)
            
            for similar_memory in similar_memories:
                # Create association relationship
                association_cypher = """
                MATCH (m1:AdvancedMemory {memory_id: $memory_id})
                MATCH (m2:AdvancedMemory {memory_id: $similar_memory_id})
                CREATE (m1)-[:ASSOCIATED_WITH {
                    association_strength: $strength,
                    association_type: $type,
                    created_at: $timestamp
                }]->(m2)
                RETURN m1.memory_id AS memory_id
                """
                
                strength = self._calculate_association_strength(memory, similar_memory)
                association_type = self._determine_association_type(memory, similar_memory)
                
                result = self.neo4j.execute_write_query(association_cypher, {
                    "memory_id": memory.memory_id,
                    "similar_memory_id": similar_memory.memory_id,
                    "strength": strength,
                    "type": association_type,
                    "timestamp": datetime.now().isoformat()
                })
                
                associations.append(similar_memory.memory_id)
            
            logger.info(f"✅ Created {len(associations)} memory associations")
            return associations
            
        except Exception as e:
            logger.error(f"❌ Failed to create memory associations: {e}")
            return []
    
    def _calculate_episodic_importance(
        self,
        content: str,
        emotional_context: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ) -> float:
        """Calculate importance score for episodic memories"""
        base_score = 0.5
        
        # Emotional intensity boost
        emotional_intensity = emotional_context.get("intensity", 0.5)
        base_score += emotional_intensity * 0.3
        
        # Consciousness level boost
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        base_score += consciousness_level * 0.2
        
        # Content length boost (longer content often more important)
        content_length = len(content.split())
        length_boost = min(0.2, content_length / 100.0)
        base_score += length_boost
        
        return min(1.0, base_score)
    
    def _calculate_emotional_importance(
        self,
        content: str,
        emotional_context: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ) -> float:
        """Calculate importance score for emotional memories"""
        base_score = 0.6  # Emotional memories start higher
        
        # Emotional intensity boost
        emotional_intensity = emotional_context.get("intensity", 0.5)
        base_score += emotional_intensity * 0.4
        
        # Valence impact (strong positive or negative emotions)
        valence = abs(emotional_context.get("valence", 0.0))
        base_score += valence * 0.2
        
        # Consciousness level boost
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        base_score += consciousness_level * 0.1
        
        return min(1.0, base_score)
    
    def _calculate_consolidation_strength(self, memory: AdvancedMemory) -> float:
        """Calculate consolidation strength for a memory"""
        base_strength = memory.importance_score
        
        # Access frequency boost
        access_boost = min(0.3, memory.access_frequency / 10.0)
        base_strength += access_boost
        
        # Time decay adjustment
        time_since_creation = (datetime.now() - memory.created_at).days
        time_decay = max(0.1, 1.0 - (time_since_creation * 0.01))
        base_strength *= time_decay
        
        return min(1.0, base_strength)
    
    async def _find_similar_memories(
        self,
        memory: AdvancedMemory,
        user_id: str,
        limit: int = 5
    ) -> List[AdvancedMemory]:
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
                "memory_id": memory.memory_id,
                "memory_type": memory.memory_type.value,
                "limit": limit
            })
            
            similar_memories = []
            for record in result:
                memory_data = record["m"]
                similar_memory = self._neo4j_to_advanced_memory(memory_data)
                similar_memories.append(similar_memory)
            
            return similar_memories
            
        except Exception as e:
            logger.error(f"❌ Failed to find similar memories: {e}")
            return []
    
    def _calculate_association_strength(
        self,
        memory1: AdvancedMemory,
        memory2: AdvancedMemory
    ) -> float:
        """Calculate association strength between two memories"""
        # Base strength from importance scores
        base_strength = (memory1.importance_score + memory2.importance_score) / 2.0
        
        # Type compatibility boost
        if memory1.memory_type == memory2.memory_type:
            base_strength += 0.2
        
        # Emotional context similarity
        if memory1.emotional_context and memory2.emotional_context:
            emotional_similarity = self._calculate_emotional_similarity(
                memory1.emotional_context, memory2.emotional_context
            )
            base_strength += emotional_similarity * 0.3
        
        return min(1.0, base_strength)
    
    def _calculate_emotional_similarity(
        self,
        emotional_context1: Dict[str, Any],
        emotional_context2: Dict[str, Any]
    ) -> float:
        """Calculate emotional similarity between two contexts"""
        # Simple similarity based on emotional state
        state1 = emotional_context1.get("emotional_state", "")
        state2 = emotional_context2.get("emotional_state", "")
        
        if state1 == state2:
            return 0.8
        elif state1 in ["curious", "excited"] and state2 in ["curious", "excited"]:
            return 0.6
        elif state1 in ["focused", "determined"] and state2 in ["focused", "determined"]:
            return 0.6
        else:
            return 0.3
    
    def _determine_association_type(
        self,
        memory1: AdvancedMemory,
        memory2: AdvancedMemory
    ) -> str:
        """Determine the type of association between two memories"""
        if memory1.memory_type == memory2.memory_type:
            return "same_type"
        elif memory1.memory_type == MemoryType.EMOTIONAL and memory2.memory_type == MemoryType.EPISODIC:
            return "emotional_episodic"
        elif memory1.memory_type == MemoryType.CONSCIOUSNESS and memory2.memory_type == MemoryType.REFLECTION:
            return "consciousness_reflection"
        else:
            return "general"
    
    async def _store_advanced_memory(self, memory: AdvancedMemory, user_id: str):
        """Store advanced memory in Neo4j"""
        try:
            cypher = """
            MERGE (u:User {user_id: $user_id})
            CREATE (m:AdvancedMemory {
                memory_id: $memory_id,
                content: $content,
                memory_type: $memory_type,
                consolidation_level: $consolidation_level,
                emotional_context: $emotional_context,
                consciousness_context: $consciousness_context,
                importance_score: $importance_score,
                access_frequency: $access_frequency,
                last_accessed: $last_accessed,
                created_at: $created_at,
                embedding: $embedding,
                decay_rate: $decay_rate,
                consolidation_strength: $consolidation_strength,
                metadata: $metadata
            })
            CREATE (u)-[:HAS_MEMORY]->(m)
            
            RETURN m.memory_id AS memory_id
            """
            
            result = self.neo4j.execute_write_query(cypher, {
                "user_id": user_id,
                "memory_id": memory.memory_id,
                "content": memory.content,
                "memory_type": memory.memory_type.value,
                "consolidation_level": memory.consolidation_level.value,
                "emotional_context": json.dumps(memory.emotional_context),
                "consciousness_context": json.dumps(memory.consciousness_context),
                "importance_score": memory.importance_score,
                "access_frequency": memory.access_frequency,
                "last_accessed": memory.last_accessed.isoformat(),
                "created_at": memory.created_at.isoformat(),
                "embedding": memory.embedding,
                "decay_rate": memory.decay_rate,
                "consolidation_strength": memory.consolidation_strength,
                "metadata": json.dumps(memory.metadata)
            })
            
            logger.debug(f"✅ Stored advanced memory: {result}")
            
        except Exception as e:
            logger.error(f"❌ Failed to store advanced memory: {e}")
            raise
    
    def _neo4j_to_advanced_memory(self, memory_data: Dict[str, Any]) -> AdvancedMemory:
        """Convert Neo4j memory data to AdvancedMemory object"""
        return AdvancedMemory(
            memory_id=memory_data["memory_id"],
            content=memory_data["content"],
            memory_type=MemoryType(memory_data["memory_type"]),
            consolidation_level=MemoryConsolidationLevel(memory_data["consolidation_level"]),
            emotional_context=json.loads(memory_data.get("emotional_context", "{}")),
            consciousness_context=json.loads(memory_data.get("consciousness_context", "{}")),
            importance_score=memory_data["importance_score"],
            access_frequency=memory_data["access_frequency"],
            last_accessed=datetime.fromisoformat(memory_data["last_accessed"]),
            created_at=datetime.fromisoformat(memory_data["created_at"]),
            embedding=memory_data["embedding"],
            decay_rate=memory_data.get("decay_rate", 0.95),
            consolidation_strength=memory_data.get("consolidation_strength", 0.5),
            metadata=json.loads(memory_data.get("metadata", "{}"))
        )
    
    async def _strengthen_memory(self, memory_id: str, consolidation_strength: float):
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
    
    async def _weaken_memory(self, memory_id: str):
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

# Global instance
advanced_memory_architecture = AdvancedMemoryArchitecture()
