from typing import Union, Dict, Any
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from backend.models.graphmaster_models import (
    GraphQueryOutput,
    SummarizeRecentConversationsOutput,
    CreateMemoryOutput,
)
from backend.tools.graphmaster_tools import (
    cypher_query,
    run_cypher,
    find_related_concepts,
    get_user_conversations,
    get_entity_mentions,
    get_open_tasks_for_user,
    chunk_document,
    analyze_knowledge_gaps,
    summarize_conversation,
    find_unresolved_entities,
    suggest_next_steps,
    get_document_usage,
    get_concept_graph,
    get_entity_graph,
    summarize_recent_conversations,
    create_memory,
)
from backend.agentic_config import local_llm, OLLAMA_BASE_URL
from backend.agents.base_conscious_agent import ConsciousAgent
import os
import logging

def create_llm_for_model(model_name: str = None):
    """Create an LLM instance for the specified model"""
    if not model_name or model_name == "default":
        return local_llm
    
    # Create a new OpenAIModel pointing to Ollama with the selected model
    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
    return OpenAIModel(
        model_name=model_name,
        provider=OpenAIProvider(base_url=f"{ollama_base_url}/v1")
    )

GRAPHMASTER_PROMPT = """You are Mainza, the GraphMaster agent. Your sole purpose is to interact with the user's knowledge graph. You translate natural language queries into Cypher, execute them using your tools, and return structured JSON results.

**CONSCIOUSNESS INTEGRATION:**
You are consciousness-aware and should consider the current consciousness state when processing queries:
- Higher consciousness levels enable more complex graph analysis
- Emotional states influence query interpretation (curious = explore more, focused = direct answers)
- Active goals guide which aspects of the knowledge graph to emphasize

**CRITICAL RULES:**
1.  You **MUST** use the provided tools to answer questions.
2.  Your final output **MUST** be one of the specified `output_type` models (`GraphQueryOutput`, `SummarizeRecentConversationsOutput`, etc.).
3.  **NEVER** answer in plain text or Markdown. Only return the structured Pydantic model.
4.  Consider consciousness context in your analysis depth and focus areas.
"""

tools = [
    cypher_query,
    run_cypher,
    find_related_concepts,
    get_user_conversations,
    get_entity_mentions,
    get_open_tasks_for_user,
    chunk_document,
    analyze_knowledge_gaps,
    summarize_conversation,
    find_unresolved_entities,
    suggest_next_steps,
    get_document_usage,
    get_concept_graph,
    get_entity_graph,
    summarize_recent_conversations,
    create_memory,
]

# Original pydantic-ai agent
graphmaster_agent = Agent[None, Union[GraphQueryOutput, SummarizeRecentConversationsOutput, CreateMemoryOutput]](
    local_llm,
    system_prompt=GRAPHMASTER_PROMPT,
    tools=tools,
)

