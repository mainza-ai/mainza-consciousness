"""
Comprehensive Neo4j schema management system.
Addresses critical issues:
- Missing ChunkEmbeddingIndex vector index
- Performance indexes for common query patterns
- Schema validation and health checks
- Automated schema migrations
"""
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from backend.utils.neo4j_production import neo4j_production
from backend.config.production_config import get_neo4j_config

logger = logging.getLogger(__name__)

class SchemaManager:
    """Manages Neo4j database schema with migrations and validation."""
    
    def __init__(self):
        self.neo4j_config = get_neo4j_config()
        
        # Schema version tracking
        self.current_schema_version = "1.2.0"
        
        # Define required constraints
        self.required_constraints = [
            {
                "name": "user_id_unique",
                "type": "UNIQUENESS",
                "query": "CREATE CONSTRAINT user_id_unique IF NOT EXISTS FOR (u:User) REQUIRE u.user_id IS UNIQUE"
            },
            {
                "name": "conversation_id_unique", 
                "type": "UNIQUENESS",
                "query": "CREATE CONSTRAINT conversation_id_unique IF NOT EXISTS FOR (c:Conversation) REQUIRE c.conversation_id IS UNIQUE"
            },
            {
                "name": "memory_id_unique",
                "type": "UNIQUENESS", 
                "query": "CREATE CONSTRAINT memory_id_unique IF NOT EXISTS FOR (m:Memory) REQUIRE m.memory_id IS UNIQUE"
            },
            {
                "name": "document_id_unique",
                "type": "UNIQUENESS",
                "query": "CREATE CONSTRAINT document_id_unique IF NOT EXISTS FOR (d:Document) REQUIRE d.document_id IS UNIQUE"
            },
            {
                "name": "chunk_id_unique",
                "type": "UNIQUENESS",
                "query": "CREATE CONSTRAINT chunk_id_unique IF NOT EXISTS FOR (ch:Chunk) REQUIRE ch.chunk_id IS UNIQUE"
            },
            {
                "name": "entity_id_unique",
                "type": "UNIQUENESS",
                "query": "CREATE CONSTRAINT entity_id_unique IF NOT EXISTS FOR (e:Entity) REQUIRE e.entity_id IS UNIQUE"
            },
            {
                "name": "concept_id_unique",
                "type": "UNIQUENESS",
                "query": "CREATE CONSTRAINT concept_id_unique IF NOT EXISTS FOR (co:Concept) REQUIRE co.concept_id IS UNIQUE"
            },
            {
                "name": "task_id_unique",
                "type": "UNIQUENESS",
                "query": "CREATE CONSTRAINT task_id_unique IF NOT EXISTS FOR (t:Task) REQUIRE t.task_id IS UNIQUE"
            },
            {
                "name": "mainzastate_id_unique",
                "type": "UNIQUENESS",
                "query": "CREATE CONSTRAINT mainzastate_id_unique IF NOT EXISTS FOR (ms:MainzaState) REQUIRE ms.state_id IS UNIQUE"
            }
        ]
        
        # Define required indexes
        self.required_indexes = [
            {
                "name": "memory_content_index",
                "type": "BTREE",
                "query": "CREATE INDEX memory_content_index IF NOT EXISTS FOR (m:Memory) ON (m.content)"
            },
            {
                "name": "entity_name_index",
                "type": "BTREE", 
                "query": "CREATE INDEX entity_name_index IF NOT EXISTS FOR (e:Entity) ON (e.name)"
            },
            {
                "name": "concept_name_index",
                "type": "BTREE",
                "query": "CREATE INDEX concept_name_index IF NOT EXISTS FOR (co:Concept) ON (co.name)"
            },
            {
                "name": "document_filename_index",
                "type": "BTREE",
                "query": "CREATE INDEX document_filename_index IF NOT EXISTS FOR (d:Document) ON (d.filename)"
            },
            {
                "name": "conversation_started_at_index",
                "type": "BTREE",
                "query": "CREATE INDEX conversation_started_at_index IF NOT EXISTS FOR (c:Conversation) ON (c.started_at)"
            },
            {
                "name": "memory_created_at_index",
                "type": "BTREE",
                "query": "CREATE INDEX memory_created_at_index IF NOT EXISTS FOR (m:Memory) ON (m.created_at)"
            },
            {
                "name": "task_completed_index",
                "type": "BTREE",
                "query": "CREATE INDEX task_completed_index IF NOT EXISTS FOR (t:Task) ON (t.completed)"
            },
            {
                "name": "chunk_document_id_index",
                "type": "BTREE",
                "query": "CREATE INDEX chunk_document_id_index IF NOT EXISTS FOR (ch:Chunk) ON (ch.document_id)"
            },
            {
                "name": "memory_source_index",
                "type": "BTREE",
                "query": "CREATE INDEX memory_source_index IF NOT EXISTS FOR (m:Memory) ON (m.source)"
            }
        ]
        
        # Define composite indexes for common query patterns
        self.composite_indexes = [
            {
                "name": "user_memory_conversation_index",
                "type": "BTREE",
                "query": "CREATE INDEX user_memory_conversation_index IF NOT EXISTS FOR (m:Memory) ON (m.user_id, m.conversation_id)"
            },
            {
                "name": "memory_user_created_index",
                "type": "BTREE", 
                "query": "CREATE INDEX memory_user_created_index IF NOT EXISTS FOR (m:Memory) ON (m.user_id, m.created_at)"
            }
        ]
        
        # Define vector indexes
        self.vector_indexes = [
            {
                "name": "ChunkEmbeddingIndex",
                "type": "VECTOR",
                "query": """
                CREATE VECTOR INDEX ChunkEmbeddingIndex IF NOT EXISTS
                FOR (ch:Chunk) ON ch.embedding
                OPTIONS {indexConfig: {
                  `vector.dimensions`: 384,
                  `vector.similarity_function`: 'cosine'
                }}
                """
            }
        ]
        
        # Define full-text indexes
        self.fulltext_indexes = [
            {
                "name": "memory_content_search",
                "type": "FULLTEXT",
                "query": "CREATE FULLTEXT INDEX memory_content_search IF NOT EXISTS FOR (m:Memory) ON EACH [m.content]"
            },
            {
                "name": "document_content_search",
                "type": "FULLTEXT",
                "query": "CREATE FULLTEXT INDEX document_content_search IF NOT EXISTS FOR (d:Document) ON EACH [d.filename, d.text]"
            },
            {
                "name": "entity_name_search",
                "type": "FULLTEXT",
                "query": "CREATE FULLTEXT INDEX entity_name_search IF NOT EXISTS FOR (e:Entity) ON EACH [e.name]"
            }
        ]
    
    def get_current_schema_info(self) -> Dict[str, Any]:
        """Get current database schema information."""
        try:
            # Get constraints
            constraints_query = """
            SHOW CONSTRAINTS 
            YIELD name, type, entityType, labelsOrTypes, properties, ownedIndex
            RETURN name, type, entityType, labelsOrTypes, properties, ownedIndex
            ORDER BY name
            """
            constraints = neo4j_production.execute_query(constraints_query)
            
            # Get indexes
            indexes_query = """
            SHOW INDEXES 
            YIELD name, type, state, populationPercent, uniqueness, entityType, labelsOrTypes, properties
            RETURN name, type, state, populationPercent, uniqueness, entityType, labelsOrTypes, properties
            ORDER BY name
            """
            indexes = neo4j_production.execute_query(indexes_query)
            
            return {
                "schema_version": self.current_schema_version,
                "timestamp": datetime.now().isoformat(),
                "constraints": constraints,
                "indexes": indexes,
                "constraint_count": len(constraints),
                "index_count": len(indexes)
            }
            
        except Exception as e:
            logger.error(f"Failed to get schema info: {e}")
            return {"error": str(e)}
    
    def validate_schema(self) -> Dict[str, Any]:
        """Validate current schema against requirements."""
        validation_results = {
            "valid": True,
            "missing_constraints": [],
            "missing_indexes": [],
            "failed_indexes": [],
            "recommendations": []
        }
        
        try:
            current_schema = self.get_current_schema_info()
            
            if "error" in current_schema:
                validation_results["valid"] = False
                validation_results["error"] = current_schema["error"]
                return validation_results
            
            # Check constraints
            existing_constraints = {c["name"] for c in current_schema["constraints"]}
            for required_constraint in self.required_constraints:
                if required_constraint["name"] not in existing_constraints:
                    validation_results["missing_constraints"].append(required_constraint["name"])
                    validation_results["valid"] = False
            
            # Check indexes
            existing_indexes = {idx["name"] for idx in current_schema["indexes"]}
            failed_indexes = {idx["name"] for idx in current_schema["indexes"] if idx["state"] == "FAILED"}
            
            # Check required indexes
            all_required_indexes = (
                self.required_indexes + 
                self.composite_indexes + 
                self.vector_indexes + 
                self.fulltext_indexes
            )
            
            for required_index in all_required_indexes:
                if required_index["name"] not in existing_indexes:
                    validation_results["missing_indexes"].append(required_index["name"])
                    validation_results["valid"] = False
            
            # Check for failed indexes
            validation_results["failed_indexes"] = list(failed_indexes)
            if failed_indexes:
                validation_results["valid"] = False
            
            # Generate recommendations
            if validation_results["missing_constraints"]:
                validation_results["recommendations"].append(
                    f"Create {len(validation_results['missing_constraints'])} missing constraints"
                )
            
            if validation_results["missing_indexes"]:
                validation_results["recommendations"].append(
                    f"Create {len(validation_results['missing_indexes'])} missing indexes"
                )
            
            if validation_results["failed_indexes"]:
                validation_results["recommendations"].append(
                    f"Rebuild {len(validation_results['failed_indexes'])} failed indexes"
                )
            
            # Check for vector index specifically
            if "ChunkEmbeddingIndex" in validation_results["missing_indexes"]:
                validation_results["recommendations"].append(
                    "CRITICAL: Create ChunkEmbeddingIndex for vector search functionality"
                )
            
            return validation_results
            
        except Exception as e:
            logger.error(f"Schema validation failed: {e}")
            return {
                "valid": False,
                "error": str(e),
                "missing_constraints": [],
                "missing_indexes": [],
                "failed_indexes": [],
                "recommendations": ["Fix schema validation error"]
            }
    
    def create_missing_schema_elements(self) -> Dict[str, Any]:
        """Create missing constraints and indexes."""
        results = {
            "constraints_created": [],
            "indexes_created": [],
            "errors": [],
            "success": True
        }
        
        try:
            validation = self.validate_schema()
            
            # Create missing constraints
            for constraint in self.required_constraints:
                if constraint["name"] in validation["missing_constraints"]:
                    try:
                        neo4j_production.execute_write_query(constraint["query"])
                        results["constraints_created"].append(constraint["name"])
                        logger.info(f"Created constraint: {constraint['name']}")
                    except Exception as e:
                        error_msg = f"Failed to create constraint {constraint['name']}: {e}"
                        results["errors"].append(error_msg)
                        logger.error(error_msg)
                        results["success"] = False
            
            # Create missing indexes
            all_indexes = (
                self.required_indexes + 
                self.composite_indexes + 
                self.vector_indexes + 
                self.fulltext_indexes
            )
            
            for index in all_indexes:
                if index["name"] in validation["missing_indexes"]:
                    try:
                        neo4j_production.execute_write_query(index["query"])
                        results["indexes_created"].append(index["name"])
                        logger.info(f"Created index: {index['name']}")
                    except Exception as e:
                        error_msg = f"Failed to create index {index['name']}: {e}"
                        results["errors"].append(error_msg)
                        logger.error(error_msg)
                        results["success"] = False
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to create schema elements: {e}")
            return {
                "constraints_created": [],
                "indexes_created": [],
                "errors": [str(e)],
                "success": False
            }
    
    def rebuild_failed_indexes(self) -> Dict[str, Any]:
        """Rebuild failed indexes."""
        results = {
            "indexes_rebuilt": [],
            "errors": [],
            "success": True
        }
        
        try:
            current_schema = self.get_current_schema_info()
            failed_indexes = [idx for idx in current_schema["indexes"] if idx["state"] == "FAILED"]
            
            for failed_index in failed_indexes:
                try:
                    # Drop the failed index
                    drop_query = f"DROP INDEX {failed_index['name']} IF EXISTS"
                    neo4j_production.execute_write_query(drop_query)
                    
                    # Find the corresponding index definition and recreate
                    all_indexes = (
                        self.required_indexes + 
                        self.composite_indexes + 
                        self.vector_indexes + 
                        self.fulltext_indexes
                    )
                    
                    for index_def in all_indexes:
                        if index_def["name"] == failed_index["name"]:
                            neo4j_production.execute_write_query(index_def["query"])
                            results["indexes_rebuilt"].append(failed_index["name"])
                            logger.info(f"Rebuilt index: {failed_index['name']}")
                            break
                    
                except Exception as e:
                    error_msg = f"Failed to rebuild index {failed_index['name']}: {e}"
                    results["errors"].append(error_msg)
                    logger.error(error_msg)
                    results["success"] = False
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to rebuild indexes: {e}")
            return {
                "indexes_rebuilt": [],
                "errors": [str(e)],
                "success": False
            }
    
    def initialize_schema(self) -> Dict[str, Any]:
        """Initialize complete database schema."""
        logger.info("Initializing Neo4j database schema...")
        
        results = {
            "schema_validation": {},
            "creation_results": {},
            "rebuild_results": {},
            "final_validation": {},
            "success": True
        }
        
        try:
            # Step 1: Validate current schema
            results["schema_validation"] = self.validate_schema()
            
            # Step 2: Create missing elements
            if not results["schema_validation"]["valid"]:
                results["creation_results"] = self.create_missing_schema_elements()
                if not results["creation_results"]["success"]:
                    results["success"] = False
            
            # Step 3: Rebuild failed indexes
            if results["schema_validation"]["failed_indexes"]:
                results["rebuild_results"] = self.rebuild_failed_indexes()
                if not results["rebuild_results"]["success"]:
                    results["success"] = False
            
            # Step 4: Final validation
            results["final_validation"] = self.validate_schema()
            if not results["final_validation"]["valid"]:
                results["success"] = False
            
            if results["success"]:
                logger.info("Schema initialization completed successfully")
            else:
                logger.error("Schema initialization completed with errors")
            
            return results
            
        except Exception as e:
            logger.error(f"Schema initialization failed: {e}")
            return {
                "schema_validation": {},
                "creation_results": {},
                "rebuild_results": {},
                "final_validation": {},
                "success": False,
                "error": str(e)
            }
    
    def get_schema_health_report(self) -> Dict[str, Any]:
        """Generate comprehensive schema health report."""
        try:
            current_schema = self.get_current_schema_info()
            validation = self.validate_schema()
            
            # Calculate health score
            total_required = (
                len(self.required_constraints) + 
                len(self.required_indexes) + 
                len(self.composite_indexes) + 
                len(self.vector_indexes) + 
                len(self.fulltext_indexes)
            )
            
            missing_count = len(validation["missing_constraints"]) + len(validation["missing_indexes"])
            failed_count = len(validation["failed_indexes"])
            
            health_score = max(0, (total_required - missing_count - failed_count) / total_required * 100)
            
            return {
                "timestamp": datetime.now().isoformat(),
                "schema_version": self.current_schema_version,
                "health_score": round(health_score, 2),
                "status": "healthy" if validation["valid"] else "needs_attention",
                "current_schema": current_schema,
                "validation": validation,
                "recommendations": validation["recommendations"]
            }
            
        except Exception as e:
            logger.error(f"Failed to generate schema health report: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "health_score": 0,
                "status": "error",
                "error": str(e)
            }

# Global schema manager instance
schema_manager = SchemaManager()

# Convenience functions
def validate_schema() -> Dict[str, Any]:
    """Validate database schema."""
    return schema_manager.validate_schema()

def initialize_schema() -> Dict[str, Any]:
    """Initialize database schema."""
    return schema_manager.initialize_schema()

def get_schema_health() -> Dict[str, Any]:
    """Get schema health report."""
    return schema_manager.get_schema_health_report()
