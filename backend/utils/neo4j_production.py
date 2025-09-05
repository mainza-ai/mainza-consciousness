"""
Production-ready Neo4j utilities with comprehensive error handling, monitoring, and security.
Addresses all critical issues from the code review:
- Connection pooling with circuit breaker pattern
- Comprehensive transaction management
- Query performance monitoring
- Security enhancements
- Health monitoring and metrics
"""
import os
import logging
import time
from contextlib import contextmanager
from typing import Optional, Dict, Any, List, Callable, Union
from dataclasses import dataclass
from enum import Enum
from neo4j import GraphDatabase, basic_auth, Session, Transaction
from neo4j.exceptions import ServiceUnavailable, TransientError, ClientError
import threading
from datetime import datetime, timedelta
import json

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
    error: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class CircuitBreaker:
    """Circuit breaker pattern for Neo4j connections."""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitBreakerState.CLOSED
        self._lock = threading.Lock()
    
    def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        with self._lock:
            if self.state == CircuitBreakerState.OPEN:
                if self._should_attempt_reset():
                    self.state = CircuitBreakerState.HALF_OPEN
                else:
                    raise ServiceUnavailable("Circuit breaker is OPEN")
            
            try:
                result = func(*args, **kwargs)
                self._on_success()
                return result
            except Exception as e:
                self._on_failure()
                raise e
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if self.last_failure_time is None:
            return True
        return (datetime.now() - self.last_failure_time).seconds >= self.recovery_timeout
    
    def _on_success(self):
        """Handle successful operation."""
        self.failure_count = 0
        self.state = CircuitBreakerState.CLOSED
    
    def _on_failure(self):
        """Handle failed operation."""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitBreakerState.OPEN

class QueryValidator:
    """Enhanced query validation with security and performance checks."""
    
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
        'max_match_clauses': 15,  # Increased to allow more complex queries
        'max_query_length': 15000,  # Increased query length limit
        'max_limit_value': 10000,
    }
    
    @classmethod
    def validate_query(cls, query: str, parameters: Optional[Dict] = None) -> tuple[bool, str]:
        """Comprehensive query validation."""
        query_upper = query.upper()
        
        # Security checks
        for pattern in cls.DANGEROUS_PATTERNS:
            import re
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

