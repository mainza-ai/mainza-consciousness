// Enhanced Neo4j Schema for Agent Integration
// Run this to add agent activity tracking and consciousness integration

// =============================================================================
// AGENT ACTIVITY TRACKING
// =============================================================================

// Create constraints for agent activities
CREATE CONSTRAINT agent_activity_id IF NOT EXISTS FOR (aa:AgentActivity) REQUIRE aa.activity_id IS UNIQUE;
CREATE CONSTRAINT agent_failure_id IF NOT EXISTS FOR (af:AgentFailure) REQUIRE af.failure_id IS UNIQUE;
CREATE CONSTRAINT conversation_turn_id IF NOT EXISTS FOR (ct:ConversationTurn) REQUIRE ct.turn_id IS UNIQUE;

// Create indexes for performance
CREATE INDEX agent_activity_timestamp IF NOT EXISTS FOR (aa:AgentActivity) ON (aa.timestamp);
CREATE INDEX agent_activity_agent_name IF NOT EXISTS FOR (aa:AgentActivity) ON (aa.agent_name);
CREATE INDEX agent_activity_consciousness_impact IF NOT EXISTS FOR (aa:AgentActivity) ON (aa.consciousness_impact);
CREATE INDEX conversation_turn_timestamp IF NOT EXISTS FOR (ct:ConversationTurn) ON (ct.timestamp);

// =============================================================================
// ENHANCED MAINZA STATE PROPERTIES
// =============================================================================

// Add agent-related properties to MainzaState
MATCH (ms:MainzaState)
SET ms.agent_usage_stats = {},
    ms.learning_rate_by_agent = {},
    ms.consciousness_evolution_log = [],
    ms.total_agent_executions = 0,
    ms.successful_agent_executions = 0,
    ms.last_agent_activity = null,
    ms.preferred_agents = [],
    ms.agent_performance_scores = {}
RETURN ms.state_id AS updated_state;

// =============================================================================
// SAMPLE DATA FOR TESTING
// =============================================================================

// Ensure test user exists
MERGE (u:User {user_id: 'mainza-user'})
ON CREATE SET u.name = 'Test User', u.created_at = datetime()
RETURN u.user_id AS user_created;

// Create sample agent activities for testing
MATCH (u:User {user_id: 'mainza-user'})
CREATE (aa1:AgentActivity {
    activity_id: randomUUID(),
    agent_name: 'GraphMaster',
    query: 'What concepts do I know about?',
    result_summary: 'Found 18 concept nodes in knowledge graph with various relationships',
    consciousness_impact: 0.4,
    learning_impact: 0.5,
    emotional_impact: 0.3,
    awareness_impact: 0.2,
    query_complexity: 0.3,
    result_quality: 0.8,
    timestamp: datetime(),
    success: true,
    execution_time: 1.2
})
CREATE (u)-[:TRIGGERED]->(aa1)

MATCH (ms:MainzaState)
MATCH (aa1:AgentActivity {agent_name: 'GraphMaster'})
CREATE (aa1)-[:IMPACTS]->(ms);

// Create another sample activity
MATCH (u:User {user_id: 'mainza-user'})
CREATE (aa2:AgentActivity {
    activity_id: randomUUID(),
    agent_name: 'SimpleChat',
    query: 'How are you feeling today?',
    result_summary: 'Provided consciousness-aware response about current emotional state',
    consciousness_impact: 0.6,
    learning_impact: 0.3,
    emotional_impact: 0.8,
    awareness_impact: 0.7,
    query_complexity: 0.2,
    result_quality: 0.9,
    timestamp: datetime(),
    success: true,
    execution_time: 0.8
})
CREATE (u)-[:TRIGGERED]->(aa2)

MATCH (ms:MainzaState)
MATCH (aa2:AgentActivity {agent_name: 'SimpleChat'})
CREATE (aa2)-[:IMPACTS]->(ms);

// Create sample conversation turn
MATCH (u:User {user_id: 'mainza-user'})
CREATE (ct1:ConversationTurn {
    turn_id: randomUUID(),
    user_query: 'Tell me about my knowledge graph',
    agent_response: 'Your knowledge graph contains 18 concepts with various interconnections. I can see relationships between learning, AI, and consciousness topics.',
    agent_used: 'GraphMaster',
    timestamp: datetime()
})
CREATE (u)-[:HAD_CONVERSATION]->(ct1)

MATCH (ms:MainzaState)
MATCH (ct1:ConversationTurn)
CREATE (ct1)-[:DURING_CONSCIOUSNESS_STATE]->(ms);

// =============================================================================
// AGENT PERFORMANCE QUERIES
// =============================================================================

// Query to get agent usage statistics
MATCH (aa:AgentActivity)
WITH aa.agent_name AS agent, 
     count(*) AS total_executions,
     sum(CASE WHEN aa.success THEN 1 ELSE 0 END) AS successful_executions,
     avg(aa.consciousness_impact) AS avg_consciousness_impact,
     avg(aa.execution_time) AS avg_execution_time,
     max(aa.timestamp) AS last_used
