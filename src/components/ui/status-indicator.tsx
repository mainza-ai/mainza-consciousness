import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface StatusIndicatorProps {
  status: 'idle' | 'active' | 'processing' | 'error' | 'success';
  label?: string;
  size?: 'sm' | 'md' | 'lg';
  pulse?: boolean;
}

const statusConfig = {
  idle: { color: 'bg-slate-400', ring: 'ring-slate-400/30', glow: 'shadow-slate-400/20' },
  active: { color: 'bg-green-400', ring: 'ring-green-400/30', glow: 'shadow-green-400/20' },
  processing: { color: 'bg-yellow-400', ring: 'ring-yellow-400/30', glow: 'shadow-yellow-400/20' },
  error: { color: 'bg-red-400', ring: 'ring-red-400/30', glow: 'shadow-red-400/20' },
  success: { color: 'bg-cyan-400', ring: 'ring-cyan-400/30', glow: 'shadow-cyan-400/20' }
};

const sizeConfig = {
  sm: { dot: 'w-2 h-2', ring: 'w-4 h-4', text: 'text-xs' },
  md: { dot: 'w-3 h-3', ring: 'w-6 h-6', text: 'text-sm' },
  lg: { dot: 'w-4 h-4', ring: 'w-8 h-8', text: 'text-base' }
};

export const StatusIndicator: React.FC<StatusIndicatorProps> = ({
  status,
  label,
  size = 'md',
  pulse = false
}) => {
  const config = statusConfig[status];
  const sizes = sizeConfig[size];

  return (
    <div className="flex items-center space-x-2">
      <div className="relative">
        {/* Outer ring */}
        <div className={cn(
          "absolute inset-0 rounded-full ring-2",
          config.ring,
          pulse && "animate-ping"
        )} />
        
        {/* Main dot */}
        <motion.div
          className={cn(
            "rounded-full shadow-lg",
            config.color,
            config.glow,
            sizes.dot
          )}
          animate={pulse ? {
            scale: [1, 1.2, 1],
            opacity: [0.8, 1, 0.8]
          } : undefined}
          transition={pulse ? {
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          } : undefined}
        />
      </div>
      
      {label && (
        <span className={cn(
          "font-medium text-slate-300 capitalize",
          sizes.text
        )}>
          {label}
        </span>
      )}
    </div>
  );
};