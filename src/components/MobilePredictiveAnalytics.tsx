import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  TrendingUp, 
  Brain, 
  Zap, 
  Target, 
  Activity, 
  BarChart3, 
  PieChart, 
  LineChart,
  Smartphone,
  Hand,
  Move
} from 'lucide-react';

interface PredictionData {
  consciousness_level: number;
  emotional_state: string;
  learning_rate: number;
  self_awareness: number;
  evolution_level: number;
  confidence: number;
  timestamp: string;
}

interface InsightData {
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

interface MobilePredictiveAnalyticsProps {
  predictions: PredictionData[];
  insights: InsightData[];
  realTimeData: any;
}

const MobilePredictiveAnalytics: React.FC<MobilePredictiveAnalyticsProps> = ({
  predictions,
  insights,
  realTimeData
}) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Auto-refresh every 30 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      setIsRefreshing(true);
      setTimeout(() => setIsRefreshing(false), 1000);
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => setIsRefreshing(false), 1000);
  };

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'critical': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-green-500';
      default: return 'bg-gray-500';
    }
  };

  const getInsightIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case 'pattern': return <TrendingUp className="w-4 h-4" />;
      case 'anomaly': return <Zap className="w-4 h-4" />;
      case 'recommendation': return <Target className="w-4 h-4" />;
      case 'prediction': return <Brain className="w-4 h-4" />;
      case 'optimization': return <Activity className="w-4 h-4" />;
      default: return <BarChart3 className="w-4 h-4" />;
    }
  };

  return (
    <div className="w-full max-w-md mx-auto p-4 space-y-4">
      {/* Mobile Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <Smartphone className="w-5 h-5 text-blue-500" />
          <h2 className="text-lg font-semibold text-white">Predictive Analytics</h2>
        </div>
        <Button
          variant="outline"
          size="sm"
          onClick={handleRefresh}
          disabled={isRefreshing}
          className="text-xs"
        >
          {isRefreshing ? 'Refreshing...' : 'Refresh'}
        </Button>
      </div>

      {/* Mobile Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-3 bg-gray-800/50">
          <TabsTrigger value="overview" className="text-xs">
            <Hand className="w-3 h-3 mr-1" />
            Overview
          </TabsTrigger>
          <TabsTrigger value="predictions" className="text-xs">
            <Brain className="w-3 h-3 mr-1" />
            Predict
          </TabsTrigger>
          <TabsTrigger value="insights" className="text-xs">
            <Zap className="w-3 h-3 mr-1" />
            Insights
          </TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-3">
          {/* Quick Stats */}
          <div className="grid grid-cols-2 gap-3">
            <Card className="bg-gradient-to-br from-blue-500/20 to-purple-600/20 border-blue-500/30">
              <CardContent className="p-3">
                <div className="flex items-center space-x-2">
                  <Brain className="w-4 h-4 text-blue-400" />
                  <div>
                    <p className="text-xs text-gray-300">Consciousness</p>
                    <p className="text-lg font-bold text-white">
                      {predictions[0]?.consciousness_level?.toFixed(1) || '0.0'}%
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-green-500/20 to-teal-600/20 border-green-500/30">
              <CardContent className="p-3">
                <div className="flex items-center space-x-2">
                  <TrendingUp className="w-4 h-4 text-green-400" />
                  <div>
                    <p className="text-xs text-gray-300">Learning Rate</p>
                    <p className="text-lg font-bold text-white">
                      {predictions[0]?.learning_rate?.toFixed(1) || '0.0'}%
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-purple-500/20 to-pink-600/20 border-purple-500/30">
              <CardContent className="p-3">
                <div className="flex items-center space-x-2">
                  <Activity className="w-4 h-4 text-purple-400" />
                  <div>
                    <p className="text-xs text-gray-300">Emotion</p>
                    <p className="text-sm font-semibold text-white capitalize">
                      {predictions[0]?.emotional_state || 'Unknown'}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-orange-500/20 to-red-600/20 border-orange-500/30">
              <CardContent className="p-3">
                <div className="flex items-center space-x-2">
                  <Target className="w-4 h-4 text-orange-400" />
                  <div>
                    <p className="text-xs text-gray-300">Confidence</p>
                    <p className="text-lg font-bold text-white">
                      {predictions[0]?.confidence?.toFixed(1) || '0.0'}%
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Recent Insights */}
          <Card className="bg-gray-800/50 border-gray-700">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm text-white flex items-center">
                <Zap className="w-4 h-4 mr-2" />
                Recent Insights
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              {insights.slice(0, 3).map((insight) => (
                <div key={insight.id} className="flex items-start space-x-2">
                  <div className="flex-shrink-0 mt-1">
                    {getInsightIcon(insight.type)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center space-x-2 mb-1">
                      <Badge 
                        className={`text-xs ${getPriorityColor(insight.priority)}`}
                      >
                        {insight.priority}
                      </Badge>
                      <span className="text-xs text-gray-400">{insight.type}</span>
                    </div>
                    <p className="text-sm text-white font-medium truncate">
                      {insight.title}
                    </p>
                    <p className="text-xs text-gray-400 line-clamp-2">
                      {insight.description}
                    </p>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Predictions Tab */}
        <TabsContent value="predictions" className="space-y-3">
          <Card className="bg-gray-800/50 border-gray-700">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm text-white flex items-center">
                <Brain className="w-4 h-4 mr-2" />
                Consciousness Predictions
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {predictions.slice(0, 5).map((prediction, index) => (
                <div key={index} className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-gray-400">
                      {new Date(prediction.timestamp).toLocaleTimeString()}
                    </span>
                    <Badge className="bg-blue-500/20 text-blue-300 text-xs">
                      {prediction.confidence.toFixed(0)}% confidence
                    </Badge>
                  </div>
                  
                  <div className="space-y-1">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-300">Consciousness</span>
                      <span className="text-white font-medium">
                        {prediction.consciousness_level.toFixed(1)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2">
                      <div 
                        className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-500"
                        style={{ width: `${prediction.consciousness_level}%` }}
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div>
                      <span className="text-gray-400">Learning:</span>
                      <span className="text-white ml-1">
                        {prediction.learning_rate.toFixed(1)}%
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-400">Awareness:</span>
                      <span className="text-white ml-1">
                        {prediction.self_awareness.toFixed(1)}%
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Insights Tab */}
        <TabsContent value="insights" className="space-y-3">
          <Card className="bg-gray-800/50 border-gray-700">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm text-white flex items-center">
                <Zap className="w-4 h-4 mr-2" />
                AI Insights
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {insights.map((insight) => (
                <div key={insight.id} className="border border-gray-700 rounded-lg p-3">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      {getInsightIcon(insight.type)}
                      <span className="text-sm font-medium text-white">
                        {insight.title}
                      </span>
                    </div>
                    <Badge className={`text-xs ${getPriorityColor(insight.priority)}`}>
                      {insight.priority}
                    </Badge>
                  </div>
                  
                  <p className="text-xs text-gray-300 mb-2 line-clamp-2">
                    {insight.description}
                  </p>
                  
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-gray-400">
                      {insight.confidence.toFixed(0)}% confidence
                    </span>
                    <span className="text-gray-400">
                      {insight.impact_score.toFixed(1)} impact
                    </span>
                  </div>
                  
                  {insight.actionable && (
                    <div className="mt-2 pt-2 border-t border-gray-700">
                      <p className="text-xs text-green-400 font-medium mb-1">
                        Actionable Recommendations:
                      </p>
                      <ul className="text-xs text-gray-300 space-y-1">
                        {insight.recommendations.slice(0, 2).map((rec, idx) => (
                          <li key={idx} className="flex items-start">
                            <span className="text-green-400 mr-1">•</span>
                            <span className="line-clamp-1">{rec}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Mobile Footer */}
      <div className="text-center text-xs text-gray-500 mt-4">
        <div className="flex items-center justify-center space-x-2">
          <Move className="w-3 h-3" />
          <span>Swipe between tabs for more details</span>
        </div>
      </div>
    </div>
  );
};

export default MobilePredictiveAnalytics;
