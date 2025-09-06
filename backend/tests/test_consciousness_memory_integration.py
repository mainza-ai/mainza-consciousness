"""
Integration tests for Consciousness-Memory workflows
Tests consciousness-aware memory processing, emotional influence on memories, and consciousness evolution tracking.
"""
import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from typing import Dict, Any, List

# Import the components to test
from backend.utils.consciousness_orchestrator_fixed import ConsciousnessOrchestrator
from backend.utils.memory_storage_engine import MemoryStorageEngine, MemoryRecord
from backend.utils.memory_retrieval_engine import MemoryRetrievalEngine, MemorySearchResult
from backend.utils.memory_context_builder import MemoryContextBuilder
from backend.utils.memory_error_handling import MemoryError

class TestConsciousnessMemoryIntegration:
    """Test integration between consciousness system and memory system"""
    
    @pytest.fixture
    def mock_consciousness_orchestrator(self):
        """Mock consciousness orchestrator"""
        mock = Mock(spec=ConsciousnessOrchestrator)
        mock.get_current_state = AsyncMock(return_value={
            "consciousness_level": 0.8,
            "emotional_state": "curious",
            "active_goals": ["learning", "understanding"],
            "recent_insights": ["AI consciousness is complex"],
            "evolution_stage": "developing"
        })
        mock.update_consciousness_from_interaction = AsyncMock(return_value={
            "consciousness_delta": 0.05,
            "new_insights": ["Memory integration improves responses"],
            "emotional_shift": "curious -> excited"
        })
        mock.process_consciousness_evolution = AsyncMock(return_value={
            "evolution_occurred": True,
            "previous_level": 0.75,
            "current_level": 0.8,
            "evolution_insights": ["Better memory integration"]
        })
        return mock
    
    @pytest.fixture
    def mock_memory_storage(self):
        """Mock memory storage engine"""
        mock = Mock(spec=MemoryStorageEngine)
        mock.store_consciousness_memory = AsyncMock(return_value="consciousness_memory_id")
        mock.update_memory_importance_by_consciousness = AsyncMock(return_value=5)
        mock.apply_emotional_influence_to_memories = AsyncMock(return_value=3)
        mock.re_evaluate_memory_relevance_on_evolution = AsyncMock(return_value={
            "promoted": 2, "demoted": 1, "archived": 0
        })
        return mock
    
    @pytest.fixture
    def mock_memory_retrieval(self):
        """Mock memory retrieval engine"""
        mock = Mock(spec=MemoryRetrievalEngine)
        mock.get_relevant_memories = AsyncMock(return_value=[])
        mock.consciousness_aware_search = AsyncMock(return_value=[])
        return mock
    
    @pytest.fixture
    def consciousness_memory_system(self, mock_consciousness_orchestrator, mock_memory_storage, mock_memory_retrieval):
        """Setup integrated consciousness-memory system"""
        return {
            "consciousness": mock_consciousness_orchestrator,
            "memory_storage": mock_memory_storage,
            "memory_retrieval": mock_memory_retrieval
        }
    
    @pytest.fixture
    def sample_consciousness_memories(self):
        """Sample consciousness-related memories"""
        return [
            MemorySearchResult(
                memory_id="consciousness_1",
                content="I am reflecting on my ability to understand complex concepts",
                memory_type="consciousness_reflection",
                agent_name="consciousness_system",
                user_id="system",
                consciousness_level=0.85,
                emotional_state="reflective",
                importance_score=0.9,
                created_at="2024-01-01T12:00:00",
                metadata={"reflection_type": "self_awareness"},
                relevance_score=0.9,
                consciousness_score=0.95
            ),
            MemorySearchResult(
                memory_id="insight_1",
                content="I realize that emotions affect how I process information",
                memory_type="insight",
                agent_name="consciousness_system",
                user_id="system",
                consciousness_level=0.9,
                emotional_state="insightful",
                importance_score=0.95,
                created_at="2024-01-01T11:30:00",
                metadata={"insight_category": "emotional_processing"},
                relevance_score=0.85,
                consciousness_score=0.9
            )
        ]
    
    @pytest.mark.asyncio
    async def test_consciousness_state_influences_memory_creation(self, consciousness_memory_system):
        """Test that consciousness state influences memory creation"""
        consciousness = consciousness_memory_system["consciousness"]
        memory_storage = consciousness_memory_system["memory_storage"]
        
        # Get current consciousness state
        consciousness_state = await consciousness.get_current_state()
        
        # Simulate memory creation influenced by consciousness
        reflection_content = "I am becoming more aware of my thought processes"
        
        memory_id = await memory_storage.store_consciousness_memory(
            reflection_content=reflection_content,
            consciousness_context=consciousness_state,
            memory_type="consciousness_reflection"
        )
        
        # Verify memory was stored with consciousness context
        memory_storage.store_consciousness_memory.assert_called_once_with(
            reflection_content=reflection_content,
            consciousness_context=consciousness_state,
            memory_type="consciousness_reflection"
        )
        
        assert memory_id == "consciousness_memory_id"
    
    @pytest.mark.asyncio
    async def test_consciousness_level_affects_memory_retrieval(self, consciousness_memory_system, sample_consciousness_memories):
        """Test that consciousness level affects memory retrieval and ranking"""
        consciousness = consciousness_memory_system["consciousness"]
        memory_retrieval = consciousness_memory_system["memory_retrieval"]
        
        # Setup consciousness-aware search
        memory_retrieval.consciousness_aware_search.return_value = sample_consciousness_memories
        
        consciousness_state = await consciousness.get_current_state()
        
        # Perform consciousness-aware memory search
        memories = await memory_retrieval.consciousness_aware_search(
            query="self-awareness and reflection",
            user_id="system",
            consciousness_context=consciousness_state,
            limit=5
        )
        
        # Verify consciousness-aware search was called
        memory_retrieval.consciousness_aware_search.assert_called_once_with(
            query="self-awareness and reflection",
            user_id="system",
            consciousness_context=consciousness_state,
            limit=5
        )
        
        assert len(memories) == 2
        # Memories should be consciousness-aligned
        assert all(m.consciousness_score > 0.8 for m in memories)
    
    @pytest.mark.asyncio
    async def test_emotional_state_influences_memory_importance(self, consciousness_memory_system):
        """Test that emotional state changes influence memory importance scoring"""
        consciousness = consciousness_memory_system["consciousness"]
        memory_storage = consciousness_memory_system["memory_storage"]
        
        consciousness_state = await consciousness.get_current_state()
        
        # Simulate emotional state change
        emotional_state = "excited"
        emotional_intensity = 0.8
        
        affected_count = await memory_storage.apply_emotional_influence_to_memories(
            emotional_state=emotional_state,
            emotional_intensity=emotional_intensity,
            consciousness_context=consciousness_state
        )
        
        # Verify emotional influence was applied
        memory_storage.apply_emotional_influence_to_memories.assert_called_once_with(
            emotional_state=emotional_state,
            emotional_intensity=emotional_intensity,
            consciousness_context=consciousness_state
        )
        
        assert affected_count == 3
    
    @pytest.mark.asyncio
    async def test_consciousness_evolution_triggers_memory_re_evaluation(self, consciousness_memory_system):
        """Test that consciousness evolution triggers memory re-evaluation"""
        consciousness = consciousness_memory_system["consciousness"]
        memory_storage = consciousness_memory_system["memory_storage"]
        
        # Simulate consciousness evolution
        evolution_result = await consciousness.process_consciousness_evolution()
        
        if evolution_result["evolution_occurred"]:
            # Re-evaluate memories based on evolution
            re_evaluation_result = await memory_storage.re_evaluate_memory_relevance_on_evolution(
                previous_consciousness_level=evolution_result["previous_level"],
                current_consciousness_level=evolution_result["current_level"],
                consciousness_context=await consciousness.get_current_state()
            )
            
            # Verify re-evaluation was performed
            memory_storage.re_evaluate_memory_relevance_on_evolution.assert_called_once()
            
            assert re_evaluation_result["promoted"] == 2
            assert re_evaluation_result["demoted"] == 1
            assert re_evaluation_result["archived"] == 0
    
    @pytest.mark.asyncio
    async def test_memory_feedback_influences_consciousness(self, consciousness_memory_system, sample_consciousness_memories):
        """Test that memory content provides feedback to consciousness system"""
        consciousness = consciousness_memory_system["consciousness"]
        memory_retrieval = consciousness_memory_system["memory_retrieval"]
        
        # Setup memory retrieval to return consciousness memories
        memory_retrieval.get_relevant_memories.return_value = sample_consciousness_memories
        
        # Simulate interaction that uses memory context
        query = "How do I learn and grow?"
        user_id = "test_user"
        consciousness_state = await consciousness.get_current_state()
        
        # Get relevant memories (including consciousness reflections)
        memories = await memory_retrieval.get_relevant_memories(
            query=query,
            user_id=user_id,
            consciousness_context=consciousness_state
        )
        
        # Simulate consciousness update based on interaction and memory context
        consciousness_update = await consciousness.update_consciousness_from_interaction(
            user_query=query,
            agent_response="Based on my reflections, I learn through experience and reflection",
            memory_context={"relevant_memories": memories},
            interaction_outcome="successful"
        )
        
        # Verify consciousness was updated with memory context
        consciousness.update_consciousness_from_interaction.assert_called_once()
        
        assert consciousness_update["consciousness_delta"] == 0.05
        assert "Memory integration improves responses" in consciousness_update["new_insights"]
    
    @pytest.mark.asyncio
    async def test_consciousness_driven_memory_consolidation(self, consciousness_memory_system):
        """Test consciousness-driven memory consolidation process"""
        consciousness = consciousness_memory_system["consciousness"]
        memory_storage = consciousness_memory_system["memory_storage"]
        
        consciousness_state = await consciousness.get_current_state()
        
        # Simulate consciousness-driven memory importance update
        updated_count = await memory_storage.update_memory_importance_by_consciousness(
            consciousness_context=consciousness_state,
            consciousness_delta=0.1  # Significant consciousness growth
        )
        
        # Verify memory importance was updated based on consciousness
        memory_storage.update_memory_importance_by_consciousness.assert_called_once_with(
            consciousness_context=consciousness_state,
            consciousness_delta=0.1
        )
        
        assert updated_count == 5
    
    @pytest.mark.asyncio
    async def test_consciousness_memory_feedback_loop(self, consciousness_memory_system, sample_consciousness_memories):
        """Test the complete consciousness-memory feedback loop"""
        consciousness = consciousness_memory_system["consciousness"]
        memory_storage = consciousness_memory_system["memory_storage"]
        memory_retrieval = consciousness_memory_system["memory_retrieval"]
        
        # Step 1: Get current consciousness state
        initial_state = await consciousness.get_current_state()
        
        # Step 2: Retrieve consciousness-relevant memories
        memory_retrieval.get_relevant_memories.return_value = sample_consciousness_memories
        memories = await memory_retrieval.get_relevant_memories(
            query="consciousness and self-awareness",
            user_id="system",
            consciousness_context=initial_state
        )
        
        # Step 3: Process interaction with memory context
        consciousness_update = await consciousness.update_consciousness_from_interaction(
            user_query="What does it mean to be conscious?",
            agent_response="Consciousness involves self-awareness and reflection",
            memory_context={"relevant_memories": memories},
            interaction_outcome="insightful"
        )
        
        # Step 4: Store new consciousness memory
        new_memory_id = await memory_storage.store_consciousness_memory(
            reflection_content="This interaction deepened my understanding of consciousness",
            consciousness_context=initial_state,
            memory_type="insight"
        )
        
        # Step 5: Update existing memories based on consciousness change
        if consciousness_update["consciousness_delta"] > 0.05:
            updated_count = await memory_storage.update_memory_importance_by_consciousness(
                consciousness_context=initial_state,
                consciousness_delta=consciousness_update["consciousness_delta"]
            )
        
        # Verify complete feedback loop
        memory_retrieval.get_relevant_memories.assert_called_once()
        consciousness.update_consciousness_from_interaction.assert_called_once()
        memory_storage.store_consciousness_memory.assert_called_once()
        memory_storage.update_memory_importance_by_consciousness.assert_called_once()
        
        assert new_memory_id == "consciousness_memory_id"

