# GRIDMASTERS - Terminal Sudoku

A modern Sudoku game with both standard (9x9) and hexadecimal (16x16) variants, featuring a retro Linux terminal-style interface.

## Features

- 🎮 **Two Game Modes**: Standard Sudoku (1-9) and Hex Sudoku (0-F)
- 🎯 **Three Difficulty Levels**: Easy, Medium, and Hard
- 💡 **Smart Hints**: Get contextual hints when you're stuck
- ✅ **Solution Validation**: Check your solution in real-time
- 🖥️ **Terminal Aesthetics**: Beautiful retro terminal-style UI
- 🔒 **Secure Backend**: Input validation and error handling
- ✨ **Modern Tech Stack**: Flask + Vue.js

## Architecture

### Backend (Flask)
- **Flask REST API** with CORS support
- **Sudoku Generator**: Algorithm to create valid puzzles
- **Sudoku Validator**: Solution verification and hint generation
- **Security**: Input validation, request size limits, logging
- **Testing**: Comprehensive unit and integration tests

### Frontend (Vue.js)
- **Vue 3** with Composition API
- **Vite** for fast development
- **Terminal UI**: Custom CSS for Linux terminal aesthetics
- **State Management**: Maintained on frontend
- **API Integration**: Axios for HTTP requests

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask server:
```bash
python run.py
```

The backend will start on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will start on `http://localhost:3000`

## Running Tests

### Backend Tests

```bash
cd backend
pytest
```

For coverage report:
```bash
pytest --cov=app tests/
```

## API Documentation

See [docs/Routes.md](docs/Routes.md) for complete API documentation.

### Quick Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sudoku_puzzle` | GET | Get a standard Sudoku puzzle |
| `/hex_sudoku_puzzle` | GET | Get a hex Sudoku puzzle |
| `/sudoku_solution` | POST | Validate standard Sudoku solution |
| `/hex_sudoku_solution` | POST | Validate hex Sudoku solution |
| `/sudoku_hint` | POST | Get hint for standard Sudoku |
| `/hex_sudoku_hint` | POST | Get hint for hex Sudoku |
| `/health` | GET | Health check |

## Usage

1. **Start the backend server** (port 5000)
2. **Start the frontend dev server** (port 3000)
3. **Open your browser** to `http://localhost:3000`
4. **Select game mode**: Standard or Hex
5. **Choose difficulty**: Easy, Medium, or Hard
6. **Play**: Fill in the empty cells (marked as 0)
7. **Get hints** when stuck using the `[?] GET HINT` button
8. **Validate** your solution with the `[✓] VALIDATE` button
9. **Start new game** with the `[↻] NEW GAME` button

## Project Structure

```
Gridmasters/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── routes.py            # API endpoints
│   │   ├── sudoku_generator.py  # Puzzle generation
│   │   └── sudoku_validator.py  # Solution validation
│   ├── tests/
│   │   ├── conftest.py          # Test configuration
│   │   ├── test_routes.py       # API tests
│   │   └── test_sudoku_logic.py # Logic tests
│   ├── requirements.txt         # Python dependencies
│   └── run.py                   # Application entry point
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── GameBoard.vue    # Game board component
│   │   ├── services/
│   │   │   └── api.js           # API client
│   │   ├── App.vue              # Main app component
│   │   └── main.js              # Application entry
│   ├── index.html               # HTML template
│   ├── package.json             # Node dependencies
│   └── vite.config.js           # Vite configuration
├── docs/
│   └── Routes.md                # API documentation
└── README.md                    # This file
```

## Technologies Used

### Backend
- **Flask 3.0** - Web framework
- **Flask-CORS** - Cross-origin resource sharing
- **pytest** - Testing framework
- **python-dotenv** - Environment configuration

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **Vite** - Next generation frontend tooling
- **Axios** - HTTP client
- **IBM Plex Mono** - Terminal-style font

## Security Features

- ✅ Input validation on all endpoints
- ✅ Request size limits (16 KB max)
- ✅ CORS configuration
- ✅ Error logging
- ✅ Type checking for board dimensions
- ✅ Sanitized error messages

## Development

### Adding New Features

1. **Backend**: Add endpoint in `backend/app/routes.py`
2. **Frontend**: Add API method in `frontend/src/services/api.js`
3. **UI**: Update components in `frontend/src/components/`
4. **Tests**: Add tests in `backend/tests/`

### Environment Variables

Create a `.env` file in the backend directory:

```env
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
PORT=5000
```

## Troubleshooting

### Backend won't start
- Check if port 5000 is available
- Ensure all dependencies are installed
- Check Python version (3.8+)

### Frontend won't start
- Check if port 3000 is available
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` and reinstall

### CORS errors
- Ensure backend is running on port 5000
- Check CORS configuration in `backend/app/__init__.py`

### Tests failing
- Activate virtual environment
- Ensure all dependencies are installed
- Check Python path in `conftest.py`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Credits

Developed with ❤️ using Flask and Vue.js

---

**Enjoy playing GRIDMASTERS!** 🎮