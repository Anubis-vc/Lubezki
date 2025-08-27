'use client';

import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center max-w-md mx-auto px-4">
        <div className="text-6xl text-red-400 mb-4">⚠️</div>
        <h2 className="text-2xl font-semibold text-black mb-4">Something went wrong!</h2>
        <p className="text-gray-500 mb-6">
          We encountered an error while loading the page. Please try again or contact support if the problem persists.
        </p>
        <div className="space-x-4">
          <button
            onClick={reset}
            className="px-6 py-3 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors"
          >
            Try again
          </button>
          <button
            onClick={() => window.location.href = '/'}
            className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
          >
            Go home
          </button>
        </div>
      </div>
    </div>
  );
} 