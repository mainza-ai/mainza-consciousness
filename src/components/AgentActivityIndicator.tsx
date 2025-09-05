import React from 'react';
import { motion } from 'framer-motion';
import { 
  Brain, 
  Database, 
  CheckSquare, 
  Code, 
  FileText, 
  Bell, 
  Calendar, 
  Shuffle,
  Loader2,
  Zap
} from 'lucide-react';
import { cn } from '@/lib/utils';

type ActiveAgent = 'none' | 'router' | 'graphmaster' | 'taskmaster' | 'codeweaver' | 'rag' | 'conductor' | 'notification' | 'calendar';

interface AgentActivityIndicatorProps {
  currentAgent: ActiveAgent;
  activity?: string;
  estimatedTime?: string;
  showDetails?: boolean;
  className?: string;
}

const agentConfig = {
  none: {
    name: 'Idle',
    icon: Brain,
    color: 'text-slate-400',
    bgColor: 'bg-slate-500/10',
    description: 'Ready to assist',
    defaultActivity: 'Waiting for your input...'
  },
  router: {
    name: 'Router',
    icon: Shuffle,
    color: 'text-gray-400',
    bgColor: 'bg-gray-500/10',
    description: 'Analyzing and routing your request',
    defaultActivity: 'Determining the best approach for your request...'
  },
  graphmaster: {
    name: 'GraphMaster',
    icon: Database,
    color: 'text-green-400',
    bgColor: 'bg-green-500/10',
    description: 'Managing knowledge graph and memories',
    defaultActivity: 'Searching through knowledge and memories...'
  },
  taskmaster: {
    name: 'TaskMaster',
    icon: CheckSquare,
    color: 'text-yellow-400',
    bgColor: 'bg-yellow-500/10',
    description: 'Organizing and managing tasks',
    defaultActivity: 'Processing task requirements...'
  },
  codeweaver: {
    name: 'CodeWeaver',
    icon: Code,
    color: 'text-purple-400',
    bgColor: 'bg-purple-500/10',
    description: 'Writing and analyzing code',
    defaultActivity: 'Analyzing code and generating solutions...'
  },
  rag: {
    name: 'RAG',
    icon: FileText,
    color: 'text-blue-400',
    bgColor: 'bg-blue-500/10',
    description: 'Retrieving relevant documents',
    defaultActivity: 'Searching through documents for relevant information...'
  },
  conductor: {
    name: 'Conductor',
    icon: Zap,
    color: 'text-pink-400',
    bgColor: 'bg-pink-500/10',
    description: 'Orchestrating complex workflows',
    defaultActivity: 'Coordinating multiple agents for complex task...'
  },
  notification: {
    name: 'Notification',
    icon: Bell,
    color: 'text-orange-400',
    bgColor: 'bg-orange-500/10',
    description: 'Managing notifications and alerts',
    defaultActivity: 'Processing notification request...'
  },
  calendar: {
    name: 'Calendar',
    icon: Calendar,
    color: 'text-cyan-400',
    bgColor: 'bg-cyan-500/10',
    description: 'Managing calendar and scheduling',
    defaultActivity: 'Processing calendar request...'
  }
};

export const AgentActivityIndicator: React.FC<AgentActivityIndicatorProps> = ({
  currentAgent,
  activity,
  estimatedTime,
  showDetails = true,
  className
}) => {
  const config = agentConfig[currentAgent];
  const Icon = config.icon;
  const displayActivity = activity || config.defaultActivity;
  const isActive = currentAgent !== 'none';

  return (
    <motion.div 
      className={cn(
        "rounded-xl p-4 shadow-lg transition-all duration-300",
        config.bgColor,
        "border border-slate-700/50",
        className
      )}
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.2 }}
    >
      <div className="flex items-center space-x-3">
        {/* Agent Icon */}
        <div className={cn(
          "flex items-center justify-center w-10 h-10 rounded-full",
          config.bgColor,
          "border border-current/20"
        )}>
          {isActive ? (
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            >
              <Icon className={cn("w-5 h-5", config.color)} />
            </motion.div>
          ) : (
            <Icon className={cn("w-5 h-5", config.color)} />
          )}
        </div>

        {/* Agent Info */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center space-x-2">
            <h4 className={cn("font-semibold", config.color)}>
              {config.name}
            </h4>
            {isActive && (
              <motion.div
                animate={{ opacity: [0.5, 1, 0.5] }}
                transition={{ duration: 1.5, repeat: Infinity }}
              >
                <Loader2 className="w-4 h-4 text-slate-400" />
              </motion.div>
            )}
            {estimatedTime && (
              <span className="text-xs text-slate-500 bg-slate-700/30 px-2 py-1 rounded">
                ~{estimatedTime}
              </span>
            )}
          </div>
          
          {showDetails && (
            <div className="mt-1">
              <p className="text-sm text-slate-300 truncate">
                {displayActivity}
              </p>
              <p className="text-xs text-slate-500 mt-1">
                {config.description}
              </p>
            </div>
          )}
        </div>

        {/* Activity Indicator */}
        {isActive && (
          <div className="flex flex-col items-center">
            <motion.div
              className={cn("w-2 h-2 rounded-full", config.color.replace('text-', 'bg-'))}
              animate={{ 
                scale: [1, 1.2, 1],
                opacity: [0.7, 1, 0.7]
              }}
              transition={{ 
                duration: 1, 
                repeat: Infinity,
                ease: "easeInOut"
              }}
            />
            <span className="text-xs text-slate-500 mt-1">Active</span>
          </div>
        )}
      </div>

      {/* Progress Bar for Active Agents */}
      {isActive && estimatedTime && (
        <div className="mt-3">
          <div className="w-full bg-slate-700/30 rounded-full h-1">
            <motion.div 
              className={cn("h-1 rounded-full", config.color.replace('text-', 'bg-'))}
              initial={{ width: "0%" }}
              animate={{ width: "100%" }}
              transition={{ 
                duration: estimatedTime.includes('s') ? 
                  parseInt(estimatedTime.replace('s', '')) : 3,
                ease: "linear"
              }}
            />
          </div>
        </div>
      )}
    </motion.div>
  );
};