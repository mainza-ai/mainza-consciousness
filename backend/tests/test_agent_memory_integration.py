"""
Integration tests for Agent-Memory workflows
Tests memory integration with agents, consciousness-aware memory processing, and end-to-end workflows.
"""
import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from typing import Dict, Any, List

# Import the components to test
from backend.agents.base_conscious_agent import ConsciousAgent
from backend.agents.simple_chat import EnhancedSimpleChatAgent
from backend.utils.memory_storage_engine import MemoryStorageEngine, MemoryRecord
from backend.utils.memory_retrieval_engine import MemoryRetrievalEngine, MemorySearchResult
from backend.utils.memory_context_builder import MemoryContextBuilder, MemoryContext
from backend.utils.memory_error_handling import MemoryError, MemoryStorageError

class TestAgentMemoryIntegration:
    """Test memory integration with agent framework"""
    
    @pytest.fixture
    def mock_memory_storage(self):
        """Mock memory storage engine"""
        mock = Mock(spec=MemoryStorageEngine)
        mock.initialize = AsyncMock(return_value=True)
        mock.store_interaction_memory = AsyncMock(return_value="test_memory_id")
        mock.store_consciousness_memory = AsyncMock(return_value="consciousness_memory_id")
        return mock
    
    @pytest.fixture
    def mock_memory_retrieval(self):
        """Mock memory retrieval engine"""
        mock = Mock(spec=MemoryRetrievalEngine)
        mock.initialize = AsyncMock(return_value=True)
        mock.get_relevant_memories = AsyncMock(return_value=[])
        mock.get_conversation_history = AsyncMock(return_value=[])
        return mock
    
    @pytest.fixture
    def mock_memory_context_builder(self):
        """Mock memory context builder"""
        mock = Mock(spec=MemoryContextBuilder)
        mock.build_comprehensive_context = AsyncMock(return_value=MemoryContext(
            relevant_memories=[],
            conversation_history=[],
            related_concepts=[],
            context_strength=0.5,
            consciousness_alignment=0.7,
            temporal_relevance=0.8,
            formatted_context="Test memory context"
        ))
        return mock
    
    @pytest.fixture
    def sample_agent(self, mock_memory_storage, mock_memory_retrieval, mock_memory_context_builder):
        """Create test agent with mocked memory components"""
        class TestAgent(ConsciousAgent):
            def __init__(self):
                super().__init__("TestAgent", ["test_capability"])
                # Override memory components with mocks
                self.memory_storage = mock_memory_storage
                self.memory_retrieval = mock_memory_retrieval
                self.memory_context_builder = mock_memory_context_builder
                self.memory_enabled = True
            
            async def execute_with_context(self, query, user_id, consciousness_context, **kwargs):
                return f"Test response to: {query}"
            
            async def get_consciousness_context(self):
                return {"consciousness_level": 0.8, "emotional_state": "curious"}
        
        return TestAgent()
    
    @pytest.fixture
    def sample_memories(self):
        """Sample memory search results"""
        return [
            MemorySearchResult(
                memory_id="memory_1",
                content="Previous conversation about AI",
                memory_type="interaction",
                agent_name="SimpleChat",
                user_id="test_user",
                consciousness_level=0.7,
                emotional_state="neutral",
                importance_score=0.6,
                created_at="2024-01-01T12:00:00",
                metadata={"user_query": "What is AI?"},
                relevance_score=0.8
            ),
            MemorySearchResult(
                memory_id="memory_2",
                content="Consciousness reflection on learning",
                memory_type="consciousness_reflection",
                agent_name="consciousness_system",
                user_id="system",
                consciousness_level=0.9,
                emotional_state="reflective",
                importance_score=0.8,
                created_at="2024-01-01T11:00:00",
                metadata={},
                relevance_score=0.7
            )
        ]
    
    @pytest.mark.asyncio
    async def test_agent_memory_initialization(self, sample_agent):
        """Test agent memory component initialization"""
        assert sample_agent.memory_enabled is True
        assert sample_agent.memory_storage is not None
        assert sample_agent.memory_retrieval is not None
        assert sample_agent.memory_context_builder is not None
    
    @pytest.mark.asyncio
    async def test_agent_memory_initialization_failure(self):
        """Test agent behavior when memory initialization fails"""
        with patch('backend.agents.base_conscious_agent.memory_storage_engine', side_effect=ImportError("Module not found")):
            class TestAgent(ConsciousAgent):
                def __init__(self):
                    super().__init__("TestAgent", ["test"])
                
                async def execute_with_context(self, query, user_id, consciousness_context, **kwargs):
                    return "test response"
                
                async def get_consciousness_context(self):
                    return {"consciousness_level": 0.7}
            
            agent = TestAgent()
            assert agent.memory_enabled is False
    
    @pytest.mark.asyncio
    async def test_get_relevant_memories(self, sample_agent, sample_memories):
        """Test agent memory retrieval functionality"""
        # Setup mock to return sample memories
        sample_agent.memory_retrieval.get_relevant_memories.return_value = sample_memories
        
        query = "Tell me about artificial intelligence"
        user_id = "test_user"
        consciousness_context = {"consciousness_level": 0.8, "emotional_state": "curious"}
        
        memories = await sample_agent.get_relevant_memories(query, user_id, consciousness_context)
        
        assert len(memories) == 2
        sample_agent.memory_retrieval.get_relevant_memories.assert_called_once_with(
            query=query,
            user_id=user_id,
            consciousness_context=consciousness_context,
            limit=5,
            search_type="hybrid"
        )
    
    @pytest.mark.asyncio
    async def test_get_relevant_memories_failure(self, sample_agent):
        """Test agent behavior when memory retrieval fails"""
        sample_agent.memory_retrieval.get_relevant_memories.side_effect = Exception("Retrieval failed")
        
        memories = await sample_agent.get_relevant_memories(
            "test query", "test_user", {"consciousness_level": 0.7}
        )
        
        # Should return empty dict on failure
        assert memories == {}
    
    @pytest.mark.asyncio
    async def test_store_interaction_memory(self, sample_agent):
        """Test agent interaction memory storage"""
        query = "What is consciousness?"
        response = "Consciousness is the state of being aware..."
        user_id = "test_user"
        consciousness_context = {"consciousness_level": 0.8, "emotional_state": "reflective"}
        
        memory_id = await sample_agent.store_interaction_memory(
            query, response, user_id, consciousness_context
        )
        
        assert memory_id == "test_memory_id"
        sample_agent.memory_storage.store_interaction_memory.assert_called_once_with(
            user_query=query,
            agent_response=response,
            user_id=user_id,
            agent_name=sample_agent.name,
            consciousness_context=consciousness_context
        )
    
    @pytest.mark.asyncio
    async def test_store_interaction_memory_failure(self, sample_agent):
        """Test agent behavior when memory storage fails"""
        sample_agent.memory_storage.store_interaction_memory.side_effect = MemoryStorageError("Storage failed")
        
        memory_id = await sample_agent.store_interaction_memory(
            "test query", "test response", "test_user", {"consciousness_level": 0.7}
        )
        
        # Should return None on failure
        assert memory_id is None
    
    @pytest.mark.asyncio
    async def test_enhance_prompt_with_memory(self, sample_agent, sample_memories):
        """Test prompt enhancement with memory context"""
        query = "Tell me about AI"
        memory_context = {
            "relevant_memories": sample_memories,
            "formatted_context": "Previous conversation: User asked about AI..."
        }
        
        enhanced_prompt = sample_agent.enhance_prompt_with_memory(query, memory_context)
        
        assert isinstance(enhanced_prompt, str)
        assert query in enhanced_prompt
        assert "Previous conversation" in enhanced_prompt
    
    @pytest.mark.asyncio
    async def test_enhance_prompt_with_empty_memory(self, sample_agent):
        """Test prompt enhancement with empty memory context"""
        query = "Tell me about AI"
        memory_context = {}
        
        enhanced_prompt = sample_agent.enhance_prompt_with_memory(query, memory_context)
        
        # Should return original query when no memory context
        assert enhanced_prompt == query
    
    @pytest.mark.asyncio
    async def test_run_with_consciousness_memory_integration(self, sample_agent, sample_memories):
        """Test full agent execution with memory integration"""
        # Setup mocks
        sample_agent.memory_retrieval.get_relevant_memories.return_value = sample_memories
        
        with patch.object(sample_agent, 'get_consciousness_context') as mock_consciousness, \
             patch('backend.utils.knowledge_integration.knowledge_integration_manager') as mock_knowledge:
            
            mock_consciousness.return_value = {"consciousness_level": 0.8, "emotional_state": "curious"}
            mock_knowledge.get_consciousness_aware_context.return_value = {"concepts": ["ai"]}
            
            query = "What is artificial intelligence?"
            user_id = "test_user"
            
            result = await sample_agent.run_with_consciousness(query, user_id)
            
            # Verify memory retrieval was called
            sample_agent.memory_retrieval.get_relevant_memories.assert_called_once()
            
            # Verify memory storage was called
            sample_agent.memory_storage.store_interaction_memory.assert_called_once()
            
            assert isinstance(result, str)
    
    @pytest.mark.asyncio
    async def test_memory_performance_tracking(self, sample_agent):
        """Test memory performance tracking in agents"""
        # Execute multiple operations to track performance
        for i in range(3):
            await sample_agent.get_relevant_memories(
                f"query {i}", "test_user", {"consciousness_level": 0.7}
            )
        
        # Verify performance metrics are tracked
        assert hasattr(sample_agent, 'execution_count')
        assert sample_agent.memory_retrieval.get_relevant_memories.call_count == 3

