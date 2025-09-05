"""
Memory System Health Monitoring and Performance Tracking

This module provides comprehensive health monitoring, performance tracking,
and diagnostics for the Mainza AI memory system.
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging
from collections import defaultdict, deque

from .neo4j_enhanced import Neo4jManager
from .memory_storage_engine import MemoryStorageEngine
from .memory_retrieval_engine import MemoryRetrievalEngine

logger = logging.getLogger(__name__)

class HealthStatus(Enum):
    """Health status levels for memory system components"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"

@dataclass
class PerformanceMetrics:
    """Performance metrics for memory operations"""
    operation_type: str
    total_operations: int = 0
    successful_operations: int = 0
    failed_operations: int = 0
    average_response_time: float = 0.0
    min_response_time: float = float('inf')
    max_response_time: float = 0.0
    last_operation_time: Optional[datetime] = None
    response_times: deque = field(default_factory=lambda: deque(maxlen=100))
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage"""
        if self.total_operations == 0:
            return 0.0
        return (self.successful_operations / self.total_operations) * 100
    
    @property
    def failure_rate(self) -> float:
        """Calculate failure rate percentage"""
        return 100.0 - self.success_rate
    
    def update_metrics(self, response_time: float, success: bool):
        """Update metrics with new operation data"""
        self.total_operations += 1
        self.last_operation_time = datetime.utcnow()
        
        if success:
            self.successful_operations += 1
        else:
            self.failed_operations += 1
        
        # Update response time metrics
        self.response_times.append(response_time)
        self.min_response_time = min(self.min_response_time, response_time)
        self.max_response_time = max(self.max_response_time, response_time)
        
        # Calculate rolling average
        if self.response_times:
            self.average_response_time = sum(self.response_times) / len(self.response_times)

@dataclass
class MemorySystemHealth:
    """Overall memory system health status"""
    overall_status: HealthStatus = HealthStatus.UNKNOWN
    storage_status: HealthStatus = HealthStatus.UNKNOWN
    retrieval_status: HealthStatus = HealthStatus.UNKNOWN
    neo4j_status: HealthStatus = HealthStatus.UNKNOWN
    embedding_status: HealthStatus = HealthStatus.UNKNOWN
    last_check_time: Optional[datetime] = None
    issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def add_issue(self, issue: str, severity: str = "warning"):
        """Add a health issue or warning"""
        if severity == "critical":
            self.issues.append(f"{datetime.utcnow().isoformat()}: {issue}")
        else:
            self.warnings.append(f"{datetime.utcnow().isoformat()}: {issue}")

@dataclass
class MemoryUsageStats:
    """Memory storage usage statistics"""
    total_memories: int = 0
    memories_by_type: Dict[str, int] = field(default_factory=dict)
    memories_by_user: Dict[str, int] = field(default_factory=dict)
    storage_size_mb: float = 0.0
    oldest_memory_date: Optional[datetime] = None
    newest_memory_date: Optional[datetime] = None
    average_memory_size: float = 0.0
    
class MemorySystemMonitor:
    """
    Comprehensive memory system health monitoring and performance tracking
    """
    
    def __init__(self):
        self.neo4j_manager = Neo4jManager()
        self.storage_engine = None
        self.retrieval_engine = None
        
        # Performance tracking
        self.metrics: Dict[str, PerformanceMetrics] = {
            'memory_storage': PerformanceMetrics('memory_storage'),
            'memory_retrieval': PerformanceMetrics('memory_retrieval'),
            'semantic_search': PerformanceMetrics('semantic_search'),
            'context_building': PerformanceMetrics('context_building'),
            'neo4j_operations': PerformanceMetrics('neo4j_operations'),
            'embedding_generation': PerformanceMetrics('embedding_generation')
        }
        
        # Health tracking
        self.health_status = MemorySystemHealth()
        self.usage_stats = MemoryUsageStats()
        
        # Monitoring configuration
        self.health_check_interval = 300  # 5 minutes
        self.performance_window = 3600   # 1 hour
        self.alert_thresholds = {
            'max_response_time': 5.0,      # 5 seconds
            'min_success_rate': 95.0,      # 95%
            'max_storage_size_gb': 10.0,   # 10 GB
            'max_memory_age_days': 365     # 1 year
        }
        
        # Background monitoring
        self._monitoring_active = False
        self._monitoring_task = None
    
    async def initialize(self):
        """Initialize the memory system monitor"""
        try:
            # Initialize storage and retrieval engines
            self.storage_engine = MemoryStorageEngine()
            await self.storage_engine.initialize()
            
            self.retrieval_engine = MemoryRetrievalEngine()
            await self.retrieval_engine.initialize()
            
            logger.info("Memory system monitor initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize memory system monitor: {e}")
            return False
    
    async def start_monitoring(self):
        """Start background health monitoring"""
        if self._monitoring_active:
            logger.warning("Memory monitoring already active")
            return
        
        self._monitoring_active = True
        self._monitoring_task = asyncio.create_task(self._monitoring_loop())
        logger.info("Memory system monitoring started")
    
    async def stop_monitoring(self):
        """Stop background health monitoring"""
        self._monitoring_active = False
        if self._monitoring_task:
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                pass
        logger.info("Memory system monitoring stopped")
    
    async def _monitoring_loop(self):
        """Background monitoring loop"""
        while self._monitoring_active:
            try:
                await self.perform_health_check()
                await self.update_usage_statistics()
                await self._check_alert_conditions()
                
                await asyncio.sleep(self.health_check_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(60)  # Wait before retrying
    
    async def perform_health_check(self) -> MemorySystemHealth:
        """Perform comprehensive health check of memory system"""
        start_time = time.time()
        
        try:
            # Reset health status
            self.health_status = MemorySystemHealth()
            self.health_status.last_check_time = datetime.utcnow()
            
            # Check Neo4j connectivity
            neo4j_healthy = await self._check_neo4j_health()
            self.health_status.neo4j_status = HealthStatus.HEALTHY if neo4j_healthy else HealthStatus.CRITICAL
            
            # Check storage engine health
            storage_healthy = await self._check_storage_health()
            self.health_status.storage_status = HealthStatus.HEALTHY if storage_healthy else HealthStatus.CRITICAL
            
            # Check retrieval engine health
            retrieval_healthy = await self._check_retrieval_health()
            self.health_status.retrieval_status = HealthStatus.HEALTHY if retrieval_healthy else HealthStatus.CRITICAL
            
            # Check embedding service health
            embedding_healthy = await self._check_embedding_health()
            self.health_status.embedding_status = HealthStatus.HEALTHY if embedding_healthy else HealthStatus.WARNING
            
            # Determine overall health
            critical_components = [
                self.health_status.neo4j_status,
                self.health_status.storage_status,
                self.health_status.retrieval_status
            ]
            
            if any(status == HealthStatus.CRITICAL for status in critical_components):
                self.health_status.overall_status = HealthStatus.CRITICAL
            elif any(status == HealthStatus.WARNING for status in critical_components + [self.health_status.embedding_status]):
                self.health_status.overall_status = HealthStatus.WARNING
            else:
                self.health_status.overall_status = HealthStatus.HEALTHY
            
            # Record health check performance
            response_time = time.time() - start_time
            self.record_operation_metric('health_check', response_time, True)
            
            logger.info(f"Health check completed: {self.health_status.overall_status.value}")
            return self.health_status
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            self.health_status.overall_status = HealthStatus.CRITICAL
            self.health_status.add_issue(f"Health check failed: {str(e)}", "critical")
            
            response_time = time.time() - start_time
            self.record_operation_metric('health_check', response_time, False)
            
            return self.health_status
    
    async def _check_neo4j_health(self) -> bool:
        """Check Neo4j database connectivity and performance"""
        try:
            # Test basic connectivity
            result = self.neo4j_manager.execute_query(
                "RETURN 1 as test",
                {}
            )
            
            if not result:
                self.health_status.add_issue("Neo4j connectivity test failed", "critical")
                return False
            
            # Test memory schema existence
            schema_check = self.neo4j_manager.execute_query(
                "MATCH (m:Memory) RETURN count(m) as memory_count LIMIT 1",
                {}
            )
            
            if schema_check is None:
                self.health_status.add_issue("Memory schema not found in Neo4j", "critical")
                return False
            
            return True
            
        except Exception as e:
            self.health_status.add_issue(f"Neo4j health check failed: {str(e)}", "critical")
            return False
    
    async def _check_storage_health(self) -> bool:
        """Check memory storage engine health"""
        try:
            if not self.storage_engine:
                self.health_status.add_issue("Memory storage engine not initialized", "critical")
                return False
            
            # Test storage functionality with a dummy memory
            test_memory_data = {
                'content': 'Health check test memory',
                'memory_type': 'health_check',
                'user_id': 'system',
                'agent_name': 'monitor',
                'consciousness_level': 0.5,
                'emotional_state': 'neutral',
                'importance_score': 0.1
            }
            
            # Try to create and immediately clean up test memory
            memory_id = await self.storage_engine.store_consciousness_memory(
                "Health check test",
                {'consciousness_level': 0.5, 'emotional_state': 'neutral'},
                'health_check'
            )
            
            if memory_id:
                # Clean up test memory (detach delete to remove relationships first)
                self.neo4j_manager.execute_query(
                    "MATCH (m:Memory {memory_id: $memory_id}) DETACH DELETE m",
                    {'memory_id': memory_id}
                )
                return True
            else:
                self.health_status.add_issue("Memory storage test failed", "critical")
                return False
                
        except Exception as e:
            self.health_status.add_issue(f"Storage health check failed: {str(e)}", "critical")
            return False
    
    async def _check_retrieval_health(self) -> bool:
        """Check memory retrieval engine health"""
        try:
            if not self.retrieval_engine:
                self.health_status.add_issue("Memory retrieval engine not initialized", "critical")
                return False
            
            # Test retrieval functionality
            memories = await self.retrieval_engine.get_conversation_history(
                user_id='system',
                limit=1
            )
            
            # Retrieval should work even if no memories exist
            if memories is None:
                self.health_status.add_issue("Memory retrieval test failed", "critical")
                return False
            
            return True
            
        except Exception as e:
            self.health_status.add_issue(f"Retrieval health check failed: {str(e)}", "critical")
            return False
    
    async def _check_embedding_health(self) -> bool:
        """Check embedding service health"""
        try:
            # Test embedding generation
            from .embedding_enhanced import EmbeddingManager
            embedding_manager = EmbeddingManager()
            
            test_embedding = await embedding_manager.generate_embedding("health check test")
            
            if not test_embedding or len(test_embedding) == 0:
                self.health_status.add_issue("Embedding generation test failed", "warning")
                return False
            
            return True
            
        except Exception as e:
            self.health_status.add_issue(f"Embedding health check failed: {str(e)}", "warning")
            return False
    
    def record_operation_metric(self, operation_type: str, response_time: float, success: bool):
        """Record performance metrics for an operation"""
        if operation_type not in self.metrics:
            self.metrics[operation_type] = PerformanceMetrics(operation_type)
        
        self.metrics[operation_type].update_metrics(response_time, success)
    
    async def get_performance_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Get current performance metrics for all operations"""
        metrics_data = {}
        
        for operation_type, metrics in self.metrics.items():
            metrics_data[operation_type] = {
                'total_operations': metrics.total_operations,
                'success_rate': metrics.success_rate,
                'failure_rate': metrics.failure_rate,
                'average_response_time': metrics.average_response_time,
                'min_response_time': metrics.min_response_time if metrics.min_response_time != float('inf') else 0,
                'max_response_time': metrics.max_response_time,
                'last_operation_time': metrics.last_operation_time.isoformat() if metrics.last_operation_time else None
            }
        
        return metrics_data
    
    async def update_usage_statistics(self) -> MemoryUsageStats:
        """Update memory system usage statistics"""
        try:
            # Get total memory count
            total_result = self.neo4j_manager.execute_query(
                "MATCH (m:Memory) RETURN count(m) as total",
                {}
            )
            self.usage_stats.total_memories = total_result[0]['total'] if total_result else 0
            
            # Get memories by type
            type_result = self.neo4j_manager.execute_query(
                "MATCH (m:Memory) RETURN m.memory_type as type, count(m) as count",
                {}
            )
            self.usage_stats.memories_by_type = {
                record['type']: record['count'] for record in type_result
            } if type_result else {}
            
            # Get memories by user (top 10)
            user_result = self.neo4j_manager.execute_query(
                "MATCH (m:Memory) RETURN m.user_id as user_id, count(m) as count ORDER BY count DESC LIMIT 10",
                {}
            )
            self.usage_stats.memories_by_user = {
                record['user_id']: record['count'] for record in user_result
            } if user_result else {}
            
            # Get date range
            date_result = self.neo4j_manager.execute_query(
                "MATCH (m:Memory) RETURN min(m.created_at) as oldest, max(m.created_at) as newest",
                {}
            )
            if date_result and date_result[0]['oldest']:
                try:
                    oldest_str = date_result[0]['oldest']
                    newest_str = date_result[0]['newest']
                    
                    # Handle different datetime formats
                    if isinstance(oldest_str, str):
                        # Remove timezone info if present
                        oldest_str = oldest_str.replace('Z', '+00:00')
                        if '+' in oldest_str:
                            # Parse with timezone and convert to naive
                            from dateutil import parser as date_parser
                            self.usage_stats.oldest_memory_date = date_parser.parse(oldest_str).replace(tzinfo=None)
                        else:
                            self.usage_stats.oldest_memory_date = datetime.fromisoformat(oldest_str)
                    
                    if isinstance(newest_str, str):
                        # Remove timezone info if present
                        newest_str = newest_str.replace('Z', '+00:00')
                        if '+' in newest_str:
                            # Parse with timezone and convert to naive
                            from dateutil import parser as date_parser
                            self.usage_stats.newest_memory_date = date_parser.parse(newest_str).replace(tzinfo=None)
                        else:
                            self.usage_stats.newest_memory_date = datetime.fromisoformat(newest_str)
                            
                except Exception as e:
                    logger.warning(f"Failed to parse memory dates: {e}")
                    # Set to None if parsing fails
                    self.usage_stats.oldest_memory_date = None
                    self.usage_stats.newest_memory_date = None
            
            # Estimate storage size (rough calculation)
            size_result = self.neo4j_manager.execute_query(
                "MATCH (m:Memory) RETURN avg(size(m.content)) as avg_size",
                {}
            )
            if size_result and size_result[0]['avg_size']:
                avg_content_size = size_result[0]['avg_size']
                # Rough estimate including metadata and relationships
                estimated_size_bytes = self.usage_stats.total_memories * (avg_content_size + 500)
                self.usage_stats.storage_size_mb = estimated_size_bytes / (1024 * 1024)
                self.usage_stats.average_memory_size = avg_content_size
            
            return self.usage_stats
            
        except Exception as e:
            logger.error(f"Failed to update usage statistics: {e}")
            return self.usage_stats
    
    async def _check_alert_conditions(self):
        """Check for alert conditions and log warnings"""
        try:
            # Check response time alerts
            for operation_type, metrics in self.metrics.items():
                if metrics.average_response_time > self.alert_thresholds['max_response_time']:
                    self.health_status.add_issue(
                        f"{operation_type} average response time ({metrics.average_response_time:.2f}s) exceeds threshold",
                        "warning"
                    )
                
                if metrics.success_rate < self.alert_thresholds['min_success_rate']:
                    self.health_status.add_issue(
                        f"{operation_type} success rate ({metrics.success_rate:.1f}%) below threshold",
                        "critical"
                    )
            
            # Check storage size alerts
            if self.usage_stats.storage_size_mb > (self.alert_thresholds['max_storage_size_gb'] * 1024):
                self.health_status.add_issue(
                    f"Memory storage size ({self.usage_stats.storage_size_mb:.1f} MB) exceeds threshold",
                    "warning"
                )
            
            # Check memory age alerts
            if self.usage_stats.oldest_memory_date:
                age_days = (datetime.utcnow() - self.usage_stats.oldest_memory_date).days
                if age_days > self.alert_thresholds['max_memory_age_days']:
                    self.health_status.add_issue(
                        f"Oldest memory is {age_days} days old, consider cleanup",
                        "warning"
                    )
            
        except Exception as e:
            logger.error(f"Error checking alert conditions: {e}")
    
    async def get_system_status_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive system status for dashboard display"""
        await self.perform_health_check()
        await self.update_usage_statistics()
        
        return {
            'health_status': {
                'overall_status': self.health_status.overall_status.value,
                'storage_status': self.health_status.storage_status.value,
                'retrieval_status': self.health_status.retrieval_status.value,
                'neo4j_status': self.health_status.neo4j_status.value,
                'embedding_status': self.health_status.embedding_status.value,
                'last_check_time': self.health_status.last_check_time.isoformat() if self.health_status.last_check_time else None,
                'issues': self.health_status.issues[-10:],  # Last 10 issues
                'warnings': self.health_status.warnings[-10:]  # Last 10 warnings
            },
            'performance_metrics': await self.get_performance_metrics(),
            'usage_statistics': {
                'total_memories': self.usage_stats.total_memories,
                'memories_by_type': self.usage_stats.memories_by_type,
                'memories_by_user': dict(list(self.usage_stats.memories_by_user.items())[:5]),  # Top 5 users
                'storage_size_mb': round(self.usage_stats.storage_size_mb, 2),
                'oldest_memory_date': self.usage_stats.oldest_memory_date.isoformat() if self.usage_stats.oldest_memory_date else None,
                'newest_memory_date': self.usage_stats.newest_memory_date.isoformat() if self.usage_stats.newest_memory_date else None,
                'average_memory_size': round(self.usage_stats.average_memory_size, 2)
            },
            'alert_thresholds': self.alert_thresholds,
            'monitoring_active': self._monitoring_active
        }

# Global monitor instance
memory_monitor = MemorySystemMonitor()