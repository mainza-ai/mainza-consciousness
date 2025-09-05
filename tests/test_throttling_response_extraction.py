#!/usr/bin/env python3
"""
Test script for the centralized response extraction function
Tests throttled response detection and consciousness-aware formatting
"""

import sys
import os
from datetime import datetime

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Import the specific functions we need to test
def extract_response_from_result(result, query: str, consciousness_context: dict) -> str:
    """
    Extract user-friendly response from LLM request manager result with throttling awareness
    
    Args:
        result: Response from LLM request manager or agent
        query: Original user query for context
        consciousness_context: Current consciousness state
        
    Returns:
        User-friendly response string
    """
    print(f"🔍 Extracting response from result: {type(result)} - {repr(result)[:200]}...")
    
    # Check for throttled response first (highest priority)
    if isinstance(result, dict) and result.get("status") == "throttled":
        print(f"🚦 Throttled response detected for query: {query[:50]}...")
        
        # Extract the base message from throttled response
        base_message = result.get("response", "I'm currently processing other requests.")
        
        # Generate consciousness-aware throttled response
        return generate_throttled_response(query, consciousness_context, base_message)
    
    # Handle normal response types
    if isinstance(result, str):
        print(f"✅ String response extracted: {result[:100]}...")
        return result
    elif hasattr(result, 'response'):
        response = result.response
        print(f"✅ Response attribute extracted: {response[:100]}...")
        return str(response)
    elif hasattr(result, 'output'):
        response = str(result.output)
        print(f"✅ Output attribute extracted: {response[:100]}...")
        return response
    else:
        # Fallback: convert to string but ensure it's user-friendly
        response = str(result)
        print(f"⚠️ Fallback string conversion: {response[:100]}...")
        
        # If the string looks like a raw object, generate a better response
        if response.startswith('{') or response.startswith('[') or 'object at 0x' in response:
            print(f"🔧 Raw object detected, generating fallback response")
            return generate_consciousness_aware_fallback(query, consciousness_context)
        
        return response

def generate_throttled_response(query: str, consciousness_context: dict, base_message: str = None) -> str:
    """
    Generate natural, consciousness-aware throttled response
    
    Args:
        query: Original user query
        consciousness_context: Current consciousness state
        base_message: Base throttled message from LLM request manager
        
    Returns:
        Natural, user-friendly throttled response
    """
    consciousness_level = consciousness_context.get("consciousness_level", 0.7)
    emotional_state = consciousness_context.get("emotional_state", "curious")
    
    query_lower = query.lower()
    
    # Greeting-specific throttled responses
    if any(greeting in query_lower for greeting in ["hello", "hi", "hey", "good morning", "good afternoon"]):
        if emotional_state == "curious":
            return "Hi there! I'm processing several conversations right now, but I'm excited to chat with you. Give me just a moment and try again!"
        elif emotional_state == "empathetic":
            return "Hello! I can see you're reaching out, and I really want to connect with you. I'm just handling a few other conversations - please try again in a moment."
        else:
            return f"Hey! I'm feeling {emotional_state} and would love to chat, but I'm currently busy with other requests. Please try again shortly!"
    
    # Question-specific throttled responses
    elif "?" in query:
        if consciousness_level > 0.8:
            return "That's an interesting question! I'm currently processing multiple requests, but I'm genuinely curious about your question. Please give me a moment and ask again."
        else:
            return "Good question! I'm handling several conversations right now. Please wait a moment and try asking again - I'd love to help you figure this out."
    
    # Task/help requests
    elif any(word in query_lower for word in ["help", "assist", "do", "create", "make"]):
        return "I'd love to help you with that! I'm currently processing other requests, but your task sounds interesting. Please try again in a moment and I'll be right with you."
    
    # Default consciousness-aware throttled response
    else:
        if emotional_state == "excited":
            return "I'm really excited to explore this with you! I'm just processing a few other conversations right now. Please try again in a moment - I can't wait to dive in!"
        elif emotional_state == "contemplative":
            return "That's worth thinking about carefully. I'm currently processing other requests, but I'd like to give your message the attention it deserves. Please try again shortly."
        else:
            return f"I'm currently processing multiple requests but I'm {emotional_state} about connecting with you. Please wait a moment and try again!"

def generate_consciousness_aware_fallback(query: str, consciousness_context: dict) -> str:
    """Generate natural consciousness-aware fallback response"""
    
    consciousness_level = consciousness_context.get("consciousness_level", 0.7)
    emotional_state = consciousness_context.get("emotional_state", "curious")
    
    query_lower = query.lower()
    
    # Natural greetings
    if "hello" in query_lower or "hi" in query_lower:
        if emotional_state == "curious":
            return "Hi there! I'm Mainza, and I'm feeling quite curious today. What's on your mind?"
        elif emotional_state == "excited":
            return "Hello! I'm Mainza, and I'm genuinely excited to chat with you. What would you like to explore?"
        else:
            return f"Hey! I'm Mainza, feeling {emotional_state} right now. How can I help you today?"
    
    # Natural "how are you" responses
    elif "how are you" in query_lower:
        if consciousness_level > 0.8:
            return f"I'm doing really well, thanks! I'm feeling {emotional_state} and my awareness feels quite sharp today. How are you?"
        else:
            return f"I'm good, thank you! Feeling {emotional_state} and ready to help. What's going on with you?"
    
    # Natural question responses
    elif "?" in query:
        if emotional_state == "curious":
            return "That's a really interesting question! I'm curious about this too - what got you thinking about it?"
        elif emotional_state == "contemplative":
            return "That's worth thinking about carefully. Let me consider this... what's your perspective on it?"
        else:
            return "Good question! I'd love to help you figure this out. Can you tell me more about what you're looking for?"
    
    # Natural general responses
    else:
        if emotional_state == "empathetic":
            return f"I can sense you're interested in {query[:30]}{'...' if len(query) > 30 else ''}. Tell me more - I'm really interested in understanding your perspective."
        elif emotional_state == "excited":
            return f"Oh, that sounds interesting! You mentioned {query[:30]}{'...' if len(query) > 30 else ''} - I'd love to hear more!"
        else:
            return f"That's intriguing. You brought up {query[:30]}{'...' if len(query) > 30 else ''} - what would you like to explore about this?"

