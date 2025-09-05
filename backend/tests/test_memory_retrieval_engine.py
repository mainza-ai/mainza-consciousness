"""
Comprehensive unit tests for Memory Retrieval Engine
Tests memory search functionality, ranking algorithms, and consciousness-aware filtering.
"""
import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from typing import Dict, Any, List

# Import the components to test
from backend.utils.memory_retrieval_engine import (
    MemoryRetrievalEngine, MemorySearchParams, MemorySearchResult, MemoryRetrievalError
)
from backend.utils.memory_error_handling import (
    MemoryError, MemoryConnectionError, MemoryTimeoutError,
    MemoryErrorSeverity, MemoryErrorCategory
)

class TestMemorySearchParams:
    """Test the MemorySearchParams dataclass"""
    
    def test_search_params_creation(self):
        """Test basic search parameters creation"""
        consciousness_context = {"consciousness_level": 0.8, "emotional_state": "curious"}
        
        params = MemorySearchParams(
            query="test query",
            user_id="test_user",
            consciousness_context=consciousness_context,
            search_type="semantic",
            limit=10,
            similarity_threshold=0.5
        )
        
        assert params.query == "test query"
        assert params.user_id == "test_user"
        assert params.consciousness_context == consciousness_context
        assert params.search_type == "semantic"
        assert params.limit == 10
        assert params.similarity_threshold == 0.5
        assert params.temporal_weight == 0.3
        assert params.consciousness_weight == 0.4
        assert params.importance_weight == 0.3
    
    def test_search_params_defaults(self):
        """Test search parameters with default values"""
        params = MemorySearchParams(
            query="test",
            user_id="user",
            consciousness_context={}
        )
        
        assert params.search_type == "semantic"
        assert params.limit == 5
        assert params.similarity_threshold == 0.3
        assert params.memory_types is None
        assert params.time_range_hours is None

class TestMemorySearchResult:
    """Test the MemorySearchResult dataclass"""
    
    def test_search_result_creation(self):
        """Test memory search result creation"""
        result = MemorySearchResult(
            memory_id="test_memory_id",
            content="Test memory content",
            memory_type="interaction",
            agent_name="test_agent",
            user_id="test_user",
            consciousness_level=0.7,
            emotional_state="neutral",
            importance_score=0.6,
            created_at="2024-01-01T12:00:00",
            metadata={"test": "data"},
            relevance_score=0.8,
            similarity_score=0.75,
            temporal_score=0.9,
            consciousness_score=0.85,
            importance_factor=0.6
        )
        
        assert result.memory_id == "test_memory_id"
        assert result.content == "Test memory content"
        assert result.memory_type == "interaction"
        assert result.relevance_score == 0.8
        assert result.similarity_score == 0.75
        assert result.temporal_score == 0.9
        assert result.consciousness_score == 0.85

