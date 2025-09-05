from pydantic_ai import Agent
from backend.models.research_models import ResearchResult
from backend.agentic_config import cloud_llm, CLOUD_ENABLED
from backend.tools.research_tools import search_the_web

# The ResearchAgent is only functional if a cloud LLM is configured.
if CLOUD_ENABLED:
    ResearchAgent = Agent[None, ResearchResult](
        cloud_llm,
        system_prompt="You are a research agent. Use the web to answer questions and return a ResearchResult.",
        tools=[search_the_web],
    )
else:
    # If no cloud model is available, provide a non-functional placeholder.
    # This prevents the application from crashing if the research agent is imported
    # but allows other logic to check for its availability.
    ResearchAgent = None 