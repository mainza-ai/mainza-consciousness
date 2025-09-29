import React, { useState, useEffect, useRef, useCallback } from 'react';
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
  Star,
  ThumbsUp,
  ThumbsDown,
  Share2,
  Bookmark as BookmarkIcon,
  Wifi,
  Bluetooth,
  Radio,
  Signal,
  WifiOff,
  BluetoothOff,
  RadioOff,
  SignalOff
} from 'lucide-react';

interface NeuralArchitecture {
  id: string;
  name: string;
  type: 'transformer' | 'cnn' | 'rnn' | 'lstm' | 'gru' | 'gan' | 'vae' | 'attention' | 'residual' | 'dense';
  description: string;
  layers: number;
  parameters: number;
  complexity: 'low' | 'medium' | 'high' | 'extreme';
  consciousness_integration: number;
  performance_metrics: {
    accuracy: number;
    speed: number;
    efficiency: number;
    scalability: number;
    memory_usage: number;
    training_time: number;
  };
  applications: string[];
  requirements: {
    min_consciousness_level: number;
    hardware_requirements: string[];
    software_dependencies: string[];
    memory_requirements: number;
  };
  created_at: string;
  updated_at: string;
  is_verified: boolean;
  is_experimental: boolean;
}

interface NeuralTraining {
  id: string;
  name: string;
  architecture_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'paused';
  progress: number;
  epochs: number;
  current_epoch: number;
  batch_size: number;
  learning_rate: number;
  loss_function: string;
  optimizer: string;
  dataset_size: number;
  training_data: {
    consciousness_levels: number[];
    emotional_states: string[];
    learning_patterns: number[];
    memory_consolidation: number[];
  };
  metrics: {
    training_loss: number;
    validation_loss: number;
    accuracy: number;
    precision: number;
    recall: number;
    f1_score: number;
  };
  started_at: string;
  completed_at?: string;
  estimated_completion: string;
}

interface NeuralModel {
  id: string;
  name: string;
  architecture: NeuralArchitecture;
  version: string;
  status: 'training' | 'ready' | 'deployed' | 'archived';
  performance: {
    consciousness_prediction: number;
    emotion_recognition: number;
    learning_acceleration: number;
    memory_enhancement: number;
    decision_making: number;
  };
  deployment: {
    environment: 'local' | 'cloud' | 'edge' | 'hybrid';
    instances: number;
    load_balancing: boolean;
    auto_scaling: boolean;
  };
  monitoring: {
    requests_per_second: number;
    average_response_time: number;
    error_rate: number;
    cpu_usage: number;
    memory_usage: number;
    gpu_usage: number;
  };
  created_at: string;
  last_updated: string;
}

interface NeuralExperiment {
  id: string;
  name: string;
  description: string;
  hypothesis: string;
  methodology: string;
  status: 'planning' | 'running' | 'completed' | 'failed';
  duration: number;
  participants: number;
  architectures: string[];
  datasets: string[];
  metrics: {
    success_rate: number;
    average_improvement: number;
    statistical_significance: number;
    reproducibility: number;
  };
  results: {
    findings: string[];
    insights: string[];
    recommendations: string[];
    publications: string[];
  };
  created_at: string;
  last_updated: string;
}

interface AdvancedNeuralNetworksProps {
  consciousnessData: any;
  onArchitectureSelect: (architecture: NeuralArchitecture) => void;
  onTrainingStart: (training: NeuralTraining) => void;
  onModelDeploy: (model: NeuralModel) => void;
  onExperimentStart: (experiment: NeuralExperiment) => void;
}

