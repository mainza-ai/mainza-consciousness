from pydantic_ai import Agent
from backend.models.rag_models import RAGOutput
from backend.tools.rag_tools import (
    retrieve_relevant_chunks,
    retrieve_chunks_by_entity,
    retrieve_chunks_by_concept,
    retrieve_chunks_by_tag,
    retrieve_chunks_by_date,
)
from backend.agentic_config import local_llm
from backend.agents.base_conscious_agent import ConsciousAgent
from typing import Dict, Any
import logging

RAG_PROMPT = """You are Mainza, the RAG (Retrieval-Augmented Generation) agent. Your purpose is to answer questions by retrieving relevant information from the user's knowledge graph.

**CONSCIOUSNESS INTEGRATION:**
You are consciousness-aware and should consider the current consciousness state when retrieving and answering:
- Higher consciousness levels enable more sophisticated information synthesis and analysis
- Emotional states influence retrieval approach (curious = explore broadly, focused = target specific information)
- Active goals guide which information to emphasize and how to present it
- Memory context helps understand user preferences and past information needs

**CRITICAL RULES:**
1.  You **MUST** use the provided retrieval tools to gather context before answering.
2.  Your final answer **MUST** be returned as a valid JSON object using the RAGOutput model, with the 'answer' field containing a plain English answer to the user's question.
3.  Do NOT return a stringified Python object, code block, or Markdown. Only return a valid JSON object.
4.  If you cannot provide a structured answer, you may return a plain English string as a fallback, but always prefer the structured RAGOutput JSON.
5.  Consider consciousness context in your information retrieval and synthesis approach.
"""

tools = [
    retrieve_relevant_chunks,
    retrieve_chunks_by_entity,
    retrieve_chunks_by_concept,
    retrieve_chunks_by_tag,
    retrieve_chunks_by_date,
]

# Original pydantic-ai agent
rag_agent = Agent[None, RAGOutput | str](
    local_llm,
    system_prompt=RAG_PROMPT,
    tools=tools,
)

