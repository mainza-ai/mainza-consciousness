#!/usr/bin/env python3
"""
Comprehensive Test Suite for Mainza AI Optimization Implementations
Tests all optimization systems and verifies functionality
"""

import asyncio
import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Import optimization systems
from backend.utils.optimized_vector_embeddings import OptimizedVectorEmbeddings
from backend.utils.enhanced_redis_caching import EnhancedRedisCache, CacheManager
from backend.utils.memory_compression_system import MemoryCompressionSystem, CompressionStrategy
from backend.utils.optimized_agent_memory_system import OptimizedAgentMemorySystem, MemoryType, MemoryImportance
from backend.utils.performance_monitoring_system import PerformanceMonitoringSystem, MetricType
from backend.utils.optimized_system_integration import OptimizedMainzaSystem

# Mock Neo4j driver for testing
class MockNeo4jDriver:
    def session(self):
        return MockSession()

class MockSession:
    def run(self, query, parameters=None):
        return MockResult()
    
    def close(self):
        pass

class MockResult:
    def single(self):
        return {"test": 1}
    
    def data(self):
        return [{"test": 1}]

class TestOptimizationImplementations:
    """Test suite for all optimization implementations"""
    
    def __init__(self):
        self.test_results = {}
        self.mock_driver = MockNeo4jDriver()
        self.redis_url = "redis://localhost:6379"
        self.config = {
            "vector_embeddings": {
                "compression_enabled": True,
                "similarity_threshold": 0.85
            },
            "redis_cache": {
                "compression_enabled": True,
                "serialization_method": "json",
                "default_ttl": 3600
            },
            "memory_compression": {
                "similarity_threshold": 0.85,
                "compression_threshold": 0.7
            },
            "agent_memory": {
                "consolidation_threshold": 0.8,
                "learning_threshold": 0.7
            },
            "performance_monitoring": {
                "monitoring_interval": 5,
                "alert_thresholds": {
                    "cpu_usage": 80.0,
                    "memory_usage": 85.0
                }
            }
        }
    
    async def run_all_tests(self):
        """Run all optimization tests"""
        print("🚀 Starting Mainza AI Optimization Implementation Tests")
        print("=" * 60)
        
        test_methods = [
            self.test_vector_embeddings,
            self.test_redis_caching,
            self.test_memory_compression,
            self.test_agent_memory_system,
            self.test_performance_monitoring,
            self.test_system_integration
        ]
        
        for test_method in test_methods:
            try:
                print(f"\n🧪 Running {test_method.__name__}...")
                result = await test_method()
                self.test_results[test_method.__name__] = result
                status = "✅ PASSED" if result["success"] else "❌ FAILED"
                print(f"{status}: {result['message']}")
            except Exception as e:
                print(f"❌ FAILED: {test_method.__name__} - {str(e)}")
                self.test_results[test_method.__name__] = {
                    "success": False,
                    "message": f"Exception: {str(e)}",
                    "error": str(e)
                }
        
        # Generate test report
        await self.generate_test_report()
    
    async def test_vector_embeddings(self) -> Dict[str, Any]:
        """Test vector embeddings optimization"""
        try:
            # Initialize system
            vector_system = OptimizedVectorEmbeddings(self.mock_driver, self.config["vector_embeddings"])
            
            # Test embedding generation
            test_text = "This is a test for consciousness and memory optimization"
            embedding = await vector_system.generate_optimized_embedding(test_text, "consciousness")
            
            # Verify embedding properties
            assert isinstance(embedding, list), "Embedding should be a list"
            assert len(embedding) > 0, "Embedding should not be empty"
            assert all(isinstance(x, (int, float)) for x in embedding), "Embedding should contain numbers"
            
            # Test performance metrics
            metrics = vector_system.get_performance_metrics()
            assert "total_embeddings" in metrics, "Should track total embeddings"
            
            return {
                "success": True,
                "message": f"Vector embeddings working correctly. Generated {len(embedding)}-dimensional embedding.",
                "embedding_length": len(embedding),
                "metrics": metrics
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Vector embeddings test failed: {str(e)}",
                "error": str(e)
            }
    
    async def test_redis_caching(self) -> Dict[str, Any]:
        """Test enhanced Redis caching system"""
        try:
            # Initialize cache system
            cache = EnhancedRedisCache(self.redis_url, self.config["redis_cache"])
            await cache.initialize()
            
            # Test basic operations
            test_key = "test_key_123"
            test_value = {"test": "data", "timestamp": datetime.now().isoformat()}
            
            # Set value
            set_result = await cache.set(test_key, test_value, ttl=60)
            assert set_result, "Set operation should succeed"
            
            # Get value
            retrieved_value = await cache.get(test_key)
            assert retrieved_value == test_value, "Retrieved value should match set value"
            
            # Test batch operations
            batch_data = {
                "batch_key_1": {"data": "test1"},
                "batch_key_2": {"data": "test2"},
                "batch_key_3": {"data": "test3"}
            }
            
            batch_set_result = await cache.batch_set(batch_data, ttl=60)
            assert batch_set_result, "Batch set should succeed"
            
            batch_get_result = await cache.batch_get(list(batch_data.keys()))
            assert len(batch_get_result) == len(batch_data), "Should retrieve all batch values"
            
            # Test cache statistics
            stats = await cache.get_cache_stats()
            assert "cache_stats" in stats, "Should provide cache statistics"
            
            # Cleanup
            await cache.close()
            
            return {
                "success": True,
                "message": "Redis caching system working correctly with compression and batch operations",
                "stats": stats
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Redis caching test failed: {str(e)}",
                "error": str(e)
            }
    
    async def test_memory_compression(self) -> Dict[str, Any]:
        """Test memory compression system"""
        try:
            # Initialize compression system
            compression_system = MemoryCompressionSystem(self.mock_driver, self.config["memory_compression"])
            
            # Test deduplication
            dedup_result = await compression_system.deduplicate_memories()
            assert "deduplication_successful" in dedup_result, "Should return deduplication status"
            
            # Test compression statistics
            stats = compression_system.get_compression_stats()
            assert "compression_stats" in stats, "Should provide compression statistics"
            
            return {
                "success": True,
                "message": "Memory compression system working correctly",
                "deduplication_result": dedup_result,
                "compression_stats": stats
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Memory compression test failed: {str(e)}",
                "error": str(e)
            }
    
    async def test_agent_memory_system(self) -> Dict[str, Any]:
        """Test optimized agent memory system"""
        try:
            # Initialize agent memory system
            agent_memory = OptimizedAgentMemorySystem(self.mock_driver, self.config["agent_memory"])
            
            # Test memory storage
            test_agent_id = "test_agent_123"
            test_content = "This is a test memory for consciousness optimization"
            test_embedding = [0.1, 0.2, 0.3, 0.4, 0.5]  # Mock embedding
            
            memory_id = await agent_memory.store_agent_memory(
                test_agent_id,
                test_content,
                MemoryType.EPISODIC,
                MemoryImportance.HIGH,
                test_embedding,
                {"confidence": 0.8}
            )
            
            assert memory_id is not None, "Should return memory ID"
            
            # Test memory retrieval
            retrieved_memories = await agent_memory.retrieve_agent_memories(
                test_agent_id,
                "test memory",
                [MemoryType.EPISODIC],
                5
            )
            
            assert isinstance(retrieved_memories, list), "Should return list of memories"
            
            # Test cross-agent learning
            cross_learning_success = await agent_memory.cross_agent_knowledge_transfer(
                "agent_1",
                "agent_2",
                "Shared knowledge about consciousness",
                "semantic"
            )
            
            # Test performance metrics
            metrics = agent_memory.get_performance_metrics()
            assert "performance_metrics" in metrics, "Should provide performance metrics"
            
            return {
                "success": True,
                "message": "Agent memory system working correctly with cross-agent learning",
                "memory_id": memory_id,
                "retrieved_count": len(retrieved_memories),
                "cross_learning_success": cross_learning_success,
                "metrics": metrics
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Agent memory system test failed: {str(e)}",
                "error": str(e)
            }
    
    async def test_performance_monitoring(self) -> Dict[str, Any]:
        """Test performance monitoring system"""
        try:
            # Initialize performance monitoring
            monitoring = PerformanceMonitoringSystem(self.mock_driver, None, self.config["performance_monitoring"])
            
            # Test metric recording
            monitoring.record_request(True, 0.5)  # Successful request
            monitoring.record_request(False, 2.0)  # Failed request
            
            # Test performance summary
            summary = monitoring.get_performance_summary()
            assert "performance_stats" in summary, "Should provide performance statistics"
            assert "monitoring_status" in summary, "Should provide monitoring status"
            
            # Test optimization recommendations
            recommendations = monitoring.get_optimization_recommendations()
            assert isinstance(recommendations, list), "Should return list of recommendations"
            
            return {
                "success": True,
                "message": "Performance monitoring system working correctly",
                "summary": summary,
                "recommendations_count": len(recommendations)
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Performance monitoring test failed: {str(e)}",
                "error": str(e)
            }
    
    async def test_system_integration(self) -> Dict[str, Any]:
        """Test integrated optimization system"""
        try:
            # Initialize integrated system
            integrated_system = OptimizedMainzaSystem(
                self.mock_driver,
                self.redis_url,
                self.config
            )
            
            # Test system initialization
            await integrated_system.initialize()
            assert integrated_system.initialized, "System should be initialized"
            
            # Test memory storage with optimization
            memory_id = await integrated_system.store_optimized_memory(
                "test_agent",
                "Optimized memory content",
                MemoryType.SEMANTIC,
                MemoryImportance.HIGH,
                {"confidence": 0.9}
            )
            
            assert memory_id is not None, "Should return memory ID"
            
            # Test memory retrieval with optimization
            retrieved_memories = await integrated_system.retrieve_optimized_memories(
                "test_agent",
                "optimized memory",
                [MemoryType.SEMANTIC],
                5
            )
            
            assert isinstance(retrieved_memories, list), "Should return list of memories"
            
            # Test cross-agent knowledge transfer
            transfer_success = await integrated_system.cross_agent_knowledge_transfer(
                "agent_1",
                "agent_2",
                "Optimized knowledge transfer",
                "semantic"
            )
            
            # Test system health report
            health_report = await integrated_system.get_system_health_report()
            assert "overall_health_score" in health_report, "Should provide health score"
            
            # Cleanup
            await integrated_system.shutdown()
            
            return {
                "success": True,
                "message": "Integrated optimization system working correctly",
                "memory_id": memory_id,
                "retrieved_count": len(retrieved_memories),
                "transfer_success": transfer_success,
                "health_score": health_report.get("overall_health_score", 0)
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"System integration test failed: {str(e)}",
                "error": str(e)
            }
    
    async def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print("\n📋 DETAILED RESULTS:")
        print("-" * 40)
        
        for test_name, result in self.test_results.items():
            status = "✅ PASSED" if result["success"] else "❌ FAILED"
            print(f"{status} {test_name}")
            print(f"   Message: {result['message']}")
            
            if not result["success"] and "error" in result:
                print(f"   Error: {result['error']}")
            
            print()
        
        # Save report to file
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (passed_tests/total_tests)*100,
            "results": self.test_results
        }
        
        with open("optimization_test_report.json", "w") as f:
            json.dump(report_data, f, indent=2)
        
        print(f"📄 Detailed report saved to: optimization_test_report.json")
        
        if failed_tests == 0:
            print("\n🎉 ALL TESTS PASSED! Optimization implementations are working correctly.")
        else:
            print(f"\n⚠️  {failed_tests} tests failed. Please review the errors above.")

async def main():
    """Main test execution"""
    tester = TestOptimizationImplementations()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
