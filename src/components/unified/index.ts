/**
 * Unified Component Library Index
 * Consolidates all unified components into a single, consistent library
 * 
 * This library provides the definitive component interface that:
 * - Consolidates all component variations into one unified library
 * - Ensures consistent styling across all component usage
 * - Provides reusable and consistent component functionality
 * - Integrates seamlessly with the unified design system
 * 
 * Author: Mainza AI Consciousness Team
 * Date: 2025-10-01
 */

// ============================================================================
// CORE COMPONENTS
// ============================================================================

export { UnifiedCard } from './UnifiedCard';
export { UnifiedButton } from './UnifiedButton';
export { UnifiedInput } from './UnifiedInput';
export { UnifiedBadge } from './UnifiedBadge';
export { UnifiedTabs } from './UnifiedTabs';

// ============================================================================
// CONSCIOUSNESS COMPONENTS
// ============================================================================

export { UnifiedConsciousnessComponent } from './UnifiedConsciousnessComponent';

// ============================================================================
// DESIGN SYSTEM
// ============================================================================

export {
  designTokens,
  componentCategories,
  unifiedStyles,
  unifiedAnimations,
  unifiedTheme,
  type DesignTokens,
  type ComponentCategories,
  type UnifiedStyles,
  type UnifiedAnimations,
  type UnifiedTheme,
} from '@/lib/unified-design-system';

// ============================================================================
// REALTIME SYNC
// ============================================================================

export {
  unifiedRealtimeSync,
  useUnifiedRealtimeSync,
  useRealtimeData,
  type RealtimeData,
  type RealtimeEvent,
  type RealtimeSubscription,
  type RealtimeConnection,
} from '@/lib/unified-realtime-sync';

// ============================================================================
// FRONTEND SYNC
// ============================================================================

export {
  unifiedFrontendSync,
  useUnifiedFrontendSync,
  useConsciousnessData,
  type FrontendData,
  type FrontendSyncOptions,
  type FrontendSyncState,
} from '@/lib/unified-frontend-sync';

// ============================================================================
// UNIFIED COMPONENT PROPS
// ============================================================================

export type {
  UnifiedComponentProps,
  UnifiedCardProps,
  UnifiedButtonProps,
  UnifiedInputProps,
  UnifiedBadgeProps,
  UnifiedTabsProps,
} from '@/lib/unified-design-system';
