'use client';

import { useState, useEffect } from 'react';
import { ImageUpload } from './index';

export default function CollapsibleUploadPanel() {
  const [isOpen, setIsOpen] = useState(false);
  const [isAnimating, setIsAnimating] = useState(false);

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

    window.addEventListener('toggleUploadPanel', handleToggle);
    
    return () => {
      window.removeEventListener('toggleUploadPanel', handleToggle);
    };
  }, [isOpen]);

  const handleClose = () => {
    setIsAnimating(false);
    // Small delay to allow exit animation to complete
    setTimeout(() => setIsOpen(false), 300);
  };

  return (
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
  );
} 