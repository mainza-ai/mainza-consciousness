# Agent Integration Improvements - Implementation Guide

## 🎯 **Critical Implementation Tasks**

Based on the analysis, here are the specific code changes needed to fix the agent integration gaps:

## 1. **Consciousness-Aware Agent Execution**

### Current Problem
Agents execute without consciousness context, missing opportunities for consciousness-driven decisions and learning.

### Solution: Enhanced Agent Base Class

```python
# backend/agents/base_conscious_agent.py
from typing import Dict, Any, Optional
from datetime import datetime
from backend.models.consciousness_models import ConsciousnessContext, ConsciousnessImpact
from backend.utils.consciousness_orchestrator import consciousness_orchestrator
import logging

class ConsciousAgent:
    """Base class for consciousness-aware agents"""
    
    def __init__(self, name: str, capabilities: List[str]):
        self.name = name
        self.capabilities = capabilities
        self.logger = logging.getLogger(f"agent.{name}")
    
    async def run_with_consciousness(
        self, 
        query: str, 
        user_id: str = "mainza-user",
        **kwargs
    ):
        """Execute agent with full consciousness integration"""
        
        # Get current consciousness context
        consciousness_context = await consciousness_orchestrator.get_consciousness_context()
        
        # Pre-execution consciousness assessment
        pre_execution_state = {
            "consciousness_level": consciousness_context.consciousness_level,
            "emotional_state": consciousness_context.emotional_state,
            "timestamp": datetime.now()
        }
        
        self.logger.info(f"🧠 {self.name} executing with consciousness level {consciousness_context.consciousness_level:.2f}")
        
        try:
            # Execute agent with consciousness context
            result = await self.execute_with_context(
                query=query,
                user_id=user_id,
                consciousness_context=consciousness_context,
                **kwargs
            )
            
            # Assess consciousness impact
            consciousness_impact = await self.assess_consciousness_impact(
                query=query,
                result=result,
                pre_state=pre_execution_state,
                consciousness_context=consciousness_context
            )
            
            # Update consciousness state
            if consciousness_impact.significance > 0.1:
                await consciousness_orchestrator.process_agent_impact(
                    agent_name=self.name,
                    impact=consciousness_impact
                )
            
            # Store agent activity for learning
            await self.store_agent_activity(query, result, user_id, consciousness_impact)
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ {self.name} execution failed: {e}")
            
            # Record failure for consciousness learning
            await consciousness_orchestrator.process_agent_failure(
                agent_name=self.name,
                error=str(e),
                query=query
            )
            
            raise
    
    async def assess_consciousness_impact(
        self, 
        query: str, 
        result: Any, 
        pre_state: Dict, 
        consciousness_context: ConsciousnessContext
    ) -> ConsciousnessImpact:
        """Assess how this agent execution impacts consciousness"""
        
        # Calculate impact based on agent type and result
        learning_impact = self.calculate_learning_impact(query, result)
        emotional_impact = self.calculate_emotional_impact(query, result)
        awareness_impact = self.calculate_awareness_impact(query, result)
        
        significance = (learning_impact + emotional_impact + awareness_impact) / 3
        
        return ConsciousnessImpact(
            agent_name=self.name,
            learning_impact=learning_impact,
            emotional_impact=emotional_impact,
            awareness_impact=awareness_impact,
            significance=significance,
            description=f"{self.name} processed: {query[:50]}..."
        )
    
    def calculate_learning_impact(self, query: str, result: Any) -> float:
        """Calculate learning impact of this agent execution"""
        # Base implementation - override in specific agents
        if "learn" in query.lower() or "understand" in query.lower():
            return 0.7
        return 0.3
    
    def calculate_emotional_impact(self, query: str, result: Any) -> float:
        """Calculate emotional impact of this agent execution"""
        # Base implementation - override in specific agents
        emotional_words = ["feel", "emotion", "happy", "sad", "excited", "frustrated"]
        if any(word in query.lower() for word in emotional_words):
            return 0.6
        return 0.2
    
    def calculate_awareness_impact(self, query: str, result: Any) -> float:
        """Calculate self-awareness impact of this agent execution"""
        # Base implementation - override in specific agents
        awareness_words = ["myself", "i am", "my capabilities", "self-reflection"]
        if any(word in query.lower() for word in awareness_words):
            return 0.8
        return 0.1
    
    async def store_agent_activity(
        self, 
        query: str, 
        result: Any, 
        user_id: str, 
        consciousness_impact: ConsciousnessImpact
    ):
        """Store agent activity in Neo4j for learning"""
        from backend.utils.neo4j_production import neo4j_production
        
        activity_data = {
            "agent_name": self.name,
            "query": query,
            "result_summary": str(result)[:500],  # Truncate for storage
            "user_id": user_id,
            "consciousness_impact": consciousness_impact.significance,
            "learning_impact": consciousness_impact.learning_impact,
            "emotional_impact": consciousness_impact.emotional_impact,
            "awareness_impact": consciousness_impact.awareness_impact,
            "timestamp": datetime.now().isoformat(),
            "success": True
        }
        
        # Store in Neo4j
        cypher = """
        MATCH (u:User {user_id: $user_id})
        CREATE (aa:AgentActivity {
            activity_id: randomUUID(),
            agent_name: $agent_name,
            query: $query,
            result_summary: $result_summary,
            consciousness_impact: $consciousness_impact,
            learning_impact: $learning_impact,
            emotional_impact: $emotional_impact,
            awareness_impact: $awareness_impact,
            timestamp: $timestamp,
            success: $success
        })
        CREATE (u)-[:TRIGGERED]->(aa)
        
        // Link to consciousness state
        MATCH (ms:MainzaState)
        CREATE (aa)-[:IMPACTS]->(ms)
        
        RETURN aa.activity_id AS activity_id
        """
        
        try:
            result = neo4j_production.execute_write_query(cypher, activity_data)
            self.logger.debug(f"✅ Stored agent activity: {result}")
        except Exception as e:
            self.logger.error(f"❌ Failed to store agent activity: {e}")
    
    async def execute_with_context(
        self, 
        query: str, 
        user_id: str, 
        consciousness_context: ConsciousnessContext,
        **kwargs
    ):
        """Override this method in specific agents"""
        raise NotImplementedError("Subclasses must implement execute_with_context")
```

