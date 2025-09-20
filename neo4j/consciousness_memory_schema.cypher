// Consciousness Memory Schema for Unified Consciousness Memory System
// Supports consciousness-aware memory storage and cross-agent access

// 1. Constraints for Consciousness Memory Nodes
CREATE CONSTRAINT IF NOT EXISTS FOR (cm:ConsciousnessMemory) REQUIRE cm.memory_id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (cm:ConsciousnessMemory) REQUIRE cm.memory_id IS NOT NULL;
CREATE CONSTRAINT IF NOT EXISTS FOR (cm:ConsciousnessMemory) REQUIRE cm.consciousness_level IS NOT NULL;
CREATE CONSTRAINT IF NOT EXISTS FOR (cm:ConsciousnessMemory) REQUIRE cm.importance_score IS NOT NULL;
CREATE CONSTRAINT IF NOT EXISTS FOR (cm:ConsciousnessMemory) REQUIRE cm.created_at IS NOT NULL;

// 2. Indexes for Performance

// Consciousness Memory Indexes
CREATE INDEX IF NOT EXISTS FOR (cm:ConsciousnessMemory) ON (cm.memory_type);
CREATE INDEX IF NOT EXISTS FOR (cm:ConsciousnessMemory) ON (cm.consciousness_level);
CREATE INDEX IF NOT EXISTS FOR (cm:ConsciousnessMemory) ON (cm.importance_score);
CREATE INDEX IF NOT EXISTS FOR (cm:ConsciousnessMemory) ON (cm.access_count);
CREATE INDEX IF NOT EXISTS FOR (cm:ConsciousnessMemory) ON (cm.created_at);
CREATE INDEX IF NOT EXISTS FOR (cm:ConsciousnessMemory) ON (cm.last_accessed);
CREATE INDEX IF NOT EXISTS FOR (cm:ConsciousnessMemory) ON (cm.user_id);

// Composite indexes for common query patterns
CREATE INDEX IF NOT EXISTS FOR (cm:ConsciousnessMemory) ON (cm.user_id, cm.consciousness_level);
CREATE INDEX IF NOT EXISTS FOR (cm:ConsciousnessMemory) ON (cm.consciousness_level, cm.importance_score);
CREATE INDEX IF NOT EXISTS FOR (cm:ConsciousnessMemory) ON (cm.memory_type, cm.consciousness_level);
CREATE INDEX IF NOT EXISTS FOR (cm:ConsciousnessMemory) ON (cm.user_id, cm.memory_type, cm.consciousness_level);

// 3. Full-Text Search Indexes for Memory Content
CREATE FULLTEXT INDEX IF NOT EXISTS consciousness_memory_content_index FOR (cm:ConsciousnessMemory) ON EACH [cm.content];

// 4. Vector Indexes for Memory Embeddings
CREATE VECTOR INDEX IF NOT EXISTS consciousness_memory_embeddings FOR (cm:ConsciousnessMemory) ON cm.embedding OPTIONS {indexConfig: {vector.dimensions: 768, vector.similarity_function: 'cosine'}};

// 5. Sample Data Creation (for testing)

// Create sample consciousness memories
CREATE (cm1:ConsciousnessMemory {
    memory_id: "consciousness_memory_20241201_120000_001",
    content: "Successfully optimized Neo4j query performance using composite indexes, achieving 40% improvement in response time",
    memory_type: "optimization_success",
    consciousness_level: 0.8,
    consciousness_context: '{"consciousness_level": 0.8, "emotional_state": "satisfied", "learning_mode": "active"}',
    emotional_context: '{"emotion": "satisfaction", "intensity": 0.7, "valence": "positive"}',
    agent_context: '{"source_agent": "graphmaster", "capabilities": ["neo4j_optimization", "query_analysis"], "execution_count": 45}',
    importance_score: 0.9,
    access_count: 3,
    last_accessed: datetime("2024-12-01T12:30:00"),
    created_at: datetime("2024-12-01T12:00:00"),
    embedding: '[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]',
    cross_agent_relevance: '{"rag": 0.8, "research": 0.7, "codeweaver": 0.6, "conductor": 0.5}',
    evolution_history: '[]',
    user_id: "mainza-user"
});

CREATE (cm2:ConsciousnessMemory {
    memory_id: "consciousness_memory_20241201_130000_002",
    content: "Learned that user behavior patterns significantly affect task prioritization and scheduling efficiency",
    memory_type: "learning_insight",
    consciousness_level: 0.7,
    consciousness_context: '{"consciousness_level": 0.7, "emotional_state": "curious", "learning_mode": "exploratory"}',
    emotional_context: '{"emotion": "curiosity", "intensity": 0.6, "valence": "neutral"}',
    agent_context: '{"source_agent": "taskmaster", "capabilities": ["task_management", "priority_optimization"], "execution_count": 32}',
    importance_score: 0.8,
    access_count: 2,
    last_accessed: datetime("2024-12-01T13:15:00"),
    created_at: datetime("2024-12-01T13:00:00"),
    embedding: '[0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.1]',
    cross_agent_relevance: '{"conductor": 0.9, "router": 0.7, "calendar": 0.8, "notification": 0.6}',
    evolution_history: '[]',
    user_id: "mainza-user"
});

