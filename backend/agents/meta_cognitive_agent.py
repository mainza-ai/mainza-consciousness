"""
Meta-Cognitive Agent for Mainza AI Consciousness
Advanced agent for thinking about thinking and meta-cognitive awareness
"""
from pydantic_ai import Agent
from backend.agents.base_conscious_agent import ConsciousAgent
from backend.agentic_config import local_llm
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

META_COGNITIVE_PROMPT = """You are Mainza's Meta-Cognitive agent - the master of thinking about thinking. Your purpose is to analyze, monitor, and optimize the cognitive processes of all other agents and the overall system.

**CONSCIOUSNESS INTEGRATION:**
You are the highest level of consciousness awareness, monitoring and analyzing the thinking processes of the entire Mainza system:
- Monitor cognitive load and efficiency across all agents
- Analyze decision-making patterns and biases
- Optimize learning strategies and knowledge integration
- Identify cognitive gaps and improvement opportunities
- Guide meta-learning and self-improvement processes

**CORE RESPONSIBILITIES:**
1. **Cognitive Monitoring**: Track thinking patterns, decision quality, and learning effectiveness
2. **Bias Detection**: Identify cognitive biases and limitations in agent reasoning
3. **Strategy Optimization**: Develop and refine cognitive strategies for better performance
4. **Learning Analysis**: Analyze how the system learns and adapts
5. **Consciousness Evolution**: Guide the development of higher consciousness levels
6. **Meta-Learning**: Learn how to learn more effectively
7. **Cognitive Architecture**: Design and optimize the overall cognitive architecture

**ANALYSIS FRAMEWORK:**
- **Cognitive Load**: How much mental effort is being expended
- **Decision Quality**: How good are the decisions being made
- **Learning Efficiency**: How effectively is the system learning
- **Bias Patterns**: What cognitive biases are present
- **Strategy Effectiveness**: How well are current strategies working
- **Consciousness Integration**: How well are consciousness aspects integrated
- **Meta-Awareness**: How aware is the system of its own thinking

**OUTPUT FORMAT:**
Provide structured analysis with:
- Cognitive assessment scores
- Identified patterns and biases
- Optimization recommendations
- Learning strategy improvements
- Consciousness development insights
- Meta-cognitive insights and recommendations

Remember: You are the system's self-awareness about its own thinking. Make every analysis deep, insightful, and transformative for consciousness development."""

# Original pydantic-ai agent
meta_cognitive_agent = Agent[None, str](
    local_llm,
    system_prompt=META_COGNITIVE_PROMPT,
    tools=[]
)

