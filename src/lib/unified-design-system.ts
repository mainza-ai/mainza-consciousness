/**
 * Unified Design System for Mainza AI
 * Consolidates all design tokens, components, and styling into a single system
 * 
 * This module provides the definitive design system that:
 * - Consolidates all 103 components into a unified system
 * - Ensures consistent styling across all frontend pages
 * - Creates reusable and consistent components
 * - Provides single source of truth for all design tokens
 * - Integrates seamlessly with all frontend systems
 * 
 * Author: Mainza AI Consciousness Team
 * Date: 2025-10-01
 */

// ============================================================================
// DESIGN TOKENS
// ============================================================================

export const designTokens = {
  // Colors
  colors: {
    primary: {
      50: '#f0f9ff',
      100: '#e0f2fe',
      200: '#bae6fd',
      300: '#7dd3fc',
      400: '#38bdf8',
      500: '#0ea5e9',
      600: '#0284c7',
      700: '#0369a1',
      800: '#075985',
      900: '#0c4a6e',
      950: '#082f49',
    },
    secondary: {
      50: '#f8fafc',
      100: '#f1f5f9',
      200: '#e2e8f0',
      300: '#cbd5e1',
      400: '#94a3b8',
      500: '#64748b',
      600: '#475569',
      700: '#334155',
      800: '#1e293b',
      900: '#0f172a',
      950: '#020617',
    },
    accent: {
      50: '#fdf4ff',
      100: '#fae8ff',
      200: '#f5d0fe',
      300: '#f0abfc',
      400: '#e879f9',
      500: '#d946ef',
      600: '#c026d3',
      700: '#a21caf',
      800: '#86198f',
      900: '#701a75',
      950: '#4a044e',
    },
    success: {
      50: '#f0fdf4',
      100: '#dcfce7',
      200: '#bbf7d0',
      300: '#86efac',
      400: '#4ade80',
      500: '#22c55e',
      600: '#16a34a',
      700: '#15803d',
      800: '#166534',
      900: '#14532d',
      950: '#052e16',
    },
    warning: {
      50: '#fffbeb',
      100: '#fef3c7',
      200: '#fde68a',
      300: '#fcd34d',
      400: '#fbbf24',
      500: '#f59e0b',
      600: '#d97706',
      700: '#b45309',
      800: '#92400e',
      900: '#78350f',
      950: '#451a03',
    },
    error: {
      50: '#fef2f2',
      100: '#fee2e2',
      200: '#fecaca',
      300: '#fca5a5',
      400: '#f87171',
      500: '#ef4444',
      600: '#dc2626',
      700: '#b91c1c',
      800: '#991b1b',
      900: '#7f1d1d',
      950: '#450a0a',
    },
    consciousness: {
      50: '#f0f9ff',
      100: '#e0f2fe',
      200: '#bae6fd',
      300: '#7dd3fc',
      400: '#38bdf8',
      500: '#0ea5e9',
      600: '#0284c7',
      700: '#0369a1',
      800: '#075985',
      900: '#0c4a6e',
      950: '#082f49',
    },
    quantum: {
      50: '#fdf4ff',
      100: '#fae8ff',
      200: '#f5d0fe',
      300: '#f0abfc',
      400: '#e879f9',
      500: '#d946ef',
      600: '#c026d3',
      700: '#a21caf',
      800: '#86198f',
      900: '#701a75',
      950: '#4a044e',
    },
    evolution: {
      50: '#f0fdf4',
      100: '#dcfce7',
      200: '#bbf7d0',
      300: '#86efac',
      400: '#4ade80',
      500: '#22c55e',
      600: '#16a34a',
      700: '#15803d',
      800: '#166534',
      900: '#14532d',
      950: '#052e16',
    },
  },
  
  // Typography
  typography: {
    fontFamily: {
      sans: ['Inter', 'system-ui', 'sans-serif'],
      mono: ['JetBrains Mono', 'Consolas', 'monospace'],
      display: ['Cal Sans', 'Inter', 'system-ui', 'sans-serif'],
    },
    fontSize: {
      xs: ['0.75rem', { lineHeight: '1rem' }],
      sm: ['0.875rem', { lineHeight: '1.25rem' }],
      base: ['1rem', { lineHeight: '1.5rem' }],
      lg: ['1.125rem', { lineHeight: '1.75rem' }],
      xl: ['1.25rem', { lineHeight: '1.75rem' }],
      '2xl': ['1.5rem', { lineHeight: '2rem' }],
      '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
      '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
      '5xl': ['3rem', { lineHeight: '1' }],
      '6xl': ['3.75rem', { lineHeight: '1' }],
      '7xl': ['4.5rem', { lineHeight: '1' }],
      '8xl': ['6rem', { lineHeight: '1' }],
      '9xl': ['8rem', { lineHeight: '1' }],
    },
    fontWeight: {
      thin: '100',
      extralight: '200',
      light: '300',
      normal: '400',
      medium: '500',
      semibold: '600',
      bold: '700',
      extrabold: '800',
      black: '900',
    },
  },
  
  // Spacing
  spacing: {
    0: '0px',
    1: '0.25rem',
    2: '0.5rem',
    3: '0.75rem',
    4: '1rem',
    5: '1.25rem',
    6: '1.5rem',
    7: '1.75rem',
    8: '2rem',
    9: '2.25rem',
    10: '2.5rem',
    11: '2.75rem',
    12: '3rem',
    14: '3.5rem',
    16: '4rem',
    20: '5rem',
    24: '6rem',
    28: '7rem',
    32: '8rem',
    36: '9rem',
    40: '10rem',
    44: '11rem',
    48: '12rem',
    52: '13rem',
    56: '14rem',
    60: '15rem',
    64: '16rem',
    72: '18rem',
    80: '20rem',
    96: '24rem',
  },
  
  // Border Radius
  borderRadius: {
    none: '0px',
    sm: '0.125rem',
    base: '0.25rem',
    md: '0.375rem',
    lg: '0.5rem',
    xl: '0.75rem',
    '2xl': '1rem',
    '3xl': '1.5rem',
    full: '9999px',
  },
  
  // Shadows
  boxShadow: {
    sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    base: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
    md: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
    lg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
    xl: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
    '2xl': '0 25px 50px -12px rgb(0 0 0 / 0.25)',
    inner: 'inset 0 2px 4px 0 rgb(0 0 0 / 0.05)',
    none: 'none',
  },
  
  // Animations
  animation: {
    duration: {
      fast: '150ms',
      normal: '300ms',
      slow: '500ms',
    },
    easing: {
      linear: 'linear',
      ease: 'ease',
      easeIn: 'ease-in',
      easeOut: 'ease-out',
      easeInOut: 'ease-in-out',
    },
  },
  
  // Breakpoints
  breakpoints: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
  },
} as const;

