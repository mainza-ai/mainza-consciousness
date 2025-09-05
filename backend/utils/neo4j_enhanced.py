"""
Enhanced Neo4j connection utilities with connection pooling and transaction management.
Maintains backward compatibility with existing driver usage patterns.
"""
import os
import logging
from contextlib import contextmanager
from typing import Optional, Dict, Any, List
from neo4j import GraphDatabase, basic_auth, Session, Transaction
from neo4j.exceptions import ServiceUnavailable, TransientError
import time

logger = logging.getLogger(__name__)

class Neo4jManager:
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD")
        
        if not self.password:
            raise ValueError("NEO4J_PASSWORD environment variable is required")
        
        # Enhanced driver configuration
        self.driver = GraphDatabase.driver(
            self.uri, 
            auth=basic_auth(self.user, self.password),
            max_connection_lifetime=30 * 60,  # 30 minutes
            max_connection_pool_size=50,
            connection_acquisition_timeout=60,  # 60 seconds
            encrypted=False,  # Set to True for production
            trust="TRUST_ALL_CERTIFICATES"  # Configure properly for production
        )
        
    def close(self):
        """Close the driver connection."""
        if self.driver:
            self.driver.close()
    
    @contextmanager
    def get_session(self, database: Optional[str] = None):
        """Context manager for Neo4j sessions with proper cleanup."""
        session = None
        try:
            session = self.driver.session(database=database)
            yield session
        except ServiceUnavailable as e:
            logger.error(f"Neo4j service unavailable: {e}")
            raise
        except Exception as e:
            logger.error(f"Neo4j session error: {e}")
            raise
        finally:
            if session:
                session.close()
    
    @contextmanager
    def get_transaction(self, database: Optional[str] = None):
        """Context manager for Neo4j transactions with automatic rollback on error."""
        with self.get_session(database) as session:
            tx = session.begin_transaction()
            try:
                yield tx
                tx.commit()
            except Exception as e:
                tx.rollback()
                logger.error(f"Transaction rolled back due to error: {e}")
                raise
            finally:
                if tx.closed() is False:
                    tx.close()
    
    def execute_query(self, query: str, parameters: Optional[Dict[str, Any]] = None,
                     database: Optional[str] = None, retry_count: int = 3) -> List[Dict[str, Any]]:
        """Execute a query with retry logic and proper error handling."""
        parameters = parameters or {}

        for attempt in range(retry_count):
            try:
                with self.get_session(database) as session:
                    result = session.run(query, parameters)
                    return [dict(record) for record in result]
            except TransientError as e:
                if attempt < retry_count - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"Transient error on attempt {attempt + 1}, retrying in {wait_time}s: {e}")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error(f"Query failed after {retry_count} attempts: {e}")
                    raise
            except Exception as e:
                logger.error(f"Query execution error: {e}")
                raise

    async def execute_query_async(self, query: str, parameters: Optional[Dict[str, Any]] = None,
                                 database: Optional[str] = None, retry_count: int = 3) -> List[Dict[str, Any]]:
        """Execute a query asynchronously with retry logic and proper error handling."""
        parameters = parameters or {}

        for attempt in range(retry_count):
            try:
                with self.get_session(database) as session:
                    result = session.run(query, parameters)
                    return [dict(record) for record in result]
            except TransientError as e:
                if attempt < retry_count - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"Transient error on attempt {attempt + 1}, retrying in {wait_time}s: {e}")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    logger.error(f"Query failed after {retry_count} attempts: {e}")
                    raise
            except Exception as e:
                logger.error(f"Query execution error: {e}")
                raise

    def execute_write_query(self, query: str, parameters: Optional[Dict[str, Any]] = None,
                           database: Optional[str] = None) -> List[Dict[str, Any]]:
        """Execute a write query within a transaction."""
        parameters = parameters or {}

        with self.get_transaction(database) as tx:
            result = tx.run(query, parameters)
            return [dict(record) for record in result]

    async def execute_write_query_async(self, query: str, parameters: Optional[Dict[str, Any]] = None,
                                       database: Optional[str] = None) -> List[Dict[str, Any]]:
        """Execute a write query asynchronously within a transaction."""
        parameters = parameters or {}

        with self.get_transaction(database) as tx:
            result = tx.run(query, parameters)
            return [dict(record) for record in result]
    
    def health_check(self) -> bool:
        """Check if Neo4j is accessible."""
        try:
            with self.get_session() as session:
                result = session.run("RETURN 1 AS health")
                return result.single()["health"] == 1
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def get_database_info(self) -> Dict[str, Any]:
        """Get database information and statistics."""
        try:
            queries = {
                "node_count": "MATCH (n) RETURN count(n) AS count",
                "relationship_count": "MATCH ()-[r]->() RETURN count(r) AS count",
                "indexes": "SHOW INDEXES YIELD name, type, state RETURN name, type, state",
                "constraints": "SHOW CONSTRAINTS YIELD name, type RETURN name, type"
            }
            
            info = {}
            for key, query in queries.items():
                try:
                    result = self.execute_query(query)
                    info[key] = result
                except Exception as e:
                    logger.warning(f"Failed to get {key}: {e}")
                    info[key] = None
            
            return info
        except Exception as e:
            logger.error(f"Failed to get database info: {e}")
            return {}

# Global instance
neo4j_manager = Neo4jManager()

# Backward compatibility
driver = neo4j_manager.driver

# Cleanup on module exit
import atexit
atexit.register(neo4j_manager.close)
