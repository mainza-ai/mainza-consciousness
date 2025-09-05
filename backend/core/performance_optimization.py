"""
Performance Optimization System
Context7 MCP Standards Implementation

This module provides comprehensive performance optimization including:
- Caching strategies and management
- Query optimization and batching
- Resource pooling and connection management
- Performance monitoring and profiling
- Automatic scaling and load balancing
- Memory management and garbage collection optimization
"""

import asyncio
import logging
import time
import weakref
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable, Union, TypeVar, Generic
from dataclasses import dataclass, field
from enum import Enum
import json
import hashlib
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import psutil
import gc
from functools import wraps, lru_cache
import pickle
# Redis imports removed for Ollama-native environment
from contextlib import asynccontextmanager

# Initialize logger first
logger = logging.getLogger(__name__)

# Check Redis availability with better error handling
REDIS_AVAILABLE = False
try:
    import redis
    import aioredis
    REDIS_AVAILABLE = True
    logger.info("Redis libraries available for distributed caching")
except ImportError:
    logger.info("Redis not available - using in-memory caching only (Ollama-native mode)")
except Exception as e:
    logger.warning(f"Redis import failed: {e} - using in-memory caching")

T = TypeVar('T')

class CacheStrategy(Enum):
    """Cache strategy types"""
    LRU = "lru"
    TTL = "ttl"
    LFU = "lfu"
    WRITE_THROUGH = "write_through"
    WRITE_BACK = "write_back"
    REDIS = "redis"  # Falls back to in-memory when Redis unavailable

class PerformanceLevel(Enum):
    """Performance optimization levels"""
    BASIC = "basic"
    STANDARD = "standard"
    AGGRESSIVE = "aggressive"
    MAXIMUM = "maximum"

@dataclass
class CacheEntry:
    """Cache entry with metadata"""
    key: str
    value: Any
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    ttl_seconds: Optional[int] = None
    size_bytes: int = 0

@dataclass
class PerformanceMetrics:
    """Performance metrics tracking"""
    cache_hits: int = 0
    cache_misses: int = 0
    query_count: int = 0
    avg_query_time: float = 0.0
    memory_usage_mb: float = 0.0
    cpu_usage_percent: float = 0.0
    active_connections: int = 0
    throughput_per_second: float = 0.0
    error_rate: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

