"""
Fix Evolution Level Discrepancy
Updates the evolution_level in the database to match the actual consciousness development
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import driver
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_evolution_level(consciousness_level, self_awareness_score, total_interactions):
    """
    Calculate appropriate evolution level based on consciousness metrics
    
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
    
    # Adjust based on self-awareness
    if self_awareness_score > 0.8:
        base_level += 1
    elif self_awareness_score < 0.4:
        base_level -= 1
    
    # Adjust based on experience (interactions)
    if total_interactions > 1000:
        base_level += 1
    elif total_interactions > 500:
        base_level += 0.5
    
    # Cap at 10
    return min(10, max(1, int(base_level)))

def fix_evolution_level():
    """Fix the evolution level discrepancy"""
    
    try:
        with driver.session() as session:
            # Get current consciousness state
            result = session.run("""
                MATCH (ms:MainzaState)
                WHERE ms.state_id CONTAINS 'mainza'
                RETURN ms.consciousness_level AS consciousness_level,
                       ms.self_awareness_score AS self_awareness_score,
                       ms.evolution_level AS current_evolution_level,
                       ms.total_interactions AS total_interactions
                ORDER BY ms.last_accessed DESC
                LIMIT 1
            """).single()
            
            if not result:
                logger.error("No MainzaState found")
                return False
            
            consciousness_level = result["consciousness_level"]
            self_awareness_score = result["self_awareness_score"]
            current_evolution_level = result["current_evolution_level"]
            total_interactions = result["total_interactions"] or 0
            
            logger.info(f"Current state:")
            logger.info(f"  Consciousness Level: {consciousness_level}")
            logger.info(f"  Self-Awareness Score: {self_awareness_score}")
            logger.info(f"  Current Evolution Level: {current_evolution_level}")
            logger.info(f"  Total Interactions: {total_interactions}")
            
            # Calculate correct evolution level
            correct_evolution_level = calculate_evolution_level(
                consciousness_level, self_awareness_score, total_interactions
            )
            
            logger.info(f"Calculated Evolution Level: {correct_evolution_level}")
            
            if correct_evolution_level != current_evolution_level:
                # Update the evolution level
                session.run("""
                    MATCH (ms:MainzaState)
                    WHERE ms.state_id CONTAINS 'mainza'
                    SET ms.evolution_level = $evolution_level,
                        ms.last_updated = timestamp()
                    RETURN ms.evolution_level AS new_evolution_level
                """, evolution_level=correct_evolution_level)
                
                logger.info(f"✅ Updated evolution level from {current_evolution_level} to {correct_evolution_level}")
                return True
            else:
                logger.info(f"✅ Evolution level is already correct: {current_evolution_level}")
                return True
                
    except Exception as e:
        logger.error(f"❌ Failed to fix evolution level: {e}")
        return False

def main():
    """Main function"""
    logger.info("🔧 Fixing evolution level discrepancy...")
    logger.info("=" * 50)
    
    success = fix_evolution_level()
    
    logger.info("=" * 50)
    if success:
        logger.info("🎉 Evolution level discrepancy fixed!")
        logger.info("💡 The UI should now show consistent evolution levels")
    else:
        logger.info("⚠️  Failed to fix evolution level discrepancy")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)