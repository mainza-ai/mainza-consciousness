import { useState } from 'react';
import { Upload } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { HolographicPane } from './ui/holographic-pane';
import { DocumentCrystal } from './ui/document-crystal';

interface KnowledgeVaultProps {
  activeDocumentIds?: number[];
  getCrystalRef?: (id: number, ref: HTMLDivElement | null) => void;
}

export const KnowledgeVault = ({ activeDocumentIds = [], getCrystalRef }: KnowledgeVaultProps) => {
  const [documents] = useState([
    { id: 1, name: 'Project Phoenix Brief', type: 'pdf' },
    { id: 2, name: 'Meeting Notes Q4', type: 'doc' },
    { id: 3, name: 'Research Papers', type: 'pdf' },
  ]);

  return (
    <HolographicPane title="Knowledge Vault" className="w-72">
      {/* Document Crystals */}
      <div className="space-y-2 mb-4 flex flex-col items-center">
        {documents.map((doc) => (
          <DocumentCrystal
            key={doc.id}
            name={doc.name}
            type={doc.type}
            active={activeDocumentIds.includes(doc.id)}
            ref={el => getCrystalRef && getCrystalRef(doc.id, el)}
          />
        ))}
      </div>
      <Button variant="ghost" className="w-full flex items-center justify-center gap-2 mt-2">
        <Upload className="w-4 h-4 text-cyan-400" />
        <span>Upload Document</span>
      </Button>
    </HolographicPane>
  );
};
