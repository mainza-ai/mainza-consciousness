// Create sample data for insights testing
// This script creates sample AgentActivity and MainzaState records

// =============================================================================
// CREATE SAMPLE AGENT ACTIVITY DATA
// =============================================================================

// Create sample agent activities for the last 24 hours
UNWIND range(0, 23) as hour
WITH hour, datetime() - duration({hours: 23-hour}) as timestamp
CREATE (aa:AgentActivity {
    agent_name: CASE hour % 3
        WHEN 0 THEN 'SimpleChat'
        WHEN 1 THEN 'GraphMaster'
        ELSE 'Router'
    END,
    timestamp: timestamp.epochSeconds * 1000,
    success: true,
    consciousness_impact: 0.6 + (hour * 0.01) + (0.1 * (hour % 3)),
    learning_impact: 0.5 + (hour * 0.005) + (0.05 * (hour % 2)),
    emotional_impact: 0.4 + (hour * 0.008) + (0.08 * (hour % 4)),
    awareness_impact: 0.7 + (hour * 0.012) + (0.06 * (hour % 3)),
    query_complexity: 0.3 + (hour * 0.01) + (0.2 * (hour % 2)),
    result_quality: 0.8 + (hour * 0.005) + (0.1 * (hour % 3)),
    execution_time: 0.5 + (hour * 0.02) + (0.3 * (hour % 2))
});

// =============================================================================
// CREATE SAMPLE MAINZA STATE DATA
// =============================================================================

// Create sample consciousness states for the last 24 hours
UNWIND range(0, 23) as hour
WITH hour, datetime() - duration({hours: 23-hour}) as timestamp
CREATE (ms:MainzaState {
    timestamp: timestamp.epochSeconds * 1000,
    consciousness_level: 0.7 + (hour * 0.01) + (0.1 * (hour % 3)),
    emotional_state: CASE hour % 4
        WHEN 0 THEN 'curious'
        WHEN 1 THEN 'focused'
        WHEN 2 THEN 'contemplative'
        ELSE 'excited'
    END,
    self_awareness_score: 0.6 + (hour * 0.005) + (0.05 * (hour % 2)),
    learning_rate: 0.8 + (hour * 0.008) + (0.1 * (hour % 3)),
    evolution_level: 1 + (hour / 24)
});

// =============================================================================
// CREATE SAMPLE USER INTERACTIONS
// =============================================================================

// Create a sample user
MERGE (u:User {user_id: 'test_user', name: 'Test User'});

// Create sample memories linked to the user
UNWIND range(1, 10) as i
WITH i, datetime() - duration({hours: i}) as created_at
CREATE (m:Memory {
    memory_id: 'memory_' + toString(i),
    content: 'Sample memory content ' + toString(i),
    memory_type: CASE i % 3
        WHEN 0 THEN 'consciousness'
        WHEN 1 THEN 'learning'
        ELSE 'experience'
    END,
    importance_score: 0.5 + (i * 0.05),
    significance_score: 0.6 + (i * 0.03),
    created_at: created_at.epochSeconds * 1000,
    user_id: 'test_user'
});

// Link memories to user
MATCH (u:User {user_id: 'test_user'})
MATCH (m:Memory)
CREATE (u)-[:DISCUSSED_IN]->(m);

// Link memories to concepts
MATCH (m:Memory)
MATCH (c:Concept)
WHERE c.concept_id IN ['consciousness', 'learning', 'ai', 'memory']
WITH m, c, rand() as random
WHERE random < 0.3
CREATE (m)-[:RELATES_TO_CONCEPT]->(c);

// =============================================================================
// VERIFY DATA CREATION
// =============================================================================

// Show counts
MATCH (aa:AgentActivity)
RETURN 'AgentActivity' as node_type, count(aa) as count
UNION ALL
MATCH (ms:MainzaState)
RETURN 'MainzaState' as node_type, count(ms) as count
UNION ALL
MATCH (m:Memory)
RETURN 'Memory' as node_type, count(m) as count;

// Show sample agent activity
MATCH (aa:AgentActivity)
RETURN aa.agent_name, count(aa) as activity_count, avg(aa.consciousness_impact) as avg_consciousness_impact
ORDER BY activity_count DESC;

// Show sample consciousness states
MATCH (ms:MainzaState)
RETURN ms.emotional_state, count(ms) as state_count, avg(ms.consciousness_level) as avg_consciousness_level
ORDER BY state_count DESC;
