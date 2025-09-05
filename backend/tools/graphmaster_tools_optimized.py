"""
Optimized GraphMaster tools with enhanced performance, security, and Context7 compliance.
Addresses critical issues identified in code review:
- Connection pooling and transaction management
- Query optimization and batch operations
- Security improvements for Cypher injection prevention
- Enhanced error handling and monitoring
"""
from backend.utils.neo4j_enhanced import neo4j_manager
from backend.utils.embedding_enhanced import get_embedding_batch, get_embedding
from backend.models.graphmaster_models import *
from pydantic_ai import RunContext
import logging
import uuid
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
import re

logger = logging.getLogger(__name__)

class QueryValidator:
    """Validates Cypher queries for security and performance."""
    
    DANGEROUS_PATTERNS = [
        r'\bDROP\s+DATABASE\b',
        r'\bDELETE\s+ALL\b',
        r'\bDETACH\s+DELETE\s+ALL\b',
        r'\bCREATE\s+DATABASE\b',
        r'\bALTER\s+DATABASE\b',
        r';\s*MATCH',  # Query chaining
        r'LOAD\s+CSV',  # File operations
    ]
    
    @classmethod
    def validate_query(cls, query: str) -> tuple[bool, str]:
        """Validate query for security issues."""
        query_upper = query.upper()
        
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, query_upper, re.IGNORECASE):
                return False, f"Dangerous pattern detected: {pattern}"
        
        # Check for excessive complexity
        if query.count('MATCH') > 10:
            return False, "Query too complex (too many MATCH clauses)"
        
        return True, "Valid"

def cypher_query_secure(ctx: RunContext, cypher: str, parameters: Optional[Dict[str, Any]] = None) -> GraphQueryOutput:
    """
    Secure Cypher query execution with validation, parameterization, and monitoring.
    """
    # Validate query security
    is_valid, validation_msg = QueryValidator.validate_query(cypher)
    if not is_valid:
        logger.warning(f"Query blocked: {validation_msg}")
        return GraphQueryOutput(result={"error": f"Query blocked: {validation_msg}"})
    
    start_time = datetime.now()
    
    try:
        # Use enhanced Neo4j manager with connection pooling
        records = neo4j_manager.execute_query(cypher, parameters)
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return GraphQueryOutput(result={
            "cypher": cypher,
            "result": records,
            "execution_time_ms": round(execution_time * 1000, 2),
            "record_count": len(records)
        })
    except Exception as e:
        logger.error(f"Secure Cypher query failed: {e}")
        return GraphQueryOutput(result={
            "cypher": cypher, 
            "error": str(e),
            "execution_time_ms": round((datetime.now() - start_time).total_seconds() * 1000, 2)
        })

def find_related_concepts_batch(ctx: RunContext, concept_ids: List[str], depth: int = 2, limit: int = 20) -> GraphQueryOutput:
    """
    Batch concept relationship finder - processes multiple concepts in one query.
    """
    # Limit depth and batch size for performance
    depth = min(depth, 3)
    concept_ids = concept_ids[:10]  # Limit batch size
    
    # Fix: Neo4j doesn't allow parameter variables in relationship patterns
    # Fix: Simplify query without CALL subquery to avoid syntax issues
    cypher = f"""
    UNWIND $concept_ids AS concept_id
    MATCH (c:Concept {{concept_id: concept_id}})-[:RELATES_TO*1..{depth}]-(related:Concept)
    WHERE related <> c
    WITH c.concept_id AS source_concept_id,
         related.concept_id AS related_concept_id, 
         related.name AS related_name,
         size((c)-[:RELATES_TO*1..{depth}]-(related)) AS relationship_strength
    ORDER BY source_concept_id, relationship_strength DESC
    LIMIT $limit
    RETURN source_concept_id, related_concept_id, related_name, relationship_strength
    """
    
    try:
        records = neo4j_manager.execute_query(cypher, {
            "concept_ids": concept_ids, 
            "depth": depth, 
            "limit": limit
        })
        return GraphQueryOutput(result=records)
    except Exception as e:
        logger.error(f"Batch find related concepts failed: {e}")
        return GraphQueryOutput(result={"error": str(e)})

