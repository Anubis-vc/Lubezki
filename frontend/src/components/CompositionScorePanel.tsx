'use client';

import { useState, useEffect } from 'react';
import { CompositionScore } from '@/types/image';

interface CompositionScorePanelProps {
  isOpen: boolean;
  onClose: () => void;
  imageUrl?: string;
  scores?: CompositionScore;
  imageName?: string;
}

export default function CompositionScorePanel({ 
  isOpen, 
  onClose, 
  imageUrl, 
  scores, 
  imageName 
}: CompositionScorePanelProps) {
  const [isAnimating, setIsAnimating] = useState(false);

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

  // Mock data for demonstration - replace with actual scores when available
  const mockScores: CompositionScore = {
    color: 85,
    lighting: 72,
    composition: 91,
    overall: 83
  };

  const displayScores = scores || mockScores;

  const CircularProgress = ({ value, label, size = "w-24 h-24" }: { 
    value: number; 
    label: string; 
    size?: string;
  }) => {
    const radius = 40;
    const circumference = 2 * Math.PI * radius;
    const strokeDasharray = circumference;
    const strokeDashoffset = circumference - (value / 100) * circumference;

    return (
      <div className="flex flex-col items-center space-y-2">
        <div className={`relative ${size}`}>
          <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
            {/* Background circle */}
            <circle
              cx="50"
              cy="50"
              r={radius}
              stroke="#e5e7eb"
              strokeWidth="8"
              fill="transparent"
            />
            {/* Progress circle */}
            <circle
              cx="50"
              cy="50"
              r={radius}
              stroke="#3b82f6"
              strokeWidth="8"
              fill="transparent"
              strokeDasharray={strokeDasharray}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              className="transition-all duration-1000 ease-out"
            />
          </svg>
          {/* Score text */}
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-lg font-bold text-gray-800">{value}%</span>
          </div>
        </div>
        <span className="text-sm font-medium text-gray-600 text-center">{label}</span>
      </div>
    );
  };

  const LinearProgress = ({ value, label }: { value: number; label: string }) => {
    return (
      <div className="w-full">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-700">{label}</span>
          <span className="text-sm font-bold text-gray-800">{value}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-4">
          <div 
            className="bg-gradient-to-r from-blue-500 to-blue-600 h-4 rounded-full transition-all duration-1000 ease-out"
            style={{ width: `${value}%` }}
          />
        </div>
      </div>
    );
  };

  return (
    <div 
      className={`fixed top-0 right-0 h-full w-1/2 bg-white shadow-2xl z-40 transition-transform duration-300 ease-in-out ${
        isAnimating ? 'translate-x-0' : 'translate-x-full'
      }`}
    >
      <div className="h-full overflow-y-auto p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-800">Composition Analysis</h2>
          <button
            onClick={handleClose}
            className="text-gray-500 hover:text-gray-700 transition-colors"
            aria-label="Close composition panel"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Image Display */}
        {imageUrl && (
          <div className="mb-6">
            <div className="relative rounded-lg overflow-hidden shadow-lg">
              <img 
                src={imageUrl} 
                alt={imageName || "Analyzed image"} 
                className="w-full h-auto object-cover"
              />
            </div>
            {imageName && (
              <p className="text-sm text-gray-600 mt-2 text-center">{imageName}</p>
            )}
          </div>
        )}

        {/* Overall Score Bar */}
        <div className="mb-8">
          <LinearProgress 
            value={displayScores.overall} 
            label="Overall Composition Score" 
          />
        </div>

        {/* Individual Score Circles */}
        <div className="space-y-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Individual Scores</h3>
          
          <div className="grid grid-cols-3 gap-6">
            <CircularProgress 
              value={displayScores.color} 
              label="Color" 
            />
            <CircularProgress 
              value={displayScores.lighting} 
              label="Lighting" 
            />
            <CircularProgress 
              value={displayScores.composition} 
              label="Composition" 
            />
          </div>
        </div>

        {/* Score Interpretation */}
        <div className="mt-8 p-4 bg-gray-50 rounded-lg">
          <h4 className="text-md font-semibold text-gray-800 mb-2">Score Interpretation</h4>
          <div className="space-y-2 text-sm text-gray-600">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span>90-100%: Excellent quality</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
              <span>70-89%: Good quality</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
              <span>50-69%: Fair quality</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-red-500 rounded-full"></div>
              <span>Below 50%: Needs improvement</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
