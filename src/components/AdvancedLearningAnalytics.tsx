import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { 
  Brain, 
  TrendingUp, 
  Target, 
  Zap, 
  BookOpen, 
  Lightbulb, 
  BarChart3, 
  PieChart, 
  Activity,
  Award,
  Clock,
  Star,
  ArrowUp,
  ArrowDown,
  Minus
} from 'lucide-react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  BarChart, 
  Bar, 
  PieChart as RechartsPieChart, 
  Pie, 
  Cell,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ScatterChart,
  Scatter
} from 'recharts';

interface LearningPattern {
  concept: string;
  mastery_level: number;
  learning_velocity: number;
  retention_rate: number;
  difficulty_score: number;
  importance_score: number;
  last_accessed: string;
  access_frequency: number;
  learning_efficiency: number;
  cognitive_load: number;
}

interface LearningMilestone {
  id: string;
  concept: string;
  achievement: string;
  timestamp: string;
  impact_score: number;
  learning_type: 'conceptual' | 'procedural' | 'metacognitive' | 'emotional';
  difficulty_level: number;
}

interface LearningInsight {
  type: 'pattern' | 'anomaly' | 'recommendation' | 'prediction';
  title: string;
  description: string;
  confidence: number;
  impact: 'high' | 'medium' | 'low';
  actionable: boolean;
  category: string;
}

interface AdvancedLearningAnalyticsProps {
  learningPatterns: LearningPattern[];
  milestones: LearningMilestone[];
  insights: LearningInsight[];
  realTimeData?: any;
}

