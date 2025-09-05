"""
Consciousness-Knowledge Graph Integrator
Context7 MCP-compliant system for automatic knowledge graph updates from consciousness evolution
Bridges consciousness insights with dynamic knowledge graph management
"""
import logging
from typing import Dict, Any, List, Optional, Set
from datetime import datetime, timedelta
import asyncio
import json
import re
import uuid
from backend.utils.neo4j_production import neo4j_production
from backend.utils.knowledge_graph_evolution import knowledge_graph_evolution_manager
from backend.utils.embedding_enhanced import get_embedding
from backend.core.performance_optimization import PerformanceOptimizer
from backend.core.enhanced_error_handling import ErrorHandler, ErrorSeverity, handle_errors

logger = logging.getLogger(__name__)
error_handler = ErrorHandler()
performance_optimizer = PerformanceOptimizer()

class ConsciousnessKnowledgeIntegrator:
    """
    Context7 MCP-compliant consciousness-knowledge graph integration system
    Automatically updates knowledge graph based on consciousness evolution and insights
    """
    
    def __init__(self):
        self.performance_optimizer = performance_optimizer
        self.evolution_manager = knowledge_graph_evolution_manager
        self.concept_extraction_patterns = [
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',  # Proper nouns
            r'\b(artificial intelligence|machine learning|consciousness|knowledge|learning|memory|reasoning)\b',  # Key terms
            r'\b(\w+ing|\w+tion|\w+ness|\w+ity)\b'  # Abstract concepts
        ]
        
    @handle_errors(
        component="consciousness_knowledge_integrator",
        fallback_result={},
        suppress_errors=True
    )
    async def integrate_consciousness_evolution(
        self,
        consciousness_delta: Dict[str, Any],
        interaction_context: Dict[str, Any],
        user_id: str = "mainza-user"
    ) -> Dict[str, Any]:
        """
        Integrate consciousness evolution into knowledge graph updates
        
        Args:
            consciousness_delta: Changes in consciousness state
            interaction_context: Context from recent interactions
            user_id: User identifier
            
        Returns:
            Integration results and actions taken
        """
        try:
            logger.info("🧠 Integrating consciousness evolution into knowledge graph")
            
            integration_actions = []
            
            # Extract new concepts from consciousness insights
            if consciousness_delta.get("insights"):
                new_concepts = await self._extract_concepts_from_insights(
                    consciousness_delta["insights"], consciousness_delta
                )
                
                for concept in new_concepts:
                    concept_id = await self._create_or_update_concept(
                        concept["name"], concept["description"], consciousness_delta
                    )
                    integration_actions.append({
                        "action": "concept_created",
                        "concept_id": concept_id,
                        "source": "consciousness_insight"
                    })
            
            # Update existing concepts based on consciousness focus
            if consciousness_delta.get("focus_areas"):
                for focus_area in consciousness_delta["focus_areas"]:
                    await self._boost_concept_importance(focus_area, consciousness_delta)
                    integration_actions.append({
                        "action": "concept_boosted",
                        "concept": focus_area,
                        "source": "consciousness_focus"
                    })
            
            # Create memories from consciousness reflections
            if consciousness_delta.get("reflections"):
                for reflection in consciousness_delta["reflections"]:
                    memory_id = await self._create_consciousness_memory(
                        reflection, consciousness_delta, user_id
                    )
                    integration_actions.append({
                        "action": "memory_created",
                        "memory_id": memory_id,
                        "source": "consciousness_reflection"
                    })
            
            # Update relationships based on consciousness patterns
            if consciousness_delta.get("relationship_patterns"):
                relationship_updates = await self._update_relationships_from_patterns(
                    consciousness_delta["relationship_patterns"], consciousness_delta
                )
                integration_actions.extend(relationship_updates)
            
            # Evolve knowledge graph based on consciousness level changes
            if abs(consciousness_delta.get("consciousness_level_delta", 0)) > 0.1:
                evolution_results = await self._evolve_graph_from_consciousness_change(
                    consciousness_delta, interaction_context
                )
                integration_actions.extend(evolution_results)
            
            # Record integration event
            await self._record_consciousness_integration(
                consciousness_delta, integration_actions, user_id
            )
            
            logger.info(f"✅ Consciousness integration completed with {len(integration_actions)} actions")
            
            return {
                "integration_successful": True,
                "actions_taken": len(integration_actions),
                "integration_actions": integration_actions,
                "consciousness_level": consciousness_delta.get("consciousness_level", 0.7),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to integrate consciousness evolution: {e}")
            return {"error": str(e), "integration_successful": False}
    
    @handle_errors(
        component="consciousness_knowledge_integrator",
        fallback_result=[],
        suppress_errors=True
    )
    async def auto_discover_concepts_from_interaction(
        self,
        interaction_text: str,
        consciousness_context: Dict[str, Any],
        user_id: str = "mainza-user"
    ) -> List[Dict[str, Any]]:
        """
        Automatically discover and create new concepts from interaction text
        """
        try:
            logger.info("🔍 Auto-discovering concepts from interaction")
            
            # Extract potential concepts using NLP patterns
            potential_concepts = self._extract_concepts_from_text(interaction_text)
            
            # Filter concepts based on consciousness context
            filtered_concepts = self._filter_concepts_by_consciousness(
                potential_concepts, consciousness_context
            )
            
            discovered_concepts = []
            
            for concept_data in filtered_concepts:
                # Check if concept already exists
                existing_concept = await self._find_existing_concept(concept_data["name"])
                
                if existing_concept:
                    # Update existing concept
                    await self.evolution_manager.evolve_concept(
                        existing_concept["concept_id"],
                        {"query": interaction_text, "related_concepts": [concept_data["name"]]},
                        consciousness_context
                    )
                    discovered_concepts.append({
                        "action": "updated_existing",
                        "concept_id": existing_concept["concept_id"],
                        "concept_name": concept_data["name"]
                    })
                else:
                    # Create new concept
                    concept_id = await self._create_or_update_concept(
                        concept_data["name"], 
                        concept_data.get("description", f"Concept discovered from interaction: {concept_data['name']}"),
                        consciousness_context
                    )
                    
                    # Link to user interaction
                    await self._link_concept_to_interaction(concept_id, interaction_text, user_id)
                    
                    discovered_concepts.append({
                        "action": "created_new",
                        "concept_id": concept_id,
                        "concept_name": concept_data["name"],
                        "confidence": concept_data.get("confidence", 0.7)
                    })
            
            logger.debug(f"✅ Discovered {len(discovered_concepts)} concepts from interaction")
            
            return discovered_concepts
            
        except Exception as e:
            logger.error(f"❌ Failed to auto-discover concepts: {e}")
            return []
    
    @handle_errors(
        component="consciousness_knowledge_integrator",
        fallback_result={},
        suppress_errors=True
    )
    async def consolidate_knowledge_from_consciousness_patterns(
        self,
        consciousness_patterns: Dict[str, Any],
        time_window: timedelta = timedelta(days=7)
    ) -> Dict[str, Any]:
        """
        Consolidate knowledge graph based on consciousness usage patterns
        """
        try:
            logger.info("🧠 Consolidating knowledge from consciousness patterns")
            
            consolidation_actions = []
            
            # Get frequently accessed concepts
            frequent_concepts = await self._get_frequently_accessed_concepts(time_window)
            
            # Consolidate similar concepts
            for concept_group in self._group_similar_concepts(frequent_concepts):
                if len(concept_group) > 1:
                    consolidated_concept = await self._consolidate_concept_group(
                        concept_group, consciousness_patterns
                    )
                    consolidation_actions.append({
                        "action": "concepts_consolidated",
                        "original_concepts": [c["concept_id"] for c in concept_group],
                        "consolidated_concept": consolidated_concept["concept_id"],
                        "consolidation_score": consolidated_concept["consolidation_score"]
                    })
            
            # Consolidate related memories
            memory_clusters = await self._identify_memory_clusters(consciousness_patterns)
            
            for cluster in memory_clusters:
                if len(cluster["memories"]) > 2:
                    consolidated_memory = await self._consolidate_memory_cluster(
                        cluster, consciousness_patterns
                    )
                    consolidation_actions.append({
                        "action": "memories_consolidated",
                        "original_memories": cluster["memories"],
                        "consolidated_memory": consolidated_memory["memory_id"],
                        "cluster_theme": cluster["theme"]
                    })
            
            # Strengthen important relationships
            relationship_updates = await self._strengthen_important_relationships(
                consciousness_patterns, time_window
            )
            consolidation_actions.extend(relationship_updates)
            
            logger.info(f"✅ Knowledge consolidation completed with {len(consolidation_actions)} actions")
            
            return {
                "consolidation_successful": True,
                "actions_taken": len(consolidation_actions),
                "consolidation_actions": consolidation_actions,
                "time_window_days": time_window.days,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to consolidate knowledge: {e}")
            return {"error": str(e), "consolidation_successful": False}
    
    def _extract_concepts_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract potential concepts from text using NLP patterns"""
        concepts = []
        text_lower = text.lower()
        
        # Extract using predefined patterns
        for pattern in self.concept_extraction_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                
                # Filter out common words and short terms
                if (len(match) > 2 and 
                    match.lower() not in ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'who', 'boy', 'did', 'man', 'men', 'put', 'say', 'she', 'too', 'use']):
                    
                    concepts.append({
                        "name": match.strip(),
                        "confidence": 0.7,
                        "source": "pattern_extraction",
                        "context": text[:100] + "..." if len(text) > 100 else text
                    })
        
        # Remove duplicates and sort by confidence
        unique_concepts = {}
        for concept in concepts:
            name = concept["name"].lower()
            if name not in unique_concepts or concept["confidence"] > unique_concepts[name]["confidence"]:
                unique_concepts[name] = concept
        
        return list(unique_concepts.values())
    
    def _filter_concepts_by_consciousness(
        self,
        concepts: List[Dict[str, Any]],
        consciousness_context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Filter concepts based on consciousness context"""
        
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "curious")
        active_goals = consciousness_context.get("active_goals", [])
        
        # Consciousness level affects concept acceptance threshold
        acceptance_threshold = 0.5 + (consciousness_level * 0.3)
        
        # Emotional state affects concept preferences
        emotional_preferences = {
            "curious": ["learning", "discovery", "exploration", "knowledge", "understanding"],
            "contemplative": ["meaning", "philosophy", "reflection", "thought", "consciousness"],
            "focused": ["goal", "task", "solution", "method", "approach"],
            "empathetic": ["emotion", "feeling", "relationship", "connection", "understanding"],
            "excited": ["innovation", "creativity", "possibility", "potential", "breakthrough"]
        }
        
        preferred_terms = emotional_preferences.get(emotional_state, [])
        
        filtered_concepts = []
        for concept in concepts:
            # Base acceptance based on confidence
            if concept["confidence"] < acceptance_threshold:
                continue
            
            # Boost concepts related to emotional state
            if any(term in concept["name"].lower() for term in preferred_terms):
                concept["confidence"] += 0.2
            
            # Boost concepts related to active goals
            if any(goal.lower() in concept["name"].lower() for goal in active_goals):
                concept["confidence"] += 0.3
            
            # Final acceptance check
            if concept["confidence"] >= acceptance_threshold:
                filtered_concepts.append(concept)
        
        return sorted(filtered_concepts, key=lambda x: x["confidence"], reverse=True)[:10]
    
    async def _extract_concepts_from_insights(
        self,
        insights: List[str],
        consciousness_context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract concepts from consciousness insights"""
        
        all_concepts = []
        
        for insight in insights:
            concepts = self._extract_concepts_from_text(insight)
            filtered_concepts = self._filter_concepts_by_consciousness(concepts, consciousness_context)
            
            for concept in filtered_concepts:
                concept["description"] = f"Concept from consciousness insight: {insight[:100]}..."
                concept["source"] = "consciousness_insight"
                all_concepts.append(concept)
        
        return all_concepts
    
    async def _create_or_update_concept(
        self,
        concept_name: str,
        description: str,
        consciousness_context: Dict[str, Any]
    ) -> str:
        """Create or update a concept with consciousness context"""
        
        concept_id = concept_name.lower().replace(" ", "_")
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "curious")
        
        cypher = """
        MERGE (c:Concept {concept_id: $concept_id})
        ON CREATE SET 
            c.name = $name,
            c.description = $description,
            c.created_at = timestamp(),
            c.importance_score = $importance_score,
            c.consciousness_relevance = $consciousness_relevance,
            c.source = $source,
            c.emotional_context = $emotional_context
        ON MATCH SET
            c.description = $description,
            c.last_updated = timestamp(),
            c.importance_score = coalesce(c.importance_score, 0.0) + $importance_boost,
            c.consciousness_relevance = coalesce(c.consciousness_relevance, 0.0) + $consciousness_boost,
            c.usage_frequency = coalesce(c.usage_frequency, 0) + 1
        
        RETURN c.concept_id as concept_id
        """
        
        result = neo4j_production.execute_write_query(cypher, {
            "concept_id": concept_id,
            "name": concept_name,
            "description": description,
            "importance_score": consciousness_level * 0.8,
            "consciousness_relevance": consciousness_level,
            "importance_boost": 0.1,
            "consciousness_boost": 0.05,
            "source": "consciousness_integration",
            "emotional_context": emotional_state
        })
        
        return concept_id
    
    async def _create_consciousness_memory(
        self,
        reflection_text: str,
        consciousness_context: Dict[str, Any],
        user_id: str
    ) -> str:
        """Create a memory from consciousness reflection"""
        
        memory_id = f"consciousness_reflection_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8]}"
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        
        cypher = """
        CREATE (m:Memory {
            memory_id: $memory_id,
            text: $text,
            source: 'consciousness_reflection',
            type: 'reflection',
            created_at: timestamp(),
            significance_score: $significance_score,
            consciousness_impact: $consciousness_impact,
            emotional_context: $emotional_context
        })
        
        // Link to user
        WITH m
        MERGE (u:User {user_id: $user_id})
        CREATE (m)-[:DISCUSSED_IN]->(u)
        
        // Link to consciousness state
        WITH m
        MATCH (ms:MainzaState)
        WHERE ms.state_id CONTAINS 'mainza'
        CREATE (m)-[:RELATES_TO]->(ms)
        
        RETURN m.memory_id as memory_id
        """
        
        result = neo4j_production.execute_write_query(cypher, {
            "memory_id": memory_id,
            "text": reflection_text,
            "significance_score": consciousness_level * 0.9,  # High significance for reflections
            "consciousness_impact": consciousness_level,
            "emotional_context": consciousness_context.get("emotional_state", "curious"),
            "user_id": user_id
        })
        
        return memory_id
    
    async def _record_consciousness_integration(
        self,
        consciousness_delta: Dict[str, Any],
        integration_actions: List[Dict[str, Any]],
        user_id: str
    ):
        """Record consciousness integration event for tracking"""
        
        try:
            cypher = """
            CREATE (ci:ConsciousnessIntegration {
                integration_id: randomUUID(),
                consciousness_level: $consciousness_level,
                emotional_state: $emotional_state,
                actions_count: $actions_count,
                actions: $actions,
                user_id: $user_id,
                timestamp: timestamp()
            })
            
            // Link to consciousness state
            WITH ci
            MATCH (ms:MainzaState)
            WHERE ms.state_id CONTAINS 'mainza'
            CREATE (ci)-[:INTEGRATED_WITH]->(ms)
            
            RETURN ci.integration_id as integration_id
            """
            
            neo4j_production.execute_write_query(cypher, {
                "consciousness_level": consciousness_delta.get("consciousness_level", 0.7),
                "emotional_state": consciousness_delta.get("emotional_state", "curious"),
                "actions_count": len(integration_actions),
                "actions": json.dumps(integration_actions),
                "user_id": user_id
            })
            
        except Exception as e:
            logger.error(f"Failed to record consciousness integration: {e}")

# Global instance
consciousness_knowledge_integrator = ConsciousnessKnowledgeIntegrator()