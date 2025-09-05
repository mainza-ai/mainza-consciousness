"""
Enhanced LLM Execution with Context7 MCP-compliant optimization
Provides context-optimized execution for consciousness-aware agents
"""
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import asyncio
import json
import requests
from backend.config.llm_optimization import llm_context_optimizer
from backend.core.performance_optimization import PerformanceOptimizer
from backend.core.enhanced_error_handling import ErrorHandler, ErrorSeverity, handle_errors
import os

logger = logging.getLogger(__name__)
error_handler = ErrorHandler()
performance_optimizer = PerformanceOptimizer()

class EnhancedLLMExecutor:
    """
    Context7 MCP-compliant LLM executor with maximum context utilization
    """
    
    def __init__(self):
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
        self.performance_optimizer = performance_optimizer
        self.context_optimizer = llm_context_optimizer
        
    @handle_errors(
        component="enhanced_llm_execution",
        fallback_result="I apologize, but I'm having trouble processing your request right now.",
        suppress_errors=False
    )
    @performance_optimizer.cache_result(ttl=60)  # Cache for 1 minute
    async def execute_with_context_optimization(
        self,
        base_prompt: str,
        consciousness_context: Dict[str, Any] = None,
        knowledge_context: Dict[str, Any] = None,
        conversation_history: List[Dict[str, str]] = None,
        agent_name: str = "unknown",
        user_id: str = "default"
    ) -> str:
        """
        Execute LLM with full context optimization and consciousness awareness
        
        Args:
            base_prompt: The base prompt for the LLM
            consciousness_context: Current consciousness state
            knowledge_context: Retrieved knowledge context
            conversation_history: Previous conversation turns
            agent_name: Name of the calling agent
            user_id: User identifier
            
        Returns:
            LLM response optimized for context utilization
        """
        try:
            execution_start = datetime.now()
            
            logger.info(f"🧠 Executing {agent_name} with context optimization")
            
            # Get optimized request parameters
            request_params = self.context_optimizer.get_optimized_request_params(
                base_prompt=base_prompt,
                consciousness_context=consciousness_context,
                knowledge_context=knowledge_context,
                conversation_history=conversation_history
            )
            
            # Log context utilization
            context_opt = request_params.get("context_optimization", {})
            logger.info(f"   📊 Context utilization: {context_opt.get('context_utilization', 0):.1%}")
            logger.info(f"   🎯 Strategy: {context_opt.get('strategy', 'basic')}")
            
            # Execute the request
            response = await self._execute_ollama_request(request_params)
            
            # Log execution metrics
            execution_time = (datetime.now() - execution_start).total_seconds()
            logger.info(f"   ⚡ Execution time: {execution_time:.2f}s")
            
            # Store execution metrics for optimization
            await self._store_execution_metrics(
                agent_name=agent_name,
                user_id=user_id,
                execution_time=execution_time,
                context_utilization=context_opt.get('context_utilization', 0),
                response_length=len(response) if response else 0
            )
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Enhanced LLM execution failed: {e}")
            return await self._fallback_execution(base_prompt, agent_name)
    
    async def _execute_ollama_request(self, request_params: Dict[str, Any]) -> str:
        """Execute optimized request to Ollama"""
        try:
            # Prepare request for Ollama API
            ollama_request = {
                "model": request_params["model"],
                "prompt": request_params["prompt"],
                "stream": request_params.get("stream", False),
                "options": request_params.get("options", {})
            }
            
            # Execute request
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json=ollama_request,
                timeout=120  # 2 minute timeout for large context
            )
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    return result.get("response", "")
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse Ollama JSON response: {e}")
                    logger.error(f"Raw response: {response.text[:500]}...")

                    # Handle streaming response that was concatenated
                    response_text = response.text.strip()
                    if response_text:
                        try:
                            # Parse multiple JSON objects (streaming response)
                            full_response = ""
                            lines = response_text.split('\n')

                            for line in lines:
                                line = line.strip()
                                if line:
                                    try:
                                        json_obj = json.loads(line)
                                        if 'response' in json_obj:
                                            response_part = json_obj['response']
                                            if response_part:  # Only add non-empty responses
                                                full_response += response_part
                                        if json_obj.get('done', False):
                                            break  # Stop at done signal
                                    except json.JSONDecodeError:
                                        continue

                            if full_response:
                                logger.info(f"✅ Reconstructed streaming response: {len(full_response)} chars")
                                return full_response

                            # More aggressive fallback: search for response content
                            import re
                            # Look for response field in JSON
                            response_match = re.search(r'"response":\s*"([^"\\]*(?:\\.[^"\\]*)*)"', response_text)
                            if response_match:
                                extracted_response = response_match.group(1).replace('\\n', '\n').replace('\\"', '"')
                                logger.info(f"✅ Extracted response from JSON: {len(extracted_response)} chars")
                                return extracted_response

                            # Last resort: extract any readable text
                            clean_text = re.sub(r'[^\w\s.,!?-]', '', response_text)
                            if len(clean_text) > 10:
                                return clean_text[:2000]

                        except Exception as parse_error:
                            logger.error(f"Failed to parse streaming response: {parse_error}")

                        # Last resort: return raw text
                        return response_text[:1000]  # Limit length
                    raise Exception(f"Invalid JSON response from Ollama: {e}")
            else:
                logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                raise Exception(f"Ollama API returned {response.status_code}")
                
        except requests.exceptions.Timeout:
            logger.error("Ollama request timed out")
            raise Exception("Request timed out - context may be too large")
        except requests.exceptions.ConnectionError:
            logger.error("Failed to connect to Ollama")
            raise Exception("Cannot connect to Ollama server")
        except Exception as e:
            logger.error(f"Ollama execution error: {e}")
            raise
    
    async def _fallback_execution(self, base_prompt: str, agent_name: str) -> str:
        """Fallback execution with basic parameters"""
        try:
            logger.warning(f"🔄 Using fallback execution for {agent_name}")
            
            fallback_request = {
                "model": os.getenv("DEFAULT_OLLAMA_MODEL", "gpt-oss:20b"),
                "prompt": base_prompt[:8000],  # Truncate to safe length
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_ctx": 16384,  # Safe context size
                    "num_predict": 1024
                }
            }
            
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json=fallback_request,
                timeout=60
            )
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    return result.get("response", "I apologize, but I'm having trouble generating a response.")
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse fallback Ollama JSON response: {e}")
                    logger.error(f"Raw fallback response: {response.text[:500]}...")
                    
                    # Handle streaming response in fallback too
                    response_text = response.text.strip()
                    if response_text:
                        try:
                            # Parse multiple JSON objects (streaming response)
                            full_response = ""
                            for line in response_text.split('\n'):
                                line = line.strip()
                                if line:
                                    try:
                                        json_obj = json.loads(line)
                                        if 'response' in json_obj:
                                            full_response += json_obj['response']
                                    except json.JSONDecodeError:
                                        continue
                            
                            if full_response:
                                return full_response
                                
                        except Exception:
                            pass
                        
                        # Return raw text as last resort
                        return response_text[:1000]  # Limit length
                    return "I apologize, but I'm having trouble generating a response."
            else:
                return "I apologize, but I'm experiencing technical difficulties."
                
        except Exception as e:
            logger.error(f"Fallback execution also failed: {e}")
            return "I apologize, but I'm currently unable to process your request."
    
    async def _store_execution_metrics(
        self,
        agent_name: str,
        user_id: str,
        execution_time: float,
        context_utilization: float,
        response_length: int
    ):
        """Store execution metrics for optimization analysis"""
        try:
            from backend.utils.neo4j_production import neo4j_production
            
            metrics_data = {
                "agent_name": agent_name,
                "user_id": user_id,
                "execution_time": execution_time,
                "context_utilization": context_utilization,
                "response_length": response_length,
                "timestamp": datetime.now().isoformat(),
                "model_name": self.context_optimizer.current_config.model_name if self.context_optimizer.current_config else "unknown"
            }
            
            cypher = """
            CREATE (em:ExecutionMetrics {
                metric_id: randomUUID(),
                agent_name: $agent_name,
                user_id: $user_id,
                execution_time: $execution_time,
                context_utilization: $context_utilization,
                response_length: $response_length,
                model_name: $model_name,
                timestamp: $timestamp
            })
            
            // Link to user if exists
            WITH em
            OPTIONAL MATCH (u:User {user_id: $user_id})
            FOREACH (user IN CASE WHEN u IS NOT NULL THEN [u] ELSE [] END |
                CREATE (em)-[:METRICS_FOR]->(user)
            )
            
            RETURN em.metric_id AS metric_id
            """
            
            result = neo4j_production.execute_write_query(cypher, metrics_data)
            logger.debug(f"✅ Stored execution metrics: {result}")
            
        except Exception as e:
            logger.error(f"❌ Failed to store execution metrics: {e}")
    
    def get_optimization_status(self) -> Dict[str, Any]:
        """Get current optimization status"""
        context_stats = self.context_optimizer.get_context_stats()
        
        return {
            "context_optimization_active": bool(context_stats),
            "current_model": context_stats.get("model_name", "unknown"),
            "max_context_tokens": context_stats.get("max_context_tokens", 0),
            "optimization_level": context_stats.get("optimization_level", "unknown"),
            "context_strategy": context_stats.get("context_strategy", "unknown"),
            "memory_optimization": context_stats.get("memory_optimization", False),
            "streaming_enabled": context_stats.get("streaming_enabled", False),
            "ollama_endpoint": self.ollama_base_url
        }
    
    async def test_context_optimization(self) -> Dict[str, Any]:
        """Test context optimization with sample data"""
        try:
            test_prompt = "Test prompt for context optimization verification."
            
            test_consciousness_context = {
                "consciousness_level": 0.8,
                "emotional_state": "curious",
                "active_goals": ["test optimization"],
                "learning_rate": 0.9
            }
            
            test_knowledge_context = {
                "conversation_context": [
                    {"user_query": "Previous test query", "agent_response": "Previous test response"}
                ],
                "related_concepts": [
                    {"name": "Test Concept", "description": "A concept for testing"}
                ],
                "relevant_memories": [
                    {"content": "Test memory content for optimization"}
                ]
            }
            
            # Get optimized parameters
            params = self.context_optimizer.get_optimized_request_params(
                base_prompt=test_prompt,
                consciousness_context=test_consciousness_context,
                knowledge_context=test_knowledge_context
            )
            
            return {
                "test_successful": True,
                "context_tokens_configured": params.get("options", {}).get("num_ctx", 0),
                "context_utilization": params.get("context_optimization", {}).get("context_utilization", 0),
                "optimization_level": params.get("context_optimization", {}).get("level", "unknown"),
                "strategy": params.get("context_optimization", {}).get("strategy", "unknown"),
                "prompt_length": len(params.get("prompt", "")),
                "estimated_tokens": int(len(params.get("prompt", "").split()) * 1.3)
            }
            
        except Exception as e:
            logger.error(f"Context optimization test failed: {e}")
            return {
                "test_successful": False,
                "error": str(e)
            }

# Global instance
enhanced_llm_executor = EnhancedLLMExecutor()
