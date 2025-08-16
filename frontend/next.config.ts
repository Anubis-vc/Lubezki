import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      new URL('http://localhost/**'),
      new URL('https://public-lubezki-images.s3.amazonaws.com/**'),
    ],
  },
  experimental: {
    optimizePackageImports: ['react', 'react-dom'],
  },
  // Enable static generation for better performance
  // output: 'export', // TODO: enable this for prod
  // Optimize for static rendering
  staticPageGenerationTimeout: 120,
  // Enable incremental static regeneration
  trailingSlash: true,
};

export default nextConfig;
