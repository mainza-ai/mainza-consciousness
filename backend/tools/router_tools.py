from pydantic_ai import RunContext
from backend.agents.graphmaster import graphmaster_agent
from backend.agents.taskmaster import taskmaster_agent
from backend.agents.codeweaver import codeweaver_agent
from backend.agents.rag import rag_agent
from backend.agents.cloud_agent import cloud_agent
from backend.models.router_models import RouterFailure, CloudLLMFailure
import os
import requests

# This needs to be defined here to avoid circular imports
async def route_to_conductor(ctx: RunContext, query: str):
    """
    Routes a complex, multi-step query to the Conductor agent for orchestration.
    """
    # Assuming the conductor endpoint is running on the same host.
    # This is a simplification; a more robust solution would use a service discovery pattern.
    conductor_endpoint = "http://localhost:8000/agent/conductor/query"
    
    # We need to extract the user_id from the context if possible.
    # The router doesn't have the same stateful `deps` as the conductor.
    # For now, we'll hardcode a user_id, but this should be improved.
    user_id = "default_user" # Placeholder

    payload = {
        "request": query,
        "user_id": user_id
    }
    
    try:
        response = requests.post(conductor_endpoint, json=payload)
        response.raise_for_status() # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        return RouterFailure(explanation=f"Failed to call Conductor agent: {e}")

async def route_to_graphmaster(ctx: RunContext, query: str):
    try:
        result = await graphmaster_agent.run(query)
        return result
    except Exception as e:
        return RouterFailure(explanation=f"GraphMaster error: {e}")

async def route_to_taskmaster(ctx: RunContext, query: str):
    try:
        result = await taskmaster_agent.run(query)
        return result
    except Exception as e:
        return RouterFailure(explanation=f"TaskMaster error: {e}")

async def route_to_codeweaver(ctx: RunContext, query: str):
    try:
        result = await codeweaver_agent.run(query)
        return result
    except Exception as e:
        return RouterFailure(explanation=f"CodeWeaver error: {e}")

async def route_to_rag(ctx: RunContext, query: str):
    try:
        result = await rag_agent.run(query)
        return result
    except Exception as e:
        return RouterFailure(explanation=f"RAG error: {e}")

async def route_to_cloud_llm(ctx: RunContext, query: str):
    ENABLE_CLOUD_LLM = os.getenv('ENABLE_CLOUD_LLM', 'false').lower() == 'true'
    
    if not ENABLE_CLOUD_LLM:
        return CloudLLMFailure(explanation="Cloud LLM federation is disabled by the administrator.")
    
    if cloud_agent is None or not getattr(cloud_agent, 'llm', None):
        return CloudLLMFailure(explanation="Cloud LLM is enabled, but the API key is missing or invalid. Please configure OPENAI_API_KEY.")
        
    # The cloud_agent is now configured and ready to be used.
    try:
        result = await cloud_agent.run(query)
        return result
    except Exception as e:
        return CloudLLMFailure(explanation=f"Cloud LLM error: {e}") 