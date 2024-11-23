from abc import ABC, abstractmethod

class OCRInterface(ABC):
    """
    Abstract base class defining the interface for OCR implementations.
    
    All OCR backend implementations must inherit from this class and
    implement its abstract methods.
    """

    @abstractmethod
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
        pass

    @abstractmethod
    def preprocess_image(self, image):
        """
        Preprocess image before OCR processing.
        
        Args:
            image (numpy.ndarray): Input image in BGR format
            
        Returns:
            numpy.ndarray: Preprocessed image (typically grayscale)
        """
        pass

    @abstractmethod
    def perform_ocr(self, image_path, detection_areas=None, output_file='detected_text.txt'):
        """
        Perform OCR on specified image regions.
        
        Args:
            image_path (str): Path to the input image
            detection_areas (dict, optional): Dictionary of areas to process
                Format: {'area_name': [x, y, width, height]}
            output_file (str): Path where detected text will be saved
            
        Raises:
            IOError: If image cannot be read or output cannot be saved
            Exception: If OCR processing fails
        """
        pass 