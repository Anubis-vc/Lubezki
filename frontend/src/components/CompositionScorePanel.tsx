'use client';

import { useState, useEffect } from 'react';
import { CompositionScore, ItemData } from '@/types/image';
import CompositionScores from './CompositionScores';
import CompositionItems from './CompositionItems';

interface CompositionScorePanelProps {
  isOpen: boolean;
  onClose: () => void;
  imageUrl?: string;
  scores?: CompositionScore;
  imageName?: string;
  analysis?: string;
  items?: ItemData[];
  isLoading?: boolean;
}

export default function CompositionScorePanel({
  isOpen,
  onClose,
  imageUrl,
  scores,
  imageName,
  analysis,
  items = [],
  isLoading = false
}: CompositionScorePanelProps) {
  const [isAnimating, setIsAnimating] = useState(false);
  const [activeTab, setActiveTab] = useState<'scores' | 'items'>('scores');

  useEffect(() => {
    if (isOpen) {
      setIsAnimating(true);
    } else {
      setIsAnimating(false);
    }
  }, [isOpen]);

  const handleClose = () => {
    setIsAnimating(false);
    // Small delay to allow exit animation to complete
    setTimeout(() => onClose(), 300);
  };


  return (
    <div
      className={`fixed inset-0 bg-white z-40 transition-transform duration-300 ease-in-out ${isAnimating ? 'translate-x-0' : 'translate-x-full'
        }`}
    >
      {/* Close Button */}
      <button
        onClick={handleClose}
        className="absolute top-4 left-4 z-50 text-gray-500 hover:text-gray-700 transition-colors rounded-full p-2"
        aria-label="Close composition panel"
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <div className="h-full flex overflow-y-auto flex-col lg:flex-row">
        {/* Image Display - Full width on mobile, 2/3 on desktop */}
        <div className="w-full lg:w-2/3 flex items-center justify-center p-6">
          {imageUrl ? (
            <div className="w-full h-full flex items-center justify-center">
              <img
                src={imageUrl}
                alt={imageName || "Analyzed image"}
                className="max-w-[90%] max-h-[90%] object-contain rounded-lg"
              />
            </div>
          ) : (
            <div className="text-gray-400 text-center">
              <p>No image selected</p>
            </div>
          )}
        </div>

        {/* Tabbed Content - Full width on mobile, 1/3 on desktop */}
        <div className="w-full lg:w-1/3 border-t lg:border-t-0 lg:border-l border-gray-200 flex flex-col h-full">
          {/* Tab Navigation */}
          <div className="flex border-b border-gray-200 flex-shrink-0">
            <button
              onClick={() => setActiveTab('scores')}
              className={`flex-1 px-4 py-3 text-sm font-medium transition-colors ${
                activeTab === 'scores'
                  ? 'text-green-600 border-b-2 border-green-600 bg-green-50'
                  : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
              }`}
            >
              Scores
            </button>
            <button
              onClick={() => setActiveTab('items')}
              className={`flex-1 px-4 py-3 text-sm font-medium transition-colors ${
                activeTab === 'items'
                  ? 'text-green-600 border-b-2 border-green-600 bg-green-50'
                  : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
              }`}
            >
              Items ({items.length})
            </button>
          </div>

          {/* Tab Content */}
          <div className="flex-1 overflow-y-auto">
            {activeTab === 'scores' ? (
              <CompositionScores
                scores={scores}
                analysis={analysis}
                isLoading={isLoading}
              />
            ) : (
              <CompositionItems
                items={items}
                isLoading={isLoading}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
