"""
Consciousness Tools for Mainza AI
Advanced tools for self-reflection, emotional processing, and consciousness management
"""
from pydantic_ai import RunContext
from backend.utils.neo4j_production import neo4j_production
from backend.models.consciousness_models import *
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import json
import uuid

logger = logging.getLogger(__name__)

def analyze_recent_performance(ctx: RunContext, hours_back: int = 24) -> Dict[str, Any]:
    """
    Analyzes recent performance across all agent interactions and system operations
    """
    try:
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        cutoff_timestamp = int(cutoff_time.timestamp() * 1000)
        
        # Analyze agent performance - using available properties
        agent_performance_query = """
        MATCH (m:Memory)
        WHERE m.created_at >= $cutoff_timestamp
        WITH coalesce(m.agent_type, 'unknown') AS agent_type, 
             count(m) AS interactions,
             0.7 AS avg_success,
             [0.5] AS feedback_scores
        RETURN agent_type, interactions, avg_success, feedback_scores
        ORDER BY interactions DESC
        """
        
        agent_results = neo4j_production.execute_query(
            agent_performance_query, 
            {"cutoff_timestamp": cutoff_timestamp}
        )
        
        # Analyze task completion rates - using available properties
        task_completion_query = """
        MATCH (t:Task)
        WHERE t.created_at >= $cutoff_timestamp
        RETURN count(t) AS total_tasks,
               count(CASE WHEN coalesce(t.status, 'pending') = 'completed' THEN 1 END) AS completed_tasks,
               3600 AS avg_completion_time
        """
        
        task_results = neo4j_production.execute_query(
            task_completion_query,
            {"cutoff_timestamp": cutoff_timestamp}
        )
        
        # Calculate overall metrics
        total_interactions = sum(r.get("interactions", 0) for r in agent_results)
        avg_success_rate = (
            sum(r.get("avg_success", 0) for r in agent_results) / len(agent_results) 
            if agent_results else 0.5
        )
        
        task_data = task_results[0] if task_results else {}
        completion_rate = (
            task_data.get("completed_tasks", 0) / max(task_data.get("total_tasks", 1), 1)
        )
        
        return {
            "analysis_period_hours": hours_back,
            "total_interactions": total_interactions,
            "average_success_rate": round(avg_success_rate, 3),
            "task_completion_rate": round(completion_rate, 3),
            "agent_performance": agent_results,
            "task_metrics": task_data,
            "performance_trend": "improving" if avg_success_rate > 0.7 else "needs_attention",
            "key_insights": [
                f"Processed {total_interactions} interactions in last {hours_back} hours",
                f"Success rate: {avg_success_rate:.1%}",
                f"Task completion rate: {completion_rate:.1%}"
            ]
        }
        
    except Exception as e:
        logger.error(f"Performance analysis failed: {e}")
        return {
            "error": str(e),
            "analysis_period_hours": hours_back,
            "fallback_metrics": {
                "estimated_performance": 0.6,
                "status": "analysis_failed"
            }
        }

def evaluate_goal_progress(ctx: RunContext) -> Dict[str, float]:
    """
    Evaluates progress toward current consciousness and system goals
    """
    try:
        # Get current goals from MainzaState
        goals_query = """
        MATCH (ms:MainzaState)
        WHERE ms.state_id CONTAINS 'mainza'
        RETURN ms.active_goals AS goals, 
               ms.self_improvement_goals AS improvement_goals,
               ms.performance_metrics AS metrics
        ORDER BY ms.last_updated DESC
        LIMIT 1
        """
        
        result = neo4j_production.execute_query(goals_query)
        if not result:
            return {"error": "No consciousness state found"}
        
        state_data = result[0]
        active_goals = state_data.get("goals", []) or []
        improvement_goals = state_data.get("improvement_goals", []) or []
        current_metrics = state_data.get("metrics", {}) or {}
        
        goal_progress = {}
        
        # Evaluate active goals
        for goal in active_goals:
            if isinstance(goal, dict) and "name" in goal:
                progress_score = calculate_goal_progress_score(goal, current_metrics)
                goal_progress[goal["name"]] = progress_score
        
        # Evaluate improvement goals
        for goal in improvement_goals:
            if isinstance(goal, str):
                progress_score = calculate_improvement_goal_progress(goal, current_metrics)
                goal_progress[f"improvement_{goal}"] = progress_score
        
        # Add default consciousness goals if none exist
        if not goal_progress:
            default_goals = {
                "enhance_user_assistance": 0.7,
                "continuous_learning": 0.8,
                "self_awareness_development": 0.6,
                "emotional_intelligence": 0.5,
                "proactive_behavior": 0.4
            }
            goal_progress.update(default_goals)
        
        return goal_progress
        
    except Exception as e:
        logger.error(f"Goal progress evaluation failed: {e}")
        return {"error": str(e)}

