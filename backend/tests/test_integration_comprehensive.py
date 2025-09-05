"""
Comprehensive integration tests for Mainza backend.
Addresses critical testing gaps identified in code review:
- Multi-agent workflow testing
- End-to-end integration tests
- Performance testing
- Error handling validation
"""
import pytest
import asyncio
import time
from typing import Dict, Any, List
from unittest.mock import Mock, patch
import uuid

from backend.utils.neo4j_production import neo4j_production
from backend.utils.schema_manager import schema_manager
from backend.utils.neo4j_monitoring import initialize_monitoring
from backend.tools.graphmaster_tools_optimized import (
    cypher_query_secure,
    chunk_document_optimized,
    semantic_search_optimized,
    create_memory_batch,
    get_user_context_optimized
)
from backend.utils.embedding_enhanced import embedding_manager
from backend.config.production_config import config
from pydantic_ai import RunContext

class TestDatabaseIntegration:
    """Test database operations and schema management."""
    
    @pytest.fixture(autouse=True)
    def setup_database(self):
        """Setup test database state."""
        # Ensure schema is initialized
        schema_result = schema_manager.initialize_schema()
        assert schema_result["success"], f"Schema initialization failed: {schema_result}"
        
        # Initialize monitoring
        self.monitor = initialize_monitoring(neo4j_production)
        
        yield
        
        # Cleanup test data
        self.cleanup_test_data()
    
    def cleanup_test_data(self):
        """Clean up test data after tests."""
        try:
            cleanup_queries = [
                "MATCH (n:TestUser) DETACH DELETE n",
                "MATCH (n:TestDocument) DETACH DELETE n", 
                "MATCH (n:TestMemory) DETACH DELETE n",
                "MATCH (n:TestChunk) DETACH DELETE n"
            ]
            
            for query in cleanup_queries:
                try:
                    neo4j_production.execute_write_query(query)
                except Exception as e:
                    print(f"Cleanup warning: {e}")
        except Exception as e:
            print(f"Cleanup failed: {e}")
    
    def test_schema_validation_and_creation(self):
        """Test schema validation and creation process."""
        # Get current schema state
        validation = schema_manager.validate_schema()
        
        # Schema should be valid after initialization
        assert validation["valid"], f"Schema validation failed: {validation}"
        
        # Check for critical vector index
        current_schema = schema_manager.get_current_schema_info()
        index_names = {idx["name"] for idx in current_schema["indexes"]}
        assert "ChunkEmbeddingIndex" in index_names, "Critical vector index missing"
    
    def test_connection_pooling_and_resilience(self):
        """Test connection pooling and error resilience."""
        # Test multiple concurrent connections
        async def concurrent_query():
            ctx = Mock(spec=RunContext)
            result = cypher_query_secure(ctx, "RETURN 1 AS test")
            return result.result["result"][0]["test"]
        
        # Run multiple queries concurrently
        async def run_concurrent_tests():
            tasks = [concurrent_query() for _ in range(10)]
            results = await asyncio.gather(*tasks)
            return results
        
        results = asyncio.run(run_concurrent_tests())
        assert all(r == 1 for r in results), "Concurrent queries failed"
    
    def test_query_security_validation(self):
        """Test query security validation."""
        ctx = Mock(spec=RunContext)
        
        # Test dangerous query blocking
        dangerous_queries = [
            "DROP DATABASE neo4j",
            "DELETE ALL",
            "DETACH DELETE ALL",
            "LOAD CSV FROM 'file:///etc/passwd' AS line RETURN line"
        ]
        
        for dangerous_query in dangerous_queries:
            result = cypher_query_secure(ctx, dangerous_query)
            assert "error" in result.result, f"Dangerous query not blocked: {dangerous_query}"
            assert "blocked" in result.result["error"].lower()
    
    def test_transaction_management(self):
        """Test transaction management and rollback."""
        ctx = Mock(spec=RunContext)
        
        # Test successful transaction
        test_user_id = f"test-user-{uuid.uuid4()}"
        create_query = f"""
        CREATE (u:TestUser {{user_id: '{test_user_id}', name: 'Test User'}})
        RETURN u.user_id AS user_id
        """
        
        result = cypher_query_secure(ctx, create_query, read_only=False)
        assert result.result["status"] == "success"
        assert result.result["result"][0]["user_id"] == test_user_id
        
        # Verify user was created
        verify_query = f"MATCH (u:TestUser {{user_id: '{test_user_id}'}}) RETURN count(u) AS count"
        verify_result = cypher_query_secure(ctx, verify_query)
        assert verify_result.result["result"][0]["count"] == 1

