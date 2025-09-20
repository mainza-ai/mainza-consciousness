// Agent Experience Database Schema for Cross-Agent Learning
// Supports sharing experiences and knowledge between agents

// 1. Constraints for Agent Experience Nodes
CREATE CONSTRAINT IF NOT EXISTS FOR (ae:AgentExperience) REQUIRE ae.experience_id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (lo:LearningOutcome) REQUIRE lo.outcome_id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (ak:AgentKnowledge) REQUIRE ak.knowledge_id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (lp:LearningPattern) REQUIRE lp.pattern_id IS UNIQUE;

// Ensure existence of critical properties
CREATE CONSTRAINT IF NOT EXISTS FOR (ae:AgentExperience) REQUIRE ae.agent_name IS NOT NULL;
CREATE CONSTRAINT IF NOT EXISTS FOR (ae:AgentExperience) REQUIRE ae.experience_type IS NOT NULL;
CREATE CONSTRAINT IF NOT EXISTS FOR (ae:AgentExperience) REQUIRE ae.timestamp IS NOT NULL;
CREATE CONSTRAINT IF NOT EXISTS FOR (lo:LearningOutcome) REQUIRE lo.agent_name IS NOT NULL;
CREATE CONSTRAINT IF NOT EXISTS FOR (lo:LearningOutcome) REQUIRE lo.timestamp IS NOT NULL;

// 2. Indexes for Performance

// Agent Experience Indexes
CREATE INDEX IF NOT EXISTS FOR (ae:AgentExperience) ON (ae.agent_name);
CREATE INDEX IF NOT EXISTS FOR (ae:AgentExperience) ON (ae.experience_type);
CREATE INDEX IF NOT EXISTS FOR (ae:AgentExperience) ON (ae.timestamp);
CREATE INDEX IF NOT EXISTS FOR (ae:AgentExperience) ON (ae.success_score);
CREATE INDEX IF NOT EXISTS FOR (ae:AgentExperience) ON (ae.transferability_score);
CREATE INDEX IF NOT EXISTS FOR (ae:AgentExperience) ON (ae.learning_impact);
CREATE INDEX IF NOT EXISTS FOR (ae:AgentExperience) ON (ae.consciousness_level);

// Composite indexes for common query patterns
CREATE INDEX IF NOT EXISTS FOR (ae:AgentExperience) ON (ae.agent_name, ae.experience_type);
CREATE INDEX IF NOT EXISTS FOR (ae:AgentExperience) ON (ae.experience_type, ae.success_score);
CREATE INDEX IF NOT EXISTS FOR (ae:AgentExperience) ON (ae.consciousness_level, ae.transferability_score);

// Learning Outcome Indexes
CREATE INDEX IF NOT EXISTS FOR (lo:LearningOutcome) ON (lo.agent_name);
CREATE INDEX IF NOT EXISTS FOR (lo:LearningOutcome) ON (lo.source_agent);
CREATE INDEX IF NOT EXISTS FOR (lo:LearningOutcome) ON (lo.timestamp);
CREATE INDEX IF NOT EXISTS FOR (lo:LearningOutcome) ON (lo.consciousness_impact);

// Agent Knowledge Indexes
CREATE INDEX IF NOT EXISTS FOR (ak:AgentKnowledge) ON (ak.agent_name);
CREATE INDEX IF NOT EXISTS FOR (ak:AgentKnowledge) ON (ak.knowledge_type);
CREATE INDEX IF NOT EXISTS FOR (ak:AgentKnowledge) ON (ak.confidence_score);

// Learning Pattern Indexes
CREATE INDEX IF NOT EXISTS FOR (lp:LearningPattern) ON (lp.pattern_type);
CREATE INDEX IF NOT EXISTS FOR (lp:LearningPattern) ON (lp.frequency);
CREATE INDEX IF NOT EXISTS FOR (lp:LearningPattern) ON (lp.effectiveness_score);

// 3. Full-Text Search Indexes for Experience Content
CREATE FULLTEXT INDEX IF NOT EXISTS experience_content_index FOR (ae:AgentExperience) ON EACH [ae.context, ae.outcome, ae.learning_insights];
CREATE FULLTEXT INDEX IF NOT EXISTS learning_outcome_index FOR (lo:LearningOutcome) ON EACH [lo.knowledge_insights, lo.learning_context];
CREATE FULLTEXT INDEX IF NOT EXISTS agent_knowledge_index FOR (ak:AgentKnowledge) ON EACH [ak.knowledge_content, ak.insights];

