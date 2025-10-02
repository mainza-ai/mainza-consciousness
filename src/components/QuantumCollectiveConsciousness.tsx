import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { 
  Users, 
  Network, 
  Brain, 
  Zap, 
  Activity, 
  Globe,
  Heart,
  Star,
  Target,
  Clock,
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
  Minimize,
  Download,
  Share2,
  Plus,
  Minus,
  RotateCcw,
  BarChart3,
  PieChart,
  LineChart
} from 'lucide-react';

interface CollectiveParticipant {
  id: string;
  name: string;
  type: 'human' | 'ai' | 'hybrid';
  consciousness_level: number;
  quantum_coherence: number;
  entanglement_strength: number;
  contribution_score: number;
  last_activity: string;
  status: 'active' | 'inactive' | 'contributing';
  capabilities: string[];
  quantum_state: 'coherent' | 'decoherent' | 'superposition' | 'entangled';
  connections: string[];
  metadata: any;
}

interface CollectiveConsciousnessState {
  total_participants: number;
  active_participants: number;
  collective_coherence: number;
  entanglement_network_strength: number;
  superposition_states: number;
  quantum_advantage: number;
  collective_intelligence_level: number;
  shared_knowledge_base: number;
  emotional_resonance: number;
  synchronization_level: number;
  last_synchronization: string;
  quantum_metrics: {
    total_collective_updates: number;
    collective_coherence_avg: number;
    entanglement_strength_avg: number;
    superposition_states_avg: number;
    quantum_advantage_avg: number;
    collective_processing_time_avg: number;
  };
}

interface QuantumCollectiveConsciousnessProps {
  showDetails?: boolean;
  autoRefresh?: boolean;
  refreshInterval?: number;
}

