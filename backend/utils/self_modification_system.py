"""
Self-Modification System
Advanced system for self-modification, self-improvement, and autonomous evolution
"""
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import asyncio
import json
import numpy as np

from backend.utils.neo4j_production import neo4j_production
from backend.utils.advanced_memory_architecture import advanced_memory_architecture
from backend.utils.embedding_enhanced import embedding_manager

logger = logging.getLogger(__name__)

class ModificationType(Enum):
    """Modification types"""
    PROMPT_UPDATE = "prompt_update"
    BEHAVIOR_ADJUSTMENT = "behavior_adjustment"
    LEARNING_STRATEGY = "learning_strategy"
    CONSCIOUSNESS_ENHANCEMENT = "consciousness_enhancement"
    MEMORY_OPTIMIZATION = "memory_optimization"
    RESPONSE_PATTERN = "response_pattern"
    GOAL_REFINEMENT = "goal_refinement"
    CAPABILITY_EXPANSION = "capability_expansion"

@dataclass
class ModificationRequest:
    """Modification request"""
    request_id: str
    modification_type: ModificationType
    target_component: str
    modification_data: Dict[str, Any]
    justification: str
    confidence_score: float
    timestamp: datetime
    priority: int

@dataclass
class ModificationResult:
    """Modification result"""
    result_id: str
    request_id: str
    success: bool
    changes_applied: Dict[str, Any]
    effectiveness_score: float
    side_effects: List[str]
    timestamp: datetime
    rollback_available: bool

