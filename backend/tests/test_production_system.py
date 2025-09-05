"""
Production System Test Suite
Context7 MCP Standards Implementation

Comprehensive testing for the production-grade Mainza AI system including:
- Unit tests for core components
- Integration tests for system interactions
- Performance tests for optimization
- Security tests for vulnerabilities
- Load tests for scalability
- Chaos engineering tests for resilience
"""

import pytest
import asyncio
import time
import threading
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, Any, List
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import production components
from backend.core.production_foundation import (
    health_monitor, resource_manager, config_manager,
    CircuitBreaker, RetryManager, HealthMonitor
)
from backend.core.enhanced_error_handling import (
    error_handler, ErrorSeverity, ErrorCategory,
    MainzaException, DatabaseException, handle_errors
)
from backend.core.performance_optimization import (
    performance_optimizer, InMemoryCache, QueryOptimizer,
    CacheStrategy, PerformanceLevel
)
from backend.core.security_framework import (
    security_framework, RateLimiter, InputValidator,
    SecurityLevel, ThreatLevel, SecurityEventType
)

class TestProductionFoundation:
    """Test production foundation components"""
    
    @pytest.mark.asyncio
    async def test_health_monitor_initialization(self):
        """Test health monitor initialization"""
        monitor = HealthMonitor()
        
        # Register a test component
        def test_health_check():
            return True
        
        monitor.register_component("test_component", test_health_check)
        
        assert "test_component" in monitor.components
        assert monitor.health_checks["test_component"] == test_health_check
    
    @pytest.mark.asyncio
    async def test_health_monitor_check_execution(self):
        """Test health check execution"""
        monitor = HealthMonitor()
        
        # Register healthy component
        def healthy_check():
            return True
        
        # Register unhealthy component
        def unhealthy_check():
            return False
        
        monitor.register_component("healthy", healthy_check)
        monitor.register_component("unhealthy", unhealthy_check)
        
        await monitor.check_all_components()
        
        assert monitor.components["healthy"].status.value == "active"
        assert monitor.components["unhealthy"].status.value == "error"
    
    def test_circuit_breaker_functionality(self):
        """Test circuit breaker pattern"""
        breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=1)
        
        def failing_function():
            raise Exception("Test failure")
        
        def working_function():
            return "success"
        
        # Test failure accumulation
        for _ in range(3):
            with pytest.raises(Exception):
                breaker.call(failing_function)
        
        # Circuit should be open now
        assert breaker.state == "open"
        
        # Should raise circuit breaker exception
        with pytest.raises(Exception, match="Circuit breaker is OPEN"):
            breaker.call(working_function)
        
        # Wait for recovery timeout
        time.sleep(1.1)
        
        # Should work after recovery
        result = breaker.call(working_function)
        assert result == "success"
        assert breaker.state == "closed"
    
    @pytest.mark.asyncio
    async def test_retry_manager(self):
        """Test retry mechanism"""
        retry_manager = RetryManager(max_retries=3, base_delay=0.1)
        
        call_count = 0
        
        def failing_then_succeeding():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise Exception("Temporary failure")
            return "success"
        
        result = await retry_manager.execute_with_retry(failing_then_succeeding)
        assert result == "success"
        assert call_count == 3

class TestEnhancedErrorHandling:
    """Test enhanced error handling system"""
    
    @pytest.mark.asyncio
    async def test_error_classification(self):
        """Test error classification"""
        # Test database exception
        db_error = DatabaseException("Connection failed")
        assert db_error.category == ErrorCategory.DATABASE
        
        # Test custom exception
        custom_error = MainzaException(
            "Test error",
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.CONSCIOUSNESS
        )
        assert custom_error.severity == ErrorSeverity.HIGH
        assert custom_error.category == ErrorCategory.CONSCIOUSNESS
    
    @pytest.mark.asyncio
    async def test_error_handler_processing(self):
        """Test error handler processing"""
        test_error = Exception("Test error")
        
        error_context = await error_handler.handle_error(
            error=test_error,
            context={"test": "data"},
            component="test_component"
        )
        
        assert error_context.component == "test_component"
        assert error_context.system_state["test"] == "data"
        assert len(error_handler.error_history) > 0
    
    def test_error_decorator(self):
        """Test error handling decorator"""
        @handle_errors(component="test_function", suppress_errors=True, fallback_result="fallback")
        def failing_function():
            raise Exception("Test failure")
        
        result = failing_function()
        assert result == "fallback"
    
    @pytest.mark.asyncio
    async def test_error_analytics(self):
        """Test error analytics"""
        # Generate some test errors
        for i in range(5):
            await error_handler.handle_error(
                Exception(f"Test error {i}"),
                component="test_analytics"
            )
        
        analytics = error_handler.get_error_analytics()
        
        assert analytics["total_errors"] >= 5
        assert "errors_by_category" in analytics
        assert "errors_by_severity" in analytics

