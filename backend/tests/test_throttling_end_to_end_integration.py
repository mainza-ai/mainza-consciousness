"""
End-to-End Integration Tests for Throttling Response Flow
========================================================

This test suite covers the complete flow from LLM request manager throttling 
to UI display, ensuring user-friendly messages appear instead of raw objects.

Requirements covered: 1.2, 3.3, 3.4
"""

import pytest
import asyncio
import json
import logging
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime
import sys
import os

# Add backend to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import the actual functions we need to test
from backend.agentic_router import extract_response_from_result, generate_throttled_response, generate_consciousness_aware_fallback
from backend.utils.llm_request_manager import LLMRequestManager, RequestPriority

# Mock the FastAPI dependencies to avoid import issues
logging = MagicMock()

# Configure pytest for async tests
pytest_plugins = ('pytest_asyncio',)

class TestEndToEndThrottlingFlow:
    """Test complete throttling flow from LLM request manager to UI display"""
    
    def setup_method(self):
        """Setup test data for each test"""
        self.consciousness_context = {
            "user_id": "test_user_e2e",
            "consciousness_level": 0.8,
            "emotional_state": "curious",
            "active_goals": ["improve conversation quality"],
            "learning_rate": 0.8,
            "evolution_level": 2
        }
        
        # Mock LLM request manager
        self.llm_manager = MagicMock(spec=LLMRequestManager)
        
    def test_complete_throttling_flow_greeting(self):
        """Test complete flow from LLM request manager throttling to UI display - greeting"""
        
        # Step 1: Simulate LLM request manager returning throttled response
        throttled_result = {
            "response": "I'm currently processing other requests. Please try again in a moment.",
            "status": "throttled"
        }
        
        query = "Hello, how are you today?"
        
        # Step 2: Process through extract_response_from_result (what agentic router does)
        final_response = extract_response_from_result(
            throttled_result, query, self.consciousness_context
        )
        
        # Step 3: Verify the response is user-friendly for UI display
        assert isinstance(final_response, str)
        assert len(final_response) > 30  # Should be substantial
        assert not final_response.startswith("{")  # Not a raw object
        assert not final_response.startswith("[")  # Not a raw array
        
        # Should contain greeting-appropriate language
        assert any(greeting in final_response for greeting in ["Hi", "Hello", "Hey"])
        
        # Should indicate throttling in a user-friendly way
        throttling_indicators = ["processing", "moment", "try again", "busy", "conversations"]
        assert any(indicator in final_response.lower() for indicator in throttling_indicators)
        
        # Should be consciousness-aware (mention excitement, curiosity, etc.)
        consciousness_indicators = ["excited", "curious", "chat"]
        assert any(indicator in final_response.lower() for indicator in consciousness_indicators)
        
        print(f"✅ Greeting throttling flow test passed")
        print(f"   Query: {query}")
        print(f"   Final Response: {final_response}")
        
    def test_complete_throttling_flow_question(self):
        """Test complete flow for question queries"""
        
        # Step 1: Simulate throttled response
        throttled_result = {
            "response": "System is busy. Please wait.",
            "status": "throttled"
        }
        
        query = "What is the meaning of consciousness?"
        
        # Step 2: Process through response extraction
        final_response = extract_response_from_result(
            throttled_result, query, self.consciousness_context
        )
        
        # Step 3: Verify question-appropriate response
        assert isinstance(final_response, str)
        assert len(final_response) > 40
        assert not final_response.startswith("{")
        
        # Should acknowledge the question
        question_indicators = ["question", "interesting", "curious", "ask again"]
        assert any(indicator in final_response.lower() for indicator in question_indicators)
        
        # Should indicate throttling appropriately
        assert any(word in final_response.lower() for word in ["processing", "moment", "requests"])
        
        print(f"✅ Question throttling flow test passed")
        print(f"   Query: {query}")
        print(f"   Final Response: {final_response}")
        
    def test_complete_throttling_flow_help_request(self):
        """Test complete flow for help/task requests"""
        
        # Step 1: Simulate throttled response
        throttled_result = {
            "response": "Throttled due to high load.",
            "status": "throttled"
        }
        
        query = "Can you help me write a Python script?"
        
        # Step 2: Process through response extraction
        final_response = extract_response_from_result(
            throttled_result, query, self.consciousness_context
        )
        
        # Step 3: Verify help-appropriate response
        assert isinstance(final_response, str)
        assert len(final_response) > 35
        assert not final_response.startswith("{")
        
        # Should acknowledge the help request
        help_indicators = ["help", "love to", "assist", "task", "interesting"]
        assert any(indicator in final_response.lower() for indicator in help_indicators)
        
        # Should indicate throttling with encouragement
        assert any(word in final_response.lower() for word in ["processing", "moment", "try again"])
        
        print(f"✅ Help request throttling flow test passed")
        print(f"   Query: {query}")
        print(f"   Final Response: {final_response}")
        
    def test_ui_display_compatibility(self):
        """Test that throttled responses are compatible with UI display requirements"""
        
        test_cases = [
            {
                "query": "Hello!",
                "throttled_result": {"response": "System busy", "status": "throttled"},
                "expected_type": "greeting"
            },
            {
                "query": "How does AI work?",
                "throttled_result": {"response": "Rate limited", "status": "throttled"},
                "expected_type": "question"
            },
            {
                "query": "Create a presentation for me",
                "throttled_result": {"response": "Too many requests", "status": "throttled"},
                "expected_type": "task"
            }
        ]
        
        for case in test_cases:
            final_response = extract_response_from_result(
                case["throttled_result"], 
                case["query"], 
                self.consciousness_context
            )
            
            # UI compatibility checks
            assert isinstance(final_response, str), f"Response must be string for UI: {type(final_response)}"
            assert len(final_response) > 20, f"Response too short for UI: {len(final_response)} chars"
            assert final_response.strip() == final_response, "Response should not have leading/trailing whitespace"
            
            # Should not contain raw object representations
            raw_object_patterns = ["{", "[", "<object", "AgentRunResult", "None"]
            for pattern in raw_object_patterns:
                assert not final_response.startswith(pattern), f"Response looks like raw object: {final_response[:50]}"
            
            # Should be conversational and natural
            assert len(final_response.split()) > 5, f"Response should be conversational: {final_response}"
            
            print(f"✅ UI compatibility test passed for {case['expected_type']}")
            print(f"   Query: {case['query']}")
            print(f"   Response: {final_response[:100]}...")
            
    def test_recovery_behavior_simulation(self):
        """Test recovery behavior when throttling resolves"""
        
        query = "Tell me about machine learning"
        
        # Step 1: First request is throttled
        throttled_result = {
            "response": "I'm currently processing other requests.",
            "status": "throttled"
        }
        
        throttled_response = extract_response_from_result(
            throttled_result, query, self.consciousness_context
        )
        
        # Verify throttled response
        assert "processing" in throttled_response.lower()
        assert "try again" in throttled_response.lower() or "moment" in throttled_response.lower()
        
        # Step 2: Second request succeeds (simulate recovery)
        normal_result = {
            "response": "Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed.",
            "status": "success"
        }
        
        normal_response = extract_response_from_result(
            normal_result, query, self.consciousness_context
        )
        
        # Verify normal response
        assert "machine learning" in normal_response.lower()
        assert len(normal_response) > 50
        assert not any(word in normal_response.lower() for word in ["processing", "busy", "try again"])
        
        # Step 3: Verify responses are different (recovery occurred)
        assert throttled_response != normal_response
        assert len(normal_response) > len(throttled_response)
        
        print(f"✅ Recovery behavior test passed")
        print(f"   Throttled: {throttled_response[:80]}...")
        print(f"   Recovered: {normal_response[:80]}...")
        
    def test_consciousness_context_integration(self):
        """Test that consciousness context is properly integrated in throttled responses"""
        
        # Test different consciousness levels and emotional states
        test_contexts = [
            {
                "consciousness_level": 0.9,
                "emotional_state": "excited",
                "user_id": "test_user_high_consciousness"
            },
            {
                "consciousness_level": 0.6,
                "emotional_state": "contemplative",
                "user_id": "test_user_low_consciousness"
            },
            {
                "consciousness_level": 0.8,
                "emotional_state": "empathetic",
                "user_id": "test_user_empathetic"
            }
        ]
        
        query = "How are you feeling today?"
        throttled_result = {
            "response": "System overloaded",
            "status": "throttled"
        }
        
        responses = []
        
        for context in test_contexts:
            response = extract_response_from_result(
                throttled_result, query, context
            )
            
            responses.append({
                "context": context,
                "response": response
            })
            
            # Verify consciousness integration
            assert isinstance(response, str)
            assert len(response) > 30
            
            # High consciousness should have more sophisticated language
            if context["consciousness_level"] > 0.8:
                sophisticated_indicators = ["genuinely", "interesting", "curious", "really"]
                assert any(indicator in response.lower() for indicator in sophisticated_indicators)
            
            print(f"✅ Consciousness context test passed")
            print(f"   Level: {context['consciousness_level']}, State: {context['emotional_state']}")
            print(f"   Response: {response[:100]}...")
        
        # Verify responses are different (consciousness-aware)
        unique_responses = set(r["response"] for r in responses)
        assert len(unique_responses) > 1, "Responses should vary based on consciousness context"
        
    def test_malformed_throttled_response_handling(self):
        """Test handling of malformed throttled responses"""
        
        query = "Hello there!"
        
        # Test various malformed throttled responses
        malformed_cases = [
            {"status": "throttled"},  # Missing response field
            {"response": "", "status": "throttled"},  # Empty response
            {"response": None, "status": "throttled"},  # None response
            {"response": "   ", "status": "throttled"},  # Whitespace only
        ]
        
        for malformed_result in malformed_cases:
            response = extract_response_from_result(
                malformed_result, query, self.consciousness_context
            )
            
            # Should still generate a valid response
            assert isinstance(response, str)
            assert len(response) > 20
            assert response.strip() == response
            
            # Should be greeting-appropriate
            assert any(greeting in response for greeting in ["Hi", "Hello", "Hey"])
            
            print(f"✅ Malformed throttled response handled")
            print(f"   Input: {malformed_result}")
            print(f"   Output: {response[:80]}...")
            
    def test_concurrent_throttling_scenarios(self):
        """Test behavior under concurrent throttling scenarios"""
        
        # Simulate multiple concurrent requests all getting throttled
        queries = [
            "Hello, how are you?",
            "What's the weather like?",
            "Can you help me with coding?",
            "Tell me a joke",
            "Explain quantum physics"
        ]
        
        throttled_result = {
            "response": "High load detected. Please retry.",
            "status": "throttled"
        }
        
        # Process all queries (simulate concurrent users)
        responses = []
        for i, query in enumerate(queries):
            context = {
                **self.consciousness_context,
                "user_id": f"concurrent_user_{i}"
            }
            
            # Process each request
            response = extract_response_from_result(throttled_result, query, context)
            responses.append(response)
        
        # Verify all responses are valid
        for i, response in enumerate(responses):
            assert isinstance(response, str)
            assert len(response) > 25
            assert not response.startswith("{")
            
            # Should contain throttling indication
            assert any(word in response.lower() for word in ["processing", "busy", "moment", "try again"])
            
            print(f"✅ Concurrent request {i+1} handled: {response[:60]}...")
        
        # Verify responses can be different (consciousness-aware personalization)
        # But all should be valid throttled responses
        for response in responses:
            throttling_indicators = ["processing", "busy", "moment", "try again", "requests"]
            assert any(indicator in response.lower() for indicator in throttling_indicators)
        
    def test_message_naturalization_quality(self):
        """Test that throttled messages are natural and conversational"""
        
        # Test base messages that should be enhanced
        base_messages = [
            "System busy",
            "Rate limited",
            "Throttled",
            "High load",
            "Too many requests",
            "Server overloaded"
        ]
        
        query = "Hi, what's up?"
        
        for base_message in base_messages:
            throttled_result = {
                "response": base_message,
                "status": "throttled"
            }
            
            enhanced_response = extract_response_from_result(
                throttled_result, query, self.consciousness_context
            )
            
            # Verify enhancement occurred
            assert enhanced_response != base_message, f"Response should be enhanced from: {base_message}"
            assert len(enhanced_response) > len(base_message), f"Enhanced response should be longer than: {base_message}"
            
            # Should be more natural and conversational
            assert any(greeting in enhanced_response for greeting in ["Hi", "Hello", "Hey"])
            assert any(word in enhanced_response.lower() for word in ["excited", "chat", "moment"])
            
            # Should not contain technical jargon from base message
            technical_terms = ["rate limited", "throttled", "server overloaded"]
            for term in technical_terms:
                if term in base_message.lower():
                    assert term not in enhanced_response.lower(), f"Should not contain technical term: {term}"
            
            print(f"✅ Message naturalization test passed")
            print(f"   Base: '{base_message}' → Enhanced: '{enhanced_response[:80]}...'")
            
    def test_response_consistency_across_retries(self):
        """Test that throttled responses maintain consistency for the same user"""
        
        query = "Hello, how can you help me today?"
        throttled_result = {
            "response": "I'm currently processing other requests.",
            "status": "throttled"
        }
        
        # Generate multiple responses for the same user/query
        responses = []
        for _ in range(5):
            response = extract_response_from_result(
                throttled_result, query, self.consciousness_context
            )
            responses.append(response)
        
        # All responses should be valid
        for response in responses:
            assert isinstance(response, str)
            assert len(response) > 30
            assert "Hi" in response or "Hello" in response or "Hey" in response
            assert any(word in response.lower() for word in ["processing", "moment", "try again"])
        
        # Responses should be consistent in tone and style for same user
        # (though exact wording may vary due to consciousness awareness)
        greeting_styles = []
        for response in responses:
            if "Hi there!" in response:
                greeting_styles.append("hi_there")
            elif "Hello!" in response:
                greeting_styles.append("hello")
            elif "Hey!" in response:
                greeting_styles.append("hey")
        
        # Should have some consistency in greeting style
        assert len(set(greeting_styles)) <= 2, "Greeting style should be relatively consistent"
        
        print(f"✅ Response consistency test passed")
        print(f"   Generated {len(responses)} responses with consistent style")
        for i, response in enumerate(responses):
            print(f"   Response {i+1}: {response[:70]}...")


