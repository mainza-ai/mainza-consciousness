"""
Privacy-First Telemetry Router

Provides API endpoints for telemetry data with complete privacy protection.
All data remains local, no personal information is collected or transmitted.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import logging

from backend.utils.privacy_first_telemetry import get_telemetry, PrivacyFirstTelemetry

router = APIRouter(prefix="/telemetry", tags=["telemetry"])
logger = logging.getLogger(__name__)

@router.get("/status")
async def get_telemetry_status():
    """
    Get telemetry system status and privacy information.
    Shows exactly what data is collected (transparency).
    """
    try:
        telemetry = get_telemetry()
        return {
            "status": "operational",
            "privacy_protection": {
                "personal_data_collected": False,
                "external_transmission": False,
                "local_processing_only": True,
                "user_controlled": True
            },
            "collection_enabled": telemetry.is_enabled(),
            "data_location": telemetry.data_dir.absolute().as_posix(),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        logger.error(f"Error getting telemetry status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get telemetry status")

@router.get("/summary")
async def get_telemetry_summary():
    """
    Get summary of collected telemetry data.
    Shows data counts and collection settings (transparency).
    """
    try:
        telemetry = get_telemetry()
        summary = telemetry.get_telemetry_summary()
        return summary
    except Exception as e:
        logger.error(f"Error getting telemetry summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to get telemetry summary")

@router.get("/data/{data_type}")
async def get_telemetry_data(
    data_type: str,
    limit: Optional[int] = Query(100, description="Maximum number of records to return"),
    days: Optional[int] = Query(7, description="Number of days to look back")
):
    """
    Get telemetry data for review (local only).
    No personal data, no external transmission.
    
    Args:
        data_type: Type of data to retrieve (system_health, consciousness, errors)
        limit: Maximum number of records to return
        days: Number of days to look back
    """
    try:
        if data_type not in ["system_health", "consciousness", "errors"]:
            raise HTTPException(status_code=400, detail="Invalid data type")
        
        telemetry = get_telemetry()
        data = telemetry.export_data(data_type)
        
        if data is None:
            raise HTTPException(status_code=500, detail="Failed to export data")
        
        # Filter by date if specified
        if days > 0:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            filtered_data = []
            for item in data:
                try:
                    item_date = datetime.fromisoformat(item['timestamp'].replace('Z', '+00:00'))
                    if item_date >= cutoff_date:
                        filtered_data.append(item)
                except Exception:
                    # Keep item if date parsing fails
                    filtered_data.append(item)
            data = filtered_data
        
        # Apply limit
        if limit > 0:
            data = data[-limit:]  # Get most recent records
        
        return {
            "data_type": data_type,
            "count": len(data),
            "data": data,
            "privacy_note": "No personal data collected - local processing only"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting telemetry data: {e}")
        raise HTTPException(status_code=500, detail="Failed to get telemetry data")

@router.post("/control/enable")
async def enable_telemetry():
    """Enable telemetry collection (user control)"""
    try:
        telemetry = get_telemetry()
        telemetry.set_enabled(True)
        return {
            "status": "success",
            "message": "Telemetry enabled",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        logger.error(f"Error enabling telemetry: {e}")
        raise HTTPException(status_code=500, detail="Failed to enable telemetry")

@router.post("/control/disable")
async def disable_telemetry():
    """Disable telemetry collection (user control)"""
    try:
        telemetry = get_telemetry()
        telemetry.set_enabled(False)
        return {
            "status": "success",
            "message": "Telemetry disabled",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        logger.error(f"Error disabling telemetry: {e}")
        raise HTTPException(status_code=500, detail="Failed to disable telemetry")

@router.post("/control/settings")
async def update_collection_settings(
    system_health: Optional[bool] = None,
    consciousness: Optional[bool] = None,
    errors: Optional[bool] = None
):
    """Update telemetry collection settings (user control)"""
    try:
        telemetry = get_telemetry()
        
        # Only update provided settings
        current_settings = {
            "system_health": telemetry.collect_system_health,
            "consciousness": telemetry.collect_consciousness,
            "errors": telemetry.collect_errors
        }
        
        if system_health is not None:
            current_settings["system_health"] = system_health
        if consciousness is not None:
            current_settings["consciousness"] = consciousness
        if errors is not None:
            current_settings["errors"] = errors
        
        telemetry.set_collection_settings(**current_settings)
        
        return {
            "status": "success",
            "message": "Collection settings updated",
            "settings": current_settings,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        logger.error(f"Error updating collection settings: {e}")
        raise HTTPException(status_code=500, detail="Failed to update collection settings")

@router.delete("/data")
async def delete_all_telemetry_data():
    """Delete all telemetry data (user control)"""
    try:
        telemetry = get_telemetry()
        telemetry.delete_all_data()
        return {
            "status": "success",
            "message": "All telemetry data deleted",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        logger.error(f"Error deleting telemetry data: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete telemetry data")

@router.get("/privacy")
async def get_privacy_information():
    """
    Get detailed privacy information about telemetry collection.
    Shows exactly what data is collected and how it's protected.
    """
    try:
        return {
            "privacy_policy": {
                "data_collection": {
                    "personal_data": False,
                    "user_identification": False,
                    "conversation_data": False,
                    "usage_patterns": False,
                    "session_data": False
                },
                "data_processing": {
                    "local_processing_only": True,
                    "external_transmission": False,
                    "third_party_services": False,
                    "cloud_storage": False
                },
                "data_types_collected": {
                    "system_health": "Basic system status, resource usage, service health",
                    "consciousness": "Anonymous consciousness level, evolution status",
                    "errors": "Critical system errors, no personal information"
                },
                "user_controls": {
                    "enable_disable": True,
                    "data_deletion": True,
                    "collection_settings": True,
                    "data_export": True
                },
                "data_retention": {
                    "system_health": "30 days maximum",
                    "consciousness": "90 days maximum",
                    "errors": "7 days maximum"
                }
            },
            "compliance": {
                "gdpr_compliant": True,
                "ccpa_compliant": True,
                "local_processing_only": True,
                "user_consent_required": True
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        logger.error(f"Error getting privacy information: {e}")
        raise HTTPException(status_code=500, detail="Failed to get privacy information")

@router.get("/health")
async def get_telemetry_health():
    """Get telemetry system health status"""
    try:
        telemetry = get_telemetry()
        summary = telemetry.get_telemetry_summary()
        
        return {
            "status": "healthy",
            "enabled": telemetry.is_enabled(),
            "data_directory_exists": telemetry.data_dir.exists(),
            "collection_active": {
                "system_health": telemetry.collect_system_health,
                "consciousness": telemetry.collect_consciousness,
                "errors": telemetry.collect_errors
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        logger.error(f"Error getting telemetry health: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
