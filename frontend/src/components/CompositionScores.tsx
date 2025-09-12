'use client';

import { CompositionScore } from '@/types/image';

interface CompositionScoresProps {
  scores?: CompositionScore;
  analysis?: string;
  isLoading?: boolean;
}

export default function CompositionScores({
  scores,
  analysis,
  isLoading = false
}: CompositionScoresProps) {
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

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center p-6">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mb-4"></div>
        <p className="text-gray-600">Loading image analysis...</p>
      </div>
    );
  }

  return (
    <div className="w-full">
      <div className="p-6">
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
            <div className="mt-8 p-4 bg-gray-100 rounded-lg">
              <h3 className="text-lg font-semibold text-gray-800 mb-3">Analysis</h3>
              <p className="text-gray-700 text-sm leading-relaxed">{analysis}</p>
            </div>
          )}
        </div>
    </div>
  );
}
