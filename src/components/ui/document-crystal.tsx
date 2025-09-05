import React, { forwardRef } from 'react';
import { FileText, File, FileType2 } from 'lucide-react';

interface DocumentCrystalProps {
  name: string;
  type: string;
  active?: boolean;
  className?: string;
}

const iconMap: Record<string, React.ReactNode> = {
  pdf: <FileText className="w-5 h-5 text-red-400 drop-shadow" />,
  doc: <FileType2 className="w-5 h-5 text-blue-400 drop-shadow" />,
  default: <File className="w-5 h-5 text-slate-400 drop-shadow" />,
};

export const DocumentCrystal = forwardRef<HTMLDivElement, DocumentCrystalProps>(
  ({ name, type, active = false, className = '' }, ref) => {
    return (
      <div
        ref={ref}
        className={`relative flex items-center gap-3 px-4 py-2 rounded-xl bg-gradient-to-br from-white/10 via-cyan-400/5 to-purple-400/10 border border-cyan-400/20 shadow-xl backdrop-blur-md select-none transition-transform duration-500 ${
          active ? 'animate-crystal-glow scale-105 border-cyan-400/60' : 'hover:scale-105'
        } ${className}`}
        style={{
          boxShadow: active
            ? '0 0 32px 8px rgba(34,211,238,0.25), 0 0 64px 16px rgba(168,85,247,0.15)'
            : '0 2px 8px 0 rgba(31,38,135,0.10)',
          transform: active ? 'translateY(-2px) rotateZ(-2deg)' : 'translateY(0) rotateZ(0deg)',
          animation: active
            ? 'crystal-float 2.5s ease-in-out infinite alternate, crystal-glow 2.5s ease-in-out infinite alternate'
            : 'crystal-float 3.5s ease-in-out infinite alternate',
        }}
        tabIndex={0}
        aria-label={name}
      >
        <span className="flex-shrink-0">
          {iconMap[type] || iconMap.default}
        </span>
        <span className="text-xs text-slate-200 font-semibold truncate flex-1">
          {name}
        </span>
        {/* Animated glow ring */}
        {active && (
          <span className="absolute -inset-1 rounded-2xl border-2 border-cyan-400/40 pointer-events-none animate-pulse" />
        )}
        <style>{`
          @keyframes crystal-float {
            0% { transform: translateY(0) rotateZ(0deg); }
            100% { transform: translateY(-6px) rotateZ(-2deg); }
          }
          @keyframes crystal-glow {
            0% {
              box-shadow: 0 0 32px 8px rgba(34,211,238,0.25), 0 0 64px 16px rgba(168,85,247,0.15);
            }
            100% {
              box-shadow: 0 0 48px 16px rgba(34,211,238,0.35), 0 0 96px 32px rgba(168,85,247,0.25);
            }
          }
          .animate-crystal-glow {
            animation: crystal-float 2.5s ease-in-out infinite alternate, crystal-glow 2.5s ease-in-out infinite alternate;
          }
        `}</style>
      </div>
    );
  }
); 