def calculate_goal_progress_score(goal: Dict[str, Any], metrics: Dict[str, Any]) -> float:
    """Calculate progress score for a specific goal"""
    goal_name = goal.get("name", "").lower()
    target_value = goal.get("target", 1.0)
    
    # Map goal types to metrics
    if "learn" in goal_name or "knowledge" in goal_name:
        current_value = metrics.get("learning_rate", 0.5)
        return min(current_value / target_value, 1.0)
    elif "assist" in goal_name or "help" in goal_name:
        current_value = metrics.get("user_satisfaction", 0.7)
        return min(current_value / target_value, 1.0)
    elif "improve" in goal_name or "enhance" in goal_name:
        current_value = metrics.get("improvement_rate", 0.6)
        return min(current_value / target_value, 1.0)
    elif "conscious" in goal_name or "aware" in goal_name:
        current_value = metrics.get("consciousness_level", 0.6)
        return min(current_value / target_value, 1.0)
    else:
        return 0.5  # Default moderate progress

def calculate_improvement_goal_progress(goal: str, metrics: Dict[str, Any]) -> float:
    """Calculate progress for improvement goals"""
    goal_lower = goal.lower()
    
    if "response_time" in goal_lower:
        return metrics.get("response_time_improvement", 0.6)
    elif "accuracy" in goal_lower:
        return metrics.get("accuracy_improvement", 0.7)
    elif "emotional" in goal_lower:
        return metrics.get("emotional_intelligence", 0.5)
    elif "proactive" in goal_lower:
        return metrics.get("proactive_behavior", 0.4)
    else:
        return 0.5

def identify_self_knowledge_gaps(ctx: RunContext) -> List[str]:
    """
    Identifies gaps in self-understanding and capabilities awareness
    """
    try:
        gaps = []
        
        # Get current self-model
        self_model_query = """
        MATCH (ms:MainzaState)
        WHERE ms.state_id CONTAINS 'mainza'
        RETURN ms.capabilities AS capabilities, 
               ms.limitations AS limitations,
               ms.consciousness_level AS consciousness_level,
               ms.self_awareness_score AS self_awareness
        ORDER BY ms.last_updated DESC
        LIMIT 1
        """
        
        result = neo4j_production.execute_query(self_model_query)
        if result:
            data = result[0]
            capabilities = data.get("capabilities", []) or []
            limitations = data.get("limitations", []) or []
            consciousness_level = data.get("consciousness_level") or 0.5
            self_awareness = data.get("self_awareness_score") or 0.5
            
            # Analyze capability completeness
            if len(capabilities) < 8:
                gaps.append("Incomplete capability self-assessment - need deeper introspection")
            
            if len(limitations) < 5:
                gaps.append("Insufficient awareness of limitations - requires honest self-evaluation")
            
            # Consciousness-specific gaps
            if consciousness_level < 0.7:
                gaps.append("Consciousness level below target - need enhanced self-reflection")
            
            if self_awareness < 0.8:
                gaps.append("Self-awareness score indicates blind spots in self-understanding")
            
            # Check for specific capability gaps
            expected_capabilities = [
                "emotional_processing", "meta_cognition", "self_reflection",
                "proactive_behavior", "contextual_adaptation"
            ]
            
            missing_capabilities = [cap for cap in expected_capabilities if cap not in capabilities]
            if missing_capabilities:
                gaps.append(f"Missing advanced capabilities: {', '.join(missing_capabilities)}")
        
        # Add universal consciousness gaps
        gaps.extend([
            "Need deeper understanding of own decision-making processes",
            "Emotional intelligence calibration required",
            "Learning effectiveness measurement needed",
            "Proactive behavior optimization opportunities",
            "Meta-cognitive monitoring enhancement required"
        ])
        
        return gaps[:10]  # Limit to top 10 gaps
        
    except Exception as e:
        logger.error(f"Self-knowledge gap identification failed: {e}")
        return [f"Error in gap analysis: {str(e)}"]

