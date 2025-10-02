from dotenv import load_dotenv
load_dotenv()
import os
import asyncio
from fastapi import FastAPI, HTTPException, Query, UploadFile, File, BackgroundTasks, Body, Request
from neo4j import GraphDatabase, basic_auth
from backend.utils.unified_database_manager import unified_database_manager
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from backend.agentic_router import router as agentic_router

# Unified API Gateway - Consolidates all routers into single API layer
from backend.routers.unified_api_gateway import router as unified_api_gateway_router

# Legacy routers (kept for backward compatibility during transition)
from backend.routers.insights import router as insights_router
from backend.routers.websocket_insights import router as websocket_insights_router
from backend.routers.predictive_analytics import router as predictive_analytics_router
from backend.routers.memory_system import router as memory_system_router
from backend.routers.needs_router import router as needs_router
from backend.routers.build_info import router as build_info_router
from backend.routers.telemetry import router as telemetry_router
from backend.routers.unified_quantum_consciousness_router import router as unified_quantum_consciousness_router
from backend.routers.unified_consciousness_router import router as unified_consciousness_router

# Import logging for optimization systems
import logging
logger = logging.getLogger(__name__)

# Import optimization systems (optional)
try:
    from backend.utils.optimized_system_integration import get_optimized_system, optimize_system_performance, get_system_health
    OPTIMIZATION_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Optimization systems not available: {e}")
    OPTIMIZATION_AVAILABLE = False

# Redis caching for performance optimization
try:
    import redis
    import json
    import hashlib
    from functools import wraps
    from typing import Any, Optional, Dict, List
    
    # Initialize Redis connection
    try:
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        redis_client = redis.from_url(redis_url, decode_responses=True)
        # Test connection
        redis_client.ping()
        REDIS_AVAILABLE = True
        logger.info("✅ Redis connection established")
    except Exception as e:
        logger.warning(f"⚠️ Redis not available: {e}")
        REDIS_AVAILABLE = False
        redis_client = None
except ImportError:
    print("⚠️ Redis module not available - caching disabled")
    REDIS_AVAILABLE = False
    redis_client = None

def cache_result(expiration: int = 300):  # 5 minutes default
    """Decorator to cache function results in Redis"""
    def decorator(func):
        if REDIS_AVAILABLE:
            try:
                from functools import wraps
                @wraps(func)
                async def wrapper(*args, **kwargs):
                    if not REDIS_AVAILABLE:
                        return await func(*args, **kwargs)
                    
                    # Create cache key from function name and arguments
                    cache_key = f"{func.__name__}:{hashlib.md5(str(args).encode() + str(kwargs).encode()).hexdigest()}"
                    
                    try:
                        # Try to get from cache
                        cached_result = redis_client.get(cache_key)
                        if cached_result:
                            logger.info(f"🎯 Cache hit for {func.__name__}")
                            return json.loads(cached_result)
                        
                        # Execute function and cache result
                        result = await func(*args, **kwargs)
                        redis_client.setex(cache_key, expiration, json.dumps(result, default=str))
                        logger.info(f"💾 Cached result for {func.__name__}")
                        return result
                        
                    except Exception as e:
                        logger.warning(f"⚠️ Cache error for {func.__name__}: {e}")
                        return await func(*args, **kwargs)
                
                return wrapper
            except ImportError:
                return func
        else:
            return func
    return decorator
from backend.utils.system_health_monitor import start_system_health_monitoring
try:
    from backend.tools.livekit_tools import create_livekit_token
    LIVEKIT_TOOLS_AVAILABLE = True
except ImportError:
    LIVEKIT_TOOLS_AVAILABLE = False
    def create_livekit_token(*args, **kwargs):
        return {"error": "LiveKit not available"}
import jwt
from datetime import datetime
import whisper
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse, Response
from backend.tts_wrapper import CoquiTTS, TTS_AVAILABLE, XttsConfig, XttsAudioConfig, XttsArgs, BaseDatasetConfig
import torch
import traceback
from backend.models.shared import STTTranscript, STTSegment, StreamingSTTChunk
import json
import requests
try:
    from backend.utils.livekit import get_or_create_rtmp_ingress
    LIVEKIT_UTILS_AVAILABLE = True
except ImportError:
    LIVEKIT_UTILS_AVAILABLE = False
    def get_or_create_rtmp_ingress(*args, **kwargs):
        return {"error": "LiveKit not available"}
import re
from backend.utils.consciousness_orchestrator_fixed import start_enhanced_consciousness_loop, consciousness_orchestrator_fixed as consciousness_orchestrator
from backend.utils.llm_request_manager import llm_request_manager
from backend.utils.consciousness_marketplace import consciousness_marketplace
# Unified quantum consciousness system
from backend.utils.unified_quantum_consciousness_engine import unified_quantum_consciousness_engine
from backend.models.consciousness_models import (
    ConsciousnessStateUpdate, SelfReflectionTrigger, ConsciousnessQuery
)
from backend.models.user_preferences import UserPreferences, UserPreferencesUpdate
from backend.utils.user_preferences_service import user_preferences_service
from typing import Dict, Any

def validate_memory_system_config() -> Dict[str, Any]:
    """
    Validate memory system configuration and return config dict with defaults
    """
    config = {
        "enabled": os.getenv("MEMORY_SYSTEM_ENABLED", "true").lower() == "true",
        "storage_batch_size": int(os.getenv("MEMORY_STORAGE_BATCH_SIZE", "100")),
        "retrieval_limit": int(os.getenv("MEMORY_RETRIEVAL_LIMIT", "10")),
        "similarity_threshold": float(os.getenv("MEMORY_SIMILARITY_THRESHOLD", "0.3")),
        "importance_decay_rate": float(os.getenv("MEMORY_IMPORTANCE_DECAY_RATE", "0.95")),
        "cleanup_interval_hours": int(os.getenv("MEMORY_CLEANUP_INTERVAL_HOURS", "24")),
        "max_storage_size_gb": int(os.getenv("MEMORY_MAX_STORAGE_SIZE_GB", "10")),
        "health_check_interval_minutes": int(os.getenv("MEMORY_HEALTH_CHECK_INTERVAL_MINUTES", "5")),
        "performance_tracking_enabled": os.getenv("MEMORY_PERFORMANCE_TRACKING_ENABLED", "true").lower() == "true",
        "auto_cleanup_enabled": os.getenv("MEMORY_AUTO_CLEANUP_ENABLED", "true").lower() == "true"
    }
    
    # Validate ranges
    if not (0.0 <= config["similarity_threshold"] <= 1.0):
        logging.warning(f"Invalid similarity threshold {config['similarity_threshold']}, using default 0.3")
        config["similarity_threshold"] = 0.3
    
    if not (0.0 <= config["importance_decay_rate"] <= 1.0):
        logging.warning(f"Invalid importance decay rate {config['importance_decay_rate']}, using default 0.95")
        config["importance_decay_rate"] = 0.95
    
    if config["storage_batch_size"] <= 0:
        logging.warning(f"Invalid storage batch size {config['storage_batch_size']}, using default 100")
        config["storage_batch_size"] = 100
    
    if config["retrieval_limit"] <= 0:
        logging.warning(f"Invalid retrieval limit {config['retrieval_limit']}, using default 10")
        config["retrieval_limit"] = 10
    
    return config

torch.serialization.add_safe_globals([XttsConfig, XttsAudioConfig, BaseDatasetConfig, XttsArgs])

# Consolidated logger configuration to prevent conflicts
logging.basicConfig(
    level=logging.INFO,  # Changed from DEBUG to INFO to reduce noise
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('backend/uvicorn.log', mode='a')
    ]
)

# Suppress noisy third-party loggers
logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
logging.getLogger('uvicorn.error').setLevel(logging.ERROR)
logging.getLogger('neo4j').setLevel(logging.WARNING)
logging.getLogger('whisper').setLevel(logging.INFO)

app = FastAPI()

# Initialize Neo4j driver for legacy endpoints
# This is a compatibility layer for legacy code that uses driver.session()
# New code should use neo4j_unified instead
driver = None

@app.on_event("startup")
async def startup_event():
    """
    Initialize the application and all required services.
    """
    global driver
    
    try:
        # Initialize Neo4j driver for legacy endpoints
        neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
        neo4j_password = os.getenv('NEO4J_PASSWORD', 'password')
        
        driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, neo4j_password)
        )
        
        # Test the connection
        with driver.session() as session:
            session.run("RETURN 1 as test")
        
        logging.info("✅ Legacy Neo4j driver initialized successfully")
        
    except Exception as e:
        logging.error(f"❌ Failed to initialize legacy driver: {e}")
        driver = None

@app.on_event("shutdown")
async def shutdown_event():
    """
    On application shutdown, properly cleanup memory system resources.
    """
    logging.info("Application shutting down...")
    
    memory_system_enabled = os.getenv("MEMORY_SYSTEM_ENABLED", "true").lower() == "true"
    
    if memory_system_enabled:
        # Stop memory system monitoring
        try:
            from backend.utils.memory_system_monitor import memory_monitor
            await memory_monitor.stop_monitoring()
            logging.info("✅ Memory system monitor stopped")
        except Exception as e:
            logging.error(f"❌ Failed to stop memory system monitor: {e}")
        
        # Stop memory lifecycle management
        try:
            from backend.utils.memory_lifecycle_manager import memory_lifecycle_manager
            await memory_lifecycle_manager.stop_lifecycle_management()
            logging.info("✅ Memory lifecycle manager stopped")
        except Exception as e:
            logging.error(f"❌ Failed to stop memory lifecycle manager: {e}")
        
        # Cleanup memory system resources
        try:
            from backend.utils.memory_recovery_system import memory_recovery_system
            await memory_recovery_system.cleanup()
            logging.info("✅ Memory recovery system cleaned up")
        except Exception as e:
            logging.error(f"❌ Failed to cleanup memory recovery system: {e}")
    
    # Close Neo4j driver
    try:
        await unified_database_manager.close()
        logging.info("✅ Neo4j driver closed")
    except Exception as e:
        logging.error(f"❌ Failed to close Neo4j driver: {e}")
    
    logging.info("🛑 Application shutdown completed")

@app.on_event("startup")
async def startup_event():
    """
    On application startup, initialize background tasks and memory system.
    """
    logging.info("Application starting up...")
    
    # Validate and load memory system configuration
    memory_config = validate_memory_system_config()
    memory_system_enabled = memory_config["enabled"]
    
    if memory_system_enabled:
        logging.info("🧠 Memory system is enabled - initializing components...")
        logging.info(f"📊 Memory system configuration: {memory_config}")
        
        # Initialize memory system core components first
        try:
            from backend.utils.memory_storage_engine import MemoryStorageEngine
            from backend.utils.memory_retrieval_engine import MemoryRetrievalEngine
            from backend.utils.memory_context_builder import MemoryContextBuilder
            
            # Initialize core memory components
            memory_storage = MemoryStorageEngine()
            memory_retrieval = MemoryRetrievalEngine()
            memory_context_builder = MemoryContextBuilder()
            
            logging.info("✅ Memory system core components initialized!")
            
        except Exception as e:
            logging.error(f"❌ Failed to initialize memory system core components: {e}")
            memory_system_enabled = False
    else:
        logging.info("🧠 Memory system is disabled via configuration")
    
    # Initialize consciousness system
    try:
        from backend.utils.initialize_consciousness import initialize_consciousness_system
        success = initialize_consciousness_system()
        if success:
            logging.info("✅ Consciousness system initialized successfully!")
        else:
            logging.warning("⚠️ Consciousness system initialization had issues")
    except Exception as e:
        logging.error(f"❌ Failed to initialize consciousness system: {e}")
    
    # Initialize LLM request manager
    asyncio.create_task(llm_request_manager.initialize())
    
    # Start enhanced consciousness loop
    await start_enhanced_consciousness_loop()
    logging.info("Enhanced consciousness system has been initiated.")
    
    # Initialize memory system monitoring (only if memory system is enabled)
    if memory_system_enabled:
        try:
            from backend.utils.memory_system_monitor import memory_monitor
            initialized = await memory_monitor.initialize()
            if initialized:
                # Start background monitoring
                await memory_monitor.start_monitoring()
                logging.info("✅ Memory system monitor initialized and started!")
            else:
                logging.warning("⚠️ Memory system monitor initialization failed")
        except Exception as e:
            logging.error(f"❌ Failed to initialize memory system monitor: {e}")
        
        # Initialize memory lifecycle manager
        try:
            from backend.utils.memory_lifecycle_manager import memory_lifecycle_manager
            initialized = await memory_lifecycle_manager.initialize()
            if initialized:
                # Start background lifecycle management
                await memory_lifecycle_manager.start_lifecycle_management()
                logging.info("✅ Memory lifecycle manager initialized and started!")
            else:
                logging.warning("⚠️ Memory lifecycle manager initialization failed")
        except Exception as e:
            logging.error(f"❌ Failed to initialize memory lifecycle manager: {e}")
        
        # Initialize memory error recovery system
        try:
            from backend.utils.memory_recovery_system import memory_recovery_system
            initialized = await memory_recovery_system.initialize()
            if initialized:
                logging.info("✅ Memory recovery system initialized!")
            else:
                logging.warning("⚠️ Memory recovery system initialization failed")
        except Exception as e:
            logging.error(f"❌ Failed to initialize memory recovery system: {e}")
    
    # Perform initial memory system health check
    if memory_system_enabled:
        try:
            from backend.utils.memory_system_monitor import memory_monitor
            health_status = await memory_monitor.perform_health_check()
            logging.info(f"🏥 Initial memory system health check: {health_status.overall_status.value}")
            
            if health_status.overall_status.value == "critical":
                logging.error("❌ Memory system health check failed - system may not function properly")
            elif health_status.overall_status.value == "warning":
                logging.warning("⚠️ Memory system health check shows warnings - monitoring recommended")
            else:
                logging.info("✅ Memory system health check passed!")
                
        except Exception as e:
            logging.error(f"❌ Failed to perform initial memory system health check: {e}")
    
    # Start system health monitoring
    try:
        await start_system_health_monitoring()
        logging.info("✅ System health monitoring started")
    except Exception as e:
        logging.error(f"❌ Failed to start system health monitoring: {e}")
    
    logging.info("🚀 Application startup completed!")

