import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Brain, Cpu, Loader2, AlertCircle, CheckCircle, XCircle, Play } from 'lucide-react';
import { GlassCard } from '@/components/ui/glass-card';
import { Button } from '@/components/ui/button';

interface OllamaModel {
  name: string;
  size: number;
  modified_at: string;
  digest: string;
}

interface ModelSelectorProps {
  onModelChange: (model: string) => void;
  selectedModel: string;
  className?: string;
  onModelLoad?: (model: string) => Promise<boolean>;
}

export const ModelSelector: React.FC<ModelSelectorProps> = ({
  onModelChange,
  selectedModel,
  className = '',
  onModelLoad
}) => {
  const [models, setModels] = useState<OllamaModel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modelLoading, setModelLoading] = useState(false);
  const [modelLoadStatus, setModelLoadStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [loadError, setLoadError] = useState<string | null>(null);
  const [memoryUsage, setMemoryUsage] = useState<number | null>(null);

  useEffect(() => {
    fetchModels();
    fetchMemoryUsage();
  }, []);

  const fetchMemoryUsage = async () => {
    try {
      const response = await fetch('/telemetry/system-health');
      if (response.ok) {
        const data = await response.json();
        setMemoryUsage(data.memory_percent);
      }
    } catch (err) {
      console.warn('Failed to fetch memory usage:', err);
    }
  };

  const fetchModels = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch('/ollama/models');

      if (response.ok) {
        const data = await response.json();
        // Handle new error format from backend
        if (data.error) {
          setError(data.details || data.error || 'Failed to fetch models');
          setModels([]); // Clear models on error
        } else {
          setModels(data.models || []);
        }
      } else {
        // Try to get error message from response
        try {
          const errorData = await response.json();
          setError(errorData.details || errorData.error || `HTTP ${response.status}`);
        } catch {
          setError(`HTTP ${response.status}: ${response.statusText}`);
        }
        setModels([]); // Clear models on error
      }
    } catch (err) {
      console.error('Error fetching Ollama models:', err);
      setError('Network error: Could not connect to server');
      // Add minimal fallback models with clear indication they're placeholder
      setModels([
        { name: 'gpt-oss:20b', size: 13780173839, modified_at: '', digest: '' },
        { name: 'llama3.2:1b', size: 1321098329, modified_at: '', digest: '' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const formatModelSize = (bytes: number): string => {
    if (bytes === 0) return 'Unknown';
    const gb = bytes / (1024 * 1024 * 1024);
    return `${gb.toFixed(1)} GB`;
  };

  const getModelDisplayName = (modelName: string): string => {
    // Clean up common model names
    if (modelName === 'default') return 'Default Model';
    if (modelName.includes(':')) {
      const [base, tag] = modelName.split(':');
      return `${base.charAt(0).toUpperCase() + base.slice(1)} (${tag})`;
    }
    return modelName.charAt(0).toUpperCase() + modelName.slice(1);
  };

  const handleModelLoad = async () => {
    if (!onModelLoad || !selectedModel) return;
    
    setModelLoading(true);
    setModelLoadStatus('loading');
    setLoadError(null);
    
    try {
      const success = await onModelLoad(selectedModel);
      if (success) {
        setModelLoadStatus('success');
        // Reset status after 3 seconds
        setTimeout(() => setModelLoadStatus('idle'), 3000);
      } else {
        setModelLoadStatus('error');
        setLoadError('Failed to load model');
      }
    } catch (err) {
      setModelLoadStatus('error');
      setLoadError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setModelLoading(false);
    }
  };

  const getModelSizeGB = (bytes: number): number => {
    return bytes / (1024 * 1024 * 1024);
  };

  const isLargeModel = (bytes: number): boolean => {
    return getModelSizeGB(bytes) > 10; // Consider models > 10GB as large
  };

  return (
    <GlassCard className={`p-3 ${className}`}>
      <div className="flex items-center space-x-2 mb-2">
        <Brain className="w-4 h-4 text-cyan-400" />
        <h3 className="text-xs font-semibold text-slate-200">LLM Model</h3>
      </div>

      <div className="relative">
        {loading ? (
          <div className="flex items-center justify-center py-2">
            <Loader2 className="w-4 h-4 animate-spin text-cyan-400 mr-2" />
            <span className="text-xs text-slate-400">Loading models...</span>
          </div>
        ) : error ? (
          <div className="flex items-center py-2 text-orange-400">
            <AlertCircle className="w-4 h-4 mr-1" />
            <span className="text-xs">{error}</span>
          </div>
        ) : (
          <select
            value={selectedModel}
            onChange={(e) => onModelChange(e.target.value)}
            className="w-full bg-slate-700/50 border border-slate-600 rounded px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:ring-1 focus:ring-cyan-400/50 transition-colors"
          >
            {models.map((model) => (
              <option key={model.name} value={model.name}>
                {getModelDisplayName(model.name)} ({formatModelSize(model.size)})
              </option>
            ))}
          </select>
        )}
      </div>

      {selectedModel && !loading && (
        <div className="mt-2 space-y-2">
          <div className="text-xs text-slate-400 flex items-center">
            <Cpu className="w-3 h-3 mr-1" />
            Selected: {getModelDisplayName(selectedModel)}
          </div>
          
          {onModelLoad && (
            <div className="space-y-2">
              <Button
                onClick={handleModelLoad}
                disabled={modelLoading || !selectedModel}
                size="sm"
                className="w-full h-7 text-xs bg-cyan-600/20 hover:bg-cyan-600/30 border border-cyan-500/30 hover:border-cyan-500/50 text-cyan-300 hover:text-cyan-200 transition-all duration-200"
              >
                {modelLoading ? (
                  <>
                    <Loader2 className="w-3 h-3 mr-1 animate-spin" />
                    Loading Model...
                  </>
                ) : modelLoadStatus === 'success' ? (
                  <>
                    <CheckCircle className="w-3 h-3 mr-1 text-green-400" />
                    Model Loaded
                  </>
                ) : modelLoadStatus === 'error' ? (
                  <>
                    <XCircle className="w-3 h-3 mr-1 text-red-400" />
                    Load Failed
                  </>
                ) : (
                  <>
                    <Play className="w-3 h-3 mr-1" />
                    Load Model
                  </>
                )}
              </Button>
              
              {loadError && (
                <div className="text-xs text-red-400 flex items-center">
                  <AlertCircle className="w-3 h-3 mr-1" />
                  {loadError}
                </div>
              )}
              
              {selectedModel && models.find(m => m.name === selectedModel) && (
                <div className="text-xs text-slate-500 space-y-1">
                  <div>
                    {(() => {
                      const model = models.find(m => m.name === selectedModel);
                      if (!model) return '';
                      const sizeGB = getModelSizeGB(model.size);
                      const isLarge = isLargeModel(model.size);
                      return `Size: ${sizeGB.toFixed(1)}GB${isLarge ? ' (Large - may take time)' : ''}`;
                    })()}
                  </div>
                  {memoryUsage !== null && (
                    <div className="flex items-center justify-between">
                      <span>Memory Usage:</span>
                      <span className={`font-medium ${
                        memoryUsage > 90 ? 'text-red-400' : 
                        memoryUsage > 75 ? 'text-yellow-400' : 
                        'text-green-400'
                      }`}>
                        {memoryUsage.toFixed(1)}%
                      </span>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </GlassCard>
  );
};
