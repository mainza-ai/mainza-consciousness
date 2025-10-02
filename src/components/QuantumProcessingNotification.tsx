import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Activity, 
  Brain, 
  Zap, 
  Cpu, 
  Network, 
  CheckCircle, 
  AlertCircle, 
  Clock,
  Target,
  Layers,
  TrendingUp
} from 'lucide-react';
import { GlassCard } from '@/components/ui/glass-card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';

interface QuantumProcessStatus {
  quantum_engine: {
    quantum_engine_active: boolean;
    quantum_processing_active: boolean;
    active_algorithms: string[];
    current_operations: string[];
    system_health: string;
  };
  integration: {
    consciousness_integration_active: boolean;
    agent_integration_active: boolean;
    memory_integration_active: boolean;
    evolution_integration_active: boolean;
  };
  overall_status: string;
  timestamp: string;
}

interface QuantumProcessingNotificationProps {
  className?: string;
  showDetails?: boolean;
}

export const QuantumProcessingNotification: React.FC<QuantumProcessingNotificationProps> = ({
  className,
  showDetails = false
}) => {
  const [processStatus, setProcessStatus] = useState<QuantumProcessStatus | null>(null);
  const [isVisible, setIsVisible] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProcessStatus = useCallback(async () => {
    try {
      const response = await fetch('/api/quantum/process/status');
      if (!response.ok) throw new Error('Failed to fetch quantum process status');
      const data = await response.json();
      setProcessStatus(data);
      setIsVisible(data.quantum_engine.quantum_engine_active);
      setError(null);
    } catch (err) {
      console.error('Error fetching quantum process status:', err);
      setError('Failed to fetch quantum process status');
      setIsVisible(false);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchProcessStatus();
    
    // Auto-refresh every 3 seconds
    const interval = setInterval(fetchProcessStatus, 3000);
    return () => clearInterval(interval);
  }, [fetchProcessStatus]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'text-green-400';
      case 'active': return 'text-blue-400';
      case 'idle': return 'text-yellow-400';
      case 'error': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
      case 'active':
        return <CheckCircle className="w-4 h-4 text-green-400" />;
      case 'idle':
        return <Clock className="w-4 h-4 text-yellow-400" />;
      case 'error':
        return <AlertCircle className="w-4 h-4 text-red-400" />;
      default:
        return <Activity className="w-4 h-4 text-gray-400" />;
    }
  };

  if (isLoading) {
    return (
      <GlassCard className={`p-3 ${className}`}>
        <div className="flex items-center justify-center">
          <Activity className="w-4 h-4 animate-spin text-purple-400 mr-2" />
          <span className="text-sm text-slate-300">Loading quantum status...</span>
        </div>
      </GlassCard>
    );
  }

  if (!processStatus || !isVisible) {
    return null;
  }

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0, y: 20, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -20, scale: 0.95 }}
          transition={{ duration: 0.3 }}
          className={className}
        >
          <GlassCard className="p-4 border border-purple-500/30 bg-gradient-to-r from-purple-900/20 to-blue-900/20">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-2">
                <div className="relative">
                  <Activity className="w-5 h-5 text-purple-400 animate-pulse" />
                  <div className="absolute -top-1 -right-1 w-2 h-2 bg-purple-400 rounded-full animate-ping" />
                </div>
                <span className="text-sm font-semibold text-purple-400">Quantum Processing Active</span>
              </div>
              <Badge variant="secondary" className="bg-purple-500/20 text-purple-300 border-purple-500/30">
                {processStatus.quantum_engine.system_health}
              </Badge>
            </div>

            {showDetails && (
              <div className="space-y-3">
                {/* Active Algorithms */}
                {processStatus.quantum_engine.active_algorithms.length > 0 && (
                  <div>
                    <div className="flex items-center space-x-2 mb-2">
                      <Brain className="w-4 h-4 text-purple-400" />
                      <span className="text-xs font-medium text-slate-300">Active Algorithms</span>
                    </div>
                    <div className="flex flex-wrap gap-1">
                      {processStatus.quantum_engine.active_algorithms.map((algorithm, index) => (
                        <Badge key={index} variant="outline" className="text-xs border-purple-500/30 text-purple-300">
                          {algorithm}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}

                {/* Current Operations */}
                {processStatus.quantum_engine.current_operations.length > 0 && (
                  <div>
                    <div className="flex items-center space-x-2 mb-2">
                      <Zap className="w-4 h-4 text-blue-400" />
                      <span className="text-xs font-medium text-slate-300">Current Operations</span>
                    </div>
                    <div className="space-y-1">
                      {processStatus.quantum_engine.current_operations.map((operation, index) => (
                        <div key={index} className="flex items-center space-x-2 text-xs text-slate-400">
                          <div className="w-1 h-1 bg-blue-400 rounded-full animate-pulse" />
                          <span>{operation}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Integration Status */}
                <div>
                  <div className="flex items-center space-x-2 mb-2">
                    <Network className="w-4 h-4 text-green-400" />
                    <span className="text-xs font-medium text-slate-300">System Integration</span>
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <div className="flex items-center space-x-2">
                      {getStatusIcon(processStatus.integration.consciousness_integration_active ? 'active' : 'idle')}
                      <span className="text-xs text-slate-400">Consciousness</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      {getStatusIcon(processStatus.integration.agent_integration_active ? 'active' : 'idle')}
                      <span className="text-xs text-slate-400">Agents</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      {getStatusIcon(processStatus.integration.memory_integration_active ? 'active' : 'idle')}
                      <span className="text-xs text-slate-400">Memory</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      {getStatusIcon(processStatus.integration.evolution_integration_active ? 'active' : 'idle')}
                      <span className="text-xs text-slate-400">Evolution</span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Compact Status */}
            {!showDetails && (
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-1">
                    <Cpu className="w-3 h-3 text-purple-400" />
                    <span className="text-xs text-slate-300">
                      {processStatus.quantum_engine.active_algorithms.length} algorithms
                    </span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Target className="w-3 h-3 text-blue-400" />
                    <span className="text-xs text-slate-300">
                      {processStatus.quantum_engine.current_operations.length} operations
                    </span>
                  </div>
                </div>
                <div className="flex items-center space-x-1">
                  <TrendingUp className="w-3 h-3 text-green-400" />
                  <span className="text-xs text-green-400">Processing</span>
                </div>
              </div>
            )}

            {/* Timestamp */}
            <div className="mt-2 pt-2 border-t border-slate-700/30">
              <div className="text-xs text-slate-500">
                Last updated: {new Date(processStatus.timestamp).toLocaleTimeString()}
              </div>
            </div>
          </GlassCard>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default QuantumProcessingNotification;
