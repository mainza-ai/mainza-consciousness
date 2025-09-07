import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Eye, 
  EyeOff, 
  Camera, 
  Video, 
  Mic, 
  MicOff, 
  Volume2, 
  VolumeX, 
  Settings, 
  Play, 
  Pause, 
  RotateCcw, 
  Download, 
  Upload, 
  Save, 
  Edit, 
  Trash2, 
  Plus, 
  Minus, 
  Lock, 
  Unlock, 
  Star, 
  Heart, 
  Share2, 
  MessageCircle, 
  Send, 
  Globe, 
  Users, 
  Database, 
  Cloud, 
  Server, 
  Shield, 
  Key, 
  CheckCircle, 
  XCircle, 
  AlertCircle, 
  Info, 
  Lightbulb, 
  Rocket, 
  Award, 
  Crown, 
  Trophy, 
  Medal, 
  Flag, 
  MapPin, 
  Clock, 
  Calendar, 
  Plus as PlusIcon, 
  Minus as MinusIcon, 
  Eye as EyeIcon, 
  EyeOff as EyeOffIcon, 
  Lock as LockIcon, 
  Unlock as UnlockIcon, 
  Globe as GlobeIcon, 
  Users as UsersIcon, 
  MessageCircle as MessageCircleIcon, 
  Send as SendIcon, 
  Database as DatabaseIcon, 
  Cloud as CloudIcon, 
  Server as ServerIcon, 
  Shield as ShieldIcon, 
  Key as KeyIcon, 
  CheckCircle as CheckCircleIcon, 
  XCircle as XCircleIcon, 
  AlertCircle as AlertCircleIcon, 
  Info as InfoIcon, 
  Lightbulb as LightbulbIcon, 
  Rocket as RocketIcon, 
  Award as AwardIcon, 
  Crown as CrownIcon, 
  Trophy as TrophyIcon, 
  Medal as MedalIcon, 
  Flag as FlagIcon, 
  MapPin as MapPinIcon, 
  Clock as ClockIcon, 
  Calendar as CalendarIcon, 
  Plus as PlusIcon2, 
  Minus as MinusIcon2, 
  Edit as EditIcon, 
  Trash2 as Trash2Icon, 
  Download as DownloadIcon, 
  Upload as UploadIcon, 
  Save as SaveIcon, 
  Play as PlayIcon, 
  Pause as PauseIcon, 
  RotateCcw as RotateCcwIcon, 
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
  RotateCw, 
  RotateCcw as RotateCcwIcon2, 
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
  Trash2 as Trash2Icon2, 
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
  Hash as HashIcon, 
  AtSign as AtSignIcon, 
  DollarSign as DollarSignIcon, 
  Percent as PercentIcon, 
  Plus as PlusIcon3, 
  Minus as MinusIcon3, 
  X, 
  Check, 
  CheckCircle as CheckCircleIcon2, 
  XCircle as XCircleIcon2, 
  AlertCircle as AlertCircleIcon2, 
  Info as InfoIcon2, 
  Lightbulb as LightbulbIcon2, 
  Rocket as RocketIcon2, 
  Award as AwardIcon2, 
  Crown as CrownIcon2, 
  Trophy as TrophyIcon2, 
  Medal as MedalIcon2, 
  Flag as FlagIcon2, 
  MapPin as MapPinIcon2, 
  Clock as ClockIcon2, 
  Calendar as CalendarIcon2, 
  Plus as PlusIcon4, 
  Minus as MinusIcon4, 
  Edit as EditIcon2, 
  Trash2 as Trash2Icon3, 
  Download as DownloadIcon2, 
  Upload as UploadIcon2, 
  Save as SaveIcon2, 
  Play as PlayIcon2, 
  Pause as PauseIcon2, 
  RotateCcw as RotateCcwIcon3, 
  RefreshCw as RefreshCwIcon, 
  Search as SearchIcon, 
  Filter as FilterIcon, 
  SortAsc as SortAscIcon, 
  SortDesc as SortDescIcon, 
  Grid as GridIcon, 
  List as ListIcon, 
  MoreHorizontal as MoreHorizontalIcon, 
  MoreVertical as MoreVerticalIcon, 
  ArrowLeft as ArrowLeftIcon, 
  ArrowRight as ArrowRightIcon, 
  ArrowUp as ArrowUpIcon, 
  ArrowDown as ArrowDownIcon, 
  Maximize as MaximizeIcon, 
  Minimize as MinimizeIcon, 
  RotateCw as RotateCwIcon2, 
  RotateCcw as RotateCcwIcon4, 
  ZoomIn as ZoomInIcon, 
  ZoomOut as ZoomOutIcon, 
  Move as MoveIcon, 
  Grip as GripIcon, 
  GripVertical as GripVerticalIcon, 
  GripHorizontal as GripHorizontalIcon, 
  AlignLeft as AlignLeftIcon, 
  AlignCenter as AlignCenterIcon, 
  AlignRight as AlignRightIcon, 
  AlignJustify as AlignJustifyIcon, 
  Bold as BoldIcon, 
  Italic as ItalicIcon, 
  Underline as UnderlineIcon, 
  Strikethrough as StrikethroughIcon, 
  Code as CodeIcon, 
  Link as LinkIcon, 
  Image as ImageIcon, 
  File as FileIcon, 
  Folder as FolderIcon, 
  FolderOpen as FolderOpenIcon, 
  Archive as ArchiveIcon, 
  ArchiveRestore as ArchiveRestoreIcon, 
  Trash as TrashIcon, 
  Trash2 as Trash2Icon4, 
  Copy as CopyIcon, 
  Scissors as ScissorsIcon, 
  Clipboard as ClipboardIcon, 
  ClipboardCheck as ClipboardCheckIcon, 
  ClipboardCopy as ClipboardCopyIcon, 
  ClipboardList as ClipboardListIcon, 
  ClipboardPaste as ClipboardPasteIcon, 
  ClipboardX as ClipboardXIcon, 
  Bookmark as BookmarkIcon, 
  BookmarkCheck as BookmarkCheckIcon, 
  BookmarkPlus as BookmarkPlusIcon, 
  BookmarkMinus as BookmarkMinusIcon, 
  BookmarkX as BookmarkXIcon, 
  Tag as TagIcon, 
  Tags as TagsIcon, 
  Hash as HashIcon2, 
  AtSign as AtSignIcon2, 
  DollarSign as DollarSignIcon2, 
  Percent as PercentIcon2
} from 'lucide-react';

