"""
Comprehensive unit tests for Memory Context Builder
Tests context building functionality, memory formatting, and consciousness integration.
"""
import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from typing import Dict, Any, List

# Import the components to test
from backend.utils.memory_context_builder import (
    MemoryContextBuilder, MemoryContext, memory_context_builder
)
from backend.utils.memory_retrieval_engine import MemorySearchResult
from backend.utils.memory_error_handling import (
    MemoryContextError, MemoryError
)

class TestMemoryContext:
    """Test the MemoryContext dataclass"""
    
    def test_memory_context_creation(self):
        """Test basic memory context creation"""
        memories = [
            MemorySearchResult(
                memory_id="test_memory",
                content="Test content",
                memory_type="interaction",
                agent_name="test_agent",
                user_id="test_user",
                consciousness_level=0.7,
                emotional_state="neutral",
                importance_score=0.6,
                created_at="2024-01-01T12:00:00",
                metadata={},
                relevance_score=0.8
            )
        ]
        
        context = MemoryContext(
            relevant_memories=memories,
            conversation_history=[{"content": "test", "timestamp": "2024-01-01", "agent": "test"}],
            related_concepts=["ai", "consciousness"],
            context_strength=0.8,
            consciousness_alignment=0.7,
            temporal_relevance=0.9,
            formatted_context="Test formatted context"
        )
        
        assert len(context.relevant_memories) == 1
        assert len(context.conversation_history) == 1
        assert len(context.related_concepts) == 2
        assert context.context_strength == 0.8
        assert context.consciousness_alignment == 0.7
        assert context.temporal_relevance == 0.9
        assert context.formatted_context == "Test formatted context"
    
    def test_memory_context_defaults(self):
        """Test memory context with default metadata"""
        context = MemoryContext(
            relevant_memories=[],
            conversation_history=[],
            related_concepts=[],
            context_strength=0.0,
            consciousness_alignment=0.5,
            temporal_relevance=0.5,
            formatted_context=""
        )
        
        assert context.metadata == {}

