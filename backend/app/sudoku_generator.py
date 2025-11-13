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

    def generate_puzzle(self, difficulty='medium'):
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
        board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self._fill_board(board)
        return board

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
        """Recursively fill the board using values 0-15 (displayed as 0-9, A-F)."""
        if row == self.size:
            return True
        next_row, next_col = (row, col + 1) if col + 1 < self.size else (row + 1, 0)
        # Use values 0-15 for hex Sudoku (mapped to 0-9, A-F)
        # Note: We use 0-15 instead of 1-16 to align with hex notation
        numbers = list(range(0, 16))
        random.shuffle(numbers)
        for num in numbers:
            if self._is_valid_hex(board, row, col, num):
                board[row][col] = num
                if self._fill_board(board, next_row, next_col):
                    return True
                board[row][col] = -1  # Use -1 for empty instead of 0
        return False

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
        """Create a completely solved Sudoku board using -1 for empty."""
        board = [[-1 for _ in range(self.size)] for _ in range(self.size)]
        self._fill_board(board)
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
