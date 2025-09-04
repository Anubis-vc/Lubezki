export interface ImageData {
  url: string;
  thumbnail_url?: string;
  original_name: string;
  size_bytes: number;
  mime_type: string;
  width_px: number;
  height_px: number;
  is_analysis_complete: boolean;
  score?: Record<string, any>;
  analysis?: string;
  created_at: string;
  updated_at: string;
  status: string;
}

export interface CompositionScore {
  color: number;
  lighting: number;
  composition: number;
  overall: number;
}

export interface Image {
  base_image: string;
  thumbnail_image: string;
  height_px: number;
  width_px: number;
  thumbnail_height_px: number;
  thumbnail_width_px: number;
  scores?: CompositionScore;
}

export interface UploadResponse {
  message: string;
  image_id?: string;
}

export interface GalleryResponse {
  images: Image[];
  total: number;
} 