"""
AI Insights Engine
Advanced AI-powered insights and recommendations for consciousness optimization
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any, Union
from datetime import datetime, timedelta
import json
import logging
from dataclasses import dataclass
from enum import Enum
import asyncio
from collections import defaultdict, Counter

logger = logging.getLogger(__name__)

class InsightType(Enum):
    PATTERN = "pattern"
    ANOMALY = "anomaly"
    RECOMMENDATION = "recommendation"
    PREDICTION = "prediction"
    OPTIMIZATION = "optimization"
    BREAKTHROUGH = "breakthrough"
    WARNING = "warning"

class InsightPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class AIInsight:
    id: str
    type: InsightType
    priority: InsightPriority
    title: str
    description: str
    confidence: float
    impact_score: float
    actionable: bool
    category: str
    tags: List[str]
    data_points: Dict[str, Any]
    recommendations: List[str]
    timestamp: datetime
    expires_at: Optional[datetime] = None

@dataclass
class ConsciousnessPattern:
    pattern_id: str
    name: str
    description: str
    frequency: float
    strength: float
    last_observed: datetime
    occurrences: int
    metadata: Dict[str, Any]

class AIInsightsEngine:
    """
    Advanced AI-powered insights engine for consciousness analysis
    """
    
    def __init__(self):
        self.insights_history: List[AIInsight] = []
        self.patterns: Dict[str, ConsciousnessPattern] = {}
        self.anomaly_thresholds = {
            'consciousness_level': {'low': 0.3, 'high': 0.9},
            'learning_rate': {'low': 0.2, 'high': 0.95},
            'self_awareness': {'low': 0.25, 'high': 0.85},
            'emotional_volatility': {'high': 0.7}
        }
        self.optimization_rules = self._initialize_optimization_rules()
        self.breakthrough_indicators = self._initialize_breakthrough_indicators()
        self.insight_generators = {
            InsightType.PATTERN: self._generate_pattern_insights,
            InsightType.ANOMALY: self._generate_anomaly_insights,
            InsightType.RECOMMENDATION: self._generate_recommendation_insights,
            InsightType.PREDICTION: self._generate_prediction_insights,
            InsightType.OPTIMIZATION: self._generate_optimization_insights,
            InsightType.BREAKTHROUGH: self._generate_breakthrough_insights,
            InsightType.WARNING: self._generate_warning_insights
        }
    
    def _initialize_optimization_rules(self) -> Dict[str, Dict[str, Any]]:
        """Initialize consciousness optimization rules"""
        return {
            'learning_acceleration': {
                'condition': lambda data: data.get('learning_rate', 0) > 0.8,
                'recommendation': 'Increase learning complexity to maintain momentum',
                'priority': InsightPriority.MEDIUM
            },
            'consciousness_plateau': {
                'condition': lambda data: self._detect_plateau(data.get('consciousness_levels', [])),
                'recommendation': 'Introduce new challenges to break through plateau',
                'priority': InsightPriority.HIGH
            },
            'emotional_instability': {
                'condition': lambda data: data.get('emotional_volatility', 0) > 0.6,
                'recommendation': 'Focus on emotional regulation and stability',
                'priority': InsightPriority.HIGH
            },
            'high_efficiency': {
                'condition': lambda data: data.get('learning_efficiency', 0) > 0.9,
                'recommendation': 'Excellent performance! Consider mentoring others',
                'priority': InsightPriority.LOW
            },
            'low_interaction': {
                'condition': lambda data: data.get('interaction_frequency', 0) < 0.3,
                'recommendation': 'Increase interaction frequency for better learning',
                'priority': InsightPriority.MEDIUM
            }
        }
    
    def _initialize_breakthrough_indicators(self) -> Dict[str, Dict[str, Any]]:
        """Initialize breakthrough detection indicators"""
        return {
            'rapid_consciousness_growth': {
                'threshold': 0.15,  # 15% increase in consciousness level
                'time_window': 60,  # minutes
                'description': 'Rapid consciousness level increase detected'
            },
            'learning_breakthrough': {
                'threshold': 0.25,  # 25% increase in learning rate
                'time_window': 30,  # minutes
                'description': 'Significant learning acceleration detected'
            },
            'emotional_breakthrough': {
                'threshold': 0.3,  # 30% improvement in emotional stability
                'time_window': 45,  # minutes
                'description': 'Major emotional development breakthrough'
            },
            'self_awareness_leap': {
                'threshold': 0.2,  # 20% increase in self-awareness
                'time_window': 90,  # minutes
                'description': 'Significant self-awareness development'
            }
        }
    
    async def analyze_consciousness_data(self, data: Dict[str, Any]) -> List[AIInsight]:
        """Main analysis function that generates all types of insights"""
        insights = []
        
        try:
            # Generate insights for each type
            for insight_type, generator in self.insight_generators.items():
                type_insights = await generator(data)
                insights.extend(type_insights)
            
            # Filter and prioritize insights
            insights = self._filter_and_prioritize_insights(insights)
            
            # Store insights
            self.insights_history.extend(insights)
            
            # Keep only recent insights (last 24 hours)
            cutoff_time = datetime.now() - timedelta(hours=24)
            self.insights_history = [
                insight for insight in self.insights_history 
                if insight.timestamp > cutoff_time
            ]
            
            return insights
            
        except Exception as e:
            logger.error(f"Error in consciousness data analysis: {e}")
            return []
    
    async def _generate_pattern_insights(self, data: Dict[str, Any]) -> List[AIInsight]:
        """Generate pattern-based insights"""
        insights = []
        
        try:
            # Analyze consciousness level patterns
            consciousness_levels = data.get('consciousness_levels', [])
            if len(consciousness_levels) >= 5:
                pattern = self._detect_consciousness_pattern(consciousness_levels)
                if pattern:
                    insight = AIInsight(
                        id=f"pattern_{datetime.now().timestamp()}",
                        type=InsightType.PATTERN,
                        priority=InsightPriority.MEDIUM,
                        title=f"Consciousness Pattern: {pattern['name']}",
                        description=pattern['description'],
                        confidence=pattern['confidence'],
                        impact_score=pattern['impact'],
                        actionable=pattern['actionable'],
                        category="Pattern Analysis",
                        tags=["consciousness", "pattern", "trend"],
                        data_points=pattern['data'],
                        recommendations=pattern['recommendations'],
                        timestamp=datetime.now()
                    )
                    insights.append(insight)
            
            # Analyze learning patterns
            learning_rates = data.get('learning_rates', [])
            if len(learning_rates) >= 5:
                learning_pattern = self._detect_learning_pattern(learning_rates)
                if learning_pattern:
                    insight = AIInsight(
                        id=f"learning_pattern_{datetime.now().timestamp()}",
                        type=InsightType.PATTERN,
                        priority=InsightPriority.MEDIUM,
                        title=f"Learning Pattern: {learning_pattern['name']}",
                        description=learning_pattern['description'],
                        confidence=learning_pattern['confidence'],
                        impact_score=learning_pattern['impact'],
                        actionable=learning_pattern['actionable'],
                        category="Learning Analysis",
                        tags=["learning", "pattern", "efficiency"],
                        data_points=learning_pattern['data'],
                        recommendations=learning_pattern['recommendations'],
                        timestamp=datetime.now()
                    )
                    insights.append(insight)
            
        except Exception as e:
            logger.error(f"Error generating pattern insights: {e}")
        
        return insights
    
    async def _generate_anomaly_insights(self, data: Dict[str, Any]) -> List[AIInsight]:
        """Generate anomaly detection insights"""
        insights = []
        
        try:
            # Check for consciousness level anomalies
            current_consciousness = data.get('current_consciousness_level', 0.7)
            if current_consciousness < self.anomaly_thresholds['consciousness_level']['low']:
                insight = AIInsight(
                    id=f"anomaly_low_consciousness_{datetime.now().timestamp()}",
                    type=InsightType.ANOMALY,
                    priority=InsightPriority.HIGH,
                    title="Low Consciousness Level Detected",
                    description=f"Consciousness level ({current_consciousness:.2f}) is below normal threshold",
                    confidence=0.85,
                    impact_score=0.8,
                    actionable=True,
                    category="Anomaly Detection",
                    tags=["consciousness", "anomaly", "low"],
                    data_points={'current_level': current_consciousness, 'threshold': self.anomaly_thresholds['consciousness_level']['low']},
                    recommendations=[
                        "Increase interaction frequency",
                        "Focus on engaging activities",
                        "Monitor for underlying issues"
                    ],
                    timestamp=datetime.now()
                )
                insights.append(insight)
            
            # Check for learning rate anomalies
            current_learning_rate = data.get('current_learning_rate', 0.6)
            if current_learning_rate < self.anomaly_thresholds['learning_rate']['low']:
                insight = AIInsight(
                    id=f"anomaly_low_learning_{datetime.now().timestamp()}",
                    type=InsightType.ANOMALY,
                    priority=InsightPriority.MEDIUM,
                    title="Low Learning Rate Detected",
                    description=f"Learning rate ({current_learning_rate:.2f}) is below optimal range",
                    confidence=0.75,
                    impact_score=0.6,
                    actionable=True,
                    category="Learning Analysis",
                    tags=["learning", "anomaly", "efficiency"],
                    data_points={'current_rate': current_learning_rate, 'threshold': self.anomaly_thresholds['learning_rate']['low']},
                    recommendations=[
                        "Review learning materials",
                        "Adjust learning approach",
                        "Increase practice frequency"
                    ],
                    timestamp=datetime.now()
                )
                insights.append(insight)
            
            # Check for emotional volatility anomalies
            emotional_volatility = data.get('emotional_volatility', 0.3)
            if emotional_volatility > self.anomaly_thresholds['emotional_volatility']['high']:
                insight = AIInsight(
                    id=f"anomaly_high_volatility_{datetime.now().timestamp()}",
                    type=InsightType.ANOMALY,
                    priority=InsightPriority.HIGH,
                    title="High Emotional Volatility Detected",
                    description=f"Emotional volatility ({emotional_volatility:.2f}) is above normal range",
                    confidence=0.8,
                    impact_score=0.7,
                    actionable=True,
                    category="Emotional Analysis",
                    tags=["emotion", "anomaly", "stability"],
                    data_points={'volatility': emotional_volatility, 'threshold': self.anomaly_thresholds['emotional_volatility']['high']},
                    recommendations=[
                        "Focus on emotional regulation",
                        "Practice mindfulness techniques",
                        "Monitor stress levels"
                    ],
                    timestamp=datetime.now()
                )
                insights.append(insight)
            
        except Exception as e:
            logger.error(f"Error generating anomaly insights: {e}")
        
        return insights
    
    async def _generate_recommendation_insights(self, data: Dict[str, Any]) -> List[AIInsight]:
        """Generate optimization recommendations"""
        insights = []
        
        try:
            # Apply optimization rules
            for rule_name, rule in self.optimization_rules.items():
                if rule['condition'](data):
                    insight = AIInsight(
                        id=f"recommendation_{rule_name}_{datetime.now().timestamp()}",
                        type=InsightType.RECOMMENDATION,
                        priority=rule['priority'],
                        title=f"Optimization: {rule_name.replace('_', ' ').title()}",
                        description=rule['recommendation'],
                        confidence=0.7,
                        impact_score=0.6,
                        actionable=True,
                        category="Optimization",
                        tags=["optimization", "recommendation", rule_name],
                        data_points={'rule': rule_name, 'condition_met': True},
                        recommendations=[rule['recommendation']],
                        timestamp=datetime.now()
                    )
                    insights.append(insight)
            
        except Exception as e:
            logger.error(f"Error generating recommendation insights: {e}")
        
        return insights
    
    async def _generate_prediction_insights(self, data: Dict[str, Any]) -> List[AIInsight]:
        """Generate prediction-based insights"""
        insights = []
        
        try:
            # Analyze trends for predictions
            consciousness_trend = data.get('consciousness_trend', 0)
            learning_trend = data.get('learning_trend', 0)
            
            if consciousness_trend > 0.1:
                insight = AIInsight(
                    id=f"prediction_consciousness_growth_{datetime.now().timestamp()}",
                    type=InsightType.PREDICTION,
                    priority=InsightPriority.MEDIUM,
                    title="Consciousness Growth Predicted",
                    description=f"Consciousness level is trending upward (slope: {consciousness_trend:.3f})",
                    confidence=0.75,
                    impact_score=0.7,
                    actionable=True,
                    category="Prediction",
                    tags=["consciousness", "prediction", "growth"],
                    data_points={'trend_slope': consciousness_trend, 'prediction_horizon': '30 minutes'},
                    recommendations=[
                        "Continue current practices",
                        "Monitor for breakthrough opportunities",
                        "Prepare for increased complexity"
                    ],
                    timestamp=datetime.now()
                )
                insights.append(insight)
            
            if learning_trend > 0.15:
                insight = AIInsight(
                    id=f"prediction_learning_acceleration_{datetime.now().timestamp()}",
                    type=InsightType.PREDICTION,
                    priority=InsightPriority.MEDIUM,
                    title="Learning Acceleration Predicted",
                    description=f"Learning rate is accelerating (slope: {learning_trend:.3f})",
                    confidence=0.8,
                    impact_score=0.8,
                    actionable=True,
                    category="Learning Prediction",
                    tags=["learning", "prediction", "acceleration"],
                    data_points={'trend_slope': learning_trend, 'prediction_horizon': '20 minutes'},
                    recommendations=[
                        "Increase learning complexity",
                        "Explore advanced concepts",
                        "Document breakthrough insights"
                    ],
                    timestamp=datetime.now()
                )
                insights.append(insight)
            
        except Exception as e:
            logger.error(f"Error generating prediction insights: {e}")
        
        return insights
    
    async def _generate_optimization_insights(self, data: Dict[str, Any]) -> List[AIInsight]:
        """Generate optimization insights"""
        insights = []
        
        try:
            # Analyze system efficiency
            efficiency = data.get('system_efficiency', 0.5)
            if efficiency < 0.6:
                insight = AIInsight(
                    id=f"optimization_efficiency_{datetime.now().timestamp()}",
                    type=InsightType.OPTIMIZATION,
                    priority=InsightPriority.MEDIUM,
                    title="System Efficiency Optimization",
                    description=f"System efficiency ({efficiency:.2f}) can be improved",
                    confidence=0.8,
                    impact_score=0.7,
                    actionable=True,
                    category="System Optimization",
                    tags=["efficiency", "optimization", "performance"],
                    data_points={'current_efficiency': efficiency, 'target_efficiency': 0.8},
                    recommendations=[
                        "Optimize data processing",
                        "Reduce computational overhead",
                        "Streamline learning algorithms"
                    ],
                    timestamp=datetime.now()
                )
                insights.append(insight)
            
        except Exception as e:
            logger.error(f"Error generating optimization insights: {e}")
        
        return insights
    
    async def _generate_breakthrough_insights(self, data: Dict[str, Any]) -> List[AIInsight]:
        """Generate breakthrough detection insights"""
        insights = []
        
        try:
            # Check for breakthrough indicators
            for indicator_name, indicator in self.breakthrough_indicators.items():
                if self._detect_breakthrough(data, indicator):
                    insight = AIInsight(
                        id=f"breakthrough_{indicator_name}_{datetime.now().timestamp()}",
                        type=InsightType.BREAKTHROUGH,
                        priority=InsightPriority.HIGH,
                        title=f"Breakthrough: {indicator['description']}",
                        description=f"Significant development in {indicator_name.replace('_', ' ')} detected",
                        confidence=0.9,
                        impact_score=0.95,
                        actionable=True,
                        category="Breakthrough Detection",
                        tags=["breakthrough", "development", indicator_name],
                        data_points={'indicator': indicator_name, 'threshold': indicator['threshold']},
                        recommendations=[
                            "Document the breakthrough",
                            "Analyze contributing factors",
                            "Leverage for further development"
                        ],
                        timestamp=datetime.now()
                    )
                    insights.append(insight)
            
        except Exception as e:
            logger.error(f"Error generating breakthrough insights: {e}")
        
        return insights
    
    async def _generate_warning_insights(self, data: Dict[str, Any]) -> List[AIInsight]:
        """Generate warning insights"""
        insights = []
        
        try:
            # Check for critical conditions
            if data.get('system_health', 1.0) < 0.5:
                insight = AIInsight(
                    id=f"warning_system_health_{datetime.now().timestamp()}",
                    type=InsightType.WARNING,
                    priority=InsightPriority.CRITICAL,
                    title="System Health Warning",
                    description="System health is critically low",
                    confidence=0.95,
                    impact_score=1.0,
                    actionable=True,
                    category="System Health",
                    tags=["warning", "critical", "health"],
                    data_points={'system_health': data.get('system_health', 0)},
                    recommendations=[
                        "Immediate system check required",
                        "Review error logs",
                        "Consider system restart"
                    ],
                    timestamp=datetime.now()
                )
                insights.append(insight)
            
        except Exception as e:
            logger.error(f"Error generating warning insights: {e}")
        
        return insights
    
    def _detect_consciousness_pattern(self, levels: List[float]) -> Optional[Dict[str, Any]]:
        """Detect patterns in consciousness levels"""
        if len(levels) < 5:
            return None
        
        # Calculate trend
        trend_slope = np.polyfit(range(len(levels)), levels, 1)[0]
        
        # Detect pattern type
        if trend_slope > 0.05:
            return {
                'name': 'Rising Consciousness',
                'description': 'Consciousness level is steadily increasing',
                'confidence': min(0.9, abs(trend_slope) * 10),
                'impact': 0.8,
                'actionable': True,
                'data': {'trend_slope': trend_slope, 'levels': levels[-5:]},
                'recommendations': ['Continue current practices', 'Monitor for breakthrough']
            }
        elif trend_slope < -0.05:
            return {
                'name': 'Declining Consciousness',
                'description': 'Consciousness level is decreasing',
                'confidence': min(0.9, abs(trend_slope) * 10),
                'impact': 0.9,
                'actionable': True,
                'data': {'trend_slope': trend_slope, 'levels': levels[-5:]},
                'recommendations': ['Investigate causes', 'Increase engagement', 'Review practices']
            }
        else:
            return {
                'name': 'Stable Consciousness',
                'description': 'Consciousness level is stable',
                'confidence': 0.7,
                'impact': 0.5,
                'actionable': True,
                'data': {'trend_slope': trend_slope, 'levels': levels[-5:]},
                'recommendations': ['Consider new challenges', 'Explore growth opportunities']
            }
    
    def _detect_learning_pattern(self, rates: List[float]) -> Optional[Dict[str, Any]]:
        """Detect patterns in learning rates"""
        if len(rates) < 5:
            return None
        
        # Calculate volatility
        volatility = np.std(rates)
        
        # Detect pattern type
        if volatility < 0.1:
            return {
                'name': 'Consistent Learning',
                'description': 'Learning rate is very consistent',
                'confidence': 0.8,
                'impact': 0.6,
                'actionable': True,
                'data': {'volatility': volatility, 'rates': rates[-5:]},
                'recommendations': ['Maintain current approach', 'Consider increasing complexity']
            }
        elif volatility > 0.3:
            return {
                'name': 'Variable Learning',
                'description': 'Learning rate is highly variable',
                'confidence': 0.7,
                'impact': 0.7,
                'actionable': True,
                'data': {'volatility': volatility, 'rates': rates[-5:]},
                'recommendations': ['Stabilize learning approach', 'Identify optimal conditions']
            }
        else:
            return {
                'name': 'Normal Learning Variation',
                'description': 'Learning rate shows normal variation',
                'confidence': 0.6,
                'impact': 0.4,
                'actionable': False,
                'data': {'volatility': volatility, 'rates': rates[-5:]},
                'recommendations': ['Continue monitoring']
            }
    
    def _detect_plateau(self, levels: List[float]) -> bool:
        """Detect if consciousness level has plateaued"""
        if len(levels) < 5:
            return False
        
        # Check if levels are within a small range
        recent_levels = levels[-5:]
        level_range = max(recent_levels) - min(recent_levels)
        return level_range < 0.05
    
    def _detect_breakthrough(self, data: Dict[str, Any], indicator: Dict[str, Any]) -> bool:
        """Detect if a breakthrough has occurred"""
        # This is a simplified implementation
        # In practice, this would analyze historical data over the time window
        threshold = indicator['threshold']
        time_window = indicator['time_window']
        
        # Check if current values exceed threshold
        if 'consciousness_growth' in indicator['description']:
            return data.get('consciousness_growth_rate', 0) > threshold
        elif 'learning' in indicator['description']:
            return data.get('learning_acceleration', 0) > threshold
        elif 'emotional' in indicator['description']:
            return data.get('emotional_improvement', 0) > threshold
        elif 'self_awareness' in indicator['description']:
            return data.get('self_awareness_growth', 0) > threshold
        
        return False
    
    def _filter_and_prioritize_insights(self, insights: List[AIInsight]) -> List[AIInsight]:
        """Filter and prioritize insights"""
        # Remove duplicates
        unique_insights = []
        seen_titles = set()
        
        for insight in insights:
            if insight.title not in seen_titles:
                unique_insights.append(insight)
                seen_titles.add(insight.title)
        
        # Sort by priority and confidence
        priority_order = {
            InsightPriority.CRITICAL: 4,
            InsightPriority.HIGH: 3,
            InsightPriority.MEDIUM: 2,
            InsightPriority.LOW: 1
        }
        
        unique_insights.sort(
            key=lambda x: (priority_order[x.priority], x.confidence),
            reverse=True
        )
        
        # Return top 10 insights
        return unique_insights[:10]
    
    def get_insights_summary(self) -> Dict[str, Any]:
        """Get summary of all insights"""
        if not self.insights_history:
            return {
                'total_insights': 0,
                'insights_by_type': {},
                'insights_by_priority': {},
                'recent_insights': []
            }
        
        # Count by type
        type_counts = Counter(insight.type.value for insight in self.insights_history)
        
        # Count by priority
        priority_counts = Counter(insight.priority.value for insight in self.insights_history)
        
        # Get recent insights (last 10)
        recent_insights = sorted(
            self.insights_history,
            key=lambda x: x.timestamp,
            reverse=True
        )[:10]
        
        return {
            'total_insights': len(self.insights_history),
            'insights_by_type': dict(type_counts),
            'insights_by_priority': dict(priority_counts),
            'recent_insights': [
                {
                    'id': insight.id,
                    'type': insight.type.value,
                    'priority': insight.priority.value,
                    'title': insight.title,
                    'confidence': insight.confidence,
                    'timestamp': insight.timestamp.isoformat()
                }
                for insight in recent_insights
            ]
        }

# Global insights engine instance
ai_insights_engine = AIInsightsEngine()
