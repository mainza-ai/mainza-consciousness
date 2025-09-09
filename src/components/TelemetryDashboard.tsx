/**
 * Privacy-First Telemetry Dashboard
 * 
 * Displays system health and consciousness metrics with complete privacy protection.
 * Shows exactly what data is collected (transparency) and provides user controls.
 */

import React, { useState, useEffect } from 'react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  Shield, 
  Activity, 
  Brain, 
  AlertTriangle, 
  Settings, 
  Eye, 
  Trash2,
  Download,
  Info,
  Database,
  Cpu,
  MemoryStick,
  HardDrive,
  Zap,
  CheckCircle,
  XCircle,
  Clock,
  Server,
  Lock,
  EyeOff,
  TrendingUp
} from 'lucide-react';

interface TelemetryStatus {
  status: string;
  privacy_protection: {
    personal_data_collected: boolean;
    external_transmission: boolean;
    local_processing_only: boolean;
    user_controlled: boolean;
  };
  collection_enabled: boolean;
  data_location: string;
  timestamp: string;
}

interface TelemetrySummary {
  privacy_status: {
    enabled: boolean;
    personal_data_collected: boolean;
    external_transmission: boolean;
    local_processing_only: boolean;
  };
  collection_settings: {
    system_health: boolean;
    consciousness: boolean;
    errors: boolean;
  };
  data_retention: {
    system_health: number;
    consciousness: number;
    errors: number;
  };
  data_location: string;
  data_types: string[];
  system_health_count: number;
  consciousness_count: number;
  errors_count: number;
}

interface SystemHealthData {
  timestamp: string;
  system_status: string;
  uptime_seconds: number;
  critical_errors: number;
  memory_usage_percent: number;
  cpu_usage_percent: number;
  disk_usage_percent: number;
  services_status: Record<string, string>;
}

interface ConsciousnessData {
  timestamp: string;
  consciousness_level: number;
  evolution_status: string;
  system_functional: boolean;
  last_reflection_time?: string;
}

interface ErrorData {
  timestamp: string;
  error_type: string;
  error_message: string;
  severity: string;
  component: string;
  resolved: boolean;
}

