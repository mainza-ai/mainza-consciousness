/**
 * Unified Tabs Component
 * Consolidates all tabs components into a single, consistent component
 * 
 * This component provides the definitive tabs interface that:
 * - Consolidates all tabs variations into one unified component
 * - Ensures consistent styling across all tabs usage
 * - Provides reusable and consistent tabs functionality
 * - Integrates seamlessly with the unified design system
 * 
 * Author: Mainza AI Consciousness Team
 * Date: 2025-10-01
 */

import React from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { cn } from '@/lib/utils';
import { UnifiedTabsProps } from '@/lib/unified-design-system';

export const UnifiedTabs: React.FC<UnifiedTabsProps> = ({
  className,
  children,
  defaultValue,
  value,
  onValueChange,
  orientation = 'horizontal',
  tabs,
  disabled = false,
  loading = false,
  animated = true,
  dataTestId,
}) => {
  const baseClasses = cn(
    'w-full transition-all duration-200',
    {
      'opacity-50 pointer-events-none': disabled,
      'animate-pulse': loading,
    },
    className
  );
  
  const tabsListClasses = cn(
    'grid w-full transition-all duration-200',
    {
      'grid-cols-1': orientation === 'vertical',
      'grid-cols-auto': orientation === 'horizontal',
      'grid-flow-col': orientation === 'horizontal',
    }
  );
  
  const tabsTriggerClasses = cn(
    'transition-all duration-200',
    {
      'hover:scale-105': animated && !disabled && !loading,
    }
  );
  
  return (
    <Tabs
      defaultValue={defaultValue}
      value={value}
      onValueChange={onValueChange}
      orientation={orientation}
      className={baseClasses}
      data-testid={dataTestId}
    >
      <TabsList className={tabsListClasses}>
        {tabs.map((tab) => (
          <TabsTrigger
            key={tab.value}
            value={tab.value}
            disabled={disabled || loading || tab.disabled}
            className={tabsTriggerClasses}
          >
            {tab.icon && (
              <span className="mr-2">{tab.icon}</span>
            )}
            {tab.label}
          </TabsTrigger>
        ))}
      </TabsList>
      
      {tabs.map((tab) => (
        <TabsContent
          key={tab.value}
          value={tab.value}
          className="mt-4"
        >
          {tab.content}
        </TabsContent>
      ))}
      
      {children}
    </Tabs>
  );
};

export default UnifiedTabs;
