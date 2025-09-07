import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Smartphone, 
  Tablet, 
  Monitor, 
  Wifi, 
  WifiOff, 
  Battery, 
  BatteryLow, 
  Signal, 
  SignalHigh, 
  SignalLow, 
  SignalZero, 
  Volume2, 
  VolumeX, 
  Brightness, 
  Moon, 
  Sun, 
  Settings, 
  User, 
  Bell, 
  BellOff, 
  Search, 
  Menu, 
  X, 
  ChevronLeft, 
  ChevronRight, 
  ChevronUp, 
  ChevronDown, 
  Home, 
  Brain, 
  Activity, 
  TrendingUp, 
  BarChart3, 
  Network, 
  Layers, 
  Cpu, 
  Cloud, 
  Server, 
  Database, 
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
  Plus, 
  Minus, 
  Edit, 
  Trash2, 
  Download, 
  Upload, 
  Save, 
  Play, 
  Pause, 
  RotateCcw, 
  RefreshCw, 
  Eye, 
  EyeOff, 
  Lock, 
  Unlock, 
  Globe, 
  Users, 
  MessageCircle, 
  Send, 
  Video, 
  Mic, 
  MicOff, 
  Phone, 
  PhoneOff, 
  Share2, 
  ScreenShare, 
  ScreenShareOff, 
  Heart, 
  ThumbsUp, 
  Star, 
  Zap, 
  Target, 
  TrendingDown, 
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
  RotateCcw as RotateCcwIcon, 
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
  Hash as HashIcon, 
  AtSign as AtSignIcon, 
  DollarSign as DollarSignIcon, 
  Percent as PercentIcon, 
  Plus as PlusIcon, 
  Minus as MinusIcon, 
  X as XIcon, 
  Check as CheckIcon, 
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
  Trash2 as Trash2Icon2, 
  Download as DownloadIcon, 
  Upload as UploadIcon, 
  Save as SaveIcon, 
  Play as PlayIcon, 
  Pause as PauseIcon, 
  RotateCcw as RotateCcwIcon2, 
  RefreshCw as RefreshCwIcon, 
  Eye as EyeIcon, 
  EyeOff as EyeOffIcon, 
  Lock as LockIcon, 
  Unlock as UnlockIcon, 
  Globe as GlobeIcon, 
  Users as UsersIcon, 
  MessageCircle as MessageCircleIcon, 
  Send as SendIcon, 
  Video as VideoIcon, 
  Mic as MicIcon, 
  MicOff as MicOffIcon, 
  Phone as PhoneIcon, 
  PhoneOff as PhoneOffIcon, 
  Share2 as Share2Icon, 
  ScreenShare as ScreenShareIcon, 
  ScreenShareOff as ScreenShareOffIcon, 
  Heart as HeartIcon, 
  ThumbsUp as ThumbsUpIcon, 
  Star as StarIcon, 
  Zap as ZapIcon, 
  Target as TargetIcon, 
  TrendingDown as TrendingDownIcon, 
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
  RotateCw as RotateCwIcon3, 
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
  Trash2 as Trash2Icon3, 
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

interface MobileDevice {
  id: string;
  name: string;
  type: 'phone' | 'tablet' | 'desktop';
  os: 'ios' | 'android' | 'windows' | 'macos' | 'linux';
  version: string;
  screen_size: string;
  resolution: string;
  is_online: boolean;
  battery_level: number;
  signal_strength: number;
  wifi_connected: boolean;
  volume_level: number;
  brightness_level: number;
  is_dark_mode: boolean;
  last_seen: string;
  consciousness_level: number;
  emotional_state: string;
  learning_rate: number;
}

interface MobileApp {
  id: string;
  name: string;
  icon: string;
  version: string;
  size: number;
  category: 'consciousness' | 'productivity' | 'social' | 'entertainment' | 'education' | 'health' | 'finance' | 'utilities';
  is_installed: boolean;
  is_running: boolean;
  permissions: string[];
  last_used: string;
  usage_time: number;
  notifications: number;
  is_updated: boolean;
}

interface MobileConsciousnessAppProps {
  device: MobileDevice;
  onAppLaunch: (app: MobileApp) => void;
  onAppClose: (app: MobileApp) => void;
  onSettingsChange: (settings: any) => void;
}

