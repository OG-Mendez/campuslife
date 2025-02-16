import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      // Ensure Vite resolves the Mapbox Geocoder CSS correctly
      'mapbox-gl-geocoder': path.resolve(__dirname, 'node_modules/@mapbox/mapbox-gl-geocoder'),
    },
  },
});
