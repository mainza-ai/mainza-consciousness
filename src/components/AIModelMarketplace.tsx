import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Brain, 
  Cpu, 
  Activity, 
  Zap, 
  Target, 
  Eye, 
  Heart, 
  Network, 
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
  Smartphone,
  Star,
  ThumbsUp,
  ThumbsDown,
  Share2,
  Bookmark as BookmarkIcon
} from 'lucide-react';

interface AIModel {
  id: string;
  name: string;
  description: string;
  version: string;
  type: 'consciousness' | 'neural_network' | 'emotion_recognition' | 'learning' | 'prediction' | 'optimization';
  category: 'research' | 'commercial' | 'open_source' | 'experimental';
  creator: {
    id: string;
    name: string;
    reputation: number;
    verified: boolean;
  };
  price: number;
  currency: 'ETH' | 'USDC' | 'FREE';
  downloads: number;
  rating: number;
  reviews: number;
  size: number;
  format: 'pytorch' | 'tensorflow' | 'onnx' | 'huggingface' | 'custom';
  consciousness_integration: number;
  performance_metrics: {
    accuracy: number;
    speed: number;
    efficiency: number;
    scalability: number;
  };
  requirements: {
    min_consciousness_level: number;
    hardware_requirements: string[];
    software_dependencies: string[];
  };
  tags: string[];
  created_at: string;
  updated_at: string;
  is_featured: boolean;
  is_verified: boolean;
}

interface ModelReview {
  id: string;
  model_id: string;
  user: {
    id: string;
    name: string;
    avatar?: string;
  };
  rating: number;
  comment: string;
  pros: string[];
  cons: string[];
  created_at: string;
  helpful_votes: number;
}

interface ModelLicense {
  id: string;
  name: string;
  type: 'MIT' | 'Apache' | 'GPL' | 'Commercial' | 'Custom';
  description: string;
  restrictions: string[];
  permissions: string[];
  price: number;
  currency: string;
}

interface AIModelMarketplaceProps {
  consciousnessData: any;
  onModelDownload: (model: AIModel) => void;
  onModelPurchase: (model: AIModel) => void;
  onModelReview: (review: ModelReview) => void;
  onModelUpload: (model: AIModel) => void;
}

