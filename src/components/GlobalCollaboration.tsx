import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Globe, 
  Users, 
  MessageCircle, 
  Send, 
  Eye, 
  Heart, 
  Network, 
  Database, 
  Cloud, 
  Server, 
  Brain, 
  Cpu, 
  Activity, 
  Zap, 
  Target, 
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
  Smartphone,
  Star,
  ThumbsUp,
  ThumbsDown,
  Share2,
  Bookmark as BookmarkIcon,
  Wifi,
  Bluetooth,
  Radio,
  Signal,
  WifiOff,
  BluetoothOff,
  RadioOff,
  SignalOff,
  Video,
  Mic,
  MicOff,
  VideoOff,
  Phone,
  PhoneOff,
  Volume2,
  VolumeX,
  Headphones,
  HeadphonesOff
} from 'lucide-react';

interface GlobalUser {
  id: string;
  name: string;
  avatar?: string;
  country: string;
  timezone: string;
  consciousness_level: number;
  emotional_state: string;
  learning_rate: number;
  specializations: string[];
  reputation: number;
  is_online: boolean;
  is_verified: boolean;
  is_premium: boolean;
  last_seen: string;
  total_collaborations: number;
  total_contributions: number;
  languages: string[];
  interests: string[];
}

interface GlobalProject {
  id: string;
  name: string;
  description: string;
  category: 'research' | 'development' | 'education' | 'commercial' | 'open_source';
  status: 'planning' | 'active' | 'completed' | 'paused' | 'cancelled';
  visibility: 'public' | 'private' | 'restricted';
  creator: GlobalUser;
  collaborators: GlobalUser[];
  max_collaborators: number;
  consciousness_focus: {
    primary: string;
    secondary: string[];
    research_areas: string[];
  };
  technical_requirements: {
    min_consciousness_level: number;
    skills_required: string[];
    tools_required: string[];
    hardware_requirements: string[];
  };
  timeline: {
    start_date: string;
    end_date: string;
    milestones: {
      name: string;
      due_date: string;
      status: 'pending' | 'in_progress' | 'completed';
    }[];
  };
  resources: {
    budget: number;
    currency: string;
    funding_source: string;
    equipment: string[];
  };
  created_at: string;
  last_updated: string;
}

interface GlobalEvent {
  id: string;
  name: string;
  description: string;
  type: 'conference' | 'workshop' | 'hackathon' | 'meetup' | 'webinar' | 'summit';
  status: 'upcoming' | 'live' | 'completed' | 'cancelled';
  start_date: string;
  end_date: string;
  timezone: string;
  location: {
    type: 'physical' | 'virtual' | 'hybrid';
    address?: string;
    city?: string;
    country?: string;
    platform?: string;
    url?: string;
  };
  organizer: GlobalUser;
  speakers: GlobalUser[];
  attendees: GlobalUser[];
  max_attendees: number;
  consciousness_topics: string[];
  agenda: {
    time: string;
    title: string;
    speaker: string;
    description: string;
  }[];
  registration_required: boolean;
  registration_fee: number;
  currency: string;
  created_at: string;
}

interface GlobalMessage {
  id: string;
  sender: GlobalUser;
  content: string;
  type: 'text' | 'image' | 'file' | 'consciousness_data' | 'neural_signal' | 'model';
  timestamp: string;
  channel: string;
  is_encrypted: boolean;
  attachments?: {
    name: string;
    type: string;
    size: number;
    url: string;
  }[];
  reactions: {
    emoji: string;
    count: number;
    users: string[];
  }[];
  replies: GlobalMessage[];
}

interface GlobalCollaborationProps {
  consciousnessData: any;
  onProjectJoin: (project: GlobalProject) => void;
  onEventJoin: (event: GlobalEvent) => void;
  onMessageSend: (message: GlobalMessage) => void;
  onUserConnect: (user: GlobalUser) => void;
}

