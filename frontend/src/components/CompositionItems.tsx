'use client';

import { ItemData } from '@/types/image';

interface CompositionItemsProps {
  items: ItemData[];
  isLoading?: boolean;
}

export default function CompositionItems({
  items,
  isLoading = false
}: CompositionItemsProps) {
  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center p-6">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mb-4"></div>
        <p className="text-gray-600">Loading items analysis...</p>
      </div>
    );
  }

  if (!items || items.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center p-6 text-gray-500">
        <svg className="w-16 h-16 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
        <p className="text-lg font-medium">No items detected</p>
        <p className="text-sm">The AI didn't identify any specific objects to analyze.</p>
      </div>
    );
  }

  return (
    <div className="w-full h-full">
      <div className="p-6 space-y-4">
        {items.map((item, index) => (
          <div
            key={item.item_id || index}
            className={`p-4 rounded-lg border-2 transition-all duration-200 ${
              item.is_positive
                ? 'border-green-200 bg-green-50 hover:bg-green-100'
                : 'border-red-200 bg-red-50 hover:bg-red-100'
            }`}
          >
            {/* Item Header */}
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-3">
                <h3 className="text-lg font-semibold text-gray-700">
                  {item.name}
                </h3>
              </div>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                item.is_positive
                  ? 'bg-green-100 text-green-800'
                  : 'bg-red-100 text-red-800'
              }`}>
                {item.is_positive ? 'Good' : 'Needs Improvement'}
              </span>
            </div>

            {/* Analysis */}
            <div>
              <p className="text-sm text-gray-700 leading-relaxed">
                {item.analysis}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