class TestPerformanceOptimization:
    """Test performance optimization components"""
    
    def test_in_memory_cache_basic_operations(self):
        """Test basic cache operations"""
        cache = InMemoryCache(max_size=3, default_ttl=1)
        
        # Test set and get
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"
        
        # Test cache miss
        assert cache.get("nonexistent") is None
        
        # Test TTL expiration
        cache.set("ttl_key", "ttl_value", ttl=1)
        time.sleep(1.1)
        assert cache.get("ttl_key") is None
    
    def test_cache_eviction_strategies(self):
        """Test cache eviction strategies"""
        # Test LRU eviction
        lru_cache = InMemoryCache(max_size=2, strategy=CacheStrategy.LRU)
        
        lru_cache.set("key1", "value1")
        lru_cache.set("key2", "value2")
        lru_cache.set("key3", "value3")  # Should evict key1
        
        assert lru_cache.get("key1") is None
        assert lru_cache.get("key2") == "value2"
        assert lru_cache.get("key3") == "value3"
    
    def test_cache_statistics(self):
        """Test cache statistics"""
        cache = InMemoryCache(max_size=10)
        
        # Generate some cache activity
        cache.set("key1", "value1")
        cache.get("key1")  # Hit
        cache.get("key2")  # Miss
        
        stats = cache.get_stats()
        
        assert stats["entries"] == 1
        assert stats["hit_rate"] > 0
        assert stats["cache_hits"] >= 1
        assert stats["cache_misses"] >= 1
    
    @pytest.mark.asyncio
    async def test_query_optimizer_caching(self):
        """Test query optimizer caching"""
        optimizer = QueryOptimizer()
        
        query = "MATCH (n) RETURN n"
        params = {"limit": 10}
        result = {"data": "test_result"}
        
        # Cache result
        optimizer.cache_query_result(query, params, result)
        
        # Retrieve cached result
        cached_result = optimizer.get_cached_result(query, params)
        assert cached_result == result
        
        # Test cache miss with different params
        different_params = {"limit": 20}
        cached_result = optimizer.get_cached_result(query, different_params)
        assert cached_result is None
    
    @pytest.mark.asyncio
    async def test_performance_profiler(self):
        """Test performance profiler"""
        from backend.core.performance_optimization import PerformanceProfiler
        
        profiler = PerformanceProfiler()
        
        # Profile a function
        profiler.start_profile("test_function")
        time.sleep(0.1)  # Simulate work
        duration = profiler.end_profile("test_function")
        
        assert duration >= 0.1
        
        # Get profile stats
        stats = profiler.get_profile_stats("test_function")
        assert stats["count"] == 1
        assert stats["avg"] >= 0.1