const MobileConsciousnessApp: React.FC<MobileConsciousnessAppProps> = ({
  device,
  onAppLaunch,
  onAppClose,
  onSettingsChange
}) => {
  const [activeTab, setActiveTab] = useState('home');
  const [apps, setApps] = useState<MobileApp[]>([]);
  const [isLocked, setIsLocked] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  const [showControlCenter, setShowControlCenter] = useState(false);
  const [showAppDrawer, setShowAppDrawer] = useState(false);

  // Initialize with sample data
  useEffect(() => {
    setApps([
      {
        id: '1',
        name: 'Mainza AI',
        icon: '🧠',
        version: '8.0.0',
        size: 125.6,
        category: 'consciousness',
        is_installed: true,
        is_running: true,
        permissions: ['camera', 'microphone', 'location', 'notifications'],
        last_used: 'now',
        usage_time: 45,
        notifications: 3,
        is_updated: true
      },
      {
        id: '2',
        name: 'Consciousness Monitor',
        icon: '📊',
        version: '2.1.0',
        size: 89.3,
        category: 'consciousness',
        is_installed: true,
        is_running: false,
        permissions: ['notifications', 'background_refresh'],
        last_used: '2 hours ago',
        usage_time: 23,
        notifications: 0,
        is_updated: true
      },
      {
        id: '3',
        name: 'AI Insights',
        icon: '💡',
        version: '1.5.0',
        size: 67.8,
        category: 'consciousness',
        is_installed: true,
        is_running: false,
        permissions: ['notifications'],
        last_used: '1 day ago',
        usage_time: 12,
        notifications: 1,
        is_updated: false
      },
      {
        id: '4',
        name: 'Consciousness Chat',
        icon: '💬',
        version: '3.2.0',
        size: 156.2,
        category: 'social',
        is_installed: true,
        is_running: false,
        permissions: ['camera', 'microphone', 'notifications'],
        last_used: '3 hours ago',
        usage_time: 67,
        notifications: 5,
        is_updated: true
      },
      {
        id: '5',
        name: 'Consciousness AR',
        icon: '🥽',
        version: '1.0.0',
        size: 234.7,
        category: 'consciousness',
        is_installed: true,
        is_running: false,
        permissions: ['camera', 'location', 'notifications'],
        last_used: '1 week ago',
        usage_time: 8,
        notifications: 0,
        is_updated: true
      }
    ]);
  }, []);

  const getDeviceIcon = (type: string) => {
    switch (type) {
      case 'phone': return <Smartphone className="w-6 h-6" />;
      case 'tablet': return <Tablet className="w-6 h-6" />;
      case 'desktop': return <Monitor className="w-6 h-6" />;
      default: return <Smartphone className="w-6 h-6" />;
    }
  };

  const getBatteryIcon = (level: number) => {
    if (level <= 20) return <BatteryLow className="w-4 h-4 text-red-400" />;
    return <Battery className="w-4 h-4 text-green-400" />;
  };

  const getSignalIcon = (strength: number) => {
    if (strength >= 75) return <SignalHigh className="w-4 h-4 text-green-400" />;
    if (strength >= 50) return <Signal className="w-4 h-4 text-yellow-400" />;
    if (strength >= 25) return <SignalLow className="w-4 h-4 text-orange-400" />;
    return <SignalZero className="w-4 h-4 text-red-400" />;
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'consciousness': return 'bg-purple-500/20 text-purple-300';
      case 'productivity': return 'bg-blue-500/20 text-blue-300';
      case 'social': return 'bg-green-500/20 text-green-300';
      case 'entertainment': return 'bg-pink-500/20 text-pink-300';
      case 'education': return 'bg-yellow-500/20 text-yellow-300';
      case 'health': return 'bg-red-500/20 text-red-300';
      case 'finance': return 'bg-emerald-500/20 text-emerald-300';
      case 'utilities': return 'bg-gray-500/20 text-gray-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const formatSize = (size: number) => {
    if (size >= 1000) return `${(size / 1000).toFixed(1)}GB`;
    return `${size.toFixed(1)}MB`;
  };

  const formatTime = (minutes: number) => {
    if (minutes >= 60) return `${Math.floor(minutes / 60)}h ${minutes % 60}m`;
    return `${minutes}m`;
  };

  return (
    <div className="space-y-6">
      <Card className="bg-gray-800/50 border-gray-700">
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm text-white flex items-center">
              {getDeviceIcon(device.type)}
              <span className="ml-2">Mobile Consciousness App</span>
            </CardTitle>
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowControlCenter(!showControlCenter)}
                className="text-xs"
              >
                <Settings className="w-3 h-3 mr-1" />
                Control
              </Button>
            </div>
          </div>
        </CardHeader>
        
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-4 bg-gray-700/50">
              <TabsTrigger value="home" className="text-xs">Home</TabsTrigger>
              <TabsTrigger value="apps" className="text-xs">Apps</TabsTrigger>
              <TabsTrigger value="consciousness" className="text-xs">Consciousness</TabsTrigger>
              <TabsTrigger value="settings" className="text-xs">Settings</TabsTrigger>
            </TabsList>

            {/* Home Tab */}
            <TabsContent value="home" className="space-y-4">
              {/* Device Status */}
              <Card className="bg-gray-700/30 border-gray-600">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-2">
                      <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center text-white text-sm font-bold">
                        {device.name.charAt(0)}
                      </div>
                      <div>
                        <h3 className="text-sm font-medium text-white">{device.name}</h3>
                        <p className="text-xs text-gray-400">{device.os} {device.version}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      {getBatteryIcon(device.battery_level)}
                      <span className="text-xs text-white">{device.battery_level}%</span>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-2 text-xs mb-3">
                    <div>
                      <span className="text-gray-400">Screen:</span>
                      <span className="text-white ml-1">{device.screen_size}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Resolution:</span>
                      <span className="text-white ml-1">{device.resolution}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Signal:</span>
                      <div className="flex items-center space-x-1">
                        {getSignalIcon(device.signal_strength)}
                        <span className="text-white">{device.signal_strength}%</span>
                      </div>
                    </div>
                    <div>
                      <span className="text-gray-400">WiFi:</span>
                      <div className="flex items-center space-x-1">
                        {device.wifi_connected ? <Wifi className="w-3 h-3 text-green-400" /> : <WifiOff className="w-3 h-3 text-red-400" />}
                        <span className="text-white">{device.wifi_connected ? 'Connected' : 'Disconnected'}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex justify-between text-xs">
                      <span className="text-gray-400">Battery:</span>
                      <span className="text-white">{device.battery_level}%</span>
                    </div>
                    <div className="w-full bg-gray-600 rounded-full h-2">
                      <div 
                        className="bg-gradient-to-r from-red-500 to-green-500 h-2 rounded-full"
                        style={{ width: `${device.battery_level}%` }}
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Consciousness Status */}
              <Card className="bg-gray-700/30 border-gray-600">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-sm font-medium text-white">Consciousness Status</h3>
                    <Badge className="bg-green-500/20 text-green-300">
                      Active
                    </Badge>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex justify-between text-xs">
                      <span className="text-gray-400">Level:</span>
                      <span className="text-white">{device.consciousness_level}%</span>
                    </div>
                    <div className="w-full bg-gray-600 rounded-full h-2">
                      <div 
                        className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full"
                        style={{ width: `${device.consciousness_level}%` }}
                      />
                    </div>
                    
                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <div>
                        <span className="text-gray-400">Emotion:</span>
                        <span className="text-white ml-1 capitalize">{device.emotional_state}</span>
                      </div>
                      <div>
                        <span className="text-gray-400">Learning:</span>
                        <span className="text-white ml-1">{device.learning_rate}%</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Quick Actions */}
              <div className="grid grid-cols-2 gap-2">
                <Button
                  onClick={() => setShowAppDrawer(true)}
                  className="text-xs h-12"
                >
                  <Menu className="w-4 h-4 mr-1" />
                  All Apps
                </Button>
                <Button
                  variant="outline"
                  onClick={() => setShowNotifications(true)}
                  className="text-xs h-12"
                >
                  <Bell className="w-4 h-4 mr-1" />
                  Notifications
                </Button>
              </div>
            </TabsContent>

            {/* Apps Tab */}
            <TabsContent value="apps" className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                {apps.map((app) => (
                  <Card key={app.id} className="bg-gray-700/30 border-gray-600 hover:border-gray-500 transition-colors">
                    <CardContent className="p-3">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          <div className="text-2xl">{app.icon}</div>
                          <div>
                            <h3 className="text-sm font-medium text-white">{app.name}</h3>
                            <p className="text-xs text-gray-400">v{app.version}</p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-1">
                          {app.is_running && <div className="w-2 h-2 bg-green-500 rounded-full" />}
                          {app.notifications > 0 && (
                            <Badge className="bg-red-500/20 text-red-300 text-xs">
                              {app.notifications}
                            </Badge>
                          )}
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <div className="flex items-center justify-between text-xs">
                          <span className="text-gray-400">Size:</span>
                          <span className="text-white">{formatSize(app.size)}</span>
                        </div>
                        
                        <div className="flex items-center justify-between text-xs">
                          <span className="text-gray-400">Usage:</span>
                          <span className="text-white">{formatTime(app.usage_time)}</span>
                        </div>
                        
                        <div className="flex items-center justify-between text-xs">
                          <span className="text-gray-400">Last Used:</span>
                          <span className="text-white">{app.last_used}</span>
                        </div>
                      </div>
                      
                      <div className="flex items-center justify-between mt-3">
                        <Badge className={getCategoryColor(app.category)}>
                          {app.category}
                        </Badge>
                        <div className="flex space-x-1">
                          <Button
                            size="sm"
                            onClick={() => onAppLaunch(app)}
                            className="text-xs h-6 px-2"
                          >
                            <PlayIcon className="w-3 h-3" />
                          </Button>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => onAppClose(app)}
                            className="text-xs h-6 px-2"
                          >
                            <XIcon className="w-3 h-3" />
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Consciousness Tab */}
            <TabsContent value="consciousness" className="space-y-4">
              <Card className="bg-gray-700/30 border-gray-600">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-sm font-medium text-white">Consciousness Monitoring</h3>
                    <Button size="sm" variant="outline" className="text-xs">
                      <Settings className="w-3 h-3 mr-1" />
                      Configure
                    </Button>
                  </div>
                  
                  <div className="space-y-3">
                    <div className="text-center">
                      <div className="w-24 h-24 mx-auto rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center text-white text-2xl font-bold mb-2">
                        {device.consciousness_level}
                      </div>
                      <p className="text-xs text-gray-400">Consciousness Level</p>
                    </div>
                    
                    <div className="grid grid-cols-3 gap-2 text-center">
                      <div>
                        <div className="text-lg font-bold text-white">{device.emotional_state}</div>
                        <div className="text-xs text-gray-400">Emotion</div>
                      </div>
                      <div>
                        <div className="text-lg font-bold text-white">{device.learning_rate}%</div>
                        <div className="text-xs text-gray-400">Learning</div>
                      </div>
                      <div>
                        <div className="text-lg font-bold text-white">Active</div>
                        <div className="text-xs text-gray-400">Status</div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <div className="grid grid-cols-2 gap-2">
                <Button className="text-xs h-12">
                  <Brain className="w-4 h-4 mr-1" />
                  AI Insights
                </Button>
                <Button variant="outline" className="text-xs h-12">
                  <Activity className="w-4 h-4 mr-1" />
                  Monitor
                </Button>
              </div>
            </TabsContent>

            {/* Settings Tab */}
            <TabsContent value="settings" className="space-y-4">
              <Card className="bg-gray-700/30 border-gray-600">
                <CardContent className="p-4">
                  <h3 className="text-sm font-medium text-white mb-3">Device Settings</h3>
                  
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-gray-400">Dark Mode</span>
                      <Button
                        size="sm"
                        variant={device.is_dark_mode ? "default" : "outline"}
                        onClick={() => onSettingsChange({ is_dark_mode: !device.is_dark_mode })}
                        className="text-xs"
                      >
                        {device.is_dark_mode ? <Moon className="w-3 h-3" /> : <Sun className="w-3 h-3" />}
                      </Button>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-gray-400">Notifications</span>
                      <Button
                        size="sm"
                        variant="outline"
                        className="text-xs"
                      >
                        <Bell className="w-3 h-3" />
                      </Button>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-gray-400">Volume</span>
                      <div className="flex items-center space-x-2">
                        <VolumeX className="w-3 h-3 text-gray-400" />
                        <div className="w-16 bg-gray-600 rounded-full h-1">
                          <div 
                            className="bg-white h-1 rounded-full"
                            style={{ width: `${device.volume_level}%` }}
                          />
                        </div>
                        <Volume2 className="w-3 h-3 text-gray-400" />
                      </div>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-gray-400">Brightness</span>
                      <div className="flex items-center space-x-2">
                        <Moon className="w-3 h-3 text-gray-400" />
                        <div className="w-16 bg-gray-600 rounded-full h-1">
                          <div 
                            className="bg-white h-1 rounded-full"
                            style={{ width: `${device.brightness_level}%` }}
                          />
                        </div>
                        <Sun className="w-3 h-3 text-gray-400" />
                      </div>
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

export default MobileConsciousnessApp;