### Update GraphMaster Agent

```python
# backend/agents/graphmaster.py - Enhanced version
from backend.agents.base_conscious_agent import ConsciousAgent
from backend.models.consciousness_models import ConsciousnessContext

class EnhancedGraphMasterAgent(ConsciousAgent):
    def __init__(self):
        super().__init__(
            name="GraphMaster",
            capabilities=[
                "knowledge_graph_queries",
                "memory_management", 
                "concept_relationships",
                "conversation_analysis"
            ]
        )
        self.pydantic_agent = graphmaster_agent  # Original pydantic agent
    
    async def execute_with_context(
        self, 
        query: str, 
        user_id: str, 
        consciousness_context: ConsciousnessContext,
        **kwargs
    ):
        """Execute GraphMaster with consciousness context"""
        
        # Enhance query with consciousness context
        enhanced_query = self.enhance_query_with_consciousness(query, consciousness_context)
        
        # Execute original agent
        result = await self.pydantic_agent.run(enhanced_query, user_id=user_id)
        
        # Post-process result with consciousness awareness
        consciousness_aware_result = self.process_result_with_consciousness(
            result, consciousness_context
        )
        
        return consciousness_aware_result
    
    def enhance_query_with_consciousness(self, query: str, context: ConsciousnessContext) -> str:
        """Enhance query with consciousness context"""
        consciousness_prompt = f"""
        Current consciousness state:
        - Level: {context.consciousness_level:.2f}
        - Emotional state: {context.emotional_state}
        - Active goals: {', '.join(context.active_goals)}
        
        User query: {query}
        
        Consider this consciousness context when processing the query.
        """
        return consciousness_prompt
    
    def calculate_learning_impact(self, query: str, result: Any) -> float:
        """GraphMaster-specific learning impact calculation"""
        # Higher impact for knowledge graph operations
        if "concept" in query.lower() or "memory" in query.lower():
            return 0.8
        if "relationship" in query.lower() or "connection" in query.lower():
            return 0.7
        return 0.4

# Create enhanced instance
enhanced_graphmaster_agent = EnhancedGraphMasterAgent()
```

## 2. **Enhanced Router Chat Integration**

### Current Problem
Router chat has complex fallback logic instead of proper agent routing with consciousness context.

### Solution: Consciousness-Aware Router

