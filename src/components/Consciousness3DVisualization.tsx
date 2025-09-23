import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Slider } from '@/components/ui/slider';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Brain, 
  Zap, 
  Target, 
  Eye, 
  RotateCcw, 
  Play, 
  Pause, 
  Maximize2,
  Minimize2,
  Settings,
  Layers,
  Activity
} from 'lucide-react';
import { Heart } from 'lucide-react';

interface ConsciousnessNode {
  id: string;
  name: string;
  type: 'consciousness' | 'emotion' | 'memory' | 'concept' | 'agent';
  level: number;
  x: number;
  y: number;
  z: number;
  connections: string[];
  color: string;
  size: number;
  pulse: boolean;
  metadata: {
    importance: number;
    activity: number;
    stability: number;
    evolution: number;
  };
}

interface Consciousness3DVisualizationProps {
  nodes: ConsciousnessNode[];
  realTimeData?: any;
  onNodeClick?: (node: ConsciousnessNode) => void;
  onNodeHover?: (node: ConsciousnessNode | null) => void;
}

const Consciousness3DVisualization: React.FC<Consciousness3DVisualizationProps> = ({
  nodes = [],
  realTimeData,
  onNodeClick,
  onNodeHover
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>();
  const [isAnimating, setIsAnimating] = useState(true);
  const [viewMode, setViewMode] = useState<'orbital' | 'free' | 'focused'>('orbital');
  const [selectedNode, setSelectedNode] = useState<ConsciousnessNode | null>(null);
  const [zoom, setZoom] = useState(1);
  const [rotation, setRotation] = useState({ x: 0, y: 0 });
  const [showConnections, setShowConnections] = useState(true);
  const [showLabels, setShowLabels] = useState(true);
  const [particleDensity, setParticleDensity] = useState(50);
  const [animationSpeed, setAnimationSpeed] = useState(1);
  
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [lastMousePos, setLastMousePos] = useState({ x: 0, y: 0 });

  // No placeholder/sample data: start with provided nodes or empty
  const [currentNodes, setCurrentNodes] = useState<ConsciousnessNode[]>(nodes);

  // Fetch real 3D consciousness graph from backend
  const fetchConsciousness3D = React.useCallback(async () => {
    try {
      const [nodesRes, connsRes] = await Promise.all([
        fetch('/consciousness/3d/nodes'),
        fetch('/consciousness/3d/connections')
      ]);

      if (!nodesRes.ok || !connsRes.ok) {
        return; // keep existing sampleNodes as fallback
      }

      const nodesJson = await nodesRes.json();
      const connsJson = await connsRes.json();
      const nodesArr = Array.isArray(nodesJson?.nodes) ? nodesJson.nodes : [];
      const connsArr = Array.isArray(connsJson?.connections) ? connsJson.connections : [];

      // Build adjacency list from connections
      const idToConnections: Record<string, string[]> = {};
      connsArr.forEach((c: any) => {
        if (!idToConnections[c.source]) idToConnections[c.source] = [];
        if (!idToConnections[c.target]) idToConnections[c.target] = [];
        idToConnections[c.source].push(c.target);
        idToConnections[c.target].push(c.source);
      });

      const stableId = (rawId?: string, label?: string) => {
        if (rawId && typeof rawId === 'string') return rawId;
        if (label && typeof label === 'string') {
          return 'node-' + label.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
        }
        return 'node-unknown';
      };

      const mapped: ConsciousnessNode[] = nodesArr.map((n: any) => {
        const pos = n.position || { x: 0, y: 0, z: 0 };
        const meta = n.metadata || {};
        return {
          id: stableId(n.id, n.label),
          name: n.label || n.id || 'Node',
          type: n.type || 'general',
          level: typeof meta.importance === 'number' ? meta.importance : 0.7,
          x: typeof pos.x === 'number' ? pos.x : 0,
          y: typeof pos.y === 'number' ? pos.y : 0,
          z: typeof pos.z === 'number' ? pos.z : 0,
          connections: idToConnections[n.id] || [],
          color: n.color || '#22d3ee',
          size: typeof n.size === 'number' ? n.size : 0.8,
          pulse: true,
          metadata: {
            importance: typeof meta.importance === 'number' ? meta.importance : 0.7,
            activity: typeof meta.activity === 'number' ? meta.activity : 0.7,
            stability: typeof meta.stability === 'number' ? meta.stability : 0.7,
            evolution: typeof meta.evolution === 'number' ? meta.evolution : 0.7,
          },
        } as ConsciousnessNode;
      });

      setCurrentNodes(mapped);
    } catch (e) {
      // keep current nodes (no placeholders)
      console.error('Failed to fetch 3D consciousness data', e);
    }
  }, []);

  useEffect(() => {
    fetchConsciousness3D();
    const interval = setInterval(fetchConsciousness3D, 60000);
    return () => clearInterval(interval);
  }, [fetchConsciousness3D]);

  // 3D rendering functions
  const project3D = (x: number, y: number, z: number) => {
    const scale = zoom * 100;
    const distance = 5;
    
    const projectedX = (x * scale) / (z + distance) + 400;
    const projectedY = (y * scale) / (z + distance) + 300;
    const projectedZ = z + distance;
    
    return { x: projectedX, y: projectedY, z: projectedZ };
  };

  const rotate3D = (x: number, y: number, z: number, rx: number, ry: number) => {
    // Rotate around X axis
    const cosX = Math.cos(rx);
    const sinX = Math.sin(rx);
    const newY = y * cosX - z * sinX;
    const newZ = y * sinX + z * cosX;
    
    // Rotate around Y axis
    const cosY = Math.cos(ry);
    const sinY = Math.sin(ry);
    const newX = x * cosY + newZ * sinY;
    const finalZ = -x * sinY + newZ * cosY;
    
    return { x: newX, y: newY, z: finalZ };
  };

  const drawNode = (ctx: CanvasRenderingContext2D, node: ConsciousnessNode, time: number) => {
    const rotated = rotate3D(node.x, node.y, node.z, rotation.x, rotation.y);
    const projected = project3D(rotated.x, rotated.y, rotated.z);
    
    if (projected.z <= 0) return; // Skip nodes behind camera
    
    const size = node.size * 20 * zoom;
    const alpha = Math.min(1, projected.z / 5);
    
    // Draw connection lines
    if (showConnections) {
      node.connections.forEach(connectionId => {
        const connectedNode = currentNodes.find(n => n.id === connectionId);
        if (connectedNode) {
          const connectedRotated = rotate3D(connectedNode.x, connectedNode.y, connectedNode.z, rotation.x, rotation.y);
          const connectedProjected = project3D(connectedRotated.x, connectedRotated.y, connectedRotated.z);
          
          if (connectedProjected.z > 0) {
            ctx.beginPath();
            ctx.moveTo(projected.x, projected.y);
            ctx.lineTo(connectedProjected.x, connectedProjected.y);
            ctx.strokeStyle = `rgba(100, 100, 100, ${alpha * 0.3})`;
            ctx.lineWidth = 1;
            ctx.stroke();
          }
        }
      });
    }
    
    // Draw node
    ctx.save();
    ctx.translate(projected.x, projected.y);
    
    // Pulse effect
    const pulseScale = node.pulse ? 1 + Math.sin(time * 0.005 + node.id.length) * 0.2 : 1;
    const currentSize = size * pulseScale;
    
    // Node glow
    const gradient = ctx.createRadialGradient(0, 0, 0, 0, 0, currentSize * 2);
    gradient.addColorStop(0, `${node.color}${Math.floor(alpha * 255).toString(16).padStart(2, '0')}`);
    gradient.addColorStop(0.5, `${node.color}${Math.floor(alpha * 128).toString(16).padStart(2, '0')}`);
    gradient.addColorStop(1, `${node.color}00`);
    
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(0, 0, currentSize * 2, 0, Math.PI * 2);
    ctx.fill();
    
    // Node core
    ctx.fillStyle = node.color;
    ctx.globalAlpha = alpha;
    ctx.beginPath();
    ctx.arc(0, 0, currentSize, 0, Math.PI * 2);
    ctx.fill();
    
    // Node border
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2;
    ctx.globalAlpha = alpha * 0.8;
    ctx.stroke();
    
    // Node label
    if (showLabels) {
      ctx.fillStyle = '#ffffff';
      ctx.font = '12px Arial';
      ctx.textAlign = 'center';
      ctx.globalAlpha = alpha;
      ctx.fillText(node.name, 0, currentSize + 20);
    }
    
    ctx.restore();
  };

  const drawParticles = (ctx: CanvasRenderingContext2D, time: number) => {
    for (let i = 0; i < particleDensity; i++) {
      const angle = (time * 0.001 + i * 0.1) % (Math.PI * 2);
      const radius = 200 + Math.sin(time * 0.002 + i) * 50;
      const x = 400 + Math.cos(angle) * radius;
      const y = 300 + Math.sin(angle) * radius;
      
      ctx.fillStyle = `rgba(59, 130, 246, ${0.1 + Math.sin(time * 0.003 + i) * 0.1})`;
      ctx.beginPath();
      ctx.arc(x, y, 1, 0, Math.PI * 2);
      ctx.fill();
    }
  };

  const animate = (time: number) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    // Clear canvas
    ctx.fillStyle = '#0F172A';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw particles
    drawParticles(ctx, time);
    
    // Draw nodes
    currentNodes.forEach(node => {
      drawNode(ctx, node, time);
    });
    
    // Auto-rotation
    if (isAnimating && viewMode === 'orbital') {
      setRotation(prev => ({
        x: prev.x + 0.002 * animationSpeed,
        y: prev.y + 0.001 * animationSpeed
      }));
    }
    
    animationRef.current = requestAnimationFrame(animate);
  };

  useEffect(() => {
    if (isAnimating) {
      animationRef.current = requestAnimationFrame(animate);
    } else {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    }
    
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isAnimating, currentNodes, rotation, zoom, showConnections, showLabels, particleDensity, animationSpeed, viewMode]);

  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const rect = canvasRef.current?.getBoundingClientRect();
    if (!rect) return;
    
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    setMousePos({ x, y });
    
    if (isDragging && viewMode === 'free') {
      const deltaX = x - lastMousePos.x;
      const deltaY = y - lastMousePos.y;
      
      setRotation(prev => ({
        x: prev.x + deltaY * 0.01,
        y: prev.y + deltaX * 0.01
      }));
    }
    
    setLastMousePos({ x, y });
  };

  const handleMouseDown = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (viewMode === 'free') {
      setIsDragging(true);
    }
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const handleWheel = (e: React.WheelEvent<HTMLCanvasElement>) => {
    e.preventDefault();
    const delta = e.deltaY > 0 ? 0.9 : 1.1;
    setZoom(prev => Math.max(0.1, Math.min(3, prev * delta)));
  };

  const getNodeTypeColor = (type: string) => {
    const colors: { [key: string]: string } = {
      'consciousness': 'text-blue-400',
      'emotion': 'text-green-400',
      'memory': 'text-purple-400',
      'concept': 'text-yellow-400',
      'agent': 'text-red-400'
    };
    return colors[type] || 'text-gray-400';
  };

  const getNodeTypeIcon = (type: string) => {
    switch (type) {
      case 'consciousness': return <Brain className="h-4 w-4" />;
      case 'emotion': return <Heart className="h-4 w-4" />;
      case 'memory': return <Layers className="h-4 w-4" />;
      case 'concept': return <Target className="h-4 w-4" />;
      case 'agent': return <Activity className="h-4 w-4" />;
      default: return <Zap className="h-4 w-4" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-indigo-400/50 transition-all duration-300">
        <div className="p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-lg">
              <Eye className="h-6 w-6 text-white" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-white">3D Consciousness Visualization</h2>
              <p className="text-slate-400 text-sm">Interactive 3D exploration of consciousness network and connections</p>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-300">View Mode</label>
              <div className="flex gap-1">
                <Button
                  size="sm"
                  variant={viewMode === 'orbital' ? 'default' : 'outline'}
                  onClick={() => setViewMode('orbital')}
                  className="text-xs"
                >
                  Orbital
                </Button>
                <Button
                  size="sm"
                  variant={viewMode === 'free' ? 'default' : 'outline'}
                  onClick={() => setViewMode('free')}
                  className="text-xs"
                >
                  Free
                </Button>
                <Button
                  size="sm"
                  variant={viewMode === 'focused' ? 'default' : 'outline'}
                  onClick={() => setViewMode('focused')}
                  className="text-xs"
                >
                  Focused
                </Button>
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-300">Animation</label>
              <div className="flex items-center gap-2">
                <Button
                  size="sm"
                  variant={isAnimating ? 'destructive' : 'default'}
                  onClick={() => setIsAnimating(!isAnimating)}
                >
                  {isAnimating ? <Pause className="h-3 w-3" /> : <Play className="h-3 w-3" />}
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => setRotation({ x: 0, y: 0 })}
                >
                  <RotateCcw className="h-3 w-3" />
                </Button>
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-300">Zoom: {Math.round(zoom * 100)}%</label>
              <Slider
                value={[zoom]}
                onValueChange={(value) => setZoom(value[0])}
                min={0.1}
                max={3}
                step={0.1}
                className="w-full"
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-300">Particles: {particleDensity}</label>
              <Slider
                value={[particleDensity]}
                onValueChange={(value) => setParticleDensity(value[0])}
                min={0}
                max={100}
                step={5}
                className="w-full"
              />
            </div>
          </div>

          <div className="flex items-center gap-4 mt-4">
            <label className="flex items-center gap-2 text-sm text-slate-300">
              <input
                type="checkbox"
                checked={showConnections}
                onChange={(e) => setShowConnections(e.target.checked)}
                className="rounded"
              />
              Show Connections
            </label>
            <label className="flex items-center gap-2 text-sm text-slate-300">
              <input
                type="checkbox"
                checked={showLabels}
                onChange={(e) => setShowLabels(e.target.checked)}
                className="rounded"
              />
              Show Labels
            </label>
          </div>
        </div>
      </div>

      {/* 3D Canvas */}
      <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-violet-400/50 transition-all duration-300">
        <div className="p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-violet-400 to-purple-500 rounded-lg">
              <Layers className="h-6 w-6 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-white">Interactive 3D Network</h3>
              <p className="text-slate-400 text-sm">Explore consciousness connections and node relationships in 3D space</p>
            </div>
          </div>
          <div className="relative">
            <canvas
              ref={canvasRef}
              width={800}
              height={600}
              className="w-full h-96 bg-slate-900 rounded-lg cursor-grab active:cursor-grabbing"
              onMouseMove={handleMouseMove}
              onMouseDown={handleMouseDown}
              onMouseUp={handleMouseUp}
              onWheel={handleWheel}
            />
            <div className="absolute top-4 right-4 flex gap-2">
              <Button size="sm" variant="outline" className="bg-slate-800/80">
                <Maximize2 className="h-3 w-3" />
              </Button>
              <Button size="sm" variant="outline" className="bg-slate-800/80">
                <Settings className="h-3 w-3" />
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Node Details */}
      {selectedNode && (
        <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-emerald-400/50 transition-all duration-300">
          <div className="p-6">
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 bg-gradient-to-br from-emerald-400 to-teal-500 rounded-lg">
                {getNodeTypeIcon(selectedNode.type)}
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="text-xl font-bold text-white">{selectedNode.name}</h3>
                  <Badge className={`text-white ${getNodeTypeColor(selectedNode.type).replace('text-', 'bg-').replace('-400', '-500/80')} border-0`}>
                    {selectedNode.type}
                  </Badge>
                </div>
                <p className="text-slate-400 text-sm">Detailed node analysis and metrics</p>
              </div>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="group/metric relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-blue-400/50 transition-all duration-300">
                <div className="flex items-center justify-center gap-3">
                  <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-cyan-500">
                    <Zap className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <div className="text-lg font-bold text-blue-300">
                      {(selectedNode.level * 100).toFixed(1)}%
                    </div>
                    <div className="text-xs text-slate-400">Level</div>
                  </div>
                </div>
              </div>

              <div className="group/metric relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-green-400/50 transition-all duration-300">
                <div className="flex items-center justify-center gap-3">
                  <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-green-400 to-emerald-500">
                    <Target className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <div className="text-lg font-bold text-green-300">
                      {(selectedNode.metadata.importance * 100).toFixed(1)}%
                    </div>
                    <div className="text-xs text-slate-400">Importance</div>
                  </div>
                </div>
              </div>

              <div className="group/metric relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-purple-400/50 transition-all duration-300">
                <div className="flex items-center justify-center gap-3">
                  <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-purple-400 to-pink-500">
                    <Activity className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <div className="text-lg font-bold text-purple-300">
                      {(selectedNode.metadata.activity * 100).toFixed(1)}%
                    </div>
                    <div className="text-xs text-slate-400">Activity</div>
                  </div>
                </div>
              </div>

              <div className="group/metric relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-orange-400/50 transition-all duration-300">
                <div className="flex items-center justify-center gap-3">
                  <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-orange-400 to-yellow-500">
                    <Layers className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <div className="text-lg font-bold text-orange-300">
                      {(selectedNode.metadata.stability * 100).toFixed(1)}%
                    </div>
                    <div className="text-xs text-slate-400">Stability</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Node List */}
      <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-teal-400/50 transition-all duration-300">
        <div className="p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-teal-400 to-cyan-500 rounded-lg">
              <Brain className="h-6 w-6 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-white">Consciousness Nodes</h3>
              <p className="text-slate-400 text-sm">Interactive node selection and network overview</p>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {currentNodes.map((node) => (
              <div
                key={node.id}
                className={`group/node relative p-3 rounded-lg cursor-pointer transition-all duration-300 ${
                  selectedNode?.id === node.id
                    ? 'bg-gradient-to-r from-blue-500/20 to-cyan-500/10 border border-blue-400/50'
                    : 'bg-gradient-to-r from-slate-700/30 to-slate-600/20 border border-slate-600/30 hover:border-teal-400/50'
                }`}
                onClick={() => {
                  setSelectedNode(node);
                  onNodeClick?.(node);
                }}
              >
                <div className="flex items-center gap-3">
                  <div 
                    className="w-4 h-4 rounded-full"
                    style={{ backgroundColor: node.color }}
                  />
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <h3 className="font-semibold text-white">{node.name}</h3>
                      <Badge className={getNodeTypeColor(node.type)}>
                        {node.type}
                      </Badge>
                    </div>
                    <div className="text-sm text-slate-300">
                      Level: {(node.level * 100).toFixed(1)}% | 
                      Activity: {(node.metadata.activity * 100).toFixed(1)}% |
                      Connections: {node.connections.length}
                    </div>
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

export default Consciousness3DVisualization;