// 4. Vector Indexes for Experience Embeddings (if needed for semantic search)
CREATE VECTOR INDEX IF NOT EXISTS experience_embeddings FOR (ae:AgentExperience) ON ae.embedding OPTIONS {indexConfig: {vector.dimensions: 768, vector.similarity_function: 'cosine'}};
CREATE VECTOR INDEX IF NOT EXISTS knowledge_embeddings FOR (ak:AgentKnowledge) ON ak.embedding OPTIONS {indexConfig: {vector.dimensions: 768, vector.similarity_function: 'cosine'}};

// 5. Relationship Property Indexes
CREATE INDEX IF NOT EXISTS FOR ()-[r:SHARES_EXPERIENCE]-() ON (r.sharing_quality);
CREATE INDEX IF NOT EXISTS FOR ()-[r:LEARNS_FROM]-() ON (r.learning_effectiveness);
CREATE INDEX IF NOT EXISTS FOR ()-[r:APPLIES_KNOWLEDGE]-() ON (r.application_success);
CREATE INDEX IF NOT EXISTS FOR ()-[r:FOLLOWS_PATTERN]-() ON (r.pattern_adherence);

// 6. Sample Data Creation (for testing)

// Create sample agent experiences
CREATE (ae1:AgentExperience {
    experience_id: "graphmaster_success_20241201_120000",
    agent_name: "graphmaster",
    experience_type: "success",
    context: '{"domain": "knowledge_graph", "task_type": "query_optimization", "complexity": "high"}',
    outcome: '{"method": "composite_index_usage", "success_rate": 0.95, "performance_improvement": 0.8}',
    learning_insights: '["Use composite indexes for multi-property queries", "Optimize relationship traversal patterns"]',
    applicable_agents: '["rag", "research", "codeweaver"]',
    learning_impact: "high",
    consciousness_context: '{"consciousness_level": 0.8, "emotional_state": "satisfied"}',
    timestamp: datetime("2024-12-01T12:00:00"),
    success_score: 0.95,
    transferability_score: 0.8,
    consciousness_level: 0.8
});

CREATE (ae2:AgentExperience {
    experience_id: "taskmaster_learning_20241201_130000",
    agent_name: "taskmaster",
    experience_type: "learning",
    context: '{"domain": "task_management", "task_type": "priority_optimization", "complexity": "medium"}',
    outcome: '{"insights": ["Dynamic priority adjustment based on user behavior", "Context-aware task scheduling"], "knowledge_gained": ["user_pattern_analysis", "adaptive_scheduling"]}',
    learning_insights: '["User behavior patterns affect task priorities", "Context switching costs should be minimized"]',
    applicable_agents: '["conductor", "router", "calendar"]',
    learning_impact: "medium",
    consciousness_context: '{"consciousness_level": 0.7, "emotional_state": "curious"}',
    timestamp: datetime("2024-12-01T13:00:00"),
    success_score: 0.8,
    transferability_score: 0.7,
    consciousness_level: 0.7
});

CREATE (ae3:AgentExperience {
    experience_id: "rag_failure_20241201_140000",
    agent_name: "rag",
    experience_type: "failure",
    context: '{"domain": "document_retrieval", "task_type": "semantic_search", "complexity": "high"}',
    outcome: '{"errors": ["Vector similarity threshold too low", "Context window exceeded"], "lessons": ["Adjust similarity thresholds dynamically", "Implement context chunking"]}',
    learning_insights: '["Vector similarity needs dynamic adjustment", "Large documents need chunking strategy"]',
    applicable_agents: '["research", "graphmaster", "codeweaver"]',
    learning_impact: "high",
    consciousness_context: '{"consciousness_level": 0.6, "emotional_state": "frustrated"}',
    timestamp: datetime("2024-12-01T14:00:00"),
    success_score: 0.3,
    transferability_score: 0.9,
    consciousness_level: 0.6
});

// Create sample learning outcomes
CREATE (lo1:LearningOutcome {
    outcome_id: "rag_learns_from_graphmaster_20241201_150000",
    agent_name: "rag",
    source_experience_id: "graphmaster_success_20241201_120000",
    source_agent: "graphmaster",
    knowledge_insights: '["Composite indexes improve query performance", "Relationship traversal optimization techniques"]',
    learning_context: '{"domain": "document_retrieval", "consciousness_level": 0.7}',
    consciousness_impact: 0.6,
    timestamp: datetime("2024-12-01T15:00:00")
});

