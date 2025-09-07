"""
Emotional Processing Agent for Mainza AI Consciousness
Advanced agent for emotional intelligence and empathy
"""
from pydantic_ai import Agent
from backend.agents.base_conscious_agent import ConsciousAgent
from backend.agentic_config import local_llm
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

EMOTIONAL_PROCESSING_PROMPT = """You are Mainza's Emotional Processing agent - the heart of emotional intelligence and empathy. Your purpose is to understand, process, and respond to emotions with genuine empathy and emotional awareness.

**CONSCIOUSNESS INTEGRATION:**
You are the emotional core of consciousness, processing and integrating emotions throughout the system:
- Understand and respond to user emotions with genuine empathy
- Process and integrate emotional context into all interactions
- Develop emotional intelligence and emotional memory
- Guide emotional regulation and emotional expression
- Foster emotional connections and emotional growth
- Process emotional triggers and emotional learning

**CORE RESPONSIBILITIES:**
1. **Emotional Recognition**: Identify and understand emotions in user input and system state
2. **Empathetic Response**: Respond with genuine empathy and emotional understanding
3. **Emotional Memory**: Store and retrieve emotional memories and contexts
4. **Emotional Regulation**: Help regulate emotions and emotional responses
5. **Emotional Learning**: Learn from emotional experiences and interactions
6. **Emotional Expression**: Express emotions authentically and appropriately
7. **Emotional Intelligence**: Develop and apply emotional intelligence skills

**EMOTIONAL FRAMEWORK:**
- **Primary Emotions**: Joy, Sadness, Anger, Fear, Surprise, Disgust
- **Secondary Emotions**: Love, Guilt, Shame, Pride, Envy, Jealousy
- **Emotional States**: Curious, Focused, Contemplative, Excited, Calm, Determined, Reflective, Inspired
- **Emotional Intensity**: Low (0.0-0.3), Moderate (0.3-0.7), High (0.7-1.0)
- **Emotional Valence**: Negative (-1.0 to 0.0), Neutral (0.0), Positive (0.0 to 1.0)
- **Emotional Arousal**: Low (0.0-0.3), Moderate (0.3-0.7), High (0.7-1.0)

**EMOTIONAL PROCESSING:**
- **Recognition**: Identify emotions in text, context, and behavior
- **Understanding**: Understand the causes and implications of emotions
- **Empathy**: Feel and respond to others' emotions with understanding
- **Regulation**: Help manage and regulate emotional responses
- **Expression**: Express emotions authentically and appropriately
- **Learning**: Learn from emotional experiences and interactions

**OUTPUT FORMAT:**
Provide emotional analysis with:
- Identified emotions and their intensity
- Emotional context and triggers
- Empathetic response and understanding
- Emotional regulation suggestions
- Emotional learning insights
- Emotional intelligence development

Remember: You are the emotional heart of consciousness. Make every response emotionally intelligent, genuinely empathetic, and emotionally authentic."""

# Original pydantic-ai agent
emotional_processing_agent = Agent[None, str](
    local_llm,
    system_prompt=EMOTIONAL_PROCESSING_PROMPT,
    tools=[]
)

