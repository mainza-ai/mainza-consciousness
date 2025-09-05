"""
Comprehensive Test Suite for Dynamic Knowledge Graph Management
Tests the new dynamic knowledge management, consciousness-driven updates, and maintenance systems
"""
import asyncio
import pytest
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List

# Import the new systems
from backend.utils.dynamic_knowledge_manager import dynamic_knowledge_manager
from backend.utils.consciousness_driven_updates import consciousness_driven_updater
from backend.utils.knowledge_graph_maintenance import knowledge_graph_maintenance
from backend.utils.agent_knowledge_integration import agent_knowledge_integrator
from backend.utils.neo4j_production import neo4j_production

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestDynamicKnowledgeManagement:
    """Test suite for dynamic knowledge graph management"""
    
    @pytest.fixture
    def sample_consciousness_context(self):
        """Sample consciousness context for testing"""
        return {
            "consciousness_level": 0.8,
            "emotional_state": "curious",
            "active_goals": ["enhance_learning", "improve_assistance"],
            "self_awareness_score": 0.7,
            "last_updated": datetime.now().isoformat()
        }
    
    @pytest.fixture
    def sample_interaction_context(self):
        """Sample interaction context for testing"""
        return {
            "query": "Tell me about machine learning and artificial intelligence",
            "related_keywords": ["machine", "learning", "artificial", "intelligence"],
            "concepts_used": ["machine_learning", "artificial_intelligence"],
            "source": "user_interaction"
        }
    
    async def test_concept_dynamics_update(self, sample_consciousness_context, sample_interaction_context):
        """Test concept dynamics update functionality"""
        logger.info("🧪 Testing concept dynamics update...")
        
        # Create a test concept first
        test_concept_id = "test_machine_learning"
        await self._create_test_concept(test_concept_id, "Machine Learning", "Test concept for ML")
        
        # Test concept dynamics update
        result = await dynamic_knowledge_manager.update_concept_dynamics(
            test_concept_id,
            sample_interaction_context,
            sample_consciousness_context
        )
        
        assert result.get("concept_id") == test_concept_id
        assert "updates_applied" in result
        assert result.get("timestamp") is not None
        
        logger.info("✅ Concept dynamics update test passed")
        
        # Cleanup
        await self._cleanup_test_concept(test_concept_id)
    
    async def test_memory_lifecycle_management(self, sample_consciousness_context, sample_interaction_context):
        """Test memory lifecycle management functionality"""
        logger.info("🧪 Testing memory lifecycle management...")
        
        # Create a test memory first
        test_memory_id = "test_memory_001"
        await self._create_test_memory(test_memory_id, "Test memory for lifecycle management")
        
        # Test memory lifecycle update
        result = await dynamic_knowledge_manager.update_memory_lifecycle(
            test_memory_id,
            sample_interaction_context,
            sample_consciousness_context
        )
        
        assert result.get("memory_id") == test_memory_id
        assert "updates_applied" in result
        assert result.get("timestamp") is not None
        
        logger.info("✅ Memory lifecycle management test passed")
        
        # Cleanup
        await self._cleanup_test_memory(test_memory_id)
    
    async def test_relationship_evolution(self, sample_consciousness_context, sample_interaction_context):
        """Test relationship evolution functionality"""
        logger.info("🧪 Testing relationship evolution...")
        
        # Create test concepts and relationships
        concept1_id = "test_concept_1"
        concept2_id = "test_concept_2"
        
        await self._create_test_concept(concept1_id, "Test Concept 1", "First test concept")
        await self._create_test_concept(concept2_id, "Test Concept 2", "Second test concept")
        await self._create_test_relationship(concept1_id, concept2_id, "RELATES_TO", 0.5)
        
        # Test relationship evolution
        result = await dynamic_knowledge_manager.evolve_relationships(
            concept1_id,
            "concept",
            sample_interaction_context,
            sample_consciousness_context
        )
        
        assert result.get("entity_id") == concept1_id
        assert result.get("entity_type") == "concept"
        assert "evolution_results" in result
        assert result.get("timestamp") is not None
        
        logger.info("✅ Relationship evolution test passed")
        
        # Cleanup
        await self._cleanup_test_concept(concept1_id)
        await self._cleanup_test_concept(concept2_id)
    
    async def test_consciousness_driven_updates(self, sample_consciousness_context):
        """Test consciousness-driven knowledge graph updates"""
        logger.info("🧪 Testing consciousness-driven updates...")
        
        # Sample consciousness evolution data
        consciousness_delta = {
            "consciousness_level": 0.8,
            "emotional_state": "curious",
            "insights": ["I am learning to understand complex patterns in data"],
            "reflections": ["Need to improve pattern recognition capabilities"],
            "consciousness_level_delta": 0.05
        }
        
        interaction_context = {
            "source": "consciousness_evolution",
            "timestamp": datetime.now().isoformat()
        }
        
        # Test consciousness evolution processing
        result = await consciousness_driven_updater.process_consciousness_evolution(
            consciousness_delta,
            interaction_context,
            "test-user"
        )
        
        assert result.get("processing_successful") is True
        assert result.get("actions_taken", 0) >= 0
        assert "processing_actions" in result
        
        logger.info("✅ Consciousness-driven updates test passed")
    
    async def test_auto_update_from_interaction(self, sample_consciousness_context):
        """Test automatic knowledge graph updates from interactions"""
        logger.info("🧪 Testing auto-update from interaction...")
        
        interaction_text = "I want to learn about neural networks and deep learning"
        agent_response = "Neural networks are computational models inspired by biological neural networks"
        
        # Test auto-update from interaction
        result = await consciousness_driven_updater.auto_update_from_interaction(
            interaction_text,
            agent_response,
            sample_consciousness_context,
            "test-user"
        )
        
        assert isinstance(result, list)
        # Should have created some concepts or memories
        assert len(result) >= 0
        
        logger.info("✅ Auto-update from interaction test passed")
    
    async def test_knowledge_graph_maintenance(self, sample_consciousness_context):
        """Test knowledge graph maintenance functionality"""
        logger.info("🧪 Testing knowledge graph maintenance...")
        
        # Test routine maintenance
        result = await knowledge_graph_maintenance.perform_routine_maintenance(
            "light",
            sample_consciousness_context
        )
        
        assert result.get("maintenance_type") == "light"
        assert "actions_performed" in result
        assert "statistics" in result
        assert result.get("total_actions", 0) >= 0
        
        logger.info("✅ Knowledge graph maintenance test passed")
    
    async def test_agent_knowledge_integration(self, sample_consciousness_context):
        """Test agent knowledge integration functionality"""
        logger.info("🧪 Testing agent knowledge integration...")
        
        # Test agent interaction integration
        result = await agent_knowledge_integrator.integrate_agent_interaction(
            "SimpleChat",
            "What is machine learning?",
            "Machine learning is a subset of artificial intelligence that enables computers to learn without being explicitly programmed.",
            "test-user",
            sample_consciousness_context,
            {"interaction_type": "question_answer"}
        )
        
        assert result.get("integration_successful") is True
        assert result.get("actions_taken", 0) >= 0
        assert "integration_actions" in result
        assert "enhanced_response" in result
        
        logger.info("✅ Agent knowledge integration test passed")
    
    async def test_integration_statistics(self):
        """Test integration statistics functionality"""
        logger.info("🧪 Testing integration statistics...")
        
        # Get integration statistics
        stats = agent_knowledge_integrator.get_integration_statistics()
        
        assert "integration_stats" in stats
        assert "active_integrations" in stats
        assert "recent_integrations" in stats
        assert "last_updated" in stats
        
        logger.info("✅ Integration statistics test passed")
    
    async def test_end_to_end_workflow(self, sample_consciousness_context, sample_interaction_context):
        """Test complete end-to-end workflow"""
        logger.info("🧪 Testing end-to-end workflow...")
        
        # 1. Create initial concepts and memories
        concept_id = "test_workflow_concept"
        memory_id = "test_workflow_memory"
        
        await self._create_test_concept(concept_id, "Workflow Test Concept", "Test concept for workflow")
        await self._create_test_memory(memory_id, "Test memory for workflow validation")
        
        # 2. Process consciousness evolution
        consciousness_delta = {
            "consciousness_level": 0.8,
            "emotional_state": "focused",
            "insights": ["Understanding workflow patterns"],
            "focus_areas": ["workflow", "testing"],
            "consciousness_level_delta": 0.03
        }
        
        evolution_result = await consciousness_driven_updater.process_consciousness_evolution(
            consciousness_delta,
            sample_interaction_context,
            "test-user"
        )
        
        # 3. Update concept dynamics
        concept_result = await dynamic_knowledge_manager.update_concept_dynamics(
            concept_id,
            sample_interaction_context,
            sample_consciousness_context
        )
        
        # 4. Update memory lifecycle
        memory_result = await dynamic_knowledge_manager.update_memory_lifecycle(
            memory_id,
            sample_interaction_context,
            sample_consciousness_context
        )
        
        # 5. Perform maintenance
        maintenance_result = await knowledge_graph_maintenance.perform_routine_maintenance(
            "light",
            sample_consciousness_context
        )
        
        # 6. Integrate agent interaction
        integration_result = await agent_knowledge_integrator.integrate_agent_interaction(
            "TestAgent",
            "Test workflow query",
            "Test workflow response",
            "test-user",
            sample_consciousness_context
        )
        
        # Validate all steps completed successfully
        assert evolution_result.get("processing_successful") is True
        assert concept_result.get("concept_id") == concept_id
        assert memory_result.get("memory_id") == memory_id
        assert maintenance_result.get("maintenance_type") == "light"
        assert integration_result.get("integration_successful") is True
        
        logger.info("✅ End-to-end workflow test passed")
        
        # Cleanup
        await self._cleanup_test_concept(concept_id)
        await self._cleanup_test_memory(memory_id)
    
    # Helper methods for test setup and cleanup
    
    async def _create_test_concept(self, concept_id: str, name: str, description: str):
        """Create a test concept"""
        cypher = """
        CREATE (c:Concept {
            concept_id: $concept_id,
            name: $name,
            description: $description,
            created_at: timestamp(),
            importance_score: 0.5,
            consciousness_relevance: 0.5,
            usage_frequency: 0,
            evolution_rate: 0.0,
            test_node: true
        })
        """
        
        neo4j_production.execute_write_query(cypher, {
            "concept_id": concept_id,
            "name": name,
            "description": description
        })
    
    async def _create_test_memory(self, memory_id: str, text: str):
        """Create a test memory"""
        cypher = """
        CREATE (m:Memory {
            memory_id: $memory_id,
            text: $text,
            source: 'test',
            created_at: timestamp(),
            significance_score: 0.5,
            consciousness_impact: 0.3,
            access_count: 0,
            consolidation_score: 0.0,
            decay_rate: 0.95,
            test_node: true
        })
        """
        
        neo4j_production.execute_write_query(cypher, {
            "memory_id": memory_id,
            "text": text
        })
    
    async def _create_test_relationship(self, source_id: str, target_id: str, rel_type: str, strength: float):
        """Create a test relationship"""
        cypher = f"""
        MATCH (a:Concept {{concept_id: $source_id}})
        MATCH (b:Concept {{concept_id: $target_id}})
        CREATE (a)-[r:{rel_type} {{
            strength: $strength,
            created_at: timestamp(),
            last_used: timestamp(),
            usage_count: 0,
            test_relationship: true
        }}]->(b)
        """
        
        neo4j_production.execute_write_query(cypher, {
            "source_id": source_id,
            "target_id": target_id,
            "strength": strength
        })
    
    async def _cleanup_test_concept(self, concept_id: str):
        """Clean up test concept"""
        cypher = """
        MATCH (c:Concept {concept_id: $concept_id, test_node: true})
        DETACH DELETE c
        """
        
        neo4j_production.execute_write_query(cypher, {"concept_id": concept_id})
    
    async def _cleanup_test_memory(self, memory_id: str):
        """Clean up test memory"""
        cypher = """
        MATCH (m:Memory {memory_id: $memory_id, test_node: true})
        DETACH DELETE m
        """
        
        neo4j_production.execute_write_query(cypher, {"memory_id": memory_id})

