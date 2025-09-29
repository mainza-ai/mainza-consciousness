"""
Enhanced Redis Caching System for Mainza AI
Implements advanced caching strategies with compression and optimization
"""

import asyncio
import json
import logging
import pickle
import gzip
import hashlib
from typing import Any, Dict, List, Optional, Union, Callable
from datetime import datetime, timedelta
from functools import wraps
import redis.asyncio as redis
from redis.asyncio import ConnectionPool
import numpy as np

logger = logging.getLogger(__name__)

class EnhancedRedisCache:
    """
    Advanced Redis caching system with compression, serialization, and optimization
    """
    
    def __init__(self, redis_url: str, config: Dict[str, Any]):
        self.redis_url = redis_url
        self.config = config
        self.pool = None
        self.redis_client = None
        self.compression_enabled = config.get("compression_enabled", True)
        self.serialization_method = config.get("serialization_method", "json")
        self.default_ttl = config.get("default_ttl", 3600)  # 1 hour
        self.max_memory_usage = config.get("max_memory_usage", "512mb")
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "deletes": 0,
            "compressions": 0,
            "total_size": 0
        }
        
    async def initialize(self):
        """Initialize Redis connection with optimized settings"""
        try:
            # Create connection pool with optimization
            self.pool = ConnectionPool.from_url(
                self.redis_url,
                max_connections=20,
                retry_on_timeout=True,
                socket_keepalive=True,
                socket_keepalive_options={},
                health_check_interval=30
            )
            
            self.redis_client = redis.Redis(connection_pool=self.pool)
            
            # Configure Redis for optimal performance
            await self._configure_redis_optimization()
            
            # Test connection
            await self.redis_client.ping()
            logger.info("Enhanced Redis cache initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing Redis cache: {e}")
            raise
    
    async def _configure_redis_optimization(self):
        """Configure Redis for optimal performance"""
        try:
            # Set memory policy
            await self.redis_client.config_set("maxmemory-policy", "allkeys-lru")
            await self.redis_client.config_set("maxmemory", self.max_memory_usage)
            
            # Enable compression for large values
            await self.redis_client.config_set("hash-max-ziplist-entries", "512")
            await self.redis_client.config_set("hash-max-ziplist-value", "64")
            
            # Optimize for memory usage
            await self.redis_client.config_set("list-max-ziplist-size", "-2")
            await self.redis_client.config_set("set-max-intset-entries", "512")
            
            logger.info("Redis optimization configuration applied")
            
        except Exception as e:
            logger.warning(f"Could not apply Redis optimization: {e}")
    
    async def get(self, key: str, default: Any = None) -> Any:
        """
        Get value from cache with decompression and deserialization
        """
        try:
            start_time = datetime.now()
            
            # Get raw value from Redis
            raw_value = await self.redis_client.get(key)
            
            if raw_value is None:
                self.cache_stats["misses"] += 1
                return default
            
            # Deserialize and decompress
            value = await self._deserialize_value(raw_value)
            
            # Update statistics
            self.cache_stats["hits"] += 1
            self.cache_stats["total_size"] += len(raw_value)
            
            # Update hit rate
            hit_rate = self._calculate_hit_rate()
            if hit_rate > 0.8:  # High hit rate, consider extending TTL
                await self._extend_ttl_if_beneficial(key)
            
            return value
            
        except Exception as e:
            logger.error(f"Error getting cache value for key '{key}': {e}")
            self.cache_stats["misses"] += 1
            return default
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None, 
                 compress: bool = None) -> bool:
        """
        Set value in cache with compression and serialization
        """
        try:
            start_time = datetime.now()
            
            # Determine compression
            if compress is None:
                compress = self._should_compress(value)
            
            # Serialize and compress
            serialized_value = await self._serialize_value(value, compress)
            
            # Set TTL
            if ttl is None:
                ttl = self.default_ttl
            
            # Store in Redis
            await self.redis_client.setex(key, ttl, serialized_value)
            
            # Update statistics
            self.cache_stats["sets"] += 1
            self.cache_stats["total_size"] += len(serialized_value)
            if compress:
                self.cache_stats["compressions"] += 1
            
            # Update cache metadata
            await self._update_cache_metadata(key, {
                "size": len(serialized_value),
                "compressed": compress,
                "created_at": datetime.now().isoformat(),
                "ttl": ttl
            })
            
            return True
            
        except Exception as e:
            logger.error(f"Error setting cache value for key '{key}': {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            result = await self.redis_client.delete(key)
            self.cache_stats["deletes"] += 1
            return bool(result)
            
        except Exception as e:
            logger.error(f"Error deleting cache key '{key}': {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        try:
            return bool(await self.redis_client.exists(key))
        except Exception as e:
            logger.error(f"Error checking cache key existence '{key}': {e}")
            return False
    
    async def get_or_set(self, key: str, factory: Callable, ttl: Optional[int] = None) -> Any:
        """
        Get value from cache or set it using factory function
        """
        try:
            # Try to get from cache
            value = await self.get(key)
            if value is not None:
                return value
            
            # Generate value using factory
            if asyncio.iscoroutinefunction(factory):
                value = await factory()
            else:
                value = factory()
            
            # Set in cache
            await self.set(key, value, ttl)
            return value
            
        except Exception as e:
            logger.error(f"Error in get_or_set for key '{key}': {e}")
            # Fallback to factory result
            if asyncio.iscoroutinefunction(factory):
                return await factory()
            else:
                return factory()
    
    async def batch_get(self, keys: List[str]) -> Dict[str, Any]:
        """Get multiple values in batch"""
        try:
            if not keys:
                return {}
            
            # Use pipeline for batch operations
            pipe = self.redis_client.pipeline()
            for key in keys:
                pipe.get(key)
            
            results = await pipe.execute()
            
            # Deserialize results
            batch_results = {}
            for i, key in enumerate(keys):
                if results[i] is not None:
                    try:
                        batch_results[key] = await self._deserialize_value(results[i])
                        self.cache_stats["hits"] += 1
                    except Exception as e:
                        logger.warning(f"Error deserializing value for key '{key}': {e}")
                        self.cache_stats["misses"] += 1
                else:
                    self.cache_stats["misses"] += 1
            
            return batch_results
            
        except Exception as e:
            logger.error(f"Error in batch_get: {e}")
            return {}
    
    async def batch_set(self, data: Dict[str, Any], ttl: Optional[int] = None) -> bool:
        """Set multiple values in batch"""
        try:
            if not data:
                return True
            
            # Use pipeline for batch operations
            pipe = self.redis_client.pipeline()
            
            for key, value in data.items():
                # Serialize value
                serialized_value = await self._serialize_value(value)
                pipe.setex(key, ttl or self.default_ttl, serialized_value)
            
            await pipe.execute()
            
            # Update statistics
            self.cache_stats["sets"] += len(data)
            
            return True
            
        except Exception as e:
            logger.error(f"Error in batch_set: {e}")
            return False
    
    async def _serialize_value(self, value: Any, compress: bool = None) -> bytes:
        """Serialize value with optional compression"""
        try:
            # Choose serialization method
            if self.serialization_method == "pickle":
                serialized = pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL)
            else:  # JSON
                serialized = json.dumps(value, default=str).encode('utf-8')
            
            # Apply compression if beneficial
            if compress or (compress is None and self._should_compress(value)):
                compressed = gzip.compress(serialized)
                if len(compressed) < len(serialized):
                    serialized = compressed
                    # Add compression marker
                    serialized = b"COMPRESSED:" + serialized
            
            return serialized
            
        except Exception as e:
            logger.error(f"Error serializing value: {e}")
            raise
    
    async def _deserialize_value(self, raw_value: bytes) -> Any:
        """Deserialize value with decompression"""
        try:
            # Check for compression marker
            if raw_value.startswith(b"COMPRESSED:"):
                raw_value = gzip.decompress(raw_value[11:])  # Remove "COMPRESSED:" prefix
            
            # Choose deserialization method
            if self.serialization_method == "pickle":
                return pickle.loads(raw_value)
            else:  # JSON
                return json.loads(raw_value.decode('utf-8'))
                
        except Exception as e:
            logger.error(f"Error deserializing value: {e}")
            raise
    
    def _should_compress(self, value: Any) -> bool:
        """Determine if value should be compressed"""
        try:
            # Estimate size
            if isinstance(value, (str, bytes)):
                size = len(value)
            elif isinstance(value, (list, dict)):
                size = len(str(value))
            else:
                size = len(str(value))
            
            # Compress if larger than threshold
            return size > 1024  # 1KB threshold
            
        except Exception:
            return False
    
    def _calculate_hit_rate(self) -> float:
        """Calculate cache hit rate"""
        total = self.cache_stats["hits"] + self.cache_stats["misses"]
        return self.cache_stats["hits"] / total if total > 0 else 0.0
    
    async def _extend_ttl_if_beneficial(self, key: str):
        """Extend TTL for frequently accessed keys"""
        try:
            current_ttl = await self.redis_client.ttl(key)
            if current_ttl > 0:
                # Extend TTL by 50% if it's less than 1 hour
                new_ttl = min(current_ttl * 1.5, 3600)
                await self.redis_client.expire(key, int(new_ttl))
                
        except Exception as e:
            logger.warning(f"Error extending TTL for key '{key}': {e}")
    
    async def _update_cache_metadata(self, key: str, metadata: Dict[str, Any]):
        """Update cache metadata for monitoring"""
        try:
            metadata_key = f"metadata:{key}"
            await self.redis_client.hset(metadata_key, mapping=metadata)
            await self.redis_client.expire(metadata_key, 86400)  # 24 hours
            
        except Exception as e:
            logger.warning(f"Error updating cache metadata: {e}")
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics"""
        try:
            # Get Redis info
            redis_info = await self.redis_client.info()
            
            return {
                "cache_stats": self.cache_stats,
                "hit_rate": self._calculate_hit_rate(),
                "redis_info": {
                    "used_memory": redis_info.get("used_memory_human"),
                    "connected_clients": redis_info.get("connected_clients"),
                    "keyspace_hits": redis_info.get("keyspace_hits"),
                    "keyspace_misses": redis_info.get("keyspace_misses")
                },
                "compression_enabled": self.compression_enabled,
                "serialization_method": self.serialization_method
            }
            
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {"error": str(e)}
    
    async def cleanup_expired_keys(self):
        """Clean up expired keys and optimize memory"""
        try:
            # Get all keys with metadata
            metadata_keys = await self.redis_client.keys("metadata:*")
            
            expired_count = 0
            for metadata_key in metadata_keys:
                # Check if the actual key exists
                actual_key = metadata_key.decode().replace("metadata:", "")
                if not await self.redis_client.exists(actual_key):
                    # Clean up metadata for non-existent keys
                    await self.redis_client.delete(metadata_key)
                    expired_count += 1
            
            logger.info(f"Cleaned up {expired_count} expired metadata entries")
            
        except Exception as e:
            logger.error(f"Error cleaning up expired keys: {e}")
    
    async def warm_cache(self, warmup_data: Dict[str, Any]):
        """Warm up cache with frequently accessed data"""
        try:
            logger.info("Starting cache warmup...")
            
            # Batch set warmup data
            await self.batch_set(warmup_data, ttl=7200)  # 2 hours TTL
            
            logger.info(f"Cache warmed up with {len(warmup_data)} entries")
            
        except Exception as e:
            logger.error(f"Error warming up cache: {e}")
    
    async def close(self):
        """Close Redis connection"""
        try:
            if self.redis_client:
                await self.redis_client.close()
            if self.pool:
                await self.pool.disconnect()
            logger.info("Redis cache connection closed")
            
        except Exception as e:
            logger.error(f"Error closing Redis cache: {e}")


def cache_result(ttl: int = 3600, key_prefix: str = "", compress: bool = None):
    """
    Decorator for caching function results
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{key_prefix}:{func.__name__}:{hashlib.md5(str(args).encode() + str(kwargs).encode()).hexdigest()}"
            
            # Get cache instance (you'd inject this in your app)
            from backend.main import get_redis_cache
            cache = await get_redis_cache()
            
            # Try to get from cache
            result = await cache.get(cache_key)
            if result is not None:
                return result
            
            # Execute function
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            # Store in cache
            await cache.set(cache_key, result, ttl, compress)
            return result
        
        return wrapper
    return decorator


class CacheManager:
    """
    Centralized cache management for the application
    """
    
    def __init__(self, redis_url: str, config: Dict[str, Any]):
        self.redis_url = redis_url
        self.config = config
        self.cache = None
        self.initialized = False
    
    async def initialize(self):
        """Initialize cache manager"""
        if not self.initialized:
            self.cache = EnhancedRedisCache(self.redis_url, self.config)
            await self.cache.initialize()
            self.initialized = True
    
    async def get_cache(self) -> EnhancedRedisCache:
        """Get cache instance"""
        if not self.initialized:
            await self.initialize()
        return self.cache
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        if not self.initialized:
            return {"error": "Cache not initialized"}
        
        return await self.cache.get_cache_stats()
    
    async def cleanup(self):
        """Cleanup cache"""
        if self.initialized and self.cache:
            await self.cache.cleanup_expired_keys()
    
    async def close(self):
        """Close cache manager"""
        if self.initialized and self.cache:
            await self.cache.close()
            self.initialized = False
