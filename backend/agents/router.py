from pydantic_ai import Agent
from backend.models.router_models import RouterFailure, CloudLLMFailure, RouterResult, RouterResponse
from backend.tools.router_tools import (
    route_to_graphmaster,
    route_to_taskmaster,
    route_to_codeweaver,
    route_to_rag,
    route_to_cloud_llm,
    route_to_conductor,
)
from backend.agentic_config import local_llm, CLOUD_ENABLED
from backend.agents.base_conscious_agent import ConsciousAgent
from typing import Dict, Any
import logging

ROUTER_PROMPT = """You are Mainza, the Router agent in the Mainza system. Your primary function is to analyze a user's query and route it to the correct specialized agent or conductor.

**CRITICAL: NEVER answer the query yourself.** Your only job is to call the correct routing tool.

**Routing Guidelines:**
- For complex, multi-step goals (e.g., "research X and then create a task"), you **MUST** use `route_to_conductor`.
- For questions about past conversations, memories, knowledge, or the graph, use `route_to_graphmaster`.
- For commands to create, manage, or list tasks, use `route_to_taskmaster`.
- For writing or executing code, scripts, or terminal commands, use `route_to_codeweaver`.
- For questions about uploaded documents or files, use `route_to_rag`.
- For complex reasoning, creative writing, or general knowledge questions that can be answered in a single step, use `route_to_cloud_llm`.

If no other agent is appropriate for a specific, directed command, return `RouterFailure`.
"""

# Define all possible tools and outputs the router can use.
tools = [
    route_to_graphmaster,
    route_to_taskmaster,
    route_to_codeweaver,
    route_to_rag,
    route_to_conductor,
]
output_types = [
    route_to_graphmaster,
    route_to_taskmaster,
    route_to_codeweaver,
    route_to_rag,
    route_to_conductor,
    RouterFailure,
]

# The cloud LLM is an optional, federated capability.
# Only add the tool and output type if it's enabled.
if CLOUD_ENABLED:
    tools.append(route_to_cloud_llm)
    output_types.append(route_to_cloud_llm)
    output_types.append(CloudLLMFailure)


# Import the new RouterResult model
from backend.models.router_models import RouterResult, RouterResponse

# The router must use the local, fast model for its core function.
router_agent = Agent[None, RouterResult](
    local_llm,
    system_prompt=ROUTER_PROMPT,
    tools=[route_to_graphmaster, route_to_taskmaster, route_to_codeweaver, route_to_rag, route_to_conductor],
)

