"""
Production-ready configuration management system.
Addresses critical issue: Hard-coded values in agentic_config.py
Provides environment-based configuration with validation and type safety.
"""
import os
import logging
from typing import Dict, Any, Optional, List, Union
from pydantic import BaseSettings, Field, validator
from enum import Enum
import json

logger = logging.getLogger(__name__)

class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"

class Neo4jConfig(BaseSettings):
    """Neo4j database configuration."""
    
    uri: str = Field(default="bolt://localhost:7687", env="NEO4J_URI")
    user: str = Field(default="neo4j", env="NEO4J_USER")
    password: str = Field(env="NEO4J_PASSWORD")  # Required - no default for security
    database: str = Field(default="neo4j", env="NEO4J_DATABASE")
    
    # Connection pool settings
    max_connection_lifetime: int = Field(default=1800, env="NEO4J_MAX_CONNECTION_LIFETIME")  # 30 minutes
    max_connection_pool_size: int = Field(default=50, env="NEO4J_MAX_CONNECTION_POOL_SIZE")
    connection_acquisition_timeout: int = Field(default=60, env="NEO4J_CONNECTION_ACQUISITION_TIMEOUT")
    connection_timeout: int = Field(default=30, env="NEO4J_CONNECTION_TIMEOUT")
    
    # Security settings
    encrypted: bool = Field(default=False, env="NEO4J_ENCRYPTED")
    trust: str = Field(default="TRUST_ALL_CERTIFICATES", env="NEO4J_TRUST")
    
    # Performance settings
    slow_query_threshold: float = Field(default=1.0, env="NEO4J_SLOW_QUERY_THRESHOLD")
    circuit_breaker_threshold: int = Field(default=5, env="NEO4J_CIRCUIT_BREAKER_THRESHOLD")
    circuit_breaker_timeout: int = Field(default=60, env="NEO4J_CIRCUIT_BREAKER_TIMEOUT")
    
    # Monitoring settings
    monitoring_enabled: bool = Field(default=True, env="NEO4J_MONITORING_ENABLED")
    metrics_retention_hours: int = Field(default=168, env="NEO4J_METRICS_RETENTION_HOURS")  # 1 week
    
    @validator('uri')
    def validate_uri(cls, v):
        if not v.startswith(('bolt://', 'neo4j://', 'bolt+s://', 'neo4j+s://')):
            raise ValueError('Neo4j URI must start with bolt://, neo4j://, bolt+s://, or neo4j+s://')
        return v

class EmbeddingConfig(BaseSettings):
    """Embedding service configuration."""
    
    # Ollama settings
    ollama_base_url: str = Field(default="http://localhost:11434", env="OLLAMA_BASE_URL")
    default_model: str = Field(default="nomic-embed-text:latest", env="DEFAULT_EMBEDDING_MODEL")
    fallback_model: str = Field(default="all-MiniLM-L6-v2", env="FALLBACK_EMBEDDING_MODEL")
    
    # Performance settings
    batch_size: int = Field(default=32, env="EMBEDDING_BATCH_SIZE")
    timeout: int = Field(default=30, env="EMBEDDING_TIMEOUT")
    max_text_length: int = Field(default=8000, env="EMBEDDING_MAX_TEXT_LENGTH")
    
    # Cache settings
    cache_enabled: bool = Field(default=True, env="EMBEDDING_CACHE_ENABLED")
    cache_size: int = Field(default=1000, env="EMBEDDING_CACHE_SIZE")
    
    # Vector search settings
    default_similarity_threshold: float = Field(default=0.7, env="VECTOR_SIMILARITY_THRESHOLD")
    default_top_k: int = Field(default=10, env="VECTOR_DEFAULT_TOP_K")

class AgentConfig(BaseSettings):
    """Agent system configuration."""
    
    # Agent behavior settings
    max_iterations: int = Field(default=10, env="AGENT_MAX_ITERATIONS")
    timeout: int = Field(default=300, env="AGENT_TIMEOUT")  # 5 minutes
    retry_attempts: int = Field(default=3, env="AGENT_RETRY_ATTEMPTS")
    
    # Memory settings
    max_memory_items: int = Field(default=1000, env="AGENT_MAX_MEMORY_ITEMS")
    memory_cleanup_threshold: int = Field(default=800, env="AGENT_MEMORY_CLEANUP_THRESHOLD")
    
    # Tool settings
    tool_timeout: int = Field(default=60, env="AGENT_TOOL_TIMEOUT")
    max_tool_calls: int = Field(default=20, env="AGENT_MAX_TOOL_CALLS")
    
    # Workflow settings
    workflow_enabled: bool = Field(default=True, env="AGENT_WORKFLOW_ENABLED")
    parallel_execution: bool = Field(default=True, env="AGENT_PARALLEL_EXECUTION")

