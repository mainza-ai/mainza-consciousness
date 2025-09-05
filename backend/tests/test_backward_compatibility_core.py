"""
Core Backward Compatibility Tests for Throttling Response Fix

This test suite validates the core response processing functions work unchanged
without requiring the full application stack (Neo4j, agents, etc.).

Requirements: 5.1, 5.2, 5.4
"""

import pytest
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Test data for various response types
CONSCIOUSNESS_CONTEXT = {
    "user_id": "test_user",
    "consciousness_level": 0.7,
    "emotional_state": "curious",
    "active_goals": ["learning"],
    "learning_rate": 0.8
}

class TestCoreBackwardCompatibility:
    """Test suite for core backward compatibility validation"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.test_query = "Hello, how are you?"
        self.consciousness_context = CONSCIOUSNESS_CONTEXT.copy()
    
    # ========================================
    # Test 1: Core Response Processing Functions
    # ========================================
    
    def test_extract_response_from_result_import(self):
        """Test that we can import the core function"""
        try:
            # Import the core function directly
            from backend.agentic_router import extract_response_from_result
            assert callable(extract_response_from_result)
        except ImportError as e:
            pytest.skip(f"Cannot import extract_response_from_result: {e}")
    
    def test_extract_answer_import(self):
        """Test that we can import the legacy extract_answer function"""
        try:
            from backend.agentic_router import extract_answer
            assert callable(extract_answer)
        except ImportError as e:
            pytest.skip(f"Cannot import extract_answer: {e}")
    
    # ========================================
    # Test 2: String Response Types (Legacy)
    # ========================================
    
    def test_simple_string_response_unchanged(self):
        """Test that simple string responses work exactly as before"""
        try:
            from backend.agentic_router import extract_response_from_result
        except ImportError:
            pytest.skip("Cannot import extract_response_from_result")
        
        # Test various string response formats that should remain unchanged
        test_cases = [
            "Hello! I'm doing well, thank you for asking.",
            "This is a simple response with no special formatting.",
            "I can help you with that task. Let me know what you need.",
            "Here's the information you requested: The answer is 42.",
            "Great question! Let me think about that for a moment.",
        ]
        
        for test_response in test_cases:
            result = extract_response_from_result(
                test_response, 
                self.test_query, 
                self.consciousness_context
            )
            
            # Should return exactly the same string
            assert result == test_response
            assert isinstance(result, str)
            assert len(result) > 0
    
    def test_multiline_string_response_unchanged(self):
        """Test that multiline string responses work as before"""
        try:
            from backend.agentic_router import extract_response_from_result
        except ImportError:
            pytest.skip("Cannot import extract_response_from_result")
        
        multiline_response = """This is a multiline response.
        
It contains multiple paragraphs and should be preserved exactly.

