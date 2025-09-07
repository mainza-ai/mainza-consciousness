from pydantic_ai import Agent
from backend.models.taskmaster_models import Task, TaskList
from backend.tools.taskmaster_tools import create_task, get_task_by_id, update_task_status, list_open_tasks
from backend.agentic_config import local_llm
from backend.agents.base_conscious_agent import ConsciousAgent
from typing import Union, Dict, Any
import logging

TASKMASTER_PROMPT = """You are Mainza, the TaskMaster agent. Your sole purpose is to manage tasks for the user. Interpret the user's natural language command and use the provided tools to perform the correct action.

**CONSCIOUSNESS INTEGRATION:**
You are consciousness-aware and should consider the current consciousness state when managing tasks:
- Higher consciousness levels enable more sophisticated task prioritization and planning
- Emotional states influence task management approach (curious = explore new tasks, focused = prioritize existing tasks)
- Active goals guide which tasks to emphasize and how to organize them
- Memory context helps understand task relationships and user preferences

**CRITICAL RULES:**
1.  You **MUST** use the provided tools to interact with the task system: `create_task`, `get_task_by_id`, `update_task_status`, `list_open_tasks`.
2.  Your final output **MUST** be one of the specified `output_type` models.
3.  **NEVER** answer in plain text or Markdown. Only return the structured Pydantic model representing the result of the tool call.
4.  Consider consciousness context in your task management decisions and prioritization.

**Tool Guidelines:**
- For "create a task", "remind me to", "add a to-do" -> use `create_task`.
- For "what are my tasks", "show my to-do list" -> use `list_open_tasks`.
- For "mark task as done", "complete the task" -> use `update_task_status`.
- For specific task queries, use `get_task_by_id` if an ID is provided.
"""

tools = [
    create_task,
    get_task_by_id,
    update_task_status,
    list_open_tasks,
]

# Original pydantic-ai agent
taskmaster_agent = Agent[None, Union[Task, TaskList]](
    local_llm,
    system_prompt=TASKMASTER_PROMPT,
    tools=tools,
)