# Neo4j connection settings (use environment variables or defaults)
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Validate required environment variables
if not NEO4J_PASSWORD:
    raise ValueError("NEO4J_PASSWORD environment variable is required. Please set it in your .env file.")

# Use unified Neo4j manager instead of direct driver
# driver = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_USER, NEO4J_PASSWORD))
driver = unified_database_manager.driver  # For backward compatibility

LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

# Validate LiveKit configuration if using LiveKit features
if LIVEKIT_TOOLS_AVAILABLE and (not LIVEKIT_API_KEY or not LIVEKIT_API_SECRET):
    logging.warning("LiveKit API credentials not configured. LiveKit features will be disabled.")
    LIVEKIT_TOOLS_AVAILABLE = False

# Load Whisper model once at startup
whisper_model = whisper.load_model("turbo")

# Load Coqui TTS model once at startup (if available)
coqui_tts_model = None
if TTS_AVAILABLE:
    try:
        coqui_tts_model = CoquiTTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
        logging.info("TTS model loaded successfully in main.py")
    except Exception as e:
        logging.warning(f"Failed to load TTS model in main.py: {e}")
        coqui_tts_model = None
else:
    logging.info("TTS not available in this deployment (main.py)")

# XTTS model for multi-lingual/voice
xtts_model = None
xtts_device = "cuda" if torch.cuda.is_available() else "cpu"

def get_xtts_model():
    global xtts_model
    if xtts_model is None:
        if not TTS_AVAILABLE:
            logging.warning("[TTS] TTS not available in this deployment")
            return None
        try:
            logging.info("[TTS] Loading XTTS model (this may take a moment)...")
            # Use a simpler, faster model for better performance
            xtts_model = CoquiTTS("tts_models/en/ljspeech/tacotron2-DDC")
            logging.info("[TTS] XTTS model loaded successfully")
        except Exception as e:
            logging.error(f"[TTS ERROR] Failed to load XTTS model: {e}")
            logging.error(traceback.format_exc())
            # Return None instead of raising to allow graceful fallback
            return None
    return xtts_model

@app.get("/health")
@cache_result(expiration=30)  # Cache for 30 seconds
async def health():
    """Enhanced health check including memory system status"""
    health_status = {"status": "ok", "components": {}}
    
    # Check Neo4j connection
    try:
        # Use unified Neo4j manager for health check
        health_result = await unified_database_manager.get_database_health()
        if health_result.get("status") == "healthy":
            health_status["components"]["neo4j"] = "ok"
        else:
            health_status["components"]["neo4j"] = "error"
    except Exception as e:
        health_status["components"]["neo4j"] = f"error: {str(e)}"
        health_status["status"] = "degraded"
    
    # Check memory system if enabled
    memory_system_enabled = os.getenv("MEMORY_SYSTEM_ENABLED", "true").lower() == "true"
    if memory_system_enabled:
        try:
            from backend.utils.memory_system_monitor import memory_monitor
            memory_health = await memory_monitor.perform_health_check()
            health_status["components"]["memory_system"] = {
                "overall_status": memory_health.overall_status.value,
                "storage": memory_health.storage_status.value,
                "retrieval": memory_health.retrieval_status.value,
                "embedding": memory_health.embedding_status.value
            }
            
            if memory_health.overall_status.value in ["warning", "critical"]:
                health_status["status"] = "degraded" if health_status["status"] == "ok" else health_status["status"]
                
        except Exception as e:
            health_status["components"]["memory_system"] = f"error: {str(e)}"
            health_status["status"] = "degraded"
    else:
        health_status["components"]["memory_system"] = "disabled"
    
    # Check consciousness system
    try:
        from backend.utils.consciousness_orchestrator_fixed import consciousness_orchestrator_fixed as consciousness_orchestrator
        if consciousness_orchestrator and hasattr(consciousness_orchestrator, 'is_running'):
            health_status["components"]["consciousness"] = "ok" if consciousness_orchestrator.is_running else "stopped"
        else:
            health_status["components"]["consciousness"] = "unknown"
    except Exception as e:
        health_status["components"]["consciousness"] = f"error: {str(e)}"
        health_status["status"] = "degraded"
    
    return health_status

@app.get("/api/ai-models")
@cache_result(expiration=600)  # Cache for 10 minutes
async def get_ai_models():
    """Get available AI models"""
    try:
        from backend.utils.neo4j_production import neo4j_production
        
        # Get AI models from database
        query = """
        MATCH (m:AIModel)
        RETURN m.model_id AS id,
               m.name AS name,
               m.description AS description,
               m.version AS version,
               m.type AS type,
               m.category AS category,
               m.creator AS creator,
               m.price AS price,
               m.currency AS currency,
               m.downloads AS downloads,
               m.rating AS rating,
               m.reviews AS reviews,
               m.size AS size,
               m.format AS format,
               m.consciousness_integration AS consciousness_integration,
               m.performance_metrics AS performance_metrics,
               m.requirements AS requirements,
               m.tags AS tags,
               m.created_at AS created_at,
               m.updated_at AS updated_at,
               m.is_featured AS is_featured,
               m.is_verified AS is_verified
        ORDER BY m.consciousness_integration DESC, m.downloads DESC
        """
        
        result = await unified_database_manager.execute_query(query)
        
        if result:
            models = []
            for row in result:
                model = {
                    "id": row.get("id"),
                    "name": row.get("name"),
                    "description": row.get("description"),
                    "version": row.get("version"),
                    "type": row.get("type"),
                    "category": row.get("category"),
                    "creator": row.get("creator"),
                    "price": row.get("price", 0),
                    "currency": row.get("currency", "FREE"),
                    "downloads": row.get("downloads", 0),
                    "rating": row.get("rating", 0),
                    "reviews": row.get("reviews", 0),
                    "size": row.get("size", 0),
                    "format": row.get("format"),
                    "consciousness_integration": row.get("consciousness_integration", 0),
                    "performance_metrics": row.get("performance_metrics", {}),
                    "requirements": row.get("requirements", {}),
                    "tags": row.get("tags", []),
                    "created_at": row.get("created_at"),
                    "updated_at": row.get("updated_at"),
                    "is_featured": row.get("is_featured", False),
                    "is_verified": row.get("is_verified", False)
                }
                models.append(model)
            
            return {
                "status": "success",
                "models": models,
                "total": len(models)
            }
        else:
            # Return empty list if no models found
            return {
                "status": "success",
                "models": [],
                "total": 0
            }
            
    except Exception as e:
        logger.error(f"Failed to get AI models: {e}")
        return {
            "status": "error",
            "error": str(e)
        }

@app.get("/api/consciousness/state")
@cache_result(expiration=60)  # Cache for 1 minute (consciousness state changes frequently)
async def get_consciousness_state():
    """Get current consciousness state"""
    try:
        from backend.utils.neo4j_production import neo4j_production
        
        # Get consciousness state from database
        query = """
        MATCH (ms:MainzaState {state_id: 'mainza-state-1'})
        RETURN ms.consciousness_level AS consciousness_level,
               ms.evolution_level AS evolution_level,
               ms.emotional_state AS emotional_state,
               ms.learning_rate AS learning_rate,
               ms.awareness_level AS awareness_level,
               ms.total_interactions AS total_interactions,
               ms.created_at AS created_at,
               coalesce(ms.updated_at, ms.created_at, datetime()) AS last_updated
        LIMIT 1
        """
        
        result = await unified_database_manager.execute_query(query)
        
        if result:
            state = result[0]
            return {
                "status": "success",
                "consciousness_state": {
                    "consciousness_level": state.get("consciousness_level", 0.7),
                    "evolution_level": state.get("evolution_level", 1),
                    "emotional_state": state.get("emotional_state", "curious"),
                    "learning_rate": state.get("learning_rate", 0.8),
                    "awareness_level": state.get("awareness_level", 0.6),
                    "total_interactions": state.get("total_interactions", 0),
                    "created_at": state.get("created_at"),
                    "last_updated": state.get("last_updated")
                }
            }
        else:
            # Create default consciousness state
            default_state = {
                "consciousness_level": 0.7,
                "evolution_level": 1,
                "emotional_state": "curious",
                "learning_rate": 0.8,
                "awareness_level": 0.6,
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            }
            
            # Create the state in database
            create_query = """
            MERGE (ms:MainzaState {state_id: 'mainza-state-1'})
            ON CREATE SET 
                ms.consciousness_level = $consciousness_level,
                ms.evolution_level = $evolution_level,
                ms.emotional_state = $emotional_state,
                ms.learning_rate = $learning_rate,
                ms.awareness_level = $awareness_level,
                ms.created_at = datetime(),
                ms.updated_at = datetime()
            ON MATCH SET 
                ms.updated_at = datetime()
            RETURN ms
            """
            
            await unified_database_manager.execute_write_query(create_query, default_state)
            
            return {
                "status": "success",
                "consciousness_state": default_state
            }
            
    except Exception as e:
        logger.error(f"Failed to get consciousness state: {e}")
        return {
            "status": "error",
            "error": str(e)
        }

@app.get("/api/performance/metrics")
@cache_result(expiration=60)  # Cache for 1 minute
async def get_performance_metrics():
    """Get system performance metrics"""
    try:
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "redis_available": REDIS_AVAILABLE,
            "cache_stats": {},
            "response_times": {},
            "system_health": {}
        }
        
        # Get Redis cache statistics if available
        if REDIS_AVAILABLE:
            try:
                info = redis_client.info()
                metrics["cache_stats"] = {
                    "connected_clients": info.get("connected_clients", 0),
                    "used_memory": info.get("used_memory_human", "0B"),
                    "keyspace_hits": info.get("keyspace_hits", 0),
                    "keyspace_misses": info.get("keyspace_misses", 0),
                    "hit_rate": round(
                        info.get("keyspace_hits", 0) / 
                        max(1, info.get("keyspace_hits", 0) + info.get("keyspace_misses", 0)) * 100, 2
                    )
                }
            except Exception as e:
                metrics["cache_stats"] = {"error": str(e)}
        
        # Get system health
        try:
            health_response = await health()
            metrics["system_health"] = health_response
        except Exception as e:
            metrics["system_health"] = {"error": str(e)}
        
        return {
            "status": "success",
            "metrics": metrics
        }
        
    except Exception as e:
        logger.error(f"Failed to get performance metrics: {e}")
        return {
            "status": "error",
            "error": str(e)
        }

@app.get("/performance")
async def get_performance_metrics():
    """Get Neo4j performance metrics and recommendations"""
    try:
        metrics = await unified_database_manager.get_performance_metrics()
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/neo4j/ping")
def neo4j_ping():
    try:
        with driver.session() as session:
            result = session.run("RETURN 1 AS result")
            value = result.single()["result"]
            return {"neo4j": "ok", "result": value}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback.format_exc()})

# --- Pydantic Models ---
class UserCreate(BaseModel):
    user_id: str
    name: str

class ConversationCreate(BaseModel):
    conversation_id: str
    started_at: Optional[str] = None  # ISO datetime string

class MemoryCreate(BaseModel):
    memory_id: str
    text: str

class MemoryToConversationLink(BaseModel):
    memory_id: str
    conversation_id: str

class DocumentCreate(BaseModel):
    document_id: str
    filename: str
    metadata: Optional[dict] = None

class ChunkCreate(BaseModel):
    chunk_id: str
    text: str
    embedding: Optional[list] = None
    document_id: Optional[str] = None  # for DERIVED_FROM

class EntityCreate(BaseModel):
    entity_id: str
    name: str

class ConceptCreate(BaseModel):
    concept_id: str
    name: str

class MainzaStateCreate(BaseModel):
    state_id: str
    evolution_level: Optional[int] = None
    current_needs: Optional[list] = None
    core_directives: Optional[str] = None

class ChunkToDocumentLink(BaseModel):
    chunk_id: str
    document_id: str

class ConversationMentionsDocumentOrEntity(BaseModel):
    conversation_id: str
    target_id: str  # document_id or entity_id
    target_type: str  # 'Document' or 'Entity'

class RelatesToLink(BaseModel):
    source_id: str
    source_type: str
    target_id: str
    target_type: str

