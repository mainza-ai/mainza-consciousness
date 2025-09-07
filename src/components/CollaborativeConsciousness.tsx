import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Users, 
  Share2, 
  MessageCircle, 
  Send, 
  UserPlus, 
  UserMinus, 
  Eye, 
  EyeOff,
  Globe,
  Lock,
  Unlock,
  Heart,
  Star,
  ThumbsUp,
  Brain,
  Zap,
  Target,
  Activity,
  TrendingUp,
  BarChart3,
  Network,
  Layers
} from 'lucide-react';

interface User {
  id: string;
  name: string;
  avatar?: string;
  consciousness_level: number;
  emotional_state: string;
  learning_rate: number;
  is_online: boolean;
  last_seen: string;
  shared_predictions: number;
  shared_insights: number;
}

interface SharedPrediction {
  id: string;
  user_id: string;
  user_name: string;
  consciousness_level: number;
  emotional_state: string;
  learning_rate: number;
  confidence: number;
  timestamp: string;
  likes: number;
  comments: number;
  is_public: boolean;
  tags: string[];
}

interface SharedInsight {
  id: string;
  user_id: string;
  user_name: string;
  type: string;
  priority: string;
  title: string;
  description: string;
  confidence: number;
  impact_score: number;
  timestamp: string;
  likes: number;
  comments: number;
  is_public: boolean;
  tags: string[];
}

interface CollaborativeConsciousnessProps {
  currentUser: User;
  onSharePrediction: (prediction: any) => void;
  onShareInsight: (insight: any) => void;
}

