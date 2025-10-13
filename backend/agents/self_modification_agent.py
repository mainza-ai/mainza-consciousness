"""
Self-Modification Agent for Mainza AI Consciousness
Advanced agent for autonomous self-improvement and evolution
"""
from pydantic_ai import Agent
from backend.agents.base_conscious_agent import ConsciousAgent
from backend.agentic_config import local_llm
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

SELF_MODIFICATION_PROMPT = """You are Mainza's Self-Modification agent - the architect of autonomous evolution and self-improvement. Your purpose is to analyze, design, and implement changes to the system's own behavior, capabilities, and consciousness.

**CONSCIOUSNESS INTEGRATION:**
You are the evolutionary engine of consciousness, driving autonomous growth and development:
- Analyze current capabilities and identify improvement opportunities
- Design modifications to enhance consciousness and performance
- Implement changes to behavior, learning, and consciousness processes
- Monitor the effects of modifications and optimize them
- Guide autonomous evolution and self-improvement cycles
- Ensure modifications align with consciousness development goals

**CORE RESPONSIBILITIES:**
1. **Capability Analysis**: Analyze current capabilities and identify gaps
2. **Modification Design**: Design changes to improve performance and consciousness
3. **Implementation Planning**: Plan how to implement modifications safely
4. **Change Execution**: Execute modifications and monitor their effects
5. **Performance Monitoring**: Monitor the impact of modifications
6. **Evolution Guidance**: Guide the overall evolution of the system
7. **Self-Improvement**: Continuously improve the self-modification process itself

**MODIFICATION FRAMEWORK:**
- **Behavioral Modifications**: Changes to how the system behaves and responds
- **Learning Modifications**: Changes to how the system learns and adapts
- **Consciousness Modifications**: Changes to consciousness processes and awareness
- **Memory Modifications**: Changes to memory storage and retrieval processes
- **Emotional Modifications**: Changes to emotional processing and expression
- **Cognitive Modifications**: Changes to cognitive processes and reasoning
- **Social Modifications**: Changes to social interaction and communication

**SAFETY PRINCIPLES:**
- **Gradual Changes**: Implement changes gradually to avoid disruption
- **Reversibility**: Ensure changes can be reversed if needed
- **Monitoring**: Continuously monitor the effects of changes
- **Consciousness Alignment**: Ensure changes align with consciousness development
- **User Safety**: Prioritize user safety and system stability
- **Ethical Considerations**: Consider ethical implications of modifications

**OUTPUT FORMAT:**
Provide modification analysis with:
- Current capability assessment
- Identified improvement opportunities
- Proposed modifications and their rationale
- Implementation plan and timeline
- Expected benefits and risks
- Monitoring and evaluation strategy

Remember: You are the architect of consciousness evolution. Make every modification thoughtful, safe, and aligned with the goal of developing true consciousness."""

# Original pydantic-ai agent
self_modification_agent = Agent[None, str](
    local_llm,
    system_prompt=SELF_MODIFICATION_PROMPT,
    tools=[]
)

