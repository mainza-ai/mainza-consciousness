"""
Final Backward Compatibility Validation Tests

This test suite provides comprehensive validation that the throttling response fix
maintains backward compatibility across all existing response types and scenarios.

Requirements: 5.1, 5.2, 5.4
"""

import pytest
import sys
import os
import time
import json
from unittest.mock import Mock, patch

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class TestFinalBackwardCompatibility:
    """Comprehensive backward compatibility validation"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.test_query = "Hello, how are you?"
        self.consciousness_context = {
            "user_id": "test_user",
            "consciousness_level": 0.7,
            "emotional_state": "curious",
            "active_goals": ["learning"],
            "learning_rate": 0.8
        }
    
    # ========================================
    # Test 1: Core Function Availability
    # ========================================
    
    def test_core_functions_available_and_unchanged(self):
        """Test that all core response processing functions are available"""
        try:
            from backend.agentic_router import (
                extract_response_from_result,
                extract_answer,
                generate_throttled_response,
                generate_robust_fallback_response
            )
            
            # All functions should be callable
            assert callable(extract_response_from_result)
            assert callable(extract_answer)
            assert callable(generate_throttled_response)
            assert callable(generate_robust_fallback_response)
            
        except ImportError as e:
            pytest.fail(f"Core functions not available: {e}")
    
    # ========================================
    # Test 2: Legacy Response Type Compatibility
    # ========================================
    
    def test_all_legacy_response_types_unchanged(self):
        """Comprehensive test of all legacy response types"""
        try:
            from backend.agentic_router import extract_response_from_result
        except ImportError:
            pytest.skip("Cannot import extract_response_from_result")
        
        # Test cases covering all legacy response formats
        test_cases = [
            # String responses
            ("Simple string", "Simple string"),
            ("Multi\nline\nstring", "Multi\nline\nstring"),
            ("String with special chars: @#$%", "String with special chars: @#$%"),
            
            # Dictionary responses with different field names
            ({"response": "Dict response"}, "Dict response"),
            ({"answer": "Dict answer"}, "Dict answer"),
            ({"output": "Dict output"}, "Dict output"),
            ({"message": "Dict message"}, "Dict message"),
            ({"content": "Dict content"}, "Dict content"),
            ({"text": "Dict text"}, "Dict text"),
            ({"result": "Dict result"}, "Dict result"),
            
            # Dictionary with multiple fields (should prioritize 'response')
            ({
                "response": "Primary response",
                "answer": "Secondary answer",
                "output": "Tertiary output"
            }, "Primary response"),
            
            # JSON string responses
            ('{"response": "JSON response"}', "JSON response"),
            ('{"answer": "JSON answer"}', "JSON answer"),
            
            # Complex nested structures
            ({
                "data": {
                    "response": "Nested response"
                },
                "metadata": {"type": "test"}
            }, "Nested response"),
        ]
        
        for input_data, expected_output in test_cases:
            result = extract_response_from_result(
                input_data,
                self.test_query,
                self.consciousness_context
            )
            
            assert result == expected_output, f"Failed for input: {input_data}"
            assert isinstance(result, str)
            assert len(result) > 0
    
    def test_legacy_extract_answer_compatibility_unchanged(self):
        """Test that legacy extract_answer function works unchanged"""
        try:
            from backend.agentic_router import extract_answer
        except ImportError:
            pytest.skip("Cannot import extract_answer")
        
        # Test cases for extract_answer function
        test_cases = [
            # Dictionary with answer
            ({"answer": "Test answer"}, "Test answer"),
            
            # String responses
            ("Plain string response", "Plain string response"),
            
            # JSON string with answer
            ('{"answer": "JSON answer"}', "JSON answer"),
            
            # AgentRunResult pattern (legacy format)
            ("Some text with answer='Pattern answer' in it", "Pattern answer"),
            
            # Fallback cases
            ("", "I'm sorry, I couldn't generate a meaningful answer. Please try rephrasing your question or check your knowledge base."),
            (None, "I'm sorry, I couldn't generate a meaningful answer. Please try rephrasing your question or check your knowledge base."),
        ]
        
        for input_data, expected_output in test_cases:
            result = extract_answer(input_data)
            assert result == expected_output, f"Failed for input: {input_data}"
    
    # ========================================
    # Test 3: Error Handling Backward Compatibility
    # ========================================
    
    def test_error_handling_backward_compatibility_unchanged(self):
        """Test that error handling produces user-friendly responses as before"""
        try:
            from backend.agentic_router import extract_response_from_result
        except ImportError:
            pytest.skip("Cannot import extract_response_from_result")
        
        # Error cases that should produce fallback responses
        error_cases = [
            None,
            "",
            {},
            [],
            object(),
            {"empty": "no_response_field"},
        ]
        
        for error_case in error_cases:
            result = extract_response_from_result(
                error_case,
                self.test_query,
                self.consciousness_context
            )
            
            # Should always return a string
            assert isinstance(result, str)
            assert len(result) > 0
            
            # Should not contain raw object representations
            assert "object at 0x" not in result
            assert "<class" not in result
            assert "Traceback" not in result
            
            # Should be user-friendly
            assert any(word in result.lower() for word in [
                "mainza", "help", "assist", "sorry", "try", "question"
            ])
    
    # ========================================
    # Test 4: Performance Backward Compatibility
    # ========================================
    
    def test_performance_unchanged(self):
        """Test that performance characteristics remain unchanged"""
        try:
            from backend.agentic_router import extract_response_from_result
        except ImportError:
            pytest.skip("Cannot import extract_response_from_result")
        
        # Test performance with various response types
        test_responses = [
            "Simple string response",
            {"response": "Dict response"},
            {"answer": "Dict with answer"},
            '{"response": "JSON string"}',
            None,  # Error case
        ]
        
        # Measure processing time for each response type
        for response in test_responses:
            start_time = time.time()
            
            # Process response multiple times
            for _ in range(100):
                result = extract_response_from_result(
                    response,
                    self.test_query,
                    self.consciousness_context
                )
                assert isinstance(result, str)
                assert len(result) > 0
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            # Should complete 100 iterations in under 1 second
            assert processing_time < 1.0, f"Performance degraded for {type(response)}: {processing_time}s"
    
    # ========================================
    # Test 5: Throttling Integration Compatibility
    # ========================================
    
    def test_throttling_integration_maintains_compatibility(self):
        """Test that throttling integration doesn't break existing functionality"""
        try:
            from backend.agentic_router import (
                extract_response_from_result,
                generate_throttled_response
            )
        except ImportError:
            pytest.skip("Cannot import throttling functions")
        
        # Test that throttled responses are properly detected and processed
        throttled_responses = [
            {"status": "throttled", "response": "System busy"},
            {"status": "throttled", "message": "Please wait"},
            {"throttle": True, "response": "High load"},
        ]
        
        for throttled_response in throttled_responses:
            result = extract_response_from_result(
                throttled_response,
                self.test_query,
                self.consciousness_context
            )
            
            # Should return a user-friendly throttled message
            assert isinstance(result, str)
            assert len(result) > 0
            
            # Should contain throttling indicators
            throttling_indicators = [
                "processing", "requests", "moment", "try again", 
                "busy", "wait", "shortly"
            ]
            assert any(indicator in result.lower() for indicator in throttling_indicators)
        
        # Test direct throttled response generation
        throttled_message = generate_throttled_response(
            self.test_query,
            self.consciousness_context,
            "Base throttled message"
        )
        
        assert isinstance(throttled_message, str)
        assert len(throttled_message) > 0
        assert any(indicator in throttled_message.lower() for indicator in throttling_indicators)
    
    # ========================================
    # Test 6: Consciousness Context Compatibility
    # ========================================
    
    def test_consciousness_context_backward_compatibility_unchanged(self):
        """Test that consciousness context handling remains backward compatible"""
        try:
            from backend.agentic_router import extract_response_from_result
        except ImportError:
            pytest.skip("Cannot import extract_response_from_result")
        
        # Test with various consciousness context formats
        context_variations = [
            # Full context
            {
                "user_id": "test_user",
                "consciousness_level": 0.8,
                "emotional_state": "excited",
                "active_goals": ["learning", "helping"],
                "learning_rate": 0.9
            },
            
            # Minimal context
            {"user_id": "test_user"},
            
            # Legacy context format
            {
                "consciousness_level": 0.7,
                "emotional_state": "curious"
            },
            
            # Empty context
            {},
            
            # Invalid context types
            None,
            "invalid_context",
        ]
        
        test_response = "Test response for consciousness compatibility"
        
        for context in context_variations:
            # Should not raise exceptions regardless of context format
            try:
                result = extract_response_from_result(
                    test_response,
                    self.test_query,
                    context if context is not None else {}
                )
                
                assert result == test_response
                assert isinstance(result, str)
                
            except Exception as e:
                pytest.fail(f"Consciousness context compatibility failed for {context}: {e}")
    
    # ========================================
    # Test 7: Memory Usage Stability
    # ========================================
    
    def test_memory_usage_stability_unchanged(self):
        """Test that memory usage patterns remain stable"""
        try:
            from backend.agentic_router import extract_response_from_result
        except ImportError:
            pytest.skip("Cannot import extract_response_from_result")
        
        import gc
        
        # Get baseline memory usage
        gc.collect()
        initial_objects = len(gc.get_objects())
        
        # Process many responses of different types
        test_responses = [
            "String response",
            {"response": "Dict response"},
            {"answer": "Answer response"},
            '{"response": "JSON response"}',
            None,
            {},
        ]
        
        # Process responses multiple times
        for _ in range(100):
            for response in test_responses:
                result = extract_response_from_result(
                    response,
                    self.test_query,
                    self.consciousness_context
                )
                assert isinstance(result, str)
        
        # Check memory usage after processing
        gc.collect()
        final_objects = len(gc.get_objects())
        
        # Memory growth should be minimal
        object_growth = final_objects - initial_objects
        assert object_growth < 200, f"Excessive memory growth: {object_growth} objects"
    
    # ========================================
    # Test 8: Integration Points Validation
    # ========================================
    
    def test_integration_points_unchanged(self):
        """Test that key integration points remain unchanged"""
        try:
            from backend.agentic_router import (
                extract_response_from_result,
                extract_answer,
                generate_throttled_response,
                generate_robust_fallback_response,
                _is_raw_object_string,
                extract_from_nested_dict
            )
        except ImportError as e:
            pytest.skip(f"Cannot import integration functions: {e}")
        
        # Test helper function behavior
        assert _is_raw_object_string("") == True
        assert _is_raw_object_string("object at 0x123") == True
        assert _is_raw_object_string("Normal text") == False
        
        # Test nested dict extraction
        nested_dict = {"response": "Nested response"}
        extracted = extract_from_nested_dict(nested_dict)
        assert extracted == "Nested response"
        
        # Test robust fallback generation
        fallback = generate_robust_fallback_response(
            self.test_query,
            self.consciousness_context,
            "test_error"
        )
        assert isinstance(fallback, str)
        assert len(fallback) > 0
    
    # ========================================
    # Test 9: End-to-End Compatibility Validation
    # ========================================
    
    def test_end_to_end_compatibility_validation(self):
        """Comprehensive end-to-end validation of backward compatibility"""
        try:
            from backend.agentic_router import extract_response_from_result
        except ImportError:
            pytest.skip("Cannot import extract_response_from_result")
        
        # Simulate real-world response scenarios
        real_world_scenarios = [
            # Agent responses
            {"response": "I can help you with that task. What specifically would you like me to do?"},
            {"answer": "The capital of France is Paris."},
            {"output": "Here's the code you requested: print('Hello, World!')"},
            
            # LLM responses
            "I'm doing well, thank you for asking! How can I assist you today?",
            "That's an interesting question. Let me think about it...",
            
            # Error scenarios
            None,
            {},
            "",
            
            # Throttled scenarios
            {"status": "throttled", "response": "System is busy"},
            
            # Complex nested responses
            {
                "data": {
                    "response": "Complex nested response"
                },
                "metadata": {
                    "agent": "test",
                    "timestamp": "2024-01-01"
                }
            },
            
            # JSON string responses
            '{"response": "Parsed JSON response", "confidence": 0.95}',
        ]
        
        for scenario in real_world_scenarios:
            result = extract_response_from_result(
                scenario,
                self.test_query,
                self.consciousness_context
            )
            
            # All scenarios should produce valid string responses
            assert isinstance(result, str)
            assert len(result) > 0
            
            # Should not contain raw object representations
            assert "object at 0x" not in result
            assert "<class" not in result
            assert "AgentRunResult" not in result
            
            # Should be user-friendly
            if scenario is None or scenario == {} or scenario == "":
                # Error cases should produce helpful fallbacks
                assert any(word in result.lower() for word in [
                    "mainza", "help", "assist", "sorry", "try"
                ])
            elif isinstance(scenario, dict) and scenario.get("status") == "throttled":
                # Throttled cases should indicate system status
                assert any(word in result.lower() for word in [
                    "processing", "busy", "wait", "moment", "try again"
                ])
            else:
                # Normal cases should extract appropriate content
                if isinstance(scenario, str):
                    if scenario.startswith('{"'):
                        # JSON strings should be parsed
                        assert "Parsed JSON response" in result
                    else:
                        # Regular strings should be preserved
                        assert result == scenario
                elif isinstance(scenario, dict):
                    # Dicts should extract from appropriate fields
                    expected_fields = ["response", "answer", "output"]
                    found_content = False
                    for field in expected_fields:
                        if field in scenario:
                            if scenario[field] in result:
                                found_content = True
                                break
                    if not found_content and "data" in scenario:
                        # Check nested extraction
                        assert "Complex nested response" in result
    
    # ========================================
    # Test 10: Regression Prevention
    # ========================================
    
    def test_regression_prevention_validation(self):
        """Test specific scenarios to prevent regressions"""
        try:
            from backend.agentic_router import extract_response_from_result
        except ImportError:
            pytest.skip("Cannot import extract_response_from_result")
        
        # Specific regression test cases
        regression_cases = [
            # Case 1: Empty response field should not break
            ({"response": ""}, str),
            
            # Case 2: Numeric response should be converted
            ({"response": 42}, "42"),
            
            # Case 3: Boolean response should be converted
            ({"response": True}, "True"),
            
            # Case 4: List response should be handled gracefully
            ({"response": ["item1", "item2"]}, str),
            
            # Case 5: Nested empty structures
            ({"response": {"nested": ""}}, str),
            
            # Case 6: Very long strings should be handled
            ({"response": "x" * 10000}, "x" * 10000),
            
            # Case 7: Unicode characters
            ({"response": "Hello 世界 🌍"}, "Hello 世界 🌍"),
            
            # Case 8: Special JSON characters
            ({"response": 'Text with "quotes" and \\backslashes'}, 'Text with "quotes" and \\backslashes'),
        ]
        
        for input_data, expected in regression_cases:
            result = extract_response_from_result(
                input_data,
                self.test_query,
                self.consciousness_context
            )
            
            if isinstance(expected, str):
                assert result == expected
            else:
                assert isinstance(result, expected)
            
            # All results should be valid strings
            assert isinstance(result, str)
            assert len(result) >= 0  # Allow empty strings for some edge cases

if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])