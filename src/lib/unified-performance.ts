/**
 * Unified Performance Optimization System
 * Consolidates all performance optimization into a single, consistent system
 * 
 * This system provides the definitive performance optimization interface that:
 * - Consolidates all performance optimization variations into one unified system
 * - Ensures consistent performance across all frontend components
 * - Provides reusable and consistent performance functionality
 * - Integrates seamlessly with the unified design system
 * 
 * Author: Mainza AI Consciousness Team
 * Date: 2025-10-01
 */

import React, { useEffect, useRef, useCallback, useState, useMemo } from 'react';

// ============================================================================
// TYPES AND INTERFACES
// ============================================================================

export interface PerformanceMetrics {
  renderTime: number;
  memoryUsage: number;
  componentCount: number;
  reRenderCount: number;
  lastUpdate: string;
}

export interface PerformanceOptions {
  enabled?: boolean;
  threshold?: number;
  sampling?: number;
  onPerformanceIssue?: (metrics: PerformanceMetrics) => void;
}

export interface PerformanceState {
  metrics: PerformanceMetrics;
  isOptimized: boolean;
  warnings: string[];
  recommendations: string[];
}

// ============================================================================
// UNIFIED PERFORMANCE CLASS
// ============================================================================

export class UnifiedPerformance {
  private static instance: UnifiedPerformance;
  private metrics: PerformanceMetrics = {
    renderTime: 0,
    memoryUsage: 0,
    componentCount: 0,
    reRenderCount: 0,
    lastUpdate: new Date().toISOString(),
  };
  private listeners: Set<(state: PerformanceState) => void> = new Set();
  private performanceObserver: PerformanceObserver | null = null;
  private renderStartTime: number = 0;
  private componentCount = 0;
  private reRenderCount = 0;
  
  private constructor() {
    this.initializePerformanceMonitoring();
  }
  
  public static getInstance(): UnifiedPerformance {
    if (!UnifiedPerformance.instance) {
      UnifiedPerformance.instance = new UnifiedPerformance();
    }
    return UnifiedPerformance.instance;
  }
  
  // ============================================================================
  // INITIALIZATION
  // ============================================================================
  
  private initializePerformanceMonitoring(): void {
    if (typeof window !== 'undefined' && 'PerformanceObserver' in window) {
      this.performanceObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach((entry) => {
          if (entry.entryType === 'measure') {
            this.updateRenderTime(entry.duration);
          }
        });
      });
      
      this.performanceObserver.observe({ entryTypes: ['measure'] });
    }
    
    // Monitor memory usage
    this.startMemoryMonitoring();
  }
  
  private startMemoryMonitoring(): void {
    setInterval(() => {
      if ('memory' in performance) {
        const memory = (performance as any).memory;
        this.metrics.memoryUsage = memory.usedJSHeapSize / memory.jsHeapSizeLimit;
      }
    }, 1000);
  }
  
  // ============================================================================
  // PERFORMANCE TRACKING
  // ============================================================================
  
  public startRender(): void {
    this.renderStartTime = performance.now();
  }
  
  public endRender(): void {
    if (this.renderStartTime > 0) {
      const renderTime = performance.now() - this.renderStartTime;
      this.updateRenderTime(renderTime);
      this.renderStartTime = 0;
    }
  }
  
  private updateRenderTime(renderTime: number): void {
    this.metrics.renderTime = renderTime;
    this.metrics.lastUpdate = new Date().toISOString();
    this.notifyListeners();
  }
  
  public incrementComponentCount(): void {
    this.componentCount++;
    this.metrics.componentCount = this.componentCount;
    this.metrics.lastUpdate = new Date().toISOString();
    this.notifyListeners();
  }
  
  public incrementReRenderCount(): void {
    this.reRenderCount++;
    this.metrics.reRenderCount = this.reRenderCount;
    this.metrics.lastUpdate = new Date().toISOString();
    this.notifyListeners();
  }
  
  // ============================================================================
  // LISTENER MANAGEMENT
  // ============================================================================
  
  public addListener(listener: (state: PerformanceState) => void): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }
  
  private notifyListeners(): void {
    const state: PerformanceState = {
      metrics: this.metrics,
      isOptimized: this.isOptimized(),
      warnings: this.getWarnings(),
      recommendations: this.getRecommendations(),
    };
    
    this.listeners.forEach(listener => {
      try {
        listener(state);
      } catch (error) {
        console.error('Error in performance listener:', error);
      }
    });
  }
  
  // ============================================================================
  // PERFORMANCE ANALYSIS
  // ============================================================================
  
  private isOptimized(): boolean {
    return (
      this.metrics.renderTime < 16 && // 60fps
      this.metrics.memoryUsage < 0.8 && // 80% memory usage
      this.metrics.reRenderCount < this.metrics.componentCount * 0.1 // 10% re-render ratio
    );
  }
  
  private getWarnings(): string[] {
    const warnings: string[] = [];
    
    if (this.metrics.renderTime > 16) {
      warnings.push(`Render time ${this.metrics.renderTime.toFixed(2)}ms exceeds 16ms threshold`);
    }
    
    if (this.metrics.memoryUsage > 0.8) {
      warnings.push(`Memory usage ${(this.metrics.memoryUsage * 100).toFixed(1)}% exceeds 80% threshold`);
    }
    
    if (this.metrics.reRenderCount > this.metrics.componentCount * 0.1) {
      warnings.push(`Re-render count ${this.metrics.reRenderCount} exceeds 10% of component count`);
    }
    
    return warnings;
  }
  
  private getRecommendations(): string[] {
    const recommendations: string[] = [];
    
    if (this.metrics.renderTime > 16) {
      recommendations.push('Consider using React.memo() for expensive components');
      recommendations.push('Implement useMemo() for expensive calculations');
      recommendations.push('Use useCallback() for event handlers');
    }
    
    if (this.metrics.memoryUsage > 0.8) {
      recommendations.push('Consider implementing virtual scrolling');
      recommendations.push('Use lazy loading for large datasets');
      recommendations.push('Implement component cleanup in useEffect');
    }
    
    if (this.metrics.reRenderCount > this.metrics.componentCount * 0.1) {
      recommendations.push('Check for unnecessary state updates');
      recommendations.push('Use useMemo() to prevent unnecessary recalculations');
      recommendations.push('Consider splitting large components');
    }
    
    return recommendations;
  }
  
  // ============================================================================
  // STATE GETTERS
  // ============================================================================
  
  public getMetrics(): PerformanceMetrics {
    return { ...this.metrics };
  }
  
  public getState(): PerformanceState {
    return {
      metrics: this.metrics,
      isOptimized: this.isOptimized(),
      warnings: this.getWarnings(),
      recommendations: this.getRecommendations(),
    };
  }
  
  // ============================================================================
  // CLEANUP
  // ============================================================================
  
  public destroy(): void {
    if (this.performanceObserver) {
      this.performanceObserver.disconnect();
    }
    this.listeners.clear();
  }
}

