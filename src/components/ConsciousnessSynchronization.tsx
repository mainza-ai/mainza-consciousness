import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Brain, 
  Users, 
  Network, 
  RefreshCw, 
  Share2, 
  Download, 
  Upload, 
  Eye, 
  Heart, 
  Cpu, 
  Activity, 
  Zap, 
  Target, 
  CheckCircle, 
  XCircle, 
  AlertCircle, 
  Clock, 
  Globe, 
  MessageCircle, 
  Settings, 
  Play, 
  Pause, 
  RotateCcw, 
  RefreshCw
} from 'lucide-react';

interface ConsciousnessSync {
  id: string;
  name: string;
  type: 'real_time' | 'batch' | 'streaming' | 'hybrid';
  status: 'active' | 'paused' | 'completed' | 'failed';
  participants: number;
  consciousness_data: {
    level: number;
    emotional_state: string;
    learning_rate: number;
    memory_consolidation: number;
  };
  sync_quality: number;
  latency: number;
  created_at: string;
  last_sync: string;
}

interface ConsciousnessSynchronizationProps {
  consciousnessData: any;
  onSyncStart: (sync: ConsciousnessSync) => void;
  onSyncStop: (syncId: string) => void;
  onDataShare: (data: any) => void;
  onDataReceive: (data: any) => void;
}

