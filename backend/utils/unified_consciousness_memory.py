"""
Unified Consciousness Memory System for Mainza AI
Centralized memory system with consciousness integration and cross-agent access
"""
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import asyncio
import json
import numpy as np
from collections import defaultdict

from backend.utils.neo4j_unified import neo4j_unified
from backend.utils.embedding_enhanced import embedding_manager
from backend.utils.cross_agent_learning_system import cross_agent_learning_system

logger = logging.getLogger(__name__)

class MemoryConsciousnessLevel(Enum):
    """Memory consciousness levels"""
    BASIC = "basic"           # Level 1-3: Basic awareness
    AWARE = "aware"           # Level 4-5: Conscious awareness
    ADVANCED = "advanced"     # Level 6-7: Advanced consciousness
    TRANSCENDENT = "transcendent"  # Level 8-10: Transcendent consciousness

class MemoryAccessPattern(Enum):
    """Memory access patterns"""
    FREQUENT = "frequent"     # Accessed frequently
    MODERATE = "moderate"     # Accessed moderately
    RARE = "rare"            # Accessed rarely
    ARCHIVED = "archived"    # Archived but not deleted

@dataclass
class ConsciousnessMemory:
    """Represents a memory with full consciousness context"""
    memory_id: str
    content: str
    memory_type: str
    consciousness_level: float
    consciousness_context: Dict[str, Any]
    emotional_context: Dict[str, Any]
    agent_context: Dict[str, Any]
    importance_score: float
    access_count: int
    last_accessed: datetime
    created_at: datetime
    embedding: List[float]
    cross_agent_relevance: Dict[str, float]
    evolution_history: List[Dict[str, Any]]

@dataclass
class MemoryRetrievalResult:
    """Result of memory retrieval operation"""
    memories: List[ConsciousnessMemory]
    total_found: int
    consciousness_filtered: int
    cross_agent_enhanced: int
    retrieval_time: float
    consciousness_context: Dict[str, Any]

