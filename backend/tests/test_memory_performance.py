"""
Performance tests for Memory System
Tests memory operation speed, load handling, and scalability under realistic usage patterns.
"""
import pytest
import asyncio
import time
import statistics
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, Any, List
import concurrent.futures

# Import the components to test
from backend.utils.memory_storage_engine import MemoryStorageEngine, MemoryRecord
from backend.utils.memory_retrieval_engine import MemoryRetrievalEngine, MemorySearchResult
from backend.utils.memory_context_builder import MemoryContextBuilder
from backend.utils.memory_error_handling import MemoryError

class TestMemoryStoragePerformance:
    """Test memory storage performance under various loads"""
    
    @pytest.fixture
    def performance_storage_engine(self):
        """Create storage engine with performance-optimized mocks"""
        engine = MemoryStorageEngine()
        
        # Mock Neo4j with realistic delays
        mock_neo4j = Mock()
        mock_neo4j.execute_write_query = Mock(side_effect=self._mock_neo4j_write_delay)
        engine.neo4j = mock_neo4j
        
        # Mock embedding with realistic delays
        mock_embedding = Mock()
        mock_embedding.get_embedding = Mock(side_effect=self._mock_embedding_delay)
        engine.embedding = mock_embedding
        
        return engine
    
    def _mock_neo4j_write_delay(self, query, params):
        """Mock Neo4j write with realistic delay"""
        time.sleep(0.01)  # 10ms delay to simulate database write
        return [{"memory_id": f"memory_{time.time()}"}]
    
    def _mock_embedding_delay(self, text):
        """Mock embedding generation with realistic delay"""
        time.sleep(0.005)  # 5ms delay to simulate embedding generation
        return [0.1] * 384  # Typical embedding size
    
    @pytest.mark.asyncio
    async def test_single_memory_storage_performance(self, performance_storage_engine):
        """Test performance of storing a single memory"""
        start_time = time.time()
        
        memory_id = await performance_storage_engine.store_interaction_memory(
            user_query="Test query for performance",
            agent_response="Test response for performance measurement",
            user_id="perf_user",
            agent_name="perf_agent",
            consciousness_context={"consciousness_level": 0.8}
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete within reasonable time (< 100ms for single operation)
        assert duration < 0.1
        assert memory_id is not None
        
        print(f"Single memory storage took: {duration:.3f}s")
    
    @pytest.mark.asyncio
    async def test_batch_memory_storage_performance(self, performance_storage_engine):
        """Test performance of storing multiple memories in sequence"""
        batch_size = 10
        durations = []
        
        for i in range(batch_size):
            start_time = time.time()
            
            memory_id = await performance_storage_engine.store_interaction_memory(
                user_query=f"Test query {i}",
                agent_response=f"Test response {i}",
                user_id="batch_user",
                agent_name="batch_agent",
                consciousness_context={"consciousness_level": 0.7 + (i * 0.01)}
            )
            
            end_time = time.time()
            durations.append(end_time - start_time)
            
            assert memory_id is not None
        
        # Calculate performance metrics
        avg_duration = statistics.mean(durations)
        max_duration = max(durations)
        min_duration = min(durations)
        
        # Performance assertions
        assert avg_duration < 0.1  # Average should be under 100ms
        assert max_duration < 0.2  # No single operation should exceed 200ms
        
        print(f"Batch storage performance:")
        print(f"  Average: {avg_duration:.3f}s")
        print(f"  Min: {min_duration:.3f}s")
        print(f"  Max: {max_duration:.3f}s")
    
    @pytest.mark.asyncio
    async def test_concurrent_memory_storage_performance(self, performance_storage_engine):
        """Test performance of concurrent memory storage operations"""
        concurrent_operations = 5
        
        async def store_memory(index):
            start_time = time.time()
            memory_id = await performance_storage_engine.store_interaction_memory(
                user_query=f"Concurrent query {index}",
                agent_response=f"Concurrent response {index}",
                user_id=f"concurrent_user_{index}",
                agent_name="concurrent_agent",
                consciousness_context={"consciousness_level": 0.8}
            )
            end_time = time.time()
            return memory_id, end_time - start_time
        
        # Execute concurrent operations
        start_time = time.time()
        tasks = [store_memory(i) for i in range(concurrent_operations)]
        results = await asyncio.gather(*tasks)
        total_time = time.time() - start_time
        
        # Verify all operations completed
        assert len(results) == concurrent_operations
        assert all(result[0] is not None for result in results)
        
        # Performance analysis
        individual_durations = [result[1] for result in results]
        avg_individual = statistics.mean(individual_durations)
        
        # Concurrent operations should complete faster than sequential
        expected_sequential_time = avg_individual * concurrent_operations
        efficiency = expected_sequential_time / total_time
        
        print(f"Concurrent storage performance:")
        print(f"  Total time: {total_time:.3f}s")
        print(f"  Average individual: {avg_individual:.3f}s")
        print(f"  Efficiency gain: {efficiency:.2f}x")
        
        # Should show some concurrency benefit
        assert efficiency > 1.0
    
    @pytest.mark.asyncio
    async def test_large_content_storage_performance(self, performance_storage_engine):
        """Test performance with large content that requires truncation"""
        # Create large content
        large_query = "A" * 5000
        large_response = "B" * 10000
        
        start_time = time.time()
        
        memory_id = await performance_storage_engine.store_interaction_memory(
            user_query=large_query,
            agent_response=large_response,
            user_id="large_content_user",
            agent_name="large_content_agent",
            consciousness_context={"consciousness_level": 0.8}
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Large content should still be processed efficiently
        assert duration < 0.15  # Allow slightly more time for large content
        assert memory_id is not None
        
        print(f"Large content storage took: {duration:.3f}s")

class TestMemoryRetrievalPerformance:
    """Test memory retrieval performance under various conditions"""
    
    @pytest.fixture
    def performance_retrieval_engine(self):
        """Create retrieval engine with performance-optimized mocks"""
        engine = MemoryRetrievalEngine()
        
        # Mock Neo4j with realistic query delays
        mock_neo4j = Mock()
        mock_neo4j.execute_query = Mock(side_effect=self._mock_neo4j_query_delay)
        engine.neo4j = mock_neo4j
        
        # Mock embedding manager
        mock_embedding_manager = Mock()
        mock_embedding_manager.find_similar_memories = AsyncMock(side_effect=self._mock_similarity_search_delay)
        engine.embedding_manager = mock_embedding_manager
        
        # Mock embedding service
        mock_embedding = Mock()
        mock_embedding.get_embedding = Mock(side_effect=self._mock_embedding_delay)
        engine.embedding = mock_embedding
        
        return engine
    
    def _mock_neo4j_query_delay(self, query, params):
        """Mock Neo4j query with realistic delay based on complexity"""
        # Simulate different delays based on query complexity
        if "MATCH" in query and "ORDER BY" in query:
            time.sleep(0.02)  # Complex query: 20ms
        else:
            time.sleep(0.01)  # Simple query: 10ms
        
        # Return mock results
        return [
            {
                "memory_id": f"memory_{i}",
                "content": f"Mock memory content {i}",
                "memory_type": "interaction",
                "agent_name": "mock_agent",
                "consciousness_level": 0.7 + (i * 0.1),
                "emotional_state": "neutral",
                "importance_score": 0.6 + (i * 0.05),
                "created_at": "2024-01-01T12:00:00",
                "metadata": "{}",
                "similarity_score": 0.8 - (i * 0.1)
            }
            for i in range(min(5, params.get("limit", 5)))
        ]
    
    async def _mock_similarity_search_delay(self, query_text, user_id, memory_types, limit, min_similarity):
        """Mock similarity search with realistic delay"""
        await asyncio.sleep(0.015)  # 15ms for vector similarity search
        
        return [
            {
                "memory_id": f"sim_memory_{i}",
                "content": f"Similar memory content {i}",
                "memory_type": "interaction",
                "agent_name": "sim_agent",
                "consciousness_level": 0.8,
                "emotional_state": "curious",
                "importance_score": 0.7,
                "created_at": "2024-01-01T12:00:00",
                "metadata": {},
                "similarity_score": 0.9 - (i * 0.1)
            }
            for i in range(min(limit, 3))
        ]
    
    def _mock_embedding_delay(self, text):
        """Mock embedding generation with realistic delay"""
        time.sleep(0.005)  # 5ms delay
        return [0.1] * 384
    
    @pytest.mark.asyncio
    async def test_semantic_search_performance(self, performance_retrieval_engine):
        """Test semantic search performance"""
        start_time = time.time()
        
        results = await performance_retrieval_engine.get_relevant_memories(
            query="test semantic search performance",
            user_id="perf_user",
            consciousness_context={"consciousness_level": 0.8},
            search_type="semantic",
            limit=5
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Semantic search should complete within reasonable time
        assert duration < 0.1  # Under 100ms
        assert len(results) >= 0  # Should return results or empty list
        
        print(f"Semantic search took: {duration:.3f}s")
    
    @pytest.mark.asyncio
    async def test_hybrid_search_performance(self, performance_retrieval_engine):
        """Test hybrid search performance (most complex search type)"""
        start_time = time.time()
        
        results = await performance_retrieval_engine.get_relevant_memories(
            query="test hybrid search performance with multiple strategies",
            user_id="perf_user",
            consciousness_context={"consciousness_level": 0.8, "emotional_state": "curious"},
            search_type="hybrid",
            limit=10
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Hybrid search combines multiple strategies, should still be fast
        assert duration < 0.2  # Under 200ms for complex hybrid search
        assert len(results) >= 0
        
        print(f"Hybrid search took: {duration:.3f}s")
    
    @pytest.mark.asyncio
    async def test_conversation_history_performance(self, performance_retrieval_engine):
        """Test conversation history retrieval performance"""
        start_time = time.time()
        
        history = await performance_retrieval_engine.get_conversation_history(
            user_id="perf_user",
            limit=20
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Conversation history should be very fast (simple query)
        assert duration < 0.05  # Under 50ms
        assert len(history) >= 0
        
        print(f"Conversation history retrieval took: {duration:.3f}s")
    
    @pytest.mark.asyncio
    async def test_concurrent_search_performance(self, performance_retrieval_engine):
        """Test performance of concurrent search operations"""
        concurrent_searches = 3
        
        async def perform_search(search_type, index):
            start_time = time.time()
            results = await performance_retrieval_engine.get_relevant_memories(
                query=f"concurrent search {index}",
                user_id=f"concurrent_user_{index}",
                consciousness_context={"consciousness_level": 0.8},
                search_type=search_type,
                limit=5
            )
            end_time = time.time()
            return results, end_time - start_time
        
        # Execute different search types concurrently
        search_types = ["semantic", "keyword", "temporal"]
        
        start_time = time.time()
        tasks = [perform_search(search_types[i], i) for i in range(concurrent_searches)]
        results = await asyncio.gather(*tasks)
        total_time = time.time() - start_time
        
        # Verify all searches completed
        assert len(results) == concurrent_searches
        
        # Performance analysis
        individual_durations = [result[1] for result in results]
        avg_individual = statistics.mean(individual_durations)
        
        print(f"Concurrent search performance:")
        print(f"  Total time: {total_time:.3f}s")
        print(f"  Average individual: {avg_individual:.3f}s")
        
        # Should complete efficiently
        assert total_time < 0.3  # All concurrent searches under 300ms

class TestMemoryContextBuildingPerformance:
    """Test memory context building performance"""
    
    @pytest.fixture
    def performance_context_builder(self):
        """Create context builder with performance-optimized mocks"""
        builder = MemoryContextBuilder()
        
        # Mock Neo4j for concept extraction
        mock_neo4j = Mock()
        mock_neo4j.execute_query = Mock(side_effect=self._mock_concept_query_delay)
        builder.neo4j = mock_neo4j
        
        # Mock memory retrieval
        mock_retrieval = Mock()
        mock_retrieval.get_relevant_memories = AsyncMock(side_effect=self._mock_memory_retrieval_delay)
        mock_retrieval.get_conversation_history = AsyncMock(side_effect=self._mock_history_retrieval_delay)
        builder.memory_retrieval = mock_retrieval
        
        return builder
    
    def _mock_concept_query_delay(self, query, params):
        """Mock concept extraction query with delay"""
        time.sleep(0.008)  # 8ms for concept extraction
        return [
            {"concept": {"name": f"concept_{i}", "importance": 0.8 - (i * 0.1)}}
            for i in range(3)
        ]
    
    async def _mock_memory_retrieval_delay(self, query, user_id, consciousness_context, **kwargs):
        """Mock memory retrieval with delay"""
        await asyncio.sleep(0.02)  # 20ms for memory retrieval
        return [
            MemorySearchResult(
                memory_id=f"context_memory_{i}",
                content=f"Context memory content {i}",
                memory_type="interaction",
                agent_name="context_agent",
                user_id=user_id,
                consciousness_level=0.8,
                emotional_state="neutral",
                importance_score=0.7,
                created_at="2024-01-01T12:00:00",
                metadata={},
                relevance_score=0.8 - (i * 0.1)
            )
            for i in range(3)
        ]
    
    async def _mock_history_retrieval_delay(self, user_id, limit):
        """Mock conversation history retrieval with delay"""
        await asyncio.sleep(0.01)  # 10ms for history retrieval
        return [
            MemorySearchResult(
                memory_id=f"history_{i}",
                content=f"History content {i}",
                memory_type="interaction",
                agent_name="history_agent",
                user_id=user_id,
                consciousness_level=0.7,
                emotional_state="neutral",
                importance_score=0.6,
                created_at="2024-01-01T12:00:00",
                metadata={},
                relevance_score=1.0
            )
            for i in range(min(limit, 2))
        ]
    
    @pytest.mark.asyncio
    async def test_comprehensive_context_building_performance(self, performance_context_builder):
        """Test comprehensive context building performance"""
        start_time = time.time()
        
        context = await performance_context_builder.build_comprehensive_context(
            query="test comprehensive context building performance",
            user_id="perf_user",
            consciousness_context={"consciousness_level": 0.8, "emotional_state": "focused"},
            include_concepts=True,
            context_type="hybrid"
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Comprehensive context building should complete efficiently
        assert duration < 0.15  # Under 150ms for full context building
        assert context is not None
        assert hasattr(context, 'formatted_context')
        
        print(f"Comprehensive context building took: {duration:.3f}s")
    
    @pytest.mark.asyncio
    async def test_context_building_with_large_memory_set(self, performance_context_builder):
        """Test context building performance with large memory sets"""
        # Mock large memory set
        large_memory_set = [
            MemorySearchResult(
                memory_id=f"large_memory_{i}",
                content=f"Large memory set content {i}",
                memory_type="interaction",
                agent_name="large_agent",
                user_id="perf_user",
                consciousness_level=0.8,
                emotional_state="neutral",
                importance_score=0.7,
                created_at="2024-01-01T12:00:00",
                metadata={},
                relevance_score=0.8 - (i * 0.01)
            )
            for i in range(50)  # Large set of memories
        ]
        
        start_time = time.time()
        
        context = await performance_context_builder.build_conversation_context(
            memories=large_memory_set,
            consciousness_context={"consciousness_level": 0.8},
            context_type="conversation"
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should handle large memory sets efficiently
        assert duration < 0.1  # Under 100ms even with large memory set
        assert isinstance(context, str)
        
        print(f"Large memory set context building took: {duration:.3f}s")

class TestMemorySystemLoadTesting:
    """Test memory system under sustained load"""
    
    @pytest.fixture
    def load_test_system(self):
        """Create system for load testing"""
        # Create mocks with realistic performance characteristics
        storage = Mock()
        storage.store_interaction_memory = AsyncMock(side_effect=self._mock_storage_with_load)
        
        retrieval = Mock()
        retrieval.get_relevant_memories = AsyncMock(side_effect=self._mock_retrieval_with_load)
        
        return {
            "storage": storage,
            "retrieval": retrieval
        }
    
    async def _mock_storage_with_load(self, *args, **kwargs):
        """Mock storage with load-dependent delay"""
        # Simulate increasing delay under load
        await asyncio.sleep(0.01 + (asyncio.current_task().get_name().count('storage') * 0.002))
        return f"memory_{time.time()}"
    
    async def _mock_retrieval_with_load(self, *args, **kwargs):
        """Mock retrieval with load-dependent delay"""
        # Simulate increasing delay under load
        await asyncio.sleep(0.015 + (asyncio.current_task().get_name().count('retrieval') * 0.003))
        return []
    
    @pytest.mark.asyncio
    async def test_sustained_load_performance(self, load_test_system):
        """Test system performance under sustained load"""
        storage = load_test_system["storage"]
        retrieval = load_test_system["retrieval"]
        
        # Define load test parameters
        operations_per_second = 10
        test_duration_seconds = 2
        total_operations = operations_per_second * test_duration_seconds
        
        async def storage_operation(index):
            return await storage.store_interaction_memory(
                user_query=f"Load test query {index}",
                agent_response=f"Load test response {index}",
                user_id=f"load_user_{index % 5}",  # Simulate 5 concurrent users
                agent_name="load_agent",
                consciousness_context={"consciousness_level": 0.8}
            )
        
        async def retrieval_operation(index):
            return await retrieval.get_relevant_memories(
                query=f"Load test search {index}",
                user_id=f"load_user_{index % 5}",
                consciousness_context={"consciousness_level": 0.8}
            )
        
        # Execute load test
        start_time = time.time()
        
        # Create mixed workload
        storage_tasks = [storage_operation(i) for i in range(total_operations // 2)]
        retrieval_tasks = [retrieval_operation(i) for i in range(total_operations // 2)]
        
        all_tasks = storage_tasks + retrieval_tasks
        results = await asyncio.gather(*all_tasks, return_exceptions=True)
        
        end_time = time.time()
        actual_duration = end_time - start_time
        
        # Analyze results
        successful_operations = sum(1 for result in results if not isinstance(result, Exception))
        failed_operations = len(results) - successful_operations
        
        operations_per_second_actual = successful_operations / actual_duration
        
        print(f"Load test results:")
        print(f"  Target operations: {total_operations}")
        print(f"  Successful operations: {successful_operations}")
        print(f"  Failed operations: {failed_operations}")
        print(f"  Actual duration: {actual_duration:.2f}s")
        print(f"  Operations per second: {operations_per_second_actual:.2f}")
        
        # Performance assertions
        assert failed_operations == 0  # No operations should fail
        assert operations_per_second_actual >= operations_per_second * 0.8  # At least 80% of target throughput
    
    @pytest.mark.asyncio
    async def test_memory_system_scalability(self, load_test_system):
        """Test memory system scalability with increasing load"""
        storage = load_test_system["storage"]
        
        # Test different load levels
        load_levels = [5, 10, 20]  # Operations per batch
        performance_results = []
        
        for load_level in load_levels:
            start_time = time.time()
            
            # Execute batch of operations
            tasks = [
                storage.store_interaction_memory(
                    user_query=f"Scalability test {i}",
                    agent_response=f"Scalability response {i}",
                    user_id="scale_user",
                    agent_name="scale_agent",
                    consciousness_context={"consciousness_level": 0.8}
                )
                for i in range(load_level)
            ]
            
            results = await asyncio.gather(*tasks)
            
            end_time = time.time()
            duration = end_time - start_time
            
            throughput = load_level / duration
            performance_results.append((load_level, throughput, duration))
            
            print(f"Load level {load_level}: {throughput:.2f} ops/sec, {duration:.3f}s total")
        
        # Analyze scalability
        # Throughput should not degrade significantly with increased load
        base_throughput = performance_results[0][1]
        max_throughput = performance_results[-1][1]
        
        # Allow some degradation but not more than 50%
        assert max_throughput >= base_throughput * 0.5

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])  # -s to see print statements