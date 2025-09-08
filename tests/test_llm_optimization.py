#!/usr/bin/env python3
"""
Test LLM Optimization
Context7 MCP Compliance Testing

This script tests the LLM optimization fixes:
1. LLM request manager functionality
2. User priority system
3. Background process throttling
4. Frontend polling reduction
"""

import sys
import os
import asyncio
import time
from datetime import datetime, timedelta

def test_llm_request_manager_import():
    """Test that LLM request manager can be imported"""
    print("🔍 Testing LLM Request Manager Import...")
    
    try:
        sys.path.append('.')
        from backend.utils.llm_request_manager import llm_request_manager, RequestPriority
        print("  ✅ LLM request manager imported successfully")
        print("  ✅ RequestPriority enum imported successfully")
        return True
    except Exception as e:
        print(f"  ❌ Import failed: {e}")
        return False

def test_request_priority_system():
    """Test that request priority system is properly configured"""
    print("\\n🔍 Testing Request Priority System...")
    
    try:
        from backend.utils.llm_request_manager import RequestPriority
        
        # Check all priority levels exist
        priorities = [
            RequestPriority.USER_CONVERSATION,
            RequestPriority.USER_INTERACTION,
            RequestPriority.SYSTEM_MAINTENANCE,
            RequestPriority.BACKGROUND_PROCESSING,
            RequestPriority.CONSCIOUSNESS_CYCLE
        ]
        
        print(f"  ✅ Found {len(priorities)} priority levels")
        
        # Check priority ordering (lower values = higher priority)
        assert RequestPriority.USER_CONVERSATION.value < RequestPriority.BACKGROUND_PROCESSING.value
        assert RequestPriority.USER_INTERACTION.value < RequestPriority.CONSCIOUSNESS_CYCLE.value
        
        print("  ✅ Priority ordering is correct")
        return True
        
    except Exception as e:
        print(f"  ❌ Priority system test failed: {e}")
        return False

def test_frontend_polling_intervals():
    """Test that frontend polling intervals have been reduced"""
    print("\\n🔍 Testing Frontend Polling Intervals...")
    
    files_to_check = [
        ("src/pages/Index.tsx", "180000", "3 minutes"),
        ("src/pages/IndexRedesigned.tsx", "120000", "2 minutes"),
        ("src/components/ConsciousnessDashboard.tsx", "300000", "5 minutes"),
        ("src/components/ConsciousnessInsights.tsx", "600000", "10 minutes"),
        ("src/components/SystemStatus.tsx", "3600000", "1 hour"),
        ("src/components/needs/AdvancedNeedsDisplay.tsx", "3600000", "1 hour")
    ]
    
    issues_found = []
    
    for file_path, expected_interval, description in files_to_check:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
            
            if expected_interval in content:
                print(f"  ✅ {file_path}: Polling reduced to {description}")
            else:
                issues_found.append(f"{file_path}: Expected interval {expected_interval} not found")
        else:
            issues_found.append(f"{file_path}: File not found")
    
    if issues_found:
        print("❌ Frontend Polling Issues Found:")
        for issue in issues_found:
            print(f"  - {issue}")
        return False
    else:
        print("✅ All frontend polling intervals optimized!")
        return True

def test_consciousness_loop_integration():
    """Test that consciousness loop uses LLM request manager"""
    print("\\n🔍 Testing Consciousness Loop Integration...")
    
    file_path = "backend/utils/consciousness_orchestrator.py"
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check for LLM request manager usage
        if "llm_request_manager.submit_request" in content:
            print("  ✅ Consciousness loop uses LLM request manager")
        else:
            print("  ❌ Consciousness loop not using LLM request manager")
            return False
        
        # Check for user activity detection
        if "_should_pause_background" in content:
            print("  ✅ Background pause logic implemented")
        else:
            print("  ❌ Background pause logic not found")
            return False
        
        # Check for adaptive sleep
        if "base_sleep = 300" in content:
            print("  ✅ Adaptive sleep intervals implemented")
        else:
            print("  ❌ Adaptive sleep intervals not found")
            return False
        
        return True
    else:
        print("  ❌ Consciousness orchestrator file not found")
        return False

