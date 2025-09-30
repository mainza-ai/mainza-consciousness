"""
Optimized Agent Memory System for Mainza AI
Implements advanced agent memory interactions and cross-agent learning
"""

import asyncio
import logging
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from neo4j import GraphDatabase
from collections import defaultdict, deque
import hashlib

logger = logging.getLogger(__name__)

class MemoryType(Enum):
    """Types of agent memories"""
    EPISODIC = "episodic"  # Specific events and experiences
    SEMANTIC = "semantic"  # Facts and knowledge
    PROCEDURAL = "procedural"  # Skills and procedures
    EMOTIONAL = "emotional"  # Emotional associations
    CROSS_AGENT = "cross_agent"  # Shared knowledge between agents

class MemoryImportance(Enum):
    """Importance levels for memories"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    TRIVIAL = "trivial"

@dataclass
class AgentMemory:
    """Represents an agent's memory with metadata"""
    id: str
    agent_id: str
    content: str
    memory_type: MemoryType
    importance: MemoryImportance
    embedding: List[float]
    created_at: datetime
    last_accessed: datetime
    access_count: int
    emotional_context: Dict[str, float]
    associated_agents: List[str] = field(default_factory=list)
    cross_agent_connections: List[str] = field(default_factory=list)
    consolidation_score: float = 0.0
    retrieval_strength: float = 1.0

@dataclass
class CrossAgentLearning:
    """Represents cross-agent learning event"""
    id: str
    source_agent: str
    target_agent: str
    knowledge_transferred: str
    transfer_type: str
    success_rate: float
    created_at: datetime
    embedding: List[float]

