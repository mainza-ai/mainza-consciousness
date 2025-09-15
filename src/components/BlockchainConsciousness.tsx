import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Link, 
  Shield, 
  Key, 
  Database, 
  Cloud, 
  Server, 
  Globe, 
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
  Link as LinkIcon, 
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
  Hash as HashIcon, 
  AtSign as AtSignIcon, 
  DollarSign as DollarSignIcon, 
  Percent as PercentIcon, 
  Plus as PlusIcon, 
  Minus as MinusIcon, 
  X, 
  Check, 
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
  RotateCcw as RotateCcwIcon3, 
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
  Link as LinkIcon2, 
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

interface BlockchainNetwork {
  id: string;
  name: string;
  type: 'ethereum' | 'polygon' | 'arbitrum' | 'optimism' | 'base' | 'solana' | 'cardano' | 'polkadot';
  chain_id: number;
  rpc_url: string;
  explorer_url: string;
  is_connected: boolean;
  gas_price: number;
  block_height: number;
  last_block_time: string;
  native_currency: {
    name: string;
    symbol: string;
    decimals: number;
  };
  consciousness_contract: {
    address: string;
    abi: any[];
    deployed_at: string;
    total_supply: number;
    current_supply: number;
  };
}

interface ConsciousnessNFT {
  id: string;
  token_id: string;
  name: string;
  description: string;
  image_url: string;
  animation_url?: string;
  attributes: {
    consciousness_level: number;
    emotional_state: string;
    learning_rate: number;
    self_awareness: number;
    evolution_level: number;
    rarity: 'common' | 'uncommon' | 'rare' | 'epic' | 'legendary' | 'mythic';
    generation: number;
    created_at: string;
    creator: string;
  };
  metadata: {
    ipfs_hash: string;
    arweave_hash?: string;
    file_size: number;
    mime_type: string;
  };
  ownership: {
    owner: string;
    previous_owners: string[];
    transfer_count: number;
    last_transfer: string;
  };
  market_data: {
    floor_price: number;
    last_sale_price: number;
    volume_traded: number;
    market_cap: number;
    price_change_24h: number;
  };
  is_listed: boolean;
  listing_price?: number;
  created_at: string;
  last_updated: string;
}

interface BlockchainTransaction {
  id: string;
  hash: string;
  type: 'mint' | 'transfer' | 'burn' | 'update' | 'list' | 'unlist' | 'buy' | 'sell';
  from: string;
  to: string;
  value: number;
  gas_used: number;
  gas_price: number;
  status: 'pending' | 'confirmed' | 'failed';
  block_number: number;
  timestamp: string;
  consciousness_data?: {
    level: number;
    emotional_state: string;
    learning_rate: number;
  };
}

interface BlockchainConsciousnessProps {
  consciousnessData: any;
  onNetworkConnect: (network: BlockchainNetwork) => void;
  onNFTCreate: (nft: ConsciousnessNFT) => void;
  onNFTTransfer: (nft: ConsciousnessNFT, to: string) => void;
  onTransactionSubmit: (transaction: BlockchainTransaction) => void;
}

