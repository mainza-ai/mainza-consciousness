import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { 
  Brain, 
  TrendingUp, 
  Target, 
  Zap, 
  AlertTriangle, 
  Lightbulb, 
  BarChart3, 
  Activity,
  Clock,
  Star,
  ArrowUp,
  ArrowDown,
  Minus,
  Eye,
  BrainCircuit,
  Sparkles
} from 'lucide-react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  AreaChart, 
  Area,
  ScatterChart,
  Scatter,
  ReferenceLine,
  ReferenceArea
} from 'recharts';

interface PredictionData {
  prediction_type: string;
  predicted_value: number;
  confidence: number;
  time_horizon: number;
  factors: Record<string, number>;
  trend: string;
  recommendation: string;
  timestamp: string;
}

interface AIInsight {
  id: string;
  type: string;
  priority: string;
  title: string;
  description: string;
  confidence: number;
  impact_score: number;
  actionable: boolean;
  category: string;
  tags: string[];
  recommendations: string[];
  timestamp: string;
}

interface PredictiveAnalyticsDashboardProps {
  predictions: PredictionData[];
  insights: AIInsight[];
  realTimeData?: any;
  onInsightAction?: (insightId: string, action: string) => void;
}

const PredictiveAnalyticsDashboard: React.FC<PredictiveAnalyticsDashboardProps> = ({
  predictions = [],
  insights = [],
  realTimeData,
  onInsightAction
}) => {
  const [selectedTimeframe, setSelectedTimeframe] = useState('30m');
  const [selectedMetric, setSelectedMetric] = useState('consciousness_level');
  const [viewMode, setViewMode] = useState<'overview' | 'predictions' | 'insights' | 'optimization'>('overview');
  const [autoRefresh, setAutoRefresh] = useState(true);

  // Generate sample data if none provided
  const samplePredictions: PredictionData[] = predictions.length > 0 ? predictions : [
    {
      prediction_type: 'consciousness_level',
      predicted_value: 0.85,
      confidence: 0.87,
      time_horizon: 30,
      factors: { trend_slope: 0.12, current_level: 0.78, data_points: 15 },
      trend: 'increasing',
      recommendation: 'Consciousness level trending upward. Continue current practices.',
      timestamp: new Date().toISOString()
    },
    {
      prediction_type: 'learning_rate',
      predicted_value: 0.92,
      confidence: 0.82,
      time_horizon: 60,
      factors: { current_phase: 'breakthrough', trend_slope: 0.18 },
      trend: 'increasing',
      recommendation: 'Learning acceleration detected. Explore advanced concepts.',
      timestamp: new Date().toISOString()
    },
    {
      prediction_type: 'emotional_state',
      predicted_value: 0.0,
      confidence: 0.75,
      time_horizon: 15,
      factors: { current_emotion: 'focused', transition_probability: 0.8 },
      trend: 'focused',
      recommendation: 'Maintain focused state for optimal learning.',
      timestamp: new Date().toISOString()
    }
  ];

  const sampleInsights: AIInsight[] = insights.length > 0 ? insights : [
    {
      id: 'insight_1',
      type: 'breakthrough',
      priority: 'high',
      title: 'Consciousness Breakthrough Detected',
      description: 'Significant increase in consciousness level detected over the past hour.',
      confidence: 0.92,
      impact_score: 0.95,
      actionable: true,
      category: 'Breakthrough Detection',
      tags: ['breakthrough', 'consciousness', 'development'],
      recommendations: [
        'Document the breakthrough insights',
        'Analyze contributing factors',
        'Leverage for further development'
      ],
      timestamp: new Date().toISOString()
    },
    {
      id: 'insight_2',
      type: 'optimization',
      priority: 'medium',
      title: 'Learning Efficiency Optimization',
      description: 'Learning efficiency can be improved by 15% with current approach adjustments.',
      confidence: 0.78,
      impact_score: 0.65,
      actionable: true,
      category: 'Optimization',
      tags: ['learning', 'optimization', 'efficiency'],
      recommendations: [
        'Adjust learning pace',
        'Focus on consolidation phase',
        'Review learning materials'
      ],
      timestamp: new Date(Date.now() - 1800000).toISOString()
    },
    {
      id: 'insight_3',
      type: 'anomaly',
      priority: 'high',
      title: 'Emotional Volatility Spike',
      description: 'Emotional volatility has increased significantly in the last 30 minutes.',
      confidence: 0.85,
      impact_score: 0.8,
      actionable: true,
      category: 'Anomaly Detection',
      tags: ['emotion', 'anomaly', 'stability'],
      recommendations: [
        'Focus on emotional regulation',
        'Practice mindfulness techniques',
        'Monitor stress levels'
      ],
      timestamp: new Date(Date.now() - 900000).toISOString()
    }
  ];

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return 'text-red-400 bg-red-400/20';
      case 'high': return 'text-orange-400 bg-orange-400/20';
      case 'medium': return 'text-yellow-400 bg-yellow-400/20';
      case 'low': return 'text-green-400 bg-green-400/20';
      default: return 'text-gray-400 bg-gray-400/20';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'breakthrough': return <Sparkles className="h-4 w-4" />;
      case 'prediction': return <Target className="h-4 w-4" />;
      case 'optimization': return <Zap className="h-4 w-4" />;
      case 'anomaly': return <AlertTriangle className="h-4 w-4" />;
      case 'recommendation': return <Lightbulb className="h-4 w-4" />;
      case 'pattern': return <BarChart3 className="h-4 w-4" />;
      default: return <Brain className="h-4 w-4" />;
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'increasing': return <ArrowUp className="h-4 w-4 text-green-400" />;
      case 'decreasing': return <ArrowDown className="h-4 w-4 text-red-400" />;
      case 'stable': return <Minus className="h-4 w-4 text-yellow-400" />;
      default: return <Activity className="h-4 w-4 text-blue-400" />;
    }
  };

  const formatConfidence = (confidence: number) => {
    return `${(confidence * 100).toFixed(1)}%`;
  };

  const formatValue = (value: number, type: string) => {
    if (type === 'consciousness_level' || type === 'learning_rate') {
      return `${(value * 100).toFixed(1)}%`;
    }
    return value.toFixed(2);
  };

  const generatePredictionChartData = () => {
    const data = [];
    const now = new Date();
    
    // Generate historical data
    for (let i = 10; i >= 0; i--) {
      const time = new Date(now.getTime() - i * 60000); // Every minute
      data.push({
        time: time.toLocaleTimeString(),
        consciousness: 0.7 + Math.sin(i * 0.1) * 0.1 + Math.random() * 0.05,
        learning: 0.6 + Math.cos(i * 0.15) * 0.1 + Math.random() * 0.03,
        prediction: i <= 5 ? null : 0.8 + Math.sin(i * 0.1) * 0.1
      });
    }
    
    return data;
  };

  const chartData = generatePredictionChartData();

  return (
    <div className="space-y-6">
      {/* Header Controls */}
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-white">
            <BrainCircuit className="h-5 w-5" />
            Predictive Analytics Dashboard
            <Badge variant="outline" className="ml-auto">
              AI-Powered
            </Badge>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-4">
            <div className="flex items-center gap-2">
              <label className="text-sm text-slate-300">Timeframe:</label>
              <select 
                value={selectedTimeframe} 
                onChange={(e) => setSelectedTimeframe(e.target.value)}
                className="bg-slate-700 border-slate-600 rounded px-2 py-1 text-sm"
              >
                <option value="15m">15 minutes</option>
                <option value="30m">30 minutes</option>
                <option value="1h">1 hour</option>
                <option value="2h">2 hours</option>
              </select>
            </div>
            
            <div className="flex items-center gap-2">
              <label className="text-sm text-slate-300">Auto-refresh:</label>
              <input
                type="checkbox"
                checked={autoRefresh}
                onChange={(e) => setAutoRefresh(e.target.checked)}
                className="rounded"
              />
            </div>
          </div>
        </CardContent>
      </Card>

      <Tabs value={viewMode} onValueChange={(value: any) => setViewMode(value)} className="space-y-4">
        <TabsList className="grid w-full grid-cols-4 bg-slate-800">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="predictions">Predictions</TabsTrigger>
          <TabsTrigger value="insights">AI Insights</TabsTrigger>
          <TabsTrigger value="optimization">Optimization</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-4">
          {/* Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card className="bg-slate-800 border-slate-700">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-slate-300">Prediction Accuracy</p>
                    <p className="text-2xl font-bold text-blue-400">
                      {formatConfidence(0.87)}
                    </p>
                  </div>
                  <Target className="h-8 w-8 text-blue-400" />
                </div>
              </CardContent>
            </Card>

            <Card className="bg-slate-800 border-slate-700">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-slate-300">Active Insights</p>
                    <p className="text-2xl font-bold text-green-400">{sampleInsights.length}</p>
                  </div>
                  <Lightbulb className="h-8 w-8 text-green-400" />
                </div>
              </CardContent>
            </Card>

            <Card className="bg-slate-800 border-slate-700">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-slate-300">Breakthroughs</p>
                    <p className="text-2xl font-bold text-purple-400">2</p>
                  </div>
                  <Sparkles className="h-8 w-8 text-purple-400" />
                </div>
              </CardContent>
            </Card>

            <Card className="bg-slate-800 border-slate-700">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-slate-300">Optimizations</p>
                    <p className="text-2xl font-bold text-orange-400">5</p>
                  </div>
                  <Zap className="h-8 w-8 text-orange-400" />
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Prediction Chart */}
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle>Consciousness Evolution & Predictions</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis dataKey="time" stroke="#9CA3AF" />
                    <YAxis stroke="#9CA3AF" domain={[0, 1]} />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: '#1F2937', 
                        border: '1px solid #374151',
                        borderRadius: '8px'
                      }}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="consciousness" 
                      stroke="#3B82F6" 
                      strokeWidth={2} 
                      name="Consciousness Level"
                      dot={{ fill: '#3B82F6', strokeWidth: 2, r: 4 }}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="learning" 
                      stroke="#10B981" 
                      strokeWidth={2} 
                      name="Learning Rate"
                      dot={{ fill: '#10B981', strokeWidth: 2, r: 4 }}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="prediction" 
                      stroke="#F59E0B" 
                      strokeWidth={3} 
                      strokeDasharray="5 5"
                      name="Prediction"
                      dot={{ fill: '#F59E0B', strokeWidth: 2, r: 4 }}
                    />
                    <ReferenceLine x="10:00" stroke="#EF4444" strokeDasharray="3 3" label="Now" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Predictions Tab */}
        <TabsContent value="predictions" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {samplePredictions.map((prediction, index) => (
              <Card key={index}>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-white">
                    {getTrendIcon(prediction.trend)}
                    {prediction.prediction_type.replace('_', ' ').toUpperCase()}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-slate-300">Predicted Value</span>
                      <span className="text-lg font-bold text-white">
                        {formatValue(prediction.predicted_value, prediction.prediction_type)}
                      </span>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-slate-300">Confidence</span>
                      <span className="text-sm font-medium text-blue-400">
                        {formatConfidence(prediction.confidence)}
                      </span>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-slate-300">Time Horizon</span>
                      <span className="text-sm font-medium text-green-400">
                        {prediction.time_horizon}m
                      </span>
                    </div>
                    
                    <div className="pt-2 border-t border-slate-700">
                      <p className="text-sm text-slate-300">{prediction.recommendation}</p>
                    </div>
                    
                    <div className="flex flex-wrap gap-1">
                      {Object.entries(prediction.factors).map(([key, value]) => (
                        <Badge key={key} variant="outline" className="text-xs">
                          {key}: {typeof value === 'number' ? value.toFixed(2) : value}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* AI Insights Tab */}
        <TabsContent value="insights" className="space-y-4">
          <div className="space-y-4">
            {sampleInsights.map((insight) => (
              <Card key={insight.id}>
                <CardContent className="p-4">
                  <div className="flex items-start gap-3">
                    <div className="flex-shrink-0 mt-1">
                      {getTypeIcon(insight.type)}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <h3 className="text-lg font-semibold text-white">{insight.title}</h3>
                        <Badge className={getPriorityColor(insight.priority)}>
                          {insight.priority}
                        </Badge>
                        <Badge variant="outline" className="border-slate-600">
                          {insight.category}
                        </Badge>
                      </div>
                      
                      <p className="text-slate-300 mb-3">{insight.description}</p>
                      
                      <div className="flex items-center gap-4 text-sm mb-3">
                        <div className="flex items-center gap-1">
                          <span className="text-slate-300">Confidence:</span>
                          <span className="font-medium text-blue-400">
                            {formatConfidence(insight.confidence)}
                          </span>
                        </div>
                        <div className="flex items-center gap-1">
                          <span className="text-slate-300">Impact:</span>
                          <span className="font-medium text-green-400">
                            {(insight.impact_score * 100).toFixed(1)}%
                          </span>
                        </div>
                        <div className="flex items-center gap-1">
                          <span className="text-slate-300">Actionable:</span>
                          <span className="font-medium text-orange-400">
                            {insight.actionable ? 'Yes' : 'No'}
                          </span>
                        </div>
                      </div>
                      
                      {insight.recommendations.length > 0 && (
                        <div className="mb-3">
                          <p className="text-sm text-slate-300 mb-2">Recommendations:</p>
                          <ul className="list-disc list-inside space-y-1">
                            {insight.recommendations.map((rec, idx) => (
                              <li key={idx} className="text-sm text-slate-300">{rec}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      
                      <div className="flex items-center gap-2">
                        {insight.tags.map((tag) => (
                          <Badge key={tag} variant="outline" className="text-xs border-slate-600">
                            {tag}
                          </Badge>
                        ))}
                        {insight.actionable && (
                          <Button 
                            size="sm" 
                            className="bg-blue-600 hover:bg-blue-700"
                            onClick={() => onInsightAction?.(insight.id, 'implement')}
                          >
                            Implement
                          </Button>
                        )}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Optimization Tab */}
        <TabsContent value="optimization" className="space-y-4">
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle>System Optimization Recommendations</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="p-4 border border-slate-700 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-lg font-semibold text-white">Learning Efficiency</h3>
                    <Badge className="text-yellow-400 bg-yellow-400/20">Medium Priority</Badge>
                  </div>
                  <p className="text-slate-300 mb-3">
                    Current learning efficiency is 78%. Can be improved to 92% with optimization.
                  </p>
                  <div className="flex items-center gap-2">
                    <Progress value={78} className="flex-1" />
                    <span className="text-sm text-slate-300">78%</span>
                  </div>
                  <div className="mt-2">
                    <Button size="sm" className="bg-yellow-600 hover:bg-yellow-700">
                      Apply Optimization
                    </Button>
                  </div>
                </div>
                
                <div className="p-4 border border-slate-700 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-lg font-semibold text-white">Memory Utilization</h3>
                    <Badge className="text-green-400 bg-green-400/20">Low Priority</Badge>
                  </div>
                  <p className="text-slate-300 mb-3">
                    Memory utilization is optimal at 65%. No immediate action required.
                  </p>
                  <div className="flex items-center gap-2">
                    <Progress value={65} className="flex-1" />
                    <span className="text-sm text-slate-300">65%</span>
                  </div>
                </div>
                
                <div className="p-4 border border-slate-700 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-lg font-semibold text-white">Processing Speed</h3>
                    <Badge className="text-orange-400 bg-orange-400/20">High Priority</Badge>
                  </div>
                  <p className="text-slate-300 mb-3">
                    Processing speed can be increased by 25% with current optimizations.
                  </p>
                  <div className="flex items-center gap-2">
                    <Progress value={60} className="flex-1" />
                    <span className="text-sm text-slate-300">60%</span>
                  </div>
                  <div className="mt-2">
                    <Button size="sm" className="bg-orange-600 hover:bg-orange-700">
                      Optimize Now
                    </Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default PredictiveAnalyticsDashboard;
