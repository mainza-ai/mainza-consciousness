"""
Enhanced Error Handling System
Context7 MCP Standards Implementation

This module provides comprehensive error handling, recovery, and resilience patterns:
- Custom exception hierarchy
- Error classification and routing
- Automatic recovery strategies
- Error analytics and learning
- Graceful degradation patterns
"""

import asyncio
import logging
import traceback
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Type, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import json
import uuid
from contextlib import contextmanager, asynccontextmanager
import functools
import inspect

logger = logging.getLogger(__name__)

class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    """Error categories for classification"""
    SYSTEM = "system"
    DATABASE = "database"
    NETWORK = "network"
    AUTHENTICATION = "authentication"
    VALIDATION = "validation"
    BUSINESS_LOGIC = "business_logic"
    EXTERNAL_SERVICE = "external_service"
    RESOURCE = "resource"
    CONSCIOUSNESS = "consciousness"

class RecoveryStrategy(Enum):
    """Recovery strategy types"""
    RETRY = "retry"
    FALLBACK = "fallback"
    CIRCUIT_BREAKER = "circuit_breaker"
    GRACEFUL_DEGRADATION = "graceful_degradation"
    MANUAL_INTERVENTION = "manual_intervention"
    IGNORE = "ignore"

@dataclass
class ErrorContext:
    """Comprehensive error context information"""
    error_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
    category: ErrorCategory = ErrorCategory.SYSTEM
    component: str = ""
    function_name: str = ""
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    stack_trace: str = ""
    system_state: Dict[str, Any] = field(default_factory=dict)
    recovery_attempts: int = 0
    recovery_strategy: Optional[RecoveryStrategy] = None
    resolved: bool = False
    resolution_time: Optional[datetime] = None

class MainzaException(Exception):
    """Base exception class for Mainza system"""
    
    def __init__(
        self, 
        message: str, 
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        category: ErrorCategory = ErrorCategory.SYSTEM,
        context: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None
    ):
        super().__init__(message)
        self.message = message
        self.severity = severity
        self.category = category
        self.context = context or {}
        self.cause = cause
        self.error_id = str(uuid.uuid4())
        self.timestamp = datetime.now()

class DatabaseException(MainzaException):
    """Database-related exceptions"""
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.DATABASE, **kwargs)

class NetworkException(MainzaException):
    """Network-related exceptions"""
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.NETWORK, **kwargs)

class AuthenticationException(MainzaException):
    """Authentication-related exceptions"""
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.AUTHENTICATION, severity=ErrorSeverity.HIGH, **kwargs)

class ValidationException(MainzaException):
    """Validation-related exceptions"""
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.VALIDATION, severity=ErrorSeverity.LOW, **kwargs)

class BusinessLogicException(MainzaException):
    """Business logic exceptions"""
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.BUSINESS_LOGIC, **kwargs)

class ExternalServiceException(MainzaException):
    """External service exceptions"""
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.EXTERNAL_SERVICE, **kwargs)

class ResourceException(MainzaException):
    """Resource-related exceptions"""
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.RESOURCE, severity=ErrorSeverity.HIGH, **kwargs)

class ConsciousnessException(MainzaException):
    """Consciousness system exceptions"""
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.CONSCIOUSNESS, **kwargs)

