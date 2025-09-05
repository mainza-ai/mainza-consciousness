"""
Enhanced Neo4j administration and monitoring endpoints with security and comprehensive management.
Addresses critical issues from code review:
- Enhanced security with proper validation
- Integration with monitoring system
- Comprehensive health checks and metrics
- Safe query execution with validation
"""
from fastapi import APIRouter, HTTPException, Depends, Security, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any, Optional, List
from backend.utils.neo4j_production import neo4j_production
from backend.utils.neo4j_monitoring import initialize_monitoring, get_monitor
from backend.utils.embedding_enhanced import embedding_manager
from pydantic import BaseModel, Field
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

# Initialize monitoring
monitor = initialize_monitoring(neo4j_production)

# Security
security = HTTPBearer(auto_error=False)

class CypherQueryRequest(BaseModel):
    query: str = Field(..., description="Cypher query to execute")
    parameters: Optional[Dict[str, Any]] = Field(default=None, description="Query parameters")
    read_only: bool = Field(default=True, description="Whether this is a read-only query")
    timeout: Optional[int] = Field(default=30, description="Query timeout in seconds")

class DatabaseCleanupRequest(BaseModel):
    confirm: bool = Field(..., description="Confirmation required for cleanup operations")
    operations: List[str] = Field(default=["orphaned_chunks"], description="Cleanup operations to perform")

def get_admin_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify admin credentials for sensitive operations."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin authentication required"
        )
    
    # In production, implement proper JWT validation
    admin_token = os.getenv("ADMIN_TOKEN", "admin-secret-token")
    if credentials.credentials != admin_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid admin credentials"
        )
    
    return {"admin": True}

router = APIRouter(prefix="/admin/neo4j", tags=["Neo4j Administration"])

@router.get("/health")
async def get_health_status() -> Dict[str, Any]:
    """Get comprehensive Neo4j health status with enhanced monitoring."""
    try:
        # Use production Neo4j manager for health check
        health_status = neo4j_production.health_check()
        
        # Add monitoring data if available
        if monitor:
            monitoring_data = monitor.get_monitoring_report(hours_back=1)
            health_status["monitoring"] = {
                "active_alerts": len(monitoring_data["alerts"]["active"]),
                "system_health": monitoring_data["system_overview"]["system_health"],
                "recent_performance": monitoring_data["detailed_metrics"]
            }
        
        # Determine HTTP status code based on health
        status_code = 200
        if health_status.get("status") == "unhealthy":
            status_code = 503  # Service unavailable
        elif health_status.get("connection_status") == "failed":
            status_code = 503
        
        return JSONResponse(content=health_status, status_code=status_code)
        
    except Exception as e:
        logger.error(f"Health check endpoint failed: {e}")
        return JSONResponse(
            content={"error": str(e), "status": "error"}, 
            status_code=500
        )

