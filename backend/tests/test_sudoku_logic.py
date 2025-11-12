import pytest
from app.sudoku_generator import SudokuGenerator, HexSudokuGenerator
from app.sudoku_validator import SudokuValidator, HexSudokuValidator


class TestSudokuGenerator:
    """Test standard Sudoku generator."""
    
    def test_generate_puzzle_size(self):
        """Test that generated puzzle has correct size."""
        gen = SudokuGenerator(size=9)
        puzzle = gen.generate_puzzle('medium')
        assert len(puzzle) == 9
        assert all(len(row) == 9 for row in puzzle)
    
    def test_generate_puzzle_has_empty_cells(self):
        """Test that generated puzzle has empty cells."""
        gen = SudokuGenerator(size=9)
        puzzle = gen.generate_puzzle('medium')
        empty_count = sum(row.count(0) for row in puzzle)
        assert empty_count > 0
    
    def test_difficulty_levels(self):
        """Test different difficulty levels."""
        gen = SudokuGenerator(size=9)
        easy = gen.generate_puzzle('easy')
        hard = gen.generate_puzzle('hard')
        
        easy_empty = sum(row.count(0) for row in easy)
        hard_empty = sum(row.count(0) for row in hard)
        
        assert hard_empty > easy_empty


class TestHexSudokuGenerator:
    """Test hexadecimal Sudoku generator."""
    
    def test_generate_hex_puzzle_size(self):
        """Test that generated hex puzzle has correct size."""
        gen = HexSudokuGenerator()
        puzzle = gen.generate_puzzle('medium')
        assert len(puzzle) == 16
        assert all(len(row) == 16 for row in puzzle)
    
    def test_hex_puzzle_format(self):
        """Test that hex puzzle uses hex characters."""
        gen = HexSudokuGenerator()
        puzzle = gen.generate_puzzle('medium')
        for row in puzzle:
            for cell in row:
                assert cell in '0123456789ABCDEF'


class TestSudokuValidator:
    """Test standard Sudoku validator."""
    
    def test_valid_complete_solution(self):
        """Test validation of a complete valid solution."""
        validator = SudokuValidator(size=9)
        
        # Simple valid 9x9 solution
        puzzle_state = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        
        puzzle_solution = [
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
        
        assert validator.validate_solution(puzzle_state, puzzle_solution) == True
    
    def test_invalid_solution_changed_clue(self):
        """Test that validator rejects solution with changed original clue."""
        validator = SudokuValidator(size=9)
        
        puzzle_state = [[i if j == 0 else 0 for j in range(9)] for i in range(1, 10)]
        puzzle_solution = [[i if j == 0 else j for j in range(1, 10)] for i in range(1, 10)]
        
        # Change a clue
        puzzle_solution[0][0] = 9
        
        assert validator.validate_solution(puzzle_state, puzzle_solution) == False
    
    def test_get_hint(self):
        """Test hint generation."""
        validator = SudokuValidator(size=9)
        
        puzzle = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        
        hint, cell_index = validator.get_hint(puzzle)
        
        assert isinstance(hint, str)
        assert isinstance(cell_index, int)
        assert len(hint) > 0


class TestHexSudokuValidator:
    """Test hexadecimal Sudoku validator."""
    
    def test_hex_validator_initialization(self):
        """Test hex validator initialization."""
        validator = HexSudokuValidator()
        assert validator.size == 16
    
    def test_get_hex_hint(self):
        """Test hint generation for hex Sudoku."""
        validator = HexSudokuValidator()
        
        # Create a simple hex puzzle
        puzzle = [['0' for _ in range(16)] for _ in range(16)]
        puzzle[0][0] = '1'
        
        hint, cell_index = validator.get_hint(puzzle)
        
        assert isinstance(hint, str)
        assert isinstance(cell_index, int)
