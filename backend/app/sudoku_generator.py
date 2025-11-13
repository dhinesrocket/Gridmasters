import random
import copy

class SudokuGenerator:
    """Generate Sudoku puzzles for both standard (1-9) and hex (0-F) variants."""

    def __init__(self, size=9):
        """
        Initialize generator.
        Args:
            size: Board size (9 for standard, 16 for hex)
        """

        self.size = size
        self.box_size = int(size ** 0.5)

    def generate_puzzle(self, difficulty='medium'):  # pylint: disable=unused-argument
        """
        Generate a complete Sudoku solution.
        Args:
            difficulty: 'easy', 'medium', or 'hard' (kept for API compatibility, not used)
        Returns:
            2D list representing the complete solved board
        """
        # Create and return a complete solved board
        # Frontend will handle removing numbers based on difficulty
        board = self._create_solved_board()
        return board
    def _create_solved_board(self):
        """Create a completely solved Sudoku board."""
        max_attempts = 100
        for _ in range(max_attempts):
            board = [[0 for _ in range(self.size)] for _ in range(self.size)]
            if self._fill_board(board):
                return board
        # If all attempts fail, raise an error
        raise RuntimeError(f"Failed to generate valid Sudoku board after {max_attempts} attempts")

    def _fill_board(self, board, row=0, col=0):
        """Recursively fill the board using backtracking."""
        if row == self.size:
            return True
        next_row, next_col = (row, col + 1) if col + 1 < self.size else (row + 1, 0)
        numbers = list(range(1, self.size + 1))
        random.shuffle(numbers)
        for num in numbers:
            if self._is_valid(board, row, col, num):
                board[row][col] = num
                if self._fill_board(board, next_row, next_col):
                    return True
                board[row][col] = 0
        return False

    def _is_valid(self, board, row, col, num):
        """Check if placing num at (row, col) is valid."""
        # Check row
        if num in board[row]:
            return False
        # Check column
        if num in [board[r][col] for r in range(self.size)]:
            return False
        # Check box
        box_row, box_col = (row // self.box_size) * self.box_size, (col // self.box_size) * self.box_size
        for r in range(box_row, box_row + self.box_size):
            for c in range(box_col, box_col + self.box_size):
                if board[r][c] == num:
                    return False
        return True

    def _remove_numbers(self, board, difficulty):
        """Remove numbers from solved board based on difficulty."""
        puzzle = copy.deepcopy(board)
        # Define removal counts based on difficulty
        removal_map = {
            'easy': int(self.size * self.size * 0.4),    # 40% removed
            'medium': int(self.size * self.size * 0.5),  # 50% removed
            'hard': int(self.size * self.size * 0.6)     # 60% removed
        }
        removals = removal_map.get(difficulty, removal_map['medium'])
        positions = [(r, c) for r in range(self.size) for c in range(self.size)]
        random.shuffle(positions)
        for i in range(removals):
            row, col = positions[i]
            puzzle[row][col] = 0
        return puzzle

# ...existing code...
class HexSudokuGenerator(SudokuGenerator):
    """Generator for 16x16 hexadecimal Sudoku puzzles."""

    def __init__(self):
        """Initialize hex sudoku generator."""
        super().__init__(size=16)

    def _fill_board(self, board, row=0, col=0):
        """Recursively fill the board using values 0-15 (displayed as 0-9, A-F).

        Optimized for 16x16 boards to avoid getting stuck in backtracking.
        Uses constraint propagation to limit search space.
        """
        if row == self.size:
            return True
        next_row, next_col = (row, col + 1) if col + 1 < self.size else (row + 1, 0)

        # Get valid numbers for this position (constraint propagation)
        valid_nums = self._get_valid_numbers_hex(board, row, col)
        if not valid_nums:
            return False

        # Shuffle for randomness
        random.shuffle(valid_nums)

        for num in valid_nums:
            board[row][col] = num
            if self._fill_board(board, next_row, next_col):
                return True
            board[row][col] = -1  # Use -1 for empty instead of 0
        return False

    def _get_valid_numbers_hex(self, board, row, col):
        """Get list of valid numbers for position using constraint propagation."""
        valid = []
        for num in range(0, 16):
            if self._is_valid_hex(board, row, col, num):
                valid.append(num)
        return valid

    def _is_valid_hex(self, board, row, col, num):
        """Check if placing num at (row, col) is valid. Uses -1 for empty cells."""
        # Check row
        if num in board[row]:
            return False
        # Check column
        if num in [board[r][col] for r in range(self.size)]:
            return False
        # Check box
        box_row, box_col = (row // self.box_size) * self.box_size, (col // self.box_size) * self.box_size
        for r in range(box_row, box_row + self.box_size):
            for c in range(box_col, box_col + self.box_size):
                if board[r][c] == num:
                    return False
        return True

    def _create_solved_board(self):
        """Create a completely solved Sudoku board using -1 for empty.

        Uses a fast pattern-based approach with shuffling for randomness.
        Much faster than pure backtracking for 16x16 boards.
        """
        # Use pattern-based generation for speed (O(n^2) instead of exponential backtracking)
        board = self._generate_pattern_board()
        # Shuffle rows and columns within boxes to add randomness while maintaining validity
        board = self._shuffle_board(board)
        return board

    def _generate_pattern_board(self):
        """Generate a valid 16x16 sudoku using a deterministic pattern.

        Uses the formula: board[i][j] = (i*4 + i//4 + j) % 16
        This creates a valid sudoku that we can then shuffle for randomness.
        """
        board = [[-1 for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                # Pattern formula that guarantees valid sudoku
                board[i][j] = (i * self.box_size + i // self.box_size + j) % self.size
        return board

    def _shuffle_board(self, board):
        """Shuffle rows and columns within boxes to randomize while preserving validity."""
        # Shuffle rows within each band (4 rows per band)
        for band in range(self.box_size):
            rows = list(range(band * self.box_size, (band + 1) * self.box_size))
            random.shuffle(rows)
            # Reorder the rows
            board = [board[i] if i not in range(band * self.box_size, (band + 1) * self.box_size)
                    else board[rows[i - band * self.box_size]] for i in range(self.size)]

        # Shuffle columns within each stack (4 columns per stack)
        for stack in range(self.box_size):
            cols = list(range(stack * self.box_size, (stack + 1) * self.box_size))
            random.shuffle(cols)
            # Reorder the columns
            for row in range(self.size):
                temp = [board[row][i] for i in range(self.size)]
                for i, col in enumerate(cols):
                    board[row][stack * self.box_size + i] = temp[col]

        return board

    def _remove_numbers(self, board, difficulty):
        """Remove numbers from solved board. Removed cells set to -1."""
        puzzle = copy.deepcopy(board)
        removal_map = {
            'easy': int(self.size * self.size * 0.4),
            'medium': int(self.size * self.size * 0.5),
            'hard': int(self.size * self.size * 0.6)
        }
        removals = removal_map.get(difficulty, removal_map['medium'])
        positions = [(r, c) for r in range(self.size) for c in range(self.size)]
        random.shuffle(positions)
        for i in range(removals):
            row, col = positions[i]
            puzzle[row][col] = -1
        return puzzle

    def _convert_to_hex(self, board):
        """Convert numeric board to hex representation.
        Maps: -1 -> -1 (empty), 0-15 -> '0'-'9', 'A'-'F'
        """
        hex_board = []
        for row in board:
            hex_row = []
            for cell in row:
                if cell == -1:
                    hex_row.append(-1)  # Empty cell stays -1
                else:
                    # Convert 0-15 to '0'-'9', 'A'-'F'
                    hex_row.append(format(cell, 'X'))
            hex_board.append(hex_row)
        return hex_board

    def generate_puzzle(self, difficulty='medium'):
        """Generate a complete hex sudoku solution."""
        # Create solved board (uses -1 for empty during generation)
        board = self._create_solved_board()
        # Convert to hex representation
        # Frontend will handle removing numbers based on difficulty
        return self._convert_to_hex(board)
