import axios from 'axios'

const API_BASE_URL = 'http://localhost:5000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 10000
})

export const sudokuApi = {
  // Get standard Sudoku puzzle
  async getSudokuPuzzle(difficulty = 'medium') {
    try {
      const response = await apiClient.get('/sudoku_puzzle', {
        params: { difficulty }
      })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to fetch puzzle')
    }
  },

  // Get hex Sudoku puzzle
  async getHexSudokuPuzzle(difficulty = 'medium') {
    try {
      const response = await apiClient.get('/hex_sudoku_puzzle', {
        params: { difficulty }
      })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to fetch hex puzzle')
    }
  },

  // Validate standard Sudoku solution
  async validateSudokuSolution(puzzleState, puzzleSolution) {
    try {
      const response = await apiClient.post('/sudoku_solution', {
        puzzle_state: puzzleState,
        puzzle_solution: puzzleSolution
      })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to validate solution')
    }
  },

  // Validate hex Sudoku solution
  async validateHexSudokuSolution(puzzleState, puzzleSolution) {
    try {
      const response = await apiClient.post('/hex_sudoku_solution', {
        puzzle_state: puzzleState,
        puzzle_solution: puzzleSolution
      })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to validate hex solution')
    }
  },

  // Get hint for standard Sudoku
  async getSudokuHint(puzzle) {
    try {
      const response = await apiClient.post('/sudoku_hint', {
        puzzle: puzzle
      })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get hint')
    }
  },

  // Get hint for hex Sudoku
  async getHexSudokuHint(puzzle) {
    try {
      const response = await apiClient.post('/hex_sudoku_hint', {
        puzzle: puzzle
      })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get hex hint')
    }
  }
}