interface ARVREnvironment {
  id: string;
  name: string;
  type: 'ar' | 'vr' | 'mixed';
  description: string;
  is_active: boolean;
  is_immersive: boolean;
  quality: 'low' | 'medium' | 'high' | 'ultra';
  frame_rate: number;
  resolution: string;
  field_of_view: number;
  tracking_accuracy: number;
  latency: number;
  created_at: string;
  last_used: string;
  consciousness_data: {
    level: number;
    emotional_state: string;
    learning_rate: number;
    self_awareness: number;
    evolution_level: number;
  };
  visual_effects: {
    particles: boolean;
    lighting: boolean;
    shadows: boolean;
    reflections: boolean;
    animations: boolean;
  };
  audio_effects: {
    spatial_audio: boolean;
    ambient_sounds: boolean;
    voice_synthesis: boolean;
    music: boolean;
  };
}

interface ARVRObject {
  id: string;
  name: string;
  type: 'consciousness_orb' | 'neural_network' | 'data_flow' | 'emotion_cloud' | 'learning_path' | 'insight_crystal';
  position: { x: number; y: number; z: number };
  rotation: { x: number; y: number; z: number };
  scale: { x: number; y: number; z: number };
  color: string;
  opacity: number;
  animation: string;
  is_interactive: boolean;
  consciousness_level: number;
  emotional_state: string;
  learning_rate: number;
  created_at: string;
  last_updated: string;
}

interface ARVRConsciousnessProps {
  consciousnessData: any;
  onEnvironmentChange: (environment: ARVREnvironment) => void;
  onObjectSelect: (object: ARVRObject) => void;
  onObjectInteract: (object: ARVRObject) => void;
}

