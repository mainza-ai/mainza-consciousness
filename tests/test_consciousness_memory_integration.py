#!/usr/bin/env python3
"""
Test script for consciousness-memory integration functionality
"""
import asyncio
import logging
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.utils.consciousness_orchestrator import ConsciousnessOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_consciousness_memory_integration():
    """Test the consciousness-memory integration functionality"""
    
    print("🧪 Testing Consciousness-Memory Integration")
    print("=" * 50)
    
    try:
        # Initialize consciousness orchestrator
        orchestrator = ConsciousnessOrchestrator()
        
        # Initialize consciousness system
        await orchestrator.initialize_consciousness()
        print("✅ Consciousness system initialized")
        
        # Test consciousness-memory integration
        test_results = await orchestrator.test_consciousness_memory_integration()
        
        print("\n📊 Test Results:")
        print("-" * 30)
        
        for test_name, result in test_results.items():
            if test_name.endswith("_test"):
                status_emoji = "✅" if result == "passed" else "❌"
                print(f"{status_emoji} {test_name.replace('_', ' ').title()}: {result}")
        
        print(f"\n🎯 Overall Status: {test_results.get('overall_status', 'unknown')}")
        
        if test_results.get('test_memory_id'):
            print(f"📝 Test Memory ID: {test_results['test_memory_id']}")
        
        if test_results.get('retrieved_memories_count', 0) > 0:
            print(f"🔍 Retrieved Memories: {test_results['retrieved_memories_count']}")
        
        if test_results.get('alignment_score'):
            print(f"🎯 Alignment Score: {test_results['alignment_score']:.3f}")
        
        # Test consciousness cycle with memory integration
        print("\n🔄 Testing Consciousness Cycle with Memory Integration")
        print("-" * 50)
        
        cycle_result = await orchestrator.consciousness_cycle()
        
        print(f"✅ Consciousness cycle completed")
        print(f"   - Previous Level: {cycle_result.previous_consciousness_level:.3f}")
        print(f"   - Updated Level: {cycle_result.updated_consciousness_level:.3f}")
        print(f"   - Delta: {cycle_result.consciousness_delta:+.3f}")
        print(f"   - Processes: {len(cycle_result.processes_executed)}")
        print(f"   - Significance: {cycle_result.significance_score:.3f}")
        
        if cycle_result.proactive_actions:
            print(f"   - Proactive Actions: {len(cycle_result.proactive_actions)}")
            for action in cycle_result.proactive_actions:
                action_type = action.get('action_type', 'unknown')
                print(f"     • {action_type}")
        
        print("\n🎉 Consciousness-Memory Integration Test Completed Successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_consciousness_memory_integration())
    sys.exit(0 if success else 1)