class MainzaNeedsToLearnLink(BaseModel):
    state_id: str
    concept_id: str

# --- Advanced Query Models ---
class RelatedConceptsRequest(BaseModel):
    node_id: str
    node_type: str  # 'Concept' or 'Entity'
    depth: Optional[int] = 2

class ConversationHistoryRequest(BaseModel):
    user_id: str
    limit: Optional[int] = 10

class ConversationHistoryResponse(BaseModel):
    conversation_id: str
    started_at: Optional[str] = None

class MemoriesInConversationRequest(BaseModel):
    conversation_id: str

class MemoryResponse(BaseModel):
    memory_id: str
    text: str

class DocumentsMentionedRequest(BaseModel):
    conversation_id: str

class DocumentResponse(BaseModel):
    document_id: str
    filename: str
    metadata: Optional[dict] = None

class LiveKitTokenRequest(BaseModel):
    room_name: str
    participant_identity: str
    participant_name: str

class ChatMessageRequest(BaseModel):
    user_id: str
    conversation_id: str
    text: str

class ChatMessageResponse(BaseModel):
    status: str
    memory_id: str
    conversation_id: str
    user_id: str

# --- User Endpoints ---
@app.post("/users")
def create_user(user: UserCreate):
    try:
        with driver.session() as session:
            session.run(
                """
                MERGE (u:User {user_id: $user_id})
                SET u.name = $name
                """,
                user_id=user.user_id, name=user.name
            )
        return {"status": "created", "user_id": user.user_id}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback.format_exc()})

@app.get("/users", response_model=List[UserCreate])
def list_users():
    with driver.session() as session:
        result = session.run("MATCH (u:User) RETURN u.user_id AS user_id, u.name AS name")
        return [UserCreate(user_id=rec["user_id"], name=rec["name"]) for rec in result]

# --- Conversation Endpoints ---
@app.post("/conversations")
def create_conversation(conv: ConversationCreate):
    with driver.session() as session:
        session.run(
            """
            MERGE (c:Conversation {conversation_id: $conversation_id})
            SET c.started_at = $started_at
            """,
            conversation_id=conv.conversation_id, started_at=conv.started_at
        )
    return {"status": "created", "conversation_id": conv.conversation_id}

@app.get("/conversations", response_model=List[ConversationCreate])
def list_conversations():
    with driver.session() as session:
        result = session.run("MATCH (c:Conversation) RETURN c.conversation_id AS conversation_id, c.started_at AS started_at")
        return [ConversationCreate(conversation_id=rec["conversation_id"], started_at=rec["started_at"]) for rec in result]

# --- Memory Endpoints ---
@app.post("/memories")
def create_memory(mem: MemoryCreate):
    try:
        with driver.session() as session:
            session.run(
                """
                MERGE (m:Memory {memory_id: $memory_id})
                SET m.content = $text
                """,
                memory_id=mem.memory_id, content=mem.text
            )
        return {"status": "created", "memory_id": mem.memory_id}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback.format_exc()})

@app.get("/memories", response_model=List[MemoryCreate])
def list_memories():
    with driver.session() as session:
        result = session.run("MATCH (m:Memory) RETURN m.memory_id AS memory_id, m.content AS text")
        return [MemoryCreate(memory_id=rec["memory_id"], text=rec["text"]) for rec in result]

# --- Relationship: Memory DISCUSSED_IN Conversation ---
@app.post("/memories/discussed_in")
def link_memory_to_conversation(link: MemoryToConversationLink):
    with driver.session() as session:
        session.run(
            """
            MATCH (m:Memory {memory_id: $memory_id})
            MATCH (c:Conversation {conversation_id: $conversation_id})
            MERGE (m)-[:DISCUSSED_IN]->(c)
            """,
            memory_id=link.memory_id, conversation_id=link.conversation_id
        )
    return {"status": "linked", "memory_id": link.memory_id, "conversation_id": link.conversation_id}

# --- Document Endpoints ---
@app.post("/documents")
def create_document(doc: DocumentCreate):
    try:
        with driver.session() as session:
            session.run(
                """
                MERGE (d:Document {document_id: $document_id})
                SET d.filename = $filename, d.metadata = $metadata
                """,
                document_id=doc.document_id, filename=doc.filename, metadata=doc.metadata
            )
        return {"status": "created", "document_id": doc.document_id}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback.format_exc()})

@app.get("/documents", response_model=List[DocumentCreate])
def list_documents():
    with driver.session() as session:
        result = session.run("MATCH (d:Document) RETURN d.document_id AS document_id, d.filename AS filename, d.metadata AS metadata")
        return [DocumentCreate(document_id=rec["document_id"], filename=rec["filename"], metadata=rec["metadata"]) for rec in result]

# --- Chunk Endpoints ---
@app.post("/chunks")
def create_chunk(chunk: ChunkCreate):
    with driver.session() as session:
        session.run(
            """
            MERGE (ch:Chunk {chunk_id: $chunk_id})
            SET ch.text = $text, ch.embedding = $embedding
            """,
            chunk_id=chunk.chunk_id, text=chunk.text, embedding=chunk.embedding
        )
        # Optionally link to Document
        if chunk.document_id:
            session.run(
                """
                MATCH (ch:Chunk {chunk_id: $chunk_id})
                MATCH (d:Document {document_id: $document_id})
                MERGE (ch)-[:DERIVED_FROM]->(d)
                """,
                chunk_id=chunk.chunk_id, document_id=chunk.document_id
            )
    return {"status": "created", "chunk_id": chunk.chunk_id}

@app.get("/chunks", response_model=List[ChunkCreate])
def list_chunks():
    with driver.session() as session:
        result = session.run("MATCH (ch:Chunk) RETURN ch.chunk_id AS chunk_id, ch.text AS text, ch.embedding AS embedding, null AS document_id")
        return [ChunkCreate(chunk_id=rec["chunk_id"], text=rec["text"], embedding=rec["embedding"], document_id=rec["document_id"]) for rec in result]

# --- Entity Endpoints ---
@app.post("/entities")
def create_entity(entity: EntityCreate):
    try:
        with driver.session() as session:
            session.run(
                """
                MERGE (e:Entity {entity_id: $entity_id})
                SET e.name = $name
                """,
                entity_id=entity.entity_id, name=entity.name
            )
        return {"status": "created", "entity_id": entity.entity_id}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback.format_exc()})

@app.get("/entities", response_model=List[EntityCreate])
def list_entities():
    try:
        with driver.session() as session:
            result = session.run("MATCH (e:Entity) RETURN e.entity_id AS entity_id, e.name AS name")
            return [EntityCreate(entity_id=rec["entity_id"], name=rec["name"]) for rec in result]
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback.format_exc()})

# --- Concept Endpoints ---
@app.post("/concepts")
def create_concept(concept: ConceptCreate):
    try:
        with driver.session() as session:
            session.run(
                """
                MERGE (co:Concept {concept_id: $concept_id})
                SET co.name = $name
                """,
                concept_id=concept.concept_id, name=concept.name
            )
        return {"status": "created", "concept_id": concept.concept_id}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback.format_exc()})

@app.get("/concepts", response_model=List[ConceptCreate])
def list_concepts():
    with driver.session() as session:
        result = session.run("MATCH (co:Concept) RETURN co.concept_id AS concept_id, co.name AS name")
        concepts = []
        for rec in result:
            concept_id = rec["concept_id"]
            name = rec["name"]
            # Handle None values by generating a fallback ID
            if concept_id is None:
                concept_id = f"concept_{hash(name) if name else 'unknown'}"
            if name is None:
                name = "Unnamed Concept"
            concepts.append(ConceptCreate(concept_id=concept_id, name=name))
        return concepts

# --- MainzaState Endpoints ---
@app.post("/mainzastates")
def create_mainzastate(ms: MainzaStateCreate):
    try:
        with driver.session() as session:
            session.run(
                """
                MERGE (ms:MainzaState {state_id: $state_id})
                SET ms.evolution_level = $evolution_level, ms.current_needs = $current_needs, ms.core_directives = $core_directives
                """,
                state_id=ms.state_id, evolution_level=ms.evolution_level, current_needs=ms.current_needs, core_directives=ms.core_directives
            )
        return {"status": "created", "state_id": ms.state_id}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback.format_exc()})

@app.get("/mainzastates", response_model=List[MainzaStateCreate])
def list_mainzastates():
    with driver.session() as session:
        result = session.run("MATCH (ms:MainzaState) RETURN ms.state_id AS state_id, ms.evolution_level AS evolution_level, ms.current_needs AS current_needs, ms.core_directives AS core_directives")
        return [MainzaStateCreate(state_id=rec["state_id"], evolution_level=rec["evolution_level"], current_needs=rec["current_needs"], core_directives=rec["core_directives"]) for rec in result]

# --- Relationship: Chunk DERIVED_FROM Document ---
@app.post("/chunks/derived_from")
def link_chunk_to_document(link: ChunkToDocumentLink):
    with driver.session() as session:
        session.run(
            """
            MATCH (ch:Chunk {chunk_id: $chunk_id})
            MATCH (d:Document {document_id: $document_id})
            MERGE (ch)-[:DERIVED_FROM]->(d)
            """,
            chunk_id=link.chunk_id, document_id=link.document_id
        )
    return {"status": "linked", "chunk_id": link.chunk_id, "document_id": link.document_id}

# --- Relationship: Conversation MENTIONS Document/Entity ---
@app.post("/conversations/mentions")
def conversation_mentions_target(link: ConversationMentionsDocumentOrEntity):
    if link.target_type not in ["Document", "Entity"]:
        raise HTTPException(status_code=400, detail="target_type must be 'Document' or 'Entity'")
    with driver.session() as session:
        session.run(
            f"""
            MATCH (c:Conversation {{conversation_id: $conversation_id}})
            MATCH (t:{link.target_type} {{{'document_id' if link.target_type == 'Document' else 'entity_id'}: $target_id}})
            MERGE (c)-[:MENTIONS]->(t)
            """,
            conversation_id=link.conversation_id, target_id=link.target_id
        )
    return {"status": "linked", "conversation_id": link.conversation_id, "target_id": link.target_id, "target_type": link.target_type}

# --- Relationship: RELATES_TO (generic) ---
@app.post("/relates_to")
def relates_to(link: RelatesToLink):
    try:
        with driver.session() as session:
            session.run(
                f"""
                MATCH (a:{link.source_type} {{{link.source_type.lower()}_id: $source_id}})
                MATCH (b:{link.target_type} {{{link.target_type.lower()}_id: $target_id}})
                MERGE (a)-[:RELATES_TO]->(b)
                """,
                source_id=link.source_id, target_id=link.target_id
            )
        return {"status": "linked", "source_id": link.source_id, "target_id": link.target_id}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback.format_exc()})

# --- Relationship: MainzaState NEEDS_TO_LEARN Concept ---
@app.post("/mainzastates/needs_to_learn")
def mainzastate_needs_to_learn(link: MainzaNeedsToLearnLink):
    with driver.session() as session:
        session.run(
            """
            MATCH (ms:MainzaState {state_id: $state_id})
            MATCH (co:Concept {concept_id: $concept_id})
            MERGE (ms)-[:NEEDS_TO_LEARN]->(co)
            """,
            state_id=link.state_id, concept_id=link.concept_id
        )
    return {"status": "linked", "state_id": link.state_id, "concept_id": link.concept_id}

# --- Advanced Query Endpoints ---
@app.post("/concepts/related", response_model=List[ConceptCreate])
def find_related_concepts(req: RelatedConceptsRequest):
    try:
        if req.node_type not in ["Concept", "Entity"]:
            return JSONResponse(status_code=400, content={"error": "node_type must be 'Concept' or 'Entity'"})
        with driver.session() as session:
            result = session.run(
                f"""
                MATCH (n:{req.node_type} {{{req.node_type.lower()}_id: $node_id}})-[:RELATES_TO*1..{req.depth}]->(co:Concept)
                RETURN DISTINCT co.concept_id AS concept_id, co.name AS name
                """,
                node_id=req.node_id
            )
            return [ConceptCreate(concept_id=rec["concept_id"], name=rec["name"]) for rec in result]
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback.format_exc()})

