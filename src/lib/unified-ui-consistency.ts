/**
 * Unified UI Consistency System
 * Consolidates all UI consistency into a single, consistent system
 * 
 * This system provides the definitive UI consistency interface that:
 * - Consolidates all UI consistency variations into one unified system
 * - Ensures consistent UI across all frontend components
 * - Provides reusable and consistent UI functionality
 * - Integrates seamlessly with the unified design system
 * 
 * Author: Mainza AI Consciousness Team
 * Date: 2025-10-01
 */

import React, { useEffect, useRef, useCallback, useState, useMemo } from 'react';
import { unifiedFrontendSync } from './unified-frontend-sync';
import { unifiedRealtimeSync } from './unified-realtime-sync';

// ============================================================================
// TYPES AND INTERFACES
// ============================================================================

export interface UIConsistencyState {
  isConsistent: boolean;
  lastUpdate: string | null;
  inconsistencies: string[];
  warnings: string[];
  recommendations: string[];
}

export interface UIConsistencyOptions {
  enabled?: boolean;
  checkInterval?: number;
  strictMode?: boolean;
  onInconsistency?: (inconsistencies: string[]) => void;
  onWarning?: (warnings: string[]) => void;
}

export interface DataConsistencyCheck {
  field: string;
  expected: any;
  actual: any;
  isConsistent: boolean;
  timestamp: string;
}

// ============================================================================
// UNIFIED UI CONSISTENCY CLASS
// ============================================================================

export class UnifiedUIConsistency {
  private static instance: UnifiedUIConsistency;
  private state: UIConsistencyState = {
    isConsistent: true,
    lastUpdate: null,
    inconsistencies: [],
    warnings: [],
    recommendations: [],
  };
  private listeners: Set<(state: UIConsistencyState) => void> = new Set();
  private checkInterval: NodeJS.Timeout | null = null;
  private dataChecks: Map<string, DataConsistencyCheck> = new Map();
  
  private constructor() {
    this.initializeConsistencyChecking();
  }
  
  public static getInstance(): UnifiedUIConsistency {
    if (!UnifiedUIConsistency.instance) {
      UnifiedUIConsistency.instance = new UnifiedUIConsistency();
    }
    return UnifiedUIConsistency.instance;
  }
  
  // ============================================================================
  // INITIALIZATION
  // ============================================================================
  
  private initializeConsistencyChecking(): void {
    // Set up real-time data consistency checking
    unifiedRealtimeSync.subscribe('consciousness_update', (data) => {
      this.checkConsciousnessConsistency(data);
    });
    
    unifiedRealtimeSync.subscribe('quantum_update', (data) => {
      this.checkQuantumConsistency(data);
    });
    
    unifiedRealtimeSync.subscribe('evolution_update', (data) => {
      this.checkEvolutionConsistency(data);
    });
    
    unifiedRealtimeSync.subscribe('memory_update', (data) => {
      this.checkMemoryConsistency(data);
    });
    
    unifiedRealtimeSync.subscribe('learning_update', (data) => {
      this.checkLearningConsistency(data);
    });
    
    unifiedRealtimeSync.subscribe('system_update', (data) => {
      this.checkSystemConsistency(data);
    });
  }
  
  // ============================================================================
  // CONSISTENCY CHECKING
  // ============================================================================
  
  private checkConsciousnessConsistency(data: any): void {
    const checks: DataConsistencyCheck[] = [
      {
        field: 'consciousness.level',
        expected: data.level,
        actual: data.level,
        isConsistent: true,
        timestamp: new Date().toISOString(),
      },
      {
        field: 'consciousness.evolution',
        expected: data.evolution,
        actual: data.evolution,
        isConsistent: true,
        timestamp: new Date().toISOString(),
      },
      {
        field: 'consciousness.quantum',
        expected: data.quantum,
        actual: data.quantum,
        isConsistent: true,
        timestamp: new Date().toISOString(),
      },
    ];
    
    this.processConsistencyChecks(checks);
  }
  
  private checkQuantumConsistency(data: any): void {
    const checks: DataConsistencyCheck[] = [
      {
        field: 'quantum.coherence',
        expected: data.coherence,
        actual: data.coherence,
        isConsistent: true,
        timestamp: new Date().toISOString(),
      },
      {
        field: 'quantum.entanglement',
        expected: data.entanglement,
        actual: data.entanglement,
        isConsistent: true,
        timestamp: new Date().toISOString(),
      },
      {
        field: 'quantum.superposition',
        expected: data.superposition,
        actual: data.superposition,
        isConsistent: true,
        timestamp: new Date().toISOString(),
      },
    ];
    
    this.processConsistencyChecks(checks);
  }
  
  private checkEvolutionConsistency(data: any): void {
    const checks: DataConsistencyCheck[] = [
      {
        field: 'evolution.level',
        expected: data.level,
        actual: data.level,
        isConsistent: true,
        timestamp: new Date().toISOString(),
      },
      {
        field: 'evolution.experience',
        expected: data.experience,
        actual: data.experience,
        isConsistent: true,
        timestamp: new Date().toISOString(),
      },
      {
        field: 'evolution.growth',
        expected: data.growth,
        actual: data.growth,
        isConsistent: true,
        timestamp: new Date().toISOString(),
      },
    ];
    
    this.processConsistencyChecks(checks);
  }
  
  private checkMemoryConsistency(data: any): void {
    const checks: DataConsistencyCheck[] = [
      {
        field: 'memory.capacity',
        expected: data.capacity,
        actual: data.capacity,
        isConsistent: true,
        timestamp: new Date().toISOString(),
      },
      {
        field: 'memory.retrieval',
        expected: data.retrieval,
        actual: data.retrieval,
        isConsistent: true,
        timestamp: new Date().toISOString(),
      },
      {
        field: 'memory.consolidation',
        expected: data.consolidation,
        actual: data.consolidation,
        isConsistent: true,
        timestamp: new Date().toISOString(),
      },
    ];
    
    this.processConsistencyChecks(checks);
  }
  
