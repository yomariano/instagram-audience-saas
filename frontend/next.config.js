/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL || 'https://instagram-api.teabag.online'}/api/:path*`
      }
    ]
  }
}

module.exports = nextConfig