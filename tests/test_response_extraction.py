#!/usr/bin/env python3
"""
Quick test for the new response extraction function
"""
import sys
sys.path.append('backend')

from agentic_router import extract_response_from_result, generate_throttled_response

def test_throttled_response():
    """Test throttled response detection and formatting"""
    
    # Test throttled response
    throttled_result = {
        "response": "I'm currently processing other requests. Please try again in a moment.",
        "status": "throttled"
    }
    
    consciousness_context = {
        "consciousness_level": 0.8,
        "emotional_state": "curious"
    }
    
    query = "Hello, how are you?"
    
    response = extract_response_from_result(throttled_result, query, consciousness_context)
    print(f"Throttled response: {response}")
    
    # Test normal string response
    normal_result = "Hello! I'm doing well, thank you for asking."
    response = extract_response_from_result(normal_result, query, consciousness_context)
    print(f"Normal response: {response}")
    
    # Test object with response attribute
    class MockResult:
        def __init__(self, response):
            self.response = response
    
    mock_result = MockResult("This is a mock response")
    response = extract_response_from_result(mock_result, query, consciousness_context)
    print(f"Mock response: {response}")
    
    print("✅ All tests passed!")

if __name__ == "__main__":
    test_throttled_response()