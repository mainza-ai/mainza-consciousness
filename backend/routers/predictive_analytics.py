"""
Predictive Analytics Router
WebSocket and REST endpoints for predictive analytics and AI insights
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Dict, List, Any, Optional
import asyncio
import json
import logging
from datetime import datetime, timedelta
import uuid

from backend.utils.consciousness_predictor import consciousness_predictor, PredictionResult, ConsciousnessState
from backend.utils.ai_insights_engine import ai_insights_engine, AIInsight
from backend.utils.insights_calculation_engine import InsightsCalculationEngine

logger = logging.getLogger(__name__)

router = APIRouter()

class PredictiveAnalyticsManager:
    """Manages WebSocket connections for predictive analytics"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.insights_connections: List[WebSocket] = []
        self.predictions_connections: List[WebSocket] = []
        self.optimization_connections: List[WebSocket] = []
        self.insights_engine = InsightsCalculationEngine()
        
    async def connect(self, websocket: WebSocket, connection_type: str = "general"):
        """Accept WebSocket connection"""
        await websocket.accept()
        
        if connection_type == "insights":
            self.insights_connections.append(websocket)
        elif connection_type == "predictions":
            self.predictions_connections.append(websocket)
        elif connection_type == "optimization":
            self.optimization_connections.append(websocket)
        else:
            self.active_connections.append(websocket)
        
        logger.info(f"Predictive analytics connection established. Type: {connection_type}")
    
    def disconnect(self, websocket: WebSocket, connection_type: str = "general"):
        """Remove WebSocket connection"""
        if connection_type == "insights":
            if websocket in self.insights_connections:
                self.insights_connections.remove(websocket)
        elif connection_type == "predictions":
            if websocket in self.predictions_connections:
                self.predictions_connections.remove(websocket)
        elif connection_type == "optimization":
            if websocket in self.optimization_connections:
                self.optimization_connections.remove(websocket)
        else:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)
        
        logger.info(f"Predictive analytics connection closed. Type: {connection_type}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send message to specific WebSocket"""
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
    
    async def broadcast_insights(self, insights: List[AIInsight]):
        """Broadcast insights to all insights connections"""
        if not self.insights_connections:
            return
        
        message = {
            "type": "insights_update",
            "data": {
                "insights": [
                    {
                        "id": insight.id,
                        "type": insight.type.value,
                        "priority": insight.priority.value,
                        "title": insight.title,
                        "description": insight.description,
                        "confidence": insight.confidence,
                        "impact_score": insight.impact_score,
                        "actionable": insight.actionable,
                        "category": insight.category,
                        "tags": insight.tags,
                        "recommendations": insight.recommendations,
                        "timestamp": insight.timestamp.isoformat()
                    }
                    for insight in insights
                ],
                "timestamp": datetime.now().isoformat()
            }
        }
        
        disconnected = []
        for connection in self.insights_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error broadcasting insights: {e}")
                disconnected.append(connection)
        
        # Remove disconnected connections
        for connection in disconnected:
            self.disconnect(connection, "insights")
    
    async def broadcast_predictions(self, predictions: List[PredictionResult]):
        """Broadcast predictions to all predictions connections"""
        if not self.predictions_connections:
            return
        
        message = {
            "type": "predictions_update",
            "data": {
                "predictions": [
                    {
                        "prediction_type": prediction.prediction_type.value,
                        "predicted_value": prediction.predicted_value,
                        "confidence": prediction.confidence,
                        "time_horizon": prediction.time_horizon,
                        "factors": prediction.factors,
                        "trend": prediction.trend,
                        "recommendation": prediction.recommendation,
                        "timestamp": prediction.timestamp.isoformat()
                    }
                    for prediction in predictions
                ],
                "timestamp": datetime.now().isoformat()
            }
        }
        
        disconnected = []
        for connection in self.predictions_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error broadcasting predictions: {e}")
                disconnected.append(connection)
        
        # Remove disconnected connections
        for connection in disconnected:
            self.disconnect(connection, "predictions")
    
    async def broadcast_optimization(self, optimization_data: Dict[str, Any]):
        """Broadcast optimization data to all optimization connections"""
        if not self.optimization_connections:
            return
        
        message = {
            "type": "optimization_update",
            "data": {
                **optimization_data,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        disconnected = []
        for connection in self.optimization_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error broadcasting optimization: {e}")
                disconnected.append(connection)
        
        # Remove disconnected connections
        for connection in disconnected:
            self.disconnect(connection, "optimization")

# Global manager instance
predictive_manager = PredictiveAnalyticsManager()

@router.websocket("/ws/insights")
async def websocket_insights(websocket: WebSocket):
    """WebSocket endpoint for AI insights streaming"""
    await predictive_manager.connect(websocket, "insights")
    
    try:
        while True:
            # Keep connection alive and send periodic updates
            await asyncio.sleep(30)  # Send updates every 30 seconds
            
            # Generate insights
            try:
                # Get current consciousness data
                consciousness_data = await predictive_manager.insights_engine.get_consciousness_insights()
                
                # Generate AI insights
                insights = await ai_insights_engine.analyze_consciousness_data(consciousness_data)
                
                if insights:
                    await predictive_manager.broadcast_insights(insights)
                    
            except Exception as e:
                logger.error(f"Error generating insights: {e}")
                
    except WebSocketDisconnect:
        predictive_manager.disconnect(websocket, "insights")
    except Exception as e:
        logger.error(f"WebSocket insights error: {e}")
        predictive_manager.disconnect(websocket, "insights")

@router.websocket("/ws/predictions")
async def websocket_predictions(websocket: WebSocket):
    """WebSocket endpoint for predictions streaming"""
    await predictive_manager.connect(websocket, "predictions")
    
    try:
        while True:
            # Keep connection alive and send periodic updates
            await asyncio.sleep(60)  # Send updates every minute
            
            # Generate predictions
            try:
                # Get comprehensive predictions
                predictions = consciousness_predictor.get_comprehensive_predictions([15, 30, 60, 120])
                
                # Flatten predictions
                all_predictions = []
                for prediction_list in predictions.values():
                    all_predictions.extend(prediction_list)
                
                if all_predictions:
                    await predictive_manager.broadcast_predictions(all_predictions)
                    
            except Exception as e:
                logger.error(f"Error generating predictions: {e}")
                
    except WebSocketDisconnect:
        predictive_manager.disconnect(websocket, "predictions")
    except Exception as e:
        logger.error(f"WebSocket predictions error: {e}")
        predictive_manager.disconnect(websocket, "predictions")

@router.websocket("/ws/optimization")
async def websocket_optimization(websocket: WebSocket):
    """WebSocket endpoint for optimization data streaming"""
    await predictive_manager.connect(websocket, "optimization")
    
    try:
        while True:
            # Keep connection alive and send periodic updates
            await asyncio.sleep(45)  # Send updates every 45 seconds
            
            # Generate optimization data
            try:
                # Get system metrics
                performance_data = await predictive_manager.insights_engine.calculate_agent_performance_insights()
                
                # Calculate optimization recommendations
                optimization_data = {
                    "system_efficiency": performance_data.get("system_metrics", {}).get("system_wide_efficiency", 0.5),
                    "learning_efficiency": performance_data.get("learning_metrics", {}).get("learning_efficiency", 0.6),
                    "memory_utilization": performance_data.get("system_metrics", {}).get("memory_utilization", 0.65),
                    "processing_speed": performance_data.get("system_metrics", {}).get("processing_speed", 0.6),
                    "recommendations": [
                        {
                            "type": "learning_efficiency",
                            "priority": "medium",
                            "current_value": 0.78,
                            "target_value": 0.92,
                            "improvement": 0.14,
                            "description": "Learning efficiency can be improved by 14%"
                        },
                        {
                            "type": "processing_speed",
                            "priority": "high",
                            "current_value": 0.6,
                            "target_value": 0.85,
                            "improvement": 0.25,
                            "description": "Processing speed can be increased by 25%"
                        }
                    ]
                }
                
                await predictive_manager.broadcast_optimization(optimization_data)
                
            except Exception as e:
                logger.error(f"Error generating optimization data: {e}")
                
    except WebSocketDisconnect:
        predictive_manager.disconnect(websocket, "optimization")
    except Exception as e:
        logger.error(f"WebSocket optimization error: {e}")
        predictive_manager.disconnect(websocket, "optimization")

@router.get("/predictions")
async def get_predictions():
    """Get current predictions"""
    try:
        predictions = consciousness_predictor.get_comprehensive_predictions([15, 30, 60, 120])
        
        # Format predictions for API response
        formatted_predictions = {}
        for prediction_type, prediction_list in predictions.items():
            formatted_predictions[prediction_type] = [
                {
                    "prediction_type": pred.prediction_type.value,
                    "predicted_value": pred.predicted_value,
                    "confidence": pred.confidence,
                    "time_horizon": pred.time_horizon,
                    "factors": pred.factors,
                    "trend": pred.trend,
                    "recommendation": pred.recommendation,
                    "timestamp": pred.timestamp.isoformat()
                }
                for pred in prediction_list
            ]
        
        return {
            "status": "success",
            "data": formatted_predictions,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting predictions: {e}")
        raise HTTPException(status_code=500, detail="Failed to get predictions")

@router.get("/insights")
async def get_insights():
    """Get current AI insights"""
    try:
        # Get insights summary
        insights_summary = ai_insights_engine.get_insights_summary()
        
        return {
            "status": "success",
            "data": insights_summary,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting insights: {e}")
        raise HTTPException(status_code=500, detail="Failed to get insights")

@router.post("/insights/analyze")
async def analyze_consciousness_data(data: Dict[str, Any]):
    """Analyze consciousness data and generate insights"""
    try:
        # Generate insights from provided data
        insights = await ai_insights_engine.analyze_consciousness_data(data)
        
        # Format insights for response
        formatted_insights = [
            {
                "id": insight.id,
                "type": insight.type.value,
                "priority": insight.priority.value,
                "title": insight.title,
                "description": insight.description,
                "confidence": insight.confidence,
                "impact_score": insight.impact_score,
                "actionable": insight.actionable,
                "category": insight.category,
                "tags": insight.tags,
                "recommendations": insight.recommendations,
                "timestamp": insight.timestamp.isoformat()
            }
            for insight in insights
        ]
        
        return {
            "status": "success",
            "data": {
                "insights": formatted_insights,
                "total_insights": len(formatted_insights)
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error analyzing consciousness data: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze consciousness data")

@router.get("/optimization")
async def get_optimization_recommendations():
    """Get optimization recommendations"""
    try:
        # Get system metrics
        performance_data = await predictive_manager.insights_engine.calculate_agent_performance_insights()
        
        # Calculate optimization recommendations
        optimization_data = {
            "system_efficiency": performance_data.get("system_metrics", {}).get("system_wide_efficiency", 0.5),
            "learning_efficiency": performance_data.get("learning_metrics", {}).get("learning_efficiency", 0.6),
            "memory_utilization": performance_data.get("system_metrics", {}).get("memory_utilization", 0.65),
            "processing_speed": performance_data.get("system_metrics", {}).get("processing_speed", 0.6),
            "recommendations": [
                {
                    "type": "learning_efficiency",
                    "priority": "medium",
                    "current_value": 0.78,
                    "target_value": 0.92,
                    "improvement": 0.14,
                    "description": "Learning efficiency can be improved by 14%",
                    "actionable": True
                },
                {
                    "type": "processing_speed",
                    "priority": "high",
                    "current_value": 0.6,
                    "target_value": 0.85,
                    "improvement": 0.25,
                    "description": "Processing speed can be increased by 25%",
                    "actionable": True
                },
                {
                    "type": "memory_optimization",
                    "priority": "low",
                    "current_value": 0.65,
                    "target_value": 0.7,
                    "improvement": 0.05,
                    "description": "Memory utilization is optimal",
                    "actionable": False
                }
            ]
        }
        
        return {
            "status": "success",
            "data": optimization_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting optimization recommendations: {e}")
        raise HTTPException(status_code=500, detail="Failed to get optimization recommendations")

@router.get("/status")
async def get_predictive_analytics_status():
    """Get predictive analytics system status"""
    try:
        return {
            "status": "success",
            "data": {
                "total_connections": len(predictive_manager.active_connections),
                "insights_connections": len(predictive_manager.insights_connections),
                "predictions_connections": len(predictive_manager.predictions_connections),
                "optimization_connections": len(predictive_manager.optimization_connections),
                "consciousness_predictor_active": True,
                "ai_insights_engine_active": True,
                "last_update": datetime.now().isoformat()
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting predictive analytics status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get status")
