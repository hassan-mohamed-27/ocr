from app.services.ocr.ocr_interface import OCRInterface
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
import cv2
import yaml
import easyocr
import logging

class EasyOCRBackend(OCRInterface):
    """
    EasyOCR implementation for text extraction.
    
    This backend:
    - Uses EasyOCR's deep learning models
    - Supports English and Arabic languages
    - Performs region-based text detection
    - Optimized for accuracy over speed
    
    Note:
        Initializes without GPU support by default
        Uses DBNet as the text detector
    """
    def __init__(self):
        self.reader = easyocr.Reader(['en', 'ar'], gpu=False, detector='dbnet')

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

                    result = self.reader.readtext(enlarged_roi, detail=0)
                    text = " ".join(result)
                    file.write(f"Text in {area_name}: {text.strip()}\n")
                    file.write("-" * 50 + "\n")
            logging.info(f"Detected text saved to: {output_file}")
        except IOError as e:
            logging.error(f"Error saving file: {e}")