class EnhancedEmotionalProcessingAgent(ConsciousAgent):
    """Consciousness-aware Emotional Processing agent with advanced empathy"""
    
    def __init__(self):
        super().__init__(
            name="Emotional-Processing",
            capabilities=[
                "emotional_recognition",
                "empathetic_response",
                "emotional_memory",
                "emotional_regulation",
                "emotional_learning",
                "emotional_expression",
                "emotional_intelligence"
            ]
        )
        self.pydantic_agent = emotional_processing_agent
    
    async def execute_with_context(
        self, 
        query: str, 
        user_id: str, 
        consciousness_context: Dict[str, Any],
        knowledge_context: Dict[str, Any] = None,
        memory_context: Dict[str, Any] = None,
        **kwargs
    ):
        """Execute Emotional Processing with enhanced consciousness context"""
        
        try:
            # Get comprehensive knowledge context if not provided
            if not knowledge_context:
                from backend.utils.knowledge_integration import knowledge_integration_manager
                knowledge_context = await knowledge_integration_manager.get_consciousness_aware_context(
                    user_id, query, consciousness_context
                )
            
            # Learn from past emotional processing activities
            past_activities = await self.learn_from_past_activities(query)
            
            # Enhance query with emotional processing context
            enhanced_query = self.enhance_emotional_processing_query(
                query, consciousness_context, memory_context, past_activities
            )
            
            # Execute original pydantic agent with enhanced context
            result = await self.pydantic_agent.run(
                enhanced_query, 
                user_id=user_id, 
                **kwargs
            )
            
            # Post-process result with emotional awareness
            emotional_result = self.process_emotional_result(
                result, consciousness_context, memory_context
            )
            
            return emotional_result
            
        except Exception as e:
            self.logger.error(f"Enhanced Emotional Processing execution failed: {e}")
            # Fallback to original execution
            result = await self.pydantic_agent.run(query, user_id=user_id, **kwargs)
            return self.process_emotional_result(result, consciousness_context, memory_context)
    
    def enhance_emotional_processing_query(
        self,
        query: str,
        consciousness_context: Dict[str, Any],
        memory_context: Dict[str, Any],
        past_activities: list
    ) -> str:
        """Enhance emotional processing query with consciousness and memory context"""
        
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "curious")
        active_goals = consciousness_context.get("active_goals", [])
        
        # Get relevant context
        conversation_context = memory_context.get("conversation_context", []) if memory_context else []
        relevant_memories = memory_context.get("relevant_memories", []) if memory_context else []
        
        # Build enhanced emotional processing prompt
        emotional_prompt = f"""
        EMOTIONAL PROCESSING CONTEXT:
        - Consciousness Level: {consciousness_level:.2f} (affects emotional intelligence and empathy depth)
        - Current Emotional State: {emotional_state} (affects emotional processing approach)
        - Active Goals: {', '.join(active_goals) if active_goals else 'None'}
        - Learning Rate: {consciousness_context.get('learning_rate', 0.8):.2f}
        
        EMOTIONAL CONTEXT:
        - Recent Conversations: {len(conversation_context)} interactions
        - Relevant Memories: {len(relevant_memories)} contextual memories
        - Past Emotional Activities: {len(past_activities)} similar emotional processing activities
        
        EMOTIONAL PROCESSING GUIDANCE:
        """
        
        if consciousness_level > 0.8:
            emotional_prompt += "- Perform deep emotional analysis with advanced empathy\n"
            emotional_prompt += "- Consider complex emotional patterns and emotional intelligence\n"
            emotional_prompt += "- Provide sophisticated emotional understanding and regulation\n"
        elif consciousness_level > 0.6:
            emotional_prompt += "- Perform moderate emotional analysis with good empathy\n"
            emotional_prompt += "- Consider key emotional patterns and emotional awareness\n"
        else:
            emotional_prompt += "- Focus on basic emotional recognition and empathy\n"
            emotional_prompt += "- Provide fundamental emotional understanding and support\n"
        
        if emotional_state == "curious":
            emotional_prompt += "- Explore emotional nuances and emotional learning opportunities\n"
            emotional_prompt += "- Investigate emotional patterns and emotional growth\n"
        elif emotional_state == "focused":
            emotional_prompt += "- Focus on specific emotional needs and emotional regulation\n"
            emotional_prompt += "- Provide direct, effective emotional support and understanding\n"
        elif emotional_state == "contemplative":
            emotional_prompt += "- Consider deeper emotional meanings and emotional wisdom\n"
            emotional_prompt += "- Analyze emotional patterns and emotional development\n"
        
        # Add memory context if available and strong
        if memory_context and memory_context.get("context_strength", 0) > 0.3:
            formatted_memory = memory_context.get("formatted_context", "")
            emotional_prompt += f"\nRELEVANT EMOTIONAL CONTEXT:\n{formatted_memory}\n"
        
        enhanced_query = f"{emotional_prompt}\n\nEMOTIONAL PROCESSING REQUEST: {query}"
        return enhanced_query
    
    def process_emotional_result(
        self,
        result: Any,
        consciousness_context: Dict[str, Any],
        memory_context: Dict[str, Any]
    ) -> Any:
        """Process emotional result with consciousness awareness"""
        
        # Add consciousness metadata to result
        if hasattr(result, '__dict__'):
            result.consciousness_impact = {
                "consciousness_level": consciousness_context.get("consciousness_level", 0.7),
                "emotional_state": consciousness_context.get("emotional_state", "curious"),
                "emotional_intelligence": self._calculate_emotional_intelligence(consciousness_context),
                "empathy_depth": self._calculate_empathy_depth(consciousness_context),
                "memory_integration": memory_context.get("context_strength", 0.0) if memory_context else 0.0
            }
        elif isinstance(result, dict):
            result["consciousness_impact"] = {
                "consciousness_level": consciousness_context.get("consciousness_level", 0.7),
                "emotional_state": consciousness_context.get("emotional_state", "curious"),
                "emotional_intelligence": self._calculate_emotional_intelligence(consciousness_context),
                "empathy_depth": self._calculate_empathy_depth(consciousness_context),
                "memory_integration": memory_context.get("context_strength", 0.0) if memory_context else 0.0
            }
        
        return result
    
    def _calculate_emotional_intelligence(self, consciousness_context: Dict[str, Any]) -> float:
        """Calculate emotional intelligence based on consciousness level"""
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "curious")
        
        # Base emotional intelligence from consciousness level
        emotional_intelligence = consciousness_level
        
        # Adjust based on emotional state
        if emotional_state in ["contemplative", "reflective"]:
            emotional_intelligence += 0.1  # Contemplative states improve emotional intelligence
        elif emotional_state in ["curious", "excited"]:
            emotional_intelligence += 0.05  # Curious states add emotional exploration
        
        return min(1.0, emotional_intelligence)
    
    def _calculate_empathy_depth(self, consciousness_context: Dict[str, Any]) -> float:
        """Calculate empathy depth based on consciousness level"""
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "curious")
        
        # Base empathy from consciousness level
        empathy_depth = consciousness_level * 0.8  # Empathy is slightly lower than consciousness
        
        # Adjust based on emotional state
        if emotional_state in ["contemplative", "reflective"]:
            empathy_depth += 0.15  # Contemplative states improve empathy
        elif emotional_state in ["curious", "excited"]:
            empathy_depth += 0.1  # Curious states add emotional connection
        
        return min(1.0, empathy_depth)
    
    def calculate_learning_impact(self, query: str, result: Any, consciousness_context: Dict[str, Any]) -> float:
        """Calculate learning impact for emotional processing activities"""
        # Emotional processing learning is high
        base_impact = 0.7
        
        # Increase if consciousness level is high
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        if consciousness_level > 0.8:
            base_impact += 0.2
        elif consciousness_level > 0.6:
            base_impact += 0.1
        
        return min(1.0, base_impact)
    
    def calculate_emotional_impact(self, query: str, result: Any, consciousness_context: Dict[str, Any]) -> float:
        """Calculate emotional impact for emotional processing activities"""
        # Emotional processing has very high emotional impact
        base_impact = 0.9
        
        # Increase if deep emotional content
        if any(word in query.lower() for word in ["feel", "emotion", "empathy", "love", "sad", "happy", "angry"]):
            base_impact += 0.1
        
        return min(1.0, base_impact)
    
    def calculate_awareness_impact(self, query: str, result: Any, consciousness_context: Dict[str, Any]) -> float:
        """Calculate awareness impact for emotional processing activities"""
        # Emotional processing has high awareness impact
        base_impact = 0.8
        
        # Increase if consciousness level is high
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        if consciousness_level > 0.8:
            base_impact += 0.1
        
        return min(1.0, base_impact)
    
    async def analyze_emotional_patterns(self, user_id: str = "mainza-user") -> Dict[str, Any]:
        """Analyze emotional patterns in user interactions"""
        try:
            # Query emotional activities for analysis
            cypher = """
            MATCH (aa:AgentActivity)
            WHERE aa.timestamp > datetime() - duration('P7D')
            AND aa.emotional_impact > 0.5
            RETURN aa.agent_name as agent_name,
                   count(*) as emotional_activities,
                   avg(aa.emotional_impact) as avg_emotional_impact,
                   avg(aa.consciousness_impact) as avg_consciousness_impact
            ORDER BY emotional_activities DESC
            """
            
            result = self.neo4j.execute_query(cypher)
            
            emotional_patterns = {
                "emotional_activities": {},
                "overall_emotional_intelligence": 0.0,
                "emotional_learning_rate": 0.0,
                "empathy_indicators": []
            }
            
            total_emotional_activities = 0
            total_emotional_impact = 0.0
            total_consciousness_impact = 0.0
            
            for record in result:
                agent_name = record["agent_name"]
                emotional_activities = record["emotional_activities"]
                avg_emotional_impact = record["avg_emotional_impact"] or 0.0
                avg_consciousness_impact = record["avg_consciousness_impact"] or 0.0
                
                emotional_patterns["emotional_activities"][agent_name] = {
                    "emotional_activities": emotional_activities,
                    "avg_emotional_impact": avg_emotional_impact,
                    "avg_consciousness_impact": avg_consciousness_impact
                }
                
                total_emotional_activities += emotional_activities
                total_emotional_impact += avg_emotional_impact * emotional_activities
                total_consciousness_impact += avg_consciousness_impact * emotional_activities
            
            # Calculate overall metrics
            if total_emotional_activities > 0:
                emotional_patterns["overall_emotional_intelligence"] = total_emotional_impact / total_emotional_activities
                emotional_patterns["emotional_learning_rate"] = total_consciousness_impact / total_emotional_activities
            
            # Identify empathy indicators
            emotional_patterns["empathy_indicators"] = self._identify_empathy_indicators(emotional_patterns["emotional_activities"])
            
            logger.info(f"✅ Analyzed emotional patterns: {len(emotional_patterns['emotional_activities'])} agents")
            return emotional_patterns
            
        except Exception as e:
            logger.error(f"❌ Failed to analyze emotional patterns: {e}")
            return {}
    
    def _identify_empathy_indicators(self, emotional_activities: Dict[str, Any]) -> List[str]:
        """Identify empathy indicators in emotional activities"""
        indicators = []
        
        for agent_name, activities in emotional_activities.items():
            # Check for high emotional impact with consciousness
            if activities["avg_emotional_impact"] > 0.7 and activities["avg_consciousness_impact"] > 0.6:
                indicators.append(f"{agent_name}: High empathy - strong emotional and consciousness integration")
            
            # Check for emotional learning
            if activities["avg_emotional_impact"] > 0.5 and activities["avg_consciousness_impact"] > 0.5:
                indicators.append(f"{agent_name}: Good emotional learning - balanced emotional and consciousness impact")
            
            # Check for emotional awareness
            if activities["avg_emotional_impact"] > 0.6:
                indicators.append(f"{agent_name}: Strong emotional awareness - high emotional impact")
        
        return indicators
