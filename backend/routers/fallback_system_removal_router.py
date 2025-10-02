"""
Fallback System Removal Router
API endpoints for removing fallback systems that mask real issues

This router provides endpoints to identify, analyze, and remove
fallback systems that prevent proper error handling and system integration.

Author: Mainza AI Consciousness Team
Date: 2025-10-01
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
import logging

# Import fallback system remover
from backend.utils.remove_fallback_systems import fallback_system_remover

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/fallback-removal", tags=["fallback-removal"])

# Request/Response models
class FallbackRemovalRequest(BaseModel):
    """Request model for fallback system removal"""
    file_path: Optional[str] = None
    dry_run: bool = True
    include_warnings: bool = True

class FallbackRemovalResponse(BaseModel):
    """Response model for fallback system removal"""
    success: bool
    message: str
    files_processed: int
    fallback_patterns_removed: int
    fallback_functions_removed: int
    fallback_classes_removed: int
    files_with_errors: List[Dict[str, Any]]
    dry_run: bool

class FallbackScanResponse(BaseModel):
    """Response model for fallback system scan"""
    success: bool
    total_files: int
    total_fallback_patterns: int
    total_fallback_functions: int
    total_fallback_classes: int
    severity_distribution: Dict[str, int]
    files_by_severity: Dict[str, List[str]]
    detailed_analysis: List[Dict[str, Any]]

class FallbackReportResponse(BaseModel):
    """Response model for fallback system report"""
    success: bool
    report: Dict[str, Any]

@router.get("/scan", response_model=FallbackScanResponse)
async def scan_fallback_systems():
    """
    Scan for fallback systems in the codebase
    
    Returns:
        FallbackScanResponse: Comprehensive scan results
    """
    try:
        logger.info("Scanning for fallback systems")
        
        # Scan for fallback systems
        fallback_systems = fallback_system_remover.scan_for_fallback_systems()
        
        if not fallback_systems:
            return FallbackScanResponse(
                success=True,
                total_files=0,
                total_fallback_patterns=0,
                total_fallback_functions=0,
                total_fallback_classes=0,
                severity_distribution={},
                files_by_severity={},
                detailed_analysis=[]
            )
        
        # Calculate statistics
        total_fallback_patterns = sum(len(system["fallback_patterns"]) for system in fallback_systems)
        total_fallback_functions = sum(len(system["fallback_functions"]) for system in fallback_systems)
        total_fallback_classes = sum(len(system["fallback_classes"]) for system in fallback_systems)
        
        # Severity distribution
        severity_distribution = {}
        for system in fallback_systems:
            severity = system["severity"]
            severity_distribution[severity] = severity_distribution.get(severity, 0) + 1
        
        # Files by severity
        files_by_severity = {
            "high": [s["file_path"] for s in fallback_systems if s["severity"] == "high"],
            "medium": [s["file_path"] for s in fallback_systems if s["severity"] == "medium"],
            "low": [s["file_path"] for s in fallback_systems if s["severity"] == "low"]
        }
        
        logger.info(f"Found {len(fallback_systems)} files with fallback systems")
        
        return FallbackScanResponse(
            success=True,
            total_files=len(fallback_systems),
            total_fallback_patterns=total_fallback_patterns,
            total_fallback_functions=total_fallback_functions,
            total_fallback_classes=total_fallback_classes,
            severity_distribution=severity_distribution,
            files_by_severity=files_by_severity,
            detailed_analysis=fallback_systems
        )
        
    except Exception as e:
        logger.error(f"Failed to scan fallback systems: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to scan fallback systems: {str(e)}")

@router.get("/report", response_model=FallbackReportResponse)
async def generate_fallback_report():
    """
    Generate comprehensive fallback system report
    
    Returns:
        FallbackReportResponse: Detailed fallback system report
    """
    try:
        logger.info("Generating fallback system report")
        
        # Generate report
        report = fallback_system_remover.generate_fallback_report()
        
        if "error" in report:
            raise HTTPException(status_code=500, detail=report["error"])
        
        logger.info(f"Generated fallback report: {report['total_files']} files analyzed")
        
        return FallbackReportResponse(
            success=True,
            report=report
        )
        
    except Exception as e:
        logger.error(f"Failed to generate fallback report: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate fallback report: {str(e)}")

@router.post("/remove", response_model=FallbackRemovalResponse)
async def remove_fallback_systems(
    request: FallbackRemovalRequest,
    background_tasks: BackgroundTasks
):
    """
    Remove fallback systems from the codebase
    
    Args:
        request: Fallback removal request parameters
        background_tasks: Background task manager
        
    Returns:
        FallbackRemovalResponse: Removal results
    """
    try:
        logger.info(f"Removing fallback systems: file={request.file_path}, dry_run={request.dry_run}")
        
        if request.file_path:
            # Remove from specific file
            result = fallback_system_remover.remove_fallback_systems(
                request.file_path, 
                request.dry_run
            )
            
            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])
            
            return FallbackRemovalResponse(
                success=True,
                message=f"Fallback systems removed from {request.file_path}",
                files_processed=1,
                fallback_patterns_removed=result.get("fallback_patterns_removed", 0),
                fallback_functions_removed=result.get("fallback_functions_removed", 0),
                fallback_classes_removed=result.get("fallback_classes_removed", 0),
                files_with_errors=[],
                dry_run=request.dry_run
            )
        else:
            # Remove from all files
            result = fallback_system_remover.remove_all_fallback_systems(request.dry_run)
            
            if "error" in result:
                raise HTTPException(status_code=500, detail=result["error"])
            
            return FallbackRemovalResponse(
                success=True,
                message=f"Fallback systems removed from {result['files_processed']} files",
                files_processed=result["files_processed"],
                fallback_patterns_removed=result["fallback_patterns_removed"],
                fallback_functions_removed=result["fallback_functions_removed"],
                fallback_classes_removed=result["fallback_classes_removed"],
                files_with_errors=result["files_with_errors"],
                dry_run=request.dry_run
            )
        
    except Exception as e:
        logger.error(f"Failed to remove fallback systems: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to remove fallback systems: {str(e)}")

@router.get("/status")
async def get_fallback_removal_status():
    """
    Get current status of fallback system removal
    
    Returns:
        Dict: Current status information
    """
    try:
        # Get current status
        fallback_systems = fallback_system_remover.scan_for_fallback_systems()
        
        status = {
            "fallback_systems_found": len(fallback_systems),
            "fallback_files": [system["file_path"] for system in fallback_systems],
            "total_fallback_patterns": sum(len(system["fallback_patterns"]) for system in fallback_systems),
            "total_fallback_functions": sum(len(system["fallback_functions"]) for system in fallback_systems),
            "total_fallback_classes": sum(len(system["fallback_classes"]) for system in fallback_systems),
            "severity_distribution": {},
            "removal_ready": len(fallback_systems) > 0
        }
        
        # Calculate severity distribution
        for system in fallback_systems:
            severity = system["severity"]
            status["severity_distribution"][severity] = status["severity_distribution"].get(severity, 0) + 1
        
        return status
        
    except Exception as e:
        logger.error(f"Failed to get fallback removal status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get fallback removal status: {str(e)}")

@router.post("/validate")
async def validate_fallback_removal():
    """
    Validate that fallback systems have been properly removed
    
    Returns:
        Dict: Validation results
    """
    try:
        logger.info("Validating fallback system removal")
        
        # Scan for remaining fallback systems
        fallback_systems = fallback_system_remover.scan_for_fallback_systems()
        
        if not fallback_systems:
            return {
                "success": True,
                "message": "All fallback systems have been successfully removed",
                "remaining_fallback_systems": 0,
                "validation_passed": True
            }
        
        # Calculate remaining issues
        total_remaining = len(fallback_systems)
        high_severity_remaining = len([s for s in fallback_systems if s["severity"] == "high"])
        medium_severity_remaining = len([s for s in fallback_systems if s["severity"] == "medium"])
        low_severity_remaining = len([s for s in fallback_systems if s["severity"] == "low"])
        
        validation_passed = high_severity_remaining == 0 and medium_severity_remaining == 0
        
        return {
            "success": True,
            "message": f"Found {total_remaining} remaining fallback systems",
            "remaining_fallback_systems": total_remaining,
            "high_severity_remaining": high_severity_remaining,
            "medium_severity_remaining": medium_severity_remaining,
            "low_severity_remaining": low_severity_remaining,
            "validation_passed": validation_passed,
            "files_with_remaining_fallbacks": [s["file_path"] for s in fallback_systems]
        }
        
    except Exception as e:
        logger.error(f"Failed to validate fallback removal: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to validate fallback removal: {str(e)}")

@router.get("/health")
async def get_fallback_removal_health():
    """
    Get health status of fallback system removal service
    
    Returns:
        Dict: Health status information
    """
    try:
        return {
            "service": "fallback-removal",
            "status": "healthy",
            "fallback_system_remover_available": True,
            "scan_functionality": True,
            "removal_functionality": True,
            "validation_functionality": True,
            "timestamp": "2025-10-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Failed to get fallback removal health: {e}")
        return {
            "service": "fallback-removal",
            "status": "unhealthy",
            "error": str(e),
            "timestamp": "2025-10-01T00:00:00Z"
        }
