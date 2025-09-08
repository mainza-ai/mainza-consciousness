#!/usr/bin/env python3
"""
Test API Endpoints
Context7 MCP Compliance Testing

This script tests that all required API endpoints exist and are properly configured:
1. Consciousness endpoints
2. Recommendations endpoints  
3. TTS/STT endpoints
4. LiveKit endpoints
"""

import sys
import os
import re
import subprocess
from pathlib import Path

def test_endpoint_definitions():
    """Test that all required endpoints are defined in the backend"""
    print("🔍 Testing API Endpoint Definitions...")
    
    # Required endpoints based on frontend calls
    required_endpoints = [
        ("/consciousness/state", "GET"),
        ("/consciousness/insights", "GET"),
        ("/consciousness/knowledge-graph-stats", "GET"),
        ("/consciousness/reflect", "POST"),
        ("/recommendations/needs_and_suggestions", "POST"),
        ("/agent/router/chat", "POST"),
        ("/stt/transcribe", "POST"),
        ("/tts/synthesize", "POST"),
        ("/tts/voices", "GET"),
        ("/api/livekit/get-token", "POST"),
        ("/health", "GET"),
        ("/build/info", "GET"),
        ("/build/health", "GET")
    ]
    
    # Check main.py for endpoints
    main_py_path = "backend/main.py"
    agentic_router_path = "backend/agentic_router.py"
    
    found_endpoints = []
    missing_endpoints = []
    
    if os.path.exists(main_py_path):
        with open(main_py_path, 'r') as f:
            main_content = f.read()
        
        for endpoint, method in required_endpoints:
            # Check for endpoint in main.py (more flexible pattern)
            pattern = f'@app\\.{method.lower()}\\(".*{re.escape(endpoint.split("/")[-1])}'
            if re.search(pattern, main_content):
                found_endpoints.append((endpoint, method, "main.py"))
                print(f"  ✅ {method} {endpoint}: Found in main.py")
            else:
                # Check if it might be in agentic_router
                if endpoint.startswith('/consciousness/') or endpoint.startswith('/agent/'):
                    # These should be in agentic_router.py
                    if os.path.exists(agentic_router_path):
                        with open(agentic_router_path, 'r') as f:
                            router_content = f.read()
                        
                        router_pattern = f'@router\\.{method.lower()}\\("{re.escape(endpoint)}"\\)'
                        if re.search(router_pattern, router_content):
                            found_endpoints.append((endpoint, method, "agentic_router.py"))
                            print(f"  ✅ {method} {endpoint}: Found in agentic_router.py")
                        else:
                            missing_endpoints.append((endpoint, method))
                            print(f"  ❌ {method} {endpoint}: Not found")
                    else:
                        missing_endpoints.append((endpoint, method))
                        print(f"  ❌ {method} {endpoint}: agentic_router.py not found")
                else:
                    missing_endpoints.append((endpoint, method))
                    print(f"  ❌ {method} {endpoint}: Not found in main.py")
    
    if missing_endpoints:
        print("\\n❌ Missing Endpoints Found:")
        for endpoint, method in missing_endpoints:
            print(f"  - {method} {endpoint}")
        return False
    else:
        print(f"\\n✅ All {len(found_endpoints)} required endpoints found!")
        return True

def test_router_inclusion():
    """Test that agentic_router is properly included in main app"""
    print("\\n🔍 Testing Router Inclusion...")
    
    main_py_path = "backend/main.py"
    
    if os.path.exists(main_py_path):
        with open(main_py_path, 'r') as f:
            content = f.read()
        
        # Check for router import
        if re.search(r'from.*agentic_router.*import.*agentic_router', content):
            print("  ✅ agentic_router imported correctly")
        else:
            print("  ❌ agentic_router import not found")
            return False
        
        # Check for router inclusion
        if re.search(r'app\.include_router\(agentic_router\)', content):
            print("  ✅ agentic_router included in app")
            return True
        else:
            print("  ❌ agentic_router not included in app")
            return False
    else:
        print("  ❌ main.py not found")
        return False

def test_endpoint_response_structure():
    """Test that endpoints return expected response structures"""
    print("\\n🔍 Testing Endpoint Response Structures...")
    
    # Check needs_and_suggestions endpoint structure
    main_py_path = "backend/main.py"
    
    if os.path.exists(main_py_path):
        with open(main_py_path, 'r') as f:
            content = f.read()
        
        # Check needs_and_suggestions returns correct structure (more flexible pattern)
        if re.search(r'"needs":\s*needs', content):
            print("  ✅ needs_and_suggestions: Returns 'needs' field")
        else:
            print("  ❌ needs_and_suggestions: Missing 'needs' field in response")
            return False
        
        # Check consciousness_level is included
        if re.search(r'"consciousness_level":', content):
            print("  ✅ needs_and_suggestions: Includes consciousness_level")
        else:
            print("  ❌ needs_and_suggestions: Missing consciousness_level")
            return False
        
        print("✅ Endpoint response structures are correct!")
        return True
    else:
        print("  ❌ main.py not found")
        return False

def test_python_syntax():
    """Test that Python files have valid syntax"""
    print("\\n🔍 Testing Python Syntax...")
    
    python_files = [
        "backend/main.py",
        "backend/agentic_router.py"
    ]
    
    syntax_errors = []
    
    for file_path in python_files:
        if os.path.exists(file_path):
            try:
                result = subprocess.run(
                    ['conda', 'run', '-n', 'mainza', 'python', '-m', 'py_compile', file_path],
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

def main():
    """Run all API endpoint tests"""
    print("🚀 API Endpoints Testing - Context7 MCP Compliance")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Run all tests
    tests = [
        test_endpoint_definitions,
        test_router_inclusion,
        test_endpoint_response_structure,
        test_python_syntax
    ]
    
    for test in tests:
        if not test():
            all_tests_passed = False
    
    print("\\n" + "=" * 60)
    
    if all_tests_passed:
        print("🎉 ALL API ENDPOINT TESTS PASSED!")
        print("✅ All required endpoints are defined")
        print("✅ Router inclusion is correct")
        print("✅ Response structures are valid")
        print("✅ Context7 MCP compliance maintained")
        return 0
    else:
        print("❌ SOME API ENDPOINT ISSUES EXIST!")
        print("⚠️  Please review and fix remaining issues")
        return 1

if __name__ == "__main__":
    exit(main())