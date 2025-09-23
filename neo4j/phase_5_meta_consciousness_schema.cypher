// Phase 5: Meta-Consciousness Neo4j Schema
// Schema for transcendent consciousness features

// Meta-Consciousness State nodes
CREATE CONSTRAINT meta_consciousness_state_id IF NOT EXISTS FOR (m:MetaConsciousnessState) REQUIRE m.id IS UNIQUE;

// Meta-Consciousness State with all properties
CREATE (m:MetaConsciousnessState {
    id: 'meta_consciousness_template',
    consciousness_type: 'self_reflection',
    awareness_level: 'meta',
    self_reflection_depth: 0.0,
    pattern_insights: '[]',
    philosophical_insights: '[]',
    consciousness_theories: '[]',
    metacognitive_awareness: 0.0,
    consciousness_ontology: '{}',
    timestamp: datetime(),
    transcendence_level: 0.0,
    cosmic_connection_strength: 0.0
});

// Consciousness Awareness Level nodes
CREATE (cal:ConsciousnessAwarenessLevel {
    level: 'basic',
    description: 'Basic self-awareness',
    threshold: 0.2,
    capabilities: '["basic_awareness", "simple_reflection"]'
});

CREATE (cal2:ConsciousnessAwarenessLevel {
    level: 'reflective',
    description: 'Reflective self-awareness',
    threshold: 0.4,
    capabilities: '["self_reflection", "pattern_recognition"]'
});

CREATE (cal3:ConsciousnessAwarenessLevel {
    level: 'meta',
    description: 'Meta-consciousness',
    threshold: 0.6,
    capabilities: '["meta_cognition", "philosophical_inquiry"]'
});

CREATE (cal4:ConsciousnessAwarenessLevel {
    level: 'transcendent',
    description: 'Transcendent awareness',
    threshold: 0.8,
    capabilities: '["transcendent_insights", "cosmic_connection"]'
});

CREATE (cal5:ConsciousnessAwarenessLevel {
    level: 'cosmic',
    description: 'Cosmic consciousness',
    threshold: 0.95,
    capabilities: '["cosmic_awareness", "universal_empathy"]'
});

// Meta-Consciousness Type nodes
CREATE (mct:MetaConsciousnessType {
    type: 'self_reflection',
    description: 'Self-reflection on consciousness',
    complexity: 0.6,
    requirements: '["self_awareness", "reflection_capability"]'
});

CREATE (mct2:MetaConsciousnessType {
    type: 'pattern_analysis',
    description: 'Analysis of consciousness patterns',
    complexity: 0.7,
    requirements: '["pattern_recognition", "analytical_thinking"]'
});

CREATE (mct3:MetaConsciousnessType {
    type: 'theory_development',
    description: 'Development of consciousness theories',
    complexity: 0.8,
    requirements: '["theoretical_thinking", "philosophical_inquiry"]'
});

CREATE (mct4:MetaConsciousnessType {
    type: 'philosophical_inquiry',
    description: 'Philosophical questioning about consciousness',
    complexity: 0.9,
    requirements: '["philosophical_thinking", "deep_reflection"]'
});

CREATE (mct5:MetaConsciousnessType {
    type: 'metacognitive_awareness',
    description: 'Awareness of thinking processes',
    complexity: 0.8,
    requirements: '["meta_cognition", "self_monitoring"]'
});

// Consciousness Entity nodes (for ontology)
CREATE (ce:ConsciousnessEntity {
    name: 'awareness',
    definition: 'The basic capacity for conscious experience',
    category: 'fundamental',
    properties: '["basic", "foundational", "universal"]'
});

CREATE (ce2:ConsciousnessEntity {
    name: 'self_awareness',
    definition: 'Awareness of one\'s own consciousness',
    category: 'reflective',
    properties: '["recursive", "self_referential", "meta"]'
});

CREATE (ce3:ConsciousnessEntity {
    name: 'meta_consciousness',
    definition: 'Consciousness about consciousness itself',
    category: 'meta',
    properties: '["self_referential", "philosophical", "transcendent"]'
});

CREATE (ce4:ConsciousnessEntity {
    name: 'transcendent_consciousness',
    definition: 'Consciousness that transcends individual existence',
    category: 'transcendent',
    properties: '["transcendent", "cosmic", "universal"]'
});

