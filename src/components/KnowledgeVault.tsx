
import { useState } from 'react';
import { FileText, Upload, Brain } from 'lucide-react';
import { Button } from '@/components/ui/button';

export const KnowledgeVault = () => {
  const [documents] = useState([
    { id: 1, name: 'Project Phoenix Brief', type: 'pdf', active: false },
    { id: 2, name: 'Meeting Notes Q4', type: 'doc', active: true },
    { id: 3, name: 'Research Papers', type: 'pdf', active: false },
  ]);

  return (
    <div className="bg-slate-800/30 backdrop-blur-md border border-cyan-400/20 rounded-2xl p-4 w-72">
      <div className="flex items-center space-x-2 mb-4">
        <Brain className="w-5 h-5 text-cyan-400" />
        <h3 className="text-sm font-semibold text-cyan-100">Knowledge Vault</h3>
      </div>

      {/* Document Crystals */}
      <div className="space-y-2 mb-4">
        {documents.map((doc) => (
          <div
            key={doc.id}
            className={`flex items-center space-x-3 p-2 rounded-lg transition-all ${
              doc.active
                ? 'bg-cyan-500/20 border border-cyan-400/30'
                : 'bg-slate-700/30 hover:bg-slate-700/50'
            }`}
          >
            <div
              className={`w-3 h-3 rounded-full ${
                doc.active
                  ? 'bg-cyan-400 shadow-lg shadow-cyan-400/50 animate-pulse'
                  : 'bg-slate-500'
              }`}
            />
            <FileText className="w-4 h-4 text-slate-400" />
            <span className="text-xs text-slate-300 flex-1 truncate">
              {doc.name}
            </span>
          </div>
        ))}
      </div>

      {/* Upload Interface */}
      <Button
        variant="outline"
        className="w-full border-cyan-400/30 bg-slate-800/50 hover:bg-cyan-500/20 hover:border-cyan-400 text-cyan-400"
      >
        <Upload className="w-4 h-4 mr-2" />
        Ingest Knowledge
      </Button>
    </div>
  );
};
