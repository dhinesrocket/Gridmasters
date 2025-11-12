# GRIDMASTERS Setup Guide

## Quick Start

### Step 1: Install Backend Dependencies

Open a PowerShell terminal in the backend directory:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Step 2: Install Frontend Dependencies

Open another PowerShell terminal in the frontend directory:

```powershell
cd frontend
npm install
```

### Step 3: Start the Backend Server

In the backend terminal:

```powershell
python run.py
```

You should see:
```
* Running on http://0.0.0.0:5000
```

### Step 4: Start the Frontend Server

In the frontend terminal:

```powershell
npm run dev
```

You should see:
```
VITE v5.x.x ready in xxx ms
➜  Local:   http://localhost:3000/
```

### Step 5: Play!

Open your browser and navigate to: `http://localhost:3000`

## Testing the Backend

To run tests:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
pytest
```

To run tests with coverage:

```powershell
pytest --cov=app tests/
```

## Troubleshooting

### Python venv activation fails
Try:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Port already in use
Kill the process using the port:
```powershell
# For port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# For port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Module not found errors
Ensure you're in the virtual environment:
```powershell
# Backend
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Frontend
cd frontend
rm -r node_modules
npm install
```

## What You Should See

### Backend Running:
```
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server.
 * Running on http://0.0.0.0:5000
```

### Frontend Running:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

### Browser:
You should see a terminal-style interface with green text on a dark background, featuring ASCII art and game mode selection options.

## API Endpoints Available

Once the backend is running, you can test endpoints:

- GET http://localhost:5000/health
- GET http://localhost:5000/sudoku_puzzle?difficulty=medium
- GET http://localhost:5000/hex_sudoku_puzzle?difficulty=easy
- POST http://localhost:5000/sudoku_solution
- POST http://localhost:5000/hex_sudoku_solution
- POST http://localhost:5000/sudoku_hint
- POST http://localhost:5000/hex_sudoku_hint

## Next Steps

1. Try generating a standard Sudoku puzzle
2. Try generating a hex Sudoku puzzle
3. Play a game and validate your solution
4. Use the hint feature
5. Run the test suite

Enjoy GRIDMASTERS! 🎮
