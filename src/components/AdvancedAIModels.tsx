import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Brain, 
  Cpu, 
  Layers, 
  Network, 
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
  Wifi,
  WifiOff,
  CheckCircle,
  XCircle,
  AlertCircle,
  Info,
  Lightbulb,
  Rocket,
  Shield,
  Key,
  Lock as LockIcon,
  Unlock as UnlockIcon,
  Globe as GlobeIcon,
  Eye as EyeIcon,
  EyeOff as EyeOffIcon
} from 'lucide-react';

interface AIModel {
  id: string;
  name: string;
  type: 'transformer' | 'lstm' | 'cnn' | 'gan' | 'autoencoder' | 'attention' | 'hybrid' | 'quantum' | 'federated' | 'distributed';
  architecture: string;
  parameters: number;
  accuracy: number;
  loss: number;
  training_time: number;
  inference_time: number;
  status: 'active' | 'training' | 'idle' | 'error' | 'deployed' | 'archived';
  description: string;
  created_at: string;
  last_trained: string;
  performance_metrics: {
    precision: number;
    recall: number;
    f1_score: number;
    auc: number;
    mse: number;
    mae: number;
    bleu: number;
    rouge: number;
    perplexity: number;
  };
  deployment: {
    environment: 'local' | 'cloud' | 'edge' | 'hybrid';
    instances: number;
    region: string;
    cost_per_hour: number;
    uptime: number;
  };
  collaboration: {
    is_public: boolean;
    contributors: string[];
    forks: number;
    stars: number;
    downloads: number;
    license: string;
  };
}

interface TrainingJob {
  id: string;
  model_id: string;
  dataset: string;
  epochs: number;
  batch_size: number;
  learning_rate: number;
  optimizer: string;
  status: 'running' | 'completed' | 'failed' | 'paused' | 'queued';
  progress: number;
  current_epoch: number;
  start_time: string;
  end_time?: string;
  metrics: {
    accuracy: number[];
    loss: number[];
    validation_accuracy: number[];
    validation_loss: number[];
    learning_rate: number[];
  };
  resources: {
    gpu_usage: number;
    memory_usage: number;
    cpu_usage: number;
    storage_usage: number;
  };
}

interface GlobalCollaboration {
  id: string;
  name: string;
  description: string;
  host: string;
  participants: number;
  models_shared: number;
  insights_generated: number;
  is_public: boolean;
  region: string;
  created_at: string;
  last_activity: string;
  tags: string[];
}

interface AdvancedAIModelsProps {
  consciousnessData: any;
  onModelSelect: (model: AIModel) => void;
  onTrainingStart: (job: TrainingJob) => void;
  onCollaborationJoin: (collaboration: GlobalCollaboration) => void;
}