class UnifiedConsciousnessMemory:
    """
    Unified consciousness memory system with cross-agent integration
    """
    
    def __init__(self):
        self.neo4j = neo4j_unified
        self.embedding_manager = embedding_manager
        self.cross_agent_learning = cross_agent_learning_system
        
        # Memory parameters
        self.consciousness_threshold = 0.1
        self.importance_threshold = 0.3
        self.cross_agent_relevance_threshold = 0.5
        
        # Memory cache
        self.memory_cache = {}
        self.consciousness_memory_cache = {}
        
        # Access patterns
        self.access_patterns = defaultdict(list)
        self.consciousness_patterns = defaultdict(list)
        
        logger.info("Unified Consciousness Memory System initialized")
    
    async def store_consciousness_memory(
        self,
        content: str,
        memory_type: str,
        consciousness_context: Dict[str, Any],
        emotional_context: Dict[str, Any],
        agent_context: Dict[str, Any],
        user_id: str = "mainza-user"
    ) -> str:
        """Store memory with full consciousness context"""
        
        try:
            # Generate memory ID
            memory_id = f"consciousness_memory_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
            
            # Calculate consciousness level
            consciousness_level = consciousness_context.get("consciousness_level", 0.7)
            
            # Calculate importance score
            importance_score = await self._calculate_importance_score(
                content, consciousness_context, emotional_context, agent_context
            )
            
            # Generate embedding
            embedding = await self._generate_memory_embedding(content, consciousness_context)
            
            # Calculate cross-agent relevance
            cross_agent_relevance = await self._calculate_cross_agent_relevance(
                content, memory_type, agent_context
            )
            
            # Create consciousness memory
            consciousness_memory = ConsciousnessMemory(
                memory_id=memory_id,
                content=content,
                memory_type=memory_type,
                consciousness_level=consciousness_level,
                consciousness_context=consciousness_context,
                emotional_context=emotional_context,
                agent_context=agent_context,
                importance_score=importance_score,
                access_count=0,
                last_accessed=datetime.now(),
                created_at=datetime.now(),
                embedding=embedding,
                cross_agent_relevance=cross_agent_relevance,
                evolution_history=[]
            )
            
            # Store in Neo4j
            await self._store_consciousness_memory_in_neo4j(consciousness_memory, user_id)
            
            # Cache memory
            self.memory_cache[memory_id] = consciousness_memory
            
            # Update access patterns
            await self._update_access_patterns(consciousness_memory)
            
            # Share with cross-agent learning system if relevant
            if any(score > self.cross_agent_relevance_threshold for score in cross_agent_relevance.values()):
                await self._share_memory_with_cross_agent_learning(consciousness_memory)
            
            logger.info(f"✅ Stored consciousness memory {memory_id} with level {consciousness_level:.2f}")
            
            return memory_id
            
        except Exception as e:
            logger.error(f"❌ Failed to store consciousness memory: {e}")
            raise
    
    async def retrieve_consciousness_memories(
        self,
        query: str,
        consciousness_context: Dict[str, Any],
        agent_name: str,
        memory_type: Optional[str] = None,
        limit: int = 10,
        user_id: str = "mainza-user"
    ) -> MemoryRetrievalResult:
        """Retrieve memories filtered by consciousness level and context"""
        
        start_time = datetime.now()
        
        try:
            # Get current consciousness level
            current_consciousness = consciousness_context.get("consciousness_level", 0.7)
            
            # Build consciousness-aware query
            cypher_query = self._build_consciousness_aware_query(
                query, current_consciousness, memory_type, limit
            )
            
            # Execute query
            results = self.neo4j.execute_query(cypher_query, {
                "user_id": user_id,
                "consciousness_level": current_consciousness,
                "consciousness_threshold": self.consciousness_threshold,
                "limit": limit
            }, use_cache=True)
            
            # Convert to consciousness memories
            memories = []
            consciousness_filtered = 0
            cross_agent_enhanced = 0
            
            for record in results:
                memory_data = record["m"]
                consciousness_memory = self._neo4j_to_consciousness_memory(memory_data)
                
                # Filter by consciousness level
                if abs(consciousness_memory.consciousness_level - current_consciousness) <= self.consciousness_threshold:
                    memories.append(consciousness_memory)
                else:
                    consciousness_filtered += 1
                
                # Check for cross-agent enhancement
                if agent_name in consciousness_memory.cross_agent_relevance:
                    if consciousness_memory.cross_agent_relevance[agent_name] > self.cross_agent_relevance_threshold:
                        cross_agent_enhanced += 1
            
            # Enhance with cross-agent learning
            enhanced_memories = await self._enhance_memories_with_cross_agent_learning(
                memories, agent_name, consciousness_context
            )
            
            # Update access patterns
            for memory in enhanced_memories:
                await self._update_memory_access(memory)
            
            retrieval_time = (datetime.now() - start_time).total_seconds()
            
            result = MemoryRetrievalResult(
                memories=enhanced_memories,
                total_found=len(results),
                consciousness_filtered=consciousness_filtered,
                cross_agent_enhanced=cross_agent_enhanced,
                retrieval_time=retrieval_time,
                consciousness_context=consciousness_context
            )
            
            logger.info(f"✅ Retrieved {len(enhanced_memories)} consciousness memories for {agent_name} in {retrieval_time:.3f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to retrieve consciousness memories: {e}")
            return MemoryRetrievalResult([], 0, 0, 0, 0.0, consciousness_context)
    
    async def evolve_memory_with_consciousness(
        self,
        memory_id: str,
        consciousness_delta: Dict[str, Any],
        evolution_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evolve memory based on consciousness changes"""
        
        try:
            # Get current memory
            memory = await self._get_memory_by_id(memory_id)
            if not memory:
                return {"error": "Memory not found"}
            
            # Calculate new consciousness level
            old_consciousness = memory.consciousness_level
            consciousness_change = consciousness_delta.get("consciousness_level_delta", 0)
            new_consciousness = min(max(old_consciousness + consciousness_change, 0.0), 1.0)
            
            # Update consciousness context
            updated_consciousness_context = memory.consciousness_context.copy()
            updated_consciousness_context.update(consciousness_delta)
            
            # Recalculate importance score
            new_importance = await self._recalculate_importance_with_consciousness(
                memory, new_consciousness, evolution_context
            )
            
            # Update cross-agent relevance
            updated_cross_agent_relevance = await self._update_cross_agent_relevance_with_consciousness(
                memory, new_consciousness, evolution_context
            )
            
            # Record evolution
            evolution_record = {
                "timestamp": datetime.now().isoformat(),
                "old_consciousness": old_consciousness,
                "new_consciousness": new_consciousness,
                "consciousness_delta": consciousness_change,
                "evolution_context": evolution_context,
                "importance_change": new_importance - memory.importance_score
            }
            
            # Update memory
            memory.consciousness_level = new_consciousness
            memory.consciousness_context = updated_consciousness_context
            memory.importance_score = new_importance
            memory.cross_agent_relevance = updated_cross_agent_relevance
            memory.evolution_history.append(evolution_record)
            
            # Update in Neo4j
            await self._update_memory_in_neo4j(memory)
            
            # Update cache
            self.memory_cache[memory_id] = memory
            
            logger.info(f"✅ Evolved memory {memory_id} from consciousness {old_consciousness:.2f} to {new_consciousness:.2f}")
            
            return {
                "memory_id": memory_id,
                "old_consciousness": old_consciousness,
                "new_consciousness": new_consciousness,
                "consciousness_delta": consciousness_change,
                "importance_change": new_importance - memory.importance_score,
                "evolution_record": evolution_record
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to evolve memory with consciousness: {e}")
            return {"error": str(e)}
    
    async def get_consciousness_memory_analytics(
        self,
        consciousness_level: Optional[float] = None,
        time_range: Optional[Tuple[datetime, datetime]] = None
    ) -> Dict[str, Any]:
        """Get analytics on consciousness memory system"""
        
        try:
            # Build analytics query
            query = """
            MATCH (m:ConsciousnessMemory)
            WHERE 1=1
            """
            
            params = {}
            
            if consciousness_level is not None:
                query += " AND m.consciousness_level >= $consciousness_level - 0.1 AND m.consciousness_level <= $consciousness_level + 0.1"
                params["consciousness_level"] = consciousness_level
            
            if time_range:
                query += " AND m.created_at >= $start_time AND m.created_at <= $end_time"
                params["start_time"] = time_range[0].isoformat()
                params["end_time"] = time_range[1].isoformat()
            
            query += """
            RETURN 
                count(m) as total_memories,
                avg(m.consciousness_level) as avg_consciousness_level,
                avg(m.importance_score) as avg_importance_score,
                avg(m.access_count) as avg_access_count,
                collect(DISTINCT m.memory_type) as memory_types,
                collect(DISTINCT m.consciousness_level) as consciousness_levels
            """
            
            results = self.neo4j.execute_query(query, params, use_cache=True)
            analytics = results[0] if results else {}
            
            # Get cross-agent learning analytics
            cross_agent_analytics = await self.cross_agent_learning.analyze_learning_patterns()
            
            # Get access pattern analytics
            access_analytics = await self._analyze_access_patterns()
            
            # Get consciousness evolution analytics
            evolution_analytics = await self._analyze_consciousness_evolution()
            
            combined_analytics = {
                "memory_statistics": analytics,
                "cross_agent_learning": cross_agent_analytics,
                "access_patterns": access_analytics,
                "consciousness_evolution": evolution_analytics,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("✅ Generated consciousness memory analytics")
            
            return combined_analytics
            
        except Exception as e:
            logger.error(f"❌ Failed to get consciousness memory analytics: {e}")
            return {"error": str(e)}
    
    async def _calculate_importance_score(
        self,
        content: str,
        consciousness_context: Dict[str, Any],
        emotional_context: Dict[str, Any],
        agent_context: Dict[str, Any]
    ) -> float:
        """Calculate importance score for memory"""
        
        importance = 0.5  # Base importance
        
        # Adjust based on consciousness level
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        importance += consciousness_level * 0.3
        
        # Adjust based on emotional intensity
        emotional_intensity = emotional_context.get("intensity", 0.5)
        importance += emotional_intensity * 0.2
        
        # Adjust based on agent context
        if agent_context.get("critical_task", False):
            importance += 0.2
        
        if agent_context.get("user_interaction", False):
            importance += 0.1
        
        # Adjust based on content length and complexity
        content_length = len(content)
        if content_length > 500:
            importance += 0.1
        elif content_length < 100:
            importance -= 0.1
        
        return min(max(importance, 0.0), 1.0)
    
    async def _generate_memory_embedding(
        self,
        content: str,
        consciousness_context: Dict[str, Any]
    ) -> List[float]:
        """Generate embedding for memory with consciousness context"""
        
        # Combine content with consciousness context for embedding
        enhanced_content = f"{content} [CONSCIOUSNESS: {consciousness_context.get('consciousness_level', 0.7):.2f}]"
        
        # Generate embedding
        embedding = self.embedding_manager.get_embedding(enhanced_content)
        
        return embedding
    
    async def _calculate_cross_agent_relevance(
        self,
        content: str,
        memory_type: str,
        agent_context: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate relevance to different agents"""
        
        relevance = {}
        
        # Base relevance for all agents
        all_agents = [
            "router", "graphmaster", "taskmaster", "codeweaver", "rag",
            "conductor", "research", "cloud", "calendar", "notification",
            "self_reflection", "emotional_processing", "meta_cognitive",
            "consciousness_evolution", "self_modification"
        ]
        
        for agent in all_agents:
            relevance[agent] = 0.3  # Base relevance
        
        # Adjust based on memory type
        if memory_type == "knowledge_graph":
            relevance["graphmaster"] += 0.4
            relevance["rag"] += 0.3
            relevance["research"] += 0.2
        elif memory_type == "task_management":
            relevance["taskmaster"] += 0.4
            relevance["conductor"] += 0.3
            relevance["calendar"] += 0.2
        elif memory_type == "code_analysis":
            relevance["codeweaver"] += 0.4
            relevance["graphmaster"] += 0.2
        elif memory_type == "consciousness":
            relevance["self_reflection"] += 0.4
            relevance["meta_cognitive"] += 0.3
            relevance["consciousness_evolution"] += 0.3
        elif memory_type == "emotional":
            relevance["emotional_processing"] += 0.4
            relevance["self_reflection"] += 0.2
        
        # Adjust based on agent context
        if agent_context.get("source_agent"):
            source_agent = agent_context["source_agent"]
            if source_agent in relevance:
                relevance[source_agent] += 0.2
        
        # Normalize relevance scores
        for agent in relevance:
            relevance[agent] = min(relevance[agent], 1.0)
        
        return relevance
    
    async def _store_consciousness_memory_in_neo4j(
        self,
        memory: ConsciousnessMemory,
        user_id: str
    ):
        """Store consciousness memory in Neo4j"""
        
        query = """
        CREATE (m:ConsciousnessMemory {
            memory_id: $memory_id,
            content: $content,
            memory_type: $memory_type,
            consciousness_level: $consciousness_level,
            consciousness_context: $consciousness_context,
            emotional_context: $emotional_context,
            agent_context: $agent_context,
            importance_score: $importance_score,
            access_count: $access_count,
            last_accessed: $last_accessed,
            created_at: $created_at,
            embedding: $embedding,
            cross_agent_relevance: $cross_agent_relevance,
            evolution_history: $evolution_history,
            user_id: $user_id
        })
        """
        
        params = {
            "memory_id": memory.memory_id,
            "content": memory.content,
            "memory_type": memory.memory_type,
            "consciousness_level": memory.consciousness_level,
            "consciousness_context": json.dumps(memory.consciousness_context),
            "emotional_context": json.dumps(memory.emotional_context),
            "agent_context": json.dumps(memory.agent_context),
            "importance_score": memory.importance_score,
            "access_count": memory.access_count,
            "last_accessed": memory.last_accessed.isoformat(),
            "created_at": memory.created_at.isoformat(),
            "embedding": json.dumps(memory.embedding),
            "cross_agent_relevance": json.dumps(memory.cross_agent_relevance),
            "evolution_history": json.dumps(memory.evolution_history),
            "user_id": user_id
        }
        
        self.neo4j.execute_write_query(query, params)
    
    def _build_consciousness_aware_query(
        self,
        query: str,
        consciousness_level: float,
        memory_type: Optional[str],
        limit: int
    ) -> str:
        """Build consciousness-aware Cypher query"""
        
        cypher_query = """
        MATCH (m:ConsciousnessMemory)
        WHERE m.user_id = $user_id
        AND m.consciousness_level >= $consciousness_level - $consciousness_threshold
        AND m.consciousness_level <= $consciousness_level + $consciousness_threshold
        """
        
        if memory_type:
            cypher_query += " AND m.memory_type = $memory_type"
        
        cypher_query += """
        RETURN m
        ORDER BY m.importance_score DESC, m.consciousness_level DESC
        LIMIT $limit
        """
        
        return cypher_query
    
    async def _enhance_memories_with_cross_agent_learning(
        self,
        memories: List[ConsciousnessMemory],
        agent_name: str,
        consciousness_context: Dict[str, Any]
    ) -> List[ConsciousnessMemory]:
        """Enhance memories with cross-agent learning insights"""
        
        enhanced_memories = []
        
        for memory in memories:
            # Check if memory is relevant to this agent
            if agent_name in memory.cross_agent_relevance:
                relevance_score = memory.cross_agent_relevance[agent_name]
                
                if relevance_score > self.cross_agent_relevance_threshold:
                    # Get relevant experiences from cross-agent learning
                    relevant_experiences = await self.cross_agent_learning.get_relevant_experiences(
                        agent_name, memory.agent_context, consciousness_context, limit=3
                    )
                    
                    # Enhance memory with cross-agent insights
                    if relevant_experiences:
                        memory.agent_context["cross_agent_insights"] = [
                            exp.learning_insights for exp in relevant_experiences
                        ]
                        memory.agent_context["cross_agent_relevance_score"] = relevance_score
            
            enhanced_memories.append(memory)
        
        return enhanced_memories
    
    async def _update_memory_access(self, memory: ConsciousnessMemory):
        """Update memory access patterns"""
        
        memory.access_count += 1
        memory.last_accessed = datetime.now()
        
        # Update access patterns
        self.access_patterns[memory.memory_type].append(datetime.now())
        self.consciousness_patterns[memory.consciousness_level].append(datetime.now())
        
        # Update in Neo4j
        query = """
        MATCH (m:ConsciousnessMemory {memory_id: $memory_id})
        SET m.access_count = $access_count,
            m.last_accessed = $last_accessed
        """
        
        params = {
            "memory_id": memory.memory_id,
            "access_count": memory.access_count,
            "last_accessed": memory.last_accessed.isoformat()
        }
        
        self.neo4j.execute_write_query(query, params)
    
    async def _get_memory_by_id(self, memory_id: str) -> Optional[ConsciousnessMemory]:
        """Get memory by ID"""
        
        # Check cache first
        if memory_id in self.memory_cache:
            return self.memory_cache[memory_id]
        
        # Query Neo4j
        query = """
        MATCH (m:ConsciousnessMemory {memory_id: $memory_id})
        RETURN m
        """
        
        results = self.neo4j.execute_query(query, {"memory_id": memory_id}, use_cache=True)
        
        if results:
            memory_data = results[0]["m"]
            memory = self._neo4j_to_consciousness_memory(memory_data)
            self.memory_cache[memory_id] = memory
            return memory
        
        return None
    
    def _neo4j_to_consciousness_memory(self, data: Dict[str, Any]) -> ConsciousnessMemory:
        """Convert Neo4j data to ConsciousnessMemory object"""
        
        return ConsciousnessMemory(
            memory_id=data["memory_id"],
            content=data["content"],
            memory_type=data["memory_type"],
            consciousness_level=data["consciousness_level"],
            consciousness_context=json.loads(data["consciousness_context"]),
            emotional_context=json.loads(data["emotional_context"]),
            agent_context=json.loads(data["agent_context"]),
            importance_score=data["importance_score"],
            access_count=data["access_count"],
            last_accessed=datetime.fromisoformat(data["last_accessed"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            embedding=json.loads(data["embedding"]),
            cross_agent_relevance=json.loads(data["cross_agent_relevance"]),
            evolution_history=json.loads(data["evolution_history"])
        )
    
    async def _update_access_patterns(self, memory: ConsciousnessMemory):
        """Update access patterns for memory"""
        
        self.access_patterns[memory.memory_type].append(datetime.now())
        self.consciousness_patterns[memory.consciousness_level].append(datetime.now())
    
    async def _share_memory_with_cross_agent_learning(self, memory: ConsciousnessMemory):
        """Share memory with cross-agent learning system"""
        
        # Create experience from memory
        experience_type = "learning" if memory.importance_score > 0.7 else "insight"
        
        await self.cross_agent_learning.share_agent_experience(
            agent_name=memory.agent_context.get("source_agent", "unknown"),
            experience_type=experience_type,
            context=memory.agent_context,
            outcome={"memory_content": memory.content, "importance": memory.importance_score},
            consciousness_context=memory.consciousness_context
        )
    
    async def _recalculate_importance_with_consciousness(
        self,
        memory: ConsciousnessMemory,
        new_consciousness: float,
        evolution_context: Dict[str, Any]
    ) -> float:
        """Recalculate importance score with new consciousness level"""
        
        # Base importance from original calculation
        base_importance = memory.importance_score
        
        # Adjust based on consciousness change
        consciousness_change = new_consciousness - memory.consciousness_level
        importance_adjustment = consciousness_change * 0.2
        
        # Adjust based on evolution context
        if evolution_context.get("significant_learning", False):
            importance_adjustment += 0.1
        
        if evolution_context.get("cross_agent_impact", False):
            importance_adjustment += 0.1
        
        new_importance = base_importance + importance_adjustment
        
        return min(max(new_importance, 0.0), 1.0)
    
    async def _update_cross_agent_relevance_with_consciousness(
        self,
        memory: ConsciousnessMemory,
        new_consciousness: float,
        evolution_context: Dict[str, Any]
    ) -> Dict[str, float]:
        """Update cross-agent relevance with new consciousness level"""
        
        updated_relevance = memory.cross_agent_relevance.copy()
        
        # Adjust relevance based on consciousness change
        consciousness_change = new_consciousness - memory.consciousness_level
        
        for agent in updated_relevance:
            # Higher consciousness memories are more relevant to advanced agents
            if agent in ["meta_cognitive", "consciousness_evolution", "self_modification"]:
                updated_relevance[agent] += consciousness_change * 0.1
            
            # Ensure relevance stays within bounds
            updated_relevance[agent] = min(max(updated_relevance[agent], 0.0), 1.0)
        
        return updated_relevance
    
    async def _update_memory_in_neo4j(self, memory: ConsciousnessMemory):
        """Update memory in Neo4j"""
        
        query = """
        MATCH (m:ConsciousnessMemory {memory_id: $memory_id})
        SET m.consciousness_level = $consciousness_level,
            m.consciousness_context = $consciousness_context,
            m.importance_score = $importance_score,
            m.cross_agent_relevance = $cross_agent_relevance,
            m.evolution_history = $evolution_history
        """
        
        params = {
            "memory_id": memory.memory_id,
            "consciousness_level": memory.consciousness_level,
            "consciousness_context": json.dumps(memory.consciousness_context),
            "importance_score": memory.importance_score,
            "cross_agent_relevance": json.dumps(memory.cross_agent_relevance),
            "evolution_history": json.dumps(memory.evolution_history)
        }
        
        self.neo4j.execute_write_query(query, params)
    
    async def _analyze_access_patterns(self) -> Dict[str, Any]:
        """Analyze memory access patterns"""
        
        patterns = {}
        
        for memory_type, timestamps in self.access_patterns.items():
            if timestamps:
                patterns[memory_type] = {
                    "access_count": len(timestamps),
                    "last_access": max(timestamps).isoformat(),
                    "access_frequency": len(timestamps) / max(1, (max(timestamps) - min(timestamps)).days)
                }
        
        return patterns
    
    async def _analyze_consciousness_evolution(self) -> Dict[str, Any]:
        """Analyze consciousness evolution patterns"""
        
        evolution_stats = {}
        
        for consciousness_level, timestamps in self.consciousness_patterns.items():
            if timestamps:
                evolution_stats[f"level_{consciousness_level:.1f}"] = {
                    "memory_count": len(timestamps),
                    "latest_memory": max(timestamps).isoformat()
                }
        
        return evolution_stats

# Global instance
unified_consciousness_memory = UnifiedConsciousnessMemory()
