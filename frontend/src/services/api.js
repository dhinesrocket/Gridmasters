import axios from 'axios'
import { getHint } from '../utils/sudokuUtils'

const API_BASE_URL = 'http://localhost:5000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 10000
})

export const sudokuApi = {
  // Get complete standard Sudoku solution
  async getSudokuPuzzle(difficulty = 'medium') {
    try {
      const response = await apiClient.get('/sudoku_puzzle', {
        params: { difficulty }
      })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to fetch solution')
    }
  },

  // Get complete hex Sudoku solution
  async getHexSudokuPuzzle(difficulty = 'medium') {
    try {
      const response = await apiClient.get('/hex_sudoku_puzzle', {
        params: { difficulty }
      })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to fetch hex solution')
    }
  },

  async getHint(number) {
    try {
      const response = await apiClient.get('/hint', {
        params: { number }
      })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to fetch hint')
    }

  }
}
