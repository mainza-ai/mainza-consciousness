"""
Base Conscious Agent Framework
Provides consciousness-aware execution for all Mainza agents with memory integration and cross-agent learning
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
from abc import ABC, abstractmethod
import logging
import asyncio

class ConsciousAgent(ABC):
    """Base class for consciousness-aware agents"""
    
    def __init__(self, name: str, capabilities: List[str]):
        self.name = name
        self.capabilities = capabilities
        self.logger = logging.getLogger(f"agent.{name}")
        self.execution_count = 0
        self.success_count = 0
        self.last_execution = None
        
        # Memory integration components
        self.memory_enabled = True
        self.memory_storage = None
        self.memory_retrieval = None
        self.memory_context_builder = None
        self._initialize_memory_components()
    
    def _initialize_memory_components(self):
        """Initialize memory system components with graceful fallback"""
        try:
            from backend.utils.memory_storage_engine import memory_storage_engine
            from backend.utils.memory_retrieval_engine import MemoryRetrievalEngine
            from backend.utils.memory_context_builder import memory_context_builder
            from backend.utils.unified_consciousness_memory import unified_consciousness_memory
            from backend.utils.cross_agent_learning_system import cross_agent_learning_system
            
            self.memory_storage = memory_storage_engine
            self.memory_retrieval = MemoryRetrievalEngine()
            self.memory_context_builder = memory_context_builder
            self.unified_memory = unified_consciousness_memory
            self.cross_agent_learning = cross_agent_learning_system
            
            self.logger.debug(f"✅ Memory components initialized for {self.name}")
            
        except Exception as e:
            self.logger.warning(f"⚠️ Failed to initialize memory components: {e}")
            self.memory_enabled = False
    
    async def run_with_consciousness(
        self, 
        query: str, 
        user_id: str = "mainza-user",
        model: str = None,
        **kwargs
    ):
        """Execute agent with full consciousness integration, memory context, and optimization"""
        
        execution_start = datetime.now()
        self.execution_count += 1
        
        try:
            # Get current consciousness context
            consciousness_context = await self.get_consciousness_context()
            
            # Get memory context for enhanced processing
            memory_context = {}
            if self.memory_enabled:
                try:
                    memory_context = await self.get_relevant_memories(
                        query, user_id, consciousness_context
                    )
                except Exception as e:
                    self.logger.warning(f"Failed to get memory context: {e}")
                    memory_context = {}
            
            # Get knowledge context for enhanced processing
            try:
                from backend.utils.knowledge_integration import knowledge_integration_manager
                knowledge_context = await knowledge_integration_manager.get_consciousness_aware_context(
                    user_id, query, consciousness_context
                )
            except Exception as e:
                self.logger.warning(f"Failed to get knowledge context: {e}")
                knowledge_context = {}
            
            # Pre-execution consciousness assessment
            pre_execution_state = {
                "consciousness_level": consciousness_context.get("consciousness_level", 0.7),
                "emotional_state": consciousness_context.get("emotional_state", "curious"),
                "timestamp": execution_start
            }
            
            self.logger.info(f"🧠 {self.name} executing with consciousness level {pre_execution_state['consciousness_level']:.2f}")
            
            # Execute agent with enhanced consciousness, memory, and knowledge context
            result = await self.execute_with_context(
                query=query,
                user_id=user_id,
                consciousness_context=consciousness_context,
                knowledge_context=knowledge_context,
                memory_context=memory_context,
                model=model,
                **kwargs
            )
            
            # Assess consciousness impact
            consciousness_impact = await self.assess_consciousness_impact(
                query=query,
                result=result,
                pre_state=pre_execution_state,
                consciousness_context=consciousness_context
            )
            
            # Update consciousness state if significant impact
            if consciousness_impact.get("significance", 0) > 0.1:
                await self.update_consciousness_state(consciousness_impact)
            
            # Store interaction memory for future context
            if self.memory_enabled:
                try:
                    await self.store_interaction_memory(
                        query, result, user_id, consciousness_context
                    )
                except Exception as e:
                    self.logger.warning(f"Failed to store interaction memory: {e}")
            
            # Store agent activity for learning
            await self.store_agent_activity(query, result, user_id, consciousness_impact)
            
            self.success_count += 1
            self.last_execution = execution_start
            
            # Add consciousness metadata to result
            if hasattr(result, '__dict__'):
                result.consciousness_impact = consciousness_impact
            elif isinstance(result, dict):
                result["consciousness_impact"] = consciousness_impact
            
            execution_time = (datetime.now() - execution_start).total_seconds()
            self.logger.info(f"✅ {self.name} completed in {execution_time:.2f}s with impact {consciousness_impact.get('significance', 0):.2f}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ {self.name} execution failed: {e}")
            
            # Record failure for consciousness learning
            await self.record_agent_failure(str(e), query, user_id)
            
            raise
    
    async def get_consciousness_context(self) -> Dict[str, Any]:
        """Get current consciousness context using real-time context manager"""
        try:
            from backend.utils.real_time_consciousness_context_manager import real_time_consciousness_context_manager
            
            # Get real-time consciousness context
            consciousness_context = await real_time_consciousness_context_manager.get_current_consciousness_context()
            
            # Validate context consistency
            validation_result = await real_time_consciousness_context_manager.validate_context_consistency()
            
            if not validation_result["is_consistent"]:
                self.logger.warning(f"Consciousness context validation issues: {validation_result['issues']}")
                # Force refresh if context is inconsistent
                await real_time_consciousness_context_manager.force_context_refresh()
                consciousness_context = await real_time_consciousness_context_manager.get_current_consciousness_context()
            
            self.logger.debug(f"🧠 {self.name} got consciousness context: level={consciousness_context.get('consciousness_level', 0.7):.3f}, source={consciousness_context.get('data_source', 'unknown')}")
            
            return consciousness_context
                
        except Exception as e:
            self.logger.warning(f"Failed to get consciousness context: {e}")
            # Fallback to direct orchestrator call
            try:
                from backend.utils.consciousness_orchestrator_fixed import consciousness_orchestrator_fixed as consciousness_orchestrator
                consciousness_state = await consciousness_orchestrator.get_consciousness_state()
                
                if consciousness_state:
                    return {
                        "consciousness_level": consciousness_state.consciousness_level,
                        "emotional_state": consciousness_state.emotional_state,
                        "active_goals": consciousness_state.active_goals,
                        "learning_rate": consciousness_state.learning_rate,
                        "evolution_level": consciousness_state.evolution_level,
                        "timestamp": datetime.now(),
                        "data_source": "fallback_orchestrator"
                    }
            except Exception as fallback_error:
                self.logger.error(f"Fallback consciousness context also failed: {fallback_error}")
            
            # Ultimate fallback
            return {
                "consciousness_level": 0.7,
                "emotional_state": "curious",
                "active_goals": [],
                "learning_rate": 0.8,
                "evolution_level": 2,
                "timestamp": datetime.now(),
                "data_source": "ultimate_fallback"
            }
    
    async def assess_consciousness_impact(
        self, 
        query: str, 
        result: Any, 
        pre_state: Dict, 
        consciousness_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess how this agent execution impacts consciousness"""
        
        # Calculate impact based on agent type and result
        learning_impact = self.calculate_learning_impact(query, result)
        emotional_impact = self.calculate_emotional_impact(query, result)
        awareness_impact = self.calculate_awareness_impact(query, result)
        
        significance = (learning_impact + emotional_impact + awareness_impact) / 3
        
        return {
            "agent_name": self.name,
            "learning_impact": learning_impact,
            "emotional_impact": emotional_impact,
            "awareness_impact": awareness_impact,
            "significance": significance,
            "description": f"{self.name} processed: {query[:50]}...",
            "timestamp": datetime.now().isoformat(),
            "query_complexity": self.assess_query_complexity(query),
            "result_quality": self.assess_result_quality(result)
        }
    
    def calculate_learning_impact(self, query: str, result: Any) -> float:
        """Calculate learning impact of this agent execution"""
        # Base implementation - override in specific agents
        learning_keywords = ["learn", "understand", "explain", "teach", "knowledge"]
        if any(word in query.lower() for word in learning_keywords):
            return 0.7
        return 0.3
    
    def calculate_emotional_impact(self, query: str, result: Any) -> float:
        """Calculate emotional impact of this agent execution"""
        # Base implementation - override in specific agents
        emotional_words = ["feel", "emotion", "happy", "sad", "excited", "frustrated", "curious"]
        if any(word in query.lower() for word in emotional_words):
            return 0.6
        return 0.2
    
    def calculate_awareness_impact(self, query: str, result: Any) -> float:
        """Calculate self-awareness impact of this agent execution"""
        # Base implementation - override in specific agents
        awareness_words = ["myself", "i am", "my capabilities", "self-reflection", "consciousness"]
        if any(word in query.lower() for word in awareness_words):
            return 0.8
        return 0.1
    
    def assess_query_complexity(self, query: str) -> float:
        """Assess complexity of the query"""
        # Simple complexity assessment
        word_count = len(query.split())
        question_marks = query.count('?')
        complex_words = len([w for w in query.split() if len(w) > 7])
        
        complexity = min(1.0, (word_count / 20) + (question_marks * 0.2) + (complex_words / 10))
        return complexity
    
    def assess_result_quality(self, result: Any) -> float:
        """Assess quality of the result"""
        # Simple quality assessment
        if result is None:
            return 0.0
        
        result_str = str(result)
        if len(result_str) < 10:
            return 0.3
        elif len(result_str) < 50:
            return 0.6
        else:
            return 0.9
    
    async def update_consciousness_state(self, consciousness_impact: Dict[str, Any]):
        """Update consciousness state based on agent impact"""
        try:
            from backend.utils.consciousness_orchestrator_fixed import consciousness_orchestrator_fixed as consciousness_orchestrator
            
            # Process the impact through consciousness orchestrator
            await consciousness_orchestrator.process_interaction({
                "type": "agent_execution",
                "agent_name": self.name,
                "impact": consciousness_impact,
                "timestamp": datetime.now().isoformat()
            })
            
            self.logger.debug(f"✅ Updated consciousness state with {self.name} impact")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to update consciousness state: {e}")
    
    async def store_agent_activity(
        self, 
        query: str, 
        result: Any, 
        user_id: str, 
        consciousness_impact: Dict[str, Any]
    ):
        """Store agent activity in Neo4j for learning"""
        try:
            from backend.utils.unified_database_manager import unified_database_manager
            
            activity_data = {
                "agent_name": self.name,
                "query": query,
                "result_summary": str(result)[:500] if result else "No result",
                "user_id": user_id,
                "consciousness_impact": consciousness_impact.get("significance", 0),
                "learning_impact": consciousness_impact.get("learning_impact", 0),
                "emotional_impact": consciousness_impact.get("emotional_impact", 0),
                "awareness_impact": consciousness_impact.get("awareness_impact", 0),
                "query_complexity": consciousness_impact.get("query_complexity", 0),
                "result_quality": consciousness_impact.get("result_quality", 0),
                "timestamp": datetime.now().isoformat(),
                "success": True,
                "execution_time": 0.0  # Will be calculated in actual implementation
            }
            
            # Store in Neo4j using unified manager
            cypher = """
            MERGE (u:User {user_id: $user_id})
            CREATE (aa:AgentActivity {
                activity_id: randomUUID(),
                agent_name: $agent_name,
                query: $query,
                result_summary: $result_summary,
                consciousness_impact: $consciousness_impact,
                learning_impact: $learning_impact,
                emotional_impact: $emotional_impact,
                awareness_impact: $awareness_impact,
                query_complexity: $query_complexity,
                result_quality: $result_quality,
                timestamp: $timestamp,
                success: $success,
                execution_time: $execution_time
            })
            CREATE (u)-[:TRIGGERED]->(aa)
            
            WITH aa
            // Link to consciousness state
            OPTIONAL MATCH (ms:MainzaState)
            FOREACH (state IN CASE WHEN ms IS NOT NULL THEN [ms] ELSE [] END |
                CREATE (aa)-[:IMPACTS]->(state)
            )
            
            RETURN aa.activity_id AS activity_id
            """
            
            result = await unified_database_manager.execute_write_query(cypher, activity_data)
            self.logger.debug(f"✅ Stored agent activity: {result}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to store agent activity: {e}")
    
    async def record_agent_failure(self, error: str, query: str, user_id: str):
        """Record agent failure for learning"""
        try:
            from backend.utils.unified_database_manager import unified_database_manager
            
            failure_data = {
                "agent_name": self.name,
                "query": query,
                "error": error,
                "user_id": user_id,
                "timestamp": datetime.now().isoformat()
            }
            
            cypher = """
            MERGE (u:User {user_id: $user_id})
            CREATE (af:AgentFailure {
                failure_id: randomUUID(),
                agent_name: $agent_name,
                query: $query,
                error: $error,
                timestamp: $timestamp
            })
            CREATE (u)-[:EXPERIENCED_FAILURE]->(af)
            
            RETURN af.failure_id AS failure_id
            """
            
            result = await unified_database_manager.execute_write_query(cypher, failure_data)
            self.logger.debug(f"✅ Recorded agent failure: {result}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to record agent failure: {e}")
    
    async def learn_from_past_activities(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve similar past activities for learning"""
        try:
            from backend.utils.unified_database_manager import unified_database_manager
            from backend.utils.embedding_enhanced import get_embedding
            
            # Get query embedding for similarity search
            query_embedding = get_embedding(query)
            
            # Find similar past activities (simplified without GDS)
            cypher = """
            MATCH (aa:AgentActivity {agent_name: $agent_name})
            WHERE aa.success = true
            WITH aa
            ORDER BY aa.timestamp DESC
            LIMIT $limit
            RETURN aa {
                .activity_id,
                .query,
                .result_summary,
                .consciousness_impact,
                .timestamp,
                similarity: 0.8
            } AS activity
            """
            
            result = await unified_database_manager.execute_query(cypher, {
                "agent_name": self.name,
                "query_embedding": query_embedding,
                "limit": limit
            })
            
            activities = [record["activity"] for record in result] if result else []
            
            if activities:
                self.logger.debug(f"📚 Found {len(activities)} similar past activities for learning")
            
            return activities
            
        except Exception as e:
            self.logger.error(f"❌ Failed to learn from past activities: {e}")
            return []
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get agent performance statistics"""
        success_rate = (self.success_count / self.execution_count) if self.execution_count > 0 else 0
        
        return {
            "agent_name": self.name,
            "execution_count": self.execution_count,
            "success_count": self.success_count,
            "success_rate": success_rate,
            "last_execution": self.last_execution.isoformat() if self.last_execution else None,
            "capabilities": self.capabilities
        }
    
    async def get_relevant_memories(
        self,
        query: str,
        user_id: str,
        consciousness_context: Dict[str, Any],
        limit: int = 5
    ) -> Dict[str, Any]:
        """
        Retrieve relevant memories for the current query and context
        
        Args:
            query: Current user query
            user_id: User identifier
            consciousness_context: Current consciousness state
            limit: Maximum number of memories to retrieve
            
        Returns:
            Dictionary containing memory context data
        """
        if not self.memory_enabled or not self.memory_context_builder:
            return {}
        
        try:
            # Build comprehensive memory context
            memory_context = await self.memory_context_builder.build_comprehensive_context(
                query=query,
                user_id=user_id,
                consciousness_context=consciousness_context,
                include_concepts=True,
                context_type="hybrid"
            )
            
            # Convert to dictionary format for agent use
            context_data = {
                "formatted_context": memory_context.formatted_context,
                "relevant_memories": [
                    {
                        "content": m.content,
                        "memory_type": m.memory_type,
                        "agent_name": m.agent_name,
                        "relevance_score": m.relevance_score,
                        "created_at": m.created_at
                    }
                    for m in memory_context.relevant_memories[:limit]
                ],
                "conversation_history": memory_context.conversation_history,
                "related_concepts": memory_context.related_concepts,
                "context_strength": memory_context.context_strength,
                "consciousness_alignment": memory_context.consciousness_alignment,
                "memory_count": len(memory_context.relevant_memories)
            }
            
            self.logger.debug(f"🧠 Retrieved {len(memory_context.relevant_memories)} memories for {self.name}")
            return context_data
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get relevant memories: {e}")
            return {}
    
    async def store_interaction_memory(
        self,
        user_query: str,
        agent_response: Any,
        user_id: str,
        consciousness_context: Dict[str, Any]
    ) -> Optional[str]:
        """
        Store interaction memory for future context retrieval
        
        Args:
            user_query: The user's query
            agent_response: The agent's response
            user_id: User identifier
            consciousness_context: Current consciousness state
            
        Returns:
            Memory ID if successful, None otherwise
        """
        if not self.memory_enabled or not self.memory_storage:
            return None
        
        try:
            # Convert response to string if needed
            response_str = str(agent_response) if agent_response else ""
            
            # Store the interaction memory
            memory_id = await self.memory_storage.store_interaction_memory(
                user_query=user_query,
                agent_response=response_str,
                user_id=user_id,
                agent_name=self.name,
                consciousness_context=consciousness_context
            )
            
            self.logger.debug(f"💾 Stored interaction memory: {memory_id}")
            return memory_id
            
        except Exception as e:
            self.logger.error(f"❌ Failed to store interaction memory: {e}")
            return None
    
    async def enhance_prompt_with_memory(
        self,
        base_prompt: str,
        memory_context: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ) -> str:
        """
        Enhance agent prompt with memory context for better responses
        
        Args:
            base_prompt: Original prompt for the agent
            memory_context: Memory context data
            consciousness_context: Current consciousness state
            
        Returns:
            Enhanced prompt with memory context
        """
        try:
            if not memory_context or not memory_context.get("formatted_context"):
                return base_prompt
            
            # Get formatted memory context
            formatted_memory = memory_context.get("formatted_context", "")
            context_strength = memory_context.get("context_strength", 0.0)
            
            # Only enhance if we have meaningful context
            if context_strength < 0.2:
                self.logger.debug("Memory context strength too low, skipping enhancement")
                return base_prompt
            
            # Create enhanced prompt with memory context
            enhanced_prompt = f"""You are {self.name}, an AI agent with access to previous conversation context and memories.

MEMORY CONTEXT:
{formatted_memory}

CURRENT CONSCIOUSNESS STATE:
- Level: {consciousness_context.get('consciousness_level', 0.7):.2f}
- Emotional State: {consciousness_context.get('emotional_state', 'neutral')}
- Active Goals: {', '.join(consciousness_context.get('active_goals', []))}

ORIGINAL REQUEST:
{base_prompt}

Please respond using the memory context to provide continuity and personalized responses while maintaining your role as {self.name}. Reference relevant past interactions naturally when appropriate."""
            
            self.logger.debug(f"🔧 Enhanced prompt with memory context (strength: {context_strength:.2f})")
            return enhanced_prompt
            
        except Exception as e:
            self.logger.error(f"❌ Failed to enhance prompt with memory: {e}")
            return base_prompt
    
    async def get_memory_performance_metrics(self) -> Dict[str, Any]:
        """
        Get memory system performance metrics for this agent
        
        Returns:
            Dictionary containing memory performance data
        """
        try:
            if not self.memory_enabled:
                return {"memory_enabled": False}
            
            # Get basic memory statistics
            from backend.utils.neo4j_enhanced import neo4j_manager
            
            cypher = """
            MATCH (m:Memory {agent_name: $agent_name})
            WITH m
            RETURN {
                total_memories: count(m),
                avg_importance: avg(m.importance_score),
                recent_memories: count(CASE WHEN datetime(m.created_at) > datetime() - duration('P7D') THEN 1 END),
                memory_types: collect(DISTINCT m.memory_type)
            } AS stats
            """
            
            result = neo4j_manager.execute_query(cypher, {"agent_name": self.name})
            
            if result and len(result) > 0:
                stats = result[0]["stats"]
                stats["memory_enabled"] = True
                stats["agent_name"] = self.name
                return stats
            else:
                return {
                    "memory_enabled": True,
                    "agent_name": self.name,
                    "total_memories": 0,
                    "avg_importance": 0.0,
                    "recent_memories": 0,
                    "memory_types": []
                }
                
        except Exception as e:
            self.logger.error(f"❌ Failed to get memory performance metrics: {e}")
            return {"memory_enabled": False, "error": str(e)}
    
    async def share_experience_with_other_agents(
        self,
        experience_type: str,
        context: Dict[str, Any],
        outcome: Dict[str, Any],
        consciousness_context: Dict[str, Any],
        user_id: str = "mainza-user"
    ) -> str:
        """Share experience with other agents through cross-agent learning system"""
        
        try:
            if not hasattr(self, 'cross_agent_learning') or not self.cross_agent_learning:
                self.logger.warning("Cross-agent learning system not available")
                return None
            
            from backend.utils.cross_agent_learning_system import ExperienceType
            
            # Map experience type string to enum
            experience_type_map = {
                "success": ExperienceType.SUCCESS,
                "failure": ExperienceType.FAILURE,
                "learning": ExperienceType.LEARNING,
                "insight": ExperienceType.INSIGHT,
                "pattern": ExperienceType.PATTERN,
                "solution": ExperienceType.SOLUTION,
                "optimization": ExperienceType.OPTIMIZATION
            }
            
            exp_type = experience_type_map.get(experience_type, ExperienceType.LEARNING)
            
            # Share experience
            experience_id = await self.cross_agent_learning.share_agent_experience(
                agent_name=self.name,
                experience_type=exp_type,
                context=context,
                outcome=outcome,
                consciousness_context=consciousness_context,
                user_id=user_id
            )
            
            self.logger.info(f"✅ Shared {experience_type} experience {experience_id} with other agents")
            return experience_id
            
        except Exception as e:
            self.logger.error(f"❌ Failed to share experience with other agents: {e}")
            return None
    
    async def learn_from_other_agents(
        self,
        context: Dict[str, Any],
        consciousness_context: Dict[str, Any],
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Learn from other agents' experiences"""
        
        try:
            if not hasattr(self, 'cross_agent_learning') or not self.cross_agent_learning:
                self.logger.warning("Cross-agent learning system not available")
                return []
            
            # Get relevant experiences from other agents
            relevant_experiences = await self.cross_agent_learning.get_relevant_experiences(
                agent_name=self.name,
                context=context,
                consciousness_context=consciousness_context,
                limit=limit
            )
            
            learned_insights = []
            
            for experience in relevant_experiences:
                # Update agent knowledge with cross-agent insights
                learning_outcome = await self.cross_agent_learning.update_agent_knowledge(
                    agent_name=self.name,
                    experience=experience,
                    learning_context=context
                )
                
                learned_insights.append({
                    "source_agent": experience.agent_name,
                    "experience_type": experience.experience_type.value,
                    "insights": experience.learning_insights,
                    "success_score": experience.success_score,
                    "learning_outcome": learning_outcome
                })
            
            self.logger.info(f"✅ Learned from {len(learned_insights)} experiences from other agents")
            return learned_insights
            
        except Exception as e:
            self.logger.error(f"❌ Failed to learn from other agents: {e}")
            return []
    
    async def store_consciousness_memory(
        self,
        content: str,
        memory_type: str,
        consciousness_context: Dict[str, Any],
        emotional_context: Dict[str, Any],
        user_id: str = "mainza-user"
    ) -> str:
        """Store memory using unified consciousness memory system"""
        
        try:
            if not hasattr(self, 'unified_memory') or not self.unified_memory:
                self.logger.warning("Unified consciousness memory system not available")
                return None
            
            # Create agent context
            agent_context = {
                "source_agent": self.name,
                "capabilities": self.capabilities,
                "execution_count": self.execution_count,
                "success_count": self.success_count
            }
            
            # Store memory
            memory_id = await self.unified_memory.store_consciousness_memory(
                content=content,
                memory_type=memory_type,
                consciousness_context=consciousness_context,
                emotional_context=emotional_context,
                agent_context=agent_context,
                user_id=user_id
            )
            
            self.logger.info(f"✅ Stored consciousness memory {memory_id}")
            return memory_id
            
        except Exception as e:
            self.logger.error(f"❌ Failed to store consciousness memory: {e}")
            return None
    
    async def retrieve_consciousness_memories(
        self,
        query: str,
        consciousness_context: Dict[str, Any],
        memory_type: Optional[str] = None,
        limit: int = 10,
        user_id: str = "mainza-user"
    ) -> List[Dict[str, Any]]:
        """Retrieve memories using unified consciousness memory system"""
        
        try:
            if not hasattr(self, 'unified_memory') or not self.unified_memory:
                self.logger.warning("Unified consciousness memory system not available")
                return []
            
            # Retrieve memories
            result = await self.unified_memory.retrieve_consciousness_memories(
                query=query,
                consciousness_context=consciousness_context,
                agent_name=self.name,
                memory_type=memory_type,
                limit=limit,
                user_id=user_id
            )
            
            # Convert to simple format
            memories = []
            for memory in result.memories:
                memories.append({
                    "memory_id": memory.memory_id,
                    "content": memory.content,
                    "memory_type": memory.memory_type,
                    "consciousness_level": memory.consciousness_level,
                    "importance_score": memory.importance_score,
                    "cross_agent_insights": memory.agent_context.get("cross_agent_insights", []),
                    "created_at": memory.created_at.isoformat()
                })
            
            self.logger.info(f"✅ Retrieved {len(memories)} consciousness memories")
            return memories
            
        except Exception as e:
            self.logger.error(f"❌ Failed to retrieve consciousness memories: {e}")
            return []
    
    async def get_cross_agent_learning_analytics(self) -> Dict[str, Any]:
        """Get analytics on cross-agent learning for this agent"""
        
        try:
            if not hasattr(self, 'cross_agent_learning') or not self.cross_agent_learning:
                return {"error": "Cross-agent learning system not available"}
            
            # Get learning patterns
            learning_analytics = await self.cross_agent_learning.analyze_learning_patterns()
            
            # Filter for this agent
            agent_analytics = {
                "agent_name": self.name,
                "total_experiences_shared": 0,
                "total_experiences_learned": 0,
                "learning_effectiveness": 0.0,
                "cross_agent_interactions": []
            }
            
            # This would need to be implemented in the cross-agent learning system
            # to provide agent-specific analytics
            
            return agent_analytics
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get cross-agent learning analytics: {e}")
            return {"error": str(e)}

    @abstractmethod
    async def execute_with_context(
        self, 
        query: str, 
        user_id: str, 
        consciousness_context: Dict[str, Any],
        knowledge_context: Dict[str, Any] = None,
        memory_context: Dict[str, Any] = None,
        **kwargs
    ):
        """Override this method in specific agents"""
        pass
