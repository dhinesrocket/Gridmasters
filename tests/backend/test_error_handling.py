"""
Tests for error handling in routes.
"""
import pytest
from unittest.mock import patch, MagicMock
from app.sudoku_generator import SudokuGenerator, HexSudokuGenerator


class TestErrorHandling:
    """Tests for error handling in API endpoints."""

    @pytest.fixture
    def client(self, app):
        """Create test client."""
        return app.test_client()

    def test_sudoku_generator_exception(self, client):
        """Test error handling when sudoku generator raises exception."""
        with patch.object(SudokuGenerator, 'generate_puzzle', side_effect=Exception("Generator error")):
            response = client.get('/sudoku_puzzle')
            assert response.status_code == 500
            data = response.get_json()
            assert 'error' in data
            assert data['error'] == 'Internal server error'

    def test_hex_sudoku_generator_exception(self, client):
        """Test error handling when hex sudoku generator raises exception."""
        with patch.object(HexSudokuGenerator, 'generate_puzzle', side_effect=Exception("Generator error")):
            response = client.get('/hex_sudoku_puzzle')
            assert response.status_code == 500
            data = response.get_json()
            assert 'error' in data
            assert data['error'] == 'Internal server error'

    def test_sudoku_invalid_difficulty(self, client):
        """Test invalid difficulty parameter for sudoku."""
        response = client.get('/sudoku_puzzle?difficulty=invalid')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_hex_sudoku_invalid_difficulty(self, client):
        """Test invalid difficulty parameter for hex sudoku."""
        response = client.get('/hex_sudoku_puzzle?difficulty=invalid')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_sudoku_all_valid_difficulties(self, client):
        """Test all valid difficulty levels for sudoku."""
        difficulties = ['super_easy', 'easy', 'medium', 'hard']
        for difficulty in difficulties:
            response = client.get(f'/sudoku_puzzle?difficulty={difficulty}')
            assert response.status_code == 200
            data = response.get_json()
            assert 'solution' in data
            assert data['difficulty'] == difficulty

    def test_hex_sudoku_all_valid_difficulties(self, client):
        """Test all valid difficulty levels for hex sudoku."""
        difficulties = ['super_easy', 'easy', 'medium', 'hard']
        for difficulty in difficulties:
            response = client.get(f'/hex_sudoku_puzzle?difficulty={difficulty}')
            assert response.status_code == 200
            data = response.get_json()
            assert 'solution' in data
            assert data['difficulty'] == difficulty

    def test_sudoku_case_insensitive_difficulty(self, client):
        """Test that difficulty parameter is case-insensitive."""
        response = client.get('/sudoku_puzzle?difficulty=EASY')
        assert response.status_code == 200
        data = response.get_json()
        assert data['difficulty'] == 'easy'

    def test_hex_sudoku_case_insensitive_difficulty(self, client):
        """Test that difficulty parameter is case-insensitive for hex."""
        response = client.get('/hex_sudoku_puzzle?difficulty=HARD')
        assert response.status_code == 200
        data = response.get_json()
        assert data['difficulty'] == 'hard'


class TestGeneratorEdgeCases:
    """Tests for edge cases in generators."""

    def test_sudoku_generator_max_retries_exceeded(self):
        """Test generator raises error when max retries exceeded."""
        gen = SudokuGenerator()
        
        # Mock _fill_board to always fail
        with patch.object(gen, '_fill_board', return_value=False):
            with pytest.raises(RuntimeError) as exc_info:
                gen._create_solved_board()
            assert 'Failed to generate' in str(exc_info.value)

    def test_hex_sudoku_generator_max_retries_exceeded(self):
        """Test hex generator raises error when max retries exceeded."""
        gen = HexSudokuGenerator()
        
        # Mock _fill_board to always fail
        with patch.object(gen, '_fill_board', return_value=False):
            with pytest.raises(RuntimeError) as exc_info:
                gen._create_solved_board()
            assert 'Failed to generate' in str(exc_info.value)
