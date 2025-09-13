'use client';

import Image from 'next/image';
import { CompositionScore, ItemData } from '@/types/image';

interface UploadSummaryProps {
  imageUrl: string;
  scores?: CompositionScore;
  analysis?: string;
  items?: ItemData[];
  onViewFullAnalysis: () => void;
}

export default function UploadSummary({
  imageUrl,
  scores,
  analysis,
  onViewFullAnalysis
}: UploadSummaryProps) {
  // Helper function to safely parse scores with fallback
  const parseScore = (score: string | undefined): number => {
    if (!score) return 0;
    return parseInt(score, 10) || 0;
  };

  const getScoreColor = (value: number) => {
    if (value >= 80) return "#10b981"; // green-500
    if (value >= 60) return "#f59e0b"; // amber-500
    if (value >= 40) return "#f97316"; // orange-500
    return "#ef4444"; // red-500
  };

  const overallScore = Math.floor((parseScore(scores?.color) + parseScore(scores?.lighting) + parseScore(scores?.composition)) / 3);

  const CircularProgress = ({ value, size = "w-16 h-16" }: {
    value: number;
    size?: string;
  }) => {
    const radius = 20;
    const circumference = 2 * Math.PI * radius;
    const strokeDasharray = circumference;
    const strokeDashoffset = circumference - (value / 100) * circumference;
    const strokeColor = getScoreColor(value);

    return (
      <div className={`relative ${size}`}>
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 50 50">
          {/* Background circle */}
          <circle
            cx="25"
            cy="25"
            r={radius}
            stroke="#e5e7eb"
            strokeWidth="4"
            fill="transparent"
          />
          {/* Progress circle */}
          <circle
            cx="25"
            cy="25"
            r={radius}
            stroke={strokeColor}
            strokeWidth="4"
            fill="transparent"
            strokeDasharray={strokeDasharray}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        {/* Score text */}
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-2xl font-bold text-gray-800">{value}%</span>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-4">
      {/* Success Message */}
      <div className="bg-green-100 text-green-700 p-3 rounded-lg text-center">
        <p className="font-medium">Analysis Complete!</p>
      </div>

        {/* Image and Score Circle */}
        <div className="flex items-center justify-around">
        {/* Image Thumbnail */}
        <div className="flex-shrink-0">
          <img
            src={imageUrl}
            alt="Uploaded image"
            className="w-56 h-48 object-cover rounded-lg"
          />
        </div>

        {/* Overall Score Circle */}
        <div className="flex flex-col items-center space-y-2">
          <CircularProgress value={overallScore} size="w-36 h-36" />
        </div>
      </div>

      {/* Analysis Section */}
      {analysis && (
        <div className="bg-gray-100 rounded-lg p-4">
          <p className="text-sm text-gray-700 leading-relaxed line-clamp-4">
            {analysis}
          </p>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex space-x-3">
        <button
          onClick={onViewFullAnalysis}
          className="flex-1 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors text-sm font-medium"
        >
          View Full Analysis
        </button>
        <button
          onClick={() => window.dispatchEvent(new CustomEvent('toggleUploadPanel'))}
          className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm font-medium"
        >
          Close
        </button>
      </div>
    </div>
  );
}
