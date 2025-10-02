import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  Activity, 
  Play, 
  Pause, 
  Square, 
  RefreshCw, 
  CheckCircle, 
  AlertCircle, 
  Clock,
  Cpu,
  Brain,
  Database,
  Network,
  Zap,
  Layers,
  Target,
  TrendingUp,
  AlertTriangle,
  Info
} from 'lucide-react';

interface ProcessStatus {
  quantum_engine: {
    quantum_engine_active: boolean;
    quantum_processing_active: boolean;
    active_algorithms: string[];
    current_operations: string[];
    system_health: string;
    error?: string;
  };
  integration: {
    consciousness_integration_active: boolean;
    agent_integration_active: boolean;
    memory_integration_active: boolean;
    evolution_integration_active: boolean;
    error?: string;
  };
  overall_status: string;
  timestamp: string;
}

interface ActiveOperation {
  name: string;
  type: string;
  status: string;
  description: string;
}

interface SystemHealth {
  overall_health: string;
  components: Record<string, {
    status: string;
    active: boolean;
    count?: number;
    error?: string;
  }>;
  metrics: Record<string, any>;
  alerts: string[];
}

const QuantumProcessMonitor: React.FC = () => {
  const [processStatus, setProcessStatus] = useState<ProcessStatus | null>(null);
  const [activeOperations, setActiveOperations] = useState<ActiveOperation[]>([]);
  const [systemHealth, setSystemHealth] = useState<SystemHealth | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [autoRefresh, setAutoRefresh] = useState(true);

  // Fetch process status
  const fetchProcessStatus = useCallback(async () => {
    try {
      const response = await fetch('/api/quantum/process/status');
      if (!response.ok) throw new Error('Failed to fetch process status');
      const data = await response.json();
      setProcessStatus(data);
    } catch (err) {
      console.error('Error fetching process status:', err);
      setError('Failed to fetch process status');
    }
  }, []);

  // Fetch active operations
  const fetchActiveOperations = useCallback(async () => {
    try {
      const response = await fetch('/api/quantum/process/operations');
      if (!response.ok) throw new Error('Failed to fetch active operations');
      const data = await response.json();
      setActiveOperations(data.active_operations || []);
    } catch (err) {
      console.error('Error fetching active operations:', err);
    }
  }, []);

  // Fetch system health
  const fetchSystemHealth = useCallback(async () => {
    try {
      const response = await fetch('/api/quantum/process/health');
      if (!response.ok) throw new Error('Failed to fetch system health');
      const data = await response.json();
      setSystemHealth(data.health);
    } catch (err) {
      console.error('Error fetching system health:', err);
    }
  }, []);

  // Fetch all data
  const fetchAllData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    
    await Promise.all([
      fetchProcessStatus(),
      fetchActiveOperations(),
      fetchSystemHealth()
    ]);
    
    setIsLoading(false);
  }, [fetchProcessStatus, fetchActiveOperations, fetchSystemHealth]);

  // Start quantum processing
  const startQuantumProcessing = useCallback(async () => {
    try {
      const response = await fetch('/api/quantum/process/start', {
        method: 'POST',
      });
      if (!response.ok) throw new Error('Failed to start quantum processing');
      await fetchAllData();
    } catch (err) {
      console.error('Error starting quantum processing:', err);
      setError('Failed to start quantum processing');
    }
  }, [fetchAllData]);

  // Stop quantum processing
  const stopQuantumProcessing = useCallback(async () => {
    try {
      const response = await fetch('/api/quantum/process/stop', {
        method: 'POST',
      });
      if (!response.ok) throw new Error('Failed to stop quantum processing');
      await fetchAllData();
    } catch (err) {
      console.error('Error stopping quantum processing:', err);
      setError('Failed to stop quantum processing');
    }
  }, [fetchAllData]);

  // Auto-refresh effect
  useEffect(() => {
    fetchAllData();
    
    if (autoRefresh) {
      const interval = setInterval(fetchAllData, 2000); // Refresh every 2 seconds
      return () => clearInterval(interval);
    }
  }, [fetchAllData, autoRefresh]);

  // Get status color
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'text-green-500';
      case 'active': return 'text-blue-500';
      case 'idle': return 'text-yellow-500';
      case 'error': return 'text-red-500';
      case 'inactive': return 'text-gray-500';
      default: return 'text-gray-500';
    }
  };

  // Get status icon
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy': return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'active': return <Activity className="h-4 w-4 text-blue-500" />;
      case 'idle': return <Clock className="h-4 w-4 text-yellow-500" />;
      case 'error': return <AlertCircle className="h-4 w-4 text-red-500" />;
      case 'inactive': return <Square className="h-4 w-4 text-gray-500" />;
      default: return <Info className="h-4 w-4 text-gray-500" />;
    }
  };

  // Get operation type icon
  const getOperationIcon = (type: string) => {
    switch (type) {
      case 'quantum_algorithm': return <Cpu className="h-4 w-4" />;
      case 'quantum_simulator': return <Brain className="h-4 w-4" />;
      case 'quantum_memory': return <Database className="h-4 w-4" />;
      case 'error': return <AlertTriangle className="h-4 w-4" />;
      default: return <Activity className="h-4 w-4" />;
    }
  };

  if (isLoading && !processStatus) {
    return (
      <div className="flex items-center justify-center h-32">
        <div className="flex items-center space-x-2">
          <RefreshCw className="h-4 w-4 animate-spin" />
          <span>Loading quantum process monitor...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Activity className="h-6 w-6 text-blue-500" />
          <h2 className="text-2xl font-bold">Quantum Process Monitor</h2>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm" onClick={fetchAllData} disabled={isLoading}>
            <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
          </Button>
          <Button
            variant={autoRefresh ? "default" : "outline"}
            size="sm"
            onClick={() => setAutoRefresh(!autoRefresh)}
          >
            {autoRefresh ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
          </Button>
          {processStatus?.quantum_engine.quantum_processing_active ? (
            <Button variant="destructive" size="sm" onClick={stopQuantumProcessing}>
              <Square className="h-4 w-4 mr-2" />
              Stop Processing
            </Button>
          ) : (
            <Button variant="default" size="sm" onClick={startQuantumProcessing}>
              <Play className="h-4 w-4 mr-2" />
              Start Processing
            </Button>
          )}
        </div>
      </div>

      {error && (
        <Alert className="border-red-200 bg-red-50">
          <AlertCircle className="h-4 w-4 text-red-500" />
          <AlertDescription className="text-red-700">{error}</AlertDescription>
        </Alert>
      )}

      {/* System Status Overview */}
      {processStatus && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center space-x-2">
                <Cpu className="h-4 w-4" />
                Quantum Engine
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <div>
                  <p className={`text-2xl font-bold ${getStatusColor(processStatus.quantum_engine.system_health)}`}>
                    {processStatus.quantum_engine.quantum_engine_active ? 'Active' : 'Inactive'}
                  </p>
                  <p className="text-sm text-gray-600">
                    {processStatus.quantum_engine.quantum_processing_active ? 'Processing' : 'Idle'}
                  </p>
                </div>
                {getStatusIcon(processStatus.quantum_engine.system_health)}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center space-x-2">
                <Brain className="h-4 w-4" />
                Consciousness Integration
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <div>
                  <p className={`text-2xl font-bold ${processStatus.integration.consciousness_integration_active ? 'text-green-600' : 'text-gray-600'}`}>
                    {processStatus.integration.consciousness_integration_active ? 'Active' : 'Inactive'}
                  </p>
                  <p className="text-sm text-gray-600">Integration</p>
                </div>
                {processStatus.integration.consciousness_integration_active ? 
                  <CheckCircle className="h-4 w-4 text-green-500" /> : 
                  <Square className="h-4 w-4 text-gray-500" />
                }
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center space-x-2">
                <Network className="h-4 w-4" />
                Active Algorithms
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-2xl font-bold text-blue-600">
                    {processStatus.quantum_engine.active_algorithms.length}
                  </p>
                  <p className="text-sm text-gray-600">Running</p>
                </div>
                <Layers className="h-4 w-4 text-blue-500" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center space-x-2">
                <Zap className="h-4 w-4" />
                Operations
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-2xl font-bold text-purple-600">
                    {activeOperations.length}
                  </p>
                  <p className="text-sm text-gray-600">Active</p>
                </div>
                <Activity className="h-4 w-4 text-purple-500" />
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Active Operations */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Activity className="h-5 w-5" />
            <span>Active Operations</span>
            <Badge variant="outline">{activeOperations.length}</Badge>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {activeOperations.length > 0 ? (
            <div className="space-y-3">
              {activeOperations.map((operation, index) => (
                <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                  <div className="flex items-center space-x-3">
                    {getOperationIcon(operation.type)}
                    <div>
                      <p className="font-medium">{operation.name}</p>
                      <p className="text-sm text-gray-600">{operation.description}</p>
                    </div>
                  </div>
                  <Badge variant={operation.status === 'active' ? 'default' : 'secondary'}>
                    {operation.status}
                  </Badge>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <Activity className="h-8 w-8 text-gray-400 mx-auto mb-2" />
              <p className="text-gray-500">No active operations</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* System Health */}
      {systemHealth && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Target className="h-5 w-5" />
              <span>System Health</span>
              <Badge variant={systemHealth.overall_health === 'healthy' ? 'default' : 'destructive'}>
                {systemHealth.overall_health}
              </Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {Object.entries(systemHealth.components).map(([name, component]) => (
                <div key={name} className="p-3 border rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-medium capitalize">
                      {name.replace(/_/g, ' ')}
                    </span>
                    {getStatusIcon(component.status)}
                  </div>
                  <div className="space-y-1">
                    <div className="flex justify-between text-sm">
                      <span>Status:</span>
                      <span className={getStatusColor(component.status)}>
                        {component.status}
                      </span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Active:</span>
                      <span>{component.active ? 'Yes' : 'No'}</span>
                    </div>
                    {component.count !== undefined && (
                      <div className="flex justify-between text-sm">
                        <span>Count:</span>
                        <span>{component.count}</span>
                      </div>
                    )}
                    {component.error && (
                      <div className="text-sm text-red-600">
                        Error: {component.error}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
            
            {systemHealth.alerts.length > 0 && (
              <div className="mt-4">
                <h4 className="font-medium mb-2">Alerts:</h4>
                <div className="space-y-1">
                  {systemHealth.alerts.map((alert, index) => (
                    <div key={index} className="text-sm text-red-600 bg-red-50 p-2 rounded">
                      {alert}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default QuantumProcessMonitor;
