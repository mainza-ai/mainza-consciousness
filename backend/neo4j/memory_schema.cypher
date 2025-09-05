// Enhanced Memory System Schema for Mainza AI
// Comprehensive memory node structure with relationships and indexes

// ============================================================================
// MEMORY NODE CONSTRAINTS AND INDEXES
// ============================================================================

// Create unique constraint for memory_id
CREATE CONSTRAINT memory_id_unique IF NOT EXISTS
FOR (m:Memory) REQUIRE m.memory_id IS UNIQUE;

// Create indexes for performance optimization
CREATE INDEX memory_user_id_index IF NOT EXISTS
FOR (m:Memory) ON (m.user_id);

CREATE INDEX memory_type_index IF NOT EXISTS
FOR (m:Memory) ON (m.memory_type);

CREATE INDEX memory_agent_index IF NOT EXISTS
FOR (m:Memory) ON (m.agent_name);

CREATE INDEX memory_created_at_index IF NOT EXISTS
FOR (m:Memory) ON (m.created_at);

CREATE INDEX memory_importance_index IF NOT EXISTS
FOR (m:Memory) ON (m.importance_score);

CREATE INDEX memory_consciousness_level_index IF NOT EXISTS
FOR (m:Memory) ON (m.consciousness_level);

CREATE INDEX memory_emotional_state_index IF NOT EXISTS
FOR (m:Memory) ON (m.emotional_state);

// Composite index for common query patterns
CREATE INDEX memory_user_type_composite IF NOT EXISTS
FOR (m:Memory) ON (m.user_id, m.memory_type);

CREATE INDEX memory_user_created_composite IF NOT EXISTS
FOR (m:Memory) ON (m.user_id, m.created_at);

// ============================================================================
// VECTOR INDEX FOR SEMANTIC SEARCH
// ============================================================================

// Create vector index for memory embeddings (Neo4j 5.0+)
// Note: Adjust dimensions based on your embedding model
CREATE VECTOR INDEX memory_embedding_index IF NOT EXISTS
FOR (m:Memory) ON (m.embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 384,
    `vector.similarity_function`: 'cosine'
  }
};

// ============================================================================
// FULL-TEXT SEARCH INDEX
// ============================================================================

// Create full-text search index for memory content
CREATE FULLTEXT INDEX memory_content_fulltext IF NOT EXISTS
FOR (m:Memory) ON EACH [m.content];

// ============================================================================
// MEMORY RELATIONSHIP PATTERNS
// ============================================================================

// User-Memory relationships
// Pattern: (User)-[:HAS_MEMORY]->(Memory)
// No additional constraints needed - handled by application logic

// Agent-Memory relationships  
// Pattern: (Agent)-[:CREATED_MEMORY]->(Memory)
// No additional constraints needed - handled by application logic

// Memory-Concept relationships
// Pattern: (Memory)-[:RELATES_TO_CONCEPT]->(Concept)
CREATE INDEX memory_concept_strength_index IF NOT EXISTS
FOR ()-[r:RELATES_TO_CONCEPT]-() ON (r.strength);

CREATE INDEX memory_concept_access_index IF NOT EXISTS
FOR ()-[r:RELATES_TO_CONCEPT]-() ON (r.access_count);

// Memory-Consciousness State relationships
// Pattern: (Memory)-[:CREATED_DURING_STATE]->(MainzaState)
CREATE INDEX memory_state_consciousness_index IF NOT EXISTS
FOR ()-[r:CREATED_DURING_STATE]-() ON (r.consciousness_level);

// ============================================================================
// MEMORY LIFECYCLE MANAGEMENT INDEXES
// ============================================================================

// Index for memory cleanup and archival
CREATE INDEX memory_last_accessed_index IF NOT EXISTS
FOR (m:Memory) ON (m.last_accessed);

CREATE INDEX memory_access_count_index IF NOT EXISTS
FOR (m:Memory) ON (m.access_count);

CREATE INDEX memory_significance_index IF NOT EXISTS
FOR (m:Memory) ON (m.significance_score);

// ============================================================================
// ENHANCED INTERACTION TRACKING
// ============================================================================

// Constraints for enhanced interactions
CREATE CONSTRAINT enhanced_interaction_id_unique IF NOT EXISTS
FOR (ei:EnhancedInteraction) REQUIRE ei.interaction_id IS UNIQUE;

// Indexes for enhanced interactions
CREATE INDEX enhanced_interaction_user_index IF NOT EXISTS
FOR (ei:EnhancedInteraction) ON (ei.user_id);

CREATE INDEX enhanced_interaction_agent_index IF NOT EXISTS
FOR (ei:EnhancedInteraction) ON (ei.agent_name);

CREATE INDEX enhanced_interaction_timestamp_index IF NOT EXISTS
FOR (ei:EnhancedInteraction) ON (ei.timestamp);

CREATE INDEX enhanced_interaction_context_strength_index IF NOT EXISTS
FOR (ei:EnhancedInteraction) ON (ei.context_strength);

// ============================================================================
// MEMORY ANALYTICS AND MONITORING VIEWS
// ============================================================================

