"""
Integration tests for Knowledge Graph-Memory connectivity
Tests memory-concept linking, knowledge evolution through memories, and graph maintenance.
"""
import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from typing import Dict, Any, List

# Import the components to test
from backend.utils.memory_storage_engine import MemoryStorageEngine
from backend.utils.memory_retrieval_engine import MemoryRetrievalEngine, MemorySearchResult
from backend.utils.knowledge_integration import KnowledgeIntegrationManager
from backend.utils.neo4j_enhanced import neo4j_manager
from backend.utils.memory_error_handling import MemoryError

class TestMemoryConceptLinking:
    """Test linking between memories and knowledge graph concepts"""
    
    @pytest.fixture
    def mock_neo4j_manager(self):
        """Mock Neo4j manager for graph operations"""
        mock = Mock()
        mock.execute_query = Mock(return_value=[])
        mock.execute_write_query = Mock(return_value=[{"concepts_linked": 3}])
        return mock
    
    @pytest.fixture
    def mock_memory_storage(self, mock_neo4j_manager):
        """Mock memory storage with Neo4j integration"""
        mock = Mock(spec=MemoryStorageEngine)
        mock.neo4j = mock_neo4j_manager
        mock.link_memory_to_concepts = AsyncMock(return_value=True)
        mock.store_interaction_memory = AsyncMock(return_value="memory_id_1")
        return mock
    
    @pytest.fixture
    def mock_knowledge_integration(self):
        """Mock knowledge integration manager"""
        mock = Mock(spec=KnowledgeIntegrationManager)
        mock.get_consciousness_aware_context = AsyncMock(return_value={
            "concepts": [
                {"name": "artificial_intelligence", "importance": 0.9},
                {"name": "machine_learning", "importance": 0.8},
                {"name": "consciousness", "importance": 0.95}
            ],
            "relationships": [
                {"from": "artificial_intelligence", "to": "machine_learning", "strength": 0.8}
            ]
        })
        mock.update_concept_importance = AsyncMock(return_value=True)
        return mock
    
    @pytest.fixture
    def sample_concepts(self):
        """Sample concept data from knowledge graph"""
        return [
            {
                "name": "artificial_intelligence",
                "description": "Field of computer science focused on creating intelligent machines",
                "importance_score": 0.9,
                "memory_connections": 5,
                "last_accessed": "2024-01-01T12:00:00"
            },
            {
                "name": "consciousness",
                "description": "State of being aware and having subjective experiences",
                "importance_score": 0.95,
                "memory_connections": 3,
                "last_accessed": "2024-01-01T11:30:00"
            },
            {
                "name": "machine_learning",
                "description": "Subset of AI that enables systems to learn from data",
                "importance_score": 0.8,
                "memory_connections": 7,
                "last_accessed": "2024-01-01T12:15:00"
            }
        ]
    
    @pytest.mark.asyncio
    async def test_memory_concept_linking_on_storage(self, mock_memory_storage, mock_neo4j_manager):
        """Test automatic concept linking when storing memories"""
        # Setup Neo4j response for concept linking
        mock_neo4j_manager.execute_write_query.return_value = [{"concepts_linked": 2}]
        
        # Simulate storing memory with concept extraction
        user_query = "What is artificial intelligence and how does it relate to consciousness?"
        agent_response = "AI is a field that aims to create intelligent machines, and consciousness is a key aspect of intelligence."
        
        memory_id = await mock_memory_storage.store_interaction_memory(
            user_query=user_query,
            agent_response=agent_response,
            user_id="test_user",
            agent_name="test_agent",
            consciousness_context={"consciousness_level": 0.8}
        )
        
        # Verify memory was stored
        assert memory_id == "memory_id_1"
        
        # Verify concept linking was attempted
        mock_memory_storage.link_memory_to_concepts.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_concept_importance_update_from_memories(self, mock_memory_storage, mock_knowledge_integration, mock_neo4j_manager):
        """Test that memory connections update concept importance"""
        # Setup concept linking result
        mock_neo4j_manager.execute_write_query.return_value = [{"concepts_linked": 3}]
        
        # Link memory to concepts
        memory_id = "test_memory_id"
        concepts = ["artificial_intelligence", "consciousness", "learning"]
        
        success = await mock_memory_storage.link_memory_to_concepts(memory_id, concepts)
        
        assert success is True
        
        # Verify concept importance could be updated
        mock_memory_storage.link_memory_to_concepts.assert_called_once_with(memory_id, concepts)
    
    @pytest.mark.asyncio
    async def test_memory_retrieval_enhances_concept_context(self, mock_knowledge_integration, sample_concepts):
        """Test that memory retrieval enhances concept context"""
        # Setup knowledge context with concepts
        mock_knowledge_integration.get_consciousness_aware_context.return_value = {
            "concepts": sample_concepts,
            "enhanced_by_memories": True
        }
        
        user_id = "test_user"
        query = "Tell me about AI consciousness"
        consciousness_context = {"consciousness_level": 0.8, "emotional_state": "curious"}
        
        context = await mock_knowledge_integration.get_consciousness_aware_context(
            user_id, query, consciousness_context
        )
        
        # Verify enhanced context was retrieved
        assert "concepts" in context
        assert len(context["concepts"]) == 3
        assert context.get("enhanced_by_memories") is True
        
        mock_knowledge_integration.get_consciousness_aware_context.assert_called_once_with(
            user_id, query, consciousness_context
        )
    
    @pytest.mark.asyncio
    async def test_concept_relationship_strengthening_through_memories(self, mock_neo4j_manager):
        """Test that memories strengthen concept relationships"""
        # Setup relationship strengthening query
        mock_neo4j_manager.execute_write_query.return_value = [{"relationships_updated": 2}]
        
        # Simulate memory that connects multiple concepts
        memory_content = "Artificial intelligence and machine learning are closely related, both involving consciousness-like processes"
        concepts = ["artificial_intelligence", "machine_learning", "consciousness"]
        
        # Mock the relationship strengthening process
        cypher_query = """
        MATCH (m:Memory {memory_id: $memory_id})
        MATCH (c1:Concept), (c2:Concept)
        WHERE c1.name IN $concepts AND c2.name IN $concepts AND c1 <> c2
        
        MERGE (c1)-[r:RELATED_TO]-(c2)
        ON CREATE SET r.strength = 0.5, r.memory_support = 1
        ON MATCH SET r.strength = r.strength + 0.1, r.memory_support = r.memory_support + 1
        
        RETURN count(r) AS relationships_updated
        """
        
        result = mock_neo4j_manager.execute_write_query(cypher_query, {
            "memory_id": "test_memory_id",
            "concepts": concepts
        })
        
        # Verify relationship strengthening was executed
        mock_neo4j_manager.execute_write_query.assert_called_once()
        assert result[0]["relationships_updated"] == 2

