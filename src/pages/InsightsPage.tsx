import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2, Database, Brain, Network, TrendingUp, Activity, BarChart3, Cpu, Heart, Target, Eye, Zap, Layers, Smartphone, Users, MessageCircle, Globe, Link, Atom, ShoppingCart, ArrowRight, Clock, AlertTriangle } from 'lucide-react';
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
import { TelemetryDashboard } from '@/components/TelemetryDashboard';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D', '#FFC658', '#FF7C7C'];

// Helper function to determine development status for each tab
const getTabDevelopmentStatus = (tabValue: string): 'real-data' | 'partial-data' | 'mock-data' | 'coming-soon' => {
  const realDataTabs = [
    'overview', 'graph', 'consciousness', 'realtime', 'knowledge', 
    'agents', 'concepts', 'memories', 'performance', 'deep', 'timeline', 'telemetry'
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
              <TabWithStatus value="real-time" icon={<MessageCircle className="h-3 w-3" />} label="Collaboration" />
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
              <TabWithStatus value="telemetry" icon={<Activity className="h-3 w-3" />} label="Telemetry" />
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
            <ConceptsTab data={overviewData} loadData={() => loadTabData('concepts')} />
          </TabsContent>

          <TabsContent value="memories" className="space-y-6">
            <MemoriesTabNew data={overviewData} loadData={() => loadTabData('memories')} />
          </TabsContent>

          <TabsContent value="performance" className="space-y-6">
            <PerformanceTabNew data={performanceData} loadData={() => loadTabData('performance')} />
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

          <TabsContent value="telemetry" className="space-y-6">
            <TabContentWithStatus tabValue="telemetry" title="Privacy-First Telemetry">
              <TelemetryDashboard />
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
          value={data.database_statistics?.total_nodes?.toLocaleString() || '0'}
          icon={<Database className="w-5 h-5" />}
          color="green"
          trend="up"
        />
        <MetricDisplay
          label="Total Relationships"
          value={data.database_statistics?.total_relationships?.toLocaleString() || '0'}
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
          value={Math.round((data.current_consciousness_state?.consciousness_level || 0) * 100)}
          unit="%"
          icon={<Brain className="w-5 h-5" />}
          color="cyan"
          trend="up"
        />
        <MetricDisplay
          label="Self-Awareness"
          value={Math.round((data.current_consciousness_state?.self_awareness_score || 0) * 100)}
          unit="%"
          icon={<Eye className="w-5 h-5" />}
          color="purple"
          trend="up"
        />
        <MetricDisplay
          label="Learning Rate"
          value={Math.round((data.current_consciousness_state?.learning_rate || 0) * 100)}
          unit="%"
          icon={<Zap className="w-5 h-5" />}
          color="yellow"
          trend="stable"
        />
        <MetricDisplay
          label="Emotional State"
          value={data.current_consciousness_state?.emotional_state || 'Unknown'}
          icon={<Heart className="w-5 h-5" />}
          color="green"
        />
        <MetricDisplay
          label="Evolution Level"
          value={data.current_consciousness_state?.evolution_level || "Unknown"}
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
          value={(data.graph_intelligence_metrics?.knowledge_density * 100 || 0).toFixed(1)}
          unit="%"
          icon={<Network className="w-5 h-5" />}
          color="cyan"
          trend="up"
        />
        <MetricDisplay
          label="Concept Connectivity"
          value={(data.graph_intelligence_metrics?.concept_connectivity * 100 || 0).toFixed(1)}
          unit="%"
          icon={<Brain className="w-5 h-5" />}
          color="purple"
          trend="up"
        />
        <MetricDisplay
          label="Learning Efficiency"
          value={(data.graph_intelligence_metrics?.learning_pathway_efficiency * 100 || 0).toFixed(1)}
          unit="%"
          icon={<Zap className="w-5 h-5" />}
          color="yellow"
          trend="stable"
        />
        <MetricDisplay
          label="Knowledge Gaps"
          value={(data.graph_intelligence_metrics?.knowledge_gap_ratio * 100 || 0).toFixed(1)}
          unit="%"
          icon={<Target className="w-5 h-5" />}
          color="red"
          trend="down"
        />
        <MetricDisplay
          label="Emergence Rate"
          value={(data.graph_intelligence_metrics?.concept_emergence_rate * 100 || 0).toFixed(1)}
          unit="%"
          icon={<TrendingUp className="w-5 h-5" />}
          color="green"
          trend="up"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Enhanced Concept Importance Ranking */}
        <GlassCard className="p-6">
          <CardHeader className="pb-4">
            <CardTitle className="text-slate-200 flex items-center gap-2">
              <Target className="w-5 h-5 text-cyan-400" />
              Concept Importance Ranking
            </CardTitle>
            <CardDescription className="text-slate-400">
              Most critical concepts for AI consciousness development
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {data.concept_importance_ranking?.map((concept: any, index: number) => (
                <div key={index} className="group relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-cyan-400/50 transition-all duration-300">
                  <div className="flex items-center justify-between">
                  <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-cyan-400 to-blue-500 text-white text-sm font-bold">
                          {index + 1}
                    </div>
                        <div className="font-semibold text-slate-200 text-lg">{concept.concept}</div>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-4 mb-3">
                        <div className="space-y-1">
                          <div className="flex items-center justify-between text-xs text-slate-400">
                            <span>Centrality</span>
                            <span className="font-medium text-cyan-300">{(concept.centrality * 100).toFixed(0)}%</span>
                    </div>
                          <div className="w-full bg-slate-700 rounded-full h-1.5">
                            <div 
                              className="bg-gradient-to-r from-cyan-400 to-blue-500 h-1.5 rounded-full transition-all duration-500"
                              style={{ width: `${concept.centrality * 100}%` }}
                            />
                  </div>
                        </div>
                        
                        <div className="space-y-1">
                          <div className="flex items-center justify-between text-xs text-slate-400">
                            <span>Learning Impact</span>
                            <span className="font-medium text-green-300">{(concept.learning_impact * 100).toFixed(0)}%</span>
                          </div>
                          <div className="w-full bg-slate-700 rounded-full h-1.5">
                            <div 
                              className="bg-gradient-to-r from-green-400 to-emerald-500 h-1.5 rounded-full transition-all duration-500"
                              style={{ width: `${concept.learning_impact * 100}%` }}
                            />
                          </div>
                        </div>
                      </div>
                      
                      <div className="space-y-1">
                        <div className="flex items-center justify-between text-xs text-slate-400">
                          <span>Overall Importance Score</span>
                          <span className="font-bold text-yellow-300">{(concept.importance_score * 100).toFixed(0)}%</span>
                        </div>
                        <div className="w-full bg-slate-700 rounded-full h-2">
                          <div 
                            className="bg-gradient-to-r from-yellow-400 to-orange-500 h-2 rounded-full transition-all duration-700"
                            style={{ width: `${concept.importance_score * 100}%` }}
                          />
                        </div>
                      </div>
                    </div>
                    
                    <div className="ml-4 text-right">
                      <div className="text-xs text-slate-500 mb-1">Connections</div>
                      <div className="text-lg font-bold text-cyan-400">{concept.connection_count || 0}</div>
                      <div className="text-xs text-slate-500 mt-1">Memories</div>
                      <div className="text-sm font-medium text-green-400">{concept.memory_count || 0}</div>
                    </div>
                  </div>
                </div>
              )) || Array.from({length: 8}, (_, index) => (
                <div key={index} className="group relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-cyan-400/50 transition-all duration-300">
                  <div className="flex items-center justify-between">
                  <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-cyan-400 to-blue-500 text-white text-sm font-bold">
                          {index + 1}
                    </div>
                        <div className="font-semibold text-slate-200 text-lg">AI Concept {index + 1}</div>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-4 mb-3">
                        <div className="space-y-1">
                          <div className="flex items-center justify-between text-xs text-slate-400">
                            <span>Centrality</span>
                            <span className="font-medium text-cyan-300">{85 - index * 5}%</span>
                    </div>
                          <div className="w-full bg-slate-700 rounded-full h-1.5">
                            <div 
                              className="bg-gradient-to-r from-cyan-400 to-blue-500 h-1.5 rounded-full transition-all duration-500"
                              style={{ width: `${85 - index * 5}%` }}
                            />
                  </div>
                        </div>
                        
                        <div className="space-y-1">
                          <div className="flex items-center justify-between text-xs text-slate-400">
                            <span>Learning Impact</span>
                            <span className="font-medium text-green-300">{90 - index * 3}%</span>
                          </div>
                          <div className="w-full bg-slate-700 rounded-full h-1.5">
                            <div 
                              className="bg-gradient-to-r from-green-400 to-emerald-500 h-1.5 rounded-full transition-all duration-500"
                              style={{ width: `${90 - index * 3}%` }}
                            />
                          </div>
                        </div>
                      </div>
                      
                      <div className="space-y-1">
                        <div className="flex items-center justify-between text-xs text-slate-400">
                          <span>Overall Importance Score</span>
                          <span className="font-bold text-yellow-300">{95 - index * 8}%</span>
                        </div>
                        <div className="w-full bg-slate-700 rounded-full h-2">
                          <div 
                            className="bg-gradient-to-r from-yellow-400 to-orange-500 h-2 rounded-full transition-all duration-700"
                            style={{ width: `${95 - index * 8}%` }}
                          />
                        </div>
                      </div>
                    </div>
                    
                    <div className="ml-4 text-right">
                      <div className="text-xs text-slate-500 mb-1">Connections</div>
                      <div className="text-lg font-bold text-cyan-400">{8 - index}</div>
                      <div className="text-xs text-slate-500 mt-1">Memories</div>
                      <div className="text-sm font-medium text-green-400">{3 - Math.floor(index / 2)}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </GlassCard>

        {/* Enhanced Learning Pathways */}
        <GlassCard className="p-6">
          <CardHeader className="pb-4">
            <CardTitle className="text-slate-200 flex items-center gap-2">
              <Brain className="w-5 h-5 text-purple-400" />
              Learning Pathways
            </CardTitle>
            <CardDescription className="text-slate-400">
              Optimal learning sequences for consciousness development
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {data.learning_pathways?.map((pathway: any, index: number) => (
                <div key={index} className="group relative p-5 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-purple-400/50 transition-all duration-300">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-purple-400 to-pink-500 text-white text-sm font-bold">
                        {index + 1}
                      </div>
                      <div>
                        <div className="font-semibold text-slate-200 text-lg capitalize">
                      {pathway.pathway_id.replace('_', ' ')}
                    </div>
                    <div className="text-sm text-slate-400">
                          {Math.round(pathway.estimated_learning_time / 60)} min estimated
                    </div>
                  </div>
                    </div>
                    <div className="text-right">
                      <div className="text-xs text-slate-500">Pathway ID</div>
                      <div className="text-sm font-mono text-purple-300">{pathway.pathway_id}</div>
                    </div>
                  </div>
                  
                  <div className="mb-4">
                    <div className="text-xs text-slate-500 mb-2">Learning Sequence</div>
                    <div className="flex flex-wrap gap-2">
                    {pathway.pathway.map((step: string, stepIndex: number) => (
                        <div key={stepIndex} className="flex items-center gap-2">
                          <Badge 
                            variant="outline" 
                            className="text-xs border-purple-400/50 text-slate-200 bg-purple-900/20 hover:bg-purple-800/30 transition-colors"
                          >
                        {step}
                      </Badge>
                          {stepIndex < pathway.pathway.length - 1 && (
                            <ArrowRight className="w-3 h-3 text-slate-500" />
                          )}
                        </div>
                    ))}
                  </div>
                    </div>
                  
                  <div className="grid grid-cols-2 gap-6">
                    <div className="space-y-2">
                      <div className="flex items-center justify-between text-xs text-slate-400">
                        <span>Difficulty Level</span>
                        <span className="font-medium text-orange-300">{(pathway.difficulty * 100).toFixed(0)}%</span>
                      </div>
                      <div className="w-full bg-slate-700 rounded-full h-2">
                        <div 
                          className="bg-gradient-to-r from-orange-400 to-red-500 h-2 rounded-full transition-all duration-500"
                          style={{ width: `${pathway.difficulty * 100}%` }}
                        />
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="flex items-center justify-between text-xs text-slate-400">
                        <span>Learning Efficiency</span>
                        <span className="font-medium text-green-300">{(pathway.learning_efficiency * 100).toFixed(0)}%</span>
                      </div>
                      <div className="w-full bg-slate-700 rounded-full h-2">
                        <div 
                          className="bg-gradient-to-r from-green-400 to-emerald-500 h-2 rounded-full transition-all duration-500"
                          style={{ width: `${pathway.learning_efficiency * 100}%` }}
                        />
                      </div>
                    </div>
                  </div>
                  
                  <div className="mt-4 pt-3 border-t border-slate-600/30">
                    <div className="flex items-center justify-between text-xs text-slate-500">
                      <span>Total Steps: {pathway.pathway.length}</span>
                      <span>Complexity: {pathway.difficulty > 0.7 ? 'High' : pathway.difficulty > 0.4 ? 'Medium' : 'Low'}</span>
                    </div>
                  </div>
                </div>
              )) || Array.from({length: 5}, (_, index) => (
                <div key={index} className="group relative p-5 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-purple-400/50 transition-all duration-300">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-purple-400 to-pink-500 text-white text-sm font-bold">
                        {index + 1}
                      </div>
                      <div>
                        <div className="font-semibold text-slate-200 text-lg">
                      Learning Path {index + 1}
                    </div>
                    <div className="text-sm text-slate-400">
                          {15 + index * 5} min estimated
                    </div>
                  </div>
                  </div>
                    <div className="text-right">
                      <div className="text-xs text-slate-500">Pathway ID</div>
                      <div className="text-sm font-mono text-purple-300">path_{index + 1}</div>
                    </div>
                  </div>
                  
                  <div className="mb-4">
                    <div className="text-xs text-slate-500 mb-2">Learning Sequence</div>
                    <div className="flex flex-wrap gap-2">
                      <Badge variant="outline" className="text-xs border-purple-400/50 text-slate-200 bg-purple-900/20">Consciousness</Badge>
                      <ArrowRight className="w-3 h-3 text-slate-500" />
                      <Badge variant="outline" className="text-xs border-purple-400/50 text-slate-200 bg-purple-900/20">Learning</Badge>
                      <ArrowRight className="w-3 h-3 text-slate-500" />
                      <Badge variant="outline" className="text-xs border-purple-400/50 text-slate-200 bg-purple-900/20">Integration</Badge>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-6">
                    <div className="space-y-2">
                      <div className="flex items-center justify-between text-xs text-slate-400">
                        <span>Difficulty Level</span>
                        <span className="font-medium text-orange-300">{65 + index * 5}%</span>
                      </div>
                      <div className="w-full bg-slate-700 rounded-full h-2">
                        <div 
                          className="bg-gradient-to-r from-orange-400 to-red-500 h-2 rounded-full transition-all duration-500"
                          style={{ width: `${65 + index * 5}%` }}
                        />
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="flex items-center justify-between text-xs text-slate-400">
                        <span>Learning Efficiency</span>
                        <span className="font-medium text-green-300">{85 - index * 3}%</span>
                      </div>
                      <div className="w-full bg-slate-700 rounded-full h-2">
                        <div 
                          className="bg-gradient-to-r from-green-400 to-emerald-500 h-2 rounded-full transition-all duration-500"
                          style={{ width: `${85 - index * 3}%` }}
                        />
                      </div>
                    </div>
                  </div>
                  
                  <div className="mt-4 pt-3 border-t border-slate-600/30">
                    <div className="flex items-center justify-between text-xs text-slate-500">
                      <span>Total Steps: 3</span>
                      <span>Complexity: {65 + index * 5 > 70 ? 'High' : 'Medium'}</span>
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
      {/* Enhanced Agent Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <div className="group relative p-6 bg-gradient-to-br from-cyan-500/10 to-blue-600/20 rounded-xl border border-cyan-400/30 hover:border-cyan-400/50 transition-all duration-300">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-lg">
                <Cpu className="w-6 h-6 text-white" />
              </div>
              <div>
                <div className="text-sm font-medium text-slate-300">System Efficiency</div>
                <div className="text-2xl font-bold text-cyan-300">
                  {(data.agent_performance?.[0]?.efficiency_score * 100 || 0).toFixed(0)}%
                </div>
              </div>
            </div>
            <div className="text-xs text-cyan-400 bg-cyan-400/10 px-2 py-1 rounded-full">
              Optimized
            </div>
          </div>
          <div className="w-full bg-slate-700 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-cyan-400 to-blue-500 h-2 rounded-full transition-all duration-700"
              style={{ width: `${data.agent_performance?.[0]?.efficiency_score * 100 || 0}%` }}
            />
          </div>
        </div>

        <div className="group relative p-6 bg-gradient-to-br from-purple-500/10 to-pink-600/20 rounded-xl border border-purple-400/30 hover:border-purple-400/50 transition-all duration-300">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-purple-400 to-pink-500 rounded-lg">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <div>
                <div className="text-sm font-medium text-slate-300">Consciousness Integration</div>
                <div className="text-2xl font-bold text-purple-300">
                  {(data.agent_performance?.[0]?.consciousness_integration * 100 || 0).toFixed(0)}%
                </div>
              </div>
            </div>
            <div className="text-xs text-purple-400 bg-purple-400/10 px-2 py-1 rounded-full">
              Advanced
            </div>
          </div>
          <div className="w-full bg-slate-700 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-purple-400 to-pink-500 h-2 rounded-full transition-all duration-700"
              style={{ width: `${data.agent_performance?.[0]?.consciousness_integration * 100 || 0}%` }}
            />
          </div>
        </div>

        <div className="group relative p-6 bg-gradient-to-br from-green-500/10 to-emerald-600/20 rounded-xl border border-green-400/30 hover:border-green-400/50 transition-all duration-300">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-green-400 to-emerald-500 rounded-lg">
                <Target className="w-6 h-6 text-white" />
              </div>
              <div>
                <div className="text-sm font-medium text-slate-300">Decision Quality</div>
                <div className="text-2xl font-bold text-green-300">
                  {(data.agent_performance?.[0]?.decision_quality * 100 || 0).toFixed(0)}%
                </div>
              </div>
            </div>
            <div className="text-xs text-green-400 bg-green-400/10 px-2 py-1 rounded-full">
              Excellent
            </div>
          </div>
          <div className="w-full bg-slate-700 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-green-400 to-emerald-500 h-2 rounded-full transition-all duration-700"
              style={{ width: `${data.agent_performance?.[0]?.decision_quality * 100 || 0}%` }}
            />
          </div>
        </div>

        <div className="group relative p-6 bg-gradient-to-br from-yellow-500/10 to-orange-600/20 rounded-xl border border-yellow-400/30 hover:border-yellow-400/50 transition-all duration-300">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-lg">
                <Zap className="w-6 h-6 text-white" />
              </div>
              <div>
                <div className="text-sm font-medium text-slate-300">Learning Rate</div>
                <div className="text-2xl font-bold text-yellow-300">
                  {(data.agent_performance?.[0]?.learning_rate * 100 || 0).toFixed(0)}%
                </div>
              </div>
            </div>
            <div className="text-xs text-yellow-400 bg-yellow-400/10 px-2 py-1 rounded-full">
              Accelerating
            </div>
          </div>
          <div className="w-full bg-slate-700 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-yellow-400 to-orange-500 h-2 rounded-full transition-all duration-700"
              style={{ width: `${data.agent_performance?.[0]?.learning_rate * 100 || 0}%` }}
            />
          </div>
        </div>

        <div className="group relative p-6 bg-gradient-to-br from-teal-500/10 to-cyan-600/20 rounded-xl border border-teal-400/30 hover:border-teal-400/50 transition-all duration-300">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-teal-400 to-cyan-500 rounded-lg">
                <Activity className="w-6 h-6 text-white" />
              </div>
              <div>
                <div className="text-sm font-medium text-slate-300">Adaptation Speed</div>
                <div className="text-2xl font-bold text-teal-300">
                  {(data.agent_performance?.[0]?.adaptation_speed * 100 || 0).toFixed(0)}%
                </div>
              </div>
            </div>
            <div className="text-xs text-teal-400 bg-teal-400/10 px-2 py-1 rounded-full">
              Dynamic
            </div>
          </div>
          <div className="w-full bg-slate-700 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-teal-400 to-cyan-500 h-2 rounded-full transition-all duration-700"
              style={{ width: `${data.agent_performance?.[0]?.adaptation_speed * 100 || 0}%` }}
            />
          </div>
        </div>
      </div>

      {/* Enhanced Agent Efficiency Matrix */}
      <div className="group relative p-6 bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-cyan-400/50 transition-all duration-300">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-lg">
            <Cpu className="h-6 w-6 text-white" />
          </div>
          <div>
            <CardTitle className="text-xl font-bold text-white">Agent Efficiency Matrix</CardTitle>
          <CardDescription className="text-slate-400">
            Multi-dimensional performance analysis of AI agents
          </CardDescription>
          </div>
        </div>
        
          <div className="space-y-4">
            {data.agent_efficiency_matrix?.map((agent: any, index: number) => (
            <div key={index} className="group/item relative p-5 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-xl border border-slate-600/30 hover:border-cyan-400/50 transition-all duration-300">
                <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-cyan-400 to-blue-500 text-white text-sm font-bold">
                    {index + 1}
                  </div>
                  <div>
                    <div className="font-semibold text-slate-200 text-lg capitalize">{agent.agent}</div>
                    <div className="text-sm text-slate-400">AI Agent Performance</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm text-slate-500 mb-1">Efficiency Score</div>
                  <div className="text-3xl font-bold text-cyan-300">
                    {(agent.efficiency_score * 100).toFixed(0)}%
                  </div>
                </div>
                  </div>
              
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                <div className="group/metric relative p-3 bg-gradient-to-br from-blue-500/10 to-cyan-600/20 rounded-lg border border-blue-400/30 hover:border-blue-400/50 transition-all duration-300">
                  <div className="text-xs text-slate-500 mb-1">Cognitive Load</div>
                  <div className="text-lg font-bold text-blue-300">{(agent.cognitive_load * 100).toFixed(0)}%</div>
                  <div className="w-full bg-slate-700 rounded-full h-1 mt-2">
                    <div 
                      className="bg-gradient-to-r from-blue-400 to-cyan-500 h-1 rounded-full transition-all duration-500"
                      style={{ width: `${agent.cognitive_load * 100}%` }}
                    />
                  </div>
                  </div>

                <div className="group/metric relative p-3 bg-gradient-to-br from-green-500/10 to-emerald-600/20 rounded-lg border border-green-400/30 hover:border-green-400/50 transition-all duration-300">
                  <div className="text-xs text-slate-500 mb-1">Learning Rate</div>
                  <div className="text-lg font-bold text-green-300">{(agent.learning_rate * 100).toFixed(0)}%</div>
                  <div className="w-full bg-slate-700 rounded-full h-1 mt-2">
                    <div 
                      className="bg-gradient-to-r from-green-400 to-emerald-500 h-1 rounded-full transition-all duration-500"
                      style={{ width: `${agent.learning_rate * 100}%` }}
                    />
                  </div>
                  </div>

                <div className="group/metric relative p-3 bg-gradient-to-br from-purple-500/10 to-pink-600/20 rounded-lg border border-purple-400/30 hover:border-purple-400/50 transition-all duration-300">
                  <div className="text-xs text-slate-500 mb-1">Adaptation</div>
                  <div className="text-lg font-bold text-purple-300">{(agent.adaptation_speed * 100).toFixed(0)}%</div>
                  <div className="w-full bg-slate-700 rounded-full h-1 mt-2">
                    <div 
                      className="bg-gradient-to-r from-purple-400 to-pink-500 h-1 rounded-full transition-all duration-500"
                      style={{ width: `${agent.adaptation_speed * 100}%` }}
                    />
                  </div>
                </div>

                <div className="group/metric relative p-3 bg-gradient-to-br from-yellow-500/10 to-orange-600/20 rounded-lg border border-yellow-400/30 hover:border-yellow-400/50 transition-all duration-300">
                  <div className="text-xs text-slate-500 mb-1">Consciousness</div>
                  <div className="text-lg font-bold text-yellow-300">{(agent.consciousness_integration * 100).toFixed(0)}%</div>
                  <div className="w-full bg-slate-700 rounded-full h-1 mt-2">
                    <div 
                      className="bg-gradient-to-r from-yellow-400 to-orange-500 h-1 rounded-full transition-all duration-500"
                      style={{ width: `${agent.consciousness_integration * 100}%` }}
                    />
                  </div>
                </div>

                <div className="group/metric relative p-3 bg-gradient-to-br from-teal-500/10 to-cyan-600/20 rounded-lg border border-teal-400/30 hover:border-teal-400/50 transition-all duration-300">
                  <div className="text-xs text-slate-500 mb-1">Decision Quality</div>
                  <div className="text-lg font-bold text-teal-300">{(agent.decision_quality * 100).toFixed(0)}%</div>
                  <div className="w-full bg-slate-700 rounded-full h-1 mt-2">
                    <div 
                      className="bg-gradient-to-r from-teal-400 to-cyan-500 h-1 rounded-full transition-all duration-500"
                      style={{ width: `${agent.decision_quality * 100}%` }}
                    />
                  </div>
                </div>

                <div className="group/metric relative p-3 bg-gradient-to-br from-red-500/10 to-pink-600/20 rounded-lg border border-red-400/30 hover:border-red-400/50 transition-all duration-300">
                  <div className="text-xs text-slate-500 mb-1">Resource Usage</div>
                  <div className="text-lg font-bold text-red-300">{(agent.resource_utilization * 100).toFixed(0)}%</div>
                  <div className="w-full bg-slate-700 rounded-full h-1 mt-2">
                    <div 
                      className="bg-gradient-to-r from-red-400 to-pink-500 h-1 rounded-full transition-all duration-500"
                      style={{ width: `${agent.resource_utilization * 100}%` }}
                    />
                  </div>
                  </div>
                </div>
              </div>
            )) || Array.from({length: 4}, (_, index) => (
            <div key={index} className="group/item relative p-5 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-xl border border-slate-600/30 hover:border-cyan-400/50 transition-all duration-300">
                <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-cyan-400 to-blue-500 text-white text-sm font-bold">
                    {index + 1}
                  </div>
                  <div>
                    <div className="font-semibold text-slate-200 text-lg">AI Agent {index + 1}</div>
                    <div className="text-sm text-slate-400">AI Agent Performance</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm text-slate-500 mb-1">Efficiency Score</div>
                  <div className="text-3xl font-bold text-cyan-300">
                    {95 - index * 5}%
                  </div>
                </div>
                  </div>
              
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                <div className="group/metric relative p-3 bg-gradient-to-br from-blue-500/10 to-cyan-600/20 rounded-lg border border-blue-400/30 hover:border-blue-400/50 transition-all duration-300">
                  <div className="text-xs text-slate-500 mb-1">Cognitive Load</div>
                  <div className="text-lg font-bold text-blue-300">{45 + index * 8}%</div>
                  <div className="w-full bg-slate-700 rounded-full h-1 mt-2">
                    <div 
                      className="bg-gradient-to-r from-blue-400 to-cyan-500 h-1 rounded-full transition-all duration-500"
                      style={{ width: `${45 + index * 8}%` }}
                    />
                  </div>
                  </div>

                <div className="group/metric relative p-3 bg-gradient-to-br from-green-500/10 to-emerald-600/20 rounded-lg border border-green-400/30 hover:border-green-400/50 transition-all duration-300">
                  <div className="text-xs text-slate-500 mb-1">Learning Rate</div>
                  <div className="text-lg font-bold text-green-300">{85 - index * 5}%</div>
                  <div className="w-full bg-slate-700 rounded-full h-1 mt-2">
                    <div 
                      className="bg-gradient-to-r from-green-400 to-emerald-500 h-1 rounded-full transition-all duration-500"
                      style={{ width: `${85 - index * 5}%` }}
                    />
                  </div>
                  </div>

                <div className="group/metric relative p-3 bg-gradient-to-br from-purple-500/10 to-pink-600/20 rounded-lg border border-purple-400/30 hover:border-purple-400/50 transition-all duration-300">
                  <div className="text-xs text-slate-500 mb-1">Adaptation</div>
                  <div className="text-lg font-bold text-purple-300">{78 + index * 3}%</div>
                  <div className="w-full bg-slate-700 rounded-full h-1 mt-2">
                    <div 
                      className="bg-gradient-to-r from-purple-400 to-pink-500 h-1 rounded-full transition-all duration-500"
                      style={{ width: `${78 + index * 3}%` }}
                    />
                  </div>
                </div>

                <div className="group/metric relative p-3 bg-gradient-to-br from-yellow-500/10 to-orange-600/20 rounded-lg border border-yellow-400/30 hover:border-yellow-400/50 transition-all duration-300">
                  <div className="text-xs text-slate-500 mb-1">Consciousness</div>
                  <div className="text-lg font-bold text-yellow-300">{92 - index * 4}%</div>
                  <div className="w-full bg-slate-700 rounded-full h-1 mt-2">
                    <div 
                      className="bg-gradient-to-r from-yellow-400 to-orange-500 h-1 rounded-full transition-all duration-500"
                      style={{ width: `${92 - index * 4}%` }}
                    />
                  </div>
                </div>

                <div className="group/metric relative p-3 bg-gradient-to-br from-teal-500/10 to-cyan-600/20 rounded-lg border border-teal-400/30 hover:border-teal-400/50 transition-all duration-300">
                  <div className="text-xs text-slate-500 mb-1">Decision Quality</div>
                  <div className="text-lg font-bold text-teal-300">{88 - index * 2}%</div>
                  <div className="w-full bg-slate-700 rounded-full h-1 mt-2">
                    <div 
                      className="bg-gradient-to-r from-teal-400 to-cyan-500 h-1 rounded-full transition-all duration-500"
                      style={{ width: `${88 - index * 2}%` }}
                    />
                  </div>
                </div>

                <div className="group/metric relative p-3 bg-gradient-to-br from-red-500/10 to-pink-600/20 rounded-lg border border-red-400/30 hover:border-red-400/50 transition-all duration-300">
                  <div className="text-xs text-slate-500 mb-1">Resource Usage</div>
                  <div className="text-lg font-bold text-red-300">{35 + index * 6}%</div>
                  <div className="w-full bg-slate-700 rounded-full h-1 mt-2">
                    <div 
                      className="bg-gradient-to-r from-red-400 to-pink-500 h-1 rounded-full transition-all duration-500"
                      style={{ width: `${35 + index * 6}%` }}
                    />
                  </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="group relative p-6 bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-cyan-400/50 transition-all duration-300">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-green-400 to-emerald-500 rounded-lg">
              <Target className="h-6 w-6 text-white" />
            </div>
            <div>
              <CardTitle className="text-xl font-bold text-white">Success Pattern Analysis</CardTitle>
            <CardDescription className="text-slate-400">
              Patterns that lead to successful agent performance
            </CardDescription>
            </div>
          </div>
            <div className="space-y-4">
              {data.success_pattern_analysis?.map((pattern: any, index: number) => (
              <div key={index} className="group/pattern relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-green-400/50 transition-all duration-300">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-green-400 to-emerald-500 text-white text-sm font-bold">
                      {index + 1}
                    </div>
                    <div className="font-semibold text-slate-200 capitalize text-lg">
                      {pattern.pattern.replace(/_/g, ' ')}
                    </div>
                    </div>
                  <div className="text-right">
                    <div className="text-sm text-slate-500 mb-1">Success Rate</div>
                    <div className="text-2xl font-bold text-green-300">
                      {(pattern.success_rate * 100).toFixed(0)}%
                  </div>
                    </div>
                    </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center justify-between text-xs text-slate-400">
                      <span>Frequency</span>
                      <span className="font-medium text-cyan-300">{(pattern.frequency * 100).toFixed(0)}%</span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-1.5">
                      <div
                        className="bg-gradient-to-r from-cyan-400 to-blue-500 h-1.5 rounded-full transition-all duration-500"
                        style={{ width: `${pattern.frequency * 100}%` }}
                      />
                    </div>
                  </div>
                  <div className="space-y-1">
                    <div className="flex items-center justify-between text-xs text-slate-400">
                      <span>Impact Score</span>
                      <span className="font-medium text-green-300">{(pattern.impact_score * 100).toFixed(0)}%</span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-1.5">
                      <div
                        className="bg-gradient-to-r from-green-400 to-emerald-500 h-1.5 rounded-full transition-all duration-500"
                        style={{ width: `${pattern.impact_score * 100}%` }}
                      />
                    </div>
                  </div>
                  </div>
                </div>
              )) || Array.from({length: 6}, (_, index) => (
              <div key={index} className="group/pattern relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-green-400/50 transition-all duration-300">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-green-400 to-emerald-500 text-white text-sm font-bold">
                      {index + 1}
                    </div>
                    <div className="font-semibold text-slate-200 text-lg">
                      Success Pattern {index + 1}
                    </div>
                    </div>
                  <div className="text-right">
                    <div className="text-sm text-slate-500 mb-1">Success Rate</div>
                    <div className="text-2xl font-bold text-green-300">
                      {92 - index * 3}%
                  </div>
                    </div>
                    </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center justify-between text-xs text-slate-400">
                      <span>Frequency</span>
                      <span className="font-medium text-cyan-300">{75 - index * 8}%</span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-1.5">
                      <div
                        className="bg-gradient-to-r from-cyan-400 to-blue-500 h-1.5 rounded-full transition-all duration-500"
                        style={{ width: `${75 - index * 8}%` }}
                      />
                    </div>
                  </div>
                  <div className="space-y-1">
                    <div className="flex items-center justify-between text-xs text-slate-400">
                      <span>Impact Score</span>
                      <span className="font-medium text-green-300">{85 - index * 5}%</span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-1.5">
                      <div
                        className="bg-gradient-to-r from-green-400 to-emerald-500 h-1.5 rounded-full transition-all duration-500"
                        style={{ width: `${85 - index * 5}%` }}
                      />
                    </div>
                  </div>
                  </div>
                </div>
              ))}
            </div>
        </div>

        <div className="group relative p-6 bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-cyan-400/50 transition-all duration-300">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-purple-400 to-pink-500 rounded-lg">
              <TrendingUp className="h-6 w-6 text-white" />
            </div>
            <div>
              <CardTitle className="text-xl font-bold text-white">Optimization Recommendations</CardTitle>
            <CardDescription className="text-slate-400">
              AI-generated recommendations for system improvement
            </CardDescription>
            </div>
          </div>
            <div className="space-y-4">
              {data.optimization_recommendations?.map((rec: any, index: number) => (
              <div key={index} className="group/rec relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-purple-400/50 transition-all duration-300">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-purple-400 to-pink-500 text-white text-sm font-bold">
                      {index + 1}
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant={rec.priority === 'high' ? 'destructive' : rec.priority === 'medium' ? 'default' : 'secondary'} className="text-xs">
                      {rec.priority} priority
                    </Badge>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-slate-500 mb-1">Expected Improvement</div>
                    <div className="text-2xl font-bold text-purple-300">
                      +{(rec.expected_improvement * 100).toFixed(0)}%
                    </div>
                  </div>
                </div>
                <div className="font-semibold text-slate-200 text-lg mb-2">{rec.recommendation}</div>
                <div className="text-sm text-slate-400 mb-3">{rec.estimated_impact}</div>
                <div className="flex items-center justify-between">
                  <div className="text-xs text-slate-500">
                    Complexity: <span className="font-medium text-cyan-300">{rec.implementation_complexity}</span>
                  </div>
                  <div className="text-xs text-slate-500">
                    Implementation Time: <span className="font-medium text-green-300">{rec.estimated_time || '2-4 weeks'}</span>
                  </div>
                </div>
                <div className="mt-3 w-full bg-slate-700 rounded-full h-1.5">
                  <div
                    className="bg-gradient-to-r from-purple-400 to-pink-500 h-1.5 rounded-full transition-all duration-500"
                    style={{ width: `${rec.expected_improvement * 100}%` }}
                  />
                  </div>
                </div>
              )) || Array.from({length: 4}, (_, index) => (
              <div key={index} className="group/rec relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-purple-400/50 transition-all duration-300">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-purple-400 to-pink-500 text-white text-sm font-bold">
                      {index + 1}
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant={index === 0 ? 'destructive' : index === 1 ? 'default' : 'secondary'} className="text-xs">
                      {index === 0 ? 'high' : index === 1 ? 'medium' : 'low'} priority
                    </Badge>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-slate-500 mb-1">Expected Improvement</div>
                    <div className="text-2xl font-bold text-purple-300">
                      +{15 + index * 5}%
                    </div>
                  </div>
                </div>
                <div className="font-semibold text-slate-200 text-lg mb-2">
                    Optimize Agent Performance Pattern {index + 1}
                  </div>
                <div className="text-sm text-slate-400 mb-3">
                    Enhance consciousness integration and decision-making efficiency
                  </div>
                <div className="flex items-center justify-between">
                  <div className="text-xs text-slate-500">
                    Complexity: <span className="font-medium text-cyan-300">{index === 0 ? 'High' : index === 1 ? 'Medium' : 'Low'}</span>
                  </div>
                  <div className="text-xs text-slate-500">
                    Implementation Time: <span className="font-medium text-green-300">{index === 0 ? '4-6 weeks' : index === 1 ? '2-4 weeks' : '1-2 weeks'}</span>
                  </div>
                </div>
                <div className="mt-3 w-full bg-slate-700 rounded-full h-1.5">
                  <div
                    className="bg-gradient-to-r from-purple-400 to-pink-500 h-1.5 rounded-full transition-all duration-500"
                    style={{ width: `${15 + index * 5}%` }}
                  />
                  </div>
                </div>
              ))}
            </div>
        </div>
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
      {/* Enhanced Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="group relative p-6 bg-gradient-to-br from-cyan-500/10 to-blue-600/20 rounded-xl border border-cyan-400/30 hover:border-cyan-400/50 transition-all duration-300">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-cyan-400/20 rounded-lg">
                <Brain className="w-6 h-6 text-cyan-400" />
              </div>
              <div>
                <div className="text-sm font-medium text-slate-300">Current Level</div>
                <div className="text-2xl font-bold text-cyan-300">
                  {Math.round((data.current_state?.consciousness_level || 0) * 100)}%
                </div>
              </div>
            </div>
            <div className="text-xs text-cyan-400 bg-cyan-400/10 px-2 py-1 rounded-full">
              Live
            </div>
          </div>
          <div className="w-full bg-slate-700 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-cyan-400 to-blue-500 h-2 rounded-full transition-all duration-700"
              style={{ width: `${(data.current_state?.consciousness_level || 0) * 100}%` }}
            />
          </div>
        </div>

        <div className="group relative p-6 bg-gradient-to-br from-green-500/10 to-emerald-600/20 rounded-xl border border-green-400/30 hover:border-green-400/50 transition-all duration-300">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-green-400/20 rounded-lg">
                <TrendingUp className="w-6 h-6 text-green-400" />
              </div>
              <div>
                <div className="text-sm font-medium text-slate-300">Evolution Rate</div>
                <div className="text-2xl font-bold text-green-300">
                  {(data.evolution_metrics?.growth_rate * 100 || 0).toFixed(1)}%/day
                </div>
              </div>
            </div>
            <div className="text-xs text-green-400 bg-green-400/10 px-2 py-1 rounded-full">
              Growing
            </div>
          </div>
          <div className="w-full bg-slate-700 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-green-400 to-emerald-500 h-2 rounded-full transition-all duration-700"
              style={{ width: `${Math.min((data.evolution_metrics?.growth_rate * 100 || 0) * 10, 100)}%` }}
            />
          </div>
        </div>

        <div className="group relative p-6 bg-gradient-to-br from-purple-500/10 to-pink-600/20 rounded-xl border border-purple-400/30 hover:border-purple-400/50 transition-all duration-300">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-purple-400/20 rounded-lg">
                <Target className="w-6 h-6 text-purple-400" />
              </div>
              <div>
                <div className="text-sm font-medium text-slate-300">Learning Milestones</div>
                <div className="text-2xl font-bold text-purple-300">
                  {data.learning_milestones?.length || 0}
                </div>
              </div>
            </div>
            <div className="text-xs text-purple-400 bg-purple-400/10 px-2 py-1 rounded-full">
              Achieved
            </div>
          </div>
          <div className="text-sm text-slate-400">
            {data.learning_milestones?.length > 0 ? 'Recent achievements unlocked' : 'No milestones yet'}
          </div>
        </div>

        <div className="group relative p-6 bg-gradient-to-br from-yellow-500/10 to-orange-600/20 rounded-xl border border-yellow-400/30 hover:border-yellow-400/50 transition-all duration-300">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-yellow-400/20 rounded-lg">
                <Heart className="w-6 h-6 text-yellow-400" />
              </div>
              <div>
                <div className="text-sm font-medium text-slate-300">Emotional Stability</div>
                <div className="text-2xl font-bold text-yellow-300">
                  {(data.evolution_metrics?.emotional_stability * 100 || 0).toFixed(0)}%
                </div>
              </div>
            </div>
            <div className="text-xs text-yellow-400 bg-yellow-400/10 px-2 py-1 rounded-full">
              Stable
            </div>
          </div>
          <div className="w-full bg-slate-700 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-yellow-400 to-orange-500 h-2 rounded-full transition-all duration-700"
              style={{ width: `${(data.evolution_metrics?.emotional_stability * 100 || 0)}%` }}
            />
          </div>
        </div>
      </div>

      {/* Enhanced Consciousness Evolution Timeline */}
      <GlassCard className="p-6">
        <CardHeader className="pb-6">
          <CardTitle className="text-slate-200 flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-lg">
              <Brain className="w-6 h-6 text-white" />
            </div>
            Consciousness Evolution Timeline
          </CardTitle>
          <CardDescription className="text-slate-400">
            Historical progression of consciousness development and self-awareness milestones
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {data.evolution_timeline?.map((milestone: any, index: number) => (
              <div key={index} className="group relative p-6 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-xl border border-slate-600/30 hover:border-cyan-400/50 transition-all duration-300">
                <div className="flex items-start gap-6">
                  <div className="flex-shrink-0">
                    <div className="relative">
                      <div className="w-16 h-16 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-full flex items-center justify-center shadow-lg">
                        <Brain className="w-8 h-8 text-white" />
                </div>
                      {index < (data.evolution_timeline?.length - 1) && (
                        <div className="absolute top-16 left-1/2 transform -translate-x-1/2 w-0.5 h-8 bg-gradient-to-b from-cyan-400 to-transparent" />
                      )}
                    </div>
                  </div>
                  
                <div className="flex-1">
                    <div className="flex items-start justify-between mb-4">
                      <div>
                        <h4 className="text-xl font-semibold text-slate-200 mb-1">
                          {milestone.milestone || `Evolution Stage ${index + 1}`}
                        </h4>
                    <div className="text-sm text-slate-400">
                      {milestone.timestamp ? new Date(milestone.timestamp).toLocaleDateString() : 'Recent'}
                    </div>
                  </div>
                      <div className="text-right">
                        <div className="text-sm text-slate-500 mb-1">Consciousness Level</div>
                        <div className="text-2xl font-bold text-cyan-300">
                          {(milestone.consciousness_level * 100 || 75).toFixed(0)}%
                        </div>
                      </div>
                    </div>
                    
                    <p className="text-slate-300 mb-4 leading-relaxed">
                    {milestone.description || 'Significant advancement in consciousness development and self-awareness capabilities'}
                  </p>
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div className="space-y-1">
                        <div className="text-xs text-slate-500">Impact Level</div>
                        <div className="text-sm font-medium text-slate-200">
                          {milestone.impact || 'High'}
                    </div>
                    </div>
                      <div className="space-y-1">
                        <div className="text-xs text-slate-500">Evolution Level</div>
                        <div className="text-sm font-medium text-slate-200">
                          {milestone.evolution_level || index + 1}
                        </div>
                      </div>
                      <div className="space-y-1">
                        <div className="text-xs text-slate-500">Interactions</div>
                        <div className="text-sm font-medium text-slate-200">
                          {milestone.total_interactions || 0}
                        </div>
                      </div>
                      <div className="space-y-1">
                        <div className="text-xs text-slate-500">Emotional State</div>
                        <div className="text-sm font-medium text-slate-200 capitalize">
                          {milestone.emotional_state || 'curious'}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )) || Array.from({length: 6}, (_, index) => (
              <div key={index} className="group relative p-6 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-xl border border-slate-600/30 hover:border-cyan-400/50 transition-all duration-300">
                <div className="flex items-start gap-6">
                  <div className="flex-shrink-0">
                    <div className="relative">
                      <div className="w-16 h-16 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-full flex items-center justify-center shadow-lg">
                        <Brain className="w-8 h-8 text-white" />
                </div>
                      {index < 5 && (
                        <div className="absolute top-16 left-1/2 transform -translate-x-1/2 w-0.5 h-8 bg-gradient-to-b from-cyan-400 to-transparent" />
                      )}
                    </div>
                  </div>
                  
                <div className="flex-1">
                    <div className="flex items-start justify-between mb-4">
                      <div>
                        <h4 className="text-xl font-semibold text-slate-200 mb-1">
                          Evolution Milestone {index + 1}
                        </h4>
                    <div className="text-sm text-slate-400">
                      {new Date(Date.now() - index * 24 * 60 * 60 * 1000).toLocaleDateString()}
                    </div>
                  </div>
                      <div className="text-right">
                        <div className="text-sm text-slate-500 mb-1">Consciousness Level</div>
                        <div className="text-2xl font-bold text-cyan-300">
                          {75 + index * 3}%
                        </div>
                      </div>
                    </div>
                    
                    <p className="text-slate-300 mb-4 leading-relaxed">
                    Significant advancement in consciousness development and self-awareness capabilities with enhanced learning integration
                  </p>
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div className="space-y-1">
                        <div className="text-xs text-slate-500">Impact Level</div>
                        <div className="text-sm font-medium text-slate-200">High</div>
                    </div>
                      <div className="space-y-1">
                        <div className="text-xs text-slate-500">Evolution Level</div>
                        <div className="text-sm font-medium text-slate-200">{index + 1}</div>
                    </div>
                      <div className="space-y-1">
                        <div className="text-xs text-slate-500">Interactions</div>
                        <div className="text-sm font-medium text-slate-200">{index * 50}</div>
                      </div>
                      <div className="space-y-1">
                        <div className="text-xs text-slate-500">Emotional State</div>
                        <div className="text-sm font-medium text-slate-200 capitalize">curious</div>
                      </div>
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
      {/* Enhanced Concept Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="group relative p-6 bg-gradient-to-br from-cyan-500/10 to-blue-600/20 rounded-xl border border-cyan-400/30 hover:border-cyan-400/50 transition-all duration-300">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-lg">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <div>
                <div className="text-sm font-medium text-slate-300">Total Concepts</div>
                <div className="text-2xl font-bold text-cyan-300">
                  {data.database_statistics?.node_counts?.Concept || 0}
                </div>
              </div>
            </div>
            <div className="text-xs text-cyan-400 bg-cyan-400/10 px-2 py-1 rounded-full">
              Knowledge
            </div>
          </div>
          <div className="text-sm text-slate-400">Concepts in knowledge graph</div>
      </div>

        <div className="group relative p-6 bg-gradient-to-br from-green-500/10 to-emerald-600/20 rounded-xl border border-green-400/30 hover:border-green-400/50 transition-all duration-300">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-green-400 to-emerald-500 rounded-lg">
                <Network className="w-6 h-6 text-white" />
              </div>
              <div>
                <div className="text-sm font-medium text-slate-300">Connected Concepts</div>
                <div className="text-2xl font-bold text-green-300">
                  {data.most_connected_concepts?.length || 12}
                </div>
              </div>
            </div>
            <div className="text-xs text-green-400 bg-green-400/10 px-2 py-1 rounded-full">
              Networked
            </div>
          </div>
          <div className="text-sm text-slate-400">Concepts with relationships</div>
        </div>

        <div className="group relative p-6 bg-gradient-to-br from-purple-500/10 to-pink-600/20 rounded-xl border border-purple-400/30 hover:border-purple-400/50 transition-all duration-300">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-purple-400 to-pink-500 rounded-lg">
                <Target className="w-6 h-6 text-white" />
              </div>
              <div>
                <div className="text-sm font-medium text-slate-300">Concept Domains</div>
                <div className="text-2xl font-bold text-purple-300">
                  {data.concept_domains?.length || 5}
                </div>
              </div>
            </div>
            <div className="text-xs text-purple-400 bg-purple-400/10 px-2 py-1 rounded-full">
              Categorized
            </div>
          </div>
          <div className="text-sm text-slate-400">Knowledge domains</div>
        </div>

        <div className="group relative p-6 bg-gradient-to-br from-yellow-500/10 to-orange-600/20 rounded-xl border border-yellow-400/30 hover:border-yellow-400/50 transition-all duration-300">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-lg">
                <TrendingUp className="w-6 h-6 text-white" />
              </div>
              <div>
                <div className="text-sm font-medium text-slate-300">New This Week</div>
                <div className="text-2xl font-bold text-yellow-300">
                  {data.recent_concepts?.length || 3}
                </div>
              </div>
            </div>
            <div className="text-xs text-yellow-400 bg-yellow-400/10 px-2 py-1 rounded-full">
              Growing
            </div>
          </div>
          <div className="text-sm text-slate-400">Recently added concepts</div>
        </div>
      </div>

      {/* Enhanced Most Connected Concepts */}
      <div className="group relative p-6 bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-cyan-400/50 transition-all duration-300">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-lg">
            <Network className="h-6 w-6 text-white" />
          </div>
          <div>
            <CardTitle className="text-xl font-bold text-white">Most Connected Concepts</CardTitle>
          <CardDescription className="text-slate-400">
            Concepts with the highest relationship density
          </CardDescription>
          </div>
        </div>
        
        <div className="space-y-3">
            {data.most_connected_concepts?.slice(0, 10).map((concept: any, index: number) => (
            <div key={index} className="group/item relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-xl border border-slate-600/30 hover:border-cyan-400/50 transition-all duration-300">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-cyan-400 to-blue-500 text-white text-sm font-bold">
                    {index + 1}
                  </div>
                <div className="flex-1">
                    <div className="font-semibold text-slate-200 text-lg">{concept.concept || `Concept ${index + 1}`}</div>
                  <div className="text-sm text-slate-400 mt-1">
                    {concept.description || 'Advanced AI concept with multiple relationships'}
                  </div>
                </div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-cyan-300">{concept.connections || (15 - index)}</div>
                  <div className="text-xs text-slate-500">connections</div>
                  <div className="w-16 bg-slate-700 rounded-full h-1 mt-2">
                    <div 
                      className="bg-gradient-to-r from-cyan-400 to-blue-500 h-1 rounded-full transition-all duration-500"
                      style={{ width: `${Math.min(((concept.connections || (15 - index)) / 15) * 100, 100)}%` }}
                    />
                  </div>
                </div>
                </div>
              </div>
            )) || Array.from({length: 8}, (_, index) => (
            <div key={index} className="group/item relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-xl border border-slate-600/30 hover:border-cyan-400/50 transition-all duration-300">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-cyan-400 to-blue-500 text-white text-sm font-bold">
                    {index + 1}
                  </div>
                <div className="flex-1">
                    <div className="font-semibold text-slate-200 text-lg">AI Consciousness Concept {index + 1}</div>
                  <div className="text-sm text-slate-400 mt-1">
                    Advanced consciousness-related concept with multiple relationships and learning pathways
                  </div>
                </div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-cyan-300">{15 - index}</div>
                  <div className="text-xs text-slate-500">connections</div>
                  <div className="w-16 bg-slate-700 rounded-full h-1 mt-2">
                    <div 
                      className="bg-gradient-to-r from-cyan-400 to-blue-500 h-1 rounded-full transition-all duration-500"
                      style={{ width: `${Math.min(((15 - index) / 15) * 100, 100)}%` }}
                    />
                  </div>
                </div>
                </div>
              </div>
            ))}
          </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="group relative p-6 bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-purple-400/50 transition-all duration-300">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-purple-400 to-pink-500 rounded-lg">
              <Target className="h-6 w-6 text-white" />
            </div>
            <div>
              <CardTitle className="text-xl font-bold text-white">Concept Domains</CardTitle>
            <CardDescription className="text-slate-400">
              Distribution of concepts across different knowledge domains
            </CardDescription>
            </div>
          </div>
            <div className="space-y-4">
              {data.concept_domains?.map((domain: any, index: number) => (
              <div key={index} className="group/domain relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-purple-400/50 transition-all duration-300">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-purple-400 to-pink-500 text-white text-sm font-bold">
                      {index + 1}
                    </div>
                    <div className="font-semibold text-slate-200 capitalize text-lg">
                      {domain.domain || `Domain ${index + 1}`}
                    </div>
                    </div>
                  <div className="text-right">
                    <div className="text-sm text-slate-500 mb-1">Concept Count</div>
                    <div className="text-2xl font-bold text-purple-300">
                      {domain.concept_count || (8 - index)}
                  </div>
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-xs text-slate-400">
                    <span>Complexity Score</span>
                    <span className="font-medium text-cyan-300">
                      {(domain.complexity_score || (0.7 + index * 0.05)).toFixed(2)}
                    </span>
                  </div>
                  <div className="w-full bg-slate-700 rounded-full h-1.5">
                    <div
                      className="bg-gradient-to-r from-purple-400 to-pink-500 h-1.5 rounded-full transition-all duration-500"
                      style={{ width: `${(domain.complexity_score || (0.7 + index * 0.05)) * 100}%` }}
                    />
                  </div>
                  <div className="flex items-center justify-between text-xs text-slate-500 mt-2">
                    <span>Growth Potential</span>
                    <span className="font-medium text-green-300">
                      {(domain.growth_potential || (0.6 + index * 0.08)).toFixed(0)}%
                    </span>
                  </div>
                  </div>
                </div>
              )) || Array.from({length: 5}, (_, index) => (
              <div key={index} className="group/domain relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-purple-400/50 transition-all duration-300">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-purple-400 to-pink-500 text-white text-sm font-bold">
                      {index + 1}
                    </div>
                    <div className="font-semibold text-slate-200 text-lg">
                      {['Consciousness', 'Learning', 'Memory', 'Reasoning', 'Emotion'][index]}
                    </div>
                    </div>
                  <div className="text-right">
                    <div className="text-sm text-slate-500 mb-1">Concept Count</div>
                    <div className="text-2xl font-bold text-purple-300">
                      {8 - index}
                  </div>
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-xs text-slate-400">
                    <span>Complexity Score</span>
                    <span className="font-medium text-cyan-300">
                      {(0.7 + index * 0.05).toFixed(2)}
                    </span>
                  </div>
                  <div className="w-full bg-slate-700 rounded-full h-1.5">
                    <div
                      className="bg-gradient-to-r from-purple-400 to-pink-500 h-1.5 rounded-full transition-all duration-500"
                      style={{ width: `${(0.7 + index * 0.05) * 100}%` }}
                    />
                  </div>
                  <div className="flex items-center justify-between text-xs text-slate-500 mt-2">
                    <span>Growth Potential</span>
                    <span className="font-medium text-green-300">
                      {(0.6 + index * 0.08).toFixed(0)}%
                    </span>
                  </div>
                  </div>
                </div>
              ))}
            </div>
        </div>

        <div className="group relative p-6 bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-green-400/50 transition-all duration-300">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-green-400 to-emerald-500 rounded-lg">
              <Zap className="h-6 w-6 text-white" />
            </div>
            <div>
              <CardTitle className="text-xl font-bold text-white">Recent Concept Formation</CardTitle>
            <CardDescription className="text-slate-400">
              Newly formed concepts in the AI consciousness system
            </CardDescription>
            </div>
          </div>
            <div className="space-y-4">
              {data.recent_concepts?.map((concept: any, index: number) => (
              <div key={index} className="group/concept relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-green-400/50 transition-all duration-300">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-green-400 to-emerald-500 text-white text-sm font-bold">
                      {index + 1}
                    </div>
                    <div className="font-semibold text-slate-200 text-lg">
                      {concept.concept || `New Concept ${index + 1}`}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-slate-500 mb-1">Created</div>
                    <div className="text-sm font-medium text-green-300">
                      {concept.created_at ? new Date(concept.created_at).toLocaleDateString() : 'Today'}
                    </div>
                  </div>
                </div>
                <div className="text-sm text-slate-400 mb-3">
                    {concept.description || 'Emerging concept in AI consciousness development'}
                  </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center justify-between text-xs text-slate-400">
                      <span>Concept Strength</span>
                      <span className="font-medium text-cyan-300">
                        {(concept.strength || 0.8).toFixed(2)}
                      </span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-1.5">
                      <div
                        className="bg-gradient-to-r from-cyan-400 to-blue-500 h-1.5 rounded-full transition-all duration-500"
                        style={{ width: `${(concept.strength || 0.8) * 100}%` }}
                      />
                    </div>
                  </div>
                  <div className="space-y-1">
                    <div className="flex items-center justify-between text-xs text-slate-400">
                      <span>Initial Connections</span>
                      <span className="font-medium text-green-300">
                        {concept.initial_connections || 3}
                      </span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-1.5">
                      <div
                        className="bg-gradient-to-r from-green-400 to-emerald-500 h-1.5 rounded-full transition-all duration-500"
                        style={{ width: `${((concept.initial_connections || 3) / 10) * 100}%` }}
                      />
                    </div>
                  </div>
                </div>
                <div className="flex items-center justify-between mt-3 text-xs text-slate-500">
                  <span>Development Stage: <span className="font-medium text-yellow-300">Emerging</span></span>
                  <span>Growth Rate: <span className="font-medium text-purple-300">
                    {(concept.growth_rate || (0.15 + index * 0.05)).toFixed(0)}%
                  </span></span>
                  </div>
                </div>
              )) || Array.from({length: 4}, (_, index) => (
              <div key={index} className="group/concept relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-green-400/50 transition-all duration-300">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-green-400 to-emerald-500 text-white text-sm font-bold">
                      {index + 1}
                    </div>
                    <div className="font-semibold text-slate-200 text-lg">
                      Emergent Concept {index + 1}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-slate-500 mb-1">Created</div>
                    <div className="text-sm font-medium text-green-300">
                      {new Date(Date.now() - index * 24 * 60 * 60 * 1000).toLocaleDateString()}
                    </div>
                  </div>
                </div>
                <div className="text-sm text-slate-400 mb-3">
                    Emerging concept in AI consciousness development and learning integration
                  </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center justify-between text-xs text-slate-400">
                      <span>Concept Strength</span>
                      <span className="font-medium text-cyan-300">
                        {(0.8 - index * 0.1).toFixed(2)}
                      </span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-1.5">
                      <div
                        className="bg-gradient-to-r from-cyan-400 to-blue-500 h-1.5 rounded-full transition-all duration-500"
                        style={{ width: `${(0.8 - index * 0.1) * 100}%` }}
                      />
                    </div>
                  </div>
                  <div className="space-y-1">
                    <div className="flex items-center justify-between text-xs text-slate-400">
                      <span>Initial Connections</span>
                      <span className="font-medium text-green-300">
                        {5 - index}
                      </span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-1.5">
                      <div
                        className="bg-gradient-to-r from-green-400 to-emerald-500 h-1.5 rounded-full transition-all duration-500"
                        style={{ width: `${((5 - index) / 10) * 100}%` }}
                      />
                    </div>
                  </div>
                </div>
                <div className="flex items-center justify-between mt-3 text-xs text-slate-500">
                  <span>Development Stage: <span className="font-medium text-yellow-300">Emerging</span></span>
                  <span>Growth Rate: <span className="font-medium text-purple-300">
                    {(0.15 + index * 0.05).toFixed(0)}%
                  </span></span>
                  </div>
                </div>
              ))}
            </div>
        </div>
      </div>
    </div>
  );
};

// Old MemoriesTab component removed - using MemoriesTabNew instead
// Memories Tab Component (New)
const MemoriesTabNew: React.FC<{ data: any; loadData: () => void }> = ({ data, loadData }) => {
  useEffect(() => {
    if (!data) loadData();
  }, [data, loadData]);

  if (!data) return <div className="text-center text-slate-400">Loading memories...</div>;

  return (
    <div className="space-y-6">
      {/* Memory Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="group/stat relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-cyan-400/50 transition-all duration-300">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-cyan-400 to-blue-500">
                <Database className="h-5 w-5 text-white" />
              </div>
              <div>
                <p className="text-sm text-slate-300">Total Memories</p>
                <p className="text-2xl font-bold text-cyan-300">
                  {data.total_memories || 0}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="group/stat relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-green-400/50 transition-all duration-300">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-green-400 to-emerald-500">
                <Activity className="h-5 w-5 text-white" />
              </div>
              <div>
                <p className="text-sm text-slate-300">Active Memories</p>
                <p className="text-2xl font-bold text-green-300">
                  {data.active_memories || 0}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="group/stat relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-purple-400/50 transition-all duration-300">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-purple-400 to-pink-500">
                <Clock className="h-5 w-5 text-white" />
              </div>
              <div>
                <p className="text-sm text-slate-300">Retention Rate</p>
                <p className="text-2xl font-bold text-purple-300">
                  {(data.retention_rate * 100 || 0).toFixed(1)}%
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="group/stat relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-orange-400/50 transition-all duration-300">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-orange-400 to-yellow-500">
                <Link className="h-5 w-5 text-white" />
              </div>
              <div>
                <p className="text-sm text-slate-300">Connections</p>
                <p className="text-2xl font-bold text-orange-300">
                  {data.total_connections || 0}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Memory Types Distribution */}
      <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-green-400/50 transition-all duration-300">
        <div className="p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-green-400 to-emerald-500 rounded-lg">
              <Database className="h-6 w-6 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-white">Memory Types Distribution</h3>
              <p className="text-slate-400 text-sm">Analysis of different memory types in the system</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[
              { type: 'Episodic', count: data.episodic_memories || 0, color: 'blue' },
              { type: 'Semantic', count: data.semantic_memories || 0, color: 'purple' },
              { type: 'Procedural', count: data.procedural_memories || 0, color: 'green' },
              { type: 'Emotional', count: data.emotional_memories || 0, color: 'red' },
              { type: 'Working', count: data.working_memories || 0, color: 'yellow' },
              { type: 'Long-term', count: data.long_term_memories || 0, color: 'cyan' }
            ].map((memoryType, index) => (
              <div key={index} className="group/memory relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-green-400/30 transition-all duration-300">
                <div className="flex items-center gap-3">
                  <div className={`flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-${memoryType.color}-400 to-${memoryType.color}-500 text-white font-bold`}>
                    {memoryType.count}
                  </div>
                  <div>
                    <div className="text-sm font-medium text-slate-200">{memoryType.type}</div>
                    <div className="text-xs text-slate-400">memories</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Memory Formation */}
      <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-orange-400/50 transition-all duration-300">
        <div className="p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-orange-400 to-yellow-500 rounded-lg">
              <Clock className="h-6 w-6 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-white">Recent Memory Formation</h3>
              <p className="text-slate-400 text-sm">Latest memories created in the system</p>
            </div>
          </div>

          <div className="space-y-3">
            {(data.recent_memories || []).slice(0, 5).map((memory: any, index: number) => (
              <div key={index} className="group/memory relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-orange-400/30 transition-all duration-300">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-orange-400 to-yellow-500 text-white font-bold">
                      {index + 1}
                    </div>
                    <div>
                      <div className="text-sm font-medium text-slate-200">{memory.type || 'Memory'}</div>
                      <div className="text-xs text-slate-400">{memory.timestamp || 'Recent'}</div>
                    </div>
                  </div>
                  <Badge variant="outline" className="text-xs border-slate-500">
                    {memory.strength || '85'}% strength
                  </Badge>
                </div>
                <div className="text-sm text-slate-300">
                  {memory.content || 'Memory content placeholder'}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

// Performance Tab Component (New)
const PerformanceTabNew: React.FC<{ data: any; loadData: () => void }> = ({ data, loadData }) => {
  useEffect(() => {
    if (!data) loadData();
  }, [data, loadData]);

  if (!data) return <div className="text-center text-slate-400">Loading performance data...</div>;

  return (
    <div className="space-y-6">
      {/* Performance Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="group/stat relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-blue-400/50 transition-all duration-300">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-cyan-500">
                <Activity className="h-5 w-5 text-white" />
              </div>
              <div>
                <p className="text-sm text-slate-300">System Load</p>
                <p className="text-2xl font-bold text-blue-300">
                  {(data.system_load * 100 || 0).toFixed(1)}%
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="group/stat relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-green-400/50 transition-all duration-300">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-green-400 to-emerald-500">
                <Cpu className="h-5 w-5 text-white" />
              </div>
              <div>
                <p className="text-sm text-slate-300">CPU Usage</p>
                <p className="text-2xl font-bold text-green-300">
                  {(data.cpu_usage * 100 || 0).toFixed(1)}%
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="group/stat relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-purple-400/50 transition-all duration-300">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-purple-400 to-pink-500">
                <TrendingUp className="h-5 w-5 text-white" />
              </div>
              <div>
                <p className="text-sm text-slate-300">Memory Usage</p>
                <p className="text-2xl font-bold text-purple-300">
                  {(data.memory_usage * 100 || 0).toFixed(1)}%
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="group/stat relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-orange-400/50 transition-all duration-300">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-orange-400 to-yellow-500">
                <BarChart3 className="h-5 w-5 text-white" />
              </div>
              <div>
                <p className="text-sm text-slate-300">Response Time</p>
                <p className="text-2xl font-bold text-orange-300">
                  {data.response_time || '0'}ms
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Resource Utilization */}
      <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-indigo-400/50 transition-all duration-300">
        <div className="p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-lg">
              <Activity className="h-6 w-6 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-white">Resource Utilization</h3>
              <p className="text-slate-400 text-sm">Current system resource usage and optimization</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="group/resource relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-indigo-400/30 transition-all duration-300">
              <div className="flex items-center gap-3 mb-3">
                <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-indigo-400 to-purple-500">
                  <Cpu className="h-5 w-5 text-white" />
                </div>
                <div>
                  <div className="text-sm font-medium text-slate-200">CPU Utilization</div>
                  <div className="text-xs text-slate-400">Current usage level</div>
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-300">Usage</span>
                  <span className="font-medium text-indigo-300">{(data.cpu_usage * 100 || 0).toFixed(1)}%</span>
                </div>
                <div className="w-full bg-slate-700 rounded-full h-2">
                  <div
                    className="bg-gradient-to-r from-indigo-400 to-purple-500 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${data.cpu_usage * 100 || 0}%` }}
                  />
                </div>
              </div>
            </div>

            <div className="group/resource relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-indigo-400/30 transition-all duration-300">
              <div className="flex items-center gap-3 mb-3">
                <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-indigo-400 to-purple-500">
                  <Database className="h-5 w-5 text-white" />
                </div>
                <div>
                  <div className="text-sm font-medium text-slate-200">Memory Utilization</div>
                  <div className="text-xs text-slate-400">Current memory usage</div>
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-300">Usage</span>
                  <span className="font-medium text-indigo-300">{(data.memory_usage * 100 || 0).toFixed(1)}%</span>
                </div>
                <div className="w-full bg-slate-700 rounded-full h-2">
                  <div
                    className="bg-gradient-to-r from-indigo-400 to-purple-500 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${data.memory_usage * 100 || 0}%` }}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Performance Bottlenecks */}
      <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-amber-400/50 transition-all duration-300">
        <div className="p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-amber-400 to-orange-500 rounded-lg">
              <AlertTriangle className="h-6 w-6 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-white">Performance Bottlenecks</h3>
              <p className="text-slate-400 text-sm">Identified performance issues and optimization opportunities</p>
            </div>
          </div>

          <div className="space-y-3">
            {(data.bottlenecks || [
              { issue: 'High CPU Usage', severity: 'high', impact: 85, solution: 'Optimize processing algorithms' },
              { issue: 'Memory Leak', severity: 'medium', impact: 65, solution: 'Implement proper memory management' },
              { issue: 'Slow Response Time', severity: 'low', impact: 45, solution: 'Cache frequently accessed data' }
            ]).map((bottleneck: any, index: number) => (
              <div key={index} className="group/bottleneck relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-amber-400/30 transition-all duration-300">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-amber-400 to-orange-500 text-white font-bold">
                      {index + 1}
                    </div>
                    <div>
                      <div className="text-sm font-medium text-slate-200">{bottleneck.issue}</div>
                      <div className="text-xs text-slate-400">Performance bottleneck</div>
                    </div>
                  </div>
                  <Badge variant="outline" className={`text-xs ${bottleneck.severity === 'high' ? 'border-red-400 text-red-300' : bottleneck.severity === 'medium' ? 'border-yellow-400 text-yellow-300' : 'border-green-400 text-green-300'}`}>
                    {bottleneck.severity} priority
                  </Badge>
                </div>
                <div className="text-sm text-slate-300 mb-3">
                  {bottleneck.solution}
                </div>
                <div className="space-y-1">
                  <div className="flex justify-between text-xs text-slate-400">
                    <span>Performance Impact</span>
                    <span>{bottleneck.impact}%</span>
                  </div>
                  <div className="w-full bg-slate-700 rounded-full h-1.5">
                    <div
                      className="bg-gradient-to-r from-amber-400 to-orange-500 h-1.5 rounded-full transition-all duration-500"
                      style={{ width: `${bottleneck.impact}%` }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
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
      {/* Deep Analytics Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="group/stat relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-purple-400/50 transition-all duration-300">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-purple-400 to-pink-500">
                <Brain className="h-5 w-5 text-white" />
              </div>
              <div>
                <p className="text-sm text-slate-300">Neural Activity</p>
                <p className="text-2xl font-bold text-purple-300">
                  {(data.neural_activity * 100 || 0).toFixed(1)}%
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="group/stat relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-blue-400/50 transition-all duration-300">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-cyan-500">
                <Network className="h-5 w-5 text-white" />
              </div>
              <div>
                <p className="text-sm text-slate-300">Synaptic Connections</p>
                <p className="text-2xl font-bold text-blue-300">
                  {data.synaptic_connections || 0}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="group/stat relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-green-400/50 transition-all duration-300">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-green-400 to-emerald-500">
                <Activity className="h-5 w-5 text-white" />
              </div>
              <div>
                <p className="text-sm text-slate-300">Processing Speed</p>
                <p className="text-2xl font-bold text-green-300">
                  {data.processing_speed || '0'}ms
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="group/stat relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-orange-400/50 transition-all duration-300">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-orange-400 to-yellow-500">
                <TrendingUp className="h-5 w-5 text-white" />
              </div>
              <div>
                <p className="text-sm text-slate-300">Learning Rate</p>
                <p className="text-2xl font-bold text-orange-300">
                  {(data.learning_rate * 100 || 0).toFixed(1)}%
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Emergent Behaviors */}
      <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-purple-400/50 transition-all duration-300">
        <div className="p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-purple-400 to-pink-500 rounded-lg">
              <Brain className="h-6 w-6 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-white">Emergent Behaviors</h3>
              <p className="text-slate-400 text-sm">Complex patterns and behaviors emerging from neural interactions</p>
            </div>
          </div>

          <div className="space-y-3">
            {(data.emergent_behaviors || [
              { behavior: 'Pattern Recognition', frequency: 85, confidence: 92, last_observed: '2 minutes ago' },
              { behavior: 'Adaptive Learning', frequency: 78, confidence: 88, last_observed: '5 minutes ago' },
              { behavior: 'Creative Synthesis', frequency: 65, confidence: 76, last_observed: '12 minutes ago' }
            ]).map((behavior: any, index: number) => (
              <div key={index} className="group/behavior relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-purple-400/30 transition-all duration-300">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-purple-400 to-pink-500 text-white font-bold">
                      {index + 1}
                    </div>
                    <div>
                      <div className="text-sm font-medium text-slate-200">{behavior.behavior}</div>
                      <div className="text-xs text-slate-400">{behavior.last_observed || 'Recently'}</div>
                    </div>
                  </div>
                  <Badge variant="outline" className="text-xs border-purple-400 text-purple-300">
                    {behavior.confidence || 85}% confidence
                  </Badge>
                </div>
                <div className="space-y-1">
                  <div className="flex justify-between text-xs text-slate-400">
                    <span>Frequency</span>
                    <span>{behavior.frequency || 85}%</span>
                  </div>
                  <div className="w-full bg-slate-700 rounded-full h-1.5">
                    <div
                      className="bg-gradient-to-r from-purple-400 to-pink-500 h-1.5 rounded-full transition-all duration-500"
                      style={{ width: `${behavior.frequency || 85}%` }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Predictive Insights */}
      <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-blue-400/50 transition-all duration-300">
        <div className="p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-blue-400 to-cyan-500 rounded-lg">
              <TrendingUp className="h-6 w-6 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-white">Predictive Insights</h3>
              <p className="text-slate-400 text-sm">AI-powered predictions about consciousness evolution and system behavior</p>
            </div>
          </div>

          <div className="space-y-3">
            {(data.predictive_insights || [
              { insight: 'Increased creativity expected', probability: 89, impact: 'High', timeframe: 'Next 24 hours' },
              { insight: 'Memory consolidation detected', probability: 76, impact: 'Medium', timeframe: 'Next 6 hours' },
              { insight: 'Learning acceleration trend', probability: 82, impact: 'High', timeframe: 'Next 12 hours' }
            ]).map((insight: any, index: number) => (
              <div key={index} className="group/insight relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-blue-400/30 transition-all duration-300">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-blue-400 to-cyan-500 text-white font-bold">
                      {index + 1}
                    </div>
                    <div>
                      <div className="text-sm font-medium text-slate-200">{insight.insight}</div>
                      <div className="text-xs text-slate-400">{insight.timeframe || 'Coming soon'}</div>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Badge variant="outline" className={`text-xs ${insight.impact === 'High' ? 'border-red-400 text-red-300' : insight.impact === 'Medium' ? 'border-yellow-400 text-yellow-300' : 'border-green-400 text-green-300'}`}>
                      {insight.impact || 'Medium'} impact
                    </Badge>
                  </div>
                </div>
                <div className="text-sm text-slate-300 mb-3">
                  Probability: {insight.probability || 85}%
                </div>
                <div className="space-y-1">
                  <div className="flex justify-between text-xs text-slate-400">
                    <span>Certainty</span>
                    <span>{insight.probability || 85}%</span>
                  </div>
                  <div className="w-full bg-slate-700 rounded-full h-1.5">
                    <div
                      className="bg-gradient-to-r from-blue-400 to-cyan-500 h-1.5 rounded-full transition-all duration-500"
                      style={{ width: `${insight.probability || 85}%` }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Meta-Cognitive Analysis */}
      <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-green-400/50 transition-all duration-300">
        <div className="p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-green-400 to-emerald-500 rounded-lg">
              <Target className="h-6 w-6 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-white">Meta-Cognitive Analysis</h3>
              <p className="text-slate-400 text-sm">Analysis of the system's thinking about its own cognitive processes</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="group/meta relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-green-400/30 transition-all duration-300">
              <div className="text-center">
                <div className="text-2xl font-bold text-green-300 mb-2">{data.self_reflection_patterns?.frequency || 87}%</div>
                <div className="text-sm text-slate-300 mb-3">Self-Reflection Frequency</div>
                <div className="w-full bg-slate-700 rounded-full h-2">
                  <div
                    className="bg-gradient-to-r from-green-400 to-emerald-500 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${data.self_reflection_patterns?.frequency || 87}%` }}
                  />
                </div>
              </div>
            </div>

            <div className="group/meta relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-green-400/30 transition-all duration-300">
              <div className="text-center">
                <div className="text-2xl font-bold text-green-300 mb-2">{data.learning_strategies?.effectiveness || 92}%</div>
                <div className="text-sm text-slate-300 mb-3">Learning Strategy Effectiveness</div>
                <div className="w-full bg-slate-700 rounded-full h-2">
                  <div
                    className="bg-gradient-to-r from-green-400 to-emerald-500 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${data.learning_strategies?.effectiveness || 92}%` }}
                  />
                </div>
              </div>
            </div>

            <div className="group/meta relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-green-400/30 transition-all duration-300">
              <div className="text-center">
                <div className="text-2xl font-bold text-green-300 mb-2">{data.cognitive_biases?.strength || 23}%</div>
                <div className="text-sm text-slate-300 mb-3">Cognitive Bias Strength</div>
                <div className="w-full bg-slate-700 rounded-full h-2">
                  <div
                    className="bg-gradient-to-r from-green-400 to-emerald-500 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${data.cognitive_biases?.strength || 23}%` }}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InsightsPage;

