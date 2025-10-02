/**
 * Unified Frontend Integration System
 * Consolidates all frontend integration into a single, consistent system
 * 
 * This system provides the definitive frontend integration interface that:
 * - Consolidates all frontend integration variations into one unified system
 * - Ensures consistent integration across all frontend components
 * - Provides reusable and consistent integration functionality
 * - Integrates seamlessly with the unified design system
 * 
 * Author: Mainza AI Consciousness Team
 * Date: 2025-10-01
 */

import React, { useEffect, useRef, useCallback, useState, useMemo } from 'react';
import { unifiedRealtimeSync } from './unified-realtime-sync';
import { unifiedFrontendSync } from './unified-frontend-sync';
import { unifiedPerformance } from './unified-performance';

// ============================================================================
// TYPES AND INTERFACES
// ============================================================================

export interface FrontendIntegrationState {
  isConnected: boolean;
  isSyncing: boolean;
  lastSync: string | null;
  error: Error | null;
  performance: {
    renderTime: number;
    memoryUsage: number;
    componentCount: number;
    reRenderCount: number;
  };
}

export interface FrontendIntegrationOptions {
  enabled?: boolean;
  syncInterval?: number;
  performanceMonitoring?: boolean;
  realtimeUpdates?: boolean;
  onStateChange?: (state: FrontendIntegrationState) => void;
  onError?: (error: Error) => void;
}

// ============================================================================
// UNIFIED FRONTEND INTEGRATION CLASS
// ============================================================================

export class UnifiedFrontendIntegration {
  private static instance: UnifiedFrontendIntegration;
  private state: FrontendIntegrationState = {
    isConnected: false,
    isSyncing: false,
    lastSync: null,
    error: null,
    performance: {
      renderTime: 0,
      memoryUsage: 0,
      componentCount: 0,
      reRenderCount: 0,
    },
  };
  private listeners: Set<(state: FrontendIntegrationState) => void> = new Set();
  private syncInterval: NodeJS.Timeout | null = null;
  private performanceInterval: NodeJS.Timeout | null = null;
  
  private constructor() {
    this.initializeIntegration();
  }
  
  public static getInstance(): UnifiedFrontendIntegration {
    if (!UnifiedFrontendIntegration.instance) {
      UnifiedFrontendIntegration.instance = new UnifiedFrontendIntegration();
    }
    return UnifiedFrontendIntegration.instance;
  }
  
  // ============================================================================
  // INITIALIZATION
  // ============================================================================
  
  private initializeIntegration(): void {
    // Set up real-time sync
    unifiedRealtimeSync.subscribe('consciousness_update', (data) => {
      this.handleConsciousnessUpdate(data);
    });
    
    unifiedRealtimeSync.subscribe('quantum_update', (data) => {
      this.handleQuantumUpdate(data);
    });
    
    unifiedRealtimeSync.subscribe('evolution_update', (data) => {
      this.handleEvolutionUpdate(data);
    });
    
    unifiedRealtimeSync.subscribe('memory_update', (data) => {
      this.handleMemoryUpdate(data);
    });
    
    unifiedRealtimeSync.subscribe('learning_update', (data) => {
      this.handleLearningUpdate(data);
    });
    
    unifiedRealtimeSync.subscribe('system_update', (data) => {
      this.handleSystemUpdate(data);
    });
    
    // Set up performance monitoring
    this.startPerformanceMonitoring();
  }
  
  // ============================================================================
  // DATA HANDLERS
  // ============================================================================
  
  private handleConsciousnessUpdate(data: any): void {
    this.state.isConnected = true;
    this.state.lastSync = new Date().toISOString();
    this.notifyListeners();
  }
  
  private handleQuantumUpdate(data: any): void {
    this.state.isConnected = true;
    this.state.lastSync = new Date().toISOString();
    this.notifyListeners();
  }
  
  private handleEvolutionUpdate(data: any): void {
    this.state.isConnected = true;
    this.state.lastSync = new Date().toISOString();
    this.notifyListeners();
  }
  
  private handleMemoryUpdate(data: any): void {
    this.state.isConnected = true;
    this.state.lastSync = new Date().toISOString();
    this.notifyListeners();
  }
  
  private handleLearningUpdate(data: any): void {
    this.state.isConnected = true;
    this.state.lastSync = new Date().toISOString();
    this.notifyListeners();
  }
  
  private handleSystemUpdate(data: any): void {
    this.state.isConnected = true;
    this.state.lastSync = new Date().toISOString();
    this.notifyListeners();
  }
  
