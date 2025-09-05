import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
  glow?: boolean;
  gradient?: boolean;
}

export const GlassCard: React.FC<GlassCardProps> = ({
  children,
  className,
  hover = true,
  glow = false,
  gradient = false
}) => {
  return (
    <motion.div
      className={cn(
        "relative backdrop-blur-md border border-white/10 rounded-2xl overflow-hidden",
        gradient 
          ? "bg-gradient-to-br from-slate-900/60 via-slate-800/40 to-slate-900/60" 
          : "bg-slate-900/40",
        glow && "shadow-2xl shadow-cyan-500/10",
        className
      )}
      whileHover={hover ? { 
        scale: 1.02,
        boxShadow: glow 
          ? "0 25px 50px -12px rgba(34, 211, 238, 0.25)" 
          : "0 25px 50px -12px rgba(0, 0, 0, 0.25)"
      } : undefined}
      transition={{ type: "spring", stiffness: 300, damping: 30 }}
    >
      {/* Glass reflection effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/5 via-transparent to-transparent pointer-events-none" />
      
      {/* Content */}
      <div className="relative z-10">
        {children}
      </div>
      
      {/* Subtle border glow */}
      {glow && (
        <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-cyan-400/20 via-purple-400/20 to-pink-400/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
      )}
    </motion.div>
  );
};