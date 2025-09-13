'use client';

import { useState, useEffect } from 'react';
import { ImageUpload, CompositionScorePanel } from './index';
import { CompositionScore, ItemData } from '@/types/image';

export default function CollapsibleUploadPanel() {
  const [isOpen, setIsOpen] = useState(false);
  const [isAnimating, setIsAnimating] = useState(false);
  const [isAnalysisPanelOpen, setIsAnalysisPanelOpen] = useState(false);
  const [analysisData, setAnalysisData] = useState<{
    imageUrl: string;
    scores?: CompositionScore;
    analysis?: string;
    items?: ItemData[];
  } | null>(null);

  useEffect(() => {
    const handleToggle = () => {
      if (!isOpen) {
        setIsOpen(true);
        setIsAnimating(true);
      } else {
        setIsAnimating(false);
        // Small delay to allow exit animation to complete
        setTimeout(() => setIsOpen(false), 300);
      }
    };

    const handleOpenAnalysis = (event: CustomEvent) => {
      setAnalysisData(event.detail);
      setIsAnalysisPanelOpen(true);
    };

    window.addEventListener('toggleUploadPanel', handleToggle);
    window.addEventListener('openFullAnalysis', handleOpenAnalysis as EventListener);
    
    return () => {
      window.removeEventListener('toggleUploadPanel', handleToggle);
      window.removeEventListener('openFullAnalysis', handleOpenAnalysis as EventListener);
    };
  }, [isOpen]);

  const handleClose = () => {
    setIsAnimating(false);
    // Small delay to allow exit animation to complete
    setTimeout(() => setIsOpen(false), 300);
  };

  const handleCloseAnalysis = () => {
    setIsAnalysisPanelOpen(false);
    setAnalysisData(null);
  };

  return (
    <>
      <div 
        className={`fixed top-0 left-0 h-full w-1/2 bg-white shadow-2xl z-40 transition-transform duration-300 ease-in-out ${
          isAnimating ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="h-full overflow-y-auto p-6">
          <div className="flex items-center justify-between mb-6">
            <button
              onClick={handleClose}
              className="text-gray-500 hover:text-gray-700 transition-colors"
              aria-label="Close upload panel"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <ImageUpload />
        </div>
      </div>

      {/* Analysis Panel */}
      {analysisData && (
        <CompositionScorePanel
          isOpen={isAnalysisPanelOpen}
          onClose={handleCloseAnalysis}
          imageUrl={analysisData.imageUrl}
          scores={analysisData.scores}
          analysis={analysisData.analysis}
          items={analysisData.items}
          isLoading={false}
          imageWidth={undefined}
          imageHeight={undefined}
        />
      )}
    </>
  );
} 