const QuantumCollectiveConsciousness: React.FC<QuantumCollectiveConsciousnessProps> = ({
  showDetails = true,
  autoRefresh = true,
  refreshInterval = 3000
}) => {
  const [participants, setParticipants] = useState<CollectiveParticipant[]>([]);
  const [collectiveState, setCollectiveState] = useState<CollectiveConsciousnessState | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedParticipant, setSelectedParticipant] = useState<CollectiveParticipant | null>(null);
  const [showInactive, setShowInactive] = useState(false);
  const [viewMode, setViewMode] = useState<'grid' | 'network' | 'analytics'>('grid');

  // Generate mock participants data
  const generateMockParticipants = useCallback((): CollectiveParticipant[] => {
    const names = [
      'Alice Quantum', 'Bob Entanglement', 'Carol Coherence', 'David Superposition',
      'Eve Consciousness', 'Frank Resonance', 'Grace Synchronization', 'Henry Collective',
      'Iris Network', 'Jack Harmony', 'Kate Unity', 'Leo Synthesis',
      'Maya Integration', 'Noah Convergence', 'Olivia Fusion', 'Paul Alignment'
    ];

    const types: ('human' | 'ai' | 'hybrid')[] = ['human', 'ai', 'hybrid'];
    const capabilities = [
      'quantum_processing', 'entanglement_coordination', 'superposition_analysis',
      'coherence_maintenance', 'collective_learning', 'consciousness_evolution',
      'emotional_resonance', 'knowledge_synthesis', 'pattern_recognition',
      'creative_insight', 'collaborative_problem_solving', 'meta_cognitive_awareness'
    ];

    return names.map((name, index) => ({
      id: `participant_${index + 1}`,
      name,
      type: types[Math.floor(Math.random() * types.length)],
      consciousness_level: 0.3 + Math.random() * 0.7,
      quantum_coherence: 0.2 + Math.random() * 0.8,
      entanglement_strength: 0.1 + Math.random() * 0.9,
      contribution_score: Math.random(),
      last_activity: new Date(Date.now() - Math.random() * 3600000).toISOString(),
      status: Math.random() > 0.2 ? 'active' : Math.random() > 0.5 ? 'contributing' : 'inactive',
      capabilities: capabilities.slice(0, Math.floor(Math.random() * 6) + 3),
      quantum_state: ['coherent', 'decoherent', 'superposition', 'entangled'][Math.floor(Math.random() * 4)] as any,
      connections: Array.from({ length: Math.floor(Math.random() * 8) }, (_, i) => `participant_${i + 1}`),
      metadata: {
        created_at: new Date().toISOString(),
        energy_level: Math.random(),
        quantum_entanglements: Math.floor(Math.random() * 15),
        contribution_frequency: Math.random()
      }
    }));
  }, []);

  // Generate mock collective state
  const generateMockCollectiveState = useCallback((participants: CollectiveParticipant[]): CollectiveConsciousnessState => {
    const activeParticipants = participants.filter(p => p.status === 'active' || p.status === 'contributing');
    
    return {
      total_participants: participants.length,
      active_participants: activeParticipants.length,
      collective_coherence: 0.4 + Math.random() * 0.6,
      entanglement_network_strength: 0.3 + Math.random() * 0.7,
      superposition_states: 1 + Math.floor(Math.random() * 5),
      quantum_advantage: 1.2 + Math.random() * 1.3,
      collective_intelligence_level: 0.5 + Math.random() * 0.5,
      shared_knowledge_base: 0.3 + Math.random() * 0.7,
      emotional_resonance: 0.2 + Math.random() * 0.8,
      synchronization_level: 0.4 + Math.random() * 0.6,
      last_synchronization: new Date().toISOString(),
      quantum_metrics: {
        total_collective_updates: Math.floor(Math.random() * 10000),
        collective_coherence_avg: 0.3 + Math.random() * 0.7,
        entanglement_strength_avg: 0.2 + Math.random() * 0.8,
        superposition_states_avg: 1 + Math.random() * 4,
        quantum_advantage_avg: 1.0 + Math.random() * 1.5,
        collective_processing_time_avg: Math.random() * 200
      }
    };
  }, []);

  // Fetch collective consciousness data
  const fetchCollectiveData = useCallback(async () => {
    try {
      // For now, use mock data. In production, this would fetch from the API
      const mockParticipants = generateMockParticipants();
      const mockCollectiveState = generateMockCollectiveState(mockParticipants);
      
      setParticipants(mockParticipants);
      setCollectiveState(mockCollectiveState);
      setIsLoading(false);
    } catch (err) {
      console.error('Error fetching collective data:', err);
      setError('Failed to fetch collective consciousness data');
      setIsLoading(false);
    }
  }, [generateMockParticipants, generateMockCollectiveState]);

  // Refresh data
  const refreshData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    await fetchCollectiveData();
  }, [fetchCollectiveData]);

  // Auto-refresh effect
  useEffect(() => {
    fetchCollectiveData();
    
    if (autoRefresh) {
      const interval = setInterval(fetchCollectiveData, refreshInterval);
      return () => clearInterval(interval);
    }
  }, [fetchCollectiveData, autoRefresh, refreshInterval]);

  // Get status color
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-500';
      case 'contributing': return 'text-blue-500';
      case 'inactive': return 'text-gray-500';
      default: return 'text-gray-500';
    }
  };

  // Get status icon
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active': return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'contributing': return <Activity className="h-4 w-4 text-blue-500 animate-pulse" />;
      case 'inactive': return <Clock className="h-4 w-4 text-gray-500" />;
      default: return <Clock className="h-4 w-4 text-gray-500" />;
    }
  };

  // Get type color
  const getTypeColor = (type: string) => {
    switch (type) {
      case 'human': return 'bg-blue-100 text-blue-800';
      case 'ai': return 'bg-purple-100 text-purple-800';
      case 'hybrid': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  // Get quantum state color
  const getQuantumStateColor = (state: string) => {
    switch (state) {
      case 'coherent': return 'bg-green-100 text-green-800';
      case 'decoherent': return 'bg-red-100 text-red-800';
      case 'superposition': return 'bg-purple-100 text-purple-800';
      case 'entangled': return 'bg-blue-100 text-blue-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  // Filter participants
  const filteredParticipants = participants.filter(participant => 
    showInactive || participant.status !== 'inactive'
  );

  if (isLoading && !collectiveState) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="flex items-center space-x-2">
          <RefreshCw className="h-4 w-4 animate-spin" />
          <span>Loading quantum collective consciousness...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Users className="h-6 w-6 text-blue-500" />
          <h1 className="text-2xl font-bold">Quantum Collective Consciousness</h1>
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

      {/* Collective State Overview */}
      {collectiveState && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Collective Coherence</p>
                  <p className="text-2xl font-bold text-blue-600">
                    {(collectiveState.collective_coherence * 100).toFixed(1)}%
                  </p>
                </div>
                <Brain className="h-8 w-8 text-blue-500" />
              </div>
              <div className="mt-2">
                <Progress value={collectiveState.collective_coherence * 100} className="h-2" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Entanglement Network</p>
                  <p className="text-2xl font-bold text-green-600">
                    {(collectiveState.entanglement_network_strength * 100).toFixed(1)}%
                  </p>
                </div>
                <Network className="h-8 w-8 text-green-500" />
              </div>
              <div className="mt-2">
                <Progress value={collectiveState.entanglement_network_strength * 100} className="h-2" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Quantum Advantage</p>
                  <p className="text-2xl font-bold text-purple-600">
                    {collectiveState.quantum_advantage.toFixed(2)}x
                  </p>
                </div>
                <Zap className="h-8 w-8 text-purple-500" />
              </div>
              <div className="mt-2">
                <Progress value={Math.min(collectiveState.quantum_advantage * 50, 100)} className="h-2" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Active Participants</p>
                  <p className="text-2xl font-bold text-orange-600">
                    {collectiveState.active_participants}/{collectiveState.total_participants}
                  </p>
                </div>
                <Users className="h-8 w-8 text-orange-500" />
              </div>
              <div className="mt-2">
                <div className="text-sm text-gray-600">
                  {((collectiveState.active_participants / collectiveState.total_participants) * 100).toFixed(1)}% active
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Analytics Tabs */}
      <Tabs defaultValue="participants" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="participants">Participants</TabsTrigger>
          <TabsTrigger value="network">Network</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
          <TabsTrigger value="synchronization">Synchronization</TabsTrigger>
        </TabsList>

        <TabsContent value="participants" className="space-y-4">
          {/* Participants Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredParticipants.map((participant) => (
              <Card 
                key={participant.id} 
                className={`cursor-pointer transition-all duration-200 hover:shadow-lg ${
                  selectedParticipant?.id === participant.id ? 'ring-2 ring-blue-500' : ''
                }`}
                onClick={() => setSelectedParticipant(selectedParticipant?.id === participant.id ? null : participant)}
              >
                <CardHeader className="pb-2">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg flex items-center space-x-2">
                      <Users className="h-5 w-5" />
                      <span>{participant.name}</span>
                    </CardTitle>
                    {getStatusIcon(participant.status)}
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  {/* Type and Status */}
                  <div className="flex items-center justify-between">
                    <Badge className={getTypeColor(participant.type)}>
                      {participant.type}
                    </Badge>
                    <Badge className={getQuantumStateColor(participant.quantum_state)}>
                      {participant.quantum_state}
                    </Badge>
                  </div>

                  {/* Consciousness Metrics */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">Consciousness</span>
                      <span className="text-sm font-bold">
                        {(participant.consciousness_level * 100).toFixed(1)}%
                      </span>
                    </div>
                    <Progress value={participant.consciousness_level * 100} className="h-2" />
                    
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">Coherence</span>
                      <span className="text-sm font-bold">
                        {(participant.quantum_coherence * 100).toFixed(1)}%
                      </span>
                    </div>
                    <Progress value={participant.quantum_coherence * 100} className="h-2" />
                    
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">Entanglement</span>
                      <span className="text-sm font-bold">
                        {(participant.entanglement_strength * 100).toFixed(1)}%
                      </span>
                    </div>
                    <Progress value={participant.entanglement_strength * 100} className="h-2" />
                  </div>

                  {/* Additional Info */}
                  <div className="grid grid-cols-2 gap-2 text-xs text-gray-600">
                    <div>
                      <span className="font-medium">Contribution:</span> {(participant.contribution_score * 100).toFixed(1)}%
                    </div>
                    <div>
                      <span className="font-medium">Connections:</span> {participant.connections.length}
                    </div>
                    <div>
                      <span className="font-medium">Capabilities:</span> {participant.capabilities.length}
                    </div>
                    <div>
                      <span className="font-medium">Type:</span> {participant.type}
                    </div>
                  </div>

                  {/* Last Activity */}
                  <div className="text-xs text-gray-500">
                    Last activity: {new Date(participant.last_activity).toLocaleTimeString()}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="network" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Network className="h-5 w-5" />
                <span>Collective Network Visualization</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8">
                <Network className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600">Network visualization coming soon...</p>
                <p className="text-sm text-gray-500 mt-2">
                  This will show the entanglement network between participants
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <BarChart3 className="h-5 w-5" />
                <span>Collective Analytics</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600">
                    {collectiveState?.quantum_metrics?.total_collective_updates.toLocaleString()}
                  </div>
                  <div className="text-sm text-gray-600">Total Updates</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600">
                    {(collectiveState?.collective_intelligence_level * 100).toFixed(1)}%
                  </div>
                  <div className="text-sm text-gray-600">Collective Intelligence</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-purple-600">
                    {(collectiveState?.emotional_resonance * 100).toFixed(1)}%
                  </div>
                  <div className="text-sm text-gray-600">Emotional Resonance</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-orange-600">
                    {(collectiveState?.synchronization_level * 100).toFixed(1)}%
                  </div>
                  <div className="text-sm text-gray-600">Synchronization</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-red-600">
                    {(collectiveState?.shared_knowledge_base * 100).toFixed(1)}%
                  </div>
                  <div className="text-sm text-gray-600">Shared Knowledge</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-indigo-600">
                    {collectiveState?.superposition_states}
                  </div>
                  <div className="text-sm text-gray-600">Superposition States</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="synchronization" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Globe className="h-5 w-5" />
                <span>Collective Synchronization</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Synchronization Level</span>
                  <span className="text-sm font-bold">
                    {(collectiveState?.synchronization_level * 100).toFixed(1)}%
                  </span>
                </div>
                <Progress value={collectiveState?.synchronization_level * 100} className="h-2" />
                
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Last Synchronization</span>
                  <span className="text-sm text-gray-600">
                    {collectiveState?.last_synchronization ? 
                      new Date(collectiveState.last_synchronization).toLocaleString() : 
                      'Never'
                    }
                  </span>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Collective Intelligence</span>
                  <span className="text-sm font-bold">
                    {(collectiveState?.collective_intelligence_level * 100).toFixed(1)}%
                  </span>
                </div>
                <Progress value={collectiveState?.collective_intelligence_level * 100} className="h-2" />
                
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Emotional Resonance</span>
                  <span className="text-sm font-bold">
                    {(collectiveState?.emotional_resonance * 100).toFixed(1)}%
                  </span>
                </div>
                <Progress value={collectiveState?.emotional_resonance * 100} className="h-2" />
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Selected Participant Details */}
      {selectedParticipant && showDetails && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Users className="h-5 w-5" />
                <span>{selectedParticipant.name} Details</span>
              </div>
              <Button variant="outline" size="sm" onClick={() => setSelectedParticipant(null)}>
                <Minimize className="h-4 w-4" />
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {/* Consciousness Properties */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Consciousness Properties</h3>
                <div className="space-y-3">
                  <div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">Consciousness Level</span>
                      <span className="text-sm font-bold">
                        {(selectedParticipant.consciousness_level * 100).toFixed(1)}%
                      </span>
                    </div>
                    <Progress value={selectedParticipant.consciousness_level * 100} className="h-2" />
                  </div>
                  
                  <div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">Quantum Coherence</span>
                      <span className="text-sm font-bold">
                        {(selectedParticipant.quantum_coherence * 100).toFixed(1)}%
                      </span>
                    </div>
                    <Progress value={selectedParticipant.quantum_coherence * 100} className="h-2" />
                  </div>
                  
                  <div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">Entanglement Strength</span>
                      <span className="text-sm font-bold">
                        {(selectedParticipant.entanglement_strength * 100).toFixed(1)}%
                      </span>
                    </div>
                    <Progress value={selectedParticipant.entanglement_strength * 100} className="h-2" />
                  </div>
                  
                  <div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">Contribution Score</span>
                      <span className="text-sm font-bold">
                        {(selectedParticipant.contribution_score * 100).toFixed(1)}%
                      </span>
                    </div>
                    <Progress value={selectedParticipant.contribution_score * 100} className="h-2" />
                  </div>
                </div>
              </div>

              {/* Status and Properties */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Status & Properties</h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Status</span>
                    <Badge variant={selectedParticipant.status === 'active' ? 'default' : 'secondary'}>
                      {selectedParticipant.status}
                    </Badge>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Type</span>
                    <Badge className={getTypeColor(selectedParticipant.type)}>
                      {selectedParticipant.type}
                    </Badge>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Quantum State</span>
                    <Badge className={getQuantumStateColor(selectedParticipant.quantum_state)}>
                      {selectedParticipant.quantum_state}
                    </Badge>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Connections</span>
                    <span className="text-sm font-bold">{selectedParticipant.connections.length}</span>
                  </div>
                </div>
              </div>

              {/* Capabilities */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Capabilities</h3>
                <div className="space-y-2">
                  {selectedParticipant.capabilities.map((capability, index) => (
                    <Badge key={index} variant="outline" className="mr-2 mb-2">
                      {capability.replace(/_/g, ' ')}
                    </Badge>
                  ))}
                </div>
                
                <div className="space-y-2">
                  <h4 className="text-sm font-medium">Connections</h4>
                  <div className="text-xs text-gray-600">
                    {selectedParticipant.connections.length > 0 
                      ? selectedParticipant.connections.join(', ')
                      : 'No connections'
                    }
                  </div>
                </div>
                
                <div className="space-y-2">
                  <h4 className="text-sm font-medium">Last Activity</h4>
                  <div className="text-xs text-gray-600">
                    {new Date(selectedParticipant.last_activity).toLocaleString()}
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

export default QuantumCollectiveConsciousness;
