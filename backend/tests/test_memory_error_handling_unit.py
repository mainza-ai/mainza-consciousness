"""
Comprehensive unit tests for Memory Error Handling
Tests error classes, error handler functionality, and graceful degradation mechanisms.
"""
import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from typing import Dict, Any, List

# Import the components to test
from backend.utils.memory_error_handling import (
    MemoryError, MemoryStorageError, MemoryRetrievalError, MemoryContextError,
    MemoryEmbeddingError, MemoryConnectionError, MemoryValidationError,
    MemoryCorruptionError, MemoryTimeoutError, MemoryResourceError,
    MemoryErrorSeverity, MemoryErrorCategory, MemoryErrorDetails,
    MemoryErrorHandler, memory_error_handler,
    handle_memory_errors, safe_memory_operation, safe_async_memory_operation,
    create_memory_error_notification_callback
)

class TestMemoryErrorClasses:
    """Test memory error exception classes"""
    
    def test_memory_error_base_class(self):
        """Test base MemoryError class"""
        error = MemoryError(
            message="Test error",
            category=MemoryErrorCategory.STORAGE,
            severity=MemoryErrorSeverity.HIGH,
            component="test_component",
            operation="test_operation",
            context={"test": "data"}
        )
        
        assert str(error) == "Test error"
        assert error.category == MemoryErrorCategory.STORAGE
        assert error.severity == MemoryErrorSeverity.HIGH
        assert error.component == "test_component"
        assert error.operation == "test_operation"
        assert error.context == {"test": "data"}
        assert error.original_error is None
        assert isinstance(error.timestamp, datetime)
        assert len(error.error_id) == 8  # UUID truncated to 8 chars
    
    def test_memory_error_with_original_error(self):
        """Test MemoryError with original exception"""
        original = ValueError("Original error")
        
        error = MemoryError(
            message="Wrapped error",
            original_error=original
        )
        
        assert error.original_error == original
        assert str(error) == "Wrapped error"
    
    def test_memory_storage_error(self):
        """Test MemoryStorageError specialization"""
        error = MemoryStorageError(
            message="Storage failed",
            component="storage_engine",
            operation="store_memory"
        )
        
        assert isinstance(error, MemoryError)
        assert error.category == MemoryErrorCategory.STORAGE
        assert str(error) == "Storage failed"
    
    def test_memory_retrieval_error(self):
        """Test MemoryRetrievalError specialization"""
        error = MemoryRetrievalError(
            message="Retrieval failed",
            severity=MemoryErrorSeverity.HIGH
        )
        
        assert isinstance(error, MemoryError)
        assert error.category == MemoryErrorCategory.RETRIEVAL
        assert error.severity == MemoryErrorSeverity.HIGH
    
    def test_memory_context_error(self):
        """Test MemoryContextError specialization"""
        error = MemoryContextError("Context building failed")
        
        assert isinstance(error, MemoryError)
        assert error.category == MemoryErrorCategory.CONTEXT
    
    def test_memory_embedding_error(self):
        """Test MemoryEmbeddingError specialization"""
        error = MemoryEmbeddingError("Embedding generation failed")
        
        assert isinstance(error, MemoryError)
        assert error.category == MemoryErrorCategory.EMBEDDING
    
    def test_memory_connection_error(self):
        """Test MemoryConnectionError specialization"""
        error = MemoryConnectionError("Neo4j connection failed")
        
        assert isinstance(error, MemoryError)
        assert error.category == MemoryErrorCategory.NEO4J_CONNECTION
        assert error.severity == MemoryErrorSeverity.HIGH
    
    def test_memory_validation_error(self):
        """Test MemoryValidationError specialization"""
        error = MemoryValidationError("Invalid memory data")
        
        assert isinstance(error, MemoryError)
        assert error.category == MemoryErrorCategory.VALIDATION
    
    def test_memory_corruption_error(self):
        """Test MemoryCorruptionError specialization"""
        error = MemoryCorruptionError("Memory data corrupted")
        
        assert isinstance(error, MemoryError)
        assert error.category == MemoryErrorCategory.CORRUPTION
        assert error.severity == MemoryErrorSeverity.CRITICAL
    
    def test_memory_timeout_error(self):
        """Test MemoryTimeoutError specialization"""
        error = MemoryTimeoutError("Operation timed out")
        
        assert isinstance(error, MemoryError)
        assert error.category == MemoryErrorCategory.TIMEOUT
    
    def test_memory_resource_error(self):
        """Test MemoryResourceError specialization"""
        error = MemoryResourceError("Resource limit exceeded")
        
        assert isinstance(error, MemoryError)
        assert error.category == MemoryErrorCategory.RESOURCE
        assert error.severity == MemoryErrorSeverity.HIGH

