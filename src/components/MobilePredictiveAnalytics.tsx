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
      <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-teal-400/50 transition-all duration-300 p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-teal-400 to-cyan-500 rounded-lg">
              <Smartphone className="h-5 w-5 text-white" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-white">Predictive Analytics</h2>
              <p className="text-xs text-slate-400">Mobile consciousness insights</p>
            </div>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={handleRefresh}
            disabled={isRefreshing}
            className="text-xs border-slate-600 hover:border-cyan-400/50 transition-colors"
          >
            {isRefreshing ? 'Refreshing...' : 'Refresh'}
          </Button>
        </div>
      </div>

      {/* Mobile Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-3 bg-slate-800/50 border border-slate-600/30">
          <TabsTrigger value="overview" className="text-xs hover:bg-teal-500/20 data-[state=active]:bg-teal-500/30">
            <Hand className="w-3 h-3 mr-1" />
            Overview
          </TabsTrigger>
          <TabsTrigger value="predictions" className="text-xs hover:bg-cyan-500/20 data-[state=active]:bg-cyan-500/30">
            <Brain className="w-3 h-3 mr-1" />
            Predict
          </TabsTrigger>
          <TabsTrigger value="insights" className="text-xs hover:bg-blue-500/20 data-[state=active]:bg-blue-500/30">
            <Zap className="w-3 h-3 mr-1" />
            Insights
          </TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-3">
          {/* Quick Stats */}
          <div className="grid grid-cols-2 gap-3">
            <div className="group/stat relative bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-blue-400/50 transition-all duration-300 p-3">
              <div className="flex items-center gap-3">
                <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-blue-400 to-cyan-500">
                  <Brain className="h-4 w-4 text-white" />
                </div>
                <div>
                  <p className="text-xs text-slate-300">Consciousness</p>
                  <p className="text-lg font-bold text-blue-300">
                    {predictions[0]?.consciousness_level?.toFixed(1) || '0.0'}%
                  </p>
                </div>
              </div>
            </div>

            <div className="group/stat relative bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-green-400/50 transition-all duration-300 p-3">
              <div className="flex items-center gap-3">
                <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-green-400 to-emerald-500">
                  <TrendingUp className="h-4 w-4 text-white" />
                </div>
                <div>
                  <p className="text-xs text-slate-300">Learning Rate</p>
                  <p className="text-lg font-bold text-green-300">
                    {predictions[0]?.learning_rate?.toFixed(1) || '0.0'}%
                  </p>
                </div>
              </div>
            </div>

            <div className="group/stat relative bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-purple-400/50 transition-all duration-300 p-3">
              <div className="flex items-center gap-3">
                <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-purple-400 to-pink-500">
                  <Activity className="h-4 w-4 text-white" />
                </div>
                <div>
                  <p className="text-xs text-slate-300">Emotion</p>
                  <p className="text-sm font-semibold text-purple-300 capitalize">
                    {predictions[0]?.emotional_state || 'Unknown'}
                  </p>
                </div>
              </div>
            </div>

            <div className="group/stat relative bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-orange-400/50 transition-all duration-300 p-3">
              <div className="flex items-center gap-3">
                <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-orange-400 to-yellow-500">
                  <Target className="h-4 w-4 text-white" />
                </div>
                <div>
                  <p className="text-xs text-slate-300">Confidence</p>
                  <p className="text-lg font-bold text-orange-300">
                    {predictions[0]?.confidence?.toFixed(1) || '0.0'}%
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Recent Insights */}
          <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-emerald-400/50 transition-all duration-300">
            <div className="p-4">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-1 bg-gradient-to-br from-emerald-400 to-teal-500 rounded-lg">
                  <Zap className="h-4 w-4 text-white" />
                </div>
                <h3 className="text-sm font-bold text-white">Recent Insights</h3>
              </div>
              <div className="space-y-3">
              {insights.slice(0, 3).map((insight) => (
                <div key={insight.id} className="group/insight relative bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-emerald-400/30 transition-all duration-300 p-3">
                  <div className="flex items-start gap-3">
                    <div className="flex-shrink-0">
                      <div className="p-1 bg-gradient-to-br from-emerald-400 to-teal-500 rounded">
                        {getInsightIcon(insight.type)}
                      </div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-2">
                        <Badge
                          className={`text-xs text-white ${getPriorityColor(insight.priority).replace('bg-', 'bg-')} border-0`}
                        >
                          {insight.priority}
                        </Badge>
                        <span className="text-xs text-slate-400">{insight.type}</span>
                      </div>
                      <p className="text-sm text-white font-medium truncate">
                        {insight.title}
                      </p>
                      <p className="text-xs text-slate-400 line-clamp-2">
                        {insight.description}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
              </div>
            </div>
          </div>
        </TabsContent>

        {/* Predictions Tab */}
        <TabsContent value="predictions" className="space-y-3">
          <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-cyan-400/50 transition-all duration-300">
            <div className="p-4">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-1 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-lg">
                  <Brain className="h-4 w-4 text-white" />
                </div>
                <h3 className="text-sm font-bold text-white">Consciousness Predictions</h3>
              </div>
              <div className="space-y-3">
              {predictions.slice(0, 5).map((prediction, index) => (
                <div key={index} className="group/prediction relative bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-cyan-400/30 transition-all duration-300 p-3 space-y-2">
                  <div className="flex justify-between items-center mb-3">
                    <span className="text-xs text-slate-400">
                      {new Date(prediction.timestamp).toLocaleTimeString()}
                    </span>
                    <Badge className="bg-blue-500/20 text-blue-300 text-xs border-0">
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
              </div>
            </div>
          </div>
        </TabsContent>

        {/* Insights Tab */}
        <TabsContent value="insights" className="space-y-3">
          <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-blue-400/50 transition-all duration-300">
            <div className="p-4">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-1 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-lg">
                  <Zap className="h-4 w-4 text-white" />
                </div>
                <h3 className="text-sm font-bold text-white">AI Insights</h3>
              </div>
              <div className="space-y-3">
              {insights.map((insight) => (
                <div key={insight.id} className="group/insight relative bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-blue-400/30 transition-all duration-300 p-3">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center gap-3">
                      <div className="p-1 bg-gradient-to-br from-blue-400 to-indigo-500 rounded">
                        {getInsightIcon(insight.type)}
                      </div>
                      <span className="text-sm font-medium text-white">
                        {insight.title}
                      </span>
                    </div>
                    <Badge className={`text-xs text-white ${getPriorityColor(insight.priority).replace('bg-', 'bg-')} border-0`}>
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
              </div>
            </div>
          </div>
        </TabsContent>
      </Tabs>

      {/* Mobile Footer */}
      <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-teal-400/50 transition-all duration-300 p-3 mt-4">
        <div className="text-center text-xs text-slate-400">
          <div className="flex items-center justify-center gap-2">
            <div className="p-1 bg-gradient-to-br from-teal-400 to-cyan-500 rounded">
              <Move className="w-3 h-3 text-white" />
            </div>
            <span>Swipe between tabs for more details</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MobilePredictiveAnalytics;
