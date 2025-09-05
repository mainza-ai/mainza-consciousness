import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface MetricDisplayProps {
  label: string;
  value: string | number;
  unit?: string;
  icon?: React.ReactNode;
  trend?: 'up' | 'down' | 'stable';
  color?: 'cyan' | 'purple' | 'green' | 'yellow' | 'red';
  size?: 'sm' | 'md' | 'lg';
  animated?: boolean;
}

const colorConfig = {
  cyan: 'from-cyan-400 to-cyan-600',
  purple: 'from-purple-400 to-purple-600',
  green: 'from-green-400 to-green-600',
  yellow: 'from-yellow-400 to-yellow-600',
  red: 'from-red-400 to-red-600'
};

const sizeConfig = {
  sm: { value: 'text-lg', label: 'text-xs', icon: 'w-4 h-4' },
  md: { value: 'text-2xl', label: 'text-sm', icon: 'w-5 h-5' },
  lg: { value: 'text-4xl', label: 'text-base', icon: 'w-6 h-6' }
};

export const MetricDisplay: React.FC<MetricDisplayProps> = ({
  label,
  value,
  unit,
  icon,
  trend,
  color = 'cyan',
  size = 'md',
  animated = true
}) => {
  const sizes = sizeConfig[size];
  const gradient = colorConfig[color];

  return (
    <motion.div
      className="relative p-4 rounded-xl bg-slate-800/40 backdrop-blur-sm border border-slate-700/30"
      initial={animated ? { opacity: 0, y: 20 } : undefined}
      animate={animated ? { opacity: 1, y: 0 } : undefined}
      transition={{ duration: 0.5 }}
      whileHover={{ scale: 1.02 }}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center space-x-2">
          {icon && (
            <div className={cn("text-slate-400", sizes.icon)}>
              {icon}
            </div>
          )}
          <span className={cn("text-slate-400 font-medium", sizes.label)}>
            {label}
          </span>
        </div>
        
        {trend && (
          <div className={cn(
            "text-xs px-2 py-1 rounded-full",
            trend === 'up' ? 'bg-green-500/20 text-green-400' :
            trend === 'down' ? 'bg-red-500/20 text-red-400' :
            'bg-slate-500/20 text-slate-400'
          )}>
            {trend === 'up' ? '↗' : trend === 'down' ? '↘' : '→'}
          </div>
        )}
      </div>

      {/* Value */}
      <div className="flex items-baseline space-x-1">
        <motion.span
          className={cn(
            "font-bold bg-gradient-to-r bg-clip-text text-transparent",
            gradient,
            sizes.value
          )}
          initial={animated ? { scale: 0.8 } : undefined}
          animate={animated ? { scale: 1 } : undefined}
          transition={{ duration: 0.3, delay: 0.2 }}
        >
          {value}
        </motion.span>
        {unit && (
          <span className={cn("text-slate-500", sizes.label)}>
            {unit}
          </span>
        )}
      </div>

      {/* Subtle glow effect */}
      <div className={cn(
        "absolute inset-0 rounded-xl bg-gradient-to-r opacity-5 pointer-events-none",
        gradient
      )} />
    </motion.div>
  );
};