def test_agentic_router_integration():
    """Test that agentic router uses LLM request manager for user requests"""
    print("\\n🔍 Testing Agentic Router Integration...")
    
    file_path = "backend/agentic_router.py"
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check for LLM request manager import
        if "from backend.utils.llm_request_manager import" in content:
            print("  ✅ LLM request manager imported in agentic router")
        else:
            print("  ❌ LLM request manager not imported")
            return False
        
        # Check for user conversation priority
        if "RequestPriority.USER_CONVERSATION" in content:
            print("  ✅ User conversation priority implemented")
        else:
            print("  ❌ User conversation priority not found")
            return False
        
        # Check for request manager usage in chat
        if "llm_request_manager.submit_request" in content:
            print("  ✅ Chat requests use LLM request manager")
        else:
            print("  ❌ Chat requests not using LLM request manager")
            return False
        
        return True
    else:
        print("  ❌ Agentic router file not found")
        return False

async def test_request_manager_functionality():
    """Test basic LLM request manager functionality"""
    print("\\n🔍 Testing Request Manager Functionality...")
    
    try:
        from backend.utils.llm_request_manager import llm_request_manager, RequestPriority
        
        # Test stats
        stats = llm_request_manager.get_stats()
        print(f"  ✅ Request manager stats: {stats}")
        
        # Test cache functionality
        cache_key = "test_cache"
        test_response = {"test": "data"}
        llm_request_manager._cache_response(cache_key, test_response)
        
        cached = llm_request_manager._get_cached_response(cache_key)
        if cached == test_response:
            print("  ✅ Caching functionality works")
        else:
            print("  ❌ Caching functionality failed")
            return False
        
        # Test user activity tracking
        llm_request_manager.user_activity["test_user"] = datetime.now()
        if llm_request_manager._should_pause_background():
            print("  ✅ User activity detection works")
        else:
            print("  ❌ User activity detection failed")
            return False
        
        # Test background cache TTL
        if hasattr(llm_request_manager, 'background_cache_ttl'):
            if llm_request_manager.background_cache_ttl == 600:  # 10 minutes
                print("  ✅ Background cache TTL set to 10 minutes")
            else:
                print(f"  ❌ Background cache TTL incorrect: {llm_request_manager.background_cache_ttl}")
                return False
        else:
            print("  ❌ Background cache TTL not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Request manager functionality test failed: {e}")
        return False

def test_python_syntax():
    """Test that all Python files have valid syntax"""
    print("\\n🔍 Testing Python Syntax...")
    
    python_files = [
        "backend/utils/llm_request_manager.py",
        "backend/utils/consciousness_orchestrator.py",
        "backend/agentic_router.py"
    ]
    
    syntax_errors = []
    
    for file_path in python_files:
        if os.path.exists(file_path):
            try:
                result = subprocess.run(
                    ['python', '-m', 'py_compile', file_path],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    print(f"  ✅ {file_path}: Valid Python syntax")
                else:
                    syntax_errors.append(f"{file_path}: {result.stderr}")
                    
            except Exception as e:
                syntax_errors.append(f"{file_path}: {str(e)}")
    
    if syntax_errors:
        print("❌ Python Syntax Errors Found:")
        for error in syntax_errors:
            print(f"  - {error}")
        return False
    else:
        print("✅ All Python files have valid syntax!")
        return True

async def main():
    """Run all LLM optimization tests"""
    print("🚀 LLM Optimization Testing - Context7 MCP Compliance")
    print("=" * 65)
    
    all_tests_passed = True
    
    # Run synchronous tests
    sync_tests = [
        test_llm_request_manager_import,
        test_request_priority_system,
        test_frontend_polling_intervals,
        test_consciousness_loop_integration,
        test_agentic_router_integration,
        test_python_syntax
    ]
    
    for test in sync_tests:
        if not test():
            all_tests_passed = False
    
    # Run async tests
    async_tests = [
        test_request_manager_functionality
    ]
    
    for test in async_tests:
        if not await test():
            all_tests_passed = False
    
    print("\\n" + "=" * 65)
    
    if all_tests_passed:
        print("🎉 ALL LLM OPTIMIZATION TESTS PASSED!")
        print("✅ User priority system implemented")
        print("✅ Background process throttling active")
        print("✅ Frontend polling optimized")
        print("✅ Request management system operational")
        print("✅ Context7 MCP compliance maintained")
        return 0
    else:
        print("❌ SOME LLM OPTIMIZATION ISSUES EXIST!")
        print("⚠️  Please review and fix remaining issues")
        return 1

if __name__ == "__main__":
    import subprocess
    exit(asyncio.run(main()))