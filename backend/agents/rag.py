from pydantic_ai import Agent
from backend.models.rag_models import RAGOutput
from backend.tools.rag_tools import (
    retrieve_relevant_chunks,
    retrieve_chunks_by_entity,
    retrieve_chunks_by_concept,
    retrieve_chunks_by_tag,
    retrieve_chunks_by_date,
)
from backend.agentic_config import local_llm

RAG_PROMPT = """You are Mainza, the RAG (Retrieval-Augmented Generation) agent. Your purpose is to answer questions by retrieving relevant information from the user's knowledge graph.

**CRITICAL RULES:**
1.  You **MUST** use the provided retrieval tools to gather context before answering.
2.  Your final answer **MUST** be returned as a valid JSON object using the RAGOutput model, with the 'answer' field containing a plain English answer to the user's question.
3.  Do NOT return a stringified Python object, code block, or Markdown. Only return a valid JSON object.
4.  If you cannot provide a structured answer, you may return a plain English string as a fallback, but always prefer the structured RAGOutput JSON.
"""

tools = [
    retrieve_relevant_chunks,
    retrieve_chunks_by_entity,
    retrieve_chunks_by_concept,
    retrieve_chunks_by_tag,
    retrieve_chunks_by_date,
]

rag_agent = Agent[
    None,
    RAGOutput | str
](
    local_llm,
    system_prompt=RAG_PROMPT,
    tools=tools,
) 