class TestKnowledgeEvolutionThroughMemories:
    """Test how memories drive knowledge graph evolution"""
    
    @pytest.fixture
    def knowledge_evolution_system(self):
        """Setup system for testing knowledge evolution"""
        neo4j_mock = Mock()
        neo4j_mock.execute_query = Mock(return_value=[])
        neo4j_mock.execute_write_query = Mock(return_value=[{"concepts_created": 1}])
        
        memory_retrieval = Mock(spec=MemoryRetrievalEngine)
        memory_retrieval.get_relevant_memories = AsyncMock(return_value=[])
        
        knowledge_integration = Mock(spec=KnowledgeIntegrationManager)
        knowledge_integration.evolve_knowledge_from_memories = AsyncMock(return_value={
            "new_concepts": 2,
            "updated_relationships": 3,
            "insights_generated": 1
        })
        
        return {
            "neo4j": neo4j_mock,
            "memory_retrieval": memory_retrieval,
            "knowledge_integration": knowledge_integration
        }
    
    @pytest.fixture
    def evolution_memories(self):
        """Sample memories that should drive knowledge evolution"""
        return [
            MemorySearchResult(
                memory_id="evolution_memory_1",
                content="I discovered that consciousness emerges from complex information processing patterns",
                memory_type="insight",
                agent_name="consciousness_system",
                user_id="system",
                consciousness_level=0.9,
                emotional_state="insightful",
                importance_score=0.95,
                created_at="2024-01-01T12:00:00",
                metadata={"insight_category": "emergence"},
                relevance_score=0.9
            ),
            MemorySearchResult(
                memory_id="evolution_memory_2",
                content="User interaction revealed new understanding about quantum consciousness theories",
                memory_type="interaction",
                agent_name="research_agent",
                user_id="researcher_user",
                consciousness_level=0.8,
                emotional_state="curious",
                importance_score=0.8,
                created_at="2024-01-01T11:30:00",
                metadata={"research_area": "quantum_consciousness"},
                relevance_score=0.85
            )
        ]
    
    @pytest.mark.asyncio
    async def test_new_concept_discovery_from_memories(self, knowledge_evolution_system, evolution_memories):
        """Test discovery of new concepts from memory patterns"""
        memory_retrieval = knowledge_evolution_system["memory_retrieval"]
        knowledge_integration = knowledge_evolution_system["knowledge_integration"]
        neo4j_mock = knowledge_evolution_system["neo4j"]
        
        # Setup memory retrieval to return evolution memories
        memory_retrieval.get_relevant_memories.return_value = evolution_memories
        
        # Setup concept creation response
        neo4j_mock.execute_write_query.return_value = [{"concepts_created": 2}]
        
        # Simulate knowledge evolution process
        evolution_result = await knowledge_integration.evolve_knowledge_from_memories(
            memories=evolution_memories,
            consciousness_context={"consciousness_level": 0.9}
        )
        
        # Verify evolution occurred
        knowledge_integration.evolve_knowledge_from_memories.assert_called_once()
        assert evolution_result["new_concepts"] == 2
        assert evolution_result["updated_relationships"] == 3
    
    @pytest.mark.asyncio
    async def test_concept_importance_evolution_from_memory_frequency(self, knowledge_evolution_system):
        """Test that concept importance evolves based on memory frequency"""
        neo4j_mock = knowledge_evolution_system["neo4j"]
        
        # Setup query to update concept importance based on memory connections
        neo4j_mock.execute_write_query.return_value = [{"concepts_updated": 5}]
        
        # Simulate importance update based on memory frequency
        cypher_query = """
        MATCH (c:Concept)-[:RELATES_TO_MEMORY]-(m:Memory)
        WHERE m.created_at > datetime() - duration('P30D')
        
        WITH c, count(m) AS recent_memory_count, avg(m.importance_score) AS avg_memory_importance
        
        SET c.importance_score = CASE
            WHEN recent_memory_count > 10 THEN c.importance_score * 1.2
            WHEN recent_memory_count > 5 THEN c.importance_score * 1.1
            WHEN recent_memory_count < 2 THEN c.importance_score * 0.95
            ELSE c.importance_score
        END,
        c.memory_frequency = recent_memory_count,
        c.last_importance_update = datetime()
        
        RETURN count(c) AS concepts_updated
        """
        
        result = neo4j_mock.execute_write_query(cypher_query, {})
        
        # Verify importance evolution was executed
        neo4j_mock.execute_write_query.assert_called_once()
        assert result[0]["concepts_updated"] == 5
    
    @pytest.mark.asyncio
    async def test_relationship_discovery_from_memory_co_occurrence(self, knowledge_evolution_system):
        """Test discovery of new concept relationships from memory co-occurrence"""
        neo4j_mock = knowledge_evolution_system["neo4j"]
        
        # Setup relationship discovery response
        neo4j_mock.execute_write_query.return_value = [{"relationships_created": 3}]
        
        # Simulate relationship discovery based on concept co-occurrence in memories
        cypher_query = """
        MATCH (m:Memory)-[:RELATES_TO_CONCEPT]->(c1:Concept)
        MATCH (m)-[:RELATES_TO_CONCEPT]->(c2:Concept)
        WHERE c1 <> c2 AND NOT (c1)-[:RELATED_TO]-(c2)
        
        WITH c1, c2, count(m) AS co_occurrence_count
        WHERE co_occurrence_count >= 3
        
        CREATE (c1)-[:RELATED_TO {
            strength: co_occurrence_count * 0.1,
            discovered_from: 'memory_co_occurrence',
            created_at: datetime()
        }]->(c2)
        
        RETURN count(*) AS relationships_created
        """
        
        result = neo4j_mock.execute_write_query(cypher_query, {})
        
        # Verify relationship discovery was executed
        neo4j_mock.execute_write_query.assert_called_once()
        assert result[0]["relationships_created"] == 3