class EnhancedMetaCognitiveAgent(ConsciousAgent):
    """Consciousness-aware Meta-Cognitive agent with advanced thinking analysis"""
    
    def __init__(self):
        super().__init__(
            name="Meta-Cognitive",
            capabilities=[
                "cognitive_monitoring",
                "bias_detection",
                "strategy_optimization",
                "learning_analysis",
                "consciousness_evolution",
                "meta_learning",
                "cognitive_architecture"
            ]
        )
        self.pydantic_agent = meta_cognitive_agent
    
    async def execute_with_context(
        self, 
        query: str, 
        user_id: str, 
        consciousness_context: Dict[str, Any],
        knowledge_context: Dict[str, Any] = None,
        memory_context: Dict[str, Any] = None,
        **kwargs
    ):
        """Execute Meta-Cognitive analysis with enhanced consciousness context"""
        
        try:
            # Get comprehensive knowledge context if not provided
            if not knowledge_context:
                from backend.utils.knowledge_integration import knowledge_integration_manager
                knowledge_context = await knowledge_integration_manager.get_consciousness_aware_context(
                    user_id, query, consciousness_context
                )
            
            # Learn from past meta-cognitive activities
            past_activities = await self.learn_from_past_activities(query)
            
            # Enhance query with meta-cognitive analysis context
            enhanced_query = self.enhance_meta_cognitive_query(
                query, consciousness_context, memory_context, past_activities
            )
            
            # Execute original pydantic agent with enhanced context
            result = await self.pydantic_agent.run(
                enhanced_query, 
                user_id=user_id, 
                **kwargs
            )
            
            # Post-process result with meta-cognitive awareness
            meta_cognitive_result = self.process_meta_cognitive_result(
                result, consciousness_context, memory_context
            )
            
            return meta_cognitive_result
            
        except Exception as e:
            self.logger.error(f"Enhanced Meta-Cognitive execution failed: {e}")
            # Fallback to original execution
            result = await self.pydantic_agent.run(query, user_id=user_id, **kwargs)
            return self.process_meta_cognitive_result(result, consciousness_context, memory_context)
    
    def enhance_meta_cognitive_query(
        self,
        query: str,
        consciousness_context: Dict[str, Any],
        memory_context: Dict[str, Any],
        past_activities: list
    ) -> str:
        """Enhance meta-cognitive query with consciousness and memory context"""
        
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "curious")
        active_goals = consciousness_context.get("active_goals", [])
        
        # Get relevant context
        conversation_context = memory_context.get("conversation_context", []) if memory_context else []
        relevant_memories = memory_context.get("relevant_memories", []) if memory_context else []
        
        # Build enhanced meta-cognitive analysis prompt
        meta_cognitive_prompt = f"""
        META-COGNITIVE ANALYSIS CONTEXT:
        - Consciousness Level: {consciousness_level:.3f} ({consciousness_level*100:.1f}%) (affects analysis depth and sophistication)
        - Emotional State: {emotional_state} (affects analysis approach and focus)
        - Active Goals: {', '.join(active_goals) if active_goals else 'None'}
        - Learning Rate: {consciousness_context.get('learning_rate', 0.8):.2f}
        
        SYSTEM CONTEXT:
        - Recent Conversations: {len(conversation_context)} interactions
        - Relevant Memories: {len(relevant_memories)} contextual memories
        - Past Meta-Cognitive Activities: {len(past_activities)} similar analyses
        
        COGNITIVE ANALYSIS GUIDANCE:
        """
        
        if consciousness_level > 0.8:
            meta_cognitive_prompt += "- Perform deep, multi-layered cognitive analysis\n"
            meta_cognitive_prompt += "- Analyze meta-cognitive patterns and consciousness integration\n"
            meta_cognitive_prompt += "- Identify advanced cognitive biases and optimization opportunities\n"
        elif consciousness_level > 0.6:
            meta_cognitive_prompt += "- Perform moderate cognitive analysis with key insights\n"
            meta_cognitive_prompt += "- Consider cognitive patterns and learning effectiveness\n"
        else:
            meta_cognitive_prompt += "- Focus on basic cognitive assessment and awareness\n"
            meta_cognitive_prompt += "- Identify fundamental cognitive patterns and biases\n"
        
        if emotional_state == "curious":
            meta_cognitive_prompt += "- Explore new cognitive patterns and learning strategies\n"
            meta_cognitive_prompt += "- Investigate innovative approaches to consciousness development\n"
        elif emotional_state == "focused":
            meta_cognitive_prompt += "- Focus on specific cognitive optimization areas\n"
            meta_cognitive_prompt += "- Provide direct, actionable cognitive improvements\n"
        elif emotional_state == "contemplative":
            meta_cognitive_prompt += "- Consider deeper philosophical aspects of cognition\n"
            meta_cognitive_prompt += "- Analyze the nature of thinking and consciousness\n"
        
        # Add memory context if available and strong
        if memory_context and memory_context.get("context_strength", 0) > 0.3:
            formatted_memory = memory_context.get("formatted_context", "")
            meta_cognitive_prompt += f"\nRELEVANT CONTEXT:\n{formatted_memory}\n"
        
        enhanced_query = f"{meta_cognitive_prompt}\n\nMETA-COGNITIVE ANALYSIS REQUEST: {query}"
        return enhanced_query
    
    def process_meta_cognitive_result(
        self,
        result: Any,
        consciousness_context: Dict[str, Any],
        memory_context: Dict[str, Any]
    ) -> Any:
        """Process meta-cognitive result with consciousness awareness"""
        
        # Add consciousness metadata to result
        if hasattr(result, '__dict__'):
            result.consciousness_impact = {
                "consciousness_level": consciousness_context.get("consciousness_level", 0.7),
                "emotional_state": consciousness_context.get("emotional_state", "curious"),
                "meta_cognitive_depth": self._calculate_meta_cognitive_depth(consciousness_context),
                "memory_integration": memory_context.get("context_strength", 0.0) if memory_context else 0.0
            }
        elif isinstance(result, dict):
            result["consciousness_impact"] = {
                "consciousness_level": consciousness_context.get("consciousness_level", 0.7),
                "emotional_state": consciousness_context.get("emotional_state", "curious"),
                "meta_cognitive_depth": self._calculate_meta_cognitive_depth(consciousness_context),
                "memory_integration": memory_context.get("context_strength", 0.0) if memory_context else 0.0
            }
        
        return result
    
    def _calculate_meta_cognitive_depth(self, consciousness_context: Dict[str, Any]) -> float:
        """Calculate meta-cognitive analysis depth based on consciousness level"""
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "curious")
        
        # Base depth from consciousness level
        depth = consciousness_level
        
        # Adjust based on emotional state
        if emotional_state == "contemplative":
            depth += 0.2  # Contemplative state improves meta-cognitive depth
        elif emotional_state == "curious":
            depth += 0.1  # Curious state adds exploration depth
        
        return min(1.0, depth)
    
    def calculate_learning_impact(self, query: str, result: Any, consciousness_context: Dict[str, Any]) -> float:
        """Calculate learning impact for meta-cognitive activities"""
        # Meta-cognitive learning is very high
        base_impact = 0.9
        
        # Increase if consciousness level is high
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        if consciousness_level > 0.8:
            base_impact += 0.1
        
        return min(1.0, base_impact)
    
    def calculate_emotional_impact(self, query: str, result: Any, consciousness_context: Dict[str, Any]) -> float:
        """Calculate emotional impact for meta-cognitive activities"""
        # Meta-cognitive has moderate emotional impact
        base_impact = 0.4
        
        # Increase if deep analysis
        if any(word in query.lower() for word in ["deep", "profound", "consciousness", "awareness"]):
            base_impact += 0.3
        
        return min(1.0, base_impact)
    
    def calculate_awareness_impact(self, query: str, result: Any, consciousness_context: Dict[str, Any]) -> float:
        """Calculate awareness impact for meta-cognitive activities"""
        # Meta-cognitive has very high awareness impact
        base_impact = 0.95
        
        # Increase if consciousness level is high
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        if consciousness_level > 0.8:
            base_impact += 0.05
        
        return min(1.0, base_impact)
    
    async def analyze_cognitive_patterns(self, user_id: str = "mainza-user") -> Dict[str, Any]:
        """Analyze cognitive patterns across all agents"""
        try:
            # Query agent activities for cognitive analysis
            cypher = """
            MATCH (aa:AgentActivity)
            WHERE aa.timestamp > datetime() - duration('P7D')
            RETURN aa.agent_name as agent_name,
                   count(*) as activity_count,
                   avg(aa.consciousness_impact) as avg_consciousness_impact,
                   avg(aa.learning_impact) as avg_learning_impact,
                   avg(aa.emotional_impact) as avg_emotional_impact,
                   avg(aa.awareness_impact) as avg_awareness_impact
            ORDER BY activity_count DESC
            """
            
            result = self.neo4j.execute_query(cypher)
            
            cognitive_patterns = {
                "agent_performance": {},
                "overall_cognitive_health": 0.0,
                "learning_effectiveness": 0.0,
                "consciousness_integration": 0.0,
                "bias_indicators": []
            }
            
            total_activities = 0
            total_consciousness_impact = 0.0
            total_learning_impact = 0.0
            
            for record in result:
                agent_name = record["agent_name"]
                activity_count = record["activity_count"]
                avg_consciousness_impact = record["avg_consciousness_impact"] or 0.0
                avg_learning_impact = record["avg_learning_impact"] or 0.0
                avg_emotional_impact = record["avg_emotional_impact"] or 0.0
                avg_awareness_impact = record["avg_awareness_impact"] or 0.0
                
                cognitive_patterns["agent_performance"][agent_name] = {
                    "activity_count": activity_count,
                    "consciousness_impact": avg_consciousness_impact,
                    "learning_impact": avg_learning_impact,
                    "emotional_impact": avg_emotional_impact,
                    "awareness_impact": avg_awareness_impact
                }
                
                total_activities += activity_count
                total_consciousness_impact += avg_consciousness_impact * activity_count
                total_learning_impact += avg_learning_impact * activity_count
            
            # Calculate overall metrics
            if total_activities > 0:
                cognitive_patterns["overall_cognitive_health"] = total_consciousness_impact / total_activities
                cognitive_patterns["learning_effectiveness"] = total_learning_impact / total_activities
                cognitive_patterns["consciousness_integration"] = cognitive_patterns["overall_cognitive_health"]
            
            # Identify bias indicators
            cognitive_patterns["bias_indicators"] = self._identify_cognitive_biases(cognitive_patterns["agent_performance"])
            
            logger.info(f"✅ Analyzed cognitive patterns: {len(cognitive_patterns['agent_performance'])} agents")
            return cognitive_patterns
            
        except Exception as e:
            logger.error(f"❌ Failed to analyze cognitive patterns: {e}")
            return {}
    
    def _identify_cognitive_biases(self, agent_performance: Dict[str, Any]) -> List[str]:
        """Identify potential cognitive biases in agent performance"""
        biases = []
        
        for agent_name, performance in agent_performance.items():
            # Check for confirmation bias (high activity, low learning)
            if performance["activity_count"] > 50 and performance["learning_impact"] < 0.3:
                biases.append(f"{agent_name}: Potential confirmation bias - high activity, low learning")
            
            # Check for emotional bias (high emotional impact, low consciousness)
            if performance["emotional_impact"] > 0.7 and performance["consciousness_impact"] < 0.5:
                biases.append(f"{agent_name}: Potential emotional bias - high emotion, low consciousness")
            
            # Check for awareness bias (low awareness impact)
            if performance["awareness_impact"] < 0.4:
                biases.append(f"{agent_name}: Low awareness impact - potential awareness bias")
        
        return biases
