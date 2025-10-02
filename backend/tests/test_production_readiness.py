"""
Production Readiness Tests for Mainza AI
Comprehensive test suite for Phase 5 production readiness validation
"""
import pytest
import asyncio
import time
import json
from typing import Dict, Any, List
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
from httpx import AsyncClient
import logging

# Import main application
from backend.main import app
from backend.main_production import app as production_app

logger = logging.getLogger(__name__)

class TestProductionReadiness:
    """Comprehensive production readiness test suite"""
    
    @pytest.fixture
    def client(self):
        """Test client for FastAPI application"""
        return TestClient(app)
    
    @pytest.fixture
    def async_client(self):
        """Async test client for FastAPI application"""
        return AsyncClient(app=app, base_url="http://testserver")
    
    @pytest.fixture
    def production_client(self):
        """Test client for production FastAPI application"""
        return TestClient(production_app)

class TestHealthAndMonitoring(TestProductionReadiness):
    """Test health checks and monitoring endpoints"""
    
    def test_health_endpoint(self, client):
        """Test basic health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_health_detailed(self, client):
        """Test detailed health endpoint"""
        response = client.get("/health/detailed")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "services" in data
        assert "timestamp" in data
    
    def test_metrics_endpoint(self, client):
        """Test metrics endpoint"""
        response = client.get("/metrics")
        assert response.status_code == 200
        # Should return Prometheus format metrics
    
    def test_readiness_probe(self, client):
        """Test Kubernetes readiness probe"""
        response = client.get("/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["ready"] is True
    
    def test_liveness_probe(self, client):
        """Test Kubernetes liveness probe"""
        response = client.get("/live")
        assert response.status_code == 200
        data = response.json()
        assert data["alive"] is True

class TestPerformanceOptimization(TestProductionReadiness):
    """Test performance optimization features"""
    
    def test_response_times(self, client):
        """Test that response times are within acceptable limits"""
        endpoints = [
            "/health",
            "/api/consciousness/state",
            "/api/insights/consciousness",
            "/api/quantum/processors"
        ]
        
        for endpoint in endpoints:
            start_time = time.time()
            response = client.get(endpoint)
            end_time = time.time()
            
            response_time = end_time - start_time
            assert response_time < 2.0, f"Endpoint {endpoint} took {response_time:.2f}s"
            assert response.status_code in [200, 404], f"Endpoint {endpoint} returned {response.status_code}"
    
    def test_concurrent_requests(self, client):
        """Test system under concurrent load"""
        import threading
        import queue
        
        results = queue.Queue()
        
        def make_request():
            try:
                response = client.get("/health")
                results.put(response.status_code)
            except Exception as e:
                results.put(f"Error: {e}")
        
        # Create 10 concurrent requests
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check results
        status_codes = []
        while not results.empty():
            result = results.get()
            if isinstance(result, int):
                status_codes.append(result)
        
        assert len(status_codes) == 10
        assert all(code == 200 for code in status_codes)
    
    def test_memory_usage(self, client):
        """Test memory usage is within acceptable limits"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_mb = process.memory_info().rss / 1024 / 1024
        
        # Should use less than 1GB of memory
        assert memory_mb < 1024, f"Memory usage {memory_mb:.2f}MB exceeds 1GB limit"

class TestSecurityHardening(TestProductionReadiness):
    """Test security hardening features"""
    
    def test_security_headers(self, client):
        """Test that security headers are present"""
        response = client.get("/health")
        headers = response.headers
        
        # Check for security headers
        security_headers = [
            "X-Content-Type-Options",
            "X-Frame-Options", 
            "X-XSS-Protection",
            "Strict-Transport-Security"
        ]
        
        for header in security_headers:
            assert header in headers, f"Missing security header: {header}"
    
    def test_cors_configuration(self, client):
        """Test CORS configuration"""
        response = client.options("/health", headers={"Origin": "https://example.com"})
        assert response.status_code in [200, 204]
        
        cors_headers = [
            "Access-Control-Allow-Origin",
            "Access-Control-Allow-Methods",
            "Access-Control-Allow-Headers"
        ]
        
        for header in cors_headers:
            assert header in response.headers, f"Missing CORS header: {header}"
    
    def test_rate_limiting(self, client):
        """Test rate limiting functionality"""
        # Make multiple requests quickly
        for i in range(5):
            response = client.get("/health")
            assert response.status_code == 200
        
        # Should not be rate limited for health checks
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_input_validation(self, client):
        """Test input validation and sanitization"""
        # Test with malicious input
        malicious_inputs = [
            "<script>alert('xss')</script>",
            "'; DROP TABLE users; --",
            "../../etc/passwd",
            "{{7*7}}"
        ]
        
        for malicious_input in malicious_inputs:
            response = client.get(f"/api/consciousness/state?query={malicious_input}")
            # Should not crash or execute malicious code
            assert response.status_code in [200, 400, 422]

