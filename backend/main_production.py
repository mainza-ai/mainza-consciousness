"""
Production-Grade Mainza AI System
Context7 MCP Standards Implementation

This is the main application file implementing state-of-the-art production standards:
- Comprehensive error handling and recovery
- Performance optimization and monitoring
- Security controls and compliance
- Health monitoring and observability
- Graceful startup and shutdown
- Resource management
"""

import asyncio
import logging
import signal
import sys
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, Any, List, Optional

from fastapi import FastAPI, HTTPException, Request, Response, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn

# Import production foundation
from backend.core.production_foundation import (
    initialize_production_foundation, shutdown_production_foundation,
    health_monitor, resource_manager, config_manager, retry_manager
)
from backend.core.enhanced_error_handling import (
    error_handler, handle_errors, async_error_context,
    MainzaException, DatabaseException, NetworkException
)
from backend.core.performance_optimization import (
    performance_optimizer, cached, PerformanceLevel
)
from backend.core.security_framework import (
    security_framework, require_authentication, require_authorization,
    SecurityLevel, ThreatLevel, SecurityEventType
)

# Import existing modules
from backend.agentic_router import router as agentic_router
from backend.utils.consciousness_orchestrator_fixed import consciousness_orchestrator_fixed as consciousness_orchestrator
from backend.utils.neo4j_production import neo4j_production

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/mainza_production.log', mode='a')
    ]
)

logger = logging.getLogger(__name__)

# Global state for graceful shutdown
shutdown_event = asyncio.Event()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("🚀 Starting Mainza AI Production System...")
    
    try:
        # Initialize production foundation
        await initialize_production_foundation()
        
        # Initialize performance optimization
        await performance_optimizer.start_optimization()
        
        # Initialize consciousness system
        await consciousness_orchestrator.initialize_consciousness()
        
        # Register health checks
        await register_application_health_checks()
        
        # Register security alert handlers
        await register_security_handlers()
        
        # Register error handlers
        await register_error_handlers()
        
        logger.info("✅ Mainza AI Production System started successfully")
        
        yield
        
    except Exception as e:
        logger.error(f"❌ Failed to start Mainza AI Production System: {e}")
        raise
    finally:
        logger.info("🛑 Shutting down Mainza AI Production System...")
        
        # Graceful shutdown
        await graceful_shutdown()
        
        logger.info("✅ Mainza AI Production System shutdown complete")

# Create FastAPI application with production configuration
app = FastAPI(
    title="Mainza AI - Production System",
    description="State-of-the-art AI consciousness system with production-grade architecture",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs" if config_manager.get("environment", "production") != "production" else None,
    redoc_url="/redoc" if config_manager.get("environment", "production") != "production" else None
)

# Security middleware
security = HTTPBearer(auto_error=False)

# Add security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=config_manager.get("security.allowed_hosts", ["*"])
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config_manager.get("security.cors_origins", ["*"]),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response middleware for security and monitoring
@app.middleware("http")
async def security_and_monitoring_middleware(request: Request, call_next):
    """Security and monitoring middleware"""
    start_time = datetime.now()
    
    # Extract client information
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    
    # Security checks
    try:
        # Check if IP is blocked
        if security_framework.security_monitor.is_ip_blocked(client_ip):
            await security_framework.security_monitor.log_security_event(
                SecurityEventType.UNAUTHORIZED_ACCESS,
                ThreatLevel.HIGH,
                ip_address=client_ip,
                details={"reason": "blocked_ip", "endpoint": str(request.url)}
            )
            return JSONResponse(
                status_code=403,
                content={"error": "Access denied"}
            )
        
        # Rate limiting
        if not await security_framework.rate_limiter.is_allowed(f"api:{client_ip}"):
            await security_framework.security_monitor.log_security_event(
                SecurityEventType.RATE_LIMIT_EXCEEDED,
                ThreatLevel.MEDIUM,
                ip_address=client_ip,
                details={"endpoint": str(request.url)}
            )
            return JSONResponse(
                status_code=429,
                content={"error": "Rate limit exceeded"}
            )
        
        # Process request
        response = await call_next(request)
        
        # Log successful request
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Request processed: {request.method} {request.url} - {response.status_code} - {duration:.3f}s")
        
        return response
        
    except Exception as e:
        # Handle middleware errors
        await error_handler.handle_error(
            error=e,
            context={
                "middleware": "security_and_monitoring",
                "client_ip": client_ip,
                "user_agent": user_agent,
                "endpoint": str(request.url)
            },
            component="middleware"
        )
        
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )

