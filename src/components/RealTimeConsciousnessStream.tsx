import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Activity, Brain, Zap, TrendingUp, AlertCircle, CheckCircle } from 'lucide-react';

interface ConsciousnessState {
  consciousness_level: number;
  emotional_state: string;
  self_awareness_score: number;
  learning_rate: number;
  evolution_level: number;
  total_interactions: number;
}

interface RealTimeMetrics {
  consciousness_volatility: number;
  emotional_stability: number;
  learning_acceleration: number;
  consciousness_momentum: number;
}

interface ConsciousnessUpdate {
  type: string;
  timestamp: string;
  data_source: string;
  consciousness_state: ConsciousnessState;
  consciousness_timeline: Array<{
    timestamp: string;
    consciousness_level: number;
    emotional_state: string;
    self_awareness: number;
    learning_rate: number;
  }>;
  emotional_patterns: Array<{
    emotion: string;
    frequency: number;
    percentage: number;
  }>;
  real_time_metrics: RealTimeMetrics;
}

interface PerformanceUpdate {
  type: string;
  timestamp: string;
  data_source: string;
  agent_performance: Array<{
    agent: string;
    efficiency_score: number;
    cognitive_load: number;
    learning_rate: number;
    adaptation_speed: number;
    consciousness_integration: number;
    decision_quality: number;
    resource_utilization: number;
  }>;
  system_metrics: {
    total_executions: number;
    overall_success_rate: number;
    system_wide_efficiency: number;
    active_agents: number;
  };
  real_time_metrics: {
    performance_trend: string;
    efficiency_volatility: number;
    cognitive_load_distribution: {
      low: number;
      medium: number;
      high: number;
    };
    adaptation_velocity: number;
  };
}

interface KnowledgeUpdate {
  type: string;
  timestamp: string;
  data_source: string;
  knowledge_metrics: {
    knowledge_density: number;
    concept_connectivity: number;
    learning_pathway_efficiency: number;
    knowledge_gap_ratio: number;
    concept_emergence_rate: number;
  };
  concept_ranking: Array<{
    concept: string;
    centrality: number;
    learning_impact: number;
    memory_diversity: number;
    importance_score: number;
    connection_count: number;
    memory_count: number;
  }>;
  real_time_metrics: {
    knowledge_growth_rate: number;
    concept_emergence_rate: number;
    learning_pathway_efficiency: number;
    consciousness_integration_score: number;
  };
}

