/**
 * Sudoku utility functions for validation and game logic.
 * Frontend handles all validation since backend only provides complete solutions.
 */

/**
 * Hide cells in a complete solution based on difficulty level
 * @param {Array} solution - Complete solved Sudoku board
 * @param {string} difficulty - 'easy', 'medium', or 'hard'
 * @param {string} gameMode - 'standard' or 'hex'
 * @returns {Array} Puzzle with hidden cells (0 for standard, '0' for hex)
 */
export function hideCells(solution, difficulty, gameMode) {
  const size = solution.length
  const emptyValue = -1  // Use -1 for empty cells in both modes
  
  // Calculate number of cells to hide based on difficulty
  let cellsToHide
  
  if (difficulty === 'super_easy') {
    // Super easy: hide only 3-4 cells
    cellsToHide = Math.floor(Math.random() * 2) + 3 // Random between 3-4
  } else {
    const removalRates = {
      easy: 0.4,   // 40% hidden
      medium: 0.5, // 50% hidden
      hard: 0.6    // 60% hidden
    }
    
    const removalRate = removalRates[difficulty] || removalRates.medium
    const totalCells = size * size
    cellsToHide = Math.floor(totalCells * removalRate)
  }
  
  // Create a copy of the solution
  const puzzle = JSON.parse(JSON.stringify(solution))
  
  // Generate random positions to hide
  const positions = []
  for (let row = 0; row < size; row++) {
    for (let col = 0; col < size; col++) {
      positions.push({ row, col })
    }
  }
  
  // Shuffle positions randomly
  for (let i = positions.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [positions[i], positions[j]] = [positions[j], positions[i]]
  }
  
  // Hide the first N cells
  for (let i = 0; i < cellsToHide; i++) {
    const { row, col } = positions[i]
    puzzle[row][col] = emptyValue
  }
  
  return puzzle
}

/**
 * Validate if a cell value is correct
 * @param {Array} userBoard - Current user's board
 * @param {Array} solution - Complete solution
 * @param {number} row - Row index
 * @param {number} col - Column index
 * @returns {boolean} True if cell is correct
 */
export function validateCell(userBoard, solution, row, col) {
  return userBoard[row][col] === solution[row][col]
}

/**
 * Validate the entire board against the solution
 * @param {Array} userBoard - Current user's board
 * @param {Array} solution - Complete solution
 * @param {string} gameMode - 'standard' or 'hex'
 * @returns {boolean} True if all filled cells are correct and board is complete
 */
export function validateBoard(userBoard, solution, gameMode) {
  const emptyValue = -1  // Use -1 for empty cells
  
  for (let row = 0; row < userBoard.length; row++) {
    for (let col = 0; col < userBoard[row].length; col++) {
      // Check if cell is empty
      if (userBoard[row][col] === emptyValue) {
        return false // Board is not complete
      }
      // Check if filled cell matches solution
      if (userBoard[row][col] !== solution[row][col]) {
        return false // Cell is incorrect
      }
    }
  }
  
  return true // All cells are filled and correct
}

/**
 * Check if the board is completely filled
 * @param {Array} board - Current board
 * @param {string} gameMode - 'standard' or 'hex'
 * @returns {boolean} True if no empty cells
 */
export function isBoardComplete(board, gameMode) {
  const emptyValue = -1  // Use -1 for empty cells
  
  for (let row = 0; row < board.length; row++) {
    for (let col = 0; col < board[row].length; col++) {
      if (board[row][col] === emptyValue) {
        return false
      }
    }
  }
  
  return true
}

/**
 * Get a hint by finding the first empty cell and revealing its value
 * @param {Array} userBoard - Current user's board
 * @param {Array} solution - Complete solution
 * @param {string} gameMode - 'standard' or 'hex'
 * @returns {Object} Hint object with row, col, value, and message
 */
export function getHint(userBoard, solution, gameMode) {
  const emptyValue = -1  // Use -1 for empty cells
  
  // Find first empty cell
  for (let row = 0; row < userBoard.length; row++) {
    for (let col = 0; col < userBoard[row].length; col++) {
      if (userBoard[row][col] === emptyValue) {
        const value = solution[row][col]
        return {
          row,
          col,
          value,
          message: `Cell at row ${row + 1}, column ${col + 1} should be ${value}`
        }
      }
    }
  }
  
  // No empty cells found
  return {
    row: -1,
    col: -1,
    value: null,
    message: 'No hints available - all cells are filled!'
  }
}

/**
 * Get valid numbers for a specific cell (for advanced hints)
 * @param {Array} board - Current board
 * @param {number} row - Row index
 * @param {number} col - Column index
 * @param {string} gameMode - 'standard' or 'hex'
 * @returns {Array} Array of valid values for the cell
 */
export function getValidNumbers(board, row, col, gameMode) {
  const size = board.length
  const boxSize = Math.sqrt(size)
  const valid = new Set()
  
  // Generate all possible values based on game mode
  if (gameMode === 'hex') {
    for (let i = 0; i <= 15; i++) {
      valid.add(i.toString(16).toUpperCase())
    }
  } else {
    for (let i = 1; i <= 9; i++) {
      valid.add(i)
    }
  }
  
  // Remove values in the same row
  for (let c = 0; c < size; c++) {
    valid.delete(board[row][c])
  }
  
  // Remove values in the same column
  for (let r = 0; r < size; r++) {
    valid.delete(board[r][col])
  }
  
  // Remove values in the same box
  const boxRow = Math.floor(row / boxSize) * boxSize
  const boxCol = Math.floor(col / boxSize) * boxSize
  for (let r = boxRow; r < boxRow + boxSize; r++) {
    for (let c = boxCol; c < boxCol + boxSize; c++) {
      valid.delete(board[r][c])
    }
  }
  
  // Remove empty value
  const emptyValue = -1  // Use -1 for empty cells
  valid.delete(emptyValue)
  
  return Array.from(valid).sort()
}

/**
 * Count how many cells are filled
 * @param {Array} board - Current board
 * @param {string} gameMode - 'standard' or 'hex'
 * @returns {Object} Object with filled and total counts
 */
export function getCellCounts(board, gameMode) {
  const emptyValue = -1  // Use -1 for empty cells
  const size = board.length
  const total = size * size
  let filled = 0
  
  for (let row = 0; row < size; row++) {
    for (let col = 0; col < board[row].length; col++) {
      if (board[row][col] !== emptyValue) {
        filled++
      }
    }
  }
  
  return { filled, total, empty: total - filled }
}