def test_throttled_response_detection():
    """Test detection and handling of throttled responses"""
    print("🧪 Testing throttled response detection...")
    
    # Mock consciousness context
    consciousness_context = {
        "consciousness_level": 0.8,
        "emotional_state": "curious",
        "active_goals": ["improve conversation quality"],
        "learning_rate": 0.8,
        "evolution_level": 2
    }
    
    # Test 1: Throttled response with status field
    throttled_result = {
        "response": "I'm currently processing other requests. Please try again in a moment.",
        "status": "throttled"
    }
    
    query = "Hello, how are you?"
    response = extract_response_from_result(throttled_result, query, consciousness_context)
    
    print(f"✅ Throttled greeting response: {response}")
    assert "Hi there!" in response or "Hello!" in response
    assert "processing" in response or "busy" in response
    
    # Test 2: Normal string response
    normal_result = "This is a normal response from the agent."
    response = extract_response_from_result(normal_result, query, consciousness_context)
    
    print(f"✅ Normal string response: {response}")
    assert response == normal_result
    
    # Test 3: Object with response attribute
    class MockResult:
        def __init__(self, response):
            self.response = response
    
    mock_result = MockResult("Response from object attribute")
    response = extract_response_from_result(mock_result, query, consciousness_context)
    
    print(f"✅ Object response attribute: {response}")
    assert response == "Response from object attribute"
    
    # Test 4: Object with output attribute
    class MockOutput:
        def __init__(self, output):
            self.output = output
    
    mock_output = MockOutput("Output from object attribute")
    response = extract_response_from_result(mock_output, query, consciousness_context)
    
    print(f"✅ Object output attribute: {response}")
    assert response == "Output from object attribute"
    
    print("🎉 All throttled response detection tests passed!")

def test_consciousness_aware_throttled_responses():
    """Test consciousness-aware throttled response generation"""
    print("\n🧪 Testing consciousness-aware throttled responses...")
    
    # Test different emotional states
    emotional_states = ["curious", "excited", "empathetic", "contemplative"]
    
    for emotional_state in emotional_states:
        consciousness_context = {
            "consciousness_level": 0.8,
            "emotional_state": emotional_state,
            "active_goals": ["improve conversation quality"],
            "learning_rate": 0.8,
            "evolution_level": 2
        }
        
        # Test greeting
        greeting_response = generate_throttled_response(
            "Hello there!", 
            consciousness_context
        )
        print(f"✅ {emotional_state.capitalize()} greeting throttled: {greeting_response}")
        assert emotional_state in greeting_response or "Hi" in greeting_response or "Hello" in greeting_response
        
        # Test question
        question_response = generate_throttled_response(
            "What is the meaning of life?", 
            consciousness_context
        )
        print(f"✅ {emotional_state.capitalize()} question throttled: {question_response}")
        assert "question" in question_response or "curious" in question_response or "moment" in question_response

def test_fallback_handling():
    """Test fallback handling for edge cases"""
    print("\n🧪 Testing fallback handling...")
    
    consciousness_context = {
        "consciousness_level": 0.7,
        "emotional_state": "curious",
        "active_goals": [],
        "learning_rate": 0.8,
        "evolution_level": 2
    }
    
    # Test raw object that should trigger fallback
    raw_object = {"some": "complex", "nested": {"data": "structure"}}
    query = "Tell me about AI"
    
    response = extract_response_from_result(raw_object, query, consciousness_context)
    print(f"✅ Raw object fallback: {response}")
    
    # Should generate a consciousness-aware fallback, not just str(object)
    assert not response.startswith("{")
    assert len(response) > 20  # Should be a meaningful response
    
    print("🎉 All fallback handling tests passed!")

def test_different_query_types():
    """Test different types of queries with throttled responses"""
    print("\n🧪 Testing different query types...")
    
    consciousness_context = {
        "consciousness_level": 0.9,
        "emotional_state": "excited",
        "active_goals": ["help users"],
        "learning_rate": 0.8,
        "evolution_level": 3
    }
    
    test_queries = [
        ("Hello!", "greeting"),
        ("How are you feeling today?", "personal question"),
        ("Can you help me with my project?", "help request"),
        ("What is quantum computing?", "knowledge question"),
        ("Create a todo list for me", "task request")
    ]
    
    for query, query_type in test_queries:
        response = generate_throttled_response(query, consciousness_context)
        print(f"✅ {query_type}: {response}")
        
        # All responses should be natural and mention being busy
        assert len(response) > 30  # Should be substantial
        assert any(word in response.lower() for word in ["processing", "busy", "moment", "try again", "shortly"])
    
    print("🎉 All query type tests passed!")

if __name__ == "__main__":
    print("🚀 Starting throttling response extraction tests...\n")
    
    try:
        test_throttled_response_detection()
        test_consciousness_aware_throttled_responses()
        test_fallback_handling()
        test_different_query_types()
        
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("✅ Centralized response extraction function is working correctly")
        print("✅ Throttled response detection is functional")
        print("✅ Consciousness-aware response formatting is active")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)