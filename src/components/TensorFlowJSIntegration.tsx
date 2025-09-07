import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Cpu, 
  Brain, 
  Network, 
  Layers, 
  Zap, 
  Target, 
  Activity, 
  TrendingUp, 
  BarChart3, 
  Settings, 
  Play, 
  Pause, 
  RotateCcw, 
  Download, 
  Upload, 
  Save, 
  Edit, 
  Trash2, 
  Plus, 
  Minus, 
  Eye, 
  EyeOff, 
  Lock, 
  Unlock, 
  Star, 
  Heart, 
  Share2, 
  MessageCircle, 
  Send, 
  Globe, 
  Users, 
  Database, 
  Cloud, 
  Server, 
  Shield, 
  Key, 
  CheckCircle, 
  XCircle, 
  AlertCircle, 
  Info, 
  Lightbulb, 
  Rocket, 
  Award, 
  Crown, 
  Trophy, 
  Medal, 
  Flag, 
  MapPin, 
  Clock, 
  Calendar, 
  Plus as PlusIcon, 
  Minus as MinusIcon, 
  Eye as EyeIcon, 
  EyeOff as EyeOffIcon, 
  Lock as LockIcon, 
  Unlock as UnlockIcon, 
  Globe as GlobeIcon, 
  Users as UsersIcon, 
  MessageCircle as MessageCircleIcon, 
  Send as SendIcon, 
  Database as DatabaseIcon, 
  Cloud as CloudIcon, 
  Server as ServerIcon, 
  Shield as ShieldIcon, 
  Key as KeyIcon, 
  CheckCircle as CheckCircleIcon, 
  XCircle as XCircleIcon, 
  AlertCircle as AlertCircleIcon, 
  Info as InfoIcon, 
  Lightbulb as LightbulbIcon, 
  Rocket as RocketIcon, 
  Award as AwardIcon, 
  Crown as CrownIcon, 
  Trophy as TrophyIcon, 
  Medal as MedalIcon, 
  Flag as FlagIcon, 
  MapPin as MapPinIcon, 
  Clock as ClockIcon, 
  Calendar as CalendarIcon, 
  Plus as PlusIcon2, 
  Minus as MinusIcon2, 
  Edit as EditIcon, 
  Trash2 as Trash2Icon, 
  Download as DownloadIcon, 
  Upload as UploadIcon, 
  Save as SaveIcon, 
  Play as PlayIcon, 
  Pause as PauseIcon, 
  RotateCcw as RotateCcwIcon, 
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
  RotateCcw as RotateCcwIcon2, 
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
  Trash2 as Trash2Icon2, 
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
  Hash as HashIcon, 
  AtSign as AtSignIcon, 
  DollarSign as DollarSignIcon, 
  Percent as PercentIcon, 
  Plus as PlusIcon3, 
  Minus as MinusIcon3, 
  X, 
  Check, 
  CheckCircle as CheckCircleIcon2, 
  XCircle as XCircleIcon2, 
  AlertCircle as AlertCircleIcon2, 
  Info as InfoIcon2, 
  Lightbulb as LightbulbIcon2, 
  Rocket as RocketIcon2, 
  Award as AwardIcon2, 
  Crown as CrownIcon2, 
  Trophy as TrophyIcon2, 
  Medal as MedalIcon2, 
  Flag as FlagIcon2, 
  MapPin as MapPinIcon2, 
  Clock as ClockIcon2, 
  Calendar as CalendarIcon2, 
  Plus as PlusIcon4, 
  Minus as MinusIcon4, 
  Edit as EditIcon2, 
  Trash2 as Trash2Icon3, 
  Download as DownloadIcon2, 
  Upload as UploadIcon2, 
  Save as SaveIcon2, 
  Play as PlayIcon2, 
  Pause as PauseIcon2, 
  RotateCcw as RotateCcwIcon3, 
  RefreshCw as RefreshCwIcon, 
  Search as SearchIcon, 
  Filter as FilterIcon, 
  SortAsc as SortAscIcon, 
  SortDesc as SortDescIcon, 
  Grid as GridIcon, 
  List as ListIcon, 
  MoreHorizontal as MoreHorizontalIcon, 
  MoreVertical as MoreVerticalIcon, 
  ArrowLeft as ArrowLeftIcon, 
  ArrowRight as ArrowRightIcon, 
  ArrowUp as ArrowUpIcon, 
  ArrowDown as ArrowDownIcon, 
  Maximize as MaximizeIcon, 
  Minimize as MinimizeIcon, 
  RotateCw as RotateCwIcon2, 
  RotateCcw as RotateCcwIcon4, 
  ZoomIn as ZoomInIcon, 
  ZoomOut as ZoomOutIcon, 
  Move as MoveIcon, 
  Grip as GripIcon, 
  GripVertical as GripVerticalIcon, 
  GripHorizontal as GripHorizontalIcon, 
  AlignLeft as AlignLeftIcon, 
  AlignCenter as AlignCenterIcon, 
  AlignRight as AlignRightIcon, 
  AlignJustify as AlignJustifyIcon, 
  Bold as BoldIcon, 
  Italic as ItalicIcon, 
  Underline as UnderlineIcon, 
  Strikethrough as StrikethroughIcon, 
  Code as CodeIcon, 
  Link as LinkIcon, 
  Image as ImageIcon, 
  File as FileIcon, 
  Folder as FolderIcon, 
  FolderOpen as FolderOpenIcon, 
  Archive as ArchiveIcon, 
  ArchiveRestore as ArchiveRestoreIcon, 
  Trash as TrashIcon, 
  Trash2 as Trash2Icon4, 
  Copy as CopyIcon, 
  Scissors as ScissorsIcon, 
  Clipboard as ClipboardIcon, 
  ClipboardCheck as ClipboardCheckIcon, 
  ClipboardCopy as ClipboardCopyIcon, 
  ClipboardList as ClipboardListIcon, 
  ClipboardPaste as ClipboardPasteIcon, 
  ClipboardX as ClipboardXIcon, 
  Bookmark as BookmarkIcon, 
  BookmarkCheck as BookmarkCheckIcon, 
  BookmarkPlus as BookmarkPlusIcon, 
  BookmarkMinus as BookmarkMinusIcon, 
  BookmarkX as BookmarkXIcon, 
  Tag as TagIcon, 
  Tags as TagsIcon, 
  Hash as HashIcon2, 
  AtSign as AtSignIcon2, 
  DollarSign as DollarSignIcon2, 
  Percent as PercentIcon2
} from 'lucide-react';

