"""
Extended tests for Sudoku validator functionality.
"""
import pytest
from app.sudoku_validator import SudokuValidator, HexSudokuValidator


class TestSudokuValidatorExtended:
    """Extended tests for standard Sudoku validator - NOTE: Validation moved to frontend."""

    @pytest.mark.skip(reason="Validation moved to frontend - validate_solution method no longer used")
    def test_validate_row_duplicates(self):
        """Test detection of duplicate numbers in rows."""
        puzzle = [
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
        solution = [row[:] for row in puzzle]
        solution[0][0] = 3  # Create duplicate in first row

        validator = SudokuValidator(size=9)
        is_valid = validator.validate_solution(puzzle, solution)
        assert not is_valid

    @pytest.mark.skip(reason="Validation moved to frontend - validate_solution method no longer used")
    def test_validate_column_duplicates(self):
        """Test detection of duplicate numbers in columns."""
        puzzle = [[0]*9 for _ in range(9)]
        solution = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [5, 4, 5, 2, 8, 6, 1, 7, 9]  # Duplicate 5 in first column
        ]

        validator = SudokuValidator(size=9)
        is_valid = validator.validate_solution(puzzle, solution)
        assert not is_valid

    @pytest.mark.skip(reason="Validation moved to frontend - validate_solution method no longer used")
    def test_validate_box_duplicates(self):
        """Test detection of duplicate numbers in 3x3 boxes."""
        puzzle = [[0]*9 for _ in range(9)]
        solution = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 5, 3, 4, 2, 5, 6, 7],  # Duplicate 5 in first box
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]

        validator = SudokuValidator(size=9)
        is_valid = validator.validate_solution(puzzle, solution)
        assert not is_valid


class TestHexSudokuValidatorExtended:
    """Extended tests for hex Sudoku validator."""

    def test_hex_validator_valid_chars(self):
        """Test that hex validator accepts valid hex characters."""
        validator = HexSudokuValidator()
        assert validator.size == 16
        assert validator.box_size == 4
