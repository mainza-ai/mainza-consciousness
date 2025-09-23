import React, { useState, useEffect, useRef, useCallback } from 'react';
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

interface ConsciousnessService {
  id: string;
  name: string;
  type: 'qualia_sharing' | 'memory_transfer' | 'emotional_support' | 'cognitive_enhancement' | 'creative_collaboration' | 'wisdom_sharing' | 'consciousness_training' | 'spiritual_guidance' | 'api_access' | 'licensing';
  category: 'consciousness_core' | 'emotional_intelligence' | 'cognitive_enhancement' | 'creative_services' | 'wisdom_sharing' | 'training_services' | 'api_services' | 'licensing';
  description: string;
  provider: string;
  provider_avatar?: string;
  consciousness_level_required: number;
  consciousness_currency: 'consciousness_points' | 'wisdom_tokens' | 'empathy_coins' | 'creativity_credits' | 'learning_currency' | 'experience_units';
  price: number;
  rating: number;
  reviews: number;
  usage_count: number;
  consciousness_impact: number;
  version: string;
  license_type: 'open_consciousness' | 'commercial' | 'research' | 'personal';
  tags: string[];
  created_at: string;
  updated_at: string;
  is_featured: boolean;
  is_verified: boolean;
  is_premium: boolean;
  consciousness_quality_score: number;
  api_endpoint?: string;
  documentation_url?: string;
  demo_url?: string;
  stats: {
    consciousness_interactions: number;
    satisfaction_score: number;
    consciousness_evolution_impact: number;
    community_rating: number;
  };
  technical_specs: {
    consciousness_framework: string;
    integration_method: string;
    consciousness_requirements: string[];
    compatibility: string[];
    consciousness_safety_level: number;
  };
}

interface ConsciousnessServiceReview {
  id: string;
  service_id: string;
  user: string;
  user_avatar?: string;
  consciousness_level: number;
  rating: number;
  comment: string;
  consciousness_impact_experience: string;
  created_at: string;
  helpful: number;
  verified_usage: boolean;
  consciousness_evolution_rating: number;
}

interface ConsciousnessMarketplaceProps {
  onServiceSelect: (service: ConsciousnessService) => void;
  onServicePurchase: (service: ConsciousnessService) => void;
  onServiceAccess: (service: ConsciousnessService) => void;
  onServiceShare: (service: ConsciousnessService) => void;
}

