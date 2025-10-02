"""
Monitoring and Observability System for Mainza AI
Comprehensive monitoring, logging, and metrics collection
"""
import asyncio
import logging
import time
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import psutil
import threading
from collections import defaultdict, deque
import traceback

logger = logging.getLogger(__name__)

@dataclass
class SystemMetrics:
    """System metrics data class"""
    timestamp: datetime
    cpu_percent: float
    memory_mb: float
    memory_percent: float
    disk_usage_percent: float
    network_io_bytes: int
    active_connections: int
    load_average: float

@dataclass
class ApplicationMetrics:
    """Application metrics data class"""
    timestamp: datetime
    request_count: int
    response_time_ms: float
    error_count: int
    active_sessions: int
    consciousness_level: float
    quantum_operations: int
    memory_operations: int

@dataclass
class Alert:
    """Alert data class"""
    timestamp: datetime
    severity: str  # "low", "medium", "high", "critical"
    category: str  # "performance", "security", "system", "application"
    message: str
    details: Dict[str, Any]
    resolved: bool = False

class MonitoringSystem:
    """Comprehensive monitoring and observability system"""
    
    def __init__(self):
        self.system_metrics: deque = deque(maxlen=1000)
        self.application_metrics: deque = deque(maxlen=1000)
        self.alerts: List[Alert] = []
        self.logs: deque = deque(maxlen=10000)
        self.monitoring_enabled = True
        self.alert_thresholds = {
            "cpu_percent": 80.0,
            "memory_percent": 85.0,
            "response_time_ms": 2000.0,
            "error_rate": 0.05,  # 5%
            "disk_usage_percent": 90.0
        }
        self._monitoring_task = None
        self._metrics_lock = threading.Lock()
        
    async def start_monitoring(self):
        """Start monitoring system"""
        if self.monitoring_enabled:
            logger.info("🔍 Starting monitoring system")
            self._monitoring_task = asyncio.create_task(self._monitor_loop())
            await self._initialize_monitoring()
    
    async def stop_monitoring(self):
        """Stop monitoring system"""
        if self._monitoring_task:
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                pass
        logger.info("🛑 Monitoring system stopped")
    
    async def _monitor_loop(self):
        """Main monitoring loop"""
        while True:
            try:
                await self._collect_system_metrics()
                await self._collect_application_metrics()
                await self._check_alerts()
                await self._process_logs()
                await asyncio.sleep(30)  # Monitor every 30 seconds
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                await asyncio.sleep(5)
    
    async def _collect_system_metrics(self):
        """Collect system metrics"""
        try:
            with self._metrics_lock:
                metrics = SystemMetrics(
                    timestamp=datetime.now(),
                    cpu_percent=psutil.cpu_percent(interval=1),
                    memory_mb=psutil.virtual_memory().used / 1024 / 1024,
                    memory_percent=psutil.virtual_memory().percent,
                    disk_usage_percent=psutil.disk_usage('/').percent,
                    network_io_bytes=sum(psutil.net_io_counters()._asdict().values()),
                    active_connections=len(psutil.Process().connections()),
                    load_average=psutil.getloadavg()[0] if hasattr(psutil, 'getloadavg') else 0.0
                )
                
                self.system_metrics.append(metrics)
                
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
    
    async def _collect_application_metrics(self):
        """Collect application metrics"""
        try:
            with self._metrics_lock:
                metrics = ApplicationMetrics(
                    timestamp=datetime.now(),
                    request_count=0,  # Will be updated by middleware
                    response_time_ms=0.0,  # Will be updated by middleware
                    error_count=0,  # Will be updated by error handlers
                    active_sessions=0,  # Will be updated by session manager
                    consciousness_level=0.7,  # Will be updated by consciousness system
                    quantum_operations=0,  # Will be updated by quantum system
                    memory_operations=0  # Will be updated by memory system
                )
                
                self.application_metrics.append(metrics)
                
        except Exception as e:
            logger.error(f"Error collecting application metrics: {e}")
    
    async def _check_alerts(self):
        """Check for alert conditions"""
        if not self.system_metrics:
            return
        
        latest_system = self.system_metrics[-1]
        latest_app = self.application_metrics[-1] if self.application_metrics else None
        
        # Check CPU usage
        if latest_system.cpu_percent > self.alert_thresholds["cpu_percent"]:
            await self._create_alert("high", "performance", 
                f"High CPU usage: {latest_system.cpu_percent:.1f}%",
                {"cpu_percent": latest_system.cpu_percent})
        
        # Check memory usage
        if latest_system.memory_percent > self.alert_thresholds["memory_percent"]:
            await self._create_alert("high", "performance",
                f"High memory usage: {latest_system.memory_percent:.1f}%",
                {"memory_percent": latest_system.memory_percent})
        
        # Check disk usage
        if latest_system.disk_usage_percent > self.alert_thresholds["disk_usage_percent"]:
            await self._create_alert("critical", "system",
                f"High disk usage: {latest_system.disk_usage_percent:.1f}%",
                {"disk_usage_percent": latest_system.disk_usage_percent})
        
        # Check response times
        if latest_app and latest_app.response_time_ms > self.alert_thresholds["response_time_ms"]:
            await self._create_alert("medium", "performance",
                f"Slow response time: {latest_app.response_time_ms:.1f}ms",
                {"response_time_ms": latest_app.response_time_ms})
        
        # Check error rate
        if latest_app and latest_app.request_count > 0:
            error_rate = latest_app.error_count / latest_app.request_count
            if error_rate > self.alert_thresholds["error_rate"]:
                await self._create_alert("high", "application",
                    f"High error rate: {error_rate:.2%}",
                    {"error_rate": error_rate, "error_count": latest_app.error_count})
    
    async def _create_alert(self, severity: str, category: str, message: str, details: Dict[str, Any]):
        """Create a new alert"""
        alert = Alert(
            timestamp=datetime.now(),
            severity=severity,
            category=category,
            message=message,
            details=details
        )
        
        self.alerts.append(alert)
        
        # Log alert
        logger.warning(f"ALERT [{severity.upper()}] {category}: {message}")
        
        # Keep only last 1000 alerts
        if len(self.alerts) > 1000:
            self.alerts = self.alerts[-1000:]
    
    async def _process_logs(self):
        """Process and analyze logs"""
        # This would implement log analysis and correlation
        pass
    
    async def _initialize_monitoring(self):
        """Initialize monitoring components"""
        try:
            # Set up logging
            await self._setup_logging()
            
            # Set up metrics collection
            await self._setup_metrics_collection()
            
            # Set up alerting
            await self._setup_alerting()
            
            logger.info("✅ Monitoring system initialized")
        except Exception as e:
            logger.error(f"Error initializing monitoring: {e}")
    
    async def _setup_logging(self):
        """Set up structured logging"""
        # Configure structured logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('logs/mainza_monitoring.log')
            ]
        )
    
    async def _setup_metrics_collection(self):
        """Set up metrics collection"""
        # This would set up Prometheus metrics or other monitoring systems
        pass
    
    async def _setup_alerting(self):
        """Set up alerting system"""
        # This would set up alerting channels (email, Slack, etc.)
        pass
    
    def log_event(self, level: str, message: str, details: Dict[str, Any] = None):
        """Log an event"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "details": details or {}
        }
        
        with self._metrics_lock:
            self.logs.append(log_entry)
        
        # Also log to standard logger
        getattr(logger, level.lower(), logger.info)(f"{message} - {details}")
    
    def update_application_metrics(self, **kwargs):
        """Update application metrics"""
        if not self.application_metrics:
            return
        
        with self._metrics_lock:
            latest = self.application_metrics[-1]
            for key, value in kwargs.items():
                if hasattr(latest, key):
                    setattr(latest, key, value)
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get system health status"""
        if not self.system_metrics:
            return {"status": "unknown", "message": "No metrics available"}
        
        latest = self.system_metrics[-1]
        
        # Determine health status
        health_issues = []
        
        if latest.cpu_percent > 90:
            health_issues.append("Critical CPU usage")
        elif latest.cpu_percent > 80:
            health_issues.append("High CPU usage")
        
        if latest.memory_percent > 95:
            health_issues.append("Critical memory usage")
        elif latest.memory_percent > 85:
            health_issues.append("High memory usage")
        
        if latest.disk_usage_percent > 95:
            health_issues.append("Critical disk usage")
        elif latest.disk_usage_percent > 90:
            health_issues.append("High disk usage")
        
        if health_issues:
            status = "unhealthy"
            message = "; ".join(health_issues)
        else:
            status = "healthy"
            message = "All systems operational"
        
        return {
            "status": status,
            "message": message,
            "timestamp": latest.timestamp.isoformat(),
            "metrics": asdict(latest),
            "active_alerts": len([a for a in self.alerts if not a.resolved])
        }
    
    def get_metrics_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get metrics summary for specified hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # Filter metrics by time
        system_metrics = [m for m in self.system_metrics if m.timestamp > cutoff_time]
        app_metrics = [m for m in self.application_metrics if m.timestamp > cutoff_time]
        
        if not system_metrics:
            return {"error": "No metrics available for the specified time period"}
        
        # Calculate averages
        avg_cpu = sum(m.cpu_percent for m in system_metrics) / len(system_metrics)
        avg_memory = sum(m.memory_percent for m in system_metrics) / len(system_metrics)
        avg_response_time = sum(m.response_time_ms for m in app_metrics) / len(app_metrics) if app_metrics else 0
        
        return {
            "time_period_hours": hours,
            "metrics_count": len(system_metrics),
            "averages": {
                "cpu_percent": round(avg_cpu, 2),
                "memory_percent": round(avg_memory, 2),
                "response_time_ms": round(avg_response_time, 2)
            },
            "current": {
                "cpu_percent": system_metrics[-1].cpu_percent,
                "memory_percent": system_metrics[-1].memory_percent,
                "response_time_ms": app_metrics[-1].response_time_ms if app_metrics else 0
            },
            "alerts": len([a for a in self.alerts if a.timestamp > cutoff_time and not a.resolved])
        }
    
    def get_recent_alerts(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent alerts"""
        recent_alerts = sorted(self.alerts, key=lambda x: x.timestamp, reverse=True)[:limit]
        return [asdict(alert) for alert in recent_alerts]
    
    def resolve_alert(self, alert_id: int):
        """Resolve an alert"""
        if 0 <= alert_id < len(self.alerts):
            self.alerts[alert_id].resolved = True
            logger.info(f"Alert {alert_id} resolved")
    
    def get_logs(self, level: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent logs"""
        logs = list(self.logs)
        
        if level:
            logs = [log for log in logs if log["level"] == level]
        
        return logs[-limit:]

# Global monitoring system instance
monitoring_system = MonitoringSystem()

# Monitoring decorators
def monitor_performance(func):
    """Decorator to monitor function performance"""
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            execution_time = (time.time() - start_time) * 1000
            monitoring_system.update_application_metrics(response_time_ms=execution_time)
    return wrapper

def log_errors(func):
    """Decorator to log errors"""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            monitoring_system.log_event("error", f"Error in {func.__name__}", {
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            monitoring_system.update_application_metrics(error_count=1)
            raise
    return wrapper

# Monitoring middleware
class MonitoringMiddleware:
    """FastAPI middleware for monitoring"""
    
    def __init__(self, app):
        self.app = app
        self.request_count = 0
        self.error_count = 0
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        start_time = time.time()
        self.request_count += 1
        
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                process_time = (time.time() - start_time) * 1000
                
                # Update metrics
                monitoring_system.update_application_metrics(
                    request_count=self.request_count,
                    response_time_ms=process_time,
                    error_count=self.error_count
                )
                
                # Add monitoring headers
                message["headers"].append([b"x-process-time", str(process_time).encode()])
                message["headers"].append([b"x-request-id", str(self.request_count).encode()])
            
            await send(message)
        
        try:
            await self.app(scope, receive, send_wrapper)
        except Exception as e:
            self.error_count += 1
            monitoring_system.log_event("error", f"Request error: {str(e)}")
            raise
