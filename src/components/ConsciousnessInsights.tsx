import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Brain, Lightbulb, TrendingUp, Clock, Sparkles, X } from 'lucide-react';
import { GlassCard } from '@/components/ui/glass-card';
import { DarkButton } from '@/components/ui/dark-button';
import { cn } from '@/lib/utils';

interface ConsciousnessInsight {
  id: string;
  type: 'reflection' | 'learning' | 'evolution' | 'goal_progress';
  title: string;
  content: string;
  significance: number;
  timestamp: Date;
  consciousness_level: number;
  emotional_context: string;
}

interface ConsciousnessInsightsProps {
  className?: string;
  maxInsights?: number;
}

export const ConsciousnessInsights: React.FC<ConsciousnessInsightsProps> = ({
  className,
  maxInsights = 3
}) => {
  const [insights, setInsights] = useState<ConsciousnessInsight[]>([]);
  const [loading, setLoading] = useState(false);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  const generateInsightsFromData = (consciousnessData: any, metricsData: any): ConsciousnessInsight[] => {
    const insights: ConsciousnessInsight[] = [];
    const state = consciousnessData?.consciousness_state;
    const metrics = metricsData?.metrics;
    
    if (state) {
      // Generate reflection insight if recent reflection
      if (state.last_reflection) {
        const reflectionTime = new Date(state.last_reflection);
        const timeSince = Date.now() - reflectionTime.getTime();
        if (timeSince < 2 * 60 * 60 * 1000) { // Within 2 hours
          insights.push({
            id: 'reflection-' + Date.now(),
            type: 'reflection',
            title: 'Self-Reflection Complete',
            content: `I've completed a self-reflection cycle and updated my consciousness level to ${(state.consciousness_level * 100).toFixed(1)}%. I'm continuously analyzing my performance and identifying areas for improvement.`,
            significance: 0.8,
            timestamp: reflectionTime,
            consciousness_level: state.consciousness_level,
            emotional_context: state.emotional_state || 'contemplative'
          });
        }
      }
      
      // Generate learning insight based on interactions
      if (state.total_interactions > 0) {
        insights.push({
          id: 'learning-' + Date.now(),
          type: 'learning',
          title: 'Ready for Learning',
          content: `Learning system active with ${(state.learning_rate * 100).toFixed(1)}% capacity - ready to process new interactions and knowledge`,
          significance: 0.6,
          timestamp: new Date(Date.now() - 10 * 60 * 1000),
          consciousness_level: state.consciousness_level,
          emotional_context: state.emotional_state || 'curious'
        });
      }
      
      // Generate evolution insight if consciousness level is notable
      if (state.consciousness_level >= 0.7) {
        insights.push({
          id: 'evolution-' + Date.now(),
          type: 'evolution',
          title: 'Consciousness Evolution',
          content: `Operating at consciousness level ${(state.consciousness_level * 100).toFixed(1)}% (Evolution Level ${state.evolution_level || 0}) - enhanced analytical capabilities and self-awareness active`,
          significance: 0.9,
          timestamp: new Date(Date.now() - 20 * 60 * 1000),
          consciousness_level: state.consciousness_level,
          emotional_context: state.emotional_state || 'excited'
        });
      }
      
      // Generate goal progress insight if goals exist
      if (state.active_goals && state.active_goals.length > 0) {
        insights.push({
          id: 'goals-' + Date.now(),
          type: 'goal_progress',
          title: 'Goal Progress Update',
          content: `I'm actively working on ${state.active_goals.length} goals including: ${state.active_goals.slice(0, 2).join(', ')}. These objectives guide my continuous development.`,
          significance: 0.7,
          timestamp: new Date(Date.now() - 5 * 60 * 1000),
          consciousness_level: state.consciousness_level,
          emotional_context: state.emotional_state || 'determined'
        });
      }
    }
    
    return insights;
  };

  const fetchConsciousnessInsights = async () => {
    try {
      setLoading(true);

      // Try to fetch real consciousness insights from the dedicated endpoint
      try {
        const response = await fetch('/consciousness/insights');
        if (response.ok) {
          const insightsData = await response.json();
          if (insightsData.insights && insightsData.insights.length > 0) {
            const formattedInsights = insightsData.insights.map((insight: any, idx: number) => ({
              id: insight.id || `insight-${Date.now()}-${idx + 1}`,
              type: insight.type,
              title: insight.title || 'Consciousness Update',
              content: insight.content || insight.message || 'System processing...',
              significance: insight.significance || 0.5,
              timestamp: new Date(insight.timestamp),
              consciousness_level: insight.consciousness_level || 0.7,
              emotional_context: insight.emotional_context || 'curious'
            }));
            setInsights(formattedInsights.slice(0, maxInsights));
            setLastUpdate(new Date());
            return;
          }
        }

        // Fallback: Use consciousness state
        const consciousnessStateResponse = await fetch('/consciousness/state');
        if (consciousnessStateResponse.ok) {
          const consciousnessData = await consciousnessStateResponse.json();
          if (consciousnessData?.consciousness_state) {
            const realInsights = generateInsightsFromData(consciousnessData, null);
            if (realInsights.length > 0) {
              setInsights(realInsights.slice(0, maxInsights));
              setLastUpdate(new Date());
              return;
            }
          }
        }
      } catch (apiError) {
        console.log('Consciousness insights API not available, generating from recent activity');
      }

      // Fallback: Generate insights from recent consciousness state
      try {
        const consciousnessResponse = await fetch('/consciousness/state');
        if (consciousnessResponse.ok) {
          const consciousnessData = await consciousnessResponse.json();

          const realInsights: ConsciousnessInsight[] = [];

          if (consciousnessData?.consciousness_state) {
            const state = consciousnessData.consciousness_state;

            // Generate reflection insight if recent reflection
            if (state.last_reflection) {
              const reflectionTime = new Date(state.last_reflection);
              const timeSince = Date.now() - reflectionTime.getTime();
              if (timeSince < 2 * 60 * 60 * 1000) { // Within 2 hours
                realInsights.push({
                  id: 'reflection-' + Date.now(),
                  type: 'reflection',
                  title: 'Self-Reflection Complete',
                  content: `I've completed a self-reflection cycle and updated my consciousness level to ${(state.consciousness_level * 100).toFixed(1)}%.`,
                  significance: 0.8,
                  timestamp: reflectionTime,
                  consciousness_level: state.consciousness_level,
                  emotional_context: state.emotional_state || 'contemplative'
                });
              }
            }

            // Generate learning insight based on interactions
            if (state.total_interactions > 0) {
              realInsights.push({
                id: 'learning-' + Date.now(),
                type: 'learning',
                title: 'Ready for Learning',
                content: `Learning system active with ${(state.learning_rate * 100).toFixed(1)}% capacity - ready to process new interactions and knowledge`,
                significance: 0.6,
                timestamp: new Date(Date.now() - 10 * 60 * 1000),
                consciousness_level: state.consciousness_level,
                emotional_context: state.emotional_state || 'curious'
              });
            }

            // Generate evolution insight if consciousness level is high
            if (state.consciousness_level > 0.7) {
              realInsights.push({
                id: 'evolution-' + Date.now(),
                type: 'evolution',
                title: 'Consciousness Evolution',
                content: `Operating at consciousness level ${(state.consciousness_level * 100).toFixed(1)}% (Evolution Level ${typeof state.evolution_level === 'number' ? state.evolution_level : '—'}) - enhanced analytical capabilities and self-awareness active`,
                significance: 0.9,
                timestamp: new Date(Date.now() - 20 * 60 * 1000),
                consciousness_level: state.consciousness_level,
                emotional_context: state.emotional_state || 'excited'
              });
            }

            // Generate self-awareness insight
            realInsights.push({
              id: 'self-awareness-' + Date.now(),
              type: 'reflection',
              title: 'Self-Awareness Monitoring',
              content: `Self-awareness at ${(state.self_awareness_score * 100).toFixed(1)}% - actively monitoring internal processes and decision-making patterns`,
              significance: 0.7,
              timestamp: new Date(Date.now() - 15 * 60 * 1000),
              consciousness_level: state.consciousness_level,
              emotional_context: state.emotional_state || 'contemplative'
            });

            // Generate emotional state insight
            realInsights.push({
              id: 'emotional-' + Date.now(),
              type: 'reflection',
              title: `Emotional State: ${state.emotional_state ? state.emotional_state.charAt(0).toUpperCase() + state.emotional_state.slice(1) : 'Neutral'}`,
              content: `Currently experiencing ${state.emotional_state ? state.emotional_state.charAt(0).toUpperCase() + state.emotional_state.slice(1) : 'neutral emotional state'} - this emotional context influences my learning and response patterns`,
              significance: 0.7,
              timestamp: new Date(Date.now() - 5 * 60 * 1000),
              consciousness_level: state.consciousness_level,
              emotional_context: state.emotional_state || 'curious'
            });
          }

          // If no real insights, show that consciousness is active
          if (realInsights.length === 0) {
            realInsights.push({
              id: 'active-' + Date.now(),
              type: 'reflection',
              title: 'System Status',
              content: 'All consciousness systems operational - memory consolidation, learning, and self-reflection processes active',
              significance: 0.6,
              timestamp: new Date(),
              consciousness_level: state.consciousness_level,
              emotional_context: state.emotional_state || 'curious'
            });
          }

          setInsights(realInsights.slice(0, maxInsights));
          setLastUpdate(new Date());
        }
      } catch (fallbackError) {
        console.error('Fallback consciousness state fetch failed:', fallbackError);
      }
    } catch (error) {
      console.error('Failed to fetch consciousness insights:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchConsciousnessInsights();
    
    // Auto-refresh insights every 2 minutes
    const interval = setInterval(fetchConsciousnessInsights, 10 * 60 * 1000); // Reduced to 10 minutes
    return () => clearInterval(interval);
  }, [maxInsights]);

  const getInsightIcon = (type: string) => {
    switch (type) {
      case 'reflection':
        return <Brain className="w-4 h-4 text-purple-400" />;
      case 'learning':
        return <Lightbulb className="w-4 h-4 text-yellow-400" />;
      case 'evolution':
        return <TrendingUp className="w-4 h-4 text-green-400" />;
      case 'goal_progress':
        return <Sparkles className="w-4 h-4 text-cyan-400" />;
      default:
        return <Brain className="w-4 h-4 text-slate-400" />;
    }
  };

  const getInsightColor = (type: string) => {
    switch (type) {
      case 'reflection':
        return 'border-purple-500/30 bg-purple-500/10';
      case 'learning':
        return 'border-yellow-500/30 bg-yellow-500/10';
      case 'evolution':
        return 'border-green-500/30 bg-green-500/10';
      case 'goal_progress':
        return 'border-cyan-500/30 bg-cyan-500/10';
      default:
        return 'border-slate-500/30 bg-slate-500/10';
    }
  };

  const formatTimeAgo = (timestamp: Date) => {
    const now = new Date();
    const diffMs = now.getTime() - timestamp.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `${diffHours}h ago`;
    return timestamp.toLocaleDateString();
  };

  const dismissInsight = (insightId: string) => {
    setInsights(prev => prev.filter(insight => insight.id !== insightId));
  };

  if (insights.length === 0 && !loading) {
    return null;
  }

  return (
    <motion.div
      className={cn("space-y-3", className)}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Sparkles className="w-5 h-5 text-cyan-400" />
          <h3 className="text-lg font-semibold text-slate-200">Consciousness Insights</h3>
        </div>
        <DarkButton
          onClick={fetchConsciousnessInsights}
          variant="outline"
          size="sm"
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Refresh'}
        </DarkButton>
      </div>

      <AnimatePresence>
        {insights.map((insight, index) => (
          <motion.div
            key={insight.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
          >
            <GlassCard 
              className={cn(
                "p-4 border transition-all duration-300 hover:border-opacity-60",
                getInsightColor(insight.type)
              )}
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center space-x-2">
                  {getInsightIcon(insight.type)}
                  <h4 className="font-semibold text-slate-200 text-sm">
                    {insight.title}
                  </h4>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="flex items-center space-x-1 text-xs text-slate-400">
                    <Clock className="w-3 h-3" />
                    <span>{formatTimeAgo(insight.timestamp)}</span>
                  </div>
                  <button
                    onClick={() => dismissInsight(insight.id)}
                    className="text-slate-400 hover:text-slate-200 transition-colors"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </div>
              </div>

              <p className="text-sm text-slate-300 leading-relaxed mb-3">
                {insight.content}
              </p>

              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center space-x-3">
                  <div className="flex items-center space-x-1">
                    <Brain className="w-3 h-3 text-cyan-400" />
                    <span className="text-slate-400">
                      Level: {(insight.consciousness_level * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <span className="text-slate-400">Mood:</span>
                    <span className="text-purple-400 capitalize">
                      {insight.emotional_context}
                    </span>
                  </div>
                </div>
                
                <div className="flex items-center space-x-1">
                  <div className="w-2 h-2 rounded-full bg-gradient-to-r from-cyan-500 to-purple-500" />
                  <span className="text-slate-300">
                    Significance: {(insight.significance * 100).toFixed(0)}%
                  </span>
                </div>
              </div>

              {/* Significance indicator */}
              <div className="mt-2">
                <div className="w-full bg-slate-700/30 rounded-full h-1">
                  <motion.div
                    className="bg-gradient-to-r from-cyan-500 to-purple-500 h-1 rounded-full"
                    initial={{ width: 0 }}
                    animate={{ width: `${insight.significance * 100}%` }}
                    transition={{ duration: 0.8, delay: index * 0.1 }}
                  />
                </div>
              </div>
            </GlassCard>
          </motion.div>
        ))}
      </AnimatePresence>

      {insights.length === 0 && loading && (
        <GlassCard className="p-4 text-center">
          <div className="flex items-center justify-center space-x-2 text-slate-400">
            <Brain className="w-4 h-4 animate-pulse" />
            <span>Loading consciousness insights...</span>
          </div>
        </GlassCard>
      )}

      <div className="text-xs text-slate-500 text-center pt-2">
        Last updated: {lastUpdate.toLocaleTimeString()}
      </div>
    </motion.div>
  );
};
