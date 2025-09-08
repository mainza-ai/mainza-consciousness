/**
 * Privacy-First Telemetry Dashboard
 * 
 * Displays system health and consciousness metrics with complete privacy protection.
 * Shows exactly what data is collected (transparency) and provides user controls.
 */

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
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
  Info
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
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading telemetry data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Privacy Notice */}
      <Alert>
        <Shield className="h-4 w-4" />
        <AlertDescription>
          <strong>Privacy-First Telemetry:</strong> This system collects only essential data for system health monitoring. 
          No personal data, conversation content, or user behavior is collected. All data remains local and is never transmitted externally.
        </AlertDescription>
      </Alert>

      {/* Error Display */}
      {error && (
        <Alert variant="destructive">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Status and Controls */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="h-5 w-5" />
              System Status
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {status && (
              <>
                <div className="flex items-center justify-between">
                  <span>Telemetry Status:</span>
                  <Badge variant={status.collection_enabled ? "default" : "secondary"}>
                    {status.collection_enabled ? "Enabled" : "Disabled"}
                  </Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span>System Status:</span>
                  <Badge variant="outline">{status.status}</Badge>
                </div>
                <div className="text-sm text-gray-600">
                  <p><strong>Data Location:</strong> {status.data_location}</p>
                  <p><strong>Last Updated:</strong> {new Date(status.timestamp).toLocaleString()}</p>
                </div>
              </>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Settings className="h-5 w-5" />
              Controls
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {status && (
              <div className="flex items-center justify-between">
                <span>Enable Telemetry:</span>
                <Switch
                  checked={status.collection_enabled}
                  onCheckedChange={toggleTelemetry}
                />
              </div>
            )}
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => fetchTelemetrySummary()}
              >
                <Eye className="h-4 w-4 mr-2" />
                Refresh
              </Button>
              <Button
                variant="destructive"
                size="sm"
                onClick={deleteAllData}
              >
                <Trash2 className="h-4 w-4 mr-2" />
                Delete All Data
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Data Tabs */}
      <Tabs defaultValue="system" className="space-y-4">
        <TabsList>
          <TabsTrigger value="system">System Health</TabsTrigger>
          <TabsTrigger value="consciousness">Consciousness</TabsTrigger>
          <TabsTrigger value="errors">Errors</TabsTrigger>
          <TabsTrigger value="privacy">Privacy Info</TabsTrigger>
        </TabsList>

        <TabsContent value="system" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span className="flex items-center gap-2">
                  <Activity className="h-5 w-5" />
                  System Health Data
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => exportData('system_health')}
                >
                  <Download className="h-4 w-4 mr-2" />
                  Export
                </Button>
              </CardTitle>
              <CardDescription>
                System resource usage and health metrics (no personal data)
              </CardDescription>
            </CardHeader>
            <CardContent>
              {systemHealthData.length === 0 ? (
                <p className="text-gray-500 text-center py-4">No system health data available</p>
              ) : (
                <div className="space-y-4">
                  {systemHealthData.map((data, index) => (
                    <div key={index} className="border rounded-lg p-4 space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="font-medium">
                          {new Date(data.timestamp).toLocaleString()}
                        </span>
                        <div className="flex items-center gap-2">
                          <div className={`w-3 h-3 rounded-full ${getStatusColor(data.system_status)}`}></div>
                          <Badge variant="outline">{data.system_status}</Badge>
                        </div>
                      </div>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                        <div>
                          <span className="text-gray-600">Uptime:</span>
                          <p className="font-medium">{formatUptime(data.uptime_seconds)}</p>
                        </div>
                        <div>
                          <span className="text-gray-600">CPU:</span>
                          <p className="font-medium">{data.cpu_usage_percent.toFixed(1)}%</p>
                        </div>
                        <div>
                          <span className="text-gray-600">Memory:</span>
                          <p className="font-medium">{data.memory_usage_percent.toFixed(1)}%</p>
                        </div>
                        <div>
                          <span className="text-gray-600">Disk:</span>
                          <p className="font-medium">{data.disk_usage_percent.toFixed(1)}%</p>
                        </div>
                      </div>
                      {data.critical_errors > 0 && (
                        <div className="text-red-600 text-sm">
                          <AlertTriangle className="h-4 w-4 inline mr-1" />
                          {data.critical_errors} critical errors
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="consciousness" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span className="flex items-center gap-2">
                  <Brain className="h-5 w-5" />
                  Consciousness Data
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => exportData('consciousness')}
                >
                  <Download className="h-4 w-4 mr-2" />
                  Export
                </Button>
              </CardTitle>
              <CardDescription>
                Anonymous consciousness level and evolution metrics (no personal context)
              </CardDescription>
            </CardHeader>
            <CardContent>
              {consciousnessData.length === 0 ? (
                <p className="text-gray-500 text-center py-4">No consciousness data available</p>
              ) : (
                <div className="space-y-4">
                  {consciousnessData.map((data, index) => (
                    <div key={index} className="border rounded-lg p-4 space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="font-medium">
                          {new Date(data.timestamp).toLocaleString()}
                        </span>
                        <Badge variant="outline">{data.evolution_status}</Badge>
                      </div>
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
                        <div>
                          <span className="text-gray-600">Consciousness Level:</span>
                          <p className="font-medium">{data.consciousness_level.toFixed(1)}%</p>
                        </div>
                        <div>
                          <span className="text-gray-600">System Functional:</span>
                          <p className="font-medium">{data.system_functional ? "Yes" : "No"}</p>
                        </div>
                        {data.last_reflection_time && (
                          <div>
                            <span className="text-gray-600">Last Reflection:</span>
                            <p className="font-medium">
                              {new Date(data.last_reflection_time).toLocaleString()}
                            </p>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="errors" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span className="flex items-center gap-2">
                  <AlertTriangle className="h-5 w-5" />
                  Error Log
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => exportData('errors')}
                >
                  <Download className="h-4 w-4 mr-2" />
                  Export
                </Button>
              </CardTitle>
              <CardDescription>
                Critical system errors and warnings (no personal data)
              </CardDescription>
            </CardHeader>
            <CardContent>
              {errorData.length === 0 ? (
                <p className="text-gray-500 text-center py-4">No error data available</p>
              ) : (
                <div className="space-y-4">
                  {errorData.map((data, index) => (
                    <div key={index} className="border rounded-lg p-4 space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="font-medium">
                          {new Date(data.timestamp).toLocaleString()}
                        </span>
                        <div className="flex items-center gap-2">
                          <div className={`w-3 h-3 rounded-full ${getSeverityColor(data.severity)}`}></div>
                          <Badge variant="outline">{data.severity}</Badge>
                        </div>
                      </div>
                      <div className="text-sm">
                        <p><strong>Type:</strong> {data.error_type}</p>
                        <p><strong>Component:</strong> {data.component}</p>
                        <p><strong>Message:</strong> {data.error_message}</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="privacy" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Info className="h-5 w-5" />
                Privacy Information
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-4">
                <div>
                  <h4 className="font-medium mb-2">Data Collection Policy</h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• <strong>Personal Data:</strong> None collected</li>
                    <li>• <strong>User Identification:</strong> None collected</li>
                    <li>• <strong>Conversation Data:</strong> None collected</li>
                    <li>• <strong>Usage Patterns:</strong> None collected</li>
                    <li>• <strong>Session Data:</strong> None collected</li>
                  </ul>
                </div>
                
                <div>
                  <h4 className="font-medium mb-2">Data Processing</h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• <strong>Local Processing:</strong> All data processed locally</li>
                    <li>• <strong>External Transmission:</strong> None</li>
                    <li>• <strong>Third-Party Services:</strong> None used</li>
                    <li>• <strong>Cloud Storage:</strong> None used</li>
                  </ul>
                </div>

                <div>
                  <h4 className="font-medium mb-2">Data Types Collected</h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• <strong>System Health:</strong> Basic system status, resource usage, service health</li>
                    <li>• <strong>Consciousness:</strong> Anonymous consciousness level, evolution status</li>
                    <li>• <strong>Errors:</strong> Critical system errors, no personal information</li>
                  </ul>
                </div>

                <div>
                  <h4 className="font-medium mb-2">User Controls</h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• <strong>Enable/Disable:</strong> Complete control over data collection</li>
                    <li>• <strong>Data Deletion:</strong> Delete all data at any time</li>
                    <li>• <strong>Collection Settings:</strong> Control what data is collected</li>
                    <li>• <strong>Data Export:</strong> Export your data for review</li>
                  </ul>
                </div>

                {summary && (
                  <div>
                    <h4 className="font-medium mb-2">Current Settings</h4>
                    <div className="text-sm text-gray-600 space-y-1">
                      <p><strong>System Health Collection:</strong> {summary.collection_settings.system_health ? "Enabled" : "Disabled"}</p>
                      <p><strong>Consciousness Collection:</strong> {summary.collection_settings.consciousness ? "Enabled" : "Disabled"}</p>
                      <p><strong>Error Collection:</strong> {summary.collection_settings.errors ? "Enabled" : "Disabled"}</p>
                      <p><strong>Data Retention:</strong> System Health ({summary.data_retention.system_health} days), Consciousness ({summary.data_retention.consciousness} days), Errors ({summary.data_retention.errors} days)</p>
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};