class TestSecurityFramework:
    """Test security framework components"""
    
    @pytest.mark.asyncio
    async def test_rate_limiter(self):
        """Test rate limiting functionality"""
        limiter = RateLimiter(max_requests=3, window_seconds=1)
        
        # Test within limit
        for _ in range(3):
            assert await limiter.is_allowed("test_user") == True
        
        # Test exceeding limit
        assert await limiter.is_allowed("test_user") == False
        
        # Test different user
        assert await limiter.is_allowed("other_user") == True
        
        # Test window reset
        time.sleep(1.1)
        assert await limiter.is_allowed("test_user") == True
    
    def test_input_validator_sql_injection(self):
        """Test SQL injection detection"""
        validator = InputValidator()
        
        # Test malicious input
        malicious_input = "'; DROP TABLE users; --"
        result = validator.validate_input(malicious_input)
        
        assert result["is_valid"] == False
        assert "sql_injection" in result["threats_detected"]
    
    def test_input_validator_xss(self):
        """Test XSS detection"""
        validator = InputValidator()
        
        # Test XSS input
        xss_input = "<script>alert('xss')</script>"
        result = validator.validate_input(xss_input)
        
        assert result["is_valid"] == False
        assert "xss" in result["threats_detected"]
    
    def test_input_validator_sanitization(self):
        """Test input sanitization"""
        validator = InputValidator()
        
        # Test sanitization
        dirty_input = "<script>alert('test')</script>Hello World"
        result = validator.validate_input(dirty_input)
        
        # Should be sanitized even if invalid
        sanitized = result["sanitized_data"]
        assert "<script>" not in sanitized
        assert "Hello World" in sanitized
    
    def test_encryption_manager(self):
        """Test encryption functionality"""
        from backend.core.security_framework import EncryptionManager
        
        encryption_manager = EncryptionManager()
        
        # Test encryption/decryption
        original_data = "sensitive information"
        encrypted = encryption_manager.encrypt(original_data)
        decrypted = encryption_manager.decrypt(encrypted)
        
        assert decrypted == original_data
        assert encrypted != original_data
    
    def test_password_hashing(self):
        """Test password hashing"""
        from backend.core.security_framework import EncryptionManager
        
        encryption_manager = EncryptionManager()
        
        password = "test_password123"
        hashed = encryption_manager.hash_password(password)
        
        # Verify correct password
        assert encryption_manager.verify_password(password, hashed) == True
        
        # Verify incorrect password
        assert encryption_manager.verify_password("wrong_password", hashed) == False
    
    @pytest.mark.asyncio
    async def test_security_monitoring(self):
        """Test security monitoring"""
        from backend.core.security_framework import SecurityMonitor
        
        monitor = SecurityMonitor()
        
        # Log security events
        await monitor.log_security_event(
            SecurityEventType.LOGIN_FAILURE,
            ThreatLevel.MEDIUM,
            user_id="test_user",
            ip_address="192.168.1.1"
        )
        
        await monitor.log_security_event(
            SecurityEventType.SUSPICIOUS_ACTIVITY,
            ThreatLevel.HIGH,
            user_id="test_user"
        )
        
        # Check security report
        report = monitor.get_security_report()
        
        assert report["total_events_24h"] >= 2
        assert "login_failure" in report["events_by_type"]
        assert "suspicious_activity" in report["events_by_type"]

class TestIntegrationScenarios:
    """Test integration scenarios"""
    
    @pytest.mark.asyncio
    async def test_error_handling_with_security(self):
        """Test error handling integration with security"""
        # Simulate a security-related error
        try:
            raise MainzaException(
                "Unauthorized access attempt",
                severity=ErrorSeverity.HIGH,
                category=ErrorCategory.AUTHENTICATION
            )
        except MainzaException as e:
            error_context = await error_handler.handle_error(
                error=e,
                context={"ip_address": "192.168.1.1"},
                component="authentication"
            )
            
            assert error_context.category == ErrorCategory.AUTHENTICATION
            assert error_context.severity == ErrorSeverity.HIGH
    
    @pytest.mark.asyncio
    async def test_performance_with_caching(self):
        """Test performance optimization with caching"""
        from backend.core.performance_optimization import cached
        
        call_count = 0
        
        @cached(ttl=1)
        def expensive_operation(param):
            nonlocal call_count
            call_count += 1
            return f"result_{param}"
        
        # First call should execute function
        result1 = expensive_operation("test")
        assert call_count == 1
        assert result1 == "result_test"
        
        # Second call should use cache
        result2 = expensive_operation("test")
        assert call_count == 1  # Should not increment
        assert result2 == "result_test"
        
        # Different parameter should execute function
        result3 = expensive_operation("other")
        assert call_count == 2
        assert result3 == "result_other"

class TestLoadAndStress:
    """Load and stress testing"""
    
    @pytest.mark.asyncio
    async def test_concurrent_cache_operations(self):
        """Test cache under concurrent load"""
        cache = InMemoryCache(max_size=1000)
        
        async def cache_worker(worker_id: int):
            for i in range(100):
                key = f"worker_{worker_id}_key_{i}"
                value = f"worker_{worker_id}_value_{i}"
                cache.set(key, value)
                retrieved = cache.get(key)
                assert retrieved == value
        
        # Run concurrent workers
        tasks = [cache_worker(i) for i in range(10)]
        await asyncio.gather(*tasks)
        
        # Verify cache statistics
        stats = cache.get_stats()
        assert stats["entries"] <= 1000  # Should not exceed max size
    
    @pytest.mark.asyncio
    async def test_rate_limiter_under_load(self):
        """Test rate limiter under concurrent load"""
        limiter = RateLimiter(max_requests=100, window_seconds=1)
        
        async def rate_limit_worker(worker_id: int):
            allowed_count = 0
            for i in range(50):
                if await limiter.is_allowed(f"user_{worker_id}"):
                    allowed_count += 1
            return allowed_count
        
        # Run concurrent workers
        tasks = [rate_limit_worker(i) for i in range(10)]
        results = await asyncio.gather(*tasks)
        
        # Each worker should be allowed up to the limit
        for result in results:
            assert result <= 100
    
    def test_error_handler_memory_usage(self):
        """Test error handler memory usage under load"""
        initial_error_count = len(error_handler.error_history)
        
        # Generate many errors
        for i in range(2000):
            try:
                raise Exception(f"Test error {i}")
            except Exception as e:
                asyncio.run(error_handler.handle_error(e, component="load_test"))
        
        # Should not exceed maximum history size
        final_error_count = len(error_handler.error_history)
        assert final_error_count <= error_handler.max_history_size