class TestMemoryContextBuilder:
    """Test the MemoryContextBuilder class"""
    
    @pytest.fixture
    def mock_neo4j_manager(self):
        """Mock Neo4j manager"""
        mock = Mock()
        mock.execute_query = Mock(return_value=[])
        return mock
    
    @pytest.fixture
    def mock_memory_retrieval(self):
        """Mock memory retrieval engine"""
        mock = Mock()
        mock.get_relevant_memories = AsyncMock(return_value=[])
        mock.get_conversation_history = AsyncMock(return_value=[])
        return mock
    
    @pytest.fixture
    def context_builder(self, mock_neo4j_manager, mock_memory_retrieval):
        """Create context builder with mocked dependencies"""
        builder = MemoryContextBuilder()
        builder.neo4j = mock_neo4j_manager
        builder.memory_retrieval = mock_memory_retrieval
        return builder
    
    @pytest.fixture
    def sample_memories(self):
        """Sample memory search results for testing"""
        return [
            MemorySearchResult(
                memory_id="memory_1",
                content="User asked about AI and I explained artificial intelligence",
                memory_type="interaction",
                agent_name="simple_chat",
                user_id="test_user",
                consciousness_level=0.7,
                emotional_state="neutral",
                importance_score=0.6,
                created_at="2024-01-01T12:00:00",
                metadata={"user_query": "What is AI?", "agent_response": "AI is..."},
                relevance_score=0.8,
                similarity_score=0.75,
                temporal_score=0.9,
                consciousness_score=0.7
            ),
            MemorySearchResult(
                memory_id="memory_2",
                content="I reflected on consciousness and self-awareness",
                memory_type="consciousness_reflection",
                agent_name="consciousness_system",
                user_id="system",
                consciousness_level=0.9,
                emotional_state="reflective",
                importance_score=0.8,
                created_at="2024-01-01T11:00:00",
                metadata={},
                relevance_score=0.6,
                similarity_score=0.6,
                temporal_score=0.8,
                consciousness_score=0.9
            ),
            MemorySearchResult(
                memory_id="memory_3",
                content="Low relevance memory that should be filtered",
                memory_type="interaction",
                agent_name="test_agent",
                user_id="test_user",
                consciousness_level=0.5,
                emotional_state="neutral",
                importance_score=0.3,
                created_at="2024-01-01T10:00:00",
                metadata={},
                relevance_score=0.2,  # Below threshold
                similarity_score=0.2,
                temporal_score=0.7,
                consciousness_score=0.4
            )
        ]
    
    @pytest.mark.asyncio
    async def test_build_conversation_context_success(self, context_builder, sample_memories):
        """Test successful conversation context building"""
        consciousness_context = {"consciousness_level": 0.7, "emotional_state": "neutral"}
        
        context = await context_builder.build_conversation_context(
            memories=sample_memories,
            consciousness_context=consciousness_context,
            context_type="conversation"
        )
        
        assert isinstance(context, str)
        assert len(context) > 0
        # Should filter out low relevance memories
        assert "Low relevance memory" not in context
    
    @pytest.mark.asyncio
    async def test_build_conversation_context_empty_memories(self, context_builder):
        """Test conversation context building with empty memories"""
        consciousness_context = {"consciousness_level": 0.7}
        
        context = await context_builder.build_conversation_context(
            memories=[],
            consciousness_context=consciousness_context
        )
        
        assert context == ""
    
    @pytest.mark.asyncio
    async def test_build_conversation_context_no_relevant_memories(self, context_builder):
        """Test conversation context building when no memories meet threshold"""
        low_relevance_memories = [
            MemorySearchResult(
                memory_id="low_memory",
                content="Low relevance content",
                memory_type="interaction",
                agent_name="agent",
                user_id="user",
                consciousness_level=0.5,
                emotional_state="neutral",
                importance_score=0.3,
                created_at="2024-01-01T12:00:00",
                metadata={},
                relevance_score=0.1  # Below threshold
            )
        ]
        
        consciousness_context = {"consciousness_level": 0.7}
        
        context = await context_builder.build_conversation_context(
            memories=low_relevance_memories,
            consciousness_context=consciousness_context
        )
        
        assert context == ""
    
    @pytest.mark.asyncio
    async def test_build_knowledge_context_success(self, context_builder, sample_memories, mock_neo4j_manager):
        """Test successful knowledge context building"""
        # Mock concept extraction
        mock_concepts = [
            {"name": "artificial_intelligence", "description": "AI concept", "importance": 0.8},
            {"name": "consciousness", "description": "Consciousness concept", "importance": 0.9}
        ]
        mock_neo4j_manager.execute_query.return_value = [{"concept": concept} for concept in mock_concepts]
        
        related_concepts = [
            {"name": "machine_learning", "importance": 0.7},
            {"name": "neural_networks", "importance": 0.6}
        ]
        
        consciousness_context = {"consciousness_level": 0.8, "emotional_state": "curious"}
        
        context = await context_builder.build_knowledge_context(
            memories=sample_memories,
            related_concepts=related_concepts,
            consciousness_context=consciousness_context
        )
        
        assert isinstance(context, str)
        assert len(context) > 0
    
    @pytest.mark.asyncio
    async def test_build_knowledge_context_empty_inputs(self, context_builder):
        """Test knowledge context building with empty inputs"""
        consciousness_context = {"consciousness_level": 0.7}
        
        context = await context_builder.build_knowledge_context(
            memories=[],
            related_concepts=[],
            consciousness_context=consciousness_context
        )
        
        assert context == ""
    
    @pytest.mark.asyncio
    async def test_calculate_context_relevance(self, context_builder, sample_memories):
        """Test context relevance calculation"""
        current_query = "Tell me about artificial intelligence"
        consciousness_context = {"consciousness_level": 0.7, "emotional_state": "curious"}
        
        enhanced_memories = await context_builder.calculate_context_relevance(
            memories=sample_memories,
            current_query=current_query,
            consciousness_context=consciousness_context
        )
        
        assert len(enhanced_memories) == len(sample_memories)
        assert all(isinstance(m, MemorySearchResult) for m in enhanced_memories)
        # Should be sorted by relevance
        assert enhanced_memories[0].relevance_score >= enhanced_memories[1].relevance_score
    
    @pytest.mark.asyncio
    async def test_calculate_context_relevance_empty_memories(self, context_builder):
        """Test context relevance calculation with empty memories"""
        enhanced_memories = await context_builder.calculate_context_relevance(
            memories=[],
            current_query="test query",
            consciousness_context={"consciousness_level": 0.7}
        )
        
        assert enhanced_memories == []
    
    def test_format_memory_for_context_interaction(self, context_builder, sample_memories):
        """Test formatting interaction memory for context"""
        interaction_memory = sample_memories[0]  # First memory is interaction type
        
        formatted = context_builder.format_memory_for_context(
            memory=interaction_memory,
            context_type="conversation"
        )
        
        assert isinstance(formatted, str)
        assert len(formatted) > 0
        assert "What is AI?" in formatted  # Should include user query from metadata
    
    def test_format_memory_for_context_consciousness(self, context_builder, sample_memories):
        """Test formatting consciousness memory for context"""
        consciousness_memory = sample_memories[1]  # Second memory is consciousness type
        
        formatted = context_builder.format_memory_for_context(
            memory=consciousness_memory,
            context_type="conversation"
        )
        
        assert isinstance(formatted, str)
        assert len(formatted) > 0
        assert "I previously reflected" in formatted
    
    def test_format_memory_for_context_with_metadata(self, context_builder, sample_memories):
        """Test formatting memory with metadata inclusion"""
        memory = sample_memories[0]
        
        formatted = context_builder.format_memory_for_context(
            memory=memory,
            context_type="conversation",
            include_metadata=True
        )
        
        assert isinstance(formatted, str)
        assert "Relevance:" in formatted
    
    @pytest.mark.asyncio
    async def test_build_comprehensive_context_success(self, context_builder, mock_memory_retrieval, mock_neo4j_manager):
        """Test comprehensive context building"""
        # Setup mocks
        mock_memories = [
            MemorySearchResult(
                memory_id="comprehensive_memory",
                content="Comprehensive test memory",
                memory_type="interaction",
                agent_name="test_agent",
                user_id="test_user",
                consciousness_level=0.8,
                emotional_state="curious",
                importance_score=0.7,
                created_at="2024-01-01T12:00:00",
                metadata={"user_query": "test query"},
                relevance_score=0.8
            )
        ]
        
        mock_memory_retrieval.get_relevant_memories.return_value = mock_memories
        mock_memory_retrieval.get_conversation_history.return_value = mock_memories
        mock_neo4j_manager.execute_query.return_value = [
            {"concept": {"name": "test_concept", "importance": 0.8}}
        ]
        
        query = "Tell me about AI"
        user_id = "test_user"
        consciousness_context = {"consciousness_level": 0.8, "emotional_state": "curious"}
        
        context = await context_builder.build_comprehensive_context(
            query=query,
            user_id=user_id,
            consciousness_context=consciousness_context,
            include_concepts=True,
            context_type="hybrid"
        )
        
        assert isinstance(context, MemoryContext)
        assert len(context.relevant_memories) > 0
        assert len(context.conversation_history) > 0
        assert context.context_strength > 0
        assert context.consciousness_alignment > 0
        assert context.temporal_relevance > 0
        assert len(context.formatted_context) > 0
    
    @pytest.mark.asyncio
    async def test_build_comprehensive_context_error_handling(self, context_builder, mock_memory_retrieval):
        """Test comprehensive context building with error handling"""
        # Setup mock to raise exception
        mock_memory_retrieval.get_relevant_memories.side_effect = Exception("Retrieval failed")
        
        context = await context_builder.build_comprehensive_context(
            query="test query",
            user_id="test_user",
            consciousness_context={"consciousness_level": 0.7}
        )
        
        # Should return empty context on error
        assert isinstance(context, MemoryContext)
        assert len(context.relevant_memories) == 0
        assert context.context_strength == 0.0
        assert "error" in context.metadata
    
    def test_extract_conversation_history(self, context_builder, sample_memories):
        """Test conversation history extraction from memories"""
        conversation_history = context_builder._extract_conversation_history(sample_memories)
        
        # Should only extract interaction memories
        assert len(conversation_history) == 1  # Only one interaction memory in sample
        assert conversation_history[0]["user_query"] == "What is AI?"
        assert "agent_response" in conversation_history[0]
    
    @pytest.mark.asyncio
    async def test_extract_concepts_from_memories(self, context_builder, sample_memories, mock_neo4j_manager):
        """Test concept extraction from memories"""
        mock_concepts = [
            {"name": "artificial_intelligence", "memory_connections": 2, "importance": 0.8},
            {"name": "consciousness", "memory_connections": 1, "importance": 0.9}
        ]
        mock_neo4j_manager.execute_query.return_value = [{"concept": concept} for concept in mock_concepts]
        
        concepts = await context_builder._extract_concepts_from_memories(sample_memories)
        
        assert len(concepts) == 2
        assert concepts[0]["name"] == "artificial_intelligence"
        assert concepts[1]["name"] == "consciousness"
    
    @pytest.mark.asyncio
    async def test_extract_concepts_from_memories_empty(self, context_builder):
        """Test concept extraction with empty memories"""
        concepts = await context_builder._extract_concepts_from_memories([])
        
        assert concepts == []
    
    def test_merge_concept_lists(self, context_builder):
        """Test merging and deduplicating concept lists"""
        memory_concepts = [
            {"name": "ai", "importance": 0.8},
            {"name": "consciousness", "importance": 0.9}
        ]
        
        related_concepts = [
            {"name": "machine_learning", "importance": 0.7},
            {"name": "ai", "importance": 0.6}  # Duplicate, should not overwrite
        ]
        
        merged = context_builder._merge_concept_lists(memory_concepts, related_concepts)
        
        assert len(merged) == 3  # ai, consciousness, machine_learning
        # Memory concepts should take priority
        ai_concept = next(c for c in merged if c["name"] == "ai")
        assert ai_concept["importance"] == 0.8  # From memory_concepts, not related_concepts
    
    def test_calculate_query_alignment(self, context_builder):
        """Test query alignment calculation"""
        memory_content = "artificial intelligence machine learning algorithms"
        query = "machine learning AI"
        
        alignment = context_builder._calculate_query_alignment(memory_content, query)
        
        assert 0.0 <= alignment <= 1.0
        assert alignment > 0  # Should have some overlap
    
    def test_calculate_query_alignment_no_overlap(self, context_builder):
        """Test query alignment with no keyword overlap"""
        memory_content = "completely different topic"
        query = "artificial intelligence"
        
        alignment = context_builder._calculate_query_alignment(memory_content, query)
        
        assert alignment == 0.0
    
    def test_calculate_consciousness_alignment(self, context_builder):
        """Test consciousness alignment calculation"""
        # Perfect alignment
        perfect_alignment = context_builder._calculate_consciousness_alignment(
            memory_consciousness=0.8,
            memory_emotion="curious",
            current_consciousness=0.8,
            current_emotion="curious"
        )
        
        # Partial alignment
        partial_alignment = context_builder._calculate_consciousness_alignment(
            memory_consciousness=0.6,
            memory_emotion="neutral",
            current_consciousness=0.8,
            current_emotion="curious"
        )
        
        assert 0.0 <= perfect_alignment <= 1.0
        assert 0.0 <= partial_alignment <= 1.0
        assert perfect_alignment > partial_alignment
    
    def test_calculate_temporal_relevance(self, context_builder):
        """Test temporal relevance calculation"""
        # Recent memory
        recent_time = datetime.now().isoformat()
        recent_relevance = context_builder._calculate_temporal_relevance(recent_time)
        
        # Old memory
        old_time = (datetime.now() - timedelta(weeks=2)).isoformat()
        old_relevance = context_builder._calculate_temporal_relevance(old_time)
        
        assert 0.1 <= recent_relevance <= 1.0
        assert 0.1 <= old_relevance <= 1.0
        assert recent_relevance > old_relevance
    
    def test_get_memory_type_importance(self, context_builder):
        """Test memory type importance multipliers"""
        interaction_importance = context_builder._get_memory_type_importance("interaction")
        consciousness_importance = context_builder._get_memory_type_importance("consciousness_reflection")
        insight_importance = context_builder._get_memory_type_importance("insight")
        unknown_importance = context_builder._get_memory_type_importance("unknown_type")
        
        assert interaction_importance == 1.0
        assert consciousness_importance > interaction_importance
        assert insight_importance > consciousness_importance
        assert unknown_importance == 1.0  # Default
    
    def test_calculate_context_strength(self, context_builder, sample_memories):
        """Test context strength calculation"""
        # High relevance memories
        high_relevance_memories = [m for m in sample_memories if m.relevance_score >= 0.6]
        strength = context_builder._calculate_context_strength(high_relevance_memories)
        
        assert 0.0 <= strength <= 1.0
        assert strength > 0
        
        # Empty memories
        empty_strength = context_builder._calculate_context_strength([])
        assert empty_strength == 0.0
    
    def test_calculate_avg_consciousness_alignment(self, context_builder, sample_memories):
        """Test average consciousness alignment calculation"""
        consciousness_context = {"consciousness_level": 0.8, "emotional_state": "curious"}
        
        avg_alignment = context_builder._calculate_avg_consciousness_alignment(
            sample_memories, consciousness_context
        )
        
        assert 0.0 <= avg_alignment <= 1.0
        
        # Empty memories
        empty_alignment = context_builder._calculate_avg_consciousness_alignment(
            [], consciousness_context
        )
        assert empty_alignment == 0.5
    
    def test_calculate_avg_temporal_relevance(self, context_builder, sample_memories):
        """Test average temporal relevance calculation"""
        avg_relevance = context_builder._calculate_avg_temporal_relevance(sample_memories)
        
        assert 0.0 <= avg_relevance <= 1.0
        
        # Empty memories
        empty_relevance = context_builder._calculate_avg_temporal_relevance([])
        assert empty_relevance == 0.5
    
    def test_prepare_template_data(self, context_builder, sample_memories):
        """Test template data preparation"""
        context_data = {
            "memories": sample_memories[:1],
            "concepts": [{"name": "ai"}, {"name": "consciousness"}],
            "consciousness_level": 0.8,
            "emotional_state": "curious"
        }
        
        prepared = context_builder._prepare_template_data(context_data)
        
        assert isinstance(prepared, dict)
        assert "memories" in prepared
        assert "concepts" in prepared
        assert prepared["consciousness_level"] == "0.8"
        assert prepared["emotional_state"] == "curious"
        assert "ai, consciousness" in prepared["concepts"]
    
    def test_context_templates(self, context_builder):
        """Test context template retrieval"""
        conversation_template = context_builder._get_conversation_template()
        knowledge_template = context_builder._get_knowledge_template()
        reflection_template = context_builder._get_reflection_template()
        hybrid_template = context_builder._get_hybrid_template()
        
        assert isinstance(conversation_template, str)
        assert isinstance(knowledge_template, str)
        assert isinstance(reflection_template, str)
        assert isinstance(hybrid_template, str)
        
        # Templates should contain placeholders
        assert "{memories}" in conversation_template
        assert "{concepts}" in knowledge_template
        assert "{memories}" in reflection_template
        assert "{interaction_memories}" in hybrid_template
    
    @pytest.mark.asyncio
    async def test_build_hybrid_context(self, context_builder, sample_memories):
        """Test hybrid context building"""
        concepts = [{"name": "ai"}, {"name": "consciousness"}]
        consciousness_context = {"consciousness_level": 0.8, "emotional_state": "reflective"}
        
        hybrid_context = await context_builder._build_hybrid_context(
            memories=sample_memories,
            concepts=concepts,
            consciousness_context=consciousness_context
        )
        
        assert isinstance(hybrid_context, str)
        assert len(hybrid_context) > 0

