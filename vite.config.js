import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: '0.0.0.0',
    allowedHosts: [
      'localhost',
      '.preview.emergentagent.com',
      'c9d1bc23-80d8-46ce-ba5e-22ff1eab640a.preview.emergentagent.com'
    ]
  }
})
