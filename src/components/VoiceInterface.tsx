
import { Mic, MicOff } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface VoiceInterfaceProps {
  isListening: boolean;
  onToggle: () => void;
}

export const VoiceInterface = ({ isListening, onToggle }: VoiceInterfaceProps) => {
  return (
    <div className="flex items-center space-x-2">
      <Button
        onClick={onToggle}
        variant="outline"
        className={`border-2 transition-all ${
          isListening
            ? 'border-red-400 bg-red-500/20 text-red-400 shadow-lg shadow-red-400/25'
            : 'border-cyan-400/30 bg-slate-800/50 text-cyan-400 hover:bg-cyan-500/20'
        }`}
      >
        {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
      </Button>
      
      {isListening && (
        <div className="flex items-center space-x-1">
          <div className="w-1 h-4 bg-red-400 rounded-full animate-pulse" />
          <div className="w-1 h-6 bg-red-400 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }} />
          <div className="w-1 h-3 bg-red-400 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }} />
          <span className="text-xs text-red-400 ml-2">LISTENING</span>
        </div>
      )}
    </div>
  );
};