class TestMemoryContextBuilderIntegration:
    """Integration tests for memory context builder"""
    
    @pytest.fixture
    def context_builder(self):
        """Create real context builder for integration tests"""
        return MemoryContextBuilder()
    
    @pytest.mark.asyncio
    async def test_full_context_building_workflow(self, context_builder):
        """Test complete context building workflow with mocked dependencies"""
        with patch.object(context_builder, 'neo4j') as mock_neo4j, \
             patch.object(context_builder, 'memory_retrieval') as mock_retrieval:
            
            # Setup mocks
            mock_memories = [
                MemorySearchResult(
                    memory_id="integration_memory",
                    content="Integration test memory content",
                    memory_type="interaction",
                    agent_name="test_agent",
                    user_id="test_user",
                    consciousness_level=0.8,
                    emotional_state="curious",
                    importance_score=0.7,
                    created_at="2024-01-01T12:00:00",
                    metadata={"user_query": "integration test"},
                    relevance_score=0.8
                )
            ]
            
            mock_retrieval.get_relevant_memories.return_value = mock_memories
            mock_retrieval.get_conversation_history.return_value = mock_memories
            mock_neo4j.execute_query.return_value = [
                {"concept": {"name": "integration", "importance": 0.8}}
            ]
            
            # Build comprehensive context
            context = await context_builder.build_comprehensive_context(
                query="integration test query",
                user_id="test_user",
                consciousness_context={"consciousness_level": 0.8, "emotional_state": "curious"},
                include_concepts=True,
                context_type="hybrid"
            )
            
            # Verify comprehensive context
            assert isinstance(context, MemoryContext)
            assert len(context.relevant_memories) > 0
            assert context.context_strength > 0
            assert len(context.formatted_context) > 0
            assert context.metadata["query"] == "integration test query"

def test_global_instance():
    """Test that global memory_context_builder instance exists"""
    assert memory_context_builder is not None
    assert isinstance(memory_context_builder, MemoryContextBuilder)

if __name__ == "__main__":
    pytest.main([__file__])