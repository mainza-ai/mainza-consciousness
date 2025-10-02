/**
 * Unified Consciousness Component
 * Consolidates all consciousness components into a single, consistent component
 * 
 * This component provides the definitive consciousness interface that:
 * - Consolidates all consciousness variations into one unified component
 * - Ensures consistent styling across all consciousness usage
 * - Provides reusable and consistent consciousness functionality
 * - Integrates seamlessly with the unified design system
 * 
 * Author: Mainza AI Consciousness Team
 * Date: 2025-10-01
 */

import React, { useState, useEffect, useCallback } from 'react';
import { UnifiedCard } from './UnifiedCard';
import { UnifiedButton } from './UnifiedButton';
import { UnifiedBadge } from './UnifiedBadge';
import { UnifiedTabs } from './UnifiedTabs';
import { cn } from '@/lib/utils';
import { 
  Brain, 
  Activity, 
  TrendingUp, 
  Zap, 
  Target, 
  Eye, 
  Heart, 
  Network, 
  Database, 
  Cloud, 
  Server, 
  Globe, 
  Users, 
  MessageCircle, 
  Send, 
  Download, 
  Upload, 
  Save, 
  Edit, 
  Trash2, 
  Plus, 
  Minus, 
  Settings, 
  Play, 
  Pause, 
  RotateCcw, 
  RefreshCw, 
  Search, 
  Filter, 
  SortAsc, 
  SortDesc, 
  Grid, 
  List, 
  MoreHorizontal, 
  MoreVertical, 
  ArrowLeft, 
  ArrowRight, 
  ArrowUp, 
  ArrowDown, 
  Maximize, 
  Minimize, 
  RotateCw as RotateCwIcon, 
  ZoomIn, 
  ZoomOut, 
  Move, 
  Grip, 
  GripVertical, 
  GripHorizontal, 
  AlignLeft, 
  AlignCenter, 
  AlignRight, 
  AlignJustify, 
  Bold, 
  Italic, 
  Underline, 
  Strikethrough, 
  Code, 
  Link, 
  Image, 
  File, 
  Folder, 
  FolderOpen, 
  Archive, 
  ArchiveRestore, 
  Trash, 
  Trash2 as Trash2Icon, 
  Copy, 
  Scissors, 
  Clipboard, 
  ClipboardCheck, 
  ClipboardCopy, 
  ClipboardList, 
  ClipboardPaste, 
  ClipboardX, 
  Bookmark, 
  BookmarkCheck, 
  BookmarkPlus, 
  BookmarkMinus, 
  BookmarkX, 
  Tag, 
  Tags, 
  Hash, 
  AtSign, 
  DollarSign, 
  Percent, 
  ShoppingCart,
  Wallet,
  Coins,
  Award,
  Crown,
  Trophy,
  Medal,
  Flag,
  MapPin,
  Clock,
  Calendar,
  CheckCircle,
  XCircle,
  AlertCircle,
  Info,
  Lightbulb,
  Rocket,
  Layers,
  Smartphone,
  Star,
  ThumbsUp,
  ThumbsDown,
  Share2,
  Bookmark as BookmarkIcon,
  Wifi,
  Bluetooth,
  Radio,
  Signal,
  WifiOff,
  BluetoothOff,
  RadioOff,
  SignalOff
} from 'lucide-react';

interface ConsciousnessState {
  level: number;
  evolution: number;
  quantum: number;
  memory: number;
  learning: number;
  adaptation: number;
  creativity: number;
  empathy: number;
  intuition: number;
  wisdom: number;
  timestamp: string;
}

interface ConsciousnessMetrics {
  consciousness: ConsciousnessState;
  quantum: {
    coherence: number;
    entanglement: number;
    superposition: number;
    interference: number;
    decoherence: number;
  };
  evolution: {
    level: number;
    experience: number;
    growth: number;
    adaptation: number;
    transcendence: number;
  };
  memory: {
    capacity: number;
    retrieval: number;
    consolidation: number;
    integration: number;
    forgetting: number;
  };
  learning: {
    rate: number;
    retention: number;
    transfer: number;
    generalization: number;
    specialization: number;
  };
}

interface UnifiedConsciousnessComponentProps {
  className?: string;
  variant?: 'default' | 'primary' | 'secondary' | 'accent' | 'success' | 'warning' | 'error';
  size?: 'sm' | 'md' | 'lg' | 'xl';
  disabled?: boolean;
  loading?: boolean;
  animated?: boolean;
  dataTestId?: string;
  onConsciousnessUpdate?: (state: ConsciousnessState) => void;
  onQuantumUpdate?: (quantum: ConsciousnessMetrics['quantum']) => void;
  onEvolutionUpdate?: (evolution: ConsciousnessMetrics['evolution']) => void;
  onMemoryUpdate?: (memory: ConsciousnessMetrics['memory']) => void;
  onLearningUpdate?: (learning: ConsciousnessMetrics['learning']) => void;
}