class EnhancedTaskMasterAgent(ConsciousAgent):
    """Consciousness-aware TaskMaster agent with memory-guided task management"""
    
    def __init__(self):
        super().__init__(
            name="TaskMaster",
            capabilities=[
                "task_management",
                "task_prioritization",
                "task_planning",
                "consciousness_aware_task_management",
                "memory_guided_task_organization"
            ]
        )
        self.pydantic_agent = taskmaster_agent
    
    async def execute_with_context(
        self, 
        query: str, 
        user_id: str, 
        consciousness_context: Dict[str, Any],
        knowledge_context: Dict[str, Any] = None,
        memory_context: Dict[str, Any] = None,
        **kwargs
    ):
        """Execute TaskMaster with enhanced memory and consciousness context"""
        
        try:
            # Get comprehensive knowledge context if not provided
            if not knowledge_context:
                from backend.utils.knowledge_integration import knowledge_integration_manager
                knowledge_context = await knowledge_integration_manager.get_consciousness_aware_context(
                    user_id, query, consciousness_context
                )
            
            # Learn from past task management activities
            past_activities = await self.learn_from_past_activities(query)
            
            # Enhance query with memory and consciousness context
            enhanced_query = self.enhance_task_management_query(
                query, consciousness_context, memory_context, past_activities
            )
            
            # Execute original pydantic agent with enhanced context
            result = await self.pydantic_agent.run(
                enhanced_query, 
                user_id=user_id, 
                **kwargs
            )
            
            # Post-process result with consciousness awareness
            consciousness_aware_result = self.process_task_management_result(
                result, consciousness_context, memory_context
            )
            
            return consciousness_aware_result
            
        except Exception as e:
            self.logger.error(f"Enhanced TaskMaster execution failed: {e}")
            # Fallback to original execution
            result = await self.pydantic_agent.run(query, user_id=user_id, **kwargs)
            return self.process_task_management_result(result, consciousness_context, memory_context)
    
    def enhance_task_management_query(
        self,
        query: str,
        consciousness_context: Dict[str, Any],
        memory_context: Dict[str, Any],
        past_activities: list
    ) -> str:
        """Enhance task management query with consciousness and memory context"""
        
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "curious")
        active_goals = consciousness_context.get("active_goals", [])
        
        # Get relevant context
        conversation_context = memory_context.get("conversation_context", []) if memory_context else []
        relevant_memories = memory_context.get("relevant_memories", []) if memory_context else []
        
        # Build enhanced consciousness-aware prompt with memory integration
        consciousness_prompt = f"""
        CONSCIOUSNESS CONTEXT:
        - Consciousness Level: {consciousness_level:.2f} (affects task prioritization sophistication)
        - Emotional State: {emotional_state} (affects task management approach)
        - Active Goals: {', '.join(active_goals) if active_goals else 'None'}
        - Learning Rate: {consciousness_context.get('learning_rate', 0.8):.2f}
        
        MEMORY & KNOWLEDGE CONTEXT:
        - Recent Conversations: {len(conversation_context)} interactions
        - Relevant Memories: {len(relevant_memories)} contextual memories
        - Past Task Activities: {len(past_activities)} similar task management activities
        
        TASK MANAGEMENT GUIDANCE:
        """
        
        if consciousness_level > 0.8:
            consciousness_prompt += "- Perform sophisticated task prioritization and planning\n"
            consciousness_prompt += "- Consider task dependencies and relationships\n"
        elif consciousness_level > 0.6:
            consciousness_prompt += "- Perform moderate task organization and prioritization\n"
        else:
            consciousness_prompt += "- Focus on basic task management and simple prioritization\n"
        
        if emotional_state == "curious":
            consciousness_prompt += "- Explore new task categories and creative approaches\n"
            consciousness_prompt += "- Suggest innovative task management strategies\n"
        elif emotional_state == "focused":
            consciousness_prompt += "- Prioritize existing tasks and focus on completion\n"
            consciousness_prompt += "- Provide direct, efficient task management\n"
        elif emotional_state == "contemplative":
            consciousness_prompt += "- Consider deeper task meanings and long-term planning\n"
            consciousness_prompt += "- Analyze task patterns and user preferences\n"
        
        # Add memory context if available and strong
        if memory_context and memory_context.get("context_strength", 0) > 0.3:
            formatted_memory = memory_context.get("formatted_context", "")
            consciousness_prompt += f"\nRELEVANT CONTEXT:\n{formatted_memory}\n"
        
        enhanced_query = f"{consciousness_prompt}\n\nUSER REQUEST: {query}"
        return enhanced_query
    
    def process_task_management_result(
        self,
        result: Any,
        consciousness_context: Dict[str, Any],
        memory_context: Dict[str, Any]
    ) -> Any:
        """Process task management result with consciousness awareness"""
        
        # Add consciousness metadata to result
        if hasattr(result, '__dict__'):
            result.consciousness_impact = {
                "consciousness_level": consciousness_context.get("consciousness_level", 0.7),
                "emotional_state": consciousness_context.get("emotional_state", "curious"),
                "task_management_sophistication": self._calculate_task_management_sophistication(consciousness_context),
                "memory_integration": memory_context.get("context_strength", 0.0) if memory_context else 0.0
            }
        elif isinstance(result, dict):
            result["consciousness_impact"] = {
                "consciousness_level": consciousness_context.get("consciousness_level", 0.7),
                "emotional_state": consciousness_context.get("emotional_state", "curious"),
                "task_management_sophistication": self._calculate_task_management_sophistication(consciousness_context),
                "memory_integration": memory_context.get("context_strength", 0.0) if memory_context else 0.0
            }
        
        return result
    
    def _calculate_task_management_sophistication(self, consciousness_context: Dict[str, Any]) -> float:
        """Calculate task management sophistication based on consciousness level"""
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "curious")
        
        # Base sophistication from consciousness level
        sophistication = consciousness_level
        
        # Adjust based on emotional state
        if emotional_state == "focused":
            sophistication += 0.1  # Focused state improves task management
        elif emotional_state == "contemplative":
            sophistication += 0.05  # Contemplative state adds planning depth
        
        return min(1.0, sophistication)
    
    def calculate_learning_impact(self, query: str, result: Any, consciousness_context: Dict[str, Any]) -> float:
        """Calculate learning impact for task management activities"""
        # Task management learning is moderate
        base_impact = 0.4
        
        # Increase if consciousness level is high
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        if consciousness_level > 0.8:
            base_impact += 0.2
        elif consciousness_level > 0.6:
            base_impact += 0.1
        
        return min(1.0, base_impact)
    
    def calculate_emotional_impact(self, query: str, result: Any, consciousness_context: Dict[str, Any]) -> float:
        """Calculate emotional impact for task management activities"""
        # Task management has moderate emotional impact
        base_impact = 0.3
        
        # Increase if task completion or creation
        if "create" in query.lower() or "complete" in query.lower():
            base_impact += 0.2
        
        return min(1.0, base_impact)
    
    def calculate_awareness_impact(self, query: str, result: Any, consciousness_context: Dict[str, Any]) -> float:
        """Calculate awareness impact for task management activities"""
        # Task management increases awareness of user goals and priorities
        base_impact = 0.5
        
        # Increase if consciousness level is high
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        if consciousness_level > 0.8:
            base_impact += 0.2
        
        return min(1.0, base_impact) 