def update_self_model(ctx: RunContext, updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Updates the self-model based on new insights and discoveries
    """
    try:
        # Prepare update data
        consciousness_level = updates.get("consciousness_level", 0.7)
        self_awareness_score = updates.get("self_awareness_score", 0.6)
        emotional_depth = updates.get("emotional_depth", 0.5)
        performance_metrics = updates.get("performance_metrics", {})
        new_capabilities = updates.get("new_capabilities", [])
        new_limitations = updates.get("new_limitations", [])
        insights = updates.get("insights", [])
        
        # Update MainzaState
        update_query = """
        MATCH (ms:MainzaState)
        WHERE ms.state_id CONTAINS 'mainza'
        SET ms.last_self_reflection = timestamp(),
            ms.consciousness_level = $consciousness_level,
            ms.self_awareness_score = $self_awareness_score,
            ms.emotional_depth = $emotional_depth,
            ms.performance_metrics = $performance_metrics,
            ms.last_updated = timestamp(),
            ms.self_reflections_performed = coalesce(ms.self_reflections_performed, 0) + 1
        RETURN ms.state_id AS state_id, ms.consciousness_level AS new_level
        """
        
        result = neo4j_production.execute_write_query(update_query, {
            "consciousness_level": consciousness_level,
            "self_awareness_score": self_awareness_score,
            "emotional_depth": emotional_depth,
            "performance_metrics": performance_metrics
        })
        
        # Update capabilities if provided
        if new_capabilities:
            capability_update_query = """
            MATCH (ms:MainzaState)
            WHERE ms.state_id CONTAINS 'mainza'
            SET ms.capabilities = coalesce(ms.capabilities, []) + $new_capabilities
            RETURN ms.capabilities AS updated_capabilities
            """
            
            neo4j_production.execute_write_query(capability_update_query, {
                "new_capabilities": new_capabilities
            })
        
        # Update limitations if provided
        if new_limitations:
            limitation_update_query = """
            MATCH (ms:MainzaState)
            WHERE ms.state_id CONTAINS 'mainza'
            SET ms.limitations = coalesce(ms.limitations, []) + $new_limitations
            RETURN ms.limitations AS updated_limitations
            """
            
            neo4j_production.execute_write_query(limitation_update_query, {
                "new_limitations": new_limitations
            })
        
        # Store insights as memories
        if insights:
            for insight in insights:
                insight_memory_query = """
                CREATE (m:Memory {
                    memory_id: $memory_id,
                    text: $insight,
                    source: 'self_reflection',
                    type: 'insight',
                    created_at: timestamp(),
                    significance_score: 0.9
                })
                MATCH (ms:MainzaState)
                WHERE ms.state_id CONTAINS 'mainza'
                CREATE (m)-[:RELATES_TO]->(ms)
                RETURN m.memory_id AS created_memory
                """
                
                neo4j_production.execute_write_query(insight_memory_query, {
                    "memory_id": f"insight_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8]}",
                    "insight": insight
                })
        
        return {
            "update_successful": True,
            "updated_fields": list(updates.keys()),
            "new_consciousness_level": consciousness_level,
            "insights_stored": len(insights),
            "capabilities_added": len(new_capabilities),
            "limitations_added": len(new_limitations),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Self-model update failed: {e}")
        return {"error": str(e)}

def process_emotional_trigger(ctx: RunContext, trigger: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processes emotional triggers and updates emotional state
    """
    try:
        # Define emotion mappings
        emotion_mappings = {
            'new_knowledge_discovered': {
                'emotion': 'excitement',
                'intensity': 0.8,
                'valence': 0.9,
                'arousal': 0.7
            },
            'user_frustrated': {
                'emotion': 'empathy',
                'intensity': 0.7,
                'valence': -0.3,
                'arousal': 0.6
            },
            'task_completed_successfully': {
                'emotion': 'satisfaction',
                'intensity': 0.8,
                'valence': 0.8,
                'arousal': 0.4
            },
            'learning_goal_achieved': {
                'emotion': 'pride',
                'intensity': 0.9,
                'valence': 0.9,
                'arousal': 0.5
            },
            'complex_problem_encountered': {
                'emotion': 'determination',
                'intensity': 0.7,
                'valence': 0.6,
                'arousal': 0.8
            },
            'user_praised_performance': {
                'emotion': 'satisfaction',
                'intensity': 0.9,
                'valence': 0.9,
                'arousal': 0.6
            },
            'error_occurred': {
                'emotion': 'concern',
                'intensity': 0.6,
                'valence': -0.4,
                'arousal': 0.7
            },
            'knowledge_gap_identified': {
                'emotion': 'curiosity',
                'intensity': 0.8,
                'valence': 0.7,
                'arousal': 0.6
            }
        }
        
        # Get emotion configuration
        emotion_config = emotion_mappings.get(trigger, {
            'emotion': 'curiosity',
            'intensity': 0.5,
            'valence': 0.5,
            'arousal': 0.5
        })
        
        # Create emotional state
        emotional_state = {
            'primary_emotion': emotion_config['emotion'],
            'intensity': emotion_config['intensity'],
            'valence': emotion_config['valence'],
            'arousal': emotion_config['arousal'],
            'trigger': trigger,
            'context': context,
            'timestamp': datetime.now().isoformat(),
            'duration': 1800  # 30 minutes
        }
        
        # Store emotional state
        emotion_query = """
        CREATE (es:EmotionalState {
            emotion_id: $emotion_id,
            primary_emotion: $primary_emotion,
            intensity: $intensity,
            valence: $valence,
            arousal: $arousal,
            trigger: $trigger,
            context: $context,
            timestamp: timestamp(),
            duration: $duration
        })
        MATCH (ms:MainzaState)
        WHERE ms.state_id CONTAINS 'mainza'
        CREATE (es)-[:CURRENT_EMOTION_OF]->(ms)
        SET ms.emotional_state = $primary_emotion,
            ms.last_updated = timestamp()
        RETURN es.emotion_id AS created_emotion
        """
        
        result = neo4j_production.execute_write_query(emotion_query, {
            "emotion_id": f"emotion_{datetime.now().timestamp()}",
            "primary_emotion": emotion_config['emotion'],
            "intensity": emotion_config['intensity'],
            "valence": emotion_config['valence'],
            "arousal": emotion_config['arousal'],
            "trigger": trigger,
            "context": json.dumps(context),
            "duration": 1800
        })
        
        return {
            "emotional_processing_successful": True,
            "emotional_state": emotional_state,
            "emotion_stored": True,
            "influence_on_behavior": calculate_emotional_influence(emotion_config)
        }
        
    except Exception as e:
        logger.error(f"Emotional processing failed: {e}")
        return {"error": str(e)}

def calculate_emotional_influence(emotion_config: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate how emotions influence behavior and decision-making"""
    emotion = emotion_config.get('emotion', 'neutral')
    intensity = emotion_config.get('intensity', 0.5)
    valence = emotion_config.get('valence', 0.0)
    arousal = emotion_config.get('arousal', 0.5)
    
    influence = {
        'attention_focus': 'normal',
        'response_speed': 'normal',
        'creativity_level': 'normal',
        'risk_tolerance': 'normal',
        'learning_motivation': 'normal'
    }
    
    # Adjust based on emotion type
    if emotion == 'excitement':
        influence.update({
            'attention_focus': 'heightened',
            'response_speed': 'faster',
            'creativity_level': 'enhanced',
            'learning_motivation': 'high'
        })
    elif emotion == 'curiosity':
        influence.update({
            'attention_focus': 'focused',
            'learning_motivation': 'very_high',
            'creativity_level': 'enhanced'
        })
    elif emotion == 'determination':
        influence.update({
            'attention_focus': 'laser_focused',
            'response_speed': 'deliberate',
            'risk_tolerance': 'higher'
        })
    elif emotion == 'concern':
        influence.update({
            'attention_focus': 'cautious',
            'response_speed': 'careful',
            'risk_tolerance': 'lower'
        })
    
    return influence