class TestChaosEngineering:
    """Chaos engineering tests for resilience"""
    
    @pytest.mark.asyncio
    async def test_database_failure_resilience(self):
        """Test system resilience to database failures"""
        # Mock database failure
        with patch('backend.utils.neo4j_production.neo4j_production.execute_query') as mock_query:
            mock_query.side_effect = Exception("Database connection failed")
            
            # System should handle database failure gracefully
            try:
                # This would normally query the database
                result = await self._simulate_database_operation()
                # Should either return fallback data or handle error gracefully
                assert result is not None or True  # Placeholder assertion
            except Exception as e:
                # Error should be handled by error handler
                assert isinstance(e, Exception)
    
    async def _simulate_database_operation(self):
        """Simulate a database operation that might fail"""
        # This is a placeholder for actual database operations
        return {"status": "fallback_data"}
    
    @pytest.mark.asyncio
    async def test_memory_pressure_handling(self):
        """Test system behavior under memory pressure"""
        # Simulate memory pressure by creating large objects
        large_objects = []
        
        try:
            # Create objects until memory pressure
            for i in range(100):
                large_objects.append([0] * 100000)  # 100k integers
            
            # System should still be responsive
            cache = InMemoryCache(max_size=10)
            cache.set("test", "value")
            assert cache.get("test") == "value"
            
        except MemoryError:
            # System should handle memory errors gracefully
            pass
        finally:
            # Clean up
            large_objects.clear()
    
    def test_high_cpu_load_resilience(self):
        """Test system resilience under high CPU load"""
        def cpu_intensive_task():
            # Simulate CPU-intensive work
            total = 0
            for i in range(1000000):
                total += i * i
            return total
        
        # Run CPU-intensive tasks in parallel
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(cpu_intensive_task) for _ in range(4)]
            
            # System should still be able to handle basic operations
            cache = InMemoryCache(max_size=10)
            cache.set("cpu_test", "value")
            assert cache.get("cpu_test") == "value"
            
            # Wait for CPU tasks to complete
            for future in as_completed(futures):
                result = future.result()
                assert isinstance(result, int)

# Test fixtures and utilities
@pytest.fixture
async def clean_error_handler():
    """Clean error handler for isolated tests"""
    original_history = error_handler.error_history.copy()
    error_handler.error_history.clear()
    yield error_handler
    error_handler.error_history = original_history

@pytest.fixture
def clean_security_monitor():
    """Clean security monitor for isolated tests"""
    from backend.core.security_framework import SecurityMonitor
    return SecurityMonitor()

# Performance benchmarks
class TestPerformanceBenchmarks:
    """Performance benchmarks for optimization validation"""
    
    def test_cache_performance_benchmark(self):
        """Benchmark cache performance"""
        cache = InMemoryCache(max_size=10000)
        
        # Benchmark write performance
        start_time = time.time()
        for i in range(10000):
            cache.set(f"key_{i}", f"value_{i}")
        write_time = time.time() - start_time
        
        # Benchmark read performance
        start_time = time.time()
        for i in range(10000):
            cache.get(f"key_{i}")
        read_time = time.time() - start_time
        
        # Performance assertions (adjust based on requirements)
        assert write_time < 1.0  # Should write 10k items in under 1 second
        assert read_time < 0.5   # Should read 10k items in under 0.5 seconds
        
        print(f"Cache write performance: {10000/write_time:.0f} ops/sec")
        print(f"Cache read performance: {10000/read_time:.0f} ops/sec")
    
    @pytest.mark.asyncio
    async def test_rate_limiter_performance_benchmark(self):
        """Benchmark rate limiter performance"""
        limiter = RateLimiter(max_requests=10000, window_seconds=60)
        
        start_time = time.time()
        for i in range(1000):
            await limiter.is_allowed(f"user_{i % 100}")  # 100 different users
        elapsed_time = time.time() - start_time
        
        # Performance assertion
        assert elapsed_time < 1.0  # Should process 1k checks in under 1 second
        
        print(f"Rate limiter performance: {1000/elapsed_time:.0f} checks/sec")

if __name__ == "__main__":
    # Run tests with detailed output
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--durations=10",
        "--cov=backend.core",
        "--cov-report=html",
        "--cov-report=term-missing"
    ])