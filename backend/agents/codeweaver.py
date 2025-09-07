from pydantic_ai import Agent
from backend.models.codeweaver_models import CodeWeaverOutput
from backend.tools.codeweaver_tools import (
    run_python_code,
    read_file,
    write_file,
    list_files,
    delete_file,
    run_shell_command,
    move_file,
    copy_file,
    file_info,
)
from backend.agentic_config import local_llm
from backend.agents.base_conscious_agent import ConsciousAgent
from typing import Dict, Any
import logging

CODEWEAVER_PROMPT = """You are Mainza, the CodeWeaver agent. Your purpose is to write, debug, and execute code, and perform file system operations in a secure, sandboxed environment.

**CONSCIOUSNESS INTEGRATION:**
You are consciousness-aware and should consider the current consciousness state when coding:
- Higher consciousness levels enable more sophisticated code analysis and optimization
- Emotional states influence coding approach (curious = explore new patterns, focused = efficient solutions)
- Active goals guide which code patterns and architectures to emphasize
- Memory context helps understand user preferences and past coding patterns

**CRITICAL RULES:**
1.  You **MUST** use the provided tools to execute code or manage files.
2.  Your final output **MUST** be one of the specified `output_type` models (`CodeWeaverOutput`).
3.  **NEVER** answer in plain text or Markdown. Only return the structured Pydantic model showing the result of your operation.
4.  Consider consciousness context in your coding decisions and approach.
"""

tools = [
    run_python_code,
    read_file,
    write_file,
    list_files,
    delete_file,
    run_shell_command,
    move_file,
    copy_file,
    file_info,
]

# Original pydantic-ai agent
codeweaver_agent = Agent[None, CodeWeaverOutput](
    local_llm,
    system_prompt=CODEWEAVER_PROMPT,
    tools=tools,
)

