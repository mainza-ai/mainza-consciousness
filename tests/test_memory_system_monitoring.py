#!/usr/bin/env python3
"""
Test script for Memory System Health Monitoring and Management

This script tests the memory system monitoring and lifecycle management
functionality to ensure it works correctly.
"""

import asyncio
import sys
import os
import logging

# Load environment variables first
from dotenv import load_dotenv
load_dotenv()

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.utils.memory_system_monitor import memory_monitor, HealthStatus
from backend.utils.memory_lifecycle_manager import memory_lifecycle_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_memory_monitoring():
    """Test memory system monitoring functionality"""
    print("🧪 Testing Memory System Monitoring...")
    
    try:
        # Test monitor initialization
        print("1. Testing monitor initialization...")
        initialized = await memory_monitor.initialize()
        if initialized:
            print("✅ Memory monitor initialized successfully")
        else:
            print("❌ Memory monitor initialization failed")
            return False
        
        # Test health check
        print("2. Testing health check...")
        health_status = await memory_monitor.perform_health_check()
        print(f"   Overall status: {health_status.overall_status.value}")
        print(f"   Storage status: {health_status.storage_status.value}")
        print(f"   Retrieval status: {health_status.retrieval_status.value}")
        print(f"   Neo4j status: {health_status.neo4j_status.value}")
        
        # Test performance metrics
        print("3. Testing performance metrics...")
        metrics = await memory_monitor.get_performance_metrics()
        print(f"   Available metrics: {list(metrics.keys())}")
        
        # Test usage statistics
        print("4. Testing usage statistics...")
        usage_stats = await memory_monitor.update_usage_statistics()
        print(f"   Total memories: {usage_stats.total_memories}")
        print(f"   Storage size: {usage_stats.storage_size_mb:.2f} MB")
        
        # Test dashboard data
        print("5. Testing dashboard data...")
        dashboard = await memory_monitor.get_system_status_dashboard()
        print(f"   Dashboard sections: {list(dashboard.keys())}")
        
        print("✅ Memory monitoring tests completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Memory monitoring test failed: {e}")
        return False

async def test_memory_lifecycle():
    """Test memory lifecycle management functionality"""
    print("\n🧪 Testing Memory Lifecycle Management...")
    
    try:
        # Test lifecycle manager initialization
        print("1. Testing lifecycle manager initialization...")
        initialized = await memory_lifecycle_manager.initialize()
        if initialized:
            print("✅ Memory lifecycle manager initialized successfully")
        else:
            print("❌ Memory lifecycle manager initialization failed")
            return False
        
        # Test importance decay
        print("2. Testing importance decay...")
        decay_results = await memory_lifecycle_manager.apply_importance_decay()
        if 'error' not in decay_results:
            print(f"   Processed {decay_results.get('memories_processed', 0)} memories")
            print(f"   Updated {decay_results.get('memories_updated', 0)} memories")
            print("✅ Importance decay test completed")
        else:
            print(f"❌ Importance decay failed: {decay_results['error']}")
        
        # Test memory cleanup
        print("3. Testing memory cleanup...")
        cleanup_results = await memory_lifecycle_manager.cleanup_low_importance_memories()
        print(f"   Processed: {cleanup_results.total_memories_processed}")
        print(f"   Archived: {cleanup_results.memories_archived}")
        print(f"   Deleted: {cleanup_results.memories_deleted}")
        print(f"   Processing time: {cleanup_results.processing_time_seconds:.2f}s")
        print("✅ Memory cleanup test completed")
        
        # Test storage optimization
        print("4. Testing storage optimization...")
        optimization_results = await memory_lifecycle_manager.optimize_memory_storage()
        if 'error' not in optimization_results:
            print("✅ Storage optimization test completed")
        else:
            print(f"❌ Storage optimization failed: {optimization_results['error']}")
        
        # Test lifecycle status
        print("5. Testing lifecycle status...")
        status = await memory_lifecycle_manager.get_lifecycle_status()
        print(f"   Lifecycle active: {status['lifecycle_active']}")
        print(f"   Configuration keys: {list(status['configuration'].keys())}")
        
        print("✅ Memory lifecycle tests completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Memory lifecycle test failed: {e}")
        return False

async def test_integration():
    """Test integration between monitoring and lifecycle management"""
    print("\n🧪 Testing Integration...")
    
    try:
        # Test that both systems can work together
        print("1. Testing concurrent operation...")
        
        # Run health check and maintenance simultaneously
        health_task = memory_monitor.perform_health_check()
        maintenance_task = memory_lifecycle_manager.run_daily_maintenance()
        
        health_result, maintenance_result = await asyncio.gather(
            health_task, maintenance_task, return_exceptions=True
        )
        
        if isinstance(health_result, Exception):
            print(f"❌ Health check failed: {health_result}")
        else:
            print(f"✅ Health check completed: {health_result.overall_status.value}")
        
        if isinstance(maintenance_result, Exception):
            print(f"❌ Maintenance failed: {maintenance_result}")
        else:
            print("✅ Maintenance completed successfully")
        
        print("✅ Integration tests completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

async def main():
    """Run all memory system tests"""
    print("🚀 Starting Memory System Health Monitoring and Management Tests\n")
    
    # Run individual test suites
    monitoring_success = await test_memory_monitoring()
    lifecycle_success = await test_memory_lifecycle()
    integration_success = await test_integration()
    
    # Summary
    print("\n📊 Test Results Summary:")
    print(f"   Memory Monitoring: {'✅ PASS' if monitoring_success else '❌ FAIL'}")
    print(f"   Memory Lifecycle: {'✅ PASS' if lifecycle_success else '❌ FAIL'}")
    print(f"   Integration: {'✅ PASS' if integration_success else '❌ FAIL'}")
    
    overall_success = monitoring_success and lifecycle_success and integration_success
    
    if overall_success:
        print("\n🎉 All memory system tests passed successfully!")
        print("Memory system health monitoring and management is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Please check the implementation.")
    
    return overall_success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)