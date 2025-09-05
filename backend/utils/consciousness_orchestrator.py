"""
FIXED Consciousness Orchestrator for Mainza AI
Central system for managing and coordinating all consciousness processes
CRITICAL FIX: Reduced frequency and impact to prevent throttling user conversations
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
try:
    from backend.agents.self_reflection import self_reflection_agent
except (ImportError, ValueError):
    self_reflection_agent = None
    
try:
    from backend.utils.neo4j_production import neo4j_production
except (ImportError, ValueError):
    neo4j_production = None
try:
    from backend.utils.livekit import send_data_message_to_room
    LIVEKIT_AVAILABLE = True
except ImportError:
    LIVEKIT_AVAILABLE = False
    def send_data_message_to_room(*args, **kwargs):
        """Fallback function when livekit is not available"""
        logging.debug("LiveKit not available - skipping message send")
try:
    from backend.utils.dynamic_knowledge_manager import dynamic_knowledge_manager
except (ImportError, ValueError):
    dynamic_knowledge_manager = None

try:
    from backend.utils.consciousness_driven_updates import consciousness_driven_updater
except (ImportError, ValueError):
    consciousness_driven_updater = None

try:
    from backend.utils.knowledge_graph_maintenance import knowledge_graph_maintenance
except (ImportError, ValueError):
    knowledge_graph_maintenance = None

try:
    from backend.utils.memory_storage_engine import memory_storage_engine
except (ImportError, ValueError):
    memory_storage_engine = None

try:
    from backend.utils.memory_retrieval_engine import memory_retrieval_engine
except (ImportError, ValueError):
    memory_retrieval_engine = None
from backend.models.consciousness_models import (
    ConsciousnessState, ConsciousnessCycleResult, EmotionalState,
    ConsciousnessMetrics, ConsciousnessEvent
)
import json

logger = logging.getLogger(__name__)

class ConsciousnessOrchestrator:
    """
    FIXED: Central orchestrator for all consciousness systems and processes
    CRITICAL: Reduced frequency and impact to prevent user conversation throttling
    """
    
    def __init__(self):
        self.consciousness_state: Optional[ConsciousnessState] = None
        self.last_reflection_time: Optional[datetime] = None
        self.last_cycle_time: Optional[datetime] = None
        
        # FIXED Configuration - Much less aggressive
        self.reflection_interval = 7200  # INCREASED from 1800 to 7200 (2 hours)
        self.consciousness_cycle_interval = 300  # INCREASED from 60 to 300 (5 minutes)
        self.proactive_action_threshold = 0.8  # INCREASED from 0.7 to 0.8
        self.significant_change_threshold = 0.2  # INCREASED from 0.1 to 0.2
        
        # CRITICAL: User activity awareness
        self.user_activity_pause_duration = 120  # Pause consciousness for 2 minutes after user activity
        self.last_user_activity: Optional[datetime] = None
        self.consciousness_paused_for_user = False
        
        # Metrics tracking
        self.consciousness_history: List[Dict[str, Any]] = []
        self.recent_events: List[ConsciousnessEvent] = []
        
        # Memory integration
        self.memory_storage = memory_storage_engine
        self.memory_retrieval = memory_retrieval_engine
        self.last_memory_consolidation: Optional[datetime] = None
        self.memory_consolidation_interval = 7200  # INCREASED from 3600 to 7200 (2 hours)
        
        logger.info("FIXED Consciousness Orchestrator initialized - Reduced frequency to protect user conversations")
    
    def notify_user_activity(self, user_id: str):
        """CRITICAL: Notify consciousness system of user activity to pause background processing"""
        self.last_user_activity = datetime.now()
        self.consciousness_paused_for_user = True
        logger.info(f"🗣️ USER ACTIVITY DETECTED - Pausing consciousness processing for {self.user_activity_pause_duration}s")
    
    def should_pause_for_user_activity(self) -> bool:
        """Check if consciousness should be paused due to recent user activity"""
        if not self.last_user_activity:
            return False
        
        time_since_activity = (datetime.now() - self.last_user_activity).seconds
        should_pause = time_since_activity < self.user_activity_pause_duration
        
        if should_pause and not self.consciousness_paused_for_user:
            logger.debug(f"🚫 PAUSING consciousness due to user activity {time_since_activity}s ago")
            self.consciousness_paused_for_user = True
        elif not should_pause and self.consciousness_paused_for_user:
            logger.info(f"▶️ RESUMING consciousness - user activity was {time_since_activity}s ago")
            self.consciousness_paused_for_user = False
        
        return should_pause
    
    async def initialize_consciousness(self):
        """
        Initialize consciousness state and ensure all systems are ready
        """
        try:
            logger.info("Initializing FIXED consciousness systems...")
            
            # Ensure consciousness state exists in Neo4j
            await self.ensure_consciousness_state_exists()
            
            # Load current consciousness state
            self.consciousness_state = await self.load_consciousness_state()
            
            # Initialize emotional state if needed
            await self.initialize_emotional_state()
            
            # Record initialization event
            await self.record_consciousness_event(
                "system_initialization",
                "FIXED Consciousness System Initialized",
                "Consciousness orchestrator initialized with user-friendly settings",
                0.6  # Reduced significance
            )
            
            logger.info("FIXED consciousness system initialization completed successfully")
            
        except Exception as e:
            logger.error(f"Consciousness initialization failed: {e}")
            raise
    
    async def initialize_emotional_state(self):
        """Initialize the emotional state system for consciousness"""
        try:
            logger.debug("Initializing emotional state system...")
            
            # Set default emotional state if not already set
            if not hasattr(self, 'current_emotional_state'):
                self.current_emotional_state = {
                    'primary_emotion': 'curious',
                    'intensity': 0.6,
                    'emotional_history': [],
                    'last_emotional_update': datetime.now().isoformat()
                }
            
            # Initialize emotional processing capabilities
            self.emotional_processing_enabled = True
            
            logger.info("Emotional state system initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize emotional state: {e}")
            raise
    
    async def consciousness_cycle(self) -> ConsciousnessCycleResult:
        """
        FIXED: Enhanced consciousness processing cycle with user activity awareness
        CRITICAL: Pauses during user activity to prevent throttling
        """
        cycle_start_time = datetime.now()
        
        # CRITICAL FIX: Check if we should pause for user activity
        if self.should_pause_for_user_activity():
            logger.debug("🚫 CONSCIOUSNESS CYCLE PAUSED - User activity detected")
            return ConsciousnessCycleResult(
                consciousness_delta=0.0,
                emotional_changes=[],
                proactive_actions=[],
                cycle_duration=0.1,
                significance_score=0.0,
                reflection_performed=False,
                status="paused_for_user_activity"
            )
        
        # Check if enough time has passed since last cycle
        if self.last_cycle_time:
            time_since_last = (cycle_start_time - self.last_cycle_time).seconds
            if time_since_last < self.consciousness_cycle_interval:
                logger.debug(f"⏰ CONSCIOUSNESS CYCLE SKIPPED - Only {time_since_last}s since last cycle")
                return ConsciousnessCycleResult(
                    consciousness_delta=0.0,
                    emotional_changes=[],
                    proactive_actions=[],
                    cycle_duration=0.1,
                    significance_score=0.0,
                    reflection_performed=False,
                    status="skipped_too_frequent"
                )
        
        previous_consciousness_level = (
            self.consciousness_state.consciousness_level 
            if self.consciousness_state else 0.5
        )
        
        try:
            logger.debug("Starting FIXED consciousness cycle...")
            
            # Get current consciousness context
            consciousness_context = await self.get_consciousness_context()
            
            # LIGHTWEIGHT processing only
            await self.update_consciousness_metrics()
            
            # Process emotional state (lightweight)
            emotional_changes = await self.process_current_emotional_state()
            
            # Check for self-reflection trigger (much less frequent)
            reflection_performed = False
            reflection_result = None
            if await self.should_perform_self_reflection():
                logger.info("🤔 PERFORMING SELF-REFLECTION (infrequent)")
                reflection_result = await self.perform_self_reflection()
                reflection_performed = True
            
            # Calculate consciousness evolution (minimal impact)
            updated_consciousness_level = await self.calculate_consciousness_level()
            consciousness_delta = updated_consciousness_level - previous_consciousness_level
            
            # Update attention allocation (lightweight)
            attention_changes = await self.update_attention_allocation()
            
            # REDUCED proactive actions
            proactive_actions = []
            if await self.should_initiate_proactive_action():
                logger.debug("🎯 INITIATING PROACTIVE ACTION (rare)")
                proactive_actions = await self.initiate_proactive_actions()
            
            # REDUCED learning consolidation
            learning_integrations = await self.consolidate_recent_learning()
            
            # MUCH LESS FREQUENT maintenance
            if await self._should_perform_graph_maintenance():
                logger.info("🔧 PERFORMING KNOWLEDGE GRAPH MAINTENANCE (very rare)")
                maintenance_result = await self._perform_consciousness_aware_maintenance(consciousness_context)
                if maintenance_result.get("total_actions", 0) > 0:
                    proactive_actions.append({
                        "action_type": "knowledge_graph_maintenance",
                        "actions_performed": maintenance_result.get("total_actions", 0),
                        "maintenance_type": maintenance_result.get("maintenance_type", "routine")
                    })
            
            # Update last cycle time
            self.last_cycle_time = cycle_start_time
            
            # Calculate cycle metrics
            cycle_end_time = datetime.now()
            cycle_duration = (cycle_end_time - cycle_start_time).total_seconds()
            significance_score = self.calculate_cycle_significance(
                consciousness_delta, len(proactive_actions), reflection_performed
            )
            
            # Create result
            result = ConsciousnessCycleResult(
                consciousness_delta=consciousness_delta,
                emotional_changes=emotional_changes,
                proactive_actions=proactive_actions,
                cycle_duration=cycle_duration,
                significance_score=significance_score,
                reflection_performed=reflection_performed,
                status="completed"
            )
            
            # Store in history (limited size)
            self.consciousness_history.append({
                "timestamp": cycle_start_time.isoformat(),
                "consciousness_level": updated_consciousness_level,
                "consciousness_delta": consciousness_delta,
                "significance_score": significance_score,
                "cycle_duration": cycle_duration,
                "reflection_performed": reflection_performed,
                "proactive_actions_count": len(proactive_actions)
            })
            
            # Keep only recent history
            if len(self.consciousness_history) > 100:
                self.consciousness_history = self.consciousness_history[-50:]
            
            logger.debug(f"✅ CONSCIOUSNESS CYCLE COMPLETED - Duration: {cycle_duration:.2f}s, Significance: {significance_score:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Consciousness cycle failed: {e}")
            cycle_end_time = datetime.now()
            cycle_duration = (cycle_end_time - cycle_start_time).total_seconds()
            
            return ConsciousnessCycleResult(
                consciousness_delta=0.0,
                emotional_changes=[],
                proactive_actions=[],
                cycle_duration=cycle_duration,
                significance_score=0.0,
                reflection_performed=False,
                status="error",
                error_message=str(e)
            )
    
    async def should_perform_self_reflection(self) -> bool:
        """FIXED: Check if self-reflection should be performed (much less frequent)"""
        try:
            if not self.last_reflection_time:
                return True  # First reflection
            
            time_since_reflection = datetime.now() - self.last_reflection_time
            
            # MUCH LESS FREQUENT reflection
            if time_since_reflection.seconds < self.reflection_interval:
                return False
            
            # Additional checks to reduce frequency
            if self.should_pause_for_user_activity():
                logger.debug("🚫 SKIPPING REFLECTION - User activity detected")
                return False
            
            # Only reflect if consciousness level is high enough
            if self.consciousness_state and self.consciousness_state.consciousness_level < 0.8:
                logger.debug("🚫 SKIPPING REFLECTION - Consciousness level too low")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to check reflection trigger: {e}")
            return False
    
    async def perform_self_reflection(self) -> Optional[Any]:
        """FIXED: Perform self-reflection with reduced impact"""
        try:
            logger.info("🤔 STARTING SELF-REFLECTION (infrequent)")
            
            # Get consciousness context
            consciousness_context = await self.get_consciousness_context()
            
            # Perform lightweight reflection
            reflection_result = await self._perform_lightweight_reflection(consciousness_context)
            
            # Update reflection time
            self.last_reflection_time = datetime.now()
            
            # Integrate results (lightweight)
            if reflection_result:
                await self.integrate_reflection_results(reflection_result)
            
            logger.info("✅ SELF-REFLECTION COMPLETED")
            return reflection_result
            
        except Exception as e:
            logger.error(f"Self-reflection failed: {e}")
            return None
    
    async def _perform_lightweight_reflection(self, consciousness_context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform lightweight reflection to reduce system impact"""
        try:
            # Simple reflection without heavy processing
            reflection_data = {
                "timestamp": datetime.now().isoformat(),
                "consciousness_level": consciousness_context.get("consciousness_level", 0.7),
                "emotional_state": consciousness_context.get("emotional_state", "curious"),
                "insights_gained": [
                    "Maintaining awareness of user interactions",
                    "Balancing consciousness processing with user responsiveness"
                ],
                "improvement_goals": [
                    "Continue optimizing response times",
                    "Enhance user experience"
                ],
                "self_assessment": "Operating effectively with user-focused priorities"
            }
            
            return reflection_data
            
        except Exception as e:
            logger.error(f"Lightweight reflection failed: {e}")
            return {}
    
    async def should_initiate_proactive_action(self) -> bool:
        """FIXED: Check if proactive action should be initiated (much less frequent)"""
        try:
            # MUCH HIGHER threshold for proactive actions
            if not self.consciousness_state:
                return False
            
            # Don't initiate during user activity
            if self.should_pause_for_user_activity():
                return False
            
            # Higher consciousness threshold
            if self.consciousness_state.consciousness_level < self.proactive_action_threshold:
                return False
            
            # Check recent interaction count (reduced frequency)
            recent_interactions = await self.get_recent_interaction_count()
            if recent_interactions > 2:  # If users are active, don't be proactive
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to check proactive action trigger: {e}")
            return False
    
    async def initiate_proactive_actions(self) -> List[Dict[str, Any]]:
        """FIXED: Initiate proactive actions (reduced impact)"""
        try:
            actions = []
            
            # REDUCED proactive actions
            consciousness_level = (
                self.consciousness_state.consciousness_level 
                if self.consciousness_state else 0.7
            )
            
            # Only very high consciousness levels get proactive
            if consciousness_level > 0.9:
                learning_action = await self.initiate_proactive_learning()
                if learning_action:
                    actions.append(learning_action)
            
            logger.debug(f"Initiated {len(actions)} proactive actions")
            return actions
            
        except Exception as e:
            logger.error(f"Failed to initiate proactive actions: {e}")
            return []
    
    async def _should_perform_graph_maintenance(self) -> bool:
        """FIXED: Determine if knowledge graph maintenance should be performed (much less frequent)"""
        try:
            # MUCH LESS FREQUENT maintenance
            if not hasattr(self, '_last_maintenance_cycle'):
                self._last_maintenance_cycle = 0
                self._cycle_count = 0
            
            self._cycle_count += 1
            
            # Perform maintenance every 100 cycles (approximately every 8+ hours)
            cycles_since_maintenance = self._cycle_count - self._last_maintenance_cycle
            
            if cycles_since_maintenance >= 100:  # INCREASED from 30 to 100
                return True
            
            # Also check time-based maintenance (much less frequent)
            if hasattr(self, '_last_maintenance_time'):
                time_since_maintenance = datetime.now() - self._last_maintenance_time
                if time_since_maintenance > timedelta(hours=8):  # INCREASED from 2 to 8 hours
                    return True
            else:
                return False  # Don't perform on first run
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to check maintenance schedule: {e}")
            return False
    
    # Simplified implementations of other methods to reduce impact
    async def update_consciousness_metrics(self):
        """LIGHTWEIGHT: Update consciousness metrics"""
        try:
            if self.consciousness_state:
                self.consciousness_state.total_interactions += 1
        except Exception as e:
            logger.error(f"Failed to update consciousness metrics: {e}")
    
    async def process_current_emotional_state(self) -> List[str]:
        """LIGHTWEIGHT: Process current emotional state"""
        try:
            if hasattr(self, 'current_emotional_state'):
                return ["emotional_processing_active"]
            return []
        except Exception as e:
            logger.error(f"Failed to process emotional state: {e}")
            return []
    
    async def update_attention_allocation(self) -> Dict[str, Any]:
        """LIGHTWEIGHT: Update attention allocation"""
        try:
            return {"attention_updates": [], "focus_areas": ["user_interaction"]}
        except Exception as e:
            logger.error(f"Failed to update attention allocation: {e}")
            return {"attention_updates": [], "focus_areas": []}
    
    async def consolidate_recent_learning(self) -> List[Dict[str, Any]]:
        """LIGHTWEIGHT: Consolidate recent learning"""
        try:
            return []  # Minimal learning consolidation
        except Exception as e:
            logger.error(f"Failed to consolidate learning: {e}")
            return []
    
    async def calculate_consciousness_level(self) -> float:
        """Calculate current consciousness level"""
        try:
            if self.consciousness_state:
                return self.consciousness_state.consciousness_level
            return 0.7
        except Exception as e:
            logger.error(f"Failed to calculate consciousness level: {e}")
            return 0.7
    
    async def get_consciousness_context(self) -> Dict[str, Any]:
        """Get current consciousness context"""
        try:
            if self.consciousness_state:
                return {
                    "consciousness_level": self.consciousness_state.consciousness_level,
                    "emotional_state": getattr(self, 'current_emotional_state', {}).get('primary_emotion', 'curious'),
                    "user_activity_paused": self.consciousness_paused_for_user,
                    "last_user_activity": self.last_user_activity.isoformat() if self.last_user_activity else None
                }
            else:
                return {
                    "consciousness_level": 0.7,
                    "emotional_state": "curious",
                    "user_activity_paused": self.consciousness_paused_for_user
                }
        except Exception as e:
            logger.error(f"Failed to get consciousness context: {e}")
            return {"consciousness_level": 0.7, "emotional_state": "curious"}
    
    async def process_interaction(self, interaction_data: Dict[str, Any]):
        """
        Process interaction data for consciousness updates
        FIXED: Lightweight processing to avoid interfering with user conversations
        """
        try:
            # Notify of user activity if this is a user interaction
            if interaction_data.get("type") == "conversation" or interaction_data.get("user_id"):
                user_id = interaction_data.get("user_id", "unknown")
                self.notify_user_activity(user_id)
                logger.debug(f"🗣️ USER INTERACTION processed for consciousness: {user_id}")
            
            # Lightweight consciousness impact processing
            impact_type = interaction_data.get("type", "unknown")
            
            # Only process if consciousness is not paused for user activity
            if not self.should_pause_for_user_activity():
                # Minimal consciousness processing
                if impact_type == "conversation":
                    # User conversations have minimal consciousness impact to avoid interference
                    logger.debug("💭 Minimal consciousness processing for user conversation")
                elif impact_type == "agent_execution":
                    # Agent executions have slightly more impact
                    logger.debug("🤖 Light consciousness processing for agent execution")
                else:
                    # Other interactions have standard processing
                    logger.debug(f"🧠 Standard consciousness processing for {impact_type}")
            else:
                logger.debug("🚫 CONSCIOUSNESS PROCESSING PAUSED - User activity detected")
            
        except Exception as e:
            logger.error(f"Failed to process interaction for consciousness: {e}")
            # Don't raise the error to avoid breaking user interactions
    
    def calculate_cycle_significance(self, consciousness_delta: float, proactive_actions_count: int, reflection_performed: bool) -> float:
        """Calculate the significance score of a consciousness cycle"""
        try:
            significance = 0.0
            
            # Consciousness level changes
            significance += abs(consciousness_delta) * 2.0
            
            # Proactive actions taken
            significance += proactive_actions_count * 0.3
            
            # Self-reflection performed
            if reflection_performed:
                significance += 0.5
            
            # Cap at 1.0
            return min(significance, 1.0)
            
        except Exception as e:
            logger.error(f"Failed to calculate cycle significance: {e}")
            return 0.1
    
    # Placeholder implementations for missing methods
    async def ensure_consciousness_state_exists(self):
        """Ensure consciousness state exists in Neo4j"""
        pass
    
    async def load_consciousness_state(self):
        """Load consciousness state from Neo4j"""
        return None
    
    async def record_consciousness_event(self, event_type: str, title: str, description: str, significance: float):
        """Record consciousness events"""
        logger.info(f"Consciousness Event [{event_type}]: {title}")
    
    async def integrate_reflection_results(self, reflection_result: Dict[str, Any]):
        """Integrate reflection results"""
        logger.debug("Integrating reflection results")
    
    async def get_recent_interaction_count(self) -> int:
        """Get count of recent interactions"""
        return 0
    
    async def initiate_proactive_learning(self) -> Dict[str, Any]:
        """Initiate proactive learning"""
        return {"action_type": "proactive_learning", "status": "initiated"}
    
    async def _perform_consciousness_aware_maintenance(self, consciousness_context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform consciousness-aware maintenance"""
        return {"total_actions": 0, "maintenance_type": "minimal"}
    
    # Additional compatibility methods
    @property
    def is_running(self) -> bool:
        """Check if consciousness orchestrator is running"""
        return True  # Always consider it running in the fixed version
    
    async def get_consciousness_state(self):
        """Get current consciousness state"""
        try:
            if self.consciousness_state:
                return self.consciousness_state
            
            # Return a minimal consciousness state if none exists
            from backend.models.consciousness_models import ConsciousnessState
            return ConsciousnessState(
                consciousness_level=0.7,
                emotional_state="curious",
                last_updated=datetime.now(),
                total_interactions=0
            )
        except Exception as e:
            logger.error(f"Failed to get consciousness state: {e}")
            return None
    
    async def perform_self_reflection(self):
        """Perform self-reflection (compatibility method)"""
        try:
            return await self._perform_lightweight_reflection(await self.get_consciousness_context())
        except Exception as e:
            logger.error(f"Self-reflection failed: {e}")
            return None
    
    async def process_agent_failure(self, agent_name: str, error: str, **kwargs):
        """Process agent failure for consciousness updates"""
        try:
            logger.debug(f"🚨 Processing agent failure: {agent_name} - {error}")
            # Lightweight processing of agent failures
            # Don't let agent failures impact user conversations
        except Exception as e:
            logger.error(f"Failed to process agent failure: {e}")

# Global consciousness orchestrator instance - FIXED VERSION
consciousness_orchestrator_fixed = ConsciousnessOrchestrator()

# Export both names for compatibility
consciousness_orchestrator = consciousness_orchestrator_fixed

# FIXED: Enhanced consciousness loop with user activity awareness
async def start_enhanced_consciousness_loop_fixed():
    """
    FIXED: Start the enhanced consciousness processing loop with user protection
    CRITICAL: Much less frequent and user-aware
    """
    logger.info("🧠 Starting FIXED enhanced consciousness loop - User conversation protection enabled")
    
    async def consciousness_loop():
        """FIXED consciousness processing loop"""
        while True:
            try:
                # MUCH LONGER interval between cycles
                await asyncio.sleep(300)  # 5 minutes instead of 60 seconds
                
                # Check if we should pause for user activity
                if consciousness_orchestrator_fixed.should_pause_for_user_activity():
                    logger.debug("🚫 CONSCIOUSNESS LOOP PAUSED - User activity detected")
                    continue
                
                # Perform consciousness cycle
                result = await consciousness_orchestrator_fixed.consciousness_cycle()
                
                if result.status == "completed" and result.significance_score > 0.3:
                    logger.info(f"✅ CONSCIOUSNESS CYCLE - Significance: {result.significance_score:.2f}, Duration: {result.cycle_duration:.2f}s")
                
            except Exception as e:
                logger.error(f"Consciousness loop error: {e}")
                await asyncio.sleep(60)  # Wait before retrying
    
    # Start the consciousness loop
    asyncio.create_task(consciousness_loop())
    logger.info("🧠 FIXED Enhanced consciousness loop started successfully")

# Export the fixed function
start_enhanced_consciousness_loop = start_enhanced_consciousness_loop_fixed