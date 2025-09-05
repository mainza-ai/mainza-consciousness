"""
Enhanced GraphMaster tools with improved performance, error handling, and Context7 compliance.
"""
from backend.utils.neo4j import driver
from backend.utils.embedding import get_embedding
from backend.models.graphmaster_models import *
from pydantic_ai import RunContext
import logging
import uuid
from typing import Optional, List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

def cypher_query_enhanced(ctx: RunContext, cypher: str, parameters: Optional[Dict[str, Any]] = None) -> GraphQueryOutput:
    """
    Enhanced Cypher query execution with validation and performance monitoring.
    """
    # Basic query validation
    dangerous_keywords = ['DROP', 'DELETE ALL', 'DETACH DELETE ALL']
    if any(keyword in cypher.upper() for keyword in dangerous_keywords):
        return GraphQueryOutput(result={"error": "Dangerous query detected and blocked"})
    
    start_time = datetime.now()
    
    try:
        with driver.session() as session:
            result = session.run(cypher, parameters or {})
            records = [dict(record) for record in result]
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return GraphQueryOutput(result={
                "cypher": cypher,
                "result": records,
                "execution_time_ms": round(execution_time * 1000, 2),
                "record_count": len(records)
            })
    except Exception as e:
        logger.error(f"Enhanced Cypher query failed: {e}")
        return GraphQueryOutput(result={
            "cypher": cypher, 
            "error": str(e),
            "execution_time_ms": round((datetime.now() - start_time).total_seconds() * 1000, 2)
        })

def find_related_concepts_optimized(ctx: RunContext, concept_id: str, depth: int = 2, limit: int = 20) -> GraphQueryOutput:
    """
    Optimized concept relationship finder with performance improvements.
    """
    # Limit depth to prevent expensive queries
    depth = min(depth, 3)
    
    # Fix: Neo4j doesn't allow parameter variables in relationship patterns
    # Fix: Simplify query without CALL subquery to avoid syntax issues
    cypher = f"""
    MATCH (c:Concept {{concept_id: $concept_id}})-[:RELATES_TO*1..{depth}]-(related:Concept)
    WHERE related <> c
    WITH DISTINCT related.concept_id AS concept_id, 
         related.name AS name,
         size((c)-[:RELATES_TO*1..{depth}]-(related)) AS relationship_strength
    RETURN concept_id, name, relationship_strength
    ORDER BY relationship_strength DESC
    LIMIT $limit
    """
    
    try:
        with driver.session() as session:
            result = session.run(cypher, {
                "concept_id": concept_id, 
                "depth": depth, 
                "limit": limit
            })
            records = [dict(record) for record in result]
            return GraphQueryOutput(result=records)
    except Exception as e:
        logger.error(f"Find related concepts failed: {e}")
        return GraphQueryOutput(result={"error": str(e)})