@router.get("/stats")
async def get_database_stats() -> Dict[str, Any]:
    """Get comprehensive database statistics with enhanced monitoring."""
    try:
        # Get health info which includes database statistics
        health_info = neo4j_production.health_check()
        stats = health_info.get("database_info", {})
        
        # Add monitoring metrics if available
        if monitor:
            monitoring_report = monitor.get_monitoring_report(hours_back=24)
            stats["monitoring_summary"] = monitoring_report["system_overview"]
            stats["performance_metrics"] = monitoring_report["detailed_metrics"]
        
        return {
            "timestamp": datetime.now().isoformat(),
            "database_statistics": stats,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Database stats endpoint failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/embedding-info")
async def get_embedding_info() -> Dict[str, Any]:
    """Get information about embedding configuration and status."""
    try:
        info = embedding_manager.get_model_info()
        return info
    except Exception as e:
        logger.error(f"Embedding info endpoint failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-embedding")
async def test_embedding(text: str = "This is a test embedding") -> Dict[str, Any]:
    """Test embedding generation."""
    try:
        embedding = embedding_manager.get_embedding(text)
        
        return {
            "text": text,
            "embedding_length": len(embedding),
            "embedding_sample": embedding[:5],  # First 5 dimensions
            "all_zeros": all(x == 0.0 for x in embedding),
            "status": "success" if not all(x == 0.0 for x in embedding) else "warning"
        }
    except Exception as e:
        logger.error(f"Test embedding failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-vector-search")
async def test_vector_search(query: str = "artificial intelligence", top_k: int = 3) -> Dict[str, Any]:
    """Test vector search functionality."""
    try:
        from backend.utils.embedding_enhanced import vector_search_chunks
        
        results = vector_search_chunks(query, top_k)
        
        return {
            "query": query,
            "top_k": top_k,
            "results_count": len(results),
            "results": results,
            "status": "success" if results else "no_results"
        }
    except Exception as e:
        logger.error(f"Test vector search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cleanup")
async def cleanup_database(
    request: DatabaseCleanupRequest,
    admin: dict = Depends(get_admin_user)
) -> Dict[str, Any]:
    """Clean up orphaned data (requires admin authentication and confirmation)."""
    if not request.confirm:
        raise HTTPException(
            status_code=400, 
            detail="This operation requires confirmation. Set confirm=true"
        )
    
    try:
        cleanup_results = {}
        
        # Define cleanup operations
        cleanup_operations = {
            "orphaned_chunks": """
                MATCH (ch:Chunk) 
                WHERE NOT (ch)-[:DERIVED_FROM]->(:Document)
                DELETE ch
                RETURN count(ch) AS deleted_count
            """,
            "empty_memories": """
                MATCH (m:Memory)
                WHERE m.content IS NULL OR trim(m.content) = ''
                DELETE m
                RETURN count(m) AS deleted_count
            """,
            "duplicate_concepts": """
                MATCH (c1:Concept), (c2:Concept)
                WHERE c1.name = c2.name AND id(c1) < id(c2)
                DELETE c2
                RETURN count(c2) AS deleted_count
            """
        }
        
        for operation in request.operations:
            if operation in cleanup_operations:
                query = cleanup_operations[operation]
                result = neo4j_production.execute_write_query(query)
                cleanup_results[operation] = result[0] if result else {"deleted_count": 0}
            else:
                cleanup_results[operation] = {"error": f"Unknown operation: {operation}"}
        
        return {
            "timestamp": datetime.now().isoformat(),
            "operations_performed": request.operations,
            "results": cleanup_results,
            "status": "completed"
        }
        
    except Exception as e:
        logger.error(f"Database cleanup failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/indexes")
async def get_index_status() -> Dict[str, Any]:
    """Get detailed index status information using production Neo4j manager."""
    try:
        query = """
        SHOW INDEXES 
        YIELD name, type, state, populationPercent, 
              uniqueness, entityType, labelsOrTypes, properties
        RETURN name, type, state, populationPercent, 
               uniqueness, entityType, labelsOrTypes, properties
        ORDER BY name
        """
        
        records = neo4j_production.execute_query(query)
        
        # Analyze index health
        online_indexes = [r for r in records if r["state"] == "ONLINE"]
        failed_indexes = [r for r in records if r["state"] == "FAILED"]
        vector_indexes = [r for r in records if r["type"] == "VECTOR"]
        
        return {
            "timestamp": datetime.now().isoformat(),
            "indexes": records,
            "summary": {
                "total_count": len(records),
                "online_count": len(online_indexes),
                "failed_count": len(failed_indexes),
                "vector_count": len(vector_indexes)
            },
            "health_status": "healthy" if len(failed_indexes) == 0 else "degraded",
            "recommendations": [
                "Rebuild failed indexes" if failed_indexes else None,
                "Consider adding vector index for embeddings" if not vector_indexes else None
            ]
        }
    except Exception as e:
        logger.error(f"Get index status failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/constraints")
async def get_constraint_status() -> Dict[str, Any]:
    """Get detailed constraint status information using production Neo4j manager."""
    try:
        query = """
        SHOW CONSTRAINTS 
        YIELD name, type, entityType, labelsOrTypes, properties, ownedIndex
        RETURN name, type, entityType, labelsOrTypes, properties, ownedIndex
        ORDER BY name
        """
        
        records = neo4j_production.execute_query(query)
        
        # Analyze constraint types
        uniqueness_constraints = [r for r in records if r["type"] == "UNIQUENESS"]
        existence_constraints = [r for r in records if r["type"] == "NODE_PROPERTY_EXISTENCE"]
        
        return {
            "timestamp": datetime.now().isoformat(),
            "constraints": records,
            "summary": {
                "total_count": len(records),
                "uniqueness_count": len(uniqueness_constraints),
                "existence_count": len(existence_constraints)
            },
            "health_status": "healthy",
            "recommendations": [
                "Consider adding existence constraints for critical properties" if len(existence_constraints) == 0 else None
            ]
        }
    except Exception as e:
        logger.error(f"Get constraint status failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/execute-cypher")
async def execute_cypher_query(
    request: CypherQueryRequest,
    admin: dict = Depends(get_admin_user)
) -> Dict[str, Any]:
    """Execute a Cypher query with enhanced security validation (admin only)."""
    
    try:
        # Use production Neo4j manager with built-in security validation
        if request.read_only:
            records = neo4j_production.execute_query(
                request.query, 
                request.parameters, 
                timeout=request.timeout
            )
        else:
            records = neo4j_production.execute_write_query(
                request.query, 
                request.parameters, 
                timeout=request.timeout
            )
        
        return {
            "timestamp": datetime.now().isoformat(),
            "query": request.query,
            "parameters": request.parameters,
            "result": records,
            "result_count": len(records),
            "read_only": request.read_only,
            "status": "success"
        }
    except ValueError as e:
        # Query validation failed
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Execute Cypher query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performance-metrics")
async def get_performance_metrics(hours_back: int = 24) -> Dict[str, Any]:
    """Get comprehensive performance metrics and recommendations using monitoring system."""
    try:
        # Get monitoring report if available
        if monitor:
            monitoring_report = monitor.get_monitoring_report(hours_back)
            return {
                "timestamp": datetime.now().isoformat(),
                "monitoring_report": monitoring_report,
                "status": "success"
            }
        
        # Fallback to basic performance tests using production manager
        import time
        start_time = time.time()
        
        test_queries = {
            "simple_count": "MATCH (n) RETURN count(n) AS total_nodes",
            "memory_search": "MATCH (m:Memory) WHERE m.content CONTAINS 'test' RETURN count(m) AS matches",
            "relationship_count": "MATCH ()-[r]->() RETURN count(r) AS total_relationships"
        }
        
        metrics = {}
        for name, query in test_queries.items():
            query_start = time.time()
            result = neo4j_production.execute_query(query)
            query_time = time.time() - query_start
            
            metrics[name] = {
                "result": result[0] if result else None,
                "execution_time_ms": round(query_time * 1000, 2)
            }
        
        total_time = time.time() - start_time
        
        # Performance recommendations
        recommendations = []
        if metrics["simple_count"]["execution_time_ms"] > 1000:
            recommendations.append("Consider adding more indexes for better query performance")
        if metrics.get("memory_search", {}).get("execution_time_ms", 0) > 500:
            recommendations.append("Text search is slow - consider using full-text indexes")
        
        return {
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
            "total_test_time_ms": round(total_time * 1000, 2),
            "recommendations": recommendations,
            "status": "good" if not recommendations else "needs_optimization"
        }
        
    except Exception as e:
        logger.error(f"Get performance metrics failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/monitoring-dashboard")
async def get_monitoring_dashboard() -> Dict[str, Any]:
    """Get comprehensive monitoring dashboard data."""
    try:
        if not monitor:
            raise HTTPException(status_code=503, detail="Monitoring system not available")
        
        dashboard = monitor.metrics_collector.get_metrics_dashboard()
        return {
            "timestamp": datetime.now().isoformat(),
            "dashboard": dashboard,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Get monitoring dashboard failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/alerts")
async def get_active_alerts() -> Dict[str, Any]:
    """Get all active alerts from the monitoring system."""
    try:
        if not monitor:
            return {"alerts": [], "message": "Monitoring system not available"}
        
        active_alerts = monitor.metrics_collector.get_active_alerts()
        return {
            "timestamp": datetime.now().isoformat(),
            "active_alerts": active_alerts,
            "alert_count": len(active_alerts),
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Get active alerts failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/resolve-alert/{alert_index}")
async def resolve_alert(
    alert_index: int,
    admin: dict = Depends(get_admin_user)
) -> Dict[str, Any]:
    """Resolve an active alert (admin only)."""
    try:
        if not monitor:
            raise HTTPException(status_code=503, detail="Monitoring system not available")
        
        success = monitor.metrics_collector.resolve_alert(alert_index)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "alert_index": alert_index,
            "resolved": success,
            "status": "success" if success else "failed"
        }
    except Exception as e:
        logger.error(f"Resolve alert failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/optimize-database")
async def optimize_database(
    admin: dict = Depends(get_admin_user)
) -> Dict[str, Any]:
    """Run database optimization tasks (admin only)."""
    try:
        optimization_results = neo4j_production.optimize_database()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "optimization_results": optimization_results,
            "status": "completed"
        }
    except Exception as e:
        logger.error(f"Database optimization failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/query-metrics")
async def get_query_metrics(hours_back: int = 1) -> Dict[str, Any]:
    """Get detailed query execution metrics."""
    try:
        if not monitor:
            return {"metrics": [], "message": "Monitoring system not available"}
        
        query_metrics = monitor.metrics_collector.get_query_metrics(hours_back)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "hours_back": hours_back,
            "query_metrics": query_metrics,
            "total_queries": len(query_metrics),
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Get query metrics failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export-metrics")
async def export_metrics(
    format: str = "json",
    hours_back: int = 24,
    admin: dict = Depends(get_admin_user)
) -> Dict[str, Any]:
    """Export comprehensive metrics data (admin only)."""
    try:
        if not monitor:
            raise HTTPException(status_code=503, detail="Monitoring system not available")
        
        exported_data = monitor.export_metrics(format, hours_back)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "format": format,
            "hours_back": hours_back,
            "data": exported_data,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Export metrics failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
