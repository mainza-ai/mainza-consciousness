// Mainza Neo4j Schema Setup
// Constraints and indexes for development

// --- NODE CONSTRAINTS ---
CREATE CONSTRAINT user_id_unique IF NOT EXISTS FOR (u:User) REQUIRE u.user_id IS UNIQUE;
CREATE CONSTRAINT conversation_id_unique IF NOT EXISTS FOR (c:Conversation) REQUIRE c.conversation_id IS UNIQUE;
CREATE CONSTRAINT memory_id_unique IF NOT EXISTS FOR (m:Memory) REQUIRE m.memory_id IS UNIQUE;
CREATE CONSTRAINT document_id_unique IF NOT EXISTS FOR (d:Document) REQUIRE d.document_id IS UNIQUE;
CREATE CONSTRAINT chunk_id_unique IF NOT EXISTS FOR (ch:Chunk) REQUIRE ch.chunk_id IS UNIQUE;
CREATE CONSTRAINT entity_id_unique IF NOT EXISTS FOR (e:Entity) REQUIRE e.entity_id IS UNIQUE;
CREATE CONSTRAINT concept_id_unique IF NOT EXISTS FOR (co:Concept) REQUIRE co.concept_id IS UNIQUE;
CREATE CONSTRAINT mainzastate_id_unique IF NOT EXISTS FOR (ms:MainzaState) REQUIRE ms.state_id IS UNIQUE;

// --- INDEXES FOR SEARCHABLE PROPERTIES ---
CREATE INDEX memory_text IF NOT EXISTS FOR (m:Memory) ON (m.text);
CREATE INDEX entity_name IF NOT EXISTS FOR (e:Entity) ON (e.name);
CREATE INDEX concept_name IF NOT EXISTS FOR (co:Concept) ON (co.name);
CREATE INDEX document_filename IF NOT EXISTS FOR (d:Document) ON (d.filename);
// Vector index for semantic search (CRITICAL FIX)
CREATE VECTOR INDEX ChunkEmbeddingIndex IF NOT EXISTS
FOR (ch:Chunk) ON ch.embedding
OPTIONS {indexConfig: {
  `vector.dimensions`: 384,
  `vector.similarity_function`: 'cosine'
}};

// --- RELATIONSHIP TYPES (for documentation, not enforced in Cypher) ---
// DISCUSSED_IN: (:Memory|:Entity)-[:DISCUSSED_IN]->(:Conversation)
// RELATES_TO: (any node)-[:RELATES_TO]->(any node)
// DERIVED_FROM: (:Chunk)-[:DERIVED_FROM]->(:Document)
// MENTIONS: (:Conversation)-[:MENTIONS]->(:Document|:Entity)
// NEEDS_TO_LEARN: (:MainzaState)-[:NEEDS_TO_LEARN]->(:Concept)

// --- EXAMPLE NODE CREATION (for reference) ---
// CREATE (u:User {user_id: 'user-1', name: 'Alice'});
// CREATE (c:Conversation {conversation_id: 'conv-1', started_at: datetime()});
// CREATE (m:Memory {memory_id: 'mem-1', text: 'User's sister's name is Jessica.'});
// CREATE (d:Document {document_id: 'doc-1', filename: 'notes.pdf'});
// CREATE (ch:Chunk {chunk_id: 'chunk-1', text: '...', embedding: [0.1, 0.2, ...]});
// CREATE (e:Entity {entity_id: 'ent-1', name: 'Jessica'});
// CREATE (co:Concept {concept_id: 'concept-1', name: 'Machine Learning'});
// CREATE (ms:MainzaState {state_id: 'mainza-1', evolution_level: 1, current_needs: [], core_directives: '...'});

// --- MINIMAL MAINZA SEED ---
// Run this section in Neo4j Browser or cypher-shell to create the minimum required nodes for Mainza to function.
// These nodes are required for the backend endpoints to work and for the UI to show needs/recommendations.

CREATE (ms:MainzaState {state_id: 'mainza-state-1', evolution_level: 1, current_needs: [], core_directives: 'Assist the user.'});
CREATE (co1:Concept {concept_id: 'concept-1', name: 'Machine Learning'});
CREATE (co2:Concept {concept_id: 'concept-2', name: 'Neo4j'});
CREATE (co3:Concept {concept_id: 'concept-3', name: 'Personal Knowledge Management'});

// --- COMPREHENSIVE MAINZA DEMO SEED ---
// Run this section in Neo4j Browser or cypher-shell for a richer demo graph.
// This will create a user, conversation, memory, document, chunk, entity, concepts, and all key relationships.

// User
CREATE (u:User {user_id: 'user-1', name: 'Alice'});

// Conversation
CREATE (conv:Conversation {conversation_id: 'conv-1', started_at: datetime()});

// Memory (linked to user and conversation)
CREATE (m:Memory {memory_id: 'mem-1', text: "Alice's sister's name is Jessica."});
CREATE (m)-[:DISCUSSED_IN]->(conv);
CREATE (m)<-[:DISCUSSED_IN]-(u);

// Document
CREATE (d:Document {document_id: 'doc-1', filename: 'notes.pdf', metadata: {topic: 'AI'}});

// Chunk (derived from document)
CREATE (ch:Chunk {chunk_id: 'chunk-1', text: 'AI is transforming the world.', embedding: [0.1, 0.2, 0.3]});
CREATE (ch)-[:DERIVED_FROM]->(d);

// Entity
CREATE (e:Entity {entity_id: 'ent-1', name: 'Jessica'});

// Concepts (reuse minimal seed, but ensure they exist)
MERGE (co1:Concept {concept_id: 'concept-1', name: 'Machine Learning'});
MERGE (co2:Concept {concept_id: 'concept-2', name: 'Neo4j'});
MERGE (co3:Concept {concept_id: 'concept-3', name: 'Personal Knowledge Management'});

// MainzaState (reuse minimal seed, but ensure it exists)
MERGE (ms:MainzaState {state_id: 'mainza-state-1', evolution_level: 1, current_needs: [], core_directives: 'Assist the user.'});

// Relationships
// Memory discussed in Conversation
MERGE (m)-[:DISCUSSED_IN]->(conv);
// Conversation mentions Document and Entity
MERGE (conv)-[:MENTIONS]->(d);
MERGE (conv)-[:MENTIONS]->(e);
// MainzaState NEEDS_TO_LEARN a Concept
MERGE (ms)-[:NEEDS_TO_LEARN]->(co1);
// Concepts RELATES_TO each other
MERGE (co1)-[:RELATES_TO]->(co2);
MERGE (co2)-[:RELATES_TO]->(co3);
// Chunk DERIVED_FROM Document (already above)

// Example: Entity mentioned in Memory
MERGE (m)-[:MENTIONS]->(e); 

CREATE CONSTRAINT task_id_unique IF NOT EXISTS FOR (t:Task) REQUIRE t.task_id IS UNIQUE;
CREATE INDEX task_completed IF NOT EXISTS FOR (t:Task) ON (t.completed);

CREATE (t:Task {task_id: 'task-1', completed: false, description: 'Demo task'});
MATCH (u:User {user_id: 'user-1'}), (t:Task {task_id: 'task-1'})
CREATE (t)-[:ASSIGNED_TO]->(u);