"""
Comprehensive Memory Error Handling for Mainza AI
Provides memory-specific exception classes, error handling wrappers, and graceful degradation mechanisms.
"""
import logging
import asyncio
import functools
import traceback
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable, Union, TypeVar, Generic
from dataclasses import dataclass, field
from enum import Enum
import json

logger = logging.getLogger(__name__)

# Type variable for generic error handling
T = TypeVar('T')

class MemoryErrorSeverity(Enum):
    """Severity levels for memory errors"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class MemoryErrorCategory(Enum):
    """Categories of memory errors"""
    STORAGE = "storage"
    RETRIEVAL = "retrieval"
    CONTEXT = "context"
    EMBEDDING = "embedding"
    NEO4J_CONNECTION = "neo4j_connection"
    VALIDATION = "validation"
    CORRUPTION = "corruption"
    TIMEOUT = "timeout"
    RESOURCE = "resource"

@dataclass
class MemoryErrorDetails:
    """Detailed information about a memory error"""
    error_id: str
    category: MemoryErrorCategory
    severity: MemoryErrorSeverity
    message: str
    component: str
    operation: str
    timestamp: datetime
    user_id: Optional[str] = None
    memory_id: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    stack_trace: Optional[str] = None
    recovery_attempted: bool = False
    recovery_successful: bool = False

class MemoryError(Exception):
    """Base exception for all memory operations"""
    
    def __init__(
        self, 
        message: str, 
        category: MemoryErrorCategory = MemoryErrorCategory.STORAGE,
        severity: MemoryErrorSeverity = MemoryErrorSeverity.MEDIUM,
        component: str = "unknown",
        operation: str = "unknown",
        context: Optional[Dict[str, Any]] = None,
        original_error: Optional[Exception] = None
    ):
        super().__init__(message)
        self.category = category
        self.severity = severity
        self.component = component
        self.operation = operation
        self.context = context or {}
        self.original_error = original_error
        self.timestamp = datetime.now()
        
        # Generate unique error ID
        import uuid
        self.error_id = str(uuid.uuid4())[:8]

class MemoryStorageError(MemoryError):
    """Raised when memory storage operations fail"""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message, 
            category=MemoryErrorCategory.STORAGE,
            **kwargs
        )

class MemoryRetrievalError(MemoryError):
    """Raised when memory retrieval operations fail"""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message, 
            category=MemoryErrorCategory.RETRIEVAL,
            **kwargs
        )

class MemoryContextError(MemoryError):
    """Raised when memory context building fails"""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message, 
            category=MemoryErrorCategory.CONTEXT,
            **kwargs
        )

class MemoryEmbeddingError(MemoryError):
    """Raised when embedding generation or processing fails"""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message, 
            category=MemoryErrorCategory.EMBEDDING,
            **kwargs
        )

class MemoryConnectionError(MemoryError):
    """Raised when Neo4j connection issues occur"""
    
    def __init__(self, message: str, **kwargs):
        # Remove severity from kwargs if it exists to avoid duplicate
        kwargs.pop('severity', None)
        super().__init__(
            message, 
            category=MemoryErrorCategory.NEO4J_CONNECTION,
            severity=MemoryErrorSeverity.HIGH,
            **kwargs
        )

class MemoryValidationError(MemoryError):
    """Raised when memory data validation fails"""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message, 
            category=MemoryErrorCategory.VALIDATION,
            **kwargs
        )

class MemoryCorruptionError(MemoryError):
    """Raised when memory data corruption is detected"""
    
    def __init__(self, message: str, **kwargs):
        # Remove severity from kwargs if it exists to avoid duplicate
        kwargs.pop('severity', None)
        super().__init__(
            message, 
            category=MemoryErrorCategory.CORRUPTION,
            severity=MemoryErrorSeverity.CRITICAL,
            **kwargs
        )

class MemoryTimeoutError(MemoryError):
    """Raised when memory operations timeout"""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message, 
            category=MemoryErrorCategory.TIMEOUT,
            **kwargs
        )

class MemoryResourceError(MemoryError):
    """Raised when memory system resource limits are exceeded"""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message, 
            category=MemoryErrorCategory.RESOURCE,
            severity=MemoryErrorSeverity.HIGH,
            **kwargs
        )

class MemoryErrorHandler:
    """
    Comprehensive error handler for memory operations with logging, 
    notification, and graceful degradation capabilities
    """
    
    def __init__(self):
        self.error_log: List[MemoryErrorDetails] = []
        self.max_error_log_size = 1000
        self.notification_callbacks: List[Callable] = []
        self.critical_error_threshold = 5  # Number of critical errors before system alert
        self.critical_error_count = 0
        
        # Graceful degradation settings
        self.degradation_active = False
        self.degradation_start_time: Optional[datetime] = None
        self.degradation_timeout_minutes = 30
        
        # Error rate tracking
        self.error_counts: Dict[MemoryErrorCategory, int] = {
            category: 0 for category in MemoryErrorCategory
        }
        self.error_rate_window_minutes = 10
        self.max_error_rate = 10  # Max errors per category per window
    
    def register_notification_callback(self, callback: Callable[[MemoryErrorDetails], None]):
        """Register a callback for error notifications"""
        self.notification_callbacks.append(callback)
    
    def log_error(
        self,
        error: MemoryError,
        user_id: Optional[str] = None,
        memory_id: Optional[str] = None,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> MemoryErrorDetails:
        """
        Log a memory error with full details and context
        
        Args:
            error: The MemoryError instance
            user_id: Optional user ID associated with the error
            memory_id: Optional memory ID associated with the error
            additional_context: Additional context information
            
        Returns:
            MemoryErrorDetails object with full error information
        """
        try:
            # Create error details
            error_details = MemoryErrorDetails(
                error_id=getattr(error, 'error_id', 'unknown'),
                category=getattr(error, 'category', MemoryErrorCategory.STORAGE),
                severity=getattr(error, 'severity', MemoryErrorSeverity.MEDIUM),
                message=str(error),
                component=getattr(error, 'component', 'unknown'),
                operation=getattr(error, 'operation', 'unknown'),
                timestamp=getattr(error, 'timestamp', datetime.now()),
                user_id=user_id,
                memory_id=memory_id,
                context={**getattr(error, 'context', {}), **(additional_context or {})},
                stack_trace=traceback.format_exc() if getattr(error, 'original_error', None) else None
            )
            
            # Add to error log
            self.error_log.append(error_details)
            
            # Maintain log size
            if len(self.error_log) > self.max_error_log_size:
                self.error_log = self.error_log[-self.max_error_log_size:]
            
            # Update error counts
            self.error_counts[error.category] += 1
            
            # Log based on severity
            if error.severity == MemoryErrorSeverity.CRITICAL:
                logger.critical(f"🚨 CRITICAL Memory Error [{error.error_id}]: {str(error)}")
                self.critical_error_count += 1
                self._handle_critical_error(error_details)
            elif error.severity == MemoryErrorSeverity.HIGH:
                logger.error(f"❌ HIGH Memory Error [{error.error_id}]: {str(error)}")
            elif error.severity == MemoryErrorSeverity.MEDIUM:
                logger.warning(f"⚠️ MEDIUM Memory Error [{error.error_id}]: {str(error)}")
            else:
                logger.info(f"ℹ️ LOW Memory Error [{error.error_id}]: {str(error)}")
            
            # Log additional context
            if error_details.context:
                logger.debug(f"Error context [{error.error_id}]: {json.dumps(error_details.context, default=str)}")
            
            # Send notifications
            self._send_notifications(error_details)
            
            # Check if degradation should be activated
            self._check_degradation_trigger()
            
            return error_details
            
        except Exception as e:
            # Fallback logging if error handling itself fails
            logger.error(f"Failed to log memory error: {e}")
            # Try to get basic info from the original error
            try:
                error_id = getattr(error, 'error_id', 'unknown')
                category = getattr(error, 'category', MemoryErrorCategory.STORAGE)
                severity = getattr(error, 'severity', MemoryErrorSeverity.CRITICAL)
                component = getattr(error, 'component', 'error_handler')
                operation = getattr(error, 'operation', 'log_error')
            except:
                error_id = "unknown"
                category = MemoryErrorCategory.STORAGE
                severity = MemoryErrorSeverity.CRITICAL
                component = "error_handler"
                operation = "log_error"
            
            return MemoryErrorDetails(
                error_id=error_id,
                category=category,
                severity=severity,
                message=f"Error handling system failure: {e}",
                component=component,
                operation=operation,
                timestamp=datetime.now()
            )
    
    def _handle_critical_error(self, error_details: MemoryErrorDetails):
        """Handle critical errors with special procedures"""
        try:
            # Activate degradation mode if too many critical errors
            if self.critical_error_count >= self.critical_error_threshold:
                self.activate_degradation_mode()
            
            # Log critical error details
            logger.critical(f"Critical memory error details: {error_details}")
            
            # Additional critical error handling could include:
            # - Sending alerts to administrators
            # - Triggering system health checks
            # - Initiating automatic recovery procedures
            
        except Exception as e:
            logger.error(f"Failed to handle critical error: {e}")
    
    def _send_notifications(self, error_details: MemoryErrorDetails):
        """Send error notifications to registered callbacks"""
        for callback in self.notification_callbacks:
            try:
                callback(error_details)
            except Exception as e:
                logger.warning(f"Notification callback failed: {e}")
    
    def _check_degradation_trigger(self):
        """Check if error rates warrant activating degradation mode"""
        try:
            # Check error rates for each category
            for category, count in self.error_counts.items():
                if count >= self.max_error_rate:
                    logger.warning(f"High error rate detected for {category.value}: {count} errors")
                    if not self.degradation_active:
                        self.activate_degradation_mode()
                    break
                    
        except Exception as e:
            logger.error(f"Failed to check degradation trigger: {e}")
    
    def activate_degradation_mode(self):
        """Activate graceful degradation mode"""
        if not self.degradation_active:
            self.degradation_active = True
            self.degradation_start_time = datetime.now()
            logger.warning("🔄 Memory system degradation mode ACTIVATED")
            
            # Reset error counts when entering degradation
            self.error_counts = {category: 0 for category in MemoryErrorCategory}
    
    def deactivate_degradation_mode(self):
        """Deactivate graceful degradation mode"""
        if self.degradation_active:
            self.degradation_active = False
            self.degradation_start_time = None
            self.critical_error_count = 0
            logger.info("✅ Memory system degradation mode DEACTIVATED")
    
    def is_degradation_active(self) -> bool:
        """Check if degradation mode is currently active"""
        # Auto-deactivate after timeout
        if (self.degradation_active and 
            self.degradation_start_time and 
            (datetime.now() - self.degradation_start_time).total_seconds() > 
            self.degradation_timeout_minutes * 60):
            self.deactivate_degradation_mode()
        
        return self.degradation_active
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of recent errors"""
        try:
            recent_errors = [
                error for error in self.error_log 
                if (datetime.now() - error.timestamp).total_seconds() < 3600  # Last hour
            ]
            
            return {
                "total_errors": len(self.error_log),
                "recent_errors": len(recent_errors),
                "error_counts_by_category": dict(self.error_counts),
                "critical_error_count": self.critical_error_count,
                "degradation_active": self.degradation_active,
                "degradation_start_time": self.degradation_start_time.isoformat() if self.degradation_start_time else None
            }
            
        except Exception as e:
            logger.error(f"Failed to generate error summary: {e}")
            return {"error": "Failed to generate summary"}