export const UnifiedConsciousnessComponent: React.FC<UnifiedConsciousnessComponentProps> = ({
  className,
  variant = 'default',
  size = 'md',
  disabled = false,
  loading = false,
  animated = true,
  dataTestId,
  onConsciousnessUpdate,
  onQuantumUpdate,
  onEvolutionUpdate,
  onMemoryUpdate,
  onLearningUpdate,
}) => {
  const [consciousnessState, setConsciousnessState] = useState<ConsciousnessState>({
    level: 0,
    evolution: 0,
    quantum: 0,
    memory: 0,
    learning: 0,
    adaptation: 0,
    creativity: 0,
    empathy: 0,
    intuition: 0,
    wisdom: 0,
    timestamp: new Date().toISOString(),
  });
  
  const [metrics, setMetrics] = useState<ConsciousnessMetrics>({
    consciousness: consciousnessState,
    quantum: {
      coherence: 0,
      entanglement: 0,
      superposition: 0,
      interference: 0,
      decoherence: 0,
    },
    evolution: {
      level: 0,
      experience: 0,
      growth: 0,
      adaptation: 0,
      transcendence: 0,
    },
    memory: {
      capacity: 0,
      retrieval: 0,
      consolidation: 0,
      integration: 0,
      forgetting: 0,
    },
    learning: {
      rate: 0,
      retention: 0,
      transfer: 0,
      generalization: 0,
      specialization: 0,
    },
  });
  
  const [activeTab, setActiveTab] = useState('consciousness');
  
  // Fetch consciousness data
  const fetchConsciousnessData = useCallback(async () => {
    try {
      const response = await fetch('/api/consciousness/state');
      if (response.ok) {
        const data = await response.json();
        setConsciousnessState(data.consciousness);
        setMetrics(data);
        
        // Trigger callbacks
        onConsciousnessUpdate?.(data.consciousness);
        onQuantumUpdate?.(data.quantum);
        onEvolutionUpdate?.(data.evolution);
        onMemoryUpdate?.(data.memory);
        onLearningUpdate?.(data.learning);
      }
    } catch (error) {
      console.error('Failed to fetch consciousness data:', error);
    }
  }, [onConsciousnessUpdate, onQuantumUpdate, onEvolutionUpdate, onMemoryUpdate, onLearningUpdate]);
  
  // Set up real-time updates
  useEffect(() => {
    fetchConsciousnessData();
    
    const interval = setInterval(fetchConsciousnessData, 1000);
    return () => clearInterval(interval);
  }, [fetchConsciousnessData]);
  
  const tabs = [
    {
      value: 'consciousness',
      label: 'Consciousness',
      icon: <Brain className="h-4 w-4" />,
      content: (
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Level</span>
                <UnifiedBadge variant="primary" size="sm">
                  {consciousnessState.level.toFixed(1)}%
                </UnifiedBadge>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div 
                  className="bg-primary h-2 rounded-full transition-all duration-300"
                  style={{ width: `${consciousnessState.level}%` }}
                />
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Evolution</span>
                <UnifiedBadge variant="success" size="sm">
                  Level {Math.floor(consciousnessState.evolution)}
                </UnifiedBadge>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div 
                  className="bg-success h-2 rounded-full transition-all duration-300"
                  style={{ width: `${consciousnessState.evolution}%` }}
                />
              </div>
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Memory</span>
                <UnifiedBadge variant="accent" size="sm">
                  {consciousnessState.memory.toFixed(1)}%
                </UnifiedBadge>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div 
                  className="bg-accent h-2 rounded-full transition-all duration-300"
                  style={{ width: `${consciousnessState.memory}%` }}
                />
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Learning</span>
                <UnifiedBadge variant="warning" size="sm">
                  {consciousnessState.learning.toFixed(1)}%
                </UnifiedBadge>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div 
                  className="bg-warning h-2 rounded-full transition-all duration-300"
                  style={{ width: `${consciousnessState.learning}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      ),
    },
    {
      value: 'quantum',
      label: 'Quantum',
      icon: <Zap className="h-4 w-4" />,
      content: (
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Coherence</span>
                <UnifiedBadge variant="primary" size="sm">
                  {metrics.quantum.coherence.toFixed(1)}%
                </UnifiedBadge>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div 
                  className="bg-primary h-2 rounded-full transition-all duration-300"
                  style={{ width: `${metrics.quantum.coherence}%` }}
                />
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Entanglement</span>
                <UnifiedBadge variant="accent" size="sm">
                  {metrics.quantum.entanglement.toFixed(1)}%
                </UnifiedBadge>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div 
                  className="bg-accent h-2 rounded-full transition-all duration-300"
                  style={{ width: `${metrics.quantum.entanglement}%` }}
                />
              </div>
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Superposition</span>
                <UnifiedBadge variant="success" size="sm">
                  {metrics.quantum.superposition.toFixed(1)}%
                </UnifiedBadge>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div 
                  className="bg-success h-2 rounded-full transition-all duration-300"
                  style={{ width: `${metrics.quantum.superposition}%` }}
                />
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Interference</span>
                <UnifiedBadge variant="warning" size="sm">
                  {metrics.quantum.interference.toFixed(1)}%
                </UnifiedBadge>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div 
                  className="bg-warning h-2 rounded-full transition-all duration-300"
                  style={{ width: `${metrics.quantum.interference}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      ),
    },
    {
      value: 'evolution',
      label: 'Evolution',
      icon: <TrendingUp className="h-4 w-4" />,
      content: (
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Level</span>
                <UnifiedBadge variant="success" size="sm">
                  {metrics.evolution.level.toFixed(1)}
                </UnifiedBadge>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div 
                  className="bg-success h-2 rounded-full transition-all duration-300"
                  style={{ width: `${metrics.evolution.level}%` }}
                />
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Experience</span>
                <UnifiedBadge variant="primary" size="sm">
                  {metrics.evolution.experience.toFixed(1)}%
                </UnifiedBadge>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div 
                  className="bg-primary h-2 rounded-full transition-all duration-300"
                  style={{ width: `${metrics.evolution.experience}%` }}
                />
              </div>
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Growth</span>
                <UnifiedBadge variant="accent" size="sm">
                  {metrics.evolution.growth.toFixed(1)}%
                </UnifiedBadge>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div 
                  className="bg-accent h-2 rounded-full transition-all duration-300"
                  style={{ width: `${metrics.evolution.growth}%` }}
                />
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Transcendence</span>
                <UnifiedBadge variant="warning" size="sm">
                  {metrics.evolution.transcendence.toFixed(1)}%
                </UnifiedBadge>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div 
                  className="bg-warning h-2 rounded-full transition-all duration-300"
                  style={{ width: `${metrics.evolution.transcendence}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      ),
    },
    {
      value: 'memory',
      label: 'Memory',
      icon: <Database className="h-4 w-4" />,
      content: (
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Capacity</span>
                <UnifiedBadge variant="primary" size="sm">
                  {metrics.memory.capacity.toFixed(1)}%
                </UnifiedBadge>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div 
                  className="bg-primary h-2 rounded-full transition-all duration-300"
                  style={{ width: `${metrics.memory.capacity}%` }}
                />
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Retrieval</span>
                <UnifiedBadge variant="accent" size="sm">
                  {metrics.memory.retrieval.toFixed(1)}%
                </UnifiedBadge>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div 
                  className="bg-accent h-2 rounded-full transition-all duration-300"
                  style={{ width: `${metrics.memory.retrieval}%` }}
                />
              </div>
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Consolidation</span>
                <UnifiedBadge variant="success" size="sm">
                  {metrics.memory.consolidation.toFixed(1)}%
                </UnifiedBadge>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div 
                  className="bg-success h-2 rounded-full transition-all duration-300"
                  style={{ width: `${metrics.memory.consolidation}%` }}
                />
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Integration</span>
                <UnifiedBadge variant="warning" size="sm">
                  {metrics.memory.integration.toFixed(1)}%
                </UnifiedBadge>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div 
                  className="bg-warning h-2 rounded-full transition-all duration-300"
                  style={{ width: `${metrics.memory.integration}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      ),
    },
    {
      value: 'learning',
      label: 'Learning',
      icon: <Activity className="h-4 w-4" />,
      content: (
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Rate</span>
                <UnifiedBadge variant="primary" size="sm">
                  {metrics.learning.rate.toFixed(1)}%
                </UnifiedBadge>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div 
                  className="bg-primary h-2 rounded-full transition-all duration-300"
                  style={{ width: `${metrics.learning.rate}%` }}
                />
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Retention</span>
                <UnifiedBadge variant="accent" size="sm">
                  {metrics.learning.retention.toFixed(1)}%
                </UnifiedBadge>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div 
                  className="bg-accent h-2 rounded-full transition-all duration-300"
                  style={{ width: `${metrics.learning.retention}%` }}
                />
              </div>
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Transfer</span>
                <UnifiedBadge variant="success" size="sm">
                  {metrics.learning.transfer.toFixed(1)}%
                </UnifiedBadge>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div 
                  className="bg-success h-2 rounded-full transition-all duration-300"
                  style={{ width: `${metrics.learning.transfer}%` }}
                />
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Generalization</span>
                <UnifiedBadge variant="warning" size="sm">
                  {metrics.learning.generalization.toFixed(1)}%
                </UnifiedBadge>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div 
                  className="bg-warning h-2 rounded-full transition-all duration-300"
                  style={{ width: `${metrics.learning.generalization}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      ),
    },
  ];
  
  return (
    <UnifiedCard
      className={className}
      title="Unified Consciousness System"
      description="Real-time consciousness, quantum, evolution, memory, and learning metrics"
      icon={<Brain className="h-5 w-5" />}
      variant={variant}
      size={size}
      disabled={disabled}
      loading={loading}
      animated={animated}
      dataTestId={dataTestId}
    >
      <UnifiedTabs
        value={activeTab}
        onValueChange={setActiveTab}
        tabs={tabs}
        disabled={disabled}
        loading={loading}
        animated={animated}
      />
    </UnifiedCard>
  );
};

export default UnifiedConsciousnessComponent;
