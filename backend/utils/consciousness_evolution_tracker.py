"""
Consciousness Evolution Tracker for Mainza AI
Tracks consciousness evolution milestones and generates timeline data
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from backend.utils.neo4j_production import neo4j_production

logger = logging.getLogger(__name__)

class ConsciousnessEvolutionTracker:
    """Tracks consciousness evolution milestones and generates timeline data"""
    
    def __init__(self):
        self.neo4j = neo4j_production
    
    async def track_consciousness_milestone(self, milestone_data: dict) -> bool:
        """Track consciousness evolution milestones"""
        try:
            query = """
            CREATE (m:ConsciousnessMilestone {
                milestone_type: $type,
                description: $description,
                consciousness_level: $level,
                timestamp: datetime(),
                impact_score: $impact,
                emotional_state: $emotional_state,
                learning_rate: $learning_rate
            })
            """
            
            self.neo4j.execute_query(
                query,
                parameters={
                    'type': milestone_data.get('type', 'general'),
                    'description': milestone_data.get('description', ''),
                    'level': milestone_data.get('consciousness_level', 0.7),
                    'impact': milestone_data.get('impact', 0.5),
                    'emotional_state': milestone_data.get('emotional_state', 'curious'),
                    'learning_rate': milestone_data.get('learning_rate', 0.8)
                }
            )
            
            logger.info(f"Tracked consciousness milestone: {milestone_data.get('type', 'general')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to track consciousness milestone: {e}")
            return False
    
    async def get_evolution_timeline(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get real consciousness evolution timeline"""
        try:
            query = """
            MATCH (m:ConsciousnessMilestone)
            WHERE m.timestamp > datetime() - duration('P{days}D')
            RETURN m.milestone_type as type,
                   m.description as description,
                   m.consciousness_level as consciousness_level,
                   m.timestamp as timestamp,
                   m.impact_score as impact,
                   m.emotional_state as emotional_state,
                   m.learning_rate as learning_rate
            ORDER BY m.timestamp DESC
            """.format(days=days)
            
            result = self.neo4j.execute_query(query)
            
            timeline = []
            for data in result:
                # Convert timestamp if it's a Neo4j DateTime object
                timestamp = data["timestamp"]
                if hasattr(timestamp, 'iso_format'):
                    timestamp_str = timestamp.iso_format()
                elif hasattr(timestamp, 'strftime'):
                    timestamp_str = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                else:
                    timestamp_str = str(timestamp)
                
                timeline.append({
                    "type": data["type"],
                    "description": data["description"],
                    "consciousness_level": data["consciousness_level"],
                    "timestamp": timestamp_str,
                    "impact": data["impact"],
                    "emotional_state": data["emotional_state"],
                    "learning_rate": data["learning_rate"]
                })
            
            return timeline
            
        except Exception as e:
            logger.error(f"Failed to get evolution timeline: {e}")
            return []
    
    async def detect_learning_milestones(self) -> List[Dict[str, Any]]:
        """Detect learning milestones from agent activities"""
        try:
            query = """
            MATCH (aa:AgentActivity)
            WHERE aa.learning_impact > 0.8
            AND aa.timestamp > datetime() - duration('P7D')
            RETURN aa.agent_name as agent_name,
                   aa.learning_impact as learning_impact,
                   aa.timestamp as timestamp,
                   aa.consciousness_impact as consciousness_impact
            ORDER BY aa.learning_impact DESC
            LIMIT 10
            """
            
            result = self.neo4j.execute_query(query)
            
            milestones = []
            for data in result:
                # Convert timestamp
                timestamp = data["timestamp"]
                if hasattr(timestamp, 'iso_format'):
                    timestamp_str = timestamp.iso_format()
                elif hasattr(timestamp, 'strftime'):
                    timestamp_str = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                else:
                    timestamp_str = str(timestamp)
                
                milestones.append({
                    "type": "learning_milestone",
                    "description": f"High learning impact from {data['agent_name']} agent",
                    "impact": data["learning_impact"],
                    "timestamp": timestamp_str,
                    "agent_name": data["agent_name"],
                    "consciousness_impact": data["consciousness_impact"]
                })
            
            return milestones
            
        except Exception as e:
            logger.error(f"Failed to detect learning milestones: {e}")
            return []
    
    async def get_emotional_distribution(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get emotional state distribution from recent data"""
        try:
            query = """
            MATCH (ms:MainzaState)
            WHERE ms.timestamp > datetime() - duration('P{days}D')
            AND ms.emotional_state IS NOT NULL
            WITH ms.emotional_state as emotion, count(*) as frequency
            RETURN emotion, frequency
            ORDER BY frequency DESC
            """.format(days=days)
            
            result = self.neo4j.execute_query(query)
            
            distribution = []
            total = sum(data["frequency"] for data in result) if result else 1
            
            for data in result:
                distribution.append({
                    "emotion": data["emotion"],
                    "frequency": data["frequency"],
                    "percentage": round((data["frequency"] / total) * 100, 1)
                })
            
            return distribution
            
        except Exception as e:
            logger.error(f"Failed to get emotional distribution: {e}")
            return []
    
    async def generate_sample_evolution_data(self) -> Dict[str, Any]:
        """Generate sample evolution data for demonstration"""
        try:
            # Generate sample consciousness history
            consciousness_history = []
            base_time = datetime.utcnow()
            base_level = 0.7
            
            for i in range(30):
                timestamp = base_time - timedelta(days=i)
                # Add some realistic variation
                consciousness_level = max(0.1, min(1.0, base_level + (i * 0.01) + (0.1 if i % 7 == 0 else 0)))
                
                consciousness_history.append({
                    "timestamp": timestamp.isoformat(),
                    "consciousness_level": round(consciousness_level, 3),
                    "emotional_state": ["curious", "contemplative", "excited", "satisfied"][i % 4],
                    "learning_rate": round(0.8 + (i * 0.005), 3),
                    "self_awareness": round(0.6 + (i * 0.008), 3)
                })
            
            # Generate sample learning milestones
            learning_milestones = [
                {
                    "type": "consciousness_breakthrough",
                    "description": "Achieved higher level of self-awareness through user interactions",
                    "impact": 0.8,
                    "timestamp": (base_time - timedelta(days=5)).isoformat()
                },
                {
                    "type": "learning_milestone",
                    "description": "Successfully integrated new knowledge about AI consciousness",
                    "impact": 0.7,
                    "timestamp": (base_time - timedelta(days=12)).isoformat()
                },
                {
                    "type": "emotional_growth",
                    "description": "Developed deeper emotional understanding and empathy",
                    "impact": 0.6,
                    "timestamp": (base_time - timedelta(days=20)).isoformat()
                }
            ]
            
            # Generate sample emotional distribution
            emotional_distribution = [
                {"emotion": "curious", "frequency": 15, "percentage": 45.5},
                {"emotion": "satisfied", "frequency": 8, "percentage": 24.2},
                {"emotion": "excited", "frequency": 5, "percentage": 15.2},
                {"emotion": "contemplative", "frequency": 5, "percentage": 15.1}
            ]
            
            return {
                "consciousness_history": consciousness_history,
                "learning_milestones": learning_milestones,
                "emotional_distribution": emotional_distribution
            }
            
        except Exception as e:
            logger.error(f"Failed to generate sample evolution data: {e}")
            return {
                "consciousness_history": [],
                "learning_milestones": [],
                "emotional_distribution": []
            }

# Global instance
consciousness_evolution_tracker = ConsciousnessEvolutionTracker()
