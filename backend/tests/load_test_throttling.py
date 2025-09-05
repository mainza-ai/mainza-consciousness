"""
Load testing script for throttling response processing
Tests system behavior under various load conditions and throttling scenarios
"""

import asyncio
import aiohttp
import time
import json
import statistics
import sys
import os
from typing import Dict, List, Any, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from dataclasses import dataclass
from datetime import datetime
import psutil

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, backend_path)


@dataclass
class LoadTestResult:
    """Result of a load test scenario"""
    scenario_name: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    throttled_responses: int
    total_time_seconds: float
    avg_response_time_ms: float
    min_response_time_ms: float
    max_response_time_ms: float
    requests_per_second: float
    error_rate_percent: float
    throttling_rate_percent: float
    memory_usage_mb: float
    cpu_usage_percent: float


class ThrottlingLoadTester:
    """Load tester for throttling response processing"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results: List[LoadTestResult] = []
    
    async def make_request(self, session: aiohttp.ClientSession, query: str, user_id: str) -> Tuple[bool, float, bool, str]:
        """
        Make a single request and return (success, response_time_ms, is_throttled, response_text)
        """
        start_time = time.perf_counter()
        
        try:
            payload = {
                "query": query,
                "user_id": user_id,
                "consciousness_context": {
                    "consciousness_level": 0.7,
                    "emotional_state": "curious"
                }
            }
            
            async with session.post(
                f"{self.base_url}/enhanced_router_chat",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                end_time = time.perf_counter()
                response_time_ms = (end_time - start_time) * 1000
                
                if response.status == 200:
                    response_data = await response.json()
                    response_text = response_data.get('response', '')
                    
                    # Check if response indicates throttling
                    is_throttled = any(word in response_text.lower() for word in 
                                     ['processing', 'busy', 'try again', 'moment', 'throttled'])
                    
                    return True, response_time_ms, is_throttled, response_text
                else:
                    return False, response_time_ms, False, f"HTTP {response.status}"
                    
        except Exception as e:
            end_time = time.perf_counter()
            response_time_ms = (end_time - start_time) * 1000
            return False, response_time_ms, False, str(e)
    
    async def run_concurrent_load_test(
        self, 
        scenario_name: str,
        num_requests: int,
        concurrent_users: int,
        request_delay_ms: int = 0
    ) -> LoadTestResult:
        """Run a concurrent load test scenario"""
        
        print(f"Running load test: {scenario_name}")
        print(f"  Requests: {num_requests}, Concurrent Users: {concurrent_users}, Delay: {request_delay_ms}ms")
        
        # Track system resources
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024
        
        successful_requests = 0
        failed_requests = 0
        throttled_responses = 0
        response_times = []
        
        start_time = time.perf_counter()
        
        async with aiohttp.ClientSession() as session:
            semaphore = asyncio.Semaphore(concurrent_users)
            
            async def make_limited_request(request_id: int):
                async with semaphore:
                    if request_delay_ms > 0:
                        await asyncio.sleep(request_delay_ms / 1000)
                    
                    query = f"Load test query {request_id} for scenario {scenario_name}"
                    user_id = f"load_test_user_{request_id % concurrent_users}"
                    
                    return await self.make_request(session, query, user_id)
            
            # Create all tasks
            tasks = [make_limited_request(i) for i in range(num_requests)]
            
            # Execute tasks and collect results
            for task in asyncio.as_completed(tasks):
                success, response_time_ms, is_throttled, response_text = await task
                
                response_times.append(response_time_ms)
                
                if success:
                    successful_requests += 1
                    if is_throttled:
                        throttled_responses += 1
                else:
                    failed_requests += 1
        
        end_time = time.perf_counter()
        total_time = end_time - start_time
        
        # Calculate final metrics
        final_memory = process.memory_info().rss / 1024 / 1024
        memory_usage = final_memory - initial_memory
        cpu_usage = psutil.cpu_percent(interval=1)
        
        # Calculate statistics
        avg_response_time = statistics.mean(response_times) if response_times else 0
        min_response_time = min(response_times) if response_times else 0
        max_response_time = max(response_times) if response_times else 0
        requests_per_second = num_requests / total_time if total_time > 0 else 0
        error_rate = (failed_requests / num_requests) * 100 if num_requests > 0 else 0
        throttling_rate = (throttled_responses / successful_requests) * 100 if successful_requests > 0 else 0
        
        result = LoadTestResult(
            scenario_name=scenario_name,
            total_requests=num_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            throttled_responses=throttled_responses,
            total_time_seconds=total_time,
            avg_response_time_ms=avg_response_time,
            min_response_time_ms=min_response_time,
            max_response_time_ms=max_response_time,
            requests_per_second=requests_per_second,
            error_rate_percent=error_rate,
            throttling_rate_percent=throttling_rate,
            memory_usage_mb=memory_usage,
            cpu_usage_percent=cpu_usage
        )
        
        self.results.append(result)
        
        print(f"  Completed: {successful_requests}/{num_requests} successful, "
              f"{throttled_responses} throttled, {failed_requests} failed")
        print(f"  Performance: {requests_per_second:.1f} req/s, "
              f"{avg_response_time:.1f}ms avg response time")
        print()
        
        return result
    
    def run_synthetic_load_test(
        self,
        scenario_name: str,
        num_requests: int,
        throttling_rate: float = 0.0
    ) -> LoadTestResult:
        """Run synthetic load test without actual HTTP requests"""
        
        print(f"Running synthetic load test: {scenario_name}")
        print(f"  Requests: {num_requests}, Simulated Throttling Rate: {throttling_rate:.1%}")
        
        # Import here to avoid circular imports
        original_cwd = os.getcwd()
        backend_path = os.path.join(os.path.dirname(__file__), '..')
        os.chdir(backend_path)
        try:
            from agentic_router import extract_response_from_result
        finally:
            os.chdir(original_cwd)
        
        consciousness_context = {
            "consciousness_level": 0.7,
            "emotional_state": "curious",
            "user_id": "load_test_user"
        }
        
        successful_requests = 0
        failed_requests = 0
        throttled_responses = 0
        response_times = []
        
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024
        
        start_time = time.perf_counter()
        
        for i in range(num_requests):
            request_start = time.perf_counter()
            
            try:
                # Simulate different response types based on throttling rate
                import random
                if random.random() < throttling_rate:
                    # Simulate throttled response
                    response = {
                        "response": f"I'm currently processing other requests. Please try again in a moment.",
                        "status": "throttled"
                    }
                    is_throttled = True
                else:
                    # Simulate normal response
                    response = f"Normal response to load test query {i}"
                    is_throttled = False
                
                # Process through response extraction
                result = extract_response_from_result(
                    response,
                    f"Load test query {i}",
                    consciousness_context
                )
                
                request_end = time.perf_counter()
                response_time_ms = (request_end - request_start) * 1000
                response_times.append(response_time_ms)
                
                successful_requests += 1
                if is_throttled:
                    throttled_responses += 1
                    
            except Exception as e:
                request_end = time.perf_counter()
                response_time_ms = (request_end - request_start) * 1000
                response_times.append(response_time_ms)
                failed_requests += 1
        
        end_time = time.perf_counter()
        total_time = end_time - start_time
        
        final_memory = process.memory_info().rss / 1024 / 1024
        memory_usage = final_memory - initial_memory
        cpu_usage = psutil.cpu_percent(interval=0.1)
        
        # Calculate statistics
        avg_response_time = statistics.mean(response_times) if response_times else 0
        min_response_time = min(response_times) if response_times else 0
        max_response_time = max(response_times) if response_times else 0
        requests_per_second = num_requests / total_time if total_time > 0 else 0
        error_rate = (failed_requests / num_requests) * 100 if num_requests > 0 else 0
        throttling_rate_actual = (throttled_responses / successful_requests) * 100 if successful_requests > 0 else 0
        
        result = LoadTestResult(
            scenario_name=scenario_name,
            total_requests=num_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            throttled_responses=throttled_responses,
            total_time_seconds=total_time,
            avg_response_time_ms=avg_response_time,
            min_response_time_ms=min_response_time,
            max_response_time_ms=max_response_time,
            requests_per_second=requests_per_second,
            error_rate_percent=error_rate,
            throttling_rate_percent=throttling_rate_actual,
            memory_usage_mb=memory_usage,
            cpu_usage_percent=cpu_usage
        )
        
        self.results.append(result)
        
        print(f"  Completed: {successful_requests}/{num_requests} successful, "
              f"{throttled_responses} throttled, {failed_requests} failed")
        print(f"  Performance: {requests_per_second:.1f} req/s, "
              f"{avg_response_time:.3f}ms avg response time")
        print()
        
        return result
    
    async def run_all_load_tests(self, include_http_tests: bool = False):
        """Run comprehensive load test suite"""
        
        print("Starting comprehensive load test suite...")
        print("=" * 60)
        
        # Synthetic load tests (always run)
        print("SYNTHETIC LOAD TESTS (Direct Function Calls)")
        print("-" * 50)
        
        # Basic performance test
        self.run_synthetic_load_test("Basic Performance", 10000, 0.0)
        
        # Light throttling
        self.run_synthetic_load_test("Light Throttling", 5000, 0.1)
        
        # Moderate throttling
        self.run_synthetic_load_test("Moderate Throttling", 5000, 0.3)
        
        # Heavy throttling
        self.run_synthetic_load_test("Heavy Throttling", 5000, 0.5)
        
        # Extreme throttling
        self.run_synthetic_load_test("Extreme Throttling", 2000, 0.8)
        
        # High volume test
        self.run_synthetic_load_test("High Volume", 50000, 0.2)
        
        if include_http_tests:
            print("HTTP LOAD TESTS (Requires Running Server)")
            print("-" * 50)
            
            try:
                # Test if server is running
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.base_url}/health", timeout=aiohttp.ClientTimeout(total=5)) as response:
                        if response.status != 200:
                            raise Exception("Server not healthy")
                
                # Low concurrency
                await self.run_concurrent_load_test("Low Concurrency", 100, 5, 100)
                
                # Medium concurrency
                await self.run_concurrent_load_test("Medium Concurrency", 200, 20, 50)
                
                # High concurrency
                await self.run_concurrent_load_test("High Concurrency", 500, 50, 10)
                
                # Burst test
                await self.run_concurrent_load_test("Burst Test", 1000, 100, 0)
                
            except Exception as e:
                print(f"Skipping HTTP tests - server not available: {e}")
                print()
    
    def generate_load_test_report(self) -> str:
        """Generate comprehensive load test report"""
        
        if not self.results:
            return "No load test results available."
        
        report = []
        report.append("THROTTLING RESPONSE PROCESSING - LOAD TEST REPORT")
        report.append("=" * 60)
        report.append(f"Timestamp: {datetime.now().isoformat()}")
        report.append(f"Total Scenarios: {len(self.results)}")
        report.append("")
        
        # Individual scenario results
        report.append("SCENARIO RESULTS")
        report.append("-" * 30)
        
        for result in self.results:
            report.append(f"Scenario: {result.scenario_name}")
            report.append(f"  Requests: {result.total_requests:,} total, "
                         f"{result.successful_requests:,} successful, "
                         f"{result.failed_requests:,} failed")
            report.append(f"  Throttling: {result.throttled_responses:,} responses "
                         f"({result.throttling_rate_percent:.1f}%)")
            report.append(f"  Performance: {result.requests_per_second:.1f} req/s, "
                         f"{result.avg_response_time_ms:.2f}ms avg")
            report.append(f"  Response Times: {result.min_response_time_ms:.2f}ms min, "
                         f"{result.max_response_time_ms:.2f}ms max")
            report.append(f"  Resources: {result.memory_usage_mb:.1f}MB memory, "
                         f"{result.cpu_usage_percent:.1f}% CPU")
            report.append(f"  Error Rate: {result.error_rate_percent:.2f}%")
            report.append("")
        
        # Performance summary
        report.append("PERFORMANCE SUMMARY")
        report.append("-" * 30)
        
        # Best and worst performance
        best_throughput = max(self.results, key=lambda x: x.requests_per_second)
        worst_throughput = min(self.results, key=lambda x: x.requests_per_second)
        
        report.append(f"Best Throughput: {best_throughput.scenario_name} - "
                     f"{best_throughput.requests_per_second:.1f} req/s")
        report.append(f"Worst Throughput: {worst_throughput.scenario_name} - "
                     f"{worst_throughput.requests_per_second:.1f} req/s")
        
        # Response time analysis
        avg_response_times = [r.avg_response_time_ms for r in self.results]
        fastest_avg = min(avg_response_times)
        slowest_avg = max(avg_response_times)
        
        report.append(f"Fastest Avg Response: {fastest_avg:.2f}ms")
        report.append(f"Slowest Avg Response: {slowest_avg:.2f}ms")
        
        # Throttling analysis
        throttling_scenarios = [r for r in self.results if r.throttled_responses > 0]
        if throttling_scenarios:
            avg_throttling_rate = statistics.mean([r.throttling_rate_percent for r in throttling_scenarios])
            report.append(f"Average Throttling Rate: {avg_throttling_rate:.1f}%")
        
        # Error analysis
        total_requests = sum(r.total_requests for r in self.results)
        total_errors = sum(r.failed_requests for r in self.results)
        overall_error_rate = (total_errors / total_requests) * 100 if total_requests > 0 else 0
        
        report.append(f"Overall Error Rate: {overall_error_rate:.2f}%")
        report.append("")
        
        # Resource usage analysis
        report.append("RESOURCE USAGE ANALYSIS")
        report.append("-" * 30)
        
        memory_usage = [r.memory_usage_mb for r in self.results]
        cpu_usage = [r.cpu_usage_percent for r in self.results]
        
        report.append(f"Memory Usage: {min(memory_usage):.1f}MB min, "
                     f"{max(memory_usage):.1f}MB max, "
                     f"{statistics.mean(memory_usage):.1f}MB avg")
        report.append(f"CPU Usage: {min(cpu_usage):.1f}% min, "
                     f"{max(cpu_usage):.1f}% max, "
                     f"{statistics.mean(cpu_usage):.1f}% avg")
        report.append("")
        
        # Recommendations
        report.append("RECOMMENDATIONS")
        report.append("-" * 30)
        
        # Performance recommendations
        if slowest_avg > 10:
            report.append("• Response times are high - consider optimization")
        
        if overall_error_rate > 1:
            report.append("• Error rate is elevated - investigate failure causes")
        
        if max(memory_usage) > 100:
            report.append("• High memory usage detected - check for memory leaks")
        
        if max(cpu_usage) > 80:
            report.append("• High CPU usage - consider performance optimization")
        
        # Throttling recommendations
        high_throttling_scenarios = [r for r in self.results if r.throttling_rate_percent > 30]
        if high_throttling_scenarios:
            report.append("• High throttling rates detected - consider capacity planning")
        
        # Scalability recommendations
        throughput_variance = max([r.requests_per_second for r in self.results]) - min([r.requests_per_second for r in self.results])
        if throughput_variance > 1000:
            report.append("• Large throughput variance - investigate scalability bottlenecks")
        
        return "\n".join(report)
    
    def save_results(self, filename: str = None):
        """Save load test results to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"throttling_load_test_results_{timestamp}.json"
        
        results_data = {
            'timestamp': datetime.now().isoformat(),
            'scenarios': [
                {
                    'scenario_name': r.scenario_name,
                    'total_requests': r.total_requests,
                    'successful_requests': r.successful_requests,
                    'failed_requests': r.failed_requests,
                    'throttled_responses': r.throttled_responses,
                    'total_time_seconds': r.total_time_seconds,
                    'avg_response_time_ms': r.avg_response_time_ms,
                    'min_response_time_ms': r.min_response_time_ms,
                    'max_response_time_ms': r.max_response_time_ms,
                    'requests_per_second': r.requests_per_second,
                    'error_rate_percent': r.error_rate_percent,
                    'throttling_rate_percent': r.throttling_rate_percent,
                    'memory_usage_mb': r.memory_usage_mb,
                    'cpu_usage_percent': r.cpu_usage_percent
                }
                for r in self.results
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(results_data, f, indent=2)
        
        print(f"Load test results saved to: {filename}")


async def main():
    """Run the load test suite"""
    
    # Check if server should be tested
    import argparse
    parser = argparse.ArgumentParser(description='Run throttling load tests')
    parser.add_argument('--include-http', action='store_true', 
                       help='Include HTTP tests (requires running server)')
    args = parser.parse_args()
    
    tester = ThrottlingLoadTester()
    
    try:
        await tester.run_all_load_tests(include_http_tests=args.include_http)
        
        # Generate and display report
        report = tester.generate_load_test_report()
        print(report)
        
        # Save results
        tester.save_results()
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"throttling_load_test_report_{timestamp}.txt"
        with open(report_filename, 'w') as f:
            f.write(report)
        print(f"Load test report saved to: {report_filename}")
        
    except Exception as e:
        print(f"Load test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())