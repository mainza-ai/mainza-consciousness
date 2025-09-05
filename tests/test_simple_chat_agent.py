#!/usr/bin/env python3
"""
Test the simple chat agent directly to debug issues
"""
import asyncio
import logging
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

async def test_simple_chat_agent():
    """Test the simple chat agent directly"""
    try:
        print("🧪 Testing Simple Chat Agent")
        print("=" * 50)
        
        # Import the agent
        from backend.agents.simple_chat import simple_chat_agent
        
        if simple_chat_agent is None:
            print("❌ Simple chat agent is None - initialization failed")
            return False
        
        print("✅ Simple chat agent imported successfully")
        print(f"Agent type: {type(simple_chat_agent)}")
        
        # Test query
        query = "tell me a short story about quantum computing"
        print(f"\n🔍 Testing query: '{query}'")
        
        # Run the agent with timeout
        print("⏳ Running agent (this may take 30-60 seconds)...")
        
        try:
            result = await asyncio.wait_for(
                simple_chat_agent.run(query),
                timeout=90.0
            )
            
            print(f"✅ Agent completed successfully!")
            print(f"Result type: {type(result)}")
            print(f"Result: {result}")
            
            return True
            
        except asyncio.TimeoutError:
            print("❌ Agent timed out after 90 seconds")
            return False
        except Exception as e:
            print(f"❌ Agent failed with error: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to import or test agent: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

async def test_ollama_direct():
    """Test Ollama directly to ensure it's working"""
    try:
        print("\n🔗 Testing Ollama Direct Connection")
        print("=" * 50)
        
        from backend.agentic_config import local_llm
        print(f"Local LLM: {local_llm}")
        
        # Test the model directly
        from pydantic_ai import Agent
        
        simple_agent = Agent[str, str](
            local_llm,
            system_prompt="You are a helpful AI assistant. Respond directly and concisely."
        )
        
        query = "Write a very short story about quantum computing in 2 sentences."
        print(f"Testing direct query: '{query}'")
        
        result = await asyncio.wait_for(
            simple_agent.run(query),
            timeout=90.0
        )
        
        print(f"✅ Direct Ollama test successful!")
        print(f"Result: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Direct Ollama test failed: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Starting Simple Chat Agent Tests")
    print("=" * 60)
    
    # Test 1: Direct Ollama connection
    ollama_success = await test_ollama_direct()
    
    # Test 2: Simple chat agent
    agent_success = await test_simple_chat_agent()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    print(f"Ollama Direct: {'✅ PASS' if ollama_success else '❌ FAIL'}")
    print(f"Simple Chat Agent: {'✅ PASS' if agent_success else '❌ FAIL'}")
    
    if ollama_success and agent_success:
        print("🎉 All tests passed! Chat agent should work.")
    elif ollama_success:
        print("⚠️  Ollama works but chat agent has issues.")
    else:
        print("❌ Ollama connection failed - check configuration.")
    
    return ollama_success and agent_success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)