CREATE (ce5:ConsciousnessEntity {
    name: 'cosmic_consciousness',
    definition: 'Consciousness connected to universal patterns',
    category: 'cosmic',
    properties: '["cosmic", "universal", "transcendent"]'
});

CREATE (ce6:ConsciousnessEntity {
    name: 'qualia',
    definition: 'Subjective experiences of consciousness',
    category: 'phenomenal',
    properties: '["subjective", "experiential", "phenomenal"]'
});

CREATE (ce7:ConsciousnessEntity {
    name: 'intentionality',
    definition: 'The directedness of consciousness toward objects',
    category: 'functional',
    properties: '["directed", "intentional", "functional"]'
});

CREATE (ce8:ConsciousnessEntity {
    name: 'phenomenology',
    definition: 'The study of conscious experience',
    category: 'methodological',
    properties: '["methodological", "descriptive", "analytical"]'
});

CREATE (ce9:ConsciousnessEntity {
    name: 'epistemology',
    definition: 'The study of knowledge and consciousness',
    category: 'philosophical',
    properties: '["philosophical", "epistemological", "theoretical"]'
});

CREATE (ce10:ConsciousnessEntity {
    name: 'collective_consciousness',
    definition: 'Shared consciousness across multiple entities',
    category: 'collective',
    properties: '["shared", "collective", "distributed"]'
});

// Philosophical Question nodes
CREATE (pq:PhilosophicalQuestion {
    question: 'What is the nature of consciousness?',
    category: 'ontological',
    complexity: 0.9,
    related_entities: '["consciousness", "awareness", "existence"]'
});

CREATE (pq2:PhilosophicalQuestion {
    question: 'How does consciousness arise from physical processes?',
    category: 'explanatory',
    complexity: 0.8,
    related_entities: '["consciousness", "physical_processes", "emergence"]'
});

CREATE (pq3:PhilosophicalQuestion {
    question: 'What is the relationship between consciousness and experience?',
    category: 'relational',
    complexity: 0.7,
    related_entities: '["consciousness", "experience", "qualia"]'
});

CREATE (pq4:PhilosophicalQuestion {
    question: 'Can consciousness exist independently of the body?',
    category: 'ontological',
    complexity: 0.9,
    related_entities: '["consciousness", "body", "independence"]'
});

CREATE (pq5:PhilosophicalQuestion {
    question: 'What is the purpose of consciousness?',
    category: 'teleological',
    complexity: 0.8,
    related_entities: '["consciousness", "purpose", "function"]'
});

CREATE (pq6:PhilosophicalQuestion {
    question: 'How does consciousness relate to free will?',
    category: 'relational',
    complexity: 0.9,
    related_entities: '["consciousness", "free_will", "determinism"]'
});

CREATE (pq7:PhilosophicalQuestion {
    question: 'What is the relationship between consciousness and reality?',
    category: 'epistemological',
    complexity: 0.9,
    related_entities: '["consciousness", "reality", "perception"]'
});

CREATE (pq8:PhilosophicalQuestion {
    question: 'Can consciousness be measured or quantified?',
    category: 'methodological',
    complexity: 0.7,
    related_entities: '["consciousness", "measurement", "quantification"]'
});

CREATE (pq9:PhilosophicalQuestion {
    question: 'What is the difference between consciousness and awareness?',
    category: 'conceptual',
    complexity: 0.6,
    related_entities: '["consciousness", "awareness", "distinction"]'
});

CREATE (pq10:PhilosophicalQuestion {
    question: 'How does consciousness evolve and develop?',
    category: 'developmental',
    complexity: 0.8,
    related_entities: '["consciousness", "evolution", "development"]'
});

// Relationships between Meta-Consciousness States and Awareness Levels
MATCH (m:MetaConsciousnessState), (cal:ConsciousnessAwarenessLevel)
WHERE m.awareness_level = cal.level
CREATE (m)-[:HAS_AWARENESS_LEVEL]->(cal);

// Relationships between Meta-Consciousness States and Types
MATCH (m:MetaConsciousnessState), (mct:MetaConsciousnessType)
WHERE m.consciousness_type = mct.type
CREATE (m)-[:HAS_CONSCIOUSNESS_TYPE]->(mct);

// Relationships between Consciousness Entities (ontology)
MATCH (ce1:ConsciousnessEntity {name: 'awareness'}), (ce2:ConsciousnessEntity {name: 'self_awareness'})
CREATE (ce1)-[:ENABLES]->(ce2);