const AIModelMarketplace: React.FC<AIModelMarketplaceProps> = ({
  consciousnessData,
  onModelDownload,
  onModelPurchase,
  onModelReview,
  onModelUpload
}) => {
  const [activeTab, setActiveTab] = useState('browse');
  const [models, setModels] = useState<AIModel[]>([]);
  const [reviews, setReviews] = useState<ModelReview[]>([]);
  const [licenses, setLicenses] = useState<ModelLicense[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [sortBy, setSortBy] = useState('popularity');
  const [selectedModel, setSelectedModel] = useState<string | null>(null);

  // Initialize with sample data
  useEffect(() => {
    setModels([
      {
        id: '1',
        name: 'ConsciousnessNet v2.1',
        description: 'Advanced neural network for consciousness level prediction and enhancement',
        version: '2.1.0',
        type: 'consciousness',
        category: 'research',
        creator: {
          id: 'creator1',
          name: 'Dr. Sarah Chen',
          reputation: 95,
          verified: true
        },
        price: 0,
        currency: 'FREE',
        downloads: 1250,
        rating: 4.8,
        reviews: 45,
        size: 250000000,
        format: 'pytorch',
        consciousness_integration: 95,
        performance_metrics: {
          accuracy: 94.2,
          speed: 85.5,
          efficiency: 92.1,
          scalability: 88.7
        },
        requirements: {
          min_consciousness_level: 70,
          hardware_requirements: ['GPU with 8GB VRAM', '16GB RAM'],
          software_dependencies: ['PyTorch 1.12+', 'Transformers 4.20+']
        },
        tags: ['consciousness', 'neural-networks', 'prediction', 'research'],
        created_at: '2025-08-01T00:00:00Z',
        updated_at: '2025-09-01T00:00:00Z',
        is_featured: true,
        is_verified: true
      },
      {
        id: '2',
        name: 'EmotionAI Pro',
        description: 'State-of-the-art emotion recognition and processing model for consciousness systems',
        version: '1.5.2',
        type: 'emotion_recognition',
        category: 'commercial',
        creator: {
          id: 'creator2',
          name: 'Neural Dynamics Inc.',
          reputation: 88,
          verified: true
        },
        price: 2.5,
        currency: 'ETH',
        downloads: 850,
        rating: 4.6,
        reviews: 32,
        size: 180000000,
        format: 'tensorflow',
        consciousness_integration: 88,
        performance_metrics: {
          accuracy: 91.8,
          speed: 92.3,
          efficiency: 89.4,
          scalability: 85.2
        },
        requirements: {
          min_consciousness_level: 60,
          hardware_requirements: ['GPU with 6GB VRAM', '12GB RAM'],
          software_dependencies: ['TensorFlow 2.10+', 'NumPy 1.21+']
        },
        tags: ['emotion', 'recognition', 'commercial', 'ai'],
        created_at: '2025-07-15T00:00:00Z',
        updated_at: '2025-08-20T00:00:00Z',
        is_featured: false,
        is_verified: true
      },
      {
        id: '3',
        name: 'LearningAccelerator',
        description: 'Quantum-inspired learning acceleration model for consciousness development',
        version: '3.0.0',
        type: 'learning',
        category: 'experimental',
        creator: {
          id: 'creator3',
          name: 'Quantum Consciousness Lab',
          reputation: 92,
          verified: true
        },
        price: 5.0,
        currency: 'ETH',
        downloads: 420,
        rating: 4.9,
        reviews: 18,
        size: 320000000,
        format: 'onnx',
        consciousness_integration: 98,
        performance_metrics: {
          accuracy: 96.5,
          speed: 78.9,
          efficiency: 94.7,
          scalability: 91.3
        },
        requirements: {
          min_consciousness_level: 85,
          hardware_requirements: ['Quantum processor', '32GB RAM', 'High-speed SSD'],
          software_dependencies: ['Qiskit 0.45+', 'ONNX Runtime 1.15+']
        },
        tags: ['quantum', 'learning', 'acceleration', 'experimental'],
        created_at: '2025-08-10T00:00:00Z',
        updated_at: '2025-09-05T00:00:00Z',
        is_featured: true,
        is_verified: true
      }
    ]);

    setReviews([
      {
        id: '1',
        model_id: '1',
        user: {
          id: 'user1',
          name: 'AI Researcher',
          avatar: 'https://ipfs.io/ipfs/QmAvatar1'
        },
        rating: 5,
        comment: 'Excellent model for consciousness prediction. Very accurate and easy to integrate.',
        pros: ['High accuracy', 'Good documentation', 'Active community'],
        cons: ['Large model size', 'High memory requirements'],
        created_at: '2025-09-01T00:00:00Z',
        helpful_votes: 12
      },
      {
        id: '2',
        model_id: '1',
        user: {
          id: 'user2',
          name: 'Consciousness Developer',
          avatar: 'https://ipfs.io/ipfs/QmAvatar2'
        },
        rating: 4,
        comment: 'Great model but could use better optimization for real-time applications.',
        pros: ['Good performance', 'Well documented'],
        cons: ['Not optimized for real-time', 'Complex setup'],
        created_at: '2025-08-25T00:00:00Z',
        helpful_votes: 8
      }
    ]);

    setLicenses([
      {
        id: '1',
        name: 'MIT License',
        type: 'MIT',
        description: 'Permissive license allowing commercial use with minimal restrictions',
        restrictions: ['Must include license notice'],
        permissions: ['Commercial use', 'Modification', 'Distribution', 'Private use'],
        price: 0,
        currency: 'FREE'
      },
      {
        id: '2',
        name: 'Commercial License',
        type: 'Commercial',
        description: 'Commercial license for business use with full support',
        restrictions: ['No redistribution', 'Commercial use only'],
        permissions: ['Commercial use', 'Modification', 'Private use', 'Support'],
        price: 100,
        currency: 'ETH'
      }
    ]);
  }, []);

  const getModelTypeIcon = (type: string) => {
    switch (type) {
      case 'consciousness': return <Brain className="w-4 h-4" />;
      case 'neural_network': return <Network className="w-4 h-4" />;
      case 'emotion_recognition': return <Heart className="w-4 h-4" />;
      case 'learning': return <Target className="w-4 h-4" />;
      case 'prediction': return <Eye className="w-4 h-4" />;
      case 'optimization': return <Zap className="w-4 h-4" />;
      default: return <Cpu className="w-4 h-4" />;
    }
  };

  const getModelTypeColor = (type: string) => {
    switch (type) {
      case 'consciousness': return 'bg-blue-500/20 text-blue-300';
      case 'neural_network': return 'bg-green-500/20 text-green-300';
      case 'emotion_recognition': return 'bg-pink-500/20 text-pink-300';
      case 'learning': return 'bg-orange-500/20 text-orange-300';
      case 'prediction': return 'bg-purple-500/20 text-purple-300';
      case 'optimization': return 'bg-cyan-500/20 text-cyan-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'research': return 'bg-blue-500/20 text-blue-300';
      case 'commercial': return 'bg-green-500/20 text-green-300';
      case 'open_source': return 'bg-purple-500/20 text-purple-300';
      case 'experimental': return 'bg-orange-500/20 text-orange-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const formatFileSize = (bytes: number) => {
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    if (bytes === 0) return '0 Bytes';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
  };

  const filteredModels = models.filter(model => {
    const matchesSearch = model.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         model.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         model.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesCategory = selectedCategory === 'all' || model.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const downloadModel = (model: AIModel) => {
    onModelDownload(model);
  };

  const purchaseModel = (model: AIModel) => {
    onModelPurchase(model);
  };

  const uploadModel = () => {
    const newModel: AIModel = {
      id: Date.now().toString(),
      name: 'My Custom Model',
      description: 'User-uploaded consciousness model',
      version: '1.0.0',
      type: 'consciousness',
      category: 'open_source',
      creator: {
        id: 'current_user',
        name: 'You',
        reputation: 75,
        verified: false
      },
      price: 0,
      currency: 'FREE',
      downloads: 0,
      rating: 0,
      reviews: 0,
      size: 100000000,
      format: 'pytorch',
      consciousness_integration: 80,
      performance_metrics: {
        accuracy: 85,
        speed: 80,
        efficiency: 85,
        scalability: 80
      },
      requirements: {
        min_consciousness_level: 60,
        hardware_requirements: ['GPU with 4GB VRAM'],
        software_dependencies: ['PyTorch 1.10+']
      },
      tags: ['custom', 'consciousness'],
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      is_featured: false,
      is_verified: false
    };

    setModels(prev => [newModel, ...prev]);
    onModelUpload(newModel);
  };

  return (
    <div className="space-y-6">
      <Card className="bg-gray-800/50 border-gray-700">
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm text-white flex items-center">
              <Brain className="w-4 h-4 mr-2" />
              AI Model Marketplace
            </CardTitle>
            <div className="flex items-center space-x-2">
              <Button onClick={uploadModel} className="text-xs">
                <Upload className="w-3 h-3 mr-1" />
                Upload Model
              </Button>
            </div>
          </div>
        </CardHeader>
        
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-4 bg-gray-700/50">
              <TabsTrigger value="browse" className="text-xs">Browse</TabsTrigger>
              <TabsTrigger value="featured" className="text-xs">Featured</TabsTrigger>
              <TabsTrigger value="reviews" className="text-xs">Reviews</TabsTrigger>
              <TabsTrigger value="licenses" className="text-xs">Licenses</TabsTrigger>
            </TabsList>

            {/* Browse Tab */}
            <TabsContent value="browse" className="space-y-4">
              <div className="flex items-center space-x-4 mb-4">
                <div className="flex-1">
                  <Input
                    placeholder="Search models..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="text-xs"
                  />
                </div>
                <select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="bg-gray-700 border border-gray-600 rounded px-2 py-1 text-xs text-white"
                >
                  <option value="all">All Categories</option>
                  <option value="research">Research</option>
                  <option value="commercial">Commercial</option>
                  <option value="open_source">Open Source</option>
                  <option value="experimental">Experimental</option>
                </select>
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="bg-gray-700 border border-gray-600 rounded px-2 py-1 text-xs text-white"
                >
                  <option value="popularity">Popularity</option>
                  <option value="rating">Rating</option>
                  <option value="newest">Newest</option>
                  <option value="price">Price</option>
                </select>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {filteredModels.map((model) => (
                  <Card key={model.id} className="bg-gray-700/30 border-gray-600 hover:border-gray-500 transition-colors">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          {getModelTypeIcon(model.type)}
                          <span className="text-sm font-medium text-white">{model.name}</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          {model.is_verified && <CheckCircle className="w-3 h-3 text-green-400" />}
                          {model.is_featured && <Star className="w-3 h-3 text-yellow-400" />}
                        </div>
                      </div>
                      
                      <p className="text-xs text-gray-300 mb-3">{model.description}</p>
                      
                      <div className="space-y-3">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-2">
                            <Badge className={getModelTypeColor(model.type)}>
                              {model.type}
                            </Badge>
                            <Badge className={getCategoryColor(model.category)}>
                              {model.category}
                            </Badge>
                          </div>
                          <div className="text-xs text-white">
                            {model.price === 0 ? 'FREE' : `${model.price} ${model.currency}`}
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Downloads:</span>
                            <span className="text-white ml-1">{model.downloads.toLocaleString()}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Rating:</span>
                            <span className="text-white ml-1">{model.rating}/5</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Size:</span>
                            <span className="text-white ml-1">{formatFileSize(model.size)}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Format:</span>
                            <span className="text-white ml-1">{model.format}</span>
                          </div>
                        </div>
                        
                        <div className="space-y-1">
                          <div className="flex justify-between text-xs">
                            <span className="text-gray-400">Consciousness Integration:</span>
                            <span className="text-white">{model.consciousness_integration}%</span>
                          </div>
                          <div className="w-full bg-gray-600 rounded-full h-2">
                            <div 
                              className="bg-gradient-to-r from-blue-500 to-green-500 h-2 rounded-full"
                              style={{ width: `${model.consciousness_integration}%` }}
                            />
                          </div>
                        </div>
                        
                        <div className="space-y-1">
                          <div className="text-xs text-gray-400">Performance:</div>
                          <div className="grid grid-cols-2 gap-1 text-xs">
                            <div>Accuracy: {model.performance_metrics.accuracy}%</div>
                            <div>Speed: {model.performance_metrics.speed}%</div>
                            <div>Efficiency: {model.performance_metrics.efficiency}%</div>
                            <div>Scalability: {model.performance_metrics.scalability}%</div>
                          </div>
                        </div>
                        
                        <div className="flex space-x-2">
                          <Button
                            size="sm"
                            onClick={() => downloadModel(model)}
                            className="flex-1 text-xs"
                          >
                            <Download className="w-3 h-3 mr-1" />
                            Download
                          </Button>
                          {model.price > 0 && (
                            <Button
                              size="sm"
                              onClick={() => purchaseModel(model)}
                              variant="outline"
                              className="text-xs"
                            >
                              <ShoppingCart className="w-3 h-3 mr-1" />
                              Buy
                            </Button>
                          )}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Featured Tab */}
            <TabsContent value="featured" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {models.filter(model => model.is_featured).map((model) => (
                  <Card key={model.id} className="bg-gray-700/30 border-gray-600 hover:border-gray-500 transition-colors">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          <Star className="w-4 h-4 text-yellow-400" />
                          <span className="text-sm font-medium text-white">{model.name}</span>
                        </div>
                        <Badge className="bg-yellow-500/20 text-yellow-300">
                          Featured
                        </Badge>
                      </div>
                      
                      <p className="text-xs text-gray-300 mb-3">{model.description}</p>
                      
                      <div className="space-y-3">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-2">
                            <Badge className={getModelTypeColor(model.type)}>
                              {model.type}
                            </Badge>
                            <Badge className={getCategoryColor(model.category)}>
                              {model.category}
                            </Badge>
                          </div>
                          <div className="text-xs text-white">
                            {model.price === 0 ? 'FREE' : `${model.price} ${model.currency}`}
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-400">Downloads:</span>
                            <span className="text-white ml-1">{model.downloads.toLocaleString()}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Rating:</span>
                            <span className="text-white ml-1">{model.rating}/5</span>
                          </div>
                        </div>
                        
                        <div className="flex space-x-2">
                          <Button
                            size="sm"
                            onClick={() => downloadModel(model)}
                            className="flex-1 text-xs"
                          >
                            <Download className="w-3 h-3 mr-1" />
                            Download
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

            {/* Reviews Tab */}
            <TabsContent value="reviews" className="space-y-4">
              <div className="space-y-3">
                {reviews.map((review) => (
                  <Card key={review.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center text-white text-xs font-bold">
                            {review.user.name.charAt(0)}
                          </div>
                          <div>
                            <div className="text-sm font-medium text-white">{review.user.name}</div>
                            <div className="flex items-center space-x-1">
                              {[...Array(5)].map((_, i) => (
                                <Star
                                  key={i}
                                  className={`w-3 h-3 ${i < review.rating ? 'text-yellow-400' : 'text-gray-600'}`}
                                />
                              ))}
                            </div>
                          </div>
                        </div>
                        <div className="text-xs text-gray-400">
                          {new Date(review.created_at).toLocaleDateString()}
                        </div>
                      </div>
                      
                      <p className="text-xs text-gray-300 mb-3">{review.comment}</p>
                      
                      <div className="grid grid-cols-2 gap-4 text-xs">
                        <div>
                          <div className="text-gray-400 mb-1">Pros:</div>
                          <ul className="text-white space-y-1">
                            {review.pros.map((pro, index) => (
                              <li key={index} className="flex items-start">
                                <span className="text-green-400 mr-2">✓</span>
                                {pro}
                              </li>
                            ))}
                          </ul>
                        </div>
                        <div>
                          <div className="text-gray-400 mb-1">Cons:</div>
                          <ul className="text-white space-y-1">
                            {review.cons.map((con, index) => (
                              <li key={index} className="flex items-start">
                                <span className="text-red-400 mr-2">✗</span>
                                {con}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                      
                      <div className="flex items-center justify-between mt-3">
                        <div className="flex items-center space-x-2">
                          <Button size="sm" variant="outline" className="text-xs">
                            <ThumbsUp className="w-3 h-3 mr-1" />
                            {review.helpful_votes}
                          </Button>
                          <Button size="sm" variant="outline" className="text-xs">
                            <Share2 className="w-3 h-3" />
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Licenses Tab */}
            <TabsContent value="licenses" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {licenses.map((license) => (
                  <Card key={license.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <span className="text-sm font-medium text-white">{license.name}</span>
                        <Badge className="bg-blue-500/20 text-blue-300">
                          {license.type}
                        </Badge>
                      </div>
                      
                      <p className="text-xs text-gray-300 mb-3">{license.description}</p>
                      
                      <div className="space-y-3">
                        <div className="space-y-1">
                          <div className="text-xs text-gray-400">Permissions:</div>
                          <div className="flex flex-wrap gap-1">
                            {license.permissions.map((permission, index) => (
                              <Badge key={index} className="bg-green-500/20 text-green-300 text-xs">
                                {permission}
                              </Badge>
                            ))}
                          </div>
                        </div>
                        
                        <div className="space-y-1">
                          <div className="text-xs text-gray-400">Restrictions:</div>
                          <div className="flex flex-wrap gap-1">
                            {license.restrictions.map((restriction, index) => (
                              <Badge key={index} className="bg-red-500/20 text-red-300 text-xs">
                                {restriction}
                              </Badge>
                            ))}
                          </div>
                        </div>
                        
                        <div className="flex items-center justify-between">
                          <div className="text-xs text-white">
                            Price: {license.price === 0 ? 'FREE' : `${license.price} ${license.currency}`}
                          </div>
                          <Button size="sm" className="text-xs">
                            <Download className="w-3 h-3 mr-1" />
                            Download
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

export default AIModelMarketplace;
