from flask import Blueprint, request, jsonify
from app.services.google_drive_service import GoogleDriveService
from app.utils.config import CREDENTIALS_PATH, TOKEN_PATH
import logging
import threading

monitor_bp = Blueprint('monitor', __name__)

drive_service = GoogleDriveService(CREDENTIALS_PATH, TOKEN_PATH)
monitor_thread = None

@monitor_bp.route('/monitor', methods=['POST'])
def monitor():
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