from flask import Flask
from app.routes.auth import auth_bp
from app.routes.monitor import monitor_bp
from app.routes.ocr import ocr_bp
from app.routes.upload import upload_bp
import logging

def create_app():
    """
    Create and configure the Flask application.
    
    This factory function:
    - Creates a new Flask application instance
    - Registers all blueprints (auth, monitor, ocr, upload)
    - Configures basic logging
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(monitor_bp)
    app.register_blueprint(ocr_bp)
    app.register_blueprint(upload_bp)

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)