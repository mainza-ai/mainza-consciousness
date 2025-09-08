"""
Build Information Router
Provides build metadata and timestamps for container verification
"""

from fastapi import APIRouter
from datetime import datetime
import os
import subprocess
import sys

router = APIRouter(prefix="/build", tags=["build"])

@router.get("/info")
async def get_build_info():
    """Get build information including timestamps and git commit"""
    try:
        # Get git commit if available
        git_commit = "unknown"
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True,
                text=True,
                cwd="/app"
            )
            if result.returncode == 0:
                git_commit = result.stdout.strip()
        except Exception:
            pass

        # Get build timestamp from environment or current time
        build_date = os.getenv("BUILD_DATE", datetime.utcnow().isoformat() + "Z")
        
        # Get cache bust value
        cache_bust = os.getenv("CACHE_BUST", "unknown")
        
        # Get Python version
        python_version = sys.version
        
        return {
            "build_date": build_date,
            "git_commit": git_commit,
            "cache_bust": cache_bust,
            "python_version": python_version,
            "container_started": datetime.utcnow().isoformat() + "Z",
            "status": "healthy"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }

@router.get("/health")
async def build_health_check():
    """Simple health check for build verification"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