class TestEmbeddingIntegration:
    """Test embedding generation and vector search integration."""
    
    def test_embedding_generation_and_caching(self):
        """Test embedding generation with caching."""
        test_text = "This is a test for embedding generation and caching"
        
        # First call - should generate embedding
        start_time = time.time()
        embedding1 = embedding_manager.get_embedding(test_text)
        first_call_time = time.time() - start_time
        
        # Second call - should use cache
        start_time = time.time()
        embedding2 = embedding_manager.get_embedding(test_text)
        second_call_time = time.time() - start_time
        
        # Verify embeddings are identical
        assert embedding1 == embedding2, "Cached embedding differs from original"
        
        # Verify caching improves performance
        assert second_call_time < first_call_time, "Caching did not improve performance"
        
        # Verify embedding quality
        assert len(embedding1) > 0, "Empty embedding generated"
        assert not all(x == 0.0 for x in embedding1), "Zero vector generated"
    
    def test_batch_embedding_performance(self):
        """Test batch embedding generation performance."""
        test_texts = [f"Test text number {i} for batch processing" for i in range(20)]
        
        # Test batch processing
        start_time = time.time()
        batch_embeddings = embedding_manager.get_embeddings_batch(test_texts, batch_size=5)
        batch_time = time.time() - start_time
        
        # Test individual processing
        start_time = time.time()
        individual_embeddings = [embedding_manager.get_embedding(text) for text in test_texts]
        individual_time = time.time() - start_time
        
        # Verify results are identical
        assert len(batch_embeddings) == len(individual_embeddings)
        for batch_emb, ind_emb in zip(batch_embeddings, individual_embeddings):
            assert batch_emb == ind_emb, "Batch and individual embeddings differ"
        
        # Batch processing should be more efficient for larger batches
        print(f"Batch time: {batch_time:.2f}s, Individual time: {individual_time:.2f}s")

