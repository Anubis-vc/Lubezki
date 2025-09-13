import { ImageWithItemsResponse } from '@/types/image';

const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://lubezki.onrender.com';

export async function fetchImageData(imageId: string): Promise<ImageWithItemsResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/basic/${imageId}`);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch image data: ${response.statusText}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching image data:', error);
    throw error;
  }
}
