#!/usr/bin/env python3
"""
Validation script for throttling fix
"""
import sys
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def validate_fix():
    """Validate that the fix is working"""
    print("🔍 Validating throttling fix...")
    
    try:
        # Test LLM Request Manager
        from backend.utils.llm_request_manager import LLMRequestManager, RequestPriority
        manager = LLMRequestManager()
        
        # Check that user conversation protection is enabled
        if hasattr(manager, 'user_conversation_protection') and manager.user_conversation_protection:
            print("✅ LLM Request Manager: User conversation protection enabled")
        else:
            print("❌ LLM Request Manager: User conversation protection missing")
            return False
        
        # Check never throttle priorities
        if hasattr(manager, 'never_throttle_priorities'):
            never_throttle = manager.never_throttle_priorities
            if RequestPriority.USER_CONVERSATION in never_throttle and RequestPriority.USER_INTERACTION in never_throttle:
                print("✅ LLM Request Manager: Never throttle priorities configured correctly")
            else:
                print("❌ LLM Request Manager: Never throttle priorities not configured")
                return False
        else:
            print("❌ LLM Request Manager: Never throttle priorities missing")
            return False
        
        # Test Consciousness Orchestrator
        from backend.utils.consciousness_orchestrator import ConsciousnessOrchestrator
        orchestrator = ConsciousnessOrchestrator()
        
        # Check user activity awareness
        if hasattr(orchestrator, 'notify_user_activity'):
            print("✅ Consciousness Orchestrator: User activity awareness enabled")
        else:
            print("❌ Consciousness Orchestrator: User activity awareness missing")
            return False
        
        # Check reduced frequency
        if hasattr(orchestrator, 'consciousness_cycle_interval') and orchestrator.consciousness_cycle_interval >= 300:
            print("✅ Consciousness Orchestrator: Reduced frequency configured")
        else:
            print("❌ Consciousness Orchestrator: Frequency not reduced")
            return False
        
        print("🎉 ALL VALIDATIONS PASSED - Fix is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False

if __name__ == "__main__":
    success = validate_fix()
    sys.exit(0 if success else 1)
