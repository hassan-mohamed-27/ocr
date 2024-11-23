from app.services.ocr.ocr_interface import OCRInterface
import os
import cv2
import yaml
import pytesseract
import logging

class PytesseractOCR(OCRInterface):
    def __init__(self):
        # Configure the path to Tesseract executable if needed
        # Uncomment and update the line below if Tesseract is not in your PATH
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass

    def load_detection_areas(self, yaml_path='detection_areas.yaml'):
        with open(yaml_path, 'r') as f:
            areas = yaml.safe_load(f)
        return areas

    def preprocess_image(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Enhance contrast here if needed
        return gray

    def perform_ocr(self, image_path, detection_areas=None, output_file='detected_text.txt'):
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
                    
                    config = "--psm 12 --oem 1"
                    text = pytesseract.image_to_string(enlarged_roi, lang='ara2+eng', config=config)
                    file.write(f"Text in {area_name}: {text.strip()}\n")
                    file.write("-" * 50 + "\n")
            logging.info(f"Detected text saved to: {output_file}")
        except IOError as e:
            logging.error(f"Error saving file: {e}")