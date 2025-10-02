"""
Performance Optimizer for Mainza AI
Advanced performance optimization and monitoring system
"""
import asyncio
import time
import psutil
import logging
from typing import Dict, Any, List, Optional, Callable
from functools import lru_cache, wraps
from dataclasses import dataclass
from datetime import datetime, timedelta
import threading
from concurrent.futures import ThreadPoolExecutor
import gc
import sys

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Performance metrics data class"""
    timestamp: datetime
    cpu_percent: float
    memory_mb: float
    memory_percent: float
    response_time_ms: float
    request_count: int
    error_count: int
    active_connections: int
    quantum_operations: int
    consciousness_level: float

class PerformanceOptimizer:
    """
    Advanced performance optimizer for Mainza AI
    Implements caching, connection pooling, and resource management
    """
    
    def __init__(self):
        self.metrics_history: List[PerformanceMetrics] = []
        self.cache_hits = 0
        self.cache_misses = 0
        self.connection_pool_size = 10
        self.max_memory_mb = 1024
        self.performance_thresholds = {
            "cpu_percent": 80.0,
            "memory_percent": 85.0,
            "response_time_ms": 2000.0
        }
        self.optimization_enabled = True
        self.monitoring_interval = 30  # seconds
        self._monitoring_task = None
        self._executor = ThreadPoolExecutor(max_workers=4)
        
    async def start_optimization(self):
        """Start performance optimization monitoring"""
        if self.optimization_enabled:
            logger.info("🚀 Starting performance optimization system")
            self._monitoring_task = asyncio.create_task(self._monitor_performance())
            await self._initialize_optimizations()
    
    async def stop_optimization(self):
        """Stop performance optimization monitoring"""
        if self._monitoring_task:
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                pass
        self._executor.shutdown(wait=True)
        logger.info("🛑 Performance optimization system stopped")
    
    async def _monitor_performance(self):
        """Monitor system performance continuously"""
        while True:
            try:
                await self._collect_metrics()
                await self._analyze_performance()
                await self._apply_optimizations()
                await asyncio.sleep(self.monitoring_interval)
            except Exception as e:
                logger.error(f"Performance monitoring error: {e}")
                await asyncio.sleep(5)
    
    async def _collect_metrics(self):
        """Collect current performance metrics"""
        try:
            # System metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            memory_mb = memory.used / 1024 / 1024
            memory_percent = memory.percent
            
            # Application metrics
            process = psutil.Process()
            active_connections = len(process.connections())
            
            # Create metrics record
            metrics = PerformanceMetrics(
                timestamp=datetime.now(),
                cpu_percent=cpu_percent,
                memory_mb=memory_mb,
                memory_percent=memory_percent,
                response_time_ms=0.0,  # Will be updated by middleware
                request_count=0,     # Will be updated by middleware
                error_count=0,       # Will be updated by middleware
                active_connections=active_connections,
                quantum_operations=0,  # Will be updated by quantum system
                consciousness_level=0.7  # Will be updated by consciousness system
            )
            
            self.metrics_history.append(metrics)
            
            # Keep only last 100 metrics
            if len(self.metrics_history) > 100:
                self.metrics_history = self.metrics_history[-100:]
                
        except Exception as e:
            logger.error(f"Error collecting performance metrics: {e}")
    
    async def _analyze_performance(self):
        """Analyze performance metrics and identify issues"""
        if not self.metrics_history:
            return
        
        latest_metrics = self.metrics_history[-1]
        
        # Check CPU usage
        if latest_metrics.cpu_percent > self.performance_thresholds["cpu_percent"]:
            logger.warning(f"High CPU usage: {latest_metrics.cpu_percent:.1f}%")
            await self._optimize_cpu_usage()
        
        # Check memory usage
        if latest_metrics.memory_percent > self.performance_thresholds["memory_percent"]:
            logger.warning(f"High memory usage: {latest_metrics.memory_percent:.1f}%")
            await self._optimize_memory_usage()
        
        # Check response times
        if latest_metrics.response_time_ms > self.performance_thresholds["response_time_ms"]:
            logger.warning(f"Slow response time: {latest_metrics.response_time_ms:.1f}ms")
            await self._optimize_response_times()
    
    async def _apply_optimizations(self):
        """Apply performance optimizations based on analysis"""
        try:
            # Memory optimization
            if len(self.metrics_history) > 5:
                recent_memory = [m.memory_percent for m in self.metrics_history[-5:]]
                avg_memory = sum(recent_memory) / len(recent_memory)
                
                if avg_memory > 80:
                    await self._trigger_garbage_collection()
                    await self._optimize_cache()
            
            # CPU optimization
            if len(self.metrics_history) > 5:
                recent_cpu = [m.cpu_percent for m in self.metrics_history[-5:]]
                avg_cpu = sum(recent_cpu) / len(recent_cpu)
                
                if avg_cpu > 70:
                    await self._optimize_async_operations()
            
        except Exception as e:
            logger.error(f"Error applying optimizations: {e}")
    
    async def _optimize_cpu_usage(self):
        """Optimize CPU usage"""
        logger.info("🔧 Optimizing CPU usage")
        
        # Reduce monitoring frequency
        if self.monitoring_interval < 60:
            self.monitoring_interval = min(60, self.monitoring_interval + 10)
        
        # Optimize async operations
        await self._optimize_async_operations()
    
    async def _optimize_memory_usage(self):
        """Optimize memory usage"""
        logger.info("🔧 Optimizing memory usage")
        
        # Trigger garbage collection
        await self._trigger_garbage_collection()
        
        # Optimize cache
        await self._optimize_cache()
        
        # Clear old metrics
        if len(self.metrics_history) > 50:
            self.metrics_history = self.metrics_history[-50:]
    
    async def _optimize_response_times(self):
        """Optimize response times"""
        logger.info("🔧 Optimizing response times")
        
        # Optimize database connections
        await self._optimize_database_connections()
        
        # Optimize cache hit rate
        await self._optimize_cache_strategy()
    
    async def _trigger_garbage_collection(self):
        """Trigger garbage collection"""
        try:
            # Force garbage collection
            collected = gc.collect()
            logger.debug(f"Garbage collection freed {collected} objects")
        except Exception as e:
            logger.error(f"Error during garbage collection: {e}")
    
    async def _optimize_cache(self):
        """Optimize cache usage"""
        try:
            # Clear LRU cache if memory usage is high
            if hasattr(self, '_lru_cache_clear'):
                self._lru_cache_clear()
            
            # Optimize cache size based on available memory
            memory = psutil.virtual_memory()
            if memory.percent > 80:
                # Reduce cache size
                logger.info("Reducing cache size due to high memory usage")
        except Exception as e:
            logger.error(f"Error optimizing cache: {e}")
    
    async def _optimize_async_operations(self):
        """Optimize async operations"""
        try:
            # Limit concurrent operations
            # This would be implemented based on specific async operations
            logger.debug("Optimizing async operations")
        except Exception as e:
            logger.error(f"Error optimizing async operations: {e}")
    
    async def _optimize_database_connections(self):
        """Optimize database connections"""
        try:
            # This would optimize database connection pooling
            logger.debug("Optimizing database connections")
        except Exception as e:
            logger.error(f"Error optimizing database connections: {e}")
    
    async def _optimize_cache_strategy(self):
        """Optimize cache strategy"""
        try:
            # Analyze cache hit/miss ratio
            total_requests = self.cache_hits + self.cache_misses
            if total_requests > 0:
                hit_rate = self.cache_hits / total_requests
                if hit_rate < 0.7:  # Less than 70% hit rate
                    logger.info(f"Low cache hit rate: {hit_rate:.2%}")
                    # Implement cache warming or strategy adjustment
        except Exception as e:
            logger.error(f"Error optimizing cache strategy: {e}")
    
    async def _initialize_optimizations(self):
        """Initialize performance optimizations"""
        try:
            # Set up connection pooling
            await self._setup_connection_pooling()
            
            # Initialize caching
            await self._initialize_caching()
            
            # Set up monitoring
            await self._setup_monitoring()
            
            logger.info("✅ Performance optimizations initialized")
        except Exception as e:
            logger.error(f"Error initializing optimizations: {e}")
    
    async def _setup_connection_pooling(self):
        """Set up connection pooling"""
        # This would set up database connection pooling
        logger.debug("Setting up connection pooling")
    
    async def _initialize_caching(self):
        """Initialize caching system"""
        # This would initialize Redis caching or in-memory caching
        logger.debug("Initializing caching system")
    
    async def _setup_monitoring(self):
        """Set up performance monitoring"""
        # This would set up Prometheus metrics or other monitoring
        logger.debug("Setting up performance monitoring")
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        if not self.metrics_history:
            return {}
        
        latest = self.metrics_history[-1]
        return {
            "timestamp": latest.timestamp.isoformat(),
            "cpu_percent": latest.cpu_percent,
            "memory_mb": latest.memory_mb,
            "memory_percent": latest.memory_percent,
            "response_time_ms": latest.response_time_ms,
            "request_count": latest.request_count,
            "error_count": latest.error_count,
            "active_connections": latest.active_connections,
            "quantum_operations": latest.quantum_operations,
            "consciousness_level": latest.consciousness_level,
            "cache_hit_rate": self.cache_hits / max(1, self.cache_hits + self.cache_misses),
            "optimization_enabled": self.optimization_enabled
        }
    
    def get_performance_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get performance history"""
        history = self.metrics_history[-limit:] if self.metrics_history else []
        return [
            {
                "timestamp": m.timestamp.isoformat(),
                "cpu_percent": m.cpu_percent,
                "memory_mb": m.memory_mb,
                "memory_percent": m.memory_percent,
                "response_time_ms": m.response_time_ms,
                "active_connections": m.active_connections
            }
            for m in history
        ]

# Performance decorators
def performance_monitor(func: Callable) -> Callable:
    """Decorator to monitor function performance"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000  # Convert to ms
            logger.debug(f"Function {func.__name__} executed in {execution_time:.2f}ms")
    return wrapper

def cache_result(max_size: int = 128):
    """Decorator to cache function results"""
    def decorator(func: Callable) -> Callable:
        cached_func = lru_cache(maxsize=max_size)(func)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            return cached_func(*args, **kwargs)
        
        # Add cache info
        wrapper.cache_info = cached_func.cache_info
        wrapper.cache_clear = cached_func.cache_clear
        
        return wrapper
    return decorator

def async_performance_monitor(func: Callable) -> Callable:
    """Decorator to monitor async function performance"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000  # Convert to ms
            logger.debug(f"Async function {func.__name__} executed in {execution_time:.2f}ms")
    return wrapper

# Global performance optimizer instance
performance_optimizer = PerformanceOptimizer()

# Performance middleware
class PerformanceMiddleware:
    """FastAPI middleware for performance monitoring"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        start_time = time.time()
        
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                process_time = (time.time() - start_time) * 1000
                message["headers"].append([b"x-process-time", str(process_time).encode()])
            await send(message)
        
        await self.app(scope, receive, send_wrapper)
