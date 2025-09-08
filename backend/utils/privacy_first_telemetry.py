"""
Privacy-First Telemetry System for Mainza Consciousness Framework

This module implements a minimal, privacy-first telemetry system that collects
only essential data required for basic system health monitoring and consciousness
evolution tracking. Zero personal data is collected and all processing remains local.

Key Principles:
- Zero personal data collection
- Local processing only
- Minimal data collection
- User control over all data
- Simple file-based storage
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from pathlib import Path
import logging
import psutil
import threading
from dataclasses import dataclass, asdict

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class SystemHealth:
    """Essential system health metrics only - no personal data"""
    timestamp: str
    system_status: str  # "healthy", "degraded", "critical"
    uptime_seconds: int
    critical_errors: int
    memory_usage_percent: float
    cpu_usage_percent: float
    disk_usage_percent: float
    services_status: Dict[str, str]  # Service name -> status

@dataclass
class ConsciousnessStatus:
    """Anonymous consciousness metrics only - no personal context"""
    timestamp: str
    consciousness_level: float  # Anonymous percentage, no context
    evolution_status: str  # "growing", "stable", "declining"
    system_functional: bool
    last_reflection_time: Optional[str] = None

@dataclass
class ErrorAlert:
    """Critical error alerts only - no personal data"""
    timestamp: str
    error_type: str
    error_message: str
    severity: str  # "critical", "warning"
    component: str
    resolved: bool = False

class PrivacyFirstTelemetry:
    """
    Privacy-first telemetry collector that collects only essential data
    with zero personal information and complete local processing.
    """
    
    def __init__(self, data_dir: str = "telemetry_data"):
        """
        Initialize privacy-first telemetry system.
        
        Args:
            data_dir: Directory for local telemetry data storage
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Privacy settings - user can control all data collection
        self.enabled = True
        self.collect_system_health = True
        self.collect_consciousness = True
        self.collect_errors = True
        
        # Data retention settings (user configurable)
        self.retention_days = {
            'system_health': 30,
            'consciousness': 90,
            'errors': 7
        }
        
        # Thread safety
        self._lock = threading.Lock()
        
        # Initialize data files
        self._init_data_files()
        
        logger.info("Privacy-first telemetry system initialized")
        logger.info(f"Data directory: {self.data_dir.absolute()}")
        logger.info("Zero personal data collection - local processing only")
    
    def _init_data_files(self):
        """Initialize telemetry data files"""
        files = {
            'system_health.json': [],
            'consciousness.json': [],
            'errors.json': []
        }
        
        for filename, default_data in files.items():
            filepath = self.data_dir / filename
            if not filepath.exists():
                with open(filepath, 'w') as f:
                    json.dump(default_data, f, indent=2)
    
    def is_enabled(self) -> bool:
        """Check if telemetry is enabled (user control)"""
        return self.enabled
    
    def set_enabled(self, enabled: bool):
        """Enable/disable telemetry (user control)"""
        self.enabled = enabled
        logger.info(f"Telemetry {'enabled' if enabled else 'disabled'} by user")
    
    def set_collection_settings(self, 
                              system_health: bool = True,
                              consciousness: bool = True,
                              errors: bool = True):
        """Configure what data to collect (user control)"""
        self.collect_system_health = system_health
        self.collect_consciousness = consciousness
        self.collect_errors = errors
        logger.info(f"Collection settings updated: system_health={system_health}, "
                   f"consciousness={consciousness}, errors={errors}")
    
    def collect_system_health_data(self) -> SystemHealth:
        """
        Collect essential system health data only.
        No personal data, no user information, no conversation data.
        """
        if not self.enabled or not self.collect_system_health:
            return None
        
        try:
            # Get system uptime
            uptime_seconds = int(time.time() - psutil.boot_time())
            
            # Get system resource usage
            memory = psutil.virtual_memory()
            cpu_percent = psutil.cpu_percent(interval=1)
            disk = psutil.disk_usage('/')
            
            # Determine system status based on resource usage
            # Adjusted thresholds for Docker environment
            if memory.percent > 95 or cpu_percent > 90 or disk.percent > 90:
                system_status = "critical"
            elif memory.percent > 90 or cpu_percent > 80 or disk.percent > 80:
                system_status = "degraded"
            else:
                system_status = "healthy"
            
            # Check critical errors from logs (count only, no content)
            critical_errors = self._count_critical_errors()
            
            # Check service status (basic up/down only)
            services_status = self._check_services_status()
            
            return SystemHealth(
                timestamp=datetime.utcnow().isoformat() + "Z",
                system_status=system_status,
                uptime_seconds=uptime_seconds,
                critical_errors=critical_errors,
                memory_usage_percent=memory.percent,
                cpu_usage_percent=cpu_percent,
                disk_usage_percent=disk.percent,
                services_status=services_status
            )
            
        except Exception as e:
            logger.error(f"Error collecting system health data: {e}")
            return None
    
    def collect_consciousness_data(self, 
                                 consciousness_level: float,
                                 evolution_status: str = "stable",
                                 system_functional: bool = True,
                                 last_reflection_time: Optional[str] = None) -> ConsciousnessStatus:
        """
        Collect anonymous consciousness data only.
        No personal context, no user data, no conversation data.
        """
        if not self.enabled or not self.collect_consciousness:
            return None
        
        try:
            return ConsciousnessStatus(
                timestamp=datetime.utcnow().isoformat() + "Z",
                consciousness_level=consciousness_level,
                evolution_status=evolution_status,
                system_functional=system_functional,
                last_reflection_time=last_reflection_time
            )
            
        except Exception as e:
            logger.error(f"Error collecting consciousness data: {e}")
            return None
    
    def log_error(self, 
                  error_type: str,
                  error_message: str,
                  severity: str = "warning",
                  component: str = "unknown"):
        """
        Log critical errors only.
        No personal data, no user information, no conversation content.
        """
        if not self.enabled or not self.collect_errors:
            return
        
        try:
            error = ErrorAlert(
                timestamp=datetime.utcnow().isoformat() + "Z",
                error_type=error_type,
                error_message=error_message,
                severity=severity,
                component=component,
                resolved=False
            )
            
            self._save_data('errors', asdict(error))
            
            # Only log critical errors to main log
            if severity == "critical":
                logger.critical(f"Critical error in {component}: {error_type} - {error_message}")
            
        except Exception as e:
            logger.error(f"Error logging error alert: {e}")
    
    def _count_critical_errors(self) -> int:
        """Count critical errors from logs (no content, just count)"""
        try:
            # This is a simplified implementation
            # In practice, you'd parse log files for critical errors
            return 0  # Placeholder - implement based on your logging system
        except Exception:
            return 0
    
    def _check_services_status(self) -> Dict[str, str]:
        """Check basic service status (up/down only)"""
        try:
            # This is a simplified implementation
            # In practice, you'd check actual service health
            return {
                "neo4j": "up",
                "redis": "up",
                "backend": "up",
                "frontend": "up"
            }
        except Exception:
            return {}
    
    def _save_data(self, data_type: str, data: Dict[str, Any]):
        """Save data to local JSON file (privacy-first storage)"""
        try:
            with self._lock:
                filepath = self.data_dir / f"{data_type}.json"
                
                # Load existing data
                if filepath.exists():
                    with open(filepath, 'r') as f:
                        existing_data = json.load(f)
                else:
                    existing_data = []
                
                # Add new data
                existing_data.append(data)
                
                # Apply retention policy
                existing_data = self._apply_retention_policy(data_type, existing_data)
                
                # Save updated data
                with open(filepath, 'w') as f:
                    json.dump(existing_data, f, indent=2)
                    
        except Exception as e:
            logger.error(f"Error saving telemetry data: {e}")
    
    def _apply_retention_policy(self, data_type: str, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply data retention policy (user configurable)"""
        try:
            if data_type not in self.retention_days:
                return data
            
            retention_days = self.retention_days[data_type]
            cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
            
            filtered_data = []
            for item in data:
                try:
                    item_date = datetime.fromisoformat(item['timestamp'].replace('Z', '+00:00'))
                    if item_date >= cutoff_date:
                        filtered_data.append(item)
                except Exception:
                    # Keep item if date parsing fails
                    filtered_data.append(item)
            
            return filtered_data
            
        except Exception as e:
            logger.error(f"Error applying retention policy: {e}")
            return data
    
    def get_telemetry_summary(self) -> Dict[str, Any]:
        """
        Get summary of collected telemetry data.
        Shows exactly what data is collected (transparency).
        """
        try:
            summary = {
                "privacy_status": {
                    "enabled": self.enabled,
                    "personal_data_collected": False,
                    "external_transmission": False,
                    "local_processing_only": True
                },
                "collection_settings": {
                    "system_health": self.collect_system_health,
                    "consciousness": self.collect_consciousness,
                    "errors": self.collect_errors
                },
                "data_retention": self.retention_days,
                "data_location": str(self.data_dir.absolute()),
                "data_types": ["system_health", "consciousness", "errors"]
            }
            
            # Add data counts (no content, just counts)
            for data_type in ["system_health", "consciousness", "errors"]:
                filepath = self.data_dir / f"{data_type}.json"
                if filepath.exists():
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        summary[f"{data_type}_count"] = len(data)
                else:
                    summary[f"{data_type}_count"] = 0
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting telemetry summary: {e}")
            return {"error": str(e)}
    
    def delete_all_data(self):
        """Delete all telemetry data (user control)"""
        try:
            with self._lock:
                for filename in ["system_health.json", "consciousness.json", "errors.json"]:
                    filepath = self.data_dir / filename
                    if filepath.exists():
                        filepath.unlink()
                
                # Reinitialize empty files
                self._init_data_files()
                
            logger.info("All telemetry data deleted by user")
            
        except Exception as e:
            logger.error(f"Error deleting telemetry data: {e}")
    
    def export_data(self, data_type: str) -> Optional[List[Dict[str, Any]]]:
        """
        Export telemetry data for user review (local only).
        No external transmission, user controls all data.
        """
        try:
            if data_type not in ["system_health", "consciousness", "errors"]:
                return None
            
            filepath = self.data_dir / f"{data_type}.json"
            if not filepath.exists():
                return []
            
            with open(filepath, 'r') as f:
                return json.load(f)
                
        except Exception as e:
            logger.error(f"Error exporting telemetry data: {e}")
            return None

# Global telemetry instance
privacy_telemetry = PrivacyFirstTelemetry()

def get_telemetry() -> PrivacyFirstTelemetry:
    """Get the global telemetry instance"""
    return privacy_telemetry