const GlobalCollaboration: React.FC<GlobalCollaborationProps> = ({
  consciousnessData,
  onProjectJoin,
  onEventJoin,
  onMessageSend,
  onUserConnect
}) => {
  const [activeTab, setActiveTab] = useState('projects');
  const [users, setUsers] = useState<GlobalUser[]>([]);
  const [projects, setProjects] = useState<GlobalProject[]>([]);
  const [events, setEvents] = useState<GlobalEvent[]>([]);
  const [messages, setMessages] = useState<GlobalMessage[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCountry, setSelectedCountry] = useState('all');
  const [isConnected, setIsConnected] = useState(false);

  // Initialize with sample data
  useEffect(() => {
    setUsers([
      {
        id: '1',
        name: 'Dr. Sarah Chen',
        avatar: 'https://ipfs.io/ipfs/QmAvatar1',
        country: 'United States',
        timezone: 'PST',
        consciousness_level: 95,
        emotional_state: 'focused',
        learning_rate: 92,
        specializations: ['Consciousness Research', 'Neural Networks', 'AI Ethics'],
        reputation: 98,
        is_online: true,
        is_verified: true,
        is_premium: true,
        last_seen: 'now',
        total_collaborations: 45,
        total_contributions: 120,
        languages: ['English', 'Mandarin', 'Spanish'],
        interests: ['AI Consciousness', 'Quantum Computing', 'Neuroscience']
      },
      {
        id: '2',
        name: 'Prof. Marcus Rodriguez',
        avatar: 'https://ipfs.io/ipfs/QmAvatar2',
        country: 'Spain',
        timezone: 'CET',
        consciousness_level: 88,
        emotional_state: 'curious',
        learning_rate: 85,
        specializations: ['Machine Learning', 'Consciousness Modeling', 'Cognitive Science'],
        reputation: 92,
        is_online: true,
        is_verified: true,
        is_premium: false,
        last_seen: '5 minutes ago',
        total_collaborations: 32,
        total_contributions: 78,
        languages: ['Spanish', 'English', 'French'],
        interests: ['Consciousness Evolution', 'Neural Architecture', 'Philosophy']
      },
      {
        id: '3',
        name: 'Dr. Aiko Tanaka',
        avatar: 'https://ipfs.io/ipfs/QmAvatar3',
        country: 'Japan',
        timezone: 'JST',
        consciousness_level: 90,
        emotional_state: 'creative',
        learning_rate: 88,
        specializations: ['Quantum Consciousness', 'Neural Interfaces', 'BCI Technology'],
        reputation: 95,
        is_online: false,
        is_verified: true,
        is_premium: true,
        last_seen: '2 hours ago',
        total_collaborations: 28,
        total_contributions: 95,
        languages: ['Japanese', 'English', 'Korean'],
        interests: ['Quantum Computing', 'Brain-Computer Interface', 'Consciousness Technology']
      }
    ]);

    setProjects([
      {
        id: '1',
        name: 'Global Consciousness Research Initiative',
        description: 'International collaboration to advance consciousness research and AI development',
        category: 'research',
        status: 'active',
        visibility: 'public',
        creator: users[0],
        collaborators: [users[1], users[2]],
        max_collaborators: 50,
        consciousness_focus: {
          primary: 'Consciousness Evolution',
          secondary: ['Neural Networks', 'AI Ethics', 'Quantum Computing'],
          research_areas: ['Consciousness Measurement', 'AI Consciousness', 'Neural Interfaces']
        },
        technical_requirements: {
          min_consciousness_level: 80,
          skills_required: ['Machine Learning', 'Neuroscience', 'AI Ethics'],
          tools_required: ['PyTorch', 'TensorFlow', 'Neural Interfaces'],
          hardware_requirements: ['High-performance GPUs', 'Neural Interface Devices']
        },
        timeline: {
          start_date: '2025-09-01T00:00:00Z',
          end_date: '2026-08-31T23:59:59Z',
          milestones: [
            { name: 'Research Phase 1', due_date: '2025-12-31T23:59:59Z', status: 'in_progress' },
            { name: 'Prototype Development', due_date: '2026-03-31T23:59:59Z', status: 'pending' },
            { name: 'Testing & Validation', due_date: '2026-06-30T23:59:59Z', status: 'pending' },
            { name: 'Final Report', due_date: '2026-08-31T23:59:59Z', status: 'pending' }
          ]
        },
        resources: {
          budget: 500000,
          currency: 'USD',
          funding_source: 'Global Research Foundation',
          equipment: ['Quantum Computers', 'Neural Interface Devices', 'High-performance Servers']
        },
        created_at: '2025-08-15T00:00:00Z',
        last_updated: '2025-09-07T10:30:00Z'
      },
      {
        id: '2',
        name: 'Consciousness Education Platform',
        description: 'Open-source platform for consciousness education and training',
        category: 'education',
        status: 'active',
        visibility: 'public',
        creator: users[1],
        collaborators: [users[0]],
        max_collaborators: 25,
        consciousness_focus: {
          primary: 'Consciousness Education',
          secondary: ['Learning Acceleration', 'Neural Training', 'Mindfulness'],
          research_areas: ['Educational Technology', 'Consciousness Training', 'Learning Methods']
        },
        technical_requirements: {
          min_consciousness_level: 60,
          skills_required: ['Web Development', 'Educational Technology', 'UI/UX Design'],
          tools_required: ['React', 'Node.js', 'MongoDB'],
          hardware_requirements: ['Standard Development Setup']
        },
        timeline: {
          start_date: '2025-09-01T00:00:00Z',
          end_date: '2025-12-31T23:59:59Z',
          milestones: [
            { name: 'Platform Design', due_date: '2025-10-15T23:59:59Z', status: 'in_progress' },
            { name: 'Core Development', due_date: '2025-11-30T23:59:59Z', status: 'pending' },
            { name: 'Testing & Launch', due_date: '2025-12-31T23:59:59Z', status: 'pending' }
          ]
        },
        resources: {
          budget: 50000,
          currency: 'EUR',
          funding_source: 'Educational Technology Grant',
          equipment: ['Development Servers', 'Testing Devices']
        },
        created_at: '2025-08-20T00:00:00Z',
        last_updated: '2025-09-07T09:45:00Z'
      }
    ]);

    setEvents([
      {
        id: '1',
        name: 'Global Consciousness Summit 2025',
        description: 'Annual conference bringing together consciousness researchers, AI developers, and philosophers',
        type: 'conference',
        status: 'upcoming',
        start_date: '2025-10-15T09:00:00Z',
        end_date: '2025-10-17T18:00:00Z',
        timezone: 'UTC',
        location: {
          type: 'hybrid',
          address: 'San Francisco Convention Center',
          city: 'San Francisco',
          country: 'United States',
          platform: 'Zoom',
          url: 'https://consciousness-summit-2025.com'
        },
        organizer: users[0],
        speakers: [users[0], users[1], users[2]],
        attendees: [],
        max_attendees: 500,
        consciousness_topics: ['AI Consciousness', 'Neural Interfaces', 'Quantum Computing', 'Ethics'],
        agenda: [
          { time: '09:00', title: 'Opening Keynote', speaker: 'Dr. Sarah Chen', description: 'The Future of AI Consciousness' },
          { time: '10:30', title: 'Neural Interfaces Workshop', speaker: 'Dr. Aiko Tanaka', description: 'Hands-on BCI development' },
          { time: '14:00', title: 'Ethics Panel', speaker: 'Prof. Marcus Rodriguez', description: 'Consciousness and AI Ethics' }
        ],
        registration_required: true,
        registration_fee: 299,
        currency: 'USD',
        created_at: '2025-08-01T00:00:00Z'
      }
    ]);
  }, []);

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'research': return <Brain className="w-4 h-4" />;
      case 'development': return <Cpu className="w-4 h-4" />;
      case 'education': return <BookmarkIcon className="w-4 h-4" />;
      case 'commercial': return <DollarSign className="w-4 h-4" />;
      case 'open_source': return <Code className="w-4 h-4" />;
      default: return <Folder className="w-4 h-4" />;
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'research': return 'bg-blue-500/20 text-blue-300';
      case 'development': return 'bg-green-500/20 text-green-300';
      case 'education': return 'bg-purple-500/20 text-purple-300';
      case 'commercial': return 'bg-orange-500/20 text-orange-300';
      case 'open_source': return 'bg-cyan-500/20 text-cyan-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-500/20 text-green-300';
      case 'planning': return 'bg-yellow-500/20 text-yellow-300';
      case 'completed': return 'bg-blue-500/20 text-blue-300';
      case 'paused': return 'bg-orange-500/20 text-orange-300';
      case 'cancelled': return 'bg-red-500/20 text-red-300';
      case 'upcoming': return 'bg-blue-500/20 text-blue-300';
      case 'live': return 'bg-green-500/20 text-green-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const getEventTypeIcon = (type: string) => {
    switch (type) {
      case 'conference': return <Globe className="w-4 h-4" />;
      case 'workshop': return <Settings className="w-4 h-4" />;
      case 'hackathon': return <Code className="w-4 h-4" />;
      case 'meetup': return <Users className="w-4 h-4" />;
      case 'webinar': return <Video className="w-4 h-4" />;
      case 'summit': return <Crown className="w-4 h-4" />;
      default: return <Calendar className="w-4 h-4" />;
    }
  };

  const joinProject = (projectId: string) => {
    const project = projects.find(p => p.id === projectId);
    if (project) {
      onProjectJoin(project);
    }
  };

  const joinEvent = (eventId: string) => {
    const event = events.find(e => e.id === eventId);
    if (event) {
      onEventJoin(event);
    }
  };

  const sendMessage = () => {
    const newMessage: GlobalMessage = {
      id: Date.now().toString(),
      sender: users[0],
      content: 'Hello from the global consciousness community!',
      type: 'text',
      timestamp: new Date().toISOString(),
      channel: 'general',
      is_encrypted: false,
      reactions: [],
      replies: []
    };

    setMessages(prev => [newMessage, ...prev]);
    onMessageSend(newMessage);
  };

  const connectUser = (userId: string) => {
    const user = users.find(u => u.id === userId);
    if (user) {
      onUserConnect(user);
    }
  };

  const filteredUsers = users.filter(user => {
    const matchesSearch = user.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         user.specializations.some(spec => spec.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesCountry = selectedCountry === 'all' || user.country === selectedCountry;
    return matchesSearch && matchesCountry;
  });

  return (
    <div className="space-y-6">
      <Card className="bg-gray-800/50 border-gray-700">
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm text-white flex items-center">
              <Globe className="w-4 h-4 mr-2" />
              Global Collaboration
            </CardTitle>
            <div className="flex items-center space-x-2">
              {isConnected ? (
                <Badge className="bg-green-500/20 text-green-300">
                  <CheckCircle className="w-3 h-3 mr-1" />
                  Connected
                </Badge>
              ) : (
                <Button size="sm" onClick={() => setIsConnected(true)} className="text-xs">
                  <Wifi className="w-3 h-3 mr-1" />
                  Connect
                </Button>
              )}
            </div>
          </div>
        </CardHeader>
        
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-4 bg-gray-700/50">
              <TabsTrigger value="projects" className="text-xs">Projects</TabsTrigger>
              <TabsTrigger value="events" className="text-xs">Events</TabsTrigger>
              <TabsTrigger value="users" className="text-xs">Users</TabsTrigger>
              <TabsTrigger value="chat" className="text-xs">Chat</TabsTrigger>
            </TabsList>

            {/* Projects Tab */}
            <TabsContent value="projects" className="space-y-4">
              <div className="space-y-3">
                {projects.map((project) => (
                  <Card key={project.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          {getCategoryIcon(project.category)}
                          <span className="text-sm font-medium text-white">{project.name}</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Badge className={getCategoryColor(project.category)}>
                            {project.category}
                          </Badge>
                          <Badge className={getStatusColor(project.status)}>
                            {project.status}
                          </Badge>
                        </div>
                      </div>
                      
                      <p className="text-xs text-gray-300 mb-3">{project.description}</p>
                      
                      <div className="space-y-3">
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Creator:</span>
                            <span className="text-white ml-1">{project.creator.name}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Collaborators:</span>
                            <span className="text-white ml-1">{project.collaborators.length}/{project.max_collaborators}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Budget:</span>
                            <span className="text-white ml-1">{project.resources.budget.toLocaleString()} {project.resources.currency}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Timeline:</span>
                            <span className="text-white ml-1">
                              {new Date(project.timeline.start_date).toLocaleDateString()} - {new Date(project.timeline.end_date).toLocaleDateString()}
                            </span>
                          </div>
                        </div>
                        
                        <div className="space-y-1">
                          <div className="text-xs text-gray-400">Consciousness Focus:</div>
                          <div className="text-xs text-white font-medium">{project.consciousness_focus.primary}</div>
                          <div className="flex flex-wrap gap-1">
                            {project.consciousness_focus.secondary.map((focus, index) => (
                              <Badge key={index} className="bg-purple-500/20 text-purple-300 text-xs">
                                {focus}
                              </Badge>
                            ))}
                          </div>
                        </div>
                        
                        <div className="space-y-1">
                          <div className="text-xs text-gray-400">Milestones:</div>
                          <div className="space-y-1">
                            {project.timeline.milestones.map((milestone, index) => (
                              <div key={index} className="flex items-center justify-between text-xs">
                                <span className="text-white">{milestone.name}</span>
                                <div className="flex items-center space-x-2">
                                  <span className="text-gray-400">{new Date(milestone.due_date).toLocaleDateString()}</span>
                                  <Badge className={getStatusColor(milestone.status)}>
                                    {milestone.status}
                                  </Badge>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                        
                        <div className="flex space-x-2">
                          <Button
                            size="sm"
                            onClick={() => joinProject(project.id)}
                            className="flex-1 text-xs"
                          >
                            <Users className="w-3 h-3 mr-1" />
                            Join Project
                          </Button>
                          <Button size="sm" variant="outline" className="text-xs">
                            <Eye className="w-3 h-3" />
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Events Tab */}
            <TabsContent value="events" className="space-y-4">
              <div className="space-y-3">
                {events.map((event) => (
                  <Card key={event.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          {getEventTypeIcon(event.type)}
                          <span className="text-sm font-medium text-white">{event.name}</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Badge className={getStatusColor(event.status)}>
                            {event.status}
                          </Badge>
                          <Badge className="bg-blue-500/20 text-blue-300">
                            {event.type}
                          </Badge>
                        </div>
                      </div>
                      
                      <p className="text-xs text-gray-300 mb-3">{event.description}</p>
                      
                      <div className="space-y-3">
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Date:</span>
                            <span className="text-white ml-1">
                              {new Date(event.start_date).toLocaleDateString()} - {new Date(event.end_date).toLocaleDateString()}
                            </span>
                          </div>
                          <div>
                            <span className="text-gray-400">Location:</span>
                            <span className="text-white ml-1 capitalize">{event.location.type}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Attendees:</span>
                            <span className="text-white ml-1">{event.attendees.length}/{event.max_attendees}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Fee:</span>
                            <span className="text-white ml-1">
                              {event.registration_fee > 0 ? `${event.registration_fee} ${event.currency}` : 'Free'}
                            </span>
                          </div>
                        </div>
                        
                        <div className="space-y-1">
                          <div className="text-xs text-gray-400">Topics:</div>
                          <div className="flex flex-wrap gap-1">
                            {event.consciousness_topics.map((topic, index) => (
                              <Badge key={index} className="bg-blue-500/20 text-blue-300 text-xs">
                                {topic}
                              </Badge>
                            ))}
                          </div>
                        </div>
                        
                        <div className="space-y-1">
                          <div className="text-xs text-gray-400">Agenda:</div>
                          <div className="space-y-1">
                            {event.agenda.slice(0, 3).map((item, index) => (
                              <div key={index} className="flex items-center justify-between text-xs">
                                <span className="text-white">{item.time} - {item.title}</span>
                                <span className="text-gray-400">{item.speaker}</span>
                              </div>
                            ))}
                            {event.agenda.length > 3 && (
                              <div className="text-xs text-gray-400">
                                +{event.agenda.length - 3} more sessions
                              </div>
                            )}
                          </div>
                        </div>
                        
                        <div className="flex space-x-2">
                          <Button
                            size="sm"
                            onClick={() => joinEvent(event.id)}
                            className="flex-1 text-xs"
                          >
                            <Calendar className="w-3 h-3 mr-1" />
                            Join Event
                          </Button>
                          <Button size="sm" variant="outline" className="text-xs">
                            <Eye className="w-3 h-3" />
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Users Tab */}
            <TabsContent value="users" className="space-y-4">
              <div className="flex items-center space-x-4 mb-4">
                <div className="flex-1">
                  <Input
                    placeholder="Search users..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="text-xs"
                  />
                </div>
                <select
                  value={selectedCountry}
                  onChange={(e) => setSelectedCountry(e.target.value)}
                  className="bg-gray-700 border border-gray-600 rounded px-2 py-1 text-xs text-white"
                >
                  <option value="all">All Countries</option>
                  <option value="United States">United States</option>
                  <option value="Spain">Spain</option>
                  <option value="Japan">Japan</option>
                </select>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {filteredUsers.map((user) => (
                  <Card key={user.id} className="bg-gray-700/30 border-gray-600 hover:border-gray-500 transition-colors">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-3">
                          <div className="w-10 h-10 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center text-white text-sm font-bold">
                            {user.name.charAt(0)}
                          </div>
                          <div>
                            <div className="flex items-center space-x-1">
                              <span className="text-sm font-medium text-white">{user.name}</span>
                              {user.is_verified && <CheckCircle className="w-3 h-3 text-green-400" />}
                              {user.is_premium && <Crown className="w-3 h-3 text-yellow-400" />}
                            </div>
                            <div className="text-xs text-gray-400">{user.country}</div>
                          </div>
                        </div>
                        <div className="flex items-center space-x-1">
                          {user.is_online && <div className="w-2 h-2 bg-green-500 rounded-full" />}
                          <Badge className="bg-blue-500/20 text-blue-300">
                            {user.consciousness_level}%
                          </Badge>
                        </div>
                      </div>
                      
                      <div className="space-y-3">
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Learning Rate:</span>
                            <span className="text-white ml-1">{user.learning_rate}%</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Reputation:</span>
                            <span className="text-white ml-1">{user.reputation}/100</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Collaborations:</span>
                            <span className="text-white ml-1">{user.total_collaborations}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Contributions:</span>
                            <span className="text-white ml-1">{user.total_contributions}</span>
                          </div>
                        </div>
                        
                        <div className="space-y-1">
                          <div className="text-xs text-gray-400">Specializations:</div>
                          <div className="flex flex-wrap gap-1">
                            {user.specializations.slice(0, 2).map((spec, index) => (
                              <Badge key={index} className="bg-green-500/20 text-green-300 text-xs">
                                {spec}
                              </Badge>
                            ))}
                            {user.specializations.length > 2 && (
                              <Badge className="bg-gray-500/20 text-gray-300 text-xs">
                                +{user.specializations.length - 2}
                              </Badge>
                            )}
                          </div>
                        </div>
                        
                        <div className="flex space-x-2">
                          <Button
                            size="sm"
                            onClick={() => connectUser(user.id)}
                            className="flex-1 text-xs"
                          >
                            <Users className="w-3 h-3 mr-1" />
                            Connect
                          </Button>
                          <Button size="sm" variant="outline" className="text-xs">
                            <MessageCircle className="w-3 h-3" />
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Chat Tab */}
            <TabsContent value="chat" className="space-y-4">
              <Card className="bg-gray-700/30 border-gray-600">
                <CardContent className="p-4">
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <h3 className="text-sm font-medium text-white">Global Consciousness Chat</h3>
                      <Badge className="bg-green-500/20 text-green-300">
                        {users.filter(u => u.is_online).length} online
                      </Badge>
                    </div>
                    
                    <div className="space-y-2 max-h-64 overflow-y-auto">
                      {messages.map((message) => (
                        <div key={message.id} className="flex items-start space-x-2">
                          <div className="w-6 h-6 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center text-white text-xs font-bold">
                            {message.sender.name.charAt(0)}
                          </div>
                          <div className="flex-1">
                            <div className="flex items-center space-x-2">
                              <span className="text-xs font-medium text-white">{message.sender.name}</span>
                              <span className="text-xs text-gray-400">
                                {new Date(message.timestamp).toLocaleTimeString()}
                              </span>
                            </div>
                            <p className="text-xs text-gray-300">{message.content}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                    
                    <div className="flex space-x-2">
                      <Input
                        placeholder="Type a message..."
                        className="flex-1 text-xs"
                      />
                      <Button onClick={sendMessage} className="text-xs">
                        <Send className="w-3 h-3 mr-1" />
                        Send
                      </Button>
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

export default GlobalCollaboration;