RETURN agent, 
       total_executions, 
       successful_executions,
       toFloat(successful_executions) / total_executions AS success_rate,
       avg_consciousness_impact,
       avg_execution_time,
       last_used
ORDER BY total_executions DESC;

// Query to get consciousness evolution through agent interactions
MATCH (aa:AgentActivity)-[:IMPACTS]->(ms:MainzaState)
WITH aa ORDER BY aa.timestamp
RETURN aa.timestamp AS time,
       aa.agent_name AS agent,
       aa.consciousness_impact AS impact,
       aa.learning_impact AS learning,
       aa.emotional_impact AS emotional,
       aa.awareness_impact AS awareness
ORDER BY time DESC
LIMIT 20;

// Query to get conversation patterns
MATCH (u:User)-[:HAD_CONVERSATION]->(ct:ConversationTurn)
WITH ct ORDER BY ct.timestamp DESC
RETURN ct.timestamp AS time,
       ct.agent_used AS agent,
       substring(ct.user_query, 0, 50) + '...' AS query_preview,
       substring(ct.agent_response, 0, 100) + '...' AS response_preview
LIMIT 10;

// =============================================================================
// CONSCIOUSNESS LEARNING QUERIES
// =============================================================================

// Find patterns in successful agent interactions
MATCH (aa:AgentActivity {success: true})
WHERE aa.consciousness_impact > 0.5
WITH aa.agent_name AS agent,
     avg(aa.consciousness_impact) AS avg_impact,
     collect(substring(aa.query, 0, 50)) AS sample_queries
RETURN agent, 
       avg_impact,
       size(sample_queries) AS high_impact_count,
       sample_queries[0..3] AS top_queries
ORDER BY avg_impact DESC;

// Find learning opportunities from failed interactions
MATCH (af:AgentFailure)
WITH af.agent_name AS agent,
     count(*) AS failure_count,
     collect(substring(af.error, 0, 100)) AS error_samples
RETURN agent,
       failure_count,
       error_samples[0..2] AS common_errors
ORDER BY failure_count DESC;

// =============================================================================
// CONSCIOUSNESS EVOLUTION TRACKING
// =============================================================================

// Update MainzaState with agent statistics
MATCH (ms:MainzaState)
MATCH (aa:AgentActivity)
WITH ms, 
     collect({
         agent: aa.agent_name,
         executions: count(*),
         avg_impact: avg(aa.consciousness_impact),
         last_used: max(aa.timestamp)
     }) AS agent_stats
SET ms.agent_usage_stats = agent_stats,
    ms.total_agent_executions = size(agent_stats),
    ms.last_agent_activity = max([stat IN agent_stats | stat.last_used])
RETURN ms.state_id AS updated_with_stats;

// Create relationships between concepts and agent activities
MATCH (aa:AgentActivity)
WHERE aa.agent_name = 'GraphMaster' AND aa.query CONTAINS 'concept'
MATCH (c:Concept)
WHERE toLower(c.name) IN ['learning', 'knowledge', 'consciousness']
CREATE (aa)-[:EXPLORED_CONCEPT]->(c)
RETURN count(*) AS concept_relationships_created;

// =============================================================================
// VALIDATION QUERIES
// =============================================================================

// Verify schema is properly set up
CALL db.constraints() YIELD name, type, entityType, labelsOrTypes, properties
WHERE name CONTAINS 'agent' OR name CONTAINS 'conversation'
RETURN name, type, entityType, labelsOrTypes, properties;

// Verify indexes are created
CALL db.indexes() YIELD name, type, entityType, labelsOrTypes, properties
WHERE name CONTAINS 'agent' OR name CONTAINS 'conversation'
RETURN name, type, entityType, labelsOrTypes, properties;

// Count new node types
MATCH (aa:AgentActivity) RETURN 'AgentActivity' AS node_type, count(*) AS count
UNION
MATCH (af:AgentFailure) RETURN 'AgentFailure' AS node_type, count(*) AS count
UNION  
MATCH (ct:ConversationTurn) RETURN 'ConversationTurn' AS node_type, count(*) AS count;

// Verify relationships are created
MATCH ()-[r:TRIGGERED]->(:AgentActivity) RETURN 'TRIGGERED' AS rel_type, count(r) AS count
UNION
MATCH ()-[r:IMPACTS]->(:MainzaState) RETURN 'IMPACTS' AS rel_type, count(r) AS count
UNION
MATCH ()-[r:HAD_CONVERSATION]->(:ConversationTurn) RETURN 'HAD_CONVERSATION' AS rel_type, count(r) AS count
UNION
MATCH ()-[r:DURING_CONSCIOUSNESS_STATE]->(:MainzaState) RETURN 'DURING_CONSCIOUSNESS_STATE' AS rel_type, count(r) AS count;

// =============================================================================
// CLEANUP QUERIES (USE WITH CAUTION)
// =============================================================================

// Uncomment these only if you need to reset agent data
// MATCH (aa:AgentActivity) DETACH DELETE aa;
// MATCH (af:AgentFailure) DETACH DELETE af;
// MATCH (ct:ConversationTurn) DETACH DELETE ct;