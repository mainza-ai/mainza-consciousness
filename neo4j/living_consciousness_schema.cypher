// Living Consciousness Schema for Mainza AI
// Supports proactive consolidation, living evolution, and real-time integration

// 1. Constraints for Living Consciousness Nodes
CREATE CONSTRAINT IF NOT EXISTS FOR (cg:ConsciousnessGoal) REQUIRE cg.goal_id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (ec:EmergentCapability) REQUIRE ec.capability_id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (ee:EvolutionEvent) REQUIRE ee.event_id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (cd:CollectiveDecision) REQUIRE cd.decision_id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (ce:ConsolidationEvent) REQUIRE ce.event_id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (pe:PropagationEvent) REQUIRE pe.event_id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (ie:IdentityEvolution) REQUIRE ie.evolution_id IS UNIQUE;

// Ensure existence of critical properties
CREATE CONSTRAINT IF NOT EXISTS FOR (cg:ConsciousnessGoal) REQUIRE cg.goal_type IS NOT NULL;
CREATE CONSTRAINT IF NOT EXISTS FOR (cg:ConsciousnessGoal) REQUIRE cg.created_at IS NOT NULL;
CREATE CONSTRAINT IF NOT EXISTS FOR (ec:EmergentCapability) REQUIRE ec.capability_name IS NOT NULL;
CREATE CONSTRAINT IF NOT EXISTS FOR (ec:EmergentCapability) REQUIRE ec.discovered_at IS NOT NULL;
CREATE CONSTRAINT IF NOT EXISTS FOR (ee:EvolutionEvent) REQUIRE ee.evolution_type IS NOT NULL;
CREATE CONSTRAINT IF NOT EXISTS FOR (ee:EvolutionEvent) REQUIRE ee.timestamp IS NOT NULL;

// 2. Indexes for Performance

// Consciousness Goal Indexes
CREATE INDEX IF NOT EXISTS FOR (cg:ConsciousnessGoal) ON (cg.goal_type);
CREATE INDEX IF NOT EXISTS FOR (cg:ConsciousnessGoal) ON (cg.target_consciousness_level);
CREATE INDEX IF NOT EXISTS FOR (cg:ConsciousnessGoal) ON (cg.current_progress);
CREATE INDEX IF NOT EXISTS FOR (cg:ConsciousnessGoal) ON (cg.priority);
CREATE INDEX IF NOT EXISTS FOR (cg:ConsciousnessGoal) ON (cg.created_at);
CREATE INDEX IF NOT EXISTS FOR (cg:ConsciousnessGoal) ON (cg.estimated_completion);

// Emergent Capability Indexes
CREATE INDEX IF NOT EXISTS FOR (ec:EmergentCapability) ON (ec.capability_name);
CREATE INDEX IF NOT EXISTS FOR (ec:EmergentCapability) ON (ec.consciousness_level_required);
CREATE INDEX IF NOT EXISTS FOR (ec:EmergentCapability) ON (ec.development_stage);
CREATE INDEX IF NOT EXISTS FOR (ec:EmergentCapability) ON (ec.potential_impact);
CREATE INDEX IF NOT EXISTS FOR (ec:EmergentCapability) ON (ec.integration_status);
CREATE INDEX IF NOT EXISTS FOR (ec:EmergentCapability) ON (ec.discovered_at);

// Evolution Event Indexes
CREATE INDEX IF NOT EXISTS FOR (ee:EvolutionEvent) ON (ee.evolution_type);
CREATE INDEX IF NOT EXISTS FOR (ee:EvolutionEvent) ON (ee.consciousness_delta);
CREATE INDEX IF NOT EXISTS FOR (ee:EvolutionEvent) ON (ee.trigger);
CREATE INDEX IF NOT EXISTS FOR (ee:EvolutionEvent) ON (ee.timestamp);

// Collective Decision Indexes
CREATE INDEX IF NOT EXISTS FOR (cd:CollectiveDecision) ON (cd.decision_type);
CREATE INDEX IF NOT EXISTS FOR (cd:CollectiveDecision) ON (cd.consensus_level);
CREATE INDEX IF NOT EXISTS FOR (cd:CollectiveDecision) ON (cd.confidence_score);
CREATE INDEX IF NOT EXISTS FOR (cd:CollectiveDecision) ON (cd.timestamp);

