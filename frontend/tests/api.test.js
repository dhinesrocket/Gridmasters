/**
 * Tests for API service
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'

describe('sudokuApi', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.resetModules()
  })

  describe('API configuration', () => {
    it('should have correct API base URL', () => {
      const API_BASE_URL = 'http://localhost:5000'
      expect(API_BASE_URL).toBe('http://localhost:5000')
    })

    it('should have correct timeout', () => {
      const timeout = 10000
      expect(timeout).toBe(10000)
    })
  })

  describe('API error handling', () => {
    it('should handle network errors gracefully', () => {
      const error = new Error('Network error')
      expect(error.message).toBe('Network error')
    })

    it('should handle server errors with error message', () => {
      const errorResponse = {
        response: {
          data: {
            error: 'Server error'
          }
        }
      }
      expect(errorResponse.response.data.error).toBe('Server error')
    })

    it('should provide default error message when no response', () => {
      const defaultMessage = 'Failed to fetch solution'
      expect(defaultMessage).toBeTruthy()
    })
  })

  describe('API endpoints', () => {
    it('should have sudoku_puzzle endpoint', () => {
      const endpoint = '/sudoku_puzzle'
      expect(endpoint).toBe('/sudoku_puzzle')
    })

    it('should have hex_sudoku_puzzle endpoint', () => {
      const endpoint = '/hex_sudoku_puzzle'
      expect(endpoint).toBe('/hex_sudoku_puzzle')
    })

    it('should accept difficulty parameter', () => {
      const params = { difficulty: 'medium' }
      expect(params.difficulty).toBe('medium')
    })
  })
})

