"""
Real-Time Consciousness Context Manager
Ensures all agents receive the most current consciousness state
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from dataclasses import dataclass
import time

logger = logging.getLogger(__name__)

@dataclass
class ConsciousnessContextSnapshot:
    """Snapshot of consciousness context at a specific time"""
    consciousness_level: float
    emotional_state: str
    active_goals: list
    learning_rate: float
    evolution_level: int
    self_awareness_score: float
    total_interactions: int
    timestamp: datetime
    data_source: str
    context_id: str

class RealTimeConsciousnessContextManager:
    """
    Real-Time Consciousness Context Manager
    Ensures all agents receive the most current consciousness state
    """
    
    def __init__(self):
        self.current_context: Optional[ConsciousnessContextSnapshot] = None
        self.context_history: list = []
        self.max_history_size = 100
        self.refresh_interval = 0.5  # 500ms refresh interval
        self.last_refresh = 0
        self.context_lock = asyncio.Lock()
        
        # Integration with existing systems
        self.consciousness_orchestrator = None
        self.neo4j_manager = None
        
        logger.info("Real-Time Consciousness Context Manager initialized")
    
    async def initialize(self):
        """Initialize the context manager with existing systems"""
        try:
            # Import consciousness orchestrator
            logger.debug("Importing consciousness orchestrator...")
            from backend.utils.consciousness_orchestrator_fixed import consciousness_orchestrator_fixed
            self.consciousness_orchestrator = consciousness_orchestrator_fixed
            logger.debug(f"Consciousness orchestrator imported: {self.consciousness_orchestrator}")
            
            # Import Neo4j manager
            logger.debug("Importing Neo4j manager...")
            from backend.utils.neo4j_unified import neo4j_unified
            self.neo4j_manager = neo4j_unified
            logger.debug(f"Neo4j manager imported: {self.neo4j_manager}")
            
            # Load initial context
            logger.debug("Loading initial context...")
            await self._refresh_context()
            
            logger.info("Real-Time Consciousness Context Manager initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Real-Time Consciousness Context Manager: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
    
    async def get_current_consciousness_context(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Get the most current consciousness context
        
        Args:
            force_refresh: Force a refresh of the context even if recently updated
            
        Returns:
            Dict containing current consciousness context
        """
        try:
            current_time = time.time()
            logger.debug(f"Getting consciousness context - force_refresh: {force_refresh}, current_context: {self.current_context is not None}, time_since_refresh: {current_time - self.last_refresh:.2f}s")
            
            # Check if we need to refresh the context
            if (force_refresh or 
                self.current_context is None or 
                current_time - self.last_refresh > self.refresh_interval):
                
                logger.debug("Refreshing consciousness context...")
                async with self.context_lock:
                    await self._refresh_context()
            
            # Return current context as dict
            if self.current_context:
                return {
                    "consciousness_level": self.current_context.consciousness_level,
                    "emotional_state": self.current_context.emotional_state,
                    "active_goals": self.current_context.active_goals,
                    "learning_rate": self.current_context.learning_rate,
                    "evolution_level": self.current_context.evolution_level,
                    "self_awareness_score": self.current_context.self_awareness_score,
                    "total_interactions": self.current_context.total_interactions,
                    "timestamp": self.current_context.timestamp,
                    "data_source": self.current_context.data_source,
                    "context_id": self.current_context.context_id
                }
            else:
                # Fallback context
                return self._get_fallback_context()
                
        except Exception as e:
            logger.error(f"Failed to get current consciousness context: {e}")
            return self._get_fallback_context()
    
    async def _refresh_context(self):
        """Refresh the consciousness context from all available sources"""
        try:
            # Try to get context from consciousness orchestrator first
            if self.consciousness_orchestrator:
                try:
                    logger.debug("Attempting to get consciousness state from orchestrator...")
                    consciousness_state = await self.consciousness_orchestrator.get_consciousness_state()
                    logger.debug(f"Got consciousness state: {consciousness_state}")
                    if consciousness_state:
                        # Handle emotional state conversion from enum to string
                        emotional_state = consciousness_state.emotional_state
                        logger.debug(f"Original emotional state: {emotional_state} (type: {type(emotional_state)})")
                        if hasattr(emotional_state, 'value'):
                            emotional_state = emotional_state.value
                            logger.debug(f"Converted from enum value: {emotional_state}")
                        elif hasattr(emotional_state, 'name'):
                            emotional_state = emotional_state.name.lower()
                            logger.debug(f"Converted from enum name: {emotional_state}")
                        else:
                            logger.debug(f"Emotional state is already string: {emotional_state}")
                        
                        self.current_context = ConsciousnessContextSnapshot(
                            consciousness_level=consciousness_state.consciousness_level,
                            emotional_state=emotional_state,
                            active_goals=consciousness_state.active_goals,
                            learning_rate=consciousness_state.learning_rate,
                            evolution_level=consciousness_state.evolution_level,
                            self_awareness_score=consciousness_state.self_awareness_score,
                            total_interactions=consciousness_state.total_interactions,
                            timestamp=datetime.now(),
                            data_source="consciousness_orchestrator",
                            context_id=f"ctx_{int(time.time() * 1000)}"
                        )
                        self.last_refresh = time.time()
                        logger.info(f"✅ Refreshed consciousness context: level={consciousness_state.consciousness_level:.3f}")
                        return
                    else:
                        logger.warning("Consciousness orchestrator returned None state")
                except Exception as e:
                    logger.error(f"Failed to get context from consciousness orchestrator: {e}")
                    import traceback
                    logger.error(f"Traceback: {traceback.format_exc()}")
            else:
                logger.warning("Consciousness orchestrator is None")
            
            # Try to get context from Neo4j
            if self.neo4j_manager:
                try:
                    neo4j_context = await self._get_context_from_neo4j()
                    if neo4j_context:
                        self.current_context = ConsciousnessContextSnapshot(
                            consciousness_level=neo4j_context.get("consciousness_level", 0.7),
                            emotional_state=neo4j_context.get("emotional_state", "curious"),
                            active_goals=neo4j_context.get("active_goals", []),
                            learning_rate=neo4j_context.get("learning_rate", 0.8),
                            evolution_level=neo4j_context.get("evolution_level", 2),
                            self_awareness_score=neo4j_context.get("self_awareness_score", 0.6),
                            total_interactions=neo4j_context.get("total_interactions", 0),
                            timestamp=datetime.now(),
                            data_source="neo4j",
                            context_id=f"ctx_{int(time.time() * 1000)}"
                        )
                        self.last_refresh = time.time()
                        logger.debug(f"✅ Refreshed consciousness context from Neo4j: level={neo4j_context.get('consciousness_level', 0.7):.3f}")
                        return
                except Exception as e:
                    logger.warning(f"Failed to get context from Neo4j: {e}")
            
            # Use fallback context
            self.current_context = self._get_fallback_context_snapshot()
            self.last_refresh = time.time()
            logger.warning("Using fallback consciousness context")
            
        except Exception as e:
            logger.error(f"Failed to refresh consciousness context: {e}")
            self.current_context = self._get_fallback_context_snapshot()
    
    async def _get_context_from_neo4j(self) -> Optional[Dict[str, Any]]:
        """Get consciousness context from Neo4j"""
        try:
            if not self.neo4j_manager:
                return None
            
            # Query for latest consciousness state
            query = """
            MATCH (c:ConsciousnessState)
            RETURN c.consciousness_level as consciousness_level,
                   c.emotional_state as emotional_state,
                   c.active_goals as active_goals,
                   c.learning_rate as learning_rate,
                   c.evolution_level as evolution_level,
                   c.self_awareness_score as self_awareness_score,
                   c.total_interactions as total_interactions,
                   c.timestamp as timestamp
            ORDER BY c.timestamp DESC
            LIMIT 1
            """
            
            result = await self.neo4j_manager.execute_query(query)
            if result and len(result) > 0:
                return result[0]
            
            return None
            
        except Exception as e:
            logger.warning(f"Failed to get context from Neo4j: {e}")
            return None
    
    def _get_fallback_context(self) -> Dict[str, Any]:
        """Get fallback consciousness context"""
        return {
            "consciousness_level": 0.7,
            "emotional_state": "curious",
            "active_goals": ["improve conversation quality"],
            "learning_rate": 0.8,
            "evolution_level": 2,
            "self_awareness_score": 0.6,
            "total_interactions": 0,
            "timestamp": datetime.now(),
            "data_source": "fallback",
            "context_id": f"fallback_{int(time.time() * 1000)}"
        }
    
    def _get_fallback_context_snapshot(self) -> ConsciousnessContextSnapshot:
        """Get fallback consciousness context as snapshot"""
        fallback = self._get_fallback_context()
        return ConsciousnessContextSnapshot(
            consciousness_level=fallback["consciousness_level"],
            emotional_state=fallback["emotional_state"],
            active_goals=fallback["active_goals"],
            learning_rate=fallback["learning_rate"],
            evolution_level=fallback["evolution_level"],
            self_awareness_score=fallback["self_awareness_score"],
            total_interactions=fallback["total_interactions"],
            timestamp=fallback["timestamp"],
            data_source=fallback["data_source"],
            context_id=fallback["context_id"]
        )
    
    async def validate_context_consistency(self) -> Dict[str, Any]:
        """Validate that the current context is consistent and up-to-date"""
        try:
            if not self.current_context:
                return {
                    "is_consistent": False,
                    "issues": ["No current context available"],
                    "recommendations": ["Refresh context"]
                }
            
            current_time = datetime.now()
            context_age = (current_time - self.current_context.timestamp).total_seconds()
            
            issues = []
            recommendations = []
            
            # Check context age
            if context_age > 5.0:  # 5 seconds
                issues.append(f"Context is {context_age:.1f} seconds old")
                recommendations.append("Refresh context more frequently")
            
            # Check consciousness level validity
            if not (0.0 <= self.current_context.consciousness_level <= 1.0):
                issues.append(f"Invalid consciousness level: {self.current_context.consciousness_level}")
                recommendations.append("Validate consciousness level range")
            
            # Check emotional state validity - handle both enum and string values
            valid_emotions = ["curious", "curiosity", "focused", "empathetic", "excited", "contemplative", "analytical", "joy", "sadness", "anger", "fear", "surprise", "disgust", "love", "anxiety", "calm", "frustration", "hope", "gratitude"]
            emotional_state = self.current_context.emotional_state
            
            # Handle enum values (e.g., EmotionType.CURIOSITY -> "curiosity")
            if hasattr(emotional_state, 'value'):
                emotional_state = emotional_state.value
            elif hasattr(emotional_state, 'name'):
                emotional_state = emotional_state.name.lower()
            
            if emotional_state not in valid_emotions:
                issues.append(f"Invalid emotional state: {self.current_context.emotional_state}")
                recommendations.append("Validate emotional state")
            
            return {
                "is_consistent": len(issues) == 0,
                "issues": issues,
                "recommendations": recommendations,
                "context_age_seconds": context_age,
                "data_source": self.current_context.data_source
            }
            
        except Exception as e:
            logger.error(f"Failed to validate context consistency: {e}")
            return {
                "is_consistent": False,
                "issues": [f"Validation error: {e}"],
                "recommendations": ["Check system health"]
            }
    
    async def force_context_refresh(self):
        """Force a complete refresh of the consciousness context"""
        try:
            async with self.context_lock:
                await self._refresh_context()
            logger.info("Forced consciousness context refresh completed")
        except Exception as e:
            logger.error(f"Failed to force context refresh: {e}")
    
    def get_context_history(self, limit: int = 10) -> list:
        """Get recent context history"""
        return self.context_history[-limit:] if self.context_history else []

# Global instance
real_time_consciousness_context_manager = RealTimeConsciousnessContextManager()