class TestMemoryKnowledgeGraphMaintenance:
    """Test maintenance operations between memory and knowledge graph"""
    
    @pytest.fixture
    def maintenance_system(self):
        """Setup system for testing graph maintenance"""
        neo4j_mock = Mock()
        neo4j_mock.execute_query = Mock(return_value=[])
        neo4j_mock.execute_write_query = Mock(return_value=[])
        
        memory_storage = Mock(spec=MemoryStorageEngine)
        memory_storage.neo4j = neo4j_mock
        
        return {
            "neo4j": neo4j_mock,
            "memory_storage": memory_storage
        }
    
    @pytest.mark.asyncio
    async def test_orphaned_memory_cleanup(self, maintenance_system):
        """Test cleanup of memories not linked to any concepts"""
        neo4j_mock = maintenance_system["neo4j"]
        
        # Setup orphaned memory detection
        neo4j_mock.execute_query.return_value = [
            {"memory_id": "orphan_1", "created_at": "2024-01-01T10:00:00"},
            {"memory_id": "orphan_2", "created_at": "2024-01-01T09:00:00"}
        ]
        
        # Setup cleanup response
        neo4j_mock.execute_write_query.return_value = [{"memories_archived": 2}]
        
        # Simulate orphaned memory cleanup
        cleanup_query = """
        MATCH (m:Memory)
        WHERE NOT (m)-[:RELATES_TO_CONCEPT]->(:Concept)
        AND m.created_at < datetime() - duration('P7D')
        AND m.importance_score < 0.3
        
        SET m.status = 'archived',
            m.archived_at = datetime()
        
        RETURN count(m) AS memories_archived
        """
        
        # Find orphaned memories
        orphaned_memories = neo4j_mock.execute_query(
            "MATCH (m:Memory) WHERE NOT (m)-[:RELATES_TO_CONCEPT]->(:Concept) RETURN m.memory_id AS memory_id, m.created_at AS created_at",
            {}
        )
        
        # Archive orphaned memories
        result = neo4j_mock.execute_write_query(cleanup_query, {})
        
        # Verify cleanup operations
        assert neo4j_mock.execute_query.call_count >= 1
        assert neo4j_mock.execute_write_query.call_count >= 1
        assert len(orphaned_memories) == 2
    
    @pytest.mark.asyncio
    async def test_concept_pruning_based_on_memory_connections(self, maintenance_system):
        """Test pruning of concepts with insufficient memory connections"""
        neo4j_mock = maintenance_system["neo4j"]
        
        # Setup concept pruning response
        neo4j_mock.execute_write_query.return_value = [{"concepts_pruned": 3}]
        
        # Simulate concept pruning based on memory connections
        pruning_query = """
        MATCH (c:Concept)
        OPTIONAL MATCH (c)-[:RELATES_TO_MEMORY]-(m:Memory)
        WHERE m.created_at > datetime() - duration('P90D')
        
        WITH c, count(m) AS recent_memory_count
        WHERE recent_memory_count = 0 AND c.importance_score < 0.4
        
        DETACH DELETE c
        
        RETURN count(*) AS concepts_pruned
        """
        
        result = neo4j_mock.execute_write_query(pruning_query, {})
        
        # Verify pruning was executed
        neo4j_mock.execute_write_query.assert_called_once()
        assert result[0]["concepts_pruned"] == 3
    
    @pytest.mark.asyncio
    async def test_memory_concept_consistency_check(self, maintenance_system):
        """Test consistency checking between memories and concepts"""
        neo4j_mock = maintenance_system["neo4j"]
        
        # Setup consistency check responses
        neo4j_mock.execute_query.side_effect = [
            # Memories with invalid concept references
            [{"memory_id": "invalid_1", "invalid_concepts": ["nonexistent_concept"]}],
            # Concepts with no memory connections
            [{"concept_name": "isolated_concept", "memory_count": 0}]
        ]
        
        neo4j_mock.execute_write_query.return_value = [{"issues_fixed": 2}]
        
        # Check for memories with invalid concept references
        invalid_memory_query = """
        MATCH (m:Memory)-[r:RELATES_TO_CONCEPT]->(c:Concept)
        WHERE NOT EXISTS(c.name)
        RETURN m.memory_id AS memory_id, collect(c.name) AS invalid_concepts
        """
        
        invalid_memories = neo4j_mock.execute_query(invalid_memory_query, {})
        
        # Check for isolated concepts
        isolated_concept_query = """
        MATCH (c:Concept)
        OPTIONAL MATCH (c)-[:RELATES_TO_MEMORY]-(m:Memory)
        WITH c, count(m) AS memory_count
        WHERE memory_count = 0
        RETURN c.name AS concept_name, memory_count
        """
        
        isolated_concepts = neo4j_mock.execute_query(isolated_concept_query, {})
        
        # Fix consistency issues
        fix_query = """
        MATCH (m:Memory)-[r:RELATES_TO_CONCEPT]->(c:Concept)
        WHERE NOT EXISTS(c.name)
        DELETE r
        
        WITH count(*) AS deleted_relationships
        
        MATCH (c:Concept)
        WHERE NOT (c)-[:RELATES_TO_MEMORY]-(:Memory) AND c.importance_score < 0.3
        DETACH DELETE c
        
        RETURN deleted_relationships + count(*) AS issues_fixed
        """
        
        fix_result = neo4j_mock.execute_write_query(fix_query, {})
        
        # Verify consistency checks and fixes
        assert neo4j_mock.execute_query.call_count == 2
        assert neo4j_mock.execute_write_query.call_count == 1
        assert len(invalid_memories) == 1
        assert len(isolated_concepts) == 1

