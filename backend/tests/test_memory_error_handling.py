"""
Comprehensive tests for memory error handling system
Tests error scenarios, graceful degradation, and recovery mechanisms.
"""
import pytest
import asyncio
import logging
import os
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, Any, List

# Set environment variables before importing modules that need them
os.environ.setdefault('NEO4J_PASSWORD', 'test_password')
os.environ.setdefault('NEO4J_URI', 'bolt://localhost:7687')
os.environ.setdefault('NEO4J_USER', 'neo4j')

from backend.utils.memory_error_handling import (
    MemoryError, MemoryStorageError, MemoryRetrievalError, MemoryContextError,
    MemoryEmbeddingError, MemoryConnectionError, MemoryValidationError,
    MemoryCorruptionError, MemoryTimeoutError, MemoryResourceError,
    MemoryErrorHandler, MemoryErrorSeverity, MemoryErrorCategory,
    handle_memory_errors, safe_memory_operation, safe_async_memory_operation,
    memory_error_handler
)

class TestMemoryErrorClasses:
    """Test memory-specific exception classes"""
    
    def test_memory_error_base_class(self):
        """Test base MemoryError class"""
        error = MemoryError(
            "Test error",
            category=MemoryErrorCategory.STORAGE,
            severity=MemoryErrorSeverity.HIGH,
            component="test_component",
            operation="test_operation",
            context={"key": "value"}
        )
        
        assert str(error) == "Test error"
        assert error.category == MemoryErrorCategory.STORAGE
        assert error.severity == MemoryErrorSeverity.HIGH
        assert error.component == "test_component"
        assert error.operation == "test_operation"
        assert error.context == {"key": "value"}
        assert error.error_id is not None
        assert isinstance(error.timestamp, datetime)
    
    def test_memory_storage_error(self):
        """Test MemoryStorageError specific behavior"""
        error = MemoryStorageError("Storage failed")
        
        assert error.category == MemoryErrorCategory.STORAGE
        assert str(error) == "Storage failed"
    
    def test_memory_retrieval_error(self):
        """Test MemoryRetrievalError specific behavior"""
        error = MemoryRetrievalError("Retrieval failed")
        
        assert error.category == MemoryErrorCategory.RETRIEVAL
        assert str(error) == "Retrieval failed"
    
    def test_memory_connection_error(self):
        """Test MemoryConnectionError specific behavior"""
        error = MemoryConnectionError("Connection failed")
        
        assert error.category == MemoryErrorCategory.NEO4J_CONNECTION
        assert error.severity == MemoryErrorSeverity.HIGH
        assert str(error) == "Connection failed"
    
    def test_memory_corruption_error(self):
        """Test MemoryCorruptionError specific behavior"""
        error = MemoryCorruptionError("Data corrupted")
        
        assert error.category == MemoryErrorCategory.CORRUPTION
        assert error.severity == MemoryErrorSeverity.CRITICAL
        assert str(error) == "Data corrupted"

class TestMemoryErrorHandler:
    """Test MemoryErrorHandler functionality"""
    
    def setup_method(self):
        """Setup for each test"""
        self.handler = MemoryErrorHandler()
    
    def test_error_logging(self):
        """Test error logging functionality"""
        error = MemoryStorageError(
            "Test storage error",
            component="test_storage",
            operation="store_memory"
        )
        
        error_details = self.handler.log_error(
            error,
            user_id="test_user",
            memory_id="test_memory",
            additional_context={"test": "context"}
        )
        
        assert error_details.error_id == error.error_id
        assert error_details.category == MemoryErrorCategory.STORAGE
        assert error_details.user_id == "test_user"
        assert error_details.memory_id == "test_memory"
        assert "test" in error_details.context
        
        # Check error was added to log
        assert len(self.handler.error_log) == 1
        assert self.handler.error_counts[MemoryErrorCategory.STORAGE] == 1
    
    def test_critical_error_handling(self):
        """Test critical error handling and degradation activation"""
        # Create multiple critical errors
        for i in range(6):  # Exceed threshold of 5
            error = MemoryCorruptionError(f"Critical error {i}")
            self.handler.log_error(error)
        
        # Should activate degradation mode
        assert self.handler.is_degradation_active()
        assert self.handler.critical_error_count >= 5
    
    def test_degradation_mode_timeout(self):
        """Test degradation mode auto-deactivation after timeout"""
        # Activate degradation mode
        self.handler.activate_degradation_mode()
        assert self.handler.is_degradation_active()
        
        # Simulate timeout by setting start time in the past
        self.handler.degradation_start_time = datetime.now() - timedelta(minutes=35)
        
        # Check should deactivate
        assert not self.handler.is_degradation_active()
    
    def test_notification_callbacks(self):
        """Test error notification callbacks"""
        callback_called = False
        callback_error = None
        
        def test_callback(error_details):
            nonlocal callback_called, callback_error
            callback_called = True
            callback_error = error_details
        
        self.handler.register_notification_callback(test_callback)
        
        error = MemoryStorageError("Test error", severity=MemoryErrorSeverity.HIGH)
        self.handler.log_error(error)
        
        assert callback_called
        assert callback_error.error_id == error.error_id
    
    def test_error_summary(self):
        """Test error summary generation"""
        # Add some errors
        self.handler.log_error(MemoryStorageError("Storage error 1"))
        self.handler.log_error(MemoryRetrievalError("Retrieval error 1"))
        self.handler.log_error(MemoryStorageError("Storage error 2"))
        
        summary = self.handler.get_error_summary()
        
        assert summary["total_errors"] == 3
        assert summary["error_counts_by_category"][MemoryErrorCategory.STORAGE] == 2
        assert summary["error_counts_by_category"][MemoryErrorCategory.RETRIEVAL] == 1
        assert "degradation_active" in summary

