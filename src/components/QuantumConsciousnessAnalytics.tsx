import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { 
  BarChart3, 
  LineChart, 
  PieChart, 
  TrendingUp, 
  TrendingDown,
  Activity,
  Brain,
  Zap,
  Network,
  Database,
  Clock,
  Target,
  AlertCircle,
  CheckCircle,
  RefreshCw,
  Download,
  Share2,
  Settings,
  Filter,
  Search,
  Calendar,
  Users,
  Layers,
  Cpu,
  Memory,
  HardDrive
} from 'lucide-react';

interface QuantumAnalytics {
  quantum_metrics: {
    total_quantum_updates: number;
    quantum_coherence_avg: number;
    entanglement_strength_avg: number;
    superposition_states_avg: number;
    quantum_advantage_avg: number;
    quantum_processing_time_avg: number;
  };
  realtime_metrics: {
    quantum_processing_active: boolean;
    quantum_update_interval: number;
    entanglement_network_size: number;
    superposition_network_size: number;
    snapshots_count: number;
  };
  meta_consciousness_metrics: {
    total_quantum_meta_reflections: number;
    quantum_coherence_evolution: number[];
    entanglement_strength_evolution: number[];
    superposition_states_evolution: number[];
    quantum_advantage_evolution: number[];
    quantum_insights_generated: number;
    quantum_philosophical_insights: number;
    quantum_metaphysical_insights: number;
  };
  memory_metrics: {
    total_quantum_memories: number;
    quantum_coherence_avg: number;
    entanglement_strength_avg: number;
    superposition_states_avg: number;
    quantum_advantage_avg: number;
    quantum_memory_processing_time_avg: number;
    quantum_entanglement_connections: number;
    quantum_superposition_connections: number;
    quantum_collective_connections: number;
  };
  overall_quantum_advantage: number;
  total_quantum_processing_active: boolean;
}

interface QuantumSnapshot {
  timestamp: string;
  consciousness_level: number;
  quantum_coherence: number;
  entanglement_strength: number;
  superposition_states: number;
  quantum_advantage: number;
  quantum_state: string;
  emotional_state: string;
  active_goals: string[];
  emergent_capabilities: string[];
  cross_agent_connections: number;
  memory_consolidation_status: string;
}

