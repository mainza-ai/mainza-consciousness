#!/usr/bin/env python3
"""
Comprehensive Test Runner for Mainza AI
Runs all updated tests and provides detailed reporting
"""
import subprocess
import sys
import os
import time
from datetime import datetime
from pathlib import Path

def run_test(test_file, test_name):
    """Run a single test file and return results"""
    print(f"\n{'='*60}")
    print(f"🧪 Running: {test_name}")
    print(f"📁 File: {test_file}")
    print(f"⏰ Started: {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ {test_name} - PASSED ({duration:.2f}s)")
            return True, duration, result.stdout
        else:
            print(f"❌ {test_name} - FAILED ({duration:.2f}s)")
            print(f"Error output: {result.stderr}")
            return False, duration, result.stderr
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {test_name} - TIMEOUT (300s)")
        return False, 300, "Test timed out"
    except Exception as e:
        print(f"💥 {test_name} - ERROR: {e}")
        return False, 0, str(e)

def main():
    """Run all tests and provide comprehensive reporting"""
    print("🚀 MAINZA AI COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print(f"Test run started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Define test categories and their tests
    test_categories = {
        "Core System Tests": [
            ("test_system_comprehensive_updated.py", "Comprehensive System Test (Updated)"),
            ("test_system_startup.py", "System Startup Test"),
            ("test_server_startup.py", "Server Startup Test")
        ],
        "API & Integration Tests": [
            ("test_api_endpoints.py", "API Endpoints Test"),
            ("test_frontend_backend_comprehensive.py", "Frontend-Backend Integration Test"),
            ("test_backend_frontend_integration.py", "Backend-Frontend Integration Test")
        ],
        "Consciousness System Tests": [
            ("test_consciousness_system.py", "Consciousness System Test"),
            ("test_consciousness_insights.py", "Consciousness Insights Test"),
            ("test_consciousness_memory_integration.py", "Consciousness Memory Integration Test")
        ],
        "LLM & Optimization Tests": [
            ("test_llm_optimization.py", "LLM Optimization Test"),
            ("test_llm_response_truncation.py", "LLM Response Truncation Test"),
            ("test_throttling_integration.py", "Throttling Integration Test")
        ],
        "Docker & Build System Tests": [
            ("test_docker_build_system.py", "Docker Build System Test")
        ],
        "Insights Dashboard Tests": [
            ("test_insights_dashboard_updates.py", "Insights Dashboard Updates Test"),
            ("test_insights_system.py", "Insights System Test")
        ],
        "Agent System Tests": [
            ("test_agent_execution.py", "Agent Execution Test"),
            ("test_enhanced_agent_integration.py", "Enhanced Agent Integration Test"),
            ("test_simple_chat_agent.py", "Simple Chat Agent Test")
        ],
        "Memory System Tests": [
            ("test_memory_system_monitoring.py", "Memory System Monitoring Test")
        ],
        "Error Handling Tests": [
            ("test_critical_error_fixes.py", "Critical Error Fixes Test"),
            ("test_enhanced_error_handling_integration.py", "Enhanced Error Handling Test"),
            ("test_runtime_error_fixes.py", "Runtime Error Fixes Test")
        ]
    }
    
    # Track results
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    total_duration = 0
    category_results = {}
    
    # Run tests by category
    for category, tests in test_categories.items():
        print(f"\n{'🔍 ' + category.upper() + ' ' + '🔍':=^70}")
        
        category_passed = 0
        category_failed = 0
        category_duration = 0
        
        for test_file, test_name in tests:
            if os.path.exists(test_file):
                total_tests += 1
                passed, duration, output = run_test(test_file, test_name)
                
                if passed:
                    passed_tests += 1
                    category_passed += 1
                else:
                    failed_tests += 1
                    category_failed += 1
                
                total_duration += duration
                category_duration += duration
            else:
                print(f"⚠️  {test_file} - FILE NOT FOUND")
                failed_tests += 1
                category_failed += 1
        
        category_results[category] = {
            'passed': category_passed,
            'failed': category_failed,
            'duration': category_duration
        }
    
    # Generate comprehensive report
    print(f"\n{'='*70}")
    print("📊 COMPREHENSIVE TEST REPORT")
    print(f"{'='*70}")
    print(f"Test run completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total duration: {total_duration:.2f} seconds")
    print()
    
    # Overall results
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    print(f"📈 OVERALL RESULTS:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Passed: {passed_tests} ✅")
    print(f"   Failed: {failed_tests} ❌")
    print(f"   Success Rate: {success_rate:.1f}%")
    print()
    
    # Category breakdown
    print(f"📋 CATEGORY BREAKDOWN:")
    for category, results in category_results.items():
        cat_total = results['passed'] + results['failed']
        cat_success_rate = (results['passed'] / cat_total * 100) if cat_total > 0 else 0
        print(f"   {category}:")
        print(f"     Passed: {results['passed']}/{cat_total} ({cat_success_rate:.1f}%)")
        print(f"     Duration: {results['duration']:.2f}s")
    
    print()
    
    # Recommendations
    if failed_tests == 0:
        print("🎉 ALL TESTS PASSED!")
        print("✅ System is ready for production deployment")
        print("✅ All recent updates are working correctly")
        print("✅ Docker optimization is functional")
        print("✅ LLM optimization is active")
        print("✅ Insights dashboard is operational")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED!")
        print("🔧 Recommendations:")
        print("   1. Review failed test outputs above")
        print("   2. Check service status with 'docker-compose ps'")
        print("   3. Verify services are running with './scripts/verify-changes.sh'")
        print("   4. Check service logs with 'docker-compose logs'")
        print("   5. Rebuild if necessary with './scripts/build-dev.sh'")
        return 1

if __name__ == "__main__":
    exit(main())