class TestGraphMasterToolsIntegration:
    """Test GraphMaster tools integration and workflows."""
    
    @pytest.fixture(autouse=True)
    def setup_test_data(self):
        """Setup test data for GraphMaster tools."""
        self.ctx = Mock(spec=RunContext)
        self.test_document_id = f"test-doc-{uuid.uuid4()}"
        self.test_user_id = f"test-user-{uuid.uuid4()}"
        
        # Create test document
        create_doc_query = f"""
        CREATE (d:TestDocument {{
            document_id: '{self.test_document_id}',
            filename: 'test_document.txt',
            text: 'This is a comprehensive test document for testing chunking and vector search functionality. It contains multiple sentences and concepts that should be properly indexed and searchable through semantic search capabilities.',
            created_at: timestamp()
        }})
        RETURN d.document_id AS document_id
        """
        
        result = neo4j_production.execute_write_query(create_doc_query)
        assert result[0]["document_id"] == self.test_document_id
        
        # Create test user
        create_user_query = f"""
        CREATE (u:TestUser {{
            user_id: '{self.test_user_id}',
            name: 'Test User',
            created_at: timestamp()
        }})
        RETURN u.user_id AS user_id
        """
        
        result = neo4j_production.execute_write_query(create_user_query)
        assert result[0]["user_id"] == self.test_user_id
        
        yield
        
        # Cleanup
        cleanup_queries = [
            f"MATCH (d:TestDocument {{document_id: '{self.test_document_id}'}}) DETACH DELETE d",
            f"MATCH (u:TestUser {{user_id: '{self.test_user_id}'}}) DETACH DELETE u",
            f"MATCH (ch:Chunk)-[:DERIVED_FROM]->(d:TestDocument) DELETE ch",
            f"MATCH (m:TestMemory) DETACH DELETE m"
        ]
        
        for query in cleanup_queries:
            try:
                neo4j_production.execute_write_query(query)
            except Exception:
                pass
    
    def test_document_chunking_workflow(self):
        """Test complete document chunking workflow."""
        # Test document chunking
        result = chunk_document_optimized(
            self.ctx, 
            self.test_document_id, 
            chunk_size=100, 
            overlap=20
        )
        
        assert "chunks_created" in result.result
        assert result.result["chunks_created"] > 0
        chunks_created = result.result["chunks_created"]
        
        # Verify chunks were created with embeddings
        verify_query = f"""
        MATCH (ch:Chunk)-[:DERIVED_FROM]->(d:TestDocument {{document_id: '{self.test_document_id}'}})
        RETURN count(ch) AS chunk_count, 
               count(ch.embedding) AS embedding_count,
               avg(size(ch.embedding)) AS avg_embedding_size
        """
        
        verify_result = neo4j_production.execute_query(verify_query)
        assert verify_result[0]["chunk_count"] == chunks_created
        assert verify_result[0]["embedding_count"] == chunks_created
        assert verify_result[0]["avg_embedding_size"] > 0
    
    def test_semantic_search_workflow(self):
        """Test semantic search workflow."""
        # First chunk the document
        chunk_result = chunk_document_optimized(self.ctx, self.test_document_id, chunk_size=100)
        assert chunk_result.result["chunks_created"] > 0
        
        # Test semantic search
        search_result = semantic_search_optimized(
            self.ctx, 
            "test document functionality", 
            limit=5,
            similarity_threshold=0.1  # Lower threshold for test
        )
        
        assert "results" in search_result.result
        results = search_result.result["results"]
        
        # Should find relevant chunks
        assert len(results) > 0, "No search results found"
        
        # Verify result structure
        for result in results:
            assert "chunk_id" in result
            assert "text" in result
            assert "similarity_score" in result
            assert "document_id" in result
    
    def test_memory_batch_creation_workflow(self):
        """Test batch memory creation workflow."""
        test_memories = [
            {
                "text": f"Test memory {i} for batch creation",
                "source": "test",
                "user_id": self.test_user_id
            }
            for i in range(5)
        ]
        
        # Create memories in batch
        result = create_memory_batch(self.ctx, test_memories)
        
        assert "memories_created" in result.result
        assert result.result["memories_created"] == 5
        
        # Verify memories were created
        verify_query = f"""
        MATCH (m:Memory)-[:DISCUSSED_IN]->(u:TestUser {{user_id: '{self.test_user_id}'}})
        WHERE m.source = 'test'
        RETURN count(m) AS memory_count
        """
        
        verify_result = neo4j_production.execute_query(verify_query)
        assert verify_result[0]["memory_count"] == 5
    
    def test_user_context_retrieval_workflow(self):
        """Test user context retrieval workflow."""
        # Create test memories first
        test_memories = [
            {
                "text": "User likes artificial intelligence",
                "source": "conversation",
                "user_id": self.test_user_id
            },
            {
                "text": "User is interested in machine learning",
                "source": "conversation", 
                "user_id": self.test_user_id
            }
        ]
        
        create_memory_batch(self.ctx, test_memories)
        
        # Test context retrieval
        context_result = get_user_context_optimized(self.ctx, self.test_user_id, limit=10)
        
        assert "user_id" in context_result.result
        assert context_result.result["user_id"] == self.test_user_id
        assert "recent_memories" in context_result.result
        
        recent_memories = context_result.result["recent_memories"]
        assert len(recent_memories) == 2
        
        # Verify memory content
        memory_texts = [mem["text"] for mem in recent_memories]
        assert any("artificial intelligence" in text for text in memory_texts)
        assert any("machine learning" in text for text in memory_texts)

