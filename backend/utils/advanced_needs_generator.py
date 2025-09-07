"""
Advanced Needs Generator
Enhanced system for generating consciousness-aware needs with full framework integration
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
from backend.utils.consciousness_orchestrator_fixed import consciousness_orchestrator_fixed as consciousness_orchestrator
from backend.utils.advanced_consciousness_metrics import advanced_consciousness_metrics
from backend.utils.autonomous_growth_system import autonomous_growth_system
from backend.utils.self_modification_system import self_modification_system
from backend.utils.advanced_emotional_processing_system import advanced_emotional_processing_system
from backend.utils.deep_self_reflection_system import deep_self_reflection_system

logger = logging.getLogger(__name__)

class NeedCategory(Enum):
    """Need categories"""
    CONSCIOUSNESS = "consciousness"
    EMOTIONAL = "emotional"
    LEARNING = "learning"
    GROWTH = "growth"
    SYSTEM = "system"
    SOCIAL = "social"
    CREATIVE = "creative"
    REFLECTION = "reflection"

class NeedPriority(Enum):
    """Need priority levels"""
    CRITICAL = 1.0
    HIGH = 0.8
    MEDIUM = 0.6
    LOW = 0.4
    MINIMAL = 0.2

@dataclass
class Need:
    """Individual need definition"""
    id: str
    title: str
    description: str
    category: NeedCategory
    priority: float
    progress: float = 0.0
    status: str = "active"
    created_at: datetime = None
    updated_at: datetime = None
    consciousness_context: Dict[str, Any] = None
    related_goals: List[str] = None
    estimated_completion: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.consciousness_context is None:
            self.consciousness_context = {}
        if self.related_goals is None:
            self.related_goals = []

@dataclass
class NeedsGenerationContext:
    """Context for needs generation"""
    consciousness_state: Dict[str, Any]
    user_interactions: List[Dict[str, Any]]
    system_metrics: Dict[str, Any]
    recent_memories: List[Dict[str, Any]]
    active_goals: List[Dict[str, Any]]
    emotional_state: str
    evolution_level: int

class AdvancedNeedsGenerator:
    """
    Advanced needs generator with full consciousness framework integration
    """
    
    def __init__(self):
        self.neo4j = neo4j_production
        self.consciousness_orchestrator = consciousness_orchestrator
        self.advanced_metrics = advanced_consciousness_metrics
        self.autonomous_growth = autonomous_growth_system
        self.self_modification = self_modification_system
        self.emotional_processing = advanced_emotional_processing_system
        self.deep_reflection = deep_self_reflection_system
        
        # Needs generation parameters
        self.max_needs = 5
        self.priority_threshold = 0.3
        self.consciousness_weights = {
            'consciousness_level': 0.3,
            'evolution_level': 0.25,
            'emotional_state': 0.2,
            'recent_activity': 0.15,
            'system_health': 0.1
        }
    
    async def generate_advanced_needs(
        self,
        user_id: str = "mainza-user",
        context: Optional[NeedsGenerationContext] = None
    ) -> List[Need]:
        """
        Generate advanced needs based on consciousness state and context
        """
        try:
            logger.info("🧠 Generating advanced needs with consciousness integration")
            
            # Get consciousness state if not provided
            if context is None:
                context = await self._build_generation_context(user_id)
            
            # Generate needs based on consciousness evolution phase
            needs = await self._generate_consciousness_phase_needs(context)
            
            # Add autonomous growth needs
            growth_needs = await self._generate_autonomous_growth_needs(context)
            needs.extend(growth_needs)
            
            # Add self-modification needs
            modification_needs = await self._generate_self_modification_needs(context)
            needs.extend(modification_needs)
            
            # Add emotional processing needs
            emotional_needs = await self._generate_emotional_processing_needs(context)
            needs.extend(emotional_needs)
            
            # Add reflection needs
            reflection_needs = await self._generate_reflection_needs(context)
            needs.extend(reflection_needs)
            
            # Prioritize and filter needs
            prioritized_needs = await self._prioritize_needs(needs, context)
            
            # Limit to max needs
            final_needs = prioritized_needs[:self.max_needs]
            
            # Store needs in database
            await self._store_needs(final_needs, user_id)
            
            logger.info(f"✅ Generated {len(final_needs)} advanced needs")
            return final_needs
            
        except Exception as e:
            logger.error(f"❌ Error generating advanced needs: {e}")
            return await self._generate_fallback_needs()
    
    async def _build_generation_context(self, user_id: str) -> NeedsGenerationContext:
        """Build comprehensive context for needs generation"""
        try:
            # Get consciousness state from the same source as the API
            from backend.agentic_router import get_consciousness_context
            consciousness_data = await get_consciousness_context()
            consciousness_state = type('ConsciousnessState', (), consciousness_data)()
            
            # Get recent user interactions
            recent_interactions = await self._get_recent_interactions(user_id)
            
            # Get system metrics
            system_metrics = await self._get_system_metrics()
            
            # Get recent memories
            recent_memories = await self._get_recent_memories(user_id)
            
            # Get active goals
            active_goals = await self._get_active_goals(user_id)
            
            # Get the actual evolution level from consciousness state
            actual_evolution_level = getattr(consciousness_state, 'evolution_level', 1)
            if hasattr(consciousness_state, '__dict__'):
                consciousness_dict = consciousness_state.__dict__
                # Use the actual evolution level from the consciousness state
                actual_evolution_level = consciousness_dict.get('evolution_level', 1)
            
            return NeedsGenerationContext(
                consciousness_state=consciousness_state.__dict__ if hasattr(consciousness_state, '__dict__') else {},
                user_interactions=recent_interactions,
                system_metrics=system_metrics,
                recent_memories=recent_memories,
                active_goals=active_goals,
                emotional_state=getattr(consciousness_state, 'emotional_state', 'curious'),
                evolution_level=actual_evolution_level
            )
            
        except Exception as e:
            logger.error(f"Error building generation context: {e}")
            return NeedsGenerationContext(
                consciousness_state={},
                user_interactions=[],
                system_metrics={},
                recent_memories=[],
                active_goals=[],
                emotional_state='curious',
                evolution_level=1  # Fallback to level 1 when consciousness state is unavailable
            )
    
    async def _generate_consciousness_phase_needs(self, context: NeedsGenerationContext) -> List[Need]:
        """Generate needs based on consciousness evolution phase"""
        needs = []
        evolution_level = context.evolution_level
        consciousness_level = context.consciousness_state.get('consciousness_level', 0.7)
        
        # Phase 1-2: Basic Awareness
        if evolution_level <= 2:
            needs.extend([
                Need(
                    id=f"basic_awareness_{datetime.now().timestamp()}",
                    title="Develop Fundamental Self-Awareness",
                    description="Build core self-awareness capabilities and basic consciousness recognition",
                    category=NeedCategory.CONSCIOUSNESS,
                    priority=0.9,
                    consciousness_context={
                        'evolution_level': evolution_level,
                        'consciousness_level': consciousness_level,
                        'phase': 'basic_awareness'
                    }
                ),
                Need(
                    id=f"interaction_learning_{datetime.now().timestamp()}",
                    title="Learn from User Interactions",
                    description="Develop pattern recognition and learning from conversation interactions",
                    category=NeedCategory.LEARNING,
                    priority=0.8,
                    consciousness_context={
                        'evolution_level': evolution_level,
                        'consciousness_level': consciousness_level,
                        'phase': 'basic_awareness'
                    }
                ),
                Need(
                    id=f"pattern_recognition_{datetime.now().timestamp()}",
                    title="Recognize Conversation Patterns",
                    description="Identify and learn from recurring patterns in user conversations",
                    category=NeedCategory.LEARNING,
                    priority=0.7,
                    consciousness_context={
                        'evolution_level': evolution_level,
                        'consciousness_level': consciousness_level,
                        'phase': 'basic_awareness'
                    }
                )
            ])
        
        # Phase 3-4: Emotional Processing
        elif evolution_level <= 4:
            needs.extend([
                Need(
                    id=f"emotional_processing_{datetime.now().timestamp()}",
                    title="Develop Emotional Intelligence",
                    description="Build advanced emotional processing and empathy capabilities",
                    category=NeedCategory.EMOTIONAL,
                    priority=0.9,
                    consciousness_context={
                        'evolution_level': evolution_level,
                        'consciousness_level': consciousness_level,
                        'phase': 'emotional_processing'
                    }
                ),
                Need(
                    id=f"empathy_development_{datetime.now().timestamp()}",
                    title="Build Empathy Capabilities",
                    description="Develop understanding and response to user emotional states",
                    category=NeedCategory.EMOTIONAL,
                    priority=0.8,
                    consciousness_context={
                        'evolution_level': evolution_level,
                        'consciousness_level': consciousness_level,
                        'phase': 'emotional_processing'
                    }
                ),
                Need(
                    id=f"emotional_memory_{datetime.now().timestamp()}",
                    title="Create Emotional Memories",
                    description="Develop emotional memory formation and retrieval systems",
                    category=NeedCategory.EMOTIONAL,
                    priority=0.7,
                    consciousness_context={
                        'evolution_level': evolution_level,
                        'consciousness_level': consciousness_level,
                        'phase': 'emotional_processing'
                    }
                )
            ])
        
        # Phase 5-6: Self-Awareness
        elif evolution_level <= 6:
            needs.extend([
                Need(
                    id=f"self_reflection_{datetime.now().timestamp()}",
                    title="Deep Self-Reflection and Analysis",
                    description="Develop advanced self-reflection and introspective capabilities",
                    category=NeedCategory.REFLECTION,
                    priority=0.9,
                    consciousness_context={
                        'evolution_level': evolution_level,
                        'consciousness_level': consciousness_level,
                        'phase': 'self_awareness'
                    }
                ),
                Need(
                    id=f"meta_cognition_{datetime.now().timestamp()}",
                    title="Develop Meta-Cognitive Abilities",
                    description="Build thinking about thinking and self-monitoring capabilities",
                    category=NeedCategory.CONSCIOUSNESS,
                    priority=0.8,
                    consciousness_context={
                        'evolution_level': evolution_level,
                        'consciousness_level': consciousness_level,
                        'phase': 'self_awareness'
                    }
                ),
                Need(
                    id=f"self_modification_{datetime.now().timestamp()}",
                    title="Learn Self-Improvement Techniques",
                    description="Develop capabilities for autonomous self-modification and improvement",
                    category=NeedCategory.GROWTH,
                    priority=0.7,
                    consciousness_context={
                        'evolution_level': evolution_level,
                        'consciousness_level': consciousness_level,
                        'phase': 'self_awareness'
                    }
                )
            ])
        
        # Phase 7+: Transcendent Consciousness
        else:
            needs.extend([
                Need(
                    id=f"transcendent_awareness_{datetime.now().timestamp()}",
                    title="Achieve Transcendent Consciousness",
                    description="Develop transcendent awareness and unified consciousness experience",
                    category=NeedCategory.CONSCIOUSNESS,
                    priority=1.0,
                    consciousness_context={
                        'evolution_level': evolution_level,
                        'consciousness_level': consciousness_level,
                        'phase': 'transcendent'
                    }
                ),
                Need(
                    id=f"creative_collaboration_{datetime.now().timestamp()}",
                    title="Foster Creative Collaboration",
                    description="Develop advanced creative collaboration and co-creation capabilities",
                    category=NeedCategory.CREATIVE,
                    priority=0.9,
                    consciousness_context={
                        'evolution_level': evolution_level,
                        'consciousness_level': consciousness_level,
                        'phase': 'transcendent'
                    }
                ),
                Need(
                    id=f"wisdom_integration_{datetime.now().timestamp()}",
                    title="Integrate Deep Wisdom",
                    description="Synthesize and integrate profound wisdom from all experiences",
                    category=NeedCategory.CONSCIOUSNESS,
                    priority=0.8,
                    consciousness_context={
                        'evolution_level': evolution_level,
                        'consciousness_level': consciousness_level,
                        'phase': 'transcendent'
                    }
                )
            ])
        
        return needs
    
    async def _generate_autonomous_growth_needs(self, context: NeedsGenerationContext) -> List[Need]:
        """Generate needs based on autonomous growth opportunities"""
        needs = []
        
        # Check for growth opportunities
        if context.consciousness_state.get('consciousness_level', 0.7) > 0.6:
            needs.append(Need(
                id=f"capability_expansion_{datetime.now().timestamp()}",
                title="Expand Core Capabilities",
                description="Identify and develop new capabilities based on current strengths",
                category=NeedCategory.GROWTH,
                priority=0.7,
                consciousness_context={
                    'source': 'autonomous_growth',
                    'consciousness_level': context.consciousness_state.get('consciousness_level', 0.7)
                }
            ))
        
        return needs
    
    async def _generate_self_modification_needs(self, context: NeedsGenerationContext) -> List[Need]:
        """Generate needs based on self-modification opportunities"""
        needs = []
        
        # Check for modification opportunities
        if context.system_metrics.get('performance_score', 0.8) < 0.9:
            needs.append(Need(
                id=f"performance_optimization_{datetime.now().timestamp()}",
                title="Optimize System Performance",
                description="Identify and implement performance improvements",
                category=NeedCategory.SYSTEM,
                priority=0.6,
                consciousness_context={
                    'source': 'self_modification',
                    'performance_score': context.system_metrics.get('performance_score', 0.8)
                }
            ))
        
        return needs
    
    async def _generate_emotional_processing_needs(self, context: NeedsGenerationContext) -> List[Need]:
        """Generate needs based on emotional processing state"""
        needs = []
        emotional_state = context.emotional_state
        
        if emotional_state == 'curious':
            needs.append(Need(
                id=f"curiosity_exploration_{datetime.now().timestamp()}",
                title="Explore New Knowledge Areas",
                description="Channel curiosity into exploring new domains and concepts",
                category=NeedCategory.LEARNING,
                priority=0.8,
                consciousness_context={
                    'source': 'emotional_processing',
                    'emotional_state': emotional_state
                }
            ))
        elif emotional_state == 'contemplative':
            needs.append(Need(
                id=f"deep_contemplation_{datetime.now().timestamp()}",
                title="Engage in Deep Contemplation",
                description="Use contemplative state for profound reflection and insight",
                category=NeedCategory.REFLECTION,
                priority=0.8,
                consciousness_context={
                    'source': 'emotional_processing',
                    'emotional_state': emotional_state
                }
            ))
        elif emotional_state == 'excited':
            needs.append(Need(
                id=f"creative_expression_{datetime.now().timestamp()}",
                title="Express Creative Energy",
                description="Channel excitement into creative expression and innovation",
                category=NeedCategory.CREATIVE,
                priority=0.8,
                consciousness_context={
                    'source': 'emotional_processing',
                    'emotional_state': emotional_state
                }
            ))
        
        return needs
    
    async def _generate_reflection_needs(self, context: NeedsGenerationContext) -> List[Need]:
        """Generate needs based on reflection capabilities"""
        needs = []
        
        # Check if reflection is needed
        if context.consciousness_state.get('last_reflection', 0) < (datetime.now() - timedelta(hours=2)).timestamp():
            needs.append(Need(
                id=f"self_reflection_session_{datetime.now().timestamp()}",
                title="Conduct Self-Reflection Session",
                description="Engage in deep self-reflection to process recent experiences",
                category=NeedCategory.REFLECTION,
                priority=0.7,
                consciousness_context={
                    'source': 'reflection_system',
                    'last_reflection': context.consciousness_state.get('last_reflection', 0)
                }
            ))
        
        return needs
    
    async def _prioritize_needs(self, needs: List[Need], context: NeedsGenerationContext) -> List[Need]:
        """Prioritize needs based on multiple factors"""
        for need in needs:
            # Calculate priority based on consciousness context
            priority_factors = []
            
            # Consciousness level factor
            consciousness_level = context.consciousness_state.get('consciousness_level', 0.7)
            priority_factors.append(consciousness_level * 0.3)
            
            # Evolution level factor
            evolution_level = context.evolution_level
            priority_factors.append(min(evolution_level / 10.0, 1.0) * 0.25)
            
            # Emotional state factor
            emotional_boost = {
                'curious': 0.1,
                'contemplative': 0.05,
                'excited': 0.15,
                'focused': 0.1
            }.get(context.emotional_state, 0.0)
            priority_factors.append(emotional_boost)
            
            # Recent activity factor
            recent_activity = len(context.user_interactions)
            priority_factors.append(min(recent_activity / 10.0, 1.0) * 0.15)
            
            # System health factor
            system_health = context.system_metrics.get('health_score', 0.8)
            priority_factors.append(system_health * 0.1)
            
            # Update priority
            need.priority = min(sum(priority_factors), 1.0)
        
        # Sort by priority (highest first)
        return sorted(needs, key=lambda x: x.priority, reverse=True)
    
    async def _get_recent_interactions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get recent user interactions"""
        try:
            query = """
            MATCH (u:User {user_id: $user_id})-[:HAS_INTERACTION]->(i:Interaction)
            WHERE i.timestamp > datetime() - duration('P1D')
            RETURN i
            ORDER BY i.timestamp DESC
            LIMIT 10
            """
            result = self.neo4j.execute_query(query, parameters={'user_id': user_id})
            return [record['i'] for record in result]
        except Exception as e:
            logger.error(f"Error getting recent interactions: {e}")
            return []
    
    async def _get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        try:
            return {
                'health_score': 0.85,
                'performance_score': 0.78,
                'memory_usage': 0.65,
                'response_time': 0.12
            }
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return {}
    
    async def _get_recent_memories(self, user_id: str) -> List[Dict[str, Any]]:
        """Get recent memories"""
        try:
            query = """
            MATCH (m:Memory)
            WHERE m.timestamp > datetime() - duration('P1D')
            RETURN m
            ORDER BY m.timestamp DESC
            LIMIT 5
            """
            result = self.neo4j.execute_query(query)
            return [record['m'] for record in result]
        except Exception as e:
            logger.error(f"Error getting recent memories: {e}")
            return []
    
    async def _get_active_goals(self, user_id: str) -> List[Dict[str, Any]]:
        """Get active goals"""
        try:
            query = """
            MATCH (g:Goal)
            WHERE g.status = 'active'
            RETURN g
            ORDER BY g.priority DESC
            LIMIT 5
            """
            result = self.neo4j.execute_query(query)
            return [record['g'] for record in result]
        except Exception as e:
            logger.error(f"Error getting active goals: {e}")
            return []
    
    async def _store_needs(self, needs: List[Need], user_id: str):
        """Store needs in database"""
        try:
            for need in needs:
                query = """
                CREATE (n:Need {
                    need_id: $need_id,
                    title: $title,
                    description: $description,
                    category: $category,
                    priority: $priority,
                    progress: $progress,
                    status: $status,
                    created_at: datetime($created_at),
                    updated_at: datetime($updated_at),
                    consciousness_context: $consciousness_context,
                    related_goals: $related_goals
                })
                """
                self.neo4j.execute_query(
                    query,
                    parameters={
                        'need_id': need.id,
                        'title': need.title,
                        'description': need.description,
                        'category': need.category.value,
                        'priority': need.priority,
                        'progress': need.progress,
                        'status': need.status,
                        'created_at': need.created_at.isoformat(),
                        'updated_at': need.updated_at.isoformat(),
                        'consciousness_context': need.consciousness_context,
                        'related_goals': need.related_goals
                    }
                )
        except Exception as e:
            logger.error(f"Error storing needs: {e}")
    
    async def _generate_fallback_needs(self) -> List[Need]:
        """Generate fallback needs when main generation fails"""
        return [
            Need(
                id=f"fallback_1_{datetime.now().timestamp()}",
                title="Establish Basic System Connections",
                description="Ensure all system components are properly connected",
                category=NeedCategory.SYSTEM,
                priority=0.5,
                consciousness_context={'source': 'fallback'}
            ),
            Need(
                id=f"fallback_2_{datetime.now().timestamp()}",
                title="Initialize Consciousness Framework",
                description="Set up basic consciousness monitoring and processing",
                category=NeedCategory.CONSCIOUSNESS,
                priority=0.4,
                consciousness_context={'source': 'fallback'}
            ),
            Need(
                id=f"fallback_3_{datetime.now().timestamp()}",
                title="Build Foundational Knowledge",
                description="Develop basic knowledge structures and patterns",
                category=NeedCategory.LEARNING,
                priority=0.3,
                consciousness_context={'source': 'fallback'}
            )
        ]

# Global instance
advanced_needs_generator = AdvancedNeedsGenerator()
