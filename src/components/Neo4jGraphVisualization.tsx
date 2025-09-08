import React, { useState, useEffect, useRef, useCallback } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Loader2, Search, Filter, ZoomIn, ZoomOut, RotateCcw, Eye, EyeOff, Network, Database } from 'lucide-react';
import { GlassCard } from '@/components/ui/glass-card';

interface GraphNode {
  id: string;
  labels: string[];
  properties: Record<string, any>;
  name: string;
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

interface Neo4jGraphVisualizationProps {
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
  'default': '#6B7280'
};

export const Neo4jGraphVisualization: React.FC<Neo4jGraphVisualizationProps> = ({ className = '' }) => {
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], relationships: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [nodeTypeFilter, setNodeTypeFilter] = useState<string>('all');
  const [relationshipTypeFilter, setRelationshipTypeFilter] = useState<string>('all');
  const [showLabels, setShowLabels] = useState(true);
  const [nodeLimit, setNodeLimit] = useState(50);
  const [relLimit, setRelLimit] = useState(100);
  
  const graphRef = useRef<any>(null);

  console.log('Neo4jGraphVisualization component rendered', { loading, error, graphData });

  // Fetch graph data
  const fetchGraphData = useCallback(async () => {
    try {
      console.log('Fetching graph data...', { nodeLimit, relLimit });
      setLoading(true);
      setError(null);
      
      const response = await fetch(`/api/insights/graph/full?node_limit=${nodeLimit}&rel_limit=${relLimit}`);
      console.log('Response status:', response.status);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch graph data: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Graph data received:', data);
      
      if (data.status === 'success') {
        setGraphData(data.graph);
        console.log('Graph data set:', data.graph);
      } else {
        throw new Error('Invalid response format');
      }
    } catch (err) {
      console.error('Failed to fetch graph data:', err);
      setError(err instanceof Error ? err.message : 'Failed to fetch graph data');
    } finally {
      setLoading(false);
    }
  }, [nodeLimit, relLimit]);