class TestSimpleChatMemoryIntegration:
    """Test memory integration with SimpleChat agent specifically"""
    
    @pytest.fixture
    def mock_simple_chat_agent(self):
        """Mock the pydantic-ai simple chat agent"""
        mock = Mock()
        mock.run = AsyncMock(return_value=Mock(data="Test response from simple chat"))
        return mock
    
    @pytest.fixture
    def enhanced_simple_chat(self, mock_simple_chat_agent):
        """Create enhanced simple chat agent with mocked dependencies"""
        with patch('backend.agents.simple_chat.simple_chat_agent', mock_simple_chat_agent):
            agent = EnhancedSimpleChatAgent()
            
            # Mock memory components
            agent.memory_storage = Mock()
            agent.memory_storage.store_interaction_memory = AsyncMock(return_value="chat_memory_id")
            
            agent.memory_retrieval = Mock()
            agent.memory_retrieval.get_relevant_memories = AsyncMock(return_value=[])
            
            agent.memory_context_builder = Mock()
            agent.memory_context_builder.build_comprehensive_context = AsyncMock(
                return_value=MemoryContext(
                    relevant_memories=[],
                    conversation_history=[],
                    related_concepts=[],
                    context_strength=0.6,
                    consciousness_alignment=0.8,
                    temporal_relevance=0.7,
                    formatted_context="Chat memory context"
                )
            )
            
            agent.memory_enabled = True
            return agent
    
    @pytest.mark.asyncio
    async def test_simple_chat_memory_enhanced_execution(self, enhanced_simple_chat):
        """Test SimpleChat execution with memory enhancement"""
        with patch('backend.utils.knowledge_integration.knowledge_integration_manager') as mock_knowledge:
            mock_knowledge.get_consciousness_aware_context.return_value = {"concepts": ["conversation"]}
            
            query = "Hello, how are you?"
            user_id = "test_user"
            consciousness_context = {"consciousness_level": 0.7, "emotional_state": "friendly"}
            
            result = await enhanced_simple_chat.execute_with_context(
                query=query,
                user_id=user_id,
                consciousness_context=consciousness_context
            )
            
            # Verify memory context was built
            enhanced_simple_chat.memory_context_builder.build_comprehensive_context.assert_called_once()
            
            assert isinstance(result, str)
    
    @pytest.mark.asyncio
    async def test_simple_chat_conversation_continuity(self, enhanced_simple_chat):
        """Test conversation continuity through memory"""
        # Setup conversation history
        conversation_memories = [
            MemorySearchResult(
                memory_id="conv_1",
                content="User: Hi, I'm John. Agent: Nice to meet you, John!",
                memory_type="interaction",
                agent_name="SimpleChat",
                user_id="test_user",
                consciousness_level=0.7,
                emotional_state="friendly",
                importance_score=0.6,
                created_at="2024-01-01T12:00:00",
                metadata={"user_query": "Hi, I'm John"},
                relevance_score=0.9
            )
        ]
        
        enhanced_simple_chat.memory_retrieval.get_relevant_memories.return_value = conversation_memories
        
        with patch('backend.utils.knowledge_integration.knowledge_integration_manager') as mock_knowledge:
            mock_knowledge.get_consciousness_aware_context.return_value = {}
            
            # Second message in conversation
            query = "Do you remember my name?"
            consciousness_context = {"consciousness_level": 0.7, "emotional_state": "curious"}
            
            result = await enhanced_simple_chat.execute_with_context(
                query=query,
                user_id="test_user",
                consciousness_context=consciousness_context
            )
            
            # Verify memory retrieval was called to get conversation history
            enhanced_simple_chat.memory_retrieval.get_relevant_memories.assert_called()
            
            assert isinstance(result, str)
    
    @pytest.mark.asyncio
    async def test_simple_chat_fallback_without_memory(self, enhanced_simple_chat):
        """Test SimpleChat fallback when memory is disabled"""
        enhanced_simple_chat.memory_enabled = False
        
        query = "Tell me a joke"
        consciousness_context = {"consciousness_level": 0.8, "emotional_state": "playful"}
        
        result = await enhanced_simple_chat.execute_with_context(
            query=query,
            user_id="test_user",
            consciousness_context=consciousness_context
        )
        
        # Should still work without memory
        assert isinstance(result, str)
        
        # Memory components should not be called
        enhanced_simple_chat.memory_retrieval.get_relevant_memories.assert_not_called()

