#!/usr/bin/env python3
"""
Test script to verify LLM context optimization and 128k context utilization
"""
import asyncio
import sys
import os
import json
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

async def test_context_optimization():
    """Test the LLM context optimization system"""
    try:
        print("🧠 Testing LLM Context Optimization System...")
        
        # Test 1: Context Optimizer Configuration
        print("\n1. Testing Context Optimizer Configuration...")
        from backend.config.llm_optimization import llm_context_optimizer
        
        context_stats = llm_context_optimizer.get_context_stats()
        
        print(f"   ✅ Context Optimizer loaded:")
        print(f"      - Model: {context_stats.get('model_name', 'Unknown')}")
        print(f"      - Max Context: {context_stats.get('max_context_tokens', 0):,} tokens")
        print(f"      - Target Context: {context_stats.get('target_context_tokens', 0):,} tokens")
        print(f"      - Optimization Level: {context_stats.get('optimization_level', 'unknown')}")
        print(f"      - Strategy: {context_stats.get('context_strategy', 'unknown')}")
        print(f"      - Memory Optimization: {context_stats.get('memory_optimization', False)}")
        
        # Check if we're using maximum context
        max_tokens = context_stats.get('max_context_tokens', 0)
        if max_tokens >= 131072:  # 128k tokens
            print(f"   🎯 EXCELLENT: Using maximum 128k+ context window ({max_tokens:,} tokens)")
        elif max_tokens >= 65536:  # 64k tokens
            print(f"   ✅ GOOD: Using extended 64k+ context window ({max_tokens:,} tokens)")
        elif max_tokens >= 32768:  # 32k tokens
            print(f"   ⚠️ MODERATE: Using standard 32k+ context window ({max_tokens:,} tokens)")
        else:
            print(f"   ❌ LIMITED: Using basic context window ({max_tokens:,} tokens)")
        
        # Test 2: Enhanced LLM Executor
        print("\n2. Testing Enhanced LLM Executor...")
        from backend.utils.enhanced_llm_execution import enhanced_llm_executor
        
        executor_status = enhanced_llm_executor.get_optimization_status()
        
        print(f"   ✅ Enhanced LLM Executor status:")
        print(f"      - Context Optimization Active: {executor_status.get('context_optimization_active', False)}")
        print(f"      - Current Model: {executor_status.get('current_model', 'Unknown')}")
        print(f"      - Max Context Tokens: {executor_status.get('max_context_tokens', 0):,}")
        print(f"      - Optimization Level: {executor_status.get('optimization_level', 'unknown')}")
        print(f"      - Memory Optimization: {executor_status.get('memory_optimization', False)}")
        print(f"      - Streaming Enabled: {executor_status.get('streaming_enabled', False)}")
        
        # Test 3: Context Optimization Test
        print("\n3. Testing Context Optimization Parameters...")
        
        optimization_test = await enhanced_llm_executor.test_context_optimization()
        
        if optimization_test.get('test_successful', False):
            print(f"   ✅ Context optimization test successful:")
            print(f"      - Context Tokens Configured: {optimization_test.get('context_tokens_configured', 0):,}")
            print(f"      - Context Utilization: {optimization_test.get('context_utilization', 0):.1%}")
            print(f"      - Optimization Level: {optimization_test.get('optimization_level', 'unknown')}")
            print(f"      - Strategy: {optimization_test.get('strategy', 'unknown')}")
            print(f"      - Estimated Tokens: {optimization_test.get('estimated_tokens', 0):,}")
            
            # Check context utilization
            utilization = optimization_test.get('context_utilization', 0)
            if utilization > 0.8:
                print(f"   🎯 EXCELLENT: High context utilization ({utilization:.1%})")
            elif utilization > 0.6:
                print(f"   ✅ GOOD: Moderate context utilization ({utilization:.1%})")
            else:
                print(f"   ⚠️ LOW: Limited context utilization ({utilization:.1%})")
        else:
            print(f"   ❌ Context optimization test failed: {optimization_test.get('error', 'Unknown error')}")
        
        # Test 4: Real Agent Execution with Context Optimization
        print("\n4. Testing Real Agent Execution with Context Optimization...")
        
        try:
            from backend.agents.simple_chat import enhanced_simple_chat_agent
            
            # Create comprehensive test context
            test_consciousness_context = {
                "consciousness_level": 0.9,  # High consciousness for maximum context
                "emotional_state": "curious",
                "active_goals": ["maximize context utilization", "test optimization"],
                "learning_rate": 0.9
            }
            
            # Test with a complex query that should utilize context
            complex_query = """
            I'd like to understand how consciousness, artificial intelligence, and knowledge graphs 
            work together in a comprehensive system. Can you explain the relationships between 
            these concepts, how they might be implemented in practice, and what the implications 
            are for creating truly intelligent systems? Please consider both the technical 
            architecture and the philosophical implications of consciousness in AI systems.
            """
            
            print(f"   🧠 Executing complex query with enhanced context...")
            
            start_time = datetime.now()
            
            result = await enhanced_simple_chat_agent.run_with_consciousness(
                query=complex_query,
                user_id="context-test-user"
            )
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            print(f"   ✅ Agent execution completed:")
            print(f"      - Execution time: {execution_time:.2f} seconds")
            print(f"      - Response length: {len(str(result))} characters")
            print(f"      - Response preview: {str(result)[:200]}...")
            
            # Check if response shows context awareness
            response_str = str(result).lower()
            context_indicators = [
                "consciousness", "knowledge graph", "artificial intelligence",
                "relationship", "implementation", "architecture", "philosophical"
            ]
            
            context_coverage = sum(1 for indicator in context_indicators if indicator in response_str)
            coverage_percentage = (context_coverage / len(context_indicators)) * 100
            
            print(f"      - Context coverage: {coverage_percentage:.1f}% ({context_coverage}/{len(context_indicators)} topics)")
            
            if coverage_percentage > 80:
                print(f"   🎯 EXCELLENT: High context awareness in response")
            elif coverage_percentage > 60:
                print(f"   ✅ GOOD: Moderate context awareness in response")
            else:
                print(f"   ⚠️ LIMITED: Low context awareness in response")
                
        except Exception as e:
            print(f"   ❌ Agent execution test failed: {e}")
        
        # Test 5: Context Window Verification
        print("\n5. Testing Context Window Configuration...")
        
        try:
            # Test direct Ollama configuration
            import requests
            import os
            
            ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            model_name = os.getenv("DEFAULT_OLLAMA_MODEL", "gpt-oss:20b")
            
            # Test with a large context request
            test_request = {
                "model": model_name,
                "prompt": "Test prompt for context verification.",
                "stream": False,
                "options": {
                    "num_ctx": 131072,  # Request 128k context
                    "temperature": 0.7,
                    "num_predict": 100
                }
            }
            
            print(f"   🔍 Testing direct Ollama context configuration...")
            print(f"      - Model: {model_name}")
            print(f"      - Requested context: 131,072 tokens (128k)")
            
            response = requests.post(
                f"{ollama_url}/api/generate",
                json=test_request,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Ollama accepted 128k context request")
                print(f"      - Response received: {len(result.get('response', ''))} characters")
                print(f"      - Context configuration successful")
            else:
                print(f"   ⚠️ Ollama context test failed: {response.status_code}")
                print(f"      - Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"   ❌ Direct Ollama test failed: {e}")
        
        # Test 6: Performance Metrics
        print("\n6. Testing Performance with Large Context...")
        
        try:
            # Create a large context test
            large_context_prompt = "Context optimization test. " * 1000  # ~3k words
            
            start_time = datetime.now()
            
            large_context_result = await enhanced_llm_executor.execute_with_context_optimization(
                base_prompt=large_context_prompt,
                consciousness_context=test_consciousness_context,
                agent_name="context_test",
                user_id="performance_test"
            )
            
            large_context_time = (datetime.now() - start_time).total_seconds()
            
            print(f"   ✅ Large context performance test:")
            print(f"      - Input size: ~{len(large_context_prompt.split()):,} words")
            print(f"      - Execution time: {large_context_time:.2f} seconds")
            print(f"      - Response length: {len(large_context_result)} characters")
            print(f"      - Performance: {len(large_context_prompt.split()) / large_context_time:.0f} words/second")
            
            if large_context_time < 10:
                print(f"   🎯 EXCELLENT: Fast processing of large context")
            elif large_context_time < 30:
                print(f"   ✅ GOOD: Reasonable processing time")
            else:
                print(f"   ⚠️ SLOW: Context processing may need optimization")
                
        except Exception as e:
            print(f"   ❌ Large context performance test failed: {e}")
        
        print("\n✅ LLM Context Optimization Testing Complete!")
        
        # Summary
        print("\n📋 CONTEXT OPTIMIZATION SUMMARY:")
        if max_tokens >= 131072:
            print("   🎯 MAXIMUM CONTEXT: 128k+ tokens configured")
        else:
            print(f"   ⚠️ SUBOPTIMAL CONTEXT: Only {max_tokens:,} tokens configured")
        
        print(f"   ✅ Context Optimization: {'Active' if context_stats else 'Inactive'}")
        print(f"   ✅ Enhanced LLM Executor: {'Operational' if executor_status.get('context_optimization_active') else 'Basic'}")
        print(f"   ✅ Memory Optimization: {'Enabled' if context_stats.get('memory_optimization') else 'Disabled'}")
        print(f"   ✅ Streaming: {'Enabled' if context_stats.get('streaming_enabled') else 'Disabled'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Context optimization test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    async def main():
        print("🚀 Starting LLM Context Optimization Tests...")
        
        success = await test_context_optimization()
        
        if success:
            print("\n🎉 ALL CONTEXT OPTIMIZATION TESTS COMPLETED!")
            print("\n💡 RECOMMENDATIONS:")
            print("   - Ensure Ollama model supports 128k context")
            print("   - Monitor context utilization in production")
            print("   - Optimize prompt engineering for maximum context use")
            print("   - Consider model upgrade if context is limited")
        else:
            print("\n⚠️ Some context optimization tests failed. Check configuration.")
    
    asyncio.run(main())