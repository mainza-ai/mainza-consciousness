"""
Needs Router
Advanced API endpoints for needs management and consciousness integration
"""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from backend.utils.advanced_needs_generator import advanced_needs_generator, Need, NeedCategory
from backend.utils.needs_prioritization_engine import needs_prioritization_engine, PrioritizationContext
from backend.utils.consciousness_orchestrator_fixed import consciousness_orchestrator_fixed as consciousness_orchestrator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/needs", tags=["needs"])

class AdvancedNeedsRequest(BaseModel):
    """Request model for advanced needs generation"""
    user_id: str = "mainza-user"
    include_consciousness: bool = True
    include_growth: bool = True
    include_modification: bool = True
    include_emotional: bool = True
    include_reflection: bool = True
    max_needs: int = 5
    user_preferences: Optional[Dict[str, Any]] = None

class NeedUpdateRequest(BaseModel):
    """Request model for updating need progress"""
    need_id: str
    progress: float
    status: Optional[str] = None
    notes: Optional[str] = None

class NeedInteractionRequest(BaseModel):
    """Request model for need interactions"""
    need_id: str
    interaction_type: str  # 'click', 'complete', 'skip', 'favorite'
    user_id: str = "mainza-user"

@router.post("/advanced")
async def get_advanced_needs(request: AdvancedNeedsRequest):
    """
    Get advanced needs with full consciousness integration
    """
    try:
        logger.info(f"🧠 Generating advanced needs for user: {request.user_id}")
        
        # Generate needs using advanced generator
        needs = await advanced_needs_generator.generate_advanced_needs(
            user_id=request.user_id
        )
        
        # Get consciousness state for context
        consciousness_state = await consciousness_orchestrator.get_consciousness_state()
        
        # Build prioritization context
        prioritization_context = PrioritizationContext(
            consciousness_state=consciousness_state.__dict__ if hasattr(consciousness_state, '__dict__') else {},
            user_preferences=request.user_preferences or {},
            system_metrics={
                'health_score': 0.85,
                'performance_score': 0.78,
                'memory_usage': 0.65,
                'cpu_usage': 0.45
            },
            recent_activity=[],
            goal_alignment={},
            time_constraints={'urgency': 0.5}
        )
        
        # Prioritize needs
        prioritized_needs = await needs_prioritization_engine.prioritize_needs(
            needs, prioritization_context
        )
        
        # Convert to response format
        needs_response = []
        for need in prioritized_needs[:request.max_needs]:
            needs_response.append({
                'id': need.id,
                'title': need.title,
                'description': need.description,
                'category': need.category.value,
                'priority': need.priority,
                'progress': need.progress,
                'status': need.status,
                'created_at': need.created_at.isoformat() if need.created_at else None,
                'updated_at': need.updated_at.isoformat() if need.updated_at else None,
                'consciousness_context': need.consciousness_context,
                'related_goals': need.related_goals,
                'estimated_completion': need.estimated_completion.isoformat() if need.estimated_completion else None
            })
        
        return {
            'needs': needs_response,
            'consciousness_level': getattr(consciousness_state, 'consciousness_level', 0.7),
            'evolution_level': getattr(consciousness_state, 'evolution_level', 1),
            'emotional_state': getattr(consciousness_state, 'emotional_state', 'curious'),
            'total_needs_generated': len(needs),
            'needs_displayed': len(needs_response),
            'generated_at': datetime.now().isoformat(),
            'user_id': request.user_id
        }
        
    except Exception as e:
        logger.error(f"❌ Error generating advanced needs: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating advanced needs: {str(e)}")

