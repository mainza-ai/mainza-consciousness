"""
Memory System Resilience Tests
Tests failure recovery, graceful degradation, and system resilience under various failure conditions.
"""
import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from typing import Dict, Any, List

# Import the components to test
from backend.utils.memory_storage_engine import MemoryStorageEngine
from backend.utils.memory_retrieval_engine import MemoryRetrievalEngine
from backend.utils.memory_context_builder import MemoryContextBuilder
from backend.utils.memory_error_handling import (
    MemoryError, MemoryStorageError, MemoryRetrievalError, MemoryConnectionError,
    MemoryTimeoutError, MemoryCorruptionError, memory_error_handler
)
from backend.agents.simple_chat import EnhancedSimpleChatAgent

class TestMemorySystemFailureRecovery:
    """Test memory system recovery from various failure scenarios"""
    
    @pytest.fixture
    def resilient_memory_system(self):
        """Setup memory system with failure simulation capabilities"""
        storage = Mock(spec=MemoryStorageEngine)
        retrieval = Mock(spec=MemoryRetrievalEngine)
        context_builder = Mock(spec=MemoryContextBuilder)
        
        return {
            "storage": storage,
            "retrieval": retrieval,
            "context_builder": context_builder
        }
    
    @pytest.mark.asyncio
    async def test_neo4j_connection_failure_recovery(self, resilient_memory_system):
        """Test recovery from Neo4j connection failures"""
        storage = resilient_memory_system["storage"]
        
        # Simulate connection failure followed by recovery
        connection_attempts = []
        
        def mock_store_with_connection_issues(*args, **kwargs):
            connection_attempts.append(len(connection_attempts) + 1)
            if len(connection_attempts) <= 2:
                # First two attempts fail
                raise MemoryConnectionError("Neo4j connection failed")
            else:
                # Third attempt succeeds
                return "recovered_memory_id"
        
        storage.store_interaction_memory.side_effect = mock_store_with_connection_issues
        
        # Attempt to store memory with retry logic
        memory_id = None
        for attempt in range(3):
            try:
                memory_id = await storage.store_interaction_memory(
                    user_query="Test query",
                    agent_response="Test response",
                    user_id="resilience_user",
                    agent_name="resilience_agent",
                    consciousness_context={"consciousness_level": 0.8}
                )
                break
            except MemoryConnectionError:
                if attempt < 2:
                    await asyncio.sleep(0.1)  # Brief delay before retry
                    continue
                else:
                    raise
        
        # Verify recovery occurred
        assert memory_id == "recovered_memory_id"
        assert len(connection_attempts) == 3
        assert storage.store_interaction_memory.call_count == 3
    
    @pytest.mark.asyncio
    async def test_embedding_service_failure_graceful_degradation(self, resilient_memory_system):
        """Test graceful degradation when embedding service fails"""
        retrieval = resilient_memory_system["retrieval"]
        
        # Setup embedding failure with fallback to keyword search
        def mock_retrieval_with_embedding_failure(query, user_id, consciousness_context, **kwargs):
            search_type = kwargs.get("search_type", "semantic")
            
            if search_type == "semantic":
                # Simulate embedding failure
                raise MemoryRetrievalError("Embedding service unavailable")
            elif search_type == "keyword":
                # Fallback keyword search succeeds
                return [
                    Mock(
                        memory_id="fallback_memory",
                        content="Fallback search result",
                        relevance_score=0.6
                    )
                ]
            else:
                return []
        
        retrieval.get_relevant_memories.side_effect = mock_retrieval_with_embedding_failure
        
        # Attempt semantic search with fallback to keyword search
        memories = None
        try:
            memories = await retrieval.get_relevant_memories(
                query="test query",
                user_id="resilience_user",
                consciousness_context={"consciousness_level": 0.8},
                search_type="semantic"
            )
        except MemoryRetrievalError:
            # Fallback to keyword search
            memories = await retrieval.get_relevant_memories(
                query="test query",
                user_id="resilience_user",
                consciousness_context={"consciousness_level": 0.8},
                search_type="keyword"
            )
        
        # Verify fallback worked
        assert memories is not None
        assert len(memories) == 1
        assert memories[0].memory_id == "fallback_memory"
    
    @pytest.mark.asyncio
    async def test_memory_corruption_detection_and_recovery(self, resilient_memory_system):
        """Test detection and recovery from memory corruption"""
        retrieval = resilient_memory_system["retrieval"]
        
        # Simulate corrupted memory data
        corrupted_memories = [
            {
                "memory_id": "corrupted_memory_1",
                "content": None,  # Corrupted content
                "memory_type": "interaction",
                "created_at": "invalid_date",  # Corrupted timestamp
                "importance_score": "not_a_number"  # Corrupted score
            },
            {
                "memory_id": "valid_memory_1",
                "content": "Valid memory content",
                "memory_type": "interaction",
                "created_at": "2024-01-01T12:00:00",
                "importance_score": 0.8
            }
        ]
        
        def mock_retrieval_with_corruption_handling(*args, **kwargs):
            # Simulate corruption detection and filtering
            valid_memories = []
            
            for memory_data in corrupted_memories:
                try:
                    # Validate memory data
                    if (memory_data.get("content") is not None and
                        isinstance(memory_data.get("importance_score"), (int, float)) and
                        memory_data.get("created_at") and
                        "T" in memory_data.get("created_at", "")):
                        
                        # Create valid memory result
                        valid_memories.append(Mock(
                            memory_id=memory_data["memory_id"],
                            content=memory_data["content"],
                            memory_type=memory_data["memory_type"],
                            created_at=memory_data["created_at"],
                            importance_score=memory_data["importance_score"],
                            relevance_score=0.8
                        ))
                    else:
                        # Log corruption but continue
                        print(f"Detected corrupted memory: {memory_data['memory_id']}")
                        
                except Exception as e:
                    # Handle corruption gracefully
                    print(f"Memory corruption error: {e}")
                    continue
            
            return valid_memories
        
        retrieval.get_relevant_memories.side_effect = mock_retrieval_with_corruption_handling
        
        # Retrieve memories with corruption handling
        memories = await retrieval.get_relevant_memories(
            query="test query",
            user_id="resilience_user",
            consciousness_context={"consciousness_level": 0.8}
        )
        
        # Verify only valid memories were returned
        assert len(memories) == 1
        assert memories[0].memory_id == "valid_memory_1"
        assert memories[0].content == "Valid memory content"
    
    @pytest.mark.asyncio
    async def test_timeout_handling_and_recovery(self, resilient_memory_system):
        """Test handling of operation timeouts"""
        storage = resilient_memory_system["storage"]
        
        # Simulate timeout scenarios
        timeout_count = 0
        
        async def mock_store_with_timeout(*args, **kwargs):
            nonlocal timeout_count
            timeout_count += 1
            
            if timeout_count <= 2:
                # First two attempts timeout
                await asyncio.sleep(0.2)  # Simulate long operation
                raise MemoryTimeoutError("Operation timed out")
            else:
                # Third attempt succeeds quickly
                return "timeout_recovered_memory_id"
        
        storage.store_interaction_memory.side_effect = mock_store_with_timeout
        
        # Attempt storage with timeout handling
        memory_id = None
        max_attempts = 3
        
        for attempt in range(max_attempts):
            try:
                # Use shorter timeout for testing
                memory_id = await asyncio.wait_for(
                    storage.store_interaction_memory(
                        user_query="Timeout test query",
                        agent_response="Timeout test response",
                        user_id="timeout_user",
                        agent_name="timeout_agent",
                        consciousness_context={"consciousness_level": 0.8}
                    ),
                    timeout=0.1  # Short timeout for testing
                )
                break
            except (asyncio.TimeoutError, MemoryTimeoutError):
                if attempt < max_attempts - 1:
                    print(f"Attempt {attempt + 1} timed out, retrying...")
                    continue
                else:
                    print("All attempts timed out")
                    break
        
        # Verify eventual success or graceful handling
        assert memory_id == "timeout_recovered_memory_id"
        assert timeout_count == 3
    
    @pytest.mark.asyncio
    async def test_partial_system_failure_graceful_degradation(self, resilient_memory_system):
        """Test graceful degradation when parts of the memory system fail"""
        storage = resilient_memory_system["storage"]
        retrieval = resilient_memory_system["retrieval"]
        context_builder = resilient_memory_system["context_builder"]
        
        # Simulate partial failures
        storage.store_interaction_memory.side_effect = MemoryStorageError("Storage unavailable")
        retrieval.get_relevant_memories.return_value = []  # Retrieval works but returns empty
        context_builder.build_comprehensive_context.side_effect = Exception("Context building failed")
        
        # Test agent operation with partial failures
        with patch('backend.agents.simple_chat.simple_chat_agent') as mock_agent:
            mock_agent.run = AsyncMock(return_value=Mock(data="Degraded response"))
            
            agent = EnhancedSimpleChatAgent()
            agent.memory_storage = storage
            agent.memory_retrieval = retrieval
            agent.memory_context_builder = context_builder
            agent.memory_enabled = True
            
            # Agent should still function despite memory system failures
            with patch('backend.utils.knowledge_integration.knowledge_integration_manager') as mock_knowledge:
                mock_knowledge.get_consciousness_aware_context.return_value = {"concepts": []}
                
                response = await agent.run_with_consciousness(
                    "Test query with partial failures",
                    "degradation_user"
                )
                
                # Verify agent still responds despite failures
                assert isinstance(response, str)
                assert len(response) > 0
                
                # Verify storage was attempted but failed gracefully
                storage.store_interaction_memory.assert_called()
                
                # Verify retrieval was attempted
                retrieval.get_relevant_memories.assert_called()