def chunk_document_optimized(ctx: RunContext, document_id: str, chunk_size: int = 500, overlap: int = 50) -> GraphQueryOutput:
    """
    Optimized document chunking with sliding window, batch embeddings, and transaction safety.
    """
    try:
        # Get document text
        doc_query = """
        MATCH (d:Document {document_id: $document_id}) 
        RETURN d.text AS text, d.filename AS filename, d.metadata AS metadata
        """
        doc_records = neo4j_manager.execute_query(doc_query, {"document_id": document_id})
        
        if not doc_records or not doc_records[0].get("text"):
            return GraphQueryOutput(result={"error": "Document not found or has no text"})
        
        text = doc_records[0]["text"]
        filename = doc_records[0].get("filename", "unknown")
        metadata = doc_records[0].get("metadata", {})
        
        # Create overlapping chunks for better context preservation
        chunks = []
        chunk_texts = []
        
        start = 0
        chunk_index = 0
        
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end]
            
            chunk_id = f"{document_id}_chunk_{chunk_index}"
            chunks.append({
                "chunk_id": chunk_id,
                "text": chunk_text,
                "position": chunk_index,
                "start_pos": start,
                "end_pos": end,
                "document_id": document_id,
                "created_at": int(datetime.now().timestamp() * 1000)
            })
            chunk_texts.append(chunk_text)
            
            # Move start position with overlap
            start = end - overlap if end < len(text) else end
            chunk_index += 1
        
        # Generate embeddings in batch for efficiency
        logger.info(f"Generating embeddings for {len(chunks)} chunks from {filename}")
        embeddings = get_embedding_batch(chunk_texts)
        
        # Add embeddings to chunks
        for chunk, embedding in zip(chunks, embeddings):
            chunk["embedding"] = embedding
        
        # Batch insert with transaction
        cypher = """
        UNWIND $chunks AS chunk_data
        MATCH (d:Document {document_id: $document_id})
        CREATE (ch:Chunk {
            chunk_id: chunk_data.chunk_id,
            text: chunk_data.text,
            embedding: chunk_data.embedding,
            position: chunk_data.position,
            start_pos: chunk_data.start_pos,
            end_pos: chunk_data.end_pos,
            created_at: chunk_data.created_at
        })-[:DERIVED_FROM]->(d)
        RETURN ch.chunk_id AS chunk_id, ch.position AS position
        """
        
        created_chunks = neo4j_manager.execute_write_query(cypher, {
            "chunks": chunks, 
            "document_id": document_id
        })
        
        logger.info(f"Created {len(created_chunks)} chunks for document {document_id}")
        return GraphQueryOutput(result={
            "chunks_created": len(created_chunks),
            "document_id": document_id,
            "filename": filename,
            "total_text_length": len(text),
            "chunk_size": chunk_size,
            "overlap": overlap,
            "chunks": created_chunks
        })
        
    except Exception as e:
        logger.error(f"Optimized chunk document failed: {e}")
        return GraphQueryOutput(result={"error": str(e)})

def semantic_search_optimized(ctx: RunContext, query_text: str, limit: int = 10, 
                            similarity_threshold: float = 0.7) -> GraphQueryOutput:
    """
    Optimized semantic search using vector index with proper similarity scoring.
    """
    try:
        # Generate query embedding
        query_embedding = get_embedding(query_text)
        
        # Use vector index for efficient similarity search
        cypher = """
        CALL db.index.vector.queryNodes('ChunkEmbeddingIndex', $limit, $query_embedding)
        YIELD node AS chunk, score
        WHERE score >= $similarity_threshold
        MATCH (chunk)-[:DERIVED_FROM]->(d:Document)
        RETURN chunk.chunk_id AS chunk_id,
               chunk.text AS text,
               chunk.position AS position,
               d.document_id AS document_id,
               d.filename AS filename,
               score AS similarity_score
        ORDER BY score DESC
        """
        
        records = neo4j_manager.execute_query(cypher, {
            "query_embedding": query_embedding,
            "limit": limit,
            "similarity_threshold": similarity_threshold
        })
        
        return GraphQueryOutput(result={
            "query": query_text,
            "results": records,
            "similarity_threshold": similarity_threshold
        })
        
    except Exception as e:
        logger.error(f"Semantic search failed: {e}")
        return GraphQueryOutput(result={"error": str(e)})