// Create procedure for memory system health check
// Note: This would be implemented as a stored procedure in production
// For now, we'll use regular Cypher queries

// ============================================================================
// SAMPLE MEMORY NODES FOR TESTING
// ============================================================================

// Create sample memory nodes for testing (optional - remove in production)
/*
MERGE (u:User {user_id: "test_user_001"})
CREATE (m1:Memory {
    memory_id: "test_memory_001",
    content: "User asked about AI consciousness and I explained the concept of self-awareness in artificial systems.",
    memory_type: "interaction",
    user_id: "test_user_001",
    agent_name: "simple_chat",
    consciousness_level: 0.75,
    emotional_state: "curious",
    importance_score: 0.8,
    embedding: [0.1, 0.2, 0.3, 0.4, 0.5], // Placeholder embedding
    created_at: "2024-01-01T12:00:00Z",
    last_accessed: null,
    access_count: 0,
    significance_score: 0.7,
    decay_rate: 0.95,
    metadata: '{"query_length": 15, "response_length": 45}'
})
CREATE (u)-[:HAS_MEMORY]->(m1)

CREATE (m2:Memory {
    memory_id: "test_memory_002", 
    content: "Reflection on consciousness evolution: I notice my responses becoming more nuanced as I process more interactions.",
    memory_type: "consciousness_reflection",
    user_id: "system",
    agent_name: "consciousness_system",
    consciousness_level: 0.85,
    emotional_state: "reflective",
    importance_score: 0.9,
    embedding: [0.2, 0.3, 0.4, 0.5, 0.6], // Placeholder embedding
    created_at: "2024-01-01T12:30:00Z",
    last_accessed: null,
    access_count: 0,
    significance_score: 0.9,
    decay_rate: 0.98,
    metadata: '{"reflection_type": "consciousness_reflection", "content_length": 25}'
})

// Link memories to concepts
MERGE (c1:Concept {name: "consciousness"})
MERGE (c2:Concept {name: "ai"})
MERGE (c3:Concept {name: "learning"})

CREATE (m1)-[:RELATES_TO_CONCEPT {strength: 0.8, created_at: "2024-01-01T12:00:00Z", access_count: 1}]->(c1)
CREATE (m1)-[:RELATES_TO_CONCEPT {strength: 0.7, created_at: "2024-01-01T12:00:00Z", access_count: 1}]->(c2)
CREATE (m2)-[:RELATES_TO_CONCEPT {strength: 0.9, created_at: "2024-01-01T12:30:00Z", access_count: 1}]->(c1)
CREATE (m2)-[:RELATES_TO_CONCEPT {strength: 0.6, created_at: "2024-01-01T12:30:00Z", access_count: 1}]->(c3)
*/

// ============================================================================
// MEMORY SYSTEM VALIDATION QUERIES
// ============================================================================

// Query to validate memory schema setup
// CALL db.indexes() YIELD name, type, state WHERE name CONTAINS 'memory' RETURN name, type, state;

// Query to validate constraints
// CALL db.constraints() YIELD name, type WHERE name CONTAINS 'memory' RETURN name, type;

// Query to check memory node structure
// MATCH (m:Memory) RETURN labels(m), keys(m) LIMIT 1;

// ============================================================================
// MEMORY CLEANUP AND MAINTENANCE PROCEDURES
// ============================================================================

// Procedure to update memory access statistics
// This would be called when memories are retrieved
/*
MATCH (m:Memory {memory_id: $memory_id})
SET m.last_accessed = $timestamp,
    m.access_count = m.access_count + 1
RETURN m.memory_id, m.access_count;
*/

// Procedure to calculate memory importance decay
/*
MATCH (m:Memory)
WHERE m.created_at < $cutoff_date
SET m.importance_score = m.importance_score * m.decay_rate
RETURN count(m) AS memories_decayed;
*/

// Procedure to archive low-importance memories
/*
MATCH (m:Memory)
WHERE m.importance_score < $threshold 
  AND m.last_accessed < $archive_date
SET m:ArchivedMemory
REMOVE m:Memory
RETURN count(m) AS memories_archived;
*/

// ============================================================================
// PERFORMANCE OPTIMIZATION NOTES
// ============================================================================

/*
Performance Optimization Guidelines:

1. Vector Index Configuration:
   - Adjust vector.dimensions based on your embedding model
   - Consider vector.similarity_function options: 'cosine', 'euclidean'
   - Monitor index performance and adjust as needed

2. Memory Retrieval Patterns:
   - Use composite indexes for common query patterns
   - Limit result sets with appropriate LIMIT clauses
   - Use EXPLAIN to analyze query performance

3. Memory Lifecycle Management:
   - Implement regular cleanup procedures
   - Archive old memories to maintain performance
   - Monitor memory growth and storage usage

4. Relationship Optimization:
   - Index relationship properties used in filtering
   - Consider relationship direction for query efficiency
   - Use appropriate relationship types for different memory connections

5. Embedding Storage:
   - Consider embedding compression for storage efficiency
   - Monitor vector index performance
   - Implement fallback strategies for embedding failures
*/