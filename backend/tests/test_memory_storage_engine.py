"""
Comprehensive unit tests for Memory Storage Engine
Tests memory storage functionality, Neo4j integration, and error handling.
"""
import pytest
import asyncio
import uuid
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from typing import Dict, Any, List

# Import the components to test
from backend.utils.memory_storage_engine import (
    MemoryStorageEngine, MemoryRecord, MemoryStorageError
)
from backend.utils.memory_error_handling import (
    MemoryError, MemoryConnectionError, MemoryValidationError,
    MemoryEmbeddingError, MemoryErrorSeverity, MemoryErrorCategory
)

class TestMemoryRecord:
    """Test the MemoryRecord dataclass"""
    
    def test_memory_record_creation(self):
        """Test basic memory record creation"""
        memory_id = str(uuid.uuid4())
        created_at = datetime.now()
        
        record = MemoryRecord(
            memory_id=memory_id,
            content="Test memory content",
            memory_type="interaction",
            user_id="test_user",
            agent_name="test_agent",
            consciousness_level=0.7,
            emotional_state="neutral",
            importance_score=0.5,
            embedding=[0.1, 0.2, 0.3],
            created_at=created_at
        )
        
        assert record.memory_id == memory_id
        assert record.content == "Test memory content"
        assert record.memory_type == "interaction"
        assert record.user_id == "test_user"
        assert record.agent_name == "test_agent"
        assert record.consciousness_level == 0.7
        assert record.emotional_state == "neutral"
        assert record.importance_score == 0.5
        assert record.embedding == [0.1, 0.2, 0.3]
        assert record.created_at == created_at
        assert record.access_count == 0
        assert record.significance_score == 0.5
        assert record.decay_rate == 0.95
    
    def test_memory_record_defaults(self):
        """Test memory record with default values"""
        record = MemoryRecord(
            memory_id="test_id",
            content="Test content",
            memory_type="reflection",
            user_id="user",
            agent_name="agent",
            consciousness_level=0.8,
            emotional_state="excited",
            importance_score=0.9,
            embedding=[],
            created_at=datetime.now()
        )
        
        assert record.last_accessed is None
        assert record.access_count == 0
        assert record.significance_score == 0.5
        assert record.decay_rate == 0.95
        assert record.metadata == {}