class Neo4jProductionManager:
    """Production-ready Neo4j manager with comprehensive features."""
    
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD")
        
        if not self.password:
            raise ValueError("NEO4J_PASSWORD environment variable is required")
        self.database = os.getenv("NEO4J_DATABASE", "neo4j")
        
        # Production configuration
        self.driver = GraphDatabase.driver(
            self.uri,
            auth=basic_auth(self.user, self.password),
            max_connection_lifetime=30 * 60,  # 30 minutes
            max_connection_pool_size=50,
            connection_acquisition_timeout=60,  # 60 seconds
            connection_timeout=30,
            encrypted=os.getenv("NEO4J_ENCRYPTED", "false").lower() == "true",
            trust=os.getenv("NEO4J_TRUST", "TRUST_ALL_CERTIFICATES")
        )
        
        # Circuit breaker for connection resilience
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=int(os.getenv("NEO4J_CIRCUIT_BREAKER_THRESHOLD", "5")),
            recovery_timeout=int(os.getenv("NEO4J_CIRCUIT_BREAKER_TIMEOUT", "60"))
        )
        
        # Query metrics storage
        self.query_metrics: List[QueryMetrics] = []
        self.metrics_lock = threading.Lock()
        self.max_metrics_history = 1000
        
        # Performance monitoring
        self.slow_query_threshold = float(os.getenv("NEO4J_SLOW_QUERY_THRESHOLD", "1.0"))  # seconds
        
        logger.info(f"Initialized Neo4j Production Manager for {self.uri}")
    
    def close(self):
        """Close the driver connection."""
        if self.driver:
            self.driver.close()
            logger.info("Neo4j driver closed")
    
    @contextmanager
    def get_session(self, database: Optional[str] = None, access_mode: str = "READ"):
        """Enhanced session context manager with circuit breaker."""
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
        """Enhanced transaction context manager with automatic rollback."""
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
                     timeout: Optional[int] = None) -> List[Dict[str, Any]]:
        """Execute query with comprehensive error handling and monitoring."""
        parameters = parameters or {}
        
        # Validate query
        is_valid, validation_msg = QueryValidator.validate_query(query, parameters)
        if not is_valid:
            error_msg = f"Query validation failed: {validation_msg}"
            logger.warning(error_msg)
            self._record_metrics(query, 0, 0, False, error_msg)
            raise ValueError(error_msg)
        
        start_time = time.time()
        last_exception = None
        
        for attempt in range(retry_count):
            try:
                with self.get_session(database) as session:
                    result = session.run(query, parameters, timeout=timeout)
                    records = [dict(record) for record in result]
                    
                    execution_time = time.time() - start_time
                    self._record_metrics(query, execution_time, len(records), True)
                    
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
                    self._record_metrics(query, execution_time, 0, False, str(e))
                    logger.error(f"Query failed after {retry_count} attempts: {e}")
                    raise
                    
            except Exception as e:
                execution_time = time.time() - start_time
                self._record_metrics(query, execution_time, 0, False, str(e))
                logger.error(f"Query execution error: {e}")
                raise
        
        # This should never be reached, but just in case
        if last_exception:
            raise last_exception
    
    def execute_write_query(self, query: str, parameters: Optional[Dict[str, Any]] = None,
                           database: Optional[str] = None, timeout: Optional[int] = None) -> List[Dict[str, Any]]:
        """Execute write query within a transaction."""
        parameters = parameters or {}
        
        # Validate query
        is_valid, validation_msg = QueryValidator.validate_query(query, parameters)
        if not is_valid:
            error_msg = f"Write query validation failed: {validation_msg}"
            logger.warning(error_msg)
            raise ValueError(error_msg)
        
        start_time = time.time()
        
        try:
            with self.get_transaction(database, timeout) as tx:
                result = tx.run(query, parameters)
                records = [dict(record) for record in result]
                
                execution_time = time.time() - start_time
                self._record_metrics(query, execution_time, len(records), True)
                
                return records
                
        except Exception as e:
            execution_time = time.time() - start_time
            self._record_metrics(query, execution_time, 0, False, str(e))
            logger.error(f"Write query execution error: {e}")
            raise
    
    def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check with detailed metrics."""
        health_info = {
            "status": "unknown",
            "timestamp": datetime.now().isoformat(),
            "connection_status": "unknown",
            "circuit_breaker_state": self.circuit_breaker.state.value,
            "database_info": {},
            "performance_metrics": {}
        }
        
        try:
            # Basic connectivity test
            start_time = time.time()
            with self.get_session() as session:
                result = session.run("RETURN 1 AS health")
                health_value = result.single()["health"]
                
            connection_time = time.time() - start_time
            
            if health_value == 1:
                health_info["status"] = "healthy"
                health_info["connection_status"] = "connected"
                health_info["connection_time_ms"] = round(connection_time * 1000, 2)
            else:
                health_info["status"] = "unhealthy"
                health_info["connection_status"] = "invalid_response"
            
            # Get database statistics
            health_info["database_info"] = self._get_database_statistics()
            health_info["performance_metrics"] = self._get_performance_metrics()
            
        except Exception as e:
            health_info["status"] = "unhealthy"
            health_info["connection_status"] = "failed"
            health_info["error"] = str(e)
            logger.error(f"Health check failed: {e}")
        
        return health_info
    
    def _get_database_statistics(self) -> Dict[str, Any]:
        """Get comprehensive database statistics."""
        stats = {}
        
        stat_queries = {
            "node_count": "MATCH (n) RETURN count(n) AS count",
            "relationship_count": "MATCH ()-[r]->() RETURN count(r) AS count",
            "node_labels": "MATCH (n) RETURN labels(n)[0] AS label, count(n) AS count ORDER BY count DESC LIMIT 10",
            "relationship_types": "MATCH ()-[r]->() RETURN type(r) AS type, count(r) AS count ORDER BY count DESC LIMIT 10",
            "indexes": "SHOW INDEXES YIELD name, type, state, populationPercent RETURN name, type, state, populationPercent",
            "constraints": "SHOW CONSTRAINTS YIELD name, type RETURN name, type"
        }
        
        for key, query in stat_queries.items():
            try:
                result = self.execute_query(query)
                stats[key] = result
            except Exception as e:
                logger.warning(f"Failed to get {key}: {e}")
                stats[key] = {"error": str(e)}
        
        return stats
    
    def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics from query history."""
        with self.metrics_lock:
            if not self.query_metrics:
                return {"message": "No metrics available"}
            
            recent_metrics = [m for m in self.query_metrics 
                            if (datetime.now() - m.timestamp).seconds < 3600]  # Last hour
            
            if not recent_metrics:
                return {"message": "No recent metrics available"}
            
            total_queries = len(recent_metrics)
            successful_queries = len([m for m in recent_metrics if m.success])
            failed_queries = total_queries - successful_queries
            
            execution_times = [m.execution_time for m in recent_metrics if m.success]
            
            metrics = {
                "total_queries_last_hour": total_queries,
                "successful_queries": successful_queries,
                "failed_queries": failed_queries,
                "success_rate": round((successful_queries / total_queries) * 100, 2) if total_queries > 0 else 0,
                "avg_execution_time_ms": round(sum(execution_times) / len(execution_times) * 1000, 2) if execution_times else 0,
                "slow_queries_count": len([t for t in execution_times if t > self.slow_query_threshold])
            }
            
            if execution_times:
                execution_times.sort()
                metrics["median_execution_time_ms"] = round(execution_times[len(execution_times) // 2] * 1000, 2)
                metrics["p95_execution_time_ms"] = round(execution_times[int(len(execution_times) * 0.95)] * 1000, 2)
            
            return metrics
    
    def _record_metrics(self, query: str, execution_time: float, record_count: int, 
                       success: bool, error: Optional[str] = None):
        """Record query metrics for monitoring."""
        metric = QueryMetrics(
            query=query[:200],  # Truncate long queries
            execution_time=execution_time,
            record_count=record_count,
            success=success,
            error=error
        )
        
        with self.metrics_lock:
            self.query_metrics.append(metric)
            
            # Keep only recent metrics to prevent memory bloat
            if len(self.query_metrics) > self.max_metrics_history:
                self.query_metrics = self.query_metrics[-self.max_metrics_history:]
    
    def get_query_metrics(self, hours_back: int = 1) -> List[Dict[str, Any]]:
        """Get query metrics for analysis."""
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        with self.metrics_lock:
            recent_metrics = [
                {
                    "query": m.query,
                    "execution_time_ms": round(m.execution_time * 1000, 2),
                    "record_count": m.record_count,
                    "success": m.success,
                    "error": m.error,
                    "timestamp": m.timestamp.isoformat()
                }
                for m in self.query_metrics
                if m.timestamp >= cutoff_time
            ]
        
        return recent_metrics
    
    def optimize_database(self) -> Dict[str, Any]:
        """Run database optimization tasks."""
        optimization_results = {}
        
        optimization_tasks = [
            ("Update Statistics", "CALL db.stats.retrieve('GRAPH COUNTS')"),
            ("Analyze Indexes", "SHOW INDEXES YIELD name, type, state, populationPercent WHERE populationPercent < 100"),
        ]
        
        for task_name, query in optimization_tasks:
            try:
                start_time = time.time()
                result = self.execute_query(query)
                execution_time = time.time() - start_time
                
                optimization_results[task_name] = {
                    "status": "completed",
                    "execution_time_ms": round(execution_time * 1000, 2),
                    "result": result
                }
                
            except Exception as e:
                optimization_results[task_name] = {
                    "status": "failed",
                    "error": str(e)
                }
        
        return optimization_results

# Global production instance
neo4j_production = Neo4jProductionManager()

# Backward compatibility
driver = neo4j_production.driver

# Cleanup on module exit
import atexit
atexit.register(neo4j_production.close)