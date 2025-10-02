#!/usr/bin/env python3
"""
Phase 5 Integration Script for Mainza AI
Comprehensive integration and validation of all Phase 5 components
"""
import asyncio
import aiohttp
import time
import json
import subprocess
import sys
import os
from typing import Dict, Any, List
from datetime import datetime

class Phase5Integration:
    """Phase 5 integration and validation system"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = {}
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def test_comprehensive_testing(self) -> Dict[str, Any]:
        """Test comprehensive testing infrastructure"""
        print("🧪 Testing comprehensive testing infrastructure...")
        
        try:
            # Run production readiness tests
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                "backend/tests/test_production_readiness.py", 
                "-v", "--tb=short"
            ], capture_output=True, text=True, timeout=300)
            
            return {
                "status": "success" if result.returncode == 0 else "failed",
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def test_performance_optimization(self) -> Dict[str, Any]:
        """Test performance optimization system"""
        print("⚡ Testing performance optimization...")
        
        try:
            # Test performance endpoints
            endpoints = [
                "/health",
                "/api/consciousness/state",
                "/api/insights/consciousness",
                "/api/quantum/processors"
            ]
            
            results = {}
            for endpoint in endpoints:
                start_time = time.time()
                async with self.session.get(f"{self.base_url}{endpoint}") as response:
                    await response.text()
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000
                results[endpoint] = {
                    "response_time_ms": response_time,
                    "status_code": response.status,
                    "within_limits": response_time < 2000  # 2 second limit
                }
            
            return {
                "status": "success",
                "results": results,
                "all_within_limits": all(r["within_limits"] for r in results.values())
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def test_security_hardening(self) -> Dict[str, Any]:
        """Test security hardening features"""
        print("🔒 Testing security hardening...")
        
        try:
            # Test security headers
            async with self.session.get(f"{self.base_url}/health") as response:
                headers = dict(response.headers)
                
                security_headers = [
                    "x-content-type-options",
                    "x-frame-options",
                    "x-xss-protection",
                    "strict-transport-security"
                ]
                
                present_headers = [h for h in security_headers if h in headers]
                
                return {
                    "status": "success",
                    "security_headers_present": len(present_headers),
                    "security_headers_expected": len(security_headers),
                    "headers": {h: headers.get(h) for h in present_headers}
                }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def test_monitoring_observability(self) -> Dict[str, Any]:
        """Test monitoring and observability system"""
        print("📊 Testing monitoring and observability...")
        
        try:
            # Test monitoring endpoints
            monitoring_endpoints = [
                "/health",
                "/health/detailed",
                "/metrics",
                "/ready",
                "/live"
            ]
            
            results = {}
            for endpoint in monitoring_endpoints:
                async with self.session.get(f"{self.base_url}{endpoint}") as response:
                    data = await response.text()
                    results[endpoint] = {
                        "status_code": response.status,
                        "accessible": response.status == 200,
                        "has_content": len(data) > 0
                    }
            
            return {
                "status": "success",
                "results": results,
                "all_accessible": all(r["accessible"] for r in results.values())
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def test_load_testing(self) -> Dict[str, Any]:
        """Test load testing capabilities"""
        print("🏋️ Testing load testing capabilities...")
        
        try:
            # Run quick load test
            result = subprocess.run([
                sys.executable, "scripts/load_test.py", "--quick"
            ], capture_output=True, text=True, timeout=120)
            
            return {
                "status": "success" if result.returncode == 0 else "failed",
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def test_documentation_deployment(self) -> Dict[str, Any]:
        """Test documentation and deployment readiness"""
        print("📚 Testing documentation and deployment...")
        
        try:
            # Check if required files exist
            required_files = [
                "docs/PRODUCTION_DEPLOYMENT_GUIDE.md",
                "scripts/deploy_production.sh",
                "scripts/load_test.py",
                "backend/tests/test_production_readiness.py",
                "backend/core/performance_optimizer.py",
                "backend/core/security_framework.py",
                "backend/core/monitoring_system.py"
            ]
            
            existing_files = []
            missing_files = []
            
            for file_path in required_files:
                if os.path.exists(file_path):
                    existing_files.append(file_path)
                else:
                    missing_files.append(file_path)
            
            return {
                "status": "success" if len(missing_files) == 0 else "partial",
                "existing_files": len(existing_files),
                "missing_files": len(missing_files),
                "missing": missing_files
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def run_comprehensive_integration(self):
        """Run comprehensive Phase 5 integration test"""
        print("🚀 Starting Phase 5 Integration Testing")
        print("=" * 60)
        
        start_time = time.time()
        
        # Test all Phase 5 components
        tests = [
            ("Comprehensive Testing", self.test_comprehensive_testing),
            ("Performance Optimization", self.test_performance_optimization),
            ("Security Hardening", self.test_security_hardening),
            ("Monitoring & Observability", self.test_monitoring_observability),
            ("Load Testing", self.test_load_testing),
            ("Documentation & Deployment", self.test_documentation_deployment)
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            print(f"\n🔍 Running {test_name}...")
            try:
                result = await test_func()
                results[test_name] = result
                
                if result["status"] == "success":
                    print(f"✅ {test_name}: PASSED")
                elif result["status"] == "partial":
                    print(f"⚠️  {test_name}: PARTIAL")
                else:
                    print(f"❌ {test_name}: FAILED")
                    if "error" in result:
                        print(f"   Error: {result['error']}")
            except Exception as e:
                print(f"❌ {test_name}: ERROR - {e}")
                results[test_name] = {"status": "error", "error": str(e)}
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Generate report
        self.generate_integration_report(results, total_time)
        
        return results
    
    def generate_integration_report(self, results: Dict[str, Any], total_time: float):
        """Generate comprehensive integration report"""
        print("\n" + "=" * 60)
        print("📊 PHASE 5 INTEGRATION REPORT")
        print("=" * 60)
        
        # Summary statistics
        total_tests = len(results)
        passed_tests = len([r for r in results.values() if r.get("status") == "success"])
        partial_tests = len([r for r in results.values() if r.get("status") == "partial"])
        failed_tests = len([r for r in results.values() if r.get("status") in ["failed", "error"]])
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Partial: {partial_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests / total_tests * 100):.1f}%")
        print(f"Total Time: {total_time:.2f} seconds")
        print()
        
        # Detailed results
        for test_name, result in results.items():
            status = result.get("status", "unknown")
            status_icon = {
                "success": "✅",
                "partial": "⚠️",
                "failed": "❌",
                "error": "💥"
            }.get(status, "❓")
            
            print(f"{status_icon} {test_name}: {status.upper()}")
            
            if status == "error" and "error" in result:
                print(f"   Error: {result['error']}")
            elif status == "partial" and "missing" in result:
                print(f"   Missing: {', '.join(result['missing'])}")
        
        print()
        
        # Overall assessment
        if passed_tests == total_tests:
            print("🎉 ALL TESTS PASSED - Phase 5 Integration Complete!")
            print("✅ Mainza AI is ready for production deployment")
        elif passed_tests + partial_tests == total_tests:
            print("⚠️  MOSTLY SUCCESSFUL - Some components need attention")
            print("🔧 Review partial results and address missing components")
        else:
            print("❌ INTEGRATION ISSUES DETECTED")
            print("🚨 Review failed tests and resolve issues before production")
        
        # Save results
        self.save_integration_results(results, total_time)
    
    def save_integration_results(self, results: Dict[str, Any], total_time: float):
        """Save integration results to file"""
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "total_time_seconds": total_time,
            "results": results,
            "summary": {
                "total_tests": len(results),
                "passed": len([r for r in results.values() if r.get("status") == "success"]),
                "partial": len([r for r in results.values() if r.get("status") == "partial"]),
                "failed": len([r for r in results.values() if r.get("status") in ["failed", "error"]])
            }
        }
        
        with open("phase5_integration_report.json", "w") as f:
            json.dump(report_data, f, indent=2)
        
        print(f"📁 Integration report saved to phase5_integration_report.json")

async def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Phase 5 Integration Testing")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL to test")
    parser.add_argument("--quick", action="store_true", help="Run quick integration test")
    
    args = parser.parse_args()
    
    async with Phase5Integration(args.url) as integrator:
        if args.quick:
            print("🏃 Running quick Phase 5 integration test...")
            # Run only critical tests
            await integrator.test_performance_optimization()
            await integrator.test_security_hardening()
            await integrator.test_monitoring_observability()
        else:
            await integrator.run_comprehensive_integration()

if __name__ == "__main__":
    asyncio.run(main())