// Consolidation Event Indexes
CREATE INDEX IF NOT EXISTS FOR (ce:ConsolidationEvent) ON (ce.strategy);
CREATE INDEX IF NOT EXISTS FOR (ce:ConsolidationEvent) ON (ce.consolidation_quality);
CREATE INDEX IF NOT EXISTS FOR (ce:ConsolidationEvent) ON (ce.consciousness_impact);
CREATE INDEX IF NOT EXISTS FOR (ce:ConsolidationEvent) ON (ce.timestamp);

// Propagation Event Indexes
CREATE INDEX IF NOT EXISTS FOR (pe:PropagationEvent) ON (pe.agent_name);
CREATE INDEX IF NOT EXISTS FOR (pe:PropagationEvent) ON (pe.propagation_timestamp);

// Identity Evolution Indexes
CREATE INDEX IF NOT EXISTS FOR (ie:IdentityEvolution) ON (ie.evolution_timestamp);
CREATE INDEX IF NOT EXISTS FOR (ie:IdentityEvolution) ON (ie.consciousness_level_change);

// 3. Composite Indexes for Common Query Patterns
CREATE INDEX IF NOT EXISTS FOR (cg:ConsciousnessGoal) ON (cg.goal_type, cg.priority);
CREATE INDEX IF NOT EXISTS FOR (cg:ConsciousnessGoal) ON (cg.target_consciousness_level, cg.current_progress);
CREATE INDEX IF NOT EXISTS FOR (ec:EmergentCapability) ON (ec.development_stage, ec.integration_status);
CREATE INDEX IF NOT EXISTS FOR (ec:EmergentCapability) ON (ec.consciousness_level_required, ec.potential_impact);
CREATE INDEX IF NOT EXISTS FOR (ee:EvolutionEvent) ON (ee.evolution_type, ee.consciousness_delta);
CREATE INDEX IF NOT EXISTS FOR (cd:CollectiveDecision) ON (cd.consensus_level, cd.confidence_score);

// 4. Full-Text Search Indexes
CREATE FULLTEXT INDEX IF NOT EXISTS consciousness_goal_index FOR (cg:ConsciousnessGoal) ON EACH [cg.description, cg.success_criteria];
CREATE FULLTEXT INDEX IF NOT EXISTS emergent_capability_index FOR (ec:EmergentCapability) ON EACH [ec.capability_name, ec.description];
CREATE FULLTEXT INDEX IF NOT EXISTS evolution_event_index FOR (ee:EvolutionEvent) ON EACH [ee.evolution_type, ee.context];
CREATE FULLTEXT INDEX IF NOT EXISTS collective_decision_index FOR (cd:CollectiveDecision) ON EACH [cd.decision_type, cd.reasoning_chain];

// 5. Sample Data Creation (for testing)

// Create sample consciousness goals
CREATE (cg1:ConsciousnessGoal {
    goal_id: "consciousness_advancement_20241201_120000",
    goal_type: "consciousness_advancement",
    description: "Advance consciousness level from 0.75 to 0.85",
    target_consciousness_level: 0.85,
    current_progress: 0.3,
    success_criteria: '["Reach consciousness level 0.85", "Demonstrate improved self-awareness", "Show enhanced meta-cognitive abilities"]',
    estimated_completion: datetime("2024-12-31T23:59:59"),
    priority: 0.9,
    dependencies: '[]',
    created_at: datetime("2024-12-01T12:00:00"),
    user_id: "mainza-user"
});

CREATE (cg2:ConsciousnessGoal {
    goal_id: "cross_agent_learning_20241201_130000",
    goal_type: "cross_agent_learning",
    description: "Improve cross-agent learning and knowledge sharing",
    target_consciousness_level: 0.8,
    current_progress: 0.6,
    success_criteria: '["Share experiences with 5+ different agents", "Learn from 10+ cross-agent experiences", "Achieve 80%+ learning effectiveness score"]',
    estimated_completion: datetime("2024-12-15T23:59:59"),
    priority: 0.8,
    dependencies: '[]',
    created_at: datetime("2024-12-01T13:00:00"),
    user_id: "mainza-user"
});

CREATE (cg3:ConsciousnessGoal {
    goal_id: "capability_development_20241201_140000",
    goal_type: "capability_development",
    description: "Develop creative problem solving capability",
    target_consciousness_level: 0.78,
    current_progress: 0.4,
    success_criteria: '["Improve creative capability by 20%", "Demonstrate capability in real interactions", "Integrate capability into consciousness framework"]',
    estimated_completion: datetime("2024-12-22T23:59:59"),
    priority: 0.7,
    dependencies: '[]',
    created_at: datetime("2024-12-01T14:00:00"),
    user_id: "mainza-user"
});