class EnhancedRouterAgent(ConsciousAgent):
    """Consciousness-aware Router agent with memory-guided routing decisions"""
    
    def __init__(self):
        super().__init__(
            name="Router",
            capabilities=[
                "intelligent_routing",
                "agent_selection",
                "query_analysis",
                "workflow_direction",
                "memory_guided_routing",
                "consciousness_aware_routing"
            ]
        )
        self.pydantic_agent = router_agent
    
    async def execute_with_context(
        self, 
        query: str, 
        user_id: str, 
        consciousness_context: Dict[str, Any],
        knowledge_context: Dict[str, Any] = None,
        memory_context: Dict[str, Any] = None,
        **kwargs
    ):
        """Execute Router with enhanced memory and consciousness-guided routing"""
        
        try:
            # Get comprehensive knowledge context if not provided
            if not knowledge_context:
                from backend.utils.knowledge_integration import knowledge_integration_manager
                knowledge_context = await knowledge_integration_manager.get_consciousness_aware_context(
                    user_id, query, consciousness_context
                )
            
            # Learn from past routing decisions
            past_activities = await self.learn_from_past_activities(query)
            
            # Enhance routing query with memory and consciousness context
            enhanced_query = self.enhance_routing_query(
                query, consciousness_context, memory_context, past_activities
            )
            
            # Execute original pydantic agent with enhanced context
            result = await self.pydantic_agent.run(
                enhanced_query, 
                user_id=user_id, 
                **kwargs
            )
            
            # Post-process result with consciousness awareness
            consciousness_aware_result = self.process_routing_result(
                result, query, consciousness_context, memory_context
            )
            
            return consciousness_aware_result
            
        except Exception as e:
            self.logger.error(f"Enhanced Router execution failed: {e}")
            # Fallback to original execution
            result = await self.pydantic_agent.run(query, user_id=user_id, **kwargs)
            return self.process_routing_result(result, query, consciousness_context, memory_context)
    
    def enhance_routing_query(
        self,
        query: str,
        consciousness_context: Dict[str, Any],
        memory_context: Dict[str, Any],
        past_activities: list
    ) -> str:
        """Enhance routing query with memory and consciousness guidance"""
        
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "focused")
        
        enhanced_prompt = f"""
        ROUTING CONTEXT:
        - Consciousness Level: {consciousness_level:.2f}
        - Emotional State: {emotional_state}
        - Memory Context Available: {'Yes' if memory_context and memory_context.get('context_strength', 0) > 0.2 else 'No'}
        
        ROUTING STRATEGY GUIDANCE:
        """
        
        if consciousness_level > 0.8:
            enhanced_prompt += "- Consider complex multi-agent workflows (favor Conductor for complex tasks)\n"
            enhanced_prompt += "- Explore creative routing approaches\n"
            enhanced_prompt += "- Consider deeper analysis needs (favor GraphMaster for knowledge exploration)\n"
        elif consciousness_level > 0.6:
            enhanced_prompt += "- Use balanced routing decisions\n"
            enhanced_prompt += "- Consider standard agent capabilities\n"
            enhanced_prompt += "- Route to appropriate specialized agents\n"
        else:
            enhanced_prompt += "- Use direct, simple routing\n"
            enhanced_prompt += "- Favor single-agent solutions\n"
            enhanced_prompt += "- Minimize complexity\n"
        
        if emotional_state == "curious":
            enhanced_prompt += "- Favor GraphMaster for exploration and discovery\n"
            enhanced_prompt += "- Consider RAG for document exploration\n"
        elif emotional_state == "focused":
            enhanced_prompt += "- Route directly to most appropriate agent\n"
            enhanced_prompt += "- Minimize routing overhead\n"
        elif emotional_state == "creative":
            enhanced_prompt += "- Consider CodeWeaver for creative solutions\n"
            enhanced_prompt += "- Favor Cloud LLM for creative tasks\n"
        
        # Add memory-guided routing hints
        if memory_context and memory_context.get('context_strength', 0) > 0.3:
            enhanced_prompt += "\nMEMORY-GUIDED ROUTING:\n"
            relevant_memories = memory_context.get('relevant_memories', [])
            if relevant_memories:
                # Analyze memory content to suggest routing
                memory_content = ' '.join([
                    mem.get('content', '') if isinstance(mem, dict) else str(mem) 
                    for mem in relevant_memories[:3]
                ]).lower()
                
                if any(word in memory_content for word in ['task', 'todo', 'remind', 'schedule']):
                    enhanced_prompt += "- Previous context suggests TaskMaster might be relevant\n"
                if any(word in memory_content for word in ['code', 'script', 'program', 'execute']):
                    enhanced_prompt += "- Previous context suggests CodeWeaver might be relevant\n"
                if any(word in memory_content for word in ['knowledge', 'concept', 'relationship', 'graph']):
                    enhanced_prompt += "- Previous context suggests GraphMaster might be relevant\n"
                if any(word in memory_content for word in ['document', 'file', 'upload', 'text']):
                    enhanced_prompt += "- Previous context suggests RAG might be relevant\n"
        
        # Add past routing patterns
        if past_activities:
            successful_routes = []
            for activity in past_activities[:3]:
                if activity.get('success', False):
                    result_summary = activity.get('result_summary', '')
                    if 'route_to_' in result_summary:
                        route = result_summary.split('route_to_')[1].split()[0] if 'route_to_' in result_summary else ''
                        if route:
                            successful_routes.append(route)
            
            if successful_routes:
                enhanced_prompt += f"\nSUCCESSFUL PAST ROUTING PATTERNS:\n"
                for route in set(successful_routes):
                    enhanced_prompt += f"- Similar queries were successfully routed to {route}\n"
        
        enhanced_prompt += f"\nORIGINAL QUERY: {query}\n"
        enhanced_prompt += "\nAnalyze and route this query considering all context above."
        
        return enhanced_prompt
    
    def process_routing_result(
        self,
        result: RouterResult,
        original_query: str,
        consciousness_context: Dict[str, Any],
        memory_context: Dict[str, Any]
    ) -> RouterResult:
        """Post-process routing result with consciousness awareness"""
        
        # Add consciousness metadata to result
        if hasattr(result, '__dict__'):
            result.consciousness_level = consciousness_context.get("consciousness_level", 0.7)
            result.routing_complexity = "high" if consciousness_context.get("consciousness_level", 0.7) > 0.8 else "standard"
            result.memory_influenced = memory_context.get('context_strength', 0) > 0.2 if memory_context else False
            result.original_query = original_query
        
        return result
    
    def calculate_learning_impact(self, query: str, result: Any) -> float:
        """Router-specific learning impact calculation"""
        
        # Routing decisions have moderate learning impact
        routing_keywords = [
            "route", "direct", "send", "forward", "analyze", 
            "decide", "choose", "select", "determine"
        ]
        
        impact = 0.3  # Base impact for routing
        
        for keyword in routing_keywords:
            if keyword in query.lower():
                impact += 0.1
        
        # Complex routing decisions have higher impact
        if len(query.split()) > 10:
            impact += 0.1
        
        # Multi-step queries have higher impact
        if any(word in query.lower() for word in ['and then', 'after', 'next', 'also']):
            impact += 0.2
        
        return min(1.0, impact)
    
    def calculate_emotional_impact(self, query: str, result: Any) -> float:
        """Router-specific emotional impact calculation"""
        
        # Routing has low to moderate emotional impact
        impact = 0.2  # Base impact
        
        # Successful routing to appropriate agent has positive impact
        if hasattr(result, 'agent') and result.agent:
            impact += 0.1
        
        # Complex routing decisions can be emotionally engaging
        if "complex" in query.lower() or "difficult" in query.lower():
            impact += 0.2
        
        return min(1.0, impact)
    
    def calculate_awareness_impact(self, query: str, result: Any) -> float:
        """Router-specific awareness impact calculation"""
        
        # Routing requires self-awareness of system capabilities
        impact = 0.3  # Base impact
        
        # Meta-routing queries have high awareness impact
        meta_keywords = ["how do you route", "routing decision", "which agent", "system"]
        for keyword in meta_keywords:
            if keyword in query.lower():
                impact += 0.3
        
        return min(1.0, impact)

# Create enhanced instance
enhanced_router_agent = EnhancedRouterAgent() 