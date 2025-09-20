"""
Memory Retrieval Engine for Mainza AI
Provides comprehensive memory search and retrieval functionality with multiple search strategies,
consciousness-aware filtering, and relevance scoring.
"""
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple, Union
import json
import math
from dataclasses import dataclass, field

from backend.utils.neo4j_unified import neo4j_unified
from backend.utils.memory_embedding_manager import memory_embedding_manager
from backend.utils.embedding_enhanced import embedding_manager
from backend.core.enhanced_error_handling import ErrorHandler, handle_errors
from backend.utils.memory_error_handling import (
    MemoryRetrievalError, MemoryConnectionError, MemoryTimeoutError,
    handle_memory_errors, memory_error_handler
)

logger = logging.getLogger(__name__)
error_handler = ErrorHandler()

@dataclass
class MemorySearchParams:
    """Parameters for memory search operations"""
    query: str
    user_id: str
    consciousness_context: Dict[str, Any]
    search_type: str = "semantic"  # "semantic", "keyword", "temporal", "hybrid"
    limit: int = 5
    similarity_threshold: float = 0.3
    temporal_weight: float = 0.3
    consciousness_weight: float = 0.4
    importance_weight: float = 0.3
    memory_types: Optional[List[str]] = None
    time_range_hours: Optional[int] = None

@dataclass
class MemorySearchResult:
    """Result from memory search with scoring details"""
    memory_id: str
    content: str
    memory_type: str
    agent_name: str
    user_id: str
    consciousness_level: float
    emotional_state: str
    importance_score: float
    created_at: str
    metadata: Dict[str, Any]
    relevance_score: float
    similarity_score: float = 0.0
    temporal_score: float = 0.0
    consciousness_score: float = 0.0
    importance_factor: float = 0.0

# MemoryRetrievalError is now imported from memory_error_handling

