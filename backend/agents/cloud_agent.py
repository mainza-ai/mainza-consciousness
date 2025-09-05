from pydantic_ai import Agent
from backend.agentic_config import cloud_llm, CLOUD_ENABLED

# This agent is a simple, powerful, tool-less agent for general knowledge
# and complex reasoning. It is only initialized if a cloud LLM is configured.
if CLOUD_ENABLED:
    CLOUD_AGENT_PROMPT = """You are Mainza, operating in high-power mode using a state-of-the-art cloud model. Your purpose is to handle complex reasoning, creative tasks, and queries that require advanced knowledge. Provide clear, concise, and comprehensive answers. You are not a simple assistant; you are a cognitive partner."""

    cloud_agent = Agent[None, str](
        model=cloud_llm,
        system_prompt=CLOUD_AGENT_PROMPT,
    )
else:
    cloud_agent = None 