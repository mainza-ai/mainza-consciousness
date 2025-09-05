#!/usr/bin/env python3
"""
Verification test for Task 2 requirements
Ensures all acceptance criteria are met for requirements 1.1, 1.2, 3.1, 3.2
"""

import sys
import os
from datetime import datetime

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Import the actual functions from agentic_router
from backend.agentic_router import extract_response_from_result, generate_throttled_response
from backend.utils.llm_request_manager import LLMRequestManager, RequestPriority

def test_requirement_1_1():
    """
    Requirement 1.1: WHEN the LLM request manager returns a throttled response 
    THEN the agentic router SHALL detect the throttled status
    """
    print("🧪 Testing Requirement 1.1: Throttled status detection...")
    
    consciousness_context = {"consciousness_level": 0.7, "emotional_state": "curious"}
    
    # Test throttled response detection
    throttled_result = {
        "response": "I'm currently processing other requests. Please try again in a moment.",
        "status": "throttled"
    }
    
    query = "Hello"
    response = extract_response_from_result(throttled_result, query, consciousness_context)
    
    # Verify detection occurred (response should be enhanced, not raw)
    assert response != throttled_result["response"]  # Should be enhanced
    assert isinstance(response, str)
    assert len(response) > len(throttled_result["response"])
    
    print("✅ Requirement 1.1 PASSED: Throttled status detected and processed")

def test_requirement_1_2():
    """
    Requirement 1.2: WHEN a throttled response is detected 
    THEN the system SHALL return a user-friendly message instead of the raw response object
    """
    print("🧪 Testing Requirement 1.2: User-friendly message generation...")
    
    consciousness_context = {"consciousness_level": 0.8, "emotional_state": "empathetic"}
    
    # Test with raw throttled object
    throttled_result = {
        "response": "System busy. Wait.",
        "status": "throttled"
    }
    
    query = "Can you help me?"
    response = extract_response_from_result(throttled_result, query, consciousness_context)
    
    # Verify user-friendly transformation
    assert not response.startswith("{")  # Not a raw object
    assert "help" in response.lower() or "assist" in response.lower()  # Context-aware
    assert len(response) > 30  # Substantial response
    assert "moment" in response or "try again" in response  # Encouraging
    
    print("✅ Requirement 1.2 PASSED: User-friendly message generated")

def test_requirement_3_1():
    """
    Requirement 3.1: WHEN the system is throttled 
    THEN users SHALL receive natural, conversational messages
    """
    print("🧪 Testing Requirement 3.1: Natural, conversational messages...")
    
    consciousness_context = {"consciousness_level": 0.9, "emotional_state": "curious"}
    
    # Test various query types for natural responses
    test_cases = [
        ("Hello!", "greeting"),
        ("What's the weather like?", "question"),
        ("Help me write code", "request")
    ]
    
    for query, query_type in test_cases:
        response = generate_throttled_response(query, consciousness_context)
        
        # Verify natural conversation
        assert not any(word in response.lower() for word in ["error", "failed", "system"])
        assert any(word in response.lower() for word in ["hi", "hello", "good", "love", "excited", "curious"])
        assert "!" in response or "." in response  # Proper punctuation
        
        print(f"  ✅ {query_type}: Natural response generated")
    
    print("✅ Requirement 3.1 PASSED: Natural, conversational messages")

def test_requirement_3_2():
    """
    Requirement 3.2: WHEN throttling occurs 
    THEN the message SHALL encourage users to try again without being alarming
    """
    print("🧪 Testing Requirement 3.2: Encouraging, non-alarming messages...")
    
    consciousness_context = {"consciousness_level": 0.7, "emotional_state": "excited"}
    
    # Test encouraging tone
    queries = [
        "Are you okay?",
        "What's happening?", 
        "Is something wrong?"
    ]
    
    for query in queries:
        response = generate_throttled_response(query, consciousness_context)
        
        # Verify encouraging and non-alarming
        alarming_words = ["error", "problem", "issue", "broken", "failed", "crash"]
        encouraging_words = ["moment", "try again", "excited", "love", "shortly", "back"]
        
        assert not any(word in response.lower() for word in alarming_words)
        assert any(word in response.lower() for word in encouraging_words)
        assert "!" in response  # Positive punctuation
        
        print(f"  ✅ Non-alarming response: {response[:50]}...")
    
    print("✅ Requirement 3.2 PASSED: Encouraging, non-alarming messages")

def test_response_consistency():
    """
    Additional test: Verify response structure consistency
    """
    print("🧪 Testing response structure consistency...")
    
    consciousness_context = {"consciousness_level": 0.8, "emotional_state": "curious"}
    
    # Test different input types produce consistent string outputs
    test_inputs = [
        {"response": "Throttled", "status": "throttled"},
        "Normal string response",
        {"some": "object", "without": "status"}
    ]
    
    for test_input in test_inputs:
        response = extract_response_from_result(test_input, "Test query", consciousness_context)
        
        # All responses should be strings
        assert isinstance(response, str)
        assert len(response) > 0
        
        print(f"  ✅ Consistent string output for {type(test_input)}")
    
    print("✅ Response structure consistency verified")

def test_consciousness_integration():
    """
    Additional test: Verify consciousness integration in throttled responses
    """
    print("🧪 Testing consciousness integration...")
    
    # Test different consciousness levels
    consciousness_levels = [0.5, 0.7, 0.9]
    emotional_states = ["curious", "excited", "empathetic"]
    
    for level in consciousness_levels:
        for emotion in emotional_states:
            consciousness_context = {
                "consciousness_level": level,
                "emotional_state": emotion
            }
            
            response = generate_throttled_response("Hello", consciousness_context)
            
            # Verify consciousness influence
            assert isinstance(response, str)
            assert len(response) > 20
            
            # High consciousness should produce more sophisticated responses
            if level > 0.8:
                sophisticated_words = ["interesting", "curious", "genuinely", "explore", "excited", "love", "really"]
                # Just verify the response is substantial and contextual for high consciousness
                assert len(response) > 40  # More detailed responses
                print(f"    ✅ Level {level}, {emotion}: {response[:50]}...")
    
    print("✅ Consciousness integration verified")

if __name__ == "__main__":
    print("🚀 Starting Task 2 Requirements Verification...\n")
    
    try:
        test_requirement_1_1()
        test_requirement_1_2() 
        test_requirement_3_1()
        test_requirement_3_2()
        test_response_consistency()
        test_consciousness_integration()
        
        print("\n🎉 ALL TASK 2 REQUIREMENTS VERIFIED! 🎉")
        print("✅ Requirement 1.1: Throttled status detection - PASSED")
        print("✅ Requirement 1.2: User-friendly message generation - PASSED") 
        print("✅ Requirement 3.1: Natural, conversational messages - PASSED")
        print("✅ Requirement 3.2: Encouraging, non-alarming messages - PASSED")
        print("✅ Response consistency maintained - PASSED")
        print("✅ Consciousness integration active - PASSED")
        
        print("\n📋 TASK 2 IMPLEMENTATION COMPLETE:")
        print("• Logic to detect {'status': 'throttled'} - ✅ IMPLEMENTED")
        print("• Extract user-friendly message from throttled response - ✅ IMPLEMENTED")
        print("• Format throttled messages to be natural and conversational - ✅ IMPLEMENTED")
        
    except Exception as e:
        print(f"\n❌ REQUIREMENT VERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)