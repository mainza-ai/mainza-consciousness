from backend.utils.unified_database_manager import unified_database_manager
from backend.utils.embedding import get_embedding
from backend.models.graphmaster_models import *
from pydantic_ai import RunContext
import logging
import uuid
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# Place all @graphmaster_agent.tool functions here, e.g.:
# @graphmaster_agent.tool
async def cypher_query(ctx: RunContext, cypher: str) -> GraphQueryOutput:
    """Execute Cypher query using unified Neo4j manager with caching and monitoring"""
    start_time = datetime.now()
    try:
        records = await unified_database_manager.execute_query(cypher)
        execution_time = (datetime.now() - start_time).total_seconds()
        logger.debug(f"GraphMaster cypher_query executed in {execution_time:.3f}s")
        return GraphQueryOutput(result={"cypher": cypher, "result": records, "execution_time_ms": round(execution_time * 1000, 2)})
    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds()
        logger.error(f"GraphMaster cypher_query failed after {execution_time:.3f}s: {e}")
        return GraphQueryOutput(result={"cypher": cypher, "error": str(e), "execution_time_ms": round(execution_time * 1000, 2)})

async def run_cypher(ctx: RunContext, cypher: str, parameters: dict = None) -> GraphQueryOutput:
    """Execute parameterized Cypher query using unified Neo4j manager"""
    start_time = datetime.now()
    try:
        records = await unified_database_manager.execute_query(cypher, parameters or {})
        execution_time = (datetime.now() - start_time).total_seconds()
        logger.debug(f"GraphMaster run_cypher executed in {execution_time:.3f}s")
        return GraphQueryOutput(result={"cypher": cypher, "result": records, "execution_time_ms": round(execution_time * 1000, 2)})
    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds()
        logger.error(f"GraphMaster run_cypher failed after {execution_time:.3f}s: {e}")
        return GraphQueryOutput(result={"cypher": cypher, "error": str(e), "execution_time_ms": round(execution_time * 1000, 2)})

async def find_related_concepts(ctx: RunContext, concept_id: str, depth: int = 2) -> GraphQueryOutput:
    # Fix: Neo4j doesn't allow parameter variables in relationship patterns
    # Use f-string formatting for depth parameter (safe since it's an integer)
    cypher = (
        f"MATCH (c:Concept {{concept_id: $concept_id}})-[:RELATES_TO*1..{depth}]-(related:Concept) "
        "RETURN DISTINCT related.concept_id AS concept_id, related.name AS name"
    )
    try:
        records = await unified_database_manager.execute_query(cypher, {"concept_id": concept_id, "depth": depth})
        return GraphQueryOutput(result=records)
    except Exception as e:
        return GraphQueryOutput(result={"error": str(e)})

async def get_user_conversations(ctx: RunContext, user_id: str, limit: int = 10) -> GraphQueryOutput:
    cypher = (
        "MATCH (u:User {user_id: $user_id})<-[:DISCUSSED_IN]-(m:Memory)-[:DISCUSSED_IN]->(c:Conversation) "
        "RETURN DISTINCT c.conversation_id AS conversation_id, c.started_at AS started_at "
        "ORDER BY c.started_at DESC LIMIT $limit"
    )
    try:
        records = await unified_database_manager.execute_query(cypher, {"user_id": user_id, "limit": limit})
        return GraphQueryOutput(result=records)
    except Exception as e:
        return GraphQueryOutput(result={"error": str(e)})

async def get_entity_mentions(ctx: RunContext, entity_id: str) -> GraphQueryOutput:
    cypher = (
        "MATCH (e:Entity {entity_id: $entity_id})<-[:MENTIONS]-(c:Conversation) "
        "RETURN c.conversation_id AS conversation_id, c.started_at AS started_at"
    )
    try:
        records = await unified_database_manager.execute_query(cypher, {"entity_id": entity_id})
        return GraphQueryOutput(result=records)
    except Exception as e:
        return GraphQueryOutput(result={"error": str(e)})

async def get_open_tasks_for_user(ctx: RunContext, user_id: str) -> GraphQueryOutput:
    cypher = (
        "MATCH (u:User {user_id: $user_id})<-[:ASSIGNED_TO]-(t:Task) "
        "WHERE coalesce(t.completed, false) = false "
        "RETURN t"
    )
    try:
        records = await unified_database_manager.execute_query(cypher, {"user_id": user_id})
        return GraphQueryOutput(result=records)
    except Exception as e:
        return GraphQueryOutput(result={"error": str(e)})

