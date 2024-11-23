import cv2
import yaml
import numpy as np

class AreaSelector:
    def __init__(self, image_path):
        # Read the image
        self.image = cv2.imread(image_path)
        self.original = self.image.copy()
        self.areas = []
        self.current_area = None
        self.drawing = False

    def draw_rectangle(self, event, x, y, flags, param):
        """
        Mouse callback function to draw rectangles
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            # Start drawing
            self.drawing = True
            self.current_area = [(x, y)]

        elif event == cv2.EVENT_MOUSEMOVE:
            # Draw rectangle while mouse is moving with left button pressed
            if self.drawing:
                # Reset image to original
                self.image = self.original.copy()
                # Draw temporary rectangle
                cv2.rectangle(self.image, self.current_area[0], (x, y), (0, 255, 0), 2)

        elif event == cv2.EVENT_LBUTTONUP:
            # Finish drawing
            if self.drawing:
                self.current_area.append((x, y))
                # Ensure consistent rectangle (top-left to bottom-right)
                x1, y1 = self.current_area[0]
                x2, y2 = self.current_area[1]
                
                # Normalize coordinates
                area = [
                    min(x1, x2),  # x
                    min(y1, y2),  # y
                    abs(x2 - x1),  # width
                    abs(y2 - y1)   # height
                ]
                
                # Add area to list
                self.areas.append(area)
                
                # Draw final rectangle
                cv2.rectangle(self.image, 
                              (area[0], area[1]), 
                              (area[0] + area[2], area[1] + area[3]), 
                              (0, 255, 0), 2)
                
                self.drawing = False

    def select_areas(self):
        """
        Open window to select areas
        """
        window_name = 'Area Selector (Press ESC to finish)'
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, self.draw_rectangle)

        while True:
            cv2.imshow(window_name, self.image)
            key = cv2.waitKey(1) & 0xFF

            # Add text to show current number of areas
            area_text = f'Areas selected: {len(self.areas)}'
            cv2.putText(self.image, area_text, (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Finish selection on ESC key
            if key == 27:  # ESC key
                break

        cv2.destroyAllWindows()
        return self.areas

    def save_areas_to_yaml(self, output_path='detection_areas.yaml'):
        """
        Save selected areas to YAML file
        """
        # Prepare areas dictionary
        areas_dict = {f'area_{i+1}': area for i, area in enumerate(self.areas)}
        
        # Save to YAML
        with open(output_path, 'w') as f:
            yaml.dump(areas_dict, f, default_flow_style=False)
        
        print(f"Areas saved to {output_path}")

def main():
    # Prompt for image path
    image_path = input("Enter the path to the image: ")
    
    # Create area selector
    selector = AreaSelector(image_path)
    
    # Select areas
    areas = selector.select_areas()
    
    # Save areas to YAML
    selector.save_areas_to_yaml()

    print("Area selection complete. Check detection_areas.yaml")

if __name__ == '__main__':
    main()