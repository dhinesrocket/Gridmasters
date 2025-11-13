import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_cors import CORS

def create_app():
    """Application factory pattern."""
    app = Flask(__name__)
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024  # 16 KB max request size
    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}}) 
    # Setup logging
    if not app.debug and not os.environ.get("PYTEST_CURRENT_TEST"):
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/gridmasters.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Gridmasters startup')
    # Register routes
    from . import routes
    app.register_blueprint(routes.bp)
    return app
