import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import throttle from 'lodash.throttle';

interface DataTendrilsProps {
  orbRef: React.RefObject<HTMLElement>;
  crystalRefs: { [id: number]: HTMLElement | null };
  activeDocumentIds: number[];
}

export const DataTendrils: React.FC<DataTendrilsProps> = React.memo(({ orbRef, crystalRefs, activeDocumentIds }) => {
  const [lines, setLines] = useState<{ x1: number; y1: number; x2: number; y2: number; key: string }[]>([]);

  useEffect(() => {
    const updateLines = throttle(() => {
      if (!orbRef.current || activeDocumentIds.length === 0) {
        setLines([]);
        return;
      }
      const orbRect = orbRef.current.getBoundingClientRect();
      const orbX = orbRect.left + orbRect.width / 2;
      const orbY = orbRect.top + orbRect.height / 2;
      const newLines: typeof lines = [];
      activeDocumentIds.forEach((id) => {
        const crystal = crystalRefs[id];
        if (crystal) {
          const crystalRect = crystal.getBoundingClientRect();
          const crystalX = crystalRect.left + crystalRect.width / 2;
          const crystalY = crystalRect.top + crystalRect.height / 2;
          newLines.push({ x1: orbX, y1: orbY, x2: crystalX, y2: crystalY, key: `tendril-${id}` });
        }
      });
      setLines(newLines);
    }, 80); // 80ms throttle
    updateLines();
    return () => { updateLines.cancel && updateLines.cancel(); };
  }, [orbRef, crystalRefs, activeDocumentIds]);

  if (lines.length === 0) return null;

  // Get viewport size for SVG
  const width = window.innerWidth;
  const height = window.innerHeight;

  // Helper for Bezier curve path
  const getBezierPath = (x1: number, y1: number, x2: number, y2: number) => {
    const dx = x2 - x1;
    const dy = y2 - y1;
    // Control points: curve out from orb, then curve in to crystal
    const c1x = x1 + dx * 0.25;
    const c1y = y1 + dy * 0.1 - 40;
    const c2x = x1 + dx * 0.75;
    const c2y = y1 + dy * 0.9 + 40;
    return `M${x1},${y1} C${c1x},${c1y} ${c2x},${c2y} ${x2},${y2}`;
  };

  return (
    <svg
      className="pointer-events-none fixed inset-0 z-40"
      width={width}
      height={height}
      style={{ position: 'fixed', left: 0, top: 0, width: '100vw', height: '100vh', pointerEvents: 'none' }}
      aria-label="Animated data tendrils connecting orb and documents"
      role="img"
    >
      <defs>
        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="6" result="coloredBlur" />
          <feMerge>
            <feMergeNode in="coloredBlur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
        <linearGradient id="tendril-gradient" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#22d3ee" />
          <stop offset="100%" stopColor="#a855f7" />
        </linearGradient>
        <linearGradient id="tendril-flow-gradient" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stopColor="#22d3ee" stopOpacity="0.7" />
          <stop offset="50%" stopColor="#a855f7" stopOpacity="0.9">
            <animate attributeName="offset" values="0;1;0" dur="2.2s" repeatCount="indefinite" />
          </stop>
          <stop offset="100%" stopColor="#22d3ee" stopOpacity="0.7" />
        </linearGradient>
      </defs>
      <AnimatePresence>
        {lines.map(({ x1, y1, x2, y2, key }) => (
          <motion.path
            key={key}
            d={getBezierPath(x1, y1, x2, y2)}
            stroke="url(#tendril-flow-gradient)"
            strokeWidth={4}
            filter="url(#glow)"
            fill="none"
            initial={{ opacity: 0, pathLength: 0, scale: 0.95 }}
            animate={{ opacity: 0.85, pathLength: 1, scale: 1 }}
            exit={{ opacity: 0, pathLength: 0, scale: 0.95 }}
            transition={{ duration: 0.7, ease: 'easeInOut' }}
            style={{
              strokeDasharray: 16,
              strokeDashoffset: 0,
              willChange: 'opacity, transform, pathLength',
            }}
          />
        ))}
      </AnimatePresence>
    </svg>
  );
}); 