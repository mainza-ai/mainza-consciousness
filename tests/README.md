# Mainza AI Test Suite

This directory contains comprehensive tests for the Mainza AI consciousness framework, updated to reflect all recent system changes including Docker optimization, LLM improvements, and insights dashboard enhancements.

## 🧪 Test Categories

### **Core System Tests**
- `test_system_comprehensive_updated.py` - **MAIN TEST RUNNER** - Comprehensive system test with all recent updates
- `test_system_comprehensive.py` - Original comprehensive system test
- `test_system_startup.py` - System startup and initialization tests
- `test_server_startup.py` - Server startup validation

### **API & Endpoint Tests**
- `test_api_endpoints.py` - API endpoint definitions and availability
- `test_frontend_backend_comprehensive.py` - Frontend-backend integration tests
- `test_backend_frontend_integration.py` - Backend-frontend data flow tests

### **Consciousness System Tests**
- `test_consciousness_system.py` - Core consciousness functionality
- `test_consciousness_insights.py` - Consciousness insights and analytics
- `test_consciousness_memory_integration.py` - Memory system integration
- `test_consciousness_orchestrator_import.py` - Consciousness orchestrator tests

### **LLM & Optimization Tests**
- `test_llm_optimization.py` - **UPDATED** - LLM optimization and throttling tests
- `test_llm_response_truncation.py` - Response truncation handling
- `test_generate_throttled_response.py` - Throttled response generation
- `test_throttling_integration.py` - Throttling system integration
- `test_throttling_performance.py` - Throttling performance tests

### **Docker & Build System Tests**
- `test_docker_build_system.py` - **NEW** - Docker build system and verification tests
- Tests for build scripts, Dockerfile optimizations, and verification tools

### **Insights Dashboard Tests**
- `test_insights_dashboard_updates.py` - **NEW** - Insights dashboard updates and UI improvements
- `test_insights_system.py` - Insights system functionality
- Tests for development status badges, tab classification, and UI contrast improvements

### **Agent System Tests**
- `test_agent_execution.py` - Agent execution and coordination
- `test_enhanced_agent_integration.py` - Enhanced agent integration
- `test_simple_chat_agent.py` - Simple chat agent functionality

### **Memory System Tests**
- `test_memory_system_monitoring.py` - Memory system monitoring and health
- Tests for memory performance, error handling, and recovery

### **Error Handling & Fixes Tests**
- `test_critical_error_fixes.py` - Critical error fixes validation
- `test_additional_critical_fixes.py` - Additional critical fixes
- `test_final_critical_fixes.py` - Final critical fixes
- `test_enhanced_error_handling_integration.py` - Enhanced error handling
- `test_null_safety_fixes.py` - Null safety fixes
- `test_runtime_error_fixes.py` - Runtime error fixes
- `test_syntax_fixes.py` - Syntax fixes validation

### **Integration & Performance Tests**
- `test_context_optimization.py` - Context optimization tests
- `test_dynamic_knowledge_management.py` - Dynamic knowledge management
- `test_enhanced_knowledge_integration.py` - Enhanced knowledge integration
- `test_ollama_native_fixes.py` - Ollama native integration fixes

## 🚀 Quick Start

### **Run Main Test Suite**
```bash
# Run the comprehensive updated test suite
python tests/test_system_comprehensive_updated.py

# Run specific test categories
python tests/test_docker_build_system.py
python tests/test_insights_dashboard_updates.py
python tests/test_llm_optimization.py
```

### **Run Backend Tests**
```bash
# Run backend-specific tests
cd backend
python -m pytest tests/
```

### **Run Frontend Integration Tests**
```bash
# Ensure backend is running first
python tests/test_frontend_backend_comprehensive.py
```

## 📊 Test Coverage

### **System Components Tested**
- ✅ **Docker Build System** - Build scripts, verification, optimization
- ✅ **LLM Optimization** - Request management, throttling, caching
- ✅ **Insights Dashboard** - UI updates, badges, tab classification
- ✅ **Consciousness System** - State management, emotional intelligence
- ✅ **Memory System** - Storage, retrieval, lifecycle management
- ✅ **API Endpoints** - All REST endpoints including new build info
- ✅ **Frontend Integration** - React components, data flow
- ✅ **Error Handling** - Comprehensive error management
- ✅ **Performance** - Response times, system health

### **Recent Updates Tested**
- ✅ **Docker Optimization** - 96% build context reduction, cache busting
- ✅ **LLM Request Management** - Priority queues, background throttling
- ✅ **Development Status Badges** - Tab classification system
- ✅ **UI Contrast Improvements** - Dark theme consistency
- ✅ **Build Info Endpoints** - Container verification system
- ✅ **Frontend Port Changes** - Port 80 configuration
- ✅ **Polling Optimization** - Reduced frontend polling intervals

## 🔧 Test Requirements

### **Prerequisites**
- Docker and Docker Compose running
- Backend service on `http://localhost:8000`
- Frontend service on `http://localhost` (port 80)
- Neo4j database accessible
- Ollama service running

### **Environment Setup**
```bash
# Start all services
./scripts/build-dev.sh

# Verify services are running
./scripts/verify-changes.sh

# Run tests
python tests/test_system_comprehensive_updated.py
```

## 📈 Test Results

### **Expected Pass Rates**
- **System Tests**: 100% pass rate
- **API Tests**: 100% pass rate  
- **Integration Tests**: 95%+ pass rate
- **Performance Tests**: 90%+ pass rate

### **Performance Benchmarks**
- **API Response Time**: < 1 second
- **Frontend Load Time**: < 3 seconds
- **Docker Build Time**: < 5 minutes
- **Memory Usage**: < 2GB

## 🐛 Troubleshooting

### **Common Issues**
1. **Backend Not Running**: Check Docker services with `docker-compose ps`
2. **Frontend Not Accessible**: Verify port 80 is not blocked
3. **Test Failures**: Check service logs with `docker-compose logs`
4. **Build Issues**: Run `./scripts/build-dev.sh` to rebuild

### **Debug Commands**
```bash
# Check service status
docker-compose ps

# View service logs
docker-compose logs -f

# Verify build info
curl http://localhost:8000/build/info

# Check frontend
curl http://localhost
```

## 📝 Test Maintenance

### **Adding New Tests**
1. Create test file in appropriate category
2. Follow naming convention: `test_[feature]_[aspect].py`
3. Include comprehensive error handling
4. Add to main test runner if needed
5. Update this README

### **Updating Existing Tests**
1. Update test expectations for system changes
2. Verify test still covers intended functionality
3. Update documentation if test scope changes
4. Run full test suite to ensure no regressions

## 🎯 Test Goals

### **Primary Objectives**
- Ensure system stability and reliability
- Validate all recent system changes
- Maintain high code quality standards
- Provide comprehensive coverage
- Enable confident deployment

### **Quality Metrics**
- **Coverage**: 95%+ of critical paths
- **Reliability**: 99%+ test pass rate
- **Performance**: Meet all benchmarks
- **Maintainability**: Clear, documented tests

---

**Last Updated**: December 7, 2024  
**Test Suite Version**: 2.1.0  
**Maintainer**: Mainza AI Development Team