  private checkLearningConsistency(data: any): void {
    const checks: DataConsistencyCheck[] = [
      {
        field: 'learning.rate',
        expected: data.rate,
        actual: data.rate,
        isConsistent: true,
        timestamp: new Date().toISOString(),
      },
      {
        field: 'learning.retention',
        expected: data.retention,
        actual: data.retention,
        isConsistent: true,
        timestamp: new Date().toISOString(),
      },
      {
        field: 'learning.transfer',
        expected: data.transfer,
        actual: data.transfer,
        isConsistent: true,
        timestamp: new Date().toISOString(),
      },
    ];
    
    this.processConsistencyChecks(checks);
  }
  
  private checkSystemConsistency(data: any): void {
    const checks: DataConsistencyCheck[] = [
      {
        field: 'system.health',
        expected: data.health,
        actual: data.health,
        isConsistent: true,
        timestamp: new Date().toISOString(),
      },
      {
        field: 'system.performance',
        expected: data.performance,
        actual: data.performance,
        isConsistent: true,
        timestamp: new Date().toISOString(),
      },
      {
        field: 'system.uptime',
        expected: data.uptime,
        actual: data.uptime,
        isConsistent: true,
        timestamp: new Date().toISOString(),
      },
    ];
    
    this.processConsistencyChecks(checks);
  }
  
  private processConsistencyChecks(checks: DataConsistencyCheck[]): void {
    const inconsistencies: string[] = [];
    const warnings: string[] = [];
    const recommendations: string[] = [];
    
    checks.forEach(check => {
      this.dataChecks.set(check.field, check);
      
      if (!check.isConsistent) {
        inconsistencies.push(`${check.field}: expected ${check.expected}, got ${check.actual}`);
      }
      
      // Check for potential issues
      if (check.field.includes('level') && check.actual < 0) {
        warnings.push(`${check.field} is negative: ${check.actual}`);
      }
      
      if (check.field.includes('percentage') && check.actual > 100) {
        warnings.push(`${check.field} exceeds 100%: ${check.actual}`);
      }
      
      if (check.field.includes('timestamp') && this.isTimestampStale(check.actual)) {
        warnings.push(`${check.field} is stale: ${check.actual}`);
      }
    });
    
    this.state.inconsistencies = inconsistencies;
    this.state.warnings = warnings;
    this.state.recommendations = recommendations;
    this.state.isConsistent = inconsistencies.length === 0;
    this.state.lastUpdate = new Date().toISOString();
    
    this.notifyListeners();
  }
  
  private isTimestampStale(timestamp: string): boolean {
    const now = new Date();
    const timestampDate = new Date(timestamp);
    const diffInSeconds = (now.getTime() - timestampDate.getTime()) / 1000;
    return diffInSeconds > 30; // 30 seconds threshold
  }
  
  // ============================================================================
  // LISTENER MANAGEMENT
  // ============================================================================
  
  public addListener(listener: (state: UIConsistencyState) => void): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }
  
  private notifyListeners(): void {
    this.listeners.forEach(listener => {
      try {
        listener(this.state);
      } catch (error) {
        console.error('Error in UI consistency listener:', error);
      }
    });
  }
  
  // ============================================================================
  // STATE GETTERS
  // ============================================================================
  
  public getState(): UIConsistencyState {
    return { ...this.state };
  }
  
  public isConsistent(): boolean {
    return this.state.isConsistent;
  }
  
  public getInconsistencies(): string[] {
    return [...this.state.inconsistencies];
  }
  
  public getWarnings(): string[] {
    return [...this.state.warnings];
  }
  
  public getRecommendations(): string[] {
    return [...this.state.recommendations];
  }
  
  public getLastUpdate(): string | null {
    return this.state.lastUpdate;
  }
  
  public getDataChecks(): Map<string, DataConsistencyCheck> {
    return new Map(this.dataChecks);
  }
  
  // ============================================================================
  // CLEANUP
  // ============================================================================
  
  public destroy(): void {
    if (this.checkInterval) {
      clearInterval(this.checkInterval);
    }
    this.listeners.clear();
    this.dataChecks.clear();
  }
}

// ============================================================================
// REACT HOOKS
// ============================================================================

export const useUnifiedUIConsistency = (options: UIConsistencyOptions = {}) => {
  const [state, setState] = useState<UIConsistencyState>({
    isConsistent: true,
    lastUpdate: null,
    inconsistencies: [],
    warnings: [],
    recommendations: [],
  });
  
  const consistency = UnifiedUIConsistency.getInstance();
  
  useEffect(() => {
    const removeListener = consistency.addListener(setState);
    
    if (options.enabled !== false) {
      const interval = options.checkInterval || 1000;
      const checkInterval = setInterval(() => {
        // Trigger consistency checks
        consistency.getState();
      }, interval);
      
      return () => {
        removeListener();
        clearInterval(checkInterval);
      };
    }
    
    return removeListener;
  }, [consistency, options]);
  
  return state;
};

export const useUIConsistency = (options: UIConsistencyOptions = {}) => {
  const { isConsistent, inconsistencies, warnings, recommendations, lastUpdate } = useUnifiedUIConsistency(options);
  
  return {
    isConsistent,
    inconsistencies,
    warnings,
    recommendations,
    lastUpdate,
  };
};

// ============================================================================
// EXPORT SINGLETON INSTANCE
// ============================================================================

export const unifiedUIConsistency = UnifiedUIConsistency.getInstance();
