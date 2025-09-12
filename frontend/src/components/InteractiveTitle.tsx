'use client';

export default function InteractiveTitle() {
  const handleUploadClick = () => {
    const event = new CustomEvent('toggleUploadPanel');
    window.dispatchEvent(event);
  };

  return (
    <div className="flex flex-row items-center justify-between border-b-1 border-gray-400 pb-4">
      <div className="flex flex-col items-start gap-2">
        <h1 className="text-5xl font-bold text-gray-800">Lubezki</h1>
        <h2 className="text-2xl font-bold text-gray-400">Image Analysis</h2>
      </div>
      <button
        onClick={handleUploadClick}
        className="text-5xl cursor-pointer border-2 border-dashed border-red-500 rounded-2xl p-4 hover:border-green-500 hover:scale-110 transition-transform duration-200"
        aria-label="Open upload panel"
      >
        📸
      </button>
    </div>
  );
} 