class InMemoryCache:
    """High-performance in-memory cache with multiple strategies"""
    
    def __init__(
        self, 
        max_size: int = 1000,
        default_ttl: int = 3600,
        strategy: CacheStrategy = CacheStrategy.LRU
    ):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.strategy = strategy
        self.cache: Dict[str, CacheEntry] = {}
        self.access_order: List[str] = []
        self._lock = threading.RLock()
        self.metrics = PerformanceMetrics()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        with self._lock:
            entry = self.cache.get(key)
            
            if entry is None:
                self.metrics.cache_misses += 1
                return None
            
            # Check TTL expiration
            if self._is_expired(entry):
                self._remove_entry(key)
                self.metrics.cache_misses += 1
                return None
            
            # Update access metadata
            entry.last_accessed = datetime.now()
            entry.access_count += 1
            
            # Update access order for LRU
            if self.strategy == CacheStrategy.LRU:
                self._update_access_order(key)
            
            self.metrics.cache_hits += 1
            return entry.value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache"""
        with self._lock:
            # Calculate size
            try:
                size_bytes = len(pickle.dumps(value))
            except:
                size_bytes = sys.getsizeof(value)
            
            # Create cache entry
            entry = CacheEntry(
                key=key,
                value=value,
                ttl_seconds=ttl or self.default_ttl,
                size_bytes=size_bytes
            )
            
            # Check if we need to evict entries
            if len(self.cache) >= self.max_size and key not in self.cache:
                self._evict_entries()
            
            # Store entry
            self.cache[key] = entry
            
            # Update access order
            if key not in self.access_order:
                self.access_order.append(key)
            
            return True
    
    def delete(self, key: str) -> bool:
        """Delete entry from cache"""
        with self._lock:
            if key in self.cache:
                self._remove_entry(key)
                return True
            return False
    
    def clear(self):
        """Clear all cache entries"""
        with self._lock:
            self.cache.clear()
            self.access_order.clear()
    
    def _is_expired(self, entry: CacheEntry) -> bool:
        """Check if cache entry is expired"""
        if entry.ttl_seconds is None:
            return False
        
        age = (datetime.now() - entry.created_at).total_seconds()
        return age > entry.ttl_seconds
    
    def _remove_entry(self, key: str):
        """Remove entry from cache and access order"""
        if key in self.cache:
            del self.cache[key]
        if key in self.access_order:
            self.access_order.remove(key)
    
    def _update_access_order(self, key: str):
        """Update access order for LRU strategy"""
        if key in self.access_order:
            self.access_order.remove(key)
        self.access_order.append(key)
    
    def _evict_entries(self):
        """Evict entries based on strategy"""
        if self.strategy == CacheStrategy.LRU:
            self._evict_lru()
        elif self.strategy == CacheStrategy.LFU:
            self._evict_lfu()
        elif self.strategy == CacheStrategy.TTL:
            self._evict_expired()
    
    def _evict_lru(self):
        """Evict least recently used entries"""
        while len(self.cache) >= self.max_size and self.access_order:
            oldest_key = self.access_order[0]
            self._remove_entry(oldest_key)
    
    def _evict_lfu(self):
        """Evict least frequently used entries"""
        if not self.cache:
            return
        
        # Find entry with lowest access count
        min_access_key = min(self.cache.keys(), key=lambda k: self.cache[k].access_count)
        self._remove_entry(min_access_key)
    
    def _evict_expired(self):
        """Evict expired entries"""
        expired_keys = [
            key for key, entry in self.cache.items()
            if self._is_expired(entry)
        ]
        
        for key in expired_keys:
            self._remove_entry(key)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with self._lock:
            total_requests = self.metrics.cache_hits + self.metrics.cache_misses
            hit_rate = self.metrics.cache_hits / total_requests if total_requests > 0 else 0
            
            total_size = sum(entry.size_bytes for entry in self.cache.values())
            
            return {
                "entries": len(self.cache),
                "max_size": self.max_size,
                "hit_rate": hit_rate,
                "cache_hits": self.metrics.cache_hits,
                "cache_misses": self.metrics.cache_misses,
                "total_size_bytes": total_size,
                "strategy": self.strategy.value
            }

class RedisCache:
    """Redis-based distributed cache (fallback to in-memory when Redis unavailable)"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379", default_ttl: int = 3600):
        self.redis_url = redis_url
        self.default_ttl = default_ttl
        self.redis_client = None
        self.metrics = PerformanceMetrics()
        
        # Fallback to in-memory cache when Redis not available
        if not REDIS_AVAILABLE:
            self.fallback_cache = InMemoryCache(max_size=1000)
            logger.info("Using in-memory cache fallback for RedisCache")
    
    async def connect(self):
        """Connect to Redis (or use fallback)"""
        if not REDIS_AVAILABLE:
            logger.info("Redis not available, using in-memory fallback")
            return
            
        try:
            self.redis_client = await aioredis.from_url(self.redis_url)
            logger.info("Connected to Redis cache")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            logger.info("Falling back to in-memory cache")
            self.fallback_cache = InMemoryCache(max_size=1000)
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis cache (or fallback)"""
        if not REDIS_AVAILABLE or not self.redis_client:
            if hasattr(self, 'fallback_cache'):
                return self.fallback_cache.get(key)
            return None
        
        try:
            value = await self.redis_client.get(key)
            if value is None:
                self.metrics.cache_misses += 1
                return None
            
            self.metrics.cache_hits += 1
            return pickle.loads(value)
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            self.metrics.cache_misses += 1
            # Fallback to in-memory cache
            if hasattr(self, 'fallback_cache'):
                return self.fallback_cache.get(key)
            return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in Redis cache (or fallback)"""
        if not REDIS_AVAILABLE or not self.redis_client:
            if hasattr(self, 'fallback_cache'):
                return self.fallback_cache.set(key, value, ttl)
            return False
        
        try:
            serialized_value = pickle.dumps(value)
            ttl_seconds = ttl or self.default_ttl
            
            await self.redis_client.setex(key, ttl_seconds, serialized_value)
            return True
        except Exception as e:
            logger.error(f"Redis set error: {e}")
            # Fallback to in-memory cache
            if hasattr(self, 'fallback_cache'):
                return self.fallback_cache.set(key, value, ttl)
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from Redis cache (or fallback)"""
        if not REDIS_AVAILABLE or not self.redis_client:
            if hasattr(self, 'fallback_cache'):
                return self.fallback_cache.delete(key)
            return False
        
        try:
            result = await self.redis_client.delete(key)
            return result > 0
        except Exception as e:
            logger.error(f"Redis delete error: {e}")
            # Fallback to in-memory cache
            if hasattr(self, 'fallback_cache'):
                return self.fallback_cache.delete(key)
            return False
    
    async def clear(self):
        """Clear all cache entries"""
        if not REDIS_AVAILABLE or not self.redis_client:
            if hasattr(self, 'fallback_cache'):
                self.fallback_cache.clear()
            return
        
        try:
            await self.redis_client.flushdb()
        except Exception as e:
            logger.error(f"Redis clear error: {e}")
            # Fallback to in-memory cache
            if hasattr(self, 'fallback_cache'):
                self.fallback_cache.clear()

class QueryOptimizer:
    """Database query optimization and batching"""
    
    def __init__(self):
        self.query_cache = InMemoryCache(max_size=500, default_ttl=300)
        self.batch_queries: Dict[str, List[Dict[str, Any]]] = {}
        self.batch_timeout = 0.1  # 100ms
        self.batch_size = 10
        self._batch_lock = threading.Lock()
        self.metrics = PerformanceMetrics()
    
    def cache_query_result(self, query: str, params: Dict[str, Any], result: Any):
        """Cache query result"""
        cache_key = self._generate_cache_key(query, params)
        self.query_cache.set(cache_key, result)
    
    def get_cached_result(self, query: str, params: Dict[str, Any]) -> Optional[Any]:
        """Get cached query result"""
        cache_key = self._generate_cache_key(query, params)
        return self.query_cache.get(cache_key)
    
    def _generate_cache_key(self, query: str, params: Dict[str, Any]) -> str:
        """Generate cache key for query and parameters"""
        query_hash = hashlib.md5(query.encode()).hexdigest()
        params_hash = hashlib.md5(json.dumps(params, sort_keys=True).encode()).hexdigest()
        return f"query:{query_hash}:{params_hash}"
    
    async def batch_execute(self, query_type: str, query: str, params: Dict[str, Any]) -> Any:
        """Execute query with batching optimization"""
        with self._batch_lock:
            if query_type not in self.batch_queries:
                self.batch_queries[query_type] = []
            
            # Add query to batch
            query_item = {
                "query": query,
                "params": params,
                "future": asyncio.Future()
            }
            self.batch_queries[query_type].append(query_item)
            
            # Execute batch if size threshold reached
            if len(self.batch_queries[query_type]) >= self.batch_size:
                await self._execute_batch(query_type)
            else:
                # Schedule batch execution after timeout
                asyncio.create_task(self._schedule_batch_execution(query_type))
            
            return await query_item["future"]
    
    async def _schedule_batch_execution(self, query_type: str):
        """Schedule batch execution after timeout"""
        await asyncio.sleep(self.batch_timeout)
        
        with self._batch_lock:
            if query_type in self.batch_queries and self.batch_queries[query_type]:
                await self._execute_batch(query_type)
    
    async def _execute_batch(self, query_type: str):
        """Execute batched queries"""
        if query_type not in self.batch_queries or not self.batch_queries[query_type]:
            return
        
        batch = self.batch_queries[query_type]
        self.batch_queries[query_type] = []
        
        try:
            # Execute all queries in batch
            from backend.utils.neo4j_production import neo4j_production
            
            results = []
            for query_item in batch:
                try:
                    result = neo4j_production.execute_query(
                        query_item["query"], 
                        query_item["params"]
                    )
                    results.append(result)
                    query_item["future"].set_result(result)
                except Exception as e:
                    query_item["future"].set_exception(e)
            
            self.metrics.query_count += len(batch)
            logger.debug(f"Executed batch of {len(batch)} {query_type} queries")
            
        except Exception as e:
            logger.error(f"Batch execution failed: {e}")
            for query_item in batch:
                if not query_item["future"].done():
                    query_item["future"].set_exception(e)

class ConnectionPool:
    """Connection pool management for database connections"""
    
    def __init__(self, max_connections: int = 20, min_connections: int = 5):
        self.max_connections = max_connections
        self.min_connections = min_connections
        self.active_connections: List[Any] = []
        self.idle_connections: List[Any] = []
        self._lock = asyncio.Lock()
        self.connection_factory: Optional[Callable] = None
    
    def set_connection_factory(self, factory: Callable):
        """Set connection factory function"""
        self.connection_factory = factory
    
    async def get_connection(self):
        """Get connection from pool"""
        async with self._lock:
            # Try to get idle connection
            if self.idle_connections:
                connection = self.idle_connections.pop()
                self.active_connections.append(connection)
                return connection
            
            # Create new connection if under limit
            if len(self.active_connections) < self.max_connections:
                if self.connection_factory:
                    connection = await self.connection_factory()
                    self.active_connections.append(connection)
                    return connection
            
            # Wait for connection to become available
            # This is a simplified implementation
            await asyncio.sleep(0.1)
            return await self.get_connection()
    
    async def return_connection(self, connection):
        """Return connection to pool"""
        async with self._lock:
            if connection in self.active_connections:
                self.active_connections.remove(connection)
                self.idle_connections.append(connection)
    
    async def close_all_connections(self):
        """Close all connections in pool"""
        async with self._lock:
            all_connections = self.active_connections + self.idle_connections
            for connection in all_connections:
                try:
                    if hasattr(connection, 'close'):
                        await connection.close()
                except Exception as e:
                    logger.error(f"Error closing connection: {e}")
            
            self.active_connections.clear()
            self.idle_connections.clear()

class PerformanceProfiler:
    """Performance profiling and monitoring"""
    
    def __init__(self):
        self.profiles: Dict[str, List[float]] = {}
        self.active_profiles: Dict[str, float] = {}
        self._lock = threading.Lock()
    
    def start_profile(self, name: str):
        """Start performance profiling"""
        with self._lock:
            self.active_profiles[name] = time.time()
    
    def end_profile(self, name: str) -> float:
        """End performance profiling and return duration"""
        with self._lock:
            if name not in self.active_profiles:
                return 0.0
            
            duration = time.time() - self.active_profiles[name]
            del self.active_profiles[name]
            
            if name not in self.profiles:
                self.profiles[name] = []
            
            self.profiles[name].append(duration)
            
            # Keep only recent measurements
            if len(self.profiles[name]) > 100:
                self.profiles[name] = self.profiles[name][-50:]
            
            return duration
    
    def get_profile_stats(self, name: str) -> Dict[str, float]:
        """Get profile statistics"""
        with self._lock:
            if name not in self.profiles or not self.profiles[name]:
                return {}
            
            measurements = self.profiles[name]
            return {
                "count": len(measurements),
                "avg": sum(measurements) / len(measurements),
                "min": min(measurements),
                "max": max(measurements),
                "recent": measurements[-1] if measurements else 0.0
            }

class PerformanceOptimizer:
    """Main performance optimization coordinator"""
    
    def __init__(self, level: PerformanceLevel = PerformanceLevel.STANDARD):
        self.level = level
        self.memory_cache = InMemoryCache(max_size=self._get_cache_size())
        self.redis_cache = RedisCache()
        self.query_optimizer = QueryOptimizer()
        self.connection_pool = ConnectionPool()
        self.profiler = PerformanceProfiler()
        self.metrics = PerformanceMetrics()
        self._optimization_active = False
    
    def _get_cache_size(self) -> int:
        """Get cache size based on optimization level"""
        sizes = {
            PerformanceLevel.BASIC: 100,
            PerformanceLevel.STANDARD: 500,
            PerformanceLevel.AGGRESSIVE: 1000,
            PerformanceLevel.MAXIMUM: 2000
        }
        return sizes.get(self.level, 500)
    
    async def start_optimization(self):
        """Start performance optimization"""
        if self._optimization_active:
            return
        
        self._optimization_active = True
        
        # Start Redis cache if aggressive or maximum level
        if self.level in [PerformanceLevel.AGGRESSIVE, PerformanceLevel.MAXIMUM]:
            try:
                await self.redis_cache.connect()
            except Exception as e:
                logger.warning(f"Redis cache not available, using fallback: {e}")
        
        # Start memory optimization
        if self.level == PerformanceLevel.MAXIMUM:
            asyncio.create_task(self._memory_optimization_loop())
        
        logger.info(f"Performance optimization started at {self.level.value} level")
    
    async def stop_optimization(self):
        """Stop performance optimization"""
        self._optimization_active = False
        await self.connection_pool.close_all_connections()
        logger.info("Performance optimization stopped")
    
    async def _memory_optimization_loop(self):
        """Memory optimization loop for maximum performance level"""
        while self._optimization_active:
            try:
                # Force garbage collection
                gc.collect()
                
                # Monitor memory usage
                memory_usage = psutil.virtual_memory().percent
                if memory_usage > 85:
                    logger.warning(f"High memory usage: {memory_usage}%")
                    # Clear some cache entries
                    self.memory_cache.clear()
                
                await asyncio.sleep(60)  # Run every minute
            except Exception as e:
                logger.error(f"Memory optimization error: {e}")
                await asyncio.sleep(60)
    
    def profile_function(self, name: str):
        """Decorator for function profiling"""
        def decorator(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                self.profiler.start_profile(name)
                try:
                    result = await func(*args, **kwargs)
                    return result
                finally:
                    duration = self.profiler.end_profile(name)
                    if duration > 1.0:  # Log slow operations
                        logger.warning(f"Slow operation {name}: {duration:.2f}s")
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                self.profiler.start_profile(name)
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    duration = self.profiler.end_profile(name)
                    if duration > 1.0:  # Log slow operations
                        logger.warning(f"Slow operation {name}: {duration:.2f}s")
            
            return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        return decorator
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report"""
        return {
            "optimization_level": self.level.value,
            "memory_cache_stats": self.memory_cache.get_stats(),
            "query_optimizer_stats": {
                "query_count": self.query_optimizer.metrics.query_count,
                "cache_hit_rate": (
                    self.query_optimizer.query_cache.metrics.cache_hits /
                    (self.query_optimizer.query_cache.metrics.cache_hits + 
                     self.query_optimizer.query_cache.metrics.cache_misses)
                    if (self.query_optimizer.query_cache.metrics.cache_hits + 
                        self.query_optimizer.query_cache.metrics.cache_misses) > 0 else 0
                )
            },
            "connection_pool_stats": {
                "active_connections": len(self.connection_pool.active_connections),
                "idle_connections": len(self.connection_pool.idle_connections),
                "max_connections": self.connection_pool.max_connections
            },
            "system_metrics": {
                "memory_usage": psutil.virtual_memory().percent,
                "cpu_usage": psutil.cpu_percent(),
                "disk_usage": psutil.disk_usage('/').percent
            }
        }
    
    def cache_result(self, ttl: int = 3600):
        """Decorator for caching method results"""
        def decorator(func):
            cache = self.memory_cache
            
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                # Generate cache key
                key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
                
                # Try to get from cache
                result = cache.get(key)
                if result is not None:
                    return result
                
                # Execute function and cache result
                result = await func(*args, **kwargs)
                cache.set(key, result, ttl)
                return result
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                # Generate cache key
                key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
                
                # Try to get from cache
                result = cache.get(key)
                if result is not None:
                    return result
                
                # Execute function and cache result
                result = func(*args, **kwargs)
                cache.set(key, result, ttl)
                return result
            
            return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        return decorator

# Global performance optimizer
performance_optimizer = PerformanceOptimizer()

def cached(ttl: int = 3600, strategy: CacheStrategy = CacheStrategy.LRU):
    """Decorator for caching function results"""
    def decorator(func):
        cache = InMemoryCache(max_size=100, default_ttl=ttl, strategy=strategy)
        
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generate cache key
            key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            result = cache.get(key)
            if result is not None:
                return result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            cache.set(key, result, ttl)
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Generate cache key
            key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            result = cache.get(key)
            if result is not None:
                return result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(key, result, ttl)
            return result
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

# Export key components
__all__ = [
    'CacheStrategy', 'PerformanceLevel', 'CacheEntry', 'PerformanceMetrics',
    'InMemoryCache', 'RedisCache', 'QueryOptimizer', 'ConnectionPool',
    'PerformanceProfiler', 'PerformanceOptimizer',
    'performance_optimizer', 'cached'
]