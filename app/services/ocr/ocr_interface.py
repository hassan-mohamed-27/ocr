from abc import ABC, abstractmethod

class OCRInterface(ABC):
    @abstractmethod
    def load_detection_areas(self, yaml_path='detection_areas.yaml'):
        pass

    @abstractmethod
    def preprocess_image(self, image):
        pass

    @abstractmethod
    def perform_ocr(self, image_path, detection_areas=None, output_file='detected_text.txt'):
        pass 