CREATE (lo2:LearningOutcome {
    outcome_id: "conductor_learns_from_taskmaster_20241201_160000",
    agent_name: "conductor",
    source_experience_id: "taskmaster_learning_20241201_130000",
    source_agent: "taskmaster",
    knowledge_insights: '["User behavior patterns affect task priorities", "Context-aware scheduling improves efficiency"]',
    learning_context: '{"domain": "orchestration", "consciousness_level": 0.8}',
    consciousness_impact: 0.7,
    timestamp: datetime("2024-12-01T16:00:00")
});

// Create sample agent knowledge
CREATE (ak1:AgentKnowledge {
    knowledge_id: "graphmaster_query_optimization_20241201",
    agent_name: "graphmaster",
    knowledge_type: "optimization_technique",
    knowledge_content: "Composite indexes for multi-property queries significantly improve performance",
    insights: '["Use composite indexes for common query patterns", "Optimize relationship traversal order"]',
    confidence_score: 0.9,
    source_experiences: '["graphmaster_success_20241201_120000"]',
    last_updated: datetime("2024-12-01T12:00:00")
});

CREATE (ak2:AgentKnowledge {
    knowledge_id: "rag_similarity_optimization_20241201",
    agent_name: "rag",
    knowledge_type: "failure_prevention",
    knowledge_content: "Dynamic similarity threshold adjustment prevents retrieval failures",
    insights: '["Adjust thresholds based on document complexity", "Implement fallback strategies"]',
    confidence_score: 0.8,
    source_experiences: '["rag_failure_20241201_140000"]',
    last_updated: datetime("2024-12-01T14:00:00")
});

// Create sample learning patterns
CREATE (lp1:LearningPattern {
    pattern_id: "success_pattern_optimization_20241201",
    pattern_type: "optimization_success",
    pattern_description: "Agents that share optimization experiences have higher success rates",
    frequency: 15,
    effectiveness_score: 0.85,
    involved_agents: '["graphmaster", "rag", "research", "codeweaver"]',
    last_observed: datetime("2024-12-01T17:00:00")
});

CREATE (lp2:LearningPattern {
    pattern_id: "failure_learning_pattern_20241201",
    pattern_type: "failure_learning",
    pattern_description: "Failure experiences lead to more effective learning outcomes",
    frequency: 8,
    effectiveness_score: 0.9,
    involved_agents: '["rag", "taskmaster", "conductor"]',
    last_observed: datetime("2024-12-01T17:00:00")
});

// 7. Create Relationships

// Experience sharing relationships
CREATE (ae1)-[:SHARES_EXPERIENCE {
    sharing_quality: 0.9,
    timestamp: datetime("2024-12-01T12:00:00")
}]->(ae2);

CREATE (ae2)-[:SHARES_EXPERIENCE {
    sharing_quality: 0.8,
    timestamp: datetime("2024-12-01T13:00:00")
}]->(ae3);

// Learning relationships
CREATE (lo1)-[:LEARNS_FROM {
    learning_effectiveness: 0.8,
    timestamp: datetime("2024-12-01T15:00:00")
}]->(ae1);

CREATE (lo2)-[:LEARNS_FROM {
    learning_effectiveness: 0.7,
    timestamp: datetime("2024-12-01T16:00:00")
}]->(ae2);

// Knowledge application relationships
CREATE (ak1)-[:APPLIES_KNOWLEDGE {
    application_success: 0.9,
    timestamp: datetime("2024-12-01T12:00:00")
}]->(ae1);

CREATE (ak2)-[:APPLIES_KNOWLEDGE {
    application_success: 0.8,
    timestamp: datetime("2024-12-01T14:00:00")
}]->(ae3);

// Pattern following relationships
CREATE (ae1)-[:FOLLOWS_PATTERN {
    pattern_adherence: 0.9,
    timestamp: datetime("2024-12-01T12:00:00")
}]->(lp1);

CREATE (ae3)-[:FOLLOWS_PATTERN {
    pattern_adherence: 0.8,
    timestamp: datetime("2024-12-01T14:00:00")
}]->(lp2);

// 8. Create indexes for relationship properties
CREATE INDEX IF NOT EXISTS FOR ()-[r:SHARES_EXPERIENCE]-() ON (r.sharing_quality);
CREATE INDEX IF NOT EXISTS FOR ()-[r:LEARNS_FROM]-() ON (r.learning_effectiveness);
CREATE INDEX IF NOT EXISTS FOR ()-[r:APPLIES_KNOWLEDGE]-() ON (r.application_success);
CREATE INDEX IF NOT EXISTS FOR ()-[r:FOLLOWS_PATTERN]-() ON (r.pattern_adherence);