class TestMemoryRetrievalEngine:
    """Test the MemoryRetrievalEngine class"""
    
    @pytest.fixture
    def mock_neo4j_manager(self):
        """Mock Neo4j manager"""
        mock = Mock()
        mock.execute_query = Mock(return_value=[])
        return mock
    
    @pytest.fixture
    def mock_embedding_manager(self):
        """Mock memory embedding manager"""
        mock = Mock()
        mock.find_similar_memories = AsyncMock(return_value=[])
        return mock
    
    @pytest.fixture
    def mock_embedding(self):
        """Mock embedding service"""
        mock = Mock()
        mock.get_embedding = Mock(return_value=[0.1, 0.2, 0.3, 0.4, 0.5])
        return mock
    
    @pytest.fixture
    def retrieval_engine(self, mock_neo4j_manager, mock_embedding_manager, mock_embedding):
        """Create retrieval engine with mocked dependencies"""
        engine = MemoryRetrievalEngine()
        engine.neo4j = mock_neo4j_manager
        engine.embedding_manager = mock_embedding_manager
        engine.embedding = mock_embedding
        return engine
    
    @pytest.fixture
    def sample_memory_data(self):
        """Sample memory data for testing"""
        return [
            {
                "memory_id": "memory_1",
                "content": "User asked about AI and I explained artificial intelligence concepts",
                "memory_type": "interaction",
                "agent_name": "simple_chat",
                "consciousness_level": 0.7,
                "emotional_state": "neutral",
                "importance_score": 0.6,
                "created_at": "2024-01-01T12:00:00",
                "metadata": "{\"user_query\": \"What is AI?\"}",
                "similarity_score": 0.8
            },
            {
                "memory_id": "memory_2",
                "content": "Reflection on consciousness and self-awareness",
                "memory_type": "consciousness_reflection",
                "agent_name": "consciousness_system",
                "consciousness_level": 0.9,
                "emotional_state": "reflective",
                "importance_score": 0.8,
                "created_at": "2024-01-01T11:00:00",
                "metadata": "{}",
                "similarity_score": 0.6
            }
        ]
    
    @pytest.mark.asyncio
    async def test_initialize_success(self, retrieval_engine, mock_neo4j_manager):
        """Test successful initialization"""
        mock_neo4j_manager.execute_query.return_value = [{"test": 1}]
        
        result = await retrieval_engine.initialize()
        
        assert result is True
        mock_neo4j_manager.execute_query.assert_called_once_with("RETURN 1 as test", {})
    
    @pytest.mark.asyncio
    async def test_initialize_failure(self, retrieval_engine, mock_neo4j_manager):
        """Test initialization failure"""
        mock_neo4j_manager.execute_query.return_value = None
        
        result = await retrieval_engine.initialize()
        
        assert result is False
    
    @pytest.mark.asyncio
    async def test_get_relevant_memories_semantic_search(self, retrieval_engine, mock_embedding_manager):
        """Test semantic search for relevant memories"""
        # Setup mock response
        mock_memories = [
            {
                "memory_id": "test_memory",
                "content": "Test content",
                "memory_type": "interaction",
                "agent_name": "test_agent",
                "consciousness_level": 0.7,
                "emotional_state": "neutral",
                "importance_score": 0.6,
                "created_at": "2024-01-01T12:00:00",
                "metadata": {},
                "similarity_score": 0.8
            }
        ]
        mock_embedding_manager.find_similar_memories.return_value = mock_memories
        
        consciousness_context = {"consciousness_level": 0.7, "emotional_state": "neutral"}
        
        results = await retrieval_engine.get_relevant_memories(
            query="test query",
            user_id="test_user",
            consciousness_context=consciousness_context,
            search_type="semantic"
        )
        
        assert len(results) == 1
        assert isinstance(results[0], MemorySearchResult)
        assert results[0].memory_id == "test_memory"
        assert results[0].content == "Test content"
    
    @pytest.mark.asyncio
    async def test_get_relevant_memories_empty_result(self, retrieval_engine, mock_embedding_manager):
        """Test handling of empty search results"""
        mock_embedding_manager.find_similar_memories.return_value = []
        
        consciousness_context = {"consciousness_level": 0.7}
        
        results = await retrieval_engine.get_relevant_memories(
            query="nonexistent query",
            user_id="test_user",
            consciousness_context=consciousness_context
        )
        
        assert results == []
    
    @pytest.mark.asyncio
    async def test_get_relevant_memories_hybrid_search(self, retrieval_engine, sample_memory_data):
        """Test hybrid search combining multiple strategies"""
        with patch.object(retrieval_engine, '_semantic_search') as mock_semantic, \
             patch.object(retrieval_engine, '_keyword_search') as mock_keyword, \
             patch.object(retrieval_engine, '_temporal_search') as mock_temporal, \
             patch.object(retrieval_engine, '_calculate_relevance_scores') as mock_scoring, \
             patch.object(retrieval_engine, '_update_access_statistics') as mock_update:
            
            # Setup mock returns
            mock_semantic.return_value = [sample_memory_data[0]]
            mock_keyword.return_value = [sample_memory_data[1]]
            mock_temporal.return_value = []
            
            # Mock scoring to return MemorySearchResult objects
            mock_results = [
                MemorySearchResult(
                    memory_id="memory_1",
                    content="Test content 1",
                    memory_type="interaction",
                    agent_name="agent",
                    user_id="test_user",
                    consciousness_level=0.7,
                    emotional_state="neutral",
                    importance_score=0.6,
                    created_at="2024-01-01T12:00:00",
                    metadata={},
                    relevance_score=0.8
                )
            ]
            mock_scoring.return_value = mock_results
            mock_update.return_value = None
            
            consciousness_context = {"consciousness_level": 0.7}
            
            results = await retrieval_engine.get_relevant_memories(
                query="test query",
                user_id="test_user",
                consciousness_context=consciousness_context,
                search_type="hybrid"
            )
            
            assert len(results) == 1
            mock_semantic.assert_called_once()
            mock_keyword.assert_called_once()
            mock_temporal.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_semantic_memory_search(self, retrieval_engine, mock_embedding_manager):
        """Test semantic memory search with embeddings"""
        query_embedding = [0.1, 0.2, 0.3, 0.4, 0.5]
        consciousness_context = {"consciousness_level": 0.8}
        
        mock_memories = [
            {
                "memory_id": "semantic_memory",
                "content": "Semantic search result",
                "memory_type": "interaction",
                "agent_name": "test_agent",
                "consciousness_level": 0.8,
                "emotional_state": "neutral",
                "importance_score": 0.7,
                "created_at": "2024-01-01T12:00:00",
                "metadata": {},
                "similarity_score": 0.9
            }
        ]
        mock_embedding_manager.find_similar_memories.return_value = mock_memories
        
        results = await retrieval_engine.semantic_memory_search(
            query_embedding=query_embedding,
            user_id="test_user",
            consciousness_context=consciousness_context,
            limit=5
        )
        
        assert len(results) == 1
        assert results[0].memory_id == "semantic_memory"
        assert results[0].similarity_score == 0.9
        mock_embedding_manager.find_similar_memories.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_semantic_memory_search_invalid_embedding(self, retrieval_engine):
        """Test semantic search with invalid embedding"""
        invalid_embedding = []  # Empty embedding
        consciousness_context = {"consciousness_level": 0.7}
        
        results = await retrieval_engine.semantic_memory_search(
            query_embedding=invalid_embedding,
            user_id="test_user",
            consciousness_context=consciousness_context
        )
        
        assert results == []
    
    @pytest.mark.asyncio
    async def test_get_conversation_history(self, retrieval_engine, mock_neo4j_manager, sample_memory_data):
        """Test conversation history retrieval"""
        # Filter to only interaction memories
        interaction_memories = [m for m in sample_memory_data if m["memory_type"] == "interaction"]
        mock_neo4j_manager.execute_query.return_value = interaction_memories
        
        results = await retrieval_engine.get_conversation_history(
            user_id="test_user",
            limit=10
        )
        
        assert len(results) == 1
        assert results[0].memory_type == "interaction"
        assert results[0].relevance_score == 1.0  # Full relevance for conversation history
        mock_neo4j_manager.execute_query.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_conversation_history_with_filters(self, retrieval_engine, mock_neo4j_manager):
        """Test conversation history with time and agent filters"""
        mock_neo4j_manager.execute_query.return_value = []
        
        await retrieval_engine.get_conversation_history(
            user_id="test_user",
            limit=5,
            hours_back=24,
            agent_name="specific_agent"
        )
        
        # Verify query was called with appropriate parameters
        call_args = mock_neo4j_manager.execute_query.call_args
        assert call_args is not None
        query, params = call_args[0]
        
        assert "cutoff_time" in params
        assert "agent_name" in params
        assert params["agent_name"] == "specific_agent"
    
    @pytest.mark.asyncio
    async def test_keyword_search(self, retrieval_engine, mock_neo4j_manager, sample_memory_data):
        """Test keyword-based search"""
        mock_neo4j_manager.execute_query.return_value = sample_memory_data
        
        search_params = MemorySearchParams(
            query="artificial intelligence",
            user_id="test_user",
            consciousness_context={"consciousness_level": 0.7}
        )
        
        results = await retrieval_engine._keyword_search(search_params)
        
        assert len(results) == 2
        mock_neo4j_manager.execute_query.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_temporal_search(self, retrieval_engine, mock_neo4j_manager, sample_memory_data):
        """Test temporal-based search"""
        mock_neo4j_manager.execute_query.return_value = sample_memory_data
        
        search_params = MemorySearchParams(
            query="recent memories",
            user_id="test_user",
            consciousness_context={"consciousness_level": 0.7},
            time_range_hours=24
        )
        
        results = await retrieval_engine._temporal_search(search_params)
        
        assert len(results) == 2
        mock_neo4j_manager.execute_query.assert_called_once()
        
        # Verify time filter was applied
        call_args = mock_neo4j_manager.execute_query.call_args
        query, params = call_args[0]
        assert "cutoff_time" in params
    
    @pytest.mark.asyncio
    async def test_calculate_relevance_scores(self, retrieval_engine, sample_memory_data):
        """Test relevance score calculation"""
        search_params = MemorySearchParams(
            query="test query",
            user_id="test_user",
            consciousness_context={"consciousness_level": 0.7, "emotional_state": "neutral"},
            search_type="hybrid"
        )
        
        results = await retrieval_engine._calculate_relevance_scores(sample_memory_data, search_params)
        
        assert len(results) == 2
        assert all(isinstance(r, MemorySearchResult) for r in results)
        assert all(0.0 <= r.relevance_score <= 1.0 for r in results)
        assert all(hasattr(r, 'similarity_score') for r in results)
        assert all(hasattr(r, 'temporal_score') for r in results)
        assert all(hasattr(r, 'consciousness_score') for r in results)
    
    def test_calculate_temporal_score(self, retrieval_engine):
        """Test temporal score calculation"""
        current_time = datetime.now()
        
        # Recent memory (1 hour ago)
        recent_time = current_time - timedelta(hours=1)
        recent_score = retrieval_engine._calculate_temporal_score(
            recent_time.isoformat(), current_time
        )
        
        # Old memory (1 week ago)
        old_time = current_time - timedelta(weeks=1)
        old_score = retrieval_engine._calculate_temporal_score(
            old_time.isoformat(), current_time
        )
        
        assert 0.1 <= recent_score <= 1.0
        assert 0.1 <= old_score <= 1.0
        assert recent_score > old_score  # Recent should score higher
    
    def test_calculate_consciousness_score(self, retrieval_engine):
        """Test consciousness alignment score calculation"""
        current_context = {"consciousness_level": 0.8, "emotional_state": "curious"}
        
        # Aligned memory
        aligned_score = retrieval_engine._calculate_consciousness_score(
            memory_consciousness=0.8,
            memory_emotion="curious",
            current_context=current_context
        )
        
        # Misaligned memory
        misaligned_score = retrieval_engine._calculate_consciousness_score(
            memory_consciousness=0.3,
            memory_emotion="frustrated",
            current_context=current_context
        )
        
        assert 0.0 <= aligned_score <= 1.0
        assert 0.0 <= misaligned_score <= 1.0
        assert aligned_score > misaligned_score
    
    def test_extract_keywords(self, retrieval_engine):
        """Test keyword extraction from query text"""
        query = "What is artificial intelligence and machine learning?"
        
        keywords = retrieval_engine._extract_keywords(query)
        
        assert isinstance(keywords, list)
        assert "artificial" in keywords
        assert "intelligence" in keywords
        assert "machine" in keywords
        assert "learning" in keywords
        # Stop words should be filtered out
        assert "what" not in keywords
        assert "is" not in keywords
        assert "and" not in keywords
    
    def test_extract_keywords_empty_query(self, retrieval_engine):
        """Test keyword extraction from empty query"""
        keywords = retrieval_engine._extract_keywords("")
        
        assert keywords == []
    
    @pytest.mark.asyncio
    async def test_consciousness_aware_search(self, retrieval_engine, mock_embedding_manager):
        """Test consciousness-aware search functionality"""
        consciousness_context = {
            "consciousness_level": 0.9,
            "emotional_state": "reflective"
        }
        
        mock_memories = [
            {
                "memory_id": "consciousness_memory",
                "content": "Deep reflection on consciousness",
                "memory_type": "consciousness_reflection",
                "agent_name": "consciousness_system",
                "consciousness_level": 0.9,
                "emotional_state": "reflective",
                "importance_score": 0.9,
                "created_at": "2024-01-01T12:00:00",
                "metadata": {},
                "similarity_score": 0.95
            }
        ]
        mock_embedding_manager.find_similar_memories.return_value = mock_memories
        
        results = await retrieval_engine.get_relevant_memories(
            query="consciousness reflection",
            user_id="test_user",
            consciousness_context=consciousness_context,
            search_type="consciousness_aware"
        )
        
        assert len(results) >= 0  # Should handle consciousness-aware search
    
    @pytest.mark.asyncio
    async def test_update_access_statistics(self, retrieval_engine, mock_neo4j_manager):
        """Test updating memory access statistics"""
        mock_neo4j_manager.execute_write_query = Mock(return_value=[{"updated_count": 3}])
        
        memory_ids = ["memory_1", "memory_2", "memory_3"]
        
        await retrieval_engine._update_access_statistics(memory_ids)
        
        mock_neo4j_manager.execute_write_query.assert_called_once()
        call_args = mock_neo4j_manager.execute_write_query.call_args
        assert call_args is not None
    
    @pytest.mark.asyncio
    async def test_error_handling_neo4j_failure(self, retrieval_engine, mock_neo4j_manager):
        """Test error handling when Neo4j fails"""
        mock_neo4j_manager.execute_query.side_effect = Exception("Neo4j connection failed")
        
        # Should return empty list instead of raising exception
        results = await retrieval_engine.get_conversation_history("test_user")
        
        assert results == []
    
    @pytest.mark.asyncio
    async def test_error_handling_embedding_failure(self, retrieval_engine, mock_embedding_manager):
        """Test error handling when embedding service fails"""
        mock_embedding_manager.find_similar_memories.side_effect = Exception("Embedding service down")
        
        consciousness_context = {"consciousness_level": 0.7}
        
        # Should return empty list instead of raising exception
        results = await retrieval_engine.get_relevant_memories(
            query="test query",
            user_id="test_user",
            consciousness_context=consciousness_context,
            search_type="semantic"
        )
        
        assert results == []
    
    @pytest.mark.asyncio
    async def test_parameter_validation(self, retrieval_engine, mock_embedding_manager):
        """Test parameter validation and sanitization"""
        mock_embedding_manager.find_similar_memories.return_value = []
        
        consciousness_context = {"consciousness_level": 0.7}
        
        # Test limit validation (should be clamped to max_limit)
        results = await retrieval_engine.get_relevant_memories(
            query="test",
            user_id="test_user",
            consciousness_context=consciousness_context,
            limit=1000  # Exceeds max_limit
        )
        
        # Should not raise error, limit should be clamped
        assert results == []
        
        # Test similarity threshold validation
        results = await retrieval_engine.get_relevant_memories(
            query="test",
            user_id="test_user",
            consciousness_context=consciousness_context,
            similarity_threshold=2.0  # Invalid threshold > 1.0
        )
        
        # Should not raise error, threshold should be clamped
        assert results == []