class TestMemoryStorageEngine:
    """Test the MemoryStorageEngine class"""
    
    @pytest.fixture
    def mock_neo4j_manager(self):
        """Mock Neo4j manager"""
        mock = Mock()
        mock.execute_query = Mock(return_value=[{"test": 1}])
        mock.execute_write_query = Mock(return_value=[{"memory_id": "test_memory_id"}])
        return mock
    
    @pytest.fixture
    def mock_embedding_manager(self):
        """Mock embedding manager"""
        mock = Mock()
        mock.get_embedding = Mock(return_value=[0.1, 0.2, 0.3, 0.4, 0.5])
        return mock
    
    @pytest.fixture
    def storage_engine(self, mock_neo4j_manager, mock_embedding_manager):
        """Create storage engine with mocked dependencies"""
        engine = MemoryStorageEngine()
        engine.neo4j = mock_neo4j_manager
        engine.embedding = mock_embedding_manager
        return engine
    
    @pytest.mark.asyncio
    async def test_initialize_success(self, storage_engine, mock_neo4j_manager):
        """Test successful initialization"""
        mock_neo4j_manager.execute_query.return_value = [{"test": 1}]
        
        result = await storage_engine.initialize()
        
        assert result is True
        mock_neo4j_manager.execute_query.assert_called_once_with("RETURN 1 as test", {})
    
    @pytest.mark.asyncio
    async def test_initialize_failure(self, storage_engine, mock_neo4j_manager):
        """Test initialization failure"""
        mock_neo4j_manager.execute_query.return_value = None
        
        result = await storage_engine.initialize()
        
        assert result is False
    
    @pytest.mark.asyncio
    async def test_initialize_exception(self, storage_engine, mock_neo4j_manager):
        """Test initialization with exception"""
        mock_neo4j_manager.execute_query.side_effect = Exception("Connection failed")
        
        result = await storage_engine.initialize()
        
        assert result is False
    
    @pytest.mark.asyncio
    async def test_store_interaction_memory_success(self, storage_engine, mock_neo4j_manager, mock_embedding_manager):
        """Test successful interaction memory storage"""
        # Setup mocks
        mock_embedding_manager.get_embedding.return_value = [0.1, 0.2, 0.3]
        mock_neo4j_manager.execute_write_query.return_value = [{"memory_id": "test_memory_id"}]
        
        # Test data
        user_query = "What is artificial intelligence?"
        agent_response = "AI is a field of computer science..."
        user_id = "test_user"
        agent_name = "simple_chat"
        consciousness_context = {
            "consciousness_level": 0.8,
            "emotional_state": "curious"
        }
        
        # Execute
        result = await storage_engine.store_interaction_memory(
            user_query, agent_response, user_id, agent_name, consciousness_context
        )
        
        # Verify
        assert result is not None
        assert isinstance(result, str)
        mock_embedding_manager.get_embedding.assert_called_once()
        mock_neo4j_manager.execute_write_query.assert_called()
    
    @pytest.mark.asyncio
    async def test_store_interaction_memory_long_content(self, storage_engine, mock_neo4j_manager, mock_embedding_manager):
        """Test interaction memory storage with content truncation"""
        # Setup mocks
        mock_embedding_manager.get_embedding.return_value = [0.1, 0.2, 0.3]
        mock_neo4j_manager.execute_write_query.return_value = [{"memory_id": "test_memory_id"}]
        
        # Create very long content
        long_query = "A" * 5000
        long_response = "B" * 5000
        
        result = await storage_engine.store_interaction_memory(
            long_query, long_response, "user", "agent", {"consciousness_level": 0.7}
        )
        
        assert result is not None
        # Verify embedding was called with truncated content
        call_args = mock_embedding_manager.get_embedding.call_args[0][0]
        assert len(call_args) <= storage_engine.max_content_length + 3  # +3 for "..."
    
    @pytest.mark.asyncio
    async def test_store_consciousness_memory_success(self, storage_engine, mock_neo4j_manager, mock_embedding_manager):
        """Test successful consciousness memory storage"""
        # Setup mocks
        mock_embedding_manager.get_embedding.return_value = [0.1, 0.2, 0.3]
        mock_neo4j_manager.execute_write_query.return_value = [{"memory_id": "test_memory_id"}]
        
        reflection_content = "I am reflecting on my understanding of consciousness..."
        consciousness_context = {
            "consciousness_level": 0.9,
            "emotional_state": "reflective"
        }
        
        result = await storage_engine.store_consciousness_memory(
            reflection_content, consciousness_context, "consciousness_reflection"
        )
        
        assert result is not None
        assert isinstance(result, str)
        mock_embedding_manager.get_embedding.assert_called_once_with(reflection_content)
    
    @pytest.mark.asyncio
    async def test_create_memory_node_success(self, storage_engine, mock_neo4j_manager):
        """Test successful memory node creation"""
        mock_neo4j_manager.execute_write_query.return_value = [{"memory_id": "test_memory_id"}]
        
        memory_record = MemoryRecord(
            memory_id="test_memory_id",
            content="Test content",
            memory_type="interaction",
            user_id="test_user",
            agent_name="test_agent",
            consciousness_level=0.7,
            emotional_state="neutral",
            importance_score=0.5,
            embedding=[0.1, 0.2, 0.3],
            created_at=datetime.now()
        )
        
        result = await storage_engine.create_memory_node(memory_record)
        
        assert result is True
        mock_neo4j_manager.execute_write_query.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_memory_node_failure(self, storage_engine, mock_neo4j_manager):
        """Test memory node creation failure"""
        mock_neo4j_manager.execute_write_query.return_value = []
        
        memory_record = MemoryRecord(
            memory_id="test_memory_id",
            content="Test content",
            memory_type="interaction",
            user_id="test_user",
            agent_name="test_agent",
            consciousness_level=0.7,
            emotional_state="neutral",
            importance_score=0.5,
            embedding=[0.1, 0.2, 0.3],
            created_at=datetime.now()
        )
        
        result = await storage_engine.create_memory_node(memory_record)
        
        assert result is False
    
    @pytest.mark.asyncio
    async def test_create_memory_node_exception(self, storage_engine, mock_neo4j_manager):
        """Test memory node creation with exception"""
        mock_neo4j_manager.execute_write_query.side_effect = Exception("Database error")
        
        memory_record = MemoryRecord(
            memory_id="test_memory_id",
            content="Test content",
            memory_type="interaction",
            user_id="test_user",
            agent_name="test_agent",
            consciousness_level=0.7,
            emotional_state="neutral",
            importance_score=0.5,
            embedding=[0.1, 0.2, 0.3],
            created_at=datetime.now()
        )
        
        with pytest.raises(MemoryStorageError):
            await storage_engine.create_memory_node(memory_record)
    
    @pytest.mark.asyncio
    async def test_link_memory_to_concepts_success(self, storage_engine, mock_neo4j_manager):
        """Test successful memory-concept linking"""
        mock_neo4j_manager.execute_write_query.return_value = [{"concepts_linked": 3}]
        
        result = await storage_engine.link_memory_to_concepts(
            "test_memory_id", ["ai", "machine learning", "consciousness"]
        )
        
        assert result is True
        mock_neo4j_manager.execute_write_query.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_link_memory_to_concepts_empty_list(self, storage_engine):
        """Test linking with empty concept list"""
        result = await storage_engine.link_memory_to_concepts("test_memory_id", [])
        
        assert result is True  # Should return True for empty list
    
    @pytest.mark.asyncio
    async def test_link_memory_to_concepts_failure(self, storage_engine, mock_neo4j_manager):
        """Test memory-concept linking failure"""
        mock_neo4j_manager.execute_write_query.return_value = []
        
        result = await storage_engine.link_memory_to_concepts(
            "test_memory_id", ["ai", "consciousness"]
        )
        
        assert result is False
    
    def test_calculate_interaction_importance_basic(self, storage_engine):
        """Test basic interaction importance calculation"""
        user_query = "What is AI?"
        agent_response = "AI is artificial intelligence."
        consciousness_context = {"consciousness_level": 0.7, "emotional_state": "neutral"}
        
        importance = storage_engine._calculate_interaction_importance(
            user_query, agent_response, consciousness_context
        )
        
        assert 0.1 <= importance <= 1.0
        assert isinstance(importance, float)
    
    def test_calculate_interaction_importance_complex_query(self, storage_engine):
        """Test importance calculation with complex query"""
        user_query = "How does machine learning work and what are the different types of algorithms?"
        agent_response = "Machine learning is a subset of AI that enables computers to learn..."
        consciousness_context = {"consciousness_level": 0.8, "emotional_state": "curious"}
        
        importance = storage_engine._calculate_interaction_importance(
            user_query, agent_response, consciousness_context
        )
        
        # Should be higher due to longer query, question mark, and curious state
        assert importance > 0.5
    
    def test_calculate_consciousness_importance_basic(self, storage_engine):
        """Test basic consciousness importance calculation"""
        content = "I am reflecting on my understanding."
        consciousness_context = {"consciousness_level": 0.8}
        memory_type = "consciousness_reflection"
        
        importance = storage_engine._calculate_consciousness_importance(
            content, consciousness_context, memory_type
        )
        
        assert 0.3 <= importance <= 1.0  # Consciousness memories have higher minimum
        assert isinstance(importance, float)
    
    def test_calculate_consciousness_importance_insight(self, storage_engine):
        """Test consciousness importance for insights"""
        content = "I realize that consciousness involves self-awareness and reflection."
        consciousness_context = {"consciousness_level": 0.9}
        memory_type = "insight"
        
        importance = storage_engine._calculate_consciousness_importance(
            content, consciousness_context, memory_type
        )
        
        # Should be higher due to insight type and insight keywords
        assert importance > 0.8
    
    def test_extract_concepts_from_text(self, storage_engine):
        """Test concept extraction from text"""
        text = "I am learning about artificial intelligence and machine learning algorithms."
        
        concepts = storage_engine._extract_concepts_from_text(text)
        
        assert isinstance(concepts, list)
        assert "ai" in concepts or "artificial intelligence" in concepts
        assert "machine learning" in concepts
        assert "algorithm" in concepts or "algorithms" in concepts
        assert len(concepts) <= 10  # Should be limited
    
    def test_extract_concepts_empty_text(self, storage_engine):
        """Test concept extraction from empty text"""
        concepts = storage_engine._extract_concepts_from_text("")
        
        assert concepts == []
    
    @pytest.mark.asyncio
    async def test_update_memory_importance_by_consciousness(self, storage_engine, mock_neo4j_manager):
        """Test updating memory importance based on consciousness changes"""
        mock_neo4j_manager.execute_write_query.return_value = [{"updated_count": 5}]
        
        consciousness_context = {
            "consciousness_level": 0.8,
            "emotional_state": "reflective"
        }
        
        result = await storage_engine.update_memory_importance_by_consciousness(
            consciousness_context, consciousness_delta=0.1
        )
        
        assert result == 5
        mock_neo4j_manager.execute_write_query.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_apply_emotional_influence_to_memories(self, storage_engine, mock_neo4j_manager):
        """Test applying emotional influence to memories"""
        mock_neo4j_manager.execute_write_query.return_value = [{"affected_count": 3}]
        
        consciousness_context = {"consciousness_level": 0.7}
        
        result = await storage_engine.apply_emotional_influence_to_memories(
            "excited", 0.8, consciousness_context
        )
        
        assert result == 3
        mock_neo4j_manager.execute_write_query.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_store_interaction_memory_embedding_failure(self, storage_engine, mock_neo4j_manager, mock_embedding_manager):
        """Test interaction memory storage when embedding generation fails"""
        # Setup embedding failure
        mock_embedding_manager.get_embedding.side_effect = Exception("Embedding service unavailable")
        
        with pytest.raises(MemoryStorageError):
            await storage_engine.store_interaction_memory(
                "test query", "test response", "user", "agent", {"consciousness_level": 0.7}
            )
    
    @pytest.mark.asyncio
    async def test_store_interaction_memory_neo4j_failure(self, storage_engine, mock_neo4j_manager, mock_embedding_manager):
        """Test interaction memory storage when Neo4j fails"""
        # Setup successful embedding but Neo4j failure
        mock_embedding_manager.get_embedding.return_value = [0.1, 0.2, 0.3]
        mock_neo4j_manager.execute_write_query.side_effect = Exception("Neo4j connection failed")
        
        with pytest.raises(MemoryStorageError):
            await storage_engine.store_interaction_memory(
                "test query", "test response", "user", "agent", {"consciousness_level": 0.7}
            )