async def chunk_document(ctx: RunContext, document_id: str, chunk_size: int = 500) -> GraphQueryOutput:
    cypher_get = "MATCH (d:Document {document_id: $document_id}) RETURN d.text AS text"
    try:
        doc_result = await unified_database_manager.execute_query(cypher_get, {"document_id": document_id})
        if not doc_result or not doc_result[0].get("text"):
            return GraphQueryOutput(result={"error": "Document not found or has no text property"})
        
        text = doc_result[0]["text"]
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        created_chunks = []
        
        for idx, chunk_text in enumerate(chunks):
            chunk_id = f"{document_id}_chunk_{idx}"
            embedding = get_embedding(chunk_text)
            cypher_create = (
                "MATCH (d:Document {document_id: $document_id}) "
                "CREATE (ch:Chunk {chunk_id: $chunk_id, text: $chunk_text, embedding: $embedding})-[:DERIVED_FROM]->(d) "
                "RETURN ch"
            )
            result = await unified_database_manager.execute_query(cypher_create, {
                "document_id": document_id, 
                "chunk_id": chunk_id, 
                "chunk_text": chunk_text, 
                "embedding": embedding
            })
            if result:
                created_chunks.append(result[0]["ch"])
        
        return GraphQueryOutput(result={"chunks_created": len(created_chunks), "chunks": created_chunks})
    except Exception as e:
        return GraphQueryOutput(result={"error": str(e)})

async def analyze_knowledge_gaps(ctx: RunContext, mainza_state_id: str) -> GraphQueryOutput:
    cypher = (
        "MATCH (ms:MainzaState {state_id: $mainza_state_id})-[:NEEDS_TO_LEARN]->(c:Concept) "
        "RETURN c.concept_id AS concept_id, c.name AS name"
    )
    try:
        records = await unified_database_manager.execute_query(cypher, {"mainza_state_id": mainza_state_id})
        return GraphQueryOutput(result=records)
    except Exception as e:
        return GraphQueryOutput(result={"error": str(e)})

async def summarize_conversation(ctx: RunContext, conversation_id: str):
    cypher = (
        "MATCH (m:Memory)-[:DISCUSSED_IN]->(c:Conversation {conversation_id: $conversation_id}) "
        "RETURN m.text AS text ORDER BY m.memory_id"
    )
    try:
        records = await unified_database_manager.execute_query(cypher, {"conversation_id": conversation_id})
        texts = [record["text"] for record in records if record.get("text")]
        summary = "\n".join(texts)
        return {"conversation_id": conversation_id, "summary": summary}
    except Exception as e:
        return {"error": str(e)}

async def find_unresolved_entities(ctx: RunContext):
    cypher = (
        "MATCH (e:Entity)<-[:MENTIONS]-(c:Conversation) "
        "WHERE NOT (e)-[:RELATES_TO]->(:Concept) "
        "RETURN DISTINCT e.entity_id AS entity_id, e.name AS name"
    )
    try:
        records = await unified_database_manager.execute_query(cypher)
        return records
    except Exception as e:
        return {"error": str(e)}

async def suggest_next_steps(ctx: RunContext, user_id: str):
    logging.debug(f"[TOOL] suggest_next_steps called with user_id={user_id}")
    suggestions = []
    unresolved_entities = find_unresolved_entities(ctx)
    logging.debug(f"[TOOL] unresolved_entities: {unresolved_entities}")
    if unresolved_entities and isinstance(unresolved_entities, list) and unresolved_entities:
        for e in unresolved_entities:
            suggestions.append({
                "type": "unresolved_entity",
                "message": f"You mentioned '{e['name']}' but haven't linked it to a concept. Want to explore or define it?",
                "entity": e
            })
    open_tasks = get_open_tasks_for_user(ctx, user_id)
    logging.debug(f"[TOOL] open_tasks: {open_tasks}")
    if open_tasks and isinstance(open_tasks, list) and open_tasks:
        for t in open_tasks:
            suggestions.append({
                "type": "open_task",
                "message": f"You have an open task: '{t.get('description')}'. Mark as done or update?",
                "task": t
            })
    knowledge_gaps = analyze_knowledge_gaps(ctx, mainza_state_id=user_id)
    logging.debug(f"[TOOL] knowledge_gaps: {knowledge_gaps}")
    if knowledge_gaps and isinstance(knowledge_gaps, list) and knowledge_gaps:
        for k in knowledge_gaps:
            suggestions.append({
                "type": "knowledge_gap",
                "message": f"Mainza needs to learn more about '{k['name']}'. Shall we explore this topic?",
                "concept": k
            })
    
    cypher_curiosity = (
        "MATCH (a:Concept), (b:Concept) WHERE a <> b AND NOT (a)-[:RELATES_TO]-(b) "
        "RETURN a.concept_id AS a_id, a.name AS a_name, b.concept_id AS b_id, b.name AS b_name LIMIT 1"
    )
    try:
        curiosity_result = await unified_database_manager.execute_query(cypher_curiosity)
        logging.debug(f"[TOOL] curiosity_result: {curiosity_result}")
        if curiosity_result:
            suggestions.append({
                "type": "curiosity",
                "message": f"Curious about the intersection of '{curiosity_result[0]['a_name']}' and '{curiosity_result[0]['b_name']}'. Want to explore how they relate?",
                "concepts": [
                    {"concept_id": curiosity_result[0]["a_id"], "name": curiosity_result[0]["a_name"]},
                    {"concept_id": curiosity_result[0]["b_id"], "name": curiosity_result[0]["b_name"]}
                ]
            })
    except Exception as e:
        logging.debug(f"[TOOL] curiosity query failed: {e}")
    
    if not suggestions:
        suggestions.append({"type": "none", "message": "No open loops detected. All caught up!"})
    logging.debug(f"[TOOL] Final suggestions: {suggestions}")
    return {"suggestions": suggestions}

