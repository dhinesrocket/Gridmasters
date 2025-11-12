from flask import Blueprint, request, jsonify, current_app
from app.sudoku_generator import SudokuGenerator, HexSudokuGenerator
from app.sudoku_validator import SudokuValidator, HexSudokuValidator
import traceback

bp = Blueprint('api', __name__)

# Initialize generators and validators
sudoku_gen = SudokuGenerator(size=9)
hex_sudoku_gen = HexSudokuGenerator()
sudoku_val = SudokuValidator(size=9)
hex_sudoku_val = HexSudokuValidator()


def validate_board_input(board, expected_size):
    """
    Validate board input structure and content.
    Args:
        board: The board to validate
        expected_size: Expected board size (9 or 16)
    Returns:
        tuple: (is_valid, error_message)
    """
    if not isinstance(board, list):
        return False, "Board must be a list"
    
    if len(board) != expected_size:
        return False, f"Board must have {expected_size} rows"
    
    for i, row in enumerate(board):
        if not isinstance(row, list):
            return False, f"Row {i} must be a list"
        if len(row) != expected_size:
            return False, f"Row {i} must have {expected_size} columns"
    
    return True, None


@bp.route('/sudoku_puzzle', methods=['GET'])
def get_sudoku_puzzle():
    """
    GET sudoku_puzzle
    Retrieves a new standard Sudoku puzzle (numbers 1-9).
    Query params:
        difficulty: 'easy', 'medium', or 'hard' (default: 'medium')
    """
    try:
        difficulty = request.args.get('difficulty', 'medium').lower()
        
        if difficulty not in ['easy', 'medium', 'hard']:
            current_app.logger.warning(f"Invalid difficulty requested: {difficulty}")
            return jsonify({"error": "Difficulty must be 'easy', 'medium', or 'hard'"}), 400
        
        puzzle = sudoku_gen.generate_puzzle(difficulty)
        current_app.logger.info(f"Generated standard Sudoku puzzle with difficulty: {difficulty}")
        
        return jsonify({
            "puzzle": puzzle,
            "difficulty": difficulty,
            "size": 9
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error generating sudoku puzzle: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Internal server error"}), 500


@bp.route('/hex_sudoku_puzzle', methods=['GET'])
def get_hex_sudoku_puzzle():
    """
    GET hex_sudoku_puzzle
    Retrieves a new hexadecimal Sudoku puzzle (hex values 0-F).
    Query params:
        difficulty: 'easy', 'medium', or 'hard' (default: 'medium')
    """
    try:
        difficulty = request.args.get('difficulty', 'medium').lower()
        
        if difficulty not in ['easy', 'medium', 'hard']:
            current_app.logger.warning(f"Invalid difficulty requested: {difficulty}")
            return jsonify({"error": "Difficulty must be 'easy', 'medium', or 'hard'"}), 400
        
        puzzle = hex_sudoku_gen.generate_puzzle(difficulty)
        current_app.logger.info(f"Generated hex Sudoku puzzle with difficulty: {difficulty}")
        
        return jsonify({
            "puzzle": puzzle,
            "difficulty": difficulty,
            "size": 16
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error generating hex sudoku puzzle: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Internal server error"}), 500


@bp.route('/sudoku_solution', methods=['POST'])
def validate_sudoku_solution():
    """
    POST sudoku_solution
    Validates a submitted solution for a standard Sudoku puzzle.
    Request body:
        puzzle_solution: The completed puzzle submitted by the user
        puzzle_state: The original puzzle state
    Returns:
        bool: true if solution is correct, false otherwise
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400
        
        if 'puzzle_solution' not in data or 'puzzle_state' not in data:
            return jsonify({"error": "Both 'puzzle_solution' and 'puzzle_state' are required"}), 400
        
        puzzle_solution = data['puzzle_solution']
        puzzle_state = data['puzzle_state']
        
        # Validate input structure
        is_valid, error = validate_board_input(puzzle_solution, 9)
        if not is_valid:
            current_app.logger.warning(f"Invalid puzzle_solution: {error}")
            return jsonify({"error": f"Invalid puzzle_solution: {error}"}), 400
        
        is_valid, error = validate_board_input(puzzle_state, 9)
        if not is_valid:
            current_app.logger.warning(f"Invalid puzzle_state: {error}")
            return jsonify({"error": f"Invalid puzzle_state: {error}"}), 400
        
        # Validate solution
        is_correct = sudoku_val.validate_solution(puzzle_state, puzzle_solution)
        current_app.logger.info(f"Standard Sudoku solution validation: {is_correct}")
        
        return jsonify({"valid": is_correct}), 200
        
    except Exception as e:
        current_app.logger.error(f"Error validating sudoku solution: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Internal server error"}), 500


@bp.route('/hex_sudoku_solution', methods=['POST'])
def validate_hex_sudoku_solution():
    """
    POST hex_sudoku_solution
    Validates a submitted solution for a hexadecimal Sudoku puzzle.
    Request body:
        puzzle_solution: The completed hex puzzle submitted by the user
        puzzle_state: The original hex puzzle state
    Returns:
        bool: true if solution is correct, false otherwise
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400
        
        if 'puzzle_solution' not in data or 'puzzle_state' not in data:
            return jsonify({"error": "Both 'puzzle_solution' and 'puzzle_state' are required"}), 400
        
        puzzle_solution = data['puzzle_solution']
        puzzle_state = data['puzzle_state']
        
        # Validate input structure
        is_valid, error = validate_board_input(puzzle_solution, 16)
        if not is_valid:
            current_app.logger.warning(f"Invalid puzzle_solution: {error}")
            return jsonify({"error": f"Invalid puzzle_solution: {error}"}), 400
        
        is_valid, error = validate_board_input(puzzle_state, 16)
        if not is_valid:
            current_app.logger.warning(f"Invalid puzzle_state: {error}")
            return jsonify({"error": f"Invalid puzzle_state: {error}"}), 400
        
        # Validate solution
        is_correct = hex_sudoku_val.validate_solution(puzzle_state, puzzle_solution)
        current_app.logger.info(f"Hex Sudoku solution validation: {is_correct}")
        
        return jsonify({"valid": is_correct}), 200
        
    except Exception as e:
        current_app.logger.error(f"Error validating hex sudoku solution: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Internal server error"}), 500


@bp.route('/sudoku_hint', methods=['POST'])
def get_sudoku_hint():
    """
    POST sudoku_hint
    Provides a hint for a standard Sudoku puzzle.
    Request body:
        puzzle: The current state of the puzzle
    Returns:
        hint: string - Description or guidance for the hint
        cell_index: int - Cell position identifier for the hint
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400
        
        if 'puzzle' not in data:
            return jsonify({"error": "'puzzle' is required"}), 400
        
        puzzle = data['puzzle']
        
        # Validate input structure
        is_valid, error = validate_board_input(puzzle, 9)
        if not is_valid:
            current_app.logger.warning(f"Invalid puzzle: {error}")
            return jsonify({"error": f"Invalid puzzle: {error}"}), 400
        
        # Get hint
        hint_text, cell_index = sudoku_val.get_hint(puzzle)
        current_app.logger.info(f"Generated hint for standard Sudoku at cell {cell_index}")
        
        return jsonify({
            "hint": hint_text,
            "cell_index": cell_index
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error generating sudoku hint: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Internal server error"}), 500


@bp.route('/hex_sudoku_hint', methods=['POST'])
def get_hex_sudoku_hint():
    """
    POST hex_sudoku_hint
    Provides a hint for a hexadecimal Sudoku puzzle.
    Request body:
        puzzle: The current state of the hex puzzle
    Returns:
        hint: string - Description or guidance for the hint
        cell_index: int - Cell position identifier for the hint
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400
        
        if 'puzzle' not in data:
            return jsonify({"error": "'puzzle' is required"}), 400
        
        puzzle = data['puzzle']
        
        # Validate input structure
        is_valid, error = validate_board_input(puzzle, 16)
        if not is_valid:
            current_app.logger.warning(f"Invalid puzzle: {error}")
            return jsonify({"error": f"Invalid puzzle: {error}"}), 400
        
        # Get hint
        hint_text, cell_index = hex_sudoku_val.get_hint(puzzle)
        current_app.logger.info(f"Generated hint for hex Sudoku at cell {cell_index}")
        
        return jsonify({
            "hint": hint_text,
            "cell_index": cell_index
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error generating hex sudoku hint: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Internal server error"}), 500


@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200
