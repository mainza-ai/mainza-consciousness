// Fix Neo4j Schema for Insights System
// This script creates missing indexes and ensures proper data structure for insights

// =============================================================================
// CREATE MISSING INDEXES FOR INSIGHTS QUERIES
// =============================================================================

// Create indexes for Concept nodes
CREATE INDEX concept_id_index IF NOT EXISTS FOR (c:Concept) ON (c.concept_id);
CREATE INDEX concept_name_index IF NOT EXISTS FOR (c:Concept) ON (c.name);
CREATE INDEX concept_importance_index IF NOT EXISTS FOR (c:Concept) ON (c.importance_score);
CREATE INDEX concept_usage_frequency_index IF NOT EXISTS FOR (c:Concept) ON (c.usage_frequency);

// Create indexes for AgentActivity nodes
CREATE INDEX agent_activity_timestamp_index IF NOT EXISTS FOR (aa:AgentActivity) ON (aa.timestamp);
CREATE INDEX agent_activity_agent_name_index IF NOT EXISTS FOR (aa:AgentActivity) ON (aa.agent_name);
CREATE INDEX agent_activity_success_index IF NOT EXISTS FOR (aa:AgentActivity) ON (aa.success);
CREATE INDEX agent_activity_consciousness_impact_index IF NOT EXISTS FOR (aa:AgentActivity) ON (aa.consciousness_impact);

// Create indexes for MainzaState nodes
CREATE INDEX mainza_state_timestamp_index IF NOT EXISTS FOR (ms:MainzaState) ON (ms.timestamp);
CREATE INDEX mainza_state_consciousness_level_index IF NOT EXISTS FOR (ms:MainzaState) ON (ms.consciousness_level);

// Create indexes for User nodes
CREATE INDEX user_id_index IF NOT EXISTS FOR (u:User) ON (u.user_id);

// =============================================================================
// ENSURE PROPER DATA STRUCTURE
// =============================================================================

// Ensure Concept nodes have required properties
MATCH (c:Concept)
WHERE c.importance_score IS NULL
SET c.importance_score = 0.5;

MATCH (c:Concept)
WHERE c.usage_frequency IS NULL
SET c.usage_frequency = 0;

MATCH (c:Concept)
WHERE c.consciousness_relevance IS NULL
SET c.consciousness_relevance = 0.5;

MATCH (c:Concept)
WHERE c.evolution_rate IS NULL
SET c.evolution_rate = 0.0;

// Ensure AgentActivity nodes have required properties
MATCH (aa:AgentActivity)
WHERE aa.consciousness_impact IS NULL
SET aa.consciousness_impact = 0.0;

MATCH (aa:AgentActivity)
WHERE aa.learning_impact IS NULL
SET aa.learning_impact = 0.0;

MATCH (aa:AgentActivity)
WHERE aa.emotional_impact IS NULL
SET aa.emotional_impact = 0.0;

MATCH (aa:AgentActivity)
WHERE aa.awareness_impact IS NULL
SET aa.awareness_impact = 0.0;

MATCH (aa:AgentActivity)
WHERE aa.query_complexity IS NULL
SET aa.query_complexity = 0.5;

MATCH (aa:AgentActivity)
WHERE aa.result_quality IS NULL
SET aa.result_quality = 0.8;

MATCH (aa:AgentActivity)
WHERE aa.execution_time IS NULL
SET aa.execution_time = 0.0;

MATCH (aa:AgentActivity)
WHERE aa.success IS NULL
SET aa.success = true;

// =============================================================================
// CREATE SAMPLE DATA FOR TESTING (if no data exists)
// =============================================================================

// Create sample concepts if none exist
MATCH (c:Concept)
WITH count(c) as concept_count
WHERE concept_count = 0
CREATE (c1:Concept {
    concept_id: 'ai',
    name: 'Artificial Intelligence',
    importance_score: 0.9,
    usage_frequency: 15,
    consciousness_relevance: 0.8,
    evolution_rate: 0.1,
    created_at: datetime()
})
CREATE (c2:Concept {
    concept_id: 'consciousness',
    name: 'Consciousness',
    importance_score: 0.95,
    usage_frequency: 12,
    consciousness_relevance: 0.95,
    evolution_rate: 0.15,
    created_at: datetime()
})
CREATE (c3:Concept {
    concept_id: 'learning',
    name: 'Learning',
    importance_score: 0.85,
    usage_frequency: 18,
    consciousness_relevance: 0.7,
    evolution_rate: 0.12,
    created_at: datetime()
})
CREATE (c4:Concept {
    concept_id: 'memory',
    name: 'Memory',
    importance_score: 0.8,
    usage_frequency: 10,
    consciousness_relevance: 0.6,
    evolution_rate: 0.08,
    created_at: datetime()
})
CREATE (c5:Concept {
    concept_id: 'reasoning',
    name: 'Reasoning',
    importance_score: 0.88,
    usage_frequency: 14,
    consciousness_relevance: 0.75,
    evolution_rate: 0.11,
    created_at: datetime()
});

// Create relationships between concepts
MATCH (c1:Concept {concept_id: 'ai'})
MATCH (c2:Concept {concept_id: 'consciousness'})
CREATE (c1)-[:RELATES_TO {strength: 0.9, created_at: datetime()}]->(c2);

MATCH (c1:Concept {concept_id: 'consciousness'})
MATCH (c2:Concept {concept_id: 'learning'})
CREATE (c1)-[:RELATES_TO {strength: 0.8, created_at: datetime()}]->(c2);

MATCH (c1:Concept {concept_id: 'learning'})
MATCH (c2:Concept {concept_id: 'memory'})
CREATE (c1)-[:RELATES_TO {strength: 0.7, created_at: datetime()}]->(c2);

MATCH (c1:Concept {concept_id: 'ai'})
MATCH (c2:Concept {concept_id: 'reasoning'})
CREATE (c1)-[:RELATES_TO {strength: 0.85, created_at: datetime()}]->(c2);

// =============================================================================
// VERIFY SCHEMA
// =============================================================================

// Show all indexes
SHOW INDEXES;

// Show concept count
MATCH (c:Concept)
RETURN count(c) as concept_count;

// Show relationship count
MATCH ()-[r:RELATES_TO]->()
RETURN count(r) as relationship_count;

// Test the clustering query
MATCH (c:Concept)
OPTIONAL MATCH (c)-[:RELATES_TO]-(related:Concept)
WITH c, count(related) as connection_count, collect(related.name)[0..5] as sample_connections
RETURN c.concept_id as concept_id, c.name as name, connection_count, sample_connections
ORDER BY connection_count DESC
LIMIT 20;