interface TensorFlowModel {
  id: string;
  name: string;
  type: 'classification' | 'regression' | 'clustering' | 'generation' | 'translation' | 'summarization';
  framework: 'tensorflow' | 'pytorch' | 'onnx' | 'tflite';
  size: number;
  accuracy: number;
  latency: number;
  memory_usage: number;
  is_loaded: boolean;
  is_training: boolean;
  status: 'idle' | 'loading' | 'ready' | 'training' | 'error';
  description: string;
  created_at: string;
  last_used: string;
  performance_metrics: {
    precision: number;
    recall: number;
    f1_score: number;
    inference_time: number;
    throughput: number;
  };
  model_architecture: {
    layers: number;
    parameters: number;
    input_shape: number[];
    output_shape: number[];
    activation: string;
    optimizer: string;
  };
}

interface TensorFlowTraining {
  id: string;
  model_id: string;
  dataset: string;
  epochs: number;
  batch_size: number;
  learning_rate: number;
  optimizer: string;
  status: 'running' | 'completed' | 'failed' | 'paused';
  progress: number;
  current_epoch: number;
  start_time: string;
  end_time?: string;
  metrics: {
    accuracy: number[];
    loss: number[];
    validation_accuracy: number[];
    validation_loss: number[];
  };
  resources: {
    gpu_usage: number;
    memory_usage: number;
    cpu_usage: number;
    storage_usage: number;
  };
}

