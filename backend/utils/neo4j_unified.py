"""
Unified Neo4j Manager for Mainza AI
Consolidates all Neo4j operations with production-ready features:
- Single connection pool management
- Circuit breaker pattern
- Query caching
- Performance monitoring
- Error handling and resilience
"""
import os
import logging
import time
import asyncio
from contextlib import contextmanager
from typing import Optional, Dict, Any, List, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import json
import threading
from collections import defaultdict

from neo4j import GraphDatabase, basic_auth, Session, Transaction
from neo4j.exceptions import ServiceUnavailable, TransientError, ClientError
from cachetools import TTLCache

logger = logging.getLogger(__name__)

class CircuitBreakerState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

@dataclass
class QueryMetrics:
    query: str
    execution_time: float
    record_count: int
    success: bool
    error_message: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

class CircuitBreaker:
    """Circuit breaker for Neo4j connection resilience"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitBreakerState.CLOSED
        self.half_open_calls = 0
        self.half_open_max_calls = 3
        
    def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        if self.state == CircuitBreakerState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitBreakerState.HALF_OPEN
                self.half_open_calls = 0
            else:
                raise ServiceUnavailable("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        if self.last_failure_time is None:
            return True
        return time.time() - self.last_failure_time >= self.recovery_timeout
    
    def _on_success(self):
        """Handle successful operation"""
        self.failure_count = 0
        self.state = CircuitBreakerState.CLOSED
        self.half_open_calls = 0
    
    def _on_failure(self):
        """Handle failed operation"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.half_open_calls += 1
            if self.half_open_calls >= self.half_open_max_calls:
                self.state = CircuitBreakerState.OPEN
        elif self.failure_count >= self.failure_threshold:
            self.state = CircuitBreakerState.OPEN

class QueryValidator:
    """Enhanced query validation with security and performance checks"""
    
    DANGEROUS_PATTERNS = [
        r'\bDROP\s+DATABASE\b',
        r'\bDELETE\s+ALL\b',
        r'\bDETACH\s+DELETE\s+ALL\b',
        r'\bCREATE\s+DATABASE\b',
        r'\bALTER\s+DATABASE\b',
        r';\s*MATCH',  # Query chaining
        r'LOAD\s+CSV',  # File operations
        r'CALL\s+apoc\.export',  # Export operations
        r'CALL\s+apoc\.import',  # Import operations
    ]
    
    PERFORMANCE_LIMITS = {
        'max_match_clauses': 15,
        'max_query_length': 15000,
        'max_limit_value': 10000,
    }
    
    @classmethod
    def validate_query(cls, query: str, parameters: Optional[Dict] = None) -> tuple[bool, str]:
        """Comprehensive query validation"""
        import re
        query_upper = query.upper()
        
        # Security checks
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, query_upper, re.IGNORECASE):
                return False, f"Dangerous pattern detected: {pattern}"
        
        # Performance checks
        if len(query) > cls.PERFORMANCE_LIMITS['max_query_length']:
            return False, f"Query too long: {len(query)} > {cls.PERFORMANCE_LIMITS['max_query_length']}"
        
        match_count = query_upper.count('MATCH')
        if match_count > cls.PERFORMANCE_LIMITS['max_match_clauses']:
            return False, f"Too many MATCH clauses: {match_count} > {cls.PERFORMANCE_LIMITS['max_match_clauses']}"
        
        # Check LIMIT values in parameters
        if parameters:
            for key, value in parameters.items():
                if 'limit' in key.lower() and isinstance(value, int):
                    if value > cls.PERFORMANCE_LIMITS['max_limit_value']:
                        return False, f"LIMIT value too high: {value} > {cls.PERFORMANCE_LIMITS['max_limit_value']}"
        
        return True, "Valid"

