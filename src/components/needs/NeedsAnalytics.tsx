import React from 'react';
import { motion } from 'framer-motion';
import { BarChart3, TrendingUp, Target, Clock, CheckCircle, AlertCircle } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';

interface NeedsAnalyticsProps {
  analytics: {
    total_needs: number;
    average_priority: number;
    average_progress: number;
    completed_needs: number;
    active_needs: number;
    completion_rate: number;
  };
  className?: string;
}

export const NeedsAnalytics: React.FC<NeedsAnalyticsProps> = ({
  analytics,
  className = ''
}) => {
  const metrics = [
    {
      label: 'Total Needs',
      value: analytics.total_needs,
      icon: Target,
      color: 'text-blue-400',
      bgColor: 'bg-blue-500/10',
      borderColor: 'border-blue-500/30'
    },
    {
      label: 'Completion Rate',
      value: `${analytics.completion_rate}%`,
      icon: CheckCircle,
      color: 'text-green-400',
      bgColor: 'bg-green-500/10',
      borderColor: 'border-green-500/30'
    },
    {
      label: 'Active Needs',
      value: analytics.active_needs,
      icon: Clock,
      color: 'text-yellow-400',
      bgColor: 'bg-yellow-500/10',
      borderColor: 'border-yellow-500/30'
    },
    {
      label: 'Avg Priority',
      value: `${(analytics.average_priority * 100).toFixed(0)}%`,
      icon: TrendingUp,
      color: 'text-purple-400',
      bgColor: 'bg-purple-500/10',
      borderColor: 'border-purple-500/30'
    }
  ];

  const getCompletionStatus = (rate: number) => {
    if (rate >= 80) return { status: 'Excellent', color: 'text-green-400' };
    if (rate >= 60) return { status: 'Good', color: 'text-yellow-400' };
    if (rate >= 40) return { status: 'Fair', color: 'text-orange-400' };
    return { status: 'Needs Improvement', color: 'text-red-400' };
  };

  const completionStatus = getCompletionStatus(analytics.completion_rate);

  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{ duration: 0.3 }}
      className={`p-4 rounded-lg border border-slate-700/50 bg-slate-800/30 ${className}`}
    >
      <div className="flex items-center space-x-2 mb-4">
        <BarChart3 className="w-5 h-5 text-slate-300" />
        <h4 className="text-lg font-semibold text-slate-200">Needs Analytics</h4>
        <Badge 
          variant="outline" 
          className={`text-xs ${completionStatus.color} border-current`}
        >
          {completionStatus.status}
        </Badge>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 gap-4 mb-4">
        {metrics.map((metric, index) => (
          <motion.div
            key={metric.label}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
            className={`p-3 rounded-lg border ${metric.borderColor} ${metric.bgColor}`}
          >
            <div className="flex items-center space-x-2 mb-2">
              <metric.icon className={`w-4 h-4 ${metric.color}`} />
              <span className="text-sm text-slate-300">{metric.label}</span>
            </div>
            <div className={`text-2xl font-bold ${metric.color}`}>
              {metric.value}
            </div>
          </motion.div>
        ))}
      </div>

      {/* Progress Overview */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-sm text-slate-300">Overall Progress</span>
          <span className="text-sm text-slate-400">
            {analytics.average_progress.toFixed(1)}%
          </span>
        </div>
        <Progress 
          value={analytics.average_progress} 
          className="h-3 bg-slate-700/50"
        />

        <div className="flex items-center justify-between">
          <span className="text-sm text-slate-300">Completion Rate</span>
          <span className={`text-sm font-medium ${completionStatus.color}`}>
            {analytics.completion_rate.toFixed(1)}%
          </span>
        </div>
        <Progress 
          value={analytics.completion_rate} 
          className="h-3 bg-slate-700/50"
        />
      </div>

      {/* Insights */}
      <div className="mt-4 pt-4 border-t border-slate-700/50">
        <h5 className="text-sm font-medium text-slate-300 mb-2">Insights</h5>
        <div className="space-y-2 text-xs text-slate-400">
          {analytics.completion_rate >= 80 && (
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-3 h-3 text-green-400" />
              <span>Excellent need completion rate! Keep up the great work.</span>
            </div>
          )}
          
          {analytics.completion_rate < 60 && (
            <div className="flex items-center space-x-2">
              <AlertCircle className="w-3 h-3 text-yellow-400" />
              <span>Consider focusing on completing existing needs before taking on new ones.</span>
            </div>
          )}
          
          {analytics.average_priority > 0.7 && (
            <div className="flex items-center space-x-2">
              <TrendingUp className="w-3 h-3 text-purple-400" />
              <span>High priority needs detected. Focus on critical tasks first.</span>
            </div>
          )}
          
          {analytics.active_needs > analytics.completed_needs && (
            <div className="flex items-center space-x-2">
              <Clock className="w-3 h-3 text-blue-400" />
              <span>More active needs than completed ones. Consider prioritizing completion.</span>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
};
