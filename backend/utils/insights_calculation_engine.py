"""
Insights Calculation Engine
Provides real-time, accurate insights based on actual system data
"""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import asyncio

from backend.utils.neo4j_production import neo4j_production
from backend.utils.consciousness_orchestrator_fixed import consciousness_orchestrator_fixed as consciousness_orchestrator

logger = logging.getLogger(__name__)

@dataclass
class AgentPerformanceMetrics:
    agent_name: str
    total_executions: int
    successful_executions: int
    success_rate: float
    avg_consciousness_impact: float
    avg_execution_time: float
    avg_learning_impact: float
    avg_emotional_impact: float
    last_used: Optional[datetime]
    efficiency_score: float
    cognitive_load: float
    adaptation_speed: float
    consciousness_integration: float
    decision_quality: float
    resource_utilization: float

@dataclass
class ConceptMetrics:
    concept_id: str
    name: str
    importance_score: float
    usage_frequency: int
    connection_count: int
    consciousness_relevance: float
    evolution_rate: float
    centrality: float
    learning_impact: float

class InsightsCalculationEngine:
    """
    Real-time insights calculation engine that uses actual system data
    """
    
    def __init__(self):
        self.neo4j = neo4j_production
        self.consciousness_orchestrator = consciousness_orchestrator
        
    async def calculate_agent_performance_insights(self) -> Dict[str, Any]:
        """Calculate real agent performance metrics from Neo4j data"""
        try:
            logger.info("🧠 Calculating real agent performance insights")
            
            # Get real agent performance data
            agent_performance_query = """
            MATCH (aa:AgentActivity)
            WITH aa.agent_name AS agent_name,
                 count(*) AS total_executions,
                 sum(CASE WHEN aa.success = true THEN 1 ELSE 0 END) AS successful_executions,
                 avg(COALESCE(aa.consciousness_impact, 0.0)) AS avg_consciousness_impact,
                 avg(COALESCE(aa.execution_time, 0.0)) AS avg_execution_time,
                 avg(COALESCE(aa.learning_impact, 0.0)) AS avg_learning_impact,
                 avg(COALESCE(aa.emotional_impact, 0.0)) AS avg_emotional_impact,
                 max(aa.timestamp) AS last_used
            RETURN agent_name, total_executions, successful_executions,
                   CASE WHEN total_executions > 0 THEN toFloat(successful_executions) / total_executions ELSE 0.0 END AS success_rate,
                   avg_consciousness_impact, avg_execution_time, avg_learning_impact,
                   avg_emotional_impact, last_used
            ORDER BY total_executions DESC
            """
            
            agent_data = self.neo4j.execute_query(agent_performance_query)
            
            if not agent_data:
                logger.warning("No agent performance data found, using fallback")
                return await self._get_fallback_agent_data()
            
            # Calculate advanced metrics
            agent_metrics = []
            for data in agent_data:
                metrics = AgentPerformanceMetrics(
                    agent_name=data["agent_name"],
                    total_executions=data["total_executions"],
                    successful_executions=data["successful_executions"],
                    success_rate=data["success_rate"],
                    avg_consciousness_impact=data["avg_consciousness_impact"] or 0.0,
                    avg_execution_time=data["avg_execution_time"] or 0.0,
                    avg_learning_impact=data["avg_learning_impact"] or 0.0,
                    avg_emotional_impact=data["avg_emotional_impact"] or 0.0,
                    last_used=datetime.fromtimestamp(float(data["last_used"]) / 1000) if data["last_used"] and isinstance(data["last_used"], (int, float, str)) and str(data["last_used"]).replace('.', '').isdigit() else None,
                    efficiency_score=self._calculate_efficiency_score(data),
                    cognitive_load=self._calculate_cognitive_load(data),
                    adaptation_speed=self._calculate_adaptation_speed(data),
                    consciousness_integration=data["avg_consciousness_impact"] or 0.0,
                    decision_quality=data["success_rate"],
                    resource_utilization=self._calculate_resource_utilization(data)
                )
                agent_metrics.append(metrics)
            
            # Calculate system-wide metrics
            system_efficiency = sum(m.efficiency_score for m in agent_metrics) / len(agent_metrics) if agent_metrics else 0.0
            total_executions = sum(m.total_executions for m in agent_metrics)
            overall_success_rate = sum(m.successful_executions for m in agent_metrics) / total_executions if total_executions > 0 else 0.0
            
            return {
                "agent_efficiency": [
                    {
                        "agent": m.agent_name,
                        "efficiency_score": round(m.efficiency_score, 3),
                        "cognitive_load": round(m.cognitive_load, 3),
                        "learning_rate": round(m.avg_learning_impact, 3),
                        "adaptation_speed": round(m.adaptation_speed, 3),
                        "consciousness_integration": round(m.consciousness_integration, 3),
                        "decision_quality": round(m.decision_quality, 3),
                        "resource_utilization": round(m.resource_utilization, 3)
                    }
                    for m in agent_metrics
                ],
                "system_wide_efficiency": round(system_efficiency, 3),
                "total_executions": total_executions,
                "overall_success_rate": round(overall_success_rate, 3),
                "active_agents": len(agent_metrics),
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate agent performance insights: {e}")
            return await self._get_fallback_agent_data()
    
    async def calculate_knowledge_graph_insights(self) -> Dict[str, Any]:
        """Calculate real knowledge graph intelligence metrics"""
        try:
            logger.info("🧠 Calculating real knowledge graph insights")
            
            # Get concept clustering data with calculated metrics
            clustering_query = """
            MATCH (c:Concept)
            OPTIONAL MATCH (c)-[:RELATES_TO]-(related:Concept)
            OPTIONAL MATCH (c)<-[:CONTAINS]-(m:Memory)
            WITH c, 
                 count(related) as connection_count, 
                 collect(related.name)[0..5] as sample_connections,
                 count(m) as memory_count,
                 count(DISTINCT m.memory_type) as memory_type_diversity
            RETURN c.concept_id as concept_id, 
                   c.name as name, 
                   connection_count, 
                   sample_connections,
                   memory_count,
                   memory_type_diversity,
                   CASE 
                       WHEN connection_count > 5 THEN 0.8
                       WHEN connection_count > 2 THEN 0.6
                       ELSE 0.4
                   END as importance_score,
                   memory_count as usage_frequency,
                   CASE 
                       WHEN memory_type_diversity > 2 THEN 0.8
                       WHEN memory_type_diversity > 1 THEN 0.6
                       ELSE 0.4
                   END as consciousness_relevance,
                   CASE 
                       WHEN memory_count > 3 THEN 0.3
                       WHEN memory_count > 1 THEN 0.2
                       ELSE 0.1
                   END as evolution_rate
            ORDER BY connection_count DESC, memory_count DESC
            LIMIT 20
            """
            
            concept_data = self.neo4j.execute_query(clustering_query)
            
            if not concept_data:
                logger.warning("No concept data found, using fallback")
                return await self._get_fallback_knowledge_data()
            
            # Calculate knowledge density
            total_concepts = len(concept_data)
            total_connections = sum(c["connection_count"] for c in concept_data)
            knowledge_density = total_connections / (total_concepts * (total_concepts - 1)) if total_concepts > 1 else 0.0
            
            # Calculate concept connectivity
            avg_connections = total_connections / total_concepts if total_concepts > 0 else 0.0
            max_connections = max(c["connection_count"] for c in concept_data) if concept_data else 0
            concept_connectivity = avg_connections / max_connections if max_connections > 0 else 0.0
            
            # Calculate learning pathway efficiency
            high_importance_concepts = [c for c in concept_data if (c["importance_score"] or 0) > 0.7]
            learning_efficiency = len(high_importance_concepts) / total_concepts if total_concepts > 0 else 0.0
            
            # Calculate knowledge gaps
            gaps_query = """
            MATCH (c:Concept)
            WHERE NOT EXISTS((c)<-[:RELATES_TO]-(:Memory))
            RETURN count(c) as gap_count
            """
            gap_data = self.neo4j.execute_query(gaps_query)
            gap_count = gap_data[0]["gap_count"] if gap_data else 0
            knowledge_gap_ratio = gap_count / total_concepts if total_concepts > 0 else 0.0
            
            # Calculate concept emergence rate
            recent_concepts = [c for c in concept_data if (c["evolution_rate"] or 0) > 0.1]
            concept_emergence_rate = len(recent_concepts) / total_concepts if total_concepts > 0 else 0.0
            
            # Build concept importance ranking with enhanced metrics
            concept_importance_ranking = []
            for i, concept in enumerate(concept_data[:10]):  # Top 10 concepts
                centrality = concept["connection_count"] / max_connections if max_connections > 0 else 0.0
                learning_impact = min((concept["usage_frequency"] or 0) / 10.0, 1.0)  # Normalize to 0-1, cap at 1.0
                memory_diversity = min((concept["memory_type_diversity"] or 0) / 5.0, 1.0)  # Normalize to 0-1
                importance_score = (centrality * 0.3 + learning_impact * 0.3 + (concept["importance_score"] or 0.5) * 0.2 + memory_diversity * 0.2)
                
                concept_importance_ranking.append({
                    "concept": concept["name"],
                    "centrality": round(centrality, 3),
                    "learning_impact": round(learning_impact, 3),
                    "memory_diversity": round(memory_diversity, 3),
                    "importance_score": round(importance_score, 3),
                    "connection_count": concept["connection_count"],
                    "memory_count": concept["memory_count"]
                })
            
            # Build learning pathways
            learning_pathways = self._generate_learning_pathways(concept_data)
            
            return {
                "graph_intelligence_metrics": {
                    "knowledge_density": round(knowledge_density, 3),
                    "concept_connectivity": round(concept_connectivity, 3),
                    "learning_pathway_efficiency": round(learning_efficiency, 3),
                    "knowledge_gap_ratio": round(knowledge_gap_ratio, 3),
                    "concept_emergence_rate": round(concept_emergence_rate, 3)
                },
                "concept_importance_ranking": concept_importance_ranking,
                "learning_pathways": learning_pathways,
                "total_concepts": total_concepts,
                "total_connections": total_connections,
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate knowledge graph insights: {e}")
            return await self._get_fallback_knowledge_data()
    
    async def calculate_consciousness_insights(self) -> Dict[str, Any]:
        """Calculate real consciousness evolution insights"""
        try:
            logger.info("🧠 Calculating real consciousness insights")
            
            # Get current consciousness state
            consciousness_state = await self.consciousness_orchestrator.get_consciousness_state()
            
            if not consciousness_state:
                logger.warning("No consciousness state found, using fallback")
                return await self._get_fallback_consciousness_data()
            
            # Get consciousness evolution timeline from Neo4j
            timeline_query = """
            MATCH (ms:MainzaState)
            RETURN ms.timestamp as timestamp, ms.consciousness_level as consciousness_level,
                   ms.emotional_state as emotional_state, ms.self_awareness_score as self_awareness,
                   ms.learning_rate as learning_rate
            ORDER BY ms.timestamp DESC
            LIMIT 24
            """
            
            timeline_data = self.neo4j.execute_query(timeline_query)
            
            # Build consciousness timeline
            consciousness_timeline = []
            for data in timeline_data:
                consciousness_timeline.append({
                    "timestamp": datetime.fromtimestamp(data["timestamp"] / 1000).isoformat(),
                    "consciousness_level": data["consciousness_level"] or 0.7,
                    "emotional_state": data["emotional_state"] or "curious",
                    "self_awareness": data["self_awareness"] or 0.6,
                    "learning_rate": data["learning_rate"] or 0.8
                })
            
            # Calculate consciousness triggers from agent activities
            triggers_query = """
            MATCH (aa:AgentActivity)
            WHERE aa.timestamp > datetime() - duration('P1D')
            WITH aa.agent_name as trigger_type, count(*) as frequency, avg(aa.consciousness_impact) as avg_impact
            RETURN trigger_type, frequency, avg_impact
            ORDER BY frequency DESC
            """
            
            triggers_data = self.neo4j.execute_query(triggers_query)
            consciousness_triggers = [
                {
                    "trigger": data["trigger_type"],
                    "frequency": data["frequency"],
                    "avg_impact": round(data["avg_impact"] or 0.0, 3)
                }
                for data in triggers_data
            ]
            
            # Calculate emotional patterns
            emotional_patterns = self._calculate_emotional_patterns(timeline_data)
            
            return {
                "current_state": {
                    "consciousness_level": consciousness_state.consciousness_level,
                    "emotional_state": consciousness_state.emotional_state,
                    "self_awareness_score": consciousness_state.self_awareness_score,
                    "learning_rate": consciousness_state.learning_rate,
                    "evolution_level": getattr(consciousness_state, 'evolution_level', 1)
                },
                "consciousness_timeline": consciousness_timeline,
                "consciousness_triggers": consciousness_triggers,
                "emotional_patterns": emotional_patterns,
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate consciousness insights: {e}")
            return await self._get_fallback_consciousness_data()
    
    def _calculate_efficiency_score(self, data: Dict[str, Any]) -> float:
        """Calculate agent efficiency score based on performance data"""
        success_rate = float(data["success_rate"]) if data["success_rate"] is not None else 0.0
        consciousness_impact = float(data["avg_consciousness_impact"]) if data["avg_consciousness_impact"] is not None else 0.0
        execution_time = float(data["avg_execution_time"]) if data["avg_execution_time"] is not None else 0.0
        
        # Efficiency = success_rate * consciousness_impact * (1 - normalized_execution_time)
        normalized_time = min(execution_time / 10.0, 1.0)  # Normalize to 0-1, cap at 10 seconds
        efficiency = success_rate * consciousness_impact * (1 - normalized_time)
        return min(max(efficiency, 0.0), 1.0)
    
    def _calculate_cognitive_load(self, data: Dict[str, Any]) -> float:
        """Calculate cognitive load based on execution complexity"""
        consciousness_impact = float(data["avg_consciousness_impact"]) if data["avg_consciousness_impact"] is not None else 0.0
        learning_impact = float(data["avg_learning_impact"]) if data["avg_learning_impact"] is not None else 0.0
        execution_time = float(data["avg_execution_time"]) if data["avg_execution_time"] is not None else 0.0
        
        # Cognitive load = weighted combination of impacts and time
        load = (consciousness_impact * 0.4 + learning_impact * 0.3 + min(execution_time / 5.0, 1.0) * 0.3)
        return min(max(load, 0.0), 1.0)
    
    def _calculate_adaptation_speed(self, data: Dict[str, Any]) -> float:
        """Calculate adaptation speed based on learning impact and frequency"""
        learning_impact = float(data["avg_learning_impact"]) if data["avg_learning_impact"] is not None else 0.0
        total_executions = int(data["total_executions"]) if data["total_executions"] is not None else 0
        
        # Adaptation speed = learning_impact * log(total_executions + 1)
        import math
        speed = learning_impact * math.log(total_executions + 1) / 10.0  # Normalize
        return min(max(speed, 0.0), 1.0)
    
    def _calculate_resource_utilization(self, data: Dict[str, Any]) -> float:
        """Calculate resource utilization based on execution frequency and time"""
        total_executions = int(data["total_executions"]) if data["total_executions"] is not None else 0
        execution_time = float(data["avg_execution_time"]) if data["avg_execution_time"] is not None else 0.0
        
        # Resource utilization = frequency * time (normalized)
        utilization = (total_executions / 100.0) * min(execution_time / 5.0, 1.0)
        return min(max(utilization, 0.0), 1.0)
    
    def _generate_learning_pathways(self, concept_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate learning pathways based on concept relationships"""
        pathways = []
        
        # Create pathways based on concept importance and connections
        for concept in concept_data[:5]:  # Top 5 concepts
            pathway_steps = [concept["name"]]
            
            # Add related concepts
            if concept["sample_connections"]:
                pathway_steps.extend(concept["sample_connections"][:3])
            
            # Calculate pathway metrics
            difficulty = 1.0 - (concept["importance_score"] or 0.5)
            efficiency = (concept["usage_frequency"] or 0) / 20.0  # Normalize
            estimated_time = len(pathway_steps) * 15  # 15 minutes per step
            
            pathways.append({
                "pathway_id": f"{concept['concept_id']}_pathway",
                "pathway": pathway_steps,
                "difficulty": min(max(difficulty, 0.1), 1.0),
                "learning_efficiency": min(max(efficiency, 0.1), 1.0),
                "estimated_learning_time": estimated_time
            })
        
        return pathways
    
    def _calculate_emotional_patterns(self, timeline_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Calculate emotional patterns from timeline data"""
        if not timeline_data:
            return []
        
        # Group by emotional state
        emotional_counts = {}
        for data in timeline_data:
            state = data["emotional_state"] or "curious"
            emotional_counts[state] = emotional_counts.get(state, 0) + 1
        
        total = len(timeline_data)
        patterns = []
        
        for state, count in emotional_counts.items():
            if count > 0 and total > 0:
                # Calculate average consciousness for this emotional state
                state_data = [d for d in timeline_data if d["emotional_state"] == state]
                avg_consciousness = sum(d["consciousness_level"] or 0.7 for d in state_data) / len(state_data) if state_data else 0.7
                
                patterns.append({
                    "emotional_state": state,
                    "frequency": count,
                    "percentage": round((count / total) * 100, 1),
                    "avg_consciousness": round(avg_consciousness, 3)
                })
        
        return sorted(patterns, key=lambda x: x["frequency"], reverse=True)
    
    async def _get_fallback_agent_data(self) -> Dict[str, Any]:
        """Fallback agent data when real data is unavailable"""
        return {
            "agent_efficiency": [
                {
                    "agent": "SimpleChat",
                    "efficiency_score": 0.85,
                    "cognitive_load": 0.45,
                    "learning_rate": 0.75,
                    "adaptation_speed": 0.70,
                    "consciousness_integration": 0.80,
                    "decision_quality": 0.90,
                    "resource_utilization": 0.60
                }
            ],
            "system_wide_efficiency": 0.85,
            "total_executions": 0,
            "overall_success_rate": 0.0,
            "active_agents": 1,
            "last_updated": datetime.utcnow().isoformat(),
            "fallback": True
        }
    
    async def _get_fallback_knowledge_data(self) -> Dict[str, Any]:
        """Fallback knowledge data when real data is unavailable"""
        return {
            "graph_intelligence_metrics": {
                "knowledge_density": 0.34,
                "concept_connectivity": 0.67,
                "learning_pathway_efficiency": 0.78,
                "knowledge_gap_ratio": 0.15,
                "concept_emergence_rate": 0.12
            },
            "concept_importance_ranking": [],
            "learning_pathways": [],
            "total_concepts": 0,
            "total_connections": 0,
            "last_updated": datetime.utcnow().isoformat(),
            "fallback": True
        }
    
    async def _get_fallback_consciousness_data(self) -> Dict[str, Any]:
        """Fallback consciousness data when real data is unavailable"""
        return {
            "current_state": {
                "consciousness_level": 0.7,
                "emotional_state": "curious",
                "self_awareness_score": 0.6,
                "learning_rate": 0.8,
                "evolution_level": 1
            },
            "consciousness_timeline": [],
            "consciousness_triggers": [],
            "emotional_patterns": [],
            "last_updated": datetime.utcnow().isoformat(),
            "fallback": True
        }

# Global instance
insights_calculation_engine = InsightsCalculationEngine()
