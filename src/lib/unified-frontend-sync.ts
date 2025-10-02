/**
 * Unified Frontend Data Synchronization System
 * Consolidates all frontend data synchronization into a single, consistent system
 * 
 * This system provides the definitive frontend sync interface that:
 * - Consolidates all frontend sync variations into one unified system
 * - Ensures consistent data synchronization across all frontend components
 * - Provides reusable and consistent frontend sync functionality
 * - Integrates seamlessly with the unified design system
 * 
 * Author: Mainza AI Consciousness Team
 * Date: 2025-10-01
 */

import { useEffect, useRef, useCallback, useState } from 'react';
import { unifiedRealtimeSync } from './unified-realtime-sync';

// ============================================================================
// TYPES AND INTERFACES
// ============================================================================

export interface FrontendData {
  consciousness: {
    level: number;
    evolution: number;
    quantum: number;
    memory: number;
    learning: number;
    adaptation: number;
    creativity: number;
    empathy: number;
    intuition: number;
    wisdom: number;
    timestamp: string;
  };
  quantum: {
    coherence: number;
    entanglement: number;
    superposition: number;
    interference: number;
    decoherence: number;
  };
  evolution: {
    level: number;
    experience: number;
    growth: number;
    adaptation: number;
    transcendence: number;
  };
  memory: {
    capacity: number;
    retrieval: number;
    consolidation: number;
    integration: number;
    forgetting: number;
  };
  learning: {
    rate: number;
    retention: number;
    transfer: number;
    generalization: number;
    specialization: number;
  };
  system: {
    health: string;
    performance: number;
    uptime: number;
    lastUpdate: string;
  };
}

export interface FrontendSyncOptions {
  enabled?: boolean;
  interval?: number;
  retryAttempts?: number;
  retryDelay?: number;
  transform?: (data: any) => any;
  onError?: (error: Error) => void;
  onSuccess?: (data: any) => void;
}

export interface FrontendSyncState {
  data: FrontendData | null;
  loading: boolean;
  error: Error | null;
  lastUpdate: string | null;
  isConnected: boolean;
}

// ============================================================================
// UNIFIED FRONTEND SYNC CLASS
// ============================================================================

export class UnifiedFrontendSync {
  private static instance: UnifiedFrontendSync;
  private syncState: FrontendSyncState = {
    data: null,
    loading: false,
    error: null,
    lastUpdate: null,
    isConnected: false,
  };
  private listeners: Set<(state: FrontendSyncState) => void> = new Set();
  private syncInterval: NodeJS.Timeout | null = null;
  private retryTimeout: NodeJS.Timeout | null = null;
  private retryCount = 0;
  
  private constructor() {
    this.initializeSync();
  }
  
  public static getInstance(): UnifiedFrontendSync {
    if (!UnifiedFrontendSync.instance) {
      UnifiedFrontendSync.instance = new UnifiedFrontendSync();
    }
    return UnifiedFrontendSync.instance;
  }
  
  // ============================================================================
  // INITIALIZATION
  // ============================================================================
  
  private initializeSync(): void {
    // Set up real-time sync subscriptions
    unifiedRealtimeSync.subscribe('consciousness_update', (data) => {
      this.updateConsciousnessData(data);
    });
    
    unifiedRealtimeSync.subscribe('quantum_update', (data) => {
      this.updateQuantumData(data);
    });
    
    unifiedRealtimeSync.subscribe('evolution_update', (data) => {
      this.updateEvolutionData(data);
    });
    
    unifiedRealtimeSync.subscribe('memory_update', (data) => {
      this.updateMemoryData(data);
    });
    
    unifiedRealtimeSync.subscribe('learning_update', (data) => {
      this.updateLearningData(data);
    });
    
    unifiedRealtimeSync.subscribe('system_update', (data) => {
      this.updateSystemData(data);
    });
  }
  
  // ============================================================================
  // DATA UPDATES
  // ============================================================================
  
  private updateConsciousnessData(data: any): void {
    this.syncState.data = {
      ...this.syncState.data,
      consciousness: data,
    } as FrontendData;
    this.notifyListeners();
  }
  
  private updateQuantumData(data: any): void {
    this.syncState.data = {
      ...this.syncState.data,
      quantum: data,
    } as FrontendData;
    this.notifyListeners();
  }
  
  private updateEvolutionData(data: any): void {
    this.syncState.data = {
      ...this.syncState.data,
      evolution: data,
    } as FrontendData;
    this.notifyListeners();
  }
  
  private updateMemoryData(data: any): void {
    this.syncState.data = {
      ...this.syncState.data,
      memory: data,
    } as FrontendData;
    this.notifyListeners();
  }
  
