// Layout constants for z-index management and UI layering
export const Z_LAYERS = {
  BACKGROUND: 0,
  OVERLAY_LINES: 1,
  CONTENT: 10,
  MODAL: 50,
  CRITICAL_ALERTS: 100,
  TOOLTIP: 200,
  DROPDOWN: 300,
  STICKY: 400,
  FIXED: 500,
  MAXIMUM: 9999
} as const;

// Animation durations for consistent timing
export const ANIMATION_DURATION = {
  FAST: 150,
  NORMAL: 300,
  SLOW: 500,
  VERY_SLOW: 1000
} as const;

// Breakpoints for responsive design
export const BREAKPOINTS = {
  MOBILE: 640,
  TABLET: 768,
  DESKTOP: 1024,
  LARGE: 1280,
  XLARGE: 1536
} as const;

// Spacing constants
export const SPACING = {
  XS: '0.25rem',
  SM: '0.5rem',
  MD: '1rem',
  LG: '1.5rem',
  XL: '2rem',
  XXL: '3rem'
} as const;

// Color opacity levels
export const OPACITY = {
  LIGHT: 0.1,
  MEDIUM: 0.3,
  STRONG: 0.6,
  OPAQUE: 0.9
} as const;

// Component sizing
export const SIZES = {
  BUTTON_HEIGHT: '2.5rem',
  INPUT_HEIGHT: '2.5rem',
  CARD_PADDING: '1.5rem',
  MODAL_WIDTH: '32rem',
  SIDEBAR_WIDTH: '16rem'
} as const;

// Typography scale
export const TYPOGRAPHY = {
  FONT_SIZES: {
    XS: '0.75rem',
    SM: '0.875rem',
    BASE: '1rem',
    LG: '1.125rem',
    XL: '1.25rem',
    XXL: '1.5rem',
    XXXL: '2rem'
  },
  LINE_HEIGHTS: {
    TIGHT: 1.2,
    NORMAL: 1.5,
    RELAXED: 1.75
  },
  FONT_WEIGHTS: {
    LIGHT: 300,
    NORMAL: 400,
    MEDIUM: 500,
    SEMIBOLD: 600,
    BOLD: 700
  }
} as const;

// Shadow presets
export const SHADOWS = {
  SM: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
  MD: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
  LG: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
  XL: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
  GLOW: '0 0 20px rgb(59 130 246 / 0.5)'
} as const;

// Border radius presets
export const BORDER_RADIUS = {
  NONE: '0',
  SM: '0.125rem',
  MD: '0.375rem',
  LG: '0.5rem',
  XL: '0.75rem',
  FULL: '9999px'
} as const;

// Transition presets
export const TRANSITIONS = {
  FAST: 'all 150ms ease-in-out',
  NORMAL: 'all 300ms ease-in-out',
  SLOW: 'all 500ms ease-in-out',
  BOUNCE: 'all 300ms cubic-bezier(0.68, -0.55, 0.265, 1.55)',
  EASE_OUT: 'all 300ms cubic-bezier(0.25, 0.46, 0.45, 0.94)'
} as const;

// Grid system
export const GRID = {
  COLUMNS: 12,
  GUTTER: '1rem',
  CONTAINER_MAX_WIDTH: '1200px',
  BREAKPOINTS: {
    SM: '640px',
    MD: '768px',
    LG: '1024px',
    XL: '1280px'
  }
} as const;

// Component states
export const STATES = {
  IDLE: 'idle',
  LOADING: 'loading',
  SUCCESS: 'success',
  ERROR: 'error',
  DISABLED: 'disabled',
  ACTIVE: 'active',
  HOVER: 'hover',
  FOCUS: 'focus'
} as const;

// API endpoints
export const API_ENDPOINTS = {
  BASE_URL: process.env.NODE_ENV === 'production' ? '/api' : 'http://localhost:8000/api',
  CONSCIOUSNESS: '/consciousness',
  AGENTS: '/agents',
  MEMORY: '/memory',
  INSIGHTS: '/insights',
  HEALTH: '/health'
} as const;

// Local storage keys
export const STORAGE_KEYS = {
  CONVERSATION: 'mainza-conversation',
  SETTINGS: 'mainza-settings',
  PREFERENCES: 'mainza-preferences',
  THEME: 'mainza-theme',
  MODEL: 'mainza-model'
} as const;

// Event types for custom events
export const EVENTS = {
  CONSCIOUSNESS_UPDATE: 'consciousness-update',
  AGENT_ACTIVITY: 'agent-activity',
  MEMORY_UPDATE: 'memory-update',
  ERROR_OCCURRED: 'error-occurred',
  SUCCESS_MESSAGE: 'success-message'
} as const;

// Default values
export const DEFAULTS = {
  CONSCIOUSNESS_LEVEL: 0.7,
  EMOTIONAL_STATE: 'curious',
  EVOLUTION_LEVEL: 1,
  ACTIVE_AGENT: 'none',
  MODE: 'idle',
  THEME: 'dark',
  LANGUAGE: 'en',
  MODEL: 'llama3'
} as const;

// Validation rules
export const VALIDATION = {
  MIN_CONSCIOUSNESS_LEVEL: 0,
  MAX_CONSCIOUSNESS_LEVEL: 1,
  MIN_EVOLUTION_LEVEL: 1,
  MAX_EVOLUTION_LEVEL: 5,
  MAX_MESSAGE_LENGTH: 1000,
  MAX_NEEDS_COUNT: 10
} as const;

// Performance thresholds
export const PERFORMANCE = {
  MAX_RENDER_TIME: 16, // 60fps
  MAX_API_RESPONSE_TIME: 5000, // 5 seconds
  MAX_MEMORY_USAGE: 100 * 1024 * 1024, // 100MB
  MAX_STORAGE_SIZE: 10 * 1024 * 1024 // 10MB
} as const;