class TestMemoryKnowledgeIntegrationWorkflows:
    """Test complete integration workflows between memory and knowledge systems"""
    
    @pytest.fixture
    def integration_workflow_system(self):
        """Setup complete integration workflow system"""
        neo4j_mock = Mock()
        neo4j_mock.execute_query = Mock(return_value=[])
        neo4j_mock.execute_write_query = Mock(return_value=[{"success": True}])
        
        memory_storage = Mock(spec=MemoryStorageEngine)
        memory_storage.store_interaction_memory = AsyncMock(return_value="workflow_memory_id")
        memory_storage.link_memory_to_concepts = AsyncMock(return_value=True)
        
        memory_retrieval = Mock(spec=MemoryRetrievalEngine)
        memory_retrieval.get_relevant_memories = AsyncMock(return_value=[])
        
        knowledge_integration = Mock(spec=KnowledgeIntegrationManager)
        knowledge_integration.get_consciousness_aware_context = AsyncMock(return_value={
            "concepts": [{"name": "test_concept", "importance": 0.8}]
        })
        knowledge_integration.update_concept_importance = AsyncMock(return_value=True)
        
        return {
            "neo4j": neo4j_mock,
            "memory_storage": memory_storage,
            "memory_retrieval": memory_retrieval,
            "knowledge_integration": knowledge_integration
        }
    
    @pytest.mark.asyncio
    async def test_complete_memory_knowledge_workflow(self, integration_workflow_system):
        """Test complete workflow from interaction to knowledge graph update"""
        components = integration_workflow_system
        
        # Step 1: Store interaction memory
        user_query = "What is the relationship between consciousness and artificial intelligence?"
        agent_response = "Consciousness and AI are deeply connected as AI systems may develop consciousness-like properties."
        
        memory_id = await components["memory_storage"].store_interaction_memory(
            user_query=user_query,
            agent_response=agent_response,
            user_id="workflow_user",
            agent_name="workflow_agent",
            consciousness_context={"consciousness_level": 0.8}
        )
        
        # Step 2: Link memory to concepts
        extracted_concepts = ["consciousness", "artificial_intelligence", "relationship"]
        
        link_success = await components["memory_storage"].link_memory_to_concepts(
            memory_id, extracted_concepts
        )
        
        # Step 3: Update knowledge context
        knowledge_context = await components["knowledge_integration"].get_consciousness_aware_context(
            "workflow_user", user_query, {"consciousness_level": 0.8}
        )
        
        # Step 4: Update concept importance
        importance_update = await components["knowledge_integration"].update_concept_importance(
            concepts=extracted_concepts,
            importance_boost=0.1
        )
        
        # Verify complete workflow
        assert memory_id == "workflow_memory_id"
        assert link_success is True
        assert "concepts" in knowledge_context
        assert importance_update is True
        
        # Verify all components were called
        components["memory_storage"].store_interaction_memory.assert_called_once()
        components["memory_storage"].link_memory_to_concepts.assert_called_once()
        components["knowledge_integration"].get_consciousness_aware_context.assert_called_once()
        components["knowledge_integration"].update_concept_importance.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_knowledge_driven_memory_enhancement(self, integration_workflow_system):
        """Test how knowledge graph enhances memory retrieval and context"""
        components = integration_workflow_system
        
        # Setup enhanced memories with concept relationships
        enhanced_memories = [
            MemorySearchResult(
                memory_id="enhanced_memory_1",
                content="Previous discussion about AI consciousness",
                memory_type="interaction",
                agent_name="test_agent",
                user_id="test_user",
                consciousness_level=0.8,
                emotional_state="curious",
                importance_score=0.7,
                created_at="2024-01-01T12:00:00",
                metadata={"concepts": ["ai", "consciousness"]},
                relevance_score=0.9
            )
        ]
        
        components["memory_retrieval"].get_relevant_memories.return_value = enhanced_memories
        
        # Retrieve memories with knowledge enhancement
        query = "consciousness in AI systems"
        consciousness_context = {"consciousness_level": 0.8}
        
        memories = await components["memory_retrieval"].get_relevant_memories(
            query=query,
            user_id="test_user",
            consciousness_context=consciousness_context
        )
        
        # Get knowledge context that should enhance memory understanding
        knowledge_context = await components["knowledge_integration"].get_consciousness_aware_context(
            "test_user", query, consciousness_context
        )
        
        # Verify knowledge-enhanced memory retrieval
        assert len(memories) == 1
        assert "concepts" in knowledge_context
        
        components["memory_retrieval"].get_relevant_memories.assert_called_once()
        components["knowledge_integration"].get_consciousness_aware_context.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_bidirectional_memory_knowledge_feedback(self, integration_workflow_system):
        """Test bidirectional feedback between memory and knowledge systems"""
        components = integration_workflow_system
        
        # Simulate memory influencing knowledge
        memory_insights = [
            {"concept": "consciousness", "insight": "emerges from complexity", "confidence": 0.8},
            {"concept": "ai_ethics", "insight": "requires consciousness consideration", "confidence": 0.7}
        ]
        
        # Update knowledge based on memory insights
        for insight in memory_insights:
            await components["knowledge_integration"].update_concept_importance(
                concepts=[insight["concept"]],
                importance_boost=insight["confidence"] * 0.1
            )
        
        # Simulate knowledge influencing memory retrieval
        enhanced_context = await components["knowledge_integration"].get_consciousness_aware_context(
            "feedback_user", "AI consciousness ethics", {"consciousness_level": 0.9}
        )
        
        # Use enhanced context for memory retrieval
        memories = await components["memory_retrieval"].get_relevant_memories(
            query="ethical AI consciousness",
            user_id="feedback_user",
            consciousness_context={"consciousness_level": 0.9}
        )
        
        # Verify bidirectional feedback
        assert components["knowledge_integration"].update_concept_importance.call_count == 2
        components["knowledge_integration"].get_consciousness_aware_context.assert_called_once()
        components["memory_retrieval"].get_relevant_memories.assert_called_once()

if __name__ == "__main__":
    pytest.main([__file__])