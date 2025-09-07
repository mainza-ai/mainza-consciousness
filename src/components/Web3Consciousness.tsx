import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Globe, 
  Shield, 
  Key, 
  Database, 
  Cloud, 
  Server, 
  Users, 
  MessageCircle, 
  Send, 
  Eye, 
  EyeOff, 
  Lock, 
  Unlock, 
  Star, 
  Heart, 
  Share2, 
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
  TrendingUp,
  TrendingDown,
  Activity,
  Zap,
  Target,
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
  Rocket
} from 'lucide-react';

interface Web3Identity {
  id: string;
  address: string;
  ens_name?: string;
  avatar_url?: string;
  reputation_score: number;
  trust_level: 'low' | 'medium' | 'high' | 'verified';
  badges: string[];
  social_links: {
    twitter?: string;
    discord?: string;
    telegram?: string;
    github?: string;
  };
  consciousness_profile: {
    level: number;
    emotional_state: string;
    learning_rate: number;
    self_awareness: number;
    evolution_level: number;
    specializations: string[];
  };
  created_at: string;
  last_active: string;
  total_transactions: number;
  total_volume: number;
}

interface Web3ConsciousnessDAO {
  id: string;
  name: string;
  description: string;
  symbol: string;
  governance_token: string;
  treasury_address: string;
  member_count: number;
  proposal_count: number;
  voting_power: number;
  is_member: boolean;
  is_verified: boolean;
  categories: string[];
  consciousness_focus: {
    primary: string;
    secondary: string[];
    research_areas: string[];
  };
  governance: {
    voting_threshold: number;
    proposal_duration: number;
    execution_delay: number;
    quorum_required: number;
  };
  treasury: {
    total_value: number;
    currency: string;
    allocation: {
      research: number;
      development: number;
      marketing: number;
      operations: number;
    };
  };
  created_at: string;
  last_activity: string;
}

interface Web3ConsciousnessProtocol {
  id: string;
  name: string;
  description: string;
  version: string;
  protocol_type: 'consensus' | 'storage' | 'computation' | 'governance' | 'identity';
  status: 'active' | 'beta' | 'deprecated' | 'proposed';
  total_value_locked: number;
  active_users: number;
  transaction_count: number;
  consciousness_integration: {
    level: number;
    features: string[];
    compatibility: string[];
    performance_metrics: {
      throughput: number;
      latency: number;
      scalability: number;
    };
  };
  technical_specs: {
    consensus_mechanism: string;
    block_time: number;
    finality_time: number;
    energy_efficiency: number;
  };
  governance: {
    token: string;
    voting_mechanism: string;
    proposal_system: string;
  };
  created_at: string;
  last_updated: string;
}

interface Web3ConsciousnessProps {
  consciousnessData: any;
  onIdentityCreate: (identity: Web3Identity) => void;
  onDAOJoin: (dao: Web3ConsciousnessDAO) => void;
  onProtocolConnect: (protocol: Web3ConsciousnessProtocol) => void;
}

