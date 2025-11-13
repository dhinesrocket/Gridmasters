"""
Extended tests for Sudoku generator functionality.
"""
import pytest
from app.sudoku_generator import SudokuGenerator, HexSudokuGenerator


class TestSudokuGeneratorExtended:
    """Extended tests for standard Sudoku generator."""

    def test_puzzle_uniqueness(self):
        """Test that generated puzzles are unique."""
        gen = SudokuGenerator()
        puzzle1 = gen.generate_puzzle('easy')
        puzzle2 = gen.generate_puzzle('easy')
        assert puzzle1 != puzzle2

    def test_empty_cells_within_range(self):
        """Test that number of empty cells matches difficulty."""
        gen = SudokuGenerator()
        easy_puzzle = gen.generate_puzzle('easy')
        hard_puzzle = gen.generate_puzzle('hard')

        easy_empty = sum(row.count(0) for row in easy_puzzle)
        hard_empty = sum(row.count(0) for row in hard_puzzle)

        assert easy_empty < hard_empty

    def test_valid_numbers_only(self):
        """Test that only valid numbers (1-9) are used."""
        gen = SudokuGenerator()
        puzzle = gen.generate_puzzle('medium')
        for row in puzzle:
            for cell in row:
                assert 0 <= cell <= 9


class TestHexSudokuGeneratorExtended:
    """Extended tests for hex Sudoku generator."""

    def test_hex_conversion_accuracy(self):
        """Test that hex conversion is accurate."""
        gen = HexSudokuGenerator()
        puzzle = gen.generate_puzzle('easy')

        # Check all cells are valid hex digits
        valid_hex = set('0123456789ABCDEF')
        for row in puzzle:
            for cell in row:
                assert cell in valid_hex

    def test_hex_puzzle_has_clues(self):
        """Test that hex puzzle has non-zero clues."""
        gen = HexSudokuGenerator()
        puzzle = gen.generate_puzzle('medium')

        non_empty = sum(1 for row in puzzle for cell in row if cell != '0')
        assert non_empty > 0