class TestMemoryErrorDecorator:
    """Test handle_memory_errors decorator"""
    
    @pytest.mark.asyncio
    async def test_successful_operation(self):
        """Test decorator with successful operation"""
        
        @handle_memory_errors(
            component="test",
            operation="test_op",
            fallback_result="fallback"
        )
        async def test_function():
            return "success"
        
        result = await test_function()
        assert result == "success"
    
    @pytest.mark.asyncio
    async def test_memory_error_handling(self):
        """Test decorator handling MemoryError"""
        
        @handle_memory_errors(
            component="test",
            operation="test_op",
            fallback_result="fallback",
            suppress_errors=True
        )
        async def test_function():
            raise MemoryStorageError("Test error")
        
        result = await test_function()
        assert result == "fallback"
    
    @pytest.mark.asyncio
    async def test_timeout_handling(self):
        """Test decorator timeout handling"""
        
        @handle_memory_errors(
            component="test",
            operation="test_op",
            fallback_result="timeout_fallback",
            suppress_errors=True,
            timeout_seconds=0.1
        )
        async def test_function():
            await asyncio.sleep(0.2)  # Longer than timeout
            return "success"
        
        result = await test_function()
        assert result == "timeout_fallback"
    
    @pytest.mark.asyncio
    async def test_retry_mechanism(self):
        """Test decorator retry mechanism"""
        call_count = 0
        
        @handle_memory_errors(
            component="test",
            operation="test_op",
            fallback_result="fallback",
            suppress_errors=True,
            retry_attempts=2,
            retry_delay=0.01
        )
        async def test_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:  # Fail first 2 attempts
                raise MemoryConnectionError("Connection failed")
            return "success"
        
        result = await test_function()
        assert result == "success"
        assert call_count == 3
    
    @pytest.mark.asyncio
    async def test_retry_exhaustion(self):
        """Test decorator when retries are exhausted"""
        call_count = 0
        
        @handle_memory_errors(
            component="test",
            operation="test_op",
            fallback_result="fallback",
            suppress_errors=True,
            retry_attempts=2,
            retry_delay=0.01
        )
        async def test_function():
            nonlocal call_count
            call_count += 1
            raise MemoryConnectionError("Connection failed")
        
        result = await test_function()
        assert result == "fallback"
        assert call_count == 3  # Original + 2 retries
    
    def test_sync_function_handling(self):
        """Test decorator with synchronous functions"""
        
        @handle_memory_errors(
            component="test",
            operation="test_op",
            fallback_result="fallback",
            suppress_errors=True
        )
        def test_function():
            raise MemoryValidationError("Validation failed")
        
        result = test_function()
        assert result == "fallback"
    
    @pytest.mark.asyncio
    async def test_unexpected_error_wrapping(self):
        """Test decorator wrapping unexpected errors"""
        
        @handle_memory_errors(
            component="test",
            operation="test_op",
            fallback_result="fallback",
            suppress_errors=True
        )
        async def test_function():
            raise ValueError("Unexpected error")
        
        result = await test_function()
        assert result == "fallback"

