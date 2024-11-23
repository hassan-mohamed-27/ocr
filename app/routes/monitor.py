from flask import Blueprint, request, jsonify
from app.services.google_drive_service import GoogleDriveService
from app.utils.config import CREDENTIALS_PATH, TOKEN_PATH
import logging
import threading

monitor_bp = Blueprint('monitor', __name__)

"""
Blueprint for monitoring routes.

This blueprint handles:
- Starting monitoring of a Google Drive folder for new files
- Monitoring Google Drive folders for new files
"""

drive_service = GoogleDriveService(CREDENTIALS_PATH, TOKEN_PATH)
monitor_thread = None

@monitor_bp.route('/monitor', methods=['POST'])
def monitor():
    """
    Start monitoring a Google Drive folder for new files.

    Expects JSON payload:
        folder_name (str): Name of the Google Drive folder to monitor

    Returns:
        200: Monitoring started successfully
        400: Invalid request or monitoring already in progress
        401: Not authenticated
        500: Server error

    Note:
        - Creates a background thread for continuous monitoring
        - Only one monitoring thread can be active at a time
    """
    data = request.get_json()
    folder_name = data.get('folder_name')

    if not drive_service:
        return jsonify({"error": "Not logged in"}), 401

    try:
        folder_id = drive_service.get_folder_id_by_name(folder_name)

        global monitor_thread
        if monitor_thread and monitor_thread.is_alive():
            return jsonify({"message": "Monitoring already in progress"}), 400

        monitor_thread = threading.Thread(target=drive_service.monitor_folder, args=(folder_id,))
        monitor_thread.start()

        return jsonify({"message": "Monitoring started"}), 200
    except ValueError as e:
        logging.error(f"Monitoring error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Monitoring error: {e}")
        return jsonify({"error": "Failed to start monitoring"}), 500