// Common type definitions to replace 'any' usage
export interface ApiResponse<T = unknown> {
  status: string;
  data?: T;
  message?: string;
  error?: string;
}

export interface GraphNode {
  id: string;
  label: string;
  properties: Record<string, unknown>;
  connections?: number;
  importance?: number;
  context?: string;
}

export interface GraphLink {
  source: string;
  target: string;
  type: string;
  strength?: number;
  context?: string;
}

export interface ConsciousnessData {
  level: number;
  evolution: number;
  emotional_state: string;
  learning_rate: number;
  awareness: number;
  total_interactions: number;
}

export interface MemoryData {
  id: string;
  content: string;
  timestamp: string;
  importance: number;
  context: string;
}

export interface AgentData {
  id: string;
  name: string;
  status: string;
  capabilities: string[];
  performance: Record<string, number>;
}

export interface AnalyticsData {
  timestamp: string;
  metric: string;
  value: number;
  category: string;
}

export interface UserData {
  id: string;
  name: string;
  preferences: Record<string, unknown>;
  interactions: number;
}

export interface SystemHealth {
  status: string;
  uptime: number;
  memory_usage: number;
  cpu_usage: number;
  database_status: string;
}

export interface ConversationMessage {
  id: string;
  content: string;
  timestamp: string;
  sender: string;
  type: 'user' | 'ai';
}

export interface QuantumState {
  amplitude: number;
  phase: number;
  probability: number;
}

export interface NeuralNetworkData {
  layers: number;
  neurons: number[];
  weights: number[][];
  biases: number[];
}

export interface BlockchainData {
  hash: string;
  timestamp: string;
  block_number: number;
  transactions: number;
}

export interface Web3Data {
  address: string;
  balance: string;
  network: string;
  transactions: BlockchainData[];
}

export interface ARVRData {
  position: { x: number; y: number; z: number };
  rotation: { x: number; y: number; z: number };
  scale: { x: number; y: number; z: number };
}

export interface MobileData {
  device: string;
  platform: string;
  version: string;
  capabilities: string[];
}

export interface CollaborationData {
  users: UserData[];
  projects: string[];
  messages: ConversationMessage[];
  shared_resources: string[];
}

export interface PredictiveData {
  prediction: number;
  confidence: number;
  factors: string[];
  timeframe: string;
}

export interface LearningData {
  algorithm: string;
  accuracy: number;
  loss: number;
  epochs: number;
  dataset_size: number;
}

export interface QuantumConsciousnessData {
  superposition: QuantumState[];
  entanglement: string[];
  coherence: number;
  decoherence: number;
}

export interface ConsciousnessInsight {
  type: string;
  description: string;
  confidence: number;
  timestamp: string;
  source: string;
}

export interface MarketplaceItem {
  id: string;
  name: string;
  description: string;
  price: number;
  category: string;
  seller: string;
}

export interface SynchronizationData {
  nodes: string[];
  connections: GraphLink[];
  last_sync: string;
  conflicts: string[];
}

export interface RealTimeData {
  timestamp: string;
  event_type: string;
  data: Record<string, unknown>;
  source: string;
}

export interface TensorFlowData {
  model: string;
  input_shape: number[];
  output_shape: number[];
  parameters: number;
  accuracy: number;
}

export interface NeedsData {
  category: string;
  priority: number;
  description: string;
  status: string;
  dependencies: string[];
}

export interface AdvancedNeedsData extends NeedsData {
  analytics: AnalyticsData[];
  trends: PredictiveData[];
  recommendations: string[];
}

export interface UIComponentProps {
  className?: string;
  children?: React.ReactNode;
  onClick?: () => void;
  onMouseEnter?: () => void;
  onMouseLeave?: () => void;
}

export interface FormData {
  [key: string]: string | number | boolean | File | null;
}

export interface NavigationItem {
  label: string;
  href: string;
  icon?: string;
  children?: NavigationItem[];
}

export interface SidebarItem {
  id: string;
  label: string;
  icon: string;
  href?: string;
  children?: SidebarItem[];
}

export interface CommandItem {
  id: string;
  label: string;
  description: string;
  icon?: string;
  action: () => void;
}

export interface DataTendrilProps {
  data: Record<string, unknown>;
  onUpdate: (data: Record<string, unknown>) => void;
}

export interface FormFieldProps {
  name: string;
  label: string;
  type: string;
  required?: boolean;
  placeholder?: string;
  validation?: (value: unknown) => string | null;
}

export interface ToggleProps {
  pressed: boolean;
  onPressedChange: (pressed: boolean) => void;
  children: React.ReactNode;
}

export interface UtilityFunction {
  (...args: unknown[]): unknown;
}

export interface BuildInfo {
  buildDate: string;
  gitCommit: string;
  cacheBust: string;
  buildTimestamp: number;
}

export interface WindowWithBuildInfo extends Window {
  BUILD_INFO?: BuildInfo;
}
