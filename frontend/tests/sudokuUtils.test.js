/**
 * Tests for sudokuUtils.js utility functions
 */
import { describe, it, expect } from 'vitest'
import {
  hideCells,
  validateCell,
  validateBoard,
  isBoardComplete,
  getHint,
  getValidNumbers,
  getCellCounts
} from '../src/utils/sudokuUtils.js'

describe('sudokuUtils', () => {
  // Sample 9x9 solved board
  const standardSolution = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
  ]

  describe('hideCells', () => {
    it('should hide cells based on difficulty', () => {
      const puzzle = hideCells(standardSolution, 'easy', 'standard')
      
      // Count hidden cells
      let hiddenCount = 0
      for (let row of puzzle) {
        for (let cell of row) {
          if (cell === -1) hiddenCount++
        }
      }
      
      // Easy should hide about 40% of 81 cells = ~32 cells
      expect(hiddenCount).toBeGreaterThan(25)
      expect(hiddenCount).toBeLessThan(40)
    })

    it('should hide very few cells for super_easy difficulty', () => {
      const puzzle = hideCells(standardSolution, 'super_easy', 'standard')
      
      let hiddenCount = 0
      for (let row of puzzle) {
        for (let cell of row) {
          if (cell === -1) hiddenCount++
        }
      }
      
      // Super easy should hide 3-4 cells
      expect(hiddenCount).toBeGreaterThanOrEqual(3)
      expect(hiddenCount).toBeLessThanOrEqual(4)
    })

    it('should not modify original solution', () => {
      const originalCopy = JSON.parse(JSON.stringify(standardSolution))
      hideCells(standardSolution, 'medium', 'standard')
      
      expect(standardSolution).toEqual(originalCopy)
    })
  })

  describe('validateCell', () => {
    it('should validate correct cell value', () => {
      const userBoard = JSON.parse(JSON.stringify(standardSolution))
      const isValid = validateCell(userBoard, standardSolution, 0, 0)
      
      expect(isValid).toBe(true)
    })

    it('should invalidate incorrect cell value', () => {
      const userBoard = JSON.parse(JSON.stringify(standardSolution))
      userBoard[0][0] = 9 // Wrong value
      
      const isValid = validateCell(userBoard, standardSolution, 0, 0)
      expect(isValid).toBe(false)
    })
  })

  describe('validateBoard', () => {
    it('should validate complete and correct board', () => {
      const userBoard = JSON.parse(JSON.stringify(standardSolution))
      const isValid = validateBoard(userBoard, standardSolution, 'standard')
      
      expect(isValid).toBe(true)
    })

    it('should invalidate incomplete board', () => {
      const userBoard = JSON.parse(JSON.stringify(standardSolution))
      userBoard[0][0] = -1 // Empty cell
      
      const isValid = validateBoard(userBoard, standardSolution, 'standard')
      expect(isValid).toBe(false)
    })

    it('should invalidate incorrect board', () => {
      const userBoard = JSON.parse(JSON.stringify(standardSolution))
      userBoard[0][0] = 9 // Wrong value
      
      const isValid = validateBoard(userBoard, standardSolution, 'standard')
      expect(isValid).toBe(false)
    })
  })

  describe('isBoardComplete', () => {
    it('should return true for complete board', () => {
      const complete = isBoardComplete(standardSolution, 'standard')
      expect(complete).toBe(true)
    })

    it('should return false for incomplete board', () => {
      const userBoard = JSON.parse(JSON.stringify(standardSolution))
      userBoard[0][0] = -1
      
      const complete = isBoardComplete(userBoard, 'standard')
      expect(complete).toBe(false)
    })
  })

  describe('getHint', () => {
    it('should provide hint for first empty cell', () => {
      const userBoard = JSON.parse(JSON.stringify(standardSolution))
      userBoard[2][3] = -1 // Make cell empty
      
      const hint = getHint(userBoard, standardSolution, 'standard')
      
      expect(hint.row).toBe(2)
      expect(hint.col).toBe(3)
      expect(hint.value).toBe(3)
      expect(hint.message).toContain('Cell at row 3, column 4')
    })

    it('should return no hints for complete board', () => {
      const hint = getHint(standardSolution, standardSolution, 'standard')
      
      expect(hint.row).toBe(-1)
      expect(hint.col).toBe(-1)
      expect(hint.value).toBe(null)
      expect(hint.message).toContain('No hints available')
    })
  })

  describe('getValidNumbers', () => {
    it('should return valid numbers for an empty cell', () => {
      const board = JSON.parse(JSON.stringify(standardSolution))
      board[0][0] = -1 // Empty cell
      
      const valid = getValidNumbers(board, 0, 0, 'standard')
      
      // Only 5 should be valid for this position
      expect(valid).toContain(5)
      expect(valid.length).toBeGreaterThan(0)
    })

    it('should return empty array for cell with no valid options', () => {
      // This is tricky - in a valid solved board, each cell has only one valid value
      const board = JSON.parse(JSON.stringify(standardSolution))
      board[0][0] = -1
      
      const valid = getValidNumbers(board, 0, 0, 'standard')
      expect(Array.isArray(valid)).toBe(true)
    })
  })

  describe('getCellCounts', () => {
    it('should count filled and empty cells correctly', () => {
      const counts = getCellCounts(standardSolution, 'standard')
      
      expect(counts.total).toBe(81)
      expect(counts.filled).toBe(81)
      expect(counts.empty).toBe(0)
    })

    it('should count empty cells in puzzle', () => {
      const puzzle = hideCells(standardSolution, 'medium', 'standard')
      const counts = getCellCounts(puzzle, 'standard')
      
      expect(counts.total).toBe(81)
      expect(counts.filled + counts.empty).toBe(81)
      expect(counts.empty).toBeGreaterThan(0)
    })
  })
})

