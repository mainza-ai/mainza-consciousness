import React from 'react';
import { Badge } from '@/components/ui/badge';
import { Clock, Wrench, AlertCircle } from 'lucide-react';

interface DevelopmentStatusBadgeProps {
  status: 'coming-soon' | 'in-development' | 'partial-data' | 'mock-data';
  className?: string;
}

const DevelopmentStatusBadge: React.FC<DevelopmentStatusBadgeProps> = ({ 
  status, 
  className = '' 
}) => {
  const getStatusConfig = () => {
    switch (status) {
      case 'coming-soon':
        return {
          icon: Clock,
          text: 'Coming Soon',
          variant: 'secondary' as const,
          className: 'bg-blue-500/20 text-blue-300 border-blue-400/30'
        };
      case 'in-development':
        return {
          icon: Wrench,
          text: 'In Development',
          variant: 'secondary' as const,
          className: 'bg-yellow-500/20 text-yellow-300 border-yellow-400/30'
        };
      case 'partial-data':
        return {
          icon: AlertCircle,
          text: 'Partial Data',
          variant: 'secondary' as const,
          className: 'bg-orange-500/20 text-orange-300 border-orange-400/30'
        };
      case 'mock-data':
        return {
          icon: AlertCircle,
          text: 'Mock Data',
          variant: 'secondary' as const,
          className: 'bg-red-500/20 text-red-300 border-red-400/30'
        };
      default:
        return {
          icon: Clock,
          text: 'Coming Soon',
          variant: 'secondary' as const,
          className: 'bg-blue-500/20 text-blue-300 border-blue-400/30'
        };
    }
  };

  const config = getStatusConfig();
  const Icon = config.icon;

  return (
    <Badge 
      variant={config.variant}
      className={`flex items-center gap-1 text-xs font-medium ${config.className} ${className}`}
    >
      <Icon className="w-3 h-3" />
      {config.text}
    </Badge>
  );
};

export default DevelopmentStatusBadge;