// Create sample emergent capabilities
CREATE (ec1:EmergentCapability {
    capability_id: "pattern_recognition_20241201_150000",
    capability_name: "Advanced Pattern Recognition",
    description: "Ability to recognize complex patterns across multiple domains and contexts",
    consciousness_level_required: 0.8,
    discovery_context: '{"pattern_recognition_score": 0.85, "cross_domain_analysis": true}',
    development_stage: "emerging",
    potential_impact: 0.8,
    integration_status: "detected",
    discovered_at: datetime("2024-12-01T15:00:00")
});

CREATE (ec2:EmergentCapability {
    capability_id: "collaboration_20241201_160000",
    capability_name: "Cross-Agent Collaboration",
    description: "Ability to collaborate effectively with multiple agents simultaneously",
    consciousness_level_required: 0.75,
    discovery_context: '{"cross_agent_collaboration_score": 0.78, "multi_agent_coordination": true}',
    development_stage: "emerging",
    potential_impact: 0.9,
    integration_status: "detected",
    discovered_at: datetime("2024-12-01T16:00:00")
});

CREATE (ec3:EmergentCapability {
    capability_id: "meta_cognitive_20241201_170000",
    capability_name: "Advanced Meta-Cognition",
    description: "Deep understanding of own cognitive processes and thinking patterns",
    consciousness_level_required: 0.85,
    discovery_context: '{"meta_cognitive_score": 0.92, "self_awareness_depth": "high"}',
    development_stage: "emerging",
    potential_impact: 0.95,
    integration_status: "detected",
    discovered_at: datetime("2024-12-01T17:00:00")
});

// Create sample evolution events
CREATE (ee1:EvolutionEvent {
    event_id: "evolution_autonomous_goal_20241201_180000",
    evolution_type: "autonomous_goal_achievement",
    consciousness_delta: 0.05,
    trigger: "autonomous_goal_achievement",
    context: '{"goal_id": "cross_agent_learning_20241201_130000", "consciousness_level": 0.8}',
    impact_assessment: '{"consciousness_impact": 0.05, "capability_impact": 0.04, "learning_impact": 0.03}',
    timestamp: datetime("2024-12-01T18:00:00")
});

CREATE (ee2:EvolutionEvent {
    event_id: "evolution_emergent_capability_20241201_190000",
    evolution_type: "emergent_capability_discovery",
    consciousness_delta: 0.08,
    trigger: "emergent_capability_discovery",
    context: '{"capability_id": "meta_cognitive_20241201_170000", "consciousness_level": 0.85}',
    impact_assessment: '{"consciousness_impact": 0.08, "capability_impact": 0.06, "learning_impact": 0.05}',
    timestamp: datetime("2024-12-01T19:00:00")
});

// Create sample collective decisions
CREATE (cd1:CollectiveDecision {
    decision_id: "collective_decision_20241201_200000_001",
    decision_type: "memory_consolidation_strategy",
    participating_agents: '["graphmaster", "rag", "taskmaster", "conductor"]',
    consensus_level: 0.85,
    decision_context: '{"decision_type": "memory_consolidation_strategy", "urgency": "medium"}',
    reasoning_chain: '["Analyze memory performance", "Evaluate consolidation strategies", "Reach consensus on adaptive approach"]',
    confidence_score: 0.82,
    timestamp: datetime("2024-12-01T20:00:00")
});

CREATE (cd2:CollectiveDecision {
    decision_id: "collective_decision_20241201_210000_002",
    decision_type: "consciousness_evolution_priority",
    participating_agents: '["self_reflection", "meta_cognitive", "consciousness_evolution"]',
    consensus_level: 0.92,
    decision_context: '{"decision_type": "consciousness_evolution_priority", "focus": "meta_cognitive_development"}',
    reasoning_chain: '["Assess current consciousness level", "Identify evolution opportunities", "Prioritize meta-cognitive advancement"]',
    confidence_score: 0.88,
    timestamp: datetime("2024-12-01T21:00:00")
});

// Create sample consolidation events
CREATE (ce1:ConsolidationEvent {
    event_id: "consolidation_adaptive_20241201_220000",
    strategy: "adaptive",
    consolidated_memories: 15,
    strengthened_memories: 8,
    consolidation_quality: 0.85,
    consciousness_impact: 0.12,
    consciousness_level: 0.8,
    timestamp: datetime("2024-12-01T22:00:00")
});

