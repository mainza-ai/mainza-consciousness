import React from 'react';

interface HolographicPaneProps {
  title?: string;
  children: React.ReactNode;
  onClose?: () => void;
  actions?: React.ReactNode;
  className?: string;
  style?: React.CSSProperties;
}

export const HolographicPane: React.FC<HolographicPaneProps> = ({
  title,
  children,
  onClose,
  actions,
  className = '',
  style = {},
}) => {
  return (
    <div
      className={
        `relative p-8 rounded-3xl shadow-2xl border border-cyan-400/30 bg-gradient-to-br from-white/10 via-cyan-400/5 to-purple-400/10 backdrop-blur-lg overflow-hidden ${className}`
      }
      style={{
        ...style,
        boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.37), 0 0 24px 4px rgba(34,211,238,0.15)',
        border: '1.5px solid rgba(34,211,238,0.25)',
        transition: 'transform 0.3s cubic-bezier(.4,2,.6,1), box-shadow 0.3s',
        transform: 'perspective(1200px) rotateX(2deg) scale(1.01)',
      }}
    >
      {/* Animated border glow */}
      <div className="pointer-events-none absolute inset-0 rounded-3xl border-2 border-cyan-400/30 animate-holo-glow" style={{zIndex:1}} />
      {/* Close button */}
      {onClose && (
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-cyan-300 hover:text-cyan-100 text-2xl font-bold z-10 bg-black/10 rounded-full w-8 h-8 flex items-center justify-center backdrop-blur-sm"
          aria-label="Close"
        >
          &times;
        </button>
      )}
      {/* Title */}
      {title && (
        <h2 className="text-xl font-bold mb-4 text-cyan-200 drop-shadow-lg z-10 relative">{title}</h2>
      )}
      {/* Content */}
      <div className="relative z-10">{children}</div>
      {/* Actions */}
      {actions && (
        <div className="mt-6 flex justify-end gap-2 z-10 relative">{actions}</div>
      )}
      {/* CSS for animated border glow */}
      <style>{`
        .animate-holo-glow {
          box-shadow: 0 0 32px 8px rgba(34,211,238,0.25), 0 0 64px 16px rgba(168,85,247,0.15);
          animation: holo-glow 2.5s ease-in-out infinite alternate;
        }
        @keyframes holo-glow {
          0% {
            box-shadow: 0 0 32px 8px rgba(34,211,238,0.25), 0 0 64px 16px rgba(168,85,247,0.15);
          }
          100% {
            box-shadow: 0 0 48px 16px rgba(34,211,238,0.35), 0 0 96px 32px rgba(168,85,247,0.25);
          }
        }
      `}</style>
    </div>
  );
};

interface NeedsCuriosityPaneProps {
  needs: string[];
  onRequestHelp?: (need: string) => void;
}

export const NeedsCuriosityPane: React.FC<NeedsCuriosityPaneProps> = ({ needs, onRequestHelp }) => {
  if (!needs || needs.length === 0) return null;
  return (
    <HolographicPane title="Mainza's Needs & Curiosity" className="w-72">
      <div className="flex flex-wrap gap-2" role="list" aria-label="Mainza's needs and curiosity">
        {needs.map((need, i) => {
          const isNeed = need.toLowerCase().includes('need');
          const isCuriosity = need.toLowerCase().includes('curiosity');
          let badgeClass = 'bg-cyan-700/40 border-cyan-400/30';
          let anim = '';
          if (isNeed) {
            badgeClass = 'bg-red-500/30 border-red-400/40 text-red-200';
            anim = 'animate-badge-pulse';
          } else if (isCuriosity) {
            badgeClass = 'bg-yellow-400/20 border-yellow-300/40 text-yellow-200';
            anim = 'animate-badge-shimmer';
          }
          return (
            <span
              key={i}
              className={`px-3 py-1 rounded-xl border text-xs font-semibold shadow-md ${badgeClass} ${anim}`}
              tabIndex={0}
              role="listitem"
              aria-label={need}
            >
              {need}
              {onRequestHelp && (
                <button
                  className="ml-2 px-2 py-1 rounded-lg bg-cyan-800/40 text-cyan-100 hover:bg-cyan-600/60 focus:outline-none focus:ring-2 focus:ring-cyan-400 text-xs font-bold transition"
                  onClick={() => onRequestHelp(need)}
                  aria-label={`Help Mainza with ${need}`}
                  tabIndex={0}
                >
                  Help Mainza
                </button>
              )}
            </span>
          );
        })}
      </div>
      <style>{`
        @keyframes badge-pulse {
          0% { box-shadow: 0 0 0 0 #ef444455; }
          70% { box-shadow: 0 0 12px 8px #ef444422; }
          100% { box-shadow: 0 0 0 0 #ef444400; }
        }
        .animate-badge-pulse {
          animation: badge-pulse 1.2s infinite;
        }
        @keyframes badge-shimmer {
          0% { background-position: 0% 50%; }
          100% { background-position: 100% 50%; }
        }
        .animate-badge-shimmer {
          background: linear-gradient(90deg, #fde68a33 0%, #f472b633 50%, #a78bfa33 100%);
          background-size: 200% 100%;
          animation: badge-shimmer 2.2s linear infinite;
        }
      `}</style>
    </HolographicPane>
  );
}; 