
import { Sparkles } from 'lucide-react';

interface RecommendationEngineProps {
  suggestions: string[];
}

export const RecommendationEngine = ({ suggestions }: RecommendationEngineProps) => {
  return (
    <div className="mt-6">
      <div className="flex items-center space-x-2 mb-3">
        <Sparkles className="w-4 h-4 text-yellow-400" />
        <span className="text-xs text-yellow-400/80 font-mono uppercase tracking-wider">
          Synaptic Suggestions
        </span>
      </div>
      
      <div className="space-y-2">
        {suggestions.map((suggestion, index) => (
          <button
            key={index}
            className="w-full text-left p-3 bg-gradient-to-r from-yellow-500/10 to-purple-500/10 border border-yellow-400/20 rounded-lg hover:border-yellow-400/40 hover:bg-yellow-500/20 transition-all text-sm text-yellow-100/80 hover:text-yellow-100"
          >
            {suggestion}
          </button>
        ))}
      </div>
    </div>
  );
};