class TestSafeMemoryOperations:
    """Test safe memory operation utilities"""
    
    def test_safe_memory_operation_success(self):
        """Test safe_memory_operation with successful operation"""
        
        def test_operation():
            return "success"
        
        result = safe_memory_operation(
            test_operation,
            fallback_result="fallback"
        )
        
        assert result == "success"
    
    def test_safe_memory_operation_failure(self):
        """Test safe_memory_operation with failure"""
        
        def test_operation():
            raise MemoryStorageError("Storage failed")
        
        result = safe_memory_operation(
            test_operation,
            fallback_result="fallback"
        )
        
        assert result == "fallback"
    
    @pytest.mark.asyncio
    async def test_safe_async_memory_operation_success(self):
        """Test safe_async_memory_operation with successful operation"""
        
        async def test_operation():
            return "success"
        
        result = await safe_async_memory_operation(
            test_operation,
            fallback_result="fallback"
        )
        
        assert result == "success"
    
    @pytest.mark.asyncio
    async def test_safe_async_memory_operation_timeout(self):
        """Test safe_async_memory_operation with timeout"""
        
        async def test_operation():
            await asyncio.sleep(0.2)
            return "success"
        
        result = await safe_async_memory_operation(
            test_operation,
            fallback_result="timeout_fallback",
            timeout_seconds=0.1
        )
        
        assert result == "timeout_fallback"

class TestMemoryErrorIntegration:
    """Test memory error handling integration scenarios"""
    
    def setup_method(self):
        """Setup for each test"""
        # Reset global error handler state
        memory_error_handler.error_log.clear()
        memory_error_handler.error_counts = {
            category: 0 for category in MemoryErrorCategory
        }
        memory_error_handler.critical_error_count = 0
        memory_error_handler.deactivate_degradation_mode()
    
    def test_error_rate_monitoring(self):
        """Test error rate monitoring and degradation activation"""
        # Generate high error rate
        for i in range(12):  # Exceed max_error_rate of 10
            error = MemoryStorageError(f"Error {i}")
            memory_error_handler.log_error(error)
        
        # Should trigger degradation mode
        assert memory_error_handler.is_degradation_active()
    
    def test_mixed_error_scenarios(self):
        """Test handling of mixed error types and severities"""
        errors = [
            MemoryStorageError("Storage error", severity=MemoryErrorSeverity.LOW),
            MemoryRetrievalError("Retrieval error", severity=MemoryErrorSeverity.MEDIUM),
            MemoryConnectionError("Connection error", severity=MemoryErrorSeverity.HIGH),
            MemoryCorruptionError("Corruption error", severity=MemoryErrorSeverity.CRITICAL)
        ]
        
        for error in errors:
            memory_error_handler.log_error(error)
        
        # Check all errors were logged
        assert len(memory_error_handler.error_log) == 4
        
        # Check error counts by category
        assert memory_error_handler.error_counts[MemoryErrorCategory.STORAGE] == 1
        assert memory_error_handler.error_counts[MemoryErrorCategory.RETRIEVAL] == 1
        assert memory_error_handler.error_counts[MemoryErrorCategory.NEO4J_CONNECTION] == 1
        assert memory_error_handler.error_counts[MemoryErrorCategory.CORRUPTION] == 1
        
        # Critical error should increment counter
        assert memory_error_handler.critical_error_count == 1
    
    @pytest.mark.asyncio
    async def test_concurrent_error_handling(self):
        """Test error handling under concurrent operations"""
        
        @handle_memory_errors(
            component="concurrent_test",
            operation="concurrent_op",
            fallback_result="fallback",
            suppress_errors=True
        )
        async def concurrent_operation(operation_id: int):
            if operation_id % 3 == 0:  # Every 3rd operation fails
                raise MemoryStorageError(f"Operation {operation_id} failed")
            return f"success_{operation_id}"
        
        # Run multiple concurrent operations
        tasks = [concurrent_operation(i) for i in range(10)]
        results = await asyncio.gather(*tasks)
        
        # Check results
        success_count = sum(1 for r in results if r.startswith("success"))
        fallback_count = sum(1 for r in results if r == "fallback")
        
        assert success_count > 0
        assert fallback_count > 0
        assert success_count + fallback_count == 10
    
    def test_error_context_preservation(self):
        """Test that error context is properly preserved"""
        original_error = ValueError("Original error")
        
        memory_error = MemoryStorageError(
            "Wrapped error",
            component="test_component",
            operation="test_operation",
            context={"user_id": "test_user", "data": "test_data"},
            original_error=original_error
        )
        
        error_details = memory_error_handler.log_error(
            memory_error,
            user_id="test_user",
            memory_id="test_memory",
            additional_context={"additional": "context"}
        )
        
        # Check context preservation
        assert error_details.context["user_id"] == "test_user"
        assert error_details.context["data"] == "test_data"
        assert error_details.context["additional"] == "context"
        assert error_details.user_id == "test_user"
        assert error_details.memory_id == "test_memory"

if __name__ == "__main__":
    pytest.main([__file__])