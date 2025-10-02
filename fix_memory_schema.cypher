// Fix Memory schema by adding missing properties
// This script adds the missing properties that are causing Neo4j warnings

// Add missing properties to existing Memory nodes
MATCH (m:Memory)
WHERE m.last_importance_update IS NULL
SET m.last_importance_update = datetime();

MATCH (m:Memory)
WHERE m.access_frequency IS NULL
SET m.access_frequency = 0;

// Create indexes for the new properties
CREATE INDEX memory_last_importance_update IF NOT EXISTS FOR (m:Memory) ON (m.last_importance_update);
CREATE INDEX memory_access_frequency IF NOT EXISTS FOR (m:Memory) ON (m.access_frequency);