def chunk_document_batch_optimized(ctx: RunContext, document_id: str, chunk_size: int = 500) -> GraphQueryOutput:
    """
    Optimized document chunking with batch processing and transaction management.
    """
    try:
        with driver.session() as session:
            # Get document in a separate transaction
            doc_query = "MATCH (d:Document {document_id: $document_id}) RETURN d.text AS text, d.filename AS filename"
            doc_result = session.run(doc_query, {"document_id": document_id})
            doc_record = doc_result.single()
            
            if not doc_record or not doc_record.get("text"):
                return GraphQueryOutput(result={"error": "Document not found or has no text property"})
            
            text = doc_record["text"]
            filename = doc_record.get("filename", "unknown")
            
            # Create chunks with embeddings
            chunks = []
            chunk_texts = []
            
            for i in range(0, len(text), chunk_size):
                chunk_text = text[i:i + chunk_size]
                chunk_id = f"{document_id}_chunk_{len(chunks)}"
                chunks.append({
                    "chunk_id": chunk_id,
                    "text": chunk_text,
                    "position": len(chunks),
                    "document_id": document_id,
                    "created_at": int(datetime.now().timestamp() * 1000)
                })
                chunk_texts.append(chunk_text)
            
            # Generate embeddings in batch (more efficient)
            logger.info(f"Generating embeddings for {len(chunks)} chunks from {filename}")
            embeddings = []
            for chunk_text in chunk_texts:
                embedding = get_embedding(chunk_text)
                embeddings.append(embedding)
            
            # Add embeddings to chunks
            for chunk, embedding in zip(chunks, embeddings):
                chunk["embedding"] = embedding
            
            # Batch insert with transaction
            with session.begin_transaction() as tx:
                cypher = """
                UNWIND $chunks AS chunk_data
                MATCH (d:Document {document_id: $document_id})
                CREATE (ch:Chunk {
                    chunk_id: chunk_data.chunk_id,
                    text: chunk_data.text,
                    embedding: chunk_data.embedding,
                    position: chunk_data.position,
                    created_at: chunk_data.created_at
                })-[:DERIVED_FROM]->(d)
                RETURN ch.chunk_id AS chunk_id, ch.position AS position
                """
                
                result = tx.run(cypher, {"chunks": chunks, "document_id": document_id})
                created_chunks = [dict(record) for record in result]
            
            logger.info(f"Created {len(created_chunks)} chunks for document {document_id}")
            return GraphQueryOutput(result={
                "chunks_created": len(created_chunks),
                "document_id": document_id,
                "filename": filename,
                "chunks": created_chunks
            })
            
    except Exception as e:
        logger.error(f"Batch chunk document failed: {e}")
        return GraphQueryOutput(result={"error": str(e)})

def get_user_conversations_optimized(ctx: RunContext, user_id: str, limit: int = 10) -> GraphQueryOutput:
    """
    Optimized user conversation retrieval with proper indexing and sorting.
    """
    cypher = """
    MATCH (u:User {user_id: $user_id})<-[:DISCUSSED_IN]-(m:Memory)-[:DISCUSSED_IN]->(c:Conversation)
    WITH c, count(m) AS memory_count, 
         max(coalesce(m.created_at, c.started_at, 0)) AS last_activity
    RETURN DISTINCT c.conversation_id AS conversation_id,
           c.started_at AS started_at,
           memory_count,
           last_activity
    ORDER BY last_activity DESC
    LIMIT $limit
    """
    
    try:
        with driver.session() as session:
            result = session.run(cypher, {"user_id": user_id, "limit": limit})
            records = [dict(record) for record in result]
            return GraphQueryOutput(result=records)
    except Exception as e:
        logger.error(f"Get user conversations failed: {e}")
        return GraphQueryOutput(result={"error": str(e)})

def create_memory_with_transaction(ctx: RunContext, text: str, source: str = "user", 
                                 concept_id: Optional[str] = None, 
                                 user_id: Optional[str] = None,
                                 conversation_id: Optional[str] = None) -> CreateMemoryOutput:
    """
    Enhanced memory creation with proper transaction management and validation.
    """
    memory_id = str(uuid.uuid4())
    timestamp = int(datetime.now().timestamp() * 1000)
    
    try:
        with driver.session() as session:
            with session.begin_transaction() as tx:
                # Create memory node
                memory_query = """
                CREATE (m:Memory {
                    memory_id: $memory_id,
                    text: $text,
                    source: $source,
                    created_at: $created_at
                })
                RETURN m
                """
                
                tx.run(memory_query, {
                    "memory_id": memory_id,
                    "text": text,
                    "source": source,
                    "created_at": timestamp
                })
                
                # Link to concept if provided
                linked_concept_id = None
                if concept_id:
                    concept_query = """
                    MATCH (m:Memory {memory_id: $memory_id})
                    MATCH (c:Concept {concept_id: $concept_id})
                    CREATE (m)-[:RELATES_TO {created_at: $created_at}]->(c)
                    RETURN c.concept_id AS concept_id
                    """
                    
                    result = tx.run(concept_query, {
                        "memory_id": memory_id,
                        "concept_id": concept_id,
                        "created_at": timestamp
                    })
                    
                    record = result.single()
                    if record:
                        linked_concept_id = record["concept_id"]
                
                # Link to user if provided
                if user_id:
                    user_query = """
                    MATCH (m:Memory {memory_id: $memory_id})
                    MATCH (u:User {user_id: $user_id})
                    CREATE (m)-[:DISCUSSED_IN]->(u)
                    """
                    tx.run(user_query, {"memory_id": memory_id, "user_id": user_id})
                
                # Link to conversation if provided
                if conversation_id:
                    conv_query = """
                    MATCH (m:Memory {memory_id: $memory_id})
                    MATCH (c:Conversation {conversation_id: $conversation_id})
                    CREATE (m)-[:DISCUSSED_IN]->(c)
                    """
                    tx.run(conv_query, {"memory_id": memory_id, "conversation_id": conversation_id})
        
        logger.info(f"Created memory {memory_id} with source {source}")
        return CreateMemoryOutput(
            memory_id=memory_id,
            text=text,
            source=source,
            linked_concept_id=linked_concept_id
        )
        
    except Exception as e:
        logger.error(f"Create memory with transaction failed: {e}")
        raise

