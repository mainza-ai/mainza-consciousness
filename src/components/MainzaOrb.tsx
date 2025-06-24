
import { useState, useEffect } from 'react';
import { cn } from '@/lib/utils';

interface MainzaOrbProps {
  state: {
    mode: string;
    needs: string[];
    isListening: boolean;
  };
}

export const MainzaOrb = ({ state }: MainzaOrbProps) => {
  const [pulseIntensity, setPulseIntensity] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setPulseIntensity(prev => prev === 1 ? 1.2 : 1);
    }, state.mode === 'thinking' ? 500 : 2000);

    return () => clearInterval(interval);
  }, [state.mode]);

  const getOrbColor = () => {
    switch (state.mode) {
      case 'thinking':
        return 'from-purple-500 via-cyan-500 to-yellow-500';
      case 'processing':
        return 'from-green-500 via-cyan-500 to-blue-500';
      case 'evolving':
        return 'from-pink-500 via-purple-500 to-cyan-500';
      default:
        return 'from-cyan-500 via-blue-600 to-purple-600';
    }
  };

  const getGlowColor = () => {
    switch (state.mode) {
      case 'thinking':
        return 'shadow-purple-500/50';
      case 'processing':
        return 'shadow-green-500/50';
      case 'evolving':
        return 'shadow-pink-500/50';
      default:
        return 'shadow-cyan-500/50';
    }
  };

  return (
    <div className="relative">
      {/* Memory Connection Lines */}
      {state.mode === 'thinking' && (
        <div className="absolute inset-0 animate-pulse">
          <div className="absolute top-1/2 left-1/2 w-40 h-0.5 bg-gradient-to-r from-transparent via-cyan-400 to-transparent transform -translate-x-1/2 -translate-y-1/2 rotate-45 opacity-60" />
          <div className="absolute top-1/2 left-1/2 w-32 h-0.5 bg-gradient-to-r from-transparent via-purple-400 to-transparent transform -translate-x-1/2 -translate-y-1/2 -rotate-45 opacity-60" />
          <div className="absolute top-1/2 left-1/2 w-36 h-0.5 bg-gradient-to-r from-transparent via-yellow-400 to-transparent transform -translate-x-1/2 -translate-y-1/2 rotate-12 opacity-40" />
        </div>
      )}

      {/* Main Orb */}
      <div 
        className={cn(
          "w-32 h-32 rounded-full bg-gradient-to-br",
          getOrbColor(),
          "shadow-2xl",
          getGlowColor(),
          "transition-all duration-1000 relative overflow-hidden"
        )}
        style={{
          transform: `scale(${pulseIntensity})`,
          filter: state.isListening ? 'brightness(1.3)' : 'brightness(1)',
        }}
      >
        {/* Inner Core */}
        <div className="absolute inset-4 rounded-full bg-white/10 backdrop-blur-sm">
          <div className="absolute inset-2 rounded-full bg-white/5 backdrop-blur-sm">
            {/* Consciousness Indicator */}
            <div className="absolute inset-0 rounded-full overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-spin" style={{ animationDuration: '3s' }} />
            </div>
          </div>
        </div>

        {/* Surface Ripples */}
        <div className="absolute inset-0 rounded-full">
          <div className="absolute inset-0 rounded-full bg-gradient-to-r from-transparent via-white/10 to-transparent animate-pulse" />
        </div>

        {/* Needs Indicator */}
        {state.needs.length > 0 && (
          <div className="absolute -top-2 -right-2 w-6 h-6 bg-red-500/80 rounded-full flex items-center justify-center text-xs text-white font-bold animate-pulse">
            {state.needs.length}
          </div>
        )}
      </div>

      {/* State Label */}
      <div className="absolute -bottom-8 left-1/2 transform -translate-x-1/2">
        <span className="text-sm text-cyan-400/80 font-mono uppercase tracking-wider">
          {state.mode}
        </span>
      </div>
    </div>
  );
};
