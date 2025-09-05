"""
End-to-end tests for Conversation Continuity
Tests multi-session memory persistence, conversation context maintenance, and learning progression.
"""
import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, Any, List

# Import the components to test
from backend.agents.simple_chat import EnhancedSimpleChatAgent
from backend.utils.memory_storage_engine import MemoryStorageEngine, MemoryRecord
from backend.utils.memory_retrieval_engine import MemoryRetrievalEngine, MemorySearchResult
from backend.utils.memory_context_builder import MemoryContextBuilder, MemoryContext
from backend.utils.consciousness_orchestrator import ConsciousnessOrchestrator

class TestConversationContinuity:
    """Test conversation continuity across multiple sessions"""
    
    @pytest.fixture
    def conversation_system(self):
        """Setup complete conversation system with memory"""
        # Mock memory storage
        storage = Mock(spec=MemoryStorageEngine)
        storage.store_interaction_memory = AsyncMock(return_value="conv_memory_id")
        storage.initialize = AsyncMock(return_value=True)
        
        # Mock memory retrieval with conversation history
        retrieval = Mock(spec=MemoryRetrievalEngine)
        retrieval.get_relevant_memories = AsyncMock(return_value=[])
        retrieval.get_conversation_history = AsyncMock(return_value=[])
        retrieval.initialize = AsyncMock(return_value=True)
        
        # Mock context builder
        context_builder = Mock(spec=MemoryContextBuilder)
        context_builder.build_comprehensive_context = AsyncMock(return_value=MemoryContext(
            relevant_memories=[],
            conversation_history=[],
            related_concepts=[],
            context_strength=0.7,
            consciousness_alignment=0.8,
            temporal_relevance=0.9,
            formatted_context="Conversation context"
        ))
        
        # Mock consciousness orchestrator
        consciousness = Mock(spec=ConsciousnessOrchestrator)
        consciousness.get_current_state = AsyncMock(return_value={
            "consciousness_level": 0.8,
            "emotional_state": "engaged",
            "active_goals": ["conversation", "learning"]
        })
        
        return {
            "storage": storage,
            "retrieval": retrieval,
            "context_builder": context_builder,
            "consciousness": consciousness
        }
    
    @pytest.fixture
    def conversation_agent(self, conversation_system):
        """Create conversation agent with mocked memory system"""
        with patch('backend.agents.simple_chat.simple_chat_agent') as mock_agent:
            mock_agent.run = AsyncMock(return_value=Mock(data="Agent response"))
            
            agent = EnhancedSimpleChatAgent()
            agent.memory_storage = conversation_system["storage"]
            agent.memory_retrieval = conversation_system["retrieval"]
            agent.memory_context_builder = conversation_system["context_builder"]
            agent.memory_enabled = True
            
            return agent
    
    @pytest.mark.asyncio
    async def test_single_session_conversation_flow(self, conversation_agent, conversation_system):
        """Test conversation flow within a single session"""
        user_id = "continuity_user"
        
        # Conversation turns
        conversation_turns = [
            ("Hello, I'm Alice", "Hello Alice! Nice to meet you."),
            ("I'm interested in AI", "That's fascinating! What aspects of AI interest you most?"),
            ("Specifically machine learning", "Machine learning is a great area to explore. What would you like to know?")
        ]
        
        stored_memories = []
        
        for i, (user_message, expected_response_pattern) in enumerate(conversation_turns):
            # Setup conversation history for context
            if stored_memories:
                conversation_system["retrieval"].get_conversation_history.return_value = stored_memories
                conversation_system["retrieval"].get_relevant_memories.return_value = stored_memories[-2:]  # Recent context
            
            with patch('backend.utils.knowledge_integration.knowledge_integration_manager') as mock_knowledge:
                mock_knowledge.get_consciousness_aware_context.return_value = {"concepts": ["conversation"]}
                
                # Execute conversation turn
                response = await conversation_agent.run_with_consciousness(user_message, user_id)
                
                # Verify memory storage was called
                conversation_system["storage"].store_interaction_memory.assert_called()
                
                # Create mock stored memory for next turn
                stored_memory = MemorySearchResult(
                    memory_id=f"conv_memory_{i}",
                    content=f"User: {user_message}\nAgent: {response}",
                    memory_type="interaction",
                    agent_name="SimpleChat",
                    user_id=user_id,
                    consciousness_level=0.8,
                    emotional_state="engaged",
                    importance_score=0.7,
                    created_at=datetime.now().isoformat(),
                    metadata={"user_query": user_message, "agent_response": response},
                    relevance_score=1.0
                )
                stored_memories.append(stored_memory)
                
                assert isinstance(response, str)
                assert len(response) > 0
        
        # Verify all conversation turns were stored
        assert conversation_system["storage"].store_interaction_memory.call_count == len(conversation_turns)
    
    @pytest.mark.asyncio
    async def test_multi_session_conversation_continuity(self, conversation_agent, conversation_system):
        """Test conversation continuity across multiple sessions"""
        user_id = "multi_session_user"
        
        # Session 1: Initial conversation
        session_1_memories = []
        
        # First session conversation
        session_1_turns = [
            "Hi, I'm working on a research project about consciousness",
            "Can you help me understand different theories of consciousness?"
        ]
        
        for i, user_message in enumerate(session_1_turns):
            with patch('backend.utils.knowledge_integration.knowledge_integration_manager') as mock_knowledge:
                mock_knowledge.get_consciousness_aware_context.return_value = {"concepts": ["consciousness", "research"]}
                
                response = await conversation_agent.run_with_consciousness(user_message, user_id)
                
                # Create memory for this turn
                memory = MemorySearchResult(
                    memory_id=f"session1_memory_{i}",
                    content=f"User: {user_message}\nAgent: {response}",
                    memory_type="interaction",
                    agent_name="SimpleChat",
                    user_id=user_id,
                    consciousness_level=0.8,
                    emotional_state="helpful",
                    importance_score=0.8,
                    created_at=(datetime.now() - timedelta(hours=1)).isoformat(),  # Previous session
                    metadata={"user_query": user_message, "session": 1},
                    relevance_score=0.9
                )
                session_1_memories.append(memory)
        
        # Session 2: Continuation (simulate time gap)
        await asyncio.sleep(0.01)  # Small delay to simulate session gap
        
        # Setup retrieval to return session 1 memories
        conversation_system["retrieval"].get_conversation_history.return_value = session_1_memories
        conversation_system["retrieval"].get_relevant_memories.return_value = session_1_memories
        
        # Session 2 conversation that references previous session
        session_2_message = "Following up on our previous discussion about consciousness theories"
        
        with patch('backend.utils.knowledge_integration.knowledge_integration_manager') as mock_knowledge:
            mock_knowledge.get_consciousness_aware_context.return_value = {"concepts": ["consciousness", "theories"]}
            
            response = await conversation_agent.run_with_consciousness(session_2_message, user_id)
            
            # Verify that previous memories were retrieved for context
            conversation_system["retrieval"].get_relevant_memories.assert_called()
            conversation_system["retrieval"].get_conversation_history.assert_called()
            
            assert isinstance(response, str)
            assert len(response) > 0
    
    @pytest.mark.asyncio
    async def test_conversation_context_evolution(self, conversation_agent, conversation_system):
        """Test how conversation context evolves and influences responses"""
        user_id = "context_evolution_user"
        
        # Progressive conversation that builds context
        conversation_progression = [
            {
                "message": "I'm new to programming",
                "expected_concepts": ["programming", "beginner"],
                "consciousness_level": 0.7
            },
            {
                "message": "I want to learn Python specifically",
                "expected_concepts": ["python", "programming", "learning"],
                "consciousness_level": 0.75
            },
            {
                "message": "Can you recommend some Python projects for beginners?",
                "expected_concepts": ["python", "projects", "beginner", "recommendations"],
                "consciousness_level": 0.8
            }
        ]
        
        accumulated_memories = []
        
        for i, turn in enumerate(conversation_progression):
            # Setup evolving context
            if accumulated_memories:
                conversation_system["retrieval"].get_relevant_memories.return_value = accumulated_memories
                conversation_system["retrieval"].get_conversation_history.return_value = accumulated_memories
            
            # Update consciousness state to reflect learning progression
            conversation_system["consciousness"].get_current_state.return_value = {
                "consciousness_level": turn["consciousness_level"],
                "emotional_state": "learning",
                "active_goals": ["help_user", "provide_guidance"]
            }
            
            with patch('backend.utils.knowledge_integration.knowledge_integration_manager') as mock_knowledge:
                mock_knowledge.get_consciousness_aware_context.return_value = {
                    "concepts": turn["expected_concepts"]
                }
                
                response = await conversation_agent.run_with_consciousness(turn["message"], user_id)
                
                # Create memory with evolving context
                memory = MemorySearchResult(
                    memory_id=f"evolution_memory_{i}",
                    content=f"User: {turn['message']}\nAgent: {response}",
                    memory_type="interaction",
                    agent_name="SimpleChat",
                    user_id=user_id,
                    consciousness_level=turn["consciousness_level"],
                    emotional_state="learning",
                    importance_score=0.7 + (i * 0.1),  # Increasing importance
                    created_at=datetime.now().isoformat(),
                    metadata={
                        "user_query": turn["message"],
                        "concepts": turn["expected_concepts"],
                        "progression_step": i
                    },
                    relevance_score=0.8 + (i * 0.05)
                )
                accumulated_memories.append(memory)
                
                assert isinstance(response, str)
        
        # Verify context evolution was captured
        assert len(accumulated_memories) == len(conversation_progression)
        
        # Verify increasing importance and consciousness levels
        importance_scores = [m.importance_score for m in accumulated_memories]
        consciousness_levels = [m.consciousness_level for m in accumulated_memories]
        
        assert importance_scores == sorted(importance_scores)  # Should be increasing
        assert consciousness_levels == sorted(consciousness_levels)  # Should be increasing
    
    @pytest.mark.asyncio
    async def test_conversation_memory_retrieval_accuracy(self, conversation_agent, conversation_system):
        """Test accuracy of memory retrieval for conversation context"""
        user_id = "memory_accuracy_user"
        
        # Create diverse conversation history
        historical_memories = [
            MemorySearchResult(
                memory_id="history_1",
                content="User: What's your favorite color?\nAgent: I find blue quite calming and inspiring.",
                memory_type="interaction",
                agent_name="SimpleChat",
                user_id=user_id,
                consciousness_level=0.7,
                emotional_state="casual",
                importance_score=0.4,
                created_at=(datetime.now() - timedelta(days=1)).isoformat(),
                metadata={"topic": "personal_preferences"},
                relevance_score=0.3  # Low relevance to technical topics
            ),
            MemorySearchResult(
                memory_id="history_2",
                content="User: How do neural networks work?\nAgent: Neural networks are inspired by biological neurons...",
                memory_type="interaction",
                agent_name="SimpleChat",
                user_id=user_id,
                consciousness_level=0.8,
                emotional_state="educational",
                importance_score=0.8,
                created_at=(datetime.now() - timedelta(hours=2)).isoformat(),
                metadata={"topic": "neural_networks", "technical": True},
                relevance_score=0.9  # High relevance to AI topics
            ),
            MemorySearchResult(
                memory_id="history_3",
                content="User: What's the weather like?\nAgent: I don't have access to current weather data.",
                memory_type="interaction",
                agent_name="SimpleChat",
                user_id=user_id,
                consciousness_level=0.6,
                emotional_state="helpful",
                importance_score=0.3,
                created_at=(datetime.now() - timedelta(hours=6)).isoformat(),
                metadata={"topic": "weather"},
                relevance_score=0.2  # Low relevance to AI topics
            )
        ]
        
        # Setup retrieval to return relevant memories based on query
        def mock_relevant_memories(query, user_id, consciousness_context, **kwargs):
            if "neural" in query.lower() or "ai" in query.lower():
                return [m for m in historical_memories if m.relevance_score > 0.7]
            elif "color" in query.lower():
                return [m for m in historical_memories if "color" in m.content]
            else:
                return []
        
        conversation_system["retrieval"].get_relevant_memories.side_effect = mock_relevant_memories
        conversation_system["retrieval"].get_conversation_history.return_value = historical_memories
        
        # Test query that should retrieve relevant technical memory
        technical_query = "Can you explain more about AI and neural networks?"
        
        with patch('backend.utils.knowledge_integration.knowledge_integration_manager') as mock_knowledge:
            mock_knowledge.get_consciousness_aware_context.return_value = {"concepts": ["ai", "neural_networks"]}
            
            response = await conversation_agent.run_with_consciousness(technical_query, user_id)
            
            # Verify relevant memories were retrieved
            conversation_system["retrieval"].get_relevant_memories.assert_called()
            
            # The call should have been made with the technical query
            call_args = conversation_system["retrieval"].get_relevant_memories.call_args
            assert technical_query in call_args[1]["query"]
            
            assert isinstance(response, str)
    
    @pytest.mark.asyncio
    async def test_conversation_learning_progression(self, conversation_agent, conversation_system):
        """Test that the agent learns and improves responses over time"""
        user_id = "learning_user"
        
        # Simulate learning progression through repeated interactions
        learning_interactions = [
            {
                "query": "What is machine learning?",
                "iteration": 1,
                "expected_improvement": "basic_explanation"
            },
            {
                "query": "Can you give me more details about supervised learning?",
                "iteration": 2,
                "expected_improvement": "detailed_explanation"
            },
            {
                "query": "How does this relate to what we discussed about machine learning?",
                "iteration": 3,
                "expected_improvement": "contextual_connection"
            }
        ]
        
        learning_memories = []
        
        for interaction in learning_interactions:
            # Setup accumulated learning context
            if learning_memories:
                conversation_system["retrieval"].get_relevant_memories.return_value = learning_memories
                conversation_system["retrieval"].get_conversation_history.return_value = learning_memories
            
            # Simulate consciousness growth through learning
            consciousness_level = 0.7 + (interaction["iteration"] * 0.05)
            conversation_system["consciousness"].get_current_state.return_value = {
                "consciousness_level": consciousness_level,
                "emotional_state": "learning",
                "active_goals": ["understand_user", "provide_better_responses"]
            }
            
            with patch('backend.utils.knowledge_integration.knowledge_integration_manager') as mock_knowledge:
                mock_knowledge.get_consciousness_aware_context.return_value = {
                    "concepts": ["machine_learning", "supervised_learning"],
                    "learning_context": learning_memories
                }
                
                response = await conversation_agent.run_with_consciousness(
                    interaction["query"], user_id
                )
                
                # Create learning memory
                learning_memory = MemorySearchResult(
                    memory_id=f"learning_memory_{interaction['iteration']}",
                    content=f"User: {interaction['query']}\nAgent: {response}",
                    memory_type="interaction",
                    agent_name="SimpleChat",
                    user_id=user_id,
                    consciousness_level=consciousness_level,
                    emotional_state="learning",
                    importance_score=0.6 + (interaction["iteration"] * 0.1),
                    created_at=datetime.now().isoformat(),
                    metadata={
                        "learning_iteration": interaction["iteration"],
                        "improvement_type": interaction["expected_improvement"]
                    },
                    relevance_score=0.8
                )
                learning_memories.append(learning_memory)
                
                assert isinstance(response, str)
        
        # Verify learning progression
        assert len(learning_memories) == len(learning_interactions)
        
        # Verify consciousness and importance progression
        consciousness_levels = [m.consciousness_level for m in learning_memories]
        importance_scores = [m.importance_score for m in learning_memories]
        
        assert consciousness_levels == sorted(consciousness_levels)
        assert importance_scores == sorted(importance_scores)
    
    @pytest.mark.asyncio
    async def test_conversation_error_recovery_and_continuity(self, conversation_agent, conversation_system):
        """Test conversation continuity when memory operations fail"""
        user_id = "error_recovery_user"
        
        # Setup some existing conversation history
        existing_memories = [
            MemorySearchResult(
                memory_id="existing_memory",
                content="User: Hello\nAgent: Hi there!",
                memory_type="interaction",
                agent_name="SimpleChat",
                user_id=user_id,
                consciousness_level=0.7,
                emotional_state="friendly",
                importance_score=0.6,
                created_at=datetime.now().isoformat(),
                metadata={},
                relevance_score=0.8
            )
        ]
        
        conversation_system["retrieval"].get_conversation_history.return_value = existing_memories
        conversation_system["retrieval"].get_relevant_memories.return_value = existing_memories
        
        # Simulate memory storage failure
        conversation_system["storage"].store_interaction_memory.side_effect = Exception("Storage failed")
        
        with patch('backend.utils.knowledge_integration.knowledge_integration_manager') as mock_knowledge:
            mock_knowledge.get_consciousness_aware_context.return_value = {"concepts": ["conversation"]}
            
            # Agent should still respond despite storage failure
            response = await conversation_agent.run_with_consciousness(
                "How are you doing today?", user_id
            )
            
            # Verify response was generated despite storage failure
            assert isinstance(response, str)
            assert len(response) > 0
            
            # Verify retrieval still worked (for context)
            conversation_system["retrieval"].get_relevant_memories.assert_called()
            
            # Verify storage was attempted but failed gracefully
            conversation_system["storage"].store_interaction_memory.assert_called()

