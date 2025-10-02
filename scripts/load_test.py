#!/usr/bin/env python3
"""
Load Testing Script for Mainza AI
Comprehensive load testing for production readiness validation
"""
import asyncio
import aiohttp
import time
import json
import statistics
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import argparse
import sys

@dataclass
class LoadTestResult:
    """Load test result data class"""
    endpoint: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_response_time: float
    min_response_time: float
    max_response_time: float
    requests_per_second: float
    error_rate: float
    errors: List[str]

class LoadTester:
    """Comprehensive load testing system"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results: List[LoadTestResult] = []
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def test_endpoint(self, endpoint: str, method: str = "GET", 
                          payload: Dict[str, Any] = None, 
                          concurrent_users: int = 10, 
                          requests_per_user: int = 10,
                          timeout: int = 30) -> LoadTestResult:
        """Test a single endpoint under load"""
        
        print(f"🧪 Testing {endpoint} with {concurrent_users} concurrent users, {requests_per_user} requests each")
        
        start_time = time.time()
        response_times = []
        errors = []
        successful_requests = 0
        failed_requests = 0
        
        async def make_request():
            """Make a single request"""
            try:
                request_start = time.time()
                
                if method.upper() == "GET":
                    async with self.session.get(f"{self.base_url}{endpoint}", timeout=timeout) as response:
                        await response.text()
                elif method.upper() == "POST":
                    async with self.session.post(f"{self.base_url}{endpoint}", 
                                               json=payload, timeout=timeout) as response:
                        await response.text()
                elif method.upper() == "PUT":
                    async with self.session.put(f"{self.base_url}{endpoint}", 
                                              json=payload, timeout=timeout) as response:
                        await response.text()
                elif method.upper() == "DELETE":
                    async with self.session.delete(f"{self.base_url}{endpoint}", timeout=timeout) as response:
                        await response.text()
                
                request_end = time.time()
                response_time = (request_end - request_start) * 1000  # Convert to ms
                response_times.append(response_time)
                
                if response.status < 400:
                    successful_requests += 1
                else:
                    failed_requests += 1
                    errors.append(f"HTTP {response.status}")
                    
            except asyncio.TimeoutError:
                failed_requests += 1
                errors.append("Timeout")
            except Exception as e:
                failed_requests += 1
                errors.append(str(e))
        
        # Create tasks for concurrent requests
        tasks = []
        for _ in range(concurrent_users):
            for _ in range(requests_per_user):
                tasks.append(make_request())
        
        # Execute all requests concurrently
        await asyncio.gather(*tasks, return_exceptions=True)
        
        end_time = time.time()
        total_time = end_time - start_time
        total_requests = concurrent_users * requests_per_user
        
        # Calculate metrics
        if response_times:
            avg_response_time = statistics.mean(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
        else:
            avg_response_time = min_response_time = max_response_time = 0
        
        requests_per_second = total_requests / total_time if total_time > 0 else 0
        error_rate = failed_requests / total_requests if total_requests > 0 else 0
        
        result = LoadTestResult(
            endpoint=endpoint,
            total_requests=total_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            average_response_time=avg_response_time,
            min_response_time=min_response_time,
            max_response_time=max_response_time,
            requests_per_second=requests_per_second,
            error_rate=error_rate,
            errors=errors[:10]  # Keep only first 10 errors
        )
        
        self.results.append(result)
        return result
    
    async def test_health_endpoints(self):
        """Test health and monitoring endpoints"""
        print("🏥 Testing health endpoints...")
        
        health_endpoints = [
            "/health",
            "/health/detailed",
            "/ready",
            "/live",
            "/metrics"
        ]
        
        for endpoint in health_endpoints:
            await self.test_endpoint(endpoint, concurrent_users=5, requests_per_user=5)
    
    async def test_api_endpoints(self):
        """Test main API endpoints"""
        print("🔌 Testing API endpoints...")
        
        api_endpoints = [
            ("/api/consciousness/state", "GET"),
            ("/api/insights/consciousness", "GET"),
            ("/api/quantum/processors", "GET"),
            ("/api/quantum/jobs", "GET"),
            ("/api/quantum/statistics", "GET"),
            ("/api/agents", "GET"),
            ("/api/memory/retrieve?user_id=test-user&limit=10", "GET")
        ]
        
        for endpoint, method in api_endpoints:
            await self.test_endpoint(endpoint, method, concurrent_users=3, requests_per_user=3)
    
    async def test_agent_execution(self):
        """Test agent execution under load"""
        print("🤖 Testing agent execution...")
        
        agent_payload = {
            "query": "What is my current consciousness level?",
            "user_id": "load-test-user",
            "agent_name": "conductor"
        }
        
        await self.test_endpoint("/api/agents/execute", "POST", agent_payload, 
                               concurrent_users=2, requests_per_user=2, timeout=60)
    
    async def test_memory_operations(self):
        """Test memory operations under load"""
        print("🧠 Testing memory operations...")
        
        memory_payload = {
            "content": "Load test memory content",
            "memory_type": "test",
            "user_id": "load-test-user",
            "agent_name": "test-agent",
            "consciousness_level": 0.8,
            "emotional_state": "curious",
            "importance_score": 0.7
        }
        
        await self.test_endpoint("/api/memory/store", "POST", memory_payload,
                               concurrent_users=2, requests_per_user=2)
    
    async def test_websocket_connections(self):
        """Test WebSocket connections"""
        print("🔌 Testing WebSocket connections...")
        
        # This would test WebSocket connections
        # Implementation depends on WebSocket testing requirements
        pass
    
    async def run_comprehensive_test(self):
        """Run comprehensive load test suite"""
        print("🚀 Starting comprehensive load test for Mainza AI")
        print("=" * 60)
        
        start_time = time.time()
        
        # Test health endpoints
        await self.test_health_endpoints()
        
        # Test API endpoints
        await self.test_api_endpoints()
        
        # Test agent execution
        await self.test_agent_execution()
        
        # Test memory operations
        await self.test_memory_operations()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print("=" * 60)
        print(f"✅ Load testing completed in {total_time:.2f} seconds")
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate load test report"""
        print("\n📊 LOAD TEST REPORT")
        print("=" * 60)
        
        total_requests = sum(r.total_requests for r in self.results)
        total_successful = sum(r.successful_requests for r in self.results)
        total_failed = sum(r.failed_requests for r in self.results)
        overall_success_rate = (total_successful / total_requests * 100) if total_requests > 0 else 0
        
        print(f"Total Requests: {total_requests}")
        print(f"Successful: {total_successful}")
        print(f"Failed: {total_failed}")
        print(f"Overall Success Rate: {overall_success_rate:.2f}%")
        print()
        
        # Individual endpoint results
        for result in self.results:
            print(f"Endpoint: {result.endpoint}")
            print(f"  Requests: {result.total_requests}")
            print(f"  Success Rate: {((result.successful_requests / result.total_requests) * 100):.2f}%")
            print(f"  Avg Response Time: {result.average_response_time:.2f}ms")
            print(f"  Min Response Time: {result.min_response_time:.2f}ms")
            print(f"  Max Response Time: {result.max_response_time:.2f}ms")
            print(f"  Requests/sec: {result.requests_per_second:.2f}")
            if result.errors:
                print(f"  Errors: {', '.join(set(result.errors))}")
            print()
        
        # Performance analysis
        self.analyze_performance()
    
    def analyze_performance(self):
        """Analyze performance and provide recommendations"""
        print("🔍 PERFORMANCE ANALYSIS")
        print("=" * 60)
        
        # Check for performance issues
        issues = []
        recommendations = []
        
        for result in self.results:
            # Check response times
            if result.average_response_time > 2000:  # 2 seconds
                issues.append(f"Slow response time for {result.endpoint}: {result.average_response_time:.2f}ms")
                recommendations.append("Consider optimizing database queries or adding caching")
            
            # Check error rates
            if result.error_rate > 0.05:  # 5%
                issues.append(f"High error rate for {result.endpoint}: {result.error_rate:.2%}")
                recommendations.append("Investigate and fix error causes")
            
            # Check throughput
            if result.requests_per_second < 1:
                issues.append(f"Low throughput for {result.endpoint}: {result.requests_per_second:.2f} req/s")
                recommendations.append("Consider horizontal scaling or performance optimization")
        
        if issues:
            print("⚠️  PERFORMANCE ISSUES DETECTED:")
            for issue in issues:
                print(f"  - {issue}")
            print()
        
        if recommendations:
            print("💡 RECOMMENDATIONS:")
            for rec in set(recommendations):
                print(f"  - {rec}")
            print()
        
        # Overall assessment
        if not issues:
            print("✅ All endpoints performing within acceptable limits")
        else:
            print(f"❌ {len(issues)} performance issues detected")
        
        # Save results to file
        self.save_results()
    
    def save_results(self):
        """Save test results to file"""
        results_data = {
            "timestamp": time.time(),
            "total_requests": sum(r.total_requests for r in self.results),
            "total_successful": sum(r.successful_requests for r in self.results),
            "total_failed": sum(r.failed_requests for r in self.results),
            "results": [
                {
                    "endpoint": r.endpoint,
                    "total_requests": r.total_requests,
                    "successful_requests": r.successful_requests,
                    "failed_requests": r.failed_requests,
                    "average_response_time": r.average_response_time,
                    "min_response_time": r.min_response_time,
                    "max_response_time": r.max_response_time,
                    "requests_per_second": r.requests_per_second,
                    "error_rate": r.error_rate,
                    "errors": r.errors
                }
                for r in self.results
            ]
        }
        
        with open("load_test_results.json", "w") as f:
            json.dump(results_data, f, indent=2)
        
        print(f"📁 Results saved to load_test_results.json")

async def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Load test Mainza AI system")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL to test")
    parser.add_argument("--quick", action="store_true", help="Run quick test with fewer requests")
    
    args = parser.parse_args()
    
    async with LoadTester(args.url) as tester:
        if args.quick:
            print("🏃 Running quick load test...")
            await tester.test_health_endpoints()
            await tester.test_api_endpoints()
        else:
            await tester.run_comprehensive_test()

if __name__ == "__main__":
    asyncio.run(main())
