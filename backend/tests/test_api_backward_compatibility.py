"""
API Backward Compatibility Tests for Throttling Response Fix

This test suite validates that API endpoints maintain consistent response structures
and agent integrations work unchanged after implementing the throttling response fix.

Requirements: 5.1, 5.2, 5.4
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
from backend.main import app
from backend.models.graphmaster_models import GraphQueryInput, GraphQueryOutput
from backend.models.taskmaster_models import TaskInput, TaskOutput
from backend.models.codeweaver_models import CodeWeaverInput, CodeWeaverOutput

# Test client for API testing
client = TestClient(app)

class TestAPIBackwardCompatibility:
    """Test suite for API backward compatibility validation"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.test_user_id = "test_user"
        self.test_query = "Hello, how are you?"
    
    # ========================================
    # Test 1: Enhanced Router Chat Endpoint
    # ========================================
    
    @patch('backend.agentic_router.get_consciousness_context')
    @patch('backend.agentic_router.get_conversation_context')
    @patch('backend.agentic_router.make_consciousness_aware_routing_decision')
    @patch('backend.agentic_router.llm_request_manager')
    @patch('backend.agentic_router.store_conversation_turn')
    @patch('backend.agentic_router.update_consciousness_from_conversation')
    def test_enhanced_router_chat_response_structure_unchanged(
        self, mock_update, mock_store, mock_llm_manager, 
        mock_routing, mock_conversation, mock_consciousness
    ):
        """Test that enhanced_router_chat maintains consistent response structure"""
        
        # Setup mocks
        mock_consciousness.return_value = {
            "user_id": self.test_user_id,
            "consciousness_level": 0.7,
            "emotional_state": "curious",
            "active_goals": ["learning"]
        }
        mock_conversation.return_value = []
        mock_routing.return_value = {"agent_name": "simple_chat", "confidence": 0.8}
        mock_llm_manager.submit_request = AsyncMock(return_value="Test response from agent")
        mock_store.return_value = None
        mock_update.return_value = None
        
        # Make API request
        response = client.post(
            "/agent/router/chat",
            json={
                "query": self.test_query,
                "user_id": self.test_user_id
            }
        )
        
        # Validate response status
        assert response.status_code == 200
        
        # Validate response structure remains consistent
        response_data = response.json()
        assert isinstance(response_data, dict)
        
        # Check required fields exist
        required_fields = [
            "response", "agent_used", "consciousness_level", 
            "emotional_state", "routing_confidence", "user_id", "query"
        ]
        for field in required_fields:
            assert field in response_data, f"Missing required field: {field}"
        
        # Validate field types
        assert isinstance(response_data["response"], str)
        assert isinstance(response_data["agent_used"], str)
        assert isinstance(response_data["consciousness_level"], (int, float))
        assert isinstance(response_data["emotional_state"], str)
        assert isinstance(response_data["routing_confidence"], (int, float))
        assert isinstance(response_data["user_id"], str)
        assert isinstance(response_data["query"], str)
        
        # Validate field values
        assert response_data["response"] == "Test response from agent"
        assert response_data["agent_used"] == "simple_chat"
        assert response_data["user_id"] == self.test_user_id
        assert response_data["query"] == self.test_query
    
    # ========================================
    # Test 2: GraphMaster Agent Endpoints
    # ========================================
    
    @patch('backend.agents.graphmaster.graphmaster_agent')
    def test_graphmaster_query_endpoint_unchanged(self, mock_agent):
        """Test GraphMaster query endpoint maintains consistent structure"""
        
        # Mock agent response
        mock_result = Mock()
        mock_result.output = {"response": "Graph query result", "nodes": 5}
        mock_agent.run = AsyncMock(return_value=mock_result)
        
        # Make API request
        response = client.post(
            "/agent/graphmaster/query",
            json={
                "query": "Find related concepts",
                "user_id": self.test_user_id
            }
        )
        
        # Validate response
        assert response.status_code == 200
        response_data = response.json()
        
        # Should return GraphQueryOutput structure
        assert "result" in response_data
        assert isinstance(response_data["result"], dict)
        assert response_data["result"]["response"] == "Graph query result"
        assert response_data["result"]["nodes"] == 5
    
    @patch('backend.agents.graphmaster.graphmaster_agent')
    def test_graphmaster_summarize_endpoint_unchanged(self, mock_agent):
        """Test GraphMaster summarize endpoint maintains consistent structure"""
        
        # Mock agent response
        mock_result = Mock()
        mock_result.output = {
            "summary": "Recent conversation summary",
            "conversations": [{"id": "1", "content": "test"}]
        }
        mock_agent.run = AsyncMock(return_value=mock_result)
        
        # Make API request
        response = client.post(
            "/agent/graphmaster/summarize_recent",
            json={
                "user_id": self.test_user_id,
                "limit": 5
            }
        )
        
        # Validate response
        assert response.status_code == 200
        response_data = response.json()
        
        # Should return SummarizeRecentConversationsOutput structure
        assert "summary" in response_data
        assert "conversations" in response_data
        assert response_data["summary"] == "Recent conversation summary"
        assert isinstance(response_data["conversations"], list)
    
    # ========================================
    # Test 3: TaskMaster Agent Endpoint
    # ========================================
    
    @patch('backend.agents.taskmaster.taskmaster_agent')
    def test_taskmaster_endpoint_unchanged(self, mock_agent):
        """Test TaskMaster endpoint maintains consistent structure"""
        
        # Mock agent response
        mock_result = TaskOutput(
            status="completed",
            message="Task completed successfully",
            result={"task_id": "123", "output": "Task result"}
        )
        mock_agent.run = AsyncMock(return_value=mock_result)
        
        # Make API request
        response = client.post(
            "/agent/taskmaster/task",
            json={
                "task_command": "Create a new task",
                "user_id": self.test_user_id
            }
        )
        
        # Validate response
        assert response.status_code == 200
        response_data = response.json()
        
        # Should return TaskOutput structure
        assert "status" in response_data
        assert "message" in response_data
        assert "result" in response_data
        assert response_data["status"] == "completed"
        assert response_data["message"] == "Task completed successfully"
    
    # ========================================
    # Test 4: CodeWeaver Agent Endpoint
    # ========================================
    
    @patch('backend.agents.codeweaver.codeweaver_agent')
    def test_codeweaver_endpoint_unchanged(self, mock_agent):
        """Test CodeWeaver endpoint maintains consistent structure"""
        
        # Mock agent response
        mock_result = Mock()
        mock_result.output = CodeWeaverOutput(
            code="print('Hello, World!')",
            explanation="Simple Python print statement",
            language="python"
        )
        mock_agent.run = AsyncMock(return_value=mock_result)
        
        # Make API request
        response = client.post(
            "/agent/codeweaver/run",
            json={
                "command": "Write a hello world program in Python"
            }
        )
        
        # Validate response
        assert response.status_code == 200
        response_data = response.json()
        
        # Should return CodeWeaverOutput structure
        assert "code" in response_data
        assert "explanation" in response_data
        assert "language" in response_data
        assert response_data["code"] == "print('Hello, World!')"
        assert response_data["language"] == "python"
    
    # ========================================
    # Test 5: Error Handling Consistency
    # ========================================
    
    @patch('backend.agentic_router.get_consciousness_context')
    @patch('backend.agentic_router.get_conversation_context')
    @patch('backend.agentic_router.make_consciousness_aware_routing_decision')
    @patch('backend.agentic_router.llm_request_manager')
    def test_error_handling_response_structure_unchanged(
        self, mock_llm_manager, mock_routing, mock_conversation, mock_consciousness
    ):
        """Test that error handling maintains consistent response structure"""
        
        # Setup mocks to simulate error
        mock_consciousness.return_value = {
            "user_id": self.test_user_id,
            "consciousness_level": 0.7,
            "emotional_state": "curious"
        }
        mock_conversation.return_value = []
        mock_routing.return_value = {"agent_name": "simple_chat", "confidence": 0.8}
        mock_llm_manager.submit_request = AsyncMock(side_effect=Exception("Test error"))
        
        # Make API request
        response = client.post(
            "/agent/router/chat",
            json={
                "query": self.test_query,
                "user_id": self.test_user_id
            }
        )
        
        # Should still return 200 with fallback response
        assert response.status_code == 200
        response_data = response.json()
        
        # Should maintain consistent structure even in error cases
        required_fields = [
            "response", "agent_used", "consciousness_level", 
            "emotional_state", "user_id", "query"
        ]
        for field in required_fields:
            assert field in response_data, f"Missing required field in error response: {field}"
        
        # Response should be a fallback message
        assert isinstance(response_data["response"], str)
        assert len(response_data["response"]) > 0
        assert response_data["agent_used"] == "consciousness_fallback"
    
    # ========================================
    # Test 6: Throttling Response Structure
    # ========================================
    
    @patch('backend.agentic_router.get_consciousness_context')
    @patch('backend.agentic_router.get_conversation_context')
    @patch('backend.agentic_router.make_consciousness_aware_routing_decision')
    @patch('backend.agentic_router.llm_request_manager')
    @patch('backend.agentic_router.store_conversation_turn')
    @patch('backend.agentic_router.update_consciousness_from_conversation')
    def test_throttled_response_structure_unchanged(
        self, mock_update, mock_store, mock_llm_manager, 
        mock_routing, mock_conversation, mock_consciousness
    ):
        """Test that throttled responses maintain consistent API structure"""
        
        # Setup mocks for throttled response
        mock_consciousness.return_value = {
            "user_id": self.test_user_id,
            "consciousness_level": 0.7,
            "emotional_state": "curious"
        }
        mock_conversation.return_value = []
        mock_routing.return_value = {"agent_name": "simple_chat", "confidence": 0.8}
        
        # Mock throttled response from LLM request manager
        throttled_response = {
            "status": "throttled",
            "response": "I'm currently processing other requests."
        }
        mock_llm_manager.submit_request = AsyncMock(return_value=throttled_response)
        mock_store.return_value = None
        mock_update.return_value = None
        
        # Make API request
        response = client.post(
            "/agent/router/chat",
            json={
                "query": self.test_query,
                "user_id": self.test_user_id
            }
        )
        
        # Validate response status
        assert response.status_code == 200
        
        # Validate response structure remains consistent even for throttled responses
        response_data = response.json()
        assert isinstance(response_data, dict)
        
        # Check required fields exist
        required_fields = [
            "response", "agent_used", "consciousness_level", 
            "emotional_state", "routing_confidence", "user_id", "query"
        ]
        for field in required_fields:
            assert field in response_data, f"Missing required field: {field}"
        
        # Response should be consciousness-aware throttled message
        assert isinstance(response_data["response"], str)
        assert len(response_data["response"]) > 0
        # Should contain throttling indicators
        throttling_indicators = ["processing", "requests", "moment", "try again"]
        assert any(indicator in response_data["response"].lower() 
                  for indicator in throttling_indicators)
    
    # ========================================
    # Test 7: Response Content Validation
    # ========================================
    
    @patch('backend.agentic_router.get_consciousness_context')
    @patch('backend.agentic_router.get_conversation_context')
    @patch('backend.agentic_router.make_consciousness_aware_routing_decision')
    @patch('backend.agentic_router.llm_request_manager')
    @patch('backend.agentic_router.store_conversation_turn')
    @patch('backend.agentic_router.update_consciousness_from_conversation')
    def test_response_content_quality_unchanged(
        self, mock_update, mock_store, mock_llm_manager, 
        mock_routing, mock_conversation, mock_consciousness
    ):
        """Test that response content quality remains high and user-friendly"""
        
        # Setup mocks
        mock_consciousness.return_value = {
            "user_id": self.test_user_id,
            "consciousness_level": 0.7,
            "emotional_state": "curious"
        }
        mock_conversation.return_value = []
        mock_routing.return_value = {"agent_name": "simple_chat", "confidence": 0.8}
        mock_llm_manager.submit_request = AsyncMock(return_value="Hello! I'm doing well, thank you for asking. How can I help you today?")
        mock_store.return_value = None
        mock_update.return_value = None
        
        # Make API request
        response = client.post(
            "/agent/router/chat",
            json={
                "query": self.test_query,
                "user_id": self.test_user_id
            }
        )
        
        # Validate response
        assert response.status_code == 200
        response_data = response.json()
        
        # Validate response content quality
        response_text = response_data["response"]
        
        # Should not contain raw object representations
        assert "object at 0x" not in response_text
        assert "<class" not in response_text
        assert "AgentRunResult" not in response_text
        assert "Traceback" not in response_text
        
        # Should be user-friendly
        assert len(response_text) > 10  # Meaningful length
        assert not response_text.startswith("{")  # Not raw JSON
        assert not response_text.startswith("[")  # Not raw list
        
        # Should match expected response
        assert response_text == "Hello! I'm doing well, thank you for asking. How can I help you today?"
    
    # ========================================
    # Test 8: Multiple Request Consistency
    # ========================================
    
    @patch('backend.agentic_router.get_consciousness_context')
    @patch('backend.agentic_router.get_conversation_context')
    @patch('backend.agentic_router.make_consciousness_aware_routing_decision')
    @patch('backend.agentic_router.llm_request_manager')
    @patch('backend.agentic_router.store_conversation_turn')
    @patch('backend.agentic_router.update_consciousness_from_conversation')
    def test_multiple_requests_consistency_unchanged(
        self, mock_update, mock_store, mock_llm_manager, 
        mock_routing, mock_conversation, mock_consciousness
    ):
        """Test that multiple requests maintain consistent behavior"""
        
        # Setup mocks
        mock_consciousness.return_value = {
            "user_id": self.test_user_id,
            "consciousness_level": 0.7,
            "emotional_state": "curious"
        }
        mock_conversation.return_value = []
        mock_routing.return_value = {"agent_name": "simple_chat", "confidence": 0.8}
        mock_store.return_value = None
        mock_update.return_value = None
        
        # Test multiple different response types
        test_cases = [
            "Simple string response",
            {"response": "Dict response"},
            {"answer": "Answer field response"},
            '{"response": "JSON string response"}'
        ]
        
        for i, mock_response in enumerate(test_cases):
            mock_llm_manager.submit_request = AsyncMock(return_value=mock_response)
            
            # Make API request
            response = client.post(
                "/agent/router/chat",
                json={
                    "query": f"Test query {i}",
                    "user_id": self.test_user_id
                }
            )
            
            # Validate response
            assert response.status_code == 200
            response_data = response.json()
            
            # Should maintain consistent structure
            assert "response" in response_data
            assert isinstance(response_data["response"], str)
            assert len(response_data["response"]) > 0
            
            # Should extract appropriate content
            if isinstance(mock_response, str):
                if mock_response.startswith('{"'):
                    # JSON string should be parsed
                    assert "JSON string response" in response_data["response"]
                else:
                    # Regular string should be returned as-is
                    assert response_data["response"] == mock_response
            elif isinstance(mock_response, dict):
                # Dict should extract appropriate field
                if "response" in mock_response:
                    assert response_data["response"] == mock_response["response"]
                elif "answer" in mock_response:
                    assert response_data["response"] == mock_response["answer"]

if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])