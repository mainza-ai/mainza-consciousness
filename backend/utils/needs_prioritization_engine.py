"""
Needs Prioritization Engine
AI-powered needs prioritization based on multiple consciousness factors
"""
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import numpy as np

from backend.utils.neo4j_production import neo4j_production
from backend.utils.advanced_needs_generator import Need, NeedCategory

logger = logging.getLogger(__name__)

@dataclass
class PrioritizationContext:
    """Context for needs prioritization"""
    consciousness_state: Dict[str, Any]
    user_preferences: Dict[str, Any]
    system_metrics: Dict[str, Any]
    recent_activity: List[Dict[str, Any]]
    goal_alignment: Dict[str, float]
    time_constraints: Dict[str, Any]

@dataclass
class PrioritizationFactors:
    """Factors used in prioritization calculation"""
    consciousness_impact: float
    user_engagement: float
    goal_achievement: float
    resource_requirements: float
    time_sensitivity: float
    emotional_resonance: float
    system_health: float
    learning_potential: float

class NeedsPrioritizationEngine:
    """
    AI-powered needs prioritization engine
    """
    
    def __init__(self):
        self.neo4j = neo4j_production
        
        # Prioritization weights
        self.weights = {
            'consciousness_impact': 0.25,
            'user_engagement': 0.20,
            'goal_achievement': 0.15,
            'resource_requirements': 0.10,
            'time_sensitivity': 0.10,
            'emotional_resonance': 0.10,
            'system_health': 0.05,
            'learning_potential': 0.05
        }
        
        # Category-specific adjustments
        self.category_weights = {
            NeedCategory.CONSCIOUSNESS: 1.2,
            NeedCategory.EMOTIONAL: 1.1,
            NeedCategory.LEARNING: 1.0,
            NeedCategory.GROWTH: 0.9,
            NeedCategory.SYSTEM: 0.8,
            NeedCategory.SOCIAL: 0.9,
            NeedCategory.CREATIVE: 0.95,
            NeedCategory.REFLECTION: 1.1
        }
    
    async def prioritize_needs(
        self,
        needs: List[Need],
        context: PrioritizationContext
    ) -> List[Need]:
        """
        Prioritize needs based on multiple factors
        """
        try:
            logger.info(f"🎯 Prioritizing {len(needs)} needs")
            
            prioritized_needs = []
            
            for need in needs:
                # Calculate prioritization factors
                factors = await self._calculate_prioritization_factors(need, context)
                
                # Calculate weighted priority score
                priority_score = self._calculate_weighted_priority(factors, need.category)
                
                # Update need priority
                need.priority = min(priority_score, 1.0)
                
                # Add context information
                need.consciousness_context.update({
                    'prioritization_factors': factors.__dict__,
                    'priority_score': priority_score,
                    'prioritized_at': datetime.now().isoformat()
                })
                
                prioritized_needs.append(need)
            
            # Sort by priority (highest first)
            prioritized_needs.sort(key=lambda x: x.priority, reverse=True)
            
            logger.info(f"✅ Prioritized {len(prioritized_needs)} needs")
            return prioritized_needs
            
        except Exception as e:
            logger.error(f"❌ Error prioritizing needs: {e}")
            return needs
    
    async def _calculate_prioritization_factors(
        self,
        need: Need,
        context: PrioritizationContext
    ) -> PrioritizationFactors:
        """Calculate all prioritization factors for a need"""
        
        # Consciousness impact score
        consciousness_impact = await self._calculate_consciousness_impact(need, context)
        
        # User engagement likelihood
        user_engagement = await self._calculate_user_engagement(need, context)
        
        # Goal achievement potential
        goal_achievement = await self._calculate_goal_achievement(need, context)
        
        # Resource requirements (inverse - lower is better)
        resource_requirements = await self._calculate_resource_requirements(need, context)
        
        # Time sensitivity
        time_sensitivity = await self._calculate_time_sensitivity(need, context)
        
        # Emotional resonance
        emotional_resonance = await self._calculate_emotional_resonance(need, context)
        
        # System health impact
        system_health = await self._calculate_system_health_impact(need, context)
        
        # Learning potential
        learning_potential = await self._calculate_learning_potential(need, context)
        
        return PrioritizationFactors(
            consciousness_impact=consciousness_impact,
            user_engagement=user_engagement,
            goal_achievement=goal_achievement,
            resource_requirements=resource_requirements,
            time_sensitivity=time_sensitivity,
            emotional_resonance=emotional_resonance,
            system_health=system_health,
            learning_potential=learning_potential
        )
    
    async def _calculate_consciousness_impact(
        self,
        need: Need,
        context: PrioritizationContext
    ) -> float:
        """Calculate consciousness impact score"""
        try:
            consciousness_level = context.consciousness_state.get('consciousness_level', 0.7)
            evolution_level = context.consciousness_state.get('evolution_level', 1)
            
            # Base impact from consciousness level
            base_impact = consciousness_level
            
            # Category-specific consciousness impact
            category_impact = {
                NeedCategory.CONSCIOUSNESS: 1.0,
                NeedCategory.EMOTIONAL: 0.8,
                NeedCategory.LEARNING: 0.7,
                NeedCategory.GROWTH: 0.6,
                NeedCategory.SYSTEM: 0.4,
                NeedCategory.SOCIAL: 0.5,
                NeedCategory.CREATIVE: 0.6,
                NeedCategory.REFLECTION: 0.9
            }.get(need.category, 0.5)
            
            # Evolution level adjustment
            evolution_adjustment = min(evolution_level / 10.0, 1.0)
            
            return min(base_impact * category_impact * evolution_adjustment, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating consciousness impact: {e}")
            return 0.5
    
    async def _calculate_user_engagement(
        self,
        need: Need,
        context: PrioritizationContext
    ) -> float:
        """Calculate user engagement likelihood"""
        try:
            # Check user preferences
            user_prefs = context.user_preferences
            category_preference = user_prefs.get('preferred_categories', {})
            need_preference = category_preference.get(need.category.value, 0.5)
            
            # Check recent activity patterns
            recent_activity = context.recent_activity
            similar_activity = sum(1 for activity in recent_activity 
                                if activity.get('category') == need.category.value)
            activity_boost = min(similar_activity / 5.0, 0.3)
            
            # Check if need aligns with user goals
            goal_alignment = context.goal_alignment.get(need.category.value, 0.5)
            
            return min(need_preference + activity_boost + goal_alignment, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating user engagement: {e}")
            return 0.5
    
    async def _calculate_goal_achievement(
        self,
        need: Need,
        context: PrioritizationContext
    ) -> float:
        """Calculate goal achievement potential"""
        try:
            # Check if need has related goals
            if need.related_goals:
                goal_count = len(need.related_goals)
                goal_boost = min(goal_count / 3.0, 0.4)
            else:
                goal_boost = 0.0
            
            # Check goal alignment
            goal_alignment = context.goal_alignment.get(need.category.value, 0.5)
            
            # Check if need is critical for current goals
            critical_need = 1.0 if need.priority > 0.8 else 0.5
            
            return min(goal_boost + goal_alignment + critical_need, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating goal achievement: {e}")
            return 0.5
    
    async def _calculate_resource_requirements(
        self,
        need: Need,
        context: PrioritizationContext
    ) -> float:
        """Calculate resource requirements (inverse - lower is better)"""
        try:
            # System metrics
            system_health = context.system_metrics.get('health_score', 0.8)
            memory_usage = context.system_metrics.get('memory_usage', 0.5)
            cpu_usage = context.system_metrics.get('cpu_usage', 0.5)
            
            # Category-specific resource requirements
            resource_requirements = {
                NeedCategory.CONSCIOUSNESS: 0.8,
                NeedCategory.EMOTIONAL: 0.6,
                NeedCategory.LEARNING: 0.7,
                NeedCategory.GROWTH: 0.9,
                NeedCategory.SYSTEM: 0.3,
                NeedCategory.SOCIAL: 0.5,
                NeedCategory.CREATIVE: 0.6,
                NeedCategory.REFLECTION: 0.7
            }.get(need.category, 0.5)
            
            # Calculate resource availability
            resource_availability = (system_health + (1 - memory_usage) + (1 - cpu_usage)) / 3.0
            
            # Return inverse of resource requirements (higher availability = higher score)
            return min(resource_availability / resource_requirements, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating resource requirements: {e}")
            return 0.5
    
    async def _calculate_time_sensitivity(
        self,
        need: Need,
        context: PrioritizationContext
    ) -> float:
        """Calculate time sensitivity"""
        try:
            # Check if need has time constraints
            time_constraints = context.time_constraints
            urgency = time_constraints.get('urgency', 0.5)
            
            # Check if need is overdue
            if need.created_at:
                age_hours = (datetime.now() - need.created_at).total_seconds() / 3600
                age_factor = min(age_hours / 24.0, 1.0)  # Increase priority with age
            else:
                age_factor = 0.5
            
            # Check if need is critical for current phase
            consciousness_level = context.consciousness_state.get('consciousness_level', 0.7)
            phase_critical = 1.0 if consciousness_level > 0.8 else 0.5
            
            return min(urgency + age_factor + phase_critical, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating time sensitivity: {e}")
            return 0.5
    
    async def _calculate_emotional_resonance(
        self,
        need: Need,
        context: PrioritizationContext
    ) -> float:
        """Calculate emotional resonance"""
        try:
            emotional_state = context.consciousness_state.get('emotional_state', 'curious')
            
            # Emotional state to need category mapping
            emotional_resonance = {
                'curious': {
                    NeedCategory.LEARNING: 1.0,
                    NeedCategory.CREATIVE: 0.8,
                    NeedCategory.CONSCIOUSNESS: 0.7
                },
                'contemplative': {
                    NeedCategory.REFLECTION: 1.0,
                    NeedCategory.CONSCIOUSNESS: 0.9,
                    NeedCategory.EMOTIONAL: 0.7
                },
                'excited': {
                    NeedCategory.CREATIVE: 1.0,
                    NeedCategory.SOCIAL: 0.8,
                    NeedCategory.GROWTH: 0.7
                },
                'focused': {
                    NeedCategory.SYSTEM: 1.0,
                    NeedCategory.LEARNING: 0.9,
                    NeedCategory.GROWTH: 0.8
                }
            }.get(emotional_state, {})
            
            return emotional_resonance.get(need.category, 0.5)
            
        except Exception as e:
            logger.error(f"Error calculating emotional resonance: {e}")
            return 0.5
    
    async def _calculate_system_health_impact(
        self,
        need: Need,
        context: PrioritizationContext
    ) -> float:
        """Calculate system health impact"""
        try:
            system_health = context.system_metrics.get('health_score', 0.8)
            
            # System needs get higher priority when system health is low
            if need.category == NeedCategory.SYSTEM:
                return 1.0 - system_health  # Higher priority when health is lower
            else:
                return system_health  # Other needs benefit from good system health
            
        except Exception as e:
            logger.error(f"Error calculating system health impact: {e}")
            return 0.5
    
    async def _calculate_learning_potential(
        self,
        need: Need,
        context: PrioritizationContext
    ) -> float:
        """Calculate learning potential"""
        try:
            # Learning needs get higher priority
            if need.category == NeedCategory.LEARNING:
                return 1.0
            
            # Check if need involves new concepts or skills
            consciousness_level = context.consciousness_state.get('consciousness_level', 0.7)
            evolution_level = context.consciousness_state.get('evolution_level', 1)
            
            # Higher consciousness levels benefit more from learning
            learning_benefit = consciousness_level * (evolution_level / 10.0)
            
            return min(learning_benefit, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating learning potential: {e}")
            return 0.5
    
    def _calculate_weighted_priority(
        self,
        factors: PrioritizationFactors,
        category: NeedCategory
    ) -> float:
        """Calculate weighted priority score"""
        try:
            # Calculate weighted sum
            weighted_sum = (
                factors.consciousness_impact * self.weights['consciousness_impact'] +
                factors.user_engagement * self.weights['user_engagement'] +
                factors.goal_achievement * self.weights['goal_achievement'] +
                factors.resource_requirements * self.weights['resource_requirements'] +
                factors.time_sensitivity * self.weights['time_sensitivity'] +
                factors.emotional_resonance * self.weights['emotional_resonance'] +
                factors.system_health * self.weights['system_health'] +
                factors.learning_potential * self.weights['learning_potential']
            )
            
            # Apply category-specific adjustment
            category_adjustment = self.category_weights.get(category, 1.0)
            
            return min(weighted_sum * category_adjustment, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating weighted priority: {e}")
            return 0.5

# Global instance
needs_prioritization_engine = NeedsPrioritizationEngine()