class TestMemoryErrorDetails:
    """Test MemoryErrorDetails dataclass"""
    
    def test_error_details_creation(self):
        """Test error details creation"""
        timestamp = datetime.now()
        
        details = MemoryErrorDetails(
            error_id="test_error",
            category=MemoryErrorCategory.STORAGE,
            severity=MemoryErrorSeverity.HIGH,
            message="Test error message",
            component="test_component",
            operation="test_operation",
            timestamp=timestamp,
            user_id="test_user",
            memory_id="test_memory",
            context={"test": "data"},
            stack_trace="test stack trace"
        )
        
        assert details.error_id == "test_error"
        assert details.category == MemoryErrorCategory.STORAGE
        assert details.severity == MemoryErrorSeverity.HIGH
        assert details.message == "Test error message"
        assert details.component == "test_component"
        assert details.operation == "test_operation"
        assert details.timestamp == timestamp
        assert details.user_id == "test_user"
        assert details.memory_id == "test_memory"
        assert details.context == {"test": "data"}
        assert details.stack_trace == "test stack trace"
        assert details.recovery_attempted is False
        assert details.recovery_successful is False

class TestMemoryErrorHandler:
    """Test MemoryErrorHandler class"""
    
    @pytest.fixture
    def error_handler(self):
        """Create fresh error handler for testing"""
        return MemoryErrorHandler()
    
    @pytest.fixture
    def sample_error(self):
        """Create sample memory error for testing"""
        return MemoryStorageError(
            message="Test storage error",
            component="test_component",
            operation="test_operation",
            context={"test": "data"}
        )
    
    def test_error_handler_initialization(self, error_handler):
        """Test error handler initialization"""
        assert error_handler.error_log == []
        assert error_handler.max_error_log_size == 1000
        assert error_handler.notification_callbacks == []
        assert error_handler.critical_error_threshold == 5
        assert error_handler.critical_error_count == 0
        assert error_handler.degradation_active is False
        assert error_handler.degradation_start_time is None
        assert len(error_handler.error_counts) == len(MemoryErrorCategory)
    
    def test_register_notification_callback(self, error_handler):
        """Test registering notification callbacks"""
        callback = Mock()
        
        error_handler.register_notification_callback(callback)
        
        assert callback in error_handler.notification_callbacks
    
    def test_log_error_basic(self, error_handler, sample_error):
        """Test basic error logging"""
        error_details = error_handler.log_error(sample_error)
        
        assert isinstance(error_details, MemoryErrorDetails)
        assert error_details.message == "Test storage error"
        assert error_details.category == MemoryErrorCategory.STORAGE
        assert error_details.component == "test_component"
        assert error_details.operation == "test_operation"
        assert len(error_handler.error_log) == 1
        assert error_handler.error_counts[MemoryErrorCategory.STORAGE] == 1
    
    def test_log_error_with_additional_context(self, error_handler, sample_error):
        """Test error logging with additional context"""
        additional_context = {"additional": "info", "user_action": "test"}
        
        error_details = error_handler.log_error(
            sample_error,
            user_id="test_user",
            memory_id="test_memory",
            additional_context=additional_context
        )
        
        assert error_details.user_id == "test_user"
        assert error_details.memory_id == "test_memory"
        assert "additional" in error_details.context
        assert "test" in error_details.context  # Original context
        assert "user_action" in error_details.context  # Additional context
    
    def test_log_critical_error(self, error_handler):
        """Test logging critical errors"""
        critical_error = MemoryCorruptionError(
            message="Critical corruption detected",
            component="storage",
            operation="validate_data"
        )
        
        error_details = error_handler.log_error(critical_error)
        
        assert error_details.severity == MemoryErrorSeverity.CRITICAL
        assert error_handler.critical_error_count == 1
    
    def test_log_multiple_critical_errors_triggers_degradation(self, error_handler):
        """Test that multiple critical errors trigger degradation mode"""
        # Log multiple critical errors
        for i in range(error_handler.critical_error_threshold):
            critical_error = MemoryCorruptionError(f"Critical error {i}")
            error_handler.log_error(critical_error)
        
        assert error_handler.degradation_active is True
        assert error_handler.degradation_start_time is not None
    
    def test_error_log_size_limit(self, error_handler):
        """Test error log size limiting"""
        # Set small limit for testing
        error_handler.max_error_log_size = 3
        
        # Log more errors than the limit
        for i in range(5):
            error = MemoryStorageError(f"Error {i}")
            error_handler.log_error(error)
        
        assert len(error_handler.error_log) == 3
        # Should keep the most recent errors
        assert "Error 4" in error_handler.error_log[-1].message
    
    def test_activate_degradation_mode(self, error_handler):
        """Test activating degradation mode"""
        assert error_handler.degradation_active is False
        
        error_handler.activate_degradation_mode()
        
        assert error_handler.degradation_active is True
        assert error_handler.degradation_start_time is not None
        # Error counts should be reset
        assert all(count == 0 for count in error_handler.error_counts.values())
    
    def test_deactivate_degradation_mode(self, error_handler):
        """Test deactivating degradation mode"""
        error_handler.activate_degradation_mode()
        error_handler.critical_error_count = 3
        
        error_handler.deactivate_degradation_mode()
        
        assert error_handler.degradation_active is False
        assert error_handler.degradation_start_time is None
        assert error_handler.critical_error_count == 0
    
    def test_degradation_mode_auto_timeout(self, error_handler):
        """Test automatic degradation mode timeout"""
        # Activate degradation mode with past start time
        error_handler.degradation_active = True
        error_handler.degradation_start_time = datetime.now() - timedelta(minutes=35)
        error_handler.degradation_timeout_minutes = 30
        
        # Check if degradation is active (should auto-deactivate)
        is_active = error_handler.is_degradation_active()
        
        assert is_active is False
        assert error_handler.degradation_active is False
    
    def test_get_error_summary(self, error_handler, sample_error):
        """Test error summary generation"""
        # Log some errors
        error_handler.log_error(sample_error)
        error_handler.log_error(MemoryRetrievalError("Retrieval failed"))
        
        summary = error_handler.get_error_summary()
        
        assert isinstance(summary, dict)
        assert "total_errors" in summary
        assert "recent_errors" in summary
        assert "error_counts_by_category" in summary
        assert "critical_error_count" in summary
        assert "degradation_active" in summary
        assert summary["total_errors"] == 2
    
    def test_notification_callbacks_called(self, error_handler, sample_error):
        """Test that notification callbacks are called"""
        callback1 = Mock()
        callback2 = Mock()
        
        error_handler.register_notification_callback(callback1)
        error_handler.register_notification_callback(callback2)
        
        error_handler.log_error(sample_error)
        
        callback1.assert_called_once()
        callback2.assert_called_once()
        
        # Verify callback was called with MemoryErrorDetails
        call_args = callback1.call_args[0][0]
        assert isinstance(call_args, MemoryErrorDetails)
    
    def test_notification_callback_failure_handling(self, error_handler, sample_error):
        """Test handling of notification callback failures"""
        failing_callback = Mock(side_effect=Exception("Callback failed"))
        working_callback = Mock()
        
        error_handler.register_notification_callback(failing_callback)
        error_handler.register_notification_callback(working_callback)
        
        # Should not raise exception even if callback fails
        error_handler.log_error(sample_error)
        
        failing_callback.assert_called_once()
        working_callback.assert_called_once()
    
    def test_error_handler_logging_failure(self, error_handler):
        """Test error handler behavior when logging itself fails"""
        # Create an error with problematic attributes
        error = MemoryError("Test error")
        # Remove required attributes to cause logging failure
        delattr(error, 'category')
        
        # Should not raise exception, should return fallback error details
        error_details = error_handler.log_error(error)
        
        assert isinstance(error_details, MemoryErrorDetails)
        assert "Error handling system failure" in error_details.message