const AdvancedAIModels: React.FC<AdvancedAIModelsProps> = ({
  consciousnessData,
  onModelSelect,
  onTrainingStart,
  onCollaborationJoin
}) => {
  const [activeTab, setActiveTab] = useState('models');
  const [models, setModels] = useState<AIModel[]>([]);
  const [trainingJobs, setTrainingJobs] = useState<TrainingJob[]>([]);
  const [globalCollaborations, setGlobalCollaborations] = useState<GlobalCollaboration[]>([]);
  const [selectedModel, setSelectedModel] = useState<string | null>(null);
  const [isTraining, setIsTraining] = useState(false);
  const [newModel, setNewModel] = useState({
    name: '',
    type: 'transformer' as const,
    architecture: '',
    description: ''
  });

  // Initialize with sample data
  useEffect(() => {
    setModels([
      {
        id: '1',
        name: 'Consciousness Quantum Transformer',
        type: 'quantum',
        architecture: 'Quantum Attention Mechanism',
        parameters: 500000000,
        accuracy: 0.97,
        loss: 0.08,
        training_time: 12.5,
        inference_time: 0.05,
        status: 'deployed',
        description: 'Revolutionary quantum-enhanced transformer for consciousness prediction',
        created_at: '2025-09-01',
        last_trained: '2025-09-07',
        performance_metrics: {
          precision: 0.95,
          recall: 0.93,
          f1_score: 0.94,
          auc: 0.98,
          mse: 0.12,
          mae: 0.06,
          bleu: 0.89,
          rouge: 0.91,
          perplexity: 2.3
        },
        deployment: {
          environment: 'cloud',
          instances: 5,
          region: 'global',
          cost_per_hour: 2.50,
          uptime: 99.9
        },
        collaboration: {
          is_public: true,
          contributors: ['Alex Chen', 'Sarah Johnson', 'Marcus Rodriguez'],
          forks: 23,
          stars: 156,
          downloads: 1247,
          license: 'MIT'
        }
      },
      {
        id: '2',
        name: 'Federated Consciousness LSTM',
        type: 'federated',
        architecture: 'Federated Learning LSTM',
        parameters: 200000000,
        accuracy: 0.92,
        loss: 0.15,
        training_time: 8.2,
        inference_time: 0.08,
        status: 'training',
        description: 'Federated learning LSTM for distributed consciousness analysis',
        created_at: '2025-09-03',
        last_trained: '2025-09-07',
        performance_metrics: {
          precision: 0.90,
          recall: 0.88,
          f1_score: 0.89,
          auc: 0.94,
          mse: 0.18,
          mae: 0.09,
          bleu: 0.85,
          rouge: 0.87,
          perplexity: 3.1
        },
        deployment: {
          environment: 'hybrid',
          instances: 12,
          region: 'multi-region',
          cost_per_hour: 1.80,
          uptime: 99.7
        },
        collaboration: {
          is_public: true,
          contributors: ['Global Research Team'],
          forks: 45,
          stars: 234,
          downloads: 2156,
          license: 'Apache 2.0'
        }
      },
      {
        id: '3',
        name: 'Distributed Consciousness GAN',
        type: 'distributed',
        architecture: 'Distributed GAN Architecture',
        parameters: 800000000,
        accuracy: 0.89,
        loss: 0.22,
        training_time: 15.8,
        inference_time: 0.12,
        status: 'active',
        description: 'Distributed GAN for consciousness state generation across multiple nodes',
        created_at: '2025-09-05',
        last_trained: '2025-09-06',
        performance_metrics: {
          precision: 0.87,
          recall: 0.85,
          f1_score: 0.86,
          auc: 0.91,
          mse: 0.25,
          mae: 0.12,
          bleu: 0.82,
          rouge: 0.84,
          perplexity: 3.8
        },
        deployment: {
          environment: 'edge',
          instances: 8,
          region: 'edge-nodes',
          cost_per_hour: 3.20,
          uptime: 99.5
        },
        collaboration: {
          is_public: true,
          contributors: ['Edge Computing Team'],
          forks: 67,
          stars: 189,
          downloads: 987,
          license: 'GPL-3.0'
        }
      }
    ]);

    setTrainingJobs([
      {
        id: '1',
        model_id: '2',
        dataset: 'federated_consciousness_v3',
        epochs: 200,
        batch_size: 64,
        learning_rate: 0.0005,
        optimizer: 'AdamW',
        status: 'running',
        progress: 75,
        current_epoch: 150,
        start_time: '2025-09-07T08:00:00Z',
        metrics: {
          accuracy: Array.from({ length: 150 }, (_, i) => 0.6 + (i / 150) * 0.32),
          loss: Array.from({ length: 150 }, (_, i) => 1.2 - (i / 150) * 1.05),
          validation_accuracy: Array.from({ length: 150 }, (_, i) => 0.55 + (i / 150) * 0.30),
          validation_loss: Array.from({ length: 150 }, (_, i) => 1.3 - (i / 150) * 1.0),
          learning_rate: Array.from({ length: 150 }, (_, i) => 0.0005 * Math.exp(-i / 100))
        },
        resources: {
          gpu_usage: 85,
          memory_usage: 78,
          cpu_usage: 45,
          storage_usage: 62
        }
      }
    ]);

    setGlobalCollaborations([
      {
        id: '1',
        name: 'Global Consciousness Research Initiative',
        description: 'Worldwide collaboration on consciousness AI research',
        host: 'MIT Consciousness Lab',
        participants: 1247,
        models_shared: 89,
        insights_generated: 234,
        is_public: true,
        region: 'global',
        created_at: '2025-09-01',
        last_activity: '2025-09-07T10:30:00Z',
        tags: ['research', 'consciousness', 'ai', 'global']
      },
      {
        id: '2',
        name: 'Quantum Consciousness Collective',
        description: 'Advanced quantum consciousness research and development',
        host: 'Quantum AI Institute',
        participants: 456,
        models_shared: 34,
        insights_generated: 89,
        is_public: true,
        region: 'north-america',
        created_at: '2025-09-03',
        last_activity: '2025-09-07T09:45:00Z',
        tags: ['quantum', 'consciousness', 'advanced', 'research']
      },
      {
        id: '3',
        name: 'Federated Learning Alliance',
        description: 'Distributed consciousness learning across institutions',
        host: 'Stanford AI Lab',
        participants: 789,
        models_shared: 56,
        insights_generated: 156,
        is_public: true,
        region: 'multi-region',
        created_at: '2025-09-05',
        last_activity: '2025-09-07T08:15:00Z',
        tags: ['federated', 'learning', 'distributed', 'collaboration']
      }
    ]);
  }, []);

  const getModelIcon = (type: string) => {
    switch (type) {
      case 'transformer': return <Network className="w-4 h-4" />;
      case 'lstm': return <Layers className="w-4 h-4" />;
      case 'cnn': return <Brain className="w-4 h-4" />;
      case 'gan': return <Zap className="w-4 h-4" />;
      case 'autoencoder': return <Target className="w-4 h-4" />;
      case 'attention': return <Eye className="w-4 h-4" />;
      case 'quantum': return <Rocket className="w-4 h-4" />;
      case 'federated': return <Globe className="w-4 h-4" />;
      case 'distributed': return <Server className="w-4 h-4" />;
      default: return <Cpu className="w-4 h-4" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-500/20 text-green-300';
      case 'training': return 'bg-blue-500/20 text-blue-300';
      case 'deployed': return 'bg-purple-500/20 text-purple-300';
      case 'idle': return 'bg-gray-500/20 text-gray-300';
      case 'error': return 'bg-red-500/20 text-red-300';
      case 'archived': return 'bg-yellow-500/20 text-yellow-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const getEnvironmentIcon = (environment: string) => {
    switch (environment) {
      case 'local': return <Cpu className="w-3 h-3" />;
      case 'cloud': return <Cloud className="w-3 h-3" />;
      case 'edge': return <Wifi className="w-3 h-3" />;
      case 'hybrid': return <Database className="w-3 h-3" />;
      default: return <Server className="w-3 h-3" />;
    }
  };

  const formatParameters = (params: number) => {
    if (params >= 1000000000) return `${(params / 1000000000).toFixed(1)}B`;
    if (params >= 1000000) return `${(params / 1000000).toFixed(1)}M`;
    if (params >= 1000) return `${(params / 1000).toFixed(1)}K`;
    return params.toString();
  };

  const startTraining = (modelId: string) => {
    const model = models.find(m => m.id === modelId);
    if (!model) return;

    const newJob: TrainingJob = {
      id: Date.now().toString(),
      model_id: modelId,
      dataset: 'consciousness_data_v4',
      epochs: 200,
      batch_size: 64,
      learning_rate: 0.0005,
      optimizer: 'AdamW',
      status: 'running',
      progress: 0,
      current_epoch: 0,
      start_time: new Date().toISOString(),
      metrics: {
        accuracy: [],
        loss: [],
        validation_accuracy: [],
        validation_loss: [],
        learning_rate: []
      },
      resources: {
        gpu_usage: 0,
        memory_usage: 0,
        cpu_usage: 0,
        storage_usage: 0
      }
    };

    setTrainingJobs(prev => [newJob, ...prev]);
    onTrainingStart(newJob);
    setIsTraining(true);
  };

  const createModel = () => {
    const newModel: AIModel = {
      id: Date.now().toString(),
      name: newModel.name,
      type: newModel.type,
      architecture: newModel.architecture,
      parameters: Math.floor(Math.random() * 1000000000),
      accuracy: 0,
      loss: 1.0,
      training_time: 0,
      inference_time: 0,
      status: 'idle',
      description: newModel.description,
      created_at: new Date().toISOString().split('T')[0],
      last_trained: 'Never',
      performance_metrics: {
        precision: 0,
        recall: 0,
        f1_score: 0,
        auc: 0,
        mse: 1.0,
        mae: 1.0,
        bleu: 0,
        rouge: 0,
        perplexity: 10.0
      },
      deployment: {
        environment: 'local',
        instances: 1,
        region: 'local',
        cost_per_hour: 0,
        uptime: 0
      },
      collaboration: {
        is_public: false,
        contributors: [],
        forks: 0,
        stars: 0,
        downloads: 0,
        license: 'MIT'
      }
    };

    setModels(prev => [newModel, ...prev]);
    setNewModel({ name: '', type: 'transformer', architecture: '', description: '' });
  };

  return (
    <div className="space-y-6">
      <Card className="bg-gray-800/50 border-gray-700">
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm text-white flex items-center">
              <Brain className="w-4 h-4 mr-2" />
              Advanced AI Models
            </CardTitle>
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                className="text-xs"
              >
                <Plus className="w-3 h-3 mr-1" />
                New Model
              </Button>
              <Button
                variant="outline"
                size="sm"
                className="text-xs"
              >
                <Settings className="w-3 h-3 mr-1" />
                Configure
              </Button>
            </div>
          </div>
        </CardHeader>
        
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-4 bg-gray-700/50">
              <TabsTrigger value="models" className="text-xs">Models</TabsTrigger>
              <TabsTrigger value="training" className="text-xs">Training</TabsTrigger>
              <TabsTrigger value="deployment" className="text-xs">Deployment</TabsTrigger>
              <TabsTrigger value="collaboration" className="text-xs">Global</TabsTrigger>
            </TabsList>

            {/* Models Tab */}
            <TabsContent value="models" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {models.map((model) => (
                  <Card key={model.id} className="bg-gray-700/30 border-gray-600">
                    <CardHeader className="pb-2">
                      <div className="flex items-center justify-between">
                        <CardTitle className="text-xs text-white flex items-center">
                          {getModelIcon(model.type)}
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
                          <span className="text-gray-400">Parameters:</span>
                          <span className="text-white ml-1">{formatParameters(model.parameters)}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Accuracy:</span>
                          <span className="text-green-400 ml-1">{(model.accuracy * 100).toFixed(1)}%</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Architecture:</span>
                          <span className="text-white ml-1">{model.architecture}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Loss:</span>
                          <span className="text-red-400 ml-1">{model.loss.toFixed(3)}</span>
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
                      
                      <div className="flex items-center justify-between text-xs">
                        <div className="flex items-center space-x-2">
                          {getEnvironmentIcon(model.deployment.environment)}
                          <span className="text-gray-400">{model.deployment.environment}</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Star className="w-3 h-3 text-yellow-400" />
                          <span className="text-white">{model.collaboration.stars}</span>
                        </div>
                      </div>
                      
                      <div className="flex space-x-2">
                        <Button
                          size="sm"
                          onClick={() => startTraining(model.id)}
                          disabled={model.status === 'training'}
                          className="flex-1 text-xs"
                        >
                          <Play className="w-3 h-3 mr-1" />
                          Train
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => onModelSelect(model)}
                          className="flex-1 text-xs"
                        >
                          <Eye className="w-3 h-3 mr-1" />
                          View
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
                            <span className="text-gray-400">GPU:</span>
                            <span className="text-white ml-1">{job.resources.gpu_usage}%</span>
                          </div>
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
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Deployment Tab */}
            <TabsContent value="deployment" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {models.filter(m => m.status === 'deployed').map((model) => (
                  <Card key={model.id} className="bg-gray-700/30 border-gray-600">
                    <CardHeader className="pb-2">
                      <CardTitle className="text-xs text-white">{model.name}</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-gray-400">Environment:</span>
                        <div className="flex items-center space-x-1">
                          {getEnvironmentIcon(model.deployment.environment)}
                          <span className="text-white">{model.deployment.environment}</span>
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-2 text-xs">
                        <div>
                          <span className="text-gray-400">Instances:</span>
                          <span className="text-white ml-1">{model.deployment.instances}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Region:</span>
                          <span className="text-white ml-1">{model.deployment.region}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Cost/Hour:</span>
                          <span className="text-white ml-1">${model.deployment.cost_per_hour}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Uptime:</span>
                          <span className="text-green-400 ml-1">{model.deployment.uptime}%</span>
                        </div>
                      </div>
                      
                      <div className="flex space-x-2">
                        <Button size="sm" variant="outline" className="flex-1 text-xs">
                          <Eye className="w-3 h-3 mr-1" />
                          Monitor
                        </Button>
                        <Button size="sm" variant="outline" className="flex-1 text-xs">
                          <Settings className="w-3 h-3 mr-1" />
                          Configure
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Global Collaboration Tab */}
            <TabsContent value="collaboration" className="space-y-4">
              <div className="space-y-3">
                {globalCollaborations.map((collaboration) => (
                  <Card key={collaboration.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <div className="flex items-center space-x-2 mb-1">
                            <h3 className="text-sm font-medium text-white">{collaboration.name}</h3>
                            {collaboration.is_public ? <GlobeIcon className="w-3 h-3 text-green-400" /> : <LockIcon className="w-3 h-3 text-yellow-400" />}
                          </div>
                          <p className="text-xs text-gray-300 mb-2">{collaboration.description}</p>
                          <div className="flex items-center space-x-4 text-xs text-gray-400">
                            <span>Host: {collaboration.host}</span>
                            <span>{collaboration.participants} participants</span>
                            <span>{collaboration.models_shared} models</span>
                          </div>
                        </div>
                        <div className="flex flex-col space-y-2">
                          <Button
                            size="sm"
                            onClick={() => onCollaborationJoin(collaboration)}
                            className="text-xs"
                          >
                            <Users className="w-3 h-3 mr-1" />
                            Join
                          </Button>
                          <div className="text-xs text-gray-400 text-right">
                            {collaboration.region}
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex flex-wrap gap-1">
                        {collaboration.tags.map((tag, index) => (
                          <Badge key={index} className="bg-gray-600/50 text-gray-300 text-xs">
                            {tag}
                          </Badge>
                        ))}
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

export default AdvancedAIModels;
