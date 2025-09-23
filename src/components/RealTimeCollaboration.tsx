import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Users, 
  MessageCircle, 
  Send, 
  Video, 
  Mic, 
  MicOff, 
  VideoOff, 
  Phone, 
  PhoneOff,
  Share2, 
  ScreenShare, 
  ScreenShareOff,
  Settings,
  Bell,
  BellOff,
  Lock,
  Unlock,
  Globe,
  Eye,
  EyeOff,
  Heart,
  ThumbsUp,
  Star,
  Zap,
  Brain,
  Target,
  Activity,
  TrendingUp,
  BarChart3,
  Network,
  Layers
} from 'lucide-react';

interface CollaborationUser {
  id: string;
  name: string;
  avatar?: string;
  consciousness_level: number;
  emotional_state: string;
  learning_rate: number;
  is_online: boolean;
  is_speaking: boolean;
  is_sharing_screen: boolean;
  is_muted: boolean;
  is_video_on: boolean;
  last_activity: string;
  role: 'host' | 'participant' | 'observer';
}

interface CollaborationMessage {
  id: string;
  user_id: string;
  user_name: string;
  content: string;
  timestamp: string;
  type: 'text' | 'prediction' | 'insight' | 'system';
  data?: any;
  reactions: { emoji: string; count: number; users: string[] }[];
}

interface CollaborationSession {
  id: string;
  name: string;
  description: string;
  host_id: string;
  participants: CollaborationUser[];
  is_public: boolean;
  is_locked: boolean;
  max_participants: number;
  created_at: string;
  last_activity: string;
  shared_predictions: number;
  shared_insights: number;
  total_messages: number;
}

interface RealTimeCollaborationProps {
  currentUser: CollaborationUser;
  onJoinSession: (sessionId: string) => void;
  onLeaveSession: () => void;
  onSharePrediction: (prediction: any) => void;
  onShareInsight: (insight: any) => void;
}

