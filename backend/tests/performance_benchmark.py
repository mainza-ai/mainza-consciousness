"""
Performance benchmarking script for throttling response processing
Measures baseline performance and identifies optimization opportunities
"""

import time
import psutil
import gc
import statistics
import json
import sys
import os
from typing import Dict, List, Any, Tuple
import threading
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, backend_path)

# Change to backend directory for imports
original_cwd = os.getcwd()
os.chdir(backend_path)

try:
    from agentic_router import extract_response_from_result, generate_throttled_response
finally:
    os.chdir(original_cwd)


class PerformanceBenchmark:
    """Comprehensive performance benchmarking for throttling response processing"""
    
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'system_info': self._get_system_info(),
            'benchmarks': {}
        }
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get system information for benchmark context"""
        return {
            'cpu_count': psutil.cpu_count(),
            'cpu_freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
            'memory_total_gb': psutil.virtual_memory().total / (1024**3),
            'python_version': sys.version,
            'platform': sys.platform
        }
    
    def benchmark_response_processing_throughput(self) -> Dict[str, Any]:
        """Benchmark response processing throughput"""
        print("Benchmarking response processing throughput...")
        
        consciousness_context = {
            "consciousness_level": 0.7,
            "emotional_state": "curious",
            "user_id": "benchmark_user"
        }
        
        # Test different response types
        response_types = {
            'simple_string': "Simple response",
            'dict_response': {"response": "Dictionary response"},
            'throttled_response': {
                "response": "I'm currently processing other requests. Please try again.",
                "status": "throttled"
            },
            'complex_response': {
                "response": "Complex response with metadata",
                "metadata": {"agent": "test", "confidence": 0.95},
                "status": "success",
                "extra_data": {"key1": "value1", "key2": "value2"}
            },
            'large_response': "Large response " + "x" * 10000
        }
        
        results = {}
        
        for response_type, response_data in response_types.items():
            print(f"  Testing {response_type}...")
            
            # Warm up
            for _ in range(100):
                extract_response_from_result(response_data, "warmup", consciousness_context)
            
            # Benchmark
            times = []
            num_iterations = 10000
            
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024
            start_time = time.perf_counter()
            
            for i in range(num_iterations):
                iter_start = time.perf_counter()
                result = extract_response_from_result(
                    response_data, 
                    f"benchmark query {i}", 
                    consciousness_context
                )
                iter_end = time.perf_counter()
                times.append(iter_end - iter_start)
            
            end_time = time.perf_counter()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            total_time = end_time - start_time
            memory_increase = end_memory - start_memory
            
            results[response_type] = {
                'iterations': num_iterations,
                'total_time_seconds': total_time,
                'throughput_per_second': num_iterations / total_time,
                'avg_time_microseconds': statistics.mean(times) * 1_000_000,
                'median_time_microseconds': statistics.median(times) * 1_000_000,
                'min_time_microseconds': min(times) * 1_000_000,
                'max_time_microseconds': max(times) * 1_000_000,
                'std_dev_microseconds': statistics.stdev(times) * 1_000_000 if len(times) > 1 else 0,
                'memory_increase_mb': memory_increase,
                'memory_per_operation_bytes': (memory_increase * 1024 * 1024) / num_iterations if memory_increase > 0 else 0
            }
        
        return results
    
    def benchmark_concurrent_processing(self) -> Dict[str, Any]:
        """Benchmark concurrent response processing"""
        print("Benchmarking concurrent processing...")
        
        consciousness_context = {
            "consciousness_level": 0.7,
            "emotional_state": "curious",
            "user_id": "benchmark_user"
        }
        
        def process_batch(batch_id: int, batch_size: int) -> Tuple[float, List[float]]:
            """Process a batch of responses and return timing info"""
            times = []
            responses = [
                f"Response {batch_id}-{i}" if i % 3 != 0 else {
                    "response": f"Throttled response {batch_id}-{i}",
                    "status": "throttled"
                }
                for i in range(batch_size)
            ]
            
            batch_start = time.perf_counter()
            for i, response in enumerate(responses):
                iter_start = time.perf_counter()
                result = extract_response_from_result(
                    response,
                    f"concurrent query {batch_id}-{i}",
                    consciousness_context
                )
                iter_end = time.perf_counter()
                times.append(iter_end - iter_start)
            batch_end = time.perf_counter()
            
            return batch_end - batch_start, times
        
        results = {}
        thread_counts = [1, 2, 4, 8, 16]
        batch_size = 1000
        
        for num_threads in thread_counts:
            print(f"  Testing with {num_threads} threads...")
            
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024
            start_time = time.perf_counter()
            
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = []
                for thread_id in range(num_threads):
                    future = executor.submit(process_batch, thread_id, batch_size)
                    futures.append(future)
                
                all_batch_times = []
                all_individual_times = []
                
                for future in futures:
                    batch_time, individual_times = future.result()
                    all_batch_times.append(batch_time)
                    all_individual_times.extend(individual_times)
            
            end_time = time.perf_counter()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            total_time = end_time - start_time
            total_operations = num_threads * batch_size
            memory_increase = end_memory - start_memory
            
            results[f'{num_threads}_threads'] = {
                'num_threads': num_threads,
                'total_operations': total_operations,
                'total_time_seconds': total_time,
                'throughput_per_second': total_operations / total_time,
                'avg_batch_time_seconds': statistics.mean(all_batch_times),
                'avg_operation_time_microseconds': statistics.mean(all_individual_times) * 1_000_000,
                'memory_increase_mb': memory_increase,
                'scalability_efficiency': (total_operations / total_time) / (batch_size / statistics.mean(all_batch_times)) if all_batch_times else 0
            }
        
        return results
    
    def benchmark_memory_efficiency(self) -> Dict[str, Any]:
        """Benchmark memory efficiency over time"""
        print("Benchmarking memory efficiency...")
        
        consciousness_context = {
            "consciousness_level": 0.7,
            "emotional_state": "curious",
            "user_id": "benchmark_user"
        }
        
        # Force garbage collection
        gc.collect()
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        memory_samples = [initial_memory]
        operation_counts = [0]
        
        # Process responses in batches and track memory
        batch_size = 1000
        num_batches = 20
        
        for batch in range(num_batches):
            # Create varied responses for this batch
            responses = []
            for i in range(batch_size):
                if i % 4 == 0:
                    responses.append({
                        "response": f"Throttled response {batch}-{i}",
                        "status": "throttled"
                    })
                elif i % 4 == 1:
                    responses.append(f"String response {batch}-{i}")
                elif i % 4 == 2:
                    responses.append({"response": f"Dict response {batch}-{i}"})
                else:
                    responses.append({
                        "response": f"Complex response {batch}-{i}",
                        "metadata": {"batch": batch, "index": i},
                        "large_data": "x" * 1000
                    })
            
            # Process the batch
            for i, response in enumerate(responses):
                result = extract_response_from_result(
                    response,
                    f"memory test {batch}-{i}",
                    consciousness_context
                )
            
            # Sample memory after each batch
            current_memory = psutil.Process().memory_info().rss / 1024 / 1024
            memory_samples.append(current_memory)
            operation_counts.append((batch + 1) * batch_size)
            
            # Force garbage collection every few batches
            if batch % 5 == 0:
                gc.collect()
        
        # Calculate memory efficiency metrics
        final_memory = memory_samples[-1]
        total_operations = num_batches * batch_size
        memory_increase = final_memory - initial_memory
        
        # Calculate memory growth rate
        if len(memory_samples) > 2:
            memory_growth_rate = (memory_samples[-1] - memory_samples[1]) / (len(memory_samples) - 2)
        else:
            memory_growth_rate = 0
        
        # Calculate memory stability (standard deviation)
        memory_stability = statistics.stdev(memory_samples) if len(memory_samples) > 1 else 0
        
        return {
            'total_operations': total_operations,
            'initial_memory_mb': initial_memory,
            'final_memory_mb': final_memory,
            'memory_increase_mb': memory_increase,
            'memory_per_operation_bytes': (memory_increase * 1024 * 1024) / total_operations if total_operations > 0 else 0,
            'memory_growth_rate_mb_per_batch': memory_growth_rate,
            'memory_stability_std_dev': memory_stability,
            'memory_samples': memory_samples,
            'operation_counts': operation_counts
        }
    
    def benchmark_throttling_scenarios(self) -> Dict[str, Any]:
        """Benchmark different throttling scenarios"""
        print("Benchmarking throttling scenarios...")
        
        consciousness_context = {
            "consciousness_level": 0.7,
            "emotional_state": "curious",
            "user_id": "benchmark_user"
        }
        
        scenarios = {
            'no_throttling': 0.0,
            'light_throttling': 0.1,
            'moderate_throttling': 0.3,
            'heavy_throttling': 0.5,
            'extreme_throttling': 0.8
        }
        
        results = {}
        num_operations = 5000
        
        for scenario_name, throttling_rate in scenarios.items():
            print(f"  Testing {scenario_name} (rate: {throttling_rate})...")
            
            times = []
            throttled_count = 0
            normal_count = 0
            
            start_time = time.perf_counter()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            for i in range(num_operations):
                # Simulate throttling based on rate
                import random
                if random.random() < throttling_rate:
                    response = {
                        "response": f"Throttled response {i}",
                        "status": "throttled"
                    }
                    throttled_count += 1
                else:
                    response = f"Normal response {i}"
                    normal_count += 1
                
                iter_start = time.perf_counter()
                result = extract_response_from_result(
                    response,
                    f"throttling test {i}",
                    consciousness_context
                )
                iter_end = time.perf_counter()
                times.append(iter_end - iter_start)
            
            end_time = time.perf_counter()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            total_time = end_time - start_time
            memory_increase = end_memory - start_memory
            
            results[scenario_name] = {
                'throttling_rate': throttling_rate,
                'total_operations': num_operations,
                'throttled_responses': throttled_count,
                'normal_responses': normal_count,
                'actual_throttling_rate': throttled_count / num_operations,
                'total_time_seconds': total_time,
                'throughput_per_second': num_operations / total_time,
                'avg_time_microseconds': statistics.mean(times) * 1_000_000,
                'memory_increase_mb': memory_increase,
                'performance_impact_percent': 0  # Will be calculated relative to no_throttling
            }
        
        # Calculate performance impact relative to no throttling
        baseline_throughput = results['no_throttling']['throughput_per_second']
        for scenario_name in results:
            if scenario_name != 'no_throttling':
                scenario_throughput = results[scenario_name]['throughput_per_second']
                impact = ((baseline_throughput - scenario_throughput) / baseline_throughput) * 100
                results[scenario_name]['performance_impact_percent'] = impact
        
        return results
    
    def run_all_benchmarks(self) -> Dict[str, Any]:
        """Run all benchmarks and return comprehensive results"""
        print("Starting comprehensive performance benchmarks...")
        print("=" * 60)
        
        self.results['benchmarks']['throughput'] = self.benchmark_response_processing_throughput()
        self.results['benchmarks']['concurrent'] = self.benchmark_concurrent_processing()
        self.results['benchmarks']['memory'] = self.benchmark_memory_efficiency()
        self.results['benchmarks']['throttling'] = self.benchmark_throttling_scenarios()
        
        return self.results
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate a comprehensive performance report"""
        report = []
        report.append("THROTTLING RESPONSE PROCESSING - PERFORMANCE BENCHMARK REPORT")
        report.append("=" * 70)
        report.append(f"Timestamp: {results['timestamp']}")
        report.append(f"System: {results['system_info']['cpu_count']} CPUs, "
                     f"{results['system_info']['memory_total_gb']:.1f}GB RAM")
        report.append("")
        
        # Throughput Results
        report.append("1. RESPONSE PROCESSING THROUGHPUT")
        report.append("-" * 40)
        throughput = results['benchmarks']['throughput']
        for response_type, metrics in throughput.items():
            report.append(f"{response_type.upper()}:")
            report.append(f"  Throughput: {metrics['throughput_per_second']:,.0f} ops/sec")
            report.append(f"  Avg Time: {metrics['avg_time_microseconds']:.1f} μs")
            report.append(f"  Memory/Op: {metrics['memory_per_operation_bytes']:.1f} bytes")
            report.append("")
        
        # Concurrent Processing Results
        report.append("2. CONCURRENT PROCESSING SCALABILITY")
        report.append("-" * 40)
        concurrent = results['benchmarks']['concurrent']
        for thread_config, metrics in concurrent.items():
            report.append(f"{metrics['num_threads']} THREADS:")
            report.append(f"  Throughput: {metrics['throughput_per_second']:,.0f} ops/sec")
            report.append(f"  Efficiency: {metrics['scalability_efficiency']:.2f}")
            report.append(f"  Memory: {metrics['memory_increase_mb']:.1f} MB")
            report.append("")
        
        # Memory Efficiency Results
        report.append("3. MEMORY EFFICIENCY")
        report.append("-" * 40)
        memory = results['benchmarks']['memory']
        report.append(f"Total Operations: {memory['total_operations']:,}")
        report.append(f"Memory Increase: {memory['memory_increase_mb']:.1f} MB")
        report.append(f"Memory/Operation: {memory['memory_per_operation_bytes']:.1f} bytes")
        report.append(f"Memory Stability: {memory['memory_stability_std_dev']:.2f} MB std dev")
        report.append("")
        
        # Throttling Scenarios Results
        report.append("4. THROTTLING SCENARIO PERFORMANCE")
        report.append("-" * 40)
        throttling = results['benchmarks']['throttling']
        for scenario, metrics in throttling.items():
            report.append(f"{scenario.upper()}:")
            report.append(f"  Throttling Rate: {metrics['throttling_rate']:.1%}")
            report.append(f"  Throughput: {metrics['throughput_per_second']:,.0f} ops/sec")
            report.append(f"  Performance Impact: {metrics['performance_impact_percent']:.1f}%")
            report.append("")
        
        # Performance Summary
        report.append("5. PERFORMANCE SUMMARY")
        report.append("-" * 40)
        
        # Best throughput
        best_throughput = max(throughput.values(), key=lambda x: x['throughput_per_second'])
        report.append(f"Best Throughput: {best_throughput['throughput_per_second']:,.0f} ops/sec")
        
        # Memory efficiency
        avg_memory_per_op = memory['memory_per_operation_bytes']
        report.append(f"Memory Efficiency: {avg_memory_per_op:.1f} bytes/operation")
        
        # Throttling impact
        heavy_throttling_impact = throttling['heavy_throttling']['performance_impact_percent']
        report.append(f"Heavy Throttling Impact: {heavy_throttling_impact:.1f}%")
        
        # Scalability
        single_thread_throughput = concurrent['1_threads']['throughput_per_second']
        multi_thread_throughput = max(concurrent.values(), key=lambda x: x['throughput_per_second'])['throughput_per_second']
        scalability_factor = multi_thread_throughput / single_thread_throughput
        report.append(f"Scalability Factor: {scalability_factor:.1f}x")
        
        report.append("")
        report.append("6. RECOMMENDATIONS")
        report.append("-" * 40)
        
        # Generate recommendations based on results
        if avg_memory_per_op > 100:
            report.append("• Consider optimizing memory usage - high per-operation overhead")
        
        if heavy_throttling_impact > 10:
            report.append("• Throttling has significant performance impact - consider optimization")
        
        if scalability_factor < 2:
            report.append("• Limited scalability - investigate threading bottlenecks")
        
        if memory['memory_stability_std_dev'] > 5:
            report.append("• Memory usage is unstable - check for memory leaks")
        
        return "\n".join(report)
    
    def save_results(self, results: Dict[str, Any], filename: str = None):
        """Save benchmark results to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"throttling_performance_benchmark_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to: {filename}")


def main():
    """Run the performance benchmark"""
    benchmark = PerformanceBenchmark()
    
    try:
        results = benchmark.run_all_benchmarks()
        
        # Generate and display report
        report = benchmark.generate_report(results)
        print("\n" + report)
        
        # Save results
        benchmark.save_results(results)
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"throttling_performance_report_{timestamp}.txt"
        with open(report_filename, 'w') as f:
            f.write(report)
        print(f"Report saved to: {report_filename}")
        
    except Exception as e:
        print(f"Benchmark failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()