class OptimizedAgentMemorySystem:
    """
    Advanced agent memory system with cross-agent learning capabilities
    """
    
    def __init__(self, neo4j_driver, config: Dict[str, Any]):
        self.driver = neo4j_driver
        self.config = config
        self.agent_memories = defaultdict(list)
        self.cross_agent_learning = []
        self.memory_consolidation_queue = deque()
        self.learning_patterns = defaultdict(list)
        self.performance_metrics = {
            "total_memories": 0,
            "cross_agent_transfers": 0,
            "consolidation_events": 0,
            "retrieval_success_rate": 0.0,
            "learning_efficiency": 0.0
        }
        
        # Configuration parameters
        self.consolidation_threshold = config.get("consolidation_threshold", 0.8)
        self.learning_threshold = config.get("learning_threshold", 0.7)
        self.memory_decay_rate = config.get("memory_decay_rate", 0.1)
        self.cross_agent_similarity_threshold = config.get("cross_agent_similarity_threshold", 0.75)
        
    async def store_agent_memory(self, agent_id: str, content: str, 
                                memory_type: MemoryType, importance: MemoryImportance,
                                embedding: List[float], emotional_context: Dict[str, float] = None) -> str:
        """
        Store a new memory for an agent with optimization
        """
        try:
            memory_id = f"memory_{agent_id}_{datetime.now().timestamp()}"
            
            # Create memory object
            memory = AgentMemory(
                id=memory_id,
                agent_id=agent_id,
                content=content,
                memory_type=memory_type,
                importance=importance,
                embedding=embedding,
                created_at=datetime.now(),
                last_accessed=datetime.now(),
                access_count=1,
                emotional_context=emotional_context or {},
                consolidation_score=self._calculate_initial_consolidation_score(importance),
                retrieval_strength=1.0
            )
            
            # Store in database
            await self._store_memory_in_db(memory)
            
            # Add to agent's memory list
            self.agent_memories[agent_id].append(memory)
            
            # Check for cross-agent learning opportunities
            await self._check_cross_agent_learning_opportunities(memory)
            
            # Update performance metrics
            self.performance_metrics["total_memories"] += 1
            
            logger.info(f"Stored memory {memory_id} for agent {agent_id}")
            return memory_id
            
        except Exception as e:
            logger.error(f"Error storing agent memory: {e}")
            raise
    
    async def retrieve_agent_memories(self, agent_id: str, query: str, 
                                     memory_types: List[MemoryType] = None,
                                     limit: int = 10) -> List[AgentMemory]:
        """
        Retrieve relevant memories for an agent with optimization
        """
        try:
            # Get agent's memories
            agent_memories = self.agent_memories.get(agent_id, [])
            
            if not agent_memories:
                return []
            
            # Filter by memory types if specified
            if memory_types:
                agent_memories = [
                    m for m in agent_memories 
                    if m.memory_type in memory_types
                ]
            
            # Calculate relevance scores
            relevance_scores = await self._calculate_relevance_scores(
                agent_memories, query
            )
            
            # Sort by relevance and retrieval strength
            scored_memories = [
                (memory, score) for memory, score in zip(agent_memories, relevance_scores)
            ]
            scored_memories.sort(key=lambda x: x[1] * x[0].retrieval_strength, reverse=True)
            
            # Update access patterns
            retrieved_memories = [memory for memory, _ in scored_memories[:limit]]
            await self._update_access_patterns(retrieved_memories)
            
            # Update performance metrics
            self._update_retrieval_metrics(len(retrieved_memories), len(agent_memories))
            
            return retrieved_memories
            
        except Exception as e:
            logger.error(f"Error retrieving agent memories: {e}")
            return []
    
    async def cross_agent_knowledge_transfer(self, source_agent: str, target_agent: str, 
                                           knowledge: str, transfer_type: str = "semantic") -> bool:
        """
        Transfer knowledge between agents with optimization
        """
        try:
            # Check if transfer is beneficial
            if not await self._is_transfer_beneficial(source_agent, target_agent, knowledge):
                return False
            
            # Create cross-agent learning record
            learning_id = f"learning_{source_agent}_{target_agent}_{datetime.now().timestamp()}"
            
            # Generate embedding for the knowledge
            knowledge_embedding = await self._generate_knowledge_embedding(knowledge)
            
            # Create cross-agent learning object
            cross_learning = CrossAgentLearning(
                id=learning_id,
                source_agent=source_agent,
                target_agent=target_agent,
                knowledge_transferred=knowledge,
                transfer_type=transfer_type,
                success_rate=0.0,  # Will be updated based on usage
                created_at=datetime.now(),
                embedding=knowledge_embedding
            )
            
            # Store in database
            await self._store_cross_agent_learning(cross_learning)
            
            # Create memory for target agent
            await self.store_agent_memory(
                agent_id=target_agent,
                content=f"[Transferred from {source_agent}] {knowledge}",
                memory_type=MemoryType.CROSS_AGENT,
                importance=MemoryImportance.MEDIUM,
                embedding=knowledge_embedding,
                emotional_context={"transfer_confidence": 0.8}
            )
            
            # Update learning patterns
            self.learning_patterns[f"{source_agent}->{target_agent}"].append(cross_learning)
            
            # Update performance metrics
            self.performance_metrics["cross_agent_transfers"] += 1
            
            logger.info(f"Knowledge transferred from {source_agent} to {target_agent}")
            return True
            
        except Exception as e:
            logger.error(f"Error in cross-agent knowledge transfer: {e}")
            return False
    
    async def consolidate_agent_memories(self, agent_id: str) -> Dict[str, Any]:
        """
        Consolidate agent memories for optimization
        """
        try:
            logger.info(f"Starting memory consolidation for agent {agent_id}")
            
            agent_memories = self.agent_memories.get(agent_id, [])
            if not agent_memories:
                return {"consolidated": 0, "eliminated": 0}
            
            # Group memories by type and importance
            memory_groups = self._group_memories_for_consolidation(agent_memories)
            
            consolidated_memories = []
            eliminated_count = 0
            
            for group_type, memories in memory_groups.items():
                if len(memories) > 1:
                    # Consolidate similar memories
                    consolidated_group = await self._consolidate_memory_group(memories)
                    consolidated_memories.extend(consolidated_group)
                    eliminated_count += len(memories) - len(consolidated_group)
                else:
                    consolidated_memories.extend(memories)
            
            # Update agent's memory list
            self.agent_memories[agent_id] = consolidated_memories
            
            # Update database
            await self._update_consolidated_memories(agent_id, consolidated_memories)
            
            # Update performance metrics
            self.performance_metrics["consolidation_events"] += 1
            
            result = {
                "consolidated": len(consolidated_memories),
                "eliminated": eliminated_count,
                "consolidation_ratio": eliminated_count / len(agent_memories) if agent_memories else 0
            }
            
            logger.info(f"Memory consolidation completed for agent {agent_id}: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error consolidating agent memories: {e}")
            return {"error": str(e)}
    
    async def optimize_memory_retrieval(self, agent_id: str) -> Dict[str, Any]:
        """
        Optimize memory retrieval patterns for an agent
        """
        try:
            agent_memories = self.agent_memories.get(agent_id, [])
            if not agent_memories:
                return {"optimized": 0}
            
            # Analyze retrieval patterns
            retrieval_patterns = await self._analyze_retrieval_patterns(agent_id)
            
            # Optimize memory organization
            optimized_memories = await self._optimize_memory_organization(
                agent_memories, retrieval_patterns
            )
            
            # Update retrieval strengths based on usage
            await self._update_retrieval_strengths(optimized_memories)
            
            # Update agent's memory list
            self.agent_memories[agent_id] = optimized_memories
            
            # Update database
            await self._update_optimized_memories(agent_id, optimized_memories)
            
            return {
                "optimized": len(optimized_memories),
                "retrieval_patterns_analyzed": len(retrieval_patterns),
                "optimization_successful": True
            }
            
        except Exception as e:
            logger.error(f"Error optimizing memory retrieval: {e}")
            return {"error": str(e)}
    
    async def learn_from_cross_agent_interactions(self) -> Dict[str, Any]:
        """
        Learn patterns from cross-agent interactions
        """
        try:
            logger.info("Analyzing cross-agent learning patterns...")
            
            # Analyze successful transfers
            successful_transfers = [
                learning for learning in self.cross_agent_learning
                if learning.success_rate > self.learning_threshold
            ]
            
            # Identify learning patterns
            patterns = await self._identify_learning_patterns(successful_transfers)
            
            # Update learning efficiency
            learning_efficiency = len(successful_transfers) / len(self.cross_agent_learning) if self.cross_agent_learning else 0
            self.performance_metrics["learning_efficiency"] = learning_efficiency
            
            # Generate recommendations
            recommendations = await self._generate_learning_recommendations(patterns)
            
            result = {
                "patterns_identified": len(patterns),
                "learning_efficiency": learning_efficiency,
                "successful_transfers": len(successful_transfers),
                "recommendations": recommendations
            }
            
            logger.info(f"Cross-agent learning analysis completed: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error learning from cross-agent interactions: {e}")
            return {"error": str(e)}
    
    def _calculate_initial_consolidation_score(self, importance: MemoryImportance) -> float:
        """Calculate initial consolidation score based on importance"""
        importance_scores = {
            MemoryImportance.CRITICAL: 1.0,
            MemoryImportance.HIGH: 0.8,
            MemoryImportance.MEDIUM: 0.6,
            MemoryImportance.LOW: 0.4,
            MemoryImportance.TRIVIAL: 0.2
        }
        return importance_scores.get(importance, 0.5)
    
    async def _calculate_relevance_scores(self, memories: List[AgentMemory], 
                                        query: str) -> List[float]:
        """Calculate relevance scores for memories based on query"""
        try:
            # Generate query embedding
            query_embedding = await self._generate_query_embedding(query)
            
            relevance_scores = []
            for memory in memories:
                # Calculate cosine similarity
                similarity = self._calculate_cosine_similarity(
                    query_embedding, memory.embedding
                )
                
                # Factor in memory importance and access patterns
                importance_factor = self._get_importance_factor(memory.importance)
                access_factor = min(memory.access_count / 10, 1.0)  # Cap at 1.0
                
                # Combined relevance score
                relevance_score = (
                    similarity * 0.5 +
                    importance_factor * 0.3 +
                    access_factor * 0.2
                )
                
                relevance_scores.append(relevance_score)
            
            return relevance_scores
            
        except Exception as e:
            logger.error(f"Error calculating relevance scores: {e}")
            return [0.0] * len(memories)
    
    def _calculate_cosine_similarity(self, embedding1: List[float], 
                                   embedding2: List[float]) -> float:
        """Calculate cosine similarity between embeddings"""
        try:
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
            
        except Exception as e:
            logger.error(f"Error calculating cosine similarity: {e}")
            return 0.0
    
    def _get_importance_factor(self, importance: MemoryImportance) -> float:
        """Get importance factor for scoring"""
        importance_factors = {
            MemoryImportance.CRITICAL: 1.0,
            MemoryImportance.HIGH: 0.8,
            MemoryImportance.MEDIUM: 0.6,
            MemoryImportance.LOW: 0.4,
            MemoryImportance.TRIVIAL: 0.2
        }
        return importance_factors.get(importance, 0.5)
    
    async def _update_access_patterns(self, memories: List[AgentMemory]):
        """Update access patterns for retrieved memories"""
        try:
            current_time = datetime.now()
            
            for memory in memories:
                memory.last_accessed = current_time
                memory.access_count += 1
                
                # Update retrieval strength based on access
                memory.retrieval_strength = min(
                    memory.retrieval_strength + 0.1, 1.0
                )
            
        except Exception as e:
            logger.error(f"Error updating access patterns: {e}")
    
    def _update_retrieval_metrics(self, retrieved_count: int, total_count: int):
        """Update retrieval performance metrics"""
        try:
            if total_count > 0:
                success_rate = retrieved_count / total_count
                # Update running average
                current_avg = self.performance_metrics["retrieval_success_rate"]
                total_retrievals = self.performance_metrics.get("total_retrievals", 0) + 1
                
                self.performance_metrics["retrieval_success_rate"] = (
                    (current_avg * (total_retrievals - 1) + success_rate) / total_retrievals
                )
                self.performance_metrics["total_retrievals"] = total_retrievals
            
        except Exception as e:
            logger.error(f"Error updating retrieval metrics: {e}")
    
    async def _check_cross_agent_learning_opportunities(self, memory: AgentMemory):
        """Check for cross-agent learning opportunities"""
        try:
            # Find other agents with similar memories
            for other_agent_id, other_memories in self.agent_memories.items():
                if other_agent_id == memory.agent_id:
                    continue
                
                for other_memory in other_memories:
                    # Calculate similarity
                    similarity = self._calculate_cosine_similarity(
                        memory.embedding, other_memory.embedding
                    )
                    
                    if similarity > self.cross_agent_similarity_threshold:
                        # Found similar memory in another agent
                        await self._suggest_cross_agent_learning(
                            memory, other_memory, other_agent_id
                        )
            
        except Exception as e:
            logger.error(f"Error checking cross-agent learning opportunities: {e}")
    
    async def _suggest_cross_agent_learning(self, memory1: AgentMemory, 
                                          memory2: AgentMemory, other_agent_id: str):
        """Suggest cross-agent learning between similar memories"""
        try:
            # Create learning suggestion
            suggestion = {
                "source_agent": memory1.agent_id,
                "target_agent": other_agent_id,
                "similarity": self._calculate_cosine_similarity(
                    memory1.embedding, memory2.embedding
                ),
                "suggested_knowledge": memory1.content,
                "timestamp": datetime.now()
            }
            
            # Store suggestion for later processing
            await self._store_learning_suggestion(suggestion)
            
        except Exception as e:
            logger.error(f"Error suggesting cross-agent learning: {e}")
    
    def _group_memories_for_consolidation(self, memories: List[AgentMemory]) -> Dict[str, List[AgentMemory]]:
        """Group memories for consolidation based on type and importance"""
        try:
            groups = defaultdict(list)
            
            for memory in memories:
                # Group by memory type and importance
                group_key = f"{memory.memory_type.value}_{memory.importance.value}"
                groups[group_key].append(memory)
            
            return dict(groups)
            
        except Exception as e:
            logger.error(f"Error grouping memories for consolidation: {e}")
            return {"default": memories}
    
    async def _consolidate_memory_group(self, memories: List[AgentMemory]) -> List[AgentMemory]:
        """Consolidate a group of similar memories"""
        try:
            if len(memories) <= 1:
                return memories
            
            # Find the most important memory as base
            base_memory = max(memories, key=lambda m: (
                m.importance.value, m.access_count, m.consolidation_score
            ))
            
            # Merge other memories into base memory
            consolidated_content = base_memory.content
            total_access_count = base_memory.access_count
            max_importance = base_memory.importance
            
            for memory in memories:
                if memory.id != base_memory.id:
                    # Merge content
                    consolidated_content += f" | {memory.content}"
                    total_access_count += memory.access_count
                    
                    # Update importance if higher
                    if memory.importance.value > max_importance.value:
                        max_importance = memory.importance
            
            # Update base memory
            base_memory.content = consolidated_content
            base_memory.access_count = total_access_count
            base_memory.importance = max_importance
            base_memory.consolidation_score = 1.0
            
            return [base_memory]
            
        except Exception as e:
            logger.error(f"Error consolidating memory group: {e}")
            return memories
    
    async def _analyze_retrieval_patterns(self, agent_id: str) -> List[Dict[str, Any]]:
        """Analyze retrieval patterns for an agent"""
        try:
            # This would analyze historical retrieval data
            # For now, return basic patterns
            patterns = [
                {
                    "pattern_type": "frequency",
                    "description": "Most accessed memories",
                    "memories": sorted(
                        self.agent_memories[agent_id],
                        key=lambda m: m.access_count,
                        reverse=True
                    )[:5]
                },
                {
                    "pattern_type": "recency",
                    "description": "Recently accessed memories",
                    "memories": sorted(
                        self.agent_memories[agent_id],
                        key=lambda m: m.last_accessed,
                        reverse=True
                    )[:5]
                }
            ]
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing retrieval patterns: {e}")
            return []
    
    async def _optimize_memory_organization(self, memories: List[AgentMemory], 
                                          patterns: List[Dict[str, Any]]) -> List[AgentMemory]:
        """Optimize memory organization based on patterns"""
        try:
            # Reorganize memories based on access patterns
            optimized_memories = memories.copy()
            
            # Sort by combined score (importance + access + recency)
            for memory in optimized_memories:
                recency_score = (datetime.now() - memory.last_accessed).total_seconds() / 86400  # Days
                memory.retrieval_strength = (
                    self._get_importance_factor(memory.importance) * 0.4 +
                    min(memory.access_count / 10, 1.0) * 0.4 +
                    max(0, 1 - recency_score) * 0.2
                )
            
            # Sort by retrieval strength
            optimized_memories.sort(key=lambda m: m.retrieval_strength, reverse=True)
            
            return optimized_memories
            
        except Exception as e:
            logger.error(f"Error optimizing memory organization: {e}")
            return memories
    
    async def _update_retrieval_strengths(self, memories: List[AgentMemory]):
        """Update retrieval strengths based on usage patterns"""
        try:
            for memory in memories:
                # Decay unused memories
                time_since_access = (datetime.now() - memory.last_accessed).total_seconds()
                decay_factor = max(0, 1 - (time_since_access / 86400) * self.memory_decay_rate)
                
                memory.retrieval_strength *= decay_factor
                memory.retrieval_strength = max(0.1, memory.retrieval_strength)  # Minimum strength
            
        except Exception as e:
            logger.error(f"Error updating retrieval strengths: {e}")
    
    async def _generate_knowledge_embedding(self, knowledge: str) -> List[float]:
        """Generate embedding for knowledge (placeholder)"""
        # In a real implementation, this would use an embedding model
        # For now, return a simple hash-based embedding
        hash_value = hashlib.md5(knowledge.encode()).hexdigest()
        embedding = [float(int(hash_value[i:i+2], 16)) / 255.0 for i in range(0, len(hash_value), 2)]
        return embedding[:128]  # 128-dimensional embedding
    
    async def _generate_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for query (placeholder)"""
        # Similar to knowledge embedding
        hash_value = hashlib.md5(query.encode()).hexdigest()
        embedding = [float(int(hash_value[i:i+2], 16)) / 255.0 for i in range(0, len(hash_value), 2)]
        return embedding[:128]
    
    async def _is_transfer_beneficial(self, source_agent: str, target_agent: str, 
                                    knowledge: str) -> bool:
        """Check if knowledge transfer would be beneficial"""
        try:
            # Check if target agent already has similar knowledge
            target_memories = self.agent_memories.get(target_agent, [])
            
            if not target_memories:
                return True  # No existing memories, transfer is beneficial
            
            # Generate knowledge embedding
            knowledge_embedding = await self._generate_knowledge_embedding(knowledge)
            
            # Check similarity with existing memories
            for memory in target_memories:
                similarity = self._calculate_cosine_similarity(
                    knowledge_embedding, memory.embedding
                )
                if similarity > 0.8:  # Very similar knowledge already exists
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking transfer benefit: {e}")
            return False
    
    async def _store_memory_in_db(self, memory: AgentMemory):
        """Store memory in Neo4j database"""
        try:
            with self.driver.session() as session:
                query = """
                CREATE (m:AgentMemory {
                    id: $id,
                    agent_id: $agent_id,
                    content: $content,
                    memory_type: $memory_type,
                    importance: $importance,
                    embedding: $embedding,
                    created_at: $created_at,
                    last_accessed: $last_accessed,
                    access_count: $access_count,
                    emotional_context: $emotional_context,
                    consolidation_score: $consolidation_score,
                    retrieval_strength: $retrieval_strength
                })
                """
                
                await session.run(query, {
                    "id": memory.id,
                    "agent_id": memory.agent_id,
                    "content": memory.content,
                    "memory_type": memory.memory_type.value,
                    "importance": memory.importance.value,
                    "embedding": memory.embedding,
                    "created_at": memory.created_at.isoformat(),
                    "last_accessed": memory.last_accessed.isoformat(),
                    "access_count": memory.access_count,
                    "emotional_context": json.dumps(memory.emotional_context),
                    "consolidation_score": memory.consolidation_score,
                    "retrieval_strength": memory.retrieval_strength
                })
            
        except Exception as e:
            logger.error(f"Error storing memory in database: {e}")
            raise
    
    async def _store_cross_agent_learning(self, learning: CrossAgentLearning):
        """Store cross-agent learning in database"""
        try:
            with self.driver.session() as session:
                query = """
                CREATE (l:CrossAgentLearning {
                    id: $id,
                    source_agent: $source_agent,
                    target_agent: $target_agent,
                    knowledge_transferred: $knowledge_transferred,
                    transfer_type: $transfer_type,
                    success_rate: $success_rate,
                    created_at: $created_at,
                    embedding: $embedding
                })
                """
                
                await session.run(query, {
                    "id": learning.id,
                    "source_agent": learning.source_agent,
                    "target_agent": learning.target_agent,
                    "knowledge_transferred": learning.knowledge_transferred,
                    "transfer_type": learning.transfer_type,
                    "success_rate": learning.success_rate,
                    "created_at": learning.created_at.isoformat(),
                    "embedding": learning.embedding
                })
            
            # Add to local list
            self.cross_agent_learning.append(learning)
            
        except Exception as e:
            logger.error(f"Error storing cross-agent learning: {e}")
            raise
    
    async def _update_consolidated_memories(self, agent_id: str, memories: List[AgentMemory]):
        """Update consolidated memories in database"""
        try:
            with self.driver.session() as session:
                # Delete old memories for this agent
                await session.run(
                    "MATCH (m:AgentMemory {agent_id: $agent_id}) DELETE m",
                    agent_id=agent_id
                )
                
                # Insert consolidated memories
                for memory in memories:
                    await self._store_memory_in_db(memory)
            
        except Exception as e:
            logger.error(f"Error updating consolidated memories: {e}")
            raise
    
    async def _update_optimized_memories(self, agent_id: str, memories: List[AgentMemory]):
        """Update optimized memories in database"""
        try:
            with self.driver.session() as session:
                for memory in memories:
                    query = """
                    MATCH (m:AgentMemory {id: $id})
                    SET m.retrieval_strength = $retrieval_strength,
                        m.last_accessed = $last_accessed,
                        m.access_count = $access_count
                    """
                    
                    await session.run(query, {
                        "id": memory.id,
                        "retrieval_strength": memory.retrieval_strength,
                        "last_accessed": memory.last_accessed.isoformat(),
                        "access_count": memory.access_count
                    })
            
        except Exception as e:
            logger.error(f"Error updating optimized memories: {e}")
            raise
    
    async def _identify_learning_patterns(self, successful_transfers: List[CrossAgentLearning]) -> List[Dict[str, Any]]:
        """Identify patterns in successful cross-agent learning"""
        try:
            patterns = []
            
            # Pattern 1: Most successful agent pairs
            agent_pairs = defaultdict(int)
            for transfer in successful_transfers:
                pair = f"{transfer.source_agent}->{transfer.target_agent}"
                agent_pairs[pair] += 1
            
            if agent_pairs:
                patterns.append({
                    "pattern_type": "successful_pairs",
                    "description": "Most successful agent learning pairs",
                    "data": dict(sorted(agent_pairs.items(), key=lambda x: x[1], reverse=True)[:5])
                })
            
            # Pattern 2: Most effective transfer types
            transfer_types = defaultdict(int)
            for transfer in successful_transfers:
                transfer_types[transfer.transfer_type] += 1
            
            if transfer_types:
                patterns.append({
                    "pattern_type": "effective_transfer_types",
                    "description": "Most effective knowledge transfer types",
                    "data": dict(sorted(transfer_types.items(), key=lambda x: x[1], reverse=True))
                })
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error identifying learning patterns: {e}")
            return []
    
    async def _generate_learning_recommendations(self, patterns: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on learning patterns"""
        try:
            recommendations = []
            
            for pattern in patterns:
                if pattern["pattern_type"] == "successful_pairs":
                    top_pair = list(pattern["data"].keys())[0]
                    recommendations.append(
                        f"Encourage more knowledge transfer between {top_pair} "
                        f"(success rate: {pattern['data'][top_pair]})"
                    )
                
                elif pattern["pattern_type"] == "effective_transfer_types":
                    top_type = list(pattern["data"].keys())[0]
                    recommendations.append(
                        f"Prioritize {top_type} transfer methods for better learning outcomes"
                    )
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating learning recommendations: {e}")
            return []
    
    async def _store_learning_suggestion(self, suggestion: Dict[str, Any]):
        """Store learning suggestion for later processing"""
        try:
            # Store in database or queue for processing
            with self.driver.session() as session:
                query = """
                CREATE (s:LearningSuggestion {
                    source_agent: $source_agent,
                    target_agent: $target_agent,
                    similarity: $similarity,
                    suggested_knowledge: $suggested_knowledge,
                    timestamp: $timestamp
                })
                """
                
                await session.run(query, suggestion)
            
        except Exception as e:
            logger.error(f"Error storing learning suggestion: {e}")
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for the agent memory system"""
        return {
            "performance_metrics": self.performance_metrics,
            "total_agents": len(self.agent_memories),
            "total_cross_agent_learning": len(self.cross_agent_learning),
            "consolidation_threshold": self.consolidation_threshold,
            "learning_threshold": self.learning_threshold
        }

    async def optimize_cross_agent_learning(self) -> Dict[str, Any]:
        """Optimize cross-agent learning system"""
        try:
            # Run cross-agent learning optimization
            await self.learn_from_cross_agent_interactions()
            
            # Optimize learning thresholds
            self.learning_threshold = max(0.1, self.learning_threshold - 0.05)
            
            return {
                "optimization_type": "cross_agent_learning",
                "learning_threshold": self.learning_threshold,
                "cross_agent_learning_completed": True,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error optimizing cross-agent learning: {e}")
            return {"status": "error", "message": str(e)}

    async def optimize_agent_memory(self) -> Dict[str, Any]:
        """Optimize agent memory system"""
        try:
            # Run memory consolidation for all agents
            consolidation_results = []
            for agent_id in self.agent_memories.keys():
                result = await self.consolidate_agent_memory(agent_id)
                consolidation_results.append(result)
            
            # Optimize consolidation threshold
            self.consolidation_threshold = max(0.1, self.consolidation_threshold - 0.05)
            
            return {
                "optimization_type": "agent_memory",
                "consolidation_threshold": self.consolidation_threshold,
                "consolidation_results": consolidation_results,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error optimizing agent memory: {e}")
            return {"status": "error", "message": str(e)}
