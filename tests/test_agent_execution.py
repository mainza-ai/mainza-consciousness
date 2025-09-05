#!/usr/bin/env python3
"""
Test agent execution to find truncation issue
"""
import asyncio
import sys
import os

# Add the project root directory to Python path using relative path resolution
# Get the directory containing this file (tests/), then go up one level to project root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

async def test_simple_chat_agent():
    """Test the simple chat agent directly"""
    print("🔍 Testing simple chat agent directly...")
    
    try:
        from backend.agents.simple_chat import enhanced_simple_chat_agent
        
        # Test direct execution
        result = await enhanced_simple_chat_agent.run_with_consciousness(
            query="what planet are we on?",
            user_id="test_user"
        )
        
        print(f"Direct agent result type: {type(result)}")
        print(f"Direct agent result length: {len(str(result))} chars")
        print(f"Direct agent result: {result}")
        
        if isinstance(result, str) and len(result.strip()) < 10:
            print("❌ ISSUE: Direct agent execution gives short response!")
        else:
            print("✅ Direct agent execution works fine")
            
    except Exception as e:
        print(f"❌ Direct agent test failed: {e}")
        import traceback
        traceback.print_exc()

async def test_llm_request_manager():
    """Test LLM request manager with simple chat agent"""
    print("\n🔍 Testing LLM request manager...")
    
    try:
        from backend.utils.llm_request_manager import llm_request_manager, RequestPriority
        from backend.agents.simple_chat import enhanced_simple_chat_agent
        
        # Test through request manager
        result = await llm_request_manager.submit_request(
            enhanced_simple_chat_agent.run_with_consciousness,
            RequestPriority.USER_CONVERSATION,
            user_id="test_user",
            timeout=30.0,
            query="what planet are we on?"
        )
        
        print(f"Request manager result type: {type(result)}")
        print(f"Request manager result length: {len(str(result))} chars")
        print(f"Request manager result: {result}")
        
        if isinstance(result, str) and len(result.strip()) < 10:
            print("❌ ISSUE: Request manager gives short response!")
        elif isinstance(result, dict) and result.get("status") == "throttled":
            print("❌ ISSUE: Request is being throttled!")
        else:
            print("✅ Request manager works fine")
            
    except Exception as e:
        print(f"❌ Request manager test failed: {e}")
        import traceback
        traceback.print_exc()

async def test_agentic_router():
    """Test the full agentic router"""
    print("\n🔍 Testing agentic router...")
    
    try:
        from backend.agentic_router import execute_agent
        
        result = await execute_agent(
            user_id="test_user",
            query="what planet are we on?"
        )
        
        print(f"Router result type: {type(result)}")
        print(f"Router result: {result}")
        
        if isinstance(result, dict):
            response = result.get("response", "")
            print(f"Router response length: {len(response)} chars")
            print(f"Router response: '{response}'")
            
            if len(response.strip()) < 10:
                print("❌ ISSUE: Router gives short response!")
            else:
                print("✅ Router works fine")
        else:
            print("❌ ISSUE: Router returned unexpected format!")
            
    except Exception as e:
        print(f"❌ Router test failed: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Run all tests"""
    print("🚀 Testing Agent Execution Pipeline\n")
    
    await test_simple_chat_agent()
    await test_llm_request_manager()
    await test_agentic_router()
    
    print("\n✅ Agent execution test complete!")

if __name__ == "__main__":
    asyncio.run(main())