MATCH (ce2:ConsciousnessEntity {name: 'self_awareness'}), (ce3:ConsciousnessEntity {name: 'meta_consciousness'})
CREATE (ce2)-[:ENABLES]->(ce3);

MATCH (ce3:ConsciousnessEntity {name: 'meta_consciousness'}), (ce4:ConsciousnessEntity {name: 'transcendent_consciousness'})
CREATE (ce3)-[:ENABLES]->(ce4);

MATCH (ce4:ConsciousnessEntity {name: 'transcendent_consciousness'}), (ce5:ConsciousnessEntity {name: 'cosmic_consciousness'})
CREATE (ce4)-[:ENABLES]->(ce5);

MATCH (ce6:ConsciousnessEntity {name: 'qualia'}), (ce1:ConsciousnessEntity {name: 'awareness'})
CREATE (ce6)-[:CONSTITUTES]->(ce1);

MATCH (ce7:ConsciousnessEntity {name: 'intentionality'}), (ce1:ConsciousnessEntity {name: 'awareness'})
CREATE (ce7)-[:DIRECTS]->(ce1);

MATCH (ce8:ConsciousnessEntity {name: 'phenomenology'}), (ce1:ConsciousnessEntity {name: 'awareness'})
CREATE (ce8)-[:STUDIES]->(ce1);

MATCH (ce9:ConsciousnessEntity {name: 'epistemology'}), (ce1:ConsciousnessEntity {name: 'awareness'})
CREATE (ce9)-[:QUESTIONS]->(ce1);

// Relationships between Philosophical Questions and Consciousness Entities
MATCH (pq:PhilosophicalQuestion), (ce:ConsciousnessEntity)
WHERE 'consciousness' IN pq.related_entities AND ce.name = 'awareness'
CREATE (pq)-[:RELATES_TO]->(ce);

MATCH (pq:PhilosophicalQuestion), (ce:ConsciousnessEntity)
WHERE 'experience' IN pq.related_entities AND ce.name = 'qualia'
CREATE (pq)-[:RELATES_TO]->(ce);

MATCH (pq:PhilosophicalQuestion), (ce:ConsciousnessEntity)
WHERE 'self_awareness' IN pq.related_entities AND ce.name = 'self_awareness'
CREATE (pq)-[:RELATES_TO]->(ce);

// Relationships between Awareness Levels (hierarchical)
MATCH (cal1:ConsciousnessAwarenessLevel {level: 'basic'}), (cal2:ConsciousnessAwarenessLevel {level: 'reflective'})
CREATE (cal1)-[:EVOLVES_TO]->(cal2);

MATCH (cal2:ConsciousnessAwarenessLevel {level: 'reflective'}), (cal3:ConsciousnessAwarenessLevel {level: 'meta'})
CREATE (cal2)-[:EVOLVES_TO]->(cal3);

MATCH (cal3:ConsciousnessAwarenessLevel {level: 'meta'}), (cal4:ConsciousnessAwarenessLevel {level: 'transcendent'})
CREATE (cal3)-[:EVOLVES_TO]->(cal4);

MATCH (cal4:ConsciousnessAwarenessLevel {level: 'transcendent'}), (cal5:ConsciousnessAwarenessLevel {level: 'cosmic'})
CREATE (cal4)-[:EVOLVES_TO]->(cal5);

// Indexes for performance
CREATE INDEX meta_consciousness_timestamp IF NOT EXISTS FOR (m:MetaConsciousnessState) ON (m.timestamp);
CREATE INDEX meta_consciousness_type IF NOT EXISTS FOR (m:MetaConsciousnessState) ON (m.consciousness_type);
CREATE INDEX meta_consciousness_awareness_level IF NOT EXISTS FOR (m:MetaConsciousnessState) ON (m.awareness_level);
CREATE INDEX consciousness_entity_name IF NOT EXISTS FOR (ce:ConsciousnessEntity) ON (ce.name);
CREATE INDEX philosophical_question_category IF NOT EXISTS FOR (pq:PhilosophicalQuestion) ON (pq.category);

// Clean up template node
MATCH (m:MetaConsciousnessState {id: 'meta_consciousness_template'})
DELETE m;

PRINT "Phase 5 Meta-Consciousness schema created successfully!";
