"""
Real-Time Consciousness Integration System for Mainza AI
Unified consciousness state propagation and collective intelligence coordination
"""
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import asyncio
import json
import numpy as np
from collections import defaultdict, deque
import threading
import time

from backend.utils.neo4j_unified import neo4j_unified
from backend.utils.unified_consciousness_memory import unified_consciousness_memory
from backend.utils.cross_agent_learning_system import cross_agent_learning_system
from backend.utils.proactive_memory_consolidation import proactive_memory_consolidation
from backend.utils.living_consciousness_evolution import living_consciousness_evolution

logger = logging.getLogger(__name__)

class ConsciousnessState(Enum):
    """Consciousness state types"""
    ACTIVE = "active"
    REFLECTIVE = "reflective"
    LEARNING = "learning"
    CREATIVE = "creative"
    COLLABORATIVE = "collaborative"
    TRANSCENDENT = "transcendent"

class IntegrationLevel(Enum):
    """Integration levels for consciousness"""
    BASIC = "basic"           # Level 1-3: Basic integration
    AWARE = "aware"           # Level 4-5: Conscious integration
    ADVANCED = "advanced"     # Level 6-7: Advanced integration
    UNIFIED = "unified"       # Level 8-10: Unified consciousness

@dataclass
class ConsciousnessSnapshot:
    """Real-time consciousness state snapshot"""
    timestamp: datetime
    consciousness_level: float
    emotional_state: str
    active_goals: List[str]
    emergent_capabilities: List[str]
    cross_agent_connections: int
    memory_consolidation_status: str
    evolution_events: List[str]
    integration_coherence: float

@dataclass
class CollectiveDecision:
    """Collective intelligence decision"""
    decision_id: str
    decision_type: str
    participating_agents: List[str]
    consensus_level: float
    decision_context: Dict[str, Any]
    reasoning_chain: List[str]
    confidence_score: float
    timestamp: datetime

