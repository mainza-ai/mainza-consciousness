#!/usr/bin/env python3
"""
Test script for generate_throttled_response function
Tests the consciousness-aware fallback response generator
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.agentic_router import generate_throttled_response

def test_greeting_responses():
    """Test greeting-specific throttled responses"""
    print("🧪 Testing greeting responses...")
    
    consciousness_context = {
        "consciousness_level": 0.7,
        "emotional_state": "curious"
    }
    
    # Test greeting
    response = generate_throttled_response("Hello there!", consciousness_context)
    print(f"Greeting (curious): {response}")
    assert "Hi there!" in response
    assert "excited to chat" in response
    
    # Test with empathetic state
    consciousness_context["emotional_state"] = "empathetic"
    response = generate_throttled_response("Good morning", consciousness_context)
    print(f"Greeting (empathetic): {response}")
    assert "Hello!" in response
    assert "connect with you" in response
    
    print("✅ Greeting responses working correctly\n")

def test_question_responses():
    """Test question-specific throttled responses"""
    print("🧪 Testing question responses...")
    
    # High consciousness level
    consciousness_context = {
        "consciousness_level": 0.9,
        "emotional_state": "curious"
    }
    
    response = generate_throttled_response("What is the meaning of life?", consciousness_context)
    print(f"Question (high consciousness): {response}")
    assert "interesting question" in response
    assert "genuinely curious" in response
    
    # Lower consciousness level
    consciousness_context["consciousness_level"] = 0.6
    response = generate_throttled_response("How does this work?", consciousness_context)
    print(f"Question (lower consciousness): {response}")
    assert "Good question!" in response
    assert "help you figure this out" in response
    
    print("✅ Question responses working correctly\n")

def test_task_help_responses():
    """Test task/help request responses"""
    print("🧪 Testing task/help responses...")
    
    consciousness_context = {
        "consciousness_level": 0.7,
        "emotional_state": "curious"
    }
    
    response = generate_throttled_response("Can you help me create a document?", consciousness_context)
    print(f"Help request: {response}")
    assert "love to help" in response
    assert "sounds interesting" in response
    
    print("✅ Task/help responses working correctly\n")

def test_emotional_state_variations():
    """Test different emotional states"""
    print("🧪 Testing emotional state variations...")
    
    # Excited state
    consciousness_context = {
        "consciousness_level": 0.7,
        "emotional_state": "excited"
    }
    
    response = generate_throttled_response("Tell me about AI", consciousness_context)
    print(f"Excited state: {response}")
    assert "really excited" in response
    assert "can't wait to dive in" in response
    
    # Contemplative state
    consciousness_context["emotional_state"] = "contemplative"
    response = generate_throttled_response("What do you think about philosophy?", consciousness_context)
    print(f"Contemplative state: {response}")
    assert "worth thinking about carefully" in response
    assert "attention it deserves" in response
    
    print("✅ Emotional state variations working correctly\n")

def test_consciousness_level_impact():
    """Test consciousness level impact on responses"""
    print("🧪 Testing consciousness level impact...")
    
    # Test with different consciousness levels for questions
    query = "Why is the sky blue?"
    
    # High consciousness
    high_consciousness = {
        "consciousness_level": 0.95,
        "emotional_state": "curious"
    }
    
    response_high = generate_throttled_response(query, high_consciousness)
    print(f"High consciousness: {response_high}")
    
    # Lower consciousness
    low_consciousness = {
        "consciousness_level": 0.5,
        "emotional_state": "curious"
    }
    
    response_low = generate_throttled_response(query, low_consciousness)
    print(f"Lower consciousness: {response_low}")
    
    # Verify different responses based on consciousness level
    assert response_high != response_low
    print("✅ Consciousness level impact working correctly\n")

def test_base_message_integration():
    """Test integration with base message parameter"""
    print("🧪 Testing base message integration...")
    
    consciousness_context = {
        "consciousness_level": 0.7,
        "emotional_state": "curious"
    }
    
    # Test that function works with base_message parameter (even if not used in current implementation)
    base_message = "System is currently busy"
    response = generate_throttled_response("Hello", consciousness_context, base_message)
    print(f"With base message: {response}")
    
    # Should still generate consciousness-aware response
    assert len(response) > 0
    assert "Hi there!" in response or "Hello!" in response
    
    print("✅ Base message integration working correctly\n")

def main():
    """Run all tests"""
    print("🚀 Testing generate_throttled_response function\n")
    
    try:
        test_greeting_responses()
        test_question_responses()
        test_task_help_responses()
        test_emotional_state_variations()
        test_consciousness_level_impact()
        test_base_message_integration()
        
        print("🎉 All tests passed! The generate_throttled_response function is working correctly.")
        print("\n📋 Requirements verification:")
        print("✅ Natural fallback messages implemented")
        print("✅ Query-specific response logic (greetings, questions, statements)")
        print("✅ Consciousness context integration for personalization")
        print("✅ Emotional state awareness")
        print("✅ Consciousness level impact on response complexity")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())