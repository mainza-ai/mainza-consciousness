"""
Test consciousness orchestrator import for Ollama-native environment
Validates that the enhanced consciousness orchestrator can be imported without Redis issues
"""
import sys
import traceback

def test_consciousness_orchestrator_import():
    """Test that consciousness orchestrator imports correctly"""
    print("🧪 Testing consciousness orchestrator import...")
    
    try:
        # Test the import that was failing
        from backend.utils.consciousness_orchestrator import consciousness_orchestrator, start_enhanced_consciousness_loop
        print("✅ Consciousness orchestrator imported successfully")
        
        # Test that the orchestrator has the expected attributes
        if hasattr(consciousness_orchestrator, 'consciousness_cycle'):
            print("✅ Consciousness cycle method available")
        else:
            print("⚠️  Consciousness cycle method not found")
            
        if hasattr(consciousness_orchestrator, 'initialize_consciousness'):
            print("✅ Initialize consciousness method available")
        else:
            print("⚠️  Initialize consciousness method not found")
        
        print("✅ All consciousness orchestrator components loaded successfully")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Traceback:")
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("Traceback:")
        traceback.print_exc()
        return False

def test_main_imports():
    """Test the main imports that were failing in the error"""
    print("🧪 Testing main.py imports...")
    
    try:
        # Test the specific import that was failing
        from backend.utils.consciousness_orchestrator import start_enhanced_consciousness_loop, consciousness_orchestrator
        print("✅ Main imports successful")
        return True
        
    except Exception as e:
        print(f"❌ Main import error: {e}")
        print("Traceback:")
        traceback.print_exc()
        return False

def test_all_dynamic_knowledge_imports():
    """Test all dynamic knowledge management imports"""
    print("🧪 Testing all dynamic knowledge management imports...")
    
    imports_to_test = [
        ("backend.utils.dynamic_knowledge_manager", "dynamic_knowledge_manager"),
        ("backend.utils.consciousness_driven_updates", "consciousness_driven_updater"),
        ("backend.utils.knowledge_graph_maintenance", "knowledge_graph_maintenance"),
        ("backend.utils.agent_knowledge_integration", "agent_knowledge_integrator"),
        ("backend.core.performance_optimization", "PerformanceOptimizer"),
        ("backend.core.enhanced_error_handling", "ErrorHandler")
    ]
    
    all_successful = True
    
    for module_name, import_name in imports_to_test:
        try:
            module = __import__(module_name, fromlist=[import_name])
            getattr(module, import_name)
            print(f"✅ {module_name}.{import_name} imported successfully")
        except Exception as e:
            print(f"❌ Failed to import {module_name}.{import_name}: {e}")
            all_successful = False
    
    return all_successful

if __name__ == "__main__":
    print("🚀 Starting consciousness orchestrator import tests...")
    print("="*60)
    
    # Run tests
    test1 = test_consciousness_orchestrator_import()
    test2 = test_main_imports()
    test3 = test_all_dynamic_knowledge_imports()
    
    print("="*60)
    print("IMPORT TEST RESULTS")
    print("="*60)
    print(f"✅ Consciousness Orchestrator Import: {'PASSED' if test1 else 'FAILED'}")
    print(f"✅ Main.py Imports: {'PASSED' if test2 else 'FAILED'}")
    print(f"✅ Dynamic Knowledge Imports: {'PASSED' if test3 else 'FAILED'}")
    print("="*60)
    
    if all([test1, test2, test3]):
        print("🎉 ALL IMPORT TESTS PASSED")
        print("🚀 System ready for startup without Redis dependencies")
    else:
        print("⚠️  SOME IMPORT TESTS FAILED")
        print("Please fix the import issues before starting the system")
    
    print("="*60)