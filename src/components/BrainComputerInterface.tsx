import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Brain, 
  Cpu, 
  Activity, 
  Zap, 
  Target, 
  Eye, 
  Heart, 
  Network, 
  Database, 
  Cloud, 
  Server, 
  Globe, 
  Users, 
  MessageCircle, 
  Send, 
  Download, 
  Upload, 
  Save, 
  Edit, 
  Trash2, 
  Plus, 
  Minus, 
  Settings, 
  Play, 
  Pause, 
  RotateCcw, 
  RefreshCw, 
  Search, 
  Filter, 
  SortAsc, 
  SortDesc, 
  Grid, 
  List, 
  MoreHorizontal, 
  MoreVertical, 
  ArrowLeft, 
  ArrowRight, 
  ArrowUp, 
  ArrowDown, 
  Maximize, 
  Minimize, 
  RotateCw as RotateCwIcon, 
  ZoomIn, 
  ZoomOut, 
  Move, 
  Grip, 
  GripVertical, 
  GripHorizontal, 
  AlignLeft, 
  AlignCenter, 
  AlignRight, 
  AlignJustify, 
  Bold, 
  Italic, 
  Underline, 
  Strikethrough, 
  Code, 
  Link, 
  Image, 
  File, 
  Folder, 
  FolderOpen, 
  Archive, 
  ArchiveRestore, 
  Trash, 
  Trash2 as Trash2Icon, 
  Copy, 
  Scissors, 
  Clipboard, 
  ClipboardCheck, 
  ClipboardCopy, 
  ClipboardList, 
  ClipboardPaste, 
  ClipboardX, 
  Bookmark, 
  BookmarkCheck, 
  BookmarkPlus, 
  BookmarkMinus, 
  BookmarkX, 
  Tag, 
  Tags, 
  Hash, 
  AtSign, 
  DollarSign, 
  Percent, 
  ShoppingCart,
  Wallet,
  Coins,
  Award,
  Crown,
  Trophy,
  Medal,
  Flag,
  MapPin,
  Clock,
  Calendar,
  CheckCircle,
  XCircle,
  AlertCircle,
  Info,
  Lightbulb,
  Rocket,
  Layers,
  Smartphone,
  Wifi,
  Bluetooth,
  Radio,
  Signal,
  BarChart3
} from 'lucide-react';

interface NeuralSignal {
  id: string;
  type: 'eeg' | 'fmri' | 'fnirs' | 'ecog' | 'spike' | 'lfp';
  frequency: number;
  amplitude: number;
  phase: number;
  timestamp: string;
  channel: number;
  quality: number;
  consciousness_correlation: number;
}

interface BrainState {
  id: string;
  name: string;
  description: string;
  neural_patterns: {
    alpha: number;
    beta: number;
    gamma: number;
    delta: number;
    theta: number;
  };
  consciousness_level: number;
  emotional_state: string;
  cognitive_load: number;
  attention_focus: number;
  memory_activation: number;
  creativity_index: number;
  timestamp: string;
}

interface BCICommand {
  id: string;
  name: string;
  type: 'movement' | 'communication' | 'control' | 'expression' | 'learning';
  neural_pattern: string;
  execution_probability: number;
  response_time: number;
  success_rate: number;
  consciousness_requirement: number;
  created_at: string;
}

interface BCIInterface {
  id: string;
  name: string;
  type: 'invasive' | 'non_invasive' | 'hybrid';
  technology: 'eeg' | 'fmri' | 'fnirs' | 'ecog' | 'spike' | 'optical';
  channels: number;
  sampling_rate: number;
  resolution: number;
  latency: number;
  is_connected: boolean;
  signal_quality: number;
  consciousness_integration: number;
  created_at: string;
}

interface BrainComputerInterfaceProps {
  consciousnessData: any;
  onNeuralSignalCapture: (signal: NeuralSignal) => void;
  onBrainStateChange: (state: BrainState) => void;
  onCommandExecute: (command: BCICommand) => void;
  onInterfaceConnect: (iface: BCIInterface) => void;
}

