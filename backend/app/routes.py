import traceback
from flask import Blueprint, request, jsonify, current_app
from app.sudoku_generator import SudokuGenerator, HexSudokuGenerator

bp = Blueprint('api', __name__)

# Initialize generators
sudoku_gen = SudokuGenerator(size=9)
hex_sudoku_gen = HexSudokuGenerator()


@bp.route('/sudoku_puzzle', methods=['GET'])
def get_sudoku_puzzle():
    """
    GET sudoku_puzzle
    Retrieves a complete standard Sudoku solution (numbers 1-9).
    Query params:
        difficulty: 'easy', 'medium', or 'hard' (default: 'medium') - kept for API compatibility
    Note: Returns a complete solution. Frontend should hide cells based on difficulty.
    """
    try:
        difficulty = request.args.get('difficulty', 'medium').lower()

        if difficulty not in ['super_easy', 'easy', 'medium', 'hard']:
            current_app.logger.warning(f"Invalid difficulty requested: {difficulty}")
            return jsonify({"error": "Difficulty must be 'super_easy', 'easy', 'medium', or 'hard'"}), 400

        solution = sudoku_gen.generate_puzzle(difficulty)
        current_app.logger.info(f"Generated standard Sudoku solution with difficulty: {difficulty}")

        return jsonify({
            "solution": solution,
            "difficulty": difficulty,
            "size": 9
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error generating sudoku solution: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Internal server error"}), 500


@bp.route('/hex_sudoku_puzzle', methods=['GET'])
def get_hex_sudoku_puzzle():
    """
    GET hex_sudoku_puzzle
    Retrieves a complete hexadecimal Sudoku solution (hex values 0-F).
    Query params:
        difficulty: 'easy', 'medium', or 'hard' (default: 'medium') - kept for API compatibility
    Note: Returns a complete solution. Frontend should hide cells based on difficulty.
    """
    try:
        difficulty = request.args.get('difficulty', 'medium').lower()

        if difficulty not in ['super_easy', 'easy', 'medium', 'hard']:
            current_app.logger.warning(f"Invalid difficulty requested: {difficulty}")
            return jsonify({"error": "Difficulty must be 'super_easy', 'easy', 'medium', or 'hard'"}), 400

        solution = hex_sudoku_gen.generate_puzzle(difficulty)
        current_app.logger.info(f"Generated hex Sudoku solution with difficulty: {difficulty}")

        return jsonify({
            "solution": solution,
            "difficulty": difficulty,
            "size": 16
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error generating hex sudoku solution: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Internal server error"}), 500


@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200
