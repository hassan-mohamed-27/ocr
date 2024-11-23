
# Invoice OCR App

The Invoice OCR App is a comprehensive application designed to extract essential information from invoice images using multiple OCR (Optical Character Recognition) backends. Leveraging Flask for the backend and integrating with Google Drive for storage and monitoring, this app provides a robust solution for automating invoice data extraction.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [OCR Backends](#ocr-backends)
  - [Pytesseract](#pytesseract)
  - [EasyOCR](#easyocr)
  - [Google Generative AI (GenAI)](#google-generative-ai-genai)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)
- [License](#license)


## Features

- **File Uploads:** Upload invoice images and YAML files defining detection areas.
- **Multiple OCR Backends:**
    - Pytesseract: Utilizes a custom model fine-tuned for Arabic numbers.
    - EasyOCR: Supports multiple languages with high accuracy.
    - Google Generative AI (GenAI): Leverages Google's advanced generative models for OCR.
- **Google Drive Integration:** Monitor specific Google Drive folders for new invoice uploads and process them automatically.
- **Data Extraction:** Extracts specific fields such as invoice number, date, amounts, etc., from processed invoices.
- **Logging:** Comprehensive logging for monitoring application behavior and troubleshooting.


## Prerequisites

- **Python 3.7+:**  [Download Python](https://www.python.org/downloads/)
- **Google Drive API Credentials:** Obtain `client_secret.json` from the Google Cloud Console.
- **Tesseract OCR:**
    - **Windows:** [Download Tesseract OCR Installer](https://tesseract-ocr.github.io/tessdoc/Downloads)
    - **Linux:** `sudo apt-get install tesseract-ocr`
    - **macOS:** `brew install tesseract`
- **Google Generative AI API Key:** Obtain an API key from the Google Cloud Console.


## Installation

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   ```

2. **Create a Virtual Environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the Virtual Environment:**
   - **Windows:** `venv\Scripts\activate`
   - **Linux/macOS:** `source venv/bin/activate`

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up Tesseract Path (If Necessary):**
   If Tesseract is not in your system's PATH, specify its location in `app/services/ocr/pytesseract_backend.py`.


## Configuration

1. **Google Drive API Credentials:** Place your `client_secret.json` file in the project's root directory.  The application will generate a `token.json` file upon first authentication.


3. **Detection Areas YAML:** Define detection areas in a YAML file (`detection_areas.yaml`) specifying regions in the invoice images for OCR using helper script.



## Usage

1. **Start the Flask Server:**
   ```bash
   python app.py 
   ```
   The server will run on `http://localhost:5000` by default.


2. **Interact with the API:** Use tools like Postman or cURL to interact with the API endpoints described below.




## API Endpoints

| Method | Endpoint         | Description                                           |
|--------|-----------------|-------------------------------------------------------|
| GET    | `/login`         | Authenticate with Google Drive.                       |
| POST   | `/upload_yaml`   | Upload YAML configuration for detection areas.        |
| POST   | `/upload_image`  | Upload an invoice image.                              |
| POST   | `/extract_invoice`| Perform OCR on an invoice image.                     |
| POST   | `/monitor`       | Start monitoring a Google Drive folder.                |
detailed description  is in the postman collection 





## OCR Backends



### Pytesseract

- Uses Tesseract OCR with a custom model for Arabic numbers.  Ensure the custom model is correctly placed and referenced in `pytesseract_backend.py`.


### EasyOCR

- Supports multiple languages and provides high accuracy. Requires no additional configuration.


### Google Generative AI (GenAI)

- Leverages Google's advanced gmini models for OCR. Requires a GenAI API key (set as an environment variable).


## Folder Structure


The project follows this structure:

```
project/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── monitor.py
│   │   ├── ocr.py
│   │   └── upload.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── google_drive_service.py
│   │   └── ocr/
│   │       ├── __init__.py
│   │       ├── ocr_interface.py
│   │       ├── pytesseract_backend.py
│   │       ├── easyocr_backend.py
│   │       └── genai_backend.py
│   └── utils/
│       ├── __init__.py
│       ├── text_parser.py
│       └── config.py
│
├── downloads/
│
├── client_secret.json
├── token.json
├── requirements.txt
└── README.md 
```
