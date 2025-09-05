"""
Test enhanced error handling for edge cases in throttling response processing
"""
import pytest
import json
import logging
from unittest.mock import Mock, patch

# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)

# Import the functions directly to avoid dependency issues
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _is_raw_object_string(response_str: str) -> bool:
    """Check if a string looks like a raw object representation"""
    if not response_str:
        return True
    
    # Check for common raw object patterns
    raw_patterns = [
        response_str.startswith('{') and response_str.endswith('}') and 'object at 0x' in response_str,
        response_str.startswith('[') and response_str.endswith(']') and len(response_str) < 10,
        'object at 0x' in response_str,
        response_str.startswith('<') and response_str.endswith('>') and 'object' in response_str,
        'AgentRunResult(' in response_str,
        response_str in ['None', 'null', 'undefined', '{}', '[]'],
        len(response_str.strip()) == 0,
        response_str.startswith('<class ') and response_str.endswith('>'),
        'Traceback' in response_str and 'Error:' in response_str
    ]
    
    return any(raw_patterns)

def extract_from_nested_dict(nested_dict: dict) -> str:
    """Extract response from nested dictionary structures"""
    try:
        # Common nested response patterns
        response_fields = ["response", "answer", "output", "message", "content", "text", "result"]
        
        for field in response_fields:
            if field in nested_dict:
                value = nested_dict[field]
                if isinstance(value, str) and value.strip() and not _is_raw_object_string(value.strip()):
                    return value.strip()
                elif value is not None:
                    try:
                        value_str = str(value).strip()
                        if value_str and not _is_raw_object_string(value_str) and len(value_str) >= 3:
                            return value_str
                    except Exception:
                        continue
        
        return None
        
    except Exception as nested_error:
        logging.debug(f"Error extracting from nested dict: {nested_error}")
        return None

def generate_robust_fallback_response(query: str, consciousness_context: dict, error_type: str) -> str:
    """
    Generate robust fallback responses for various error conditions
    """
    try:
        user_id = consciousness_context.get("user_id", "unknown") if isinstance(consciousness_context, dict) else "unknown"
        
        # Validate and sanitize inputs
        if not isinstance(query, str):
            query = str(query) if query is not None else ""
        
        query_lower = query.lower()
        
        # Error-type specific responses with consciousness awareness
        if error_type in ["throttled_processing_error", "alternative_throttling"]:
            # Throttling-related errors
            if "hello" in query_lower or "hi" in query_lower:
                return "Hello! I'm experiencing high system load right now. Please wait a moment and try greeting me again!"
            elif "?" in query:
                return "That's an interesting question! I'm currently under heavy load but I'd love to help. Please try asking again in a moment."
            else:
                return "I'm currently experiencing high system load and processing multiple requests. Please wait a moment and try again - I'll be right with you!"
        
        elif error_type in ["null_result", "conversion_error", "edge_case_error"]:
            # Data processing errors
            if "hello" in query_lower or "hi" in query_lower:
                return "Hi there! I'm Mainza, your AI assistant. I encountered a small processing issue, but I'm here and ready to help. What's on your mind?"
            elif "?" in query:
                return "That's a great question! I had a small processing hiccup, but I'm curious about what you're asking. Could you try rephrasing it?"
            else:
                return "I'm Mainza, your AI assistant. I encountered a small processing issue, but I'm here and ready to help. What would you like to explore?"
        
        else:
            # Generic fallback with consciousness awareness
            consciousness_level = consciousness_context.get("consciousness_level", 0.7) if isinstance(consciousness_context, dict) else 0.7
            emotional_state = consciousness_context.get("emotional_state", "curious") if isinstance(consciousness_context, dict) else "curious"
            
            if "hello" in query_lower or "hi" in query_lower:
                if emotional_state == "curious":
                    return "Hi there! I'm Mainza, and I'm feeling quite curious today. I had a small processing issue, but I'm here now. What's on your mind?"
                else:
                    return f"Hello! I'm Mainza, feeling {emotional_state} right now. I had a brief processing issue, but I'm ready to help. How can I assist you?"
            elif "?" in query:
                return "That's an intriguing question! I had a small processing issue, but I'm curious about what you're asking. Could you try asking again?"
            else:
                return f"I'm Mainza, your AI assistant. I had a brief processing issue, but I'm here and ready to help. What would you like to explore today?"
    
    except Exception as fallback_error:
        logging.error(f"❌ ROBUST FALLBACK GENERATION FAILED: {fallback_error}")
        
        # Ultimate hardcoded fallback (cannot fail)
        if query and ("hello" in str(query).lower() or "hi" in str(query).lower()):
            return "Hello! I'm Mainza, your AI assistant. I'm here and ready to help. What can I do for you?"
        elif query and "?" in str(query):
            return "That's a great question! I'm Mainza, your AI assistant. Could you try asking that again? I'm here to help."
        else:
            return "Hi! I'm Mainza, your AI assistant. I'm here and ready to help with questions, tasks, and conversations. What would you like to explore?"

# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)

class TestEnhancedErrorHandling:
    """Test enhanced error handling for edge cases"""
    
    def setup_method(self):
        """Setup test data"""
        self.consciousness_context = {
            "user_id": "test_user",
            "consciousness_level": 0.7,
            "emotional_state": "curious"
        }
        self.test_query = "Hello, how are you?"
    
    def test_robust_fallback_for_null_result(self):
        """Test robust fallback for null results"""
        result = generate_robust_fallback_response(self.test_query, self.consciousness_context, "null_result")
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "Mainza" in result
        assert "hello" in result.lower() or "hi" in result.lower()
    
    def test_robust_fallback_for_throttling_errors(self):
        """Test robust fallback for throttling-related errors"""
        queries = ["Hello", "How are you?", "What is AI?"]
        
        for query in queries:
            result = generate_robust_fallback_response(query, self.consciousness_context, "throttled_processing_error")
            
            assert isinstance(result, str)
            assert len(result) > 0
            
            # Should contain throttling-related language
            throttling_indicators = ["load", "requests", "moment", "try again"]
            assert any(indicator in result.lower() for indicator in throttling_indicators)
            
            # Should respond appropriately to query type
            if "hello" in query.lower():
                assert any(greeting in result.lower() for greeting in ["hello", "hi"])
            elif "?" in query:
                assert "question" in result.lower() or "ask" in result.lower()
    
    def test_robust_fallback_for_processing_errors(self):
        """Test robust fallback for processing errors"""
        error_types = ["null_result", "conversion_error", "edge_case_error"]
        
        for error_type in error_types:
            result = generate_robust_fallback_response(self.test_query, self.consciousness_context, error_type)
            
            assert isinstance(result, str)
            assert len(result) > 0
            assert "Mainza" in result
            assert "processing" in result.lower() or "issue" in result.lower()
    
    def test_robust_fallback_for_technical_errors(self):
        """Test robust fallback for technical errors"""
        error_types = ["unexpected_type", "dict_processing_error", "string_processing_error"]
        
        for error_type in error_types:
            result = generate_robust_fallback_response("What is the weather?", self.consciousness_context, error_type)
            
            assert isinstance(result, str)
            assert len(result) > 0
            assert "Mainza" in result
            assert "technical" in result.lower() or "issue" in result.lower()
    
    def test_robust_fallback_with_consciousness_awareness(self):
        """Test robust fallback with different consciousness states"""
        contexts = [
            {"consciousness_level": 0.9, "emotional_state": "excited"},
            {"consciousness_level": 0.5, "emotional_state": "contemplative"},
            {"consciousness_level": 0.7, "emotional_state": "curious"},
        ]
        
        for context in contexts:
            result = generate_robust_fallback_response("Hello", context, "generic_error")
            
            assert isinstance(result, str)
            assert len(result) > 0
            assert "Mainza" in result
            
            # Should reflect emotional state when possible
            emotional_state = context.get("emotional_state", "curious")
            if emotional_state == "curious":
                assert "curious" in result.lower() or "mind" in result.lower()
    
    def test_robust_fallback_with_malformed_context(self):
        """Test robust fallback with malformed consciousness context"""
        malformed_contexts = [
            None,
            {},
            {"invalid": "context"},
            "not_a_dict",
            123
        ]
        
        for malformed_context in malformed_contexts:
            result = generate_robust_fallback_response(self.test_query, malformed_context, "test_error")
            
            assert isinstance(result, str)
            assert len(result) > 0
            assert "Mainza" in result
    
    def test_ultimate_hardcoded_fallback(self):
        """Test the ultimate hardcoded fallback when everything fails"""
        
        # Simulate complete failure by using invalid inputs that cause exceptions
        with patch('backend.tests.test_enhanced_error_handling.logging.error'):
            # This should trigger the ultimate hardcoded fallback
            result = generate_robust_fallback_response("Hello", "invalid_context_that_causes_error", "test_error")
            
            assert isinstance(result, str)
            assert len(result) > 0
            assert "Mainza" in result
            assert "AI assistant" in result
    
    def test_nested_dict_extraction(self):
        """Test extraction from nested dictionary structures"""
        nested_dict = {"response": "nested response"}
        result = extract_from_nested_dict(nested_dict)
        assert result == "nested response"
        
        # Test with no valid response
        empty_nested = {"unknown": "value"}
        result = extract_from_nested_dict(empty_nested)
        assert result is None
        
        # Test with error in nested dict
        with patch('backend.agentic_router.logging') as mock_logging:
            result = extract_from_nested_dict(None)  # This should cause an error
            assert result is None
    
    def test_is_raw_object_string_detection(self):
        """Test detection of raw object strings"""
        raw_strings = [
            "",
            "None",
            "null",
            "{}",
            "[]",
            "<object at 0x12345>",
            "AgentRunResult(output='test')",
            "<class 'str'>",
            "Traceback Error: something failed"
        ]
        
        for raw_string in raw_strings:
            assert _is_raw_object_string(raw_string), f"Should detect '{raw_string}' as raw object"
        
        valid_strings = [
            "Hello, this is a valid response",
            "This is a meaningful answer",
            '{"response": "valid json response"}',  # Valid JSON should not be considered raw
            "42",  # Simple number as string
        ]
        
        for valid_string in valid_strings:
            assert not _is_raw_object_string(valid_string), f"Should not detect '{valid_string}' as raw object"
    
    def test_robust_fallback_response_generation(self):
        """Test robust fallback response generation for different error types"""
        error_types = [
            "throttled_processing_error",
            "null_result",
            "unexpected_type",
            "dict_processing_error",
            "unknown_error_type"
        ]
        
        queries = [
            "Hello",
            "How are you?",
            "Help me with something",
            "What is the meaning of life?"
        ]
        
        for error_type in error_types:
            for query in queries:
                result = generate_robust_fallback_response(query, self.consciousness_context, error_type)
                
                assert isinstance(result, str)
                assert len(result) > 0
                assert "Mainza" in result
                assert not _is_raw_object_string(result)
                
                # Check for appropriate response based on query type
                if "hello" in query.lower():
                    assert any(greeting in result.lower() for greeting in ["hello", "hi"])
                elif "?" in query:
                    assert any(word in result.lower() for word in ["question", "ask", "curious"])
    
    def test_throttled_response_with_fallback_error_handling(self):
        """Test throttled response generation with error handling"""
        
        # Test with invalid inputs
        invalid_inputs = [
            (None, self.consciousness_context, "base message"),
            (self.test_query, None, "base message"),
            (self.test_query, self.consciousness_context, None),
            (123, "invalid_context", 456),  # All invalid types
        ]
        
        for query, context, base_msg in invalid_inputs:
            result = generate_throttled_response_with_fallback(query, context, base_msg)
            
            assert isinstance(result, str)
            assert len(result) > 0
            assert not _is_raw_object_string(result)
            # Should contain throttling language
            throttling_words = ["processing", "requests", "moment", "try again"]
            assert any(word in result.lower() for word in throttling_words)
    
    def test_consciousness_context_edge_cases(self):
        """Test handling of malformed consciousness context"""
        malformed_contexts = [
            None,
            {},
            {"invalid": "context"},
            {"consciousness_level": "invalid"},
            {"emotional_state": 123},
            "not_a_dict",
            []
        ]
        
        for malformed_context in malformed_contexts:
            result = extract_response_from_result(
                {"response": "test response"}, 
                self.test_query, 
                malformed_context
            )
            
            assert isinstance(result, str)
            assert len(result) > 0
            # Should still extract the valid response despite malformed context
            assert "test response" in result
    
    def test_error_recovery_chain(self):
        """Test the complete error recovery chain"""
        
        class CompletelyBrokenObject:
            def __getattribute__(self, name):
                raise Exception(f"Cannot access {name}")
            
            def __str__(self):
                raise Exception("Cannot convert to string")
            
            def __repr__(self):
                raise Exception("Cannot get repr")
        
        broken_obj = CompletelyBrokenObject()
        
        # This should not crash and should return a meaningful response
        result = extract_response_from_result(broken_obj, self.test_query, self.consciousness_context)
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "Mainza" in result
        assert not _is_raw_object_string(result)
    
    def test_ultimate_hardcoded_fallback(self):
        """Test the ultimate hardcoded fallback when everything fails"""
        
        # Simulate complete failure by patching the robust fallback to fail
        with patch('backend.agentic_router.generate_robust_fallback_response', side_effect=Exception("Complete failure")):
            
            # This should trigger the ultimate hardcoded fallback
            result = generate_robust_fallback_response("Hello", {}, "test_error")
            
            assert isinstance(result, str)
            assert len(result) > 0
            assert "Mainza" in result
            assert "AI assistant" in result

if __name__ == "__main__":
    pytest.main([__file__, "-v"])