class Neo4jQueryCache:
    """Intelligent query caching with TTL and invalidation"""
    
    def __init__(self, maxsize: int = 1000, ttl: int = 300):
        self.cache = TTLCache(maxsize=maxsize, ttl=ttl)
        self.query_stats = defaultdict(int)
        self.cache_hits = 0
        self.cache_misses = 0
    
    def get_cached_result(self, query_hash: str, params: Dict) -> Optional[List]:
        """Get cached query result if available and valid"""
        cache_key = f"{query_hash}:{hash(str(sorted(params.items())))}"
        result = self.cache.get(cache_key)
        
        if result is not None:
            self.cache_hits += 1
            self.query_stats[query_hash] += 1
            logger.debug(f"Cache HIT for query: {query_hash[:50]}...")
            return result
        
        self.cache_misses += 1
        logger.debug(f"Cache MISS for query: {query_hash[:50]}...")
        return None
    
    def cache_result(self, query_hash: str, params: Dict, result: List):
        """Cache query result with TTL"""
        cache_key = f"{query_hash}:{hash(str(sorted(params.items())))}"
        self.cache[cache_key] = result
        logger.debug(f"Cached result for query: {query_hash[:50]}...")
    
    def should_cache(self, query: str) -> bool:
        """Determine if query should be cached based on patterns"""
        read_only_patterns = ['MATCH', 'RETURN', 'WITH', 'CALL']
        write_patterns = ['CREATE', 'MERGE', 'SET', 'DELETE', 'DETACH', 'REMOVE']
        
        query_upper = query.upper()
        has_read = any(pattern in query_upper for pattern in read_only_patterns)
        has_write = any(pattern in query_upper for pattern in write_patterns)
        
        # Cache read-only queries, don't cache write queries
        return has_read and not has_write
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        total_requests = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'hit_rate_percent': round(hit_rate, 2),
            'cache_size': len(self.cache),
            'max_size': self.cache.maxsize,
            'ttl_seconds': self.cache.ttl
        }

