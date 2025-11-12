


# API Routes

## Sudoku Endpoints

### GET sudoku_puzzle
Retrieves a new standard Sudoku puzzle (numbers 1-9).

**Response:**
- Returns a Sudoku puzzle grid

---

### GET hex_sudoku_puzzle
Retrieves a new hexadecimal Sudoku puzzle (hex values 0-F).

**Response:**
- Returns a hex Sudoku puzzle grid

---

### POST sudoku_solution
Validates a submitted solution for a standard Sudoku puzzle.

**Request Body:**
- `puzzle_solution`: The completed puzzle submitted by the user
- `puzzle_state`: The original puzzle state

**Response:**
- Returns `bool` - `true` if the solution is correct, `false` otherwise

---

### POST hex_sudoku_solution
Validates a submitted solution for a hexadecimal Sudoku puzzle.

**Request Body:**
- `puzzle_solution`: The completed hex puzzle submitted by the user
- `puzzle_state`: The original hex puzzle state

**Response:**
- Returns `bool` - `true` if the solution is correct, `false` otherwise

---

### GET sudoku_hint
Provides a hint for a standard Sudoku puzzle.

**Request Parameters:**
- `puzzle`: The current state of the puzzle

**Response:**
- Returns `string` - Description or guidance for the hint
- Returns `int` - Cell or position identifier for the hint

---

### GET hex_sudoku_hint
Provides a hint for a hexadecimal Sudoku puzzle.

**Request Parameters:**
- `puzzle`: The current state of the hex puzzle

**Response:**
- Returns `string` - Description or guidance for the hint
- Returns `int` - Cell or position identifier for the hint