def get_user_context_optimized(ctx: RunContext, user_id: str, conversation_id: Optional[str] = None, 
                              limit: int = 20) -> GraphQueryOutput:
    """
    Optimized user context retrieval with proper indexing and minimal queries.
    """
    cypher = """
    MATCH (u:User {user_id: $user_id})
    OPTIONAL MATCH (u)<-[:DISCUSSED_IN]-(recent_memories:Memory)
    WHERE ($conversation_id IS NULL OR EXISTS((recent_memories)-[:DISCUSSED_IN]->(:Conversation {conversation_id: $conversation_id})))
    WITH u, recent_memories
    ORDER BY coalesce(recent_memories.created_at, 0) DESC
    LIMIT $limit
    
    OPTIONAL MATCH (u)<-[:DISCUSSED_IN]-(all_memories:Memory)-[:RELATES_TO]->(concepts:Concept)
    
    RETURN {
        user_id: u.user_id,
        name: u.name,
        recent_memories: collect(DISTINCT {
            memory_id: recent_memories.memory_id,
            text: recent_memories.text,
            source: recent_memories.source,
            created_at: recent_memories.created_at
        })[0..$limit],
        related_concepts: collect(DISTINCT {
            concept_id: concepts.concept_id,
            name: concepts.name
        })[0..10]
    } AS user_context
    """
    
    try:
        records = neo4j_manager.execute_query(cypher, {
            "user_id": user_id,
            "conversation_id": conversation_id,
            "limit": limit
        })
        
        return GraphQueryOutput(result=records[0] if records else {"error": "User not found"})
        
    except Exception as e:
        logger.error(f"Get user context failed: {e}")
        return GraphQueryOutput(result={"error": str(e)})

def create_memory_batch(ctx: RunContext, memories: List[Dict[str, Any]]) -> GraphQueryOutput:
    """
    Batch memory creation for improved performance.
    """
    try:
        # Prepare memory data with IDs and timestamps
        processed_memories = []
        for memory_data in memories:
            memory_id = str(uuid.uuid4())
            timestamp = int(datetime.now().timestamp() * 1000)
            
            processed_memories.append({
                "memory_id": memory_id,
                "text": memory_data["text"],
                "source": memory_data.get("source", "user"),
                "user_id": memory_data.get("user_id"),
                "conversation_id": memory_data.get("conversation_id"),
                "concept_id": memory_data.get("concept_id"),
                "created_at": timestamp
            })
        
        # Batch create memories
        cypher = """
        UNWIND $memories AS memory_data
        CREATE (m:Memory {
            memory_id: memory_data.memory_id,
            text: memory_data.text,
            source: memory_data.source,
            created_at: memory_data.created_at
        })
        
        // Link to user if provided
        FOREACH (user_id IN CASE WHEN memory_data.user_id IS NOT NULL THEN [memory_data.user_id] ELSE [] END |
            MERGE (u:User {user_id: user_id})
            CREATE (m)-[:DISCUSSED_IN]->(u)
        )
        
        // Link to conversation if provided
        FOREACH (conv_id IN CASE WHEN memory_data.conversation_id IS NOT NULL THEN [memory_data.conversation_id] ELSE [] END |
            MERGE (c:Conversation {conversation_id: conv_id})
            CREATE (m)-[:DISCUSSED_IN]->(c)
        )
        
        // Link to concept if provided
        FOREACH (concept_id IN CASE WHEN memory_data.concept_id IS NOT NULL THEN [memory_data.concept_id] ELSE [] END |
            MERGE (co:Concept {concept_id: concept_id})
            CREATE (m)-[:RELATES_TO {created_at: memory_data.created_at}]->(co)
        )
        
        RETURN m.memory_id AS memory_id, m.text AS text, m.source AS source
        """
        
        created_memories = neo4j_manager.execute_write_query(cypher, {"memories": processed_memories})
        
        logger.info(f"Created {len(created_memories)} memories in batch")
        return GraphQueryOutput(result={
            "memories_created": len(created_memories),
            "memories": created_memories
        })
        
    except Exception as e:
        logger.error(f"Batch create memories failed: {e}")
        return GraphQueryOutput(result={"error": str(e)})

