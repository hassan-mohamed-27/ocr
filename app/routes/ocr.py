from flask import Blueprint, request, jsonify
import os
import logging
from app.services.google_drive_service import GoogleDriveService
from app.services.ocr.pytesseract_backend import PytesseractOCR
from app.services.ocr.easyocr_backend import EasyOCRBackend
from app.services.ocr.genai_backend import GenAIOCRBackend
from app.utils.text_parser import parse_detected_text
import yaml

ocr_bp = Blueprint('ocr', __name__)

drive_service = GoogleDriveService('client_secret.json', 'token.json')

# Initialize OCR backends
pytesseract_ocr = PytesseractOCR()
easyocr_backend = EasyOCRBackend()

@ocr_bp.route('/extract_invoice', methods=['POST'])
def extract_invoice():
    """
    Endpoint to extract invoice details from an existing image in the downloads folder.

    Expects:
        - 'filename': Name of the image file in the 'downloads' folder
        - 'ocr_backend': String indicating which OCR backend to use ('pytesseract', 'easyocr', 'genai')
        - 'genai_api_key': Required if 'ocr_backend' is 'genai'

    Returns:
        JSON with fields:
            - invoice_number
            - date
            - second_product_amount
            - total_amount
    """
    filename = request.form.get('filename')
    if not filename:
        return jsonify({"error": "No filename provided"}), 400

    image_path = os.path.join('downloads', filename)
    if not os.path.exists(image_path):
        return jsonify({"error": f"File '{filename}' does not exist in downloads folder"}), 400

    ocr_backend_name = request.form.get('ocr_backend', 'pytesseract').lower()
    genai_api_key = request.form.get('genai_api_key')  # Only needed for GenAI

    if ocr_backend_name not in ['pytesseract', 'easyocr', 'genai']:
        return jsonify({"error": "Invalid OCR backend specified"}), 400

    if ocr_backend_name == 'genai' and not genai_api_key:
        return jsonify({"error": "genai_api_key is required for 'genai' OCR backend"}), 400

    # Initialize OCR instance
    if ocr_backend_name == 'pytesseract':
        ocr_instance = pytesseract_ocr
    elif ocr_backend_name == 'easyocr':
        ocr_instance = easyocr_backend
    elif ocr_backend_name == 'genai':
        ocr_instance = GenAIOCRBackend(genai_api_key)

    detection_areas = ocr_instance.load_detection_areas(yaml_path=os.path.join('downloads', 'detection_areas.yaml'))

    # Perform OCR
    try:
        detected_text_file = os.path.join('downloads', 'detected_text.txt')
        if ocr_backend_name == 'genai':
            ocr_instance.perform_ocr(image_path, detection_areas, output_file=detected_text_file, prompt="Extract text from the image.")
        else:
            ocr_instance.perform_ocr(image_path, detection_areas, output_file=detected_text_file)

        # Parse the detected text to extract required fields
        extracted_data = parse_detected_text(detected_text_file)

        # Clean up detected text file
        os.remove(detected_text_file)

        return jsonify(extracted_data), 200
    except Exception as e:
        logging.error(f"OCR extraction error: {e}")
        return jsonify({"error": "Failed to extract invoice data"}), 500