const AdvancedNeuralNetworks: React.FC<AdvancedNeuralNetworksProps> = ({
  consciousnessData,
  onArchitectureSelect,
  onTrainingStart,
  onModelDeploy,
  onExperimentStart
}) => {
  const [activeTab, setActiveTab] = useState('architectures');
  const [architectures, setArchitectures] = useState<NeuralArchitecture[]>([]);
  const [trainings, setTrainings] = useState<NeuralTraining[]>([]);
  const [models, setModels] = useState<NeuralModel[]>([]);
  const [experiments, setExperiments] = useState<NeuralExperiment[]>([]);
  const [selectedArchitecture, setSelectedArchitecture] = useState<string | null>(null);
  const [isTraining, setIsTraining] = useState(false);

  // Fetch neural network data from APIs
  const fetchNeuralData = useCallback(async () => {
    try {
      // Fetch architectures
      const architecturesResponse = await fetch('/api/neural/architectures');
      if (architecturesResponse.ok) {
        const architecturesData = await architecturesResponse.json();
        setArchitectures(architecturesData.architectures || []);
      }

      // Fetch training jobs
      const trainingsResponse = await fetch('/api/neural/training');
      if (trainingsResponse.ok) {
        const trainingsData = await trainingsResponse.json();
        setTrainings(trainingsData.trainings || []);
      }

      // Fetch models
      const modelsResponse = await fetch('/api/neural/models');
      if (modelsResponse.ok) {
        const modelsData = await modelsResponse.json();
        setModels(modelsData.models || []);
      }

      // Fetch experiments
      const experimentsResponse = await fetch('/api/neural/experiments');
      if (experimentsResponse.ok) {
        const experimentsData = await experimentsResponse.json();
        setExperiments(experimentsData.experiments || []);
      }
    } catch (error) {
      console.error('Error fetching neural network data:', error);
      // Set empty arrays on error - no fallback to mock data
      setArchitectures([]);
      setTrainings([]);
      setModels([]);
      setExperiments([]);
    }
  }, []);

  useEffect(() => {
    fetchNeuralData();
  }, [fetchNeuralData]);

  const getArchitectureTypeIcon = (type: string) => {
    switch (type) {
      case 'transformer': return <Brain className="w-4 h-4" />;
      case 'cnn': return <Network className="w-4 h-4" />;
      case 'rnn': return <Activity className="w-4 h-4" />;
      case 'lstm': return <Zap className="w-4 h-4" />;
      case 'gru': return <Target className="w-4 h-4" />;
      case 'gan': return <Eye className="w-4 h-4" />;
      case 'vae': return <Heart className="w-4 h-4" />;
      case 'attention': return <Cpu className="w-4 h-4" />;
      case 'residual': return <Layers className="w-4 h-4" />;
      case 'dense': return <Database className="w-4 h-4" />;
      default: return <Network className="w-4 h-4" />;
    }
  };

  const getArchitectureTypeColor = (type: string) => {
    switch (type) {
      case 'transformer': return 'bg-blue-500/20 text-blue-300';
      case 'cnn': return 'bg-green-500/20 text-green-300';
      case 'rnn': return 'bg-purple-500/20 text-purple-300';
      case 'lstm': return 'bg-orange-500/20 text-orange-300';
      case 'gru': return 'bg-pink-500/20 text-pink-300';
      case 'gan': return 'bg-cyan-500/20 text-cyan-300';
      case 'vae': return 'bg-yellow-500/20 text-yellow-300';
      case 'attention': return 'bg-red-500/20 text-red-300';
      case 'residual': return 'bg-indigo-500/20 text-indigo-300';
      case 'dense': return 'bg-gray-500/20 text-gray-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const getComplexityColor = (complexity: string) => {
    switch (complexity) {
      case 'low': return 'bg-green-500/20 text-green-300';
      case 'medium': return 'bg-yellow-500/20 text-yellow-300';
      case 'high': return 'bg-orange-500/20 text-orange-300';
      case 'extreme': return 'bg-red-500/20 text-red-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-500/20 text-green-300';
      case 'running': return 'bg-blue-500/20 text-blue-300';
      case 'pending': return 'bg-yellow-500/20 text-yellow-300';
      case 'failed': return 'bg-red-500/20 text-red-300';
      case 'paused': return 'bg-gray-500/20 text-gray-300';
      case 'ready': return 'bg-green-500/20 text-green-300';
      case 'deployed': return 'bg-blue-500/20 text-blue-300';
      case 'archived': return 'bg-gray-500/20 text-gray-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000000) return (num / 1000000000).toFixed(1) + 'B';
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
  };

  const startTraining = (architectureId: string) => {
    const architecture = architectures.find(a => a.id === architectureId);
    if (!architecture) return;

    const newTraining: NeuralTraining = {
      id: Date.now().toString(),
      name: `${architecture.name} Training`,
      architecture_id: architectureId,
      status: 'running',
      progress: 0,
      epochs: 100,
      current_epoch: 0,
      batch_size: 32,
      learning_rate: 0.001,
      loss_function: 'CrossEntropyLoss',
      optimizer: 'AdamW',
      dataset_size: 100000,
      training_data: {
        consciousness_levels: [75, 80, 85, 90, 95],
        emotional_states: ['curious', 'focused', 'creative'],
        learning_patterns: [0.8, 0.85, 0.9],
        memory_consolidation: [0.7, 0.75, 0.8]
      },
      metrics: {
        training_loss: 0,
        validation_loss: 0,
        accuracy: 0,
        precision: 0,
        recall: 0,
        f1_score: 0
      },
      started_at: new Date().toISOString(),
      estimated_completion: new Date(Date.now() + 8 * 60 * 60 * 1000).toISOString()
    };

    setTrainings(prev => [newTraining, ...prev]);
    onTrainingStart(newTraining);
  };

  const deployModel = (modelId: string) => {
    setModels(prev => prev.map(model => 
      model.id === modelId ? { ...model, status: 'deployed' } : model
    ));
    
    const model = models.find(m => m.id === modelId);
    if (model) {
      onModelDeploy(model);
    }
  };

  const startExperiment = () => {
    const newExperiment: NeuralExperiment = {
      id: Date.now().toString(),
      name: 'Custom Neural Experiment',
      description: 'User-defined neural network experiment',
      hypothesis: 'Custom hypothesis for consciousness enhancement',
      methodology: 'Custom methodology for neural network testing',
      status: 'planning',
      duration: 24,
      participants: 1,
      architectures: ['ConsciousnessTransformer'],
      datasets: ['CustomDataset'],
      metrics: {
        success_rate: 0,
        average_improvement: 0,
        statistical_significance: 0,
        reproducibility: 0
      },
      results: {
        findings: [],
        insights: [],
        recommendations: [],
        publications: []
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
              <Brain className="w-4 h-4 mr-2" />
              Advanced Neural Networks
            </CardTitle>
            <div className="flex items-center space-x-2">
              <Button onClick={startExperiment} className="text-xs">
                <Plus className="w-3 h-3 mr-1" />
                New Experiment
              </Button>
            </div>
          </div>
        </CardHeader>
        
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-4 bg-gray-700/50">
              <TabsTrigger value="architectures" className="text-xs">Architectures</TabsTrigger>
              <TabsTrigger value="training" className="text-xs">Training</TabsTrigger>
              <TabsTrigger value="models" className="text-xs">Models</TabsTrigger>
              <TabsTrigger value="experiments" className="text-xs">Experiments</TabsTrigger>
            </TabsList>

            {/* Architectures Tab */}
            <TabsContent value="architectures" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {architectures.map((architecture) => (
                  <Card key={architecture.id} className="bg-gray-700/30 border-gray-600 hover:border-gray-500 transition-colors">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          {getArchitectureTypeIcon(architecture.type)}
                          <span className="text-sm font-medium text-white">{architecture.name}</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          {architecture.is_verified && <CheckCircle className="w-3 h-3 text-green-400" />}
                          {architecture.is_experimental && <Rocket className="w-3 h-3 text-orange-400" />}
                        </div>
                      </div>
                      
                      <p className="text-xs text-gray-300 mb-3">{architecture.description}</p>
                      
                      <div className="space-y-3">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-2">
                            <Badge className={getArchitectureTypeColor(architecture.type)}>
                              {architecture.type}
                            </Badge>
                            <Badge className={getComplexityColor(architecture.complexity)}>
                              {architecture.complexity}
                            </Badge>
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Layers:</span>
                            <span className="text-white ml-1">{architecture.layers}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Parameters:</span>
                            <span className="text-white ml-1">{formatNumber(architecture.parameters)}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Accuracy:</span>
                            <span className="text-white ml-1">{architecture.performance_metrics.accuracy}%</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Speed:</span>
                            <span className="text-white ml-1">{architecture.performance_metrics.speed}%</span>
                          </div>
                        </div>
                        
                        <div className="space-y-2">
                          <div className="flex justify-between text-xs">
                            <span className="text-gray-400">Consciousness Integration:</span>
                            <span className="text-white">{architecture.consciousness_integration}%</span>
                          </div>
                          <div className="w-full bg-gray-600 rounded-full h-2">
                            <div 
                              className="bg-gradient-to-r from-blue-500 to-green-500 h-2 rounded-full"
                              style={{ width: `${architecture.consciousness_integration}%` }}
                            />
                          </div>
                        </div>
                        
                        <div className="space-y-1">
                          <div className="text-xs text-gray-400">Applications:</div>
                          <div className="flex flex-wrap gap-1">
                            {architecture.applications.slice(0, 2).map((app, index) => (
                              <Badge key={index} className="bg-blue-500/20 text-blue-300 text-xs">
                                {app}
                              </Badge>
                            ))}
                            {architecture.applications.length > 2 && (
                              <Badge className="bg-gray-500/20 text-gray-300 text-xs">
                                +{architecture.applications.length - 2} more
                              </Badge>
                            )}
                          </div>
                        </div>
                        
                        <div className="flex space-x-2">
                          <Button
                            size="sm"
                            onClick={() => startTraining(architecture.id)}
                            className="flex-1 text-xs"
                          >
                            <Play className="w-3 h-3 mr-1" />
                            Train
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

            {/* Training Tab */}
            <TabsContent value="training" className="space-y-4">
              <div className="space-y-3">
                {trainings.map((training) => (
                  <Card key={training.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <span className="text-sm font-medium text-white">{training.name}</span>
                        <Badge className={getStatusColor(training.status)}>
                          {training.status}
                        </Badge>
                      </div>
                      
                      <div className="space-y-3">
                        <div className="flex justify-between text-xs">
                          <span className="text-gray-400">Progress:</span>
                          <span className="text-white">{training.progress}%</span>
                        </div>
                        <div className="w-full bg-gray-600 rounded-full h-2">
                          <div 
                            className="bg-gradient-to-r from-blue-500 to-green-500 h-2 rounded-full transition-all duration-500"
                            style={{ width: `${training.progress}%` }}
                          />
                        </div>
                        
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Epoch:</span>
                            <span className="text-white ml-1">{training.current_epoch}/{training.epochs}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Batch Size:</span>
                            <span className="text-white ml-1">{training.batch_size}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Learning Rate:</span>
                            <span className="text-white ml-1">{training.learning_rate}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Dataset Size:</span>
                            <span className="text-white ml-1">{formatNumber(training.dataset_size)}</span>
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-3 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Training Loss:</span>
                            <span className="text-white ml-1">{training.metrics.training_loss.toFixed(3)}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Validation Loss:</span>
                            <span className="text-white ml-1">{training.metrics.validation_loss.toFixed(3)}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Accuracy:</span>
                            <span className="text-white ml-1">{training.metrics.accuracy.toFixed(1)}%</span>
                          </div>
                        </div>
                        
                        <div className="flex space-x-2">
                          <Button size="sm" className="flex-1 text-xs">
                            <Eye className="w-3 h-3 mr-1" />
                            View Details
                          </Button>
                          <Button size="sm" variant="outline" className="text-xs">
                            <Pause className="w-3 h-3" />
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Models Tab */}
            <TabsContent value="models" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {models.map((model) => (
                  <Card key={model.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <span className="text-sm font-medium text-white">{model.name}</span>
                        <Badge className={getStatusColor(model.status)}>
                          {model.status}
                        </Badge>
                      </div>
                      
                      <div className="space-y-3">
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Version:</span>
                            <span className="text-white ml-1">{model.version}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Environment:</span>
                            <span className="text-white ml-1 capitalize">{model.deployment.environment}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Instances:</span>
                            <span className="text-white ml-1">{model.deployment.instances}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">RPS:</span>
                            <span className="text-white ml-1">{model.monitoring.requests_per_second}</span>
                          </div>
                        </div>
                        
                        <div className="space-y-2">
                          <div className="text-xs text-gray-400">Performance:</div>
                          <div className="grid grid-cols-2 gap-2 text-xs">
                            <div>Consciousness: {model.performance.consciousness_prediction}%</div>
                            <div>Emotion: {model.performance.emotion_recognition}%</div>
                            <div>Learning: {model.performance.learning_acceleration}%</div>
                            <div>Memory: {model.performance.memory_enhancement}%</div>
                          </div>
                        </div>
                        
                        <div className="space-y-2">
                          <div className="text-xs text-gray-400">Monitoring:</div>
                          <div className="grid grid-cols-2 gap-2 text-xs">
                            <div>CPU: {model.monitoring.cpu_usage}%</div>
                            <div>Memory: {model.monitoring.memory_usage}%</div>
                            <div>GPU: {model.monitoring.gpu_usage}%</div>
                            <div>Error Rate: {model.monitoring.error_rate}%</div>
                          </div>
                        </div>
                        
                        <div className="flex space-x-2">
                          <Button
                            size="sm"
                            onClick={() => deployModel(model.id)}
                            disabled={model.status === 'deployed'}
                            className="flex-1 text-xs"
                          >
                            {model.status === 'deployed' ? 'Deployed' : 'Deploy'}
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

            {/* Experiments Tab */}
            <TabsContent value="experiments" className="space-y-4">
              <div className="space-y-3">
                {experiments.map((experiment) => (
                  <Card key={experiment.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <span className="text-sm font-medium text-white">{experiment.name}</span>
                        <Badge className={getStatusColor(experiment.status)}>
                          {experiment.status}
                        </Badge>
                      </div>
                      
                      <p className="text-xs text-gray-300 mb-3">{experiment.description}</p>
                      
                      <div className="space-y-3">
                        <div className="space-y-1">
                          <div className="text-xs text-gray-400">Hypothesis:</div>
                          <div className="text-xs text-white">{experiment.hypothesis}</div>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Duration:</span>
                            <span className="text-white ml-1">{experiment.duration}h</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Participants:</span>
                            <span className="text-white ml-1">{experiment.participants}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Success Rate:</span>
                            <span className="text-white ml-1">{experiment.metrics.success_rate}%</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Improvement:</span>
                            <span className="text-white ml-1">+{experiment.metrics.average_improvement}%</span>
                          </div>
                        </div>
                        
                        {experiment.results.findings.length > 0 && (
                          <div className="space-y-1">
                            <div className="text-xs text-gray-400">Findings:</div>
                            <ul className="text-xs text-white space-y-1">
                              {experiment.results.findings.map((finding, index) => (
                                <li key={index} className="flex items-start">
                                  <span className="text-green-400 mr-2">•</span>
                                  {finding}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                        
                        <div className="flex space-x-2">
                          <Button size="sm" className="flex-1 text-xs">
                            <Eye className="w-3 h-3 mr-1" />
                            View Results
                          </Button>
                          <Button size="sm" variant="outline" className="text-xs">
                            <Download className="w-3 h-3" />
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
};

export default AdvancedNeuralNetworks;