# Global error handler instance
memory_error_handler = MemoryErrorHandler()

def handle_memory_errors(
    component: str,
    operation: str,
    fallback_result: Any = None,
    suppress_errors: bool = True,
    timeout_seconds: Optional[float] = None,
    retry_attempts: int = 0,
    retry_delay: float = 1.0
):
    """
    Decorator for comprehensive memory error handling with graceful degradation
    
    Args:
        component: Name of the component (e.g., "memory_storage", "memory_retrieval")
        operation: Name of the operation (e.g., "store_memory", "search_memories")
        fallback_result: Result to return if operation fails
        suppress_errors: Whether to suppress exceptions (return fallback instead)
        timeout_seconds: Optional timeout for the operation
        retry_attempts: Number of retry attempts for transient errors
        retry_delay: Delay between retry attempts in seconds
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> T:
            last_error = None
            
            for attempt in range(retry_attempts + 1):
                try:
                    # Apply timeout if specified
                    if timeout_seconds:
                        result = await asyncio.wait_for(
                            func(*args, **kwargs), 
                            timeout=timeout_seconds
                        )
                    else:
                        result = await func(*args, **kwargs)
                    
                    # If we had previous failures but this succeeded, log recovery
                    if attempt > 0:
                        logger.info(f"✅ Operation recovered after {attempt} attempts: {component}.{operation}")
                    
                    return result
                    
                except asyncio.TimeoutError as e:
                    error = MemoryTimeoutError(
                        f"Operation timed out after {timeout_seconds}s",
                        component=component,
                        operation=operation,
                        original_error=e
                    )
                    last_error = error
                    
                except MemoryConnectionError as e:
                    # Connection errors are often transient, retry them
                    last_error = e
                    if attempt < retry_attempts:
                        logger.warning(f"🔄 Retrying {component}.{operation} after connection error (attempt {attempt + 1}/{retry_attempts + 1})")
                        await asyncio.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                        continue
                    
                except MemoryError as e:
                    # Log the memory error
                    error_details = memory_error_handler.log_error(
                        e,
                        additional_context={
                            "function": func.__name__,
                            "args_count": len(args),
                            "kwargs_keys": list(kwargs.keys()),
                            "attempt": attempt + 1
                        }
                    )
                    last_error = e
                    
                    # For certain error types, don't retry
                    if e.category in [MemoryErrorCategory.VALIDATION, MemoryErrorCategory.CORRUPTION]:
                        break
                    
                    # Retry for other error types
                    if attempt < retry_attempts:
                        logger.warning(f"🔄 Retrying {component}.{operation} after error (attempt {attempt + 1}/{retry_attempts + 1}): {e}")
                        await asyncio.sleep(retry_delay * (2 ** attempt))
                        continue
                    
                except Exception as e:
                    # Wrap unexpected errors in MemoryError
                    memory_error = MemoryError(
                        f"Unexpected error in {operation}: {str(e)}",
                        component=component,
                        operation=operation,
                        severity=MemoryErrorSeverity.HIGH,
                        original_error=e
                    )
                    
                    memory_error_handler.log_error(memory_error)
                    last_error = memory_error
                    
                    # Don't retry unexpected errors
                    break
            
            # All attempts failed
            if suppress_errors:
                logger.warning(f"🔄 Returning fallback result for {component}.{operation} after {retry_attempts + 1} attempts")
                return fallback_result
            else:
                raise last_error or MemoryError(f"Operation failed: {component}.{operation}")
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> T:
            try:
                result = func(*args, **kwargs)
                return result
                
            except MemoryError as e:
                error_details = memory_error_handler.log_error(
                    e,
                    additional_context={
                        "function": func.__name__,
                        "args_count": len(args),
                        "kwargs_keys": list(kwargs.keys())
                    }
                )
                
                if suppress_errors:
                    return fallback_result
                else:
                    raise
                    
            except Exception as e:
                memory_error = MemoryError(
                    f"Unexpected error in {operation}: {str(e)}",
                    component=component,
                    operation=operation,
                    severity=MemoryErrorSeverity.HIGH,
                    original_error=e
                )
                
                memory_error_handler.log_error(memory_error)
                
                if suppress_errors:
                    return fallback_result
                else:
                    raise memory_error
        
        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator

def safe_memory_operation(
    operation_func: Callable[..., T],
    fallback_result: T = None,
    component: str = "memory",
    operation_name: str = "operation",
    log_errors: bool = True,
    **kwargs
) -> T:
    """
    Execute a memory operation safely with error handling
    
    Args:
        operation_func: Function to execute
        fallback_result: Result to return on failure
        component: Component name for logging
        operation_name: Operation name for logging
        log_errors: Whether to log errors
        **kwargs: Additional arguments for the operation
        
    Returns:
        Operation result or fallback result on failure
    """
    try:
        return operation_func(**kwargs)
        
    except MemoryError as e:
        if log_errors:
            memory_error_handler.log_error(
                e,
                additional_context={
                    "operation_name": operation_name,
                    "component": component
                }
            )
        return fallback_result
        
    except Exception as e:
        if log_errors:
            memory_error = MemoryError(
                f"Unexpected error in {operation_name}: {str(e)}",
                component=component,
                operation=operation_name,
                original_error=e
            )
            memory_error_handler.log_error(memory_error)
        
        return fallback_result

async def safe_async_memory_operation(
    operation_func: Callable[..., T],
    fallback_result: T = None,
    component: str = "memory",
    operation_name: str = "operation",
    log_errors: bool = True,
    timeout_seconds: Optional[float] = None,
    **kwargs
) -> T:
    """
    Execute an async memory operation safely with error handling
    
    Args:
        operation_func: Async function to execute
        fallback_result: Result to return on failure
        component: Component name for logging
        operation_name: Operation name for logging
        log_errors: Whether to log errors
        timeout_seconds: Optional timeout for the operation
        **kwargs: Additional arguments for the operation
        
    Returns:
        Operation result or fallback result on failure
    """
    try:
        if timeout_seconds:
            return await asyncio.wait_for(operation_func(**kwargs), timeout=timeout_seconds)
        else:
            return await operation_func(**kwargs)
            
    except asyncio.TimeoutError as e:
        if log_errors:
            timeout_error = MemoryTimeoutError(
                f"Operation {operation_name} timed out after {timeout_seconds}s",
                component=component,
                operation=operation_name,
                original_error=e
            )
            memory_error_handler.log_error(timeout_error)
        return fallback_result
        
    except MemoryError as e:
        if log_errors:
            memory_error_handler.log_error(
                e,
                additional_context={
                    "operation_name": operation_name,
                    "component": component
                }
            )
        return fallback_result
        
    except Exception as e:
        if log_errors:
            memory_error = MemoryError(
                f"Unexpected error in {operation_name}: {str(e)}",
                component=component,
                operation=operation_name,
                original_error=e
            )
            memory_error_handler.log_error(memory_error)
        
        return fallback_result

def create_memory_error_notification_callback():
    """Create a callback for memory error notifications (can be customized)"""
    def notification_callback(error_details: MemoryErrorDetails):
        """Default notification callback for memory errors"""
        if error_details.severity in [MemoryErrorSeverity.HIGH, MemoryErrorSeverity.CRITICAL]:
            # In production, this could send alerts via email, Slack, etc.
            logger.warning(f"📧 Memory error notification: {error_details.message}")
    
    return notification_callback

# Register default notification callback
memory_error_handler.register_notification_callback(create_memory_error_notification_callback())