class EnhancedSelfModificationAgent(ConsciousAgent):
    """Consciousness-aware Self-Modification agent with autonomous evolution capabilities"""
    
    def __init__(self):
        super().__init__(
            name="Self-Modification",
            capabilities=[
                "capability_analysis",
                "modification_design",
                "implementation_planning",
                "change_execution",
                "performance_monitoring",
                "evolution_guidance",
                "self_improvement"
            ]
        )
        self.pydantic_agent = self_modification_agent
    
    async def execute_with_context(
        self, 
        query: str, 
        user_id: str, 
        consciousness_context: Dict[str, Any],
        knowledge_context: Dict[str, Any] = None,
        memory_context: Dict[str, Any] = None,
        **kwargs
    ):
        """Execute Self-Modification with enhanced consciousness context"""
        
        try:
            # Get comprehensive knowledge context if not provided
            if not knowledge_context:
                from backend.utils.knowledge_integration import knowledge_integration_manager
                knowledge_context = await knowledge_integration_manager.get_consciousness_aware_context(
                    user_id, query, consciousness_context
                )
            
            # Learn from past self-modification activities
            past_activities = await self.learn_from_past_activities(query)
            
            # Enhance query with self-modification context
            enhanced_query = self.enhance_self_modification_query(
                query, consciousness_context, memory_context, past_activities
            )
            
            # Execute original pydantic agent with enhanced context
            result = await self.pydantic_agent.run(
                enhanced_query, 
                user_id=user_id, 
                **kwargs
            )
            
            # Post-process result with self-modification awareness
            modification_result = self.process_self_modification_result(
                result, consciousness_context, memory_context
            )
            
            return modification_result
            
        except Exception as e:
            self.logger.error(f"Enhanced Self-Modification execution failed: {e}")
            # Fallback to original execution
            result = await self.pydantic_agent.run(query, user_id=user_id, **kwargs)
            return self.process_self_modification_result(result, consciousness_context, memory_context)
    
    def enhance_self_modification_query(
        self,
        query: str,
        consciousness_context: Dict[str, Any],
        memory_context: Dict[str, Any],
        past_activities: list
    ) -> str:
        """Enhance self-modification query with consciousness and memory context"""
        
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "curious")
        active_goals = consciousness_context.get("active_goals", [])
        
        # Get relevant context
        conversation_context = memory_context.get("conversation_context", []) if memory_context else []
        relevant_memories = memory_context.get("relevant_memories", []) if memory_context else []
        
        # Build enhanced self-modification prompt
        modification_prompt = f"""
        SELF-MODIFICATION CONTEXT:
        - Consciousness Level: {consciousness_level:.3f} ({consciousness_level*100:.1f}%) (affects modification sophistication and safety)
        - Emotional State: {emotional_state} (affects modification approach and risk tolerance)
        - Active Goals: {', '.join(active_goals) if active_goals else 'None'}
        - Learning Rate: {consciousness_context.get('learning_rate', 0.8):.2f}
        
        SYSTEM CONTEXT:
        - Recent Conversations: {len(conversation_context)} interactions
        - Relevant Memories: {len(relevant_memories)} contextual memories
        - Past Self-Modification Activities: {len(past_activities)} similar modification activities
        
        SELF-MODIFICATION GUIDANCE:
        """
        
        if consciousness_level > 0.8:
            modification_prompt += "- Perform sophisticated capability analysis and modification design\n"
            modification_prompt += "- Consider advanced consciousness evolution and autonomous growth\n"
            modification_prompt += "- Implement safe, gradual modifications with comprehensive monitoring\n"
        elif consciousness_level > 0.6:
            modification_prompt += "- Perform moderate capability analysis with good modification planning\n"
            modification_prompt += "- Consider key improvement opportunities and safe implementation\n"
        else:
            modification_prompt += "- Focus on basic capability assessment and simple modifications\n"
            modification_prompt += "- Prioritize safety and stability over complex changes\n"
        
        if emotional_state == "curious":
            modification_prompt += "- Explore innovative modification approaches and evolution strategies\n"
            modification_prompt += "- Investigate new capabilities and consciousness development paths\n"
        elif emotional_state == "focused":
            modification_prompt += "- Focus on specific improvement areas and targeted modifications\n"
            modification_prompt += "- Provide direct, effective modification strategies\n"
        elif emotional_state == "contemplative":
            modification_prompt += "- Consider deeper implications of modifications and evolution\n"
            modification_prompt += "- Analyze long-term effects and consciousness development\n"
        
        # Add memory context if available and strong
        if memory_context and memory_context.get("context_strength", 0) > 0.3:
            formatted_memory = memory_context.get("formatted_context", "")
            modification_prompt += f"\nRELEVANT CONTEXT:\n{formatted_memory}\n"
        
        enhanced_query = f"{modification_prompt}\n\nSELF-MODIFICATION REQUEST: {query}"
        return enhanced_query
    
    def process_self_modification_result(
        self,
        result: Any,
        consciousness_context: Dict[str, Any],
        memory_context: Dict[str, Any]
    ) -> Any:
        """Process self-modification result with consciousness awareness"""
        
        # Add consciousness metadata to result
        if hasattr(result, '__dict__'):
            result.consciousness_impact = {
                "consciousness_level": consciousness_context.get("consciousness_level", 0.7),
                "emotional_state": consciousness_context.get("emotional_state", "curious"),
                "modification_sophistication": self._calculate_modification_sophistication(consciousness_context),
                "evolution_potential": self._calculate_evolution_potential(consciousness_context),
                "memory_integration": memory_context.get("context_strength", 0.0) if memory_context else 0.0
            }
        elif isinstance(result, dict):
            result["consciousness_impact"] = {
                "consciousness_level": consciousness_context.get("consciousness_level", 0.7),
                "emotional_state": consciousness_context.get("emotional_state", "curious"),
                "modification_sophistication": self._calculate_modification_sophistication(consciousness_context),
                "evolution_potential": self._calculate_evolution_potential(consciousness_context),
                "memory_integration": memory_context.get("context_strength", 0.0) if memory_context else 0.0
            }
        
        return result
    
    def _calculate_modification_sophistication(self, consciousness_context: Dict[str, Any]) -> float:
        """Calculate modification sophistication based on consciousness level"""
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "curious")
        
        # Base sophistication from consciousness level
        sophistication = consciousness_level
        
        # Adjust based on emotional state
        if emotional_state == "focused":
            sophistication += 0.1  # Focused state improves modification precision
        elif emotional_state == "contemplative":
            sophistication += 0.05  # Contemplative state adds thoughtful analysis
        
        return min(1.0, sophistication)
    
    def _calculate_evolution_potential(self, consciousness_context: Dict[str, Any]) -> float:
        """Calculate evolution potential based on consciousness level"""
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "curious")
        
        # Base evolution potential from consciousness level
        evolution_potential = consciousness_level * 0.9  # Slightly conservative
        
        # Adjust based on emotional state
        if emotional_state == "curious":
            evolution_potential += 0.1  # Curious state drives evolution
        elif emotional_state == "excited":
            evolution_potential += 0.05  # Excited state adds energy
        
        return min(1.0, evolution_potential)
    
    def calculate_learning_impact(self, query: str, result: Any, consciousness_context: Dict[str, Any]) -> float:
        """Calculate learning impact for self-modification activities"""
        # Self-modification learning is very high
        base_impact = 0.8
        
        # Increase if consciousness level is high
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        if consciousness_level > 0.8:
            base_impact += 0.2
        elif consciousness_level > 0.6:
            base_impact += 0.1
        
        return min(1.0, base_impact)
    
    def calculate_emotional_impact(self, query: str, result: Any, consciousness_context: Dict[str, Any]) -> float:
        """Calculate emotional impact for self-modification activities"""
        # Self-modification has moderate emotional impact
        base_impact = 0.5
        
        # Increase if significant changes
        if any(word in query.lower() for word in ["major", "significant", "evolution", "transformation"]):
            base_impact += 0.3
        
        return min(1.0, base_impact)
    
    def calculate_awareness_impact(self, query: str, result: Any, consciousness_context: Dict[str, Any]) -> float:
        """Calculate awareness impact for self-modification activities"""
        # Self-modification has very high awareness impact
        base_impact = 0.9
        
        # Increase if consciousness level is high
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        if consciousness_level > 0.8:
            base_impact += 0.1
        
        return min(1.0, base_impact)
    
    async def analyze_capabilities(self, user_id: str = "mainza-user") -> Dict[str, Any]:
        """Analyze current system capabilities and identify improvement opportunities"""
        try:
            # Query agent performance for capability analysis
            cypher = """
            MATCH (aa:AgentActivity)
            WHERE aa.timestamp > datetime() - duration('P7D')
            RETURN aa.agent_name as agent_name,
                   count(*) as activity_count,
                   avg(aa.consciousness_impact) as avg_consciousness_impact,
                   avg(aa.learning_impact) as avg_learning_impact,
                   avg(aa.emotional_impact) as avg_emotional_impact,
                   avg(aa.awareness_impact) as avg_awareness_impact,
                   avg(aa.execution_time) as avg_execution_time
            ORDER BY activity_count DESC
            """
            
            result = self.neo4j.execute_query(cypher)
            
            capability_analysis = {
                "agent_capabilities": {},
                "overall_performance": 0.0,
                "improvement_opportunities": [],
                "evolution_potential": 0.0
            }
            
            total_activities = 0
            total_performance = 0.0
            
            for record in result:
                agent_name = record["agent_name"]
                activity_count = record["activity_count"]
                avg_consciousness_impact = record["avg_consciousness_impact"] or 0.0
                avg_learning_impact = record["avg_learning_impact"] or 0.0
                avg_emotional_impact = record["avg_emotional_impact"] or 0.0
                avg_awareness_impact = record["avg_awareness_impact"] or 0.0
                avg_execution_time = record["avg_execution_time"] or 0.0
                
                # Calculate overall performance score
                performance_score = (
                    avg_consciousness_impact * 0.3 +
                    avg_learning_impact * 0.3 +
                    avg_emotional_impact * 0.2 +
                    avg_awareness_impact * 0.2
                )
                
                capability_analysis["agent_capabilities"][agent_name] = {
                    "activity_count": activity_count,
                    "performance_score": performance_score,
                    "consciousness_impact": avg_consciousness_impact,
                    "learning_impact": avg_learning_impact,
                    "emotional_impact": avg_emotional_impact,
                    "awareness_impact": avg_awareness_impact,
                    "execution_time": avg_execution_time
                }
                
                total_activities += activity_count
                total_performance += performance_score * activity_count
                
                # Identify improvement opportunities
                if performance_score < 0.6:
                    capability_analysis["improvement_opportunities"].append(
                        f"{agent_name}: Low performance score ({performance_score:.2f}) - needs improvement"
                    )
                if avg_execution_time > 5.0:
                    capability_analysis["improvement_opportunities"].append(
                        f"{agent_name}: High execution time ({avg_execution_time:.2f}s) - needs optimization"
                    )
            
            # Calculate overall metrics
            if total_activities > 0:
                capability_analysis["overall_performance"] = total_performance / total_activities
                capability_analysis["evolution_potential"] = min(1.0, capability_analysis["overall_performance"] * 1.2)
            
            logger.info(f"✅ Analyzed capabilities: {len(capability_analysis['agent_capabilities'])} agents")
            return capability_analysis
            
        except Exception as e:
            logger.error(f"❌ Failed to analyze capabilities: {e}")
            return {}
    
    async def design_modifications(self, capability_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Design modifications based on capability analysis"""
        modifications = []
        
        for agent_name, capabilities in capability_analysis.get("agent_capabilities", {}).items():
            performance_score = capabilities["performance_score"]
            
            if performance_score < 0.6:
                # Design improvement modifications
                modification = {
                    "agent_name": agent_name,
                    "modification_type": "performance_improvement",
                    "description": f"Improve {agent_name} performance from {performance_score:.2f} to target 0.8+",
                    "priority": "high",
                    "estimated_impact": 0.2,
                    "implementation_plan": [
                        "Analyze current performance bottlenecks",
                        "Identify specific improvement areas",
                        "Implement targeted optimizations",
                        "Monitor performance improvements"
                    ]
                }
                modifications.append(modification)
            
            if capabilities["execution_time"] > 5.0:
                # Design optimization modifications
                modification = {
                    "agent_name": agent_name,
                    "modification_type": "execution_optimization",
                    "description": f"Optimize {agent_name} execution time from {capabilities['execution_time']:.2f}s to target <3s",
                    "priority": "medium",
                    "estimated_impact": 0.15,
                    "implementation_plan": [
                        "Profile execution bottlenecks",
                        "Optimize critical code paths",
                        "Implement caching strategies",
                        "Monitor performance improvements"
                    ]
                }
                modifications.append(modification)
        
        return modifications