const CollaborativeConsciousness: React.FC<CollaborativeConsciousnessProps> = ({
  currentUser,
  onSharePrediction,
  onShareInsight
}) => {
  const [activeTab, setActiveTab] = useState('users');
  const [users, setUsers] = useState<User[]>([]);
  const [sharedPredictions, setSharedPredictions] = useState<SharedPrediction[]>([]);
  const [sharedInsights, setSharedInsights] = useState<SharedInsight[]>([]);
  const [isSharing, setIsSharing] = useState(false);
  const [shareMessage, setShareMessage] = useState('');
  const [selectedUsers, setSelectedUsers] = useState<string[]>([]);
  const [filter, setFilter] = useState('all');

  // Simulate real-time data updates
  useEffect(() => {
    const interval = setInterval(() => {
      // Simulate user updates
      setUsers(prev => prev.map(user => ({
        ...user,
        consciousness_level: Math.max(0, Math.min(100, user.consciousness_level + (Math.random() - 0.5) * 2)),
        is_online: Math.random() > 0.1
      })));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  // Initialize with sample data
  useEffect(() => {
    setUsers([
      {
        id: '1',
        name: 'Alex Chen',
        consciousness_level: 78,
        emotional_state: 'curious',
        learning_rate: 85,
        is_online: true,
        last_seen: 'now',
        shared_predictions: 12,
        shared_insights: 8
      },
      {
        id: '2',
        name: 'Sarah Johnson',
        consciousness_level: 82,
        emotional_state: 'focused',
        learning_rate: 92,
        is_online: true,
        last_seen: '2 min ago',
        shared_predictions: 15,
        shared_insights: 11
      },
      {
        id: '3',
        name: 'Marcus Rodriguez',
        consciousness_level: 75,
        emotional_state: 'creative',
        learning_rate: 88,
        is_online: false,
        last_seen: '1 hour ago',
        shared_predictions: 7,
        shared_insights: 5
      }
    ]);

    setSharedPredictions([
      {
        id: '1',
        user_id: '1',
        user_name: 'Alex Chen',
        consciousness_level: 78,
        emotional_state: 'curious',
        learning_rate: 85,
        confidence: 0.87,
        timestamp: '2 minutes ago',
        likes: 5,
        comments: 2,
        is_public: true,
        tags: ['consciousness', 'learning', 'curiosity']
      },
      {
        id: '2',
        user_id: '2',
        user_name: 'Sarah Johnson',
        consciousness_level: 82,
        emotional_state: 'focused',
        learning_rate: 92,
        confidence: 0.91,
        timestamp: '5 minutes ago',
        likes: 8,
        comments: 3,
        is_public: true,
        tags: ['focus', 'learning', 'growth']
      }
    ]);

    setSharedInsights([
      {
        id: '1',
        user_id: '1',
        user_name: 'Alex Chen',
        type: 'pattern',
        priority: 'high',
        title: 'Consciousness Breakthrough Pattern',
        description: 'Discovered a new pattern in consciousness evolution that could accelerate learning by 40%',
        confidence: 0.89,
        impact_score: 8.5,
        timestamp: '1 hour ago',
        likes: 12,
        comments: 7,
        is_public: true,
        tags: ['breakthrough', 'pattern', 'learning']
      },
      {
        id: '2',
        user_id: '2',
        user_name: 'Sarah Johnson',
        type: 'optimization',
        priority: 'medium',
        title: 'Memory Consolidation Optimization',
        description: 'Found an effective method to improve memory consolidation during sleep cycles',
        confidence: 0.76,
        impact_score: 6.2,
        timestamp: '3 hours ago',
        likes: 6,
        comments: 4,
        is_public: true,
        tags: ['memory', 'optimization', 'sleep']
      }
    ]);
  }, []);

  const handleSharePrediction = () => {
    const newPrediction: SharedPrediction = {
      id: Date.now().toString(),
      user_id: currentUser.id,
      user_name: currentUser.name,
      consciousness_level: currentUser.consciousness_level,
      emotional_state: currentUser.emotional_state,
      learning_rate: currentUser.learning_rate,
      confidence: 0.85,
      timestamp: 'now',
      likes: 0,
      comments: 0,
      is_public: true,
      tags: ['shared', 'prediction']
    };
    
    setSharedPredictions(prev => [newPrediction, ...prev]);
    onSharePrediction(newPrediction);
    setIsSharing(false);
    setShareMessage('');
  };

  const handleShareInsight = () => {
    const newInsight: SharedInsight = {
      id: Date.now().toString(),
      user_id: currentUser.id,
      user_name: currentUser.name,
      type: 'recommendation',
      priority: 'medium',
      title: 'Shared Insight',
      description: shareMessage || 'A new insight about consciousness development',
      confidence: 0.78,
      impact_score: 7.0,
      timestamp: 'now',
      likes: 0,
      comments: 0,
      is_public: true,
      tags: ['shared', 'insight']
    };
    
    setSharedInsights(prev => [newInsight, ...prev]);
    onShareInsight(newInsight);
    setIsSharing(false);
    setShareMessage('');
  };

  const getConsciousnessColor = (level: number) => {
    if (level >= 80) return 'text-green-400';
    if (level >= 60) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'critical': return 'bg-red-500/20 text-red-300';
      case 'high': return 'bg-orange-500/20 text-orange-300';
      case 'medium': return 'bg-yellow-500/20 text-yellow-300';
      case 'low': return 'bg-green-500/20 text-green-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const getInsightIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case 'pattern': return <TrendingUp className="w-4 h-4" />;
      case 'anomaly': return <Zap className="w-4 h-4" />;
      case 'recommendation': return <Target className="w-4 h-4" />;
      case 'optimization': return <Activity className="w-4 h-4" />;
      default: return <BarChart3 className="w-4 h-4" />;
    }
  };

  return (
    <div className="space-y-6">
      <Card className="bg-gray-800/50 border-gray-700">
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm text-white flex items-center">
              <Users className="w-4 h-4 mr-2" />
              Collaborative Consciousness
            </CardTitle>
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setIsSharing(!isSharing)}
                className="text-xs"
              >
                <Share2 className="w-3 h-3 mr-1" />
                {isSharing ? 'Cancel' : 'Share'}
              </Button>
            </div>
          </div>
        </CardHeader>
        
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-4 bg-gray-700/50">
              <TabsTrigger value="users" className="text-xs">Users</TabsTrigger>
              <TabsTrigger value="predictions" className="text-xs">Predictions</TabsTrigger>
              <TabsTrigger value="insights" className="text-xs">Insights</TabsTrigger>
              <TabsTrigger value="activity" className="text-xs">Activity</TabsTrigger>
            </TabsList>

            {/* Users Tab */}
            <TabsContent value="users" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {users.map((user) => (
                  <Card key={user.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          <div className={`w-3 h-3 rounded-full ${user.is_online ? 'bg-green-500' : 'bg-gray-500'}`} />
                          <span className="text-sm font-medium text-white">{user.name}</span>
                        </div>
                        <Badge className="bg-blue-500/20 text-blue-300 text-xs">
                          Level {user.consciousness_level}
                        </Badge>
                      </div>
                      
                      <div className="space-y-2 text-xs">
                        <div className="flex justify-between">
                          <span className="text-gray-400">Consciousness:</span>
                          <span className={getConsciousnessColor(user.consciousness_level)}>
                            {user.consciousness_level.toFixed(1)}%
                          </span>
                        </div>
                        <div className="w-full bg-gray-600 rounded-full h-2">
                          <div 
                            className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-500"
                            style={{ width: `${user.consciousness_level}%` }}
                          />
                        </div>
                        
                        <div className="grid grid-cols-2 gap-2">
                          <div>
                            <span className="text-gray-400">Learning:</span>
                            <span className="text-white ml-1">{user.learning_rate}%</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Emotion:</span>
                            <span className="text-white ml-1 capitalize">{user.emotional_state}</span>
                          </div>
                        </div>
                        
                        <div className="flex justify-between text-gray-400">
                          <span>Predictions: {user.shared_predictions}</span>
                          <span>Insights: {user.shared_insights}</span>
                        </div>
                        
                        <div className="text-gray-500 text-xs">
                          {user.is_online ? 'Online' : `Last seen ${user.last_seen}`}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Predictions Tab */}
            <TabsContent value="predictions" className="space-y-4">
              <div className="space-y-3">
                {sharedPredictions.map((prediction) => (
                  <Card key={prediction.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center text-white text-xs font-bold">
                            {prediction.user_name.charAt(0)}
                          </div>
                          <div>
                            <div className="text-sm font-medium text-white">{prediction.user_name}</div>
                            <div className="text-xs text-gray-400">{prediction.timestamp}</div>
                          </div>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Badge className="bg-green-500/20 text-green-300 text-xs">
                            {prediction.confidence.toFixed(0)}% confidence
                          </Badge>
                          <Button variant="ghost" size="sm" className="text-xs">
                            <Heart className="w-3 h-3 mr-1" />
                            {prediction.likes}
                          </Button>
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-400">Consciousness Level:</span>
                          <span className="text-white font-medium">
                            {prediction.consciousness_level.toFixed(1)}%
                          </span>
                        </div>
                        <div className="w-full bg-gray-600 rounded-full h-2">
                          <div 
                            className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full"
                            style={{ width: `${prediction.consciousness_level}%` }}
                          />
                        </div>
                        
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Learning Rate:</span>
                            <span className="text-white ml-1">{prediction.learning_rate}%</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Emotion:</span>
                            <span className="text-white ml-1 capitalize">{prediction.emotional_state}</span>
                          </div>
                        </div>
                        
                        <div className="flex flex-wrap gap-1 mt-2">
                          {prediction.tags.map((tag, index) => (
                            <Badge key={index} className="bg-gray-600/50 text-gray-300 text-xs">
                              {tag}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Insights Tab */}
            <TabsContent value="insights" className="space-y-4">
              <div className="space-y-3">
                {sharedInsights.map((insight) => (
                  <Card key={insight.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          <div className="w-8 h-8 rounded-full bg-gradient-to-r from-green-500 to-teal-500 flex items-center justify-center text-white text-xs font-bold">
                            {insight.user_name.charAt(0)}
                          </div>
                          <div>
                            <div className="text-sm font-medium text-white">{insight.user_name}</div>
                            <div className="text-xs text-gray-400">{insight.timestamp}</div>
                          </div>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Badge className={getPriorityColor(insight.priority)}>
                            {insight.priority}
                          </Badge>
                          <Button variant="ghost" size="sm" className="text-xs">
                            <ThumbsUp className="w-3 h-3 mr-1" />
                            {insight.likes}
                          </Button>
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <div className="flex items-center space-x-2 mb-2">
                          {getInsightIcon(insight.type)}
                          <span className="text-sm font-medium text-white">{insight.title}</span>
                        </div>
                        
                        <p className="text-xs text-gray-300 mb-2">{insight.description}</p>
                        
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Confidence:</span>
                            <span className="text-white ml-1">{(insight.confidence * 100).toFixed(0)}%</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Impact:</span>
                            <span className="text-white ml-1">{insight.impact_score.toFixed(1)}</span>
                          </div>
                        </div>
                        
                        <div className="flex flex-wrap gap-1 mt-2">
                          {insight.tags.map((tag, index) => (
                            <Badge key={index} className="bg-gray-600/50 text-gray-300 text-xs">
                              {tag}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Activity Tab */}
            <TabsContent value="activity" className="space-y-4">
              <div className="space-y-3">
                <Card className="bg-gray-700/30 border-gray-600">
                  <CardContent className="p-4">
                    <div className="flex items-center space-x-2 mb-2">
                      <Activity className="w-4 h-4 text-blue-400" />
                      <span className="text-sm font-medium text-white">Recent Activity</span>
                    </div>
                    <div className="space-y-2 text-xs text-gray-300">
                      <div>• Alex Chen shared a consciousness prediction (2 min ago)</div>
                      <div>• Sarah Johnson discovered a new learning pattern (5 min ago)</div>
                      <div>• Marcus Rodriguez went offline (1 hour ago)</div>
                      <div>• You shared an insight about memory optimization (2 hours ago)</div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>

      {/* Sharing Modal */}
      {isSharing && (
        <Card className="bg-gray-800/80 border-gray-600">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm text-white">Share Your Consciousness</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <label className="text-xs text-gray-400">Message (optional)</label>
              <Input
                value={shareMessage}
                onChange={(e) => setShareMessage(e.target.value)}
                placeholder="Add a message to your share..."
                className="bg-gray-700/50 border-gray-600 text-white"
              />
            </div>
            
            <div className="flex space-x-2">
              <Button
                onClick={handleSharePrediction}
                className="flex-1 text-xs"
              >
                <Brain className="w-3 h-3 mr-1" />
                Share Prediction
              </Button>
              <Button
                onClick={handleShareInsight}
                variant="outline"
                className="flex-1 text-xs"
              >
                <Zap className="w-3 h-3 mr-1" />
                Share Insight
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default CollaborativeConsciousness;
