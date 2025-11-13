import json


class TestSudokuPuzzleEndpoint:
    """Test GET /sudoku_puzzle endpoint."""

    def test_get_sudoku_puzzle_default(self, client):
        """Test getting a complete solution with default difficulty."""
        response = client.get('/sudoku_puzzle')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'solution' in data
        assert 'difficulty' in data
        assert data['size'] == 9

        # Verify it's a complete solution (no zeros)
        solution = data['solution']
        for row in solution:
            for cell in row:
                assert 1 <= cell <= 9

    def test_get_sudoku_puzzle_with_difficulty(self, client):
        """Test getting solution with specified difficulty."""
        for difficulty in ['easy', 'medium', 'hard']:
            response = client.get(f'/sudoku_puzzle?difficulty={difficulty}')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['difficulty'] == difficulty

            # Verify complete solution
            solution = data['solution']
            assert len(solution) == 9
            for row in solution:
                assert len(row) == 9
                assert all(1 <= cell <= 9 for cell in row)

    def test_get_sudoku_puzzle_invalid_difficulty(self, client):
        """Test invalid difficulty returns error."""
        response = client.get('/sudoku_puzzle?difficulty=invalid')
        assert response.status_code == 400


class TestHexSudokuPuzzleEndpoint:
    """Test GET /hex_sudoku_puzzle endpoint."""

    def test_get_hex_sudoku_puzzle(self, client):
        """Test getting a complete hex solution."""
        response = client.get('/hex_sudoku_puzzle')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'solution' in data
        assert data['size'] == 16

        # Verify it's a complete solution (all hex values 0-F)
        solution = data['solution']
        assert len(solution) == 16
        for row in solution:
            assert len(row) == 16
            for cell in row:
                assert cell in '0123456789ABCDEF'

    def test_hex_puzzle_format(self, client):
        """Test that hex solution contains valid hex characters."""
        response = client.get('/hex_sudoku_puzzle')
        data = json.loads(response.data)
        solution = data['solution']
        for row in solution:
            for cell in row:
                assert cell in '0123456789ABCDEF'


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_check(self, client):
        """Test health check returns OK."""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
