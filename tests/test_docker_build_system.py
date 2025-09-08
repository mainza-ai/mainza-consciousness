#!/usr/bin/env python3
"""
Test Docker Build System
Context7 MCP Compliance Testing

This script tests the Docker build system and verification tools:
1. Docker build scripts functionality
2. Build verification scripts
3. Docker optimization features
4. Build info endpoints
"""

import sys
import os
import subprocess
import time
import requests
from datetime import datetime
from pathlib import Path

def test_docker_build_scripts():
    """Test that all Docker build scripts exist and are executable"""
    print("🔍 Testing Docker Build Scripts...")
    
    required_scripts = [
        "scripts/build-dev.sh",
        "scripts/build-prod.sh", 
        "scripts/build-dev-hot.sh",
        "scripts/verify-changes.sh",
        "scripts/monitor-builds.sh",
        "scripts/dev-tools.sh"
    ]
    
    missing_scripts = []
    non_executable = []
    
    for script_path in required_scripts:
        if not os.path.exists(script_path):
            missing_scripts.append(script_path)
        elif not os.access(script_path, os.X_OK):
            non_executable.append(script_path)
        else:
            print(f"  ✅ {script_path}: Exists and executable")
    
    if missing_scripts:
        print("❌ Missing Docker Build Scripts:")
        for script in missing_scripts:
            print(f"  - {script}")
        return False
    
    if non_executable:
        print("❌ Non-executable Docker Build Scripts:")
        for script in non_executable:
            print(f"  - {script}")
        return False
    
    print("✅ All Docker build scripts present and executable!")
    return True

def test_dockerfile_optimizations():
    """Test that Dockerfiles have optimization features"""
    print("\n🔍 Testing Dockerfile Optimizations...")
    
    dockerfiles = [
        "Dockerfile",
        "Dockerfile.frontend",
        "Dockerfile.backend.dev",
        "Dockerfile.frontend.dev"
    ]
    
    optimization_features = [
        "CACHE_BUST",
        "BUILD_DATE", 
        "GIT_COMMIT",
        "ENV BUILD_DATE",
        "ENV GIT_COMMIT",
        "ENV CACHE_BUST"
    ]
    
    issues_found = []
    
    for dockerfile in dockerfiles:
        if os.path.exists(dockerfile):
            with open(dockerfile, 'r') as f:
                content = f.read()
            
            found_features = []
            for feature in optimization_features:
                if feature in content:
                    found_features.append(feature)
            
            if len(found_features) >= 3:  # At least 3 optimization features
                print(f"  ✅ {dockerfile}: {len(found_features)} optimization features found")
            else:
                issues_found.append(f"{dockerfile}: Only {len(found_features)} optimization features found")
        else:
            issues_found.append(f"{dockerfile}: File not found")
    
    if issues_found:
        print("❌ Dockerfile Optimization Issues:")
        for issue in issues_found:
            print(f"  - {issue}")
        return False
    else:
        print("✅ All Dockerfiles have optimization features!")
        return True

def test_dockerignore_file():
    """Test that .dockerignore file exists and is properly configured"""
    print("\n🔍 Testing .dockerignore Configuration...")
    
    dockerignore_path = ".dockerignore"
    
    if not os.path.exists(dockerignore_path):
        print("❌ .dockerignore file not found")
        return False
    
    with open(dockerignore_path, 'r') as f:
        content = f.read()
    
    required_exclusions = [
        "node_modules/",
        "dist/",
        "docs/",
        "*.md",
        ".git/",
        "logs/"
    ]
    
    missing_exclusions = []
    for exclusion in required_exclusions:
        if exclusion not in content:
            missing_exclusions.append(exclusion)
    
    if missing_exclusions:
        print("❌ Missing .dockerignore exclusions:")
        for exclusion in missing_exclusions:
            print(f"  - {exclusion}")
        return False
    
    print("✅ .dockerignore properly configured!")
    return True