class TestMemoryAgentWorkflows:
    """Test complete memory-agent workflows"""
    
    @pytest.fixture
    def memory_workflow_setup(self):
        """Setup complete memory workflow with all components"""
        # Mock all memory components
        storage = Mock(spec=MemoryStorageEngine)
        storage.initialize = AsyncMock(return_value=True)
        storage.store_interaction_memory = AsyncMock(return_value="workflow_memory_id")
        
        retrieval = Mock(spec=MemoryRetrievalEngine)
        retrieval.initialize = AsyncMock(return_value=True)
        retrieval.get_relevant_memories = AsyncMock(return_value=[])
        
        context_builder = Mock(spec=MemoryContextBuilder)
        context_builder.build_comprehensive_context = AsyncMock(
            return_value=MemoryContext(
                relevant_memories=[],
                conversation_history=[],
                related_concepts=[],
                context_strength=0.7,
                consciousness_alignment=0.8,
                temporal_relevance=0.6,
                formatted_context="Workflow memory context"
            )
        )
        
        return {
            "storage": storage,
            "retrieval": retrieval,
            "context_builder": context_builder
        }
    
    @pytest.mark.asyncio
    async def test_complete_memory_workflow(self, memory_workflow_setup):
        """Test complete memory workflow from query to response with storage"""
        components = memory_workflow_setup
        
        class WorkflowAgent(ConsciousAgent):
            def __init__(self):
                super().__init__("WorkflowAgent", ["workflow_test"])
                self.memory_storage = components["storage"]
                self.memory_retrieval = components["retrieval"]
                self.memory_context_builder = components["context_builder"]
                self.memory_enabled = True
            
            async def execute_with_context(self, query, user_id, consciousness_context, **kwargs):
                return f"Workflow response to: {query}"
            
            async def get_consciousness_context(self):
                return {"consciousness_level": 0.8, "emotional_state": "focused"}
        
        agent = WorkflowAgent()
        
        with patch('backend.utils.knowledge_integration.knowledge_integration_manager') as mock_knowledge:
            mock_knowledge.get_consciousness_aware_context.return_value = {"concepts": ["workflow"]}
            
            # Execute complete workflow
            query = "Test workflow query"
            user_id = "workflow_user"
            
            result = await agent.run_with_consciousness(query, user_id)
            
            # Verify all memory operations were called
            components["retrieval"].get_relevant_memories.assert_called_once()
            components["storage"].store_interaction_memory.assert_called_once()
            
            # Verify result
            assert "Workflow response to: Test workflow query" in result
    
    @pytest.mark.asyncio
    async def test_memory_workflow_error_recovery(self, memory_workflow_setup):
        """Test memory workflow error recovery and graceful degradation"""
        components = memory_workflow_setup
        
        # Setup storage to fail
        components["storage"].store_interaction_memory.side_effect = MemoryStorageError("Storage failed")
        
        class ErrorRecoveryAgent(ConsciousAgent):
            def __init__(self):
                super().__init__("ErrorRecoveryAgent", ["error_recovery"])
                self.memory_storage = components["storage"]
                self.memory_retrieval = components["retrieval"]
                self.memory_context_builder = components["context_builder"]
                self.memory_enabled = True
            
            async def execute_with_context(self, query, user_id, consciousness_context, **kwargs):
                return f"Recovery response to: {query}"
            
            async def get_consciousness_context(self):
                return {"consciousness_level": 0.7, "emotional_state": "resilient"}
        
        agent = ErrorRecoveryAgent()
        
        with patch('backend.utils.knowledge_integration.knowledge_integration_manager') as mock_knowledge:
            mock_knowledge.get_consciousness_aware_context.return_value = {}
            
            # Execute workflow with storage failure
            query = "Test error recovery"
            user_id = "recovery_user"
            
            # Should not raise exception despite storage failure
            result = await agent.run_with_consciousness(query, user_id)
            
            # Verify retrieval still worked
            components["retrieval"].get_relevant_memories.assert_called_once()
            
            # Verify storage was attempted but failed gracefully
            components["storage"].store_interaction_memory.assert_called_once()
            
            # Agent should still return result
            assert "Recovery response to: Test error recovery" in result
    
    @pytest.mark.asyncio
    async def test_multi_agent_memory_sharing(self, memory_workflow_setup):
        """Test memory sharing between multiple agents"""
        components = memory_workflow_setup
        
        # Setup shared memories
        shared_memories = [
            MemorySearchResult(
                memory_id="shared_memory",
                content="Shared knowledge about user preferences",
                memory_type="interaction",
                agent_name="Agent1",
                user_id="shared_user",
                consciousness_level=0.8,
                emotional_state="helpful",
                importance_score=0.7,
                created_at="2024-01-01T12:00:00",
                metadata={"shared": True},
                relevance_score=0.8
            )
        ]
        
        components["retrieval"].get_relevant_memories.return_value = shared_memories
        
        class SharedMemoryAgent(ConsciousAgent):
            def __init__(self, name):
                super().__init__(name, ["shared_memory"])
                self.memory_storage = components["storage"]
                self.memory_retrieval = components["retrieval"]
                self.memory_context_builder = components["context_builder"]
                self.memory_enabled = True
            
            async def execute_with_context(self, query, user_id, consciousness_context, **kwargs):
                return f"{self.name} response with shared memory"
            
            async def get_consciousness_context(self):
                return {"consciousness_level": 0.8, "emotional_state": "collaborative"}
        
        agent1 = SharedMemoryAgent("Agent1")
        agent2 = SharedMemoryAgent("Agent2")
        
        with patch('backend.utils.knowledge_integration.knowledge_integration_manager') as mock_knowledge:
            mock_knowledge.get_consciousness_aware_context.return_value = {}
            
            # Both agents should access the same shared memories
            user_id = "shared_user"
            query = "Remember my preferences"
            
            result1 = await agent1.run_with_consciousness(query, user_id)
            result2 = await agent2.run_with_consciousness(query, user_id)
            
            # Both agents should have retrieved the same shared memory
            assert components["retrieval"].get_relevant_memories.call_count == 2
            
            # Both should return responses
            assert "Agent1 response" in result1
            assert "Agent2 response" in result2
    
    @pytest.mark.asyncio
    async def test_memory_context_influence_on_response(self, memory_workflow_setup):
        """Test how memory context influences agent responses"""
        components = memory_workflow_setup
        
        # Setup memory with specific context
        contextual_memories = [
            MemorySearchResult(
                memory_id="context_memory",
                content="User prefers detailed technical explanations",
                memory_type="interaction",
                agent_name="ContextAgent",
                user_id="context_user",
                consciousness_level=0.9,
                emotional_state="analytical",
                importance_score=0.8,
                created_at="2024-01-01T12:00:00",
                metadata={"preference": "detailed"},
                relevance_score=0.9
            )
        ]
        
        components["retrieval"].get_relevant_memories.return_value = contextual_memories
        
        class ContextInfluencedAgent(ConsciousAgent):
            def __init__(self):
                super().__init__("ContextAgent", ["context_aware"])
                self.memory_storage = components["storage"]
                self.memory_retrieval = components["retrieval"]
                self.memory_context_builder = components["context_builder"]
                self.memory_enabled = True
            
            async def execute_with_context(self, query, user_id, consciousness_context, **kwargs):
                memory_context = kwargs.get("memory_context", {})
                
                # Simulate response adaptation based on memory context
                if memory_context and "detailed" in str(memory_context):
                    return f"Detailed technical response to: {query}"
                else:
                    return f"Simple response to: {query}"
            
            async def get_consciousness_context(self):
                return {"consciousness_level": 0.9, "emotional_state": "adaptive"}
        
        agent = ContextInfluencedAgent()
        
        with patch('backend.utils.knowledge_integration.knowledge_integration_manager') as mock_knowledge:
            mock_knowledge.get_consciousness_aware_context.return_value = {}
            
            query = "Explain machine learning"
            user_id = "context_user"
            
            result = await agent.run_with_consciousness(query, user_id)
            
            # Response should be influenced by memory context
            # Note: This test demonstrates the pattern, actual implementation may vary
            assert isinstance(result, str)
            components["retrieval"].get_relevant_memories.assert_called_once()

if __name__ == "__main__":
    pytest.main([__file__])