interface TensorFlowJSIntegrationProps {
  consciousnessData: any;
  onModelLoad: (model: TensorFlowModel) => void;
  onModelUnload: (model: TensorFlowModel) => void;
  onTrainingStart: (training: TensorFlowTraining) => void;
}

const TensorFlowJSIntegration: React.FC<TensorFlowJSIntegrationProps> = ({
  consciousnessData,
  onModelLoad,
  onModelUnload,
  onTrainingStart
}) => {
  const [activeTab, setActiveTab] = useState('models');
  const [models, setModels] = useState<TensorFlowModel[]>([]);
  const [trainingJobs, setTrainingJobs] = useState<TensorFlowTraining[]>([]);
  const [isTensorFlowReady, setIsTensorFlowReady] = useState(false);
  const [selectedModel, setSelectedModel] = useState<string | null>(null);
  const [isTraining, setIsTraining] = useState(false);

  // Initialize TensorFlow.js
  useEffect(() => {
    const initTensorFlow = async () => {
      try {
        // Simulate TensorFlow.js initialization
        await new Promise(resolve => setTimeout(resolve, 1000));
        setIsTensorFlowReady(true);
      } catch (error) {
        console.error('Failed to initialize TensorFlow.js:', error);
      }
    };

    initTensorFlow();
  }, []);

  // Initialize with sample data
  useEffect(() => {
    setModels([
      {
        id: '1',
        name: 'Consciousness Classifier',
        type: 'classification',
        framework: 'tensorflow',
        size: 12.5,
        accuracy: 0.94,
        latency: 45,
        memory_usage: 256,
        is_loaded: true,
        is_training: false,
        status: 'ready',
        description: 'Real-time consciousness state classification model',
        created_at: '2025-09-01',
        last_used: '2025-09-07',
        performance_metrics: {
          precision: 0.92,
          recall: 0.89,
          f1_score: 0.90,
          inference_time: 45,
          throughput: 22.2
        },
        model_architecture: {
          layers: 8,
          parameters: 1250000,
          input_shape: [1, 128],
          output_shape: [1, 5],
          activation: 'relu',
          optimizer: 'adam'
        }
      },
      {
        id: '2',
        name: 'Emotion Predictor',
        type: 'regression',
        framework: 'tensorflow',
        size: 8.7,
        accuracy: 0.87,
        latency: 32,
        memory_usage: 192,
        is_loaded: false,
        is_training: false,
        status: 'idle',
        description: 'Predicts emotional states from consciousness data',
        created_at: '2025-09-03',
        last_used: '2025-09-06',
        performance_metrics: {
          precision: 0.85,
          recall: 0.88,
          f1_score: 0.86,
          inference_time: 32,
          throughput: 31.3
        },
        model_architecture: {
          layers: 6,
          parameters: 890000,
          input_shape: [1, 64],
          output_shape: [1, 1],
          activation: 'tanh',
          optimizer: 'rmsprop'
        }
      },
      {
        id: '3',
        name: 'Learning Pattern Generator',
        type: 'generation',
        framework: 'tensorflow',
        size: 25.3,
        accuracy: 0.91,
        latency: 78,
        memory_usage: 512,
        is_loaded: false,
        is_training: true,
        status: 'training',
        description: 'Generates learning patterns for consciousness development',
        created_at: '2025-09-05',
        last_used: '2025-09-07',
        performance_metrics: {
          precision: 0.89,
          recall: 0.92,
          f1_score: 0.90,
          inference_time: 78,
          throughput: 12.8
        },
        model_architecture: {
          layers: 12,
          parameters: 2500000,
          input_shape: [1, 256],
          output_shape: [1, 256],
          activation: 'gelu',
          optimizer: 'adamw'
        }
      }
    ]);

    setTrainingJobs([
      {
        id: '1',
        model_id: '3',
        dataset: 'consciousness_patterns_v2',
        epochs: 100,
        batch_size: 32,
        learning_rate: 0.001,
        optimizer: 'AdamW',
        status: 'running',
        progress: 65,
        current_epoch: 65,
        start_time: '2025-09-07T08:00:00Z',
        metrics: {
          accuracy: Array.from({ length: 65 }, (_, i) => 0.6 + (i / 65) * 0.31),
          loss: Array.from({ length: 65 }, (_, i) => 1.2 - (i / 65) * 1.0),
          validation_accuracy: Array.from({ length: 65 }, (_, i) => 0.55 + (i / 65) * 0.30),
          validation_loss: Array.from({ length: 65 }, (_, i) => 1.3 - (i / 65) * 0.9)
        },
        resources: {
          gpu_usage: 0, // Client-side, no GPU
          memory_usage: 85,
          cpu_usage: 45,
          storage_usage: 62
        }
      }
    ]);
  }, []);

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'classification': return <Target className="w-4 h-4" />;
      case 'regression': return <TrendingUp className="w-4 h-4" />;
      case 'clustering': return <Network className="w-4 h-4" />;
      case 'generation': return <Zap className="w-4 h-4" />;
      case 'translation': return <Globe className="w-4 h-4" />;
      case 'summarization': return <File className="w-4 h-4" />;
      default: return <Brain className="w-4 h-4" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ready': return 'bg-green-500/20 text-green-300';
      case 'loading': return 'bg-blue-500/20 text-blue-300';
      case 'training': return 'bg-purple-500/20 text-purple-300';
      case 'idle': return 'bg-gray-500/20 text-gray-300';
      case 'error': return 'bg-red-500/20 text-red-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const getFrameworkIcon = (framework: string) => {
    switch (framework) {
      case 'tensorflow': return <Layers className="w-4 h-4" />;
      case 'pytorch': return <Cpu className="w-4 h-4" />;
      case 'onnx': return <Network className="w-4 h-4" />;
      case 'tflite': return <Smartphone className="w-4 h-4" />;
      default: return <Brain className="w-4 h-4" />;
    }
  };

  const formatSize = (size: number) => {
    if (size >= 1000) return `${(size / 1000).toFixed(1)}GB`;
    return `${size.toFixed(1)}MB`;
  };

  const loadModel = async (modelId: string) => {
    const model = models.find(m => m.id === modelId);
    if (!model) return;

    try {
      // Simulate model loading
      setModels(prev => prev.map(m => 
        m.id === modelId ? { ...m, status: 'loading' } : m
      ));
      
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      setModels(prev => prev.map(m => 
        m.id === modelId ? { ...m, status: 'ready', is_loaded: true } : m
      ));
      
      onModelLoad(model);
    } catch (error) {
      setModels(prev => prev.map(m => 
        m.id === modelId ? { ...m, status: 'error' } : m
      ));
    }
  };

  const unloadModel = (modelId: string) => {
    const model = models.find(m => m.id === modelId);
    if (!model) return;

    setModels(prev => prev.map(m => 
      m.id === modelId ? { ...m, status: 'idle', is_loaded: false } : m
    ));
    
    onModelUnload(model);
  };

  const startTraining = (modelId: string) => {
    const model = models.find(m => m.id === modelId);
    if (!model) return;

    const newTraining: TensorFlowTraining = {
      id: Date.now().toString(),
      model_id: modelId,
      dataset: 'consciousness_data_v4',
      epochs: 100,
      batch_size: 32,
      learning_rate: 0.001,
      optimizer: 'Adam',
      status: 'running',
      progress: 0,
      current_epoch: 0,
      start_time: new Date().toISOString(),
      metrics: {
        accuracy: [],
        loss: [],
        validation_accuracy: [],
        validation_loss: []
      },
      resources: {
        gpu_usage: 0,
        memory_usage: 0,
        cpu_usage: 0,
        storage_usage: 0
      }
    };

    setTrainingJobs(prev => [newTraining, ...prev]);
    onTrainingStart(newTraining);
    setIsTraining(true);
  };

  return (
    <div className="space-y-6">
      <Card className="bg-gray-800/50 border-gray-700">
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm text-white flex items-center">
              <Cpu className="w-4 h-4 mr-2" />
              TensorFlow.js Integration
            </CardTitle>
            <div className="flex items-center space-x-2">
              <div className={`w-2 h-2 rounded-full ${isTensorFlowReady ? 'bg-green-500' : 'bg-red-500'}`} />
              <span className="text-xs text-gray-400">
                {isTensorFlowReady ? 'Ready' : 'Loading...'}
              </span>
            </div>
          </div>
        </CardHeader>
        
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-4 bg-gray-700/50">
              <TabsTrigger value="models" className="text-xs">Models</TabsTrigger>
              <TabsTrigger value="training" className="text-xs">Training</TabsTrigger>
              <TabsTrigger value="inference" className="text-xs">Inference</TabsTrigger>
              <TabsTrigger value="performance" className="text-xs">Performance</TabsTrigger>
            </TabsList>

            {/* Models Tab */}
            <TabsContent value="models" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {models.map((model) => (
                  <Card key={model.id} className="bg-gray-700/30 border-gray-600">
                    <CardHeader className="pb-2">
                      <div className="flex items-center justify-between">
                        <CardTitle className="text-xs text-white flex items-center">
                          {getTypeIcon(model.type)}
                          <span className="ml-2">{model.name}</span>
                        </CardTitle>
                        <Badge className={getStatusColor(model.status)}>
                          {model.status}
                        </Badge>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <p className="text-xs text-gray-300">{model.description}</p>
                      
                      <div className="grid grid-cols-2 gap-2 text-xs">
                        <div>
                          <span className="text-gray-400">Framework:</span>
                          <div className="flex items-center space-x-1 mt-1">
                            {getFrameworkIcon(model.framework)}
                            <span className="text-white">{model.framework}</span>
                          </div>
                        </div>
                        <div>
                          <span className="text-gray-400">Size:</span>
                          <span className="text-white ml-1">{formatSize(model.size)}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Accuracy:</span>
                          <span className="text-green-400 ml-1">{(model.accuracy * 100).toFixed(1)}%</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Latency:</span>
                          <span className="text-white ml-1">{model.latency}ms</span>
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <div className="flex justify-between text-xs">
                          <span className="text-gray-400">Performance:</span>
                          <span className="text-white">{model.performance_metrics.f1_score.toFixed(3)}</span>
                        </div>
                        <div className="w-full bg-gray-600 rounded-full h-2">
                          <div 
                            className="bg-gradient-to-r from-blue-500 to-green-500 h-2 rounded-full"
                            style={{ width: `${model.accuracy * 100}%` }}
                          />
                        </div>
                      </div>
                      
                      <div className="flex space-x-2">
                        <Button
                          size="sm"
                          onClick={() => model.is_loaded ? unloadModel(model.id) : loadModel(model.id)}
                          disabled={model.status === 'loading'}
                          className="flex-1 text-xs"
                        >
                          {model.is_loaded ? 'Unload' : 'Load'}
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => startTraining(model.id)}
                          disabled={model.is_training}
                          className="flex-1 text-xs"
                        >
                          <Play className="w-3 h-3 mr-1" />
                          Train
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Training Tab */}
            <TabsContent value="training" className="space-y-4">
              <div className="space-y-3">
                {trainingJobs.map((job) => (
                  <Card key={job.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          <div className="w-3 h-3 rounded-full bg-blue-500 animate-pulse" />
                          <span className="text-sm font-medium text-white">
                            {models.find(m => m.id === job.model_id)?.name}
                          </span>
                        </div>
                        <Badge className="bg-blue-500/20 text-blue-300">
                          {job.status}
                        </Badge>
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
                            <span className="text-gray-400">Epoch:</span>
                            <span className="text-white ml-1">{job.current_epoch}/{job.epochs}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Batch Size:</span>
                            <span className="text-white ml-1">{job.batch_size}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Learning Rate:</span>
                            <span className="text-white ml-1">{job.learning_rate}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Optimizer:</span>
                            <span className="text-white ml-1">{job.optimizer}</span>
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-4 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Memory:</span>
                            <span className="text-white ml-1">{job.resources.memory_usage}%</span>
                          </div>
                          <div>
                            <span className="text-gray-400">CPU:</span>
                            <span className="text-white ml-1">{job.resources.cpu_usage}%</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Storage:</span>
                            <span className="text-white ml-1">{job.resources.storage_usage}%</span>
                          </div>
                          <div>
                            <span className="text-gray-400">GPU:</span>
                            <span className="text-white ml-1">{job.resources.gpu_usage}%</span>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Inference Tab */}
            <TabsContent value="inference" className="space-y-4">
              <Card className="bg-gray-700/30 border-gray-600">
                <CardContent className="p-4">
                  <h3 className="text-sm font-medium text-white mb-3">Real-time Inference</h3>
                  
                  <div className="space-y-3">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="text-xs text-gray-400">Input Data</label>
                        <textarea
                          className="w-full bg-gray-600/50 border border-gray-500 rounded px-2 py-1 text-xs text-white mt-1"
                          rows={4}
                          placeholder="Enter consciousness data for inference..."
                        />
                      </div>
                      <div>
                        <label className="text-xs text-gray-400">Output</label>
                        <div className="w-full bg-gray-600/50 border border-gray-500 rounded px-2 py-1 text-xs text-white mt-1 h-20 flex items-center justify-center">
                          <span className="text-gray-400">Run inference to see results</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex space-x-2">
                      <Button className="flex-1 text-xs">
                        <Play className="w-3 h-3 mr-1" />
                        Run Inference
                      </Button>
                      <Button variant="outline" className="text-xs">
                        <Settings className="w-3 h-3 mr-1" />
                        Configure
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Performance Tab */}
            <TabsContent value="performance" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {models.filter(m => m.is_loaded).map((model) => (
                  <Card key={model.id} className="bg-gray-700/30 border-gray-600">
                    <CardHeader className="pb-2">
                      <CardTitle className="text-xs text-white">{model.name}</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <div className="space-y-2">
                        <div className="flex justify-between text-xs">
                          <span className="text-gray-400">Precision:</span>
                          <span className="text-white">{(model.performance_metrics.precision * 100).toFixed(1)}%</span>
                        </div>
                        <div className="w-full bg-gray-600 rounded-full h-2">
                          <div 
                            className="bg-gradient-to-r from-blue-500 to-cyan-500 h-2 rounded-full"
                            style={{ width: `${model.performance_metrics.precision * 100}%` }}
                          />
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <div className="flex justify-between text-xs">
                          <span className="text-gray-400">Recall:</span>
                          <span className="text-white">{(model.performance_metrics.recall * 100).toFixed(1)}%</span>
                        </div>
                        <div className="w-full bg-gray-600 rounded-full h-2">
                          <div 
                            className="bg-gradient-to-r from-green-500 to-emerald-500 h-2 rounded-full"
                            style={{ width: `${model.performance_metrics.recall * 100}%` }}
                          />
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <div className="flex justify-between text-xs">
                          <span className="text-gray-400">F1 Score:</span>
                          <span className="text-white">{(model.performance_metrics.f1_score * 100).toFixed(1)}%</span>
                        </div>
                        <div className="w-full bg-gray-600 rounded-full h-2">
                          <div 
                            className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full"
                            style={{ width: `${model.performance_metrics.f1_score * 100}%` }}
                          />
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-2 text-xs">
                        <div>
                          <span className="text-gray-400">Inference Time:</span>
                          <span className="text-white ml-1">{model.performance_metrics.inference_time}ms</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Throughput:</span>
                          <span className="text-white ml-1">{model.performance_metrics.throughput.toFixed(1)}/s</span>
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

export default TensorFlowJSIntegration;
