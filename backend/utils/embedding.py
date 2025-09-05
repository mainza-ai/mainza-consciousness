"""
Embedding utilities for Mainza agentic backend.
"""
from typing import List
try:
    from sentence_transformers import SentenceTransformer
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
except ImportError:
    embedding_model = None
    # TODO: Add Ollama or other fallback

def get_embedding(text: str) -> List[float]:
    if embedding_model:
        return embedding_model.encode([text])[0].tolist()
    # Fallback: return dummy embedding
    return [0.0] * 384 

def vector_search_chunks(query: str, top_k: int = 5) -> list:
    from backend.utils.neo4j import driver
    query_embedding = get_embedding(query)
    try:
        cypher = (
            "CALL db.index.vector.queryNodes('ChunkEmbeddingIndex', $top_k, $embedding) "
            "YIELD node, score RETURN node.chunk_id AS chunk_id, node.text AS text, score, id(node) AS chunk_node_id LIMIT $top_k"
        )
        with driver.session() as session:
            result = session.run(cypher, {"top_k": top_k, "embedding": query_embedding})
            chunks = []
            for record in result:
                chunk = dict(record)
                # Fetch parent document_id for this chunk
                cypher_doc = (
                    "MATCH (ch:Chunk) WHERE id(ch) = $chunk_node_id "
                    "OPTIONAL MATCH (ch)-[:DERIVED_FROM]->(d:Document) RETURN d.document_id AS document_id LIMIT 1"
                )
                doc_result = session.run(cypher_doc, {"chunk_node_id": chunk["chunk_node_id"]})
                doc_row = doc_result.single()
                if doc_row and doc_row["document_id"]:
                    chunk["document_id"] = doc_row["document_id"]
                chunks.append(chunk)
            return chunks
    except Exception:
        # Fallback: dummy search
        cypher = "MATCH (ch:Chunk) RETURN ch.chunk_id AS chunk_id, ch.text AS text LIMIT $top_k"
        with driver.session() as session:
            result = session.run(cypher, {"top_k": top_k})
            return [dict(record) for record in result] 