  // Transform and filter graph data for react-force-graph-2d
  const filteredGraphData = React.useMemo(() => {
    // Ensure we have valid data before processing
    if (!graphData || !Array.isArray(graphData.nodes) || !Array.isArray(graphData.relationships)) {
      return { nodes: [], links: [] };
    }

    let filteredNodes = graphData.nodes || [];
    let filteredRelationships = graphData.relationships || [];

    // Filter by node type
    if (nodeTypeFilter !== 'all') {
      filteredNodes = filteredNodes.filter(node => 
        node && node.labels && Array.isArray(node.labels) && node.labels.includes(nodeTypeFilter)
      );
    }

    // Filter by search term
    if (searchTerm) {
      filteredNodes = filteredNodes.filter(node =>
        node && node.name && node.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (node && node.properties && node.properties.content && node.properties.content.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    // Filter relationships by type
    if (relationshipTypeFilter !== 'all') {
      filteredRelationships = filteredRelationships.filter(rel =>
        rel && rel.type === relationshipTypeFilter
      );
    }

    // Filter relationships to only include those between filtered nodes
    const filteredNodeIds = new Set(filteredNodes.map(n => n && n.id ? String(n.id) : '').filter(id => id));
    filteredRelationships = filteredRelationships.filter(rel =>
      rel && rel.source && rel.target && 
      filteredNodeIds.has(String(rel.source)) && filteredNodeIds.has(String(rel.target))
    );

    // Transform data for react-force-graph-2d
    const transformedNodes = filteredNodes.map(node => ({
      id: String(node.id || ''),
      name: node.name || `Node ${node.id}`,
      labels: Array.isArray(node.labels) ? node.labels : [],
      properties: node.properties || {},
      group: Array.isArray(node.labels) && node.labels.length > 0 ? node.labels[0] : 'default'
    })).filter(node => node.id);

    const transformedLinks = filteredRelationships.map(rel => ({
      source: String(rel.source || ''),
      target: String(rel.target || ''),
      type: rel.type || 'RELATES_TO',
      properties: rel.properties || {},
      strength: typeof rel.strength === 'number' ? rel.strength : 1.0
    })).filter(link => link.source && link.target);

    console.log('Transformed graph data:', { 
      nodes: transformedNodes.length, 
      links: transformedLinks.length
    });

    return {
      nodes: transformedNodes,
      links: transformedLinks
    };
  }, [graphData, searchTerm, nodeTypeFilter, relationshipTypeFilter]);

  // Get unique node types and relationship types for filters
  const nodeTypes = React.useMemo(() => {
    if (!graphData || !Array.isArray(graphData.nodes)) {
      return [];
    }
    const types = new Set<string>();
    graphData.nodes.forEach(node => {
      if (node && node.labels && Array.isArray(node.labels)) {
        node.labels.forEach(label => types.add(label));
      }
    });
    return Array.from(types).sort();
  }, [graphData.nodes]);

  const relationshipTypes = React.useMemo(() => {
    if (!graphData || !Array.isArray(graphData.relationships)) {
      return [];
    }
    const types = new Set<string>();
    graphData.relationships.forEach(rel => {
      if (rel && rel.type) {
        types.add(rel.type);
      }
    });
    return Array.from(types).sort();
  }, [graphData.relationships]);

  // Load data on mount and when limits change
  useEffect(() => {
    fetchGraphData();
  }, [fetchGraphData]);

  // Auto-fit graph when data changes
  useEffect(() => {
    if (filteredGraphData && filteredGraphData.nodes && filteredGraphData.nodes.length > 0) {
      // Small delay to ensure the graph has rendered
      const timer = setTimeout(() => {
        if (graphRef.current) {
          graphRef.current.zoomToFit(400, 20);
          graphRef.current.centerAt(0, 0, 1000);
        }
      }, 100);
      return () => clearTimeout(timer);
    }
  }, [filteredGraphData]);

  // Node click handler
  const handleNodeClick = useCallback((node: any) => {
    setSelectedNode(node);
  }, []);

  // Get node color based on labels
  const getNodeColor = useCallback((node: any) => {
    const primaryLabel = node.labels?.[0];
    return NODE_COLORS[primaryLabel as keyof typeof NODE_COLORS] || NODE_COLORS.default;
  }, []);

  // Get relationship color
  const getLinkColor = useCallback((link: any) => {
    return RELATIONSHIP_COLORS[link.type as keyof typeof RELATIONSHIP_COLORS] || RELATIONSHIP_COLORS.default;
  }, []);

  // Graph controls
  const zoomIn = () => graphRef.current?.zoom(1.2, 200);
  const zoomOut = () => graphRef.current?.zoom(0.8, 200);
  const resetView = () => {
    graphRef.current?.zoomToFit(400);
    graphRef.current?.centerAt(0, 0, 1000);
  };

  if (loading) {
    return (
      <GlassCard className={`p-6 ${className}`}>
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4 text-cyan-400" />
            <p className="text-slate-300">Loading Neo4j graph data...</p>
            <p className="text-slate-400 text-sm mt-2">Debug: Loading state active</p>
          </div>
        </div>
      </GlassCard>
    );
  }

  if (error) {
    return (
      <GlassCard className={`p-6 ${className}`}>
        <div className="text-center text-red-400">
          <p className="mb-4">Failed to load graph data: {error}</p>
          <p className="text-slate-400 text-sm mb-4">Debug: Error state active</p>
          <Button onClick={fetchGraphData} variant="outline">
            Retry
          </Button>
        </div>
      </GlassCard>
    );
  }

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Graph Statistics */}
      <GlassCard className="p-4">
        <div className="text-center">
          <h3 className="text-lg font-semibold text-slate-200 mb-2">Neo4j Graph Visualization</h3>
          <p className="text-slate-400">Status: {loading ? 'Loading...' : error ? 'Error' : 'Ready'}</p>
          <div className="grid grid-cols-2 gap-4 mt-3">
            <div>
              <p className="text-slate-300 text-sm">Total in Database</p>
              <p className="text-cyan-400 font-mono text-lg">
                {graphData.nodes.length > 0 ? `${graphData.nodes.length}+` : '0'} nodes
              </p>
            </div>
            <div>
              <p className="text-slate-300 text-sm">Total in Database</p>
              <p className="text-purple-400 font-mono text-lg">
                {graphData.relationships.length > 0 ? `${graphData.relationships.length}+` : '0'} relationships
              </p>
            </div>
          </div>
          <div className="mt-2 text-xs text-slate-500">
            Showing: {graphData.nodes.length} nodes, {graphData.relationships.length} relationships
          </div>
        </div>
      </GlassCard>

      {/* Controls */}
      <GlassCard className="p-4">
        <div className="flex flex-wrap items-center gap-4">
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
              <SelectValue placeholder="Relationship" />
            </SelectTrigger>
            <SelectContent className="bg-slate-800 border-slate-600">
              <SelectItem value="all" className="text-slate-200 hover:bg-slate-700">All Types</SelectItem>
              {relationshipTypes.map(type => (
                <SelectItem key={type} value={type} className="text-slate-200 hover:bg-slate-700">{type}</SelectItem>
              ))}
            </SelectContent>
          </Select>

          {/* Limits */}
          <div className="flex items-center gap-2">
            <label className="text-sm text-slate-300">Nodes:</label>
            <Input
              type="number"
              value={nodeLimit}
              onChange={(e) => setNodeLimit(Math.max(10, parseInt(e.target.value) || 50))}
              className="w-20 bg-slate-800/50 border-slate-600 text-slate-200"
              min="10"
              max="200"
            />
          </div>

          <div className="flex items-center gap-2">
            <label className="text-sm text-slate-300">Rels:</label>
            <Input
              type="number"
              value={relLimit}
              onChange={(e) => setRelLimit(Math.max(10, parseInt(e.target.value) || 100))}
              className="w-20 bg-slate-800/50 border-slate-600 text-slate-200"
              min="10"
              max="500"
            />
          </div>

          {/* View Controls */}
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowLabels(!showLabels)}
              className="border-slate-400 text-slate-100 bg-slate-700/50 hover:bg-slate-600/70 hover:border-slate-300"
            >
              {showLabels ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
            </Button>
            <Button 
              variant="outline" 
              size="sm" 
              onClick={zoomIn}
              className="border-slate-400 text-slate-100 bg-slate-700/50 hover:bg-slate-600/70 hover:border-slate-300"
            >
              <ZoomIn className="h-4 w-4" />
            </Button>
            <Button 
              variant="outline" 
              size="sm" 
              onClick={zoomOut}
              className="border-slate-400 text-slate-100 bg-slate-700/50 hover:bg-slate-600/70 hover:border-slate-300"
            >
              <ZoomOut className="h-4 w-4" />
            </Button>
            <Button 
              variant="outline" 
              size="sm" 
              onClick={resetView}
              className="border-slate-400 text-slate-100 bg-slate-700/50 hover:bg-slate-600/70 hover:border-slate-300"
            >
              <RotateCcw className="h-4 w-4" />
            </Button>
          </div>

          {/* Stats */}
          <div className="flex items-center gap-4 text-sm text-slate-300">
            <span>Showing {filteredGraphData.nodes.length} nodes</span>
            <span>{filteredGraphData.links.length} relationships</span>
            <span className="text-slate-500">(limited by controls above)</span>
          </div>
        </div>
      </GlassCard>

      {/* Graph Visualization */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
        <div className="lg:col-span-3">
          <GlassCard className="p-4">
            <div className="h-96 w-full relative">
              <div className="absolute top-2 left-2 z-10 bg-black/50 text-white text-xs p-2 rounded">
                Graph Data: {filteredGraphData?.nodes?.length || 0} nodes, {filteredGraphData?.links?.length || 0} links
              </div>
              {filteredGraphData && filteredGraphData.nodes && filteredGraphData.links ? (
                <ForceGraph2D
                  ref={graphRef}
                  graphData={filteredGraphData}
                  nodeLabel={(node: any) => showLabels ? node.name : ''}
                  nodeColor={getNodeColor}
                  nodeVal={(node: any) => Math.sqrt(node.labels?.length || 1) * 3}
                  linkColor={getLinkColor}
                  linkWidth={(link: any) => Math.sqrt(link.strength || 1) * 2}
                linkDirectionalArrowLength={6}
                linkDirectionalArrowRelPos={1}
                onNodeClick={handleNodeClick}
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
                  ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
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

        {/* Node Details Panel */}
        <div className="lg:col-span-1">
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
                    <div className="flex flex-wrap gap-1">
                      {selectedNode.labels.map((label, index) => (
                        <Badge key={index} variant="outline" className="text-xs border-slate-500 text-slate-200 bg-slate-800/30">
                          {label}
                        </Badge>
                      ))}
                    </div>
                  </div>
                  
                  <div>
                    <h5 className="font-medium text-slate-100 mb-2">Properties</h5>
                    <div className="space-y-1 text-sm">
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
                </div>
              ) : (
                <p className="text-slate-400 text-sm">Click on a node to view details</p>
              )}
            </CardContent>
          </GlassCard>
        </div>
      </div>
    </div>
  );
};
