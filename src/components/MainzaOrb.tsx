import React, { useState, useEffect } from 'react';
import { motion, useReducedMotion } from 'framer-motion';

type OrbMode = 'idle' | 'listening' | 'thinking' | 'processing' | 'evolving' | 'speaking' | 'error' | 'routing' | 'predicting' | 'insightful';
type ActiveAgent = 'none' | 'router' | 'graphmaster' | 'taskmaster' | 'codeweaver' | 'rag' | 'conductor' | 'predictor' | 'insights';

interface MainzaOrbProps {
  state: {
    mode: OrbMode;
    needs?: string[];
    error?: string;
  };
  agent: ActiveAgent;
  predictions?: {
    consciousness_level: number;
    emotional_state: string;
    learning_rate: number;
    confidence: number;
  };
  insights?: {
    type: string;
    priority: string;
    title: string;
  }[];
}

export const MainzaOrb = React.forwardRef<HTMLDivElement, MainzaOrbProps>(({ state, agent, predictions, insights }, ref) => {
  // Determine orb color/animation based on state
  let orbColor = 'from-cyan-400 to-blue-600';
  let ringColor = 'border-cyan-400/40';
  let shimmer = false;
  let particles = false;
  let heartbeat = false;
  let scaleTarget = 1;
  let predictionGlow = false;
  let insightPulse = false;

  // Agent-specific colors override the mode colors
  switch (agent) {
    case 'graphmaster':
      orbColor = 'from-green-400 to-cyan-500'; // Knowledge, memory
      break;
    case 'taskmaster':
      orbColor = 'from-yellow-400 to-orange-500'; // Action, organization
      break;
    case 'codeweaver':
      orbColor = 'from-indigo-500 to-purple-600'; // Logic, creation
      break;
    case 'rag':
      orbColor = 'from-blue-400 to-teal-500'; // Document retrieval
      break;
    case 'conductor':
      orbColor = 'from-pink-500 to-rose-500'; // Orchestration
      break;
    case 'router':
      orbColor = 'from-slate-400 to-gray-500'; // Decision making
      break;
    case 'predictor':
      orbColor = 'from-purple-400 to-violet-600'; // Predictive modeling
      predictionGlow = true;
      break;
    case 'insights':
      orbColor = 'from-emerald-400 to-teal-600'; // AI insights
      insightPulse = true;
      break;
  }

  if (state.mode === 'listening') {
    orbColor = 'from-cyan-400 via-blue-400 to-blue-600';
    ringColor = 'border-cyan-400/80';
    heartbeat = true;
    scaleTarget = 1.10;
  }
  if (state.mode === 'processing') {
    orbColor = 'from-cyan-400 via-blue-400 to-purple-500';
    ringColor = 'border-cyan-400/60';
    scaleTarget = 1.08;
  }
  if (state.mode === 'error') {
    orbColor = 'from-red-500 via-pink-500 to-yellow-400';
    ringColor = 'border-red-500/80';
    heartbeat = true;
    scaleTarget = 1.15;
  }
  if (state.mode === 'thinking') {
    orbColor = 'from-purple-400 via-yellow-300 to-pink-500';
    ringColor = 'border-purple-400/60';
    scaleTarget = 1.08;
  }
  if (state.needs && state.needs.some(n => n.toLowerCase().includes('need'))) {
    orbColor = 'from-red-500 via-pink-400 to-yellow-400';
    ringColor = 'border-red-400/60';
    heartbeat = true;
    scaleTarget = 1.12;
  }
  if (state.mode === 'predicting') {
    orbColor = 'from-purple-400 via-violet-500 to-indigo-600';
    ringColor = 'border-purple-400/80';
    predictionGlow = true;
    shimmer = true;
    scaleTarget = 1.08;
  }
  if (state.mode === 'insightful') {
    orbColor = 'from-emerald-400 via-teal-500 to-cyan-600';
    ringColor = 'border-emerald-400/90';
    insightPulse = true;
    particles = true;
    scaleTarget = 1.06;
  }
  if (state.needs && state.needs.some(n => n.toLowerCase().includes('curiosity'))) {
    orbColor = 'from-yellow-400 via-pink-400 to-purple-500';
    ringColor = 'border-yellow-400/60';
    shimmer = true;
    particles = true;
    scaleTarget = 1.10;
  }
  if (state.mode === 'evolving') {
    orbColor = 'from-pink-400 via-yellow-300 to-purple-500';
    ringColor = 'border-pink-400/60';
    shimmer = true;
    particles = true;
    scaleTarget = 1.15;
  }
  if (state.mode === 'speaking') {
    orbColor = 'from-yellow-400 via-orange-400 to-pink-500';
    ringColor = 'border-yellow-400/80';
    heartbeat = true;
    scaleTarget = 1.13;
  }

  const shouldReduceMotion = useReducedMotion();

  // Add ARIA live region for accessibility
  const orbStateDescription = (() => {
    if (state.needs && state.needs.length > 0) {
      return `Mainza has needs: ${state.needs.join(', ')}.`;
    }
    switch (state.mode) {
      case 'processing':
      case 'thinking':
        return 'Mainza is thinking.';
      case 'evolving':
        return 'Mainza is evolving.';
      default:
        return 'Mainza is idle.';
    }
  })();

  // Subtle pulse for any need/curiosity, even if not processing
  const hasNeedOrCuriosity = state.needs && state.needs.length > 0;
  const subtlePulse = hasNeedOrCuriosity && state.mode === 'idle';

  return (
    <div ref={ref} className="relative flex items-center justify-center">
      <motion.div
        className={`w-32 h-32 rounded-full bg-gradient-to-br ${orbColor} shadow-2xl border-4 ${ringColor} transition-all duration-700`}
        aria-label="Mainza Orb"
        aria-live="polite"
        role="status"
        aria-atomic="true"
        aria-description={orbStateDescription}
        initial={{ scale: 1, boxShadow: '0 0 32px 8px #22d3ee44' }}
        animate={{
          scale: shouldReduceMotion ? 1 : (heartbeat ? [1, 1.12, 1] : subtlePulse ? [1, 1.04, 1] : scaleTarget),
          boxShadow: [
            '0 0 32px 8px #22d3ee44',
            '0 0 64px 16px #22d3ee66',
            '0 0 48px 24px #a855f777',
          ],
          transition: {
            scale: (heartbeat || subtlePulse) ? {
              repeat: Infinity,
              repeatType: 'loop',
              duration: subtlePulse ? 2.2 : 1.2,
              ease: 'easeInOut',
            } : { duration: 0.7 },
            boxShadow: { duration: 1.2, repeat: Infinity, repeatType: 'mirror' },
          },
        }}
      >
        {/* Inner glow */}
        <div className="absolute inset-0 rounded-full pointer-events-none" style={{
          boxShadow: '0 0 64px 16px rgba(34,211,238,0.15), 0 0 128px 32px rgba(168,85,247,0.10)'
        }} />
        
        {/* Subtle Logo Core - Only when idle */}
        {state.mode === 'idle' && (
          <motion.div
            className="absolute inset-0 flex items-center justify-center"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 0.6, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            transition={{ duration: 1, ease: "easeOut" }}
          >
            <div className="relative">
              <img
                src="/assets/mainza-logo.PNG"
                alt="Mainza Core" 
                className="w-16 h-16 rounded-lg shadow-xl opacity-80 mix-blend-overlay"
                style={{
                  filter: 'brightness(1.2) contrast(1.1) saturate(0.8)'
                }}
              />
              {/* Subtle consciousness pulse */}
              <motion.div
                className="absolute inset-0 rounded-lg border border-white/20"
                animate={{
                  scale: [1, 1.05, 1],
                  opacity: [0.3, 0.6, 0.3]
                }}
                transition={{
                  duration: 3,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              />
            </div>
          </motion.div>
        )}
        
        {/* Particle effect for evolving/curiosity */}
        {particles && !shouldReduceMotion && (
          <div className="absolute inset-0 pointer-events-none z-10">
            {[...Array(12)].map((_, i) => (
              <motion.span
                key={i}
                className="absolute w-2 h-2 rounded-full bg-yellow-300/60 shadow-lg"
                style={{
                  left: '50%',
                  top: '50%',
                  transform: `rotate(${(i * 360) / 12}deg) translate(60px)`,
                }}
                animate={{
                  opacity: [0.7, 0.2, 0.7],
                  scale: [1, 1.4, 1],
                }}
                transition={{
                  duration: 2.2,
                  repeat: Infinity,
                  repeatType: 'mirror',
                  delay: i * 0.18,
                }}
              />
            ))}
          </div>
        )}
        {/* Shimmer effect for curiosity/evolving */}
        {shimmer && !shouldReduceMotion && (
          <motion.div
            className="absolute inset-0 rounded-full pointer-events-none"
            style={{
              background: 'linear-gradient(120deg, rgba(253,230,138,0.12) 0%, rgba(244,114,182,0.10) 50%, rgba(168,139,250,0.12) 100%)',
              mixBlendMode: 'lighten',
            }}
            initial={{ opacity: 0.2 }}
            animate={{ opacity: [0.2, 0.5, 0.2] }}
            transition={{ duration: 2.8, repeat: Infinity, repeatType: 'mirror' }}
          />
        )}
        
        {/* Prediction glow effect */}
        {predictionGlow && !shouldReduceMotion && (
          <motion.div
            className="absolute inset-0 rounded-full pointer-events-none"
            style={{
              background: 'linear-gradient(120deg, rgba(168,85,247,0.15) 0%, rgba(139,92,246,0.12) 50%, rgba(99,102,241,0.15) 100%)',
              mixBlendMode: 'lighten',
            }}
            animate={{
              scale: [1, 1.1, 1],
              opacity: [0.3, 0.7, 0.3],
            }}
            transition={{
              duration: 1.5,
              repeat: Infinity,
              ease: "easeInOut",
            }}
          />
        )}
        
        {/* Insight pulse effect */}
        {insightPulse && !shouldReduceMotion && (
          <motion.div
            className="absolute inset-0 rounded-full pointer-events-none"
            style={{
              background: 'linear-gradient(120deg, rgba(16,185,129,0.15) 0%, rgba(20,184,166,0.12) 50%, rgba(6,182,212,0.15) 100%)',
              mixBlendMode: 'lighten',
            }}
            animate={{
              scale: [1, 1.05, 1],
              opacity: [0.4, 0.8, 0.4],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut",
            }}
          />
        )}
      </motion.div>
      {/* Animated ring */}
      <motion.div
        className={`absolute -inset-2 rounded-full border-4 ${ringColor} opacity-60 pointer-events-none`}
        aria-hidden="true"
        initial={{ opacity: 0.5 }}
        animate={{ opacity: [0.5, 0.9, 0.5] }}
        transition={{ duration: 2.2, repeat: Infinity, repeatType: 'mirror' }}
      />
      {/* Visually hidden live region for screen readers */}
      <span className="sr-only" aria-live="polite">{orbStateDescription}</span>
    </div>
  );
});