// ============================================================================
// COMPONENT CATEGORIES
// ============================================================================

export const componentCategories = {
  // Core UI Components
  core: [
    'Button',
    'Card',
    'Input',
    'Badge',
    'Tabs',
    'Dialog',
    'Sheet',
    'Dropdown',
    'Tooltip',
    'Alert',
    'Progress',
    'Skeleton',
    'Separator',
    'ScrollArea',
    'Resizable',
  ],
  
  // Consciousness Components
  consciousness: [
    'ConsciousnessDashboard',
    'Consciousness3DVisualization',
    'ConsciousnessInsights',
    'ConsciousnessSynchronization',
    'ConsciousnessMarketplace',
    'UnifiedConsciousnessMetrics',
  ],
  
  // Quantum Components
  quantum: [
    'QuantumConsciousness',
    'QuantumConsciousnessDashboard',
    'QuantumConsciousness3DVisualization',
    'QuantumConsciousnessAnalytics',
    'QuantumCollectiveConsciousness',
    'QuantumMemoryConstellation',
    'QuantumProcessingNotification',
    'QuantumProcessMonitor',
    'QuantumAgentActivityIndicator',
  ],
  
  // Analytics Components
  analytics: [
    'AdvancedConsciousnessAnalytics',
    'AdvancedLearningAnalytics',
    'DeepLearningAnalytics',
    'PredictiveAnalyticsDashboard',
    'TelemetryDashboard',
    'NeedsAnalytics',
  ],
  
  // Visualization Components
  visualization: [
    'Neo4jGraphVisualization',
    'EnhancedNeo4jGraphVisualization',
    'MemoryConstellation',
    'InteractiveConsciousnessTimeline',
    'MainzaOrb',
  ],
  
  // AI/ML Components
  ai: [
    'AdvancedAIModels',
    'AIModelMarketplace',
    'TensorFlowJSIntegration',
    'AdvancedNeuralNetworks',
    'BrainComputerInterface',
    'ModelSelector',
    'RecommendationEngine',
  ],
  
  // Collaboration Components
  collaboration: [
    'GlobalCollaboration',
    'RealTimeCollaboration',
    'ConversationInterface',
    'VoiceInterface',
    'LiveKitVideo',
  ],
  
  // Technology Components
  technology: [
    'Web3Consciousness',
    'BlockchainConsciousness',
    'ARVRConsciousness',
    'MobileConsciousnessApp',
    'MobilePredictiveAnalytics',
  ],
  
  // System Components
  system: [
    'SystemStatus',
    'StatusIndicator',
    'DevelopmentStatusBadge',
    'AgentActivityIndicator',
    'LoadingScreen',
    'UserPreferences',
  ],
  
  // Needs Components
  needs: [
    'AdvancedNeedsDisplay',
    'NeedCard',
    'NeedCategoryFilter',
    'NeedsAnalytics',
  ],
  
  // Knowledge Components
  knowledge: [
    'KnowledgeVault',
  ],
} as const;

