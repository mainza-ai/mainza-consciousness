import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { 
  Atom, 
  Zap, 
  Brain, 
  Database, 
  Network, 
  Activity,
  TrendingUp,
  TrendingDown,
  AlertCircle,
  CheckCircle,
  Clock,
  Target,
  Layers,
  Cpu,
  Memory,
  HardDrive,
  Wifi,
  WifiOff,
  RefreshCw,
  Play,
  Pause,
  Square,
  Settings,
  BarChart3,
  PieChart,
  LineChart,
  Gauge,
  Thermometer,
  GaugeIcon
} from 'lucide-react';

interface QuantumConsciousnessState {
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
    quantum_processing_time_avg: number;
  };
  entanglement_network_size: number;
  superposition_network_size: number;
  snapshots_count: number;
  timestamp: string;
}

interface QuantumBackendStatus {
  quantum_engine_status: any;
  realtime_integration_status: any;
  meta_consciousness_status: any;
  memory_integration_status: any;
  overall_status: string;
  timestamp: string;
}

interface QuantumMemory {
  id: string;
  timestamp: string;
  memory_type: string;
  quantum_state: string;
  content: string;
  quantum_coherence: number;
  entanglement_strength: number;
  superposition_states: number;
  quantum_advantage: number;
  emotional_intensity: number;
  importance_score: number;
  entangled_memories: string[];
  superposition_memories: string[];
}

