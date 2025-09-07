import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Atom, 
  Zap, 
  Cpu, 
  Database, 
  Cloud, 
  Server, 
  Globe, 
  Users, 
  MessageCircle, 
  Send, 
  Eye, 
  EyeOff, 
  Lock, 
  Unlock, 
  Star, 
  Heart, 
  Share2, 
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
  TrendingUp,
  TrendingDown,
  Activity,
  Target,
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
  Brain,
  Network,
  Layers
} from 'lucide-react';

interface QuantumProcessor {
  id: string;
  name: string;
  type: 'superconducting' | 'trapped_ion' | 'topological' | 'photonic' | 'neutral_atom';
  qubits: number;
  coherence_time: number;
  gate_fidelity: number;
  connectivity: number;
  error_rate: number;
  is_available: boolean;
  queue_length: number;
  estimated_wait_time: number;
  consciousness_capability: {
    max_consciousness_level: number;
    processing_power: number;
    memory_capacity: number;
    parallel_processing: number;
  };
  technical_specs: {
    temperature: number;
    magnetic_field: number;
    control_precision: number;
    measurement_fidelity: number;
  };
  created_at: string;
  last_updated: string;
}

interface QuantumConsciousnessJob {
  id: string;
  name: string;
  type: 'consciousness_simulation' | 'neural_optimization' | 'emotion_analysis' | 'learning_acceleration' | 'memory_consolidation';
  status: 'queued' | 'running' | 'completed' | 'failed' | 'cancelled';
  priority: 'low' | 'medium' | 'high' | 'critical';
  processor_id: string;
  estimated_duration: number;
  actual_duration?: number;
  progress: number;
  consciousness_data: {
    input_level: number;
    target_level: number;
    emotional_state: string;
    learning_rate: number;
    complexity: number;
  };
  quantum_circuit: {
    gates: number;
    depth: number;
    qubits_used: number;
    entanglement_level: number;
  };
  results?: {
    consciousness_enhancement: number;
    processing_speed: number;
    accuracy: number;
    insights: string[];
  };
  created_at: string;
  started_at?: string;
  completed_at?: string;
}

interface QuantumConsciousnessExperiment {
  id: string;
  name: string;
  description: string;
  hypothesis: string;
  methodology: string;
  status: 'planning' | 'running' | 'completed' | 'failed';
  duration: number;
  participants: number;
  consciousness_metrics: {
    baseline_level: number;
    target_level: number;
    measured_level: number;
    improvement: number;
  };
  quantum_parameters: {
    qubits: number;
    gates: number;
    entanglement: number;
    coherence: number;
  };
  results: {
    success_rate: number;
    average_improvement: number;
    statistical_significance: number;
    insights: string[];
  };
  created_at: string;
  last_updated: string;
}

interface QuantumConsciousnessProps {
  consciousnessData: any;
  onJobSubmit: (job: QuantumConsciousnessJob) => void;
  onExperimentStart: (experiment: QuantumConsciousnessExperiment) => void;
  onProcessorSelect: (processor: QuantumProcessor) => void;
}