async def get_document_usage(ctx: RunContext, document_id: str):
    cypher = (
        "MATCH (d:Document {document_id: $document_id})<-[:MENTIONS]-(c:Conversation) "
        "OPTIONAL MATCH (m:Memory)-[:DERIVED_FROM]->(d) "
        "RETURN c.conversation_id AS conversation_id, m.memory_id AS memory_id, m.text AS memory_text"
    )
    try:
        records = await unified_database_manager.execute_query(cypher, {"document_id": document_id})
        return records
    except Exception as e:
        return {"error": str(e)}

async def get_concept_graph(ctx: RunContext, concept_id: str, depth: int = 2):
    # Fix: Neo4j doesn't allow parameter variables in relationship patterns
    cypher = (
        f"MATCH (c:Concept {{concept_id: $concept_id}})-[r*1..{depth}]-(n) "
        "RETURN c, r, n"
    )
    try:
        records = await unified_database_manager.execute_query(cypher, {"concept_id": concept_id, "depth": depth})
        nodes = set()
        rels = []
        for record in records:
            nodes.add(record["c"])
            nodes.add(record["n"])
            rels.extend(record["r"])
        return {"nodes": list(nodes), "relationships": rels}
    except Exception as e:
        return {"error": str(e)}

async def get_entity_graph(ctx: RunContext, entity_id: str, depth: int = 2):
    # Fix: Neo4j doesn't allow parameter variables in relationship patterns
    cypher = (
        f"MATCH (e:Entity {{entity_id: $entity_id}})-[r*1..{depth}]-(n) "
        "RETURN e, r, n"
    )
    try:
        records = await unified_database_manager.execute_query(cypher, {"entity_id": entity_id, "depth": depth})
        nodes = set()
        rels = []
        for record in records:
            nodes.add(record["e"])
            nodes.add(record["n"])
            rels.extend(record["r"])
        return {"nodes": list(nodes), "relationships": rels}
    except Exception as e:
        return {"error": str(e)}

async def search_concepts_by_keywords(ctx: RunContext, keywords: str, limit: int = 10) -> GraphQueryOutput:
    """
    Search for concepts by keywords using text matching and similarity.
    Returns concepts that match the search terms.
    """
    cypher = (
        "MATCH (c:Concept) "
        "WHERE toLower(c.name) CONTAINS toLower($keywords) "
        "   OR toLower(c.description) CONTAINS toLower($keywords) "
        "RETURN c.concept_id AS concept_id, c.name AS name, c.description AS description "
        "ORDER BY c.name "
        "LIMIT $limit"
    )
    try:
        records = await unified_database_manager.execute_query(cypher, {"keywords": keywords, "limit": limit})
        return GraphQueryOutput(result=records)
    except Exception as e:
        return GraphQueryOutput(result={"error": str(e)})

async def suggest_new_concept(ctx: RunContext, topic: str, description: str = None) -> GraphQueryOutput:
    """
    Suggest creating a new concept for a topic not found in the knowledge graph.
    Returns a structured suggestion for concept creation.
    """
    concept_id = topic.lower().replace(" ", "_").replace("-", "_")
    suggestion = {
        "suggestion_type": "new_concept",
        "concept_id": concept_id,
        "name": topic.title(),
        "description": description or f"Knowledge about {topic}",
        "reason": f"No existing concepts found for '{topic}' in the knowledge graph",
        "action": "Consider adding this concept to expand the knowledge base"
    }
    return GraphQueryOutput(result=suggestion)