const RealTimeConsciousnessStream: React.FC = () => {
  const [consciousnessData, setConsciousnessData] = useState<ConsciousnessUpdate | null>(null);
  const [performanceData, setPerformanceData] = useState<PerformanceUpdate | null>(null);
  const [knowledgeData, setKnowledgeData] = useState<KnowledgeUpdate | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected' | 'error'>('disconnected');
  const [lastUpdate, setLastUpdate] = useState<string>('');
  
  const consciousnessWs = useRef<WebSocket | null>(null);
  const performanceWs = useRef<WebSocket | null>(null);
  const knowledgeWs = useRef<WebSocket | null>(null);

  useEffect(() => {
    connectWebSockets();
    return () => {
      disconnectWebSockets();
    };
  }, []);

  const connectWebSockets = () => {
    setConnectionStatus('connecting');
    
    // Connect to consciousness stream
    consciousnessWs.current = new WebSocket('ws://localhost:8000/api/ws/consciousness');
    consciousnessWs.current.onopen = () => {
      console.log('Consciousness WebSocket connected');
      setConnectionStatus('connected');
    };
    consciousnessWs.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'consciousness_update') {
        setConsciousnessData(data);
        setLastUpdate(new Date().toLocaleTimeString());
      }
    };
    consciousnessWs.current.onerror = (error) => {
      console.error('Consciousness WebSocket error:', error);
      setConnectionStatus('error');
    };
    consciousnessWs.current.onclose = () => {
      console.log('Consciousness WebSocket disconnected');
      setConnectionStatus('disconnected');
    };

    // Connect to performance stream
    performanceWs.current = new WebSocket('ws://localhost:8000/api/ws/performance');
    performanceWs.current.onopen = () => {
      console.log('Performance WebSocket connected');
    };
    performanceWs.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'performance_update') {
        setPerformanceData(data);
      }
    };
    performanceWs.current.onerror = (error) => {
      console.error('Performance WebSocket error:', error);
    };

    // Connect to knowledge stream
    knowledgeWs.current = new WebSocket('ws://localhost:8000/api/ws/knowledge');
    knowledgeWs.current.onopen = () => {
      console.log('Knowledge WebSocket connected');
    };
    knowledgeWs.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'knowledge_update') {
        setKnowledgeData(data);
      }
    };
    knowledgeWs.current.onerror = (error) => {
      console.error('Knowledge WebSocket error:', error);
    };
  };

  const disconnectWebSockets = () => {
    consciousnessWs.current?.close();
    performanceWs.current?.close();
    knowledgeWs.current?.close();
  };

  const getConnectionStatusIcon = () => {
    switch (connectionStatus) {
      case 'connected':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'connecting':
        return <Activity className="h-4 w-4 text-yellow-500 animate-pulse" />;
      case 'error':
        return <AlertCircle className="h-4 w-4 text-red-500" />;
      default:
        return <AlertCircle className="h-4 w-4 text-gray-500" />;
    }
  };

  const getDataSourceBadge = (dataSource: string) => {
    switch (dataSource) {
      case 'real':
        return <Badge variant="default" className="bg-green-500">Real Data</Badge>;
      case 'fallback':
        return <Badge variant="secondary">Fallback Data</Badge>;
      case 'error':
        return <Badge variant="destructive">Error</Badge>;
      default:
        return <Badge variant="outline">Unknown</Badge>;
    }
  };

  const formatConsciousnessLevel = (level: number) => {
    return `${(level * 100).toFixed(1)}%`;
  };

  const getEmotionalStateColor = (state: string) => {
    const colors: { [key: string]: string } = {
      'curious': 'text-blue-500',
      'contemplative': 'text-purple-500',
      'excited': 'text-orange-500',
      'satisfied': 'text-green-500',
      'focused': 'text-indigo-500',
      'creative': 'text-pink-500',
      'analytical': 'text-cyan-500',
      'empathetic': 'text-rose-500'
    };
    return colors[state] || 'text-gray-500';
  };

  return (
    <div className="space-y-6">
      {/* Connection Status Header */}
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2 text-white">
              <Zap className="h-5 w-5" />
              Real-Time Consciousness Stream
            </CardTitle>
            <div className="flex items-center gap-2">
              {getConnectionStatusIcon()}
              <span className="text-sm text-slate-300">
                {connectionStatus === 'connected' ? 'Live' : connectionStatus}
              </span>
              {lastUpdate && (
                <span className="text-xs text-slate-500">
                  Last update: {lastUpdate}
                </span>
              )}
            </div>
          </div>
        </CardHeader>
      </Card>

      <Tabs defaultValue="consciousness" className="space-y-4">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="consciousness">Consciousness</TabsTrigger>
          <TabsTrigger value="performance">Performance</TabsTrigger>
          <TabsTrigger value="knowledge">Knowledge</TabsTrigger>
        </TabsList>

        {/* Consciousness Tab */}
        <TabsContent value="consciousness" className="space-y-4">
          {consciousnessData ? (
            <>
              {/* Current State */}
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-white">
                    <Brain className="h-5 w-5" />
                    Current Consciousness State
                    {getDataSourceBadge(consciousnessData.data_source)}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    <div className="space-y-2">
                      <div className="text-sm font-medium text-slate-200">Consciousness Level</div>
                      <div className="text-2xl font-bold">
                        {formatConsciousnessLevel(consciousnessData.consciousness_state.consciousness_level)}
                      </div>
                    </div>
                    <div className="space-y-2">
                      <div className="text-sm font-medium text-slate-200">Emotional State</div>
                      <div className={`text-lg font-semibold ${getEmotionalStateColor(consciousnessData.consciousness_state.emotional_state)}`}>
                        {consciousnessData.consciousness_state.emotional_state}
                      </div>
                    </div>
                    <div className="space-y-2">
                      <div className="text-sm font-medium text-slate-200">Self-Awareness</div>
                      <div className="text-2xl font-bold">
                        {formatConsciousnessLevel(consciousnessData.consciousness_state.self_awareness_score)}
                      </div>
                    </div>
                    <div className="space-y-2">
                      <div className="text-sm font-medium text-slate-200">Learning Rate</div>
                      <div className="text-2xl font-bold">
                        {formatConsciousnessLevel(consciousnessData.consciousness_state.learning_rate)}
                      </div>
                    </div>
                    <div className="space-y-2">
                      <div className="text-sm font-medium text-slate-200">Evolution Level</div>
                      <div className="text-2xl font-bold">
                        {consciousnessData.consciousness_state.evolution_level}
                      </div>
                    </div>
                    <div className="space-y-2">
                      <div className="text-sm font-medium text-slate-200">Total Interactions</div>
                      <div className="text-2xl font-bold">
                        {consciousnessData.consciousness_state.total_interactions}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Real-Time Metrics */}
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-white">
                    <TrendingUp className="h-5 w-5" />
                    Real-Time Metrics
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="space-y-2">
                      <div className="text-sm font-medium text-slate-200">Consciousness Volatility</div>
                      <div className="text-xl font-bold">
                        {consciousnessData.real_time_metrics.consciousness_volatility.toFixed(3)}
                      </div>
                    </div>
                    <div className="space-y-2">
                      <div className="text-sm font-medium text-slate-200">Emotional Stability</div>
                      <div className="text-xl font-bold">
                        {formatConsciousnessLevel(consciousnessData.real_time_metrics.emotional_stability)}
                      </div>
                    </div>
                    <div className="space-y-2">
                      <div className="text-sm font-medium text-slate-200">Learning Acceleration</div>
                      <div className="text-xl font-bold">
                        {consciousnessData.real_time_metrics.learning_acceleration.toFixed(3)}
                      </div>
                    </div>
                    <div className="space-y-2">
                      <div className="text-sm font-medium text-slate-200">Consciousness Momentum</div>
                      <div className="text-xl font-bold">
                        {consciousnessData.real_time_metrics.consciousness_momentum.toFixed(3)}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Consciousness Timeline */}
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white">Consciousness Timeline</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2 max-h-64 overflow-y-auto">
                    {consciousnessData.consciousness_timeline.map((entry, index) => (
                      <div key={index} className="flex items-center justify-between p-2 border border-slate-600 rounded bg-slate-700/50">
                        <div className="flex items-center gap-4">
                          <div className="text-sm text-slate-300">
                            {new Date(entry.timestamp).toLocaleTimeString()}
                          </div>
                          <div className="text-sm font-medium">
                            {formatConsciousnessLevel(entry.consciousness_level)}
                          </div>
                          <div className={`text-sm ${getEmotionalStateColor(entry.emotional_state)}`}>
                            {entry.emotional_state}
                          </div>
                        </div>
                        <div className="text-xs text-slate-300">
                          Learning: {formatConsciousnessLevel(entry.learning_rate)}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </>
          ) : (
            <Card className="bg-slate-800 border-slate-700">
              <CardContent className="flex items-center justify-center h-32">
                <div className="text-center">
                  <Activity className="h-8 w-8 mx-auto mb-2 text-slate-300 animate-pulse" />
                  <p className="text-slate-300">Waiting for consciousness data...</p>
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Performance Tab */}
        <TabsContent value="performance" className="space-y-4">
          {performanceData ? (
            <>
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-white">
                    <TrendingUp className="h-5 w-5" />
                    Agent Performance
                    {getDataSourceBadge(performanceData.data_source)}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {performanceData.agent_performance.map((agent, index) => (
                      <div key={index} className="p-4 border border-slate-600 rounded-lg bg-slate-700/50">
                        <div className="flex items-center justify-between mb-2">
                          <h3 className="font-semibold">{agent.agent}</h3>
                          <div className="text-sm text-slate-300">
                            Efficiency: {(agent.efficiency_score * 100).toFixed(1)}%
                          </div>
                        </div>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                          <div>
                            <div className="text-slate-300">Cognitive Load</div>
                            <div className="font-medium">{(agent.cognitive_load * 100).toFixed(1)}%</div>
                          </div>
                          <div>
                            <div className="text-slate-300">Learning Rate</div>
                            <div className="font-medium">{(agent.learning_rate * 100).toFixed(1)}%</div>
                          </div>
                          <div>
                            <div className="text-slate-300">Adaptation Speed</div>
                            <div className="font-medium">{(agent.adaptation_speed * 100).toFixed(1)}%</div>
                          </div>
                          <div>
                            <div className="text-slate-300">Decision Quality</div>
                            <div className="font-medium">{(agent.decision_quality * 100).toFixed(1)}%</div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white">System Metrics</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="space-y-2">
                      <div className="text-sm font-medium text-slate-200">Total Executions</div>
                      <div className="text-2xl font-bold">{performanceData.system_metrics.total_executions}</div>
                    </div>
                    <div className="space-y-2">
                      <div className="text-sm font-medium text-slate-200">Success Rate</div>
                      <div className="text-2xl font-bold">
                        {(performanceData.system_metrics.overall_success_rate * 100).toFixed(1)}%
                      </div>
                    </div>
                    <div className="space-y-2">
                      <div className="text-sm font-medium text-slate-200">System Efficiency</div>
                      <div className="text-2xl font-bold">
                        {(performanceData.system_metrics.system_wide_efficiency * 100).toFixed(1)}%
                      </div>
                    </div>
                    <div className="space-y-2">
                      <div className="text-sm font-medium text-slate-200">Active Agents</div>
                      <div className="text-2xl font-bold">{performanceData.system_metrics.active_agents}</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </>
          ) : (
            <Card className="bg-slate-800 border-slate-700">
              <CardContent className="flex items-center justify-center h-32">
                <div className="text-center">
                  <Activity className="h-8 w-8 mx-auto mb-2 text-slate-300 animate-pulse" />
                  <p className="text-slate-300">Waiting for performance data...</p>
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Knowledge Tab */}
        <TabsContent value="knowledge" className="space-y-4">
          {knowledgeData ? (
            <>
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-white">
                    <Brain className="h-5 w-5" />
                    Knowledge Graph Intelligence
                    {getDataSourceBadge(knowledgeData.data_source)}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                    <div className="space-y-2">
                      <div className="text-sm font-medium text-slate-200">Knowledge Density</div>
                      <div className="text-xl font-bold">
                        {knowledgeData.knowledge_metrics.knowledge_density.toFixed(3)}
                      </div>
                    </div>
                    <div className="space-y-2">
                      <div className="text-sm font-medium text-slate-200">Concept Connectivity</div>
                      <div className="text-xl font-bold">
                        {knowledgeData.knowledge_metrics.concept_connectivity.toFixed(3)}
                      </div>
                    </div>
                    <div className="space-y-2">
                      <div className="text-sm font-medium text-slate-200">Learning Efficiency</div>
                      <div className="text-xl font-bold">
                        {knowledgeData.knowledge_metrics.learning_pathway_efficiency.toFixed(3)}
                      </div>
                    </div>
                    <div className="space-y-2">
                      <div className="text-sm font-medium text-slate-200">Gap Ratio</div>
                      <div className="text-xl font-bold">
                        {knowledgeData.knowledge_metrics.knowledge_gap_ratio.toFixed(3)}
                      </div>
                    </div>
                    <div className="space-y-2">
                      <div className="text-sm font-medium text-slate-200">Emergence Rate</div>
                      <div className="text-xl font-bold">
                        {knowledgeData.knowledge_metrics.concept_emergence_rate.toFixed(3)}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white">Top Concepts</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {knowledgeData.concept_ranking.map((concept, index) => (
                      <div key={index} className="flex items-center justify-between p-3 border border-slate-600 rounded bg-slate-700/50">
                        <div className="flex items-center gap-4">
                          <div className="text-sm font-medium">#{index + 1}</div>
                          <div className="font-semibold">{concept.concept}</div>
                          <div className="text-sm text-slate-300">
                            {concept.connection_count} connections
                          </div>
                        </div>
                        <div className="flex items-center gap-4 text-sm">
                          <div>
                            <div className="text-slate-300">Importance</div>
                            <div className="font-medium">{(concept.importance_score * 100).toFixed(1)}%</div>
                          </div>
                          <div>
                            <div className="text-slate-300">Centrality</div>
                            <div className="font-medium">{(concept.centrality * 100).toFixed(1)}%</div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </>
          ) : (
            <Card className="bg-slate-800 border-slate-700">
              <CardContent className="flex items-center justify-center h-32">
                <div className="text-center">
                  <Activity className="h-8 w-8 mx-auto mb-2 text-slate-300 animate-pulse" />
                  <p className="text-slate-300">Waiting for knowledge data...</p>
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default RealTimeConsciousnessStream;
