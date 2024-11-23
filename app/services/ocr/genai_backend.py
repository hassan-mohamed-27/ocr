from app.services.ocr.ocr_interface import OCRInterface
import os
import cv2
import yaml
import google.generativeai as genai
import logging

class GenAIOCRBackend(OCRInterface):
    """
    Google's Generative AI implementation for text extraction.
    
    This backend:
    - Uses Google's Gemini model for text extraction
    - Supports multiple languages
    - Can handle complex document layouts
    - Allows custom prompts for extraction
    
    Note:
        Requires valid Google GenAI API key
        Uses experimental Gemini model version
    """
    def __init__(self, api_key):
        genai.configure(api_key=api_key)

    def load_detection_areas(self, yaml_path='detection_areas.yaml'):
        """
        Load detection areas from a YAML configuration file.

        Args:
            yaml_path (str): Path to the YAML configuration file

        Returns:
            dict: Dictionary containing area coordinates in format:
                {
                    'area_name': [x, y, width, height],
                    ...
                }

        Raises:
            IOError: If YAML file cannot be read
            yaml.YAMLError: If YAML file is malformed
        """
        with open(yaml_path, 'r') as f:
            areas = yaml.safe_load(f)
        return areas

    def preprocess_image(self, image):
        """
        Preprocess image before OCR processing.

        Args:
            image (numpy.ndarray): Input image in BGR format

        Returns:
            numpy.ndarray: Preprocessed image (typically grayscale)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Enhance contrast here if needed
        return gray

    def send_to_genai_api(self, image, prompt):
        """
        Send image to Google's Generative AI API for text extraction.

        Args:
            image (numpy.ndarray): Preprocessed image
            prompt (str): Instruction prompt for the AI model

        Returns:
            str: Extracted text from the image

        Note:
            Creates a temporary file for API upload
            Uses Gemini experimental model for OCR
        """
        try:
            temp_image_path = 'temp_image.jpg'
            cv2.imwrite(temp_image_path, image)
            myfile = genai.upload_file(temp_image_path)
            model = genai.GenerativeModel(model_name="gemini-exp-1121")
            result = model.generate_content([myfile, "\n\n", prompt])
            os.remove(temp_image_path)

            return result.text.strip()
        except Exception as e:
            logging.error(f"GenAI request failed: {e}")
            return ""

    def perform_ocr(self, image_path, detection_areas=None, output_file='detected_text.txt', prompt="Provide OCR text from this image."):
        """
        Perform OCR on specified image regions.

        Args:
            image_path (str): Path to the input image
            detection_areas (dict, optional): Dictionary of areas to process
                Format: {'area_name': [x, y, width, height]}
            output_file (str): Path where detected text will be saved
            prompt (str): Instruction prompt for the AI model

        Raises:
            IOError: If image cannot be read or output cannot be saved
            Exception: If OCR processing fails
        """
        image = cv2.imread(image_path)
        if detection_areas is None:
            detection_areas = self.load_detection_areas()

        try:
            with open(output_file, "w", encoding="utf-8") as file:
                for area_name, area in detection_areas.items():
                    x, y, w, h = area
                    roi = image[y:y+h, x:x+w]
                    preprocessed_roi = self.preprocess_image(roi)
                    enlarged_roi = cv2.resize(preprocessed_roi, None, fx=3, fy=3, interpolation=cv2.INTER_LANCZOS4)

                    text = self.send_to_genai_api(enlarged_roi, prompt)
                    file.write(f"Text in {area_name}: {text}\n")
                    file.write("-" * 50 + "\n")
            logging.info(f"Detected text saved to: {output_file}")
        except IOError as e:
            logging.error(f"Error saving file: {e}")