class TestMemoryStorageEngineIntegration:
    """Integration tests for memory storage engine"""
    
    @pytest.fixture
    def storage_engine(self):
        """Create real storage engine for integration tests"""
        return MemoryStorageEngine()
    
    @pytest.mark.asyncio
    async def test_full_memory_storage_workflow(self, storage_engine):
        """Test complete memory storage workflow with mocked dependencies"""
        with patch.object(storage_engine, 'neo4j') as mock_neo4j, \
             patch.object(storage_engine, 'embedding') as mock_embedding:
            
            # Setup mocks
            mock_embedding.get_embedding.return_value = [0.1, 0.2, 0.3, 0.4, 0.5]
            mock_neo4j.execute_write_query.return_value = [{"memory_id": "test_memory_id"}]
            
            # Store interaction memory
            memory_id = await storage_engine.store_interaction_memory(
                user_query="What is consciousness?",
                agent_response="Consciousness is the state of being aware...",
                user_id="test_user",
                agent_name="consciousness_agent",
                consciousness_context={
                    "consciousness_level": 0.85,
                    "emotional_state": "curious"
                }
            )
            
            # Verify memory was stored
            assert memory_id is not None
            assert isinstance(memory_id, str)
            
            # Verify embedding was generated
            mock_embedding.get_embedding.assert_called_once()
            
            # Verify Neo4j was called
            assert mock_neo4j.execute_write_query.call_count >= 1
    
    @pytest.mark.asyncio
    async def test_consciousness_memory_workflow(self, storage_engine):
        """Test consciousness memory storage workflow"""
        with patch.object(storage_engine, 'neo4j') as mock_neo4j, \
             patch.object(storage_engine, 'embedding') as mock_embedding:
            
            # Setup mocks
            mock_embedding.get_embedding.return_value = [0.2, 0.4, 0.6, 0.8, 1.0]
            mock_neo4j.execute_write_query.return_value = [{"memory_id": "consciousness_memory_id"}]
            
            # Store consciousness memory
            memory_id = await storage_engine.store_consciousness_memory(
                reflection_content="I am becoming more aware of my thought processes...",
                consciousness_context={
                    "consciousness_level": 0.9,
                    "emotional_state": "reflective"
                },
                memory_type="insight"
            )
            
            # Verify memory was stored
            assert memory_id is not None
            assert isinstance(memory_id, str)
            
            # Verify higher importance for consciousness memories
            # This would be verified by checking the call arguments to Neo4j
            call_args = mock_neo4j.execute_write_query.call_args
            assert call_args is not None

if __name__ == "__main__":
    pytest.main([__file__])