#!/usr/bin/env python3
"""
Test script to verify comprehensive throttling event logging
"""

import asyncio
import logging
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Configure logging to see all levels
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Verify environment variables are loaded
print(f"NEO4J_PASSWORD loaded: {'✅' if os.getenv('NEO4J_PASSWORD') else '❌'}")
print(f"OLLAMA_BASE_URL: {os.getenv('OLLAMA_BASE_URL', 'Not set')}")
print(f"DEFAULT_OLLAMA_MODEL: {os.getenv('DEFAULT_OLLAMA_MODEL', 'Not set')}")
print()

async def test_throttling_logging():
    """Test throttling event logging functionality"""
    
    print("🧪 Testing Throttling Event Logging")
    print("=" * 50)
    
    try:
        # Import the functions we need to test
        from backend.agentic_router import extract_response_from_result, generate_throttled_response
        
        # Test 1: Throttled response detection and logging
        print("\n📋 Test 1: Throttled Response Detection")
        print("-" * 30)
        
        throttled_result = {
            "status": "throttled",
            "response": "I'm currently processing other requests. Please try again in a moment."
        }
        
        consciousness_context = {
            "user_id": "test-user-123",
            "consciousness_level": 0.8,
            "emotional_state": "curious"
        }
        
        query = "Hello, how are you today?"
        
        print(f"Input Query: {query}")
        print(f"Throttled Result: {throttled_result}")
        print(f"Consciousness Context: {consciousness_context}")
        print("\nProcessing...")
        
        response = extract_response_from_result(throttled_result, query, consciousness_context)
        
        print(f"\nExtracted Response: {response}")
        print("✅ Test 1 Complete")
        
        # Test 2: Direct throttled response generation
        print("\n📋 Test 2: Direct Throttled Response Generation")
        print("-" * 30)
        
        base_message = "System is busy processing multiple requests"
        
        print(f"Input Query: {query}")
        print(f"Base Message: {base_message}")
        print(f"Consciousness Context: {consciousness_context}")
        print("\nGenerating...")
        
        throttled_response = generate_throttled_response(query, consciousness_context, base_message)
        
        print(f"\nGenerated Response: {throttled_response}")
        print("✅ Test 2 Complete")
        
        # Test 3: Different query types
        print("\n📋 Test 3: Different Query Types")
        print("-" * 30)
        
        test_queries = [
            "What is artificial intelligence?",
            "Can you help me with my project?",
            "Hi there!",
            "How does machine learning work?"
        ]
        
        for i, test_query in enumerate(test_queries, 1):
            print(f"\nSubtest 3.{i}: {test_query}")
            
            # Test with different emotional states
            test_context = consciousness_context.copy()
            test_context["emotional_state"] = ["curious", "excited", "contemplative", "empathetic"][i-1]
            
            response = generate_throttled_response(test_query, test_context)
            print(f"Response: {response}")
        
        print("✅ Test 3 Complete")
        
        # Test 4: Error conditions
        print("\n📋 Test 4: Error Conditions")
        print("-" * 30)
        
        # Test with None result
        print("Subtest 4.1: None result")
        none_response = extract_response_from_result(None, query, consciousness_context)
        print(f"None Response: {none_response}")
        
        # Test with empty dict
        print("\nSubtest 4.2: Empty dict result")
        empty_dict_response = extract_response_from_result({}, query, consciousness_context)
        print(f"Empty Dict Response: {empty_dict_response}")
        
        # Test with malformed result
        print("\nSubtest 4.3: Malformed result")
        malformed_result = {"unexpected": "data", "no_response": True}
        malformed_response = extract_response_from_result(malformed_result, query, consciousness_context)
        print(f"Malformed Response: {malformed_response}")
        
        print("✅ Test 4 Complete")
        
        print("\n🎉 All Throttling Logging Tests Completed Successfully!")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_throttling_logging())
    sys.exit(0 if success else 1)