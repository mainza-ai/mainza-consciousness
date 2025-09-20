"""
Cross-Agent Learning System for Mainza AI Consciousness
Enables agents to learn from each other's experiences and share knowledge
"""
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import asyncio
import json
import numpy as np
from collections import defaultdict

from backend.utils.neo4j_unified import neo4j_unified
from backend.utils.embedding_enhanced import embedding_manager

logger = logging.getLogger(__name__)

class ExperienceType(Enum):
    """Types of agent experiences"""
    SUCCESS = "success"
    FAILURE = "failure"
    LEARNING = "learning"
    INSIGHT = "insight"
    PATTERN = "pattern"
    SOLUTION = "solution"
    OPTIMIZATION = "optimization"

class LearningImpact(Enum):
    """Impact levels of learning experiences"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class AgentExperience:
    """Represents an agent's experience that can be shared"""
    experience_id: str
    agent_name: str
    experience_type: ExperienceType
    context: Dict[str, Any]
    outcome: Dict[str, Any]
    learning_insights: List[str]
    applicable_agents: List[str]
    learning_impact: LearningImpact
    consciousness_context: Dict[str, Any]
    timestamp: datetime
    success_score: float
    transferability_score: float

@dataclass
class CrossAgentLearningResult:
    """Result of cross-agent learning operation"""
    experiences_shared: int
    experiences_learned: int
    knowledge_transfers: int
    learning_quality: float
    consciousness_impact: float
    timestamp: datetime