class ErrorHandler:
    """Comprehensive error handling and recovery system"""
    
    def __init__(self):
        self.error_history: List[ErrorContext] = []
        self.recovery_strategies: Dict[ErrorCategory, List[RecoveryStrategy]] = {
            ErrorCategory.DATABASE: [RecoveryStrategy.RETRY, RecoveryStrategy.CIRCUIT_BREAKER],
            ErrorCategory.NETWORK: [RecoveryStrategy.RETRY, RecoveryStrategy.FALLBACK],
            ErrorCategory.EXTERNAL_SERVICE: [RecoveryStrategy.RETRY, RecoveryStrategy.GRACEFUL_DEGRADATION],
            ErrorCategory.RESOURCE: [RecoveryStrategy.GRACEFUL_DEGRADATION, RecoveryStrategy.MANUAL_INTERVENTION],
            ErrorCategory.CONSCIOUSNESS: [RecoveryStrategy.FALLBACK, RecoveryStrategy.GRACEFUL_DEGRADATION],
            ErrorCategory.AUTHENTICATION: [RecoveryStrategy.MANUAL_INTERVENTION],
            ErrorCategory.VALIDATION: [RecoveryStrategy.IGNORE],
            ErrorCategory.BUSINESS_LOGIC: [RecoveryStrategy.FALLBACK, RecoveryStrategy.MANUAL_INTERVENTION]
        }
        self.fallback_handlers: Dict[str, Callable] = {}
        self.error_listeners: List[Callable] = []
        self.max_history_size = 1000
    
    def register_fallback_handler(self, component: str, handler: Callable):
        """Register fallback handler for a component"""
        self.fallback_handlers[component] = handler
        logger.info(f"Registered fallback handler for {component}")
    
    def register_error_listener(self, listener: Callable):
        """Register error event listener"""
        self.error_listeners.append(listener)
        logger.info("Registered error listener")
    
    async def handle_error(
        self, 
        error: Exception, 
        context: Optional[Dict[str, Any]] = None,
        component: str = "",
        user_id: Optional[str] = None
    ) -> ErrorContext:
        """Handle error with comprehensive processing"""
        
        # Create error context
        error_context = self._create_error_context(error, context, component, user_id)
        
        # Log error
        await self._log_error(error_context)
        
        # Store error history
        self._store_error_history(error_context)
        
        # Notify listeners
        await self._notify_error_listeners(error_context)
        
        # Attempt recovery
        await self._attempt_recovery(error_context)
        
        # Update consciousness system about error
        await self._update_consciousness_about_error(error_context)
        
        return error_context
    
    def _create_error_context(
        self, 
        error: Exception, 
        context: Optional[Dict[str, Any]], 
        component: str,
        user_id: Optional[str]
    ) -> ErrorContext:
        """Create comprehensive error context"""
        
        # Determine error properties
        if isinstance(error, MainzaException):
            severity = error.severity
            category = error.category
        else:
            severity = self._classify_error_severity(error)
            category = self._classify_error_category(error)
        
        # Get function name from stack trace
        frame = inspect.currentframe()
        function_name = ""
        try:
            # Go up the stack to find the actual error location
            for _ in range(5):  # Look up to 5 frames up
                frame = frame.f_back
                if frame and frame.f_code.co_name not in ['handle_error', '_create_error_context']:
                    function_name = frame.f_code.co_name
                    break
        except:
            pass
        finally:
            del frame
        
        return ErrorContext(
            severity=severity,
            category=category,
            component=component,
            function_name=function_name,
            user_id=user_id,
            stack_trace=traceback.format_exc(),
            system_state=context or {}
        )
    
    def _classify_error_severity(self, error: Exception) -> ErrorSeverity:
        """Classify error severity based on type and message"""
        error_type = type(error).__name__
        error_message = str(error).lower()
        
        # Critical errors
        if any(keyword in error_message for keyword in ['critical', 'fatal', 'system failure']):
            return ErrorSeverity.CRITICAL
        
        # High severity errors
        if any(keyword in error_message for keyword in ['connection', 'timeout', 'authentication', 'permission']):
            return ErrorSeverity.HIGH
        
        # Low severity errors
        if any(keyword in error_message for keyword in ['validation', 'not found', 'invalid input']):
            return ErrorSeverity.LOW
        
        return ErrorSeverity.MEDIUM
    
    def _classify_error_category(self, error: Exception) -> ErrorCategory:
        """Classify error category based on type and context"""
        error_type = type(error).__name__.lower()
        error_message = str(error).lower()
        
        # Database errors
        if any(keyword in error_type for keyword in ['database', 'neo4j', 'connection', 'transaction']):
            return ErrorCategory.DATABASE
        
        # Network errors
        if any(keyword in error_type for keyword in ['network', 'http', 'connection', 'timeout']):
            return ErrorCategory.NETWORK
        
        # Authentication errors
        if any(keyword in error_message for keyword in ['authentication', 'authorization', 'permission', 'access denied']):
            return ErrorCategory.AUTHENTICATION
        
        # Validation errors
        if any(keyword in error_type for keyword in ['validation', 'value', 'type']):
            return ErrorCategory.VALIDATION
        
        return ErrorCategory.SYSTEM
    
    async def _log_error(self, error_context: ErrorContext):
        """Log error with appropriate level"""
        # Extract error message from stack trace (avoiding backslash in f-string)
        newline_char = '\n'
        error_message = (
            error_context.stack_trace.split('Exception: ')[-1].split(newline_char)[0] 
            if 'Exception: ' in error_context.stack_trace 
            else 'Unknown error'
        )
        
        log_message = (
            f"[{error_context.error_id}] {error_context.category.value.upper()} ERROR "
            f"in {error_context.component}.{error_context.function_name}: "
            f"{error_message}"
        )
        
        if error_context.severity == ErrorSeverity.CRITICAL:
            logger.critical(log_message)
        elif error_context.severity == ErrorSeverity.HIGH:
            logger.error(log_message)
        elif error_context.severity == ErrorSeverity.MEDIUM:
            logger.warning(log_message)
        else:
            logger.info(log_message)
    
    def _store_error_history(self, error_context: ErrorContext):
        """Store error in history for analysis"""
        self.error_history.append(error_context)
        
        # Maintain history size limit
        if len(self.error_history) > self.max_history_size:
            self.error_history = self.error_history[-self.max_history_size//2:]
    
    async def _notify_error_listeners(self, error_context: ErrorContext):
        """Notify registered error listeners"""
        for listener in self.error_listeners:
            try:
                if asyncio.iscoroutinefunction(listener):
                    await listener(error_context)
                else:
                    listener(error_context)
            except Exception as e:
                logger.error(f"Error listener failed: {e}")
    
    async def _attempt_recovery(self, error_context: ErrorContext):
        """Attempt error recovery based on category and strategy"""
        strategies = self.recovery_strategies.get(error_context.category, [])
        
        for strategy in strategies:
            try:
                success = await self._execute_recovery_strategy(strategy, error_context)
                if success:
                    error_context.resolved = True
                    error_context.resolution_time = datetime.now()
                    error_context.recovery_strategy = strategy
                    logger.info(f"Error {error_context.error_id} recovered using {strategy.value}")
                    break
            except Exception as e:
                logger.error(f"Recovery strategy {strategy.value} failed: {e}")
                error_context.recovery_attempts += 1
    
    async def _execute_recovery_strategy(
        self, 
        strategy: RecoveryStrategy, 
        error_context: ErrorContext
    ) -> bool:
        """Execute specific recovery strategy"""
        
        if strategy == RecoveryStrategy.FALLBACK:
            return await self._execute_fallback(error_context)
        elif strategy == RecoveryStrategy.GRACEFUL_DEGRADATION:
            return await self._execute_graceful_degradation(error_context)
        elif strategy == RecoveryStrategy.RETRY:
            return await self._execute_retry(error_context)
        elif strategy == RecoveryStrategy.CIRCUIT_BREAKER:
            return await self._execute_circuit_breaker(error_context)
        elif strategy == RecoveryStrategy.IGNORE:
            return True  # Always "succeeds" by ignoring
        
        return False
    
    async def _execute_fallback(self, error_context: ErrorContext) -> bool:
        """Execute fallback handler"""
        fallback_handler = self.fallback_handlers.get(error_context.component)
        if fallback_handler:
            try:
                if asyncio.iscoroutinefunction(fallback_handler):
                    await fallback_handler(error_context)
                else:
                    fallback_handler(error_context)
                return True
            except Exception as e:
                logger.error(f"Fallback handler failed: {e}")
        return False
    
    async def _execute_graceful_degradation(self, error_context: ErrorContext) -> bool:
        """Execute graceful degradation"""
        # Implement graceful degradation logic
        logger.info(f"Graceful degradation activated for {error_context.component}")
        return True
    
    async def _execute_retry(self, error_context: ErrorContext) -> bool:
        """Execute retry logic"""
        # Simple retry implementation - can be enhanced
        if error_context.recovery_attempts < 3:
            await asyncio.sleep(2 ** error_context.recovery_attempts)  # Exponential backoff
            return False  # Indicate retry needed
        return False
    
    async def _execute_circuit_breaker(self, error_context: ErrorContext) -> bool:
        """Execute circuit breaker logic"""
        # Circuit breaker implementation would go here
        logger.info(f"Circuit breaker activated for {error_context.component}")
        return True
    
    async def _update_consciousness_about_error(self, error_context: ErrorContext):
        """Update consciousness system about error for learning"""
        try:
            from backend.utils.consciousness_orchestrator import consciousness_orchestrator
            
            await consciousness_orchestrator.process_agent_failure(
                agent_name=error_context.component,
                error=str(error_context.stack_trace.split('Exception: ')[-1].split('\\n')[0] if 'Exception: ' in error_context.stack_trace else 'Unknown error'),
                query=error_context.system_state.get('query', 'Unknown query')
            )
        except Exception as e:
            logger.error(f"Failed to update consciousness about error: {e}")
    
    def get_error_analytics(self) -> Dict[str, Any]:
        """Get error analytics and patterns"""
        if not self.error_history:
            return {"message": "No error history available"}
        
        # Calculate error statistics
        total_errors = len(self.error_history)
        resolved_errors = len([e for e in self.error_history if e.resolved])
        
        # Error by category
        category_counts = {}
        for error in self.error_history:
            category = error.category.value
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Error by severity
        severity_counts = {}
        for error in self.error_history:
            severity = error.severity.value
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Recent error trend (last 24 hours)
        recent_cutoff = datetime.now() - timedelta(hours=24)
        recent_errors = [e for e in self.error_history if e.timestamp > recent_cutoff]
        
        return {
            "total_errors": total_errors,
            "resolved_errors": resolved_errors,
            "resolution_rate": resolved_errors / total_errors if total_errors > 0 else 0,
            "errors_by_category": category_counts,
            "errors_by_severity": severity_counts,
            "recent_errors_24h": len(recent_errors),
            "most_common_category": max(category_counts.items(), key=lambda x: x[1])[0] if category_counts else None,
            "most_common_severity": max(severity_counts.items(), key=lambda x: x[1])[0] if severity_counts else None
        }

# Global error handler instance
error_handler = ErrorHandler()

def handle_errors(
    component: str = "",
    fallback_result: Any = None,
    suppress_errors: bool = False
):
    """Decorator for automatic error handling"""
    def decorator(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                error_context = await error_handler.handle_error(
                    error=e,
                    context={"args": str(args), "kwargs": str(kwargs)},
                    component=component or func.__name__
                )
                
                if suppress_errors:
                    return fallback_result
                else:
                    raise
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # For sync functions, we need to handle errors synchronously
                logger.error(f"Error in {component or func.__name__}: {e}")
                if suppress_errors:
                    return fallback_result
                else:
                    raise
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

@contextmanager
def error_context(component: str, user_id: Optional[str] = None):
    """Context manager for error handling"""
    try:
        yield
    except Exception as e:
        # Handle error synchronously in context manager
        logger.error(f"Error in {component}: {e}")
        raise

@asynccontextmanager
async def async_error_context(component: str, user_id: Optional[str] = None):
    """Async context manager for error handling"""
    try:
        yield
    except Exception as e:
        await error_handler.handle_error(
            error=e,
            component=component,
            user_id=user_id
        )
        raise

# Export key components
__all__ = [
    'ErrorSeverity', 'ErrorCategory', 'RecoveryStrategy', 'ErrorContext',
    'MainzaException', 'DatabaseException', 'NetworkException', 'AuthenticationException',
    'ValidationException', 'BusinessLogicException', 'ExternalServiceException',
    'ResourceException', 'ConsciousnessException',
    'ErrorHandler', 'error_handler',
    'handle_errors', 'error_context', 'async_error_context'
]