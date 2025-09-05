"""
Validation and model utility functions for Mainza agentic backend.
Required env vars:
  DEFAULT_OLLAMA_MODEL: Name of the Ollama model to use (e.g. 'llama3', 'mistral', etc.)
  OLLAMA_BASE_URL: Base URL for Ollama server (e.g. 'http://localhost:11434')
"""
import os
import requests

def validate_ollama_model():
    model_name = os.getenv("DEFAULT_OLLAMA_MODEL")
    ollama_base_url = os.getenv("OLLAMA_BASE_URL")
    if not model_name:
        raise RuntimeError("DEFAULT_OLLAMA_MODEL must be set in your .env file.")
    if not ollama_base_url:
        raise RuntimeError("OLLAMA_BASE_URL must be set in your .env file.")
    try:
        resp = requests.get(f'{ollama_base_url}/api/tags', timeout=2)
        resp.raise_for_status()
        tags = resp.json().get('models', [])
        available = [m['name'] for m in tags]
        if model_name not in available:
            raise RuntimeError(
                f"Ollama model '{model_name}' not found.\nAvailable models: {available}\n"
                f"To fix: pull or create the model/tag, or set DEFAULT_OLLAMA_MODEL to one of the above."
            )
    except Exception as e:
        raise RuntimeError(f"Failed to validate Ollama model '{model_name}': {e}")

def coerce_to_model(model_cls, data):
    if isinstance(data, model_cls):
        return data
    if isinstance(data, dict):
        try:
            return model_cls(**data)
        except Exception as e:
            print(f"[DEBUG] coerce_to_model failed: {e}, data={data}")
            return model_cls()
    return model_cls(result=data) if hasattr(model_cls, 'result') else model_cls(details=data) 