class SecurityConfig(BaseSettings):
    """Security configuration."""
    
    # Authentication
    admin_token: str = Field(default="admin-secret-token", env="ADMIN_TOKEN")
    jwt_secret: str = Field(default="your-secret-key", env="JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_expiration: int = Field(default=3600, env="JWT_EXPIRATION")  # 1 hour
    
    # API security
    rate_limit_enabled: bool = Field(default=True, env="RATE_LIMIT_ENABLED")
    rate_limit_requests: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=60, env="RATE_LIMIT_WINDOW")  # 1 minute
    
    # Query security
    query_validation_enabled: bool = Field(default=True, env="QUERY_VALIDATION_ENABLED")
    max_query_length: int = Field(default=10000, env="MAX_QUERY_LENGTH")
    max_query_complexity: int = Field(default=10, env="MAX_QUERY_COMPLEXITY")
    
    # CORS settings
    cors_origins: List[str] = Field(default=["http://localhost:3000"], env="CORS_ORIGINS")
    cors_credentials: bool = Field(default=True, env="CORS_CREDENTIALS")

class ApplicationConfig(BaseSettings):
    """Main application configuration."""
    
    # Environment
    environment: EnvironmentType = Field(default=EnvironmentType.DEVELOPMENT, env="ENVIRONMENT")
    debug: bool = Field(default=True, env="DEBUG")
    log_level: LogLevel = Field(default=LogLevel.INFO, env="LOG_LEVEL")
    
    # Server settings
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    workers: int = Field(default=1, env="WORKERS")
    
    # API settings
    api_prefix: str = Field(default="/api/v1", env="API_PREFIX")
    docs_url: Optional[str] = Field(default="/docs", env="DOCS_URL")
    redoc_url: Optional[str] = Field(default="/redoc", env="REDOC_URL")
    
    # Performance settings
    request_timeout: int = Field(default=300, env="REQUEST_TIMEOUT")  # 5 minutes
    max_request_size: int = Field(default=16777216, env="MAX_REQUEST_SIZE")  # 16MB
    
    # Feature flags
    monitoring_enabled: bool = Field(default=True, env="MONITORING_ENABLED")
    metrics_enabled: bool = Field(default=True, env="METRICS_ENABLED")
    health_checks_enabled: bool = Field(default=True, env="HEALTH_CHECKS_ENABLED")
    
    @validator('cors_origins', pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v

class ProductionConfig:
    """Main configuration class that combines all config sections."""
    
    def __init__(self):
        self.app = ApplicationConfig()
        self.neo4j = Neo4jConfig()
        self.embedding = EmbeddingConfig()
        self.agent = AgentConfig()
        self.security = SecurityConfig()
        
        # Validate configuration
        self._validate_config()
        
        # Log configuration summary
        self._log_config_summary()
    
    def _validate_config(self):
        """Validate configuration consistency."""
        errors = []
        
        # Environment-specific validations
        if self.app.environment == EnvironmentType.PRODUCTION:
            if self.app.debug:
                errors.append("Debug mode should be disabled in production")
            
            if self.security.admin_token == "admin-secret-token":
                errors.append("Default admin token should be changed in production")
            
            if self.security.jwt_secret == "your-secret-key":
                errors.append("Default JWT secret should be changed in production")
            
            if not self.neo4j.encrypted:
                logger.warning("Neo4j encryption is disabled in production")
        
        # Neo4j validations
        if self.neo4j.max_connection_pool_size < 1:
            errors.append("Neo4j connection pool size must be at least 1")
        
        if self.neo4j.slow_query_threshold <= 0:
            errors.append("Neo4j slow query threshold must be positive")
        
        # Embedding validations
        if self.embedding.batch_size < 1:
            errors.append("Embedding batch size must be at least 1")
        
        if self.embedding.default_similarity_threshold < 0 or self.embedding.default_similarity_threshold > 1:
            errors.append("Similarity threshold must be between 0 and 1")
        
        # Agent validations
        if self.agent.max_iterations < 1:
            errors.append("Agent max iterations must be at least 1")
        
        if self.agent.timeout <= 0:
            errors.append("Agent timeout must be positive")
        
        if errors:
            error_msg = "Configuration validation failed:\n" + "\n".join(f"- {error}" for error in errors)
            raise ValueError(error_msg)
    
    def _log_config_summary(self):
        """Log configuration summary."""
        logger.info(f"Configuration loaded for environment: {self.app.environment}")
        logger.info(f"Debug mode: {self.app.debug}")
        logger.info(f"Log level: {self.app.log_level}")
        logger.info(f"Neo4j URI: {self.neo4j.uri}")
        logger.info(f"Embedding model: {self.embedding.default_model}")
        logger.info(f"Monitoring enabled: {self.app.monitoring_enabled}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary (excluding sensitive data)."""
        return {
            "app": {
                "environment": self.app.environment,
                "debug": self.app.debug,
                "log_level": self.app.log_level,
                "host": self.app.host,
                "port": self.app.port,
                "monitoring_enabled": self.app.monitoring_enabled
            },
            "neo4j": {
                "uri": self.neo4j.uri,
                "database": self.neo4j.database,
                "encrypted": self.neo4j.encrypted,
                "monitoring_enabled": self.neo4j.monitoring_enabled,
                "max_connection_pool_size": self.neo4j.max_connection_pool_size
            },
            "embedding": {
                "default_model": self.embedding.default_model,
                "batch_size": self.embedding.batch_size,
                "cache_enabled": self.embedding.cache_enabled
            },
            "agent": {
                "max_iterations": self.agent.max_iterations,
                "workflow_enabled": self.agent.workflow_enabled,
                "parallel_execution": self.agent.parallel_execution
            },
            "security": {
                "rate_limit_enabled": self.security.rate_limit_enabled,
                "query_validation_enabled": self.security.query_validation_enabled,
                "cors_origins": self.security.cors_origins
            }
        }
    
    def export_env_template(self) -> str:
        """Export environment variable template."""
        template = """# Mainza Production Configuration Template
# Copy this file to .env and customize the values

# Application Settings
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000

# Neo4j Database Settings
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-secure-password
NEO4J_DATABASE=neo4j
NEO4J_ENCRYPTED=true
NEO4J_MAX_CONNECTION_POOL_SIZE=50
NEO4J_MONITORING_ENABLED=true

# Embedding Service Settings
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_EMBEDDING_MODEL=nomic-embed-text:latest
EMBEDDING_BATCH_SIZE=32
EMBEDDING_CACHE_ENABLED=true

# Agent System Settings
AGENT_MAX_ITERATIONS=10
AGENT_TIMEOUT=300
AGENT_WORKFLOW_ENABLED=true

# Security Settings
ADMIN_TOKEN=your-secure-admin-token
JWT_SECRET=your-secure-jwt-secret
RATE_LIMIT_ENABLED=true
QUERY_VALIDATION_ENABLED=true
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

# Monitoring Settings
MONITORING_ENABLED=true
METRICS_ENABLED=true
HEALTH_CHECKS_ENABLED=true
"""
        return template

# Global configuration instance
config = ProductionConfig()

# Convenience functions for backward compatibility
def get_neo4j_config() -> Neo4jConfig:
    """Get Neo4j configuration."""
    return config.neo4j

def get_embedding_config() -> EmbeddingConfig:
    """Get embedding configuration."""
    return config.embedding

def get_agent_config() -> AgentConfig:
    """Get agent configuration."""
    return config.agent

def get_security_config() -> SecurityConfig:
    """Get security configuration."""
    return config.security

def get_app_config() -> ApplicationConfig:
    """Get application configuration."""
    return config.app

def is_production() -> bool:
    """Check if running in production environment."""
    return config.app.environment == EnvironmentType.PRODUCTION

def is_development() -> bool:
    """Check if running in development environment."""
    return config.app.environment == EnvironmentType.DEVELOPMENT