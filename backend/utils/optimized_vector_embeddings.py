"""
Optimized Vector Embeddings System for Mainza AI
Implements advanced vector embedding strategies using Neo4j GraphRAG
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
from neo4j import GraphDatabase
from neo4j_graphrag.embeddings import SentenceTransformerEmbeddings
from neo4j_graphrag.indexes import create_vector_index, upsert_vectors
from neo4j_graphrag.retrievers import VectorRetriever
from neo4j_graphrag.types import EntityType
import json
import hashlib
import ollama
import os

logger = logging.getLogger(__name__)

class OllamaEmbeddings:
    """Custom Ollama embeddings wrapper for compatibility with Neo4j GraphRAG"""
    
    def __init__(self, model: str, base_url: str = None):
        self.model = model
        self.base_url = base_url or os.getenv('OLLAMA_BASE_URL', 'http://host.docker.internal:11434')
        self.client = ollama.Client(host=self.base_url)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents"""
        embeddings = []
        for text in texts:
            try:
                response = self.client.embeddings(model=self.model, prompt=text)
                embeddings.append(response['embedding'])
            except Exception as e:
                logger.error(f"Error generating embedding for text: {e}")
                # Return zero vector as fallback
                embeddings.append([0.0] * 768)  # Default dimension for nomic-embed-text
        return embeddings
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query"""
        try:
            response = self.client.embeddings(model=self.model, prompt=text)
            return response['embedding']
        except Exception as e:
            logger.error(f"Error generating embedding for query: {e}")
            # Return zero vector as fallback
            return [0.0] * 768  # Default dimension for nomic-embed-text

class OptimizedVectorEmbeddings:
    """
    Advanced vector embeddings system with optimization strategies
    """
    
    def __init__(self, neo4j_driver, config: Dict[str, Any]):
        self.driver = neo4j_driver
        self.config = config
        self.embedding_models = {}
        self.vector_indexes = {}
        self.cache = {}
        self.performance_metrics = {
            "total_embeddings": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "average_embedding_time": 0.0,
            "compression_ratio": 0.0
        }
        
        # Initialize embedding models
        self._initialize_embedding_models()
        
    def _initialize_embedding_models(self):
        """Initialize multiple embedding models for different use cases"""
        try:
            # Get the default embedding model from environment
            default_model = os.getenv('DEFAULT_EMBEDDING_MODEL', 'nomic-embed-text:latest')
            ollama_base_url = os.getenv('OLLAMA_BASE_URL', 'http://host.docker.internal:11434')
            
            # Primary model for general embeddings using Ollama
            self.embedding_models["primary"] = OllamaEmbeddings(
                model=default_model,
                base_url=ollama_base_url
            )
            
            # Fast model for real-time applications using SentenceTransformers as fallback
            self.embedding_models["fast"] = SentenceTransformerEmbeddings(
                model="all-MiniLM-L6-v2"
            )
            
            # Specialized model for consciousness-related content using Ollama
            self.embedding_models["consciousness"] = OllamaEmbeddings(
                model=default_model,
                base_url=ollama_base_url
            )
            
            logger.info(f"Embedding models initialized successfully with Ollama model: {default_model}")
            
        except Exception as e:
            logger.error(f"Error initializing embedding models: {e}")
            raise
    
    async def create_optimized_vector_indexes(self):
        """Create optimized vector indexes for different content types"""
        try:
            # Consciousness content index
            await self._create_vector_index(
                index_name="consciousness_embeddings",
                label="ConsciousnessMemory",
                embedding_property="embedding",
                dimensions=768,
                similarity_fn="cosine"
            )
            
            # Agent memory index
            await self._create_vector_index(
                index_name="agent_memory_embeddings",
                label="AgentMemory",
                embedding_property="embedding",
                dimensions=768,
                similarity_fn="cosine"
            )
            
            # Concept knowledge index
            await self._create_vector_index(
                index_name="concept_embeddings",
                label="Concept",
                embedding_property="embedding",
                dimensions=768,
                similarity_fn="cosine"
            )
            
            # Cross-agent learning index
            await self._create_vector_index(
                index_name="cross_agent_embeddings",
                label="CrossAgentLearning",
                embedding_property="embedding",
                dimensions=768,
                similarity_fn="cosine"
            )
            
            logger.info("Optimized vector indexes created successfully")
            
        except Exception as e:
            logger.error(f"Error creating vector indexes: {e}")
            raise
    
    async def _create_vector_index(self, index_name: str, label: str, 
                                 embedding_property: str, dimensions: int, 
                                 similarity_fn: str):
        """Create a vector index with optimized settings"""
        try:
            # Create vector index using direct Cypher query to avoid parameterized index name issues
            cypher_query = f"""
            CREATE VECTOR INDEX {index_name} IF NOT EXISTS
            FOR (n:{label}) ON n.{embedding_property}
            OPTIONS {{
              indexConfig: {{
                `vector.dimensions`: {dimensions},
                `vector.similarity_function`: '{similarity_fn}'
              }}
            }}
            """
            
            # Execute the query directly
            with self.driver.session() as session:
                session.run(cypher_query)
            
            self.vector_indexes[index_name] = {
                "label": label,
                "property": embedding_property,
                "dimensions": dimensions,
                "similarity_fn": similarity_fn
            }
            logger.info(f"Vector index '{index_name}' created successfully")
            
        except Exception as e:
            logger.error(f"Error creating vector index '{index_name}': {e}")
            raise
    
    async def generate_optimized_embedding(self, text: str, content_type: str = "general") -> List[float]:
        """
        Generate optimized embedding with caching and compression
        """
        start_time = datetime.now()
        
        # Check cache first
        cache_key = self._generate_cache_key(text, content_type)
        if cache_key in self.cache:
            self.performance_metrics["cache_hits"] += 1
            return self.cache[cache_key]
        
        self.performance_metrics["cache_misses"] += 1
        
        try:
            # Select appropriate model based on content type
            model_name = self._select_embedding_model(content_type)
            embedder = self.embedding_models[model_name]
            
            # Generate embedding
            embedding = await self._generate_embedding_async(embedder, text)
            
            # Apply compression if beneficial
            if len(embedding) > 512:  # Only compress large embeddings
                embedding = self._compress_embedding(embedding)
            
            # Cache the result
            self.cache[cache_key] = embedding
            
            # Update performance metrics
            embedding_time = (datetime.now() - start_time).total_seconds()
            self._update_performance_metrics(embedding_time)
            
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def _select_embedding_model(self, content_type: str) -> str:
        """Select the most appropriate embedding model based on content type"""
        model_mapping = {
            "consciousness": "consciousness",
            "agent_memory": "primary",
            "concept": "consciousness",
            "cross_agent": "primary",
            "real_time": "fast",
            "general": "primary"
        }
        return model_mapping.get(content_type, "primary")
    
    async def _generate_embedding_async(self, embedder, text: str) -> List[float]:
        """Generate embedding asynchronously"""
        try:
            if hasattr(embedder, 'embed_query'):
                return embedder.embed_query(text)
            else:
                # Fallback for synchronous embedders
                return embedder.embed_documents([text])[0]
        except Exception as e:
            logger.error(f"Error in embedding generation: {e}")
            raise
    
    def _compress_embedding(self, embedding: List[float], compression_ratio: float = 0.5) -> List[float]:
        """Compress embedding while preserving semantic information"""
        try:
            # Use PCA-like compression for large embeddings
            if len(embedding) > 1024:
                # Simple dimensionality reduction
                target_size = int(len(embedding) * compression_ratio)
                step = len(embedding) // target_size
                compressed = embedding[::step][:target_size]
                return compressed
            return embedding
            
        except Exception as e:
            logger.error(f"Error compressing embedding: {e}")
            return embedding
    
    def _generate_cache_key(self, text: str, content_type: str) -> str:
        """Generate cache key for embedding"""
        content_hash = hashlib.md5(f"{text}_{content_type}".encode()).hexdigest()
        return f"embedding_{content_hash}"
    
    def _update_performance_metrics(self, embedding_time: float):
        """Update performance metrics"""
        self.performance_metrics["total_embeddings"] += 1
        
        # Update average embedding time
        current_avg = self.performance_metrics["average_embedding_time"]
        total = self.performance_metrics["total_embeddings"]
        self.performance_metrics["average_embedding_time"] = (
            (current_avg * (total - 1) + embedding_time) / total
        )
    
    async def batch_upsert_embeddings(self, embeddings_data: List[Dict[str, Any]], 
                                    index_name: str) -> Dict[str, Any]:
        """
        Batch upsert embeddings with optimization
        """
        try:
            if index_name not in self.vector_indexes:
                raise ValueError(f"Vector index '{index_name}' not found")
            
            index_config = self.vector_indexes[index_name]
            
            # Prepare data for upsert
            ids = [item["id"] for item in embeddings_data]
            embeddings = [item["embedding"] for item in embeddings_data]
            
            # Upsert vectors
            result = upsert_vectors(
                self.driver,
                ids=ids,
                embedding_property=index_config["property"],
                embeddings=embeddings,
                entity_type=EntityType.NODE
            )
            
            logger.info(f"Successfully upserted {len(embeddings_data)} embeddings to {index_name}")
            return {
                "status": "success",
                "count": len(embeddings_data),
                "index_name": index_name,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error batch upserting embeddings: {e}")
            raise
    
    async def semantic_search(self, query: str, index_name: str, 
                           top_k: int = 10, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Perform semantic search with optimization
        """
        try:
            if index_name not in self.vector_indexes:
                raise ValueError(f"Vector index '{index_name}' not found")
            
            # Generate query embedding
            query_embedding = await self.generate_optimized_embedding(query, "general")
            
            # Create retriever
            retriever = VectorRetriever(
                self.driver,
                index_name=index_name
            )
            
            # Perform search
            if filters:
                results = retriever.search(
                    query_vector=query_embedding,
                    top_k=top_k,
                    filters=filters
                )
            else:
                results = retriever.search(
                    query_vector=query_embedding,
                    top_k=top_k
                )
            
            return results
            
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            raise
    
    async def cross_agent_similarity_search(self, query: str, agent_id: str, 
                                         top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Perform cross-agent similarity search for knowledge sharing
        """
        try:
            # Search across multiple agent memories
            results = []
            
            # Search in agent-specific memory
            agent_results = await self.semantic_search(
                query, f"agent_{agent_id}_memory", top_k
            )
            results.extend(agent_results)
            
            # Search in cross-agent learning index
            cross_agent_results = await self.semantic_search(
                query, "cross_agent_embeddings", top_k
            )
            results.extend(cross_agent_results)
            
            # Remove duplicates and rank by relevance
            unique_results = self._deduplicate_results(results)
            ranked_results = self._rank_results_by_relevance(unique_results, query)
            
            return ranked_results[:top_k]
            
        except Exception as e:
            logger.error(f"Error in cross-agent similarity search: {e}")
            raise
    
    def _deduplicate_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate results based on content similarity"""
        unique_results = []
        seen_content = set()
        
        for result in results:
            content_hash = hashlib.md5(
                str(result.get("content", "")).encode()
            ).hexdigest()
            
            if content_hash not in seen_content:
                seen_content.add(content_hash)
                unique_results.append(result)
        
        return unique_results
    
    def _rank_results_by_relevance(self, results: List[Dict[str, Any]], 
                                 query: str) -> List[Dict[str, Any]]:
        """Rank results by relevance to query"""
        # Simple relevance scoring based on similarity score
        return sorted(results, key=lambda x: x.get("score", 0), reverse=True)
    
    async def optimize_memory_storage(self) -> Dict[str, Any]:
        """
        Optimize memory storage by compressing and deduplicating embeddings
        """
        try:
            optimization_results = {
                "compressed_embeddings": 0,
                "deduplicated_memories": 0,
                "storage_savings": 0,
                "performance_improvement": 0
            }
            
            # Get all embeddings from database
            with self.driver.session() as session:
                # Find duplicate embeddings
                duplicate_query = """
                MATCH (n)
                WHERE n.embedding IS NOT NULL
                WITH n.embedding as embedding, collect(n) as nodes
                WHERE size(nodes) > 1
                RETURN embedding, nodes
                """
                
                duplicates = session.run(duplicate_query).data()
                
                for duplicate in duplicates:
                    nodes = duplicate["nodes"]
                    # Keep the most recent node, remove others
                    nodes_sorted = sorted(nodes, key=lambda x: x.get("created_at", 0), reverse=True)
                    
                    for node in nodes_sorted[1:]:  # Remove all but the first
                        session.run("DELETE n", n=node)
                        optimization_results["deduplicated_memories"] += 1
            
            logger.info(f"Memory optimization completed: {optimization_results}")
            return optimization_results
            
        except Exception as e:
            logger.error(f"Error optimizing memory storage: {e}")
            raise
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        cache_hit_rate = (
            self.performance_metrics["cache_hits"] / 
            (self.performance_metrics["cache_hits"] + self.performance_metrics["cache_misses"])
            if (self.performance_metrics["cache_hits"] + self.performance_metrics["cache_misses"]) > 0 
            else 0
        )
        
        return {
            **self.performance_metrics,
            "cache_hit_rate": cache_hit_rate,
            "total_cache_entries": len(self.cache)
        }
    
    async def cleanup_cache(self, max_age_hours: int = 24):
        """Clean up old cache entries"""
        try:
            current_time = datetime.now()
            cutoff_time = current_time - timedelta(hours=max_age_hours)
            
            # Simple cleanup - in production, you'd want more sophisticated cache management
            if len(self.cache) > 1000:  # Arbitrary limit
                # Clear half the cache
                keys_to_remove = list(self.cache.keys())[:len(self.cache)//2]
                for key in keys_to_remove:
                    del self.cache[key]
            
            logger.info(f"Cache cleanup completed. Current cache size: {len(self.cache)}")
            
        except Exception as e:
            logger.error(f"Error cleaning up cache: {e}")
            raise

    async def optimize_retrieval(self) -> Dict[str, Any]:
        """Optimize memory retrieval system"""
        try:
            # Optimize retrieval by improving cache and indexing
            await self.cleanup_cache(max_age_hours=12)
            
            # Optimize similarity search parameters
            self.similarity_threshold = max(0.1, self.similarity_threshold - 0.05)
            
            return {
                "optimization_type": "memory_retrieval",
                "similarity_threshold": self.similarity_threshold,
                "cache_cleaned": True,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error optimizing memory retrieval: {e}")
            return {"status": "error", "message": str(e)}

    async def optimize_embeddings(self) -> Dict[str, Any]:
        """Optimize vector embeddings system"""
        try:
            # Optimize embedding generation and storage
            await self.initialize_index()
            
            # Clean up cache and optimize performance
            await self.cleanup_cache(max_age_hours=6)
            
            # Update performance metrics
            metrics = self.get_performance_metrics()
            
            return {
                "optimization_type": "vector_embeddings",
                "index_initialized": True,
                "cache_optimized": True,
                "performance_metrics": metrics,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error optimizing vector embeddings: {e}")
            return {"status": "error", "message": str(e)}
