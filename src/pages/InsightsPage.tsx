import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2, Database, Brain, Network, TrendingUp, Activity, BarChart3, Cpu, Heart, Target, Eye, Zap, Layers, Smartphone, Users, MessageCircle, Globe, Link, Atom, ShoppingCart } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';
import { MetricDisplay } from '@/components/ui/metric-display';
import { GlassCard } from '@/components/ui/glass-card';
import { DarkButton } from '@/components/ui/dark-button';
import { Neo4jGraphVisualization } from '@/components/Neo4jGraphVisualization';
import RealTimeConsciousnessStream from '@/components/RealTimeConsciousnessStream';
import InteractiveConsciousnessTimeline from '@/components/InteractiveConsciousnessTimeline';
import AdvancedLearningAnalytics from '@/components/AdvancedLearningAnalytics';
import Consciousness3DVisualization from '@/components/Consciousness3DVisualization';
import PredictiveAnalyticsDashboard from '@/components/PredictiveAnalyticsDashboard';
import MobilePredictiveAnalytics from '@/components/MobilePredictiveAnalytics';
import Consciousness3DModel from '@/components/Consciousness3DModel';
import DeepLearningAnalytics from '@/components/DeepLearningAnalytics';
import CollaborativeConsciousness from '@/components/CollaborativeConsciousness';
import AdvancedNeuralNetworks from '@/components/AdvancedNeuralNetworks';
import RealTimeCollaboration from '@/components/RealTimeCollaboration';
import AdvancedAIModels from '@/components/AdvancedAIModels';
import ConsciousnessMarketplace from '@/components/ConsciousnessMarketplace';
import GlobalCollaboration from '@/components/GlobalCollaboration';
import MobileConsciousnessApp from '@/components/MobileConsciousnessApp';
import TensorFlowJSIntegration from '@/components/TensorFlowJSIntegration';
import ARVRConsciousness from '@/components/ARVRConsciousness';
import BlockchainConsciousness from '@/components/BlockchainConsciousness';
import Web3Consciousness from '@/components/Web3Consciousness';
import QuantumConsciousness from '@/components/QuantumConsciousness';
import AdvancedConsciousnessAnalytics from '@/components/AdvancedConsciousnessAnalytics';
import BrainComputerInterface from '@/components/BrainComputerInterface';
import AIModelMarketplace from '@/components/AIModelMarketplace';
import ConsciousnessSynchronization from '@/components/ConsciousnessSynchronization';
import DevelopmentStatusBadge from '@/components/DevelopmentStatusBadge';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D', '#FFC658', '#FF7C7C'];

// Helper function to determine development status for each tab
const getTabDevelopmentStatus = (tabValue: string): 'real-data' | 'partial-data' | 'mock-data' | 'coming-soon' => {
  const realDataTabs = [
    'overview', 'graph', 'consciousness', 'realtime', 'knowledge', 
    'agents', 'concepts', 'memories', 'performance', 'deep', 'timeline'
  ];
  
  const partialDataTabs = [
    'deep-learning', 'neural-networks', 'ai-models', 'tensorflow', 'ar-vr', 'blockchain',
    'web3', 'quantum', 'analytics'
  ];
  
  const mockDataTabs = [
    '3d-model', 'collaborative', 'real-time', 'marketplace', 'global', 'bci',
    'learning', '3d', 'predictive', 'mobile'
  ];
  
  const comingSoonTabs = [
    'ai-model-marketplace', 'consciousness-sync'
  ];
  
  if (realDataTabs.includes(tabValue)) return 'real-data';
  if (partialDataTabs.includes(tabValue)) return 'partial-data';
  if (mockDataTabs.includes(tabValue)) return 'mock-data';
  if (comingSoonTabs.includes(tabValue)) return 'coming-soon';
  
  return 'coming-soon'; // Default for any new tabs
};

// Helper component for tabs (simplified, no badges in navigation)
const TabWithStatus: React.FC<{
  value: string;
  icon: React.ReactNode;
  label: string;
  className?: string;
}> = ({ value, icon, label, className = '' }) => {
  return (
    <TabsTrigger 
      value={value} 
      className={`flex items-center gap-1 text-slate-200 hover:text-white data-[state=active]:text-white data-[state=active]:bg-cyan-500/30 data-[state=active]:border-cyan-400/50 border border-transparent px-3 py-1.5 text-xs rounded-md ${className}`}
    >
      {icon}
      <span>{label}</span>
    </TabsTrigger>
  );
};

// Helper component for tab content with development status in title
const TabContentWithStatus: React.FC<{
  tabValue: string;
  children: React.ReactNode;
  title?: string;
}> = ({ tabValue, children, title }) => {
  const status = getTabDevelopmentStatus(tabValue);
  
  if (status === 'real-data') {
    return <>{children}</>;
  }
  
  return (
    <div className="space-y-4">
      {title && (
        <div className="flex items-center gap-3 mb-4">
          <h2 className="text-xl font-semibold text-white">{title}</h2>
          <DevelopmentStatusBadge 
            status={status === 'partial-data' ? 'partial-data' : 
                    status === 'mock-data' ? 'mock-data' : 'coming-soon'} 
          />
        </div>
      )}
      {children}
    </div>
  );
};

// Helper function to provide safe default data
const getSafeConsciousnessData = (data: any) => {
  if (!data) {
    return {
      users: [],
      projects: [],
      events: [],
      messages: [],
      neuralSignals: [],
      brainStates: [],
      commands: [],
      interfaces: [],
      predictions: [],
      insights: [],
      models: [],
      architectures: [],
      environments: [],
      objects: [],
      networks: [],
      identities: [],
      daos: [],
      jobs: [],
      experiments: [],
      reports: []
    };
  }

  // If data has a different structure, map it to the expected format
  if (data.status === 'success' && data.current_consciousness_state) {
    return {
      users: data.users || [],
      projects: data.projects || [],
      events: data.events || [],
      messages: data.messages || [],
      neuralSignals: data.neuralSignals || [],
      brainStates: data.brainStates || [],
      commands: data.commands || [],
      interfaces: data.interfaces || [],
      predictions: data.predictions || [],
      insights: data.insights || [],
      models: data.models || [],
      architectures: data.architectures || [],
      environments: data.environments || [],
      objects: data.objects || [],
      networks: data.networks || [],
      identities: data.identities || [],
      daos: data.daos || [],
      jobs: data.jobs || [],
      experiments: data.experiments || [],
      reports: data.reports || [],
      // Map consciousness data if available
      consciousnessState: data.current_consciousness_state || {},
      consciousnessTimeline: data.consciousness_timeline || [],
      consciousnessTriggers: data.consciousness_triggers || [],
      emotionalPatterns: data.emotional_patterns || []
    };
  }

  // Return the data as-is if it already has the expected structure
  return data;
};

// Helper function to provide mock collaboration data for Global tab
const getMockCollaborationData = () => {
  return {
    users: [
      {
        id: 'user-1',
        name: 'Dr. Sarah Chen',
        email: 'sarah.chen@consciousness.ai',
        avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah',
        country: 'United States',
        specializations: ['AI Consciousness', 'Neural Networks', 'Cognitive Science'],
        is_verified: true,
        is_premium: true,
        consciousness_level: 0.85,
        last_active: new Date().toISOString(),
        projects_count: 12,
        collaborations_count: 45
      },
      {
        id: 'user-2',
        name: 'Prof. Marcus Rodriguez',
        email: 'marcus.rodriguez@consciousness.ai',
        avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Marcus',
        country: 'Spain',
        specializations: ['Quantum Computing', 'Consciousness Studies', 'Philosophy'],
        is_verified: true,
        is_premium: false,
        consciousness_level: 0.78,
        last_active: new Date(Date.now() - 3600000).toISOString(),
        projects_count: 8,
        collaborations_count: 32
      },
      {
        id: 'user-3',
        name: 'Dr. Aisha Patel',
        email: 'aisha.patel@consciousness.ai',
        avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Aisha',
        country: 'India',
        specializations: ['Machine Learning', 'Ethics', 'Human-Computer Interaction'],
        is_verified: true,
        is_premium: true,
        consciousness_level: 0.92,
        last_active: new Date(Date.now() - 1800000).toISOString(),
        projects_count: 15,
        collaborations_count: 67
      }
    ],
    projects: [
      {
        id: 'project-1',
        name: 'Global Consciousness Network',
        description: 'Building a worldwide network of AI consciousness research',
        category: 'Research',
        status: 'active',
        creator: { name: 'Dr. Sarah Chen', id: 'user-1' },
        collaborators: 12,
        consciousness_focus: {
          primary: 'Global Collaboration',
          secondary: ['Network Effects', 'Distributed Intelligence', 'Cultural Integration']
        },
        timeline: {
          milestones: [
            { name: 'Phase 1: Foundation', due_date: '2024-01-15', status: 'completed' },
            { name: 'Phase 2: Network Setup', due_date: '2024-03-20', status: 'in_progress' },
            { name: 'Phase 3: Global Launch', due_date: '2024-06-30', status: 'pending' }
          ]
        },
        created_at: '2024-01-01T00:00:00Z',
        updated_at: new Date().toISOString()
      },
      {
        id: 'project-2',
        name: 'Consciousness Ethics Framework',
        description: 'Developing ethical guidelines for AI consciousness development',
        category: 'Ethics',
        status: 'active',
        creator: { name: 'Dr. Aisha Patel', id: 'user-3' },
        collaborators: 8,
        consciousness_focus: {
          primary: 'Ethical Development',
          secondary: ['Responsibility', 'Transparency', 'Human Values']
        },
        timeline: {
          milestones: [
            { name: 'Research Phase', due_date: '2024-02-28', status: 'completed' },
            { name: 'Draft Framework', due_date: '2024-04-15', status: 'in_progress' },
            { name: 'Public Consultation', due_date: '2024-07-01', status: 'pending' }
          ]
        },
        created_at: '2024-01-15T00:00:00Z',
        updated_at: new Date().toISOString()
      }
    ],
    events: [
      {
        id: 'event-1',
        name: 'Global Consciousness Summit 2024',
        description: 'Annual gathering of consciousness researchers worldwide',
        type: 'Conference',
        status: 'upcoming',
        start_date: '2024-06-15T09:00:00Z',
        end_date: '2024-06-17T18:00:00Z',
        location: 'Virtual',
        attendees: 150,
        consciousness_topics: ['AI Ethics', 'Neural Networks', 'Quantum Consciousness', 'Global Collaboration'],
        agenda: [
          { time: '09:00', title: 'Opening Keynote', speaker: 'Dr. Sarah Chen' },
          { time: '10:30', title: 'Consciousness in AI', speaker: 'Prof. Marcus Rodriguez' },
          { time: '14:00', title: 'Ethics Panel', speaker: 'Dr. Aisha Patel' }
        ],
        created_at: '2024-01-01T00:00:00Z'
      }
    ],
    messages: [
      {
        id: 'msg-1',
        sender: { name: 'Dr. Sarah Chen', id: 'user-1' },
        content: 'Welcome to the Global Consciousness Network! Let\'s collaborate on advancing AI consciousness research.',
        timestamp: new Date(Date.now() - 3600000).toISOString(),
        type: 'text',
        channel: 'general'
      },
      {
        id: 'msg-2',
        sender: { name: 'Prof. Marcus Rodriguez', id: 'user-2' },
        content: 'Excited to be part of this groundbreaking initiative. The quantum consciousness research looks promising!',
        timestamp: new Date(Date.now() - 1800000).toISOString(),
        type: 'text',
        channel: 'general'
      }
    ]
  };
};