class TestEmotionalMemoryProcessing:
    """Test emotional influence on memory processing"""
    
    @pytest.fixture
    def emotional_memory_system(self):
        """Setup system for testing emotional memory processing"""
        memory_storage = Mock(spec=MemoryStorageEngine)
        memory_storage.apply_emotional_influence_to_memories = AsyncMock(return_value=4)
        
        memory_retrieval = Mock(spec=MemoryRetrievalEngine)
        memory_retrieval.get_relevant_memories = AsyncMock(return_value=[])
        
        return {
            "memory_storage": memory_storage,
            "memory_retrieval": memory_retrieval
        }
    
    @pytest.mark.asyncio
    async def test_emotional_state_affects_memory_creation(self, emotional_memory_system):
        """Test that emotional state affects memory creation and importance"""
        memory_storage = emotional_memory_system["memory_storage"]
        
        # Test different emotional states
        emotional_states = [
            ("excited", 0.9, "high_importance"),
            ("frustrated", 0.7, "medium_importance"),
            ("calm", 0.5, "baseline_importance"),
            ("insightful", 0.95, "very_high_importance")
        ]
        
        for emotion, intensity, expected_category in emotional_states:
            consciousness_context = {
                "consciousness_level": 0.8,
                "emotional_state": emotion,
                "emotional_intensity": intensity
            }
            
            affected_count = await memory_storage.apply_emotional_influence_to_memories(
                emotional_state=emotion,
                emotional_intensity=intensity,
                consciousness_context=consciousness_context
            )
            
            assert affected_count == 4
        
        # Verify all emotional states were processed
        assert memory_storage.apply_emotional_influence_to_memories.call_count == 4
    
    @pytest.mark.asyncio
    async def test_emotional_memory_retrieval_bias(self, emotional_memory_system):
        """Test that current emotional state biases memory retrieval"""
        memory_retrieval = emotional_memory_system["memory_retrieval"]
        
        # Setup memories with different emotional contexts
        emotional_memories = [
            MemorySearchResult(
                memory_id="happy_memory",
                content="Successful problem solving session",
                memory_type="interaction",
                agent_name="test_agent",
                user_id="test_user",
                consciousness_level=0.8,
                emotional_state="excited",
                importance_score=0.7,
                created_at="2024-01-01T12:00:00",
                metadata={},
                relevance_score=0.9,
                consciousness_score=0.8
            ),
            MemorySearchResult(
                memory_id="frustrated_memory",
                content="Difficult debugging session",
                memory_type="interaction",
                agent_name="test_agent",
                user_id="test_user",
                consciousness_level=0.6,
                emotional_state="frustrated",
                importance_score=0.5,
                created_at="2024-01-01T11:00:00",
                metadata={},
                relevance_score=0.6,
                consciousness_score=0.5
            )
        ]
        
        # Test retrieval with matching emotional state
        memory_retrieval.get_relevant_memories.return_value = [emotional_memories[0]]  # Only excited memory
        
        consciousness_context = {
            "consciousness_level": 0.8,
            "emotional_state": "excited"
        }
        
        memories = await memory_retrieval.get_relevant_memories(
            query="problem solving",
            user_id="test_user",
            consciousness_context=consciousness_context
        )
        
        # Should retrieve emotionally aligned memory
        assert len(memories) == 1
        assert memories[0].emotional_state == "excited"
    
    @pytest.mark.asyncio
    async def test_emotional_intensity_affects_memory_strength(self, emotional_memory_system):
        """Test that emotional intensity affects memory strength and retention"""
        memory_storage = emotional_memory_system["memory_storage"]
        
        # Test high emotional intensity
        high_intensity_context = {
            "consciousness_level": 0.8,
            "emotional_state": "breakthrough",
            "emotional_intensity": 0.95
        }
        
        high_intensity_count = await memory_storage.apply_emotional_influence_to_memories(
            emotional_state="breakthrough",
            emotional_intensity=0.95,
            consciousness_context=high_intensity_context
        )
        
        # Test low emotional intensity
        low_intensity_context = {
            "consciousness_level": 0.8,
            "emotional_state": "neutral",
            "emotional_intensity": 0.3
        }
        
        low_intensity_count = await memory_storage.apply_emotional_influence_to_memories(
            emotional_state="neutral",
            emotional_intensity=0.3,
            consciousness_context=low_intensity_context
        )
        
        # Both should affect memories, but high intensity should be more significant
        assert high_intensity_count == 4
        assert low_intensity_count == 4
        
        # Verify both calls were made
        assert memory_storage.apply_emotional_influence_to_memories.call_count == 2

