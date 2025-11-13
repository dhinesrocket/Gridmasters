import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      '/sudoku_puzzle': 'http://localhost:5000',
      '/hex_sudoku_puzzle': 'http://localhost:5000',
      '/sudoku_solution': 'http://localhost:5000',
      '/hex_sudoku_solution': 'http://localhost:5000',
      '/sudoku_hint': 'http://localhost:5000',
      '/hex_sudoku_hint': 'http://localhost:5000',
    }
  },
  test: {
    globals: true,
    environment: 'happy-dom',
    pool: 'vmThreads',
    poolOptions: {
      vmThreads: {
        singleThread: true
      }
    }
  }
})
