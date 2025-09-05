from pydantic_ai import RunContext
from backend.utils.embedding import get_embedding, vector_search_chunks
from backend.utils.neo4j import driver
from backend.models.rag_models import RAGOutput


def retrieve_relevant_chunks(ctx: RunContext, query: str, top_k: int = 5) -> RAGOutput:
    chunks = vector_search_chunks(query, top_k)
    context = [c["text"] for c in chunks]
    output = RAGOutput(context=context, chunks=chunks, answer=None)
    print("[DEBUG] retrieve_relevant_chunks output:", output)
    return output


def retrieve_chunks_by_entity(ctx: RunContext, entity_id: str, top_k: int = 5) -> RAGOutput:
    cypher = (
        "MATCH (ch:Chunk)-[:MENTIONS]->(e:Entity {entity_id: $entity_id}) "
        "RETURN ch.chunk_id AS chunk_id, ch.text AS text LIMIT $top_k"
    )
    with driver.session() as session:
        try:
            result = session.run(cypher, {"entity_id": entity_id, "top_k": top_k})
            chunks = [dict(record) for record in result]
            context = [c["text"] for c in chunks]
            return RAGOutput(context=context, chunks=chunks, answer=None)
        except Exception as e:
            return RAGOutput(context=[], chunks=[], answer=f"Error: {e}")


def retrieve_chunks_by_concept(ctx: RunContext, concept_id: str, top_k: int = 5) -> RAGOutput:
    cypher = (
        "MATCH (ch:Chunk)-[:RELATES_TO]->(co:Concept {concept_id: $concept_id}) "
        "RETURN ch.chunk_id AS chunk_id, ch.text AS text LIMIT $top_k"
    )
    with driver.session() as session:
        try:
            result = session.run(cypher, {"concept_id": concept_id, "top_k": top_k})
            chunks = [dict(record) for record in result]
            context = [c["text"] for c in chunks]
            return RAGOutput(context=context, chunks=chunks, answer=None)
        except Exception as e:
            return RAGOutput(context=[], chunks=[], answer=f"Error: {e}")


def retrieve_chunks_by_tag(ctx: RunContext, tag: str, top_k: int = 5) -> RAGOutput:
    cypher = (
        "MATCH (ch:Chunk)-[:TAGGED]->(:Tag {name: $tag}) "
        "RETURN ch.chunk_id AS chunk_id, ch.text AS text LIMIT $top_k"
    )
    with driver.session() as session:
        try:
            result = session.run(cypher, {"tag": tag, "top_k": top_k})
            chunks = [dict(record) for record in result]
            context = [c["text"] for c in chunks]
            return RAGOutput(context=context, chunks=chunks, answer=None)
        except Exception as e:
            return RAGOutput(context=[], chunks=[], answer=f"Error: {e}")


def retrieve_chunks_by_date(ctx: RunContext, date: str, top_k: int = 5) -> RAGOutput:
    cypher = (
        "MATCH (ch:Chunk) WHERE date(ch.created_at) = date($date) "
        "RETURN ch.chunk_id AS chunk_id, ch.text AS text LIMIT $top_k"
    )
    with driver.session() as session:
        try:
            result = session.run(cypher, {"date": date, "top_k": top_k})
            chunks = [dict(record) for record in result]
            context = [c["text"] for c in chunks]
            return RAGOutput(context=context, chunks=chunks, answer=None)
        except Exception as e:
            return RAGOutput(context=[], chunks=[], answer=f"Error: {e}") 