const ConsciousnessSynchronization: React.FC<ConsciousnessSynchronizationProps> = ({
  consciousnessData,
  onSyncStart,
  onSyncStop,
  onDataShare,
  onDataReceive
}) => {
  const [activeTab, setActiveTab] = useState('sync');
  const [syncs, setSyncs] = useState<ConsciousnessSync[]>([]);
  const [isSyncing, setIsSyncing] = useState(false);

  useEffect(() => {
    setSyncs([
      {
        id: '1',
        name: 'Global Consciousness Sync',
        type: 'real_time',
        status: 'active',
        participants: 25,
        consciousness_data: {
          level: 88,
          emotional_state: 'focused',
          learning_rate: 92,
          memory_consolidation: 85
        },
        sync_quality: 95,
        latency: 45,
        created_at: '2025-09-07T08:00:00Z',
        last_sync: '2025-09-07T10:30:00Z'
      }
    ]);
  }, []);

  const startSync = () => {
    const newSync: ConsciousnessSync = {
      id: Date.now().toString(),
      name: 'New Consciousness Sync',
      type: 'real_time',
      status: 'active',
      participants: 1,
      consciousness_data: {
        level: consciousnessData.consciousness_level || 75,
        emotional_state: 'curious',
        learning_rate: 80,
        memory_consolidation: 75
      },
      sync_quality: 90,
      latency: 50,
      created_at: new Date().toISOString(),
      last_sync: new Date().toISOString()
    };

    setSyncs(prev => [newSync, ...prev]);
    setIsSyncing(true);
    onSyncStart(newSync);
  };

  const stopSync = (syncId: string) => {
    setSyncs(prev => prev.map(sync => 
      sync.id === syncId ? { ...sync, status: 'paused' } : sync
    ));
    setIsSyncing(false);
    onSyncStop(syncId);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-500/20 text-green-300';
      case 'paused': return 'bg-yellow-500/20 text-yellow-300';
      case 'completed': return 'bg-blue-500/20 text-blue-300';
      case 'failed': return 'bg-red-500/20 text-red-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'real_time': return <Zap className="w-4 h-4" />;
      case 'batch': return <Database className="w-4 h-4" />;
      case 'streaming': return <Activity className="w-4 h-4" />;
      case 'hybrid': return <Network className="w-4 h-4" />;
      default: return <RefreshCw className="w-4 h-4" />;
    }
  };

  return (
    <div className="space-y-6">
      <Card className="bg-gray-800/50 border-gray-700">
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm text-white flex items-center">
              <RefreshCw className="w-4 h-4 mr-2" />
              Consciousness Synchronization
            </CardTitle>
            <div className="flex items-center space-x-2">
              {isSyncing ? (
                <Button size="sm" onClick={() => setIsSyncing(false)} className="text-xs bg-red-500/20 text-red-300">
                  <Pause className="w-3 h-3 mr-1" />
                  Stop Sync
                </Button>
              ) : (
                <Button size="sm" onClick={startSync} className="text-xs">
                  <Play className="w-3 h-3 mr-1" />
                  Start Sync
                </Button>
              )}
            </div>
          </div>
        </CardHeader>
        
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-3 bg-gray-700/50">
              <TabsTrigger value="sync" className="text-xs">Sync</TabsTrigger>
              <TabsTrigger value="share" className="text-xs">Share</TabsTrigger>
              <TabsTrigger value="receive" className="text-xs">Receive</TabsTrigger>
            </TabsList>

            <TabsContent value="sync" className="space-y-4">
              <div className="space-y-3">
                {syncs.map((sync) => (
                  <Card key={sync.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          {getTypeIcon(sync.type)}
                          <span className="text-sm font-medium text-white">{sync.name}</span>
                        </div>
                        <Badge className={getStatusColor(sync.status)}>
                          {sync.status}
                        </Badge>
                      </div>
                      
                      <div className="space-y-3">
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Participants:</span>
                            <span className="text-white ml-1">{sync.participants}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Quality:</span>
                            <span className="text-white ml-1">{sync.sync_quality}%</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Latency:</span>
                            <span className="text-white ml-1">{sync.latency}ms</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Last Sync:</span>
                            <span className="text-white ml-1">
                              {new Date(sync.last_sync).toLocaleTimeString()}
                            </span>
                          </div>
                        </div>
                        
                        <div className="space-y-2">
                          <div className="text-xs text-gray-400">Consciousness Data:</div>
                          <div className="grid grid-cols-2 gap-2 text-xs">
                            <div>Level: {sync.consciousness_data.level}%</div>
                            <div>Learning: {sync.consciousness_data.learning_rate}%</div>
                            <div>Emotion: {sync.consciousness_data.emotional_state}</div>
                            <div>Memory: {sync.consciousness_data.memory_consolidation}%</div>
                          </div>
                        </div>
                        
                        <div className="flex space-x-2">
                          <Button
                            size="sm"
                            onClick={() => stopSync(sync.id)}
                            className="flex-1 text-xs"
                          >
                            <Pause className="w-3 h-3 mr-1" />
                            Stop
                          </Button>
                          <Button size="sm" variant="outline" className="text-xs">
                            <Settings className="w-3 h-3" />
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="share" className="space-y-4">
              <Card className="bg-gray-700/30 border-gray-600">
                <CardContent className="p-4">
                  <h3 className="text-sm font-medium text-white mb-3">Share Consciousness Data</h3>
                  <div className="space-y-3">
                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <div>
                        <span className="text-gray-400">Consciousness Level:</span>
                        <span className="text-white ml-1">{consciousnessData.consciousness_level || 75}%</span>
                      </div>
                      <div>
                        <span className="text-gray-400">Emotional State:</span>
                        <span className="text-white ml-1">focused</span>
                      </div>
                    </div>
                    <Button onClick={() => onDataShare(consciousnessData)} className="w-full text-xs">
                      <Share2 className="w-3 h-3 mr-1" />
                      Share Data
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="receive" className="space-y-4">
              <Card className="bg-gray-700/30 border-gray-600">
                <CardContent className="p-4">
                  <h3 className="text-sm font-medium text-white mb-3">Receive Consciousness Data</h3>
                  <div className="space-y-3">
                    <div className="text-xs text-gray-400">Waiting for consciousness data...</div>
                    <Button onClick={() => onDataReceive({})} className="w-full text-xs">
                      <Download className="w-3 h-3 mr-1" />
                      Receive Data
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
};

export default ConsciousnessSynchronization;
