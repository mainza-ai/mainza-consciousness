import React from 'react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Filter } from 'lucide-react';

interface NeedCategoryFilterProps {
  selected: string;
  onChange: (category: string) => void;
  className?: string;
}

const categories = [
  { value: 'all', label: 'All Categories', icon: '🔍' },
  { value: 'consciousness', label: 'Consciousness', icon: '🧠' },
  { value: 'emotional', label: 'Emotional', icon: '❤️' },
  { value: 'learning', label: 'Learning', icon: '🎯' },
  { value: 'growth', label: 'Growth', icon: '📈' },
  { value: 'system', label: 'System', icon: '⚙️' },
  { value: 'social', label: 'Social', icon: '👥' },
  { value: 'creative', label: 'Creative', icon: '✨' },
  { value: 'reflection', label: 'Reflection', icon: '🤔' }
];

export const NeedCategoryFilter: React.FC<NeedCategoryFilterProps> = ({
  selected,
  onChange,
  className = ''
}) => {
  const selectedCategory = categories.find(cat => cat.value === selected);

  return (
    <div className={`flex items-center space-x-2 ${className}`}>
      <Filter className="w-4 h-4 text-slate-400" />
      <Select value={selected} onValueChange={onChange}>
        <SelectTrigger className="w-48 h-8 bg-slate-800/50 border-slate-600 text-slate-200 hover:bg-slate-700/50">
          <SelectValue>
            <div className="flex items-center space-x-2">
              <span>{selectedCategory?.icon}</span>
              <span className="text-sm">{selectedCategory?.label}</span>
            </div>
          </SelectValue>
        </SelectTrigger>
        <SelectContent className="bg-slate-800 border-slate-600">
          {categories.map((category) => (
            <SelectItem
              key={category.value}
              value={category.value}
              className="text-slate-200 hover:bg-slate-700 focus:bg-slate-700"
            >
              <div className="flex items-center space-x-2">
                <span>{category.icon}</span>
                <span>{category.label}</span>
              </div>
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
};
