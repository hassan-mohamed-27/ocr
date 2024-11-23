from app.services.ocr.ocr_interface import OCRInterface
import os
import cv2
import yaml
import google.generativeai as genai
import logging

class GenAIOCRBackend(OCRInterface):
    def __init__(self, api_key):
        genai.configure(api_key=api_key)

    def load_detection_areas(self, yaml_path='detection_areas.yaml'):
        with open(yaml_path, 'r') as f:
            areas = yaml.safe_load(f)
        return areas

    def preprocess_image(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Enhance contrast here if needed
        return gray

    def send_to_genai_api(self, image, prompt):
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