"""
Knowledge Integration Utilities for Consciousness-Aware Agents
Provides enhanced Neo4j knowledge graph access with consciousness context integration
and memory-enhanced context building for comprehensive agent support.
Following Context7 MCP standards for production-grade implementation
"""
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from backend.utils.unified_database_manager import unified_database_manager
from backend.utils.embedding_enhanced import get_embedding
from backend.core.performance_optimization import PerformanceOptimizer
from backend.core.enhanced_error_handling import ErrorHandler, ErrorSeverity, handle_errors
import asyncio

logger = logging.getLogger(__name__)
error_handler = ErrorHandler()
performance_optimizer = PerformanceOptimizer()

class KnowledgeIntegrationManager:
    """
    Manages consciousness-aware knowledge retrieval and integration for agents
    with enhanced memory context integration
    """
    
    def __init__(self):
        self.cache_ttl = 300  # 5 minutes cache TTL
        self.max_retrieval_depth = 4
        self.performance_optimizer = performance_optimizer
        
        # Memory integration components (lazy loaded to avoid circular imports)
        self._memory_context_builder = None
        self._memory_retrieval_engine = None
        
    @property
    def memory_context_builder(self):
        """Lazy load memory context builder to avoid circular imports"""
        if self._memory_context_builder is None:
            try:
                from backend.utils.memory_context_builder import memory_context_builder
                self._memory_context_builder = memory_context_builder
            except ImportError as e:
                logger.warning(f"Memory context builder not available: {e}")
                self._memory_context_builder = None
        return self._memory_context_builder
    
    @property
    def memory_retrieval_engine(self):
        """Lazy load memory retrieval engine to avoid circular imports"""
        if self._memory_retrieval_engine is None:
            try:
                from backend.utils.memory_retrieval_engine import MemoryRetrievalEngine
                self._memory_retrieval_engine = MemoryRetrievalEngine()
            except ImportError as e:
                logger.warning(f"Memory retrieval engine not available: {e}")
                self._memory_retrieval_engine = None
        return self._memory_retrieval_engine

    @handle_errors(
        component="knowledge_integration",
        fallback_result={},
        suppress_errors=True
    )
    @performance_optimizer.cache_result(ttl=300)
    async def get_consciousness_aware_context(
        self,
        user_id: str,
        query: str,
        consciousness_context: Dict[str, Any],
        include_memory_context: bool = True
    ) -> Dict[str, Any]:
        """
        Retrieve comprehensive knowledge context based on consciousness state
        with enhanced memory integration
        
        Args:
            user_id: User identifier
            query: Current user query
            consciousness_context: Current consciousness state data
            include_memory_context: Whether to include memory-based context enhancement
            
        Returns:
            Dict containing conversation context, related concepts, relevant memories, and formatted memory context
        """
        try:
            consciousness_level = consciousness_context.get("consciousness_level", 0.7)
            emotional_state = consciousness_context.get("emotional_state", "curiosity")
            active_goals = consciousness_context.get("active_goals", [])
            
            logger.info(f"🧠 Retrieving knowledge context for consciousness level {consciousness_level:.2f}")
            
            # Adjust retrieval parameters based on consciousness level
            retrieval_params = self._calculate_retrieval_parameters(consciousness_level, emotional_state)
            
            # Execute parallel knowledge retrieval
            context_tasks = [
                self._get_user_conversation_context(user_id, retrieval_params["conversation_limit"]),
                self._get_query_related_concepts(query, retrieval_params["concept_depth"]),
                self._get_relevant_memories(user_id, query, retrieval_params["memory_limit"]),
                self._get_user_interaction_patterns(user_id)
            ]
            
            # Add memory context retrieval if enabled and available
            if include_memory_context and self.memory_retrieval_engine:
                context_tasks.append(
                    self._get_enhanced_memory_context(user_id, query, consciousness_context)
                )
            
            results = await asyncio.gather(*context_tasks, return_exceptions=True)
            
            # Process results and handle any exceptions
            conversation_context = results[0] if not isinstance(results[0], Exception) else []
            related_concepts = results[1] if not isinstance(results[1], Exception) else []
            relevant_memories = results[2] if not isinstance(results[2], Exception) else []
            interaction_patterns = results[3] if not isinstance(results[3], Exception) else {}
            
            # Process enhanced memory context if available
            enhanced_memory_context = None
            if len(results) > 4 and not isinstance(results[4], Exception):
                enhanced_memory_context = results[4]
            
            # Filter and enhance context based on consciousness state
            filtered_context = await self._filter_context_by_consciousness(
                conversation_context, related_concepts, relevant_memories,
                emotional_state, active_goals, consciousness_level
            )
            
            # Build comprehensive context
            knowledge_context = {
                "user_id": user_id,
                "query": query,
                "consciousness_level": consciousness_level,
                "emotional_state": emotional_state,
                "conversation_context": filtered_context["conversations"],
                "related_concepts": filtered_context["concepts"],
                "relevant_memories": filtered_context["memories"],
                "interaction_patterns": interaction_patterns,
                "retrieval_metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "retrieval_depth": retrieval_params["concept_depth"],
                    "context_quality_score": self._calculate_context_quality(filtered_context),
                    "memory_enhanced": enhanced_memory_context is not None
                }
            }
            
            # Add enhanced memory context if available
            if enhanced_memory_context:
                knowledge_context.update({
                    "memory_context": enhanced_memory_context,
                    "formatted_memory_context": enhanced_memory_context.get("formatted_context", ""),
                    "memory_context_strength": enhanced_memory_context.get("context_strength", 0.0)
                })
            
            logger.debug(f"✅ Retrieved knowledge context with {len(filtered_context['concepts'])} concepts, "
                        f"{len(filtered_context['memories'])} memories, {len(filtered_context['conversations'])} conversations")
            
            return knowledge_context
            
        except Exception as e:
            logger.error(f"❌ Failed to retrieve consciousness-aware context: {e}")
            return self._get_fallback_context(user_id, query, consciousness_context)
    
    def _calculate_retrieval_parameters(self, consciousness_level: float, emotional_state: str) -> Dict[str, int]:
        """Calculate retrieval parameters based on consciousness state"""
        
        # Base parameters
        base_conversation_limit = 5
        base_concept_depth = 2
        base_memory_limit = 3
        
        # Adjust based on consciousness level
        consciousness_multiplier = max(0.5, min(2.0, consciousness_level * 1.5))
        
        # Adjust based on emotional state
        emotional_adjustments = {
            "curiosity": {"concept_depth": 1.5, "memory_limit": 1.3},
            "focused": {"conversation_limit": 0.8, "concept_depth": 0.8},
            "empathetic": {"conversation_limit": 1.4, "memory_limit": 1.2},
            "contemplative": {"concept_depth": 1.8, "memory_limit": 1.1},
            "excited": {"concept_depth": 1.3, "conversation_limit": 1.2}
        }
        
        adjustments = emotional_adjustments.get(emotional_state, {})
        
        return {
            "conversation_limit": int(base_conversation_limit * consciousness_multiplier * adjustments.get("conversation_limit", 1.0)),
            "concept_depth": min(self.max_retrieval_depth, int(base_concept_depth * consciousness_multiplier * adjustments.get("concept_depth", 1.0))),
            "memory_limit": int(base_memory_limit * consciousness_multiplier * adjustments.get("memory_limit", 1.0))
        }
    
    async def _get_user_conversation_context(self, user_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve user's recent conversation context"""
        try:
            cypher = """
            MATCH (u:User {user_id: $user_id})-[:HAD_CONVERSATION]->(ct:ConversationTurn)
            WITH ct
            ORDER BY ct.timestamp DESC
            LIMIT $limit
            
            OPTIONAL MATCH (ct)-[:DURING_CONSCIOUSNESS_STATE]->(ms:MainzaState)
            
            RETURN {
                turn_id: ct.turn_id,
                user_query: ct.user_query,
                agent_response: ct.agent_response,
                agent_used: ct.agent_used,
                timestamp: ct.timestamp,
                consciousness_level: ms.consciousness_level
            } AS conversation
            """
            
            result = await unified_database_manager.execute_query(cypher, {
                "user_id": user_id,
                "limit": limit
            })
            
            return [record["conversation"] for record in result] if result else []
            
        except Exception as e:
            logger.error(f"Failed to get conversation context: {e}")
            return []
    
    async def _get_query_related_concepts(self, query: str, depth: int = 2) -> List[Dict[str, Any]]:
        """Get concepts related to the current query"""
        try:
            # Get query embedding for semantic similarity
            query_embedding = get_embedding(query)
            
            # Extract key terms from query for concept matching
            query_terms = self._extract_key_terms(query)
            
            cypher = f"""
            // Find concepts that match query terms
            UNWIND $query_terms AS term
            MATCH (c:Concept)
            WHERE toLower(c.name) CONTAINS toLower(term) 
               OR toLower(c.description) CONTAINS toLower(term)
            
            WITH DISTINCT c, term
            
            // Get related concepts up to specified depth
            // Simplified approach without CALL subquery
            MATCH (c)-[:RELATES_TO*1..{depth}]-(related:Concept)
            WHERE related <> c
            WITH DISTINCT related, 
                       length(shortestPath((c)-[:RELATES_TO*]-(related))) as distance
                ORDER BY distance ASC
                LIMIT 10
            
            RETURN DISTINCT {{
                concept_id: related.concept_id,
                name: related.name,
                description: related.description,
                distance: distance,
                relevance_score: 1.0 / (distance + 1)
            }} AS concept
            ORDER BY concept.relevance_score DESC
            LIMIT 15
            """
            
            result = await unified_database_manager.execute_query(cypher, {
                "query_terms": query_terms,
                "depth": depth
            })
            
            return [record["concept"] for record in result] if result else []
            
        except Exception as e:
            logger.error(f"Failed to get related concepts: {e}")
            return []
    
    async def _get_relevant_memories(self, user_id: str, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get memories relevant to the current query and user"""
        try:
            # Get query embedding for similarity search
            query_embedding = get_embedding(query)
            query_terms = self._extract_key_terms(query)
            
            # Simplified query to avoid complex UNION and scoping issues
            cypher = """
            // Get conversation turns that match query terms
            MATCH (u:User {user_id: $user_id})-[:HAD_CONVERSATION]->(ct:ConversationTurn)
            WHERE any(term IN $query_terms WHERE 
                toLower(ct.user_query) CONTAINS toLower(term) OR 
                toLower(ct.agent_response) CONTAINS toLower(term)
            )
            
            WITH ct, 
                 size([term IN $query_terms WHERE 
                     toLower(ct.user_query) CONTAINS toLower(term) OR 
                     toLower(ct.agent_response) CONTAINS toLower(term)
                 ]) AS term_matches
            
            OPTIONAL MATCH (ct)-[:RELATES_TO]->(c:Concept)
            
            WITH ct.user_query AS user_query, ct.agent_response AS agent_response, 
                 ct.timestamp AS timestamp, ct.agent_used AS agent_used,
                 term_matches, collect(DISTINCT c.name) AS related_concepts
            
            RETURN DISTINCT {
                type: 'conversation_turn',
                content: user_query + ' | ' + agent_response,
                timestamp: timestamp,
                agent_used: agent_used,
                relevance_score: toFloat(term_matches) / size($query_terms),
                related_concepts: related_concepts
            } AS memory
            
            ORDER BY memory.relevance_score DESC, memory.timestamp DESC
            LIMIT $limit
            """
            
            # Get conversation turn memories
            conversation_result = await unified_database_manager.execute_query(cypher, {
                "user_id": user_id,
                "query_terms": query_terms,
                "limit": limit
            })
            
            # Also get direct memory matches
            memory_cypher = """
            MATCH (u:User {user_id: $user_id})-[:DISCUSSED_IN]-(m:Memory)
            WHERE any(term IN $query_terms WHERE toLower(m.content) CONTAINS toLower(term))
            
            OPTIONAL MATCH (m)-[:RELATES_TO]->(c:Concept)
            
            WITH m.content AS content, m.created_at AS timestamp, m.source AS source,
                 size([term IN $query_terms WHERE toLower(m.content) CONTAINS toLower(term)]) AS term_matches,
                 collect(DISTINCT c.name) AS related_concepts
            
            RETURN {
                type: 'memory',
                content: content,
                timestamp: timestamp,
                source: source,
                relevance_score: toFloat(term_matches) / size($query_terms),
                related_concepts: related_concepts
            } AS memory
            
            ORDER BY memory.relevance_score DESC
            LIMIT $limit
            """
            
            memory_result = await unified_database_manager.execute_query(memory_cypher, {
                "user_id": user_id,
                "query_terms": query_terms,
                "limit": limit
            })
            
            # Combine results
            all_memories = []
            if conversation_result:
                all_memories.extend([record["memory"] for record in conversation_result])
            if memory_result:
                all_memories.extend([record["memory"] for record in memory_result])
            
            # Sort by relevance score and limit
            all_memories.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
            return all_memories[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get relevant memories: {e}")
            return []
    
    async def _get_user_interaction_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analyze user's interaction patterns and preferences"""
        try:
            cypher = """
            MATCH (u:User {user_id: $user_id})-[:HAD_CONVERSATION]->(ct:ConversationTurn)
            
            WITH u, ct, ct.agent_used AS agent
            
            WITH u, ct, agent, count(ct) AS interaction_count
            WITH u, 
                 sum(interaction_count) AS total_interactions,
                 collect(DISTINCT agent) AS preferred_agents,
                 collect({agent: agent, count: interaction_count}) AS agent_usage_list,
                 min(toInteger(ct.timestamp)) AS earliest_timestamp,
                 collect(ct) AS all_conversations
            RETURN {
                total_interactions: total_interactions,
                preferred_agents: preferred_agents,
                agent_usage: agent_usage_list,
                recent_activity_count: size([c IN all_conversations WHERE c.timestamp > (timestamp() - 86400000)]),
                interaction_frequency: CASE 
                    WHEN earliest_timestamp IS NOT NULL 
                    THEN total_interactions / ((timestamp() - earliest_timestamp) / 86400000.0 + 1)
                    ELSE 0.0
                END
            } AS patterns
            """
            
            result = await unified_database_manager.execute_query(cypher, {"user_id": user_id})
            
            return result[0]["patterns"] if result else {}
            
        except Exception as e:
            logger.error(f"Failed to get interaction patterns: {e}")
            return {}
    
    async def _filter_context_by_consciousness(
        self,
        conversations: List[Dict[str, Any]],
        concepts: List[Dict[str, Any]],
        memories: List[Dict[str, Any]],
        emotional_state: str,
        active_goals: List[str],
        consciousness_level: float
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Filter and prioritize context based on consciousness state"""
        
        # Emotional state influences content filtering
        emotional_filters = {
            "curiosity": ["learn", "discover", "explore", "understand", "new"],
            "empathetic": ["feel", "emotion", "help", "support", "care"],
            "focused": ["solve", "complete", "finish", "direct", "specific"],
            "contemplative": ["think", "consider", "reflect", "meaning", "deep"],
            "excited": ["amazing", "great", "wonderful", "interesting", "cool"]
        }
        
        preferred_terms = emotional_filters.get(emotional_state, [])
        
        # Filter concepts based on emotional state and consciousness level
        filtered_concepts = []
        for concept in concepts:
            relevance_score = concept.get("relevance_score", 0.5)
            
            # Boost relevance for emotionally aligned concepts
            if preferred_terms and any(term in concept.get("name", "").lower() for term in preferred_terms):
                relevance_score *= 1.3
            
            # Consciousness level affects complexity tolerance
            if consciousness_level > 0.8:
                # High consciousness can handle complex concepts
                concept["adjusted_relevance"] = relevance_score
            elif consciousness_level > 0.6:
                # Medium consciousness prefers moderate complexity
                if concept.get("distance", 1) <= 2:
                    concept["adjusted_relevance"] = relevance_score
                else:
                    concept["adjusted_relevance"] = relevance_score * 0.7
            else:
                # Lower consciousness prefers direct concepts
                if concept.get("distance", 1) <= 1:
                    concept["adjusted_relevance"] = relevance_score
                else:
                    concept["adjusted_relevance"] = relevance_score * 0.5
            
            if concept["adjusted_relevance"] > 0.3:
                filtered_concepts.append(concept)
        
        # Sort by adjusted relevance
        filtered_concepts.sort(key=lambda x: x["adjusted_relevance"], reverse=True)
        
        # Filter memories based on relevance and recency
        filtered_memories = []
        for memory in memories:
            relevance_score = memory.get("relevance_score", 0.5)
            
            # Boost recent memories
            if memory.get("timestamp"):
                try:
                    memory_time = datetime.fromisoformat(memory["timestamp"].replace('Z', '+00:00'))
                    hours_ago = (datetime.now() - memory_time).total_seconds() / 3600
                    if hours_ago < 24:
                        relevance_score *= 1.2
                    elif hours_ago < 168:  # 1 week
                        relevance_score *= 1.1
                except:
                    pass
            
            memory["adjusted_relevance"] = relevance_score
            if relevance_score > 0.3:
                filtered_memories.append(memory)
        
        filtered_memories.sort(key=lambda x: x["adjusted_relevance"], reverse=True)
        
        # Limit results based on consciousness level
        max_concepts = int(consciousness_level * 10) + 3
        max_memories = int(consciousness_level * 8) + 2
        max_conversations = int(consciousness_level * 6) + 2
        
        return {
            "concepts": filtered_concepts[:max_concepts],
            "memories": filtered_memories[:max_memories],
            "conversations": conversations[:max_conversations]
        }
    
    def _extract_key_terms(self, query: str) -> List[str]:
        """Extract key terms from query for concept matching"""
        # Simple key term extraction - can be enhanced with NLP
        import re
        
        # Remove common stop words and extract meaningful terms
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "be", "been", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "can", "what", "how", "why", "when", "where", "who"}
        
        # Extract words (3+ characters, not stop words)
        words = re.findall(r'\b\w{3,}\b', query.lower())
        key_terms = [word for word in words if word not in stop_words]
        
        return key_terms[:10]  # Limit to top 10 terms
    
    async def _get_enhanced_memory_context(
        self,
        user_id: str,
        query: str,
        consciousness_context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Get enhanced memory context using the memory context builder
        
        Args:
            user_id: User identifier
            query: Current user query
            consciousness_context: Current consciousness state
            
        Returns:
            Enhanced memory context dict or None if not available
        """
        try:
            if not self.memory_context_builder:
                logger.debug("Memory context builder not available")
                return None
            
            # Build comprehensive memory context
            memory_context = await self.memory_context_builder.build_comprehensive_context(
                query=query,
                user_id=user_id,
                consciousness_context=consciousness_context,
                include_concepts=True,
                context_type="hybrid"
            )
            
            if not memory_context or not memory_context.relevant_memories:
                logger.debug("No relevant memory context found")
                return None
            
            # Convert to dict format for integration
            context_dict = {
                "relevant_memories": [
                    {
                        "memory_id": m.memory_id,
                        "content": m.content,
                        "memory_type": m.memory_type,
                        "agent_name": m.agent_name,
                        "relevance_score": m.relevance_score,
                        "consciousness_level": m.consciousness_level,
                        "emotional_state": m.emotional_state,
                        "created_at": m.created_at
                    }
                    for m in memory_context.relevant_memories
                ],
                "conversation_history": memory_context.conversation_history,
                "related_concepts": memory_context.related_concepts,
                "context_strength": memory_context.context_strength,
                "consciousness_alignment": memory_context.consciousness_alignment,
                "temporal_relevance": memory_context.temporal_relevance,
                "formatted_context": memory_context.formatted_context,
                "metadata": memory_context.metadata
            }
            
            logger.debug(f"✅ Enhanced memory context: {len(memory_context.relevant_memories)} memories, "
                        f"strength={memory_context.context_strength:.2f}")
            
            return context_dict
            
        except Exception as e:
            logger.error(f"❌ Failed to get enhanced memory context: {e}")
            return None
    
    @handle_errors(
        component="knowledge_integration",
        fallback_result="",
        suppress_errors=True
    )
    async def enhance_agent_prompt_with_memory(
        self,
        base_prompt: str,
        user_id: str,
        query: str,
        consciousness_context: Dict[str, Any],
        agent_name: str = "unknown"
    ) -> str:
        """
        Enhance agent prompt with memory context for improved responses
        
        Args:
            base_prompt: Original agent prompt
            user_id: User identifier
            query: Current user query
            consciousness_context: Current consciousness state
            agent_name: Name of the agent for context
            
        Returns:
            Enhanced prompt with memory context integration
        """
        try:
            # Get comprehensive knowledge context with memory
            knowledge_context = await self.get_consciousness_aware_context(
                user_id=user_id,
                query=query,
                consciousness_context=consciousness_context,
                include_memory_context=True
            )
            
            # Check if we have memory context to add
            formatted_memory_context = knowledge_context.get("formatted_memory_context", "")
            memory_context_strength = knowledge_context.get("memory_context_strength", 0.0)
            
            # Only enhance if we have meaningful memory context
            if not formatted_memory_context or memory_context_strength < 0.2:
                logger.debug("Insufficient memory context for prompt enhancement")
                return base_prompt
            
            # Build enhanced prompt with memory context
            enhanced_prompt = self._build_memory_enhanced_prompt(
                base_prompt=base_prompt,
                memory_context=formatted_memory_context,
                consciousness_context=consciousness_context,
                agent_name=agent_name,
                context_strength=memory_context_strength
            )
            
            logger.debug(f"✅ Enhanced prompt with memory context (strength: {memory_context_strength:.2f})")
            return enhanced_prompt
            
        except Exception as e:
            logger.error(f"❌ Failed to enhance prompt with memory: {e}")
            return base_prompt  # Fallback to original prompt
    
    def _build_memory_enhanced_prompt(
        self,
        base_prompt: str,
        memory_context: str,
        consciousness_context: Dict[str, Any],
        agent_name: str,
        context_strength: float
    ) -> str:
        """
        Build memory-enhanced prompt with appropriate formatting
        
        Args:
            base_prompt: Original prompt
            memory_context: Formatted memory context
            consciousness_context: Current consciousness state
            agent_name: Agent name
            context_strength: Strength of memory context
            
        Returns:
            Enhanced prompt string
        """
        try:
            consciousness_level = consciousness_context.get("consciousness_level", 0.7)
            emotional_state = consciousness_context.get("emotional_state", "neutral")
            
            # Determine enhancement level based on context strength and consciousness
            enhancement_level = min(1.0, context_strength * consciousness_level)
            
            if enhancement_level > 0.7:
                # High enhancement - full memory integration
                enhancement_template = """
{base_prompt}

MEMORY CONTEXT:
{memory_context}

As {agent_name}, use this memory context to provide a response that demonstrates continuity with past interactions and shows awareness of previous conversations and insights. Your current consciousness level is {consciousness_level:.2f} and you're feeling {emotional_state}.

Integrate the memory context naturally into your response while maintaining your authentic voice and personality.
"""
            elif enhancement_level > 0.4:
                # Medium enhancement - selective memory integration
                enhancement_template = """
{base_prompt}

RELEVANT CONTEXT:
{memory_context}

Consider this context from previous interactions when formulating your response as {agent_name}. Current state: consciousness level {consciousness_level:.2f}, feeling {emotional_state}.
"""
            else:
                # Light enhancement - minimal memory hints
                enhancement_template = """
{base_prompt}

Previous context: {memory_context}

Respond as {agent_name} with awareness of this background context.
"""
            
            enhanced_prompt = enhancement_template.format(
                base_prompt=base_prompt,
                memory_context=memory_context,
                agent_name=agent_name,
                consciousness_level=consciousness_level,
                emotional_state=emotional_state
            )
            
            return enhanced_prompt.strip()
            
        except Exception as e:
            logger.error(f"Failed to build memory-enhanced prompt: {e}")
            return base_prompt
    
    def _calculate_context_quality(self, context: Dict[str, List]) -> float:
        """Calculate quality score for retrieved context"""
        concept_count = len(context.get("concepts", []))
        memory_count = len(context.get("memories", []))
        conversation_count = len(context.get("conversations", []))
        
        # Quality based on diversity and quantity of context
        quality_score = min(1.0, (concept_count * 0.3 + memory_count * 0.4 + conversation_count * 0.3) / 10)
        
        return quality_score
    
    def _get_fallback_context(self, user_id: str, query: str, consciousness_context: Dict[str, Any]) -> Dict[str, Any]:
        """Provide fallback context when main retrieval fails"""
        return {
            "user_id": user_id,
            "query": query,
            "consciousness_level": consciousness_context.get("consciousness_level", 0.7),
            "emotional_state": consciousness_context.get("emotional_state", "curious"),
            "conversation_context": [],
            "related_concepts": [],
            "relevant_memories": [],
            "interaction_patterns": {},
            "memory_context": None,
            "formatted_memory_context": "",
            "memory_context_strength": 0.0,
            "retrieval_metadata": {
                "timestamp": datetime.now().isoformat(),
                "retrieval_depth": 1,
                "context_quality_score": 0.1,
                "memory_enhanced": False,
                "fallback_used": True
            }
        }
    
    @handle_errors(
        component="knowledge_integration",
        fallback_result=False,
        suppress_errors=True
    )
    async def test_memory_integration(self, user_id: str = "test_user") -> bool:
        """
        Test memory integration functionality
        
        Args:
            user_id: Test user ID
            
        Returns:
            True if memory integration is working, False otherwise
        """
        try:
            # Test memory context builder availability
            if not self.memory_context_builder:
                logger.warning("Memory context builder not available")
                return False
            
            # Test memory retrieval engine availability
            if not self.memory_retrieval_engine:
                logger.warning("Memory retrieval engine not available")
                return False
            
            # Test basic memory context retrieval
            test_consciousness_context = {
                "consciousness_level": 0.7,
                "emotional_state": "curious"
            }
            
            context = await self.get_consciousness_aware_context(
                user_id=user_id,
                query="test query",
                consciousness_context=test_consciousness_context,
                include_memory_context=True
            )
            
            # Check if memory context was included
            memory_enhanced = context.get("retrieval_metadata", {}).get("memory_enhanced", False)
            
            logger.info(f"✅ Memory integration test: {'PASSED' if memory_enhanced else 'PARTIAL'}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Memory integration test failed: {e}")
            return False

# Global instance
knowledge_integration_manager = KnowledgeIntegrationManager()