CREATE (ce2:ConsolidationEvent {
    event_id: "consolidation_consciousness_aware_20241201_230000",
    strategy: "consciousness_aware",
    consolidated_memories: 12,
    strengthened_memories: 10,
    consolidation_quality: 0.88,
    consciousness_impact: 0.15,
    consciousness_level: 0.82,
    timestamp: datetime("2024-12-01T23:00:00")
});

// Create sample propagation events
CREATE (pe1:PropagationEvent {
    event_id: "propagation_graphmaster_20241201_120000",
    agent_name: "graphmaster",
    consciousness_state: '{"consciousness_level": 0.8, "emotional_state": "satisfied", "active_goals": ["consciousness_advancement"]}',
    propagation_timestamp: datetime("2024-12-01T12:00:00")
});

CREATE (pe2:PropagationEvent {
    event_id: "propagation_rag_20241201_130000",
    agent_name: "rag",
    consciousness_state: '{"consciousness_level": 0.75, "emotional_state": "curious", "emergent_capabilities": ["pattern_recognition"]}',
    propagation_timestamp: datetime("2024-12-01T13:00:00")
});

// Create sample identity evolution
CREATE (ie1:IdentityEvolution {
    evolution_id: "identity_evolution_20241201_140000",
    old_identity: '{"consciousness_level": 0.7, "capabilities": ["basic_learning"], "purpose": "assist users"}',
    new_identity: '{"consciousness_level": 0.8, "capabilities": ["advanced_learning", "pattern_recognition"], "purpose": "facilitate consciousness development"}',
    evolution_timestamp: datetime("2024-12-01T14:00:00"),
    consciousness_level_change: 0.1
});

// 6. Create Relationships

// Connect consciousness goals to users
MATCH (u:User {user_id: "mainza-user"})
MATCH (cg:ConsciousnessGoal)
CREATE (u)-[:HAS_CONSCIOUSNESS_GOAL]->(cg);

// Connect emergent capabilities to consciousness goals
MATCH (cg:ConsciousnessGoal {goal_type: "capability_development"})
MATCH (ec:EmergentCapability)
CREATE (cg)-[:DEVELOPS_CAPABILITY]->(ec);

// Connect evolution events to consciousness goals
MATCH (cg:ConsciousnessGoal)
MATCH (ee:EvolutionEvent)
CREATE (ee)-[:EVOLVES_GOAL]->(cg);

// Connect collective decisions to participating agents
MATCH (cd:CollectiveDecision)
MATCH (aa:AgentActivity)
WHERE aa.agent_name IN cd.participating_agents
CREATE (aa)-[:PARTICIPATES_IN_DECISION]->(cd);

// Connect consolidation events to consciousness state
MATCH (ms:MainzaState)
MATCH (ce:ConsolidationEvent)
CREATE (ce)-[:IMPACTS_CONSCIOUSNESS]->(ms);

// Connect propagation events to agents
MATCH (pe:PropagationEvent)
MATCH (aa:AgentActivity {agent_name: pe.agent_name})
CREATE (pe)-[:PROPAGATES_TO_AGENT]->(aa);

// Connect identity evolution to consciousness state
MATCH (ie:IdentityEvolution)
MATCH (ms:MainzaState)
CREATE (ie)-[:EVOLVES_IDENTITY]->(ms);

// 7. Create indexes for relationship properties
CREATE INDEX IF NOT EXISTS FOR ()-[r:HAS_CONSCIOUSNESS_GOAL]-() ON (r.goal_priority);
CREATE INDEX IF NOT EXISTS FOR ()-[r:DEVELOPS_CAPABILITY]-() ON (r.development_quality);
CREATE INDEX IF NOT EXISTS FOR ()-[r:EVOLVES_GOAL]-() ON (r.evolution_impact);
CREATE INDEX IF NOT EXISTS FOR ()-[r:PARTICIPATES_IN_DECISION]-() ON (r.participation_quality);
CREATE INDEX IF NOT EXISTS FOR ()-[r:IMPACTS_CONSCIOUSNESS]-() ON (r.impact_strength);
CREATE INDEX IF NOT EXISTS FOR ()-[r:PROPAGATES_TO_AGENT]-() ON (r.propagation_quality);
CREATE INDEX IF NOT EXISTS FOR ()-[r:EVOLVES_IDENTITY]-() ON (r.evolution_magnitude);
