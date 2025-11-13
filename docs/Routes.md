


# API Routes

## Overview
The backend API generates **complete Sudoku solutions**. The frontend is responsible for:
- Hiding cells based on difficulty level
- Validating user input against the known solution
- Providing hints and game logic

## Sudoku Endpoints

### GET /sudoku_puzzle
Retrieves a complete standard Sudoku solution (numbers 1-9).

**Query Parameters:**
- `difficulty` (optional): `'super_easy'`, `'easy'`, `'medium'`, or `'hard'` (default: `'medium'`)
  - Note: Kept for API compatibility but does not affect the generated solution
  - Frontend should use this to determine how many cells to hide

**Response:**
```json
{
  "solution": [[1,2,3,...], [4,5,6,...], ...],
  "difficulty": "medium",
  "size": 9
}
```

**Response Fields:**
- `solution`: 9x9 array of integers (1-9) representing a complete valid Sudoku solution
- `difficulty`: The requested difficulty level
- `size`: Board size (always 9 for standard Sudoku)

**Example:**
```
GET /sudoku_puzzle?difficulty=easy
```

---

### GET /hex_sudoku_puzzle
Retrieves a complete hexadecimal Sudoku solution (hex values 0-F).

**Query Parameters:**
- `difficulty` (optional): `'super_easy'`, `'easy'`, `'medium'`, or `'hard'` (default: `'medium'`)
  - Note: Kept for API compatibility but does not affect the generated solution
  - Frontend should use this to determine how many cells to hide

**Response:**
```json
{
  "solution": [["0","1","2",...], ["3","4","5",...], ...],
  "difficulty": "medium",
  "size": 16
}
```

**Response Fields:**
- `solution`: 16x16 array of hex strings ('0'-'9', 'A'-'F') representing a complete valid hex Sudoku solution
- `difficulty`: The requested difficulty level
- `size`: Board size (always 16 for hex Sudoku)

**Example:**
```
GET /hex_sudoku_puzzle?difficulty=hard
```

---

### GET /health
Health check endpoint to verify the API is running.

**Response:**
```json
{
  "status": "healthy"
}
```

---

## Removed Endpoints

The following endpoints have been **removed** as validation and hints are now handled by the frontend:

- ~~POST /sudoku_solution~~ - Validation now done on frontend
- ~~POST /hex_sudoku_solution~~ - Validation now done on frontend
- ~~POST /sudoku_hint~~ - Hints now generated on frontend
- ~~POST /hex_sudoku_hint~~ - Hints now generated on frontend

## Frontend Responsibilities

With the new architecture, the frontend should:

1. **Request a complete solution** from the backend
2. **Store the complete solution** for validation purposes
3. **Hide cells based on difficulty**:
   - Super Easy: Hide 3-4 cells
   - Easy: Hide ~40% of cells
   - Medium: Hide ~50% of cells
   - Hard: Hide ~60% of cells
4. **Validate user input** by comparing against the stored solution
5. **Provide hints** by revealing cells from the stored solution
6. **Check win condition** by comparing user's board with the complete solution