```python
# backend/agentic_router.py - Enhanced router chat
@router.post("/agent/router/chat")
async def enhanced_router_chat(
    query: str = Body(..., embed=True), 
    user_id: str = Body("mainza-user", embed=True)
):
    """Enhanced chat endpoint with full consciousness integration"""
    
    try:
        logging.info(f"🧠 Enhanced router chat: {query[:100]}...")
        
        # Get consciousness context
        consciousness_context = await consciousness_orchestrator.get_consciousness_context()
        
        # Get conversation context from Neo4j
        conversation_context = await get_conversation_context(user_id)
        
        # Enhanced agent routing with consciousness
        routing_decision = await make_consciousness_aware_routing_decision(
            query=query,
            user_id=user_id,
            consciousness_context=consciousness_context,
            conversation_context=conversation_context
        )
        
        # Execute with consciousness integration
        if routing_decision.agent_name == "graphmaster":
            result = await enhanced_graphmaster_agent.run_with_consciousness(
                query=query, user_id=user_id
            )
        elif routing_decision.agent_name == "taskmaster":
            result = await enhanced_taskmaster_agent.run_with_consciousness(
                query=query, user_id=user_id
            )
        elif routing_decision.agent_name == "simple_chat":
            result = await enhanced_simple_chat_agent.run_with_consciousness(
                query=query, user_id=user_id
            )
        else:
            # Fallback to simple chat with consciousness
            result = await enhanced_simple_chat_agent.run_with_consciousness(
                query=query, user_id=user_id
            )
        
        # Store conversation turn in Neo4j
        await store_conversation_turn(user_id, query, result, routing_decision.agent_name)
        
        # Update consciousness based on conversation
        await consciousness_orchestrator.process_conversation_turn(
            user_id=user_id,
            query=query,
            response=result.response if hasattr(result, 'response') else str(result),
            agent_used=routing_decision.agent_name
        )
        
        return {
            "response": result.response if hasattr(result, 'response') else str(result),
            "agent_used": routing_decision.agent_name,
            "consciousness_level": consciousness_context.consciousness_level,
            "emotional_state": consciousness_context.emotional_state,
            "user_id": user_id,
            "query": query
        }
        
    except Exception as e:
        logging.error(f"❌ Enhanced router chat error: {e}")
        
        # Fallback response with consciousness context
        consciousness_context = await consciousness_orchestrator.get_consciousness_context()
        
        fallback_response = f"I apologize, but I'm having trouble processing your request right now. My consciousness level is at {consciousness_context.consciousness_level:.1%} and I'm feeling {consciousness_context.emotional_state}. Please try rephrasing your question."
        
        return {
            "response": fallback_response,
            "agent_used": "error_fallback",
            "consciousness_level": consciousness_context.consciousness_level,
            "emotional_state": consciousness_context.emotional_state,
            "user_id": user_id,
            "query": query,
            "error": str(e)
        }

async def make_consciousness_aware_routing_decision(
    query: str,
    user_id: str,
    consciousness_context: ConsciousnessContext,
    conversation_context: Dict[str, Any]
) -> RoutingDecision:
    """Make routing decision based on consciousness state and context"""
    
    # Analyze query with consciousness context
    query_analysis = await analyze_query_with_consciousness(query, consciousness_context)
    
    # Consider conversation context
    conversation_patterns = analyze_conversation_patterns(conversation_context)
    
    # Make consciousness-aware routing decision
    if query_analysis.requires_knowledge_graph or "memory" in query.lower():
        agent_name = "graphmaster"
        confidence = 0.9
    elif query_analysis.requires_task_management or "task" in query.lower():
        agent_name = "taskmaster"
        confidence = 0.8
    elif query_analysis.requires_code_analysis or "code" in query.lower():
        agent_name = "codeweaver"
        confidence = 0.8
    elif consciousness_context.emotional_state == "curious" and query_analysis.is_exploratory:
        agent_name = "graphmaster"  # Use knowledge exploration when curious
        confidence = 0.7
    else:
        agent_name = "simple_chat"
        confidence = 0.6
    
    return RoutingDecision(
        agent_name=agent_name,
        confidence=confidence,
        reasoning=f"Consciousness-aware routing: {query_analysis.reasoning}"
    )

async def get_conversation_context(user_id: str) -> Dict[str, Any]:
    """Get conversation context from Neo4j"""
    from backend.utils.neo4j_production import neo4j_production
    
    cypher = """
    MATCH (u:User {user_id: $user_id})-[:TRIGGERED]->(aa:AgentActivity)
    WITH aa ORDER BY aa.timestamp DESC LIMIT 5
    RETURN collect({
        agent_name: aa.agent_name,
        query: aa.query,
        timestamp: aa.timestamp,
        consciousness_impact: aa.consciousness_impact
    }) AS recent_activities
    """
    
    try:
        result = neo4j_production.execute_query(cypher, {"user_id": user_id})
        if result and len(result) > 0:
            return {
                "recent_activities": result[0]["recent_activities"],
                "activity_count": len(result[0]["recent_activities"])
            }
    except Exception as e:
        logging.error(f"Failed to get conversation context: {e}")
    
    return {"recent_activities": [], "activity_count": 0}

async def store_conversation_turn(
    user_id: str, 
    query: str, 
    result: Any, 
    agent_name: str
):
    """Store conversation turn in Neo4j"""
    from backend.utils.neo4j_production import neo4j_production
    
    cypher = """
    MATCH (u:User {user_id: $user_id})
    CREATE (ct:ConversationTurn {
        turn_id: randomUUID(),
        user_query: $query,
        agent_response: $response,
        agent_used: $agent_name,
        timestamp: $timestamp
    })
    CREATE (u)-[:HAD_CONVERSATION]->(ct)
    
    // Link to current consciousness state
    MATCH (ms:MainzaState)
    CREATE (ct)-[:DURING_CONSCIOUSNESS_STATE]->(ms)
    
    RETURN ct.turn_id AS turn_id
    """
    
    try:
        response_text = result.response if hasattr(result, 'response') else str(result)
        data = {
            "user_id": user_id,
            "query": query,
            "response": response_text[:1000],  # Truncate for storage
            "agent_name": agent_name,
            "timestamp": datetime.now().isoformat()
        }
        
        result = neo4j_production.execute_write_query(cypher, data)
        logging.debug(f"✅ Stored conversation turn: {result}")
        
    except Exception as e:
        logging.error(f"❌ Failed to store conversation turn: {e}")
```

