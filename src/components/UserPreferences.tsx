import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { Slider } from '@/components/ui/slider';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Label } from '@/components/ui/label';
import { Separator } from '@/components/ui/separator';
import { Settings, User, MessageSquare, Palette, Brain, RotateCcw, Save } from 'lucide-react';
import { toast } from 'sonner';

interface UserPreferences {
  verbosity: 'concise' | 'detailed' | 'comprehensive';
  max_response_length: number;
  show_tools_used: boolean;
  format_tables: boolean;
  show_context_info: boolean;
  preferred_agent: string | null;
  consciousness_awareness: boolean;
  emotional_responses: boolean;
  dark_mode: boolean;
  compact_mode: boolean;
  auto_suggestions: boolean;
  progressive_disclosure: boolean;
}

interface UserPreferencesProps {
  userId: string;
  onClose?: () => void;
}

const UserPreferencesComponent: React.FC<UserPreferencesProps> = ({ userId, onClose }) => {
  const [preferences, setPreferences] = useState<UserPreferences>({
    verbosity: 'detailed',
    max_response_length: 500,
    show_tools_used: true,
    format_tables: true,
    show_context_info: true,
    preferred_agent: null,
    consciousness_awareness: true,
    emotional_responses: true,
    dark_mode: true,
    compact_mode: false,
    auto_suggestions: true,
    progressive_disclosure: true
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [hasChanges, setHasChanges] = useState(false);

  // Load user preferences on component mount
  useEffect(() => {
    loadPreferences();
  }, [userId]);

  const loadPreferences = async () => {
    try {
      setLoading(true);
      const response = await fetch(`/users/${userId}/preferences`);
      if (response.ok) {
        const data = await response.json();
        setPreferences(data);
      } else {
        console.error('Failed to load preferences');
        toast.error('Failed to load preferences');
      }
    } catch (error) {
      console.error('Error loading preferences:', error);
      toast.error('Error loading preferences');
    } finally {
      setLoading(false);
    }
  };

  const savePreferences = async () => {
    try {
      setSaving(true);
      const response = await fetch(`/users/${userId}/preferences`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(preferences),
      });

      if (response.ok) {
        toast.success('Preferences saved successfully!');
        setHasChanges(false);
      } else {
        toast.error('Failed to save preferences');
      }
    } catch (error) {
      console.error('Error saving preferences:', error);
      toast.error('Error saving preferences');
    } finally {
      setSaving(false);
    }
  };

  const resetPreferences = async () => {
    try {
      setSaving(true);
      const response = await fetch(`/users/${userId}/preferences/reset`, {
        method: 'POST',
      });

      if (response.ok) {
        const data = await response.json();
        setPreferences(data);
        toast.success('Preferences reset to defaults');
        setHasChanges(false);
      } else {
        toast.error('Failed to reset preferences');
      }
    } catch (error) {
      console.error('Error resetting preferences:', error);
      toast.error('Error resetting preferences');
    } finally {
      setSaving(false);
    }
  };

  const updatePreference = (key: keyof UserPreferences, value: any) => {
    setPreferences(prev => ({ ...prev, [key]: value }));
    setHasChanges(true);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-slate-400">Loading preferences...</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-amber-400 to-orange-500 rounded-lg">
            <Settings className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">User Preferences</h1>
            <p className="text-slate-400 text-sm">Customize your Mainza experience</p>
          </div>
        </div>
        <div className="flex gap-2">
          <Button
            onClick={resetPreferences}
            variant="outline"
            size="sm"
            disabled={saving}
            className="text-slate-400 hover:text-white"
          >
            <RotateCcw className="w-4 h-4 mr-2" />
            Reset
          </Button>
          <Button
            onClick={savePreferences}
            disabled={!hasChanges || saving}
            size="sm"
            className="bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600"
          >
            <Save className="w-4 h-4 mr-2" />
            {saving ? 'Saving...' : 'Save Changes'}
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Response Preferences */}
        <Card className="bg-gradient-to-r from-slate-800/50 to-slate-700/30 border-slate-600/30">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-white">
              <MessageSquare className="w-5 h-5 text-amber-400" />
              Response Preferences
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <Label className="text-slate-200">Response Verbosity</Label>
              <Select
                value={preferences.verbosity}
                onValueChange={(value: 'concise' | 'detailed' | 'comprehensive') => 
                  updatePreference('verbosity', value)
                }
              >
                <SelectTrigger className="bg-slate-700/50 border-slate-600">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="concise">Concise (200 chars max)</SelectItem>
                  <SelectItem value="detailed">Detailed (500 chars max)</SelectItem>
                  <SelectItem value="comprehensive">Comprehensive (1000 chars max)</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label className="text-slate-200">
                Max Response Length: {preferences.max_response_length} characters
              </Label>
              <Slider
                value={[preferences.max_response_length]}
                onValueChange={([value]) => updatePreference('max_response_length', value)}
                min={100}
                max={2000}
                step={50}
                className="w-full"
              />
            </div>

            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <Label className="text-slate-200">Show Tools Used</Label>
                <Switch
                  checked={preferences.show_tools_used}
                  onCheckedChange={(checked) => updatePreference('show_tools_used', checked)}
                />
              </div>

              <div className="flex items-center justify-between">
                <Label className="text-slate-200">Format Tables for Chat</Label>
                <Switch
                  checked={preferences.format_tables}
                  onCheckedChange={(checked) => updatePreference('format_tables', checked)}
                />
              </div>

              <div className="flex items-center justify-between">
                <Label className="text-slate-200">Show Context Information</Label>
                <Switch
                  checked={preferences.show_context_info}
                  onCheckedChange={(checked) => updatePreference('show_context_info', checked)}
                />
              </div>

              <div className="flex items-center justify-between">
                <Label className="text-slate-200">Progressive Disclosure</Label>
                <Switch
                  checked={preferences.progressive_disclosure}
                  onCheckedChange={(checked) => updatePreference('progressive_disclosure', checked)}
                />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* AI Interaction Preferences */}
        <Card className="bg-gradient-to-r from-slate-800/50 to-slate-700/30 border-slate-600/30">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-white">
              <Brain className="w-5 h-5 text-amber-400" />
              AI Interaction
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <Label className="text-slate-200">Preferred Agent</Label>
              <Select
                value={preferences.preferred_agent || 'auto'}
                onValueChange={(value) => 
                  updatePreference('preferred_agent', value === 'auto' ? null : value)
                }
              >
                <SelectTrigger className="bg-slate-700/50 border-slate-600">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="auto">Auto-select (Recommended)</SelectItem>
                  <SelectItem value="graphmaster">Graphmaster (Knowledge)</SelectItem>
                  <SelectItem value="taskmaster">Taskmaster (Tasks)</SelectItem>
                  <SelectItem value="codeweaver">CodeWeaver (Code)</SelectItem>
                  <SelectItem value="rag">RAG (Documents)</SelectItem>
                  <SelectItem value="simple_chat">Simple Chat (General)</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <Label className="text-slate-200">Consciousness Awareness</Label>
                <Switch
                  checked={preferences.consciousness_awareness}
                  onCheckedChange={(checked) => updatePreference('consciousness_awareness', checked)}
                />
              </div>

              <div className="flex items-center justify-between">
                <Label className="text-slate-200">Emotional Responses</Label>
                <Switch
                  checked={preferences.emotional_responses}
                  onCheckedChange={(checked) => updatePreference('emotional_responses', checked)}
                />
              </div>

              <div className="flex items-center justify-between">
                <Label className="text-slate-200">Auto Suggestions</Label>
                <Switch
                  checked={preferences.auto_suggestions}
                  onCheckedChange={(checked) => updatePreference('auto_suggestions', checked)}
                />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* UI Preferences */}
        <Card className="bg-gradient-to-r from-slate-800/50 to-slate-700/30 border-slate-600/30">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-white">
              <Palette className="w-5 h-5 text-amber-400" />
              Interface Preferences
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <Label className="text-slate-200">Dark Mode</Label>
                <Switch
                  checked={preferences.dark_mode}
                  onCheckedChange={(checked) => updatePreference('dark_mode', checked)}
                />
              </div>

              <div className="flex items-center justify-between">
                <Label className="text-slate-200">Compact Mode</Label>
                <Switch
                  checked={preferences.compact_mode}
                  onCheckedChange={(checked) => updatePreference('compact_mode', checked)}
                />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* User Info */}
        <Card className="bg-gradient-to-r from-slate-800/50 to-slate-700/30 border-slate-600/30">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-white">
              <User className="w-5 h-5 text-amber-400" />
              User Information
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="text-sm text-slate-400">
              <p><strong>User ID:</strong> {userId}</p>
              <p><strong>Preferences Version:</strong> 1.0</p>
              <p><strong>Last Updated:</strong> {new Date().toLocaleString()}</p>
            </div>
            
            <Separator className="bg-slate-600" />
            
            <div className="text-xs text-slate-500">
              <p>These preferences control how Mainza responds to your queries and how the interface behaves.</p>
              <p>Changes are saved automatically when you click "Save Changes".</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default UserPreferencesComponent;
