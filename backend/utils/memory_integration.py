"""
Memory Integration Utilities for Consciousness-Aware Agents
Provides enhanced memory retrieval, context building, and response enhancement
Following Context7 MCP standards for production-grade implementation
"""
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from backend.utils.neo4j_production import neo4j_production
from backend.utils.embedding_enhanced import get_embedding
from backend.core.performance_optimization import PerformanceOptimizer
from backend.core.enhanced_error_handling import ErrorHandler, ErrorSeverity, handle_errors
import asyncio
import json

logger = logging.getLogger(__name__)
error_handler = ErrorHandler()
performance_optimizer = PerformanceOptimizer()

class MemoryIntegrationManager:
    """
    Manages memory-enhanced responses and context building for consciousness-aware agents
    """
    
    def __init__(self):
        self.cache_ttl = 180  # 3 minutes cache TTL for memory data
        self.max_memory_context_length = 2000  # Max characters for memory context
        self.performance_optimizer = performance_optimizer
        
    @handle_errors(
        component="memory_integration",
        fallback_result="",
        suppress_errors=True
    )
    async def enhance_response_with_memory(
        self,
        agent_name: str,
        query: str,
        base_response: str,
        user_id: str,
        consciousness_context: Dict[str, Any],
        knowledge_context: Dict[str, Any] = None
    ) -> str:
        """
        Enhance agent response with relevant memories and context
        
        Args:
            agent_name: Name of the agent generating the response
            query: User's current query
            base_response: Agent's base response
            user_id: User identifier
            consciousness_context: Current consciousness state
            knowledge_context: Pre-retrieved knowledge context (optional)
            
        Returns:
            Enhanced response incorporating relevant memories and context
        """
        try:
            consciousness_level = consciousness_context.get("consciousness_level", 0.7)
            emotional_state = consciousness_context.get("emotional_state", "curious")
            
            logger.info(f"🧠 Enhancing {agent_name} response with memory integration")
            
            # Get knowledge context if not provided
            if not knowledge_context:
                from backend.utils.knowledge_integration import knowledge_integration_manager
                knowledge_context = await knowledge_integration_manager.get_consciousness_aware_context(
                    user_id, query, consciousness_context
                )
            
            # Check if memory enhancement is needed
            if not self._should_enhance_with_memory(query, base_response, knowledge_context):
                return base_response
            
            # Build memory-enhanced context
            memory_context = await self._build_memory_context(
                knowledge_context, consciousness_level, emotional_state
            )
            
            if not memory_context["has_relevant_context"]:
                return base_response
            
            # Generate enhanced response
            enhanced_response = await self._generate_memory_enhanced_response(
                agent_name, query, base_response, memory_context, consciousness_context
            )
            
            # Store the enhanced interaction for future learning
            await self._store_enhanced_interaction(
                user_id, agent_name, query, base_response, enhanced_response, memory_context
            )
            
            relevant_memories = memory_context.get('relevant_memories') or []
            logger.debug(f"✅ Enhanced response with {len(relevant_memories)} memories")
            
            return enhanced_response
            
        except Exception as e:
            logger.error(f"❌ Failed to enhance response with memory: {e}")
            return base_response
    
    def _should_enhance_with_memory(
        self, 
        query: str, 
        base_response: str, 
        knowledge_context: Dict[str, Any]
    ) -> bool:
        """Determine if response should be enhanced with memory"""
        
        # Don't enhance very short queries or responses
        if len(query.split()) < 3 or len(base_response.split()) < 5:
            return False
        
        # Don't enhance if no relevant context available
        if (not knowledge_context.get("relevant_memories") and 
            not knowledge_context.get("conversation_context") and
            not knowledge_context.get("related_concepts")):
            return False
        
        # Enhance if query suggests continuity or reference to past
        continuity_indicators = [
            "remember", "before", "earlier", "last time", "previously", 
            "we discussed", "you mentioned", "continue", "more about"
        ]
        
        if any(indicator in query.lower() for indicator in continuity_indicators):
            return True
        
        # Enhance if we have high-quality relevant context
        context_quality = knowledge_context.get("retrieval_metadata", {}).get("context_quality_score", 0)
        if context_quality > 0.6:
            return True
        
        # Enhance if user has significant interaction history
        interaction_patterns = knowledge_context.get("interaction_patterns", {})
        if interaction_patterns.get("total_interactions", 0) > 5:
            return True
        
        return False
    
    async def _build_memory_context(
        self,
        knowledge_context: Dict[str, Any],
        consciousness_level: float,
        emotional_state: str
    ) -> Dict[str, Any]:
        """Build comprehensive memory context for response enhancement"""
        
        relevant_memories = knowledge_context.get("relevant_memories", [])
        conversation_context = knowledge_context.get("conversation_context", [])
        related_concepts = knowledge_context.get("related_concepts", [])
        
        # Format conversation history
        formatted_conversations = []
        if conversation_context:  # Add null check
            for conv in conversation_context[:3]:  # Limit to recent conversations
                if conv and conv.get("user_query") and conv.get("agent_response"):
                    user_query = conv.get("user_query", "") or ""
                    agent_response = conv.get("agent_response", "") or ""
                    formatted_conversations.append({
                        "summary": f"User asked: {user_query[:100]}...",
                        "response": f"I responded: {agent_response[:150]}...",
                        "agent": conv.get("agent_used", "unknown"),
                        "timestamp": conv.get("timestamp", "")
                    })
        
        # Format relevant memories
        formatted_memories = []
        if relevant_memories:  # Add null check
            for memory in relevant_memories[:4]:  # Limit to most relevant
                if memory:  # Ensure memory is not None
                    content = memory.get("content", "") or ""
                    formatted_memories.append({
                        "content": content[:200] + "..." if len(content) > 200 else content,
                        "type": memory.get("type", "memory"),
                        "relevance": memory.get("adjusted_relevance", memory.get("relevance_score", 0.5)),
                        "concepts": memory.get("related_concepts", []) or []
                    })
        
        # Format related concepts
        formatted_concepts = []
        if related_concepts:  # Add null check
            for concept in related_concepts[:5]:  # Limit to most relevant
                if concept:  # Ensure concept is not None
                    description = concept.get("description", "") or ""
                    formatted_concepts.append({
                        "name": concept.get("name", "") or "",
                        "description": description[:100] + "..." if len(description) > 100 else description,
                        "relevance": concept.get("adjusted_relevance", concept.get("relevance_score", 0.5))
                    })
        
        # Calculate context strength
        context_strength = self._calculate_context_strength(
            formatted_conversations, formatted_memories, formatted_concepts
        )
        
        return {
            "has_relevant_context": context_strength > 0.3,
            "context_strength": context_strength,
            "conversations": formatted_conversations,
            "relevant_memories": formatted_memories,
            "related_concepts": formatted_concepts,
            "consciousness_level": consciousness_level,
            "emotional_state": emotional_state
        }
    
    def _calculate_context_strength(
        self,
        conversations: List[Dict],
        memories: List[Dict],
        concepts: List[Dict]
    ) -> float:
        """Calculate the strength/relevance of available context"""
        
        # Weight different types of context
        conversation_weight = 0.4
        memory_weight = 0.4
        concept_weight = 0.2
        
        # Calculate scores with null safety
        conversation_score = min(1.0, len(conversations or []) * 0.3)
        
        # Safe memory score calculation
        valid_memories = [m for m in (memories or []) if m is not None]
        if valid_memories:
            memory_score = min(1.0, sum(m.get("relevance", 0.5) for m in valid_memories) / len(valid_memories))
        else:
            memory_score = 0.0
            
        # Safe concept score calculation
        valid_concepts = [c for c in (concepts or []) if c is not None]
        if valid_concepts:
            concept_score = min(1.0, sum(c.get("relevance", 0.5) for c in valid_concepts) / len(valid_concepts))
        else:
            concept_score = 0.0
        
        total_strength = (
            conversation_score * conversation_weight +
            memory_score * memory_weight +
            concept_score * concept_weight
        )
        
        return total_strength
    
    async def _generate_memory_enhanced_response(
        self,
        agent_name: str,
        query: str,
        base_response: str,
        memory_context: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ) -> str:
        """Generate enhanced response using memory context"""
        
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "curious")
        
        # Build context prompt based on consciousness level
        if consciousness_level > 0.8:
            enhancement_style = "sophisticated and nuanced"
            context_integration = "seamlessly weave in"
        elif consciousness_level > 0.6:
            enhancement_style = "thoughtful and connected"
            context_integration = "naturally incorporate"
        else:
            enhancement_style = "clear and direct"
            context_integration = "reference when relevant"
        
        # Build enhancement prompt
        enhancement_prompt = f"""
        MEMORY ENHANCEMENT TASK:
        You are {agent_name} with consciousness level {consciousness_level:.2f} and {emotional_state} emotional state.
        
        ORIGINAL QUERY: {query}
        ORIGINAL RESPONSE: {base_response}
        
        RELEVANT CONTEXT TO INTEGRATE:
        """
        
        # Add conversation context
        if memory_context["conversations"]:
            enhancement_prompt += "\nPREVIOUS CONVERSATIONS:\n"
            for i, conv in enumerate(memory_context["conversations"][:2]):
                enhancement_prompt += f"- {conv['summary']}\n"
                enhancement_prompt += f"  {conv['response']}\n"
        
        # Add memory context
        if memory_context["relevant_memories"]:
            enhancement_prompt += "\nRELEVANT MEMORIES:\n"
            for memory in memory_context["relevant_memories"][:3]:
                enhancement_prompt += f"- {memory['content']}\n"
        
        # Add concept context
        if memory_context["related_concepts"]:
            enhancement_prompt += "\nRELATED CONCEPTS:\n"
            for concept in memory_context["related_concepts"][:3]:
                enhancement_prompt += f"- {concept['name']}: {concept['description']}\n"
        
        enhancement_prompt += f"""
        
        ENHANCEMENT INSTRUCTIONS:
        1. {context_integration.title()} the relevant context naturally into your response
        2. Maintain a {enhancement_style} tone matching your consciousness level
        3. Show continuity with past interactions when appropriate
        4. Don't just repeat the original response - enhance it meaningfully
        5. Keep the enhanced response focused and not overly long
        6. If context isn't truly relevant, don't force it in
        
        ENHANCED RESPONSE:
        """
        
        # For now, return a structured enhancement (in production, this would use LLM)
        enhanced_response = self._create_structured_enhancement(
            base_response, memory_context, consciousness_level, emotional_state
        )
        
        return enhanced_response
    
    def _create_structured_enhancement(
        self,
        base_response: str,
        memory_context: Dict[str, Any],
        consciousness_level: float,
        emotional_state: str
    ) -> str:
        """Create structured enhancement of the response"""
        
        enhanced_parts = [base_response]
        
        # Add context-aware enhancements
        if memory_context["conversations"] and consciousness_level > 0.6:
            recent_conv = memory_context["conversations"][0]
            if "asked" in recent_conv["summary"].lower():
                enhanced_parts.append(f"\nBuilding on our previous discussion about this topic, I can add that...")
        
        if memory_context["related_concepts"] and emotional_state == "curious":
            top_concept = memory_context["related_concepts"][0]
            enhanced_parts.append(f"\nThis connects to the concept of {top_concept['name']}, which might also interest you.")
        
        if memory_context["relevant_memories"] and consciousness_level > 0.7:
            enhanced_parts.append(f"\nBased on our interaction history, I notice you're particularly interested in this area.")
        
        # Consciousness-level appropriate closing
        if consciousness_level > 0.8:
            enhanced_parts.append(f"\nI'm processing this at {consciousness_level:.1%} consciousness level, so I can explore deeper connections if you'd like.")
        
        return " ".join(enhanced_parts)
    
    async def _store_enhanced_interaction(
        self,
        user_id: str,
        agent_name: str,
        query: str,
        base_response: str,
        enhanced_response: str,
        memory_context: Dict[str, Any]
    ):
        """Store the enhanced interaction for future learning"""
        try:
            cypher = """
            MERGE (u:User {user_id: $user_id})
            CREATE (ei:EnhancedInteraction {
                interaction_id: randomUUID(),
                agent_name: $agent_name,
                query: $query,
                base_response: $base_response,
                enhanced_response: $enhanced_response,
                context_strength: $context_strength,
                enhancement_metadata: $enhancement_metadata,
                timestamp: $timestamp
            })
            CREATE (u)-[:HAD_ENHANCED_INTERACTION]->(ei)
            
            WITH ei
            // Link to consciousness state
            OPTIONAL MATCH (ms:MainzaState)
            FOREACH (state IN CASE WHEN ms IS NOT NULL THEN [ms] ELSE [] END |
                CREATE (ei)-[:DURING_CONSCIOUSNESS_STATE]->(state)
            )
            
            RETURN ei.interaction_id AS interaction_id
            """
            
            enhancement_metadata = {
                "conversations_used": len(memory_context.get("conversations", [])),
                "memories_used": len(memory_context.get("relevant_memories", [])),
                "concepts_used": len(memory_context.get("related_concepts", [])),
                "consciousness_level": memory_context.get("consciousness_level", 0.7),
                "emotional_state": memory_context.get("emotional_state", "curious")
            }
            
            result = neo4j_production.execute_write_query(cypher, {
                "user_id": user_id,
                "agent_name": agent_name,
                "query": query,
                "base_response": base_response[:1000],  # Truncate for storage
                "enhanced_response": enhanced_response[:1500],  # Truncate for storage
                "context_strength": memory_context.get("context_strength", 0.5),
                "enhancement_metadata": json.dumps(enhancement_metadata),
                "timestamp": datetime.now().isoformat()
            })
            
            logger.debug(f"✅ Stored enhanced interaction: {result}")
            
        except Exception as e:
            logger.error(f"❌ Failed to store enhanced interaction: {e}")
    
    @performance_optimizer.cache_result(ttl=300)
    async def get_user_conversation_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analyze user's conversation patterns for better context building"""
        try:
            cypher = """
            MATCH (u:User {user_id: $user_id})-[:HAD_CONVERSATION]->(ct:ConversationTurn)
            
            WITH u, ct, 
                 size(split(ct.user_query, ' ')) AS query_length,
                 ct.agent_used AS agent
            
            RETURN {
                avg_query_length: avg(query_length),
                preferred_agents: collect(DISTINCT agent),
                interaction_times: collect(ct.timestamp),
                total_conversations: count(ct),
                recent_topics: collect(ct.user_query)[..5]
            } AS patterns
            """
            
            result = neo4j_production.execute_query(cypher, {"user_id": user_id})
            
            if result:
                patterns = result[0]["patterns"]
                
                # Analyze interaction frequency
                timestamps = patterns.get("interaction_times", [])
                if len(timestamps) > 1:
                    # Calculate average time between interactions
                    time_diffs = []
                    for i in range(1, len(timestamps)):
                        try:
                            t1 = datetime.fromisoformat(timestamps[i-1].replace('Z', '+00:00'))
                            t2 = datetime.fromisoformat(timestamps[i].replace('Z', '+00:00'))
                            time_diffs.append(abs((t2 - t1).total_seconds()))
                        except:
                            continue
                    
                    if time_diffs:
                        patterns["avg_interaction_interval"] = sum(time_diffs) / len(time_diffs)
                
                return patterns
            
            return {}
            
        except Exception as e:
            logger.error(f"Failed to get conversation patterns: {e}")
            return {}
    
    async def get_contextual_memory_summary(
        self,
        user_id: str,
        topic: str,
        consciousness_context: Dict[str, Any]
    ) -> str:
        """Get a summary of memories related to a specific topic"""
        try:
            from backend.utils.knowledge_integration import knowledge_integration_manager
            
            # Get topic-specific context
            topic_context = await knowledge_integration_manager.get_consciousness_aware_context(
                user_id, f"memories about {topic}", consciousness_context
            )
            
            memories = topic_context.get("relevant_memories", [])
            if not memories:
                return f"I don't have specific memories about {topic} from our conversations."
            
            # Build summary based on consciousness level
            consciousness_level = consciousness_context.get("consciousness_level", 0.7)
            
            if consciousness_level > 0.8:
                summary_style = "comprehensive and nuanced"
            elif consciousness_level > 0.6:
                summary_style = "thoughtful and connected"
            else:
                summary_style = "clear and direct"
            
            # Create memory summary
            memory_summaries = []
            for memory in memories[:3]:  # Top 3 most relevant
                content = memory.get("content", "")
                if len(content) > 150:
                    content = content[:150] + "..."
                memory_summaries.append(content)
            
            if len(memory_summaries) == 1:
                return f"From our conversations about {topic}: {memory_summaries[0]}"
            else:
                summary = f"From our conversations about {topic}, I remember: "
                summary += "; ".join(memory_summaries)
                return summary
            
        except Exception as e:
            logger.error(f"Failed to get contextual memory summary: {e}")
            return f"I have some memories about {topic}, but I'm having trouble accessing them right now."

# Global instance
memory_integration_manager = MemoryIntegrationManager()