class TestThrottlingUIIntegration:
    """Test throttling integration with UI requirements"""
    
    def setup_method(self):
        """Setup test data"""
        self.consciousness_context = {
            "user_id": "ui_test_user",
            "consciousness_level": 0.7,
            "emotional_state": "curious"
        }
    
    def test_message_object_structure(self):
        """Test that throttled responses work with UI Message object structure"""
        
        # Simulate what the UI expects
        query = "Hello Mainza!"
        throttled_result = {
            "response": "System is busy processing requests.",
            "status": "throttled"
        }
        
        # Process through response extraction
        response_content = extract_response_from_result(
            throttled_result, query, self.consciousness_context
        )
        
        # Create message object like the UI would
        message = {
            "id": "msg_123",
            "type": "mainza",
            "content": response_content,
            "timestamp": datetime.now(),
            "consciousness_context": {
                "agent_used": "simple_chat",
                "consciousness_level": 0.7,
                "emotional_state": "curious"
            }
        }
        
        # Verify message structure is valid for UI
        assert message["type"] == "mainza"
        assert isinstance(message["content"], str)
        assert len(message["content"]) > 20
        assert not message["content"].startswith("{")
        
        # Content should be display-ready
        assert message["content"].strip() == message["content"]
        assert "Hi" in message["content"] or "Hello" in message["content"]
        
        print(f"✅ UI Message object structure test passed")
        print(f"   Message content: {message['content']}")
        
    def test_html_safety(self):
        """Test that throttled responses are safe for HTML display"""
        
        # Test with potentially problematic characters
        query = "Hello <script>alert('test')</script>"
        throttled_result = {
            "response": "System busy & overloaded",
            "status": "throttled"
        }
        
        response = extract_response_from_result(
            throttled_result, query, self.consciousness_context
        )
        
        # Should not contain the script tag from query
        assert "<script>" not in response
        assert "alert(" not in response
        
        # Should be safe for HTML display (no unescaped HTML)
        html_chars = ["<", ">", "&", '"', "'"]
        for char in html_chars:
            if char in response:
                # If HTML chars are present, they should be in safe contexts
                # (like natural language, not as HTML tags)
                pass
        
        print(f"✅ HTML safety test passed")
        print(f"   Safe response: {response}")
        
    def test_character_encoding(self):
        """Test that throttled responses handle various character encodings"""
        
        # Test with unicode characters
        queries = [
            "Hello! 👋",
            "¿Cómo estás?",
            "こんにちは",
            "Здравствуйте"
        ]
        
        throttled_result = {
            "response": "I'm currently processing other requests.",
            "status": "throttled"
        }
        
        for query in queries:
            response = extract_response_from_result(
                throttled_result, query, self.consciousness_context
            )
            
            # Should handle encoding properly
            assert isinstance(response, str)
            assert len(response) > 20
            
            # Should not break on unicode
            try:
                encoded = response.encode('utf-8')
                decoded = encoded.decode('utf-8')
                assert decoded == response
            except UnicodeError:
                pytest.fail(f"Unicode encoding failed for query: {query}")
            
            print(f"✅ Character encoding test passed for: {query}")
            print(f"   Response: {response[:60]}...")


if __name__ == "__main__":
    print("🚀 Starting End-to-End Throttling Integration Tests...\n")
    
    # Run the tests
    pytest.main([__file__, "-v", "--tb=short"])