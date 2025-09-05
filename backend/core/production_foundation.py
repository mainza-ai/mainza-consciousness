"""
Production Foundation for Mainza AI System
Context7 MCP Standards Implementation

This module provides the core production-grade foundation including:
- Robust error handling and recovery
- Performance monitoring and metrics
- Health checks and observability
- Configuration management
- Resource management
- Security controls
"""

import asyncio
import logging
import time
import traceback
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import json
import os
from contextlib import asynccontextmanager
import psutil
import threading
from concurrent.futures import ThreadPoolExecutor
import weakref

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

class SystemHealth(Enum):
    """System health status enumeration"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    OFFLINE = "offline"

class ComponentStatus(Enum):
    """Component status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    RECOVERING = "recovering"

@dataclass
class PerformanceMetrics:
    """Performance metrics data structure"""
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    disk_usage: float = 0.0
    network_io: Dict[str, int] = field(default_factory=dict)
    response_times: List[float] = field(default_factory=list)
    error_count: int = 0
    success_count: int = 0
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class ComponentHealth:
    """Component health information"""
    name: str
    status: ComponentStatus
    last_check: datetime
    error_message: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None
    dependencies: List[str] = field(default_factory=list)

class CircuitBreaker:
    """Circuit breaker pattern implementation for fault tolerance"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
        self._lock = threading.Lock()
    
    def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        with self._lock:
            if self.state == "open":
                if self._should_attempt_reset():
                    self.state = "half-open"
                else:
                    raise Exception("Circuit breaker is OPEN")
            
            try:
                result = func(*args, **kwargs)
                self._on_success()
                return result
            except Exception as e:
                self._on_failure()
                raise
    
    def _should_attempt_reset(self) -> bool:
        """Check if circuit breaker should attempt reset"""
        return (
            self.last_failure_time and
            datetime.now() - self.last_failure_time > timedelta(seconds=self.recovery_timeout)
        )
    
    def _on_success(self):
        """Handle successful execution"""
        self.failure_count = 0
        self.state = "closed"
    
    def _on_failure(self):
        """Handle failed execution"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "open"

class RetryManager:
    """Retry mechanism with exponential backoff"""
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 60.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
    
    async def execute_with_retry(
        self, 
        func: Callable, 
        *args, 
        exceptions: tuple = (Exception,),
        **kwargs
    ):
        """Execute function with retry logic"""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)
            except exceptions as e:
                last_exception = e
                
                if attempt == self.max_retries:
                    logger.error(f"Max retries ({self.max_retries}) exceeded for {func.__name__}")
                    break
                
                delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}, retrying in {delay}s: {e}")
                await asyncio.sleep(delay)
        
        raise last_exception