async def create_concept(ctx: RunContext, topic: str, description: str = None) -> GraphQueryOutput:
    """
    Actually create a new concept in the knowledge graph.
    """
    concept_id = topic.lower().replace(" ", "_").replace("-", "_")
    concept_name = topic.title()
    
    try:
        # Create the concept directly in Neo4j
        cypher = """
        MERGE (c:Concept {concept_id: $concept_id})
        ON CREATE SET 
            c.name = $name,
            c.description = $description,
            c.created_at = timestamp(),
            c.source = 'graphmaster_agent'
        ON MATCH SET
            c.last_accessed = timestamp()
        RETURN c
        """
        
        result = await unified_database_manager.execute_query(cypher, {
            "concept_id": concept_id,
            "name": concept_name,
            "description": description or f"Knowledge about {topic}"
        })
        
        if result:
            # Extract properties from Neo4j Node object
            created_concept = result[0]["c"]
            concept_properties = dict(created_concept) if hasattr(created_concept, '__dict__') else created_concept
            
            return GraphQueryOutput(result={
                "status": "created",
                "concept_id": concept_properties.get("concept_id", concept_id),
                "name": concept_properties.get("name", concept_name),
                "description": concept_properties.get("description", description or f"Knowledge about {topic}"),
                "message": f"Successfully created concept '{concept_name}'"
            })
        else:
            return GraphQueryOutput(result={"error": "Failed to create concept - no result returned"})
            
    except Exception as e:
        logging.error(f"Failed to create concept: {e}")
        return GraphQueryOutput(result={"error": str(e)})

async def create_memory(ctx: RunContext, text: str, source: str = "user", concept_id: Optional[str] = None) -> CreateMemoryOutput:
    """
    Creates a new Memory node in the graph.
    Optionally links it to an existing Concept node.
    """
    memory_id = str(uuid.uuid4())
    try:
        # Create the memory node
        cypher_create_memory = (
            "CREATE (m:Memory {memory_id: $memory_id, text: $text, source: $source, created_at: timestamp()}) "
            "RETURN m"
        )
        result = await unified_database_manager.execute_query(cypher_create_memory, {
            "memory_id": memory_id, 
            "text": text, 
            "source": source
        })
        created_memory = result[0]["m"]

        linked_concept = None
        # If a concept_id is provided, create the relationship
        if concept_id:
            cypher_link_concept = (
                "MATCH (m:Memory {memory_id: $memory_id}) "
                "MATCH (c:Concept {concept_id: $concept_id}) "
                "CREATE (m)-[:RELATES_TO]->(c) "
                "RETURN c"
            )
            result = await unified_database_manager.execute_query(cypher_link_concept, {
                "memory_id": memory_id, 
                "concept_id": concept_id
            })
            linked_concept = result[0]["c"]

        return CreateMemoryOutput(
            memory_id=created_memory["memory_id"],
            text=created_memory["text"],
            source=created_memory["source"],
            linked_concept_id=linked_concept["concept_id"] if linked_concept else None
        )
    except Exception as e:
        # Basic error handling, consider more specific exceptions
        logging.error(f"Failed to create memory: {e}")
        raise

async def summarize_recent_conversations(ctx: RunContext, user_id: str, limit: int = 5) -> SummarizeRecentConversationsOutput:
    """
    Summarizes recent conversations for a given user, returning an overall summary
    and a list of individual conversation summaries.
    """
    cypher = """
        MATCH (u:User {user_id: $user_id})<-[:DISCUSSED_IN]-(m:Memory)-[:DISCUSSED_IN]->(c:Conversation)
        WITH c, collect(m.text) AS texts, max(coalesce(m.created_at, 0)) AS last_activity
        ORDER BY last_activity DESC
        LIMIT $limit
        RETURN c.conversation_id AS conversation_id, c.started_at as started_at, texts, last_activity
    """
    overall_summary_text = ""
    conversation_summaries = []
    
    try:
        records = await unified_database_manager.execute_query(cypher, {"user_id": user_id, "limit": limit})

        if not records:
            return SummarizeRecentConversationsOutput(summary="No recent conversations found.", conversations=[])

        all_texts = []
        for record in records:
            conv_texts = record.get("texts", [])
            if not conv_texts:
                continue

            all_texts.extend(conv_texts)
            # Create a simple title and preview for each conversation
            title = "Conversation" 
            if len(conv_texts) > 0:
                # A simple heuristic for a title
                title = " ".join(conv_texts[0].split()[:5]) + "..."
            
            conversation_summaries.append(
                ConversationSummary(
                    conversation_id=record["conversation_id"],
                    started_at=str(record["started_at"]) if record["started_at"] else None,
                    title=title,
                )
            )
        
        # Create a simple overall summary
        overall_summary_text = "Here's a summary of what we talked about recently."
        if all_texts:
            full_text = " ".join(all_texts)
            overall_summary_text = " ".join(full_text.split()[:50]) + "..."

        return SummarizeRecentConversationsOutput(
            summary=overall_summary_text,
            conversations=conversation_summaries,
        )
    except Exception as e:
        logging.error(f"Failed to summarize conversations: {e}")
        return SummarizeRecentConversationsOutput(summary="Error summarizing conversations.", conversations=[])
