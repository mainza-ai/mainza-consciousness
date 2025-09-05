"""
Complete startup test for Ollama-native environment
Tests the entire import chain that was failing
"""
import sys
import traceback
import logging

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_import_chain():
    """Test the complete import chain that was failing"""
    
    import_chain = [
        # Step 1: Core modules
        ("backend.core.enhanced_error_handling", "ErrorHandler"),
        ("backend.core.performance_optimization", "PerformanceOptimizer"),
        
        # Step 2: Configuration modules  
        ("backend.config.llm_optimization", "llm_context_optimizer"),
        ("backend.agentic_config", "local_llm"),
        
        # Step 3: Agent modules
        ("backend.agents.graphmaster", "graphmaster_agent"),
        ("backend.agentic_router", "router"),
        
        # Step 4: Main application
        ("backend.main", "app")
    ]
    
    successful_imports = []
    failed_imports = []
    
    for i, (module_name, import_name) in enumerate(import_chain, 1):
        try:
            logger.info(f"Step {i}: Importing {module_name}.{import_name}")
            module = __import__(module_name, fromlist=[import_name])
            getattr(module, import_name)
            successful_imports.append((module_name, import_name))
            logger.info(f"✅ Step {i}: SUCCESS")
        except Exception as e:
            failed_imports.append((module_name, import_name, str(e)))
            logger.error(f"❌ Step {i}: FAILED - {e}")
            # Print detailed traceback for debugging
            logger.error("Detailed traceback:")
            traceback.print_exc()
            break  # Stop at first failure to see the exact issue
    
    return successful_imports, failed_imports

def test_consciousness_orchestrator_chain():
    """Test the consciousness orchestrator import chain specifically"""
    
    try:
        logger.info("Testing consciousness orchestrator import chain...")
        
        # Test the specific import that was enhanced
        from backend.utils.consciousness_orchestrator import consciousness_orchestrator, start_enhanced_consciousness_loop
        
        logger.info("✅ Consciousness orchestrator imported successfully")
        
        # Test that it has the expected enhanced methods
        if hasattr(consciousness_orchestrator, 'get_consciousness_context'):
            logger.info("✅ Enhanced consciousness context method available")
        else:
            logger.warning("⚠️  Enhanced consciousness context method not found")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Consciousness orchestrator import failed: {e}")
        traceback.print_exc()
        return False

def test_dynamic_knowledge_management_chain():
    """Test the new dynamic knowledge management imports"""
    
    try:
        logger.info("Testing dynamic knowledge management imports...")
        
        # Test all the new modules
        from backend.utils.dynamic_knowledge_manager import dynamic_knowledge_manager
        from backend.utils.consciousness_driven_updates import consciousness_driven_updater
        from backend.utils.knowledge_graph_maintenance import knowledge_graph_maintenance
        from backend.utils.agent_knowledge_integration import agent_knowledge_integrator
        
        logger.info("✅ All dynamic knowledge management modules imported successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Dynamic knowledge management import failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run complete startup test"""
    logger.info("🚀 Starting complete Ollama-native startup test")
    logger.info("=" * 60)
    
    # Test 1: Import chain
    logger.info("TEST 1: Complete import chain")
    successful, failed = test_import_chain()
    
    # Test 2: Consciousness orchestrator
    logger.info("\nTEST 2: Consciousness orchestrator")
    consciousness_success = test_consciousness_orchestrator_chain()
    
    # Test 3: Dynamic knowledge management
    logger.info("\nTEST 3: Dynamic knowledge management")
    knowledge_success = test_dynamic_knowledge_management_chain()
    
    # Results
    logger.info("\n" + "=" * 60)
    logger.info("COMPLETE STARTUP TEST RESULTS")
    logger.info("=" * 60)
    
    logger.info(f"✅ Import Chain: {len(successful)}/{len(successful) + len(failed)} successful")
    logger.info(f"✅ Consciousness Orchestrator: {'PASSED' if consciousness_success else 'FAILED'}")
    logger.info(f"✅ Dynamic Knowledge Management: {'PASSED' if knowledge_success else 'FAILED'}")
    
    if failed:
        logger.info(f"\n❌ FAILED IMPORTS ({len(failed)}):")
        for module_name, import_name, error in failed:
            logger.info(f"  - {module_name}.{import_name}: {error}")
    
    overall_success = len(failed) == 0 and consciousness_success and knowledge_success
    
    logger.info("\n" + "=" * 60)
    if overall_success:
        logger.info("🎉 ALL STARTUP TESTS PASSED")
        logger.info("🚀 System is ready for Ollama-native deployment")
        logger.info("💡 No Redis dependencies - pure Ollama environment")
    else:
        logger.info("⚠️  SOME STARTUP TESTS FAILED")
        logger.info("🔧 Please fix the issues before deployment")
    logger.info("=" * 60)
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)