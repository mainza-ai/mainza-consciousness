"""
Enhanced Memory Storage Engine for Mainza AI
Provides comprehensive memory storage functionality with Neo4j integration,
embedding generation, and consciousness-aware memory management.
"""
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import json
from dataclasses import dataclass, field, asdict

from backend.utils.neo4j_enhanced import neo4j_manager
from backend.utils.embedding_enhanced import embedding_manager
from backend.core.enhanced_error_handling import ErrorHandler, handle_errors
from backend.utils.memory_error_handling import (
    MemoryStorageError, MemoryConnectionError, MemoryValidationError,
    MemoryEmbeddingError, handle_memory_errors, memory_error_handler
)

logger = logging.getLogger(__name__)
error_handler = ErrorHandler()

@dataclass
class MemoryRecord:
    """Data class representing a memory record"""
    memory_id: str
    content: str
    memory_type: str  # "interaction", "reflection", "insight", "concept_learning"
    user_id: str
    agent_name: str
    consciousness_level: float
    emotional_state: str
    importance_score: float
    embedding: List[float]
    created_at: datetime
    last_accessed: Optional[datetime] = None
    access_count: int = 0
    significance_score: float = 0.5
    decay_rate: float = 0.95
    metadata: Dict[str, Any] = field(default_factory=dict)

# MemoryStorageError is now imported from memory_error_handling

