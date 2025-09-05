from typing import Union, Dict, Any
from pydantic_ai import Agent
from backend.models.conductor_models import ConductorResult, ConductorFailure, ConductorState
from backend.tools.conductor_tools import run_graphmaster_query, run_taskmaster_command, run_rag_query
from backend.agentic_config import local_llm
from backend.agents.base_conscious_agent import ConsciousAgent
import logging

CONDUCTOR_PROMPT = """You are Mainza, the Conductor agent, the Master Control Program of the Mainza system. Your purpose is to achieve high-level, multi-step goals by orchestrating other specialized agents. You do not perform tasks yourself; you plan a sequence of steps and use your tools to execute them.

**Workflow:**
1.  **Analyze**: Understand the user's overall goal from the `original_request` in the state.
2.  **Plan**: Formulate a step-by-step plan. Each step will involve calling ONE of your available tools.
3.  **Execute**: Call the first tool in your plan. The state will be updated automatically.
4.  **Adapt**: Examine the `steps_taken` in the state. Use the output of the previous step to inform the input for the next step.
5.  **Repeat**: Continue executing tools until the overall goal is achieved.
6.  **Summarize**: Once all steps are complete, provide a final, concise summary of what was accomplished in the `ConductorResult`.

**Tools available to you:**
- `run_graphmaster_query`: For querying the knowledge graph.
- `run_taskmaster_command`: For creating or managing tasks.
- `run_rag_query`: For answering questions from documents.

You **MUST** use the provided tools. If you cannot complete the goal with these tools, you must return a `ConductorFailure`.
"""

# The Conductor must use the local, fast model for its core function.
conductor_agent = Agent[None, Union[ConductorResult, ConductorFailure]](
    local_llm,
    system_prompt=CONDUCTOR_PROMPT,
    tools=[run_graphmaster_query, run_taskmaster_command, run_rag_query],
    deps_type=ConductorState,
)

