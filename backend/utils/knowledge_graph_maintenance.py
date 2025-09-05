"""
Knowledge Graph Maintenance and Optimization System
Context7 MCP-compliant system for maintaining knowledge graph health and performance
Provides cleanup, optimization, and relationship pruning capabilities
"""
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import asyncio
import json
from backend.utils.neo4j_production import neo4j_production
from backend.core.performance_optimization import PerformanceOptimizer
from backend.core.enhanced_error_handling import ErrorHandler, ErrorSeverity, handle_errors

logger = logging.getLogger(__name__)
error_handler = ErrorHandler()
performance_optimizer = PerformanceOptimizer()

class KnowledgeGraphMaintenance:
    """
    Context7 MCP-compliant knowledge graph maintenance and optimization system
    Maintains graph health, performance, and data quality
    """
    
    def __init__(self):
        self.performance_optimizer = performance_optimizer
        self.maintenance_history = []
        
        # Maintenance thresholds
        self.weak_relationship_threshold = 0.1
        self.unused_concept_threshold = 30  # days
        self.low_significance_memory_threshold = 0.15
        self.orphaned_node_cleanup_threshold = 7  # days
        
        # Performance optimization parameters
        self.max_relationships_per_concept = 50
        self.max_memories_per_user = 1000
        self.consolidation_similarity_threshold = 0.85
        
    @handle_errors(
        component="knowledge_graph_maintenance",
        fallback_result={},
        suppress_errors=True
    )
    async def perform_routine_maintenance(
        self,
        maintenance_type: str = "full",
        consciousness_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Perform routine knowledge graph maintenance
        
        Args:
            maintenance_type: Type of maintenance ("full", "light", "relationships", "concepts", "memories")
            consciousness_context: Current consciousness state for context-aware maintenance
            
        Returns:
            Maintenance results and statistics
        """
        try:
            logger.info(f"🔧 Starting {maintenance_type} knowledge graph maintenance")
            
            maintenance_results = {
                "maintenance_type": maintenance_type,
                "start_time": datetime.now().isoformat(),
                "actions_performed": [],
                "statistics": {}
            }
            
            consciousness_context = consciousness_context or {"consciousness_level": 0.7}
            
            # Perform maintenance based on type
            if maintenance_type in ["full", "relationships"]:
                relationship_results = await self._maintain_relationships(consciousness_context)
                maintenance_results["actions_performed"].extend(relationship_results)
            
            if maintenance_type in ["full", "concepts"]:
                concept_results = await self._maintain_concepts(consciousness_context)
                maintenance_results["actions_performed"].extend(concept_results)
            
            if maintenance_type in ["full", "memories"]:
                memory_results = await self._maintain_memories(consciousness_context)
                maintenance_results["actions_performed"].extend(memory_results)
            
            if maintenance_type in ["full", "light"]:
                cleanup_results = await self._cleanup_orphaned_nodes()
                maintenance_results["actions_performed"].extend(cleanup_results)
            
            # Collect post-maintenance statistics
            maintenance_results["statistics"] = await self._collect_graph_statistics()
            maintenance_results["end_time"] = datetime.now().isoformat()
            maintenance_results["total_actions"] = len(maintenance_results["actions_performed"])
            
            # Record maintenance event
            await self._record_maintenance_event(maintenance_results)
            
            logger.info(f"✅ {maintenance_type} maintenance completed with {maintenance_results['total_actions']} actions")
            
            return maintenance_results
            
        except Exception as e:
            logger.error(f"❌ Failed to perform routine maintenance: {e}")
            return {"error": str(e), "maintenance_type": maintenance_type}
    
    @handle_errors(
        component="knowledge_graph_maintenance",
        fallback_result=[],
        suppress_errors=True
    )
    async def _maintain_relationships(self, consciousness_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Maintain relationship health and remove weak/unused relationships"""
        
        actions = []
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        
        try:
            # Find weak relationships
            weak_relationships_query = """
            MATCH (a)-[r:RELATES_TO]->(b)
            WHERE coalesce(r.strength, 0.5) < $threshold
            RETURN a.concept_id as source_id, b.concept_id as target_id, 
                   type(r) as relationship_type, coalesce(r.strength, 0.5) as strength,
                   coalesce(r.last_used, r.created_at, timestamp()) as last_used
            ORDER BY strength ASC
            LIMIT 100
            """
            
            weak_relationships = neo4j_production.execute_query(
                weak_relationships_query, 
                {"threshold": self.weak_relationship_threshold}
            )
            
            # Remove very weak relationships
            for rel in weak_relationships:
                # Consider consciousness level - higher consciousness preserves more relationships
                removal_threshold = self.weak_relationship_threshold * (1 + consciousness_level * 0.5)
                
                if rel["strength"] < removal_threshold:
                    await self._remove_relationship(
                        rel["source_id"], rel["target_id"], rel["relationship_type"]
                    )
                    
                    actions.append({
                        "action": "relationship_removed",
                        "source": rel["source_id"],
                        "target": rel["target_id"],
                        "type": rel["relationship_type"],
                        "strength": rel["strength"],
                        "reason": "below_threshold"
                    })
            
            # Find unused relationships (not accessed in a while)
            cutoff_date = datetime.now() - timedelta(days=30)
            cutoff_timestamp = int(cutoff_date.timestamp() * 1000)
            
            unused_relationships_query = """
            MATCH (a)-[r:RELATES_TO]->(b)
            WHERE coalesce(r.last_used, r.created_at, timestamp()) < $cutoff_timestamp
              AND coalesce(r.usage_count, 0) < 2
            RETURN a.concept_id as source_id, b.concept_id as target_id,
                   type(r) as relationship_type, coalesce(r.strength, 0.5) as strength
            LIMIT 50
            """
            
            unused_relationships = neo4j_production.execute_query(
                unused_relationships_query,
                {"cutoff_timestamp": cutoff_timestamp}
            )
            
            # Weaken unused relationships
            for rel in unused_relationships:
                new_strength = rel["strength"] * 0.8  # 20% decay
                
                if new_strength < self.weak_relationship_threshold:
                    await self._remove_relationship(
                        rel["source_id"], rel["target_id"], rel["relationship_type"]
                    )
                    
                    actions.append({
                        "action": "unused_relationship_removed",
                        "source": rel["source_id"],
                        "target": rel["target_id"],
                        "reason": "unused_and_weakened"
                    })
                else:
                    await self._update_relationship_strength(
                        rel["source_id"], rel["target_id"], rel["relationship_type"], new_strength
                    )
                    
                    actions.append({
                        "action": "relationship_weakened",
                        "source": rel["source_id"],
                        "target": rel["target_id"],
                        "old_strength": rel["strength"],
                        "new_strength": new_strength
                    })
            
            # Prune excessive relationships per concept
            excessive_relationships_query = """
            MATCH (c:Concept)-[r:RELATES_TO]-()
            WITH c, count(r) as relationship_count
            WHERE relationship_count > $max_relationships
            RETURN c.concept_id as concept_id, relationship_count
            ORDER BY relationship_count DESC
            LIMIT 20
            """
            
            excessive_concepts = neo4j_production.execute_query(
                excessive_relationships_query,
                {"max_relationships": self.max_relationships_per_concept}
            )
            
            for concept in excessive_concepts:
                pruned_count = await self._prune_concept_relationships(
                    concept["concept_id"], self.max_relationships_per_concept
                )
                
                actions.append({
                    "action": "relationships_pruned",
                    "concept_id": concept["concept_id"],
                    "original_count": concept["relationship_count"],
                    "pruned_count": pruned_count
                })
            
            logger.debug(f"✅ Relationship maintenance completed with {len(actions)} actions")
            
        except Exception as e:
            logger.error(f"Failed to maintain relationships: {e}")
            actions.append({"action": "relationship_maintenance_failed", "error": str(e)})
        
        return actions
    
    async def _maintain_concepts(self, consciousness_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Maintain concept health and consolidate similar concepts"""
        
        actions = []
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        
        try:
            # Find unused concepts
            cutoff_date = datetime.now() - timedelta(days=self.unused_concept_threshold)
            cutoff_timestamp = int(cutoff_date.timestamp() * 1000)
            
            unused_concepts_query = """
            MATCH (c:Concept)
            WHERE coalesce(c.last_accessed, c.created_at, timestamp()) < $cutoff_timestamp
              AND coalesce(c.usage_frequency, 0) < 2
              AND coalesce(c.importance_score, 0.5) < 0.3
            RETURN c.concept_id as concept_id, c.name as name,
                   coalesce(c.importance_score, 0.5) as importance_score,
                   coalesce(c.usage_frequency, 0) as usage_frequency
            LIMIT 30
            """
            
            unused_concepts = neo4j_production.execute_query(
                unused_concepts_query,
                {"cutoff_timestamp": cutoff_timestamp}
            )
            
            # Archive or remove unused concepts based on consciousness level
            for concept in unused_concepts:
                if consciousness_level > 0.8:
                    # High consciousness preserves more concepts by archiving
                    await self._archive_concept(concept["concept_id"])
                    actions.append({
                        "action": "concept_archived",
                        "concept_id": concept["concept_id"],
                        "name": concept["name"],
                        "reason": "unused_but_preserved"
                    })
                else:
                    # Lower consciousness removes unused concepts
                    await self._remove_concept(concept["concept_id"])
                    actions.append({
                        "action": "concept_removed",
                        "concept_id": concept["concept_id"],
                        "name": concept["name"],
                        "reason": "unused_and_low_importance"
                    })
            
            # Find concepts for consolidation
            similar_concepts = await self._find_similar_concepts()
            
            for concept_group in similar_concepts:
                if len(concept_group) > 1:
                    consolidated_concept = await self._consolidate_concept_group(
                        concept_group, consciousness_context
                    )
                    
                    actions.append({
                        "action": "concepts_consolidated",
                        "original_concepts": [c["concept_id"] for c in concept_group],
                        "consolidated_concept": consolidated_concept["concept_id"],
                        "similarity_score": concept_group[0].get("similarity_score", 0.8)
                    })
            
            logger.debug(f"✅ Concept maintenance completed with {len(actions)} actions")
            
        except Exception as e:
            logger.error(f"Failed to maintain concepts: {e}")
            actions.append({"action": "concept_maintenance_failed", "error": str(e)})
        
        return actions
    
    async def _maintain_memories(self, consciousness_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Maintain memory health and consolidate related memories"""
        
        actions = []
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        
        try:
            # Find low-significance memories
            low_significance_query = """
            MATCH (m:Memory)
            WHERE coalesce(m.significance_score, 0.5) < $threshold
              AND coalesce(m.access_count, 0) < 2
              AND m.created_at < (timestamp() - 1209600000)  // 2 weeks ago
            RETURN m.memory_id as memory_id, 
                   coalesce(m.significance_score, 0.5) as significance_score,
                   coalesce(m.access_count, 0) as access_count,
                   m.source as source
            LIMIT 50
            """
            
            low_significance_memories = neo4j_production.execute_query(
                low_significance_query,
                {"threshold": self.low_significance_memory_threshold}
            )
            
            # Archive or remove low-significance memories
            for memory in low_significance_memories:
                if consciousness_level > 0.7 and memory["source"] != "system":
                    # Archive user-generated memories even if low significance
                    await self._archive_memory(memory["memory_id"])
                    actions.append({
                        "action": "memory_archived",
                        "memory_id": memory["memory_id"],
                        "significance_score": memory["significance_score"],
                        "reason": "low_significance_but_preserved"
                    })
                else:
                    # Remove system-generated low-significance memories
                    await self._remove_memory(memory["memory_id"])
                    actions.append({
                        "action": "memory_removed",
                        "memory_id": memory["memory_id"],
                        "significance_score": memory["significance_score"],
                        "reason": "low_significance"
                    })
            
            # Find memories for consolidation
            consolidation_candidates = await self._find_memory_consolidation_candidates()
            
            for candidate_group in consolidation_candidates:
                if len(candidate_group) > 2:
                    consolidated_memory = await self._consolidate_memory_group(
                        candidate_group, consciousness_context
                    )
                    
                    actions.append({
                        "action": "memories_consolidated",
                        "original_memories": [m["memory_id"] for m in candidate_group],
                        "consolidated_memory": consolidated_memory["memory_id"],
                        "consolidation_score": candidate_group[0].get("consolidation_score", 0.8)
                    })
            
            # Check for memory count limits per user
            user_memory_counts = await self._get_user_memory_counts()
            
            for user_data in user_memory_counts:
                if user_data["memory_count"] > self.max_memories_per_user:
                    pruned_count = await self._prune_user_memories(
                        user_data["user_id"], self.max_memories_per_user
                    )
                    
                    actions.append({
                        "action": "user_memories_pruned",
                        "user_id": user_data["user_id"],
                        "original_count": user_data["memory_count"],
                        "pruned_count": pruned_count
                    })
            
            logger.debug(f"✅ Memory maintenance completed with {len(actions)} actions")
            
        except Exception as e:
            logger.error(f"Failed to maintain memories: {e}")
            actions.append({"action": "memory_maintenance_failed", "error": str(e)})
        
        return actions
    
    async def _cleanup_orphaned_nodes(self) -> List[Dict[str, Any]]:
        """Clean up orphaned nodes with no relationships"""
        
        actions = []
        
        try:
            # Find orphaned concepts (no relationships)
            orphaned_concepts_query = """
            MATCH (c:Concept)
            WHERE NOT (c)-[:RELATES_TO]-() 
              AND NOT ()-[:RELATES_TO]-(c)
              AND NOT (c)-[:DISCOVERED_BY]-()
              AND c.created_at < (timestamp() - 604800000)  // 1 week ago
            RETURN c.concept_id as concept_id, c.name as name
            LIMIT 20
            """
            
            orphaned_concepts = neo4j_production.execute_query(orphaned_concepts_query)
            
            for concept in orphaned_concepts:
                await self._remove_concept(concept["concept_id"])
                actions.append({
                    "action": "orphaned_concept_removed",
                    "concept_id": concept["concept_id"],
                    "name": concept["name"]
                })
            
            # Find orphaned memories (no user or concept relationships)
            orphaned_memories_query = """
            MATCH (m:Memory)
            WHERE NOT (m)-[:DISCUSSED_IN]-()
              AND NOT (m)-[:RELATES_TO]-()
              AND m.created_at < (timestamp() - 604800000)  // 1 week ago
            RETURN m.memory_id as memory_id
            LIMIT 20
            """
            
            orphaned_memories = neo4j_production.execute_query(orphaned_memories_query)
            
            for memory in orphaned_memories:
                await self._remove_memory(memory["memory_id"])
                actions.append({
                    "action": "orphaned_memory_removed",
                    "memory_id": memory["memory_id"]
                })
            
            logger.debug(f"✅ Orphaned node cleanup completed with {len(actions)} actions")
            
        except Exception as e:
            logger.error(f"Failed to cleanup orphaned nodes: {e}")
            actions.append({"action": "orphaned_cleanup_failed", "error": str(e)})
        
        return actions
    
    async def _collect_graph_statistics(self) -> Dict[str, Any]:
        """Collect comprehensive graph statistics"""
        
        try:
            stats_queries = {
                "total_concepts": "MATCH (c:Concept) RETURN count(c) as count",
                "total_memories": "MATCH (m:Memory) RETURN count(m) as count",
                "total_relationships": "MATCH ()-[r:RELATES_TO]->() RETURN count(r) as count",
                "total_users": "MATCH (u:User) RETURN count(u) as count",
                "avg_concept_importance": "MATCH (c:Concept) RETURN avg(coalesce(c.importance_score, 0.5)) as avg_score",
                "avg_memory_significance": "MATCH (m:Memory) RETURN avg(coalesce(m.significance_score, 0.5)) as avg_score",
                "avg_relationship_strength": "MATCH ()-[r:RELATES_TO]->() RETURN avg(coalesce(r.strength, 0.5)) as avg_strength"
            }
            
            statistics = {}
            
            for stat_name, query in stats_queries.items():
                try:
                    result = neo4j_production.execute_query(query)
                    if result:
                        if "count" in result[0]:
                            statistics[stat_name] = result[0]["count"]
                        elif "avg_score" in result[0]:
                            statistics[stat_name] = round(result[0]["avg_score"], 3)
                        elif "avg_strength" in result[0]:
                            statistics[stat_name] = round(result[0]["avg_strength"], 3)
                except Exception as e:
                    logger.warning(f"Failed to collect {stat_name}: {e}")
                    statistics[stat_name] = None
            
            # Calculate health metrics
            statistics["graph_health_score"] = self._calculate_graph_health_score(statistics)
            statistics["collection_timestamp"] = datetime.now().isoformat()
            
            return statistics
            
        except Exception as e:
            logger.error(f"Failed to collect graph statistics: {e}")
            return {"error": str(e)}
    
    def _calculate_graph_health_score(self, statistics: Dict[str, Any]) -> float:
        """Calculate overall graph health score"""
        
        try:
            # Base health metrics
            concept_count = statistics.get("total_concepts", 0)
            memory_count = statistics.get("total_memories", 0)
            relationship_count = statistics.get("total_relationships", 0)
            
            # Avoid division by zero
            if concept_count == 0:
                return 0.0
            
            # Calculate ratios
            relationship_to_concept_ratio = relationship_count / concept_count
            memory_to_concept_ratio = memory_count / concept_count
            
            # Ideal ratios (can be tuned)
            ideal_rel_ratio = 3.0  # 3 relationships per concept
            ideal_mem_ratio = 2.0  # 2 memories per concept
            
            # Calculate health components
            relationship_health = min(1.0, relationship_to_concept_ratio / ideal_rel_ratio)
            memory_health = min(1.0, memory_to_concept_ratio / ideal_mem_ratio)
            
            # Quality metrics
            avg_concept_importance = statistics.get("avg_concept_importance", 0.5)
            avg_memory_significance = statistics.get("avg_memory_significance", 0.5)
            avg_relationship_strength = statistics.get("avg_relationship_strength", 0.5)
            
            quality_health = (avg_concept_importance + avg_memory_significance + avg_relationship_strength) / 3
            
            # Overall health score
            health_score = (relationship_health * 0.3 + memory_health * 0.3 + quality_health * 0.4)
            
            return round(health_score, 3)
            
        except Exception as e:
            logger.error(f"Failed to calculate graph health score: {e}")
            return 0.5
    
    async def _remove_relationship(self, source_id: str, target_id: str, relationship_type: str):
        """Remove a relationship between two nodes"""
        cypher = f"""
        MATCH (a {{concept_id: $source_id}})-[r:{relationship_type}]->(b {{concept_id: $target_id}})
        DELETE r
        """
        
        neo4j_production.execute_write_query(cypher, {
            "source_id": source_id,
            "target_id": target_id
        })
    
    async def _remove_concept(self, concept_id: str):
        """Remove a concept and all its relationships"""
        try:
            cypher = """
            MATCH (c:Concept {concept_id: $concept_id})
            DETACH DELETE c
            """
            
            neo4j_production.execute_write_query(cypher, {"concept_id": concept_id})
            logger.debug(f"Removed concept: {concept_id}")
            
        except Exception as e:
            logger.error(f"Failed to remove concept {concept_id}: {e}")
            raise
    
    async def _archive_concept(self, concept_id: str):
        """Archive a concept by marking it as archived instead of deleting"""
        try:
            cypher = """
            MATCH (c:Concept {concept_id: $concept_id})
            SET c.archived = true, c.archived_at = timestamp()
            """
            
            neo4j_production.execute_write_query(cypher, {"concept_id": concept_id})
            logger.debug(f"Archived concept: {concept_id}")
            
        except Exception as e:
            logger.error(f"Failed to archive concept {concept_id}: {e}")
            raise
    
    async def _remove_memory(self, memory_id: str):
        """Remove a memory and all its relationships"""
        try:
            cypher = """
            MATCH (m:Memory {memory_id: $memory_id})
            DETACH DELETE m
            """
            
            neo4j_production.execute_write_query(cypher, {"memory_id": memory_id})
            logger.debug(f"Removed memory: {memory_id}")
            
        except Exception as e:
            logger.error(f"Failed to remove memory {memory_id}: {e}")
            raise
    
    async def _archive_memory(self, memory_id: str):
        """Archive a memory by marking it as archived instead of deleting"""
        try:
            cypher = """
            MATCH (m:Memory {memory_id: $memory_id})
            SET m.archived = true, m.archived_at = timestamp()
            """
            
            neo4j_production.execute_write_query(cypher, {"memory_id": memory_id})
            logger.debug(f"Archived memory: {memory_id}")
            
        except Exception as e:
            logger.error(f"Failed to archive memory {memory_id}: {e}")
            raise
    
    async def _update_relationship_strength(self, source_id: str, target_id: str, relationship_type: str, new_strength: float):
        """Update the strength of a relationship"""
        try:
            cypher = f"""
            MATCH (a {{concept_id: $source_id}})-[r:{relationship_type}]->(b {{concept_id: $target_id}})
            SET r.strength = $new_strength, r.last_updated = timestamp()
            """
            
            neo4j_production.execute_write_query(cypher, {
                "source_id": source_id,
                "target_id": target_id,
                "new_strength": new_strength
            })
            
        except Exception as e:
            logger.error(f"Failed to update relationship strength: {e}")
            raise
    
    async def _prune_concept_relationships(self, concept_id: str, max_relationships: int) -> int:
        """Prune excessive relationships for a concept, keeping the strongest ones"""
        try:
            cypher = """
            MATCH (c:Concept {concept_id: $concept_id})-[r:RELATES_TO]-(other)
            WITH r, coalesce(r.strength, 0.5) as strength
            ORDER BY strength ASC
            WITH collect(r) as relationships
            WITH relationships[0..(size(relationships) - $max_relationships)] as to_delete
            UNWIND to_delete as rel
            DELETE rel
            RETURN size(to_delete) as pruned_count
            """
            
            result = neo4j_production.execute_query(cypher, {
                "concept_id": concept_id,
                "max_relationships": max_relationships
            })
            
            return result[0]["pruned_count"] if result else 0
            
        except Exception as e:
            logger.error(f"Failed to prune concept relationships: {e}")
            return 0
    
    async def _find_similar_concepts(self) -> List[List[Dict[str, Any]]]:
        """Find groups of similar concepts for consolidation"""
        # Simplified implementation - can be enhanced with embedding similarity
        try:
            cypher = """
            MATCH (c1:Concept), (c2:Concept)
            WHERE c1.concept_id < c2.concept_id
              AND toLower(c1.name) CONTAINS toLower(c2.name) 
              OR toLower(c2.name) CONTAINS toLower(c1.name)
              OR c1.name =~ '.*' + c2.name + '.*'
            RETURN c1.concept_id as concept1_id, c1.name as concept1_name,
                   c2.concept_id as concept2_id, c2.name as concept2_name,
                   0.8 as similarity_score
            LIMIT 10
            """
            
            similar_pairs = neo4j_production.execute_query(cypher)
            
            # Group similar concepts
            concept_groups = []
            for pair in similar_pairs:
                concept_groups.append([
                    {"concept_id": pair["concept1_id"], "name": pair["concept1_name"], "similarity_score": pair["similarity_score"]},
                    {"concept_id": pair["concept2_id"], "name": pair["concept2_name"], "similarity_score": pair["similarity_score"]}
                ])
            
            return concept_groups
            
        except Exception as e:
            logger.error(f"Failed to find similar concepts: {e}")
            return []
    
    async def _consolidate_concept_group(self, concept_group: List[Dict[str, Any]], consciousness_context: Dict[str, Any]) -> Dict[str, Any]:
        """Consolidate a group of similar concepts into one"""
        # Simplified implementation - merge into the first concept
        try:
            primary_concept = concept_group[0]
            other_concepts = concept_group[1:]
            
            for concept in other_concepts:
                # Transfer relationships to primary concept
                cypher = """
                MATCH (old:Concept {concept_id: $old_id})-[r:RELATES_TO]-(other)
                MATCH (new:Concept {concept_id: $new_id})
                WHERE NOT (new)-[:RELATES_TO]-(other)
                CREATE (new)-[:RELATES_TO {
                    strength: coalesce(r.strength, 0.5),
                    created_at: timestamp(),
                    consolidated_from: $old_id
                }]-(other)
                """
                
                neo4j_production.execute_write_query(cypher, {
                    "old_id": concept["concept_id"],
                    "new_id": primary_concept["concept_id"]
                })
                
                # Remove old concept
                await self._remove_concept(concept["concept_id"])
            
            return primary_concept
            
        except Exception as e:
            logger.error(f"Failed to consolidate concept group: {e}")
            return concept_group[0]
    
    async def _find_memory_consolidation_candidates(self) -> List[List[Dict[str, Any]]]:
        """Find groups of memories that can be consolidated"""
        # Simplified implementation
        return []
    
    async def _consolidate_memory_group(self, memory_group: List[Dict[str, Any]], consciousness_context: Dict[str, Any]) -> Dict[str, Any]:
        """Consolidate a group of related memories"""
        # Simplified implementation
        return memory_group[0]
    
    async def _get_user_memory_counts(self) -> List[Dict[str, Any]]:
        """Get memory counts per user"""
        try:
            cypher = """
            MATCH (u:User)-[:DISCUSSED_IN]-(m:Memory)
            RETURN u.user_id as user_id, count(m) as memory_count
            ORDER BY memory_count DESC
            """
            
            return neo4j_production.execute_query(cypher)
            
        except Exception as e:
            logger.error(f"Failed to get user memory counts: {e}")
            return []
    
    async def _prune_user_memories(self, user_id: str, max_memories: int) -> int:
        """Prune user memories, keeping the most significant ones"""
        try:
            cypher = """
            MATCH (u:User {user_id: $user_id})-[:DISCUSSED_IN]-(m:Memory)
            WITH m, coalesce(m.significance_score, 0.5) as significance
            ORDER BY significance ASC
            WITH collect(m) as memories
            WITH memories[0..(size(memories) - $max_memories)] as to_delete
            UNWIND to_delete as memory
            DETACH DELETE memory
            RETURN size(to_delete) as pruned_count
            """
            
            result = neo4j_production.execute_query(cypher, {
                "user_id": user_id,
                "max_memories": max_memories
            })
            
            return result[0]["pruned_count"] if result else 0
            
        except Exception as e:
            logger.error(f"Failed to prune user memories: {e}")
            return 0

    async def _record_maintenance_event(self, maintenance_results: Dict[str, Any]):
        """Record maintenance event for tracking"""
        try:
            cypher = """
            CREATE (me:MaintenanceEvent {
                event_id: randomUUID(),
                maintenance_type: $maintenance_type,
                actions_count: $actions_count,
                results: $results,
                timestamp: timestamp()
            })
            RETURN me.event_id as event_id
            """
            
            neo4j_production.execute_write_query(cypher, {
                "maintenance_type": maintenance_results["maintenance_type"],
                "actions_count": maintenance_results["total_actions"],
                "results": json.dumps(maintenance_results)
            })
            
        except Exception as e:
            logger.error(f"Failed to record maintenance event: {e}")

# Global instance
knowledge_graph_maintenance = KnowledgeGraphMaintenance()