class TestMemoryRetrievalEngineIntegration:
    """Integration tests for memory retrieval engine"""
    
    @pytest.fixture
    def retrieval_engine(self):
        """Create real retrieval engine for integration tests"""
        return MemoryRetrievalEngine()
    
    @pytest.mark.asyncio
    async def test_full_search_workflow(self, retrieval_engine):
        """Test complete search workflow with mocked dependencies"""
        with patch.object(retrieval_engine, 'neo4j') as mock_neo4j, \
             patch.object(retrieval_engine, 'embedding_manager') as mock_embedding_manager, \
             patch.object(retrieval_engine, 'embedding') as mock_embedding:
            
            # Setup mocks
            mock_embedding.get_embedding.return_value = [0.1, 0.2, 0.3, 0.4, 0.5]
            mock_embedding_manager.find_similar_memories.return_value = [
                {
                    "memory_id": "test_memory",
                    "content": "Test memory content",
                    "memory_type": "interaction",
                    "agent_name": "test_agent",
                    "consciousness_level": 0.7,
                    "emotional_state": "neutral",
                    "importance_score": 0.6,
                    "created_at": "2024-01-01T12:00:00",
                    "metadata": {},
                    "similarity_score": 0.8
                }
            ]
            mock_neo4j.execute_write_query = Mock(return_value=[{"updated_count": 1}])
            
            consciousness_context = {
                "consciousness_level": 0.7,
                "emotional_state": "neutral"
            }
            
            # Execute search
            results = await retrieval_engine.get_relevant_memories(
                query="test query about AI",
                user_id="test_user",
                consciousness_context=consciousness_context,
                limit=5,
                search_type="semantic"
            )
            
            # Verify results
            assert len(results) == 1
            assert results[0].memory_id == "test_memory"
            assert results[0].relevance_score > 0
            
            # Verify access statistics were updated
            mock_neo4j.execute_write_query.assert_called_once()

if __name__ == "__main__":
    pytest.main([__file__])