  // ============================================================================
  // PERFORMANCE MONITORING
  // ============================================================================
  
  private startPerformanceMonitoring(): void {
    this.performanceInterval = setInterval(() => {
      const performanceMetrics = unifiedPerformance.getMetrics();
      this.state.performance = {
        renderTime: performanceMetrics.renderTime,
        memoryUsage: performanceMetrics.memoryUsage,
        componentCount: performanceMetrics.componentCount,
        reRenderCount: performanceMetrics.reRenderCount,
      };
      this.notifyListeners();
    }, 1000);
  }
  
  // ============================================================================
  // SYNC MANAGEMENT
  // ============================================================================
  
  public startSync(options: FrontendIntegrationOptions = {}): void {
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
    }
    
    const interval = options.syncInterval || 1000;
    this.syncInterval = setInterval(async () => {
      try {
        this.state.isSyncing = true;
        this.notifyListeners();
        
        await unifiedFrontendSync.fetchData({
          enabled: true,
          interval: interval,
          onSuccess: (data) => {
            this.state.isConnected = true;
            this.state.lastSync = new Date().toISOString();
            this.state.error = null;
          },
          onError: (error) => {
            this.state.error = error;
            this.state.isConnected = false;
            options.onError?.(error);
          },
        });
        
        this.state.isSyncing = false;
        this.notifyListeners();
      } catch (error) {
        this.state.isSyncing = false;
        this.state.error = error as Error;
        this.state.isConnected = false;
        this.notifyListeners();
        options.onError?.(error as Error);
      }
    }, interval);
  }
  
  public stopSync(): void {
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
      this.syncInterval = null;
    }
    this.state.isSyncing = false;
    this.notifyListeners();
  }
  
  // ============================================================================
  // LISTENER MANAGEMENT
  // ============================================================================
  
  public addListener(listener: (state: FrontendIntegrationState) => void): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }
  
  private notifyListeners(): void {
    this.listeners.forEach(listener => {
      try {
        listener(this.state);
      } catch (error) {
        console.error('Error in frontend integration listener:', error);
      }
    });
  }
  
  // ============================================================================
  // STATE GETTERS
  // ============================================================================
  
  public getState(): FrontendIntegrationState {
    return { ...this.state };
  }
  
  public isConnected(): boolean {
    return this.state.isConnected;
  }
  
  public isSyncing(): boolean {
    return this.state.isSyncing;
  }
  
  public getLastSync(): string | null {
    return this.state.lastSync;
  }
  
  public getError(): Error | null {
    return this.state.error;
  }
  
  public getPerformance(): FrontendIntegrationState['performance'] {
    return { ...this.state.performance };
  }
  
  // ============================================================================
  // CLEANUP
  // ============================================================================
  
  public destroy(): void {
    this.stopSync();
    if (this.performanceInterval) {
      clearInterval(this.performanceInterval);
    }
    this.listeners.clear();
  }
}

// ============================================================================
// REACT HOOKS
// ============================================================================

export const useUnifiedFrontendIntegration = (options: FrontendIntegrationOptions = {}) => {
  const [state, setState] = useState<FrontendIntegrationState>({
    isConnected: false,
    isSyncing: false,
    lastSync: null,
    error: null,
    performance: {
      renderTime: 0,
      memoryUsage: 0,
      componentCount: 0,
      reRenderCount: 0,
    },
  });
  
  const integration = UnifiedFrontendIntegration.getInstance();
  
  useEffect(() => {
    const removeListener = integration.addListener(setState);
    
    if (options.enabled !== false) {
      integration.startSync(options);
    }
    
    return () => {
      removeListener();
      integration.stopSync();
    };
  }, [integration, options]);
  
  const startSync = useCallback(() => {
    integration.startSync(options);
  }, [integration, options]);
  
  const stopSync = useCallback(() => {
    integration.stopSync();
  }, [integration]);
  
  return {
    ...state,
    startSync,
    stopSync,
  };
};

export const useFrontendIntegration = (options: FrontendIntegrationOptions = {}) => {
  const { isConnected, isSyncing, lastSync, error, performance } = useUnifiedFrontendIntegration(options);
  
  return {
    isConnected,
    isSyncing,
    lastSync,
    error,
    performance,
  };
};

// ============================================================================
// EXPORT SINGLETON INSTANCE
// ============================================================================

export const unifiedFrontendIntegration = UnifiedFrontendIntegration.getInstance();