// ============================================================================
// REACT HOOKS
// ============================================================================

export const useUnifiedPerformance = (options: PerformanceOptions = {}) => {
  const [state, setState] = useState<PerformanceState>({
    metrics: {
      renderTime: 0,
      memoryUsage: 0,
      componentCount: 0,
      reRenderCount: 0,
      lastUpdate: new Date().toISOString(),
    },
    isOptimized: true,
    warnings: [],
    recommendations: [],
  });
  
  const performance = UnifiedPerformance.getInstance();
  
  useEffect(() => {
    if (options.enabled !== false) {
      const removeListener = performance.addListener(setState);
      return removeListener;
    }
  }, [performance, options]);
  
  const startRender = useCallback(() => {
    performance.startRender();
  }, [performance]);
  
  const endRender = useCallback(() => {
    performance.endRender();
  }, [performance]);
  
  const incrementComponentCount = useCallback(() => {
    performance.incrementComponentCount();
  }, [performance]);
  
  const incrementReRenderCount = useCallback(() => {
    performance.incrementReRenderCount();
  }, [performance]);
  
  return {
    ...state,
    startRender,
    endRender,
    incrementComponentCount,
    incrementReRenderCount,
  };
};

export const usePerformanceOptimization = (options: PerformanceOptions = {}) => {
  const { startRender, endRender, incrementComponentCount, incrementReRenderCount } = useUnifiedPerformance(options);
  
  useEffect(() => {
    startRender();
    return () => endRender();
  }, [startRender, endRender]);
  
  useEffect(() => {
    incrementComponentCount();
  }, [incrementComponentCount]);
  
  useEffect(() => {
    incrementReRenderCount();
  });
  
  return {
    startRender,
    endRender,
    incrementComponentCount,
    incrementReRenderCount,
  };
};

// ============================================================================
// PERFORMANCE UTILITIES
// ============================================================================

export const withPerformanceTracking = <P extends object>(
  Component: React.ComponentType<P>
): React.ComponentType<P> => {
  return React.memo((props: P) => {
    const { startRender, endRender, incrementComponentCount } = usePerformanceOptimization();
    
    useEffect(() => {
      startRender();
      incrementComponentCount();
      return () => endRender();
    }, [startRender, endRender, incrementComponentCount]);
    
    return <Component {...props} />;
  });
};

export const useMemoizedCallback = <T extends (...args: any[]) => any>(
  callback: T,
  deps: React.DependencyList
): T => {
  return useCallback(callback, deps);
};

export const useMemoizedValue = <T>(
  value: T,
  deps: React.DependencyList
): T => {
  return useMemo(() => value, deps);
};

// ============================================================================
// EXPORT SINGLETON INSTANCE
// ============================================================================

export const unifiedPerformance = UnifiedPerformance.getInstance();