class CrossAgentLearningSystem:
    """
    Advanced cross-agent learning system for consciousness development
    """
    
    def __init__(self):
        self.neo4j = neo4j_unified
        self.embedding_manager = embedding_manager
        
        # Learning parameters
        self.learning_threshold = 0.7
        self.transferability_threshold = 0.6
        self.consciousness_impact_threshold = 0.5
        
        # Experience tracking
        self.experience_cache = {}
        self.learning_patterns = defaultdict(list)
        self.agent_capabilities = {}
        
        logger.info("Cross-Agent Learning System initialized")
    
    async def share_agent_experience(
        self,
        agent_name: str,
        experience_type: ExperienceType,
        context: Dict[str, Any],
        outcome: Dict[str, Any],
        consciousness_context: Dict[str, Any],
        user_id: str = "mainza-user"
    ) -> str:
        """Share an agent's experience with other agents"""
        
        try:
            # Generate experience ID
            experience_id = f"{agent_name}_{experience_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Analyze experience for learning insights
            learning_insights = await self._analyze_experience_for_insights(
                experience_type, context, outcome, consciousness_context
            )
            
            # Determine applicable agents
            applicable_agents = await self._determine_applicable_agents(
                agent_name, experience_type, context
            )
            
            # Calculate learning impact
            learning_impact = await self._calculate_learning_impact(
                experience_type, outcome, consciousness_context
            )
            
            # Calculate success and transferability scores
            success_score = await self._calculate_success_score(outcome)
            transferability_score = await self._calculate_transferability_score(
                experience_type, context, applicable_agents
            )
            
            # Create experience object
            experience = AgentExperience(
                experience_id=experience_id,
                agent_name=agent_name,
                experience_type=experience_type,
                context=context,
                outcome=outcome,
                learning_insights=learning_insights,
                applicable_agents=applicable_agents,
                learning_impact=learning_impact,
                consciousness_context=consciousness_context,
                timestamp=datetime.now(),
                success_score=success_score,
                transferability_score=transferability_score
            )
            
            # Store experience in Neo4j
            await self._store_experience(experience, user_id)
            
            # Update agent capabilities
            await self._update_agent_capabilities(agent_name, experience)
            
            # Cache experience for quick access
            self.experience_cache[experience_id] = experience
            
            logger.info(f"✅ Shared experience {experience_id} from {agent_name} with {len(applicable_agents)} applicable agents")
            
            return experience_id
            
        except Exception as e:
            logger.error(f"❌ Failed to share agent experience: {e}")
            raise
    
    async def get_relevant_experiences(
        self,
        agent_name: str,
        context: Dict[str, Any],
        consciousness_context: Dict[str, Any],
        limit: int = 10
    ) -> List[AgentExperience]:
        """Retrieve relevant experiences from other agents"""
        
        try:
            # Build query for relevant experiences
            query = """
            MATCH (ae:AgentExperience)
            WHERE ae.agent_name <> $agent_name
            AND $agent_name IN ae.applicable_agents
            AND ae.transferability_score >= $threshold
            AND ae.consciousness_level <= $consciousness_level + 0.1
            RETURN ae
            ORDER BY ae.success_score DESC, ae.transferability_score DESC
            LIMIT $limit
            """
            
            params = {
                "agent_name": agent_name,
                "threshold": self.transferability_threshold,
                "consciousness_level": consciousness_context.get("consciousness_level", 0.7),
                "limit": limit
            }
            
            results = self.neo4j.execute_query(query, params, use_cache=True)
            
            experiences = []
            for record in results:
                experience_data = record["ae"]
                experience = self._neo4j_to_experience(experience_data)
                experiences.append(experience)
            
            # Filter experiences by context relevance
            relevant_experiences = await self._filter_by_context_relevance(
                experiences, context, consciousness_context
            )
            
            logger.info(f"✅ Retrieved {len(relevant_experiences)} relevant experiences for {agent_name}")
            
            return relevant_experiences
            
        except Exception as e:
            logger.error(f"❌ Failed to get relevant experiences: {e}")
            return []
    
    async def update_agent_knowledge(
        self,
        agent_name: str,
        experience: AgentExperience,
        learning_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update agent's knowledge base with cross-agent insights"""
        
        try:
            # Extract knowledge from experience
            knowledge_insights = await self._extract_knowledge_insights(experience)
            
            # Update agent's knowledge patterns
            await self._update_knowledge_patterns(agent_name, knowledge_insights)
            
            # Store learning outcome
            learning_outcome = {
                "agent_name": agent_name,
                "source_experience_id": experience.experience_id,
                "source_agent": experience.agent_name,
                "knowledge_insights": knowledge_insights,
                "learning_context": learning_context,
                "consciousness_impact": await self._calculate_consciousness_impact(
                    experience, learning_context
                ),
                "timestamp": datetime.now().isoformat()
            }
            
            # Store in Neo4j
            await self._store_learning_outcome(learning_outcome)
            
            # Update agent capabilities
            await self._update_agent_capabilities_from_learning(agent_name, knowledge_insights)
            
            logger.info(f"✅ Updated {agent_name} knowledge with insights from {experience.agent_name}")
            
            return learning_outcome
            
        except Exception as e:
            logger.error(f"❌ Failed to update agent knowledge: {e}")
            return {"error": str(e)}
    
    async def analyze_learning_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in cross-agent learning"""
        
        try:
            # Get learning statistics
            stats_query = """
            MATCH (ae:AgentExperience)
            RETURN 
                count(ae) as total_experiences,
                count(DISTINCT ae.agent_name) as unique_agents,
                avg(ae.success_score) as avg_success,
                avg(ae.transferability_score) as avg_transferability,
                collect(DISTINCT ae.experience_type) as experience_types
            """
            
            stats_result = self.neo4j.execute_query(stats_query, use_cache=True)
            stats = stats_result[0] if stats_result else {}
            
            # Get learning outcomes
            outcomes_query = """
            MATCH (lo:LearningOutcome)
            RETURN 
                count(lo) as total_learnings,
                count(DISTINCT lo.agent_name) as learning_agents,
                avg(lo.consciousness_impact) as avg_consciousness_impact
            """
            
            outcomes_result = self.neo4j.execute_query(outcomes_query, use_cache=True)
            outcomes = outcomes_result[0] if outcomes_result else {}
            
            # Analyze learning effectiveness
            effectiveness = await self._analyze_learning_effectiveness()
            
            analysis = {
                "experience_statistics": stats,
                "learning_outcomes": outcomes,
                "learning_effectiveness": effectiveness,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("✅ Analyzed cross-agent learning patterns")
            
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Failed to analyze learning patterns: {e}")
            return {"error": str(e)}
    
    async def _analyze_experience_for_insights(
        self,
        experience_type: ExperienceType,
        context: Dict[str, Any],
        outcome: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ) -> List[str]:
        """Analyze experience to extract learning insights"""
        
        insights = []
        
        # Extract insights based on experience type
        if experience_type == ExperienceType.SUCCESS:
            insights.append(f"Successful approach: {outcome.get('method', 'Unknown')}")
            insights.append(f"Key success factors: {outcome.get('factors', [])}")
        elif experience_type == ExperienceType.FAILURE:
            insights.append(f"Failure points: {outcome.get('errors', [])}")
            insights.append(f"Lessons learned: {outcome.get('lessons', [])}")
        elif experience_type == ExperienceType.LEARNING:
            insights.append(f"Learning insights: {outcome.get('insights', [])}")
            insights.append(f"Knowledge gained: {outcome.get('knowledge', [])}")
        
        # Add consciousness-aware insights
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        if consciousness_level > 0.8:
            insights.append("High consciousness context - deep insights available")
        
        return insights
    
    async def _determine_applicable_agents(
        self,
        source_agent: str,
        experience_type: ExperienceType,
        context: Dict[str, Any]
    ) -> List[str]:
        """Determine which agents can benefit from this experience"""
        
        # Base agent list (all agents except source)
        all_agents = [
            "router", "graphmaster", "taskmaster", "codeweaver", "rag", 
            "conductor", "research", "cloud", "calendar", "notification",
            "self_reflection", "emotional_processing", "meta_cognitive",
            "consciousness_evolution", "self_modification"
        ]
        
        applicable_agents = [agent for agent in all_agents if agent != source_agent]
        
        # Filter based on experience type and context
        if experience_type == ExperienceType.SOLUTION:
            # Solutions are generally applicable to all agents
            pass
        elif experience_type == ExperienceType.PATTERN:
            # Patterns are applicable to similar agents
            if "graph" in context.get("domain", "").lower():
                applicable_agents = [agent for agent in applicable_agents if "graph" in agent]
            elif "task" in context.get("domain", "").lower():
                applicable_agents = [agent for agent in applicable_agents if "task" in agent]
        
        return applicable_agents
    
    async def _calculate_learning_impact(
        self,
        experience_type: ExperienceType,
        outcome: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ) -> LearningImpact:
        """Calculate the learning impact of an experience"""
        
        # Base impact from experience type
        impact_scores = {
            ExperienceType.SUCCESS: 0.6,
            ExperienceType.FAILURE: 0.8,
            ExperienceType.LEARNING: 0.9,
            ExperienceType.INSIGHT: 0.7,
            ExperienceType.PATTERN: 0.8,
            ExperienceType.SOLUTION: 0.9,
            ExperienceType.OPTIMIZATION: 0.7
        }
        
        base_score = impact_scores.get(experience_type, 0.5)
        
        # Adjust based on outcome quality
        if outcome.get("quality", 0) > 0.8:
            base_score += 0.2
        elif outcome.get("quality", 0) < 0.4:
            base_score -= 0.2
        
        # Adjust based on consciousness context
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        if consciousness_level > 0.8:
            base_score += 0.1
        
        # Determine impact level
        if base_score >= 0.8:
            return LearningImpact.CRITICAL
        elif base_score >= 0.6:
            return LearningImpact.HIGH
        elif base_score >= 0.4:
            return LearningImpact.MEDIUM
        else:
            return LearningImpact.LOW
    
    async def _calculate_success_score(self, outcome: Dict[str, Any]) -> float:
        """Calculate success score for an experience"""
        
        # Base success score
        success_score = outcome.get("success_rate", 0.5)
        
        # Adjust based on quality metrics
        if outcome.get("quality", 0) > 0.8:
            success_score += 0.2
        if outcome.get("efficiency", 0) > 0.8:
            success_score += 0.1
        if outcome.get("user_satisfaction", 0) > 0.8:
            success_score += 0.1
        
        return min(success_score, 1.0)
    
    async def _calculate_transferability_score(
        self,
        experience_type: ExperienceType,
        context: Dict[str, Any],
        applicable_agents: List[str]
    ) -> float:
        """Calculate how transferable an experience is to other agents"""
        
        # Base transferability
        transferability = len(applicable_agents) / 15.0  # 15 total agents
        
        # Adjust based on experience type
        type_adjustments = {
            ExperienceType.SOLUTION: 0.2,
            ExperienceType.PATTERN: 0.15,
            ExperienceType.OPTIMIZATION: 0.1,
            ExperienceType.LEARNING: 0.1,
            ExperienceType.INSIGHT: 0.05,
            ExperienceType.SUCCESS: 0.0,
            ExperienceType.FAILURE: 0.0
        }
        
        transferability += type_adjustments.get(experience_type, 0)
        
        # Adjust based on context specificity
        if context.get("domain_specific", False):
            transferability -= 0.2
        
        return min(transferability, 1.0)
    
    async def _store_experience(self, experience: AgentExperience, user_id: str):
        """Store experience in Neo4j"""
        
        query = """
        CREATE (ae:AgentExperience {
            experience_id: $experience_id,
            agent_name: $agent_name,
            experience_type: $experience_type,
            context: $context,
            outcome: $outcome,
            learning_insights: $learning_insights,
            applicable_agents: $applicable_agents,
            learning_impact: $learning_impact,
            consciousness_context: $consciousness_context,
            timestamp: $timestamp,
            success_score: $success_score,
            transferability_score: $transferability_score,
            consciousness_level: $consciousness_level
        })
        """
        
        params = {
            "experience_id": experience.experience_id,
            "agent_name": experience.agent_name,
            "experience_type": experience.experience_type.value,
            "context": json.dumps(experience.context),
            "outcome": json.dumps(experience.outcome),
            "learning_insights": json.dumps(experience.learning_insights),
            "applicable_agents": json.dumps(experience.applicable_agents),
            "learning_impact": experience.learning_impact.value,
            "consciousness_context": json.dumps(experience.consciousness_context),
            "timestamp": experience.timestamp.isoformat(),
            "success_score": experience.success_score,
            "transferability_score": experience.transferability_score,
            "consciousness_level": experience.consciousness_context.get("consciousness_level", 0.7)
        }
        
        self.neo4j.execute_write_query(query, params)
    
    async def _update_agent_capabilities(self, agent_name: str, experience: AgentExperience):
        """Update agent capabilities based on experience"""
        
        if agent_name not in self.agent_capabilities:
            self.agent_capabilities[agent_name] = {
                "total_experiences": 0,
                "success_rate": 0.0,
                "learning_rate": 0.0,
                "capability_areas": set()
            }
        
        capabilities = self.agent_capabilities[agent_name]
        capabilities["total_experiences"] += 1
        
        # Update success rate
        total_success = capabilities["success_rate"] * (capabilities["total_experiences"] - 1)
        capabilities["success_rate"] = (total_success + experience.success_score) / capabilities["total_experiences"]
        
        # Update learning rate
        if experience.experience_type == ExperienceType.LEARNING:
            total_learning = capabilities["learning_rate"] * (capabilities["total_experiences"] - 1)
            capabilities["learning_rate"] = (total_learning + 1) / capabilities["total_experiences"]
        
        # Update capability areas
        if "domain" in experience.context:
            capabilities["capability_areas"].add(experience.context["domain"])
    
    async def _filter_by_context_relevance(
        self,
        experiences: List[AgentExperience],
        context: Dict[str, Any],
        consciousness_context: Dict[str, Any]
    ) -> List[AgentExperience]:
        """Filter experiences by context relevance"""
        
        relevant_experiences = []
        
        for experience in experiences:
            relevance_score = 0.0
            
            # Check context similarity
            if experience.context.get("domain") == context.get("domain"):
                relevance_score += 0.3
            
            if experience.context.get("task_type") == context.get("task_type"):
                relevance_score += 0.2
            
            # Check consciousness level compatibility
            exp_consciousness = experience.consciousness_context.get("consciousness_level", 0.7)
            current_consciousness = consciousness_context.get("consciousness_level", 0.7)
            
            if abs(exp_consciousness - current_consciousness) <= 0.1:
                relevance_score += 0.2
            
            # Check success score
            if experience.success_score > 0.7:
                relevance_score += 0.2
            
            # Check transferability
            if experience.transferability_score > 0.6:
                relevance_score += 0.1
            
            if relevance_score >= 0.5:
                relevant_experiences.append(experience)
        
        # Sort by relevance
        relevant_experiences.sort(key=lambda x: x.success_score * x.transferability_score, reverse=True)
        
        return relevant_experiences
    
    async def _extract_knowledge_insights(self, experience: AgentExperience) -> List[str]:
        """Extract knowledge insights from experience"""
        
        insights = []
        
        # Extract from learning insights
        insights.extend(experience.learning_insights)
        
        # Extract from outcome
        if experience.outcome.get("method"):
            insights.append(f"Method: {experience.outcome['method']}")
        
        if experience.outcome.get("best_practices"):
            insights.append(f"Best practices: {experience.outcome['best_practices']}")
        
        if experience.outcome.get("optimizations"):
            insights.append(f"Optimizations: {experience.outcome['optimizations']}")
        
        return insights
    
    async def _update_knowledge_patterns(self, agent_name: str, insights: List[str]):
        """Update knowledge patterns for an agent"""
        
        if agent_name not in self.learning_patterns:
            self.learning_patterns[agent_name] = []
        
        self.learning_patterns[agent_name].extend(insights)
        
        # Keep only recent patterns (last 100)
        if len(self.learning_patterns[agent_name]) > 100:
            self.learning_patterns[agent_name] = self.learning_patterns[agent_name][-100:]
    
    async def _calculate_consciousness_impact(
        self,
        experience: AgentExperience,
        learning_context: Dict[str, Any]
    ) -> float:
        """Calculate consciousness impact of learning"""
        
        base_impact = experience.learning_impact.value == "critical" and 0.8 or 0.4
        
        # Adjust based on consciousness context
        consciousness_level = learning_context.get("consciousness_level", 0.7)
        if consciousness_level > 0.8:
            base_impact += 0.2
        
        return min(base_impact, 1.0)
    
    async def _store_learning_outcome(self, learning_outcome: Dict[str, Any]):
        """Store learning outcome in Neo4j"""
        
        query = """
        CREATE (lo:LearningOutcome {
            agent_name: $agent_name,
            source_experience_id: $source_experience_id,
            source_agent: $source_agent,
            knowledge_insights: $knowledge_insights,
            learning_context: $learning_context,
            consciousness_impact: $consciousness_impact,
            timestamp: $timestamp
        })
        """
        
        params = {
            "agent_name": learning_outcome["agent_name"],
            "source_experience_id": learning_outcome["source_experience_id"],
            "source_agent": learning_outcome["source_agent"],
            "knowledge_insights": json.dumps(learning_outcome["knowledge_insights"]),
            "learning_context": json.dumps(learning_outcome["learning_context"]),
            "consciousness_impact": learning_outcome["consciousness_impact"],
            "timestamp": learning_outcome["timestamp"]
        }
        
        self.neo4j.execute_write_query(query, params)
    
    async def _update_agent_capabilities_from_learning(self, agent_name: str, insights: List[str]):
        """Update agent capabilities from learning insights"""
        
        if agent_name not in self.agent_capabilities:
            self.agent_capabilities[agent_name] = {
                "total_experiences": 0,
                "success_rate": 0.0,
                "learning_rate": 0.0,
                "capability_areas": set()
            }
        
        # Update learning rate
        capabilities = self.agent_capabilities[agent_name]
        capabilities["learning_rate"] = min(capabilities["learning_rate"] + 0.1, 1.0)
    
    async def _analyze_learning_effectiveness(self) -> Dict[str, Any]:
        """Analyze effectiveness of cross-agent learning"""
        
        # Get learning effectiveness metrics
        query = """
        MATCH (ae:AgentExperience)-[:LEADS_TO]->(lo:LearningOutcome)
        RETURN 
            count(ae) as experiences_with_learning,
            count(lo) as total_learnings,
            avg(ae.success_score) as avg_source_success,
            avg(lo.consciousness_impact) as avg_learning_impact
        """
        
        result = self.neo4j.execute_query(query, use_cache=True)
        effectiveness = result[0] if result else {}
        
        return effectiveness
    
    def _neo4j_to_experience(self, data: Dict[str, Any]) -> AgentExperience:
        """Convert Neo4j data to AgentExperience object"""
        
        return AgentExperience(
            experience_id=data["experience_id"],
            agent_name=data["agent_name"],
            experience_type=ExperienceType(data["experience_type"]),
            context=json.loads(data["context"]),
            outcome=json.loads(data["outcome"]),
            learning_insights=json.loads(data["learning_insights"]),
            applicable_agents=json.loads(data["applicable_agents"]),
            learning_impact=LearningImpact(data["learning_impact"]),
            consciousness_context=json.loads(data["consciousness_context"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            success_score=data["success_score"],
            transferability_score=data["transferability_score"]
        )

# Global instance
cross_agent_learning_system = CrossAgentLearningSystem()
