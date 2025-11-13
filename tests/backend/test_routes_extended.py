"""
Extended tests for API routes.
"""
import pytest
import json


class TestSudokuPuzzleEndpointExtended:
    """Extended tests for sudoku puzzle generation endpoint."""

    def test_puzzle_response_structure(self, client):
        """Test that solution response has correct structure."""
        response = client.get('/sudoku_puzzle')
        data = json.loads(response.data)

        assert 'solution' in data
        assert isinstance(data['solution'], list)
        assert len(data['solution']) == 9
        for row in data['solution']:
            assert len(row) == 9
            # Verify it's a complete solution with no empty cells
            for cell in row:
                assert 1 <= cell <= 9

    def test_multiple_difficulty_levels(self, client):
        """Test all difficulty levels work."""
        for difficulty in ['easy', 'medium', 'hard']:
            response = client.get(f'/sudoku_puzzle?difficulty={difficulty}')
            assert response.status_code == 200


class TestCorsHeaders:
    """Test CORS headers are set correctly."""

    def test_cors_headers_present(self, client):
        """Test that CORS headers are in response."""
        response = client.get('/health')
        assert 'Access-Control-Allow-Origin' in response.headers