class TestMemoryErrorDecorator:
    """Test handle_memory_errors decorator"""
    
    @pytest.mark.asyncio
    async def test_decorator_success(self):
        """Test decorator with successful function execution"""
        @handle_memory_errors(
            component="test_component",
            operation="test_operation",
            fallback_result="fallback"
        )
        async def test_function():
            return "success"
        
        result = await test_function()
        assert result == "success"
    
    @pytest.mark.asyncio
    async def test_decorator_memory_error_suppressed(self):
        """Test decorator with memory error (suppressed)"""
        @handle_memory_errors(
            component="test_component",
            operation="test_operation",
            fallback_result="fallback",
            suppress_errors=True
        )
        async def test_function():
            raise MemoryStorageError("Storage failed")
        
        result = await test_function()
        assert result == "fallback"
    
    @pytest.mark.asyncio
    async def test_decorator_memory_error_not_suppressed(self):
        """Test decorator with memory error (not suppressed)"""
        @handle_memory_errors(
            component="test_component",
            operation="test_operation",
            fallback_result="fallback",
            suppress_errors=False
        )
        async def test_function():
            raise MemoryStorageError("Storage failed")
        
        with pytest.raises(MemoryStorageError):
            await test_function()
    
    @pytest.mark.asyncio
    async def test_decorator_timeout(self):
        """Test decorator with timeout"""
        @handle_memory_errors(
            component="test_component",
            operation="test_operation",
            fallback_result="timeout_fallback",
            timeout_seconds=0.1,
            suppress_errors=True
        )
        async def test_function():
            await asyncio.sleep(0.2)  # Longer than timeout
            return "success"
        
        result = await test_function()
        assert result == "timeout_fallback"
    
    @pytest.mark.asyncio
    async def test_decorator_retry_success(self):
        """Test decorator with retry on transient error"""
        call_count = 0
        
        @handle_memory_errors(
            component="test_component",
            operation="test_operation",
            fallback_result="fallback",
            retry_attempts=2,
            retry_delay=0.01,
            suppress_errors=True
        )
        async def test_function():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise MemoryConnectionError("Connection failed")
            return "success"
        
        result = await test_function()
        assert result == "success"
        assert call_count == 2
    
    @pytest.mark.asyncio
    async def test_decorator_retry_exhausted(self):
        """Test decorator when all retry attempts are exhausted"""
        @handle_memory_errors(
            component="test_component",
            operation="test_operation",
            fallback_result="fallback",
            retry_attempts=2,
            retry_delay=0.01,
            suppress_errors=True
        )
        async def test_function():
            raise MemoryConnectionError("Connection failed")
        
        result = await test_function()
        assert result == "fallback"
    
    @pytest.mark.asyncio
    async def test_decorator_no_retry_for_validation_error(self):
        """Test that validation errors are not retried"""
        call_count = 0
        
        @handle_memory_errors(
            component="test_component",
            operation="test_operation",
            fallback_result="fallback",
            retry_attempts=2,
            suppress_errors=True
        )
        async def test_function():
            nonlocal call_count
            call_count += 1
            raise MemoryValidationError("Invalid data")
        
        result = await test_function()
        assert result == "fallback"
        assert call_count == 1  # Should not retry validation errors
    
    def test_decorator_sync_function(self):
        """Test decorator with synchronous function"""
        @handle_memory_errors(
            component="test_component",
            operation="test_operation",
            fallback_result="fallback",
            suppress_errors=True
        )
        def test_function():
            raise MemoryStorageError("Storage failed")
        
        result = test_function()
        assert result == "fallback"
    
    def test_decorator_sync_function_success(self):
        """Test decorator with successful synchronous function"""
        @handle_memory_errors(
            component="test_component",
            operation="test_operation",
            fallback_result="fallback"
        )
        def test_function():
            return "success"
        
        result = test_function()
        assert result == "success"

