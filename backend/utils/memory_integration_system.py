"""
Memory Integration System
Advanced system for memory integration, synthesis, and coherence
"""
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import asyncio
import json
import numpy as np

from backend.utils.neo4j_production import neo4j_production
from backend.utils.advanced_memory_architecture import advanced_memory_architecture, MemoryType, MemoryConsolidationLevel
from backend.utils.embedding_enhanced import embedding_manager

logger = logging.getLogger(__name__)

class IntegrationType(Enum):
    """Memory integration types"""
    CONCEPTUAL_INTEGRATION = "conceptual_integration"
    EMOTIONAL_INTEGRATION = "emotional_integration"
    TEMPORAL_INTEGRATION = "temporal_integration"
    CONTEXTUAL_INTEGRATION = "contextual_integration"
    ASSOCIATIVE_INTEGRATION = "associative_integration"
    CONSCIOUSNESS_INTEGRATION = "consciousness_integration"

@dataclass
class IntegrationResult:
    """Memory integration result"""
    integration_id: str
    memory_ids: List[str]
    integration_type: IntegrationType
    integration_strength: float
    coherence_score: float
    synthesis_data: Dict[str, Any]
    timestamp: datetime
    significance: float

class MemoryIntegrationSystem:
    """
    Advanced memory integration system
    """
    
    def __init__(self):
        self.neo4j = neo4j_production
        self.memory_architecture = advanced_memory_architecture
        self.embedding_manager = embedding_manager
        
        # Integration parameters
        self.similarity_threshold = 0.7
        self.coherence_threshold = 0.6
        self.integration_threshold = 0.5
        
    async def integrate_memories(
        self,
        memory_ids: List[str],
        integration_type: IntegrationType,
        user_id: str = "mainza-user"
    ) -> Optional[IntegrationResult]:
        """Integrate multiple memories"""
        try:
            logger.info(f"🔗 Integrating {len(memory_ids)} memories with {integration_type.value}")
            
            # Get memories
            memories = await self._get_memories_by_ids(memory_ids, user_id)
            if len(memories) < 2:
                logger.warning("Need at least 2 memories for integration")
                return None
            
            # Calculate integration strength
            integration_strength = await self._calculate_integration_strength(memories, integration_type)
            
            if integration_strength < self.integration_threshold:
                logger.info(f"Integration strength too low: {integration_strength:.3f}")
                return None
            
            # Perform integration
            synthesis_data = await self._perform_integration(memories, integration_type)
            
            # Calculate coherence score
            coherence_score = await self._calculate_coherence_score(memories, synthesis_data)
            
            # Create integration result
            integration_result = IntegrationResult(
                integration_id=f"integration_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
                memory_ids=memory_ids,
                integration_type=integration_type,
                integration_strength=integration_strength,
                coherence_score=coherence_score,
                synthesis_data=synthesis_data,
                timestamp=datetime.now(),
                significance=self._calculate_integration_significance(integration_strength, coherence_score)
            )
            
            # Store integration result
            await self._store_integration_result(integration_result, user_id)
            
            logger.info(f"✅ Memory integration complete: {integration_result.integration_id}")
            return integration_result
            
        except Exception as e:
            logger.error(f"❌ Failed to integrate memories: {e}")
            return None
    
    async def find_integration_candidates(
        self,
        user_id: str = "mainza-user",
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Find memory integration candidates"""
        try:
            logger.info("🔍 Finding memory integration candidates")
            
            # Get recent memories
            cypher = """
            MATCH (u:User {user_id: $user_id})-[:HAS_MEMORY]->(m:AdvancedMemory)
            WHERE m.created_at > datetime() - duration('P7D')
            AND m.importance_score > 0.5
            RETURN m
            ORDER BY m.importance_score DESC
            LIMIT $limit
            """
            
            result = self.neo4j.execute_query(cypher, {"user_id": user_id, "limit": limit})
            
            memories = [record["m"] for record in result]
            
            # Find integration candidates
            candidates = []
            for i, memory1 in enumerate(memories):
                for memory2 in memories[i+1:]:
                    similarity = await self._calculate_memory_similarity(memory1, memory2)
                    if similarity > self.similarity_threshold:
                        candidates.append({
                            "memory1": memory1,
                            "memory2": memory2,
                            "similarity": similarity,
                            "integration_potential": similarity * (memory1.get("importance_score", 0.5) + memory2.get("importance_score", 0.5)) / 2
                        })
            
            # Sort by integration potential
            candidates.sort(key=lambda x: x["integration_potential"], reverse=True)
            
            logger.info(f"✅ Found {len(candidates)} integration candidates")
            return candidates
            
        except Exception as e:
            logger.error(f"❌ Failed to find integration candidates: {e}")
            return []
    
    async def auto_integrate_memories(self, user_id: str = "mainza-user") -> Dict[str, Any]:
        """Automatically integrate memories"""
        try:
            logger.info("🤖 Auto-integrating memories")
            
            # Find integration candidates
            candidates = await self.find_integration_candidates(user_id)
            
            if not candidates:
                logger.info("No integration candidates found")
                return {"integrated_groups": 0, "total_memories": 0}
            
            # Group memories for integration
            integration_groups = await self._group_memories_for_integration(candidates)
            
            # Integrate each group
            integration_results = []
            total_memories = 0
            
            for group in integration_groups:
                if len(group["memories"]) >= 2:
                    # Determine integration type
                    integration_type = self._determine_integration_type(group["memories"])
                    
                    # Integrate memories
                    result = await self.integrate_memories(
                        group["memory_ids"], integration_type, user_id
                    )
                    
                    if result:
                        integration_results.append(result)
                        total_memories += len(group["memory_ids"])
            
            auto_integration = {
                "integrated_groups": len(integration_results),
                "total_memories": total_memories,
                "integration_results": [r.integration_id for r in integration_results],
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"✅ Auto-integration complete: {len(integration_results)} groups integrated")
            return auto_integration
            
        except Exception as e:
            logger.error(f"❌ Failed to auto-integrate memories: {e}")
            return {"integrated_groups": 0, "total_memories": 0}
    
    async def _calculate_integration_strength(
        self,
        memories: List[Dict[str, Any]],
        integration_type: IntegrationType
    ) -> float:
        """Calculate integration strength for memories"""
        if len(memories) < 2:
            return 0.0
        
        # Calculate pairwise similarities
        similarities = []
        for i, memory1 in enumerate(memories):
            for memory2 in memories[i+1:]:
                similarity = await self._calculate_memory_similarity(memory1, memory2)
                similarities.append(similarity)
        
        if not similarities:
            return 0.0
        
        # Calculate average similarity
        avg_similarity = sum(similarities) / len(similarities)
        
        # Adjust based on integration type
        if integration_type == IntegrationType.CONCEPTUAL_INTEGRATION:
            # Check for conceptual similarity
            conceptual_similarity = await self._calculate_conceptual_similarity(memories)
            return (avg_similarity + conceptual_similarity) / 2
        
        elif integration_type == IntegrationType.EMOTIONAL_INTEGRATION:
            # Check for emotional similarity
            emotional_similarity = await self._calculate_emotional_similarity(memories)
            return (avg_similarity + emotional_similarity) / 2
        
        elif integration_type == IntegrationType.TEMPORAL_INTEGRATION:
            # Check for temporal proximity
            temporal_similarity = await self._calculate_temporal_similarity(memories)
            return (avg_similarity + temporal_similarity) / 2
        
        elif integration_type == IntegrationType.CONTEXTUAL_INTEGRATION:
            # Check for contextual similarity
            contextual_similarity = await self._calculate_contextual_similarity(memories)
            return (avg_similarity + contextual_similarity) / 2
        
        elif integration_type == IntegrationType.ASSOCIATIVE_INTEGRATION:
            # Check for associative strength
            associative_similarity = await self._calculate_associative_similarity(memories)
            return (avg_similarity + associative_similarity) / 2
        
        elif integration_type == IntegrationType.CONSCIOUSNESS_INTEGRATION:
            # Check for consciousness similarity
            consciousness_similarity = await self._calculate_consciousness_similarity(memories)
            return (avg_similarity + consciousness_similarity) / 2
        
        return avg_similarity
    
    async def _calculate_memory_similarity(
        self,
        memory1: Dict[str, Any],
        memory2: Dict[str, Any]
    ) -> float:
        """Calculate similarity between two memories"""
        try:
            # Get embeddings
            embedding1 = memory1.get("embedding")
            embedding2 = memory2.get("embedding")
            
            if not embedding1 or not embedding2:
                # Fallback to text similarity
                return await self._calculate_text_similarity(
                    memory1.get("content", ""),
                    memory2.get("content", "")
                )
            
            # Calculate cosine similarity
            similarity = await self.embedding_manager.calculate_similarity(embedding1, embedding2)
            return similarity
            
        except Exception as e:
            logger.error(f"❌ Failed to calculate memory similarity: {e}")
            return 0.0
    
    async def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity as fallback"""
        try:
            if not text1 or not text2:
                return 0.0
            
            # Simple word overlap similarity
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            
            if not words1 or not words2:
                return 0.0
            
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            
            return len(intersection) / len(union) if union else 0.0
            
        except Exception as e:
            logger.error(f"❌ Failed to calculate text similarity: {e}")
            return 0.0
    
    async def _calculate_conceptual_similarity(self, memories: List[Dict[str, Any]]) -> float:
        """Calculate conceptual similarity between memories"""
        try:
            # Extract concepts from memories
            concepts = []
            for memory in memories:
                memory_concepts = memory.get("metadata", {}).get("concepts", [])
                concepts.extend(memory_concepts)
            
            if not concepts:
                return 0.0
            
            # Calculate concept overlap
            concept_sets = [set(memory.get("metadata", {}).get("concepts", [])) for memory in memories]
            
            if len(concept_sets) < 2:
                return 0.0
            
            # Calculate average pairwise overlap
            overlaps = []
            for i, concepts1 in enumerate(concept_sets):
                for concepts2 in concept_sets[i+1:]:
                    if concepts1 or concepts2:
                        overlap = len(concepts1.intersection(concepts2)) / len(concepts1.union(concepts2))
                        overlaps.append(overlap)
            
            return sum(overlaps) / len(overlaps) if overlaps else 0.0
            
        except Exception as e:
            logger.error(f"❌ Failed to calculate conceptual similarity: {e}")
            return 0.0
    
    async def _calculate_emotional_similarity(self, memories: List[Dict[str, Any]]) -> float:
        """Calculate emotional similarity between memories"""
        try:
            # Extract emotional contexts
            emotional_contexts = []
            for memory in memories:
                emotional_context = memory.get("emotional_context", {})
                if emotional_context:
                    emotional_contexts.append(emotional_context)
            
            if len(emotional_contexts) < 2:
                return 0.0
            
            # Calculate emotional similarity
            similarities = []
            for i, context1 in enumerate(emotional_contexts):
                for context2 in emotional_contexts[i+1:]:
                    similarity = self._calculate_emotional_context_similarity(context1, context2)
                    similarities.append(similarity)
            
            return sum(similarities) / len(similarities) if similarities else 0.0
            
        except Exception as e:
            logger.error(f"❌ Failed to calculate emotional similarity: {e}")
            return 0.0
    
    def _calculate_emotional_context_similarity(
        self,
        context1: Dict[str, Any],
        context2: Dict[str, Any]
    ) -> float:
        """Calculate similarity between emotional contexts"""
        try:
            # Extract emotional dimensions
            emotion1 = context1.get("emotion", "neutral")
            emotion2 = context2.get("emotion", "neutral")
            
            intensity1 = context1.get("intensity", 0.5)
            intensity2 = context2.get("intensity", 0.5)
            
            valence1 = context1.get("valence", 0.0)
            valence2 = context2.get("valence", 0.0)
            
            arousal1 = context1.get("arousal", 0.0)
            arousal2 = context2.get("arousal", 0.0)
            
            # Calculate similarity
            emotion_similarity = 1.0 if emotion1 == emotion2 else 0.0
            intensity_similarity = 1.0 - abs(intensity1 - intensity2)
            valence_similarity = 1.0 - abs(valence1 - valence2)
            arousal_similarity = 1.0 - abs(arousal1 - arousal2)
            
            return (emotion_similarity + intensity_similarity + valence_similarity + arousal_similarity) / 4
            
        except Exception as e:
            logger.error(f"❌ Failed to calculate emotional context similarity: {e}")
            return 0.0
    
    async def _calculate_temporal_similarity(self, memories: List[Dict[str, Any]]) -> float:
        """Calculate temporal similarity between memories"""
        try:
            # Extract timestamps
            timestamps = []
            for memory in memories:
                created_at = memory.get("created_at")
                if created_at:
                    timestamps.append(datetime.fromisoformat(created_at))
            
            if len(timestamps) < 2:
                return 0.0
            
            # Calculate temporal proximity
            time_diffs = []
            for i, time1 in enumerate(timestamps):
                for time2 in timestamps[i+1:]:
                    diff_hours = abs((time1 - time2).total_seconds()) / 3600
                    # Convert to similarity (closer in time = higher similarity)
                    similarity = max(0.0, 1.0 - (diff_hours / 168))  # 1 week = 0 similarity
                    time_diffs.append(similarity)
            
            return sum(time_diffs) / len(time_diffs) if time_diffs else 0.0
            
        except Exception as e:
            logger.error(f"❌ Failed to calculate temporal similarity: {e}")
            return 0.0
    
    async def _calculate_contextual_similarity(self, memories: List[Dict[str, Any]]) -> float:
        """Calculate contextual similarity between memories"""
        try:
            # Extract contexts
            contexts = []
            for memory in memories:
                context = memory.get("context", {})
                if context:
                    contexts.append(context)
            
            if len(contexts) < 2:
                return 0.0
            
            # Calculate context similarity
            similarities = []
            for i, context1 in enumerate(contexts):
                for context2 in contexts[i+1:]:
                    similarity = self._calculate_context_similarity(context1, context2)
                    similarities.append(similarity)
            
            return sum(similarities) / len(similarities) if similarities else 0.0
            
        except Exception as e:
            logger.error(f"❌ Failed to calculate contextual similarity: {e}")
            return 0.0
    
    def _calculate_context_similarity(
        self,
        context1: Dict[str, Any],
        context2: Dict[str, Any]
    ) -> float:
        """Calculate similarity between contexts"""
        try:
            # Extract context keys
            keys1 = set(context1.keys())
            keys2 = set(context2.keys())
            
            if not keys1 or not keys2:
                return 0.0
            
            # Calculate key overlap
            key_overlap = len(keys1.intersection(keys2)) / len(keys1.union(keys2))
            
            # Calculate value similarity for common keys
            value_similarities = []
            for key in keys1.intersection(keys2):
                value1 = context1[key]
                value2 = context2[key]
                
                if isinstance(value1, str) and isinstance(value2, str):
                    # String similarity
                    similarity = 1.0 if value1 == value2 else 0.0
                elif isinstance(value1, (int, float)) and isinstance(value2, (int, float)):
                    # Numeric similarity
                    similarity = 1.0 - abs(value1 - value2) / max(abs(value1), abs(value2), 1.0)
                else:
                    # Default similarity
                    similarity = 1.0 if value1 == value2 else 0.0
                
                value_similarities.append(similarity)
            
            value_similarity = sum(value_similarities) / len(value_similarities) if value_similarities else 0.0
            
            return (key_overlap + value_similarity) / 2
            
        except Exception as e:
            logger.error(f"❌ Failed to calculate context similarity: {e}")
            return 0.0
    
    async def _calculate_associative_similarity(self, memories: List[Dict[str, Any]]) -> float:
        """Calculate associative similarity between memories"""
        try:
            # Extract associations
            associations = []
            for memory in memories:
                memory_associations = memory.get("associations", [])
                associations.append(set(memory_associations))
            
            if len(associations) < 2:
                return 0.0
            
            # Calculate association overlap
            overlaps = []
            for i, assoc1 in enumerate(associations):
                for assoc2 in associations[i+1:]:
                    if assoc1 or assoc2:
                        overlap = len(assoc1.intersection(assoc2)) / len(assoc1.union(assoc2))
                        overlaps.append(overlap)
            
            return sum(overlaps) / len(overlaps) if overlaps else 0.0
            
        except Exception as e:
            logger.error(f"❌ Failed to calculate associative similarity: {e}")
            return 0.0
    
    async def _calculate_consciousness_similarity(self, memories: List[Dict[str, Any]]) -> float:
        """Calculate consciousness similarity between memories"""
        try:
            # Extract consciousness contexts
            consciousness_contexts = []
            for memory in memories:
                consciousness_context = memory.get("consciousness_context", {})
                if consciousness_context:
                    consciousness_contexts.append(consciousness_context)
            
            if len(consciousness_contexts) < 2:
                return 0.0
            
            # Calculate consciousness similarity
            similarities = []
            for i, context1 in enumerate(consciousness_contexts):
                for context2 in consciousness_contexts[i+1:]:
                    similarity = self._calculate_consciousness_context_similarity(context1, context2)
                    similarities.append(similarity)
            
            return sum(similarities) / len(similarities) if similarities else 0.0
            
        except Exception as e:
            logger.error(f"❌ Failed to calculate consciousness similarity: {e}")
            return 0.0
    
    def _calculate_consciousness_context_similarity(
        self,
        context1: Dict[str, Any],
        context2: Dict[str, Any]
    ) -> float:
        """Calculate similarity between consciousness contexts"""
        try:
            # Extract consciousness dimensions
            level1 = context1.get("consciousness_level", 0.5)
            level2 = context2.get("consciousness_level", 0.5)
            
            awareness1 = context1.get("self_awareness", 0.5)
            awareness2 = context2.get("self_awareness", 0.5)
            
            goals1 = set(context1.get("active_goals", []))
            goals2 = set(context2.get("active_goals", []))
            
            # Calculate similarity
            level_similarity = 1.0 - abs(level1 - level2)
            awareness_similarity = 1.0 - abs(awareness1 - awareness2)
            
            goal_similarity = 0.0
            if goals1 or goals2:
                goal_similarity = len(goals1.intersection(goals2)) / len(goals1.union(goals2))
            
            return (level_similarity + awareness_similarity + goal_similarity) / 3
            
        except Exception as e:
            logger.error(f"❌ Failed to calculate consciousness context similarity: {e}")
            return 0.0
    
    async def _perform_integration(
        self,
        memories: List[Dict[str, Any]],
        integration_type: IntegrationType
    ) -> Dict[str, Any]:
        """Perform memory integration"""
        try:
            synthesis_data = {
                "integration_type": integration_type.value,
                "memory_count": len(memories),
                "timestamp": datetime.now().isoformat()
            }
            
            if integration_type == IntegrationType.CONCEPTUAL_INTEGRATION:
                synthesis_data.update(await self._perform_conceptual_integration(memories))
            elif integration_type == IntegrationType.EMOTIONAL_INTEGRATION:
                synthesis_data.update(await self._perform_emotional_integration(memories))
            elif integration_type == IntegrationType.TEMPORAL_INTEGRATION:
                synthesis_data.update(await self._perform_temporal_integration(memories))
            elif integration_type == IntegrationType.CONTEXTUAL_INTEGRATION:
                synthesis_data.update(await self._perform_contextual_integration(memories))
            elif integration_type == IntegrationType.ASSOCIATIVE_INTEGRATION:
                synthesis_data.update(await self._perform_associative_integration(memories))
            elif integration_type == IntegrationType.CONSCIOUSNESS_INTEGRATION:
                synthesis_data.update(await self._perform_consciousness_integration(memories))
            
            return synthesis_data
            
        except Exception as e:
            logger.error(f"❌ Failed to perform integration: {e}")
            return {}
    
    async def _perform_conceptual_integration(self, memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform conceptual integration"""
        try:
            # Extract concepts from all memories
            all_concepts = []
            for memory in memories:
                concepts = memory.get("metadata", {}).get("concepts", [])
                all_concepts.extend(concepts)
            
            # Find common concepts
            concept_counts = {}
            for concept in all_concepts:
                concept_counts[concept] = concept_counts.get(concept, 0) + 1
            
            common_concepts = [concept for concept, count in concept_counts.items() if count > 1]
            
            return {
                "conceptual_integration": {
                    "total_concepts": len(set(all_concepts)),
                    "common_concepts": common_concepts,
                    "concept_diversity": len(set(all_concepts)) / len(all_concepts) if all_concepts else 0.0
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to perform conceptual integration: {e}")
            return {}
    
    async def _perform_emotional_integration(self, memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform emotional integration"""
        try:
            # Extract emotional contexts
            emotional_contexts = []
            for memory in memories:
                emotional_context = memory.get("emotional_context", {})
                if emotional_context:
                    emotional_contexts.append(emotional_context)
            
            if not emotional_contexts:
                return {"emotional_integration": {"emotion_count": 0}}
            
            # Calculate emotional synthesis
            emotions = [ctx.get("emotion", "neutral") for ctx in emotional_contexts]
            intensities = [ctx.get("intensity", 0.5) for ctx in emotional_contexts]
            valences = [ctx.get("valence", 0.0) for ctx in emotional_contexts]
            arousals = [ctx.get("arousal", 0.0) for ctx in emotional_contexts]
            
            # Find dominant emotion
            emotion_counts = {}
            for emotion in emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            dominant_emotion = max(emotion_counts, key=emotion_counts.get) if emotion_counts else "neutral"
            
            # Calculate average emotional dimensions
            avg_intensity = sum(intensities) / len(intensities)
            avg_valence = sum(valences) / len(valences)
            avg_arousal = sum(arousals) / len(arousals)
            
            return {
                "emotional_integration": {
                    "emotion_count": len(emotional_contexts),
                    "dominant_emotion": dominant_emotion,
                    "avg_intensity": avg_intensity,
                    "avg_valence": avg_valence,
                    "avg_arousal": avg_arousal,
                    "emotional_diversity": len(set(emotions)) / len(emotions) if emotions else 0.0
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to perform emotional integration: {e}")
            return {}
    
    async def _perform_temporal_integration(self, memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform temporal integration"""
        try:
            # Extract timestamps
            timestamps = []
            for memory in memories:
                created_at = memory.get("created_at")
                if created_at:
                    timestamps.append(datetime.fromisoformat(created_at))
            
            if not timestamps:
                return {"temporal_integration": {"time_span": 0}}
            
            # Calculate temporal metrics
            timestamps.sort()
            time_span = (timestamps[-1] - timestamps[0]).total_seconds() / 3600  # hours
            
            # Calculate temporal clustering
            time_diffs = [(timestamps[i+1] - timestamps[i]).total_seconds() / 3600 for i in range(len(timestamps)-1)]
            avg_time_diff = sum(time_diffs) / len(time_diffs) if time_diffs else 0.0
            
            return {
                "temporal_integration": {
                    "time_span": time_span,
                    "avg_time_diff": avg_time_diff,
                    "temporal_clustering": 1.0 / (1.0 + avg_time_diff) if avg_time_diff > 0 else 1.0
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to perform temporal integration: {e}")
            return {}
    
    async def _perform_contextual_integration(self, memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform contextual integration"""
        try:
            # Extract contexts
            contexts = []
            for memory in memories:
                context = memory.get("context", {})
                if context:
                    contexts.append(context)
            
            if not contexts:
                return {"contextual_integration": {"context_count": 0}}
            
            # Find common context keys
            all_keys = set()
            for context in contexts:
                all_keys.update(context.keys())
            
            common_keys = set(all_keys)
            for context in contexts:
                common_keys = common_keys.intersection(context.keys())
            
            # Calculate context similarity
            context_similarities = []
            for i, context1 in enumerate(contexts):
                for context2 in contexts[i+1:]:
                    similarity = self._calculate_context_similarity(context1, context2)
                    context_similarities.append(similarity)
            
            avg_context_similarity = sum(context_similarities) / len(context_similarities) if context_similarities else 0.0
            
            return {
                "contextual_integration": {
                    "context_count": len(contexts),
                    "common_keys": list(common_keys),
                    "avg_similarity": avg_context_similarity
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to perform contextual integration: {e}")
            return {}
    
    async def _perform_associative_integration(self, memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform associative integration"""
        try:
            # Extract associations
            all_associations = []
            for memory in memories:
                associations = memory.get("associations", [])
                all_associations.extend(associations)
            
            # Find common associations
            association_counts = {}
            for association in all_associations:
                association_counts[association] = association_counts.get(association, 0) + 1
            
            common_associations = [assoc for assoc, count in association_counts.items() if count > 1]
            
            return {
                "associative_integration": {
                    "total_associations": len(set(all_associations)),
                    "common_associations": common_associations,
                    "association_diversity": len(set(all_associations)) / len(all_associations) if all_associations else 0.0
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to perform associative integration: {e}")
            return {}
    
    async def _perform_consciousness_integration(self, memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform consciousness integration"""
        try:
            # Extract consciousness contexts
            consciousness_contexts = []
            for memory in memories:
                consciousness_context = memory.get("consciousness_context", {})
                if consciousness_context:
                    consciousness_contexts.append(consciousness_context)
            
            if not consciousness_contexts:
                return {"consciousness_integration": {"context_count": 0}}
            
            # Calculate consciousness synthesis
            levels = [ctx.get("consciousness_level", 0.5) for ctx in consciousness_contexts]
            awarenesses = [ctx.get("self_awareness", 0.5) for ctx in consciousness_contexts]
            
            all_goals = []
            for ctx in consciousness_contexts:
                goals = ctx.get("active_goals", [])
                all_goals.extend(goals)
            
            # Calculate averages
            avg_level = sum(levels) / len(levels)
            avg_awareness = sum(awarenesses) / len(awarenesses)
            
            # Find common goals
            goal_counts = {}
            for goal in all_goals:
                goal_counts[goal] = goal_counts.get(goal, 0) + 1
            
            common_goals = [goal for goal, count in goal_counts.items() if count > 1]
            
            return {
                "consciousness_integration": {
                    "context_count": len(consciousness_contexts),
                    "avg_consciousness_level": avg_level,
                    "avg_self_awareness": avg_awareness,
                    "common_goals": common_goals,
                    "goal_diversity": len(set(all_goals)) / len(all_goals) if all_goals else 0.0
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to perform consciousness integration: {e}")
            return {}
    
    async def _calculate_coherence_score(
        self,
        memories: List[Dict[str, Any]],
        synthesis_data: Dict[str, Any]
    ) -> float:
        """Calculate coherence score for integrated memories"""
        try:
            if not synthesis_data:
                return 0.0
            
            coherence_factors = []
            
            # Check for conceptual coherence
            if "conceptual_integration" in synthesis_data:
                concept_data = synthesis_data["conceptual_integration"]
                concept_diversity = concept_data.get("concept_diversity", 0.0)
                coherence_factors.append(concept_diversity)
            
            # Check for emotional coherence
            if "emotional_integration" in synthesis_data:
                emotion_data = synthesis_data["emotional_integration"]
                emotional_diversity = emotion_data.get("emotional_diversity", 0.0)
                coherence_factors.append(1.0 - emotional_diversity)  # Lower diversity = higher coherence
            
            # Check for temporal coherence
            if "temporal_integration" in synthesis_data:
                temporal_data = synthesis_data["temporal_integration"]
                temporal_clustering = temporal_data.get("temporal_clustering", 0.0)
                coherence_factors.append(temporal_clustering)
            
            # Check for contextual coherence
            if "contextual_integration" in synthesis_data:
                context_data = synthesis_data["contextual_integration"]
                avg_similarity = context_data.get("avg_similarity", 0.0)
                coherence_factors.append(avg_similarity)
            
            # Check for associative coherence
            if "associative_integration" in synthesis_data:
                assoc_data = synthesis_data["associative_integration"]
                association_diversity = assoc_data.get("association_diversity", 0.0)
                coherence_factors.append(association_diversity)
            
            # Check for consciousness coherence
            if "consciousness_integration" in synthesis_data:
                consciousness_data = synthesis_data["consciousness_integration"]
                goal_diversity = consciousness_data.get("goal_diversity", 0.0)
                coherence_factors.append(goal_diversity)
            
            if not coherence_factors:
                return 0.0
            
            return sum(coherence_factors) / len(coherence_factors)
            
        except Exception as e:
            logger.error(f"❌ Failed to calculate coherence score: {e}")
            return 0.0
    
    def _calculate_integration_significance(
        self,
        integration_strength: float,
        coherence_score: float
    ) -> float:
        """Calculate integration significance"""
        try:
            # Weighted combination of strength and coherence
            significance = (integration_strength * 0.6) + (coherence_score * 0.4)
            return min(1.0, significance)
            
        except Exception as e:
            logger.error(f"❌ Failed to calculate integration significance: {e}")
            return 0.0
    
    async def _group_memories_for_integration(
        self,
        candidates: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Group memories for integration"""
        try:
            # Simple grouping based on similarity
            groups = []
            used_memories = set()
            
            for candidate in candidates:
                memory1_id = candidate["memory1"]["memory_id"]
                memory2_id = candidate["memory2"]["memory_id"]
                
                if memory1_id in used_memories or memory2_id in used_memories:
                    continue
                
                # Create new group
                group = {
                    "memory_ids": [memory1_id, memory2_id],
                    "memories": [candidate["memory1"], candidate["memory2"]],
                    "similarity": candidate["similarity"],
                    "integration_potential": candidate["integration_potential"]
                }
                
                groups.append(group)
                used_memories.add(memory1_id)
                used_memories.add(memory2_id)
            
            return groups
            
        except Exception as e:
            logger.error(f"❌ Failed to group memories for integration: {e}")
            return []
    
    def _determine_integration_type(self, memories: List[Dict[str, Any]]) -> IntegrationType:
        """Determine integration type based on memory characteristics"""
        try:
            # Check for conceptual memories
            conceptual_count = sum(1 for m in memories if m.get("memory_type") == "semantic")
            if conceptual_count >= len(memories) * 0.5:
                return IntegrationType.CONCEPTUAL_INTEGRATION
            
            # Check for emotional memories
            emotional_count = sum(1 for m in memories if m.get("memory_type") == "emotional")
            if emotional_count >= len(memories) * 0.5:
                return IntegrationType.EMOTIONAL_INTEGRATION
            
            # Check for temporal proximity
            timestamps = []
            for memory in memories:
                created_at = memory.get("created_at")
                if created_at:
                    timestamps.append(datetime.fromisoformat(created_at))
            
            if len(timestamps) >= 2:
                time_span = (max(timestamps) - min(timestamps)).total_seconds() / 3600
                if time_span < 24:  # Within 24 hours
                    return IntegrationType.TEMPORAL_INTEGRATION
            
            # Check for consciousness context
            consciousness_count = sum(1 for m in memories if m.get("consciousness_context"))
            if consciousness_count >= len(memories) * 0.5:
                return IntegrationType.CONSCIOUSNESS_INTEGRATION
            
            # Default to associative integration
            return IntegrationType.ASSOCIATIVE_INTEGRATION
            
        except Exception as e:
            logger.error(f"❌ Failed to determine integration type: {e}")
            return IntegrationType.ASSOCIATIVE_INTEGRATION
    
    async def _get_memories_by_ids(
        self,
        memory_ids: List[str],
        user_id: str
    ) -> List[Dict[str, Any]]:
        """Get memories by IDs"""
        try:
            cypher = """
            MATCH (u:User {user_id: $user_id})-[:HAS_MEMORY]->(m:AdvancedMemory)
            WHERE m.memory_id IN $memory_ids
            RETURN m
            """
            
            result = self.neo4j.execute_query(cypher, {
                "user_id": user_id,
                "memory_ids": memory_ids
            })
            
            memories = [record["m"] for record in result]
            return memories
            
        except Exception as e:
            logger.error(f"❌ Failed to get memories by IDs: {e}")
            return []
    
    async def _store_integration_result(
        self,
        integration_result: IntegrationResult,
        user_id: str
    ):
        """Store integration result in Neo4j"""
        try:
            cypher = """
            MERGE (u:User {user_id: $user_id})
            CREATE (ir:IntegrationResult {
                integration_id: $integration_id,
                memory_ids: $memory_ids,
                integration_type: $integration_type,
                integration_strength: $integration_strength,
                coherence_score: $coherence_score,
                synthesis_data: $synthesis_data,
                timestamp: $timestamp,
                significance: $significance
            })
            CREATE (u)-[:HAS_INTEGRATION]->(ir)
            
            RETURN ir.integration_id AS integration_id
            """
            
            result = self.neo4j.execute_write_query(cypher, {
                "user_id": user_id,
                "integration_id": integration_result.integration_id,
                "memory_ids": integration_result.memory_ids,
                "integration_type": integration_result.integration_type.value,
                "integration_strength": integration_result.integration_strength,
                "coherence_score": integration_result.coherence_score,
                "synthesis_data": json.dumps(integration_result.synthesis_data),
                "timestamp": integration_result.timestamp.isoformat(),
                "significance": integration_result.significance
            })
            
            logger.debug(f"✅ Stored integration result: {result}")
            
        except Exception as e:
            logger.error(f"❌ Failed to store integration result: {e}")

# Global instance
memory_integration_system = MemoryIntegrationSystem()
