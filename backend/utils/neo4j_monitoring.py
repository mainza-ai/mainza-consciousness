"""
Neo4j Monitoring and Observability Utilities
Provides comprehensive monitoring, alerting, and performance analysis for Neo4j operations.
"""
import os
import logging
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import threading
from collections import defaultdict, deque
import statistics

logger = logging.getLogger(__name__)

class AlertLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class Alert:
    level: AlertLevel
    message: str
    metric_name: str
    current_value: float
    threshold: float
    timestamp: datetime
    resolved: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            'level': self.level.value,
            'timestamp': self.timestamp.isoformat()
        }

@dataclass
class PerformanceMetric:
    name: str
    value: float
    unit: str
    timestamp: datetime
    tags: Dict[str, str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = {}

class MetricsCollector:
    """Collects and aggregates Neo4j performance metrics."""
    
    def __init__(self, max_history_size: int = 10000):
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_history_size))
        self.alerts: List[Alert] = []
        self.alert_rules: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.Lock()
        
        # Default alert thresholds
        self.setup_default_alert_rules()
    
    def setup_default_alert_rules(self):
        """Setup default alerting rules for common metrics."""
        self.alert_rules = {
            "query_execution_time": {
                "warning_threshold": 1.0,  # 1 second
                "error_threshold": 5.0,    # 5 seconds
                "critical_threshold": 10.0  # 10 seconds
            },
            "connection_pool_usage": {
                "warning_threshold": 0.7,   # 70%
                "error_threshold": 0.85,    # 85%
                "critical_threshold": 0.95  # 95%
            },
            "failed_query_rate": {
                "warning_threshold": 0.05,  # 5%
                "error_threshold": 0.1,     # 10%
                "critical_threshold": 0.2   # 20%
            },
            "memory_usage": {
                "warning_threshold": 0.8,   # 80%
                "error_threshold": 0.9,     # 90%
                "critical_threshold": 0.95  # 95%
            }
        }
    
    def record_metric(self, name: str, value: float, unit: str = "", tags: Dict[str, str] = None):
        """Record a performance metric."""
        metric = PerformanceMetric(
            name=name,
            value=value,
            unit=unit,
            timestamp=datetime.now(),
            tags=tags or {}
        )
        
        with self.lock:
            self.metrics[name].append(metric)
            self._check_alerts(name, value)
    
    def _check_alerts(self, metric_name: str, value: float):
        """Check if metric value triggers any alerts."""
        if metric_name not in self.alert_rules:
            return
        
        rules = self.alert_rules[metric_name]
        alert_level = None
        threshold = 0
        
        if value >= rules.get("critical_threshold", float('inf')):
            alert_level = AlertLevel.CRITICAL
            threshold = rules["critical_threshold"]
        elif value >= rules.get("error_threshold", float('inf')):
            alert_level = AlertLevel.ERROR
            threshold = rules["error_threshold"]
        elif value >= rules.get("warning_threshold", float('inf')):
            alert_level = AlertLevel.WARNING
            threshold = rules["warning_threshold"]
        
        if alert_level:
            alert = Alert(
                level=alert_level,
                message=f"{metric_name} exceeded threshold: {value} >= {threshold}",
                metric_name=metric_name,
                current_value=value,
                threshold=threshold,
                timestamp=datetime.now()
            )
            
            self.alerts.append(alert)
            logger.log(
                logging.CRITICAL if alert_level == AlertLevel.CRITICAL else
                logging.ERROR if alert_level == AlertLevel.ERROR else
                logging.WARNING,
                alert.message
            )
    
    def get_metric_summary(self, metric_name: str, hours_back: int = 1) -> Dict[str, Any]:
        """Get statistical summary of a metric over time period."""
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        with self.lock:
            if metric_name not in self.metrics:
                return {"error": f"Metric {metric_name} not found"}
            
            recent_metrics = [
                m for m in self.metrics[metric_name]
                if m.timestamp >= cutoff_time
            ]
            
            if not recent_metrics:
                return {"message": "No recent data available"}
            
            values = [m.value for m in recent_metrics]
            
            return {
                "metric_name": metric_name,
                "time_period_hours": hours_back,
                "sample_count": len(values),
                "min": min(values),
                "max": max(values),
                "mean": statistics.mean(values),
                "median": statistics.median(values),
                "std_dev": statistics.stdev(values) if len(values) > 1 else 0,
                "p95": sorted(values)[int(len(values) * 0.95)] if len(values) > 1 else values[0],
                "p99": sorted(values)[int(len(values) * 0.99)] if len(values) > 1 else values[0]
            }
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get all active (unresolved) alerts."""
        with self.lock:
            return [alert.to_dict() for alert in self.alerts if not alert.resolved]
    
    def resolve_alert(self, alert_index: int) -> bool:
        """Mark an alert as resolved."""
        with self.lock:
            if 0 <= alert_index < len(self.alerts):
                self.alerts[alert_index].resolved = True
                return True
            return False
    
    def get_metrics_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive metrics dashboard data."""
        dashboard = {
            "timestamp": datetime.now().isoformat(),
            "active_alerts": len(self.get_active_alerts()),
            "metrics_summary": {},
            "system_health": "unknown"
        }
        
        # Get summaries for key metrics
        key_metrics = ["query_execution_time", "connection_pool_usage", "failed_query_rate"]
        
        for metric in key_metrics:
            dashboard["metrics_summary"][metric] = self.get_metric_summary(metric)
        
        # Determine overall system health
        active_alerts = self.get_active_alerts()
        if not active_alerts:
            dashboard["system_health"] = "healthy"
        elif any(alert["level"] == "critical" for alert in active_alerts):
            dashboard["system_health"] = "critical"
        elif any(alert["level"] == "error" for alert in active_alerts):
            dashboard["system_health"] = "degraded"
        else:
            dashboard["system_health"] = "warning"
        
        return dashboard