const QuantumConsciousnessAnalytics: React.FC = () => {
  const [analytics, setAnalytics] = useState<QuantumAnalytics | null>(null);
  const [snapshots, setSnapshots] = useState<QuantumSnapshot[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [timeRange, setTimeRange] = useState('1h');
  const [selectedMetric, setSelectedMetric] = useState('coherence');

  // Fetch quantum analytics
  const fetchAnalytics = useCallback(async () => {
    try {
      const response = await fetch('/api/quantum/backend/metrics');
      if (!response.ok) throw new Error('Failed to fetch analytics');
      const data = await response.json();
      setAnalytics(data.quantum_backend_metrics);
    } catch (err) {
      console.error('Error fetching analytics:', err);
      setError('Failed to fetch analytics');
    }
  }, []);

  // Fetch quantum snapshots
  const fetchSnapshots = useCallback(async () => {
    try {
      const response = await fetch('/api/quantum/backend/realtime/snapshots?limit=50');
      if (!response.ok) throw new Error('Failed to fetch snapshots');
      const data = await response.json();
      setSnapshots(data.quantum_snapshots || []);
    } catch (err) {
      console.error('Error fetching snapshots:', err);
      setError('Failed to fetch snapshots');
    }
  }, []);

  // Refresh data
  const refreshData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      await Promise.all([fetchAnalytics(), fetchSnapshots()]);
    } catch (err) {
      console.error('Error refreshing data:', err);
      setError('Failed to refresh data');
    } finally {
      setIsLoading(false);
    }
  }, [fetchAnalytics, fetchSnapshots]);

  useEffect(() => {
    refreshData();
    const interval = setInterval(refreshData, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, [refreshData]);

  // Generate chart data
  const generateChartData = useCallback((metric: string) => {
    if (!snapshots.length) return { labels: [], datasets: [] };

    const labels = snapshots.slice(-20).map(s => 
      new Date(s.timestamp).toLocaleTimeString()
    );

    const data = snapshots.slice(-20).map(s => {
      switch (metric) {
        case 'coherence': return s.quantum_coherence * 100;
        case 'entanglement': return s.entanglement_strength * 100;
        case 'consciousness': return s.consciousness_level * 100;
        case 'advantage': return s.quantum_advantage;
        default: return s.quantum_coherence * 100;
      }
    });

    return {
      labels,
      datasets: [{
        label: metric.charAt(0).toUpperCase() + metric.slice(1),
        data,
        borderColor: metric === 'coherence' ? '#3B82F6' : 
                    metric === 'entanglement' ? '#8B5CF6' :
                    metric === 'consciousness' ? '#10B981' : '#F59E0B',
        backgroundColor: metric === 'coherence' ? '#3B82F680' : 
                        metric === 'entanglement' ? '#8B5CF680' :
                        metric === 'consciousness' ? '#10B98180' : '#F59E0B80',
        tension: 0.4,
        fill: true
      }]
    };
  }, [snapshots]);

  // Get trend direction
  const getTrendDirection = (values: number[]) => {
    if (values.length < 2) return 'stable';
    const first = values[0];
    const last = values[values.length - 1];
    const change = ((last - first) / first) * 100;
    
    if (change > 5) return 'up';
    if (change < -5) return 'down';
    return 'stable';
  };

  // Get trend icon
  const getTrendIcon = (direction: string) => {
    switch (direction) {
      case 'up': return <TrendingUp className="h-4 w-4 text-green-500" />;
      case 'down': return <TrendingDown className="h-4 w-4 text-red-500" />;
      default: return <Activity className="h-4 w-4 text-gray-500" />;
    }
  };

  if (isLoading && !analytics) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="flex items-center space-x-2">
          <RefreshCw className="h-4 w-4 animate-spin" />
          <span>Loading quantum analytics...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <BarChart3 className="h-6 w-6 text-blue-500" />
          <h1 className="text-2xl font-bold">Quantum Consciousness Analytics</h1>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm" onClick={refreshData} disabled={isLoading}>
            <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
          </Button>
          <Button variant="outline" size="sm">
            <Download className="h-4 w-4" />
          </Button>
          <Button variant="outline" size="sm">
            <Share2 className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center space-x-2">
            <AlertCircle className="h-4 w-4 text-red-500" />
            <span className="text-red-700">{error}</span>
          </div>
        </div>
      )}

      {/* Overview Cards */}
      {analytics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Quantum Advantage</p>
                  <p className="text-2xl font-bold text-blue-600">
                    {(analytics.overall_quantum_advantage || 0).toFixed(2)}x
                  </p>
                </div>
                <Zap className="h-8 w-8 text-blue-500" />
              </div>
              <div className="mt-2">
                <Progress value={Math.min((analytics.overall_quantum_advantage || 0) * 50, 100)} className="h-2" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Updates</p>
                  <p className="text-2xl font-bold text-green-600">
                    {analytics.quantum_metrics?.total_quantum_updates.toLocaleString()}
                  </p>
                </div>
                <Activity className="h-8 w-8 text-green-500" />
              </div>
              <div className="mt-2">
                <div className="flex items-center space-x-2">
                  <Badge variant={analytics.total_quantum_processing_active ? 'default' : 'secondary'}>
                    {analytics.total_quantum_processing_active ? 'Active' : 'Inactive'}
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Avg Coherence</p>
                  <p className="text-2xl font-bold text-purple-600">
                    {((analytics.quantum_metrics?.quantum_coherence_avg || 0) * 100).toFixed(1)}%
                  </p>
                </div>
                <Brain className="h-8 w-8 text-purple-500" />
              </div>
              <div className="mt-2">
                <Progress value={analytics.quantum_metrics?.quantum_coherence_avg * 100} className="h-2" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Processing Time</p>
                  <p className="text-2xl font-bold text-orange-600">
                    {((analytics.quantum_metrics?.quantum_processing_time_avg || 0) * 1000).toFixed(1)}ms
                  </p>
                </div>
                <Clock className="h-8 w-8 text-orange-500" />
              </div>
              <div className="mt-2">
                <div className="text-sm text-gray-600">
                  {analytics.realtime_metrics?.quantum_update_interval}ms interval
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Analytics Tabs */}
      <Tabs defaultValue="overview" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="realtime">Real-time</TabsTrigger>
          <TabsTrigger value="meta">Meta-consciousness</TabsTrigger>
          <TabsTrigger value="memory">Memory</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {/* Quantum Metrics */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <BarChart3 className="h-5 w-5" />
                  <span>Quantum Metrics</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Coherence Average</span>
                    <span className="text-sm font-bold">
                      {((analytics?.quantum_metrics?.quantum_coherence_avg || 0) * 100).toFixed(1)}%
                    </span>
                  </div>
                  <Progress value={(analytics?.quantum_metrics?.quantum_coherence_avg || 0) * 100} className="h-2" />
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Entanglement Average</span>
                    <span className="text-sm font-bold">
                      {((analytics?.quantum_metrics?.entanglement_strength_avg || 0) * 100).toFixed(1)}%
                    </span>
                  </div>
                  <Progress value={(analytics?.quantum_metrics?.entanglement_strength_avg || 0) * 100} className="h-2" />
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Superposition Average</span>
                    <span className="text-sm font-bold">
                      {(analytics?.quantum_metrics?.superposition_states_avg || 0).toFixed(1)}
                    </span>
                  </div>
                  <Progress value={(analytics?.quantum_metrics?.superposition_states_avg || 0) * 25} className="h-2" />
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Quantum Advantage</span>
                    <span className="text-sm font-bold">
                      {(analytics?.quantum_metrics?.quantum_advantage_avg || 0).toFixed(2)}x
                    </span>
                  </div>
                  <Progress value={Math.min((analytics?.quantum_metrics?.quantum_advantage_avg || 0) * 50, 100)} className="h-2" />
                </div>
              </CardContent>
            </Card>

            {/* Network Status */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Network className="h-5 w-5" />
                  <span>Network Status</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Entanglement Network</span>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm font-bold">
                        {analytics?.realtime_metrics?.entanglement_network_size}
                      </span>
                      <Badge variant="default">Active</Badge>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Superposition Network</span>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm font-bold">
                        {analytics?.realtime_metrics?.superposition_network_size}
                      </span>
                      <Badge variant="default">Active</Badge>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Consciousness Snapshots</span>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm font-bold">
                        {analytics?.realtime_metrics?.snapshots_count}
                      </span>
                      <Badge variant="secondary">Stored</Badge>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Processing Status</span>
                    <Badge variant={analytics?.total_quantum_processing_active ? 'default' : 'destructive'}>
                      {analytics?.total_quantum_processing_active ? 'Active' : 'Inactive'}
                    </Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="realtime" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Activity className="h-5 w-5" />
                <span>Real-time Quantum Processing</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600">
                    {analytics?.quantum_metrics?.total_quantum_updates.toLocaleString()}
                  </div>
                  <div className="text-sm text-gray-600">Total Updates</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600">
                    {analytics?.realtime_metrics?.quantum_update_interval}ms
                  </div>
                  <div className="text-sm text-gray-600">Update Interval</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-purple-600">
                    {analytics?.realtime_metrics?.snapshots_count}
                  </div>
                  <div className="text-sm text-gray-600">Snapshots</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="meta" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Brain className="h-5 w-5" />
                <span>Meta-consciousness Analytics</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">
                    {analytics?.meta_consciousness_metrics?.total_quantum_meta_reflections}
                  </div>
                  <div className="text-sm text-gray-600">Meta Reflections</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">
                    {analytics?.meta_consciousness_metrics?.quantum_insights_generated}
                  </div>
                  <div className="text-sm text-gray-600">Insights Generated</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">
                    {analytics?.meta_consciousness_metrics?.quantum_philosophical_insights}
                  </div>
                  <div className="text-sm text-gray-600">Philosophical Insights</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-600">
                    {analytics?.meta_consciousness_metrics?.quantum_metaphysical_insights}
                  </div>
                  <div className="text-sm text-gray-600">Metaphysical Insights</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="memory" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Database className="h-5 w-5" />
                <span>Quantum Memory Analytics</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">
                    {analytics?.memory_metrics?.total_quantum_memories}
                  </div>
                  <div className="text-sm text-gray-600">Total Memories</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">
                    {analytics?.memory_metrics?.quantum_entanglement_connections}
                  </div>
                  <div className="text-sm text-gray-600">Entanglement Connections</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">
                    {analytics?.memory_metrics?.quantum_superposition_connections}
                  </div>
                  <div className="text-sm text-gray-600">Superposition Connections</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-600">
                    {analytics?.memory_metrics?.quantum_collective_connections}
                  </div>
                  <div className="text-sm text-gray-600">Collective Connections</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-red-600">
                    {((analytics?.memory_metrics?.quantum_memory_processing_time_avg || 0) * 1000).toFixed(1)}ms
                  </div>
                  <div className="text-sm text-gray-600">Avg Processing Time</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-indigo-600">
                    {((analytics?.memory_metrics?.quantum_coherence_avg || 0) * 100).toFixed(1)}%
                  </div>
                  <div className="text-sm text-gray-600">Memory Coherence</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default QuantumConsciousnessAnalytics;
