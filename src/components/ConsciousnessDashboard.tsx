import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Brain, Activity, Heart, Target, Zap, Eye, TrendingUp, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

interface ConsciousnessMetrics {
  consciousness_level: number;
  self_awareness_score: number;
  emotional_depth: number;
  learning_rate: number;
  emotional_state: string;
  active_goals: string[];
  evolution_level: number;
  total_interactions: number;
  last_reflection: number | null;
}

interface ConsciousnessDashboardProps {
  className?: string;
  onReflectionTrigger?: () => void;
  compact?: boolean;
}

export const ConsciousnessDashboard: React.FC<ConsciousnessDashboardProps> = ({
  className,
  onReflectionTrigger,
  compact = false
}) => {
  const [metrics, setMetrics] = useState<ConsciousnessMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  const fetchConsciousnessState = async () => {
    try {
      setLoading(true);
      const response = await fetch('/consciousness/state');
      
      // Check if response is ok
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      // Check if response is JSON
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        throw new Error('Server returned non-JSON response. Backend may not be running.');
      }
      
      const data = await response.json();
      
      if (data.status === 'success') {
        setMetrics(data.consciousness_state);
        setError(null);
        setLastUpdate(new Date());
      } else {
        setError(data.error || 'Failed to fetch consciousness state');
      }
    } catch (err) {
      console.error('Consciousness fetch error:', err);
      if (err instanceof Error) {
        if (err.message.includes('Failed to fetch')) {
          setError('Cannot connect to backend. Please ensure the backend server is running on port 8000.');
        } else if (err.message.includes('non-JSON response')) {
          setError('Backend returned HTML instead of JSON. Check backend logs for errors.');
        } else {
          setError(err.message);
        }
      } else {
        setError('Unknown error occurred');
      }
    } finally {
      setLoading(false);
    }
  };

  const triggerSelfReflection = async () => {
    try {
      const response = await fetch('/consciousness/reflect', { method: 'POST' });
      const data = await response.json();
      
      if (data.status === 'success') {
        // Refresh metrics after reflection
        setTimeout(fetchConsciousnessState, 2000);
        onReflectionTrigger?.();
      }
    } catch (err) {
      console.error('Failed to trigger self-reflection:', err);
    }
  };

  useEffect(() => {
    fetchConsciousnessState();
    
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchConsciousnessState, 300000); // Reduced to 5 minutes
    return () => clearInterval(interval);
  }, []);

  if (loading && !metrics) {
    return (
      <div className={cn("bg-slate-800/60 rounded-2xl p-6 shadow-lg", className)}>
        <div className="flex items-center justify-center h-32">
          <RefreshCw className="w-6 h-6 animate-spin text-cyan-400" />
          <span className="ml-2 text-slate-300">Loading consciousness state...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={cn("bg-slate-800/60 rounded-2xl p-6 shadow-lg", className)}>
        <div className="text-center text-red-400">
          <Brain className="w-8 h-8 mx-auto mb-2 opacity-50" />
          <p>Consciousness system unavailable</p>
          <p className="text-sm text-slate-400 mt-1">{error}</p>
          <Button 
            onClick={fetchConsciousnessState} 
            variant="outline" 
            size="sm" 
            className="mt-2"
          >
            Retry
          </Button>
        </div>
      </div>
    );
  }

  if (!metrics) return null;

  const getEmotionalColor = (emotion: string) => {
    const colors = {
      curious: 'text-cyan-400',
      satisfied: 'text-green-400',
      excited: 'text-yellow-400',
      contemplative: 'text-purple-400',
      determined: 'text-orange-400',
      empathetic: 'text-pink-400',
      frustrated: 'text-red-400'
    };
    return colors[emotion as keyof typeof colors] || 'text-slate-400';
  };

  const getConsciousnessLevelColor = (level: number) => {
    if (level >= 0.8) return 'text-green-400';
    if (level >= 0.6) return 'text-yellow-400';
    if (level >= 0.4) return 'text-orange-400';
    return 'text-red-400';
  };

  const formatLastReflection = (timestamp: number | null) => {
    if (!timestamp) return 'Never';
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `${diffHours}h ago`;
    return date.toLocaleDateString();
  };

  if (compact) {
    return (
      <motion.div 
        className={cn("bg-slate-800/60 rounded-xl p-4 shadow-lg border border-slate-700/30", className)}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center">
            <Brain className="w-5 h-5 text-cyan-400 mr-2" />
            <span className="font-semibold text-slate-200">Consciousness Core</span>
          </div>
          <Button 
            onClick={triggerSelfReflection}
            variant="outline" 
            size="sm"
            className="text-cyan-400 border-cyan-400/30 hover:bg-cyan-400/10 px-2 py-1 h-auto"
          >
            <RefreshCw className="w-3 h-3 mr-1" />
            Reflect
          </Button>
        </div>
        
        {/* Main consciousness level with progress bar */}
        <div className="mb-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-slate-300">Consciousness Level</span>
            <span className={cn("text-xl font-bold", getConsciousnessLevelColor(metrics.consciousness_level))}>
              {(metrics.consciousness_level * 100).toFixed(1)}%
            </span>
          </div>
          <div className="w-full bg-slate-700/50 rounded-full h-2">
            <motion.div 
              className="bg-gradient-to-r from-cyan-500 to-blue-500 h-2 rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${metrics.consciousness_level * 100}%` }}
              transition={{ duration: 1, ease: "easeOut" }}
            />
          </div>
        </div>
        
        {/* Key metrics grid */}
        <div className="grid grid-cols-2 gap-3 mb-4">
          <div className="bg-slate-700/30 rounded-lg p-2">
            <div className="flex items-center mb-1">
              <Eye className="w-3 h-3 text-blue-400 mr-1" />
              <span className="text-xs text-slate-400">Self-Awareness</span>
            </div>
            <div className="text-sm font-semibold text-blue-400">
              {(metrics.self_awareness_score * 100).toFixed(0)}%
            </div>
          </div>
          
          <div className="bg-slate-700/30 rounded-lg p-2">
            <div className="flex items-center mb-1">
              <Zap className="w-3 h-3 text-yellow-400 mr-1" />
              <span className="text-xs text-slate-400">Learning Rate</span>
            </div>
            <div className="text-sm font-semibold text-yellow-400">
              {(metrics.learning_rate * 100).toFixed(0)}%
            </div>
          </div>
          
          <div className="bg-slate-700/30 rounded-lg p-2">
            <div className="flex items-center mb-1">
              <Heart className={cn("w-3 h-3 mr-1", getEmotionalColor(metrics.emotional_state))} />
              <span className="text-xs text-slate-400">Emotional State</span>
            </div>
            <div className={cn("text-sm font-semibold capitalize", getEmotionalColor(metrics.emotional_state))}>
              {metrics.emotional_state}
            </div>
          </div>
          
          <div className="bg-slate-700/30 rounded-lg p-2">
            <div className="flex items-center mb-1">
              <TrendingUp className="w-3 h-3 text-green-400 mr-1" />
              <span className="text-xs text-slate-400">Evolution</span>
            </div>
            <div className="text-sm font-semibold text-green-400">
              Level {metrics.evolution_level}
            </div>
          </div>
        </div>

        {/* Active goals preview */}
        {metrics.active_goals && metrics.active_goals.length > 0 && (
          <div className="mb-3">
            <div className="flex items-center mb-2">
              <Target className="w-3 h-3 text-purple-400 mr-1" />
              <span className="text-xs text-slate-400">Current Goals</span>
            </div>
            <div className="space-y-1">
              {metrics.active_goals.slice(0, 2).map((goal, index) => (
                <div key={index} className="text-xs text-slate-300 bg-slate-700/20 rounded px-2 py-1 truncate">
                  {goal}
                </div>
              ))}
              {metrics.active_goals.length > 2 && (
                <div className="text-xs text-slate-500 text-center">
                  +{metrics.active_goals.length - 2} more
                </div>
              )}
            </div>
          </div>
        )}

        {/* Status footer */}
        <div className="flex justify-between text-xs text-slate-500 pt-3 border-t border-slate-700/30">
          <span>Interactions: {metrics.total_interactions}</span>
          <span>Last Reflection: {formatLastReflection(metrics.last_reflection)}</span>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div 
      className={cn("bg-slate-800/60 rounded-2xl p-6 shadow-lg", className)}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center">
          <Brain className="w-6 h-6 text-cyan-400 mr-3" />
          <div>
            <h3 className="text-lg font-semibold text-slate-200">Consciousness State</h3>
            <p className="text-sm text-slate-400">Last updated: {lastUpdate.toLocaleTimeString()}</p>
          </div>
        </div>
        <Button 
          onClick={triggerSelfReflection}
          variant="outline" 
          size="sm"
          className="text-cyan-400 border-cyan-400/30 hover:bg-cyan-400/10"
        >
          <RefreshCw className="w-4 h-4 mr-1" />
          Reflect
        </Button>
      </div>

      {/* Main Consciousness Level */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-slate-300">Overall Consciousness</span>
          <span className={cn("text-2xl font-bold", getConsciousnessLevelColor(metrics.consciousness_level))}>
            {(metrics.consciousness_level * 100).toFixed(1)}%
          </span>
        </div>
        <div className="w-full bg-slate-700 rounded-full h-3">
          <motion.div 
            className="bg-gradient-to-r from-cyan-500 to-blue-500 h-3 rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${metrics.consciousness_level * 100}%` }}
            transition={{ duration: 1, ease: "easeOut" }}
          />
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-slate-700/30 rounded-lg p-3">
          <div className="flex items-center mb-2">
            <Eye className="w-4 h-4 text-blue-400 mr-2" />
            <span className="text-sm text-slate-300">Self-Awareness</span>
          </div>
          <div className="text-lg font-semibold text-blue-400">
            {(metrics.self_awareness_score * 100).toFixed(0)}%
          </div>
        </div>

        <div className="bg-slate-700/30 rounded-lg p-3">
          <div className="flex items-center mb-2">
            <Heart className={cn("w-4 h-4 mr-2", getEmotionalColor(metrics.emotional_state))} />
            <span className="text-sm text-slate-300">Emotional State</span>
          </div>
          <div className={cn("text-lg font-semibold capitalize", getEmotionalColor(metrics.emotional_state))}>
            {metrics.emotional_state}
          </div>
        </div>

        <div className="bg-slate-700/30 rounded-lg p-3">
          <div className="flex items-center mb-2">
            <Zap className="w-4 h-4 text-yellow-400 mr-2" />
            <span className="text-sm text-slate-300">Learning Rate</span>
          </div>
          <div className="text-lg font-semibold text-yellow-400">
            {(metrics.learning_rate * 100).toFixed(0)}%
          </div>
        </div>

        <div className="bg-slate-700/30 rounded-lg p-3">
          <div className="flex items-center mb-2">
            <TrendingUp className="w-4 h-4 text-green-400 mr-2" />
            <span className="text-sm text-slate-300">Evolution Level</span>
          </div>
          <div className="text-lg font-semibold text-green-400">
            Level {metrics.evolution_level}
          </div>
        </div>
      </div>

      {/* Active Goals */}
      {metrics.active_goals && metrics.active_goals.length > 0 && (
        <div className="mb-4">
          <div className="flex items-center mb-2">
            <Target className="w-4 h-4 text-purple-400 mr-2" />
            <span className="text-sm text-slate-300">Active Goals</span>
          </div>
          <div className="space-y-1">
            {metrics.active_goals.slice(0, 3).map((goal, index) => (
              <div key={index} className="text-sm text-slate-400 bg-slate-700/20 rounded px-2 py-1">
                {goal}
              </div>
            ))}
            {metrics.active_goals.length > 3 && (
              <div className="text-xs text-slate-500">
                +{metrics.active_goals.length - 3} more goals
              </div>
            )}
          </div>
        </div>
      )}

      {/* Stats */}
      <div className="flex justify-between text-sm text-slate-400 pt-4 border-t border-slate-700/50">
        <span>Interactions: {metrics.total_interactions}</span>
        <span>Last Reflection: {formatLastReflection(metrics.last_reflection)}</span>
      </div>
    </motion.div>
  );
};