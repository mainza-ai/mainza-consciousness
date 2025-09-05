"""
Memory Schema Manager for Mainza AI
Handles creation and validation of memory-related Neo4j schema elements
"""
import logging
import os
from typing import Dict, Any, List, Optional
from backend.utils.neo4j_enhanced import neo4j_manager

logger = logging.getLogger(__name__)

class MemorySchemaManager:
    """
    Manages Neo4j schema elements for the memory system
    """
    
    def __init__(self):
        self.neo4j = neo4j_manager
        self.schema_file = "backend/neo4j/memory_schema.cypher"
        
    async def initialize_memory_schema(self) -> bool:
        """
        Initialize the complete memory schema in Neo4j
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.info("🔧 Initializing memory schema in Neo4j...")
            
            # Create constraints
            constraints_created = await self._create_memory_constraints()
            if not constraints_created:
                logger.error("❌ Failed to create memory constraints")
                return False
            
            # Create indexes
            indexes_created = await self._create_memory_indexes()
            if not indexes_created:
                logger.error("❌ Failed to create memory indexes")
                return False
            
            # Create vector index for embeddings
            vector_index_created = await self._create_vector_index()
            if not vector_index_created:
                logger.warning("⚠️ Failed to create vector index (may not be supported)")
            
            # Create full-text index
            fulltext_index_created = await self._create_fulltext_index()
            if not fulltext_index_created:
                logger.warning("⚠️ Failed to create full-text index")
            
            logger.info("✅ Memory schema initialization completed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Memory schema initialization failed: {e}")
            return False
    
    async def _create_memory_constraints(self) -> bool:
        """Create memory-related constraints"""
        try:
            constraints = [
                # Memory node constraints
                """
                CREATE CONSTRAINT memory_id_unique IF NOT EXISTS
                FOR (m:Memory) REQUIRE m.memory_id IS UNIQUE
                """,
                
                # Enhanced interaction constraints
                """
                CREATE CONSTRAINT enhanced_interaction_id_unique IF NOT EXISTS
                FOR (ei:EnhancedInteraction) REQUIRE ei.interaction_id IS UNIQUE
                """
            ]
            
            for constraint in constraints:
                try:
                    self.neo4j.execute_write_query(constraint.strip())
                    logger.debug(f"✅ Created constraint: {constraint.split()[2]}")
                except Exception as e:
                    if "already exists" in str(e).lower():
                        logger.debug(f"⚠️ Constraint already exists: {constraint.split()[2]}")
                    else:
                        logger.error(f"❌ Failed to create constraint: {e}")
                        return False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create memory constraints: {e}")
            return False
    
    async def _create_memory_indexes(self) -> bool:
        """Create memory-related indexes"""
        try:
            indexes = [
                # Basic memory indexes
                "CREATE INDEX memory_user_id_index IF NOT EXISTS FOR (m:Memory) ON (m.user_id)",
                "CREATE INDEX memory_type_index IF NOT EXISTS FOR (m:Memory) ON (m.memory_type)",
                "CREATE INDEX memory_agent_index IF NOT EXISTS FOR (m:Memory) ON (m.agent_name)",
                "CREATE INDEX memory_created_at_index IF NOT EXISTS FOR (m:Memory) ON (m.created_at)",
                "CREATE INDEX memory_importance_index IF NOT EXISTS FOR (m:Memory) ON (m.importance_score)",
                "CREATE INDEX memory_consciousness_level_index IF NOT EXISTS FOR (m:Memory) ON (m.consciousness_level)",
                "CREATE INDEX memory_emotional_state_index IF NOT EXISTS FOR (m:Memory) ON (m.emotional_state)",
                
                # Composite indexes for common query patterns
                "CREATE INDEX memory_user_type_composite IF NOT EXISTS FOR (m:Memory) ON (m.user_id, m.memory_type)",
                "CREATE INDEX memory_user_created_composite IF NOT EXISTS FOR (m:Memory) ON (m.user_id, m.created_at)",
                
                # Memory lifecycle indexes
                "CREATE INDEX memory_last_accessed_index IF NOT EXISTS FOR (m:Memory) ON (m.last_accessed)",
                "CREATE INDEX memory_access_count_index IF NOT EXISTS FOR (m:Memory) ON (m.access_count)",
                "CREATE INDEX memory_significance_index IF NOT EXISTS FOR (m:Memory) ON (m.significance_score)",
                
                # Relationship indexes
                "CREATE INDEX memory_concept_strength_index IF NOT EXISTS FOR ()-[r:RELATES_TO_CONCEPT]-() ON (r.strength)",
                "CREATE INDEX memory_concept_access_index IF NOT EXISTS FOR ()-[r:RELATES_TO_CONCEPT]-() ON (r.access_count)",
                "CREATE INDEX memory_state_consciousness_index IF NOT EXISTS FOR ()-[r:CREATED_DURING_STATE]-() ON (r.consciousness_level)",
                
                # Enhanced interaction indexes
                "CREATE INDEX enhanced_interaction_user_index IF NOT EXISTS FOR (ei:EnhancedInteraction) ON (ei.user_id)",
                "CREATE INDEX enhanced_interaction_agent_index IF NOT EXISTS FOR (ei:EnhancedInteraction) ON (ei.agent_name)",
                "CREATE INDEX enhanced_interaction_timestamp_index IF NOT EXISTS FOR (ei:EnhancedInteraction) ON (ei.timestamp)",
                "CREATE INDEX enhanced_interaction_context_strength_index IF NOT EXISTS FOR (ei:EnhancedInteraction) ON (ei.context_strength)"
            ]
            
            for index in indexes:
                try:
                    self.neo4j.execute_write_query(index)
                    index_name = index.split()[2]  # Extract index name
                    logger.debug(f"✅ Created index: {index_name}")
                except Exception as e:
                    if "already exists" in str(e).lower():
                        index_name = index.split()[2]
                        logger.debug(f"⚠️ Index already exists: {index_name}")
                    else:
                        logger.error(f"❌ Failed to create index: {e}")
                        return False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create memory indexes: {e}")
            return False
    
    async def _create_vector_index(self) -> bool:
        """Create vector index for memory embeddings"""
        try:
            # Check if vector indexes are supported
            version_query = "CALL dbms.components() YIELD versions RETURN versions"
            version_result = self.neo4j.execute_query(version_query)
            
            # Get current embedding dimensions from the embedding manager
            from backend.utils.embedding_enhanced import embedding_manager
            current_dimensions = embedding_manager.dimensions
            
            # Try to create vector index (Neo4j 5.0+)
            vector_index_query = f"""
            CREATE VECTOR INDEX memory_embedding_index IF NOT EXISTS
            FOR (m:Memory) ON (m.embedding)
            OPTIONS {{
              indexConfig: {{
                `vector.dimensions`: {current_dimensions},
                `vector.similarity_function`: 'cosine'
              }}
            }}
            """
            
            self.neo4j.execute_write_query(vector_index_query)
            logger.info("✅ Created vector index for memory embeddings")
            return True
            
        except Exception as e:
            logger.warning(f"⚠️ Vector index creation failed (may not be supported): {e}")
            return False
    
    async def _create_fulltext_index(self) -> bool:
        """Create full-text search index for memory content"""
        try:
            fulltext_query = """
            CREATE FULLTEXT INDEX memory_content_fulltext IF NOT EXISTS
            FOR (m:Memory) ON EACH [m.content]
            """
            
            self.neo4j.execute_write_query(fulltext_query)
            logger.info("✅ Created full-text index for memory content")
            return True
            
        except Exception as e:
            logger.warning(f"⚠️ Full-text index creation failed: {e}")
            return False
    
    async def validate_memory_schema(self) -> Dict[str, Any]:
        """
        Validate that the memory schema is properly set up
        
        Returns:
            Dict containing validation results
        """
        try:
            validation_results = {
                "constraints": [],
                "indexes": [],
                "vector_index_exists": False,
                "fulltext_index_exists": False,
                "schema_valid": False
            }
            
            # Check constraints (try different procedures for compatibility)
            constraints_result = []
            try:
                constraints_query = """
                CALL db.constraints() 
                YIELD name, type 
                WHERE name CONTAINS 'memory' OR name CONTAINS 'enhanced_interaction'
                RETURN name, type
                """
                constraints_result = self.neo4j.execute_query(constraints_query)
            except Exception as e:
                if "ProcedureNotFound" in str(e):
                    # Try alternative procedure for older Neo4j versions
                    try:
                        constraints_query = "SHOW CONSTRAINTS YIELD name, type RETURN name, type"
                        constraints_result = self.neo4j.execute_query(constraints_query)
                        # Filter for memory-related constraints
                        constraints_result = [
                            c for c in constraints_result 
                            if 'memory' in c.get('name', '').lower() or 'enhanced_interaction' in c.get('name', '').lower()
                        ]
                    except Exception:
                        logger.warning("Could not retrieve constraints information")
                        constraints_result = []
                else:
                    raise e
            
            validation_results["constraints"] = constraints_result
            
            # Check indexes (try different procedures for compatibility)
            indexes_result = []
            try:
                indexes_query = """
                CALL db.indexes() 
                YIELD name, type, state 
                WHERE name CONTAINS 'memory' OR name CONTAINS 'enhanced_interaction'
                RETURN name, type, state
                """
                indexes_result = self.neo4j.execute_query(indexes_query)
            except Exception as e:
                if "ProcedureNotFound" in str(e):
                    # Try alternative procedure for older Neo4j versions
                    try:
                        indexes_query = "SHOW INDEXES YIELD name, type, state RETURN name, type, state"
                        indexes_result = self.neo4j.execute_query(indexes_query)
                        # Filter for memory-related indexes
                        indexes_result = [
                            idx for idx in indexes_result 
                            if 'memory' in idx.get('name', '').lower() or 'enhanced_interaction' in idx.get('name', '').lower()
                        ]
                    except Exception:
                        logger.warning("Could not retrieve indexes information")
                        indexes_result = []
                else:
                    raise e
            
            validation_results["indexes"] = indexes_result
            
            # Check for vector index
            vector_indexes = [idx for idx in indexes_result if idx.get("type") == "VECTOR"]
            validation_results["vector_index_exists"] = len(vector_indexes) > 0
            
            # Check for full-text index
            fulltext_indexes = [idx for idx in indexes_result if idx.get("type") == "FULLTEXT"]
            validation_results["fulltext_index_exists"] = len(fulltext_indexes) > 0
            
            # Overall validation
            required_constraints = ["memory_id_unique", "enhanced_interaction_id_unique"]
            existing_constraint_names = [c.get("name", "") for c in constraints_result]
            
            constraints_valid = all(
                any(req in name for name in existing_constraint_names) 
                for req in required_constraints
            )
            
            indexes_valid = len(indexes_result) >= 10  # Expect at least 10 indexes
            
            validation_results["schema_valid"] = constraints_valid and indexes_valid
            
            logger.info(f"📊 Memory schema validation: {validation_results['schema_valid']}")
            return validation_results
            
        except Exception as e:
            logger.error(f"❌ Memory schema validation failed: {e}")
            return {"schema_valid": False, "error": str(e)}
    
    async def get_memory_schema_info(self) -> Dict[str, Any]:
        """Get comprehensive information about the memory schema"""
        try:
            info = {
                "memory_nodes_count": 0,
                "enhanced_interactions_count": 0,
                "memory_relationships_count": 0,
                "schema_elements": {}
            }
            
            # Count memory nodes
            memory_count_query = "MATCH (m:Memory) RETURN count(m) AS count"
            memory_result = self.neo4j.execute_query(memory_count_query)
            if memory_result:
                info["memory_nodes_count"] = memory_result[0]["count"]
            
            # Count enhanced interactions
            interaction_count_query = "MATCH (ei:EnhancedInteraction) RETURN count(ei) AS count"
            interaction_result = self.neo4j.execute_query(interaction_count_query)
            if interaction_result:
                info["enhanced_interactions_count"] = interaction_result[0]["count"]
            
            # Count memory relationships
            relationship_count_query = """
            MATCH (m:Memory)-[r]->()
            RETURN type(r) AS relationship_type, count(r) AS count
            """
            relationship_result = self.neo4j.execute_query(relationship_count_query)
            info["memory_relationships_count"] = sum(r["count"] for r in relationship_result)
            
            # Get schema validation
            validation = await self.validate_memory_schema()
            info["schema_elements"] = validation
            
            return info
            
        except Exception as e:
            logger.error(f"❌ Failed to get memory schema info: {e}")
            return {"error": str(e)}
    
    async def cleanup_test_data(self) -> bool:
        """Remove test memory data (for development/testing)"""
        try:
            cleanup_queries = [
                "MATCH (m:Memory) WHERE m.memory_id STARTS WITH 'test_' DELETE m",
                "MATCH (ei:EnhancedInteraction) WHERE ei.interaction_id STARTS WITH 'test_' DELETE ei"
            ]
            
            for query in cleanup_queries:
                result = self.neo4j.execute_write_query(query)
                logger.debug(f"✅ Cleaned up test data: {query}")
            
            logger.info("✅ Test data cleanup completed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Test data cleanup failed: {e}")
            return False

# Global instance
memory_schema_manager = MemorySchemaManager()