class HealthMonitor:
    """System health monitoring and alerting"""
    
    def __init__(self):
        self.components: Dict[str, ComponentHealth] = {}
        self.system_metrics = PerformanceMetrics()
        self.health_checks: Dict[str, Callable] = {}
        self.alert_handlers: List[Callable] = []
        self._monitoring_active = False
        self._monitor_task = None
    
    def register_component(
        self, 
        name: str, 
        health_check: Callable,
        dependencies: List[str] = None
    ):
        """Register a component for health monitoring"""
        self.components[name] = ComponentHealth(
            name=name,
            status=ComponentStatus.INACTIVE,
            last_check=datetime.now(),
            dependencies=dependencies or []
        )
        self.health_checks[name] = health_check
        logger.info(f"Registered component for monitoring: {name}")
    
    def register_alert_handler(self, handler: Callable):
        """Register alert handler for health issues"""
        self.alert_handlers.append(handler)
    
    async def start_monitoring(self, interval: int = 30):
        """Start continuous health monitoring"""
        if self._monitoring_active:
            logger.warning("Health monitoring already active")
            return
        
        self._monitoring_active = True
        self._monitor_task = asyncio.create_task(self._monitor_loop(interval))
        logger.info(f"Started health monitoring with {interval}s interval")
    
    async def stop_monitoring(self):
        """Stop health monitoring"""
        self._monitoring_active = False
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
        logger.info("Stopped health monitoring")
    
    async def _monitor_loop(self, interval: int):
        """Main monitoring loop"""
        while self._monitoring_active:
            try:
                await self.check_all_components()
                await self.update_system_metrics()
                await self.evaluate_system_health()
                await asyncio.sleep(interval)
            except Exception as e:
                logger.error(f"Health monitoring error: {e}")
                await asyncio.sleep(interval)
    
    async def check_all_components(self):
        """Check health of all registered components"""
        for name, health_check in self.health_checks.items():
            try:
                start_time = time.time()
                
                if asyncio.iscoroutinefunction(health_check):
                    result = await health_check()
                else:
                    result = health_check()
                
                response_time = time.time() - start_time
                
                # Update component health
                component = self.components[name]
                component.status = ComponentStatus.ACTIVE if result else ComponentStatus.ERROR
                component.last_check = datetime.now()
                component.error_message = None if result else "Health check failed"
                component.metrics = {"response_time": response_time}
                
            except Exception as e:
                logger.error(f"Health check failed for {name}: {e}")
                component = self.components[name]
                component.status = ComponentStatus.ERROR
                component.last_check = datetime.now()
                component.error_message = str(e)
    
    async def update_system_metrics(self):
        """Update system performance metrics"""
        try:
            # CPU and Memory usage
            self.system_metrics.cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            self.system_metrics.memory_usage = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            self.system_metrics.disk_usage = (disk.used / disk.total) * 100
            
            # Network I/O
            net_io = psutil.net_io_counters()
            self.system_metrics.network_io = {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv
            }
            
            self.system_metrics.timestamp = datetime.now()
            
        except Exception as e:
            logger.error(f"Failed to update system metrics: {e}")
    
    async def evaluate_system_health(self) -> SystemHealth:
        """Evaluate overall system health"""
        error_components = [c for c in self.components.values() if c.status == ComponentStatus.ERROR]
        total_components = len(self.components)
        
        if not total_components:
            return SystemHealth.HEALTHY
        
        error_ratio = len(error_components) / total_components
        
        # Check system resource usage
        high_resource_usage = (
            self.system_metrics.cpu_usage > 90 or
            self.system_metrics.memory_usage > 90 or
            self.system_metrics.disk_usage > 95
        )
        
        if error_ratio > 0.5 or high_resource_usage:
            health = SystemHealth.CRITICAL
        elif error_ratio > 0.2 or self.system_metrics.cpu_usage > 80:
            health = SystemHealth.DEGRADED
        else:
            health = SystemHealth.HEALTHY
        
        # Trigger alerts if needed
        if health in [SystemHealth.CRITICAL, SystemHealth.DEGRADED]:
            await self._trigger_alerts(health, error_components)
        
        return health
    
    async def _trigger_alerts(self, health: SystemHealth, error_components: List[ComponentHealth]):
        """Trigger health alerts"""
        alert_data = {
            "system_health": health.value,
            "timestamp": datetime.now().isoformat(),
            "error_components": [
                {
                    "name": c.name,
                    "status": c.status.value,
                    "error": c.error_message
                } for c in error_components
            ],
            "system_metrics": {
                "cpu_usage": self.system_metrics.cpu_usage,
                "memory_usage": self.system_metrics.memory_usage,
                "disk_usage": self.system_metrics.disk_usage
            }
        }
        
        for handler in self.alert_handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(alert_data)
                else:
                    handler(alert_data)
            except Exception as e:
                logger.error(f"Alert handler failed: {e}")
    
    def get_health_report(self) -> Dict[str, Any]:
        """Get comprehensive health report"""
        return {
            "system_health": self.evaluate_system_health(),
            "timestamp": datetime.now().isoformat(),
            "components": {
                name: {
                    "status": comp.status.value,
                    "last_check": comp.last_check.isoformat(),
                    "error_message": comp.error_message,
                    "metrics": comp.metrics
                } for name, comp in self.components.items()
            },
            "system_metrics": {
                "cpu_usage": self.system_metrics.cpu_usage,
                "memory_usage": self.system_metrics.memory_usage,
                "disk_usage": self.system_metrics.disk_usage,
                "network_io": self.system_metrics.network_io
            }
        }

