from flask import Blueprint, request, jsonify
import os
import logging

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload_yaml', methods=['POST'])
def upload_yaml():
    """
    Endpoint to upload a YAML file.

    Expects:
        - 'yaml_file': YAML file in multipart/form-data

    Returns:
        JSON with status message.
    """
    if 'yaml_file' not in request.files:
        return jsonify({"error": "No YAML file provided"}), 400

    file = request.files['yaml_file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    if not file.filename.endswith(('.yaml', '.yml')):
        return jsonify({"error": "Invalid file type. Only YAML files are allowed."}), 400

    # Save the uploaded YAML file as 'detection_areas.yaml' in the 'downloads' folder
    yaml_path = os.path.join('downloads', 'detection_areas.yaml')
    os.makedirs('downloads', exist_ok=True)
    file.save(yaml_path)

    return jsonify({"message": "YAML file uploaded successfully.", "file_path": yaml_path}), 200

@upload_bp.route('/upload_image', methods=['POST'])
def upload_image():
    """
    Endpoint to upload an image file to the 'downloads' folder.

    Expects:
        - 'image': Image file in multipart/form-data

    Returns:
        JSON with status message and file path.
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    if not image_file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        return jsonify({"error": "Invalid file type. Only image files are allowed."}), 400

    # Save the uploaded image to the 'downloads' folder
    download_path = os.path.join('downloads', image_file.filename)
    os.makedirs('downloads', exist_ok=True)
    image_file.save(download_path)

    return jsonify({"message": "Image uploaded successfully.", "file_path": download_path}), 200