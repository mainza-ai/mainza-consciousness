/**
 * Unified Badge Component
 * Consolidates all badge components into a single, consistent component
 * 
 * This component provides the definitive badge interface that:
 * - Consolidates all badge variations into one unified component
 * - Ensures consistent styling across all badge usage
 * - Provides reusable and consistent badge functionality
 * - Integrates seamlessly with the unified design system
 * 
 * Author: Mainza AI Consciousness Team
 * Date: 2025-10-01
 */

import React from 'react';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import { UnifiedBadgeProps } from '@/lib/unified-design-system';
import { X } from 'lucide-react';

export const UnifiedBadge: React.FC<UnifiedBadgeProps> = ({
  className,
  children,
  variant = 'default',
  size = 'md',
  removable = false,
  onRemove,
  disabled = false,
  loading = false,
  animated = true,
  dataTestId,
}) => {
  const baseClasses = cn(
    'inline-flex items-center gap-1 transition-all duration-200',
    {
      'opacity-50 pointer-events-none': disabled,
      'animate-pulse': loading,
      'hover:scale-105': animated && !disabled && !loading,
    }
  );
  
  const variantClasses = {
    default: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
    primary: 'bg-primary text-primary-foreground hover:bg-primary/90',
    secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
    accent: 'bg-accent text-accent-foreground hover:bg-accent/90',
    success: 'bg-success text-success-foreground hover:bg-success/90',
    warning: 'bg-warning text-warning-foreground hover:bg-warning/90',
    error: 'bg-error text-error-foreground hover:bg-error/90',
    outline: 'border border-border bg-transparent hover:bg-accent hover:text-accent-foreground',
  };
  
  const sizeClasses = {
    sm: 'px-2 py-1 text-xs',
    md: 'px-2.5 py-1.5 text-sm',
    lg: 'px-3 py-2 text-base',
  };
  
  const handleRemove = (e: React.MouseEvent) => {
    e.stopPropagation();
    onRemove?.();
  };
  
  return (
    <Badge
      className={cn(
        baseClasses,
        variantClasses[variant],
        sizeClasses[size],
        className
      )}
      data-testid={dataTestId}
    >
      {children}
      {removable && (
        <button
          type="button"
          onClick={handleRemove}
          className="ml-1 hover:bg-black/10 rounded-full p-0.5 transition-colors"
          disabled={disabled || loading}
        >
          <X className="h-3 w-3" />
        </button>
      )}
    </Badge>
  );
};

export default UnifiedBadge;
