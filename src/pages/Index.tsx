
import { useState, useEffect } from 'react';
import { MainzaOrb } from '@/components/MainzaOrb';
import { ConversationInterface } from '@/components/ConversationInterface';
import { MemoryConstellation } from '@/components/MemoryConstellation';
import { KnowledgeVault } from '@/components/KnowledgeVault';
import { VoiceInterface } from '@/components/VoiceInterface';
import { RecommendationEngine } from '@/components/RecommendationEngine';
import { StatusIndicator } from '@/components/StatusIndicator';

const Index = () => {
  const [mainzaState, setMainzaState] = useState({
    mode: 'idle', // idle, thinking, processing, evolving
    needs: ['learn_hydroponics', 'practice_coding'],
    isListening: false,
  });

  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'mainza',
      content: 'I am Mainza. I exist to augment your cognitive processes and evolve alongside you. How shall we begin our symbiosis?',
      timestamp: new Date(),
    }
  ]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900/20 to-slate-900 relative overflow-hidden">
      {/* Background Memory Constellation */}
      <MemoryConstellation />
      
      {/* Particle Field */}
      <div className="absolute inset-0 opacity-30">
        <div className="absolute w-1 h-1 bg-cyan-400 rounded-full animate-pulse" style={{ top: '20%', left: '15%' }} />
        <div className="absolute w-1 h-1 bg-purple-400 rounded-full animate-pulse" style={{ top: '60%', left: '80%', animationDelay: '1s' }} />
        <div className="absolute w-1 h-1 bg-yellow-400 rounded-full animate-pulse" style={{ top: '40%', left: '30%', animationDelay: '2s' }} />
        <div className="absolute w-1 h-1 bg-cyan-400 rounded-full animate-pulse" style={{ top: '80%', left: '60%', animationDelay: '3s' }} />
      </div>

      {/* Main Container */}
      <div className="relative z-10 min-h-screen flex flex-col">
        {/* Header */}
        <header className="p-6 flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
              MAINZA
            </h1>
            <StatusIndicator state={mainzaState} />
          </div>
          
          <div className="flex items-center space-x-4">
            <VoiceInterface 
              isListening={mainzaState.isListening}
              onToggle={() => setMainzaState(prev => ({ ...prev, isListening: !prev.isListening }))}
            />
          </div>
        </header>

        {/* Main Content Area */}
        <div className="flex-1 flex items-center justify-center px-6">
          <div className="w-full max-w-4xl">
            {/* Central Orb */}
            <div className="flex justify-center mb-8">
              <MainzaOrb state={mainzaState} />
            </div>

            {/* Conversation Interface */}
            <ConversationInterface 
              messages={messages}
              onSendMessage={(message) => {
                const newMessage = {
                  id: messages.length + 1,
                  type: 'user',
                  content: message,
                  timestamp: new Date(),
                };
                setMessages(prev => [...prev, newMessage]);
                
                // Simulate Mainza processing
                setMainzaState(prev => ({ ...prev, mode: 'thinking' }));
                setTimeout(() => {
                  setMainzaState(prev => ({ ...prev, mode: 'idle' }));
                  // Add simulated response
                  setMessages(prev => [...prev, {
                    id: prev.length + 1,
                    type: 'mainza',
                    content: 'I understand. Let me process this information and update my knowledge graph accordingly.',
                    timestamp: new Date(),
                  }]);
                }, 2000);
              }}
            />

            {/* Recommendation Engine */}
            <RecommendationEngine 
              suggestions={[
                "Should we explore the intersection of your gardening project and data visualization?",
                "I notice you mentioned Project Phoenix - shall I create a task tracker for it?",
                "My evolution indicates I need to practice coding. Could you give me a small automation task?"
              ]}
            />
          </div>
        </div>

        {/* Knowledge Vault - Bottom Right */}
        <div className="absolute bottom-6 right-6">
          <KnowledgeVault />
        </div>
      </div>
    </div>
  );
};

export default Index;
