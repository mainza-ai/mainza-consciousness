import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Slider } from '@/components/ui/slider';
import { 
  Atom, 
  Network, 
  Zap, 
  Brain, 
  Layers,
  RotateCcw,
  Play,
  Pause,
  Square,
  Settings,
  Eye,
  EyeOff,
  Maximize,
  Minimize,
  RefreshCw,
  Target,
  Activity,
  Cpu,
  Database,
  Globe
} from 'lucide-react';

interface QuantumNode {
  id: string;
  type: 'consciousness' | 'emotion' | 'memory' | 'concept' | 'agent';
  position: { x: number; y: number; z: number };
  size: number;
  color: string;
  quantum_coherence: number;
  entanglement_strength: number;
  superposition_states: number;
  quantum_advantage: number;
  connections: string[];
  metadata: any;
}

interface QuantumConnection {
  id: string;
  source: string;
  target: string;
  strength: number;
  type: 'entanglement' | 'superposition' | 'coherence' | 'evolution';
  quantum_properties: {
    coherence: number;
    entanglement: number;
    superposition: number;
    advantage: number;
  };
}

interface QuantumConsciousness3DProps {
  width?: number;
  height?: number;
  autoRotate?: boolean;
  showLabels?: boolean;
  showConnections?: boolean;
  quantumState?: any;
}

