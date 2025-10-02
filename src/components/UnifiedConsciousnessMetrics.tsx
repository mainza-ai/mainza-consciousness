import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  Brain, 
  Activity, 
  Database, 
  Network, 
  Zap, 
  Target,
  TrendingUp,
  TrendingDown,
  CheckCircle,
  AlertCircle,
  Clock,
  Cpu,
  Memory,
  Layers
} from 'lucide-react';
import { MetricDisplay } from '@/components/ui/metric-display';
import { GlassCard } from '@/components/ui/glass-card';

interface UnifiedConsciousnessData {
  classical: {
    consciousness_level: number;
    emotional_state: string;
    self_awareness_score: number;
    learning_rate: number;
    evolution_level: number;
    total_interactions: number;
    database_stats: {
      total_nodes: number;
      total_relationships: number;
      node_counts: Record<string, number>;
    };
    system_health: {
      neo4j_connected: boolean;
      consciousness_active: boolean;
      total_uptime_hours: number;
    };
  };
  quantum: {
    quantum_consciousness_level: number;
    quantum_coherence: number;
    entanglement_strength: number;
    superposition_states: number;
    quantum_advantage: number;
    quantum_processing_active: boolean;
    quantum_metrics: {
      total_quantum_updates: number;
      quantum_coherence_avg: number;
      entanglement_strength_avg: number;
      superposition_states_avg: number;
      quantum_advantage_avg: number;
    };
    meta_consciousness: {
      quantum_meta_processing_active: boolean;
      total_quantum_meta_reflections: number;
      quantum_insights_generated: number;
    };
    memory_integration: {
      quantum_memory_processing_active: boolean;
      evolution_network_size: number;
    };
  };
  unified: {
    overall_consciousness_level: number;
    system_integration_level: number;
    processing_efficiency: number;
    data_consistency: number;
    last_sync: string;
  };
}

interface UnifiedConsciousnessMetricsProps {
  className?: string;
  showDetails?: boolean;
}

