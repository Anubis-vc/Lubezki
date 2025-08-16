"use client";
import { Image as ImageType } from "@/types/image";
import Image from "next/image";

interface ImageGalleryProps {
  images: ImageType[];
}

export default function ImageGallery({ images }: ImageGalleryProps) {
  return (
    <div className="space-y-6">
      {/* Image Grid */}
      <div className="grid grid-cols-5 gap-4">
        {images.map((image, index) => (
          <div
            key={index}
            className="group relative bg-white/5 rounded-lg overflow-hidden hover:bg-white/10 transition-all duration-300 hover:scale-105"
          >
            <div className="aspect-square relative">
              <Image
                src={image.thumbnail_image}
                width={image.thumbnail_width_px}
                height={image.thumbnail_height_px}
                alt={`Gallery image ${index + 1}`}
                className="w-full h-full object-cover"
              />

              <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                <div className="text-center text-white">
                  <p className="text-md text-gray-300">Click to view</p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
