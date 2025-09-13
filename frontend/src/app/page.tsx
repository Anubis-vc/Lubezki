import { ImageGallery, CollapsibleUploadPanel, InteractiveTitle } from '@/components';
import { Image } from '@/types/image';

// Cache the fetch request with ISR
async function getImages(): Promise<Image[]> {
  try {
    const response = await fetch(`${process.env.BACKEND_URL || 'https://lubezki.onrender.com'}/api/v1/basic/`, {
      next: { revalidate: 300 } // ISR: revalidate every hour
    });
    
    if (!response.ok) {
      console.warn('Backend not available during build, returning empty array');
      return [];
    }
    
    const data = await response.json();
    return data.images || [];
  } catch (error) {
    console.warn('Failed to fetch gallery data during build:', error);
    return [];
  }
}

export default async function Home() {
  const images = await getImages();

  return (
    <main className="min-h-screen max-h-screen relative">
      {/* Title and Upload Icon */}
      <div className="container mx-auto px-4 py-8">
        <InteractiveTitle />
      </div>

      <CollapsibleUploadPanel />

      {/* Gallery Container */}
      <div className="container mx-auto px-4 py-5">
        <ImageGallery images={images} />
      </div>
    </main>
  );
}
