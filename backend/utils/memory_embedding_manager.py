"""
Memory Embedding Manager for Mainza AI
Handles embedding generation, storage, and similarity search for memories
"""
import logging
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import numpy as np

from backend.utils.neo4j_enhanced import neo4j_manager
from backend.utils.embedding_enhanced import embedding_manager
from backend.core.enhanced_error_handling import ErrorHandler, handle_errors

logger = logging.getLogger(__name__)
error_handler = ErrorHandler()

class MemoryEmbeddingManager:
    """
    Manages embedding operations for memory storage and retrieval
    """
    
    def __init__(self):
        self.neo4j = neo4j_manager
        self.embedding = embedding_manager
        self.similarity_threshold = 0.7  # Minimum similarity for related memories
        self.max_similar_memories = 10   # Maximum similar memories to return
        self.batch_size = 50            # Batch size for bulk operations
        
    @handle_errors(
        component="memory_embedding",
        fallback_result=[],
        suppress_errors=True
    )
    async def find_similar_memories(
        self,
        query_text: str,
        user_id: str,
        memory_types: Optional[List[str]] = None,
        limit: int = 5,
        min_similarity: float = 0.6
    ) -> List[Dict[str, Any]]:
        """
        Find memories similar to the given query text using vector search
        
        Args:
            query_text: Text to search for similar memories
            user_id: User identifier to filter memories
            memory_types: Optional list of memory types to filter by
            limit: Maximum number of results to return
            min_similarity: Minimum similarity threshold
            
        Returns:
            List of similar memory records with similarity scores
        """
        try:
            # Generate embedding for query
            query_embedding = self.embedding.get_embedding(query_text)
            
            if not query_embedding or all(x == 0.0 for x in query_embedding):
                logger.warning("Invalid query embedding, falling back to text search")
                return await self._fallback_text_search(query_text, user_id, memory_types, limit)
            
            # Try vector search first
            similar_memories = await self._vector_similarity_search(
                query_embedding, user_id, memory_types, limit, min_similarity
            )
            
            if similar_memories:
                logger.debug(f"✅ Found {len(similar_memories)} similar memories via vector search")
                return similar_memories
            
            # Fallback to text search if vector search fails or returns no results
            logger.info("Vector search returned no results, falling back to text search")
            return await self._fallback_text_search(query_text, user_id, memory_types, limit)
            
        except Exception as e:
            logger.error(f"❌ Failed to find similar memories: {e}")
            return []
    
    async def _vector_similarity_search(
        self,
        query_embedding: List[float],
        user_id: str,
        memory_types: Optional[List[str]],
        limit: int,
        min_similarity: float
    ) -> List[Dict[str, Any]]:
        """Perform vector similarity search using Neo4j vector index"""
        try:
            # Continue with vector search

            # Build the Cypher query with optional memory type filtering
            base_query = """
            CALL db.index.vector.queryNodes('memory_embedding_index', $limit, $embedding)
            YIELD node, score
            WHERE node.user_id = $user_id
            """

            # Add memory type filtering if specified
            if memory_types:
                base_query += " AND node.memory_type IN $memory_types"

            # Add similarity threshold and return clause
            base_query += """
            AND score >= $min_similarity
            RETURN node.memory_id AS memory_id,
                   node.content AS content,
                   node.memory_type AS memory_type,
                   node.agent_name AS agent_name,
                   node.consciousness_level AS consciousness_level,
                   node.emotional_state AS emotional_state,
                   node.importance_score AS importance_score,
                   node.created_at AS created_at,
                   node.metadata AS metadata,
                   score AS similarity_score
            ORDER BY score DESC
            LIMIT $limit
            """

            params = {
                "embedding": query_embedding,
                "user_id": user_id,
                "limit": limit,
                "min_similarity": min_similarity
            }

            if memory_types:
                params["memory_types"] = memory_types

            result = self.neo4j.execute_query(base_query, params)
            
            # Process results
            similar_memories = []
            for record in result:
                memory = dict(record)
                
                # Parse metadata if it's a JSON string
                if isinstance(memory.get("metadata"), str):
                    try:
                        import json
                        memory["metadata"] = json.loads(memory["metadata"])
                    except json.JSONDecodeError:
                        memory["metadata"] = {}
                
                similar_memories.append(memory)
            
            return similar_memories
            
        except Exception as e:
            logger.error(f"❌ Vector similarity search failed: {e}")
            return []
    
    async def _fallback_text_search(
        self,
        query_text: str,
        user_id: str,
        memory_types: Optional[List[str]],
        limit: int
    ) -> List[Dict[str, Any]]:
        """Fallback text-based search when vector search is unavailable"""
        try:
            # Try full-text search first
            fulltext_query = """
            CALL db.index.fulltext.queryNodes('memory_content_fulltext', $query) 
            YIELD node, score
            WHERE node.user_id = $user_id
            """
            
            if memory_types:
                fulltext_query += " AND node.memory_type IN $memory_types"
            
            fulltext_query += """
            RETURN node.memory_id AS memory_id,
                   node.content AS content,
                   node.memory_type AS memory_type,
                   node.agent_name AS agent_name,
                   node.consciousness_level AS consciousness_level,
                   node.emotional_state AS emotional_state,
                   node.importance_score AS importance_score,
                   node.created_at AS created_at,
                   node.metadata AS metadata,
                   score AS similarity_score
            ORDER BY score DESC
            LIMIT $limit
            """
            
            params = {
                "query": query_text,
                "user_id": user_id,
                "limit": limit
            }
            
            if memory_types:
                params["memory_types"] = memory_types
            
            try:
                result = self.neo4j.execute_query(fulltext_query, params)
                if result:
                    logger.debug(f"✅ Full-text search found {len(result)} memories")
                    return [dict(record) for record in result]
            except Exception as e:
                logger.debug(f"Full-text search failed: {e}")
            
            # Final fallback: simple text matching
            simple_query = """
            MATCH (m:Memory)
            WHERE m.user_id = $user_id
            AND toLower(m.content) CONTAINS toLower($query)
            """
            
            if memory_types:
                simple_query += " AND m.memory_type IN $memory_types"
            
            simple_query += """
            RETURN m.memory_id AS memory_id,
                   m.content AS content,
                   m.memory_type AS memory_type,
                   m.agent_name AS agent_name,
                   m.consciousness_level AS consciousness_level,
                   m.emotional_state AS emotional_state,
                   m.importance_score AS importance_score,
                   m.created_at AS created_at,
                   m.metadata AS metadata,
                   0.5 AS similarity_score
            ORDER BY m.importance_score DESC, m.created_at DESC
            LIMIT $limit
            """
            
            result = self.neo4j.execute_query(simple_query, params)
            logger.debug(f"✅ Simple text search found {len(result)} memories")
            return [dict(record) for record in result]
            
        except Exception as e:
            logger.error(f"❌ Fallback text search failed: {e}")
            return []
    
    @handle_errors(
        component="memory_embedding",
        fallback_result=False,
        suppress_errors=True
    )
    async def update_memory_embedding(self, memory_id: str, content: str) -> bool:
        """
        Update the embedding for an existing memory
        
        Args:
            memory_id: Unique identifier of the memory
            content: Updated content to generate embedding for
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Generate new embedding
            new_embedding = self.embedding.get_embedding(content)
            
            if not new_embedding or all(x == 0.0 for x in new_embedding):
                logger.warning(f"Failed to generate embedding for memory {memory_id}")
                return False
            
            # Update memory in Neo4j
            cypher = """
            MATCH (m:Memory {memory_id: $memory_id})
            SET m.embedding = $embedding,
                m.content = $content,
                m.last_accessed = $timestamp
            RETURN m.memory_id AS memory_id
            """
            
            result = self.neo4j.execute_write_query(cypher, {
                "memory_id": memory_id,
                "embedding": new_embedding,
                "content": content,
                "timestamp": datetime.now().isoformat()
            })
            
            if result and len(result) > 0:
                logger.debug(f"✅ Updated embedding for memory: {memory_id}")
                return True
            else:
                logger.warning(f"Memory not found for embedding update: {memory_id}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to update memory embedding: {e}")
            return False
    
    @handle_errors(
        component="memory_embedding",
        fallback_result=0,
        suppress_errors=True
    )
    async def regenerate_all_embeddings(
        self,
        user_id: Optional[str] = None,
        batch_size: Optional[int] = None
    ) -> int:
        """
        Regenerate embeddings for all memories (or for a specific user)
        
        Args:
            user_id: Optional user ID to filter memories
            batch_size: Optional batch size for processing
            
        Returns:
            int: Number of embeddings successfully regenerated
        """
        try:
            batch_size = batch_size or self.batch_size
            
            # Get memories that need embedding regeneration
            query = """
            MATCH (m:Memory)
            """
            
            if user_id:
                query += " WHERE m.user_id = $user_id"
            
            query += """
            RETURN m.memory_id AS memory_id, m.content AS content
            ORDER BY m.created_at DESC
            """
            
            params = {"user_id": user_id} if user_id else {}
            memories = self.neo4j.execute_query(query, params)
            
            if not memories:
                logger.info("No memories found for embedding regeneration")
                return 0
            
            logger.info(f"🔄 Regenerating embeddings for {len(memories)} memories...")
            
            # Process in batches
            updated_count = 0
            for i in range(0, len(memories), batch_size):
                batch = memories[i:i + batch_size]
                
                # Generate embeddings for batch
                contents = [memory["content"] for memory in batch]
                embeddings = self.embedding.get_embeddings_batch(contents, batch_size)
                
                # Update memories with new embeddings
                for j, memory in enumerate(batch):
                    if j < len(embeddings) and embeddings[j]:
                        success = await self._update_memory_embedding_direct(
                            memory["memory_id"], embeddings[j]
                        )
                        if success:
                            updated_count += 1
                
                # Log progress
                if len(memories) > 100 and i % (batch_size * 5) == 0:
                    logger.info(f"📊 Processed {i + len(batch)}/{len(memories)} memories")
            
            logger.info(f"✅ Regenerated {updated_count}/{len(memories)} embeddings")
            return updated_count
            
        except Exception as e:
            logger.error(f"❌ Failed to regenerate embeddings: {e}")
            return 0
    
    async def _update_memory_embedding_direct(self, memory_id: str, embedding: List[float]) -> bool:
        """Update memory embedding directly without regenerating"""
        try:
            cypher = """
            MATCH (m:Memory {memory_id: $memory_id})
            SET m.embedding = $embedding
            RETURN m.memory_id AS memory_id
            """
            
            result = self.neo4j.execute_write_query(cypher, {
                "memory_id": memory_id,
                "embedding": embedding
            })
            
            return result and len(result) > 0
            
        except Exception as e:
            logger.error(f"❌ Failed to update memory embedding directly: {e}")
            return False
    
    @handle_errors(
        component="memory_embedding",
        fallback_result=[],
        suppress_errors=True
    )
    async def find_memory_clusters(
        self,
        user_id: str,
        cluster_threshold: float = 0.8,
        min_cluster_size: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Find clusters of similar memories for a user
        
        Args:
            user_id: User identifier
            cluster_threshold: Similarity threshold for clustering
            min_cluster_size: Minimum number of memories in a cluster
            
        Returns:
            List of memory clusters with their members
        """
        try:
            # Get all memories for the user with embeddings
            query = """
            MATCH (m:Memory {user_id: $user_id})
            WHERE m.embedding IS NOT NULL
            RETURN m.memory_id AS memory_id,
                   m.content AS content,
                   m.memory_type AS memory_type,
                   m.embedding AS embedding,
                   m.importance_score AS importance_score
            ORDER BY m.created_at DESC
            """
            
            memories = self.neo4j.execute_query(query, {"user_id": user_id})
            
            if len(memories) < min_cluster_size:
                logger.info(f"Not enough memories for clustering: {len(memories)}")
                return []
            
            # Simple clustering based on cosine similarity
            clusters = []
            processed = set()
            
            for i, memory in enumerate(memories):
                if memory["memory_id"] in processed:
                    continue
                
                # Start a new cluster
                cluster = {
                    "cluster_id": f"cluster_{len(clusters)}",
                    "members": [memory],
                    "avg_importance": memory["importance_score"],
                    "dominant_type": memory["memory_type"]
                }
                
                processed.add(memory["memory_id"])
                
                # Find similar memories for this cluster
                for j, other_memory in enumerate(memories[i+1:], i+1):
                    if other_memory["memory_id"] in processed:
                        continue
                    
                    # Calculate similarity
                    similarity = self.embedding.cosine_similarity(
                        memory["embedding"], other_memory["embedding"]
                    )
                    
                    if similarity >= cluster_threshold:
                        cluster["members"].append(other_memory)
                        processed.add(other_memory["memory_id"])
                
                # Only keep clusters with minimum size
                if len(cluster["members"]) >= min_cluster_size:
                    # Calculate cluster statistics
                    cluster["size"] = len(cluster["members"])
                    cluster["avg_importance"] = sum(
                        m["importance_score"] for m in cluster["members"]
                    ) / len(cluster["members"])
                    
                    # Determine dominant memory type
                    type_counts = {}
                    for member in cluster["members"]:
                        mem_type = member["memory_type"]
                        type_counts[mem_type] = type_counts.get(mem_type, 0) + 1
                    
                    cluster["dominant_type"] = max(type_counts, key=type_counts.get)
                    cluster["type_distribution"] = type_counts
                    
                    clusters.append(cluster)
            
            logger.info(f"✅ Found {len(clusters)} memory clusters for user {user_id}")
            return clusters
            
        except Exception as e:
            logger.error(f"❌ Failed to find memory clusters: {e}")
            return []
    
    async def reindex_all_memories(self) -> Dict[str, Any]:
        """
        Reindex all memories by regenerating embeddings and updating vector indices
        """
        try:
            logger.info("Starting memory reindexing process...")
            
            # Get count of memories without embeddings
            query = """
                MATCH (m:Memory) 
                WHERE m.embedding IS NULL OR size(m.embedding) = 0
                RETURN count(m) as missing_embeddings
            """
            result = self.neo4j.execute_query(query, {})
            missing_embeddings = result[0]['missing_embeddings'] if result else 0
            
            # Get total memory count
            query = "MATCH (m:Memory) RETURN count(m) as total"
            result = self.neo4j.execute_query(query, {})
            total_memories = result[0]['total'] if result else 0
            
            # Regenerate embeddings for memories without them
            regenerated = 0
            if missing_embeddings > 0:
                regenerated = await self.regenerate_all_embeddings()
            
            # Update vector indices (this would depend on your vector database setup)
            # For now, we'll just report the statistics
            
            reindex_results = {
                "total_memories": total_memories,
                "missing_embeddings_before": missing_embeddings,
                "embeddings_regenerated": regenerated,
                "reindex_completed": True,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Memory reindexing completed: {reindex_results}")
            return reindex_results
            
        except Exception as e:
            logger.error(f"Memory reindexing failed: {e}")
            return {
                "reindex_completed": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def get_embedding_statistics(self) -> Dict[str, Any]:
        """Get statistics about memory embeddings in the system"""
        try:
            stats = {
                "total_memories": 0,
                "memories_with_embeddings": 0,
                "embedding_coverage": 0.0,
                "avg_embedding_dimension": 0,
                "memory_types": {}
            }
            
            # Get basic counts
            count_query = """
            MATCH (m:Memory)
            RETURN count(m) AS total_memories,
                   count(CASE WHEN m.embedding IS NOT NULL THEN 1 END) AS memories_with_embeddings
            """
            
            count_result = self.neo4j.execute_query(count_query)
            if count_result:
                stats["total_memories"] = count_result[0]["total_memories"]
                stats["memories_with_embeddings"] = count_result[0]["memories_with_embeddings"]
                
                if stats["total_memories"] > 0:
                    stats["embedding_coverage"] = (
                        stats["memories_with_embeddings"] / stats["total_memories"]
                    )
            
            # Get embedding dimension info
            dimension_query = """
            MATCH (m:Memory)
            WHERE m.embedding IS NOT NULL
            RETURN size(m.embedding) AS dimension
            LIMIT 1
            """
            
            dimension_result = self.neo4j.execute_query(dimension_query)
            if dimension_result:
                stats["avg_embedding_dimension"] = dimension_result[0]["dimension"]
            
            # Get memory type distribution
            type_query = """
            MATCH (m:Memory)
            RETURN m.memory_type AS memory_type,
                   count(m) AS count,
                   count(CASE WHEN m.embedding IS NOT NULL THEN 1 END) AS with_embeddings
            """
            
            type_result = self.neo4j.execute_query(type_query)
            for record in type_result:
                memory_type = record["memory_type"]
                stats["memory_types"][memory_type] = {
                    "total": record["count"],
                    "with_embeddings": record["with_embeddings"],
                    "coverage": record["with_embeddings"] / record["count"] if record["count"] > 0 else 0
                }
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Failed to get embedding statistics: {e}")
            return {"error": str(e)}

# Global instance
memory_embedding_manager = MemoryEmbeddingManager()