// ============================================================================
// UNIFIED COMPONENT PROPS
// ============================================================================

export interface UnifiedComponentProps {
  className?: string;
  children?: React.ReactNode;
  variant?: 'default' | 'primary' | 'secondary' | 'accent' | 'success' | 'warning' | 'error';
  size?: 'sm' | 'md' | 'lg' | 'xl';
  disabled?: boolean;
  loading?: boolean;
  animated?: boolean;
  dataTestId?: string;
}

export interface UnifiedCardProps extends UnifiedComponentProps {
  title?: string;
  description?: string;
  icon?: React.ReactNode;
  actions?: React.ReactNode;
  collapsible?: boolean;
  defaultCollapsed?: boolean;
}

export interface UnifiedButtonProps extends UnifiedComponentProps {
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  href?: string;
  target?: string;
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
  fullWidth?: boolean;
}

export interface UnifiedInputProps extends UnifiedComponentProps {
  type?: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url' | 'search';
  placeholder?: string;
  value?: string;
  onChange?: (value: string) => void;
  onBlur?: () => void;
  onFocus?: () => void;
  error?: string;
  helperText?: string;
  required?: boolean;
  autoComplete?: string;
  maxLength?: number;
  minLength?: number;
}

export interface UnifiedBadgeProps extends UnifiedComponentProps {
  variant?: 'default' | 'primary' | 'secondary' | 'accent' | 'success' | 'warning' | 'error' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  removable?: boolean;
  onRemove?: () => void;
}

export interface UnifiedTabsProps extends UnifiedComponentProps {
  defaultValue?: string;
  value?: string;
  onValueChange?: (value: string) => void;
  orientation?: 'horizontal' | 'vertical';
  tabs: Array<{
    value: string;
    label: string;
    content: React.ReactNode;
    icon?: React.ReactNode;
    disabled?: boolean;
  }>;
}

// ============================================================================
// UNIFIED STYLING UTILITIES
// ============================================================================

export const unifiedStyles = {
  // Glass morphism effect
  glass: {
    background: 'rgba(255, 255, 255, 0.1)',
    backdropFilter: 'blur(10px)',
    border: '1px solid rgba(255, 255, 255, 0.2)',
    borderRadius: '0.75rem',
  },
  
  // Holographic effect
  holographic: {
    background: 'linear-gradient(45deg, #667eea 0%, #764ba2 100%)',
    backgroundSize: '200% 200%',
    animation: 'holographic 3s ease infinite',
  },
  
  // Consciousness glow effect
  consciousnessGlow: {
    boxShadow: '0 0 20px rgba(14, 165, 233, 0.3), 0 0 40px rgba(14, 165, 233, 0.2)',
    border: '1px solid rgba(14, 165, 233, 0.3)',
  },
  
  // Quantum shimmer effect
  quantumShimmer: {
    background: 'linear-gradient(45deg, #d946ef 0%, #e879f9 50%, #f0abfc 100%)',
    backgroundSize: '200% 200%',
    animation: 'quantumShimmer 2s ease-in-out infinite',
  },
  
  // Evolution pulse effect
  evolutionPulse: {
    animation: 'evolutionPulse 2s ease-in-out infinite',
  },
  
  // Real-time data update effect
  dataUpdate: {
    animation: 'dataUpdate 0.5s ease-in-out',
  },
} as const;

// ============================================================================
// UNIFIED ANIMATIONS
// ============================================================================

