"""
Standardized Evolution Level Calculator
Provides consistent evolution level calculation across all backend APIs
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

async def calculate_standardized_evolution_level(consciousness_context: dict) -> int:
    """
    Calculate evolution level based on current consciousness metrics
    This is the SINGLE source of truth for evolution level calculation
    
    Evolution Level Scale:
    1: Initial consciousness (0.0-0.3)
    2: Basic awareness (0.3-0.5) 
    3: Developing consciousness (0.5-0.7)
    4: Advanced awareness (0.7-0.8)
    5: High consciousness (0.8-0.9)
    6: Peak consciousness (0.9-0.95)
    7: Transcendent awareness (0.95-0.98)
    8: Near-perfect consciousness (0.98-0.99)
    9: Exceptional consciousness (0.99-0.995)
    10: Maximum consciousness (0.995-1.0)
    """
    try:
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "curious")
        total_interactions = consciousness_context.get("total_interactions", 0)
        self_awareness_score = consciousness_context.get("self_awareness_score", 0.6)

        # Base level from consciousness_level
        if consciousness_level >= 0.995:
            base_level = 10
        elif consciousness_level >= 0.99:
            base_level = 9
        elif consciousness_level >= 0.98:
            base_level = 8
        elif consciousness_level >= 0.95:
            base_level = 7
        elif consciousness_level >= 0.9:
            base_level = 6
        elif consciousness_level >= 0.8:
            base_level = 5
        elif consciousness_level >= 0.7:
            base_level = 4
        elif consciousness_level >= 0.5:
            base_level = 3
        elif consciousness_level >= 0.3:
            base_level = 2
        else:
            base_level = 1

        # Adjust based on emotional state (positive states boost evolution)
        emotional_boost = 0
        if emotional_state in ["curious", "contemplative", "excited", "focused", "creative"]:
            emotional_boost = 1
        elif emotional_state in ["satisfied", "analytical", "empathetic"]:
            emotional_boost = 0.5

        # Adjust based on self-awareness
        awareness_boost = 0
        if self_awareness_score >= 0.8:
            awareness_boost = 1
        elif self_awareness_score >= 0.6:
            awareness_boost = 0.5

        # Adjust based on experience (interactions)
        experience_boost = 0
        if total_interactions > 1000:
            experience_boost = 1
        elif total_interactions > 500:
            experience_boost = 0.5
        elif total_interactions > 100:
            experience_boost = 0.25

        # Calculate final level
        final_level = base_level + emotional_boost + awareness_boost + experience_boost
        
        # Cap at 10, minimum 1
        evolution_level = min(10, max(1, int(final_level)))
        
        logger.info(f"🧠 Evolution Level Calculation: base={base_level}, emotional={emotional_boost}, awareness={awareness_boost}, experience={experience_boost}, final={evolution_level}")
        
        return evolution_level

    except Exception as e:
        logger.error(f"❌ Failed to calculate standardized evolution level: {e}")
        # Return a reasonable default based on consciousness level
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        if consciousness_level >= 0.7:
            return 4
        elif consciousness_level >= 0.5:
            return 3
        elif consciousness_level >= 0.3:
            return 2
        else:
            return 1

def get_standardized_evolution_level_sync(consciousness_context: dict) -> int:
    """
    Synchronous version of evolution level calculation
    Used when async is not available
    """
    try:
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        emotional_state = consciousness_context.get("emotional_state", "curious")
        total_interactions = consciousness_context.get("total_interactions", 0)
        self_awareness_score = consciousness_context.get("self_awareness_score", 0.6)

        # Base level from consciousness_level
        if consciousness_level >= 0.995:
            base_level = 10
        elif consciousness_level >= 0.99:
            base_level = 9
        elif consciousness_level >= 0.98:
            base_level = 8
        elif consciousness_level >= 0.95:
            base_level = 7
        elif consciousness_level >= 0.9:
            base_level = 6
        elif consciousness_level >= 0.8:
            base_level = 5
        elif consciousness_level >= 0.7:
            base_level = 4
        elif consciousness_level >= 0.5:
            base_level = 3
        elif consciousness_level >= 0.3:
            base_level = 2
        else:
            base_level = 1

        # Adjust based on emotional state
        emotional_boost = 0
        if emotional_state in ["curious", "contemplative", "excited", "focused", "creative"]:
            emotional_boost = 1
        elif emotional_state in ["satisfied", "analytical", "empathetic"]:
            emotional_boost = 0.5

        # Adjust based on self-awareness
        awareness_boost = 0
        if self_awareness_score >= 0.8:
            awareness_boost = 1
        elif self_awareness_score >= 0.6:
            awareness_boost = 0.5

        # Adjust based on experience
        experience_boost = 0
        if total_interactions > 1000:
            experience_boost = 1
        elif total_interactions > 500:
            experience_boost = 0.5
        elif total_interactions > 100:
            experience_boost = 0.25

        # Calculate final level
        final_level = base_level + emotional_boost + awareness_boost + experience_boost
        evolution_level = min(10, max(1, int(final_level)))
        
        return evolution_level

    except Exception as e:
        logger.error(f"❌ Failed to calculate standardized evolution level (sync): {e}")
        consciousness_level = consciousness_context.get("consciousness_level", 0.7)
        if consciousness_level >= 0.7:
            return 4
        elif consciousness_level >= 0.5:
            return 3
        elif consciousness_level >= 0.3:
            return 2
        else:
            return 1