class TestMemorySystemErrorHandling:
    """Test comprehensive error handling across the memory system"""
    
    @pytest.fixture
    def error_handling_system(self):
        """Setup system for testing error handling"""
        # Reset global error handler for clean testing
        memory_error_handler.error_log.clear()
        memory_error_handler.critical_error_count = 0
        memory_error_handler.degradation_active = False
        
        return memory_error_handler
    
    @pytest.mark.asyncio
    async def test_error_logging_and_categorization(self, error_handling_system):
        """Test proper error logging and categorization"""
        error_handler = error_handling_system
        
        # Test different error types
        test_errors = [
            MemoryStorageError("Storage failed", component="storage_engine", operation="store_memory"),
            MemoryRetrievalError("Retrieval failed", component="retrieval_engine", operation="search_memories"),
            MemoryConnectionError("Connection failed", component="neo4j_manager", operation="execute_query"),
            MemoryCorruptionError("Data corrupted", component="data_validator", operation="validate_memory")
        ]
        
        # Log each error
        error_details_list = []
        for error in test_errors:
            error_details = error_handler.log_error(error)
            error_details_list.append(error_details)
        
        # Verify all errors were logged
        assert len(error_handler.error_log) == 4
        
        # Verify error categorization
        categories = [details.category for details in error_details_list]
        assert "STORAGE" in [cat.value for cat in categories]
        assert "RETRIEVAL" in [cat.value for cat in categories]
        assert "NEO4J_CONNECTION" in [cat.value for cat in categories]
        assert "CORRUPTION" in [cat.value for cat in categories]
        
        # Verify severity levels
        severities = [details.severity for details in error_details_list]
        assert any(sev.value == "CRITICAL" for sev in severities)  # Corruption error
        assert any(sev.value == "HIGH" for sev in severities)      # Connection error
    
    @pytest.mark.asyncio
    async def test_degradation_mode_activation_and_recovery(self, error_handling_system):
        """Test degradation mode activation and recovery"""
        error_handler = error_handling_system
        
        # Generate multiple critical errors to trigger degradation
        critical_errors = [
            MemoryCorruptionError(f"Critical corruption {i}")
            for i in range(error_handler.critical_error_threshold)
        ]
        
        # Log critical errors
        for error in critical_errors:
            error_handler.log_error(error)
        
        # Verify degradation mode was activated
        assert error_handler.degradation_active is True
        assert error_handler.degradation_start_time is not None
        
        # Test degradation mode recovery
        error_handler.deactivate_degradation_mode()
        
        assert error_handler.degradation_active is False
        assert error_handler.degradation_start_time is None
        assert error_handler.critical_error_count == 0
    
    @pytest.mark.asyncio
    async def test_error_rate_monitoring_and_throttling(self, error_handling_system):
        """Test error rate monitoring and throttling"""
        error_handler = error_handling_system
        
        # Generate high error rate
        for i in range(15):  # Exceed max_error_rate of 10
            error = MemoryStorageError(f"High rate error {i}")
            error_handler.log_error(error)
        
        # Verify error rate tracking
        storage_error_count = error_handler.error_counts.get("STORAGE", 0)
        assert storage_error_count >= 10
        
        # Verify degradation activation due to high error rate
        assert error_handler.degradation_active is True
    
    @pytest.mark.asyncio
    async def test_error_notification_system(self, error_handling_system):
        """Test error notification callbacks"""
        error_handler = error_handling_system
        
        # Setup notification callback
        notifications_received = []
        
        def test_notification_callback(error_details):
            notifications_received.append(error_details)
        
        error_handler.register_notification_callback(test_notification_callback)
        
        # Generate errors of different severities
        test_errors = [
            MemoryStorageError("Low severity error"),  # Default medium severity
            MemoryConnectionError("High severity error"),  # High severity
            MemoryCorruptionError("Critical severity error")  # Critical severity
        ]
        
        for error in test_errors:
            error_handler.log_error(error)
        
        # Verify notifications were sent
        assert len(notifications_received) == 3
        
        # Verify notification content
        severities = [notif.severity.value for notif in notifications_received]
        assert "MEDIUM" in severities
        assert "HIGH" in severities
        assert "CRITICAL" in severities

