export default function Loading() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-black mx-auto mb-4"></div>
        <h2 className="text-2xl font-semibold text-black mb-2">Loading Lubezki</h2>
        <p className="text-gray-300">Preparing your film composition analysis...</p>
      </div>
    </div>
  );
}