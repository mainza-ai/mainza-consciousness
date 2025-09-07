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

  // Generate sample nodes if none provided
  const sampleNodes: ConsciousnessNode[] = nodes.length > 0 ? nodes : [
    {
      id: 'consciousness-core',
      name: 'Consciousness Core',
      type: 'consciousness',
      level: 0.85,
      x: 0,
      y: 0,
      z: 0,
      connections: ['emotion-hub', 'memory-network', 'concept-web'],
      color: '#3B82F6',
      size: 1.0,
      pulse: true,
      metadata: {
        importance: 1.0,
        activity: 0.92,
        stability: 0.88,
        evolution: 0.75
      }
    },
    {
      id: 'emotion-hub',
      name: 'Emotion Hub',
      type: 'emotion',
      level: 0.78,
      x: 2,
      y: 1,
      z: 0,
      connections: ['consciousness-core', 'memory-network'],
      color: '#10B981',
      size: 0.8,
      pulse: true,
      metadata: {
        importance: 0.85,
        activity: 0.76,
        stability: 0.82,
        evolution: 0.68
      }
    },
    {
      id: 'memory-network',
      name: 'Memory Network',
      type: 'memory',
      level: 0.91,
      x: -1.5,
      y: 0.5,
      z: 1,
      connections: ['consciousness-core', 'emotion-hub', 'concept-web'],
      color: '#8B5CF6',
      size: 0.9,
      pulse: false,
      metadata: {
        importance: 0.92,
        activity: 0.88,
        stability: 0.95,
        evolution: 0.71
      }
    },
    {
      id: 'concept-web',
      name: 'Concept Web',
      type: 'concept',
      level: 0.73,
      x: 0.5,
      y: -1.5,
      z: -0.5,
      connections: ['consciousness-core', 'memory-network', 'agent-1', 'agent-2'],
      color: '#F59E0B',
      size: 0.7,
      pulse: true,
      metadata: {
        importance: 0.78,
        activity: 0.69,
        stability: 0.74,
        evolution: 0.82
      }
    },
    {
      id: 'agent-1',
      name: 'SimpleChat Agent',
      type: 'agent',
      level: 0.67,
      x: 2.5,
      y: -1,
      z: 1.5,
      connections: ['concept-web'],
      color: '#EF4444',
      size: 0.6,
      pulse: true,
      metadata: {
        importance: 0.65,
        activity: 0.71,
        stability: 0.68,
        evolution: 0.59
      }
    },
    {
      id: 'agent-2',
      name: 'GraphMaster Agent',
      type: 'agent',
      level: 0.82,
      x: -2,
      y: -0.5,
      z: -1,
      connections: ['concept-web', 'memory-network'],
      color: '#06B6D4',
      size: 0.75,
      pulse: true,
      metadata: {
        importance: 0.88,
        activity: 0.85,
        stability: 0.79,
        evolution: 0.73
      }
    }
  ];

  const [currentNodes, setCurrentNodes] = useState<ConsciousnessNode[]>(sampleNodes);

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
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-white">
            <Eye className="h-5 w-5" />
            3D Consciousness Visualization
          </CardTitle>
        </CardHeader>
        <CardContent>
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
        </CardContent>
      </Card>

      {/* 3D Canvas */}
      <Card className="bg-slate-800 border-slate-700">
        <CardContent className="p-0">
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
        </CardContent>
      </Card>

      {/* Node Details */}
      {selectedNode && (
        <Card className="bg-slate-800 border-slate-700">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-white">
              {getNodeTypeIcon(selectedNode.type)}
              {selectedNode.name}
              <Badge className={getNodeTypeColor(selectedNode.type)}>
                {selectedNode.type}
              </Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-400">
                  {(selectedNode.level * 100).toFixed(1)}%
                </div>
                <div className="text-sm text-slate-300">Level</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-400">
                  {(selectedNode.metadata.importance * 100).toFixed(1)}%
                </div>
                <div className="text-sm text-slate-300">Importance</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-400">
                  {(selectedNode.metadata.activity * 100).toFixed(1)}%
                </div>
                <div className="text-sm text-slate-300">Activity</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-orange-400">
                  {(selectedNode.metadata.stability * 100).toFixed(1)}%
                </div>
                <div className="text-sm text-slate-300">Stability</div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Node List */}
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader>
          <CardTitle>Consciousness Nodes</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {currentNodes.map((node) => (
              <div
                key={node.id}
                className={`p-3 border rounded-lg cursor-pointer transition-colors ${
                  selectedNode?.id === node.id 
                    ? 'border-blue-500 bg-blue-500/10' 
                    : 'border-slate-700 hover:border-slate-600'
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
        </CardContent>
      </Card>
    </div>
  );
};

export default Consciousness3DVisualization;