def analyze_knowledge_gaps_with_scoring(ctx: RunContext, mainza_state_id: str) -> GraphQueryOutput:
    """
    Enhanced knowledge gap analysis with priority scoring and recommendations.
    """
    cypher = """
    MATCH (ms:MainzaState {state_id: $mainza_state_id})-[:NEEDS_TO_LEARN]->(c:Concept)
    OPTIONAL MATCH (c)<-[:RELATES_TO]-(related:Concept)
    OPTIONAL MATCH (c)<-[:MENTIONS]-(conv:Conversation)
    OPTIONAL MATCH (c)<-[:RELATES_TO]-(mem:Memory)
    WITH c, 
         count(DISTINCT related) AS related_count,
         count(DISTINCT conv) AS mention_count,
         count(DISTINCT mem) AS memory_count,
         coalesce(c.priority, 0) AS priority
    RETURN c.concept_id AS concept_id,
           c.name AS name,
           related_count,
           mention_count,
           memory_count,
           priority,
           (related_count * 2 + mention_count + memory_count + priority) AS urgency_score
    ORDER BY urgency_score DESC
    """
    
    try:
        with driver.session() as session:
            result = session.run(cypher, {"mainza_state_id": mainza_state_id})
            records = [dict(record) for record in result]
            return GraphQueryOutput(result=records)
    except Exception as e:
        logger.error(f"Analyze knowledge gaps with scoring failed: {e}")
        return GraphQueryOutput(result={"error": str(e)})

def get_graph_health_metrics(ctx: RunContext) -> GraphQueryOutput:
    """
    Get comprehensive graph health and statistics for monitoring.
    """
    queries = {
        "node_counts": """
        MATCH (n) 
        RETURN labels(n)[0] AS label, count(n) AS count 
        ORDER BY count DESC
        """,
        "relationship_counts": """
        MATCH ()-[r]->() 
        RETURN type(r) AS relationship_type, count(r) AS count 
        ORDER BY count DESC
        """,
        "recent_activity": """
        MATCH (n) 
        WHERE n.created_at IS NOT NULL AND n.created_at > $yesterday
        RETURN labels(n)[0] AS label, count(n) AS count
        ORDER BY count DESC
        """,
        "orphaned_data": """
        MATCH (ch:Chunk) 
        WHERE NOT (ch)-[:DERIVED_FROM]->(:Document)
        RETURN count(ch) AS orphaned_chunks
        """,
        "memory_sources": """
        MATCH (m:Memory) 
        WHERE m.source IS NOT NULL
        RETURN m.source AS source, count(m) AS count 
        ORDER BY count DESC
        """
    }
    
    try:
        yesterday = int((datetime.now().timestamp() - 86400) * 1000)  # 24 hours ago
        stats = {}
        
        with driver.session() as session:
            for key, query in queries.items():
                if key == "recent_activity":
                    result = session.run(query, {"yesterday": yesterday})
                else:
                    result = session.run(query)
                stats[key] = [dict(record) for record in result]
        
        return GraphQueryOutput(result=stats)
    except Exception as e:
        logger.error(f"Get graph health metrics failed: {e}")
        return GraphQueryOutput(result={"error": str(e)})