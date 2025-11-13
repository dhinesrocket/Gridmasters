import json
import pytest

class TestSudokuPuzzleEndpoint:
    """Test GET /sudoku_puzzle endpoint."""

    def test_get_sudoku_puzzle_default(self, client):
        """Test getting a puzzle with default difficulty."""
        response = client.get('/sudoku_puzzle')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'puzzle' in data
        assert 'difficulty' in data
        assert data['size'] == 9

    def test_get_sudoku_puzzle_with_difficulty(self, client):
        """Test getting puzzle with specified difficulty."""
        for difficulty in ['easy', 'medium', 'hard']:
            response = client.get(f'/sudoku_puzzle?difficulty={difficulty}')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['difficulty'] == difficulty

    def test_get_sudoku_puzzle_invalid_difficulty(self, client):
        """Test invalid difficulty returns error."""
        response = client.get('/sudoku_puzzle?difficulty=invalid')
        assert response.status_code == 400


class TestHexSudokuPuzzleEndpoint:
    """Test GET /hex_sudoku_puzzle endpoint."""

    def test_get_hex_sudoku_puzzle(self, client):
        """Test getting a hex puzzle."""
        response = client.get('/hex_sudoku_puzzle')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'puzzle' in data
        assert data['size'] == 16

    def test_hex_puzzle_format(self, client):
        """Test that hex puzzle contains hex characters."""
        response = client.get('/hex_sudoku_puzzle')
        data = json.loads(response.data)
        puzzle = data['puzzle']
        for row in puzzle:
            for cell in row:
                assert cell in '0123456789ABCDEF'


class TestSudokuSolutionEndpoint:
    """Test POST /sudoku_solution endpoint."""

    def test_validate_correct_solution(self, client):
        """Test validation of correct solution."""
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

        response = client.post('/sudoku_solution',
                              data=json.dumps({
                                  'puzzle_state': puzzle_state,
                                  'puzzle_solution': puzzle_solution
                              }),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['valid'] == True

    def test_validate_missing_fields(self, client):
        """Test validation with missing fields."""
        response = client.post('/sudoku_solution',
                              data=json.dumps({'puzzle_state': []}),
                              content_type='application/json')
        assert response.status_code == 400

    def test_validate_invalid_board_size(self, client):
        """Test validation with wrong board size."""
        response = client.post('/sudoku_solution',
                              data=json.dumps({
                                  'puzzle_state': [[0] * 8] * 8,
                                  'puzzle_solution': [[1] * 8] * 8
                              }),
                              content_type='application/json')
        assert response.status_code == 400


class TestHexSudokuSolutionEndpoint:
    """Test POST /hex_sudoku_solution endpoint."""

    def test_validate_hex_solution_missing_fields(self, client):
        """Test hex solution validation with missing fields."""
        response = client.post('/hex_sudoku_solution',
                              data=json.dumps({'puzzle_state': []}),
                              content_type='application/json')
        assert response.status_code == 400

    def test_validate_hex_solution_wrong_size(self, client):
        """Test hex solution validation with wrong size."""
        response = client.post('/hex_sudoku_solution',
                              data=json.dumps({
                                  'puzzle_state': [['0'] * 9] * 9,
                                  'puzzle_solution': [['1'] * 9] * 9
                              }),
                              content_type='application/json')
        assert response.status_code == 400


class TestSudokuHintEndpoint:
    """Test POST /sudoku_hint endpoint."""

    def test_get_hint(self, client):
        """Test getting a hint."""
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

        response = client.post('/sudoku_hint',
                              data=json.dumps({'puzzle': puzzle}),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'hint' in data
        assert 'cell_index' in data

    def test_get_hint_missing_puzzle(self, client):
        """Test hint request without puzzle."""
        response = client.post('/sudoku_hint',
                              data=json.dumps({}),
                              content_type='application/json')
        assert response.status_code == 400

    def test_get_hint_invalid_board(self, client):
        """Test hint with invalid board."""
        response = client.post('/sudoku_hint',
                              data=json.dumps({'puzzle': [[0] * 8] * 8}),
                              content_type='application/json')
        assert response.status_code == 400


class TestHexSudokuHintEndpoint:
    """Test POST /hex_sudoku_hint endpoint."""

    def test_get_hex_hint(self, client):
        """Test getting a hex hint."""
        puzzle = [['0' for _ in range(16)] for _ in range(16)]
        puzzle[0][0] = '1'

        response = client.post('/hex_sudoku_hint',
                              data=json.dumps({'puzzle': puzzle}),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'hint' in data
        assert 'cell_index' in data

    def test_get_hex_hint_invalid_size(self, client):
        """Test hex hint with wrong size."""
        response = client.post('/hex_sudoku_hint',
                              data=json.dumps({'puzzle': [[0] * 9] * 9}),
                              content_type='application/json')
        assert response.status_code == 400


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_check(self, client):
        """Test health check returns OK."""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
