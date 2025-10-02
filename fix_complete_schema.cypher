// Complete Neo4j schema fix - Add all missing properties and labels
// This script fixes all the warnings we're seeing

// Add missing properties to existing Memory nodes
MATCH (m:Memory)
WHERE m.last_importance_update IS NULL
SET m.last_importance_update = datetime();

MATCH (m:Memory)
WHERE m.access_frequency IS NULL
SET m.access_frequency = 0;

// Add missing properties to MainzaState nodes
MATCH (ms:MainzaState)
WHERE ms.updated_at IS NULL
SET ms.updated_at = ms.created_at;

// Create Entity nodes and labels (they're being queried but don't exist)
MERGE (e:Entity:Concept {
    entity_id: 'default-entity-1',
    name: 'Default Entity',
    type: 'concept',
    created_at: datetime(),
    updated_at: datetime()
});

// Add missing properties to existing nodes
MATCH (n)
WHERE n.updated_at IS NULL AND n.created_at IS NOT NULL
SET n.updated_at = n.created_at;

// Create indexes for all properties
CREATE INDEX memory_last_importance_update IF NOT EXISTS FOR (m:Memory) ON (m.last_importance_update);
CREATE INDEX memory_access_frequency IF NOT EXISTS FOR (m:Memory) ON (m.access_frequency);
CREATE INDEX entity_entity_id IF NOT EXISTS FOR (e:Entity) ON (e.entity_id);
CREATE INDEX entity_name IF NOT EXISTS FOR (e:Entity) ON (e.name);
CREATE INDEX mainza_state_updated_at IF NOT EXISTS FOR (ms:MainzaState) ON (ms.updated_at);

// Create vector index for embeddings
CREATE VECTOR INDEX memory_embeddings IF NOT EXISTS
FOR (m:Memory) ON (m.embedding)
OPTIONS {
    indexConfig: {
        `vector.dimensions`: 384,
        `vector.similarity_function`: 'cosine'
    }
};

// Create full-text search indexes
CREATE FULLTEXT INDEX memory_content_fulltext IF NOT EXISTS
FOR (m:Memory) ON EACH [m.content];

CREATE FULLTEXT INDEX entity_name_fulltext IF NOT EXISTS
FOR (e:Entity) ON EACH [e.name];