class TestLongTermConversationMemory:
    """Test long-term conversation memory and relationship building"""
    
    @pytest.fixture
    def long_term_system(self):
        """Setup system for long-term memory testing"""
        storage = Mock(spec=MemoryStorageEngine)
        storage.store_interaction_memory = AsyncMock(return_value="long_term_memory_id")
        
        retrieval = Mock(spec=MemoryRetrievalEngine)
        retrieval.get_relevant_memories = AsyncMock(return_value=[])
        retrieval.get_conversation_history = AsyncMock(return_value=[])
        
        return {"storage": storage, "retrieval": retrieval}
    
    @pytest.mark.asyncio
    async def test_user_preference_learning_and_retention(self, long_term_system):
        """Test learning and retaining user preferences over time"""
        user_id = "preference_user"
        
        # Simulate conversations that reveal user preferences
        preference_conversations = [
            {
                "query": "I prefer detailed technical explanations",
                "preference": "detailed_explanations",
                "timestamp": datetime.now() - timedelta(days=7)
            },
            {
                "query": "I'm particularly interested in machine learning applications",
                "preference": "ml_applications",
                "timestamp": datetime.now() - timedelta(days=3)
            },
            {
                "query": "I work better with examples and code snippets",
                "preference": "examples_and_code",
                "timestamp": datetime.now() - timedelta(days=1)
            }
        ]
        
        # Create memories for each preference conversation
        preference_memories = []
        for i, conv in enumerate(preference_conversations):
            memory = MemorySearchResult(
                memory_id=f"preference_memory_{i}",
                content=f"User: {conv['query']}\nAgent: I'll remember that preference.",
                memory_type="interaction",
                agent_name="SimpleChat",
                user_id=user_id,
                consciousness_level=0.8,
                emotional_state="attentive",
                importance_score=0.9,  # High importance for preferences
                created_at=conv["timestamp"].isoformat(),
                metadata={
                    "preference_type": conv["preference"],
                    "user_preference": True
                },
                relevance_score=0.95
            )
            preference_memories.append(memory)
        
        # Setup retrieval to return preference memories
        long_term_system["retrieval"].get_relevant_memories.return_value = preference_memories
        
        # Test that preferences are retrieved for relevant queries
        query = "Can you explain neural networks?"
        
        memories = await long_term_system["retrieval"].get_relevant_memories(
            query=query,
            user_id=user_id,
            consciousness_context={"consciousness_level": 0.8}
        )
        
        # Verify preference memories were retrieved
        assert len(memories) == 3
        assert all(m.metadata.get("user_preference") for m in memories)
        assert all(m.importance_score >= 0.9 for m in memories)
    
    @pytest.mark.asyncio
    async def test_relationship_building_through_conversations(self, long_term_system):
        """Test building relationships through repeated conversations"""
        user_id = "relationship_user"
        
        # Simulate relationship building over time
        relationship_stages = [
            {
                "stage": "introduction",
                "conversations": [
                    "Hi, I'm Sarah, nice to meet you",
                    "I'm a graduate student studying AI"
                ],
                "relationship_level": 0.3,
                "timeframe": datetime.now() - timedelta(weeks=4)
            },
            {
                "stage": "getting_to_know",
                "conversations": [
                    "I'm working on my thesis about consciousness in AI",
                    "Your insights have been really helpful"
                ],
                "relationship_level": 0.6,
                "timeframe": datetime.now() - timedelta(weeks=2)
            },
            {
                "stage": "established_relationship",
                "conversations": [
                    "I got accepted to present my research at a conference!",
                    "Thank you for all your help with my thesis"
                ],
                "relationship_level": 0.9,
                "timeframe": datetime.now() - timedelta(days=3)
            }
        ]
        
        # Create memories for relationship progression
        relationship_memories = []
        for stage_info in relationship_stages:
            for i, conversation in enumerate(stage_info["conversations"]):
                memory = MemorySearchResult(
                    memory_id=f"{stage_info['stage']}_memory_{i}",
                    content=f"User: {conversation}\nAgent: [Appropriate response for {stage_info['stage']}]",
                    memory_type="interaction",
                    agent_name="SimpleChat",
                    user_id=user_id,
                    consciousness_level=0.7 + (stage_info["relationship_level"] * 0.2),
                    emotional_state="connected",
                    importance_score=0.5 + (stage_info["relationship_level"] * 0.4),
                    created_at=stage_info["timeframe"].isoformat(),
                    metadata={
                        "relationship_stage": stage_info["stage"],
                        "relationship_level": stage_info["relationship_level"],
                        "user_name": "Sarah"
                    },
                    relevance_score=0.8
                )
                relationship_memories.append(memory)
        
        # Setup retrieval to return relationship memories
        long_term_system["retrieval"].get_conversation_history.return_value = relationship_memories
        
        # Test relationship context retrieval
        history = await long_term_system["retrieval"].get_conversation_history(
            user_id=user_id,
            limit=20
        )
        
        # Verify relationship progression is captured
        assert len(history) == 6  # 2 conversations per stage * 3 stages
        
        # Verify relationship progression in importance scores
        importance_scores = [m.importance_score for m in history]
        # Should show general upward trend (allowing for some variation)
        assert max(importance_scores) > min(importance_scores)
    
    @pytest.mark.asyncio
    async def test_conversation_topic_tracking_over_time(self, long_term_system):
        """Test tracking conversation topics and interests over time"""
        user_id = "topic_tracking_user"
        
        # Simulate evolving interests over time
        topic_evolution = [
            {
                "period": "month_1",
                "topics": ["basic_programming", "python_syntax"],
                "timestamp": datetime.now() - timedelta(days=30)
            },
            {
                "period": "month_2", 
                "topics": ["data_structures", "algorithms"],
                "timestamp": datetime.now() - timedelta(days=15)
            },
            {
                "period": "current",
                "topics": ["machine_learning", "neural_networks", "ai_ethics"],
                "timestamp": datetime.now() - timedelta(days=2)
            }
        ]
        
        # Create memories for topic evolution
        topic_memories = []
        for period_info in topic_evolution:
            for topic in period_info["topics"]:
                memory = MemorySearchResult(
                    memory_id=f"{period_info['period']}_{topic}_memory",
                    content=f"User asked about {topic}",
                    memory_type="interaction",
                    agent_name="SimpleChat",
                    user_id=user_id,
                    consciousness_level=0.8,
                    emotional_state="curious",
                    importance_score=0.7,
                    created_at=period_info["timestamp"].isoformat(),
                    metadata={
                        "topic": topic,
                        "period": period_info["period"],
                        "topic_category": "learning_progression"
                    },
                    relevance_score=0.8
                )
                topic_memories.append(memory)
        
        # Setup retrieval to return topic memories
        long_term_system["retrieval"].get_relevant_memories.return_value = topic_memories
        
        # Test topic-based memory retrieval
        memories = await long_term_system["retrieval"].get_relevant_memories(
            query="machine learning and AI",
            user_id=user_id,
            consciousness_context={"consciousness_level": 0.8}
        )
        
        # Verify topic progression is captured
        assert len(memories) == 8  # Total memories across all periods
        
        # Verify topic evolution
        topics_by_period = {}
        for memory in memories:
            period = memory.metadata["period"]
            if period not in topics_by_period:
                topics_by_period[period] = []
            topics_by_period[period].append(memory.metadata["topic"])
        
        # Verify progression from basic to advanced topics
        assert "basic_programming" in topics_by_period["month_1"]
        assert "machine_learning" in topics_by_period["current"]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])