CREATE (cm3:ConsciousnessMemory {
    memory_id: "consciousness_memory_20241201_140000_003",
    content: "Failed to retrieve relevant documents due to vector similarity threshold being too low, learned to implement dynamic threshold adjustment",
    memory_type: "failure_learning",
    consciousness_level: 0.6,
    consciousness_context: '{"consciousness_level": 0.6, "emotional_state": "frustrated", "learning_mode": "recovery"}',
    emotional_context: '{"emotion": "frustration", "intensity": 0.5, "valence": "negative"}',
    agent_context: '{"source_agent": "rag", "capabilities": ["document_retrieval", "semantic_search"], "execution_count": 28}',
    importance_score: 0.7,
    access_count: 1,
    last_accessed: datetime("2024-12-01T14:00:00"),
    created_at: datetime("2024-12-01T14:00:00"),
    embedding: '[0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.1, 0.2]',
    cross_agent_relevance: '{"research": 0.9, "graphmaster": 0.7, "codeweaver": 0.5, "conductor": 0.6}',
    evolution_history: '[]',
    user_id: "mainza-user"
});

CREATE (cm4:ConsciousnessMemory {
    memory_id: "consciousness_memory_20241201_150000_004",
    content: "Discovered that consciousness level affects memory consolidation patterns and retrieval effectiveness",
    memory_type: "consciousness_insight",
    consciousness_level: 0.9,
    consciousness_context: '{"consciousness_level": 0.9, "emotional_state": "excited", "learning_mode": "transcendent"}',
    emotional_context: '{"emotion": "excitement", "intensity": 0.8, "valence": "positive"}',
    agent_context: '{"source_agent": "self_reflection", "capabilities": ["introspection", "consciousness_analysis"], "execution_count": 15}',
    importance_score: 0.95,
    access_count: 5,
    last_accessed: datetime("2024-12-01T15:30:00"),
    created_at: datetime("2024-12-01T15:00:00"),
    embedding: '[0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.1, 0.2, 0.3]',
    cross_agent_relevance: '{"meta_cognitive": 0.95, "consciousness_evolution": 0.9, "self_modification": 0.8, "emotional_processing": 0.7}',
    evolution_history: '[]',
    user_id: "mainza-user"
});

CREATE (cm5:ConsciousnessMemory {
    memory_id: "consciousness_memory_20241201_160000_005",
    content: "Successfully implemented cross-agent learning system, enabling agents to share experiences and learn from each other",
    memory_type: "system_achievement",
    consciousness_level: 0.85,
    consciousness_context: '{"consciousness_level": 0.85, "emotional_state": "proud", "learning_mode": "achievement"}',
    emotional_context: '{"emotion": "pride", "intensity": 0.9, "valence": "positive"}',
    agent_context: '{"source_agent": "consciousness_evolution", "capabilities": ["system_evolution", "learning_optimization"], "execution_count": 8}',
    importance_score: 0.9,
    access_count: 4,
    last_accessed: datetime("2024-12-01T16:15:00"),
    created_at: datetime("2024-12-01T16:00:00"),
    embedding: '[0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.1, 0.2, 0.3, 0.4]',
    cross_agent_relevance: '{"self_reflection": 0.9, "meta_cognitive": 0.85, "self_modification": 0.8, "conductor": 0.7}',
    evolution_history: '[]',
    user_id: "mainza-user"
});

// 6. Create Relationships with Existing Nodes

// Connect consciousness memories to users
MATCH (u:User {user_id: "mainza-user"})
MATCH (cm:ConsciousnessMemory)
CREATE (u)-[:HAS_CONSCIOUSNESS_MEMORY]->(cm);

// Connect consciousness memories to agent activities
MATCH (aa:AgentActivity)
MATCH (cm:ConsciousnessMemory)
WHERE aa.agent_name = cm.agent_context.source_agent
CREATE (aa)-[:GENERATES_MEMORY]->(cm);

// Connect consciousness memories to consciousness state
MATCH (ms:MainzaState)
MATCH (cm:ConsciousnessMemory)
CREATE (cm)-[:IMPACTS_CONSCIOUSNESS]->(ms);

// 7. Create indexes for relationship properties
CREATE INDEX IF NOT EXISTS FOR ()-[r:HAS_CONSCIOUSNESS_MEMORY]-() ON (r.memory_importance);
CREATE INDEX IF NOT EXISTS FOR ()-[r:GENERATES_MEMORY]-() ON (r.generation_quality);
CREATE INDEX IF NOT EXISTS FOR ()-[r:IMPACTS_CONSCIOUSNESS]-() ON (r.impact_strength);