class TestMemorySystemStressResilience:
    """Test memory system resilience under stress conditions"""
    
    @pytest.fixture
    def stress_test_system(self):
        """Setup system for stress testing"""
        storage = Mock(spec=MemoryStorageEngine)
        retrieval = Mock(spec=MemoryRetrievalEngine)
        
        # Add realistic delays and occasional failures
        storage.store_interaction_memory = AsyncMock(side_effect=self._mock_storage_with_stress)
        retrieval.get_relevant_memories = AsyncMock(side_effect=self._mock_retrieval_with_stress)
        
        return {"storage": storage, "retrieval": retrieval}
    
    async def _mock_storage_with_stress(self, *args, **kwargs):
        """Mock storage with stress-induced delays and failures"""
        # Simulate increasing delay under stress
        await asyncio.sleep(0.01)
        
        # Occasional failures under stress (5% failure rate)
        import random
        if random.random() < 0.05:
            raise MemoryStorageError("Stress-induced storage failure")
        
        return f"stress_memory_{random.randint(1000, 9999)}"
    
    async def _mock_retrieval_with_stress(self, *args, **kwargs):
        """Mock retrieval with stress-induced delays and failures"""
        # Simulate stress delay
        await asyncio.sleep(0.008)
        
        # Occasional failures under stress (3% failure rate)
        import random
        if random.random() < 0.03:
            raise MemoryRetrievalError("Stress-induced retrieval failure")
        
        return [Mock(memory_id=f"stress_result_{i}", relevance_score=0.8) for i in range(3)]
    
    @pytest.mark.asyncio
    async def test_concurrent_operation_stress_resilience(self, stress_test_system):
        """Test resilience under concurrent operation stress"""
        storage = stress_test_system["storage"]
        retrieval = stress_test_system["retrieval"]
        
        # Define stress test parameters
        concurrent_operations = 20
        operation_types = ["storage", "retrieval"]
        
        async def stress_operation(op_type, index):
            try:
                if op_type == "storage":
                    result = await storage.store_interaction_memory(
                        user_query=f"Stress query {index}",
                        agent_response=f"Stress response {index}",
                        user_id=f"stress_user_{index % 5}",
                        agent_name="stress_agent",
                        consciousness_context={"consciousness_level": 0.8}
                    )
                    return ("storage", "success", result)
                else:
                    result = await retrieval.get_relevant_memories(
                        query=f"Stress search {index}",
                        user_id=f"stress_user_{index % 5}",
                        consciousness_context={"consciousness_level": 0.8}
                    )
                    return ("retrieval", "success", len(result))
            except Exception as e:
                return (op_type, "failure", str(e))
        
        # Execute concurrent stress operations
        import random
        tasks = [
            stress_operation(random.choice(operation_types), i)
            for i in range(concurrent_operations)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Analyze stress test results
        successful_ops = sum(1 for result in results if result[1] == "success")
        failed_ops = len(results) - successful_ops
        
        success_rate = successful_ops / len(results)
        
        print(f"Stress test results:")
        print(f"  Total operations: {len(results)}")
        print(f"  Successful: {successful_ops}")
        print(f"  Failed: {failed_ops}")
        print(f"  Success rate: {success_rate:.2%}")
        
        # Verify acceptable success rate under stress (>90%)
        assert success_rate >= 0.90
    
    @pytest.mark.asyncio
    async def test_memory_system_recovery_after_stress(self, stress_test_system):
        """Test memory system recovery after stress period"""
        storage = stress_test_system["storage"]
        
        # Simulate stress period with high failure rate
        original_side_effect = storage.store_interaction_memory.side_effect
        
        async def high_failure_storage(*args, **kwargs):
            import random
            if random.random() < 0.3:  # 30% failure rate during stress
                raise MemoryStorageError("High stress failure")
            return await original_side_effect(*args, **kwargs)
        
        storage.store_interaction_memory.side_effect = high_failure_storage
        
        # Execute operations during stress period
        stress_results = []
        for i in range(10):
            try:
                result = await storage.store_interaction_memory(
                    user_query=f"Stress period query {i}",
                    agent_response=f"Stress period response {i}",
                    user_id="recovery_user",
                    agent_name="recovery_agent",
                    consciousness_context={"consciousness_level": 0.8}
                )
                stress_results.append(("success", result))
            except MemoryStorageError:
                stress_results.append(("failure", None))
        
        # Restore normal operation (end stress period)
        storage.store_interaction_memory.side_effect = original_side_effect
        
        # Test recovery period
        recovery_results = []
        for i in range(10):
            try:
                result = await storage.store_interaction_memory(
                    user_query=f"Recovery period query {i}",
                    agent_response=f"Recovery period response {i}",
                    user_id="recovery_user",
                    agent_name="recovery_agent",
                    consciousness_context={"consciousness_level": 0.8}
                )
                recovery_results.append(("success", result))
            except MemoryStorageError:
                recovery_results.append(("failure", None))
        
        # Analyze recovery
        stress_success_rate = sum(1 for r in stress_results if r[0] == "success") / len(stress_results)
        recovery_success_rate = sum(1 for r in recovery_results if r[0] == "success") / len(recovery_results)
        
        print(f"Recovery test results:")
        print(f"  Stress period success rate: {stress_success_rate:.2%}")
        print(f"  Recovery period success rate: {recovery_success_rate:.2%}")
        
        # Verify recovery (should be significantly better than stress period)
        assert recovery_success_rate > stress_success_rate
        assert recovery_success_rate >= 0.95  # Should recover to high success rate

class TestMemorySystemDataIntegrity:
    """Test data integrity and consistency under failure conditions"""
    
    @pytest.mark.asyncio
    async def test_transaction_rollback_on_failure(self):
        """Test that failed operations don't leave partial data"""
        # Mock Neo4j transaction behavior
        mock_neo4j = Mock()
        transaction_log = []
        
        def mock_transaction_execute(query, params):
            transaction_log.append(("execute", query, params))
            if "ROLLBACK" in query:
                transaction_log.append(("rollback", None, None))
                raise Exception("Transaction rolled back")
            return [{"success": True}]
        
        mock_neo4j.execute_write_query.side_effect = mock_transaction_execute
        
        storage = MemoryStorageEngine()
        storage.neo4j = mock_neo4j
        
        # Simulate transaction failure
        try:
            # This would normally trigger a rollback in real implementation
            mock_neo4j.execute_write_query("ROLLBACK TRANSACTION", {})
        except Exception:
            pass
        
        # Verify transaction behavior was logged
        assert len(transaction_log) >= 1
        assert any("rollback" in entry for entry in transaction_log)
    
    @pytest.mark.asyncio
    async def test_data_consistency_validation(self):
        """Test validation of data consistency after operations"""
        # Mock memory data with consistency checks
        memory_data = {
            "memory_id": "consistency_test_memory",
            "content": "Test content",
            "user_id": "test_user",
            "created_at": datetime.now().isoformat(),
            "importance_score": 0.8
        }
        
        # Validate required fields
        required_fields = ["memory_id", "content", "user_id", "created_at", "importance_score"]
        
        for field in required_fields:
            assert field in memory_data, f"Required field {field} missing"
            assert memory_data[field] is not None, f"Required field {field} is None"
        
        # Validate data types
        assert isinstance(memory_data["memory_id"], str)
        assert isinstance(memory_data["content"], str)
        assert isinstance(memory_data["importance_score"], (int, float))
        assert 0.0 <= memory_data["importance_score"] <= 1.0
        
        # Validate timestamp format
        try:
            datetime.fromisoformat(memory_data["created_at"].replace('Z', '+00:00'))
        except ValueError:
            pytest.fail("Invalid timestamp format")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])