class TestSafeMemoryOperations:
    """Test safe memory operation functions"""
    
    def test_safe_memory_operation_success(self):
        """Test safe memory operation with success"""
        def test_operation():
            return "success"
        
        result = safe_memory_operation(
            operation_func=test_operation,
            fallback_result="fallback"
        )
        
        assert result == "success"
    
    def test_safe_memory_operation_memory_error(self):
        """Test safe memory operation with memory error"""
        def test_operation():
            raise MemoryStorageError("Storage failed")
        
        result = safe_memory_operation(
            operation_func=test_operation,
            fallback_result="fallback"
        )
        
        assert result == "fallback"
    
    def test_safe_memory_operation_unexpected_error(self):
        """Test safe memory operation with unexpected error"""
        def test_operation():
            raise ValueError("Unexpected error")
        
        result = safe_memory_operation(
            operation_func=test_operation,
            fallback_result="fallback"
        )
        
        assert result == "fallback"
    
    @pytest.mark.asyncio
    async def test_safe_async_memory_operation_success(self):
        """Test safe async memory operation with success"""
        async def test_operation():
            return "success"
        
        result = await safe_async_memory_operation(
            operation_func=test_operation,
            fallback_result="fallback"
        )
        
        assert result == "success"
    
    @pytest.mark.asyncio
    async def test_safe_async_memory_operation_timeout(self):
        """Test safe async memory operation with timeout"""
        async def test_operation():
            await asyncio.sleep(0.2)
            return "success"
        
        result = await safe_async_memory_operation(
            operation_func=test_operation,
            fallback_result="timeout_fallback",
            timeout_seconds=0.1
        )
        
        assert result == "timeout_fallback"
    
    @pytest.mark.asyncio
    async def test_safe_async_memory_operation_memory_error(self):
        """Test safe async memory operation with memory error"""
        async def test_operation():
            raise MemoryRetrievalError("Retrieval failed")
        
        result = await safe_async_memory_operation(
            operation_func=test_operation,
            fallback_result="fallback"
        )
        
        assert result == "fallback"