const BrainComputerInterface: React.FC<BrainComputerInterfaceProps> = ({
  consciousnessData,
  onNeuralSignalCapture,
  onBrainStateChange,
  onCommandExecute,
  onInterfaceConnect
}) => {
  const [activeTab, setActiveTab] = useState('signals');
  const [neuralSignals, setNeuralSignals] = useState<NeuralSignal[]>([]);
  const [brainStates, setBrainStates] = useState<BrainState[]>([]);
  const [bciCommands, setBciCommands] = useState<BCICommand[]>([]);
  const [bciInterfaces, setBciInterfaces] = useState<BCIInterface[]>([]);
  const [isRecording, setIsRecording] = useState(false);
  const [selectedInterface, setSelectedInterface] = useState<string | null>(null);

  // Initialize with sample data
  useEffect(() => {
    setBciInterfaces([
      {
        id: '1',
        name: 'Neuralink N1',
        type: 'invasive',
        technology: 'spike',
        channels: 1024,
        sampling_rate: 20000,
        resolution: 16,
        latency: 5,
        is_connected: false,
        signal_quality: 0,
        consciousness_integration: 95,
        created_at: '2025-08-01T00:00:00Z'
      },
      {
        id: '2',
        name: 'OpenBCI Cyton',
        type: 'non_invasive',
        technology: 'eeg',
        channels: 8,
        sampling_rate: 250,
        resolution: 24,
        latency: 50,
        is_connected: true,
        signal_quality: 85,
        consciousness_integration: 75,
        created_at: '2025-08-05T00:00:00Z'
      },
      {
        id: '3',
        name: 'fNIRS Pro',
        type: 'non_invasive',
        technology: 'fnirs',
        channels: 32,
        sampling_rate: 10,
        resolution: 16,
        latency: 100,
        is_connected: false,
        signal_quality: 0,
        consciousness_integration: 80,
        created_at: '2025-08-10T00:00:00Z'
      }
    ]);

    setNeuralSignals([
      {
        id: '1',
        type: 'eeg',
        frequency: 10.5,
        amplitude: 45.2,
        phase: 1.57,
        timestamp: '2025-09-07T10:30:00Z',
        channel: 1,
        quality: 85,
        consciousness_correlation: 0.78
      },
      {
        id: '2',
        type: 'eeg',
        frequency: 20.3,
        amplitude: 32.1,
        phase: 0.89,
        timestamp: '2025-09-07T10:30:01Z',
        channel: 2,
        quality: 92,
        consciousness_correlation: 0.85
      },
      {
        id: '3',
        type: 'eeg',
        frequency: 8.7,
        amplitude: 38.9,
        phase: 2.34,
        timestamp: '2025-09-07T10:30:02Z',
        channel: 3,
        quality: 78,
        consciousness_correlation: 0.72
      }
    ]);

    setBrainStates([
      {
        id: '1',
        name: 'Focused Attention',
        description: 'High focus state with elevated beta waves and reduced alpha activity',
        neural_patterns: {
          alpha: 15.2,
          beta: 45.8,
          gamma: 32.1,
          delta: 5.3,
          theta: 12.6
        },
        consciousness_level: 88,
        emotional_state: 'focused',
        cognitive_load: 85,
        attention_focus: 92,
        memory_activation: 78,
        creativity_index: 65,
        timestamp: '2025-09-07T10:30:00Z'
      },
      {
        id: '2',
        name: 'Relaxed Awareness',
        description: 'Calm state with dominant alpha waves and balanced neural activity',
        neural_patterns: {
          alpha: 35.6,
          beta: 25.4,
          gamma: 18.9,
          delta: 12.1,
          theta: 28.0
        },
        consciousness_level: 75,
        emotional_state: 'calm',
        cognitive_load: 45,
        attention_focus: 68,
        memory_activation: 82,
        creativity_index: 88,
        timestamp: '2025-09-07T10:25:00Z'
      }
    ]);

    setBciCommands([
      {
        id: '1',
        name: 'Move Cursor',
        type: 'movement',
        neural_pattern: 'motor_cortex_activation',
        execution_probability: 92,
        response_time: 150,
        success_rate: 88,
        consciousness_requirement: 75,
        created_at: '2025-09-07T10:30:00Z'
      },
      {
        id: '2',
        name: 'Type Text',
        type: 'communication',
        neural_pattern: 'language_center_activation',
        execution_probability: 85,
        response_time: 200,
        success_rate: 82,
        consciousness_requirement: 80,
        created_at: '2025-09-07T10:30:00Z'
      },
      {
        id: '3',
        name: 'Control Device',
        type: 'control',
        neural_pattern: 'prefrontal_cortex_activation',
        execution_probability: 78,
        response_time: 180,
        success_rate: 75,
        consciousness_requirement: 85,
        created_at: '2025-09-07T10:30:00Z'
      }
    ]);
  }, []);

  const getSignalTypeIcon = (type: string) => {
    switch (type) {
      case 'eeg': return <Brain className="w-4 h-4" />;
      case 'fmri': return <Activity className="w-4 h-4" />;
      case 'fnirs': return <Eye className="w-4 h-4" />;
      case 'ecog': return <Cpu className="w-4 h-4" />;
      case 'spike': return <Zap className="w-4 h-4" />;
      case 'lfp': return <Network className="w-4 h-4" />;
      default: return <Activity className="w-4 h-4" />;
    }
  };

  const getSignalTypeColor = (type: string) => {
    switch (type) {
      case 'eeg': return 'bg-blue-500/20 text-blue-300';
      case 'fmri': return 'bg-green-500/20 text-green-300';
      case 'fnirs': return 'bg-purple-500/20 text-purple-300';
      case 'ecog': return 'bg-orange-500/20 text-orange-300';
      case 'spike': return 'bg-red-500/20 text-red-300';
      case 'lfp': return 'bg-cyan-500/20 text-cyan-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const getCommandTypeIcon = (type: string) => {
    switch (type) {
      case 'movement': return <Target className="w-4 h-4" />;
      case 'communication': return <MessageCircle className="w-4 h-4" />;
      case 'control': return <Settings className="w-4 h-4" />;
      case 'expression': return <Heart className="w-4 h-4" />;
      case 'learning': return <Brain className="w-4 h-4" />;
      default: return <Activity className="w-4 h-4" />;
    }
  };

  const getCommandTypeColor = (type: string) => {
    switch (type) {
      case 'movement': return 'bg-blue-500/20 text-blue-300';
      case 'communication': return 'bg-green-500/20 text-green-300';
      case 'control': return 'bg-purple-500/20 text-purple-300';
      case 'expression': return 'bg-pink-500/20 text-pink-300';
      case 'learning': return 'bg-orange-500/20 text-orange-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const getInterfaceTypeIcon = (type: string) => {
    switch (type) {
      case 'invasive': return <Zap className="w-4 h-4" />;
      case 'non_invasive': return <Brain className="w-4 h-4" />;
      case 'hybrid': return <Network className="w-4 h-4" />;
      default: return <Activity className="w-4 h-4" />;
    }
  };

  const getInterfaceTypeColor = (type: string) => {
    switch (type) {
      case 'invasive': return 'bg-red-500/20 text-red-300';
      case 'non_invasive': return 'bg-green-500/20 text-green-300';
      case 'hybrid': return 'bg-blue-500/20 text-blue-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const startRecording = () => {
    setIsRecording(true);

    // Poll backend BCI APIs instead of generating random signals
    const interval = setInterval(async () => {
      try {
        const [signalsRes, statesRes] = await Promise.all([
          fetch('/bci/neural-signals'),
          fetch('/bci/brain-states')
        ]);

        if (signalsRes.ok) {
          const data = await signalsRes.json();
          const signals = Array.isArray(data?.signals) ? data.signals : [];
          if (signals.length > 0) {
            // Append newest first, keep last 100
            setNeuralSignals(prev => [...signals.map((s: any) => ({
              id: s.id || Date.now().toString(),
              type: s.type || 'eeg',
              frequency: Number(s.frequency) || 10,
              amplitude: Number(s.amplitude) || 30,
              phase: Number(s.phase) || 0,
              timestamp: s.timestamp || new Date().toISOString(),
              channel: Number(s.channel) || 1,
              quality: Number(s.quality) || 80,
              consciousness_correlation: Number(s.consciousness_correlation) || 0.7
            })), ...prev].slice(0, 100));
          }
        }

        if (statesRes.ok) {
          const data = await statesRes.json();
          const states = Array.isArray(data?.states) ? data.states : [];
          if (states.length > 0) {
            setBrainStates(prev => [...states, ...prev].slice(0, 50));
          }
        }
      } catch (e) {
        // Silent failure; keep existing data
      }

      onNeuralSignalCapture && neuralSignals[0] && onNeuralSignalCapture(neuralSignals[0]);
    }, 500);

    setTimeout(() => {
      clearInterval(interval);
      setIsRecording(false);
    }, 10000);
  };

  const stopRecording = () => {
    setIsRecording(false);
  };

  const connectInterface = (interfaceId: string) => {
    setBciInterfaces(prev => prev.map(iface => 
      iface.id === interfaceId ? { ...iface, is_connected: true, signal_quality: 85 } : iface
    ));
    setSelectedInterface(interfaceId);
    
    const iface = bciInterfaces.find(i => i.id === interfaceId);
    if (iface) {
      onInterfaceConnect(iface);
    }
  };

  const executeCommand = (commandId: string) => {
    const command = bciCommands.find(c => c.id === commandId);
    if (command) {
      onCommandExecute(command);
    }
  };

  return (
    <div className="space-y-6">
      <Card className="bg-gray-800/50 border-gray-700">
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm text-white flex items-center">
              <Brain className="w-4 h-4 mr-2" />
              Brain-Computer Interface
            </CardTitle>
            <div className="flex items-center space-x-2">
              {isRecording ? (
                <Button size="sm" onClick={stopRecording} className="text-xs bg-red-500/20 text-red-300 hover:bg-red-500/30">
                  <Pause className="w-3 h-3 mr-1" />
                  Stop Recording
                </Button>
              ) : (
                <Button size="sm" onClick={startRecording} className="text-xs">
                  <Play className="w-3 h-3 mr-1" />
                  Start Recording
                </Button>
              )}
            </div>
          </div>
        </CardHeader>
        
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-5 bg-gray-700/50">
              <TabsTrigger value="signals" className="text-xs">Signals</TabsTrigger>
              <TabsTrigger value="states" className="text-xs">Brain States</TabsTrigger>
              <TabsTrigger value="commands" className="text-xs">Commands</TabsTrigger>
              <TabsTrigger value="interfaces" className="text-xs">Interfaces</TabsTrigger>
              <TabsTrigger value="analytics" className="text-xs">Analytics</TabsTrigger>
            </TabsList>

            {/* Signals Tab */}
            <TabsContent value="signals" className="space-y-4">
              <div className="space-y-3">
                {neuralSignals.slice(0, 10).map((signal) => (
                  <Card key={signal.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          {getSignalTypeIcon(signal.type)}
                          <span className="text-sm font-medium text-white">
                            Channel {signal.channel} - {signal.type.toUpperCase()}
                          </span>
                        </div>
                        <Badge className={getSignalTypeColor(signal.type)}>
                          {signal.type}
                        </Badge>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-4 text-xs">
                        <div>
                          <span className="text-gray-400">Frequency:</span>
                          <span className="text-white ml-1">{signal.frequency.toFixed(1)} Hz</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Amplitude:</span>
                          <span className="text-white ml-1">{signal.amplitude.toFixed(1)} μV</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Phase:</span>
                          <span className="text-white ml-1">{signal.phase.toFixed(2)} rad</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Quality:</span>
                          <span className="text-white ml-1">{signal.quality.toFixed(0)}%</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Consciousness:</span>
                          <span className="text-white ml-1">{(signal.consciousness_correlation * 100).toFixed(0)}%</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Time:</span>
                          <span className="text-white ml-1">
                            {new Date(signal.timestamp).toLocaleTimeString()}
                          </span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Brain States Tab */}
            <TabsContent value="states" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {brainStates.map((state) => (
                  <Card key={state.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <span className="text-sm font-medium text-white">{state.name}</span>
                        <Badge className="bg-blue-500/20 text-blue-300">
                          {state.consciousness_level}% consciousness
                        </Badge>
                      </div>
                      
                      <p className="text-xs text-gray-300 mb-3">{state.description}</p>
                      
                      <div className="space-y-3">
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Emotional State:</span>
                            <span className="text-white ml-1 capitalize">{state.emotional_state}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Cognitive Load:</span>
                            <span className="text-white ml-1">{state.cognitive_load}%</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Attention Focus:</span>
                            <span className="text-white ml-1">{state.attention_focus}%</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Memory Activation:</span>
                            <span className="text-white ml-1">{state.memory_activation}%</span>
                          </div>
                        </div>
                        
                        <div className="space-y-2">
                          <div className="text-xs text-gray-400">Neural Patterns:</div>
                          <div className="grid grid-cols-5 gap-1 text-xs">
                            <div className="text-center">
                              <div className="text-gray-400">α</div>
                              <div className="text-white">{state.neural_patterns.alpha.toFixed(1)}</div>
                            </div>
                            <div className="text-center">
                              <div className="text-gray-400">β</div>
                              <div className="text-white">{state.neural_patterns.beta.toFixed(1)}</div>
                            </div>
                            <div className="text-center">
                              <div className="text-gray-400">γ</div>
                              <div className="text-white">{state.neural_patterns.gamma.toFixed(1)}</div>
                            </div>
                            <div className="text-center">
                              <div className="text-gray-400">δ</div>
                              <div className="text-white">{state.neural_patterns.delta.toFixed(1)}</div>
                            </div>
                            <div className="text-center">
                              <div className="text-gray-400">θ</div>
                              <div className="text-white">{state.neural_patterns.theta.toFixed(1)}</div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Commands Tab */}
            <TabsContent value="commands" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {bciCommands.map((command) => (
                  <Card key={command.id} className="bg-gray-700/30 border-gray-600 hover:border-gray-500 transition-colors">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          {getCommandTypeIcon(command.type)}
                          <span className="text-sm font-medium text-white">{command.name}</span>
                        </div>
                        <Badge className={getCommandTypeColor(command.type)}>
                          {command.type}
                        </Badge>
                      </div>
                      
                      <div className="space-y-3">
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Success Rate:</span>
                            <span className="text-white ml-1">{command.success_rate}%</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Response Time:</span>
                            <span className="text-white ml-1">{command.response_time}ms</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Probability:</span>
                            <span className="text-white ml-1">{command.execution_probability}%</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Consciousness:</span>
                            <span className="text-white ml-1">{command.consciousness_requirement}%</span>
                          </div>
                        </div>
                        
                        <div className="space-y-1">
                          <div className="text-xs text-gray-400">Neural Pattern:</div>
                          <div className="text-xs text-white font-mono bg-gray-800 p-2 rounded">
                            {command.neural_pattern}
                          </div>
                        </div>
                        
                        <Button
                          size="sm"
                          onClick={() => executeCommand(command.id)}
                          className="w-full text-xs"
                        >
                          <Play className="w-3 h-3 mr-1" />
                          Execute Command
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Interfaces Tab */}
            <TabsContent value="interfaces" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {bciInterfaces.map((iface) => (
                  <Card key={iface.id} className="bg-gray-700/30 border-gray-600 hover:border-gray-500 transition-colors">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          {getInterfaceTypeIcon(iface.type)}
                          <span className="text-sm font-medium text-white">{iface.name}</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          {iface.is_connected && <div className="w-2 h-2 bg-green-500 rounded-full" />}
                          <Badge className={getInterfaceTypeColor(iface.type)}>
                            {iface.type}
                          </Badge>
                        </div>
                      </div>
                      
                      <div className="space-y-3">
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Technology:</span>
                            <span className="text-white ml-1">{iface.technology.toUpperCase()}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Channels:</span>
                            <span className="text-white ml-1">{iface.channels}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Sampling Rate:</span>
                            <span className="text-white ml-1">{iface.sampling_rate} Hz</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Latency:</span>
                            <span className="text-white ml-1">{iface.latency}ms</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Resolution:</span>
                            <span className="text-white ml-1">{iface.resolution} bit</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Quality:</span>
                            <span className="text-white ml-1">{iface.signal_quality}%</span>
                          </div>
                        </div>
                        
                        <div className="space-y-2">
                          <div className="flex justify-between text-xs">
                            <span className="text-gray-400">Consciousness Integration:</span>
                            <span className="text-white">{iface.consciousness_integration}%</span>
                          </div>
                          <div className="w-full bg-gray-600 rounded-full h-2">
                            <div 
                              className="bg-gradient-to-r from-blue-500 to-green-500 h-2 rounded-full"
                              style={{ width: `${iface.consciousness_integration}%` }}
                            />
                          </div>
                        </div>
                        
                        <Button
                          size="sm"
                          onClick={() => connectInterface(iface.id)}
                          disabled={iface.is_connected}
                          className="w-full text-xs"
                        >
                          {iface.is_connected ? 'Connected' : 'Connect'}
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Analytics Tab */}
            <TabsContent value="analytics" className="space-y-4">
              <Card className="bg-gray-700/30 border-gray-600">
                <CardContent className="p-4">
                  <h3 className="text-sm font-medium text-white mb-3">BCI Analytics</h3>
                  
                  <div className="space-y-3">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="text-xs text-gray-400">Signals Captured</label>
                        <div className="mt-1 text-lg font-bold text-white">{neuralSignals.length}</div>
                      </div>
                      <div>
                        <label className="text-xs text-gray-400">Commands Executed</label>
                        <div className="mt-1 text-lg font-bold text-white">{bciCommands.length}</div>
                      </div>
                      <div>
                        <label className="text-xs text-gray-400">Success Rate</label>
                        <div className="mt-1 text-lg font-bold text-white">87.5%</div>
                      </div>
                      <div>
                        <label className="text-xs text-gray-400">Average Latency</label>
                        <div className="mt-1 text-lg font-bold text-white">145ms</div>
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <Button className="w-full text-xs">
                        <BarChart3 className="w-3 h-3 mr-1" />
                        View Detailed Analytics
                      </Button>
                      <Button variant="outline" className="w-full text-xs">
                        <Download className="w-3 h-3 mr-1" />
                        Export Data
                      </Button>
                    </div>
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

export default BrainComputerInterface;