const AdvancedLearningAnalytics: React.FC<AdvancedLearningAnalyticsProps> = ({
  learningPatterns = [],
  milestones = [],
  insights = [],
  realTimeData
}) => {
  const [selectedTimeframe, setSelectedTimeframe] = useState('7d');
  const [selectedMetric, setSelectedMetric] = useState('mastery_level');
  const [viewMode, setViewMode] = useState<'overview' | 'patterns' | 'milestones' | 'insights'>('overview');
  const [sortBy, setSortBy] = useState('mastery_level');
  const [filterDifficulty, setFilterDifficulty] = useState('all');

  // Generate sample data if none provided
  const samplePatterns: LearningPattern[] = learningPatterns.length > 0 ? learningPatterns : [
    {
      concept: 'Neural Networks',
      mastery_level: 0.85,
      learning_velocity: 0.72,
      retention_rate: 0.91,
      difficulty_score: 0.78,
      importance_score: 0.95,
      last_accessed: new Date().toISOString(),
      access_frequency: 45,
      learning_efficiency: 0.88,
      cognitive_load: 0.65
    },
    {
      concept: 'Consciousness Theory',
      mastery_level: 0.92,
      learning_velocity: 0.68,
      retention_rate: 0.89,
      difficulty_score: 0.85,
      importance_score: 0.98,
      last_accessed: new Date(Date.now() - 3600000).toISOString(),
      access_frequency: 38,
      learning_efficiency: 0.94,
      cognitive_load: 0.72
    },
    {
      concept: 'Memory Systems',
      mastery_level: 0.76,
      learning_velocity: 0.81,
      retention_rate: 0.87,
      difficulty_score: 0.65,
      importance_score: 0.82,
      last_accessed: new Date(Date.now() - 7200000).toISOString(),
      access_frequency: 52,
      learning_efficiency: 0.79,
      cognitive_load: 0.58
    },
    {
      concept: 'Emotional Intelligence',
      mastery_level: 0.68,
      learning_velocity: 0.74,
      retention_rate: 0.83,
      difficulty_score: 0.72,
      importance_score: 0.88,
      last_accessed: new Date(Date.now() - 10800000).toISOString(),
      access_frequency: 29,
      learning_efficiency: 0.71,
      cognitive_load: 0.69
    },
    {
      concept: 'Decision Making',
      mastery_level: 0.89,
      learning_velocity: 0.66,
      retention_rate: 0.93,
      difficulty_score: 0.81,
      importance_score: 0.91,
      last_accessed: new Date(Date.now() - 1800000).toISOString(),
      access_frequency: 41,
      learning_efficiency: 0.86,
      cognitive_load: 0.74
    }
  ];

  const sampleMilestones: LearningMilestone[] = milestones.length > 0 ? milestones : [
    {
      id: '1',
      concept: 'Neural Networks',
      achievement: 'Achieved 85% mastery in backpropagation',
      timestamp: new Date(Date.now() - 86400000).toISOString(),
      impact_score: 0.92,
      learning_type: 'conceptual',
      difficulty_level: 0.8
    },
    {
      id: '2',
      concept: 'Consciousness Theory',
      achievement: 'Developed new consciousness framework',
      timestamp: new Date(Date.now() - 172800000).toISOString(),
      impact_score: 0.98,
      learning_type: 'metacognitive',
      difficulty_level: 0.9
    },
    {
      id: '3',
      concept: 'Memory Systems',
      achievement: 'Optimized memory retrieval algorithm',
      timestamp: new Date(Date.now() - 259200000).toISOString(),
      impact_score: 0.87,
      learning_type: 'procedural',
      difficulty_level: 0.7
    }
  ];

  const sampleInsights: LearningInsight[] = insights.length > 0 ? insights : [
    {
      type: 'pattern',
      title: 'Accelerated Learning in Neural Networks',
      description: 'Learning velocity increased by 23% over the past week, indicating strong conceptual understanding.',
      confidence: 0.89,
      impact: 'high',
      actionable: true,
      category: 'Performance'
    },
    {
      type: 'recommendation',
      title: 'Focus on Emotional Intelligence',
      description: 'Mastery level is below average. Consider more practice sessions and real-world applications.',
      confidence: 0.76,
      impact: 'medium',
      actionable: true,
      category: 'Improvement'
    },
    {
      type: 'prediction',
      title: 'Consciousness Theory Mastery Prediction',
      description: 'Based on current learning patterns, 95% mastery expected within 2 weeks.',
      confidence: 0.82,
      impact: 'high',
      actionable: false,
      category: 'Forecasting'
    }
  ];

  const filteredPatterns = samplePatterns.filter(pattern => {
    if (filterDifficulty === 'all') return true;
    if (filterDifficulty === 'easy') return pattern.difficulty_score < 0.4;
    if (filterDifficulty === 'medium') return pattern.difficulty_score >= 0.4 && pattern.difficulty_score < 0.7;
    if (filterDifficulty === 'hard') return pattern.difficulty_score >= 0.7;
    return true;
  }).sort((a, b) => {
    const aVal = a[sortBy as keyof LearningPattern] as number;
    const bVal = b[sortBy as keyof LearningPattern] as number;
    return bVal - aVal;
  });

  const getDifficultyColor = (difficulty: number) => {
    if (difficulty < 0.4) return 'text-green-400';
    if (difficulty < 0.7) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'high': return 'text-red-400 bg-red-400/20';
      case 'medium': return 'text-yellow-400 bg-yellow-400/20';
      case 'low': return 'text-green-400 bg-green-400/20';
      default: return 'text-gray-400 bg-gray-400/20';
    }
  };

  const getLearningTypeColor = (type: string) => {
    switch (type) {
      case 'conceptual': return 'text-blue-400';
      case 'procedural': return 'text-green-400';
      case 'metacognitive': return 'text-purple-400';
      case 'emotional': return 'text-pink-400';
      default: return 'text-gray-400';
    }
  };

  const getInsightIcon = (type: string) => {
    switch (type) {
      case 'pattern': return <TrendingUp className="h-4 w-4" />;
      case 'anomaly': return <Activity className="h-4 w-4" />;
      case 'recommendation': return <Lightbulb className="h-4 w-4" />;
      case 'prediction': return <Target className="h-4 w-4" />;
      default: return <Brain className="h-4 w-4" />;
    }
  };

  const radarData = [
    {
      subject: 'Mastery',
      A: 0.85,
      B: 0.92,
      C: 0.76,
      D: 0.68,
      E: 0.89
    },
    {
      subject: 'Velocity',
      A: 0.72,
      B: 0.68,
      C: 0.81,
      D: 0.74,
      E: 0.66
    },
    {
      subject: 'Retention',
      A: 0.91,
      B: 0.89,
      C: 0.87,
      D: 0.83,
      E: 0.93
    },
    {
      subject: 'Efficiency',
      A: 0.88,
      B: 0.94,
      C: 0.79,
      D: 0.71,
      E: 0.86
    },
    {
      subject: 'Frequency',
      A: 0.45,
      B: 0.38,
      C: 0.52,
      D: 0.29,
      E: 0.41
    }
  ];

  const learningTrendData = [
    { time: 'Week 1', mastery: 0.65, velocity: 0.58, efficiency: 0.72 },
    { time: 'Week 2', mastery: 0.72, velocity: 0.64, efficiency: 0.78 },
    { time: 'Week 3', mastery: 0.78, velocity: 0.69, efficiency: 0.82 },
    { time: 'Week 4', mastery: 0.83, velocity: 0.73, efficiency: 0.85 },
    { time: 'Week 5', mastery: 0.87, velocity: 0.76, efficiency: 0.88 },
    { time: 'Week 6', mastery: 0.90, velocity: 0.78, efficiency: 0.91 }
  ];

  return (
    <div className="space-y-6">
      {/* Header Controls */}
      <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-blue-400/50 transition-all duration-300">
        <div className="p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-blue-400 to-cyan-500 rounded-lg">
              <Brain className="h-6 w-6 text-white" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-white">Advanced Learning Analytics</h2>
              <p className="text-slate-400 text-sm">Comprehensive analysis of learning patterns and cognitive development</p>
            </div>
          </div>
          <div className="flex flex-wrap gap-4">
            <Select value={selectedTimeframe} onValueChange={setSelectedTimeframe}>
              <SelectTrigger className="w-32 bg-slate-700 border-slate-600 hover:border-cyan-400/50 transition-colors">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="1d">1 Day</SelectItem>
                <SelectItem value="7d">7 Days</SelectItem>
                <SelectItem value="30d">30 Days</SelectItem>
                <SelectItem value="90d">90 Days</SelectItem>
              </SelectContent>
            </Select>

            <Select value={selectedMetric} onValueChange={setSelectedMetric}>
              <SelectTrigger className="w-40 bg-slate-700 border-slate-600 hover:border-cyan-400/50 transition-colors">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="mastery_level">Mastery Level</SelectItem>
                <SelectItem value="learning_velocity">Learning Velocity</SelectItem>
                <SelectItem value="retention_rate">Retention Rate</SelectItem>
                <SelectItem value="learning_efficiency">Learning Efficiency</SelectItem>
              </SelectContent>
            </Select>

            <Select value={filterDifficulty} onValueChange={setFilterDifficulty}>
              <SelectTrigger className="w-32 bg-slate-700 border-slate-600 hover:border-cyan-400/50 transition-colors">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Levels</SelectItem>
                <SelectItem value="easy">Easy</SelectItem>
                <SelectItem value="medium">Medium</SelectItem>
                <SelectItem value="hard">Hard</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </div>

      <Tabs value={viewMode} onValueChange={(value: any) => setViewMode(value)} className="space-y-4">
        <TabsList className="grid w-full grid-cols-4 bg-slate-800">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="patterns">Learning Patterns</TabsTrigger>
          <TabsTrigger value="milestones">Milestones</TabsTrigger>
          <TabsTrigger value="insights">AI Insights</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-4">
          {/* Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="group/stat relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-blue-400/50 transition-all duration-300">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-cyan-500">
                    <Award className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <p className="text-sm text-slate-300">Average Mastery</p>
                    <p className="text-2xl font-bold text-blue-300">
                      {(filteredPatterns.reduce((sum, p) => sum + p.mastery_level, 0) / filteredPatterns.length * 100).toFixed(1)}%
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div className="group/stat relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-green-400/50 transition-all duration-300">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-green-400 to-emerald-500">
                    <TrendingUp className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <p className="text-sm text-slate-300">Learning Velocity</p>
                    <p className="text-2xl font-bold text-green-300">
                      {(filteredPatterns.reduce((sum, p) => sum + p.learning_velocity, 0) / filteredPatterns.length * 100).toFixed(1)}%
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div className="group/stat relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-purple-400/50 transition-all duration-300">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-purple-400 to-pink-500">
                    <BookOpen className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <p className="text-sm text-slate-300">Retention Rate</p>
                    <p className="text-2xl font-bold text-purple-300">
                      {(filteredPatterns.reduce((sum, p) => sum + p.retention_rate, 0) / filteredPatterns.length * 100).toFixed(1)}%
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div className="group/stat relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-orange-400/50 transition-all duration-300">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-orange-400 to-yellow-500">
                    <Star className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <p className="text-sm text-slate-300">Total Milestones</p>
                    <p className="text-2xl font-bold text-orange-300">{sampleMilestones.length}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Learning Trend Chart */}
          <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-green-400/50 transition-all duration-300">
            <div className="p-6">
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-gradient-to-br from-green-400 to-emerald-500 rounded-lg">
                  <TrendingUp className="h-6 w-6 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-white">Learning Progress Trend</h3>
                  <p className="text-slate-400 text-sm">Track mastery, velocity, and efficiency over time</p>
                </div>
              </div>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={learningTrendData}>
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
                    <Line type="monotone" dataKey="mastery" stroke="#3B82F6" strokeWidth={2} name="Mastery" />
                    <Line type="monotone" dataKey="velocity" stroke="#10B981" strokeWidth={2} name="Velocity" />
                    <Line type="monotone" dataKey="efficiency" stroke="#8B5CF6" strokeWidth={2} name="Efficiency" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          {/* Learning Radar Chart */}
          <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-purple-400/50 transition-all duration-300">
            <div className="p-6">
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-gradient-to-br from-purple-400 to-pink-500 rounded-lg">
                  <Target className="h-6 w-6 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-white">Learning Capabilities Radar</h3>
                  <p className="text-slate-400 text-sm">Multi-dimensional learning capability assessment</p>
                </div>
              </div>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart data={radarData}>
                    <PolarGrid stroke="#374151" />
                    <PolarAngleAxis dataKey="subject" stroke="#9CA3AF" />
                    <PolarRadiusAxis stroke="#9CA3AF" domain={[0, 1]} />
                    <Radar name="Neural Networks" dataKey="A" stroke="#3B82F6" fill="#3B82F6" fillOpacity={0.3} />
                    <Radar name="Consciousness Theory" dataKey="B" stroke="#10B981" fill="#10B981" fillOpacity={0.3} />
                    <Radar name="Memory Systems" dataKey="C" stroke="#8B5CF6" fill="#8B5CF6" fillOpacity={0.3} />
                    <Radar name="Emotional Intelligence" dataKey="D" stroke="#F59E0B" fill="#F59E0B" fillOpacity={0.3} />
                    <Radar name="Decision Making" dataKey="E" stroke="#EF4444" fill="#EF4444" fillOpacity={0.3} />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        </TabsContent>

        {/* Learning Patterns Tab */}
        <TabsContent value="patterns" className="space-y-4">
          <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-cyan-400/50 transition-all duration-300">
            <div className="p-6">
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-lg">
                  <BarChart3 className="h-6 w-6 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-white">Learning Patterns Analysis</h3>
                  <p className="text-slate-400 text-sm">Detailed analysis of individual learning patterns and metrics</p>
                </div>
              </div>
              <div className="space-y-4">
                {filteredPatterns.map((pattern, index) => (
                  <div key={index} className="group/pattern relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-cyan-400/30 transition-all duration-300">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="text-lg font-semibold text-white">{pattern.concept}</h3>
                      <div className="flex items-center gap-2">
                        <Badge className={getDifficultyColor(pattern.difficulty_score)}>
                          {pattern.difficulty_score < 0.4 ? 'Easy' : 
                           pattern.difficulty_score < 0.7 ? 'Medium' : 'Hard'}
                        </Badge>
                        <span className="text-sm text-slate-300">
                          {new Date(pattern.last_accessed).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-3">
                      <div>
                        <div className="text-sm text-slate-300 mb-1">Mastery Level</div>
                        <div className="flex items-center gap-2">
                          <Progress value={pattern.mastery_level * 100} className="flex-1" />
                          <span className="text-sm font-medium">{(pattern.mastery_level * 100).toFixed(1)}%</span>
                        </div>
                      </div>
                      <div>
                        <div className="text-sm text-slate-300 mb-1">Learning Velocity</div>
                        <div className="flex items-center gap-2">
                          <Progress value={pattern.learning_velocity * 100} className="flex-1" />
                          <span className="text-sm font-medium">{(pattern.learning_velocity * 100).toFixed(1)}%</span>
                        </div>
                      </div>
                      <div>
                        <div className="text-sm text-slate-300 mb-1">Retention Rate</div>
                        <div className="flex items-center gap-2">
                          <Progress value={pattern.retention_rate * 100} className="flex-1" />
                          <span className="text-sm font-medium">{(pattern.retention_rate * 100).toFixed(1)}%</span>
                        </div>
                      </div>
                      <div>
                        <div className="text-sm text-slate-300 mb-1">Efficiency</div>
                        <div className="flex items-center gap-2">
                          <Progress value={pattern.learning_efficiency * 100} className="flex-1" />
                          <span className="text-sm font-medium">{(pattern.learning_efficiency * 100).toFixed(1)}%</span>
                        </div>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <span className="text-slate-300">Access Frequency:</span>
                        <span className="ml-2 font-medium">{pattern.access_frequency}</span>
                      </div>
                      <div>
                        <span className="text-slate-300">Cognitive Load:</span>
                        <span className="ml-2 font-medium">{(pattern.cognitive_load * 100).toFixed(1)}%</span>
                      </div>
                      <div>
                        <span className="text-slate-300">Importance:</span>
                        <span className="ml-2 font-medium">{(pattern.importance_score * 100).toFixed(1)}%</span>
                      </div>
                      <div>
                        <span className="text-slate-300">Difficulty:</span>
                        <span className="ml-2 font-medium">{(pattern.difficulty_score * 100).toFixed(1)}%</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </TabsContent>

        {/* Milestones Tab */}
        <TabsContent value="milestones" className="space-y-4">
          <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-orange-400/50 transition-all duration-300">
            <div className="p-6">
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-gradient-to-br from-orange-400 to-yellow-500 rounded-lg">
                  <Award className="h-6 w-6 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-white">Learning Milestones</h3>
                  <p className="text-slate-400 text-sm">Track significant achievements in learning journey</p>
                </div>
              </div>
              <div className="space-y-4">
                {sampleMilestones.map((milestone) => (
                  <div key={milestone.id} className="group/milestone relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-orange-400/30 transition-all duration-300">
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-white">{milestone.concept}</h3>
                        <p className="text-slate-300 mt-1">{milestone.achievement}</p>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge className={getLearningTypeColor(milestone.learning_type)}>
                          {milestone.learning_type}
                        </Badge>
                        <span className="text-sm text-slate-300">
                          {new Date(milestone.timestamp).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-4 text-sm">
                      <div className="flex items-center gap-1">
                        <Star className="h-4 w-4 text-yellow-400" />
                        <span className="text-slate-300">Impact:</span>
                        <span className="font-medium">{(milestone.impact_score * 100).toFixed(1)}%</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <Target className="h-4 w-4 text-blue-400" />
                        <span className="text-slate-300">Difficulty:</span>
                        <span className="font-medium">{(milestone.difficulty_level * 100).toFixed(1)}%</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </TabsContent>

        {/* AI Insights Tab */}
        <TabsContent value="insights" className="space-y-4">
          <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-rose-400/50 transition-all duration-300">
            <div className="p-6">
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-gradient-to-br from-rose-400 to-pink-500 rounded-lg">
                  <Lightbulb className="h-6 w-6 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-white">AI-Powered Learning Insights</h3>
                  <p className="text-slate-400 text-sm">Intelligent recommendations and pattern analysis</p>
                </div>
              </div>
              <div className="space-y-4">
                {sampleInsights.map((insight, index) => (
                  <div key={index} className="group/insight relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-rose-400/30 transition-all duration-300">
                    <div className="flex items-start gap-3">
                      <div className="flex-shrink-0 mt-1">
                        {getInsightIcon(insight.type)}
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <h3 className="text-lg font-semibold text-white">{insight.title}</h3>
                          <Badge className={getImpactColor(insight.impact)}>
                            {insight.impact} impact
                          </Badge>
                          <Badge variant="outline" className="border-slate-600">
                            {insight.category}
                          </Badge>
                        </div>
                        <p className="text-slate-300 mb-3">{insight.description}</p>
                        <div className="flex items-center gap-4 text-sm">
                          <div className="flex items-center gap-1">
                            <span className="text-slate-300">Confidence:</span>
                            <span className="font-medium">{(insight.confidence * 100).toFixed(1)}%</span>
                          </div>
                          <div className="flex items-center gap-1">
                            <span className="text-slate-300">Actionable:</span>
                            <span className="font-medium">{insight.actionable ? 'Yes' : 'No'}</span>
                          </div>
                          {insight.actionable && (
                            <Button size="sm" className="bg-blue-600 hover:bg-blue-700">
                              Take Action
                            </Button>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default AdvancedLearningAnalytics;
