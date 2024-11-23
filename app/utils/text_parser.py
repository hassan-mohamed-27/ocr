import os
import logging

def parse_detected_text(file_path):
    """
    Parse the detected text file in plain text format with area mapping to extract invoice details.

    :param file_path: Path to the detected text file
    :return: Dictionary with extracted fields
    """
    extracted = {
        "invoice_number": None,
        "date": None,
        "second_product_amount": None,
        "total_amount": None
    }

    area_mapping = {
        "area_1": "invoice_number",
        "area_2": "date",
        "area_3": "second_product_amount",
        "area_4": "total_amount"
    }

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        areas = content.split("--------------------------------------------------")

        for area in areas:
            lines = area.strip().split("\n")
            if lines:
                header = lines[0]
                if header.startswith("Text in "):
                    # Extract the area number
                    current_area = header.split(" ")[2].strip(":")
                    field = area_mapping.get(current_area)
                    if field:
                        # Get everything after "Text in area_X: "
                        value = header[header.find(": ") + 2:].strip()
                        extracted[field] = value
    except Exception as e:
        logging.error(f"Error parsing detected text: {e}")

    return extracted