class TestNotificationCallback:
    """Test notification callback functionality"""
    
    def test_create_memory_error_notification_callback(self):
        """Test creating notification callback"""
        callback = create_memory_error_notification_callback()
        
        assert callable(callback)
        
        # Test callback with high severity error
        error_details = MemoryErrorDetails(
            error_id="test_error",
            category=MemoryErrorCategory.STORAGE,
            severity=MemoryErrorSeverity.HIGH,
            message="High severity error",
            component="test",
            operation="test",
            timestamp=datetime.now()
        )
        
        # Should not raise exception
        callback(error_details)
    
    def test_notification_callback_with_low_severity(self):
        """Test notification callback with low severity error"""
        callback = create_memory_error_notification_callback()
        
        error_details = MemoryErrorDetails(
            error_id="test_error",
            category=MemoryErrorCategory.STORAGE,
            severity=MemoryErrorSeverity.LOW,
            message="Low severity error",
            component="test",
            operation="test",
            timestamp=datetime.now()
        )
        
        # Should not raise exception
        callback(error_details)

class TestGlobalErrorHandler:
    """Test global error handler instance"""
    
    def test_global_error_handler_exists(self):
        """Test that global error handler instance exists"""
        assert memory_error_handler is not None
        assert isinstance(memory_error_handler, MemoryErrorHandler)
    
    def test_global_error_handler_has_default_callback(self):
        """Test that global error handler has default notification callback"""
        # Should have at least one callback registered by default
        assert len(memory_error_handler.notification_callbacks) >= 1

if __name__ == "__main__":
    pytest.main([__file__])