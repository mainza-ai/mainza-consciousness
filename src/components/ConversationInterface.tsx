
import { useState } from 'react';
import { Send, Mic, Upload } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

interface Message {
  id: number;
  type: 'user' | 'mainza';
  content: string;
  timestamp: Date;
}

interface ConversationInterfaceProps {
  messages: Message[];
  onSendMessage: (message: string) => void;
}

export const ConversationInterface = ({ messages, onSendMessage }: ConversationInterfaceProps) => {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim()) {
      onSendMessage(input);
      setInput('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* Messages Container */}
      <div className="h-96 overflow-y-auto mb-6 space-y-4 px-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={cn(
              "flex",
              message.type === 'user' ? 'justify-end' : 'justify-start'
            )}
          >
            <div
              className={cn(
                "max-w-[80%] rounded-2xl px-6 py-4 backdrop-blur-md border",
                message.type === 'user'
                  ? 'bg-cyan-500/20 border-cyan-400/30 text-cyan-100'
                  : 'bg-purple-500/20 border-purple-400/30 text-purple-100'
              )}
            >
              <p className="text-sm leading-relaxed">{message.content}</p>
              <div
                className={cn(
                  "text-xs mt-2 opacity-60",
                  message.type === 'user' ? 'text-cyan-300' : 'text-purple-300'
                )}
              >
                {message.timestamp.toLocaleTimeString()}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Input Interface */}
      <div className="relative">
        <div className="flex items-end space-x-2">
          <div className="flex-1 relative">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Share your thoughts with Mainza..."
              className="w-full px-6 py-4 bg-slate-800/50 backdrop-blur-md border border-cyan-400/30 rounded-2xl text-cyan-100 placeholder-cyan-400/50 resize-none focus:outline-none focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/20 transition-all"
              rows={3}
            />
            
            {/* Holographic Input Glow */}
            <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-cyan-500/10 via-transparent to-purple-500/10 pointer-events-none" />
          </div>
          
          <div className="flex flex-col space-y-2">
            <Button
              onClick={handleSend}
              disabled={!input.trim()}
              className="w-12 h-12 rounded-full bg-gradient-to-r from-cyan-500 to-purple-500 hover:from-cyan-400 hover:to-purple-400 border-0 shadow-lg shadow-cyan-500/25"
            >
              <Send className="w-5 h-5" />
            </Button>
            
            <Button
              variant="outline"
              className="w-12 h-12 rounded-full border-cyan-400/30 bg-slate-800/50 backdrop-blur-md hover:bg-cyan-500/20 hover:border-cyan-400"
            >
              <Mic className="w-5 h-5 text-cyan-400" />
            </Button>
            
            <Button
              variant="outline"
              className="w-12 h-12 rounded-full border-purple-400/30 bg-slate-800/50 backdrop-blur-md hover:bg-purple-500/20 hover:border-purple-400"
            >
              <Upload className="w-5 h-5 text-purple-400" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};
