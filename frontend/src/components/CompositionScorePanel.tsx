'use client';

import { useState, useEffect } from 'react';
import { CompositionScore } from '@/types/image';

interface CompositionScorePanelProps {
  isOpen: boolean;
  onClose: () => void;
  imageUrl?: string;
  scores?: CompositionScore;
  imageName?: string;
  analysis?: string;
  isLoading?: boolean;
}

export default function CompositionScorePanel({
  isOpen,
  onClose,
  imageUrl,
  scores,
  imageName,
  analysis,
  isLoading = false
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

  const getScoreColor = (value: number) => {
    if (value >= 80) return "#10b981"; // green-500
    if (value >= 60) return "#f59e0b"; // amber-500
    if (value >= 40) return "#f97316"; // orange-500
    return "#ef4444"; // red-500
  };

  // Helper function to safely parse scores with fallback
  const parseScore = (score: string | undefined): number => {
    if (!score) return 0;
    return parseInt(score, 10) || 0;
  };

  const CircularProgress = ({ value, label, size = "w-24 h-24" }: {
    value: number;
    label: string;
    size?: string;
  }) => {
    const radius = 40;
    const circumference = 2 * Math.PI * radius;
    const strokeDasharray = circumference;
    const strokeDashoffset = circumference - (value / 100) * circumference;
    const strokeColor = getScoreColor(value);

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
              stroke={strokeColor}
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

  return (
    <div
      className={`fixed inset-0 bg-white z-40 transition-transform duration-300 ease-in-out ${isAnimating ? 'translate-x-0' : 'translate-x-full'
        }`}
    >
      {/* Close Button */}
      <button
        onClick={handleClose}
        className="absolute top-4 right-4 z-50 text-gray-500 hover:text-gray-700 transition-colors rounded-full p-2"
        aria-label="Close composition panel"
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <div className="h-full flex">
        {/* Left Section - Image Display (2/3) */}
        <div className="w-2/3 flex items-center justify-center p-6">
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

        {/* Right Section - Scores (1/3) */}
        <div className="w-1/3 border-l border-gray-200 flex items-center justify-center">
          <div className="p-6 w-full">
            {isLoading ? (
              <div className="flex flex-col items-center justify-center h-full">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mb-4"></div>
                <p className="text-gray-600">Loading image analysis...</p>
              </div>
            ) : (
              <>
                {/* Overall Score Circle */}
                <div className="flex justify-center mb-8">
                  <CircularProgress
                    value={Math.floor((parseScore(scores?.color) + parseScore(scores?.lighting) + parseScore(scores?.composition)) / 3)}
                    label=""
                    size="w-40 h-40"
                  />
                </div>

                {/* Individual Score Circles */}
                <div className="space-y-6">
                  <div className="flex justify-between space-x-4">
                    <CircularProgress
                      value={parseScore(scores?.color)}
                      label="Color"
                    />
                    <CircularProgress
                      value={parseScore(scores?.lighting)}
                      label="Lighting"
                    />
                    <CircularProgress
                      value={parseScore(scores?.composition)}
                      label="Composition"
                    />
                  </div>
                </div>

                {/* Analysis Section */}
                {analysis && (
                  <div className="mt-8 p-4 bg-gray-50 rounded-lg">
                    <h3 className="text-lg font-semibold text-gray-800 mb-3">Analysis</h3>
                    <p className="text-gray-700 text-sm leading-relaxed">{analysis}</p>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