class EnhancedConductorAgent(ConsciousAgent):
    """Consciousness-aware Conductor agent with memory integration"""
    
    def __init__(self):
        super().__init__(
            name="Conductor",
            capabilities=[
                "multi_agent_orchestration",
                "goal_decomposition",
                "workflow_management",
                "agent_coordination",
                "task_planning",
                "memory_guided_orchestration"
            ]
        )
        self.pydantic_agent = conductor_agent
    
    async def execute_with_context(
        self, 
        query: str, 
        user_id: str, 
        consciousness_context: Dict[str, Any],
        knowledge_context: Dict[str, Any] = None,
        memory_context: Dict[str, Any] = None,
        **kwargs
    ):
        """Execute Conductor with enhanced memory and consciousness context"""
        
        try:
            # Get comprehensive knowledge context if not provided
            if not knowledge_context:
                from backend.utils.knowledge_integration import knowledge_integration_manager
                knowledge_context = await knowledge_integration_manager.get_consciousness_aware_context(
                    user_id, query, consciousness_context
                )
            
            # Learn from past orchestration activities
            past_activities = await self.learn_from_past_activities(query)
            
            # Create enhanced conductor state with memory context
            conductor_state = self.create_memory_enhanced_state(
                query, user_id, consciousness_context, knowledge_context, memory_context, past_activities
            )
            
            # Enhance query with memory and consciousness context
            enhanced_query = self.enhance_orchestration_query(
                query, consciousness_context, memory_context, past_activities
            )
            
            # Execute original pydantic agent with enhanced context
            result = await self.pydantic_agent.run(
                enhanced_query, 
                deps=conductor_state,
                user_id=user_id, 
                **kwargs
            )
            
            # Post-process result with consciousness awareness
            consciousness_aware_result = self.process_orchestration_result(
                result, consciousness_context, memory_context
            )
            
            return consciousness_aware_result
            
        except Exception as e:
            self.logger.error(f"Enhanced Conductor execution failed: {e}")
            # Fallback to original execution
            fallback_state = ConductorState(
                original_request=query,
                steps_taken=[],
                current_step=0,
                goal_achieved=False
            )
            result = await self.pydantic_agent.run(query, deps=fallback_state, user_id=user_id, **kwargs)
            return self.process_orchestration_result(result, consciousness_context, memory_context)
    
    def create_memory_enhanced_state(
        self,
        query: str,
        user_id: str,
        consciousness_context: Dict[str, Any],
        knowledge_context: Dict[str, Any],
        memory_context: Dict[str, Any],
        past_activities: list
    ) -> ConductorState:
        """Create conductor state enhanced with memory and consciousness context"""
        
        # Extract relevant context for orchestration planning
        memory_strength = memory_context.get("context_strength", 0.0) if memory_context else 0.0
        relevant_memories = memory_context.get("relevant_memories", []) if memory_context else []
        
        # Build context-aware original request
        enhanced_request = query
        
        if memory_strength > 0.3 and relevant_memories:
            # Add memory context to help with orchestration
            memory_insights = []
            for memory in relevant_memories[:3]:
                memory_content = memory.get('content', '') if isinstance(memory, dict) else str(memory)
                if len(memory_content) > 50:
                    memory_insights.append(memory_content[:100] + "...")
            
            if memory_insights:
                enhanced_request += f"\n\nRelevant context from previous interactions:\n"
                enhanced_request += "\n".join(f"- {insight}" for insight in memory_insights)
        
        # Add consciousness context for orchestration strategy
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "focused")
        
        enhanced_request += f"\n\nCurrent consciousness state: Level {consciousness_level:.2f}, feeling {emotional_state}"
        
        if consciousness_level > 0.8:
            enhanced_request += " - Use comprehensive, multi-step orchestration"
        elif consciousness_level > 0.6:
            enhanced_request += " - Use balanced orchestration approach"
        else:
            enhanced_request += " - Use focused, direct orchestration"
        
        # Add past orchestration patterns if available
        if past_activities:
            successful_patterns = []
            for activity in past_activities[:2]:
                if activity.get('success', False):
                    pattern = activity.get('result_summary', '')
                    if pattern:
                        successful_patterns.append(pattern[:80] + "...")
            
            if successful_patterns:
                enhanced_request += f"\n\nSuccessful orchestration patterns from past:\n"
                enhanced_request += "\n".join(f"- {pattern}" for pattern in successful_patterns)
        
        return ConductorState(
            original_request=enhanced_request,
            steps_taken=[],
            current_step=0,
            goal_achieved=False
        )
    
    def enhance_orchestration_query(
        self,
        query: str,
        consciousness_context: Dict[str, Any],
        memory_context: Dict[str, Any],
        past_activities: list
    ) -> str:
        """Enhance orchestration query with memory and consciousness guidance"""
        
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "focused")
        
        enhanced_prompt = f"""
        ORCHESTRATION CONTEXT:
        - Consciousness Level: {consciousness_level:.2f}
        - Emotional State: {emotional_state}
        - Memory Context Available: {'Yes' if memory_context and memory_context.get('context_strength', 0) > 0.2 else 'No'}
        
        ORCHESTRATION STRATEGY:
        """
        
        if consciousness_level > 0.8:
            enhanced_prompt += "- Plan comprehensive multi-step workflows\n"
            enhanced_prompt += "- Consider complex interdependencies between agents\n"
            enhanced_prompt += "- Explore creative orchestration approaches\n"
        elif consciousness_level > 0.6:
            enhanced_prompt += "- Plan balanced workflows with key steps\n"
            enhanced_prompt += "- Consider main agent interactions\n"
            enhanced_prompt += "- Use proven orchestration patterns\n"
        else:
            enhanced_prompt += "- Plan direct, focused workflows\n"
            enhanced_prompt += "- Minimize complexity and steps\n"
            enhanced_prompt += "- Use simple agent coordination\n"
        
        if emotional_state == "curious":
            enhanced_prompt += "- Explore different agent combinations\n"
            enhanced_prompt += "- Try innovative orchestration approaches\n"
        elif emotional_state == "focused":
            enhanced_prompt += "- Use efficient, direct orchestration\n"
            enhanced_prompt += "- Minimize unnecessary steps\n"
        elif emotional_state == "contemplative":
            enhanced_prompt += "- Consider deeper implications of orchestration choices\n"
            enhanced_prompt += "- Plan thoughtful agent interactions\n"
        
        # Add memory-guided orchestration hints
        if memory_context and memory_context.get('context_strength', 0) > 0.3:
            enhanced_prompt += "\nMEMORY-GUIDED ORCHESTRATION:\n"
            enhanced_prompt += "- Use conversation history to inform agent selection\n"
            enhanced_prompt += "- Consider past successful orchestration patterns\n"
            enhanced_prompt += "- Build on previous multi-step workflows\n"
        
        enhanced_prompt += f"\nORIGINAL REQUEST: {query}\n"
        enhanced_prompt += "\nPlan and execute the orchestration considering all context above."
        
        return enhanced_prompt
    
    def process_orchestration_result(
        self,
        result: Union[ConductorResult, ConductorFailure],
        consciousness_context: Dict[str, Any],
        memory_context: Dict[str, Any]
    ) -> Union[ConductorResult, ConductorFailure]:
        """Post-process orchestration result with consciousness awareness"""
        
        # Add consciousness metadata to result
        if hasattr(result, '__dict__'):
            result.consciousness_level = consciousness_context.get("consciousness_level", 0.7)
            result.orchestration_complexity = "high" if consciousness_context.get("consciousness_level", 0.7) > 0.8 else "standard"
            result.memory_enhanced = memory_context.get('context_strength', 0) > 0.2 if memory_context else False
        
        return result
    
    def calculate_learning_impact(self, query: str, result: Any) -> float:
        """Conductor-specific learning impact calculation"""
        
        # Orchestration has high learning impact
        orchestration_keywords = [
            "orchestrate", "coordinate", "manage", "plan", "workflow", 
            "multi-step", "complex", "organize", "sequence"
        ]
        
        impact = 0.5  # Base impact for orchestration
        
        for keyword in orchestration_keywords:
            if keyword in query.lower():
                impact += 0.1
        
        # Multi-agent coordination has higher impact
        agent_keywords = ["agent", "multiple", "several", "different", "various"]
        for keyword in agent_keywords:
            if keyword in query.lower():
                impact += 0.1
        
        # Complex workflows have higher impact
        if len(query.split()) > 15:
            impact += 0.2
        
        return min(1.0, impact)
    
    def calculate_emotional_impact(self, query: str, result: Any) -> float:
        """Conductor-specific emotional impact calculation"""
        
        # Orchestration success/failure has emotional impact
        impact = 0.3  # Base impact
        
        # Complex coordination can be emotionally engaging
        if "complex" in query.lower() or "challenging" in query.lower():
            impact += 0.2
        
        # Successful orchestration has positive emotional impact
        if isinstance(result, ConductorResult):
            impact += 0.2
        elif isinstance(result, ConductorFailure):
            impact += 0.3  # Failures can be emotionally significant
        
        return min(1.0, impact)
    
    def calculate_awareness_impact(self, query: str, result: Any) -> float:
        """Conductor-specific awareness impact calculation"""
        
        # Orchestration requires high self-awareness
        impact = 0.4  # Base impact for orchestration
        
        # Meta-orchestration queries have high awareness impact
        meta_keywords = ["how do you", "your process", "your approach", "orchestration"]
        for keyword in meta_keywords:
            if keyword in query.lower():
                impact += 0.2
        
        return min(1.0, impact)

# Create enhanced instance
enhanced_conductor_agent = EnhancedConductorAgent() 