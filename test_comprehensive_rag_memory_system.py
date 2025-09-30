#!/usr/bin/env python3
"""
Comprehensive Test for RAG Memory System Analysis Implementation
Tests all optimization systems in the Docker environment
"""

import asyncio
import json
import logging
import requests
import time
from datetime import datetime
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ComprehensiveRAGMemorySystemTest:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.test_results = {
            "timestamp": datetime.now().isoformat(),
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "detailed_results": []
        }
    
    async def run_all_tests(self):
        """Run all comprehensive tests for the RAG memory system"""
        logger.info("🚀 Starting Comprehensive RAG Memory System Test Suite")
        
        # Test 1: System Health Check
        await self.test_system_health()
        
        # Test 2: Optimization System Status
        await self.test_optimization_system_status()
        
        # Test 3: Memory System Functionality
        await self.test_memory_system_functionality()
        
        # Test 4: Vector Embeddings System
        await self.test_vector_embeddings_system()
        
        # Test 5: Redis Caching System
        await self.test_redis_caching_system()
        
        # Test 6: Performance Monitoring
        await self.test_performance_monitoring()
        
        # Test 7: Cross-Agent Learning
        await self.test_cross_agent_learning()
        
        # Test 8: Memory Compression
        await self.test_memory_compression()
        
        # Test 9: Agent Memory Optimization
        await self.test_agent_memory_optimization()
        
        # Test 10: End-to-End Integration
        await self.test_end_to_end_integration()
        
        # Generate final report
        self.generate_final_report()
    
    async def test_system_health(self):
        """Test 1: System Health Check"""
        logger.info("🔍 Test 1: System Health Check")
        try:
            response = requests.get(f"{self.base_url}/api/optimization/health", timeout=10)
            if response.status_code == 200:
                health_data = response.json()
                self.record_test_result("System Health Check", True, {
                    "status_code": response.status_code,
                    "health_data": health_data
                })
                logger.info("✅ System health check passed")
            else:
                self.record_test_result("System Health Check", False, {
                    "status_code": response.status_code,
                    "error": "Health check failed"
                })
                logger.error(f"❌ System health check failed: {response.status_code}")
        except Exception as e:
            self.record_test_result("System Health Check", False, {"error": str(e)})
            logger.error(f"❌ System health check error: {e}")
    
    async def test_optimization_system_status(self):
        """Test 2: Optimization System Status"""
        logger.info("🔍 Test 2: Optimization System Status")
        try:
            response = requests.get(f"{self.base_url}/api/optimization/status", timeout=10)
            if response.status_code == 200:
                status_data = response.json()
                self.record_test_result("Optimization System Status", True, {
                    "status_code": response.status_code,
                    "status_data": status_data
                })
                logger.info("✅ Optimization system status check passed")
            else:
                self.record_test_result("Optimization System Status", False, {
                    "status_code": response.status_code,
                    "error": "Status check failed"
                })
                logger.error(f"❌ Optimization system status check failed: {response.status_code}")
        except Exception as e:
            self.record_test_result("Optimization System Status", False, {"error": str(e)})
            logger.error(f"❌ Optimization system status check error: {e}")
    
    async def test_memory_system_functionality(self):
        """Test 3: Memory System Functionality"""
        logger.info("🔍 Test 3: Memory System Functionality")
        try:
            # Test memory storage
            memory_data = {
                "content": "Test memory content for RAG system",
                "agent_id": "test_agent",
                "context": {"test": True},
                "tags": ["test", "rag", "memory"]
            }
            
            response = requests.post(f"{self.base_url}/api/memory/store", json=memory_data, timeout=10)
            if response.status_code == 200:
                memory_result = response.json()
                self.record_test_result("Memory System Functionality", True, {
                    "status_code": response.status_code,
                    "memory_result": memory_result
                })
                logger.info("✅ Memory system functionality test passed")
            else:
                self.record_test_result("Memory System Functionality", False, {
                    "status_code": response.status_code,
                    "error": "Memory storage failed"
                })
                logger.error(f"❌ Memory system functionality test failed: {response.status_code}")
        except Exception as e:
            self.record_test_result("Memory System Functionality", False, {"error": str(e)})
            logger.error(f"❌ Memory system functionality test error: {e}")
    
    async def test_vector_embeddings_system(self):
        """Test 4: Vector Embeddings System"""
        logger.info("🔍 Test 4: Vector Embeddings System")
        try:
            # Test vector similarity search
            search_data = {
                "query": "test query for vector embeddings",
                "top_k": 5
            }
            
            response = requests.post(f"{self.base_url}/api/memory/search", json=search_data, timeout=10)
            if response.status_code == 200:
                search_result = response.json()
                self.record_test_result("Vector Embeddings System", True, {
                    "status_code": response.status_code,
                    "search_result": search_result
                })
                logger.info("✅ Vector embeddings system test passed")
            else:
                self.record_test_result("Vector Embeddings System", False, {
                    "status_code": response.status_code,
                    "error": "Vector search failed"
                })
                logger.error(f"❌ Vector embeddings system test failed: {response.status_code}")
        except Exception as e:
            self.record_test_result("Vector Embeddings System", False, {"error": str(e)})
            logger.error(f"❌ Vector embeddings system test error: {e}")
    
    async def test_redis_caching_system(self):
        """Test 5: Redis Caching System"""
        logger.info("🔍 Test 5: Redis Caching System")
        try:
            # Test cache metrics
            response = requests.get(f"{self.base_url}/api/performance/metrics", timeout=10)
            if response.status_code == 200:
                metrics_data = response.json()
                self.record_test_result("Redis Caching System", True, {
                    "status_code": response.status_code,
                    "metrics_data": metrics_data
                })
                logger.info("✅ Redis caching system test passed")
            else:
                self.record_test_result("Redis Caching System", False, {
                    "status_code": response.status_code,
                    "error": "Cache metrics failed"
                })
                logger.error(f"❌ Redis caching system test failed: {response.status_code}")
        except Exception as e:
            self.record_test_result("Redis Caching System", False, {"error": str(e)})
            logger.error(f"❌ Redis caching system test error: {e}")
    
    async def test_performance_monitoring(self):
        """Test 6: Performance Monitoring"""
        logger.info("🔍 Test 6: Performance Monitoring")
        try:
            # Test performance metrics endpoint
            response = requests.get(f"{self.base_url}/api/performance/metrics", timeout=10)
            if response.status_code == 200:
                performance_data = response.json()
                self.record_test_result("Performance Monitoring", True, {
                    "status_code": response.status_code,
                    "performance_data": performance_data
                })
                logger.info("✅ Performance monitoring test passed")
            else:
                self.record_test_result("Performance Monitoring", False, {
                    "status_code": response.status_code,
                    "error": "Performance metrics failed"
                })
                logger.error(f"❌ Performance monitoring test failed: {response.status_code}")
        except Exception as e:
            self.record_test_result("Performance Monitoring", False, {"error": str(e)})
            logger.error(f"❌ Performance monitoring test error: {e}")
    
    async def test_cross_agent_learning(self):
        """Test 7: Cross-Agent Learning"""
        logger.info("🔍 Test 7: Cross-Agent Learning")
        try:
            # Test cross-agent learning endpoint
            learning_data = {
                "agent_id": "test_agent",
                "insight": "Test insight for cross-agent learning",
                "context": {"test": True}
            }
            
            response = requests.post(f"{self.base_url}/api/agents/learn", json=learning_data, timeout=10)
            if response.status_code == 200:
                learning_result = response.json()
                self.record_test_result("Cross-Agent Learning", True, {
                    "status_code": response.status_code,
                    "learning_result": learning_result
                })
                logger.info("✅ Cross-agent learning test passed")
            else:
                self.record_test_result("Cross-Agent Learning", False, {
                    "status_code": response.status_code,
                    "error": "Cross-agent learning failed"
                })
                logger.error(f"❌ Cross-agent learning test failed: {response.status_code}")
        except Exception as e:
            self.record_test_result("Cross-Agent Learning", False, {"error": str(e)})
            logger.error(f"❌ Cross-agent learning test error: {e}")
    
    async def test_memory_compression(self):
        """Test 8: Memory Compression"""
        logger.info("🔍 Test 8: Memory Compression")
        try:
            # Test memory compression endpoint
            compression_data = {
                "content": "Test content for memory compression",
                "strategy": "hybrid"
            }
            
            response = requests.post(f"{self.base_url}/api/memory/compress", json=compression_data, timeout=10)
            if response.status_code == 200:
                compression_result = response.json()
                self.record_test_result("Memory Compression", True, {
                    "status_code": response.status_code,
                    "compression_result": compression_result
                })
                logger.info("✅ Memory compression test passed")
            else:
                self.record_test_result("Memory Compression", False, {
                    "status_code": response.status_code,
                    "error": "Memory compression failed"
                })
                logger.error(f"❌ Memory compression test failed: {response.status_code}")
        except Exception as e:
            self.record_test_result("Memory Compression", False, {"error": str(e)})
            logger.error(f"❌ Memory compression test error: {e}")
    
    async def test_agent_memory_optimization(self):
        """Test 9: Agent Memory Optimization"""
        logger.info("🔍 Test 9: Agent Memory Optimization")
        try:
            # Test agent memory optimization endpoint
            optimization_data = {
                "agent_id": "test_agent",
                "action": "consolidate"
            }
            
            response = requests.post(f"{self.base_url}/api/agents/optimize-memory", json=optimization_data, timeout=10)
            if response.status_code == 200:
                optimization_result = response.json()
                self.record_test_result("Agent Memory Optimization", True, {
                    "status_code": response.status_code,
                    "optimization_result": optimization_result
                })
                logger.info("✅ Agent memory optimization test passed")
            else:
                self.record_test_result("Agent Memory Optimization", False, {
                    "status_code": response.status_code,
                    "error": "Agent memory optimization failed"
                })
                logger.error(f"❌ Agent memory optimization test failed: {response.status_code}")
        except Exception as e:
            self.record_test_result("Agent Memory Optimization", False, {"error": str(e)})
            logger.error(f"❌ Agent memory optimization test error: {e}")
    
    async def test_end_to_end_integration(self):
        """Test 10: End-to-End Integration"""
        logger.info("🔍 Test 10: End-to-End Integration")
        try:
            # Test complete workflow: store memory -> search -> retrieve
            # Step 1: Store memory
            memory_data = {
                "content": "End-to-end test memory content",
                "agent_id": "integration_test_agent",
                "context": {"test_type": "end_to_end"},
                "tags": ["integration", "test", "end_to_end"]
            }
            
            store_response = requests.post(f"{self.base_url}/api/memory/store", json=memory_data, timeout=10)
            if store_response.status_code != 200:
                raise Exception(f"Memory storage failed: {store_response.status_code}")
            
            # Step 2: Search for memory
            search_data = {
                "query": "end-to-end test",
                "top_k": 5
            }
            
            search_response = requests.post(f"{self.base_url}/api/memory/search", json=search_data, timeout=10)
            if search_response.status_code != 200:
                raise Exception(f"Memory search failed: {search_response.status_code}")
            
            # Step 3: Retrieve memory
            retrieve_response = requests.get(f"{self.base_url}/api/memory/retrieve", timeout=10)
            if retrieve_response.status_code != 200:
                raise Exception(f"Memory retrieval failed: {retrieve_response.status_code}")
            
            self.record_test_result("End-to-End Integration", True, {
                "store_status": store_response.status_code,
                "search_status": search_response.status_code,
                "retrieve_status": retrieve_response.status_code
            })
            logger.info("✅ End-to-end integration test passed")
            
        except Exception as e:
            self.record_test_result("End-to-End Integration", False, {"error": str(e)})
            logger.error(f"❌ End-to-end integration test error: {e}")
    
    def record_test_result(self, test_name: str, passed: bool, details: Dict[str, Any]):
        """Record the result of a test"""
        self.test_results["tests_run"] += 1
        if passed:
            self.test_results["tests_passed"] += 1
        else:
            self.test_results["tests_failed"] += 1
        
        self.test_results["detailed_results"].append({
            "test_name": test_name,
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
    
    def generate_final_report(self):
        """Generate the final test report"""
        logger.info("📊 Generating Final Test Report")
        
        total_tests = self.test_results["tests_run"]
        passed_tests = self.test_results["tests_passed"]
        failed_tests = self.test_results["tests_failed"]
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        logger.info(f"📈 Test Results Summary:")
        logger.info(f"   Total Tests: {total_tests}")
        logger.info(f"   Passed: {passed_tests}")
        logger.info(f"   Failed: {failed_tests}")
        logger.info(f"   Success Rate: {success_rate:.1f}%")
        
        # Save detailed results to file
        with open("comprehensive_rag_memory_test_results.json", "w") as f:
            json.dump(self.test_results, f, indent=2)
        
        logger.info("💾 Detailed results saved to: comprehensive_rag_memory_test_results.json")
        
        if success_rate >= 80:
            logger.info("🎉 RAG Memory System Analysis Implementation: EXCELLENT")
        elif success_rate >= 60:
            logger.info("✅ RAG Memory System Analysis Implementation: GOOD")
        else:
            logger.info("⚠️ RAG Memory System Analysis Implementation: NEEDS IMPROVEMENT")

async def main():
    """Main test execution"""
    test_suite = ComprehensiveRAGMemorySystemTest()
    await test_suite.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
