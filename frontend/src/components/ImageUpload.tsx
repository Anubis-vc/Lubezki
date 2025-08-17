'use client';

import { useState } from 'react';

export default function ImageUpload() {
  const [isDragOver, setIsDragOver] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string>('');

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleFileUpload(files[0]);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFileUpload(files[0]);
    }
  };

  const handleFileUpload = async (file: File) => {
    if (!file.type.startsWith('image/')) {
      setUploadStatus('Please select an image file');
      return;
    }

    if (file.size > 25 * 1024 * 1024) {
      setUploadStatus('File size must be less than 25MB');
      return;
    }

    setIsUploading(true);
    setUploadStatus('Uploading...');

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/api/v1/basic/upload-for-gallery`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const data = await response.json();
      setUploadStatus(data.message);
      
      // Clear status after 5 seconds
      setTimeout(() => setUploadStatus(''), 5000);
    } catch (error) {
      setUploadStatus('Upload failed. Please try again.');
      console.error('Upload error:', error);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="h-3/4 flex flex-col space-y-6">
      <div
        className={`flex-1 border-2 border-dashed rounded-xl p-8 text-center transition-colors flex flex-col items-center justify-center ${
          isDragOver
            ? 'border-green-400 bg-green-400/10'
            : 'border-red-300 hover:border-red-400'
        }`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <div className="space-y-4">
          <div className="text-6xl text-gray-400">🏞️</div>
          <div>
            <p className="text-lg font-medium text-gray-700">
              Drag & drop your image here
            </p>
          </div>
          <input
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
            className="hidden"
            id="file-upload"
            disabled={isUploading}
          />
          <label
            htmlFor="file-upload"
            className="inline-flex items-center px-4 py-2 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isUploading ? 'Uploading...' : 'Choose File'}
          </label>
        </div>
      </div>

      {/* Upload Status */}
      {uploadStatus && (
        <div className={`text-center p-3 rounded-lg ${
          uploadStatus.includes('successful') 
            ? 'bg-green-100 text-green-700' 
            : uploadStatus.includes('failed') || uploadStatus.includes('Please')
            ? 'bg-red-100 text-red-700'
            : 'bg-blue-100 text-blue-700'
        }`}>
          {uploadStatus}
        </div>
      )}

      {/* File Requirements */}
      <div className="bg-gray-50 rounded-lg p-4">
        <h3 className="font-medium text-gray-700 mb-2">File Requirements:</h3>
        <ul className="text-sm text-gray-600 space-y-1">
          <li>• Supported formats: JPEG, PNG, RAW</li>
          <li>• Maximum file size: 25MB</li>
        </ul>
      </div>
    </div>
  );
} 