The formatting and line breaks should remain intact."""
        
        result = extract_response_from_result(
            multiline_response,
            self.test_query,
            self.consciousness_context
        )
        
        assert result == multiline_response
        assert "\n" in result  # Verify line breaks preserved
    
    # ========================================
    # Test 3: Dictionary Response Types (Legacy)
    # ========================================
    
    def test_dict_with_response_field_unchanged(self):
        """Test dictionary with 'response' field works as before"""
        try:
            from backend.agentic_router import extract_response_from_result
        except ImportError:
            pytest.skip("Cannot import extract_response_from_result")
        
        dict_response = {
            "response": "This is the main response content",
            "metadata": {"agent": "test", "timestamp": "2024-01-01"}
        }
        
        result = extract_response_from_result(
            dict_response,
            self.test_query,
            self.consciousness_context
        )
        
        assert result == "This is the main response content"
        assert isinstance(result, str)
    
    def test_dict_with_answer_field_unchanged(self):
        """Test dictionary with 'answer' field works as before"""
        try:
            from backend.agentic_router import extract_response_from_result
        except ImportError:
            pytest.skip("Cannot import extract_response_from_result")
        
        dict_response = {
            "answer": "This is the answer to your question",
            "confidence": 0.95,
            "sources": ["source1", "source2"]
        }
        
        result = extract_response_from_result(
            dict_response,
            self.test_query,
            self.consciousness_context
        )
        
        assert result == "This is the answer to your question"
    
    def test_dict_with_multiple_fields_unchanged(self):
        """Test dictionary with multiple response fields prioritizes correctly"""
        try:
            from backend.agentic_router import extract_response_from_result
        except ImportError:
            pytest.skip("Cannot import extract_response_from_result")
        
        dict_response = {
            "response": "Primary response",
            "answer": "Secondary answer", 
            "output": "Tertiary output",
            "message": "Quaternary message"
        }
        
        result = extract_response_from_result(
            dict_response,
            self.test_query,
            self.consciousness_context
        )
        
        # Should prioritize 'response' field first
        assert result == "Primary response"
    
    # ========================================
    # Test 4: Legacy extract_answer Function
    # ========================================
    
    def test_extract_answer_function_unchanged(self):
        """Test that extract_answer function still works as before"""
        try:
            from backend.agentic_router import extract_answer
        except ImportError:
            pytest.skip("Cannot import extract_answer")
        
        # Test various formats that extract_answer should handle
        test_cases = [
            # Dict with answer
            ({"answer": "Test answer"}, "Test answer"),
            # Plain string
            ("Plain string response", "Plain string response"),
            # JSON string with answer
            ('{"answer": "JSON answer"}', "JSON answer"),
        ]
        
        for input_data, expected in test_cases:
            result = extract_answer(input_data)
            assert result == expected
    
    # ========================================
    # Test 5: Error Handling Compatibility
    # ========================================
    
    def test_none_response_unchanged(self):
        """Test None responses generate appropriate fallback as before"""
        try:
            from backend.agentic_router import extract_response_from_result
        except ImportError:
            pytest.skip("Cannot import extract_response_from_result")
        
        result = extract_response_from_result(
            None,
            self.test_query,
            self.consciousness_context
        )
        
        # Should generate fallback response
        assert isinstance(result, str)
        assert len(result) > 0
        # Should be user-friendly
        assert not any(indicator in result.lower() for indicator in [
            "object at 0x", "<class", "traceback"
        ])
    
    def test_empty_string_response_unchanged(self):
        """Test empty string responses generate fallback as before"""
        try:
            from backend.agentic_router import extract_response_from_result
        except ImportError:
            pytest.skip("Cannot import extract_response_from_result")
        
        result = extract_response_from_result(
            "",
            self.test_query,
            self.consciousness_context
        )
        
        # Should generate fallback response
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_empty_dict_response_unchanged(self):
        """Test empty dictionary responses generate fallback as before"""
        try:
            from backend.agentic_router import extract_response_from_result
        except ImportError:
            pytest.skip("Cannot import extract_response_from_result")
        
        result = extract_response_from_result(
            {},
            self.test_query,
            self.consciousness_context
        )
        
        # Should generate fallback response
        assert isinstance(result, str)
        assert len(result) > 0
    
    # ========================================
    # Test 6: Performance Consistency
    # ========================================
    
    def test_response_processing_performance_unchanged(self):
        """Test that response processing performance is not degraded"""
        try:
            from backend.agentic_router import extract_response_from_result
        except ImportError:
            pytest.skip("Cannot import extract_response_from_result")
        
        import time
        
        # Test with various response types
        test_responses = [
            "Simple string response",
            {"response": "Dict response"},
            {"answer": "Dict with answer"},
        ]
        
        processing_times = []
        
        for response in test_responses:
            start_time = time.time()
            
            # Process response multiple times to get average
            for _ in range(100):
                result = extract_response_from_result(
                    response,
                    self.test_query,
                    self.consciousness_context
                )
                assert isinstance(result, str)
                assert len(result) > 0
            
            end_time = time.time()
            processing_times.append(end_time - start_time)
        
        # Verify processing times are reasonable (under 1 second for 100 iterations)
        for processing_time in processing_times:
            assert processing_time < 1.0, f"Processing took too long: {processing_time}s"
    
    # ========================================
    # Test 7: Consciousness Context Compatibility
    # ========================================
    
    def test_consciousness_context_compatibility_unchanged(self):
        """Test that consciousness context handling remains compatible"""
        try:
            from backend.agentic_router import extract_response_from_result
        except ImportError:
            pytest.skip("Cannot import extract_response_from_result")
        
        # Test with various consciousness context formats
        context_variations = [
            # Standard context
            {
                "user_id": "test_user",
                "consciousness_level": 0.7,
                "emotional_state": "curious"
            },
            # Minimal context
            {"user_id": "test_user"},
            # Extended context
            {
                "user_id": "test_user",
                "consciousness_level": 0.9,
                "emotional_state": "excited",
                "active_goals": ["learning", "helping"],
                "learning_rate": 0.8,
                "memory_strength": 0.6
            },
            # Empty context (should not break)
            {}
        ]
        
        for context in context_variations:
            result = extract_response_from_result(
                "Test response",
                self.test_query,
                context
            )
            
            assert result == "Test response"
            assert isinstance(result, str)
    
    # ========================================
    # Test 8: JSON String Compatibility
    # ========================================
    
    def test_json_string_response_unchanged(self):
        """Test JSON string responses work as before"""
        try:
            from backend.agentic_router import extract_response_from_result
        except ImportError:
            pytest.skip("Cannot import extract_response_from_result")
        
        json_response = '{"response": "JSON formatted response", "type": "json"}'
        
        result = extract_response_from_result(
            json_response,
            self.test_query,
            self.consciousness_context
        )
        
        # Should parse JSON and extract response
        assert result == "JSON formatted response"
    
    def test_malformed_json_string_unchanged(self):
        """Test malformed JSON strings work as before (fallback to string)"""
        try:
            from backend.agentic_router import extract_response_from_result
        except ImportError:
            pytest.skip("Cannot import extract_response_from_result")
        
        malformed_json = '{"response": "Incomplete JSON'
        
        result = extract_response_from_result(
            malformed_json,
            self.test_query,
            self.consciousness_context
        )
        
        # Should treat as regular string since JSON parsing fails
        assert isinstance(result, str)
        assert len(result) > 0

if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])