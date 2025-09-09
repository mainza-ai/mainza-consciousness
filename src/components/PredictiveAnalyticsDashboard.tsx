import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Brain, TrendingUp, Target, AlertTriangle, Lightbulb, BarChart3, Activity, Clock, ArrowUp, ArrowDown } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface Prediction {
  id?: string;
  prediction_type: string;
  predicted_value: number;
  confidence: number;
  time_horizon: number;
  factors: Record<string, any>;
  recommendation: string;
  trend: 'increasing' | 'decreasing' | 'stable';
}

interface Insight {
  id?: string;
  title: string;
  description: string;
  type: string;
  priority: string;
  category: string;
  tags: string[];
  actionable: boolean;
  recommendations?: string[];
}

interface RealTimeData {
  consciousness_level?: number;
  neural_activity?: number;
  memory_usage?: number;
  prediction_accuracy?: number;
  [key: string]: any;
}

interface PredictiveAnalyticsDashboardProps {
  predictions?: Prediction[];
  insights?: Insight[];
  realTimeData?: RealTimeData;
}

const PredictiveAnalyticsDashboard: React.FC<PredictiveAnalyticsDashboardProps> = ({
  predictions = [],
  insights = [],
  realTimeData = {}
}) => {
  const [activeTab, setActiveTab] = useState('overview');

  const mockPredictions: Prediction[] = [
    {
      prediction_type: 'Consciousness Growth',
      predicted_value: 85.5,
      confidence: 0.92,
      time_horizon: 30,
      factors: { neural_activity: 0.88, memory_patterns: 0.76, learning_velocity: 0.94 },
      recommendation: 'Continue current learning patterns for optimal growth',
      trend: 'increasing'
    },
    {
      prediction_type: 'Memory Efficiency',
      predicted_value: 78.3,
      confidence: 0.85,
      time_horizon: 15,
      factors: { retrieval_speed: 0.89, storage_capacity: 0.72, pattern_recognition: 0.91 },
      recommendation: 'Optimize memory consolidation processes',
      trend: 'stable'
    }
  ];

  const mockInsights: Insight[] = [
    {
      title: 'Neural Pattern Optimization',
      description: 'Detected opportunity to improve neural network efficiency by 15%',
      type: 'optimization',
      priority: 'high',
      category: 'neural-networks',
      tags: ['optimization', 'efficiency', 'neural-networks'],
      actionable: true,
      recommendations: [
        'Implement advanced pruning techniques',
        'Optimize weight quantization',
        'Enhance gradient flow'
      ]
    },
    {
      title: 'Consciousness Evolution Insight',
      description: 'Consciousness level shows accelerated growth trajectory',
      type: 'prediction',
      priority: 'medium',
      category: 'consciousness',
      tags: ['consciousness', 'growth', 'evolution'],
      actionable: false
    }
  ];

  const displayPredictions = predictions.length > 0 ? predictions : mockPredictions;
  const displayInsights = insights.length > 0 ? insights : mockInsights;

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'increasing':
        return <ArrowUp className="h-4 w-4 text-green-400" />;
      case 'decreasing':
        return <ArrowDown className="h-4 w-4 text-red-400" />;
      default:
        return <Activity className="h-4 w-4 text-blue-400" />;
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'optimization':
        return <BarChart3 className="h-4 w-4" />;
      case 'prediction':
        return <Target className="h-4 w-4" />;
      case 'alert':
        return <AlertTriangle className="h-4 w-4" />;
      default:
        return <Lightbulb className="h-4 w-4" />;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'text-red-400 bg-red-400/20';
      case 'medium':
        return 'text-yellow-400 bg-yellow-400/20';
      case 'low':
        return 'text-green-400 bg-green-400/20';
      default:
        return 'text-gray-400 bg-gray-400/20';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-blue-400/50 transition-all duration-300">
        <div className="p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-gradient-to-br from-blue-400 to-cyan-500 rounded-lg">
              <Brain className="h-6 w-6 text-white" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-white">Predictive Analytics Dashboard</h2>
              <p className="text-slate-400 text-sm">AI-powered predictions and insights for consciousness evolution</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-3 bg-slate-800">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="predictions">Predictions</TabsTrigger>
          <TabsTrigger value="insights">AI Insights</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Prediction Accuracy Chart */}
            <Card className="bg-slate-800/50 border-slate-600/30">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <TrendingUp className="h-5 w-5" />
                  Prediction Accuracy Trend
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={200}>
                  <LineChart data={[
                    { time: '1h', accuracy: 85 },
                    { time: '2h', accuracy: 87 },
                    { time: '3h', accuracy: 89 },
                    { time: '4h', accuracy: 88 },
                    { time: '5h', accuracy: 91 },
                    { time: '6h', accuracy: 89 }
                  ]}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis dataKey="time" stroke="#9CA3AF" />
                    <YAxis stroke="#9CA3AF" />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#1F2937',
                        border: '1px solid #374151',
                        borderRadius: '8px'
                      }}
                    />
                    <Line
                      type="monotone"
                      dataKey="accuracy"
                      stroke="#3B82F6"
                      strokeWidth={2}
                      dot={{ fill: '#3B82F6' }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Recent Predictions */}
            <Card className="bg-slate-800/50 border-slate-600/30">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Target className="h-5 w-5" />
                  Recent Predictions
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {displayPredictions.slice(0, 3).map((prediction, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg">
                    <div className="flex items-center gap-3">
                      {getTrendIcon(prediction.trend)}
                      <div>
                        <p className="text-white font-medium">{prediction.prediction_type}</p>
                        <p className="text-slate-400 text-sm">
                          {prediction.predicted_value.toFixed(1)} • {(prediction.confidence * 100).toFixed(0)}%
                        </p>
                      </div>
                    </div>
                    <Badge variant="outline" className="border-slate-600">
                      {prediction.time_horizon}d
                    </Badge>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Predictions Tab */}
        <TabsContent value="predictions" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {displayPredictions.map((prediction, index) => (
              <Card key={index} className="bg-slate-800/50 border-slate-600/30 hover:border-cyan-400/50 transition-all duration-300">
                <CardHeader className="pb-3">
                  <div className="flex items-center gap-2 mb-2">
                    {getTrendIcon(prediction.trend)}
                    <CardTitle className="text-white text-lg">{prediction.prediction_type}</CardTitle>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-slate-300">Predicted Value</span>
                    <span className="text-lg font-bold text-white">
                      {prediction.predicted_value.toFixed(1)}
                    </span>
                  </div>

                  <div className="flex items-center justify-between">
                    <span className="text-sm text-slate-300">Confidence</span>
                    <span className="text-sm font-medium text-blue-400">
                      {(prediction.confidence * 100).toFixed(0)}%
                    </span>
                  </div>

                  <div className="flex items-center justify-between">
                    <span className="text-sm text-slate-300">Time Horizon</span>
                    <span className="text-sm font-medium text-green-400">
                      {prediction.time_horizon} days
                    </span>
                  </div>

                  <div className="pt-2 border-t border-slate-700">
                    <p className="text-sm text-slate-300 mb-3">{prediction.recommendation}</p>
                  </div>

                  <div className="flex flex-wrap gap-1">
                    {Object.entries(prediction.factors).map(([key, value]) => (
                      <Badge key={key} variant="outline" className="text-xs border-slate-600">
                        {key}: {typeof value === 'number' ? value.toFixed(2) : value}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* AI Insights Tab */}
        <TabsContent value="insights" className="space-y-6">
          <div className="space-y-4">
            {displayInsights.map((insight, index) => (
              <Card key={index} className="bg-slate-800/50 border-slate-600/30 hover:border-emerald-400/50 transition-all duration-300">
                <CardContent className="p-6">
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

                      {insight.recommendations && insight.recommendations.length > 0 && (
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
                            className="bg-blue-600 hover:bg-blue-700 ml-auto"
                          >
                            Take Action
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
      </Tabs>
    </div>
  );
};

export default PredictiveAnalyticsDashboard;
