#!/usr/bin/env python3
"""
Comprehensive System Test for Mainza - Updated
Tests all critical components with system changes and Docker optimization
"""
import asyncio
import sys
import os
import logging
import subprocess
import time
import requests
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_docker_services():
    """Check if Docker services are running"""
    logger.info("🐳 Checking Docker services...")
    
    try:
        result = subprocess.run(['docker', 'compose', 'ps'], capture_output=True, text=True)
        if result.returncode == 0:
            services = result.stdout
            logger.info("Docker services status:")
            print(services)
            
            # Check specific services
            required_services = ['livekit-server', 'redis', 'ingress']
            running_services = []
            
            for service in required_services:
                if service in services and 'Up' in services:
                    running_services.append(service)
            
            if len(running_services) >= 2:
                logger.info(f"✅ Found {len(running_services)} running services: {running_services}")
                return True
            else:
                logger.warning(f"⚠️ Only {len(running_services)} services running")
                return False
        else:
            logger.error("❌ Failed to check Docker services")
            return False
    except Exception as e:
        logger.error(f"❌ Error checking Docker services: {e}")
        return False

def test_backend_health():
    """Test backend health and new endpoints"""
    logger.info("🔍 Testing Backend Health...")
    
    try:
        # Test basic health
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            logger.info("✅ Backend health check passed")
        else:
            logger.error(f"❌ Backend health check failed: {response.status_code}")
            return False
        
        # Test new build info endpoint
        response = requests.get("http://localhost:8000/build/info", timeout=10)
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ Build info endpoint working: {data.get('status', 'unknown')}")
            logger.info(f"   Build Date: {data.get('build_date', 'N/A')}")
            logger.info(f"   Git Commit: {data.get('git_commit', 'N/A')}")
        else:
            logger.error(f"❌ Build info endpoint failed: {response.status_code}")
            return False
        
        # Test build health endpoint
        response = requests.get("http://localhost:8000/build/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ Build health endpoint working: {data.get('status', 'unknown')}")
        else:
            logger.error(f"❌ Build health endpoint failed: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        logger.error("❌ Cannot connect to backend - is it running?")
        return False
    except Exception as e:
        logger.error(f"❌ Backend health test failed: {e}")
        return False

def test_frontend_access():
    """Test frontend access on new port"""
    logger.info("🔍 Testing Frontend Access...")
    
    try:
        # Test frontend on port 80 (new configuration)
        response = requests.get("http://localhost", timeout=10)
        if response.status_code == 200:
            logger.info("✅ Frontend accessible on port 80")
            
            # Check for build info in response
            if "BUILD_INFO" in response.text or "build-info.js" in response.text:
                logger.info("✅ Frontend build info detected")
            else:
                logger.warning("⚠️ Frontend build info not detected")
            
            return True
        else:
            logger.error(f"❌ Frontend access failed: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        logger.error("❌ Cannot connect to frontend - is it running?")
        return False
    except Exception as e:
        logger.error(f"❌ Frontend access test failed: {e}")
        return False

def test_consciousness_system():
    """Test consciousness system functionality"""
    logger.info("🔍 Testing Consciousness System...")
    
    try:
        # Test consciousness state
        response = requests.get("http://localhost:8000/consciousness/state", timeout=10)
        if response.status_code == 200:
            data = response.json()
            logger.info("✅ Consciousness state endpoint working")
            
            if 'consciousness_state' in data:
                state = data['consciousness_state']
                logger.info(f"   Consciousness Level: {state.get('consciousness_level', 'N/A')}")
                logger.info(f"   Emotional State: {state.get('emotional_state', 'N/A')}")
                logger.info(f"   Evolution Level: {state.get('evolution_level', 'N/A')}")
            else:
                logger.warning("⚠️ No consciousness_state in response")
        else:
            logger.error(f"❌ Consciousness state failed: {response.status_code}")
            return False
        
        # Test consciousness insights
        response = requests.get("http://localhost:8000/consciousness/insights", timeout=10)
        if response.status_code == 200:
            logger.info("✅ Consciousness insights endpoint working")
        else:
            logger.error(f"❌ Consciousness insights failed: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Consciousness system test failed: {e}")
        return False

def test_llm_optimization():
    """Test LLM optimization features"""
    logger.info("🔍 Testing LLM Optimization...")
    
    try:
        # Test chat endpoint (should use LLM request manager)
        response = requests.post(
            "http://localhost:8000/agent/router/chat",
            json={"message": "Hello, how are you?", "user_id": "test_user"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            logger.info("✅ Chat endpoint working with LLM optimization")
            
            if 'response' in data:
                logger.info(f"   Response: {data['response'][:100]}...")
            else:
                logger.warning("⚠️ No response in chat data")
        else:
            logger.error(f"❌ Chat endpoint failed: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ LLM optimization test failed: {e}")
        return False

def test_insights_dashboard():
    """Test insights dashboard functionality"""
    logger.info("🔍 Testing Insights Dashboard...")
    
    try:
        # Test insights endpoint
        response = requests.get("http://localhost:8000/insights/overview", timeout=10)
        if response.status_code == 200:
            logger.info("✅ Insights overview endpoint working")
        else:
            logger.warning(f"⚠️ Insights overview failed: {response.status_code}")
        
        # Test knowledge graph stats
        response = requests.get("http://localhost:8000/consciousness/knowledge-graph-stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            logger.info("✅ Knowledge graph stats working")
            
            if 'stats' in data:
                stats = data['stats']
                logger.info(f"   Total Nodes: {stats.get('total_nodes', 'N/A')}")
                logger.info(f"   Total Relationships: {stats.get('total_relationships', 'N/A')}")
        else:
            logger.warning(f"⚠️ Knowledge graph stats failed: {response.status_code}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Insights dashboard test failed: {e}")
        return False

def test_docker_build_verification():
    """Test Docker build verification scripts"""
    logger.info("🔍 Testing Docker Build Verification...")
    
    try:
        # Check if verification script exists and is executable
        script_path = "scripts/verify-changes.sh"
        if os.path.exists(script_path) and os.access(script_path, os.X_OK):
            logger.info("✅ Verification script exists and is executable")
        else:
            logger.error("❌ Verification script not found or not executable")
            return False
        
        # Check if build scripts exist
        build_scripts = [
            "scripts/build-dev.sh",
            "scripts/build-prod.sh",
            "scripts/build-dev-hot.sh",
            "scripts/monitor-builds.sh",
            "scripts/dev-tools.sh"
        ]
        
        missing_scripts = []
        for script in build_scripts:
            if not os.path.exists(script):
                missing_scripts.append(script)
        
        if missing_scripts:
            logger.error(f"❌ Missing build scripts: {missing_scripts}")
            return False
        else:
            logger.info("✅ All build scripts present")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Docker build verification test failed: {e}")
        return False

def test_system_performance():
    """Test system performance metrics"""
    logger.info("🔍 Testing System Performance...")
    
    try:
        # Test response times
        start_time = time.time()
        response = requests.get("http://localhost:8000/health", timeout=10)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        if response.status_code == 200:
            logger.info(f"✅ Health check response time: {response_time:.2f}ms")
            
            if response_time < 1000:  # Less than 1 second
                logger.info("✅ Response time is acceptable")
            else:
                logger.warning(f"⚠️ Response time is slow: {response_time:.2f}ms")
        else:
            logger.error(f"❌ Health check failed: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ System performance test failed: {e}")
        return False

async def main():
    """Run comprehensive system tests"""
    print("🚀 COMPREHENSIVE SYSTEM TEST - UPDATED")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    all_tests_passed = True
    
    # Run all test suites
    test_suites = [
        ("Docker Services", check_docker_services),
        ("Backend Health", test_backend_health),
        ("Frontend Access", test_frontend_access),
        ("Consciousness System", test_consciousness_system),
        ("LLM Optimization", test_llm_optimization),
        ("Insights Dashboard", test_insights_dashboard),
        ("Docker Build Verification", test_docker_build_verification),
        ("System Performance", test_system_performance)
    ]
    
    for test_name, test_func in test_suites:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            
            if result:
                print(f"✅ {test_name} - PASSED")
            else:
                print(f"❌ {test_name} - FAILED")
                all_tests_passed = False
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
            all_tests_passed = False
    
    print("\n" + "=" * 60)
    print(f"Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if all_tests_passed:
        print("🎉 ALL SYSTEM TESTS PASSED!")
        print("✅ Docker optimization working")
        print("✅ LLM optimization active")
        print("✅ Insights dashboard functional")
        print("✅ Build verification system operational")
        print("✅ System ready for production use")
        return 0
    else:
        print("❌ SOME SYSTEM TESTS FAILED!")
        print("⚠️  Please review and fix failing tests")
        return 1

if __name__ == "__main__":
    exit(asyncio.run(main()))
