import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface DarkButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

export const DarkButton: React.FC<DarkButtonProps> = ({
  variant = 'outline',
  size = 'md',
  className,
  children,
  ...props
}) => {
  const baseClasses = "inline-flex items-center justify-center gap-2 font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-cyan-400/50 disabled:opacity-50 disabled:cursor-not-allowed";
  
  const variantClasses = {
    default: "bg-cyan-500 hover:bg-cyan-400 text-white border border-cyan-500 hover:border-cyan-400",
    outline: "bg-slate-800/60 hover:bg-slate-700/80 text-slate-200 border border-slate-600/50 hover:border-slate-500/50",
    ghost: "bg-transparent hover:bg-slate-800/40 text-slate-200 border border-transparent"
  };
  
  const sizeClasses = {
    sm: "h-8 px-3 text-sm rounded-lg",
    md: "h-10 px-4 text-sm rounded-lg",
    lg: "h-12 px-6 text-base rounded-xl"
  };

  return (
    <motion.button
      className={cn(
        baseClasses,
        variantClasses[variant],
        sizeClasses[size],
        className
      )}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      transition={{ type: "spring", stiffness: 400, damping: 17 }}
      {...props}
    >
      {children}
    </motion.button>
  );
};