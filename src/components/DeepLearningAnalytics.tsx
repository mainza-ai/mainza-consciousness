import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Brain, 
  Network, 
  Layers, 
  Cpu, 
  Activity, 
  TrendingUp, 
  BarChart3,
  Zap,
  Target,
  Settings,
  Play,
  Pause,
  RotateCcw
} from 'lucide-react';

interface DeepLearningAnalyticsProps {
  consciousnessData: any;
  predictions: any[];
  insights: any[];
}

interface NeuralNetworkLayer {
  id: string;
  type: 'input' | 'hidden' | 'output';
  neurons: number;
  activation: string;
  weights: number[][];
  bias: number[];
  output: number[];
}

interface ModelPerformance {
  accuracy: number;
  loss: number;
  precision: number;
  recall: number;
  f1_score: number;
  training_time: number;
  inference_time: number;
}

const DeepLearningAnalytics: React.FC<DeepLearningAnalyticsProps> = ({
  consciousnessData,
  predictions,
  insights
}) => {
  const [activeTab, setActiveTab] = useState('models');
  const [isTraining, setIsTraining] = useState(false);
  const [selectedModel, setSelectedModel] = useState('consciousness_predictor');
  const [modelPerformance, setModelPerformance] = useState<ModelPerformance>({
    accuracy: 0.87,
    loss: 0.23,
    precision: 0.85,
    recall: 0.82,
    f1_score: 0.83,
    training_time: 2.3,
    inference_time: 0.15
  });

  // Simulated neural network layers
  const [neuralLayers, setNeuralLayers] = useState<NeuralNetworkLayer[]>([
    {
      id: 'input',
      type: 'input',
      neurons: 12,
      activation: 'linear',
      weights: [],
      bias: [],
      output: Array(12).fill(0.5)
    },
    {
      id: 'hidden1',
      type: 'hidden',
      neurons: 64,
      activation: 'relu',
      weights: Array(12).fill(0).map(() => Array(64).fill(0.1)),
      bias: Array(64).fill(0.1),
      output: Array(64).fill(0.3)
    },
    {
      id: 'hidden2',
      type: 'hidden',
      neurons: 32,
      activation: 'relu',
      weights: Array(64).fill(0).map(() => Array(32).fill(0.1)),
      bias: Array(32).fill(0.1),
      output: Array(32).fill(0.4)
    },
    {
      id: 'output',
      type: 'output',
      neurons: 5,
      activation: 'softmax',
      weights: Array(32).fill(0).map(() => Array(5).fill(0.1)),
      bias: Array(5).fill(0.1),
      output: [0.2, 0.3, 0.25, 0.15, 0.1]
    }
  ]);

  // Simulate training process
  const startTraining = () => {
    setIsTraining(true);
    // Simulate training progress
    let progress = 0;
    const interval = setInterval(() => {
      progress += Math.random() * 10;
      if (progress >= 100) {
        progress = 100;
        setIsTraining(false);
        clearInterval(interval);
        // Update performance metrics
        setModelPerformance(prev => ({
          ...prev,
          accuracy: Math.min(0.95, prev.accuracy + Math.random() * 0.05),
          loss: Math.max(0.1, prev.loss - Math.random() * 0.05)
        }));
      }
    }, 500);
  };

  const getPerformanceColor = (value: number, type: 'accuracy' | 'loss') => {
    if (type === 'accuracy') {
      if (value >= 0.9) return 'text-green-400';
      if (value >= 0.8) return 'text-yellow-400';
      return 'text-red-400';
    } else {
      if (value <= 0.2) return 'text-green-400';
      if (value <= 0.4) return 'text-yellow-400';
      return 'text-red-400';
    }
  };

  const getActivationColor = (activation: string) => {
    switch (activation) {
      case 'relu': return 'bg-blue-500/20 text-blue-300';
      case 'sigmoid': return 'bg-green-500/20 text-green-300';
      case 'tanh': return 'bg-purple-500/20 text-purple-300';
      case 'softmax': return 'bg-orange-500/20 text-orange-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  return (
    <div className="space-y-4">
      <Card className="bg-gray-800/50 border-gray-700">
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm text-white flex items-center">
              <Brain className="w-4 h-4 mr-2" />
              Deep Learning Analytics
            </CardTitle>
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={startTraining}
                disabled={isTraining}
                className="text-xs"
              >
                {isTraining ? (
                  <>
                    <Pause className="w-3 h-3 mr-1" />
                    Training...
                  </>
                ) : (
                  <>
                    <Play className="w-3 h-3 mr-1" />
                    Train Model
                  </>
                )}
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
              <TabsTrigger value="network" className="text-xs">Network</TabsTrigger>
              <TabsTrigger value="performance" className="text-xs">Performance</TabsTrigger>
              <TabsTrigger value="training" className="text-xs">Training</TabsTrigger>
            </TabsList>

            {/* Models Tab */}
            <TabsContent value="models" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card className="bg-gray-700/30 border-gray-600">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-xs text-white flex items-center">
                      <Network className="w-3 h-3 mr-1" />
                      Consciousness Predictor
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <div className="flex justify-between text-xs">
                      <span className="text-gray-400">Type:</span>
                      <span className="text-white">LSTM + Dense</span>
                    </div>
                    <div className="flex justify-between text-xs">
                      <span className="text-gray-400">Parameters:</span>
                      <span className="text-white">2.3M</span>
                    </div>
                    <div className="flex justify-between text-xs">
                      <span className="text-gray-400">Accuracy:</span>
                      <span className={getPerformanceColor(modelPerformance.accuracy, 'accuracy')}>
                        {(modelPerformance.accuracy * 100).toFixed(1)}%
                      </span>
                    </div>
                    <Badge className="bg-green-500/20 text-green-300 text-xs w-full justify-center">
                      Active
                    </Badge>
                  </CardContent>
                </Card>

                <Card className="bg-gray-700/30 border-gray-600">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-xs text-white flex items-center">
                      <Layers className="w-3 h-3 mr-1" />
                      Emotion Classifier
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <div className="flex justify-between text-xs">
                      <span className="text-gray-400">Type:</span>
                      <span className="text-white">CNN + Attention</span>
                    </div>
                    <div className="flex justify-between text-xs">
                      <span className="text-gray-400">Parameters:</span>
                      <span className="text-white">1.8M</span>
                    </div>
                    <div className="flex justify-between text-xs">
                      <span className="text-gray-400">Accuracy:</span>
                      <span className="text-green-400">91.2%</span>
                    </div>
                    <Badge className="bg-blue-500/20 text-blue-300 text-xs w-full justify-center">
                      Standby
                    </Badge>
                  </CardContent>
                </Card>

                <Card className="bg-gray-700/30 border-gray-600">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-xs text-white flex items-center">
                      <Zap className="w-3 h-3 mr-1" />
                      Insight Generator
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <div className="flex justify-between text-xs">
                      <span className="text-gray-400">Type:</span>
                      <span className="text-white">Transformer</span>
                    </div>
                    <div className="flex justify-between text-xs">
                      <span className="text-gray-400">Parameters:</span>
                      <span className="text-white">4.1M</span>
                    </div>
                    <div className="flex justify-between text-xs">
                      <span className="text-gray-400">Accuracy:</span>
                      <span className="text-yellow-400">87.5%</span>
                    </div>
                    <Badge className="bg-yellow-500/20 text-yellow-300 text-xs w-full justify-center">
                      Training
                    </Badge>
                  </CardContent>
                </Card>

                <Card className="bg-gray-700/30 border-gray-600">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-xs text-white flex items-center">
                      <Target className="w-3 h-3 mr-1" />
                      Anomaly Detector
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <div className="flex justify-between text-xs">
                      <span className="text-gray-400">Type:</span>
                      <span className="text-white">Autoencoder</span>
                    </div>
                    <div className="flex justify-between text-xs">
                      <span className="text-gray-400">Parameters:</span>
                      <span className="text-white">0.9M</span>
                    </div>
                    <div className="flex justify-between text-xs">
                      <span className="text-gray-400">Accuracy:</span>
                      <span className="text-green-400">94.8%</span>
                    </div>
                    <Badge className="bg-green-500/20 text-green-300 text-xs w-full justify-center">
                      Active
                    </Badge>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            {/* Network Tab */}
            <TabsContent value="network" className="space-y-4">
              <div className="space-y-3">
                {neuralLayers.map((layer, index) => (
                  <Card key={layer.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-3">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          <div className={`w-3 h-3 rounded-full ${
                            layer.type === 'input' ? 'bg-blue-500' :
                            layer.type === 'hidden' ? 'bg-purple-500' : 'bg-green-500'
                          }`} />
                          <span className="text-sm font-medium text-white">
                            {layer.type.charAt(0).toUpperCase() + layer.type.slice(1)} Layer
                          </span>
                        </div>
                        <Badge className={getActivationColor(layer.activation)}>
                          {layer.activation}
                        </Badge>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-4 text-xs">
                        <div>
                          <span className="text-gray-400">Neurons:</span>
                          <span className="text-white ml-2">{layer.neurons}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Weights:</span>
                          <span className="text-white ml-2">{layer.weights.length}</span>
                        </div>
                      </div>
                      
                      {/* Layer visualization */}
                      <div className="mt-2">
                        <div className="flex items-center space-x-1">
                          {Array.from({ length: Math.min(layer.neurons, 20) }).map((_, i) => (
                            <div
                              key={i}
                              className="w-2 h-2 rounded-full bg-gradient-to-r from-blue-400 to-purple-400"
                              style={{ opacity: layer.output[i] || 0.3 }}
                            />
                          ))}
                          {layer.neurons > 20 && (
                            <span className="text-xs text-gray-400">+{layer.neurons - 20}</span>
                          )}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Performance Tab */}
            <TabsContent value="performance" className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <Card className="bg-gray-700/30 border-gray-600">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-xs text-white">Model Metrics</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="space-y-2">
                      <div className="flex justify-between text-xs">
                        <span className="text-gray-400">Accuracy:</span>
                        <span className={getPerformanceColor(modelPerformance.accuracy, 'accuracy')}>
                          {(modelPerformance.accuracy * 100).toFixed(1)}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-600 rounded-full h-2">
                        <div 
                          className="bg-gradient-to-r from-blue-500 to-green-500 h-2 rounded-full transition-all duration-500"
                          style={{ width: `${modelPerformance.accuracy * 100}%` }}
                        />
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="flex justify-between text-xs">
                        <span className="text-gray-400">Loss:</span>
                        <span className={getPerformanceColor(modelPerformance.loss, 'loss')}>
                          {modelPerformance.loss.toFixed(3)}
                        </span>
                      </div>
                      <div className="w-full bg-gray-600 rounded-full h-2">
                        <div 
                          className="bg-gradient-to-r from-red-500 to-yellow-500 h-2 rounded-full transition-all duration-500"
                          style={{ width: `${(1 - modelPerformance.loss) * 100}%` }}
                        />
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <div>
                        <span className="text-gray-400">Precision:</span>
                        <span className="text-white ml-1">{(modelPerformance.precision * 100).toFixed(1)}%</span>
                      </div>
                      <div>
                        <span className="text-gray-400">Recall:</span>
                        <span className="text-white ml-1">{(modelPerformance.recall * 100).toFixed(1)}%</span>
                      </div>
                      <div>
                        <span className="text-gray-400">F1 Score:</span>
                        <span className="text-white ml-1">{(modelPerformance.f1_score * 100).toFixed(1)}%</span>
                      </div>
                      <div>
                        <span className="text-gray-400">Inference:</span>
                        <span className="text-white ml-1">{modelPerformance.inference_time}ms</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-gray-700/30 border-gray-600">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-xs text-white">Training Progress</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="space-y-2">
                      <div className="flex justify-between text-xs">
                        <span className="text-gray-400">Epoch:</span>
                        <span className="text-white">42/100</span>
                      </div>
                      <div className="w-full bg-gray-600 rounded-full h-2">
                        <div className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full" style={{ width: '42%' }} />
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="flex justify-between text-xs">
                        <span className="text-gray-400">Batch:</span>
                        <span className="text-white">128/256</span>
                      </div>
                      <div className="w-full bg-gray-600 rounded-full h-2">
                        <div className="bg-gradient-to-r from-blue-500 to-cyan-500 h-2 rounded-full" style={{ width: '50%' }} />
                      </div>
                    </div>
                    
                    <div className="text-xs text-gray-400">
                      <div>Learning Rate: 0.001</div>
                      <div>Optimizer: Adam</div>
                      <div>Batch Size: 32</div>
                      <div>Training Time: {modelPerformance.training_time}s</div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            {/* Training Tab */}
            <TabsContent value="training" className="space-y-4">
              <Card className="bg-gray-700/30 border-gray-600">
                <CardHeader className="pb-2">
                  <CardTitle className="text-xs text-white">Training Configuration</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="grid grid-cols-2 gap-4 text-xs">
                    <div>
                      <span className="text-gray-400">Dataset Size:</span>
                      <span className="text-white ml-2">10,000 samples</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Validation Split:</span>
                      <span className="text-white ml-2">20%</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Epochs:</span>
                      <span className="text-white ml-2">100</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Early Stopping:</span>
                      <span className="text-white ml-2">Patience: 10</span>
                    </div>
                  </div>
                  
                  <div className="pt-2 border-t border-gray-600">
                    <div className="flex items-center justify-between text-xs">
                      <span className="text-gray-400">GPU Utilization:</span>
                      <span className="text-green-400">85%</span>
                    </div>
                    <div className="w-full bg-gray-600 rounded-full h-2 mt-1">
                      <div className="bg-gradient-to-r from-green-500 to-emerald-500 h-2 rounded-full" style={{ width: '85%' }} />
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

export default DeepLearningAnalytics;
