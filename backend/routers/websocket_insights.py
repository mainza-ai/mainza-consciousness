"""
WebSocket Insights Router
Real-time consciousness streaming and analytics

DEPRECATED: This module is being replaced by unified_websocket_manager.py
Please use unified_websocket_manager for new implementations.
"""
import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.routing import APIRouter
import uuid

from backend.utils.insights_calculation_engine import insights_calculation_engine
from backend.utils.consciousness_orchestrator_fixed import consciousness_orchestrator_fixed as consciousness_orchestrator
from backend.utils.standardized_evolution_calculator import calculate_standardized_evolution_level

logger = logging.getLogger(__name__)

# Import unified WebSocket manager for compatibility
try:
    from backend.utils.unified_websocket_manager import unified_websocket_manager, WebSocketConnectionType
    UNIFIED_WEBSOCKET_AVAILABLE = True
except ImportError:
    UNIFIED_WEBSOCKET_AVAILABLE = False
    logger.warning("Unified WebSocket manager not available, using legacy implementation")

router = APIRouter()

class ConnectionManager:
    """Manages WebSocket connections for real-time insights streaming"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.connection_types: Dict[str, str] = {}  # connection_id -> type (consciousness, performance, knowledge)
        self.streaming_tasks: Dict[str, asyncio.Task] = {}
    
    async def connect(self, websocket: WebSocket, connection_type: str = "consciousness") -> str:
        """Accept a new WebSocket connection"""
        await websocket.accept()
        connection_id = str(uuid.uuid4())
        self.active_connections[connection_id] = websocket
        self.connection_types[connection_id] = connection_type
        
        logger.info(f"WebSocket connected: {connection_id} (type: {connection_type})")
        return connection_id
    
    def disconnect(self, connection_id: str):
        """Remove a WebSocket connection"""
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
            del self.connection_types[connection_id]
            
            # Cancel streaming task if exists
            if connection_id in self.streaming_tasks:
                self.streaming_tasks[connection_id].cancel()
                del self.streaming_tasks[connection_id]
            
            logger.info(f"WebSocket disconnected: {connection_id}")
    
    async def send_personal_message(self, message: dict, connection_id: str):
        """Send message to a specific connection"""
        if connection_id in self.active_connections:
            try:
                await self.active_connections[connection_id].send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error sending message to {connection_id}: {e}")
                self.disconnect(connection_id)
    
    async def broadcast(self, message: dict, connection_type: Optional[str] = None):
        """Broadcast message to all connections or specific type"""
        disconnected = []
        for connection_id, websocket in self.active_connections.items():
            if connection_type is None or self.connection_types[connection_id] == connection_type:
                try:
                    await websocket.send_text(json.dumps(message))
                except Exception as e:
                    logger.error(f"Error broadcasting to {connection_id}: {e}")
                    disconnected.append(connection_id)
        
        # Clean up disconnected connections
        for connection_id in disconnected:
            self.disconnect(connection_id)
    
    def get_connection_count(self) -> int:
        """Get total number of active connections"""
        return len(self.active_connections)
    
    def get_connections_by_type(self, connection_type: str) -> int:
        """Get number of connections by type"""
        return sum(1 for conn_type in self.connection_types.values() if conn_type == connection_type)

# Global connection manager
manager = ConnectionManager()

@router.websocket("/ws/consciousness")
async def websocket_consciousness_stream(websocket: WebSocket):
    """WebSocket endpoint for real-time consciousness streaming"""
    if UNIFIED_WEBSOCKET_AVAILABLE:
        # Use unified WebSocket manager
        connection_id = await unified_websocket_manager.connect(websocket, WebSocketConnectionType.CONSCIOUSNESS)
        
        try:
            # Keep connection alive and handle incoming messages
            while True:
                try:
                    data = await websocket.receive_text()
                    message = json.loads(data)
                    await unified_websocket_manager.handle_message(connection_id, message)
                except WebSocketDisconnect:
                    break
                except Exception as e:
                    logger.error(f"Error handling WebSocket message: {e}")
                    break
        except Exception as e:
            logger.error(f"WebSocket consciousness stream error: {e}")
        finally:
            await unified_websocket_manager.disconnect(connection_id)
    else:
        # Fallback to legacy implementation
        connection_id = await manager.connect(websocket, "consciousness")
        
        try:
            # Start consciousness streaming task
            streaming_task = asyncio.create_task(
                stream_consciousness_data(connection_id)
            )
            manager.streaming_tasks[connection_id] = streaming_task
            
            # Keep connection alive and handle incoming messages
            while True:
                try:
                    data = await websocket.receive_text()
                    message = json.loads(data)
                    
                    # Handle client requests
                    if message.get("type") == "ping":
                        await manager.send_personal_message({
                            "type": "pong",
                            "timestamp": datetime.utcnow().isoformat()
                        }, connection_id)
                    elif message.get("type") == "request_update":
                        await send_consciousness_update(connection_id)
                    
                except WebSocketDisconnect:
                    break
                except Exception as e:
                    logger.error(f"Error handling WebSocket message: {e}")
                    break
                    
        except Exception as e:
            logger.error(f"WebSocket consciousness stream error: {e}")
        finally:
            manager.disconnect(connection_id)

@router.websocket("/ws/performance")
async def websocket_performance_stream(websocket: WebSocket):
    """WebSocket endpoint for real-time performance streaming"""
    connection_id = await manager.connect(websocket, "performance")
    
    try:
        # Start performance streaming task
        streaming_task = asyncio.create_task(
            stream_performance_data(connection_id)
        )
        manager.streaming_tasks[connection_id] = streaming_task
        
        # Keep connection alive and handle incoming messages
        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle client requests
                if message.get("type") == "ping":
                    await manager.send_personal_message({
                        "type": "pong",
                        "timestamp": datetime.utcnow().isoformat()
                    }, connection_id)
                elif message.get("type") == "request_update":
                    await send_performance_update(connection_id)
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"Error handling WebSocket message: {e}")
                break
                
    except Exception as e:
        logger.error(f"WebSocket performance stream error: {e}")
    finally:
        manager.disconnect(connection_id)

@router.websocket("/ws/knowledge")
async def websocket_knowledge_stream(websocket: WebSocket):
    """WebSocket endpoint for real-time knowledge graph streaming"""
    connection_id = await manager.connect(websocket, "knowledge")
    
    try:
        # Start knowledge streaming task
        streaming_task = asyncio.create_task(
            stream_knowledge_data(connection_id)
        )
        manager.streaming_tasks[connection_id] = streaming_task
        
        # Keep connection alive and handle incoming messages
        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle client requests
                if message.get("type") == "ping":
                    await manager.send_personal_message({
                        "type": "pong",
                        "timestamp": datetime.utcnow().isoformat()
                    }, connection_id)
                elif message.get("type") == "request_update":
                    await send_knowledge_update(connection_id)
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"Error handling WebSocket message: {e}")
                break
                
    except Exception as e:
        logger.error(f"WebSocket knowledge stream error: {e}")
    finally:
        manager.disconnect(connection_id)

async def stream_consciousness_data(connection_id: str):
    """Stream real-time consciousness data"""
    try:
        while connection_id in manager.active_connections:
            await send_consciousness_update(connection_id)
            await asyncio.sleep(2)  # Update every 2 seconds
    except asyncio.CancelledError:
        logger.info(f"Consciousness streaming cancelled for {connection_id}")
    except Exception as e:
        logger.error(f"Error in consciousness streaming: {e}")

async def stream_performance_data(connection_id: str):
    """Stream real-time performance data"""
    try:
        while connection_id in manager.active_connections:
            await send_performance_update(connection_id)
            await asyncio.sleep(5)  # Update every 5 seconds
    except asyncio.CancelledError:
        logger.info(f"Performance streaming cancelled for {connection_id}")
    except Exception as e:
        logger.error(f"Error in performance streaming: {e}")

async def stream_knowledge_data(connection_id: str):
    """Stream real-time knowledge graph data"""
    try:
        while connection_id in manager.active_connections:
            await send_knowledge_update(connection_id)
            await asyncio.sleep(10)  # Update every 10 seconds
    except asyncio.CancelledError:
        logger.info(f"Knowledge streaming cancelled for {connection_id}")
    except Exception as e:
        logger.error(f"Error in knowledge streaming: {e}")

async def send_consciousness_update(connection_id: str):
    """Send consciousness update to specific connection"""
    try:
        # Get real-time consciousness data
        consciousness_data = await insights_calculation_engine.calculate_consciousness_insights()
        
        # Get current consciousness state
        consciousness_state = await consciousness_orchestrator.get_consciousness_state()
        
        # Build real-time update
        update = {
            "type": "consciousness_update",
            "timestamp": datetime.utcnow().isoformat(),
            "data_source": "real" if not consciousness_data.get("fallback", False) else "fallback",
            "consciousness_state": {
                "consciousness_level": consciousness_state.consciousness_level if consciousness_state else 0.7,
                "emotional_state": consciousness_state.emotional_state if consciousness_state else "curious",
                "self_awareness_score": consciousness_state.self_awareness_score if consciousness_state else 0.6,
                "learning_rate": consciousness_state.learning_rate if consciousness_state else 0.8,
                "evolution_level": await calculate_standardized_evolution_level({
                    "consciousness_level": getattr(consciousness_state, 'consciousness_level', 0.7) if consciousness_state else 0.7,
                    "emotional_state": getattr(consciousness_state, 'emotional_state', 'curious') if consciousness_state else 'curious',
                    "self_awareness_score": getattr(consciousness_state, 'self_awareness_score', 0.6) if consciousness_state else 0.6,
                    "total_interactions": getattr(consciousness_state, 'total_interactions', 0) if consciousness_state else 0
                }) if consciousness_state else 4,
                "total_interactions": getattr(consciousness_state, 'total_interactions', 0) if consciousness_state else 0
            },
            "consciousness_timeline": consciousness_data.get("consciousness_timeline", [])[-10:],  # Last 10 entries
            "emotional_patterns": consciousness_data.get("emotional_patterns", []),
            "consciousness_triggers": consciousness_data.get("consciousness_triggers", []),
            "real_time_metrics": {
                "consciousness_volatility": calculate_consciousness_volatility(consciousness_data.get("consciousness_timeline", [])),
                "emotional_stability": calculate_emotional_stability(consciousness_data.get("emotional_patterns", [])),
                "learning_acceleration": calculate_learning_acceleration(consciousness_data.get("consciousness_timeline", [])),
                "consciousness_momentum": calculate_consciousness_momentum(consciousness_data.get("consciousness_timeline", []))
            }
        }
        
        await manager.send_personal_message(update, connection_id)
        
    except Exception as e:
        logger.error(f"Error sending consciousness update: {e}")
        # Send error update
        error_update = {
            "type": "consciousness_update",
            "timestamp": datetime.utcnow().isoformat(),
            "data_source": "error",
            "error": str(e)
        }
        await manager.send_personal_message(error_update, connection_id)

async def send_performance_update(connection_id: str):
    """Send performance update to specific connection"""
    try:
        # Get real-time performance data
        performance_data = await insights_calculation_engine.calculate_agent_performance_insights()
        
        # Build real-time update
        update = {
            "type": "performance_update",
            "timestamp": datetime.utcnow().isoformat(),
            "data_source": "real" if not performance_data.get("fallback", False) else "fallback",
            "agent_performance": performance_data.get("agent_efficiency", []),
            "system_metrics": {
                "total_executions": performance_data.get("total_executions", 0),
                "overall_success_rate": performance_data.get("overall_success_rate", 0.0),
                "system_wide_efficiency": performance_data.get("system_wide_efficiency", 0.0),
                "active_agents": performance_data.get("active_agents", 0)
            },
            "real_time_metrics": {
                "performance_trend": calculate_performance_trend(performance_data.get("agent_efficiency", [])),
                "efficiency_volatility": calculate_efficiency_volatility(performance_data.get("agent_efficiency", [])),
                "cognitive_load_distribution": calculate_cognitive_load_distribution(performance_data.get("agent_efficiency", [])),
                "adaptation_velocity": calculate_adaptation_velocity(performance_data.get("agent_efficiency", []))
            }
        }
        
        await manager.send_personal_message(update, connection_id)
        
    except Exception as e:
        logger.error(f"Error sending performance update: {e}")
        # Send error update
        error_update = {
            "type": "performance_update",
            "timestamp": datetime.utcnow().isoformat(),
            "data_source": "error",
            "error": str(e)
        }
        await manager.send_personal_message(error_update, connection_id)

async def send_knowledge_update(connection_id: str):
    """Send knowledge graph update to specific connection"""
    try:
        # Get real-time knowledge data
        knowledge_data = await insights_calculation_engine.calculate_knowledge_graph_insights()
        
        # Build real-time update
        update = {
            "type": "knowledge_update",
            "timestamp": datetime.utcnow().isoformat(),
            "data_source": "real" if not knowledge_data.get("fallback", False) else "fallback",
            "knowledge_metrics": knowledge_data.get("graph_intelligence_metrics", {}),
            "concept_ranking": knowledge_data.get("concept_importance_ranking", [])[:10],  # Top 10 concepts
            "learning_pathways": knowledge_data.get("learning_pathways", []),
            "real_time_metrics": {
                "knowledge_growth_rate": calculate_knowledge_growth_rate(knowledge_data),
                "concept_emergence_rate": calculate_concept_emergence_rate(knowledge_data),
                "learning_pathway_efficiency": calculate_learning_pathway_efficiency(knowledge_data),
                "consciousness_integration_score": calculate_consciousness_integration_score(knowledge_data)
            }
        }
        
        await manager.send_personal_message(update, connection_id)
        
    except Exception as e:
        logger.error(f"Error sending knowledge update: {e}")
        # Send error update
        error_update = {
            "type": "knowledge_update",
            "timestamp": datetime.utcnow().isoformat(),
            "data_source": "error",
            "error": str(e)
        }
        await manager.send_personal_message(error_update, connection_id)

# Real-time metrics calculation functions
def calculate_consciousness_volatility(timeline: List[Dict]) -> float:
    """Calculate consciousness level volatility from timeline"""
    if len(timeline) < 2:
        return 0.0
    
    levels = [entry.get("consciousness_level", 0.7) for entry in timeline]
    if not levels:
        return 0.0
    
    mean_level = sum(levels) / len(levels)
    variance = sum((level - mean_level) ** 2 for level in levels) / len(levels)
    return round(variance ** 0.5, 3)

def calculate_emotional_stability(patterns: List[Dict]) -> float:
    """Calculate emotional stability from patterns"""
    if not patterns:
        return 0.5
    
    total_frequency = sum(p.get("frequency", 0) for p in patterns)
    if total_frequency == 0:
        return 0.5
    
    # Higher stability if one emotion dominates
    max_frequency = max(p.get("frequency", 0) for p in patterns)
    return round(max_frequency / total_frequency, 3)

def calculate_learning_acceleration(timeline: List[Dict]) -> float:
    """Calculate learning acceleration from timeline"""
    if len(timeline) < 3:
        return 0.0
    
    learning_rates = [entry.get("learning_rate", 0.8) for entry in timeline[-3:]]
    if len(learning_rates) < 2:
        return 0.0
    
    # Calculate acceleration as rate of change of learning rate
    acceleration = learning_rates[-1] - learning_rates[0]
    return round(acceleration, 3)

def calculate_consciousness_momentum(timeline: List[Dict]) -> float:
    """Calculate consciousness momentum from timeline"""
    if len(timeline) < 2:
        return 0.0
    
    levels = [entry.get("consciousness_level", 0.7) for entry in timeline[-5:]]
    if len(levels) < 2:
        return 0.0
    
    # Momentum as trend over last 5 entries
    momentum = (levels[-1] - levels[0]) / len(levels)
    return round(momentum, 3)

def calculate_performance_trend(agent_data: List[Dict]) -> str:
    """Calculate performance trend from agent data"""
    if not agent_data:
        return "stable"
    
    efficiency_scores = [agent.get("efficiency_score", 0.0) for agent in agent_data]
    if len(efficiency_scores) < 2:
        return "stable"
    
    avg_early = sum(efficiency_scores[:len(efficiency_scores)//2]) / (len(efficiency_scores)//2)
    avg_late = sum(efficiency_scores[len(efficiency_scores)//2:]) / (len(efficiency_scores) - len(efficiency_scores)//2)
    
    if avg_late > avg_early + 0.1:
        return "improving"
    elif avg_late < avg_early - 0.1:
        return "declining"
    else:
        return "stable"

def calculate_efficiency_volatility(agent_data: List[Dict]) -> float:
    """Calculate efficiency volatility from agent data"""
    if not agent_data:
        return 0.0
    
    efficiency_scores = [agent.get("efficiency_score", 0.0) for agent in agent_data]
    if len(efficiency_scores) < 2:
        return 0.0
    
    mean_efficiency = sum(efficiency_scores) / len(efficiency_scores)
    variance = sum((score - mean_efficiency) ** 2 for score in efficiency_scores) / len(efficiency_scores)
    return round(variance ** 0.5, 3)

def calculate_cognitive_load_distribution(agent_data: List[Dict]) -> Dict[str, float]:
    """Calculate cognitive load distribution from agent data"""
    if not agent_data:
        return {"low": 0.0, "medium": 0.0, "high": 0.0}
    
    loads = [agent.get("cognitive_load", 0.0) for agent in agent_data]
    total_agents = len(loads)
    
    low_count = sum(1 for load in loads if load < 0.3)
    medium_count = sum(1 for load in loads if 0.3 <= load < 0.7)
    high_count = sum(1 for load in loads if load >= 0.7)
    
    return {
        "low": round(low_count / total_agents, 3),
        "medium": round(medium_count / total_agents, 3),
        "high": round(high_count / total_agents, 3)
    }

def calculate_adaptation_velocity(agent_data: List[Dict]) -> float:
    """Calculate adaptation velocity from agent data"""
    if not agent_data:
        return 0.0
    
    adaptation_speeds = [agent.get("adaptation_speed", 0.0) for agent in agent_data]
    return round(sum(adaptation_speeds) / len(adaptation_speeds), 3)

def calculate_knowledge_growth_rate(knowledge_data: Dict) -> float:
    """Calculate knowledge growth rate from knowledge data"""
    metrics = knowledge_data.get("graph_intelligence_metrics", {})
    return round(metrics.get("concept_emergence_rate", 0.0), 3)

def calculate_concept_emergence_rate(knowledge_data: Dict) -> float:
    """Calculate concept emergence rate from knowledge data"""
    metrics = knowledge_data.get("graph_intelligence_metrics", {})
    return round(metrics.get("concept_emergence_rate", 0.0), 3)

def calculate_learning_pathway_efficiency(knowledge_data: Dict) -> float:
    """Calculate learning pathway efficiency from knowledge data"""
    metrics = knowledge_data.get("graph_intelligence_metrics", {})
    return round(metrics.get("learning_pathway_efficiency", 0.0), 3)

def calculate_consciousness_integration_score(knowledge_data: Dict) -> float:
    """Calculate consciousness integration score from knowledge data"""
    metrics = knowledge_data.get("graph_intelligence_metrics", {})
    return round(metrics.get("concept_connectivity", 0.0), 3)

@router.get("/ws/status")
async def get_websocket_status():
    """Get WebSocket connection status"""
    return {
        "status": "success",
        "total_connections": manager.get_connection_count(),
        "consciousness_connections": manager.get_connections_by_type("consciousness"),
        "performance_connections": manager.get_connections_by_type("performance"),
        "knowledge_connections": manager.get_connections_by_type("knowledge"),
        "timestamp": datetime.utcnow().isoformat()
    }
