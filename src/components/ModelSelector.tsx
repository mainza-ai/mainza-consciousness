import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Brain, Cpu, Loader2, AlertCircle } from 'lucide-react';
import { GlassCard } from '@/components/ui/glass-card';

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
}

export const ModelSelector: React.FC<ModelSelectorProps> = ({
  onModelChange,
  selectedModel,
  className = ''
}) => {
  const [models, setModels] = useState<OllamaModel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchModels();
  }, []);

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
        <div className="mt-2 text-xs text-slate-400 flex items-center">
          <Cpu className="w-3 h-3 mr-1" />
          Selected: {getModelDisplayName(selectedModel)}
        </div>
      )}
    </GlassCard>
  );
};