class Neo4jPerformanceMonitor:
    """Performance monitoring and metrics collection"""
    
    def __init__(self):
        self.slow_query_threshold = 1.0  # seconds
        self.query_metrics: List[QueryMetrics] = []
        self.metrics_lock = threading.Lock()
        self.max_metrics_history = 1000
        self.alert_thresholds = {
            'avg_query_time': 0.5,  # 500ms
            'error_rate': 0.05,     # 5%
            'slow_query_rate': 0.1  # 10%
        }
    
    def record_query_metrics(self, query: str, execution_time: float, 
                           record_count: int, success: bool, error_message: str = None):
        """Record query performance metrics"""
        with self.metrics_lock:
            metrics = QueryMetrics(
                query=query,
                execution_time=execution_time,
                record_count=record_count,
                success=success,
                error_message=error_message
            )
            
            self.query_metrics.append(metrics)
            
            # Keep only recent metrics
            if len(self.query_metrics) > self.max_metrics_history:
                self.query_metrics = self.query_metrics[-self.max_metrics_history:]
            
            # Log slow queries
            if execution_time > self.slow_query_threshold:
                logger.warning(f"Slow query detected ({execution_time:.2f}s): {query[:200]}...")
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate performance report with recommendations"""
        with self.metrics_lock:
            if not self.query_metrics:
                return {'status': 'no_data', 'message': 'No query metrics available'}
            
            recent_metrics = [m for m in self.query_metrics 
                            if m.timestamp > datetime.now() - timedelta(hours=1)]
            
            if not recent_metrics:
                return {'status': 'no_recent_data', 'message': 'No recent query metrics'}
            
            total_queries = len(recent_metrics)
            successful_queries = len([m for m in recent_metrics if m.success])
            failed_queries = total_queries - successful_queries
            slow_queries = len([m for m in recent_metrics if m.execution_time > self.slow_query_threshold])
            
            avg_execution_time = sum(m.execution_time for m in recent_metrics) / total_queries
            error_rate = failed_queries / total_queries if total_queries > 0 else 0
            slow_query_rate = slow_queries / total_queries if total_queries > 0 else 0
            
            # Generate recommendations
            recommendations = []
            if avg_execution_time > self.alert_thresholds['avg_query_time']:
                recommendations.append("Consider adding indexes for frequently queried properties")
            if error_rate > self.alert_thresholds['error_rate']:
                recommendations.append("High error rate detected - check connection stability")
            if slow_query_rate > self.alert_thresholds['slow_query_rate']:
                recommendations.append("High slow query rate - optimize query patterns")
            
            return {
                'timestamp': datetime.now().isoformat(),
                'total_queries': total_queries,
                'successful_queries': successful_queries,
                'failed_queries': failed_queries,
                'slow_queries': slow_queries,
                'avg_execution_time_ms': round(avg_execution_time * 1000, 2),
                'error_rate_percent': round(error_rate * 100, 2),
                'slow_query_rate_percent': round(slow_query_rate * 100, 2),
                'recommendations': recommendations
            }
    
    def detect_slow_queries(self) -> List[Dict[str, Any]]:
        """Identify queries exceeding performance thresholds"""
        with self.metrics_lock:
            slow_queries = [m for m in self.query_metrics 
                          if m.execution_time > self.slow_query_threshold]
            
            return [{
                'query': metrics.query[:200] + '...' if len(metrics.query) > 200 else metrics.query,
                'execution_time_ms': round(metrics.execution_time * 1000, 2),
                'record_count': metrics.record_count,
                'timestamp': metrics.timestamp.isoformat()
            } for metrics in slow_queries[-10:]]  # Last 10 slow queries

class UnifiedNeo4jManager:
    """Unified Neo4j manager with production-ready features"""
    
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD")
        self.database = os.getenv("NEO4J_DATABASE", "neo4j")
        
        if not self.password:
            raise ValueError("NEO4J_PASSWORD environment variable is required")
        
        # Calculate optimal pool size based on agent count
        agent_count = 8  # Router, GraphMaster, TaskMaster, CodeWeaver, RAG, Conductor, Notification, Calendar
        concurrent_users = int(os.getenv("NEO4J_CONCURRENT_USERS", "10"))
        optimal_pool_size = max(50, agent_count * concurrent_users * 2)
        
        # Production configuration
        self.driver = GraphDatabase.driver(
            self.uri,
            auth=basic_auth(self.user, self.password),
            max_connection_lifetime=60 * 60,  # 1 hour
            max_connection_pool_size=optimal_pool_size,
            connection_acquisition_timeout=30,
            connection_timeout=15,
            encrypted=os.getenv("NEO4J_ENCRYPTED", "false").lower() == "true",
            trust=os.getenv("NEO4J_TRUST", "TRUST_ALL_CERTIFICATES"),
            keep_alive=True,
            max_transaction_retry_time=30
        )
        
        # Circuit breaker for connection resilience
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=int(os.getenv("NEO4J_CIRCUIT_BREAKER_THRESHOLD", "5")),
            recovery_timeout=int(os.getenv("NEO4J_CIRCUIT_BREAKER_TIMEOUT", "60"))
        )
        
        # Query caching
        self.query_cache = Neo4jQueryCache(
            maxsize=int(os.getenv("NEO4J_CACHE_SIZE", "1000")),
            ttl=int(os.getenv("NEO4J_CACHE_TTL", "300"))
        )
        
        # Performance monitoring
        self.performance_monitor = Neo4jPerformanceMonitor()
        self.slow_query_threshold = float(os.getenv("NEO4J_SLOW_QUERY_THRESHOLD", "1.0"))
        
        logger.info(f"Initialized Unified Neo4j Manager for {self.uri} with pool size {optimal_pool_size}")
    
    def close(self):
        """Close the driver connection"""
        if self.driver:
            self.driver.close()
            logger.info("Unified Neo4j driver closed")
    
    @contextmanager
    def get_session(self, database: Optional[str] = None, access_mode: str = "READ"):
        """Enhanced session context manager with circuit breaker"""
        session = None
        try:
            def create_session():
                return self.driver.session(
                    database=database or self.database,
                    default_access_mode=access_mode
                )
            
            session = self.circuit_breaker.call(create_session)
            yield session
            
        except ServiceUnavailable as e:
            logger.error(f"Neo4j service unavailable: {e}")
            raise
        except Exception as e:
            logger.error(f"Neo4j session error: {e}")
            raise
        finally:
            if session:
                session.close()
    
    @contextmanager
    def get_transaction(self, database: Optional[str] = None, timeout: Optional[int] = None):
        """Enhanced transaction context manager with automatic rollback"""
        with self.get_session(database, "WRITE") as session:
            tx = session.begin_transaction(timeout=timeout)
            try:
                yield tx
                tx.commit()
                logger.debug("Transaction committed successfully")
            except Exception as e:
                tx.rollback()
                logger.error(f"Transaction rolled back due to error: {e}")
                raise
            finally:
                if not tx.closed():
                    tx.close()
    
    def execute_query(self, query: str, parameters: Optional[Dict[str, Any]] = None,
                     database: Optional[str] = None, retry_count: int = 3,
                     timeout: Optional[int] = None, access_mode: str = "AUTO",
                     use_cache: bool = True) -> List[Dict[str, Any]]:
        """Execute query with comprehensive error handling and monitoring"""
        parameters = parameters or {}
        
        # Auto-detect access mode if not specified
        if access_mode == "AUTO":
            query_upper = query.upper().strip()
            write_keywords = ['CREATE', 'MERGE', 'SET', 'DELETE', 'DETACH', 'REMOVE', 'FOREACH']
            access_mode = "WRITE" if any(keyword in query_upper for keyword in write_keywords) else "READ"
        
        # Validate query
        is_valid, validation_msg = QueryValidator.validate_query(query, parameters)
        if not is_valid:
            error_msg = f"Query validation failed: {validation_msg}"
            logger.warning(error_msg)
            self.performance_monitor.record_query_metrics(query, 0, 0, False, error_msg)
            raise ValueError(error_msg)
        
        # Check cache for read queries
        if use_cache and access_mode == "READ" and self.query_cache.should_cache(query):
            query_hash = str(hash(query))
            cached_result = self.query_cache.get_cached_result(query_hash, parameters)
            if cached_result is not None:
                return cached_result
        
        start_time = time.time()
        last_exception = None
        
        for attempt in range(retry_count):
            try:
                with self.get_session(database, access_mode) as session:
                    result = session.run(query, parameters, timeout=timeout)
                    records = [dict(record) for record in result]
                    
                    execution_time = time.time() - start_time
                    self.performance_monitor.record_query_metrics(
                        query, execution_time, len(records), True
                    )
                    
                    # Cache successful read queries
                    if use_cache and access_mode == "READ" and self.query_cache.should_cache(query):
                        query_hash = str(hash(query))
                        self.query_cache.cache_result(query_hash, parameters, records)
                    
                    # Log slow queries
                    if execution_time > self.slow_query_threshold:
                        logger.warning(f"Slow query detected ({execution_time:.2f}s): {query[:200]}...")
                    
                    return records
                    
            except TransientError as e:
                last_exception = e
                if attempt < retry_count - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"Transient error on attempt {attempt + 1}, retrying in {wait_time}s: {e}")
                    time.sleep(wait_time)
                    continue
                else:
                    execution_time = time.time() - start_time
                    self.performance_monitor.record_query_metrics(
                        query, execution_time, 0, False, str(e)
                    )
                    logger.error(f"Query failed after {retry_count} attempts: {e}")
                    raise
                    
            except Exception as e:
                execution_time = time.time() - start_time
                self.performance_monitor.record_query_metrics(
                    query, execution_time, 0, False, str(e)
                )
                logger.error(f"Query execution error: {e}")
                raise
        
        # This should never be reached, but just in case
        if last_exception:
            raise last_exception
    
    def execute_write_query(self, query: str, parameters: Optional[Dict[str, Any]] = None,
                           database: Optional[str] = None, timeout: Optional[int] = None) -> List[Dict[str, Any]]:
        """Execute a write query within a transaction"""
        return self.execute_query(query, parameters, database, access_mode="WRITE", timeout=timeout, use_cache=False)
    
    async def execute_query_async(self, query: str, parameters: Optional[Dict[str, Any]] = None,
                                 database: Optional[str] = None, retry_count: int = 3,
                                 timeout: Optional[int] = None, access_mode: str = "AUTO") -> List[Dict[str, Any]]:
        """Execute query asynchronously"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, self.execute_query, query, parameters, database, retry_count, timeout, access_mode
        )
    
    def health_check(self) -> bool:
        """Check if Neo4j is accessible"""
        try:
            with self.get_session() as session:
                result = session.run("RETURN 1 AS health")
                return result.single()["health"] == 1
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def get_database_info(self) -> Dict[str, Any]:
        """Get database information and statistics"""
        try:
            queries = {
                "node_count": "MATCH (n) RETURN count(n) AS count",
                "relationship_count": "MATCH ()-[r]->() RETURN count(r) AS count",
                "node_labels": "MATCH (n) RETURN labels(n)[0] AS label, count(n) AS count ORDER BY count DESC LIMIT 10",
                "relationship_types": "MATCH ()-[r]->() RETURN type(r) AS type, count(r) AS count ORDER BY count DESC LIMIT 10",
                "indexes": "SHOW INDEXES YIELD name, type, state, populationPercent RETURN name, type, state, populationPercent",
                "constraints": "SHOW CONSTRAINTS YIELD name, type RETURN name, type"
            }
            
            info = {}
            for key, query in queries.items():
                try:
                    result = self.execute_query(query)
                    info[key] = result
                except Exception as e:
                    logger.warning(f"Failed to get {key}: {e}")
                    info[key] = None
            
            return info
        except Exception as e:
            logger.error(f"Failed to get database info: {e}")
            return {}
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get comprehensive performance metrics"""
        return {
            'performance_report': self.performance_monitor.get_performance_report(),
            'cache_stats': self.query_cache.get_cache_stats(),
            'slow_queries': self.performance_monitor.detect_slow_queries(),
            'circuit_breaker_state': self.circuit_breaker.state.value,
            'circuit_breaker_failures': self.circuit_breaker.failure_count
        }

# Global instance
neo4j_unified = UnifiedNeo4jManager()

# Backward compatibility
driver = neo4j_unified.driver

# Cleanup on module exit
import atexit
atexit.register(neo4j_unified.close)
