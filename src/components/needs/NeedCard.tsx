import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Target, Brain, Heart, Zap, TrendingUp, Settings, Clock, CheckCircle, Circle, Star, MoreHorizontal } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuItem, 
  DropdownMenuTrigger 
} from '@/components/ui/dropdown-menu';

interface AdvancedNeed {
  id: string;
  title: string;
  description: string;
  category: string;
  priority: number;
  progress: number;
  status: string;
  created_at: string;
  updated_at: string;
  consciousness_context: {
    evolution_level: number;
    emotional_state: string;
    consciousness_level: number;
    phase?: string;
    source?: string;
  };
  related_goals: string[];
  estimated_completion?: string;
}

interface NeedCardProps {
  need: AdvancedNeed;
  index: number;
  onNeedClick: () => void;
  categoryColor: string;
  categoryIcon: React.ComponentType<{ className?: string }>;
}

export const NeedCard: React.FC<NeedCardProps> = ({ 
  need, 
  index, 
  onNeedClick, 
  categoryColor,
  categoryIcon: CategoryIcon
}) => {
  const [isHovered, setIsHovered] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);

  const getPriorityColor = (priority: number) => {
    if (priority >= 0.8) return 'text-red-400';
    if (priority >= 0.6) return 'text-orange-400';
    if (priority >= 0.4) return 'text-yellow-400';
    return 'text-green-400';
  };

  const getPriorityLabel = (priority: number) => {
    if (priority >= 0.8) return 'Critical';
    if (priority >= 0.6) return 'High';
    if (priority >= 0.4) return 'Medium';
    return 'Low';
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-green-400" />;
      case 'in_progress':
        return <Clock className="w-4 h-4 text-blue-400" />;
      case 'paused':
        return <Circle className="w-4 h-4 text-yellow-400" />;
      default:
        return <Circle className="w-4 h-4 text-slate-400" />;
    }
  };

  const formatDate = (dateString: string) => {
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return 'Unknown';
    }
  };

  const handleNeedAction = async (action: string) => {
    try {
      await fetch('/api/needs/interact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          need_id: need.id,
          interaction_type: action,
          user_id: 'mainza-user'
        })
      });
    } catch (err) {
      console.error(`Failed to record ${action} action:`, err);
    }
  };

  const handleComplete = async () => {
    try {
      await fetch('/api/needs/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          need_id: need.id,
          progress: 1.0,
          status: 'completed'
        })
      });
      handleNeedAction('complete');
    } catch (err) {
      console.error('Failed to complete need:', err);
    }
  };

  const handleSkip = async () => {
    handleNeedAction('skip');
  };

  const handleFavorite = async () => {
    handleNeedAction('favorite');
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: index * 0.1 }}
      className={`p-4 rounded-lg border cursor-pointer transition-all duration-300 hover:border-opacity-60 hover:shadow-lg ${categoryColor} ${
        isHovered ? 'border-opacity-60 shadow-lg' : ''
      }`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onClick={onNeedClick}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center space-x-3 flex-1">
          <div className="flex items-center space-x-2">
            <CategoryIcon className="w-4 h-4 text-slate-300" />
            <h4 className="font-semibold text-slate-200 text-sm leading-tight">
              {need.title}
            </h4>
          </div>
          
          <div className="flex items-center space-x-2">
            <Badge 
              variant="outline" 
              className={`text-xs border-slate-500 text-slate-300 ${categoryColor}`}
            >
              {need.category}
            </Badge>
            
            {getStatusIcon(need.status)}
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <div className="flex items-center space-x-1">
            <Star className={`w-3 h-3 ${getPriorityColor(need.priority)}`} />
            <span className={`text-xs font-medium ${getPriorityColor(need.priority)}`}>
              {getPriorityLabel(need.priority)}
            </span>
          </div>
          
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button
                variant="ghost"
                size="sm"
                className="h-6 w-6 p-0 text-slate-400 hover:text-slate-200"
                onClick={(e) => e.stopPropagation()}
              >
                <MoreHorizontal className="w-3 h-3" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="bg-slate-800 border-slate-700">
              <DropdownMenuItem 
                onClick={(e) => {
                  e.stopPropagation();
                  handleComplete();
                }}
                className="text-slate-200 hover:bg-slate-700"
              >
                <CheckCircle className="w-3 h-3 mr-2" />
                Complete
              </DropdownMenuItem>
              <DropdownMenuItem 
                onClick={(e) => {
                  e.stopPropagation();
                  handleSkip();
                }}
                className="text-slate-200 hover:bg-slate-700"
              >
                <Circle className="w-3 h-3 mr-2" />
                Skip
              </DropdownMenuItem>
              <DropdownMenuItem 
                onClick={(e) => {
                  e.stopPropagation();
                  handleFavorite();
                }}
                className="text-slate-200 hover:bg-slate-700"
              >
                <Star className="w-3 h-3 mr-2" />
                Favorite
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>

      {/* Description */}
      <p className="text-sm text-slate-300 leading-relaxed mb-3 line-clamp-2">
        {need.description}
      </p>

      {/* Progress Bar */}
      <div className="mb-3">
        <div className="flex items-center justify-between mb-1">
          <span className="text-xs text-slate-400">Progress</span>
          <span className="text-xs text-slate-400">
            {(need.progress * 100).toFixed(0)}%
          </span>
        </div>
        <Progress 
          value={need.progress * 100} 
          className="h-2 bg-slate-700/50"
        />
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between text-xs">
        <div className="flex items-center space-x-3">
          {/* Consciousness Context */}
          <div className="flex items-center space-x-1">
            <Brain className="w-3 h-3 text-cyan-400" />
            <span className="text-slate-400">
              Level: {need.consciousness_context.evolution_level}
            </span>
          </div>
          
          {/* Emotional State */}
          <div className="flex items-center space-x-1">
            <Heart className="w-3 h-3 text-purple-400" />
            <span className="text-slate-400 capitalize">
              {need.consciousness_context.emotional_state}
            </span>
          </div>
          
          {/* Phase */}
          {need.consciousness_context.phase && (
            <div className="flex items-center space-x-1">
              <Zap className="w-3 h-3 text-yellow-400" />
              <span className="text-slate-400 capitalize">
                {need.consciousness_context.phase.replace('_', ' ')}
              </span>
            </div>
          )}
        </div>
        
        {/* Timestamps */}
        <div className="flex items-center space-x-2 text-slate-400">
          <span>Created: {formatDate(need.created_at)}</span>
          {need.estimated_completion && (
            <span>Due: {formatDate(need.estimated_completion)}</span>
          )}
        </div>
      </div>

      {/* Related Goals */}
      {need.related_goals && need.related_goals.length > 0 && (
        <div className="mt-3 pt-3 border-t border-slate-700/50">
          <div className="flex items-center space-x-2">
            <TrendingUp className="w-3 h-3 text-green-400" />
            <span className="text-xs text-slate-400">Related Goals:</span>
            <div className="flex flex-wrap gap-1">
              {need.related_goals.slice(0, 3).map((goal, idx) => (
                <Badge 
                  key={idx}
                  variant="secondary" 
                  className="text-xs bg-slate-600/50 text-slate-200"
                >
                  {goal}
                </Badge>
              ))}
              {need.related_goals.length > 3 && (
                <Badge 
                  variant="secondary" 
                  className="text-xs bg-slate-600/50 text-slate-200"
                >
                  +{need.related_goals.length - 3} more
                </Badge>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Expandable Details */}
      <motion.div
        initial={false}
        animate={{ height: isExpanded ? 'auto' : 0 }}
        transition={{ duration: 0.3 }}
        className="overflow-hidden"
      >
        <div className="mt-3 pt-3 border-t border-slate-700/50">
          <div className="grid grid-cols-2 gap-4 text-xs">
            <div>
              <span className="text-slate-400">Priority Score:</span>
              <span className="ml-2 text-slate-200">
                {(need.priority * 100).toFixed(1)}%
              </span>
            </div>
            <div>
              <span className="text-slate-400">Status:</span>
              <span className="ml-2 text-slate-200 capitalize">
                {need.status.replace('_', ' ')}
              </span>
            </div>
            <div>
              <span className="text-slate-400">Source:</span>
              <span className="ml-2 text-slate-200">
                {need.consciousness_context.source || 'consciousness'}
              </span>
            </div>
            <div>
              <span className="text-slate-400">Updated:</span>
              <span className="ml-2 text-slate-200">
                {formatDate(need.updated_at)}
              </span>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Expand/Collapse Button */}
      <div className="mt-3 flex justify-center">
        <Button
          variant="ghost"
          size="sm"
          onClick={(e) => {
            e.stopPropagation();
            setIsExpanded(!isExpanded);
          }}
          className="text-xs text-slate-400 hover:text-slate-200 h-6"
        >
          {isExpanded ? 'Show Less' : 'Show More'}
        </Button>
      </div>
    </motion.div>
  );
};