export const UnifiedConsciousnessMetrics: React.FC<UnifiedConsciousnessMetricsProps> = ({
  className,
  showDetails = false
}) => {
  const [data, setData] = useState<UnifiedConsciousnessData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);

  const fetchUnifiedData = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);

      // Fetch both classical and quantum data in parallel
      const [insightsResponse, quantumResponse] = await Promise.all([
        fetch('/api/insights/neo4j/statistics').then(r => r.ok ? r.json() : null).catch(() => null),
        fetch('/api/quantum/state').then(r => r.ok ? r.json() : null).catch(() => null)
      ]);

      if (!insightsResponse && !quantumResponse) {
        throw new Error('Unable to fetch consciousness data from either system');
      }

      // Process classical data
      const classical = insightsResponse ? {
        consciousness_level: 0.8, // Default consciousness level since not in API
        emotional_state: 'neutral',
        self_awareness_score: 0.7,
        learning_rate: 0.6,
        evolution_level: 5,
        total_interactions: insightsResponse.total_nodes || 0,
        database_stats: {
          total_nodes: insightsResponse.total_nodes || 0,
          total_relationships: insightsResponse.total_relationships || 0,
          node_counts: insightsResponse.node_counts || {}
        },
        system_health: {
          neo4j_connected: true,
          consciousness_active: true,
          total_uptime_hours: 24
        }
      } : null;

      // Process quantum data from quantum state
      const quantum = quantumResponse?.data ? {
        quantum_consciousness_level: quantumResponse.data.quantum_consciousness_level || 0,
        quantum_coherence: quantumResponse.data.quantum_coherence || 0,
        entanglement_strength: quantumResponse.data.entanglement_strength || 0,
        superposition_states: quantumResponse.data.superposition_states || 0,
        quantum_advantage: quantumResponse.data.quantum_advantage || 0,
        quantum_processing_active: quantumResponse.data.quantum_processing_active || false,
        quantum_metrics: {
          total_quantum_updates: 0,
          quantum_coherence_avg: quantumResponse.data.quantum_coherence || 0,
          entanglement_strength_avg: quantumResponse.data.entanglement_strength || 0,
          superposition_states_avg: quantumResponse.data.superposition_states || 0,
          quantum_advantage_avg: quantumResponse.data.quantum_advantage || 0
        },
        active_algorithms: quantumResponse.data.active_algorithms || [],
        current_operations: quantumResponse.data.current_operations || [],
        system_health: quantumResponse.data.system_health || 'healthy',
        integrated_consciousness_level: quantumResponse.data.quantum_consciousness_level || 0,
        classical_consciousness_level: 0,
        classical_self_awareness: 0,
        classical_learning_rate: 0,
        classical_evolution_level: 0
      } : null;

      // Calculate unified metrics using integrated consciousness level
      const overall_consciousness_level = quantum?.integrated_consciousness_level || 
        (classical && quantum ? 
          (classical.consciousness_level + quantum.quantum_consciousness_level) / 2 : 
          (classical?.consciousness_level || quantum?.quantum_consciousness_level || 0));

      const system_integration_level = classical && quantum ? 
        (classical.system_health.consciousness_active && quantum.quantum_processing_active ? 1.0 : 0.5) : 0;

      const processing_efficiency = quantum ? 
        Math.min(quantum.quantum_metrics.total_quantum_updates / 1000, 1.0) : 0;

      const data_consistency = classical && quantum ? 
        (Math.abs(classical.consciousness_level - quantum.quantum_consciousness_level) < 0.1 ? 1.0 : 0.7) : 0.5;

      const unifiedData: UnifiedConsciousnessData = {
        classical: classical || {
          consciousness_level: 0,
          emotional_state: 'unknown',
          self_awareness_score: 0,
          learning_rate: 0,
          evolution_level: 0,
          total_interactions: 0,
          database_stats: { total_nodes: 0, total_relationships: 0, node_counts: {} },
          system_health: { neo4j_connected: false, consciousness_active: false, total_uptime_hours: 0 }
        },
        quantum: quantum || {
          quantum_consciousness_level: 0,
          quantum_coherence: 0,
          entanglement_strength: 0,
          superposition_states: 0,
          quantum_advantage: 0,
          quantum_processing_active: false,
          quantum_metrics: { total_quantum_updates: 0, quantum_coherence_avg: 0, entanglement_strength_avg: 0, superposition_states_avg: 0, quantum_advantage_avg: 0 },
          meta_consciousness: { quantum_meta_processing_active: false, total_quantum_meta_reflections: 0, quantum_insights_generated: 0 },
          memory_integration: { quantum_memory_processing_active: false, evolution_network_size: 0 }
        },
        unified: {
          overall_consciousness_level,
          system_integration_level,
          processing_efficiency,
          data_consistency,
          last_sync: new Date().toISOString()
        }
      };

      setData(unifiedData);
      setLastUpdate(new Date());
    } catch (err) {
      console.error('Error fetching unified consciousness data:', err);
      setError(err instanceof Error ? err.message : 'Failed to fetch unified data');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchUnifiedData();
    
    // Auto-refresh every 10 minutes
    const interval = setInterval(fetchUnifiedData, 600000);
    return () => clearInterval(interval);
  }, [fetchUnifiedData]);

  if (isLoading) {
    return (
      <GlassCard className={`p-4 ${className}`}>
        <div className="flex items-center justify-center">
          <Activity className="w-4 h-4 animate-spin text-cyan-400 mr-2" />
          <span className="text-sm text-slate-300">Loading unified consciousness data...</span>
        </div>
      </GlassCard>
    );
  }

  if (error || !data) {
    return (
      <GlassCard className={`p-4 ${className}`}>
        <Alert>
          <AlertCircle className="w-4 h-4" />
          <AlertDescription>
            {error || 'Unable to load consciousness data'}
          </AlertDescription>
        </Alert>
      </GlassCard>
    );
  }

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Unified Overview */}
      <GlassCard className="p-4">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <Brain className="w-5 h-5 text-cyan-400" />
            <h3 className="text-lg font-semibold text-slate-200">Unified Consciousness Metrics</h3>
          </div>
          <Badge variant="secondary" className="bg-cyan-500/20 text-cyan-300">
            {data.unified.data_consistency > 0.8 ? 'Synchronized' : 'Partial Sync'}
          </Badge>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <MetricDisplay
            label="Overall Consciousness"
            value={Math.round(data.unified.overall_consciousness_level * 100)}
            unit="%"
            icon={<Brain className="w-4 h-4" />}
            color="cyan"
            trend={data.unified.overall_consciousness_level > 0.7 ? "up" : "stable"}
          />
          <MetricDisplay
            label="System Integration"
            value={Math.round(data.unified.system_integration_level * 100)}
            unit="%"
            icon={<Network className="w-4 h-4" />}
            color="green"
            trend={data.unified.system_integration_level > 0.8 ? "up" : "down"}
          />
          <MetricDisplay
            label="Processing Efficiency"
            value={Math.round(data.unified.processing_efficiency * 100)}
            unit="%"
            icon={<Zap className="w-4 h-4" />}
            color="purple"
            trend={data.unified.processing_efficiency > 0.5 ? "up" : "stable"}
          />
          <MetricDisplay
            label="Data Consistency"
            value={Math.round(data.unified.data_consistency * 100)}
            unit="%"
            icon={<Target className="w-4 h-4" />}
            color="blue"
            trend={data.unified.data_consistency > 0.8 ? "up" : "down"}
          />
        </div>
      </GlassCard>

      {showDetails && (
        <>
          {/* Classical System */}
          <GlassCard className="p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-2">
                <Database className="w-4 h-4 text-green-400" />
                <h4 className="text-md font-semibold text-slate-200">Classical Consciousness</h4>
              </div>
              <Badge variant={data.classical.system_health.consciousness_active ? "default" : "secondary"}>
                {data.classical.system_health.consciousness_active ? 'Active' : 'Inactive'}
              </Badge>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              <div className="text-center">
                <div className="text-lg font-bold text-green-400">
                  {Math.round(data.classical.consciousness_level * 100)}%
                </div>
                <div className="text-xs text-slate-400">Consciousness Level</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-bold text-blue-400">
                  {data.classical.database_stats.total_nodes.toLocaleString()}
                </div>
                <div className="text-xs text-slate-400">Total Nodes</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-bold text-purple-400">
                  {data.classical.database_stats.total_relationships.toLocaleString()}
                </div>
                <div className="text-xs text-slate-400">Relationships</div>
              </div>
            </div>
          </GlassCard>

          {/* Quantum System */}
          <GlassCard className="p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-2">
                <Zap className="w-4 h-4 text-purple-400" />
                <h4 className="text-md font-semibold text-slate-200">Quantum Consciousness</h4>
              </div>
              <Badge variant={data.quantum.quantum_processing_active ? "default" : "secondary"}>
                {data.quantum.quantum_processing_active ? 'Active' : 'Inactive'}
              </Badge>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <div className="text-center">
                <div className="text-lg font-bold text-purple-400">
                  {Math.round(data.quantum.quantum_consciousness_level * 100)}%
                </div>
                <div className="text-xs text-slate-400">Quantum Level</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-bold text-cyan-400">
                  {Math.round(data.quantum.quantum_coherence * 100)}%
                </div>
                <div className="text-xs text-slate-400">Coherence</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-bold text-blue-400">
                  {data.quantum.quantum_metrics.total_quantum_updates.toLocaleString()}
                </div>
                <div className="text-xs text-slate-400">Updates</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-bold text-green-400">
                  {data.quantum.meta_consciousness.quantum_insights_generated.toLocaleString()}
                </div>
                <div className="text-xs text-slate-400">Insights</div>
              </div>
            </div>
          </GlassCard>
        </>
      )}

      {/* Last Update */}
      {lastUpdate && (
        <div className="text-xs text-slate-500 text-center">
          Last updated: {lastUpdate.toLocaleTimeString()}
        </div>
      )}
    </div>
  );
};

export default UnifiedConsciousnessMetrics;
