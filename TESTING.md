# GridMasters Test Suite

This document describes the test coverage and how to run tests for the GridMasters Sudoku application.

## Test Coverage Summary

### Backend Coverage: 74%
- **40 tests passing, 5 skipped**
- Routes: 100% coverage
- App initialization: 96% coverage  
- Sudoku generator: 85% coverage
- Validator: 49% coverage (deprecated module, low priority)

### Frontend Tests: 38 tests passing
- sudokuUtils.js: 16 tests
- API service: 8 tests
- GameBoard component: 14 tests

## Running Tests

### Backend Tests (Python/Pytest)

```bash
# From project root
cd backend
python -m venv venv  # If not already created
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run all backend tests
pytest tests/backend

# Run with coverage report
pytest tests/backend --cov=backend/app --cov-report=term-missing

# Run specific test file
pytest tests/backend/test_routes.py -v
```

### Frontend Tests (Vitest)

```bash
# From project root  
cd frontend

# Install dependencies (if not already done)
npm install

# Run all frontend tests
npm test -- --run

# Run tests in watch mode
npm test

# Run with UI
npm run test:ui
```

## Test Files

### Backend Tests (`tests/backend/`)
- `test_app_init.py` - Application factory and initialization tests
- `test_routes.py` - API endpoint tests
- `test_routes_extended.py` - Extended API tests with CORS
- `test_error_handling.py` - Error handling and edge cases
- `test_sudoku_generator_extended.py` - Generator validation tests
- `test_sudoku_logic.py` - Core Sudoku logic tests
- `test_sudoku_validator_extended.py` - Validator tests (deprecated/skipped)

### Frontend Tests (`frontend/tests/`)
- `sudokuUtils.test.js` - Utility function tests (16 tests)
  - hideCells() - Cell hiding based on difficulty
  - validateBoard() - Solution validation
  - getHint() - Hint generation
  - getCellCounts() - Board state tracking
- `api.test.js` - API service tests (8 tests)
  - Configuration validation
  - Error handling
  - Endpoint structure
- `GameBoard.test.js` - Component tests (14 tests)
  - Rendering
  - User input handling
  - Event emissions
  - Props validation

## What's Tested

### Backend
✅ Complete puzzle generation (9x9 and 16x16 hex)  
✅ API endpoints return correct data format
✅ Error handling for invalid inputs
✅ CORS headers
✅ Application initialization
✅ Generator retry mechanism
✅ Super easy mode (3-4 empty cells)

### Frontend
✅ Cell hiding based on difficulty
✅ Solution validation
✅ Hint generation
✅ User input handling (standard and hex modes)
✅ Component rendering
✅ Event handling
✅ Board state management

## What's NOT Tested (Known Gaps)

### Backend (26% uncovered)
- `_remove_numbers()` methods in generators (deprecated, unused)
- `_convert_to_hex()` internal method (covered indirectly)
- Production logging setup (requires non-test environment)
- Deprecated validator methods (marked as skipped)

### Frontend
- App.vue component (complex integration, requires full DOM)
- End-to-end user workflows
- Visual regression testing

## Architecture Notes

**Important**: The validation architecture changed in the latest version:
- Backend now returns **complete solutions** only
- Frontend handles **hiding cells** based on difficulty
- Frontend performs **all validation**
- Backend validator module is **deprecated** (tests marked as skipped)

This means backend "puzzle" endpoints actually return solutions, and frontend creates puzzles by hiding cells.

## Test Configuration

### Backend (`pytest.ini`)
```ini
[pytest]
testpaths = tests/backend
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

### Frontend (`vite.config.js`)
```javascript
test: {
  globals: true,
  environment: 'happy-dom',
  pool: 'forks',
  poolOptions: {
    forks: {
      singleFork: true
    }
  }
}
```

## Continuous Integration

Tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Backend Tests
  run: |
    cd backend
    pip install -r requirements.txt
    pytest tests/backend --cov=backend/app

- name: Frontend Tests  
  run: |
    cd frontend
    npm install
    npm test -- --run
```

## Contributing

When adding new features:
1. Write tests first (TDD approach recommended)
2. Aim for >80% coverage on new code
3. Run full test suite before committing
4. Update this README if test structure changes

## Troubleshooting

### Backend
- **Import errors**: Make sure you're in the backend directory and venv is activated
- **Module not found**: Run `pip install -r requirements.txt`

### Frontend  
- **Timeout errors**: Use `pool: 'forks'` in vite.config.js (Windows path issue)
- **Module errors**: Run `npm install` to ensure all dependencies are installed
- **Tests hang**: Use `--run` flag for one-time execution

## Test Metrics

Last updated: 2025-11-13

| Component | Files | Tests | Passed | Skipped | Coverage |
|-----------|-------|-------|--------|---------|----------|
| Backend   | 7     | 45    | 40     | 5       | 74%      |
| Frontend  | 3     | 38    | 38     | 0       | N/A      |
| **Total** | **10**| **83**| **78** | **5**   | **74%**  |
