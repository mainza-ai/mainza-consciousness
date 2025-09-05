"""
Ollama-Native Compatibility Layer
Ensures all systems work in Ollama-native environment without external dependencies
"""
import logging
import os
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class OllamaNativeCompatibility:
    """
    Compatibility layer for Ollama-native environment
    Provides fallbacks for external dependencies
    """
    
    def __init__(self):
        self.redis_available = False
        self.sentence_transformers_available = False
        self.external_apis_available = False
        
        # Check available dependencies
        self._check_dependencies()
        
    def _check_dependencies(self):
        """Check which external dependencies are available"""
        
        # Check Redis
        try:
            import redis
            self.redis_available = True
            logger.info("Redis available for distributed caching")
        except ImportError:
            logger.info("Redis not available - using in-memory caching")
        
        # Check SentenceTransformers
        try:
            import sentence_transformers
            self.sentence_transformers_available = True
            logger.info("SentenceTransformers available for embeddings")
        except ImportError:
            logger.info("SentenceTransformers not available - using Ollama embeddings")
        
        # Log compatibility mode
        if not self.redis_available and not self.sentence_transformers_available:
            logger.info("🚀 Running in full Ollama-native mode")
        else:
            logger.info("🔧 Running in hybrid mode with some external dependencies")
    
    def get_cache_strategy(self) -> str:
        """Get appropriate cache strategy for current environment"""
        if self.redis_available:
            return "redis"
        else:
            return "memory"
    
    def get_embedding_strategy(self) -> str:
        """Get appropriate embedding strategy for current environment"""
        if self.sentence_transformers_available:
            return "sentence_transformers"
        else:
            return "ollama"
    
    def get_compatibility_info(self) -> Dict[str, Any]:
        """Get comprehensive compatibility information"""
        return {
            "mode": "ollama_native" if not (self.redis_available or self.sentence_transformers_available) else "hybrid",
            "redis_available": self.redis_available,
            "sentence_transformers_available": self.sentence_transformers_available,
            "external_apis_available": self.external_apis_available,
            "cache_strategy": self.get_cache_strategy(),
            "embedding_strategy": self.get_embedding_strategy(),
            "recommendations": self._get_recommendations()
        }
    
    def _get_recommendations(self) -> List[str]:
        """Get recommendations for optimal performance"""
        recommendations = []
        
        if not self.redis_available:
            recommendations.append("Consider installing Redis for distributed caching in production")
        
        if not self.sentence_transformers_available:
            recommendations.append("SentenceTransformers not available - using Ollama embeddings (recommended for local deployment)")
        
        if not recommendations:
            recommendations.append("All dependencies available - optimal performance mode")
        
        return recommendations
    
    def ensure_ollama_native_mode(self):
        """Ensure system runs in pure Ollama-native mode"""
        logger.info("🎯 Ensuring pure Ollama-native mode...")
        
        # Set environment variables to disable external dependencies
        os.environ["DISABLE_REDIS"] = "true"
        os.environ["DISABLE_SENTENCE_TRANSFORMERS"] = "true"
        os.environ["OLLAMA_NATIVE_MODE"] = "true"
        
        logger.info("✅ Pure Ollama-native mode enabled")

# Global compatibility instance
ollama_compatibility = OllamaNativeCompatibility()

def is_ollama_native_mode() -> bool:
    """Check if running in pure Ollama-native mode"""
    return os.getenv("OLLAMA_NATIVE_MODE", "false").lower() == "true"

def get_compatibility_info() -> Dict[str, Any]:
    """Get compatibility information"""
    return ollama_compatibility.get_compatibility_info()

def ensure_ollama_native():
    """Ensure pure Ollama-native mode"""
    ollama_compatibility.ensure_ollama_native_mode()

# Auto-detect and log compatibility mode on import
compatibility_info = get_compatibility_info()
logger.info(f"🔧 Compatibility Mode: {compatibility_info['mode']}")
logger.info(f"📊 Cache Strategy: {compatibility_info['cache_strategy']}")
logger.info(f"🔤 Embedding Strategy: {compatibility_info['embedding_strategy']}")

if compatibility_info["recommendations"]:
    for rec in compatibility_info["recommendations"]:
        logger.info(f"💡 {rec}")