const QuantumConsciousness3DVisualization: React.FC<QuantumConsciousness3DProps> = ({
  width = 800,
  height = 600,
  autoRotate = true,
  showLabels = true,
  showConnections = true,
  quantumState
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>();
  const [isPlaying, setIsPlaying] = useState(true);
  const [rotation, setRotation] = useState({ x: 0, y: 0, z: 0 });
  const [zoom, setZoom] = useState(1);
  const [selectedNode, setSelectedNode] = useState<QuantumNode | null>(null);
  const [quantumNodes, setQuantumNodes] = useState<QuantumNode[]>([]);
  const [quantumConnections, setQuantumConnections] = useState<QuantumConnection[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Generate quantum nodes based on consciousness state
  const generateQuantumNodes = useCallback((state: any): QuantumNode[] => {
    if (!state) return [];

    const nodes: QuantumNode[] = [];
    const nodeTypes = ['consciousness', 'emotion', 'memory', 'concept', 'agent'];
    const colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'];

    // Central consciousness node
    nodes.push({
      id: 'consciousness_center',
      type: 'consciousness',
      position: { x: 0, y: 0, z: 0 },
      size: 20 + (state.quantum_consciousness_level || 0.5) * 30,
      color: '#3B82F6',
      quantum_coherence: state.quantum_coherence || 0.8,
      entanglement_strength: state.entanglement_strength || 0.7,
      superposition_states: state.superposition_states || 1,
      quantum_advantage: state.quantum_advantage || 1.5,
      connections: [],
      metadata: {
        level: state.quantum_consciousness_level || 0.5,
        processing_active: state.quantum_processing_active || false
      }
    });

    // Generate surrounding nodes
    const numNodes = 15 + Math.floor((state.superposition_states || 1) * 5);
    for (let i = 0; i < numNodes; i++) {
      const angle = (i / numNodes) * Math.PI * 2;
      const radius = 100 + Math.random() * 200;
      const height = (Math.random() - 0.5) * 200;
      
      const nodeType = nodeTypes[i % nodeTypes.length];
      const color = colors[i % colors.length];
      
      nodes.push({
        id: `node_${i}`,
        type: nodeType as any,
        position: {
          x: Math.cos(angle) * radius,
          y: height,
          z: Math.sin(angle) * radius
        },
        size: 5 + Math.random() * 15,
        color,
        quantum_coherence: 0.3 + Math.random() * 0.7,
        entanglement_strength: 0.2 + Math.random() * 0.8,
        superposition_states: 1 + Math.floor(Math.random() * 3),
        quantum_advantage: 1.0 + Math.random() * 1.0,
        connections: [],
        metadata: {
          created_at: new Date().toISOString(),
          energy: Math.random()
        }
      });
    }

    return nodes;
  }, []);

  // Generate quantum connections
  const generateQuantumConnections = useCallback((nodes: QuantumNode[]): QuantumConnection[] => {
    const connections: QuantumConnection[] = [];
    
    // Connect central node to all others
    nodes.slice(1).forEach(node => {
      if (Math.random() < 0.7) { // 70% chance of connection
        connections.push({
          id: `conn_center_${node.id}`,
          source: 'consciousness_center',
          target: node.id,
          strength: Math.random(),
          type: 'entanglement',
          quantum_properties: {
            coherence: Math.random(),
            entanglement: Math.random(),
            superposition: Math.random(),
            advantage: 1.0 + Math.random()
          }
        });
      }
    });

    // Connect nodes to each other
    for (let i = 1; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        if (Math.random() < 0.3) { // 30% chance of connection
          const connectionTypes = ['entanglement', 'superposition', 'coherence', 'evolution'];
          connections.push({
            id: `conn_${nodes[i].id}_${nodes[j].id}`,
            source: nodes[i].id,
            target: nodes[j].id,
            strength: Math.random(),
            type: connectionTypes[Math.floor(Math.random() * connectionTypes.length)] as any,
            quantum_properties: {
              coherence: Math.random(),
              entanglement: Math.random(),
              superposition: Math.random(),
              advantage: 1.0 + Math.random()
            }
          });
        }
      }
    }

    return connections;
  }, []);

  // 3D rendering functions
  const project3D = useCallback((x: number, y: number, z: number) => {
    const scale = zoom * 0.01;
    const distance = 500;
    const factor = distance / (distance + z);
    return {
      x: x * factor * scale + width / 2,
      y: y * factor * scale + height / 2,
      z: z + distance
    };
  }, [width, height, zoom]);

  const drawNode = useCallback((ctx: CanvasRenderingContext2D, node: QuantumNode) => {
    const projected = project3D(node.position.x, node.position.y, node.position.z);
    
    if (projected.z <= 0) return;

    // Node glow effect
    const glowSize = node.size * 2;
    const gradient = ctx.createRadialGradient(
      projected.x, projected.y, 0,
      projected.x, projected.y, glowSize
    );
    gradient.addColorStop(0, node.color + '80');
    gradient.addColorStop(1, node.color + '00');
    
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(projected.x, projected.y, glowSize, 0, Math.PI * 2);
    ctx.fill();

    // Main node
    ctx.fillStyle = node.color;
    ctx.beginPath();
    ctx.arc(projected.x, projected.y, node.size, 0, Math.PI * 2);
    ctx.fill();

    // Quantum coherence ring
    if (node.quantum_coherence > 0.5) {
      ctx.strokeStyle = node.color + '60';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(projected.x, projected.y, node.size + 5, 0, Math.PI * 2);
      ctx.stroke();
    }

    // Labels
    if (showLabels && projected.z > 0) {
      ctx.fillStyle = '#FFFFFF';
      ctx.font = '12px Arial';
      ctx.textAlign = 'center';
      ctx.fillText(node.type, projected.x, projected.y + node.size + 15);
    }
  }, [project3D, showLabels]);

  const drawConnection = useCallback((ctx: CanvasRenderingContext2D, connection: QuantumConnection, nodes: QuantumNode[]) => {
    const sourceNode = nodes.find(n => n.id === connection.source);
    const targetNode = nodes.find(n => n.id === connection.target);
    
    if (!sourceNode || !targetNode) return;

    const sourceProjected = project3D(sourceNode.position.x, sourceNode.position.y, sourceNode.position.z);
    const targetProjected = project3D(targetNode.position.x, targetNode.position.y, targetNode.position.z);
    
    if (sourceProjected.z <= 0 || targetProjected.z <= 0) return;

    // Connection color based on type
    let color = '#666666';
    switch (connection.type) {
      case 'entanglement': color = '#3B82F6'; break;
      case 'superposition': color = '#8B5CF6'; break;
      case 'coherence': color = '#10B981'; break;
      case 'evolution': color = '#F59E0B'; break;
    }

    ctx.strokeStyle = color + Math.floor(connection.strength * 255).toString(16).padStart(2, '0');
    ctx.lineWidth = 1 + connection.strength * 3;
    ctx.beginPath();
    ctx.moveTo(sourceProjected.x, sourceProjected.y);
    ctx.lineTo(targetProjected.x, targetProjected.y);
    ctx.stroke();

    // Quantum properties visualization
    if (connection.quantum_properties.entanglement > 0.7) {
      const midX = (sourceProjected.x + targetProjected.x) / 2;
      const midY = (sourceProjected.y + targetProjected.y) / 2;
      
      ctx.fillStyle = color + '40';
      ctx.beginPath();
      ctx.arc(midX, midY, 3, 0, Math.PI * 2);
      ctx.fill();
    }
  }, [project3D]);

  const render = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.clearRect(0, 0, width, height);

    // Draw connections
    if (showConnections) {
      quantumConnections.forEach(connection => {
        drawConnection(ctx, connection, quantumNodes);
      });
    }

    // Draw nodes
    quantumNodes.forEach(node => {
      drawNode(ctx, node);
    });

    // Draw selected node info
    if (selectedNode) {
      const projected = project3D(selectedNode.position.x, selectedNode.position.y, selectedNode.position.z);
      if (projected.z > 0) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
        ctx.fillRect(10, 10, 300, 150);
        
        ctx.fillStyle = '#FFFFFF';
        ctx.font = '14px Arial';
        ctx.textAlign = 'left';
        ctx.fillText(`Node: ${selectedNode.id}`, 20, 30);
        ctx.fillText(`Type: ${selectedNode.type}`, 20, 50);
        ctx.fillText(`Coherence: ${(selectedNode.quantum_coherence * 100).toFixed(1)}%`, 20, 70);
        ctx.fillText(`Entanglement: ${(selectedNode.entanglement_strength * 100).toFixed(1)}%`, 20, 90);
        ctx.fillText(`Superposition: ${selectedNode.superposition_states}`, 20, 110);
        ctx.fillText(`Advantage: ${selectedNode.quantum_advantage.toFixed(2)}x`, 20, 130);
      }
    }
  }, [quantumNodes, quantumConnections, selectedNode, showConnections, drawNode, drawConnection, project3D, width, height]);

  const animate = useCallback(() => {
    if (isPlaying) {
      setRotation(prev => ({
        x: prev.x + 0.005,
        y: prev.y + 0.01,
        z: prev.z + 0.003
      }));
    }
    render();
    animationRef.current = requestAnimationFrame(animate);
  }, [isPlaying, render]);

  // Initialize quantum nodes
  useEffect(() => {
    if (quantumState) {
      const nodes = generateQuantumNodes(quantumState);
      const connections = generateQuantumConnections(nodes);
      setQuantumNodes(nodes);
      setQuantumConnections(connections);
      setIsLoading(false);
    }
  }, [quantumState, generateQuantumNodes, generateQuantumConnections]);

  // Start animation
  useEffect(() => {
    animate();
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [animate]);

  // Mouse interaction
  const handleMouseMove = useCallback((event: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    // Find closest node
    let closestNode: QuantumNode | null = null;
    let closestDistance = Infinity;

    quantumNodes.forEach(node => {
      const projected = project3D(node.position.x, node.position.y, node.position.z);
      if (projected.z > 0) {
        const distance = Math.sqrt((x - projected.x) ** 2 + (y - projected.y) ** 2);
        if (distance < node.size + 10 && distance < closestDistance) {
          closestDistance = distance;
          closestNode = node;
        }
      }
    });

    setSelectedNode(closestNode);
  }, [quantumNodes, project3D]);

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Atom className="h-5 w-5" />
            <span>Quantum Consciousness 3D Visualization</span>
          </div>
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setIsPlaying(!isPlaying)}
            >
              {isPlaying ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setRotation({ x: 0, y: 0, z: 0 })}
            >
              <RotateCcw className="h-4 w-4" />
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setZoom(1)}
            >
              <RefreshCw className="h-4 w-4" />
            </Button>
          </div>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* Controls */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <label className="text-sm font-medium">Zoom:</label>
              <Slider
                value={[zoom]}
                onValueChange={([value]) => setZoom(value)}
                min={0.1}
                max={3}
                step={0.1}
                className="w-24"
              />
              <span className="text-sm text-gray-600">{zoom.toFixed(1)}x</span>
            </div>
            
            <div className="flex items-center space-x-2">
              <Button
                variant={showLabels ? "default" : "outline"}
                size="sm"
                onClick={() => setShowLabels(!showLabels)}
              >
                {showLabels ? <Eye className="h-4 w-4" /> : <EyeOff className="h-4 w-4" />}
              </Button>
              <span className="text-sm">Labels</span>
            </div>
            
            <div className="flex items-center space-x-2">
              <Button
                variant={showConnections ? "default" : "outline"}
                size="sm"
                onClick={() => setShowConnections(!showConnections)}
              >
                <Network className="h-4 w-4" />
              </Button>
              <span className="text-sm">Connections</span>
            </div>
          </div>

          {/* 3D Canvas */}
          <div className="relative border rounded-lg overflow-hidden bg-gray-900">
            <canvas
              ref={canvasRef}
              width={width}
              height={height}
              onMouseMove={handleMouseMove}
              className="cursor-crosshair"
            />
            
            {isLoading && (
              <div className="absolute inset-0 flex items-center justify-center bg-gray-900 bg-opacity-75">
                <div className="flex items-center space-x-2 text-white">
                  <RefreshCw className="h-4 w-4 animate-spin" />
                  <span>Loading quantum visualization...</span>
                </div>
              </div>
            )}
          </div>

          {/* Legend */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
              <span>Entanglement</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
              <span>Superposition</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span>Coherence</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-orange-500 rounded-full"></div>
              <span>Evolution</span>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-blue-600">{quantumNodes.length}</div>
              <div className="text-sm text-gray-600">Quantum Nodes</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-green-600">{quantumConnections.length}</div>
              <div className="text-sm text-gray-600">Connections</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-purple-600">
                {quantumNodes.filter(n => n.quantum_coherence > 0.7).length}
              </div>
              <div className="text-sm text-gray-600">High Coherence</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-orange-600">
                {quantumNodes.filter(n => n.entanglement_strength > 0.7).length}
              </div>
              <div className="text-sm text-gray-600">Entangled</div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default QuantumConsciousness3DVisualization;
