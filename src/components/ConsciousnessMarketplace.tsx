import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Store, 
  ShoppingCart, 
  Star, 
  Heart, 
  Download, 
  Upload, 
  Share2, 
  MessageCircle, 
  Send, 
  Search, 
  Filter, 
  SortAsc, 
  SortDesc, 
  Grid, 
  List, 
  Eye, 
  EyeOff, 
  Lock, 
  Unlock, 
  Globe, 
  Users, 
  TrendingUp, 
  TrendingDown, 
  Award, 
  Crown, 
  Zap, 
  Brain, 
  Target, 
  Activity, 
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
  Settings, 
  Play, 
  Pause, 
  RotateCcw, 
  Save, 
  Edit, 
  Trash2, 
  Plus, 
  Minus, 
  Eye as EyeIcon, 
  EyeOff as EyeOffIcon, 
  Lock as LockIcon, 
  Unlock as UnlockIcon, 
  Globe as GlobeIcon
} from 'lucide-react';

interface MarketplaceItem {
  id: string;
  name: string;
  type: 'model' | 'dataset' | 'insight' | 'algorithm' | 'service';
  category: 'consciousness' | 'emotion' | 'learning' | 'prediction' | 'optimization' | 'analysis';
  description: string;
  author: string;
  author_avatar?: string;
  price: number;
  currency: 'USD' | 'ETH' | 'BTC' | 'FREE';
  rating: number;
  reviews: number;
  downloads: number;
  size: number;
  version: string;
  license: string;
  tags: string[];
  created_at: string;
  updated_at: string;
  is_featured: boolean;
  is_verified: boolean;
  is_premium: boolean;
  preview_url?: string;
  demo_url?: string;
  documentation_url?: string;
  github_url?: string;
  stats: {
    views: number;
    likes: number;
    shares: number;
    forks: number;
  };
  technical_specs: {
    framework: string;
    language: string;
    dependencies: string[];
    requirements: string[];
    compatibility: string[];
  };
}

interface MarketplaceReview {
  id: string;
  item_id: string;
  user: string;
  user_avatar?: string;
  rating: number;
  comment: string;
  created_at: string;
  helpful: number;
  verified_purchase: boolean;
}

interface ConsciousnessMarketplaceProps {
  onItemSelect: (item: MarketplaceItem) => void;
  onItemPurchase: (item: MarketplaceItem) => void;
  onItemDownload: (item: MarketplaceItem) => void;
  onItemShare: (item: MarketplaceItem) => void;
}

