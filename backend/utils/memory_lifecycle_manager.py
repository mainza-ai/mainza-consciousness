"""
Memory Lifecycle Management

This module handles the lifecycle of memories including importance decay,
cleanup, archival, consolidation, and optimization routines.
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import logging
import math
from collections import defaultdict

try:
    from dateutil import parser as date_parser
    DATEUTIL_AVAILABLE = True
except ImportError:
    DATEUTIL_AVAILABLE = False

from .neo4j_enhanced import Neo4jManager
from .embedding_enhanced import EmbeddingManager

logger = logging.getLogger(__name__)

@dataclass
class MemoryCleanupStats:
    """Statistics from memory cleanup operations"""
    total_memories_processed: int = 0
    memories_archived: int = 0
    memories_deleted: int = 0
    memories_consolidated: int = 0
    storage_freed_mb: float = 0.0
    processing_time_seconds: float = 0.0

@dataclass
class MemoryConsolidationResult:
    """Result of memory consolidation operation"""
    original_memory_ids: List[str]
    consolidated_memory_id: str
    similarity_score: float
    content_merged: str

class MemoryLifecycleManager:
    """
    Manages the complete lifecycle of memories including decay, cleanup,
    consolidation, and optimization.
    """
    
    def __init__(self):
        self.neo4j_manager = Neo4jManager()
        self.embedding_manager = EmbeddingManager()
        
        # Lifecycle configuration
        self.config = {
            # Importance decay settings
            'base_decay_rate': 0.95,           # Daily decay multiplier
            'min_importance_threshold': 0.1,   # Minimum importance before cleanup
            'access_boost_factor': 1.2,        # Boost for accessed memories
            'consciousness_boost_factor': 1.5, # Boost for high consciousness memories
            
            # Cleanup settings
            'max_memory_age_days': 365,        # Maximum age before archival
            'cleanup_batch_size': 1000,        # Memories to process per batch
            'low_importance_threshold': 0.2,   # Threshold for low importance cleanup
            'storage_limit_mb': 10000,         # Storage limit before aggressive cleanup
            
            # Consolidation settings
            'similarity_threshold': 0.85,      # Minimum similarity for consolidation
            'consolidation_batch_size': 100,   # Memories to check per consolidation batch
            'min_consolidation_age_hours': 24, # Minimum age before consolidation
            
            # Optimization settings
            'optimization_interval_hours': 24, # How often to run optimization
            'access_frequency_window_days': 30, # Window for access frequency calculation
        }
        
        # Tracking
        self.last_cleanup_time = None
        self.last_consolidation_time = None
        self.last_optimization_time = None
        
        # Background task management
        self._lifecycle_active = False
        self._lifecycle_task = None
    
    async def initialize(self) -> bool:
        """Initialize the memory lifecycle manager"""
        try:
            # Test Neo4j connectivity
            test_result = self.neo4j_manager.execute_query(
                "RETURN 1 as test",
                {}
            )
            
            if not test_result:
                logger.error("Failed to connect to Neo4j for lifecycle management")
                return False
            
            logger.info("Memory lifecycle manager initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize memory lifecycle manager: {e}")
            return False
    
    async def start_lifecycle_management(self):
        """Start background lifecycle management"""
        if self._lifecycle_active:
            logger.warning("Memory lifecycle management already active")
            return
        
        self._lifecycle_active = True
        self._lifecycle_task = asyncio.create_task(self._lifecycle_loop())
        logger.info("Memory lifecycle management started")
    
    async def stop_lifecycle_management(self):
        """Stop background lifecycle management"""
        self._lifecycle_active = False
        if self._lifecycle_task:
            self._lifecycle_task.cancel()
            try:
                await self._lifecycle_task
            except asyncio.CancelledError:
                pass
        logger.info("Memory lifecycle management stopped")
    
    async def _lifecycle_loop(self):
        """Background lifecycle management loop"""
        while self._lifecycle_active:
            try:
                # Run daily maintenance tasks
                await self.run_daily_maintenance()
                
                # Sleep for 1 hour before next check
                await asyncio.sleep(3600)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in lifecycle management loop: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes before retrying
    
    async def run_daily_maintenance(self) -> Dict[str, Any]:
        """Run daily memory maintenance tasks"""
        start_time = time.time()
        maintenance_results = {
            'decay_results': None,
            'cleanup_results': None,
            'consolidation_results': None,
            'optimization_results': None
        }
        
        try:
            logger.info("Starting daily memory maintenance")
            
            # 1. Apply importance decay
            maintenance_results['decay_results'] = await self.apply_importance_decay()
            
            # 2. Run memory cleanup
            maintenance_results['cleanup_results'] = await self.cleanup_low_importance_memories()
            
            # 3. Consolidate similar memories (less frequent)
            if self._should_run_consolidation():
                maintenance_results['consolidation_results'] = await self.consolidate_similar_memories()
            
            # 4. Run optimization routines
            maintenance_results['optimization_results'] = await self.optimize_memory_storage()
            
            processing_time = time.time() - start_time
            logger.info(f"Daily memory maintenance completed in {processing_time:.2f} seconds")
            
            return maintenance_results
            
        except Exception as e:
            logger.error(f"Daily maintenance failed: {e}")
            return maintenance_results
    
    async def apply_importance_decay(self) -> Dict[str, Any]:
        """Apply time-based importance decay to all memories"""
        try:
            logger.info("Applying importance decay to memories")
            
            # Get all memories that need decay update
            memories_query = """
            MATCH (m:Memory)
            WHERE m.created_at IS NOT NULL
            RETURN m.memory_id as memory_id, 
                   m.importance_score as current_importance,
                   m.created_at as created_at,
                   m.last_accessed as last_accessed,
                   m.access_count as access_count,
                   m.consciousness_level as consciousness_level,
                   m.decay_rate as decay_rate
            """
            
            memories = self.neo4j_manager.execute_query(memories_query, {})
            
            if not memories:
                return {'memories_processed': 0, 'average_decay': 0}
            
            updates = []
            total_decay = 0
            
            for memory in memories:
                # Calculate new importance score
                new_importance = self._calculate_decayed_importance(memory)
                
                current_importance = memory.get('current_importance', 0.5) or 0.5
                if new_importance != current_importance:
                    updates.append({
                        'memory_id': memory['memory_id'],
                        'new_importance': new_importance
                    })
                    
                    decay_amount = current_importance - new_importance
                    total_decay += decay_amount
            
            # Batch update importance scores
            if updates:
                update_query = """
                UNWIND $updates as update
                MATCH (m:Memory {memory_id: update.memory_id})
                SET m.importance_score = update.new_importance,
                    m.last_decay_update = datetime()
                """
                
                self.neo4j_manager.execute_query(update_query, {'updates': updates})
            
            average_decay = total_decay / len(updates) if updates else 0
            
            logger.info(f"Applied decay to {len(updates)} memories, average decay: {average_decay:.4f}")
            
            return {
                'memories_processed': len(memories),
                'memories_updated': len(updates),
                'average_decay': average_decay
            }
            
        except Exception as e:
            logger.error(f"Failed to apply importance decay: {e}")
            return {'error': str(e)}
    
    def _calculate_decayed_importance(self, memory: Dict[str, Any]) -> float:
        """Calculate decayed importance score for a memory"""
        try:
            current_importance = memory.get('current_importance', 0.5)
            if current_importance is None:
                current_importance = 0.5
            
            created_at_str = memory.get('created_at')
            if not created_at_str:
                return current_importance
            
            # Handle different datetime formats
            if isinstance(created_at_str, str):
                # Remove timezone info if present and parse
                created_at_str = created_at_str.replace('Z', '+00:00')
                if ('+' in created_at_str or created_at_str.endswith('Z')) and DATEUTIL_AVAILABLE:
                    created_at = date_parser.parse(created_at_str).replace(tzinfo=None)
                else:
                    try:
                        created_at = datetime.fromisoformat(created_at_str)
                    except ValueError:
                        # Fallback for different formats
                        created_at = datetime.utcnow()
            else:
                created_at = datetime.utcnow()  # Fallback
            
            last_accessed = memory.get('last_accessed')
            access_count = memory.get('access_count', 0) or 0
            consciousness_level = memory.get('consciousness_level', 0.5) or 0.5
            decay_rate = memory.get('decay_rate', self.config['base_decay_rate']) or self.config['base_decay_rate']
            
            # Calculate age in days
            age_days = (datetime.utcnow() - created_at).days
            
            # Base decay calculation
            if decay_rate and age_days >= 0:
                decayed_importance = current_importance * (decay_rate ** age_days)
            else:
                decayed_importance = current_importance
            
            # Apply access boost
            if access_count and access_count > 0:
                access_boost = min(1.5, 1 + (access_count * 0.1))
                decayed_importance *= access_boost
            
            # Apply consciousness boost for high-consciousness memories
            if consciousness_level and consciousness_level > 0.7:
                consciousness_boost = self.config['consciousness_boost_factor']
                if consciousness_boost:
                    decayed_importance *= consciousness_boost
            
            # Apply recent access boost
            if last_accessed:
                try:
                    if isinstance(last_accessed, str):
                        last_accessed = last_accessed.replace('Z', '+00:00')
                        if ('+' in last_accessed or last_accessed.endswith('Z')) and DATEUTIL_AVAILABLE:
                            last_access_date = date_parser.parse(last_accessed).replace(tzinfo=None)
                        else:
                            try:
                                last_access_date = datetime.fromisoformat(last_accessed)
                            except ValueError:
                                last_access_date = datetime.utcnow()
                    else:
                        last_access_date = datetime.utcnow()
                    
                    days_since_access = (datetime.utcnow() - last_access_date).days
                    
                    if days_since_access < 7:  # Accessed within a week
                        recent_access_boost = self.config['access_boost_factor']
                        decayed_importance *= recent_access_boost
                except Exception:
                    # Skip access boost if date parsing fails
                    pass
            
            # Ensure importance doesn't exceed 1.0 or go below 0
            return max(0.0, min(1.0, decayed_importance))
            
        except Exception as e:
            logger.error(f"Error calculating decayed importance: {e}")
            return memory.get('current_importance', 0.5)
    
    async def cleanup_low_importance_memories(self) -> MemoryCleanupStats:
        """Clean up memories with low importance scores"""
        stats = MemoryCleanupStats()
        start_time = time.time()
        
        try:
            logger.info("Starting cleanup of low importance memories")
            
            # Find memories eligible for cleanup
            cleanup_query = """
            MATCH (m:Memory)
            WHERE m.importance_score < $threshold
            AND m.memory_type <> 'consciousness_reflection'  // Preserve consciousness memories
            RETURN m.memory_id as memory_id,
                   m.importance_score as importance,
                   m.created_at as created_at,
                   size(m.content) as content_size
            ORDER BY m.importance_score ASC
            LIMIT $batch_size
            """
            
            memories_to_cleanup = self.neo4j_manager.execute_query(
                cleanup_query,
                {
                    'threshold': self.config['low_importance_threshold'],
                    'batch_size': self.config['cleanup_batch_size']
                }
            )
            
            if not memories_to_cleanup:
                logger.info("No memories found for cleanup")
                return stats
            
            stats.total_memories_processed = len(memories_to_cleanup)
            
            # Separate into archive vs delete based on age and importance
            memories_to_archive = []
            memories_to_delete = []
            
            for memory in memories_to_cleanup:
                created_at = datetime.fromisoformat(memory['created_at'])
                age_days = (datetime.utcnow() - created_at).days
                
                # Very low importance or very old -> delete
                if (memory['importance'] < self.config['min_importance_threshold'] or 
                    age_days > self.config['max_memory_age_days']):
                    memories_to_delete.append(memory)
                else:
                    memories_to_archive.append(memory)
            
            # Archive memories (mark as archived, don't delete)
            if memories_to_archive:
                archive_ids = [m['memory_id'] for m in memories_to_archive]
                archive_query = """
                MATCH (m:Memory)
                WHERE m.memory_id IN $memory_ids
                SET m.archived = true,
                    m.archived_at = datetime(),
                    m.importance_score = 0.0
                """
                
                self.neo4j_manager.execute_query(
                    archive_query,
                    {'memory_ids': archive_ids}
                )
                
                stats.memories_archived = len(memories_to_archive)
                logger.info(f"Archived {stats.memories_archived} low importance memories")
            
            # Delete very low importance memories
            if memories_to_delete:
                delete_ids = [m['memory_id'] for m in memories_to_delete]
                
                # Calculate storage freed
                total_content_size = sum(m.get('content_size', 0) for m in memories_to_delete)
                stats.storage_freed_mb = total_content_size / (1024 * 1024)
                
                delete_query = """
                MATCH (m:Memory)
                WHERE m.memory_id IN $memory_ids
                DETACH DELETE m
                """
                
                self.neo4j_manager.execute_query(
                    delete_query,
                    {'memory_ids': delete_ids}
                )
                
                stats.memories_deleted = len(memories_to_delete)
                logger.info(f"Deleted {stats.memories_deleted} very low importance memories")
            
            stats.processing_time_seconds = time.time() - start_time
            self.last_cleanup_time = datetime.utcnow()
            
            return stats
            
        except Exception as e:
            logger.error(f"Memory cleanup failed: {e}")
            stats.processing_time_seconds = time.time() - start_time
            return stats
    
    async def consolidate_similar_memories(self) -> Dict[str, Any]:
        """Consolidate similar memories to reduce redundancy"""
        try:
            logger.info("Starting memory consolidation")
            
            # Find memories eligible for consolidation
            consolidation_query = """
            MATCH (m:Memory)
            WHERE m.created_at < datetime() - duration('PT24H')  // At least 24 hours old
            AND m.archived IS NULL OR m.archived = false
            AND m.memory_type = 'interaction'  // Only consolidate interaction memories
            RETURN m.memory_id as memory_id,
                   m.content as content,
                   m.embedding as embedding,
                   m.user_id as user_id,
                   m.created_at as created_at,
                   m.importance_score as importance
            ORDER BY m.created_at DESC
            LIMIT $batch_size
            """
            
            memories = self.neo4j_manager.execute_query(
                consolidation_query,
                {'batch_size': self.config['consolidation_batch_size']}
            )
            
            if not memories or len(memories) < 2:
                return {'consolidations_performed': 0, 'message': 'Insufficient memories for consolidation'}
            
            consolidations = []
            processed_ids = set()
            
            # Group memories by user for consolidation
            user_memories = defaultdict(list)
            for memory in memories:
                if memory['memory_id'] not in processed_ids:
                    user_memories[memory['user_id']].append(memory)
            
            # Find similar memories within each user's memories
            for user_id, user_memory_list in user_memories.items():
                if len(user_memory_list) < 2:
                    continue
                
                # Compare memories pairwise
                for i in range(len(user_memory_list)):
                    if user_memory_list[i]['memory_id'] in processed_ids:
                        continue
                    
                    similar_memories = [user_memory_list[i]]
                    
                    for j in range(i + 1, len(user_memory_list)):
                        if user_memory_list[j]['memory_id'] in processed_ids:
                            continue
                        
                        # Calculate similarity
                        similarity = await self._calculate_memory_similarity(
                            user_memory_list[i],
                            user_memory_list[j]
                        )
                        
                        if similarity >= self.config['similarity_threshold']:
                            similar_memories.append(user_memory_list[j])
                    
                    # Consolidate if we found similar memories
                    if len(similar_memories) > 1:
                        consolidation_result = await self._consolidate_memory_group(similar_memories)
                        if consolidation_result:
                            consolidations.append(consolidation_result)
                            processed_ids.update(consolidation_result.original_memory_ids)
            
            self.last_consolidation_time = datetime.utcnow()
            
            logger.info(f"Completed memory consolidation: {len(consolidations)} consolidations performed")
            
            return {
                'consolidations_performed': len(consolidations),
                'memories_processed': len(memories),
                'consolidation_details': [
                    {
                        'original_count': len(c.original_memory_ids),
                        'similarity_score': c.similarity_score
                    } for c in consolidations
                ]
            }
            
        except Exception as e:
            logger.error(f"Memory consolidation failed: {e}")
            return {'error': str(e)}
    
    async def _calculate_memory_similarity(self, memory1: Dict[str, Any], memory2: Dict[str, Any]) -> float:
        """Calculate similarity between two memories"""
        try:
            # Use embeddings if available
            if memory1.get('embedding') and memory2.get('embedding'):
                embedding1 = memory1['embedding']
                embedding2 = memory2['embedding']
                
                # Calculate cosine similarity
                dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
                magnitude1 = math.sqrt(sum(a * a for a in embedding1))
                magnitude2 = math.sqrt(sum(a * a for a in embedding2))
                
                if magnitude1 > 0 and magnitude2 > 0:
                    return dot_product / (magnitude1 * magnitude2)
            
            # Fallback to text similarity
            content1 = memory1.get('content', '').lower()
            content2 = memory2.get('content', '').lower()
            
            # Simple word overlap similarity
            words1 = set(content1.split())
            words2 = set(content2.split())
            
            if not words1 or not words2:
                return 0.0
            
            intersection = len(words1.intersection(words2))
            union = len(words1.union(words2))
            
            return intersection / union if union > 0 else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating memory similarity: {e}")
            return 0.0
    
    async def _consolidate_memory_group(self, memories: List[Dict[str, Any]]) -> Optional[MemoryConsolidationResult]:
        """Consolidate a group of similar memories into one"""
        try:
            if len(memories) < 2:
                return None
            
            # Sort by importance and recency
            memories.sort(key=lambda m: (m['importance'], m['created_at']), reverse=True)
            
            # Use the most important memory as the base
            base_memory = memories[0]
            other_memories = memories[1:]
            
            # Merge content
            merged_content = base_memory['content']
            for memory in other_memories:
                if memory['content'] not in merged_content:
                    merged_content += f"\n[Related: {memory['content']}]"
            
            # Calculate average importance
            avg_importance = sum(m['importance'] for m in memories) / len(memories)
            
            # Update the base memory with consolidated information
            update_query = """
            MATCH (m:Memory {memory_id: $memory_id})
            SET m.content = $merged_content,
                m.importance_score = $avg_importance,
                m.consolidated = true,
                m.consolidated_from_count = $original_count,
                m.consolidated_at = datetime()
            """
            
            self.neo4j_manager.execute_query(
                update_query,
                {
                    'memory_id': base_memory['memory_id'],
                    'merged_content': merged_content,
                    'avg_importance': avg_importance,
                    'original_count': len(memories)
                }
            )
            
            # Delete the other memories
            other_ids = [m['memory_id'] for m in other_memories]
            if other_ids:
                delete_query = """
                MATCH (m:Memory)
                WHERE m.memory_id IN $memory_ids
                DETACH DELETE m
                """
                
                self.neo4j_manager.execute_query(
                    delete_query,
                    {'memory_ids': other_ids}
                )
            
            return MemoryConsolidationResult(
                original_memory_ids=[m['memory_id'] for m in memories],
                consolidated_memory_id=base_memory['memory_id'],
                similarity_score=0.9,  # Placeholder
                content_merged=merged_content
            )
            
        except Exception as e:
            logger.error(f"Error consolidating memory group: {e}")
            return None
    
    async def optimize_memory_storage(self) -> Dict[str, Any]:
        """Run memory storage optimization routines"""
        try:
            logger.info("Running memory storage optimization")
            
            optimization_results = {}
            
            # 1. Update access frequency tracking
            access_update_result = await self._update_access_frequencies()
            optimization_results['access_frequency_update'] = access_update_result
            
            # 2. Recompute importance scores based on recent activity
            importance_update_result = await self._recompute_importance_scores()
            optimization_results['importance_recomputation'] = importance_update_result
            
            # 3. Optimize Neo4j indexes and constraints
            index_optimization_result = await self._optimize_database_indexes()
            optimization_results['index_optimization'] = index_optimization_result
            
            self.last_optimization_time = datetime.utcnow()
            
            logger.info("Memory storage optimization completed")
            return optimization_results
            
        except Exception as e:
            logger.error(f"Memory storage optimization failed: {e}")
            return {'error': str(e)}
    
    async def _update_access_frequencies(self) -> Dict[str, Any]:
        """Update access frequency metrics for memories"""
        try:
            # Calculate access frequency over the configured window
            window_days = self.config['access_frequency_window_days']
            
            frequency_query = """
            MATCH (m:Memory)
            WHERE m.last_accessed IS NOT NULL
            AND m.last_accessed > datetime() - duration('P{window_days}D')
            WITH m, 
                 duration.between(m.created_at, datetime()).days as age_days,
                 coalesce(m.access_count, 0) as access_count
            SET m.access_frequency = CASE 
                WHEN age_days > 0 THEN toFloat(access_count) / age_days
                ELSE toFloat(access_count)
            END
            RETURN count(m) as updated_count
            """.format(window_days=window_days)
            
            result = self.neo4j_manager.execute_query(frequency_query, {})
            updated_count = result[0]['updated_count'] if result else 0
            
            return {'memories_updated': updated_count}
            
        except Exception as e:
            logger.error(f"Error updating access frequencies: {e}")
            return {'error': str(e)}
    
    async def _recompute_importance_scores(self) -> Dict[str, Any]:
        """Recompute importance scores based on current factors"""
        try:
            # Get memories that need importance recomputation
            recompute_query = """
            MATCH (m:Memory)
            WHERE m.last_importance_update IS NULL 
               OR m.last_importance_update < datetime() - duration('P7D')
            RETURN m.memory_id as memory_id,
                   m.importance_score as current_importance,
                   m.access_frequency as access_frequency,
                   m.consciousness_level as consciousness_level,
                   m.memory_type as memory_type
            LIMIT 1000
            """
            
            memories = self.neo4j_manager.execute_query(recompute_query, {})
            
            if not memories:
                return {'memories_updated': 0}
            
            updates = []
            for memory in memories:
                # Recompute importance based on multiple factors
                new_importance = self._compute_enhanced_importance(memory)
                current_importance = memory.get('current_importance', 0.5) or 0.5
                
                if abs(new_importance - current_importance) > 0.05:  # Significant change
                    updates.append({
                        'memory_id': memory['memory_id'],
                        'new_importance': new_importance
                    })
            
            # Batch update importance scores
            if updates:
                update_query = """
                UNWIND $updates as update
                MATCH (m:Memory {memory_id: update.memory_id})
                SET m.importance_score = update.new_importance,
                    m.last_importance_update = datetime()
                """
                
                self.neo4j_manager.execute_query(update_query, {'updates': updates})
            
            return {'memories_updated': len(updates)}
            
        except Exception as e:
            logger.error(f"Error recomputing importance scores: {e}")
            return {'error': str(e)}
    
    def _compute_enhanced_importance(self, memory: Dict[str, Any]) -> float:
        """Compute enhanced importance score based on multiple factors"""
        base_importance = memory.get('current_importance', 0.5) or 0.5
        access_frequency = memory.get('access_frequency', 0.0) or 0.0
        consciousness_level = memory.get('consciousness_level', 0.5) or 0.5
        memory_type = memory.get('memory_type', 'interaction') or 'interaction'
        
        # Base importance
        importance = base_importance
        
        # Access frequency boost
        if access_frequency and access_frequency > 0:
            frequency_boost = min(0.3, access_frequency * 0.1)
            importance += frequency_boost
        
        # Consciousness level boost
        if consciousness_level and consciousness_level > 0.7:
            consciousness_boost = (consciousness_level - 0.7) * 0.5
            importance += consciousness_boost
        
        # Memory type modifiers
        type_modifiers = {
            'consciousness_reflection': 1.2,
            'insight': 1.1,
            'interaction': 1.0,
            'health_check': 0.1
        }
        
        type_modifier = type_modifiers.get(memory_type, 1.0)
        importance *= type_modifier
        
        # Ensure importance stays within bounds
        return max(0.0, min(1.0, importance))
    
    async def _optimize_database_indexes(self) -> Dict[str, Any]:
        """Optimize Neo4j indexes for memory queries"""
        try:
            # Create or update indexes for common memory queries
            index_queries = [
                "CREATE INDEX memory_importance IF NOT EXISTS FOR (m:Memory) ON (m.importance_score)",
                "CREATE INDEX memory_created_at IF NOT EXISTS FOR (m:Memory) ON (m.created_at)",
                "CREATE INDEX memory_user_id IF NOT EXISTS FOR (m:Memory) ON (m.user_id)",
                "CREATE INDEX memory_type IF NOT EXISTS FOR (m:Memory) ON (m.memory_type)",
                "CREATE INDEX memory_archived IF NOT EXISTS FOR (m:Memory) ON (m.archived)"
            ]
            
            created_indexes = 0
            for query in index_queries:
                try:
                    self.neo4j_manager.execute_query(query, {})
                    created_indexes += 1
                except Exception as e:
                    # Index might already exist
                    logger.debug(f"Index creation skipped: {e}")
            
            return {'indexes_processed': created_indexes}
            
        except Exception as e:
            logger.error(f"Error optimizing database indexes: {e}")
            return {'error': str(e)}
    
    def _should_run_consolidation(self) -> bool:
        """Determine if consolidation should run based on timing"""
        if not self.last_consolidation_time:
            return True
        
        hours_since_last = (datetime.utcnow() - self.last_consolidation_time).total_seconds() / 3600
        return hours_since_last >= 168  # Run weekly
    
    async def get_lifecycle_status(self) -> Dict[str, Any]:
        """Get current lifecycle management status"""
        return {
            'lifecycle_active': self._lifecycle_active,
            'last_cleanup_time': self.last_cleanup_time.isoformat() if self.last_cleanup_time else None,
            'last_consolidation_time': self.last_consolidation_time.isoformat() if self.last_consolidation_time else None,
            'last_optimization_time': self.last_optimization_time.isoformat() if self.last_optimization_time else None,
            'configuration': self.config
        }

# Global lifecycle manager instance
memory_lifecycle_manager = MemoryLifecycleManager()