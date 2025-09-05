"""
Memory System Health Monitoring API Endpoints

Provides REST API endpoints for memory system health monitoring,
performance metrics, and system diagnostics.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, Optional
import logging

from ..utils.memory_system_monitor import memory_monitor, HealthStatus
from ..utils.memory_lifecycle_manager import memory_lifecycle_manager
from ..utils.memory_storage_engine import MemoryStorageEngine
from ..utils.memory_retrieval_engine import MemoryRetrievalEngine
from ..utils.memory_context_builder import MemoryContextBuilder
from pydantic import BaseModel
from typing import List

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/memory-system", tags=["memory-system"])

# Pydantic models for API requests and responses
class MemorySearchRequest(BaseModel):
    query: str
    user_id: str
    limit: Optional[int] = 10
    similarity_threshold: Optional[float] = 0.3
    memory_types: Optional[List[str]] = None
    consciousness_context: Optional[Dict[str, Any]] = None

class MemoryCreateRequest(BaseModel):
    content: str
    memory_type: str
    user_id: str
    agent_name: str
    consciousness_context: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class MemoryResponse(BaseModel):
    memory_id: str
    content: str
    memory_type: str
    user_id: str
    agent_name: str
    consciousness_level: float
    emotional_state: str
    importance_score: float
    created_at: str
    last_accessed: Optional[str] = None
    access_count: int
    significance_score: float

class MemoryContextRequest(BaseModel):
    query: str
    user_id: str
    context_type: str = "conversation"
    consciousness_context: Optional[Dict[str, Any]] = None

@router.get("/health")
async def get_memory_system_health():
    """
    Get current memory system health status
    
    Returns comprehensive health information including:
    - Overall system health
    - Component-specific health status
    - Recent issues and warnings
    """
    try:
        health_status = await memory_monitor.perform_health_check()
        
        return {
            "status": "success",
            "data": {
                "overall_status": health_status.overall_status.value,
                "components": {
                    "storage": health_status.storage_status.value,
                    "retrieval": health_status.retrieval_status.value,
                    "neo4j": health_status.neo4j_status.value,
                    "embedding": health_status.embedding_status.value
                },
                "last_check_time": health_status.last_check_time.isoformat() if health_status.last_check_time else None,
                "issues": health_status.issues[-5:],  # Last 5 issues
                "warnings": health_status.warnings[-5:]  # Last 5 warnings
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get memory system health: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@router.get("/health/detailed")
async def get_detailed_health_status():
    """
    Get detailed memory system health status including performance metrics
    """
    try:
        dashboard_data = await memory_monitor.get_system_status_dashboard()
        
        return {
            "status": "success",
            "data": dashboard_data
        }
        
    except Exception as e:
        logger.error(f"Failed to get detailed health status: {e}")
        raise HTTPException(status_code=500, detail=f"Detailed health check failed: {str(e)}")

@router.get("/metrics")
async def get_performance_metrics():
    """
    Get memory system performance metrics
    
    Returns metrics for all memory operations including:
    - Response times
    - Success/failure rates
    - Operation counts
    """
    try:
        metrics = await memory_monitor.get_performance_metrics()
        
        return {
            "status": "success",
            "data": {
                "metrics": metrics,
                "monitoring_active": memory_monitor._monitoring_active
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get performance metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Metrics retrieval failed: {str(e)}")

@router.get("/usage")
async def get_usage_statistics():
    """
    Get memory system usage statistics
    
    Returns information about:
    - Total memory count
    - Memory distribution by type and user
    - Storage usage
    - Date ranges
    """
    try:
        usage_stats = await memory_monitor.update_usage_statistics()
        
        return {
            "status": "success",
            "data": {
                "total_memories": usage_stats.total_memories,
                "memories_by_type": usage_stats.memories_by_type,
                "memories_by_user": dict(list(usage_stats.memories_by_user.items())[:10]),  # Top 10 users
                "storage_size_mb": round(usage_stats.storage_size_mb, 2),
                "oldest_memory_date": usage_stats.oldest_memory_date.isoformat() if usage_stats.oldest_memory_date else None,
                "newest_memory_date": usage_stats.newest_memory_date.isoformat() if usage_stats.newest_memory_date else None,
                "average_memory_size": round(usage_stats.average_memory_size, 2)
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get usage statistics: {e}")
        raise HTTPException(status_code=500, detail=f"Usage statistics retrieval failed: {str(e)}")

@router.post("/monitoring/start")
async def start_monitoring(background_tasks: BackgroundTasks):
    """
    Start background memory system monitoring
    """
    try:
        if memory_monitor._monitoring_active:
            return {
                "status": "info",
                "message": "Memory monitoring is already active"
            }
        
        # Initialize monitor if not already done
        if not memory_monitor.storage_engine:
            initialized = await memory_monitor.initialize()
            if not initialized:
                raise HTTPException(status_code=500, detail="Failed to initialize memory monitor")
        
        # Start monitoring in background
        background_tasks.add_task(memory_monitor.start_monitoring)
        
        return {
            "status": "success",
            "message": "Memory system monitoring started"
        }
        
    except Exception as e:
        logger.error(f"Failed to start monitoring: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start monitoring: {str(e)}")

@router.post("/monitoring/stop")
async def stop_monitoring():
    """
    Stop background memory system monitoring
    """
    try:
        await memory_monitor.stop_monitoring()
        
        return {
            "status": "success",
            "message": "Memory system monitoring stopped"
        }
        
    except Exception as e:
        logger.error(f"Failed to stop monitoring: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to stop monitoring: {str(e)}")

@router.get("/monitoring/status")
async def get_monitoring_status():
    """
    Get current monitoring status
    """
    return {
        "status": "success",
        "data": {
            "monitoring_active": memory_monitor._monitoring_active,
            "health_check_interval": memory_monitor.health_check_interval,
            "alert_thresholds": memory_monitor.alert_thresholds
        }
    }

@router.post("/monitoring/configure")
async def configure_monitoring(
    health_check_interval: Optional[int] = None,
    max_response_time: Optional[float] = None,
    min_success_rate: Optional[float] = None,
    max_storage_size_gb: Optional[float] = None
):
    """
    Configure monitoring parameters
    """
    try:
        if health_check_interval is not None:
            memory_monitor.health_check_interval = max(60, health_check_interval)  # Minimum 1 minute
        
        if max_response_time is not None:
            memory_monitor.alert_thresholds['max_response_time'] = max(0.1, max_response_time)
        
        if min_success_rate is not None:
            memory_monitor.alert_thresholds['min_success_rate'] = max(0, min(100, min_success_rate))
        
        if max_storage_size_gb is not None:
            memory_monitor.alert_thresholds['max_storage_size_gb'] = max(0.1, max_storage_size_gb)
        
        return {
            "status": "success",
            "message": "Monitoring configuration updated",
            "data": {
                "health_check_interval": memory_monitor.health_check_interval,
                "alert_thresholds": memory_monitor.alert_thresholds
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to configure monitoring: {e}")
        raise HTTPException(status_code=500, detail=f"Configuration failed: {str(e)}")

@router.get("/diagnostics")
async def run_diagnostics():
    """
    Run comprehensive memory system diagnostics
    
    Performs detailed checks and returns diagnostic information
    """
    try:
        # Perform health check
        health_status = await memory_monitor.perform_health_check()
        
        # Get performance metrics
        metrics = await memory_monitor.get_performance_metrics()
        
        # Get usage statistics
        usage_stats = await memory_monitor.update_usage_statistics()
        
        # Analyze potential issues
        diagnostics = {
            "health_summary": {
                "overall_status": health_status.overall_status.value,
                "critical_issues": len(health_status.issues),
                "warnings": len(health_status.warnings)
            },
            "performance_analysis": {},
            "usage_analysis": {},
            "recommendations": []
        }
        
        # Analyze performance metrics
        for operation_type, metric_data in metrics.items():
            if metric_data['total_operations'] > 0:
                diagnostics["performance_analysis"][operation_type] = {
                    "status": "good" if metric_data['success_rate'] >= 95 else "needs_attention",
                    "success_rate": metric_data['success_rate'],
                    "average_response_time": metric_data['average_response_time']
                }
                
                # Add recommendations based on performance
                if metric_data['success_rate'] < 95:
                    diagnostics["recommendations"].append(
                        f"Low success rate for {operation_type} ({metric_data['success_rate']:.1f}%) - investigate error causes"
                    )
                
                if metric_data['average_response_time'] > 2.0:
                    diagnostics["recommendations"].append(
                        f"High response time for {operation_type} ({metric_data['average_response_time']:.2f}s) - consider optimization"
                    )
        
        # Analyze usage statistics
        diagnostics["usage_analysis"] = {
            "total_memories": usage_stats.total_memories,
            "storage_efficiency": "good" if usage_stats.storage_size_mb < 1000 else "monitor",
            "memory_distribution": usage_stats.memories_by_type
        }
        
        # Add usage-based recommendations
        if usage_stats.total_memories > 100000:
            diagnostics["recommendations"].append("High memory count - consider implementing cleanup policies")
        
        if usage_stats.storage_size_mb > 5000:  # 5GB
            diagnostics["recommendations"].append("Large storage usage - consider archiving old memories")
        
        return {
            "status": "success",
            "data": diagnostics
        }
        
    except Exception as e:
        logger.error(f"Diagnostics failed: {e}")
        raise HTTPException(status_code=500, detail=f"Diagnostics failed: {str(e)}")

@router.delete("/cleanup/test-memories")
async def cleanup_test_memories():
    """
    Clean up test memories created during health checks
    """
    try:
        from ..utils.neo4j_enhanced import Neo4jManager
        neo4j_manager = Neo4jManager()
        
        # Delete test memories (detach delete to remove relationships first)
        result = neo4j_manager.execute_query(
            "MATCH (m:Memory {memory_type: 'health_check'}) DETACH DELETE m RETURN count(m) as deleted",
            {}
        )
        
        deleted_count = result[0]['deleted'] if result else 0
        
        return {
            "status": "success",
            "message": f"Cleaned up {deleted_count} test memories"
        }
        
    except Exception as e:
        logger.error(f"Test memory cleanup failed: {e}")
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")

# Memory Lifecycle Management Endpoints

@router.get("/lifecycle/status")
async def get_lifecycle_status():
    """
    Get memory lifecycle management status
    """
    try:
        status = await memory_lifecycle_manager.get_lifecycle_status()
        
        return {
            "status": "success",
            "data": status
        }
        
    except Exception as e:
        logger.error(f"Failed to get lifecycle status: {e}")
        raise HTTPException(status_code=500, detail=f"Lifecycle status retrieval failed: {str(e)}")

@router.post("/lifecycle/start")
async def start_lifecycle_management(background_tasks: BackgroundTasks):
    """
    Start memory lifecycle management
    """
    try:
        if memory_lifecycle_manager._lifecycle_active:
            return {
                "status": "info",
                "message": "Memory lifecycle management is already active"
            }
        
        # Initialize lifecycle manager if not already done
        initialized = await memory_lifecycle_manager.initialize()
        if not initialized:
            raise HTTPException(status_code=500, detail="Failed to initialize lifecycle manager")
        
        # Start lifecycle management in background
        background_tasks.add_task(memory_lifecycle_manager.start_lifecycle_management)
        
        return {
            "status": "success",
            "message": "Memory lifecycle management started"
        }
        
    except Exception as e:
        logger.error(f"Failed to start lifecycle management: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start lifecycle management: {str(e)}")

@router.post("/lifecycle/stop")
async def stop_lifecycle_management():
    """
    Stop memory lifecycle management
    """
    try:
        await memory_lifecycle_manager.stop_lifecycle_management()
        
        return {
            "status": "success",
            "message": "Memory lifecycle management stopped"
        }
        
    except Exception as e:
        logger.error(f"Failed to stop lifecycle management: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to stop lifecycle management: {str(e)}")

@router.post("/lifecycle/maintenance")
async def run_manual_maintenance():
    """
    Run manual memory maintenance tasks
    """
    try:
        results = await memory_lifecycle_manager.run_daily_maintenance()
        
        return {
            "status": "success",
            "message": "Manual maintenance completed",
            "data": results
        }
        
    except Exception as e:
        logger.error(f"Manual maintenance failed: {e}")
        raise HTTPException(status_code=500, detail=f"Manual maintenance failed: {str(e)}")

@router.post("/lifecycle/decay")
async def apply_importance_decay():
    """
    Manually apply importance decay to memories
    """
    try:
        results = await memory_lifecycle_manager.apply_importance_decay()
        
        return {
            "status": "success",
            "message": "Importance decay applied",
            "data": results
        }
        
    except Exception as e:
        logger.error(f"Importance decay failed: {e}")
        raise HTTPException(status_code=500, detail=f"Importance decay failed: {str(e)}")

@router.post("/lifecycle/cleanup")
async def cleanup_memories():
    """
    Manually run memory cleanup
    """
    try:
        results = await memory_lifecycle_manager.cleanup_low_importance_memories()
        
        return {
            "status": "success",
            "message": "Memory cleanup completed",
            "data": {
                "total_processed": results.total_memories_processed,
                "archived": results.memories_archived,
                "deleted": results.memories_deleted,
                "storage_freed_mb": results.storage_freed_mb,
                "processing_time": results.processing_time_seconds
            }
        }
        
    except Exception as e:
        logger.error(f"Memory cleanup failed: {e}")
        raise HTTPException(status_code=500, detail=f"Memory cleanup failed: {str(e)}")

@router.post("/lifecycle/consolidate")
async def consolidate_memories():
    """
    Manually run memory consolidation
    """
    try:
        results = await memory_lifecycle_manager.consolidate_similar_memories()
        
        return {
            "status": "success",
            "message": "Memory consolidation completed",
            "data": results
        }
        
    except Exception as e:
        logger.error(f"Memory consolidation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Memory consolidation failed: {str(e)}")

@router.post("/lifecycle/optimize")
async def optimize_memory_storage():
    """
    Manually run memory storage optimization
    """
    try:
        results = await memory_lifecycle_manager.optimize_memory_storage()
        
        return {
            "status": "success",
            "message": "Memory storage optimization completed",
            "data": results
        }
        
    except Exception as e:
        logger.error(f"Memory optimization failed: {e}")
        raise HTTPException(status_code=500, detail=f"Memory optimization failed: {str(e)}")

@router.put("/lifecycle/configure")
async def configure_lifecycle_management(
    base_decay_rate: Optional[float] = None,
    min_importance_threshold: Optional[float] = None,
    max_memory_age_days: Optional[int] = None,
    similarity_threshold: Optional[float] = None,
    cleanup_batch_size: Optional[int] = None
):
    """
    Configure memory lifecycle management parameters
    """
    try:
        config_updates = {}
        
        if base_decay_rate is not None:
            memory_lifecycle_manager.config['base_decay_rate'] = max(0.1, min(1.0, base_decay_rate))
            config_updates['base_decay_rate'] = memory_lifecycle_manager.config['base_decay_rate']
        
        if min_importance_threshold is not None:
            memory_lifecycle_manager.config['min_importance_threshold'] = max(0.0, min(1.0, min_importance_threshold))
            config_updates['min_importance_threshold'] = memory_lifecycle_manager.config['min_importance_threshold']
        
        if max_memory_age_days is not None:
            memory_lifecycle_manager.config['max_memory_age_days'] = max(1, max_memory_age_days)
            config_updates['max_memory_age_days'] = memory_lifecycle_manager.config['max_memory_age_days']
        
        if similarity_threshold is not None:
            memory_lifecycle_manager.config['similarity_threshold'] = max(0.5, min(1.0, similarity_threshold))
            config_updates['similarity_threshold'] = memory_lifecycle_manager.config['similarity_threshold']
        
        if cleanup_batch_size is not None:
            memory_lifecycle_manager.config['cleanup_batch_size'] = max(10, min(10000, cleanup_batch_size))
            config_updates['cleanup_batch_size'] = memory_lifecycle_manager.config['cleanup_batch_size']
        
        return {
            "status": "success",
            "message": "Lifecycle configuration updated",
            "data": {
                "updated_parameters": config_updates,
                "current_configuration": memory_lifecycle_manager.config
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to configure lifecycle management: {e}")
        raise HTTPException(status_code=500, detail=f"Configuration failed: {str(e)}")

# Memory Search and Retrieval Endpoints

@router.post("/search", response_model=List[MemoryResponse])
async def search_memories(request: MemorySearchRequest):
    """
    Search memories using semantic similarity and filters
    
    Supports:
    - Semantic similarity search
    - User-specific filtering
    - Memory type filtering
    - Consciousness-aware search
    """
    try:
        retrieval_engine = MemoryRetrievalEngine()
        
        memories = await retrieval_engine.get_relevant_memories(
            query=request.query,
            user_id=request.user_id,
            consciousness_context=request.consciousness_context or {},
            limit=request.limit,
            similarity_threshold=request.similarity_threshold
        )
        
        # Convert to response format
        memory_responses = []
        for memory in memories:
            memory_responses.append(MemoryResponse(
                memory_id=memory.get('memory_id', ''),
                content=memory.get('content', ''),
                memory_type=memory.get('memory_type', ''),
                user_id=memory.get('user_id', ''),
                agent_name=memory.get('agent_name', ''),
                consciousness_level=memory.get('consciousness_level', 0.0),
                emotional_state=memory.get('emotional_state', ''),
                importance_score=memory.get('importance_score', 0.0),
                created_at=memory.get('created_at', ''),
                last_accessed=memory.get('last_accessed'),
                access_count=memory.get('access_count', 0),
                significance_score=memory.get('significance_score', 0.0)
            ))
        
        return memory_responses
        
    except Exception as e:
        logger.error(f"Memory search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Memory search failed: {str(e)}")

@router.get("/memories/{user_id}")
async def get_user_memories(
    user_id: str,
    limit: int = 50,
    memory_type: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """
    Get memories for a specific user with optional filtering
    """
    try:
        retrieval_engine = MemoryRetrievalEngine()
        
        # Build filter parameters
        filters = {"user_id": user_id}
        if memory_type:
            filters["memory_type"] = memory_type
        if start_date:
            filters["start_date"] = start_date
        if end_date:
            filters["end_date"] = end_date
        
        memories = await retrieval_engine.get_user_memories(
            user_id=user_id,
            limit=limit,
            filters=filters
        )
        
        return {
            "status": "success",
            "data": {
                "user_id": user_id,
                "memory_count": len(memories),
                "memories": memories
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get user memories: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get user memories: {str(e)}")

@router.get("/memories/{user_id}/conversation-history")
async def get_conversation_history(
    user_id: str,
    limit: int = 20,
    conversation_id: Optional[str] = None
):
    """
    Get conversation history for a user
    """
    try:
        retrieval_engine = MemoryRetrievalEngine()
        
        if conversation_id:
            # Get specific conversation
            memories = await retrieval_engine.get_conversation_memories(
                conversation_id=conversation_id,
                limit=limit
            )
        else:
            # Get recent conversation history
            memories = await retrieval_engine.get_conversation_history(
                user_id=user_id,
                limit=limit
            )
        
        return {
            "status": "success",
            "data": {
                "user_id": user_id,
                "conversation_id": conversation_id,
                "memory_count": len(memories),
                "memories": memories
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get conversation history: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get conversation history: {str(e)}")

@router.post("/memories/create")
async def create_memory(request: MemoryCreateRequest):
    """
    Create a new memory record
    """
    try:
        storage_engine = MemoryStorageEngine()
        
        # Create memory with provided data
        memory_id = await storage_engine.store_interaction_memory(
            user_query=request.content,
            agent_response="",  # For manual memory creation
            user_id=request.user_id,
            agent_name=request.agent_name,
            consciousness_context=request.consciousness_context or {}
        )
        
        return {
            "status": "success",
            "data": {
                "memory_id": memory_id,
                "message": "Memory created successfully"
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to create memory: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create memory: {str(e)}")

@router.get("/memories/{memory_id}/details")
async def get_memory_details(memory_id: str):
    """
    Get detailed information about a specific memory
    """
    try:
        retrieval_engine = MemoryRetrievalEngine()
        
        memory_details = await retrieval_engine.get_memory_by_id(memory_id)
        
        if not memory_details:
            raise HTTPException(status_code=404, detail="Memory not found")
        
        return {
            "status": "success",
            "data": memory_details
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get memory details: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get memory details: {str(e)}")

@router.post("/context/build")
async def build_memory_context(request: MemoryContextRequest):
    """
    Build memory context for a given query and user
    """
    try:
        retrieval_engine = MemoryRetrievalEngine()
        context_builder = MemoryContextBuilder()
        
        # Get relevant memories
        memories = await retrieval_engine.get_relevant_memories(
            query=request.query,
            user_id=request.user_id,
            consciousness_context=request.consciousness_context or {},
            limit=10
        )
        
        # Build context
        context = await context_builder.build_conversation_context(
            memories=memories,
            consciousness_context=request.consciousness_context or {}
        )
        
        return {
            "status": "success",
            "data": {
                "query": request.query,
                "user_id": request.user_id,
                "context_type": request.context_type,
                "memory_count": len(memories),
                "formatted_context": context,
                "memories_used": memories
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to build memory context: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to build memory context: {str(e)}")

@router.delete("/memories/{memory_id}")
async def delete_memory(memory_id: str):
    """
    Delete a specific memory (admin function)
    """
    try:
        from ..utils.neo4j_enhanced import Neo4jManager
        neo4j_manager = Neo4jManager()
        
        # Delete memory and its relationships
        result = neo4j_manager.execute_query(
            "MATCH (m:Memory {memory_id: $memory_id}) DETACH DELETE m RETURN count(m) as deleted",
            {"memory_id": memory_id}
        )
        
        deleted_count = result[0]['deleted'] if result else 0
        
        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="Memory not found")
        
        return {
            "status": "success",
            "message": f"Memory {memory_id} deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete memory: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete memory: {str(e)}")

@router.get("/statistics/overview")
async def get_memory_statistics():
    """
    Get comprehensive memory system statistics
    """
    try:
        from ..utils.neo4j_enhanced import Neo4jManager
        neo4j_manager = Neo4jManager()
        
        # Get various statistics
        stats_queries = {
            "total_memories": "MATCH (m:Memory) RETURN count(m) as count",
            "memories_by_type": "MATCH (m:Memory) RETURN m.memory_type as type, count(m) as count",
            "memories_by_user": "MATCH (m:Memory) RETURN m.user_id as user_id, count(m) as count ORDER BY count DESC LIMIT 10",
            "recent_memories": "MATCH (m:Memory) WHERE m.created_at > datetime() - duration('P7D') RETURN count(m) as count",
            "avg_importance": "MATCH (m:Memory) RETURN avg(m.importance_score) as avg_importance",
            "consciousness_levels": "MATCH (m:Memory) RETURN avg(m.consciousness_level) as avg_consciousness, min(m.consciousness_level) as min_consciousness, max(m.consciousness_level) as max_consciousness"
        }
        
        statistics = {}
        for stat_name, query in stats_queries.items():
            try:
                result = neo4j_manager.execute_query(query, {})
                statistics[stat_name] = result
            except Exception as e:
                logger.warning(f"Failed to get {stat_name}: {e}")
                statistics[stat_name] = None
        
        return {
            "status": "success",
            "data": statistics
        }
        
    except Exception as e:
        logger.error(f"Failed to get memory statistics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get memory statistics: {str(e)}")

@router.post("/admin/reindex")
async def reindex_memories():
    """
    Reindex all memories for better search performance (admin function)
    """
    try:
        from ..utils.memory_embedding_manager import MemoryEmbeddingManager
        embedding_manager = MemoryEmbeddingManager()
        
        # This would trigger a reindexing process
        result = await embedding_manager.reindex_all_memories()
        
        return {
            "status": "success",
            "message": "Memory reindexing completed",
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Memory reindexing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Memory reindexing failed: {str(e)}")

@router.post("/admin/validate")
async def validate_memory_integrity():
    """
    Validate memory system data integrity (admin function)
    """
    try:
        from ..utils.neo4j_enhanced import Neo4jManager
        neo4j_manager = Neo4jManager()
        
        validation_results = {
            "total_memories": 0,
            "memories_with_embeddings": 0,
            "memories_without_embeddings": 0,
            "orphaned_memories": 0,
            "duplicate_memories": 0,
            "validation_errors": []
        }
        
        # Check total memories
        result = neo4j_manager.execute_query("MATCH (m:Memory) RETURN count(m) as count", {})
        validation_results["total_memories"] = result[0]["count"] if result else 0
        
        # Check memories with embeddings
        result = neo4j_manager.execute_query(
            "MATCH (m:Memory) WHERE m.embedding IS NOT NULL RETURN count(m) as count", {}
        )
        validation_results["memories_with_embeddings"] = result[0]["count"] if result else 0
        
        # Check memories without embeddings
        result = neo4j_manager.execute_query(
            "MATCH (m:Memory) WHERE m.embedding IS NULL RETURN count(m) as count", {}
        )
        validation_results["memories_without_embeddings"] = result[0]["count"] if result else 0
        
        # Check for potential duplicates (same content and user)
        result = neo4j_manager.execute_query(
            """
            MATCH (m1:Memory), (m2:Memory) 
            WHERE m1.content = m2.content AND m1.user_id = m2.user_id AND m1.memory_id < m2.memory_id
            RETURN count(*) as count
            """, {}
        )
        validation_results["duplicate_memories"] = result[0]["count"] if result else 0
        
        # Add validation status
        if validation_results["memories_without_embeddings"] > 0:
            validation_results["validation_errors"].append(
                f"{validation_results['memories_without_embeddings']} memories missing embeddings"
            )
        
        if validation_results["duplicate_memories"] > 0:
            validation_results["validation_errors"].append(
                f"{validation_results['duplicate_memories']} potential duplicate memories found"
            )
        
        validation_results["status"] = "healthy" if not validation_results["validation_errors"] else "issues_found"
        
        return {
            "status": "success",
            "data": validation_results
        }
        
    except Exception as e:
        logger.error(f"Memory validation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Memory validation failed: {str(e)}")