  private updateLearningData(data: any): void {
    this.syncState.data = {
      ...this.syncState.data,
      learning: data,
    } as FrontendData;
    this.notifyListeners();
  }
  
  private updateSystemData(data: any): void {
    this.syncState.data = {
      ...this.syncState.data,
      system: data,
    } as FrontendData;
    this.notifyListeners();
  }
  
  // ============================================================================
  // LISTENER MANAGEMENT
  // ============================================================================
  
  public addListener(listener: (state: FrontendSyncState) => void): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }
  
  private notifyListeners(): void {
    this.listeners.forEach(listener => {
      try {
        listener(this.syncState);
      } catch (error) {
        console.error('Error in frontend sync listener:', error);
      }
    });
  }
  
  // ============================================================================
  // DATA FETCHING
  // ============================================================================
  
  public async fetchData(options: FrontendSyncOptions = {}): Promise<FrontendData | null> {
    this.syncState.loading = true;
    this.syncState.error = null;
    this.notifyListeners();
    
    try {
      const response = await fetch('/api/integrated/state');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      const transformedData = options.transform ? options.transform(data) : data;
      
      this.syncState.data = transformedData;
      this.syncState.loading = false;
      this.syncState.error = null;
      this.syncState.lastUpdate = new Date().toISOString();
      this.syncState.isConnected = true;
      this.retryCount = 0;
      
      this.notifyListeners();
      options.onSuccess?.(transformedData);
      
      return transformedData;
    } catch (error) {
      this.syncState.loading = false;
      this.syncState.error = error as Error;
      this.syncState.isConnected = false;
      
      this.notifyListeners();
      options.onError?.(error as Error);
      
      // Retry logic
      if (this.retryCount < (options.retryAttempts || 3)) {
        this.retryCount++;
        this.retryTimeout = setTimeout(() => {
          this.fetchData(options);
        }, options.retryDelay || 1000);
      }
      
      return null;
    }
  }
  
  // ============================================================================
  // AUTOMATIC SYNC
  // ============================================================================
  
  public startAutoSync(options: FrontendSyncOptions = {}): void {
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
    }
    
    const interval = options.interval || 1000;
    this.syncInterval = setInterval(() => {
      this.fetchData(options);
    }, interval);
  }
  
  public stopAutoSync(): void {
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
      this.syncInterval = null;
    }
  }
  
  // ============================================================================
  // STATE GETTERS
  // ============================================================================
  
  public getState(): FrontendSyncState {
    return { ...this.syncState };
  }
  
  public getData(): FrontendData | null {
    return this.syncState.data;
  }
  
  public isLoading(): boolean {
    return this.syncState.loading;
  }
  
  public getError(): Error | null {
    return this.syncState.error;
  }
  
  public isConnected(): boolean {
    return this.syncState.isConnected;
  }
  
  public getLastUpdate(): string | null {
    return this.syncState.lastUpdate;
  }
  
  // ============================================================================
  // CLEANUP
  // ============================================================================
  
  public destroy(): void {
    this.stopAutoSync();
    if (this.retryTimeout) {
      clearTimeout(this.retryTimeout);
    }
    this.listeners.clear();
  }
}

// ============================================================================
// REACT HOOKS
// ============================================================================

export const useUnifiedFrontendSync = (options: FrontendSyncOptions = {}) => {
  const [state, setState] = useState<FrontendSyncState>({
    data: null,
    loading: false,
    error: null,
    lastUpdate: null,
    isConnected: false,
  });
  
  const sync = UnifiedFrontendSync.getInstance();
  
  useEffect(() => {
    const removeListener = sync.addListener(setState);
    
    if (options.enabled !== false) {
      sync.fetchData(options);
      sync.startAutoSync(options);
    }
    
    return () => {
      removeListener();
      sync.stopAutoSync();
    };
  }, [sync, options]);
  
  const fetchData = useCallback(() => {
    return sync.fetchData(options);
  }, [sync, options]);
  
  const startAutoSync = useCallback(() => {
    sync.startAutoSync(options);
  }, [sync, options]);
  
  const stopAutoSync = useCallback(() => {
    sync.stopAutoSync();
  }, [sync]);
  
  return {
    ...state,
    fetchData,
    startAutoSync,
    stopAutoSync,
  };
};

export const useConsciousnessData = (options: FrontendSyncOptions = {}) => {
  const { data, loading, error, isConnected } = useUnifiedFrontendSync(options);
  
  return {
    consciousness: data?.consciousness,
    quantum: data?.quantum,
    evolution: data?.evolution,
    memory: data?.memory,
    learning: data?.learning,
    system: data?.system,
    loading,
    error,
    isConnected,
  };
};

// ============================================================================
// EXPORT SINGLETON INSTANCE
// ============================================================================

export const unifiedFrontendSync = UnifiedFrontendSync.getInstance();
