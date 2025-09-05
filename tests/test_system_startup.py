"""
Test System Startup for Ollama-Native Environment
Validates that all critical imports work without Redis or other external dependencies
"""
import sys
import traceback
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_critical_imports():
    """Test all critical imports that were failing"""
    
    critical_imports = [
        # Core modules
        ("backend.core.performance_optimization", "PerformanceOptimizer"),
        ("backend.core.enhanced_error_handling", "ErrorHandler"),
        
        # Configuration modules
        ("backend.config.llm_optimization", "llm_context_optimizer"),
        ("backend.agentic_config", "local_llm"),
        
        # Agent modules
        ("backend.agents.graphmaster", "graphmaster_agent"),
        ("backend.agentic_router", "router"),
        
        # Consciousness modules
        ("backend.utils.consciousness_orchestrator", "consciousness_orchestrator"),
        
        # New dynamic knowledge modules
        ("backend.utils.dynamic_knowledge_manager", "dynamic_knowledge_manager"),
        ("backend.utils.consciousness_driven_updates", "consciousness_driven_updater"),
        ("backend.utils.knowledge_graph_maintenance", "knowledge_graph_maintenance"),
        ("backend.utils.agent_knowledge_integration", "agent_knowledge_integrator"),
    ]
    
    failed_imports = []
    successful_imports = []
    
    for module_name, import_name in critical_imports:
        try:
            logger.info(f"Testing import: {module_name}.{import_name}")
            module = __import__(module_name, fromlist=[import_name])
            getattr(module, import_name)
            successful_imports.append((module_name, import_name))
            logger.info(f"✅ {module_name}.{import_name} - SUCCESS")
        except Exception as e:
            failed_imports.append((module_name, import_name, str(e)))
            logger.error(f"❌ {module_name}.{import_name} - FAILED: {e}")
    
    return successful_imports, failed_imports

def test_main_import():
    """Test the main backend import that was failing"""
    try:
        logger.info("Testing main backend import...")
        from backend.main import app
        logger.info("✅ Main backend import - SUCCESS")
        return True
    except Exception as e:
        logger.error(f"❌ Main backend import - FAILED: {e}")
        traceback.print_exc()
        return False

def test_compatibility_layer():
    """Test the Ollama-native compatibility layer"""
    try:
        logger.info("Testing Ollama-native compatibility layer...")
        from backend.utils.ollama_native_compatibility import get_compatibility_info, is_ollama_native_mode
        
        info = get_compatibility_info()
        logger.info(f"Compatibility mode: {info['mode']}")
        logger.info(f"Cache strategy: {info['cache_strategy']}")
        logger.info(f"Embedding strategy: {info['embedding_strategy']}")
        
        logger.info("✅ Compatibility layer - SUCCESS")
        return True
    except Exception as e:
        logger.error(f"❌ Compatibility layer - FAILED: {e}")
        return False

def main():
    """Run all startup tests"""
    logger.info("🚀 Starting Ollama-Native System Startup Tests")
    logger.info("=" * 60)
    
    # Test compatibility layer first
    compat_success = test_compatibility_layer()
    
    # Test critical imports
    successful, failed = test_critical_imports()
    
    # Test main import
    main_success = test_main_import()
    
    # Report results
    logger.info("=" * 60)
    logger.info("STARTUP TEST RESULTS")
    logger.info("=" * 60)
    
    logger.info(f"✅ Compatibility Layer: {'PASSED' if compat_success else 'FAILED'}")
    logger.info(f"✅ Successful Imports: {len(successful)}")
    logger.info(f"❌ Failed Imports: {len(failed)}")
    logger.info(f"✅ Main Import: {'PASSED' if main_success else 'FAILED'}")
    
    if failed:
        logger.info("\nFAILED IMPORTS:")
        for module_name, import_name, error in failed:
            logger.info(f"  ❌ {module_name}.{import_name}: {error}")
    
    if successful:
        logger.info(f"\nSUCCESSFUL IMPORTS ({len(successful)}):")
        for module_name, import_name in successful[:5]:  # Show first 5
            logger.info(f"  ✅ {module_name}.{import_name}")
        if len(successful) > 5:
            logger.info(f"  ... and {len(successful) - 5} more")
    
    logger.info("=" * 60)
    
    overall_success = compat_success and len(failed) == 0 and main_success
    
    if overall_success:
        logger.info("🎉 ALL STARTUP TESTS PASSED")
        logger.info("🚀 System ready for Ollama-native deployment")
        logger.info("💡 No Redis dependencies - pure Ollama environment")
    else:
        logger.info("⚠️  SOME STARTUP TESTS FAILED")
        logger.info("🔧 Please fix the issues before deployment")
    
    logger.info("=" * 60)
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)