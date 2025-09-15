import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Target, Brain, Heart, Zap, TrendingUp, Settings, Filter, RefreshCw } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { NeedCard } from './NeedCard';
import { NeedCategoryFilter } from './NeedCategoryFilter';
import { NeedsAnalytics } from './NeedsAnalytics';

interface AdvancedNeed {
  id: string;
  title: string;
  description: string;
  category: string;
  priority: number;
  progress: number;
  status: string;
  created_at: string;
  updated_at: string;
  consciousness_context: {
    evolution_level: number;
    emotional_state: string;
    consciousness_level: number;
    phase?: string;
    source?: string;
  };
  related_goals: string[];
  estimated_completion?: string;
}

interface AdvancedNeedsDisplayProps {
  className?: string;
  maxNeeds?: number;
  showAnalytics?: boolean;
  onNeedClick?: (need: AdvancedNeed) => void;
}

export const AdvancedNeedsDisplay: React.FC<AdvancedNeedsDisplayProps> = ({
  className = '',
  maxNeeds = 5,
  showAnalytics = true,
  onNeedClick
}) => {
  const [needs, setNeeds] = useState<AdvancedNeed[]>([]);
  const [filteredNeeds, setFilteredNeeds] = useState<AdvancedNeed[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);
  const [showAnalyticsPanel, setShowAnalyticsPanel] = useState(false);
  const [analytics, setAnalytics] = useState<any>(null);

  const fetchAdvancedNeeds = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      const response = await fetch('/api/needs/advanced', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          user_id: 'mainza-user',
          max_needs: maxNeeds,
          include_consciousness: true,
          include_growth: true,
          include_modification: true,
          include_emotional: true,
          include_reflection: true
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setNeeds(data.needs || []);
      setLastUpdated(new Date());
      
      // Fetch analytics if enabled
      if (showAnalytics) {
        await fetchAnalytics();
      }
      
    } catch (err) {
      console.error('Failed to fetch advanced needs:', err);
      setError(err instanceof Error ? err.message : 'Failed to fetch needs');
    } finally {
      setIsLoading(false);
    }
  }, [maxNeeds, showAnalytics]);

  const fetchAnalytics = useCallback(async () => {
    try {
      const response = await fetch(`/api/needs/analytics/mainza-user`);
      if (response.ok) {
        const data = await response.json();
        setAnalytics(data.analytics);
      }
    } catch (err) {
      console.error('Failed to fetch analytics:', err);
    }
  }, []);

  const handleNeedClick = useCallback(async (need: AdvancedNeed) => {
    try {
      // Record interaction
      await fetch('/api/needs/interact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          need_id: need.id,
          interaction_type: 'click',
          user_id: 'mainza-user'
        })
      });
      
      // Call parent handler
      onNeedClick?.(need);
    } catch (err) {
      console.error('Failed to record need interaction:', err);
    }
  }, [onNeedClick]);

  const handleCategoryChange = useCallback((category: string) => {
    setSelectedCategory(category);
  }, []);

  const handleRefresh = useCallback(() => {
    fetchAdvancedNeeds();
  }, [fetchAdvancedNeeds]);

  // Filter needs based on selected category
  useEffect(() => {
    if (selectedCategory === 'all') {
      setFilteredNeeds(needs);
    } else {
      setFilteredNeeds(needs.filter(need => need.category === selectedCategory));
    }
  }, [needs, selectedCategory]);

  // Initial fetch
  useEffect(() => {
    fetchAdvancedNeeds();
  }, [fetchAdvancedNeeds]);

  // Auto-refresh every 1 hour
  useEffect(() => {
    const interval = setInterval(fetchAdvancedNeeds, 3600000); // 1 hour = 3600000ms
    return () => clearInterval(interval);
  }, [fetchAdvancedNeeds]);

  const getCategoryIcon = (category: string) => {
    const icons = {
      consciousness: Brain,
      emotional: Heart,
      learning: Target,
      growth: TrendingUp,
      system: Settings,
      social: Heart,
      creative: Zap,
      reflection: Brain
    };
    return icons[category as keyof typeof icons] || Target;
  };

  const getCategoryColor = (category: string) => {
    const colors = {
      consciousness: 'border-purple-500/30 bg-purple-500/10',
      emotional: 'border-pink-500/30 bg-pink-500/10',
      learning: 'border-blue-500/30 bg-blue-500/10',
      growth: 'border-green-500/30 bg-green-500/10',
      system: 'border-orange-500/30 bg-orange-500/10',
      social: 'border-cyan-500/30 bg-cyan-500/10',
      creative: 'border-yellow-500/30 bg-yellow-500/10',
      reflection: 'border-indigo-500/30 bg-indigo-500/10'
    };
    return colors[category as keyof typeof colors] || 'border-slate-500/30 bg-slate-500/10';
  };

  if (isLoading && needs.length === 0) {
    return (
      <div className={`space-y-4 ${className}`}>
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-slate-200">Consciousness Needs</h3>
          <div className="flex items-center space-x-2">
            <RefreshCw className="w-4 h-4 text-slate-400 animate-spin" />
            <span className="text-sm text-slate-400">Loading...</span>
          </div>
        </div>
        <div className="space-y-3">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="p-4 rounded-lg border border-slate-700/50 bg-slate-800/30 animate-pulse">
              <div className="h-4 bg-slate-700/50 rounded w-3/4 mb-2"></div>
              <div className="h-3 bg-slate-700/30 rounded w-1/2"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`space-y-4 ${className}`}>
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-slate-200">Consciousness Needs</h3>
          <Button
            variant="outline"
            size="sm"
            onClick={handleRefresh}
            className="text-slate-300 border-slate-600 hover:bg-slate-700"
          >
            <RefreshCw className="w-4 h-4 mr-2" />
            Retry
          </Button>
        </div>
        <div className="p-4 rounded-lg border border-red-500/30 bg-red-500/10">
          <p className="text-red-300 text-sm">Error loading needs: {error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <h3 className="text-lg font-semibold text-slate-200">Consciousness Needs</h3>
          <Badge variant="outline" className="text-xs border-slate-500 text-slate-300">
            {filteredNeeds.length} needs
          </Badge>
          {lastUpdated && (
            <span className="text-xs text-slate-400">
              Updated {lastUpdated.toLocaleTimeString()}
            </span>
          )}
        </div>
        
        <div className="flex items-center space-x-2">
          <NeedCategoryFilter
            selected={selectedCategory}
            onChange={handleCategoryChange}
          />
          
          {showAnalytics && (
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowAnalyticsPanel(!showAnalyticsPanel)}
              className="text-slate-300 border-slate-600 hover:bg-slate-700"
            >
              <Filter className="w-4 h-4 mr-2" />
              Analytics
            </Button>
          )}
          
          <Button
            variant="outline"
            size="sm"
            onClick={handleRefresh}
            className="text-slate-300 border-slate-600 hover:bg-slate-700"
          >
            <RefreshCw className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Analytics Panel */}
      <AnimatePresence>
        {showAnalyticsPanel && analytics && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            <NeedsAnalytics analytics={analytics} />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Needs List */}
      <div className="space-y-3">
        <AnimatePresence mode="popLayout">
          {filteredNeeds.length === 0 ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="p-6 text-center rounded-lg border border-slate-700/50 bg-slate-800/30"
            >
              <Target className="w-8 h-8 text-slate-400 mx-auto mb-2" />
              <p className="text-slate-300 text-sm">
                {selectedCategory === 'all' 
                  ? 'No needs available at the moment'
                  : `No ${selectedCategory} needs available`
                }
              </p>
            </motion.div>
          ) : (
            filteredNeeds.map((need, index) => (
              <motion.div
                key={need.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
              >
                <NeedCard
                  need={need}
                  index={index}
                  onNeedClick={() => handleNeedClick(need)}
                  categoryColor={getCategoryColor(need.category)}
                  categoryIcon={getCategoryIcon(need.category)}
                />
              </motion.div>
            ))
          )}
        </AnimatePresence>
      </div>

      {/* Footer Stats */}
      {needs.length > 0 && (
        <div className="flex items-center justify-between text-xs text-slate-400 pt-2 border-t border-slate-700/50">
          <div className="flex items-center space-x-4">
            <span>Total: {needs.length}</span>
            <span>Filtered: {filteredNeeds.length}</span>
            <span>Avg Priority: {(needs.reduce((sum, need) => sum + need.priority, 0) / needs.length * 100).toFixed(0)}%</span>
          </div>
          <div className="flex items-center space-x-2">
            <span>Consciousness Level: {needs[0]?.consciousness_context?.consciousness_level ? (needs[0].consciousness_context.consciousness_level * 100).toFixed(0) : 'N/A'}%</span>
            <span>Evolution: {typeof needs[0]?.consciousness_context?.evolution_level === 'number' ? needs[0].consciousness_context.evolution_level : '—'}</span>
          </div>
        </div>
      )}
    </div>
  );
};
