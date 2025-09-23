import { useEffect, useState, useCallback } from 'react';
import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface MemoryNode {
  id: string;
  x: number;
  y: number;
  type: 'memory' | 'concept' | 'entity';
  active: boolean;
  name?: string;
  lastAccessed?: number;
  importance?: number;
}

interface MemoryData {
  memory_id: string;
  text: string;
  created_at?: number;
  last_accessed?: number;
}

interface ConceptData {
  concept_id: string;
  name: string;
  created_at?: number;
  last_accessed?: number;
}

interface EntityData {
  entity_id: string;
  name: string;
  created_at?: number;
  last_accessed?: number;
}

interface MemoryConstellationProps {
  highlightedConcepts?: string[];
}

export const MemoryConstellation = React.memo(({ highlightedConcepts = [] }: MemoryConstellationProps) => {
  const [nodes, setNodes] = useState<MemoryNode[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [center, setCenter] = useState<{ x: number; y: number }>({ x: 50, y: 50 });

  // Fetch real data from Neo4j APIs
  const fetchMemoryData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch real data from backend APIs
      const [memoriesResponse, conceptsResponse, entitiesResponse] = await Promise.all([
        fetch('/memories/').then(async r => r.ok ? r.json() : []),
        fetch('/concepts/').then(async r => r.ok ? r.json() : []),
        fetch('/entities/').then(async r => r.ok ? r.json() : [])
      ]);

      const memories: MemoryData[] = memoriesResponse || [];
      const concepts: ConceptData[] = conceptsResponse || [];
      const entities: EntityData[] = entitiesResponse || [];

      // Transform real data into constellation nodes
      const newNodes: MemoryNode[] = [];
      
      // Create memory nodes
      memories.forEach((memory, index) => {
        const angle = (2 * Math.PI * index) / Math.max(memories.length, 1);
        const r = 15 + (memory.last_accessed ? Math.min(10, (Date.now() - memory.last_accessed) / (1000 * 60 * 60 * 24)) : 5);
        newNodes.push({
          id: memory.memory_id,
          x: 35 + r * Math.cos(angle),
          y: 55 + r * Math.sin(angle),
          type: 'memory',
          active: memory.last_accessed ? (Date.now() - memory.last_accessed) < (1000 * 60 * 60 * 24) : false,
          name: memory.text?.substring(0, 20) + '...',
          lastAccessed: memory.last_accessed,
          importance: memory.text?.length || 0
        });
      });

      // Create concept nodes
      concepts.forEach((concept, index) => {
        const angle = (2 * Math.PI * index) / Math.max(concepts.length, 1);
        const r = 12 + (concept.last_accessed ? Math.min(8, (Date.now() - concept.last_accessed) / (1000 * 60 * 60 * 24)) : 3);
        newNodes.push({
          id: concept.concept_id,
          x: 65 + r * Math.cos(angle),
          y: 45 + r * Math.sin(angle),
          type: 'concept',
          active: concept.last_accessed ? (Date.now() - concept.last_accessed) < (1000 * 60 * 60 * 24) : false,
          name: concept.name,
          lastAccessed: concept.last_accessed,
          importance: concept.name?.length || 0
        });
      });

      // Create entity nodes
      entities.forEach((entity, index) => {
        const angle = (2 * Math.PI * index) / Math.max(entities.length, 1);
        const r = 10 + (entity.last_accessed ? Math.min(6, (Date.now() - entity.last_accessed) / (1000 * 60 * 60 * 24)) : 2);
        newNodes.push({
          id: entity.entity_id,
          x: 50 + r * Math.cos(angle),
          y: 70 + r * Math.sin(angle),
          type: 'entity',
          active: entity.last_accessed ? (Date.now() - entity.last_accessed) < (1000 * 60 * 60 * 24) : false,
          name: entity.name,
          lastAccessed: entity.last_accessed,
          importance: entity.name?.length || 0
        });
      });

      setNodes(newNodes);
    } catch (err) {
      console.error('Failed to fetch memory data:', err);
      setError('Failed to load memory constellation data');
      
      // Fallback to minimal visualization
      setNodes([
        { id: 'fallback-1', x: 50, y: 50, type: 'memory', active: true, name: 'Memory System' }
      ]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchMemoryData();

    // Refresh data every 30 seconds
    const interval = setInterval(fetchMemoryData, 30000);

    return () => clearInterval(interval);
  }, [fetchMemoryData]);

  const getNodeColor = (type: string, active: boolean) => {
    const baseColors = {
      memory: 'bg-cyan-400',
      concept: 'bg-purple-400',
      entity: 'bg-yellow-400',
    };
    return `${baseColors[type as keyof typeof baseColors]} ${active ? 'opacity-80' : 'opacity-20'}`;
  };

  // Show loading state
  if (loading) {
    return (
      <div className="absolute inset-0 overflow-hidden pointer-events-none flex items-center justify-center" aria-label="Loading memory constellation" role="img">
        <div className="text-cyan-400 text-sm opacity-50">Loading memory constellation...</div>
      </div>
    );
  }

  // Show error state
  if (error) {
    return (
      <div className="absolute inset-0 overflow-hidden pointer-events-none flex items-center justify-center" aria-label="Memory constellation error" role="img">
        <div className="text-red-400 text-sm opacity-50">{error}</div>
      </div>
    );
  }

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none" aria-label="Memory constellation of Mainza's knowledge graph" role="img">
      {/* Connection Lines */}
      <svg className="absolute inset-0 w-full h-full">
        <AnimatePresence>
          {nodes.map((node, i) => {
            const nextNode = nodes[(i + 1) % nodes.length];
            if (!node.active || !nextNode.active) return null;
            return (
              <motion.line
                key={`connection-${i}`}
                x1={`${node.x}%`}
                y1={`${node.y}%`}
                x2={`${nextNode.x}%`}
                y2={`${nextNode.y}%`}
                stroke="rgba(34, 211, 238, 0.18)"
                strokeWidth="1.5"
                initial={{ opacity: 0 }}
                animate={{ opacity: [0, 0.7, 0.18, 0.7, 0.18] }}
                exit={{ opacity: 0 }}
                transition={{ duration: 2.2, repeat: Infinity, repeatType: 'mirror', delay: i * 0.07 }}
                style={{ filter: 'drop-shadow(0 0 6px #22d3ee88)', willChange: 'opacity, filter' }}
              />
            );
          })}
        </AnimatePresence>
      </svg>
      {/* Memory Nodes */}
      <AnimatePresence>
        {nodes.map((node) => {
          const isHighlighted = highlightedConcepts.includes(node.type) || highlightedConcepts.includes(String(node.id));
          return (
            <motion.div
              key={node.id}
              className={`absolute w-2 h-2 rounded-full -translate-x-1/2 -translate-y-1/2 ${getNodeColor(node.type, node.active)} ${isHighlighted ? 'ring-4 ring-yellow-300 animate-bounce' : ''}`}
              style={{
                left: `${node.x}%`,
                top: `${node.y}%`,
                boxShadow: node.active ? `0 0 16px 4px ${node.type === 'memory' ? '#22d3ee' : node.type === 'concept' ? '#a855f7' : '#fbbf24'}` : 'none',
                zIndex: node.active ? 2 : 1,
                willChange: 'opacity, boxShadow, transform',
              }}
              initial={{ opacity: 0, scale: 0.7 }}
              animate={{
                opacity: node.active ? 1 : 0.2,
                scale: node.active ? [1, 1.25, 1] : 0.7,
                boxShadow: node.active
                  ? [
                      `0 0 16px 4px ${node.type === 'memory' ? '#22d3ee' : node.type === 'concept' ? '#a855f7' : '#fbbf24'}`,
                      `0 0 32px 8px ${node.type === 'memory' ? '#22d3ee' : node.type === 'concept' ? '#a855f7' : '#fbbf24'}`,
                      `0 0 16px 4px ${node.type === 'memory' ? '#22d3ee' : node.type === 'concept' ? '#a855f7' : '#fbbf24'}`
                    ]
                  : 'none',
              }}
              exit={{ opacity: 0, scale: 0.7 }}
              transition={{
                duration: 1.2,
                scale: { duration: 1.2, repeat: Infinity, repeatType: 'mirror' },
                boxShadow: { duration: 1.2, repeat: Infinity, repeatType: 'mirror' },
              }}
              aria-label={isHighlighted ? `Mainza is curious about this ${node.type}: ${node.name}` : `${node.type}: ${node.name}`}
              title={node.name}
              tabIndex={0}
              role="presentation"
            />
          );
        })}
      </AnimatePresence>
    </div>
  );
});