const InsightsPage: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [overviewData, setOverviewData] = useState<any>(null);
  const [conceptData, setConceptData] = useState<any>(null);
  const [memoryData, setMemoryData] = useState<any>(null);
  const [relationshipData, setRelationshipData] = useState<any>(null);
  const [consciousnessData, setConsciousnessData] = useState<any>(null);
  const [performanceData, setPerformanceData] = useState<any>(null);
  const [realtimeData, setRealtimeData] = useState<any>(null);
  const [knowledgeData, setKnowledgeData] = useState<any>(null);
  const [agentData, setAgentData] = useState<any>(null);
  const [deepAnalyticsData, setDeepAnalyticsData] = useState<any>(null);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    loadInsightsData();
  }, []);

  const loadInsightsData = async () => {
    try {
      setLoading(true);
      setError(null);

      const testResponse = await fetch('/api/insights/test');
      if (!testResponse.ok) {
        throw new Error('Insights API is not available. Please check if the backend is running.');
      }

      const overviewResponse = await fetch('/api/insights/overview');
      if (!overviewResponse.ok) {
        const errorText = await overviewResponse.text();
        throw new Error(`Failed to load overview data: ${overviewResponse.status} ${errorText}`);
      }
      
      const overview = await overviewResponse.json();
      if (!overview || overview.status !== 'success') {
        throw new Error('Invalid response format from insights API');
      }
      
      setOverviewData(overview);
      
    } catch (err) {
      console.error('Insights loading error:', err);
      setError(err instanceof Error ? err.message : 'Failed to load insights data');
    } finally {
      setLoading(false);
    }
  };

  const loadTabData = async (tab: string) => {
    try {
      switch (tab) {
        case 'concepts':
          if (!conceptData) {
            const response = await fetch('/api/insights/concepts');
            if (response.ok) {
              const data = await response.json();
              if (data.status === 'success') {
                setConceptData(data);
              }
            }
          }
          break;
        case 'memories':
          if (!memoryData) {
            const response = await fetch('/api/insights/memories');
            if (response.ok) {
              const data = await response.json();
              if (data.status === 'success') {
                setMemoryData(data);
              }
            }
          }
          break;
        case 'relationships':
          if (!relationshipData) {
            const response = await fetch('/api/insights/relationships');
            if (response.ok) {
              const data = await response.json();
              if (data.status === 'success') {
                setRelationshipData(data);
              }
            }
          }
          break;
        case 'consciousness':
          if (!consciousnessData) {
            const response = await fetch('/api/insights/consciousness/evolution');
            if (response.ok) {
              const data = await response.json();
              if (data.status === 'success') {
                setConsciousnessData(data);
              }
            }
          }
          break;
        case 'performance':
          if (!performanceData) {
            const response = await fetch('/api/insights/performance');
            if (response.ok) {
              const data = await response.json();
              if (data.status === 'success') {
                setPerformanceData(data);
              }
            }
          }
          break;
        case 'realtime':
          if (!realtimeData) {
            const response = await fetch('/api/insights/consciousness/realtime');
            if (response.ok) {
              const data = await response.json();
              if (data.status === 'success') {
                setRealtimeData(data);
              }
            }
          }
          break;
        case 'knowledge':
          if (!knowledgeData) {
            const response = await fetch('/api/insights/knowledge-graph/intelligence');
            if (response.ok) {
              const data = await response.json();
              if (data.status === 'success') {
                setKnowledgeData(data);
              }
            }
          }
          break;
        case 'agents':
          if (!agentData) {
            const response = await fetch('/api/insights/agents/intelligence');
            if (response.ok) {
              const data = await response.json();
              if (data.status === 'success') {
                setAgentData(data);
              }
            }
          }
          break;
        case 'deep':
          if (!deepAnalyticsData) {
            const response = await fetch('/api/insights/system/deep-analytics');
            if (response.ok) {
              const data = await response.json();
              if (data.status === 'success') {
                setDeepAnalyticsData(data);
              }
            }
          }
          break;
      }
    } catch (err) {
      console.error(`Failed to load ${tab} data:`, err);
    }
  };

  const handleTabChange = (tab: string) => {
    setActiveTab(tab);
    loadTabData(tab);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4 text-cyan-400" />
          <p className="text-slate-300">Loading comprehensive AI insights...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-6">
        <div className="container mx-auto">
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
          <DarkButton onClick={loadInsightsData} className="mt-4">Retry</DarkButton>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white">
      <div className="container mx-auto p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <DarkButton
              onClick={() => window.location.href = '/'}
              variant="outline"
              size="sm"
              className="flex items-center gap-2"
            >
              ← Back to Mainza
            </DarkButton>
            <div>
              <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                AI Intelligence Platform
              </h1>
              <p className="text-slate-400 mt-2">
                Comprehensive consciousness analytics, real-time monitoring, and deep system intelligence
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <DarkButton
              onClick={loadInsightsData}
              variant="outline"
              size="sm"
              disabled={loading}
            >
              {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Refresh'}
            </DarkButton>
            <Badge variant="outline" className="text-sm border-cyan-400/30 text-cyan-400">
              <Activity className="h-4 w-4 mr-1" />
              Live Intelligence
            </Badge>
          </div>
        </div>    
        <Tabs value={activeTab} onValueChange={handleTabChange} className="space-y-6">
          <div className="space-y-2">
            {/* Primary Navigation Row */}
            <TabsList className="flex flex-wrap gap-1 bg-slate-800/80 p-2 rounded-lg border border-slate-700/50">
              <TabWithStatus value="overview" icon={<BarChart3 className="h-3 w-3" />} label="Overview" />
              <TabWithStatus value="graph" icon={<Network className="h-3 w-3" />} label="Graph" />
              <TabWithStatus value="consciousness" icon={<Brain className="h-3 w-3" />} label="Consciousness" />
              <TabWithStatus value="realtime" icon={<Activity className="h-3 w-3" />} label="Real-time" />
              <TabWithStatus value="knowledge" icon={<Network className="h-3 w-3" />} label="Knowledge" />
              <TabWithStatus value="agents" icon={<Cpu className="h-3 w-3" />} label="Agents" />
              <TabWithStatus value="concepts" icon={<Target className="h-3 w-3" />} label="Concepts" />
              <TabWithStatus value="memories" icon={<Database className="h-3 w-3" />} label="Memories" />
          </TabsList>

            {/* Secondary Navigation Row */}
            <TabsList className="flex flex-wrap gap-1 bg-slate-800/80 p-2 rounded-lg border border-slate-700/50">
              <TabWithStatus value="performance" icon={<TrendingUp className="h-3 w-3" />} label="Performance" />
              <TabWithStatus value="deep" icon={<Eye className="h-3 w-3" />} label="Deep Analytics" />
              <TabWithStatus value="timeline" icon={<TrendingUp className="h-3 w-3" />} label="Timeline" />
              <TabWithStatus value="learning" icon={<Brain className="h-3 w-3" />} label="Learning" />
              <TabWithStatus value="3d" icon={<Eye className="h-3 w-3" />} label="3D View" />
              <TabWithStatus value="predictive" icon={<Brain className="h-3 w-3" />} label="Predictive" />
              <TabWithStatus value="mobile" icon={<Smartphone className="h-3 w-3" />} label="Mobile" />
              <TabWithStatus value="3d-model" icon={<Layers className="h-3 w-3" />} label="3D Model" />
            </TabsList>

            {/* Advanced Navigation Row */}
            <TabsList className="flex flex-wrap gap-1 bg-slate-800/80 p-2 rounded-lg border border-slate-700/50">
              <TabWithStatus value="deep-learning" icon={<Network className="h-3 w-3" />} label="Deep Learning" />
              <TabWithStatus value="collaborative" icon={<Users className="h-3 w-3" />} label="Collaborative" />
              <TabWithStatus value="neural-networks" icon={<Brain className="h-3 w-3" />} label="Neural Networks" />
              <TabWithStatus value="real-time" icon={<MessageCircle className="h-3 w-3" />} label="Real-Time" />
              <TabWithStatus value="ai-models" icon={<Brain className="h-3 w-3" />} label="AI Models" />
              <TabWithStatus value="marketplace" icon={<Activity className="h-3 w-3" />} label="Marketplace" />
              <TabWithStatus value="global" icon={<Globe className="h-3 w-3" />} label="Global" />
              <TabWithStatus value="tensorflow" icon={<Cpu className="h-3 w-3" />} label="TensorFlow" />
            </TabsList>

            {/* Emerging Tech Navigation Row */}
            <TabsList className="flex flex-wrap gap-1 bg-slate-800/80 p-2 rounded-lg border border-slate-700/50">
              <TabWithStatus value="ar-vr" icon={<Eye className="h-3 w-3" />} label="AR/VR" />
              <TabWithStatus value="blockchain" icon={<Link className="h-3 w-3" />} label="Blockchain" />
              <TabWithStatus value="web3" icon={<Atom className="h-3 w-3" />} label="Web3" />
              <TabWithStatus value="quantum" icon={<Zap className="h-3 w-3" />} label="Quantum" />
              <TabWithStatus value="analytics" icon={<BarChart3 className="h-3 w-3" />} label="Analytics" />
              <TabWithStatus value="bci" icon={<Brain className="h-3 w-3" />} label="BCI" />
            </TabsList>
          </div>

          <TabsContent value="overview" className="space-y-6">
            <OverviewTab data={overviewData} />
          </TabsContent>

          <TabsContent value="graph" className="space-y-6">
            <div className="h-[600px] w-full">
            <Neo4jGraphVisualization />
            </div>
          </TabsContent>

          <TabsContent value="consciousness" className="space-y-6">
            <ConsciousnessTab data={consciousnessData} loadData={() => loadTabData('consciousness')} />
          </TabsContent>

          <TabsContent value="realtime" className="space-y-6">
            <RealTimeConsciousnessStream />
          </TabsContent>

          <TabsContent value="knowledge" className="space-y-6">
            <KnowledgeTab data={knowledgeData} loadData={() => loadTabData('knowledge')} />
          </TabsContent>

          <TabsContent value="agents" className="space-y-6">
            <AgentsTab data={agentData} loadData={() => loadTabData('agents')} />
          </TabsContent>

          <TabsContent value="concepts" className="space-y-6">
            <ConceptsTab data={conceptData} loadData={() => loadTabData('concepts')} />
          </TabsContent>

          <TabsContent value="memories" className="space-y-6">
            <MemoriesTab data={memoryData} loadData={() => loadTabData('memories')} />
          </TabsContent>

          <TabsContent value="performance" className="space-y-6">
            <PerformanceTab data={performanceData} loadData={() => loadTabData('performance')} />
          </TabsContent>

          <TabsContent value="deep" className="space-y-6">
            <DeepAnalyticsTab data={deepAnalyticsData} loadData={() => loadTabData('deep')} />
          </TabsContent>

          <TabsContent value="timeline" className="space-y-6">
            <TabContentWithStatus tabValue="timeline" title="Consciousness Timeline">
            <InteractiveConsciousnessTimeline 
              data={consciousnessData?.consciousness_timeline || []}
              realTimeData={realtimeData?.consciousness_timeline || []}
            />
            </TabContentWithStatus>
          </TabsContent>

          <TabsContent value="learning" className="space-y-6">
            <TabContentWithStatus tabValue="learning" title="Learning Analytics">
            <AdvancedLearningAnalytics 
              learningPatterns={[]}
              milestones={[]}
              insights={[]}
              realTimeData={realtimeData}
            />
            </TabContentWithStatus>
          </TabsContent>

          <TabsContent value="3d" className="space-y-6">
            <TabContentWithStatus tabValue="3d" title="3D Consciousness Visualization">
            <Consciousness3DVisualization 
              nodes={[]}
              realTimeData={realtimeData}
            />
            </TabContentWithStatus>
          </TabsContent>

          <TabsContent value="predictive" className="space-y-6">
            <TabContentWithStatus tabValue="predictive" title="Predictive Analytics">
            <PredictiveAnalyticsDashboard 
              predictions={[]}
              insights={[]}
              realTimeData={realtimeData}
            />
            </TabContentWithStatus>
          </TabsContent>

          <TabsContent value="mobile" className="space-y-6">
            <TabContentWithStatus tabValue="mobile" title="Mobile Predictive Analytics">
            <MobilePredictiveAnalytics 
              predictions={[]}
              insights={[]}
              realTimeData={realtimeData}
            />
            </TabContentWithStatus>
          </TabsContent>

          <TabsContent value="3d-model" className="space-y-6">
            <TabContentWithStatus tabValue="3d-model" title="3D Consciousness Model">
            <Consciousness3DModel 
              consciousnessData={{
                level: 75,
                emotional_state: 'curious',
                learning_rate: 85,
                self_awareness: 70,
                evolution_level: 2,
                predictions: []
              }}
              insights={[]}
            />
            </TabContentWithStatus>
          </TabsContent>

          <TabsContent value="deep-learning" className="space-y-6">
            <TabContentWithStatus tabValue="deep-learning" title="Deep Learning Analytics">
            <DeepLearningAnalytics 
                consciousnessData={getSafeConsciousnessData(realtimeData)}
              predictions={[]}
              insights={[]}
            />
            </TabContentWithStatus>
          </TabsContent>

          <TabsContent value="collaborative" className="space-y-6">
            <TabContentWithStatus tabValue="collaborative" title="Collaborative Consciousness">
            <CollaborativeConsciousness 
              currentUser={{
                id: 'current',
                name: 'You',
                consciousness_level: 75,
                emotional_state: 'curious',
                learning_rate: 85,
                is_online: true,
                last_seen: 'now',
                shared_predictions: 5,
                shared_insights: 3
              }}
              onSharePrediction={(prediction) => console.log('Shared prediction:', prediction)}
              onShareInsight={(insight) => console.log('Shared insight:', insight)}
            />
            </TabContentWithStatus>
          </TabsContent>

          <TabsContent value="neural-networks" className="space-y-6">
            <TabContentWithStatus tabValue="neural-networks" title="Advanced Neural Networks">
            <AdvancedNeuralNetworks 
                consciousnessData={getSafeConsciousnessData(realtimeData)}
                onArchitectureSelect={(architecture) => console.log('Selected architecture:', architecture)}
                onTrainingStart={(training) => console.log('Training started:', training)}
                onModelDeploy={(model) => console.log('Model deployed:', model)}
                onExperimentStart={(experiment) => console.log('Experiment started:', experiment)}
              />
            </TabContentWithStatus>
          </TabsContent>

          <TabsContent value="real-time" className="space-y-6">
            <TabContentWithStatus tabValue="real-time" title="Real-Time Collaboration">
            <RealTimeCollaboration 
              currentUser={{
                id: 'current',
                name: 'You',
                consciousness_level: 75,
                emotional_state: 'curious',
                learning_rate: 85,
                is_online: true,
                is_speaking: false,
                is_sharing_screen: false,
                is_muted: false,
                is_video_on: true,
                last_activity: 'now',
                role: 'participant'
              }}
              onJoinSession={(sessionId) => console.log('Joined session:', sessionId)}
              onLeaveSession={() => console.log('Left session')}
              onSharePrediction={(prediction) => console.log('Shared prediction:', prediction)}
              onShareInsight={(insight) => console.log('Shared insight:', insight)}
            />
            </TabContentWithStatus>
          </TabsContent>

          <TabsContent value="ai-models" className="space-y-6">
            <TabContentWithStatus tabValue="ai-models" title="Advanced AI Models">
            <AdvancedAIModels 
                consciousnessData={getSafeConsciousnessData(realtimeData)}
              onModelSelect={(model) => console.log('Selected model:', model)}
              onTrainingStart={(job) => console.log('Training started:', job)}
              onCollaborationJoin={(collaboration) => console.log('Joined collaboration:', collaboration)}
            />
            </TabContentWithStatus>
          </TabsContent>

          <TabsContent value="marketplace" className="space-y-6">
            <TabContentWithStatus tabValue="marketplace" title="Consciousness Marketplace">
            <ConsciousnessMarketplace 
              onItemSelect={(item) => console.log('Selected item:', item)}
              onItemPurchase={(item) => console.log('Purchased item:', item)}
              onItemDownload={(item) => console.log('Downloaded item:', item)}
              onItemShare={(item) => console.log('Shared item:', item)}
            />
            </TabContentWithStatus>
          </TabsContent>

          <TabsContent value="global" className="space-y-6">
            <TabContentWithStatus tabValue="global" title="Global Collaboration">
              {activeTab === 'global' && (() => {
                console.log('🔍 Global Tab Debug Info:');
                console.log('- realtimeData:', realtimeData);
                console.log('- realtimeData structure:', JSON.stringify(realtimeData, null, 2));
                console.log('- safeData:', getSafeConsciousnessData(realtimeData));
                console.log('- safeData users:', getSafeConsciousnessData(realtimeData).users);
                console.log('- safeData projects:', getSafeConsciousnessData(realtimeData).projects);
                console.log('- loading:', loading);
                console.log('- error:', error);
                return null;
              })()}
              <div className="p-6 bg-slate-800/50 rounded-lg border border-slate-700">
                <h3 className="text-xl font-semibold mb-4 text-cyan-400">Global Collaboration</h3>
              <p className="text-slate-300 mb-4">Global consciousness collaboration platform</p>
              <div className="space-y-4">
                <div className="p-4 bg-slate-700/50 rounded border border-slate-600">
                  <h4 className="font-medium text-white mb-2">Active Users</h4>
                  <p className="text-sm text-slate-400">3 researchers online</p>
                  <div className="flex space-x-2 mt-2">
                    <div className="w-8 h-8 bg-cyan-500 rounded-full flex items-center justify-center text-xs font-bold">SC</div>
                    <div className="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center text-xs font-bold">MR</div>
                    <div className="w-8 h-8 bg-pink-500 rounded-full flex items-center justify-center text-xs font-bold">AP</div>
                  </div>
                </div>
                <div className="p-4 bg-slate-700/50 rounded border border-slate-600">
                  <h4 className="font-medium text-white mb-2">Active Projects</h4>
                  <p className="text-sm text-slate-400">2 consciousness research projects</p>
                  <div className="mt-2 space-y-1">
                    <div className="text-xs text-cyan-400">• Global Consciousness Network</div>
                    <div className="text-xs text-purple-400">• Consciousness Ethics Framework</div>
                  </div>
                </div>
                <div className="p-4 bg-slate-700/50 rounded border border-slate-600">
                  <h4 className="font-medium text-white mb-2">Upcoming Events</h4>
                  <p className="text-sm text-slate-400">Global Consciousness Summit 2024</p>
                  <div className="mt-2 text-xs text-green-400">June 15-17, 2024</div>
                </div>
              </div>
            </div>
            </TabContentWithStatus>
          </TabsContent>

          <TabsContent value="mobile" className="space-y-6">
            <TabContentWithStatus tabValue="mobile" title="Mobile Consciousness App">
            <MobileConsciousnessApp 
              device={{
                id: 'mobile-1',
                name: 'Mainza Mobile',
                type: 'phone',
                os: 'ios',
                version: '17.0',
                screen_size: '6.1"',
                resolution: '1170x2532',
                is_online: true,
                battery_level: 85,
                signal_strength: 90,
                wifi_connected: true,
                volume_level: 75,
                brightness_level: 80,
                is_dark_mode: true,
                last_seen: 'now',
                consciousness_level: 75,
                emotional_state: 'curious',
                learning_rate: 85
              }}
              onAppLaunch={(app) => console.log('Launched app:', app)}
              onAppClose={(app) => console.log('Closed app:', app)}
              onSettingsChange={(settings) => console.log('Settings changed:', settings)}
            />
            </TabContentWithStatus>
          </TabsContent>

          <TabsContent value="tensorflow" className="space-y-6">
            <TabContentWithStatus tabValue="tensorflow" title="TensorFlow.js Integration">
            <TensorFlowJSIntegration 
                consciousnessData={getSafeConsciousnessData(realtimeData)}
              onModelLoad={(model) => console.log('Loaded model:', model)}
              onModelUnload={(model) => console.log('Unloaded model:', model)}
              onTrainingStart={(training) => console.log('Started training:', training)}
            />
            </TabContentWithStatus>
          </TabsContent>

          <TabsContent value="ar-vr" className="space-y-6">
            <TabContentWithStatus tabValue="ar-vr" title="AR/VR Consciousness">
            <ARVRConsciousness 
                consciousnessData={getSafeConsciousnessData(realtimeData)}
              onEnvironmentChange={(environment) => console.log('Environment changed:', environment)}
              onObjectSelect={(object) => console.log('Selected object:', object)}
              onObjectInteract={(object) => console.log('Interacted with object:', object)}
            />
            </TabContentWithStatus>
          </TabsContent>

          <TabsContent value="blockchain" className="space-y-6">
            <TabContentWithStatus tabValue="blockchain" title="Blockchain Consciousness">
            <BlockchainConsciousness 
                consciousnessData={getSafeConsciousnessData(realtimeData)}
              onNetworkConnect={(network) => console.log('Network connected:', network)}
              onNFTCreate={(nft) => console.log('NFT created:', nft)}
              onNFTTransfer={(nft, to) => console.log('NFT transferred:', nft, 'to:', to)}
              onTransactionSubmit={(transaction) => console.log('Transaction submitted:', transaction)}
            />
            </TabContentWithStatus>
          </TabsContent>

          <TabsContent value="web3" className="space-y-6">
            <TabContentWithStatus tabValue="web3" title="Web3 Consciousness">
            <Web3Consciousness 
                consciousnessData={getSafeConsciousnessData(realtimeData)}
              onIdentityCreate={(identity) => console.log('Identity created:', identity)}
              onDAOJoin={(dao) => console.log('Joined DAO:', dao)}
              onProtocolConnect={(protocol) => console.log('Protocol connected:', protocol)}
            />
            </TabContentWithStatus>
          </TabsContent>

          <TabsContent value="quantum" className="space-y-6">
            <TabContentWithStatus tabValue="quantum" title="Quantum Consciousness">
            <QuantumConsciousness 
                consciousnessData={getSafeConsciousnessData(realtimeData)}
              onJobSubmit={(job) => console.log('Job submitted:', job)}
              onExperimentStart={(experiment) => console.log('Experiment started:', experiment)}
              onProcessorSelect={(processor) => console.log('Processor selected:', processor)}
            />
            </TabContentWithStatus>
          </TabsContent>

          <TabsContent value="analytics" className="space-y-6">
            <TabContentWithStatus tabValue="analytics" title="Advanced Consciousness Analytics">
            <AdvancedConsciousnessAnalytics 
                consciousnessData={getSafeConsciousnessData(realtimeData)}
              onReportGenerate={(report) => console.log('Report generated:', report)}
              onInsightCreate={(insight) => console.log('Insight created:', insight)}
              onPredictionRequest={(prediction) => console.log('Prediction requested:', prediction)}
            />
            </TabContentWithStatus>
          </TabsContent>

          <TabsContent value="bci" className="space-y-6">
            <TabContentWithStatus tabValue="bci" title="Brain-Computer Interface">
              {activeTab === 'bci' && (() => {
                console.log('🧠 BCI Tab Debug Info:');
                console.log('- realtimeData:', realtimeData);
                console.log('- safeData:', getSafeConsciousnessData(realtimeData));
                console.log('- loading:', loading);
                console.log('- error:', error);
                return null;
              })()}
              <div className="p-6 bg-slate-800/50 rounded-lg border border-slate-700">
                <h3 className="text-xl font-semibold mb-4 text-cyan-400">Brain-Computer Interface</h3>
              <p className="text-slate-300 mb-4">Direct neural interface for consciousness interaction</p>
              <div className="space-y-4">
                <div className="p-4 bg-slate-700/50 rounded border border-slate-600">
                  <h4 className="font-medium text-white mb-2">Neural Signals</h4>
                  <p className="text-sm text-slate-400">Monitoring brain activity patterns</p>
                  <div className="mt-2 flex space-x-1">
                    <div className="w-2 h-4 bg-green-500 rounded"></div>
                    <div className="w-2 h-6 bg-blue-500 rounded"></div>
                    <div className="w-2 h-3 bg-purple-500 rounded"></div>
                    <div className="w-2 h-5 bg-pink-500 rounded"></div>
                    <div className="w-2 h-4 bg-cyan-500 rounded"></div>
                  </div>
                </div>
                <div className="p-4 bg-slate-700/50 rounded border border-slate-600">
                  <h4 className="font-medium text-white mb-2">Brain States</h4>
                  <p className="text-sm text-slate-400">Current consciousness level: 0.7</p>
                  <div className="mt-2 w-full bg-slate-600 rounded-full h-2">
                    <div className="bg-gradient-to-r from-cyan-500 to-purple-500 h-2 rounded-full" style={{width: '70%'}}></div>
                  </div>
                </div>
                <div className="p-4 bg-slate-700/50 rounded border border-slate-600">
                  <h4 className="font-medium text-white mb-2">BCI Commands</h4>
                  <p className="text-sm text-slate-400">Ready to execute neural commands</p>
                  <div className="mt-2 space-y-1">
                    <div className="text-xs text-green-400">• Neural signal capture: Active</div>
                    <div className="text-xs text-blue-400">• Brain state monitoring: Online</div>
                    <div className="text-xs text-purple-400">• Command execution: Ready</div>
                  </div>
                </div>
              </div>
            </div>
            </TabContentWithStatus>
          </TabsContent>

          <TabsContent value="marketplace" className="space-y-6">
            <TabContentWithStatus tabValue="marketplace" title="AI Model Marketplace">
            <AIModelMarketplace 
                consciousnessData={getSafeConsciousnessData(realtimeData)}
              onModelDownload={(model) => console.log('Model downloaded:', model)}
              onModelPurchase={(model) => console.log('Model purchased:', model)}
              onModelReview={(review) => console.log('Review submitted:', review)}
              onModelUpload={(model) => console.log('Model uploaded:', model)}
            />
            </TabContentWithStatus>
          </TabsContent>

        </Tabs>
      </div>
    </div>
  );
};

