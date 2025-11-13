"""
DEPRECATION NOTICE:
This module is no longer used by the backend API as validation is now performed on the frontend.
The backend only generates complete Sudoku solutions, and the frontend handles:
- Hiding cells based on difficulty
- Validating user input against the known solution
- Providing hints

This file is kept for reference or potential future use.
"""


class SudokuValidator:
    """Validate Sudoku puzzles and solutions."""

    def __init__(self, size=9):
        """
        Initialize validator.
        Args:
            size: Board size (9 for standard, 16 for hex)
        """
        self.size = size
        self.box_size = int(size ** 0.5)

    def _check_dimensions(self, board):
        """Check if board has correct dimensions."""
        if len(board) != self.size:
            return False
        return all(len(row) == self.size for row in board)

    def _check_original_clues(self, puzzle_state, puzzle_solution):
        """Verify that original clues haven't been changed."""
        for r in range(self.size):
            for c in range(self.size):
                if puzzle_state[r][c] != 0:
                    if puzzle_state[r][c] != puzzle_solution[r][c]:
                        return False
        return True

    def _check_all_constraints(self, board):
        """Check all Sudoku constraints."""
        # Check all rows
        for row in board:
            if not self._check_group(row):
                return False

        # Check all columns
        for col in range(self.size):
            column = [board[row][col] for row in range(self.size)]
            if not self._check_group(column):
                return False

        # Check all boxes
        for box_row in range(0, self.size, self.box_size):
            for box_col in range(0, self.size, self.box_size):
                box = []
                for r in range(box_row, box_row + self.box_size):
                    for c in range(box_col, box_col + self.box_size):
                        box.append(board[r][c])
                if not self._check_group(box):
                    return False

        return True

    def _check_group(self, group):
        """Check if a group (row, column, or box) is valid."""
        # Remove zeros (empty cells)
        filled = [x for x in group if x != 0]

        # Check if all filled cells are in valid range
        if not all(1 <= x <= self.size for x in filled):
            return False

        # Check for duplicates
        return len(filled) == len(set(filled))

    def get_hint(self, puzzle):
        """
        Generate a hint for the puzzle.
        Args:
            puzzle: Current puzzle state
        Returns:
            tuple: (hint_string, cell_index) or (None, None) if no hint available
        """
        # Find first empty cell
        for r in range(self.size):
            for c in range(self.size):
                if puzzle[r][c] == 0:
                    # Find valid numbers for this cell
                    valid_nums = self._get_valid_numbers(puzzle, r, c)
                    if valid_nums:
                        cell_index = r * self.size + c
                        if len(valid_nums) == 1:
                            hint = f"Cell at row {r+1}, column {c+1} can only be {valid_nums[0]}"
                        else:
                            valid_str = ', '.join(map(str, valid_nums))
                            hint = f"Cell at row {r+1}, column {c+1} can be one of: {valid_str}"
                        return hint, cell_index

        return "No hints available", -1

    def _get_valid_numbers(self, puzzle, row, col):
        """Get list of valid numbers for a cell."""
        valid = set(range(1, self.size + 1))

        # Remove numbers in same row
        valid -= set(puzzle[row])

        # Remove numbers in same column
        valid -= set(puzzle[r][col] for r in range(self.size))

        # Remove numbers in same box
        box_row, box_col = (row // self.box_size) * self.box_size, (col // self.box_size) * self.box_size
        for r in range(box_row, box_row + self.box_size):
            for c in range(box_col, box_col + self.box_size):
                valid.discard(puzzle[r][c])

        return sorted(list(valid))


class HexSudokuValidator(SudokuValidator):
    """Validator for 16x16 hexadecimal Sudoku."""

    def __init__(self):
        super().__init__(size=16)

    def get_hint(self, puzzle):
        """Generate hint for hex Sudoku."""
        numeric_puzzle = self._convert_from_hex(puzzle)
        hint, cell_index = super().get_hint(numeric_puzzle)

        # Convert numeric hint to hex
        if hint and 'can only be' in hint:
            parts = hint.split('can only be ')
            num = int(parts[1])
            hint = parts[0] + 'can only be ' + format(num, 'X')
        elif hint and 'can be one of:' in hint:
            parts = hint.split('can be one of: ')
            nums = parts[1].split(', ')
            hex_nums = [format(int(n), 'X') for n in nums]
            hint = parts[0] + 'can be one of: ' + ', '.join(hex_nums)

        return hint, cell_index

    def _convert_from_hex(self, board):
        """Convert hex board to numeric."""
        numeric_board = []
        for row in board:
            numeric_row = []
            for cell in row:
                if cell in ('0', 0):
                    numeric_row.append(0)
                else:
                    numeric_row.append(int(str(cell), 16))
            numeric_board.append(numeric_row)
        return numeric_board
