import os
import traceback
from flask import Blueprint, request, jsonify, current_app
from openai import OpenAI  # pylint: disable=import-error

from app.sudoku_generator import SudokuGenerator, HexSudokuGenerator

bp = Blueprint('api', __name__)

# Initialize generators
sudoku_gen = SudokuGenerator(size=9)
hex_sudoku_gen = HexSudokuGenerator()

# Initialize OpenAI client lazily to avoid requiring API key during import
_OPENAI_CLIENT = None


def get_openai_client():
    """Get or create OpenAI client instance."""
    global _OPENAI_CLIENT  # pylint: disable=global-statement
    if _OPENAI_CLIENT is None:
        # Check if we're in test mode
        api_key = os.environ.get('OPENAI_API_KEY')
        if api_key or not os.environ.get('PYTEST_CURRENT_TEST'):
            _OPENAI_CLIENT = OpenAI(api_key=api_key or 'test-key-for-testing')
    return _OPENAI_CLIENT


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


@bp.route('/hint', methods=['GET'])
def get_hint():
    """
    GET hint
    Takes in an integer and returns an llm-generated hint for solving the Sudoku puzzle.
    Query params:
        puzzle_solution: A 2D list representing the Sudoku solution.
        target_cell: A tuple (row, col) indicating the cell for which the hint is requested.
    """
    number = request.args.get('number', None)
    if number is None:
        return jsonify({"error": "Number parameter is required"}), 400
    try:
        number = int(number)
        if not 1 <= number <= 9:
            return jsonify({"error": "Number must be between 1 and 9"}), 400

        open_ai = get_openai_client()
        if not open_ai:
            return jsonify({"error": "OpenAI client not configured"}), 503

        response = open_ai.responses.create(
            model="gpt-4o",
            input=f"""
            Role: You are a Sudoku Riddle Master.
            Goal: Provide an easy riddle where the answer is the given number. The number is from a game of either regular Sudoku, or Hexadecimal Sudoku.
            Input: {number}
            Output: A hint of no more than 3 sentences, which guides the player to the correct number to place into the given spot.
            """
        )

        hint = response.output_text

        current_app.logger.info(f"Generated hint for number: {number}")

        return jsonify({
            "hint": hint,
            "tokents": response.usage.total_tokens
        }), 200

    except ValueError:
        return jsonify({"error": "Number must be an integer"}), 400
    except Exception as e:
        current_app.logger.error(f"Error generating hint: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Internal server error"}), 500


@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200