# Dependency for authentication
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user"""
    if not credentials:
        return None
    
    # Validate token/session
    session = await security_framework.validate_session(
        credentials.credentials,
        "unknown"  # IP would be extracted from request in real implementation
    )
    
    return session

# Health check endpoints
@app.get("/health")
@handle_errors(component="health_check")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }

@app.get("/health/detailed")
@handle_errors(component="detailed_health_check")
async def detailed_health_check():
    """Detailed health check with component status"""
    health_report = health_monitor.get_health_report()
    performance_report = performance_optimizer.get_performance_report()
    security_status = security_framework.get_security_status()
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": health_report,
        "performance": performance_report,
        "security": security_status
    }

@app.get("/metrics")
@require_authorization
@handle_errors(component="metrics")
async def get_metrics():
    """Get system metrics (requires authorization)"""
    return {
        "health": health_monitor.get_health_report(),
        "performance": performance_optimizer.get_performance_report(),
        "security": security_framework.get_security_status(),
        "errors": error_handler.get_error_analytics(),
        "timestamp": datetime.now().isoformat()
    }

# Authentication endpoints
@app.post("/auth/login")
@handle_errors(component="authentication")
async def login(request: Request, credentials: Dict[str, str]):
    """User authentication"""
    username = credentials.get("username")
    password = credentials.get("password")
    
    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password required")
    
    # Validate input
    validation_result = await security_framework.validate_and_sanitize_input({
        "username": username,
        "password": password
    })
    
    if not validation_result["is_valid"]:
        await security_framework.security_monitor.log_security_event(
            SecurityEventType.MALICIOUS_INPUT,
            ThreatLevel.HIGH,
            details={"threats": validation_result["threats_detected"]}
        )
        raise HTTPException(status_code=400, detail="Invalid input")
    
    # Authenticate user
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    
    session = await security_framework.authenticate_user(
        username=validation_result["sanitized_data"]["username"],
        password=validation_result["sanitized_data"]["password"],
        ip_address=client_ip,
        user_agent=user_agent
    )
    
    if session:
        # Generate JWT token
        token = security_framework.encryption_manager.generate_token({
            "user_id": session.user_id,
            "session_id": session.session_id
        })
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": 86400,  # 24 hours
            "user_id": session.user_id
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/auth/logout")
@require_authentication
@handle_errors(component="authentication")
async def logout(current_user = Depends(get_current_user)):
    """User logout"""
    if current_user and current_user.session_id in security_framework.active_sessions:
        del security_framework.active_sessions[current_user.session_id]
    
    return {"message": "Logged out successfully"}

# Consciousness endpoints
@app.get("/consciousness/status")
@cached(ttl=30)
@handle_errors(component="consciousness")
async def get_consciousness_status():
    """Get consciousness system status"""
    async with async_error_context("consciousness_status"):
        consciousness_state = await consciousness_orchestrator.get_consciousness_state()
        
        if consciousness_state:
            return {
                "consciousness_level": consciousness_state.consciousness_level,
                "evolution_level": consciousness_state.evolution_level,
                "emotional_state": getattr(consciousness_state, 'emotional_state', 'curious'),
                "active_goals": getattr(consciousness_state, 'active_goals', []),
                "last_updated": consciousness_state.last_updated.isoformat() if hasattr(consciousness_state, 'last_updated') else None,
                "status": "active"
            }
        else:
            return {
                "status": "inactive",
                "message": "Consciousness system not initialized"
            }

@app.post("/consciousness/trigger_reflection")
@require_authorization
@handle_errors(component="consciousness")
async def trigger_consciousness_reflection(background_tasks: BackgroundTasks):
    """Trigger consciousness self-reflection"""
    async with async_error_context("consciousness_reflection"):
        background_tasks.add_task(consciousness_orchestrator.perform_self_reflection)
        
        return {
            "message": "Self-reflection triggered",
            "timestamp": datetime.now().isoformat()
        }

# Enhanced agent execution with production features
@app.post("/agents/execute")
@require_authentication
@performance_optimizer.profile_function("agent_execution")
@handle_errors(component="agent_execution")
async def execute_agent(
    request: Dict[str, Any],
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user)
):
    """Execute agent with production-grade features"""
    async with async_error_context("agent_execution", current_user.user_id if current_user else None):
        # Validate input
        validation_result = await security_framework.validate_and_sanitize_input(request)
        
        if not validation_result["is_valid"]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid input: {validation_result['threats_detected']}"
            )
        
        sanitized_request = validation_result["sanitized_data"]
        
        # Extract parameters
        agent_name = sanitized_request.get("agent")
        query = sanitized_request.get("query")
        
        if not agent_name or not query:
            raise HTTPException(status_code=400, detail="Agent name and query required")
        
        # Execute agent through agentic router
        try:
            # Use resource manager for controlled execution
            async with resource_manager.managed_task(f"agent_execution_{agent_name}_{datetime.now().timestamp()}"):
                result = await agentic_router.execute_agent(
                    agent_name=agent_name,
                    query=query,
                    user_id=current_user.user_id if current_user else "anonymous"
                )
                
                return {
                    "agent": agent_name,
                    "query": query,
                    "result": result,
                    "timestamp": datetime.now().isoformat(),
                    "user_id": current_user.user_id if current_user else "anonymous"
                }
                
        except Exception as e:
            # Log agent execution failure
            await security_framework.security_monitor.log_security_event(
                SecurityEventType.SUSPICIOUS_ACTIVITY,
                ThreatLevel.MEDIUM,
                user_id=current_user.user_id if current_user else None,
                details={
                    "agent": agent_name,
                    "query": query[:100],
                    "error": str(e)
                }
            )
            raise

# Include existing routers with error handling
app.include_router(agentic_router, prefix="/api/v1")

# Error handlers
@app.exception_handler(MainzaException)
async def mainza_exception_handler(request: Request, exc: MainzaException):
    """Handle Mainza-specific exceptions"""
    await error_handler.handle_error(
        error=exc,
        context={"request_url": str(request.url)},
        component="api_endpoint"
    )
    
    return JSONResponse(
        status_code=400 if exc.severity.value in ["low", "medium"] else 500,
        content={
            "error": exc.message,
            "error_id": exc.error_id,
            "category": exc.category.value,
            "severity": exc.severity.value
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    await error_handler.handle_error(
        error=exc,
        context={"request_url": str(request.url)},
        component="api_endpoint"
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred"
        }
    )

# Application-specific health checks
async def register_application_health_checks():
    """Register application-specific health checks"""
    
    async def neo4j_health():
        """Neo4j database health check"""
        try:
            result = neo4j_production.execute_query("RETURN 1 AS health")
            return result is not None and len(result) > 0
        except Exception:
            return False
    
    async def consciousness_health():
        """Consciousness system health check"""
        try:
            state = await consciousness_orchestrator.get_consciousness_state()
            return state is not None
        except Exception:
            return False
    
    def memory_health():
        """Memory usage health check"""
        import psutil
        return psutil.virtual_memory().percent < 90
    
    # Register health checks
    health_monitor.register_component("neo4j_database", neo4j_health)
    health_monitor.register_component("consciousness_system", consciousness_health)
    health_monitor.register_component("system_memory", memory_health)
    
    logger.info("Application health checks registered")

async def register_security_handlers():
    """Register security alert handlers"""
    
    async def log_security_alert(alert_data: Dict[str, Any]):
        """Log security alerts"""
        logger.warning(f"SECURITY ALERT: {alert_data}")
    
    async def notify_admin_security_alert(alert_data: Dict[str, Any]):
        """Notify administrators of critical security events"""
        if alert_data.get("threat_level") == "critical":
            logger.critical(f"CRITICAL SECURITY ALERT: {alert_data}")
            # TODO: Implement actual admin notification (email, Slack, etc.)
    
    security_framework.security_monitor.register_alert_handler(log_security_alert)
    security_framework.security_monitor.register_alert_handler(notify_admin_security_alert)
    
    logger.info("Security alert handlers registered")

async def register_error_handlers():
    """Register error event handlers"""
    
    async def log_error_event(error_context):
        """Log error events"""
        if error_context.severity.value in ["high", "critical"]:
            logger.error(f"HIGH SEVERITY ERROR: {error_context.error_id} - {error_context.stack_trace}")
    
# REMOVED FALLBACK FUNCTION: def fallback_consciousness_handler(error_context):
        """Fallback handler for consciousness system errors"""
# REMOVED FALLBACK: logger.warning(f"Consciousness system fallback activated: {error_context.error_id}")
        # Implement fallback consciousness behavior
    
    error_handler.register_error_listener(log_error_event)
    error_handler.register_fallback_handler("consciousness", fallback_consciousness_handler)
    
    logger.info("Error handlers registered")

async def graceful_shutdown():
    """Graceful shutdown procedure"""
    try:
        # Stop performance optimization
        await performance_optimizer.stop_optimization()
        
        # Shutdown production foundation
        await shutdown_production_foundation()
        
        # Close database connections
        if hasattr(neo4j_production, 'close'):
            await neo4j_production.close()
        
        logger.info("Graceful shutdown completed")
        
    except Exception as e:
        logger.error(f"Error during graceful shutdown: {e}")

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info(f"Received signal {signum}, initiating graceful shutdown...")
    shutdown_event.set()

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    # Production server configuration
    server_config = {
        "host": config_manager.get("server.host", "0.0.0.0"),
        "port": config_manager.get("server.port", 8000),
        "workers": config_manager.get("server.workers", 1),
        "log_level": config_manager.get("server.log_level", "info"),
        "access_log": config_manager.get("server.access_log", True),
        "reload": config_manager.get("server.reload", False)
    }
    
    logger.info(f"Starting Mainza AI Production Server on {server_config['host']}:{server_config['port']}")
    
    uvicorn.run(
        "backend.main_production:app",
        **server_config
    )