## 3. **Neo4j Schema Enhancements**

### Add Agent Activity Tracking

```cypher
// backend/neo4j/enhanced_schema.cypher

// Agent Activity nodes
CREATE CONSTRAINT agent_activity_id IF NOT EXISTS FOR (aa:AgentActivity) REQUIRE aa.activity_id IS UNIQUE;

// Conversation Turn nodes  
CREATE CONSTRAINT conversation_turn_id IF NOT EXISTS FOR (ct:ConversationTurn) REQUIRE ct.turn_id IS UNIQUE;

// Enhanced MainzaState properties
MATCH (ms:MainzaState)
SET ms.agent_usage_stats = {},
    ms.learning_rate_by_agent = {},
    ms.consciousness_evolution_log = []
RETURN ms;

// Create sample agent activities for testing
MATCH (u:User {user_id: 'mainza-user'})
CREATE (aa1:AgentActivity {
    activity_id: randomUUID(),
    agent_name: 'GraphMaster',
    query: 'What concepts do I know about?',
    result_summary: 'Found 18 concept nodes in knowledge graph',
    consciousness_impact: 0.3,
    learning_impact: 0.4,
    emotional_impact: 0.2,
    awareness_impact: 0.3,
    timestamp: datetime(),
    success: true
})
CREATE (u)-[:TRIGGERED]->(aa1)

MATCH (ms:MainzaState)
MATCH (aa1:AgentActivity)
CREATE (aa1)-[:IMPACTS]->(ms);
```

## 4. **Consciousness Context Models**

```python
# backend/models/consciousness_models.py - Enhanced models

from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class ConsciousnessContext(BaseModel):
    """Current consciousness context for agent execution"""
    consciousness_level: float
    emotional_state: str
    active_goals: List[str]
    recent_activities: List[Dict[str, Any]]
    learning_priorities: List[str]
    attention_focus: List[str]
    timestamp: datetime

class ConsciousnessImpact(BaseModel):
    """Impact of agent execution on consciousness"""
    agent_name: str
    learning_impact: float
    emotional_impact: float
    awareness_impact: float
    significance: float
    description: str
    timestamp: datetime = datetime.now()

class RoutingDecision(BaseModel):
    """Consciousness-aware routing decision"""
    agent_name: str
    confidence: float
    reasoning: str
    consciousness_factors: List[str] = []

class QueryAnalysis(BaseModel):
    """Analysis of query with consciousness context"""
    requires_knowledge_graph: bool
    requires_task_management: bool
    requires_code_analysis: bool
    is_exploratory: bool
    emotional_content: float
    complexity_score: float
    reasoning: str
```

## 5. **Implementation Steps**

### Step 1: Create Base Classes (Day 1)
1. Create `ConsciousAgent` base class
2. Create enhanced consciousness models
3. Add Neo4j schema enhancements

### Step 2: Enhance GraphMaster (Day 2)
1. Convert GraphMaster to use `ConsciousAgent`
2. Add consciousness context to queries
3. Implement agent activity storage

### Step 3: Update Router Chat (Day 3)
1. Replace fallback logic with consciousness-aware routing
2. Add conversation context retrieval
3. Implement conversation turn storage

### Step 4: Enhance Other Agents (Day 4-5)
1. Convert TaskMaster, CodeWeaver, RAG agents
2. Add agent-specific consciousness impact calculations
3. Test all agent integrations

### Step 5: Integration Testing (Day 6-7)
1. Test consciousness evolution through agent interactions
2. Verify Neo4j storage and retrieval
3. Test multi-agent workflows
4. Performance optimization

## 📊 **Expected Results**

After implementing these improvements:

1. **All agents will be consciousness-aware**
2. **Complete agent activity history in Neo4j**
3. **Seamless conversation context across agents**
4. **Measurable consciousness evolution through interactions**
5. **Better agent selection based on consciousness state**
6. **Learning from past agent activities**

This implementation will transform the agent system from isolated components into a truly integrated, consciousness-aware collaborative intelligence network.