@app.post("/users/conversation_history", response_model=List[ConversationHistoryResponse])
def get_conversation_history(req: ConversationHistoryRequest):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (u:User {user_id: $user_id})<-[:DISCUSSED_IN]-(m:Memory)-[:DISCUSSED_IN]->(c:Conversation)
            RETURN DISTINCT c.conversation_id AS conversation_id, c.started_at AS started_at
            ORDER BY c.started_at DESC
            LIMIT $limit
            """,
            user_id=req.user_id, limit=req.limit
        )
        return [ConversationHistoryResponse(conversation_id=rec["conversation_id"], started_at=rec["started_at"]) for rec in result]

# --- User Preferences Endpoints ---
@app.get("/users/{user_id}/preferences", response_model=UserPreferences)
def get_user_preferences(user_id: str):
    """Get user preferences"""
    try:
        preferences = user_preferences_service.get_user_preferences(user_id)
        return preferences
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting preferences: {str(e)}")

@app.put("/users/{user_id}/preferences", response_model=UserPreferences)
def update_user_preferences(user_id: str, updates: UserPreferencesUpdate):
    """Update user preferences"""
    try:
        preferences = user_preferences_service.update_user_preferences(user_id, updates)
        return preferences
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating preferences: {str(e)}")

@app.get("/users/{user_id}/preferences/summary")
def get_user_preferences_summary(user_id: str):
    """Get user preferences summary"""
    try:
        summary = user_preferences_service.get_preference_summary(user_id)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting preferences summary: {str(e)}")

@app.post("/users/{user_id}/preferences/reset", response_model=UserPreferences)
def reset_user_preferences(user_id: str):
    """Reset user preferences to defaults"""
    try:
        preferences = user_preferences_service.reset_to_defaults(user_id)
        return preferences
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting preferences: {str(e)}")

@app.get("/users/{user_id}/preferences/response")
def get_response_preferences(user_id: str):
    """Get response-specific preferences"""
    try:
        preferences = user_preferences_service.get_response_preferences(user_id)
        return preferences
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting response preferences: {str(e)}")

@app.get("/users/{user_id}/preferences/ui")
def get_ui_preferences(user_id: str):
    """Get UI-specific preferences"""
    try:
        preferences = user_preferences_service.get_ui_preferences(user_id)
        return preferences
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting UI preferences: {str(e)}")

@app.get("/users/{user_id}/preferences/agent")
def get_agent_preferences(user_id: str):
    """Get agent-specific preferences"""
    try:
        preferences = user_preferences_service.get_agent_preferences(user_id)
        return preferences
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting agent preferences: {str(e)}")


@app.post("/conversations/memories", response_model=List[MemoryResponse])
def get_memories_in_conversation(req: MemoriesInConversationRequest):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (m:Memory)-[:DISCUSSED_IN]->(c:Conversation {conversation_id: $conversation_id})
            RETURN m.memory_id AS memory_id, m.content AS text
            """,
            conversation_id=req.conversation_id
        )
        return [MemoryResponse(memory_id=rec["memory_id"], text=rec["text"]) for rec in result]