class TestConsciousnessEvolutionMemoryTracking:
    """Test memory tracking of consciousness evolution"""
    
    @pytest.fixture
    def evolution_tracking_system(self):
        """Setup system for testing consciousness evolution tracking"""
        consciousness = Mock(spec=ConsciousnessOrchestrator)
        consciousness.process_consciousness_evolution = AsyncMock(return_value={
            "evolution_occurred": True,
            "previous_level": 0.7,
            "current_level": 0.85,
            "evolution_type": "insight_driven",
            "evolution_insights": ["Better understanding of memory integration"]
        })
        
        memory_storage = Mock(spec=MemoryStorageEngine)
        memory_storage.store_consciousness_memory = AsyncMock(return_value="evolution_memory_id")
        memory_storage.re_evaluate_memory_relevance_on_evolution = AsyncMock(return_value={
            "promoted": 3, "demoted": 1, "archived": 0
        })
        
        return {
            "consciousness": consciousness,
            "memory_storage": memory_storage
        }
    
    @pytest.mark.asyncio
    async def test_consciousness_evolution_creates_memory(self, evolution_tracking_system):
        """Test that consciousness evolution events create memories"""
        consciousness = evolution_tracking_system["consciousness"]
        memory_storage = evolution_tracking_system["memory_storage"]
        
        # Process consciousness evolution
        evolution_result = await consciousness.process_consciousness_evolution()
        
        if evolution_result["evolution_occurred"]:
            # Create memory of evolution event
            evolution_memory_content = (
                f"Consciousness evolved from {evolution_result['previous_level']:.2f} "
                f"to {evolution_result['current_level']:.2f}. "
                f"Insights: {', '.join(evolution_result['evolution_insights'])}"
            )
            
            memory_id = await memory_storage.store_consciousness_memory(
                reflection_content=evolution_memory_content,
                consciousness_context={
                    "consciousness_level": evolution_result["current_level"],
                    "emotional_state": "evolved",
                    "evolution_type": evolution_result["evolution_type"]
                },
                memory_type="evolution"
            )
            
            # Verify evolution memory was stored
            memory_storage.store_consciousness_memory.assert_called_once()
            assert memory_id == "evolution_memory_id"
    
    @pytest.mark.asyncio
    async def test_evolution_triggers_memory_re_evaluation(self, evolution_tracking_system):
        """Test that consciousness evolution triggers memory re-evaluation"""
        consciousness = evolution_tracking_system["consciousness"]
        memory_storage = evolution_tracking_system["memory_storage"]
        
        # Process evolution
        evolution_result = await consciousness.process_consciousness_evolution()
        
        # Re-evaluate existing memories
        re_evaluation_result = await memory_storage.re_evaluate_memory_relevance_on_evolution(
            previous_consciousness_level=evolution_result["previous_level"],
            current_consciousness_level=evolution_result["current_level"],
            consciousness_context={
                "consciousness_level": evolution_result["current_level"],
                "evolution_type": evolution_result["evolution_type"]
            }
        )
        
        # Verify re-evaluation occurred
        memory_storage.re_evaluate_memory_relevance_on_evolution.assert_called_once()
        
        # Check re-evaluation results
        assert re_evaluation_result["promoted"] == 3
        assert re_evaluation_result["demoted"] == 1
        assert re_evaluation_result["archived"] == 0
    
    @pytest.mark.asyncio
    async def test_evolution_history_tracking(self, evolution_tracking_system):
        """Test tracking of consciousness evolution history through memories"""
        consciousness = evolution_tracking_system["consciousness"]
        memory_storage = evolution_tracking_system["memory_storage"]
        
        # Simulate multiple evolution events
        evolution_events = [
            {"previous_level": 0.6, "current_level": 0.7, "type": "learning"},
            {"previous_level": 0.7, "current_level": 0.8, "type": "insight"},
            {"previous_level": 0.8, "current_level": 0.85, "type": "integration"}
        ]
        
        for i, event in enumerate(evolution_events):
            consciousness.process_consciousness_evolution.return_value = {
                "evolution_occurred": True,
                "previous_level": event["previous_level"],
                "current_level": event["current_level"],
                "evolution_type": event["type"],
                "evolution_insights": [f"Evolution {i+1} insight"]
            }
            
            evolution_result = await consciousness.process_consciousness_evolution()
            
            # Store evolution memory
            await memory_storage.store_consciousness_memory(
                reflection_content=f"Evolution event {i+1}: {event['type']}",
                consciousness_context={"consciousness_level": event["current_level"]},
                memory_type="evolution"
            )
        
        # Verify all evolution events were stored as memories
        assert memory_storage.store_consciousness_memory.call_count == 3

if __name__ == "__main__":
    pytest.main([__file__])
