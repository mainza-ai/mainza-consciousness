#!/usr/bin/env python3
"""
Test script to investigate LLM response truncation issue
"""
import asyncio
import requests
import json
import os
from backend.agentic_config import local_llm
from backend.config.llm_optimization import llm_context_optimizer

async def test_direct_ollama():
    """Test direct Ollama API call"""
    print("🔍 Testing direct Ollama API call...")
    
    ollama_url = "http://localhost:11434/api/generate"
    
    test_request = {
        "model": "devstral:latest",
        "prompt": "What planet are we on? Please provide a comprehensive answer about Earth.",
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 4096,  # Allow up to 4096 tokens
            "num_ctx": 32768,     # 32k context
            "top_p": 0.9
        }
    }
    
    try:
        response = requests.post(ollama_url, json=test_request, timeout=60)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                response_text = result.get("response", "")
                print(f"Response Length: {len(response_text)} characters")
                print(f"Response: {response_text}")
                
                # Check if response was truncated
                if len(response_text) < 10:
                    print("❌ Response appears to be truncated!")
                else:
                    print("✅ Response looks complete")
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {e}")
                print(f"Raw response: {response.text[:500]}...")
        else:
            print(f"❌ HTTP error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

async def test_pydantic_ai():
    """Test pydantic-ai agent"""
    print("\n🔍 Testing pydantic-ai agent...")
    
    try:
        from backend.agents.simple_chat import simple_chat_agent
        
        if simple_chat_agent:
            result = await simple_chat_agent.run("What planet are we on? Please provide a comprehensive answer about Earth.")
            print(f"Pydantic-AI Response Length: {len(result)} characters")
            print(f"Pydantic-AI Response: {result}")
            
            if len(result) < 10:
                print("❌ Pydantic-AI response appears to be truncated!")
            else:
                print("✅ Pydantic-AI response looks complete")
        else:
            print("❌ Simple chat agent not available")
            
    except Exception as e:
        print(f"❌ Pydantic-AI test failed: {e}")

async def test_enhanced_llm_executor():
    """Test enhanced LLM executor"""
    print("\n🔍 Testing enhanced LLM executor...")
    
    try:
        from backend.utils.enhanced_llm_execution import enhanced_llm_executor
        
        result = await enhanced_llm_executor.execute_with_context_optimization(
            base_prompt="What planet are we on? Please provide a comprehensive answer about Earth.",
            consciousness_context={
                "consciousness_level": 0.8,
                "emotional_state": "curious",
                "active_goals": ["learning"],
                "learning_rate": 0.9
            },
            agent_name="test_agent",
            user_id="test_user"
        )
        
        print(f"Enhanced Executor Response Length: {len(result)} characters")
        print(f"Enhanced Executor Response: {result}")
        
        if len(result) < 10:
            print("❌ Enhanced executor response appears to be truncated!")
        else:
            print("✅ Enhanced executor response looks complete")
            
    except Exception as e:
        print(f"❌ Enhanced executor test failed: {e}")

async def test_context_optimization():
    """Test context optimization parameters"""
    print("\n🔍 Testing context optimization parameters...")
    
    try:
        params = llm_context_optimizer.get_optimized_request_params(
            base_prompt="What planet are we on? Please provide a comprehensive answer about Earth.",
            consciousness_context={
                "consciousness_level": 0.8,
                "emotional_state": "curious"
            }
        )
        
        print("Context Optimization Parameters:")
        print(f"  Model: {params.get('model')}")
        print(f"  Max Tokens: {params.get('options', {}).get('num_predict')}")
        print(f"  Context Size: {params.get('options', {}).get('num_ctx')}")
        print(f"  Temperature: {params.get('options', {}).get('temperature')}")
        print(f"  Context Utilization: {params.get('context_optimization', {}).get('context_utilization')}")
        
        # Test with these exact parameters
        print("\n🔍 Testing with optimized parameters...")
        
        ollama_request = {
            "model": params.get("model"),
            "prompt": params.get("prompt"),
            "stream": params.get("stream", False),
            "options": params.get("options", {})
        }
        
        response = requests.post("http://localhost:11434/api/generate", json=ollama_request, timeout=60)
        
        if response.status_code == 200:
            try:
                result = response.json()
                response_text = result.get("response", "")
                print(f"Optimized Response Length: {len(response_text)} characters")
                print(f"Optimized Response: {response_text}")
                
                if len(response_text) < 10:
                    print("❌ Optimized response appears to be truncated!")
                else:
                    print("✅ Optimized response looks complete")
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {e}")
                print(f"Raw response: {response.text[:500]}...")
        else:
            print(f"❌ HTTP error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Context optimization test failed: {e}")

async def main():
    """Run all tests"""
    print("🚀 Starting LLM Response Truncation Investigation\n")
    
    await test_direct_ollama()
    await test_pydantic_ai()
    await test_enhanced_llm_executor()
    await test_context_optimization()
    
    print("\n✅ Investigation complete!")

if __name__ == "__main__":
    asyncio.run(main())