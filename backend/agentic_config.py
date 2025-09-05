# Required environment variables:
#   DEFAULT_OLLAMA_MODEL: Name of the Ollama model to use (e.g. 'llama3', 'mistral', etc.)
#   OLLAMA_BASE_URL: Base URL for Ollama server (e.g. 'http://localhost:11434')
#   OPENAI_API_KEY: (optional) API key for OpenAI cloud LLM
#   CLOUD_MODEL: (optional) Model name for cloud LLM (e.g. 'gpt-4-turbo')
import os
from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

# Load environment variables from .env file
load_dotenv()

# --- Local LLM Configuration (Ollama) ---
# The default, privacy-first conversationalist running on a local server.
# pydantic-ai connects to Ollama's OpenAI-compatible endpoint.
DEFAULT_OLLAMA_MODEL = os.getenv("DEFAULT_OLLAMA_MODEL")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")

if not DEFAULT_OLLAMA_MODEL:
    raise RuntimeError("DEFAULT_OLLAMA_MODEL must be set in your .env file (e.g. 'llama3', 'mistral', etc.)")
if not OLLAMA_BASE_URL:
    raise RuntimeError("OLLAMA_BASE_URL must be set in your .env file (e.g. 'http://localhost:11434')")

# The local_llm uses OpenAIModel but is pointed at the local Ollama server.
# Enhanced with Context7 MCP-compliant context optimization
local_llm = OpenAIModel(
    model_name=DEFAULT_OLLAMA_MODEL, 
    provider=OpenAIProvider(base_url=f"{OLLAMA_BASE_URL}/v1")
)

# Import context optimization for enhanced LLM configuration
try:
    from backend.config.llm_optimization import llm_context_optimizer
    
    # Log context optimization status
    context_stats = llm_context_optimizer.get_context_stats()
    if context_stats:
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"🧠 LLM Context Optimization Active:")
        logger.info(f"   📊 Model: {context_stats.get('model_name', 'Unknown')}")
        logger.info(f"   🎯 Max Context: {context_stats.get('max_context_tokens', 0):,} tokens")
        logger.info(f"   ⚡ Optimization: {context_stats.get('optimization_level', 'standard')}")
        logger.info(f"   🧩 Strategy: {context_stats.get('context_strategy', 'basic')}")
        logger.info(f"   📈 Target Utilization: {context_stats.get('context_utilization_target', '80%')}")
        
except ImportError as e:
    import logging
    logging.warning(f"Context optimization not available: {e}")

# --- Cloud LLM Configuration (OpenAI) ---
# For specialized, high-power tasks, Mainza federates requests to the best-in-class cloud models.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CLOUD_MODEL = os.getenv("CLOUD_MODEL")
CLOUD_ENABLED = bool(OPENAI_API_KEY and CLOUD_MODEL)

cloud_llm = None
if CLOUD_ENABLED:
    # The cloud_llm uses the default OpenAIProvider, which points to api.openai.com
    cloud_llm = OpenAIModel(
        model_name=CLOUD_MODEL,
        provider=OpenAIProvider(api_key=OPENAI_API_KEY)
    ) 