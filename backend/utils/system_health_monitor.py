"""
System Health Monitor for Privacy-First Telemetry

Monitors system health and collects essential metrics without any personal data.
Runs as a background service to collect system health telemetry data.
"""

import asyncio
import logging
import time
from datetime import datetime
from typing import Optional

from backend.utils.privacy_first_telemetry import get_telemetry

logger = logging.getLogger(__name__)

class SystemHealthMonitor:
    """
    Monitors system health and collects telemetry data.
    Privacy-first: no personal data, local processing only.
    """
    
    def __init__(self, collection_interval: int = 300):  # 5 minutes default
        """
        Initialize system health monitor.
        
        Args:
            collection_interval: Seconds between health data collection
        """
        self.collection_interval = collection_interval
        self.telemetry = get_telemetry()
        self.running = False
        self._task: Optional[asyncio.Task] = None
        
        logger.info(f"System health monitor initialized with {collection_interval}s interval")
    
    async def start(self):
        """Start the system health monitoring service"""
        if self.running:
            logger.warning("System health monitor is already running")
            return
        
        self.running = True
        self._task = asyncio.create_task(self._monitor_loop())
        logger.info("System health monitor started")
    
    async def stop(self):
        """Stop the system health monitoring service"""
        if not self.running:
            logger.warning("System health monitor is not running")
            return
        
        self.running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        
        logger.info("System health monitor stopped")
    
    async def _monitor_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                await self._collect_health_data()
                await asyncio.sleep(self.collection_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in system health monitoring loop: {e}")
                # Log error to telemetry
                if self.telemetry.is_enabled():
                    try:
                        self.telemetry.log_error(
                            error_type="health_monitor_error",
                            error_message=str(e),
                            severity="warning",
                            component="system_health_monitor"
                        )
                    except Exception as te:
                        logger.error(f"Error logging telemetry: {te}")
                
                # Wait before retrying
                await asyncio.sleep(60)
    
    async def _collect_health_data(self):
        """Collect system health data"""
        if not self.telemetry.is_enabled():
            return
        
        try:
            # Collect system health data
            health_data = self.telemetry.collect_system_health_data()
            
            if health_data:
                # Save to telemetry system
                self.telemetry._save_data('system_health', health_data.__dict__)
                
                # Log critical issues
                if health_data.system_status == "critical":
                    logger.critical(f"System health critical: CPU={health_data.cpu_usage_percent}%, "
                                  f"Memory={health_data.memory_usage_percent}%, "
                                  f"Disk={health_data.disk_usage_percent}%")
                elif health_data.system_status == "degraded":
                    logger.warning(f"System health degraded: CPU={health_data.cpu_usage_percent}%, "
                                 f"Memory={health_data.memory_usage_percent}%, "
                                 f"Disk={health_data.disk_usage_percent}%")
                
                # Log critical errors
                if health_data.critical_errors > 0:
                    logger.warning(f"System has {health_data.critical_errors} critical errors")
                    
        except Exception as e:
            logger.error(f"Error collecting system health data: {e}")
            # Log this error to telemetry
            if self.telemetry.is_enabled():
                try:
                    self.telemetry.log_error(
                        error_type="health_data_collection_error",
                        error_message=str(e),
                        severity="warning",
                        component="system_health_monitor"
                    )
                except Exception as te:
                    logger.error(f"Error logging telemetry: {te}")

# Global system health monitor instance
_system_health_monitor: Optional[SystemHealthMonitor] = None

def get_system_health_monitor() -> SystemHealthMonitor:
    """Get the global system health monitor instance"""
    global _system_health_monitor
    if _system_health_monitor is None:
        _system_health_monitor = SystemHealthMonitor()
    return _system_health_monitor

async def start_system_health_monitoring():
    """Start system health monitoring service"""
    monitor = get_system_health_monitor()
    await monitor.start()

async def stop_system_health_monitoring():
    """Stop system health monitoring service"""
    monitor = get_system_health_monitor()
    await monitor.stop()
