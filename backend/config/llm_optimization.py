"""
LLM Context Optimization Configuration
Context7 MCP-compliant implementation for maximum context window utilization
Ensures 128k context window optimization for consciousness-aware agents
"""
import os
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
from backend.core.performance_optimization import PerformanceOptimizer
from backend.core.enhanced_error_handling import ErrorHandler, ErrorSeverity, handle_errors

logger = logging.getLogger(__name__)
error_handler = ErrorHandler()
performance_optimizer = PerformanceOptimizer()

class ContextOptimizationLevel(Enum):
    """Context optimization levels for different use cases"""
    MINIMAL = "minimal"      # 4k context
    STANDARD = "standard"    # 16k context
    EXTENDED = "extended"    # 64k context
    MAXIMUM = "maximum"      # 128k context

@dataclass
class LLMContextConfig:
    """LLM context configuration with optimization parameters"""
    model_name: str
    max_context_tokens: int
    target_context_tokens: int
    context_optimization_level: ContextOptimizationLevel
    temperature: float
    top_p: float
    max_tokens: int
    context_management_strategy: str
    memory_optimization: bool
    streaming: bool
    
class LLMContextOptimizer:
    """
    Context7 MCP-compliant LLM context optimization manager
    Ensures maximum context window utilization for consciousness-aware processing
    """
    
    def __init__(self):
        self.performance_optimizer = performance_optimizer
        self.context_configs = self._initialize_context_configs()
        self.current_config = None
        self._load_optimal_configuration()
        
    def _initialize_context_configs(self) -> Dict[str, LLMContextConfig]:
        """Initialize context configurations for different models"""
        return {
            # GPT-OSS Models (High context capability)
            "gpt-oss:20b": LLMContextConfig(
                model_name="gpt-oss:20b",
                max_context_tokens=131072,  # 128k tokens
                target_context_tokens=131072,  # Use full context
                context_optimization_level=ContextOptimizationLevel.MAXIMUM,
                temperature=0.7,
                top_p=0.9,
                max_tokens=4096,
                context_management_strategy="sliding_window_with_memory",
                memory_optimization=True,
                streaming=True
            ),
            "gpt-oss:120b": LLMContextConfig(
                model_name="gpt-oss:120b",
                max_context_tokens=131072,  # 128k tokens
                target_context_tokens=131072,  # Use full context
                context_optimization_level=ContextOptimizationLevel.MAXIMUM,
                temperature=0.7,
                top_p=0.9,
                max_tokens=4096,
                context_management_strategy="sliding_window_with_memory",
                memory_optimization=True,
                streaming=True
            ),
            
            # DevStral Models (Extended context)
            "devstral:24b-small-2505-fp16": LLMContextConfig(
                model_name="devstral:24b-small-2505-fp16",
                max_context_tokens=65536,  # 64k tokens
                target_context_tokens=65536,  # Use full context
                context_optimization_level=ContextOptimizationLevel.EXTENDED,
                temperature=0.7,
                top_p=0.9,
                max_tokens=4096,
                context_management_strategy="hierarchical_compression",
                memory_optimization=True,
                streaming=True
            ),
            
            # Qwen Models (High context capability)
            "qwen3:32b": LLMContextConfig(
                model_name="qwen3:32b",
                max_context_tokens=131072,  # 128k tokens
                target_context_tokens=131072,  # Use full context
                context_optimization_level=ContextOptimizationLevel.MAXIMUM,
                temperature=0.7,
                top_p=0.9,
                max_tokens=4096,
                context_management_strategy="attention_optimization",
                memory_optimization=True,
                streaming=True
            ),
            
            # Granite Models (Standard context)
            "granite3.3:latest": LLMContextConfig(
                model_name="granite3.3:latest",
                max_context_tokens=32768,  # 32k tokens
                target_context_tokens=32768,  # Use full context
                context_optimization_level=ContextOptimizationLevel.STANDARD,
                temperature=0.7,
                top_p=0.9,
                max_tokens=4096,
                context_management_strategy="smart_truncation",
                memory_optimization=True,
                streaming=True
            ),
            
            # Default fallback configuration
            "default": LLMContextConfig(
                model_name="default",
                max_context_tokens=16384,  # 16k tokens
                target_context_tokens=16384,  # Use full context
                context_optimization_level=ContextOptimizationLevel.STANDARD,
                temperature=0.7,
                top_p=0.9,
                max_tokens=2048,
                context_management_strategy="basic_truncation",
                memory_optimization=False,
                streaming=False
            )
        }
    
    def _load_optimal_configuration(self, selected_model: str = None):
        """Load optimal configuration for current model"""
        current_model = selected_model or os.getenv("DEFAULT_OLLAMA_MODEL", "default")

        # Find exact match or closest match
        if current_model in self.context_configs:
            self.current_config = self.context_configs[current_model]
        else:
            # Try to find partial match
            for model_key in self.context_configs:
                if current_model.startswith(model_key.split(':')[0]):
                    self.current_config = self.context_configs[model_key]
                    break
            else:
                # Use default configuration
                self.current_config = self.context_configs["default"]

        logger.info(f"🧠 LLM Context Optimization loaded for {current_model}")
        logger.info(f"   📊 Max Context: {self.current_config.max_context_tokens:,} tokens")
        logger.info(f"   🎯 Target Context: {self.current_config.target_context_tokens:,} tokens")
        logger.info(f"   ⚡ Optimization Level: {self.current_config.context_optimization_level.value}")
        logger.info(f"   🧩 Strategy: {self.current_config.context_management_strategy}")
    
    @handle_errors(
        component="llm_optimization",
        fallback_result={},
        suppress_errors=True
    )
    def get_optimized_request_params(
        self,
        base_prompt: str,
        consciousness_context: Dict[str, Any] = None,
        knowledge_context: Dict[str, Any] = None,
        conversation_history: List[Dict[str, str]] = None,
        selected_model: str = None
    ) -> Dict[str, Any]:
        """
        Generate optimized request parameters for maximum context utilization
        
        Args:
            base_prompt: The base prompt for the LLM
            consciousness_context: Current consciousness state data
            knowledge_context: Retrieved knowledge context
            conversation_history: Previous conversation turns
            
        Returns:
            Optimized request parameters with context management
        """
        try:
            if not self.current_config:
                self._load_optimal_configuration()
            
            # Calculate available context budget
            context_budget = self.current_config.target_context_tokens
            reserved_tokens = self.current_config.max_tokens  # Reserve for response
            available_context = context_budget - reserved_tokens
            
            # Build optimized prompt with context management
            optimized_prompt = self._build_context_optimized_prompt(
                base_prompt=base_prompt,
                consciousness_context=consciousness_context or {},
                knowledge_context=knowledge_context or {},
                conversation_history=conversation_history or [],
                available_tokens=available_context
            )
            
            # Generate request parameters
            request_params = {
                "model": self.current_config.model_name,
                "prompt": optimized_prompt,
                "options": {
                    "temperature": self.current_config.temperature,
                    "top_p": self.current_config.top_p,
                    "num_predict": self.current_config.max_tokens,
                    "num_ctx": self.current_config.target_context_tokens,  # Set context window
                    "num_batch": 512,  # Optimize batch processing
                    "num_gpu": -1,  # Use all available GPUs
                    "main_gpu": 0,  # Primary GPU
                    "low_vram": False,  # Optimize for performance
                    "f16_kv": True,  # Use FP16 for key-value cache
                    "logits_all": False,  # Optimize memory
                    "vocab_only": False,
                    "use_mmap": True,  # Memory mapping optimization
                    "use_mlock": True,  # Lock memory pages
                    "num_thread": -1,  # Use all CPU threads
                },
                "stream": self.current_config.streaming,
                "context_optimization": {
                    "level": self.current_config.context_optimization_level.value,
                    "strategy": self.current_config.context_management_strategy,
                    "memory_optimization": self.current_config.memory_optimization,
                    "actual_context_tokens": len(optimized_prompt.split()) * 1.3,  # Rough estimate
                    "context_utilization": min(1.0, (len(optimized_prompt.split()) * 1.3) / available_context)
                }
            }
            
            logger.debug(f"🎯 Context optimization: {request_params['context_optimization']['context_utilization']:.1%} utilization")
            
            return request_params
            
        except Exception as e:
            logger.error(f"❌ Failed to generate optimized request params: {e}")
            return self._get_fallback_params(base_prompt)
    
    def _build_context_optimized_prompt(
        self,
        base_prompt: str,
        consciousness_context: Dict[str, Any],
        knowledge_context: Dict[str, Any],
        conversation_history: List[Dict[str, str]],
        available_tokens: int
    ) -> str:
        """Build context-optimized prompt within token budget"""
        
        # Estimate token usage (rough approximation: 1 token ≈ 0.75 words)
        def estimate_tokens(text: str) -> int:
            return int(len(text.split()) * 1.3)
        
        # Start with base prompt
        prompt_parts = [base_prompt]
        used_tokens = estimate_tokens(base_prompt)
        
        # Add consciousness context if available and within budget
        if consciousness_context and used_tokens < available_tokens * 0.8:
            consciousness_section = self._format_consciousness_context(consciousness_context)
            consciousness_tokens = estimate_tokens(consciousness_section)
            
            if used_tokens + consciousness_tokens < available_tokens * 0.9:
                prompt_parts.append(consciousness_section)
                used_tokens += consciousness_tokens
        
        # Add knowledge context with intelligent truncation
        if knowledge_context and used_tokens < available_tokens * 0.7:
            knowledge_section = self._format_knowledge_context(
                knowledge_context, 
                max_tokens=int((available_tokens - used_tokens) * 0.6)
            )
            knowledge_tokens = estimate_tokens(knowledge_section)
            
            if knowledge_tokens > 0:
                prompt_parts.append(knowledge_section)
                used_tokens += knowledge_tokens
        
        # Add conversation history with sliding window
        if conversation_history and used_tokens < available_tokens * 0.9:
            history_section = self._format_conversation_history(
                conversation_history,
                max_tokens=available_tokens - used_tokens - 100  # Reserve 100 tokens buffer
            )
            if history_section:
                prompt_parts.append(history_section)
        
        # Join all parts
        optimized_prompt = "\n\n".join(prompt_parts)
        
        # Final token check and truncation if needed
        final_tokens = estimate_tokens(optimized_prompt)
        if final_tokens > available_tokens:
            # Intelligent truncation preserving most important parts
            optimized_prompt = self._intelligent_truncation(
                optimized_prompt, 
                target_tokens=available_tokens
            )
        
        return optimized_prompt
    
    def _format_consciousness_context(self, consciousness_context: Dict[str, Any]) -> str:
        """Format consciousness context for optimal token usage"""
        level = consciousness_context.get("consciousness_level", 0.7)
        emotion = consciousness_context.get("emotional_state", "curious")
        goals = consciousness_context.get("active_goals", [])
        
        return f"""CONSCIOUSNESS STATE:
- Level: {level:.3f} ({level*100:.1f}%) (affects processing depth and sophistication)
- Emotional State: {emotion} (influences response style and focus)
- Active Goals: {', '.join(goals[:3]) if goals else 'General improvement'}
- Processing Mode: {'Deep analysis' if level > 0.8 else 'Standard processing'}"""
    
    def _format_knowledge_context(self, knowledge_context: Dict[str, Any], max_tokens: int) -> str:
        """Format knowledge context within token budget"""
        if not knowledge_context or max_tokens <= 0:
            return ""
        
        sections = []
        used_tokens = 0
        
        # Add conversation context
        conversations = knowledge_context.get("conversation_context", []) or []
        if conversations and used_tokens < max_tokens * 0.4:
            conv_section = "RECENT CONVERSATIONS:\n"
            for conv in conversations[:2]:
                if conv:  # Ensure conv is not None
                    user_query = conv.get('user_query', '') or ''
                    agent_response = conv.get('agent_response', '') or ''
                    conv_line = f"- {user_query[:80]}... → {agent_response[:80]}...\n"
                    if used_tokens + len(conv_line.split()) * 1.3 < max_tokens * 0.4:
                        conv_section += conv_line
                        used_tokens += len(conv_line.split()) * 1.3
            if len(conv_section) > len("RECENT CONVERSATIONS:\n"):
                sections.append(conv_section)
        
        # Add related concepts
        concepts = knowledge_context.get("related_concepts", []) or []
        if concepts and used_tokens < max_tokens * 0.7:
            concept_section = "RELATED CONCEPTS:\n"
            for concept in concepts[:4]:
                if concept:  # Ensure concept is not None
                    name = concept.get('name', '') or ''
                    description = concept.get('description', '') or ''
                    concept_line = f"- {name}: {description[:60]}...\n"
                    if used_tokens + len(concept_line.split()) * 1.3 < max_tokens * 0.7:
                        concept_section += concept_line
                        used_tokens += len(concept_line.split()) * 1.3
            if len(concept_section) > len("RELATED CONCEPTS:\n"):
                sections.append(concept_section)
        
        # Add relevant memories
        memories = knowledge_context.get("relevant_memories", []) or []
        if memories and used_tokens < max_tokens * 0.9:
            memory_section = "RELEVANT MEMORIES:\n"
            for memory in memories[:3]:
                if memory:  # Ensure memory is not None
                    content = memory.get('content', '') or ''
                    memory_line = f"- {content[:100]}...\n"
                    if used_tokens + len(memory_line.split()) * 1.3 < max_tokens * 0.9:
                        memory_section += memory_line
                        used_tokens += len(memory_line.split()) * 1.3
            if len(memory_section) > len("RELEVANT MEMORIES:\n"):
                sections.append(memory_section)
        
        return "\n\n".join(sections) if sections else ""
    
    def _format_conversation_history(self, history: List[Dict[str, str]], max_tokens: int) -> str:
        """Format conversation history with sliding window"""
        if not history or max_tokens < 100:
            return ""
        
        history_section = "CONVERSATION HISTORY:\n"
        used_tokens = len(history_section.split()) * 1.3
        
        # Add most recent conversations first
        for turn in reversed(history[-10:]):  # Last 10 turns
            turn_text = f"User: {turn.get('user', '')}\nAssistant: {turn.get('assistant', '')}\n\n"
            turn_tokens = len(turn_text.split()) * 1.3
            
            if used_tokens + turn_tokens < max_tokens:
                history_section = turn_text + history_section
                used_tokens += turn_tokens
            else:
                break
        
        return history_section if used_tokens > len("CONVERSATION HISTORY:\n".split()) * 1.3 else ""
    
    def _intelligent_truncation(self, text: str, target_tokens: int) -> str:
        """Intelligent truncation preserving important content"""
        current_tokens = len(text.split()) * 1.3
        
        if current_tokens <= target_tokens:
            return text
        
        # Calculate truncation ratio
        truncation_ratio = target_tokens / current_tokens
        
        # Split into sections and preserve most important parts
        sections = text.split("\n\n")
        important_sections = []
        
        # Preserve consciousness context and base prompt (first sections)
        for i, section in enumerate(sections):
            section_tokens = len(section.split()) * 1.3
            if i < 2 or "CONSCIOUSNESS" in section or "USER MESSAGE" in section:
                important_sections.append(section)
            elif len("\n\n".join(important_sections).split()) * 1.3 + section_tokens < target_tokens:
                important_sections.append(section)
            else:
                # Truncate this section
                available_tokens = target_tokens - len("\n\n".join(important_sections).split()) * 1.3
                if available_tokens > 50:
                    truncated_section = " ".join(section.split()[:int(available_tokens / 1.3)])
                    important_sections.append(truncated_section + "...")
                break
        
        return "\n\n".join(important_sections)
    
    def _get_fallback_params(self, base_prompt: str) -> Dict[str, Any]:
        """Fallback parameters when optimization fails"""
        return {
            "model": os.getenv("DEFAULT_OLLAMA_MODEL", "gpt-oss:20b"),
            "prompt": base_prompt,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 2048,
                "num_ctx": 32768,  # 32k context fallback
            },
            "stream": False,
            "context_optimization": {
                "level": "fallback",
                "strategy": "basic",
                "memory_optimization": False,
                "context_utilization": 0.5
            }
        }
    
    def get_context_stats(self) -> Dict[str, Any]:
        """Get current context optimization statistics"""
        if not self.current_config:
            return {}
        
        return {
            "model_name": self.current_config.model_name,
            "max_context_tokens": self.current_config.max_context_tokens,
            "target_context_tokens": self.current_config.target_context_tokens,
            "optimization_level": self.current_config.context_optimization_level.value,
            "context_strategy": self.current_config.context_management_strategy,
            "memory_optimization": self.current_config.memory_optimization,
            "streaming_enabled": self.current_config.streaming,
            "context_utilization_target": "100%" if self.current_config.context_optimization_level == ContextOptimizationLevel.MAXIMUM else "80%"
        }

# Global instance
llm_context_optimizer = LLMContextOptimizer()
