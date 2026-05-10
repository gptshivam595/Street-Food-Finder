import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  images: { remotePatterns: [] },
  webpack: (config) => {
    config.resolve.fallback = { fs: false };
    return config;
  },
};

export default nextConfig;