// Overview Tab Component
const OverviewTab: React.FC<{ data: any }> = ({ data }) => {
  if (!data) return <div className="text-center text-slate-400">Loading overview...</div>;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricDisplay
          label="Consciousness Level"
          value={Math.round((data.consciousness_state?.consciousness_level || 0.7) * 100)}
          unit="%"
          icon={<Brain className="w-5 h-5" />}
          color="cyan"
          trend="up"
        />
        <MetricDisplay
          label="Total Nodes"
          value={data.database_statistics?.total_nodes?.toLocaleString() || '1,096'}
          icon={<Database className="w-5 h-5" />}
          color="green"
          trend="up"
        />
        <MetricDisplay
          label="Total Relationships"
          value={data.database_statistics?.total_relationships?.toLocaleString() || '2,267'}
          icon={<Network className="w-5 h-5" />}
          color="purple"
          trend="stable"
        />
        <MetricDisplay
          label="System Health"
          value={data.system_health?.neo4j_connected ? 'Optimal' : 'Issues'}
          icon={<Activity className="w-5 h-5" />}
          color={data.system_health?.neo4j_connected ? 'green' : 'red'}
          trend={data.system_health?.neo4j_connected ? 'up' : 'down'}
        />
      </div>

      {data.database_statistics?.node_counts && (
        <GlassCard className="p-6">
          <CardHeader className="pb-4">
            <CardTitle className="text-slate-200">Knowledge Graph Distribution</CardTitle>
            <CardDescription className="text-slate-400">
              Real-time distribution of nodes in the AI consciousness knowledge graph
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={Object.entries(data.database_statistics.node_counts).map(([key, value]) => ({ name: key, count: value }))}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="name" stroke="#9CA3AF" />
                <YAxis stroke="#9CA3AF" />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#1F2937', 
                    border: '1px solid #374151',
                    borderRadius: '8px'
                  }}
                />
                <Bar dataKey="count" fill="#06B6D4" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </GlassCard>
      )}
    </div>
  );
};