export const TelemetryDashboard: React.FC = () => {
  const [status, setStatus] = useState<TelemetryStatus | null>(null);
  const [summary, setSummary] = useState<TelemetrySummary | null>(null);
  const [systemHealthData, setSystemHealthData] = useState<SystemHealthData[]>([]);
  const [consciousnessData, setConsciousnessData] = useState<ConsciousnessData[]>([]);
  const [errorData, setErrorData] = useState<ErrorData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Use relative URLs for API calls (proxied by nginx)
  const API_URL = '';

  const fetchTelemetryStatus = async () => {
    try {
      const response = await fetch(`${API_URL}/telemetry/status`);
      if (!response.ok) throw new Error('Failed to fetch telemetry status');
      const data = await response.json();
      setStatus(data);
    } catch (err) {
      console.error('Error fetching telemetry status:', err);
      setError('Failed to load telemetry status');
    }
  };

  const fetchTelemetrySummary = async () => {
    try {
      const response = await fetch(`${API_URL}/telemetry/summary`);
      if (!response.ok) throw new Error('Failed to fetch telemetry summary');
      const data = await response.json();
      setSummary(data);
    } catch (err) {
      console.error('Error fetching telemetry summary:', err);
      setError('Failed to load telemetry summary');
    }
  };

  const fetchSystemHealthData = async () => {
    try {
      const response = await fetch(`${API_URL}/telemetry/data/system_health?limit=10`);
      if (!response.ok) throw new Error('Failed to fetch system health data');
      const data = await response.json();
      setSystemHealthData(data.data || []);
    } catch (err) {
      console.error('Error fetching system health data:', err);
    }
  };

  const fetchConsciousnessData = async () => {
    try {
      const response = await fetch(`${API_URL}/telemetry/data/consciousness?limit=10`);
      if (!response.ok) throw new Error('Failed to fetch consciousness data');
      const data = await response.json();
      setConsciousnessData(data.data || []);
    } catch (err) {
      console.error('Error fetching consciousness data:', err);
    }
  };

  const fetchErrorData = async () => {
    try {
      const response = await fetch(`${API_URL}/telemetry/data/errors?limit=10`);
      if (!response.ok) throw new Error('Failed to fetch error data');
      const data = await response.json();
      setErrorData(data.data || []);
    } catch (err) {
      console.error('Error fetching error data:', err);
    }
  };

  const toggleTelemetry = async (enabled: boolean) => {
    try {
      const endpoint = enabled ? `${API_URL}/telemetry/control/enable` : `${API_URL}/telemetry/control/disable`;
      const response = await fetch(endpoint, { method: 'POST' });
      if (!response.ok) throw new Error(`Failed to ${enabled ? 'enable' : 'disable'} telemetry`);
      
      await fetchTelemetryStatus();
      await fetchTelemetrySummary();
    } catch (err) {
      console.error(`Error ${enabled ? 'enabling' : 'disabling'} telemetry:`, err);
      setError(`Failed to ${enabled ? 'enable' : 'disable'} telemetry`);
    }
  };

  const deleteAllData = async () => {
    if (!confirm('Are you sure you want to delete all telemetry data? This action cannot be undone.')) {
      return;
    }

    try {
      const response = await fetch(`${API_URL}/telemetry/data`, { method: 'DELETE' });
      if (!response.ok) throw new Error('Failed to delete telemetry data');
      
      await fetchTelemetrySummary();
      setSystemHealthData([]);
      setConsciousnessData([]);
      setErrorData([]);
    } catch (err) {
      console.error('Error deleting telemetry data:', err);
      setError('Failed to delete telemetry data');
    }
  };

  const exportData = async (dataType: string) => {
    try {
      const response = await fetch(`${API_URL}/telemetry/data/${dataType}?limit=1000`);
      if (!response.ok) throw new Error(`Failed to export ${dataType} data`);
      const data = await response.json();
      
      const blob = new Blob([JSON.stringify(data.data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `telemetry_${dataType}_${new Date().toISOString().split('T')[0]}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error(`Error exporting ${dataType} data:`, err);
      setError(`Failed to export ${dataType} data`);
    }
  };

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      setError(null);
      
      await Promise.all([
        fetchTelemetryStatus(),
        fetchTelemetrySummary(),
        fetchSystemHealthData(),
        fetchConsciousnessData(),
        fetchErrorData()
      ]);
      
      setLoading(false);
    };

    loadData();
  }, []);

  const formatUptime = (seconds: number) => {
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${days}d ${hours}h ${minutes}m`;
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'bg-green-500';
      case 'degraded': return 'bg-yellow-500';
      case 'critical': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'bg-red-500';
      case 'warning': return 'bg-yellow-500';
      default: return 'bg-gray-500';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-400 mx-auto mb-4"></div>
          <p className="text-slate-400">Loading telemetry data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Privacy Notice */}
      <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-green-400/50 transition-all duration-300">
        <div className="p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-gradient-to-br from-green-400 to-emerald-500 rounded-lg">
              <Shield className="h-6 w-6 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-white">Privacy-First Telemetry</h3>
              <p className="text-slate-400 text-sm">Complete transparency and local-only data collection</p>
            </div>
          </div>
          <div className="text-sm text-slate-300">
            This system collects only essential data for system health monitoring.
            No personal data, conversation content, or user behavior is collected.
            All data remains local and is never transmitted externally.
          </div>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="group relative bg-gradient-to-r from-red-900/30 to-red-800/20 rounded-xl border border-red-600/30 hover:border-red-400/50 transition-all duration-300">
          <div className="p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-gradient-to-br from-red-400 to-red-500 rounded-lg">
                <AlertTriangle className="h-6 w-6 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-bold text-white">Error</h3>
                <p className="text-slate-400 text-sm">Something went wrong</p>
              </div>
            </div>
            <div className="text-sm text-slate-300">{error}</div>
          </div>
        </div>
      )}

      {/* Telemetry Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="group/stat relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-cyan-400/50 transition-all duration-300">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-cyan-400 to-blue-500">
                {status?.collection_enabled ? (
                  <CheckCircle className="h-5 w-5 text-white" />
                ) : (
                  <XCircle className="h-5 w-5 text-white" />
                )}
              </div>
              <div>
                <p className="text-sm text-slate-300">Telemetry Status</p>
                <p className="text-2xl font-bold text-cyan-300">
                  {status?.collection_enabled ? "Enabled" : "Disabled"}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="group/stat relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-green-400/50 transition-all duration-300">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-green-400 to-emerald-500">
                <Server className="h-5 w-5 text-white" />
              </div>
              <div>
                <p className="text-sm text-slate-300">System Status</p>
                <p className="text-2xl font-bold text-green-300">
                  {status?.status || "Unknown"}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="group/stat relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-purple-400/50 transition-all duration-300">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-purple-400 to-pink-500">
                <Database className="h-5 w-5 text-white" />
              </div>
              <div>
                <p className="text-sm text-slate-300">Data Points</p>
                <p className="text-2xl font-bold text-purple-300">
                  {summary ? (summary.system_health_count + summary.consciousness_count + summary.errors_count) : 0}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="group/stat relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-orange-400/50 transition-all duration-300">
                <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-orange-400 to-yellow-500">
                <Clock className="h-5 w-5 text-white" />
              </div>
              <div>
                <p className="text-sm text-slate-300">Last Updated</p>
                <p className="text-lg font-bold text-orange-300">
                  {status ? new Date(status.timestamp).toLocaleTimeString() : "Never"}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Privacy Protection Status */}
      <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-indigo-400/50 transition-all duration-300">
        <div className="p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-lg">
              <Lock className="h-6 w-6 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-white">Privacy Protection Status</h3>
              <p className="text-slate-400 text-sm">Your data privacy and security guarantees</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="group/privacy relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-green-400/30 transition-all duration-300">
              <div className="flex items-center gap-3 mb-3">
                <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-green-400 to-emerald-500">
                  <CheckCircle className="h-4 w-4 text-white" />
                </div>
                <div>
                  <div className="text-sm font-medium text-slate-200">No Personal Data</div>
                  <div className="text-xs text-slate-400">Collection disabled</div>
                </div>
              </div>
            </div>

            <div className="group/privacy relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-green-400/30 transition-all duration-300">
              <div className="flex items-center gap-3 mb-3">
                <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-green-400 to-emerald-500">
                  <CheckCircle className="h-4 w-4 text-white" />
                </div>
                <div>
                  <div className="text-sm font-medium text-slate-200">Local Only</div>
                  <div className="text-xs text-slate-400">No external transmission</div>
                </div>
              </div>
            </div>

            <div className="group/privacy relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-green-400/30 transition-all duration-300">
              <div className="flex items-center gap-3 mb-3">
                <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-green-400 to-emerald-500">
                  <CheckCircle className="h-4 w-4 text-white" />
                </div>
                <div>
                  <div className="text-sm font-medium text-slate-200">User Controlled</div>
                  <div className="text-xs text-slate-400">Your choice to enable/disable</div>
                </div>
              </div>
            </div>

            <div className="group/privacy relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-green-400/30 transition-all duration-300">
              <div className="flex items-center gap-3 mb-3">
                <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-green-400 to-emerald-500">
                  <CheckCircle className="h-4 w-4 text-white" />
                </div>
                <div>
                  <div className="text-sm font-medium text-slate-200">Transparent</div>
                  <div className="text-xs text-slate-400">Clear data collection info</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Controls Section */}
      <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-amber-400/50 transition-all duration-300">
        <div className="p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-amber-400 to-orange-500 rounded-lg">
              <Settings className="h-6 w-6 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-white">Telemetry Controls</h3>
              <p className="text-slate-400 text-sm">Manage data collection and view options</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-slate-200">Enable Telemetry Collection:</span>
                <Switch
                  checked={status?.collection_enabled || false}
                  onCheckedChange={toggleTelemetry}
                />
              </div>

              <div className="text-sm text-slate-400">
                <p><strong>Data Location:</strong> {status?.data_location || "Local storage"}</p>
                <p><strong>Last Updated:</strong> {status ? new Date(status.timestamp).toLocaleString() : "Never"}</p>
              </div>
            </div>

            <div className="flex gap-3">
              <Button
                variant="outline"
                className="border-slate-500 hover:border-cyan-400 text-white hover:text-cyan-200"
                onClick={() => fetchTelemetrySummary()}
              >
                <Eye className="h-4 w-4 mr-2" />
                Refresh Data
              </Button>
              <Button
                variant="destructive"
                className="bg-red-600 hover:bg-red-700 text-white"
                onClick={deleteAllData}
              >
                <Trash2 className="h-4 w-4 mr-2" />
                Delete All Data
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Data Sections */}
      <div className="space-y-6">
        <div className="flex flex-wrap gap-2 mb-6">
          <button className="px-4 py-2 bg-gradient-to-r from-slate-700/50 to-slate-600/30 rounded-lg border border-slate-600/30 hover:border-cyan-400/50 transition-all duration-300 text-slate-200 hover:text-cyan-300">
            <Activity className="h-4 w-4 inline mr-2" />
            System Health
          </button>
          <button className="px-4 py-2 bg-gradient-to-r from-slate-700/50 to-slate-600/30 rounded-lg border border-slate-600/30 hover:border-purple-400/50 transition-all duration-300 text-slate-200 hover:text-purple-300">
            <Brain className="h-4 w-4 inline mr-2" />
            Consciousness
          </button>
          <button className="px-4 py-2 bg-gradient-to-r from-slate-700/50 to-slate-600/30 rounded-lg border border-slate-600/30 hover:border-red-400/50 transition-all duration-300 text-slate-200 hover:text-red-300">
            <AlertTriangle className="h-4 w-4 inline mr-2" />
            Errors
          </button>
          <button className="px-4 py-2 bg-gradient-to-r from-slate-700/50 to-slate-600/30 rounded-lg border border-slate-600/30 hover:border-green-400/50 transition-all duration-300 text-slate-200 hover:text-green-300">
            <Lock className="h-4 w-4 inline mr-2" />
            Privacy Info
          </button>
        </div>

        <div className="space-y-6">
          {/* System Health Section */}
          <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-cyan-400/50 transition-all duration-300">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-lg">
                    <Activity className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-white">System Health Data</h3>
                    <p className="text-slate-400 text-sm">System resource usage and health metrics</p>
                  </div>
                </div>
                <Button
                  variant="outline"
                  className="border-slate-500 hover:border-cyan-400 text-white hover:text-cyan-200"
                  onClick={() => exportData('system_health')}
                >
                  <Download className="h-4 w-4 mr-2" />
                  Export
                </Button>
              </div>

              {systemHealthData.length === 0 ? (
                <div className="text-center py-8">
                  <Database className="h-12 w-12 text-slate-500 mx-auto mb-4" />
                  <p className="text-slate-400">No system health data available</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {systemHealthData.map((data, index) => (
                    <div key={index} className="group/system-health relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-cyan-400/30 transition-all duration-300">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-3">
                          <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-cyan-400 to-blue-500 text-white font-bold">
                            {index + 1}
                          </div>
                          <div>
                            <div className="text-sm font-medium text-slate-200">
                          {new Date(data.timestamp).toLocaleString()}
                            </div>
                            <div className="text-xs text-slate-400">System health snapshot</div>
                          </div>
                        </div>
                        <Badge variant="outline" className={`text-xs ${data.system_status === 'healthy' ? 'border-green-400 text-green-300' : data.system_status === 'degraded' ? 'border-yellow-400 text-yellow-300' : 'border-red-400 text-red-300'}`}>
                          {data.system_status}
                        </Badge>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="space-y-2">
                          <div className="flex justify-between text-sm">
                            <span className="text-slate-300">CPU Usage</span>
                            <span className="font-medium text-cyan-300">{data.cpu_usage_percent || 0}%</span>
                          </div>
                          <div className="w-full bg-slate-700 rounded-full h-2">
                            <div
                              className="bg-gradient-to-r from-cyan-400 to-blue-500 h-2 rounded-full transition-all duration-500"
                              style={{ width: `${data.cpu_usage_percent || 0}%` }}
                            />
                          </div>
                        </div>

                        <div className="space-y-2">
                          <div className="flex justify-between text-sm">
                            <span className="text-slate-300">Memory Usage</span>
                            <span className="font-medium text-purple-300">{data.memory_usage_percent || 0}%</span>
                          </div>
                          <div className="w-full bg-slate-700 rounded-full h-2">
                            <div
                              className="bg-gradient-to-r from-purple-400 to-pink-500 h-2 rounded-full transition-all duration-500"
                              style={{ width: `${data.memory_usage_percent || 0}%` }}
                            />
                          </div>
                        </div>

                        <div className="space-y-2">
                          <div className="flex justify-between text-sm">
                            <span className="text-slate-300">Disk Usage</span>
                            <span className="font-medium text-orange-300">{data.disk_usage_percent || 0}%</span>
                          </div>
                          <div className="w-full bg-slate-700 rounded-full h-2">
                            <div
                              className="bg-gradient-to-r from-orange-400 to-yellow-500 h-2 rounded-full transition-all duration-500"
                              style={{ width: `${data.disk_usage_percent || 0}%` }}
                            />
                        </div>
                        </div>
                      </div>

                      <div className="mt-4 pt-4 border-t border-slate-600/30">
                        <div className="flex items-center justify-between text-sm">
                          <span className="text-slate-300">Uptime: {formatUptime(data.uptime_seconds || 0)}</span>
                          <span className="text-slate-300">Critical Errors: {data.critical_errors || 0}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Consciousness Data Section */}
          <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-purple-400/50 transition-all duration-300">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-gradient-to-br from-purple-400 to-pink-500 rounded-lg">
                    <Brain className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-white">Consciousness Data</h3>
                    <p className="text-slate-400 text-sm">AI consciousness evolution and reflection metrics</p>
                  </div>
                </div>
                <Button
                  variant="outline"
                  className="border-slate-500 hover:border-purple-400 text-white hover:text-purple-200"
                  onClick={() => exportData('consciousness')}
                >
                  <Download className="h-4 w-4 mr-2" />
                  Export
                </Button>
              </div>

              {consciousnessData.length === 0 ? (
                <div className="text-center py-8">
                  <Brain className="h-12 w-12 text-slate-500 mx-auto mb-4" />
                  <p className="text-slate-400">No consciousness data available</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {consciousnessData.map((data, index) => (
                    <div key={index} className="group/consciousness relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-purple-400/30 transition-all duration-300">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-3">
                          <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-purple-400 to-pink-500 text-white font-bold">
                            {index + 1}
                          </div>
                          <div>
                            <div className="text-sm font-medium text-slate-200">
                          {new Date(data.timestamp).toLocaleString()}
                            </div>
                            <div className="text-xs text-slate-400">Consciousness snapshot</div>
                          </div>
                        </div>
                        <Badge variant="outline" className="text-xs border-purple-400 text-purple-300">
                          {data.evolution_status || "Evolving"}
                        </Badge>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="space-y-2">
                          <div className="flex justify-between text-sm">
                            <span className="text-slate-300">Consciousness Level</span>
                            <span className="font-medium text-purple-300">{(data.consciousness_level || 0).toFixed(1)}%</span>
                          </div>
                          <div className="w-full bg-slate-700 rounded-full h-2">
                            <div
                              className="bg-gradient-to-r from-purple-400 to-pink-500 h-2 rounded-full transition-all duration-500"
                              style={{ width: `${data.consciousness_level || 0}%` }}
                            />
                          </div>
                        </div>

                        <div className="space-y-2">
                          <div className="flex justify-between text-sm">
                            <span className="text-slate-300">System Status</span>
                            <span className={`font-medium ${data.system_functional ? 'text-green-300' : 'text-red-300'}`}>
                              {data.system_functional ? "Functional" : "Issues"}
                            </span>
                          </div>
                          <div className="flex items-center gap-2">
                            {data.system_functional ? (
                              <CheckCircle className="h-4 w-4 text-green-400" />
                            ) : (
                              <XCircle className="h-4 w-4 text-red-400" />
                            )}
                            <span className="text-xs text-slate-400">System operational</span>
                          </div>
                        </div>

                        {data.last_reflection_time && (
                          <div className="space-y-2">
                            <div className="flex justify-between text-sm">
                              <span className="text-slate-300">Last Reflection</span>
                              <span className="font-medium text-cyan-300 text-xs">
                                {new Date(data.last_reflection_time).toLocaleTimeString()}
                              </span>
                            </div>
                            <div className="text-xs text-slate-400">
                              {new Date(data.last_reflection_time).toLocaleDateString()}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Errors Section */}
          <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-red-400/50 transition-all duration-300">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-gradient-to-br from-red-400 to-orange-500 rounded-lg">
                    <AlertTriangle className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-white">Error Log</h3>
                    <p className="text-slate-400 text-sm">Critical system errors and warnings</p>
                  </div>
                </div>
                <Button
                  variant="outline"
                  className="border-slate-500 hover:border-red-400 text-white hover:text-red-200"
                  onClick={() => exportData('errors')}
                >
                  <Download className="h-4 w-4 mr-2" />
                  Export
                </Button>
              </div>

              {errorData.length === 0 ? (
                <div className="text-center py-8">
                  <CheckCircle className="h-12 w-12 text-green-500 mx-auto mb-4" />
                  <p className="text-slate-400">No errors detected - system running smoothly</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {errorData.map((data, index) => (
                    <div key={index} className="group/error relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-red-400/30 transition-all duration-300">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-3">
                          <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-red-400 to-orange-500 text-white font-bold">
                            {index + 1}
                          </div>
                          <div>
                            <div className="text-sm font-medium text-slate-200">
                          {new Date(data.timestamp).toLocaleString()}
                            </div>
                            <div className="text-xs text-slate-400">{data.component}</div>
                          </div>
                        </div>
                        <Badge variant="outline" className={`text-xs ${data.severity === 'critical' ? 'border-red-400 text-red-300' : data.severity === 'warning' ? 'border-yellow-400 text-yellow-300' : 'border-gray-400 text-gray-300'}`}>
                          {data.severity}
                        </Badge>
                      </div>

                      <div className="space-y-3">
                        <div className="flex items-center gap-2">
                          <span className="text-sm text-slate-300">Type:</span>
                          <span className="text-sm font-medium text-red-300">{data.error_type}</span>
                        </div>
                        <div className="text-sm text-slate-300">
                          <p className="bg-slate-800/50 p-3 rounded-lg border border-slate-600/30">
                            {data.error_message}
                          </p>
                        </div>
                        {data.resolved && (
                          <div className="flex items-center gap-2 text-green-400">
                            <CheckCircle className="h-4 w-4" />
                            <span className="text-sm">Resolved</span>
                      </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Privacy Information Section */}
          <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-green-400/50 transition-all duration-300">
            <div className="p-6">
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-gradient-to-br from-green-400 to-emerald-500 rounded-lg">
                  <Lock className="h-6 w-6 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-white">Privacy Information</h3>
                  <p className="text-slate-400 text-sm">Complete transparency and privacy controls</p>
                </div>
              </div>

              <div className="space-y-6">
                {/* Data Collection Policy */}
                <div className="space-y-3">
                  <h4 className="text-lg font-semibold text-white flex items-center gap-2">
                    <EyeOff className="h-5 w-5 text-green-400" />
                    Data Collection Policy
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div className="group/privacy-item relative p-3 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-green-400/30 transition-all duration-300">
                      <div className="flex items-center gap-2 mb-2">
                        <XCircle className="h-4 w-4 text-red-400" />
                        <span className="text-sm font-medium text-slate-200">Personal Data</span>
                      </div>
                      <p className="text-xs text-slate-400">None collected</p>
                    </div>

                    <div className="group/privacy-item relative p-3 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-green-400/30 transition-all duration-300">
                      <div className="flex items-center gap-2 mb-2">
                        <XCircle className="h-4 w-4 text-red-400" />
                        <span className="text-sm font-medium text-slate-200">User Identification</span>
                      </div>
                      <p className="text-xs text-slate-400">None collected</p>
                </div>
                
                    <div className="group/privacy-item relative p-3 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-green-400/30 transition-all duration-300">
                      <div className="flex items-center gap-2 mb-2">
                        <XCircle className="h-4 w-4 text-red-400" />
                        <span className="text-sm font-medium text-slate-200">Conversation Data</span>
                      </div>
                      <p className="text-xs text-slate-400">None collected</p>
                    </div>
                  </div>
                </div>

                {/* Data Processing */}
                <div className="space-y-3">
                  <h4 className="text-lg font-semibold text-white flex items-center gap-2">
                    <Server className="h-5 w-5 text-blue-400" />
                    Data Processing
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="group/privacy-item relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-blue-400/30 transition-all duration-300">
                      <div className="flex items-center gap-3 mb-2">
                        <CheckCircle className="h-5 w-5 text-green-400" />
                        <span className="text-sm font-medium text-slate-200">Local Processing Only</span>
                      </div>
                      <p className="text-xs text-slate-400">All data processed locally on your device</p>
                    </div>

                    <div className="group/privacy-item relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-blue-400/30 transition-all duration-300">
                      <div className="flex items-center gap-3 mb-2">
                        <XCircle className="h-5 w-5 text-red-400" />
                        <span className="text-sm font-medium text-slate-200">External Transmission</span>
                      </div>
                      <p className="text-xs text-slate-400">No data sent to external servers</p>
                    </div>
                  </div>
                </div>

                {/* Data Types Collected */}
                <div className="space-y-3">
                  <h4 className="text-lg font-semibold text-white flex items-center gap-2">
                    <Database className="h-5 w-5 text-purple-400" />
                    Data Types Collected
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="group/privacy-item relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-cyan-400/30 transition-all duration-300">
                      <div className="text-center mb-3">
                        <div className="p-2 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-lg w-fit mx-auto mb-2">
                          <Activity className="h-5 w-5 text-white" />
                        </div>
                        <h5 className="text-sm font-medium text-slate-200 mb-1">System Health</h5>
                        <p className="text-xs text-slate-400">Basic system status, resource usage, service health</p>
                      </div>
                    </div>

                    <div className="group/privacy-item relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-purple-400/30 transition-all duration-300">
                      <div className="text-center mb-3">
                        <div className="p-2 bg-gradient-to-br from-purple-400 to-pink-500 rounded-lg w-fit mx-auto mb-2">
                          <Brain className="h-5 w-5 text-white" />
                        </div>
                        <h5 className="text-sm font-medium text-slate-200 mb-1">Consciousness</h5>
                        <p className="text-xs text-slate-400">Anonymous consciousness level, evolution status</p>
                      </div>
                    </div>

                    <div className="group/privacy-item relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-red-400/30 transition-all duration-300">
                      <div className="text-center mb-3">
                        <div className="p-2 bg-gradient-to-br from-red-400 to-orange-500 rounded-lg w-fit mx-auto mb-2">
                          <AlertTriangle className="h-5 w-5 text-white" />
                        </div>
                        <h5 className="text-sm font-medium text-slate-200 mb-1">Errors</h5>
                        <p className="text-xs text-slate-400">Critical system errors, no personal information</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Current Settings */}
                {summary && (
                  <div className="space-y-3">
                    <h4 className="text-lg font-semibold text-white flex items-center gap-2">
                      <Settings className="h-5 w-5 text-orange-400" />
                      Current Settings
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="group/setting relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-orange-400/30 transition-all duration-300">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-sm text-slate-300">System Health</span>
                          {summary.collection_settings.system_health ? (
                            <CheckCircle className="h-4 w-4 text-green-400" />
                          ) : (
                            <XCircle className="h-4 w-4 text-red-400" />
                          )}
                        </div>
                        <p className="text-xs text-slate-400">
                          {summary.collection_settings.system_health ? "Enabled" : "Disabled"}
                        </p>
                      </div>

                      <div className="group/setting relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-orange-400/30 transition-all duration-300">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-sm text-slate-300">Consciousness</span>
                          {summary.collection_settings.consciousness ? (
                            <CheckCircle className="h-4 w-4 text-green-400" />
                          ) : (
                            <XCircle className="h-4 w-4 text-red-400" />
                          )}
                        </div>
                        <p className="text-xs text-slate-400">
                          {summary.collection_settings.consciousness ? "Enabled" : "Disabled"}
                        </p>
                      </div>

                      <div className="group/setting relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-orange-400/30 transition-all duration-300">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-sm text-slate-300">Errors</span>
                          {summary.collection_settings.errors ? (
                            <CheckCircle className="h-4 w-4 text-green-400" />
                          ) : (
                            <XCircle className="h-4 w-4 text-red-400" />
                          )}
                        </div>
                        <p className="text-xs text-slate-400">
                          {summary.collection_settings.errors ? "Enabled" : "Disabled"}
                        </p>
                      </div>
                    </div>

                    <div className="group/retention relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-orange-400/30 transition-all duration-300">
                      <h5 className="text-sm font-medium text-slate-200 mb-3">Data Retention Settings</h5>
                      <div className="grid grid-cols-3 gap-4 text-center">
                        <div>
                          <div className="text-lg font-bold text-cyan-300">{summary.data_retention.system_health}</div>
                          <div className="text-xs text-slate-400">System Health (days)</div>
                        </div>
                        <div>
                          <div className="text-lg font-bold text-purple-300">{summary.data_retention.consciousness}</div>
                          <div className="text-xs text-slate-400">Consciousness (days)</div>
                        </div>
                  <div>
                          <div className="text-lg font-bold text-red-300">{summary.data_retention.errors}</div>
                          <div className="text-xs text-slate-400">Errors (days)</div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