class ResourceManager:
    """Resource management and optimization"""
    
    def __init__(self, max_workers: int = None):
        self.max_workers = max_workers or min(32, (os.cpu_count() or 1) + 4)
        self.thread_pool = ThreadPoolExecutor(max_workers=self.max_workers)
        self.active_tasks: Dict[str, asyncio.Task] = {}
        self.resource_limits = {
            "max_memory_mb": 2048,
            "max_cpu_percent": 80,
            "max_concurrent_tasks": 100
        }
        self._cleanup_interval = 300  # 5 minutes
        self._cleanup_task = None
    
    async def start_resource_management(self):
        """Start resource management services"""
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())
        logger.info("Resource management started")
    
    async def stop_resource_management(self):
        """Stop resource management services"""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
        
        self.thread_pool.shutdown(wait=True)
        logger.info("Resource management stopped")
    
    async def _cleanup_loop(self):
        """Periodic cleanup of resources"""
        while True:
            try:
                await self._cleanup_completed_tasks()
                await self._check_resource_limits()
                await asyncio.sleep(self._cleanup_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Resource cleanup error: {e}")
                await asyncio.sleep(self._cleanup_interval)
    
    async def _cleanup_completed_tasks(self):
        """Clean up completed tasks"""
        completed_tasks = [
            task_id for task_id, task in self.active_tasks.items()
            if task.done()
        ]
        
        for task_id in completed_tasks:
            del self.active_tasks[task_id]
        
        if completed_tasks:
            logger.debug(f"Cleaned up {len(completed_tasks)} completed tasks")
    
    async def _check_resource_limits(self):
        """Check and enforce resource limits"""
        # Memory check
        memory_usage = psutil.virtual_memory().percent
        if memory_usage > 90:
            logger.warning(f"High memory usage: {memory_usage}%")
            # Implement memory cleanup strategies
        
        # CPU check
        cpu_usage = psutil.cpu_percent(interval=1)
        if cpu_usage > self.resource_limits["max_cpu_percent"]:
            logger.warning(f"High CPU usage: {cpu_usage}%")
        
        # Task count check
        active_task_count = len(self.active_tasks)
        if active_task_count > self.resource_limits["max_concurrent_tasks"]:
            logger.warning(f"High task count: {active_task_count}")
    
    @asynccontextmanager
    async def managed_task(self, task_id: str):
        """Context manager for managed task execution"""
        if len(self.active_tasks) >= self.resource_limits["max_concurrent_tasks"]:
            raise Exception("Maximum concurrent tasks exceeded")
        
        task = asyncio.current_task()
        self.active_tasks[task_id] = task
        
        try:
            yield
        finally:
            if task_id in self.active_tasks:
                del self.active_tasks[task_id]

class ConfigurationManager:
    """Configuration management with environment-based settings"""
    
    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.load_configuration()
    
    def load_configuration(self):
        """Load configuration from environment and files"""
        # Default configuration
        self.config = {
            "neo4j": {
                "uri": os.getenv("NEO4J_URI", "bolt://localhost:7687"),
                "user": os.getenv("NEO4J_USER", "neo4j"),
                "password": os.getenv("NEO4J_PASSWORD"),
                "max_connection_pool_size": int(os.getenv("NEO4J_MAX_POOL_SIZE", "50")),
                "connection_timeout": int(os.getenv("NEO4J_CONNECTION_TIMEOUT", "30"))
            },
            "livekit": {
                "api_key": os.getenv("LIVEKIT_API_KEY", ""),
                "api_secret": os.getenv("LIVEKIT_API_SECRET", ""),
                "url": os.getenv("LIVEKIT_URL", "ws://localhost:7880")
            },
            "consciousness": {
                "reflection_interval": int(os.getenv("CONSCIOUSNESS_REFLECTION_INTERVAL", "1800")),
                "cycle_interval": int(os.getenv("CONSCIOUSNESS_CYCLE_INTERVAL", "60")),
                "proactive_threshold": float(os.getenv("CONSCIOUSNESS_PROACTIVE_THRESHOLD", "0.7"))
            },
            "monitoring": {
                "health_check_interval": int(os.getenv("HEALTH_CHECK_INTERVAL", "30")),
                "metrics_retention_days": int(os.getenv("METRICS_RETENTION_DAYS", "7")),
                "alert_threshold_cpu": int(os.getenv("ALERT_THRESHOLD_CPU", "80")),
                "alert_threshold_memory": int(os.getenv("ALERT_THRESHOLD_MEMORY", "85"))
            },
            "security": {
                "api_rate_limit": int(os.getenv("API_RATE_LIMIT", "100")),
                "max_request_size": int(os.getenv("MAX_REQUEST_SIZE", "10485760")),  # 10MB
                "cors_origins": os.getenv("CORS_ORIGINS", "*").split(",")
            }
        }
        
        logger.info("Configuration loaded successfully")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot notation key"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def update(self, key: str, value: Any):
        """Update configuration value"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        logger.info(f"Configuration updated: {key} = {value}")

# Global instances
health_monitor = HealthMonitor()
resource_manager = ResourceManager()
config_manager = ConfigurationManager()
retry_manager = RetryManager()

# Circuit breakers for critical components
neo4j_circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60)
livekit_circuit_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=30)

async def initialize_production_foundation():
    """Initialize all production foundation components"""
    try:
        logger.info("🚀 Initializing production foundation...")
        
        # Start resource management
        await resource_manager.start_resource_management()
        
        # Start health monitoring
        await health_monitor.start_monitoring(
            interval=config_manager.get("monitoring.health_check_interval", 30)
        )
        
        # Register core health checks
        await register_core_health_checks()
        
        logger.info("✅ Production foundation initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize production foundation: {e}")
        raise

async def register_core_health_checks():
    """Register health checks for core components"""
    
    async def neo4j_health_check():
        """Neo4j health check"""
        try:
            from backend.utils.neo4j_production import neo4j_production
            result = neo4j_production.execute_query("RETURN 1 AS health")
            return result is not None and len(result) > 0
        except Exception:
            return False
    
    async def consciousness_health_check():
        """Consciousness system health check"""
        try:
            from backend.utils.consciousness_orchestrator import consciousness_orchestrator
            state = await consciousness_orchestrator.get_consciousness_state()
            return state is not None
        except Exception:
            return False
    
    def memory_health_check():
        """Memory usage health check"""
        memory_usage = psutil.virtual_memory().percent
        return memory_usage < 90
    
    def disk_health_check():
        """Disk usage health check"""
        disk_usage = psutil.disk_usage('/').percent
        return disk_usage < 95
    
    # Register health checks
    health_monitor.register_component("neo4j", neo4j_health_check, ["database"])
    health_monitor.register_component("consciousness", consciousness_health_check, ["neo4j"])
    health_monitor.register_component("memory", memory_health_check)
    health_monitor.register_component("disk", disk_health_check)
    
    logger.info("Core health checks registered")

async def shutdown_production_foundation():
    """Graceful shutdown of production foundation"""
    try:
        logger.info("🛑 Shutting down production foundation...")
        
        await health_monitor.stop_monitoring()
        await resource_manager.stop_resource_management()
        
        logger.info("✅ Production foundation shutdown complete")
        
    except Exception as e:
        logger.error(f"❌ Error during production foundation shutdown: {e}")

# Export key components
__all__ = [
    'SystemHealth', 'ComponentStatus', 'PerformanceMetrics', 'ComponentHealth',
    'CircuitBreaker', 'RetryManager', 'HealthMonitor', 'ResourceManager', 'ConfigurationManager',
    'health_monitor', 'resource_manager', 'config_manager', 'retry_manager',
    'neo4j_circuit_breaker', 'livekit_circuit_breaker',
    'initialize_production_foundation', 'shutdown_production_foundation'
]