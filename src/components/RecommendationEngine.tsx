import { Sparkles } from 'lucide-react';
import { HolographicPane } from './ui/holographic-pane';

interface RecommendationEngineProps {
  suggestions: string[];
}

export const RecommendationEngine = ({ suggestions }: RecommendationEngineProps) => {
  return (
    <HolographicPane title="Synaptic Suggestions" className="w-full">
      <div className="flex items-center space-x-2 mb-3">
        <Sparkles className="w-4 h-4 text-yellow-400" />
        <span className="text-xs text-white font-mono uppercase tracking-wider">
          Synaptic Suggestions
        </span>
      </div>
      <div className="space-y-2">
        {suggestions.map((suggestion, index) => (
          <div key={index} className="px-4 py-2 rounded-lg bg-slate-800/40 text-slate-200 shadow-sm">
            {suggestion}
          </div>
        ))}
      </div>
    </HolographicPane>
  );
};