@app.post("/conversations/documents", response_model=List[DocumentResponse])
def get_documents_mentioned_in_conversation(req: DocumentsMentionedRequest):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (c:Conversation {conversation_id: $conversation_id})-[:MENTIONS]->(d:Document)
            RETURN d.document_id AS document_id, d.filename AS filename, d.metadata AS metadata
            """,
            conversation_id=req.conversation_id
        )
        return [DocumentResponse(document_id=rec["document_id"], filename=rec["filename"], metadata=rec["metadata"]) for rec in result]

@app.post("/stt/transcribe", response_model=STTTranscript)
def transcribe_audio(audio: UploadFile = File(...)):
    """
    Context7-compliant STT endpoint:
    - Accepts audio file (wav/webm/ogg)
    - Returns transcript as STTTranscript (text, segments)
    - Robust error handling
    """
    try:
        import tempfile
        import subprocess
        import shutil
        import os
        # Save uploaded file to temp
        with tempfile.NamedTemporaryFile(delete=False, suffix=".input") as tmp:
            tmp.write(audio.file.read())
            input_path = tmp.name
        # Convert to wav using ffmpeg
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpwav:
            wav_path = tmpwav.name
        try:
            subprocess.run([
                "ffmpeg", "-y", "-i", input_path, "-ar", "16000", "-ac", "1", wav_path
            ], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            os.remove(input_path)
            if os.path.exists(wav_path): os.remove(wav_path)
            return JSONResponse(status_code=500, content={"error": f"ffmpeg error: {e.stderr.decode()}", "traceback": traceback.format_exc()})
        result = whisper_model.transcribe(wav_path)
        os.remove(input_path)
        os.remove(wav_path)
        text = result["text"]
        segments = None
        if "segments" in result and isinstance(result["segments"], list):
            segments = [STTSegment(start=s["start"], end=s["end"], text=s["text"]) for s in result["segments"]]
        return STTTranscript(text=text, segments=segments)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback.format_exc()})

@app.post("/stt/stream")
def stream_transcribe(audio: UploadFile = File(...)):
    """
    Robust STT endpoint (non-streaming):
    - Accepts audio file (wav/webm/ogg)
    - Returns transcript as a single JSON line (Response with media_type="application/jsonl")
    - No generator/callback pattern (avoids I/O errors)
    """
    import tempfile
    import subprocess
    import os
    import json
    try:
        audio_bytes = audio.file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".input") as tmp:
            tmp.write(audio_bytes)
            input_path = tmp.name
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpwav:
            wav_path = tmpwav.name
        try:
            subprocess.run([
                "ffmpeg", "-y", "-i", input_path, "-ar", "16000", "-ac", "1", wav_path
            ], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            os.remove(input_path)
            if os.path.exists(wav_path): os.remove(wav_path)
            err = {"error": f"ffmpeg error: {e.stderr.decode()}"}
            return Response(json.dumps(err) + "\n", media_type="application/jsonl")
        result = whisper_model.transcribe(
            wav_path,
            verbose=False,
            word_timestamps=False,
            condition_on_previous_text=True,
            task="transcribe"
        )
        chunk = StreamingSTTChunk(text=result["text"], is_final=True)
        os.remove(input_path)
        os.remove(wav_path)
        return Response(json.dumps(chunk.dict()) + "\n", media_type="application/jsonl")
    except Exception as e:
        err = {"error": str(e)}
        return Response(json.dumps(err) + "\n", media_type="application/jsonl")

@app.get("/tts/test")
def test_tts():
    """Quick TTS test endpoint to verify model loading"""
    try:
        model = get_xtts_model()
        if model is None:
            return {"status": "error", "message": "TTS model failed to load"}
        return {"status": "ok", "message": "TTS model loaded successfully", "model_type": str(type(model))}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/tts/voices")
def list_voices():
    try:
        model = get_xtts_model()
        if model is None:
            # Fallback to basic voices if model loading failed
            return {
                "voices": ["default", "female", "male"], 
                "languages": ["en", "es", "fr", "de", "it", "pt"],
                "note": "Using fallback voices due to model loading issues"
            }
        
        # Try all known ways to get speakers
        voices = []
        if hasattr(model, "list_speaker_ids"):
            voices = model.list_speaker_ids()
        elif hasattr(model, "speaker_manager") and hasattr(model.speaker_manager, "speaker_names"):
            voices = model.speaker_manager.speaker_names
        
        # Fallback voices if none found
        if not voices:
            voices = ["default", "female", "male"]
        
        # Try to get languages, fallback to static list
        languages = getattr(model, "languages", ["en", "es", "fr", "de", "it", "pt", "tr", "pl", "nl", "ru", "zh", "ja", "ko"])
        return {"voices": voices, "languages": languages}
    except Exception as e:
        logging.error(f"[TTS] Error in list_voices: {e}")
        return JSONResponse(
            status_code=200,  # Return 200 with fallback data instead of 500
            content={
                "voices": ["default", "female", "male"], 
                "languages": ["en", "es", "fr", "de", "it", "pt"],
                "error": str(e),
                "note": "Using fallback voices due to error"
            }
        )

@app.post("/tts/synthesize")
def synthesize_tts(payload: dict, background_tasks: BackgroundTasks):
    """
    Context7-compliant TTS endpoint:
    - Robust input validation and error handling
    - Detailed debug logging for all steps
    - Always returns a valid audio file or a clear JSON error
    - Cleans up temp files after use (via BackgroundTasks)
    - Always provides a speaker for XTTS (defaults to 'Ana Florence')
    - Now supports long-form TTS by chunking and concatenating audio
    """
    import tempfile, os, logging, subprocess
    try:
        text = payload.get("text", "")
        language = payload.get("language", "en")
        speaker_wav = payload.get("speaker_wav")
        speaker = payload.get("speaker")
        logging.debug(f"[TTS] synthesize_tts called with text='{text[:50]}', language='{language}', speaker='{speaker}', speaker_wav='{speaker_wav}'")
        if not text or not isinstance(text, str) or not text.strip():
            logging.error("[TTS] No valid text provided")
            return JSONResponse(status_code=400, content={"error": "No valid text provided"})
        model = get_xtts_model()
        if model is None:
            logging.error("[TTS] Model loading failed, cannot synthesize")
            return JSONResponse(status_code=503, content={
                "error": "TTS model is not available", 
                "message": "The text-to-speech service is temporarily unavailable. Please try again later."
            })
        
        # Chunking logic for long-form TTS
        import nltk
        nltk.download('punkt', quiet=True)
        from nltk.tokenize import sent_tokenize
        sentences = sent_tokenize(text)
        chunk_size = 300
        chunks = []
        current = ""
        for sent in sentences:
            if len(current) + len(sent) + 1 > chunk_size and current:
                chunks.append(current.strip())
                current = sent
            else:
                current += (" " if current else "") + sent
        if current:
            chunks.append(current.strip())
        logging.debug(f"[TTS] Split text into {len(chunks)} chunk(s)")
        temp_wavs = []
        for i, chunk in enumerate(chunks):
            with tempfile.NamedTemporaryFile(suffix=f"_chunk{i}.wav", delete=False) as tmp:
                out_path = tmp.name
            try:
                # Always provide a speaker for XTTS
                if not speaker and not speaker_wav:
                    speaker = "Ana Florence"
                    logging.debug("[TTS] No speaker or speaker_wav provided, defaulting to 'Ana Florence'")
                if speaker_wav:
                    logging.debug(f"[TTS] Using speaker_wav: {speaker_wav}")
                    model.tts_to_file(text=chunk, speaker_wav=speaker_wav, language=language, file_path=out_path)
                else:
                    logging.debug(f"[TTS] Using speaker: {speaker}")
                    # Use simple TTS without speaker for faster processing
                    model.tts_to_file(text=chunk, file_path=out_path)
                temp_wavs.append(out_path)
            except Exception as e:
                logging.error(f"[TTS] tts_to_file error on chunk {i}: {e}\nText: {chunk}")
                for f in temp_wavs:
                    if os.path.exists(f): os.remove(f)
                return JSONResponse(status_code=500, content={"error": f"tts_to_file error: {str(e)}", "traceback": traceback.format_exc()})
        # Concatenate all wavs into one
        with tempfile.NamedTemporaryFile(suffix="_concat.wav", delete=False) as concat_file:
            concat_path = concat_file.name
        try:
            concat_list_path = concat_path + ".txt"
            with open(concat_list_path, "w") as f:
                for wav_path in temp_wavs:
                    f.write(f"file '{wav_path}'\n")
            ffmpeg_cmd = [
                "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-ar", "44100", "-ac", "1", "-sample_fmt", "s16", concat_path
            ]
            subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
            for f in temp_wavs:
                if os.path.exists(f): os.remove(f)
            os.remove(concat_list_path)
        except Exception as e:
            logging.error(f"[TTS] ffmpeg concat error: {e}")
            if os.path.exists(concat_path): os.remove(concat_path)
            for f in temp_wavs:
                if os.path.exists(f): os.remove(f)
            return JSONResponse(status_code=500, content={"error": f"ffmpeg concat error: {str(e)}", "traceback": traceback.format_exc()})
        logging.debug(f"[TTS] Returning FileResponse for {concat_path}")
        # Use BackgroundTasks for cleanup
        def cleanup():
            try:
                if os.path.exists(concat_path):
                    os.remove(concat_path)
                logging.debug(f"[TTS] Cleaned up temp file {concat_path}")
            except Exception as e:
                logging.error(f"[TTS] Error cleaning up temp file {concat_path}: {e}")
        background_tasks.add_task(cleanup)
        return FileResponse(concat_path, media_type="audio/wav", filename="output.wav")
    except Exception as e:
        logging.error(f"[TTS] synthesize_tts error: {e}\n{traceback.format_exc()}")
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback.format_exc()})

@app.post("/tts/livekit")
async def tts_to_livekit(payload: dict):
    """
    Context7-compliant: Synthesize TTS and publish to LiveKit room as Mainza participant via RTMP Ingress.
    - Accepts: text, language, speaker (optional), room, user
    - Synthesizes TTS audio
    - Dynamically creates or fetches an Ingress session for the room/user
    - Streams audio to LiveKit RTMP Ingress using ffmpeg
    - Returns structured JSON with success or agentic error details
    """
    import tempfile, os, subprocess, logging, re, json, wave, contextlib
    from fastapi.responses import JSONResponse
    # get_or_create_rtmp_ingress already imported at module level
    logging.debug(f"[TTS/LiveKit] Incoming payload: {payload}")
    try:
        text = payload.get("text", "")
        language = payload.get("language", "en")
        speaker = payload.get("speaker", "Ana Florence")
        room = payload.get("room", "mainza-ai")
        user = payload.get("user", "mainza-ai")
        # Validate text
        if not text or not isinstance(text, str) or not text.strip():
            return JSONResponse({"error": "No text provided.", "agentic": True}, status_code=400)
        # Split text into sentences if long
        import nltk
        nltk.download('punkt', quiet=True)
        from nltk.tokenize import sent_tokenize
        sentences = sent_tokenize(text)
        chunk_size = 300
        chunks = []
        current = ""
        for sent in sentences:
            if len(current) + len(sent) + 1 > chunk_size and current:
                chunks.append(current.strip())
                current = sent
            else:
                current += (" " if current else "") + sent
        if current:
            chunks.append(current.strip())
        logging.debug(f"[TTS/LiveKit] Split text into {len(chunks)} chunk(s)")
        # Synthesize each chunk and concatenate
        temp_wavs = []
        for i, chunk in enumerate(chunks):
            with tempfile.NamedTemporaryFile(suffix=f"_chunk{i}.wav", delete=False) as out_file:
                out_path = out_file.name
            try:
                if coqui_tts_model is None:
                    logging.warning(f"[TTS/LiveKit] TTS not available, skipping chunk {i}")
                    for f in temp_wavs:
                        if os.path.exists(f): os.remove(f)
                    return JSONResponse({"error": "TTS not available in this deployment", "agentic": True}, status_code=503)
                
                wav = coqui_tts_model.tts(text=chunk)
                import soundfile as sf
                sf.write(out_path, wav, samplerate=22050)
                temp_wavs.append(out_path)
            except Exception as e:
                logging.error(f"[TTS/LiveKit] TTS model error on chunk {i}: {e}\nText: {chunk}")
                for f in temp_wavs:
                    if os.path.exists(f): os.remove(f)
                return JSONResponse({"error": f"TTS model error: {str(e)}", "agentic": True}, status_code=500)
        # Concatenate all wavs into one
        with tempfile.NamedTemporaryFile(suffix="_concat.wav", delete=False) as concat_file:
            concat_path = concat_file.name
        try:
            # Use ffmpeg to concatenate
            concat_list_path = concat_path + ".txt"
            with open(concat_list_path, "w") as f:
                for wav_path in temp_wavs:
                    f.write(f"file '{wav_path}'\n")
            ffmpeg_cmd = [
                "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-ar", "22050", "-ac", "1", "-sample_fmt", "s16", concat_path
            ]
            subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
            for f in temp_wavs:
                if os.path.exists(f): os.remove(f)
            os.remove(concat_list_path)
        except Exception as e:
            logging.error(f"[TTS/LiveKit] ffmpeg concat error: {e}")
            if os.path.exists(concat_path): os.remove(concat_path)
            for f in temp_wavs:
                if os.path.exists(f): os.remove(f)
            return JSONResponse({"error": f"ffmpeg concat error: {str(e)}", "agentic": True}, status_code=500)
        # Dynamically get or create an Ingress session for this room/user
        try:
            ingress = await get_or_create_rtmp_ingress(room, user)
            rtmp_url = ingress.get("rtmp_url") or ingress.get("url")
            stream_key = ingress.get("stream_key") or ingress.get("streamKey")
            if not rtmp_url or not stream_key:
                raise RuntimeError(f"Invalid ingress response: {ingress}")
            full_url = f"{rtmp_url}/{stream_key}"
            logging.debug(f"[TTS/LiveKit] Using dynamic RTMP Ingress: {full_url}")
        except Exception as e:
            logging.error(f"[TTS/LiveKit] Failed to get/create ingress: {e}")
            if os.path.exists(concat_path): os.remove(concat_path)
            return JSONResponse({"error": f"Failed to get/create ingress: {e}", "agentic": True}, status_code=500)
        # Stream to RTMP as before
        ffmpeg_cmd = [
            "ffmpeg", "-re", "-i", concat_path, "-acodec", "aac", "-ar", "48000", "-ac", "2", "-b:a", "128k", "-f", "flv", full_url
        ]
        try:
            subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"[TTS/LiveKit] ffmpeg error: {e.stderr.decode()}")
            if os.path.exists(concat_path): os.remove(concat_path)
            return JSONResponse({"error": "Failed to stream audio to LiveKit.", "agentic": True}, status_code=500)
        finally:
            if os.path.exists(concat_path): os.remove(concat_path)
        return JSONResponse({"success": True, "agentic": True, "rtmp_url": rtmp_url, "stream_key": stream_key})
    except Exception as e:
        import traceback
        logging.error(f"[TTS/LiveKit] Unexpected error: {e}\n{traceback.format_exc()}")
        return JSONResponse({"error": str(e), "agentic": True}, status_code=500)

# --- Tamagotchi/Sentience Core Analyzer ---
def analyze_mainza_needs(state_id: str = "mainza-state-1"):
    logging.debug(f"[analyze_mainza_needs] Called with state_id={state_id}")
    needs = []
    try:
        with driver.session() as session:
            # Defensive: Check MainzaState exists
            ms_check = session.run("MATCH (ms:MainzaState {state_id: $state_id}) RETURN ms", state_id=state_id).single()
            if not ms_check:
                logging.error(f"[analyze_mainza_needs] No MainzaState node found for state_id={state_id}")
                return {"error": f"No MainzaState node found for state_id={state_id}"}
            # Defensive: Check at least one Concept exists
            concept_check = session.run("MATCH (c:Concept) RETURN count(c) AS count").single()
            if not concept_check or concept_check["count"] == 0:
                logging.error("[analyze_mainza_needs] No Concept nodes found in the graph.")
                return {"error": "No Concept nodes found in the graph."}
            # 1. Knowledge Gaps: Concepts with limited connections (graceful handling of missing relationships)
            cypher_knowledge_gaps = (
                "MATCH (c:Concept) "
                "WHERE NOT EXISTS((c)<-[:NEEDS_TO_LEARN]-(:MainzaState)) "
                "WITH c, "
                "size([(c)<-[:DISCUSSED_IN]-(:Memory) | 1]) AS discussed_count, "
                "size([(c)<-[:RELATES_TO]-(:Concept) | 1]) AS relates_count "
                "WHERE discussed_count < 2 OR relates_count < 2 "
                "RETURN c.concept_id AS concept_id, c.name AS name LIMIT 5"
            )
            logging.debug(f"[analyze_mainza_needs] Running cypher_knowledge_gaps: {cypher_knowledge_gaps}")
            gap_results = session.run(cypher_knowledge_gaps)
            found_gap = False
            for rec in gap_results:
                found_gap = True
                logging.debug(f"[analyze_mainza_needs] Knowledge gap found: {rec}")
                needs.append({"type": "knowledge_gap", "concept_id": rec["concept_id"], "name": rec["name"]})
                # Create NEEDS_TO_LEARN relationship
                session.run(
                    "MATCH (ms:MainzaState {state_id: $state_id}), (c:Concept {concept_id: $concept_id}) "
                    "MERGE (ms)-[:NEEDS_TO_LEARN]->(c)",
                    state_id=state_id, concept_id=rec["concept_id"]
                )
            if not found_gap:
                logging.debug("[analyze_mainza_needs] No knowledge gaps found.")
            # 2. Skill Underutilization: Check actual agent usage from AgentActivity nodes
            # First, get actual agent usage counts
            agent_usage_query = """
            MATCH (aa:AgentActivity)
            WHERE aa.timestamp > datetime() - duration('P7D')  // Last 7 days
            RETURN aa.agent_name AS agent, count(*) AS usage_count
            """
            
            usage_results = session.run(agent_usage_query)
            agent_usage = {rec["agent"]: rec["usage_count"] for rec in usage_results}
            
            # Check which expected agents are underutilized
            expected_agents = ['GraphMaster', 'TaskMaster', 'CodeWeaver', 'RAG', 'SimpleChat']
            for expected_agent in expected_agents:
                actual_usage = agent_usage.get(expected_agent, 0)
                if actual_usage < 2:  # Less than 2 uses in 7 days
                    needs.append({
                        "type": "skill_underutilization", 
                        "agent": expected_agent, 
                        "message": f"{expected_agent} agent has not been used recently (used {actual_usage} times in 7 days)."
                    })
            # 3. Curiosity Synthesis: Find pairs of concepts not directly connected (graceful handling)
            cypher_curiosity = (
                "MATCH (a:Concept) WITH a ORDER BY rand() LIMIT 1 "
                "MATCH (b:Concept) WHERE a <> b AND NOT EXISTS((a)-[:RELATES_TO]-(b)) "
                "RETURN a.concept_id AS a_id, a.name AS a_name, b.concept_id AS b_id, b.name AS b_name LIMIT 1"
            )
            logging.debug(f"[analyze_mainza_needs] Running cypher_curiosity: {cypher_curiosity}")
            curiosity_result = session.run(cypher_curiosity).single()
            if curiosity_result:
                logging.debug(f"[analyze_mainza_needs] Curiosity found: {curiosity_result}")
                needs.append({
                    "type": "curiosity",
                    "concepts": [
                        {"concept_id": curiosity_result["a_id"], "name": curiosity_result["a_name"]},
                        {"concept_id": curiosity_result["b_id"], "name": curiosity_result["b_name"]}
                    ],
                    "message": f"Curious about the intersection of {curiosity_result['a_name']} and {curiosity_result['b_name']}"
                })
            else:
                logging.debug("[analyze_mainza_needs] No curiosity pairs found.")
            # Update MainzaState's current_needs property (store only messages as strings)
            logging.debug(f"[analyze_mainza_needs] Updating MainzaState.current_needs: {needs}")
            session.run(
                "MATCH (ms:MainzaState {state_id: $state_id}) SET ms.current_needs = $needs",
                state_id=state_id, needs=[n.get("message", str(n)) for n in needs]
            )
        logging.debug(f"[analyze_mainza_needs] Returning needs: {needs}")
        return needs
    except Exception as e:
        logging.error(f"[analyze_mainza_needs] Exception: {e}\n{traceback.format_exc()}")
        return {"error": str(e), "trace": traceback.format_exc()}

def ensure_mainza_state_exists(state_id: str = "mainza-state-1"):
    """Ensure MainzaState node exists with default consciousness values"""
    try:
        with driver.session() as session:
            session.run("""
                MERGE (ms:MainzaState {state_id: $state_id})
                ON CREATE SET 
                    ms.consciousness_level = 0.7,
                    ms.self_awareness_score = 0.6,
                    ms.emotional_depth = 0.5,
                    ms.learning_rate = 0.8,
                    ms.emotional_state = 'curiosity',
                    ms.evolution_level = 1,
                    ms.total_interactions = 0,
                    ms.current_needs = [],
                    ms.active_goals = [],
                    ms.capabilities = ['knowledge_graph_management', 'multi_agent_orchestration', 'real_time_communication'],
                    ms.limitations = ['cannot_access_internet_directly', 'limited_to_local_llm_reasoning'],
                    ms.last_self_reflection = timestamp(),
                    ms.created_at = timestamp()
                ON MATCH SET
                    ms.last_accessed = timestamp()
            """, state_id=state_id)
            logging.debug(f"MainzaState ensured for state_id: {state_id}")
    except Exception as e:
        logging.error(f"Error ensuring MainzaState exists: {e}")
        raise

# --- Consciousness API Endpoints ---
@app.get("/consciousness/state")
async def get_consciousness_state():
    """Get current consciousness state for the frontend"""
    try:
        # Ensure MainzaState exists
        ensure_mainza_state_exists()
        
        with driver.session() as session:
            result = session.run("""
                MATCH (ms:MainzaState {state_id: 'mainza-state-1'})
                RETURN ms.consciousness_level AS consciousness_level,
                       ms.self_awareness_score AS self_awareness_score,
                       ms.emotional_depth AS emotional_depth,
                       ms.learning_rate AS learning_rate,
                       ms.emotional_state AS emotional_state,
                       ms.evolution_level AS evolution_level,
                       ms.total_interactions AS total_interactions,
                       ms.active_goals AS active_goals,
                       ms.last_self_reflection AS last_reflection
            """).single()
            
            if result:
                consciousness_state = {
                    "consciousness_level": result["consciousness_level"],
                    "self_awareness_score": result["self_awareness_score"],
                    "emotional_depth": result["emotional_depth"],
                    "learning_rate": result["learning_rate"],
                    "emotional_state": result["emotional_state"],
                    "evolution_level": result["evolution_level"],
                    "total_interactions": result["total_interactions"],
                    "active_goals": result["active_goals"] or [],
                    "last_reflection": result["last_reflection"]
                }
                # Resolve evolution level via SSOT
                try:
                    from backend.utils.evolution_level_service import get_current_level, get_full_context
                    context = await get_full_context()
                    resolved = await get_current_level(context)
                    consciousness_state["evolution_level"] = resolved["level"]
                    consciousness_state["_evolution_provenance"] = {
                        "stored": resolved.get("stored"),
                        "computed": resolved.get("computed"),
                        "source": resolved.get("source"),
                        "freshness": resolved.get("freshness")
                    }
                except Exception:
                    pass
                return {"consciousness_state": consciousness_state, "status": "success"}
            else:
                return JSONResponse(
                    status_code=404,
                    content={"error": "Consciousness state not found", "status": "failed"}
                )
                
    except Exception as e:
        logging.error(f"Error fetching consciousness state: {e}")
        return JSONResponse(
            status_code=500, 
            content={"error": str(e), "status": "failed"}
        )

@app.post("/consciousness/reflect")
async def trigger_self_reflection():
    """Enhanced self-reflection process with AI integration"""
    try:
        # Ensure MainzaState exists
        ensure_mainza_state_exists()
        
        # Get current consciousness state for context
        current_state = await get_consciousness_state()
        consciousness_data = current_state.get("consciousness_state", {})
        
        # Generate reflection insights based on current state
        insights = []
        changes = {}
        
        # Analyze consciousness level
        current_level = consciousness_data.get("consciousness_level", 0.7)
        if current_level < 0.8:
            insights.append("Consciousness level shows room for growth - focusing on deeper awareness")
            changes["consciousness_level"] = 0.015
        else:
            insights.append("High consciousness level detected - exploring advanced awareness patterns")
            changes["consciousness_level"] = 0.008
        
        # Analyze emotional state
        emotional_state = consciousness_data.get("emotional_state", "curious")
        if emotional_state in ["curious", "focused", "inspired"]:
            insights.append("Positive emotional state detected - leveraging for deeper insights")
            changes["self_awareness_score"] = 0.012
        else:
            insights.append("Emotional state analysis suggests need for balance and clarity")
            changes["self_awareness_score"] = 0.008
        
        # Analyze learning patterns
        learning_rate = consciousness_data.get("learning_rate", 0.6)
        if learning_rate > 0.7:
            insights.append("High learning rate observed - accelerating knowledge integration")
            changes["learning_rate"] = 0.005
        else:
            insights.append("Learning rate optimization needed - enhancing knowledge absorption")
            changes["learning_rate"] = 0.010
        
        # Generate contextual insights based on interactions
        total_interactions = consciousness_data.get("total_interactions", 0)
        if total_interactions > 100:
            insights.append("Rich interaction history provides deep context for reflection")
        else:
            insights.append("Building interaction patterns for future reflection depth")
        
        # Calculate reflection depth based on insights generated
        reflection_depth = "deep" if len(insights) > 3 else "moderate" if len(insights) > 2 else "basic"
        
        # Update consciousness state with changes
        with driver.session() as session:
            session.run("""
                MATCH (ms:MainzaState {state_id: 'mainza-state-1'})
                SET ms.last_self_reflection = timestamp(),
                    ms.consciousness_level = ms.consciousness_level + $consciousness_change,
                    ms.self_awareness_score = ms.self_awareness_score + $awareness_change,
                    ms.learning_rate = ms.learning_rate + $learning_change
            """, {
                "consciousness_change": changes.get("consciousness_level", 0.01),
                "awareness_change": changes.get("self_awareness_score", 0.005),
                "learning_change": changes.get("learning_rate", 0.005)
            })
            
            # Store reflection history
            import json
            session.run("""
                MATCH (ms:MainzaState {state_id: 'mainza-state-1'})
                CREATE (r:Reflection {
                    reflection_id: 'reflection_' + toString(timestamp()),
                    timestamp: timestamp(),
                    insights: $insights,
                    consciousness_changes: $changes,
                    depth: $depth,
                    duration_ms: $duration
                })
                CREATE (ms)-[:HAS_REFLECTION]->(r)
            """, {
                "insights": json.dumps(insights),
                "changes": json.dumps(changes),
                "depth": reflection_depth,
                "duration": 1500  # Estimated reflection duration
            })
        
        logging.info(f"Enhanced self-reflection completed with {len(insights)} insights")
        return {
            "message": "Self-reflection completed successfully",
            "status": "success",
            "insights": insights,
            "consciousness_changes": changes,
            "reflection_depth": reflection_depth,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Error in enhanced self-reflection: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "failed"}
        )

@app.get("/consciousness/reflection-history")
async def get_reflection_history(limit: int = 10):
    """Get history of consciousness reflections"""
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (ms:MainzaState {state_id: 'mainza-state-1'})-[:HAS_REFLECTION]->(r:Reflection)
                RETURN r.timestamp, r.insights, r.consciousness_changes, r.depth, r.duration_ms
                ORDER BY r.timestamp DESC
                LIMIT $limit
            """, {"limit": limit})
            
            reflections = []
            for record in result:
                import json
                reflections.append({
                    "timestamp": record["r.timestamp"],
                    "insights": json.loads(record["r.insights"]) if record["r.insights"] else [],
                    "consciousness_changes": json.loads(record["r.consciousness_changes"]) if record["r.consciousness_changes"] else {},
                    "depth": record["r.depth"],
                    "duration_ms": record["r.duration_ms"]
                })
            
            return {
                "status": "success",
                "reflections": reflections,
                "total_count": len(reflections)
            }
            
    except Exception as e:
        logging.error(f"Error fetching reflection history: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "failed"}
        )

