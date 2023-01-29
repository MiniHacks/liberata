/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  optimizeFonts: false,
  distDir: 'build',
  images:{
    unoptimized: true
  }
}

module.exports = nextConfig