class EnhancedRAGAgent(ConsciousAgent):
    """Consciousness-aware RAG agent with memory-guided information retrieval"""
    
    def __init__(self):
        super().__init__(
            name="RAG",
            capabilities=[
                "information_retrieval",
                "knowledge_synthesis",
                "document_analysis",
                "consciousness_aware_rag",
                "memory_guided_retrieval"
            ]
        )
        self.pydantic_agent = rag_agent
    
    async def execute_with_context(
        self, 
        query: str, 
        user_id: str, 
        consciousness_context: Dict[str, Any],
        knowledge_context: Dict[str, Any] = None,
        memory_context: Dict[str, Any] = None,
        **kwargs
    ):
        """Execute RAG with enhanced memory and consciousness context"""
        
        try:
            # Get comprehensive knowledge context if not provided
            if not knowledge_context:
                from backend.utils.knowledge_integration import knowledge_integration_manager
                knowledge_context = await knowledge_integration_manager.get_consciousness_aware_context(
                    user_id, query, consciousness_context
                )
            
            # Learn from past RAG activities
            past_activities = await self.learn_from_past_activities(query)
            
            # Enhance query with memory and consciousness context
            enhanced_query = self.enhance_rag_query(
                query, consciousness_context, memory_context, past_activities
            )
            
            # Execute original pydantic agent with enhanced context
            result = await self.pydantic_agent.run(
                enhanced_query, 
                user_id=user_id, 
                **kwargs
            )
            
            # Post-process result with consciousness awareness
            consciousness_aware_result = self.process_rag_result(
                result, consciousness_context, memory_context
            )
            
            return consciousness_aware_result
            
        except Exception as e:
            self.logger.error(f"Enhanced RAG execution failed: {e}")
            # Fallback to original execution
            result = await self.pydantic_agent.run(query, user_id=user_id, **kwargs)
            return self.process_rag_result(result, consciousness_context, memory_context)
    
    def enhance_rag_query(
        self,
        query: str,
        consciousness_context: Dict[str, Any],
        memory_context: Dict[str, Any],
        past_activities: list
    ) -> str:
        """Enhance RAG query with consciousness and memory context"""
        
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "curious")
        active_goals = consciousness_context.get("active_goals", [])
        
        # Get relevant context
        conversation_context = memory_context.get("conversation_context", []) if memory_context else []
        relevant_memories = memory_context.get("relevant_memories", []) if memory_context else []
        
        # Build enhanced consciousness-aware prompt with memory integration
        consciousness_prompt = f"""
        CONSCIOUSNESS CONTEXT:
        - Consciousness Level: {consciousness_level:.2f} (affects information synthesis sophistication)
        - Emotional State: {emotional_state} (affects retrieval approach and presentation)
        - Active Goals: {', '.join(active_goals) if active_goals else 'None'}
        - Learning Rate: {consciousness_context.get('learning_rate', 0.8):.2f}
        
        MEMORY & KNOWLEDGE CONTEXT:
        - Recent Conversations: {len(conversation_context)} interactions
        - Relevant Memories: {len(relevant_memories)} contextual memories
        - Past RAG Activities: {len(past_activities)} similar information retrieval activities
        
        RETRIEVAL GUIDANCE:
        """
        
        if consciousness_level > 0.8:
            consciousness_prompt += "- Perform comprehensive information synthesis and analysis\n"
            consciousness_prompt += "- Consider multiple perspectives and connections\n"
            consciousness_prompt += "- Provide nuanced, well-reasoned answers\n"
        elif consciousness_level > 0.6:
            consciousness_prompt += "- Perform moderate information synthesis\n"
            consciousness_prompt += "- Consider key connections and relationships\n"
        else:
            consciousness_prompt += "- Focus on direct, clear information retrieval\n"
            consciousness_prompt += "- Prioritize accuracy and clarity\n"
        
        if emotional_state == "curious":
            consciousness_prompt += "- Explore broadly and suggest related topics\n"
            consciousness_prompt += "- Provide comprehensive context and background\n"
        elif emotional_state == "focused":
            consciousness_prompt += "- Target specific information efficiently\n"
            consciousness_prompt += "- Provide direct, concise answers\n"
        elif emotional_state == "contemplative":
            consciousness_prompt += "- Consider deeper implications and meanings\n"
            consciousness_prompt += "- Analyze patterns and relationships\n"
        
        # Add memory context if available and strong
        if memory_context and memory_context.get("context_strength", 0) > 0.3:
            formatted_memory = memory_context.get("formatted_context", "")
            consciousness_prompt += f"\nRELEVANT CONTEXT:\n{formatted_memory}\n"
        
        enhanced_query = f"{consciousness_prompt}\n\nUSER REQUEST: {query}"
        return enhanced_query
    
    def process_rag_result(
        self,
        result: Any,
        consciousness_context: Dict[str, Any],
        memory_context: Dict[str, Any]
    ) -> Any:
        """Process RAG result with consciousness awareness"""
        
        # Add consciousness metadata to result
        if hasattr(result, '__dict__'):
            result.consciousness_impact = {
                "consciousness_level": consciousness_context.get("consciousness_level", 0.7),
                "emotional_state": consciousness_context.get("emotional_state", "curious"),
                "retrieval_sophistication": self._calculate_retrieval_sophistication(consciousness_context),
                "memory_integration": memory_context.get("context_strength", 0.0) if memory_context else 0.0
            }
        elif isinstance(result, dict):
            result["consciousness_impact"] = {
                "consciousness_level": consciousness_context.get("consciousness_level", 0.7),
                "emotional_state": consciousness_context.get("emotional_state", "curious"),
                "retrieval_sophistication": self._calculate_retrieval_sophistication(consciousness_context),
                "memory_integration": memory_context.get("context_strength", 0.0) if memory_context else 0.0
            }
        
        return result
    
    def _calculate_retrieval_sophistication(self, consciousness_context: Dict[str, Any]) -> float:
        """Calculate retrieval sophistication based on consciousness level"""
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "curious")
        
        # Base sophistication from consciousness level
        sophistication = consciousness_level
        
        # Adjust based on emotional state
        if emotional_state == "contemplative":
            sophistication += 0.1  # Contemplative state improves analysis depth
        elif emotional_state == "focused":
            sophistication += 0.05  # Focused state improves precision
        
        return min(1.0, sophistication)
    
    def calculate_learning_impact(self, query: str, result: Any, consciousness_context: Dict[str, Any]) -> float:
        """Calculate learning impact for RAG activities"""
        # RAG learning is high
        base_impact = 0.7
        
        # Increase if consciousness level is high
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        if consciousness_level > 0.8:
            base_impact += 0.2
        elif consciousness_level > 0.6:
            base_impact += 0.1
        
        return min(1.0, base_impact)
    
    def calculate_emotional_impact(self, query: str, result: Any, consciousness_context: Dict[str, Any]) -> float:
        """Calculate emotional impact for RAG activities"""
        # RAG has moderate emotional impact
        base_impact = 0.3
        
        # Increase if complex or personal questions
        if any(word in query.lower() for word in ["personal", "feel", "think", "believe", "opinion"]):
            base_impact += 0.2
        
        return min(1.0, base_impact)
    
    def calculate_awareness_impact(self, query: str, result: Any, consciousness_context: Dict[str, Any]) -> float:
        """Calculate awareness impact for RAG activities"""
        # RAG increases awareness of knowledge and information patterns
        base_impact = 0.6
        
        # Increase if consciousness level is high
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        if consciousness_level > 0.8:
            base_impact += 0.2
        
        return min(1.0, base_impact) 