/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  // Optimize for production
  swcMinify: true,
  compress: true,
  // Exclude unnecessary files from build
  experimental: {
    outputFileTracingExcludes: {
      '*': [
        'node_modules/@swc/core-linux-x64-gnu',
        'node_modules/@swc/core-linux-x64-musl',
        'node_modules/@swc/core-darwin-x64',
        'node_modules/@swc/core-darwin-arm64',
        'node_modules/@swc/core-win32-x64-msvc',
        'node_modules/@esbuild/**',
        'node_modules/esbuild/**',
      ],
    },
  },
  async rewrites() {
    // In production, API calls go directly to the backend
    // In development, proxy to localhost
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    
    // Only proxy in development
    if (process.env.NODE_ENV === 'development') {
      return [
        {
          source: '/api/:path*',
          destination: `${apiUrl}/api/:path*`,
        },
      ];
    }
    
    return [];
  },
}

module.exports = nextConfig