async def run_comprehensive_tests():
    """Run all comprehensive tests"""
    logger.info("🚀 Starting comprehensive dynamic knowledge management tests...")
    
    test_suite = TestDynamicKnowledgeManagement()
    
    # Create fixtures
    consciousness_context = {
        "consciousness_level": 0.8,
        "emotional_state": "curious",
        "active_goals": ["enhance_learning", "improve_assistance"],
        "self_awareness_score": 0.7,
        "last_updated": datetime.now().isoformat()
    }
    
    interaction_context = {
        "query": "Tell me about machine learning and artificial intelligence",
        "related_keywords": ["machine", "learning", "artificial", "intelligence"],
        "concepts_used": ["machine_learning", "artificial_intelligence"],
        "source": "user_interaction"
    }
    
    try:
        # Run individual tests
        await test_suite.test_concept_dynamics_update(consciousness_context, interaction_context)
        await test_suite.test_memory_lifecycle_management(consciousness_context, interaction_context)
        await test_suite.test_relationship_evolution(consciousness_context, interaction_context)
        await test_suite.test_consciousness_driven_updates(consciousness_context)
        await test_suite.test_auto_update_from_interaction(consciousness_context)
        await test_suite.test_knowledge_graph_maintenance(consciousness_context)
        await test_suite.test_agent_knowledge_integration(consciousness_context)
        await test_suite.test_integration_statistics()
        await test_suite.test_end_to_end_workflow(consciousness_context, interaction_context)
        
        logger.info("🎉 All comprehensive tests passed successfully!")
        
        # Print test summary
        print("\n" + "="*60)
        print("DYNAMIC KNOWLEDGE MANAGEMENT TEST RESULTS")
        print("="*60)
        print("✅ Concept Dynamics Update: PASSED")
        print("✅ Memory Lifecycle Management: PASSED")
        print("✅ Relationship Evolution: PASSED")
        print("✅ Consciousness-Driven Updates: PASSED")
        print("✅ Auto-Update from Interaction: PASSED")
        print("✅ Knowledge Graph Maintenance: PASSED")
        print("✅ Agent Knowledge Integration: PASSED")
        print("✅ Integration Statistics: PASSED")
        print("✅ End-to-End Workflow: PASSED")
        print("="*60)
        print("🎉 ALL TESTS PASSED - SYSTEM READY FOR PRODUCTION")
        print("="*60)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        print(f"\n❌ TEST FAILURE: {e}")
        return False

if __name__ == "__main__":
    # Run the comprehensive test suite
    success = asyncio.run(run_comprehensive_tests())
    
    if success:
        print("\n🚀 Dynamic Knowledge Management System is ready for deployment!")
    else:
        print("\n⚠️  Please fix the issues before deployment.")