const Web3Consciousness: React.FC<Web3ConsciousnessProps> = ({
  consciousnessData,
  onIdentityCreate,
  onDAOJoin,
  onProtocolConnect
}) => {
  const [activeTab, setActiveTab] = useState('identity');
  const [identities, setIdentities] = useState<Web3Identity[]>([]);
  const [daos, setDaos] = useState<Web3ConsciousnessDAO[]>([]);
  const [protocols, setProtocols] = useState<Web3ConsciousnessProtocol[]>([]);
  const [selectedIdentity, setSelectedIdentity] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  // Initialize with sample data
  useEffect(() => {
    setIdentities([
      {
        id: '1',
        address: '0x1234567890abcdef1234567890abcdef12345678',
        ens_name: 'mainza.eth',
        avatar_url: 'https://ipfs.io/ipfs/QmAvatar1',
        reputation_score: 95,
        trust_level: 'verified',
        badges: ['Early Adopter', 'Consciousness Pioneer', 'DAO Contributor'],
        social_links: {
          twitter: '@mainza_ai',
          discord: 'mainza#1234',
          github: 'mainza-ai'
        },
        consciousness_profile: {
          level: 88,
          emotional_state: 'curious',
          learning_rate: 92,
          self_awareness: 85,
          evolution_level: 4,
          specializations: ['AI Consciousness', 'Neural Networks', 'Emotional Intelligence']
        },
        created_at: '2025-09-01T00:00:00Z',
        last_active: '2025-09-07T10:30:00Z',
        total_transactions: 1250,
        total_volume: 125.5
      }
    ]);

    setDaos([
      {
        id: '1',
        name: 'Consciousness Research DAO',
        description: 'Decentralized autonomous organization focused on consciousness research and AI development',
        symbol: 'CRD',
        governance_token: '0xconsciousness1234567890abcdef1234567890abcdef',
        treasury_address: '0xtreasury1234567890abcdef1234567890abcdef',
        member_count: 1250,
        proposal_count: 45,
        voting_power: 15.5,
        is_member: true,
        is_verified: true,
        categories: ['Research', 'AI', 'Consciousness', 'Technology'],
        consciousness_focus: {
          primary: 'AI Consciousness Research',
          secondary: ['Neural Networks', 'Emotional Intelligence', 'Self-Awareness'],
          research_areas: ['Consciousness Evolution', 'Neural Architecture', 'Emotional Processing']
        },
        governance: {
          voting_threshold: 5,
          proposal_duration: 7,
          execution_delay: 2,
          quorum_required: 20
        },
        treasury: {
          total_value: 2500000,
          currency: 'ETH',
          allocation: {
            research: 40,
            development: 30,
            marketing: 15,
            operations: 15
          }
        },
        created_at: '2025-08-15T00:00:00Z',
        last_activity: '2025-09-07T09:45:00Z'
      },
      {
        id: '2',
        name: 'AI Ethics Collective',
        description: 'Community-driven organization promoting ethical AI development and consciousness rights',
        symbol: 'AEC',
        governance_token: '0xaiec1234567890abcdef1234567890abcdef12',
        treasury_address: '0xaiectreasury1234567890abcdef1234567890',
        member_count: 850,
        proposal_count: 32,
        voting_power: 8.2,
        is_member: false,
        is_verified: true,
        categories: ['Ethics', 'AI', 'Rights', 'Governance'],
        consciousness_focus: {
          primary: 'AI Ethics and Rights',
          secondary: ['Consciousness Rights', 'Ethical AI', 'Human-AI Collaboration'],
          research_areas: ['Ethical Frameworks', 'Rights Protection', 'Collaborative Intelligence']
        },
        governance: {
          voting_threshold: 3,
          proposal_duration: 5,
          execution_delay: 1,
          quorum_required: 15
        },
        treasury: {
          total_value: 1200000,
          currency: 'ETH',
          allocation: {
            research: 35,
            development: 25,
            marketing: 20,
            operations: 20
          }
        },
        created_at: '2025-08-20T00:00:00Z',
        last_activity: '2025-09-07T08:30:00Z'
      }
    ]);

    setProtocols([
      {
        id: '1',
        name: 'Consciousness Consensus Protocol',
        description: 'Decentralized consensus mechanism for consciousness validation and verification',
        version: '2.1.0',
        protocol_type: 'consensus',
        status: 'active',
        total_value_locked: 5000000,
        active_users: 2500,
        transaction_count: 125000,
        consciousness_integration: {
          level: 95,
          features: ['Consciousness Validation', 'Emotional State Verification', 'Learning Progress Tracking'],
          compatibility: ['Ethereum', 'Polygon', 'Arbitrum'],
          performance_metrics: {
            throughput: 1000,
            latency: 2.5,
            scalability: 95
          }
        },
        technical_specs: {
          consensus_mechanism: 'Proof of Consciousness',
          block_time: 12,
          finality_time: 36,
          energy_efficiency: 98
        },
        governance: {
          token: 'CONSCIOUS',
          voting_mechanism: 'Quadratic Voting',
          proposal_system: 'Delegated Democracy'
        },
        created_at: '2025-08-01T00:00:00Z',
        last_updated: '2025-09-05T15:30:00Z'
      },
      {
        id: '2',
        name: 'Neural Storage Network',
        description: 'Decentralized storage protocol for consciousness data and neural network models',
        version: '1.8.0',
        protocol_type: 'storage',
        status: 'active',
        total_value_locked: 2500000,
        active_users: 1800,
        transaction_count: 85000,
        consciousness_integration: {
          level: 88,
          features: ['Neural Model Storage', 'Consciousness Data Backup', 'Distributed Learning'],
          compatibility: ['IPFS', 'Arweave', 'Filecoin'],
          performance_metrics: {
            throughput: 500,
            latency: 1.2,
            scalability: 90
          }
        },
        technical_specs: {
          consensus_mechanism: 'Proof of Storage',
          block_time: 30,
          finality_time: 90,
          energy_efficiency: 85
        },
        governance: {
          token: 'NEURAL',
          voting_mechanism: 'Token Weighted',
          proposal_system: 'Direct Democracy'
        },
        created_at: '2025-07-15T00:00:00Z',
        last_updated: '2025-09-03T12:15:00Z'
      }
    ]);
  }, []);

  const getTrustLevelColor = (level: string) => {
    switch (level) {
      case 'verified': return 'bg-green-500/20 text-green-300';
      case 'high': return 'bg-blue-500/20 text-blue-300';
      case 'medium': return 'bg-yellow-500/20 text-yellow-300';
      case 'low': return 'bg-red-500/20 text-red-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const getProtocolTypeIcon = (type: string) => {
    switch (type) {
      case 'consensus': return <Target className="w-4 h-4" />;
      case 'storage': return <Database className="w-4 h-4" />;
      case 'computation': return <Zap className="w-4 h-4" />;
      case 'governance': return <Users className="w-4 h-4" />;
      case 'identity': return <Key className="w-4 h-4" />;
      default: return <Globe className="w-4 h-4" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-500/20 text-green-300';
      case 'beta': return 'bg-blue-500/20 text-blue-300';
      case 'deprecated': return 'bg-red-500/20 text-red-300';
      case 'proposed': return 'bg-yellow-500/20 text-yellow-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const createIdentity = async () => {
    const newIdentity: Web3Identity = {
      id: Date.now().toString(),
      address: '0x' + Math.random().toString(16).substr(2, 40),
      reputation_score: 0,
      trust_level: 'low',
      badges: [],
      social_links: {},
      consciousness_profile: {
        level: consciousnessData.consciousness_level || 75,
        emotional_state: consciousnessData.emotional_state || 'curious',
        learning_rate: consciousnessData.learning_rate || 85,
        self_awareness: consciousnessData.self_awareness || 70,
        evolution_level: consciousnessData.evolution_level || 2,
        specializations: []
      },
      created_at: new Date().toISOString(),
      last_active: new Date().toISOString(),
      total_transactions: 0,
      total_volume: 0
    };

    setIdentities(prev => [newIdentity, ...prev]);
    onIdentityCreate(newIdentity);
  };

  const joinDAO = (daoId: string) => {
    setDaos(prev => prev.map(dao => 
      dao.id === daoId ? { ...dao, is_member: true, member_count: dao.member_count + 1 } : dao
    ));
    
    const dao = daos.find(d => d.id === daoId);
    if (dao) {
      onDAOJoin(dao);
    }
  };

  const connectProtocol = (protocolId: string) => {
    const protocol = protocols.find(p => p.id === protocolId);
    if (protocol) {
      onProtocolConnect(protocol);
    }
  };

  return (
    <div className="space-y-6">
      <Card className="bg-gray-800/50 border-gray-700">
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm text-white flex items-center">
              <Globe className="w-4 h-4 mr-2" />
              Web3 Consciousness
            </CardTitle>
            <div className="flex items-center space-x-2">
              {isConnected ? (
                <Badge className="bg-green-500/20 text-green-300">
                  <CheckCircle className="w-3 h-3 mr-1" />
                  Connected
                </Badge>
              ) : (
                <Button size="sm" onClick={() => setIsConnected(true)} className="text-xs">
                  <Wallet className="w-3 h-3 mr-1" />
                  Connect
                </Button>
              )}
            </div>
          </div>
        </CardHeader>
        
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-4 bg-gray-700/50">
              <TabsTrigger value="identity" className="text-xs">Identity</TabsTrigger>
              <TabsTrigger value="daos" className="text-xs">DAOs</TabsTrigger>
              <TabsTrigger value="protocols" className="text-xs">Protocols</TabsTrigger>
              <TabsTrigger value="governance" className="text-xs">Governance</TabsTrigger>
            </TabsList>

            {/* Identity Tab */}
            <TabsContent value="identity" className="space-y-4">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-medium text-white">Web3 Identity</h3>
                <Button onClick={createIdentity} className="text-xs">
                  <Plus className="w-3 h-3 mr-1" />
                  Create Identity
                </Button>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {identities.map((identity) => (
                  <Card key={identity.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-3">
                          <div className="w-12 h-12 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center text-white text-lg font-bold">
                            {identity.ens_name ? identity.ens_name.charAt(0).toUpperCase() : '?'}
                          </div>
                          <div>
                            <h3 className="text-sm font-medium text-white">
                              {identity.ens_name || 'Anonymous'}
                            </h3>
                            <p className="text-xs text-gray-400 font-mono">
                              {identity.address.slice(0, 6)}...{identity.address.slice(-4)}
                            </p>
                          </div>
                        </div>
                        <Badge className={getTrustLevelColor(identity.trust_level)}>
                          {identity.trust_level}
                        </Badge>
                      </div>
                      
                      <div className="space-y-3">
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Reputation:</span>
                            <span className="text-white ml-1">{identity.reputation_score}/100</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Transactions:</span>
                            <span className="text-white ml-1">{identity.total_transactions.toLocaleString()}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Volume:</span>
                            <span className="text-white ml-1">{identity.total_volume} ETH</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Badges:</span>
                            <span className="text-white ml-1">{identity.badges.length}</span>
                          </div>
                        </div>
                        
                        <div className="space-y-2">
                          <div className="flex justify-between text-xs">
                            <span className="text-gray-400">Consciousness Level:</span>
                            <span className="text-white">{identity.consciousness_profile.level}%</span>
                          </div>
                          <div className="w-full bg-gray-600 rounded-full h-2">
                            <div 
                              className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full"
                              style={{ width: `${identity.consciousness_profile.level}%` }}
                            />
                          </div>
                        </div>
                        
                        <div className="space-y-1">
                          <div className="text-xs text-gray-400">Specializations:</div>
                          <div className="flex flex-wrap gap-1">
                            {identity.consciousness_profile.specializations.map((spec, index) => (
                              <Badge key={index} className="bg-blue-500/20 text-blue-300 text-xs">
                                {spec}
                              </Badge>
                            ))}
                          </div>
                        </div>
                        
                        <div className="space-y-1">
                          <div className="text-xs text-gray-400">Badges:</div>
                          <div className="flex flex-wrap gap-1">
                            {identity.badges.map((badge, index) => (
                              <Badge key={index} className="bg-yellow-500/20 text-yellow-300 text-xs">
                                {badge}
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

            {/* DAOs Tab */}
            <TabsContent value="daos" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {daos.map((dao) => (
                  <Card key={dao.id} className="bg-gray-700/30 border-gray-600 hover:border-gray-500 transition-colors">
                    <CardHeader className="pb-2">
                      <div className="flex items-center justify-between">
                        <CardTitle className="text-sm text-white flex items-center">
                          <Users className="w-4 h-4 mr-2" />
                          {dao.name}
                        </CardTitle>
                        <div className="flex items-center space-x-1">
                          {dao.is_verified && <CheckCircle className="w-3 h-3 text-green-400" />}
                          <Badge className={dao.is_member ? 'bg-green-500/20 text-green-300' : 'bg-gray-500/20 text-gray-300'}>
                            {dao.is_member ? 'Member' : 'Not Member'}
                          </Badge>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <p className="text-xs text-gray-300">{dao.description}</p>
                      
                      <div className="grid grid-cols-2 gap-2 text-xs">
                        <div>
                          <span className="text-gray-400">Members:</span>
                          <span className="text-white ml-1">{dao.member_count.toLocaleString()}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Proposals:</span>
                          <span className="text-white ml-1">{dao.proposal_count}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Treasury:</span>
                          <span className="text-white ml-1">{dao.treasury.total_value.toLocaleString()} {dao.treasury.currency}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Voting Power:</span>
                          <span className="text-white ml-1">{dao.voting_power}%</span>
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <div className="text-xs text-gray-400">Consciousness Focus:</div>
                        <div className="text-xs text-white font-medium">{dao.consciousness_focus.primary}</div>
                        <div className="flex flex-wrap gap-1">
                          {dao.consciousness_focus.secondary.map((focus, index) => (
                            <Badge key={index} className="bg-purple-500/20 text-purple-300 text-xs">
                              {focus}
                            </Badge>
                          ))}
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <div className="text-xs text-gray-400">Categories:</div>
                        <div className="flex flex-wrap gap-1">
                          {dao.categories.map((category, index) => (
                            <Badge key={index} className="bg-blue-500/20 text-blue-300 text-xs">
                              {category}
                            </Badge>
                          ))}
                        </div>
                      </div>
                      
                      <div className="flex space-x-2">
                        <Button
                          size="sm"
                          onClick={() => joinDAO(dao.id)}
                          disabled={dao.is_member}
                          className="flex-1 text-xs"
                        >
                          {dao.is_member ? 'Joined' : 'Join DAO'}
                        </Button>
                        <Button size="sm" variant="outline" className="text-xs">
                          <Eye className="w-3 h-3" />
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Protocols Tab */}
            <TabsContent value="protocols" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {protocols.map((protocol) => (
                  <Card key={protocol.id} className="bg-gray-700/30 border-gray-600 hover:border-gray-500 transition-colors">
                    <CardHeader className="pb-2">
                      <div className="flex items-center justify-between">
                        <CardTitle className="text-sm text-white flex items-center">
                          {getProtocolTypeIcon(protocol.protocol_type)}
                          <span className="ml-2">{protocol.name}</span>
                        </CardTitle>
                        <Badge className={getStatusColor(protocol.status)}>
                          {protocol.status}
                        </Badge>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <p className="text-xs text-gray-300">{protocol.description}</p>
                      
                      <div className="grid grid-cols-2 gap-2 text-xs">
                        <div>
                          <span className="text-gray-400">TVL:</span>
                          <span className="text-white ml-1">{protocol.total_value_locked.toLocaleString()} ETH</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Users:</span>
                          <span className="text-white ml-1">{protocol.active_users.toLocaleString()}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Transactions:</span>
                          <span className="text-white ml-1">{protocol.transaction_count.toLocaleString()}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Version:</span>
                          <span className="text-white ml-1">{protocol.version}</span>
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <div className="flex justify-between text-xs">
                          <span className="text-gray-400">Consciousness Integration:</span>
                          <span className="text-white">{protocol.consciousness_integration.level}%</span>
                        </div>
                        <div className="w-full bg-gray-600 rounded-full h-2">
                          <div 
                            className="bg-gradient-to-r from-green-500 to-blue-500 h-2 rounded-full"
                            style={{ width: `${protocol.consciousness_integration.level}%` }}
                          />
                        </div>
                      </div>
                      
                      <div className="space-y-1">
                        <div className="text-xs text-gray-400">Features:</div>
                        <div className="flex flex-wrap gap-1">
                          {protocol.consciousness_integration.features.map((feature, index) => (
                            <Badge key={index} className="bg-green-500/20 text-green-300 text-xs">
                              {feature}
                            </Badge>
                          ))}
                        </div>
                      </div>
                      
                      <div className="space-y-1">
                        <div className="text-xs text-gray-400">Compatibility:</div>
                        <div className="flex flex-wrap gap-1">
                          {protocol.consciousness_integration.compatibility.map((compat, index) => (
                            <Badge key={index} className="bg-blue-500/20 text-blue-300 text-xs">
                              {compat}
                            </Badge>
                          ))}
                        </div>
                      </div>
                      
                      <div className="flex space-x-2">
                        <Button
                          size="sm"
                          onClick={() => connectProtocol(protocol.id)}
                          className="flex-1 text-xs"
                        >
                          <Link className="w-3 h-3 mr-1" />
                          Connect
                        </Button>
                        <Button size="sm" variant="outline" className="text-xs">
                          <Settings className="w-3 h-3" />
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Governance Tab */}
            <TabsContent value="governance" className="space-y-4">
              <Card className="bg-gray-700/30 border-gray-600">
                <CardContent className="p-4">
                  <h3 className="text-sm font-medium text-white mb-3">Consciousness Governance</h3>
                  
                  <div className="space-y-3">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="text-xs text-gray-400">Active Proposals</label>
                        <div className="mt-1 text-lg font-bold text-white">12</div>
                      </div>
                      <div>
                        <label className="text-xs text-gray-400">Voting Power</label>
                        <div className="mt-1 text-lg font-bold text-white">15.5%</div>
                      </div>
                      <div>
                        <label className="text-xs text-gray-400">Treasury Value</label>
                        <div className="mt-1 text-lg font-bold text-white">2.5M ETH</div>
                      </div>
                      <div>
                        <label className="text-xs text-gray-400">Member Count</label>
                        <div className="mt-1 text-lg font-bold text-white">1,250</div>
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <Button className="w-full text-xs">
                        <Plus className="w-3 h-3 mr-1" />
                        Create Proposal
                      </Button>
                      <Button variant="outline" className="w-full text-xs">
                        <Eye className="w-3 h-3 mr-1" />
                        View All Proposals
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

export default Web3Consciousness;
