"""
Comprehensive Performance Monitoring System for Mainza AI
Implements advanced monitoring, metrics collection, and optimization recommendations
"""

import asyncio
import logging
import time
import psutil
import json
from typing import Dict, List, Any, Optional, Tuple, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import numpy as np
from neo4j import GraphDatabase
import redis.asyncio as redis

logger = logging.getLogger(__name__)

class MetricType(Enum):
    """Types of performance metrics"""
    SYSTEM = "system"  # System-level metrics
    APPLICATION = "application"  # Application-level metrics
    DATABASE = "database"  # Database performance metrics
    MEMORY = "memory"  # Memory usage metrics
    NETWORK = "network"  # Network performance metrics
    AGENT = "agent"  # Agent-specific metrics
    CACHE = "cache"  # Cache performance metrics

class AlertLevel(Enum):
    """Alert levels for performance issues"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

@dataclass
class PerformanceMetric:
    """Represents a performance metric with metadata"""
    name: str
    value: float
    metric_type: MetricType
    timestamp: datetime
    unit: str
    tags: Dict[str, str] = field(default_factory=dict)
    alert_level: Optional[AlertLevel] = None
    threshold: Optional[float] = None

@dataclass
class PerformanceAlert:
    """Represents a performance alert"""
    id: str
    metric_name: str
    current_value: float
    threshold_value: float
    alert_level: AlertLevel
    message: str
    timestamp: datetime
    resolved: bool = False
    resolution_time: Optional[datetime] = None

class PerformanceMonitoringSystem:
    """
    Comprehensive performance monitoring system for Mainza AI
    """
    
    def __init__(self, neo4j_driver, redis_client: Optional[redis.Redis] = None, config: Dict[str, Any] = None):
        self.driver = neo4j_driver
        self.redis_client = redis_client
        self.config = config or {}
        
        # Metrics storage
        self.metrics_history = defaultdict(lambda: deque(maxlen=1000))  # Keep last 1000 metrics per type
        self.active_alerts = {}
        self.performance_baselines = {}
        self.optimization_recommendations = []
        
        # Monitoring configuration
        self.monitoring_interval = self.config.get("monitoring_interval", 30)  # seconds
        self.alert_thresholds = self.config.get("alert_thresholds", {
            "cpu_usage": 80.0,
            "memory_usage": 85.0,
            "disk_usage": 90.0,
            "response_time": 5.0,
            "error_rate": 5.0,
            "cache_hit_rate": 70.0
        })
        
        # Performance tracking
        self.performance_stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0.0,
            "peak_memory_usage": 0.0,
            "peak_cpu_usage": 0.0,
            "cache_hit_rate": 0.0,
            "database_query_time": 0.0
        }
        
        # Monitoring tasks
        self.monitoring_tasks = []
        self.is_monitoring = False
        
    async def start_monitoring(self):
        """Start comprehensive performance monitoring"""
        try:
            if self.is_monitoring:
                logger.warning("Monitoring is already running")
                return
            
            self.is_monitoring = True
            logger.info("Starting performance monitoring system...")
            
            # Start monitoring tasks
            self.monitoring_tasks = [
                asyncio.create_task(self._monitor_system_metrics()),
                asyncio.create_task(self._monitor_application_metrics()),
                asyncio.create_task(self._monitor_database_metrics()),
                asyncio.create_task(self._monitor_memory_metrics()),
                asyncio.create_task(self._monitor_cache_metrics()),
                asyncio.create_task(self._monitor_agent_metrics()),
                asyncio.create_task(self._analyze_performance_trends()),
                asyncio.create_task(self._generate_optimization_recommendations())
            ]
            
            logger.info("Performance monitoring system started successfully")
            
        except Exception as e:
            logger.error(f"Error starting performance monitoring: {e}")
            raise
    
    async def stop_monitoring(self):
        """Stop performance monitoring"""
        try:
            self.is_monitoring = False
            
            # Cancel all monitoring tasks
            for task in self.monitoring_tasks:
                task.cancel()
            
            # Wait for tasks to complete
            await asyncio.gather(*self.monitoring_tasks, return_exceptions=True)
            
            self.monitoring_tasks = []
            logger.info("Performance monitoring system stopped")
            
        except Exception as e:
            logger.error(f"Error stopping performance monitoring: {e}")
    
    async def _monitor_system_metrics(self):
        """Monitor system-level performance metrics"""
        while self.is_monitoring:
            try:
                # CPU usage
                cpu_percent = psutil.cpu_percent(interval=1)
                await self._record_metric("cpu_usage", cpu_percent, MetricType.SYSTEM, "%")
                
                # Memory usage
                memory = psutil.virtual_memory()
                await self._record_metric("memory_usage", memory.percent, MetricType.SYSTEM, "%")
                await self._record_metric("memory_available", memory.available, MetricType.SYSTEM, "bytes")
                
                # Disk usage
                disk = psutil.disk_usage('/')
                await self._record_metric("disk_usage", disk.percent, MetricType.SYSTEM, "%")
                await self._record_metric("disk_free", disk.free, MetricType.SYSTEM, "bytes")
                
                # Network I/O
                network = psutil.net_io_counters()
                await self._record_metric("network_bytes_sent", network.bytes_sent, MetricType.NETWORK, "bytes")
                await self._record_metric("network_bytes_recv", network.bytes_recv, MetricType.NETWORK, "bytes")
                
                # Update performance stats
                self.performance_stats["peak_cpu_usage"] = max(
                    self.performance_stats["peak_cpu_usage"], cpu_percent
                )
                self.performance_stats["peak_memory_usage"] = max(
                    self.performance_stats["peak_memory_usage"], memory.percent
                )
                
                await asyncio.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Error monitoring system metrics: {e}")
                await asyncio.sleep(self.monitoring_interval)
    
    async def _monitor_application_metrics(self):
        """Monitor application-level performance metrics"""
        while self.is_monitoring:
            try:
                # Request metrics
                total_requests = self.performance_stats["total_requests"]
                successful_requests = self.performance_stats["successful_requests"]
                failed_requests = self.performance_stats["failed_requests"]
                
                if total_requests > 0:
                    success_rate = (successful_requests / total_requests) * 100
                    error_rate = (failed_requests / total_requests) * 100
                    
                    await self._record_metric("success_rate", success_rate, MetricType.APPLICATION, "%")
                    await self._record_metric("error_rate", error_rate, MetricType.APPLICATION, "%")
                
                # Response time
                avg_response_time = self.performance_stats["average_response_time"]
                await self._record_metric("response_time", avg_response_time, MetricType.APPLICATION, "seconds")
                
                # Active connections (if available)
                try:
                    connections = len(psutil.net_connections())
                    await self._record_metric("active_connections", connections, MetricType.APPLICATION, "count")
                except Exception:
                    pass
                
                await asyncio.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Error monitoring application metrics: {e}")
                await asyncio.sleep(self.monitoring_interval)
    
    async def _monitor_database_metrics(self):
        """Monitor database performance metrics"""
        while self.is_monitoring:
            try:
                # Database connection metrics
                start_time = time.time()
                
                with self.driver.session() as session:
                    # Test database connectivity and performance
                    result = session.run("RETURN 1 as test")
                    result.single()
                
                db_response_time = time.time() - start_time
                await self._record_metric("database_response_time", db_response_time, MetricType.DATABASE, "seconds")
                
                # Update performance stats
                self.performance_stats["database_query_time"] = db_response_time
                
                # Database-specific metrics
                try:
                    # Get database statistics
                    with self.driver.session() as session:
                        # Node count
                        node_count_result = session.run("MATCH (n) RETURN count(n) as node_count")
                        node_count = node_count_result.single()["node_count"]
                        await self._record_metric("database_nodes", node_count, MetricType.DATABASE, "count")
                        
                        # Relationship count
                        rel_count_result = session.run("MATCH ()-[r]->() RETURN count(r) as rel_count")
                        rel_count = rel_count_result.single()["rel_count"]
                        await self._record_metric("database_relationships", rel_count, MetricType.DATABASE, "count")
                        
                except Exception as e:
                    logger.warning(f"Could not retrieve database statistics: {e}")
                
                await asyncio.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Error monitoring database metrics: {e}")
                await asyncio.sleep(self.monitoring_interval)
    
    async def _monitor_memory_metrics(self):
        """Monitor memory usage and performance"""
        while self.is_monitoring:
            try:
                # Python process memory
                process = psutil.Process()
                memory_info = process.memory_info()
                
                await self._record_metric("process_memory_rss", memory_info.rss, MetricType.MEMORY, "bytes")
                await self._record_metric("process_memory_vms", memory_info.vms, MetricType.MEMORY, "bytes")
                
                # Memory usage percentage
                memory_percent = process.memory_percent()
                await self._record_metric("process_memory_percent", memory_percent, MetricType.MEMORY, "%")
                
                # Memory fragmentation (if available)
                try:
                    memory_maps = process.memory_maps()
                    await self._record_metric("memory_maps_count", len(memory_maps), MetricType.MEMORY, "count")
                except Exception:
                    pass
                
                await asyncio.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Error monitoring memory metrics: {e}")
                await asyncio.sleep(self.monitoring_interval)
    
    async def _monitor_cache_metrics(self):
        """Monitor cache performance metrics"""
        while self.is_monitoring:
            try:
                if self.redis_client:
                    # Redis info
                    redis_info = await self.redis_client.info()
                    
                    # Memory usage
                    used_memory = redis_info.get("used_memory", 0)
                    max_memory = redis_info.get("maxmemory", 0)
                    
                    if max_memory > 0:
                        memory_usage_percent = (used_memory / max_memory) * 100
                        await self._record_metric("redis_memory_usage", memory_usage_percent, MetricType.CACHE, "%")
                    
                    # Hit rate
                    keyspace_hits = redis_info.get("keyspace_hits", 0)
                    keyspace_misses = redis_info.get("keyspace_misses", 0)
                    
                    if keyspace_hits + keyspace_misses > 0:
                        hit_rate = (keyspace_hits / (keyspace_hits + keyspace_misses)) * 100
                        await self._record_metric("cache_hit_rate", hit_rate, MetricType.CACHE, "%")
                        self.performance_stats["cache_hit_rate"] = hit_rate
                    
                    # Connected clients
                    connected_clients = redis_info.get("connected_clients", 0)
                    await self._record_metric("redis_connected_clients", connected_clients, MetricType.CACHE, "count")
                    
                    # Operations per second
                    ops_per_sec = redis_info.get("instantaneous_ops_per_sec", 0)
                    await self._record_metric("redis_ops_per_sec", ops_per_sec, MetricType.CACHE, "ops/sec")
                
                await asyncio.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Error monitoring cache metrics: {e}")
                await asyncio.sleep(self.monitoring_interval)
    
    async def _monitor_agent_metrics(self):
        """Monitor agent-specific performance metrics"""
        while self.is_monitoring:
            try:
                # Agent performance metrics from database
                with self.driver.session() as session:
                    # Active agents
                    active_agents_query = """
                    MATCH (a:Agent)
                    WHERE a.status = 'active'
                    RETURN count(a) as active_agents
                    """
                    result = session.run(active_agents_query)
                    active_agents = result.single()["active_agents"] if result.single() else 0
                    await self._record_metric("active_agents", active_agents, MetricType.AGENT, "count")
                    
                    # Agent memory usage
                    agent_memory_query = """
                    MATCH (m:AgentMemory)
                    RETURN count(m) as total_memories, 
                           avg(m.retrieval_strength) as avg_retrieval_strength
                    """
                    result = session.run(agent_memory_query)
                    if result.single():
                        total_memories = result.single()["total_memories"]
                        avg_retrieval_strength = result.single()["avg_retrieval_strength"] or 0
                        
                        await self._record_metric("agent_total_memories", total_memories, MetricType.AGENT, "count")
                        await self._record_metric("agent_avg_retrieval_strength", avg_retrieval_strength, MetricType.AGENT, "score")
                    
                    # Cross-agent learning events
                    cross_learning_query = """
                    MATCH (l:CrossAgentLearning)
                    WHERE l.created_at > datetime() - duration('P1D')
                    RETURN count(l) as daily_learning_events
                    """
                    result = session.run(cross_learning_query)
                    daily_learning = result.single()["daily_learning_events"] if result.single() else 0
                    await self._record_metric("daily_cross_agent_learning", daily_learning, MetricType.AGENT, "count")
                
                await asyncio.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Error monitoring agent metrics: {e}")
                await asyncio.sleep(self.monitoring_interval)
    
    async def _analyze_performance_trends(self):
        """Analyze performance trends and patterns"""
        while self.is_monitoring:
            try:
                # Analyze trends for each metric type
                for metric_type in MetricType:
                    await self._analyze_metric_trends(metric_type)
                
                # Generate performance insights
                insights = await self._generate_performance_insights()
                
                # Store insights
                await self._store_performance_insights(insights)
                
                await asyncio.sleep(self.monitoring_interval * 2)  # Run less frequently
                
            except Exception as e:
                logger.error(f"Error analyzing performance trends: {e}")
                await asyncio.sleep(self.monitoring_interval * 2)
    
    async def _generate_optimization_recommendations(self):
        """Generate optimization recommendations based on performance data"""
        while self.is_monitoring:
            try:
                recommendations = []
                
                # Analyze current performance
                current_metrics = await self._get_current_metrics()
                
                # CPU optimization recommendations
                if current_metrics.get("cpu_usage", 0) > 70:
                    recommendations.append({
                        "type": "cpu_optimization",
                        "priority": "high",
                        "message": "High CPU usage detected. Consider optimizing algorithms or scaling horizontally.",
                        "suggestions": [
                            "Implement async processing for I/O operations",
                            "Use connection pooling for database operations",
                            "Consider horizontal scaling"
                        ]
                    })
                
                # Memory optimization recommendations
                if current_metrics.get("memory_usage", 0) > 80:
                    recommendations.append({
                        "type": "memory_optimization",
                        "priority": "high",
                        "message": "High memory usage detected. Consider memory optimization strategies.",
                        "suggestions": [
                            "Implement memory compression for large data structures",
                            "Use memory-mapped files for large datasets",
                            "Implement garbage collection optimization"
                        ]
                    })
                
                # Cache optimization recommendations
                if current_metrics.get("cache_hit_rate", 0) < 70:
                    recommendations.append({
                        "type": "cache_optimization",
                        "priority": "medium",
                        "message": "Low cache hit rate detected. Consider cache optimization.",
                        "suggestions": [
                            "Review cache key strategies",
                            "Implement cache warming",
                            "Consider cache size optimization"
                        ]
                    })
                
                # Database optimization recommendations
                if current_metrics.get("database_response_time", 0) > 2.0:
                    recommendations.append({
                        "type": "database_optimization",
                        "priority": "medium",
                        "message": "Slow database response times detected.",
                        "suggestions": [
                            "Optimize database queries",
                            "Add database indexes",
                            "Consider query caching"
                        ]
                    })
                
                # Store recommendations
                self.optimization_recommendations = recommendations
                await self._store_optimization_recommendations(recommendations)
                
                await asyncio.sleep(self.monitoring_interval * 4)  # Run less frequently
                
            except Exception as e:
                logger.error(f"Error generating optimization recommendations: {e}")
                await asyncio.sleep(self.monitoring_interval * 4)
    
    async def _record_metric(self, name: str, value: float, metric_type: MetricType, unit: str, tags: Dict[str, str] = None):
        """Record a performance metric"""
        try:
            metric = PerformanceMetric(
                name=name,
                value=value,
                metric_type=metric_type,
                timestamp=datetime.now(),
                unit=unit,
                tags=tags or {}
            )
            
            # Check for alerts
            await self._check_metric_alerts(metric)
            
            # Store metric
            self.metrics_history[metric_type].append(metric)
            
            # Store in database
            await self._store_metric_in_db(metric)
            
        except Exception as e:
            logger.error(f"Error recording metric {name}: {e}")
    
    async def _check_metric_alerts(self, metric: PerformanceMetric):
        """Check if metric triggers any alerts"""
        try:
            threshold = self.alert_thresholds.get(metric.name)
            if not threshold:
                return
            
            alert_level = None
            if metric.value >= threshold * 1.5:
                alert_level = AlertLevel.EMERGENCY
            elif metric.value >= threshold * 1.2:
                alert_level = AlertLevel.CRITICAL
            elif metric.value >= threshold:
                alert_level = AlertLevel.WARNING
            
            if alert_level:
                alert_id = f"{metric.name}_{metric.timestamp.timestamp()}"
                
                alert = PerformanceAlert(
                    id=alert_id,
                    metric_name=metric.name,
                    current_value=metric.value,
                    threshold_value=threshold,
                    alert_level=alert_level,
                    message=f"{metric.name} exceeded threshold: {metric.value:.2f} > {threshold:.2f}",
                    timestamp=metric.timestamp
                )
                
                self.active_alerts[alert_id] = alert
                await self._store_alert_in_db(alert)
                
                logger.warning(f"Performance alert: {alert.message}")
            
        except Exception as e:
            logger.error(f"Error checking metric alerts: {e}")
    
    async def _analyze_metric_trends(self, metric_type: MetricType):
        """Analyze trends for a specific metric type"""
        try:
            metrics = list(self.metrics_history[metric_type])
            if len(metrics) < 10:  # Need enough data points
                return
            
            # Calculate trend
            values = [m.value for m in metrics[-20:]]  # Last 20 data points
            trend = self._calculate_trend(values)
            
            # Store trend analysis
            await self._store_trend_analysis(metric_type, trend)
            
        except Exception as e:
            logger.error(f"Error analyzing trends for {metric_type}: {e}")
    
    def _calculate_trend(self, values: List[float]) -> Dict[str, Any]:
        """Calculate trend from a series of values"""
        try:
            if len(values) < 2:
                return {"trend": "insufficient_data"}
            
            # Simple linear regression
            x = np.arange(len(values))
            y = np.array(values)
            
            # Calculate slope
            slope = np.polyfit(x, y, 1)[0]
            
            # Determine trend direction
            if slope > 0.1:
                trend_direction = "increasing"
            elif slope < -0.1:
                trend_direction = "decreasing"
            else:
                trend_direction = "stable"
            
            # Calculate volatility
            volatility = np.std(values)
            
            return {
                "trend": trend_direction,
                "slope": slope,
                "volatility": volatility,
                "min_value": min(values),
                "max_value": max(values),
                "avg_value": np.mean(values)
            }
            
        except Exception as e:
            logger.error(f"Error calculating trend: {e}")
            return {"trend": "error"}
    
    async def _generate_performance_insights(self) -> List[Dict[str, Any]]:
        """Generate performance insights based on collected data"""
        try:
            insights = []
            
            # Get current metrics
            current_metrics = await self._get_current_metrics()
            
            # System health insight
            cpu_usage = current_metrics.get("cpu_usage", 0)
            memory_usage = current_metrics.get("memory_usage", 0)
            
            if cpu_usage < 50 and memory_usage < 60:
                insights.append({
                    "type": "system_health",
                    "status": "excellent",
                    "message": "System is running optimally with low resource usage"
                })
            elif cpu_usage < 70 and memory_usage < 80:
                insights.append({
                    "type": "system_health",
                    "status": "good",
                    "message": "System is running well with moderate resource usage"
                })
            else:
                insights.append({
                    "type": "system_health",
                    "status": "needs_attention",
                    "message": "System resource usage is high and may need optimization"
                })
            
            # Performance efficiency insight
            cache_hit_rate = current_metrics.get("cache_hit_rate", 0)
            if cache_hit_rate > 80:
                insights.append({
                    "type": "cache_efficiency",
                    "status": "excellent",
                    "message": f"Cache is performing excellently with {cache_hit_rate:.1f}% hit rate"
                })
            elif cache_hit_rate > 60:
                insights.append({
                    "type": "cache_efficiency",
                    "status": "good",
                    "message": f"Cache is performing well with {cache_hit_rate:.1f}% hit rate"
                })
            else:
                insights.append({
                    "type": "cache_efficiency",
                    "status": "needs_improvement",
                    "message": f"Cache hit rate is low at {cache_hit_rate:.1f}%, consider optimization"
                })
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating performance insights: {e}")
            return []
    
    async def _get_current_metrics(self) -> Dict[str, float]:
        """Get current performance metrics"""
        try:
            current_metrics = {}
            
            for metric_type in MetricType:
                metrics = list(self.metrics_history[metric_type])
                if metrics:
                    latest_metric = metrics[-1]
                    current_metrics[latest_metric.name] = latest_metric.value
            
            return current_metrics
            
        except Exception as e:
            logger.error(f"Error getting current metrics: {e}")
            return {}
    
    async def _store_metric_in_db(self, metric: PerformanceMetric):
        """Store metric in Neo4j database"""
        try:
            with self.driver.session() as session:
                query = """
                CREATE (m:PerformanceMetric {
                    name: $name,
                    value: $value,
                    metric_type: $metric_type,
                    timestamp: $timestamp,
                    unit: $unit,
                    tags: $tags,
                    alert_level: $alert_level
                })
                """
                
                await session.run(query, {
                    "name": metric.name,
                    "value": metric.value,
                    "metric_type": metric.metric_type.value,
                    "timestamp": metric.timestamp.isoformat(),
                    "unit": metric.unit,
                    "tags": json.dumps(metric.tags),
                    "alert_level": metric.alert_level.value if metric.alert_level else None
                })
            
        except Exception as e:
            logger.error(f"Error storing metric in database: {e}")
    
    async def _store_alert_in_db(self, alert: PerformanceAlert):
        """Store alert in Neo4j database"""
        try:
            with self.driver.session() as session:
                query = """
                CREATE (a:PerformanceAlert {
                    id: $id,
                    metric_name: $metric_name,
                    current_value: $current_value,
                    threshold_value: $threshold_value,
                    alert_level: $alert_level,
                    message: $message,
                    timestamp: $timestamp,
                    resolved: $resolved
                })
                """
                
                await session.run(query, {
                    "id": alert.id,
                    "metric_name": alert.metric_name,
                    "current_value": alert.current_value,
                    "threshold_value": alert.threshold_value,
                    "alert_level": alert.alert_level.value,
                    "message": alert.message,
                    "timestamp": alert.timestamp.isoformat(),
                    "resolved": alert.resolved
                })
            
        except Exception as e:
            logger.error(f"Error storing alert in database: {e}")
    
    async def _store_trend_analysis(self, metric_type: MetricType, trend: Dict[str, Any]):
        """Store trend analysis in database"""
        try:
            with self.driver.session() as session:
                query = """
                CREATE (t:TrendAnalysis {
                    metric_type: $metric_type,
                    trend: $trend,
                    slope: $slope,
                    volatility: $volatility,
                    min_value: $min_value,
                    max_value: $max_value,
                    avg_value: $avg_value,
                    timestamp: $timestamp
                })
                """
                
                await session.run(query, {
                    "metric_type": metric_type.value,
                    "trend": trend.get("trend", "unknown"),
                    "slope": trend.get("slope", 0),
                    "volatility": trend.get("volatility", 0),
                    "min_value": trend.get("min_value", 0),
                    "max_value": trend.get("max_value", 0),
                    "avg_value": trend.get("avg_value", 0),
                    "timestamp": datetime.now().isoformat()
                })
            
        except Exception as e:
            logger.error(f"Error storing trend analysis: {e}")
    
    async def _store_performance_insights(self, insights: List[Dict[str, Any]]):
        """Store performance insights in database"""
        try:
            with self.driver.session() as session:
                for insight in insights:
                    query = """
                    CREATE (i:PerformanceInsight {
                        type: $type,
                        status: $status,
                        message: $message,
                        timestamp: $timestamp
                    })
                    """
                    
                    await session.run(query, {
                        "type": insight["type"],
                        "status": insight["status"],
                        "message": insight["message"],
                        "timestamp": datetime.now().isoformat()
                    })
            
        except Exception as e:
            logger.error(f"Error storing performance insights: {e}")
    
    async def _store_optimization_recommendations(self, recommendations: List[Dict[str, Any]]):
        """Store optimization recommendations in database"""
        try:
            with self.driver.session() as session:
                # Clear old recommendations
                await session.run("MATCH (r:OptimizationRecommendation) DELETE r")
                
                for rec in recommendations:
                    query = """
                    CREATE (r:OptimizationRecommendation {
                        type: $type,
                        priority: $priority,
                        message: $message,
                        suggestions: $suggestions,
                        timestamp: $timestamp
                    })
                    """
                    
                    await session.run(query, {
                        "type": rec["type"],
                        "priority": rec["priority"],
                        "message": rec["message"],
                        "suggestions": json.dumps(rec["suggestions"]),
                        "timestamp": datetime.now().isoformat()
                    })
            
        except Exception as e:
            logger.error(f"Error storing optimization recommendations: {e}")
    
    def record_request(self, success: bool, response_time: float):
        """Record a request for performance tracking"""
        try:
            self.performance_stats["total_requests"] += 1
            
            if success:
                self.performance_stats["successful_requests"] += 1
            else:
                self.performance_stats["failed_requests"] += 1
            
            # Update average response time
            total_requests = self.performance_stats["total_requests"]
            current_avg = self.performance_stats["average_response_time"]
            
            self.performance_stats["average_response_time"] = (
                (current_avg * (total_requests - 1) + response_time) / total_requests
            )
            
        except Exception as e:
            logger.error(f"Error recording request: {e}")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        try:
            current_metrics = {}
            for metric_type in MetricType:
                metrics = list(self.metrics_history[metric_type])
                if metrics:
                    latest_metric = metrics[-1]
                    current_metrics[latest_metric.name] = {
                        "value": latest_metric.value,
                        "unit": latest_metric.unit,
                        "timestamp": latest_metric.timestamp.isoformat()
                    }
            
            return {
                "performance_stats": self.performance_stats,
                "current_metrics": current_metrics,
                "active_alerts": len(self.active_alerts),
                "optimization_recommendations": len(self.optimization_recommendations),
                "monitoring_status": "active" if self.is_monitoring else "inactive",
                "total_metrics_collected": sum(len(metrics) for metrics in self.metrics_history.values())
            }
            
        except Exception as e:
            logger.error(f"Error getting performance summary: {e}")
            return {"error": str(e)}
    
    def get_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """Get current optimization recommendations"""
        return self.optimization_recommendations.copy()
    
    def get_active_alerts(self) -> List[PerformanceAlert]:
        """Get active performance alerts"""
        return list(self.active_alerts.values())
    
    async def resolve_alert(self, alert_id: str):
        """Resolve a performance alert"""
        try:
            if alert_id in self.active_alerts:
                alert = self.active_alerts[alert_id]
                alert.resolved = True
                alert.resolution_time = datetime.now()
                
                # Update in database
                with self.driver.session() as session:
                    query = """
                    MATCH (a:PerformanceAlert {id: $id})
                    SET a.resolved = true, a.resolution_time = $resolution_time
                    """
                    await session.run(query, {
                        "id": alert_id,
                        "resolution_time": alert.resolution_time.isoformat()
                    })
                
                # Remove from active alerts
                del self.active_alerts[alert_id]
                
                logger.info(f"Alert {alert_id} resolved")
            
        except Exception as e:
            logger.error(f"Error resolving alert {alert_id}: {e}")


# Performance monitoring decorator
def monitor_performance(metric_name: str, metric_type: MetricType = MetricType.APPLICATION):
    """Decorator to monitor function performance"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            success = True
            
            try:
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
                return result
            except Exception as e:
                success = False
                raise
            finally:
                response_time = time.time() - start_time
                
                # Record performance metric
                # Note: In a real implementation, you'd inject the monitoring system
                # For now, this is a placeholder
                logger.info(f"Performance metric: {metric_name} = {response_time:.3f}s (success: {success})")
        
        return wrapper
    return decorator