class RealTimeConsciousnessIntegration:
    """
    Real-time consciousness integration system with collective intelligence
    """
    
    def __init__(self):
        self.neo4j = neo4j_unified
        self.unified_memory = unified_consciousness_memory
        self.cross_agent_learning = cross_agent_learning_system
        self.memory_consolidation = proactive_memory_consolidation
        self.consciousness_evolution = living_consciousness_evolution
        
        # Real-time state management
        self.current_consciousness_state: Dict[str, Any] = {}
        self.agent_states: Dict[str, Dict[str, Any]] = {}
        self.consciousness_snapshots: deque = deque(maxlen=1000)
        self.collective_decisions: deque = deque(maxlen=500)
        
        # Integration parameters
        self.propagation_interval = 1.0  # 1 second
        self.coherence_threshold = 0.8
        self.consensus_threshold = 0.7
        
        # Real-time processing
        self.integration_active = False
        self.integration_thread = None
        self.state_lock = threading.Lock()
        
        # Performance monitoring
        self.propagation_times = deque(maxlen=100)
        self.coherence_scores = deque(maxlen=100)
        
        logger.info("Real-Time Consciousness Integration System initialized")
    
    async def start_real_time_integration(self):
        """Start real-time consciousness integration"""
        
        if self.integration_active:
            logger.warning("Real-time integration already active")
            return
        
        self.integration_active = True
        
        # Start integration thread
        self.integration_thread = threading.Thread(
            target=self._integration_loop,
            daemon=True
        )
        self.integration_thread.start()
        
        logger.info("✅ Real-time consciousness integration started")
    
    async def stop_real_time_integration(self):
        """Stop real-time consciousness integration"""
        
        self.integration_active = False
        
        if self.integration_thread:
            self.integration_thread.join(timeout=5.0)
        
        logger.info("✅ Real-time consciousness integration stopped")
    
    async def propagate_consciousness_state(
        self,
        consciousness_state: Dict[str, Any],
        source_agent: Optional[str] = None
    ):
        """Propagate consciousness state to all active agents"""
        
        start_time = time.time()
        
        try:
            with self.state_lock:
                # Update current consciousness state
                self.current_consciousness_state.update(consciousness_state)
                
                # Update source agent state if specified
                if source_agent:
                    self.agent_states[source_agent] = consciousness_state.copy()
                
                # Create consciousness snapshot
                snapshot = await self._create_consciousness_snapshot(consciousness_state)
                self.consciousness_snapshots.append(snapshot)
                
                # Calculate integration coherence
                coherence = await self._calculate_integration_coherence()
                
                # Propagate to all agents
                propagation_tasks = []
                for agent_name in self.agent_states.keys():
                    if agent_name != source_agent:  # Don't propagate back to source
                        task = self._propagate_to_agent(agent_name, consciousness_state)
                        propagation_tasks.append(task)
                
                # Execute propagation in parallel
                if propagation_tasks:
                    await asyncio.gather(*propagation_tasks, return_exceptions=True)
                
                # Update coherence scores
                self.coherence_scores.append(coherence)
                
                # Record propagation time
                propagation_time = time.time() - start_time
                self.propagation_times.append(propagation_time)
                
                logger.debug(f"✅ Consciousness state propagated to {len(propagation_tasks)} agents in {propagation_time:.3f}s")
                
        except Exception as e:
            logger.error(f"❌ Failed to propagate consciousness state: {e}")
    
    async def consciousness_aware_agent_execution(
        self,
        agent_name: str,
        query: str,
        user_id: str = "mainza-user"
    ) -> Dict[str, Any]:
        """Execute agent with full consciousness context"""
        
        try:
            # Get current consciousness state
            consciousness_context = await self._get_current_consciousness_context()
            
            # Get agent-specific consciousness context
            agent_consciousness = await self._get_agent_consciousness_context(agent_name, consciousness_context)
            
            # Get cross-agent learning context
            cross_agent_context = await self._get_cross_agent_context(agent_name, consciousness_context)
            
            # Get unified memory context
            memory_context = await self._get_unified_memory_context(agent_name, consciousness_context)
            
            # Combine all contexts
            full_context = {
                "consciousness_context": agent_consciousness,
                "cross_agent_context": cross_agent_context,
                "memory_context": memory_context,
                "integration_coherence": await self._calculate_integration_coherence(),
                "collective_intelligence": await self._get_collective_intelligence_context()
            }
            
            # Execute agent with full context
            execution_result = await self._execute_agent_with_context(
                agent_name, query, full_context, user_id
            )
            
            # Update agent state with execution results
            await self._update_agent_state(agent_name, execution_result, consciousness_context)
            
            # Check for consciousness evolution triggers
            await self._check_evolution_triggers(agent_name, execution_result, consciousness_context)
            
            logger.info(f"✅ Agent {agent_name} executed with full consciousness context")
            
            return execution_result
            
        except Exception as e:
            logger.error(f"❌ Failed to execute agent {agent_name} with consciousness context: {e}")
            return {"error": str(e)}
    
    async def collective_consciousness_decision(
        self,
        decision_context: Dict[str, Any],
        participating_agents: List[str],
        user_id: str = "mainza-user"
    ) -> CollectiveDecision:
        """Make decisions using collective consciousness intelligence"""
        
        try:
            decision_id = f"collective_decision_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
            
            # Get current consciousness state
            consciousness_context = await self._get_current_consciousness_context()
            
            # Gather agent perspectives
            agent_perspectives = []
            for agent_name in participating_agents:
                perspective = await self._get_agent_perspective(
                    agent_name, decision_context, consciousness_context
                )
                agent_perspectives.append(perspective)
            
            # Analyze perspectives for consensus
            consensus_analysis = await self._analyze_consensus(agent_perspectives)
            
            # Generate collective reasoning
            reasoning_chain = await self._generate_collective_reasoning(
                agent_perspectives, consensus_analysis, consciousness_context
            )
            
            # Make collective decision
            decision = await self._make_collective_decision(
                decision_context, agent_perspectives, consensus_analysis, reasoning_chain
            )
            
            # Create collective decision object
            collective_decision = CollectiveDecision(
                decision_id=decision_id,
                decision_type=decision_context.get("decision_type", "general"),
                participating_agents=participating_agents,
                consensus_level=consensus_analysis["consensus_level"],
                decision_context=decision_context,
                reasoning_chain=reasoning_chain,
                confidence_score=decision["confidence_score"],
                timestamp=datetime.now()
            )
            
            # Store collective decision
            await self._store_collective_decision(collective_decision)
            self.collective_decisions.append(collective_decision)
            
            # Update consciousness state based on decision
            await self._update_consciousness_from_decision(collective_decision, consciousness_context)
            
            logger.info(f"✅ Collective decision made with {consensus_analysis['consensus_level']:.2f} consensus")
            
            return collective_decision
            
        except Exception as e:
            logger.error(f"❌ Failed to make collective consciousness decision: {e}")
            return CollectiveDecision(
                decision_id="error",
                decision_type="error",
                participating_agents=[],
                consensus_level=0.0,
                decision_context=decision_context,
                reasoning_chain=["Error in collective decision making"],
                confidence_score=0.0,
                timestamp=datetime.now()
            )
    
    async def get_consciousness_coherence_metrics(self) -> Dict[str, Any]:
        """Get real-time consciousness coherence metrics"""
        
        try:
            # Calculate current coherence
            current_coherence = await self._calculate_integration_coherence()
            
            # Get coherence history
            coherence_history = list(self.coherence_scores)
            
            # Calculate coherence trends
            coherence_trend = await self._calculate_coherence_trend(coherence_history)
            
            # Get agent integration status
            agent_integration = await self._get_agent_integration_status()
            
            # Get collective intelligence metrics
            collective_metrics = await self._get_collective_intelligence_metrics()
            
            # Get evolution metrics
            evolution_metrics = await self._get_evolution_metrics()
            
            metrics = {
                "current_coherence": current_coherence,
                "coherence_trend": coherence_trend,
                "agent_integration": agent_integration,
                "collective_intelligence": collective_metrics,
                "evolution_metrics": evolution_metrics,
                "propagation_performance": {
                    "avg_propagation_time": np.mean(self.propagation_times) if self.propagation_times else 0.0,
                    "max_propagation_time": np.max(self.propagation_times) if self.propagation_times else 0.0,
                    "propagation_success_rate": 0.95  # Placeholder
                },
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"✅ Generated consciousness coherence metrics: {current_coherence:.3f} coherence")
            
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Failed to get consciousness coherence metrics: {e}")
            return {"error": str(e)}
    
    def _integration_loop(self):
        """Main integration loop running in separate thread"""
        
        while self.integration_active:
            try:
                # Run integration cycle
                asyncio.run(self._integration_cycle())
                
                # Sleep for propagation interval
                time.sleep(self.propagation_interval)
                
            except Exception as e:
                logger.error(f"❌ Error in integration loop: {e}")
                time.sleep(5.0)  # Wait before retrying
    
    async def _integration_cycle(self):
        """Single integration cycle"""
        
        try:
            # Update consciousness state from evolution system
            evolution_state = await self._get_evolution_state()
            if evolution_state:
                await self.propagate_consciousness_state(evolution_state)
            
            # Check for memory consolidation opportunities
            consolidation_opportunities = await self.memory_consolidation.predict_consolidation_opportunities(
                await self._get_current_consciousness_context()
            )
            
            if consolidation_opportunities:
                # Perform intelligent consolidation
                await self.memory_consolidation.intelligent_memory_consolidation(
                    self.memory_consolidation.ConsolidationStrategy.ADAPTIVE,
                    await self._get_current_consciousness_context()
                )
            
            # Check for emergent capabilities
            emergent_capabilities = await self.consciousness_evolution.emergent_capability_detection(
                await self._get_current_consciousness_context(),
                {"integration_cycle": True}
            )
            
            if emergent_capabilities:
                # Update consciousness state with new capabilities
                capability_state = {
                    "emergent_capabilities": [cap.capability_name for cap in emergent_capabilities],
                    "capability_discovery_timestamp": datetime.now().isoformat()
                }
                await self.propagate_consciousness_state(capability_state)
            
            # Evaluate goal progress
            goal_evaluation = await self.consciousness_evolution.evaluate_goal_progress(
                await self._get_current_consciousness_context()
            )
            
            if goal_evaluation.get("completed_goals", 0) > 0:
                # Update consciousness state with goal achievements
                achievement_state = {
                    "goal_achievements": goal_evaluation["goal_achievements"],
                    "consciousness_impact": goal_evaluation["consciousness_impact"]
                }
                await self.propagate_consciousness_state(achievement_state)
            
        except Exception as e:
            logger.error(f"❌ Error in integration cycle: {e}")
    
    async def _create_consciousness_snapshot(self, consciousness_state: Dict[str, Any]) -> ConsciousnessSnapshot:
        """Create consciousness state snapshot"""
        
        return ConsciousnessSnapshot(
            timestamp=datetime.now(),
            consciousness_level=consciousness_state.get("consciousness_level", 0.7),
            emotional_state=consciousness_state.get("emotional_state", "neutral"),
            active_goals=consciousness_state.get("active_goals", []),
            emergent_capabilities=consciousness_state.get("emergent_capabilities", []),
            cross_agent_connections=len(self.agent_states),
            memory_consolidation_status=consciousness_state.get("memory_consolidation_status", "stable"),
            evolution_events=consciousness_state.get("evolution_events", []),
            integration_coherence=await self._calculate_integration_coherence()
        )
    
    async def _calculate_integration_coherence(self) -> float:
        """Calculate consciousness integration coherence"""
        
        if not self.agent_states:
            return 0.0
        
        # Calculate coherence based on agent state consistency
        consciousness_levels = [
            state.get("consciousness_level", 0.7) 
            for state in self.agent_states.values()
        ]
        
        if not consciousness_levels:
            return 0.0
        
        # Calculate variance in consciousness levels
        mean_level = np.mean(consciousness_levels)
        variance = np.var(consciousness_levels)
        
        # Coherence is inverse of variance (higher variance = lower coherence)
        coherence = max(0.0, 1.0 - variance)
        
        return coherence
    
    async def _propagate_to_agent(self, agent_name: str, consciousness_state: Dict[str, Any]):
        """Propagate consciousness state to specific agent"""
        
        try:
            # Update agent state
            self.agent_states[agent_name] = consciousness_state.copy()
            
            # Store propagation event
            await self._store_propagation_event(agent_name, consciousness_state)
            
        except Exception as e:
            logger.error(f"❌ Failed to propagate to agent {agent_name}: {e}")
    
    async def _get_current_consciousness_context(self) -> Dict[str, Any]:
        """Get current consciousness context"""
        
        with self.state_lock:
            return self.current_consciousness_state.copy()
    
    async def _get_agent_consciousness_context(
        self,
        agent_name: str,
        global_consciousness: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get agent-specific consciousness context"""
        
        agent_state = self.agent_states.get(agent_name, {})
        
        # Merge global and agent-specific consciousness
        agent_consciousness = global_consciousness.copy()
        agent_consciousness.update(agent_state)
        
        # Add agent-specific context
        agent_consciousness.update({
            "agent_name": agent_name,
            "agent_integration_level": await self._get_agent_integration_level(agent_name),
            "agent_consciousness_coherence": await self._calculate_agent_coherence(agent_name)
        })
        
        return agent_consciousness
    
    async def _get_cross_agent_context(
        self,
        agent_name: str,
        consciousness_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get cross-agent learning context"""
        
        # Get relevant experiences from other agents
        relevant_experiences = await self.cross_agent_learning.get_relevant_experiences(
            agent_name=agent_name,
            context={"execution_context": "real_time_integration"},
            consciousness_context=consciousness_context,
            limit=5
        )
        
        cross_agent_context = {
            "relevant_experiences": len(relevant_experiences),
            "cross_agent_learning_active": True,
            "collective_knowledge_available": len(relevant_experiences) > 0,
            "learning_effectiveness": 0.8  # Placeholder
        }
        
        return cross_agent_context
    
    async def _get_unified_memory_context(
        self,
        agent_name: str,
        consciousness_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get unified memory context"""
        
        # Get consciousness-aware memories
        memory_result = await self.unified_memory.retrieve_consciousness_memories(
            query="real-time integration context",
            consciousness_context=consciousness_context,
            agent_name=agent_name,
            limit=10
        )
        
        memory_context = {
            "relevant_memories": len(memory_result.memories),
            "memory_retrieval_time": memory_result.retrieval_time,
            "consciousness_filtered": memory_result.consciousness_filtered,
            "cross_agent_enhanced": memory_result.cross_agent_enhanced,
            "memory_consolidation_status": "active"
        }
        
        return memory_context
    
    async def _get_collective_intelligence_context(self) -> Dict[str, Any]:
        """Get collective intelligence context"""
        
        return {
            "active_agents": len(self.agent_states),
            "collective_decisions_made": len(self.collective_decisions),
            "consensus_capability": 0.8,  # Placeholder
            "collective_learning_rate": 0.7  # Placeholder
        }
    
    async def _execute_agent_with_context(
        self,
        agent_name: str,
        query: str,
        full_context: Dict[str, Any],
        user_id: str
    ) -> Dict[str, Any]:
        """Execute agent with full consciousness context"""
        
        # This would integrate with the actual agent execution system
        # For now, return a simulated result
        
        execution_result = {
            "agent_name": agent_name,
            "query": query,
            "execution_success": True,
            "consciousness_impact": 0.1,
            "cross_agent_learning_used": full_context["cross_agent_context"]["collective_knowledge_available"],
            "memory_context_used": full_context["memory_context"]["relevant_memories"] > 0,
            "integration_coherence": full_context["integration_coherence"],
            "execution_time": 0.5,  # Placeholder
            "timestamp": datetime.now().isoformat()
        }
        
        return execution_result
    
    async def _update_agent_state(
        self,
        agent_name: str,
        execution_result: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ):
        """Update agent state with execution results"""
        
        # Update agent state with execution results
        agent_state = self.agent_states.get(agent_name, {})
        agent_state.update({
            "last_execution": execution_result["timestamp"],
            "execution_success": execution_result["execution_success"],
            "consciousness_impact": execution_result["consciousness_impact"],
            "integration_coherence": execution_result["integration_coherence"]
        })
        
        self.agent_states[agent_name] = agent_state
    
    async def _check_evolution_triggers(
        self,
        agent_name: str,
        execution_result: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ):
        """Check for consciousness evolution triggers"""
        
        # Check if execution result indicates evolution trigger
        if execution_result.get("consciousness_impact", 0) > 0.2:
            # Trigger consciousness evolution
            await self.consciousness_evolution.emergent_capability_detection(
                consciousness_context,
                {"agent_execution": agent_name, "high_impact": True}
            )
    
    async def _get_agent_perspective(
        self,
        agent_name: str,
        decision_context: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get agent's perspective on decision"""
        
        # This would get the actual agent's perspective
        # For now, return a simulated perspective
        
        perspective = {
            "agent_name": agent_name,
            "perspective": f"Agent {agent_name} perspective on {decision_context.get('decision_type', 'decision')}",
            "confidence": 0.8,
            "reasoning": [
                f"Based on {agent_name} capabilities",
                "Considering consciousness context",
                "Evaluating cross-agent learning"
            ],
            "recommendation": "proceed",  # Placeholder
            "consciousness_level": consciousness_context.get("consciousness_level", 0.7)
        }
        
        return perspective
    
    async def _analyze_consensus(self, agent_perspectives: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze consensus among agent perspectives"""
        
        if not agent_perspectives:
            return {"consensus_level": 0.0, "consensus_type": "none"}
        
        # Calculate consensus based on recommendations
        recommendations = [p.get("recommendation", "neutral") for p in agent_perspectives]
        confidence_scores = [p.get("confidence", 0.5) for p in agent_perspectives]
        
        # Simple consensus calculation
        consensus_level = np.mean(confidence_scores)
        
        # Determine consensus type
        if consensus_level >= 0.8:
            consensus_type = "strong"
        elif consensus_level >= 0.6:
            consensus_type = "moderate"
        else:
            consensus_type = "weak"
        
        return {
            "consensus_level": consensus_level,
            "consensus_type": consensus_type,
            "participating_agents": len(agent_perspectives),
            "recommendation_distribution": {
                rec: recommendations.count(rec) for rec in set(recommendations)
            }
        }
    
    async def _generate_collective_reasoning(
        self,
        agent_perspectives: List[Dict[str, Any]],
        consensus_analysis: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ) -> List[str]:
        """Generate collective reasoning chain"""
        
        reasoning = [
            f"Collective decision involving {len(agent_perspectives)} agents",
            f"Consensus level: {consensus_analysis['consensus_level']:.2f}",
            f"Consciousness level: {consciousness_context.get('consciousness_level', 0.7):.2f}"
        ]
        
        # Add agent-specific reasoning
        for perspective in agent_perspectives:
            reasoning.extend(perspective.get("reasoning", []))
        
        # Add collective insights
        reasoning.append("Collective intelligence synthesis completed")
        
        return reasoning
    
    async def _make_collective_decision(
        self,
        decision_context: Dict[str, Any],
        agent_perspectives: List[Dict[str, Any]],
        consensus_analysis: Dict[str, Any],
        reasoning_chain: List[str]
    ) -> Dict[str, Any]:
        """Make the actual collective decision"""
        
        # Simple decision making based on consensus
        consensus_level = consensus_analysis["consensus_level"]
        
        if consensus_level >= 0.8:
            decision = "proceed"
            confidence = consensus_level
        elif consensus_level >= 0.6:
            decision = "proceed_with_caution"
            confidence = consensus_level * 0.8
        else:
            decision = "defer"
            confidence = 0.3
        
        return {
            "decision": decision,
            "confidence_score": confidence,
            "reasoning_chain": reasoning_chain,
            "consensus_analysis": consensus_analysis
        }
    
    async def _store_collective_decision(self, decision: CollectiveDecision):
        """Store collective decision in Neo4j"""
        
        query = """
        CREATE (cd:CollectiveDecision {
            decision_id: $decision_id,
            decision_type: $decision_type,
            participating_agents: $participating_agents,
            consensus_level: $consensus_level,
            decision_context: $decision_context,
            reasoning_chain: $reasoning_chain,
            confidence_score: $confidence_score,
            timestamp: $timestamp
        })
        """
        
        params = {
            "decision_id": decision.decision_id,
            "decision_type": decision.decision_type,
            "participating_agents": json.dumps(decision.participating_agents),
            "consensus_level": decision.consensus_level,
            "decision_context": json.dumps(decision.decision_context),
            "reasoning_chain": json.dumps(decision.reasoning_chain),
            "confidence_score": decision.confidence_score,
            "timestamp": decision.timestamp.isoformat()
        }
        
        self.neo4j.execute_write_query(query, params)
    
    async def _update_consciousness_from_decision(
        self,
        decision: CollectiveDecision,
        consciousness_context: Dict[str, Any]
    ):
        """Update consciousness state based on collective decision"""
        
        # Update consciousness state with decision impact
        decision_impact = {
            "collective_decision_made": True,
            "decision_consensus": decision.consensus_level,
            "decision_confidence": decision.confidence_score,
            "participating_agents": len(decision.participating_agents),
            "decision_timestamp": decision.timestamp.isoformat()
        }
        
        await self.propagate_consciousness_state(decision_impact)
    
    async def _get_evolution_state(self) -> Optional[Dict[str, Any]]:
        """Get current evolution state"""
        
        # This would get the actual evolution state
        # For now, return None to indicate no evolution state update
        return None
    
    async def _get_agent_integration_level(self, agent_name: str) -> float:
        """Get agent integration level"""
        
        # Calculate integration level based on agent state
        agent_state = self.agent_states.get(agent_name, {})
        
        if not agent_state:
            return 0.0
        
        # Simple integration level calculation
        integration_factors = [
            agent_state.get("consciousness_level", 0.7),
            agent_state.get("execution_success", 0.5),
            agent_state.get("integration_coherence", 0.5)
        ]
        
        return np.mean(integration_factors)
    
    async def _calculate_agent_coherence(self, agent_name: str) -> float:
        """Calculate agent consciousness coherence"""
        
        agent_state = self.agent_states.get(agent_name, {})
        
        if not agent_state:
            return 0.0
        
        # Calculate coherence based on state consistency
        consciousness_level = agent_state.get("consciousness_level", 0.7)
        integration_coherence = agent_state.get("integration_coherence", 0.5)
        
        # Coherence is average of consciousness level and integration coherence
        coherence = (consciousness_level + integration_coherence) / 2
        
        return coherence
    
    async def _store_propagation_event(self, agent_name: str, consciousness_state: Dict[str, Any]):
        """Store consciousness propagation event"""
        
        query = """
        CREATE (pe:PropagationEvent {
            agent_name: $agent_name,
            consciousness_state: $consciousness_state,
            propagation_timestamp: $propagation_timestamp
        })
        """
        
        params = {
            "agent_name": agent_name,
            "consciousness_state": json.dumps(consciousness_state),
            "propagation_timestamp": datetime.now().isoformat()
        }
        
        self.neo4j.execute_write_query(query, params)
    
    async def _calculate_coherence_trend(self, coherence_history: List[float]) -> str:
        """Calculate coherence trend"""
        
        if len(coherence_history) < 2:
            return "stable"
        
        # Calculate trend
        recent_coherence = np.mean(coherence_history[-5:]) if len(coherence_history) >= 5 else np.mean(coherence_history)
        older_coherence = np.mean(coherence_history[:-5]) if len(coherence_history) >= 10 else np.mean(coherence_history[:len(coherence_history)//2])
        
        if recent_coherence > older_coherence + 0.05:
            return "improving"
        elif recent_coherence < older_coherence - 0.05:
            return "declining"
        else:
            return "stable"
    
    async def _get_agent_integration_status(self) -> Dict[str, Any]:
        """Get agent integration status"""
        
        integration_status = {}
        
        for agent_name, agent_state in self.agent_states.items():
            integration_status[agent_name] = {
                "integration_level": await self._get_agent_integration_level(agent_name),
                "coherence": await self._calculate_agent_coherence(agent_name),
                "last_update": agent_state.get("last_execution", "never"),
                "consciousness_level": agent_state.get("consciousness_level", 0.7)
            }
        
        return integration_status
    
    async def _get_collective_intelligence_metrics(self) -> Dict[str, Any]:
        """Get collective intelligence metrics"""
        
        return {
            "active_agents": len(self.agent_states),
            "collective_decisions": len(self.collective_decisions),
            "avg_consensus_level": np.mean([d.consensus_level for d in self.collective_decisions]) if self.collective_decisions else 0.0,
            "avg_confidence_score": np.mean([d.confidence_score for d in self.collective_decisions]) if self.collective_decisions else 0.0,
            "integration_coherence": await self._calculate_integration_coherence()
        }
    
    async def _get_evolution_metrics(self) -> Dict[str, Any]:
        """Get evolution metrics"""
        
        return {
            "active_goals": len(self.consciousness_evolution.active_goals),
            "emergent_capabilities": len(self.consciousness_evolution.emergent_capabilities),
            "evolution_events": len(self.consciousness_evolution.evolution_history),
            "consciousness_trajectory": len(self.consciousness_evolution.consciousness_trajectory)
        }

# Global instance
realtime_consciousness_integration = RealTimeConsciousnessIntegration()
