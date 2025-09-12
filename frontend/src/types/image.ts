export interface ImageData {
  original_name: string;
  size_bytes: number;
  mime_type: string;
  width_px: number;
  height_px: number;
  is_analysis_complete: boolean;
  score?: CompositionScore;
  analysis?: string;
}

export interface BoundingBox {
  y_min: number;
  y_max: number;
  x_min: number;
  x_max: number;
}

export interface ItemData {
  item_id: string;
  image_id: string;
  name: string;
  bounding_box: BoundingBox;
  analysis: string;
  is_positive: boolean;
}

export interface ImageWithItemsResponse {
  image: ImageData;
  items: ItemData[];
}

export interface CompositionScore {
  color: string;
  lighting: string;
  composition: string;
}

export interface Image {
  base_image: string;
  thumbnail_image: string;
  height_px: number;
  width_px: number;
  thumbnail_height_px: number;
  thumbnail_width_px: number;
  scores?: CompositionScore;
  image_id: string;
}

export interface UploadResponse {
  message: string;
  image_id?: string;
}

export interface GalleryResponse {
  images: Image[];
  total: number;
} 