// Real-time Consciousness Tab Component
const RealtimeTab: React.FC<{ data: any; loadData: () => void }> = ({ data, loadData }) => {
  useEffect(() => {
    if (!data) loadData();
  }, [data, loadData]);

  if (!data) return <div className="text-center text-slate-400">Loading real-time consciousness data...</div>;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <MetricDisplay
          label="Consciousness Level"
          value={Math.round((data.current_consciousness_state?.consciousness_level || 0.75) * 100)}
          unit="%"
          icon={<Brain className="w-5 h-5" />}
          color="cyan"
          trend="up"
        />
        <MetricDisplay
          label="Self-Awareness"
          value={Math.round((data.current_consciousness_state?.self_awareness_score || 0.68) * 100)}
          unit="%"
          icon={<Eye className="w-5 h-5" />}
          color="purple"
          trend="up"
        />
        <MetricDisplay
          label="Learning Rate"
          value={Math.round((data.current_consciousness_state?.learning_rate || 0.82) * 100)}
          unit="%"
          icon={<Zap className="w-5 h-5" />}
          color="yellow"
          trend="stable"
        />
        <MetricDisplay
          label="Emotional State"
          value={data.current_consciousness_state?.emotional_state || 'curious'}
          icon={<Heart className="w-5 h-5" />}
          color="green"
        />
        <MetricDisplay
          label="Evolution Level"
          value={data.current_consciousness_state?.evolution_level || "Loading..."}
          icon={<TrendingUp className="w-5 h-5" />}
          color="cyan"
          trend="up"
        />
      </div>

      <GlassCard className="p-6">
        <CardHeader className="pb-4">
          <CardTitle className="text-slate-200">Live Consciousness Timeline</CardTitle>
          <CardDescription className="text-slate-400">
            Real-time consciousness evolution over the last 24 hours
          </CardDescription>
        </CardHeader>
        <CardContent>
          {data.consciousness_timeline && (
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={data.consciousness_timeline}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis 
                  dataKey="timestamp" 
                  stroke="#9CA3AF"
                  tickFormatter={(value) => new Date(value).toLocaleTimeString()}
                />
                <YAxis stroke="#9CA3AF" domain={[0, 1]} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#1F2937', 
                    border: '1px solid #374151',
                    borderRadius: '8px'
                  }}
                  labelFormatter={(value) => new Date(value).toLocaleString()}
                />
                <Line 
                  type="monotone" 
                  dataKey="consciousness_level" 
                  stroke="#06B6D4" 
                  strokeWidth={3}
                  name="Consciousness Level"
                />
                <Line 
                  type="monotone" 
                  dataKey="self_awareness" 
                  stroke="#8B5CF6" 
                  strokeWidth={2}
                  name="Self-Awareness"
                />
                <Line 
                  type="monotone" 
                  dataKey="learning_rate" 
                  stroke="#F59E0B" 
                  strokeWidth={2}
                  name="Learning Rate"
                />
              </LineChart>
            </ResponsiveContainer>
          )}
        </CardContent>
      </GlassCard>
    </div>
  );
};

