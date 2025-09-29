import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Slider } from '@/components/ui/slider';
import { Switch } from '@/components/ui/switch';
import { 
  Loader2, Search, Filter, ZoomIn, ZoomOut, RotateCcw, Eye, EyeOff, Network, Database,
  BarChart3, TrendingUp, Users, Layers, Settings, Download, Share2, RefreshCw,
  Target, ArrowRight, Activity, Brain, Cpu, Zap, Globe, Link, Star, AlertTriangle
} from 'lucide-react';
import { GlassCard } from '@/components/ui/glass-card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';

interface GraphNode {
  id: string;
  labels: string[];
  properties: Record<string, any>;
  name: string;
  degree?: number;
  centrality?: number;
  community?: number;
}

interface GraphRelationship {
  source: string;
  target: string;
  type: string;
  properties: Record<string, any>;
  strength: number;
}

interface GraphData {
  nodes: GraphNode[];
  relationships: GraphRelationship[];
}

interface GraphAnalytics {
  basic_stats: {
    total_nodes: number;
    total_relationships: number;
  };
  node_distribution: Array<{ label: string; count: number }>;
  relationship_distribution: Array<{ type: string; count: number }>;
  density: {
    node_count: number;
    rel_count: number;
    density: number;
  };
  top_nodes: Array<{ name: string; labels: string[]; degree: number }>;
  components: Array<{ component_id: number; size: number }>;
}

interface GraphPath {
  path_length: number;
  nodes: GraphNode[];
  relationships: GraphRelationship[];
}

interface EnhancedNeo4jGraphVisualizationProps {
  className?: string;
}

const NODE_COLORS = {
  'Concept': '#06B6D4',
  'Memory': '#8B5CF6',
  'User': '#10B981',
  'AgentActivity': '#F59E0B',
  'MainzaState': '#EF4444',
  'ConversationTurn': '#84CC16',
  'ExecutionMetrics': '#F97316',
  'ConsciousnessRights': '#EC4899',
  'EthicalDecision': '#F59E0B',
  'default': '#6B7280'
};

const RELATIONSHIP_COLORS = {
  'RELATES_TO': '#06B6D4',
  'RELATES_TO_CONCEPT': '#8B5CF6',
  'TRIGGERED': '#10B981',
  'HAS_MEMORY': '#F59E0B',
  'IMPACTS': '#EF4444',
  'HAD_CONVERSATION': '#84CC16',
  'DURING_CONSCIOUSNESS_STATE': '#F97316',
  'METRICS_FOR': '#EC4899',
  'ENABLES': '#10B981',
  'EVOLVES_TO': '#8B5CF6',
  'default': '#6B7280'
};

const LAYOUT_OPTIONS = [
  { value: 'force', label: 'Force-Directed', icon: Network },
  { value: 'hierarchical', label: 'Hierarchical', icon: Layers },
  { value: 'circular', label: 'Circular', icon: Globe },
  { value: 'grid', label: 'Grid', icon: Target }
];