@router.get("/categories")
async def get_need_categories():
    """
    Get available need categories
    """
    try:
        categories = [
            {
                'value': category.value,
                'label': category.value.replace('_', ' ').title(),
                'description': f"Needs related to {category.value.replace('_', ' ')}"
            }
            for category in NeedCategory
        ]
        
        return {
            'categories': categories,
            'total_categories': len(categories)
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting need categories: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting need categories: {str(e)}")

@router.post("/update")
async def update_need_progress(request: NeedUpdateRequest):
    """
    Update need progress and status
    """
    try:
        logger.info(f"📊 Updating need progress: {request.need_id}")
        
        # Update need in database
        query = """
        MATCH (n:Need {need_id: $need_id})
        SET n.progress = $progress,
            n.updated_at = datetime($updated_at)
        """
        
        if request.status:
            query += ", n.status = $status"
        
        if request.notes:
            query += ", n.notes = $notes"
        
        query += " RETURN n"
        
        from backend.utils.neo4j_production import neo4j_production
        result = neo4j_production.execute_query(
            query,
            parameters={
                'need_id': request.need_id,
                'progress': request.progress,
                'updated_at': datetime.now().isoformat(),
                'status': request.status,
                'notes': request.notes
            }
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="Need not found")
        
        return {
            'success': True,
            'need_id': request.need_id,
            'updated_progress': request.progress,
            'updated_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Error updating need progress: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating need progress: {str(e)}")

@router.post("/interact")
async def record_need_interaction(request: NeedInteractionRequest):
    """
    Record user interaction with a need
    """
    try:
        logger.info(f"👆 Recording need interaction: {request.interaction_type} for {request.need_id}")
        
        # Record interaction in database
        query = """
        MATCH (n:Need {need_id: $need_id})
        CREATE (i:NeedInteraction {
            interaction_id: $interaction_id,
            need_id: $need_id,
            user_id: $user_id,
            interaction_type: $interaction_type,
            timestamp: datetime($timestamp)
        })
        CREATE (n)-[:HAS_INTERACTION]->(i)
        RETURN i
        """
        
        from backend.utils.neo4j_production import neo4j_production
        result = neo4j_production.execute_query(
            query,
            parameters={
                'interaction_id': f"interaction_{datetime.now().timestamp()}",
                'need_id': request.need_id,
                'user_id': request.user_id,
                'interaction_type': request.interaction_type,
                'timestamp': datetime.now().isoformat()
            }
        )
        
        return {
            'success': True,
            'interaction_recorded': True,
            'interaction_type': request.interaction_type,
            'need_id': request.need_id,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Error recording need interaction: {e}")
        raise HTTPException(status_code=500, detail=f"Error recording need interaction: {str(e)}")

@router.get("/history/{user_id}")
async def get_need_history(user_id: str, limit: int = 20):
    """
    Get need history for a user
    """
    try:
        logger.info(f"📚 Getting need history for user: {user_id}")
        
        query = """
        MATCH (n:Need)
        WHERE n.created_at IS NOT NULL
        RETURN n
        ORDER BY n.created_at DESC
        LIMIT $limit
        """
        
        from backend.utils.neo4j_production import neo4j_production
        result = neo4j_production.execute_query(query, parameters={'limit': limit})
        
        needs_history = []
        for record in result:
            need = record['n']
            needs_history.append({
                'id': need.get('need_id'),
                'title': need.get('title'),
                'description': need.get('description'),
                'category': need.get('category'),
                'priority': need.get('priority'),
                'progress': need.get('progress'),
                'status': need.get('status'),
                'created_at': need.get('created_at'),
                'updated_at': need.get('updated_at')
            })
        
        return {
            'needs_history': needs_history,
            'total_count': len(needs_history),
            'user_id': user_id
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting need history: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting need history: {str(e)}")

@router.get("/analytics/{user_id}")
async def get_need_analytics(user_id: str):
    """
    Get need analytics for a user
    """
    try:
        logger.info(f"📊 Getting need analytics for user: {user_id}")
        
        # Get need statistics
        query = """
        MATCH (n:Need)
        RETURN 
            count(n) as total_needs,
            avg(n.priority) as avg_priority,
            avg(n.progress) as avg_progress,
            count(CASE WHEN n.status = 'completed' THEN 1 END) as completed_needs,
            count(CASE WHEN n.status = 'active' THEN 1 END) as active_needs
        """
        
        from backend.utils.neo4j_production import neo4j_production
        result = await neo4j_production.execute_query(query)
        
        if result:
            stats = result[0]
            analytics = {
                'total_needs': stats.get('total_needs', 0),
                'average_priority': round(stats.get('avg_priority', 0), 2),
                'average_progress': round(stats.get('avg_progress', 0), 2),
                'completed_needs': stats.get('completed_needs', 0),
                'active_needs': stats.get('active_needs', 0),
                'completion_rate': round(
                    stats.get('completed_needs', 0) / max(stats.get('total_needs', 1), 1) * 100, 2
                )
            }
        else:
            analytics = {
                'total_needs': 0,
                'average_priority': 0,
                'average_progress': 0,
                'completed_needs': 0,
                'active_needs': 0,
                'completion_rate': 0
            }
        
        return {
            'analytics': analytics,
            'user_id': user_id,
            'generated_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting need analytics: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting need analytics: {str(e)}")

@router.delete("/{need_id}")
async def delete_need(need_id: str):
    """
    Delete a specific need
    """
    try:
        logger.info(f"🗑️ Deleting need: {need_id}")
        
        query = """
        MATCH (n:Need {need_id: $need_id})
        DETACH DELETE n
        RETURN count(n) as deleted_count
        """
        
        from backend.utils.neo4j_production import neo4j_production
        result = neo4j_production.execute_query(query, parameters={'need_id': need_id})
        
        if result and result[0].get('deleted_count', 0) > 0:
            return {
                'success': True,
                'need_id': need_id,
                'deleted_at': datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=404, detail="Need not found")
        
    except Exception as e:
        logger.error(f"❌ Error deleting need: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting need: {str(e)}")
