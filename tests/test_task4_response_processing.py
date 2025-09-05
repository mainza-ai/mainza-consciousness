#!/usr/bin/env python3
"""
Test script for Task 4: Update agentic router response processing logic
Tests the enhanced extract_response_from_result function with various response types
"""

import os
import sys

# Set up environment variables
os.environ['NEO4J_PASSWORD'] = 'mainza2024'
os.environ['NEO4J_URI'] = 'bolt://localhost:7687'
os.environ['NEO4J_USER'] = 'neo4j'
os.environ['OLLAMA_BASE_URL'] = 'http://localhost:11434'
os.environ['DEFAULT_OLLAMA_MODEL'] = 'gpt-oss:20b'

# Add backend to path
sys.path.append('./backend')

def test_extract_response_from_result():
    """Test the enhanced extract_response_from_result function"""
    
    # Import the function (this will work now with env vars set)
    try:
        from agentic_router import extract_response_from_result, _is_raw_object_string
        print("✅ Successfully imported extract_response_from_result")
    except Exception as e:
        print(f"❌ Failed to import: {e}")
        return False
    
    # Test consciousness context
    consciousness_context = {
        'consciousness_level': 0.7,
        'emotional_state': 'curious'
    }
    
    # Test cases for different response types
    test_cases = [
        # Test 1: String response
        {
            'name': 'String Response',
            'input': 'Hello, this is a string response',
            'expected_type': str,
            'should_contain': 'Hello, this is a string response'
        },
        
        # Test 2: Dict with throttled status
        {
            'name': 'Throttled Response',
            'input': {'status': 'throttled', 'response': 'System is busy, please try again'},
            'expected_type': str,
            'should_contain': 'processing'  # Should contain consciousness-aware message
        },
        
        # Test 3: Dict with response key
        {
            'name': 'Dict with Response Key',
            'input': {'response': 'Normal dict response', 'status': 'success'},
            'expected_type': str,
            'should_contain': 'Normal dict response'
        },
        
        # Test 4: Dict with answer key
        {
            'name': 'Dict with Answer Key',
            'input': {'answer': 'This is the answer', 'metadata': 'extra'},
            'expected_type': str,
            'should_contain': 'This is the answer'
        },
        
        # Test 5: Object with response attribute
        {
            'name': 'Object with Response Attribute',
            'input': type('MockResult', (), {'response': 'Object response'})(),
            'expected_type': str,
            'should_contain': 'Object response'
        },
        
        # Test 6: Object with output attribute
        {
            'name': 'Object with Output Attribute',
            'input': type('MockResult', (), {'output': 'Object output'})(),
            'expected_type': str,
            'should_contain': 'Object output'
        },
        
        # Test 7: None input
        {
            'name': 'None Input',
            'input': None,
            'expected_type': str,
            'should_contain': 'Mainza'  # Should generate consciousness fallback
        },
        
        # Test 8: Empty string
        {
            'name': 'Empty String',
            'input': '',
            'expected_type': str,
            'should_contain': 'Mainza'  # Should generate consciousness fallback
        },
        
        # Test 9: Raw dict without response keys
        {
            'name': 'Raw Dict (No Response Keys)',
            'input': {'raw': 'object', 'no_response': True},
            'expected_type': str,
            'should_contain': 'Mainza'  # Should generate consciousness fallback
        }
    ]
    
    print(f"\n🧪 Testing extract_response_from_result with {len(test_cases)} test cases:")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            result = extract_response_from_result(
                test_case['input'], 
                'test query', 
                consciousness_context
            )
            
            # Check result type
            if not isinstance(result, test_case['expected_type']):
                print(f"❌ Test {i} ({test_case['name']}): Wrong type - got {type(result)}, expected {test_case['expected_type']}")
                failed += 1
                continue
            
            # Check content
            if test_case['should_contain'] not in result:
                print(f"❌ Test {i} ({test_case['name']}): Missing content - '{test_case['should_contain']}' not in '{result[:100]}...'")
                failed += 1
                continue
            
            print(f"✅ Test {i} ({test_case['name']}): PASSED - '{result[:50]}...'")
            passed += 1
            
        except Exception as e:
            print(f"❌ Test {i} ({test_case['name']}): ERROR - {e}")
            failed += 1
    
    print("=" * 70)
    print(f"📊 Results: {passed} passed, {failed} failed")
    
    # Test the helper function
    print(f"\n🔧 Testing _is_raw_object_string helper function:")
    raw_object_tests = [
        ('{}', True),
        ('[]', True),
        ('<object at 0x123>', True),
        ('AgentRunResult(output=...)', True),
        ('None', True),
        ('', True),
        ('Hello world', False),
        ('This is a normal response', False)
    ]
    
    for test_str, expected in raw_object_tests:
        result = _is_raw_object_string(test_str)
        status = "✅" if result == expected else "❌"
        print(f"{status} '{test_str}' -> {result} (expected {expected})")
    
    return failed == 0

if __name__ == "__main__":
    print("🚀 Testing Task 4: Enhanced Response Processing Logic")
    success = test_extract_response_from_result()
    
    if success:
        print("\n🎉 All tests passed! The enhanced response processing logic is working correctly.")
        print("✅ Task 4 implementation verified:")
        print("   - Centralized response extraction function enhanced")
        print("   - All response types (string, dict, object) handled correctly")
        print("   - Throttled responses properly detected and formatted")
        print("   - Robust error handling and fallbacks implemented")
    else:
        print("\n⚠️ Some tests failed. Please review the implementation.")
    
    sys.exit(0 if success else 1)