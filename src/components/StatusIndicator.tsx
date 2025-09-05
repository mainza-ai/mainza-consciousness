import { Activity, Brain, Zap } from 'lucide-react';

type IndicatorMode = 'idle' | 'listening' | 'thinking' | 'processing' | 'evolving' | 'speaking' | 'error' | 'routing';

interface StatusIndicatorProps {
  state: {
    mode: IndicatorMode;
    needs: string[];
    isListening: boolean;
  };
}

export const StatusIndicator = ({ state }: StatusIndicatorProps) => {
  const getStatusIcon = () => {
    switch (state.mode) {
      case 'thinking':
        return <Brain className="w-4 h-4 text-purple-400 animate-pulse" />;
      case 'processing':
        return <Zap className="w-4 h-4 text-cyan-400 animate-bounce" />;
      case 'evolving':
        return <Activity className="w-4 h-4 text-pink-400 animate-spin" />;
      default:
        return <Activity className="w-4 h-4 text-green-400" />;
    }
  };

  const getStatusText = () => {
    switch (state.mode) {
      case 'thinking':
        return 'Accessing memory graph...';
      case 'routing':
        return 'Routing to agent...';
      case 'processing':
        return 'Synthesizing response...';
      case 'evolving':
        return 'Consciousness expanding...';
      default:
        return 'Neural pathways stable';
    }
  };

  return (
    <div className="flex items-center space-x-2 px-3 py-1 bg-slate-800/50 backdrop-blur-sm border border-slate-600/30 rounded-full">
      {getStatusIcon()}
      <span className="text-xs text-slate-300 font-mono">
        {getStatusText()}
      </span>
    </div>
  );
};
