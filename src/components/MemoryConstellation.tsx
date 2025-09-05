import { useEffect, useState } from 'react';
import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface MemoryNode {
  id: number;
  x: number;
  y: number;
  type: 'memory' | 'concept' | 'entity';
  active: boolean;
}

interface MemoryConstellationProps {
  highlightedConcepts?: string[];
}

export const MemoryConstellation = React.memo(({ highlightedConcepts = [] }: MemoryConstellationProps) => {
  const [nodes, setNodes] = useState<MemoryNode[]>([]);
  const [center, setCenter] = useState<{ x: number; y: number }>({ x: 50, y: 50 });

  useEffect(() => {
    // Generate constellation nodes
    const generateNodes = () => {
      // Cluster nodes in 3 groups (memory, concept, entity)
      const groups = [
        { type: 'memory', cx: 35, cy: 55, color: '#22d3ee' },
        { type: 'concept', cx: 65, cy: 45, color: '#a855f7' },
        { type: 'entity', cx: 50, cy: 70, color: '#fbbf24' },
      ];
      const newNodes: MemoryNode[] = [];
      let id = 0;
      groups.forEach((group, gi) => {
        for (let i = 0; i < 7; i++) {
          const angle = (2 * Math.PI * i) / 7 + gi;
          const r = 12 + Math.random() * 6;
          newNodes.push({
            id: id++, 
            x: group.cx + r * Math.cos(angle),
            y: group.cy + r * Math.sin(angle),
            type: group.type as 'memory' | 'concept' | 'entity',
            active: Math.random() > 0.7,
          });
        }
      });
      setNodes(newNodes);
    };

    generateNodes();

    // Periodically activate/deactivate nodes
    const interval = setInterval(() => {
      setNodes(prev => prev.map(node => ({
        ...node,
        active: Math.random() > 0.8,
        // Animate cluster drift
        x: node.x + (Math.random() - 0.5) * 1.2,
        y: node.y + (Math.random() - 0.5) * 1.2,
      })));
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  const getNodeColor = (type: string, active: boolean) => {
    const baseColors = {
      memory: 'bg-cyan-400',
      concept: 'bg-purple-400',
      entity: 'bg-yellow-400',
    };
    return `${baseColors[type as keyof typeof baseColors]} ${active ? 'opacity-80' : 'opacity-20'}`;
  };

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
              aria-label={isHighlighted ? `Mainza is curious about this ${node.type}` : node.type}
              tabIndex={0}
              role="presentation"
            />
          );
        })}
      </AnimatePresence>
    </div>
  );
});
