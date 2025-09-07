import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";
import { componentTagger } from "lovable-tagger";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  server: {
    host: "::",
    port: 8081,
    proxy: {
      '/livekit': 'http://localhost:8000',
      '/tts': 'http://localhost:8000',
      '/stt': 'http://localhost:8000',
      '/recommendations': 'http://localhost:8000',
      '/consciousness': 'http://localhost:8000',
      // Proxy API endpoints under /api prefix to avoid conflicts with React routes
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
      // Proxy all backend API routes to FastAPI backend on port 8000
      '/mainza': 'http://localhost:8000',
      '/agent': 'http://localhost:8000',
    },
  },
  plugins: [
    react(),
    mode === 'development' &&
    componentTagger(),
  ].filter(Boolean),
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  define: {
    // Define environment variables for the frontend
    'import.meta.env.VITE_LIVEKIT_URL': JSON.stringify(process.env.VITE_LIVEKIT_URL || 'ws://localhost:7880'),
    'import.meta.env.VITE_API_URL': JSON.stringify(process.env.VITE_API_URL || 'http://localhost:8000'),
  },
}));