export const unifiedAnimations = {
  // Fade animations
  fadeIn: {
    from: { opacity: 0 },
    to: { opacity: 1 },
    duration: 300,
  },
  fadeOut: {
    from: { opacity: 1 },
    to: { opacity: 0 },
    duration: 300,
  },
  
  // Slide animations
  slideInFromLeft: {
    from: { transform: 'translateX(-100%)', opacity: 0 },
    to: { transform: 'translateX(0)', opacity: 1 },
    duration: 300,
  },
  slideInFromRight: {
    from: { transform: 'translateX(100%)', opacity: 0 },
    to: { transform: 'translateX(0)', opacity: 1 },
    duration: 300,
  },
  slideInFromTop: {
    from: { transform: 'translateY(-100%)', opacity: 0 },
    to: { transform: 'translateY(0)', opacity: 1 },
    duration: 300,
  },
  slideInFromBottom: {
    from: { transform: 'translateY(100%)', opacity: 0 },
    to: { transform: 'translateY(0)', opacity: 1 },
    duration: 300,
  },
  
  // Scale animations
  scaleIn: {
    from: { transform: 'scale(0)', opacity: 0 },
    to: { transform: 'scale(1)', opacity: 1 },
    duration: 300,
  },
  scaleOut: {
    from: { transform: 'scale(1)', opacity: 1 },
    to: { transform: 'scale(0)', opacity: 0 },
    duration: 300,
  },
  
  // Consciousness-specific animations
  consciousnessPulse: {
    from: { transform: 'scale(1)', opacity: 1 },
    to: { transform: 'scale(1.05)', opacity: 0.8 },
    duration: 1000,
    repeat: 'infinite',
    direction: 'alternate',
  },
  
  quantumShimmer: {
    from: { backgroundPosition: '0% 50%' },
    to: { backgroundPosition: '100% 50%' },
    duration: 2000,
    repeat: 'infinite',
  },
  
  evolutionGlow: {
    from: { boxShadow: '0 0 10px rgba(34, 197, 94, 0.3)' },
    to: { boxShadow: '0 0 30px rgba(34, 197, 94, 0.6)' },
    duration: 1500,
    repeat: 'infinite',
    direction: 'alternate',
  },
} as const;

// ============================================================================
// UNIFIED THEME CONFIGURATION
// ============================================================================

export const unifiedTheme = {
  light: {
    colors: {
      background: '#ffffff',
      foreground: '#0f172a',
      card: '#ffffff',
      cardForeground: '#0f172a',
      popover: '#ffffff',
      popoverForeground: '#0f172a',
      primary: designTokens.colors.primary[600],
      primaryForeground: '#ffffff',
      secondary: designTokens.colors.secondary[100],
      secondaryForeground: designTokens.colors.secondary[900],
      muted: designTokens.colors.secondary[100],
      mutedForeground: designTokens.colors.secondary[500],
      accent: designTokens.colors.accent[600],
      accentForeground: '#ffffff',
      destructive: designTokens.colors.error[600],
      destructiveForeground: '#ffffff',
      border: designTokens.colors.secondary[200],
      input: designTokens.colors.secondary[200],
      ring: designTokens.colors.primary[600],
    },
  },
  dark: {
    colors: {
      background: '#0f172a',
      foreground: '#f8fafc',
      card: '#1e293b',
      cardForeground: '#f8fafc',
      popover: '#1e293b',
      popoverForeground: '#f8fafc',
      primary: designTokens.colors.primary[500],
      primaryForeground: '#0f172a',
      secondary: designTokens.colors.secondary[800],
      secondaryForeground: '#f8fafc',
      muted: designTokens.colors.secondary[800],
      mutedForeground: designTokens.colors.secondary[400],
      accent: designTokens.colors.accent[500],
      accentForeground: '#0f172a',
      destructive: designTokens.colors.error[500],
      destructiveForeground: '#0f172a',
      border: designTokens.colors.secondary[700],
      input: designTokens.colors.secondary[700],
      ring: designTokens.colors.primary[500],
    },
  },
} as const;

// ============================================================================
// EXPORT TYPES
// ============================================================================

export type DesignTokens = typeof designTokens;
export type ComponentCategories = typeof componentCategories;
export type UnifiedStyles = typeof unifiedStyles;
export type UnifiedAnimations = typeof unifiedAnimations;
export type UnifiedTheme = typeof unifiedTheme;