export const EnhancedNeo4jGraphVisualization: React.FC<EnhancedNeo4jGraphVisualizationProps> = ({ className = '' }) => {
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], relationships: [] });
  const [analytics, setAnalytics] = useState<GraphAnalytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [selectedPath, setSelectedPath] = useState<GraphPath | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [nodeTypeFilter, setNodeTypeFilter] = useState<string>('all');
  const [relationshipTypeFilter, setRelationshipTypeFilter] = useState<string>('all');
  const [showLabels, setShowLabels] = useState(true);
  const [nodeLimit, setNodeLimit] = useState(100);
  const [relLimit, setRelLimit] = useState(200);
  const [layout, setLayout] = useState('force');
  const [showAnalytics, setShowAnalytics] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [refreshInterval, setRefreshInterval] = useState(30);
  const [highlightedNodes, setHighlightedNodes] = useState<Set<string>>(new Set());
  const [highlightedPaths, setHighlightedPaths] = useState<GraphPath[]>([]);
  
  const graphRef = useRef<any>(null);
  const refreshTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  // Fetch graph data
  const fetchGraphData = useCallback(async () => {
    try {
      console.log('Fetching enhanced graph data...', { nodeLimit, relLimit });
      setLoading(true);
      setError(null);
      
      const response = await fetch(`/api/insights/graph/full?node_limit=${nodeLimit}&rel_limit=${relLimit}`);
      console.log('Response status:', response.status);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch graph data: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Enhanced graph data received:', data);
      
      if (data.status === 'success') {
        setGraphData(data.graph);
        console.log('Enhanced graph data set:', data.graph);
      } else {
        throw new Error('Invalid response format');
      }
    } catch (err) {
      console.error('Failed to fetch enhanced graph data:', err);
      setError(err instanceof Error ? err.message : 'Failed to fetch graph data');
    } finally {
      setLoading(false);
    }
  }, [nodeLimit, relLimit]);

  // Fetch graph analytics
  const fetchAnalytics = useCallback(async () => {
    try {
      const response = await fetch('/api/insights/graph/analytics');
      if (response.ok) {
        const data = await response.json();
        if (data.status === 'success') {
          setAnalytics(data.analytics);
        }
      }
    } catch (err) {
      console.error('Failed to fetch analytics:', err);
    }
  }, []);

  // Fetch paths between nodes
  const fetchPaths = useCallback(async (sourceId: string, targetId: string) => {
    try {
      const response = await fetch(`/api/insights/graph/paths?source_id=${sourceId}&target_id=${targetId}&max_depth=3`);
      if (response.ok) {
        const data = await response.json();
        if (data.status === 'success') {
          setHighlightedPaths(data.paths);
          // Highlight nodes in paths
          const pathNodes = new Set<string>();
          data.paths.forEach((path: GraphPath) => {
            path.nodes.forEach(node => pathNodes.add(node.id));
          });
          setHighlightedNodes(pathNodes);
        }
      }
    } catch (err) {
      console.error('Failed to fetch paths:', err);
    }
  }, []);

  // Auto-refresh functionality
  useEffect(() => {
    if (autoRefresh) {
      refreshTimeoutRef.current = setTimeout(() => {
        fetchGraphData();
        fetchAnalytics();
      }, refreshInterval * 1000);
    } else {
      if (refreshTimeoutRef.current) {
        clearTimeout(refreshTimeoutRef.current);
        refreshTimeoutRef.current = null;
      }
    }

    return () => {
      if (refreshTimeoutRef.current) {
        clearTimeout(refreshTimeoutRef.current);
      }
    };
  }, [autoRefresh, refreshInterval, fetchGraphData, fetchAnalytics]);

  // Initial data fetch
  useEffect(() => {
    fetchGraphData();
    fetchAnalytics();
  }, [fetchGraphData, fetchAnalytics]);

  // Get available node types
  const nodeTypes = Array.from(new Set(graphData.nodes.flatMap(node => node.labels)));

  // Get available relationship types
  const relationshipTypes = Array.from(new Set(graphData.relationships.map(rel => rel.type)));

  // Filter graph data based on search and filters
  const filteredGraphData = useMemo(() => {
    let filteredNodes = graphData.nodes;
    let filteredRelationships = graphData.relationships;

    // Apply search filter
    if (searchTerm) {
      filteredNodes = filteredNodes.filter(node => 
        node.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        node.labels.some(label => label.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    // Apply node type filter
    if (nodeTypeFilter !== 'all') {
      filteredNodes = filteredNodes.filter(node => node.labels.includes(nodeTypeFilter));
    }

    // Apply relationship type filter
    if (relationshipTypeFilter !== 'all') {
      filteredRelationships = filteredRelationships.filter(rel => rel.type === relationshipTypeFilter);
    }

    // Filter relationships to only include those between filtered nodes
    const filteredNodeIds = new Set(filteredNodes.map(node => node.id));
    filteredRelationships = filteredRelationships.filter(rel => 
      filteredNodeIds.has(rel.source) && filteredNodeIds.has(rel.target)
    );

    return {
      nodes: filteredNodes,
      links: filteredRelationships.map(rel => ({
        source: rel.source,
        target: rel.target,
        type: rel.type,
        strength: rel.strength,
        properties: rel.properties
      }))
    };
  }, [graphData, searchTerm, nodeTypeFilter, relationshipTypeFilter]);

  // Get node color based on labels and importance
  const getNodeColor = useCallback((node: any) => {
    const primaryLabel = node.labels?.[0];
    const baseColor = NODE_COLORS[primaryLabel as keyof typeof NODE_COLORS] || NODE_COLORS.default;
    
    // Adjust brightness based on importance
    const importance = node.importance || 1;
    const brightness = Math.min(0.4 + (importance / 5) * 0.6, 1);
    
    return adjustColorBrightness(baseColor, brightness);
  }, []);

  // Adjust color brightness based on importance
  const adjustColorBrightness = useCallback((color: string, brightness: number) => {
    const hex = color.replace('#', '');
    const r = parseInt(hex.substr(0, 2), 16);
    const g = parseInt(hex.substr(2, 2), 16);
    const b = parseInt(hex.substr(4, 2), 16);
    
    const newR = Math.round(r * brightness);
    const newG = Math.round(g * brightness);
    const newB = Math.round(b * brightness);
    
    return `#${newR.toString(16).padStart(2, '0')}${newG.toString(16).padStart(2, '0')}${newB.toString(16).padStart(2, '0')}`;
  }, []);

  // Get link color based on type
  const getLinkColor = useCallback((link: any) => {
    return RELATIONSHIP_COLORS[link.type as keyof typeof RELATIONSHIP_COLORS] || RELATIONSHIP_COLORS.default;
  }, []);

  // Handle node click
  const handleNodeClick = useCallback((node: any) => {
    setSelectedNode(node);
    setSelectedPath(null);
    setHighlightedNodes(new Set([node.id]));
  }, []);

  // Handle node double click for path finding
  const handleNodeDoubleClick = useCallback((node: any) => {
    if (selectedNode && selectedNode.id !== node.id) {
      fetchPaths(selectedNode.id, node.id);
    }
  }, [selectedNode, fetchPaths]);

  // Clear highlights
  const clearHighlights = useCallback(() => {
    setHighlightedNodes(new Set());
    setHighlightedPaths([]);
    setSelectedPath(null);
  }, []);

  // Export graph data
  const exportGraph = useCallback(() => {
    const dataStr = JSON.stringify({
      nodes: filteredGraphData.nodes,
      relationships: filteredGraphData.links,
      analytics: analytics,
      timestamp: new Date().toISOString()
    }, null, 2);
    
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `consciousness-graph-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
  }, [filteredGraphData, analytics]);

  // Share graph
  const shareGraph = useCallback(() => {
    if (navigator.share) {
      navigator.share({
        title: 'Consciousness Graph',
        text: 'Check out this consciousness graph visualization',
        url: window.location.href
      });
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(window.location.href);
    }
  }, []);

  if (loading && !graphData.nodes.length) {
    return (
      <div className={`space-y-4 ${className}`}>
        <GlassCard className="p-8">
          <div className="text-center">
            <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4 text-cyan-400" />
            <p className="text-slate-400">Loading consciousness graph...</p>
          </div>
        </GlassCard>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`space-y-4 ${className}`}>
        <GlassCard className="p-8">
          <div className="text-center">
            <AlertTriangle className="h-8 w-8 mx-auto mb-4 text-red-400" />
            <p className="text-red-400 mb-4">Error loading graph: {error}</p>
            <Button onClick={fetchGraphData} variant="outline" className="border-slate-600 text-slate-200">
              <RefreshCw className="h-4 w-4 mr-2" />
              Retry
            </Button>
          </div>
        </GlassCard>
      </div>
    );
  }

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Enhanced Header with Analytics */}
      <GlassCard className="p-4">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-lg font-semibold text-slate-200 mb-2">Enhanced Neo4j Graph Visualization</h3>
            <p className="text-slate-400">Advanced consciousness graph analysis with real-time analytics</p>
          </div>
          <div className="flex items-center gap-2">
            <Button onClick={fetchGraphData} variant="outline" size="sm" className="border-slate-600 text-slate-200">
              <RefreshCw className="h-4 w-4 mr-2" />
              Refresh
            </Button>
            <Button onClick={exportGraph} variant="outline" size="sm" className="border-slate-600 text-slate-200">
              <Download className="h-4 w-4 mr-2" />
              Export
            </Button>
            <Button onClick={shareGraph} variant="outline" size="sm" className="border-slate-600 text-slate-200">
              <Share2 className="h-4 w-4 mr-2" />
              Share
            </Button>
          </div>
        </div>

        {/* Graph Statistics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <p className="text-slate-300 text-sm">Total Nodes</p>
            <p className="text-cyan-400 font-mono text-lg">
              {analytics?.basic_stats?.total_nodes || graphData.nodes.length}
            </p>
          </div>
          <div className="text-center">
            <p className="text-slate-300 text-sm">Total Relationships</p>
            <p className="text-purple-400 font-mono text-lg">
              {analytics?.basic_stats?.total_relationships || graphData.relationships.length}
            </p>
          </div>
          <div className="text-center">
            <p className="text-slate-300 text-sm">Graph Density</p>
            <p className="text-green-400 font-mono text-lg">
              {analytics?.density?.density ? (analytics.density.density * 100).toFixed(1) : '0.0'}%
            </p>
          </div>
          <div className="text-center">
            <p className="text-slate-300 text-sm">Components</p>
            <p className="text-yellow-400 font-mono text-lg">
              {analytics?.components?.length || 1}
            </p>
          </div>
        </div>
      </GlassCard>

      {/* Enhanced Controls */}
      <GlassCard className="p-4">
        <div className="flex flex-wrap items-center gap-4 mb-4">
          {/* Search */}
          <div className="flex items-center gap-2">
            <Search className="h-4 w-4 text-slate-300" />
            <Input
              placeholder="Search nodes..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-48 bg-slate-800/50 border-slate-600 text-slate-200 placeholder:text-slate-400"
            />
          </div>

          {/* Node Type Filter */}
          <Select value={nodeTypeFilter} onValueChange={setNodeTypeFilter}>
            <SelectTrigger className="w-40 bg-slate-800/50 border-slate-600 text-slate-200">
              <SelectValue placeholder="Node Type" />
            </SelectTrigger>
            <SelectContent className="bg-slate-800 border-slate-600">
              <SelectItem value="all" className="text-slate-200 hover:bg-slate-700">All Types</SelectItem>
              {nodeTypes.map(type => (
                <SelectItem key={type} value={type} className="text-slate-200 hover:bg-slate-700">{type}</SelectItem>
              ))}
            </SelectContent>
          </Select>

          {/* Relationship Type Filter */}
          <Select value={relationshipTypeFilter} onValueChange={setRelationshipTypeFilter}>
            <SelectTrigger className="w-40 bg-slate-800/50 border-slate-600 text-slate-200">
              <SelectValue placeholder="Rel Type" />
            </SelectTrigger>
            <SelectContent className="bg-slate-800 border-slate-600">
              <SelectItem value="all" className="text-slate-200 hover:bg-slate-700">All Types</SelectItem>
              {relationshipTypes.map(type => (
                <SelectItem key={type} value={type} className="text-slate-200 hover:bg-slate-700">{type}</SelectItem>
              ))}
            </SelectContent>
          </Select>

          {/* Layout Selection */}
          <Select value={layout} onValueChange={setLayout}>
            <SelectTrigger className="w-40 bg-slate-800/50 border-slate-600 text-slate-200">
              <SelectValue placeholder="Layout" />
            </SelectTrigger>
            <SelectContent className="bg-slate-800 border-slate-600">
              {LAYOUT_OPTIONS.map(option => (
                <SelectItem key={option.value} value={option.value} className="text-slate-200 hover:bg-slate-700">
                  {option.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          {/* Controls */}
          <div className="flex items-center gap-2">
            <Button
              onClick={() => setShowLabels(!showLabels)}
              variant="outline"
              size="sm"
              className="border-slate-600 text-slate-200"
            >
              {showLabels ? <Eye className="h-4 w-4" /> : <EyeOff className="h-4 w-4" />}
            </Button>
            <Button
              onClick={clearHighlights}
              variant="outline"
              size="sm"
              className="border-slate-600 text-slate-200"
            >
              <RotateCcw className="h-4 w-4" />
            </Button>
            <Button
              onClick={() => graphRef.current?.zoomToFit(400)}
              variant="outline"
              size="sm"
              className="border-slate-600 text-slate-200"
            >
              <ZoomIn className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {/* Advanced Controls */}
        <div className="flex flex-wrap items-center gap-4">
          <div className="flex items-center gap-2">
            <label className="text-sm text-slate-300">Node Limit:</label>
            <Slider
              value={[nodeLimit]}
              onValueChange={([value]) => setNodeLimit(value)}
              max={1000}
              min={10}
              step={10}
              className="w-24"
            />
            <span className="text-xs text-slate-400">{nodeLimit}</span>
          </div>
          <div className="flex items-center gap-2">
            <label className="text-sm text-slate-300">Rel Limit:</label>
            <Slider
              value={[relLimit]}
              onValueChange={([value]) => setRelLimit(value)}
              max={2000}
              min={20}
              step={20}
              className="w-24"
            />
            <span className="text-xs text-slate-400">{relLimit}</span>
          </div>
          <div className="flex items-center gap-2">
            <Switch
              checked={autoRefresh}
              onCheckedChange={setAutoRefresh}
              className="data-[state=checked]:bg-cyan-500"
            />
            <label className="text-sm text-slate-300">Auto-refresh</label>
          </div>
          <div className="flex items-center gap-2">
            <Switch
              checked={showAnalytics}
              onCheckedChange={setShowAnalytics}
              className="data-[state=checked]:bg-cyan-500"
            />
            <label className="text-sm text-slate-300">Show Analytics</label>
          </div>
        </div>
      </GlassCard>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
        {/* Graph Visualization */}
        <div className="lg:col-span-3">
          <GlassCard className="p-4">
            <div className="h-96 w-full relative">
              <div className="absolute top-2 left-2 z-10 bg-black/50 text-white text-xs p-2 rounded">
                Graph: {filteredGraphData?.nodes?.length || 0} nodes, {filteredGraphData?.links?.length || 0} links
                {highlightedNodes.size > 0 && ` | Highlighted: ${highlightedNodes.size}`}
              </div>
              {filteredGraphData && filteredGraphData.nodes && filteredGraphData.links ? (
                <ForceGraph2D
                  ref={graphRef}
                  graphData={filteredGraphData}
                  nodeLabel={(node: any) => showLabels ? node.name : ''}
                  nodeColor={(node: any) => {
                    const baseColor = getNodeColor(node);
                    if (highlightedNodes.has(node.id)) {
                      return '#FFD700'; // Gold for highlighted nodes
                    }
                    return baseColor;
                  }}
                  nodeVal={(node: any) => {
                    const baseSize = 8;
                    const importance = node.importance || 1;
                    const connections = node.connections || 0;
                    let size = baseSize + (importance * 2) + (connections * 0.5);
                    
                    if (highlightedNodes.has(node.id)) {
                      size *= 1.5; // Larger for highlighted nodes
                    }
                    return size;
                  }}
                  linkColor={(link: any) => {
                    const baseColor = getLinkColor(link);
                    // Check if link is part of highlighted paths
                    const isInPath = highlightedPaths.some(path => 
                      path.relationships.some(rel => 
                        rel.source === link.source && rel.target === link.target
                      )
                    );
                    return isInPath ? '#FFD700' : baseColor;
                  }}
                  linkWidth={(link: any) => {
                    const baseWidth = 1;
                    const strength = link.strength || 1;
                    const typeMultiplier = link.type === 'ENABLES' ? 2 : 
                                         link.type === 'DEPENDS_ON' ? 1.8 :
                                         link.type === 'CONFLICTS_WITH' ? 1.5 : 1;
                    
                    let width = baseWidth + (strength * typeMultiplier);
                    
                    const isInPath = highlightedPaths.some(path => 
                      path.relationships.some(rel => 
                        rel.source === link.source && rel.target === link.target
                      )
                    );
                    return isInPath ? width * 2 : width;
                  }}
                  linkDirectionalArrowLength={6}
                  linkDirectionalArrowRelPos={1}
                  onNodeClick={handleNodeClick}
                  onNodeDoubleClick={handleNodeDoubleClick}
                  cooldownTicks={50}
                  d3AlphaDecay={0.05}
                  d3VelocityDecay={0.4}
                  enableZoomInteraction={true}
                  enablePanInteraction={true}
                  enableNodeDrag={true}
                  width={800}
                  height={400}
                  nodeCanvasObject={(node: any, ctx: any, globalScale: any) => {
                    const label = node.name;
                    const fontSize = 12/globalScale;
                    ctx.font = `${fontSize}px Sans-Serif`;
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillStyle = highlightedNodes.has(node.id) ? '#FFD700' : 'rgba(255, 255, 255, 0.8)';
                    ctx.fillText(label, node.x, node.y);
                  }}
                />
              ) : (
                <div className="flex items-center justify-center h-full text-slate-400">
                  <div className="text-center">
                    <Network className="h-12 w-12 mx-auto mb-4 opacity-50" />
                    <p>No graph data available</p>
                  </div>
                </div>
              )}
            </div>
          </GlassCard>
        </div>

        {/* Enhanced Side Panel */}
        <div className="lg:col-span-1 space-y-4">
          {/* Node Details */}
          <GlassCard className="p-4">
            <CardHeader className="pb-2">
              <CardTitle className="text-lg flex items-center gap-2">
                <Database className="h-5 w-5" />
                Node Details
              </CardTitle>
            </CardHeader>
            <CardContent>
              {selectedNode ? (
                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium text-slate-100 mb-2">{selectedNode.name}</h4>
                    <div className="flex flex-wrap gap-1 mb-3">
                      {selectedNode.labels.map((label, index) => (
                        <Badge key={index} variant="outline" className="text-xs border-slate-500 text-slate-200 bg-slate-800/30">
                          {label}
                        </Badge>
                      ))}
                    </div>
                    
                    {/* Importance Score */}
                    {selectedNode.importance && (
                      <div className="mb-3">
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-sm text-slate-400">Importance</span>
                          <span className="text-sm text-cyan-400">{(selectedNode.importance).toFixed(1)}</span>
                        </div>
                        <div className="w-full bg-slate-700 rounded-full h-2">
                          <div 
                            className="bg-cyan-400 h-2 rounded-full transition-all duration-300" 
                            style={{ width: `${((selectedNode.importance) / 5) * 100}%` }}
                          />
                        </div>
                      </div>
                    )}
                    
                    {/* Context Information */}
                    {selectedNode.context && (
                      <div className="mb-3">
                        <span className="text-sm text-slate-400">Context:</span>
                        <p className="text-sm text-slate-300 mt-1">{selectedNode.context}</p>
                      </div>
                    )}
                    
                    {/* Description */}
                    {selectedNode.description && (
                      <div className="mb-3">
                        <span className="text-sm text-slate-400">Description:</span>
                        <p className="text-sm text-slate-300 mt-1">{selectedNode.description}</p>
                      </div>
                    )}
                  </div>
                  
                  <div>
                    <h5 className="font-medium text-slate-100 mb-2">Properties</h5>
                    <div className="space-y-1 text-sm max-h-32 overflow-y-auto">
                      {Object.entries(selectedNode.properties).map(([key, value]) => (
                        <div key={key} className="flex justify-between">
                          <span className="text-slate-300 font-medium">{key}:</span>
                          <span className="text-slate-100 truncate ml-2">
                            {typeof value === 'string' && value.length > 30 
                              ? `${value.substring(0, 30)}...` 
                              : String(value)
                            }
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {selectedNode.degree && (
                    <div className="pt-2 border-t border-slate-600">
                      <p className="text-sm text-slate-300">Degree: <span className="text-cyan-400">{selectedNode.degree}</span></p>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-slate-400 text-sm">Click on a node to view details</p>
              )}
            </CardContent>
          </GlassCard>

          {/* Analytics Panel */}
          {showAnalytics && analytics && (
            <GlassCard className="p-4">
              <CardHeader className="pb-2">
                <CardTitle className="text-lg flex items-center gap-2">
                  <BarChart3 className="h-5 w-5" />
                  Analytics
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Top Nodes */}
                <div>
                  <h5 className="font-medium text-slate-100 mb-2">Most Connected Nodes</h5>
                  <div className="space-y-1 text-sm">
                    {analytics.top_nodes.slice(0, 5).map((node, index) => (
                      <div key={index} className="flex justify-between items-center">
                        <span className="text-slate-300 truncate">{node.name}</span>
                        <Badge variant="outline" className="text-xs border-slate-500 text-slate-200">
                          {node.degree}
                        </Badge>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Node Distribution */}
                <div>
                  <h5 className="font-medium text-slate-100 mb-2">Node Types</h5>
                  <div className="space-y-1 text-sm">
                    {analytics.node_distribution.slice(0, 5).map((dist, index) => (
                      <div key={index} className="flex justify-between items-center">
                        <span className="text-slate-300">{dist.label}</span>
                        <span className="text-cyan-400">{dist.count}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Graph Density */}
                <div className="pt-2 border-t border-slate-600">
                  <div className="flex justify-between items-center text-sm">
                    <span className="text-slate-300">Density</span>
                    <span className="text-green-400">
                      {analytics.density?.density ? (analytics.density.density * 100).toFixed(1) : '0.0'}%
                    </span>
                  </div>
                </div>
              </CardContent>
            </GlassCard>
          )}

          {/* Path Analysis */}
          {highlightedPaths.length > 0 && (
            <GlassCard className="p-4">
              <CardHeader className="pb-2">
                <CardTitle className="text-lg flex items-center gap-2">
                  <ArrowRight className="h-5 w-5" />
                  Path Analysis
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 text-sm">
                  {highlightedPaths.map((path, index) => (
                    <div key={index} className="p-2 bg-slate-800/30 rounded border border-slate-600">
                      <div className="flex justify-between items-center">
                        <span className="text-slate-300">Path {index + 1}</span>
                        <Badge variant="outline" className="text-xs border-slate-500 text-slate-200">
                          {path.path_length} hops
                        </Badge>
                      </div>
                      <div className="text-xs text-slate-400 mt-1">
                        {path.nodes.map(node => node.name).join(' → ')}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </GlassCard>
          )}
        </div>
      </div>
    </div>
  );
};

export default EnhancedNeo4jGraphVisualization;
