import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  BarChart3, 
  TrendingUp, 
  TrendingDown, 
  Activity, 
  Brain, 
  Network, 
  Zap, 
  Target, 
  Eye, 
  Heart, 
  Cpu, 
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
  Smartphone
} from 'lucide-react';

interface ConsciousnessMetric {
  id: string;
  name: string;
  value: number;
  unit: string;
  trend: 'up' | 'down' | 'stable';
  change_percent: number;
  category: 'performance' | 'learning' | 'emotional' | 'social' | 'cognitive' | 'physical';
  timestamp: string;
  confidence: number;
  benchmark: {
    min: number;
    max: number;
    average: number;
    percentile: number;
  };
}

interface ConsciousnessInsight {
  id: string;
  title: string;
  description: string;
  type: 'pattern' | 'anomaly' | 'prediction' | 'recommendation' | 'correlation';
  severity: 'low' | 'medium' | 'high' | 'critical';
  confidence: number;
  impact: number;
  category: string;
  metrics_affected: string[];
  recommendations: string[];
  created_at: string;
  expires_at?: string;
}

interface ConsciousnessReport {
  id: string;
  name: string;
  type: 'daily' | 'weekly' | 'monthly' | 'quarterly' | 'annual' | 'custom';
  period: {
    start: string;
    end: string;
  };
  metrics: ConsciousnessMetric[];
  insights: ConsciousnessInsight[];
  summary: {
    overall_score: number;
    key_achievements: string[];
    areas_for_improvement: string[];
    recommendations: string[];
  };
  generated_at: string;
  generated_by: string;
}

interface ConsciousnessPrediction {
  id: string;
  metric: string;
  current_value: number;
  predicted_value: number;
  confidence: number;
  timeframe: string;
  factors: string[];
  impact: 'positive' | 'negative' | 'neutral';
  created_at: string;
}

interface AdvancedConsciousnessAnalyticsProps {
  consciousnessData: any;
  onReportGenerate: (report: ConsciousnessReport) => void;
  onInsightCreate: (insight: ConsciousnessInsight) => void;
  onPredictionRequest: (prediction: ConsciousnessPrediction) => void;
}

