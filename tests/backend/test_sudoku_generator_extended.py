"""
Extended tests for Sudoku generator functionality.
"""
import pytest
from app.sudoku_generator import SudokuGenerator, HexSudokuGenerator


class TestSudokuGeneratorExtended:
    """Extended tests for standard Sudoku generator."""

    def test_puzzle_uniqueness(self):
        """Test that generated solutions are unique."""
        gen = SudokuGenerator()
        solution1 = gen.generate_puzzle('easy')
        solution2 = gen.generate_puzzle('easy')
        assert solution1 != solution2

    def test_complete_solution_no_empty_cells(self):
        """Test that generated solutions have no empty cells."""
        gen = SudokuGenerator()
        for difficulty in ['easy', 'medium', 'hard']:
            solution = gen.generate_puzzle(difficulty)
            
            # Verify no zeros (empty cells)
            for row in solution:
                assert 0 not in row
            
            # Verify all cells have values 1-9
            for row in solution:
                for cell in row:
                    assert 1 <= cell <= 9

    def test_valid_numbers_only(self):
        """Test that only valid numbers (1-9) are used."""
        gen = SudokuGenerator()
        solution = gen.generate_puzzle('medium')
        for row in solution:
            for cell in row:
                assert 1 <= cell <= 9


class TestHexSudokuGeneratorExtended:
    """Extended tests for hex Sudoku generator."""

    def test_hex_conversion_accuracy(self):
        """Test that hex conversion is accurate."""
        gen = HexSudokuGenerator()
        solution = gen.generate_puzzle('easy')

        # Check all cells are valid hex digits
        valid_hex = set('0123456789ABCDEF')
        for row in solution:
            for cell in row:
                assert cell in valid_hex

    def test_hex_solution_is_complete(self):
        """Test that hex solution is complete with all values 0-F."""
        gen = HexSudokuGenerator()
        solution = gen.generate_puzzle('medium')

        # Verify all cells are filled (complete solution)
        for row in solution:
            for cell in row:
                assert cell in '0123456789ABCDEF'
        
        # Verify solution has correct dimensions
        assert len(solution) == 16
        for row in solution:
            assert len(row) == 16