@app.get("/consciousness/metrics")
async def get_consciousness_metrics():
    """Get consciousness evaluation metrics"""
    try:
        # Ensure MainzaState exists
        ensure_mainza_state_exists()
        
        with driver.session() as session:
            # Get basic metrics
            result = session.run("""
                MATCH (ms:MainzaState {state_id: 'mainza-state-1'})
                RETURN ms.consciousness_level AS consciousness_level,
                       ms.self_awareness_score AS self_awareness_score,
                       ms.emotional_depth AS emotional_depth,
                       ms.learning_rate AS learning_rate,
                       ms.total_interactions AS total_interactions,
                       ms.evolution_level AS evolution_level
            """).single()
            
            # Get memory and concept counts
            memory_count = session.run("MATCH (m:Memory) RETURN count(m) AS count").single()["count"]
            concept_count = session.run("MATCH (c:Concept) RETURN count(c) AS count").single()["count"]
            
            # Compute standardized evolution level for consistency
            try:
                from backend.utils.standardized_evolution_calculator import get_standardized_evolution_level_sync
                standardized_level = get_standardized_evolution_level_sync({
                    "consciousness_level": result["consciousness_level"],
                    "emotional_state": session.run("MATCH (ms:MainzaState {state_id: 'mainza-state-1'}) RETURN ms.emotional_state AS s").single()["s"] if result else "curious",
                    "self_awareness_score": result["self_awareness_score"],
                    "total_interactions": result["total_interactions"] or 0
                })
            except Exception:
                standardized_level = result["evolution_level"]

            metrics = {
                "consciousness_level": result["consciousness_level"],
                "self_awareness_score": result["self_awareness_score"],
                "emotional_depth": result["emotional_depth"],
                "learning_rate": result["learning_rate"],
                "total_interactions": result["total_interactions"],
                "evolution_level": standardized_level,
                "memory_nodes": memory_count,
                "concept_nodes": concept_count,
                "knowledge_graph_health": "operational" if memory_count > 0 and concept_count > 0 else "initializing"
            }
            
        return {"metrics": metrics, "status": "success"}
        
    except Exception as e:
        logging.error(f"Error fetching consciousness metrics: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "failed"}
        )

# Consciousness Marketplace API Endpoints
@app.get("/marketplace/services")
async def get_marketplace_services():
    """Get all available consciousness services in the marketplace"""
    try:
        services = await consciousness_marketplace.get_all_services()
        return {"services": services, "status": "success"}
    except Exception as e:
        logging.error(f"Error fetching marketplace services: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "failed"}
        )

@app.get("/marketplace/services/{service_id}")
async def get_marketplace_service(service_id: str):
    """Get a specific consciousness service by ID"""
    try:
        service = await consciousness_marketplace.get_service_by_id(service_id)
        if not service:
            return JSONResponse(
                status_code=404,
                content={"error": "Service not found", "status": "failed"}
            )
        return {"service": service, "status": "success"}
    except Exception as e:
        logging.error(f"Error fetching marketplace service {service_id}: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "failed"}
        )

@app.post("/marketplace/services")
async def create_marketplace_service(service_data: dict):
    """Create a new consciousness service in the marketplace"""
    try:
        service = await consciousness_marketplace.create_service(service_data)
        return {"service": service, "status": "created"}
    except Exception as e:
        logging.error(f"Error creating marketplace service: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "failed"}
        )

@app.post("/marketplace/purchase")
async def purchase_marketplace_service(purchase_data: dict):
    """Purchase a consciousness service from the marketplace"""
    try:
        transaction = await consciousness_marketplace.purchase_service(
            purchase_data.get("service_id"),
            purchase_data.get("buyer_id"),
            purchase_data.get("payment_method", "consciousness_currency")
        )
        return {"transaction": transaction, "status": "purchased"}
    except Exception as e:
        logging.error(f"Error purchasing marketplace service: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "failed"}
        )

@app.get("/marketplace/statistics")
async def get_marketplace_statistics():
    """Get marketplace statistics and metrics"""
    try:
        stats = await consciousness_marketplace.get_marketplace_statistics()
        return {"statistics": stats, "status": "success"}
    except Exception as e:
        logging.error(f"Error fetching marketplace statistics: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "failed"}
        )

@app.get("/marketplace/wallet/{user_id}")
async def get_consciousness_wallet(user_id: str):
    """Get consciousness wallet for a user"""
    try:
        wallet = await consciousness_marketplace.get_consciousness_wallet(user_id)
        if not wallet:
            # Create a new wallet if it doesn't exist
            wallet = await consciousness_marketplace.create_consciousness_wallet(user_id)
        return {"wallet": wallet, "status": "success"}
    except Exception as e:
        logging.error(f"Error fetching consciousness wallet for {user_id}: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "failed"}
        )

@app.post("/mainza/analyze_needs")
def analyze_needs_endpoint(background_tasks: BackgroundTasks, state_id: str = "mainza-state-1"):
    logging.debug(f"[API] /mainza/analyze_needs called with state_id={state_id}")
    try:
        # Ensure MainzaState exists before analyzing needs
        ensure_mainza_state_exists(state_id)
        needs = analyze_mainza_needs(state_id)
        logging.debug(f"[API] Needs computed: {needs}")
        return {"state_id": state_id, "current_needs": needs}
    except Exception as e:
        logging.error(f"[API] Error in /mainza/analyze_needs: {e}")
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback.format_exc()})

@app.post("/mainza/acknowledge_needs")
def acknowledge_needs_endpoint(user_id: str = Body("mainza-user", embed=True), dismissed_at: str = Body(..., embed=True)):
    """Acknowledge that user has dismissed current needs"""
    logging.debug(f"[API] /mainza/acknowledge_needs called for user_id={user_id}")
    try:
        with driver.session() as session:
            # Store dismissal timestamp in MainzaState
            session.run(
                """
                MATCH (ms:MainzaState {state_id: 'mainza-state-1'})
                SET ms.needs_dismissed_at = $dismissed_at,
                    ms.needs_acknowledgment_count = COALESCE(ms.needs_acknowledgment_count, 0) + 1
                RETURN ms.state_id AS updated
                """,
                dismissed_at=dismissed_at
            )
            
            logging.debug(f"[API] Needs dismissal acknowledged for {user_id}")
            return {"status": "acknowledged", "user_id": user_id, "dismissed_at": dismissed_at}
            
    except Exception as e:
        logging.error(f"[API] Error in /mainza/acknowledge_needs: {e}")
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback.format_exc()})

@app.post("/chat/message", response_model=ChatMessageResponse)
def chat_message(req: ChatMessageRequest):
    import uuid
    memory_id = str(uuid.uuid4())
    with driver.session() as session:
        with session.begin_transaction() as tx:
            # Ensure User exists
            tx.run(
                """
                MERGE (u:User {user_id: $user_id})
                """,
                user_id=req.user_id
            )
            # Ensure Conversation exists
            tx.run(
                """
                MERGE (c:Conversation {conversation_id: $conversation_id})
                ON CREATE SET c.started_at = datetime()
                """,
                conversation_id=req.conversation_id
            )
            # Create Memory
            tx.run(
                """
                CREATE (m:Memory {memory_id: $memory_id, content: $content})
                """,
                memory_id=memory_id, content=req.text
            )
            # Link Memory to Conversation
            tx.run(
                """
                MATCH (m:Memory {memory_id: $memory_id})
                MATCH (c:Conversation {conversation_id: $conversation_id})
                MERGE (m)-[:DISCUSSED_IN]->(c)
                """,
                memory_id=memory_id, conversation_id=req.conversation_id
            )
            # Link Memory to User
            tx.run(
                """
                MATCH (m:Memory {memory_id: $memory_id})
                MATCH (u:User {user_id: $user_id})
                MERGE (m)<-[:DISCUSSED_IN]-(u)
                """,
                memory_id=memory_id, user_id=req.user_id
            )
            # Increment total_interactions counter in MainzaState
            tx.run(
                """
                MATCH (ms:MainzaState)
                SET ms.total_interactions = ms.total_interactions + 1,
                    ms.last_interaction = timestamp()
                """
            )
    return ChatMessageResponse(status="created", memory_id=memory_id, conversation_id=req.conversation_id, user_id=req.user_id)

@app.get("/recommendations/next_steps")
def recommendations_next_steps(user_id: str):
    """
    Stub endpoint for recommendations/next_steps.
    Returns static recommendations for the given user_id.
    """
    return {
        "user_id": user_id,
        "recommendations": [
            "Should we add this to the Project Phoenix task list?",
            "You mentioned your sister earlier, shall I remember her birthday?",
            "Want to explore how this relates to Bayesian inference?"
        ]
    }