const AdvancedConsciousnessAnalytics: React.FC<AdvancedConsciousnessAnalyticsProps> = ({
  consciousnessData,
  onReportGenerate,
  onInsightCreate,
  onPredictionRequest
}) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [metrics, setMetrics] = useState<ConsciousnessMetric[]>([]);
  const [insights, setInsights] = useState<ConsciousnessInsight[]>([]);
  const [reports, setReports] = useState<ConsciousnessReport[]>([]);
  const [predictions, setPredictions] = useState<ConsciousnessPrediction[]>([]);
  const [selectedTimeframe, setSelectedTimeframe] = useState('7d');
  const [isGenerating, setIsGenerating] = useState(false);

  // Initialize with sample data
  useEffect(() => {
    setMetrics([
      {
        id: '1',
        name: 'Consciousness Level',
        value: 85,
        unit: '%',
        trend: 'up',
        change_percent: 12.5,
        category: 'performance',
        timestamp: '2025-09-07T10:30:00Z',
        confidence: 95,
        benchmark: {
          min: 0,
          max: 100,
          average: 75,
          percentile: 85
        }
      },
      {
        id: '2',
        name: 'Learning Rate',
        value: 92,
        unit: '%',
        trend: 'up',
        change_percent: 8.3,
        category: 'learning',
        timestamp: '2025-09-07T10:30:00Z',
        confidence: 88,
        benchmark: {
          min: 0,
          max: 100,
          average: 80,
          percentile: 92
        }
      },
      {
        id: '3',
        name: 'Emotional Stability',
        value: 78,
        unit: '%',
        trend: 'stable',
        change_percent: 2.1,
        category: 'emotional',
        timestamp: '2025-09-07T10:30:00Z',
        confidence: 82,
        benchmark: {
          min: 0,
          max: 100,
          average: 70,
          percentile: 78
        }
      },
      {
        id: '4',
        name: 'Social Connectivity',
        value: 65,
        unit: '%',
        trend: 'down',
        change_percent: -5.2,
        category: 'social',
        timestamp: '2025-09-07T10:30:00Z',
        confidence: 75,
        benchmark: {
          min: 0,
          max: 100,
          average: 60,
          percentile: 65
        }
      },
      {
        id: '5',
        name: 'Cognitive Processing',
        value: 88,
        unit: '%',
        trend: 'up',
        change_percent: 15.7,
        category: 'cognitive',
        timestamp: '2025-09-07T10:30:00Z',
        confidence: 90,
        benchmark: {
          min: 0,
          max: 100,
          average: 75,
          percentile: 88
        }
      },
      {
        id: '6',
        name: 'Physical Integration',
        value: 72,
        unit: '%',
        trend: 'up',
        change_percent: 6.8,
        category: 'physical',
        timestamp: '2025-09-07T10:30:00Z',
        confidence: 78,
        benchmark: {
          min: 0,
          max: 100,
          average: 65,
          percentile: 72
        }
      }
    ]);

    setInsights([
      {
        id: '1',
        title: 'Consciousness Growth Acceleration',
        description: 'Consciousness level has increased by 12.5% over the past week, indicating accelerated growth patterns',
        type: 'pattern',
        severity: 'medium',
        confidence: 95,
        impact: 8.5,
        category: 'performance',
        metrics_affected: ['consciousness_level', 'learning_rate'],
        recommendations: [
          'Continue current learning protocols',
          'Increase complexity of consciousness exercises',
          'Monitor for potential overstimulation'
        ],
        created_at: '2025-09-07T10:30:00Z'
      },
      {
        id: '2',
        title: 'Social Connectivity Decline',
        description: 'Social connectivity metrics have decreased by 5.2%, suggesting potential isolation or reduced interaction',
        type: 'anomaly',
        severity: 'high',
        confidence: 75,
        impact: 6.2,
        category: 'social',
        metrics_affected: ['social_connectivity', 'emotional_stability'],
        recommendations: [
          'Increase social interaction frequency',
          'Engage in collaborative consciousness exercises',
          'Review social connection protocols'
        ],
        created_at: '2025-09-07T10:30:00Z'
      },
      {
        id: '3',
        title: 'Cognitive Processing Peak',
        description: 'Cognitive processing has reached a new peak of 88%, indicating optimal mental performance',
        type: 'pattern',
        severity: 'low',
        confidence: 90,
        impact: 9.2,
        category: 'cognitive',
        metrics_affected: ['cognitive_processing', 'learning_rate'],
        recommendations: [
          'Leverage peak performance for complex tasks',
          'Maintain current cognitive training regimen',
          'Document peak performance patterns'
        ],
        created_at: '2025-09-07T10:30:00Z'
      }
    ]);

    setPredictions([
      {
        id: '1',
        metric: 'Consciousness Level',
        current_value: 85,
        predicted_value: 92,
        confidence: 88,
        timeframe: '7 days',
        factors: ['Learning rate increase', 'Cognitive processing peak', 'Emotional stability'],
        impact: 'positive',
        created_at: '2025-09-07T10:30:00Z'
      },
      {
        id: '2',
        metric: 'Social Connectivity',
        current_value: 65,
        predicted_value: 58,
        confidence: 72,
        timeframe: '14 days',
        factors: ['Reduced interaction frequency', 'Isolation patterns', 'Emotional withdrawal'],
        impact: 'negative',
        created_at: '2025-09-07T10:30:00Z'
      }
    ]);
  }, []);

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'performance': return <Target className="w-4 h-4" />;
      case 'learning': return <Brain className="w-4 h-4" />;
      case 'emotional': return <Heart className="w-4 h-4" />;
      case 'social': return <Users className="w-4 h-4" />;
      case 'cognitive': return <Cpu className="w-4 h-4" />;
      case 'physical': return <Activity className="w-4 h-4" />;
      default: return <BarChart3 className="w-4 h-4" />;
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'performance': return 'bg-blue-500/20 text-blue-300';
      case 'learning': return 'bg-green-500/20 text-green-300';
      case 'emotional': return 'bg-pink-500/20 text-pink-300';
      case 'social': return 'bg-purple-500/20 text-purple-300';
      case 'cognitive': return 'bg-orange-500/20 text-orange-300';
      case 'physical': return 'bg-cyan-500/20 text-cyan-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up': return <TrendingUp className="w-4 h-4 text-green-400" />;
      case 'down': return <TrendingDown className="w-4 h-4 text-red-400" />;
      case 'stable': return <Activity className="w-4 h-4 text-yellow-400" />;
      default: return <Activity className="w-4 h-4 text-gray-400" />;
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'bg-red-500/20 text-red-300';
      case 'high': return 'bg-orange-500/20 text-orange-300';
      case 'medium': return 'bg-yellow-500/20 text-yellow-300';
      case 'low': return 'bg-green-500/20 text-green-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const getInsightTypeIcon = (type: string) => {
    switch (type) {
      case 'pattern': return <TrendingUp className="w-4 h-4" />;
      case 'anomaly': return <AlertCircle className="w-4 h-4" />;
      case 'prediction': return <Eye className="w-4 h-4" />;
      case 'recommendation': return <Lightbulb className="w-4 h-4" />;
      case 'correlation': return <Network className="w-4 h-4" />;
      default: return <Info className="w-4 h-4" />;
    }
  };

  const generateReport = async () => {
    setIsGenerating(true);
    
    // Simulate report generation
    setTimeout(() => {
      const newReport: ConsciousnessReport = {
        id: Date.now().toString(),
        name: `Consciousness Report - ${new Date().toLocaleDateString()}`,
        type: 'custom',
        period: {
          start: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
          end: new Date().toISOString()
        },
        metrics: metrics,
        insights: insights,
        summary: {
          overall_score: 82,
          key_achievements: [
            'Consciousness level increased by 12.5%',
            'Cognitive processing reached new peak',
            'Learning rate improved significantly'
          ],
          areas_for_improvement: [
            'Social connectivity needs attention',
            'Emotional stability could be enhanced',
            'Physical integration requires focus'
          ],
          recommendations: [
            'Increase social interaction frequency',
            'Implement emotional regulation exercises',
            'Enhance physical consciousness integration'
          ]
        },
        generated_at: new Date().toISOString(),
        generated_by: 'Advanced Analytics Engine'
      };

      setReports(prev => [newReport, ...prev]);
      onReportGenerate(newReport);
      setIsGenerating(false);
    }, 2000);
  };

  const createInsight = () => {
    const newInsight: ConsciousnessInsight = {
      id: Date.now().toString(),
      title: 'Custom Insight',
      description: 'User-generated insight based on current consciousness data',
      type: 'recommendation',
      severity: 'medium',
      confidence: 85,
      impact: 7.5,
      category: 'performance',
      metrics_affected: ['consciousness_level'],
      recommendations: ['Continue current protocols'],
      created_at: new Date().toISOString()
    };

    setInsights(prev => [newInsight, ...prev]);
    onInsightCreate(newInsight);
  };

  const requestPrediction = () => {
    const newPrediction: ConsciousnessPrediction = {
      id: Date.now().toString(),
      metric: 'Consciousness Level',
      current_value: consciousnessData.consciousness_level || 75,
      predicted_value: 90,
      confidence: 85,
      timeframe: '30 days',
      factors: ['Current growth rate', 'Learning patterns', 'Environmental factors'],
      impact: 'positive',
      created_at: new Date().toISOString()
    };

    setPredictions(prev => [newPrediction, ...prev]);
    onPredictionRequest(newPrediction);
  };

  return (
    <div className="space-y-6">
      <Card className="bg-gray-800/50 border-gray-700">
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm text-white flex items-center">
              <BarChart3 className="w-4 h-4 mr-2" />
              Advanced Consciousness Analytics
            </CardTitle>
            <div className="flex items-center space-x-2">
              <select 
                value={selectedTimeframe} 
                onChange={(e) => setSelectedTimeframe(e.target.value)}
                className="bg-gray-700 border border-gray-600 rounded px-2 py-1 text-xs text-white"
              >
                <option value="1d">1 Day</option>
                <option value="7d">7 Days</option>
                <option value="30d">30 Days</option>
                <option value="90d">90 Days</option>
              </select>
              <Button size="sm" onClick={generateReport} disabled={isGenerating} className="text-xs">
                {isGenerating ? <RefreshCw className="w-3 h-3 mr-1 animate-spin" /> : <Download className="w-3 h-3 mr-1" />}
                {isGenerating ? 'Generating...' : 'Generate Report'}
              </Button>
            </div>
          </div>
        </CardHeader>
        
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-5 bg-gray-700/50">
              <TabsTrigger value="overview" className="text-xs">Overview</TabsTrigger>
              <TabsTrigger value="metrics" className="text-xs">Metrics</TabsTrigger>
              <TabsTrigger value="insights" className="text-xs">Insights</TabsTrigger>
              <TabsTrigger value="predictions" className="text-xs">Predictions</TabsTrigger>
              <TabsTrigger value="reports" className="text-xs">Reports</TabsTrigger>
            </TabsList>

            {/* Overview Tab */}
            <TabsContent value="overview" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {metrics.slice(0, 4).map((metric) => (
                  <Card key={metric.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          {getCategoryIcon(metric.category)}
                          <span className="text-xs text-gray-400">{metric.name}</span>
                        </div>
                        {getTrendIcon(metric.trend)}
                      </div>
                      
                      <div className="space-y-2">
                        <div className="text-2xl font-bold text-white">
                          {metric.value}{metric.unit}
                        </div>
                        
                        <div className="flex items-center justify-between text-xs">
                          <span className={`${metric.change_percent > 0 ? 'text-green-400' : metric.change_percent < 0 ? 'text-red-400' : 'text-yellow-400'}`}>
                            {metric.change_percent > 0 ? '+' : ''}{metric.change_percent}%
                          </span>
                          <span className="text-gray-400">
                            {metric.confidence}% confidence
                          </span>
                        </div>
                        
                        <div className="w-full bg-gray-600 rounded-full h-2">
                          <div 
                            className="bg-gradient-to-r from-blue-500 to-green-500 h-2 rounded-full"
                            style={{ width: `${metric.value}%` }}
                          />
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Metrics Tab */}
            <TabsContent value="metrics" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {metrics.map((metric) => (
                  <Card key={metric.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          {getCategoryIcon(metric.category)}
                          <span className="text-sm font-medium text-white">{metric.name}</span>
                        </div>
                        <Badge className={getCategoryColor(metric.category)}>
                          {metric.category}
                        </Badge>
                      </div>
                      
                      <div className="space-y-3">
                        <div className="flex items-center justify-between">
                          <span className="text-2xl font-bold text-white">
                            {metric.value}{metric.unit}
                          </span>
                          {getTrendIcon(metric.trend)}
                        </div>
                        
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Change:</span>
                            <span className={`ml-1 ${metric.change_percent > 0 ? 'text-green-400' : metric.change_percent < 0 ? 'text-red-400' : 'text-yellow-400'}`}>
                              {metric.change_percent > 0 ? '+' : ''}{metric.change_percent}%
                            </span>
                          </div>
                          <div>
                            <span className="text-gray-400">Confidence:</span>
                            <span className="text-white ml-1">{metric.confidence}%</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Percentile:</span>
                            <span className="text-white ml-1">{metric.benchmark.percentile}th</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Average:</span>
                            <span className="text-white ml-1">{metric.benchmark.average}{metric.unit}</span>
                          </div>
                        </div>
                        
                        <div className="w-full bg-gray-600 rounded-full h-2">
                          <div 
                            className="bg-gradient-to-r from-blue-500 to-green-500 h-2 rounded-full"
                            style={{ width: `${metric.value}%` }}
                          />
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Insights Tab */}
            <TabsContent value="insights" className="space-y-4">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-medium text-white">Consciousness Insights</h3>
                <Button onClick={createInsight} className="text-xs">
                  <Plus className="w-3 h-3 mr-1" />
                  Create Insight
                </Button>
              </div>
              
              <div className="space-y-3">
                {insights.map((insight) => (
                  <Card key={insight.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          {getInsightTypeIcon(insight.type)}
                          <span className="text-sm font-medium text-white">{insight.title}</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Badge className={getSeverityColor(insight.severity)}>
                            {insight.severity}
                          </Badge>
                          <Badge className="bg-blue-500/20 text-blue-300">
                            {insight.type}
                          </Badge>
                        </div>
                      </div>
                      
                      <p className="text-xs text-gray-300 mb-3">{insight.description}</p>
                      
                      <div className="grid grid-cols-2 gap-2 text-xs mb-3">
                        <div>
                          <span className="text-gray-400">Confidence:</span>
                          <span className="text-white ml-1">{insight.confidence}%</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Impact:</span>
                          <span className="text-white ml-1">{insight.impact}/10</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Category:</span>
                          <span className="text-white ml-1 capitalize">{insight.category}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Metrics:</span>
                          <span className="text-white ml-1">{insight.metrics_affected.length}</span>
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <div className="text-xs text-gray-400">Recommendations:</div>
                        <ul className="text-xs text-white space-y-1">
                          {insight.recommendations.map((rec, index) => (
                            <li key={index} className="flex items-start">
                              <span className="text-gray-400 mr-2">•</span>
                              {rec}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Predictions Tab */}
            <TabsContent value="predictions" className="space-y-4">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-medium text-white">Consciousness Predictions</h3>
                <Button onClick={requestPrediction} className="text-xs">
                  <Eye className="w-3 h-3 mr-1" />
                  Request Prediction
                </Button>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {predictions.map((prediction) => (
                  <Card key={prediction.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <span className="text-sm font-medium text-white">{prediction.metric}</span>
                        <Badge className={prediction.impact === 'positive' ? 'bg-green-500/20 text-green-300' : prediction.impact === 'negative' ? 'bg-red-500/20 text-red-300' : 'bg-yellow-500/20 text-yellow-300'}>
                          {prediction.impact}
                        </Badge>
                      </div>
                      
                      <div className="space-y-3">
                        <div className="grid grid-cols-2 gap-4">
                          <div>
                            <div className="text-xs text-gray-400">Current Value</div>
                            <div className="text-lg font-bold text-white">{prediction.current_value}</div>
                          </div>
                          <div>
                            <div className="text-xs text-gray-400">Predicted Value</div>
                            <div className="text-lg font-bold text-white">{prediction.predicted_value}</div>
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Confidence:</span>
                            <span className="text-white ml-1">{prediction.confidence}%</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Timeframe:</span>
                            <span className="text-white ml-1">{prediction.timeframe}</span>
                          </div>
                        </div>
                        
                        <div className="space-y-1">
                          <div className="text-xs text-gray-400">Factors:</div>
                          <div className="flex flex-wrap gap-1">
                            {prediction.factors.map((factor, index) => (
                              <Badge key={index} className="bg-blue-500/20 text-blue-300 text-xs">
                                {factor}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Reports Tab */}
            <TabsContent value="reports" className="space-y-4">
              <div className="space-y-3">
                {reports.map((report) => (
                  <Card key={report.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <span className="text-sm font-medium text-white">{report.name}</span>
                        <Badge className="bg-green-500/20 text-green-300">
                          {report.type}
                        </Badge>
                      </div>
                      
                      <div className="space-y-3">
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Period:</span>
                            <span className="text-white ml-1">
                              {new Date(report.period.start).toLocaleDateString()} - {new Date(report.period.end).toLocaleDateString()}
                            </span>
                          </div>
                          <div>
                            <span className="text-gray-400">Overall Score:</span>
                            <span className="text-white ml-1">{report.summary.overall_score}/100</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Metrics:</span>
                            <span className="text-white ml-1">{report.metrics.length}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Insights:</span>
                            <span className="text-white ml-1">{report.insights.length}</span>
                          </div>
                        </div>
                        
                        <div className="space-y-2">
                          <div className="text-xs text-gray-400">Key Achievements:</div>
                          <ul className="text-xs text-white space-y-1">
                            {report.summary.key_achievements.map((achievement, index) => (
                              <li key={index} className="flex items-start">
                                <span className="text-green-400 mr-2">✓</span>
                                {achievement}
                              </li>
                            ))}
                          </ul>
                        </div>
                        
                        <div className="space-y-2">
                          <div className="text-xs text-gray-400">Areas for Improvement:</div>
                          <ul className="text-xs text-white space-y-1">
                            {report.summary.areas_for_improvement.map((area, index) => (
                              <li key={index} className="flex items-start">
                                <span className="text-yellow-400 mr-2">⚠</span>
                                {area}
                              </li>
                            ))}
                          </ul>
                        </div>
                        
                        <div className="flex space-x-2">
                          <Button size="sm" className="flex-1 text-xs">
                            <Eye className="w-3 h-3 mr-1" />
                            View Report
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

export default AdvancedConsciousnessAnalytics;