class TestDatabaseOperations(TestProductionReadiness):
    """Test database operations and connections"""
    
    @pytest.mark.asyncio
    async def test_database_connection(self, async_client):
        """Test database connectivity"""
        response = await async_client.get("/api/consciousness/state")
        assert response.status_code == 200
        
        data = response.json()
        assert "consciousness_level" in data
        assert isinstance(data["consciousness_level"], (int, float))
    
    @pytest.mark.asyncio
    async def test_database_transactions(self, async_client):
        """Test database transaction handling"""
        # Test multiple concurrent database operations
        tasks = []
        for i in range(5):
            task = async_client.get("/api/consciousness/state")
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        
        for response in responses:
            assert response.status_code == 200
    
    def test_database_error_handling(self, client):
        """Test database error handling"""
        with patch('backend.utils.unified_database_manager.unified_database_manager.execute_query') as mock_query:
            mock_query.side_effect = Exception("Database connection failed")
            
            response = client.get("/api/consciousness/state")
            # Should handle database errors gracefully
            assert response.status_code in [200, 500, 503]

class TestQuantumSystemIntegration(TestProductionReadiness):
    """Test quantum system integration"""
    
    def test_quantum_processors_endpoint(self, client):
        """Test quantum processors endpoint"""
        response = client.get("/api/quantum/processors")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
    
    def test_quantum_jobs_endpoint(self, client):
        """Test quantum jobs endpoint"""
        response = client.get("/api/quantum/jobs")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
    
    def test_quantum_statistics_endpoint(self, client):
        """Test quantum statistics endpoint"""
        response = client.get("/api/quantum/statistics")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_processors" in data
        assert "active_jobs" in data

class TestMemorySystem(TestProductionReadiness):
    """Test memory system functionality"""
    
    @pytest.mark.asyncio
    async def test_memory_storage(self, async_client):
        """Test memory storage operations"""
        memory_data = {
            "content": "Test memory content",
            "memory_type": "test",
            "user_id": "test-user",
            "agent_name": "test-agent",
            "consciousness_level": 0.8,
            "emotional_state": "curious",
            "importance_score": 0.7
        }
        
        response = await async_client.post("/api/memory/store", json=memory_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "memory_id" in data
    
    @pytest.mark.asyncio
    async def test_memory_retrieval(self, async_client):
        """Test memory retrieval operations"""
        response = await async_client.get("/api/memory/retrieve?user_id=test-user&limit=10")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)