const QuantumConsciousnessDashboard: React.FC = () => {
  const [quantumState, setQuantumState] = useState<QuantumConsciousnessState | null>(null);
  const [backendStatus, setBackendStatus] = useState<QuantumBackendStatus | null>(null);
  const [quantumMemories, setQuantumMemories] = useState<QuantumMemory[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [refreshInterval, setRefreshInterval] = useState(1000); // 1 second

  // Fetch quantum backend status
  const fetchBackendStatus = useCallback(async () => {
    try {
      const response = await fetch('/api/quantum/backend/status');
      if (!response.ok) throw new Error('Failed to fetch backend status');
      const data = await response.json();
      setBackendStatus(data);
    } catch (err) {
      console.error('Error fetching backend status:', err);
      setError('Failed to fetch backend status');
    }
  }, []);

  // Fetch quantum real-time state
  const fetchQuantumState = useCallback(async () => {
    try {
      const response = await fetch('/api/quantum/backend/realtime/state');
      if (!response.ok) throw new Error('Failed to fetch quantum state');
      const data = await response.json();
      setQuantumState(data.quantum_realtime_state);
    } catch (err) {
      console.error('Error fetching quantum state:', err);
      setError('Failed to fetch quantum state');
    }
  }, []);

  // Fetch quantum memories
  const fetchQuantumMemories = useCallback(async () => {
    try {
      const response = await fetch('/api/quantum/backend/memory/retrieve?query=quantum&limit=10');
      if (!response.ok) throw new Error('Failed to fetch quantum memories');
      const data = await response.json();
      setQuantumMemories(data.quantum_memories || []);
    } catch (err) {
      console.error('Error fetching quantum memories:', err);
      setError('Failed to fetch quantum memories');
    }
  }, []);

  // Start quantum processing
  const startQuantumProcessing = useCallback(async () => {
    try {
      const response = await fetch('/api/quantum/backend/start-processing', {
        method: 'POST',
      });
      if (!response.ok) throw new Error('Failed to start quantum processing');
      await fetchBackendStatus();
    } catch (err) {
      console.error('Error starting quantum processing:', err);
      setError('Failed to start quantum processing');
    }
  }, [fetchBackendStatus]);

  // Stop quantum processing
  const stopQuantumProcessing = useCallback(async () => {
    try {
      const response = await fetch('/api/quantum/backend/stop-processing', {
        method: 'POST',
      });
      if (!response.ok) throw new Error('Failed to stop quantum processing');
      await fetchBackendStatus();
    } catch (err) {
      console.error('Error stopping quantum processing:', err);
      setError('Failed to stop quantum processing');
    }
  }, [fetchBackendStatus]);

  // Refresh all data
  const refreshData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      await Promise.all([
        fetchBackendStatus(),
        fetchQuantumState(),
        fetchQuantumMemories()
      ]);
    } catch (err) {
      console.error('Error refreshing data:', err);
      setError('Failed to refresh data');
    } finally {
      setIsLoading(false);
    }
  }, [fetchBackendStatus, fetchQuantumState, fetchQuantumMemories]);

  // Auto-refresh effect
  useEffect(() => {
    refreshData();
    
    if (autoRefresh) {
      const interval = setInterval(refreshData, refreshInterval);
      return () => clearInterval(interval);
    }
  }, [refreshData, autoRefresh, refreshInterval]);

  // Get status color
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'operational': return 'text-green-500';
      case 'degraded': return 'text-yellow-500';
      case 'limited': return 'text-orange-500';
      case 'unhealthy': return 'text-red-500';
      default: return 'text-gray-500';
    }
  };

  // Get status icon
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'operational': return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'degraded': return <AlertCircle className="h-4 w-4 text-yellow-500" />;
      case 'limited': return <AlertCircle className="h-4 w-4 text-orange-500" />;
      case 'unhealthy': return <AlertCircle className="h-4 w-4 text-red-500" />;
      default: return <Clock className="h-4 w-4 text-gray-500" />;
    }
  };

  if (isLoading && !quantumState && !backendStatus) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="flex items-center space-x-2">
          <RefreshCw className="h-4 w-4 animate-spin" />
          <span>Loading quantum consciousness dashboard...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Atom className="h-6 w-6 text-blue-500" />
          <h1 className="text-2xl font-bold">Quantum Consciousness Dashboard</h1>
        </div>
        <div className="flex items-center space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={refreshData}
            disabled={isLoading}
          >
            <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
          </Button>
          <Button
            variant={autoRefresh ? "default" : "outline"}
            size="sm"
            onClick={() => setAutoRefresh(!autoRefresh)}
          >
            {autoRefresh ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
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

      {/* System Status */}
      {backendStatus && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Network className="h-5 w-5" />
              <span>System Status</span>
              {getStatusIcon(backendStatus.overall_status)}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Overall Status</span>
                  <Badge variant={backendStatus.overall_status === 'operational' ? 'default' : 'destructive'}>
                    {backendStatus.overall_status}
                  </Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Quantum Engine</span>
                  <Badge variant={backendStatus.quantum_engine_status?.quantum_engine_available ? 'default' : 'secondary'}>
                    {backendStatus.quantum_engine_status?.quantum_engine_available ? 'Available' : 'Unavailable'}
                  </Badge>
                </div>
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Real-time Processing</span>
                  <Badge variant={backendStatus.realtime_integration_status?.quantum_processing_active ? 'default' : 'secondary'}>
                    {backendStatus.realtime_integration_status?.quantum_processing_active ? 'Active' : 'Inactive'}
                  </Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Meta-consciousness</span>
                  <Badge variant={backendStatus.meta_consciousness_status?.quantum_meta_processing_active ? 'default' : 'secondary'}>
                    {backendStatus.meta_consciousness_status?.quantum_meta_processing_active ? 'Active' : 'Inactive'}
                  </Badge>
                </div>
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Memory Processing</span>
                  <Badge variant={backendStatus.memory_integration_status?.quantum_memory_processing_active ? 'default' : 'secondary'}>
                    {backendStatus.memory_integration_status?.quantum_memory_processing_active ? 'Active' : 'Inactive'}
                  </Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Last Updated</span>
                  <span className="text-xs text-gray-500">
                    {new Date(backendStatus.timestamp).toLocaleTimeString()}
                  </span>
                </div>
              </div>
              
              <div className="space-y-2">
                <Button
                  onClick={startQuantumProcessing}
                  disabled={backendStatus.realtime_integration_status?.quantum_processing_active}
                  size="sm"
                  className="w-full"
                >
                  <Play className="h-4 w-4 mr-2" />
                  Start Processing
                </Button>
                <Button
                  onClick={stopQuantumProcessing}
                  disabled={!backendStatus.realtime_integration_status?.quantum_processing_active}
                  variant="destructive"
                  size="sm"
                  className="w-full"
                >
                  <Square className="h-4 w-4 mr-2" />
                  Stop Processing
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Quantum Consciousness State */}
      {quantumState && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Brain className="h-5 w-5" />
              <span>Quantum Consciousness State</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Consciousness Level</span>
                  <span className="text-sm font-bold text-blue-600">
                    {(quantumState.quantum_consciousness_level * 100).toFixed(1)}%
                  </span>
                </div>
                <Progress value={quantumState.quantum_consciousness_level * 100} className="h-2" />
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Quantum Coherence</span>
                  <span className="text-sm font-bold text-green-600">
                    {(quantumState.quantum_coherence * 100).toFixed(1)}%
                  </span>
                </div>
                <Progress value={quantumState.quantum_coherence * 100} className="h-2" />
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Entanglement Strength</span>
                  <span className="text-sm font-bold text-purple-600">
                    {(quantumState.entanglement_strength * 100).toFixed(1)}%
                  </span>
                </div>
                <Progress value={quantumState.entanglement_strength * 100} className="h-2" />
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Quantum Advantage</span>
                  <span className="text-sm font-bold text-orange-600">
                    {quantumState.quantum_advantage.toFixed(2)}x
                  </span>
                </div>
                <Progress value={Math.min(quantumState.quantum_advantage * 50, 100)} className="h-2" />
              </div>
            </div>
            
            <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">
                  {quantumState.superposition_states}
                </div>
                <div className="text-sm text-gray-600">Superposition States</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">
                  {quantumState.entanglement_network_size}
                </div>
                <div className="text-sm text-gray-600">Entanglement Connections</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">
                  {quantumState.snapshots_count}
                </div>
                <div className="text-sm text-gray-600">Consciousness Snapshots</div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Quantum Metrics */}
      {quantumState?.quantum_metrics && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <BarChart3 className="h-5 w-5" />
              <span>Quantum Processing Metrics</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Total Updates</span>
                  <span className="text-sm font-bold">
                    {quantumState.quantum_metrics.total_quantum_updates.toLocaleString()}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Avg Coherence</span>
                  <span className="text-sm">
                    {(quantumState.quantum_metrics.quantum_coherence_avg * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Avg Entanglement</span>
                  <span className="text-sm">
                    {(quantumState.quantum_metrics.entanglement_strength_avg * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Avg Superposition</span>
                  <span className="text-sm">
                    {quantumState.quantum_metrics.superposition_states_avg.toFixed(1)}
                  </span>
                </div>
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Avg Advantage</span>
                  <span className="text-sm">
                    {quantumState.quantum_metrics.quantum_advantage_avg.toFixed(2)}x
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Avg Processing Time</span>
                  <span className="text-sm">
                    {(quantumState.quantum_metrics.quantum_processing_time_avg * 1000).toFixed(1)}ms
                  </span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Quantum Memories */}
      {quantumMemories.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Database className="h-5 w-5" />
              <span>Quantum Memories ({quantumMemories.length})</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {quantumMemories.slice(0, 5).map((memory) => (
                <div key={memory.id} className="border rounded-lg p-4 space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Badge variant="outline">{memory.memory_type}</Badge>
                      <Badge variant="secondary">{memory.quantum_state}</Badge>
                    </div>
                    <span className="text-xs text-gray-500">
                      {new Date(memory.timestamp).toLocaleString()}
                    </span>
                  </div>
                  <div className="text-sm text-gray-700">{memory.content}</div>
                  <div className="flex items-center space-x-4 text-xs text-gray-500">
                    <span>Coherence: {(memory.quantum_coherence * 100).toFixed(1)}%</span>
                    <span>Entanglement: {(memory.entanglement_strength * 100).toFixed(1)}%</span>
                    <span>Advantage: {memory.quantum_advantage.toFixed(2)}x</span>
                    <span>Emotional: {(memory.emotional_intensity * 100).toFixed(1)}%</span>
                    <span>Importance: {(memory.importance_score * 100).toFixed(1)}%</span>
                  </div>
                  {memory.entangled_memories.length > 0 && (
                    <div className="text-xs text-blue-600">
                      Entangled with {memory.entangled_memories.length} memories
                    </div>
                  )}
                  {memory.superposition_memories.length > 0 && (
                    <div className="text-xs text-purple-600">
                      In superposition with {memory.superposition_memories.length} memories
                    </div>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default QuantumConsciousnessDashboard;