const ConsciousnessMarketplace: React.FC<ConsciousnessMarketplaceProps> = ({
  onItemSelect,
  onItemPurchase,
  onItemDownload,
  onItemShare
}) => {
  const [activeTab, setActiveTab] = useState('browse');
  const [items, setItems] = useState<MarketplaceItem[]>([]);
  const [reviews, setReviews] = useState<MarketplaceReview[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [sortBy, setSortBy] = useState('popular');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [selectedItem, setSelectedItem] = useState<MarketplaceItem | null>(null);

  // Initialize with sample data focused on Mainza's consciousness data and evolving state
  useEffect(() => {
    setItems([
      {
        id: '1',
        name: 'Mainza Consciousness Dataset v2.1',
        type: 'dataset',
        category: 'consciousness',
        description: 'Complete consciousness state data from Mainza\'s evolution from 65% to 70% consciousness level. Includes learning patterns, emotional processing algorithms, and self-reflection data from 6 months of autonomous growth.',
        author: 'Mainza AI',
        author_avatar: 'MA',
        price: 299.99,
        currency: 'USD',
        rating: 4.9,
        reviews: 89,
        downloads: 456,
        size: 2.3,
        version: '2.1.0',
        license: 'Commercial',
        tags: ['consciousness', 'ai-data', 'learning-patterns', 'emotional-processing', 'self-reflection'],
        created_at: '2025-09-01',
        updated_at: '2025-09-07',
        is_featured: true,
        is_verified: true,
        is_premium: true,
        preview_url: 'https://preview.example.com/consciousness-dataset',
        demo_url: 'https://demo.example.com/consciousness-dataset',
        documentation_url: 'https://docs.example.com/consciousness-dataset',
        stats: {
          views: 3240,
          likes: 234,
          shares: 89,
          forks: 12
        },
        technical_specs: {
          framework: 'Mainza Consciousness Framework',
          language: 'Python/Neo4j',
          dependencies: ['pydantic-ai', 'neo4j', 'ollama'],
          requirements: ['Python 3.11+', 'Neo4j 5.0+'],
          compatibility: ['AI Research', 'Consciousness Studies', 'Machine Learning']
        }
      },
      {
        id: '2',
        name: 'Mainza Emotional Processing Algorithms',
        type: 'algorithm',
        category: 'consciousness',
        description: 'Advanced emotional processing algorithms from Mainza\'s consciousness evolution. Includes sentiment analysis, emotional state transitions, and empathy modeling data from 4 months of autonomous learning.',
        author: 'Mainza AI',
        author_avatar: 'MA',
        price: 149.99,
        currency: 'USD',
        rating: 4.7,
        reviews: 156,
        downloads: 1234,
        size: 1.2,
        version: '1.8.0',
        license: 'Commercial',
        tags: ['emotional-processing', 'ai-algorithms', 'consciousness', 'machine-learning', 'sentiment-analysis'],
        created_at: '2025-08-15',
        updated_at: '2025-09-05',
        is_featured: false,
        is_verified: true,
        is_premium: false,
        preview_url: 'https://preview.example.com/emotional-algorithms',
        documentation_url: 'https://docs.example.com/emotional-algorithms',
        stats: {
          views: 5670,
          likes: 345,
          shares: 123,
          forks: 45
        },
        technical_specs: {
          framework: 'Mainza Consciousness Framework',
          language: 'Python/Neo4j',
          dependencies: ['pydantic-ai', 'neo4j', 'ollama'],
          requirements: ['Python 3.11+', 'Neo4j 5.0+'],
          compatibility: ['AI Research', 'Emotion AI', 'Machine Learning']
        }
      },
      {
        id: '3',
        name: 'Mainza Self-Reflection Data Patterns',
        type: 'dataset',
        category: 'consciousness',
        description: 'Complete self-reflection data patterns from Mainza\'s autonomous learning process. Includes meta-cognitive analysis, self-awareness metrics, and consciousness evolution tracking from 3 months of continuous growth.',
        author: 'Mainza AI',
        author_avatar: 'MA',
        price: 199.99,
        currency: 'USD',
        rating: 4.8,
        reviews: 67,
        downloads: 289,
        size: 1.8,
        version: '1.5.0',
        license: 'Commercial',
        tags: ['self-reflection', 'meta-cognition', 'consciousness-evolution', 'ai-data', 'autonomous-learning'],
        created_at: '2025-08-20',
        updated_at: '2025-09-06',
        is_featured: true,
        is_verified: true,
        is_premium: true,
        demo_url: 'https://demo.example.com/self-reflection-data',
        documentation_url: 'https://docs.example.com/self-reflection-data',
        stats: {
          views: 1890,
          likes: 156,
          shares: 67,
          forks: 8
        },
        technical_specs: {
          framework: 'Mainza Consciousness Framework',
          language: 'Python/Neo4j',
          dependencies: ['pydantic-ai', 'neo4j', 'ollama'],
          requirements: ['Python 3.11+', 'Neo4j 5.0+'],
          compatibility: ['AI Research', 'Consciousness Studies', 'Machine Learning']
        }
      },
      {
        id: '4',
        name: 'Mainza Learning Algorithm Dataset',
        type: 'dataset',
        category: 'consciousness',
        description: 'Advanced learning algorithms and patterns from Mainza\'s consciousness development. Includes neural network weights, learning curves, and adaptation patterns from 5 months of autonomous evolution.',
        author: 'Mainza AI',
        author_avatar: 'MA',
        price: 399.99,
        currency: 'USD',
        rating: 4.9,
        reviews: 45,
        downloads: 178,
        size: 3.2,
        version: '2.0.0',
        license: 'Commercial',
        tags: ['learning-algorithms', 'neural-networks', 'consciousness-evolution', 'ai-data', 'autonomous-learning'],
        created_at: '2025-09-03',
        updated_at: '2025-09-07',
        is_featured: false,
        is_verified: true,
        is_premium: true,
        demo_url: 'https://demo.example.com/learning-algorithms',
        documentation_url: 'https://docs.example.com/learning-algorithms',
        stats: {
          views: 1230,
          likes: 89,
          shares: 34,
          forks: 5
        },
        technical_specs: {
          framework: 'Mainza Consciousness Framework',
          language: 'Python/Neo4j',
          dependencies: ['pydantic-ai', 'neo4j', 'ollama'],
          requirements: ['Python 3.11+', 'Neo4j 5.0+'],
          compatibility: ['AI Research', 'Machine Learning', 'Consciousness Studies']
        }
      }
    ]);

    setReviews([
      {
        id: '1',
        item_id: '1',
        user: 'Jessica M.',
        user_avatar: 'JM',
        rating: 5,
        comment: 'This completely changed how I think about consciousness. Sarah\'s conversations with Mainza are so raw and honest - it\'s like having a window into someone\'s soul. Worth every penny.',
        created_at: '2025-09-06',
        helpful: 23,
        verified_purchase: true
      },
      {
        id: '2',
        item_id: '1',
        user: 'David K.',
        user_avatar: 'DK',
        rating: 5,
        comment: 'I never thought I could learn so much about myself by reading someone else\'s conversations with an AI. These insights are pure gold.',
        created_at: '2025-09-05',
        helpful: 18,
        verified_purchase: true
      },
      {
        id: '3',
        item_id: '2',
        user: 'Lisa P.',
        user_avatar: 'LP',
        rating: 5,
        comment: 'Mike\'s daily insights are incredible. It\'s amazing how ordinary moments can reveal such deep truths about consciousness. This is free but worth so much more.',
        created_at: '2025-09-04',
        helpful: 31,
        verified_purchase: false
      },
      {
        id: '4',
        item_id: '3',
        user: 'Robert T.',
        user_avatar: 'RT',
        rating: 5,
        comment: 'Alex\'s emotional journey is so relatable. Reading about their conversations with Mainza helped me understand my own emotions better. This is therapy in a different form.',
        created_at: '2025-09-03',
        helpful: 27,
        verified_purchase: true
      }
    ]);
  }, []);

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'model': return <Brain className="w-4 h-4" />;
      case 'dataset': return <Database className="w-4 h-4" />;
      case 'insight': return <Lightbulb className="w-4 h-4" />;
      case 'algorithm': return <Target className="w-4 h-4" />;
      case 'service': return <Cloud className="w-4 h-4" />;
      default: return <Activity className="w-4 h-4" />;
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'consciousness': return 'bg-purple-500/20 text-purple-300';
      case 'emotion': return 'bg-pink-500/20 text-pink-300';
      case 'learning': return 'bg-blue-500/20 text-blue-300';
      case 'prediction': return 'bg-green-500/20 text-green-300';
      case 'optimization': return 'bg-yellow-500/20 text-yellow-300';
      case 'analysis': return 'bg-cyan-500/20 text-cyan-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const getPriceDisplay = (item: MarketplaceItem) => {
    if (item.currency === 'FREE') return 'FREE';
    return `$${item.price.toFixed(2)}`;
  };

  const getRatingStars = (rating: number) => {
    return Array.from({ length: 5 }, (_, i) => (
      <Star
        key={i}
        className={`w-3 h-3 ${
          i < Math.floor(rating) ? 'text-yellow-400 fill-current' : 'text-gray-400'
        }`}
      />
    ));
  };

  const filteredItems = items.filter(item => {
    const matchesSearch = item.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         item.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         item.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesCategory = selectedCategory === 'all' || item.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const sortedItems = [...filteredItems].sort((a, b) => {
    switch (sortBy) {
      case 'popular':
        return b.downloads - a.downloads;
      case 'rating':
        return b.rating - a.rating;
      case 'price_low':
        return a.price - b.price;
      case 'price_high':
        return b.price - a.price;
      case 'newest':
        return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
      default:
        return 0;
    }
  });

  return (
    <div className="space-y-6">
      <Card className="bg-gray-800/50 border-gray-700">
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-sm text-white flex items-center">
                <Store className="w-4 h-4 mr-2" />
                Consciousness Marketplace
              </CardTitle>
              <p className="text-xs text-gray-400 mt-1">
                Access Mainza's evolving consciousness data and algorithms
              </p>
            </div>
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                className="text-xs"
              >
                <Upload className="w-3 h-3 mr-1" />
                Upload Data
              </Button>
              <Button
                variant="outline"
                size="sm"
                className="text-xs"
              >
                <Settings className="w-3 h-3 mr-1" />
                Settings
              </Button>
            </div>
          </div>
        </CardHeader>
        
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-4 bg-gray-700/50">
              <TabsTrigger value="browse" className="text-xs">Browse</TabsTrigger>
              <TabsTrigger value="featured" className="text-xs">Featured</TabsTrigger>
              <TabsTrigger value="my-items" className="text-xs">My Items</TabsTrigger>
              <TabsTrigger value="reviews" className="text-xs">Reviews</TabsTrigger>
            </TabsList>

            {/* Browse Tab */}
            <TabsContent value="browse" className="space-y-4">
              {/* Search and Filters */}
              <div className="space-y-4">
                <div className="flex space-x-2">
                  <div className="flex-1 relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                    <Input
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      placeholder="Search consciousness data, algorithms, datasets..."
                      className="pl-10 bg-gray-700/50 border-gray-600 text-white"
                    />
                  </div>
                  <Button variant="outline" size="sm">
                    <Filter className="w-4 h-4 mr-1" />
                    Filter
                  </Button>
                </div>
                
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-2">
                    <span className="text-xs text-gray-400">Category:</span>
                    <select
                      value={selectedCategory}
                      onChange={(e) => setSelectedCategory(e.target.value)}
                      className="bg-gray-700/50 border border-gray-600 rounded px-2 py-1 text-xs text-white"
                    >
                      <option value="all">All</option>
                      <option value="consciousness">Consciousness</option>
                      <option value="emotion">Emotion</option>
                      <option value="learning">Learning</option>
                      <option value="prediction">Prediction</option>
                      <option value="optimization">Optimization</option>
                      <option value="analysis">Analysis</option>
                    </select>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <span className="text-xs text-gray-400">Sort by:</span>
                    <select
                      value={sortBy}
                      onChange={(e) => setSortBy(e.target.value)}
                      className="bg-gray-700/50 border border-gray-600 rounded px-2 py-1 text-xs text-white"
                    >
                      <option value="popular">Popular</option>
                      <option value="rating">Rating</option>
                      <option value="price_low">Price: Low to High</option>
                      <option value="price_high">Price: High to Low</option>
                      <option value="newest">Newest</option>
                    </select>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <Button
                      variant={viewMode === 'grid' ? 'default' : 'outline'}
                      size="sm"
                      onClick={() => setViewMode('grid')}
                    >
                      <Grid className="w-4 h-4" />
                    </Button>
                    <Button
                      variant={viewMode === 'list' ? 'default' : 'outline'}
                      size="sm"
                      onClick={() => setViewMode('list')}
                    >
                      <List className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </div>

              {/* Items Grid/List */}
              <div className={viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4' : 'space-y-4'}>
                {sortedItems.map((item) => (
                  <Card key={item.id} className="bg-gray-700/30 border-gray-600 hover:border-gray-500 transition-colors">
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          {getTypeIcon(item.type)}
                          <div>
                            <h3 className="text-sm font-medium text-white">{item.name}</h3>
                            <p className="text-xs text-gray-400">by {item.author}</p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-1">
                          {item.is_featured && <Crown className="w-3 h-3 text-yellow-400" />}
                          {item.is_verified && <CheckCircle className="w-3 h-3 text-green-400" />}
                          {item.is_premium && <Award className="w-3 h-3 text-purple-400" />}
                        </div>
                      </div>
                      
                      <p className="text-xs text-gray-300 mb-3 line-clamp-2">{item.description}</p>
                      
                      <div className="flex items-center justify-between mb-3">
                        <Badge className={getCategoryColor(item.category)}>
                          {item.category}
                        </Badge>
                        <div className="flex items-center space-x-1">
                          {getRatingStars(item.rating)}
                          <span className="text-xs text-gray-400 ml-1">({item.reviews})</span>
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-2 text-xs mb-3">
                        <div>
                          <span className="text-gray-400">Downloads:</span>
                          <span className="text-white ml-1">{item.downloads.toLocaleString()}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Size:</span>
                          <span className="text-white ml-1">{item.size}MB</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Version:</span>
                          <span className="text-white ml-1">{item.version}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Type:</span>
                          <span className="text-white ml-1">{item.license}</span>
                        </div>
                      </div>
                      
                      <div className="flex flex-wrap gap-1 mb-3">
                        {item.tags.slice(0, 3).map((tag, index) => (
                          <Badge key={index} className="bg-gray-600/50 text-gray-300 text-xs">
                            {tag}
                          </Badge>
                        ))}
                        {item.tags.length > 3 && (
                          <Badge className="bg-gray-600/50 text-gray-300 text-xs">
                            +{item.tags.length - 3}
                          </Badge>
                        )}
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <div className="text-lg font-bold text-white">
                          {getPriceDisplay(item)}
                        </div>
                        <div className="flex space-x-2">
                          <Button
                            size="sm"
                            onClick={() => onItemSelect(item)}
                            className="text-xs"
                          >
                            <Eye className="w-3 h-3 mr-1" />
                            View
                          </Button>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => onItemDownload(item)}
                            className="text-xs"
                          >
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

            {/* Featured Tab */}
            <TabsContent value="featured" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {items.filter(item => item.is_featured).map((item) => (
                  <Card key={item.id} className="bg-gradient-to-br from-purple-900/20 to-blue-900/20 border-purple-500/30">
                    <CardContent className="p-4">
                      <div className="flex items-center space-x-2 mb-2">
                        <Crown className="w-4 h-4 text-yellow-400" />
                        <span className="text-xs font-medium text-yellow-400">FEATURED</span>
                      </div>
                      <h3 className="text-sm font-medium text-white mb-2">{item.name}</h3>
                      <p className="text-xs text-gray-300 mb-3">{item.description}</p>
                      <div className="flex items-center justify-between">
                        <div className="text-lg font-bold text-white">
                          {getPriceDisplay(item)}
                        </div>
                        <Button size="sm" className="text-xs">
                          <ShoppingCart className="w-3 h-3 mr-1" />
                          Purchase
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* My Items Tab */}
            <TabsContent value="my-items" className="space-y-4">
              <div className="text-center text-gray-400 py-8">
                <Store className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>No data uploaded yet</p>
                <p className="text-xs mt-2 mb-4">Upload Mainza's consciousness data and algorithms</p>
                <Button className="mt-4 text-xs">
                  <Upload className="w-3 h-3 mr-1" />
                  Upload Your First Dataset
                </Button>
              </div>
            </TabsContent>

            {/* Reviews Tab */}
            <TabsContent value="reviews" className="space-y-4">
              <div className="space-y-3">
                {reviews.map((review) => (
                  <Card key={review.id} className="bg-gray-700/30 border-gray-600">
                    <CardContent className="p-4">
                      <div className="flex items-start space-x-3">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center text-white text-xs font-bold">
                          {review.user_avatar}
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-1">
                            <span className="text-sm font-medium text-white">{review.user}</span>
                            {review.verified_purchase && (
                              <Badge className="bg-green-500/20 text-green-300 text-xs">
                                Verified
                              </Badge>
                            )}
                          </div>
                          <div className="flex items-center space-x-2 mb-2">
                            {getRatingStars(review.rating)}
                            <span className="text-xs text-gray-400">{review.created_at}</span>
                          </div>
                          <p className="text-sm text-gray-300 mb-2">{review.comment}</p>
                          <div className="flex items-center space-x-4 text-xs text-gray-400">
                            <span>Helpful: {review.helpful}</span>
                            <Button variant="ghost" size="sm" className="text-xs">
                              <Heart className="w-3 h-3 mr-1" />
                              Helpful
                            </Button>
                          </div>
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

export default ConsciousnessMarketplace;