class Neo4jMonitor:
    """Main monitoring class that integrates with Neo4j operations."""
    
    def __init__(self, neo4j_manager):
        self.neo4j_manager = neo4j_manager
        self.metrics_collector = MetricsCollector()
        self.monitoring_enabled = os.getenv("NEO4J_MONITORING_ENABLED", "true").lower() == "true"
        
        # Background monitoring thread
        self.monitoring_thread = None
        self.monitoring_active = False
        
        if self.monitoring_enabled:
            self.start_background_monitoring()
    
    def start_background_monitoring(self):
        """Start background monitoring thread."""
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._background_monitor, daemon=True)
        self.monitoring_thread.start()
        logger.info("Neo4j background monitoring started")
    
    def stop_background_monitoring(self):
        """Stop background monitoring thread."""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("Neo4j background monitoring stopped")
    
    def _background_monitor(self):
        """Background monitoring loop."""
        while self.monitoring_active:
            try:
                self._collect_system_metrics()
                time.sleep(60)  # Collect metrics every minute
            except Exception as e:
                logger.error(f"Background monitoring error: {e}")
                time.sleep(60)
    
    def _collect_system_metrics(self):
        """Collect system-level metrics."""
        try:
            # Database health check
            health_info = self.neo4j_manager.health_check()
            
            if health_info.get("status") == "healthy":
                self.metrics_collector.record_metric("database_health", 1.0, "boolean")
                
                # Connection time
                if "connection_time_ms" in health_info:
                    self.metrics_collector.record_metric(
                        "connection_time", 
                        health_info["connection_time_ms"], 
                        "ms"
                    )
            else:
                self.metrics_collector.record_metric("database_health", 0.0, "boolean")
            
            # Database statistics
            db_info = health_info.get("database_info", {})
            
            if "node_count" in db_info and db_info["node_count"]:
                node_count = db_info["node_count"][0].get("count", 0)
                self.metrics_collector.record_metric("total_nodes", float(node_count), "count")
            
            if "relationship_count" in db_info and db_info["relationship_count"]:
                rel_count = db_info["relationship_count"][0].get("count", 0)
                self.metrics_collector.record_metric("total_relationships", float(rel_count), "count")
            
            # Performance metrics from Neo4j manager
            perf_metrics = health_info.get("performance_metrics", {})
            
            if "success_rate" in perf_metrics:
                self.metrics_collector.record_metric("success_rate", perf_metrics["success_rate"] / 100.0, "ratio")
            
            if "avg_execution_time_ms" in perf_metrics:
                self.metrics_collector.record_metric("avg_query_time", perf_metrics["avg_execution_time_ms"], "ms")
            
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")
    
    def record_query_execution(self, query: str, execution_time: float, success: bool, 
                             record_count: int = 0, error: str = None):
        """Record query execution metrics."""
        if not self.monitoring_enabled:
            return
        
        # Record basic metrics
        self.metrics_collector.record_metric("query_execution_time", execution_time, "seconds")
        self.metrics_collector.record_metric("query_success", 1.0 if success else 0.0, "boolean")
        
        if success:
            self.metrics_collector.record_metric("query_record_count", float(record_count), "count")
        
        # Categorize query type
        query_type = self._categorize_query(query)
        self.metrics_collector.record_metric(
            "query_execution_time", 
            execution_time, 
            "seconds", 
            {"query_type": query_type}
        )
    
    def _categorize_query(self, query: str) -> str:
        """Categorize query by type for better metrics."""
        query_upper = query.upper().strip()
        
        if query_upper.startswith("MATCH"):
            return "read"
        elif query_upper.startswith(("CREATE", "MERGE")):
            return "write"
        elif query_upper.startswith("DELETE"):
            return "delete"
        elif query_upper.startswith("CALL"):
            return "procedure"
        else:
            return "other"
    
    def get_monitoring_report(self, hours_back: int = 24) -> Dict[str, Any]:
        """Generate comprehensive monitoring report."""
        report = {
            "report_timestamp": datetime.now().isoformat(),
            "monitoring_period_hours": hours_back,
            "system_overview": self.metrics_collector.get_metrics_dashboard(),
            "detailed_metrics": {},
            "alerts": {
                "active": self.metrics_collector.get_active_alerts(),
                "total_count": len(self.metrics_collector.alerts)
            },
            "recommendations": []
        }
        
        # Get detailed metrics for key areas
        key_metrics = [
            "query_execution_time", "query_success", "connection_time",
            "total_nodes", "total_relationships", "avg_query_time"
        ]
        
        for metric in key_metrics:
            summary = self.metrics_collector.get_metric_summary(metric, hours_back)
            if "error" not in summary and "message" not in summary:
                report["detailed_metrics"][metric] = summary
        
        # Generate recommendations
        report["recommendations"] = self._generate_recommendations(report)
        
        return report
    
    def _generate_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """Generate performance and health recommendations."""
        recommendations = []
        
        # Check query performance
        query_time_metrics = report["detailed_metrics"].get("query_execution_time", {})
        if query_time_metrics and query_time_metrics.get("mean", 0) > 1.0:
            recommendations.append(
                f"Average query time is {query_time_metrics['mean']:.2f}s. Consider optimizing slow queries or adding indexes."
            )
        
        # Check success rate
        success_metrics = report["detailed_metrics"].get("query_success", {})
        if success_metrics and success_metrics.get("mean", 1.0) < 0.95:
            recommendations.append(
                f"Query success rate is {success_metrics['mean']*100:.1f}%. Investigate failing queries."
            )
        
        # Check active alerts
        active_alerts = len(report["alerts"]["active"])
        if active_alerts > 0:
            recommendations.append(f"There are {active_alerts} active alerts that need attention.")
        
        # Check connection time
        conn_time_metrics = report["detailed_metrics"].get("connection_time", {})
        if conn_time_metrics and conn_time_metrics.get("mean", 0) > 1000:  # 1 second
            recommendations.append(
                f"Average connection time is {conn_time_metrics['mean']:.0f}ms. Check network connectivity."
            )
        
        if not recommendations:
            recommendations.append("System is performing well. No immediate recommendations.")
        
        return recommendations
    
    def export_metrics(self, format: str = "json", hours_back: int = 24) -> str:
        """Export metrics in specified format."""
        report = self.get_monitoring_report(hours_back)
        
        if format.lower() == "json":
            return json.dumps(report, indent=2, default=str)
        else:
            raise ValueError(f"Unsupported export format: {format}")

# Global monitoring instance (will be initialized when Neo4j manager is available)
neo4j_monitor = None

def initialize_monitoring(neo4j_manager):
    """Initialize global monitoring instance."""
    global neo4j_monitor
    neo4j_monitor = Neo4jMonitor(neo4j_manager)
    return neo4j_monitor

def get_monitor():
    """Get the global monitoring instance."""
    return neo4j_monitor