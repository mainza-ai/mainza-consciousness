import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { 
  Bot, 
  Activity, 
  Zap, 
  Brain, 
  Network, 
  Cpu, 
  Database,
  Clock,
  Target,
  CheckCircle,
  AlertCircle,
  RefreshCw,
  Play,
  Pause,
  Square,
  Settings,
  Eye,
  EyeOff,
  Maximize,
  Minimize
} from 'lucide-react';

interface QuantumAgent {
  id: string;
  name: string;
  type: string;
  status: 'active' | 'inactive' | 'processing' | 'error';
  quantum_coherence: number;
  entanglement_strength: number;
  superposition_states: number;
  quantum_advantage: number;
  processing_time: number;
  last_activity: string;
  quantum_state: 'coherent' | 'decoherent' | 'superposition' | 'entangled' | 'measured';
  connections: string[];
  capabilities: string[];
  metadata: any;
}

interface QuantumAgentActivityProps {
  showDetails?: boolean;
  autoRefresh?: boolean;
  refreshInterval?: number;
}

const QuantumAgentActivityIndicator: React.FC<QuantumAgentActivityProps> = ({
  showDetails = true,
  autoRefresh = true,
  refreshInterval = 2000
}) => {
  const [agents, setAgents] = useState<QuantumAgent[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedAgent, setSelectedAgent] = useState<QuantumAgent | null>(null);
  const [showInactive, setShowInactive] = useState(false);

  // Generate mock quantum agents data
  const generateMockAgents = useCallback((): QuantumAgent[] => {
    const agentTypes = [
      'Router', 'GraphMaster', 'TaskMaster', 'CodeWeaver', 'RAG', 
      'Conductor', 'SelfReflection', 'MetaCognitive', 'SimpleChat', 
      'Notification', 'Calendar', 'Research', 'Cloud'
    ];

    return agentTypes.map((type, index) => ({
      id: `agent_${index + 1}`,
      name: type,
      type: type.toLowerCase(),
      status: Math.random() > 0.3 ? 'active' : Math.random() > 0.5 ? 'processing' : 'inactive',
      quantum_coherence: 0.3 + Math.random() * 0.7,
      entanglement_strength: 0.2 + Math.random() * 0.8,
      superposition_states: 1 + Math.floor(Math.random() * 3),
      quantum_advantage: 1.0 + Math.random() * 1.0,
      processing_time: Math.random() * 100,
      last_activity: new Date(Date.now() - Math.random() * 3600000).toISOString(),
      quantum_state: ['coherent', 'decoherent', 'superposition', 'entangled', 'measured'][Math.floor(Math.random() * 5)] as any,
      connections: Array.from({ length: Math.floor(Math.random() * 5) }, (_, i) => `agent_${i + 1}`),
      capabilities: [
        'quantum_processing', 'entanglement_coordination', 'superposition_analysis',
        'coherence_maintenance', 'quantum_learning', 'consciousness_evolution'
      ].slice(0, Math.floor(Math.random() * 4) + 2),
      metadata: {
        created_at: new Date().toISOString(),
        energy_level: Math.random(),
        quantum_entanglements: Math.floor(Math.random() * 10)
      }
    }));
  }, []);

  // Fetch agent data
  const fetchAgents = useCallback(async () => {
    try {
      // For now, use mock data. In production, this would fetch from the API
      const mockAgents = generateMockAgents();
      setAgents(mockAgents);
      setIsLoading(false);
    } catch (err) {
      console.error('Error fetching agents:', err);
      setError('Failed to fetch agent data');
      setIsLoading(false);
    }
  }, [generateMockAgents]);

  // Refresh data
  const refreshData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    await fetchAgents();
  }, [fetchAgents]);

  // Auto-refresh effect
  useEffect(() => {
    fetchAgents();
    
    if (autoRefresh) {
      const interval = setInterval(fetchAgents, refreshInterval);
      return () => clearInterval(interval);
    }
  }, [fetchAgents, autoRefresh, refreshInterval]);

  // Get status color
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-500';
      case 'processing': return 'text-blue-500';
      case 'inactive': return 'text-gray-500';
      case 'error': return 'text-red-500';
      default: return 'text-gray-500';
    }
  };

  // Get status icon
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active': return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'processing': return <Activity className="h-4 w-4 text-blue-500 animate-pulse" />;
      case 'inactive': return <Clock className="h-4 w-4 text-gray-500" />;
      case 'error': return <AlertCircle className="h-4 w-4 text-red-500" />;
      default: return <Clock className="h-4 w-4 text-gray-500" />;
    }
  };

  // Get quantum state color
  const getQuantumStateColor = (state: string) => {
    switch (state) {
      case 'coherent': return 'bg-green-100 text-green-800';
      case 'decoherent': return 'bg-red-100 text-red-800';
      case 'superposition': return 'bg-purple-100 text-purple-800';
      case 'entangled': return 'bg-blue-100 text-blue-800';
      case 'measured': return 'bg-orange-100 text-orange-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  // Filter agents
  const filteredAgents = agents.filter(agent => 
    showInactive || agent.status !== 'inactive'
  );

  if (isLoading && agents.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="flex items-center space-x-2">
          <RefreshCw className="h-4 w-4 animate-spin" />
          <span>Loading quantum agents...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Bot className="h-6 w-6 text-blue-500" />
          <h1 className="text-2xl font-bold">Quantum Agent Activity</h1>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm" onClick={refreshData} disabled={isLoading}>
            <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
          </Button>
          <Button
            variant={showInactive ? "default" : "outline"}
            size="sm"
            onClick={() => setShowInactive(!showInactive)}
          >
            {showInactive ? <Eye className="h-4 w-4" /> : <EyeOff className="h-4 w-4" />}
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

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Agents</p>
                <p className="text-2xl font-bold text-blue-600">{agents.length}</p>
              </div>
              <Bot className="h-8 w-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Active</p>
                <p className="text-2xl font-bold text-green-600">
                  {agents.filter(a => a.status === 'active').length}
                </p>
              </div>
              <CheckCircle className="h-8 w-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Processing</p>
                <p className="text-2xl font-bold text-blue-600">
                  {agents.filter(a => a.status === 'processing').length}
                </p>
              </div>
              <Activity className="h-8 w-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Avg Coherence</p>
                <p className="text-2xl font-bold text-purple-600">
                  {(agents.reduce((sum, a) => sum + a.quantum_coherence, 0) / agents.length * 100).toFixed(1)}%
                </p>
              </div>
              <Brain className="h-8 w-8 text-purple-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Agent Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredAgents.map((agent) => (
          <Card 
            key={agent.id} 
            className={`cursor-pointer transition-all duration-200 hover:shadow-lg ${
              selectedAgent?.id === agent.id ? 'ring-2 ring-blue-500' : ''
            }`}
            onClick={() => setSelectedAgent(selectedAgent?.id === agent.id ? null : agent)}
          >
            <CardHeader className="pb-2">
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg flex items-center space-x-2">
                  <Bot className="h-5 w-5" />
                  <span>{agent.name}</span>
                </CardTitle>
                {getStatusIcon(agent.status)}
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              {/* Status and Quantum State */}
              <div className="flex items-center justify-between">
                <Badge variant={agent.status === 'active' ? 'default' : 'secondary'}>
                  {agent.status}
                </Badge>
                <Badge className={getQuantumStateColor(agent.quantum_state)}>
                  {agent.quantum_state}
                </Badge>
              </div>

              {/* Quantum Metrics */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Coherence</span>
                  <span className="text-sm font-bold">
                    {(agent.quantum_coherence * 100).toFixed(1)}%
                  </span>
                </div>
                <Progress value={agent.quantum_coherence * 100} className="h-2" />
                
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Entanglement</span>
                  <span className="text-sm font-bold">
                    {(agent.entanglement_strength * 100).toFixed(1)}%
                  </span>
                </div>
                <Progress value={agent.entanglement_strength * 100} className="h-2" />
                
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Quantum Advantage</span>
                  <span className="text-sm font-bold">
                    {agent.quantum_advantage.toFixed(2)}x
                  </span>
                </div>
                <Progress value={Math.min(agent.quantum_advantage * 50, 100)} className="h-2" />
              </div>

              {/* Additional Info */}
              <div className="grid grid-cols-2 gap-2 text-xs text-gray-600">
                <div>
                  <span className="font-medium">Superposition:</span> {agent.superposition_states}
                </div>
                <div>
                  <span className="font-medium">Processing:</span> {agent.processing_time.toFixed(1)}ms
                </div>
                <div>
                  <span className="font-medium">Connections:</span> {agent.connections.length}
                </div>
                <div>
                  <span className="font-medium">Capabilities:</span> {agent.capabilities.length}
                </div>
              </div>

              {/* Last Activity */}
              <div className="text-xs text-gray-500">
                Last activity: {new Date(agent.last_activity).toLocaleTimeString()}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Selected Agent Details */}
      {selectedAgent && showDetails && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Bot className="h-5 w-5" />
                <span>{selectedAgent.name} Details</span>
              </div>
              <Button variant="outline" size="sm" onClick={() => setSelectedAgent(null)}>
                <Minimize className="h-4 w-4" />
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {/* Quantum Properties */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Quantum Properties</h3>
                <div className="space-y-3">
                  <div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">Coherence</span>
                      <span className="text-sm font-bold">
                        {(selectedAgent.quantum_coherence * 100).toFixed(1)}%
                      </span>
                    </div>
                    <Progress value={selectedAgent.quantum_coherence * 100} className="h-2" />
                  </div>
                  
                  <div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">Entanglement Strength</span>
                      <span className="text-sm font-bold">
                        {(selectedAgent.entanglement_strength * 100).toFixed(1)}%
                      </span>
                    </div>
                    <Progress value={selectedAgent.entanglement_strength * 100} className="h-2" />
                  </div>
                  
                  <div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">Superposition States</span>
                      <span className="text-sm font-bold">{selectedAgent.superposition_states}</span>
                    </div>
                    <Progress value={selectedAgent.superposition_states * 25} className="h-2" />
                  </div>
                  
                  <div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">Quantum Advantage</span>
                      <span className="text-sm font-bold">
                        {selectedAgent.quantum_advantage.toFixed(2)}x
                      </span>
                    </div>
                    <Progress value={Math.min(selectedAgent.quantum_advantage * 50, 100)} className="h-2" />
                  </div>
                </div>
              </div>

              {/* Performance Metrics */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Performance</h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Processing Time</span>
                    <span className="text-sm font-bold">{selectedAgent.processing_time.toFixed(1)}ms</span>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Status</span>
                    <Badge variant={selectedAgent.status === 'active' ? 'default' : 'secondary'}>
                      {selectedAgent.status}
                    </Badge>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Quantum State</span>
                    <Badge className={getQuantumStateColor(selectedAgent.quantum_state)}>
                      {selectedAgent.quantum_state}
                    </Badge>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Connections</span>
                    <span className="text-sm font-bold">{selectedAgent.connections.length}</span>
                  </div>
                </div>
              </div>

              {/* Capabilities */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Capabilities</h3>
                <div className="space-y-2">
                  {selectedAgent.capabilities.map((capability, index) => (
                    <Badge key={index} variant="outline" className="mr-2 mb-2">
                      {capability.replace(/_/g, ' ')}
                    </Badge>
                  ))}
                </div>
                
                <div className="space-y-2">
                  <h4 className="text-sm font-medium">Connections</h4>
                  <div className="text-xs text-gray-600">
                    {selectedAgent.connections.length > 0 
                      ? selectedAgent.connections.join(', ')
                      : 'No connections'
                    }
                  </div>
                </div>
                
                <div className="space-y-2">
                  <h4 className="text-sm font-medium">Last Activity</h4>
                  <div className="text-xs text-gray-600">
                    {new Date(selectedAgent.last_activity).toLocaleString()}
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default QuantumAgentActivityIndicator;