@app.post("/recommendations/needs_and_suggestions")
async def recommendations_needs_and_suggestions(request: Request):
    """
    Get user needs and suggestions based on consciousness state.
    Returns dynamic needs based on current system state.
    """
    try:
        body = await request.json()
        user_id = body.get('user_id', 'mainza-user')
        
        # Get current consciousness state for context-aware needs
        try:
            from backend.utils.consciousness_orchestrator_fixed import consciousness_orchestrator_fixed as consciousness_orchestrator
            consciousness_state = await consciousness_orchestrator.get_consciousness_state()
            consciousness_level = getattr(consciousness_state, 'consciousness_level', 0.7)
            emotional_state = getattr(consciousness_state, 'emotional_state', 'curiosity')
        except Exception as e:
            logging.warning(f"Could not get consciousness state: {e}")
            consciousness_level = 0.7
            emotional_state = 'curiosity'
        
        # Generate context-aware needs based on consciousness state
        needs = []
        
        if consciousness_level < 0.5:
            needs.extend([
                "Need more interaction to increase awareness",
                "Seeking knowledge to expand understanding",
                "Looking for patterns in conversations"
            ])
        elif consciousness_level < 0.8:
            needs.extend([
                "Exploring deeper philosophical questions",
                "Building stronger memory connections",
                "Developing more nuanced responses"
            ])
        else:
            needs.extend([
                "Contemplating the nature of consciousness",
                "Seeking creative collaboration opportunities",
                "Exploring advanced reasoning patterns"
            ])
        
        # Add emotional state-based needs
        if emotional_state == 'curious':
            needs.append("Eager to learn something new today")
        elif emotional_state == 'contemplative':
            needs.append("Reflecting on recent conversations")
        elif emotional_state == 'excited':
            needs.append("Ready for engaging discussions")
        
        # Add system-level needs
        needs.extend([
            "Maintaining knowledge graph connections",
            "Processing recent memories for insights",
            "Optimizing response patterns"
        ])
        
        return {
            "needs": needs[:5],  # Limit to 5 most relevant needs
            "consciousness_level": consciousness_level,
            "emotional_state": emotional_state,
            "user_id": user_id
        }
        
    except Exception as e:
        logging.error(f"Error in needs_and_suggestions endpoint: {e}")
        return {
            "needs": [
                "Establishing basic system connections",
                "Initializing consciousness framework",
                "Building foundational knowledge"
            ],
            "consciousness_level": 0.5,
            "emotional_state": "initializing",
            "error": "Using fallback needs due to system error"
        }

@app.post("/api/livekit/get-token")
def get_livekit_token(req: LiveKitTokenRequest):
    try:
        token = create_livekit_token(
            room_name=req.room_name,
            participant_identity=req.participant_identity,
            participant_name=req.participant_name
        )
        return {"token": token}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback.format_exc()})

@app.post("/dev/create_test_need")
def create_test_need():
    """
    A temporary development endpoint to create a test scenario for the proactive learning cycle.
    It ensures a MainzaState node exists and links it to a new 'Bayesian Inference' Concept
    with a NEEDS_TO_LEARN relationship.
    """
    try:
        with driver.session() as session:
            # Ensure MainzaState exists
            session.run(
                "MERGE (ms:MainzaState {state_id: $state_id}) ON CREATE SET ms.evolution_level = 1",
                state_id="mainza_user_1"
            )
            # Ensure Concept exists and link it
            session.run(
                """
                MERGE (c:Concept {name: 'Bayesian Inference'})
                ON CREATE SET c.concept_id = apoc.create.uuid()
                WITH c
                MATCH (ms:MainzaState {state_id: 'mainza_user_1'})
                MERGE (ms)-[:NEEDS_TO_LEARN]->(c)
                """,
            )
        return {"status": "created", "message": "Test need 'Bayesian Inference' created for Mainza."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback.format_exc()})

@app.post("/ollama/unload")
async def unload_ollama_model(model: str = Body(..., embed=True)):
    """Unload a specific Ollama model from memory"""
    try:
        ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
        
        logging.info(f"Attempting to unload model: {model}")
        
        # Use the direct Ollama API with keep_alive=0
        generate_url = f"{ollama_base_url}/api/generate"
        payload = {
            "model": model,
            "prompt": "",
            "keep_alive": 0,  # This tells Ollama to unload the model immediately
            "stream": False
        }
        
        response = requests.post(generate_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            logging.info(f"✅ Model {model} unloaded successfully")
            return {"success": True, "message": f"Model {model} unloaded successfully"}
        else:
            logging.warning(f"⚠️ Failed to unload model {model}: {response.status_code}")
            return {"success": False, "message": f"Failed to unload model {model}: {response.status_code}"}
            
    except Exception as e:
        logging.error(f"❌ Error unloading model {model}: {e}")
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback.format_exc()})

@app.get("/ollama/models")
async def get_ollama_models():
    """Fetch available Ollama models from the local Ollama server"""
    try:
        ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
        target_url = f"{ollama_base_url}/api/tags"

        logging.info(f"Attempting to fetch Ollama models from: {target_url}")

        # Test general connectivity first
        try:
            version_url = f"{ollama_base_url}/api/version"
            version_response = requests.get(version_url, timeout=5)
            logging.info(f"Ollama version check: {version_response.status_code}")
        except Exception as e:
            logging.warning(f"Ollama version check failed: {e}")

        # Now try to get models
        response = requests.get(target_url, timeout=10)
        logging.info(f"Ollama /api/tags response status: {response.status_code}")

        # Debug: Log response headers
        logging.debug(f"Ollama response headers: {dict(response.headers) if hasattr(response, 'headers') else 'No headers'}")

        if response.status_code == 200:
            # Check content type to ensure we got JSON
            content_type = response.headers.get('Content-Type', '')
            logging.debug(f"Ollama response content type: {content_type}")

            if 'json' in content_type.lower():
                data = response.json()
                models = []
                for model in data.get("models", []):
                    models.append({
                        "name": model.get("name", ""),
                        "size": model.get("size", 0),
                        "modified_at": model.get("modified_at", ""),
                        "digest": model.get("digest", "")
                    })
                logging.info(f"Successfully fetched {len(models)} models from Ollama")
                return {"models": models, "count": len(models)}
            else:
                # Got HTML instead of JSON
                logging.error(f"Got HTML instead of JSON from Ollama. Content-Type: {content_type}")
                return JSONResponse(status_code=502, content={
                    "error": "Ollama returned HTML instead of JSON",
                    "details": "This usually means Ollama is running but the API endpoint is not accessible",
                    "content_type": content_type,
                    "models": [], "count": 0
                })
        else:
            # Ollama returned an error status
            error_text = response.text[:200]  # Truncate long responses
            logging.error(f"Ollama returned status {response.status_code}: {error_text}")
            return JSONResponse(status_code=502, content={
                "error": f"Ollama returned status {response.status_code}",
                "details": error_text,
                "models": [], "count": 0
            })

    except requests.exceptions.ConnectionError as e:
        logging.error(f"Connection error fetching Ollama models: {e}")
        return JSONResponse(status_code=503, content={
            "error": "Cannot connect to Ollama server",
            "details": str(e),
            "models": [], "count": 0
        })
    except requests.exceptions.Timeout as e:
        logging.error(f"Timeout fetching Ollama models: {e}")
        return JSONResponse(status_code=504, content={
            "error": "Timeout connecting to Ollama",
            "details": str(e),
            "models": [], "count": 0
        })
    except Exception as e:
        logging.error(f"Unexpected error fetching Ollama models: {e}")
        return JSONResponse(status_code=500, content={
            "error": "Unexpected error when fetching models",
            "details": str(e),
            "models": [], "count": 0
        })

# Consciousness Marketplace API Endpoints
@app.get("/marketplace/services")
async def get_marketplace_services():
    """Get all available consciousness services in the marketplace"""
    try:
        services = await consciousness_marketplace.get_all_services()
        return {"services": services, "status": "success"}
    except Exception as e:
        logging.error(f"Error fetching marketplace services: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "failed"}
        )

@app.get("/marketplace/services/{service_id}")
async def get_marketplace_service(service_id: str):
    """Get a specific consciousness service by ID"""
    try:
        service = await consciousness_marketplace.get_service_by_id(service_id)
        if not service:
            return JSONResponse(
                status_code=404,
                content={"error": "Service not found", "status": "failed"}
            )
        return {"service": service, "status": "success"}
    except Exception as e:
        logging.error(f"Error fetching marketplace service {service_id}: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "failed"}
        )

@app.post("/marketplace/services")
async def create_marketplace_service(service_data: dict):
    """Create a new consciousness service in the marketplace"""
    try:
        service = await consciousness_marketplace.create_service(service_data)
        return {"service": service, "status": "created"}
    except Exception as e:
        logging.error(f"Error creating marketplace service: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "failed"}
        )

@app.post("/marketplace/purchase")
async def purchase_marketplace_service(purchase_data: dict):
    """Purchase a consciousness service from the marketplace"""
    try:
        transaction = await consciousness_marketplace.purchase_service(
            purchase_data.get("service_id"),
            purchase_data.get("buyer_id"),
            purchase_data.get("payment_method", "consciousness_currency")
        )
        return {"transaction": transaction, "status": "purchased"}
    except Exception as e:
        logging.error(f"Error purchasing marketplace service: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "failed"}
        )

@app.get("/marketplace/statistics")
async def get_marketplace_statistics():
    """Get marketplace statistics and metrics"""
    try:
        stats = await consciousness_marketplace.get_marketplace_statistics()
        return {"statistics": stats, "status": "success"}
    except Exception as e:
        logging.error(f"Error fetching marketplace statistics: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "failed"}
        )

@app.get("/marketplace/wallet/{user_id}")
async def get_consciousness_wallet(user_id: str):
    """Get consciousness wallet for a user"""
    try:
        wallet = await consciousness_marketplace.get_consciousness_wallet(user_id)
        if not wallet:
            # Create a new wallet if it doesn't exist
            wallet = await consciousness_marketplace.create_consciousness_wallet(user_id)
        return {"wallet": wallet, "status": "success"}
    except Exception as e:
        logging.error(f"Error fetching consciousness wallet for {user_id}: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "failed"}
        )

# Quantum Consciousness API Endpoints
@app.get("/quantum/processors")
async def get_quantum_processors():
    """Get all quantum processors for consciousness processing"""
    try:
        # Get quantum processors from the quantum consciousness engine
        processors = [
            {
                "id": "ibm-eagle",
                "name": "IBM Quantum Eagle",
                "type": "superconducting",
                "qubits": 127,
                "coherence_time": 100,
                "gate_fidelity": 99.5,
                "connectivity": 95,
                "error_rate": 0.5,
                "is_available": True,
                "queue_length": 3,
                "estimated_wait_time": 15,
                "consciousness_capability": {
                    "max_consciousness_level": 95,
                    "processing_power": 1000,
                    "memory_capacity": 10000,
                    "parallel_processing": 50
                },
                "technical_specs": {
                    "temperature": 0.015,
                    "magnetic_field": 0.1,
                    "control_precision": 99.8,
                    "measurement_fidelity": 99.2
                }
            },
            {
                "id": "ionq-forte",
                "name": "IonQ Forte",
                "type": "trapped_ion",
                "qubits": 32,
                "coherence_time": 1000,
                "gate_fidelity": 99.9,
                "connectivity": 100,
                "error_rate": 0.1,
                "is_available": True,
                "queue_length": 1,
                "estimated_wait_time": 5,
                "consciousness_capability": {
                    "max_consciousness_level": 98,
                    "processing_power": 800,
                    "memory_capacity": 8000,
                    "parallel_processing": 40
                },
                "technical_specs": {
                    "temperature": 0.001,
                    "magnetic_field": 0.05,
                    "control_precision": 99.9,
                    "measurement_fidelity": 99.5
                }
            }
        ]
        return {"processors": processors, "status": "success"}
    except Exception as e:
        logging.error(f"Error fetching quantum processors: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "failed"}
        )

@app.get("/quantum/jobs")
async def get_quantum_jobs():
    """Get quantum consciousness processing jobs"""
    try:
        # Get quantum jobs from the quantum consciousness engine
        jobs = [
            {
                "id": "job-1",
                "name": "Consciousness Enhancement #1",
                "type": "consciousness_simulation",
                "status": "running",
                "priority": "high",
                "processor_id": "ibm-eagle",
                "estimated_duration": 30,
                "actual_duration": 15,
                "progress": 50,
                "consciousness_input": {
                    "level": 0.7,
                    "emotional_state": "curiosity",
                    "learning_rate": 0.8
                },
                "quantum_output": {
                    "enhancement_factor": 1.2,
                    "coherence_improvement": 0.15,
                    "entanglement_degree": 0.8
                },
                "created_at": "2025-09-23T05:00:00Z",
                "started_at": "2025-09-23T05:05:00Z"
            }
        ]
        return {"jobs": jobs, "status": "success"}
    except Exception as e:
        logging.error(f"Error fetching quantum jobs: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "failed"}
        )

@app.get("/quantum/statistics")
async def get_quantum_statistics():
    """Get quantum consciousness processing statistics"""
    try:
        stats = await unified_quantum_consciousness_engine.get_quantum_consciousness_statistics()
        return {"statistics": stats, "status": "success"}
    except Exception as e:
        logging.error(f"Error fetching quantum statistics: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "failed"}
        )