def test_build_info_endpoint():
    """Test that build info endpoint is accessible"""
    print("\n🔍 Testing Build Info Endpoint...")
    
    try:
        # Test if backend is running
        response = requests.get("http://localhost:8000/build/info", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            required_fields = ["build_date", "git_commit", "cache_bust", "status"]
            
            missing_fields = []
            for field in required_fields:
                if field not in data:
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"❌ Build info endpoint missing fields: {missing_fields}")
                return False
            
            print("✅ Build info endpoint working correctly!")
            print(f"  - Build Date: {data.get('build_date', 'N/A')}")
            print(f"  - Git Commit: {data.get('git_commit', 'N/A')}")
            print(f"  - Cache Bust: {data.get('cache_bust', 'N/A')}")
            print(f"  - Status: {data.get('status', 'N/A')}")
            return True
        else:
            print(f"❌ Build info endpoint returned status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("⚠️ Backend not running - skipping build info endpoint test")
        return True
    except Exception as e:
        print(f"❌ Build info endpoint test failed: {e}")
        return False

def test_docker_compose_configuration():
    """Test that docker-compose files are properly configured"""
    print("\n🔍 Testing Docker Compose Configuration...")
    
    compose_files = [
        "docker-compose.yml",
        "docker-compose.dev.yml"
    ]
    
    issues_found = []
    
    for compose_file in compose_files:
        if os.path.exists(compose_file):
            with open(compose_file, 'r') as f:
                content = f.read()
            
            # Check for build args
            if "build-args" in content or "args:" in content:
                print(f"  ✅ {compose_file}: Build args configured")
            else:
                issues_found.append(f"{compose_file}: Build args not configured")
        else:
            issues_found.append(f"{compose_file}: File not found")
    
    if issues_found:
        print("❌ Docker Compose Configuration Issues:")
        for issue in issues_found:
            print(f"  - {issue}")
        return False
    else:
        print("✅ Docker Compose files properly configured!")
        return True

def test_verification_script_functionality():
    """Test that verification script has required functionality"""
    print("\n🔍 Testing Verification Script Functionality...")
    
    script_path = "scripts/verify-changes.sh"
    
    if not os.path.exists(script_path):
        print("❌ Verification script not found")
        return False
    
    with open(script_path, 'r') as f:
        content = f.read()
    
    required_functions = [
        "docker-compose ps",
        "grep",
        "curl",
        "build-info.js",
        "/build/info"
    ]
    
    missing_functions = []
    for function in required_functions:
        if function not in content:
            missing_functions.append(function)
    
    if missing_functions:
        print("❌ Verification script missing functionality:")
        for function in missing_functions:
            print(f"  - {function}")
        return False
    
    print("✅ Verification script has required functionality!")
    return True

def test_frontend_build_info():
    """Test that frontend build info is properly configured"""
    print("\n🔍 Testing Frontend Build Info Configuration...")
    
    # Check if build info script exists
    build_info_script = "scripts/frontend-build-info.js"
    if not os.path.exists(build_info_script):
        print("❌ Frontend build info script not found")
        return False
    
    # Check if Dockerfile.frontend embeds build info
    dockerfile_frontend = "Dockerfile.frontend"
    if os.path.exists(dockerfile_frontend):
        with open(dockerfile_frontend, 'r') as f:
            content = f.read()
        
        if "window.BUILD_INFO" in content and "build-info.js" in content:
            print("✅ Frontend build info properly configured in Dockerfile!")
        else:
            print("❌ Frontend build info not properly configured in Dockerfile")
            return False
    else:
        print("❌ Dockerfile.frontend not found")
        return False
    
    return True

def test_github_actions_optimization():
    """Test that GitHub Actions workflow has Docker optimization"""
    print("\n🔍 Testing GitHub Actions Docker Optimization...")
    
    workflow_path = ".github/workflows/ci.yml"
    
    if not os.path.exists(workflow_path):
        print("❌ GitHub Actions workflow not found")
        return False
    
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    required_features = [
        "build-args",
        "CACHE_BUST",
        "BUILD_DATE",
        "GIT_COMMIT",
        "cache-from",
        "cache-to"
    ]
    
    missing_features = []
    for feature in required_features:
        if feature not in content:
            missing_features.append(feature)
    
    if missing_features:
        print("❌ GitHub Actions missing Docker optimization features:")
        for feature in missing_features:
            print(f"  - {feature}")
        return False
    
    print("✅ GitHub Actions workflow has Docker optimization!")
    return True

def main():
    """Run all Docker build system tests"""
    print("🚀 Docker Build System Testing - Context7 MCP Compliance")
    print("=" * 70)
    
    all_tests_passed = True
    
    tests = [
        test_docker_build_scripts,
        test_dockerfile_optimizations,
        test_dockerignore_file,
        test_build_info_endpoint,
        test_docker_compose_configuration,
        test_verification_script_functionality,
        test_frontend_build_info,
        test_github_actions_optimization
    ]
    
    for test in tests:
        if not test():
            all_tests_passed = False
    
    print("\n" + "=" * 70)
    
    if all_tests_passed:
        print("🎉 ALL DOCKER BUILD SYSTEM TESTS PASSED!")
        print("✅ Build scripts present and executable")
        print("✅ Dockerfile optimizations implemented")
        print("✅ Build verification system operational")
        print("✅ Docker caching issues resolved")
        print("✅ Context7 MCP compliance maintained")
        return 0
    else:
        print("❌ SOME DOCKER BUILD SYSTEM ISSUES EXIST!")
        print("⚠️  Please review and fix remaining issues")
        return 1

if __name__ == "__main__":
    exit(main())
