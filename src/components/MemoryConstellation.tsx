
import { useEffect, useState } from 'react';

interface MemoryNode {
  id: number;
  x: number;
  y: number;
  type: 'memory' | 'concept' | 'entity';
  active: boolean;
}

export const MemoryConstellation = () => {
  const [nodes, setNodes] = useState<MemoryNode[]>([]);

  useEffect(() => {
    // Generate constellation nodes
    const generateNodes = () => {
      const newNodes: MemoryNode[] = [];
      for (let i = 0; i < 20; i++) {
        newNodes.push({
          id: i,
          x: Math.random() * 100,
          y: Math.random() * 100,
          type: ['memory', 'concept', 'entity'][Math.floor(Math.random() * 3)] as 'memory' | 'concept' | 'entity',
          active: Math.random() > 0.7,
        });
      }
      setNodes(newNodes);
    };

    generateNodes();

    // Periodically activate/deactivate nodes
    const interval = setInterval(() => {
      setNodes(prev => prev.map(node => ({
        ...node,
        active: Math.random() > 0.8,
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
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {/* Connection Lines */}
      <svg className="absolute inset-0 w-full h-full">
        {nodes.map((node, i) => {
          const nextNode = nodes[(i + 1) % nodes.length];
          if (!node.active || !nextNode.active) return null;
          
          return (
            <line
              key={`connection-${i}`}
              x1={`${node.x}%`}
              y1={`${node.y}%`}
              x2={`${nextNode.x}%`}
              y2={`${nextNode.y}%`}
              stroke="rgba(34, 211, 238, 0.2)"
              strokeWidth="1"
              className="animate-pulse"
            />
          );
        })}
      </svg>

      {/* Memory Nodes */}
      {nodes.map((node) => (
        <div
          key={node.id}
          className={`absolute w-2 h-2 rounded-full transition-all duration-1000 transform -translate-x-1/2 -translate-y-1/2 ${getNodeColor(node.type, node.active)} ${
            node.active ? 'shadow-lg' : ''
          }`}
          style={{
            left: `${node.x}%`,
            top: `${node.y}%`,
            boxShadow: node.active ? `0 0 10px ${node.type === 'memory' ? '#22d3ee' : node.type === 'concept' ? '#a855f7' : '#fbbf24'}` : 'none',
          }}
        />
      ))}
    </div>
  );
};
