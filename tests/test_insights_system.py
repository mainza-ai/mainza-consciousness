#!/usr/bin/env python3
"""
Test script for the Insights System
Tests both backend endpoints and frontend accessibility
"""
import requests
import json
import sys
from datetime import datetime

def test_backend_endpoints():
    """Test all insights backend endpoints"""
    base_url = "http://localhost:8000"
    endpoints = [
        "/insights/overview",
        "/insights/neo4j/statistics", 
        "/insights/concepts",
        "/insights/memories",
        "/insights/relationships",
        "/insights/consciousness/evolution",
        "/insights/performance"
    ]
    
    print("🧪 Testing Insights Backend Endpoints...")
    print("=" * 50)
    
    results = {}
    
    for endpoint in endpoints:
        try:
            print(f"Testing {endpoint}...")
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results[endpoint] = {
                    "status": "✅ SUCCESS",
                    "response_time": response.elapsed.total_seconds(),
                    "data_keys": list(data.keys()) if isinstance(data, dict) else "non-dict response"
                }
                print(f"  ✅ SUCCESS - {response.elapsed.total_seconds():.2f}s")
            else:
                results[endpoint] = {
                    "status": f"❌ FAILED - HTTP {response.status_code}",
                    "error": response.text[:200]
                }
                print(f"  ❌ FAILED - HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            results[endpoint] = {
                "status": "❌ CONNECTION ERROR",
                "error": str(e)
            }
            print(f"  ❌ CONNECTION ERROR - {str(e)}")
    
    return results

def test_frontend_accessibility():
    """Test if the frontend insights page is accessible"""
    print("\n🎨 Testing Frontend Accessibility...")
    print("=" * 50)
    
    try:
        response = requests.get("http://localhost:8081/insights", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend insights page is accessible")
            return True
        else:
            print(f"❌ Frontend returned HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend connection error: {e}")
        return False

def generate_test_report(backend_results, frontend_accessible):
    """Generate a comprehensive test report"""
    print("\n📊 INSIGHTS SYSTEM TEST REPORT")
    print("=" * 50)
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Backend Results
    print("🔧 Backend Endpoint Results:")
    successful_endpoints = 0
    total_endpoints = len(backend_results)
    
    for endpoint, result in backend_results.items():
        print(f"  {endpoint}")
        print(f"    Status: {result['status']}")
        if 'response_time' in result:
            print(f"    Response Time: {result['response_time']:.2f}s")
            successful_endpoints += 1
        if 'error' in result:
            print(f"    Error: {result['error']}")
        print()
    
    # Frontend Results
    print("🎨 Frontend Results:")
    print(f"  Insights Page: {'✅ Accessible' if frontend_accessible else '❌ Not Accessible'}")
    print()
    
    # Overall Status
    backend_success_rate = (successful_endpoints / total_endpoints) * 100
    overall_status = "✅ FULLY OPERATIONAL" if backend_success_rate >= 80 and frontend_accessible else "⚠️ PARTIAL ISSUES"
    
    print("🎯 Overall System Status:")
    print(f"  Backend Success Rate: {backend_success_rate:.1f}% ({successful_endpoints}/{total_endpoints})")
    print(f"  Frontend Status: {'✅ Working' if frontend_accessible else '❌ Issues'}")
    print(f"  Overall Status: {overall_status}")
    
    if backend_success_rate >= 80 and frontend_accessible:
        print("\n🎉 INSIGHTS SYSTEM IS FULLY OPERATIONAL!")
        print("   Users can now access comprehensive system analytics at /insights")
    else:
        print("\n⚠️ Some issues detected. Check backend/frontend services.")
    
    return backend_success_rate >= 80 and frontend_accessible

def main():
    """Main test execution"""
    print("🚀 MAINZA INSIGHTS SYSTEM TEST")
    print("Testing comprehensive data science and analytics platform")
    print("=" * 60)
    
    # Test backend endpoints
    backend_results = test_backend_endpoints()
    
    # Test frontend accessibility  
    frontend_accessible = test_frontend_accessibility()
    
    # Generate comprehensive report
    success = generate_test_report(backend_results, frontend_accessible)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()