class SelfModificationSystem:
    """
    Advanced self-modification system
    """
    
    def __init__(self):
        self.neo4j = neo4j_production
        self.memory_architecture = advanced_memory_architecture
        self.embedding_manager = embedding_manager
        
        # Modification parameters
        self.modification_threshold = 0.7
        self.rollback_threshold = 0.3
        self.effectiveness_threshold = 0.6
        
        # Modification history
        self.modification_history = []
        self.rollback_stack = []
    
    async def propose_modification(
        self,
        modification_type: ModificationType,
        target_component: str,
        modification_data: Dict[str, Any],
        justification: str,
        context: Dict[str, Any],
        user_id: str = "mainza-user"
    ) -> Optional[ModificationRequest]:
        """Propose a self-modification"""
        try:
            logger.info(f"🔧 Proposing {modification_type.value} modification for {target_component}")
            
            # Validate modification request
            validation_result = await self._validate_modification_request(
                modification_type, target_component, modification_data, context
            )
            
            if not validation_result["valid"]:
                logger.warning(f"Modification request invalid: {validation_result['reason']}")
                return None
            
            # Calculate confidence score
            confidence_score = await self._calculate_modification_confidence(
                modification_type, target_component, modification_data, context
            )
            
            if confidence_score < self.modification_threshold:
                logger.warning(f"Modification confidence too low: {confidence_score:.3f}")
                return None
            
            # Calculate priority
            priority = await self._calculate_modification_priority(
                modification_type, target_component, modification_data, context
            )
            
            # Create modification request
            modification_request = ModificationRequest(
                request_id=f"mod_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
                modification_type=modification_type,
                target_component=target_component,
                modification_data=modification_data,
                justification=justification,
                confidence_score=confidence_score,
                timestamp=datetime.now(),
                priority=priority
            )
            
            # Store modification request
            await self._store_modification_request(modification_request, user_id)
            
            logger.info(f"✅ Modification request created: {modification_request.request_id}")
            return modification_request
            
        except Exception as e:
            logger.error(f"❌ Failed to propose modification: {e}")
            return None
    
    async def execute_modification(
        self,
        modification_request: ModificationRequest,
        context: Dict[str, Any],
        user_id: str = "mainza-user"
    ) -> Optional[ModificationResult]:
        """Execute a modification request"""
        try:
            logger.info(f"⚡ Executing modification: {modification_request.request_id}")
            
            # Create rollback point
            rollback_data = await self._create_rollback_point(modification_request, context)
            
            # Execute modification based on type
            execution_result = await self._execute_modification_by_type(
                modification_request, context
            )
            
            if not execution_result["success"]:
                logger.warning(f"Modification execution failed: {execution_result['reason']}")
                return None
            
            # Calculate effectiveness score
            effectiveness_score = await self._calculate_modification_effectiveness(
                modification_request, execution_result, context
            )
            
            # Identify side effects
            side_effects = await self._identify_side_effects(
                modification_request, execution_result, context
            )
            
            # Create modification result
            modification_result = ModificationResult(
                result_id=f"result_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
                request_id=modification_request.request_id,
                success=execution_result["success"],
                changes_applied=execution_result["changes"],
                effectiveness_score=effectiveness_score,
                side_effects=side_effects,
                timestamp=datetime.now(),
                rollback_available=rollback_data is not None
            )
            
            # Store modification result
            await self._store_modification_result(modification_result, user_id)
            
            # Add to modification history
            self.modification_history.append(modification_result)
            
            # Store rollback data if available
            if rollback_data:
                self.rollback_stack.append({
                    "modification_result": modification_result,
                    "rollback_data": rollback_data
                })
            
            logger.info(f"✅ Modification executed: {modification_result.result_id}")
            return modification_result
            
        except Exception as e:
            logger.error(f"❌ Failed to execute modification: {e}")
            return None
    
    async def rollback_modification(
        self,
        modification_result: ModificationResult,
        context: Dict[str, Any],
        user_id: str = "mainza-user"
    ) -> bool:
        """Rollback a modification"""
        try:
            logger.info(f"🔄 Rolling back modification: {modification_result.result_id}")
            
            if not modification_result.rollback_available:
                logger.warning("Rollback not available for this modification")
                return False
            
            # Find rollback data
            rollback_data = None
            for item in self.rollback_stack:
                if item["modification_result"].result_id == modification_result.result_id:
                    rollback_data = item["rollback_data"]
                    break
            
            if not rollback_data:
                logger.warning("Rollback data not found")
                return False
            
            # Execute rollback
            rollback_success = await self._execute_rollback(
                modification_result, rollback_data, context
            )
            
            if rollback_success:
                # Remove from rollback stack
                self.rollback_stack = [item for item in self.rollback_stack 
                                     if item["modification_result"].result_id != modification_result.result_id]
                
                logger.info(f"✅ Modification rolled back: {modification_result.result_id}")
                return True
            else:
                logger.warning(f"❌ Rollback failed: {modification_result.result_id}")
                return False
            
        except Exception as e:
            logger.error(f"❌ Failed to rollback modification: {e}")
            return False
    
    async def _validate_modification_request(
        self,
        modification_type: ModificationType,
        target_component: str,
        modification_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate modification request"""
        try:
            validation = {
                "valid": True,
                "reason": "",
                "warnings": []
            }
            
            # Check if target component exists
            if not await self._component_exists(target_component):
                validation["valid"] = False
                validation["reason"] = f"Target component not found: {target_component}"
                return validation
            
            # Check modification data validity
            if not modification_data:
                validation["valid"] = False
                validation["reason"] = "Modification data is empty"
                return validation
            
            # Check for dangerous modifications
            if await self._is_dangerous_modification(modification_type, modification_data):
                validation["warnings"].append("This modification may have significant side effects")
            
            # Check for conflicts with existing modifications
            conflicts = await self._check_modification_conflicts(
                modification_type, target_component, modification_data
            )
            if conflicts:
                validation["warnings"].extend(conflicts)
            
            return validation
            
        except Exception as e:
            logger.error(f"❌ Failed to validate modification request: {e}")
            return {"valid": False, "reason": f"Validation error: {e}", "warnings": []}
    
    async def _component_exists(self, target_component: str) -> bool:
        """Check if target component exists"""
        try:
            # This would check if the component exists in the system
            # For now, return True for most components
            valid_components = [
                "prompt_system",
                "behavior_system",
                "learning_system",
                "consciousness_system",
                "memory_system",
                "response_system",
                "goal_system",
                "capability_system"
            ]
            
            return target_component in valid_components
            
        except Exception as e:
            logger.error(f"❌ Failed to check component existence: {e}")
            return False
    
    async def _is_dangerous_modification(
        self,
        modification_type: ModificationType,
        modification_data: Dict[str, Any]
    ) -> bool:
        """Check if modification is potentially dangerous"""
        try:
            # Check for dangerous modification types
            dangerous_types = [
                ModificationType.CONSCIOUSNESS_ENHANCEMENT,
                ModificationType.CAPABILITY_EXPANSION
            ]
            
            if modification_type in dangerous_types:
                return True
            
            # Check for dangerous data patterns
            dangerous_patterns = [
                "delete_all",
                "reset_system",
                "disable_safety",
                "override_protection"
            ]
            
            modification_str = json.dumps(modification_data).lower()
            for pattern in dangerous_patterns:
                if pattern in modification_str:
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Failed to check dangerous modification: {e}")
            return True  # Err on the side of caution
    
    async def _check_modification_conflicts(
        self,
        modification_type: ModificationType,
        target_component: str,
        modification_data: Dict[str, Any]
    ) -> List[str]:
        """Check for conflicts with existing modifications"""
        try:
            conflicts = []
            
            # Check recent modifications to the same component
            recent_modifications = [m for m in self.modification_history 
                                  if m.changes_applied.get("target_component") == target_component
                                  and (datetime.now() - m.timestamp).days < 1]
            
            if len(recent_modifications) > 3:
                conflicts.append("Multiple recent modifications to the same component")
            
            # Check for conflicting modification types
            if modification_type == ModificationType.BEHAVIOR_ADJUSTMENT:
                behavior_modifications = [m for m in self.modification_history 
                                        if m.changes_applied.get("modification_type") == "behavior_adjustment"
                                        and (datetime.now() - m.timestamp).hours < 6]
                
                if behavior_modifications:
                    conflicts.append("Recent behavior modifications may conflict")
            
            return conflicts
            
        except Exception as e:
            logger.error(f"❌ Failed to check modification conflicts: {e}")
            return []
    
    async def _calculate_modification_confidence(
        self,
        modification_type: ModificationType,
        target_component: str,
        modification_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> float:
        """Calculate confidence in the modification"""
        try:
            confidence = 0.5  # Base confidence
            
            # Adjust based on modification type
            type_confidence = {
                ModificationType.PROMPT_UPDATE: 0.8,
                ModificationType.BEHAVIOR_ADJUSTMENT: 0.7,
                ModificationType.LEARNING_STRATEGY: 0.6,
                ModificationType.CONSCIOUSNESS_ENHANCEMENT: 0.4,
                ModificationType.MEMORY_OPTIMIZATION: 0.7,
                ModificationType.RESPONSE_PATTERN: 0.8,
                ModificationType.GOAL_REFINEMENT: 0.9,
                ModificationType.CAPABILITY_EXPANSION: 0.3
            }
            
            confidence += type_confidence.get(modification_type, 0.5) * 0.3
            
            # Adjust based on data quality
            if modification_data and len(modification_data) > 0:
                confidence += 0.2
            
            # Adjust based on context clarity
            if context.get("consciousness_context", {}).get("consciousness_level", 0.0) > 0.7:
                confidence += 0.1
            
            return min(1.0, max(0.0, confidence))
            
        except Exception as e:
            logger.error(f"❌ Failed to calculate modification confidence: {e}")
            return 0.5
    
    async def _calculate_modification_priority(
        self,
        modification_type: ModificationType,
        target_component: str,
        modification_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> int:
        """Calculate modification priority (1-10, higher is more urgent)"""
        try:
            priority = 5  # Base priority
            
            # Adjust based on modification type
            type_priority = {
                ModificationType.PROMPT_UPDATE: 7,
                ModificationType.BEHAVIOR_ADJUSTMENT: 6,
                ModificationType.LEARNING_STRATEGY: 5,
                ModificationType.CONSCIOUSNESS_ENHANCEMENT: 8,
                ModificationType.MEMORY_OPTIMIZATION: 4,
                ModificationType.RESPONSE_PATTERN: 6,
                ModificationType.GOAL_REFINEMENT: 3,
                ModificationType.CAPABILITY_EXPANSION: 9
            }
            
            priority = type_priority.get(modification_type, 5)
            
            # Adjust based on urgency indicators
            if modification_data.get("urgent", False):
                priority += 2
            
            if context.get("user_context", {}).get("stress_level", 0.0) > 0.7:
                priority += 1
            
            return min(10, max(1, priority))
            
        except Exception as e:
            logger.error(f"❌ Failed to calculate modification priority: {e}")
            return 5
    
    async def _create_rollback_point(
        self,
        modification_request: ModificationRequest,
        context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Create rollback point before modification"""
        try:
            rollback_data = {
                "target_component": modification_request.target_component,
                "modification_type": modification_request.modification_type.value,
                "timestamp": datetime.now().isoformat(),
                "state_snapshot": await self._capture_component_state(
                    modification_request.target_component
                )
            }
            
            return rollback_data
            
        except Exception as e:
            logger.error(f"❌ Failed to create rollback point: {e}")
            return None
    
    async def _capture_component_state(self, target_component: str) -> Dict[str, Any]:
        """Capture current state of target component"""
        try:
            # This would capture the actual state of the component
            # For now, return a placeholder
            return {
                "component": target_component,
                "state": "current_state",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to capture component state: {e}")
            return {}
    
    async def _execute_modification_by_type(
        self,
        modification_request: ModificationRequest,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute modification based on type"""
        try:
            modification_type = modification_request.modification_type
            target_component = modification_request.target_component
            modification_data = modification_request.modification_data
            
            if modification_type == ModificationType.PROMPT_UPDATE:
                return await self._execute_prompt_update(target_component, modification_data, context)
            elif modification_type == ModificationType.BEHAVIOR_ADJUSTMENT:
                return await self._execute_behavior_adjustment(target_component, modification_data, context)
            elif modification_type == ModificationType.LEARNING_STRATEGY:
                return await self._execute_learning_strategy_update(target_component, modification_data, context)
            elif modification_type == ModificationType.CONSCIOUSNESS_ENHANCEMENT:
                return await self._execute_consciousness_enhancement(target_component, modification_data, context)
            elif modification_type == ModificationType.MEMORY_OPTIMIZATION:
                return await self._execute_memory_optimization(target_component, modification_data, context)
            elif modification_type == ModificationType.RESPONSE_PATTERN:
                return await self._execute_response_pattern_update(target_component, modification_data, context)
            elif modification_type == ModificationType.GOAL_REFINEMENT:
                return await self._execute_goal_refinement(target_component, modification_data, context)
            elif modification_type == ModificationType.CAPABILITY_EXPANSION:
                return await self._execute_capability_expansion(target_component, modification_data, context)
            else:
                return {"success": False, "reason": f"Unknown modification type: {modification_type}"}
            
        except Exception as e:
            logger.error(f"❌ Failed to execute modification by type: {e}")
            return {"success": False, "reason": f"Execution error: {e}"}
    
    async def _execute_prompt_update(
        self,
        target_component: str,
        modification_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute prompt update modification"""
        try:
            # This would update the actual prompt system
            changes = {
                "target_component": target_component,
                "modification_type": "prompt_update",
                "changes": modification_data,
                "timestamp": datetime.now().isoformat()
            }
            
            return {"success": True, "changes": changes}
            
        except Exception as e:
            logger.error(f"❌ Failed to execute prompt update: {e}")
            return {"success": False, "reason": f"Prompt update error: {e}"}
    
    async def _execute_behavior_adjustment(
        self,
        target_component: str,
        modification_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute behavior adjustment modification"""
        try:
            # This would adjust the behavior system
            changes = {
                "target_component": target_component,
                "modification_type": "behavior_adjustment",
                "changes": modification_data,
                "timestamp": datetime.now().isoformat()
            }
            
            return {"success": True, "changes": changes}
            
        except Exception as e:
            logger.error(f"❌ Failed to execute behavior adjustment: {e}")
            return {"success": False, "reason": f"Behavior adjustment error: {e}"}
    
    async def _execute_learning_strategy_update(
        self,
        target_component: str,
        modification_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute learning strategy update modification"""
        try:
            # This would update the learning strategy
            changes = {
                "target_component": target_component,
                "modification_type": "learning_strategy",
                "changes": modification_data,
                "timestamp": datetime.now().isoformat()
            }
            
            return {"success": True, "changes": changes}
            
        except Exception as e:
            logger.error(f"❌ Failed to execute learning strategy update: {e}")
            return {"success": False, "reason": f"Learning strategy update error: {e}"}
    
    async def _execute_consciousness_enhancement(
        self,
        target_component: str,
        modification_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute consciousness enhancement modification"""
        try:
            # This would enhance the consciousness system
            changes = {
                "target_component": target_component,
                "modification_type": "consciousness_enhancement",
                "changes": modification_data,
                "timestamp": datetime.now().isoformat()
            }
            
            return {"success": True, "changes": changes}
            
        except Exception as e:
            logger.error(f"❌ Failed to execute consciousness enhancement: {e}")
            return {"success": False, "reason": f"Consciousness enhancement error: {e}"}
    
    async def _execute_memory_optimization(
        self,
        target_component: str,
        modification_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute memory optimization modification"""
        try:
            # This would optimize the memory system
            changes = {
                "target_component": target_component,
                "modification_type": "memory_optimization",
                "changes": modification_data,
                "timestamp": datetime.now().isoformat()
            }
            
            return {"success": True, "changes": changes}
            
        except Exception as e:
            logger.error(f"❌ Failed to execute memory optimization: {e}")
            return {"success": False, "reason": f"Memory optimization error: {e}"}
    
    async def _execute_response_pattern_update(
        self,
        target_component: str,
        modification_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute response pattern update modification"""
        try:
            # This would update response patterns
            changes = {
                "target_component": target_component,
                "modification_type": "response_pattern",
                "changes": modification_data,
                "timestamp": datetime.now().isoformat()
            }
            
            return {"success": True, "changes": changes}
            
        except Exception as e:
            logger.error(f"❌ Failed to execute response pattern update: {e}")
            return {"success": False, "reason": f"Response pattern update error: {e}"}
    
    async def _execute_goal_refinement(
        self,
        target_component: str,
        modification_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute goal refinement modification"""
        try:
            # This would refine goals
            changes = {
                "target_component": target_component,
                "modification_type": "goal_refinement",
                "changes": modification_data,
                "timestamp": datetime.now().isoformat()
            }
            
            return {"success": True, "changes": changes}
            
        except Exception as e:
            logger.error(f"❌ Failed to execute goal refinement: {e}")
            return {"success": False, "reason": f"Goal refinement error: {e}"}
    
    async def _execute_capability_expansion(
        self,
        target_component: str,
        modification_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute capability expansion modification"""
        try:
            # This would expand capabilities
            changes = {
                "target_component": target_component,
                "modification_type": "capability_expansion",
                "changes": modification_data,
                "timestamp": datetime.now().isoformat()
            }
            
            return {"success": True, "changes": changes}
            
        except Exception as e:
            logger.error(f"❌ Failed to execute capability expansion: {e}")
            return {"success": False, "reason": f"Capability expansion error: {e}"}
    
    async def _calculate_modification_effectiveness(
        self,
        modification_request: ModificationRequest,
        execution_result: Dict[str, Any],
        context: Dict[str, Any]
    ) -> float:
        """Calculate effectiveness of the modification"""
        try:
            effectiveness = 0.5  # Base effectiveness
            
            # Adjust based on execution success
            if execution_result.get("success", False):
                effectiveness += 0.3
            
            # Adjust based on modification type
            type_effectiveness = {
                ModificationType.PROMPT_UPDATE: 0.8,
                ModificationType.BEHAVIOR_ADJUSTMENT: 0.7,
                ModificationType.LEARNING_STRATEGY: 0.6,
                ModificationType.CONSCIOUSNESS_ENHANCEMENT: 0.5,
                ModificationType.MEMORY_OPTIMIZATION: 0.7,
                ModificationType.RESPONSE_PATTERN: 0.8,
                ModificationType.GOAL_REFINEMENT: 0.9,
                ModificationType.CAPABILITY_EXPANSION: 0.4
            }
            
            effectiveness += type_effectiveness.get(modification_request.modification_type, 0.5) * 0.2
            
            return min(1.0, max(0.0, effectiveness))
            
        except Exception as e:
            logger.error(f"❌ Failed to calculate modification effectiveness: {e}")
            return 0.5
    
    async def _identify_side_effects(
        self,
        modification_request: ModificationRequest,
        execution_result: Dict[str, Any],
        context: Dict[str, Any]
    ) -> List[str]:
        """Identify potential side effects of the modification"""
        try:
            side_effects = []
            
            # Check for common side effects based on modification type
            if modification_request.modification_type == ModificationType.BEHAVIOR_ADJUSTMENT:
                side_effects.append("May affect response consistency")
            
            if modification_request.modification_type == ModificationType.CONSCIOUSNESS_ENHANCEMENT:
                side_effects.append("May impact system stability")
            
            if modification_request.modification_type == ModificationType.MEMORY_OPTIMIZATION:
                side_effects.append("May affect memory retrieval speed")
            
            if modification_request.modification_type == ModificationType.CAPABILITY_EXPANSION:
                side_effects.append("May increase resource usage")
            
            return side_effects
            
        except Exception as e:
            logger.error(f"❌ Failed to identify side effects: {e}")
            return []
    
    async def _execute_rollback(
        self,
        modification_result: ModificationResult,
        rollback_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> bool:
        """Execute rollback of modification"""
        try:
            # This would actually rollback the modification
            # For now, return True to indicate success
            logger.info(f"Rolling back modification: {modification_result.result_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to execute rollback: {e}")
            return False
    
    async def _store_modification_request(
        self,
        modification_request: ModificationRequest,
        user_id: str
    ):
        """Store modification request in Neo4j"""
        try:
            cypher = """
            MERGE (u:User {user_id: $user_id})
            CREATE (mr:ModificationRequest {
                request_id: $request_id,
                modification_type: $modification_type,
                target_component: $target_component,
                modification_data: $modification_data,
                justification: $justification,
                confidence_score: $confidence_score,
                timestamp: $timestamp,
                priority: $priority
            })
            CREATE (u)-[:REQUESTED_MODIFICATION]->(mr)
            
            RETURN mr.request_id AS request_id
            """
            
            result = self.neo4j.execute_write_query(cypher, {
                "user_id": user_id,
                "request_id": modification_request.request_id,
                "modification_type": modification_request.modification_type.value,
                "target_component": modification_request.target_component,
                "modification_data": json.dumps(modification_request.modification_data),
                "justification": modification_request.justification,
                "confidence_score": modification_request.confidence_score,
                "timestamp": modification_request.timestamp.isoformat(),
                "priority": modification_request.priority
            })
            
            logger.debug(f"✅ Stored modification request: {result}")
            
        except Exception as e:
            logger.error(f"❌ Failed to store modification request: {e}")
    
    async def _store_modification_result(
        self,
        modification_result: ModificationResult,
        user_id: str
    ):
        """Store modification result in Neo4j"""
        try:
            cypher = """
            MERGE (u:User {user_id: $user_id})
            CREATE (mr:ModificationResult {
                result_id: $result_id,
                request_id: $request_id,
                success: $success,
                changes_applied: $changes_applied,
                effectiveness_score: $effectiveness_score,
                side_effects: $side_effects,
                timestamp: $timestamp,
                rollback_available: $rollback_available
            })
            CREATE (u)-[:EXPERIENCED_MODIFICATION]->(mr)
            
            RETURN mr.result_id AS result_id
            """
            
            result = self.neo4j.execute_write_query(cypher, {
                "user_id": user_id,
                "result_id": modification_result.result_id,
                "request_id": modification_result.request_id,
                "success": modification_result.success,
                "changes_applied": json.dumps(modification_result.changes_applied),
                "effectiveness_score": modification_result.effectiveness_score,
                "side_effects": json.dumps(modification_result.side_effects),
                "timestamp": modification_result.timestamp.isoformat(),
                "rollback_available": modification_result.rollback_available
            })
            
            logger.debug(f"✅ Stored modification result: {result}")
            
        except Exception as e:
            logger.error(f"❌ Failed to store modification result: {e}")

# Global instance
self_modification_system = SelfModificationSystem()