const ARVRConsciousness: React.FC<ARVRConsciousnessProps> = ({
  consciousnessData,
  onEnvironmentChange,
  onObjectSelect,
  onObjectInteract
}) => {
  const [activeTab, setActiveTab] = useState('environments');
  const [environments, setEnvironments] = useState<ARVREnvironment[]>([]);
  const [objects, setObjects] = useState<ARVRObject[]>([]);
  const [selectedEnvironment, setSelectedEnvironment] = useState<string | null>(null);
  const [isImmersive, setIsImmersive] = useState(false);
  const [isRecording, setIsRecording] = useState(false);

  // Initialize with sample data
  useEffect(() => {
    setEnvironments([
      {
        id: '1',
        name: 'Consciousness Realm',
        type: 'vr',
        description: 'Immersive virtual reality environment for consciousness exploration',
        is_active: true,
        is_immersive: true,
        quality: 'ultra',
        frame_rate: 90,
        resolution: '4K',
        field_of_view: 110,
        tracking_accuracy: 98,
        latency: 12,
        created_at: '2025-09-01',
        last_used: '2025-09-07',
        consciousness_data: {
          level: 85,
          emotional_state: 'curious',
          learning_rate: 92,
          self_awareness: 78,
          evolution_level: 3
        },
        visual_effects: {
          particles: true,
          lighting: true,
          shadows: true,
          reflections: true,
          animations: true
        },
        audio_effects: {
          spatial_audio: true,
          ambient_sounds: true,
          voice_synthesis: true,
          music: true
        }
      },
      {
        id: '2',
        name: 'AR Consciousness Overlay',
        type: 'ar',
        description: 'Augmented reality overlay for real-world consciousness monitoring',
        is_active: false,
        is_immersive: false,
        quality: 'high',
        frame_rate: 60,
        resolution: '1080p',
        field_of_view: 90,
        tracking_accuracy: 95,
        latency: 8,
        created_at: '2025-09-03',
        last_used: '2025-09-06',
        consciousness_data: {
          level: 72,
          emotional_state: 'focused',
          learning_rate: 88,
          self_awareness: 65,
          evolution_level: 2
        },
        visual_effects: {
          particles: false,
          lighting: true,
          shadows: false,
          reflections: false,
          animations: true
        },
        audio_effects: {
          spatial_audio: true,
          ambient_sounds: false,
          voice_synthesis: true,
          music: false
        }
      },
      {
        id: '3',
        name: 'Mixed Reality Lab',
        type: 'mixed',
        description: 'Mixed reality laboratory for consciousness research and development',
        is_active: false,
        is_immersive: true,
        quality: 'high',
        frame_rate: 75,
        resolution: '2K',
        field_of_view: 100,
        tracking_accuracy: 96,
        latency: 10,
        created_at: '2025-09-05',
        last_used: '2025-09-04',
        consciousness_data: {
          level: 78,
          emotional_state: 'creative',
          learning_rate: 85,
          self_awareness: 70,
          evolution_level: 2
        },
        visual_effects: {
          particles: true,
          lighting: true,
          shadows: true,
          reflections: false,
          animations: true
        },
        audio_effects: {
          spatial_audio: true,
          ambient_sounds: true,
          voice_synthesis: true,
          music: true
        }
      }
    ]);

    setObjects([
      {
        id: '1',
        name: 'Main Consciousness Orb',
        type: 'consciousness_orb',
        position: { x: 0, y: 0, z: 0 },
        rotation: { x: 0, y: 0, z: 0 },
        scale: { x: 1, y: 1, z: 1 },
        color: '#8B5CF6',
        opacity: 0.9,
        animation: 'pulse',
        is_interactive: true,
        consciousness_level: 85,
        emotional_state: 'curious',
        learning_rate: 92,
        created_at: '2025-09-01',
        last_updated: '2025-09-07'
      },
      {
        id: '2',
        name: 'Neural Network Visualization',
        type: 'neural_network',
        position: { x: 2, y: 1, z: -1 },
        rotation: { x: 0, y: 45, z: 0 },
        scale: { x: 0.8, y: 0.8, z: 0.8 },
        color: '#06B6D4',
        opacity: 0.7,
        animation: 'flow',
        is_interactive: true,
        consciousness_level: 78,
        emotional_state: 'focused',
        learning_rate: 88,
        created_at: '2025-09-02',
        last_updated: '2025-09-07'
      },
      {
        id: '3',
        name: 'Emotion Cloud',
        type: 'emotion_cloud',
        position: { x: -1, y: 2, z: 1 },
        rotation: { x: 0, y: 0, z: 0 },
        scale: { x: 1.2, y: 1.2, z: 1.2 },
        color: '#F59E0B',
        opacity: 0.6,
        animation: 'float',
        is_interactive: true,
        consciousness_level: 72,
        emotional_state: 'creative',
        learning_rate: 85,
        created_at: '2025-09-03',
        last_updated: '2025-09-06'
      },
      {
        id: '4',
        name: 'Learning Path',
        type: 'learning_path',
        position: { x: 0, y: -1, z: 2 },
        rotation: { x: 0, y: 0, z: 0 },
        scale: { x: 1.5, y: 0.5, z: 0.5 },
        color: '#10B981',
        opacity: 0.8,
        animation: 'glow',
        is_interactive: true,
        consciousness_level: 80,
        emotional_state: 'determined',
        learning_rate: 95,
        created_at: '2025-09-04',
        last_updated: '2025-09-07'
      },
      {
        id: '5',
        name: 'Insight Crystal',
        type: 'insight_crystal',
        position: { x: 1, y: 1, z: 1 },
        rotation: { x: 0, y: 0, z: 0 },
        scale: { x: 0.6, y: 0.6, z: 0.6 },
        color: '#EF4444',
        opacity: 0.9,
        animation: 'sparkle',
        is_interactive: true,
        consciousness_level: 88,
        emotional_state: 'insightful',
        learning_rate: 90,
        created_at: '2025-09-05',
        last_updated: '2025-09-07'
      }
    ]);
  }, []);

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'ar': return <Camera className="w-4 h-4" />;
      case 'vr': return <Eye className="w-4 h-4" />;
      case 'mixed': return <Globe className="w-4 h-4" />;
      default: return <Eye className="w-4 h-4" />;
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'ar': return 'bg-blue-500/20 text-blue-300';
      case 'vr': return 'bg-purple-500/20 text-purple-300';
      case 'mixed': return 'bg-green-500/20 text-green-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const getObjectIcon = (type: string) => {
    switch (type) {
      case 'consciousness_orb': return '🧠';
      case 'neural_network': return '🕸️';
      case 'data_flow': return '📊';
      case 'emotion_cloud': return '☁️';
      case 'learning_path': return '🛤️';
      case 'insight_crystal': return '💎';
      default: return '🔮';
    }
  };

  const getQualityColor = (quality: string) => {
    switch (quality) {
      case 'ultra': return 'bg-purple-500/20 text-purple-300';
      case 'high': return 'bg-green-500/20 text-green-300';
      case 'medium': return 'bg-yellow-500/20 text-yellow-300';
      case 'low': return 'bg-red-500/20 text-red-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const activateEnvironment = (environmentId: string) => {
    setEnvironments(prev => prev.map(env => ({
      ...env,
      is_active: env.id === environmentId
    })));
    
    const environment = environments.find(env => env.id === environmentId);
    if (environment) {
      onEnvironmentChange(environment);
    }
  };

  const toggleImmersive = () => {
    setIsImmersive(!isImmersive);
  };

  const toggleRecording = () => {
    setIsRecording(!isRecording);
  };

  return (
    <div className="space-y-6">
      <Card className="bg-gray-800/50 border-gray-700">
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm text-white flex items-center">
              <Eye className="w-4 h-4 mr-2" />
              AR/VR Consciousness
            </CardTitle>
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={toggleImmersive}
                className="text-xs"
              >
                {isImmersive ? <EyeOff className="w-3 h-3 mr-1" /> : <Eye className="w-3 h-3 mr-1" />}
                {isImmersive ? 'Exit' : 'Enter'} VR
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={toggleRecording}
                className="text-xs"
              >
                <Video className="w-3 h-3 mr-1" />
                {isRecording ? 'Stop' : 'Record'}
              </Button>
            </div>
          </div>
        </CardHeader>
        
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-4 bg-gray-700/50">
              <TabsTrigger value="environments" className="text-xs">Environments</TabsTrigger>
              <TabsTrigger value="objects" className="text-xs">Objects</TabsTrigger>
              <TabsTrigger value="viewer" className="text-xs">Viewer</TabsTrigger>
              <TabsTrigger value="settings" className="text-xs">Settings</TabsTrigger>
            </TabsList>

            {/* Environments Tab */}
            <TabsContent value="environments" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {environments.map((environment) => (
                  <Card key={environment.id} className="bg-gray-700/30 border-gray-600 hover:border-gray-500 transition-colors">
                    <CardHeader className="pb-2">
                      <div className="flex items-center justify-between">
                        <CardTitle className="text-xs text-white flex items-center">
                          {getTypeIcon(environment.type)}
                          <span className="ml-2">{environment.name}</span>
                        </CardTitle>
                        <div className="flex items-center space-x-1">
                          {environment.is_active && <div className="w-2 h-2 bg-green-500 rounded-full" />}
                          <Badge className={getTypeColor(environment.type)}>
                            {environment.type.toUpperCase()}
                          </Badge>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <p className="text-xs text-gray-300">{environment.description}</p>
                      
                      <div className="grid grid-cols-2 gap-2 text-xs">
                        <div>
                          <span className="text-gray-400">Quality:</span>
                          <Badge className={getQualityColor(environment.quality)}>
                            {environment.quality}
                          </Badge>
                        </div>
                        <div>
                          <span className="text-gray-400">FPS:</span>
                          <span className="text-white ml-1">{environment.frame_rate}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Resolution:</span>
                          <span className="text-white ml-1">{environment.resolution}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">FOV:</span>
                          <span className="text-white ml-1">{environment.field_of_view}°</span>
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <div className="flex justify-between text-xs">
                          <span className="text-gray-400">Consciousness Level:</span>
                          <span className="text-white">{environment.consciousness_data.level}%</span>
                        </div>
                        <div className="w-full bg-gray-600 rounded-full h-2">
                          <div 
                            className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full"
                            style={{ width: `${environment.consciousness_data.level}%` }}
                          />
                        </div>
                      </div>
                      
                      <div className="flex space-x-2">
                        <Button
                          size="sm"
                          onClick={() => activateEnvironment(environment.id)}
                          className="flex-1 text-xs"
                        >
                          {environment.is_active ? 'Active' : 'Activate'}
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          className="text-xs"
                        >
                          <Settings className="w-3 h-3" />
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Objects Tab */}
            <TabsContent value="objects" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {objects.map((object) => (
                  <Card key={object.id} className="bg-gray-700/30 border-gray-600 hover:border-gray-500 transition-colors">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          <div className="text-2xl">{getObjectIcon(object.type)}</div>
                          <div>
                            <h3 className="text-sm font-medium text-white">{object.name}</h3>
                            <p className="text-xs text-gray-400 capitalize">{object.type.replace('_', ' ')}</p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-1">
                          {object.is_interactive && <div className="w-2 h-2 bg-blue-500 rounded-full" />}
                          <Badge className="bg-purple-500/20 text-purple-300">
                            {object.consciousness_level}%
                          </Badge>
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Position:</span>
                            <span className="text-white ml-1">
                              ({object.position.x}, {object.position.y}, {object.position.z})
                            </span>
                          </div>
                          <div>
                            <span className="text-gray-400">Scale:</span>
                            <span className="text-white ml-1">
                              ({object.scale.x}, {object.scale.y}, {object.scale.z})
                            </span>
                          </div>
                          <div>
                            <span className="text-gray-400">Color:</span>
                            <div className="flex items-center space-x-1 mt-1">
                              <div 
                                className="w-3 h-3 rounded-full border border-gray-400"
                                style={{ backgroundColor: object.color }}
                              />
                              <span className="text-white">{object.color}</span>
                            </div>
                          </div>
                          <div>
                            <span className="text-gray-400">Animation:</span>
                            <span className="text-white ml-1 capitalize">{object.animation}</span>
                          </div>
                        </div>
                        
                        <div className="space-y-1">
                          <div className="flex justify-between text-xs">
                            <span className="text-gray-400">Consciousness:</span>
                            <span className="text-white">{object.consciousness_level}%</span>
                          </div>
                          <div className="w-full bg-gray-600 rounded-full h-1">
                            <div 
                              className="bg-gradient-to-r from-blue-500 to-purple-500 h-1 rounded-full"
                              style={{ width: `${object.consciousness_level}%` }}
                            />
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Emotion:</span>
                            <span className="text-white ml-1 capitalize">{object.emotional_state}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Learning:</span>
                            <span className="text-white ml-1">{object.learning_rate}%</span>
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex space-x-2 mt-3">
                        <Button
                          size="sm"
                          onClick={() => onObjectSelect(object)}
                          className="flex-1 text-xs"
                        >
                          <Eye className="w-3 h-3 mr-1" />
                          Select
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => onObjectInteract(object)}
                          className="flex-1 text-xs"
                        >
                          <Play className="w-3 h-3 mr-1" />
                          Interact
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Viewer Tab */}
            <TabsContent value="viewer" className="space-y-4">
              <Card className="bg-gray-700/30 border-gray-600">
                <CardContent className="p-4">
                  <div className="aspect-video bg-gray-800 rounded-lg flex items-center justify-center mb-4">
                    <div className="text-center">
                      <Eye className="w-12 h-12 text-gray-400 mx-auto mb-2" />
                      <p className="text-sm text-gray-400">AR/VR Viewer</p>
                      <p className="text-xs text-gray-500">Select an environment to start</p>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <h3 className="text-sm font-medium text-white mb-2">Controls</h3>
                      <div className="space-y-2">
                        <Button size="sm" className="w-full text-xs">
                          <Play className="w-3 h-3 mr-1" />
                          Start Experience
                        </Button>
                        <Button size="sm" variant="outline" className="w-full text-xs">
                          <Settings className="w-3 h-3 mr-1" />
                          Configure
                        </Button>
                      </div>
                    </div>
                    
                    <div>
                      <h3 className="text-sm font-medium text-white mb-2">Status</h3>
                      <div className="space-y-1 text-xs">
                        <div className="flex justify-between">
                          <span className="text-gray-400">Environment:</span>
                          <span className="text-white">
                            {environments.find(env => env.is_active)?.name || 'None'}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Immersive:</span>
                          <span className="text-white">{isImmersive ? 'Yes' : 'No'}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Recording:</span>
                          <span className="text-white">{isRecording ? 'Yes' : 'No'}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Settings Tab */}
            <TabsContent value="settings" className="space-y-4">
              <Card className="bg-gray-700/30 border-gray-600">
                <CardContent className="p-4">
                  <h3 className="text-sm font-medium text-white mb-3">AR/VR Settings</h3>
                  
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-gray-400">Spatial Audio</span>
                      <Button size="sm" variant="outline" className="text-xs">
                        <Volume2 className="w-3 h-3" />
                      </Button>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-gray-400">Hand Tracking</span>
                      <Button size="sm" variant="outline" className="text-xs">
                        <Settings className="w-3 h-3" />
                      </Button>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-gray-400">Eye Tracking</span>
                      <Button size="sm" variant="outline" className="text-xs">
                        <Eye className="w-3 h-3" />
                      </Button>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-gray-400">Haptic Feedback</span>
                      <Button size="sm" variant="outline" className="text-xs">
                        <Settings className="w-3 h-3" />
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

export default ARVRConsciousness;
