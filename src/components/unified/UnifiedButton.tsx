/**
 * Unified Button Component
 * Consolidates all button components into a single, consistent component
 * 
 * This component provides the definitive button interface that:
 * - Consolidates all button variations into one unified component
 * - Ensures consistent styling across all button usage
 * - Provides reusable and consistent button functionality
 * - Integrates seamlessly with the unified design system
 * 
 * Author: Mainza AI Consciousness Team
 * Date: 2025-10-01
 */

import React from 'react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { UnifiedButtonProps } from '@/lib/unified-design-system';
import { Loader2 } from 'lucide-react';

export const UnifiedButton: React.FC<UnifiedButtonProps> = ({
  className,
  children,
  variant = 'default',
  size = 'md',
  disabled = false,
  loading = false,
  animated = true,
  onClick,
  type = 'button',
  href,
  target,
  icon,
  iconPosition = 'left',
  fullWidth = false,
  dataTestId,
}) => {
  const baseClasses = cn(
    'relative transition-all duration-200',
    {
      'w-full': fullWidth,
      'hover:scale-105': animated && !disabled && !loading,
      'active:scale-95': !disabled && !loading,
    }
  );
  
  const variantClasses = {
    default: 'bg-primary text-primary-foreground hover:bg-primary/90',
    primary: 'bg-primary text-primary-foreground hover:bg-primary/90',
    secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
    accent: 'bg-accent text-accent-foreground hover:bg-accent/90',
    success: 'bg-success text-success-foreground hover:bg-success/90',
    warning: 'bg-warning text-warning-foreground hover:bg-warning/90',
    error: 'bg-error text-error-foreground hover:bg-error/90',
  };
  
  const sizeClasses = {
    sm: 'h-8 px-3 text-xs',
    md: 'h-10 px-4 text-sm',
    lg: 'h-12 px-6 text-base',
    xl: 'h-14 px-8 text-lg',
  };
  
  const iconSizeClasses = {
    sm: 'h-3 w-3',
    md: 'h-4 w-4',
    lg: 'h-5 w-5',
    xl: 'h-6 w-6',
  };
  
  const buttonContent = (
    <>
      {loading && (
        <Loader2 className={cn('animate-spin', iconSizeClasses[size])} />
      )}
      {!loading && icon && iconPosition === 'left' && (
        <span className="mr-2">{icon}</span>
      )}
      {!loading && children}
      {!loading && icon && iconPosition === 'right' && (
        <span className="ml-2">{icon}</span>
      )}
    </>
  );
  
  const buttonProps = {
    className: cn(baseClasses, variantClasses[variant], sizeClasses[size], className),
    disabled: disabled || loading,
    onClick,
    type,
    'data-testid': dataTestId,
  };
  
  if (href) {
    return (
      <a
        href={href}
        target={target}
        className={cn(
          'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
          baseClasses,
          variantClasses[variant],
          sizeClasses[size],
          className
        )}
        data-testid={dataTestId}
      >
        {buttonContent}
      </a>
    );
  }
  
  return (
    <Button {...buttonProps}>
      {buttonContent}
    </Button>
  );
};

export default UnifiedButton;
