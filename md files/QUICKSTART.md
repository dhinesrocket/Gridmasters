# Gridmasters - Quick Start Guide

## Architecture Overview

Gridmasters uses a **frontend-first validation** architecture:
- **Backend**: Generates complete Sudoku solutions
- **Frontend**: Handles game logic, validation, hints, and difficulty

## Project Structure

```
Gridmasters/
├── backend/                    # Flask API
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes.py          # API endpoints
│   │   ├── sudoku_generator.py # Solution generator
│   │   └── sudoku_validator.py # (Deprecated)
│   ├── tests/
│   └── requirements.txt
│
├── frontend/                   # Vue.js App
│   ├── src/
│   │   ├── App.vue            # Main game component
│   │   ├── components/
│   │   │   └── GameBoard.vue  # Board UI component
│   │   ├── services/
│   │   │   └── api.js         # API client
│   │   └── utils/
│   │       └── sudokuUtils.js # Validation & game logic
│   └── package.json
│
└── docs/
    ├── Routes.md              # API documentation
    ├── ARCHITECTURE_CHANGES.md # Backend changes
    └── FRONTEND_CHANGES.md    # Frontend changes
```

## Setup Instructions

### Backend Setup

1. **Navigate to backend directory**
   ```powershell
   cd backend
   ```

2. **Create and activate virtual environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run the backend server**
   ```powershell
   python run.py
   ```

   Backend will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory** (in a new terminal)
   ```powershell
   cd frontend
   ```

2. **Install dependencies**
   ```powershell
   npm install
   ```

3. **Run the development server**
   ```powershell
   npm run dev
   ```

   Frontend will run on `http://localhost:5173` (or similar)

## API Endpoints

### GET /sudoku_puzzle
Returns a complete 9x9 Sudoku solution.

**Query Parameters:**
- `difficulty`: `super_easy`, `easy`, `medium`, or `hard` (default: `medium`)

**Response:**
```json
{
  "solution": [[1,2,3,...], ...],
  "difficulty": "medium",
  "size": 9
}
```

### GET /hex_sudoku_puzzle
Returns a complete 16x16 hex Sudoku solution.

**Query Parameters:**
- `difficulty`: `super_easy`, `easy`, `medium`, or `hard` (default: `medium`)

**Response:**
```json
{
  "solution": [["0","1","2",...], ...],
  "difficulty": "medium",
  "size": 16
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## How It Works

### 1. Game Start
```javascript
// User selects difficulty
loadPuzzle('medium')
  ↓
// Frontend requests complete solution from backend
GET /sudoku_puzzle?difficulty=medium
  ↓
// Backend returns complete solved board
{ solution: [[1,2,3,4,5,6,7,8,9], ...] }
  ↓
// Frontend stores solution and hides 50% of cells
solution.value = completeSolution
puzzle.value = hideCells(completeSolution, 'medium')
```

### 2. User Plays
```javascript
// User fills in cells
updateCell({ row: 0, col: 0, value: 5 })
  ↓
// Update local puzzle state
puzzle.value[0][0] = 5
```

### 3. Validation
```javascript
// User clicks "Validate"
validateSolution()
  ↓
// Check if complete
isBoardComplete(puzzle.value)
  ↓
// Validate against stored solution
validateBoard(puzzle.value, solution.value)
  ↓
// Show result (instant, no API call)
"🎉 CONGRATULATIONS! Solution is correct!"
```

### 4. Hints
```javascript
// User clicks "Get Hint"
getHint()
  ↓
// Find first empty cell
findEmptyCell(puzzle.value)
  ↓
// Get value from stored solution
value = solution.value[row][col]
  ↓
// Show hint (instant, no API call)
"Cell at row 3, column 5 should be 7"
```

## Key Frontend Utilities

### `hideCells(solution, difficulty, gameMode)`
Randomly hides cells in a complete solution based on difficulty level.

### `validateBoard(userBoard, solution, gameMode)`
Validates if user's board matches the solution.

### `getHint(userBoard, solution, gameMode)`
Finds the next empty cell and returns its correct value.

### `isBoardComplete(board, gameMode)`
Checks if all cells are filled.

## Running Tests

### Backend Tests
```powershell
cd backend
.\venv\Scripts\activate
pytest tests/
```

### Frontend Tests
```powershell
cd frontend
npm run test
```

## Development Workflow

1. **Backend changes**: Modify `backend/app/routes.py` or `sudoku_generator.py`
2. **Frontend changes**: Modify `frontend/src/App.vue` or utils
3. **Test locally**: Run both servers and test in browser
4. **Commit changes**: Use meaningful commit messages

## Common Issues

### Backend not responding
- Check if backend is running on port 5000
- Check firewall settings
- Verify virtual environment is activated

### Frontend can't connect to backend
- Check `API_BASE_URL` in `frontend/src/services/api.js`
- Ensure CORS is properly configured in backend
- Check browser console for errors

### Validation not working
- Verify `solution.value` is properly stored
- Check browser console for JavaScript errors
- Ensure `sudokuUtils.js` is imported correctly

## Performance Notes

- **Validation**: Instant (<1ms) - runs locally
- **Hints**: Instant (<1ms) - runs locally
- **Puzzle Generation**: ~100-500ms - backend call
- **Network**: Only 1 API call per game (to fetch solution)

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Technologies Used

### Backend
- Python 3.12
- Flask (web framework)
- pytest (testing)

### Frontend
- Vue 3 (Composition API)
- Vite (build tool)
- Axios (HTTP client)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

See LICENSE file for details.

## Support

For issues and questions, please open an issue on GitHub.

---

**Last Updated**: November 13, 2025
