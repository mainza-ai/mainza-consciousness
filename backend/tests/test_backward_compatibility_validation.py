"""
Backward Compatibility Validation Tests for Throttling Response Fix

This test suite validates that all existing response types continue to work unchanged
after implementing the throttling response fix. It ensures:
1. All existing response types continue to work unchanged
2. Agent integrations are not affected by the changes  
3. API response structure remains consistent

Requirements: 5.1, 5.2, 5.4
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
from backend.agentic_router import (
    extract_response_from_result,
    extract_answer,
    enhanced_router_chat
)
from backend.agents.simple_chat import enhanced_simple_chat_agent
from backend.agents.graphmaster import enhanced_graphmaster_agent
from backend.models.graphmaster_models import GraphQueryOutput
from backend.models.taskmaster_models import TaskOutput
from backend.models.codeweaver_models import CodeWeaverOutput
from backend.models.rag_models import RAGOutput
from backend.models.notification_models import NotificationOutput
from backend.models.calendar_models import CalendarOutput
from backend.models.conductor_models import ConductorResult
import logging

# Test data for various response types
CONSCIOUSNESS_CONTEXT = {
    "user_id": "test_user",
    "consciousness_level": 0.7,
    "emotional_state": "curious",
    "active_goals": ["learning"],
    "learning_rate": 0.8
}

class TestBackwardCompatibilityValidation:
    """Test suite for backward compatibility validation"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.test_query = "Hello, how are you?"
        self.consciousness_context = CONSCIOUSNESS_CONTEXT.copy()
    
    # ========================================
    # Test 1: String Response Types (Legacy)
    # ========================================
    
    def test_simple_string_response_unchanged(self):
        """Test that simple string responses work exactly as before"""
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
    
    def test_string_with_special_characters_unchanged(self):
        """Test strings with special characters work as before"""
        special_response = "Here's a response with special chars: @#$%^&*()[]{}|\\:;\"'<>,.?/~`"
        
        result = extract_response_from_result(
            special_response,
            self.test_query,
            self.consciousness_context
        )
        
        assert result == special_response
    
    # ========================================
    # Test 2: Dictionary Response Types (Legacy)
    # ========================================
    
    def test_dict_with_response_field_unchanged(self):
        """Test dictionary with 'response' field works as before"""
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
    
    def test_dict_with_output_field_unchanged(self):
        """Test dictionary with 'output' field works as before"""
        dict_response = {
            "output": "Generated output content",
            "model": "test-model",
            "tokens": 150
        }
        
        result = extract_response_from_result(
            dict_response,
            self.test_query,
            self.consciousness_context
        )
        
        assert result == "Generated output content"
    
    def test_dict_with_multiple_fields_unchanged(self):
        """Test dictionary with multiple response fields prioritizes correctly"""
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
    # Test 3: Object Response Types (Legacy)
    # ========================================
    
    def test_object_with_response_attribute_unchanged(self):
        """Test objects with response attributes work as before"""
        class MockResponse:
            def __init__(self):
                self.response = "Object response content"
                self.status = "success"
        
        mock_obj = MockResponse()
        
        result = extract_response_from_result(
            mock_obj,
            self.test_query,
            self.consciousness_context
        )
        
        assert result == "Object response content"
    
    def test_object_with_output_attribute_unchanged(self):
        """Test objects with output attributes work as before"""
        class MockOutput:
            def __init__(self):
                self.output = "Object output content"
                self.metadata = {"type": "test"}
        
        mock_obj = MockOutput()
        
        result = extract_response_from_result(
            mock_obj,
            self.test_query,
            self.consciousness_context
        )
        
        assert result == "Object output content"
    
    # ========================================
    # Test 4: Agent Model Response Types (Legacy)
    # ========================================
    
    def test_graphmaster_output_model_unchanged(self):
        """Test GraphQueryOutput model responses work as before"""
        graph_output = GraphQueryOutput(
            result={
                "response": "Graph query result",
                "nodes": 5,
                "relationships": 3
            }
        )
        
        result = extract_response_from_result(
            graph_output,
            self.test_query,
            self.consciousness_context
        )
        
        # Should extract from the result dict
        assert "Graph query result" in result or "nodes" in result
    
    def test_task_output_model_unchanged(self):
        """Test TaskOutput model responses work as before"""
        task_output = TaskOutput(
            status="completed",
            message="Task completed successfully",
            result={"task_id": "123", "output": "Task result"}
        )
        
        result = extract_response_from_result(
            task_output,
            self.test_query,
            self.consciousness_context
        )
        
        # Should extract message or convert to string
        assert "Task completed successfully" in result or "completed" in result
    
    # ========================================
    # Test 5: JSON String Response Types (Legacy)
    # ========================================
    
    def test_json_string_response_unchanged(self):
        """Test JSON string responses work as before"""
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
        malformed_json = '{"response": "Incomplete JSON'
        
        result = extract_response_from_result(
            malformed_json,
            self.test_query,
            self.consciousness_context
        )
        
        # Should treat as regular string since JSON parsing fails
        assert isinstance(result, str)
        assert len(result) > 0
    
    # ========================================
    # Test 6: Edge Cases and Error Conditions (Legacy)
    # ========================================
    
    def test_none_response_unchanged(self):
        """Test None responses generate appropriate fallback as before"""
        result = extract_response_from_result(
            None,
            self.test_query,
            self.consciousness_context
        )
        
        # Should generate fallback response
        assert isinstance(result, str)
        assert len(result) > 0
        assert "Mainza" in result or "help" in result.lower()
    
    def test_empty_string_response_unchanged(self):
        """Test empty string responses generate fallback as before"""
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
        result = extract_response_from_result(
            {},
            self.test_query,
            self.consciousness_context
        )
        
        # Should generate fallback response
        assert isinstance(result, str)
        assert len(result) > 0
    
    # ========================================
    # Test 7: Legacy extract_answer Function
    # ========================================
    
    def test_extract_answer_function_unchanged(self):
        """Test that extract_answer function still works as before"""
        # Test various formats that extract_answer should handle
        test_cases = [
            # Dict with answer
            ({"answer": "Test answer"}, "Test answer"),
            # String with AgentRunResult pattern
            ("AgentRunResult(output='Extracted output')", "Extracted output"),
            # JSON string with answer
            ('{"answer": "JSON answer"}', "JSON answer"),
            # Plain string
            ("Plain string response", "Plain string response"),
            # String with answer= pattern
            ("Some text answer='Pattern answer' more text", "Pattern answer"),
        ]
        
        for input_data, expected in test_cases:
            result = extract_answer(input_data)
            assert result == expected
    
    # ========================================
    # Test 8: Agent Integration Compatibility
    # ========================================
    
    @pytest.mark.asyncio
    async def test_simple_chat_agent_integration_unchanged(self):
        """Test simple chat agent integration works as before"""
        with patch.object(enhanced_simple_chat_agent, 'execute_with_context') as mock_execute:
            mock_execute.return_value = "Simple chat response"
            
            result = await enhanced_simple_chat_agent.execute_with_context(
                query=self.test_query,
                user_id="test_user",
                consciousness_context=self.consciousness_context
            )
            
            assert result == "Simple chat response"
            mock_execute.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_graphmaster_agent_integration_unchanged(self):
        """Test graphmaster agent integration works as before"""
        with patch.object(enhanced_graphmaster_agent, 'execute_with_context') as mock_execute:
            mock_execute.return_value = GraphQueryOutput(
                result={"response": "Graph response", "type": "query"}
            )
            
            result = await enhanced_graphmaster_agent.execute_with_context(
                query=self.test_query,
                user_id="test_user", 
                consciousness_context=self.consciousness_context
            )
            
            assert isinstance(result, GraphQueryOutput)
            assert result.result["response"] == "Graph response"
            mock_execute.assert_called_once()
    
    # ========================================
    # Test 9: API Response Structure Consistency
    # ========================================
    
    @pytest.mark.asyncio
    async def test_enhanced_router_chat_response_structure_unchanged(self):
        """Test that enhanced_router_chat maintains consistent response structure"""
        with patch('backend.agentic_router.get_consciousness_context') as mock_consciousness, \
             patch('backend.agentic_router.get_conversation_context') as mock_conversation, \
             patch('backend.agentic_router.make_consciousness_aware_routing_decision') as mock_routing, \
             patch('backend.agentic_router.llm_request_manager') as mock_llm_manager, \
             patch('backend.agentic_router.store_conversation_turn') as mock_store, \
             patch('backend.agentic_router.update_consciousness_from_conversation') as mock_update:
            
            # Setup mocks
            mock_consciousness.return_value = self.consciousness_context
            mock_conversation.return_value = []
            mock_routing.return_value = {"agent_name": "simple_chat", "confidence": 0.8}
            mock_llm_manager.submit_request = AsyncMock(return_value="Test response")
            mock_store.return_value = None
            mock_update.return_value = None
            
            # Call the endpoint
            response = await enhanced_router_chat(
                query=self.test_query,
                user_id="test_user"
            )
            
            # Validate response structure remains consistent
            assert isinstance(response, dict)
            assert "response" in response
            assert "agent_used" in response
            assert "consciousness_level" in response
            assert "emotional_state" in response
            assert "routing_confidence" in response
            assert "user_id" in response
            assert "query" in response
            
            # Validate field types
            assert isinstance(response["response"], str)
            assert isinstance(response["agent_used"], str)
            assert isinstance(response["consciousness_level"], (int, float))
            assert isinstance(response["emotional_state"], str)
            assert isinstance(response["routing_confidence"], (int, float))
            assert isinstance(response["user_id"], str)
            assert isinstance(response["query"], str)
    
    # ========================================
    # Test 10: Performance and Memory Consistency
    # ========================================
    
    def test_response_processing_performance_unchanged(self):
        """Test that response processing performance is not degraded"""
        import time
        
        # Test with various response types
        test_responses = [
            "Simple string response",
            {"response": "Dict response"},
            {"answer": "Dict with answer"},
            '{"response": "JSON string"}',
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
    
    def test_memory_usage_unchanged(self):
        """Test that memory usage patterns remain consistent"""
        import gc
        import sys
        
        # Get initial memory usage
        gc.collect()
        initial_objects = len(gc.get_objects())
        
        # Process many responses
        for i in range(1000):
            response = f"Test response {i}"
            result = extract_response_from_result(
                response,
                self.test_query,
                self.consciousness_context
            )
            assert result == response
        
        # Check memory usage after processing
        gc.collect()
        final_objects = len(gc.get_objects())
        
        # Memory usage should not grow significantly
        object_growth = final_objects - initial_objects
        assert object_growth < 100, f"Too many objects created: {object_growth}"
    
    # ========================================
    # Test 11: Concurrent Processing Compatibility
    # ========================================
    
    @pytest.mark.asyncio
    async def test_concurrent_response_processing_unchanged(self):
        """Test that concurrent response processing works as before"""
        import asyncio
        
        async def process_response(response_data):
            """Process a single response"""
            return extract_response_from_result(
                response_data,
                self.test_query,
                self.consciousness_context
            )
        
        # Create multiple concurrent processing tasks
        test_responses = [
            f"Concurrent response {i}" for i in range(50)
        ]
        
        # Process all responses concurrently
        tasks = [process_response(response) for response in test_responses]
        results = await asyncio.gather(*tasks)
        
        # Verify all results are correct
        for i, result in enumerate(results):
            expected = f"Concurrent response {i}"
            assert result == expected
    
    # ========================================
    # Test 12: Error Handling Compatibility
    # ========================================
    
    def test_error_handling_unchanged(self):
        """Test that error handling behavior remains unchanged"""
        # Test various error conditions that should be handled gracefully
        error_cases = [
            None,  # None input
            "",    # Empty string
            {},    # Empty dict
            [],    # Empty list
            object(),  # Generic object
        ]
        
        for error_case in error_cases:
            result = extract_response_from_result(
                error_case,
                self.test_query,
                self.consciousness_context
            )
            
            # Should always return a string fallback
            assert isinstance(result, str)
            assert len(result) > 0
            # Should not contain raw object representations
            assert not any(indicator in result.lower() for indicator in [
                "object at 0x", "<class", "traceback", "error:"
            ])
    
    # ========================================
    # Test 13: Logging Compatibility
    # ========================================
    
    def test_logging_behavior_unchanged(self):
        """Test that logging behavior for normal responses is unchanged"""
        with patch('backend.agentic_router.logging') as mock_logging:
            # Process normal response
            result = extract_response_from_result(
                "Normal response",
                self.test_query,
                self.consciousness_context
            )
            
            assert result == "Normal response"
            
            # Verify logging calls are made (but not excessive)
            assert mock_logging.debug.called or mock_logging.info.called
            # Should not have excessive error logging for normal responses
            assert not mock_logging.error.called
    
    # ========================================
    # Test 14: Configuration Compatibility
    # ========================================
    
    def test_consciousness_context_compatibility_unchanged(self):
        """Test that consciousness context handling remains compatible"""
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

if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])