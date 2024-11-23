from flask import Blueprint, jsonify
from app.services.google_drive_service import GoogleDriveService
from app.utils.config import CREDENTIALS_PATH, TOKEN_PATH
import logging

auth_bp = Blueprint('auth', __name__)

"""
Blueprint for authentication-related routes.

This blueprint handles:
- Google Drive OAuth2 authentication
- User session management
"""

drive_service = GoogleDriveService(CREDENTIALS_PATH, TOKEN_PATH)

@auth_bp.route('/login', methods=['GET'])
def login():
    """
    Authenticate user with Google Drive.

    Returns:
        200: Login successful
        500: Authentication failed
    """
    try:
        drive_service.login()
        return jsonify({"message": "Login successful"}), 200
    except Exception as e:
        logging.error(f"Login error: {e}")
        return jsonify({"error": "Login failed"}), 500