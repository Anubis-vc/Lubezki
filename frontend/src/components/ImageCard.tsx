"use client";
import { Image as ImageType } from "@/types/image";
import Image from "next/image";

interface ImageCardProps {
  image: ImageType;
  onClick: (image: ImageType) => void;
}

export default function ImageCard({ image, onClick }: ImageCardProps) {
  return (
    <div
      className="group relative bg-white/5 rounded-lg overflow-hidden hover:bg-white/10 transition-all duration-300 hover:scale-105 cursor-pointer"
      onClick={() => onClick(image)}
    >
      <div className="aspect-square relative">
        <Image
          src={image.thumbnail_image}
          width={image.thumbnail_width_px}
          height={image.thumbnail_height_px}
          alt={`Gallery image`}
          className="w-full h-full object-cover"
        />

        <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
          <div className="text-center text-white">
            <p className="text-md text-gray-300">Click to analyze</p>
          </div>
        </div>
      </div>
    </div>
  );
}