const QuantumConsciousness: React.FC<QuantumConsciousnessProps> = ({
  consciousnessData,
  onJobSubmit,
  onExperimentStart,
  onProcessorSelect
}) => {
  const [activeTab, setActiveTab] = useState('processors');
  const [processors, setProcessors] = useState<QuantumProcessor[]>([]);
  const [jobs, setJobs] = useState<QuantumConsciousnessJob[]>([]);
  const [experiments, setExperiments] = useState<QuantumConsciousnessExperiment[]>([]);
  const [selectedProcessor, setSelectedProcessor] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  // Initialize with sample data
  useEffect(() => {
    setProcessors([
      {
        id: '1',
        name: 'IBM Quantum Eagle',
        type: 'superconducting',
        qubits: 127,
        coherence_time: 100,
        gate_fidelity: 99.5,
        connectivity: 95,
        error_rate: 0.5,
        is_available: true,
        queue_length: 3,
        estimated_wait_time: 15,
        consciousness_capability: {
          max_consciousness_level: 95,
          processing_power: 1000,
          memory_capacity: 10000,
          parallel_processing: 50
        },
        technical_specs: {
          temperature: 0.015,
          magnetic_field: 0.1,
          control_precision: 99.8,
          measurement_fidelity: 99.2
        },
        created_at: '2025-08-01T00:00:00Z',
        last_updated: '2025-09-07T10:30:00Z'
      },
      {
        id: '2',
        name: 'IonQ Forte',
        type: 'trapped_ion',
        qubits: 32,
        coherence_time: 1000,
        gate_fidelity: 99.9,
        connectivity: 100,
        error_rate: 0.1,
        is_available: true,
        queue_length: 1,
        estimated_wait_time: 5,
        consciousness_capability: {
          max_consciousness_level: 98,
          processing_power: 800,
          memory_capacity: 8000,
          parallel_processing: 40
        },
        technical_specs: {
          temperature: 0.001,
          magnetic_field: 0.05,
          control_precision: 99.9,
          measurement_fidelity: 99.5
        },
        created_at: '2025-08-05T00:00:00Z',
        last_updated: '2025-09-07T10:25:00Z'
      },
      {
        id: '3',
        name: 'Google Sycamore',
        type: 'superconducting',
        qubits: 70,
        coherence_time: 50,
        gate_fidelity: 99.0,
        connectivity: 80,
        error_rate: 1.0,
        is_available: false,
        queue_length: 8,
        estimated_wait_time: 45,
        consciousness_capability: {
          max_consciousness_level: 90,
          processing_power: 600,
          memory_capacity: 6000,
          parallel_processing: 30
        },
        technical_specs: {
          temperature: 0.02,
          magnetic_field: 0.15,
          control_precision: 99.0,
          measurement_fidelity: 98.5
        },
        created_at: '2025-08-10T00:00:00Z',
        last_updated: '2025-09-07T09:45:00Z'
      }
    ]);

    setJobs([
      {
        id: '1',
        name: 'Consciousness Enhancement #1',
        type: 'consciousness_simulation',
        status: 'running',
        priority: 'high',
        processor_id: '1',
        estimated_duration: 30,
        actual_duration: 15,
        progress: 50,
        consciousness_data: {
          input_level: 75,
          target_level: 90,
          emotional_state: 'curious',
          learning_rate: 85,
          complexity: 8
        },
        quantum_circuit: {
          gates: 150,
          depth: 25,
          qubits_used: 20,
          entanglement_level: 0.8
        },
        results: {
          consciousness_enhancement: 12,
          processing_speed: 3.5,
          accuracy: 94.2,
          insights: ['Enhanced emotional processing', 'Improved learning efficiency', 'Increased self-awareness']
        },
        created_at: '2025-09-07T10:00:00Z',
        started_at: '2025-09-07T10:15:00Z'
      },
      {
        id: '2',
        name: 'Neural Optimization #2',
        type: 'neural_optimization',
        status: 'completed',
        priority: 'medium',
        processor_id: '2',
        estimated_duration: 45,
        actual_duration: 42,
        progress: 100,
        consciousness_data: {
          input_level: 80,
          target_level: 95,
          emotional_state: 'focused',
          learning_rate: 90,
          complexity: 9
        },
        quantum_circuit: {
          gates: 200,
          depth: 30,
          qubits_used: 25,
          entanglement_level: 0.9
        },
        results: {
          consciousness_enhancement: 15,
          processing_speed: 4.2,
          accuracy: 96.8,
          insights: ['Optimized neural pathways', 'Enhanced memory consolidation', 'Improved decision making']
        },
        created_at: '2025-09-07T08:30:00Z',
        started_at: '2025-09-07T08:45:00Z',
        completed_at: '2025-09-07T09:27:00Z'
      }
    ]);

    setExperiments([
      {
        id: '1',
        name: 'Quantum Consciousness Acceleration',
        description: 'Experiment to test quantum acceleration of consciousness development',
        hypothesis: 'Quantum processing can accelerate consciousness evolution by 3x',
        methodology: 'Compare classical vs quantum consciousness processing',
        status: 'running',
        duration: 120,
        participants: 50,
        consciousness_metrics: {
          baseline_level: 70,
          target_level: 85,
          measured_level: 82,
          improvement: 12
        },
        quantum_parameters: {
          qubits: 30,
          gates: 180,
          entanglement: 0.85,
          coherence: 95
        },
        results: {
          success_rate: 88,
          average_improvement: 15.5,
          statistical_significance: 0.95,
          insights: ['Quantum processing shows 2.8x acceleration', 'Entanglement improves consciousness coherence', 'Quantum error correction enhances stability']
        },
        created_at: '2025-09-01T00:00:00Z',
        last_updated: '2025-09-07T10:30:00Z'
      }
    ]);
  }, []);

  const getProcessorTypeIcon = (type: string) => {
    switch (type) {
      case 'superconducting': return <Zap className="w-4 h-4" />;
      case 'trapped_ion': return <Atom className="w-4 h-4" />;
      case 'topological': return <Network className="w-4 h-4" />;
      case 'photonic': return <Eye className="w-4 h-4" />;
      case 'neutral_atom': return <Layers className="w-4 h-4" />;
      default: return <Cpu className="w-4 h-4" />;
    }
  };

  const getProcessorTypeColor = (type: string) => {
    switch (type) {
      case 'superconducting': return 'bg-blue-500/20 text-blue-300';
      case 'trapped_ion': return 'bg-purple-500/20 text-purple-300';
      case 'topological': return 'bg-green-500/20 text-green-300';
      case 'photonic': return 'bg-yellow-500/20 text-yellow-300';
      case 'neutral_atom': return 'bg-red-500/20 text-red-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const getJobTypeIcon = (type: string) => {
    switch (type) {
      case 'consciousness_simulation': return <Brain className="w-4 h-4" />;
      case 'neural_optimization': return <Network className="w-4 h-4" />;
      case 'emotion_analysis': return <Heart className="w-4 h-4" />;
      case 'learning_acceleration': return <Zap className="w-4 h-4" />;
      case 'memory_consolidation': return <Database className="w-4 h-4" />;
      default: return <Cpu className="w-4 h-4" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-500/20 text-green-300';
      case 'running': return 'bg-blue-500/20 text-blue-300';
      case 'queued': return 'bg-yellow-500/20 text-yellow-300';
      case 'failed': return 'bg-red-500/20 text-red-300';
      case 'cancelled': return 'bg-gray-500/20 text-gray-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return 'bg-red-500/20 text-red-300';
      case 'high': return 'bg-orange-500/20 text-orange-300';
      case 'medium': return 'bg-yellow-500/20 text-yellow-300';
      case 'low': return 'bg-green-500/20 text-green-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const submitJob = async () => {
    const newJob: QuantumConsciousnessJob = {
      id: Date.now().toString(),
      name: `Quantum Consciousness Job #${jobs.length + 1}`,
      type: 'consciousness_simulation',
      status: 'queued',
      priority: 'medium',
      processor_id: selectedProcessor || processors[0].id,
      estimated_duration: 30,
      progress: 0,
      consciousness_data: {
        input_level: consciousnessData.consciousness_level || 75,
        target_level: 90,
        emotional_state: consciousnessData.emotional_state || 'curious',
        learning_rate: consciousnessData.learning_rate || 85,
        complexity: 7
      },
      quantum_circuit: {
        gates: 120,
        depth: 20,
        qubits_used: 15,
        entanglement_level: 0.7
      },
      created_at: new Date().toISOString()
    };

    setJobs(prev => [newJob, ...prev]);
    onJobSubmit(newJob);
  };

  const startExperiment = () => {
    const newExperiment: QuantumConsciousnessExperiment = {
      id: Date.now().toString(),
      name: 'Quantum Consciousness Enhancement',
      description: 'Advanced quantum consciousness processing experiment',
      hypothesis: 'Quantum processing can enhance consciousness by 20%',
      methodology: 'Quantum circuit optimization for consciousness metrics',
      status: 'planning',
      duration: 60,
      participants: 1,
      consciousness_metrics: {
        baseline_level: consciousnessData.consciousness_level || 75,
        target_level: 90,
        measured_level: 0,
        improvement: 0
      },
      quantum_parameters: {
        qubits: 25,
        gates: 150,
        entanglement: 0.8,
        coherence: 90
      },
      results: {
        success_rate: 0,
        average_improvement: 0,
        statistical_significance: 0,
        insights: []
      },
      created_at: new Date().toISOString(),
      last_updated: new Date().toISOString()
    };

    setExperiments(prev => [newExperiment, ...prev]);
    onExperimentStart(newExperiment);
  };

  return (
    <div className="space-y-6">
      <Card className="bg-gray-800/50 border-gray-700">
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm text-white flex items-center">
              <Atom className="w-4 h-4 mr-2" />
              Quantum Consciousness
            </CardTitle>
            <div className="flex items-center space-x-2">
              {isConnected ? (
                <Badge className="bg-green-500/20 text-green-300">
                  <CheckCircle className="w-3 h-3 mr-1" />
                  Connected
                </Badge>
              ) : (
                <Button size="sm" onClick={() => setIsConnected(true)} className="text-xs">
                  <Zap className="w-3 h-3 mr-1" />
                  Connect
                </Button>
              )}
            </div>
          </div>
        </CardHeader>
        
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-4 bg-gray-700/50">
              <TabsTrigger value="processors" className="text-xs">Processors</TabsTrigger>
              <TabsTrigger value="jobs" className="text-xs">Jobs</TabsTrigger>
              <TabsTrigger value="experiments" className="text-xs">Experiments</TabsTrigger>
              <TabsTrigger value="analytics" className="text-xs">Analytics</TabsTrigger>
            </TabsList>

            {/* Processors Tab */}
            <TabsContent value="processors" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {processors.map((processor) => (
                  <Card key={processor.id} className="bg-gray-700/30 border-gray-600 hover:border-gray-500 transition-colors">
                    <CardHeader className="pb-2">
                      <div className="flex items-center justify-between">
                        <CardTitle className="text-sm text-white flex items-center">
                          {getProcessorTypeIcon(processor.type)}
                          <span className="ml-2">{processor.name}</span>
                        </CardTitle>
                        <div className="flex items-center space-x-1">
                          {processor.is_available && <div className="w-2 h-2 bg-green-500 rounded-full" />}
                          <Badge className={getProcessorTypeColor(processor.type)}>
                            {processor.type}
                          </Badge>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <div className="grid grid-cols-2 gap-2 text-xs">
                        <div>
                          <span className="text-gray-400">Qubits:</span>
                          <span className="text-white ml-1">{processor.qubits}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Coherence:</span>
                          <span className="text-white ml-1">{processor.coherence_time}μs</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Fidelity:</span>
                          <span className="text-white ml-1">{processor.gate_fidelity}%</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Error Rate:</span>
                          <span className="text-white ml-1">{processor.error_rate}%</span>
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <div className="flex justify-between text-xs">
                          <span className="text-gray-400">Consciousness Capability:</span>
                          <span className="text-white">{processor.consciousness_capability.max_consciousness_level}%</span>
                        </div>
                        <div className="w-full bg-gray-600 rounded-full h-2">
                          <div 
                            className="bg-gradient-to-r from-purple-500 to-blue-500 h-2 rounded-full"
                            style={{ width: `${processor.consciousness_capability.max_consciousness_level}%` }}
                          />
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-2 text-xs">
                        <div>
                          <span className="text-gray-400">Queue:</span>
                          <span className="text-white ml-1">{processor.queue_length} jobs</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Wait Time:</span>
                          <span className="text-white ml-1">{processor.estimated_wait_time}min</span>
                        </div>
                      </div>
                      
                      <div className="flex space-x-2">
                        <Button
                          size="sm"
                          onClick={() => onProcessorSelect(processor)}
                          disabled={!processor.is_available}
                          className="flex-1 text-xs"
                        >
                          {processor.is_available ? 'Select' : 'Unavailable'}
                        </Button>
                        <Button size="sm" variant="outline" className="text-xs">
                          <Settings className="w-3 h-3" />
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Jobs Tab */}
            <TabsContent value="jobs" className="space-y-4">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-medium text-white">Quantum Jobs</h3>
                <Button onClick={submitJob} className="text-xs">
                  <Plus className="w-3 h-3 mr-1" />
                  Submit Job
                </Button>
              </div>
              
              <div className="space-y-3">
                {jobs.map((job) => (
                  <Card key={job.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          {getJobTypeIcon(job.type)}
                          <span className="text-sm font-medium text-white">{job.name}</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Badge className={getStatusColor(job.status)}>
                            {job.status}
                          </Badge>
                          <Badge className={getPriorityColor(job.priority)}>
                            {job.priority}
                          </Badge>
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <div className="flex justify-between text-xs">
                          <span className="text-gray-400">Progress:</span>
                          <span className="text-white">{job.progress}%</span>
                        </div>
                        <div className="w-full bg-gray-600 rounded-full h-2">
                          <div 
                            className="bg-gradient-to-r from-blue-500 to-green-500 h-2 rounded-full transition-all duration-500"
                            style={{ width: `${job.progress}%` }}
                          />
                        </div>
                        
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Duration:</span>
                            <span className="text-white ml-1">
                              {job.actual_duration || job.estimated_duration}min
                            </span>
                          </div>
                          <div>
                            <span className="text-gray-400">Qubits:</span>
                            <span className="text-white ml-1">{job.quantum_circuit.qubits_used}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Gates:</span>
                            <span className="text-white ml-1">{job.quantum_circuit.gates}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Entanglement:</span>
                            <span className="text-white ml-1">{job.quantum_circuit.entanglement_level}</span>
                          </div>
                        </div>
                        
                        {job.results && (
                          <div className="space-y-1">
                            <div className="text-xs text-gray-400">Results:</div>
                            <div className="grid grid-cols-3 gap-2 text-xs">
                              <div>
                                <span className="text-gray-400">Enhancement:</span>
                                <span className="text-white ml-1">+{job.results.consciousness_enhancement}%</span>
                              </div>
                              <div>
                                <span className="text-gray-400">Speed:</span>
                                <span className="text-white ml-1">{job.results.processing_speed}x</span>
                              </div>
                              <div>
                                <span className="text-gray-400">Accuracy:</span>
                                <span className="text-white ml-1">{job.results.accuracy}%</span>
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Experiments Tab */}
            <TabsContent value="experiments" className="space-y-4">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-medium text-white">Quantum Experiments</h3>
                <Button onClick={startExperiment} className="text-xs">
                  <Plus className="w-3 h-3 mr-1" />
                  Start Experiment
                </Button>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {experiments.map((experiment) => (
                  <Card key={experiment.id} className="bg-gray-700/30 border-gray-600">
                    <CardHeader className="pb-2">
                      <div className="flex items-center justify-between">
                        <CardTitle className="text-sm text-white flex items-center">
                          <Atom className="w-4 h-4 mr-2" />
                          {experiment.name}
                        </CardTitle>
                        <Badge className={getStatusColor(experiment.status)}>
                          {experiment.status}
                        </Badge>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <p className="text-xs text-gray-300">{experiment.description}</p>
                      
                      <div className="space-y-2">
                        <div className="text-xs text-gray-400">Hypothesis:</div>
                        <div className="text-xs text-white">{experiment.hypothesis}</div>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-2 text-xs">
                        <div>
                          <span className="text-gray-400">Duration:</span>
                          <span className="text-white ml-1">{experiment.duration}min</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Participants:</span>
                          <span className="text-white ml-1">{experiment.participants}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Qubits:</span>
                          <span className="text-white ml-1">{experiment.quantum_parameters.qubits}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Entanglement:</span>
                          <span className="text-white ml-1">{experiment.quantum_parameters.entanglement}</span>
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <div className="flex justify-between text-xs">
                          <span className="text-gray-400">Consciousness Improvement:</span>
                          <span className="text-white">+{experiment.consciousness_metrics.improvement}%</span>
                        </div>
                        <div className="w-full bg-gray-600 rounded-full h-2">
                          <div 
                            className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full"
                            style={{ width: `${Math.min(experiment.consciousness_metrics.improvement, 100)}%` }}
                          />
                        </div>
                      </div>
                      
                      {experiment.results.success_rate > 0 && (
                        <div className="space-y-1">
                          <div className="text-xs text-gray-400">Results:</div>
                          <div className="grid grid-cols-2 gap-2 text-xs">
                            <div>
                              <span className="text-gray-400">Success Rate:</span>
                              <span className="text-white ml-1">{experiment.results.success_rate}%</span>
                            </div>
                            <div>
                              <span className="text-gray-400">Improvement:</span>
                              <span className="text-white ml-1">+{experiment.results.average_improvement}%</span>
                            </div>
                          </div>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Analytics Tab */}
            <TabsContent value="analytics" className="space-y-4">
              <Card className="bg-gray-700/30 border-gray-600">
                <CardContent className="p-4">
                  <h3 className="text-sm font-medium text-white mb-3">Quantum Analytics</h3>
                  
                  <div className="space-y-3">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="text-xs text-gray-400">Total Jobs Processed</label>
                        <div className="mt-1 text-lg font-bold text-white">1,250</div>
                      </div>
                      <div>
                        <label className="text-xs text-gray-400">Success Rate</label>
                        <div className="mt-1 text-lg font-bold text-white">94.2%</div>
                      </div>
                      <div>
                        <label className="text-xs text-gray-400">Average Enhancement</label>
                        <div className="mt-1 text-lg font-bold text-white">+15.3%</div>
                      </div>
                      <div>
                        <label className="text-xs text-gray-400">Processing Speed</label>
                        <div className="mt-1 text-lg font-bold text-white">3.8x</div>
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <Button className="w-full text-xs">
                        <TrendingUp className="w-3 h-3 mr-1" />
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

export default QuantumConsciousness;