def analyze_conversation_patterns(ctx: RunContext, user_id: str, days_back: int = 30) -> GraphQueryOutput:
    """
    Analyze conversation patterns and user behavior for insights.
    """
    cutoff_timestamp = int((datetime.now().timestamp() - (days_back * 86400)) * 1000)
    
    cypher = """
    MATCH (u:User {user_id: $user_id})<-[:DISCUSSED_IN]-(m:Memory)
    WHERE m.created_at >= $cutoff_timestamp
    
    OPTIONAL MATCH (m)-[:DISCUSSED_IN]->(c:Conversation)
    OPTIONAL MATCH (m)-[:RELATES_TO]->(concepts:Concept)
    
    WITH u, m, c, concepts,
         CASE 
             WHEN m.created_at >= $cutoff_timestamp - 86400000 THEN 'today'
             WHEN m.created_at >= $cutoff_timestamp - 604800000 THEN 'this_week'
             ELSE 'older'
         END AS time_period
    
    RETURN {
        user_id: u.user_id,
        analysis_period_days: $days_back,
        memory_counts: {
            total: count(DISTINCT m),
            by_period: collect(DISTINCT {period: time_period, count: count(m)})
        },
        conversation_count: count(DISTINCT c),
        top_concepts: collect(DISTINCT concepts.name)[0..10],
        memory_sources: collect(DISTINCT m.source),
        activity_pattern: collect(DISTINCT {
            date: date(datetime({epochMillis: m.created_at})),
            memories: count(m)
        })
    } AS analysis
    """
    
    try:
        records = neo4j_manager.execute_query(cypher, {
            "user_id": user_id,
            "cutoff_timestamp": cutoff_timestamp,
            "days_back": days_back
        })
        
        return GraphQueryOutput(result=records[0] if records else {"error": "No data found"})
        
    except Exception as e:
        logger.error(f"Analyze conversation patterns failed: {e}")
        return GraphQueryOutput(result={"error": str(e)})

def get_system_health_comprehensive(ctx: RunContext) -> GraphQueryOutput:
    """
    Comprehensive system health check with performance metrics and recommendations.
    """
    try:
        # Use the enhanced Neo4j manager's health check
        if not neo4j_manager.health_check():
            return GraphQueryOutput(result={"error": "Neo4j connection failed"})
        
        # Get database info
        db_info = neo4j_manager.get_database_info()
        
        # Additional health metrics
        health_queries = {
            "memory_distribution": """
            MATCH (m:Memory) 
            RETURN m.source AS source, count(m) AS count, 
                   avg(size(m.text)) AS avg_text_length
            ORDER BY count DESC
            """,
            "recent_activity": """
            MATCH (n) 
            WHERE n.created_at IS NOT NULL AND n.created_at > $yesterday
            RETURN labels(n)[0] AS node_type, count(n) AS count
            ORDER BY count DESC
            """,
            "orphaned_chunks": """
            MATCH (ch:Chunk) 
            WHERE NOT (ch)-[:DERIVED_FROM]->(:Document)
            RETURN count(ch) AS orphaned_count
            """,
            "embedding_coverage": """
            MATCH (ch:Chunk) 
            RETURN count(ch) AS total_chunks,
                   count(ch.embedding) AS chunks_with_embeddings,
                   (count(ch.embedding) * 100.0 / count(ch)) AS coverage_percentage
            """
        }
        
        yesterday = int((datetime.now().timestamp() - 86400) * 1000)
        health_metrics = {}
        
        for key, query in health_queries.items():
            try:
                if key == "recent_activity":
                    result = neo4j_manager.execute_query(query, {"yesterday": yesterday})
                else:
                    result = neo4j_manager.execute_query(query)
                health_metrics[key] = result
            except Exception as e:
                logger.warning(f"Health metric {key} failed: {e}")
                health_metrics[key] = {"error": str(e)}
        
        return GraphQueryOutput(result={
            "database_info": db_info,
            "health_metrics": health_metrics,
            "connection_status": "healthy",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"System health check failed: {e}")
        return GraphQueryOutput(result={"error": str(e)})