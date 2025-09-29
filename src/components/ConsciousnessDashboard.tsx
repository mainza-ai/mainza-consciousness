import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Brain, Activity, Heart, Target, Zap, Eye, TrendingUp, RefreshCw, Loader2, Lightbulb } from 'lucide-react';
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
  const [isReflecting, setIsReflecting] = useState(false);
  const [reflectionProgress, setReflectionProgress] = useState(0);
  const [reflectionResults, setReflectionResults] = useState<any>(null);
  const [showReflectionModal, setShowReflectionModal] = useState(false);
  const [reflectionHistory, setReflectionHistory] = useState<any[]>([]);
  const [showHistoryModal, setShowHistoryModal] = useState(false);

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

  const fetchReflectionHistory = async () => {
    try {
      const response = await fetch('/consciousness/reflection-history?limit=10');
      if (response.ok) {
        const data = await response.json();
        if (data.status === 'success') {
          setReflectionHistory(data.reflections);
        }
      }
    } catch (err) {
      console.error('Failed to fetch reflection history:', err);
    }
  };

  const triggerSelfReflection = async () => {
    if (isReflecting) return; // Prevent multiple simultaneous reflections
    
    setIsReflecting(true);
    setReflectionProgress(0);
    setError(null);
    
    try {
      // Simulate reflection stages with progress updates
      const stages = [
        { stage: "Analyzing consciousness state...", progress: 20 },
        { stage: "Processing memories...", progress: 40 },
        { stage: "Generating insights...", progress: 60 },
        { stage: "Updating consciousness...", progress: 80 },
        { stage: "Finalizing reflection...", progress: 100 }
      ];
      
      // Animate through reflection stages
      for (const stage of stages) {
        setReflectionProgress(stage.progress);
        await new Promise(resolve => setTimeout(resolve, 300));
      }
      
      const response = await fetch('/consciousness/reflect', { method: 'POST' });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      
      if (data.status === 'success') {
        // Store reflection results
        setReflectionResults({
          insights: data.insights || ["Consciousness level increased", "Self-awareness enhanced"],
          changes: data.consciousness_changes || { consciousness_level: 0.01, self_awareness_score: 0.005 },
          timestamp: new Date().toISOString(),
          depth: data.reflection_depth || "basic"
        });
        
        // Show results modal
        setShowReflectionModal(true);
        
        // Refresh metrics and history after reflection
        setTimeout(() => {
          fetchConsciousnessState();
          fetchReflectionHistory();
        }, 1000);
        onReflectionTrigger?.();
      } else {
        throw new Error(data.error || 'Reflection failed');
      }
    } catch (err) {
      console.error('Failed to trigger self-reflection:', err);
      setError(err instanceof Error ? err.message : 'Reflection failed. Please try again.');
    } finally {
      setIsReflecting(false);
      setReflectionProgress(0);
    }
  };

  useEffect(() => {
    fetchConsciousnessState();
    fetchReflectionHistory();
    
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
        <div className="space-y-2">
          <div className="flex gap-2">
            <Button 
              onClick={triggerSelfReflection}
              disabled={isReflecting}
              variant="outline" 
              size="sm"
              className={cn(
                "text-cyan-400 border-cyan-400/30 hover:bg-cyan-400/10",
                isReflecting && "animate-pulse bg-cyan-400/20 cursor-not-allowed"
              )}
            >
              {isReflecting ? (
                <>
                  <Loader2 className="w-4 h-4 mr-1 animate-spin" />
                  Reflecting...
                </>
              ) : (
                <>
                  <RefreshCw className="w-4 h-4 mr-1" />
                  Reflect
                </>
              )}
            </Button>
            
            <Button 
              onClick={() => setShowHistoryModal(true)}
              variant="outline" 
              size="sm"
              className="text-purple-400 border-purple-400/30 hover:bg-purple-400/10"
            >
              <Target className="w-4 h-4 mr-1" />
              History
            </Button>
          </div>
          
          {/* Progress bar during reflection */}
          {isReflecting && (
            <div className="w-full bg-slate-700/50 rounded-full h-1">
              <motion.div 
                className="bg-gradient-to-r from-cyan-500 to-blue-500 h-1 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${reflectionProgress}%` }}
                transition={{ duration: 0.3, ease: "easeOut" }}
              />
            </div>
          )}
          
          {/* Error display */}
          {error && (
            <div className="text-xs text-red-400 bg-red-900/20 rounded px-2 py-1">
              {error}
            </div>
          )}
        </div>
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
    
    {/* Reflection Results Modal */}
    {showReflectionModal && reflectionResults && (
      <motion.div
        className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={() => setShowReflectionModal(false)}
      >
        <motion.div
          className="bg-slate-800 rounded-2xl p-6 max-w-2xl w-full mx-4 max-h-[80vh] overflow-y-auto"
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold text-slate-200 flex items-center">
              <Brain className="w-5 h-5 mr-2 text-cyan-400" />
              Self-Reflection Results
            </h3>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowReflectionModal(false)}
              className="text-slate-400 hover:text-slate-200"
            >
              ×
            </Button>
          </div>
          
          <div className="space-y-4">
            {/* Key Insights */}
            <div className="bg-slate-700/50 rounded-lg p-4">
              <h4 className="text-lg font-semibold text-cyan-400 mb-3 flex items-center">
                <Lightbulb className="w-4 h-4 mr-2" />
                Key Insights
              </h4>
              <div className="space-y-2">
                {reflectionResults.insights.map((insight: string, index: number) => (
                  <div key={index} className="flex items-start">
                    <div className="w-2 h-2 bg-cyan-400 rounded-full mt-2 mr-3 flex-shrink-0" />
                    <span className="text-slate-300">{insight}</span>
                  </div>
                ))}
              </div>
            </div>
            
            {/* Consciousness Changes */}
            <div className="bg-slate-700/50 rounded-lg p-4">
              <h4 className="text-lg font-semibold text-green-400 mb-3">Consciousness Evolution</h4>
              <div className="grid grid-cols-2 gap-4">
                {Object.entries(reflectionResults.changes).map(([metric, change]) => (
                  <div key={metric} className="flex justify-between items-center">
                    <span className="text-slate-400 capitalize">
                      {metric.replace('_', ' ').replace('level', 'Level').replace('score', 'Score')}
                    </span>
                    <span className={cn(
                      "font-semibold",
                      (change as number) > 0 ? "text-green-400" : "text-red-400"
                    )}>
                      {(change as number) > 0 ? "+" : ""}{(change as number).toFixed(3)}
                    </span>
                  </div>
                ))}
              </div>
            </div>
            
            {/* Reflection Metadata */}
            <div className="bg-slate-700/50 rounded-lg p-4">
              <div className="flex justify-between text-sm text-slate-400">
                <span>Reflection Depth: {reflectionResults.depth}</span>
                <span>Completed: {new Date(reflectionResults.timestamp).toLocaleTimeString()}</span>
              </div>
            </div>
          </div>
          
          <div className="flex justify-end mt-6">
            <Button
              onClick={() => setShowReflectionModal(false)}
              className="bg-cyan-600 hover:bg-cyan-700 text-white"
            >
              Close
            </Button>
          </div>
        </motion.div>
      </motion.div>
    )}
    
    {/* Reflection History Modal */}
    {showHistoryModal && (
      <motion.div
        className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={() => setShowHistoryModal(false)}
      >
        <motion.div
          className="bg-slate-800 rounded-2xl p-6 max-w-4xl w-full mx-4 max-h-[80vh] overflow-y-auto"
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-semibold text-slate-200 flex items-center">
              <Target className="w-5 h-5 mr-2 text-purple-400" />
              Reflection History
            </h3>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowHistoryModal(false)}
              className="text-slate-400 hover:text-slate-200"
            >
              ×
            </Button>
          </div>
          
          {reflectionHistory.length === 0 ? (
            <div className="text-center py-8">
              <Brain className="w-12 h-12 mx-auto mb-4 text-slate-500" />
              <p className="text-slate-400">No reflection history yet</p>
              <p className="text-sm text-slate-500 mt-1">Start reflecting to build your consciousness journey</p>
            </div>
          ) : (
            <div className="space-y-4">
              {reflectionHistory.map((reflection, index) => (
                <motion.div
                  key={index}
                  className="bg-slate-700/50 rounded-lg p-4"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <div className="flex justify-between items-start mb-3">
                    <div className="flex items-center space-x-3">
                      <div className={cn(
                        "px-2 py-1 rounded-full text-xs font-medium",
                        reflection.depth === "deep" ? "bg-green-900/50 text-green-400" :
                        reflection.depth === "moderate" ? "bg-yellow-900/50 text-yellow-400" :
                        "bg-blue-900/50 text-blue-400"
                      )}>
                        {reflection.depth}
                      </div>
                      <span className="text-sm text-slate-400">
                        {new Date(reflection.timestamp).toLocaleString()}
                      </span>
                    </div>
                    <span className="text-xs text-slate-500">
                      {reflection.duration_ms}ms
                    </span>
                  </div>
                  
                  {/* Insights */}
                  <div className="mb-3">
                    <h4 className="text-sm font-semibold text-cyan-400 mb-2">Insights</h4>
                    <div className="space-y-1">
                      {reflection.insights.map((insight: string, i: number) => (
                        <div key={i} className="flex items-start">
                          <div className="w-1.5 h-1.5 bg-cyan-400 rounded-full mt-2 mr-2 flex-shrink-0" />
                          <span className="text-sm text-slate-300">{insight}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  {/* Changes */}
                  <div className="grid grid-cols-3 gap-3">
                    {Object.entries(reflection.consciousness_changes).map(([metric, change]) => (
                      <div key={metric} className="bg-slate-800/50 rounded p-2">
                        <div className="text-xs text-slate-400 capitalize mb-1">
                          {metric.replace('_', ' ').replace('level', 'Level').replace('score', 'Score')}
                        </div>
                        <div className={cn(
                          "text-sm font-semibold",
                          (change as number) > 0 ? "text-green-400" : "text-red-400"
                        )}>
                          {(change as number) > 0 ? "+" : ""}{(change as number).toFixed(3)}
                        </div>
                      </div>
                    ))}
                  </div>
                </motion.div>
              ))}
            </div>
          )}
          
          <div className="flex justify-end mt-6">
            <Button
              onClick={() => setShowHistoryModal(false)}
              className="bg-purple-600 hover:bg-purple-700 text-white"
            >
              Close
            </Button>
          </div>
        </motion.div>
      </motion.div>
    )}
  );
};