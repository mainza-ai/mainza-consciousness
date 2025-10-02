"""
Unified Database Manager for Mainza AI
Consolidates all database managers into a single, unified system

This module provides the definitive database manager that:
- Consolidates all 4 Neo4j managers into a single unified system
- Ensures consistent data access across all database operations
- Implements unified transaction management
- Provides single source of truth for all database operations
- Integrates seamlessly with all backend systems

Author: Mainza AI Consciousness Team
Date: 2025-10-01
"""

import logging
import asyncio
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timezone
from neo4j import GraphDatabase, AsyncGraphDatabase
from neo4j.exceptions import ServiceUnavailable, AuthError, ConfigurationError
import json
import os
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

class UnifiedDatabaseManager:
    """
    Unified Database Manager
    
    Consolidates all database operations into a single, consistent interface.
    This replaces all separate Neo4j managers with a unified system.
    """
    
    def __init__(self):
        """Initialize the unified database manager"""
        self.driver = None
        self.session = None
        self.connection_status = "disconnected"
        self.connection_retry_count = 0
        self.max_retry_attempts = 5
        self.retry_delay = 1  # seconds
        
        # Database configuration
        self.neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        self.neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
        self.neo4j_password = os.getenv('NEO4J_PASSWORD', 'password')
        self.neo4j_database = os.getenv('NEO4J_DATABASE', 'neo4j')
        
        # Performance settings
        self.connection_timeout = 30
        self.max_connection_lifetime = 3600  # 1 hour
        self.max_connection_pool_size = 50
        
        # Initialize connection
        asyncio.create_task(self._initialize_connection())
    
    async def _initialize_connection(self):
        """Initialize database connection with retry logic"""
        try:
            # Create async driver
            self.driver = AsyncGraphDatabase.driver(
                self.neo4j_uri,
                auth=(self.neo4j_user, self.neo4j_password),
                max_connection_lifetime=self.max_connection_lifetime,
                max_connection_pool_size=self.max_connection_pool_size,
                connection_timeout=self.connection_timeout
            )
            
            # Test connection
            async with self.driver.session(database=self.neo4j_database) as session:
                result = await session.run("RETURN 1 as test")
                await result.consume()
            
            self.connection_status = "connected"
            self.connection_retry_count = 0
            logger.info("✅ Unified database connection established successfully")
            
        except Exception as e:
            self.connection_status = "failed"
            self.connection_retry_count += 1
            logger.error(f"❌ Database connection failed (attempt {self.connection_retry_count}): {e}")
            
            if self.connection_retry_count < self.max_retry_attempts:
                logger.info(f"🔄 Retrying database connection in {self.retry_delay} seconds...")
                await asyncio.sleep(self.retry_delay)
                await self._initialize_connection()
            else:
                logger.error("❌ Max retry attempts reached. Database connection failed.")
    
    @asynccontextmanager
    async def get_session(self, database: str = None):
        """Get database session with proper error handling"""
        if not self.driver:
            raise Exception("Database driver not initialized")
        
        database = database or self.neo4j_database
        session = None
        
        try:
            session = self.driver.session(database=database)
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            raise
        finally:
            if session:
                await session.close()
    
    async def execute_query(self, query: str, parameters: Dict[str, Any] = None, database: str = None) -> List[Dict[str, Any]]:
        """
        Execute a Cypher query with unified error handling
        
        Args:
            query: Cypher query string
            parameters: Query parameters
            database: Database name (defaults to configured database)
            
        Returns:
            List of result records
        """
        try:
            async with self.get_session(database) as session:
                result = await session.run(query, parameters or {})
                records = await result.data()
                return records
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    async def execute_write_query(self, query: str, parameters: Dict[str, Any] = None, database: str = None) -> Dict[str, Any]:
        """
        Execute a write query with unified error handling
        
        Args:
            query: Cypher query string
            parameters: Query parameters
            database: Database name
            
        Returns:
            Query execution result
        """
        try:
            async with self.get_session(database) as session:
                result = await session.run(query, parameters or {})
                summary = await result.consume()
                return {
                    "nodes_created": summary.counters.nodes_created,
                    "nodes_deleted": summary.counters.nodes_deleted,
                    "relationships_created": summary.counters.relationships_created,
                    "relationships_deleted": summary.counters.relationships_deleted,
                    "properties_set": summary.counters.properties_set,
                    "labels_added": summary.counters.labels_added,
                    "labels_removed": summary.counters.labels_removed
                }
        except Exception as e:
            logger.error(f"Write query execution failed: {e}")
            raise
    
    # ============================================================================
    # CONSCIOUSNESS DATA OPERATIONS
    # ============================================================================
    
    async def get_consciousness_state(self, state_id: str = None) -> Optional[Dict[str, Any]]:
        """Get consciousness state from database"""
        try:
            if state_id:
                query = """
                MATCH (s:MainzaState {state_id: $state_id})
                RETURN s
                """
                parameters = {"state_id": state_id}
            else:
                query = """
                MATCH (s:MainzaState)
                RETURN s
                ORDER BY s.timestamp DESC
                LIMIT 1
                """
                parameters = {}
            
            records = await self.execute_query(query, parameters)
            if records:
                return records[0]["s"]
            return None
            
        except Exception as e:
            logger.error(f"Failed to get consciousness state: {e}")
            return None
    
    async def save_consciousness_state(self, state_data: Dict[str, Any]) -> bool:
        """Save consciousness state to database"""
        try:
            query = """
            MERGE (s:MainzaState {state_id: $state_id})
            SET s.consciousness_level = $consciousness_level,
                s.self_awareness_score = $self_awareness_score,
                s.emotional_depth = $emotional_depth,
                s.learning_rate = $learning_rate,
                s.evolution_level = $evolution_level,
                s.timestamp = datetime(),
                s.updated_at = datetime()
            RETURN s
            """
            
            result = await self.execute_write_query(query, state_data)
            return result["nodes_created"] > 0 or result["properties_set"] > 0
            
        except Exception as e:
            logger.error(f"Failed to save consciousness state: {e}")
            return False
    
    # ============================================================================
    # QUANTUM DATA OPERATIONS
    # ============================================================================
    
    async def get_quantum_state(self, state_id: str = None) -> Optional[Dict[str, Any]]:
        """Get quantum state from database"""
        try:
            if state_id:
                query = """
                MATCH (q:QuantumState {state_id: $state_id})
                RETURN q
                """
                parameters = {"state_id": state_id}
            else:
                query = """
                MATCH (q:QuantumState)
                RETURN q
                ORDER BY q.timestamp DESC
                LIMIT 1
                """
                parameters = {}
            
            records = await self.execute_query(query, parameters)
            if records:
                return records[0]["q"]
            return None
            
        except Exception as e:
            logger.error(f"Failed to get quantum state: {e}")
            return None
    
    async def save_quantum_state(self, state_data: Dict[str, Any]) -> bool:
        """Save quantum state to database"""
        try:
            query = """
            MERGE (q:QuantumState {state_id: $state_id})
            SET q.quantum_consciousness_level = $quantum_consciousness_level,
                q.quantum_coherence = $quantum_coherence,
                q.entanglement_strength = $entanglement_strength,
                q.superposition_states = $superposition_states,
                q.quantum_advantage = $quantum_advantage,
                q.quantum_processing_active = $quantum_processing_active,
                q.timestamp = datetime(),
                q.updated_at = datetime()
            RETURN q
            """
            
            result = await self.execute_write_query(query, state_data)
            return result["nodes_created"] > 0 or result["properties_set"] > 0
            
        except Exception as e:
            logger.error(f"Failed to save quantum state: {e}")
            return False
    
    # ============================================================================
    # MEMORY DATA OPERATIONS
    # ============================================================================
    
    async def get_memory(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """Get memory from database"""
        try:
            query = """
            MATCH (m:Memory {memory_id: $memory_id})
            RETURN m
            """
            parameters = {"memory_id": memory_id}
            
            records = await self.execute_query(query, parameters)
            if records:
                return records[0]["m"]
            return None
            
        except Exception as e:
            logger.error(f"Failed to get memory: {e}")
            return None
    
    async def save_memory(self, memory_data: Dict[str, Any]) -> bool:
        """Save memory to database"""
        try:
            query = """
            MERGE (m:Memory {memory_id: $memory_id})
            SET m.content = $content,
                m.importance = $importance,
                m.access_frequency = $access_frequency,
                m.last_importance_update = datetime(),
                m.updated_at = datetime(),
                m.created_at = COALESCE(m.created_at, datetime())
            RETURN m
            """
            
            result = await self.execute_write_query(query, memory_data)
            return result["nodes_created"] > 0 or result["properties_set"] > 0
            
        except Exception as e:
            logger.error(f"Failed to save memory: {e}")
            return False
    
    async def search_memories(self, search_query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search memories by content"""
        try:
            query = """
            MATCH (m:Memory)
            WHERE m.content CONTAINS $search_query
            RETURN m
            ORDER BY m.importance DESC, m.access_frequency DESC
            LIMIT $limit
            """
            parameters = {"search_query": search_query, "limit": limit}
            
            records = await self.execute_query(query, parameters)
            return [record["m"] for record in records]
            
        except Exception as e:
            logger.error(f"Failed to search memories: {e}")
            return []
    
    # ============================================================================
    # ENTITY DATA OPERATIONS
    # ============================================================================
    
    async def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get entity from database"""
        try:
            query = """
            MATCH (e:Entity {entity_id: $entity_id})
            RETURN e
            """
            parameters = {"entity_id": entity_id}
            
            records = await self.execute_query(query, parameters)
            if records:
                return records[0]["e"]
            return None
            
        except Exception as e:
            logger.error(f"Failed to get entity: {e}")
            return None
    
    async def save_entity(self, entity_data: Dict[str, Any]) -> bool:
        """Save entity to database"""
        try:
            query = """
            MERGE (e:Entity {entity_id: $entity_id})
            SET e.name = $name,
                e.type = $type,
                e.source = $source,
                e.updated_at = datetime(),
                e.created_at = COALESCE(e.created_at, datetime())
            RETURN e
            """
            
            result = await self.execute_write_query(query, entity_data)
            return result["nodes_created"] > 0 or result["properties_set"] > 0
            
        except Exception as e:
            logger.error(f"Failed to save entity: {e}")
            return False
    
    # ============================================================================
    # RELATIONSHIP OPERATIONS
    # ============================================================================
    
    async def create_relationship(self, from_node: str, to_node: str, relationship_type: str, properties: Dict[str, Any] = None) -> bool:
        """Create relationship between nodes"""
        try:
            query = f"""
            MATCH (a {{id: $from_node}}), (b {{id: $to_node}})
            CREATE (a)-[r:{relationship_type}]->(b)
            SET r += $properties
            RETURN r
            """
            parameters = {
                "from_node": from_node,
                "to_node": to_node,
                "properties": properties or {}
            }
            
            result = await self.execute_write_query(query, parameters)
            return result["relationships_created"] > 0
            
        except Exception as e:
            logger.error(f"Failed to create relationship: {e}")
            return False
    
    # ============================================================================
    # DATABASE HEALTH AND MAINTENANCE
    # ============================================================================
    
    def health_check(self) -> bool:
        """Synchronous health check for backward compatibility"""
        try:
            # Simple connectivity test
            with self.driver.session() as session:
                result = session.run("RETURN 1 as test")
                return result.single() is not None
        except Exception:
            return False
    
    async def get_database_health(self) -> Dict[str, Any]:
        """Get database health status"""
        try:
            # Test basic connectivity
            query = "RETURN 1 as test"
            await self.execute_query(query)
            
            # Get database statistics
            stats_query = """
            CALL apoc.meta.stats() YIELD nodeCount, relCount
            RETURN nodeCount, relCount
            """
            
            try:
                stats_records = await self.execute_query(stats_query)
                stats = stats_records[0] if stats_records else {}
            except:
                # Fallback if APOC is not available
                stats = {"nodeCount": 0, "relCount": 0}
            
            return {
                "status": "healthy",
                "connection_status": self.connection_status,
                "node_count": stats.get("nodeCount", 0),
                "relationship_count": stats.get("relCount", 0),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                "status": "unhealthy",
                "connection_status": self.connection_status,
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    
    async def cleanup_old_data(self, days_old: int = 30) -> Dict[str, int]:
        """Clean up old data from database"""
        try:
            cutoff_date = datetime.now(timezone.utc).timestamp() - (days_old * 24 * 60 * 60)
            
            # Clean up old memories
            memory_query = """
            MATCH (m:Memory)
            WHERE m.created_at < datetime({epochSeconds: $cutoff_date})
            DELETE m
            RETURN count(m) as deleted_count
            """
            
            memory_result = await self.execute_query(memory_query, {"cutoff_date": cutoff_date})
            deleted_memories = memory_result[0]["deleted_count"] if memory_result else 0
            
            # Clean up old states
            state_query = """
            MATCH (s:MainzaState)
            WHERE s.created_at < datetime({epochSeconds: $cutoff_date})
            DELETE s
            RETURN count(s) as deleted_count
            """
            
            state_result = await self.execute_query(state_query, {"cutoff_date": cutoff_date})
            deleted_states = state_result[0]["deleted_count"] if state_result else 0
            
            return {
                "deleted_memories": deleted_memories,
                "deleted_states": deleted_states,
                "total_deleted": deleted_memories + deleted_states
            }
            
        except Exception as e:
            logger.error(f"Data cleanup failed: {e}")
            return {"error": str(e)}
    
    # ============================================================================
    # TRANSACTION MANAGEMENT
    # ============================================================================
    
    @asynccontextmanager
    async def transaction(self, database: str = None):
        """Get database transaction with proper error handling"""
        if not self.driver:
            raise Exception("Database driver not initialized")
        
        database = database or self.neo4j_database
        session = None
        transaction = None
        
        try:
            session = self.driver.session(database=database)
            transaction = await session.begin_transaction()
            yield transaction
            await transaction.commit()
        except Exception as e:
            if transaction:
                await transaction.rollback()
            logger.error(f"Transaction error: {e}")
            raise
        finally:
            if session:
                await session.close()
    
    # ============================================================================
    # CONNECTION MANAGEMENT
    # ============================================================================
    
    async def close(self):
        """Close database connection"""
        try:
            if self.driver:
                await self.driver.close()
                self.connection_status = "disconnected"
                logger.info("✅ Database connection closed")
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")
    
    async def reconnect(self):
        """Reconnect to database"""
        try:
            await self.close()
            await self._initialize_connection()
        except Exception as e:
            logger.error(f"Reconnection failed: {e}")

# Create global unified database manager instance
unified_database_manager = UnifiedDatabaseManager()