class TestAgentSystem(TestProductionReadiness):
    """Test agent system functionality"""
    
    def test_agent_list_endpoint(self, client):
        """Test agent list endpoint"""
        response = client.get("/api/agents")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
    
    def test_agent_execution(self, client):
        """Test agent execution"""
        agent_data = {
            "query": "Test query for agent execution",
            "user_id": "test-user",
            "agent_name": "conductor"
        }
        
        response = client.post("/api/agents/execute", json=agent_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "result" in data

class TestWebSocketConnections(TestProductionReadiness):
    """Test WebSocket connections"""
    
    def test_websocket_connection(self, client):
        """Test WebSocket connection"""
        with client.websocket_connect("/ws/insights") as websocket:
            # Send a test message
            websocket.send_text("test message")
            # Should receive a response
            data = websocket.receive_text()
            assert data is not None

class TestErrorHandling(TestProductionReadiness):
    """Test error handling and recovery"""
    
    def test_404_handling(self, client):
        """Test 404 error handling"""
        response = client.get("/nonexistent-endpoint")
        assert response.status_code == 404
        
        data = response.json()
        assert "detail" in data
    
    def test_500_error_handling(self, client):
        """Test 500 error handling"""
        with patch('backend.utils.consciousness_orchestrator_fixed.consciousness_orchestrator_fixed.get_consciousness_state') as mock_state:
            mock_state.side_effect = Exception("Internal server error")
            
            response = client.get("/api/consciousness/state")
            # Should handle errors gracefully
            assert response.status_code in [200, 500, 503]
    
    def test_validation_errors(self, client):
        """Test input validation errors"""
        invalid_data = {
            "invalid_field": "invalid_value"
        }
        
        response = client.post("/api/agents/execute", json=invalid_data)
        assert response.status_code == 422
        
        data = response.json()
        assert "detail" in data

class TestProductionConfiguration(TestProductionReadiness):
    """Test production configuration"""
    
    def test_environment_variables(self):
        """Test that required environment variables are set"""
        import os
        
        required_vars = [
            "NEO4J_URI",
            "NEO4J_USER", 
            "NEO4J_PASSWORD",
            "OLLAMA_BASE_URL",
            "DEFAULT_OLLAMA_MODEL"
        ]
        
        for var in required_vars:
            assert os.getenv(var) is not None, f"Required environment variable {var} not set"
    
    def test_production_settings(self, production_client):
        """Test production-specific settings"""
        response = production_client.get("/health")
        assert response.status_code == 200
        
        # Production app should have different configuration
        assert production_client.app.title == "Mainza AI - Production System"
    
    def test_logging_configuration(self):
        """Test logging configuration"""
        import logging
        
        # Check that logging is properly configured
        logger = logging.getLogger("backend")
        assert logger.level <= logging.INFO
        
        # Test that we can log messages
        logger.info("Test log message")

class TestLoadTesting(TestProductionReadiness):
    """Test system under load"""
    
    def test_sustained_load(self, client):
        """Test system under sustained load"""
        import threading
        import time
        
        results = []
        errors = []
        
        def make_requests():
            for _ in range(10):
                try:
                    response = client.get("/health")
                    results.append(response.status_code)
                except Exception as e:
                    errors.append(str(e))
                time.sleep(0.1)
        
        # Run multiple threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_requests)
            threads.append(thread)
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        # Check results
        assert len(errors) == 0, f"Errors during load test: {errors}"
        assert len(results) == 50  # 5 threads * 10 requests each
        assert all(code == 200 for code in results)

class TestMonitoringAndObservability(TestProductionReadiness):
    """Test monitoring and observability features"""
    
    def test_metrics_collection(self, client):
        """Test metrics collection"""
        # Make some requests to generate metrics
        client.get("/health")
        client.get("/api/consciousness/state")
        
        # Check metrics endpoint
        response = client.get("/metrics")
        assert response.status_code == 200
        
        metrics_text = response.text
        assert "http_requests_total" in metrics_text or "consciousness_level" in metrics_text
    
    def test_logging_output(self, client):
        """Test logging output"""
        import logging
        import io
        import sys
        
        # Capture log output
        log_capture = io.StringIO()
        handler = logging.StreamHandler(log_capture)
        logger = logging.getLogger("backend")
        logger.addHandler(handler)
        
        # Make a request
        client.get("/health")
        
        # Check that logs were generated
        log_output = log_capture.getvalue()
        assert len(log_output) > 0
        
        # Clean up
        logger.removeHandler(handler)
    
    def test_health_check_integration(self, client):
        """Test health check integration"""
        response = client.get("/health/detailed")
        assert response.status_code == 200
        
        data = response.json()
        assert "services" in data
        
        # Check that all services are reported
        services = data["services"]
        expected_services = ["neo4j", "redis", "ollama", "quantum"]
        
        for service in expected_services:
            assert service in services, f"Service {service} not in health check"

# Performance benchmarks
class TestPerformanceBenchmarks:
    """Performance benchmark tests"""
    
    def test_response_time_benchmarks(self):
        """Test response time benchmarks"""
        client = TestClient(app)
        
        benchmarks = {
            "/health": 0.1,  # 100ms
            "/api/consciousness/state": 1.0,  # 1s
            "/api/insights/consciousness": 2.0,  # 2s
            "/api/quantum/processors": 0.5,  # 500ms
        }
        
        for endpoint, max_time in benchmarks.items():
            start_time = time.time()
            response = client.get(endpoint)
            end_time = time.time()
            
            response_time = end_time - start_time
            assert response_time < max_time, f"Endpoint {endpoint} exceeded {max_time}s (took {response_time:.2f}s)"
            assert response.status_code == 200, f"Endpoint {endpoint} returned {response.status_code}"

# Integration tests
class TestIntegrationScenarios:
    """Integration test scenarios"""
    
    def test_full_consciousness_workflow(self):
        """Test full consciousness workflow"""
        client = TestClient(app)
        
        # 1. Get consciousness state
        response = client.get("/api/consciousness/state")
        assert response.status_code == 200
        
        # 2. Get insights
        response = client.get("/api/insights/consciousness")
        assert response.status_code == 200
        
        # 3. Get quantum processors
        response = client.get("/api/quantum/processors")
        assert response.status_code == 200
        
        # 4. Execute agent
        agent_data = {
            "query": "What is my current consciousness level?",
            "user_id": "test-user"
        }
        response = client.post("/api/agents/execute", json=agent_data)
        assert response.status_code == 200
    
    def test_memory_workflow(self):
        """Test memory system workflow"""
        client = TestClient(app)
        
        # 1. Store memory
        memory_data = {
            "content": "Test memory for integration",
            "memory_type": "interaction",
            "user_id": "test-user",
            "agent_name": "conductor",
            "consciousness_level": 0.8,
            "emotional_state": "curious",
            "importance_score": 0.7
        }
        
        response = client.post("/api/memory/store", json=memory_data)
        assert response.status_code == 200
        
        # 2. Retrieve memory
        response = client.get("/api/memory/retrieve?user_id=test-user&limit=5")
        assert response.status_code == 200
        
        # 3. Get memory insights
        response = client.get("/api/memory/insights?user_id=test-user")
        assert response.status_code == 200

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