class MemoryRetrievalEngine:
    """
    Advanced memory retrieval engine with multiple search strategies and consciousness awareness
    """
    
    def __init__(self):
        self.neo4j = neo4j_unified
        self.embedding_manager = memory_embedding_manager
        self.embedding = embedding_manager
        
        # Configuration
        self.default_limit = 5
        self.max_limit = 50
        self.min_similarity_threshold = 0.1
        self.max_similarity_threshold = 1.0
        self.temporal_decay_hours = 168  # 1 week
        self.consciousness_tolerance = 0.2  # Tolerance for consciousness level matching
        
        # Search strategy weights
        self.strategy_weights = {
            "semantic": {"similarity": 0.6, "temporal": 0.2, "consciousness": 0.1, "importance": 0.1},
            "keyword": {"similarity": 0.4, "temporal": 0.3, "consciousness": 0.1, "importance": 0.2},
            "temporal": {"similarity": 0.2, "temporal": 0.5, "consciousness": 0.1, "importance": 0.2},
            "hybrid": {"similarity": 0.4, "temporal": 0.3, "consciousness": 0.2, "importance": 0.1},
            "consciousness_aware": {"similarity": 0.3, "temporal": 0.2, "consciousness": 0.4, "importance": 0.1}
        }
    
    async def initialize(self) -> bool:
        """Initialize the memory retrieval engine"""
        try:
            # Test Neo4j connectivity
            test_result = self.neo4j.execute_query("RETURN 1 as test", {})
            if not test_result:
                logger.error("Failed to connect to Neo4j for memory retrieval")
                return False
            
            logger.info("Memory retrieval engine initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize memory retrieval engine: {e}")
            return False
    
    @handle_memory_errors(
        component="memory_retrieval",
        operation="get_relevant_memories",
        fallback_result=[],
        suppress_errors=True,
        timeout_seconds=15.0,
        retry_attempts=2,
        retry_delay=0.5
    )
    async def get_relevant_memories(
        self,
        query: str,
        user_id: str,
        consciousness_context: Dict[str, Any],
        limit: int = 5,
        similarity_threshold: float = 0.3,
        search_type: str = "hybrid",
        memory_types: Optional[List[str]] = None
    ) -> List[MemorySearchResult]:
        """
        Get relevant memories using multi-strategy search approach
        
        Args:
            query: Search query text
            user_id: User identifier to filter memories
            consciousness_context: Current consciousness state context
            limit: Maximum number of results to return
            similarity_threshold: Minimum similarity threshold for results
            search_type: Search strategy ("semantic", "keyword", "temporal", "hybrid")
            memory_types: Optional list of memory types to filter by
            
        Returns:
            List of MemorySearchResult objects ranked by relevance
            
        Raises:
            MemoryRetrievalError: If retrieval fails critically
        """
        try:
            # Validate and sanitize inputs
            limit = max(1, min(limit, self.max_limit))
            similarity_threshold = max(
                self.min_similarity_threshold, 
                min(similarity_threshold, self.max_similarity_threshold)
            )
            
            # Create search parameters
            search_params = MemorySearchParams(
                query=query,
                user_id=user_id,
                consciousness_context=consciousness_context,
                search_type=search_type,
                limit=limit * 2,  # Get more results for better ranking
                similarity_threshold=similarity_threshold,
                memory_types=memory_types
            )
            
            logger.debug(f"🔍 Searching memories: query='{query[:50]}...', user={user_id}, type={search_type}")
            
            # Execute search based on strategy
            if search_type == "semantic":
                memories = await self._semantic_search(search_params)
            elif search_type == "keyword":
                memories = await self._keyword_search(search_params)
            elif search_type == "temporal":
                memories = await self._temporal_search(search_params)
            elif search_type == "hybrid":
                memories = await self._hybrid_search(search_params)
            elif search_type == "consciousness_aware":
                memories = await self.consciousness_aware_search(
                    search_params.query,
                    search_params.user_id,
                    search_params.consciousness_context,
                    search_params.limit
                )
            else:
                logger.warning(f"Unknown search type '{search_type}', falling back to hybrid")
                memories = await self._hybrid_search(search_params)
            
            if not memories:
                logger.info(f"No memories found for query: {query[:50]}...")
                return []
            
            # Calculate comprehensive relevance scores
            scored_memories = await self._calculate_relevance_scores(memories, search_params)
            
            # Sort by relevance score and limit results
            scored_memories.sort(key=lambda x: x.relevance_score, reverse=True)
            final_results = scored_memories[:limit]
            
            # Update access statistics
            await self._update_access_statistics([m.memory_id for m in final_results])
            
            logger.info(f"✅ Retrieved {len(final_results)} relevant memories (from {len(memories)} candidates)")
            return final_results
            
        except Exception as e:
            logger.error(f"❌ Failed to retrieve relevant memories: {e}")
            # Return empty list for graceful degradation
            return []
    
    @handle_memory_errors(
        component="memory_retrieval",
        operation="semantic_memory_search",
        fallback_result=[],
        suppress_errors=True,
        timeout_seconds=10.0,
        retry_attempts=1,
        retry_delay=0.5
    )
    async def semantic_memory_search(
        self,
        query_embedding: List[float],
        user_id: str,
        consciousness_context: Dict[str, Any],
        limit: int = 10,
        min_similarity: float = 0.3
    ) -> List[MemorySearchResult]:
        """
        Perform semantic similarity search using vector embeddings
        
        Args:
            query_embedding: Pre-computed embedding vector for the query
            user_id: User identifier to filter memories
            consciousness_context: Current consciousness state context
            limit: Maximum number of results to return
            min_similarity: Minimum similarity threshold
            
        Returns:
            List of MemorySearchResult objects with similarity scores
        """
        try:
            if not query_embedding or all(x == 0.0 for x in query_embedding):
                logger.warning("Invalid query embedding provided")
                return []
            
            # Use the embedding manager for vector search
            similar_memories = await self.embedding_manager.find_similar_memories(
                query_text="",  # Not used when embedding is provided
                user_id=user_id,
                memory_types=None,
                limit=limit,
                min_similarity=min_similarity
            )
            
            if not similar_memories:
                return []
            
            # Convert to MemorySearchResult objects
            results = []
            for memory in similar_memories:
                result = MemorySearchResult(
                    memory_id=memory["memory_id"],
                    content=memory["content"],
                    memory_type=memory["memory_type"],
                    agent_name=memory["agent_name"],
                    user_id=user_id,
                    consciousness_level=memory["consciousness_level"],
                    emotional_state=memory["emotional_state"],
                    importance_score=memory["importance_score"],
                    created_at=memory["created_at"],
                    metadata=memory.get("metadata", {}),
                    relevance_score=memory.get("similarity_score", 0.0),
                    similarity_score=memory.get("similarity_score", 0.0)
                )
                results.append(result)
            
            logger.debug(f"✅ Semantic search found {len(results)} memories")
            return results
            
        except Exception as e:
            logger.error(f"❌ Semantic memory search failed: {e}")
            return []
    
    @handle_memory_errors(
        component="memory_retrieval",
        operation="get_conversation_history",
        fallback_result=[],
        suppress_errors=True,
        timeout_seconds=10.0,
        retry_attempts=2,
        retry_delay=0.5
    )
    async def get_conversation_history(
        self,
        user_id: str,
        limit: int = 10,
        hours_back: Optional[int] = None,
        agent_name: Optional[str] = None
    ) -> List[MemorySearchResult]:
        """
        Get conversation history for temporal context
        
        Args:
            user_id: User identifier
            limit: Maximum number of conversation memories to return
            hours_back: Optional time limit in hours (default: no limit)
            agent_name: Optional agent name filter
            
        Returns:
            List of conversation memories ordered by recency
        """
        try:
            # Build query with optional filters
            query = """
            MATCH (m:Memory {user_id: $user_id})
            WHERE m.memory_type = 'interaction'
            """
            
            params = {"user_id": user_id, "limit": limit}
            
            # Add time filter if specified
            if hours_back:
                cutoff_time = datetime.now() - timedelta(hours=hours_back)
                query += " AND datetime(m.created_at) >= datetime($cutoff_time)"
                params["cutoff_time"] = cutoff_time.isoformat()
            
            # Add agent filter if specified
            if agent_name:
                query += " AND m.agent_name = $agent_name"
                params["agent_name"] = agent_name
            
            query += """
            RETURN m.memory_id AS memory_id,
                   m.content AS content,
                   m.memory_type AS memory_type,
                   m.agent_name AS agent_name,
                   m.consciousness_level AS consciousness_level,
                   m.emotional_state AS emotional_state,
                   m.importance_score AS importance_score,
                   m.created_at AS created_at,
                   m.metadata AS metadata
            ORDER BY m.created_at DESC
            LIMIT $limit
            """
            
            result = self.neo4j.execute_query(query, params)
            
            # Convert to MemorySearchResult objects
            conversation_history = []
            for record in result:
                # Parse metadata if it's a JSON string
                metadata = record.get("metadata", {})
                if isinstance(metadata, str):
                    try:
                        metadata = json.loads(metadata)
                    except json.JSONDecodeError:
                        metadata = {}
                
                memory_result = MemorySearchResult(
                    memory_id=record["memory_id"],
                    content=record["content"],
                    memory_type=record["memory_type"],
                    agent_name=record["agent_name"],
                    user_id=user_id,
                    consciousness_level=record["consciousness_level"],
                    emotional_state=record["emotional_state"],
                    importance_score=record["importance_score"],
                    created_at=record["created_at"],
                    metadata=metadata,
                    relevance_score=1.0,  # Full relevance for conversation history
                    temporal_score=1.0
                )
                conversation_history.append(memory_result)
            
            logger.debug(f"✅ Retrieved {len(conversation_history)} conversation memories")
            return conversation_history
            
        except Exception as e:
            logger.error(f"❌ Failed to get conversation history: {e}")
            return []
    
    async def _semantic_search(self, params: MemorySearchParams) -> List[Dict[str, Any]]:
        """Perform semantic similarity search"""
        try:
            # Generate embedding for query
            query_embedding = self.embedding.get_embedding(params.query)
            
            if not query_embedding:
                logger.warning("Failed to generate query embedding, falling back to keyword search")
                return await self._keyword_search(params)
            
            # Use embedding manager for vector search
            memories = await self.embedding_manager.find_similar_memories(
                query_text=params.query,
                user_id=params.user_id,
                memory_types=params.memory_types,
                limit=params.limit,
                min_similarity=params.similarity_threshold
            )
            
            return memories
            
        except Exception as e:
            logger.error(f"❌ Semantic search failed: {e}")
            return []
    
    async def _keyword_search(self, params: MemorySearchParams) -> List[Dict[str, Any]]:
        """Perform keyword-based text search"""
        try:
            # Extract keywords from query
            keywords = self._extract_keywords(params.query)
            
            if not keywords:
                logger.warning("No keywords extracted from query")
                return []
            
            # Build keyword search query
            query = """
            MATCH (m:Memory {user_id: $user_id})
            WHERE (
                toLower(m.content) CONTAINS toLower($query)
            """
            
            # Add keyword matching
            for i, keyword in enumerate(keywords[:5]):  # Limit to 5 keywords
                query += f" OR toLower(m.content) CONTAINS toLower($keyword_{i})"
            
            query += ")"
            
            # Add memory type filter if specified
            if params.memory_types:
                query += " AND m.memory_type IN $memory_types"
            
            query += """
            RETURN m.memory_id AS memory_id,
                   m.content AS content,
                   m.memory_type AS memory_type,
                   m.agent_name AS agent_name,
                   m.consciousness_level AS consciousness_level,
                   m.emotional_state AS emotional_state,
                   m.importance_score AS importance_score,
                   m.created_at AS created_at,
                   m.metadata AS metadata,
                   0.6 AS similarity_score
            ORDER BY m.importance_score DESC, m.created_at DESC
            LIMIT $limit
            """
            
            # Prepare parameters
            query_params = {
                "user_id": params.user_id,
                "query": params.query,
                "limit": params.limit
            }
            
            # Add keyword parameters
            for i, keyword in enumerate(keywords[:5]):
                query_params[f"keyword_{i}"] = keyword
            
            if params.memory_types:
                query_params["memory_types"] = params.memory_types
            
            result = self.neo4j.execute_query(query, query_params)
            return [dict(record) for record in result]
            
        except Exception as e:
            logger.error(f"❌ Keyword search failed: {e}")
            return []
    
    async def _temporal_search(self, params: MemorySearchParams) -> List[Dict[str, Any]]:
        """Perform temporal-based search focusing on recent memories"""
        try:
            # Calculate time range
            hours_back = params.time_range_hours or 24  # Default to last 24 hours
            cutoff_time = datetime.now() - timedelta(hours=hours_back)
            
            query = """
            MATCH (m:Memory {user_id: $user_id})
            WHERE datetime(m.created_at) >= datetime($cutoff_time)
            """
            
            # Add memory type filter if specified
            if params.memory_types:
                query += " AND m.memory_type IN $memory_types"
            
            # Add basic text matching if query provided
            if params.query.strip():
                query += " AND toLower(m.content) CONTAINS toLower($query)"
            
            query += """
            RETURN m.memory_id AS memory_id,
                   m.content AS content,
                   m.memory_type AS memory_type,
                   m.agent_name AS agent_name,
                   m.consciousness_level AS consciousness_level,
                   m.emotional_state AS emotional_state,
                   m.importance_score AS importance_score,
                   m.created_at AS created_at,
                   m.metadata AS metadata,
                   0.7 AS similarity_score
            ORDER BY m.created_at DESC, m.importance_score DESC
            LIMIT $limit
            """
            
            query_params = {
                "user_id": params.user_id,
                "cutoff_time": cutoff_time.isoformat(),
                "limit": params.limit
            }
            
            if params.query.strip():
                query_params["query"] = params.query
            
            if params.memory_types:
                query_params["memory_types"] = params.memory_types
            
            result = self.neo4j.execute_query(query, query_params)
            return [dict(record) for record in result]
            
        except Exception as e:
            logger.error(f"❌ Temporal search failed: {e}")
            return []
    
    async def _hybrid_search(self, params: MemorySearchParams) -> List[Dict[str, Any]]:
        """Perform hybrid search combining multiple strategies"""
        try:
            # Run multiple search strategies in parallel
            semantic_task = asyncio.create_task(self._semantic_search(params))
            keyword_task = asyncio.create_task(self._keyword_search(params))
            temporal_task = asyncio.create_task(self._temporal_search(params))
            
            # Wait for all searches to complete
            semantic_results, keyword_results, temporal_results = await asyncio.gather(
                semantic_task, keyword_task, temporal_task, return_exceptions=True
            )
            
            # Handle exceptions
            if isinstance(semantic_results, Exception):
                logger.warning(f"Semantic search failed in hybrid: {semantic_results}")
                semantic_results = []
            
            if isinstance(keyword_results, Exception):
                logger.warning(f"Keyword search failed in hybrid: {keyword_results}")
                keyword_results = []
            
            if isinstance(temporal_results, Exception):
                logger.warning(f"Temporal search failed in hybrid: {temporal_results}")
                temporal_results = []
            
            # Combine and deduplicate results
            all_memories = {}
            
            # Add semantic results with high weight
            for memory in semantic_results:
                memory_id = memory["memory_id"]
                memory["search_source"] = "semantic"
                memory["source_weight"] = 0.4
                all_memories[memory_id] = memory
            
            # Add keyword results
            for memory in keyword_results:
                memory_id = memory["memory_id"]
                if memory_id in all_memories:
                    # Boost score for memories found in multiple searches
                    all_memories[memory_id]["similarity_score"] = min(1.0, 
                        all_memories[memory_id]["similarity_score"] + 0.2)
                    all_memories[memory_id]["search_source"] += ",keyword"
                else:
                    memory["search_source"] = "keyword"
                    memory["source_weight"] = 0.3
                    all_memories[memory_id] = memory
            
            # Add temporal results
            for memory in temporal_results:
                memory_id = memory["memory_id"]
                if memory_id in all_memories:
                    # Boost score for memories found in multiple searches
                    all_memories[memory_id]["similarity_score"] = min(1.0, 
                        all_memories[memory_id]["similarity_score"] + 0.1)
                    all_memories[memory_id]["search_source"] += ",temporal"
                else:
                    memory["search_source"] = "temporal"
                    memory["source_weight"] = 0.3
                    all_memories[memory_id] = memory
            
            # Convert back to list and sort by combined score
            combined_results = list(all_memories.values())
            
            logger.debug(f"✅ Hybrid search combined {len(combined_results)} unique memories")
            return combined_results
            
        except Exception as e:
            logger.error(f"❌ Hybrid search failed: {e}")
            return []
    
    async def _calculate_relevance_scores(
        self, 
        memories: List[Dict[str, Any]], 
        params: MemorySearchParams
    ) -> List[MemorySearchResult]:
        """Calculate comprehensive relevance scores for memories"""
        try:
            scored_memories = []
            current_time = datetime.now()
            
            # Get strategy weights
            weights = self.strategy_weights.get(params.search_type, self.strategy_weights["hybrid"])
            
            for memory in memories:
                # Parse metadata if needed
                metadata = memory.get("metadata", {})
                if isinstance(metadata, str):
                    try:
                        metadata = json.loads(metadata)
                    except json.JSONDecodeError:
                        metadata = {}
                
                # Calculate individual scores
                similarity_score = memory.get("similarity_score", 0.5)
                temporal_score = self._calculate_temporal_score(memory["created_at"], current_time)
                consciousness_score = self._calculate_consciousness_score(
                    memory["consciousness_level"], 
                    memory["emotional_state"],
                    params.consciousness_context
                )
                importance_factor = memory["importance_score"]
                
                # Calculate weighted relevance score
                relevance_score = (
                    similarity_score * weights["similarity"] +
                    temporal_score * weights["temporal"] +
                    consciousness_score * weights["consciousness"] +
                    importance_factor * weights["importance"]
                )
                
                # Create result object
                result = MemorySearchResult(
                    memory_id=memory["memory_id"],
                    content=memory["content"],
                    memory_type=memory["memory_type"],
                    agent_name=memory["agent_name"],
                    user_id=params.user_id,
                    consciousness_level=memory["consciousness_level"],
                    emotional_state=memory["emotional_state"],
                    importance_score=memory["importance_score"],
                    created_at=memory["created_at"],
                    metadata=metadata,
                    relevance_score=relevance_score,
                    similarity_score=similarity_score,
                    temporal_score=temporal_score,
                    consciousness_score=consciousness_score,
                    importance_factor=importance_factor
                )
                
                scored_memories.append(result)
            
            return scored_memories
            
        except Exception as e:
            logger.error(f"❌ Failed to calculate relevance scores: {e}")
            return []
    
    def _calculate_temporal_score(self, created_at: str, current_time: datetime) -> float:
        """Calculate temporal relevance score based on memory age"""
        try:
            # Parse creation time
            if isinstance(created_at, str):
                memory_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            else:
                memory_time = created_at
            
            # Calculate age in hours
            age_hours = (current_time - memory_time).total_seconds() / 3600
            
            # Apply exponential decay
            decay_factor = math.exp(-age_hours / self.temporal_decay_hours)
            
            # Ensure minimum score
            return max(0.1, decay_factor)
            
        except Exception as e:
            logger.warning(f"Failed to calculate temporal score: {e}")
            return 0.5
    
    def _calculate_consciousness_score(
        self, 
        memory_consciousness: float, 
        memory_emotion: str,
        current_context: Dict[str, Any]
    ) -> float:
        """Calculate consciousness alignment score"""
        try:
            current_consciousness = current_context.get("consciousness_level", 0.7)
            current_emotion = current_context.get("emotional_state", "neutral")
            
            # Consciousness level alignment
            consciousness_diff = abs(memory_consciousness - current_consciousness)
            consciousness_alignment = max(0.0, 1.0 - (consciousness_diff / self.consciousness_tolerance))
            
            # Emotional state alignment
            emotion_alignment = 1.0 if memory_emotion == current_emotion else 0.7
            
            # Combined consciousness score
            return (consciousness_alignment * 0.7 + emotion_alignment * 0.3)
            
        except Exception as e:
            logger.warning(f"Failed to calculate consciousness score: {e}")
            return 0.5
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from query text"""
        try:
            # Simple keyword extraction (in production, use more sophisticated NLP)
            import re
            
            # Remove punctuation and split
            words = re.findall(r'\b\w+\b', text.lower())
            
            # Filter out common stop words
            stop_words = {
                'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
                'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
                'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you',
                'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
            }
            
            keywords = [word for word in words if word not in stop_words and len(word) > 2]
            
            # Return unique keywords, limited to reasonable number
            return list(set(keywords))[:10]
            
        except Exception as e:
            logger.warning(f"Failed to extract keywords: {e}")
            return []
    
    @handle_errors(
        component="memory_retrieval",
        fallback_result=[],
        suppress_errors=True
    )
    async def consciousness_aware_search(
        self,
        query: str,
        user_id: str,
        consciousness_context: Dict[str, Any],
        consciousness_tolerance: float = 0.2,
        limit: int = 10
    ) -> List[MemorySearchResult]:
        """
        Search memories with consciousness-aware filtering based on consciousness level and emotional state
        
        Args:
            query: Search query text
            user_id: User identifier
            consciousness_context: Current consciousness state context
            consciousness_tolerance: Tolerance for consciousness level matching (0.0-1.0)
            limit: Maximum number of results
            
        Returns:
            List of consciousness-aligned memories
        """
        try:
            current_consciousness = consciousness_context.get("consciousness_level", 0.7)
            current_emotion = consciousness_context.get("emotional_state", "neutral")
            
            # Calculate consciousness level range
            min_consciousness = max(0.0, current_consciousness - consciousness_tolerance)
            max_consciousness = min(1.0, current_consciousness + consciousness_tolerance)
            
            # Build consciousness-aware query
            query_cypher = """
            MATCH (m:Memory {user_id: $user_id})
            WHERE m.consciousness_level >= $min_consciousness 
            AND m.consciousness_level <= $max_consciousness
            """
            
            # Add text matching if query provided
            if query.strip():
                query_cypher += " AND toLower(m.content) CONTAINS toLower($query)"
            
            # Boost memories with matching emotional state
            query_cypher += """
            WITH m,
                 CASE WHEN m.emotional_state = $current_emotion THEN 1.2 ELSE 1.0 END AS emotion_boost,
                 abs(m.consciousness_level - $current_consciousness) AS consciousness_diff
            
            RETURN m.memory_id AS memory_id,
                   m.content AS content,
                   m.memory_type AS memory_type,
                   m.agent_name AS agent_name,
                   m.consciousness_level AS consciousness_level,
                   m.emotional_state AS emotional_state,
                   m.importance_score AS importance_score,
                   m.created_at AS created_at,
                   m.metadata AS metadata,
                   (1.0 - consciousness_diff) * emotion_boost AS consciousness_score
            ORDER BY consciousness_score DESC, m.importance_score DESC
            LIMIT $limit
            """
            
            params = {
                "user_id": user_id,
                "min_consciousness": min_consciousness,
                "max_consciousness": max_consciousness,
                "current_emotion": current_emotion,
                "current_consciousness": current_consciousness,
                "limit": limit
            }
            
            if query.strip():
                params["query"] = query
            
            result = self.neo4j.execute_query(query_cypher, params)
            
            # Convert to MemorySearchResult objects
            memories = []
            for record in result:
                metadata = record.get("metadata", {})
                if isinstance(metadata, str):
                    try:
                        metadata = json.loads(metadata)
                    except json.JSONDecodeError:
                        metadata = {}
                
                memory_result = MemorySearchResult(
                    memory_id=record["memory_id"],
                    content=record["content"],
                    memory_type=record["memory_type"],
                    agent_name=record["agent_name"],
                    user_id=user_id,
                    consciousness_level=record["consciousness_level"],
                    emotional_state=record["emotional_state"],
                    importance_score=record["importance_score"],
                    created_at=record["created_at"],
                    metadata=metadata,
                    relevance_score=record["consciousness_score"],
                    consciousness_score=record["consciousness_score"]
                )
                memories.append(memory_result)
            
            logger.debug(f"✅ Consciousness-aware search found {len(memories)} memories")
            return memories
            
        except Exception as e:
            logger.error(f"❌ Consciousness-aware search failed: {e}")
            return []
    
    @handle_errors(
        component="memory_retrieval",
        fallback_result=[],
        suppress_errors=True
    )
    async def importance_weighted_search(
        self,
        query: str,
        user_id: str,
        consciousness_context: Dict[str, Any],
        importance_threshold: float = 0.3,
        limit: int = 10
    ) -> List[MemorySearchResult]:
        """
        Search memories with importance weighting and decay calculations
        
        Args:
            query: Search query text
            user_id: User identifier
            consciousness_context: Current consciousness state context
            importance_threshold: Minimum importance score threshold
            limit: Maximum number of results
            
        Returns:
            List of importance-weighted memories
        """
        try:
            current_time = datetime.now()
            
            # Build importance-weighted query
            query_cypher = """
            MATCH (m:Memory {user_id: $user_id})
            WHERE m.importance_score >= $importance_threshold
            """
            
            # Add text matching if query provided
            if query.strip():
                query_cypher += " AND toLower(m.content) CONTAINS toLower($query)"
            
            query_cypher += """
            WITH m,
                 duration.between(datetime(m.created_at), datetime($current_time)).hours AS age_hours
            
            // Calculate decayed importance score
            WITH m, age_hours,
                 m.importance_score * exp(-age_hours / 168.0) AS decayed_importance,
                 COALESCE(m.access_count, 0) AS access_count
            
            // Boost frequently accessed memories
            WITH m, decayed_importance,
                 decayed_importance * (1.0 + (access_count * 0.1)) AS weighted_importance
            
            RETURN m.memory_id AS memory_id,
                   m.content AS content,
                   m.memory_type AS memory_type,
                   m.agent_name AS agent_name,
                   m.consciousness_level AS consciousness_level,
                   m.emotional_state AS emotional_state,
                   m.importance_score AS importance_score,
                   m.created_at AS created_at,
                   m.metadata AS metadata,
                   weighted_importance AS final_importance
            ORDER BY weighted_importance DESC
            LIMIT $limit
            """
            
            params = {
                "user_id": user_id,
                "importance_threshold": importance_threshold,
                "current_time": current_time.isoformat(),
                "limit": limit
            }
            
            if query.strip():
                params["query"] = query
            
            result = self.neo4j.execute_query(query_cypher, params)
            
            # Convert to MemorySearchResult objects
            memories = []
            for record in result:
                metadata = record.get("metadata", {})
                if isinstance(metadata, str):
                    try:
                        metadata = json.loads(metadata)
                    except json.JSONDecodeError:
                        metadata = {}
                
                memory_result = MemorySearchResult(
                    memory_id=record["memory_id"],
                    content=record["content"],
                    memory_type=record["memory_type"],
                    agent_name=record["agent_name"],
                    user_id=user_id,
                    consciousness_level=record["consciousness_level"],
                    emotional_state=record["emotional_state"],
                    importance_score=record["importance_score"],
                    created_at=record["created_at"],
                    metadata=metadata,
                    relevance_score=record["final_importance"],
                    importance_factor=record["final_importance"]
                )
                memories.append(memory_result)
            
            logger.debug(f"✅ Importance-weighted search found {len(memories)} memories")
            return memories
            
        except Exception as e:
            logger.error(f"❌ Importance-weighted search failed: {e}")
            return []
    
    @handle_errors(
        component="memory_retrieval",
        fallback_result=[],
        suppress_errors=True
    )
    async def advanced_hybrid_search(
        self,
        query: str,
        user_id: str,
        consciousness_context: Dict[str, Any],
        search_weights: Optional[Dict[str, float]] = None,
        limit: int = 10
    ) -> List[MemorySearchResult]:
        """
        Advanced hybrid search combining semantic, keyword, consciousness, and importance factors
        
        Args:
            query: Search query text
            user_id: User identifier
            consciousness_context: Current consciousness state context
            search_weights: Optional custom weights for different search factors
            limit: Maximum number of results
            
        Returns:
            List of memories ranked by comprehensive hybrid scoring
        """
        try:
            # Default weights if not provided
            if not search_weights:
                search_weights = {
                    "semantic": 0.35,
                    "keyword": 0.25,
                    "consciousness": 0.20,
                    "importance": 0.15,
                    "temporal": 0.05
                }
            
            # Run multiple search strategies concurrently
            search_tasks = []
            
            # Semantic search
            if search_weights.get("semantic", 0) > 0:
                search_tasks.append(("semantic", self._semantic_search(MemorySearchParams(
                    query=query,
                    user_id=user_id,
                    consciousness_context=consciousness_context,
                    limit=limit * 2
                ))))
            
            # Consciousness-aware search
            if search_weights.get("consciousness", 0) > 0:
                search_tasks.append(("consciousness", self.consciousness_aware_search(
                    query, user_id, consciousness_context, limit=limit * 2
                )))
            
            # Importance-weighted search
            if search_weights.get("importance", 0) > 0:
                search_tasks.append(("importance", self.importance_weighted_search(
                    query, user_id, consciousness_context, limit=limit * 2
                )))
            
            # Execute all searches
            search_results = {}
            for search_type, task in search_tasks:
                try:
                    if asyncio.iscoroutine(task):
                        results = await task
                    else:
                        results = task
                    search_results[search_type] = results
                except Exception as e:
                    logger.warning(f"Search strategy '{search_type}' failed: {e}")
                    search_results[search_type] = []
            
            # Combine results with weighted scoring
            memory_scores = {}
            
            for search_type, memories in search_results.items():
                weight = search_weights.get(search_type, 0)
                
                for i, memory in enumerate(memories):
                    if isinstance(memory, dict):
                        memory_id = memory["memory_id"]
                        # Position-based scoring (higher for earlier results)
                        position_score = max(0.1, 1.0 - (i / len(memories)))
                        score = position_score * weight
                    else:  # MemorySearchResult object
                        memory_id = memory.memory_id
                        score = memory.relevance_score * weight
                    
                    if memory_id not in memory_scores:
                        memory_scores[memory_id] = {
                            "memory": memory,
                            "total_score": 0.0,
                            "component_scores": {}
                        }
                    
                    memory_scores[memory_id]["total_score"] += score
                    memory_scores[memory_id]["component_scores"][search_type] = score
            
            # Convert to final results and sort
            final_results = []
            for memory_data in memory_scores.values():
                memory = memory_data["memory"]
                
                if isinstance(memory, dict):
                    # Convert dict to MemorySearchResult
                    metadata = memory.get("metadata", {})
                    if isinstance(metadata, str):
                        try:
                            metadata = json.loads(metadata)
                        except json.JSONDecodeError:
                            metadata = {}
                    
                    result = MemorySearchResult(
                        memory_id=memory["memory_id"],
                        content=memory["content"],
                        memory_type=memory["memory_type"],
                        agent_name=memory["agent_name"],
                        user_id=user_id,
                        consciousness_level=memory["consciousness_level"],
                        emotional_state=memory["emotional_state"],
                        importance_score=memory["importance_score"],
                        created_at=memory["created_at"],
                        metadata=metadata,
                        relevance_score=memory_data["total_score"]
                    )
                else:
                    # Update existing MemorySearchResult
                    result = memory
                    result.relevance_score = memory_data["total_score"]
                
                final_results.append(result)
            
            # Sort by total score and limit results
            final_results.sort(key=lambda x: x.relevance_score, reverse=True)
            final_results = final_results[:limit]
            
            logger.info(f"✅ Advanced hybrid search found {len(final_results)} memories")
            return final_results
            
        except Exception as e:
            logger.error(f"❌ Advanced hybrid search failed: {e}")
            return []
    
    @handle_errors(
        component="memory_retrieval",
        fallback_result=[],
        suppress_errors=True
    )
    async def temporal_relevance_search(
        self,
        query: str,
        user_id: str,
        consciousness_context: Dict[str, Any],
        time_weights: Optional[Dict[str, float]] = None,
        limit: int = 10
    ) -> List[MemorySearchResult]:
        """
        Search with sophisticated temporal relevance scoring for recent vs. historical memories
        
        Args:
            query: Search query text
            user_id: User identifier
            consciousness_context: Current consciousness state context
            time_weights: Optional weights for different time periods
            limit: Maximum number of results
            
        Returns:
            List of memories with temporal relevance scoring
        """
        try:
            current_time = datetime.now()
            
            # Default time period weights if not provided
            if not time_weights:
                time_weights = {
                    "recent": 1.0,      # Last 24 hours
                    "short_term": 0.8,  # Last week
                    "medium_term": 0.6, # Last month
                    "long_term": 0.4    # Older than month
                }
            
            # Build temporal relevance query
            query_cypher = """
            MATCH (m:Memory {user_id: $user_id})
            """
            
            # Add text matching if query provided
            if query.strip():
                query_cypher += " WHERE toLower(m.content) CONTAINS toLower($query)"
            
            query_cypher += """
            WITH m,
                 duration.between(datetime(m.created_at), datetime($current_time)).hours AS age_hours,
                 duration.between(datetime(m.created_at), datetime($current_time)).days AS age_days
            
            // Calculate temporal category and weight
            WITH m, age_hours, age_days,
                 CASE 
                     WHEN age_hours <= 24 THEN $recent_weight
                     WHEN age_days <= 7 THEN $short_term_weight
                     WHEN age_days <= 30 THEN $medium_term_weight
                     ELSE $long_term_weight
                 END AS temporal_weight,
                 CASE 
                     WHEN age_hours <= 24 THEN 'recent'
                     WHEN age_days <= 7 THEN 'short_term'
                     WHEN age_days <= 30 THEN 'medium_term'
                     ELSE 'long_term'
                 END AS temporal_category
            
            // Calculate access frequency boost
            WITH m, temporal_weight, temporal_category,
                 COALESCE(m.access_count, 0) AS access_count,
                 COALESCE(m.last_accessed, m.created_at) AS last_accessed
            
            // Calculate recency of last access
            WITH m, temporal_weight, temporal_category, access_count,
                 duration.between(datetime(last_accessed), datetime($current_time)).hours AS last_access_hours
            
            // Final temporal relevance score
            WITH m, temporal_category,
                 temporal_weight * m.importance_score * 
                 (1.0 + (access_count * 0.05)) * 
                 (1.0 / (1.0 + last_access_hours / 24.0)) AS temporal_relevance
            
            RETURN m.memory_id AS memory_id,
                   m.content AS content,
                   m.memory_type AS memory_type,
                   m.agent_name AS agent_name,
                   m.consciousness_level AS consciousness_level,
                   m.emotional_state AS emotional_state,
                   m.importance_score AS importance_score,
                   m.created_at AS created_at,
                   m.metadata AS metadata,
                   temporal_relevance AS relevance_score,
                   temporal_category
            ORDER BY temporal_relevance DESC
            LIMIT $limit
            """
            
            params = {
                "user_id": user_id,
                "current_time": current_time.isoformat(),
                "recent_weight": time_weights["recent"],
                "short_term_weight": time_weights["short_term"],
                "medium_term_weight": time_weights["medium_term"],
                "long_term_weight": time_weights["long_term"],
                "limit": limit
            }
            
            if query.strip():
                params["query"] = query
            
            result = self.neo4j.execute_query(query_cypher, params)
            
            # Convert to MemorySearchResult objects
            memories = []
            for record in result:
                metadata = record.get("metadata", {})
                if isinstance(metadata, str):
                    try:
                        metadata = json.loads(metadata)
                    except json.JSONDecodeError:
                        metadata = {}
                
                # Add temporal category to metadata
                metadata["temporal_category"] = record.get("temporal_category", "unknown")
                
                memory_result = MemorySearchResult(
                    memory_id=record["memory_id"],
                    content=record["content"],
                    memory_type=record["memory_type"],
                    agent_name=record["agent_name"],
                    user_id=user_id,
                    consciousness_level=record["consciousness_level"],
                    emotional_state=record["emotional_state"],
                    importance_score=record["importance_score"],
                    created_at=record["created_at"],
                    metadata=metadata,
                    relevance_score=record["relevance_score"],
                    temporal_score=record["relevance_score"]
                )
                memories.append(memory_result)
            
            logger.debug(f"✅ Temporal relevance search found {len(memories)} memories")
            return memories
            
        except Exception as e:
            logger.error(f"❌ Temporal relevance search failed: {e}")
            return []
    
    @handle_errors(
        component="memory_retrieval",
        fallback_result=[],
        suppress_errors=True
    )
    async def comprehensive_relevance_ranking(
        self,
        memories: List[MemorySearchResult],
        query: str,
        consciousness_context: Dict[str, Any],
        ranking_factors: Optional[Dict[str, float]] = None
    ) -> List[MemorySearchResult]:
        """
        Apply comprehensive relevance ranking combining multiple factors
        
        Args:
            memories: List of memory search results to rank
            query: Original search query
            consciousness_context: Current consciousness state context
            ranking_factors: Optional weights for different ranking factors
            
        Returns:
            List of memories ranked by comprehensive relevance score
        """
        try:
            if not memories:
                return []
            
            # Default ranking factors if not provided
            if not ranking_factors:
                ranking_factors = {
                    "semantic_similarity": 0.25,
                    "consciousness_alignment": 0.20,
                    "importance_decay": 0.20,
                    "access_frequency": 0.15,
                    "temporal_relevance": 0.10,
                    "user_specificity": 0.10
                }
            
            current_time = datetime.now()
            query_embedding = None
            
            # Generate query embedding for semantic similarity if needed
            try:
                query_embedding = self.embedding.get_embedding(query)
            except Exception as e:
                logger.warning(f"Failed to generate query embedding: {e}")
            
            # Calculate comprehensive scores for each memory
            for memory in memories:
                scores = {}
                
                # 1. Semantic Similarity Score
                if query_embedding and hasattr(memory, 'similarity_score'):
                    scores["semantic_similarity"] = memory.similarity_score
                else:
                    # Fallback to keyword matching score
                    scores["semantic_similarity"] = self._calculate_keyword_similarity(query, memory.content)
                
                # 2. Consciousness Alignment Score
                scores["consciousness_alignment"] = self._calculate_consciousness_alignment_score(
                    memory, consciousness_context
                )
                
                # 3. Importance Decay Score
                scores["importance_decay"] = self._calculate_importance_decay_score(
                    memory, current_time
                )
                
                # 4. Access Frequency Score
                scores["access_frequency"] = self._calculate_access_frequency_score(memory)
                
                # 5. Temporal Relevance Score
                scores["temporal_relevance"] = self._calculate_temporal_relevance_score(
                    memory, current_time
                )
                
                # 6. User Specificity Score
                scores["user_specificity"] = self._calculate_user_specificity_score(memory)
                
                # Calculate weighted comprehensive score
                comprehensive_score = sum(
                    scores[factor] * weight 
                    for factor, weight in ranking_factors.items() 
                    if factor in scores
                )
                
                # Update memory with new relevance score and component scores
                memory.relevance_score = comprehensive_score
                memory.metadata["ranking_scores"] = scores
                memory.metadata["comprehensive_score"] = comprehensive_score
            
            # Sort by comprehensive relevance score
            memories.sort(key=lambda x: x.relevance_score, reverse=True)
            
            logger.debug(f"✅ Applied comprehensive ranking to {len(memories)} memories")
            return memories
            
        except Exception as e:
            logger.error(f"❌ Comprehensive relevance ranking failed: {e}")
            return memories  # Return original list if ranking fails
    
    def _calculate_consciousness_alignment_score(
        self, 
        memory: MemorySearchResult, 
        consciousness_context: Dict[str, Any]
    ) -> float:
        """Calculate consciousness alignment score for memory-query matching"""
        try:
            current_consciousness = consciousness_context.get("consciousness_level", 0.7)
            current_emotion = consciousness_context.get("emotional_state", "neutral")
            
            # Consciousness level alignment (0.0 to 1.0)
            consciousness_diff = abs(memory.consciousness_level - current_consciousness)
            consciousness_alignment = max(0.0, 1.0 - (consciousness_diff / 0.5))  # 0.5 max diff
            
            # Emotional state alignment
            emotion_alignment = 1.0 if memory.emotional_state == current_emotion else 0.6
            
            # Memory type bonus for consciousness memories
            type_bonus = 1.2 if memory.memory_type in ["consciousness_reflection", "insight"] else 1.0
            
            # Combined consciousness alignment score
            alignment_score = (consciousness_alignment * 0.6 + emotion_alignment * 0.4) * type_bonus
            
            return min(1.0, alignment_score)
            
        except Exception as e:
            logger.warning(f"Failed to calculate consciousness alignment score: {e}")
            return 0.5
    
    def _calculate_importance_decay_score(
        self, 
        memory: MemorySearchResult, 
        current_time: datetime
    ) -> float:
        """Calculate importance decay score for aging memories"""
        try:
            # Parse memory creation time
            if isinstance(memory.created_at, str):
                memory_time = datetime.fromisoformat(memory.created_at.replace('Z', '+00:00'))
            else:
                memory_time = memory.created_at
            
            # Calculate age in hours
            age_hours = (current_time - memory_time).total_seconds() / 3600
            
            # Get decay rate from memory or use default
            decay_rate = getattr(memory, 'decay_rate', 0.95)
            if hasattr(memory, 'metadata') and 'decay_rate' in memory.metadata:
                decay_rate = memory.metadata['decay_rate']
            
            # Calculate decay factor (exponential decay)
            decay_factor = math.exp(-age_hours / (168.0 * decay_rate))  # 168 hours = 1 week
            
            # Apply importance score with decay
            decayed_importance = memory.importance_score * decay_factor
            
            # Boost for high-importance memories (slower decay)
            if memory.importance_score > 0.8:
                decayed_importance *= 1.2
            
            return min(1.0, decayed_importance)
            
        except Exception as e:
            logger.warning(f"Failed to calculate importance decay score: {e}")
            return memory.importance_score * 0.5
    
    def _calculate_access_frequency_score(self, memory: MemorySearchResult) -> float:
        """Calculate score based on memory access frequency and recency"""
        try:
            # Get access count from metadata or default
            access_count = 0
            if hasattr(memory, 'metadata') and 'access_count' in memory.metadata:
                access_count = memory.metadata['access_count']
            
            # Get last accessed time
            last_accessed = None
            if hasattr(memory, 'metadata') and 'last_accessed' in memory.metadata:
                last_accessed_str = memory.metadata['last_accessed']
                if last_accessed_str:
                    try:
                        last_accessed = datetime.fromisoformat(last_accessed_str.replace('Z', '+00:00'))
                    except:
                        pass
            
            # Calculate access frequency score
            frequency_score = min(1.0, access_count * 0.1)  # Cap at 1.0
            
            # Calculate recency of access bonus
            recency_bonus = 1.0
            if last_accessed:
                hours_since_access = (datetime.now() - last_accessed).total_seconds() / 3600
                recency_bonus = max(0.5, 1.0 - (hours_since_access / 168.0))  # Decay over 1 week
            
            return frequency_score * recency_bonus
            
        except Exception as e:
            logger.warning(f"Failed to calculate access frequency score: {e}")
            return 0.1
    
    def _calculate_temporal_relevance_score(
        self, 
        memory: MemorySearchResult, 
        current_time: datetime
    ) -> float:
        """Calculate temporal relevance score for recent vs. historical memories"""
        try:
            # Parse memory creation time
            if isinstance(memory.created_at, str):
                memory_time = datetime.fromisoformat(memory.created_at.replace('Z', '+00:00'))
            else:
                memory_time = memory.created_at
            
            # Calculate age in different units
            age_hours = (current_time - memory_time).total_seconds() / 3600
            age_days = age_hours / 24
            
            # Time-based scoring with different decay rates for different periods
            if age_hours <= 24:  # Last 24 hours - high relevance
                temporal_score = 1.0
            elif age_days <= 7:  # Last week - good relevance
                temporal_score = 0.8 * math.exp(-(age_days - 1) / 6)
            elif age_days <= 30:  # Last month - moderate relevance
                temporal_score = 0.6 * math.exp(-(age_days - 7) / 23)
            else:  # Older - lower relevance but not zero
                temporal_score = 0.3 * math.exp(-(age_days - 30) / 60)
            
            # Boost for memories that were recently accessed
            if hasattr(memory, 'metadata') and 'last_accessed' in memory.metadata:
                last_accessed_str = memory.metadata['last_accessed']
                if last_accessed_str:
                    try:
                        last_accessed = datetime.fromisoformat(last_accessed_str.replace('Z', '+00:00'))
                        access_age_hours = (current_time - last_accessed).total_seconds() / 3600
                        if access_age_hours <= 24:
                            temporal_score *= 1.2  # 20% boost for recently accessed
                    except:
                        pass
            
            return min(1.0, temporal_score)
            
        except Exception as e:
            logger.warning(f"Failed to calculate temporal relevance score: {e}")
            return 0.5
    
    def _calculate_user_specificity_score(self, memory: MemorySearchResult) -> float:
        """Calculate user-specific memory prioritization score"""
        try:
            base_score = 0.5
            
            # Memory type scoring
            type_scores = {
                "interaction": 0.8,           # User interactions are highly relevant
                "consciousness_reflection": 0.6,  # Consciousness memories are moderately relevant
                "insight": 0.9,              # Insights are very relevant
                "concept_learning": 0.7,     # Learning memories are quite relevant
                "system": 0.3                # System memories are less relevant
            }
            
            memory_type_score = type_scores.get(memory.memory_type, 0.5)
            
            # Agent specificity (some agents might be more important to user)
            agent_scores = {
                "simple_chat": 0.9,          # Direct chat interactions
                "consciousness_system": 0.6,  # Consciousness reflections
                "graphmaster": 0.7,          # Knowledge graph interactions
                "conductor": 0.8,            # Orchestration memories
                "research_agent": 0.7        # Research interactions
            }
            
            agent_score = agent_scores.get(memory.agent_name, 0.6)
            
            # Content length factor (longer memories might be more substantial)
            content_length = len(memory.content.split())
            length_factor = min(1.2, 1.0 + (content_length - 20) / 100) if content_length > 20 else 1.0
            
            # Combine factors
            specificity_score = (memory_type_score * 0.5 + agent_score * 0.3) * length_factor * 0.2
            
            return min(1.0, base_score + specificity_score)
            
        except Exception as e:
            logger.warning(f"Failed to calculate user specificity score: {e}")
            return 0.5
    
    def _calculate_keyword_similarity(self, query: str, content: str) -> float:
        """Calculate keyword-based similarity as fallback for semantic similarity"""
        try:
            query_words = set(self._extract_keywords(query.lower()))
            content_words = set(self._extract_keywords(content.lower()))
            
            if not query_words or not content_words:
                return 0.1
            
            # Calculate Jaccard similarity
            intersection = query_words.intersection(content_words)
            union = query_words.union(content_words)
            
            jaccard_similarity = len(intersection) / len(union) if union else 0.0
            
            # Boost for exact phrase matches
            phrase_boost = 1.0
            if query.lower() in content.lower():
                phrase_boost = 1.3
            
            return min(1.0, jaccard_similarity * phrase_boost)
            
        except Exception as e:
            logger.warning(f"Failed to calculate keyword similarity: {e}")
            return 0.1
    
    @handle_errors(
        component="memory_retrieval",
        fallback_result=[],
        suppress_errors=True
    )
    async def user_personalized_ranking(
        self,
        memories: List[MemorySearchResult],
        user_id: str,
        personalization_factors: Optional[Dict[str, Any]] = None
    ) -> List[MemorySearchResult]:
        """
        Apply user-specific personalized ranking based on user preferences and history
        
        Args:
            memories: List of memory search results to rank
            user_id: User identifier for personalization
            personalization_factors: Optional user-specific factors
            
        Returns:
            List of memories ranked with user personalization
        """
        try:
            if not memories:
                return []
            
            # Get user interaction patterns
            user_patterns = await self._get_user_interaction_patterns(user_id)
            
            # Apply personalization to each memory
            for memory in memories:
                personalization_score = 1.0
                
                # Agent preference scoring
                agent_preference = user_patterns.get("agent_preferences", {}).get(
                    memory.agent_name, 0.5
                )
                personalization_score *= (0.7 + agent_preference * 0.6)
                
                # Memory type preference scoring
                type_preference = user_patterns.get("memory_type_preferences", {}).get(
                    memory.memory_type, 0.5
                )
                personalization_score *= (0.7 + type_preference * 0.6)
                
                # Time of day preference (if available)
                if hasattr(memory, 'created_at'):
                    try:
                        memory_time = datetime.fromisoformat(memory.created_at.replace('Z', '+00:00'))
                        memory_hour = memory_time.hour
                        hour_preference = user_patterns.get("time_preferences", {}).get(
                            str(memory_hour), 0.5
                        )
                        personalization_score *= (0.8 + hour_preference * 0.4)
                    except:
                        pass
                
                # Apply personalization to relevance score
                memory.relevance_score *= personalization_score
                
                # Store personalization details in metadata
                if not hasattr(memory, 'metadata'):
                    memory.metadata = {}
                memory.metadata["personalization_score"] = personalization_score
                memory.metadata["user_patterns"] = user_patterns
            
            # Re-sort by updated relevance scores
            memories.sort(key=lambda x: x.relevance_score, reverse=True)
            
            logger.debug(f"✅ Applied user personalization to {len(memories)} memories")
            return memories
            
        except Exception as e:
            logger.error(f"❌ User personalized ranking failed: {e}")
            return memories
    
    async def _get_user_interaction_patterns(self, user_id: str) -> Dict[str, Any]:
        """Get user interaction patterns for personalization"""
        try:
            # Query user interaction patterns
            query = """
            MATCH (m:Memory {user_id: $user_id})
            WITH m,
                 CASE WHEN m.created_at IS NOT NULL 
                      THEN datetime(m.created_at).hour 
                      ELSE 12 END AS hour
            
            RETURN 
                m.agent_name AS agent_name,
                m.memory_type AS memory_type,
                hour,
                count(*) AS interaction_count,
                avg(COALESCE(m.access_count, 0)) AS avg_access_count,
                avg(m.importance_score) AS avg_importance
            """
            
            result = self.neo4j.execute_query(query, {"user_id": user_id})
            
            patterns = {
                "agent_preferences": {},
                "memory_type_preferences": {},
                "time_preferences": {}
            }
            
            total_interactions = sum(record["interaction_count"] for record in result)
            
            if total_interactions == 0:
                return patterns
            
            # Calculate preferences based on interaction frequency and engagement
            for record in result:
                agent_name = record["agent_name"]
                memory_type = record["memory_type"]
                hour = record["hour"]
                count = record["interaction_count"]
                avg_access = record["avg_access_count"]
                avg_importance = record["avg_importance"]
                
                # Agent preference (frequency + engagement)
                agent_freq = count / total_interactions
                agent_engagement = (avg_access * 0.3 + avg_importance * 0.7)
                patterns["agent_preferences"][agent_name] = min(1.0, agent_freq + agent_engagement * 0.5)
                
                # Memory type preference
                type_freq = count / total_interactions
                patterns["memory_type_preferences"][memory_type] = min(1.0, type_freq + agent_engagement * 0.3)
                
                # Time preference
                time_freq = count / total_interactions
                patterns["time_preferences"][str(hour)] = min(1.0, time_freq * 2)  # Boost time preferences
            
            return patterns
            
        except Exception as e:
            logger.warning(f"Failed to get user interaction patterns: {e}")
            return {"agent_preferences": {}, "memory_type_preferences": {}, "time_preferences": {}}
    
    async def get_user_memories(
        self,
        user_id: str,
        limit: int = 50,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Get memories for a specific user with optional filtering"""
        try:
            query_parts = ["MATCH (m:Memory {user_id: $user_id})"]
            params = {"user_id": user_id}
            
            # Add filters
            if filters:
                if filters.get("memory_type"):
                    query_parts.append("AND m.memory_type = $memory_type")
                    params["memory_type"] = filters["memory_type"]
                
                if filters.get("start_date"):
                    query_parts.append("AND m.created_at >= datetime($start_date)")
                    params["start_date"] = filters["start_date"]
                
                if filters.get("end_date"):
                    query_parts.append("AND m.created_at <= datetime($end_date)")
                    params["end_date"] = filters["end_date"]
            
            query = " ".join(query_parts) + f"""
                RETURN m.memory_id as memory_id, m.content as content, m.memory_type as memory_type,
                       m.user_id as user_id, m.agent_name as agent_name, m.consciousness_level as consciousness_level,
                       m.emotional_state as emotional_state, m.importance_score as importance_score,
                       m.created_at as created_at, m.last_accessed as last_accessed,
                       m.access_count as access_count, m.significance_score as significance_score
                ORDER BY m.created_at DESC
                LIMIT $limit
            """
            params["limit"] = limit
            
            result = self.neo4j.execute_query(query, params)
            return result if result else []
            
        except Exception as e:
            logger.error(f"Failed to get user memories: {e}")
            return []
    
    async def get_conversation_memories(
        self,
        conversation_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get memories for a specific conversation"""
        try:
            query = """
                MATCH (m:Memory)-[:DISCUSSED_IN]->(c:Conversation {conversation_id: $conversation_id})
                RETURN m.memory_id as memory_id, m.content as content, m.memory_type as memory_type,
                       m.user_id as user_id, m.agent_name as agent_name, m.consciousness_level as consciousness_level,
                       m.emotional_state as emotional_state, m.importance_score as importance_score,
                       m.created_at as created_at, m.last_accessed as last_accessed,
                       m.access_count as access_count, m.significance_score as significance_score
                ORDER BY m.created_at ASC
                LIMIT $limit
            """
            
            result = self.neo4j.execute_query(query, {
                "conversation_id": conversation_id,
                "limit": limit
            })
            return result if result else []
            
        except Exception as e:
            logger.error(f"Failed to get conversation memories: {e}")
            return []
    
    async def get_memory_by_id(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific memory"""
        try:
            query = """
                MATCH (m:Memory {memory_id: $memory_id})
                OPTIONAL MATCH (m)-[:RELATES_TO]->(c:Concept)
                OPTIONAL MATCH (m)-[:DISCUSSED_IN]->(conv:Conversation)
                RETURN m.memory_id as memory_id, m.content as content, m.memory_type as memory_type,
                       m.user_id as user_id, m.agent_name as agent_name, m.consciousness_level as consciousness_level,
                       m.emotional_state as emotional_state, m.importance_score as importance_score,
                       m.created_at as created_at, m.last_accessed as last_accessed,
                       m.access_count as access_count, m.significance_score as significance_score,
                       m.decay_rate as decay_rate, m.metadata as metadata,
                       collect(DISTINCT c.name) as related_concepts,
                       collect(DISTINCT conv.conversation_id) as conversations
            """
            
            result = self.neo4j.execute_query(query, {"memory_id": memory_id})
            return result[0] if result else None
            
        except Exception as e:
            logger.error(f"Failed to get memory by ID: {e}")
            return None

    async def _update_access_statistics(self, memory_ids: List[str]):
        """Update access statistics for retrieved memories"""
        try:
            if not memory_ids:
                return
            
            query = """
            UNWIND $memory_ids AS memory_id
            MATCH (m:Memory {memory_id: memory_id})
            SET m.access_count = COALESCE(m.access_count, 0) + 1,
                m.last_accessed = $timestamp
            RETURN count(m) AS updated_count
            """
            
            result = self.neo4j.execute_write_query(query, {
                "memory_ids": memory_ids,
                "timestamp": datetime.now().isoformat()
            })
            
            if result:
                logger.debug(f"✅ Updated access statistics for {result[0]['updated_count']} memories")
                
        except Exception as e:
            logger.warning(f"Failed to update access statistics: {e}")

# Global instance
memory_retrieval_engine = MemoryRetrievalEngine()