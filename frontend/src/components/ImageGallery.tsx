"use client";
import { useState } from "react";
import { Image as ImageType, ImageData } from "@/types/image";
import ImageCard from "./ImageCard";
import CompositionScorePanel from "./CompositionScorePanel";
import { fetchImageData } from "@/services/api";

interface ImageGalleryProps {
  images: ImageType[];
}

export default function ImageGallery({ images }: ImageGalleryProps) {
  const [selectedImage, setSelectedImage] = useState<ImageType | null>(null);
  const [fullImageData, setFullImageData] = useState<ImageData | null>(null);
  const [isPanelOpen, setIsPanelOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleImageClick = async (image: ImageType) => {
    if (!image.image_id) {
      console.error('No image ID available');
      return;
    }

    setSelectedImage(image);
    setIsLoading(true);
    setIsPanelOpen(true);

    try {
      const data = await fetchImageData(image.image_id);
      setFullImageData(data);
    } catch (error) {
      console.error('Failed to fetch image data:', error);
      // Still show the panel but with limited data
    } finally {
      setIsLoading(false);
    }
  };

  const handleClosePanel = () => {
    setIsPanelOpen(false);
    setSelectedImage(null);
    setFullImageData(null);
  };

  return (
    <>
      <div className="space-y-6">
        {/* Image Grid */}
        <div className="grid grid-cols-5 gap-4">
          {images.map((image, index) => (
            <ImageCard
              key={index}
              image={image}
              onClick={handleImageClick}
            />
          ))}
        </div>
      </div>

      {/* Composition Score Panel */}
      <CompositionScorePanel
        isOpen={isPanelOpen}
        onClose={handleClosePanel}
        imageUrl={selectedImage?.base_image}
        imageName={fullImageData?.original_name || selectedImage?.base_image?.split('/').pop()}
        scores={fullImageData?.score || selectedImage?.scores}
        analysis={fullImageData?.analysis}
        isLoading={isLoading}
      />
    </>
  );
}
