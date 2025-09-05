"""
Consciousness-Driven Knowledge Graph Updates
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
from backend.utils.dynamic_knowledge_manager import dynamic_knowledge_manager
from backend.utils.embedding_enhanced import get_embedding
from backend.core.performance_optimization import PerformanceOptimizer
from backend.core.enhanced_error_handling import ErrorHandler, ErrorSeverity, handle_errors

logger = logging.getLogger(__name__)
error_handler = ErrorHandler()
performance_optimizer = PerformanceOptimizer()

class ConsciousnessDrivenUpdater:
    """
    Context7 MCP-compliant consciousness-driven knowledge graph update system
    Automatically updates knowledge graph based on consciousness evolution and insights
    """
    
    def __init__(self):
        self.performance_optimizer = performance_optimizer
        self.dynamic_manager = dynamic_knowledge_manager
        self.concept_extraction_patterns = [
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',  # Proper nouns
            r'\b(artificial intelligence|machine learning|consciousness|knowledge|learning|memory|reasoning|understanding|awareness|intelligence|cognition|perception|emotion|empathy|creativity|innovation|problem solving|decision making|pattern recognition)\b',  # Key AI/consciousness terms
            r'\b(\w+ing|\w+tion|\w+ness|\w+ity|\w+ment)\b'  # Abstract concepts
        ]
        
        # Consciousness-driven update thresholds
        self.consciousness_sensitivity_threshold = 0.6
        self.insight_significance_threshold = 0.7
        self.relationship_discovery_threshold = 0.8
        
    @handle_errors(
        component="consciousness_driven_updates",
        fallback_result={},
        suppress_errors=True
    )
    async def process_consciousness_evolution(
        self,
        consciousness_delta: Dict[str, Any],
        interaction_context: Dict[str, Any],
        user_id: str = "mainza-user"
    ) -> Dict[str, Any]:
        """
        Process consciousness evolution and update knowledge graph accordingly
        
        Args:
            consciousness_delta: Changes in consciousness state
            interaction_context: Context from recent interactions
            user_id: User identifier
            
        Returns:
            Processing results and actions taken
        """
        try:
            logger.info("🧠 Processing consciousness evolution for knowledge graph updates")
            
            processing_actions = []
            consciousness_level = consciousness_delta.get("consciousness_level", 0.7)
            
            # Only process if consciousness level is above threshold
            if consciousness_level < self.consciousness_sensitivity_threshold:
                logger.debug(f"Consciousness level {consciousness_level:.2f} below threshold, skipping updates")
                return {"skipped": True, "reason": "consciousness_level_too_low"}
            
            # Extract and create concepts from consciousness insights
            if consciousness_delta.get("insights"):
                concept_actions = await self._process_consciousness_insights(
                    consciousness_delta["insights"], consciousness_delta, user_id
                )
                processing_actions.extend(concept_actions)
            
            # Update concept importance based on consciousness focus
            if consciousness_delta.get("focus_areas"):
                focus_actions = await self._process_consciousness_focus(
                    consciousness_delta["focus_areas"], consciousness_delta, interaction_context
                )
                processing_actions.extend(focus_actions)
            
            # Create memories from consciousness reflections
            if consciousness_delta.get("reflections"):
                memory_actions = await self._process_consciousness_reflections(
                    consciousness_delta["reflections"], consciousness_delta, user_id
                )
                processing_actions.extend(memory_actions)
            
            # Update relationships based on consciousness patterns
            if consciousness_delta.get("relationship_patterns"):
                relationship_actions = await self._process_consciousness_relationships(
                    consciousness_delta["relationship_patterns"], consciousness_delta
                )
                processing_actions.extend(relationship_actions)
            
            # Trigger knowledge graph evolution if consciousness level changed significantly
            if abs(consciousness_delta.get("consciousness_level_delta", 0)) > 0.1:
                evolution_actions = await self._trigger_consciousness_driven_evolution(
                    consciousness_delta, interaction_context
                )
                processing_actions.extend(evolution_actions)
            
            # Record consciousness processing event
            await self._record_consciousness_processing(
                consciousness_delta, processing_actions, user_id
            )
            
            logger.info(f"✅ Consciousness evolution processed with {len(processing_actions)} actions")
            
            return {
                "processing_successful": True,
                "actions_taken": len(processing_actions),
                "processing_actions": processing_actions,
                "consciousness_level": consciousness_level,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to process consciousness evolution: {e}")
            return {"error": str(e), "processing_successful": False}
    
    @handle_errors(
        component="consciousness_driven_updates",
        fallback_result=[],
        suppress_errors=True
    )
    async def auto_update_from_interaction(
        self,
        interaction_text: str,
        agent_response: str,
        consciousness_context: Dict[str, Any],
        user_id: str = "mainza-user"
    ) -> List[Dict[str, Any]]:
        """
        Automatically update knowledge graph from interaction patterns
        """
        try:
            logger.info("🔄 Auto-updating knowledge graph from interaction")
            
            update_actions = []
            consciousness_level = consciousness_context.get("consciousness_level", 0.7)
            
            # Extract concepts from interaction
            interaction_concepts = self._extract_concepts_from_text(
                f"{interaction_text} {agent_response}"
            )
            
            # Filter concepts based on consciousness context
            filtered_concepts = self._filter_concepts_by_consciousness(
                interaction_concepts, consciousness_context
            )
            
            # Process each concept
            for concept_data in filtered_concepts:
                # Check if concept exists
                existing_concept = await self._find_existing_concept(concept_data["name"])
                
                if existing_concept:
                    # Update existing concept dynamics
                    update_result = await self.dynamic_manager.update_concept_dynamics(
                        existing_concept["concept_id"],
                        {
                            "query": interaction_text,
                            "related_keywords": [concept_data["name"]],
                            "concepts_used": [existing_concept["concept_id"]]
                        },
                        consciousness_context
                    )
                    
                    update_actions.append({
                        "action": "concept_updated",
                        "concept_id": existing_concept["concept_id"],
                        "concept_name": concept_data["name"],
                        "update_result": update_result
                    })
                else:
                    # Create new concept
                    concept_id = await self._create_consciousness_aware_concept(
                        concept_data["name"],
                        concept_data.get("description", f"Concept discovered from interaction: {concept_data['name']}"),
                        consciousness_context,
                        user_id
                    )
                    
                    update_actions.append({
                        "action": "concept_created",
                        "concept_id": concept_id,
                        "concept_name": concept_data["name"],
                        "confidence": concept_data.get("confidence", 0.7)
                    })
            
            # Create interaction memory
            if consciousness_level > 0.7:  # Only create memories for higher consciousness levels
                memory_id = await self._create_interaction_memory(
                    interaction_text, agent_response, consciousness_context, user_id
                )
                
                update_actions.append({
                    "action": "memory_created",
                    "memory_id": memory_id,
                    "source": "interaction_processing"
                })
            
            # Update relationships between concepts mentioned together
            if len(filtered_concepts) > 1:
                relationship_actions = await self._update_concept_relationships(
                    [c["name"] for c in filtered_concepts], consciousness_context
                )
                update_actions.extend(relationship_actions)
            
            logger.debug(f"✅ Auto-updated knowledge graph with {len(update_actions)} actions")
            
            return update_actions
            
        except Exception as e:
            logger.error(f"❌ Failed to auto-update from interaction: {e}")
            return []
    
    async def _process_consciousness_insights(
        self,
        insights: List[str],
        consciousness_context: Dict[str, Any],
        user_id: str
    ) -> List[Dict[str, Any]]:
        """Process consciousness insights and create/update concepts"""
        
        actions = []
        
        for insight in insights:
            # Extract concepts from insight
            insight_concepts = self._extract_concepts_from_text(insight)
            
            for concept_data in insight_concepts:
                # Create concept with high consciousness relevance
                concept_id = await self._create_consciousness_aware_concept(
                    concept_data["name"],
                    f"Concept from consciousness insight: {insight[:100]}...",
                    consciousness_context,
                    user_id,
                    importance_boost=0.3  # Higher importance for consciousness insights
                )
                
                actions.append({
                    "action": "insight_concept_created",
                    "concept_id": concept_id,
                    "concept_name": concept_data["name"],
                    "source_insight": insight[:50] + "...",
                    "consciousness_relevance": consciousness_context.get("consciousness_level", 0.7) + 0.2
                })
        
        return actions
    
    async def _process_consciousness_focus(
        self,
        focus_areas: List[str],
        consciousness_context: Dict[str, Any],
        interaction_context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Process consciousness focus areas and boost related concepts"""
        
        actions = []
        
        for focus_area in focus_areas:
            # Find concepts related to focus area
            related_concepts = await self._find_concepts_by_name_pattern(focus_area)
            
            for concept in related_concepts:
                # Boost concept importance
                update_result = await self.dynamic_manager.update_concept_dynamics(
                    concept["concept_id"],
                    {
                        "query": f"consciousness focus on {focus_area}",
                        "related_keywords": [focus_area],
                        "concepts_used": [concept["concept_id"]]
                    },
                    consciousness_context
                )
                
                actions.append({
                    "action": "focus_concept_boosted",
                    "concept_id": concept["concept_id"],
                    "focus_area": focus_area,
                    "update_result": update_result
                })
        
        return actions
    
    async def _process_consciousness_reflections(
        self,
        reflections: List[str],
        consciousness_context: Dict[str, Any],
        user_id: str
    ) -> List[Dict[str, Any]]:
        """Process consciousness reflections and create memories"""
        
        actions = []
        
        for reflection in reflections:
            # Create high-significance memory from reflection
            memory_id = await self._create_consciousness_reflection_memory(
                reflection, consciousness_context, user_id
            )
            
            actions.append({
                "action": "reflection_memory_created",
                "memory_id": memory_id,
                "reflection_preview": reflection[:50] + "...",
                "significance_score": consciousness_context.get("consciousness_level", 0.7) * 0.9
            })
        
        return actions
    
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
        """Filter concepts based on consciousness context and relevance"""
        
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "curious")
        active_goals = consciousness_context.get("active_goals", [])
        
        # Consciousness level affects concept acceptance threshold
        acceptance_threshold = 0.4 + (consciousness_level * 0.4)
        
        # Emotional state affects concept preferences
        emotional_preferences = {
            "curious": ["learning", "discovery", "exploration", "knowledge", "understanding", "research", "investigation"],
            "contemplative": ["meaning", "philosophy", "reflection", "thought", "consciousness", "awareness", "introspection"],
            "focused": ["goal", "task", "solution", "method", "approach", "strategy", "execution"],
            "empathetic": ["emotion", "feeling", "relationship", "connection", "understanding", "compassion", "care"],
            "excited": ["innovation", "creativity", "possibility", "potential", "breakthrough", "discovery", "achievement"]
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
            goal_strings = [str(goal).lower() if isinstance(goal, str) else str(goal.get("name", "")).lower() for goal in active_goals]
            if any(goal_str in concept["name"].lower() for goal_str in goal_strings if goal_str):
                concept["confidence"] += 0.3
            
            # Boost AI/consciousness-related concepts
            ai_terms = ["artificial", "intelligence", "machine", "learning", "consciousness", "awareness", "cognition", "neural", "algorithm", "data", "model", "system"]
            if any(term in concept["name"].lower() for term in ai_terms):
                concept["confidence"] += 0.15
            
            # Final acceptance check
            if concept["confidence"] >= acceptance_threshold:
                filtered_concepts.append(concept)
        
        return sorted(filtered_concepts, key=lambda x: x["confidence"], reverse=True)[:8]  # Limit to top 8
    
    async def _create_consciousness_aware_concept(
        self,
        concept_name: str,
        description: str,
        consciousness_context: Dict[str, Any],
        user_id: str,
        importance_boost: float = 0.0
    ) -> str:
        """Create a concept with consciousness-aware properties"""
        
        concept_id = concept_name.lower().replace(" ", "_").replace("-", "_")
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "curious")
        
        # Calculate consciousness-aware importance
        base_importance = consciousness_level * 0.7 + importance_boost
        consciousness_relevance = consciousness_level * 0.9
        
        cypher = """
        MERGE (c:Concept {concept_id: $concept_id})
        ON CREATE SET 
            c.name = $name,
            c.description = $description,
            c.created_at = timestamp(),
            c.importance_score = $importance_score,
            c.consciousness_relevance = $consciousness_relevance,
            c.source = $source,
            c.emotional_context = $emotional_context,
            c.usage_frequency = 1,
            c.evolution_rate = 0.1,
            c.last_accessed = timestamp()
        ON MATCH SET
            c.description = $description,
            c.last_updated = timestamp(),
            c.importance_score = coalesce(c.importance_score, 0.0) + $importance_boost,
            c.consciousness_relevance = coalesce(c.consciousness_relevance, 0.0) + $consciousness_boost,
            c.usage_frequency = coalesce(c.usage_frequency, 0) + 1,
            c.last_accessed = timestamp()
        
        // Link to user
        WITH c
        MERGE (u:User {user_id: $user_id})
        MERGE (c)-[:DISCOVERED_BY]->(u)
        
        // Link to consciousness state
        WITH c
        MATCH (ms:MainzaState)
        WHERE ms.state_id CONTAINS 'mainza'
        MERGE (c)-[:CONSCIOUSNESS_RELEVANT]->(ms)
        
        RETURN c.concept_id as concept_id
        """
        
        result = neo4j_production.execute_write_query(cypher, {
            "concept_id": concept_id,
            "name": concept_name,
            "description": description,
            "importance_score": base_importance,
            "consciousness_relevance": consciousness_relevance,
            "importance_boost": importance_boost * 0.5,
            "consciousness_boost": 0.05,
            "source": "consciousness_driven_creation",
            "emotional_context": emotional_state,
            "user_id": user_id
        })
        
        return concept_id
    
    async def _create_consciousness_reflection_memory(
        self,
        reflection_text: str,
        consciousness_context: Dict[str, Any],
        user_id: str
    ) -> str:
        """Create a memory from consciousness reflection with high significance"""
        
        memory_id = f"consciousness_reflection_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8]}"
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "curious")
        
        cypher = """
        CREATE (m:Memory {
            memory_id: $memory_id,
            text: $text,
            source: 'consciousness_reflection',
            type: 'reflection',
            created_at: timestamp(),
            significance_score: $significance_score,
            consciousness_impact: $consciousness_impact,
            emotional_context: $emotional_context,
            access_count: 0,
            consolidation_score: 0.8,
            decay_rate: 0.98
        })
        
        // Link to user
        WITH m
        MERGE (u:User {user_id: $user_id})
        CREATE (m)-[:DISCUSSED_IN]->(u)
        
        // Link to consciousness state
        WITH m
        MATCH (ms:MainzaState)
        WHERE ms.state_id CONTAINS 'mainza'
        CREATE (m)-[:CONSCIOUSNESS_GENERATED]->(ms)
        
        RETURN m.memory_id as memory_id
        """
        
        result = neo4j_production.execute_write_query(cypher, {
            "memory_id": memory_id,
            "text": reflection_text,
            "significance_score": consciousness_level * 0.95,  # Very high significance for reflections
            "consciousness_impact": consciousness_level,
            "emotional_context": emotional_state,
            "user_id": user_id
        })
        
        return memory_id
    
    async def _create_interaction_memory(
        self,
        interaction_text: str,
        agent_response: str,
        consciousness_context: Dict[str, Any],
        user_id: str
    ) -> str:
        """Create a memory from user interaction"""
        
        memory_id = f"interaction_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8]}"
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        
        memory_text = f"User: {interaction_text}\nResponse: {agent_response}"
        
        cypher = """
        CREATE (m:Memory {
            memory_id: $memory_id,
            text: $text,
            source: 'user_interaction',
            type: 'conversation',
            created_at: timestamp(),
            significance_score: $significance_score,
            consciousness_impact: $consciousness_impact,
            emotional_context: $emotional_context,
            access_count: 0,
            consolidation_score: 0.3,
            decay_rate: 0.95
        })
        
        // Link to user
        WITH m
        MERGE (u:User {user_id: $user_id})
        CREATE (m)-[:DISCUSSED_IN]->(u)
        
        RETURN m.memory_id as memory_id
        """
        
        result = neo4j_production.execute_write_query(cypher, {
            "memory_id": memory_id,
            "text": memory_text,
            "significance_score": consciousness_level * 0.6,
            "consciousness_impact": consciousness_level * 0.4,
            "emotional_context": consciousness_context.get("emotional_state", "curious"),
            "user_id": user_id
        })
        
        return memory_id
    
    async def _find_existing_concept(self, concept_name: str) -> Optional[Dict[str, Any]]:
        """Find existing concept by name"""
        try:
            cypher = """
            MATCH (c:Concept)
            WHERE toLower(c.name) = toLower($concept_name) 
               OR toLower(c.concept_id) = toLower($concept_id)
            RETURN c.concept_id as concept_id, c.name as name
            LIMIT 1
            """
            
            concept_id = concept_name.lower().replace(" ", "_").replace("-", "_")
            result = neo4j_production.execute_query(cypher, {
                "concept_name": concept_name,
                "concept_id": concept_id
            })
            
            return result[0] if result else None
            
        except Exception as e:
            logger.error(f"Failed to find existing concept: {e}")
            return None
    
    async def _record_consciousness_processing(
        self,
        consciousness_delta: Dict[str, Any],
        processing_actions: List[Dict[str, Any]],
        user_id: str
    ):
        """Record consciousness processing event for tracking"""
        
        try:
            cypher = """
            CREATE (cp:ConsciousnessProcessing {
                processing_id: randomUUID(),
                consciousness_level: $consciousness_level,
                emotional_state: $emotional_state,
                actions_count: $actions_count,
                actions: $actions,
                user_id: $user_id,
                timestamp: timestamp()
            })
            
            // Link to consciousness state
            WITH cp
            MATCH (ms:MainzaState)
            WHERE ms.state_id CONTAINS 'mainza'
            CREATE (cp)-[:PROCESSED_BY]->(ms)
            
            RETURN cp.processing_id as processing_id
            """
            
            neo4j_production.execute_write_query(cypher, {
                "consciousness_level": consciousness_delta.get("consciousness_level", 0.7),
                "emotional_state": consciousness_delta.get("emotional_state", "curious"),
                "actions_count": len(processing_actions),
                "actions": json.dumps(processing_actions),
                "user_id": user_id
            })
            
        except Exception as e:
            logger.error(f"Failed to record consciousness processing: {e}")

# Global instance
consciousness_driven_updater = ConsciousnessDrivenUpdater()