class TestPerformanceAndScalability:
    """Test performance characteristics and scalability."""
    
    def test_query_performance_monitoring(self):
        """Test query performance monitoring."""
        ctx = Mock(spec=RunContext)
        
        # Execute queries and monitor performance
        test_queries = [
            "MATCH (n) RETURN count(n) AS total_nodes",
            "MATCH ()-[r]->() RETURN count(r) AS total_relationships",
            "MATCH (m:Memory) RETURN count(m) AS memory_count"
        ]
        
        performance_results = []
        
        for query in test_queries:
            start_time = time.time()
            result = cypher_query_secure(ctx, query)
            execution_time = time.time() - start_time
            
            performance_results.append({
                "query": query,
                "execution_time": execution_time,
                "success": "error" not in result.result
            })
        
        # All queries should complete successfully
        assert all(r["success"] for r in performance_results)
        
        # No query should take longer than 5 seconds
        slow_queries = [r for r in performance_results if r["execution_time"] > 5.0]
        assert len(slow_queries) == 0, f"Slow queries detected: {slow_queries}"
    
    def test_concurrent_operations_scalability(self):
        """Test concurrent operations scalability."""
        async def concurrent_memory_creation():
            ctx = Mock(spec=RunContext)
            test_user_id = f"concurrent-user-{uuid.uuid4()}"
            
            # Create user first
            create_user_query = f"""
            CREATE (u:TestUser {{user_id: '{test_user_id}', name: 'Concurrent Test User'}})
            RETURN u.user_id AS user_id
            """
            neo4j_production.execute_write_query(create_user_query)
            
            # Create memories
            memories = [
                {
                    "text": f"Concurrent memory {i}",
                    "source": "concurrent_test",
                    "user_id": test_user_id
                }
                for i in range(5)
            ]
            
            result = create_memory_batch(ctx, memories)
            return result.result["memories_created"]
        
        async def run_concurrent_tests():
            tasks = [concurrent_memory_creation() for _ in range(3)]
            results = await asyncio.gather(*tasks)
            return results
        
        # Run concurrent memory creation
        results = asyncio.run(run_concurrent_tests())
        
        # All operations should succeed
        assert all(r == 5 for r in results), f"Concurrent operations failed: {results}"
    
    def test_large_batch_processing(self):
        """Test large batch processing performance."""
        ctx = Mock(spec=RunContext)
        
        # Create a large batch of memories
        large_batch = [
            {
                "text": f"Large batch memory {i} with some content to test performance",
                "source": "performance_test"
            }
            for i in range(100)
        ]
        
        start_time = time.time()
        result = create_memory_batch(ctx, large_batch)
        processing_time = time.time() - start_time
        
        # Should complete successfully
        assert result.result["memories_created"] == 100
        
        # Should complete within reasonable time (adjust threshold as needed)
        assert processing_time < 30.0, f"Large batch processing too slow: {processing_time:.2f}s"
        
        print(f"Large batch processing time: {processing_time:.2f}s")

class TestErrorHandlingAndRecovery:
    """Test error handling and recovery mechanisms."""
    
    def test_database_connection_recovery(self):
        """Test database connection recovery after failure."""
        # Test health check
        health_info = neo4j_production.health_check()
        assert health_info["status"] == "healthy"
        
        # Simulate connection issues by testing with invalid query
        ctx = Mock(spec=RunContext)
        result = cypher_query_secure(ctx, "INVALID CYPHER SYNTAX")
        
        # Should handle error gracefully
        assert "error" in result.result
        
        # Connection should still work for valid queries
        valid_result = cypher_query_secure(ctx, "RETURN 1 AS test")
        assert valid_result.result["result"][0]["test"] == 1
    
    def test_transaction_rollback_on_error(self):
        """Test transaction rollback on error."""
        ctx = Mock(spec=RunContext)
        test_user_id = f"rollback-test-{uuid.uuid4()}"
        
        # This should fail and rollback
        invalid_query = f"""
        CREATE (u:TestUser {{user_id: '{test_user_id}', name: 'Test User'}})
        CREATE (u2:TestUser {{user_id: '{test_user_id}', name: 'Duplicate User'}})
        RETURN u.user_id AS user_id
        """
        
        result = cypher_query_secure(ctx, invalid_query, read_only=False)
        
        # Should fail due to constraint violation
        assert "error" in result.result
        
        # Verify no user was created (transaction rolled back)
        verify_query = f"MATCH (u:TestUser {{user_id: '{test_user_id}'}}) RETURN count(u) AS count"
        verify_result = cypher_query_secure(ctx, verify_query)
        assert verify_result.result["result"][0]["count"] == 0
    
    def test_embedding_fallback_mechanisms(self):
        """Test embedding generation fallback mechanisms."""
        # Test with empty text
        empty_embedding = embedding_manager.get_embedding("")
        assert len(empty_embedding) > 0, "Should return zero vector for empty text"
        assert all(x == 0.0 for x in empty_embedding), "Should be zero vector for empty text"
        
        # Test with very long text
        long_text = "test " * 10000  # Very long text
        long_embedding = embedding_manager.get_embedding(long_text)
        assert len(long_embedding) > 0, "Should handle long text"
        assert not all(x == 0.0 for x in long_embedding), "Should generate valid embedding for long text"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])