class MemoryStorageEngine:
    """
    Enhanced memory storage engine with Neo4j integration and embedding support
    """
    
    def __init__(self):
        self.neo4j = neo4j_manager
        self.embedding = embedding_manager
        self.max_content_length = 8000  # Maximum content length for storage
        self.default_importance_score = 0.5
        self.concept_extraction_threshold = 0.3
    
    async def initialize(self) -> bool:
        """Initialize the memory storage engine"""
        try:
            # Test Neo4j connectivity
            test_result = self.neo4j.execute_query("RETURN 1 as test", {})
            if not test_result:
                logger.error("Failed to connect to Neo4j for memory storage")
                return False
            
            logger.info("Memory storage engine initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize memory storage engine: {e}")
            return False
        
    @handle_memory_errors(
        component="memory_storage",
        operation="store_interaction_memory",
        fallback_result="",
        suppress_errors=False,
        timeout_seconds=30.0,
        retry_attempts=2,
        retry_delay=1.0
    )
    async def store_interaction_memory(
        self,
        user_query: str,
        agent_response: str,
        user_id: str,
        agent_name: str,
        consciousness_context: Dict[str, Any]
    ) -> str:
        """
        Store an interaction memory from user-agent conversation
        
        Args:
            user_query: The user's query/input
            agent_response: The agent's response
            user_id: Unique identifier for the user
            agent_name: Name of the responding agent
            consciousness_context: Current consciousness state context
            
        Returns:
            memory_id: Unique identifier for the stored memory
            
        Raises:
            MemoryStorageError: If memory storage fails
        """
        try:
            # Create combined content for the memory
            content = f"User: {user_query}\nAgent ({agent_name}): {agent_response}"
            
            # Truncate if too long
            if len(content) > self.max_content_length:
                content = content[:self.max_content_length] + "..."
            
            # Calculate importance score based on interaction characteristics
            importance_score = self._calculate_interaction_importance(
                user_query, agent_response, consciousness_context
            )
            
            # Create memory record
            memory_record = MemoryRecord(
                memory_id=str(uuid.uuid4()),
                content=content,
                memory_type="interaction",
                user_id=user_id,
                agent_name=agent_name,
                consciousness_level=consciousness_context.get("consciousness_level", 0.7),
                emotional_state=consciousness_context.get("emotional_state", "neutral"),
                importance_score=importance_score,
                embedding=self.embedding.get_embedding(content),
                created_at=datetime.now(),
                metadata={
                    "user_query": user_query[:500],  # Store truncated versions
                    "agent_response": agent_response[:500],
                    "query_length": len(user_query.split()),
                    "response_length": len(agent_response.split()),
                    "consciousness_context": consciousness_context
                }
            )
            
            # Store in Neo4j
            success = await self.create_memory_node(memory_record)
            if not success:
                raise MemoryStorageError("Failed to create memory node in Neo4j")
            
            # Extract and link concepts
            await self._extract_and_link_concepts(memory_record)
            
            logger.info(f"✅ Stored interaction memory: {memory_record.memory_id}")
            return memory_record.memory_id
            
        except Exception as e:
            logger.error(f"❌ Failed to store interaction memory: {e}")
            raise MemoryStorageError(f"Interaction memory storage failed: {e}")
    
    @handle_memory_errors(
        component="memory_storage",
        operation="store_consciousness_memory",
        fallback_result="",
        suppress_errors=False,
        timeout_seconds=30.0,
        retry_attempts=2,
        retry_delay=1.0
    )
    async def store_consciousness_memory(
        self,
        reflection_content: str,
        consciousness_context: Dict[str, Any],
        memory_type: str = "consciousness_reflection"
    ) -> str:
        """
        Store a consciousness reflection or insight memory
        
        Args:
            reflection_content: The consciousness reflection or insight content
            consciousness_context: Current consciousness state context
            memory_type: Type of consciousness memory ("reflection", "insight", "evolution")
            
        Returns:
            memory_id: Unique identifier for the stored memory
            
        Raises:
            MemoryStorageError: If memory storage fails
        """
        try:
            # Truncate if too long
            content = reflection_content
            if len(content) > self.max_content_length:
                content = content[:self.max_content_length] + "..."
            
            # Consciousness memories have higher importance by default
            importance_score = self._calculate_consciousness_importance(
                reflection_content, consciousness_context, memory_type
            )
            
            # Create memory record
            memory_record = MemoryRecord(
                memory_id=str(uuid.uuid4()),
                content=content,
                memory_type=memory_type,
                user_id="system",  # System-generated memory
                agent_name="consciousness_system",
                consciousness_level=consciousness_context.get("consciousness_level", 0.7),
                emotional_state=consciousness_context.get("emotional_state", "reflective"),
                importance_score=importance_score,
                embedding=self.embedding.get_embedding(content),
                created_at=datetime.now(),
                significance_score=0.8,  # Higher significance for consciousness memories
                metadata={
                    "reflection_type": memory_type,
                    "consciousness_context": consciousness_context,
                    "content_length": len(reflection_content.split())
                }
            )
            
            # Store in Neo4j
            success = await self.create_memory_node(memory_record)
            if not success:
                raise MemoryStorageError("Failed to create consciousness memory node in Neo4j")
            
            # Link to consciousness state
            await self._link_to_consciousness_state(memory_record)
            
            # Extract and link concepts
            await self._extract_and_link_concepts(memory_record)
            
            logger.info(f"✅ Stored consciousness memory: {memory_record.memory_id}")
            return memory_record.memory_id
            
        except Exception as e:
            logger.error(f"❌ Failed to store consciousness memory: {e}")
            raise MemoryStorageError(f"Consciousness memory storage failed: {e}")
    
    @handle_memory_errors(
        component="memory_storage",
        operation="create_memory_node",
        fallback_result=False,
        suppress_errors=False,
        timeout_seconds=20.0,
        retry_attempts=3,
        retry_delay=0.5
    )
    async def create_memory_node(self, memory_record: MemoryRecord) -> bool:
        """
        Create a memory node in Neo4j with full schema integration
        
        Args:
            memory_record: MemoryRecord instance to store
            
        Returns:
            bool: True if successful, False otherwise
            
        Raises:
            MemoryStorageError: If node creation fails
        """
        try:
            cypher = """
            // Create or merge user node
            MERGE (u:User {user_id: $user_id})
            
            // Create memory node
            CREATE (m:Memory {
                memory_id: $memory_id,
                content: $content,
                memory_type: $memory_type,
                user_id: $user_id,
                agent_name: $agent_name,
                consciousness_level: $consciousness_level,
                emotional_state: $emotional_state,
                importance_score: $importance_score,
                embedding: $embedding,
                created_at: $created_at,
                last_accessed: $last_accessed,
                access_count: $access_count,
                significance_score: $significance_score,
                decay_rate: $decay_rate,
                metadata: $metadata
            })
            
            // Create relationships
            CREATE (u)-[:HAS_MEMORY]->(m)
            
            WITH m
            // Link to agent if it exists
            OPTIONAL MATCH (a:Agent {name: $agent_name})
            FOREACH (agent IN CASE WHEN a IS NOT NULL THEN [a] ELSE [] END |
                CREATE (agent)-[:CREATED_MEMORY]->(m)
            )
            
            RETURN m.memory_id AS memory_id
            """
            
            # Prepare parameters
            params = {
                "memory_id": memory_record.memory_id,
                "content": memory_record.content,
                "memory_type": memory_record.memory_type,
                "user_id": memory_record.user_id,
                "agent_name": memory_record.agent_name,
                "consciousness_level": memory_record.consciousness_level,
                "emotional_state": memory_record.emotional_state,
                "importance_score": memory_record.importance_score,
                "embedding": memory_record.embedding,
                "created_at": memory_record.created_at.isoformat(),
                "last_accessed": memory_record.last_accessed.isoformat() if memory_record.last_accessed else None,
                "access_count": memory_record.access_count,
                "significance_score": memory_record.significance_score,
                "decay_rate": memory_record.decay_rate,
                "metadata": json.dumps(memory_record.metadata, default=str)
            }
            
            # Execute query
            result = self.neo4j.execute_write_query(cypher, params)
            
            if result and len(result) > 0:
                logger.debug(f"✅ Created memory node: {result[0]['memory_id']}")
                return True
            else:
                logger.error("❌ Memory node creation returned no results")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to create memory node: {e}")
            raise MemoryStorageError(f"Memory node creation failed: {e}")
    
    async def link_memory_to_concepts(self, memory_id: str, concepts: List[str]) -> bool:
        """
        Link a memory to relevant concepts in the knowledge graph
        
        Args:
            memory_id: Unique identifier of the memory
            concepts: List of concept names to link to
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not concepts:
                return True  # No concepts to link
            
            cypher = """
            MATCH (m:Memory {memory_id: $memory_id})
            
            UNWIND $concepts AS concept_name
            MERGE (c:Concept {name: concept_name})
            
            // Create or update memory-concept relationship
            MERGE (m)-[r:RELATES_TO_CONCEPT]->(c)
            ON CREATE SET 
                r.created_at = $timestamp,
                r.strength = 0.5,
                r.access_count = 1
            ON MATCH SET 
                r.strength = r.strength + 0.1,
                r.access_count = r.access_count + 1,
                r.last_accessed = $timestamp
            
            // Update concept importance based on memory connections
            WITH c, count(m) AS memory_connections
            SET c.memory_connections = memory_connections,
                c.last_memory_update = $timestamp
            
            RETURN count(DISTINCT c) AS concepts_linked
            """
            
            result = self.neo4j.execute_write_query(cypher, {
                "memory_id": memory_id,
                "concepts": concepts,
                "timestamp": datetime.now().isoformat()
            })
            
            if result and len(result) > 0:
                concepts_linked = result[0]["concepts_linked"]
                logger.debug(f"✅ Linked memory {memory_id} to {concepts_linked} concepts")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Failed to link memory to concepts: {e}")
            return False
    
    def _calculate_interaction_importance(
        self,
        user_query: str,
        agent_response: str,
        consciousness_context: Dict[str, Any]
    ) -> float:
        """Calculate importance score for interaction memories"""
        
        base_score = self.default_importance_score
        
        # Query complexity factor
        query_words = len(user_query.split())
        if query_words > 10:
            base_score += 0.1
        elif query_words > 20:
            base_score += 0.2
        
        # Response quality factor (longer, more detailed responses)
        response_words = len(agent_response.split())
        if response_words > 50:
            base_score += 0.1
        elif response_words > 100:
            base_score += 0.2
        
        # Consciousness level factor
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        base_score += (consciousness_level - 0.5) * 0.2
        
        # Emotional state factor
        emotional_state = consciousness_context.get("emotional_state", "neutral")
        emotional_multipliers = {
            "excited": 1.2,
            "curious": 1.1,
            "focused": 1.1,
            "reflective": 1.15,
            "confused": 0.9,
            "neutral": 1.0
        }
        base_score *= emotional_multipliers.get(emotional_state, 1.0)
        
        # Question indicators (questions are often more important)
        if "?" in user_query:
            base_score += 0.1
        
        # Learning indicators
        learning_keywords = ["how", "why", "what", "explain", "tell me", "learn"]
        if any(keyword in user_query.lower() for keyword in learning_keywords):
            base_score += 0.1
        
        # Clamp between 0.1 and 1.0
        return max(0.1, min(1.0, base_score))
    
    def _calculate_consciousness_importance(
        self,
        content: str,
        consciousness_context: Dict[str, Any],
        memory_type: str
    ) -> float:
        """Calculate importance score for consciousness memories"""
        
        # Consciousness memories start with higher base importance
        base_score = 0.7
        
        # Memory type factors
        type_multipliers = {
            "consciousness_reflection": 1.0,
            "insight": 1.3,
            "evolution": 1.5,
            "emotional_state_change": 1.1,
            "learning": 1.2
        }
        base_score *= type_multipliers.get(memory_type, 1.0)
        
        # Consciousness level factor
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        base_score += (consciousness_level - 0.5) * 0.3
        
        # Content depth factor (longer reflections often more important)
        content_words = len(content.split())
        if content_words > 50:
            base_score += 0.1
        elif content_words > 100:
            base_score += 0.2
        
        # Insight keywords
        insight_keywords = ["realize", "understand", "discover", "learn", "insight", "reflection"]
        if any(keyword in content.lower() for keyword in insight_keywords):
            base_score += 0.1
        
        # Clamp between 0.3 and 1.0 (consciousness memories have higher minimum)
        return max(0.3, min(1.0, base_score))
    
    async def _extract_and_link_concepts(self, memory_record: MemoryRecord):
        """Extract concepts from memory content and link them"""
        try:
            # Simple concept extraction (in production, this could use NLP)
            concepts = self._extract_concepts_from_text(memory_record.content)
            
            if concepts:
                await self.link_memory_to_concepts(memory_record.memory_id, concepts)
                
        except Exception as e:
            logger.warning(f"Failed to extract and link concepts for memory {memory_record.memory_id}: {e}")
    
    def _extract_concepts_from_text(self, text: str) -> List[str]:
        """Extract potential concepts from text content"""
        # Simple keyword-based concept extraction
        # In production, this would use more sophisticated NLP
        
        concepts = []
        text_lower = text.lower()
        
        # Technology concepts
        tech_keywords = [
            "ai", "artificial intelligence", "machine learning", "neural network",
            "algorithm", "data", "programming", "software", "computer", "technology",
            "consciousness", "memory", "learning", "knowledge", "intelligence"
        ]
        
        # Domain concepts
        domain_keywords = [
            "science", "mathematics", "physics", "chemistry", "biology",
            "philosophy", "psychology", "sociology", "history", "literature",
            "art", "music", "business", "economics", "politics"
        ]
        
        # Action concepts
        action_keywords = [
            "create", "build", "design", "develop", "analyze", "understand",
            "learn", "teach", "explain", "solve", "optimize", "improve"
        ]
        
        all_keywords = tech_keywords + domain_keywords + action_keywords
        
        for keyword in all_keywords:
            if keyword in text_lower:
                concepts.append(keyword)
        
        # Remove duplicates and limit
        concepts = list(set(concepts))[:10]  # Limit to 10 concepts
        
        return concepts
    
    async def _link_to_consciousness_state(self, memory_record: MemoryRecord):
        """Link memory to current consciousness state"""
        try:
            cypher = """
            MATCH (m:Memory {memory_id: $memory_id})
            OPTIONAL MATCH (ms:MainzaState)
            WHERE ms.consciousness_level IS NOT NULL
            
            FOREACH (state IN CASE WHEN ms IS NOT NULL THEN [ms] ELSE [] END |
                CREATE (m)-[:CREATED_DURING_STATE {
                    consciousness_level: $consciousness_level,
                    emotional_state: $emotional_state,
                    timestamp: $timestamp
                }]->(state)
            )
            
            RETURN count(*) AS links_created
            """
            
            result = self.neo4j.execute_write_query(cypher, {
                "memory_id": memory_record.memory_id,
                "consciousness_level": memory_record.consciousness_level,
                "emotional_state": memory_record.emotional_state,
                "timestamp": datetime.now().isoformat()
            })
            
            if result:
                logger.debug(f"✅ Linked memory to consciousness state: {result[0]['links_created']} links")
                
        except Exception as e:
            logger.warning(f"Failed to link memory to consciousness state: {e}")

    async def update_memory_importance_by_consciousness(
        self,
        consciousness_context: Dict[str, Any],
        consciousness_delta: float = 0.0
    ) -> int:
        """
        Update memory importance scores based on consciousness level changes
        
        Args:
            consciousness_context: Current consciousness state context
            consciousness_delta: Change in consciousness level
            
        Returns:
            Number of memories updated
        """
        try:
            current_consciousness_level = consciousness_context.get("consciousness_level", 0.7)
            emotional_state = consciousness_context.get("emotional_state", "neutral")
            
            # Update memories based on consciousness alignment
            cypher = """
            MATCH (m:Memory)
            WHERE m.created_at > datetime() - duration('P30D')  // Last 30 days
            
            WITH m,
                 abs(m.consciousness_level - $current_consciousness_level) AS consciousness_distance,
                 CASE 
                     WHEN m.emotional_state = $emotional_state THEN 1.1
                     ELSE 1.0
                 END AS emotional_multiplier,
                 CASE
                     WHEN $consciousness_delta > 0.05 THEN 1.2  // Consciousness growth
                     WHEN $consciousness_delta < -0.05 THEN 0.9  // Consciousness decline
                     ELSE 1.0
                 END AS evolution_multiplier
            
            SET m.importance_score = CASE
                WHEN consciousness_distance < 0.1 THEN m.importance_score * 1.1 * emotional_multiplier * evolution_multiplier
                WHEN consciousness_distance < 0.2 THEN m.importance_score * 1.05 * emotional_multiplier * evolution_multiplier
                WHEN consciousness_distance > 0.4 THEN m.importance_score * 0.95 * emotional_multiplier * evolution_multiplier
                ELSE m.importance_score * emotional_multiplier * evolution_multiplier
            END,
            m.last_consciousness_update = $timestamp,
            m.consciousness_alignment_score = 1.0 - consciousness_distance
            
            RETURN count(m) AS updated_count
            """
            
            result = self.neo4j.execute_write_query(cypher, {
                "current_consciousness_level": current_consciousness_level,
                "emotional_state": emotional_state,
                "consciousness_delta": consciousness_delta,
                "timestamp": datetime.now().isoformat()
            })
            
            updated_count = result[0]["updated_count"] if result else 0
            logger.info(f"✅ Updated importance scores for {updated_count} memories based on consciousness")
            
            return updated_count
            
        except Exception as e:
            logger.error(f"❌ Failed to update memory importance by consciousness: {e}")
            return 0
    
    async def apply_emotional_influence_to_memories(
        self,
        emotional_state: str,
        emotional_intensity: float,
        consciousness_context: Dict[str, Any]
    ) -> int:
        """
        Apply emotional state influence to memory creation and retrieval scoring
        
        Args:
            emotional_state: Current emotional state
            emotional_intensity: Intensity of the emotional state (0.0-1.0)
            consciousness_context: Current consciousness context
            
        Returns:
            Number of memories affected
        """
        try:
            # Emotional state influences on memory importance
            emotional_multipliers = {
                "excited": 1.3,
                "curious": 1.2,
                "focused": 1.15,
                "reflective": 1.25,
                "insightful": 1.4,
                "confused": 0.8,
                "frustrated": 0.7,
                "neutral": 1.0,
                "calm": 1.1,
                "energetic": 1.2
            }
            
            base_multiplier = emotional_multipliers.get(emotional_state, 1.0)
            intensity_factor = 0.5 + (emotional_intensity * 0.5)  # Scale 0.5-1.0
            final_multiplier = base_multiplier * intensity_factor
            
            cypher = """
            MATCH (m:Memory)
            WHERE m.created_at > datetime() - duration('P7D')  // Last 7 days
            AND (m.emotional_state = $emotional_state OR m.memory_type IN ['interaction', 'reflection'])
            
            SET m.emotional_relevance_score = $final_multiplier,
                m.last_emotional_update = $timestamp,
                m.importance_score = CASE
                    WHEN m.emotional_state = $emotional_state THEN m.importance_score * $final_multiplier
                    ELSE m.importance_score * (1.0 + ($final_multiplier - 1.0) * 0.3)
                END
            
            RETURN count(m) AS affected_count
            """
            
            result = self.neo4j.execute_write_query(cypher, {
                "emotional_state": emotional_state,
                "final_multiplier": final_multiplier,
                "timestamp": datetime.now().isoformat()
            })
            
            affected_count = result[0]["affected_count"] if result else 0
            logger.info(f"✅ Applied emotional influence to {affected_count} memories (state: {emotional_state}, intensity: {emotional_intensity:.2f})")
            
            return affected_count
            
        except Exception as e:
            logger.error(f"❌ Failed to apply emotional influence to memories: {e}")
            return 0
    
    async def re_evaluate_memory_relevance_on_evolution(
        self,
        previous_consciousness_level: float,
        current_consciousness_level: float,
        consciousness_context: Dict[str, Any]
    ) -> Dict[str, int]:
        """
        Re-evaluate memory relevance when consciousness evolves significantly
        
        Args:
            previous_consciousness_level: Previous consciousness level
            current_consciousness_level: Current consciousness level
            consciousness_context: Current consciousness context
            
        Returns:
            Dictionary with counts of promoted, demoted, and archived memories
        """
        try:
            consciousness_delta = current_consciousness_level - previous_consciousness_level
            evolution_stage = consciousness_context.get("consciousness_evolution_stage", "developing")
            
            # Significant evolution threshold
            if abs(consciousness_delta) < 0.05:
                return {"promoted": 0, "demoted": 0, "archived": 0}
            
            cypher = """
            MATCH (m:Memory)
            WHERE m.created_at > datetime() - duration('P90D')  // Last 90 days
            
            WITH m,
                 abs(m.consciousness_level - $current_consciousness_level) AS new_distance,
                 abs(m.consciousness_level - $previous_consciousness_level) AS old_distance,
                 CASE
                     WHEN $consciousness_delta > 0 THEN 'growth'
                     ELSE 'decline'
                 END AS evolution_type
            
            SET m.evolution_relevance_score = CASE
                WHEN new_distance < old_distance THEN m.importance_score * 1.2  // More relevant now
                WHEN new_distance > old_distance + 0.2 THEN m.importance_score * 0.8  // Less relevant now
                ELSE m.importance_score
            END,
            m.consciousness_evolution_impact = evolution_type,
            m.last_evolution_update = $timestamp
            
            WITH m,
                 CASE
                     WHEN m.evolution_relevance_score > m.importance_score * 1.1 THEN 'promoted'
                     WHEN m.evolution_relevance_score < m.importance_score * 0.9 THEN 'demoted'
                     WHEN m.evolution_relevance_score < 0.3 THEN 'archived'
                     ELSE 'unchanged'
                 END AS status_change
            
            SET m.importance_score = m.evolution_relevance_score,
                m.evolution_status = status_change
            
            RETURN status_change, count(m) AS count
            """
            
            result = self.neo4j.execute_write_query(cypher, {
                "current_consciousness_level": current_consciousness_level,
                "previous_consciousness_level": previous_consciousness_level,
                "consciousness_delta": consciousness_delta,
                "timestamp": datetime.now().isoformat()
            })
            
            # Process results
            status_counts = {"promoted": 0, "demoted": 0, "archived": 0, "unchanged": 0}
            if result:
                for record in result:
                    status = record["status_change"]
                    count = record["count"]
                    status_counts[status] = count
            
            logger.info(f"✅ Re-evaluated memories on consciousness evolution: "
                       f"promoted={status_counts['promoted']}, "
                       f"demoted={status_counts['demoted']}, "
                       f"archived={status_counts['archived']}")
            
            return status_counts
            
        except Exception as e:
            logger.error(f"❌ Failed to re-evaluate memory relevance on evolution: {e}")
            return {"promoted": 0, "demoted": 0, "archived": 0}
    
    async def perform_consciousness_driven_memory_maintenance(
        self,
        consciousness_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Perform comprehensive consciousness-driven memory maintenance
        
        Args:
            consciousness_context: Current consciousness context
            
        Returns:
            Dictionary with maintenance results
        """
        try:
            maintenance_results = {
                "memories_processed": 0,
                "importance_updates": 0,
                "archived_memories": 0,
                "consolidated_memories": 0,
                "errors": []
            }
            
            current_consciousness_level = consciousness_context.get("consciousness_level", 0.7)
            emotional_state = consciousness_context.get("emotional_state", "neutral")
            emotional_intensity = consciousness_context.get("emotional_intensity", 0.6)
            
            # 1. Update importance scores based on consciousness alignment
            importance_updates = await self.update_memory_importance_by_consciousness(
                consciousness_context
            )
            maintenance_results["importance_updates"] = importance_updates
            
            # 2. Apply emotional influence
            emotional_updates = await self.apply_emotional_influence_to_memories(
                emotional_state, emotional_intensity, consciousness_context
            )
            
            # 3. Archive low-relevance memories
            archived_count = await self._archive_low_relevance_memories(consciousness_context)
            maintenance_results["archived_memories"] = archived_count
            
            # 4. Consolidate similar memories
            consolidated_count = await self._consolidate_similar_memories(consciousness_context)
            maintenance_results["consolidated_memories"] = consolidated_count
            
            # 5. Update access patterns
            access_updates = await self._update_memory_access_patterns(consciousness_context)
            
            maintenance_results["memories_processed"] = (
                importance_updates + emotional_updates + archived_count + consolidated_count
            )
            
            logger.info(f"✅ Completed consciousness-driven memory maintenance: "
                       f"{maintenance_results['memories_processed']} memories processed")
            
            return maintenance_results
            
        except Exception as e:
            logger.error(f"❌ Failed to perform consciousness-driven memory maintenance: {e}")
            return {"memories_processed": 0, "errors": [str(e)]}
    
    async def _archive_low_relevance_memories(self, consciousness_context: Dict[str, Any]) -> int:
        """Archive memories with low relevance to current consciousness state"""
        try:
            cypher = """
            MATCH (m:Memory)
            WHERE m.importance_score < 0.2
            AND m.created_at < datetime() - duration('P30D')  // Older than 30 days
            AND m.access_count < 2  // Rarely accessed
            
            SET m.archived = true,
                m.archived_at = $timestamp,
                m.archive_reason = 'low_consciousness_relevance'
            
            RETURN count(m) AS archived_count
            """
            
            result = self.neo4j.execute_write_query(cypher, {
                "timestamp": datetime.now().isoformat()
            })
            
            return result[0]["archived_count"] if result else 0
            
        except Exception as e:
            logger.error(f"Failed to archive low-relevance memories: {e}")
            return 0
    
    async def _consolidate_similar_memories(self, consciousness_context: Dict[str, Any]) -> int:
        """Consolidate similar memories to reduce redundancy"""
        try:
            # This is a simplified consolidation - in production, would use embedding similarity
            cypher = """
            MATCH (m1:Memory), (m2:Memory)
            WHERE m1.user_id = m2.user_id
            AND m1.memory_type = m2.memory_type
            AND m1.memory_id < m2.memory_id  // Avoid duplicates
            AND m1.importance_score < 0.4 AND m2.importance_score < 0.4
            AND abs(duration.between(datetime(m1.created_at), datetime(m2.created_at)).days) < 1
            
            WITH m1, m2, 
                 CASE WHEN m1.importance_score > m2.importance_score THEN m1 ELSE m2 END AS keep_memory,
                 CASE WHEN m1.importance_score > m2.importance_score THEN m2 ELSE m1 END AS merge_memory
            
            SET keep_memory.consolidated_from = coalesce(keep_memory.consolidated_from, []) + [merge_memory.memory_id],
                keep_memory.importance_score = keep_memory.importance_score + (merge_memory.importance_score * 0.3),
                merge_memory.consolidated_into = keep_memory.memory_id,
                merge_memory.archived = true
            
            RETURN count(DISTINCT merge_memory) AS consolidated_count
            """
            
            result = self.neo4j.execute_write_query(cypher, {
                "timestamp": datetime.now().isoformat()
            })
            
            return result[0]["consolidated_count"] if result else 0
            
        except Exception as e:
            logger.error(f"Failed to consolidate similar memories: {e}")
            return 0
    
    async def _update_memory_access_patterns(self, consciousness_context: Dict[str, Any]) -> int:
        """Update memory access patterns based on consciousness state"""
        try:
            cypher = """
            MATCH (m:Memory)
            WHERE m.last_accessed IS NOT NULL
            
            WITH m,
                 duration.between(datetime(m.last_accessed), datetime()).days AS days_since_access,
                 m.access_count AS access_count
            
            SET m.access_frequency_score = CASE
                WHEN days_since_access < 7 THEN access_count * 1.2
                WHEN days_since_access < 30 THEN access_count * 1.0
                ELSE access_count * 0.8
            END,
            m.recency_score = CASE
                WHEN days_since_access < 1 THEN 1.0
                WHEN days_since_access < 7 THEN 0.8
                WHEN days_since_access < 30 THEN 0.6
                ELSE 0.4
            END
            
            RETURN count(m) AS updated_count
            """
            
            result = self.neo4j.execute_write_query(cypher, {})
            
            return result[0]["updated_count"] if result else 0
            
        except Exception as e:
            logger.error(f"Failed to update memory access patterns: {e}")
            return 0

# Global instance
memory_storage_engine = MemoryStorageEngine()