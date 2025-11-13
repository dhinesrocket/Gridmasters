"""
Extended tests for API routes.
"""
import pytest
import json


class TestSudokuPuzzleEndpointExtended:
    """Extended tests for sudoku puzzle generation endpoint."""

    def test_puzzle_response_structure(self, client):
        """Test that puzzle response has correct structure."""
        response = client.get('/sudoku_puzzle')
        data = json.loads(response.data)

        assert 'puzzle' in data
        assert isinstance(data['puzzle'], list)
        assert len(data['puzzle']) == 9
        for row in data['puzzle']:
            assert len(row) == 9

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
