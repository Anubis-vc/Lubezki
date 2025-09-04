"use client";
import { useState } from "react";
import { Image as ImageType } from "@/types/image";
import ImageCard from "./ImageCard";
import CompositionScorePanel from "./CompositionScorePanel";

interface ImageGalleryProps {
  images: ImageType[];
}

export default function ImageGallery({ images }: ImageGalleryProps) {
  const [selectedImage, setSelectedImage] = useState<ImageType | null>(null);
  const [isPanelOpen, setIsPanelOpen] = useState(false);

  const handleImageClick = (image: ImageType) => {
    setSelectedImage(image);
    setIsPanelOpen(true);
  };

  const handleClosePanel = () => {
    setIsPanelOpen(false);
    setSelectedImage(null);
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
        imageName={selectedImage?.base_image?.split('/').pop()}
        scores={selectedImage?.scores}
      />
    </>
  );
}