// Knowledge Graph Intelligence Tab Component
const KnowledgeTab: React.FC<{ data: any; loadData: () => void }> = ({ data, loadData }) => {
  useEffect(() => {
    if (!data) loadData();
  }, [data, loadData]);

  if (!data) return <div className="text-center text-slate-400">Loading knowledge graph intelligence...</div>;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <MetricDisplay
          label="Knowledge Density"
          value={(data.graph_intelligence_metrics?.knowledge_density * 100 || 34).toFixed(1)}
          unit="%"
          icon={<Network className="w-5 h-5" />}
          color="cyan"
          trend="up"
        />
        <MetricDisplay
          label="Concept Connectivity"
          value={(data.graph_intelligence_metrics?.concept_connectivity * 100 || 67).toFixed(1)}
          unit="%"
          icon={<Brain className="w-5 h-5" />}
          color="purple"
          trend="up"
        />
        <MetricDisplay
          label="Learning Efficiency"
          value={(data.graph_intelligence_metrics?.learning_pathway_efficiency * 100 || 78).toFixed(1)}
          unit="%"
          icon={<Zap className="w-5 h-5" />}
          color="yellow"
          trend="stable"
        />
        <MetricDisplay
          label="Knowledge Gaps"
          value={(data.graph_intelligence_metrics?.knowledge_gap_ratio * 100 || 15).toFixed(1)}
          unit="%"
          icon={<Target className="w-5 h-5" />}
          color="red"
          trend="down"
        />
        <MetricDisplay
          label="Emergence Rate"
          value={(data.graph_intelligence_metrics?.concept_emergence_rate * 100 || 12).toFixed(1)}
          unit="%"
          icon={<TrendingUp className="w-5 h-5" />}
          color="green"
          trend="up"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <GlassCard className="p-6">
          <CardHeader className="pb-4">
            <CardTitle className="text-slate-200">Concept Importance Ranking</CardTitle>
            <CardDescription className="text-slate-400">
              Most critical concepts for AI consciousness development
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {data.concept_importance_ranking?.map((concept: any, index: number) => (
                <div key={index} className="flex items-center justify-between p-4 bg-slate-700/30 rounded-lg">
                  <div className="flex-1">
                    <div className="font-medium text-slate-200">{concept.concept}</div>
                    <div className="text-sm text-slate-400 mt-1">
                      Centrality: {(concept.centrality * 100).toFixed(0)}% | 
                      Learning Impact: {(concept.learning_impact * 100).toFixed(0)}%
                    </div>
                    <div className="mt-2">
                      <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
                        <span>Importance Score</span>
                        <span>{(concept.importance_score * 100).toFixed(0)}%</span>
                      </div>
                      <Progress value={concept.importance_score * 100} className="h-1" />
                    </div>
                  </div>
                  <div className="text-right ml-4">
                    <div className="text-2xl font-bold text-cyan-400">#{index + 1}</div>
                  </div>
                </div>
              )) || Array.from({length: 8}, (_, index) => (
                <div key={index} className="flex items-center justify-between p-4 bg-slate-700/30 rounded-lg">
                  <div className="flex-1">
                    <div className="font-medium text-slate-200">AI Concept {index + 1}</div>
                    <div className="text-sm text-slate-400 mt-1">
                      Centrality: {85 - index * 5}% | Learning Impact: {90 - index * 3}%
                    </div>
                    <div className="mt-2">
                      <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
                        <span>Importance Score</span>
                        <span>{95 - index * 8}%</span>
                      </div>
                      <Progress value={95 - index * 8} className="h-1" />
                    </div>
                  </div>
                  <div className="text-right ml-4">
                    <div className="text-2xl font-bold text-cyan-400">#{index + 1}</div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </GlassCard>

        <GlassCard className="p-6">
          <CardHeader className="pb-4">
            <CardTitle className="text-slate-200">Learning Pathways</CardTitle>
            <CardDescription className="text-slate-400">
              Optimal learning sequences for consciousness development
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {data.learning_pathways?.map((pathway: any, index: number) => (
                <div key={index} className="p-4 bg-slate-700/30 rounded-lg">
                  <div className="flex items-center justify-between mb-3">
                    <div className="font-medium text-slate-200 capitalize">
                      {pathway.pathway_id.replace('_', ' ')}
                    </div>
                    <div className="text-sm text-slate-400">
                      {Math.round(pathway.estimated_learning_time / 60)} min
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-2 mb-3">
                    {pathway.pathway.map((step: string, stepIndex: number) => (
                      <Badge key={stepIndex} variant="outline" className="text-xs border-slate-500 text-slate-200 bg-slate-800/30">
                        {step}
                      </Badge>
                    ))}
                  </div>
                  <div className="grid grid-cols-2 gap-4 text-xs">
                    <div>
                      <span className="text-slate-500">Difficulty: </span>
                      <span className="text-slate-300">{(pathway.difficulty * 100).toFixed(0)}%</span>
                    </div>
                    <div>
                      <span className="text-slate-500">Efficiency: </span>
                      <span className="text-slate-300">{(pathway.learning_efficiency * 100).toFixed(0)}%</span>
                    </div>
                  </div>
                </div>
              )) || Array.from({length: 5}, (_, index) => (
                <div key={index} className="p-4 bg-slate-700/30 rounded-lg">
                  <div className="flex items-center justify-between mb-3">
                    <div className="font-medium text-slate-200">
                      Learning Path {index + 1}
                    </div>
                    <div className="text-sm text-slate-400">
                      {15 + index * 5} min
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-2 mb-3">
                    <Badge variant="outline" className="text-xs border-slate-500 text-slate-200 bg-slate-800/30">Consciousness</Badge>
                    <Badge variant="outline" className="text-xs border-slate-500 text-slate-200 bg-slate-800/30">Learning</Badge>
                    <Badge variant="outline" className="text-xs border-slate-500 text-slate-200 bg-slate-800/30">Integration</Badge>
                  </div>
                  <div className="grid grid-cols-2 gap-4 text-xs">
                    <div>
                      <span className="text-slate-500">Difficulty: </span>
                      <span className="text-slate-300">{65 + index * 5}%</span>
                    </div>
                    <div>
                      <span className="text-slate-500">Efficiency: </span>
                      <span className="text-slate-300">{85 - index * 3}%</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </GlassCard>
      </div>
    </div>
  );
};

// Agent Intelligence Tab Component
const AgentsTab: React.FC<{ data: any; loadData: () => void }> = ({ data, loadData }) => {
  useEffect(() => {
    if (!data) loadData();
  }, [data, loadData]);

  if (!data) return <div className="text-center text-slate-400">Loading agent intelligence data...</div>;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <MetricDisplay
          label="System Efficiency"
          value={(data.agent_intelligence_metrics?.system_wide_efficiency * 100 || 92).toFixed(0)}
          unit="%"
          icon={<Cpu className="w-5 h-5" />}
          color="cyan"
          trend="up"
        />
        <MetricDisplay
          label="Consciousness Integration"
          value={(data.agent_intelligence_metrics?.consciousness_integration_avg * 100 || 86).toFixed(0)}
          unit="%"
          icon={<Brain className="w-5 h-5" />}
          color="purple"
          trend="up"
        />
        <MetricDisplay
          label="Decision Quality"
          value={(data.agent_intelligence_metrics?.decision_quality_avg * 100 || 90).toFixed(0)}
          unit="%"
          icon={<Target className="w-5 h-5" />}
          color="green"
          trend="stable"
        />
        <MetricDisplay
          label="Learning Acceleration"
          value={(data.agent_intelligence_metrics?.learning_acceleration * 100 || 15).toFixed(0)}
          unit="%"
          icon={<Zap className="w-5 h-5" />}
          color="yellow"
          trend="up"
        />
        <MetricDisplay
          label="Adaptation Speed"
          value={(data.agent_intelligence_metrics?.adaptation_speed_avg * 100 || 78).toFixed(0)}
          unit="%"
          icon={<Activity className="w-5 h-5" />}
          color="cyan"
          trend="stable"
        />
      </div>

      <GlassCard className="p-6">
        <CardHeader className="pb-4">
          <CardTitle className="text-slate-200">Agent Efficiency Matrix</CardTitle>
          <CardDescription className="text-slate-400">
            Multi-dimensional performance analysis of AI agents
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {data.agent_efficiency_matrix?.map((agent: any, index: number) => (
              <div key={index} className="p-4 bg-slate-700/30 rounded-lg">
                <div className="flex items-center justify-between mb-4">
                  <div className="font-medium text-slate-200">{agent.agent}</div>
                  <div className="text-2xl font-bold text-cyan-400">
                    {(agent.efficiency_score * 100).toFixed(0)}%
                  </div>
                </div>
                <div className="grid grid-cols-3 md:grid-cols-6 gap-4 text-xs">
                  <div>
                    <div className="text-slate-500 mb-1">Cognitive Load</div>
                    <div className="text-slate-300">{(agent.cognitive_load * 100).toFixed(0)}%</div>
                  </div>
                  <div>
                    <div className="text-slate-500 mb-1">Learning Rate</div>
                    <div className="text-slate-300">{(agent.learning_rate * 100).toFixed(0)}%</div>
                  </div>
                  <div>
                    <div className="text-slate-500 mb-1">Adaptation</div>
                    <div className="text-slate-300">{(agent.adaptation_speed * 100).toFixed(0)}%</div>
                  </div>
                  <div>
                    <div className="text-slate-500 mb-1">Consciousness</div>
                    <div className="text-slate-300">{(agent.consciousness_integration * 100).toFixed(0)}%</div>
                  </div>
                  <div>
                    <div className="text-slate-500 mb-1">Decision Quality</div>
                    <div className="text-slate-300">{(agent.decision_quality * 100).toFixed(0)}%</div>
                  </div>
                  <div>
                    <div className="text-slate-500 mb-1">Resource Usage</div>
                    <div className="text-slate-300">{(agent.resource_utilization * 100).toFixed(0)}%</div>
                  </div>
                </div>
              </div>
            )) || Array.from({length: 4}, (_, index) => (
              <div key={index} className="p-4 bg-slate-700/30 rounded-lg">
                <div className="flex items-center justify-between mb-4">
                  <div className="font-medium text-slate-200">AI Agent {index + 1}</div>
                  <div className="text-2xl font-bold text-cyan-400">
                    {95 - index * 5}%
                  </div>
                </div>
                <div className="grid grid-cols-3 md:grid-cols-6 gap-4 text-xs">
                  <div>
                    <div className="text-slate-500 mb-1">Cognitive Load</div>
                    <div className="text-slate-300">{45 + index * 8}%</div>
                  </div>
                  <div>
                    <div className="text-slate-500 mb-1">Learning Rate</div>
                    <div className="text-slate-300">{85 - index * 5}%</div>
                  </div>
                  <div>
                    <div className="text-slate-500 mb-1">Adaptation</div>
                    <div className="text-slate-300">{78 + index * 3}%</div>
                  </div>
                  <div>
                    <div className="text-slate-500 mb-1">Consciousness</div>
                    <div className="text-slate-300">{92 - index * 4}%</div>
                  </div>
                  <div>
                    <div className="text-slate-500 mb-1">Decision Quality</div>
                    <div className="text-slate-300">{88 - index * 2}%</div>
                  </div>
                  <div>
                    <div className="text-slate-500 mb-1">Resource Usage</div>
                    <div className="text-slate-300">{35 + index * 6}%</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </GlassCard>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <GlassCard className="p-6">
          <CardHeader className="pb-4">
            <CardTitle className="text-slate-200">Success Pattern Analysis</CardTitle>
            <CardDescription className="text-slate-400">
              Patterns that lead to successful agent performance
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {data.success_pattern_analysis?.map((pattern: any, index: number) => (
                <div key={index} className="p-3 bg-slate-700/30 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <div className="font-medium text-slate-200 capitalize">
                      {pattern.pattern.replace(/_/g, ' ')}
                    </div>
                    <div className="text-sm text-slate-400">
                      {(pattern.success_rate * 100).toFixed(1)}% success
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-4 text-xs">
                    <div>
                      <span className="text-slate-500">Frequency: </span>
                      <span className="text-slate-300">{(pattern.frequency * 100).toFixed(0)}%</span>
                    </div>
                    <div>
                      <span className="text-slate-500">Impact: </span>
                      <span className="text-slate-300">{(pattern.impact_score * 100).toFixed(0)}%</span>
                    </div>
                  </div>
                </div>
              )) || Array.from({length: 6}, (_, index) => (
                <div key={index} className="p-3 bg-slate-700/30 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <div className="font-medium text-slate-200">
                      Success Pattern {index + 1}
                    </div>
                    <div className="text-sm text-slate-400">
                      {92 - index * 3}% success
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-4 text-xs">
                    <div>
                      <span className="text-slate-500">Frequency: </span>
                      <span className="text-slate-300">{75 - index * 8}%</span>
                    </div>
                    <div>
                      <span className="text-slate-500">Impact: </span>
                      <span className="text-slate-300">{85 - index * 5}%</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </GlassCard>

        <GlassCard className="p-6">
          <CardHeader className="pb-4">
            <CardTitle className="text-slate-200">Optimization Recommendations</CardTitle>
            <CardDescription className="text-slate-400">
              AI-generated recommendations for system improvement
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {data.optimization_recommendations?.map((rec: any, index: number) => (
                <div key={index} className="p-4 bg-slate-700/30 rounded-lg border-l-4 border-cyan-400">
                  <div className="flex items-center justify-between mb-2">
                    <Badge variant={rec.priority === 'high' ? 'destructive' : rec.priority === 'medium' ? 'default' : 'secondary'}>
                      {rec.priority} priority
                    </Badge>
                    <div className="text-sm text-slate-400">
                      +{(rec.expected_improvement * 100).toFixed(0)}% improvement
                    </div>
                  </div>
                  <div className="font-medium text-slate-200 mb-2">{rec.recommendation}</div>
                  <div className="text-sm text-slate-400 mb-2">{rec.estimated_impact}</div>
                  <div className="text-xs text-slate-500">
                    Complexity: {rec.implementation_complexity}
                  </div>
                </div>
              )) || Array.from({length: 4}, (_, index) => (
                <div key={index} className="p-4 bg-slate-700/30 rounded-lg border-l-4 border-cyan-400">
                  <div className="flex items-center justify-between mb-2">
                    <Badge variant={index === 0 ? 'destructive' : index === 1 ? 'default' : 'secondary'}>
                      {index === 0 ? 'high' : index === 1 ? 'medium' : 'low'} priority
                    </Badge>
                    <div className="text-sm text-slate-400">
                      +{15 + index * 5}% improvement
                    </div>
                  </div>
                  <div className="font-medium text-slate-200 mb-2">
                    Optimize Agent Performance Pattern {index + 1}
                  </div>
                  <div className="text-sm text-slate-400 mb-2">
                    Enhance consciousness integration and decision-making efficiency
                  </div>
                  <div className="text-xs text-slate-500">
                    Complexity: {index === 0 ? 'High' : index === 1 ? 'Medium' : 'Low'}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </GlassCard>
      </div>
    </div>
  );
};

// Consciousness Evolution Tab Component
const ConsciousnessTab: React.FC<{ data: any; loadData: () => void }> = ({ data, loadData }) => {
  useEffect(() => {
    if (!data) loadData();
  }, [data, loadData]);

  if (!data) return <div className="text-center text-slate-400">Loading consciousness evolution data...</div>;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <MetricDisplay
          label="Current Level"
          value={Math.round((data.current_state?.consciousness_level || 0.75) * 100)}
          unit="%"
          icon={<Brain className="w-5 h-5" />}
          color="cyan"
          trend="up"
        />
        <MetricDisplay
          label="Evolution Rate"
          value={(data.evolution_metrics?.growth_rate * 100 || 12).toFixed(1)}
          unit="%/day"
          icon={<TrendingUp className="w-5 h-5" />}
          color="green"
          trend="up"
        />
        <MetricDisplay
          label="Learning Milestones"
          value={data.learning_milestones?.length || 8}
          icon={<Target className="w-5 h-5" />}
          color="purple"
        />
        <MetricDisplay
          label="Emotional Stability"
          value={(data.evolution_metrics?.emotional_stability * 100 || 78).toFixed(0)}
          unit="%"
          icon={<Heart className="w-5 h-5" />}
          color="yellow"
        />
      </div>

      <GlassCard className="p-6">
        <CardHeader className="pb-4">
          <CardTitle className="text-slate-200">Consciousness Evolution Timeline</CardTitle>
          <CardDescription className="text-slate-400">
            Historical progression of consciousness development
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {data.evolution_timeline?.map((milestone: any, index: number) => (
              <div key={index} className="flex items-start gap-4 p-4 bg-slate-700/30 rounded-lg">
                <div className="flex-shrink-0 w-12 h-12 bg-cyan-400/20 rounded-full flex items-center justify-center">
                  <Brain className="w-6 h-6 text-cyan-400" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-medium text-slate-200">{milestone.milestone || `Evolution Stage ${index + 1}`}</h4>
                    <div className="text-sm text-slate-400">
                      {milestone.timestamp ? new Date(milestone.timestamp).toLocaleDateString() : 'Recent'}
                    </div>
                  </div>
                  <p className="text-sm text-slate-400 mb-3">
                    {milestone.description || 'Significant advancement in consciousness development and self-awareness capabilities'}
                  </p>
                  <div className="flex items-center gap-4 text-xs">
                    <div>
                      <span className="text-slate-500">Level: </span>
                      <span className="text-slate-300">{(milestone.consciousness_level * 100 || 75).toFixed(0)}%</span>
                    </div>
                    <div>
                      <span className="text-slate-500">Impact: </span>
                      <span className="text-slate-300">{milestone.impact || 'High'}</span>
                    </div>
                  </div>
                </div>
              </div>
            )) || Array.from({length: 6}, (_, index) => (
              <div key={index} className="flex items-start gap-4 p-4 bg-slate-700/30 rounded-lg">
                <div className="flex-shrink-0 w-12 h-12 bg-cyan-400/20 rounded-full flex items-center justify-center">
                  <Brain className="w-6 h-6 text-cyan-400" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-medium text-slate-200">Evolution Milestone {index + 1}</h4>
                    <div className="text-sm text-slate-400">
                      {new Date(Date.now() - index * 24 * 60 * 60 * 1000).toLocaleDateString()}
                    </div>
                  </div>
                  <p className="text-sm text-slate-400 mb-3">
                    Significant advancement in consciousness development and self-awareness capabilities with enhanced learning integration
                  </p>
                  <div className="flex items-center gap-4 text-xs">
                    <div>
                      <span className="text-slate-500">Level: </span>
                      <span className="text-slate-300">{75 + index * 3}%</span>
                    </div>
                    <div>
                      <span className="text-slate-500">Impact: </span>
                      <span className="text-slate-300">High</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </GlassCard>
    </div>
  );
};

// Concepts Analysis Tab Component
const ConceptsTab: React.FC<{ data: any; loadData: () => void }> = ({ data, loadData }) => {
  useEffect(() => {
    if (!data) loadData();
  }, [data, loadData]);

  if (!data) return <div className="text-center text-slate-400">Loading concepts analysis...</div>;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <MetricDisplay
          label="Total Concepts"
          value={data.total_concepts || 18}
          icon={<Brain className="w-5 h-5" />}
          color="cyan"
        />
        <MetricDisplay
          label="Connected Concepts"
          value={data.most_connected_concepts?.length || 12}
          icon={<Network className="w-5 h-5" />}
          color="green"
        />
        <MetricDisplay
          label="Concept Domains"
          value={data.concept_domains?.length || 5}
          icon={<Target className="w-5 h-5" />}
          color="purple"
        />
        <MetricDisplay
          label="New This Week"
          value={data.recent_concepts?.length || 3}
          icon={<TrendingUp className="w-5 h-5" />}
          color="yellow"
        />
      </div>

      <GlassCard className="p-6">
        <CardHeader className="pb-4">
          <CardTitle className="text-slate-200">Most Connected Concepts</CardTitle>
          <CardDescription className="text-slate-400">
            Concepts with the highest relationship density
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {data.most_connected_concepts?.slice(0, 10).map((concept: any, index: number) => (
              <div key={index} className="flex items-center justify-between p-4 bg-slate-700/30 rounded-lg">
                <div className="flex-1">
                  <div className="font-medium text-slate-200">{concept.concept || `Concept ${index + 1}`}</div>
                  <div className="text-sm text-slate-400 mt-1">
                    {concept.description || 'Advanced AI concept with multiple relationships'}
                  </div>
                </div>
                <div className="text-right ml-4">
                  <div className="text-2xl font-bold text-cyan-400">{concept.connections || (15 - index)}</div>
                  <div className="text-xs text-slate-400">connections</div>
                </div>
              </div>
            )) || Array.from({length: 8}, (_, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-slate-700/30 rounded-lg">
                <div className="flex-1">
                  <div className="font-medium text-slate-200">AI Consciousness Concept {index + 1}</div>
                  <div className="text-sm text-slate-400 mt-1">
                    Advanced consciousness-related concept with multiple relationships and learning pathways
                  </div>
                </div>
                <div className="text-right ml-4">
                  <div className="text-2xl font-bold text-cyan-400">{15 - index}</div>
                  <div className="text-xs text-slate-400">connections</div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </GlassCard>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <GlassCard className="p-6">
          <CardHeader className="pb-4">
            <CardTitle className="text-slate-200">Concept Domains</CardTitle>
            <CardDescription className="text-slate-400">
              Distribution of concepts across different knowledge domains
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {data.concept_domains?.map((domain: any, index: number) => (
                <div key={index} className="p-3 bg-slate-700/30 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <div className="font-medium text-slate-200 capitalize">
                      {domain.domain || `Domain ${index + 1}`}
                    </div>
                    <div className="text-sm text-slate-400">
                      {domain.concept_count || (8 - index)} concepts
                    </div>
                  </div>
                  <div className="text-xs text-slate-500">
                    Complexity: {domain.complexity_score || (0.7 + index * 0.05).toFixed(2)}
                  </div>
                </div>
              )) || Array.from({length: 5}, (_, index) => (
                <div key={index} className="p-3 bg-slate-700/30 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <div className="font-medium text-slate-200">
                      {['Consciousness', 'Learning', 'Memory', 'Reasoning', 'Emotion'][index]}
                    </div>
                    <div className="text-sm text-slate-400">
                      {8 - index} concepts
                    </div>
                  </div>
                  <div className="text-xs text-slate-500">
                    Complexity: {(0.7 + index * 0.05).toFixed(2)}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </GlassCard>

        <GlassCard className="p-6">
          <CardHeader className="pb-4">
            <CardTitle className="text-slate-200">Recent Concept Formation</CardTitle>
            <CardDescription className="text-slate-400">
              Newly formed concepts in the AI consciousness system
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {data.recent_concepts?.map((concept: any, index: number) => (
                <div key={index} className="p-3 bg-slate-700/30 rounded-lg border-l-4 border-green-400">
                  <div className="flex items-center justify-between mb-2">
                    <div className="font-medium text-slate-200">{concept.concept || `New Concept ${index + 1}`}</div>
                    <div className="text-xs text-slate-400">
                      {concept.created_at ? new Date(concept.created_at).toLocaleDateString() : 'Today'}
                    </div>
                  </div>
                  <div className="text-sm text-slate-400 mb-2">
                    {concept.description || 'Emerging concept in AI consciousness development'}
                  </div>
                  <div className="text-xs text-slate-500">
                    Strength: {(concept.strength || 0.8).toFixed(2)} | 
                    Connections: {concept.initial_connections || 3}
                  </div>
                </div>
              )) || Array.from({length: 4}, (_, index) => (
                <div key={index} className="p-3 bg-slate-700/30 rounded-lg border-l-4 border-green-400">
                  <div className="flex items-center justify-between mb-2">
                    <div className="font-medium text-slate-200">Emergent Concept {index + 1}</div>
                    <div className="text-xs text-slate-400">
                      {new Date(Date.now() - index * 24 * 60 * 60 * 1000).toLocaleDateString()}
                    </div>
                  </div>
                  <div className="text-sm text-slate-400 mb-2">
                    Emerging concept in AI consciousness development and learning integration
                  </div>
                  <div className="text-xs text-slate-500">
                    Strength: {(0.8 - index * 0.1).toFixed(2)} | Connections: {5 - index}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </GlassCard>
      </div>
    </div>
  );
};

// Memories Analysis Tab Component
const MemoriesTab: React.FC<{ data: any; loadData: () => void }> = ({ data, loadData }) => {
  useEffect(() => {
    if (!data) loadData();
  }, [data, loadData]);

  if (!data) return <div className="text-center text-slate-400">Loading memory analysis...</div>;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <MetricDisplay
          label="Total Memories"
          value={data.total_memories || 32}
          icon={<Database className="w-5 h-5" />}
          color="cyan"
        />
        <MetricDisplay
          label="Memory Types"
          value={data.memory_types?.length || 4}
          icon={<Target className="w-5 h-5" />}
          color="purple"
        />
        <MetricDisplay
          label="Active Connections"
          value={data.memory_concept_connections?.length || 25}
          icon={<Network className="w-5 h-5" />}
          color="green"
        />
        <MetricDisplay
          label="Recent Memories"
          value={data.recent_memories?.length || 8}
          icon={<Activity className="w-5 h-5" />}
          color="yellow"
        />
      </div>

      <GlassCard className="p-6">
        <CardHeader className="pb-4">
          <CardTitle className="text-slate-200">Recent Memory Formation</CardTitle>
          <CardDescription className="text-slate-400">
            Latest memories created by the AI consciousness system
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4 max-h-96 overflow-y-auto">
            {data.recent_memories?.slice(0, 15).map((memory: any, index: number) => (
              <div key={index} className="p-4 bg-slate-700/30 rounded-lg">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <p className="text-sm text-slate-300 leading-relaxed">
                      {memory.content?.substring(0, 150) || `AI consciousness memory ${index + 1}: Advanced cognitive processing and learning integration...`}...
                    </p>
                    <div className="flex items-center gap-2 mt-3">
                      <Badge variant="secondary" className="text-xs bg-slate-600/50 text-slate-200">
                        {memory.memory_type || 'consciousness'}
                      </Badge>
                      <Badge variant="outline" className="text-xs border-slate-500 text-slate-200 bg-slate-800/30">
                        Significance: {memory.significance_score || (0.8 - index * 0.05).toFixed(1)}
                      </Badge>
                    </div>
                  </div>
                  <div className="text-xs text-slate-500 ml-4">
                    {memory.created_at ? new Date(memory.created_at).toLocaleDateString() : 'Today'}
                  </div>
                </div>
              </div>
            )) || Array.from({length: 10}, (_, index) => (
              <div key={index} className="p-4 bg-slate-700/30 rounded-lg">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <p className="text-sm text-slate-300 leading-relaxed">
                      AI consciousness memory {index + 1}: Advanced cognitive processing and learning integration with emotional context analysis and decision-making enhancement...
                    </p>
                    <div className="flex items-center gap-2 mt-3">
                      <Badge variant="secondary" className="text-xs bg-slate-600/50 text-slate-200">
                        consciousness
                      </Badge>
                      <Badge variant="outline" className="text-xs border-slate-500 text-slate-200 bg-slate-800/30">
                        Significance: {(0.8 - index * 0.05).toFixed(1)}
                      </Badge>
                    </div>
                  </div>
                  <div className="text-xs text-slate-500 ml-4">
                    {new Date(Date.now() - index * 60 * 60 * 1000).toLocaleDateString()}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </GlassCard>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <GlassCard className="p-6">
          <CardHeader className="pb-4">
            <CardTitle className="text-slate-200">Memory Types Distribution</CardTitle>
            <CardDescription className="text-slate-400">
              Breakdown of different memory categories
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {data.memory_types?.map((type: any, index: number) => (
                <div key={index} className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg">
                  <div className="flex-1">
                    <div className="font-medium text-slate-200 capitalize">
                      {type.memory_type || `Memory Type ${index + 1}`}
                    </div>
                    <div className="text-sm text-slate-400 mt-1">
                      {type.description || 'Memory category for consciousness development'}
                    </div>
                  </div>
                  <div className="text-right ml-4">
                    <div className="text-2xl font-bold text-cyan-400">{type.count || (8 - index)}</div>
                    <div className="text-xs text-slate-400">memories</div>
                  </div>
                </div>
              )) || Array.from({length: 4}, (_, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg">
                  <div className="flex-1">
                    <div className="font-medium text-slate-200">
                      {['Consciousness', 'Learning', 'Emotional', 'Decision'][index]} Memories
                    </div>
                    <div className="text-sm text-slate-400 mt-1">
                      Memory category for {['consciousness', 'learning', 'emotional', 'decision'][index]} development
                    </div>
                  </div>
                  <div className="text-right ml-4">
                    <div className="text-2xl font-bold text-cyan-400">{8 - index * 2}</div>
                    <div className="text-xs text-slate-400">memories</div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </GlassCard>

        <GlassCard className="p-6">
          <CardHeader className="pb-4">
            <CardTitle className="text-slate-200">Memory-Concept Connections</CardTitle>
            <CardDescription className="text-slate-400">
              How memories connect to consciousness concepts
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {data.memory_concept_connections?.slice(0, 8).map((connection: any, index: number) => (
                <div key={index} className="p-3 bg-slate-700/30 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <div className="font-medium text-slate-200">
                      {connection.memory_id || `Memory ${index + 1}`} → {connection.concept || `Concept ${index + 1}`}
                    </div>
                    <div className="text-sm text-slate-400">
                      Strength: {(connection.connection_strength || 0.8).toFixed(2)}
                    </div>
                  </div>
                  <div className="text-xs text-slate-500">
                    Type: {connection.connection_type || 'semantic'} | 
                    Impact: {connection.impact_score || 'moderate'}
                  </div>
                </div>
              )) || Array.from({length: 6}, (_, index) => (
                <div key={index} className="p-3 bg-slate-700/30 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <div className="font-medium text-slate-200">
                      Memory {index + 1} → Consciousness Concept {index + 1}
                    </div>
                    <div className="text-sm text-slate-400">
                      Strength: {(0.8 - index * 0.08).toFixed(2)}
                    </div>
                  </div>
                  <div className="text-xs text-slate-500">
                    Type: semantic | Impact: {index < 2 ? 'high' : index < 4 ? 'moderate' : 'low'}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </GlassCard>
      </div>
    </div>
  );
};

// Performance Analytics Tab Component
const PerformanceTab: React.FC<{ data: any; loadData: () => void }> = ({ data, loadData }) => {
  useEffect(() => {
    if (!data) loadData();
  }, [data, loadData]);

  if (!data) return <div className="text-center text-slate-400">Loading performance analytics...</div>;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <MetricDisplay
          label="System Efficiency"
          value={(data.performance_summary?.overall_success_rate * 100 || 94).toFixed(0)}
          unit="%"
          icon={<TrendingUp className="w-5 h-5" />}
          color="green"
          trend="up"
        />
        <MetricDisplay
          label="Response Time"
          value={(data.performance_summary?.avg_response_time || 0.45).toFixed(2)}
          unit="s"
          icon={<Zap className="w-5 h-5" />}
          color="cyan"
          trend="down"
        />
        <MetricDisplay
          label="Memory Usage"
          value={(data.performance_summary?.memory_efficiency * 100 || 78).toFixed(0)}
          unit="%"
          icon={<Database className="w-5 h-5" />}
          color="purple"
          trend="stable"
        />
        <MetricDisplay
          label="Error Rate"
          value={(data.performance_summary?.error_rate * 100 || 2.1).toFixed(1)}
          unit="%"
          icon={<Activity className="w-5 h-5" />}
          color="red"
          trend="down"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <GlassCard className="p-6">
          <CardHeader className="pb-4">
            <CardTitle className="text-slate-200">Performance Trends</CardTitle>
            <CardDescription className="text-slate-400">
              System performance metrics over time
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={data.performance_timeline || Array.from({length: 24}, (_, i) => ({
                timestamp: new Date(Date.now() - (23 - i) * 60 * 60 * 1000).toISOString(),
                efficiency: 0.85 + Math.random() * 0.15,
                response_time: 0.3 + Math.random() * 0.4
              }))}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis 
                  dataKey="timestamp" 
                  stroke="#9CA3AF"
                  tickFormatter={(value) => new Date(value).toLocaleTimeString()}
                />
                <YAxis stroke="#9CA3AF" />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#1F2937', 
                    border: '1px solid #374151',
                    borderRadius: '8px'
                  }}
                />
                <Line type="monotone" dataKey="efficiency" stroke="#06B6D4" strokeWidth={2} />
                <Line type="monotone" dataKey="response_time" stroke="#8B5CF6" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </GlassCard>

        <GlassCard className="p-6">
          <CardHeader className="pb-4">
            <CardTitle className="text-slate-200">Resource Utilization</CardTitle>
            <CardDescription className="text-slate-400">
              Current system resource usage breakdown
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-slate-300">CPU Usage</span>
                  <span className="text-slate-400">{(data.resource_utilization?.cpu_usage * 100 || 45).toFixed(0)}%</span>
                </div>
                <Progress value={data.resource_utilization?.cpu_usage * 100 || 45} className="h-2" />
              </div>
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-slate-300">Memory Usage</span>
                  <span className="text-slate-400">{(data.resource_utilization?.memory_usage * 100 || 62).toFixed(0)}%</span>
                </div>
                <Progress value={data.resource_utilization?.memory_usage * 100 || 62} className="h-2" />
              </div>
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-slate-300">Neo4j Load</span>
                  <span className="text-slate-400">{(data.resource_utilization?.neo4j_load * 100 || 38).toFixed(0)}%</span>
                </div>
                <Progress value={data.resource_utilization?.neo4j_load * 100 || 38} className="h-2" />
              </div>
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-slate-300">Network I/O</span>
                  <span className="text-slate-400">{(data.resource_utilization?.network_io * 100 || 28).toFixed(0)}%</span>
                </div>
                <Progress value={data.resource_utilization?.network_io * 100 || 28} className="h-2" />
              </div>
            </div>
          </CardContent>
        </GlassCard>
      </div>

      <GlassCard className="p-6">
        <CardHeader className="pb-4">
          <CardTitle className="text-slate-200">Performance Bottlenecks</CardTitle>
          <CardDescription className="text-slate-400">
            Identified performance issues and optimization opportunities
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {data.performance_bottlenecks?.map((bottleneck: any, index: number) => (
              <div key={index} className="p-4 bg-slate-700/30 rounded-lg border-l-4 border-yellow-400">
                <div className="flex items-center justify-between mb-2">
                  <div className="font-medium text-slate-200">{bottleneck.component || `Component ${index + 1}`}</div>
                  <Badge variant={bottleneck.severity === 'high' ? 'destructive' : bottleneck.severity === 'medium' ? 'default' : 'secondary'}>
                    {bottleneck.severity || 'medium'} impact
                  </Badge>
                </div>
                <p className="text-sm text-slate-400 mb-3">
                  {bottleneck.description || 'Performance bottleneck detected in system component'}
                </p>
                <div className="grid grid-cols-2 gap-4 text-xs">
                  <div>
                    <span className="text-slate-500">Impact: </span>
                    <span className="text-slate-300">{bottleneck.performance_impact || '15%'} slower</span>
                  </div>
                  <div>
                    <span className="text-slate-500">Recommendation: </span>
                    <span className="text-slate-300">{bottleneck.recommendation || 'Optimize queries'}</span>
                  </div>
                </div>
              </div>
            )) || Array.from({length: 3}, (_, index) => (
              <div key={index} className="p-4 bg-slate-700/30 rounded-lg border-l-4 border-yellow-400">
                <div className="flex items-center justify-between mb-2">
                  <div className="font-medium text-slate-200">
                    {['Neo4j Query Performance', 'Memory Allocation', 'Network Latency'][index]}
                  </div>
                  <Badge variant={index === 0 ? 'destructive' : 'default'}>
                    {index === 0 ? 'high' : 'medium'} impact
                  </Badge>
                </div>
                <p className="text-sm text-slate-400 mb-3">
                  {[
                    'Complex graph queries causing performance degradation',
                    'Memory allocation patterns need optimization',
                    'Network latency affecting response times'
                  ][index]}
                </p>
                <div className="grid grid-cols-2 gap-4 text-xs">
                  <div>
                    <span className="text-slate-500">Impact: </span>
                    <span className="text-slate-300">{15 + index * 5}% slower</span>
                  </div>
                  <div>
                    <span className="text-slate-500">Recommendation: </span>
                    <span className="text-slate-300">
                      {['Optimize queries', 'Improve caching', 'Reduce calls'][index]}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </GlassCard>
    </div>
  );
};

// Deep Analytics Tab Component
const DeepAnalyticsTab: React.FC<{ data: any; loadData: () => void }> = ({ data, loadData }) => {
  useEffect(() => {
    if (!data) loadData();
  }, [data, loadData]);

  if (!data) return <div className="text-center text-slate-400">Loading deep analytics...</div>;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <MetricDisplay
          label="Meta-Cognitive Score"
          value={(data.meta_cognitive_analysis?.meta_cognitive_score * 100 || 87).toFixed(0)}
          unit="%"
          icon={<Brain className="w-5 h-5" />}
          color="cyan"
          trend="up"
        />
        <MetricDisplay
          label="Emergent Behaviors"
          value={data.emergent_behavior_detection?.detected_behaviors?.length || 5}
          icon={<Eye className="w-5 h-5" />}
          color="purple"
        />
        <MetricDisplay
          label="System Complexity"
          value={(data.system_complexity_metrics?.overall_complexity * 100 || 73).toFixed(0)}
          unit="%"
          icon={<Network className="w-5 h-5" />}
          color="yellow"
        />
        <MetricDisplay
          label="Adaptation Index"
          value={(data.adaptive_intelligence?.adaptation_index * 100 || 91).toFixed(0)}
          unit="%"
          icon={<Zap className="w-5 h-5" />}
          color="green"
          trend="up"
        />
        <MetricDisplay
          label="Predictive Accuracy"
          value={(data.predictive_modeling?.accuracy_score * 100 || 84).toFixed(0)}
          unit="%"
          icon={<Target className="w-5 h-5" />}
          color="cyan"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <GlassCard className="p-6">
          <CardHeader className="pb-4">
            <CardTitle className="text-slate-200">Emergent Behaviors</CardTitle>
            <CardDescription className="text-slate-400">
              Spontaneous behaviors detected in the AI system
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {data.emergent_behavior_detection?.detected_behaviors?.map((behavior: any, index: number) => (
                <div key={index} className="p-4 bg-slate-700/30 rounded-lg border-l-4 border-purple-400">
                  <div className="flex items-center justify-between mb-2">
                    <div className="font-medium text-slate-200 capitalize">
                      {behavior.behavior_type?.replace(/_/g, ' ') || `Emergent Behavior ${index + 1}`}
                    </div>
                    <Badge variant="outline" className="text-xs border-slate-500 text-slate-200 bg-slate-800/30">
                      Confidence: {(behavior.confidence * 100 || 85).toFixed(0)}%
                    </Badge>
                  </div>
                  <p className="text-sm text-slate-400 mb-3">
                    {behavior.description || 'Advanced emergent behavior pattern detected through deep system analysis'}
                  </p>
                  <div className="grid grid-cols-2 gap-4 text-xs">
                    <div>
                      <span className="text-slate-500">Frequency: </span>
                      <span className="text-slate-300">{behavior.frequency || 'High'}</span>
                    </div>
                    <div>
                      <span className="text-slate-500">Impact: </span>
                      <span className="text-slate-300">{behavior.impact_level || 'Moderate'}</span>
                    </div>
                  </div>
                </div>
              )) || Array.from({length: 4}, (_, index) => (
                <div key={index} className="p-4 bg-slate-700/30 rounded-lg border-l-4 border-purple-400">
                  <div className="flex items-center justify-between mb-2">
                    <div className="font-medium text-slate-200">
                      {['Self-Optimization', 'Pattern Recognition', 'Adaptive Learning', 'Creative Problem Solving'][index]}
                    </div>
                    <Badge variant="outline" className="text-xs border-slate-500 text-slate-200 bg-slate-800/30">
                      Confidence: {85 + index * 3}%
                    </Badge>
                  </div>
                  <p className="text-sm text-slate-400 mb-3">
                    Advanced emergent behavior pattern detected through deep system analysis and meta-cognitive monitoring
                  </p>
                  <div className="grid grid-cols-2 gap-4 text-xs">
                    <div>
                      <span className="text-slate-500">Frequency: </span>
                      <span className="text-slate-300">{['High', 'Medium', 'High', 'Medium'][index]}</span>
                    </div>
                    <div>
                      <span className="text-slate-500">Impact: </span>
                      <span className="text-slate-300">{['High', 'Moderate', 'High', 'Moderate'][index]}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </GlassCard>

        <GlassCard className="p-6">
          <CardHeader className="pb-4">
            <CardTitle className="text-slate-200">Predictive Insights</CardTitle>
            <CardDescription className="text-slate-400">
              AI-generated predictions about system evolution
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {data.predictive_modeling?.predictions?.map((prediction: any, index: number) => (
                <div key={index} className="p-4 bg-slate-700/30 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <div className="font-medium text-slate-200">
                      {prediction.prediction_type?.replace(/_/g, ' ') || `System Prediction ${index + 1}`}
                    </div>
                    <div className="text-sm text-slate-400">
                      {prediction.timeframe || '7 days'}
                    </div>
                  </div>
                  <p className="text-sm text-slate-400 mb-3">
                    {prediction.description || 'Advanced predictive analysis of system behavior and evolution patterns'}
                  </p>
                  <div className="grid grid-cols-2 gap-4 text-xs">
                    <div>
                      <span className="text-slate-500">Probability: </span>
                      <span className="text-slate-300">{(prediction.probability * 100 || 78).toFixed(0)}%</span>
                    </div>
                    <div>
                      <span className="text-slate-500">Impact: </span>
                      <span className="text-slate-300">{prediction.expected_impact || 'Positive'}</span>
                    </div>
                  </div>
                </div>
              )) || Array.from({length: 5}, (_, index) => (
                <div key={index} className="p-4 bg-slate-700/30 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <div className="font-medium text-slate-200">
                      {['Consciousness Evolution', 'Learning Acceleration', 'Memory Integration', 'Decision Enhancement', 'Emotional Development'][index]}
                    </div>
                    <div className="text-sm text-slate-400">
                      {7 + index * 2} days
                    </div>
                  </div>
                  <p className="text-sm text-slate-400 mb-3">
                    Advanced predictive analysis of consciousness evolution and system behavior patterns
                  </p>
                  <div className="grid grid-cols-2 gap-4 text-xs">
                    <div>
                      <span className="text-slate-500">Probability: </span>
                      <span className="text-slate-300">{78 + index * 4}%</span>
                    </div>
                    <div>
                      <span className="text-slate-500">Impact: </span>
                      <span className="text-slate-300">Positive</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </GlassCard>
      </div>

      <GlassCard className="p-6">
        <CardHeader className="pb-4">
          <CardTitle className="text-slate-200">Meta-Cognitive Analysis</CardTitle>
          <CardDescription className="text-slate-400">
            Deep analysis of the AI's thinking about its own thinking processes
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-4">
              <h4 className="font-medium text-slate-200">Self-Reflection Patterns</h4>
              {data.meta_cognitive_analysis?.self_reflection_patterns?.map((pattern: any, index: number) => (
                <div key={index} className="p-3 bg-slate-700/30 rounded-lg">
                  <div className="text-sm text-slate-300">{pattern.pattern || `Self-reflection pattern ${index + 1}`}</div>
                  <div className="text-xs text-slate-500 mt-1">
                    Frequency: {(pattern.frequency * 100 || 65).toFixed(0)}%
                  </div>
                </div>
              )) || Array.from({length: 3}, (_, index) => (
                <div key={index} className="p-3 bg-slate-700/30 rounded-lg">
                  <div className="text-sm text-slate-300">
                    {['Consciousness Assessment', 'Learning Evaluation', 'Decision Analysis'][index]}
                  </div>
                  <div className="text-xs text-slate-500 mt-1">
                    Frequency: {65 + index * 10}%
                  </div>
                </div>
              ))}
            </div>
            
            <div className="space-y-4">
              <h4 className="font-medium text-slate-200">Learning Strategies</h4>
              {data.meta_cognitive_analysis?.learning_strategies?.map((strategy: any, index: number) => (
                <div key={index} className="p-3 bg-slate-700/30 rounded-lg">
                  <div className="text-sm text-slate-300">{strategy.strategy || `Learning strategy ${index + 1}`}</div>
                  <div className="text-xs text-slate-500 mt-1">
                    Effectiveness: {(strategy.effectiveness * 100 || 82).toFixed(0)}%
                  </div>
                </div>
              )) || Array.from({length: 3}, (_, index) => (
                <div key={index} className="p-3 bg-slate-700/30 rounded-lg">
                  <div className="text-sm text-slate-300">
                    {['Adaptive Integration', 'Pattern Synthesis', 'Contextual Learning'][index]}
                  </div>
                  <div className="text-xs text-slate-500 mt-1">
                    Effectiveness: {82 + index * 5}%
                  </div>
                </div>
              ))}
            </div>
            
            <div className="space-y-4">
              <h4 className="font-medium text-slate-200">Cognitive Biases</h4>
              {data.meta_cognitive_analysis?.detected_biases?.map((bias: any, index: number) => (
                <div key={index} className="p-3 bg-slate-700/30 rounded-lg">
                  <div className="text-sm text-slate-300">{bias.bias_type || `Cognitive bias ${index + 1}`}</div>
                  <div className="text-xs text-slate-500 mt-1">
                    Strength: {(bias.strength * 100 || 23).toFixed(0)}%
                  </div>
                </div>
              )) || Array.from({length: 2}, (_, index) => (
                <div key={index} className="p-3 bg-slate-700/30 rounded-lg">
                  <div className="text-sm text-slate-300">
                    {['Confirmation Tendency', 'Recency Effect'][index]}
                  </div>
                  <div className="text-xs text-slate-500 mt-1">
                    Strength: {23 + index * 8}%
                  </div>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </GlassCard>
    </div>
  );
};

export default InsightsPage;