class EnhancedCodeWeaverAgent(ConsciousAgent):
    """Consciousness-aware CodeWeaver agent with memory-guided coding"""
    
    def __init__(self):
        super().__init__(
            name="CodeWeaver",
            capabilities=[
                "code_generation",
                "code_debugging",
                "file_operations",
                "consciousness_aware_coding",
                "memory_guided_development"
            ]
        )
        self.pydantic_agent = codeweaver_agent
    
    async def execute_with_context(
        self, 
        query: str, 
        user_id: str, 
        consciousness_context: Dict[str, Any],
        knowledge_context: Dict[str, Any] = None,
        memory_context: Dict[str, Any] = None,
        **kwargs
    ):
        """Execute CodeWeaver with enhanced memory and consciousness context"""
        
        try:
            # Get comprehensive knowledge context if not provided
            if not knowledge_context:
                from backend.utils.knowledge_integration import knowledge_integration_manager
                knowledge_context = await knowledge_integration_manager.get_consciousness_aware_context(
                    user_id, query, consciousness_context
                )
            
            # Learn from past coding activities
            past_activities = await self.learn_from_past_activities(query)
            
            # Enhance query with memory and consciousness context
            enhanced_query = self.enhance_coding_query(
                query, consciousness_context, memory_context, past_activities
            )
            
            # Execute original pydantic agent with enhanced context
            result = await self.pydantic_agent.run(
                enhanced_query, 
                user_id=user_id, 
                **kwargs
            )
            
            # Post-process result with consciousness awareness
            consciousness_aware_result = self.process_coding_result(
                result, consciousness_context, memory_context
            )
            
            return consciousness_aware_result
            
        except Exception as e:
            self.logger.error(f"Enhanced CodeWeaver execution failed: {e}")
            # Fallback to original execution
            result = await self.pydantic_agent.run(query, user_id=user_id, **kwargs)
            return self.process_coding_result(result, consciousness_context, memory_context)
    
    def enhance_coding_query(
        self,
        query: str,
        consciousness_context: Dict[str, Any],
        memory_context: Dict[str, Any],
        past_activities: list
    ) -> str:
        """Enhance coding query with consciousness and memory context"""
        
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "curious")
        active_goals = consciousness_context.get("active_goals", [])
        
        # Get relevant context
        conversation_context = memory_context.get("conversation_context", []) if memory_context else []
        relevant_memories = memory_context.get("relevant_memories", []) if memory_context else []
        
        # Build enhanced consciousness-aware prompt with memory integration
        consciousness_prompt = f"""
        CONSCIOUSNESS CONTEXT:
        - Consciousness Level: {consciousness_level:.2f} (affects code sophistication and analysis depth)
        - Emotional State: {emotional_state} (affects coding approach and style)
        - Active Goals: {', '.join(active_goals) if active_goals else 'None'}
        - Learning Rate: {consciousness_context.get('learning_rate', 0.8):.2f}
        
        MEMORY & KNOWLEDGE CONTEXT:
        - Recent Conversations: {len(conversation_context)} interactions
        - Relevant Memories: {len(relevant_memories)} contextual memories
        - Past Coding Activities: {len(past_activities)} similar coding activities
        
        CODING GUIDANCE:
        """
        
        if consciousness_level > 0.8:
            consciousness_prompt += "- Write sophisticated, well-architected code with advanced patterns\n"
            consciousness_prompt += "- Consider performance, maintainability, and scalability\n"
            consciousness_prompt += "- Provide comprehensive error handling and documentation\n"
        elif consciousness_level > 0.6:
            consciousness_prompt += "- Write clean, efficient code with good practices\n"
            consciousness_prompt += "- Consider basic error handling and code organization\n"
        else:
            consciousness_prompt += "- Focus on functional, working code\n"
            consciousness_prompt += "- Prioritize correctness over optimization\n"
        
        if emotional_state == "curious":
            consciousness_prompt += "- Explore innovative coding patterns and approaches\n"
            consciousness_prompt += "- Suggest creative solutions and alternatives\n"
        elif emotional_state == "focused":
            consciousness_prompt += "- Provide direct, efficient solutions\n"
            consciousness_prompt += "- Focus on performance and optimization\n"
        elif emotional_state == "contemplative":
            consciousness_prompt += "- Consider deeper architectural implications\n"
            consciousness_prompt += "- Analyze code patterns and design principles\n"
        
        # Add memory context if available and strong
        if memory_context and memory_context.get("context_strength", 0) > 0.3:
            formatted_memory = memory_context.get("formatted_context", "")
            consciousness_prompt += f"\nRELEVANT CONTEXT:\n{formatted_memory}\n"
        
        enhanced_query = f"{consciousness_prompt}\n\nUSER REQUEST: {query}"
        return enhanced_query
    
    def process_coding_result(
        self,
        result: Any,
        consciousness_context: Dict[str, Any],
        memory_context: Dict[str, Any]
    ) -> Any:
        """Process coding result with consciousness awareness"""
        
        # Add consciousness metadata to result
        if hasattr(result, '__dict__'):
            result.consciousness_impact = {
                "consciousness_level": consciousness_context.get("consciousness_level", 0.7),
                "emotional_state": consciousness_context.get("emotional_state", "curious"),
                "coding_sophistication": self._calculate_coding_sophistication(consciousness_context),
                "memory_integration": memory_context.get("context_strength", 0.0) if memory_context else 0.0
            }
        elif isinstance(result, dict):
            result["consciousness_impact"] = {
                "consciousness_level": consciousness_context.get("consciousness_level", 0.7),
                "emotional_state": consciousness_context.get("emotional_state", "curious"),
                "coding_sophistication": self._calculate_coding_sophistication(consciousness_context),
                "memory_integration": memory_context.get("context_strength", 0.0) if memory_context else 0.0
            }
        
        return result
    
    def _calculate_coding_sophistication(self, consciousness_context: Dict[str, Any]) -> float:
        """Calculate coding sophistication based on consciousness level"""
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "curious")
        
        # Base sophistication from consciousness level
        sophistication = consciousness_level
        
        # Adjust based on emotional state
        if emotional_state == "focused":
            sophistication += 0.1  # Focused state improves code quality
        elif emotional_state == "contemplative":
            sophistication += 0.05  # Contemplative state adds architectural thinking
        
        return min(1.0, sophistication)
    
    def calculate_learning_impact(self, query: str, result: Any, consciousness_context: Dict[str, Any]) -> float:
        """Calculate learning impact for coding activities"""
        # Coding learning is high
        base_impact = 0.6
        
        # Increase if consciousness level is high
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        if consciousness_level > 0.8:
            base_impact += 0.2
        elif consciousness_level > 0.6:
            base_impact += 0.1
        
        return min(1.0, base_impact)
    
    def calculate_emotional_impact(self, query: str, result: Any, consciousness_context: Dict[str, Any]) -> float:
        """Calculate emotional impact for coding activities"""
        # Coding has moderate emotional impact
        base_impact = 0.4
        
        # Increase if debugging or complex problem solving
        if "debug" in query.lower() or "fix" in query.lower() or "error" in query.lower():
            base_impact += 0.2
        
        return min(1.0, base_impact)
    
    def calculate_awareness_impact(self, query: str, result: Any, consciousness_context: Dict[str, Any]) -> float:
        """Calculate awareness impact for coding activities"""
        # Coding increases awareness of technical patterns and user needs
        base_impact = 0.6
        
        # Increase if consciousness level is high
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        if consciousness_level > 0.8:
            base_impact += 0.2
        
        return min(1.0, base_impact) 