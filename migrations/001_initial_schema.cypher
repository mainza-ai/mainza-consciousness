// Mainza Neo4j Schema Setup
// Constraints and indexes for development

CREATE CONSTRAINT user_id_unique IF NOT EXISTS FOR (u:User) REQUIRE u.user_id IS UNIQUE;
CREATE CONSTRAINT conversation_id_unique IF NOT EXISTS FOR (c:Conversation) REQUIRE c.conversation_id IS UNIQUE;
CREATE CONSTRAINT memory_id_unique IF NOT EXISTS FOR (m:Memory) REQUIRE m.memory_id IS UNIQUE;
CREATE CONSTRAINT document_id_unique IF NOT EXISTS FOR (d:Document) REQUIRE d.document_id IS UNIQUE;
CREATE CONSTRAINT chunk_id_unique IF NOT EXISTS FOR (ch:Chunk) REQUIRE ch.chunk_id IS UNIQUE;
CREATE CONSTRAINT entity_id_unique IF NOT EXISTS FOR (e:Entity) REQUIRE e.entity_id IS UNIQUE;
CREATE CONSTRAINT concept_id_unique IF NOT EXISTS FOR (co:Concept) REQUIRE co.concept_id IS UNIQUE;
CREATE CONSTRAINT mainzastate_id_unique IF NOT EXISTS FOR (ms:MainzaState) REQUIRE ms.state_id IS UNIQUE;

CREATE INDEX memory_text IF NOT EXISTS FOR (m:Memory) ON (m.text);
CREATE INDEX entity_name IF NOT EXISTS FOR (e:Entity) ON (e.name);
CREATE INDEX concept_name IF NOT EXISTS FOR (co:Concept) ON (co.name);
CREATE INDEX document_filename IF NOT EXISTS FOR (d:Document) ON (d.filename);
CREATE INDEX chunk_embedding IF NOT EXISTS FOR (ch:Chunk) ON (ch.embedding);

// ... (rest of schema as in neo4j/schema.cypher) ... 