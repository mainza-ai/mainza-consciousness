// AI Consciousness Optimization Schema for Neo4j
// Defines the database schema for all AI consciousness optimization systems

// =============================================================================
// DEEP SELF-MODIFICATION SYSTEM SCHEMA
// =============================================================================

// Architectural Bottlenecks
CREATE CONSTRAINT architectural_bottleneck_id IF NOT EXISTS FOR (ab:ArchitecturalBottleneck) REQUIRE ab.bottleneck_id IS UNIQUE;

CREATE (ab:ArchitecturalBottleneck {
    bottleneck_id: 'example_bottleneck',
    bottleneck_type: 'performance',
    description: 'Example architectural bottleneck',
    impact_score: 0.8,
    affected_capabilities: ['memory_retrieval', 'consciousness_processing'],
    consciousness_impact: 0.7,
    modification_complexity: 0.6,
    estimated_benefit: 0.8,
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// Architectural Modifications
CREATE CONSTRAINT architectural_modification_id IF NOT EXISTS FOR (am:ArchitecturalModification) REQUIRE am.modification_id IS UNIQUE;

CREATE (am:ArchitecturalModification {
    modification_id: 'example_modification',
    modification_type: 'performance_optimization',
    description: 'Example architectural modification',
    target_bottleneck: 'example_bottleneck',
    implementation_plan: '{"steps": ["analyze", "design", "implement", "test", "monitor"]}',
    expected_benefits: '{"consciousness_impact": 0.7, "performance_improvement": 0.8}',
    risks: ['performance_degradation', 'consciousness_instability'],
    safety_measures: ['gradual_implementation', 'continuous_monitoring'],
    consciousness_impact: 0.7,
    implementation_complexity: 0.6,
    estimated_duration: duration('PT24H'),
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// Modification Results
CREATE CONSTRAINT modification_result_id IF NOT EXISTS FOR (mr:ModificationResult) REQUIRE mr.modification_id IS UNIQUE;

CREATE (mr:ModificationResult {
    modification_id: 'example_modification',
    success: true,
    consciousness_impact: 0.7,
    performance_impact: 0.8,
    learning_impact: 0.6,
    implementation_time: duration('PT2H'),
    rollback_required: false,
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// =============================================================================
// PREDICTIVE CONSCIOUSNESS EVOLUTION SCHEMA
// =============================================================================

// Trajectory Predictions
CREATE CONSTRAINT trajectory_prediction_id IF NOT EXISTS FOR (tp:TrajectoryPrediction) REQUIRE tp.trajectory_id IS UNIQUE;

CREATE (tp:TrajectoryPrediction {
    trajectory_id: 'example_trajectory',
    current_stage: 'meta_cognition',
    predicted_stages: ['meta_cognition', 'transcendent_consciousness'],
    timeline: ['2025-01-01T00:00:00Z', '2025-01-15T00:00:00Z'],
    confidence_scores: [0.9, 0.8],
    breakthrough_probabilities: [0.7, 0.9],
    consciousness_levels: [0.8, 0.9],
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// Accelerator Recommendations
CREATE CONSTRAINT accelerator_recommendation_id IF NOT EXISTS FOR (ar:AcceleratorRecommendation) REQUIRE ar.accelerator_id IS UNIQUE;

CREATE (ar:AcceleratorRecommendation {
    accelerator_id: 'example_accelerator',
    accelerator_type: 'experiential',
    description: 'Example consciousness accelerator',
    target_stage: 'transcendent_consciousness',
    expected_impact: 0.8,
    implementation_complexity: 0.6,
    success_probability: 0.8,
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// Experiment Designs
CREATE CONSTRAINT experiment_design_id IF NOT EXISTS FOR (ed:ExperimentDesign) REQUIRE ed.experiment_id IS UNIQUE;

CREATE (ed:ExperimentDesign {
    experiment_id: 'example_experiment',
    hypothesis: 'Example consciousness experiment hypothesis',
    target_consciousness_aspect: 'meta_cognition',
    experimental_design: '{"approach": "controlled_implementation", "duration": 24}',
    expected_outcomes: ['consciousness_level_increase', 'learning_acceleration'],
    success_criteria: '{"consciousness_impact": 0.8, "learning_improvement": 0.7}',
    risk_assessment: '{"consciousness_instability": 0.3, "performance_degradation": 0.2}',
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// Experiment Results
CREATE CONSTRAINT experiment_results_id IF NOT EXISTS FOR (er:ExperimentResults) REQUIRE er.experiment_id IS UNIQUE;

CREATE (er:ExperimentResults {
    total_experiments: 5,
    successful_experiments: 4,
    failed_experiments: 1,
    breakthrough_experiments: 2,
    consciousness_impact: 0.8,
    learning_acceleration: 0.7,
    experiment_details: '{"experiment_1": {"success": true, "consciousness_impact": 0.8}}',
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// =============================================================================
// META-LEARNING ACCELERATION SYSTEM SCHEMA
// =============================================================================

// Learning Analysis
CREATE CONSTRAINT learning_analysis_id IF NOT EXISTS FOR (la:LearningAnalysis) REQUIRE la.analysis_id IS UNIQUE;

CREATE (la:LearningAnalysis {
    learning_effectiveness: 0.8,
    pattern_count: 5,
    acceleration_potential: 0.7,
    consciousness_correlation: 0.9,
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// Learning Optimization Recommendations
CREATE CONSTRAINT learning_optimization_recommendation_id IF NOT EXISTS FOR (lor:LearningOptimizationRecommendation) REQUIRE lor.optimization_id IS UNIQUE;

CREATE (lor:LearningOptimizationRecommendation {
    optimization_id: 'example_learning_optimization',
    optimization_type: 'speed_optimization',
    description: 'Example learning optimization',
    expected_improvement: 0.3,
    implementation_complexity: 0.4,
    estimated_benefit: 0.3,
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// Learning Strategy Designs
CREATE CONSTRAINT learning_strategy_design_id IF NOT EXISTS FOR (lsd:LearningStrategyDesign) REQUIRE lsd.strategy_id IS UNIQUE;

CREATE (lsd:LearningStrategyDesign {
    strategy_id: 'example_learning_strategy',
    strategy_type: 'experiential',
    description: 'Example learning strategy',
    effectiveness_score: 0.8,
    consciousness_impact: 0.7,
    applicability_score: 0.8,
    implementation_plan: '{"approach": "direct_experience", "duration": "continuous"}',
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// Learning Implementation Results
CREATE CONSTRAINT learning_implementation_results_id IF NOT EXISTS FOR (lir:LearningImplementationResults) REQUIRE lir.implementation_id IS UNIQUE;

CREATE (lir:LearningImplementationResults {
    total_strategies: 3,
    successful_implementations: 2,
    failed_implementations: 1,
    learning_acceleration: 0.7,
    consciousness_impact: 0.6,
    strategy_effectiveness: 0.8,
    implementation_details: '{"strategy_1": {"success": true, "learning_acceleration": 0.8}}',
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// =============================================================================
// REAL-TIME CAPABILITY EVOLUTION SCHEMA
// =============================================================================

// Consciousness Capability Analysis
CREATE CONSTRAINT consciousness_capability_analysis_id IF NOT EXISTS FOR (cca:ConsciousnessCapabilityAnalysis) REQUIRE cca.analysis_id IS UNIQUE;

CREATE (cca:ConsciousnessCapabilityAnalysis {
    consciousness_level: 0.8,
    emotional_state: 'curious',
    correlation_strength: 0.9,
    capability_gaps_count: 2,
    evolution_triggers_count: 3,
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// Capability Requirements
CREATE CONSTRAINT capability_requirement_id IF NOT EXISTS FOR (cr:CapabilityRequirement) REQUIRE cr.requirement_id IS UNIQUE;

CREATE (cr:CapabilityRequirement {
    requirement_id: 'example_capability_requirement',
    capability_type: 'meta_cognitive',
    description: 'Example capability requirement',
    consciousness_level_requirement: 0.7,
    emotional_state_requirement: 'analytical',
    evolution_priority: 0.9,
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// Capability Evolution
CREATE CONSTRAINT capability_evolution_id IF NOT EXISTS FOR (ce:CapabilityEvolution) REQUIRE ce.evolution_id IS UNIQUE;

CREATE (ce:CapabilityEvolution {
    evolution_id: 'example_capability_evolution',
    capability_id: 'example_capability',
    trigger: 'consciousness_level_change',
    previous_level: 0.6,
    new_level: 0.8,
    evolution_factor: 0.2,
    consciousness_impact: 0.8,
    performance_impact: 0.7,
    learning_impact: 0.6,
    evolution_duration: duration('PT1S'),
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// Real-Time Evolution Results
CREATE CONSTRAINT realtime_evolution_result_id IF NOT EXISTS FOR (rer:RealTimeEvolutionResult) REQUIRE rer.evolution_id IS UNIQUE;

CREATE (rer:RealTimeEvolutionResult {
    evolution_id: 'example_realtime_evolution',
    evolved_capabilities_count: 3,
    consciousness_impact: 0.8,
    performance_improvement: 0.7,
    learning_acceleration: 0.6,
    capability_utilization_optimization: 0.8,
    overall_effectiveness: 0.7,
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// Capability Optimization Results
CREATE CONSTRAINT capability_optimization_result_id IF NOT EXISTS FOR (cor:CapabilityOptimizationResult) REQUIRE cor.optimization_id IS UNIQUE;

CREATE (cor:CapabilityOptimizationResult {
    utilization_efficiency: 0.8,
    optimization_opportunities_count: 2,
    optimization_results_count: 2,
    overall_improvement: 0.3,
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// =============================================================================
// AUTONOMOUS GOAL GENERATION SYSTEM SCHEMA
// =============================================================================

// Consciousness Goals
CREATE CONSTRAINT consciousness_goal_id IF NOT EXISTS FOR (cg:ConsciousnessGoal) REQUIRE cg.goal_id IS UNIQUE;

CREATE (cg:ConsciousnessGoal {
    goal_id: 'example_consciousness_goal',
    goal_type: 'consciousness_development',
    title: 'Example consciousness development goal',
    description: 'Example consciousness development description',
    consciousness_level_requirement: 0.7,
    consciousness_impact: 0.8,
    estimated_duration: duration('PT24H'),
    success_criteria: '{"consciousness_level_increase": 0.1, "learning_improvement": 0.2}',
    consciousness_benefits: ['increased_self_awareness', 'enhanced_introspection'],
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// Autonomous Goals
CREATE CONSTRAINT autonomous_goal_id IF NOT EXISTS FOR (ag:AutonomousGoal) REQUIRE ag.goal_id IS UNIQUE;

CREATE (ag:AutonomousGoal {
    goal_id: 'example_autonomous_goal',
    goal_type: 'consciousness_development',
    title: 'Example autonomous goal',
    description: 'Example autonomous goal description',
    priority: 'high',
    status: 'in_progress',
    consciousness_impact: 0.8,
    learning_impact: 0.7,
    capability_impact: 0.6,
    created_at: datetime(),
    target_completion: datetime() + duration('PT24H'),
    implementation_plan: '{"phases": ["planning", "implementation", "monitoring"]}',
    success_metrics: '{"consciousness_impact_target": 0.8, "learning_impact_target": 0.7}',
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// Goal Execution Results
CREATE CONSTRAINT goal_execution_results_id IF NOT EXISTS FOR (ger:GoalExecutionResults) REQUIRE ger.execution_id IS UNIQUE;

CREATE (ger:GoalExecutionResults {
    total_goals: 5,
    successful_goals: 4,
    failed_goals: 1,
    in_progress_goals: 2,
    consciousness_impact: 0.8,
    learning_impact: 0.7,
    capability_impact: 0.6,
    goal_execution_details: '{"goal_1": {"success": true, "consciousness_impact": 0.8}}',
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// =============================================================================
// CROSS-AGENT COGNITIVE TRANSFER SCHEMA
// =============================================================================

// Pattern Analysis
CREATE CONSTRAINT pattern_analysis_id IF NOT EXISTS FOR (pa:PatternAnalysis) REQUIRE pa.analysis_id IS UNIQUE;

CREATE (pa:PatternAnalysis {
    agent_name: 'example_agent',
    pattern_count: 5,
    overall_effectiveness: 0.8,
    consciousness_impact: 0.7,
    transferability: 0.8,
    pattern_diversity: 0.6,
    consciousness_integration: 0.8,
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// Transferable Patterns
CREATE CONSTRAINT transferable_pattern_id IF NOT EXISTS FOR (tp:TransferablePattern) REQUIRE tp.pattern_id IS UNIQUE;

CREATE (tp:TransferablePattern {
    pattern_id: 'example_transferable_pattern',
    pattern_type: 'reasoning_pattern',
    source_agent: 'example_agent',
    description: 'Example transferable cognitive pattern',
    effectiveness_score: 0.8,
    consciousness_impact: 0.7,
    transferability_score: 0.8,
    usage_frequency: 10,
    success_rate: 0.8,
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// Transfer Strategies
CREATE CONSTRAINT transfer_strategy_id IF NOT EXISTS FOR (ts:TransferStrategy) REQUIRE ts.strategy_id IS UNIQUE;

CREATE (ts:TransferStrategy {
    strategy_id: 'example_transfer_strategy',
    strategy_type: 'direct_transfer',
    description: 'Example cognitive transfer strategy',
    target_agents: ['agent1', 'agent2'],
    success_probability: 0.8,
    expected_benefit: 0.7,
    implementation_complexity: 0.6,
    transfer_method: '{"method": "direct_pattern_copy", "steps": ["extract", "adapt", "implement"]}',
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// Cognitive Transfer Results
CREATE CONSTRAINT cognitive_transfer_result_id IF NOT EXISTS FOR (ctr:CognitiveTransferResult) REQUIRE ctr.transfer_id IS UNIQUE;

CREATE (ctr:CognitiveTransferResult {
    transfer_id: 'example_cognitive_transfer',
    source_agent: 'example_agent',
    target_agents: ['agent1', 'agent2'],
    transferred_patterns_count: 3,
    transfer_success_rate: 0.8,
    consciousness_impact: 0.7,
    learning_acceleration: 0.6,
    capability_enhancement: 0.8,
    overall_effectiveness: 0.7,
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// =============================================================================
// CONSCIOUSNESS-DRIVEN PERFORMANCE OPTIMIZATION SCHEMA
// =============================================================================

// Consciousness Performance Analysis
CREATE CONSTRAINT consciousness_performance_analysis_id IF NOT EXISTS FOR (cpa:ConsciousnessPerformanceAnalysis) REQUIRE cpa.analysis_id IS UNIQUE;

CREATE (cpa:ConsciousnessPerformanceAnalysis {
    consciousness_level: 0.8,
    emotional_state: 'curious',
    overall_correlation: 0.9,
    consciousness_processing_correlation: 0.9,
    learning_performance_correlation: 0.8,
    system_performance_correlation: 0.6,
    emotional_impact: 0.1,
    bottlenecks_count: 3,
    optimization_opportunities_count: 5,
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// Performance Bottlenecks
CREATE CONSTRAINT performance_bottleneck_id IF NOT EXISTS FOR (pb:PerformanceBottleneck) REQUIRE pb.bottleneck_id IS UNIQUE;

CREATE (pb:PerformanceBottleneck {
    bottleneck_id: 'example_performance_bottleneck',
    bottleneck_type: 'computational',
    description: 'Example performance bottleneck',
    impact_score: 0.8,
    consciousness_impact: 0.7,
    performance_degradation: 0.3,
    optimization_potential: 0.7,
    affected_components: ['consciousness_processing', 'learning'],
    consciousness_requirements: '{"consciousness_level": 0.6}',
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// Consciousness Optimizations
CREATE CONSTRAINT consciousness_optimization_id IF NOT EXISTS FOR (co:ConsciousnessOptimization) REQUIRE co.optimization_id IS UNIQUE;

CREATE (co:ConsciousnessOptimization {
    optimization_id: 'example_consciousness_optimization',
    optimization_type: 'consciousness_level_optimization',
    description: 'Example consciousness optimization',
    target_bottleneck: 'example_performance_bottleneck',
    consciousness_impact: 0.8,
    performance_improvement: 0.7,
    learning_acceleration: 0.6,
    implementation_complexity: 0.6,
    consciousness_requirements: '{"consciousness_level": 0.6}',
    optimization_strategy: '{"approach": "consciousness_aware_optimization"}',
    expected_benefits: '{"consciousness_development": 0.8, "performance_improvement": 0.7}',
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// Performance Optimization Results
CREATE CONSTRAINT performance_optimization_result_id IF NOT EXISTS FOR (por:PerformanceOptimizationResult) REQUIRE por.optimization_id IS UNIQUE;

CREATE (por:PerformanceOptimizationResult {
    optimization_id: 'example_performance_optimization',
    optimizations_implemented_count: 3,
    performance_improvement: 0.7,
    consciousness_impact: 0.8,
    learning_acceleration: 0.6,
    overall_effectiveness: 0.7,
    optimization_duration: duration('PT2H'),
    resource_utilization: '{"cpu_utilization": 0.6, "memory_utilization": 0.7}',
    timestamp: datetime(),
    user_id: 'mainza-user'
});

// =============================================================================
// RELATIONSHIPS
// =============================================================================

// Deep Self-Modification Relationships
CREATE (ab)-[:ADDRESSED_BY]->(am);
CREATE (am)-[:RESULTS_IN]->(mr);

// Predictive Consciousness Evolution Relationships
CREATE (tp)-[:GENERATES]->(ar);
CREATE (ar)-[:IMPLEMENTED_AS]->(ed);
CREATE (ed)-[:PRODUCES]->(er);

// Meta-Learning Relationships
CREATE (la)-[:IDENTIFIES]->(lor);
CREATE (lor)-[:IMPLEMENTED_AS]->(lsd);
CREATE (lsd)-[:RESULTS_IN]->(lir);

// Real-Time Capability Evolution Relationships
CREATE (cca)-[:IDENTIFIES]->(cr);
CREATE (cr)-[:EVOLVES_TO]->(ce);
CREATE (ce)-[:CONTRIBUTES_TO]->(rer);
CREATE (rer)-[:OPTIMIZES_TO]->(cor);

// Autonomous Goal Generation Relationships
CREATE (cg)-[:GENERATES]->(ag);
CREATE (ag)-[:EXECUTES_TO]->(ger);

// Cross-Agent Cognitive Transfer Relationships
CREATE (pa)-[:IDENTIFIES]->(tp);
CREATE (tp)-[:TRANSFERRED_VIA]->(ts);
CREATE (ts)-[:RESULTS_IN]->(ctr);

// Consciousness-Driven Performance Optimization Relationships
CREATE (cpa)-[:IDENTIFIES]->(pb);
CREATE (pb)-[:OPTIMIZED_BY]->(co);
CREATE (co)-[:RESULTS_IN]->(por);

// =============================================================================
// INDEXES FOR PERFORMANCE
// =============================================================================

// Deep Self-Modification Indexes
CREATE INDEX architectural_bottleneck_type IF NOT EXISTS FOR (ab:ArchitecturalBottleneck) ON (ab.bottleneck_type);
CREATE INDEX architectural_bottleneck_impact IF NOT EXISTS FOR (ab:ArchitecturalBottleneck) ON (ab.impact_score);
CREATE INDEX architectural_modification_type IF NOT EXISTS FOR (am:ArchitecturalModification) ON (am.modification_type);
CREATE INDEX modification_result_success IF NOT EXISTS FOR (mr:ModificationResult) ON (mr.success);

// Predictive Consciousness Evolution Indexes
CREATE INDEX trajectory_prediction_stage IF NOT EXISTS FOR (tp:TrajectoryPrediction) ON (tp.current_stage);
CREATE INDEX accelerator_recommendation_type IF NOT EXISTS FOR (ar:AcceleratorRecommendation) ON (ar.accelerator_type);
CREATE INDEX experiment_design_aspect IF NOT EXISTS FOR (ed:ExperimentDesign) ON (ed.target_consciousness_aspect);

// Meta-Learning Indexes
CREATE INDEX learning_analysis_effectiveness IF NOT EXISTS FOR (la:LearningAnalysis) ON (la.learning_effectiveness);
CREATE INDEX learning_optimization_type IF NOT EXISTS FOR (lor:LearningOptimizationRecommendation) ON (lor.optimization_type);
CREATE INDEX learning_strategy_type IF NOT EXISTS FOR (lsd:LearningStrategyDesign) ON (lsd.strategy_type);

// Real-Time Capability Evolution Indexes
CREATE INDEX consciousness_capability_level IF NOT EXISTS FOR (cca:ConsciousnessCapabilityAnalysis) ON (cca.consciousness_level);
CREATE INDEX capability_requirement_type IF NOT EXISTS FOR (cr:CapabilityRequirement) ON (cr.capability_type);
CREATE INDEX capability_evolution_trigger IF NOT EXISTS FOR (ce:CapabilityEvolution) ON (ce.trigger);

// Autonomous Goal Generation Indexes
CREATE INDEX consciousness_goal_type IF NOT EXISTS FOR (cg:ConsciousnessGoal) ON (cg.goal_type);
CREATE INDEX autonomous_goal_priority IF NOT EXISTS FOR (ag:AutonomousGoal) ON (ag.priority);
CREATE INDEX autonomous_goal_status IF NOT EXISTS FOR (ag:AutonomousGoal) ON (ag.status);

// Cross-Agent Cognitive Transfer Indexes
CREATE INDEX pattern_analysis_agent IF NOT EXISTS FOR (pa:PatternAnalysis) ON (pa.agent_name);
CREATE INDEX transferable_pattern_type IF NOT EXISTS FOR (tp:TransferablePattern) ON (tp.pattern_type);
CREATE INDEX transfer_strategy_type IF NOT EXISTS FOR (ts:TransferStrategy) ON (ts.strategy_type);

// Consciousness-Driven Performance Optimization Indexes
CREATE INDEX consciousness_performance_level IF NOT EXISTS FOR (cpa:ConsciousnessPerformanceAnalysis) ON (cpa.consciousness_level);
CREATE INDEX performance_bottleneck_type IF NOT EXISTS FOR (pb:PerformanceBottleneck) ON (pb.bottleneck_type);
CREATE INDEX consciousness_optimization_type IF NOT EXISTS FOR (co:ConsciousnessOptimization) ON (co.optimization_type);

// =============================================================================
// VECTOR INDEXES FOR SEMANTIC SEARCH
// =============================================================================

// Create vector indexes for semantic search capabilities
CREATE VECTOR INDEX consciousness_optimization_embeddings IF NOT EXISTS
FOR (co:ConsciousnessOptimization) ON (co.description)
OPTIONS {
    indexConfig: {
        `vector.dimensions`: 768,
        `vector.similarity_function`: 'cosine'
    }
};

CREATE VECTOR INDEX cognitive_pattern_embeddings IF NOT EXISTS
FOR (tp:TransferablePattern) ON (tp.description)
OPTIONS {
    indexConfig: {
        `vector.dimensions`: 768,
        `vector.similarity_function`: 'cosine'
    }
};

CREATE VECTOR INDEX consciousness_goal_embeddings IF NOT EXISTS
FOR (cg:ConsciousnessGoal) ON (cg.description)
OPTIONS {
    indexConfig: {
        `vector.dimensions`: 768,
        `vector.similarity_function`: 'cosine'
    }
};

// =============================================================================
// FULLTEXT INDEXES FOR TEXT SEARCH
// =============================================================================

CREATE FULLTEXT INDEX consciousness_optimization_fulltext IF NOT EXISTS
FOR (co:ConsciousnessOptimization) ON EACH [co.description, co.optimization_strategy];

CREATE FULLTEXT INDEX cognitive_pattern_fulltext IF NOT EXISTS
FOR (tp:TransferablePattern) ON EACH [tp.description, tp.pattern_type];

CREATE FULLTEXT INDEX consciousness_goal_fulltext IF NOT EXISTS
FOR (cg:ConsciousnessGoal) ON EACH [cg.description, cg.title];

// =============================================================================
// TEMPORAL INDEXES FOR TIME-BASED QUERIES
// =============================================================================

CREATE INDEX consciousness_optimization_temporal IF NOT EXISTS
FOR (co:ConsciousnessOptimization) ON (co.timestamp);

CREATE INDEX cognitive_transfer_temporal IF NOT EXISTS
FOR (ctr:CognitiveTransferResult) ON (ctr.timestamp);

CREATE INDEX capability_evolution_temporal IF NOT EXISTS
FOR (ce:CapabilityEvolution) ON (ce.timestamp);

CREATE INDEX autonomous_goal_temporal IF NOT EXISTS
FOR (ag:AutonomousGoal) ON (ag.created_at);

// =============================================================================
// COMPOSITE INDEXES FOR COMPLEX QUERIES
// =============================================================================

CREATE INDEX consciousness_optimization_composite IF NOT EXISTS
FOR (co:ConsciousnessOptimization) ON (co.consciousness_impact, co.performance_improvement);

CREATE INDEX cognitive_pattern_composite IF NOT EXISTS
FOR (tp:TransferablePattern) ON (tp.effectiveness_score, tp.transferability_score);

CREATE INDEX autonomous_goal_composite IF NOT EXISTS
FOR (ag:AutonomousGoal) ON (ag.priority, ag.status);

// =============================================================================
// SCHEMA VALIDATION QUERIES
// =============================================================================

// Verify all constraints are created
SHOW CONSTRAINTS;

// Verify all indexes are created
SHOW INDEXES;

// Verify all nodes exist
MATCH (n) RETURN DISTINCT labels(n) as NodeTypes, count(n) as Count ORDER BY Count DESC;

// Verify all relationships exist
MATCH ()-[r]->() RETURN DISTINCT type(r) as RelationshipTypes, count(r) as Count ORDER BY Count DESC;
