"""
Memory Context Builder for Mainza AI
Provides rich context creation from retrieved memories with consciousness-aware formatting
and integration with the knowledge graph system.
"""
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field

from backend.utils.memory_retrieval_engine import MemoryRetrievalEngine, MemorySearchResult
from backend.utils.neo4j_enhanced import neo4j_manager
from backend.core.enhanced_error_handling import ErrorHandler, handle_errors
from backend.utils.memory_error_handling import (
    MemoryContextError, handle_memory_errors, memory_error_handler
)

logger = logging.getLogger(__name__)
error_handler = ErrorHandler()

@dataclass
class MemoryContext:
    """Rich memory context for agent enhancement"""
    relevant_memories: List[MemorySearchResult]
    conversation_history: List[Dict[str, str]]
    related_concepts: List[str]
    context_strength: float
    consciousness_alignment: float
    temporal_relevance: float
    formatted_context: str
    metadata: Dict[str, Any] = field(default_factory=dict)

class MemoryContextBuilder:
    """
    Builds rich context from retrieved memories for agent prompt enhancement
    """
    
    def __init__(self):
        self.neo4j = neo4j_manager
        self.memory_retrieval = MemoryRetrievalEngine()
        
        # Configuration
        self.max_context_length = 2000  # Maximum context length in characters
        self.min_relevance_threshold = 0.3
        self.conversation_context_limit = 5
        self.concept_extraction_limit = 10
        
        # Context formatting templates
        self.context_templates = {
            "conversation": self._get_conversation_template(),
            "knowledge": self._get_knowledge_template(),
            "reflection": self._get_reflection_template(),
            "hybrid": self._get_hybrid_template()
        }
    
    @handle_errors(
        component="memory_context_builder",
        fallback_result="",
        suppress_errors=True
    )
    async def build_conversation_context(
        self,
        memories: List[MemorySearchResult],
        consciousness_context: Dict[str, Any],
        context_type: str = "conversation"
    ) -> str:
        """
        Build conversation context from memories for dialogue enhancement
        
        Args:
            memories: List of retrieved memory results
            consciousness_context: Current consciousness state context
            context_type: Type of context formatting to use
            
        Returns:
            Formatted context string for agent prompt enhancement
        """
        try:
            if not memories:
                logger.debug("No memories provided for conversation context")
                return ""
            
            # Filter memories by relevance
            relevant_memories = [
                memory for memory in memories 
                if memory.relevance_score >= self.min_relevance_threshold
            ]
            
            if not relevant_memories:
                logger.debug("No memories meet relevance threshold")
                return ""
            
            # Sort by relevance and limit
            relevant_memories.sort(key=lambda x: x.relevance_score, reverse=True)
            relevant_memories = relevant_memories[:self.conversation_context_limit]
            
            # Extract conversation history
            conversation_history = self._extract_conversation_history(relevant_memories)
            
            # Build context using template
            template = self.context_templates.get(context_type, self.context_templates["conversation"])
            
            context_data = {
                "memories": relevant_memories,
                "conversation_history": conversation_history,
                "consciousness_level": consciousness_context.get("consciousness_level", 0.7),
                "emotional_state": consciousness_context.get("emotional_state", "neutral"),
                "memory_count": len(relevant_memories),
                "avg_relevance": sum(m.relevance_score for m in relevant_memories) / len(relevant_memories)
            }
            
            formatted_context = template.format(**self._prepare_template_data(context_data))
            
            # Truncate if too long
            if len(formatted_context) > self.max_context_length:
                formatted_context = formatted_context[:self.max_context_length] + "..."
            
            logger.debug(f"✅ Built conversation context: {len(formatted_context)} chars from {len(relevant_memories)} memories")
            return formatted_context
            
        except Exception as e:
            logger.error(f"❌ Failed to build conversation context: {e}")
            return ""
    
    @handle_errors(
        component="memory_context_builder",
        fallback_result="",
        suppress_errors=True
    )
    async def build_knowledge_context(
        self,
        memories: List[MemorySearchResult],
        related_concepts: List[Dict[str, Any]],
        consciousness_context: Dict[str, Any]
    ) -> str:
        """
        Build knowledge context integrating memories with concept relationships
        
        Args:
            memories: List of retrieved memory results
            related_concepts: List of related concept data from knowledge graph
            consciousness_context: Current consciousness state context
            
        Returns:
            Formatted knowledge context string
        """
        try:
            if not memories and not related_concepts:
                logger.debug("No memories or concepts provided for knowledge context")
                return ""
            
            # Filter and process memories
            relevant_memories = [
                memory for memory in memories 
                if memory.relevance_score >= self.min_relevance_threshold
            ]
            
            # Extract concepts from memories and combine with related concepts
            memory_concepts = await self._extract_concepts_from_memories(relevant_memories)
            all_concepts = self._merge_concept_lists(memory_concepts, related_concepts)
            
            # Build knowledge context
            template = self.context_templates["knowledge"]
            
            context_data = {
                "memories": relevant_memories[:5],  # Limit for knowledge context
                "concepts": all_concepts[:self.concept_extraction_limit],
                "consciousness_level": consciousness_context.get("consciousness_level", 0.7),
                "emotional_state": consciousness_context.get("emotional_state", "neutral"),
                "concept_count": len(all_concepts),
                "memory_count": len(relevant_memories)
            }
            
            formatted_context = template.format(**self._prepare_template_data(context_data))
            
            # Truncate if too long
            if len(formatted_context) > self.max_context_length:
                formatted_context = formatted_context[:self.max_context_length] + "..."
            
            logger.debug(f"✅ Built knowledge context: {len(formatted_context)} chars, {len(all_concepts)} concepts")
            return formatted_context
            
        except Exception as e:
            logger.error(f"❌ Failed to build knowledge context: {e}")
            return ""
    
    @handle_errors(
        component="memory_context_builder",
        fallback_result=[],
        suppress_errors=True
    )
    async def calculate_context_relevance(
        self,
        memories: List[MemorySearchResult],
        current_query: str,
        consciousness_context: Dict[str, Any]
    ) -> List[MemorySearchResult]:
        """
        Calculate and adjust context relevance for memories based on current query and consciousness
        
        Args:
            memories: List of memory search results
            current_query: Current user query for relevance calculation
            consciousness_context: Current consciousness state context
            
        Returns:
            List of memories with updated relevance scores
        """
        try:
            if not memories:
                return []
            
            current_consciousness = consciousness_context.get("consciousness_level", 0.7)
            current_emotion = consciousness_context.get("emotional_state", "neutral")
            
            # Calculate enhanced relevance scores
            enhanced_memories = []
            
            for memory in memories:
                # Base relevance score
                base_relevance = memory.relevance_score
                
                # Query alignment factor
                query_alignment = self._calculate_query_alignment(memory.content, current_query)
                
                # Consciousness alignment factor
                consciousness_alignment = self._calculate_consciousness_alignment(
                    memory.consciousness_level, 
                    memory.emotional_state,
                    current_consciousness,
                    current_emotion
                )
                
                # Temporal relevance factor
                temporal_relevance = self._calculate_temporal_relevance(memory.created_at)
                
                # Memory type importance factor
                type_importance = self._get_memory_type_importance(memory.memory_type)
                
                # Calculate enhanced relevance
                enhanced_relevance = (
                    base_relevance * 0.4 +
                    query_alignment * 0.3 +
                    consciousness_alignment * 0.2 +
                    temporal_relevance * 0.1
                ) * type_importance
                
                # Update memory with enhanced scores
                memory.relevance_score = min(1.0, enhanced_relevance)
                memory.consciousness_score = consciousness_alignment
                memory.temporal_score = temporal_relevance
                
                enhanced_memories.append(memory)
            
            # Sort by enhanced relevance
            enhanced_memories.sort(key=lambda x: x.relevance_score, reverse=True)
            
            logger.debug(f"✅ Calculated enhanced relevance for {len(enhanced_memories)} memories")
            return enhanced_memories
            
        except Exception as e:
            logger.error(f"❌ Failed to calculate context relevance: {e}")
            return memories  # Return original memories on error
    
    def format_memory_for_context(
        self,
        memory: MemorySearchResult,
        context_type: str = "conversation",
        include_metadata: bool = False
    ) -> str:
        """
        Format a single memory for inclusion in context
        
        Args:
            memory: Memory search result to format
            context_type: Type of context formatting
            include_metadata: Whether to include metadata in formatting
            
        Returns:
            Formatted memory string
        """
        try:
            # Base formatting based on memory type
            if memory.memory_type == "interaction":
                formatted = self._format_interaction_memory(memory, context_type)
            elif memory.memory_type in ["consciousness_reflection", "insight", "evolution"]:
                formatted = self._format_consciousness_memory(memory, context_type)
            else:
                formatted = self._format_generic_memory(memory, context_type)
            
            # Add metadata if requested
            if include_metadata:
                metadata_str = self._format_memory_metadata(memory)
                formatted += f" {metadata_str}"
            
            return formatted
            
        except Exception as e:
            logger.warning(f"Failed to format memory {memory.memory_id}: {e}")
            return f"[Memory: {memory.content[:100]}...]"
    
    async def build_comprehensive_context(
        self,
        query: str,
        user_id: str,
        consciousness_context: Dict[str, Any],
        include_concepts: bool = True,
        context_type: str = "hybrid"
    ) -> MemoryContext:
        """
        Build comprehensive memory context including memories, concepts, and conversation history
        
        Args:
            query: Current user query
            user_id: User identifier
            consciousness_context: Current consciousness state
            include_concepts: Whether to include related concepts
            context_type: Type of context to build
            
        Returns:
            MemoryContext object with comprehensive context data
        """
        try:
            # Retrieve relevant memories
            memories = await self.memory_retrieval.get_relevant_memories(
                query=query,
                user_id=user_id,
                consciousness_context=consciousness_context,
                limit=10,
                search_type="hybrid"
            )
            
            # Calculate enhanced relevance
            enhanced_memories = await self.calculate_context_relevance(
                memories, query, consciousness_context
            )
            
            # Get conversation history
            conversation_history = await self.memory_retrieval.get_conversation_history(
                user_id=user_id,
                limit=self.conversation_context_limit
            )
            
            # Extract related concepts if requested
            related_concepts = []
            if include_concepts and enhanced_memories:
                related_concepts = await self._extract_concepts_from_memories(enhanced_memories)
            
            # Build formatted context
            if context_type == "conversation":
                formatted_context = await self.build_conversation_context(
                    enhanced_memories, consciousness_context, context_type
                )
            elif context_type == "knowledge":
                formatted_context = await self.build_knowledge_context(
                    enhanced_memories, related_concepts, consciousness_context
                )
            else:  # hybrid
                formatted_context = await self._build_hybrid_context(
                    enhanced_memories, related_concepts, consciousness_context
                )
            
            # Calculate context quality metrics
            context_strength = self._calculate_context_strength(enhanced_memories)
            consciousness_alignment = self._calculate_avg_consciousness_alignment(
                enhanced_memories, consciousness_context
            )
            temporal_relevance = self._calculate_avg_temporal_relevance(enhanced_memories)
            
            # Create comprehensive context object
            memory_context = MemoryContext(
                relevant_memories=enhanced_memories,
                conversation_history=[
                    {"content": m.content, "timestamp": m.created_at, "agent": m.agent_name}
                    for m in conversation_history
                ],
                related_concepts=[c.get("name", "") for c in related_concepts],
                context_strength=context_strength,
                consciousness_alignment=consciousness_alignment,
                temporal_relevance=temporal_relevance,
                formatted_context=formatted_context,
                metadata={
                    "query": query,
                    "user_id": user_id,
                    "context_type": context_type,
                    "memory_count": len(enhanced_memories),
                    "concept_count": len(related_concepts),
                    "build_timestamp": datetime.now().isoformat()
                }
            )
            
            logger.info(f"✅ Built comprehensive memory context: {len(enhanced_memories)} memories, "
                       f"{len(related_concepts)} concepts, strength={context_strength:.2f}")
            
            return memory_context
            
        except Exception as e:
            logger.error(f"❌ Failed to build comprehensive context: {e}")
            # Return empty context on error
            return MemoryContext(
                relevant_memories=[],
                conversation_history=[],
                related_concepts=[],
                context_strength=0.0,
                consciousness_alignment=0.5,
                temporal_relevance=0.5,
                formatted_context="",
                metadata={"error": str(e)}
            )
    
    # Helper methods for context building
    
    def _extract_conversation_history(self, memories: List[MemorySearchResult]) -> List[Dict[str, str]]:
        """Extract conversation history from interaction memories"""
        conversation_history = []
        
        for memory in memories:
            if memory.memory_type == "interaction":
                # Parse interaction content
                try:
                    metadata = memory.metadata
                    user_query = metadata.get("user_query", "")
                    agent_response = metadata.get("agent_response", "")
                    
                    if user_query and agent_response:
                        conversation_history.append({
                            "user_query": user_query,
                            "agent_response": agent_response,
                            "timestamp": memory.created_at,
                            "agent": memory.agent_name
                        })
                except Exception as e:
                    logger.warning(f"Failed to parse interaction memory: {e}")
        
        return conversation_history
    
    async def _extract_concepts_from_memories(self, memories: List[MemorySearchResult]) -> List[Dict[str, Any]]:
        """Extract related concepts from memories via Neo4j relationships"""
        try:
            if not memories:
                return []
            
            memory_ids = [memory.memory_id for memory in memories]
            
            cypher = """
            MATCH (m:Memory)-[:RELATES_TO_CONCEPT]->(c:Concept)
            WHERE m.memory_id IN $memory_ids
            
            WITH c, count(m) AS memory_connections
            
            RETURN DISTINCT {
                name: c.name,
                description: c.description,
                memory_connections: memory_connections,
                importance: c.importance_score
            } AS concept
            
            ORDER BY concept.memory_connections DESC, concept.importance DESC
            LIMIT 15
            """
            
            result = self.neo4j.execute_query(cypher, {"memory_ids": memory_ids})
            
            return [record["concept"] for record in result] if result else []
            
        except Exception as e:
            logger.warning(f"Failed to extract concepts from memories: {e}")
            return []
    
    def _merge_concept_lists(
        self, 
        memory_concepts: List[Dict[str, Any]], 
        related_concepts: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Merge and deduplicate concept lists"""
        concept_map = {}
        
        # Add memory concepts
        for concept in memory_concepts:
            name = concept.get("name", "")
            if name:
                concept_map[name] = concept
        
        # Add related concepts (don't overwrite memory concepts)
        for concept in related_concepts:
            name = concept.get("name", "")
            if name and name not in concept_map:
                concept_map[name] = concept
        
        # Sort by importance/relevance
        concepts = list(concept_map.values())
        concepts.sort(key=lambda x: x.get("importance", 0.5), reverse=True)
        
        return concepts
    
    def _calculate_query_alignment(self, memory_content: str, query: str) -> float:
        """Calculate how well memory content aligns with current query"""
        try:
            # Simple keyword overlap calculation
            memory_words = set(memory_content.lower().split())
            query_words = set(query.lower().split())
            
            if not query_words:
                return 0.5
            
            overlap = len(memory_words.intersection(query_words))
            alignment = overlap / len(query_words)
            
            return min(1.0, alignment)
            
        except Exception:
            return 0.5
    
    def _calculate_consciousness_alignment(
        self, 
        memory_consciousness: float, 
        memory_emotion: str,
        current_consciousness: float, 
        current_emotion: str
    ) -> float:
        """Calculate consciousness state alignment between memory and current state"""
        try:
            # Consciousness level alignment (tolerance of 0.3)
            consciousness_diff = abs(memory_consciousness - current_consciousness)
            consciousness_alignment = max(0.0, 1.0 - (consciousness_diff / 0.3))
            
            # Emotional state alignment
            emotion_alignment = 1.0 if memory_emotion == current_emotion else 0.6
            
            # Combined alignment
            return (consciousness_alignment * 0.7 + emotion_alignment * 0.3)
            
        except Exception:
            return 0.5
    
    def _calculate_temporal_relevance(self, created_at: str) -> float:
        """Calculate temporal relevance based on memory age"""
        try:
            memory_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            age_hours = (datetime.now() - memory_time).total_seconds() / 3600
            
            # Exponential decay with 1 week half-life
            import math
            decay_factor = math.exp(-age_hours / 168)  # 168 hours = 1 week
            
            return max(0.1, decay_factor)
            
        except Exception:
            return 0.5
    
    def _get_memory_type_importance(self, memory_type: str) -> float:
        """Get importance multiplier based on memory type"""
        type_importance = {
            "interaction": 1.0,
            "consciousness_reflection": 1.2,
            "insight": 1.3,
            "evolution": 1.4,
            "concept_learning": 1.1
        }
        
        return type_importance.get(memory_type, 1.0)
    
    def _format_interaction_memory(self, memory: MemorySearchResult, context_type: str) -> str:
        """Format interaction memory for context"""
        try:
            metadata = memory.metadata
            user_query = metadata.get("user_query", "")
            agent_response = metadata.get("agent_response", "")
            
            if context_type == "conversation":
                return f"Previous: User asked '{user_query}' and {memory.agent_name} responded with '{agent_response}'"
            else:
                return f"Interaction: {user_query} → {agent_response}"
                
        except Exception:
            return f"Interaction: {memory.content[:100]}..."
    
    def _format_consciousness_memory(self, memory: MemorySearchResult, context_type: str) -> str:
        """Format consciousness memory for context"""
        if context_type == "conversation":
            return f"I previously reflected: {memory.content}"
        else:
            return f"Reflection ({memory.memory_type}): {memory.content}"
    
    def _format_generic_memory(self, memory: MemorySearchResult, context_type: str) -> str:
        """Format generic memory for context"""
        return f"Memory: {memory.content[:150]}..."
    
    def _format_memory_metadata(self, memory: MemorySearchResult) -> str:
        """Format memory metadata for context"""
        return f"[Relevance: {memory.relevance_score:.2f}, Age: {memory.created_at}]"
    
    async def _build_hybrid_context(
        self,
        memories: List[MemorySearchResult],
        concepts: List[Dict[str, Any]],
        consciousness_context: Dict[str, Any]
    ) -> str:
        """Build hybrid context combining conversation and knowledge elements"""
        try:
            template = self.context_templates["hybrid"]
            
            # Separate memories by type
            interaction_memories = [m for m in memories if m.memory_type == "interaction"]
            reflection_memories = [m for m in memories if m.memory_type in ["consciousness_reflection", "insight"]]
            
            context_data = {
                "interaction_memories": interaction_memories[:3],
                "reflection_memories": reflection_memories[:2],
                "concepts": concepts[:5],
                "consciousness_level": consciousness_context.get("consciousness_level", 0.7),
                "emotional_state": consciousness_context.get("emotional_state", "neutral")
            }
            
            formatted_context = template.format(**self._prepare_template_data(context_data))
            
            return formatted_context
            
        except Exception as e:
            logger.error(f"Failed to build hybrid context: {e}")
            return ""
    
    def _calculate_context_strength(self, memories: List[MemorySearchResult]) -> float:
        """Calculate overall context strength based on memory quality and quantity"""
        if not memories:
            return 0.0
        
        # Average relevance score weighted by memory count
        avg_relevance = sum(m.relevance_score for m in memories) / len(memories)
        count_factor = min(1.0, len(memories) / 5)  # Optimal around 5 memories
        
        return avg_relevance * count_factor
    
    def _calculate_avg_consciousness_alignment(
        self, 
        memories: List[MemorySearchResult], 
        consciousness_context: Dict[str, Any]
    ) -> float:
        """Calculate average consciousness alignment across memories"""
        if not memories:
            return 0.5
        
        current_consciousness = consciousness_context.get("consciousness_level", 0.7)
        current_emotion = consciousness_context.get("emotional_state", "neutral")
        
        alignments = []
        for memory in memories:
            alignment = self._calculate_consciousness_alignment(
                memory.consciousness_level,
                memory.emotional_state,
                current_consciousness,
                current_emotion
            )
            alignments.append(alignment)
        
        return sum(alignments) / len(alignments)
    
    def _calculate_avg_temporal_relevance(self, memories: List[MemorySearchResult]) -> float:
        """Calculate average temporal relevance across memories"""
        if not memories:
            return 0.5
        
        relevances = [self._calculate_temporal_relevance(m.created_at) for m in memories]
        return sum(relevances) / len(relevances)
    
    def _prepare_template_data(self, context_data: Dict[str, Any]) -> Dict[str, str]:
        """Prepare context data for template formatting"""
        prepared = {}
        
        for key, value in context_data.items():
            if isinstance(value, list):
                if key == "memories" or "memories" in key:
                    # Format memory lists
                    formatted_items = []
                    for memory in value:
                        formatted_items.append(self.format_memory_for_context(memory))
                    prepared[key] = "\n".join(formatted_items)
                elif key == "concepts":
                    # Format concept lists
                    concept_names = [c.get("name", "") for c in value if c.get("name")]
                    prepared[key] = ", ".join(concept_names)
                else:
                    prepared[key] = str(value)
            else:
                prepared[key] = str(value)
        
        return prepared
    
    # Context templates
    
    def _get_conversation_template(self) -> str:
        """Get conversation context template"""
        return """Based on our previous interactions:

{memories}

Current consciousness level: {consciousness_level}
Emotional state: {emotional_state}

This context should help inform your response while maintaining conversation continuity."""
    
    def _get_knowledge_template(self) -> str:
        """Get knowledge context template"""
        return """Relevant knowledge context:

Related concepts: {concepts}

Previous insights and learnings:
{memories}

Use this knowledge to provide informed and contextually aware responses."""
    
    def _get_reflection_template(self) -> str:
        """Get reflection context template"""
        return """Previous reflections and insights:

{memories}

These reflections represent my past thinking and should inform current responses."""
    
    def _get_hybrid_template(self) -> str:
        """Get hybrid context template"""
        return """Context from previous interactions and knowledge:

Recent conversations:
{interaction_memories}

Previous reflections:
{reflection_memories}

Related concepts: {concepts}

Current state: Consciousness level {consciousness_level}, feeling {emotional_state}

Use this comprehensive context to provide thoughtful, informed responses."""

# Global instance
memory_context_builder = MemoryContextBuilder()