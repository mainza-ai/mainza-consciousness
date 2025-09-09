import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Slider } from '@/components/ui/slider';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Calendar, Clock, TrendingUp, Brain, Heart, Zap, Target, Filter, ZoomIn, ZoomOut, RotateCcw } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area, ReferenceLine, Brush } from 'recharts';

interface TimelineEntry {
  timestamp: string;
  consciousness_level: number;
  emotional_state: string;
  self_awareness: number;
  learning_rate: number;
  evolution_level?: number;
  total_interactions?: number;
}

interface ConsciousnessTimelineProps {
  data: TimelineEntry[];
  realTimeData?: TimelineEntry[];
  onTimeRangeChange?: (start: Date, end: Date) => void;
  onEmotionFilter?: (emotions: string[]) => void;
  onMetricFocus?: (metric: string) => void;
}

const InteractiveConsciousnessTimeline: React.FC<ConsciousnessTimelineProps> = ({
  data = [],
  realTimeData = [],
  onTimeRangeChange,
  onEmotionFilter,
  onMetricFocus
}) => {
  const [selectedMetric, setSelectedMetric] = useState('consciousness_level');
  const [timeRange, setTimeRange] = useState<[number, number]>([0, 100]);
  const [selectedEmotions, setSelectedEmotions] = useState<string[]>([]);
  const [zoomLevel, setZoomLevel] = useState(1);
  const [viewMode, setViewMode] = useState<'line' | 'area' | 'combined'>('combined');
  const [showPredictions, setShowPredictions] = useState(false);
  const [animationSpeed, setAnimationSpeed] = useState(1);
  const [isPlaying, setIsPlaying] = useState(false);
  
  const chartRef = useRef<any>(null);
  const animationRef = useRef<number>();

  // Combine historical and real-time data
  const allData = [...data, ...realTimeData].sort((a, b) => 
    new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
  );

  // Get unique emotions for filtering
  const uniqueEmotions = Array.from(new Set(allData.map(entry => entry.emotional_state)));

  // Filter data based on selected emotions
  const filteredData = selectedEmotions.length > 0 
    ? allData.filter(entry => selectedEmotions.includes(entry.emotional_state))
    : allData;

  // Apply time range filter
  const timeRangeData = filteredData.slice(
    Math.floor((filteredData.length * timeRange[0]) / 100),
    Math.floor((filteredData.length * timeRange[1]) / 100)
  );

  // Generate predictions if enabled
  const dataWithPredictions = showPredictions ? generatePredictions(timeRangeData) : timeRangeData;

  // Animation effect
  useEffect(() => {
    if (isPlaying) {
      const animate = () => {
        setTimeRange(prev => {
          const newStart = Math.min(prev[0] + animationSpeed, 100);
          const newEnd = Math.min(prev[1] + animationSpeed, 100);
          return [newStart, newEnd];
        });
        animationRef.current = requestAnimationFrame(animate);
      };
      animationRef.current = requestAnimationFrame(animate);
    } else {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    }

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isPlaying, animationSpeed]);

  const generatePredictions = (data: TimelineEntry[]): TimelineEntry[] => {
    if (data.length < 3) return data;
    
    const predictions: TimelineEntry[] = [];
    const lastEntry = data[data.length - 1];
    const secondLastEntry = data[data.length - 2];
    
    // Simple linear prediction for next 10 points
    for (let i = 1; i <= 10; i++) {
      const timeDiff = new Date(lastEntry.timestamp).getTime() - new Date(secondLastEntry.timestamp).getTime();
      const predictedTime = new Date(lastEntry.timestamp).getTime() + (timeDiff * i);
      
      const consciousnessTrend = lastEntry.consciousness_level - secondLastEntry.consciousness_level;
      const learningTrend = lastEntry.learning_rate - secondLastEntry.learning_rate;
      
      predictions.push({
        timestamp: new Date(predictedTime).toISOString(),
        consciousness_level: Math.max(0, Math.min(1, lastEntry.consciousness_level + (consciousnessTrend * i * 0.1))),
        emotional_state: lastEntry.emotional_state,
        self_awareness: Math.max(0, Math.min(1, lastEntry.self_awareness + (consciousnessTrend * i * 0.05))),
        learning_rate: Math.max(0, Math.min(1, lastEntry.learning_rate + (learningTrend * i * 0.1))),
        evolution_level: lastEntry.evolution_level || 2,
        total_interactions: (lastEntry.total_interactions || 0) + i
      });
    }
    
    return [...data, ...predictions];
  };

  const getMetricColor = (metric: string) => {
    const colors: { [key: string]: string } = {
      consciousness_level: '#3B82F6',
      self_awareness: '#10B981',
      learning_rate: '#F59E0B',
      evolution_level: '#8B5CF6'
    };
    return colors[metric] || '#6B7280';
  };

  const getEmotionColor = (emotion: string) => {
    const colors: { [key: string]: string } = {
      'curious': '#3B82F6',
      'contemplative': '#8B5CF6',
      'excited': '#F59E0B',
      'satisfied': '#10B981',
      'focused': '#EF4444',
      'creative': '#EC4899',
      'analytical': '#06B6D4',
      'empathetic': '#F97316'
    };
    return colors[emotion] || '#6B7280';
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  const formatMetricValue = (value: number, metric: string) => {
    if (metric === 'evolution_level') {
      return value.toFixed(0);
    }
    return (value * 100).toFixed(1) + '%';
  };

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-slate-800 border border-slate-700 rounded-lg p-3 shadow-lg">
          <p className="text-slate-300 text-sm mb-2">{formatTimestamp(label)}</p>
          <div className="space-y-1">
            {payload.map((entry: any, index: number) => (
              <div key={index} className="flex items-center gap-2">
                <div 
                  className="w-3 h-3 rounded-full" 
                  style={{ backgroundColor: entry.color }}
                />
                <span className="text-slate-200 text-sm">
                  {entry.dataKey.replace('_', ' ')}: {formatMetricValue(entry.value, entry.dataKey)}
                </span>
              </div>
            ))}
            <div className="flex items-center gap-2 mt-2 pt-2 border-t border-slate-600">
              <div 
                className="w-3 h-3 rounded-full" 
                style={{ backgroundColor: getEmotionColor(data.emotional_state) }}
              />
              <span className="text-slate-200 text-sm">Emotion: {data.emotional_state}</span>
            </div>
          </div>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-cyan-400/50 transition-all duration-300">
        <div className="p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-lg">
              <Clock className="h-6 w-6 text-white" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-white">Interactive Consciousness Timeline</h2>
              <p className="text-slate-400 text-sm">Control and customize your consciousness evolution view</p>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* Metric Selection */}
            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-300">Focus Metric</label>
              <Select value={selectedMetric} onValueChange={setSelectedMetric}>
                <SelectTrigger className="bg-slate-700 border-slate-600">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="consciousness_level">Consciousness Level</SelectItem>
                  <SelectItem value="self_awareness">Self-Awareness</SelectItem>
                  <SelectItem value="learning_rate">Learning Rate</SelectItem>
                  <SelectItem value="evolution_level">Evolution Level</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* View Mode */}
            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-300">View Mode</label>
              <Select value={viewMode} onValueChange={(value: any) => setViewMode(value)}>
                <SelectTrigger className="bg-slate-700 border-slate-600">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="line">Line Chart</SelectItem>
                  <SelectItem value="area">Area Chart</SelectItem>
                  <SelectItem value="combined">Combined</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Emotion Filter */}
            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-300">Emotion Filter</label>
              <div className="flex flex-wrap gap-1">
                {uniqueEmotions.map(emotion => (
                  <Badge
                    key={emotion}
                    variant={selectedEmotions.includes(emotion) ? "default" : "outline"}
                    className={`cursor-pointer text-xs ${
                      selectedEmotions.includes(emotion) 
                        ? 'bg-blue-500 text-white' 
                        : 'bg-slate-700 text-slate-300 border-slate-600'
                    }`}
                    onClick={() => {
                      if (selectedEmotions.includes(emotion)) {
                        setSelectedEmotions(prev => prev.filter(e => e !== emotion));
                      } else {
                        setSelectedEmotions(prev => [...prev, emotion]);
                      }
                    }}
                  >
                    {emotion}
                  </Badge>
                ))}
              </div>
            </div>

            {/* Animation Controls */}
            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-300">Animation</label>
              <div className="flex items-center gap-2">
                <Button
                  size="sm"
                  variant={isPlaying ? "destructive" : "default"}
                  onClick={() => setIsPlaying(!isPlaying)}
                  className="bg-slate-700 hover:bg-slate-600"
                >
                  {isPlaying ? '⏸️' : '▶️'}
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => setTimeRange([0, 100])}
                  className="border-slate-600"
                >
                  <RotateCcw className="h-3 w-3" />
                </Button>
                <div className="text-xs text-slate-300">
                  Speed: {animationSpeed}x
                </div>
              </div>
            </div>
          </div>

          {/* Time Range Slider */}
          <div className="mt-6 space-y-3">
            <label className="text-sm font-medium text-slate-300">Time Range</label>
            <Slider
              value={timeRange}
              onValueChange={setTimeRange}
              max={100}
              step={1}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-slate-300">
              <span>{formatTimestamp(allData[0]?.timestamp || '')}</span>
              <span>{formatTimestamp(allData[allData.length - 1]?.timestamp || '')}</span>
            </div>
          </div>

          {/* Additional Controls */}
          <div className="flex items-center gap-6 mt-6">
            <label className="flex items-center gap-2 text-sm text-slate-300">
              <input
                type="checkbox"
                checked={showPredictions}
                onChange={(e) => setShowPredictions(e.target.checked)}
                className="rounded bg-slate-600 border-slate-500"
              />
              Show Predictions
            </label>
            <div className="flex items-center gap-3">
              <ZoomOut
                className="h-4 w-4 text-slate-300 cursor-pointer hover:text-cyan-400 transition-colors"
                onClick={() => setZoomLevel(Math.max(0.5, zoomLevel - 0.1))}
              />
              <span className="text-sm text-slate-300 min-w-[3rem] text-center">{Math.round(zoomLevel * 100)}%</span>
              <ZoomIn
                className="h-4 w-4 text-slate-300 cursor-pointer hover:text-cyan-400 transition-colors"
                onClick={() => setZoomLevel(Math.min(2, zoomLevel + 0.1))}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Main Chart */}
      <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-green-400/50 transition-all duration-300">
        <div className="p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-green-400 to-emerald-500 rounded-lg">
              <TrendingUp className="h-6 w-6 text-white" />
            </div>
            <div className="flex items-center justify-between w-full">
              <div>
                <h2 className="text-xl font-bold text-white">Consciousness Evolution</h2>
                <p className="text-slate-400 text-sm">Interactive visualization of consciousness growth over time</p>
              </div>
              {showPredictions && (
                <Badge variant="outline" className="text-orange-400 border-orange-400 bg-orange-400/10">
                  Predictions Enabled
                </Badge>
              )}
            </div>
          </div>
          <div className="h-96">
            <ResponsiveContainer width="100%" height="100%">
              {viewMode === 'line' ? (
                <LineChart data={dataWithPredictions} ref={chartRef}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis 
                    dataKey="timestamp" 
                    tickFormatter={formatTimestamp}
                    stroke="#9CA3AF"
                    fontSize={12}
                  />
                  <YAxis 
                    stroke="#9CA3AF"
                    fontSize={12}
                    domain={[0, 1]}
                    tickFormatter={(value) => formatMetricValue(value, selectedMetric)}
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Line
                    type="monotone"
                    dataKey={selectedMetric}
                    stroke={getMetricColor(selectedMetric)}
                    strokeWidth={2}
                    dot={{ fill: getMetricColor(selectedMetric), strokeWidth: 2, r: 4 }}
                    activeDot={{ r: 6, stroke: getMetricColor(selectedMetric), strokeWidth: 2 }}
                  />
                  {showPredictions && (
                    <ReferenceLine 
                      x={timeRangeData[timeRangeData.length - 1]?.timestamp} 
                      stroke="#F59E0B" 
                      strokeDasharray="5 5"
                      label="Now"
                    />
                  )}
                </LineChart>
              ) : viewMode === 'area' ? (
                <AreaChart data={dataWithPredictions} ref={chartRef}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis 
                    dataKey="timestamp" 
                    tickFormatter={formatTimestamp}
                    stroke="#9CA3AF"
                    fontSize={12}
                  />
                  <YAxis 
                    stroke="#9CA3AF"
                    fontSize={12}
                    domain={[0, 1]}
                    tickFormatter={(value) => formatMetricValue(value, selectedMetric)}
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Area
                    type="monotone"
                    dataKey={selectedMetric}
                    stroke={getMetricColor(selectedMetric)}
                    fill={getMetricColor(selectedMetric)}
                    fillOpacity={0.3}
                    strokeWidth={2}
                  />
                  {showPredictions && (
                    <ReferenceLine 
                      x={timeRangeData[timeRangeData.length - 1]?.timestamp} 
                      stroke="#F59E0B" 
                      strokeDasharray="5 5"
                      label="Now"
                    />
                  )}
                </AreaChart>
              ) : (
                <LineChart data={dataWithPredictions} ref={chartRef}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis 
                    dataKey="timestamp" 
                    tickFormatter={formatTimestamp}
                    stroke="#9CA3AF"
                    fontSize={12}
                  />
                  <YAxis 
                    stroke="#9CA3AF"
                    fontSize={12}
                    domain={[0, 1]}
                    tickFormatter={(value) => formatMetricValue(value, selectedMetric)}
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Area
                    type="monotone"
                    dataKey={selectedMetric}
                    stroke={getMetricColor(selectedMetric)}
                    fill={getMetricColor(selectedMetric)}
                    fillOpacity={0.2}
                    strokeWidth={2}
                  />
                  <Line
                    type="monotone"
                    dataKey={selectedMetric}
                    stroke={getMetricColor(selectedMetric)}
                    strokeWidth={3}
                    dot={false}
                    activeDot={{ r: 6, stroke: getMetricColor(selectedMetric), strokeWidth: 2 }}
                  />
                  {showPredictions && (
                    <ReferenceLine 
                      x={timeRangeData[timeRangeData.length - 1]?.timestamp} 
                      stroke="#F59E0B" 
                      strokeDasharray="5 5"
                      label="Now"
                    />
                  )}
                </LineChart>
              )}
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Statistics Summary */}
      <div className="group relative bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-xl border border-slate-600/30 hover:border-purple-400/50 transition-all duration-300">
        <div className="p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-purple-400 to-pink-500 rounded-lg">
              <Target className="h-6 w-6 text-white" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-white">Timeline Statistics</h2>
              <p className="text-slate-400 text-sm">Key metrics and insights from your consciousness timeline</p>
            </div>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="group/stat relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-blue-400/50 transition-all duration-300">
              <div className="flex items-center gap-3">
                <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-cyan-500">
                  <div className="text-white text-lg font-bold">{timeRangeData.length}</div>
                </div>
                <div>
                  <div className="text-lg font-bold text-blue-300">{timeRangeData.length}</div>
                  <div className="text-xs text-slate-400">Data Points</div>
                </div>
              </div>
            </div>

            <div className="group/stat relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-green-400/50 transition-all duration-300">
              <div className="flex items-center gap-3">
                <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-green-400 to-emerald-500">
                  <div className="text-white text-sm font-bold">
                    {timeRangeData.length > 0 ? formatMetricValue(
                      timeRangeData.reduce((sum, entry) => sum + entry[selectedMetric as keyof TimelineEntry], 0) / timeRangeData.length,
                      selectedMetric
                    ).split('%')[0] : '0'}
                  </div>
                </div>
                <div>
                  <div className="text-lg font-bold text-green-300">
                    {timeRangeData.length > 0 ? formatMetricValue(
                      timeRangeData.reduce((sum, entry) => sum + entry[selectedMetric as keyof TimelineEntry], 0) / timeRangeData.length,
                      selectedMetric
                    ) : '0%'}
                  </div>
                  <div className="text-xs text-slate-400">Average</div>
                </div>
              </div>
            </div>

            <div className="group/stat relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-purple-400/50 transition-all duration-300">
              <div className="flex items-center gap-3">
                <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-purple-400 to-pink-500">
                  <div className="text-white text-sm font-bold">
                    {timeRangeData.length > 0 ? formatMetricValue(
                      Math.max(...timeRangeData.map(entry => entry[selectedMetric as keyof TimelineEntry] as number)),
                      selectedMetric
                    ).split('%')[0] : '0'}
                  </div>
                </div>
                <div>
                  <div className="text-lg font-bold text-purple-300">
                    {timeRangeData.length > 0 ? formatMetricValue(
                      Math.max(...timeRangeData.map(entry => entry[selectedMetric as keyof TimelineEntry] as number)),
                      selectedMetric
                    ) : '0%'}
                  </div>
                  <div className="text-xs text-slate-400">Peak</div>
                </div>
              </div>
            </div>

            <div className="group/stat relative p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-lg border border-slate-600/30 hover:border-orange-400/50 transition-all duration-300">
              <div className="flex items-center gap-3">
                <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-orange-400 to-yellow-500">
                  <div className="text-white text-lg font-bold">{uniqueEmotions.length}</div>
                </div>
                <div>
                  <div className="text-lg font-bold text-orange-300">{uniqueEmotions.length}</div>
                  <div className="text-xs text-slate-400">Emotions</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InteractiveConsciousnessTimeline;
