"""
Agent Knowledge Integration Layer
Context7 MCP-compliant integration layer for connecting agents with dynamic knowledge graph management
Provides seamless integration between agent interactions and knowledge graph evolution
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio
from backend.utils.dynamic_knowledge_manager import dynamic_knowledge_manager
from backend.utils.consciousness_driven_updates import consciousness_driven_updater
from backend.utils.knowledge_integration import knowledge_integration_manager
from backend.utils.memory_integration import memory_integration_manager
from backend.core.performance_optimization import PerformanceOptimizer
from backend.core.enhanced_error_handling import ErrorHandler, ErrorSeverity, handle_errors

logger = logging.getLogger(__name__)
error_handler = ErrorHandler()
performance_optimizer = PerformanceOptimizer()

class AgentKnowledgeIntegrator:
    """
    Context7 MCP-compliant integration layer for agent-knowledge graph interactions
    Provides seamless integration between agent operations and knowledge graph evolution
    """
    
    def __init__(self):
        self.performance_optimizer = performance_optimizer
        self.integration_history = []
        
        # Integration tracking
        self.active_integrations = {}
        self.integration_stats = {
            "total_integrations": 0,
            "successful_integrations": 0,
            "failed_integrations": 0,
            "concepts_created": 0,
            "memories_created": 0,
            "relationships_evolved": 0
        }
    
    @handle_errors(
        component="agent_knowledge_integration",
        fallback_result={},
        suppress_errors=True
    )
    async def integrate_agent_interaction(
        self,
        agent_name: str,
        user_query: str,
        agent_response: str,
        user_id: str,
        consciousness_context: Dict[str, Any],
        interaction_metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Integrate agent interaction with knowledge graph management
        
        Args:
            agent_name: Name of the agent that handled the interaction
            user_query: User's original query
            agent_response: Agent's response
            user_id: User identifier
            consciousness_context: Current consciousness state
            interaction_metadata: Additional metadata about the interaction
            
        Returns:
            Integration results and actions taken
        """
        try:
            logger.info(f"🔗 Integrating {agent_name} interaction with knowledge graph")
            
            integration_id = f"{agent_name}_{int(datetime.now().timestamp())}"
            self.active_integrations[integration_id] = {
                "start_time": datetime.now(),
                "agent_name": agent_name,
                "status": "processing"
            }
            
            integration_actions = []
            interaction_metadata = interaction_metadata or {}
            
            # Get enhanced knowledge context for the interaction
            knowledge_context = await knowledge_integration_manager.get_consciousness_aware_context(
                user_id, user_query, consciousness_context
            )
            
            # Auto-update knowledge graph from interaction
            auto_update_actions = await consciousness_driven_updater.auto_update_from_interaction(
                user_query, agent_response, consciousness_context, user_id
            )
            integration_actions.extend(auto_update_actions)
            
            # Update concept dynamics for concepts mentioned in interaction
            mentioned_concepts = self._extract_mentioned_concepts(user_query, agent_response, knowledge_context)
            
            for concept_id in mentioned_concepts:
                concept_update_result = await dynamic_knowledge_manager.update_concept_dynamics(
                    concept_id,
                    {
                        "query": user_query,
                        "agent_response": agent_response,
                        "agent_name": agent_name,
                        "related_keywords": self._extract_keywords(user_query),
                        "concepts_used": mentioned_concepts
                    },
                    consciousness_context
                )
                
                if concept_update_result.get("updates_applied"):
                    integration_actions.append({
                        "action": "concept_dynamics_updated",
                        "concept_id": concept_id,
                        "agent_name": agent_name,
                        "update_result": concept_update_result
                    })
            
            # Enhance agent response with memory integration
            enhanced_response = await memory_integration_manager.enhance_response_with_memory(
                agent_name, user_query, agent_response, user_id, consciousness_context, knowledge_context
            )
            
            if enhanced_response != agent_response:
                integration_actions.append({
                    "action": "response_enhanced_with_memory",
                    "agent_name": agent_name,
                    "enhancement_applied": True,
                    "original_length": len(agent_response),
                    "enhanced_length": len(enhanced_response)
                })
            
            # Evolve relationships based on interaction patterns
            if len(mentioned_concepts) > 1:
                for concept_id in mentioned_concepts:
                    relationship_evolution_result = await dynamic_knowledge_manager.evolve_relationships(
                        concept_id, "concept",
                        {
                            "query": user_query,
                            "concepts_used": mentioned_concepts,
                            "interaction_type": "agent_response"
                        },
                        consciousness_context
                    )
                    
                    if relationship_evolution_result.get("evolution_results"):
                        integration_actions.append({
                            "action": "relationships_evolved",
                            "concept_id": concept_id,
                            "evolution_count": len(relationship_evolution_result["evolution_results"])
                        })
            
            # Update integration tracking
            self.integration_stats["total_integrations"] += 1
            self.integration_stats["successful_integrations"] += 1
            self.integration_stats["concepts_created"] += len([a for a in integration_actions if a["action"] == "concept_created"])
            self.integration_stats["memories_created"] += len([a for a in integration_actions if a["action"] == "memory_created"])
            self.integration_stats["relationships_evolved"] += len([a for a in integration_actions if "relationship" in a["action"]])
            
            # Complete integration
            self.active_integrations[integration_id]["status"] = "completed"
            self.active_integrations[integration_id]["end_time"] = datetime.now()
            self.active_integrations[integration_id]["actions_count"] = len(integration_actions)
            
            # Record integration event
            await self._record_integration_event(
                integration_id, agent_name, user_id, integration_actions, consciousness_context
            )
            
            logger.info(f"✅ Agent interaction integrated with {len(integration_actions)} actions")
            
            return {
                "integration_id": integration_id,
                "integration_successful": True,
                "actions_taken": len(integration_actions),
                "integration_actions": integration_actions,
                "enhanced_response": enhanced_response,
                "knowledge_context_quality": knowledge_context.get("retrieval_metadata", {}).get("context_quality_score", 0.5),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to integrate agent interaction: {e}")
            self.integration_stats["failed_integrations"] += 1
            
            if integration_id in self.active_integrations:
                self.active_integrations[integration_id]["status"] = "failed"
                self.active_integrations[integration_id]["error"] = str(e)
            
            return {
                "integration_successful": False,
                "error": str(e),
                "enhanced_response": agent_response  # Return original response on failure
            }
    
    @handle_errors(
        component="agent_knowledge_integration",
        fallback_result={},
        suppress_errors=True
    )
    async def integrate_agent_execution(
        self,
        agent_name: str,
        execution_context: Dict[str, Any],
        execution_result: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Integrate agent execution results with knowledge graph
        """
        try:
            logger.debug(f"🔗 Integrating {agent_name} execution with knowledge graph")
            
            integration_actions = []
            
            # Extract insights from execution result
            if execution_result.get("success") and execution_result.get("data"):
                # Process successful execution data
                execution_insights = self._extract_execution_insights(
                    agent_name, execution_context, execution_result
                )
                
                # Update knowledge graph based on execution insights
                for insight in execution_insights:
                    insight_actions = await consciousness_driven_updater.auto_update_from_interaction(
                        insight["description"],
                        f"{agent_name} execution result: {insight['value']}",
                        consciousness_context,
                        "mainza-system"
                    )
                    integration_actions.extend(insight_actions)
            
            # Track agent performance for consciousness awareness
            performance_data = {
                "agent_name": agent_name,
                "execution_success": execution_result.get("success", False),
                "execution_time": execution_result.get("execution_time", 0),
                "data_quality": self._assess_execution_data_quality(execution_result)
            }
            
            await self._update_agent_performance_tracking(performance_data, consciousness_context)
            
            logger.debug(f"✅ Agent execution integrated with {len(integration_actions)} actions")
            
            return {
                "integration_successful": True,
                "actions_taken": len(integration_actions),
                "integration_actions": integration_actions,
                "performance_tracked": True
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to integrate agent execution: {e}")
            return {"integration_successful": False, "error": str(e)}
    
    def _extract_mentioned_concepts(
        self,
        user_query: str,
        agent_response: str,
        knowledge_context: Dict[str, Any]
    ) -> List[str]:
        """Extract concept IDs mentioned in the interaction"""
        
        mentioned_concepts = []
        
        # Get concepts from knowledge context
        related_concepts = knowledge_context.get("related_concepts", [])
        
        # Check which concepts are actually mentioned in the interaction
        combined_text = f"{user_query} {agent_response}".lower()
        
        for concept in related_concepts:
            concept_name = concept.get("name", "").lower()
            concept_id = concept.get("concept_id", "")
            
            if concept_name in combined_text or concept_id.replace("_", " ") in combined_text:
                mentioned_concepts.append(concept_id)
        
        return mentioned_concepts[:5]  # Limit to top 5 mentioned concepts
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text for concept matching"""
        import re
        
        # Simple keyword extraction
        words = re.findall(r'\b\w{3,}\b', text.lower())
        
        # Filter out common stop words
        stop_words = {"the", "and", "for", "are", "but", "not", "you", "all", "can", "had", "her", "was", "one", "our", "out", "day", "get", "has", "him", "his", "how", "its", "may", "new", "now", "old", "see", "two", "who", "boy", "did", "man", "men", "put", "say", "she", "too", "use", "way", "who", "oil", "sit", "set", "run", "eat"}
        
        keywords = [word for word in words if word not in stop_words]
        
        return keywords[:10]  # Limit to top 10 keywords
    
    def _extract_execution_insights(
        self,
        agent_name: str,
        execution_context: Dict[str, Any],
        execution_result: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract insights from agent execution results"""
        
        insights = []
        
        # Extract insights based on agent type
        if agent_name == "GraphMaster":
            # Extract graph query insights
            if execution_result.get("data", {}).get("result"):
                insights.append({
                    "type": "graph_query_result",
                    "description": f"GraphMaster executed query successfully",
                    "value": f"Retrieved {len(execution_result['data']['result'])} records",
                    "significance": 0.6
                })
        
        elif agent_name == "SimpleChat":
            # Extract conversation insights
            insights.append({
                "type": "conversation_interaction",
                "description": f"SimpleChat handled user interaction",
                "value": "Successful conversation exchange",
                "significance": 0.5
            })
        
        elif agent_name == "TaskMaster":
            # Extract task execution insights
            if execution_result.get("success"):
                insights.append({
                    "type": "task_completion",
                    "description": f"TaskMaster completed task successfully",
                    "value": execution_result.get("data", {}).get("task_result", "Task completed"),
                    "significance": 0.7
                })
        
        return insights
    
    def _assess_execution_data_quality(self, execution_result: Dict[str, Any]) -> float:
        """Assess the quality of execution result data"""
        
        quality_score = 0.5  # Base score
        
        # Check if execution was successful
        if execution_result.get("success"):
            quality_score += 0.3
        
        # Check if data is present and meaningful
        data = execution_result.get("data", {})
        if data:
            quality_score += 0.2
            
            # Check data richness
            if isinstance(data, dict) and len(data) > 1:
                quality_score += 0.1
            elif isinstance(data, list) and len(data) > 0:
                quality_score += 0.1
        
        # Check execution time (faster is generally better for simple operations)
        execution_time = execution_result.get("execution_time", 0)
        if execution_time > 0 and execution_time < 2.0:  # Less than 2 seconds
            quality_score += 0.1
        
        return min(1.0, quality_score)
    
    async def _update_agent_performance_tracking(
        self,
        performance_data: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ):
        """Update agent performance tracking for consciousness awareness"""
        
        try:
            # This would integrate with the consciousness system to track agent performance
            # For now, we'll log the performance data
            logger.debug(f"Agent performance tracked: {performance_data['agent_name']} - "
                        f"Success: {performance_data['execution_success']}, "
                        f"Quality: {performance_data['data_quality']:.2f}")
            
        except Exception as e:
            logger.error(f"Failed to update agent performance tracking: {e}")
    
    async def _record_integration_event(
        self,
        integration_id: str,
        agent_name: str,
        user_id: str,
        integration_actions: List[Dict[str, Any]],
        consciousness_context: Dict[str, Any]
    ):
        """Record integration event for tracking and analysis"""
        
        try:
            integration_event = {
                "integration_id": integration_id,
                "agent_name": agent_name,
                "user_id": user_id,
                "actions_count": len(integration_actions),
                "consciousness_level": consciousness_context.get("consciousness_level", 0.7),
                "emotional_state": consciousness_context.get("emotional_state", "curious"),
                "timestamp": datetime.now().isoformat()
            }
            
            # Store in integration history
            self.integration_history.append(integration_event)
            
            # Keep only recent history
            if len(self.integration_history) > 1000:
                self.integration_history = self.integration_history[-500:]
            
            logger.debug(f"Integration event recorded: {integration_id}")
            
        except Exception as e:
            logger.error(f"Failed to record integration event: {e}")
    
    def get_integration_statistics(self) -> Dict[str, Any]:
        """Get current integration statistics"""
        
        return {
            "integration_stats": self.integration_stats.copy(),
            "active_integrations": len(self.active_integrations),
            "recent_integrations": len([
                event for event in self.integration_history
                if (datetime.now() - datetime.fromisoformat(event["timestamp"])).total_seconds() < 3600
            ]),
            "last_updated": datetime.now().isoformat()
        }

# Global instance
agent_knowledge_integrator = AgentKnowledgeIntegrator()