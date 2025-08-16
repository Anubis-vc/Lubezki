import { ImageGallery } from '@/components';
import { Image } from '@/types/image';

// Cache the fetch request with ISR
async function getImages(): Promise<Image[]> {
  const response = await fetch(`${process.env.BACKEND_URL || 'http://localhost:8000'}/api/v1/basic/`, {
    next: { revalidate: 3600 } // ISR: revalidate every hour
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch gallery data');
  }
  
  const data = await response.json();
  return data.images || [];
}

export default async function Home() {
  const images = await getImages();

  return (
    <main className="min-h-screen">

      <div className="container mx-auto px-4 py-8">
        <ImageGallery images={images} />
      </div>
    
    </main>
  );
}