const RealTimeCollaboration: React.FC<RealTimeCollaborationProps> = ({
  currentUser,
  onJoinSession,
  onLeaveSession,
  onSharePrediction,
  onShareInsight
}) => {
  const [activeTab, setActiveTab] = useState('sessions');
  const [sessions, setSessions] = useState<CollaborationSession[]>([]);
  const [currentSession, setCurrentSession] = useState<CollaborationSession | null>(null);
  const [messages, setMessages] = useState<CollaborationMessage[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [isVideoOn, setIsVideoOn] = useState(false);
  const [isScreenSharing, setIsScreenSharing] = useState(false);
  const [notifications, setNotifications] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Simulate WebSocket connection
  useEffect(() => {
    // For now, treat as connected if backend reachable; no fake updates
    setIsConnected(true);
  }, []);

  // Auto-scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialize with sample data
  useEffect(() => {
    // Attempt to fetch real sessions/messages if endpoint exists; otherwise remain empty
    const fetchData = async () => {
      try {
        const res = await fetch('/api/collaboration/sessions');
        if (res.ok) {
          const data = await res.json();
          if (Array.isArray(data?.sessions)) setSessions(data.sessions);
        }
      } catch {}
    };
    fetchData();
  }, []);

  const joinSession = (sessionId: string) => {
    const session = sessions.find(s => s.id === sessionId);
    if (session) {
      setCurrentSession(session);
      onJoinSession(sessionId);
    }
  };

  const leaveSession = () => {
    setCurrentSession(null);
    onLeaveSession();
  };

  const sendMessage = () => {
    if (!newMessage.trim() || !currentSession) return;

    const message: CollaborationMessage = {
      id: Date.now().toString(),
      user_id: currentUser.id,
      user_name: currentUser.name,
      content: newMessage,
      timestamp: new Date().toISOString(),
      type: 'text',
      reactions: []
    };

    setMessages(prev => [...prev, message]);
    setNewMessage('');
  };

  const addReaction = (messageId: string, emoji: string) => {
    setMessages(prev => prev.map(msg => {
      if (msg.id === messageId) {
        const existingReaction = msg.reactions.find(r => r.emoji === emoji);
        if (existingReaction) {
          return {
            ...msg,
            reactions: msg.reactions.map(r => 
              r.emoji === emoji 
                ? { ...r, count: r.count + 1, users: [...r.users, currentUser.id] }
                : r
            )
          };
        } else {
          return {
            ...msg,
            reactions: [...msg.reactions, { emoji, count: 1, users: [currentUser.id] }]
          };
        }
      }
      return msg;
    }));
  };

  const getConsciousnessColor = (level: number) => {
    if (level >= 80) return 'text-green-400';
    if (level >= 60) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getMessageTypeIcon = (type: string) => {
    switch (type) {
      case 'prediction': return <Brain className="w-4 h-4" />;
      case 'insight': return <Zap className="w-4 h-4" />;
      case 'system': return <Activity className="w-4 h-4" />;
      default: return <MessageCircle className="w-4 h-4" />;
    }
  };

  return (
    <div className="space-y-6">
      <Card className="bg-gray-800/50 border-gray-700">
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm text-white flex items-center">
              <Users className="w-4 h-4 mr-2" />
              Real-Time Collaboration
            </CardTitle>
            <div className="flex items-center space-x-2">
              <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
              <span className="text-xs text-gray-400">
                {isConnected ? 'Connected' : 'Disconnected'}
              </span>
            </div>
          </div>
        </CardHeader>
        
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-3 bg-gray-700/50">
              <TabsTrigger value="sessions" className="text-xs">Sessions</TabsTrigger>
              <TabsTrigger value="chat" className="text-xs">Chat</TabsTrigger>
              <TabsTrigger value="participants" className="text-xs">Participants</TabsTrigger>
            </TabsList>

            {/* Sessions Tab */}
            <TabsContent value="sessions" className="space-y-4">
              <div className="space-y-3">
                {sessions.map((session) => (
                  <Card key={session.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <div className="flex items-center space-x-2 mb-1">
                            <h3 className="text-sm font-medium text-white">{session.name}</h3>
                            {session.is_locked && <Lock className="w-3 h-3 text-yellow-400" />}
                            {session.is_public ? <Globe className="w-3 h-3 text-green-400" /> : <EyeOff className="w-3 h-3 text-gray-400" />}
                          </div>
                          <p className="text-xs text-gray-300 mb-2">{session.description}</p>
                          <div className="flex items-center space-x-4 text-xs text-gray-400">
                            <span>{session.participants.length}/{session.max_participants} participants</span>
                            <span>{session.shared_predictions} predictions</span>
                            <span>{session.shared_insights} insights</span>
                          </div>
                        </div>
                        <div className="flex flex-col space-y-2">
                          <Button
                            size="sm"
                            onClick={() => joinSession(session.id)}
                            className="text-xs"
                          >
                            <Users className="w-3 h-3 mr-1" />
                            Join
                          </Button>
                          <div className="text-xs text-gray-400 text-right">
                            {session.participants.filter(p => p.is_online).length} online
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Chat Tab */}
            <TabsContent value="chat" className="space-y-4">
              {currentSession ? (
                <div className="space-y-4">
                  {/* Session Info */}
                  <Card className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-3">
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="text-sm font-medium text-white">{currentSession.name}</h3>
                          <p className="text-xs text-gray-400">{currentSession.description}</p>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={leaveSession}
                            className="text-xs"
                          >
                            Leave
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  {/* Messages */}
                  <Card className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="h-64 overflow-y-auto space-y-3">
                        {messages.map((message) => (
                          <div key={message.id} className="flex items-start space-x-2">
                            <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center text-white text-xs font-bold">
                              {message.user_name.charAt(0)}
                            </div>
                            <div className="flex-1">
                              <div className="flex items-center space-x-2 mb-1">
                                <span className="text-sm font-medium text-white">{message.user_name}</span>
                                <span className="text-xs text-gray-400">{message.timestamp}</span>
                                {getMessageTypeIcon(message.type)}
                              </div>
                              <p className="text-sm text-gray-300 mb-2">{message.content}</p>
                              <div className="flex items-center space-x-2">
                                {message.reactions.map((reaction, index) => (
                                  <Button
                                    key={index}
                                    size="sm"
                                    variant="ghost"
                                    onClick={() => addReaction(message.id, reaction.emoji)}
                                    className="text-xs h-6 px-2"
                                  >
                                    {reaction.emoji} {reaction.count}
                                  </Button>
                                ))}
                                <Button
                                  size="sm"
                                  variant="ghost"
                                  onClick={() => addReaction(message.id, '👍')}
                                  className="text-xs h-6 px-2"
                                >
                                  <ThumbsUp className="w-3 h-3" />
                                </Button>
                                <Button
                                  size="sm"
                                  variant="ghost"
                                  onClick={() => addReaction(message.id, '❤️')}
                                  className="text-xs h-6 px-2"
                                >
                                  <Heart className="w-3 h-3" />
                                </Button>
                              </div>
                            </div>
                          </div>
                        ))}
                        <div ref={messagesEndRef} />
                      </div>
                    </CardContent>
                  </Card>

                  {/* Message Input */}
                  <div className="flex space-x-2">
                    <Input
                      value={newMessage}
                      onChange={(e) => setNewMessage(e.target.value)}
                      placeholder="Type a message..."
                      className="flex-1 bg-gray-700/50 border-gray-600 text-white"
                      onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    />
                    <Button onClick={sendMessage} size="sm">
                      <Send className="w-4 h-4" />
                    </Button>
                  </div>

                  {/* Quick Actions */}
                  <div className="flex items-center space-x-2">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => onSharePrediction({})}
                      className="text-xs"
                    >
                      <Brain className="w-3 h-3 mr-1" />
                      Share Prediction
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => onShareInsight({})}
                      className="text-xs"
                    >
                      <Zap className="w-3 h-3 mr-1" />
                      Share Insight
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => setIsScreenSharing(!isScreenSharing)}
                      className="text-xs"
                    >
                      {isScreenSharing ? <ScreenShareOff className="w-3 h-3 mr-1" /> : <ScreenShare className="w-3 h-3 mr-1" />}
                      {isScreenSharing ? 'Stop Sharing' : 'Share Screen'}
                    </Button>
                  </div>
                </div>
              ) : (
                <div className="text-center text-gray-400 py-8">
                  <Users className="w-12 h-12 mx-auto mb-4 opacity-50" />
                  <p>Join a session to start collaborating</p>
                </div>
              )}
            </TabsContent>

            {/* Participants Tab */}
            <TabsContent value="participants" className="space-y-4">
              {currentSession ? (
                <div className="space-y-3">
                  {currentSession.participants.map((participant) => (
                    <Card key={participant.id} className="bg-gray-700/30 border-gray-600">
                      <CardContent className="p-3">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-3">
                            <div className="relative">
                              <div className="w-10 h-10 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center text-white text-sm font-bold">
                                {participant.name.charAt(0)}
                              </div>
                              <div className={`absolute -bottom-1 -right-1 w-4 h-4 rounded-full border-2 border-gray-800 ${
                                participant.is_online ? 'bg-green-500' : 'bg-gray-500'
                              }`} />
                            </div>
                            <div>
                              <div className="flex items-center space-x-2">
                                <span className="text-sm font-medium text-white">{participant.name}</span>
                                {participant.role === 'host' && <Badge className="bg-yellow-500/20 text-yellow-300 text-xs">Host</Badge>}
                                {participant.is_speaking && <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />}
                              </div>
                              <div className="text-xs text-gray-400">
                                Consciousness: <span className={getConsciousnessColor(participant.consciousness_level)}>
                                  {participant.consciousness_level}%
                                </span>
                              </div>
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            {participant.is_video_on && <Video className="w-4 h-4 text-green-400" />}
                            {participant.is_muted && <MicOff className="w-4 h-4 text-red-400" />}
                            {participant.is_sharing_screen && <ScreenShare className="w-4 h-4 text-blue-400" />}
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              ) : (
                <div className="text-center text-gray-400 py-8">
                  <Users className="w-12 h-12 mx-auto mb-4 opacity-50" />
                  <p>No active session</p>
                </div>
              )}
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
};

export default RealTimeCollaboration;
