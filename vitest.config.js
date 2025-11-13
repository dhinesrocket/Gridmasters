import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './frontend/src')
    }
  },
  test: {
    globals: true,
    environment: 'happy-dom',
    pool: 'forks',
    poolOptions: {
      forks: {
        singleFork: true
      }
    },
    include: ['tests/frontend/**/*.{test,spec}.{js,jsx,ts,tsx}']
  }
})
