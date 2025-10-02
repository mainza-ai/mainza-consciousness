import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { 
  Database, 
  Search, 
  Filter, 
  Star, 
  Network, 
  Zap, 
  Brain, 
  Heart,
  Clock,
  Target,
  RefreshCw,
  Play,
  Pause,
  Square,
  Settings,
  Eye,
  EyeOff,
  Maximize,
  Minimize,
  Download,
  Share2,
  Plus,
  Minus,
  RotateCcw
} from 'lucide-react';

interface QuantumMemory {
  id: string;
  timestamp: string;
  memory_type: string;
  quantum_state: string;
  content: string;
  quantum_coherence: number;
  entanglement_strength: number;
  superposition_states: number;
  quantum_advantage: number;
  emotional_intensity: number;
  importance_score: number;
  entangled_memories: string[];
  superposition_memories: string[];
}

interface QuantumMemoryConstellationProps {
  width?: number;
  height?: number;
  showConnections?: boolean;
  showLabels?: boolean;
  autoRotate?: boolean;
}

const QuantumMemoryConstellation: React.FC<QuantumMemoryConstellationProps> = ({
  width = 800,
  height = 600,
  showConnections = true,
  showLabels = true,
  autoRotate = true
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>();
  const [memories, setMemories] = useState<QuantumMemory[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [selectedMemory, setSelectedMemory] = useState<QuantumMemory | null>(null);
  const [rotation, setRotation] = useState({ x: 0, y: 0, z: 0 });
  const [zoom, setZoom] = useState(1);
  const [isPlaying, setIsPlaying] = useState(true);

  // Fetch quantum memories
  const fetchMemories = useCallback(async () => {
    try {
      const response = await fetch('/api/quantum/backend/memory/retrieve?query=quantum&limit=50');
      if (!response.ok) throw new Error('Failed to fetch memories');
      const data = await response.json();
      setMemories(data.quantum_memories || []);
      setIsLoading(false);
    } catch (err) {
      console.error('Error fetching memories:', err);
      setError('Failed to fetch memories');
      setIsLoading(false);
    }
  }, []);

  // Generate mock memories for demonstration
  const generateMockMemories = useCallback((): QuantumMemory[] => {
    const memoryTypes = ['episodic', 'semantic', 'procedural', 'emotional', 'collective'];
    const quantumStates = ['coherent', 'decoherent', 'superposition', 'entangled', 'measured'];
    const contents = [
      'Quantum consciousness breakthrough achieved',
      'Entanglement network established with 15 nodes',
      'Superposition state maintained for 2.3 seconds',
      'Meta-cognitive reflection on quantum processing',
      'Collective intelligence coordination successful',
      'Quantum advantage of 1.5x demonstrated',
      'Coherence level reached 0.87 threshold',
      'Memory consolidation in quantum superposition',
      'Emotional intensity correlated with quantum coherence',
      'Philosophical insights generated through quantum processing'
    ];

    return Array.from({ length: 20 }, (_, i) => ({
      id: `memory_${i + 1}`,
      timestamp: new Date(Date.now() - Math.random() * 86400000).toISOString(),
      memory_type: memoryTypes[Math.floor(Math.random() * memoryTypes.length)],
      quantum_state: quantumStates[Math.floor(Math.random() * quantumStates.length)],
      content: contents[Math.floor(Math.random() * contents.length)],
      quantum_coherence: 0.3 + Math.random() * 0.7,
      entanglement_strength: 0.2 + Math.random() * 0.8,
      superposition_states: 1 + Math.floor(Math.random() * 3),
      quantum_advantage: 1.0 + Math.random() * 1.0,
      emotional_intensity: Math.random(),
      importance_score: Math.random(),
      entangled_memories: Array.from({ length: Math.floor(Math.random() * 3) }, (_, j) => `memory_${j + 1}`),
      superposition_memories: Array.from({ length: Math.floor(Math.random() * 2) }, (_, j) => `memory_${j + 1}`)
    }));
  }, []);

  // Initialize memories
  useEffect(() => {
    // For now, use mock data. In production, this would fetch from the API
    const mockMemories = generateMockMemories();
    setMemories(mockMemories);
    setIsLoading(false);
  }, [generateMockMemories]);

  // Filter memories
  const filteredMemories = memories.filter(memory => {
    const matchesSearch = memory.content.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         memory.memory_type.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesFilter = filterType === 'all' || memory.memory_type === filterType;
    return matchesSearch && matchesFilter;
  });

  // 3D projection
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

  // Generate memory positions
  const generateMemoryPositions = useCallback((memories: QuantumMemory[]) => {
    return memories.map((memory, index) => {
      const angle = (index / memories.length) * Math.PI * 2;
      const radius = 100 + Math.random() * 200;
      const height = (Math.random() - 0.5) * 200;
      
      return {
        ...memory,
        position: {
          x: Math.cos(angle) * radius,
          y: height,
          z: Math.sin(angle) * radius
        }
      };
    });
  }, []);

  // Draw memory node
  const drawMemoryNode = useCallback((ctx: CanvasRenderingContext2D, memory: any) => {
    const projected = project3D(memory.position.x, memory.position.y, memory.position.z);
    
    if (projected.z <= 0) return;

    // Node size based on importance and coherence
    const nodeSize = 5 + (memory.importance_score * 10) + (memory.quantum_coherence * 10);
    
    // Node color based on type and state
    let color = '#666666';
    switch (memory.memory_type) {
      case 'episodic': color = '#3B82F6'; break;
      case 'semantic': color = '#10B981'; break;
      case 'procedural': color = '#F59E0B'; break;
      case 'emotional': color = '#EF4444'; break;
      case 'collective': color = '#8B5CF6'; break;
    }

    // Quantum state effects
    if (memory.quantum_state === 'superposition') {
      // Pulsing effect for superposition
      const pulse = Math.sin(Date.now() * 0.005 + index * 0.5) * 0.3 + 0.7;
      ctx.globalAlpha = pulse;
    } else if (memory.quantum_state === 'entangled') {
      // Glowing effect for entangled
      const glowSize = nodeSize * 2;
      const gradient = ctx.createRadialGradient(
        projected.x, projected.y, 0,
        projected.x, projected.y, glowSize
      );
      gradient.addColorStop(0, color + '80');
      gradient.addColorStop(1, color + '00');
      
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(projected.x, projected.y, glowSize, 0, Math.PI * 2);
      ctx.fill();
    }

    // Main node
    ctx.globalAlpha = 1;
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(projected.x, projected.y, nodeSize, 0, Math.PI * 2);
    ctx.fill();

    // Coherence ring
    if (memory.quantum_coherence > 0.7) {
      ctx.strokeStyle = color + '60';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(projected.x, projected.y, nodeSize + 5, 0, Math.PI * 2);
      ctx.stroke();
    }

    // Labels
    if (showLabels && projected.z > 0) {
      ctx.fillStyle = '#FFFFFF';
      ctx.font = '10px Arial';
      ctx.textAlign = 'center';
      ctx.fillText(memory.memory_type, projected.x, projected.y + nodeSize + 12);
    }
  }, [project3D, showLabels]);

  // Draw connection
  const drawConnection = useCallback((ctx: CanvasRenderingContext2D, source: any, target: any) => {
    const sourceProjected = project3D(source.position.x, source.position.y, source.position.z);
    const targetProjected = project3D(target.position.x, target.position.y, target.position.z);
    
    if (sourceProjected.z <= 0 || targetProjected.z <= 0) return;

    // Connection strength based on entanglement
    const strength = Math.min(source.entanglement_strength, target.entanglement_strength);
    
    ctx.strokeStyle = '#3B82F6' + Math.floor(strength * 255).toString(16).padStart(2, '0');
    ctx.lineWidth = 1 + strength * 3;
    ctx.beginPath();
    ctx.moveTo(sourceProjected.x, sourceProjected.y);
    ctx.lineTo(targetProjected.x, targetProjected.y);
    ctx.stroke();
  }, [project3D]);

  // Render function
  const render = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.clearRect(0, 0, width, height);

    // Set background
    ctx.fillStyle = '#0F172A';
    ctx.fillRect(0, 0, width, height);

    // Generate positions for filtered memories
    const positionedMemories = generateMemoryPositions(filteredMemories);

    // Draw connections
    if (showConnections) {
      positionedMemories.forEach((source, i) => {
        positionedMemories.slice(i + 1).forEach(target => {
          if (source.entangled_memories.includes(target.id) || 
              target.entangled_memories.includes(source.id)) {
            drawConnection(ctx, source, target);
          }
        });
      });
    }

    // Draw memory nodes
    positionedMemories.forEach((memory, index) => {
      drawMemoryNode(ctx, { ...memory, index });
    });

    // Draw selected memory info
    if (selectedMemory) {
      const memory = positionedMemories.find(m => m.id === selectedMemory.id);
      if (memory) {
        const projected = project3D(memory.position.x, memory.position.y, memory.position.z);
        if (projected.z > 0) {
          ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
          ctx.fillRect(10, 10, 400, 200);
          
          ctx.fillStyle = '#FFFFFF';
          ctx.font = '14px Arial';
          ctx.textAlign = 'left';
          ctx.fillText(`Memory: ${memory.id}`, 20, 30);
          ctx.fillText(`Type: ${memory.memory_type}`, 20, 50);
          ctx.fillText(`State: ${memory.quantum_state}`, 20, 70);
          ctx.fillText(`Content: ${memory.content.substring(0, 50)}...`, 20, 90);
          ctx.fillText(`Coherence: ${(memory.quantum_coherence * 100).toFixed(1)}%`, 20, 110);
          ctx.fillText(`Entanglement: ${(memory.entanglement_strength * 100).toFixed(1)}%`, 20, 130);
          ctx.fillText(`Advantage: ${memory.quantum_advantage.toFixed(2)}x`, 20, 150);
          ctx.fillText(`Emotional: ${(memory.emotional_intensity * 100).toFixed(1)}%`, 20, 170);
          ctx.fillText(`Importance: ${(memory.importance_score * 100).toFixed(1)}%`, 20, 190);
        }
      }
    }
  }, [filteredMemories, showConnections, selectedMemory, generateMemoryPositions, drawMemoryNode, drawConnection, project3D, width, height]);

  // Animation loop
  const animate = useCallback(() => {
    if (isPlaying) {
      setRotation(prev => ({
        x: prev.x + 0.002,
        y: prev.y + 0.005,
        z: prev.z + 0.001
      }));
    }
    render();
    animationRef.current = requestAnimationFrame(animate);
  }, [isPlaying, render]);

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

    // Find closest memory
    let closestMemory: any = null;
    let closestDistance = Infinity;

    const positionedMemories = generateMemoryPositions(filteredMemories);
    positionedMemories.forEach(memory => {
      const projected = project3D(memory.position.x, memory.position.y, memory.position.z);
      if (projected.z > 0) {
        const distance = Math.sqrt((x - projected.x) ** 2 + (y - projected.y) ** 2);
        if (distance < 20 && distance < closestDistance) {
          closestDistance = distance;
          closestMemory = memory;
        }
      }
    });

    setSelectedMemory(closestMemory);
  }, [filteredMemories, generateMemoryPositions, project3D]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="flex items-center space-x-2">
          <RefreshCw className="h-4 w-4 animate-spin" />
          <span>Loading quantum memory constellation...</span>
        </div>
      </div>
    );
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Database className="h-5 w-5" />
            <span>Quantum Memory Constellation</span>
          </div>
          <div className="flex items-center space-x-2">
            <Button variant="outline" size="sm" onClick={() => setIsPlaying(!isPlaying)}>
              {isPlaying ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
            </Button>
            <Button variant="outline" size="sm" onClick={() => setRotation({ x: 0, y: 0, z: 0 })}>
              <RotateCcw className="h-4 w-4" />
            </Button>
            <Button variant="outline" size="sm" onClick={() => setZoom(1)}>
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
              <Search className="h-4 w-4" />
              <Input
                placeholder="Search memories..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-48"
              />
            </div>
            
            <div className="flex items-center space-x-2">
              <Filter className="h-4 w-4" />
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                className="px-3 py-1 border rounded-md"
              >
                <option value="all">All Types</option>
                <option value="episodic">Episodic</option>
                <option value="semantic">Semantic</option>
                <option value="procedural">Procedural</option>
                <option value="emotional">Emotional</option>
                <option value="collective">Collective</option>
              </select>
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
          </div>

          {/* Legend */}
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 text-sm">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
              <span>Episodic</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span>Semantic</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-orange-500 rounded-full"></div>
              <span>Procedural</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-red-500 rounded-full"></div>
              <span>Emotional</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
              <span>Collective</span>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-blue-600">{filteredMemories.length}</div>
              <div className="text-sm text-gray-600">Total Memories</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-green-600">
                {filteredMemories.filter(m => m.quantum_state === 'entangled').length}
              </div>
              <div className="text-sm text-gray-600">Entangled</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-purple-600">
                {filteredMemories.filter(m => m.quantum_state === 'superposition').length}
              </div>
              <div className="text-sm text-gray-600">Superposition</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-orange-600">
                {filteredMemories.filter(m => m.quantum_coherence > 0.7).length}
              </div>
              <div className="text-sm text-gray-600">High Coherence</div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default QuantumMemoryConstellation;