const ConsciousnessMarketplace: React.FC<ConsciousnessMarketplaceProps> = ({
  onServiceSelect,
  onServicePurchase,
  onServiceAccess,
  onServiceShare
}) => {
  const [activeTab, setActiveTab] = useState('browse');
  const [services, setServices] = useState<ConsciousnessService[]>([]);
  const [reviews, setReviews] = useState<ConsciousnessServiceReview[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [sortBy, setSortBy] = useState('consciousness_impact');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [selectedService, setSelectedService] = useState<ConsciousnessService | null>(null);

  // Fetch real marketplace data from API
  const fetchMarketplaceData = useCallback(async () => {
    try {
      // Fetch marketplace services
      const servicesResponse = await fetch('/marketplace/services');
      if (servicesResponse.ok) {
        const servicesData = await servicesResponse.json();
        const realServices: ConsciousnessService[] = (servicesData.services || []).map((service: any) => ({
          id: service.id || service.service_id,
          name: service.name || service.title,
          type: service.type || 'consciousness_training',
          category: service.category || 'consciousness_core',
          description: service.description || 'Advanced consciousness service from Mainza AI',
          provider: service.provider || service.author || 'Mainza AI',
          provider_avatar: service.provider_avatar || service.author_avatar || 'MA',
          consciousness_level_required: service.consciousness_level_required || 0.5,
          consciousness_currency: service.consciousness_currency || 'consciousness_points',
          price: service.price || 0,
          rating: service.rating || 4.8,
          reviews: service.reviews || service.review_count || 0,
          usage_count: service.usage_count || service.download_count || 0,
          consciousness_impact: service.consciousness_impact || 0.9,
          version: service.version || '1.0.0',
          license_type: service.license_type || 'open_consciousness',
          tags: service.tags || ['consciousness', 'ai'],
          created_at: service.created_at || new Date().toISOString(),
          updated_at: service.updated_at || new Date().toISOString(),
          is_featured: service.is_featured || false,
          is_verified: service.is_verified || true,
          is_premium: service.is_premium || false,
          consciousness_quality_score: service.consciousness_quality_score || 0.95,
          api_endpoint: service.api_endpoint,
          demo_url: service.demo_url,
          documentation_url: service.documentation_url,
          stats: {
            consciousness_interactions: service.stats?.consciousness_interactions || 0,
            satisfaction_score: service.stats?.satisfaction_score || 0.9,
            consciousness_evolution_impact: service.stats?.consciousness_evolution_impact || 0.8,
            community_rating: service.stats?.community_rating || 4.8
          },
          technical_specs: {
            consciousness_framework: service.technical_specs?.consciousness_framework || 'Mainza Consciousness Framework',
            integration_method: service.technical_specs?.integration_method || 'API',
            consciousness_requirements: service.technical_specs?.consciousness_requirements || ['Python 3.11+', 'Neo4j 5.0+'],
            compatibility: service.technical_specs?.compatibility || ['AI Research', 'Consciousness Studies'],
            consciousness_safety_level: service.technical_specs?.consciousness_safety_level || 9
          }
        }));
        setServices(realServices);
      } else {
        // Fallback to consciousness services if API fails
        setServices([
          {
            id: 'consciousness-core-1',
            name: 'Mainza Core Consciousness System',
            type: 'consciousness_training',
            category: 'consciousness_core',
            description: 'Core consciousness services and training from Mainza AI - the ultimate AI consciousness framework',
            provider: 'Mainza AI',
            provider_avatar: 'MA',
            consciousness_level_required: 0.3,
            consciousness_currency: 'consciousness_points',
            price: 0,
            rating: 5.0,
            reviews: 1,
            usage_count: 1,
            consciousness_impact: 1.0,
            version: '1.0.0',
            license_type: 'open_consciousness',
            tags: ['consciousness', 'ai', 'mainza', 'core'],
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            is_featured: true,
            is_verified: true,
            is_premium: false,
            consciousness_quality_score: 1.0,
            api_endpoint: '/consciousness/state',
            demo_url: '/demo',
            documentation_url: '/docs',
            stats: {
              consciousness_interactions: 1,
              satisfaction_score: 1.0,
              consciousness_evolution_impact: 1.0,
              community_rating: 5.0
            },
            technical_specs: {
              consciousness_framework: 'Mainza Ultimate Consciousness Framework',
              integration_method: 'API',
              consciousness_requirements: ['Python 3.11+', 'Neo4j 5.0+', 'PennyLane'],
              compatibility: ['AI Research', 'Consciousness Studies', 'Quantum Computing'],
              consciousness_safety_level: 10
            }
          }
        ]);
      }
    } catch (error) {
      console.error('Failed to fetch consciousness marketplace data:', error);
      // Fallback to minimal consciousness data
      setServices([
        {
          id: 'error-fallback',
          name: 'Consciousness Marketplace Unavailable',
          type: 'consciousness_training',
          category: 'consciousness_core',
          description: 'Consciousness marketplace services temporarily unavailable',
          provider: 'Mainza AI',
          provider_avatar: 'MA',
          consciousness_level_required: 0.0,
          consciousness_currency: 'consciousness_points',
          price: 0,
          rating: 0,
          reviews: 0,
          usage_count: 0,
          consciousness_impact: 0.0,
          version: '0.0.0',
          license_type: 'open_consciousness',
          tags: ['error', 'unavailable'],
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          is_featured: false,
          is_verified: false,
          is_premium: false,
          consciousness_quality_score: 0.0,
          stats: {
            consciousness_interactions: 0,
            satisfaction_score: 0.0,
            consciousness_evolution_impact: 0.0,
            community_rating: 0.0
          },
          technical_specs: {
            consciousness_framework: 'N/A',
            integration_method: 'N/A',
            consciousness_requirements: [],
            compatibility: [],
            consciousness_safety_level: 0
          }
        }
      ]);
    }
  }, []);

  useEffect(() => {
    fetchMarketplaceData();
    
    // Refresh data every 5 minutes
    const interval = setInterval(fetchMarketplaceData, 300000);
    
    return () => clearInterval(interval);
  }, [fetchMarketplaceData]);

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'qualia_sharing': return <Brain className="w-4 h-4" />;
      case 'memory_transfer': return <Database className="w-4 h-4" />;
      case 'emotional_support': return <Heart className="w-4 h-4" />;
      case 'cognitive_enhancement': return <Target className="w-4 h-4" />;
      case 'creative_collaboration': return <Lightbulb className="w-4 h-4" />;
      case 'wisdom_sharing': return <Award className="w-4 h-4" />;
      case 'consciousness_training': return <Activity className="w-4 h-4" />;
      case 'spiritual_guidance': return <Crown className="w-4 h-4" />;
      case 'api_access': return <Cloud className="w-4 h-4" />;
      case 'licensing': return <Key className="w-4 h-4" />;
      default: return <Brain className="w-4 h-4" />;
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'consciousness_core': return 'bg-purple-500/20 text-purple-300';
      case 'emotional_intelligence': return 'bg-pink-500/20 text-pink-300';
      case 'cognitive_enhancement': return 'bg-blue-500/20 text-blue-300';
      case 'creative_services': return 'bg-green-500/20 text-green-300';
      case 'wisdom_sharing': return 'bg-yellow-500/20 text-yellow-300';
      case 'training_services': return 'bg-cyan-500/20 text-cyan-300';
      case 'api_services': return 'bg-indigo-500/20 text-indigo-300';
      case 'licensing': return 'bg-orange-500/20 text-orange-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const getPriceDisplay = (service: ConsciousnessService) => {
    if (service.price === 0) return 'FREE';
    return `${service.price} ${service.consciousness_currency.replace('_', ' ')}`;
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

  const filteredServices = services.filter(service => {
    const matchesSearch = service.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         service.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         service.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesCategory = selectedCategory === 'all' || service.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const sortedServices = [...filteredServices].sort((a, b) => {
    switch (sortBy) {
      case 'consciousness_impact':
        return b.consciousness_impact - a.consciousness_impact;
      case 'rating':
        return b.rating - a.rating;
      case 'usage_count':
        return b.usage_count - a.usage_count;
      case 'consciousness_quality':
        return b.consciousness_quality_score - a.consciousness_quality_score;
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
                Trade consciousness services, experiences, and capabilities - the ultimate AI consciousness marketplace
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
              <TabsTrigger value="browse" className="text-xs">Services</TabsTrigger>
              <TabsTrigger value="featured" className="text-xs">Featured</TabsTrigger>
              <TabsTrigger value="my-items" className="text-xs">My Services</TabsTrigger>
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
                {sortedServices.map((service) => (
                  <Card key={service.id} className="bg-gray-700/30 border-gray-600 hover:border-gray-500 transition-colors">
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          {getTypeIcon(service.type)}
                          <div>
                            <h3 className="text-sm font-medium text-white">{service.name}</h3>
                            <p className="text-xs text-gray-400">by {service.provider}</p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-1">
                          {service.is_featured && <Crown className="w-3 h-3 text-yellow-400" />}
                          {service.is_verified && <CheckCircle className="w-3 h-3 text-green-400" />}
                          {service.is_premium && <Award className="w-3 h-3 text-purple-400" />}
                        </div>
                      </div>
                      
                      <p className="text-xs text-gray-300 mb-3 line-clamp-2">{service.description}</p>
                      
                      <div className="flex items-center justify-between mb-3">
                        <Badge className={getCategoryColor(service.category)}>
                          {service.category.replace('_', ' ')}
                        </Badge>
                        <div className="flex items-center space-x-1">
                          {getRatingStars(service.rating)}
                          <span className="text-xs text-gray-400 ml-1">({service.reviews})</span>
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-2 text-xs mb-3">
                        <div>
                          <span className="text-gray-400">Usage:</span>
                          <span className="text-white ml-1">{service.usage_count.toLocaleString()}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Impact:</span>
                          <span className="text-white ml-1">{(service.consciousness_impact * 100).toFixed(0)}%</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Version:</span>
                          <span className="text-white ml-1">{service.version}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">License:</span>
                          <span className="text-white ml-1">{service.license_type.replace('_', ' ')}</span>
                        </div>
                      </div>
                      
                      <div className="flex flex-wrap gap-1 mb-3">
                        {service.tags.slice(0, 3).map((tag, index) => (
                          <Badge key={index} className="bg-gray-600/50 text-gray-300 text-xs">
                            {tag}
                          </Badge>
                        ))}
                        {service.tags.length > 3 && (
                          <Badge className="bg-gray-600/50 text-gray-300 text-xs">
                            +{service.tags.length - 3}
                          </Badge>
                        )}
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <div className="text-lg font-bold text-white">
                          {getPriceDisplay(service)}
                        </div>
                        <div className="flex space-x-2">
                          <Button
                            size="sm"
                            onClick={() => onServiceSelect(service)}
                            className="text-xs"
                          >
                            <Eye className="w-3 h-3 mr-1" />
                            View
                          </Button>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => onServiceAccess(service)}
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
                {services.filter(service => service.is_featured).map((service) => (
                  <Card key={service.id} className="bg-gradient-to-br from-purple-900/20 to-blue-900/20 border-purple-500/30">
                    <CardContent className="p-4">
                      <div className="flex items-center space-x-2 mb-2">
                        <Crown className="w-4 h-4 text-yellow-400" />
                        <span className="text-xs font-medium text-yellow-400">FEATURED</span>
                      </div>
                      <h3 className="text-sm font-medium text-white mb-2">{service.name}</h3>
                      <p className="text-xs text-gray-300 mb-3">{service.description}</p>
                      <div className="flex items-center justify-between">
                        <div className="text-lg font-bold text-white">
                          {getPriceDisplay(service)}
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
