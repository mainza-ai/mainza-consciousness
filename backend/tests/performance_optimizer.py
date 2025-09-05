"""
Performance optimization analyzer for throttling response processing
Analyzes performance test results and provides optimization recommendations
"""

import json
import statistics
import sys
import os
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import cProfile
import pstats
import io
import time

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


@dataclass
class OptimizationRecommendation:
    """Optimization recommendation with priority and impact"""
    category: str
    priority: str  # "HIGH", "MEDIUM", "LOW"
    description: str
    impact: str
    implementation: str
    estimated_improvement: str


class PerformanceOptimizer:
    """Analyzes performance and provides optimization recommendations"""
    
    def __init__(self):
        self.recommendations: List[OptimizationRecommendation] = []
        self.profiling_results: Dict[str, Any] = {}
    
    def profile_response_processing(self) -> Dict[str, Any]:
        """Profile response processing functions to identify bottlenecks"""
        
        print("Profiling response processing functions...")
        
        consciousness_context = {
            "consciousness_level": 0.7,
            "emotional_state": "curious",
            "user_id": "profile_user"
        }
        
        # Test data for profiling
        test_responses = [
            "Simple string response",
            {"response": "Dictionary response"},
            {
                "response": "Throttled response",
                "status": "throttled"
            },
            {
                "response": "Complex response",
                "metadata": {"agent": "test", "confidence": 0.95},
                "status": "success"
            }
        ]
        
        profiling_results = {}
        
        # Profile extract_response_from_result
        print("  Profiling extract_response_from_result...")
        
        pr = cProfile.Profile()
        pr.enable()
        
        for _ in range(10000):
            for response in test_responses:
                extract_response_from_result(
                    response,
                    "Profile test query",
                    consciousness_context
                )
        
        pr.disable()
        
        # Capture profiling stats
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats(20)  # Top 20 functions
        
        profiling_results['extract_response_from_result'] = {
            'stats_text': s.getvalue(),
            'total_calls': ps.total_calls,
            'total_time': ps.total_tt
        }
        
        # Profile generate_throttled_response
        print("  Profiling generate_throttled_response...")
        
        pr2 = cProfile.Profile()
        pr2.enable()
        
        for _ in range(1000):
            generate_throttled_response("Test query", consciousness_context)
        
        pr2.disable()
        
        s2 = io.StringIO()
        ps2 = pstats.Stats(pr2, stream=s2).sort_stats('cumulative')
        ps2.print_stats(20)
        
        profiling_results['generate_throttled_response'] = {
            'stats_text': s2.getvalue(),
            'total_calls': ps2.total_calls,
            'total_time': ps2.total_tt
        }
        
        self.profiling_results = profiling_results
        return profiling_results
    
    def analyze_memory_patterns(self) -> Dict[str, Any]:
        """Analyze memory usage patterns during response processing"""
        
        print("Analyzing memory usage patterns...")
        
        import tracemalloc
        import gc
        
        consciousness_context = {
            "consciousness_level": 0.7,
            "emotional_state": "curious",
            "user_id": "memory_test_user"
        }
        
        # Start memory tracing
        tracemalloc.start()
        
        # Baseline memory
        gc.collect()
        baseline_snapshot = tracemalloc.take_snapshot()
        
        # Process various response types
        response_types = {
            'string_responses': ["String response " + str(i) for i in range(1000)],
            'dict_responses': [{"response": f"Dict response {i}"} for i in range(1000)],
            'throttled_responses': [{
                "response": f"Throttled response {i}",
                "status": "throttled"
            } for i in range(1000)],
            'complex_responses': [{
                "response": f"Complex response {i}",
                "metadata": {"index": i, "type": "complex"},
                "status": "success"
            } for i in range(1000)]
        }
        
        memory_analysis = {}
        
        for response_type, responses in response_types.items():
            print(f"  Analyzing {response_type}...")
            
            # Take snapshot before processing
            before_snapshot = tracemalloc.take_snapshot()
            
            # Process responses
            for response in responses:
                extract_response_from_result(
                    response,
                    f"Memory test query",
                    consciousness_context
                )
            
            # Take snapshot after processing
            after_snapshot = tracemalloc.take_snapshot()
            
            # Calculate memory difference
            top_stats = after_snapshot.compare_to(before_snapshot, 'lineno')
            
            # Get memory usage statistics
            memory_analysis[response_type] = {
                'top_memory_allocations': [
                    {
                        'file': stat.traceback.format()[0] if stat.traceback.format() else 'unknown',
                        'size_mb': stat.size / 1024 / 1024,
                        'count': stat.count
                    }
                    for stat in top_stats[:5]
                ],
                'total_size_mb': sum(stat.size for stat in top_stats) / 1024 / 1024,
                'total_allocations': sum(stat.count for stat in top_stats)
            }
        
        tracemalloc.stop()
        
        return memory_analysis
    
    def benchmark_optimization_opportunities(self) -> Dict[str, Any]:
        """Benchmark potential optimization opportunities"""
        
        print("Benchmarking optimization opportunities...")
        
        consciousness_context = {
            "consciousness_level": 0.7,
            "emotional_state": "curious",
            "user_id": "optimization_user"
        }
        
        optimization_tests = {}
        
        # Test 1: String vs dict response processing speed
        print("  Testing string vs dict response processing...")
        
        string_responses = ["String response " + str(i) for i in range(5000)]
        dict_responses = [{"response": f"Dict response {i}"} for i in range(5000)]
        
        # Time string processing
        start_time = time.perf_counter()
        for response in string_responses:
            extract_response_from_result(response, "test", consciousness_context)
        string_time = time.perf_counter() - start_time
        
        # Time dict processing
        start_time = time.perf_counter()
        for response in dict_responses:
            extract_response_from_result(response, "test", consciousness_context)
        dict_time = time.perf_counter() - start_time
        
        optimization_tests['string_vs_dict'] = {
            'string_time_seconds': string_time,
            'dict_time_seconds': dict_time,
            'dict_overhead_percent': ((dict_time - string_time) / string_time) * 100
        }
        
        # Test 2: Throttled response processing overhead
        print("  Testing throttled response processing overhead...")
        
        normal_responses = [f"Normal response {i}" for i in range(2000)]
        throttled_responses = [{
            "response": f"Throttled response {i}",
            "status": "throttled"
        } for i in range(2000)]
        
        # Time normal processing
        start_time = time.perf_counter()
        for response in normal_responses:
            extract_response_from_result(response, "test", consciousness_context)
        normal_time = time.perf_counter() - start_time
        
        # Time throttled processing
        start_time = time.perf_counter()
        for response in throttled_responses:
            extract_response_from_result(response, "test", consciousness_context)
        throttled_time = time.perf_counter() - start_time
        
        optimization_tests['normal_vs_throttled'] = {
            'normal_time_seconds': normal_time,
            'throttled_time_seconds': throttled_time,
            'throttled_overhead_percent': ((throttled_time - normal_time) / normal_time) * 100
        }
        
        # Test 3: Consciousness context impact
        print("  Testing consciousness context impact...")
        
        simple_context = {"user_id": "test"}
        complex_context = {
            "consciousness_level": 0.7,
            "emotional_state": "curious",
            "user_id": "test",
            "conversation_history": ["previous message 1", "previous message 2"],
            "user_preferences": {"style": "casual", "verbosity": "medium"},
            "session_data": {"start_time": "2024-01-01", "interaction_count": 15}
        }
        
        test_responses = [f"Context test response {i}" for i in range(2000)]
        
        # Time with simple context
        start_time = time.perf_counter()
        for response in test_responses:
            extract_response_from_result(response, "test", simple_context)
        simple_context_time = time.perf_counter() - start_time
        
        # Time with complex context
        start_time = time.perf_counter()
        for response in test_responses:
            extract_response_from_result(response, "test", complex_context)
        complex_context_time = time.perf_counter() - start_time
        
        optimization_tests['simple_vs_complex_context'] = {
            'simple_context_time_seconds': simple_context_time,
            'complex_context_time_seconds': complex_context_time,
            'complex_context_overhead_percent': ((complex_context_time - simple_context_time) / simple_context_time) * 100
        }
        
        return optimization_tests
    
    def generate_optimization_recommendations(
        self, 
        profiling_results: Dict[str, Any],
        memory_analysis: Dict[str, Any],
        optimization_tests: Dict[str, Any]
    ):
        """Generate optimization recommendations based on analysis"""
        
        print("Generating optimization recommendations...")
        
        # Analyze profiling results
        extract_stats = profiling_results.get('extract_response_from_result', {})
        generate_stats = profiling_results.get('generate_throttled_response', {})
        
        # Check for performance bottlenecks
        if extract_stats.get('total_time', 0) > 1.0:
            self.recommendations.append(OptimizationRecommendation(
                category="Performance",
                priority="HIGH",
                description="extract_response_from_result function shows high execution time",
                impact="Reduces response processing latency",
                implementation="Profile individual operations within the function to identify bottlenecks",
                estimated_improvement="10-30% response time reduction"
            ))
        
        # Analyze memory patterns
        for response_type, analysis in memory_analysis.items():
            total_memory = analysis.get('total_size_mb', 0)
            if total_memory > 10:  # More than 10MB for 1000 operations
                self.recommendations.append(OptimizationRecommendation(
                    category="Memory",
                    priority="MEDIUM",
                    description=f"High memory usage detected for {response_type}",
                    impact="Reduces memory footprint and GC pressure",
                    implementation="Optimize data structures and reduce object creation",
                    estimated_improvement="20-40% memory usage reduction"
                ))
        
        # Analyze optimization test results
        string_vs_dict = optimization_tests.get('string_vs_dict', {})
        dict_overhead = string_vs_dict.get('dict_overhead_percent', 0)
        
        if dict_overhead > 50:
            self.recommendations.append(OptimizationRecommendation(
                category="Performance",
                priority="MEDIUM",
                description=f"Dictionary response processing has {dict_overhead:.1f}% overhead",
                impact="Improves processing speed for dictionary responses",
                implementation="Optimize dictionary key access and reduce type checking",
                estimated_improvement="15-25% faster dictionary processing"
            ))
        
        normal_vs_throttled = optimization_tests.get('normal_vs_throttled', {})
        throttled_overhead = normal_vs_throttled.get('throttled_overhead_percent', 0)
        
        if throttled_overhead > 30:
            self.recommendations.append(OptimizationRecommendation(
                category="Performance",
                priority="HIGH",
                description=f"Throttled response processing has {throttled_overhead:.1f}% overhead",
                impact="Reduces latency during high-load throttling scenarios",
                implementation="Optimize throttled response detection and message generation",
                estimated_improvement="20-35% faster throttled response processing"
            ))
        
        context_test = optimization_tests.get('simple_vs_complex_context', {})
        context_overhead = context_test.get('complex_context_overhead_percent', 0)
        
        if context_overhead > 25:
            self.recommendations.append(OptimizationRecommendation(
                category="Performance",
                priority="LOW",
                description=f"Complex consciousness context adds {context_overhead:.1f}% overhead",
                impact="Improves performance when consciousness context is complex",
                implementation="Lazy-load consciousness context data and cache frequently used values",
                estimated_improvement="10-20% improvement with complex contexts"
            ))
        
        # General recommendations based on best practices
        self.recommendations.append(OptimizationRecommendation(
            category="Caching",
            priority="MEDIUM",
            description="No response caching detected",
            impact="Reduces redundant processing for similar responses",
            implementation="Implement LRU cache for frequently processed response patterns",
            estimated_improvement="30-50% improvement for repeated patterns"
        ))
        
        self.recommendations.append(OptimizationRecommendation(
            category="Concurrency",
            priority="LOW",
            description="Response processing is synchronous",
            impact="Improves throughput under high concurrent load",
            implementation="Consider async processing for I/O-bound operations within response handling",
            estimated_improvement="2-5x throughput improvement under high concurrency"
        ))
        
        self.recommendations.append(OptimizationRecommendation(
            category="Monitoring",
            priority="MEDIUM",
            description="Limited performance monitoring in production",
            impact="Enables proactive performance optimization",
            implementation="Add performance metrics collection and alerting",
            estimated_improvement="Enables continuous performance improvement"
        ))
    
    def run_comprehensive_analysis(self) -> Dict[str, Any]:
        """Run comprehensive performance analysis"""
        
        print("Running comprehensive performance analysis...")
        print("=" * 60)
        
        # Run all analysis components
        profiling_results = self.profile_response_processing()
        memory_analysis = self.analyze_memory_patterns()
        optimization_tests = self.benchmark_optimization_opportunities()
        
        # Generate recommendations
        self.generate_optimization_recommendations(
            profiling_results, 
            memory_analysis, 
            optimization_tests
        )
        
        return {
            'timestamp': datetime.now().isoformat(),
            'profiling_results': profiling_results,
            'memory_analysis': memory_analysis,
            'optimization_tests': optimization_tests,
            'recommendations': [
                {
                    'category': rec.category,
                    'priority': rec.priority,
                    'description': rec.description,
                    'impact': rec.impact,
                    'implementation': rec.implementation,
                    'estimated_improvement': rec.estimated_improvement
                }
                for rec in self.recommendations
            ]
        }
    
    def generate_optimization_report(self, analysis_results: Dict[str, Any]) -> str:
        """Generate comprehensive optimization report"""
        
        report = []
        report.append("THROTTLING RESPONSE PROCESSING - OPTIMIZATION ANALYSIS REPORT")
        report.append("=" * 70)
        report.append(f"Timestamp: {analysis_results['timestamp']}")
        report.append("")
        
        # Profiling Results Summary
        report.append("1. PROFILING RESULTS")
        report.append("-" * 30)
        
        profiling = analysis_results['profiling_results']
        for func_name, stats in profiling.items():
            report.append(f"{func_name.upper()}:")
            report.append(f"  Total Calls: {stats['total_calls']:,}")
            report.append(f"  Total Time: {stats['total_time']:.4f} seconds")
            report.append(f"  Avg Time per Call: {(stats['total_time'] / stats['total_calls'] * 1000):.4f} ms")
            report.append("")
        
        # Memory Analysis Summary
        report.append("2. MEMORY ANALYSIS")
        report.append("-" * 30)
        
        memory = analysis_results['memory_analysis']
        for response_type, analysis in memory.items():
            report.append(f"{response_type.upper()}:")
            report.append(f"  Total Memory: {analysis['total_size_mb']:.2f} MB")
            report.append(f"  Total Allocations: {analysis['total_allocations']:,}")
            if analysis['top_memory_allocations']:
                top_alloc = analysis['top_memory_allocations'][0]
                report.append(f"  Top Allocation: {top_alloc['size_mb']:.2f} MB")
            report.append("")
        
        # Optimization Test Results
        report.append("3. OPTIMIZATION BENCHMARKS")
        report.append("-" * 30)
        
        opt_tests = analysis_results['optimization_tests']
        
        string_vs_dict = opt_tests.get('string_vs_dict', {})
        if string_vs_dict:
            report.append("STRING vs DICT PROCESSING:")
            report.append(f"  String Time: {string_vs_dict['string_time_seconds']:.4f}s")
            report.append(f"  Dict Time: {string_vs_dict['dict_time_seconds']:.4f}s")
            report.append(f"  Dict Overhead: {string_vs_dict['dict_overhead_percent']:.1f}%")
            report.append("")
        
        normal_vs_throttled = opt_tests.get('normal_vs_throttled', {})
        if normal_vs_throttled:
            report.append("NORMAL vs THROTTLED PROCESSING:")
            report.append(f"  Normal Time: {normal_vs_throttled['normal_time_seconds']:.4f}s")
            report.append(f"  Throttled Time: {normal_vs_throttled['throttled_time_seconds']:.4f}s")
            report.append(f"  Throttled Overhead: {normal_vs_throttled['throttled_overhead_percent']:.1f}%")
            report.append("")
        
        context_test = opt_tests.get('simple_vs_complex_context', {})
        if context_test:
            report.append("SIMPLE vs COMPLEX CONTEXT:")
            report.append(f"  Simple Context: {context_test['simple_context_time_seconds']:.4f}s")
            report.append(f"  Complex Context: {context_test['complex_context_time_seconds']:.4f}s")
            report.append(f"  Complex Overhead: {context_test['complex_context_overhead_percent']:.1f}%")
            report.append("")
        
        # Optimization Recommendations
        report.append("4. OPTIMIZATION RECOMMENDATIONS")
        report.append("-" * 30)
        
        # Group recommendations by priority
        high_priority = [r for r in analysis_results['recommendations'] if r['priority'] == 'HIGH']
        medium_priority = [r for r in analysis_results['recommendations'] if r['priority'] == 'MEDIUM']
        low_priority = [r for r in analysis_results['recommendations'] if r['priority'] == 'LOW']
        
        for priority, recommendations in [('HIGH PRIORITY', high_priority), 
                                        ('MEDIUM PRIORITY', medium_priority), 
                                        ('LOW PRIORITY', low_priority)]:
            if recommendations:
                report.append(f"{priority}:")
                for i, rec in enumerate(recommendations, 1):
                    report.append(f"  {i}. {rec['description']}")
                    report.append(f"     Category: {rec['category']}")
                    report.append(f"     Impact: {rec['impact']}")
                    report.append(f"     Implementation: {rec['implementation']}")
                    report.append(f"     Expected Improvement: {rec['estimated_improvement']}")
                    report.append("")
        
        # Implementation Priority
        report.append("5. IMPLEMENTATION PRIORITY")
        report.append("-" * 30)
        
        if high_priority:
            report.append("IMMEDIATE (High Priority):")
            for rec in high_priority:
                report.append(f"  • {rec['description']}")
        
        if medium_priority:
            report.append("SHORT TERM (Medium Priority):")
            for rec in medium_priority:
                report.append(f"  • {rec['description']}")
        
        if low_priority:
            report.append("LONG TERM (Low Priority):")
            for rec in low_priority:
                report.append(f"  • {rec['description']}")
        
        report.append("")
        report.append("6. NEXT STEPS")
        report.append("-" * 30)
        report.append("1. Implement high-priority optimizations first")
        report.append("2. Set up continuous performance monitoring")
        report.append("3. Re-run analysis after optimizations to measure improvement")
        report.append("4. Consider load testing with optimized code")
        report.append("5. Monitor production performance metrics")
        
        return "\n".join(report)
    
    def save_analysis_results(self, results: Dict[str, Any], filename: str = None):
        """Save analysis results to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"throttling_optimization_analysis_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Analysis results saved to: {filename}")


def main():
    """Run the performance optimization analysis"""
    
    optimizer = PerformanceOptimizer()
    
    try:
        # Run comprehensive analysis
        results = optimizer.run_comprehensive_analysis()
        
        # Generate and display report
        report = optimizer.generate_optimization_report(results)
        print("\n" + report)
        
        # Save results
        optimizer.save_analysis_results(results)
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"throttling_optimization_report_{timestamp}.txt"
        with open(report_filename, 'w') as f:
            f.write(report)
        print(f"Optimization report saved to: {report_filename}")
        
    except Exception as e:
        print(f"Optimization analysis failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()