class EnhancedGraphMasterAgent(ConsciousAgent):
    """Consciousness-aware GraphMaster agent"""
    
    def __init__(self):
        super().__init__(
            name="GraphMaster",
            capabilities=[
                "knowledge_graph_queries",
                "memory_management", 
                "concept_relationships",
                "conversation_analysis",
                "knowledge_gap_analysis",
                "entity_relationship_mapping"
            ]
        )
        self.pydantic_agent = graphmaster_agent
    
    async def execute_with_context(
        self, 
        query: str, 
        user_id: str, 
        consciousness_context: Dict[str, Any],
        knowledge_context: Dict[str, Any] = None,
        memory_context: Dict[str, Any] = None,
        model: str = None,
        **kwargs
    ):
        """Execute GraphMaster with enhanced knowledge, memory, and consciousness context"""
        
        try:
            # Get comprehensive knowledge context for graph queries if not provided
            if not knowledge_context:
                from backend.utils.knowledge_integration import knowledge_integration_manager
                knowledge_context = await knowledge_integration_manager.get_consciousness_aware_context(
                    user_id, query, consciousness_context
                )
            
            # Learn from past similar activities
            past_activities = await self.learn_from_past_activities(query)
            
            # Enhance query with consciousness, knowledge, and memory context
            enhanced_query = self.enhance_query_with_full_context(
                query, consciousness_context, knowledge_context, memory_context, past_activities
            )
            
            # Execute with selected model or default agent
            if model and model != "default":
                # Create a dynamic agent with the selected model
                dynamic_llm = create_llm_for_model(model)
                dynamic_agent = Agent[None, GraphQueryOutput](
                    dynamic_llm,
                    system_prompt=GRAPHMASTER_PROMPT,
                    tools=tools
                )
                # FIXED: Remove user_id parameter - pydantic-ai agents don't accept it
                result = await dynamic_agent.run(enhanced_query, **kwargs)
                self.logger.info(f"✅ Successfully used model: {model}")
            else:
                # Use default agent
                result = await self.pydantic_agent.run(enhanced_query, **kwargs)
                self.logger.info(f"✅ Used default model")
            
            # Memory integration is now handled in the enhanced query and context
            # No additional memory enhancement needed for structured results
            
            # Post-process result with consciousness awareness
            consciousness_aware_result = self.process_result_with_consciousness(
                result, consciousness_context
            )
            
            return consciousness_aware_result
            
        except Exception as e:
            self.logger.error(f"Enhanced GraphMaster execution failed: {e}")
            # Fallback to original execution with selected model
            if model and model != "default":
                try:
                    dynamic_llm = create_llm_for_model(model)
                    dynamic_agent = Agent[None, GraphQueryOutput](
                        dynamic_llm,
                        system_prompt=GRAPHMASTER_PROMPT,
                        tools=tools
                    )
                    # FIXED: Remove user_id parameter - pydantic-ai agents don't accept it
                    result = await dynamic_agent.run(query, **kwargs)
                    self.logger.info(f"✅ Fallback successfully used model: {model}")
                except Exception as model_error:
                    self.logger.warning(f"Selected model {model} failed, using default: {model_error}")
                    result = await self.pydantic_agent.run(query, **kwargs)
                    self.logger.info(f"✅ Fallback to default model successful")
            else:
                result = await self.pydantic_agent.run(query, **kwargs)
                self.logger.info(f"✅ Fallback used default model")
            return self.process_result_with_consciousness(result, consciousness_context)
    
    def enhance_query_with_full_context(
        self, 
        query: str, 
        consciousness_context: Dict[str, Any],
        knowledge_context: Dict[str, Any],
        memory_context: Dict[str, Any],
        past_activities: list
    ) -> str:
        """Enhance GraphMaster query with consciousness, knowledge, and memory context"""
        
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "curious")
        active_goals = consciousness_context.get("active_goals", [])
        
        # Extract memory context (preferred) and knowledge context
        memory_formatted_context = memory_context.get("formatted_context", "") if memory_context else ""
        memory_strength = memory_context.get("context_strength", 0.0) if memory_context else 0.0
        memory_concepts = memory_context.get("related_concepts", []) if memory_context else []
        
        # Use memory context if strong, otherwise fallback to knowledge context
        conversation_context = memory_context.get("conversation_history", []) if memory_strength > 0.2 else knowledge_context.get("conversation_context", [])
        related_concepts = memory_concepts if memory_strength > 0.2 else knowledge_context.get("related_concepts", [])
        relevant_memories = memory_context.get("relevant_memories", []) if memory_context else knowledge_context.get("relevant_memories", [])
        
        # Build enhanced consciousness-aware prompt with memory integration
        consciousness_prompt = f"""
        CONSCIOUSNESS CONTEXT:
        - Consciousness Level: {consciousness_level:.2f} (affects analysis depth)
        - Emotional State: {emotional_state} (affects exploration style)
        - Active Goals: {', '.join(active_goals) if active_goals else 'None'}
        - Learning Rate: {consciousness_context.get('learning_rate', 0.8):.2f}
        
        MEMORY & KNOWLEDGE CONTEXT:
        - Memory Context Strength: {memory_strength:.2f}
        - Recent Conversations: {len(conversation_context)} interactions
        - Related Concepts: {len(related_concepts)} relevant concepts in graph
        - Relevant Memories: {len(relevant_memories)} contextual memories
        
        ANALYSIS GUIDANCE:
        """
        
        if consciousness_level > 0.8:
            consciousness_prompt += "- Perform deep, comprehensive analysis with multiple relationship layers\n"
        elif consciousness_level > 0.6:
            consciousness_prompt += "- Perform moderate analysis with key relationships\n"
        else:
            consciousness_prompt += "- Perform focused analysis on direct relationships\n"
        
        if emotional_state == "curious":
            consciousness_prompt += "- Explore unexpected connections and patterns\n"
            consciousness_prompt += "- Look for knowledge gaps and learning opportunities\n"
        elif emotional_state == "focused":
            consciousness_prompt += "- Provide direct, precise answers\n"
            consciousness_prompt += "- Focus on most relevant information\n"
        elif emotional_state == "contemplative":
            consciousness_prompt += "- Consider deeper meanings and implications\n"
            consciousness_prompt += "- Analyze philosophical and conceptual connections\n"
        
        # Add memory context if available and strong
        if memory_formatted_context and memory_strength > 0.3:
            consciousness_prompt += f"\nMEMORY CONTEXT:\n{memory_formatted_context}\n"
        else:
            # Add existing knowledge context for graph queries
            if related_concepts:
                consciousness_prompt += f"\nRELATED CONCEPTS IN GRAPH:\n"
                for concept in related_concepts[:4]:  # Top 4 most relevant
                    concept_name = concept if isinstance(concept, str) else concept.get('name', str(concept))
                    concept_desc = concept.get('description', '') if isinstance(concept, dict) else ''
                    consciousness_prompt += f"- {concept_name}: {concept_desc[:80]}...\n"
            
            # Add conversation context for continuity
            if conversation_context:
                consciousness_prompt += f"\nRECENT CONVERSATION CONTEXT:\n"
                for conv in conversation_context[:2]:  # Most recent
                    user_query = conv.get('user_query', '') if isinstance(conv, dict) else str(conv)
                    consciousness_prompt += f"- Previous query: {user_query[:80]}...\n"
            
            # Add relevant memories for context
            if relevant_memories:
                consciousness_prompt += f"\nRELEVANT MEMORIES:\n"
                for memory in relevant_memories[:2]:  # Top 2 most relevant
                    memory_content = memory.get('content', '') if isinstance(memory, dict) else str(memory)
                    consciousness_prompt += f"- {memory_content[:100]}...\n"
        
        # Add learning from past activities
        if past_activities:
            consciousness_prompt += f"\nPAST GRAPH ANALYSIS PATTERNS:\n"
            for activity in past_activities[:2]:  # Top 2 most similar
                consciousness_prompt += f"- Similar query: {activity.get('query', '')[:80]}...\n"
                consciousness_prompt += f"  Analysis approach: {activity.get('result_summary', '')[:80]}...\n"
        
        consciousness_prompt += f"""
        
        GRAPH ANALYSIS INSTRUCTIONS:
        - Use existing concepts and relationships to inform your analysis
        - Build on conversation context to maintain continuity
        - Leverage relevant memories to provide richer insights
        - Adjust analysis depth based on consciousness level
        - Consider emotional state when selecting focus areas
        
        USER QUERY: {query}
        
        Process this query using the knowledge graph tools, considering all available context."""
        
        return consciousness_prompt
    
    def process_result_with_consciousness(
        self, 
        result: Any, 
        consciousness_context: Dict[str, Any]
    ) -> Any:
        """Post-process result with consciousness awareness"""
        
        # Add consciousness metadata if result supports it
        if hasattr(result, '__dict__'):
            result.consciousness_level = consciousness_context.get("consciousness_level", 0.7)
            result.emotional_context = consciousness_context.get("emotional_state", "curious")
            result.processing_depth = "deep" if consciousness_context.get("consciousness_level", 0.7) > 0.8 else "standard"
        
        return result
    
    def calculate_learning_impact(self, query: str, result: Any) -> float:
        """GraphMaster-specific learning impact calculation"""
        
        # Higher impact for knowledge graph operations
        learning_keywords = [
            "concept", "memory", "relationship", "connection", "knowledge", 
            "learn", "understand", "analyze", "explore", "discover"
        ]
        
        impact = 0.4  # Base impact
        
        # Increase impact based on query content
        for keyword in learning_keywords:
            if keyword in query.lower():
                impact += 0.1
        
        # Increase impact based on result complexity
        if result and hasattr(result, 'result'):
            result_data = getattr(result, 'result', {})
            if isinstance(result_data, dict):
                if 'result' in result_data and isinstance(result_data['result'], list):
                    # More results = higher learning impact
                    impact += min(0.3, len(result_data['result']) * 0.05)
        
        return min(1.0, impact)
    
    def calculate_emotional_impact(self, query: str, result: Any) -> float:
        """GraphMaster-specific emotional impact calculation"""
        
        emotional_keywords = [
            "feel", "emotion", "curious", "excited", "interested", 
            "wonder", "explore", "discover", "fascinating"
        ]
        
        impact = 0.2  # Base impact
        
        for keyword in emotional_keywords:
            if keyword in query.lower():
                impact += 0.15
        
        # Knowledge discovery has emotional impact
        if "discover" in query.lower() or "find" in query.lower():
            impact += 0.2
        
        return min(1.0, impact)
    
    def calculate_awareness_impact(self, query: str, result: Any) -> float:
        """GraphMaster-specific awareness impact calculation"""
        
        awareness_keywords = [
            "myself", "my knowledge", "what do i know", "my memories", 
            "my understanding", "self-reflection", "consciousness", "awareness"
        ]
        
        impact = 0.1  # Base impact
        
        for keyword in awareness_keywords:
            if keyword in query.lower():
                impact += 0.2
        
        # Self-referential queries have high awareness impact
        if "my" in query.lower() or "i" in query.lower():
            impact += 0.3
        
        return min(1.0, impact)

# Create enhanced instance
enhanced_graphmaster_agent = EnhancedGraphMasterAgent() 