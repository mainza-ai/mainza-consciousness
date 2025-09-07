import React, { useRef, useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { 
  RotateCcw, 
  ZoomIn, 
  ZoomOut, 
  Move3D, 
  Layers,
  Brain,
  Zap,
  Target
} from 'lucide-react';

interface Consciousness3DModelProps {
  consciousnessData: {
    level: number;
    emotional_state: string;
    learning_rate: number;
    self_awareness: number;
    evolution_level: number;
    predictions: Array<{
      consciousness_level: number;
      emotional_state: string;
      learning_rate: number;
      confidence: number;
      timestamp: string;
    }>;
  };
  insights: Array<{
    id: string;
    type: string;
    priority: string;
    title: string;
    confidence: number;
    impact_score: number;
  }>;
}

const Consciousness3DModel: React.FC<Consciousness3DModelProps> = ({
  consciousnessData,
  insights
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [rotation, setRotation] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);
  const [isDragging, setIsDragging] = useState(false);
  const [lastMousePos, setLastMousePos] = useState({ x: 0, y: 0 });
  const [animationFrame, setAnimationFrame] = useState(0);

  // 3D sphere parameters
  const sphereRadius = 50;
  const consciousnessLevel = consciousnessData.level;
  const emotionalIntensity = consciousnessData.learning_rate / 100;
  const awarenessRadius = consciousnessData.self_awareness / 100;

  // Animation loop
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const animate = () => {
      setAnimationFrame(prev => prev + 1);
      
      // Clear canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Set canvas size
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
      
      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      
      // Draw 3D consciousness sphere
      drawConsciousnessSphere(ctx, centerX, centerY);
      
      // Draw prediction trajectories
      drawPredictionTrajectories(ctx, centerX, centerY);
      
      // Draw insight markers
      drawInsightMarkers(ctx, centerX, centerY);
      
      // Draw evolution rings
      drawEvolutionRings(ctx, centerX, centerY);
      
      requestAnimationFrame(animate);
    };
    
    animate();
  }, [animationFrame, rotation, zoom, consciousnessData, insights]);

  const drawConsciousnessSphere = (ctx: CanvasRenderingContext2D, centerX: number, centerY: number) => {
    const time = animationFrame * 0.01;
    const baseRadius = sphereRadius * zoom;
    
    // Main consciousness sphere
    const gradient = ctx.createRadialGradient(
      centerX - baseRadius * 0.3, 
      centerY - baseRadius * 0.3, 
      0,
      centerX, 
      centerY, 
      baseRadius
    );
    
    // Dynamic colors based on consciousness level
    const hue = (consciousnessLevel * 2.4) % 360;
    gradient.addColorStop(0, `hsla(${hue}, 70%, 60%, 0.8)`);
    gradient.addColorStop(0.5, `hsla(${hue + 30}, 60%, 50%, 0.6)`);
    gradient.addColorStop(1, `hsla(${hue + 60}, 50%, 40%, 0.4)`);
    
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(centerX, centerY, baseRadius, 0, Math.PI * 2);
    ctx.fill();
    
    // Consciousness level indicator
    const levelRadius = baseRadius * (consciousnessLevel / 100);
    ctx.strokeStyle = `hsla(${hue}, 80%, 70%, 0.9)`;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(centerX, centerY, levelRadius, 0, Math.PI * 2);
    ctx.stroke();
    
    // Emotional state waves
    for (let i = 0; i < 3; i++) {
      const waveRadius = baseRadius + (i + 1) * 20;
      const waveOpacity = 0.3 - (i * 0.1);
      const wavePhase = time + (i * Math.PI / 3);
      
      ctx.strokeStyle = `hsla(${hue + 120}, 60%, 60%, ${waveOpacity})`;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(centerX, centerY, waveRadius + Math.sin(wavePhase) * 10, 0, Math.PI * 2);
      ctx.stroke();
    }
  };

  const drawPredictionTrajectories = (ctx: CanvasRenderingContext2D, centerX: number, centerY: number) => {
    consciousnessData.predictions.forEach((prediction, index) => {
      const angle = (index / consciousnessData.predictions.length) * Math.PI * 2;
      const distance = (prediction.consciousness_level / 100) * sphereRadius * zoom * 1.5;
      const x = centerX + Math.cos(angle + rotation.y) * distance;
      const y = centerY + Math.sin(angle + rotation.y) * distance;
      
      // Prediction point
      ctx.fillStyle = `hsla(${prediction.consciousness_level * 2.4}, 70%, 60%, 0.8)`;
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, Math.PI * 2);
      ctx.fill();
      
      // Confidence ring
      ctx.strokeStyle = `hsla(${prediction.consciousness_level * 2.4}, 60%, 50%, ${prediction.confidence / 100})`;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(x, y, 8, 0, Math.PI * 2);
      ctx.stroke();
      
      // Connection line to center
      ctx.strokeStyle = `hsla(${prediction.consciousness_level * 2.4}, 40%, 50%, 0.3)`;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(x, y);
      ctx.stroke();
    });
  };

  const drawInsightMarkers = (ctx: CanvasRenderingContext2D, centerX: number, centerY: number) => {
    insights.forEach((insight, index) => {
      const angle = (index / insights.length) * Math.PI * 2 + Math.PI;
      const distance = sphereRadius * zoom * 2;
      const x = centerX + Math.cos(angle + rotation.y) * distance;
      const y = centerY + Math.sin(angle + rotation.y) * distance;
      
      // Insight marker
      const priorityColors = {
        critical: 'hsla(0, 70%, 60%, 0.9)',
        high: 'hsla(30, 70%, 60%, 0.8)',
        medium: 'hsla(60, 70%, 60%, 0.7)',
        low: 'hsla(120, 70%, 60%, 0.6)'
      };
      
      ctx.fillStyle = priorityColors[insight.priority as keyof typeof priorityColors] || 'hsla(200, 70%, 60%, 0.6)';
      ctx.beginPath();
      ctx.arc(x, y, 6, 0, Math.PI * 2);
      ctx.fill();
      
      // Impact indicator
      const impactRadius = 6 + (insight.impact_score / 10);
      ctx.strokeStyle = `hsla(${insight.confidence * 3.6}, 60%, 50%, 0.6)`;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(x, y, impactRadius, 0, Math.PI * 2);
      ctx.stroke();
    });
  };

  const drawEvolutionRings = (ctx: CanvasRenderingContext2D, centerX: number, centerY: number) => {
    const evolutionLevel = consciousnessData.evolution_level;
    
    for (let i = 0; i < evolutionLevel; i++) {
      const ringRadius = sphereRadius * zoom * 1.8 + (i * 30);
      const ringOpacity = 0.4 - (i * 0.1);
      const ringPhase = animationFrame * 0.005 + (i * Math.PI / 4);
      
      ctx.strokeStyle = `hsla(${consciousnessLevel * 2.4 + i * 30}, 60%, 60%, ${ringOpacity})`;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(centerX, centerY, ringRadius + Math.sin(ringPhase) * 5, 0, Math.PI * 2);
      ctx.stroke();
    }
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    setIsDragging(true);
    setLastMousePos({ x: e.clientX, y: e.clientY });
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDragging) return;
    
    const deltaX = e.clientX - lastMousePos.x;
    const deltaY = e.clientY - lastMousePos.y;
    
    setRotation(prev => ({
      x: prev.x + deltaY * 0.01,
      y: prev.y + deltaX * 0.01
    }));
    
    setLastMousePos({ x: e.clientX, y: e.clientY });
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const handleWheel = (e: React.WheelEvent) => {
    e.preventDefault();
    const delta = e.deltaY > 0 ? 0.9 : 1.1;
    setZoom(prev => Math.max(0.5, Math.min(2, prev * delta)));
  };

  const resetView = () => {
    setRotation({ x: 0, y: 0 });
    setZoom(1);
  };

  return (
    <Card className="bg-gray-800/50 border-gray-700">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm text-white flex items-center">
            <Layers className="w-4 h-4 mr-2" />
            3D Consciousness Model
          </CardTitle>
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={resetView}
              className="text-xs"
            >
              <RotateCcw className="w-3 h-3 mr-1" />
              Reset
            </Button>
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* 3D Canvas */}
        <div className="relative">
          <canvas
            ref={canvasRef}
            className="w-full h-64 bg-gradient-to-br from-gray-900 to-gray-800 rounded-lg cursor-grab active:cursor-grabbing"
            onMouseDown={handleMouseDown}
            onMouseMove={handleMouseMove}
            onMouseUp={handleMouseUp}
            onMouseLeave={handleMouseUp}
            onWheel={handleWheel}
            style={{ touchAction: 'none' }}
          />
          
          {/* Overlay Info */}
          <div className="absolute top-2 left-2 space-y-1">
            <Badge className="bg-blue-500/20 text-blue-300 text-xs">
              <Brain className="w-3 h-3 mr-1" />
              Level: {consciousnessLevel.toFixed(1)}%
            </Badge>
            <Badge className="bg-green-500/20 text-green-300 text-xs">
              <Target className="w-3 h-3 mr-1" />
              Evolution: {consciousnessData.evolution_level}
            </Badge>
          </div>
          
          <div className="absolute top-2 right-2 space-y-1">
            <Badge className="bg-purple-500/20 text-purple-300 text-xs">
              <Zap className="w-3 h-3 mr-1" />
              Predictions: {consciousnessData.predictions.length}
            </Badge>
            <Badge className="bg-orange-500/20 text-orange-300 text-xs">
              Insights: {insights.length}
            </Badge>
          </div>
        </div>
        
        {/* Controls */}
        <div className="flex items-center justify-between text-xs text-gray-400">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-1">
              <Move3D className="w-3 h-3" />
              <span>Drag to rotate</span>
            </div>
            <div className="flex items-center space-x-1">
              <ZoomIn className="w-3 h-3" />
              <span>Scroll to zoom</span>
            </div>
          </div>
          <div className="text-right">
            <div>Zoom: {(zoom * 100).toFixed(0)}%</div>
          </div>
        </div>
        
        {/* Legend */}
        <div className="grid grid-cols-2 gap-4 text-xs">
          <div className="space-y-2">
            <h4 className="text-white font-medium">Elements</h4>
            <div className="space-y-1 text-gray-300">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 rounded-full bg-blue-500/60"></div>
                <span>Consciousness Sphere</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 rounded-full bg-purple-500/60"></div>
                <span>Prediction Points</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 rounded-full bg-orange-500/60"></div>
                <span>Insight Markers</span>
              </div>
            </div>
          </div>
          
          <div className="space-y-2">
            <h4 className="text-white font-medium">Interactions</h4>
            <div className="space-y-1 text-gray-300">
              <div>• Drag to rotate model</div>
              <div>• Scroll to zoom in/out</div>
              <div>• Colors show consciousness level</div>
              <div>• Size shows confidence/impact</div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default Consciousness3DModel;