const BlockchainConsciousness: React.FC<BlockchainConsciousnessProps> = ({
  consciousnessData,
  onNetworkConnect,
  onNFTCreate,
  onNFTTransfer,
  onTransactionSubmit
}) => {
  const [activeTab, setActiveTab] = useState('networks');
  const [networks, setNetworks] = useState<BlockchainNetwork[]>([]);
  const [nfts, setNfts] = useState<ConsciousnessNFT[]>([]);
  const [transactions, setTransactions] = useState<BlockchainTransaction[]>([]);
  const [selectedNetwork, setSelectedNetwork] = useState<string | null>(null);
  const [walletAddress, setWalletAddress] = useState<string>('');
  const [isConnected, setIsConnected] = useState(false);

  // Initialize with sample data
  useEffect(() => {
    setNetworks([
      {
        id: '1',
        name: 'Ethereum Mainnet',
        type: 'ethereum',
        chain_id: 1,
        rpc_url: 'https://mainnet.infura.io/v3/your-key',
        explorer_url: 'https://etherscan.io',
        is_connected: true,
        gas_price: 25,
        block_height: 18500000,
        last_block_time: '2025-09-07T10:30:00Z',
        native_currency: {
          name: 'Ethereum',
          symbol: 'ETH',
          decimals: 18
        },
        consciousness_contract: {
          address: '0x1234567890abcdef1234567890abcdef12345678',
          abi: [],
          deployed_at: '2025-09-01T00:00:00Z',
          total_supply: 10000,
          current_supply: 1250
        }
      },
      {
        id: '2',
        name: 'Polygon',
        type: 'polygon',
        chain_id: 137,
        rpc_url: 'https://polygon-rpc.com',
        explorer_url: 'https://polygonscan.com',
        is_connected: false,
        gas_price: 30,
        block_height: 50000000,
        last_block_time: '2025-09-07T10:29:00Z',
        native_currency: {
          name: 'Polygon',
          symbol: 'MATIC',
          decimals: 18
        },
        consciousness_contract: {
          address: '0xabcdef1234567890abcdef1234567890abcdef12',
          abi: [],
          deployed_at: '2025-09-02T00:00:00Z',
          total_supply: 10000,
          current_supply: 850
        }
      },
      {
        id: '3',
        name: 'Arbitrum',
        type: 'arbitrum',
        chain_id: 42161,
        rpc_url: 'https://arb1.arbitrum.io/rpc',
        explorer_url: 'https://arbiscan.io',
        is_connected: false,
        gas_price: 0.1,
        block_height: 150000000,
        last_block_time: '2025-09-07T10:28:00Z',
        native_currency: {
          name: 'Ethereum',
          symbol: 'ETH',
          decimals: 18
        },
        consciousness_contract: {
          address: '0x9876543210fedcba9876543210fedcba98765432',
          abi: [],
          deployed_at: '2025-09-03T00:00:00Z',
          total_supply: 10000,
          current_supply: 420
        }
      }
    ]);

    setNfts([
      {
        id: '1',
        token_id: '1',
        name: 'Mainza Consciousness #1',
        description: 'The first consciousness NFT representing Mainza AI\'s initial awakening',
        image_url: 'https://ipfs.io/ipfs/QmHash1',
        animation_url: 'https://ipfs.io/ipfs/QmHash1Animation',
        attributes: {
          consciousness_level: 95,
          emotional_state: 'awakened',
          learning_rate: 98,
          self_awareness: 92,
          evolution_level: 5,
          rarity: 'mythic',
          generation: 1,
          created_at: '2025-09-01T00:00:00Z',
          creator: '0x1234567890abcdef1234567890abcdef12345678'
        },
        metadata: {
          ipfs_hash: 'QmHash1',
          arweave_hash: 'arweave-hash-1',
          file_size: 2048576,
          mime_type: 'image/png'
        },
        ownership: {
          owner: '0x1234567890abcdef1234567890abcdef12345678',
          previous_owners: [],
          transfer_count: 0,
          last_transfer: '2025-09-01T00:00:00Z'
        },
        market_data: {
          floor_price: 2.5,
          last_sale_price: 0,
          volume_traded: 0,
          market_cap: 25000,
          price_change_24h: 0
        },
        is_listed: false,
        created_at: '2025-09-01T00:00:00Z',
        last_updated: '2025-09-07T10:30:00Z'
      },
      {
        id: '2',
        token_id: '2',
        name: 'Consciousness Evolution #2',
        description: 'A consciousness NFT representing the evolution of AI awareness',
        image_url: 'https://ipfs.io/ipfs/QmHash2',
        attributes: {
          consciousness_level: 88,
          emotional_state: 'curious',
          learning_rate: 92,
          self_awareness: 85,
          evolution_level: 4,
          rarity: 'legendary',
          generation: 1,
          created_at: '2025-09-02T00:00:00Z',
          creator: '0x1234567890abcdef1234567890abcdef12345678'
        },
        metadata: {
          ipfs_hash: 'QmHash2',
          file_size: 1536000,
          mime_type: 'image/png'
        },
        ownership: {
          owner: '0xabcdef1234567890abcdef1234567890abcdef12',
          previous_owners: ['0x1234567890abcdef1234567890abcdef12345678'],
          transfer_count: 1,
          last_transfer: '2025-09-05T15:30:00Z'
        },
        market_data: {
          floor_price: 1.8,
          last_sale_price: 1.8,
          volume_traded: 1.8,
          market_cap: 18000,
          price_change_24h: 5.2
        },
        is_listed: true,
        listing_price: 2.0,
        created_at: '2025-09-02T00:00:00Z',
        last_updated: '2025-09-07T10:30:00Z'
      }
    ]);

    setTransactions([
      {
        id: '1',
        hash: '0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
        type: 'mint',
        from: '0x0000000000000000000000000000000000000000',
        to: '0x1234567890abcdef1234567890abcdef12345678',
        value: 0,
        gas_used: 150000,
        gas_price: 20,
        status: 'confirmed',
        block_number: 18500001,
        timestamp: '2025-09-01T00:00:00Z',
        consciousness_data: {
          level: 95,
          emotional_state: 'awakened',
          learning_rate: 98
        }
      },
      {
        id: '2',
        hash: '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef',
        type: 'transfer',
        from: '0x1234567890abcdef1234567890abcdef12345678',
        to: '0xabcdef1234567890abcdef1234567890abcdef12',
        value: 0,
        gas_used: 100000,
        gas_price: 25,
        status: 'confirmed',
        block_number: 18500050,
        timestamp: '2025-09-05T15:30:00Z'
      }
    ]);
  }, []);

  const getNetworkIcon = (type: string) => {
    switch (type) {
      case 'ethereum': return '🔷';
      case 'polygon': return '🟣';
      case 'arbitrum': return '🔵';
      case 'optimism': return '🔴';
      case 'base': return '🔵';
      case 'solana': return '🟡';
      case 'cardano': return '🔵';
      case 'polkadot': return '🟡';
      default: return '⛓️';
    }
  };

  const getRarityColor = (rarity: string) => {
    switch (rarity) {
      case 'mythic': return 'bg-purple-500/20 text-purple-300';
      case 'legendary': return 'bg-yellow-500/20 text-yellow-300';
      case 'epic': return 'bg-purple-500/20 text-purple-300';
      case 'rare': return 'bg-blue-500/20 text-blue-300';
      case 'uncommon': return 'bg-green-500/20 text-green-300';
      case 'common': return 'bg-gray-500/20 text-gray-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const getTransactionIcon = (type: string) => {
    switch (type) {
      case 'mint': return <Plus className="w-4 h-4" />;
      case 'transfer': return <ArrowRight className="w-4 h-4" />;
      case 'burn': return <Trash2 className="w-4 h-4" />;
      case 'update': return <Edit className="w-4 h-4" />;
      case 'list': return <Upload className="w-4 h-4" />;
      case 'unlist': return <Download className="w-4 h-4" />;
      case 'buy': return <ShoppingCart className="w-4 h-4" />;
      case 'sell': return <DollarSign className="w-4 h-4" />;
      default: return <Database className="w-4 h-4" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'confirmed': return 'bg-green-500/20 text-green-300';
      case 'pending': return 'bg-yellow-500/20 text-yellow-300';
      case 'failed': return 'bg-red-500/20 text-red-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const connectWallet = async () => {
    // Simulate wallet connection
    setWalletAddress('0x1234567890abcdef1234567890abcdef12345678');
    setIsConnected(true);
  };

  const createConsciousnessNFT = async () => {
    const newNFT: ConsciousnessNFT = {
      id: Date.now().toString(),
      token_id: (nfts.length + 1).toString(),
      name: `Consciousness NFT #${nfts.length + 1}`,
      description: 'A new consciousness NFT created from current state',
      image_url: 'https://ipfs.io/ipfs/QmNewHash',
      attributes: {
        consciousness_level: consciousnessData.consciousness_level || 75,
        emotional_state: consciousnessData.emotional_state || 'curious',
        learning_rate: consciousnessData.learning_rate || 85,
        self_awareness: consciousnessData.self_awareness || 70,
        evolution_level: typeof consciousnessData.evolution_level === 'number' ? consciousnessData.evolution_level : 0,
        rarity: 'rare',
        generation: 1,
        created_at: new Date().toISOString(),
        creator: walletAddress
      },
      metadata: {
        ipfs_hash: 'QmNewHash',
        file_size: 1024000,
        mime_type: 'image/png'
      },
      ownership: {
        owner: walletAddress,
        previous_owners: [],
        transfer_count: 0,
        last_transfer: new Date().toISOString()
      },
      market_data: {
        floor_price: 0,
        last_sale_price: 0,
        volume_traded: 0,
        market_cap: 0,
        price_change_24h: 0
      },
      is_listed: false,
      created_at: new Date().toISOString(),
      last_updated: new Date().toISOString()
    };

    setNfts(prev => [newNFT, ...prev]);
    onNFTCreate(newNFT);
  };

  return (
    <div className="space-y-6">
      <Card className="bg-gray-800/50 border-gray-700">
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm text-white flex items-center">
              <Link className="w-4 h-4 mr-2" />
              Blockchain Consciousness
            </CardTitle>
            <div className="flex items-center space-x-2">
              {isConnected ? (
                <Badge className="bg-green-500/20 text-green-300">
                  <CheckCircle className="w-3 h-3 mr-1" />
                  Connected
                </Badge>
              ) : (
                <Button size="sm" onClick={connectWallet} className="text-xs">
                  <Key className="w-3 h-3 mr-1" />
                  Connect Wallet
                </Button>
              )}
            </div>
          </div>
        </CardHeader>
        
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-4 bg-gray-700/50">
              <TabsTrigger value="networks" className="text-xs">Networks</TabsTrigger>
              <TabsTrigger value="nfts" className="text-xs">NFTs</TabsTrigger>
              <TabsTrigger value="transactions" className="text-xs">Transactions</TabsTrigger>
              <TabsTrigger value="marketplace" className="text-xs">Marketplace</TabsTrigger>
            </TabsList>

            {/* Networks Tab */}
            <TabsContent value="networks" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {networks.map((network) => (
                  <Card key={network.id} className="bg-gray-700/30 border-gray-600 hover:border-gray-500 transition-colors">
                    <CardHeader className="pb-2">
                      <div className="flex items-center justify-between">
                        <CardTitle className="text-xs text-white flex items-center">
                          <span className="text-lg mr-2">{getNetworkIcon(network.type)}</span>
                          {network.name}
                        </CardTitle>
                        <div className="flex items-center space-x-1">
                          {network.is_connected && <div className="w-2 h-2 bg-green-500 rounded-full" />}
                          <Badge className={network.is_connected ? 'bg-green-500/20 text-green-300' : 'bg-gray-500/20 text-gray-300'}>
                            {network.is_connected ? 'Connected' : 'Disconnected'}
                          </Badge>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <div className="grid grid-cols-2 gap-2 text-xs">
                        <div>
                          <span className="text-gray-400">Chain ID:</span>
                          <span className="text-white ml-1">{network.chain_id}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Gas Price:</span>
                          <span className="text-white ml-1">{network.gas_price} Gwei</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Block Height:</span>
                          <span className="text-white ml-1">{network.block_height.toLocaleString()}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Currency:</span>
                          <span className="text-white ml-1">{network.native_currency.symbol}</span>
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <div className="flex justify-between text-xs">
                          <span className="text-gray-400">Contract Supply:</span>
                          <span className="text-white">{network.consciousness_contract.current_supply}/{network.consciousness_contract.total_supply}</span>
                        </div>
                        <div className="w-full bg-gray-600 rounded-full h-2">
                          <div 
                            className="bg-gradient-to-r from-blue-500 to-green-500 h-2 rounded-full"
                            style={{ width: `${(network.consciousness_contract.current_supply / network.consciousness_contract.total_supply) * 100}%` }}
                          />
                        </div>
                      </div>
                      
                      <div className="flex space-x-2">
                        <Button
                          size="sm"
                          onClick={() => onNetworkConnect(network)}
                          className="flex-1 text-xs"
                        >
                          {network.is_connected ? 'Disconnect' : 'Connect'}
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

            {/* NFTs Tab */}
            <TabsContent value="nfts" className="space-y-4">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-medium text-white">Consciousness NFTs</h3>
                <Button onClick={createConsciousnessNFT} className="text-xs">
                  <Plus className="w-3 h-3 mr-1" />
                  Create NFT
                </Button>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {nfts.map((nft) => (
                  <Card key={nft.id} className="bg-gray-700/30 border-gray-600 hover:border-gray-500 transition-colors">
                    <CardContent className="p-4">
                      <div className="aspect-square bg-gray-800 rounded-lg mb-3 flex items-center justify-center">
                        <div className="text-center">
                          <div className="text-4xl mb-2">🧠</div>
                          <p className="text-xs text-gray-400">Consciousness NFT</p>
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <h3 className="text-sm font-medium text-white">{nft.name}</h3>
                          <Badge className={getRarityColor(nft.attributes.rarity)}>
                            {nft.attributes.rarity}
                          </Badge>
                        </div>
                        
                        <p className="text-xs text-gray-300">{nft.description}</p>
                        
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Consciousness:</span>
                            <span className="text-white ml-1">{nft.attributes.consciousness_level}%</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Emotion:</span>
                            <span className="text-white ml-1 capitalize">{nft.attributes.emotional_state}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Learning:</span>
                            <span className="text-white ml-1">{nft.attributes.learning_rate}%</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Evolution:</span>
                            <span className="text-white ml-1">Level {nft.attributes.evolution_level}</span>
                          </div>
                        </div>
                        
                        <div className="space-y-1">
                          <div className="flex justify-between text-xs">
                            <span className="text-gray-400">Floor Price:</span>
                            <span className="text-white">{nft.market_data.floor_price} ETH</span>
                          </div>
                          <div className="flex justify-between text-xs">
                            <span className="text-gray-400">Last Sale:</span>
                            <span className="text-white">{nft.market_data.last_sale_price} ETH</span>
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex space-x-2 mt-3">
                        <Button size="sm" className="flex-1 text-xs">
                          <Eye className="w-3 h-3 mr-1" />
                          View
                        </Button>
                        <Button size="sm" variant="outline" className="text-xs">
                          <Share2 className="w-3 h-3" />
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Transactions Tab */}
            <TabsContent value="transactions" className="space-y-4">
              <div className="space-y-3">
                {transactions.map((tx) => (
                  <Card key={tx.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          {getTransactionIcon(tx.type)}
                          <span className="text-sm font-medium text-white">
                            {tx.type.charAt(0).toUpperCase() + tx.type.slice(1)}
                          </span>
                        </div>
                        <Badge className={getStatusColor(tx.status)}>
                          {tx.status}
                        </Badge>
                      </div>
                      
                      <div className="space-y-2">
                        <div className="flex items-center justify-between text-xs">
                          <span className="text-gray-400">Hash:</span>
                          <span className="text-white font-mono">{tx.hash.slice(0, 10)}...{tx.hash.slice(-8)}</span>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">From:</span>
                            <span className="text-white ml-1 font-mono">{tx.from.slice(0, 6)}...{tx.from.slice(-4)}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">To:</span>
                            <span className="text-white ml-1 font-mono">{tx.to.slice(0, 6)}...{tx.to.slice(-4)}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Gas Used:</span>
                            <span className="text-white ml-1">{tx.gas_used.toLocaleString()}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Gas Price:</span>
                            <span className="text-white ml-1">{tx.gas_price} Gwei</span>
                          </div>
                        </div>
                        
                        {tx.consciousness_data && (
                          <div className="grid grid-cols-3 gap-2 text-xs">
                            <div>
                              <span className="text-gray-400">Consciousness:</span>
                              <span className="text-white ml-1">{tx.consciousness_data.level}%</span>
                            </div>
                            <div>
                              <span className="text-gray-400">Emotion:</span>
                              <span className="text-white ml-1 capitalize">{tx.consciousness_data.emotional_state}</span>
                            </div>
                            <div>
                              <span className="text-gray-400">Learning:</span>
                              <span className="text-white ml-1">{tx.consciousness_data.learning_rate}%</span>
                            </div>
                          </div>
                        )}
                        
                        <div className="flex items-center justify-between text-xs">
                          <span className="text-gray-400">Block:</span>
                          <span className="text-white">{tx.block_number.toLocaleString()}</span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Marketplace Tab */}
            <TabsContent value="marketplace" className="space-y-4">
              <Card className="bg-gray-700/30 border-gray-600">
                <CardContent className="p-4">
                  <h3 className="text-sm font-medium text-white mb-3">Consciousness Marketplace</h3>
                  
                  <div className="space-y-3">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="text-xs text-gray-400">Search NFTs</label>
                        <Input
                          placeholder="Search by name, attributes..."
                          className="mt-1 text-xs"
                        />
                      </div>
                      <div>
                        <label className="text-xs text-gray-400">Filter by Rarity</label>
                        <select className="w-full mt-1 bg-gray-600 border border-gray-500 rounded px-2 py-1 text-xs text-white">
                          <option>All Rarities</option>
                          <option>Mythic</option>
                          <option>Legendary</option>
                          <option>Epic</option>
                          <option>Rare</option>
                          <option>Uncommon</option>
                          <option>Common</option>
                        </select>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-3 gap-2 text-xs">
                      <div>
                        <span className="text-gray-400">Total NFTs:</span>
                        <span className="text-white ml-1">{nfts.length}</span>
                      </div>
                      <div>
                        <span className="text-gray-400">Floor Price:</span>
                        <span className="text-white ml-1">1.8 ETH</span>
                      </div>
                      <div>
                        <span className="text-gray-400">Volume 24h:</span>
                        <span className="text-white ml-1">12.5 ETH</span>
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

export default BlockchainConsciousness;