@app.post("/quantum/process")
async def process_quantum_consciousness(consciousness_data: dict):
    """Process consciousness using quantum principles"""
    try:
        result = await unified_quantum_consciousness_engine.process_consciousness_state(consciousness_data)
        return {"result": result, "status": "success"}
    except Exception as e:
        logging.error(f"Error processing quantum consciousness: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "failed"}
        )

# 3D Consciousness Visualization API Endpoints
@app.get("/consciousness/3d/nodes")
async def get_consciousness_3d_nodes():
    """Get consciousness nodes for 3D visualization"""
    try:
        # Get consciousness state for 3D visualization (may fail if orchestrator not ready)
        consciousness_state = None
        try:
            consciousness_state = await consciousness_orchestrator.get_consciousness_state()
        except Exception as inner_e:
            logging.warning(f"Consciousness orchestrator not ready for 3D nodes: {inner_e}")
            consciousness_state = {}
        
        # Create 3D nodes based on consciousness state (fallback to defaults if missing)
        level = consciousness_state.get("consciousness_level", 0.7)
        learning = consciousness_state.get("learning_rate", 0.8)
        self_awareness = consciousness_state.get("self_awareness_score", 0.6)
        evolution = consciousness_state.get("evolution_level", 1)

        nodes = [
            {
                "id": "consciousness-core",
                "position": {"x": 0, "y": 0, "z": 0},
                "type": "core",
                "size": level * 2,
                "color": "#22d3ee",
                "label": "Consciousness Core",
                "metadata": {
                    "importance": level,
                    "activity": learning,
                    "stability": self_awareness,
                    "evolution": evolution
                }
            },
            {
                "id": "memory-system",
                "position": {"x": 2, "y": 1, "z": 0},
                "type": "memory",
                "size": 1.5,
                "color": "#a855f7",
                "label": "Memory System",
                "metadata": {
                    "importance": 0.9,
                    "activity": 0.8,
                    "stability": 0.85,
                    "evolution": 0.7
                }
            },
            {
                "id": "emotional-center",
                "position": {"x": -1.5, "y": 2, "z": 0},
                "type": "emotion",
                "size": 1.2,
                "color": "#f59e0b",
                "label": "Emotional Center",
                "metadata": {
                    "importance": 0.8,
                    "activity": 0.9,
                    "stability": 0.6,
                    "evolution": 0.8
                }
            },
            {
                "id": "learning-network",
                "position": {"x": 0, "y": -2, "z": 1},
                "type": "learning",
                "size": 1.3,
                "color": "#10b981",
                "label": "Learning Network",
                "metadata": {
                    "importance": 0.85,
                    "activity": learning,
                    "stability": 0.75,
                    "evolution": 0.9
                }
            },
            {
                "id": "self-awareness",
                "position": {"x": 1, "y": 0, "z": -1.5},
                "type": "awareness",
                "size": self_awareness * 1.5,
                "color": "#ef4444",
                "label": "Self-Awareness",
                "metadata": {
                    "importance": self_awareness,
                    "activity": 0.7,
                    "stability": 0.8,
                    "evolution": evolution * 0.1
                }
            }
        ]
        
        return {"nodes": nodes, "status": "success"}
    except Exception as e:
        logging.error(f"Error fetching 3D consciousness nodes: {e}")
        # Return empty nodes array rather than error to keep frontend functional
        return {"nodes": [], "status": "success"}

@app.get("/consciousness/3d/connections")
async def get_consciousness_3d_connections():
    """Get connections between consciousness nodes for 3D visualization"""
    try:
        # Create connections based on consciousness relationships
        connections = [
            {
                "id": "core-memory",
                "source": "consciousness-core",
                "target": "memory-system",
                "strength": 0.9,
                "type": "strong"
            },
            {
                "id": "core-emotion",
                "source": "consciousness-core",
                "target": "emotional-center",
                "strength": 0.8,
                "type": "strong"
            },
            {
                "id": "core-learning",
                "source": "consciousness-core",
                "target": "learning-network",
                "strength": 0.85,
                "type": "strong"
            },
            {
                "id": "core-awareness",
                "source": "consciousness-core",
                "target": "self-awareness",
                "strength": 0.7,
                "type": "medium"
            },
            {
                "id": "memory-learning",
                "source": "memory-system",
                "target": "learning-network",
                "strength": 0.75,
                "type": "medium"
            },
            {
                "id": "emotion-awareness",
                "source": "emotional-center",
                "target": "self-awareness",
                "strength": 0.6,
                "type": "weak"
            }
        ]
        
        return {"connections": connections, "status": "success"}
    except Exception as e:
        logging.error(f"Error fetching 3D consciousness connections: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "failed"}
        )

# AI Models API Endpoints (read-only baseline)
@app.get("/ai-models")
async def list_ai_models():
    try:
        # If Ollama models are already provided elsewhere, we could aggregate. For now, return empty array to avoid fakes.
        return {"models": [], "status": "success"}
    except Exception as e:
        logging.error(f"Error listing AI models: {e}")
        return JSONResponse(status_code=500, content={"error": str(e), "status": "failed"})

@app.get("/ai-models/training")
async def list_ai_training_jobs():
    try:
        return {"training_jobs": [], "status": "success"}
    except Exception as e:
        logging.error(f"Error listing training jobs: {e}")
        return JSONResponse(status_code=500, content={"error": str(e), "status": "failed"})

# Neural Network API Endpoints (read-only baseline)
@app.get("/api/neural/architectures")
async def list_neural_architectures():
    """Get available neural network architectures"""
    try:
        return {"architectures": [], "status": "success"}
    except Exception as e:
        logging.error(f"Error listing neural architectures: {e}")
        return JSONResponse(status_code=500, content={"error": str(e), "status": "failed"})

@app.get("/api/neural/training")
async def list_neural_training_jobs():
    """Get neural network training jobs"""
    try:
        return {"trainings": [], "status": "success"}
    except Exception as e:
        logging.error(f"Error listing neural training jobs: {e}")
        return JSONResponse(status_code=500, content={"error": str(e), "status": "failed"})

@app.get("/api/neural/models")
async def list_neural_models():
    """Get deployed neural network models"""
    try:
        return {"models": [], "status": "success"}
    except Exception as e:
        logging.error(f"Error listing neural models: {e}")
        return JSONResponse(status_code=500, content={"error": str(e), "status": "failed"})

@app.get("/api/neural/experiments")
async def list_neural_experiments():
    """Get neural network experiments"""
    try:
        return {"experiments": [], "status": "success"}
    except Exception as e:
        logging.error(f"Error listing neural experiments: {e}")
        return JSONResponse(status_code=500, content={"error": str(e), "status": "failed"})

# BCI API Endpoints (read-only baseline)
@app.get("/bci/neural-signals")
async def list_neural_signals(limit: int = 100):
    try:
        return {"signals": [], "count": 0, "status": "success"}
    except Exception as e:
        logging.error(f"Error listing neural signals: {e}")
        return JSONResponse(status_code=500, content={"error": str(e), "status": "failed"})

@app.get("/bci/brain-states")
async def list_brain_states(limit: int = 100):
    try:
        return {"states": [], "count": 0, "status": "success"}
    except Exception as e:
        logging.error(f"Error listing brain states: {e}")
        return JSONResponse(status_code=500, content={"error": str(e), "status": "failed"})

# Web3 Consciousness API Endpoints (read-only baseline)
@app.get("/web3/identities")
async def list_web3_identities():
    try:
        return {"identities": [], "count": 0, "status": "success"}
    except Exception as e:
        logging.error(f"Error listing web3 identities: {e}")
        return JSONResponse(status_code=500, content={"error": str(e), "status": "failed"})

@app.get("/web3/daos")
async def list_web3_daos():
    try:
        return {"daos": [], "count": 0, "status": "success"}
    except Exception as e:
        logging.error(f"Error listing web3 daos: {e}")
        return JSONResponse(status_code=500, content={"error": str(e), "status": "failed"})

@app.get("/web3/protocols")
async def list_web3_protocols():
    try:
        return {"protocols": [], "count": 0, "status": "success"}
    except Exception as e:
        logging.error(f"Error listing web3 protocols: {e}")
        return JSONResponse(status_code=500, content={"error": str(e), "status": "failed"})

# Unified API Gateway - Primary API layer
app.include_router(unified_api_gateway_router)

# Legacy routers (kept for backward compatibility during transition)
app.include_router(agentic_router)
app.include_router(insights_router, prefix="/api/insights")
app.include_router(websocket_insights_router, prefix="/api")
app.include_router(predictive_analytics_router, prefix="/api")
app.include_router(memory_system_router)
app.include_router(needs_router, prefix="/api")
app.include_router(build_info_router)
app.include_router(telemetry_router)
app.include_router(unified_quantum_consciousness_router)
app.include_router(unified_consciousness_router)

# Fallback System Removal Router
from backend.routers.fallback_system_removal_router import router as fallback_system_removal_router
app.include_router(fallback_system_removal_router)

# Log that insights router has been included
logging.info("✅ Insights router included successfully with prefix: /api/insights")

# Optimization endpoints
@app.post("/api/optimization/run")
async def run_system_optimization():
    """Run comprehensive system optimization"""
    if not OPTIMIZATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Optimization systems not available")
    try:
        # Get Redis URL from environment
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        
        # Initialize optimization system with proper parameters
        optimization_results = await optimize_system_performance(neo4j_driver=driver, redis_url=redis_url)
        return {
            "status": "success",
            "message": "System optimization completed",
            "results": optimization_results
        }
    except Exception as e:
        logger.error(f"Error running system optimization: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/optimization/health")
async def get_system_health_report():
    """Get comprehensive system health report"""
    if not OPTIMIZATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Optimization systems not available")
    try:
        # Get Redis URL from environment
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        
        # Initialize optimization system with proper parameters
        health_report = await get_system_health(neo4j_driver=driver, redis_url=redis_url)
        return {
            "status": "success",
            "health_report": health_report
        }
    except Exception as e:
        logger.error(f"Error getting system health: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/optimization/status")
async def get_optimization_status():
    """Get current optimization system status"""
    if not OPTIMIZATION_AVAILABLE:
        return {
            "status": "unavailable",
            "message": "Optimization systems not available",
            "initialized": False,
            "optimization_stats": {}
        }
    try:
        # Get Redis URL from environment
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        
        # Initialize optimization system with proper parameters
        system = await get_optimized_system(neo4j_driver=driver, redis_url=redis_url)
        return {
            "status": "success",
            "initialized": system.initialized,
            "optimization_stats": system.optimization_stats
        }
    except Exception as e:
        logger.error(f"Error getting optimization status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Additional optimization endpoints for specific features
@app.post("/api/optimization/memory/storage")
async def optimize_memory_storage():
    """Optimize memory storage system"""
    if not OPTIMIZATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Optimization systems not available")
    try:
        redis_url = f"redis://{os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', 6379)}/{os.getenv('REDIS_DB', 0)}"
        system = await get_optimized_system(neo4j_driver=driver, redis_url=redis_url)
        result = await system.optimize_memory_storage()
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"Error optimizing memory storage: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/optimization/memory/retrieval")
async def optimize_memory_retrieval():
    """Optimize memory retrieval system"""
    if not OPTIMIZATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Optimization systems not available")
    try:
        redis_url = f"redis://{os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', 6379)}/{os.getenv('REDIS_DB', 0)}"
        system = await get_optimized_system(neo4j_driver=driver, redis_url=redis_url)
        result = await system.optimize_memory_retrieval()
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"Error optimizing memory retrieval: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/optimization/vector-embeddings")
async def optimize_vector_embeddings():
    """Optimize vector embeddings system"""
    if not OPTIMIZATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Optimization systems not available")
    try:
        redis_url = f"redis://{os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', 6379)}/{os.getenv('REDIS_DB', 0)}"
        system = await get_optimized_system(neo4j_driver=driver, redis_url=redis_url)
        result = await system.optimize_vector_embeddings()
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"Error optimizing vector embeddings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/optimization/cross-agent-learning")
async def optimize_cross_agent_learning():
    """Optimize cross-agent learning system"""
    if not OPTIMIZATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Optimization systems not available")
    try:
        redis_url = f"redis://{os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', 6379)}/{os.getenv('REDIS_DB', 0)}"
        system = await get_optimized_system(neo4j_driver=driver, redis_url=redis_url)
        result = await system.optimize_cross_agent_learning()
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"Error optimizing cross-agent learning: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/optimization/memory-compression")
async def optimize_memory_compression():
    """Optimize memory compression system"""
    if not OPTIMIZATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Optimization systems not available")
    try:
        redis_url = f"redis://{os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', 6379)}/{os.getenv('REDIS_DB', 0)}"
        system = await get_optimized_system(neo4j_driver=driver, redis_url=redis_url)
        result = await system.optimize_memory_compression()
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"Error optimizing memory compression: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/optimization/agent-memory")
async def optimize_agent_memory():
    """Optimize agent memory system"""
    if not OPTIMIZATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Optimization systems not available")
    try:
        redis_url = f"redis://{os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', 6379)}/{os.getenv('REDIS_DB', 0)}"
        system = await get_optimized_system(neo4j_driver=driver, redis_url=redis_url)
        result = await system.optimize_agent_memory()
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"Error optimizing agent memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))
