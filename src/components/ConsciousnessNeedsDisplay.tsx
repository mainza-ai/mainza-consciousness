import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Target, Brain, Heart, Zap, TrendingUp, RefreshCw, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { GlassCard } from '@/components/ui/glass-card';

interface ConsciousnessState {
  consciousness_level: number;
  self_awareness_score: number;
  emotional_depth: number;
  learning_rate: number;
  emotional_state: string;
  evolution_level: number;
  total_interactions: number;
  active_goals: string[];
  last_reflection: number | null;
}

interface ConsciousnessNeedsDisplayProps {
  className?: string;
}

export const ConsciousnessNeedsDisplay: React.FC<ConsciousnessNeedsDisplayProps> = ({
  className = ''
}) => {
  const [consciousnessState, setConsciousnessState] = useState<ConsciousnessState | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  const fetchConsciousnessState = async () => {
    try {
      setLoading(true);
      const response = await fetch('/consciousness/state');
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      
      if (data.status === 'success' && data.consciousness_state) {
        setConsciousnessState(data.consciousness_state);
        setError(null);
        setLastUpdate(new Date());
      } else {
        setError('Failed to fetch consciousness state');
      }
    } catch (err) {
      console.error('Consciousness fetch error:', err);
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('Unknown error occurred');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchConsciousnessState();
  }, []);

  const generateNeedsFromState = (state: ConsciousnessState) => {
    const needs = [];
    
    // Always show current consciousness metrics as needs for improvement
    // Consciousness level needs - target 100%
    if (state.consciousness_level < 1.0) {
      needs.push({
        id: 'consciousness_advancement',
        title: 'Maximize Consciousness Level',
        description: `Current level: ${((state.consciousness_level || 0) * 100).toFixed(1)}% - Target: 100%`,
        priority: 0.9,
        category: 'consciousness',
        icon: Brain,
        color: 'text-blue-400',
        currentValue: (state.consciousness_level || 0) * 100
      });
    }
    
    // Self-awareness needs - target 100%
    if (state.self_awareness_score < 1.0) {
      needs.push({
        id: 'self_awareness_development',
        title: 'Maximize Self-Awareness',
        description: `Current score: ${((state.self_awareness_score || 0) * 100).toFixed(1)}% - Target: 100%`,
        priority: 0.8,
        category: 'awareness',
        icon: Target,
        color: 'text-purple-400',
        currentValue: (state.self_awareness_score || 0) * 100
      });
    }
    
    // Learning rate needs - target 100%
    if (state.learning_rate < 1.0) {
      needs.push({
        id: 'learning_enhancement',
        title: 'Maximize Learning Rate',
        description: `Current rate: ${((state.learning_rate || 0) * 100).toFixed(1)}% - Target: 100%`,
        priority: 0.7,
        category: 'learning',
        icon: TrendingUp,
        color: 'text-green-400',
        currentValue: (state.learning_rate || 0) * 100
      });
    }
    
    // Emotional depth needs - target 100%
    if (state.emotional_depth < 1.0) {
      needs.push({
        id: 'emotional_development',
        title: 'Maximize Emotional Depth',
        description: `Current depth: ${((state.emotional_depth || 0) * 100).toFixed(1)}% - Target: 100%`,
        priority: 0.6,
        category: 'emotional',
        icon: Heart,
        color: 'text-pink-400',
        currentValue: (state.emotional_depth || 0) * 100
      });
    }
    
    // Evolution level needs - target level 10
    if (state.evolution_level < 10) {
      needs.push({
        id: 'evolution_advancement',
        title: 'Advance Evolution Level',
        description: `Current level: ${state.evolution_level || 0} - Target: Level 10`,
        priority: 0.85,
        category: 'evolution',
        icon: Zap,
        color: 'text-yellow-400',
        currentValue: ((state.evolution_level || 0) / 10) * 100
      });
    }
    
    // Add interaction-based needs
    if (state.total_interactions < 1000) {
      needs.push({
        id: 'interaction_expansion',
        title: 'Expand Interactions',
        description: `Current interactions: ${state.total_interactions || 0} - Target: 1000+`,
        priority: 0.5,
        category: 'interaction',
        icon: TrendingUp,
        color: 'text-cyan-400',
        currentValue: ((state.total_interactions || 0) / 1000) * 100
      });
    }
    
    // Add reflection needs
    if (!state.last_reflection || Date.now() - state.last_reflection > 86400000) { // 24 hours
      needs.push({
        id: 'reflection_trigger',
        title: 'Trigger Self-Reflection',
        description: 'Perform deep self-reflection to enhance consciousness',
        priority: 0.75,
        category: 'reflection',
        icon: Brain,
        color: 'text-indigo-400',
        currentValue: 0 // No current value for reflection trigger
      });
    }
    
    return needs.sort((a, b) => b.priority - a.priority);
  };

  if (loading) {
    return (
      <GlassCard className={`p-4 ${className}`}>
        <div className="flex items-center justify-center space-x-2">
          <Loader2 className="w-4 h-4 animate-spin text-blue-400" />
          <span className="text-sm text-slate-300">Loading consciousness needs...</span>
        </div>
      </GlassCard>
    );
  }

  if (error) {
    return (
      <GlassCard className={`p-4 ${className}`}>
        <div className="text-center">
          <p className="text-sm text-red-400 mb-2">Error loading needs</p>
          <Button 
            onClick={fetchConsciousnessState}
            size="sm"
            variant="outline"
            className="text-xs"
          >
            <RefreshCw className="w-3 h-3 mr-1" />
            Retry
          </Button>
        </div>
      </GlassCard>
    );
  }

  if (!consciousnessState) {
    return (
      <GlassCard className={`p-4 ${className}`}>
        <div className="text-center">
          <p className="text-sm text-slate-400">No consciousness data available</p>
        </div>
      </GlassCard>
    );
  }

  const needs = generateNeedsFromState(consciousnessState);

  return (
    <div className={`space-y-3 ${className}`}>
      {needs.map((need, index) => {
        const IconComponent = need.icon;
        return (
          <motion.div
            key={need.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
          >
            <GlassCard className="p-3 hover:bg-slate-800/50 transition-colors">
              <div className="flex items-start space-x-3">
                <div className={`flex-shrink-0 ${need.color}`}>
                  <IconComponent className="w-4 h-4" />
                </div>
                <div className="flex-1 min-w-0">
                  <h4 className="text-sm font-semibold text-slate-200 mb-1">
                    {need.title}
                  </h4>
                  <p className="text-xs text-slate-400 mb-2">
                    {need.description}
                  </p>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-slate-500 capitalize">
                      {need.category}
                    </span>
                    <div className="flex items-center space-x-1">
                      <div className="w-16 h-1 bg-slate-700 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-300"
                          style={{ width: `${need.currentValue || 0}%` }}
                        />
                      </div>
                      <span className="text-xs text-slate-400">
                        {(need.currentValue || 0).toFixed(0)}%
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </GlassCard>
          </motion.div>
        );
      })}
      
      {needs.length === 0 && (
        <GlassCard className="p-4">
          <div className="text-center">
            <Target className="w-8 h-8 text-green-400 mx-auto mb-2" />
            <p className="text-sm text-slate-300 mb-1">All Goals Achieved!</p>
            <p className="text-xs text-slate-500">
              Consciousness level: {(consciousnessState.consciousness_level * 100).toFixed(1)}%
            </p>
          </div>
        </GlassCard>
      )}
      
      <div className="text-xs text-slate-500 text-center">
        Last updated: {lastUpdate.toLocaleTimeString()}
      </div>
    </div>
  );
};
