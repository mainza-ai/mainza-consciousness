/**
 * Unified Card Component
 * Consolidates all card components into a single, consistent component
 * 
 * This component provides the definitive card interface that:
 * - Consolidates all card variations into one unified component
 * - Ensures consistent styling across all card usage
 * - Provides reusable and consistent card functionality
 * - Integrates seamlessly with the unified design system
 * 
 * Author: Mainza AI Consciousness Team
 * Date: 2025-10-01
 */

import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { ChevronDown, ChevronUp, MoreHorizontal } from 'lucide-react';
import { cn } from '@/lib/utils';
import { UnifiedCardProps } from '@/lib/unified-design-system';

export const UnifiedCard: React.FC<UnifiedCardProps> = ({
  className,
  children,
  title,
  description,
  icon,
  actions,
  collapsible = false,
  defaultCollapsed = false,
  variant = 'default',
  size = 'md',
  disabled = false,
  loading = false,
  animated = true,
  dataTestId,
}) => {
  const [isCollapsed, setIsCollapsed] = useState(defaultCollapsed);
  
  const baseClasses = cn(
    'relative overflow-hidden transition-all duration-300',
    {
      'opacity-50 pointer-events-none': disabled,
      'animate-pulse': loading,
      'hover:shadow-lg': animated && !disabled,
      'hover:scale-[1.02]': animated && !disabled,
    },
    className
  );
  
  const variantClasses = {
    default: 'bg-card border border-border',
    primary: 'bg-primary/5 border-primary/20',
    secondary: 'bg-secondary/5 border-secondary/20',
    accent: 'bg-accent/5 border-accent/20',
    success: 'bg-success/5 border-success/20',
    warning: 'bg-warning/5 border-warning/20',
    error: 'bg-error/5 border-error/20',
  };
  
  const sizeClasses = {
    sm: 'p-3',
    md: 'p-4',
    lg: 'p-6',
    xl: 'p-8',
  };
  
  const handleToggleCollapse = () => {
    if (collapsible) {
      setIsCollapsed(!isCollapsed);
    }
  };
  
  return (
    <Card
      className={cn(
        baseClasses,
        variantClasses[variant],
        sizeClasses[size]
      )}
      data-testid={dataTestId}
    >
      {(title || icon || actions || collapsible) && (
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              {icon && (
                <div className="flex-shrink-0">
                  {icon}
                </div>
              )}
              {title && (
                <CardTitle className="text-lg font-semibold">
                  {title}
                </CardTitle>
              )}
            </div>
            <div className="flex items-center gap-2">
              {actions && (
                <div className="flex items-center gap-1">
                  {actions}
                </div>
              )}
              {collapsible && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleToggleCollapse}
                  className="h-8 w-8 p-0"
                >
                  {isCollapsed ? (
                    <ChevronDown className="h-4 w-4" />
                  ) : (
                    <ChevronUp className="h-4 w-4" />
                  )}
                </Button>
              )}
            </div>
          </div>
          {description && (
            <p className="text-sm text-muted-foreground mt-2">
              {description}
            </p>
          )}
        </CardHeader>
      )}
      
      {!isCollapsed && (
        <CardContent className="pt-0">
          {children}
        </CardContent>
      )}
    </Card>
  );
};

export default UnifiedCard;
