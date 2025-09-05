"""
Enhanced embedding utilities with Ollama integration and better error handling.
"""
import os
import logging
import requests
import json
from typing import List, Optional, Dict, Any
import numpy as np
from functools import lru_cache

logger = logging.getLogger(__name__)

class EmbeddingManager:
    def __init__(self):
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
        self.default_model = os.getenv("DEFAULT_EMBEDING_MODEL", "nomic-embed-text:latest")
        self.fallback_model = "all-MiniLM-L6-v2"
        self.dimensions = 768  # Updated for larger embedding models
        
        # Try to initialize SentenceTransformers as fallback
        self.sentence_transformer = None
        try:
            from sentence_transformers import SentenceTransformer
            self.sentence_transformer = SentenceTransformer(self.fallback_model)
            logger.info(f"Initialized SentenceTransformer with {self.fallback_model}")
        except ImportError:
            logger.warning("SentenceTransformers not available, using Ollama only")
        except Exception as e:
            logger.warning(f"Failed to initialize SentenceTransformer: {e}")
    
    def _get_ollama_embedding(self, text: str, model: Optional[str] = None) -> Optional[List[float]]:
        """Get embedding from Ollama API."""
        model = model or self.default_model
        
        try:
            response = requests.post(
                f"{self.ollama_base_url}/api/embeddings",
                json={"model": model, "prompt": text},
                timeout=30
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    embedding = data.get("embedding")
                    if embedding and isinstance(embedding, list):
                        return embedding
                    else:
                        logger.error(f"Invalid embedding response from Ollama: {data}")
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse Ollama embedding JSON response: {e}")
                    logger.error(f"Raw embedding response: {response.text[:500]}...")
            else:
                logger.error(f"Ollama embedding request failed: {response.status_code} - {response.text}")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama request failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error getting Ollama embedding: {e}")
        
        return None
    
    def _get_sentence_transformer_embedding(self, text: str) -> Optional[List[float]]:
        """Get embedding from SentenceTransformers."""
        if not self.sentence_transformer:
            return None
        
        try:
            embedding = self.sentence_transformer.encode([text])[0]
            return embedding.tolist()
        except Exception as e:
            logger.error(f"SentenceTransformer embedding failed: {e}")
            return None
    
    @lru_cache(maxsize=1000)
    def get_embedding(self, text: str, model: Optional[str] = None) -> List[float]:
        """
        Get text embedding with fallback strategy:
        1. Try Ollama with specified/default model
        2. Fall back to SentenceTransformers
        3. Return zero vector as last resort
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for embedding")
            return [0.0] * self.dimensions
        
        # Truncate very long texts
        text = text[:8000]  # Most models have token limits
        
        # Try Ollama first
        embedding = self._get_ollama_embedding(text, model)
        if embedding:
            # Update dimensions based on actual embedding
            if len(embedding) != self.dimensions:
                self.dimensions = len(embedding)
                logger.info(f"Updated embedding dimensions to {self.dimensions}")
            return embedding
        
        # Fall back to SentenceTransformers
        embedding = self._get_sentence_transformer_embedding(text)
        if embedding:
            return embedding
        
        # Last resort: zero vector
        logger.warning(f"All embedding methods failed for text: {text[:100]}...")
        return [0.0] * self.dimensions
    
    def get_embeddings_batch(self, texts: List[str], model: Optional[str] = None, 
                           batch_size: int = 32) -> List[List[float]]:
        """Get embeddings for multiple texts efficiently."""
        if not texts:
            return []
        
        embeddings = []
        
        # Process in batches
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = []
            
            for text in batch:
                embedding = self.get_embedding(text, model)
                batch_embeddings.append(embedding)
            
            embeddings.extend(batch_embeddings)
            
            # Log progress for large batches
            if len(texts) > 100 and i % (batch_size * 10) == 0:
                logger.info(f"Processed {i + len(batch)}/{len(texts)} embeddings")
        
        return embeddings
    
    def cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two embeddings."""
        try:
            a_np = np.array(a)
            b_np = np.array(b)
            
            dot_product = np.dot(a_np, b_np)
            norm_a = np.linalg.norm(a_np)
            norm_b = np.linalg.norm(b_np)
            
            if norm_a == 0 or norm_b == 0:
                return 0.0
            
            return float(dot_product / (norm_a * norm_b))
        except Exception as e:
            logger.error(f"Cosine similarity calculation failed: {e}")
            return 0.0
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about available embedding models."""
        info = {
            "default_model": self.default_model,
            "dimensions": self.dimensions,
            "ollama_available": False,
            "sentence_transformer_available": bool(self.sentence_transformer)
        }
        
        # Check Ollama availability
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                info["ollama_available"] = True
                try:
                    models = response.json().get("models", [])
                    info["ollama_models"] = [m.get("name") for m in models]
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse Ollama models JSON response: {e}")
                    info["ollama_models"] = []
        except Exception as e:
            logger.debug(f"Ollama not available: {e}")
        
        return info

# Global instance
embedding_manager = EmbeddingManager()

# Backward compatibility functions
# Backward compatibility functions
def get_embedding(text: str) -> List[float]:
    """Backward compatible embedding function."""
    return embedding_manager.get_embedding(text)

def get_embedding_batch(texts: List[str], batch_size: int = 32) -> List[List[float]]:
    """Batch embedding function for improved performance."""
    return embedding_manager.get_embeddings_batch(texts, batch_size=batch_size)

def vector_search_chunks(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Enhanced vector search with better error handling."""
    # Import here to avoid circular imports and maintain compatibility
    from backend.utils.neo4j import driver
    
    query_embedding = embedding_manager.get_embedding(query)
    
    # Check if we have a valid embedding
    if not query_embedding or all(x == 0.0 for x in query_embedding):
        logger.warning("Invalid query embedding, falling back to text search")
        return _fallback_text_search(query, top_k)
    
    try:
        # Try vector search first
        cypher = """
        CALL db.index.vector.queryNodes('ChunkEmbeddingIndex', $top_k, $embedding) 
        YIELD node, score 
        RETURN node.chunk_id AS chunk_id, node.text AS text, score, 
               id(node) AS chunk_node_id 
        LIMIT $top_k
        """
        
        with driver.session() as session:
            result = session.run(cypher, {"top_k": top_k, "embedding": query_embedding})
            chunks = []
            for record in result:
                chunk = dict(record)
                
                # Get parent document using the same session
                doc_query = """
                MATCH (ch:Chunk) WHERE id(ch) = $chunk_node_id 
                OPTIONAL MATCH (ch)-[:DERIVED_FROM]->(d:Document) 
                RETURN d.document_id AS document_id, d.filename AS filename
                """
                
                doc_result = session.run(doc_query, {"chunk_node_id": chunk["chunk_node_id"]})
                doc_row = doc_result.single()
                if doc_row and doc_row["document_id"]:
                    chunk["document_id"] = doc_row["document_id"]
                    chunk["filename"] = doc_row["filename"]
                
                chunks.append(chunk)
            
            return chunks
        
    except Exception as e:
        logger.error(f"Vector search failed: {e}")
        return _fallback_text_search(query, top_k)

def _fallback_text_search(query: str, top_k: int) -> List[Dict[str, Any]]:
    """Fallback text search when vector search fails."""
    from backend.utils.neo4j import driver
    
    try:
        with driver.session() as session:
            # Try full-text search first if available
            try:
                cypher = """
                CALL db.index.fulltext.queryNodes('memory_text_search', $query) 
                YIELD node, score
                MATCH (node)-[:DERIVED_FROM]->(d:Document)
                RETURN node.chunk_id AS chunk_id, node.text AS text, score,
                       d.document_id AS document_id, d.filename AS filename
                LIMIT $top_k
                """
                
                result = session.run(cypher, {"query": query, "top_k": top_k})
                chunks = [dict(record) for record in result]
                if chunks:
                    return chunks
            except Exception:
                # Full-text search not available, continue to simple search
                pass
            
            # Final fallback: simple text matching
            cypher = """
            MATCH (ch:Chunk)
            WHERE toLower(ch.text) CONTAINS toLower($query)
            OPTIONAL MATCH (ch)-[:DERIVED_FROM]->(d:Document)
            RETURN ch.chunk_id AS chunk_id, ch.text AS text, 0.5 AS score,
                   d.document_id AS document_id, d.filename AS filename
            LIMIT $top_k
            """
            
            result = session.run(cypher, {"query": query, "top_k": top_k})
            return [dict(record) for record in result]
        
    except Exception as e:
        logger.error(f"Fallback text search failed: {e}")
        return []
